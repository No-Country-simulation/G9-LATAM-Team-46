# Requisitos para reentrenar el modelo

Lo que cualquier modelo nuevo tiene que cumplir para que el pipeline de
inferencia lo acepte y la API siga devolviendo lo mismo. Están ordenados por
lo que cuesta si se pasan por alto.

El entrenamiento vigente está en `machine_learning/entrenamiento_modelo.ipynb`.

---

## 1. La limpieza del entrenamiento y la del servicio son la misma

Es el requisito que más silenciosamente se rompe: el modelo aprende con un
texto y recibe otro, y nada falla — solo empeoran las respuestas.

`src/cleaning.py` es la referencia. Conserva `+ # . _ - /` y los dígitos, y
no pasa a minúsculas por su cuenta:

| Se conserva | Porque si no |
|---|---|
| `+ #` | `C++` y `C#` quedan vacíos |
| `/` | `CI/CD` desaparece |
| `.` `_` `-` | `node.js` se reduce a `node` |
| dígitos | `HTML5`, `ES6`, `S3`, `EC2`, `OAuth2` pierden lo que los distingue |

Las minúsculas las aplica el `TfidfVectorizer` por su cuenta, así que
hacerlo antes es redundante.

Tampoco se filtra por longitud de palabra: descartar los tokens de dos
caracteres o menos elimina `js`, `ai`, `go` y `r`, que son de los términos
más discriminantes que hay.

## 2. Se entrena con `título + " " + texto`, en ese orden

Es exactamente lo que la API recibe en producción. Entrenar solo con el
cuerpo hace que el modelo aprenda una distribución y reciba otra.

`ClasificadorContenido` concatena en ese orden y hay una prueba que lo
cubre: `test_clasificar_concatena_titulo_y_texto_en_ese_orden`.

## 3. Dividir antes de balancear

Balancear primero duplica registros de las clases chicas, y esos duplicados
se reparten después entre entrenamiento y prueba. El modelo termina
evaluándose con textos que ya vio: las métricas suben y no significan nada.

```
CORRECTO      dividir  →  balancear solo el entrenamiento
INCORRECTO    balancear  →  dividir
```

El notebook de limpieza cierra con un control que cuenta cuántos textos del
conjunto de prueba aparecen también en el de entrenamiento. Tiene que dar
cero.

## 4. El conjunto de prueba conserva la distribución real

No se equilibra a propósito. Si se forzara, la evaluación mediría un
escenario que no existe: en producción las categorías llegan desparejas.

Y no se reentrena con el 100 % antes de serializar. El artefacto que se
entrega tiene que ser el mismo que se midió, o el número que se reporta no
describe el archivo que corre.

## 5. La forma del artefacto

`RepositorioModelo` rechaza el `.joblib` con `ModeloInvalidoError` si no
cumple:

- Un `sklearn.pipeline.Pipeline` **entrenado** (tiene `classes_`).
- Con `predict_proba` — se usa para `probabilidad` y para elegir la
  categoría alternativa. Un `LinearSVC` habría que envolverlo en
  `CalibratedClassifierCV`.
- Con el vectorizador en un paso llamado exactamente **`tfidf`**.

## 6. Los nombres de las 8 categorías no se tocan

Son los mismos que devuelve la API y muestra el frontend. Cambiar uno rompe
la cadena entera.

Por eso el mapeo de categorías se hace con un diccionario explícito y no con
una búsqueda por coincidencia de texto: buscar `"datos" in categoria` hace
coincidir tanto *Ciencia de Datos* como *Bases de Datos*, y las funde en una
sola sin ningún aviso.

## 7. Fijar la versión de scikit-learn

El `.joblib` y el `.pkl` son pickles. El formato interno de
`TfidfVectorizer` y `LogisticRegression` cambia entre versiones, y cargarlos
con otra devuelve resultados distintos sin que nada falle a la vista.

La versión con la que se entrenó va fijada en `requirements.txt`. Si se
reentrena con otra, hay que actualizar el pin en el mismo commit.

---

## Si se reentrena, hay que regenerar los cuatro artefactos

No alcanza con el `.joblib`. `matriz_historica.pkl` guarda el vectorizador
adentro, y `sugerencias_botones.json` sale del mismo vocabulario: si el
modelo cambia y ellos no, quedan hablando de un vocabulario que el modelo ya
no entiende.

```
machine_learning/entrenamiento_modelo.ipynb        -> modelo_techmind_v2.joblib
machine_learning/sugerencias_y_relacionados.ipynb  -> matriz_historica.pkl
                                                      sugerencias_botones.json
                                                      diccionario_categorias.json
```

Después, `cd nlp && pytest` (56 pruebas) y `python scripts/validar_modelo.py`.

---

## Frontera conocida: Backend y Programación General

Las dos comparten terreno —una agrupa frameworks (`spring`, `laravel`) y la
otra lenguajes (`python`, `rust`)— y muchos textos tocan ambas. Ese cruce
concentra el 8,7 % de los errores del modelo.

Fusionarlas subiría el F1 macro 2,3 puntos, pero cambia la taxonomía sobre
la que están construidos la API y el frontend. Es una decisión de producto,
no un ajuste técnico pendiente.
