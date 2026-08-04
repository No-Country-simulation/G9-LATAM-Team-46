from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.routers import health, contenido

app = FastAPI(title=settings.app_name, version=settings.app_version)

app.include_router(health.router)
app.include_router(contenido.router)


@app.exception_handler(Exception)
async def manejador_errores_generales(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Ocurrió un error interno inesperado. El equipo ya fue notificado."},
    )