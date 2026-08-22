# 🧠 TechMind AI — Organización Inteligente del Conocimiento Técnico

Solución de Ciencia de Datos que **recibe contenido técnico** (artículos, documentación, tutoriales, apuntes de estudio) y devuelve, en **JSON**, la información necesaria para organizarlo automáticamente: **categoría**, **nivel de confianza** y **palabras clave**.

Pensada para plataformas educativas, comunidades técnicas y equipos que necesitan **clasificar, consultar y reutilizar** grandes volúmenes de conocimiento sin catalogarlo a mano.

**Hackathon ONE — Alura Latam + Oracle · Equipo 46 (G9 LATAM)**

---

## 🚀 Probalo ahora

| | |
|---|---|
| **Aplicación web** | https://techmind-frontend.vercel.app |
| **API — documentación interactiva** | http://98.81.139.150:8000/docs |

En Swagger podés clasificar un texto sin instalar nada: abrí `POST /contenido`, tocá *Try it out* y pegá cualquier contenido técnico.

**Resultado del modelo:** 75 % de acierto sobre 8 categorías (F1 macro **0.7549**), verificado con validación cruzada de 5 particiones (**0.7508 ± 0.0019**). Frente a una clasificación al azar, que acertaría 14 %, es **24 veces mejor**.

---

## Índice

