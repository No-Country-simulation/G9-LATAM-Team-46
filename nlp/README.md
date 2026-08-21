# techmind-nlp-pipeline

## ¿Qué hace este proyecto?

Le das un texto técnico (por ejemplo, la descripción de un artículo o
una pregunta de programación) y el sistema automáticamente:
1. **Identifica de qué tema trata** — Backend, Frontend, Seguridad, Bases
   de Datos, y otras 4 categorías más (8 en total).
2. **Extrae los términos más importantes** del texto.
3. Funciona **tanto en español como en inglés**.

Esta parte del proyecto (`techmind-nlp-pipeline`) es la pieza que deja
el modelo ya entrenado, probado y listo para
que el equipo de backend lo conecte a la API que usarán los usuarios
finales.

---

Pipeline de procesamiento de texto y preparación para producción del
clasificador de contenido técnico (Hackathon ONE G9 - Alura/Oracle).

Rol: Ingeniero NLP y Preparación para Producción.

Entrenado con el dataset bilingüe (inglés + español) del proyecto.
Además del clasificador, expone el motor de contenido relacionado y los
términos de los botones de sugerencia.

## Arquitectura

Cada módulo tiene una única responsabilidad (alta cohesión) y depende
de abstracciones, no de implementaciones concretas (bajo acoplamiento,
inversión de dependencias) — esto hace que cada pieza se pueda probar
y cambiar de forma aislada.

```
techmind-nlp-pipeline/
├── src/
│   ├── __init__.py
│   ├── exceptions.py        # Jerarquía de errores propios del dominio
│   ├── config.py            # Rutas y umbrales centralizados
│   ├── cleaning.py          # Limpieza de texto (réplica exacta de la del modelo)
│   ├── keywords.py          # Extracción de palabras clave por pesos TF-IDF
│   ├── model_repository.py  # Carga y caché del Pipeline serializado
│   ├── schemas.py           # Contrato de datos tipado (ResultadoClasificacion)
│   ├── classifier.py        # Orquesta: limpieza -> predicción -> palabras clave
│   ├── recommender.py       # Contenido relacionado por similitud del coseno
│   └── inference.py         # Fachada para la API: procesar_contenido() + precargar_modelo()
├── scripts/
│   ├── validar_modelo.py         # Valida carga del modelo y predicciones de prueba
│   └── simular_entrega_json.py   # Corre el pipeline completo y muestra el JSON final
├── models/
│   ├── README.md                      # Detalle de los artefactos
│   ├── modelo_techmind_v2.joblib      # El clasificador
│   ├── matriz_historica.pkl           # Corpus vectorizado, para contenido relacionado
│   ├── sugerencias_botones.json       # Términos de los botones
│   └── diccionario_categorias.json    # Las 8 categorías y sus términos
├── tests/
│   ├── __init__.py
│   ├── test_cleaning.py
│   ├── test_keywords.py
│   ├── test_model_repository.py
│   ├── test_classifier.py
│   ├── test_schemas.py       # Contrato de salida
│   └── test_inference.py     # Fachada que consume la API
├── pytest.ini
├── requirements.txt
├── NOTAS_PARA_MODELADO.md   # Requisitos para reentrenar el modelo
├── README_BACKEND.md        # Lo que queda del lado de la API
└── README.md
```

**Nota:** los artefactos **sí se versionan** en el repo y la API los toma
de `models/`. El `.joblib` pesa 5,9 MB y `matriz_historica.pkl` 47 MB,
ambos por debajo del límite de 100 MB de GitHub, así que no hace falta
Git LFS.

## Cómo levantar el entorno (local, VSCode)

```bash
python -m venv .venv

# En Windows:
 .venv\Scripts\Activate.ps1

# En Linux - Mac
source .venv/bin/activate   
     
pip install -r requirements.txt
```

No hace falta descargar nada de NLTK. Las palabras clave salen de los
pesos TF-IDF del propio vectorizador, cuyo vocabulario ya es bilingüe
porque así se entrenó.

## Cómo correr las pruebas

```bash
pytest
```

