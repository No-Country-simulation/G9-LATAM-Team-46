# Notas para el equipo de modelado (notebook v2)

## Decisión: se mantiene el modelo v2 de Lucio

Se evaluó una alternativa (v3: limpieza de Edmer corregida + vectorizador
de Lucio + stopwords ampliadas) con una ablación de 4 configuraciones sobre
el mismo split estratificado de 7.658 textos:

| Configuración | Accuracy | F1 ponderado |
|---|---|---|
| A. Edmer original (con bug) | 0.7464 | 0.7467 |
| B. Edmer con el bug corregido | 0.7614 | 0.7615 |
| **C. Lucio v2 (entregado)** | **0.7755** | **0.7759** |
| D. Híbrido (v3 candidato) | 0.7834 | 0.7834 |

**Se entrega C**, aunque D mide 0.0079 más. Razones:

1. La diferencia son 60 textos de 7.658 — 1,67 errores estándar (no
   pareado). No es concluyente sin una prueba de McNemar sobre las
   predicciones pareadas, que no se corrió.
2. Adoptar D obliga a reemplazar `src/cleaning.py` por la limpieza de
   Edmer y a reescribir las pruebas de limpieza. Con la API ya integrada
   contra el v2 y el tiempo restante, el riesgo supera a la ganancia.
3. La mejora visible de D (palabras clave sin relleno) se obtuvo por otra
   vía sin re-entrenar: el filtro de n-gramas redundantes en
   `src/keywords.py`.

Hallazgo que vale conservar: el notebook de Edmer tenía un bug que
colapsaba los 24 términos técnicos protegidos (`python`, `java`, `sql`,
`ios`, `php`, `flask`, `c#`...) en el mismo token `"kw"`. El marcador
`__kw{i}__` no sobrevivía al filtro `[^a-záéíóúñ\s]`, que elimina guiones
bajos y dígitos. Costaba **1,5 puntos** de accuracy. Está corregido en
`notebook_edmer_corregido.py` por si hay un v3.

Lo que sigue abajo se mantiene como referencia para una versión futura.

---

Hallazgos desde el lado del pipeline de inferencia. Van ordenados por
impacto. Los puntos 1 y 2 requieren re-entrenar, así que la decisión es
del equipo de modelado — desde acá no se puede hacer.

---

## 1. Las palabras clave traen ruido en español (impacto en la demo)

En el ejemplo de salida del propio notebook, 3 de las 4 palabras clave
del caso en español no aportan nada:

```json
"informacion_adicional": ["apis rest", "presentan", "java spring", "conceptos"]
```

`presentan` y `conceptos` son relleno. Y esto **se ve en pantalla
durante la demo**, al lado de la categoría — pesa más de lo que sugiere
su efecto sobre el accuracy (que es nulo: la clasificación no cambia).

**Causa:** la lista `STOP` filtra bien el inglés porque hereda
`ENGLISH_STOP_WORDS` de sklearn (~318 términos) más una lista manual de
palabras genéricas. La parte en español es una lista escrita a mano que
cubre bien artículos, preposiciones y pronombres, pero **no cubre verbos
ni sustantivos genéricos del lenguaje de tutoriales**, que es
exactamente el registro del contenido en español del dataset
(freeCodeCamp, Wikipedia, PDFs de cursos).

**Arreglo propuesto:** agregar este bloque a `STOP` y re-entrenar. Los
términos van con y sin acento a propósito, porque parte del corpus viene
sin acentuar (se ve en las pruebas tipo jurado: "creacion", "basicos"):

```python
STOP_ES_GENERICAS = {
    # Verbos de tutorial
    "aprende", "aprender", "aprendemos", "veremos", "vemos", "vamos",
    "presenta", "presentan", "presentamos", "muestra", "muestran",
    "explica", "explican", "explicamos", "crear", "crea", "crean",
    "creamos", "utiliza", "utilizan", "utilizar", "utilizando",
    "utilizado", "permite", "permiten", "conocer", "saber", "obtener",
    "realizar", "realiza", "aplicar", "aplica", "seguir", "sigue",
    "necesitas", "necesita", "debes", "debe", "deben", "podemos",
    "podras", "podrás", "quieres", "aqui", "aquí",

    # Sustantivos genéricos
    "concepto", "conceptos", "creacion", "creación", "ejemplo",
    "ejemplos", "tutorial", "tutoriales", "guia", "guía", "curso",
    "cursos", "articulo", "artículo", "parte", "partes", "caso",
    "casos", "forma", "formas", "manera", "maneras", "tipo", "tipos",
    "vez", "veces", "cosa", "cosas", "tema", "temas", "punto",
    "puntos", "paso", "pasos", "contenido", "contenidos", "seccion",
    "sección", "capitulo", "capítulo", "introduccion", "introducción",
    "continuacion", "continuación", "siguiente", "siguientes",
    "primero", "primera", "segundo", "segunda", "ultimo", "última",

    # Adjetivos y adverbios de relleno
    "basico", "básico", "basicos", "básicos", "basica", "básica",
    "simple", "sencillo", "sencilla", "facil", "fácil", "importante",
    "necesario", "necesaria", "posible", "mejor", "mejores", "bueno",
    "buena", "nuevo", "nueva", "nuevos", "nuevas", "gran", "grande",
    "solo", "sólo", "siempre", "nunca", "ahora", "luego", "despues",
    "después", "antes", "durante", "mismo", "misma", "mismos",
}

STOP = STOP | STOP_ES_GENERICAS
```

