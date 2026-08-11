# TechMind AI — Backend

API REST del proyecto TechMind AI (Hackathon ONE G9). Clasifica contenido técnico y devuelve categoría, probabilidad y palabras clave relevantes. Incluye además un endpoint conversacional que usa DeepSeek para explicar el contenido en lenguaje natural, anclado siempre al resultado del modelo propio.

## Instalación y ejecución local

```bash
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
# (pedir credenciales de MySQL y la API key de DeepSeek al equipo si hace falta)

# 6. Levantar el servidor
uvicorn app.main:app --reload
```

Documentación interactiva (Swagger): `http://127.0.0.1:8000/docs`

## Estructura del proyecto

```
backend/
├── app/
│   ├── main.py                  # Punto de entrada, junta routers, configura CORS
│   ├── core/
│   │   ├── config.py            # Configuración general (pydantic-settings)
│   │   └── database.py          # Conexión a MySQL (SQLAlchemy + PyMySQL), opcional
│   ├── routers/
│   │   ├── health.py            # GET /health
│   │   ├── categorias.py        # GET /categorias
│   │   ├── contenido.py         # POST /contenido
│   │   └── chat.py              # POST /chat
│   ├── schemas/
│   │   ├── contenido.py         # Contratos de entrada/salida de /contenido (Pydantic)
│   │   └── chat.py              # Contratos de entrada/salida de /chat (Pydantic)
│   ├── services/
│   │   ├── clasificador.py      # Lógica de clasificación con modelo real
│   │   └── chat.py              # Cliente DeepSeek, armado de prompt y respuesta
│   └── ml/
│       ├── loader.py            # Carga del modelo (.joblib), descarga automática desde OCI si falta local
│       └── preprocesamiento.py  # Función limpiar(), igual a la del notebook de entrenamiento
├── tests/
├── requirements.txt
├── .env.example
└── .gitignore
```

## Endpoints

### `GET /health`
Verifica que el servidor está corriendo.

**Respuesta:**
```json
{ "status": "ok" }
```

### `GET /categorias`
Devuelve las categorías reales que el modelo aprendió (lee `modelo.classes_` en vivo, no hardcodeado).

**Respuesta:**
```json
{
  "categorias": ["Backend", "Bases de Datos", "Ciencia de Datos", "DevOps/Cloud", "Frontend", "Mobile", "Programación General", "Seguridad"]
}
```

### `POST /contenido`
Clasifica un contenido técnico usando el modelo real (TF-IDF + Regresión Logística, entrenado sobre dataset bilingüe de ~38k filas, accuracy ~77.9%).

**Entrada:**
```json
{
  "titulo": "Introducción a FastAPI",
  "texto": "En este contenido se presentan los conceptos básicos para crear APIs REST con Python."
}
```

**Respuesta (200):**
```json
{
  "categoria": "Backend",
  "probabilidad": 0.91,
  "informacion_adicional": ["python", "fastapi", "api", "rest"]
}
```

**Validaciones:**
- `titulo` y `texto` son obligatorios, no pueden estar vacíos ni contener solo espacios en blanco (`422 Unprocessable Entity`).
- Si el modelo no está disponible, responde `503 Service Unavailable`.

### `POST /chat`
Endpoint conversacional, autosuficiente: corre su propia clasificación interna (misma lógica que `/contenido`), arma contexto con la categoría/probabilidad/palabras clave, y se lo pasa a DeepSeek para generar una explicación en lenguaje natural. No requiere haber llamado antes a `/contenido`.

Soporta seguimiento de conversación mediante el campo `historial` (opcional). El frontend es responsable de guardar y reenviar el historial en cada mensaje — el backend no persiste ninguna conversación.

**Entrada (primer mensaje, sin historial):**
```json
{
  "texto": "¿qué es Docker?"
}
```

**Entrada (mensaje de seguimiento, con historial):**
```json
{
  "texto": "y cuál es la diferencia con una máquina virtual",
  "historial": [
    { "rol": "user", "contenido": "¿qué es Docker?" },
    { "rol": "assistant", "contenido": "Docker es una plataforma que permite..." }
  ]
}
```

**Respuesta (200):**
```json
{
  "respuesta": "Una máquina virtual simula un sistema operativo completo, mientras que Docker..."
}
```

**Manejo de errores:** si DeepSeek falla (key inválida, timeout, servicio caído), el endpoint nunca devuelve `500` — responde `200` con un mensaje genérico en `respuesta`, para no romper la experiencia del usuario. El resto de la API no se ve afectado por fallos de DeepSeek.

## CORS

Configurado para aceptar los puertos comunes de desarrollo de React:
- `http://localhost:3000` (Create React App)
- `http://localhost:5173` (Vite)

## Variables de entorno necesarias (`.env`)

```
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
DB_NAME=techmind
MODELO_URL=
DEEPSEEK_API_KEY=
```

Ver `.env.example` para la plantilla sin valores reales.

**Nota:** `DB_PASSWORD` es opcional — la API arranca sin ella (la base de datos todavía no se usa en ningún endpoint activo, solo está preparada para el futuro login). `DEEPSEEK_API_KEY` también es opcional a nivel de arranque; sin ella, `/chat` responde igual pero con el mensaje genérico de fallback en vez de una respuesta real de DeepSeek.

## Notas importantes

- El modelo (`.joblib`, ~71 MB) **no está en el repo** — está en `.gitignore` por peso. Se descarga automáticamente desde OCI Object Storage al arrancar la app (`MODELO_URL` en `.env`), con caché en memoria para no repetir la descarga.
- La versión de `scikit-learn` está fijada en `requirements.txt` (`==1.4.1.post1`) porque el modelo se entrenó con esa versión exacta — no actualizar sin coordinar con Ciencia de Datos.
- La base de datos (MySQL) todavía no es consumida por ningún endpoint activo — está preparada para el futuro login (`usuarios`, `refresh_tokens`), no bloqueante para esta entrega.

## Estrategia de ramas

Modelo centralizado: cada área trabaja en su propia rama `feat/<área>` (ej. `feat/backend`, `feat/eda`) directo sobre el repositorio oficial. Ningún cambio se sube a `main` sin PR revisado.

## Pendiente

- `GET /modelo/info`, `POST /contenido/lote`
- Login/JWT (`/registro`, `/login`, `/logout`) — diseño cerrado (Bearer token, bcrypt, revocación en `refresh_tokens`), no bloqueante para esta entrega