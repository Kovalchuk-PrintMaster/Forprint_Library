from __future__ import annotations

from forprint_library.catalog.registry import CatalogLookupResult, CatalogRegistry


def resolve_catalog_alias(alias: str, 
                          registry: CatalogRegistry | None = None) -> CatalogLookupResult | None:
    active_registry = registry or CatalogRegistry.from_project()
    return active_registry.resolve_alias(alias)