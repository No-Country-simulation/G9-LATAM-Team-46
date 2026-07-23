# Banco de datos V5 — TechMind (Team 46)

Paquete local del **corpus de clasificación V5** (general + train + árbol completo).

| Métrica | Valor |
|---------|------:|
| General | **530** |
| Train | **477** |
| Clases L1 | **7** |
| Ratio max/min train | **2.872** |

## Contenido

| Ruta | Descripción |
|------|-------------|
| `data/dataset_general_v5.csv` | Corpus completo V5 |
| `data/dataset_entrenamiento_v5.csv` | Subconjunto para modelado |
| `docs/arbol_conocimiento_v5_completo.md` | Árbol de conocimientos fusionado (v2 base + v3/v4/v5) |
| `docs/VERIFICACION_arbol_vs_datasets_v5.md` | Verificación de coherencia |
| `DICCIONARIO_DATOS.md` | Schema y conteos |
| `MANIFEST.json` | Metadatos máquina-legibles |
| `CHECKSUMS.sha256` | Integridad |

## Cadena

```text
PDFs → v2 balanceo → v3 Hardware → v4 Ciberseguridad → v5 IA texto/ML
```

## Cómo usar (modelado)

```python
import pandas as pd

general = pd.read_csv("data/dataset_general_v5.csv")
train = pd.read_csv("data/dataset_entrenamiento_v5.csv")

X = train["texto_crudo"]
y = train["categoria_l1"]
```

Requisitos sugeridos: Python 3.10+, pandas, scikit-learn.

## Integridad

```powershell
Get-FileHash data\dataset_general_v5.csv -Algorithm SHA256
# comparar con CHECKSUMS.sha256
```

## Nota de distribución

**Estado:** listo en disco local. **No se ha enviado** al resto del equipo.  
Sin PDF fuente (material privado).

---

*Paquete `BancoDatos_V5_20260723` · creado 2026-07-23T01:16:20.706816+00:00*
