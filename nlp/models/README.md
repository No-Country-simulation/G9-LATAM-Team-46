# models/

Modelo y vectorizador, entrenados por el equipo de modelado
y confirmados como versión final del hackatón:

- `modelo_techmind_v1.joblib` — Regresión Logística (`modelo_lr`,
  `class_weight='balanced'`, `max_iter=1000`), accuracy 0.7535 en test.
  Se comparó contra Naive Bayes (0.6964, descartado) y una versión
  optimizada con GridSearchCV (0.7521, sin mejora significativa) —
  se eligió el modelo original por ser igual de bueno y más simple.
- `vectorizador_tfidf_v1.joblib` — TfidfVectorizer (`max_features=5000`,
  `stop_words='english'`, `ngram_range=(1, 2)`, `min_df=3`).

## Compatibilidad de versiones

Entrenados con `scikit-learn==1.6.1` — esta versión ya está fijada en
`requirements.txt`. Si cargas el modelo con una versión distinta,
verás un `InconsistentVersionWarning`; si eso pasa, reinstala el
entorno con `pip install -r requirements.txt` en Python 3.12.

## Validación

Corre `python scripts/validar_modelo.py` para confirmar que ambos
archivos cargan correctamente y que las predicciones son coherentes.
Última corrida: las 8 categorías detectadas correctamente, sin
warnings de versión.
