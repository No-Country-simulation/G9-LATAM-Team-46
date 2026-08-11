# Dataset final — `techmind_dataset_v2.csv`

Dataset **bilingüe** (español + inglés) listo para que cada área lo use en su rama: EDA, Machine Learning, NLP, backend, etc.

Se entrega **crudo, sin EDA ni limpieza aplicada** — cada equipo hace su propio procesamiento sobre este archivo base.

## Contenido

- **38.276 documentos técnicos** etiquetados en **8 categorías**.
- **Bilingüe**: 36.714 en inglés + 1.562 en español (columna `idioma`).

## Columnas

| Columna | Descripción |
|---|---|
| `titulo` | Título del contenido técnico |
| `texto` | Cuerpo del documento (a clasificar) |
| `categoria` | Etiqueta objetivo — una de las 8 categorías |
| `palabras_clave` | Tags / palabras clave del contenido |
| `fuente` | Origen del registro (stackoverflow, medium, freecodecamp_es, wikipedia_es, corpus del equipo) |
| `idioma` | `es` o `en` |

## Las 8 categorías

`Backend` · `Frontend` · `Mobile` · `Ciencia de Datos` · `Bases de Datos` · `DevOps / Cloud` · `Seguridad` · `Programación General`

## Fuentes

Construcción propia del equipo a partir de fuentes públicas: StackOverflow 2020-2025 y Medium (Kaggle), freeCodeCamp en español, Wikipedia en español (CC BY-SA) y corpus de PDFs de cursos del equipo. Deduplicado y balanceado.

## Cómo cargarlo

```python
import pandas as pd
df = pd.read_csv("dataset/processed/techmind_dataset_v2.csv")
df.head()
```
