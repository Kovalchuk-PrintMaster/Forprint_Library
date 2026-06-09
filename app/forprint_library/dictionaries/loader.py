from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from forprint_library.dictionaries.models import (
    DICTIONARY_FILES,
    DICTIONARY_GROUPS,
    SHARED_DICTIONARY_FILE,
)

PROJECT_ROOT = Path(__file__).resolve().parents[3]


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML file must contain a mapping: {path}")

    return data


def load_shared_dictionary(project_root: Path | None = None) -> dict[str, Any]:
    root = project_root or PROJECT_ROOT
    return load_yaml(root / SHARED_DICTIONARY_FILE)


def load_dictionary(group_name: str, project_root: Path | None = None) -> dict[str, Any]:
    if group_name not in DICTIONARY_FILES:
        known_groups = ", ".join(DICTIONARY_GROUPS)
        raise KeyError(f"Unknown dictionary group: {group_name}. Known groups: {known_groups}")

    root = project_root or PROJECT_ROOT
    return load_yaml(root / DICTIONARY_FILES[group_name])


def load_all_dictionaries(project_root: Path | None = None) -> dict[str, dict[str, Any]]:
    return {
        group_name: load_dictionary(group_name, project_root=project_root)
        for group_name in DICTIONARY_GROUPS
    }


def list_dictionary_groups() -> list[str]:
    return list(DICTIONARY_GROUPS)