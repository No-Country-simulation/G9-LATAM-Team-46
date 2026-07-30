"""
Módulo de extracción de palabras clave.

Identifica los términos más relevantes de un texto técnico para
enriquecer la respuesta de la API (más allá de solo la categoría).
"""

from typing import List


def extraer_palabras_clave(texto: str, top_n: int = 10) -> List[str]:
    """Extrae las `top_n` palabras clave más relevantes de un texto.

    Args:
        texto: Texto (idealmente ya preprocesado) del que extraer keywords.
        top_n: Cantidad máxima de palabras clave a devolver.

    Returns:
        Lista de palabras clave ordenadas por relevancia.
    """
    raise NotImplementedError  # Se implementa en el Bloque 3
