# Qué tiene que hacer el backend con esta rama

Rama `new-model`. Trae el modelo reentrenado, dos artefactos nuevos y el
módulo NLP actualizado. Este documento es la lista de lo que hay que tocar
del lado de la API, en orden de importancia.

Todo lo que se afirma acá está medido; los comandos para reproducirlo están
al final.

---

## Lo que llega

| Archivo | Qué es |
|---|---|
| `nlp/models/modelo_techmind_v2.joblib` | **Reemplaza** al anterior. Mismo nombre, modelo distinto |
| `nlp/models/matriz_historica.pkl` | Nuevo. 38.257 documentos vectorizados, para contenido relacionado |
| `nlp/models/sugerencias_botones.json` | Nuevo. 15 términos para los botones de la pantalla principal |
| `nlp/models/diccionario_categorias.json` | Nuevo. Las 8 categorías con sus términos característicos |
| `nlp/src/recommender.py` | Nuevo. El módulo que consulta la matriz |
| `nlp/src/` (resto) | Actualizado: limpieza, palabras clave y rutas |

El modelo nuevo se entrena con `class_weight='balanced'`. F1 macro 0,7549 en
test, validación cruzada 0,7508 ± 0,0019 sobre 5 particiones.

---

## 1. Actualizar `nlp/requirements.txt` — esto primero

Ya viene corregido en la rama, pero hay que **reinstalar**:

```bash
pip install -r nlp/requirements.txt
```

El pin de scikit-learn pasó de `1.6.1` a `1.8.0`, que es la versión con la
que se entrenó. Los dos artefactos son pickles: el formato interno de
`TfidfVectorizer` y `LogisticRegression` cambia entre versiones, y cargarlos
con otra emite `InconsistentVersionWarning` y puede devolver predicciones
distintas sin que nada falle a la vista. `numpy` y `scipy` van fijados por lo
mismo.

---

## 2. Dejar de usar `app/ml/preprocesamiento.py`

Es el punto que más cambia el resultado visible.

`limpiar()` borra los caracteres `+ # . _ - /`, borra todos los dígitos y
descarta las palabras de dos letras o menos. El modelo se entrenó
conservando las tres cosas, así que el texto que recibe no es el texto con
el que aprendió.

Qué queda de cada entrada:

| Entrada | `app/ml/preprocesamiento.py` | `nlp/src/cleaning.py` |
|---|---|---|
| `Programar en C++ y C#` | `programar` | `Programar en C++ y C#` |
| `Pipelines de CI/CD con node.js` | `pipelines con node` | `Pipelines de CI/CD con node.js` |
| `Buckets S3 e instancias EC2` | `buckets instancias` | `Buckets S3 e instancias EC2` |
| `Modelos de AI con JS` | `modelos con` | `Modelos de AI con JS` |

Y así se ven las palabras clave que devuelve la API:

```
"Pipelines de CI/CD con Docker y node.js sobre buckets S3 en AWS"
   actual : buckets, pipelines, aws, docker, node
   módulo : ci cd, node js, AWS, S3, Docker

"Autenticación OAuth2 y JWT con maquetado HTML5 y ES6"
   actual : oauth, jwt, html
   módulo : OAuth2, JWT, Autenticación, HTML5, ES6
```

**Sobre la clasificación, sin exagerar:** con contenido de largo normal —lo
que la plataforma recibe de verdad— no medimos diferencia: 8 de 8 categorías
correctas con las dos limpiezas. Las palabras de contexto alcanzan para
decidir. La diferencia aparece con entradas muy cortas, donde el término
técnico *es* toda la señal: sobre 10 títulos de tres palabras, 6 aciertos
contra 4. Ninguna de las dos es confiable ahí, porque el modelo se entrenó
con textos de 20 palabras o más.

Es decir: el motivo fuerte para cambiar son **las palabras clave**, que el
usuario ve en cada respuesta. La clasificación es el motivo de fondo —el
texto de entrenamiento y el de servicio deben coincidir— pero hoy no se
manifiesta en las métricas.

El módulo ya expone todo el pipeline, no hace falta llamar a la limpieza
por separado:

```python
from src.inference import procesar_contenido, precargar_modelo

precargar_modelo()                     # en el arranque de la API
procesar_contenido(titulo, texto)      # en cada petición
```

Devuelve un dict listo para `json.dumps()`:

```json
{
  "categoria": "DevOps / Cloud",
  "probabilidad": 0.999,
  "informacion_adicional": ["Kubernetes", "AWS", "Docker", "Contenedores", "Despliegue"]
}
```

`categoria_alternativa` se agrega solo cuando `probabilidad` baja de 0,5.

---

## 3. Subir el modelo nuevo a Object Storage

