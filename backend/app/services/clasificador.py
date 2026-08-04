from fastapi import HTTPException, status
from app.schemas.contenido import ContenidoEntrada, ContenidoSalida
from app.ml.loader import cargar_modelo

modelo = cargar_modelo()


def clasificar_contenido(entrada: ContenidoEntrada) -> ContenidoSalida:
    if modelo is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="El modelo de clasificación aún no está disponible. Intenta más tarde.",
        )

    return ContenidoSalida(
        categoria="Backend",
        probabilidad=0.87,
        informacion_adicional=["Python", "FastAPI", "API REST"],
    )