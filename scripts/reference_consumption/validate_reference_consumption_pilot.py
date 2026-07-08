from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]

EXAMPLES_PATH = (
    ROOT
    / "examples"
    / "reference_consumption"
    / "library_reference_consumption_examples.yaml"
)
SCHEMA_PATH = (
    ROOT
    / "schemas"
    / "reference_consumption"
    / "library_reference_consumption.schema.yaml"
)
REFERENCE_CONTRACT_EXAMPLES_PATH = (
    ROOT / "examples" / "reference_contract" / "library_reference_examples.yaml"
)
DOC_PATH = ROOT / "docs" / "architecture" / "reference_consumption_pilot.md"

EXPECTED_SCHEMA_VERSION = "library_reference_consumption_examples_v0_3"
EXPECTED_PILOT_ID = "library_reference_consumption_pilot_v0_3"
EXPECTED_OWNER_MODULE = "forprint_library"
EXPECTED_REFERENCE_SCHEMA_VERSION = "library_reference_v0_2"

ALLOWED_CONSUMER_MODULES = {
    "calculator_engine",
    "telegram_bot",
    "forprint_operational_registry",
    "forprint_accounting_registry_service",
    "forprint_prepress_hub",
    "forprint_integration_gateway",
}

ALLOWED_REFERENCE_TYPES = {
    "product_service",
    "material",
    "operation",
    "unit",
    "template",
    "technical_card",
}

ALLOWED_RESOLUTION_STATUSES = {
    "library_reference_confirmed",
    "library_reference_pending",
    "ambiguous_manual_review_required",
    "deprecated_reference",
}

FORBIDDEN_CONSUMER_FIELDS = {
    "canonical_name_override",
    "semantic_definition_override",
    "library_alias_write",
    "library_reference_write",
    "final_price",
    "price_formula",
    "stock_mutation",
    "material_write_off",
    "order_creation",
    "client_creation",
    "payment_posting",
    "production_runtime_write",
    "telegram_runtime_behavior",
    "calculator_runtime_integration",
    "operational_registry_write",
    "one_c_sync",
    "one_c_import",
}


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise AssertionError(f"Missing file: {path.relative_to(ROOT)}")

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise AssertionError(f"YAML root must be a mapping: {path.relative_to(ROOT)}")

    return data


def require_files() -> None:
    for path in [EXAMPLES_PATH, SCHEMA_PATH, REFERENCE_CONTRACT_EXAMPLES_PATH, DOC_PATH]:
        if not path.exists():
            raise AssertionError(f"Missing file: {path.relative_to(ROOT)}")


def collect_known_library_reference_ids() -> set[str]:
    data = load_yaml(REFERENCE_CONTRACT_EXAMPLES_PATH)
    examples = data.get("examples", [])

    if not isinstance(examples, list) or not examples:
        raise AssertionError("Reference contract examples must be a non-empty list")

    known_ids: set[str] = set()

    for example in examples:
        if not isinstance(example, dict):
            raise AssertionError("Reference contract example must be a mapping")

        reference = (
            example.get("downstream_payload", {})
            .get("library_reference", {})
        )

        if not isinstance(reference, dict):
            raise AssertionError("Reference contract library_reference must be a mapping")

        reference_id = reference.get("reference_id")
        if isinstance(reference_id, str) and reference_id:
            known_ids.add(reference_id)

    if not known_ids:
        raise AssertionError("No known Library reference IDs found")

    return known_ids


def validate_schema_file() -> None:
    schema = load_yaml(SCHEMA_PATH)

    if schema.get("$id") != (
        "forprint_library.reference_consumption.library_reference_consumption_v0_3"
    ):
        raise AssertionError("Unexpected reference consumption schema $id")

    if schema.get("title") != "ForPrint Library Reference Consumption Pilot v0.3":
        raise AssertionError("Unexpected reference consumption schema title")

    required = set(schema.get("required", []))
    expected_required = {
        "schema_version",
        "pilot_id",
        "owner_module",
        "reference_contract_source",
        "valid_consumer_payloads",
        "invalid_consumer_payloads",
    }

    missing = sorted(expected_required - required)
    if missing:
        raise AssertionError(f"Schema is missing required fields: {missing}")

    shape = schema.get("consumer_payload_shape")
    if not isinstance(shape, dict):
        raise AssertionError("Schema must document consumer_payload_shape")

    forbidden = set(shape.get("forbidden_consumer_fields", []))
    missing_forbidden = sorted(FORBIDDEN_CONSUMER_FIELDS - forbidden)
    if missing_forbidden:
        raise AssertionError(
            f"Schema is missing forbidden consumer fields: {missing_forbidden}"
        )


