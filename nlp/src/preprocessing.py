"""
Módulo de preprocesamiento de texto.

Contiene dos familias de funciones con propósitos distintos:

1. `limpiar_texto()` — réplica EXACTA de la función `limpiar()` del
   notebook de modelado. Es la que se debe usar antes de vectorizar
   texto para clasificación, porque el TfidfVectorizer fue entrenado
   sobre texto procesado exactamente así (minúsculas, regex simple,
   sin lematizar). Cualquier diferencia puede generar vectores que el
   modelo no interpreta correctamente.

2. `tokenizar()`, `eliminar_stopwords()`, `lematizar()` — utilidades de
   NLP más completas, pensadas para el módulo de extracción de
   palabras clave (Bloque 3), NO para el pipeline de clasificación
   (el TfidfVectorizer ya elimina stopwords en inglés internamente
   con stop_words='english').
"""

import re
from typing import List

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Términos técnicos cortos que no deben filtrarse aunque tengan <=2
# caracteres. DEBE mantenerse idéntico al usado en el notebook de
# modelado (ver limpiar()) para no romper la compatibilidad con el
# vectorizador TF-IDF ya entrenado.
TERMINOS_CORTOS = {
    'r', 'c', 'go', 'js', 'ts', 'ai', 'ml', 'db', 'ui', 'ux',
    'os', 'qa', 'ci', 'cd', 'vm', 'C++', 'C#',
}

_lematizador = WordNetLemmatizer()


def limpiar_texto(texto: str) -> str:
    """Réplica exacta de la función limpiar() del equipo de modelado.

    Args:
        texto: Texto crudo (título o cuerpo del contenido).

    Returns:
        Texto limpio: minúsculas, sin URLs/números/puntuación, sin
        tokens de <=2 caracteres salvo los de TERMINOS_CORTOS.
    """
    if not isinstance(texto, str):
        return ""

    texto = texto.lower()
    texto = re.sub(r'[\n\t\r]+', ' ', texto)
    texto = re.sub(r'http\S+|www\.\S+', '', texto)
    texto = re.sub(r'\d+', ' ', texto)
    texto = re.sub(r'[^a-záéíóúüñ\s]', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto)

    palabras = [p for p in texto.split() if len(p) > 2 or p in TERMINOS_CORTOS]
    return " ".join(palabras).strip()


def tokenizar(texto: str) -> List[str]:
    """Divide el texto en una lista de tokens (palabras).

    Pensada para el módulo de extracción de palabras clave (Bloque 3),
    no para el pipeline de clasificación.

    Args:
        texto: Texto (crudo o ya limpio con limpiar_texto).

    Returns:
        Lista de tokens.
    """
    return word_tokenize(texto, language='english')


def eliminar_stopwords(tokens: List[str], idioma: str = 'english') -> List[str]:
    """Elimina palabras vacías (stopwords) de una lista de tokens.

    NOTA: el TfidfVectorizer del modelo ya elimina stopwords en inglés
    internamente, así que esta función no se aplica antes de clasificar.
    Se usa para el módulo de extracción de palabras clave (Bloque 3).

    Args:
        tokens: Lista de tokens.
        idioma: Idioma de las stopwords a usar (default 'english').

    Returns:
        Lista de tokens sin stopwords.
    """
    stop_set = set(stopwords.words(idioma))
    return [t for t in tokens if t.lower() not in stop_set]


def lematizar(tokens: List[str]) -> List[str]:
    """Reduce cada token a su forma base (lema), usando WordNetLemmatizer.

    Pensada para el módulo de extracción de palabras clave (Bloque 3).

    Args:
        tokens: Lista de tokens (idealmente sin stopwords).

    Returns:
        Lista de tokens lematizados.
    """
    return [_lematizador.lemmatize(t) for t in tokens]


def preparar_para_keywords(texto: str) -> List[str]:
    """Pipeline auxiliar: limpia -> tokeniza -> quita stopwords -> lematiza.

    Pensado para alimentar el módulo de extracción de palabras clave
    (Bloque 3). No se usa en el pipeline de clasificación.

    Args:
        texto: Texto crudo (título o cuerpo del contenido).

    Returns:
        Lista de tokens lematizados, sin stopwords.
    """
    texto_limpio = limpiar_texto(texto)
    tokens = tokenizar(texto_limpio)
    tokens = eliminar_stopwords(tokens)
    tokens = lematizar(tokens)
    return tokens
