
"""Configuración general de SkillAPI."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

APP_NAME = "SkillAPI"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = (
    "API de análisis de texto con comportamiento personalizado "
    "mediante Agent Skills."
)

SKILLS_DIR = PROJECT_ROOT / ".github" / "skills"
DEFAULT_SKILL = "text-analysis"
