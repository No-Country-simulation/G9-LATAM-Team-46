"""
Extracción de palabras clave a partir de los pesos TF-IDF del propio
vectorizador ya entrenado.

Responsabilidad única: dado un texto ya limpio y un vectorizador TF-IDF
ajustado, devolver sus términos de mayor peso. No sabe cómo se limpia
el texto, ni cómo se carga el modelo, ni qué se hace con el resultado.

Este enfoque reemplaza la lematización con NLTK (como se hacía en la v1
del pipeline): WordNetLemmatizer de NLTK solo tiene lexicón en inglés, así
que con el dataset bilingüe (EN + ES) dejaba de tener sentido para la
mitad del contenido. Usar los pesos del vectorizador resuelve esto de
raíz — el vocabulario ya es bilingüe porque así se entrenó — y además
elimina una dependencia externa (nltk + descarga de corpus).
"""

from typing import List, Protocol

from sklearn.feature_extraction.text import TfidfVectorizer


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
        vocabulario = self._vectorizador.get_feature_names_out()
        pesos = vector.toarray()[0]

        indices_ordenados = pesos.argsort()[::-1]
        candidatos = [
            str(vocabulario[indice])
            for indice in indices_ordenados[: top_n * self._FACTOR_CANDIDATOS]
            if pesos[indice] > 0
        ]
        return self._filtrar_redundantes(candidatos, top_n)

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
