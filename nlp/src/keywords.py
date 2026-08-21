"""
Extracción de palabras clave a partir de los pesos TF-IDF del propio
vectorizador ya entrenado.

Responsabilidad única: dado un texto ya limpio y un vectorizador TF-IDF
ajustado, devolver sus términos de mayor peso. No sabe cómo se limpia
el texto, ni cómo se carga el modelo, ni qué se hace con el resultado.

Se usan los pesos del vectorizador y no un lematizador externo. El corpus es
bilingüe (EN + ES) y WordNetLemmatizer de NLTK solo tiene lexicón en inglés:
dejaría sin tratar la mitad del contenido. El vocabulario del vectorizador ya
es bilingüe porque así se entrenó, y no agrega una dependencia externa.
"""

from typing import List, Protocol

from sklearn.feature_extraction.text import TfidfVectorizer

# Palabras funcionales del idioma. El vectorizador se entrenó sin lista de
# stopwords porque le aportan algo de señal al clasificador, pero de cara al
# usuario no dicen nada: en "con docker despliegue", "con" pesa alto y no
# describe de qué trata el texto.
#
# La lista sale de medir el corpus: se tomaron 4.000 documentos del histórico y
# se contó qué términos entran a los primeros puestos sin ser técnicos. Se
# mantiene corta a propósito — cubre lo que de verdad aparece y nada más —
# porque un diccionario completo arriesga descartar términos legítimos (`go`
# es un lenguaje, `net` es .NET). El vectorizador ignora los tokens de un solo
# carácter, así que "y", "a" y "o" no hacen falta acá.
_PALABRAS_FUNCIONALES = frozenset({
    # español
    "de", "la", "el", "en", "al", "lo", "se", "su", "es", "un",
    "con", "para", "por", "que", "los", "las", "una", "uno", "del", "sus",
    "como", "este", "esta", "estos", "estas", "sin", "sobre", "entre", "cuando",
    "donde", "desde", "hasta", "muy", "mas", "más", "pero", "porque", "aunque",
    "ser", "son", "esa", "ese", "hay", "han", "fue", "era", "les", "nos",
    # ingles
    "to", "of", "in", "on", "is", "it", "we", "our", "my", "am",
    "at", "be", "as", "by", "an", "us", "me",
    "the", "and", "for", "with", "that", "this", "these", "those", "from",
    "have", "has", "was", "were", "are", "not", "but", "you", "your", "its",
    "can", "will", "would", "should", "could", "which", "when", "where",
    "there", "their", "them", "then", "than", "into", "over", "very", "just",
    "also", "some", "any", "all", "how", "what", "why", "who",
})


class ExtractorPalabrasClave(Protocol):
    """Contrato mínimo que cualquier extractor de palabras clave debe
    cumplir. Definirlo como Protocol (en vez de una clase base abstracta)
    permite sustituir la implementación (ej. por una basada en otro
    algoritmo) sin modificar quien la usa (ClasificadorContenido),
    siempre que respete esta firma - principio de sustitucion de Liskov
    aplicado a un lenguaje sin herencia obligatoria.
    """

    def extraer(self, texto_limpio: str, top_n: int) -> List[str]:
        """Extrae las top_n palabras clave más relevantes de un texto
        ya limpio."""
        ...


class ExtractorPalabrasClaveTfidf:
    """Extrae palabras clave usando los pesos TF-IDF que el vectorizador
    le asigna al texto de entrada — los términos con mayor peso son los
    más "distintivos" para ese texto según el vocabulario del corpus de
    entrenamiento.
    """

    def __init__(self, vectorizador: TfidfVectorizer) -> None:
        """
        Args:
            vectorizador: TfidfVectorizer ya entrenado (fit), normalmente
                el paso 'tfidf' del Pipeline serializado del modelo.
        """
        self._vectorizador = vectorizador
        # El vocabulario se pide una sola vez, al construir el extractor.
        # get_feature_names_out() reconstruye el array completo en cada
        # llamada y con las 60.000 entradas del modelo cuesta ~37 ms:
        # pedirlo en cada peticion dominaria el tiempo de respuesta.
        self._vocabulario = vectorizador.get_feature_names_out()

    def extraer(self, texto_limpio: str, top_n: int) -> List[str]:
        """Extrae las top_n palabras clave de mayor peso TF-IDF.

        Args:
            texto_limpio: Texto ya procesado por cleaning.limpiar_texto.
            top_n: Cantidad máxima de palabras clave a devolver.

        Returns:
            Lista de términos (pueden incluir bigramas, según el
            ngram_range del vectorizador), ordenados de mayor a menor
            peso. Lista vacía si ningún término del texto está en el
            vocabulario del vectorizador.
        """
        if not texto_limpio:
            return []

        vector = self._vectorizador.transform([texto_limpio])
        vocabulario = self._vocabulario
        pesos = vector.toarray()[0]

        indices_ordenados = pesos.argsort()[::-1]
        candidatos = [
            termino
            for indice in indices_ordenados[: top_n * self._FACTOR_CANDIDATOS]
            if pesos[indice] > 0
            and self._es_termino_util(termino := str(vocabulario[indice]))
        ]
        return self._filtrar_redundantes(candidatos, top_n)

    @staticmethod
    def _es_termino_util(termino: str) -> bool:
        """Descarta los términos que no le dicen nada a quien lee la respuesta.

        Basta con que una parte sea funcional para descartar el término
        entero: "the app" y "de react" ocupan un lugar y no dicen nada que
        "app" o "react" no digan solos, y el vectorizador ya puntúa esos
        unigramas por separado. Medido sobre el histórico, tres de cada
        cuatro bigramas que llegaban a la respuesta eran de esta forma.
        """
        return not any(
            parte in _PALABRAS_FUNCIONALES for parte in termino.split()
        )

    # Se piden más candidatos de los necesarios porque el filtro de
    # redundancia descarta varios; con bigramas se descartan bastantes.
    _FACTOR_CANDIDATOS = 4

    @staticmethod
    def _filtrar_redundantes(candidatos: List[str], top_n: int) -> List[str]:
        """Descarta términos que no aportan ninguna palabra nueva.

        Con ngram_range=(1, 2) el vectorizador puntúa alto tanto al bigrama
        como a sus partes, así que la lista sale repetitiva: por ejemplo
        ["apis rest", "java spring", "spring boot", "boot", "spring"] son
        cinco términos que cubren solo cinco palabras distintas. "boot" y
        "spring" ya están contenidos en los bigramas anteriores y ocupan
        lugares que podrían llevar información nueva.

        Se conserva el orden por peso: un término entra si aporta al menos
        una palabra que ningún término ya aceptado contenía.
        """
        seleccionados: List[str] = []
        palabras_cubiertas: set = set()

        for termino in candidatos:
            palabras = set(termino.split())
            if palabras - palabras_cubiertas:
                seleccionados.append(termino)
                palabras_cubiertas |= palabras
            if len(seleccionados) == top_n:
                break

        return seleccionados
