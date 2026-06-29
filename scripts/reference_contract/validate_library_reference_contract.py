from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]

DOC_PATH = ROOT / "docs" / "architecture" / "reference_contract_foundation.md"
EXAMPLES_PATH = (
    ROOT / "examples" / "reference_contract" / "library_reference_examples.yaml"
)
SCHEMA_PATH = ROOT / "schemas" / "reference_contract" / "library_reference.schema.yaml"

EXPECTED_REFERENCE_TYPES = {
    "product_service",
    "material",
    "operation",
    "unit",
    "template",
    "technical_card",
}

EXPECTED_STATUSES = {
    "library_reference_confirmed",
    "library_reference_pending",
    "ambiguous_manual_review_required",
    "deprecated_reference",
    "unknown",
}

EXPECTED_SOURCE_MODULES = {
    "calculator_engine",
    "forprint_operational_registry",
    "forprint_integration_gateway",
    "telegram_bot",
    "future_forprint_crm",
    "forprint_library",
}

REFERENCE_ID_PATTERN = re.compile(
    r"^[a-z][a-z0-9_]*(\.[a-z0-9][a-z0-9_]*)+$"
)


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise AssertionError(f"Missing file: {path.relative_to(ROOT)}")

    data = yaml.safe_load(path.read_text(encoding="utf-8"))

    if not isinstance(data, dict):
        raise AssertionError(f"YAML root must be a mapping: {path.relative_to(ROOT)}")

    return data


def require_files() -> None:
    for path in [DOC_PATH, EXAMPLES_PATH, SCHEMA_PATH]:
        if not path.exists():
            raise AssertionError(f"Missing file: {path.relative_to(ROOT)}")


def validate_schema_file() -> None:
    schema = load_yaml(SCHEMA_PATH)

    if schema.get("$id") != "forprint_library.reference_contract.library_reference_v0_2":
        raise AssertionError("Unexpected schema $id")

    if schema.get("title") != "ForPrint Library Reference Contract v0.2":
        raise AssertionError("Unexpected schema title")

    required = set(schema.get("required", []))
    expected_required = {
        "schema_version",
        "reference_type",
        "reference_id",
        "display_label",
        "resolution_status",
        "source_module",
    }

    if not expected_required.issubset(required):
        missing = sorted(expected_required - required)
        raise AssertionError(f"Schema is missing required fields: {missing}")

    properties = schema.get("properties", {})

    if not isinstance(properties, dict):
        raise AssertionError("Schema properties must be a mapping")

    reference_type_enum = set(properties["reference_type"]["enum"])
    status_enum = set(properties["resolution_status"]["enum"])
    source_module_enum = set(properties["source_module"]["enum"])

    if reference_type_enum != EXPECTED_REFERENCE_TYPES:
        raise AssertionError("Schema reference_type enum mismatch")

    if status_enum != EXPECTED_STATUSES:
        raise AssertionError("Schema resolution_status enum mismatch")

    if source_module_enum != EXPECTED_SOURCE_MODULES:
        raise AssertionError("Schema source_module enum mismatch")


def validate_docs() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")

    required_phrases = [
        "Library Reference Contract Foundation v0.2",
        "canonical Library reference id format",
        "Downstream modules must not become owners",
        "library_reference_confirmed",
        "ambiguous_manual_review_required",
        "deprecated_reference",
        "unknown",
    ]

    for phrase in required_phrases:
        if phrase not in text:
            raise AssertionError(f"Document is missing phrase: {phrase}")

    forbidden_claims = [
        "Library owns order state",
        "Library owns pricing logic",
        "Library owns warehouse stock truth",
        "Library owns payment/accounting truth",
        "Library owns CRM workflow state",
        "Library owns Telegram runtime behavior",
        "Library owns Integration Gateway delivery ledger",
    ]

    for phrase in forbidden_claims:
        if phrase in text:
            raise AssertionError(f"Forbidden ownership claim found: {phrase}")


def validate_reference_id(reference_id: Any, status: str, example_id: str) -> None:
    if status == "unknown":
        if reference_id is not None:
            raise AssertionError(
                f"{example_id}: unknown references must keep reference_id null"
            )
        return

    if not isinstance(reference_id, str) or not reference_id:
        raise AssertionError(f"{example_id}: reference_id must be a non-empty string")

    if not REFERENCE_ID_PATTERN.match(reference_id):
        raise AssertionError(f"{example_id}: invalid reference_id: {reference_id}")


