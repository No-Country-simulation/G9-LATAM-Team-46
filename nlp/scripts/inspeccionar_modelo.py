"""
Imprime los hiperparámetros reales del vectorizador y del clasificador
serializados en el `.joblib`.

Existe porque la documentación del proyecto llegó a describir un modelo
distinto al entregado (decía `min_df=3`, `sublinear_tf=True` y una lista
de 678 stopwords; el modelo real usa `min_df=5`, `sublinear_tf=False` y
ninguna stopword). Los valores que aparecen en `README.md` y en
`models/README.md` salen de este script, no del notebook.

Uso:
    python scripts/inspeccionar_modelo.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import joblib

from src.config import MODELO_PATH


def main() -> None:
    pipeline = joblib.load(MODELO_PATH)
    tfidf = pipeline.named_steps["tfidf"]
    clf = pipeline.named_steps.get("clf")

    print("Vectorizador (paso 'tfidf'):")
    print("  min_df:", tfidf.min_df)
    print("  sublinear_tf:", tfidf.sublinear_tf)
    print("  max_features:", tfidf.max_features)
    print("  ngram_range:", tfidf.ngram_range)
    print("  stop_words:", None if tfidf.stop_words is None else len(tfidf.stop_words))
    print("  features en el vocabulario:", len(tfidf.vocabulary_))
    # Si 'the' está en el vocabulario, el modelo se entrenó sin quitar
    # stopwords: es la comprobación independiente de la línea anterior.
    print("  'the' en el vocabulario:", "the" in tfidf.vocabulary_)

    if clf is not None:
        print("\nClasificador (paso 'clf'):", type(clf).__name__)
        for parametro in ("C", "max_iter", "class_weight"):
            if hasattr(clf, parametro):
                print(f"  {parametro}:", getattr(clf, parametro))

    print("\nCategorías:", list(pipeline.classes_))


if __name__ == "__main__":
    main()
