"""
Pruebas del módulo de preprocesamiento.
"""

from src.preprocessing import tokenizar, eliminar_stopwords, lematizar, limpiar_texto


def test_limpiar_texto_minusculas_y_sin_puntuacion():
    resultado = limpiar_texto("Custom Extractor with C++ and JS! See https://x.com/docs v2.0")
    assert resultado == "custom extractor with c and js see docs"


def test_limpiar_texto_filtra_tokens_cortos_salvo_terminos_tecnicos():
    # 'go' se conserva (está en TERMINOS_CORTOS), 'a' se filtra por ser <=2
    resultado = limpiar_texto("a go to the store")
    assert "go" in resultado.split()
    assert "a" not in resultado.split()


def test_limpiar_texto_input_no_string_retorna_vacio():
    assert limpiar_texto(None) == ""
    assert limpiar_texto(123) == ""


def test_tokenizar_divide_texto_en_palabras():
    tokens = tokenizar("hola mundo react")
    assert tokens == ["hola", "mundo", "react"]


def test_eliminar_stopwords_quita_palabras_vacias():
    tokens = ["this", "is", "a", "custom", "extractor"]
    resultado = eliminar_stopwords(tokens)
    assert "this" not in resultado
    assert "is" not in resultado
    assert "custom" in resultado
    assert "extractor" in resultado


def test_lematizar_reduce_a_forma_base():
    tokens = ["extractors", "running", "databases"]
    resultado = lematizar(tokens)
    assert resultado == ["extractor", "running", "database"]
