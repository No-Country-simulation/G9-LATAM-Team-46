import re


def limpiar(texto: str) -> str:
    if not isinstance(texto, str):
        return ""
    texto = texto.lower()
    texto = re.sub(r'[\n\t\r]+', ' ', texto)
    texto = re.sub(r'http\S+|www\S+|https\S+', '', texto, flags=re.MULTILINE)
    texto = re.sub(r'\d+', ' ', texto)
    texto = re.sub(r'[^áéíóúüñA-Za-z0-9\s]', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto)
    palabras = [p for p in texto.split() if len(p) > 2]
    return " ".join(palabras).strip()
