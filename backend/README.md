# TechMind AI — Backend

API REST del proyecto TechMind AI (Hackathon ONE G9). Clasifica contenido técnico y devuelve categoría, probabilidad y palabras clave relevantes.

## Instalación y ejecución local

\`\`\`bash
# 1. Entrar a la carpeta del backend
cd backend

# 2. Crear el entorno virtual (una sola vez)
python -m venv venv

# 3. Activar el entorno virtual
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Configurar variables de entorno
# Copiar .env.example a .env y completar con los valores reales
# (pedir credenciales de MySQL al equipo)

# 6. Levantar el servidor
uvicorn app.main:app --reload
\`\`\`

Documentación interactiva (Swagger): `http://127.0.0.1:8000/docs`

## Estructura del proyecto

\`\`\`
backend/
├── app/
│   ├── main.py                  # Punto de entrada, junta routers, configura CORS
│   ├── core/
│   │   ├── config.py            # Configuración general
│   │   └── database.py          # Conexión a MySQL (SQLAlchemy + PyMySQL)
│   ├── routers/
│   │   ├── health.py            # GET /health
│   │   ├── categorias.py        # GET /categorias
│   │   └── contenido.py         # POST /contenido
│   ├── schemas/
│   │   └── contenido.py         # Contratos de entrada/salida (Pydantic)
│   ├── services/
│   │   └── clasificador.py      # Lógica de clasificación con modelo real
│   └── ml/
│       ├── loader.py            # Carga real del modelo (.joblib) vía joblib.load()
│       └── preprocesamiento.py  # Función limpiar(), igual a la del notebook de entrenamiento
├── tests/
├── requirements.txt
└── .gitignore
\`\`\`

## Endpoints

### `GET /health`
Verifica que el servidor está corriendo.

**Respuesta:**
\`\`\`json
{ "status": "ok" }
\`\`\`

### `GET /categorias`
Devuelve las categorías reales que el modelo aprendió (lee `modelo.classes_` en vivo, no hardcodeado).

**Respuesta:**
\`\`\`json
{
  "categorias": ["Backend", "Bases de Datos", "Ciencia de Datos", "DevOps/Cloud", "Frontend", "Mobile", "Programación General", "Seguridad"]
}
\`\`\`

### `POST /contenido`
Clasifica un contenido técnico usando el modelo real (TF-IDF + Regresión Logística, entrenado sobre dataset bilingüe de ~38k filas, accuracy ~77.9%).

**Entrada:**
\`\`\`json
{
  "titulo": "Introducción a FastAPI",
  "texto": "En este contenido se presentan los conceptos básicos para crear APIs REST con Python."
}
\`\`\`

**Respuesta (200):**
\`\`\`json
{
  "categoria": "Backend",
  "probabilidad": 0.91,
  "informacion_adicional": ["python", "fastapi", "api", "rest"]
}
\`\`\`

**Validaciones:**
- `titulo` y `texto` son obligatorios, no pueden estar vacíos ni contener solo espacios en blanco (`422 Unprocessable Entity`).
- Si el modelo no está disponible, responde `503 Service Unavailable`.

## CORS

Configurado para aceptar los puertos comunes de desarrollo de React:
- `http://localhost:3000` (Create React App)
- `http://localhost:5173` (Vite)

## Variables de entorno necesarias (`.env`)

\`\`\`
DB_USER=...
DB_PASSWORD=...
DB_HOST=...
DB_NAME=...
\`\`\`

Ver `.env.example` para la plantilla sin valores reales.

## Notas importantes

- El modelo (`.joblib`, ~71 MB) **no está en el repo** — está en `.gitignore` por peso. Plan: alojarlo en OCI Object Storage, la API lo descarga al arrancar (en desarrollo).
- La versión de `scikit-learn` está fijada en `requirements.txt` (`==1.4.1.post1`) porque el modelo se entrenó con esa versión exacta — no actualizar sin coordinar con Ciencia de Datos.

## Estrategia de ramas

Modelo centralizado: cada área trabaja en su propia rama `feat/<área>` (ej. `feat/backend`, `feat/nlp`) directo sobre el repositorio oficial. Ningún cambio se sube a `main` sin PR revisado. Ramas se autoborran del remoto al mergear.

## Pendiente

- `GET /modelo/info`, `POST /contenido/lote`
- Login/JWT (`/registro`, `/login`, `/logout`) — diseño cerrado (Bearer token, bcrypt, revocación en `refresh_tokens`), no bloqueante para esta entrega