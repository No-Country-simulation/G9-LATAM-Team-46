"""
Pipeline de inferencia: texto crudo -> categoría + palabras clave.

Este módulo es el que la API REST va a llamar (invocar) directamente. Une los
módulos de preprocessing.py y keywords.py con el modelo serializado
(.joblib) entrenado por el equipo de modelado.
"""

import os
from typing import Dict, Optional, Tuple

import joblib

from src.keywords import extraer_palabras_clave
from src.preprocessing import limpiar_texto

# Rutas por defecto de los artefactos serializados.
MODELO_PATH = os.path.join("models", "modelo_techmind_v1.joblib")
VECTORIZADOR_PATH = os.path.join("models", "vectorizador_tfidf_v1.joblib")

# Umbral de confianza mínima. Confirmado con pruebas reales: cuando el
# vectorizador no reconoce ninguna palabra del texto de entrada (ej. texto
# en un idioma no soportado), la confianza del modelo cae a ~0.16 — apenas
# por encima del azar puro para 8 categorías (1/8 = 0.125). Por debajo de
# este umbral, la predicción se marca como poco confiable en vez de
# presentarse como si fuera un resultado válido.
UMBRAL_CONFIANZA_BAJA = 0.3

_modelo = None
_vectorizador = None


def cargar_modelo(
    modelo_path: str = MODELO_PATH, vectorizador_path: str = VECTORIZADOR_PATH
) -> Tuple[object, object]:
    """Carga el modelo y el vectorizador entrenados desde disco.

    Los guarda en caché a nivel de módulo para no releer el disco en
    cada request cuando la API llame esta función repetidamente.

    Args:
        modelo_path: Ruta al archivo .joblib del modelo.
        vectorizador_path: Ruta al archivo .joblib del vectorizador TF-IDF.

    Returns:
        Tupla (modelo, vectorizador).
    """
    global _modelo, _vectorizador
    if _modelo is None or _vectorizador is None:
        _modelo = joblib.load(modelo_path)
        _vectorizador = joblib.load(vectorizador_path)
    return _modelo, _vectorizador


def procesar_contenido(titulo: str, texto: str, top_n_keywords: int = 5) -> Dict:
    """Pipeline completo de inferencia.

    Recibe título y texto por separado, los limpia, los vectoriza,
    predice la categoría y extrae palabras clave.

    Args:
        titulo: Título del contenido técnico.
        texto: Cuerpo del contenido técnico.
        top_n_keywords: Cantidad de palabras clave a incluir en la respuesta.

    Returns:
        Diccionario con el contrato de salida acordado para la API:
        {
            "categoria": str,
            "confianza": float,
            "confianza_baja": bool,
            "palabras_clave": list[str],
        }
    """
    modelo, vectorizador = cargar_modelo()

    # Mismo orden usado para entrenar: texto primero, título después.
    texto_crudo_completo = f"{texto} {titulo}".strip()
    texto_limpio = limpiar_texto(texto_crudo_completo)

    vector_tfidf = vectorizador.transform([texto_limpio])
    categoria = modelo.predict(vector_tfidf)[0]
    confianza = float(modelo.predict_proba(vector_tfidf).max())

    palabras_clave = [
        palabra
        for palabra, _ in extraer_palabras_clave(texto_crudo_completo, top_n=top_n_keywords)
    ]

    return {
        "categoria": str(categoria),
        "confianza": round(confianza, 3),
        "confianza_baja": confianza < UMBRAL_CONFIANZA_BAJA,
        "palabras_clave": palabras_clave,
    }
