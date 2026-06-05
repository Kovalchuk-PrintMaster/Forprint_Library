from __future__ import annotations

from pathlib import Path

import yaml
from forprint_library.catalog.loader import load_all_component_catalogs, load_seed
from forprint_library.catalog.models import CATALOG_SECTIONS, REQUIRED_ITEM_FIELDS
from forprint_library.catalog.registry import CatalogRegistry
from forprint_library.catalog.validation import (
    collect_seed_items,
    find_duplicate_aliases,
    validate_catalog_seed,
    validate_component_catalog,
)
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]


def test_catalog_seed_loads_successfully() -> None:
    seed = load_seed()
    validate_catalog_seed(seed)

    assert seed["metadata"]["catalog_status"] == "draft_canonical_seed"
    assert seed["metadata"]["schema_status"] == "unstable_v0_1"
    assert seed["metadata"]["usage"] == "allowed_for_projection_use"
    assert seed["metadata"]["contract_status"] == "not_final_contract"


def test_all_catalog_item_ids_are_unique() -> None:
    items = collect_seed_items(load_seed())
    ids = [item["id"] for item in items]

    assert len(ids) == len(set(ids))


def test_all_aliases_are_lists() -> None:
    items = collect_seed_items(load_seed())

    for item in items:
        assert isinstance(item["aliases"], list)
        assert item["aliases"]


def test_duplicate_aliases_are_reported_as_empty_for_current_seed() -> None:
    items = collect_seed_items(load_seed())

    assert find_duplicate_aliases(items) == {}


def test_required_item_fields_exist() -> None:
    items = collect_seed_items(load_seed())

    for item in items:
        for field in REQUIRED_ITEM_FIELDS:
            assert field in item


def test_catalog_status_fields_exist() -> None:
    metadata = load_seed()["metadata"]

    assert metadata["catalog_status"] == "draft_canonical_seed"
    assert metadata["schema_status"] == "unstable_v0_1"
    assert metadata["usage"] == "allowed_for_projection_use"
    assert metadata["contract_status"] == "not_final_contract"
    assert metadata["owner_module"] == "forprint_library"


def test_all_required_catalog_sections_validate() -> None:
    seed = load_seed()

    for section in CATALOG_SECTIONS:
        assert section in seed
        assert isinstance(seed[section], list)
        assert seed[section]


def test_product_families_validate() -> None:
    catalogs = load_all_component_catalogs()
    validate_component_catalog("product_families", catalogs["product_families"])


def test_materials_validate() -> None:
    catalogs = load_all_component_catalogs()
    validate_component_catalog("materials", catalogs["materials"])


def test_operations_validate() -> None:
    catalogs = load_all_component_catalogs()
    validate_component_catalog("operations", catalogs["operations"])


def test_print_modes_validate() -> None:
    catalogs = load_all_component_catalogs()
    validate_component_catalog("print_modes", catalogs["print_modes"])


def test_finishing_options_validate() -> None:
    catalogs = load_all_component_catalogs()
    validate_component_catalog("finishing_options", catalogs["finishing_options"])


def test_catalog_seed_schema_validates_seed() -> None:
    seed = yaml.safe_load((ROOT / "catalog/seeds/catalog_seed_v0_1.yaml").read_text())
    schema = yaml.safe_load((ROOT / "schemas/catalog_seed.schema.yaml").read_text())

    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(seed)


def test_example_catalog_seed_validates() -> None:
    example = yaml.safe_load((ROOT / "examples/catalog_seed_v0_1.example.yaml").read_text())
    schema = yaml.safe_load((ROOT / "schemas/catalog_seed.schema.yaml").read_text())

    Draft202012Validator(schema).validate(example)


def test_registry_resolves_known_aliases() -> None:
    registry = CatalogRegistry.from_project()

    business_card = registry.resolve_alias("візитка")
    gloss_paper = registry.resolve_alias("350gsm gloss")
    color_mode = registry.resolve_alias("4+4")

    assert business_card is not None
    assert gloss_paper is not None
    assert color_mode is not None

    assert business_card.item_id == "business_card"
    assert gloss_paper.item_id == "paper_350g_gloss"
    assert color_mode.item_id == "color_4_4"


def test_registry_returns_none_for_unknown_alias() -> None:
    registry = CatalogRegistry.from_project()

    assert registry.resolve_alias("невідомий матеріал") is None