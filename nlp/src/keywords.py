"""
Módulo de extracción de palabras clave.

Identifica los términos más relevantes de un texto técnico para
enriquecer la respuesta de la API (más allá de solo la categoría).
"""

from collections import Counter
from typing import List, Tuple

from src.preprocessing import preparar_para_keywords

# Palabras funcionales que la lista de stopwords en inglés de NLTK NO
# incluye, pero que igual no aportan como palabra clave. Detectado
# durante las pruebas del demo (ej. "another" se coló como keyword).
STOPWORDS_ADICIONALES = {"another", "also", "etc", "eg", "ie", "using"}


def extraer_palabras_clave(texto: str, top_n: int = 10) -> List[Tuple[str, int]]:
    """Extrae las `top_n` palabras clave más frecuentes de un texto.

    Pipeline: limpiar -> tokenizar -> quitar stopwords -> lematizar -> contar.

    Args:
        texto: Texto (título o cuerpo del contenido).
        top_n: Cantidad máxima de palabras clave a devolver.

    Returns:
        Lista de tuplas (palabra, frecuencia), ordenada de mayor a menor
        frecuencia.
    """
    tokens = preparar_para_keywords(texto)
    tokens = [t for t in tokens if t not in STOPWORDS_ADICIONALES]

    conteo = Counter(tokens)
    return conteo.most_common(top_n)
