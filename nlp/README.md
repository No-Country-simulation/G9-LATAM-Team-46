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

**Versión actual: v2** — migrado al modelo entrenado con dataset
bilingüe (inglés + español). Ver "Historial de versiones" al final.

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
│   ├── tokenization.py      # Tokenización y eliminación de stopwords (ES + EN)
│   ├── keywords.py          # Extracción de palabras clave por pesos TF-IDF
│   ├── model_repository.py  # Carga y caché del Pipeline serializado
│   ├── schemas.py           # Contrato de datos tipado (ResultadoClasificacion)
│   ├── classifier.py        # Orquesta: limpieza -> predicción -> palabras clave
│   └── inference.py         # Fachada para la API: procesar_contenido() + precargar_modelo()
├── scripts/
│   ├── validar_modelo.py         # Valida carga del modelo y predicciones de prueba
│   ├── inspeccionar_modelo.py    # Imprime los hiperparámetros reales del vectorizador
│   └── simular_entrega_json.py   # Corre el pipeline completo y muestra el JSON final
├── models/
│   ├── README.md                     # Detalle del modelo v2
│   └── modelo_techmind_v2.joblib     # Modelo real entregado por el equipo de modelado (6,2 MB)
├── tests/
│   ├── __init__.py
│   ├── test_cleaning.py
│   ├── test_tokenization.py
│   ├── test_keywords.py
│   ├── test_model_repository.py
│   ├── test_classifier.py
│   ├── test_schemas.py       # Contrato de salida
│   └── test_inference.py     # Fachada que consume la API
├── pytest.ini
├── requirements.txt
└── README.md
```

**Nota:** el `.joblib` (6,2 MB) **sí se versiona** en el repo, igual que
se hacía con el v1: la API lo toma de `models/`. No requiere Git LFS.

## Cómo levantar el entorno (local, VSCode)

```bash
# scikit-learn==1.6.1 usa la version de python 3.12 o 3.13
# Version de python
python --version
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1

python -m venv .venv

# En Windows:
 .venv\Scripts\Activate.ps1

# En Linux - Mac
source .venv/bin/activate 

# eliminar el entorno
Remove-Item -Recurse -Force .venv
     
pip install -r requirements.txt
```

No hace falta descargar nada de NLTK — el modelo v2 ya no depende de
esa librería (ver "Historial de versiones").

## Cómo correr las pruebas

```bash
pytest
```

**72 pruebas, todas pasando.** Ninguna necesita el `.joblib` real:
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
   -> Backend  (probabilidad: 0.830)
      palabras clave: ['REST API', 'Flask', 'CORS', 'error', 'fix']
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

## Procesamiento NLP para palabras clave

La extracción de palabras clave constituye un proceso independiente de la
clasificación. Para este proceso se realizan las siguientes etapas:

```text
Texto
  ↓
Tokenización
  ↓
Eliminación de stopwords
  ↓
Identificación de términos relevantes
  ↓
Extracción de palabras clave
```

En esta etapa se aplican:

- Tokenización.
- Eliminación de stopwords en español e inglés.
- Identificación de términos relevantes mediante el vocabulario TF-IDF.
- Priorización de términos y bigramas.
- Eliminación de términos redundantes.

### Lematización

La lematización **no se encuentra implementada en la versión actual**. La
decisión de no incorporar un lematizador basado en NLTK/WordNet responde al
carácter bilingüe del corpus (español e inglés) y busca preservar la
compatibilidad con el procesamiento y vocabulario utilizados por el modelo
TF-IDF. Por lo tanto, no debe interpretarse la extracción de palabras clave
como un proceso que incluya lematización.

### Qué usa cada proceso

| Proceso | Tokenización | Stopwords | Lematización | Modelo `.joblib` |
|---|---|---|---|---|
| Clasificación | Interna del TF-IDF | No | No | Sí |
| Palabras clave | Sí | Sí | No | No |

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
accuracy, por qué es un solo archivo). `scikit-learn==1.6.1` confirmado
y fijado en `requirements.txt`.

Resumen del v2 vigente: `TfidfVectorizer(ngram_range=(1,2), sublinear_tf=False,
min_df=5, max_features=60000, stop_words=None)` + `LogisticRegression(C=4.0,
max_iter=1000, class_weight=None)`. Valores verificados directamente
sobre el `.joblib` con `scripts/inspeccionar_modelo.py`. Accuracy 0.7761
sobre test estratificado de 7.658 textos; F1 por categoría entre 0.65
(Backend) y 0.88 (Mobile).

## Estado actual

- [x] Estructura del proyecto + `requirements.txt`
- [x] Limpieza de texto (réplica exacta de la función del modelo v2)
- [x] Extracción de palabras clave (pesos TF-IDF, sin dependencia de NLTK)
- [x] Pipeline de inferencia completo, con manejo de errores tipado
- [x] Modularización aplicando SOLID (ver "Arquitectura")
- [x] Pruebas automatizadas para cada módulo (72/72 pasando)
- [x] Ruta del modelo independiente del directorio de trabajo
- [x] Precarga del modelo para el arranque de la API
- [x] Filtro de n-gramas redundantes en las palabras clave
- [x] Evaluada una alternativa (modelo v3) y descartada con datos —
      ver "Decisión" en `NOTAS_PARA_MODELADO.md`
- [x] Validado con el `.joblib` real del modelo v2 (`scripts/validar_modelo.py`):
      carga OK, 8/8 categorías, inferencia correcta en EN y ES

## Historial de versiones

**v1 → v2:** el equipo migró de un dataset solo en inglés a uno
bilingüe (inglés + español) para soportar mejor el caso de uso con
jurado/empresas de LATAM. Cambios que esto trajo a este pipeline:

- La función de limpieza cambió (orden `título + texto`, sin excepción
  para términos técnicos cortos).
- El modelo pasó de dos archivos (`modelo` + `vectorizador`) a un solo
  `Pipeline` serializado.
- Las palabras clave dejaron de extraerse con NLTK (lematización) y
  pasaron a extraerse de los pesos TF-IDF del propio vectorizador —
  esto también resolvió que `WordNetLemmatizer` (NLTK) solo funciona
  en inglés, lo cual no tenía sentido con contenido en español.
- El contrato de salida se alineó al formato pedido por el hackatón
  (`categoria` + `probabilidad` + `informacion_adicional`), agregando
  `categoria_alternativa` cuando la confianza es baja (recomendación
  del equipo de modelado).

Evidencia de que la migración resolvió el problema real: el mismo texto
en español que con el modelo v1 daba 0.16 de confianza y no reconocía
ninguna palabra, con el modelo v2 reconoce varias palabras reales y
sube a 0.20-0.87 según el caso (ver `resumen_demos_pruebas.md` para el
detalle completo de las pruebas).

## Consideraciones finales

- El `.joblib` corresponde al modelo entrenado por el equipo de Machine
  Learning.
- La limpieza de entrada debe ser compatible con el entrenamiento del modelo.
- La clasificación y la extracción de palabras clave son procesos
  independientes.
- La tokenización y eliminación de stopwords se utilizan en el proceso de
  extracción de palabras clave.
- La lematización no está implementada en la versión actual.
- La extracción de palabras clave utiliza el vocabulario TF-IDF y mecanismos
  de ponderación y filtrado de términos.
- No se debe modificar el `.joblib` para incorporar transformaciones que no
  estuvieron presentes durante su entrenamiento.
- La versión de `scikit-learn` debe mantenerse conforme a `requirements.txt`.
