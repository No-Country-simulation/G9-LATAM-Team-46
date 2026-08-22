# models/

Los artefactos entrenados que consume la API. Todos salen de los notebooks
de `machine_learning/`, ejecutados sobre el dataset bilingüe.

| Archivo | Tamaño | Qué es |
|---|--:|---|
| `modelo_techmind_v2.joblib` | 5,9 MB | El clasificador |
| `matriz_historica.pkl` | 47 MB | Contenido relacionado |
| `sugerencias_botones.json` | 2 KB | Términos de los botones |
| `diccionario_categorias.json` | 2 KB | Las 8 categorías |

## `modelo_techmind_v2.joblib`

Un único `Pipeline` de scikit-learn con el vectorizador y el clasificador
adentro: recibe texto crudo y devuelve la predicción.

- `TfidfVectorizer`: `ngram_range=(1, 2)`, `min_df=5`, `max_features=60000`,
  `lowercase=True`. Sin lista de stopwords — le aportan algo de señal al
  clasificador, y para la respuesta al usuario se filtran aparte, en
  `src/keywords.py`.
- `LogisticRegression`: `C=4.0`, `max_iter=1000`, `class_weight='balanced'`.

`C=4.0` sale de un `GridSearchCV` sobre el Pipeline completo, con criterio
F1 macro. `class_weight='balanced'` compensa el desbalance: Seguridad tiene
2.792 ejemplos frente a los 5.396 de Frontend.

### Resultados

Sobre un test estratificado de **7.652 textos** que conserva la distribución
real y no se usó en ningún momento del entrenamiento:

| Métrica | Valor |
|---|--:|
| F1 macro | 0.7549 |
| Accuracy | 0.7530 |
| Validación cruzada (5 particiones) | 0.7508 ± 0.0019 |
| Línea base (clase más frecuente) | 0.0309 |

F1 por categoría, de mayor a menor: Mobile 0.85, Bases de Datos 0.84,
Ciencia de Datos 0.81, Frontend 0.81, Seguridad 0.75, DevOps / Cloud 0.72,
Programación General 0.64, Backend 0.63.

El modelo se entrena con los 30.605 registros de entrenamiento, no con el
dataset completo: el conjunto de prueba queda fuera para que las métricas
midan algo real.

## `matriz_historica.pkl`

Un diccionario con cinco claves: `vectorizador`, `matriz`, `ids`,
`categorias` y `titulos`. La matriz es dispersa en formato CSR y tiene los
38.257 documentos del corpus vectorizados.

El vectorizador viaja adentro a propósito: un texto nuevo tiene que
vectorizarse con el mismo vocabulario con el que se construyó la matriz, o
los vectores no serían comparables.

Lo consume `src/recommender.py`. Se carga una sola vez, al arranque.

## Por qué el clasificador es un solo archivo

Un `Pipeline` encapsula el vectorizador y el modelo: se carga una vez y el
preprocesamiento no puede desincronizarse. Mantenerlos como dos artefactos
sueltos obliga a coordinarlos a mano, con el riesgo de emparejar versiones
que no se corresponden.

## Requisitos que valida el pipeline al cargar

`RepositorioModelo` rechaza el `.joblib` con `ModeloInvalidoError` si no
cumple. Un modelo nuevo debe:

- Ser un `sklearn.pipeline.Pipeline` **entrenado** (tiene `classes_`).
- Exponer **`predict_proba`** — se usa para el campo `probabilidad` y
  para elegir la categoría alternativa. Un `LinearSVC` no sirve tal
  cual; habría que envolverlo en `CalibratedClassifierCV`.
- Tener el vectorizador en un paso llamado exactamente **`tfidf`**.
- Haber sido entrenado con texto procesado por una función de limpieza
  **idéntica** a `src/cleaning.py`.

`RecomendadorContenido` valida lo suyo por separado: el `.pkl` tiene que
traer las cinco claves, y la matriz se convierte a CSR si llegara en otro
formato.

## Compatibilidad de versiones

Entrenados con `scikit-learn==1.8.0`, fijado en `requirements.txt` junto con
`numpy` y `scipy`. La versión no es negociable: los dos archivos son pickles
y el formato interno de `TfidfVectorizer` y `LogisticRegression` cambia entre
versiones. Numpy va fijado porque los pickles llevan arreglos serializados
por numpy 2.x, y cargarlos con numpy 1.x falla con
`No module named 'numpy._core'`.

Si al cargar aparece un `InconsistentVersionWarning`, reinstalá el entorno
con `pip install -r requirements.txt` en Python 3.12.

## Validación

```bash
python scripts/validar_modelo.py
```

Comprueba que el `.joblib` cargue, que las 8 categorías coincidan con las
esperadas y que la inferencia funcione en ambos idiomas.
