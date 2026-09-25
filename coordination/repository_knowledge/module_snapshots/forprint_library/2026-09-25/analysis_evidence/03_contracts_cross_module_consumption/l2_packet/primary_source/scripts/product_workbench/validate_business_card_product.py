from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]

CARD_PATH = ROOT / "catalog" / "configurable_products" / "business_card.yaml"
SCHEMA_PATH = ROOT / "schemas" / "configurable_product.schema.yaml"
EXAMPLE_PATH = ROOT / "examples" / "product_cards" / "business_card_product_card.yaml"

CATALOG_PATHS = {
    "materials": ROOT / "catalog" / "materials.yaml",
    "print_modes": ROOT / "catalog" / "print_modes.yaml",
    "finishing_options": ROOT / "catalog" / "finishing_options.yaml",
    "product_families": ROOT / "catalog" / "product_families.yaml",
}

REQUIRED_PARAMETERS = {
    "size",
    "sides",
    "material_ref",
    "print_mode_ref",
    "quantity",
    "finishing_refs",
}

REQUIRED_ALIASES = {
    "візитки",
    "візитка",
    "business cards",
    "business card",
}

FORBIDDEN_KEYS = {
    "price",
    "final_price",
    "price_formula",
    "stock_truth",
    "stock_mutation",
    "material_write_off",
    "production_task",
    "production_task_logic",
    "one_c_import",
    "one_c_sync",
    "calculator_integration",
    "telegram_runtime",
    "operational_registry_write",
    "crm_write",
    "website_write",
    "client_data",
    "order_data",
}


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise AssertionError(f"Missing file: {path.relative_to(ROOT)}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise AssertionError(f"YAML root must be mapping: {path.relative_to(ROOT)}")
    return data


def collect_catalog_ids() -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    for catalog_name, path in CATALOG_PATHS.items():
        data = load_yaml(path)
        items = data.get("items")
        if not isinstance(items, list):
            raise AssertionError(f"{catalog_name}: items must be a list")
        result[catalog_name] = {
            item["id"]
            for item in items
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        }
    return result


def iter_keys(value: Any) -> list[str]:
    if isinstance(value, dict):
        keys = list(value)
        for nested in value.values():
            keys.extend(iter_keys(nested))
        return keys

    if isinstance(value, list):
        keys: list[str] = []
        for item in value:
            keys.extend(iter_keys(item))
        return keys

    return []


def validate_no_forbidden_keys(data: dict[str, Any]) -> None:
    found = sorted(FORBIDDEN_KEYS.intersection(iter_keys(data)))
    if found:
        raise AssertionError(f"Forbidden ownership keys found: {found}")


def require_ref(ref: dict[str, Any], catalog_ids: dict[str, set[str]]) -> None:
    catalog = ref.get("catalog")
    ref_id = ref.get("id")

    if not isinstance(catalog, str) or not isinstance(ref_id, str):
        raise AssertionError(f"Reference must include catalog and id: {ref}")

    if catalog not in catalog_ids:
        raise AssertionError(f"Unknown reference catalog: {catalog}")

    if ref_id not in catalog_ids[catalog]:
        raise AssertionError(f"Unknown {catalog} reference id: {ref_id}")


def validate_reference_fields(card: dict[str, Any]) -> None:
    catalog_ids = collect_catalog_ids()

    family_ref = card.get("product_family_ref")
    if not isinstance(family_ref, dict):
        raise AssertionError("product_family_ref must be a mapping")
    require_ref(family_ref, catalog_ids)

    for parameter in card["constructor_parameters"]:
        if not isinstance(parameter, dict):
            raise AssertionError("constructor parameter must be mapping")

        for ref in parameter.get("allowed_refs", []):
            if not isinstance(ref, dict):
                raise AssertionError("allowed_refs values must be mappings")
            require_ref(ref, catalog_ids)

        for value in parameter.get("allowed_values", []):
            if not isinstance(value, dict):
                continue
            print_mode_ref = value.get("print_mode_ref")
            if isinstance(print_mode_ref, dict):
                require_ref(print_mode_ref, catalog_ids)


def validate_card(card: dict[str, Any]) -> None:
    validate_no_forbidden_keys(card)

    assert card["schema_version"] == "configurable_product_card_v0_1"
    assert card["product_id"] == "product.business_card"
    assert card["kind"] == "configurable_product"
    assert card["status"] == "draft_reference"
    assert card["owner_module"] == "forprint_library"
    assert card["names"]["uk"] == "Візитки"
    assert card["names"]["en"] == "Business cards"

    aliases = set(card.get("aliases", []))
    missing_aliases = REQUIRED_ALIASES - aliases
    if missing_aliases:
        raise AssertionError(f"Missing required aliases: {sorted(missing_aliases)}")

    parameters = card.get("constructor_parameters")
    if not isinstance(parameters, list):
        raise AssertionError("constructor_parameters must be a list")

    keys = {
        parameter.get("key")
        for parameter in parameters
        if isinstance(parameter, dict)
    }
    missing_parameters = REQUIRED_PARAMETERS - keys
    if missing_parameters:
        raise AssertionError(
            f"Missing required parameters: {sorted(missing_parameters)}"
        )

    quantity = next(
        parameter for parameter in parameters if parameter.get("key") == "quantity"
    )
    assert quantity["type"] == "numeric_input_context"
    assert quantity["consumer_owned_value"] is True

    validate_reference_fields(card)


def validate_examples(card: dict[str, Any]) -> None:
    examples = load_yaml(EXAMPLE_PATH)
    validate_no_forbidden_keys(examples)

    assert examples["product_ref"]["product_id"] == card["product_id"]

    consumers = {
        example["consumer_module"]
        for example in examples["examples"]
        if isinstance(example, dict)
    }
    expected = {
        "telegram_bot",
        "calculator_engine",
        "forprint_operational_registry",
    }
    if consumers != expected:
        raise AssertionError(f"Unexpected consumers: {sorted(consumers)}")

    for example in examples["examples"]:
        assert example.get("allowed_use")


def validate_schema_file() -> None:
    schema = load_yaml(SCHEMA_PATH)
    assert schema["title"] == "ForPrint Configurable Product Card"
    assert "constructor_parameters" in schema["required"]
    assert schema["properties"]["product_id"]["pattern"] == "^product\\.[a-z0-9_]+$"


def main() -> int:
    validate_schema_file()
    card = load_yaml(CARD_PATH)
    validate_card(card)
    validate_examples(card)
    print("OK: Business card configurable product card validates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())