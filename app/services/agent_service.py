
"""Servicio de análisis de texto guiado por una skill personalizada."""

import re
import unicodedata
from collections import Counter
from typing import Any

from app.core.config import DEFAULT_SKILL
from app.schemas.text import TextAnalysisRequest, TextAnalysisResponse
from app.services.skill_loader import load_skill


def normalizar(texto: str) -> str:
    """Normaliza el texto para comparar palabras sin distinguir mayúsculas."""
    texto = unicodedata.normalize("NFKD", texto.casefold())
    return "".join(
        caracter
        for caracter in texto
        if not unicodedata.combining(caracter)
    )


def procesar_texto(
    solicitud: TextAnalysisRequest,
) -> TextAnalysisResponse:
    """Aplica las reglas de la skill y devuelve un análisis reproducible."""
    skill = load_skill(DEFAULT_SKILL)
    reglas: dict[str, Any] = skill["rules"]

    texto = solicitud.text.strip()
    palabras_originales = re.findall(r"\b[\wáéíóúüñÁÉÍÓÚÜÑ]+\b", texto)
    palabras_normalizadas = [normalizar(p) for p in palabras_originales]

    oraciones = [
        parte.strip()
        for parte in re.split(r"(?<=[.!?])\s+", texto)
        if parte.strip()
    ]

    stopwords = {
        normalizar(palabra)
        for palabra in reglas.get("stopwords", [])
    }

    frecuencias = Counter(
        palabra
        for palabra in palabras_normalizadas
        if palabra not in stopwords and len(palabra) > 2
    )

    max_keywords = max(0, int(reglas.get("max_keywords", 5)))
    keywords = [
        palabra
        for palabra, _ in frecuencias.most_common(max_keywords)
    ]

    positivas = {
        normalizar(palabra)
        for palabra in reglas.get("positive_words", [])
    }
    negativas = {
        normalizar(palabra)
        for palabra in reglas.get("negative_words", [])
    }

    puntaje = sum(p in positivas for p in palabras_normalizadas)
    puntaje -= sum(p in negativas for p in palabras_normalizadas)

    if puntaje > 0:
        sentimiento = "positivo"
    elif puntaje < 0:
        sentimiento = "negativo"
    else:
        sentimiento = "neutral"

    max_oraciones = max(
        1,
        int(reglas.get("max_summary_sentences", 2)),
    )
    resumen = " ".join(oraciones[:max_oraciones])

    operacion = solicitud.operation

    return TextAnalysisResponse(
        operation=operacion,
        character_count=len(texto),
        word_count=len(palabras_originales),
        sentence_count=len(oraciones),
        keywords=keywords if operacion in {"keywords", "full"} else [],
        sentiment=sentimiento if operacion in {"sentiment", "full"} else "no_calculado",
        summary=resumen if operacion in {"summary", "full"} else "",
        skill_used=skill["name"],
    )
