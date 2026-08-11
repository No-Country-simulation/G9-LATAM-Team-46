"""Pruebas de cleaning.limpiar_texto — deben reflejar exactamente el
comportamiento de la función limpiar() del notebook de modelado v2."""

from src.cleaning import limpiar_texto


def test_limpiar_texto_minusculas_y_sin_puntuacion():
    resultado = limpiar_texto("Building a Drag-and-Drop UI with React!")
    assert resultado == "building drag and drop with react"


def test_limpiar_texto_elimina_urls():
    resultado = limpiar_texto("Revisa https://ejemplo.com/docs para más info")
    assert "https" not in resultado
    assert "ejemplo" not in resultado


def test_limpiar_texto_elimina_numeros():
    resultado = limpiar_texto("Python 3.12 y Node 20")
    assert not any(caracter.isdigit() for caracter in resultado)


def test_limpiar_texto_filtra_palabras_de_dos_letras_o_menos():
    # A diferencia de la v1, aquí NO hay excepción para términos cortos
    # técnicos (ej. "js", "ai") — se filtran igual que cualquier palabra.
    resultado = limpiar_texto("uso de js y ai en el backend")
    palabras = resultado.split()
    assert "js" not in palabras
    assert "ai" not in palabras
    assert "backend" in palabras


def test_limpiar_texto_conserva_acentos_en_espanol():
    # Sin `or`: los acentos SÍ deben conservarse. El vocabulario del
    # vectorizador v2 se entrenó con acentos, así que normalizarlos o
    # eliminarlos (ej. con unicodedata.normalize) haría que términos en
    # español dejen de coincidir con el vocabulario aprendido.
    resultado = limpiar_texto("Cómo optimizar una consulta que tarda mucho")
    palabras = resultado.split()
    assert "cómo" in palabras
    assert "optimizar" in palabras


def test_limpiar_texto_conserva_enie_y_dieresis():
    resultado = limpiar_texto("Diseño de esquemas con pingüino como ejemplo")
    palabras = resultado.split()
    assert "diseño" in palabras
    assert "pingüino" in palabras


def test_limpiar_texto_input_no_string_retorna_vacio():
    assert limpiar_texto(None) == ""
    assert limpiar_texto(123) == ""


def test_limpiar_texto_solo_simbolos_retorna_vacio():
    assert limpiar_texto("!!! *** ###") == ""
