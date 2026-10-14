
"""Rutas HTTP de SkillAPI."""

from fastapi import APIRouter, HTTPException

from app.schemas.text import TextAnalysisRequest, TextAnalysisResponse
from app.services.agent_service import procesar_texto
from app.services.skill_loader import list_skills

router = APIRouter()


@router.get("/health", tags=["Sistema"])
def health_check() -> dict[str, str]:
    """Comprueba que la API está disponible."""
    return {"status": "ok", "service": "SkillAPI"}


@router.get("/skills", tags=["Skills"])
def obtener_skills() -> dict[str, list[str]]:
    """Lista las skills que tienen instrucciones disponibles."""
    return {"skills": list_skills()}


@router.post(
    "/analyze",
    response_model=TextAnalysisResponse,
    tags=["Análisis"],
)
def analizar_texto(
    solicitud: TextAnalysisRequest,
) -> TextAnalysisResponse:
    """Analiza texto utilizando las reglas de la skill configurada."""
    try:
        return procesar_texto(solicitud)
    except (FileNotFoundError, ValueError) as error:
        raise HTTPException(
            status_code=500,
            detail=f"No se pudo aplicar la skill: {error}",
        ) from error
