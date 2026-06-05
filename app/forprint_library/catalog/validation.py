from __future__ import annotations

from collections import defaultdict
from typing import Any

from forprint_library.catalog.models import (
    ALLOWED_ITEM_STATUSES,
    CATALOG_SECTIONS,
    EXPECTED_SEED_STATUS,
    REQUIRED_ITEM_FIELDS,
    REQUIRED_SEED_METADATA_FIELDS,
    CatalogValidationError,
)


def normalize_alias(alias: str) -> str:
    return " ".join(alias.casefold().strip().split())


def collect_seed_items(seed: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []

    for section in CATALOG_SECTIONS:
        section_items = seed.get(section)
        if not isinstance(section_items, list):
            raise CatalogValidationError(f"Seed section must be a list: {section}")

        for item in section_items:
            if not isinstance(item, dict):
                raise CatalogValidationError(f"Seed item must be a mapping in section: {section}")

            item_with_section = dict(item)
            item_with_section["_section"] = section
            items.append(item_with_section)

    return items


def validate_seed_metadata(seed: dict[str, Any]) -> None:
    metadata = seed.get("metadata")
    if not isinstance(metadata, dict):
        raise CatalogValidationError("Seed must contain metadata mapping.")

    missing = [field for field in REQUIRED_SEED_METADATA_FIELDS if field not in metadata]
    if missing:
        raise CatalogValidationError(f"Seed metadata missing required fields: {missing}")

    mismatched = {
        key: {"expected": expected, "actual": metadata.get(key)}
        for key, expected in EXPECTED_SEED_STATUS.items()
        if metadata.get(key) != expected
    }
    if mismatched:
        raise CatalogValidationError(f"Seed metadata has unexpected status values: {mismatched}")


def validate_required_item_fields(items: list[dict[str, Any]]) -> None:
    for item in items:
        missing = [field for field in REQUIRED_ITEM_FIELDS if field not in item]
        if missing:
            item_id = item.get("id", "<missing-id>")
            raise CatalogValidationError(f"Item {item_id} missing required fields: {missing}")


def validate_item_status_values(items: list[dict[str, Any]]) -> None:
    for item in items:
        item_id = item.get("id", "<missing-id>")

        if item.get("status") not in ALLOWED_ITEM_STATUSES:
            raise CatalogValidationError(
                f"Item {item_id} has unsupported status: {item.get('status')}"
            )

        if item.get("owner_module") != "forprint_library":
            raise CatalogValidationError(f"Item {item_id} must be owned by forprint_library")

        if item.get("schema_status") != "unstable_v0_1":
            raise CatalogValidationError(f"Item {item_id} must use unstable_v0_1")


def validate_unique_item_ids(items: list[dict[str, Any]]) -> None:
    seen: dict[str, str] = {}

    for item in items:
        item_id = item["id"]
        section = item["_section"]

        if item_id in seen:
            raise CatalogValidationError(
                f"Duplicate catalog item id: {item_id} in {seen[item_id]} and {section}"
            )

        seen[item_id] = section


def validate_alias_lists(items: list[dict[str, Any]]) -> None:
    for item in items:
        item_id = item.get("id", "<missing-id>")
        aliases = item.get("aliases")

        if not isinstance(aliases, list):
            raise CatalogValidationError(f"Item {item_id} aliases must be a list.")

        for alias in aliases:
            if not isinstance(alias, str) or not alias.strip():
                raise CatalogValidationError(f"Item {item_id} has invalid alias: {alias!r}")


def find_duplicate_aliases(items: list[dict[str, Any]]) -> dict[str, list[str]]:
    alias_map: dict[str, list[str]] = defaultdict(list)

    for item in items:
        item_id = item["id"]
        for alias in item["aliases"]:
            alias_map[normalize_alias(alias)].append(item_id)

    return {
        alias: sorted(set(item_ids))
        for alias, item_ids in alias_map.items()
        if len(set(item_ids)) > 1
    }


def validate_no_duplicate_aliases(items: list[dict[str, Any]]) -> None:
    duplicates = find_duplicate_aliases(items)
    if duplicates:
        raise CatalogValidationError(f"Duplicate aliases detected: {duplicates}")


def validate_catalog_seed(seed: dict[str, Any]) -> None:
    validate_seed_metadata(seed)
    items = collect_seed_items(seed)
    validate_required_item_fields(items)
    validate_item_status_values(items)
    validate_unique_item_ids(items)
    validate_alias_lists(items)
    validate_no_duplicate_aliases(items)


def validate_component_catalog(section: str, catalog: dict[str, Any]) -> None:
    if catalog.get("catalog_type") != section:
        raise CatalogValidationError(
            f"Component catalog type mismatch: expected {section}, "
            f"got {catalog.get('catalog_type')}"
        )

    metadata = catalog.get("metadata")
    if not isinstance(metadata, dict):
        raise CatalogValidationError(f"Component catalog {section} must contain metadata.")

    for key, expected in EXPECTED_SEED_STATUS.items():
        if metadata.get(key) != expected:
            raise CatalogValidationError(
                f"Component catalog {section} metadata {key} must be {expected}"
            )

    items = catalog.get("items")
    if not isinstance(items, list):
        raise CatalogValidationError(f"Component catalog {section} items must be a list.")

    section_items = [dict(item, _section=section) for item in items]
    validate_required_item_fields(section_items)
    validate_item_status_values(section_items)
    validate_unique_item_ids(section_items)
    validate_alias_lists(section_items)
    validate_no_duplicate_aliases(section_items)