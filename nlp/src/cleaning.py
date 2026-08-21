"""
Limpieza de texto — réplica exacta del preprocesamiento del notebook
`limpieza_y_eda_techmind_v2.ipynb`, que produjo el dataset con el que
se entrenó el modelo v2.

Este módulo tiene una única responsabilidad: convertir texto crudo en
texto limpio. No sabe nada del modelo, de palabras clave, ni de cómo
se usa el resultado — eso lo mantiene fácil de probar de forma aislada
y reutilizable en cualquier contexto (entrenamiento, inferencia, scripts
de análisis).

IMPORTANTE: `limpiar_texto()` debe seguir siendo una réplica exacta de
la limpieza usada para entrenar. El `TfidfVectorizer` se ajustó sobre
texto procesado exactamente así — cualquier diferencia, por mínima que
sea, genera vectores distintos a los que el modelo aprendió a
interpretar.

Dos criterios de esa limpieza merecen explicación, porque son lo que la
distingue de una limpieza genérica:

1. Se conservan `+ # . _ - /`. Sin ellos, los términos que más
   distinguen a una categoría se destruyen o se mutilan: `C++` y `C#`
   quedan en nada, `CI/CD` desaparece, `node.js` se reduce a `node`.
   Son justamente las palabras con mayor poder discriminante.

2. No se pasa a minúsculas ni se eliminan dígitos. El `TfidfVectorizer`
   ya normaliza a minúsculas por su cuenta, y los dígitos forman parte
   de términos técnicos reales (`HTML5`, `ES6`, `Python 3`).
"""

import re

# Los patrones se compilan una sola vez a nivel de módulo (no en cada
# llamada) por eficiencia — limpiar_texto() se invoca en cada request
# de la API.
_PATRON_PUBLICADO = re.compile(r"Published.*?:.*", flags=re.IGNORECASE)
_PATRON_URL = re.compile(r"http\S+|www\S+|https\S+", flags=re.MULTILINE)
_PATRON_SALTOS = re.compile(r"\n|\r")
# Se conservan los caracteres técnicos + # . _ - / (ver docstring).
_PATRON_NO_PERMITIDO = re.compile(r"[^áéíóúüñA-Za-z0-9\s\+\#\.\_\-\/]")
_PATRON_ESPACIOS = re.compile(r"\s+")

# Normalización ortográfica: colapsa repeticiones y corrige erratas
# frecuentes del corpus (mismo criterio del notebook de entrenamiento).
_PATRON_LETRAS_REPETIDAS = re.compile(r"(.)\1{2,}")
_PATRON_PUNTUACION_REPETIDA = re.compile(r"([!?.,])\1{1,}")

_CORRECCIONES_COMUNES: dict[str, str] = {
    r"\bteh\b": "the",
    r"\brecieve\b": "receive",
    r"\bwich\b": "which",
    r"\bwierd\b": "weird",
    r"\bthier\b": "their",
    r"\baltough\b": "although",
    r"\bfuntion\b": "function",
    r"\bfuncion\b": "función",
    r"\bcompatibilty\b": "compatibility",
}

# Se compilan una vez, igual que el resto de los patrones.
_CORRECCIONES_COMPILADAS = [
    (re.compile(patron, flags=re.IGNORECASE), reemplazo)
    for patron, reemplazo in _CORRECCIONES_COMUNES.items()
]


def _corregir_ortografia(texto: str) -> str:
    """Colapsa caracteres repetidos y corrige erratas frecuentes.

    Separada de `limpiar_texto()` porque resuelve un problema distinto:
    una normaliza el formato, la otra el contenido. Mantenerlas aparte
    permite probarlas por separado.
    """
    texto = _PATRON_LETRAS_REPETIDAS.sub(r"\1\1", texto)
    texto = _PATRON_PUNTUACION_REPETIDA.sub(r"\1", texto)

    for patron, reemplazo in _CORRECCIONES_COMPILADAS:
        texto = patron.sub(reemplazo, texto)

    return _PATRON_ESPACIOS.sub(" ", texto).strip()


def limpiar_texto(texto: str) -> str:
    """Limpia un texto crudo con el mismo criterio usado para entrenar
    el modelo v2: sin encabezados de publicación, sin URLs, sin saltos
    de línea, conservando los caracteres técnicos `+ # . _ - /` y con
    la ortografía normalizada.

    Args:
        texto: Texto crudo de entrada. Cualquier valor que no sea `str`
            se trata como texto vacío (ver Returns).

    Returns:
        Texto limpio y normalizado, listo para pasar al vectorizador.
        Devuelve cadena vacía si `texto` no es un `str` o si no queda
        nada después de la limpieza.
    """
    if not isinstance(texto, str):
        return ""

    texto = _PATRON_PUBLICADO.sub("", texto)
    texto = _PATRON_URL.sub("", texto)
    texto = _PATRON_SALTOS.sub(" ", texto)
    texto = _PATRON_NO_PERMITIDO.sub("", texto)
    texto = _PATRON_ESPACIOS.sub(" ", texto).strip()

    return _corregir_ortografia(texto)
