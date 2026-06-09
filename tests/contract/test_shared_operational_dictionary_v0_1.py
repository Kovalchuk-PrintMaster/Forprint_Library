from __future__ import annotations

from pathlib import Path

import yaml
from forprint_library.dictionaries.loader import (
    load_all_dictionaries,
    load_dictionary,
    load_shared_dictionary,
)
from forprint_library.dictionaries.models import (
    DICTIONARY_GROUPS,
    EXPECTED_SHARED_METADATA,
    REQUIRED_DICTIONARY_ENTRY_FIELDS,
)
from forprint_library.dictionaries.validation import (
    collect_shared_dictionary_entries,
    find_duplicate_aliases,
    validate_dictionary_group,
    validate_shared_dictionary,
)
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]


def test_shared_dictionary_loads() -> None:
    shared_dictionary = load_shared_dictionary()

    validate_shared_dictionary(shared_dictionary)
    assert shared_dictionary["metadata"]["id"] == "shared_operational_dictionary_v0_1"


def test_all_dictionary_groups_exist() -> None:
    shared_dictionary = load_shared_dictionary()
    groups = shared_dictionary["dictionary_groups"]

    for group_name in DICTIONARY_GROUPS:
        assert group_name in groups
        assert isinstance(groups[group_name], list)
        assert groups[group_name]


def test_group_dictionary_files_load_and_validate() -> None:
    dictionaries = load_all_dictionaries()

    for group_name in DICTIONARY_GROUPS:
        dictionary = dictionaries[group_name]
        validate_dictionary_group(group_name, dictionary)
        assert dictionary["dictionary_group"] == group_name
        assert dictionary["entries"]


def test_all_entry_ids_are_unique_within_group() -> None:
    dictionaries = load_all_dictionaries()

    for group_name, dictionary in dictionaries.items():
        ids = [entry["id"] for entry in dictionary["entries"]]
        assert len(ids) == len(set(ids)), group_name


def test_all_entries_have_required_fields() -> None:
    entries = collect_shared_dictionary_entries(load_shared_dictionary())

    for entry in entries:
        for field in REQUIRED_DICTIONARY_ENTRY_FIELDS:
            assert field in entry, f"{entry.get('id')} missing {field}"


def test_aliases_are_lists() -> None:
    entries = collect_shared_dictionary_entries(load_shared_dictionary())

    for entry in entries:
        assert isinstance(entry["aliases"], list), entry["id"]


def test_duplicate_aliases_are_not_present_within_groups() -> None:
    entries = collect_shared_dictionary_entries(load_shared_dictionary())

    assert find_duplicate_aliases(entries) == {}


def test_shared_metadata_has_required_status_terms() -> None:
    metadata = load_shared_dictionary()["metadata"]

    for key, expected_value in EXPECTED_SHARED_METADATA.items():
        assert metadata[key] == expected_value

    assert metadata["unit_dictionary_status"] == "not_final_inventory_unit_system"


def test_source_system_contains_required_values() -> None:
    entries = load_dictionary("source_system")["entries"]
    ids = {entry["id"] for entry in entries}

    for required_id in [
        "forprint_operational_registry",
        "calculator_engine",
        "forprint_library",
        "accounting_registry_service",
        "telegram_bot",
        "one_c_bas",
    ]:
        assert required_id in ids


def test_entity_type_contains_required_values() -> None:
    entries = load_dictionary("entity_type")["entries"]
    ids = {entry["id"] for entry in entries}

    for required_id in [
        "order",
        "order_line",
        "client_account",
        "workflow_stage",
        "payment_projection",
        "material_requirement",
    ]:
        assert required_id in ids


def test_order_status_contains_required_values() -> None:
    entries = load_dictionary("order_status")["entries"]
    ids = {entry["id"] for entry in entries}

    for required_id in [
        "draft",
        "confirmed",
        "completed",
        "cancelled",
        "manual_review_required",
    ]:
        assert required_id in ids


def test_payment_status_contains_required_values() -> None:
    entries = load_dictionary("payment_status")["entries"]
    ids = {entry["id"] for entry in entries}

    for required_id in [
        "unpaid",
        "partially_paid",
        "overdue",
        "paid_reference_confirmed",
    ]:
        assert required_id in ids


def test_workflow_stage_status_contains_required_values() -> None:
    entries = load_dictionary("workflow_stage_status")["entries"]
    ids = {entry["id"] for entry in entries}

    for required_id in [
        "waiting_external_contractor",
        "late",
        "manual_review_required",
    ]:
        assert required_id in ids


def test_material_requirement_status_contains_required_values() -> None:
    entries = load_dictionary("material_requirement_status")["entries"]
    ids = {entry["id"] for entry in entries}

    assert "warehouse_reference_pending" in ids


def test_alert_severity_contains_required_values() -> None:
    entries = load_dictionary("alert_severity")["entries"]
    ids = {entry["id"] for entry in entries}

    for required_id in ["warning", "high", "critical"]:
        assert required_id in ids


def test_unit_contains_required_values() -> None:
    entries = load_dictionary("unit")["entries"]
    ids = {entry["id"] for entry in entries}

    for required_id in ["pcs", "m2", "kg", "service", "unknown"]:
        assert required_id in ids


def test_shared_dictionary_schema_validates_shared_dictionary() -> None:
    instance = yaml.safe_load(
        (ROOT / "dictionaries/shared_operational_dictionary_v0_1.yaml").read_text(
            encoding="utf-8"
        )
    )
    schema = yaml.safe_load(
        (ROOT / "schemas/shared_operational_dictionary.schema.yaml").read_text(
            encoding="utf-8"
        )
    )

    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(instance)


def test_dictionary_schema_files_are_valid_json_schemas() -> None:
    schema_paths = [
        ROOT / "schemas/dictionary_entry.schema.yaml",
        ROOT / "schemas/shared_operational_dictionary.schema.yaml",
    ]

    for schema_path in schema_paths:
        schema = yaml.safe_load(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)


def test_no_real_operational_records_are_created() -> None:
    forbidden_paths = [
        ROOT / "orders",
        ROOT / "clients",
        ROOT / "payments",
        ROOT / "warehouse_stock",
        ROOT / "production_runtime",
    ]

    for path in forbidden_paths:
        assert not path.exists(), path