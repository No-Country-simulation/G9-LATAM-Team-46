# Entrega DS — Perfilado TF-IDF + EDA

## Contenido

```text
TechMindV5_Entrega_Perfilado_TFIDF/
├── data/DataSetTechmindV5_perfilado.csv   # corpus TF-IDF-ready
├── notebooks/02_EDA_Hito2.ipynb           # EDA (pandas/numpy/matplotlib/seaborn)
├── docs/figures/                          # PNG del EDA
├── docs/EDA_*.md / *.json                 # hallazgos (tras Run All)
└── requirements.txt
```

## Ejecutar EDA

```bash
cd TechMindV5_Entrega_Perfilado_TFIDF
pip install -r requirements.txt
jupyter notebook notebooks/02_EDA_Hito2.ipynb
# Restart & Run All  → figuras en el notebook y en docs/figures/
```

El notebook carga `data/DataSetTechmindV5_perfilado.csv` por ruta relativa (cwd = raíz del paquete o `notebooks/`).
