# Paquete DataSetTechmindV1

Corpus unificado de corrección TechMind (Team 46).

| | |
|--|--:|
| Filas | **668** |
| Nativo / Synth / OCR | 343 / 38 / 287 |
| Ratio max/min L1 | 3.73 |
| SHA-256 | `499fa5a1e122bf3a5ffdca83c0a5f691…` |

## Contenido

| Ruta | Descripción |
|------|-------------|
| `data/DataSetTechmindV1.csv` | Dataset principal |
| `data/DataSetTechmindV1_entrenamiento.csv` | Copia train (= general) |
| `data/DataSetTechmindV1.DATASHEET.md` | Ficha técnica |
| `data/DataSetTechmindV1.ARBOL.md` | Árbol de conocimientos |
| `docs/` | Copias de ficha y árbol |
| `MANIFEST.json` | Metadatos |
| `CHECKSUMS.sha256` | Integridad |
| `notebooks/EDA_DataSetTechmindV1.ipynb` | EDA y visualizaciones |
| `README.md` | Este archivo |

## Uso rápido

```python
import pandas as pd
df = pd.read_csv("data/DataSetTechmindV1.csv")
X, y = df["texto_crudo"], df["categoria_l1"]
```

**Estado:** listo en local. **No enviado** al remoto hasta solicitud explícita.
