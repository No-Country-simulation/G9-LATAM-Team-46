"""
Valida que el modelo y el vectorizador entrenados
se puedan cargar correctamente y que la inferencia funcione
como se espera.

Uso:
    python scripts/validar_modelo.py
"""

import os

import joblib

MODELO_PATH = os.path.join("models", "modelo_techmind_v1.joblib")
VECTORIZADOR_PATH = os.path.join("models", "vectorizador_tfidf_v1.joblib")

CATEGORIAS_ESPERADAS = {
    "Backend", "Bases de Datos", "Ciencia de Datos", "DevOps / Cloud",
    "Frontend", "Mobile", "Programación General", "Seguridad",
}

# Textos de prueba pensados para "apuntar" claramente a una categoría,
# así podemos ver a simple vista si la predicción tiene sentido.
TEXTOS_DE_PRUEBA = [
    "how to configure a rest api endpoint with jwt authentication",
    "writing an efficient sql join query with indexes",
    "training a classification model with scikit learn",
    "deploying a docker container with kubernetes",
    "building a responsive layout with css grid in react",
    "fixing a gradle build error in an android project",
    "implementing a binary search algorithm in python",
    "preventing sql injection in a web application",
]


def main():
    print("1) Cargando modelo y vectorizador...")
    modelo = joblib.load(MODELO_PATH)
    vector = joblib.load(VECTORIZADOR_PATH)
    print("   OK\n")

    print("2) Verificando categorías del modelo...")
    categorias_modelo = {str(c) for c in modelo.classes_}
    print(f"   Categorías encontradas: {sorted(categorias_modelo)}")
    faltantes = CATEGORIAS_ESPERADAS - categorias_modelo
    if faltantes:
        print(f"   ADVERTENCIA: faltan categorías esperadas: {faltantes}")
    else:
        print("   OK, coinciden con las 8 categorías esperadas")
    print()

    print("3) Probando inferencia con textos de ejemplo...\n")
    for texto in TEXTOS_DE_PRUEBA:
        X = vector.transform([texto])
        pred = modelo.predict(X)[0]
        proba = modelo.predict_proba(X).max()
        print(f"   Texto: {texto}")
        print(f"   -> Categoría: {pred}  (confianza: {proba:.3f})\n")

    print("Validación completa.")


if __name__ == "__main__":
    main()
