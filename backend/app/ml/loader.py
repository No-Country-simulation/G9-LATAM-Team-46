from pathlib import Path

import joblib

RUTA_MODELO = Path(__file__).resolve().parent / "modelo_techmind_v2.joblib"


def cargar_modelo():
    if not RUTA_MODELO.exists():
        return None
    return joblib.load(RUTA_MODELO)