from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "app"))

from forprint_library.calculator_input import (  # noqa: E402
    CalculatorInputContractError,
    CalculatorInputErrorType,
    build_calculator_input,
)

FIXTURE_DIR = ROOT / "examples" / "calculator_input_contract"
SCHEMA_PATH = ROOT / "schemas" / "calculator_input" / "calculator_input_envelope.schema.yaml"

VALID_FIXTURES = {
    "minimal_valid_business_card": "minimal_valid_business_card.yaml",
    "business_card_with_finishing": "business_card_with_finishing.yaml",
    "business_card_with_artwork_source": "business_card_with_artwork_source.yaml",
}

INVALID_FIXTURES = {
    "invalid_missing_material": (
        "invalid_missing_material.yaml",
        CalculatorInputErrorType.MISSING_REQUIRED_PARAMETER,
    ),
    "invalid_print_mode_reference": (
        "invalid_print_mode_reference.yaml",
        CalculatorInputErrorType.INVALID_REFERENCE,
    ),
    "invalid_quantity": (
        "invalid_quantity.yaml",
        CalculatorInputErrorType.INVALID_CONFIGURATION,
    ),
}

FORBIDDEN_KEYS = {
    "amount",
    "calculator_formula",
    "coefficient",
    "cost",
    "currency",
    "discount",
    "final_price",
    "formula",
    "margin",
    "price",
    "price_formula",
    "quote_total",
    "subtotal",
    "tax",
    "total",
    "vendor_price",
}


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise AssertionError(f"YAML root must be mapping: {path.relative_to(ROOT)}")
    return data


def iter_keys(value: object) -> list[str]:
    if isinstance(value, dict):
        keys = list(value)
        for nested in value.values():
            keys.extend(iter_keys(nested))
        return [str(key) for key in keys]

    if isinstance(value, list):
        keys: list[str] = []
        for item in value:
            keys.extend(iter_keys(item))
        return keys

    return []


def assert_no_forbidden_keys(data: dict[str, Any]) -> None:
    found = sorted(FORBIDDEN_KEYS.intersection(iter_keys(data)))
    if found:
        raise AssertionError(f"Forbidden monetary/pricing keys found: {found}")


def validate_schema_file() -> None:
    schema = load_yaml(SCHEMA_PATH)
    assert schema["title"] == "ForPrint Library Calculator Input Envelope"
    assert schema["properties"]["schema_version"]["const"] == "calculator_input_envelope_v0_1"
    assert schema["properties"]["product_id"]["const"] == "product.business_card"


def validate_valid_fixture(case_id: str, filename: str) -> None:
    fixture = load_yaml(FIXTURE_DIR / filename)
    assert fixture["schema_version"] == "calculator_input_fixture_v0_1"
    assert fixture["case_id"] == case_id
    assert fixture["product_id"] == "product.business_card"

    output = build_calculator_input(
        "product.business_card",
        fixture["input_configuration"],
    ).to_dict()

    assert output == fixture["expected_output"]
    assert_no_forbidden_keys(output)


def validate_invalid_fixture(
    case_id: str,
    filename: str,
    error_type: CalculatorInputErrorType,
) -> None:
    fixture = load_yaml(FIXTURE_DIR / filename)
    assert fixture["schema_version"] == "calculator_input_error_fixture_v0_1"
    assert fixture["case_id"] == case_id
    assert fixture["product_id"] == "product.business_card"

    try:
        build_calculator_input("product.business_card", fixture["input_configuration"])
    except CalculatorInputContractError as exc:
        error = exc.to_public_error()
    else:
        raise AssertionError(f"{case_id}: expected CalculatorInputContractError")

    assert error["error_type"] == error_type.value
    assert error == fixture["expected_error"]
    assert_no_forbidden_keys(error)


def main() -> int:
    validate_schema_file()

    for case_id, filename in VALID_FIXTURES.items():
        validate_valid_fixture(case_id, filename)

    for case_id, (filename, error_type) in INVALID_FIXTURES.items():
        validate_invalid_fixture(case_id, filename, error_type)

    print("OK: Library Calculator input contract validates")
    print(f"Fixtures: {FIXTURE_DIR.relative_to(ROOT)}")
    print(f"Schema: {SCHEMA_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
