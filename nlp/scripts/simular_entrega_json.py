"""
Simula la entrega del JSON que el pipeline de inferencia le daría a la
API — usa los mismos textos de los demos ya probados con el equipo,
para mostrar el contrato de salida completo (categoría, confianza,
alerta de confianza baja, y palabras clave).

Uso:
    python scripts/simular_entrega_json.py
"""

import json

from src.inference import procesar_contenido

# Los mismos textos usados en los demos que se compartieron con el equipo.
CASOS_DE_PRUEBA = [
    {
        "titulo": "CORS error in Flask",
        "texto": "How to fix CORS error in a Flask REST API",
    },
    {
        "titulo": "Indexado en PostgreSQL",
        "texto": "Best indexing strategy for a PostgreSQL table with millions of rows",
    },
    {
        "titulo": "Drag and drop en React",
        "texto": "Building a drag and drop UI with React",
    },
    {
        "titulo": "Página web en español",
        "texto": "Como hacer una pagina web html",
    },
    {
        "titulo": "Consulta lenta",
        "texto": "Cómo optimizar una consulta que tarda mucho en ejecutarse",
    },
]


def main():
    for caso in CASOS_DE_PRUEBA:
        resultado = procesar_contenido(caso["titulo"], caso["texto"])
        print(f"Entrada: {caso['titulo']!r} / {caso['texto']!r}")
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
        print()


if __name__ == "__main__":
    main()
