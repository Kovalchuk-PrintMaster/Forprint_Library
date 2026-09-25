from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml
from forprint_library.catalog.loader import load_all_component_catalogs, load_seed
from forprint_library.catalog.validation import (
    CatalogValidationError,
    collect_seed_items,
    find_duplicate_aliases,
    validate_catalog_seed,
    validate_component_catalog,
    validate_unique_item_ids,
)
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]

SCHEMA_FILES: dict[str, str] = {
    "seed": "schemas/catalog_seed.schema.yaml",
    "materials": "schemas/material.schema.yaml",
    "product_families": "schemas/product_family.schema.yaml",
    "operations": "schemas/operation.schema.yaml",
    "print_modes": "schemas/print_mode.schema.yaml",
    "finishing_options": "schemas/finishing_option.schema.yaml",
}


def read_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML must contain a mapping: {path}")
    return data


def validate_with_schema(instance_path: Path, schema_path: Path) -> None:
    instance = read_yaml(instance_path)
    schema = read_yaml(schema_path)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(instance)


def check_seed() -> None:
    seed = load_seed()
    validate_catalog_seed(seed)
    validate_with_schema(
        ROOT / "catalog" / "seeds" / "catalog_seed_v0_1.yaml",
        ROOT / "schemas" / "catalog_seed.schema.yaml",
    )


def check_schemas() -> None:
    for relative_path in SCHEMA_FILES.values():
        schema = read_yaml(ROOT / relative_path)
        Draft202012Validator.check_schema(schema)


def check_component_files() -> None:
    catalogs = load_all_component_catalogs()
    schema_by_section = {
        "materials": "material.schema.yaml",
        "product_families": "product_family.schema.yaml",
        "operations": "operation.schema.yaml",
        "print_modes": "print_mode.schema.yaml",
        "finishing_options": "finishing_option.schema.yaml",
    }

    for section, catalog in catalogs.items():
        validate_component_catalog(section, catalog)
        validate_with_schema(
            ROOT / "catalog" / f"{section}.yaml",
            ROOT / "schemas" / schema_by_section[section],
        )


def check_uniqueness() -> None:
    seed = load_seed()
    validate_unique_item_ids(collect_seed_items(seed))


def check_aliases() -> None:
    seed = load_seed()
    items = collect_seed_items(seed)
    duplicates = find_duplicate_aliases(items)
    if duplicates:
        raise CatalogValidationError(f"Duplicate aliases detected: {duplicates}")


def check_example() -> None:
    validate_with_schema(
        ROOT / "examples" / "catalog_seed_v0_1.example.yaml",
        ROOT / "schemas" / "catalog_seed.schema.yaml",
    )


def check_all() -> None:
    check_seed()
    check_schemas()
    check_component_files()
    check_uniqueness()
    check_aliases()
    check_example()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        choices=[
            "all",
            "seed",
            "schemas",
            "files",
            "uniqueness",
            "aliases",
            "example",
        ],
        default="all",
    )
    args = parser.parse_args()

    checks = {
        "all": check_all,
        "seed": check_seed,
        "schemas": check_schemas,
        "files": check_component_files,
        "uniqueness": check_uniqueness,
        "aliases": check_aliases,
        "example": check_example,
    }

    try:
        checks[args.check]()
    except Exception as exc:  # noqa: BLE001
        print(f"FAILED: catalog validation check '{args.check}' failed: {exc}")
        return 1

    print(f"OK: catalog validation check '{args.check}' passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())