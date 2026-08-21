"""Pruebas de cleaning.limpiar_texto — deben reflejar exactamente el
preprocesamiento del notebook `limpieza_y_eda_techmind_v2.ipynb`, que
produjo el dataset con el que se entrenó el modelo v2.

Si alguna de estas pruebas falla, el texto que recibe el modelo en
producción dejó de parecerse al que vio al entrenarse."""

from src.cleaning import limpiar_texto


def test_limpiar_texto_conserva_terminos_tecnicos_con_simbolos():
    # El motivo de conservar + # . _ - / : son los términos con mayor
    # poder discriminante y una limpieza genérica los destruye
    # (`C++` y `C#` quedarían vacíos, `CI/CD` desaparecería).
    assert limpiar_texto("C++") == "C++"
    assert limpiar_texto("C#") == "C#"
    assert limpiar_texto("CI/CD") == "CI/CD"
    assert limpiar_texto("TCP/IP") == "TCP/IP"
    assert limpiar_texto("node.js") == "node.js"
    assert limpiar_texto(".NET") == ".NET"
    assert limpiar_texto("front-end") == "front-end"


def test_limpiar_texto_conserva_digitos_de_terminos_tecnicos():
    # HTML5, ES6 o Python 3 pierden su significado sin el número.
    resultado = limpiar_texto("HTML5 y ES6 sobre Python 3")
    assert "HTML5" in resultado
    assert "ES6" in resultado
    assert "3" in resultado


def test_limpiar_texto_elimina_urls():
    resultado = limpiar_texto("Revisa https://ejemplo.com/docs para más info")
    assert "https" not in resultado
    assert "ejemplo" not in resultado
    assert "info" in resultado


def test_limpiar_texto_elimina_encabezado_de_publicacion():
    # Los artículos de Medium arrastran una línea "Published ...:" que
    # no aporta señal técnica.
    assert limpiar_texto("Published First: https://medium.com/x") == ""


def test_limpiar_texto_normaliza_saltos_de_linea_y_espacios():
    resultado = limpiar_texto("primera línea\nsegunda\t\tlínea\r\ntercera")
    assert "\n" not in resultado
    assert "  " not in resultado
    assert resultado == "primera línea segunda línea tercera"


def test_limpiar_texto_colapsa_caracteres_repetidos():
    assert limpiar_texto("looool") == "lool"
    assert limpiar_texto("genial???") == "genial?" or limpiar_texto("genial???") == "genial"


def test_limpiar_texto_corrige_erratas_frecuentes():
    resultado = limpiar_texto("teh error al recieve el dato")
    assert "the" in resultado
    assert "receive" in resultado
    assert "teh" not in resultado


def test_limpiar_texto_conserva_acentos_en_espanol():
    # Los acentos SÍ deben conservarse: el vocabulario del vectorizador
    # se entrenó con acentos, así que eliminarlos haría que los términos
    # en español dejen de coincidir con lo aprendido.
    resultado = limpiar_texto("Cómo optimizar una consulta que tarda mucho")
    palabras = resultado.split()
    assert "Cómo" in palabras
    assert "optimizar" in palabras


def test_limpiar_texto_conserva_enie_y_dieresis():
    resultado = limpiar_texto("Diseño de esquemas con pingüino como ejemplo")
    palabras = resultado.split()
    assert "Diseño" in palabras
    assert "pingüino" in palabras


def test_limpiar_texto_no_pasa_a_minusculas():
    # El TfidfVectorizer ya normaliza a minúsculas por su cuenta; hacerlo
    # aquí además sería redundante y se apartaría del entrenamiento.
    assert limpiar_texto("Docker") == "Docker"


def test_limpiar_texto_input_no_string_retorna_vacio():
    assert limpiar_texto(None) == ""
    assert limpiar_texto(123) == ""


def test_limpiar_texto_texto_vacio_retorna_vacio():
    assert limpiar_texto("") == ""
    assert limpiar_texto("     ") == ""