`app/ml/loader.py` descarga de `settings.modelo_url` cuando el archivo no
está en disco. El `.joblib` cambió pero **conserva el nombre**, así que hay
que reemplazar el objeto en OCI. Si no, en producción sigue corriendo el
modelo viejo mientras el repositorio muestra el nuevo, y no hay nada que lo
delate.

---

## 4. Dónde busca el módulo los archivos

`src/config.py` prueba `nlp/models/` y después `modelos/`, y toma la primera
que exista. La variable de entorno manda por encima de las dos:

```bash
TECHMIND_MODELOS=/ruta/donde/descargues/los/artefactos
```

Se respeta aunque el directorio todavía no exista, para que el loader pueda
descargar ahí después de que el módulo se importe. Las tres rutas salen de
ese directorio: `MODELO_PATH`, `MATRIZ_HISTORICA_PATH` y `SUGERENCIAS_PATH`.

---

## 5. Dos endpoints nuevos

El frontend los necesita para las dos funciones que faltan. Los endpoints
actuales son `/contenido`, `/categorias`, `/chat`, `/biblioteca`, `/health`
y `/modelo/info`.

### `GET /sugerencias`

Los términos de los botones de la pantalla principal. Lectura directa del
JSON, sin modelo de por medio.

```python
import json
from src.config import SUGERENCIAS_PATH

with open(SUGERENCIAS_PATH, encoding="utf-8") as f:
    terminos = json.load(f)["terminos"]
# [{"termino": "terraform", "categoria": "DevOps / Cloud", "documentos": 120}, ...]
```

### `POST /relacionados`

Los documentos del histórico que hablan de lo mismo que el texto enviado.

```python
from src.config import MATRIZ_HISTORICA_PATH
from src.recommender import RecomendadorContenido

recomendador = RecomendadorContenido(MATRIZ_HISTORICA_PATH)   # una sola vez

resultados = recomendador.recomendar(f"{titulo} {texto}", top_n=3)
# [ContenidoRelacionado(id=..., titulo=..., categoria=..., similitud=0.35), ...]
```

Se instancia **en el arranque, junto a `precargar_modelo()`**. El `.pkl`
pesa 47 MB y cargarlo por petición agrega medio segundo a cada una.

Devuelve lista vacía cuando nada supera el umbral de 0,10 — es una respuesta
legítima, no un error: no siempre hay contenido relacionado. Conviene que el
frontend oculte la sección en ese caso en lugar de mostrarla vacía.

---

## 6. La API no arranca sin `DEEPSEEK_API_KEY`

`app/services/chat.py:10` crea el cliente `OpenAI(...)` al importarse el
módulo, y `app/routers/chat.py` lo importa. Sin la clave en el entorno,
falla el import y **no levanta la aplicación entera**, no solo el chat.

Conviene crear el cliente dentro de la función que lo usa, o detrás de un
`lru_cache`, para que la falta de la clave rompa únicamente `/chat`.

---

## 7. Validar el largo de la entrada en el esquema

Con una entrada sin contenido real —`"t"`, `"..."`— el módulo no lanza
error: devuelve la categoría más probable a priori con probabilidad ~0,17,
la lista de palabras clave vacía y `categoria_alternativa`. Es la respuesta
honesta, porque no hay señal de la que agarrarse.

El largo mínimo conviene validarlo en el esquema de Pydantic, antes de que
la petición llegue al modelo.

---

## Cómo comprobar que funciona

```bash
pip install -r nlp/requirements.txt
cd nlp && pytest
```

Esperado: **72 passed**.

```python
from src.inference import procesar_contenido
procesar_contenido("Despliegue con Docker", "Contenedores y Kubernetes en AWS")
# {'categoria': 'DevOps / Cloud', 'probabilidad': 0.999, ...}
```

Medido en este equipo: arranque 751 ms (modelo + matriz), 33 ms de mediana
por petición con clasificación, palabras clave y relacionados juntos, p95 de
49 ms. Las 8 categorías salen correctas sobre un caso representativo de cada
una.

---

## Lo que conviene no hacer

**No fusionar Backend con Programación General.** Las dos comparten
frontera —una agrupa frameworks (`spring`, `laravel`) y la otra lenguajes
(`python`, `rust`)— y ese cruce concentra el 8,7% de los errores del modelo.
Fusionarlas subiría el F1 macro 2,3 puntos, pero cambia la taxonomía sobre
la que están construidos la API y el frontend. Queda documentado como
decisión de producto, no como ajuste pendiente.

**No aplicar limpieza propia antes de llamar al módulo.** El `.joblib` es un
Pipeline completo: el `TfidfVectorizer` va adentro y hace su propio
preprocesamiento. Limpiar de más antes de entregarle el texto es
exactamente lo que produce el problema del punto 2.
