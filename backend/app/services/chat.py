import logging

from openai import OpenAI
from app.core.config import settings
from app.schemas.contenido import ContenidoEntrada
from app.services.clasificador import clasificar_contenido

logger = logging.getLogger(__name__)

cliente = OpenAI(
    api_key=settings.deepseek_api_key,
    base_url="https://api.deepseek.com",
)


def construir_prompt(texto_usuario: str, categoria: str, probabilidad: float, palabras_clave: list[str]) -> str:
    contexto = (
        f"El siguiente contenido técnico fue clasificado por nuestro modelo como '{categoria}' "
        f"con una confianza de {probabilidad:.0%}. "
        f"Las palabras clave detectadas son: {', '.join(palabras_clave)}.\n\n"
        f"Contenido del usuario: \"{texto_usuario}\"\n\n"
        f"Como asistente de TechMind AI, explica este contenido de forma clara y natural, "
        f"usando la categoría y palabras clave como contexto, sin mencionar explícitamente "
        f"que provienen de un modelo de clasificación. Varía la forma de comenzar tu respuesta "
        f"en cada mensaje, evitando repetir siempre la misma expresión de apertura (como "
        f"'¡Claro!' o '¡Excelente pregunta!'); a veces puedes ir directo al grano, otras veces "
        f"usar una frase distinta, según lo que sienta más natural para el contexto."
    )
    return contexto


def generar_respuesta(mensajes: list[dict]) -> str:
    try:
        respuesta = cliente.chat.completions.create(
            model="deepseek-chat",
            messages=mensajes,
        )
        return respuesta.choices[0].message.content
    except Exception as e:
        logger.error(f"Fallo al consultar DeepSeek: {e}")
        return "No pude generar una explicación en este momento, pero aquí está la clasificación."


def responder_chat(texto_usuario: str, historial: list) -> str:
    entrada = ContenidoEntrada(titulo="Consulta de chat", texto=texto_usuario)
    resultado = clasificar_contenido(entrada)

    prompt = construir_prompt(
        texto_usuario=texto_usuario,
        categoria=resultado.categoria,
        probabilidad=resultado.probabilidad,
        palabras_clave=resultado.informacion_adicional,
    )

    mensajes = [{"role": m.rol, "content": m.contenido} for m in historial]
    mensajes.append({"role": "user", "content": prompt})

    return generar_respuesta(mensajes)