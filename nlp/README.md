# techmind-nlp-pipeline

Pipeline de procesamiento de texto y preparación para producción del
modelo de clasificación de contenido técnico (Hackathon ONE G9 - Alura/Oracle).

Rol: Ingeniero NLP y Preparación para Producción.

## Estructura del proyecto

```
techmind-nlp-pipeline/
├── src/
│   ├── __init__.py
│   ├── preprocessing.py   # Tokenización, stopwords, lematización (Bloque 2) ✅
│   ├── keywords.py        # Extracción de palabras clave (Bloque 3)
│   └── inference.py       # Pipeline de inferencia completo (Bloque 4)
├── scripts/
│   └── validar_modelo.py  # Valida carga del modelo real y hace predicciones de prueba
├── models/
│   ├── README.md                        # Detalles del modelo elegido y su procedencia
│   ├── modelo_techmind_v1.joblib        # Modelo real (agrégalo tú aquí, no viaja en este zip)
│   └── vectorizador_tfidf_v1.joblib     # Vectorizador real (agrégalo tú aquí, no viaja en este zip)
├── tests/
│   ├── __init__.py
│   └── test_preprocessing.py
├── requirements.txt
└── README.md
```

**Nota:** los `.joblib` no vienen incluidos (Se pueden descargar 
del Colab del equipo de modelado) — cópialos a `models/`
antes de correr `scripts/validar_modelo.py`.

## Cómo levantar el entorno (local, VSCode)

```bash
# Crear y activar entorno virtual
python -m venv .venv
source .venv/bin/activate        # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Descargar recursos de NLTK necesarios (se hace una sola vez)
python -m nltk.downloader punkt stopwords wordnet
```

## Contrato de salida del pipeline de inferencia

```json
{
  "categoria": "Backend",
  "probabilidad": 0.83,
  "informacion_adicional": {
    "palabras_clave": ["api", "rest", "endpoint"]
  }
}
```

## Estado actual

- [x] Bloque 1: Estructura del proyecto + requirements.txt
- [x] Bloque 2: Preprocesamiento (limpiar_texto, tokenizar, eliminar_stopwords, lematizar)
- [ ] Bloque 3: Extracción de palabras clave
- [ ] Bloque 4: Pipeline de inferencia
- [ ] Bloque 5: Modularización y documentación final
- [x] Bloque 6 (parcial): carga del modelo real y pruebas de inferencia validadas con `scripts/validar_modelo.py` — predicciones razonables en las 8 categorías. Pendiente: reinstalar `requirements.txt` con `scikit-learn==1.6.1` fijado para eliminar el InconsistentVersionWarning.

## Notas de compatibilidad con el modelo

- El modelo fue entrenado con `scikit-learn==1.6.1` (confirmado por el
  `InconsistentVersionWarning` al cargarlo con una versión distinta). Ya
  está fijado así en `requirements.txt` — reinstalar con
  `pip install -r requirements.txt` en un entorno limpio para eliminar
  la advertencia.
-
- `limpiar_texto()` en `src/preprocessing.py` es una réplica exacta de la
  función `limpiar()` del notebook de modelado (verificado con pruebas).
  Es la única función de limpieza que debe usarse antes de vectorizar
  texto para clasificación — `tokenizar`, `eliminar_stopwords` y
  `lematizar` son para el módulo de palabras clave (Bloque 3), no para
  el pipeline de clasificación.
