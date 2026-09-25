import socket
from pathlib import Path
from typing import Any

import pytest
import yaml
from forprint_library.calculator_input import (
    CalculatorInputContractError,
    CalculatorInputErrorType,
    build_calculator_input,
)

ROOT = Path(__file__).resolve().parents[2]
FIXTURE_DIR = ROOT / "examples" / "calculator_input_contract"
VALIDATOR = ROOT / "scripts" / "calculator_input" / "validate_calculator_input_contract.py"
BUSINESS_CARD = ROOT / "catalog" / "configurable_products" / "business_card.yaml"

MONETARY_KEYS = {
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


def minimal_configuration() -> dict[str, object]:
    return {
        "size": "size_90x50_mm",
        "sides": "one_sided",
        "material_ref": {"catalog": "materials", "id": "paper_300g_matte"},
        "print_mode_ref": {"catalog": "print_modes", "id": "color_4_0"},
        "quantity": 100,
    }


def full_configuration() -> dict[str, object]:
    return {
        "size": "size_85x55_mm",
        "sides": "two_sided",
        "material_ref": {"catalog": "materials", "id": "paper_350g_gloss"},
        "print_mode_ref": {"catalog": "print_modes", "id": "color_4_4"},
        "quantity": 500,
        "finishing_refs": [
            {"catalog": "finishing_options", "id": "corner_rounding"},
            {"catalog": "finishing_options", "id": "matte_lamination"},
        ],
        "artwork_source": "customer_print_ready_file",
    }


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


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def test_valid_minimal_business_card_projection() -> None:
    envelope = build_calculator_input("product.business_card", minimal_configuration())
    data = envelope.to_dict()

    assert data["schema_version"] == "calculator_input_envelope_v0_1"
    assert data["product_id"] == "product.business_card"
    assert data["configuration_id"].startswith("calc_input_")
    assert data["normalized_parameters"] == {
        "size": "size_90x50_mm",
        "sides": "one_sided",
        "material_ref": {"catalog": "materials", "id": "paper_300g_matte"},
        "print_mode_ref": {"catalog": "print_modes", "id": "color_4_0"},
        "quantity": 100,
        "finishing_refs": [],
    }
    assert data["validation_snapshot"]["valid"] is True
    assert data["validation_snapshot"]["errors"] == []


def test_valid_full_business_card_projection() -> None:
    envelope = build_calculator_input("product.business_card", full_configuration())
    data = envelope.to_dict()

    assert data["normalized_parameters"]["size"] == "size_85x55_mm"
    assert data["normalized_parameters"]["sides"] == "two_sided"
    assert data["normalized_parameters"]["quantity"] == 500
    assert data["normalized_parameters"]["artwork_source"] == "customer_print_ready_file"
    assert data["reference_ids"]["material_ref"] == {
        "catalog": "materials",
        "id": "paper_350g_gloss",
    }


def test_deterministic_output_for_semantically_equal_input() -> None:
    first = full_configuration()
    second = full_configuration()
    second["finishing_refs"] = [
        {"catalog": "finishing_options", "id": "matte_lamination"},
        {"catalog": "finishing_options", "id": "corner_rounding"},
        {"catalog": "finishing_options", "id": "corner_rounding"},
    ]

    assert build_calculator_input("product.business_card", first).to_dict() == (
        build_calculator_input("product.business_card", second).to_dict()
    )


def test_input_mapping_is_not_mutated() -> None:
    configuration = full_configuration()
    original = load_yaml_from_string(yaml.safe_dump(configuration, allow_unicode=True))

    build_calculator_input("product.business_card", configuration)

    assert configuration == original


def test_finishing_references_normalize_deterministically() -> None:
    configuration = minimal_configuration()
    configuration["finishing_refs"] = [
        {"catalog": "finishing_options", "id": "matte_lamination"},
        {"catalog": "finishing_options", "id": "corner_rounding"},
    ]

    output = build_calculator_input("product.business_card", configuration).to_dict()

    assert output["normalized_parameters"]["finishing_refs"] == [
        {"catalog": "finishing_options", "id": "corner_rounding"},
        {"catalog": "finishing_options", "id": "matte_lamination"},
    ]


def test_optional_artwork_source_behavior() -> None:
    without_artwork = build_calculator_input(
        "product.business_card",
        minimal_configuration(),
    ).to_dict()
    assert "artwork_source" not in without_artwork["normalized_parameters"]

    configuration = minimal_configuration()
    configuration["artwork_source"] = "customer_needs_prepress_check"
    with_artwork = build_calculator_input("product.business_card", configuration).to_dict()

    assert (
        with_artwork["normalized_parameters"]["artwork_source"]
        == "customer_needs_prepress_check"
    )


def test_missing_required_parameter_error() -> None:
    configuration = minimal_configuration()
    configuration.pop("material_ref")

    with pytest.raises(CalculatorInputContractError) as exc_info:
        build_calculator_input("product.business_card", configuration)

    assert exc_info.value.error_type == CalculatorInputErrorType.MISSING_REQUIRED_PARAMETER
    assert exc_info.value.to_public_error()["field_path"] == "material_ref"


def test_invalid_material_reference_error() -> None:
    configuration = minimal_configuration()
    configuration["material_ref"] = {"catalog": "materials", "id": "unknown_material"}

    with pytest.raises(CalculatorInputContractError) as exc_info:
        build_calculator_input("product.business_card", configuration)

    assert exc_info.value.error_type == CalculatorInputErrorType.INVALID_REFERENCE
    assert exc_info.value.to_public_error()["field_path"] == "material_ref"


def test_invalid_print_mode_reference_error() -> None:
    configuration = minimal_configuration()
    configuration["print_mode_ref"] = {"catalog": "print_modes", "id": "unknown_print_mode"}

    with pytest.raises(CalculatorInputContractError) as exc_info:
        build_calculator_input("product.business_card", configuration)

    assert exc_info.value.error_type == CalculatorInputErrorType.INVALID_REFERENCE
    assert exc_info.value.to_public_error()["field_path"] == "print_mode_ref"


def test_invalid_quantity_error() -> None:
    configuration = minimal_configuration()
    configuration["quantity"] = 0

    with pytest.raises(CalculatorInputContractError) as exc_info:
        build_calculator_input("product.business_card", configuration)

    assert exc_info.value.error_type == CalculatorInputErrorType.INVALID_CONFIGURATION
    assert exc_info.value.to_public_error()["field_path"] == "quantity"


def test_unknown_product_error() -> None:
    with pytest.raises(CalculatorInputContractError) as exc_info:
        build_calculator_input("product.unknown", minimal_configuration())

    assert exc_info.value.error_type == CalculatorInputErrorType.UNKNOWN_PRODUCT


def test_unsupported_schema_version_error() -> None:
    with pytest.raises(CalculatorInputContractError) as exc_info:
        build_calculator_input(
            "product.business_card",
            minimal_configuration(),
            schema_version="calculator_input_envelope_v9_9",
        )

    assert exc_info.value.error_type == CalculatorInputErrorType.UNSUPPORTED_PROJECTION_VERSION


def test_stable_serialized_fixture() -> None:
    fixture = load_yaml(FIXTURE_DIR / "minimal_valid_business_card.yaml")
    output = build_calculator_input(
        "product.business_card",
        fixture["input_configuration"],
    ).to_dict()

    assert output == fixture["expected_output"]


def test_no_monetary_fields_in_contract_output() -> None:
    output = build_calculator_input("product.business_card", full_configuration()).to_dict()

    assert not MONETARY_KEYS.intersection(iter_keys(output))


def test_no_network_or_write_side_effects(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_write(*args: object, **kwargs: object) -> None:
        raise AssertionError("Calculator input contract must not write files")

    def fail_network(*args: object, **kwargs: object) -> None:
        raise AssertionError("Calculator input contract must not use network")

    monkeypatch.setattr(Path, "write_text", fail_write)
    monkeypatch.setattr(Path, "write_bytes", fail_write)
    monkeypatch.setattr(socket, "socket", fail_network)

    build_calculator_input("product.business_card", minimal_configuration())


def test_backward_compatibility_with_business_card_card() -> None:
    card = load_yaml(BUSINESS_CARD)

    assert card["product_id"] == "product.business_card"
    assert card["schema_version"] == "configurable_product_card_v0_1"
    assert card["kind"] == "configurable_product"


def test_fixture_validator_script_passes() -> None:
    import subprocess

    result = subprocess.run(
        [
            ".venv_forprint_library/bin/python",
            "scripts/calculator_input/validate_calculator_input_contract.py",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "OK: Library Calculator input contract validates" in result.stdout


def load_yaml_from_string(text: str) -> object:
    return yaml.safe_load(text)
