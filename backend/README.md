# TechMind AI — Backend

API REST del proyecto TechMind AI (Hackathon ONE G9). Clasifica contenido técnico y devuelve categoría, probabilidad y palabras clave relevantes.

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

# 5. Levantar el servidor
uvicorn app.main:app --reload
```

Documentación interactiva (Swagger): `http://127.0.0.1:8000/docs`

## Estructura del proyecto

```
backend/
├── app/
│   ├── main.py              # Punto de entrada, junta todos los routers
│   ├── core/
│   │   └── config.py        # Configuración general de la app
│   ├── routers/
│   │   ├── health.py        # GET /health
│   │   └── contenido.py     # POST /contenido
│   ├── schemas/
│   │   └── contenido.py     # Contratos de entrada/salida (Pydantic)
│   ├── services/
│   │   └── clasificador.py  # Lógica de negocio
│   └── ml/
│       └── loader.py        # Punto donde se carga el modelo (.joblib)
├── tests/
├── requirements.txt
└── .gitignore
```

### Por qué está dividido así

Cada carpeta tiene una única responsabilidad, así que cuando algo cambia, se sabe exactamente dónde tocar:

- **`routers/`** — recibe la petición HTTP y delega. No contiene lógica de negocio.
- **`schemas/`** — el contrato de datos. Si algo no calza con el schema, ni siquiera llega al código.
- **`services/`** — la lógica real (qué hacer con el contenido). Es lo que cambia cuando llegue el modelo real.
- **`ml/`** — el punto exacto donde se "enchufa" el modelo entrenado por el equipo de Ciencia de Datos.

## Conceptos clave (para repaso)

| Concepto | Qué es | Dónde se usa |
|---|---|---|
| `venv` | Entorno aislado de dependencias, propio de cada proyecto | Toda la instalación local |
| Paquete (`__init__.py`) | Le dice a Python que una carpeta es importable como módulo | `routers/`, `schemas/`, `services/`, `ml/` |
| Decorador (`@algo`) | Envuelve una función y le agrega comportamiento | `@router.post("/contenido")` |
| Type hints (`: str`, `-> dict`) | Anotaciones de tipo que FastAPI usa para validar y documentar | Todas las funciones y schemas |
| Pydantic (`BaseModel`) | Convierte atributos con tipo en reglas de validación automática | `schemas/contenido.py` |
| `HTTPException` | Errores HTTP controlados y explícitos, en vez de errores crudos de Python | `services/clasificador.py` |
| `field_validator` | Validación personalizada sobre un campo específico | Validador de espacios en blanco en `titulo`/`texto` |
| `exception_handler` | Captura global de errores no previstos | `main.py` |

## Endpoints

### `GET /health`
Verifica que el servidor está corriendo.

**Respuesta:**
```json
{ "status": "ok" }
```

### `POST /contenido`
Clasifica un contenido técnico (actualmente con lógica mock, pendiente integración del modelo real de Persona 5).

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
  "probabilidad": 0.87,
  "informacion_adicional": ["Python", "FastAPI", "API REST"]
}
```

**Validaciones:**
- `titulo` y `texto` son obligatorios y no pueden estar vacíos ni contener solo espacios en blanco (`422 Unprocessable Entity`).
- Si el modelo de clasificación no está disponible, responde `503 Service Unavailable`.

## Estrategia de ramas

Modelo centralizado: cada área del proyecto trabaja en su propia rama `feature/<área>-<tarea>` (ej. `feature/backend-setup`, `feature/dataset-limpieza`) directo sobre el repositorio oficial. Ningún cambio se sube a `main` sin pasar por Pull Request revisado.

## Pendiente de integración

Cuando Persona 5 entregue el modelo serializado (`.joblib`) y el pipeline de NLP:
1. Reemplazar el contenido de `app/ml/loader.py` (`cargar_modelo()`) por la carga real con `joblib.load(...)`.
2. Reemplazar la lógica mock en `app/services/clasificador.py` por la llamada real al modelo.
3. No debería ser necesario tocar `routers/` ni `schemas/` — ese es justamente el punto de tener la lógica separada por capas.
