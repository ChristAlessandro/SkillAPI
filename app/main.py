
"""Punto de entrada de la aplicación SkillAPI."""

from fastapi import FastAPI

from app.api.routes import router
from app.core.config import APP_DESCRIPTION, APP_NAME, APP_VERSION

app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
)

app.include_router(router, prefix="/api/v1")


@app.get("/", tags=["Sistema"])
def root() -> dict[str, str]:
    """Presenta la información básica de la API."""
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "docs": "/docs",
    }
