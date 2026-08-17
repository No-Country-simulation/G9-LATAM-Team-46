"""
Configuración centralizada del pipeline: rutas y umbrales.

Concentrar estos valores aquí (en vez de tenerlos repartidos como
literales dentro de la lógica de negocio) es lo que permite ajustarlos
sin tocar código, y evita que el mismo número aparezca "mágicamente"
en varios archivos a la vez.
"""

from pathlib import Path

# Raíz del proyecto, calculada a partir de la ubicación de este archivo
# (src/config.py -> src/ -> raíz). Anclar las rutas aquí, en vez de usar
# rutas relativas al directorio de trabajo, evita que el modelo "desaparezca"
# cuando la API se levanta desde otra carpeta (ej. `uvicorn` lanzado desde
# el directorio del backend, o un contenedor con otro WORKDIR).
RAIZ_PROYECTO: Path = Path(__file__).resolve().parent.parent

# Ruta del Pipeline serializado (TF-IDF + clasificador en un solo objeto,
# modelo v2 entrenado con dataset bilingüe EN/ES).
MODELO_PATH: Path = RAIZ_PROYECTO / "models" / "modelo_techmind_v2.joblib"

# Si la probabilidad de la predicción principal cae por debajo de este
# umbral, la respuesta incluye una categoría alternativa (recomendación
# del equipo de modelado documentada en el notebook v2).
UMBRAL_CATEGORIA_ALTERNATIVA: float = 0.5

# Cantidad de palabras clave a devolver por defecto en la respuesta.
# NOTA: el vectorizador del modelo v2 se entrenó con ngram_range=(1, 2),
# así que estos "términos" pueden ser unigramas ("docker") o bigramas
# ("apis rest"). Es el comportamiento esperado, no un error.
TOP_N_PALABRAS_CLAVE: int = 5

# Longitud mínima de palabra que conserva la función de limpieza
# (réplica del criterio usado para entrenar el modelo v2).
LONGITUD_MINIMA_PALABRA: int = 2
