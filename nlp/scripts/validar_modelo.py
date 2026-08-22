"""
Valida que el modelo v2 (Pipeline TF-IDF + clasificador, en un solo
archivo) se pueda cargar correctamente y que la inferencia funcione
como se espera.

Uso:
    python scripts/validar_modelo.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.classifier import ClasificadorContenido
from src.config import MODELO_PATH
from src.exceptions import TechMindNLPError
from src.model_repository import RepositorioModelo

CATEGORIAS_ESPERADAS = {
    "Backend", "Bases de Datos", "Ciencia de Datos", "DevOps / Cloud",
    "Frontend", "Mobile", "Programación General", "Seguridad",
}

# Textos de prueba: mitad en inglés, mitad en español, para confirmar
# que el modelo bilingüe funciona en ambos idiomas.
CASOS_DE_PRUEBA = [
    ("CORS error in Flask", "How to fix CORS error in a Flask REST API"),
    ("Indexing en PostgreSQL", "Best indexing strategy for a PostgreSQL table"),
    ("Autenticación segura", "Cómo implementar autenticación segura con tokens JWT en una API"),
    ("Despliegue con contenedores", "Guía para desplegar una aplicación con Docker y Kubernetes"),
    ("Secure authentication with JWT",
     "How to implement secure authentication with JWT tokens in an API"),
]


def main() -> None:
    print("1) Cargando el modelo...")
    repositorio_modelo = RepositorioModelo(MODELO_PATH)
    try:
        pipeline = repositorio_modelo.obtener_pipeline()
    except TechMindNLPError as error:
        print(f"   ERROR: {error}")
        sys.exit(1)
    print("   OK\n")

    print("2) Verificando categorías del modelo...")
    categorias_modelo = {str(c) for c in pipeline.classes_}
    print(f"   Categorías encontradas: {sorted(categorias_modelo)}")
    faltantes = CATEGORIAS_ESPERADAS - categorias_modelo
    if faltantes:
        print(f"   ADVERTENCIA: faltan categorías esperadas: {faltantes}")
    else:
        print("   OK, coinciden con las 8 categorías esperadas")
    print()

    print("3) Probando inferencia con textos de ejemplo (EN + ES)...\n")
    clasificador = ClasificadorContenido(repositorio_modelo)
    for titulo, texto in CASOS_DE_PRUEBA:
        resultado = clasificador.clasificar(titulo, texto)
        print(f"   {titulo}: {texto!r}")
        print(f"   -> {resultado.categoria}  (probabilidad: {resultado.probabilidad:.3f})")
        if resultado.categoria_alternativa:
            print(f"      (confianza baja -> alternativa: {resultado.categoria_alternativa})")
        print(f"      palabras clave: {resultado.informacion_adicional}\n")

    print("Validación completa.")


if __name__ == "__main__":
    main()