**Cómo verificar que sirvió:** correr el bloque de pruebas tipo jurado
de la sección 6 con `predecir()` y mirar las palabras clave, no solo la
categoría. El objetivo es que ninguna de las 8 devuelva términos de
relleno.

**Riesgo a controlar:** ampliar stopwords cambia el vocabulario, así que
el accuracy se mueve. Debería moverse poco (son términos poco
discriminativos por definición) pero hay que volver a correr el
`classification_report` y confirmar que no baja de forma apreciable.
Si bajara, el compromiso razonable es dejar las stopwords ampliadas
**solo para la extracción de palabras clave** y no para la
clasificación — implicaría entregar el vectorizador con dos vocabularios
o filtrar en post-proceso, lo cual complica el pipeline; conviene
intentar primero el camino simple.

---

## 2. El español es el 4,1 % del dataset

1.573 de 38.287 registros. Mobile tiene solo 55 ejemplos en español.

Las 8 pruebas tipo jurado pasan, pero están escritas con vocabulario
técnico casi idéntico en ambos idiomas (`docker`, `kubernetes`, `react`,
`sql`, `pandas`). Esos términos los acierta el modelo por el lado
inglés del vocabulario, no por el español.

**El riesgo está en el español coloquial sin anglicismos.** El caso
`"Como hacer una pagina web html"` (que ya está en
`scripts/simular_entrega_json.py`) es justo ese perfil, y es el tipo de
frase que un jurado escribiría espontáneamente.

**Sugerencia si hay tiempo:** correr 10-15 frases en español natural
—sin nombres de tecnologías— y ver cuántas quedan por debajo del umbral
de 0.5. Si son muchas, la respuesta honesta y presentable es que el
campo `categoria_alternativa` existe precisamente para eso. Si son
pocas, es un dato fuerte para la presentación.

No sugiero rebalancear el dataset a esta altura del hackatón: es caro y
puede romper lo que ya funciona.

---

## 3. Números que no cuadran entre la corrida y el texto

Ninguno afecta al código, pero un jurado técnico que lea con atención
los va a ver, y restan más credibilidad de lo que cuesta arreglarlos.

| Dónde | Dice | La corrida da |
|---|---|---|
| Tabla de conclusión final | Accuracy 77,9 % | `0.7761` → **77,6 %** |
| Tabla de conclusión final | 7.656 textos de test | soporte del report = **7.658** |
| Interpretación sección 6 | confianza 0.85–1.00 | mínimo real **0.81** (Seguridad) |
| Procedencia del dataset | 38.276 documentos | **38.287** |
| Procedencia del dataset | 1.562 en español | **1.573** |
| Tabla de fuentes | corpus propio: 524 | `corpus_es_ocr` 287 + `corpus_es_pdf` 248 = **535** |

El resto sí cuadra: verifiqué el crosstab idioma×categoría contra los
`value_counts` y las 8 categorías suman exacto.

---

## 4. Precisión al reportar el accuracy

El 77,6 % se midió con `modelo` + `vector`, entrenados con el 80 % del
dataset. El objeto que se serializa es `pipeline`, re-entrenado con el
**100 %** (`pipeline.fit(X, y)`).

Eso es práctica correcta y estándar — no hay que cambiarlo. Pero la
frase precisa para la presentación es: *"77,6 % medido sobre un test
estratificado de 7.658 textos; el modelo entregado se re-entrenó con el
dataset completo"*. Si alguien del jurado pregunta si el 77,6 % es del
archivo entregado, la respuesta es que no exactamente, y conviene tenerla
lista.

Consecuencia práctica: las pruebas de la sección 6 usan `modelo`+`vector`
mientras que `predecir()` usa `pipeline`. Son modelos distintos, así que
las probabilidades de la demo pueden no coincidir con las de esa celda.

---

## 5. La función `predecir()` del notebook no replica el entrenamiento

`predecir(texto)` hace `limpiar(texto)` — solo el texto. Pero el modelo
se entrenó con:

```python
df['texto_limpio'] = (df['titulo'].fillna('') + ' ' + df['texto'].fillna('')).apply(limpiar)
```

Es decir, `titulo + " " + texto`. Si el backend copiara `predecir()`, le
estaría dando al modelo una entrada con distinta distribución a la que
aprendió.

**Ya está resuelto del lado del pipeline:** `ClasificadorContenido`
concatena en el orden correcto, y hay una prueba que lo cubre
(`test_clasificar_concatena_titulo_y_texto_en_ese_orden`). La API debe
usar `src.inference.procesar_contenido()`, no `predecir()`.

Sugerencia: dejar `predecir()` en el notebook con un comentario que diga
que es de referencia y que la versión de producción está en
`techmind-nlp-pipeline`, para que nadie la copie por error.

---

## 6. Detalle menor: cantidad de palabras clave

El notebook usa `top_k=4`; el pipeline usa `TOP_N_PALABRAS_CLAVE = 5`.
Cualquiera sirve, pero conviene igualarlos para que la demo muestre lo
mismo que la documentación.
