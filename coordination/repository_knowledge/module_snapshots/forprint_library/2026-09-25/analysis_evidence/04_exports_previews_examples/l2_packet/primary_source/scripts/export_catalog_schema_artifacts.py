from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = ROOT / "schemas"
EXAMPLES_DIR = ROOT / "examples"
SEED_PATH = ROOT / "catalog" / "seeds" / "catalog_seed_v0_1.yaml"

COMPONENT_SCHEMAS: dict[str, tuple[str, str]] = {
    "material.schema.yaml": ("ForPrint Material Catalog", "materials"),
    "product_family.schema.yaml": ("ForPrint Product Family Catalog", "product_families"),
    "operation.schema.yaml": ("ForPrint Operation Catalog", "operations"),
    "print_mode.schema.yaml": ("ForPrint Print Mode Catalog", "print_modes"),
    "finishing_option.schema.yaml": (
        "ForPrint Finishing Option Catalog",
        "finishing_options",
    ),
}


def catalog_item_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "required": [
            "id",
            "name_uk",
            "name_en",
            "aliases",
            "status",
            "version",
            "owner_module",
            "schema_status",
            "notes",
        ],
        "properties": {
            "id": {"type": "string", "pattern": "^[a-z0-9_]+$"},
            "name_uk": {"type": "string", "minLength": 1},
            "name_en": {"type": "string", "minLength": 1},
            "aliases": {
                "type": "array",
                "minItems": 1,
                "items": {"type": "string", "minLength": 1},
            },
            "status": {
                "enum": [
                    "draft",
                    "active",
                    "deprecated",
                    "experimental",
                ]
            },
            "version": {"type": "string"},
            "owner_module": {"const": "forprint_library"},
            "schema_status": {"const": "unstable_v0_1"},
            "notes": {"type": "string"},
        },
        "additionalProperties": True,
    }


def metadata_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "required": [
            "id",
            "version",
            "catalog_status",
            "schema_status",
            "usage",
            "contract_status",
            "owner_module",
        ],
        "properties": {
            "id": {"type": "string"},
            "name": {"type": "string"},
            "version": {"type": "string"},
            "catalog_status": {"const": "draft_canonical_seed"},
            "schema_status": {"const": "unstable_v0_1"},
            "usage": {"const": "allowed_for_projection_use"},
            "contract_status": {"const": "not_final_contract"},
            "owner_module": {"const": "forprint_library"},
            "notes": {"type": "string"},
        },
        "additionalProperties": True,
    }


def catalog_seed_schema() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "ForPrint Catalog Seed",
        "type": "object",
        "required": [
            "metadata",
            "materials",
            "product_families",
            "operations",
            "print_modes",
            "finishing_options",
        ],
        "properties": {
            "metadata": metadata_schema(),
            "materials": {
                "type": "array",
                "minItems": 1,
                "items": {"$ref": "#/$defs/catalog_item"},
            },
            "product_families": {
                "type": "array",
                "minItems": 1,
                "items": {"$ref": "#/$defs/catalog_item"},
            },
            "operations": {
                "type": "array",
                "minItems": 1,
                "items": {"$ref": "#/$defs/catalog_item"},
            },
            "print_modes": {
                "type": "array",
                "minItems": 1,
                "items": {"$ref": "#/$defs/catalog_item"},
            },
            "finishing_options": {
                "type": "array",
                "minItems": 1,
                "items": {"$ref": "#/$defs/catalog_item"},
            },
        },
        "additionalProperties": False,
        "$defs": {"catalog_item": catalog_item_schema()},
    }


def component_catalog_schema(title: str, catalog_type: str) -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": title,
        "type": "object",
        "required": [
            "catalog_type",
            "metadata",
            "items",
        ],
        "properties": {
            "catalog_type": {"const": catalog_type},
            "metadata": metadata_schema(),
            "items": {
                "type": "array",
                "minItems": 1,
                "items": catalog_item_schema(),
            },
        },
        "additionalProperties": False,
    }


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    print(f"OK: wrote {path.relative_to(ROOT)}")


def read_seed() -> dict[str, Any]:
    data = yaml.safe_load(SEED_PATH.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError("Catalog seed must be a YAML mapping.")
    return data


def export_schemas() -> None:
    write_yaml(
        SCHEMAS_DIR / "catalog_seed.schema.yaml",
        catalog_seed_schema(),
    )

    for filename, schema_config in COMPONENT_SCHEMAS.items():
        title, catalog_type = schema_config
        write_yaml(
            SCHEMAS_DIR / filename,
            component_catalog_schema(title, catalog_type),
        )


def export_example_seed() -> None:
    seed = read_seed()
    example = {
        "metadata": {
            **seed["metadata"],
            "id": "canonical_catalog_seed_v0_1_example",
            "name": "Canonical Catalog Seed v0.1 Example",
            "notes": "Example projection-safe catalog seed structure.",
        },
        "materials": [seed["materials"][0]],
        "product_families": [seed["product_families"][0]],
        "operations": [seed["operations"][0]],
        "print_modes": [seed["print_modes"][0]],
        "finishing_options": [seed["finishing_options"][0]],
    }

    write_yaml(
        EXAMPLES_DIR / "catalog_seed_v0_1.example.yaml",
        example,
    )


def main() -> int:
    export_schemas()
    export_example_seed()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())