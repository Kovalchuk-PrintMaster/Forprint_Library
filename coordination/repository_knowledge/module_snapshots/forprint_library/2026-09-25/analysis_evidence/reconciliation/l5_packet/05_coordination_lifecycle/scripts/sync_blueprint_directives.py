from __future__ import annotations

import hashlib
import shutil
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
BLUEPRINT_SOURCE = ROOT / "coordination" / "blueprint_source.yaml"
RECEIVED_DIR = ROOT / "coordination" / "prompts" / "received"
PROMPTS_INDEX = ROOT / "coordination" / "prompts" / "index.yaml"


def read_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )


def stable_id_from_path(path: Path) -> str:
    digest = hashlib.sha1(str(path).encode("utf-8")).hexdigest()[:10]
    return f"blueprint_directive_{digest}"


def load_source() -> tuple[Path, Path]:
    data = read_yaml(BLUEPRINT_SOURCE)
    source = data.get("blueprint_source", {})
    blueprint_root = Path(source.get("blueprint_root", ""))
    if not blueprint_root.is_absolute():
        blueprint_root = (ROOT / blueprint_root).resolve()

    module_index = blueprint_root / source.get(
        "module_directives_index",
        "coordination/directives/modules/forprint_library/index.yaml",
    )
    return blueprint_root, module_index


def extract_active_directives(index_data: dict[str, Any]) -> list[Any]:
    module_directives = index_data.get("module_directives")
    if isinstance(module_directives, dict):
        active = module_directives.get("active", [])
        if isinstance(active, list):
            return active

    for fallback_key in ("directives", "prompts"):
        fallback = index_data.get(fallback_key)
        if isinstance(fallback, list):
            return fallback

    return []


def resolve_directive_path(blueprint_root: Path, module_index: Path, item: Any) -> Path | None:
    if isinstance(item, str):
        raw = item
    elif isinstance(item, dict):
        raw = (
            item.get("path")
            or item.get("file")
            or item.get("prompt_path")
            or item.get("directive_path")
        )
    else:
        return None

    if not raw:
        return None

    path = Path(str(raw))
    if path.is_absolute():
        return path

    candidate_from_index = (module_index.parent / path).resolve()
    if candidate_from_index.exists():
        return candidate_from_index

    return (blueprint_root / path).resolve()


def main() -> int:
    if not BLUEPRINT_SOURCE.exists():
        print("FAILED: coordination/blueprint_source.yaml is missing.")
        return 1

    blueprint_root, module_index = load_source()

    if not module_index.exists():
        print(f"WARN: module directive index is missing/deferred: {module_index}")
        return 0

    index_data = read_yaml(module_index)
    active_directives = extract_active_directives(index_data)

    RECEIVED_DIR.mkdir(parents=True, exist_ok=True)
    local_index = read_yaml(PROMPTS_INDEX)
    existing_items = local_index.get("items", [])
    if not isinstance(existing_items, list):
        existing_items = []

    existing_sources = {
        item.get("source_path")
        for item in existing_items
        if isinstance(item, dict) and item.get("source_path")
    }

    imported = 0
    for directive in active_directives:
        source_path = resolve_directive_path(blueprint_root, module_index, directive)
        if source_path is None or not source_path.exists():
            print(f"WARN: cannot resolve directive: {directive}")
            continue

        source_key = str(source_path)
        if source_key in existing_sources:
            print(f"SKIP: already imported: {source_path}")
            continue

        directive_id = stable_id_from_path(source_path)
        target_name = f"{directive_id}__{source_path.name}"
        target_path = RECEIVED_DIR / target_name
        shutil.copy2(source_path, target_path)

        existing_items.append(
            {
                "id": directive_id,
                "source_path": source_key,
                "local_path": str(target_path.relative_to(ROOT)),
                "status": "imported",
            }
        )
        imported += 1
        print(f"IMPORTED: {source_path} -> {target_path}")

    local_index = {
        "module_id": "forprint_library",
        "index_type": "received_prompts",
        "items": existing_items,
    }
    write_yaml(PROMPTS_INDEX, local_index)

    print(f"OK: imported {imported} directive(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())