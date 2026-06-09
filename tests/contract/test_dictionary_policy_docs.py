from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_DICTIONARY_DOCS = [
    "docs/architecture/shared_operational_dictionary_policy.md",
    "docs/architecture/status_dictionary_policy.md",
    "docs/architecture/source_system_dictionary_policy.md",
    "docs/architecture/entity_type_dictionary_policy.md",
    "docs/architecture/unit_dictionary_policy.md",
    "docs/architecture/dictionary_consumption_policy.md",
    "docs/architecture/dictionary_versioning_policy.md",
]


def read_lower(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8").casefold()


def test_required_dictionary_policy_docs_exist() -> None:
    for relative_path in REQUIRED_DICTIONARY_DOCS:
        assert (ROOT / relative_path).exists(), relative_path


def test_shared_operational_dictionary_policy_confirms_library_ownership() -> None:
    text = read_lower("docs/architecture/shared_operational_dictionary_policy.md")

    assert "library owns canonical shared operational dictionary definitions" in text
    assert "other modules may consume" in text
    assert "must not become independent permanent dictionary authorities" in text


def test_status_dictionary_policy_mentions_consuming_modules() -> None:
    text = read_lower("docs/architecture/status_dictionary_policy.md")

    for phrase in [
        "operational registry",
        "calculator engine",
        "telegram bot",
        "crm",
        "accounting registry",
    ]:
        assert phrase in text


def test_source_system_policy_mentions_required_sources() -> None:
    text = read_lower("docs/architecture/source_system_dictionary_policy.md")

    for phrase in [
        "forprint_operational_registry",
        "forprint_library",
        "calculator_engine",
        "accounting_registry_service",
        "telegram_bot",
        "one_c_bas",
        "manual_entry",
        "unknown",
    ]:
        assert phrase in text


def test_entity_type_policy_mentions_required_entities() -> None:
    text = read_lower("docs/architecture/entity_type_dictionary_policy.md")

    for phrase in [
        "client_account",
        "order",
        "order_line",
        "material_requirement",
        "payment_projection",
        "workflow_stage",
    ]:
        assert phrase in text


def test_unit_policy_marks_not_final_inventory_unit_system() -> None:
    text = read_lower("docs/architecture/unit_dictionary_policy.md")

    assert "not_final_inventory_unit_system" in text
    assert "not a final inventory" in text


def test_dictionary_consumption_policy_prevents_local_id_invention() -> None:
    text = read_lower("docs/architecture/dictionary_consumption_policy.md")

    assert "should reference canonical ids" in text
    assert "not invent new internal ids" in text


def test_dictionary_versioning_policy_mentions_deprecation() -> None:
    text = read_lower("docs/architecture/dictionary_versioning_policy.md")

    assert "deprecated values must remain readable" in text
    assert "historical records" in text


def test_library_boundary_prevents_operational_records() -> None:
    text = read_lower("docs/architecture/shared_operational_dictionary_policy.md")

    for phrase in [
        "real operational orders",
        "real clients",
        "real payments",
        "real material stock",
        "calculator formulas",
        "telegram runtime",
        "crm dashboard",
        "1c synchronization",
    ]:
        assert phrase in text