from __future__ import annotations

CATALOG_SECTIONS: tuple[str, ...] = (
    "materials",
    "product_families",
    "operations",
    "print_modes",
    "finishing_options",
)

COMPONENT_CATALOG_FILES: dict[str, str] = {
    "materials": "catalog/materials.yaml",
    "product_families": "catalog/product_families.yaml",
    "operations": "catalog/operations.yaml",
    "print_modes": "catalog/print_modes.yaml",
    "finishing_options": "catalog/finishing_options.yaml",
}

REQUIRED_ITEM_FIELDS: tuple[str, ...] = (
    "id",
    "name_uk",
    "name_en",
    "aliases",
    "status",
    "version",
    "owner_module",
    "schema_status",
    "notes",
)

REQUIRED_SEED_METADATA_FIELDS: tuple[str, ...] = (
    "id",
    "version",
    "catalog_status",
    "schema_status",
    "usage",
    "contract_status",
    "owner_module",
)

EXPECTED_SEED_STATUS: dict[str, str] = {
    "catalog_status": "draft_canonical_seed",
    "schema_status": "unstable_v0_1",
    "usage": "allowed_for_projection_use",
    "contract_status": "not_final_contract",
    "owner_module": "forprint_library",
}

ALLOWED_ITEM_STATUSES: set[str] = {
    "draft",
    "active",
    "deprecated",
    "experimental",
}


class CatalogValidationError(ValueError):
    """Raised when a catalog seed or component catalog is invalid."""