def validate_single_reference(example: dict[str, Any]) -> None:
    example_id = example.get("id", "<missing id>")

    payload = example.get("downstream_payload")
    if not isinstance(payload, dict):
        raise AssertionError(f"{example_id}: downstream_payload must be a mapping")

    reference = payload.get("library_reference")
    if not isinstance(reference, dict):
        raise AssertionError(f"{example_id}: library_reference must be a mapping")

    required_fields = {
        "schema_version",
        "reference_type",
        "reference_id",
        "display_label",
        "resolution_status",
        "source_module",
        "alias_input",
        "deprecation",
        "manual_review",
    }

    missing = sorted(required_fields - set(reference))
    if missing:
        raise AssertionError(f"{example_id}: missing fields: {missing}")

    if reference["schema_version"] != "library_reference_v0_2":
        raise AssertionError(f"{example_id}: invalid schema_version")

    reference_type = reference["reference_type"]
    status = reference["resolution_status"]
    source_module = reference["source_module"]

    if reference_type not in EXPECTED_REFERENCE_TYPES:
        raise AssertionError(f"{example_id}: unexpected reference_type")

    if status not in EXPECTED_STATUSES:
        raise AssertionError(f"{example_id}: unexpected resolution_status")

    if source_module not in EXPECTED_SOURCE_MODULES:
        raise AssertionError(f"{example_id}: unexpected source_module")

    if not isinstance(reference["display_label"], str) or not reference["display_label"]:
        raise AssertionError(f"{example_id}: display_label must be a non-empty string")

    validate_reference_id(reference["reference_id"], status, example_id)

    deprecation = reference["deprecation"]
    if not isinstance(deprecation, dict):
        raise AssertionError(f"{example_id}: deprecation must be a mapping")

    if status == "deprecated_reference":
        if deprecation.get("is_deprecated") is not True:
            raise AssertionError(f"{example_id}: deprecated reference must be marked")
        if not deprecation.get("replaced_by"):
            raise AssertionError(f"{example_id}: deprecated reference needs replaced_by")

    manual_review = reference["manual_review"]
    if not isinstance(manual_review, dict):
        raise AssertionError(f"{example_id}: manual_review must be a mapping")

    if status == "ambiguous_manual_review_required":
        if manual_review.get("required") is not True:
            raise AssertionError(f"{example_id}: ambiguous reference needs review")

    if status == "unknown":
        if manual_review.get("required") is not True:
            raise AssertionError(f"{example_id}: unknown reference needs review")


def validate_examples() -> None:
    data = load_yaml(EXAMPLES_PATH)

    if data.get("schema_version") != "library_reference_examples_v0_2":
        raise AssertionError("Unexpected examples schema_version")

    contract = data.get("library_reference_contract")
    if not isinstance(contract, dict):
        raise AssertionError("library_reference_contract must be a mapping")

    if contract.get("schema_version") != "library_reference_v0_2":
        raise AssertionError("Unexpected contract schema_version")

    examples = data.get("examples", [])
    if not isinstance(examples, list) or not examples:
        raise AssertionError("examples must be a non-empty list")

    seen_types: set[str] = set()
    seen_statuses: set[str] = set()

    for example in examples:
        if not isinstance(example, dict):
            raise AssertionError("Each example must be a mapping")

        validate_single_reference(example)

        reference = example["downstream_payload"]["library_reference"]
        seen_types.add(reference["reference_type"])
        seen_statuses.add(reference["resolution_status"])

    missing_types = sorted(EXPECTED_REFERENCE_TYPES - seen_types)
    missing_statuses = sorted(EXPECTED_STATUSES - seen_statuses)

    if missing_types:
        raise AssertionError(f"Missing reference type examples: {missing_types}")

    if missing_statuses:
        raise AssertionError(f"Missing status examples: {missing_statuses}")


def main() -> int:
    require_files()
    validate_schema_file()
    validate_docs()
    validate_examples()

    print("OK: Library reference contract foundation validates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())