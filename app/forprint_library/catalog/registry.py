from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from forprint_library.catalog.loader import load_seed
from forprint_library.catalog.validation import (
    collect_seed_items,
    normalize_alias,
    validate_catalog_seed,
)


@dataclass(frozen=True)
class CatalogLookupResult:
    item_id: str
    section: str
    item: dict[str, Any]


class CatalogRegistry:
    def __init__(self, seed: dict[str, Any]) -> None:
        validate_catalog_seed(seed)
        self._seed = seed
        self._items = collect_seed_items(seed)
        self._by_id = {item["id"]: item for item in self._items}
        self._aliases = self._build_alias_index(self._items)

    @classmethod
    def from_project(cls) -> CatalogRegistry:
        return cls(load_seed())

    @property
    def seed_metadata(self) -> dict[str, Any]:
        return dict(self._seed["metadata"])

    def list_items(self) -> list[dict[str, Any]]:
        return [dict(item) for item in self._items]

    def get(self, item_id: str) -> CatalogLookupResult | None:
        item = self._by_id.get(item_id)
        if item is None:
            return None

        return CatalogLookupResult(
            item_id=item["id"],
            section=item["_section"],
            item=dict(item),
        )

    def resolve_alias(self, alias: str) -> CatalogLookupResult | None:
        normalized = normalize_alias(alias)
        item_id = self._aliases.get(normalized)
        if item_id is None:
            return None

        return self.get(item_id)

    @staticmethod
    def _build_alias_index(items: list[dict[str, Any]]) -> dict[str, str]:
        alias_index: dict[str, str] = {}

        for item in items:
            for alias in item["aliases"]:
                normalized = normalize_alias(alias)
                alias_index[normalized] = item["id"]

        return alias_index