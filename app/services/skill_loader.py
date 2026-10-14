
"""Carga las instrucciones y los recursos de las Agent Skills."""

import json
import re
from pathlib import Path
from typing import Any

from app.core.config import SKILLS_DIR


def load_skill(name: str) -> dict[str, Any]:
    """Carga el SKILL.md y sus recursos JSON."""

    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise ValueError("Nombre de skill no válido.")

    skill_dir = (SKILLS_DIR / name).resolve()

    try:
        skill_dir.relative_to(SKILLS_DIR.resolve())
    except ValueError as error:
        raise ValueError("Ruta de skill no permitida.") from error

    skill_file = skill_dir / "SKILL.md"
    rules_file = skill_dir / "references" / "processing_rules.json"

    if not skill_file.is_file():
        raise FileNotFoundError(
            f"No se encontró SKILL.md para '{name}'."
        )

    if not rules_file.is_file():
        raise FileNotFoundError(
            f"No se encontraron los recursos de '{name}'."
        )

    instructions = skill_file.read_text(encoding="utf-8").strip()

    if not instructions:
        raise ValueError(f"La skill '{name}' está vacía.")

    rules = json.loads(rules_file.read_text(encoding="utf-8"))

    if not isinstance(rules, dict):
        raise ValueError("Los recursos de la skill deben ser un objeto JSON.")

    return {
        "name": name,
        "instructions": instructions,
        "rules": rules,
    }


def list_skills() -> list[str]:
    """Lista las skills que tienen un archivo SKILL.md."""

    if not SKILLS_DIR.is_dir():
        return []

    return sorted(
        directory.name
        for directory in SKILLS_DIR.iterdir()
        if directory.is_dir()
        and (directory / "SKILL.md").is_file()
    )
