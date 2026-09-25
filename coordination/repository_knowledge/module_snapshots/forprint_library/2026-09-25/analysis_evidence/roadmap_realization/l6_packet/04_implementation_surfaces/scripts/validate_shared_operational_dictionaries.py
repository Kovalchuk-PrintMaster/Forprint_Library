from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml
from forprint_library.dictionaries.loader import (
    load_all_dictionaries,
    load_shared_dictionary,
)
from forprint_library.dictionaries.models import DICTIONARY_GROUPS
from forprint_library.dictionaries.validation import (
    validate_dictionary_group,
    validate_shared_dictionary,
)
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def read_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML must contain a mapping: {path}")
    return data


def validate_schema_file(path: Path) -> None:
    Draft202012Validator.check_schema(read_yaml(path))


def validate_with_schema(instance_path: Path, schema_path: Path) -> None:
    instance = read_yaml(instance_path)
    schema = read_yaml(schema_path)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(instance)


def check_shared_dictionary() -> None:
    shared_dictionary = load_shared_dictionary()
    validate_shared_dictionary(shared_dictionary)
    validate_with_schema(
        ROOT / "dictionaries" / "shared_operational_dictionary_v0_1.yaml",
        ROOT / "schemas" / "shared_operational_dictionary.schema.yaml",
    )


def check_group_dictionaries() -> None:
    dictionaries = load_all_dictionaries()

    for group_name in DICTIONARY_GROUPS:
        dictionary = dictionaries[group_name]
        validate_dictionary_group(group_name, dictionary)


def check_dictionary_schemas() -> None:
    validate_schema_file(ROOT / "schemas" / "dictionary_entry.schema.yaml")
    validate_schema_file(ROOT / "schemas" / "shared_operational_dictionary.schema.yaml")


def check_required_values() -> None:
    shared_dictionary = load_shared_dictionary()
    groups = shared_dictionary["dictionary_groups"]

    required_values = {
        "source_system": {
            "forprint_operational_registry",
            "calculator_engine",
            "forprint_library",
            "accounting_registry_service",
            "telegram_bot",
            "one_c_bas",
        },
        "entity_type": {
            "order",
            "order_line",
            "client_account",
            "workflow_stage",
            "payment_projection",
            "material_requirement",
        },
        "order_status": {
            "draft",
            "confirmed",
            "completed",
            "cancelled",
            "manual_review_required",
        },
        "payment_status": {
            "unpaid",
            "partially_paid",
            "overdue",
            "paid_reference_confirmed",
        },
        "workflow_stage_status": {
            "waiting_external_contractor",
            "late",
            "manual_review_required",
        },
        "material_requirement_status": {
            "warehouse_reference_pending",
        },
        "alert_severity": {
            "warning",
            "high",
            "critical",
        },
        "unit": {
            "pcs",
            "m2",
            "kg",
            "service",
            "unknown",
        },
    }

    for group_name, expected_ids in required_values.items():
        actual_ids = {entry["id"] for entry in groups[group_name]}
        missing = sorted(expected_ids - actual_ids)
        if missing:
            raise AssertionError(f"Missing values in {group_name}: {missing}")


def check_all() -> None:
    check_shared_dictionary()
    check_group_dictionaries()
    check_dictionary_schemas()
    check_required_values()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        choices=[
            "all",
            "shared",
            "groups",
            "schemas",
            "required-values",
        ],
        default="all",
    )
    args = parser.parse_args()

    checks = {
        "all": check_all,
        "shared": check_shared_dictionary,
        "groups": check_group_dictionaries,
        "schemas": check_dictionary_schemas,
        "required-values": check_required_values,
    }

    try:
        checks[args.check]()
    except Exception as exc:
        print(f"FAILED: shared dictionary check '{args.check}' failed: {exc}")
        return 1

    print(f"OK: shared dictionary check '{args.check}' passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())