def iter_mapping_keys(value: Any) -> list[str]:
    keys: list[str] = []

    if isinstance(value, dict):
        for key, nested in value.items():
            keys.append(str(key))
            keys.extend(iter_mapping_keys(nested))
    elif isinstance(value, list):
        for item in value:
            keys.extend(iter_mapping_keys(item))

    return keys


def validate_no_forbidden_fields(payload: dict[str, Any], payload_id: str) -> None:
    keys = set(iter_mapping_keys(payload))
    forbidden = sorted(keys & FORBIDDEN_CONSUMER_FIELDS)

    if forbidden:
        raise AssertionError(f"{payload_id}: forbidden field(s): {forbidden}")


def validate_reference(
    reference: Any,
    *,
    payload_id: str,
    known_reference_ids: set[str],
) -> None:
    if not isinstance(reference, dict):
        raise AssertionError(f"{payload_id}: library_owned_reference must be a mapping")

    required_fields = {
        "schema_version",
        "reference_type",
        "reference_id",
        "display_label",
        "resolution_status",
    }

    missing = sorted(required_fields - set(reference))
    if missing:
        raise AssertionError(f"{payload_id}: missing library reference fields: {missing}")

    if reference["schema_version"] != EXPECTED_REFERENCE_SCHEMA_VERSION:
        raise AssertionError(f"{payload_id}: invalid library reference schema_version")

    if reference["reference_type"] not in ALLOWED_REFERENCE_TYPES:
        raise AssertionError(f"{payload_id}: invalid library reference type")

    if reference["resolution_status"] not in ALLOWED_RESOLUTION_STATUSES:
        raise AssertionError(f"{payload_id}: invalid library reference status")

    reference_id = reference["reference_id"]
    if not isinstance(reference_id, str) or not reference_id:
        raise AssertionError(f"{payload_id}: reference_id must be a non-empty string")

    if reference_id not in known_reference_ids:
        raise AssertionError(f"{payload_id}: unknown Library reference id: {reference_id}")

    display_label = reference["display_label"]
    if not isinstance(display_label, str) or not display_label:
        raise AssertionError(f"{payload_id}: display_label must be a non-empty string")


def validate_boundary_assertions(assertions: Any, payload_id: str) -> None:
    if not isinstance(assertions, dict):
        raise AssertionError(f"{payload_id}: boundary_assertions must be a mapping")

    required_true_flags = {
        "example_only",
        "no_library_semantic_redefinition",
        "no_downstream_runtime_write",
    }

    for flag in required_true_flags:
        if assertions.get(flag) is not True:
            raise AssertionError(f"{payload_id}: boundary assertion must be true: {flag}")


def validate_payload(
    payload: dict[str, Any],
    *,
    known_reference_ids: set[str],
) -> None:
    payload_id = str(payload.get("id", "<missing id>"))

    required_fields = {
        "id",
        "description",
        "consumer_module",
        "consumer_payload_id",
        "library_owned_reference",
        "consumer_owned_fields",
        "foreign_module_references",
        "boundary_assertions",
    }

    missing = sorted(required_fields - set(payload))
    if missing:
        raise AssertionError(f"{payload_id}: missing required fields: {missing}")

    consumer_module = payload["consumer_module"]
    if consumer_module not in ALLOWED_CONSUMER_MODULES:
        raise AssertionError(f"{payload_id}: invalid consumer_module: {consumer_module}")

    if not isinstance(payload["consumer_payload_id"], str) or not payload["consumer_payload_id"]:
        raise AssertionError(f"{payload_id}: consumer_payload_id must be a string")

    if not isinstance(payload["consumer_owned_fields"], dict):
        raise AssertionError(f"{payload_id}: consumer_owned_fields must be a mapping")

    if not isinstance(payload["foreign_module_references"], dict):
        raise AssertionError(f"{payload_id}: foreign_module_references must be a mapping")

    validate_no_forbidden_fields(payload, payload_id)
    validate_reference(
        payload["library_owned_reference"],
        payload_id=payload_id,
        known_reference_ids=known_reference_ids,
    )
    validate_boundary_assertions(payload["boundary_assertions"], payload_id)


