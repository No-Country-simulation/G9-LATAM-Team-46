"""
Pipeline de inferencia: texto crudo -> categoría + palabras clave.

Este módulo es el que la API REST va a invocar directamente. Une los
módulos de preprocessing.py y keywords.py con el modelo serializado
(.joblib) entrenado por el equipo de modelado.
"""

import os
from typing import Dict

# Rutas por defecto de los artefactos serializados.
# Ajustar si el equipo de modelado entrega otros nombres de archivo.
MODELO_PATH = os.path.join("models", "modelo_techmind_v1.joblib")
VECTORIZADOR_PATH = os.path.join("models", "vectorizador_tfidf_v1.joblib")


def cargar_modelo(modelo_path: str = MODELO_PATH, vectorizador_path: str = VECTORIZADOR_PATH):
    """Carga el modelo y el vectorizador entrenados desde disco.

    Args:
        modelo_path: Ruta al archivo .joblib del modelo.
        vectorizador_path: Ruta al archivo .joblib del vectorizador TF-IDF.

    Returns:
        Tupla (modelo, vectorizador).
    """
    raise NotImplementedError  # Se implementa en el Bloque 4/6


def procesar_contenido(titulo: str, texto: str) -> Dict:
    """Pipeline completo de inferencia.

    Recibe título y texto por separado, los limpia, los vectoriza,
    predice la categoría y extrae palabras clave.

    Args:
        titulo: Título del contenido técnico.
        texto: Cuerpo del contenido técnico.

    Returns:
        Diccionario con el contrato de salida acordado con el equipo:
        {"categoria": str, "probabilidad": float, "informacion_adicional": dict}
    """
    raise NotImplementedError  # Se implementa en el Bloque 4
