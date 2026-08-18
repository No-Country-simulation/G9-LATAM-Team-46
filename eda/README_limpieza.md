# Limpieza y EDA — `limpieza_y_eda_techmind_v2.ipynb`

## Requisitos

```bash
pip install -r requirements_limpieza.txt
```

Probado con Python 3.10

## Qué hace

Toma el dataset crudo y lo deja listo para entrenamiento, en un solo
notebook (sin archivos intermedios que se puedan desincronizar):

1. Verifica la integridad del CSV al cargarlo (detecta líneas mal formadas).
2. Documenta la recolección: qué aporta cada fuente (`stackoverflow`,
   `medium`, `freecodecamp_es`, `wikipedia_es`).
3. Normaliza valores faltantes (no elimina filas por un campo secundario vacío).
4. Mapea y corrige categorías (verifica que las 8 categorías originales
   sobrevivan la limpieza).
5. Limpia y normaliza el texto (formato + ortografía ligera), preservando
   caracteres técnicos (`C++`, `C#`, `CI/CD`, `TCP/IP`).
6. Filtra contenido muy corto y elimina duplicados.
7. Exporta el dataset limpio.
8. Divide en train/test **antes** de balancear, y balancea **solo** el
   train (evita fuga de datos entre train y test).
9. Corre el EDA completo: distribución de clases, nulos, duplicados,
   sesgos, longitud de documentos, palabras frecuentes y características
   por categoría, decisión sobre outliers, conclusiones y recomendaciones.

## Cómo correrlo

1. Sube `techmind_dataset_v2.csv` a la misma carpeta que el notebook.
2. `Entorno de ejecución` → `Reiniciar y ejecutar todo`.
3. Guarda el notebook (las salidas quedan embebidas en el `.ipynb`).

## Entrada

- `techmind_dataset_v2.csv` (dataset crudo)

## Salidas (entregables)

| Archivo | Contenido |
|---|---|
| `dataset_limpio.csv` | Dataset limpio completo, listo para entrenar |
| `dataset_balanceado.csv` / `train_dataset.csv` | Partición de entrenamiento, balanceada |
| `test_dataset.csv` | Partición de prueba, con la distribución real (sin balancear) |
| `diccionario_categorias.json` | Categorías y su descripción |
| `documento_fuentes.md` | De dónde viene cada parte del dataset |
| `informe_analisis_eda.md` | Hallazgos y decisiones del EDA |
| `recomendaciones_dataset.md` | Mejoras propuestas al dataset |
| `distribucion_y_longitud.png`, `top_palabras_frecuentes.png`, `palabras_caracteristicas_por_categoria.png` | Gráficos del EDA |

Estos archivos (en especial `dataset_limpio.csv`, o su copia renombrada
`dataset_limpio_techmind_v2.csv`) son la entrada del siguiente paso:
entrenamiento del modelo (`ml_data_v4.ipynb`).
