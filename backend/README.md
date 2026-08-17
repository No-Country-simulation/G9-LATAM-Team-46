# TechMind AI — Backend (API REST)

API REST desarrollada con **FastAPI** que clasifica contenido técnico usando un modelo de Machine Learning (TF-IDF + Regresión Logística), con capa conversacional sobre DeepSeek y una Biblioteca personal en memoria identificada por cookie. Integrada con Oracle Cloud Infrastructure (OCI Object Storage) para el almacenamiento del modelo entrenado.

**Hackathon ONE — Alura Latam + Oracle · Equipo 46 (G9 LATAM) · Backend Lead: Sebastián Lugo**

Rama activa: `feat/backend`.

---

## Índice

- [Arquitectura](#arquitectura)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Instalación y ejecución](#instalación-y-ejecución)
- [Variables de entorno](#variables-de-entorno)
- [Endpoints](#endpoints)
- [Modelo de Machine Learning](#modelo-de-machine-learning)
- [Biblioteca personal (identidad por cookie)](#biblioteca-personal-identidad-por-cookie)
- [Autenticación (JWT) — inactiva, preparada para v2](#autenticación-jwt--inactiva-preparada-para-v2)
- [CORS](#cors)
- [Docker](#docker)
- [Pruebas](#pruebas)
- [Dependencias y versiones](#dependencias-y-versiones)
- [Estado y pendientes conocidos](#estado-y-pendientes-conocidos)

---

## Arquitectura

Arquitectura por capas, sin base de datos relacional activa en el flujo principal:

```
Request → routers/ → schemas/ (validación Pydantic) → services/ → ml/ (modelo cacheado en memoria)
```

- **`routers/`** — define los endpoints HTTP, delega toda la lógica a `services/`.
- **`schemas/`** — contratos de entrada/salida con Pydantic. No se mezclan con los modelos de base de datos.
- **`services/`** — lógica de negocio: clasificación, chat, Biblioteca.
- **`ml/`** — carga del modelo `.joblib` (patrón singleton en memoria) y preprocesamiento de texto.
- **`core/`** — configuración (`Settings` vía `pydantic-settings`), conexión a base de datos (SQLAlchemy, no usada en el flujo activo hoy), y la dependencia de identidad por cookie.
- **`models/`** — modelos SQLAlchemy. Existe `Usuario`, pero está completamente inactivo (ver sección de autenticación).

El modelo de ML se carga **una sola vez** al arrancar el proceso (`@app.on_event("startup")`) y se mantiene cacheado en memoria durante toda la vida del servidor — no se recarga en cada petición.

---

## Estructura del proyecto

```
backend/
├── app/
│   ├── main.py                  # Punto de entrada, CORS, routers, startup, exception handler
│   ├── core/
│   │   ├── config.py            # Settings (pydantic-settings), lee backend/.env
│   │   ├── database.py          # SQLAlchemy engine + Base (no usado en el flujo activo)
│   │   ├── dependencias.py      # obtener_usuario_actual() — identidad por cookie
│   │   └── seguridad.py         # hashing/JWT — construido, inactivo (v2)
│   ├── models/
│   │   └── usuario.py           # Modelo SQLAlchemy Usuario — inactivo (v2)
│   ├── ml/
│   │   ├── loader.py            # cargar_modelo(), descarga desde OCI si no está local
│   │   ├── preprocesamiento.py  # limpiar() — replica exacta del preprocesamiento de entrenamiento
│   │   └── modelo_techmind_v2.joblib  # NO versionado (.gitignore)
│   ├── routers/
│   │   ├── health.py            # GET /health
│   │   ├── contenido.py         # POST /contenido
│   │   ├── categorias.py        # GET /categorias
│   │   ├── chat.py              # POST /chat
│   │   ├── modelo.py            # GET /modelo/info
│   │   └── biblioteca.py        # POST /biblioteca, GET /biblioteca
│   ├── schemas/
│   │   ├── contenido.py         # ContenidoEntrada, ContenidoSalida
│   │   ├── categorias.py        # CategoriasSalida
│   │   ├── modelo.py            # ModeloInfo
│   │   ├── biblioteca.py        # BibliotecaEntrada, BibliotecaResultado
│   │   └── auth.py              # UsuarioRegistro, UsuarioLogin, Token — inactivo (v2)
│   └── services/
│       ├── clasificador.py      # clasificar_contenido() — lógica central de predicción
│       ├── biblioteca.py        # Almacenamiento en memoria (dict), guardar/obtener
│       └── chat.py              # Capa conversacional sobre DeepSeek
├── tests/
│   ├── test_contenido.py        # pytest, valida contrato de /contenido
│   └── prueba_manual_clasificacion.py  # script manual ES/EN, 16 casos
├── dockerfile
├── .dockerignore
├── .gitignore
├── .env.example
└── requirements.txt
```

---

## Instalación y ejecución

### Requisitos

- Python 3.11+
- `pip`, `venv`

### Pasos

```bash
git clone https://github.com/No-Country-simulation/G9-LATAM-Team-46.git
cd G9-LATAM-Team-46/backend

python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS / Linux

pip install -r requirements.txt

copy .env.example .env         # Windows
cp .env.example .env           # macOS / Linux
```

### Levantar el servidor

```bash
uvicorn app.main:app --reload
```

- API: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`

> **Importante — activar el entorno virtual en cada sesión.** Si una terminal muestra errores de `ModuleNotFoundError` para paquetes que sí están en `requirements.txt` (típicamente `sqlalchemy`), es señal de que el `venv` no está activo en esa terminal puntual. El prompt debería mostrar el prefijo `(venv)` antes de ejecutar cualquier comando de Python.

---

## Variables de entorno

Definidas en `app/core/config.py` (clase `Settings`, vía `pydantic-settings`), leídas desde `backend/.env`.

| Variable | Obligatoria | Descripción |
|---|---|---|
| `MODELO_URL` | Solo si el modelo no está local | URL del `.joblib` en OCI Object Storage. El backend lo descarga automáticamente si no lo encuentra en `app/ml/` |
| `DEEPSEEK_API_KEY` | Solo para `/chat` | Clave del LLM conversacional |
| `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME` | No | Conexión MySQL. La API arranca sin ellas (`db_password: str \| None = None`) |
| `JWT_SECRET_KEY` | No | Clave para firmar JWT. **Opcional a propósito** (`str \| None = None`) — el login está inactivo, así que su ausencia no bloquea el arranque del servidor |

`.env` nunca se versiona (`.gitignore`). El equipo mantiene `.env.example` como referencia de qué variables existen, sin valores reales.

---

## Endpoints

| Método | Ruta | Descripción | Auth |
|---|---|---|---|
| `GET` | `/health` | Estado del servicio | No |
| `POST` | `/contenido` | Clasifica un contenido técnico (endpoint principal) | No |
| `GET` | `/categorias` | Lista las categorías que reconoce el modelo | No |
| `POST` | `/chat` | Capa conversacional sobre el mismo motor de clasificación (DeepSeek) | No |
| `GET` | `/modelo/info` | Diagnóstico: algoritmo, categorías, fecha de modificación del `.joblib` activo | No |
| `POST` | `/biblioteca` | Clasifica y guarda una entrada en la Biblioteca del usuario (cookie) | Cookie |
| `GET` | `/biblioteca` | Devuelve el historial guardado para el usuario de la cookie | Cookie |

### `POST /contenido`

**Entrada** (`ContenidoEntrada`)

| Campo | Tipo | Validación |
|---|---|---|
| `titulo` | `str` | `min_length=1`, rechaza strings solo con espacios (`field_validator`) |
| `texto` | `str` | `min_length=1`, rechaza strings solo con espacios (`field_validator`) |

**Salida** (`ContenidoSalida`)

| Campo | Tipo | Descripción |
|---|---|---|
| `categoria` | `str` | Una de las 8 categorías del modelo |
| `probabilidad` | `float` | Confianza de la predicción, redondeada a 2 decimales |
| `informacion_adicional` | `list[str]` | Top-4 palabras clave por peso TF-IDF |

**Errores**

| Código | Causa |
|---|---|
| `422` | Validación fallida (campo vacío o solo espacios) |
| `503` | Modelo no disponible (`clasificar_contenido` verifica `modelo is None`) |
| `500` | Error interno no controlado (capturado por el exception handler global) |

### `POST /biblioteca` y `GET /biblioteca`

Ver sección [Biblioteca personal](#biblioteca-personal-identidad-por-cookie) para el detalle completo de diseño.

**`POST /biblioteca`** — entrada `BibliotecaEntrada` (`titulo`, `texto`), reutiliza `clasificar_contenido()` internamente, guarda y devuelve `BibliotecaResultado` (incluye `categoria`, `probabilidad`, `palabras_clave`, `fecha_creacion`).

**`GET /biblioteca`** — sin body, devuelve `list[BibliotecaResultado]` para el `usuario_id` resuelto desde la cookie.

### `GET /modelo/info`

Devuelve `ModeloInfo`: `algoritmo` (string fijo, descriptivo), `cantidad_categorias`, `categorias` (lista), `fecha_modificacion` (de `RUTA_MODELO.stat().st_mtime`). Reutiliza el mismo caché de `cargar_modelo()` que usa `/contenido` — no dispara una carga adicional del modelo.

Coexiste con `GET /categorias` sin ser estrictamente redundante: `/categorias` da la lista simple para consumo del frontend; `/modelo/info` es diagnóstico técnico del ambiente (qué modelo/versión está corriendo).

---

## Modelo de Machine Learning

| | |
|---|---|
| Técnica | TF-IDF + Regresión Logística |
| Formato | `Pipeline` de scikit-learn, serializado con `joblib` |
| Archivo activo | `app/ml/modelo_techmind_v2.joblib` (no versionado) |
| Categorías | 8 (Backend, Bases de Datos, Ciencia de Datos, DevOps/Cloud, Frontend, Mobile, Programación General, Seguridad) |
| Accuracy | ~78% |
| Idioma | Bilingüe (español/inglés) |

**Carga del modelo** (`app/ml/loader.py`):
- `cargar_modelo()` cachea el modelo en la variable global `_modelo`. Si ya está cargado, devuelve el caché sin tocar disco.
- Si el `.joblib` no existe localmente, intenta descargarlo desde `MODELO_URL` (OCI Object Storage) antes de cargarlo.
- Si la descarga falla o `MODELO_URL` no está configurada, devuelve `None` — los endpoints que dependen del modelo responden `503`, no crashean el proceso.

**Preprocesamiento** (`app/ml/preprocesamiento.py`, función `limpiar()`):
El pipeline serializado (`.joblib`) **no incluye** el paso de limpieza de texto usado en entrenamiento — se reimplementa por separado, replicando exactamente la lógica del notebook de entrenamiento. Un desajuste aquí no genera error, pero degrada silenciosamente la calidad de las predicciones.

**Predicción** (`app/services/clasificador.py`, función `clasificar_contenido()`):
1. Concatena `titulo + " " + texto`, aplica `limpiar()`.
2. `modelo.predict_proba()` sobre el texto limpio, toma la categoría de mayor probabilidad (`argmax`).
3. Extrae las top-4 palabras clave accediendo directamente al paso `tfidf` del pipeline (`modelo.named_steps["tfidf"]`), ordenando por peso descendente.

> **Nota de versionado crítica:** la versión de `scikit-learn` en `requirements.txt` debe coincidir con la usada para entrenar el `.joblib`. Un desajuste de versión no siempre lanza error explícito — puede generar `InconsistentVersionWarning` o alterar resultados de forma silenciosa.

> **Independencia de `nlp/`:** el backend usa exclusivamente su copia local del modelo y su propia lógica de carga/preprocesamiento. No depende de `nlp/src/inference.py` (`procesar_contenido()`/`precargar_modelo()`), que existe en el repo como entregable del equipo de NLP pero aún no fue integrado — la migración queda pendiente de confirmación de versión final del modelo.

---

## Biblioteca personal (identidad por cookie)

**Sin base de datos.** Diseño elegido explícitamente para evitar dependencia de MySQL o coordinación de infraestructura en esta entrega — completamente reiniciable, sin persistencia en disco.

### Identidad — `app/core/dependencias.py`

```python
def obtener_usuario_actual(request: Request, response: Response) -> str:
```

Dependencia de FastAPI (`Depends(obtener_usuario_actual)`). Si la petición no trae cookie `usuario_id`, genera un `uuid.uuid4()` nuevo y lo setea en la respuesta. Si ya la trae, la reutiliza.

Configuración de la cookie:

```python
httponly=True
samesite="none"
secure=True
max_age=60 * 60 * 24 * 365  # 1 año
```

`samesite="none"` + `secure=True` es obligatorio porque frontend (Vercel) y backend (AWS) están en dominios distintos — toda comunicación es cross-site, y `"lax"` bloquearía la cookie en peticiones `fetch`/`POST`. Requiere HTTPS estable en ambos extremos.

### Almacenamiento — `app/services/biblioteca.py`

```python
biblioteca_en_memoria: dict[str, list[dict]] = {}
```

Diccionario en memoria del proceso. Clave: `usuario_id` (de la cookie). Valor: lista de entradas de esa persona.

- `guardar_en_biblioteca()` usa `.append()` — nunca sobreescribe entradas previas.
- `obtener_biblioteca()` usa `.get(usuario_id, [])` — lista vacía si el usuario nunca guardó nada, evita error 500 para usuarios nuevos.

Se guarda el **texto como string**, nunca un archivo como objeto — si en el futuro se acepta subir `.txt`, se lee el contenido y se descarta el archivo, evitando la necesidad de un servicio de almacenamiento adicional.

**Limitación conocida y aceptada:** todo el contenido se pierde si el proceso del backend se reinicia (mismo comportamiento que el caché del modelo ML en `loader.py`). No se pierde con un refresh de página — la cookie persiste en el navegador independientemente del ciclo de vida del backend.

### Reutilización del clasificador

`POST /biblioteca` no duplica lógica de predicción — instancia un `ContenidoEntrada` con los mismos datos y llama a `clasificar_contenido()`, la misma función que usa `POST /contenido`.

---

## Autenticación (JWT) — inactiva, preparada para v2

El equipo decidió posponer el login completo a una versión futura por el peso que agregaba al despliegue en esta etapa. El código existe, está comiteado, pero **no se ejecuta en ningún punto del flujo actual**.

**Piezas construidas:**
- `app/models/usuario.py` — modelo SQLAlchemy `Usuario`, coincide con la tabla real en MySQL (`id`, `email` único, `password_hash` nulable, `proveedor`, `proveedor_id`, `fecha_creacion`).
- `app/schemas/auth.py` — `UsuarioRegistro`, `UsuarioRespuesta`, `UsuarioLogin`, `Token`.
- `app/core/seguridad.py` — `hashear_password()`/`verificar_password()` (passlib + bcrypt), `crear_token()` (JWT vía `python-jose`, `HS256`).

**Verificación de inactividad (3 puntos):**
1. `main.py` no importa ningún router de auth, ni `seguridad.py`, ni `schemas/auth.py`.
2. `requirements.txt` no incluye `passlib`, `python-jose` ni `email-validator` — coherente con que nada los requiere en runtime.
3. No existe `app/models/__init__.py` — no hay importación automática que enganche `usuario.py` con el resto de la app.

`jwt_secret_key` en `Settings` es `str | None = None` a propósito: sin este default, el proceso fallaría al arrancar en cualquier entorno sin esa variable configurada, aunque el login no se use.

Cuando se active login en v2, el identificador de cookie de Biblioteca se reemplaza por el `id` real del usuario autenticado — el resto del diseño (estructura de almacenamiento, endpoints) no requiere rediseño.

---

## CORS

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_origin_regex=r"https://techmind-frontend.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

`allow_origin_regex` acepta tanto la URL de producción (`techmind-frontend.vercel.app`) como cualquier URL de preview que Vercel genere para ramas/builds de prueba (sufijos random del tipo `techmind-frontend-git-x.vercel.app`). `allow_credentials=True` es necesario para que las cookies de Biblioteca (y JWT, cuando se active) viajen correctamente en peticiones cross-origin.

---

## Docker

- `dockerfile` y `.dockerignore` en `backend/`.
- `.dockerignore` excluye lo que no debe copiarse a la imagen (`.env`, `.git`, `__pycache__`, `venv/`).
- El modelo (`.joblib`) no se versiona ni se copia en build time — se descarga desde OCI Object Storage al arrancar el contenedor, vía `MODELO_URL`.

```bash
docker build -t techmind-backend .
docker run -p 8000:8000 --env-file .env techmind-backend
```

---

## Pruebas

```bash
cd backend
pytest
```

| Archivo | Cubre |
|---|---|
| `tests/test_contenido.py` | Contrato de `/contenido` — estructura de respuesta, no valores fijos (el modelo responde con datos reales) |
| `tests/prueba_manual_clasificacion.py` | Script manual, 16 casos (8 categorías × ES/EN), resultados en CSV. 16/16 aciertos en la última corrida documentada |

---

## Dependencias y versiones

| Paquete | Versión |
|---|---|
| fastapi | 0.139.2 |
| uvicorn | 0.51.0 |
| pydantic | 2.13.4 |
| pydantic-settings | 2.15.0 |
| scikit-learn | 1.4.1.post1 |
| numpy | 1.26.4 |
| scipy | 1.17.1 |
| joblib | 1.5.3 |
| SQLAlchemy | 2.0.51 |
| PyMySQL | 1.2.0 |
| requests | 2.32.4 |
| python-dotenv | 1.2.2 |
| openai | 2.53.0 |

> La versión de `scikit-learn` debe coincidir con la usada para entrenar el modelo activo. Ver nota en la sección de Machine Learning.

---

## Estado y pendientes conocidos

- **Migración a `nlp/src/inference.py`** (`procesar_contenido()`/`precargar_modelo()`) — pendiente, condicionada a confirmación de versión final del modelo por el equipo de NLP. El backend hoy usa su copia local propia, ya probada.
- **`POST /contenido/lote`** — no implementado. Mismo patrón que `/contenido`, aceptando una lista de entradas.
- **HTTPS estable del backend en producción (AWS)** — necesario para que `samesite="none"` en la cookie de Biblioteca funcione fuera de local. Pendiente de confirmación con el equipo de despliegue.
- **Login v2** — diseño cerrado, código construido e inactivo. Implementación (conectar routers, activar dependencias) no iniciada.