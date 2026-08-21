import logging
from pathlib import Path

import pandas as pd

from app.core.config import settings
from app.ml.loader import descargar_archivo  

logger = logging.getLogger(__name__)

RUTA_DATASET = Path(__file__).resolve().parent / "techmind_dataset_v2.csv"

_dataset = None  

COLUMNAS_NECESARIAS = ["titulo", "texto", "categoria", "palabras_clave"]


def cargar_dataset():
    global _dataset
    if _dataset is not None:
        return _dataset

    if not RUTA_DATASET.exists():
        if not settings.dataset_url:
            logger.warning("Dataset no encontrado localmente y falta DATASET_URL en el entorno")
            return None
        try:
            logger.info("Dataset no encontrado localmente, descargando desde OCI...")
            descargar_archivo(settings.dataset_url, RUTA_DATASET)
        except Exception as e:
            logger.error(f"Fallo al descargar el dataset: {e}")
            return None

    try:
        df = pd.read_csv(RUTA_DATASET, usecols=COLUMNAS_NECESARIAS)
        _dataset = df
        logger.info(f"Dataset cargado en memoria: {len(df)} filas")
    except Exception as e:
        logger.error(f"Fallo al leer el dataset descargado: {e}")
        return None

    return _dataset