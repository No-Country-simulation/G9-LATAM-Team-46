"""
Simula la entrega del JSON que el pipeline de inferencia le daría a la
API -- usa los mismos textos ya probados en Colab con el modelo v2,
para confirmar que el pipeline local produce el mismo resultado.

Uso:
    python scripts/simular_entrega_json.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.exceptions import TechMindNLPError
from src.inference import procesar_contenido

# Mismos textos usados en los demos compartidos con el equipo (incluye
# los casos en español que confirmaron la mejora del modelo bilingüe).
CASOS_DE_PRUEBA = [
    {"titulo": "CORS error in Flask", "texto": "How to fix CORS error in a Flask REST API"},
    {"titulo": "Indexado en PostgreSQL", "texto": "Best indexing strategy for a PostgreSQL table with millions of rows"},
    {"titulo": "Drag and drop en React", "texto": "Building a drag and drop UI with React"},
    {"titulo": "Consulta lenta", "texto": "Cómo optimizar una consulta que tarda mucho en ejecutarse"},
    {"titulo": "Autenticación", "texto": "Cómo implementar autenticación segura con tokens JWT en una API"},
    {"titulo": "Despliegue con contenedores", "texto": "Guía para desplegar una aplicación con Docker y Kubernetes"},
    {"titulo": "Página web en español", "texto": "Como hacer una pagina web html"},
]


def main() -> None:
    for caso in CASOS_DE_PRUEBA:
        print(f"Entrada: {caso['titulo']!r} / {caso['texto']!r}")
        try:
            resultado = procesar_contenido(caso["titulo"], caso["texto"])
            print(json.dumps(resultado, indent=2, ensure_ascii=False))
        except TechMindNLPError as error:
            print(f"  ERROR ({type(error).__name__}): {error}")
        print()


if __name__ == "__main__":
    main()
