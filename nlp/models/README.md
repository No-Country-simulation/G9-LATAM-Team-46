# models/

Modelo **real** entrenado por el equipo de modelado, versión final del
hackatón.

- `modelo_techmind_v2.joblib` — un único `Pipeline` de scikit-learn
  serializado (6,2 MB), entrenado con el dataset bilingüe (inglés +
  español). Reemplaza los dos archivos del v1.
  - `TfidfVectorizer`: `ngram_range=(1, 2)`, `sublinear_tf=False`,
    `min_df=5`, `max_features=60000`, **sin lista de stopwords**
    (`stop_words=None`). Verificado con
    `scripts/inspeccionar_modelo.py`: el vocabulario contiene `the`,
    y llega justo a las 60.000 features, es decir que `max_features`
    está recortando (había más candidatos tras `min_df=5`).
  - `LogisticRegression`: `C=4.0`, `max_iter=1000`,
    `class_weight=None` (sin rebalanceo de clases).
  - Accuracy **0.7761** sobre test estratificado de 7.658 textos.
    F1 por categoría entre 0.65 (Backend) y 0.88 (Mobile).

El modelo entregado se re-entrenó con el 100 % del dataset; el accuracy
de arriba se midió con el modelo entrenado sobre el 80 %.

## Por qué un solo archivo

El v1 eran dos artefactos (`modelo` + `vectorizador`) que había que
cargar y coordinar por separado, con el riesgo de emparejar versiones
que no se correspondían. Un `Pipeline` los encapsula: se carga una vez
y no puede desincronizarse.

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

## Compatibilidad de versiones

Entrenado con `scikit-learn==1.6.1`, fijado en `requirements.txt` junto
con `numpy` y `scipy`. Numpy va fijado a propósito: el `.joblib` es un
pickle con arreglos serializados por numpy 2.x, y cargarlo con numpy 1.x
falla con `No module named 'numpy._core'`.

Si al cargar aparece un `InconsistentVersionWarning`, reinstala el
entorno con `pip install -r requirements.txt` en Python 3.12.

## Validación

```bash
python scripts/validar_modelo.py
```

Comprueba que el `.joblib` cargue, que las 8 categorías coincidan con
las esperadas y que la inferencia funcione en ambos idiomas. Última
corrida: carga OK, 8/8 categorías, cinco casos de prueba. Cuatro
aciertan con confianza entre 0.787 y 0.992; el quinto
("Cómo implementar autenticación segura con tokens JWT en una API")
queda en 0.353 y devuelve Seguridad como `categoria_alternativa`. El
mismo texto en inglés da Seguridad con 0.979 — la diferencia es de
cobertura del vocabulario en español, no de ambigüedad entre
categorías.

Para inspeccionar los hiperparámetros reales del vectorizador:

```bash
python scripts/inspeccionar_modelo.py
```

Los valores de este documento salen de ahí, no del notebook.