**56 pruebas, todas pasando.** Ninguna necesita el `.joblib` real:
`test_cleaning.py` y `test_schemas.py` usan datos sintéticos, y el
resto entrena Pipelines pequeños en memoria (ver el uso de "dobles de
prueba" en `test_classifier.py`). La suite corre rápido y sin depender
de `models/`.

`pytest.ini` fija `pythonpath = .`, así que los imports `from src...`
funcionan desde cualquier directorio.

## Cómo validar contra el modelo real

Las pruebas no tocan el `.joblib` de producción (usan modelos pequeños en
memoria), así que hace falta una comprobación aparte. Con el modelo en
`models/`:

```bash
python scripts/validar_modelo.py
```

Verifica tres cosas: que el `.joblib` cargue en el entorno actual, que las
8 categorías del modelo coincidan con las esperadas, y que la inferencia
funcione en inglés y español. Salida esperada:

```
1) Cargando el modelo...
   OK
2) Verificando categorías del modelo...
   OK, coinciden con las 8 categorías esperadas
3) Probando inferencia con textos de ejemplo (EN + ES)...
   CORS error in Flask: 'How to fix CORS error in a Flask REST API'
   -> Backend  (probabilidad: 0.819)
      palabras clave: ['cors', 'flask', 'rest api', 'error', 'fix']
   ...
Validación completa.
```

**Correr esto después de cada cambio de modelo**, y antes de cualquier
demo. Es lo único que detecta un `.joblib` entrenado con versiones
incompatibles de scikit-learn o numpy: el pipeline traduce ese fallo a
`ModeloNoDisponibleError`, pero conviene descubrirlo aquí y no en vivo.

Para ver el JSON completo que recibiría la API, con más casos de prueba:

```bash
python scripts/simular_entrega_json.py
```

## Contrato de salida del pipeline de inferencia

```python
from src.inference import procesar_contenido

resultado = procesar_contenido(titulo="...", texto="...")
```

```json
{
  "categoria": "Backend",
  "probabilidad": 0.99,
  "informacion_adicional": ["apis rest", "java spring", "conceptos", "creacion", "utilizando"]
}
```

**Sobre `informacion_adicional`:** el vectorizador del modelo v2 se
entrenó con `ngram_range=(1, 2)`, así que los términos pueden ser
palabras sueltas (`"docker"`) o pares (`"apis rest"`). Van ordenados de
mayor a menor peso TF-IDF. La cantidad se controla con
`config.TOP_N_PALABRAS_CLAVE` (actualmente **5**; la función de
referencia del notebook de modelado usa 4 — si se quiere el mismo
resultado en la demo, hay que igualar ese valor).

Si `probabilidad` cae por debajo de 0.5 (`config.UMBRAL_CATEGORIA_ALTERNATIVA`),
se agrega un campo adicional con la segunda categoría candidata:

```json
{
  "categoria": "Backend",
  "probabilidad": 0.2,
  "informacion_adicional": ["consulta", "optimizar", "tarda"],
  "categoria_alternativa": "Bases de Datos"
}
```

Todos los valores son tipos nativos de Python (`str`, `float`, `list`),
no tipos de numpy — hay una prueba que lo verifica explícitamente.

## Cómo integrarlo en la API

**1. Precargar el modelo al arrancar.** Sin esto, el primer usuario paga
el costo de leer el `.joblib` y un modelo faltante se descubre en pleno
request en vez de al levantar el servicio:

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.inference import precargar_modelo

@asynccontextmanager
async def lifespan(app: FastAPI):
    precargar_modelo()   # falla acá si el modelo no está — que es lo que queremos
    yield

app = FastAPI(lifespan=lifespan)
```

**2. Usar `procesar_contenido()`, no la función `predecir()` del
notebook.** Son distintas: `predecir()` limpia solo el texto, pero el
modelo se entrenó con `titulo + " " + texto`. Este pipeline replica la
concatenación del entrenamiento; la del notebook no, y alimentar al
modelo con una entrada distinta a la que aprendió degrada la predicción.

**3. Traducir las excepciones a códigos HTTP** (ver la tabla siguiente).

## Manejo de errores (para quien integre esto en la API)

Todas las excepciones propias heredan de `TechMindNLPError`
(`src/exceptions.py`). La API debe capturarlas y traducirlas a códigos
HTTP apropiados:

| Excepción | Causa | Código HTTP sugerido |
|---|---|---|
| `EntradaInvalidaError` | `titulo`/`texto` no son `str` | 400 |
| `TextoVacioError` | Texto vacío o sin contenido procesable | 400 |
| `ModeloNoDisponibleError` | El `.joblib` no existe o no cargó | 503 |
| `ModeloInvalidoError` | El `.joblib` cargado no es válido | 503 |

```python
from src.inference import procesar_contenido
from src.exceptions import TechMindNLPError

try:
    resultado = procesar_contenido(titulo, texto)
except TechMindNLPError as error:
    # traducir a respuesta HTTP según el tipo de error
    ...
```

## Requisitos que debe cumplir el modelo

`RepositorioModelo` valida esto al cargar y rechaza el `.joblib` con
`ModeloInvalidoError` si algo falta. Si el equipo de modelado entrega
una versión nueva, debe cumplir:

- Ser un `sklearn.pipeline.Pipeline` **entrenado** (tiene `classes_`).
- Exponer **`predict_proba`** — se usa para el campo `probabilidad` y
  para elegir la categoría alternativa. Un `LinearSVC` no sirve tal
  cual; habría que envolverlo en `CalibratedClassifierCV`.
- Tener el vectorizador en un paso llamado exactamente **`tfidf`** — de
  ahí se sacan las palabras clave.
- Haber sido entrenado con texto procesado por una función de limpieza
  **idéntica** a `src/cleaning.py`.

## Modelo

Ver `models/README.md` para el detalle completo (hiperparámetros,
accuracy, por qué es un solo archivo). `scikit-learn==1.8.0` confirmado
y fijado en `requirements.txt`.

Resumen del modelo vigente: `TfidfVectorizer(ngram_range=(1,2), min_df=5,
max_features=60000)` + `LogisticRegression(C=4.0, max_iter=1000,
class_weight='balanced')`. Sobre un test estratificado de 7.652 textos:
F1 macro 0.7549, accuracy 0.7530, y F1 por categoría entre 0.63 (Backend)
y 0.85 (Mobile). Validación cruzada de 5 particiones: 0.7508 ± 0.0019.

## Estado actual

- [x] Estructura del proyecto + `requirements.txt`
- [x] Limpieza de texto que replica la del entrenamiento: conserva
      `+ # . _ - /` y los dígitos, para que `C++`, `C#`, `CI/CD` y
      `HTML5` lleguen enteros al modelo
- [x] Extracción de palabras clave (pesos TF-IDF, sin dependencia de NLTK)
- [x] Filtro de n-gramas redundantes y de palabras funcionales
- [x] Motor de contenido relacionado (`src/recommender.py`)
- [x] Pipeline de inferencia completo, con manejo de errores tipado
- [x] Modularización aplicando SOLID (ver "Arquitectura")
- [x] Pruebas automatizadas para cada módulo (56/56 pasando)
- [x] Rutas independientes del directorio de trabajo y de la disposición
      de carpetas, con `TECHMIND_MODELOS` por encima
- [x] Precarga del modelo para el arranque de la API
- [x] Validado con el `.joblib` real (`scripts/validar_modelo.py`):
      carga OK, 8/8 categorías, inferencia correcta en EN y ES

## Contenido relacionado y botones de sugerencia

Además del clasificador, `models/` trae dos artefactos que alimentan
funciones de la interfaz. Los dos salen del mismo vectorizador, así que
hablan del mismo vocabulario que el modelo entiende.

### `matriz_historica.pkl` — contenido relacionado

Los 38.257 documentos del corpus vectorizados, con sus IDs, títulos y
categorías. `src/recommender.py` compara contra ellos el texto que llega
y devuelve los más parecidos por similitud del coseno.

```python
from src.config import MATRIZ_HISTORICA_PATH
from src.recommender import RecomendadorContenido

recomendador = RecomendadorContenido(MATRIZ_HISTORICA_PATH)   # una sola vez
recomendador.recomendar(f"{titulo} {texto}", top_n=3)
```

No se guarda la matriz completa de similitudes: con 38.257 documentos
serían más de mil cuatrocientos millones de valores, casi todos cercanos
a cero. Se guardan los vectores y se compara contra ellos únicamente el
texto de la consulta, que es una operación por petición.

Devuelve lista vacía cuando nada supera el umbral de 0.10. Es una
respuesta legítima, no un error: no siempre hay contenido relacionado.

### `sugerencias_botones.json` — botones de la pantalla principal

Quince términos técnicos para que alguien que entra por primera vez
pueda probar el sistema sin pensar qué escribir.

```python
import json
from src.config import SUGERENCIAS_PATH

with open(SUGERENCIAS_PATH, encoding="utf-8") as f:
    terminos = json.load(f)["terminos"]
```

No están elegidos a mano: salen de medir la **distintividad** de cada
término —cuánto pesa dentro de su categoría comparado con su peso en el
corpus entero—, con un tope de dos por categoría para que los botones
cubran temas variados. Por frecuencia no serviría: los primeros puestos
se los llevan `the`, `to` y `and`.

Se regeneran corriendo `machine_learning/sugerencias_y_relacionados.ipynb`.

---

Para la lista de lo que queda por hacer del lado de la API, ver
[`README_BACKEND.md`](README_BACKEND.md).
