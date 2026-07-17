# Dataset — TechMind AI

Carpeta dedicada a la **Etapa 2 (Construcción del Dataset)** y **Etapa 3 (Exploración y Preparación)** del proyecto. Aquí se extraen, perfilan y preparan los datos que alimentarán el modelo de clasificación de contenido técnico.

## Estructura

```
dataset/
├── notebooks/
│   └── 01_extraccion_datasets.ipynb   # Extracción desde Kaggle + perfilado de cada dataset
├── raw/                               # Datos crudos descargados (no versionado en git)
├── processed/                         # Datos limpios/listos para entrenamiento (no versionado en git)
├── .gitignore                         # Excluye contenido de raw/ y processed/
└── README.md
```

`raw/` y `processed/` se mantienen vacíos en git (solo con `.gitkeep`) porque los datasets pueden pesar cientos de MB. Cada integrante debe generarlos localmente ejecutando el notebook.

## Datasets candidatos

| # | Dataset (Kaggle) | Contenido | Rol propuesto |
|---|---|---|---|
| 1 | `stackoverflow/stacksample` | Preguntas/respuestas de Stack Overflow con tags | Fuente principal de contenido técnico ya etiquetado por tecnología |
| 2 | `fabiochiusano/medium-articles` | Artículos largos de Medium con tags | Contenido tipo "artículo/tutorial" para diversificar categorías |
| 3 | `hsankesara/medium-articles` | Artículos de Medium (dataset más pequeño) | Alternativa/complemento al anterior, útil para pruebas rápidas |
| 4 | `kutayahin/stackoverflow-programming-questions-2020-2025` | Preguntas recientes de Stack Overflow (2020-2025) | Reduce sesgo hacia tecnologías antiguas del StackSample original |
| 5 | `sunilthite/text-document-classification-dataset` | Documentos genéricos ya categorizados | Baseline/referencia para validar el pipeline de clasificación |

## Cómo usar

1. Instalar dependencias:
   ```bash
   pip install kagglehub[pandas-datasets] pandas
   ```
2. Configurar credenciales de Kaggle (`kaggle.json` en `~/.kaggle/` o `kagglehub.login()`).
3. Abrir `notebooks/01_extraccion_datasets.ipynb` y ejecutar las celdas. Cada dataset se carga, se perfila (shape, columnas, nulos, muestra) y se agrega a una tabla comparativa al final.
4. Con la tabla comparativa, decidir qué dataset(s) usar como base para el modelo (ver criterios al final del notebook).
5. Guardar el subconjunto elegido (crudo) en `raw/` y, tras la limpieza de la Etapa 3, el resultado en `processed/`.

## Próximos pasos (Etapa 3)

- Limpieza de texto y normalización.
- Eliminación de duplicados y stopwords.
- Tokenización.
- Análisis de distribución de categorías/tags.
- Preparación del dataset final de entrenamiento.
