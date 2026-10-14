
"""Modelos de validación para las solicitudes de análisis."""

from typing import Literal

from pydantic import BaseModel, Field


class TextAnalysisRequest(BaseModel):
    """Solicitud de análisis de texto."""

    text: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Texto que se desea analizar.",
    )

    operation: Literal[
        "summary",
        "sentiment",
        "keywords",
        "full",
    ] = Field(
        default="full",
        description="Tipo de análisis solicitado.",
    )


class TextAnalysisResponse(BaseModel):
    """Respuesta estructurada del análisis."""

    operation: str
    character_count: int
    word_count: int
    sentence_count: int
    keywords: list[str]
    sentiment: str
    summary: str
    skill_used: str
