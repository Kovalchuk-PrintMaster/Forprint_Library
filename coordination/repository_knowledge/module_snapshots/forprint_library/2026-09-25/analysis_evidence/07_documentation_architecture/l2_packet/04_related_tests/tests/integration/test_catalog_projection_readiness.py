from __future__ import annotations

from forprint_library.catalog.loader import load_seed
from forprint_library.catalog.registry import CatalogRegistry


def test_catalog_seed_is_projection_ready_for_dependent_modules() -> None:
    seed = load_seed()
    metadata = seed["metadata"]

    assert metadata["catalog_status"] == "draft_canonical_seed"
    assert metadata["schema_status"] == "unstable_v0_1"
    assert metadata["usage"] == "allowed_for_projection_use"
    assert metadata["contract_status"] == "not_final_contract"
    assert metadata["owner_module"] == "forprint_library"


def test_registry_provides_stable_ids_for_projection_use() -> None:
    registry = CatalogRegistry.from_project()

    business_card = registry.get("business_card")
    paper = registry.get("paper_300g_matte")
    operation = registry.get("digital_print")
    print_mode = registry.get("color_4_0")
    finishing = registry.get("matte_lamination")

    assert business_card is not None
    assert paper is not None
    assert operation is not None
    assert print_mode is not None
    assert finishing is not None

    assert business_card.section == "product_families"
    assert paper.section == "materials"
    assert operation.section == "operations"
    assert print_mode.section == "print_modes"
    assert finishing.section == "finishing_options"