def validate_examples() -> dict[str, Any]:
    data = load_yaml(EXAMPLES_PATH)
    known_reference_ids = collect_known_library_reference_ids()

    if data.get("schema_version") != EXPECTED_SCHEMA_VERSION:
        raise AssertionError("Unexpected reference consumption examples schema_version")

    if data.get("pilot_id") != EXPECTED_PILOT_ID:
        raise AssertionError("Unexpected reference consumption pilot_id")

    if data.get("owner_module") != EXPECTED_OWNER_MODULE:
        raise AssertionError("Unexpected reference consumption owner_module")

    source = data.get("reference_contract_source")
    if not isinstance(source, dict):
        raise AssertionError("reference_contract_source must be a mapping")

    if source.get("schema_version") != EXPECTED_REFERENCE_SCHEMA_VERSION:
        raise AssertionError("reference_contract_source schema_version mismatch")

    valid_payloads = data.get("valid_consumer_payloads", [])
    invalid_payloads = data.get("invalid_consumer_payloads", [])

    if not isinstance(valid_payloads, list) or not valid_payloads:
        raise AssertionError("valid_consumer_payloads must be a non-empty list")

    if not isinstance(invalid_payloads, list) or not invalid_payloads:
        raise AssertionError("invalid_consumer_payloads must be a non-empty list")

    for payload in valid_payloads:
        if not isinstance(payload, dict):
            raise AssertionError("Each valid payload must be a mapping")
        validate_payload(payload, known_reference_ids=known_reference_ids)

    for payload in invalid_payloads:
        if not isinstance(payload, dict):
            raise AssertionError("Each invalid payload must be a mapping")

        expected_error = payload.get("expected_error_contains")
        if not isinstance(expected_error, str) or not expected_error:
            raise AssertionError(
                f"{payload.get('id', '<missing id>')}: expected_error_contains required"
            )

        try:
            validate_payload(payload, known_reference_ids=known_reference_ids)
        except AssertionError as exc:
            if expected_error not in str(exc):
                raise AssertionError(
                    f"{payload.get('id', '<missing id>')}: expected error "
                    f"containing {expected_error!r}, got {exc!s}"
                ) from exc
        else:
            raise AssertionError(
                f"{payload.get('id', '<missing id>')}: invalid payload unexpectedly passed"
            )

    return data


def validate_docs() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")

    required_phrases = [
        "Library Reference Consumption Pilot v0.3",
        "Library-owned reference IDs",
        "consumer-owned runtime fields",
        "foreign module references",
        "must not redefine Library-owned semantics",
        "does not implement Calculator formulas",
        "does not implement Telegram runtime behavior",
        "does not implement Operational Registry storage",
        "does not start Configurable Product Workbench",
    ]

    for phrase in required_phrases:
        if phrase not in text:
            raise AssertionError(f"Document is missing phrase: {phrase}")


def render_preview(data: dict[str, Any]) -> None:
    print("ForPrint Library Reference Consumption Pilot v0.3")
    print("Mode: local read-only examples")
    print("")

    for payload in data["valid_consumer_payloads"]:
        reference = payload["library_owned_reference"]
        assertions = payload["boundary_assertions"]

        print(f"- Consumer: {payload['consumer_module']}")
        print(f"  Payload: {payload['consumer_payload_id']}")
        print(
            "  Uses Library reference: "
            f"{reference['reference_type']}::{reference['reference_id']}"
        )
        print(
            "  Boundary: "
            "no semantic redefinition, no downstream runtime write"
        )
        print(f"  Example only: {assertions.get('example_only')}")
        print("")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Render a human-readable preview of valid consumer payloads.",
    )
    args = parser.parse_args()

    require_files()
    validate_schema_file()
    validate_docs()
    data = validate_examples()

    if args.preview:
        render_preview(data)
    else:
        print("OK: Library reference consumption pilot validates")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())