"""
Pruebas del módulo de extracción de palabras clave.

Los dos primeros casos usan los mismos textos con los que se probó el
demo de lematización, para confirmar que el comportamiento se mantiene
al formalizarlo dentro del pipeline (src/keywords.py).
"""

from src.keywords import extraer_palabras_clave


def test_extraer_palabras_clave_agrupa_variantes_por_lema():
    texto = (
        "This tutorial covers databases, database indexing, and how a "
        "database engine optimizes queries across multiple databases."
    )
    resultado = extraer_palabras_clave(texto, top_n=5)
    # 'database'/'databases' deben agruparse en un solo lema con conteo 4
    assert resultado[0] == ("database", 4)


def test_extraer_palabras_clave_filtra_stopword_adicional():
    texto = (
        "We compare classifiers: a classifier trained on images, another "
        "classifier for text, and a final classifier ensemble."
    )
    resultado = extraer_palabras_clave(texto, top_n=5)
    palabras = [palabra for palabra, _ in resultado]

    # 'classifier' debe ser la más frecuente (agrupando 'classifiers')
    assert resultado[0] == ("classifier", 4)
    # 'another' NO debe aparecer como palabra clave (stopword adicional)
    assert "another" not in palabras


def test_extraer_palabras_clave_respeta_top_n():
    texto = "python python python java java javascript javascript javascript javascript rust"
    resultado = extraer_palabras_clave(texto, top_n=2)
    assert len(resultado) == 2
    assert resultado[0][0] == "javascript"
