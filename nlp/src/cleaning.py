"""
Limpieza de texto — réplica exacta de la función `limpiar()` del
notebook de modelado v2.

Este módulo tiene una única responsabilidad: convertir texto crudo en
texto limpio. No sabe nada del modelo, de palabras clave, ni de cómo
se usa el resultado — eso lo mantiene fácil de probar de forma aislada
y reutilizable en cualquier contexto (entrenamiento, inferencia, scripts
de análisis).

IMPORTANTE: la función `limpiar_texto()` debe ser una réplica exacta de
la usada para entrenar el modelo. El `TfidfVectorizer` fue ajustado
sobre texto procesado exactamente así — cualquier diferencia (por
mínima que sea) puede generar vectores distintos a los que el modelo
aprendió a interpretar.
"""

import re

from src.config import LONGITUD_MINIMA_PALABRA

# Los patrones se compilan una sola vez a nivel de módulo (no en cada
# llamada) por eficiencia — limpiar_texto() se invoca en cada request
# de la API.
_PATRON_SALTOS = re.compile(r"[\n\t\r]+")
_PATRON_URL = re.compile(r"http\S+|www\S+|https\S+", flags=re.MULTILINE)
_PATRON_DIGITOS = re.compile(r"\d+")
_PATRON_NO_ALFANUMERICO = re.compile(r"[^áéíóúüñA-Za-z0-9\s]")
_PATRON_ESPACIOS = re.compile(r"\s+")


def limpiar_texto(texto: str) -> str:
    """Limpia un texto crudo con el mismo criterio usado para entrenar
    el modelo v2: minúsculas, sin URLs, sin números, sin puntuación,
    sin palabras de longitud menor o igual a `LONGITUD_MINIMA_PALABRA`.

    Args:
        texto: Texto crudo de entrada. Cualquier valor que no sea `str`
            se trata como texto vacío (ver Returns).

    Returns:
        Texto limpio y normalizado, listo para pasar al vectorizador.
        Devuelve cadena vacía si `texto` no es un `str` o si no queda
        ninguna palabra después de la limpieza.
    """
    if not isinstance(texto, str):
        return ""

    texto = texto.lower()
    texto = _PATRON_SALTOS.sub(" ", texto)
    texto = _PATRON_URL.sub("", texto)
    texto = _PATRON_DIGITOS.sub(" ", texto)
    texto = _PATRON_NO_ALFANUMERICO.sub(" ", texto)
    texto = _PATRON_ESPACIOS.sub(" ", texto)

    palabras = [p for p in texto.split() if len(p) > LONGITUD_MINIMA_PALABRA]
    return " ".join(palabras).strip()