- [El problema y la solución](#el-problema-y-la-solución)
- [Cómo funciona](#cómo-funciona)
- [Categorías](#categorías)
- [Cómo ejecutar el proyecto](#cómo-ejecutar-el-proyecto)
- [Cómo usar la API](#cómo-usar-la-api)
- [Ejemplos de uso](#ejemplos-de-uso)
- [Integración con OCI](#integración-con-oci)
- [Arquitectura y despliegue](#arquitectura-y-despliegue)
- [Modelo de Machine Learning](#modelo-de-machine-learning)
- [Dataset](#dataset)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Dependencias y versiones](#dependencias-y-versiones)
- [Pruebas](#pruebas)
- [Equipo](#equipo)

---

## El problema y la solución

Estudiantes y profesionales de tecnología consumen a diario una gran cantidad de contenido técnico, y organizarlo, encontrarlo y reutilizarlo después consume mucho tiempo.

TechMind actúa como un **bibliotecario automático**: recibe un contenido, lo lee, decide a qué categoría pertenece, extrae sus términos más relevantes y devuelve una ficha estructurada lista para ser consumida por cualquier aplicación.

| Se le entrega | Devuelve |
|---|---|
| Un artículo, tutorial o apunte técnico | La **categoría** a la que pertenece |
| | La **probabilidad** (qué tan seguro está el modelo) |
| | Las **palabras clave** que lo caracterizan |

Con esa ficha, una plataforma puede construir su base de conocimiento sola: navegar por temas, buscar por palabras clave y encontrar contenidos relacionados.

---

## Cómo funciona

```
   Contenido técnico              API REST (FastAPI)                    Respuesta JSON
   ┌──────────────┐        ┌──────────────────────────┐        ┌────────────────────────┐
   │ título       │───────▶│  validación (Pydantic)   │        │ categoria              │
   │ texto        │        │  limpieza de texto       │───────▶│ probabilidad           │
   └──────────────┘        │  Pipeline TF-IDF + LR    │        │ informacion_adicional  │
                           └──────────────────────────┘        └────────────────────────┘
                                        ▲
                                        │  descarga automática si no está local
                                 ┌──────────────┐
                                 │ OCI Object   │
                                 │   Storage    │
                                 └──────────────┘
```

1. La API recibe `titulo` y `texto` y valida la entrada.
2. Se aplica la **misma función de limpieza** que se usó al entrenar (coherencia entrenamiento/producción).
3. El **Pipeline** (`TF-IDF` + `Regresión Logística`) predice la categoría y su probabilidad.
4. Se extraen las palabras clave con mayor peso TF-IDF dentro del texto.
5. Se devuelve todo en JSON.

---

## Categorías

El modelo clasifica en **8 categorías**:

| | | | |
|---|---|---|---|
| `Backend` | `Frontend` | `Mobile` | `Bases de Datos` |
| `Ciencia de Datos` | `DevOps / Cloud` | `Seguridad` | `Programación General` |

Se pueden consultar en vivo con `GET /categorias`.

---

## Cómo ejecutar el proyecto

### Requisitos

- **Python 3.11 o superior**
- `pip` y `venv`

### Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/No-Country-simulation/G9-LATAM-Team-46.git
cd G9-LATAM-Team-46/backend

# 2. Crear y activar el entorno virtual
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS / Linux

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
copy .env.example .env         # Windows
cp .env.example .env           # macOS / Linux
```

### Variables de entorno

| Variable | Obligatoria | Descripción |
|---|---|---|
| `MODELO_URL` | Solo si el modelo no está local | URL del modelo `.joblib` en OCI Object Storage |
| `DEEPSEEK_API_KEY` | Solo para `/chat` | Clave del LLM usado en el endpoint conversacional |
| `DB_USER` `DB_PASSWORD` `DB_HOST` `DB_PORT` `DB_NAME` | No | Conexión MySQL. La API arranca sin ellas |

> El modelo se descarga automáticamente desde OCI si no se encuentra en `backend/app/ml/`.

### Levantar el servidor

```bash
uvicorn app.main:app --reload
```

- API: `http://127.0.0.1:8000`
- **Documentación interactiva (Swagger): `http://127.0.0.1:8000/docs`**

### Con Docker

```bash
cd backend
docker build -t techmind-api -f dockerfile .
docker run -p 8000:8000 --env-file .env techmind-api
```

El proceso completo de despliegue está documentado en [`devops/README.md`](devops/README.md).

---

## Cómo usar la API

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/health` | Estado del servicio |
| `POST` | **`/contenido`** | **Clasifica un contenido técnico** (endpoint principal) |
| `GET` | `/categorias` | Lista las categorías disponibles |
| `POST` | `/biblioteca` | Clasifica y guarda el contenido en la biblioteca del usuario |
| `GET` | `/biblioteca` | Devuelve el historial de contenidos del usuario |
| `GET` | `/modelo/info` | Metadatos del modelo cargado |
| `POST` | `/chat` | Explicación en lenguaje natural del contenido clasificado |

### `POST /contenido`

**Entrada**

| Campo | Tipo | Reglas |
|---|---|---|
| `titulo` | `string` | Obligatorio, no vacío ni solo espacios |
| `texto` | `string` | Obligatorio, no vacío ni solo espacios |

**Salida**

| Campo | Tipo | Descripción |
|---|---|---|
| `categoria` | `string` | Una de las 8 categorías |
| `probabilidad` | `float` | Confianza del modelo, de 0 a 1 |
| `informacion_adicional` | `string[]` | Palabras clave detectadas |

**Errores**

| Código | Cuándo |
|---|---|
| `422` | Falta un campo o está vacío |
| `503` | El modelo todavía no está disponible |
| `500` | Error interno |

---

## Ejemplos de uso

### Ejemplo 1 — Backend

```bash
curl -X POST http://127.0.0.1:8000/contenido \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Introducción a Spring Boot",
    "texto": "En este contenido se presentan los conceptos básicos para la creación de APIs REST utilizando Java y Spring Boot, incluyendo controladores y servicios."
  }'
```

```json
{
  "categoria": "Backend",
  "probabilidad": 1.0,
  "informacion_adicional": ["spring boot", "boot", "apis rest", "controladores"]
}
```

### Ejemplo 2 — DevOps / Cloud

```bash
curl -X POST http://127.0.0.1:8000/contenido \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Despliegue con Docker y Kubernetes",
    "texto": "Cómo empaquetar aplicaciones en contenedores Docker y orquestarlas en un clúster de Kubernetes en la nube con pipelines de CI/CD."
  }'
```

```json
{
  "categoria": "DevOps / Cloud",
  "probabilidad": 0.99,
  "informacion_adicional": ["contenedores docker", "empaquetar", "kubernetes", "despliegue"]
}
```

### Ejemplo 3 — Seguridad

```bash
curl -X POST http://127.0.0.1:8000/contenido \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Autenticación con JWT",
    "texto": "Cómo proteger una API mediante tokens JWT, autenticación OAuth, cifrado y buenas prácticas de seguridad."
  }'
```

```json
{
  "categoria": "Seguridad",
  "probabilidad": 1.0,
  "informacion_adicional": ["autenticación", "jwt", "api tokens", "buenas prácticas"]
}
```

### Ejemplo 4 — Listar categorías

```bash
curl http://127.0.0.1:8000/categorias
```

```json
{
  "categorias": [
    "Backend", "Bases de Datos", "Ciencia de Datos", "DevOps / Cloud",
    "Frontend", "Mobile", "Programación General", "Seguridad"
  ]
}
```

### Ejemplo 5 — Entrada inválida

```bash
curl -X POST http://127.0.0.1:8000/contenido \
  -H "Content-Type: application/json" \
  -d '{"titulo": "   ", "texto": "algo"}'
```

```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "titulo"],
      "msg": "Value error, El campo no puede contener solo espacios en blanco"
    }
  ]
}
```

> Las respuestas de estos ejemplos son la salida real del modelo `modelo_techmind_v2.joblib`.

---

## Integración con OCI

El proyecto usa **Oracle Cloud Infrastructure** como parte obligatoria de la solución:

| Servicio | Uso |
|---|---|
| **OCI Object Storage** | Almacena el modelo entrenado (`.joblib`) |

El backend **descarga el modelo automáticamente desde OCI** al iniciar, si no lo encuentra localmente:

```
backend/app/ml/loader.py
  └─ si no existe el .joblib local → descarga desde MODELO_URL (OCI) → lo cachea en memoria
```

Esto permite **actualizar el modelo sin reconstruir la imagen** ni volver a desplegar la aplicación: basta con reemplazar el objeto en Object Storage y reiniciar el servicio.

---

## Arquitectura y despliegue

```
   Vercel                    AWS EC2                      OCI
┌───────────┐          ┌──────────────────┐        ┌──────────────┐
│ Frontend  │─────────▶│ Docker + FastAPI │───────▶│   Object     │
│ React/TS  │  HTTPS   │  (puerto 8000)   │ modelo │   Storage    │
└───────────┘          └──────────────────┘        └──────────────┘
```

| Capa | Tecnología |
|---|---|
| **Frontend** | React · TypeScript · Vite · TailwindCSS, desplegado en **Vercel** |
| **Backend** | Python 3.11 · FastAPI · Uvicorn, en un contenedor **Docker sobre AWS EC2** |
| **Modelo** | **OCI Object Storage**, descargado por la API al iniciar |
| **Asistente** | DeepSeek vía SDK de OpenAI, para el endpoint `/chat` |

La aplicación web ofrece cuatro secciones: **Clasificar**, **Biblioteca** (historial con búsqueda y filtro por categoría), **Chat** y **Cuenta** (identificación con Google OAuth). El usuario y su biblioteca se gestionan mediante cookies, sin base de datos relacional en esta entrega.

El paso a paso del despliegue está en [`devops/README.md`](devops/README.md).

---

## Modelo de Machine Learning

| | |
|---|---|
| **Técnica** | TF-IDF + Regresión Logística |
| **Formato** | `Pipeline` de scikit-learn (`tfidf` → `clf`) serializado con `joblib` |
| **Artefacto** | `nlp/models/modelo_techmind_v2.joblib` |
| **Vectorización** | TF-IDF con unigramas y bigramas, 60.000 términos |
| **Ajuste** | `GridSearchCV` con criterio F1 macro |
| **Clases** | 8 categorías |

El artefacto es un **Pipeline completo**: recibe texto crudo y devuelve la predicción, de modo que el preprocesamiento viaja junto al modelo y no puede desincronizarse.

### Resultados

| Métrica | Valor |
|---|---|
| **F1 macro (test)** | 0.7549 |
| **Validación cruzada 5-fold** | 0.7508 ± 0.0019 |
| Accuracy (test) | 0.7530 |
| Línea base (clase más frecuente) | 0.0309 |

Sobre un conjunto de prueba de **7.652 textos** que conserva la distribución real y no se tocó en ningún momento. El F1 por categoría va de **0.63** (Backend) a **0.85** (Mobile).

Se comparó contra un **baseline** y contra **Naive Bayes**, en versión base y ajustada. Se eligió por **F1 macro** —y no por accuracy— para no premiar a un modelo que acierte solo en las categorías grandes. La coincidencia entre el test y la validación cruzada confirma que el resultado es **estable y no producto del azar**.

El entrenamiento usa `class_weight='balanced'` para compensar el desbalance entre categorías: Seguridad tiene 2.792 ejemplos frente a los 5.396 de Frontend.

**Notebooks del proceso:** [`eda/eda_y_limpieza.ipynb`](eda/eda_y_limpieza.ipynb) · [`machine_learning/entrenamiento_modelo.ipynb`](machine_learning/entrenamiento_modelo.ipynb)

### Contenido relacionado y botones de sugerencia

Sobre el mismo vectorizador se construyeron dos funciones más, en [`machine_learning/sugerencias_y_relacionados.ipynb`](machine_learning/sugerencias_y_relacionados.ipynb):

| Artefacto | Qué hace |
|---|---|
| `nlp/models/matriz_historica.pkl` | Los 38.257 documentos del corpus vectorizados. Dado un texto, devuelve los que hablan de lo mismo por similitud del coseno |
| `nlp/models/sugerencias_botones.json` | 15 términos técnicos para los botones de la pantalla principal |

No se almacena la matriz completa de similitudes: con 38.257 documentos serían más de mil cuatrocientos millones de valores, casi todos cercanos a cero. Se guardan los vectores y se compara contra ellos únicamente el texto de la consulta.

Los términos de los botones salen de medir la **distintividad** de cada uno —cuánto pesa dentro de su categoría comparado con su peso en el corpus entero—, con un tope de dos por categoría. Por frecuencia no serviría: los primeros puestos se los llevan `the`, `to` y `and`.

Un vecino recomendado cae en la misma categoría que la consulta entre el **31 %** y el **61 %** de las veces según la categoría, contra el 12,5 % que daría recomendar al azar.

---

## Dataset

Corpus técnico propio, construido por el equipo a partir de fuentes públicas.

| | |
|---|---|
| **Registros** | 38.276 |
| **Categorías** | 8, razonablemente balanceadas |
| **Duplicados** | 0 |
| **Archivo** | `dataset/processed/techmind_dataset_v2.csv` |
| **Documentación** | [`dataset/processed/README.md`](dataset/processed/README.md) |

**Composición por fuente**

| Fuente | Registros | % |
|---|--:|--:|
| StackOverflow | 25.574 | 66,8 % |
| Medium | 11.140 | 29,1 % |
| freeCodeCamp (ES) | 659 | 1,7 % |
| Wikipedia (ES) | 379 | 1,0 % |
| Corpus propio ES (PDF/OCR) | 524 | 1,4 % |

**Columnas:** `titulo`, `texto`, `categoria`, `palabras_clave`, `fuente`, `idioma`

> **Nota sobre el corpus:** predomina el contenido en inglés (95,9 %). La clasificación se apoya en el vocabulario técnico, común a ambos idiomas (`docker`, `python`, `api`, `jwt`), por lo que el modelo responde correctamente también en español. El corpus en español se incorporó específicamente para reforzar ese caso.

---

## Estructura del repositorio

```
G9-LATAM-Team-46/
├── backend/                  # API REST (FastAPI)
│   ├── app/
│   │   ├── main.py           # Punto de entrada, routers y CORS
│   │   ├── core/             # Configuración y dependencias
│   │   ├── routers/          # /contenido · /categorias · /biblioteca · /chat · /modelo · /health
│   │   ├── schemas/          # Contratos de entrada y salida (Pydantic)
│   │   ├── services/         # Clasificación, biblioteca y chat
│   │   └── ml/               # Carga del modelo y preprocesamiento
│   ├── tests/
│   ├── dockerfile
│   └── requirements.txt
├── dataset/                  # Corpus y su documentación
├── eda/                      # Exploración, limpieza y preparación
├── machine_learning/         # Notebooks de entrenamiento y de sugerencias
├── nlp/                      # Módulo NLP, artefactos entrenados y pruebas
│   ├── models/               # modelo · matriz histórica · sugerencias
│   ├── src/                  # clasificador · recomendador · limpieza
│   ├── tests/
│   └── README_BACKEND.md     # Lo que queda del lado de la API
├── frontend/                 # Interfaz web
├── devops/                   # Guía de despliegue en AWS
└── docs/                     # Documentación del equipo
```

---

## Dependencias y versiones

**Backend** (`backend/requirements.txt`)

| Paquete | Versión |
|---|---|
| fastapi | 0.139.2 |
| uvicorn | 0.51.0 |
| pydantic | 2.13.4 |
| scikit-learn | 1.4.1.post1 |
| numpy | 1.26.4 |
| scipy | 1.17.1 |
| joblib | 1.5.3 |
| requests | 2.32.4 |
| openai | 2.53.0 |

> **Importante:** la versión de `scikit-learn` debe coincidir con la usada al entrenar el modelo. Cargar el `.joblib` con otra versión puede generar advertencias o resultados inconsistentes.

Cada módulo tiene además su propio `requirements.txt`: `nlp/`, `machine_learning/` y `dataset/requirements-eda.txt`.

---

## Pruebas

```bash
# Backend
cd backend && pytest

# Módulo NLP
cd nlp && pytest
```

| Ubicación | Cubre |
|---|---|
| `backend/tests/` | Endpoint `/contenido`, validaciones y respuestas |
| `nlp/tests/` | Clasificador, limpieza de texto, extracción de palabras clave, repositorio del modelo y esquemas, tokenización — **72 pruebas** |

---

## Equipo

**Equipo 46 — G9 LATAM · Hackathon ONE (Alura Latam + Oracle)**

- **David Fletes Esparza** — Cloud Infrastructure & Frontend Engineer
- **Sebastián Lugo** — Backend Lead
- **Daniel Soto** — NLP Engineer
- **Edmer Rubio** — Machine Learning Engineer
- **Edson Alberto Herrera Cervantes** — Data Science
- **Willman Alca Alfaro** — Data Science
- **Lucio Fernandez Chavez** — Data Science Project Lead
  

La convención de ramas está documentada en [`docs/GUIA_RAMAS.md`](docs/GUIA_RAMAS.md).
