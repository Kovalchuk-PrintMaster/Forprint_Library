from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
CARD = ROOT / "catalog" / "configurable_products" / "business_card.yaml"
SCHEMA = ROOT / "schemas" / "configurable_product.schema.yaml"
EXAMPLE = ROOT / "examples" / "product_cards" / "business_card_product_card.yaml"
VALIDATOR = ROOT / "scripts" / "product_workbench" / "validate_business_card_product.py"
PREVIEW = ROOT / "scripts" / "product_workbench" / "preview_business_card_product.py"


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def run_script(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )


def test_business_card_product_files_exist() -> None:
    assert CARD.exists()
    assert SCHEMA.exists()
    assert EXAMPLE.exists()
    assert VALIDATOR.exists()
    assert PREVIEW.exists()


def test_business_card_product_id_is_stable() -> None:
    card = load_yaml(CARD)

    assert card["schema_version"] == "configurable_product_card_v0_1"
    assert card["product_id"] == "product.business_card"
    assert card["kind"] == "configurable_product"
    assert card["status"] == "draft_reference"
    assert card["owner_module"] == "forprint_library"


def test_business_card_names_and_aliases_exist() -> None:
    card = load_yaml(CARD)

    assert card["names"]["uk"] == "Візитки"
    assert card["names"]["en"] == "Business cards"

    aliases = set(card["aliases"])
    assert {"візитки", "візитка", "business cards", "business card"} <= aliases
    assert "product:business_cards" in card["compatibility_aliases"]


def test_business_card_required_constructor_parameters_exist() -> None:
    card = load_yaml(CARD)

    keys = {parameter["key"] for parameter in card["constructor_parameters"]}
    assert {
        "size",
        "sides",
        "material_ref",
        "print_mode_ref",
        "quantity",
        "finishing_refs",
    } <= keys
    assert "artwork_source" in keys


def test_business_card_uses_library_references() -> None:
    card = load_yaml(CARD)

    assert card["product_family_ref"]["catalog"] == "product_families"
    assert card["product_family_ref"]["id"] == "business_card"

    parameters = {
        parameter["key"]: parameter
        for parameter in card["constructor_parameters"]
    }

    assert parameters["material_ref"]["reference_catalog"] == "materials"
    assert parameters["print_mode_ref"]["reference_catalog"] == "print_modes"
    assert parameters["finishing_refs"]["reference_catalog"] == "finishing_options"


def test_business_card_validator_passes() -> None:
    result = run_script(VALIDATOR)

    assert "OK: Business card configurable product card validates" in result.stdout


def test_business_card_preview_renders_expected_content() -> None:
    result = run_script(PREVIEW)

    assert "Product card: Візитки" in result.stdout
    assert "Product ID: product.business_card" in result.stdout
    assert "Kind: configurable_product" in result.stdout
    assert "- size" in result.stdout
    assert "- material_ref" in result.stdout
    assert "- finishing_refs" in result.stdout
    assert "Telegram Bot" in result.stdout
    assert "Calculator Engine" in result.stdout
    assert "Operational Registry" in result.stdout


def test_business_card_forbidden_ownership_fields_absent() -> None:
    card_text = CARD.read_text(encoding="utf-8")
    example_text = EXAMPLE.read_text(encoding="utf-8")

    forbidden = [
        "final_price:",
        "price_formula:",
        "stock_truth:",
        "stock_mutation:",
        "material_write_off:",
        "production_task:",
        "one_c_import:",
        "one_c_sync:",
        "calculator_integration:",
        "telegram_runtime:",
        "operational_registry_write:",
        "client_data:",
        "order_data:",
    ]

    for needle in forbidden:
        assert needle not in card_text
        assert needle not in example_text