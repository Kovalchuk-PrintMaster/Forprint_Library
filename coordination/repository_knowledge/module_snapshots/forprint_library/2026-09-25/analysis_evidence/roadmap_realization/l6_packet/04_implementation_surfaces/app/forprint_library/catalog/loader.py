from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from forprint_library.catalog.models import COMPONENT_CATALOG_FILES

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_SEED_PATH = PROJECT_ROOT / "catalog" / "seeds" / "catalog_seed_v0_1.yaml"


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML file must contain a mapping: {path}")

    return data


def load_seed(path: Path | None = None) -> dict[str, Any]:
    return load_yaml(path or DEFAULT_SEED_PATH)


def load_component_catalog(section: str, project_root: Path | None = None) -> dict[str, Any]:
    root = project_root or PROJECT_ROOT
    relative_path = COMPONENT_CATALOG_FILES[section]
    return load_yaml(root / relative_path)


def load_all_component_catalogs(project_root: Path | None = None) -> dict[str, dict[str, Any]]:
    return {
        section: load_component_catalog(section, project_root=project_root)
        for section in COMPONENT_CATALOG_FILES
    }