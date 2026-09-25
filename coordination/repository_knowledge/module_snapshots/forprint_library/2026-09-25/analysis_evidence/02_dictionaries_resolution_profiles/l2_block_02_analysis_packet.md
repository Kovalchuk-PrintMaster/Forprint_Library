# ForPrint Library — L2 Block 02 Analysis Packet

**Module:** `forprint_library`
**Block:** `02_dictionaries_resolution_profiles`

This packet is evidence for analysis only. It is not implementation authority.

## Evidence boundaries

- Primary implementation population comes from the human-reviewed L1 block manifest.
- Related tests come only from L1 secondary relationships.
- Block 01 analysis is supporting cross-block evidence, not authority over Block 02.
- Blueprint material is authority/planning/provenance context, not implementation proof.
- Historical evidence remains provenance unless current implementation confirms it.

# Part A — Block manifest

## L1 Block 02 manifest

**Path:** `tmp/module_knowledge_analysis/forprint_library/02_dictionaries_resolution_profiles/manifest.yaml`
**SHA256:** `bc7588a41fccaacb8e375ff2a067b7ebd396bc1a1c3def68bcfb2c8307abfbbe`

```yaml
schema_version: forprint_module_knowledge_analysis_block_manifest_v0_1
module_id: forprint_library
stage: L1_INVENTORY_AND_SEGMENTATION
block_id: 02_dictionaries_resolution_profiles
title: Dictionaries, resolution and naming profiles
purpose: Shared dictionaries, reference resolution, units, statuses/types, aliases, tokens and profile-aware naming semantics.
mutation_performed: false
selection_method: L1 deterministic classification plus bounded human review correction v0.1; classification remains preliminary
  until L2 analysis
file_count: 36
source_paths:
- app/forprint_library/catalog/registry.py
- app/forprint_library/dictionaries/__init__.py
- app/forprint_library/dictionaries/loader.py
- app/forprint_library/dictionaries/models.py
- app/forprint_library/dictionaries/resolver.py
- app/forprint_library/dictionaries/validation.py
- app/forprint_library/semantic/__init__.py
- app/forprint_library/semantic/aliases.py
- app/forprint_library/semantic/resolver.py
- dictionaries/alert_event_status.yaml
- dictionaries/alert_rule_type.yaml
- dictionaries/alert_severity.yaml
- dictionaries/contractor_reference_status.yaml
- dictionaries/deadline_type.yaml
- dictionaries/entity_type.yaml
- dictionaries/material_requirement_status.yaml
- dictionaries/notification_status.yaml
- dictionaries/order_line_status.yaml
- dictionaries/order_status.yaml
- dictionaries/payment_status.yaml
- dictionaries/product_service_reference_status.yaml
- dictionaries/production_status.yaml
- dictionaries/reference_resolution_status.yaml
- dictionaries/shared_operational_dictionary_v0_1.yaml
- dictionaries/source_system.yaml
- dictionaries/unit.yaml
- dictionaries/workflow_stage_status.yaml
- dictionaries/workflow_status.yaml
- schemas/dictionary_entry.schema.yaml
- schemas/shared_operational_dictionary.schema.yaml
- scripts/export_dictionary_policy_docs.py
- scripts/export_shared_dictionary_coordination_artifacts.py
- scripts/export_shared_operational_dictionaries.py
- scripts/preview_shared_operational_dictionaries.py
- scripts/reference_contract/validate_library_reference_contract.py
- scripts/validate_shared_operational_dictionaries.py
primary_capability_hypotheses:
- shared semantic dictionaries
- reference resolution
- naming/token/profile semantics
cross_block_dependencies: []
documents_present: []
tests_present: []
generated_outputs_present: []
legacy_candidates_present:
- scripts/export_dictionary_policy_docs.py
unknowns: []
confidence: medium
```

# Part B — Primary source population

## Primary source

**Path:** `app/forprint_library/catalog/registry.py`
**SHA256:** `4accda5226cfcb36b5479dd867e70bff4e3a42ae3acc0200f9a88c78ca924122`

```python
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
```

## Primary source

**Path:** `app/forprint_library/dictionaries/__init__.py`
**SHA256:** `7f569dd948289aa54125ed16a669a409c1b8946a642f6ec471aa4ddbecb9f968`

```python
from __future__ import annotations

from forprint_library.dictionaries.loader import (
    list_dictionary_groups,
    load_dictionary,
    load_shared_dictionary,
)
from forprint_library.dictionaries.resolver import (
    find_ambiguous_aliases,
    resolve_dictionary_value,
)
from forprint_library.dictionaries.validation import (
    validate_dictionary_entry,
    validate_shared_dictionary,
)

__all__ = [
    "find_ambiguous_aliases",
    "list_dictionary_groups",
    "load_dictionary",
    "load_shared_dictionary",
    "resolve_dictionary_value",
    "validate_dictionary_entry",
    "validate_shared_dictionary",
]
```

## Primary source

**Path:** `app/forprint_library/dictionaries/loader.py`
**SHA256:** `b7ae36524531b2a3a12fd5ca7797655654a0265d409b3855d437fe4c853fe970`

```python
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from forprint_library.dictionaries.models import (
    DICTIONARY_FILES,
    DICTIONARY_GROUPS,
    SHARED_DICTIONARY_FILE,
)

PROJECT_ROOT = Path(__file__).resolve().parents[3]


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML file must contain a mapping: {path}")

    return data


def load_shared_dictionary(project_root: Path | None = None) -> dict[str, Any]:
    root = project_root or PROJECT_ROOT
    return load_yaml(root / SHARED_DICTIONARY_FILE)


def load_dictionary(group_name: str, project_root: Path | None = None) -> dict[str, Any]:
    if group_name not in DICTIONARY_FILES:
        known_groups = ", ".join(DICTIONARY_GROUPS)
        raise KeyError(f"Unknown dictionary group: {group_name}. Known groups: {known_groups}")

    root = project_root or PROJECT_ROOT
    return load_yaml(root / DICTIONARY_FILES[group_name])


def load_all_dictionaries(project_root: Path | None = None) -> dict[str, dict[str, Any]]:
    return {
        group_name: load_dictionary(group_name, project_root=project_root)
        for group_name in DICTIONARY_GROUPS
    }


def list_dictionary_groups() -> list[str]:
    return list(DICTIONARY_GROUPS)
```

## Primary source

**Path:** `app/forprint_library/dictionaries/models.py`
**SHA256:** `e2cca60a2b9188438bbf518ceb677071124629b306c7703742c76fb60392ee59`

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

DICTIONARY_VERSION = "0.1"

DICTIONARY_GROUPS: tuple[str, ...] = (
    "source_system",
    "entity_type",
    "order_status",
    "order_line_status",
    "payment_status",
    "production_status",
    "workflow_status",
    "workflow_stage_status",
    "material_requirement_status",
    "reference_resolution_status",
    "product_service_reference_status",
    "contractor_reference_status",
    "deadline_type",
    "alert_rule_type",
    "alert_severity",
    "alert_event_status",
    "notification_status",
    "unit",
)

DICTIONARY_FILES: dict[str, str] = {
    group: f"dictionaries/{group}.yaml" for group in DICTIONARY_GROUPS
}

SHARED_DICTIONARY_FILE = "dictionaries/shared_operational_dictionary_v0_1.yaml"

REQUIRED_DICTIONARY_ENTRY_FIELDS: tuple[str, ...] = (
    "id",
    "label_uk",
    "label_en",
    "description",
    "status",
    "aliases",
    "owner_module",
    "dictionary_group",
    "version",
    "notes",
)

REQUIRED_SHARED_METADATA_FIELDS: tuple[str, ...] = (
    "id",
    "version",
    "dictionary_status",
    "schema_status",
    "usage",
    "contract_status",
    "owner_module",
)

EXPECTED_SHARED_METADATA: dict[str, str] = {
    "dictionary_status": "draft_shared_operational_dictionary_v0_1",
    "schema_status": "unstable_v0_1",
    "usage": "allowed_for_projection_use",
    "contract_status": "not_final_contract",
    "owner_module": "forprint_library",
}

ALLOWED_ENTRY_STATUSES: set[str] = {
    "active",
    "draft",
    "deprecated",
}

RESOLUTION_EXACT = "confirmed"
RESOLUTION_ALIAS = "confirmed_with_alias"
RESOLUTION_UNRESOLVED = "unresolved"
RESOLUTION_AMBIGUOUS = "ambiguous_manual_review_required"
RESOLUTION_DEPRECATED = "deprecated_reference"


class DictionaryValidationError(ValueError):
    """Raised when a shared operational dictionary is invalid."""


@dataclass(frozen=True)
class DictionaryResolutionResult:
    group_name: str
    input_value: str
    status: str
    matched_id: str | None
    matched_by: str | None
    entry: dict[str, Any] | None
    candidates: list[str]

    @property
    def is_resolved(self) -> bool:
        return self.status in {
            RESOLUTION_EXACT,
            RESOLUTION_ALIAS,
            RESOLUTION_DEPRECATED,
        }
```

## Primary source

**Path:** `app/forprint_library/dictionaries/resolver.py`
**SHA256:** `189e7c59f1317fa52cece0c9e82bc629781507160c655024d77270cac534d386`

```python
from __future__ import annotations

from collections import defaultdict
from typing import Any

from forprint_library.dictionaries.loader import load_dictionary
from forprint_library.dictionaries.models import (
    RESOLUTION_ALIAS,
    RESOLUTION_AMBIGUOUS,
    RESOLUTION_DEPRECATED,
    RESOLUTION_EXACT,
    RESOLUTION_UNRESOLVED,
    DictionaryResolutionResult,
)
from forprint_library.dictionaries.validation import normalize_dictionary_lookup_value


def resolve_dictionary_value(
    group_name: str,
    value_or_alias: str,
    dictionary: dict[str, Any] | None = None,
) -> DictionaryResolutionResult:
    active_dictionary = dictionary or load_dictionary(group_name)
    entries = active_dictionary.get("entries", [])

    normalized_input = normalize_dictionary_lookup_value(value_or_alias)

    for entry in entries:
        if normalize_dictionary_lookup_value(entry["id"]) == normalized_input:
            if entry["status"] == "deprecated":
                return DictionaryResolutionResult(
                    group_name=group_name,
                    input_value=value_or_alias,
                    status=RESOLUTION_DEPRECATED,
                    matched_id=entry["id"],
                    matched_by="id",
                    entry=dict(entry),
                    candidates=[entry["id"]],
                )

            return DictionaryResolutionResult(
                group_name=group_name,
                input_value=value_or_alias,
                status=RESOLUTION_EXACT,
                matched_id=entry["id"],
                matched_by="id",
                entry=dict(entry),
                candidates=[entry["id"]],
            )

    alias_matches: dict[str, dict[str, Any]] = {}
    for entry in entries:
        for alias in entry["aliases"]:
            if normalize_dictionary_lookup_value(alias) == normalized_input:
                alias_matches[entry["id"]] = entry

    if len(alias_matches) > 1:
        return DictionaryResolutionResult(
            group_name=group_name,
            input_value=value_or_alias,
            status=RESOLUTION_AMBIGUOUS,
            matched_id=None,
            matched_by="alias",
            entry=None,
            candidates=sorted(alias_matches),
        )

    if len(alias_matches) == 1:
        entry = next(iter(alias_matches.values()))
        if entry["status"] == "deprecated":
            return DictionaryResolutionResult(
                group_name=group_name,
                input_value=value_or_alias,
                status=RESOLUTION_DEPRECATED,
                matched_id=entry["id"],
                matched_by="alias",
                entry=dict(entry),
                candidates=[entry["id"]],
            )

        return DictionaryResolutionResult(
            group_name=group_name,
            input_value=value_or_alias,
            status=RESOLUTION_ALIAS,
            matched_id=entry["id"],
            matched_by="alias",
            entry=dict(entry),
            candidates=[entry["id"]],
        )

    return DictionaryResolutionResult(
        group_name=group_name,
        input_value=value_or_alias,
        status=RESOLUTION_UNRESOLVED,
        matched_id=None,
        matched_by=None,
        entry=None,
        candidates=[],
    )


def find_ambiguous_aliases(dictionary: dict[str, Any]) -> dict[str, list[str]]:
    alias_map: dict[str, list[str]] = defaultdict(list)

    for entry in dictionary.get("entries", []):
        for alias in entry["aliases"]:
            alias_map[normalize_dictionary_lookup_value(alias)].append(entry["id"])

    return {
        alias: sorted(set(entry_ids))
        for alias, entry_ids in alias_map.items()
        if len(set(entry_ids)) > 1
    }
```

## Primary source

**Path:** `app/forprint_library/dictionaries/validation.py`
**SHA256:** `484a9539f2970a4c97c08ff9e8dcf1ffe8b13df701898991325da806f4cd9a70`

```python
from __future__ import annotations

from collections import defaultdict
from typing import Any

from forprint_library.dictionaries.models import (
    ALLOWED_ENTRY_STATUSES,
    DICTIONARY_GROUPS,
    EXPECTED_SHARED_METADATA,
    REQUIRED_DICTIONARY_ENTRY_FIELDS,
    REQUIRED_SHARED_METADATA_FIELDS,
    DictionaryValidationError,
)


def normalize_dictionary_lookup_value(value: str) -> str:
    return " ".join(value.casefold().strip().split())


def collect_shared_dictionary_entries(shared_dictionary: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []

    groups = shared_dictionary.get("dictionary_groups")
    if not isinstance(groups, dict):
        raise DictionaryValidationError("Shared dictionary must contain dictionary_groups mapping.")

    for group_name in DICTIONARY_GROUPS:
        group_entries = groups.get(group_name)
        if not isinstance(group_entries, list):
            raise DictionaryValidationError(f"Dictionary group must be a list: {group_name}")

        for entry in group_entries:
            if not isinstance(entry, dict):
                raise DictionaryValidationError(
                    f"Dictionary entry must be a mapping in group: {group_name}"
                )

            entries.append(dict(entry))

    return entries


def validate_shared_metadata(shared_dictionary: dict[str, Any]) -> None:
    metadata = shared_dictionary.get("metadata")
    if not isinstance(metadata, dict):
        raise DictionaryValidationError("Shared dictionary must contain metadata mapping.")

    missing = [field for field in REQUIRED_SHARED_METADATA_FIELDS if field not in metadata]
    if missing:
        raise DictionaryValidationError(f"Shared dictionary metadata missing fields: {missing}")

    mismatched = {
        key: {"expected": expected, "actual": metadata.get(key)}
        for key, expected in EXPECTED_SHARED_METADATA.items()
        if metadata.get(key) != expected
    }
    if mismatched:
        raise DictionaryValidationError(
            f"Shared dictionary metadata has unexpected values: {mismatched}"
        )


def validate_dictionary_entry(entry: dict[str, Any], expected_group: str | None = None) -> None:
    missing = [field for field in REQUIRED_DICTIONARY_ENTRY_FIELDS if field not in entry]
    if missing:
        entry_id = entry.get("id", "<missing-id>")
        raise DictionaryValidationError(f"Dictionary entry {entry_id} missing fields: {missing}")

    entry_id = entry["id"]

    if not isinstance(entry_id, str) or not entry_id.strip():
        raise DictionaryValidationError("Dictionary entry id must be a non-empty string.")

    if entry["status"] not in ALLOWED_ENTRY_STATUSES:
        raise DictionaryValidationError(
            f"Dictionary entry {entry_id} has unsupported status: {entry['status']}"
        )

    if not isinstance(entry["aliases"], list):
        raise DictionaryValidationError(f"Dictionary entry {entry_id} aliases must be a list.")

    for alias in entry["aliases"]:
        if not isinstance(alias, str) or not alias.strip():
            raise DictionaryValidationError(
                f"Dictionary entry {entry_id} contains invalid alias: {alias!r}"
            )

    if entry["owner_module"] != "forprint_library":
        raise DictionaryValidationError(
            f"Dictionary entry {entry_id} must be owned by forprint_library."
        )

    if entry["version"] != "0.1":
        raise DictionaryValidationError(f"Dictionary entry {entry_id} must use version 0.1.")

    if expected_group is not None and entry["dictionary_group"] != expected_group:
        raise DictionaryValidationError(
            f"Dictionary entry {entry_id} group mismatch: "
            f"expected {expected_group}, got {entry['dictionary_group']}"
        )


def validate_dictionary_group(group_name: str, dictionary: dict[str, Any]) -> None:
    if dictionary.get("dictionary_group") != group_name:
        raise DictionaryValidationError(
            f"Dictionary group mismatch: expected {group_name}, "
            f"got {dictionary.get('dictionary_group')}"
        )

    metadata = dictionary.get("metadata")
    if not isinstance(metadata, dict):
        raise DictionaryValidationError(f"Dictionary {group_name} must contain metadata.")

    entries = dictionary.get("entries")
    if not isinstance(entries, list):
        raise DictionaryValidationError(f"Dictionary {group_name} entries must be a list.")

    seen_ids: set[str] = set()
    for entry in entries:
        validate_dictionary_entry(entry, expected_group=group_name)

        entry_id = entry["id"]
        if entry_id in seen_ids:
            raise DictionaryValidationError(
                f"Duplicate dictionary entry id in {group_name}: {entry_id}"
            )
        seen_ids.add(entry_id)


def find_duplicate_aliases(entries: list[dict[str, Any]]) -> dict[str, list[str]]:
    alias_map: dict[str, list[str]] = defaultdict(list)

    for entry in entries:
        entry_id = entry["id"]
        group_name = entry["dictionary_group"]
        for alias in entry["aliases"]:
            alias_map[f"{group_name}:{normalize_dictionary_lookup_value(alias)}"].append(
                entry_id
            )

    return {
        alias_key: sorted(set(entry_ids))
        for alias_key, entry_ids in alias_map.items()
        if len(set(entry_ids)) > 1
    }


def validate_no_duplicate_ids_within_groups(entries: list[dict[str, Any]]) -> None:
    ids_by_group: dict[str, set[str]] = defaultdict(set)

    for entry in entries:
        group_name = entry["dictionary_group"]
        entry_id = entry["id"]

        if entry_id in ids_by_group[group_name]:
            raise DictionaryValidationError(
                f"Duplicate dictionary entry id in {group_name}: {entry_id}"
            )

        ids_by_group[group_name].add(entry_id)


def validate_shared_dictionary(shared_dictionary: dict[str, Any]) -> None:
    validate_shared_metadata(shared_dictionary)
    entries = collect_shared_dictionary_entries(shared_dictionary)

    for entry in entries:
        validate_dictionary_entry(entry, expected_group=entry["dictionary_group"])

    validate_no_duplicate_ids_within_groups(entries)

    duplicates = find_duplicate_aliases(entries)
    if duplicates:
        raise DictionaryValidationError(f"Duplicate dictionary aliases detected: {duplicates}")
```

## Primary source

**Path:** `app/forprint_library/semantic/__init__.py`
**SHA256:** `6e5931da8e86c5ab2005f59adbf92ceb08ab443b22a4bc0b9faca2e59cb6ce9e`

```python
from __future__ import annotations

from forprint_library.semantic.aliases import normalize_semantic_alias

__all__ = ["normalize_semantic_alias"]
```

## Primary source

**Path:** `app/forprint_library/semantic/aliases.py`
**SHA256:** `1011b9cec07be2a87eab3975a88d1620f0e643e1c3776933c8bd3f9dcf51b4ec`

```python
from __future__ import annotations


def normalize_semantic_alias(value: str) -> str:
    return " ".join(value.casefold().strip().split())
```

## Primary source

**Path:** `app/forprint_library/semantic/resolver.py`
**SHA256:** `ca3c504ec1773b0f160ea2fb77c6c10f18fd81bf8c86fec26cb28d3fdc121e76`

```python
from __future__ import annotations

from forprint_library.catalog.registry import CatalogLookupResult, CatalogRegistry


def resolve_catalog_alias(alias: str, 
                          registry: CatalogRegistry | None = None) -> CatalogLookupResult | None:
    active_registry = registry or CatalogRegistry.from_project()
    return active_registry.resolve_alias(alias)
```

## Primary source

**Path:** `dictionaries/alert_event_status.yaml`
**SHA256:** `a23bb774b111f59466aae469e088dc7d63cb57748f09a5467bb6c08510f6f11c`

```yaml
dictionary_group: alert_event_status
metadata:
  id: shared_operational_dictionary_v0_1
  name: Shared Operational Dictionary v0.1
  version: '0.1'
  dictionary_status: draft_shared_operational_dictionary_v0_1
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  unit_dictionary_status: not_final_inventory_unit_system
entries:
- id: open
  label_uk: Відкрито
  label_en: Open
  description: Canonical shared operational dictionary value 'open' for dictionary
    group 'alert_event_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: alert_event_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: acknowledged
  label_uk: Підтверджено оператором
  label_en: Acknowledged
  description: Canonical shared operational dictionary value 'acknowledged' for dictionary
    group 'alert_event_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: alert_event_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: resolved
  label_uk: Вирішено
  label_en: Resolved
  description: Canonical shared operational dictionary value 'resolved' for dictionary
    group 'alert_event_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: alert_event_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: ignored
  label_uk: Проігноровано
  label_en: Ignored
  description: Canonical shared operational dictionary value 'ignored' for dictionary
    group 'alert_event_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: alert_event_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: failed_to_notify
  label_uk: Failed To Notify
  label_en: Failed To Notify
  description: Canonical shared operational dictionary value 'failed_to_notify' for
    dictionary group 'alert_event_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: alert_event_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: unknown
  label_uk: Невідомо
  label_en: Unknown
  description: Canonical shared operational dictionary value 'unknown' for dictionary
    group 'alert_event_status'.
  status: active
  aliases:
  - невідомо
  owner_module: forprint_library
  dictionary_group: alert_event_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
```

## Primary source

**Path:** `dictionaries/alert_rule_type.yaml`
**SHA256:** `14d8dd7a8c4213f3f362f74dc68f00398f6de43acf12754b111ca7ea52358793`

```yaml
dictionary_group: alert_rule_type
metadata:
  id: shared_operational_dictionary_v0_1
  name: Shared Operational Dictionary v0.1
  version: '0.1'
  dictionary_status: draft_shared_operational_dictionary_v0_1
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  unit_dictionary_status: not_final_inventory_unit_system
entries:
- id: workflow_stage_late
  label_uk: Workflow Stage Late
  label_en: Workflow Stage Late
  description: Canonical shared operational dictionary value 'workflow_stage_late'
    for dictionary group 'alert_rule_type'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: alert_rule_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: order_deadline_near
  label_uk: Order Deadline Near
  label_en: Order Deadline Near
  description: Canonical shared operational dictionary value 'order_deadline_near'
    for dictionary group 'alert_rule_type'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: alert_rule_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: payment_overdue
  label_uk: Payment Overdue
  label_en: Payment Overdue
  description: Canonical shared operational dictionary value 'payment_overdue' for
    dictionary group 'alert_rule_type'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: alert_rule_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: material_requirement_unresolved
  label_uk: Material Requirement Unresolved
  label_en: Material Requirement Unresolved
  description: Canonical shared operational dictionary value 'material_requirement_unresolved'
    for dictionary group 'alert_rule_type'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: alert_rule_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: manual_review_stale
  label_uk: Manual Review Stale
  label_en: Manual Review Stale
  description: Canonical shared operational dictionary value 'manual_review_stale'
    for dictionary group 'alert_rule_type'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: alert_rule_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: contractor_stage_blocked
  label_uk: Contractor Stage Blocked
  label_en: Contractor Stage Blocked
  description: Canonical shared operational dictionary value 'contractor_stage_blocked'
    for dictionary group 'alert_rule_type'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: alert_rule_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: unknown
  label_uk: Невідомо
  label_en: Unknown
  description: Canonical shared operational dictionary value 'unknown' for dictionary
    group 'alert_rule_type'.
  status: active
  aliases:
  - невідомо
  owner_module: forprint_library
  dictionary_group: alert_rule_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
```

## Primary source

**Path:** `dictionaries/alert_severity.yaml`
**SHA256:** `c8ba973ece4ba1d75f6844807094552a410cb17923baff3e72030c9611f58f8f`

```yaml
dictionary_group: alert_severity
metadata:
  id: shared_operational_dictionary_v0_1
  name: Shared Operational Dictionary v0.1
  version: '0.1'
  dictionary_status: draft_shared_operational_dictionary_v0_1
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  unit_dictionary_status: not_final_inventory_unit_system
entries:
- id: info
  label_uk: Інформаційно
  label_en: Info
  description: Canonical shared operational dictionary value 'info' for dictionary
    group 'alert_severity'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: alert_severity
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: warning
  label_uk: Попередження
  label_en: Warning
  description: Canonical shared operational dictionary value 'warning' for dictionary
    group 'alert_severity'.
  status: active
  aliases:
  - warn
  owner_module: forprint_library
  dictionary_group: alert_severity
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: high
  label_uk: Високий
  label_en: High
  description: Canonical shared operational dictionary value 'high' for dictionary
    group 'alert_severity'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: alert_severity
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: critical
  label_uk: Критичний
  label_en: Critical
  description: Canonical shared operational dictionary value 'critical' for dictionary
    group 'alert_severity'.
  status: active
  aliases:
  - crit
  owner_module: forprint_library
  dictionary_group: alert_severity
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: unknown
  label_uk: Невідомо
  label_en: Unknown
  description: Canonical shared operational dictionary value 'unknown' for dictionary
    group 'alert_severity'.
  status: active
  aliases:
  - невідомо
  owner_module: forprint_library
  dictionary_group: alert_severity
  version: '0.1'
  notes: Draft shared operational dictionary entry.
```

## Primary source

**Path:** `dictionaries/contractor_reference_status.yaml`
**SHA256:** `825161ec4fa623013d6ff096e5a1ed8eb98262cd8297bbc0b013af19fcd2d5a0`

```yaml
dictionary_group: contractor_reference_status
metadata:
  id: shared_operational_dictionary_v0_1
  name: Shared Operational Dictionary v0.1
  version: '0.1'
  dictionary_status: draft_shared_operational_dictionary_v0_1
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  unit_dictionary_status: not_final_inventory_unit_system
entries:
- id: display_only
  label_uk: Display Only
  label_en: Display Only
  description: Canonical shared operational dictionary value 'display_only' for dictionary
    group 'contractor_reference_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: contractor_reference_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: client_account_reference_pending
  label_uk: Client Account Reference Pending
  label_en: Client Account Reference Pending
  description: Canonical shared operational dictionary value 'client_account_reference_pending'
    for dictionary group 'contractor_reference_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: contractor_reference_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: client_account_reference_confirmed
  label_uk: Client Account Reference Confirmed
  label_en: Client Account Reference Confirmed
  description: Canonical shared operational dictionary value 'client_account_reference_confirmed'
    for dictionary group 'contractor_reference_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: contractor_reference_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: external_reference_pending
  label_uk: External Reference Pending
  label_en: External Reference Pending
  description: Canonical shared operational dictionary value 'external_reference_pending'
    for dictionary group 'contractor_reference_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: contractor_reference_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: manual_review_required
  label_uk: Потрібна ручна перевірка
  label_en: Manual Review Required
  description: Canonical shared operational dictionary value 'manual_review_required'
    for dictionary group 'contractor_reference_status'.
  status: active
  aliases:
  - manual_review
  - ручна перевірка
  owner_module: forprint_library
  dictionary_group: contractor_reference_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: unknown
  label_uk: Невідомо
  label_en: Unknown
  description: Canonical shared operational dictionary value 'unknown' for dictionary
    group 'contractor_reference_status'.
  status: active
  aliases:
  - невідомо
  owner_module: forprint_library
  dictionary_group: contractor_reference_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
```

## Primary source

**Path:** `dictionaries/deadline_type.yaml`
**SHA256:** `7d395319aef94d965d85a2206d40a1ca7566088862e634562500f0d35058d288`

```yaml
dictionary_group: deadline_type
metadata:
  id: shared_operational_dictionary_v0_1
  name: Shared Operational Dictionary v0.1
  version: '0.1'
  dictionary_status: draft_shared_operational_dictionary_v0_1
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  unit_dictionary_status: not_final_inventory_unit_system
entries:
- id: order_due
  label_uk: Order Due
  label_en: Order Due
  description: Canonical shared operational dictionary value 'order_due' for dictionary
    group 'deadline_type'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: deadline_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: stage_due
  label_uk: Stage Due
  label_en: Stage Due
  description: Canonical shared operational dictionary value 'stage_due' for dictionary
    group 'deadline_type'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: deadline_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: payment_due
  label_uk: Payment Due
  label_en: Payment Due
  description: Canonical shared operational dictionary value 'payment_due' for dictionary
    group 'deadline_type'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: deadline_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: material_required_by
  label_uk: Material Required By
  label_en: Material Required By
  description: Canonical shared operational dictionary value 'material_required_by'
    for dictionary group 'deadline_type'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: deadline_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: manual_review_due
  label_uk: Manual Review Due
  label_en: Manual Review Due
  description: Canonical shared operational dictionary value 'manual_review_due' for
    dictionary group 'deadline_type'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: deadline_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: unknown
  label_uk: Невідомо
  label_en: Unknown
  description: Canonical shared operational dictionary value 'unknown' for dictionary
    group 'deadline_type'.
  status: active
  aliases:
  - невідомо
  owner_module: forprint_library
  dictionary_group: deadline_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
```

## Primary source

**Path:** `dictionaries/entity_type.yaml`
**SHA256:** `2337bdaee655906f5aae179c63d3051c278a3808d8a75b4e840a0449b11d9165`

```yaml
dictionary_group: entity_type
metadata:
  id: shared_operational_dictionary_v0_1
  name: Shared Operational Dictionary v0.1
  version: '0.1'
  dictionary_status: draft_shared_operational_dictionary_v0_1
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  unit_dictionary_status: not_final_inventory_unit_system
entries:
- id: client_account
  label_uk: Client Account
  label_en: Client Account
  description: Canonical shared operational dictionary value 'client_account' for
    dictionary group 'entity_type'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: entity_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: client_group
  label_uk: Client Group
  label_en: Client Group
  description: Canonical shared operational dictionary value 'client_group' for dictionary
    group 'entity_type'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: entity_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: contact_person
  label_uk: Contact Person
  label_en: Contact Person
  description: Canonical shared operational dictionary value 'contact_person' for
    dictionary group 'entity_type'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: entity_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: contact_method
  label_uk: Contact Method
  label_en: Contact Method
  description: Canonical shared operational dictionary value 'contact_method' for
    dictionary group 'entity_type'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: entity_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: client_address
  label_uk: Client Address
  label_en: Client Address
  description: Canonical shared operational dictionary value 'client_address' for
    dictionary group 'entity_type'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: entity_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: legal_entity_profile
  label_uk: Legal Entity Profile
  label_en: Legal Entity Profile
  description: Canonical shared operational dictionary value 'legal_entity_profile'
    for dictionary group 'entity_type'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: entity_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: external_reference
  label_uk: External Reference
  label_en: External Reference
  description: Canonical shared operational dictionary value 'external_reference'
    for dictionary group 'entity_type'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: entity_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: order
  label_uk: Order
  label_en: Order
  description: Canonical shared operational dictionary value 'order' for dictionary
    group 'entity_type'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: entity_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: order_line
  label_uk: Order Line
  label_en: Order Line
  description: Canonical shared operational dictionary value 'order_line' for dictionary
    group 'entity_type'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: entity_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: calculator_output_package
  label_uk: Calculator Output Package
  label_en: Calculator Output Package
  description: Canonical shared operational dictionary value 'calculator_output_package'
    for dictionary group 'entity_type'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: entity_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: product_service_reference
  label_uk: Product Service Reference
  label_en: Product Service Reference
  description: Canonical shared operational dictionary value 'product_service_reference'
    for dictionary group 'entity_type'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: entity_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: material_requirement
  label_uk: Material Requirement
  label_en: Material Requirement
  description: Canonical shared operational dictionary value 'material_requirement'
    for dictionary group 'entity_type'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: entity_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: payment_projection
  label_uk: Payment Projection
  label_en: Payment Projection
  description: Canonical shared operational dictionary value 'payment_projection'
    for dictionary group 'entity_type'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: entity_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: workflow_template
  label_uk: Workflow Template
  label_en: Workflow Template
  description: Canonical shared operational dictionary value 'workflow_template' for
    dictionary group 'entity_type'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: entity_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: workflow_stage
  label_uk: Workflow Stage
  label_en: Workflow Stage
  description: Canonical shared operational dictionary value 'workflow_stage' for
    dictionary group 'entity_type'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: entity_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: deadline_control
  label_uk: Deadline Control
  label_en: Deadline Control
  description: Canonical shared operational dictionary value 'deadline_control' for
    dictionary group 'entity_type'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: entity_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: contractor_reference
  label_uk: Contractor Reference
  label_en: Contractor Reference
  description: Canonical shared operational dictionary value 'contractor_reference'
    for dictionary group 'entity_type'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: entity_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: alert_rule
  label_uk: Alert Rule
  label_en: Alert Rule
  description: Canonical shared operational dictionary value 'alert_rule' for dictionary
    group 'entity_type'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: entity_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: alert_event
  label_uk: Alert Event
  label_en: Alert Event
  description: Canonical shared operational dictionary value 'alert_event' for dictionary
    group 'entity_type'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: entity_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: report_definition
  label_uk: Report Definition
  label_en: Report Definition
  description: Canonical shared operational dictionary value 'report_definition' for
    dictionary group 'entity_type'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: entity_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: report_projection
  label_uk: Report Projection
  label_en: Report Projection
  description: Canonical shared operational dictionary value 'report_projection' for
    dictionary group 'entity_type'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: entity_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: operational_event
  label_uk: Operational Event
  label_en: Operational Event
  description: Canonical shared operational dictionary value 'operational_event' for
    dictionary group 'entity_type'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: entity_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: unknown
  label_uk: Невідомо
  label_en: Unknown
  description: Canonical shared operational dictionary value 'unknown' for dictionary
    group 'entity_type'.
  status: active
  aliases:
  - невідомо
  owner_module: forprint_library
  dictionary_group: entity_type
  version: '0.1'
  notes: Draft shared operational dictionary entry.
```

## Primary source

**Path:** `dictionaries/material_requirement_status.yaml`
**SHA256:** `68c49b1fd2ea2977fd5fec9d14d29ab8daf4552c0f5269928d623e76d2f39115`

```yaml
dictionary_group: material_requirement_status
metadata:
  id: shared_operational_dictionary_v0_1
  name: Shared Operational Dictionary v0.1
  version: '0.1'
  dictionary_status: draft_shared_operational_dictionary_v0_1
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  unit_dictionary_status: not_final_inventory_unit_system
entries:
- id: planned
  label_uk: Заплановано
  label_en: Planned
  description: Canonical shared operational dictionary value 'planned' for dictionary
    group 'material_requirement_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: material_requirement_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: library_reference_pending
  label_uk: Library Reference Pending
  label_en: Library Reference Pending
  description: Canonical shared operational dictionary value 'library_reference_pending'
    for dictionary group 'material_requirement_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: material_requirement_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: warehouse_reference_pending
  label_uk: Warehouse Reference Pending
  label_en: Warehouse Reference Pending
  description: Canonical shared operational dictionary value 'warehouse_reference_pending'
    for dictionary group 'material_requirement_status'.
  status: active
  aliases:
  - warehouse_pending
  owner_module: forprint_library
  dictionary_group: material_requirement_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: reserved_reference_pending
  label_uk: Reserved Reference Pending
  label_en: Reserved Reference Pending
  description: Canonical shared operational dictionary value 'reserved_reference_pending'
    for dictionary group 'material_requirement_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: material_requirement_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: confirmed
  label_uk: Підтверджено
  label_en: Confirmed
  description: Canonical shared operational dictionary value 'confirmed' for dictionary
    group 'material_requirement_status'.
  status: active
  aliases:
  - підтверджено
  owner_module: forprint_library
  dictionary_group: material_requirement_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: fulfilled
  label_uk: Виконано
  label_en: Fulfilled
  description: Canonical shared operational dictionary value 'fulfilled' for dictionary
    group 'material_requirement_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: material_requirement_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: cancelled
  label_uk: Скасовано
  label_en: Cancelled
  description: Canonical shared operational dictionary value 'cancelled' for dictionary
    group 'material_requirement_status'.
  status: active
  aliases:
  - скасовано
  owner_module: forprint_library
  dictionary_group: material_requirement_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: unknown
  label_uk: Невідомо
  label_en: Unknown
  description: Canonical shared operational dictionary value 'unknown' for dictionary
    group 'material_requirement_status'.
  status: active
  aliases:
  - невідомо
  owner_module: forprint_library
  dictionary_group: material_requirement_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
```

## Primary source

**Path:** `dictionaries/notification_status.yaml`
**SHA256:** `6136157eb6d835ef4431a0e93dd1f24d6487bd8cba766485797d21e5699297fc`

```yaml
dictionary_group: notification_status
metadata:
  id: shared_operational_dictionary_v0_1
  name: Shared Operational Dictionary v0.1
  version: '0.1'
  dictionary_status: draft_shared_operational_dictionary_v0_1
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  unit_dictionary_status: not_final_inventory_unit_system
entries:
- id: not_sent
  label_uk: Не надіслано
  label_en: Not Sent
  description: Canonical shared operational dictionary value 'not_sent' for dictionary
    group 'notification_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: notification_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: queued
  label_uk: У черзі
  label_en: Queued
  description: Canonical shared operational dictionary value 'queued' for dictionary
    group 'notification_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: notification_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: sent
  label_uk: Надіслано
  label_en: Sent
  description: Canonical shared operational dictionary value 'sent' for dictionary
    group 'notification_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: notification_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: failed
  label_uk: Помилка
  label_en: Failed
  description: Canonical shared operational dictionary value 'failed' for dictionary
    group 'notification_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: notification_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: disabled
  label_uk: Вимкнено
  label_en: Disabled
  description: Canonical shared operational dictionary value 'disabled' for dictionary
    group 'notification_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: notification_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: unknown
  label_uk: Невідомо
  label_en: Unknown
  description: Canonical shared operational dictionary value 'unknown' for dictionary
    group 'notification_status'.
  status: active
  aliases:
  - невідомо
  owner_module: forprint_library
  dictionary_group: notification_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
```

## Primary source

**Path:** `dictionaries/order_line_status.yaml`
**SHA256:** `97c12139af6050761ae34773888e48e997c4af033c0786342393edd5544b9e03`

```yaml
dictionary_group: order_line_status
metadata:
  id: shared_operational_dictionary_v0_1
  name: Shared Operational Dictionary v0.1
  version: '0.1'
  dictionary_status: draft_shared_operational_dictionary_v0_1
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  unit_dictionary_status: not_final_inventory_unit_system
entries:
- id: draft
  label_uk: Чернетка
  label_en: Draft
  description: Canonical shared operational dictionary value 'draft' for dictionary
    group 'order_line_status'.
  status: active
  aliases:
  - чернетка
  owner_module: forprint_library
  dictionary_group: order_line_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: pending_reference_resolution
  label_uk: Pending Reference Resolution
  label_en: Pending Reference Resolution
  description: Canonical shared operational dictionary value 'pending_reference_resolution'
    for dictionary group 'order_line_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: order_line_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: ready
  label_uk: Готово
  label_en: Ready
  description: Canonical shared operational dictionary value 'ready' for dictionary
    group 'order_line_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: order_line_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: in_progress
  label_uk: У роботі
  label_en: In Progress
  description: Canonical shared operational dictionary value 'in_progress' for dictionary
    group 'order_line_status'.
  status: active
  aliases:
  - у роботі
  owner_module: forprint_library
  dictionary_group: order_line_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: completed
  label_uk: Завершено
  label_en: Completed
  description: Canonical shared operational dictionary value 'completed' for dictionary
    group 'order_line_status'.
  status: active
  aliases:
  - завершено
  owner_module: forprint_library
  dictionary_group: order_line_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: cancelled
  label_uk: Скасовано
  label_en: Cancelled
  description: Canonical shared operational dictionary value 'cancelled' for dictionary
    group 'order_line_status'.
  status: active
  aliases:
  - скасовано
  owner_module: forprint_library
  dictionary_group: order_line_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: manual_review_required
  label_uk: Потрібна ручна перевірка
  label_en: Manual Review Required
  description: Canonical shared operational dictionary value 'manual_review_required'
    for dictionary group 'order_line_status'.
  status: active
  aliases:
  - manual_review
  - ручна перевірка
  owner_module: forprint_library
  dictionary_group: order_line_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: unknown
  label_uk: Невідомо
  label_en: Unknown
  description: Canonical shared operational dictionary value 'unknown' for dictionary
    group 'order_line_status'.
  status: active
  aliases:
  - невідомо
  owner_module: forprint_library
  dictionary_group: order_line_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
```

## Primary source

**Path:** `dictionaries/order_status.yaml`
**SHA256:** `8dd44cd6067cf0aa612b38664edb3f491bd2a41ede53be2ace7fecc5f02e00a7`

```yaml
dictionary_group: order_status
metadata:
  id: shared_operational_dictionary_v0_1
  name: Shared Operational Dictionary v0.1
  version: '0.1'
  dictionary_status: draft_shared_operational_dictionary_v0_1
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  unit_dictionary_status: not_final_inventory_unit_system
entries:
- id: draft
  label_uk: Чернетка
  label_en: Draft
  description: Canonical shared operational dictionary value 'draft' for dictionary
    group 'order_status'.
  status: active
  aliases:
  - чернетка
  owner_module: forprint_library
  dictionary_group: order_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: needs_review
  label_uk: Потребує перевірки
  label_en: Needs Review
  description: Canonical shared operational dictionary value 'needs_review' for dictionary
    group 'order_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: order_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: confirmed
  label_uk: Підтверджено
  label_en: Confirmed
  description: Canonical shared operational dictionary value 'confirmed' for dictionary
    group 'order_status'.
  status: active
  aliases:
  - підтверджено
  owner_module: forprint_library
  dictionary_group: order_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: in_progress
  label_uk: У роботі
  label_en: In Progress
  description: Canonical shared operational dictionary value 'in_progress' for dictionary
    group 'order_status'.
  status: active
  aliases:
  - у роботі
  owner_module: forprint_library
  dictionary_group: order_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: completed
  label_uk: Завершено
  label_en: Completed
  description: Canonical shared operational dictionary value 'completed' for dictionary
    group 'order_status'.
  status: active
  aliases:
  - завершено
  owner_module: forprint_library
  dictionary_group: order_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: cancelled
  label_uk: Скасовано
  label_en: Cancelled
  description: Canonical shared operational dictionary value 'cancelled' for dictionary
    group 'order_status'.
  status: active
  aliases:
  - скасовано
  owner_module: forprint_library
  dictionary_group: order_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: blocked
  label_uk: Заблоковано
  label_en: Blocked
  description: Canonical shared operational dictionary value 'blocked' for dictionary
    group 'order_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: order_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: manual_review_required
  label_uk: Потрібна ручна перевірка
  label_en: Manual Review Required
  description: Canonical shared operational dictionary value 'manual_review_required'
    for dictionary group 'order_status'.
  status: active
  aliases:
  - manual_review
  - ручна перевірка
  owner_module: forprint_library
  dictionary_group: order_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: archived
  label_uk: Архівовано
  label_en: Archived
  description: Canonical shared operational dictionary value 'archived' for dictionary
    group 'order_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: order_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: unknown
  label_uk: Невідомо
  label_en: Unknown
  description: Canonical shared operational dictionary value 'unknown' for dictionary
    group 'order_status'.
  status: active
  aliases:
  - невідомо
  owner_module: forprint_library
  dictionary_group: order_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
```

## Primary source

**Path:** `dictionaries/payment_status.yaml`
**SHA256:** `daf7c804d1362d54c83a464cd949615e5f640848147cdfbf8200c135e576df3c`

```yaml
dictionary_group: payment_status
metadata:
  id: shared_operational_dictionary_v0_1
  name: Shared Operational Dictionary v0.1
  version: '0.1'
  dictionary_status: draft_shared_operational_dictionary_v0_1
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  unit_dictionary_status: not_final_inventory_unit_system
entries:
- id: not_invoiced
  label_uk: Not Invoiced
  label_en: Not Invoiced
  description: Canonical shared operational dictionary value 'not_invoiced' for dictionary
    group 'payment_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: payment_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: invoice_reference_pending
  label_uk: Invoice Reference Pending
  label_en: Invoice Reference Pending
  description: Canonical shared operational dictionary value 'invoice_reference_pending'
    for dictionary group 'payment_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: payment_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: unpaid
  label_uk: Не оплачено
  label_en: Unpaid
  description: Canonical shared operational dictionary value 'unpaid' for dictionary
    group 'payment_status'.
  status: active
  aliases:
  - не оплачено
  owner_module: forprint_library
  dictionary_group: payment_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: partially_paid
  label_uk: Частково оплачено
  label_en: Partially Paid
  description: Canonical shared operational dictionary value 'partially_paid' for
    dictionary group 'payment_status'.
  status: active
  aliases:
  - частково оплачено
  owner_module: forprint_library
  dictionary_group: payment_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: paid_reference_confirmed
  label_uk: Підтверджено оплату
  label_en: Paid Reference Confirmed
  description: Canonical shared operational dictionary value 'paid_reference_confirmed'
    for dictionary group 'payment_status'.
  status: active
  aliases:
  - paid
  - оплачено
  owner_module: forprint_library
  dictionary_group: payment_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: overdue
  label_uk: Прострочено
  label_en: Overdue
  description: Canonical shared operational dictionary value 'overdue' for dictionary
    group 'payment_status'.
  status: active
  aliases:
  - прострочено
  owner_module: forprint_library
  dictionary_group: payment_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: cancelled
  label_uk: Скасовано
  label_en: Cancelled
  description: Canonical shared operational dictionary value 'cancelled' for dictionary
    group 'payment_status'.
  status: active
  aliases:
  - скасовано
  owner_module: forprint_library
  dictionary_group: payment_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: unknown
  label_uk: Невідомо
  label_en: Unknown
  description: Canonical shared operational dictionary value 'unknown' for dictionary
    group 'payment_status'.
  status: active
  aliases:
  - невідомо
  owner_module: forprint_library
  dictionary_group: payment_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
```

## Primary source

**Path:** `dictionaries/product_service_reference_status.yaml`
**SHA256:** `f3206fe457cfad223b804ccbb3ed6822e38c8d57acf33e039902b84015a3f1e3`

```yaml
dictionary_group: product_service_reference_status
metadata:
  id: shared_operational_dictionary_v0_1
  name: Shared Operational Dictionary v0.1
  version: '0.1'
  dictionary_status: draft_shared_operational_dictionary_v0_1
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  unit_dictionary_status: not_final_inventory_unit_system
entries:
- id: draft_display_only
  label_uk: Draft Display Only
  label_en: Draft Display Only
  description: Canonical shared operational dictionary value 'draft_display_only'
    for dictionary group 'product_service_reference_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: product_service_reference_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: library_reference_pending
  label_uk: Library Reference Pending
  label_en: Library Reference Pending
  description: Canonical shared operational dictionary value 'library_reference_pending'
    for dictionary group 'product_service_reference_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: product_service_reference_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: library_reference_confirmed
  label_uk: Library Reference Confirmed
  label_en: Library Reference Confirmed
  description: Canonical shared operational dictionary value 'library_reference_confirmed'
    for dictionary group 'product_service_reference_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: product_service_reference_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: ambiguous_manual_review_required
  label_uk: Ambiguous Manual Review Required
  label_en: Ambiguous Manual Review Required
  description: Canonical shared operational dictionary value 'ambiguous_manual_review_required'
    for dictionary group 'product_service_reference_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: product_service_reference_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: deprecated_reference
  label_uk: Deprecated Reference
  label_en: Deprecated Reference
  description: Canonical shared operational dictionary value 'deprecated_reference'
    for dictionary group 'product_service_reference_status'.
  status: deprecated
  aliases: []
  owner_module: forprint_library
  dictionary_group: product_service_reference_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: unknown
  label_uk: Невідомо
  label_en: Unknown
  description: Canonical shared operational dictionary value 'unknown' for dictionary
    group 'product_service_reference_status'.
  status: active
  aliases:
  - невідомо
  owner_module: forprint_library
  dictionary_group: product_service_reference_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
```

## Primary source

**Path:** `dictionaries/production_status.yaml`
**SHA256:** `68dc2e2dd1e2e54be8f49514c95258f6d6012f166d6d0683ba9cc7fc20dded27`

```yaml
dictionary_group: production_status
metadata:
  id: shared_operational_dictionary_v0_1
  name: Shared Operational Dictionary v0.1
  version: '0.1'
  dictionary_status: draft_shared_operational_dictionary_v0_1
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  unit_dictionary_status: not_final_inventory_unit_system
entries:
- id: not_started
  label_uk: Не розпочато
  label_en: Not Started
  description: Canonical shared operational dictionary value 'not_started' for dictionary
    group 'production_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: production_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: ready
  label_uk: Готово
  label_en: Ready
  description: Canonical shared operational dictionary value 'ready' for dictionary
    group 'production_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: production_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: in_progress
  label_uk: У роботі
  label_en: In Progress
  description: Canonical shared operational dictionary value 'in_progress' for dictionary
    group 'production_status'.
  status: active
  aliases:
  - у роботі
  owner_module: forprint_library
  dictionary_group: production_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: waiting_external_contractor
  label_uk: Очікування зовнішнього підрядника
  label_en: Waiting External Contractor
  description: Canonical shared operational dictionary value 'waiting_external_contractor'
    for dictionary group 'production_status'.
  status: active
  aliases:
  - external_contractor_wait
  owner_module: forprint_library
  dictionary_group: production_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: blocked
  label_uk: Заблоковано
  label_en: Blocked
  description: Canonical shared operational dictionary value 'blocked' for dictionary
    group 'production_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: production_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: completed
  label_uk: Завершено
  label_en: Completed
  description: Canonical shared operational dictionary value 'completed' for dictionary
    group 'production_status'.
  status: active
  aliases:
  - завершено
  owner_module: forprint_library
  dictionary_group: production_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: cancelled
  label_uk: Скасовано
  label_en: Cancelled
  description: Canonical shared operational dictionary value 'cancelled' for dictionary
    group 'production_status'.
  status: active
  aliases:
  - скасовано
  owner_module: forprint_library
  dictionary_group: production_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: unknown
  label_uk: Невідомо
  label_en: Unknown
  description: Canonical shared operational dictionary value 'unknown' for dictionary
    group 'production_status'.
  status: active
  aliases:
  - невідомо
  owner_module: forprint_library
  dictionary_group: production_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
```

## Primary source

**Path:** `dictionaries/reference_resolution_status.yaml`
**SHA256:** `3dc876532ae562dc9d7cf00f065f84655a6d2d66d955470bee4d5efc56d45e64`

```yaml
dictionary_group: reference_resolution_status
metadata:
  id: shared_operational_dictionary_v0_1
  name: Shared Operational Dictionary v0.1
  version: '0.1'
  dictionary_status: draft_shared_operational_dictionary_v0_1
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  unit_dictionary_status: not_final_inventory_unit_system
entries:
- id: draft_display_only
  label_uk: Draft Display Only
  label_en: Draft Display Only
  description: Canonical shared operational dictionary value 'draft_display_only'
    for dictionary group 'reference_resolution_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: reference_resolution_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: reference_pending
  label_uk: Reference Pending
  label_en: Reference Pending
  description: Canonical shared operational dictionary value 'reference_pending' for
    dictionary group 'reference_resolution_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: reference_resolution_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: reference_confirmed
  label_uk: Reference Confirmed
  label_en: Reference Confirmed
  description: Canonical shared operational dictionary value 'reference_confirmed'
    for dictionary group 'reference_resolution_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: reference_resolution_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: ambiguous_manual_review_required
  label_uk: Ambiguous Manual Review Required
  label_en: Ambiguous Manual Review Required
  description: Canonical shared operational dictionary value 'ambiguous_manual_review_required'
    for dictionary group 'reference_resolution_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: reference_resolution_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: deprecated_reference
  label_uk: Deprecated Reference
  label_en: Deprecated Reference
  description: Canonical shared operational dictionary value 'deprecated_reference'
    for dictionary group 'reference_resolution_status'.
  status: deprecated
  aliases: []
  owner_module: forprint_library
  dictionary_group: reference_resolution_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: unknown
  label_uk: Невідомо
  label_en: Unknown
  description: Canonical shared operational dictionary value 'unknown' for dictionary
    group 'reference_resolution_status'.
  status: active
  aliases:
  - невідомо
  owner_module: forprint_library
  dictionary_group: reference_resolution_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
```

## Primary source

**Path:** `dictionaries/shared_operational_dictionary_v0_1.yaml`
**SHA256:** `3610bb44537903fa66fdd7be02deacabcd6b073e69d2a44c80a8a8c075056d26`

```yaml
metadata:
  id: shared_operational_dictionary_v0_1
  name: Shared Operational Dictionary v0.1
  version: '0.1'
  dictionary_status: draft_shared_operational_dictionary_v0_1
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  unit_dictionary_status: not_final_inventory_unit_system
dictionary_groups:
  source_system:
  - id: forprint_operational_registry
    label_uk: Forprint Operational Registry
    label_en: Forprint Operational Registry
    description: Canonical shared operational dictionary value 'forprint_operational_registry'
      for dictionary group 'source_system'.
    status: active
    aliases:
    - operational_registry
    - opr
    owner_module: forprint_library
    dictionary_group: source_system
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: forprint_library
    label_uk: Forprint Library
    label_en: Forprint Library
    description: Canonical shared operational dictionary value 'forprint_library'
      for dictionary group 'source_system'.
    status: active
    aliases:
    - library
    owner_module: forprint_library
    dictionary_group: source_system
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: calculator_engine
    label_uk: Calculator Engine
    label_en: Calculator Engine
    description: Canonical shared operational dictionary value 'calculator_engine'
      for dictionary group 'source_system'.
    status: active
    aliases:
    - calculator
    owner_module: forprint_library
    dictionary_group: source_system
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: accounting_registry_service
    label_uk: Accounting Registry Service
    label_en: Accounting Registry Service
    description: Canonical shared operational dictionary value 'accounting_registry_service'
      for dictionary group 'source_system'.
    status: active
    aliases:
    - accounting_registry
    owner_module: forprint_library
    dictionary_group: source_system
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: telegram_bot
    label_uk: Telegram Bot
    label_en: Telegram Bot
    description: Canonical shared operational dictionary value 'telegram_bot' for
      dictionary group 'source_system'.
    status: active
    aliases:
    - telegram
    owner_module: forprint_library
    dictionary_group: source_system
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: forprint_crm
    label_uk: Forprint Crm
    label_en: Forprint Crm
    description: Canonical shared operational dictionary value 'forprint_crm' for
      dictionary group 'source_system'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: source_system
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: forprint_integration_gateway
    label_uk: Forprint Integration Gateway
    label_en: Forprint Integration Gateway
    description: Canonical shared operational dictionary value 'forprint_integration_gateway'
      for dictionary group 'source_system'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: source_system
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: forprint_prepress_hub
    label_uk: Forprint Prepress Hub
    label_en: Forprint Prepress Hub
    description: Canonical shared operational dictionary value 'forprint_prepress_hub'
      for dictionary group 'source_system'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: source_system
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: warehouse_service
    label_uk: Warehouse Service
    label_en: Warehouse Service
    description: Canonical shared operational dictionary value 'warehouse_service'
      for dictionary group 'source_system'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: source_system
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: logistics_service
    label_uk: Logistics Service
    label_en: Logistics Service
    description: Canonical shared operational dictionary value 'logistics_service'
      for dictionary group 'source_system'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: source_system
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: website
    label_uk: Website
    label_en: Website
    description: Canonical shared operational dictionary value 'website' for dictionary
      group 'source_system'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: source_system
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: mobile_app
    label_uk: Mobile App
    label_en: Mobile App
    description: Canonical shared operational dictionary value 'mobile_app' for dictionary
      group 'source_system'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: source_system
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: one_c_bas
    label_uk: 1C/BAS
    label_en: One C Bas
    description: Canonical shared operational dictionary value 'one_c_bas' for dictionary
      group 'source_system'.
    status: active
    aliases:
    - 1c
    - bas
    - 1c_bas
    owner_module: forprint_library
    dictionary_group: source_system
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: sanitized_demo
    label_uk: Sanitized Demo
    label_en: Sanitized Demo
    description: Canonical shared operational dictionary value 'sanitized_demo' for
      dictionary group 'source_system'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: source_system
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: manual_entry
    label_uk: Manual Entry
    label_en: Manual Entry
    description: Canonical shared operational dictionary value 'manual_entry' for
      dictionary group 'source_system'.
    status: active
    aliases:
    - manual
    - ручне введення
    owner_module: forprint_library
    dictionary_group: source_system
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'source_system'.
    status: active
    aliases: &id001
    - невідомо
    owner_module: forprint_library
    dictionary_group: source_system
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  entity_type:
  - id: client_account
    label_uk: Client Account
    label_en: Client Account
    description: Canonical shared operational dictionary value 'client_account' for
      dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: client_group
    label_uk: Client Group
    label_en: Client Group
    description: Canonical shared operational dictionary value 'client_group' for
      dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: contact_person
    label_uk: Contact Person
    label_en: Contact Person
    description: Canonical shared operational dictionary value 'contact_person' for
      dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: contact_method
    label_uk: Contact Method
    label_en: Contact Method
    description: Canonical shared operational dictionary value 'contact_method' for
      dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: client_address
    label_uk: Client Address
    label_en: Client Address
    description: Canonical shared operational dictionary value 'client_address' for
      dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: legal_entity_profile
    label_uk: Legal Entity Profile
    label_en: Legal Entity Profile
    description: Canonical shared operational dictionary value 'legal_entity_profile'
      for dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: external_reference
    label_uk: External Reference
    label_en: External Reference
    description: Canonical shared operational dictionary value 'external_reference'
      for dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: order
    label_uk: Order
    label_en: Order
    description: Canonical shared operational dictionary value 'order' for dictionary
      group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: order_line
    label_uk: Order Line
    label_en: Order Line
    description: Canonical shared operational dictionary value 'order_line' for dictionary
      group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: calculator_output_package
    label_uk: Calculator Output Package
    label_en: Calculator Output Package
    description: Canonical shared operational dictionary value 'calculator_output_package'
      for dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: product_service_reference
    label_uk: Product Service Reference
    label_en: Product Service Reference
    description: Canonical shared operational dictionary value 'product_service_reference'
      for dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: material_requirement
    label_uk: Material Requirement
    label_en: Material Requirement
    description: Canonical shared operational dictionary value 'material_requirement'
      for dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: payment_projection
    label_uk: Payment Projection
    label_en: Payment Projection
    description: Canonical shared operational dictionary value 'payment_projection'
      for dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: workflow_template
    label_uk: Workflow Template
    label_en: Workflow Template
    description: Canonical shared operational dictionary value 'workflow_template'
      for dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: workflow_stage
    label_uk: Workflow Stage
    label_en: Workflow Stage
    description: Canonical shared operational dictionary value 'workflow_stage' for
      dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: deadline_control
    label_uk: Deadline Control
    label_en: Deadline Control
    description: Canonical shared operational dictionary value 'deadline_control'
      for dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: contractor_reference
    label_uk: Contractor Reference
    label_en: Contractor Reference
    description: Canonical shared operational dictionary value 'contractor_reference'
      for dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: alert_rule
    label_uk: Alert Rule
    label_en: Alert Rule
    description: Canonical shared operational dictionary value 'alert_rule' for dictionary
      group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: alert_event
    label_uk: Alert Event
    label_en: Alert Event
    description: Canonical shared operational dictionary value 'alert_event' for dictionary
      group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: report_definition
    label_uk: Report Definition
    label_en: Report Definition
    description: Canonical shared operational dictionary value 'report_definition'
      for dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: report_projection
    label_uk: Report Projection
    label_en: Report Projection
    description: Canonical shared operational dictionary value 'report_projection'
      for dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: operational_event
    label_uk: Operational Event
    label_en: Operational Event
    description: Canonical shared operational dictionary value 'operational_event'
      for dictionary group 'entity_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'entity_type'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: entity_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  order_status:
  - id: draft
    label_uk: Чернетка
    label_en: Draft
    description: Canonical shared operational dictionary value 'draft' for dictionary
      group 'order_status'.
    status: active
    aliases: &id002
    - чернетка
    owner_module: forprint_library
    dictionary_group: order_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: needs_review
    label_uk: Потребує перевірки
    label_en: Needs Review
    description: Canonical shared operational dictionary value 'needs_review' for
      dictionary group 'order_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: order_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: confirmed
    label_uk: Підтверджено
    label_en: Confirmed
    description: Canonical shared operational dictionary value 'confirmed' for dictionary
      group 'order_status'.
    status: active
    aliases: &id008
    - підтверджено
    owner_module: forprint_library
    dictionary_group: order_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: in_progress
    label_uk: У роботі
    label_en: In Progress
    description: Canonical shared operational dictionary value 'in_progress' for dictionary
      group 'order_status'.
    status: active
    aliases: &id003
    - у роботі
    owner_module: forprint_library
    dictionary_group: order_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: completed
    label_uk: Завершено
    label_en: Completed
    description: Canonical shared operational dictionary value 'completed' for dictionary
      group 'order_status'.
    status: active
    aliases: &id004
    - завершено
    owner_module: forprint_library
    dictionary_group: order_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: cancelled
    label_uk: Скасовано
    label_en: Cancelled
    description: Canonical shared operational dictionary value 'cancelled' for dictionary
      group 'order_status'.
    status: active
    aliases: &id005
    - скасовано
    owner_module: forprint_library
    dictionary_group: order_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: blocked
    label_uk: Заблоковано
    label_en: Blocked
    description: Canonical shared operational dictionary value 'blocked' for dictionary
      group 'order_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: order_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: manual_review_required
    label_uk: Потрібна ручна перевірка
    label_en: Manual Review Required
    description: Canonical shared operational dictionary value 'manual_review_required'
      for dictionary group 'order_status'.
    status: active
    aliases: &id006
    - manual_review
    - ручна перевірка
    owner_module: forprint_library
    dictionary_group: order_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: archived
    label_uk: Архівовано
    label_en: Archived
    description: Canonical shared operational dictionary value 'archived' for dictionary
      group 'order_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: order_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'order_status'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: order_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  order_line_status:
  - id: draft
    label_uk: Чернетка
    label_en: Draft
    description: Canonical shared operational dictionary value 'draft' for dictionary
      group 'order_line_status'.
    status: active
    aliases: *id002
    owner_module: forprint_library
    dictionary_group: order_line_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: pending_reference_resolution
    label_uk: Pending Reference Resolution
    label_en: Pending Reference Resolution
    description: Canonical shared operational dictionary value 'pending_reference_resolution'
      for dictionary group 'order_line_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: order_line_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: ready
    label_uk: Готово
    label_en: Ready
    description: Canonical shared operational dictionary value 'ready' for dictionary
      group 'order_line_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: order_line_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: in_progress
    label_uk: У роботі
    label_en: In Progress
    description: Canonical shared operational dictionary value 'in_progress' for dictionary
      group 'order_line_status'.
    status: active
    aliases: *id003
    owner_module: forprint_library
    dictionary_group: order_line_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: completed
    label_uk: Завершено
    label_en: Completed
    description: Canonical shared operational dictionary value 'completed' for dictionary
      group 'order_line_status'.
    status: active
    aliases: *id004
    owner_module: forprint_library
    dictionary_group: order_line_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: cancelled
    label_uk: Скасовано
    label_en: Cancelled
    description: Canonical shared operational dictionary value 'cancelled' for dictionary
      group 'order_line_status'.
    status: active
    aliases: *id005
    owner_module: forprint_library
    dictionary_group: order_line_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: manual_review_required
    label_uk: Потрібна ручна перевірка
    label_en: Manual Review Required
    description: Canonical shared operational dictionary value 'manual_review_required'
      for dictionary group 'order_line_status'.
    status: active
    aliases: *id006
    owner_module: forprint_library
    dictionary_group: order_line_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'order_line_status'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: order_line_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  payment_status:
  - id: not_invoiced
    label_uk: Not Invoiced
    label_en: Not Invoiced
    description: Canonical shared operational dictionary value 'not_invoiced' for
      dictionary group 'payment_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: payment_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: invoice_reference_pending
    label_uk: Invoice Reference Pending
    label_en: Invoice Reference Pending
    description: Canonical shared operational dictionary value 'invoice_reference_pending'
      for dictionary group 'payment_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: payment_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unpaid
    label_uk: Не оплачено
    label_en: Unpaid
    description: Canonical shared operational dictionary value 'unpaid' for dictionary
      group 'payment_status'.
    status: active
    aliases:
    - не оплачено
    owner_module: forprint_library
    dictionary_group: payment_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: partially_paid
    label_uk: Частково оплачено
    label_en: Partially Paid
    description: Canonical shared operational dictionary value 'partially_paid' for
      dictionary group 'payment_status'.
    status: active
    aliases:
    - частково оплачено
    owner_module: forprint_library
    dictionary_group: payment_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: paid_reference_confirmed
    label_uk: Підтверджено оплату
    label_en: Paid Reference Confirmed
    description: Canonical shared operational dictionary value 'paid_reference_confirmed'
      for dictionary group 'payment_status'.
    status: active
    aliases:
    - paid
    - оплачено
    owner_module: forprint_library
    dictionary_group: payment_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: overdue
    label_uk: Прострочено
    label_en: Overdue
    description: Canonical shared operational dictionary value 'overdue' for dictionary
      group 'payment_status'.
    status: active
    aliases:
    - прострочено
    owner_module: forprint_library
    dictionary_group: payment_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: cancelled
    label_uk: Скасовано
    label_en: Cancelled
    description: Canonical shared operational dictionary value 'cancelled' for dictionary
      group 'payment_status'.
    status: active
    aliases: *id005
    owner_module: forprint_library
    dictionary_group: payment_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'payment_status'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: payment_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  production_status:
  - id: not_started
    label_uk: Не розпочато
    label_en: Not Started
    description: Canonical shared operational dictionary value 'not_started' for dictionary
      group 'production_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: production_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: ready
    label_uk: Готово
    label_en: Ready
    description: Canonical shared operational dictionary value 'ready' for dictionary
      group 'production_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: production_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: in_progress
    label_uk: У роботі
    label_en: In Progress
    description: Canonical shared operational dictionary value 'in_progress' for dictionary
      group 'production_status'.
    status: active
    aliases: *id003
    owner_module: forprint_library
    dictionary_group: production_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: waiting_external_contractor
    label_uk: Очікування зовнішнього підрядника
    label_en: Waiting External Contractor
    description: Canonical shared operational dictionary value 'waiting_external_contractor'
      for dictionary group 'production_status'.
    status: active
    aliases: &id007
    - external_contractor_wait
    owner_module: forprint_library
    dictionary_group: production_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: blocked
    label_uk: Заблоковано
    label_en: Blocked
    description: Canonical shared operational dictionary value 'blocked' for dictionary
      group 'production_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: production_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: completed
    label_uk: Завершено
    label_en: Completed
    description: Canonical shared operational dictionary value 'completed' for dictionary
      group 'production_status'.
    status: active
    aliases: *id004
    owner_module: forprint_library
    dictionary_group: production_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: cancelled
    label_uk: Скасовано
    label_en: Cancelled
    description: Canonical shared operational dictionary value 'cancelled' for dictionary
      group 'production_status'.
    status: active
    aliases: *id005
    owner_module: forprint_library
    dictionary_group: production_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'production_status'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: production_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  workflow_status:
  - id: not_started
    label_uk: Не розпочато
    label_en: Not Started
    description: Canonical shared operational dictionary value 'not_started' for dictionary
      group 'workflow_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: workflow_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: active
    label_uk: Активний
    label_en: Active
    description: Canonical shared operational dictionary value 'active' for dictionary
      group 'workflow_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: workflow_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: blocked
    label_uk: Заблоковано
    label_en: Blocked
    description: Canonical shared operational dictionary value 'blocked' for dictionary
      group 'workflow_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: workflow_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: completed
    label_uk: Завершено
    label_en: Completed
    description: Canonical shared operational dictionary value 'completed' for dictionary
      group 'workflow_status'.
    status: active
    aliases: *id004
    owner_module: forprint_library
    dictionary_group: workflow_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: cancelled
    label_uk: Скасовано
    label_en: Cancelled
    description: Canonical shared operational dictionary value 'cancelled' for dictionary
      group 'workflow_status'.
    status: active
    aliases: *id005
    owner_module: forprint_library
    dictionary_group: workflow_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: manual_review_required
    label_uk: Потрібна ручна перевірка
    label_en: Manual Review Required
    description: Canonical shared operational dictionary value 'manual_review_required'
      for dictionary group 'workflow_status'.
    status: active
    aliases: *id006
    owner_module: forprint_library
    dictionary_group: workflow_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'workflow_status'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: workflow_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  workflow_stage_status:
  - id: not_started
    label_uk: Не розпочато
    label_en: Not Started
    description: Canonical shared operational dictionary value 'not_started' for dictionary
      group 'workflow_stage_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: workflow_stage_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: ready
    label_uk: Готово
    label_en: Ready
    description: Canonical shared operational dictionary value 'ready' for dictionary
      group 'workflow_stage_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: workflow_stage_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: in_progress
    label_uk: У роботі
    label_en: In Progress
    description: Canonical shared operational dictionary value 'in_progress' for dictionary
      group 'workflow_stage_status'.
    status: active
    aliases: *id003
    owner_module: forprint_library
    dictionary_group: workflow_stage_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: blocked
    label_uk: Заблоковано
    label_en: Blocked
    description: Canonical shared operational dictionary value 'blocked' for dictionary
      group 'workflow_stage_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: workflow_stage_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: waiting_external_contractor
    label_uk: Очікування зовнішнього підрядника
    label_en: Waiting External Contractor
    description: Canonical shared operational dictionary value 'waiting_external_contractor'
      for dictionary group 'workflow_stage_status'.
    status: active
    aliases: *id007
    owner_module: forprint_library
    dictionary_group: workflow_stage_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: completed
    label_uk: Завершено
    label_en: Completed
    description: Canonical shared operational dictionary value 'completed' for dictionary
      group 'workflow_stage_status'.
    status: active
    aliases: *id004
    owner_module: forprint_library
    dictionary_group: workflow_stage_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: cancelled
    label_uk: Скасовано
    label_en: Cancelled
    description: Canonical shared operational dictionary value 'cancelled' for dictionary
      group 'workflow_stage_status'.
    status: active
    aliases: *id005
    owner_module: forprint_library
    dictionary_group: workflow_stage_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: late
    label_uk: Прострочено
    label_en: Late
    description: Canonical shared operational dictionary value 'late' for dictionary
      group 'workflow_stage_status'.
    status: active
    aliases:
    - прострочений етап
    owner_module: forprint_library
    dictionary_group: workflow_stage_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: manual_review_required
    label_uk: Потрібна ручна перевірка
    label_en: Manual Review Required
    description: Canonical shared operational dictionary value 'manual_review_required'
      for dictionary group 'workflow_stage_status'.
    status: active
    aliases: *id006
    owner_module: forprint_library
    dictionary_group: workflow_stage_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'workflow_stage_status'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: workflow_stage_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  material_requirement_status:
  - id: planned
    label_uk: Заплановано
    label_en: Planned
    description: Canonical shared operational dictionary value 'planned' for dictionary
      group 'material_requirement_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: material_requirement_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: library_reference_pending
    label_uk: Library Reference Pending
    label_en: Library Reference Pending
    description: Canonical shared operational dictionary value 'library_reference_pending'
      for dictionary group 'material_requirement_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: material_requirement_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: warehouse_reference_pending
    label_uk: Warehouse Reference Pending
    label_en: Warehouse Reference Pending
    description: Canonical shared operational dictionary value 'warehouse_reference_pending'
      for dictionary group 'material_requirement_status'.
    status: active
    aliases:
    - warehouse_pending
    owner_module: forprint_library
    dictionary_group: material_requirement_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: reserved_reference_pending
    label_uk: Reserved Reference Pending
    label_en: Reserved Reference Pending
    description: Canonical shared operational dictionary value 'reserved_reference_pending'
      for dictionary group 'material_requirement_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: material_requirement_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: confirmed
    label_uk: Підтверджено
    label_en: Confirmed
    description: Canonical shared operational dictionary value 'confirmed' for dictionary
      group 'material_requirement_status'.
    status: active
    aliases: *id008
    owner_module: forprint_library
    dictionary_group: material_requirement_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: fulfilled
    label_uk: Виконано
    label_en: Fulfilled
    description: Canonical shared operational dictionary value 'fulfilled' for dictionary
      group 'material_requirement_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: material_requirement_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: cancelled
    label_uk: Скасовано
    label_en: Cancelled
    description: Canonical shared operational dictionary value 'cancelled' for dictionary
      group 'material_requirement_status'.
    status: active
    aliases: *id005
    owner_module: forprint_library
    dictionary_group: material_requirement_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'material_requirement_status'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: material_requirement_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  reference_resolution_status:
  - id: draft_display_only
    label_uk: Draft Display Only
    label_en: Draft Display Only
    description: Canonical shared operational dictionary value 'draft_display_only'
      for dictionary group 'reference_resolution_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: reference_resolution_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: reference_pending
    label_uk: Reference Pending
    label_en: Reference Pending
    description: Canonical shared operational dictionary value 'reference_pending'
      for dictionary group 'reference_resolution_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: reference_resolution_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: reference_confirmed
    label_uk: Reference Confirmed
    label_en: Reference Confirmed
    description: Canonical shared operational dictionary value 'reference_confirmed'
      for dictionary group 'reference_resolution_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: reference_resolution_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: ambiguous_manual_review_required
    label_uk: Ambiguous Manual Review Required
    label_en: Ambiguous Manual Review Required
    description: Canonical shared operational dictionary value 'ambiguous_manual_review_required'
      for dictionary group 'reference_resolution_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: reference_resolution_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: deprecated_reference
    label_uk: Deprecated Reference
    label_en: Deprecated Reference
    description: Canonical shared operational dictionary value 'deprecated_reference'
      for dictionary group 'reference_resolution_status'.
    status: deprecated
    aliases: []
    owner_module: forprint_library
    dictionary_group: reference_resolution_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'reference_resolution_status'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: reference_resolution_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  product_service_reference_status:
  - id: draft_display_only
    label_uk: Draft Display Only
    label_en: Draft Display Only
    description: Canonical shared operational dictionary value 'draft_display_only'
      for dictionary group 'product_service_reference_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: product_service_reference_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: library_reference_pending
    label_uk: Library Reference Pending
    label_en: Library Reference Pending
    description: Canonical shared operational dictionary value 'library_reference_pending'
      for dictionary group 'product_service_reference_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: product_service_reference_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: library_reference_confirmed
    label_uk: Library Reference Confirmed
    label_en: Library Reference Confirmed
    description: Canonical shared operational dictionary value 'library_reference_confirmed'
      for dictionary group 'product_service_reference_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: product_service_reference_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: ambiguous_manual_review_required
    label_uk: Ambiguous Manual Review Required
    label_en: Ambiguous Manual Review Required
    description: Canonical shared operational dictionary value 'ambiguous_manual_review_required'
      for dictionary group 'product_service_reference_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: product_service_reference_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: deprecated_reference
    label_uk: Deprecated Reference
    label_en: Deprecated Reference
    description: Canonical shared operational dictionary value 'deprecated_reference'
      for dictionary group 'product_service_reference_status'.
    status: deprecated
    aliases: []
    owner_module: forprint_library
    dictionary_group: product_service_reference_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'product_service_reference_status'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: product_service_reference_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  contractor_reference_status:
  - id: display_only
    label_uk: Display Only
    label_en: Display Only
    description: Canonical shared operational dictionary value 'display_only' for
      dictionary group 'contractor_reference_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: contractor_reference_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: client_account_reference_pending
    label_uk: Client Account Reference Pending
    label_en: Client Account Reference Pending
    description: Canonical shared operational dictionary value 'client_account_reference_pending'
      for dictionary group 'contractor_reference_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: contractor_reference_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: client_account_reference_confirmed
    label_uk: Client Account Reference Confirmed
    label_en: Client Account Reference Confirmed
    description: Canonical shared operational dictionary value 'client_account_reference_confirmed'
      for dictionary group 'contractor_reference_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: contractor_reference_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: external_reference_pending
    label_uk: External Reference Pending
    label_en: External Reference Pending
    description: Canonical shared operational dictionary value 'external_reference_pending'
      for dictionary group 'contractor_reference_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: contractor_reference_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: manual_review_required
    label_uk: Потрібна ручна перевірка
    label_en: Manual Review Required
    description: Canonical shared operational dictionary value 'manual_review_required'
      for dictionary group 'contractor_reference_status'.
    status: active
    aliases: *id006
    owner_module: forprint_library
    dictionary_group: contractor_reference_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'contractor_reference_status'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: contractor_reference_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  deadline_type:
  - id: order_due
    label_uk: Order Due
    label_en: Order Due
    description: Canonical shared operational dictionary value 'order_due' for dictionary
      group 'deadline_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: deadline_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: stage_due
    label_uk: Stage Due
    label_en: Stage Due
    description: Canonical shared operational dictionary value 'stage_due' for dictionary
      group 'deadline_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: deadline_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: payment_due
    label_uk: Payment Due
    label_en: Payment Due
    description: Canonical shared operational dictionary value 'payment_due' for dictionary
      group 'deadline_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: deadline_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: material_required_by
    label_uk: Material Required By
    label_en: Material Required By
    description: Canonical shared operational dictionary value 'material_required_by'
      for dictionary group 'deadline_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: deadline_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: manual_review_due
    label_uk: Manual Review Due
    label_en: Manual Review Due
    description: Canonical shared operational dictionary value 'manual_review_due'
      for dictionary group 'deadline_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: deadline_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'deadline_type'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: deadline_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  alert_rule_type:
  - id: workflow_stage_late
    label_uk: Workflow Stage Late
    label_en: Workflow Stage Late
    description: Canonical shared operational dictionary value 'workflow_stage_late'
      for dictionary group 'alert_rule_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: alert_rule_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: order_deadline_near
    label_uk: Order Deadline Near
    label_en: Order Deadline Near
    description: Canonical shared operational dictionary value 'order_deadline_near'
      for dictionary group 'alert_rule_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: alert_rule_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: payment_overdue
    label_uk: Payment Overdue
    label_en: Payment Overdue
    description: Canonical shared operational dictionary value 'payment_overdue' for
      dictionary group 'alert_rule_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: alert_rule_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: material_requirement_unresolved
    label_uk: Material Requirement Unresolved
    label_en: Material Requirement Unresolved
    description: Canonical shared operational dictionary value 'material_requirement_unresolved'
      for dictionary group 'alert_rule_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: alert_rule_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: manual_review_stale
    label_uk: Manual Review Stale
    label_en: Manual Review Stale
    description: Canonical shared operational dictionary value 'manual_review_stale'
      for dictionary group 'alert_rule_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: alert_rule_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: contractor_stage_blocked
    label_uk: Contractor Stage Blocked
    label_en: Contractor Stage Blocked
    description: Canonical shared operational dictionary value 'contractor_stage_blocked'
      for dictionary group 'alert_rule_type'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: alert_rule_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'alert_rule_type'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: alert_rule_type
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  alert_severity:
  - id: info
    label_uk: Інформаційно
    label_en: Info
    description: Canonical shared operational dictionary value 'info' for dictionary
      group 'alert_severity'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: alert_severity
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: warning
    label_uk: Попередження
    label_en: Warning
    description: Canonical shared operational dictionary value 'warning' for dictionary
      group 'alert_severity'.
    status: active
    aliases:
    - warn
    owner_module: forprint_library
    dictionary_group: alert_severity
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: high
    label_uk: Високий
    label_en: High
    description: Canonical shared operational dictionary value 'high' for dictionary
      group 'alert_severity'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: alert_severity
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: critical
    label_uk: Критичний
    label_en: Critical
    description: Canonical shared operational dictionary value 'critical' for dictionary
      group 'alert_severity'.
    status: active
    aliases:
    - crit
    owner_module: forprint_library
    dictionary_group: alert_severity
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'alert_severity'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: alert_severity
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  alert_event_status:
  - id: open
    label_uk: Відкрито
    label_en: Open
    description: Canonical shared operational dictionary value 'open' for dictionary
      group 'alert_event_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: alert_event_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: acknowledged
    label_uk: Підтверджено оператором
    label_en: Acknowledged
    description: Canonical shared operational dictionary value 'acknowledged' for
      dictionary group 'alert_event_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: alert_event_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: resolved
    label_uk: Вирішено
    label_en: Resolved
    description: Canonical shared operational dictionary value 'resolved' for dictionary
      group 'alert_event_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: alert_event_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: ignored
    label_uk: Проігноровано
    label_en: Ignored
    description: Canonical shared operational dictionary value 'ignored' for dictionary
      group 'alert_event_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: alert_event_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: failed_to_notify
    label_uk: Failed To Notify
    label_en: Failed To Notify
    description: Canonical shared operational dictionary value 'failed_to_notify'
      for dictionary group 'alert_event_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: alert_event_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'alert_event_status'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: alert_event_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  notification_status:
  - id: not_sent
    label_uk: Не надіслано
    label_en: Not Sent
    description: Canonical shared operational dictionary value 'not_sent' for dictionary
      group 'notification_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: notification_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: queued
    label_uk: У черзі
    label_en: Queued
    description: Canonical shared operational dictionary value 'queued' for dictionary
      group 'notification_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: notification_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: sent
    label_uk: Надіслано
    label_en: Sent
    description: Canonical shared operational dictionary value 'sent' for dictionary
      group 'notification_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: notification_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: failed
    label_uk: Помилка
    label_en: Failed
    description: Canonical shared operational dictionary value 'failed' for dictionary
      group 'notification_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: notification_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: disabled
    label_uk: Вимкнено
    label_en: Disabled
    description: Canonical shared operational dictionary value 'disabled' for dictionary
      group 'notification_status'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: notification_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'notification_status'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: notification_status
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  unit:
  - id: pcs
    label_uk: Штуки
    label_en: Pcs
    description: Canonical shared operational dictionary value 'pcs' for dictionary
      group 'unit'.
    status: active
    aliases:
    - piece
    - pieces
    - шт
    owner_module: forprint_library
    dictionary_group: unit
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: set
    label_uk: Комплект
    label_en: Set
    description: Canonical shared operational dictionary value 'set' for dictionary
      group 'unit'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: unit
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: m
    label_uk: Метри
    label_en: M
    description: Canonical shared operational dictionary value 'm' for dictionary
      group 'unit'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: unit
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: m2
    label_uk: Квадратні метри
    label_en: M2
    description: Canonical shared operational dictionary value 'm2' for dictionary
      group 'unit'.
    status: active
    aliases:
    - sqm
    - square_meter
    - м2
    owner_module: forprint_library
    dictionary_group: unit
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: kg
    label_uk: Кілограми
    label_en: Kg
    description: Canonical shared operational dictionary value 'kg' for dictionary
      group 'unit'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: unit
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: g
    label_uk: Грами
    label_en: G
    description: Canonical shared operational dictionary value 'g' for dictionary
      group 'unit'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: unit
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: l
    label_uk: Літри
    label_en: L
    description: Canonical shared operational dictionary value 'l' for dictionary
      group 'unit'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: unit
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: ml
    label_uk: Мілілітри
    label_en: Ml
    description: Canonical shared operational dictionary value 'ml' for dictionary
      group 'unit'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: unit
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: hour
    label_uk: Година
    label_en: Hour
    description: Canonical shared operational dictionary value 'hour' for dictionary
      group 'unit'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: unit
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: minute
    label_uk: Хвилина
    label_en: Minute
    description: Canonical shared operational dictionary value 'minute' for dictionary
      group 'unit'.
    status: active
    aliases: []
    owner_module: forprint_library
    dictionary_group: unit
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: service
    label_uk: Послуга
    label_en: Service
    description: Canonical shared operational dictionary value 'service' for dictionary
      group 'unit'.
    status: active
    aliases:
    - послуга
    owner_module: forprint_library
    dictionary_group: unit
    version: '0.1'
    notes: Draft shared operational dictionary entry.
  - id: unknown
    label_uk: Невідомо
    label_en: Unknown
    description: Canonical shared operational dictionary value 'unknown' for dictionary
      group 'unit'.
    status: active
    aliases: *id001
    owner_module: forprint_library
    dictionary_group: unit
    version: '0.1'
    notes: Draft shared operational dictionary entry.
```

## Primary source

**Path:** `dictionaries/source_system.yaml`
**SHA256:** `1773c8268f22815e8647b4d682bd1e21ba335fd826700481636d55ceecc4f039`

```yaml
dictionary_group: source_system
metadata:
  id: shared_operational_dictionary_v0_1
  name: Shared Operational Dictionary v0.1
  version: '0.1'
  dictionary_status: draft_shared_operational_dictionary_v0_1
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  unit_dictionary_status: not_final_inventory_unit_system
entries:
- id: forprint_operational_registry
  label_uk: Forprint Operational Registry
  label_en: Forprint Operational Registry
  description: Canonical shared operational dictionary value 'forprint_operational_registry'
    for dictionary group 'source_system'.
  status: active
  aliases:
  - operational_registry
  - opr
  owner_module: forprint_library
  dictionary_group: source_system
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: forprint_library
  label_uk: Forprint Library
  label_en: Forprint Library
  description: Canonical shared operational dictionary value 'forprint_library' for
    dictionary group 'source_system'.
  status: active
  aliases:
  - library
  owner_module: forprint_library
  dictionary_group: source_system
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: calculator_engine
  label_uk: Calculator Engine
  label_en: Calculator Engine
  description: Canonical shared operational dictionary value 'calculator_engine' for
    dictionary group 'source_system'.
  status: active
  aliases:
  - calculator
  owner_module: forprint_library
  dictionary_group: source_system
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: accounting_registry_service
  label_uk: Accounting Registry Service
  label_en: Accounting Registry Service
  description: Canonical shared operational dictionary value 'accounting_registry_service'
    for dictionary group 'source_system'.
  status: active
  aliases:
  - accounting_registry
  owner_module: forprint_library
  dictionary_group: source_system
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: telegram_bot
  label_uk: Telegram Bot
  label_en: Telegram Bot
  description: Canonical shared operational dictionary value 'telegram_bot' for dictionary
    group 'source_system'.
  status: active
  aliases:
  - telegram
  owner_module: forprint_library
  dictionary_group: source_system
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: forprint_crm
  label_uk: Forprint Crm
  label_en: Forprint Crm
  description: Canonical shared operational dictionary value 'forprint_crm' for dictionary
    group 'source_system'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: source_system
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: forprint_integration_gateway
  label_uk: Forprint Integration Gateway
  label_en: Forprint Integration Gateway
  description: Canonical shared operational dictionary value 'forprint_integration_gateway'
    for dictionary group 'source_system'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: source_system
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: forprint_prepress_hub
  label_uk: Forprint Prepress Hub
  label_en: Forprint Prepress Hub
  description: Canonical shared operational dictionary value 'forprint_prepress_hub'
    for dictionary group 'source_system'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: source_system
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: warehouse_service
  label_uk: Warehouse Service
  label_en: Warehouse Service
  description: Canonical shared operational dictionary value 'warehouse_service' for
    dictionary group 'source_system'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: source_system
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: logistics_service
  label_uk: Logistics Service
  label_en: Logistics Service
  description: Canonical shared operational dictionary value 'logistics_service' for
    dictionary group 'source_system'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: source_system
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: website
  label_uk: Website
  label_en: Website
  description: Canonical shared operational dictionary value 'website' for dictionary
    group 'source_system'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: source_system
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: mobile_app
  label_uk: Mobile App
  label_en: Mobile App
  description: Canonical shared operational dictionary value 'mobile_app' for dictionary
    group 'source_system'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: source_system
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: one_c_bas
  label_uk: 1C/BAS
  label_en: One C Bas
  description: Canonical shared operational dictionary value 'one_c_bas' for dictionary
    group 'source_system'.
  status: active
  aliases:
  - 1c
  - bas
  - 1c_bas
  owner_module: forprint_library
  dictionary_group: source_system
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: sanitized_demo
  label_uk: Sanitized Demo
  label_en: Sanitized Demo
  description: Canonical shared operational dictionary value 'sanitized_demo' for
    dictionary group 'source_system'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: source_system
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: manual_entry
  label_uk: Manual Entry
  label_en: Manual Entry
  description: Canonical shared operational dictionary value 'manual_entry' for dictionary
    group 'source_system'.
  status: active
  aliases:
  - manual
  - ручне введення
  owner_module: forprint_library
  dictionary_group: source_system
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: unknown
  label_uk: Невідомо
  label_en: Unknown
  description: Canonical shared operational dictionary value 'unknown' for dictionary
    group 'source_system'.
  status: active
  aliases:
  - невідомо
  owner_module: forprint_library
  dictionary_group: source_system
  version: '0.1'
  notes: Draft shared operational dictionary entry.
```

## Primary source

**Path:** `dictionaries/unit.yaml`
**SHA256:** `e221517b3fcfee9276bb1f87c2113fe713024db612bffeab2f09e70800e3f8fb`

```yaml
dictionary_group: unit
metadata:
  id: shared_operational_dictionary_v0_1
  name: Shared Operational Dictionary v0.1
  version: '0.1'
  dictionary_status: draft_shared_operational_dictionary_v0_1
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  unit_dictionary_status: not_final_inventory_unit_system
entries:
- id: pcs
  label_uk: Штуки
  label_en: Pcs
  description: Canonical shared operational dictionary value 'pcs' for dictionary
    group 'unit'.
  status: active
  aliases:
  - piece
  - pieces
  - шт
  owner_module: forprint_library
  dictionary_group: unit
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: set
  label_uk: Комплект
  label_en: Set
  description: Canonical shared operational dictionary value 'set' for dictionary
    group 'unit'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: unit
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: m
  label_uk: Метри
  label_en: M
  description: Canonical shared operational dictionary value 'm' for dictionary group
    'unit'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: unit
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: m2
  label_uk: Квадратні метри
  label_en: M2
  description: Canonical shared operational dictionary value 'm2' for dictionary group
    'unit'.
  status: active
  aliases:
  - sqm
  - square_meter
  - м2
  owner_module: forprint_library
  dictionary_group: unit
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: kg
  label_uk: Кілограми
  label_en: Kg
  description: Canonical shared operational dictionary value 'kg' for dictionary group
    'unit'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: unit
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: g
  label_uk: Грами
  label_en: G
  description: Canonical shared operational dictionary value 'g' for dictionary group
    'unit'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: unit
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: l
  label_uk: Літри
  label_en: L
  description: Canonical shared operational dictionary value 'l' for dictionary group
    'unit'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: unit
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: ml
  label_uk: Мілілітри
  label_en: Ml
  description: Canonical shared operational dictionary value 'ml' for dictionary group
    'unit'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: unit
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: hour
  label_uk: Година
  label_en: Hour
  description: Canonical shared operational dictionary value 'hour' for dictionary
    group 'unit'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: unit
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: minute
  label_uk: Хвилина
  label_en: Minute
  description: Canonical shared operational dictionary value 'minute' for dictionary
    group 'unit'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: unit
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: service
  label_uk: Послуга
  label_en: Service
  description: Canonical shared operational dictionary value 'service' for dictionary
    group 'unit'.
  status: active
  aliases:
  - послуга
  owner_module: forprint_library
  dictionary_group: unit
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: unknown
  label_uk: Невідомо
  label_en: Unknown
  description: Canonical shared operational dictionary value 'unknown' for dictionary
    group 'unit'.
  status: active
  aliases:
  - невідомо
  owner_module: forprint_library
  dictionary_group: unit
  version: '0.1'
  notes: Draft shared operational dictionary entry.
```

## Primary source

**Path:** `dictionaries/workflow_stage_status.yaml`
**SHA256:** `011f995de7b642c1c98dbfa8b1ff32d35b5cea5cf4a80ff26d52adbcf810e3df`

```yaml
dictionary_group: workflow_stage_status
metadata:
  id: shared_operational_dictionary_v0_1
  name: Shared Operational Dictionary v0.1
  version: '0.1'
  dictionary_status: draft_shared_operational_dictionary_v0_1
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  unit_dictionary_status: not_final_inventory_unit_system
entries:
- id: not_started
  label_uk: Не розпочато
  label_en: Not Started
  description: Canonical shared operational dictionary value 'not_started' for dictionary
    group 'workflow_stage_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: workflow_stage_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: ready
  label_uk: Готово
  label_en: Ready
  description: Canonical shared operational dictionary value 'ready' for dictionary
    group 'workflow_stage_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: workflow_stage_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: in_progress
  label_uk: У роботі
  label_en: In Progress
  description: Canonical shared operational dictionary value 'in_progress' for dictionary
    group 'workflow_stage_status'.
  status: active
  aliases:
  - у роботі
  owner_module: forprint_library
  dictionary_group: workflow_stage_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: blocked
  label_uk: Заблоковано
  label_en: Blocked
  description: Canonical shared operational dictionary value 'blocked' for dictionary
    group 'workflow_stage_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: workflow_stage_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: waiting_external_contractor
  label_uk: Очікування зовнішнього підрядника
  label_en: Waiting External Contractor
  description: Canonical shared operational dictionary value 'waiting_external_contractor'
    for dictionary group 'workflow_stage_status'.
  status: active
  aliases:
  - external_contractor_wait
  owner_module: forprint_library
  dictionary_group: workflow_stage_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: completed
  label_uk: Завершено
  label_en: Completed
  description: Canonical shared operational dictionary value 'completed' for dictionary
    group 'workflow_stage_status'.
  status: active
  aliases:
  - завершено
  owner_module: forprint_library
  dictionary_group: workflow_stage_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: cancelled
  label_uk: Скасовано
  label_en: Cancelled
  description: Canonical shared operational dictionary value 'cancelled' for dictionary
    group 'workflow_stage_status'.
  status: active
  aliases:
  - скасовано
  owner_module: forprint_library
  dictionary_group: workflow_stage_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: late
  label_uk: Прострочено
  label_en: Late
  description: Canonical shared operational dictionary value 'late' for dictionary
    group 'workflow_stage_status'.
  status: active
  aliases:
  - прострочений етап
  owner_module: forprint_library
  dictionary_group: workflow_stage_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: manual_review_required
  label_uk: Потрібна ручна перевірка
  label_en: Manual Review Required
  description: Canonical shared operational dictionary value 'manual_review_required'
    for dictionary group 'workflow_stage_status'.
  status: active
  aliases:
  - manual_review
  - ручна перевірка
  owner_module: forprint_library
  dictionary_group: workflow_stage_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: unknown
  label_uk: Невідомо
  label_en: Unknown
  description: Canonical shared operational dictionary value 'unknown' for dictionary
    group 'workflow_stage_status'.
  status: active
  aliases:
  - невідомо
  owner_module: forprint_library
  dictionary_group: workflow_stage_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
```

## Primary source

**Path:** `dictionaries/workflow_status.yaml`
**SHA256:** `edb3c09b793a0b4bf59ccf9785cdef98ef5dd1db1df1661089dc799404e5ed8e`

```yaml
dictionary_group: workflow_status
metadata:
  id: shared_operational_dictionary_v0_1
  name: Shared Operational Dictionary v0.1
  version: '0.1'
  dictionary_status: draft_shared_operational_dictionary_v0_1
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  unit_dictionary_status: not_final_inventory_unit_system
entries:
- id: not_started
  label_uk: Не розпочато
  label_en: Not Started
  description: Canonical shared operational dictionary value 'not_started' for dictionary
    group 'workflow_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: workflow_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: active
  label_uk: Активний
  label_en: Active
  description: Canonical shared operational dictionary value 'active' for dictionary
    group 'workflow_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: workflow_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: blocked
  label_uk: Заблоковано
  label_en: Blocked
  description: Canonical shared operational dictionary value 'blocked' for dictionary
    group 'workflow_status'.
  status: active
  aliases: []
  owner_module: forprint_library
  dictionary_group: workflow_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: completed
  label_uk: Завершено
  label_en: Completed
  description: Canonical shared operational dictionary value 'completed' for dictionary
    group 'workflow_status'.
  status: active
  aliases:
  - завершено
  owner_module: forprint_library
  dictionary_group: workflow_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: cancelled
  label_uk: Скасовано
  label_en: Cancelled
  description: Canonical shared operational dictionary value 'cancelled' for dictionary
    group 'workflow_status'.
  status: active
  aliases:
  - скасовано
  owner_module: forprint_library
  dictionary_group: workflow_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: manual_review_required
  label_uk: Потрібна ручна перевірка
  label_en: Manual Review Required
  description: Canonical shared operational dictionary value 'manual_review_required'
    for dictionary group 'workflow_status'.
  status: active
  aliases:
  - manual_review
  - ручна перевірка
  owner_module: forprint_library
  dictionary_group: workflow_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
- id: unknown
  label_uk: Невідомо
  label_en: Unknown
  description: Canonical shared operational dictionary value 'unknown' for dictionary
    group 'workflow_status'.
  status: active
  aliases:
  - невідомо
  owner_module: forprint_library
  dictionary_group: workflow_status
  version: '0.1'
  notes: Draft shared operational dictionary entry.
```

## Primary source

**Path:** `schemas/dictionary_entry.schema.yaml`
**SHA256:** `ce8d1fa752b0e29b55dc053012f1ddd6c6b64219d55be02147b8985b345cee16`

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: ForPrint Dictionary Entry
type: object
required:
- id
- label_uk
- label_en
- description
- status
- aliases
- owner_module
- dictionary_group
- version
- notes
properties:
  id:
    type: string
    pattern: ^[a-z0-9_]+$
  label_uk:
    type: string
    minLength: 1
  label_en:
    type: string
    minLength: 1
  description:
    type: string
    minLength: 1
  status:
    enum:
    - active
    - draft
    - deprecated
  aliases:
    type: array
    items:
      type: string
      minLength: 1
  owner_module:
    const: forprint_library
  dictionary_group:
    type: string
    minLength: 1
  version:
    const: '0.1'
  notes:
    type: string
additionalProperties: true
```

## Primary source

**Path:** `schemas/shared_operational_dictionary.schema.yaml`
**SHA256:** `385e35f4b33d6e41ad6452ccc23e3d7db8ca9b9afa805614b571b049d354d02b`

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: ForPrint Shared Operational Dictionary
type: object
required:
- metadata
- dictionary_groups
properties:
  metadata:
    type: object
    required:
    - id
    - version
    - dictionary_status
    - schema_status
    - usage
    - contract_status
    - owner_module
    properties:
      id:
        type: string
      name:
        type: string
      version:
        const: '0.1'
      dictionary_status:
        const: draft_shared_operational_dictionary_v0_1
      schema_status:
        const: unstable_v0_1
      usage:
        const: allowed_for_projection_use
      contract_status:
        const: not_final_contract
      owner_module:
        const: forprint_library
      unit_dictionary_status:
        const: not_final_inventory_unit_system
    additionalProperties: true
  dictionary_groups:
    type: object
    required:
    - source_system
    - entity_type
    - order_status
    - order_line_status
    - payment_status
    - production_status
    - workflow_status
    - workflow_stage_status
    - material_requirement_status
    - reference_resolution_status
    - product_service_reference_status
    - contractor_reference_status
    - deadline_type
    - alert_rule_type
    - alert_severity
    - alert_event_status
    - notification_status
    - unit
    properties:
      source_system:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      entity_type:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      order_status:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      order_line_status:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      payment_status:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      production_status:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      workflow_status:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      workflow_stage_status:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      material_requirement_status:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      reference_resolution_status:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      product_service_reference_status:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      contractor_reference_status:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      deadline_type:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      alert_rule_type:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      alert_severity:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      alert_event_status:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      notification_status:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
      unit:
        type: array
        items:
          $ref: '#/$defs/dictionary_entry'
    additionalProperties: false
additionalProperties: false
$defs:
  dictionary_entry:
    $schema: https://json-schema.org/draft/2020-12/schema
    title: ForPrint Dictionary Entry
    type: object
    required:
    - id
    - label_uk
    - label_en
    - description
    - status
    - aliases
    - owner_module
    - dictionary_group
    - version
    - notes
    properties:
      id:
        type: string
        pattern: ^[a-z0-9_]+$
      label_uk:
        type: string
        minLength: 1
      label_en:
        type: string
        minLength: 1
      description:
        type: string
        minLength: 1
      status:
        enum:
        - active
        - draft
        - deprecated
      aliases:
        type: array
        items:
          type: string
          minLength: 1
      owner_module:
        const: forprint_library
      dictionary_group:
        type: string
        minLength: 1
      version:
        const: '0.1'
      notes:
        type: string
    additionalProperties: true
```

## Primary source

**Path:** `scripts/export_dictionary_policy_docs.py`
**SHA256:** `53a87594cc61cf44667c22a5fe0795c1ef3bd70d9a4aa4f980b2e1fbdd8bd93f`

```python
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs" / "architecture"

DOCS: dict[str, str] = {
    "shared_operational_dictionary_policy.md": """# Shared Operational Dictionary Policy

## Status

Draft policy for Shared Operational Dictionary v0.1.

## Purpose

Library owns canonical shared operational dictionary definitions.
ForPrint Library owns canonical shared operational 
dictionary definitions for the ForPrint ecosystem.

These dictionaries define stable operational IDs, labels, descriptions, 
aliases, statuses and versioning rules for concepts reused by 
Operational Registry, Calculator Engine, 
Accounting Registry, Telegram Bot, CRM, Gateway, Prepress Hub, 
Warehouse, Logistics, Website and future Mobile App.

## Core rule

Library defines canonical dictionary values.

Other modules may consume these values, reference them, display 
their labels and create temporary local projections, 
but they must not become independent permanent dictionary authorities.

## Boundary

This dictionary layer does not create real operational orders, real clients, real payments, 
real material stock, real warehouse records, Calculator formulas, 
Telegram runtime, CRM dashboard or 1C synchronization.

Operational Registry owns operational facts and records.

Library owns canonical operational language and semantic references.
""",
    "status_dictionary_policy.md": """# Status Dictionary Policy

## Status

Draft policy for shared status dictionaries.

## Purpose

Shared status dictionaries prevent modules from inventing 
conflicting values for the same operational state.

Examples include order_status, order_line_status, payment_status, 
production_status, workflow_status, workflow_stage_status, 
material_requirement_status, alert_event_status and notification_status.

## Stable IDs

Status IDs are stable machine values.

Labels may change, but IDs should remain stable unless a migration or deprecation rule is created.

## Consumption

Operational Registry should later reference these canonical values for operational records.

Calculator Engine should use these values when producing output packages.

Telegram Bot and CRM should display labels and must not invent internal status IDs.

Accounting Registry may map accounting statuses carefully 
without becoming the source of operational truth.

## Deprecated values

Deprecated values remain readable for historical records and migrations.
""",
    "source_system_dictionary_policy.md": """# Source System Dictionary Policy

## Status

Draft policy for the source_system dictionary.

## Purpose

source_system defines canonical IDs for systems, 
modules and external sources that produce or reference data in the ForPrint ecosystem.

Examples include forprint_operational_registry, forprint_library, calculator_engine, 
accounting_registry_service, telegram_bot, forprint_crm, 
forprint_integration_gateway, one_c_bas, manual_entry and unknown.

## Rule

Modules should store canonical source_system IDs when recording provenance, 
imports, projections or references.

Aliases may help import and display, but canonical IDs remain the stable internal truth.
""",
    "entity_type_dictionary_policy.md": """# Entity Type Dictionary Policy

## Status

Draft policy for the entity_type dictionary.

## Purpose

entity_type defines canonical IDs for shared business and operational concepts.

Examples include client_account, client_group, order, order_line, 
product_service_reference, material_requirement, payment_projection, 
workflow_stage, deadline_control, contractor_reference, alert_event and report_projection.

## Rule

Modules should reference canonical entity_type IDs in logs, alerts, reports, projections, 
integration messages and resolution records.

Entity type IDs do not mean Library owns the records. 
Operational records remain owned by their responsible modules.
""",
    "unit_dictionary_policy.md": """# Unit Dictionary Policy

## Status

Draft policy for the shared unit dictionary.

## Scope

The current unit dictionary is intentionally small and draft.

It includes values such as pcs, set, m, m2, kg, g, l, ml, hour, minute, service and unknown.

## Important limitation

This is marked as:

```yaml
dictionary_status: draft_shared_operational_dictionary_v0_1
unit_dictionary_status: not_final_inventory_unit_system

It is not a final inventory, warehouse or accounting unit system.

Future Warehouse, Accounting Registry and Library work may refine units, 
conversions and inventory-specific rules.
""",
"dictionary_consumption_policy.md": """# Dictionary Consumption Policy

Status

Draft policy for consuming Library dictionaries.

General rule

Dependent modules may consume Library dictionaries as projection input and validation references.

They should reference canonical IDs and display labels, 
not invent new internal IDs for shared operational concepts.

Operational Registry

Operational Registry should later reference these canonical values for statuses, 
entity types, source systems, alerts, deadlines and reference resolution states.

Calculator Engine

Calculator Engine should use these values when producing structured output packages, 
especially for source_system, entity_type, 
reference_resolution_status and product_service_reference_status.

Accounting Registry

Accounting Registry may map accounting statuses carefully, 
but it must not become the source of operational truth.

Telegram Bot and CRM

Telegram Bot and CRM should display labels and route ambiguous or 
unknown values for review instead of inventing canonical IDs.

Deprecated values

Deprecated dictionary values remain readable for historical records.
""",
"dictionary_versioning_policy.md": """# Dictionary Versioning Policy

Status

Draft policy for dictionary versioning.

Current version

Shared Operational Dictionary v0.1 uses:

version: "0.1"
dictionary_status: draft_shared_operational_dictionary_v0_1
schema_status: unstable_v0_1
usage: allowed_for_projection_use
contract_status: not_final_contract
owner_module: forprint_library
Stability

Dictionary IDs should be treated as stable once used by dependent modules.

Labels and descriptions may change more freely than IDs.

Deprecation

Deprecated values must remain readable for historical records and migrations.

New values should be added rather than silently changing the meaning of existing IDs.

Compatibility

Dependent modules should keep dictionary projections rebuildable from Library sources.
""",
}

def main() -> int:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    for filename, content in DOCS.items():
        path = DOCS_DIR / filename
        path.write_text(content.rstrip() + "\n", encoding="utf-8")
        print(f"OK: wrote {path.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Primary source

**Path:** `scripts/export_shared_dictionary_coordination_artifacts.py`
**SHA256:** `528fbb920edfed9c8e9247181f0cf8a0a41e78f665b695453831a8d90411e00a`

```python
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]

REPORT_ID = "2026-06-09__forprint_library__report__shared-operational-dictionary-v0-1"
REPORT_PATH = ROOT / "coordination" / "reports" / "completion" / f"{REPORT_ID}.md"

STATUS_YAML = ROOT / "coordination" / "status" / "current_status.yaml"
STATUS_MD = ROOT / "coordination" / "status" / "current_status.md"
REPORTS_INDEX = ROOT / "coordination" / "reports" / "index.yaml"

CHECKPOINT_A_COMMIT = "18900ee"
CHECKPOINT_B_COMMIT = "2fc7694"


def read_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML file must contain a mapping: {path}")
    return data


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    print(f"OK: wrote {path.relative_to(ROOT)}")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    print(f"OK: wrote {path.relative_to(ROOT)}")


def update_current_status_yaml() -> None:
    status = read_yaml(STATUS_YAML)

    status["module_id"] = "forprint_library"
    status["status"] = "shared_operational_dictionary_v0_1_ready_pending_blueprint_review"
    status["stage"] = "shared_operational_dictionary_v0_1_checkpoint_c"
    status["updated_at"] = "2026-06-09"
    status["owner_module"] = "forprint_library"
    status["current_phase"] = "shared_operational_dictionary_v0_1"
    status["last_completed_step"] = "shared_operational_dictionary_ready"

    status["current_focus"] = [
        "shared operational dictionary v0.1",
        "canonical enum and status definitions",
        "dictionary resolver and terminal preview",
        "dictionary architecture policy documentation",
        "coordination report for Blueprint review",
    ]

    status.setdefault(
        "boundary_confirmation",
        {
            "owns": [
                "canonical catalog semantics",
                "stable catalog IDs",
                "aliases",
                "contract definitions",
                "canonical dictionary IDs",
                "canonical enum values",
                "shared operational status definitions",
            ],
            "does_not_own": [
                "clients",
                "orders",
                "payments",
                "warehouse stock truth",
                "production runtime",
                "1C synchronization",
                "CRM workflow",
                "Telegram runtime",
                "Calculator logic",
            ],
        },
    )

    status["shared_operational_dictionary_v0_1"] = {
        "dictionary_status": "draft_shared_operational_dictionary_v0_1",
        "schema_status": "unstable_v0_1",
        "usage": "allowed_for_projection_use",
        "contract_status": "not_final_contract",
        "owner_module": "forprint_library",
        "unit_dictionary_status": "not_final_inventory_unit_system",
        "dictionary_groups_count": 18,
        "dictionary_files": "done",
        "schemas": "done",
        "loader_validation": "done",
        "resolver": "done",
        "terminal_preview": "done",
        "examples": "done",
        "architecture_docs": "done",
        "check_report_extension": "done",
        "coordination_report": "done",
    }

    status["shared_operational_dictionary_checkpoints"] = {
        "checkpoint_a": {
            "name": "dictionary_files_and_schemas",
            "status": "done",
            "commit": CHECKPOINT_A_COMMIT,
        },
        "checkpoint_b": {
            "name": "resolver_examples_and_preview",
            "status": "done",
            "commit": CHECKPOINT_B_COMMIT,
        },
        "checkpoint_c": {
            "name": "docs_check_report_and_coordination",
            "status": "in_progress_until_final_commit",
            "commit": "pending",
        },
    }

    status["next_recommended_step"] = {
        "status": "wait_for_blueprint_review",
        "options": [
            "align Operational Registry local enum values with Library dictionary IDs",
            "create Blueprint module directive index for forprint_library",
            "define projection export contract for consuming modules",
            "extend dictionary aliases based on real sanitized module usage",
        ],
    }

    write_yaml(STATUS_YAML, status)


def update_current_status_md() -> None:
    content = """# ForPrint Library Current Status

    Status: `shared_operational_dictionary_v0_1_ready_pending_blueprint_review`

    ForPrint Library has completed Shared Operational Dictionary / Enum Canonicalization v0.1.

    ## Current phase

    `shared_operational_dictionary_v0_1`

    ## Last completed step

    `shared_operational_dictionary_ready`

    ## Completed shared dictionary checkpoints

    ### Checkpoint A

    Dictionary files, schemas, loader validation and tests.

    ```text
    18900ee Add shared operational dictionary files
    Checkpoint B

    Dictionary resolver, resolution examples and terminal preview.

    2fc7694 Add shared dictionary resolver and preview
    Checkpoint C

    Dictionary architecture docs, check-report extension and coordination report.

    pending final commit
    Shared dictionary status
    dictionary_status: draft_shared_operational_dictionary_v0_1
    schema_status: unstable_v0_1
    usage: allowed_for_projection_use
    contract_status: not_final_contract
    owner_module: forprint_library
    unit_dictionary_status: not_final_inventory_unit_system
    Boundary confirmation

    This step added canonical dictionary IDs, enum values, status definitions,
    labels, aliases, schemas, docs, resolver helpers and terminal preview.

    It did not add real operational orders, real clients, real payments, real
    material stock, real product catalog, real 1C sync, Calculator formulas,
    Telegram runtime, CRM dashboard or Warehouse stock truth.

    Recommended next step

    Pause Library after final commit and pass the completion report to ForPrint
    System Blueprint for review.
    """
    write_text(STATUS_MD, content)

def update_reports_index() -> None:
    index = read_yaml(REPORTS_INDEX)
    index["module_id"] = "forprint_library"
    index["index_type"] = "coordination_reports"
    index["updated_at"] = "2026-06-09"

    completion_reports = index.setdefault("completion_reports", [])
    if not any(item.get("id") == REPORT_ID for item in completion_reports):
        completion_reports.append(
            {
                "id": REPORT_ID,
                "path": str(REPORT_PATH.relative_to(ROOT)),
                "status": "completed",
                "phase": "shared_operational_dictionary_v0_1",
                "summary": "Shared Operational Dictionary v0.1 completion report.",
            }
        )

    commit_reports = index.setdefault("commit_reports", [])

    commit_items = [
        {
            "id": "shared_dictionary_checkpoint_a",
            "commit": CHECKPOINT_A_COMMIT,
            "message": "Add shared operational dictionary files",
            "status": "pushed",
        },
        {
            "id": "shared_dictionary_checkpoint_b",
            "commit": CHECKPOINT_B_COMMIT,
            "message": "Add shared dictionary resolver and preview",
            "status": "pushed",
        },
        {
            "id": "shared_dictionary_checkpoint_c",
            "commit": "pending",
            "message": "Finalize shared operational dictionary checkpoint",
            "status": "pending_final_commit",
        },
    ]

    existing_ids = {item.get("id") for item in commit_reports}
    for item in commit_items:
        if item["id"] not in existing_ids:
            commit_reports.append(item)

    write_yaml(REPORTS_INDEX, index)

def write_completion_report() -> None:
    content = """
    # ForPrint Library Shared Operational Dictionary v0.1 Report

    Report ID: 2026-06-09__forprint_library__report__shared-operational-dictionary-v0-1

    Module: forprint_library

    Local path:

    /srv/software_development/forprint-project/forprint_library
    1. Files added or changed

    Major areas added or updated:

    app/forprint_library/dictionaries/
    dictionaries/
    schemas/dictionary_entry.schema.yaml
    schemas/shared_operational_dictionary.schema.yaml
    examples/dictionaries/
    scripts/export_shared_operational_dictionaries.py
    scripts/validate_shared_operational_dictionaries.py
    scripts/preview_shared_operational_dictionaries.py
    scripts/export_dictionary_policy_docs.py
    tests/contract/test_shared_operational_dictionary_v0_1.py
    tests/integration/test_dictionary_resolver_and_preview.py
    tests/contract/test_dictionary_policy_docs.py
    tests/contract/test_shared_dictionary_check_report_surface.py
    docs/architecture/*dictionary_policy.md
    coordination/status/current_status.yaml
    coordination/status/current_status.md
    coordination/reports/index.yaml
    2. Dictionary groups added

    Shared Operational Dictionary v0.1 added 18 canonical groups:

    source_system
    entity_type
    order_status
    order_line_status
    payment_status
    production_status
    workflow_status
    workflow_stage_status
    material_requirement_status
    reference_resolution_status
    product_service_reference_status
    contractor_reference_status
    deadline_type
    alert_rule_type
    alert_severity
    alert_event_status
    notification_status
    unit
    3. Schemas added

    Added schema files:

    schemas/dictionary_entry.schema.yaml
    schemas/shared_operational_dictionary.schema.yaml

    The schemas validate required entry fields, owner module, version, metadata
    status terms and shared dictionary structure.

    4. Loader and resolver behavior

    The dictionary package now supports:

    load_dictionary(group_name)
    load_shared_dictionary()
    list_dictionary_groups()
    validate_dictionary_entry(entry)
    validate_shared_dictionary()
    resolve_dictionary_value(group_name, value_or_alias)

    Resolution statuses:

    confirmed
    confirmed_with_alias
    unresolved
    ambiguous_manual_review_required
    deprecated_reference
    5. Examples added

    Safe demo fixtures added:

    examples/dictionaries/demo_shared_operational_dictionary.yaml
    examples/dictionaries/demo_dictionary_resolution_cases.yaml

    They demonstrate exact ID resolution, alias resolution, unknown value handling,
    deprecated value handling, ambiguous alias handling and display label usage.

    No real client, product, material, payment or order data was added.

    6. Terminal preview summary

    Added:

    make dictionary-preview

    The preview renders:

    DICTIONARY GROUPS
    SOURCE SYSTEMS
    ENTITY TYPES
    ORDER / WORKFLOW STATUSES
    PAYMENT / MATERIAL STATUSES
    ALERT STATUSES
    UNITS
    RESOLUTION EXAMPLES
    7. Architecture docs added

    Added dictionary policy docs:

    docs/architecture/shared_operational_dictionary_policy.md
    docs/architecture/status_dictionary_policy.md
    docs/architecture/source_system_dictionary_policy.md
    docs/architecture/entity_type_dictionary_policy.md
    docs/architecture/unit_dictionary_policy.md
    docs/architecture/dictionary_consumption_policy.md
    docs/architecture/dictionary_versioning_policy.md

    These docs confirm that Library owns canonical dictionary definitions while
    Operational Registry owns operational facts and records.

    8. Tests added and results

    Test coverage added for:

    shared dictionary loading;
    dictionary group existence;
    unique IDs within groups;
    required entry fields;
    alias list validation;
    duplicate alias detection/reporting;
    required values for source_system, entity_type, order_status, payment_status,
    workflow_stage_status, material_requirement_status, alert_severity and unit;
    schema validation;
    resolver exact ID matches;
    resolver alias matches;
    unknown values;
    deprecated values;
    ambiguous aliases;
    dictionary preview rendering;
    dictionary architecture docs;
    Library boundary against operational records.

    Latest known result before final commit:

    72 passed
    9. Check-report result

    The Library check-report now includes shared dictionary rows:

    Shared dictionary files
    Dictionary schemas
    Dictionary group files
    Dictionary required values
    Dictionary resolver/examples
    Dictionary preview

    Latest known check-report state before final commit:

    all rows OK
    10. Makefile targets added

    Added or confirmed:

    dictionary-preview
    status-report

    Existing standard targets remain:

    lint
    lint-fix
    test
    check
    check-report
    blueprint-pull
    blueprint-check
    blueprint-sync-directives
    coordination-check
    coordination-fix
    module-policy-check
    11. Coordination status and report updates

    Updated:

    coordination/status/current_status.yaml
    coordination/status/current_status.md
    coordination/reports/index.yaml
    coordination/reports/completion/2026-06-09__forprint_library__report__shared-operational-dictionary-v0-1.md

    Suggested phase:

    current_phase: shared_operational_dictionary_v0_1
    last_completed_step: shared_operational_dictionary_ready
    12. Boundary confirmation

    This step does not add:

    real operational orders
    real clients
    real payments
    real material stock
    real product catalog
    real 1C sync
    Calculator formulas
    Telegram runtime
    CRM dashboard
    Warehouse stock truth

    Library defines canonical operational language and semantic references.

    Operational Registry owns operational facts and records.

    13. Commit hashes

    Completed shared dictionary checkpoint commits:

    18900ee Add shared operational dictionary files
    2fc7694 Add shared dictionary resolver and preview

    Final Checkpoint C commit is pending at report creation time:

    pending: Finalize shared operational dictionary checkpoint
    14. Push status

    Checkpoint A and B are pushed to origin/main.

    Checkpoint C should be pushed after final validation.

    15. Open questions for Blueprint
    Should Operational Registry now map its local enum values to 
    Library canonical dictionary IDs?
    Should Blueprint create a module directive index for forprint_library?
    Should dictionary projections be exported through YAML only for now, 
    or should a read-only API contract be designed?
    Should aliases be approved by Library directly, or routed through CRM/human review?
    Should Warehouse and Accounting Registry jointly refine the 
    unit dictionary before production use?
    16. Recommended next step

    Recommended next step:

    Pass this report to ForPrint System Blueprint and align Operational
    Registry local statuses with Library shared dictionary IDs.

    """
    write_text(REPORT_PATH, content)

def main() -> int:
    update_current_status_yaml()
    update_current_status_md()
    update_reports_index()
    write_completion_report()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

## Primary source

**Path:** `scripts/export_shared_operational_dictionaries.py`
**SHA256:** `1452c1e03b008d503db3bcf3aae322b8e546e93cfb455e73c91e315a31cf0f6e`

```python
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DICTIONARIES_DIR = ROOT / "dictionaries"
SCHEMAS_DIR = ROOT / "schemas"

OWNER_MODULE = "forprint_library"
VERSION = "0.1"

DICTIONARY_VALUES: dict[str, list[str]] = {
    "source_system": [
        "forprint_operational_registry",
        "forprint_library",
        "calculator_engine",
        "accounting_registry_service",
        "telegram_bot",
        "forprint_crm",
        "forprint_integration_gateway",
        "forprint_prepress_hub",
        "warehouse_service",
        "logistics_service",
        "website",
        "mobile_app",
        "one_c_bas",
        "sanitized_demo",
        "manual_entry",
        "unknown",
    ],
    "entity_type": [
        "client_account",
        "client_group",
        "contact_person",
        "contact_method",
        "client_address",
        "legal_entity_profile",
        "external_reference",
        "order",
        "order_line",
        "calculator_output_package",
        "product_service_reference",
        "material_requirement",
        "payment_projection",
        "workflow_template",
        "workflow_stage",
        "deadline_control",
        "contractor_reference",
        "alert_rule",
        "alert_event",
        "report_definition",
        "report_projection",
        "operational_event",
        "unknown",
    ],
    "order_status": [
        "draft",
        "needs_review",
        "confirmed",
        "in_progress",
        "completed",
        "cancelled",
        "blocked",
        "manual_review_required",
        "archived",
        "unknown",
    ],
    "order_line_status": [
        "draft",
        "pending_reference_resolution",
        "ready",
        "in_progress",
        "completed",
        "cancelled",
        "manual_review_required",
        "unknown",
    ],
    "payment_status": [
        "not_invoiced",
        "invoice_reference_pending",
        "unpaid",
        "partially_paid",
        "paid_reference_confirmed",
        "overdue",
        "cancelled",
        "unknown",
    ],
    "production_status": [
        "not_started",
        "ready",
        "in_progress",
        "waiting_external_contractor",
        "blocked",
        "completed",
        "cancelled",
        "unknown",
    ],
    "workflow_status": [
        "not_started",
        "active",
        "blocked",
        "completed",
        "cancelled",
        "manual_review_required",
        "unknown",
    ],
    "workflow_stage_status": [
        "not_started",
        "ready",
        "in_progress",
        "blocked",
        "waiting_external_contractor",
        "completed",
        "cancelled",
        "late",
        "manual_review_required",
        "unknown",
    ],
    "material_requirement_status": [
        "planned",
        "library_reference_pending",
        "warehouse_reference_pending",
        "reserved_reference_pending",
        "confirmed",
        "fulfilled",
        "cancelled",
        "unknown",
    ],
    "reference_resolution_status": [
        "draft_display_only",
        "reference_pending",
        "reference_confirmed",
        "ambiguous_manual_review_required",
        "deprecated_reference",
        "unknown",
    ],
    "product_service_reference_status": [
        "draft_display_only",
        "library_reference_pending",
        "library_reference_confirmed",
        "ambiguous_manual_review_required",
        "deprecated_reference",
        "unknown",
    ],
    "contractor_reference_status": [
        "display_only",
        "client_account_reference_pending",
        "client_account_reference_confirmed",
        "external_reference_pending",
        "manual_review_required",
        "unknown",
    ],
    "deadline_type": [
        "order_due",
        "stage_due",
        "payment_due",
        "material_required_by",
        "manual_review_due",
        "unknown",
    ],
    "alert_rule_type": [
        "workflow_stage_late",
        "order_deadline_near",
        "payment_overdue",
        "material_requirement_unresolved",
        "manual_review_stale",
        "contractor_stage_blocked",
        "unknown",
    ],
    "alert_severity": [
        "info",
        "warning",
        "high",
        "critical",
        "unknown",
    ],
    "alert_event_status": [
        "open",
        "acknowledged",
        "resolved",
        "ignored",
        "failed_to_notify",
        "unknown",
    ],
    "notification_status": [
        "not_sent",
        "queued",
        "sent",
        "failed",
        "disabled",
        "unknown",
    ],
    "unit": [
        "pcs",
        "set",
        "m",
        "m2",
        "kg",
        "g",
        "l",
        "ml",
        "hour",
        "minute",
        "service",
        "unknown",
    ],
}

UK_LABEL_OVERRIDES: dict[str, str] = {
    "draft": "Чернетка",
    "needs_review": "Потребує перевірки",
    "confirmed": "Підтверджено",
    "in_progress": "У роботі",
    "completed": "Завершено",
    "cancelled": "Скасовано",
    "blocked": "Заблоковано",
    "manual_review_required": "Потрібна ручна перевірка",
    "archived": "Архівовано",
    "unknown": "Невідомо",
    "ready": "Готово",
    "active": "Активний",
    "late": "Прострочено",
    "not_started": "Не розпочато",
    "waiting_external_contractor": "Очікування зовнішнього підрядника",
    "unpaid": "Не оплачено",
    "partially_paid": "Частково оплачено",
    "paid_reference_confirmed": "Підтверджено оплату",
    "overdue": "Прострочено",
    "planned": "Заплановано",
    "fulfilled": "Виконано",
    "open": "Відкрито",
    "acknowledged": "Підтверджено оператором",
    "resolved": "Вирішено",
    "ignored": "Проігноровано",
    "failed": "Помилка",
    "disabled": "Вимкнено",
    "queued": "У черзі",
    "sent": "Надіслано",
    "not_sent": "Не надіслано",
    "info": "Інформаційно",
    "warning": "Попередження",
    "high": "Високий",
    "critical": "Критичний",
    "pcs": "Штуки",
    "set": "Комплект",
    "m": "Метри",
    "m2": "Квадратні метри",
    "kg": "Кілограми",
    "g": "Грами",
    "l": "Літри",
    "ml": "Мілілітри",
    "hour": "Година",
    "minute": "Хвилина",
    "service": "Послуга",
    "one_c_bas": "1C/BAS",
}

ALIASES: dict[str, list[str]] = {
    "forprint_operational_registry": ["operational_registry", "opr"],
    "forprint_library": ["library"],
    "calculator_engine": ["calculator"],
    "accounting_registry_service": ["accounting_registry"],
    "telegram_bot": ["telegram"],
    "one_c_bas": ["1c", "bas", "1c_bas"],
    "manual_entry": ["manual", "ручне введення"],
    "draft": ["чернетка"],
    "confirmed": ["підтверджено"],
    "in_progress": ["у роботі"],
    "completed": ["завершено"],
    "cancelled": ["скасовано"],
    "manual_review_required": ["manual_review", "ручна перевірка"],
    "unpaid": ["не оплачено"],
    "partially_paid": ["частково оплачено"],
    "overdue": ["прострочено"],
    "paid_reference_confirmed": ["paid", "оплачено"],
    "waiting_external_contractor": ["external_contractor_wait"],
    "late": ["прострочений етап"],
    "warehouse_reference_pending": ["warehouse_pending"],
    "warning": ["warn"],
    "critical": ["crit"],
    "pcs": ["piece", "pieces", "шт"],
    "m2": ["sqm", "square_meter", "м2"],
    "service": ["послуга"],
    "unknown": ["невідомо"],
}

DEPRECATED_VALUES: set[tuple[str, str]] = {
    ("reference_resolution_status", "deprecated_reference"),
    ("product_service_reference_status", "deprecated_reference"),
}

METADATA: dict[str, str] = {
    "id": "shared_operational_dictionary_v0_1",
    "name": "Shared Operational Dictionary v0.1",
    "version": VERSION,
    "dictionary_status": "draft_shared_operational_dictionary_v0_1",
    "schema_status": "unstable_v0_1",
    "usage": "allowed_for_projection_use",
    "contract_status": "not_final_contract",
    "owner_module": OWNER_MODULE,
    "unit_dictionary_status": "not_final_inventory_unit_system",
}


def title_from_id(value: str) -> str:
    return value.replace("_", " ").title()


def label_uk(value: str) -> str:
    return UK_LABEL_OVERRIDES.get(value, title_from_id(value))


def build_entry(group_name: str, value: str) -> dict[str, Any]:
    status = "deprecated" if (group_name, value) in DEPRECATED_VALUES else "active"

    return {
        "id": value,
        "label_uk": label_uk(value),
        "label_en": title_from_id(value),
        "description": (
            f"Canonical shared operational dictionary value '{value}' "
            f"for dictionary group '{group_name}'."
        ),
        "status": status,
        "aliases": ALIASES.get(value, []),
        "owner_module": OWNER_MODULE,
        "dictionary_group": group_name,
        "version": VERSION,
        "notes": "Draft shared operational dictionary entry.",
    }


def dictionary_entry_schema() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "ForPrint Dictionary Entry",
        "type": "object",
        "required": [
            "id",
            "label_uk",
            "label_en",
            "description",
            "status",
            "aliases",
            "owner_module",
            "dictionary_group",
            "version",
            "notes",
        ],
        "properties": {
            "id": {"type": "string", "pattern": "^[a-z0-9_]+$"},
            "label_uk": {"type": "string", "minLength": 1},
            "label_en": {"type": "string", "minLength": 1},
            "description": {"type": "string", "minLength": 1},
            "status": {"enum": ["active", "draft", "deprecated"]},
            "aliases": {
                "type": "array",
                "items": {"type": "string", "minLength": 1},
            },
            "owner_module": {"const": OWNER_MODULE},
            "dictionary_group": {"type": "string", "minLength": 1},
            "version": {"const": VERSION},
            "notes": {"type": "string"},
        },
        "additionalProperties": True,
    }


def shared_dictionary_schema() -> dict[str, Any]:
    group_properties = {
        group_name: {
            "type": "array",
            "items": {"$ref": "#/$defs/dictionary_entry"},
        }
        for group_name in DICTIONARY_VALUES
    }

    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "ForPrint Shared Operational Dictionary",
        "type": "object",
        "required": ["metadata", "dictionary_groups"],
        "properties": {
            "metadata": {
                "type": "object",
                "required": [
                    "id",
                    "version",
                    "dictionary_status",
                    "schema_status",
                    "usage",
                    "contract_status",
                    "owner_module",
                ],
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"},
                    "version": {"const": VERSION},
                    "dictionary_status": {
                        "const": "draft_shared_operational_dictionary_v0_1"
                    },
                    "schema_status": {"const": "unstable_v0_1"},
                    "usage": {"const": "allowed_for_projection_use"},
                    "contract_status": {"const": "not_final_contract"},
                    "owner_module": {"const": OWNER_MODULE},
                    "unit_dictionary_status": {
                        "const": "not_final_inventory_unit_system"
                    },
                },
                "additionalProperties": True,
            },
            "dictionary_groups": {
                "type": "object",
                "required": list(DICTIONARY_VALUES),
                "properties": group_properties,
                "additionalProperties": False,
            },
        },
        "additionalProperties": False,
        "$defs": {"dictionary_entry": dictionary_entry_schema()},
    }


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    print(f"OK: wrote {path.relative_to(ROOT)}")


def export_shared_dictionary() -> dict[str, Any]:
    dictionary_groups = {
        group_name: [build_entry(group_name, value) for value in values]
        for group_name, values in DICTIONARY_VALUES.items()
    }

    shared_dictionary = {
        "metadata": METADATA,
        "dictionary_groups": dictionary_groups,
    }

    write_yaml(
        DICTIONARIES_DIR / "shared_operational_dictionary_v0_1.yaml",
        shared_dictionary,
    )

    return shared_dictionary


def export_group_dictionaries(shared_dictionary: dict[str, Any]) -> None:
    for group_name, entries in shared_dictionary["dictionary_groups"].items():
        payload = {
            "dictionary_group": group_name,
            "metadata": METADATA,
            "entries": entries,
        }
        write_yaml(DICTIONARIES_DIR / f"{group_name}.yaml", payload)


def export_schemas() -> None:
    write_yaml(SCHEMAS_DIR / "dictionary_entry.schema.yaml", dictionary_entry_schema())
    write_yaml(
        SCHEMAS_DIR / "shared_operational_dictionary.schema.yaml",
        shared_dictionary_schema(),
    )


def main() -> int:
    shared_dictionary = export_shared_dictionary()
    export_group_dictionaries(shared_dictionary)
    export_schemas()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Primary source

**Path:** `scripts/preview_shared_operational_dictionaries.py`
**SHA256:** `085cccc6240fd52f8daf0c6364202d9c0dbbdd361074503981b329ce2719a024`

```python
from __future__ import annotations

from forprint_library.dictionaries.loader import list_dictionary_groups, load_dictionary
from forprint_library.dictionaries.resolver import resolve_dictionary_value


def print_section(title: str) -> None:
    print()
    print(title)
    print("=" * len(title))


def print_entries(group_name: str, limit: int = 8) -> None:
    dictionary = load_dictionary(group_name)
    entries = dictionary["entries"]

    print(f"{group_name} ({len(entries)} values)")
    print("-" * 72)
    print(f"{'ID':<34} {'STATUS':<12} LABEL")
    print("-" * 72)

    for entry in entries[:limit]:
        print(f"{entry['id']:<34} {entry['status']:<12} {entry['label_en']}")

    if len(entries) > limit:
        print(f"... {len(entries) - limit} more")


def print_resolution_example(group_name: str, value: str) -> None:
    result = resolve_dictionary_value(group_name, value)
    print(
        f"{group_name:<32} input={value:<28} "
        f"status={result.status:<34} matched={result.matched_id}"
    )


def main() -> int:
    print("ForPrint Library — Shared Operational Dictionary v0.1 Preview")

    print_section("DICTIONARY GROUPS")
    groups = list_dictionary_groups()
    for group_name in groups:
        print(f"- {group_name}")

    print_section("SOURCE SYSTEMS")
    print_entries("source_system")

    print_section("ENTITY TYPES")
    print_entries("entity_type")

    print_section("ORDER / WORKFLOW STATUSES")
    for group_name in [
        "order_status",
        "order_line_status",
        "workflow_status",
        "workflow_stage_status",
        "production_status",
    ]:
        print_entries(group_name, limit=6)
        print()

    print_section("PAYMENT / MATERIAL STATUSES")
    for group_name in [
        "payment_status",
        "material_requirement_status",
        "reference_resolution_status",
        "product_service_reference_status",
    ]:
        print_entries(group_name, limit=6)
        print()

    print_section("ALERT STATUSES")
    for group_name in [
        "alert_rule_type",
        "alert_severity",
        "alert_event_status",
        "notification_status",
    ]:
        print_entries(group_name, limit=6)
        print()

    print_section("UNITS")
    print_entries("unit", limit=12)

    print_section("RESOLUTION EXAMPLES")
    for group_name, value in [
        ("source_system", "calculator_engine"),
        ("source_system", "calculator"),
        ("source_system", "not_existing_source"),
        ("reference_resolution_status", "deprecated_reference"),
        ("unit", "шт"),
        ("alert_severity", "crit"),
    ]:
        print_resolution_example(group_name, value)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Primary source

**Path:** `scripts/reference_contract/validate_library_reference_contract.py`
**SHA256:** `e712bbf253b28f7a93ba526daab1f9fa6952f32727404fa97c851f0bbded4d4c`

```python
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]

DOC_PATH = ROOT / "docs" / "architecture" / "reference_contract_foundation.md"
EXAMPLES_PATH = (
    ROOT / "examples" / "reference_contract" / "library_reference_examples.yaml"
)
SCHEMA_PATH = ROOT / "schemas" / "reference_contract" / "library_reference.schema.yaml"

EXPECTED_REFERENCE_TYPES = {
    "product_service",
    "material",
    "operation",
    "unit",
    "template",
    "technical_card",
}

EXPECTED_STATUSES = {
    "library_reference_confirmed",
    "library_reference_pending",
    "ambiguous_manual_review_required",
    "deprecated_reference",
    "unknown",
}

EXPECTED_SOURCE_MODULES = {
    "calculator_engine",
    "forprint_operational_registry",
    "forprint_integration_gateway",
    "telegram_bot",
    "future_forprint_crm",
    "forprint_library",
}

REFERENCE_ID_PATTERN = re.compile(
    r"^[a-z][a-z0-9_]*(\.[a-z0-9][a-z0-9_]*)+$"
)


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise AssertionError(f"Missing file: {path.relative_to(ROOT)}")

    data = yaml.safe_load(path.read_text(encoding="utf-8"))

    if not isinstance(data, dict):
        raise AssertionError(f"YAML root must be a mapping: {path.relative_to(ROOT)}")

    return data


def require_files() -> None:
    for path in [DOC_PATH, EXAMPLES_PATH, SCHEMA_PATH]:
        if not path.exists():
            raise AssertionError(f"Missing file: {path.relative_to(ROOT)}")


def validate_schema_file() -> None:
    schema = load_yaml(SCHEMA_PATH)

    if schema.get("$id") != "forprint_library.reference_contract.library_reference_v0_2":
        raise AssertionError("Unexpected schema $id")

    if schema.get("title") != "ForPrint Library Reference Contract v0.2":
        raise AssertionError("Unexpected schema title")

    required = set(schema.get("required", []))
    expected_required = {
        "schema_version",
        "reference_type",
        "reference_id",
        "display_label",
        "resolution_status",
        "source_module",
    }

    if not expected_required.issubset(required):
        missing = sorted(expected_required - required)
        raise AssertionError(f"Schema is missing required fields: {missing}")

    properties = schema.get("properties", {})

    if not isinstance(properties, dict):
        raise AssertionError("Schema properties must be a mapping")

    reference_type_enum = set(properties["reference_type"]["enum"])
    status_enum = set(properties["resolution_status"]["enum"])
    source_module_enum = set(properties["source_module"]["enum"])

    if reference_type_enum != EXPECTED_REFERENCE_TYPES:
        raise AssertionError("Schema reference_type enum mismatch")

    if status_enum != EXPECTED_STATUSES:
        raise AssertionError("Schema resolution_status enum mismatch")

    if source_module_enum != EXPECTED_SOURCE_MODULES:
        raise AssertionError("Schema source_module enum mismatch")


def validate_docs() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")

    required_phrases = [
        "Library Reference Contract Foundation v0.2",
        "canonical Library reference id format",
        "Downstream modules must not become owners",
        "library_reference_confirmed",
        "ambiguous_manual_review_required",
        "deprecated_reference",
        "unknown",
    ]

    for phrase in required_phrases:
        if phrase not in text:
            raise AssertionError(f"Document is missing phrase: {phrase}")

    forbidden_claims = [
        "Library owns order state",
        "Library owns pricing logic",
        "Library owns warehouse stock truth",
        "Library owns payment/accounting truth",
        "Library owns CRM workflow state",
        "Library owns Telegram runtime behavior",
        "Library owns Integration Gateway delivery ledger",
    ]

    for phrase in forbidden_claims:
        if phrase in text:
            raise AssertionError(f"Forbidden ownership claim found: {phrase}")


def validate_reference_id(reference_id: Any, status: str, example_id: str) -> None:
    if status == "unknown":
        if reference_id is not None:
            raise AssertionError(
                f"{example_id}: unknown references must keep reference_id null"
            )
        return

    if not isinstance(reference_id, str) or not reference_id:
        raise AssertionError(f"{example_id}: reference_id must be a non-empty string")

    if not REFERENCE_ID_PATTERN.match(reference_id):
        raise AssertionError(f"{example_id}: invalid reference_id: {reference_id}")


def validate_single_reference(example: dict[str, Any]) -> None:
    example_id = example.get("id", "<missing id>")

    payload = example.get("downstream_payload")
    if not isinstance(payload, dict):
        raise AssertionError(f"{example_id}: downstream_payload must be a mapping")

    reference = payload.get("library_reference")
    if not isinstance(reference, dict):
        raise AssertionError(f"{example_id}: library_reference must be a mapping")

    required_fields = {
        "schema_version",
        "reference_type",
        "reference_id",
        "display_label",
        "resolution_status",
        "source_module",
        "alias_input",
        "deprecation",
        "manual_review",
    }

    missing = sorted(required_fields - set(reference))
    if missing:
        raise AssertionError(f"{example_id}: missing fields: {missing}")

    if reference["schema_version"] != "library_reference_v0_2":
        raise AssertionError(f"{example_id}: invalid schema_version")

    reference_type = reference["reference_type"]
    status = reference["resolution_status"]
    source_module = reference["source_module"]

    if reference_type not in EXPECTED_REFERENCE_TYPES:
        raise AssertionError(f"{example_id}: unexpected reference_type")

    if status not in EXPECTED_STATUSES:
        raise AssertionError(f"{example_id}: unexpected resolution_status")

    if source_module not in EXPECTED_SOURCE_MODULES:
        raise AssertionError(f"{example_id}: unexpected source_module")

    if not isinstance(reference["display_label"], str) or not reference["display_label"]:
        raise AssertionError(f"{example_id}: display_label must be a non-empty string")

    validate_reference_id(reference["reference_id"], status, example_id)

    deprecation = reference["deprecation"]
    if not isinstance(deprecation, dict):
        raise AssertionError(f"{example_id}: deprecation must be a mapping")

    if status == "deprecated_reference":
        if deprecation.get("is_deprecated") is not True:
            raise AssertionError(f"{example_id}: deprecated reference must be marked")
        if not deprecation.get("replaced_by"):
            raise AssertionError(f"{example_id}: deprecated reference needs replaced_by")

    manual_review = reference["manual_review"]
    if not isinstance(manual_review, dict):
        raise AssertionError(f"{example_id}: manual_review must be a mapping")

    if status == "ambiguous_manual_review_required":
        if manual_review.get("required") is not True:
            raise AssertionError(f"{example_id}: ambiguous reference needs review")

    if status == "unknown":
        if manual_review.get("required") is not True:
            raise AssertionError(f"{example_id}: unknown reference needs review")


def validate_examples() -> None:
    data = load_yaml(EXAMPLES_PATH)

    if data.get("schema_version") != "library_reference_examples_v0_2":
        raise AssertionError("Unexpected examples schema_version")

    contract = data.get("library_reference_contract")
    if not isinstance(contract, dict):
        raise AssertionError("library_reference_contract must be a mapping")

    if contract.get("schema_version") != "library_reference_v0_2":
        raise AssertionError("Unexpected contract schema_version")

    examples = data.get("examples", [])
    if not isinstance(examples, list) or not examples:
        raise AssertionError("examples must be a non-empty list")

    seen_types: set[str] = set()
    seen_statuses: set[str] = set()

    for example in examples:
        if not isinstance(example, dict):
            raise AssertionError("Each example must be a mapping")

        validate_single_reference(example)

        reference = example["downstream_payload"]["library_reference"]
        seen_types.add(reference["reference_type"])
        seen_statuses.add(reference["resolution_status"])

    missing_types = sorted(EXPECTED_REFERENCE_TYPES - seen_types)
    missing_statuses = sorted(EXPECTED_STATUSES - seen_statuses)

    if missing_types:
        raise AssertionError(f"Missing reference type examples: {missing_types}")

    if missing_statuses:
        raise AssertionError(f"Missing status examples: {missing_statuses}")


def main() -> int:
    require_files()
    validate_schema_file()
    validate_docs()
    validate_examples()

    print("OK: Library reference contract foundation validates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Primary source

**Path:** `scripts/validate_shared_operational_dictionaries.py`
**SHA256:** `b71c23a35896c8c02e25b4e1d8d9bd2d9b392c6eb8d7f6b4a263c0932cf25d40`

```python
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml
from forprint_library.dictionaries.loader import (
    load_all_dictionaries,
    load_shared_dictionary,
)
from forprint_library.dictionaries.models import DICTIONARY_GROUPS
from forprint_library.dictionaries.validation import (
    validate_dictionary_group,
    validate_shared_dictionary,
)
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def read_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML must contain a mapping: {path}")
    return data


def validate_schema_file(path: Path) -> None:
    Draft202012Validator.check_schema(read_yaml(path))


def validate_with_schema(instance_path: Path, schema_path: Path) -> None:
    instance = read_yaml(instance_path)
    schema = read_yaml(schema_path)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(instance)


def check_shared_dictionary() -> None:
    shared_dictionary = load_shared_dictionary()
    validate_shared_dictionary(shared_dictionary)
    validate_with_schema(
        ROOT / "dictionaries" / "shared_operational_dictionary_v0_1.yaml",
        ROOT / "schemas" / "shared_operational_dictionary.schema.yaml",
    )


def check_group_dictionaries() -> None:
    dictionaries = load_all_dictionaries()

    for group_name in DICTIONARY_GROUPS:
        dictionary = dictionaries[group_name]
        validate_dictionary_group(group_name, dictionary)


def check_dictionary_schemas() -> None:
    validate_schema_file(ROOT / "schemas" / "dictionary_entry.schema.yaml")
    validate_schema_file(ROOT / "schemas" / "shared_operational_dictionary.schema.yaml")


def check_required_values() -> None:
    shared_dictionary = load_shared_dictionary()
    groups = shared_dictionary["dictionary_groups"]

    required_values = {
        "source_system": {
            "forprint_operational_registry",
            "calculator_engine",
            "forprint_library",
            "accounting_registry_service",
            "telegram_bot",
            "one_c_bas",
        },
        "entity_type": {
            "order",
            "order_line",
            "client_account",
            "workflow_stage",
            "payment_projection",
            "material_requirement",
        },
        "order_status": {
            "draft",
            "confirmed",
            "completed",
            "cancelled",
            "manual_review_required",
        },
        "payment_status": {
            "unpaid",
            "partially_paid",
            "overdue",
            "paid_reference_confirmed",
        },
        "workflow_stage_status": {
            "waiting_external_contractor",
            "late",
            "manual_review_required",
        },
        "material_requirement_status": {
            "warehouse_reference_pending",
        },
        "alert_severity": {
            "warning",
            "high",
            "critical",
        },
        "unit": {
            "pcs",
            "m2",
            "kg",
            "service",
            "unknown",
        },
    }

    for group_name, expected_ids in required_values.items():
        actual_ids = {entry["id"] for entry in groups[group_name]}
        missing = sorted(expected_ids - actual_ids)
        if missing:
            raise AssertionError(f"Missing values in {group_name}: {missing}")


def check_all() -> None:
    check_shared_dictionary()
    check_group_dictionaries()
    check_dictionary_schemas()
    check_required_values()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        choices=[
            "all",
            "shared",
            "groups",
            "schemas",
            "required-values",
        ],
        default="all",
    )
    args = parser.parse_args()

    checks = {
        "all": check_all,
        "shared": check_shared_dictionary,
        "groups": check_group_dictionaries,
        "schemas": check_dictionary_schemas,
        "required-values": check_required_values,
    }

    try:
        checks[args.check]()
    except Exception as exc:
        print(f"FAILED: shared dictionary check '{args.check}' failed: {exc}")
        return 1

    print(f"OK: shared dictionary check '{args.check}' passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

# Part C — Related tests

No L1 test row declared Block 02 as a secondary relationship.

# Part D — Local L0/L1 and prior-L2 context

## L0 scope/authority

**Path:** `tmp/module_knowledge_analysis/forprint_library/00_preflight/module_scope_and_authority.md`
**SHA256:** `2f50ee3e571d1aa08749bef6ccc96c08b94c902a405209f6d6e44133c62f6233`

```markdown
# ForPrint Library — Module Knowledge Stabilization Pilot
## L0 Preflight: Module Scope and Authority

**Document:** `00_preflight/module_scope_and_authority.md`  
**Pilot:** Stage 2 — Module Knowledge Stabilization & Capability Reconciliation  
**Module:** `forprint_library`  
**Stage:** `L0_PRELIGHT_COMPLETE`  
**Date:** 2026-09-24  
**Mode:** analysis / evidence capture only  
**Mutation authority:** none  
**Implementation authority:** none  
**Roadmap mutation authority:** none  
**Purpose:** establish the trustworthy starting boundary for L1 inventory and functional segmentation.

---

# 1. L0 decision

**L0 result: `READY_FOR_L1_INVENTORY_WITH_FRESHNESS_GAPS_RECORDED`**

The Library repository is suitable for the Stage 2 pilot because:

- the repository state is captured;
- the current Git branch and HEAD are known;
- the Blueprint module policy is available;
- the current module-local coordination/status surfaces are available;
- Stage 1 historical reconciliation evidence is available;
- Library Human Intent evidence is available;
- important freshness conflicts are visible and can be carried forward explicitly rather than silently repaired.

L0 does **not** assert that all module-local status metadata is current.

L0 does **not** authorize implementation, refactoring, cleanup, migration, document rewriting or roadmap mutation.

The next allowed stage is:

`L1 — Inventory and Functional Segmentation`.

---

# 2. Evidence set used

This L0 synthesis uses four captured source files.

## 2.1 Library repository state

Source:

`library_repository_state.txt`

SHA256:

`a20b5f40a2ef92fe288ba4af113b8cdda26d0ae05d3e49653e3d4da741ff6d14`

Contains:

- repository root;
- branch;
- HEAD;
- upstream;
- Git porcelain status at capture time;
- recent commits;
- shallow top-level file inventory;
- coordination file inventory.

## 2.2 Library local authority/status surfaces

Source:

`library_local_authority.txt`

SHA256:

`9d81c595b928a1ab6a86ed2638ae6c00172eb50ceaf784d7a1057ca3e4454aed`

Contains:

- `coordination/status/current_status.yaml`;
- `coordination/status/current_status.md`;
- `coordination/status/next_questions_for_blueprint.md`;
- `coordination/prompts/index.yaml`;
- Makefile operator/governance/prompt/context surfaces.

## 2.3 Library Human Intent references

Source:

`library_human_intent_refs.txt`

SHA256:

`f47b3f2f5b980dd632cb940c8698db62747a8977fc8c3c62c257a628bab36b9a`

Contains selected Human Intent references for Library semantic/catalog/reference responsibilities and cross-module relations.

## 2.4 Blueprint authority and Stage 1/Stage 2 references

Source:

`library_blueprint_authority.txt`

SHA256:

`791b51c3b46483baea2a69875c6dc687b933fe9dfa3ef6ab69a79c07113dbfa2`

Contains:

- Blueprint branch/HEAD/upstream;
- current Library module policy;
- Stage 2 Library pilot plan;
- Stage 1 Library current-state reconciliation references;
- historical-source enrichment references;
- roadmap and portfolio references.

---

# 3. Repository snapshot

## 3.1 Repository

Canonical working repository captured at:

`/srv/software_development/forprint-project/forprint_library`

## 3.2 Git state

Captured branch:

`feature/library-calculator-input-contract-v01`

Captured HEAD:

`bba52bf6001f256a5c13ea7dbe175336b431754c`

Captured upstream:

`bba52bf6001f256a5c13ea7dbe175336b431754c`

Interpretation:

- local HEAD matched upstream at capture time;
- the captured `git status --short` section contained no entries;
- therefore the repository was **clean at L0 capture time**.

This is a point-in-time fact only. L1 must re-check Git state before any generated workspace operation.

## 3.3 Recent implementation lineage visible at HEAD

The five most recent commits at capture were:

1. `bba52bf` — `fix: validate Library completion packet schema`
2. `89c4ec6` — `Record Calculator input completion packet`
3. `d094851` — `Record Library Calculator input contract completion`
4. `0b8cbce` — `Add Library Calculator input contract`
5. `2a55286` — `fix: add Library validation compatibility targets`

L0 interpretation:

The current repository has evidence of a **Library → Calculator input-contract workstream later than the Business Card Skeleton checkpoint**.

L0 does **not** infer the full semantics, completeness or acceptance status of this capability from commit titles alone.

L1/L2 must inspect the implementation, contracts, tests and completion evidence directly.

---

# 4. Authority model for this pilot

For L0/L1 analysis, evidence should be interpreted using the following precedence.

## 4.1 Current Git facts

Strong authority for:

- actual branch;
- actual HEAD;
- tracked implementation;
- tests;
- committed coordination artifacts;
- current file existence.

Git facts do not by themselves define business ownership or architectural authority.

## 4.2 Current Blueprint Module Policy

Current architecture/ownership guidance for `forprint_library`.

The policy states that Library is the canonical semantic, catalog, naming, alias and contract-definition authority for:

- products;
- services;
- materials;
- operations;
- templates;
- shared semantic references;
- shared UI design-system publication / reusable component catalog.

The policy explicitly excludes:

- operational orders;
- client database;
- accounting truth;
- production runtime;
- CRM workflow;
- domain business rules outside Library semantics.

The policy is strategic guidance and does not automatically authorize broad refactors.

## 4.3 Current module-local status/coordination files

Useful current/supporting evidence, but their freshness must be checked against Git and Blueprint.

They must not override newer committed implementation facts or stronger Blueprint policy.

## 4.4 Human Intent

Human Intent preserves accepted/recovered direction and rationale.

It is essential for:

- intended semantic ownership;
- future roadmap relationship;
- dependency meaning;
- cross-module expectations.

Human Intent is not automatic execution authority.

## 4.5 Stage 1 historical evidence

Historical enrichment is provenance and candidate evidence.

It may identify:

- earlier architecture directions;
- candidate functionality;
- possible lineage;
- unresolved reconciliation questions.

It must not override current policy or current repository evidence.

---

# 5. Current Library strategic boundary

The strongest current boundary is:

**Library owns semantic/reference/catalog truth.**

Current Blueprint policy identifies Library as the canonical authority for:

- canonical product/service/material/operation IDs;
- aliases;
- naming rules;
- semantic ambiguity resolution;
- versioned contract definitions and catalog semantics;
- templates and technical/reference definitions;
- shared UI design-system publication and reusable UI component catalog;
- reusable semantic/capability discoverability.

The current policy does **not** assign Library ownership of:

- orders;
- customers;
- payments/accounting;
- warehouse stock truth;
- production execution/runtime;
- CRM workflows;
- Calculator pricing/calculation logic;
- other domain business rules outside Library semantics.

This boundary is consistent with the module-local status statement that Library owns canonical catalog semantics, stable IDs, aliases and contract definitions while not owning clients, orders, payments, warehouse stock truth, production runtime, 1C synchronization, CRM workflow, Telegram runtime or Calculator logic.

---

# 6. Human Intent synthesis for L0

The captured Human Intent references expand the Library target boundary beyond the oldest local status files.

Important directions include:

## 6.1 Stable canonical semantics

Library owns stable canonical IDs and versioned schemas for:

- products;
- materials;
- services;
- operations.

## 6.2 External catalog provenance

External catalog ingestion should preserve provenance such as:

- source/provider;
- fetched time;
- external key;
- content/hash identity;
- raw snapshot references.

This is a future/roadmap direction unless L1 finds current implementation.

## 6.3 Calibration/reference profiles

Library is intended to own canonical calibration/reference profiles used by Operations Assistant for physical measurements.

L1 must determine whether this exists, is planned only, or belongs to a future slice.

## 6.4 Library → Calculator contract

The intended Library → Calculator reference input is:

- deterministic;
- typed;
- versioned;
- read-only.

Pricing formulas remain owned by Calculator.

This intent is especially relevant because the current Git HEAD contains recent Calculator input-contract commits.

## 6.5 SOP / instruction / media knowledge

Library is intended to hold reusable SOP/instruction/media knowledge used for contextual guidance.

Execution truth remains with operational owners.

## 6.6 Shared UI design system

Human Intent and current Blueprint policy assign Library a publication/semantic role for:

- UI tokens;
- themes;
- reusable components;
- component catalog;
- version/adoption metadata.

Consumer modules should adopt these surfaces rather than maintain competing semantic definitions.

## 6.7 Canonical aliases and naming profiles

Library owns:

- aliases;
- common misspellings;
- short production tokens;
- naming profiles;
- profile-specific semantic defaults.

Calculator should consume these definitions rather than maintain a private vocabulary.

## 6.8 Context-dependent token semantics

The same token can mean different things across equipment or production profiles.

Therefore semantic resolution should be structured and profile/capability-aware rather than implemented as a global flat alias table.

## 6.9 Inter-module semantic contract changes

Semantic changes that affect inter-module payloads should flow through a versioned contract/adoption lifecycle.

L1/L2 must reconcile this direction with the current Contract Registry architecture and current Library implementation.

## 6.10 Shared discovery indexes

Shared indexes should allow modules to discover reusable semantic and technical primitives before creating competing implementations.

This direction directly supports Stage 2 Module Knowledge Stabilization.

## 6.11 Semantic registry direction

Recovered 2026-09 Human Intents describe Library as the shared semantic and contract-reference authority and introduce a semantic-registry direction:

- stable semantic IDs;
- maturity/version evolution;
- prioritized registration for public/cross-module/high-criticality semantics;
- batched unresolved registration/enrichment proposals.

These are roadmap/intention signals until current implementation evidence is found.

## 6.12 Historical/reference asset semantics

Historical/reference asset indexing should use stable asset/revision semantics with provenance.

Library may own canonical reference-media semantics, while order/customer/production truth remains with domain owners.

---

# 7. Stage 1 evidence carried into Stage 2

Stage 1 closed the Library historical front with:

`CURRENT_LIBRARY_HISTORICAL_CANDIDATES_CONFIRMED`

The historical enrichment explicitly records that:

- the current Library canonical boundary is stronger than early broad ownership proposals;
- broad "Library owns everything" interpretations are superseded;
- historical admin-surface ideas remain reconciliation candidates;
- historical Contract Registry lineage requires reconciliation with the current Contract Registry architecture;
- no new Library implementation task was created merely from the historical front;
- Library remains owner of semantic/reference/catalog truth.

Four historical candidate families are explicitly visible in the captured Blueprint references:

1. Library governance/standardization candidate;
2. Calculator input-contract lineage candidate;
3. Library admin/publication-surface candidate;
4. Contract Registry/sync-manager lineage candidate.

These are **candidate evidence**, not implementation authority.

---

# 8. L0 detected freshness and authority gaps

These are not failures of the pilot. They are exactly the type of knowledge inconsistency Stage 2 is intended to expose.

## GAP-LIB-L0-001 — branch metadata stale

Actual Git branch:

`feature/library-calculator-input-contract-v01`

Module-local `current_status.yaml` contains:

`branch: main`

Classification:

`CURRENT_SUPPORTING_STALE`

Action:

Do not repair in L0.

L1 should record the stale field in document/status authority analysis.

## GAP-LIB-L0-002 — last commit metadata stale

Actual Git HEAD:

`bba52bf6001f256a5c13ea7dbe175336b431754c`

Module-local status contains an older `last_commit` value.

Classification:

`CURRENT_SUPPORTING_STALE`

## GAP-LIB-L0-003 — current phase/status lags implementation lineage

Module-local status still presents:

`business_card_skeleton_v0_1`

as the current phase and asks for Blueprint review of that checkpoint.

But current Git history shows later Calculator input-contract work and completion-packet commits.

Classification:

`CONFLICT_REQUIRES_RECONCILIATION`

Important:

L0 does **not** infer whether the Calculator input contract is accepted, active, complete or only recorded.

L1/L2 must inspect current contract files, tests, completion report and Blueprint acceptance evidence.

## GAP-LIB-L0-004 — priority mismatch

Module-local status reports:

`priority: p0`

Current Blueprint Module Policy reports:

`p1`

Classification:

`CURRENT_BLUEPRINT_POLICY_WINS_FOR_STRATEGIC_GUIDANCE`

No status file is rewritten in L0.

## GAP-LIB-L0-005 — local prompt index appears obsolete/incomplete

`coordination/prompts/index.yaml` reports an empty `items` list and an old update date, while the repository contains active prompt files and Makefile logic that resolves current Blueprint outgoing Prompt Queue sources.

Classification:

`LEGACY_OR_TRANSITIONAL_COORDINATION_SURFACE_CANDIDATE`

L1 must determine:

- whether this local index is intentionally legacy;
- whether it should still be maintained;
- whether active prompt files are current, historical or transitional;
- which prompt intake mechanism is authoritative now.

Do not "fix" the index during discovery.

## GAP-LIB-L0-006 — local status mixes multiple eras/checkpoints

The current status file contains accumulated states for:

- catalog seed;
- shared operational dictionary;
- semantic reference readiness;
- reference contract foundation;
- coordination alignment;
- reference consumption pilot;
- Business Card Skeleton.

This is useful historical/current supporting evidence but is not yet a clean current-state projection.

Classification:

`CURRENT_SUPPORTING_WITH_HISTORICAL_ACCUMULATION`

Stage 2 should eventually distinguish current capability truth from checkpoint history.

---

# 9. Known implementation surfaces visible before L1

The shallow repository inventory already proves the presence of major surface families.

## 9.1 Catalog data

Visible:

- `catalog/product_families.yaml`
- `catalog/materials.yaml`
- `catalog/operations.yaml`
- `catalog/print_modes.yaml`
- `catalog/finishing_options.yaml`

## 9.2 Shared dictionaries

Visible dictionaries include operational/reference/status semantics such as:

- units;
- order statuses;
- production statuses;
- payment statuses;
- workflow statuses;
- reference-resolution statuses;
- source-system semantics;
- entity types;
- alert and notification semantics.

L1 must classify whether each dictionary is:

- canonical Library-owned semantic truth;
- projection/shared contract;
- historical/legacy;
- misplaced domain semantics;
- still current.

Presence alone does not prove correct ownership.

## 9.3 Schemas

Visible schema surfaces include:

- product family;
- material;
- operation;
- print mode;
- finishing option;
- dictionary entry;
- configurable product;
- shared operational dictionary;
- catalog seed.

## 9.4 Export / validation / preview tooling

Visible scripts include:

- catalog schema export;
- component catalog export;
- dictionary policy export;
- shared dictionary coordination export;
- semantic/reference validation;
- shared dictionary validation;
- Library check runner;
- Blueprint instruction checking/sync.

## 9.5 Coordination surfaces

Visible:

- Blueprint source pointer;
- Blueprint awareness ledger;
- prompt active/index surfaces;
- completion packets;
- completion reports;
- reports index;
- current status;
- next questions;
- standards snapshot.

This makes Library a good pilot because implementation, coordination and governance evidence are all present but not yet normalized into one knowledge model.

---

# 10. L0 document-authority provisional classification

This is provisional only. Final authority classification belongs to L4.

| Surface | L0 provisional role | Notes |
|---|---|---|
| Current Git tree | `CURRENT_IMPLEMENTATION_EVIDENCE` | strongest source for what exists |
| Blueprint `module_policy.md` | `CURRENT_AUTHORITY` | architecture/ownership guidance |
| Stage 2 Library pilot plan | `CURRENT_AUTHORITY` for pilot method | governs L0–L9 procedure |
| `current_status.yaml` | `CURRENT_SUPPORTING_STALE` | contains useful facts plus stale metadata |
| `current_status.md` | `CURRENT_SUPPORTING_STALE` | Business Card centered, behind HEAD |
| `next_questions_for_blueprint.md` | `CURRENT_SUPPORTING_STALE` | no longer sufficient to describe latest Git lineage |
| local `coordination/prompts/index.yaml` | `UNKNOWN/LEGACY_CANDIDATE` | empty despite later prompt workflow |
| active prompt files | `REQUIRES_L1/L4_CLASSIFICATION` | existence does not prove current authority |
| completion reports | `EVIDENCE` | inspect individually in L1/L2 |
| Stage 1 historical enrichment | `HISTORICAL_PROVENANCE` | candidate/lineage evidence |
| Human Intent | `GOVERNED_INTENT_EVIDENCE` | not execution authority |
| roadmap/portfolio references | `PLANNING_EVIDENCE` | maturity must be assessed per capability |

---

# 11. L1 allowed actions

L1 may:

- re-check branch/HEAD/upstream/status;
- enumerate the full repository;
- classify every file into one primary functional block and optional secondary relationships;
- create analysis-only directories under:
  `tmp/module_knowledge_analysis/forprint_library/`;
- create `manifest.yaml` files for analysis blocks;
- record hashes/sizes/types/paths;
- record inferred capability associations with confidence;
- identify documents/tests/entrypoints without changing them;
- identify likely duplicates, legacy surfaces and cross-module ownership questions as candidates;
- record unknowns explicitly;
- use Blueprint/Human Intent/roadmap evidence for classification context.

L1 should prefer semantic capability grouping over raw directory grouping.

---

# 12. L1 prohibited actions

L1 must **not**:

- edit Library source;
- edit schemas/catalog/dictionaries;
- rewrite documentation;
- update current status files;
- repair prompt indexes;
- archive old prompts;
- delete duplicates;
- move files;
- rename IDs;
- refactor code;
- implement missing roadmap items;
- create production API/database/runtime behavior;
- mutate Blueprint;
- change roadmap maturity;
- declare historical candidates implemented without evidence;
- resolve ownership conflicts by assumption;
- commit/push analysis outputs unless a later explicit publication step authorizes it.

Discovery precedes reconciliation.

Reconciliation precedes implementation.

---

# 13. L1 provisional segmentation hypothesis

L1 must verify this against the full repository before finalizing manifests.

Directory names below describe **analysis blocks**, not source ownership or required repository structure.

## `01_domain_semantics_catalog`

Candidate scope:

- products;
- services if present;
- materials;
- operations;
- print modes;
- finishing options;
- configurable product semantics;
- canonical IDs and aliases.

## `02_dictionaries_resolution_profiles`

Candidate scope:

- shared operational dictionaries;
- reference resolution;
- units;
- aliases/tokens;
- status/type dictionaries;
- profile/capability-aware naming semantics.

Special attention:

Some dictionaries may represent domain semantics owned elsewhere. L1 should flag, not fix.

## `03_contracts_cross_module_consumption`

Candidate scope:

- reference contracts;
- Library → Calculator input contract;
- consumption contracts;
- version/adoption metadata;
- Contract Registry relationship;
- downstream handoff semantics.

## `04_exports_previews_examples`

Candidate scope:

- exporters;
- previews;
- examples;
- generated semantic/reference artifacts;
- human-readable projections.

## `05_validation_tests_quality`

Candidate scope:

- validators;
- pytest suites;
- architecture/boundary tests;
- check runner/reporting;
- conformance/compatibility targets.

## `06_coordination_governance_intake`

Candidate scope:

- Blueprint sync;
- prompt intake;
- awareness ledger;
- status;
- completion reports/packets;
- standards snapshot;
- Makefile coordination/operator surfaces.

## `07_documentation_architecture`

Candidate scope:

- README;
- docs;
- architecture descriptions;
- policy notes;
- integration guidance;
- historical instruction surfaces.

The block should not pre-classify documents as current; that comes later.

## `08_ui_design_system_reference`

Create only if the repository actually contains meaningful current design-system/component-catalog implementation.

Human Intent and Blueprint policy alone are not enough.

If absent, record `roadmap/intended, implementation not found`.

## `09_sop_media_reference_knowledge`

Create only if current implementation exists.

Otherwise keep as roadmap/Human Intent evidence.

## `10_legacy_unknown_unclassified`

Temporary holding block for:

- unclear files;
- duplicated generations;
- stale generated outputs;
- old coordination artifacts;
- files that cross several capability areas;
- items requiring later owner decision.

## `synthesis`

Reserved for L3+.

Do not synthesize capability truth before selected L2 block analyses are complete.

---

# 14. L1 manifest minimum fields

Each analysis block should have a `manifest.yaml` containing at least:

- `schema_version`
- `module_id`
- `block_id`
- `title`
- `purpose`
- `source_paths`
- `file_count`
- `selection_method`
- `primary_capability_hypotheses`
- `cross_block_dependencies`
- `documents_present`
- `tests_present`
- `generated_outputs_present`
- `legacy_candidates_present`
- `unknowns`
- `confidence`
- `mutation_performed: false`

L1 should additionally create a module-wide inventory mapping every selected file to:

- primary block;
- optional secondary block(s);
- file kind;
- current/historical/unknown preliminary lifecycle;
- evidence reason.

No source file should disappear merely because it does not fit the first segmentation model.

---

# 15. Questions L1 must answer

1. What is the complete file population of the Library repository excluding Git/venv/cache/temp noise?
2. Which implementation capabilities are actually present at current HEAD?
3. What exactly was added by the recent Calculator input-contract commits?
4. Which tests prove that contract?
5. Which completion report/packet corresponds to it?
6. Is it accepted by Blueprint or only completed module-side?
7. Which Business Card implementation surfaces still exist and what is their lifecycle?
8. Which status files are projections vs historical accumulators?
9. Which prompt-intake surfaces are current vs legacy?
10. Which dictionaries are truly Library-owned semantic definitions and which may represent foreign domain truth?
11. Are there duplicate schema/contract generations?
12. Is there actual current UI Design System implementation or only roadmap/intent?
13. Is there current SOP/media knowledge implementation or only roadmap/intent?
14. Are there admin/publication surfaces corresponding to the historical candidate?
15. Is there current Contract Registry integration or only lineage/candidate evidence?
16. What are the stable public entrypoints for downstream consumers?
17. Which Makefile targets are supported operator workflows for each capability?
18. Which generated reports/artifacts are authoritative, supporting or disposable?
19. Which capabilities are implemented but absent from current roadmap visibility?
20. Which roadmap directions have no implementation yet?

---

# 16. L1 entry criteria

Before L1 inventory starts, re-check:

- Library repo exists;
- branch is known;
- HEAD/upstream relationship;
- worktree status;
- Blueprint policy readable;
- analysis root writable under `tmp/`;
- no source mutation required.

If the worktree has unrelated concurrent dirty changes, inventory may continue read-only, but hashes and snapshot metadata must record that state.

---

# 17. L1 exit criteria

L1 is complete only when:

- the full repository inventory is captured;
- exclusions are explicit;
- every selected file is assigned to a primary analysis block;
- each block has `manifest.yaml`;
- cross-block relationships are recorded;
- unknown/unclassified files are not silently discarded;
- no source mutation occurred;
- the segmentation is suitable for one-block-at-a-time L2 analysis;
- no capability truth has been prematurely synthesized.

Expected next stage:

`L2 — Sequential Block Analysis`.

---

# 18. L0 unresolved items

The following are intentionally deferred:

- exact acceptance state of the Calculator input contract;
- exact freshness correction required for `current_status.*`;
- local prompt index lifecycle;
- authority status of active local prompt files;
- Contract Registry boundary details;
- admin/publication surface candidate;
- actual UI Design System implementation state;
- SOP/media knowledge implementation state;
- semantic registry implementation state;
- historical asset index implementation state;
- cleanup/migration requirements.

These are evidence questions, not reasons to block L1.

---

# 19. L0 final boundary statement

ForPrint Library should enter Stage 2 analysis under the following working definition:

> Library is the canonical semantic/reference/catalog layer for long-lived shared product, service, material, operation, naming, alias, template and selected shared design/reference definitions. It must remain distinct from operational order truth, client/accounting truth, warehouse stock truth, production execution, CRM workflow and Calculator pricing logic.

The current repository contains more implementation history than the local rolling status files accurately expose.

Therefore Stage 2 must reconstruct capability truth from:

`current Git implementation + tests + contracts + Blueprint policy + Human Intent + roadmap/provenance`

rather than treating any single status document as complete.

**L0 status: PASS WITH RECORDED FRESHNESS GAPS.**

**Next allowed stage: L1 — Inventory and Functional Segmentation.**
```

## L1 closeout

**Path:** `tmp/module_knowledge_analysis/forprint_library/l1_inventory/l1_closeout.md`
**SHA256:** `e52e7ca3e2eaf27e7447d43b70bcd7582d7d896fd593a3f7cb278a8b82ec8971`

```markdown
# ForPrint Library — Module Knowledge Stabilization Pilot
## L1 Closeout — Inventory & Functional Segmentation

**Module:** `forprint_library`  
**Stage:** `L1 — Inventory and Functional Segmentation`  
**Status:** `PASS_CORRECTED_AFTER_HUMAN_REVIEW`  
**Date:** 2026-09-24  
**Mutation authority:** none  
**Source mutation performed:** false  
**Next stage:** `L2 — Sequential Block Analysis`

---

# 1. Closeout decision

**L1 result: PASS**

The Library repository inventory and first-pass functional segmentation are complete and suitable for sequential L2 analysis.

L1 established a complete bounded analysis population while preserving the source repository unchanged.

Final verified snapshot:

- branch: `feature/library-calculator-input-contract-v01`
- HEAD: `bba52bf6001f256a5c13ea7dbe175336b431754c`
- selected files: `178`
- analysis blocks: `8`
- low-confidence classifications: `0`
- selected untracked files: `0`
- non-`tmp/` Git status count after correction: `0`
- mutation outside `tmp/`: `false`

---

# 2. Final functional segmentation

| Block | File count | L1 role |
|---|---:|---|
| `01_domain_semantics_catalog` | 20 | catalog/domain semantic implementation |
| `02_dictionaries_resolution_profiles` | 36 | dictionaries, resolution, aliases/tokens/profile semantics |
| `03_contracts_cross_module_consumption` | 16 | contracts and downstream/module consumption |
| `04_exports_previews_examples` | 15 | exports, previews, examples and projections |
| `05_validation_tests_quality` | 32 | validators, tests, quality gates and reporting |
| `06_coordination_governance_intake` | 30 | Blueprint intake, governance, status and completion evidence |
| `07_documentation_architecture` | 28 | documentation and architecture/instruction surfaces |
| `10_legacy_unknown_unclassified` | 1 | technical/scaffolding holding area |

Total: `178` files.

---

# 3. Human-review corrections applied

The initial automated segmentation was intentionally reviewed before L1 closeout.

The review identified false positives and corrected them without changing source files.

## 3.1 Removed non-capability noise

Excluded from the capability inventory:

- root `tmp.py` — confirmed exact untracked copy of the L1 audit script;
- `.gitignore` — repository housekeeping metadata;
- `contracts/placeholders/.gitkeep` — empty directory placeholder.

These exclusions do not remove implementation evidence.

## 3.2 Corrected catalog implementation classification

The following files were reclassified from the false-positive UI Design System block to their actual catalog/validation/export roles:

- `app/forprint_library/catalog/__init__.py`
- `app/forprint_library/catalog/loader.py`
- `app/forprint_library/catalog/models.py`
- `app/forprint_library/catalog/validation.py`
- `scripts/export_catalog_schema_artifacts.py`
- `scripts/export_component_catalogs.py`
- `scripts/run_library_checks.py`
- `scripts/validate_catalog_seed.py`

## 3.3 Corrected reference-contract classification

The following files were moved from unknown/unclassified to the cross-module contracts block:

- `app/forprint_library/contracts/models.py`
- `schemas/reference_contract/library_reference.schema.yaml`

## 3.4 Technical scaffolding retained

`app/forprint_library/__init__.py` remains in the holding block as technical scaffolding rather than as a legacy capability.

---

# 4. Important negative findings

Negative findings are first-class evidence.

## 4.1 UI Design System implementation not proven

L1 found no current repository implementation sufficient to establish:

`UI_DESIGN_SYSTEM_IMPLEMENTATION_PROVEN=true`

Therefore:

`UI_DESIGN_SYSTEM_IMPLEMENTATION_PROVEN=false`

The Library UI Design System remains, at this stage:

- current Blueprint policy direction;
- Human Intent;
- roadmap/portfolio target;
- not current implementation truth proven by L1.

The former `08_ui_design_system_reference` block was removed after review because it contained only misclassified catalog/validation/export files.

## 4.2 SOP/media implementation not proven

No current implementation block was created for:

`09_sop_media_reference_knowledge`

Therefore:

`SOP_MEDIA_IMPLEMENTATION_PROVEN=false`

SOP/instruction/media knowledge remains a roadmap/Human Intent direction until later evidence proves implementation.

---

# 5. L1 evidence products

The canonical analysis outputs for this pilot stage are under:

`tmp/module_knowledge_analysis/forprint_library/`

L1 inventory surfaces:

- `l1_inventory/module_inventory.yaml`
- `l1_inventory/module_inventory.tsv`
- `l1_inventory/run_report.yaml`
- `l1_inventory/segmentation_summary.md`

Per-block analysis manifests:

- `01_domain_semantics_catalog/manifest.yaml`
- `02_dictionaries_resolution_profiles/manifest.yaml`
- `03_contracts_cross_module_consumption/manifest.yaml`
- `04_exports_previews_examples/manifest.yaml`
- `05_validation_tests_quality/manifest.yaml`
- `06_coordination_governance_intake/manifest.yaml`
- `07_documentation_architecture/manifest.yaml`
- `10_legacy_unknown_unclassified/manifest.yaml`

L0 evidence remains under:

- `00_preflight/library_repository_state.txt`
- `00_preflight/library_local_authority.txt`
- `00_preflight/module_scope_and_authority.md`

---

# 6. What L1 does and does not prove

L1 proves:

- the bounded repository analysis population;
- deterministic file inventory;
- a usable first-pass functional segmentation;
- zero source mutation during the inventory/correction process;
- the absence of current L1 evidence for UI Design System implementation;
- the absence of current L1 evidence for SOP/media implementation.

L1 does **not** yet prove:

- final capability identities;
- capability maturity;
- document authority;
- duplicate relationships;
- roadmap maturity;
- implementation completeness;
- correct domain ownership for every dictionary;
- acceptance state of the Library → Calculator contract;
- cleanup or migration requirements.

Those questions belong to L2–L8.

---

# 7. L2 analysis order

Recommended sequential analysis order:

1. `01_domain_semantics_catalog`
2. `02_dictionaries_resolution_profiles`
3. `03_contracts_cross_module_consumption`
4. `04_exports_previews_examples`
5. `05_validation_tests_quality`
6. `06_coordination_governance_intake`
7. `07_documentation_architecture`
8. `10_legacy_unknown_unclassified`

This order starts with the module's core semantic truth before interpreting contracts, validation, governance and documentation around it.

L2 should analyze one block at a time and write one:

`analysis_report.md`

per block.

Do not synthesize the final Module Knowledge Base until all selected L2 block reports exist.

---

# 8. Required L2 report dimensions

Each L2 block analysis should capture:

- capabilities;
- stable capability candidates;
- implementation paths;
- public/internal entrypoints;
- schemas/data/state;
- dependencies;
- downstream consumers;
- validators/tests proving behavior;
- generated/supporting artifacts;
- relevant documentation;
- Blueprint policy/Human Intent/roadmap evidence;
- duplicate candidates;
- legacy candidates;
- reuse candidates;
- migration candidates;
- wrong-owner candidates;
- roadmap relation;
- implementation relation;
- uncertainty/confidence.

The report must distinguish observed facts from interpretation.

---

# 9. Closeout boundary

No L1 result authorizes:

- source edits;
- refactors;
- deletions;
- document rewrites;
- prompt-index repairs;
- status corrections;
- capability migration;
- roadmap mutation;
- implementation of missing roadmap features.

Discovery precedes reconciliation.

Reconciliation precedes implementation.

---

# 10. Final status

`LIBRARY_PILOT_L1=PASS_CORRECTED_AFTER_HUMAN_REVIEW`

`SELECTED_FILE_COUNT=178`

`ANALYSIS_BLOCK_COUNT=8`

`LOW_CONFIDENCE_COUNT=0`

`UNTRACKED_SELECTED_COUNT=0`

`NON_TMP_STATUS_COUNT=0`

`UI_DESIGN_SYSTEM_IMPLEMENTATION_PROVEN=false`

`SOP_MEDIA_IMPLEMENTATION_PROVEN=false`

`NEXT_STAGE=L2_SEQUENTIAL_BLOCK_ANALYSIS`

`NEXT_BLOCK=01_domain_semantics_catalog`
```

## L1 run report

**Path:** `tmp/module_knowledge_analysis/forprint_library/l1_inventory/run_report.yaml`
**SHA256:** `dedb10a29bcc008ecb7f89c20faeb34bf3a2b88429477fd38164c3b3dcdcdaee`

```yaml
result: PASS_CORRECTED_AFTER_HUMAN_REVIEW
module_id: forprint_library
branch: feature/library-calculator-input-contract-v01
head: bba52bf6001f256a5c13ea7dbe175336b431754c
upstream: bba52bf6001f256a5c13ea7dbe175336b431754c
selected_file_count: 178
created_blocks:
- 01_domain_semantics_catalog
- 02_dictionaries_resolution_profiles
- 03_contracts_cross_module_consumption
- 04_exports_previews_examples
- 05_validation_tests_quality
- 06_coordination_governance_intake
- 07_documentation_architecture
- 10_legacy_unknown_unclassified
block_counts:
  01_domain_semantics_catalog: 20
  02_dictionaries_resolution_profiles: 36
  03_contracts_cross_module_consumption: 16
  04_exports_previews_examples: 15
  05_validation_tests_quality: 32
  06_coordination_governance_intake: 30
  07_documentation_architecture: 28
  10_legacy_unknown_unclassified: 1
low_confidence_count: 0
untracked_selected_count: 0
source_non_tmp_git_status_unchanged: true
mutation_performed_outside_tmp: false
manual_review_correction:
  version: v0_1
  excluded_paths:
    tmp.py: local L1 audit-script copy; not module capability evidence
    .gitignore: Git housekeeping metadata; excluded from capability inventory
    contracts/placeholders/.gitkeep: empty directory placeholder; excluded from capability inventory
  reassigned_path_count: 11
  ui_design_system_current_implementation_proven: false
  sop_media_current_implementation_proven: false
outputs:
  inventory_yaml: tmp/module_knowledge_analysis/forprint_library/l1_inventory/module_inventory.yaml
  inventory_tsv: tmp/module_knowledge_analysis/forprint_library/l1_inventory/module_inventory.tsv
  summary: tmp/module_knowledge_analysis/forprint_library/l1_inventory/segmentation_summary.md
```

## L1 segmentation summary

**Path:** `tmp/module_knowledge_analysis/forprint_library/l1_inventory/segmentation_summary.md`
**SHA256:** `e5fc302c3578cb0a3f0dff2d797e38afcb0c1664f43f769bd54f4e372a90d34d`

```markdown
# ForPrint Library — L1 Inventory & Functional Segmentation

- Module: `forprint_library`
- Branch: `feature/library-calculator-input-contract-v01`
- HEAD: `bba52bf6001f256a5c13ea7dbe175336b431754c`
- Upstream: `bba52bf6001f256a5c13ea7dbe175336b431754c`
- Selected files after human review: **178**
- Created analysis blocks: **8**
- Low-confidence classifications: **0**
- Selected untracked files: **0**
- Source/non-`tmp/` Git status mutation by correction: **false**

## Human-review corrections

- Removed root `tmp.py` from module inventory: exact untracked L1 audit-script artifact.
- Excluded `.gitignore` and `contracts/placeholders/.gitkeep` as non-capability housekeeping/placeholder files.
- Reassigned `app/forprint_library/catalog/*` to domain semantics/catalog.
- Reassigned catalog exporters to exports/previews/examples.
- Reassigned check/validation scripts to validation/tests/quality.
- Reassigned `app/forprint_library/contracts/models.py` and `schemas/reference_contract/library_reference.schema.yaml` to cross-module contracts.
- No current implementation evidence remains in `08_ui_design_system_reference`; the empty analysis block was removed.
- No current implementation evidence exists for `09_sop_media_reference_knowledge` in this L1 segmentation.

## Block counts

| Block | Files |
|---|---:|
| `01_domain_semantics_catalog` | 20 |
| `02_dictionaries_resolution_profiles` | 36 |
| `03_contracts_cross_module_consumption` | 16 |
| `04_exports_previews_examples` | 15 |
| `05_validation_tests_quality` | 32 |
| `06_coordination_governance_intake` | 30 |
| `07_documentation_architecture` | 28 |
| `10_legacy_unknown_unclassified` | 1 |

## Interpretation

- UI Design System remains a Blueprint policy/Human Intent/roadmap direction unless later evidence is found; L1 did not prove current implementation.
- SOP/media knowledge likewise remains intent/roadmap evidence; L1 did not prove current implementation.
- The remaining `10_legacy_unknown_unclassified` block is not a deletion list.
- No document authority, roadmap maturity or implementation status is finalized by L1.

## Next stage

L1 is ready for closeout review. After closeout, begin **L2 sequential block analysis** one functional block at a time.
```

## Prior L2 Block 01 supporting analysis

**Path:** `tmp/module_knowledge_analysis/forprint_library/01_domain_semantics_catalog/analysis_report.md`
**SHA256:** `7124be275bed431331d250599bd11ac7ea8b7d40c3f5e8593072ec1f88dc3b67`

```markdown
# ForPrint Library — Module Knowledge Stabilization Pilot
## L2 Block Analysis Report — `01_domain_semantics_catalog`

**Module:** `forprint_library`  
**Stage:** `L2 — Sequential Block Analysis`  
**Block:** `01_domain_semantics_catalog`  
**Analysis status:** `ANALYZED_WITH_RECONCILIATION_CANDIDATES`  
**Block closeout recommendation:** `PASS_FOR_L2_WITH_CARRIED_UNCERTAINTY`  
**Date:** 2026-09-24  
**Mutation performed:** false  
**Implementation authority:** none  
**Roadmap mutation authority:** none  
**Primary evidence packet:** `l2_block_01_analysis_packet.md`  
**Primary source population:** 20 files  
**Related test population:** 17 files  
**Blueprint/context evidence:** 8 files + 2 bounded roadmap subsets

---

# 1. Executive conclusion

Block `01_domain_semantics_catalog` contains a real, current, file-backed Library semantic/catalog implementation.

The strongest current implementation facts are:

1. A draft canonical catalog seed exists for:
   - materials;
   - product families;
   - operations;
   - print modes;
   - finishing options.

2. The seed contains **28 current draft catalog entries**:
   - 6 materials;
   - 6 product families;
   - 7 operations;
   - 4 print modes;
   - 5 finishing options.

3. Every current seed entry is still `draft`.

4. The catalog maturity is explicitly bounded as:
   - `catalog_status: draft_canonical_seed`
   - `schema_status: unstable_v0_1`
   - `usage: allowed_for_projection_use`
   - `contract_status: not_final_contract`
   - `owner_module: forprint_library`

5. Component catalog YAML files are current parallel representations of the seed sections. In the captured packet, their item lists are content-equivalent to the corresponding seed sections.

6. A Python loader/validation layer exists for the catalog.

7. A configurable product reference exists for:
   - `product.business_card`
   - schema `configurable_product_card_v0_1`
   - status `draft_reference`.

8. The Business Card card clearly separates:
   - Library-owned parameter definitions/reference semantics;
   - consumer-owned selected values/context;
   - non-goals such as pricing, stock truth, order creation, runtime integration and production writes.

9. Current tests provide strong proof for:
   - seed/schema validity;
   - ID uniqueness;
   - alias-list validity;
   - no current duplicate aliases across the combined seed;
   - component-catalog validation;
   - projection-readiness;
   - stable known IDs;
   - Business Card reference structure;
   - cross-module boundaries.

10. The block is **not** a final production catalog, production database, live API, pricing engine, inventory truth or operational state owner.

Two important L2 reconciliation findings were discovered:

- two `scripts/coordination/*` files are incorrectly present in the Block 01 primary population and are stronger candidates for Block 06;
- the public catalog API imports and tests use `CatalogRegistry`, but the implementation source for `app/forprint_library/catalog/registry.py` is not present in this Block 01 packet.

These findings do not invalidate the block. They are carried forward as reconciliation candidates.

---

# 2. Evidence boundary

This report deliberately separates five evidence classes.

## 2.1 Current implementation evidence

Primary source population from the human-reviewed L1 manifest.

Used to determine:

- what data exists;
- what schemas exist;
- what loading/validation implementation exists;
- what configurable-product reference exists;
- what implementation boundaries are encoded.

## 2.2 Test evidence

The packet contains 17 related test files.

Tests are used as behavioral proof where they exercise current implementation.

They are not treated as implementation source.

## 2.3 Blueprint current authority/planning evidence

Used for:

- module ownership;
- strategic role;
- roadmap relation;
- intended future direction.

It is not treated as proof that a planned capability is already implemented.

## 2.4 Human Intent evidence

Used for intended semantic direction and rationale.

Human Intent is planning context, not release/execution authority.

## 2.5 Stage 1 historical/reconciliation evidence

Used as provenance and prior reconciliation.

Historical material does not override current Git implementation or current Blueprint module policy.

---

# 3. Block population review

The L1 manifest assigned 20 primary source files to this block.

## 3.1 Strongly in-scope primary files

### Python catalog layer

- `app/forprint_library/catalog/__init__.py`
- `app/forprint_library/catalog/loader.py`
- `app/forprint_library/catalog/models.py`
- `app/forprint_library/catalog/validation.py`

### Configurable product

- `catalog/configurable_products/business_card.yaml`

### Component catalog data

- `catalog/finishing_options.yaml`
- `catalog/materials.yaml`
- `catalog/operations.yaml`
- `catalog/print_modes.yaml`
- `catalog/product_families.yaml`

### Canonical seed

- `catalog/seeds/catalog_seed_v0_1.yaml`

### Catalog/product schemas

- `schemas/catalog_seed.schema.yaml`
- `schemas/configurable_product.schema.yaml`
- `schemas/finishing_option.schema.yaml`
- `schemas/material.schema.yaml`
- `schemas/operation.schema.yaml`
- `schemas/print_mode.schema.yaml`
- `schemas/product_family.schema.yaml`

## 3.2 Block-boundary reclassification candidates

The following files are current files but do not primarily implement domain semantics/catalog behavior:

- `scripts/coordination/export_coordination_foundation_alignment_closure.py`
- `scripts/coordination/validate_coordination_foundation_alignment.py`

Their actual responsibility is coordination/governance/status/report completion.

**Candidate disposition:**

`RECLASSIFY_PRIMARY_TO_06_COORDINATION_GOVERNANCE_INTAKE`

Do not move or edit these files during L2.

The finding should be carried to L3/L5 reconciliation and included explicitly when Block 06 is analyzed.

---

# 4. Provisional capability map

Capability IDs below are **L2 candidate IDs only**.

They are not final stable Module Knowledge Base IDs until L3 synthesis.

---

## CAP-CAND-LIB-01 — Draft canonical catalog seed

**Implementation state:** `VERIFIED_CURRENT_DRAFT_PROJECTION`

**Confidence:** HIGH

### Purpose

Provide one Library-owned draft canonical semantic population covering common ForPrint reference concepts.

### Implementation paths

- `catalog/seeds/catalog_seed_v0_1.yaml`
- `schemas/catalog_seed.schema.yaml`
- `app/forprint_library/catalog/models.py`
- `app/forprint_library/catalog/loader.py`
- `app/forprint_library/catalog/validation.py`

### Sections

- `materials`
- `product_families`
- `operations`
- `print_modes`
- `finishing_options`

### Current population

| Section | Entries |
|---|---:|
| materials | 6 |
| product_families | 6 |
| operations | 7 |
| print_modes | 4 |
| finishing_options | 5 |
| **Total** | **28** |

### Maturity

All 28 entries are currently `draft`.

Seed metadata explicitly states:

- `draft_canonical_seed`
- `unstable_v0_1`
- `allowed_for_projection_use`
- `not_final_contract`
- `forprint_library`

### Current interpretation

This is current semantic/reference implementation.

It is **not** a final production catalog contract.

---

## CAP-CAND-LIB-02 — Component catalog projections

**Implementation state:** `VERIFIED_CURRENT_DRAFT_PROJECTION`

**Confidence:** HIGH

### Implementation paths

- `catalog/materials.yaml`
- `catalog/product_families.yaml`
- `catalog/operations.yaml`
- `catalog/print_modes.yaml`
- `catalog/finishing_options.yaml`

### Current finding

The item arrays in all five component catalog files are content-equivalent in the captured packet to the corresponding sections of:

`catalog/seeds/catalog_seed_v0_1.yaml`

### Interpretation

There are two representations of the same current semantic item population:

1. combined seed;
2. per-component catalog files.

This is not automatically a harmful duplicate.

The repository contains exporter tooling elsewhere in the module, so the likely architectural pattern is:

`seed/source representation -> component projections`

However, the exact generation/source-of-truth direction is outside the Block 01 primary packet and must be reconciled with Block 04.

### Candidate

`DUPLICATE_REPRESENTATION_REQUIRES_SOURCE_DIRECTION_CONFIRMATION`

Do not deduplicate or delete anything during L2.

---

## CAP-CAND-LIB-03 — Catalog loading

**Implementation state:** `VERIFIED_CURRENT`

**Confidence:** HIGH

### Implementation paths

`app/forprint_library/catalog/loader.py`

### Entry points

- `load_yaml(path)`
- `load_seed(path=None)`
- `load_component_catalog(section, project_root=None)`
- `load_all_component_catalogs(project_root=None)`

### Behavior

The loader:

- reads YAML from filesystem;
- requires mapping-shaped YAML roots;
- resolves the default seed from repository paths;
- uses `COMPONENT_CATALOG_FILES` as the catalog-section map.

### State model

File-backed, read-only during load.

No database or API is involved.

---

## CAP-CAND-LIB-04 — Catalog structural/semantic validation

**Implementation state:** `VERIFIED_CURRENT`

**Confidence:** HIGH

### Implementation path

`app/forprint_library/catalog/validation.py`

### Validated concerns

- required seed metadata;
- expected seed maturity/status values;
- required item fields;
- allowed item statuses;
- Library ownership;
- schema status;
- unique IDs across combined seed;
- aliases must be non-empty string lists;
- duplicate normalized aliases across combined seed;
- component catalog type;
- component catalog metadata;
- component item validity.

### Alias normalization

Current normalization:

- `casefold()`
- strip outer whitespace;
- collapse internal whitespace.

### Important boundary

This validator verifies current seed/catalog structure.

It does not provide:

- historical revision selection;
- effective-date semantics;
- external-provider provenance;
- Contract Registry adoption;
- production database behavior.

---

## CAP-CAND-LIB-05 — Catalog registry and alias lookup

**Implementation state:** `VERIFIED_BEHAVIOR / IMPLEMENTATION_PATH_INCOMPLETE_IN_PACKET`

**Confidence:** MEDIUM

### Evidence

Public package surface imports:

`CatalogRegistry` from `forprint_library.catalog.registry`.

Tests use:

- `CatalogRegistry.from_project()`
- `.get(...)`
- `.resolve_alias(...)`

Tests prove successful lookup of:

- product family `business_card`;
- material `paper_300g_matte`;
- operation `digital_print`;
- print mode `color_4_0`;
- finishing option `matte_lamination`;
- aliases such as `візитка`, `350gsm gloss`, `4+4`.

Unknown alias behavior is also tested.

### Evidence gap

The implementation file:

`app/forprint_library/catalog/registry.py`

is not present in the Block 01 primary packet.

### Required treatment

Do not reconstruct or guess its internal algorithm.

Carry:

`DEPENDENCY_SOURCE_NOT_IN_BLOCK_PACKET`

At L3, locate its L1 primary block assignment and merge its implementation evidence into the final capability record.

---

## CAP-CAND-LIB-06 — Business Card configurable product reference

**Implementation state:** `VERIFIED_CURRENT_DRAFT_REFERENCE`

**Confidence:** HIGH

### Implementation paths

- `catalog/configurable_products/business_card.yaml`
- `schemas/configurable_product.schema.yaml`

### Stable product identity

`product.business_card`

### Current state

- kind: `configurable_product`
- status: `draft_reference`
- version: `0.1`
- owner: `forprint_library`

### Names

- UK: `Візитки`
- EN: `Business cards`

### Compatibility identity

Includes:

`product:business_cards`

as a compatibility alias.

### Constructor parameter model

| Parameter | Type | Required | Ownership |
|---|---|---:|---|
| `size` | choice | yes | Library definition |
| `sides` | choice | yes | Library definition |
| `material_ref` | reference_choice | yes | Library definition |
| `print_mode_ref` | reference_choice | yes | Library definition |
| `quantity` | numeric_input_context | yes | consumer value |
| `finishing_refs` | reference_list | no | Library definition |
| `artwork_source` | choice | no | consumer value |

### Referenced catalog domains

- `product_families`
- `materials`
- `print_modes`
- `finishing_options`

### Important semantic boundary

Library defines:

- product identity;
- names;
- aliases;
- parameter definitions;
- allowed semantic references.

Consumers own:

- selected values;
- channel/routing context;
- pricing input context;
- operational foreign metadata.

### Explicit non-goals

The card explicitly excludes:

- full product catalog;
- product modeling UI;
- production catalog DB;
- live API;
- 1C import/sync;
- live Calculator integration;
- Telegram runtime integration;
- Operational Registry write;
- CRM/Website writes;
- price/final-price formulas;
- material write-off;
- warehouse stock truth;
- production task creation;
- real client/order data;
- production runtime.

This boundary is aligned with current Blueprint policy.

---

## CAP-CAND-LIB-07 — Consumer-boundary metadata for configurable product semantics

**Implementation state:** `VERIFIED_CURRENT_REFERENCE_METADATA`

**Confidence:** HIGH

### Evidence

`business_card.yaml` contains explicit consumer usage notes for:

- Telegram Bot;
- Calculator Engine;
- Operational Registry.

### Meaning

This is a semantic handoff description.

It is not a runtime integration.

The file correctly distinguishes:

`may consume/reference`

from:

`Library owns or executes`.

---

# 5. Public and internal entrypoints

## 5.1 Current Python package entrypoint

`forprint_library.catalog`

Current exported names:

- `CatalogRegistry`
- `load_all_component_catalogs`
- `load_seed`
- `validate_catalog_seed`

This is the strongest current code-level public surface visible in the packet.

## 5.2 File/data entrypoints

- `catalog/seeds/catalog_seed_v0_1.yaml`
- component `catalog/*.yaml`
- `catalog/configurable_products/business_card.yaml`

## 5.3 Schema entrypoints

- `schemas/catalog_seed.schema.yaml`
- `schemas/configurable_product.schema.yaml`
- component catalog schemas.

## 5.4 Non-entrypoints

The two coordination scripts included in the L1 block are not domain-semantic public entrypoints.

---

# 6. State and data model

## 6.1 Catalog item core fields

Current catalog items require:

- `id`
- `name_uk`
- `name_en`
- `aliases`
- `status`
- `version`
- `owner_module`
- `schema_status`
- `notes`

## 6.2 Allowed item lifecycle values

Current implementation allows:

- `draft`
- `active`
- `deprecated`
- `experimental`

The current seed uses only `draft`.

## 6.3 ID constraints

JSON Schema constrains current basic catalog IDs to:

`^[a-z0-9_]+$`

Configurable product IDs use:

`^product\.[a-z0-9_]+$`

## 6.4 Version maturity

The current data model has `version` and status fields, but Block 01 does not yet implement the richer target lifecycle described in Blueprint planning:

- effective-from;
- supersedes;
- historical revision lookup;
- migration graph;
- consumer freshness/adoption state.

These are future/reconciliation concerns, not hidden current features.

---

# 7. Schema assessment

## 7.1 Catalog schemas

The component schemas consistently require:

- catalog type;
- metadata;
- item list;
- item identity/names/aliases/status/version/owner/schema-status/notes.

This creates a coherent structural contract across catalog categories.

## 7.2 Seed schema

The seed schema requires all five current sections.

This makes the v0.1 seed a single combined semantic population.

## 7.3 Configurable product schema

The configurable product schema proves the existence of a controlled product-card shape.

However, it remains intentionally/permissively extensible:

- many objects allow additional properties;
- constructor-parameter objects require only a small structural core;
- cross-reference validity is not fully expressible in this schema alone;
- ownership semantics are represented by data fields/notes and external validation rather than fully enforced by JSON Schema.

This is not automatically a defect.

It means full Business Card semantic validation depends on validator/test surfaces outside the primary Block 01 source set.

---

# 8. Test evidence assessment

The packet contains 17 related test files.

They are not equally direct to Block 01.

---

## 8.1 Direct high-value Block 01 tests

### `tests/contract/test_catalog_seed_v0_1.py`

**Relevance:** DIRECT / HIGH

Proves:

- seed loads and validates;
- expected maturity metadata;
- global ID uniqueness;
- alias presence;
- no current duplicate normalized aliases;
- required fields;
- all five sections exist;
- all five component catalogs validate;
- JSON Schema validity;
- example validity;
- registry alias lookup behavior;
- unknown alias behavior.

This is the strongest test file for the block.

### `tests/integration/test_catalog_projection_readiness.py`

**Relevance:** DIRECT / HIGH

Proves:

- current seed is projection-ready under the explicit draft status;
- stable known IDs are retrievable through `CatalogRegistry`.

### `tests/content/test_business_card_product_card.py`

**Relevance:** DIRECT / HIGH

Proves:

- Business Card files exist;
- product ID is stable;
- bilingual names/aliases;
- constructor parameters;
- Library references;
- validator/preview can execute;
- forbidden ownership fields are absent.

---

## 8.2 Strong cross-block consumer evidence

### `tests/content/test_calculator_input_contract.py`

**Relevance:** CROSS-BLOCK / HIGH

This is primarily a Block 03 contract test, but it proves that Block 01 semantics are consumable as deterministic Calculator input context.

Important proven boundary:

- no monetary fields;
- no filesystem writes;
- no network use;
- Library input projection does not become Calculator pricing logic.

Do not classify Calculator input implementation as a Block 01 capability.

### `tests/content/test_library_reference_contract.py`

**Relevance:** CROSS-BLOCK / HIGH

Supports stable Library reference semantics and boundary enforcement.

Primary ownership is Block 03.

### `tests/coordination/test_reference_consumption_pilot.py`

**Relevance:** CROSS-BLOCK / MEDIUM-HIGH

Proves example downstream consumers can consume Library references without semantic redefinition.

### `tests/coordination/test_reference_consumption_pilot_closure.py`

**Relevance:** COMPLETION/COORDINATION

Useful lifecycle evidence, not core Block 01 behavior.

---

## 8.3 Supporting architecture/boundary evidence

### `tests/contract/test_architecture_docs.py`

**Relevance:** SUPPORTING

Supports:

- stable canonical IDs;
- alias policy;
- downstream consumers;
- catalog seed maturity terms;
- exclusion of operational ownership.

Document authority itself remains an L4 question.

### `tests/contract/test_semantic_reference_readiness.py`

**Relevance:** SUPPORTING / CROSS-BLOCK

Supports projection/reference boundary and downstream handoff.

### `tests/coordination/test_business_card_skeleton_closure.py`

**Relevance:** COMPLETION EVIDENCE

Supports completion record for the Business Card checkpoint.

### `tests/coordination/test_calculator_input_contract_completion.py`

**Relevance:** COMPLETION EVIDENCE / CROSS-BLOCK

Proves recorded Calculator contract completion evidence and validation counts.

It does not make that contract a Block 01 implementation.

### `tests/contract/test_completion_report.py`

**Relevance:** COMPLETION EVIDENCE

Historical/current reporting surface around initial catalog seed.

---

## 8.4 Adjacent tests that should not define Block 01 capability truth

These are useful module context but primarily belong to other blocks:

- `tests/contract/test_dictionary_policy_docs.py`
- `tests/contract/test_shared_dictionary_completion_report.py`
- `tests/contract/test_shared_operational_dictionary_v0_1.py`
- `tests/integration/test_dictionary_resolver_and_preview.py`
- `tests/coordination/test_coordination_foundation_alignment.py`

These indicate that L1 secondary-test selection is intentionally broad and should not be interpreted as capability ownership.

---

# 9. Dependency map

## 9.1 Internal Library dependencies

### Block 02 — dictionaries/resolution/profiles

Relationship:

- aliases and semantic resolution concepts overlap;
- naming/profile semantics belong primarily there;
- catalog alias behavior must eventually reconcile with shared dictionary resolver behavior.

### Block 03 — contracts/cross-module consumption

Relationship:

- Library reference contract;
- Library → Calculator input contract;
- downstream consumer payloads;
- Contract Registry/adoption semantics.

### Block 04 — exports/previews/examples

Relationship:

- component catalog export/generation direction;
- Business Card previews/examples;
- seed/component projection direction.

### Block 05 — validation/tests/quality

Relationship:

- Business Card validator;
- catalog/product validation orchestration;
- check/report surfaces.

### Block 06 — coordination/governance/intake

Relationship:

- two primary files currently misclassified into Block 01;
- completion/acceptance/status evidence.

### Block 07 — documentation/architecture

Relationship:

- canonical ID policy;
- alias policy;
- catalog seed policy;
- dependent-module usage;
- Library boundary docs.

## 9.2 External module dependencies/consumers

Current authority/planning identifies major consumers including:

- Calculator Engine;
- Telegram Bot;
- Operations Control Registry;
- Accounting mappings;
- Prepress;
- Website/catalog;
- Operations Assistant;
- CRM;
- Warehouse.

The current Block 01 implementation does not prove all these consumers are live-integrated.

---

# 10. Ownership and authority assessment

## 10.1 Confirmed aligned ownership

Current implementation is aligned with Blueprint policy for:

- product catalog semantics;
- material catalog semantics;
- operation catalog semantics;
- aliases;
- canonical/reference IDs.

## 10.2 Partial policy coverage

Blueprint policy also includes:

- service catalog semantics;
- templates;
- technical cards;
- contract definitions;
- UI design-system publication;
- reusable UI component catalog.

Block 01 current implementation does not prove those broader surfaces.

## 10.3 Confirmed exclusions

Block 01 does not own:

- operational orders;
- clients;
- accounting/payment truth;
- warehouse stock truth;
- production runtime;
- CRM workflow;
- Calculator pricing/calculation truth.

Stage 1 reconciliation also found no actual authority leakage.

---

# 11. Roadmap ↔ implementation relation

Roadmap state and implementation state are intentionally separate below.

---

## FORPRINT_LIBRARY-H01
**Roadmap:** Reconcile current catalog, alias, template, naming-profile and UI publication evidence.  
**Roadmap state:** `AGREED_PLANNING_DIRECTION`  
**Block 01 implementation state:** `PARTIAL_CURRENT`

Implemented/proven here:

- catalog seed;
- component catalogs;
- aliases;
- Business Card reference.

Not proven here:

- templates;
- naming profiles;
- UI publication.

---

## FORPRINT_LIBRARY-H02
**Roadmap:** Confirm ownership of product/material/service/operation semantics and shared UI publication.  
**Roadmap state:** `AGREED_PLANNING_DIRECTION`  
**Block 01 implementation state:** `PARTIAL_CURRENT`

Proven:

- product-family semantics;
- material semantics;
- operation semantics;
- print-mode/finishing semantics.

Not proven:

- service catalog implementation;
- UI publication implementation.

---

## FORPRINT_LIBRARY-H03
**Roadmap:** Complete capability/self-inventory for IDs, aliases, misspellings, production tokens, templates and technical cards.  
**Roadmap state:** `AGREED_PLANNING_DIRECTION`  
**Block 01 implementation state:** `PARTIAL_CURRENT`

Proven:

- canonical/draft IDs;
- aliases.

Not proven in Block 01:

- mature misspelling governance;
- production-token profiles;
- templates;
- technical cards.

---

## FORPRINT_LIBRARY-H04
**Roadmap:** Versioned naming/profile/default semantics.  
**Roadmap state:** `AGREED_PLANNING_DIRECTION`  
**Block 01 implementation state:** `NOT_PROVEN_IN_BLOCK`

Likely Block 02/future concern.

---

## FORPRINT_LIBRARY-H05
**Roadmap:** Material/product/service canonical identifiers and stable lookup contracts for Warehouse/consumers.  
**Roadmap state:** `AGREED_OR_RECOVERED_TARGET`  
**Block 01 implementation state:** `PARTIAL_CURRENT`

Proven:

- product/material IDs;
- current lookup behavior by tests.

Not proven:

- service identifiers;
- Warehouse-specific stable lookup contract;
- mature lifecycle/adoption.

---

## FORPRINT_LIBRARY-H06 / H07
**Roadmap:** UI design-system package lifecycle and adoption metadata.  
**Block 01 implementation state:** `NONE_PROVEN`

L1 already established:

`UI_DESIGN_SYSTEM_IMPLEMENTATION_PROVEN=false`

---

## FORPRINT_LIBRARY-H08
**Roadmap:** Fast capability/semantic discovery.  
**Roadmap state:** `PROPOSED_TARGET_REFINEMENT`  
**Block 01 implementation state:** `PRIMITIVE_ONLY / INCOMPLETE_EVIDENCE`

`CatalogRegistry` may be an early local lookup primitive.

It is not evidence of the planned cross-module semantic/capability discovery system.

---

## FORPRINT_LIBRARY-H09
**Roadmap:** Deprecation/migration paths for legacy aliases/profiles.  
**Roadmap state:** `PROPOSED_TARGET_REFINEMENT`  
**Block 01 implementation state:** `PRIMITIVE_ONLY`

The item model supports `deprecated` status.

No migration graph/profile migration/adoption evidence is present in Block 01.

---

## FORPRINT_LIBRARY-H10
**Roadmap:** Hold broader implementation until Contract Registry and consumer readiness are reconciled.  
**Type:** governance gate  
**Block 01 implementation state:** not applicable as implementation capability.

---

## FORPRINT_LIBRARY-H11 / H12
**Roadmap:** historical/reference asset semantics and domain boundary.  
**Block 01 implementation state:** `NONE_PROVEN`

---

# 12. Human Intent relation

---

## HI-FP-LIBRARY-001 — stable canonical IDs + versioned schemas

**Relation:** `PARTIALLY_IMPLEMENTED`

Current Block 01 has stable-looking IDs, versions and schemas.

But the implementation remains `unstable_v0_1` / draft and does not cover all policy domains such as services.

---

## HI-FP-LIBRARY-002 — aliases + provenance/confidence semantic layer

**Relation:** `PARTIAL`

Implemented:

- aliases;
- normalization.

Not proven:

- provider provenance;
- confidence;
- external-source lineage.

---

## HI-FP-LIBRARY-003 — external catalog ingestion provenance

**Relation:** `NOT_IMPLEMENTED_IN_BLOCK`

No ingestion pipeline is present here.

---

## HI-FP-LIBRARY-004 — calibration profiles

**Relation:** `NOT_IMPLEMENTED_IN_BLOCK`

---

## HI-FP-LIBRARY-005 — deterministic typed versioned read-only Calculator input

**Relation:** `CROSS_BLOCK_CURRENT_EVIDENCE`

Block 01 supplies product/reference semantics.

The actual Calculator input contract belongs to Block 03.

Tests in this packet support the boundary.

---

## HI-FP-LIBRARY-006 / 013 — SOP/instruction/media guidance

**Relation:** `NOT_IMPLEMENTED_IN_BLOCK`

L1 also found no current SOP/media implementation block.

---

## HI-FP-LIBRARY-007 / 014 — UI Design System ownership/publication

**Relation:** `POLICY_AND_INTENT_ONLY_IN_CURRENT PILOT EVIDENCE`

No Block 01 implementation.

---

## HI-FP-LIBRARY-008 — canonical reference photos/product media

**Relation:** `NOT_IMPLEMENTED_IN_BLOCK`

---

## HI-FP-LIBRARY-009 — aliases, misspellings, production tokens, naming profiles/defaults

**Relation:** `PARTIAL`

Aliases exist.

Naming profiles/defaults/device-context semantics are not proven here.

---

## HI-FP-LIBRARY-010 / 011 — profile-specific omission/default and token context

**Relation:** `NOT_IMPLEMENTED_IN_BLOCK`

Likely Block 02/future.

---

## HI-FP-LIBRARY-012 — Contract Registry/adoption process

**Relation:** `NOT_IMPLEMENTED_IN_BLOCK`

Cross-block/future architecture.

---

## HI-FP-LIBRARY-015 / semantic-registry intents — reusable discovery and registration

**Relation:** `EARLY PRIMITIVE / TARGET NOT PROVEN`

Local registry lookup is not equivalent to the target semantic registry/discovery capability.

---

# 13. Duplicate / overlap / ambiguity candidates

No candidate below authorizes deletion or refactor.

---

## DUP-CAND-LIB-01 — Combined seed vs component catalogs

**Type:** `PARALLEL_REPRESENTATION`

**Observed:**

The five component `items` lists match the corresponding combined seed sections in the packet.

**Risk:**

Potential drift if both become independently edited authorities.

**Counter-evidence:**

Repository export tooling suggests the representation may be intentional.

**Disposition:**

`RECONCILE_SOURCE_DIRECTION_WITH_BLOCK_04`

Do not delete.

---

## DUP-CAND-LIB-02 — Operation vs finishing-option semantic pairs

Examples:

- operation `rounding`
- finishing option `corner_rounding`

and:

- operation `folding`
- finishing option `finishing_folding`

These are not currently exact duplicate IDs or aliases.

They appear to model different semantic layers:

- production operation;
- selectable finishing option.

**Disposition:**

`DISTINCT_SEMANTICS_CURRENTLY_PLAUSIBLE`

Later Knowledge Base should preserve the distinction and document relation.

---

## DUP-CAND-LIB-03 — Product family `business_card` vs configurable product `product.business_card`

This is not a duplicate.

Observed layering:

- family/catalog identity: `business_card`;
- configurable product identity: `product.business_card`.

The configurable product explicitly references the family.

**Disposition:**

`INTENTIONAL_LAYERED_IDENTITY`

Do not merge.

---

# 14. Reuse candidates

## REUSE-CAND-LIB-01 — Catalog loader/validator

Potential shared internal primitive for:

- catalog projections;
- validation tooling;
- downstream inspection.

Reuse should remain Library-owned rather than copied into consumers.

## REUSE-CAND-LIB-02 — Configurable product semantic card pattern

The Business Card card is a candidate pattern for future configurable products.

Do not mass-produce new product cards during analysis.

A future bounded implementation task should first confirm:

- schema maturity;
- parameter ownership rules;
- reference contract;
- Calculator consumption pattern.

## REUSE-CAND-LIB-03 — Stable semantic reference pattern

Current IDs + aliases + read-only consumer references are reusable architectural patterns for other modules.

Consumers should reference them rather than create shadow catalogs.

---

# 15. Migration candidates

## MIG-CAND-LIB-01 — Mature catalog lifecycle

Current v0.1 draft semantics will eventually need a controlled migration path toward:

- stable/revisioned lifecycle;
- effective dates;
- supersession;
- deprecation support;
- historical resolution.

This is roadmap work, not an L2 implementation action.

## MIG-CAND-LIB-02 — Shadow consumer vocabularies

Blueprint/Human Intent requires consumers to avoid private competing vocabularies.

Block 01 does not inventory consumer shadow catalogs.

Cross-module migration candidates should be discovered later, not inferred here.

---

# 16. Wrong-owner candidates

No confirmed wrong-owner business capability was found in Block 01.

The only clear block-placement issue is analysis segmentation:

- `scripts/coordination/export_coordination_foundation_alignment_closure.py`
- `scripts/coordination/validate_coordination_foundation_alignment.py`

These belong functionally to coordination/governance analysis.

No evidence suggests Library is currently implementing pricing, order, accounting, warehouse or production truth.

---

# 17. Current architecture fit

**Architecture generation fit:** `CURRENT_BLUEPRINT_ALIGNED_WITH_DRAFT_MATURITY`

Rationale:

- ownership is consistent with current Blueprint policy;
- boundaries are explicitly encoded;
- consumers are modeled as reference consumers;
- pricing/operational/accounting truth are excluded;
- current maturity is honestly marked draft/projection-only.

The implementation is not legacy standalone architecture.

It is also not yet the full mature target state.

---

# 18. Important maturity caveats

A future assistant must not say:

> Library already has the final canonical production catalog.

Correct statement:

> Library currently has a Library-owned **draft canonical seed/reference catalog**, explicitly `unstable_v0_1`, `allowed_for_projection_use`, and `not_final_contract`.

A future assistant must not say:

> Library has full Product/Service catalog coverage.

Correct statement:

> Current Block 01 proves materials, product families, operations, print modes, finishing options, and one configurable Business Card product reference. A current service catalog is not proven in this block.

A future assistant must not say:

> Library calculates Business Card prices.

Correct statement:

> Library defines Business Card semantic/configuration input structure. Pricing remains Calculator-owned.

A future assistant must not say:

> Business Card card creates orders or production tasks.

Correct statement:

> It is a read/reference semantic product card only.

---

# 19. Block uncertainty register

## UNC-LIB-B01-001 — `CatalogRegistry` implementation source absent

**Severity:** MEDIUM

Behavior is strongly test-proven, but implementation source is outside this packet.

Carry to L3.

## UNC-LIB-B01-002 — seed/component source direction

**Severity:** MEDIUM

Current data is equivalent, but the authoritative editing/generation direction should be confirmed in Block 04.

## UNC-LIB-B01-003 — Business Card validator internals outside packet

**Severity:** LOW-MEDIUM

Tests prove execution, but the validator implementation belongs outside the Block 01 source population.

## UNC-LIB-B01-004 — Blueprint acceptance state for latest Calculator input contract

**Severity:** OUTSIDE BLOCK

Completion evidence says ready/pending Blueprint review.

Do not resolve in Block 01.

## UNC-LIB-B01-005 — service semantics implementation

**Severity:** MEDIUM

Policy says Library owns service catalog semantics.

No service catalog implementation is proven by this block.

## UNC-LIB-B01-006 — mature lifecycle/version semantics

**Severity:** EXPECTED ROADMAP GAP

Current version/status primitives are not the full target revision/effective/supersession model.

---

# 20. Evidence-to-capability matrix

| Capability candidate | Implementation evidence | Test evidence | State | Confidence |
|---|---|---|---|---|
| Draft canonical seed | seed + schemas + loader | catalog seed tests | VERIFIED_CURRENT_DRAFT_PROJECTION | HIGH |
| Component catalogs | five component YAMLs | component validation tests | VERIFIED_CURRENT_DRAFT_PROJECTION | HIGH |
| Catalog loading | loader.py | seed/component tests | VERIFIED_CURRENT | HIGH |
| Catalog validation | validation.py | catalog tests | VERIFIED_CURRENT | HIGH |
| Registry/alias lookup | public import only in primary block | registry lookup tests | VERIFIED_BEHAVIOR / SOURCE_INCOMPLETE | MEDIUM |
| Business Card configurable product | product YAML + schema | Business Card tests | VERIFIED_CURRENT_DRAFT_REFERENCE | HIGH |
| Business Card downstream semantic boundary | card usage/boundary notes | Business Card + Calculator tests | VERIFIED_CURRENT_REFERENCE_METADATA | HIGH |
| Production catalog DB/API | none | explicit negative/boundary tests | NOT_IMPLEMENTED | HIGH |
| Pricing | none | monetary/ownership exclusions | NOT_LIBRARY_OWNED | HIGH |
| UI Design System | none | no direct current implementation | NOT_PROVEN | HIGH |
| SOP/media knowledge | none | no direct current implementation | NOT_PROVEN | HIGH |

---

# 21. L2 Block 01 disposition

## Analysis result

`L2_BLOCK_01=PASS_FOR_ANALYSIS`

## Knowledge result

`CURRENT_DOMAIN_CATALOG_CORE_CONFIRMED`

## Maturity result

`CURRENT_DRAFT_PROJECTION_NOT_FINAL_CONTRACT`

## Boundary result

`BLUEPRINT_OWNERSHIP_BOUNDARY_ALIGNED`

## Reconciliation candidates

- two coordination scripts misclassified into Block 01;
- `CatalogRegistry` implementation path absent from packet;
- seed/component source-direction requires Block 04 confirmation.

## Implementation action created

`NONE`

## Source mutation

`NONE`

## Roadmap mutation

`NONE`

---

# 22. Carry-forward records for later stages

## To L3 — Module synthesis

Carry provisional capability candidates:

- draft canonical catalog seed;
- component catalog projections;
- catalog loading;
- catalog validation;
- registry/alias lookup;
- Business Card configurable product;
- consumer-boundary metadata.

Do not finalize capability IDs until all L2 blocks are analyzed.

## To L4 — Document authority reconciliation

Review authority of:

- catalog seed policy;
- canonical ID policy;
- alias policy;
- dependent module usage;
- Library boundaries;
- Business Card documentation;
- completion reports.

## To L5 — Capability reconciliation

Reconcile:

- component catalogs vs seed source direction;
- catalog alias resolver vs shared dictionary resolver;
- operation vs finishing-option semantics;
- registry placement;
- coordination-script block placement.

## To L6 — Roadmap linkage

Use the roadmap mapping in this report as Block 01 evidence, but do not finalize module-wide roadmap implementation status until all blocks are analyzed.

---

# 23. Next sequential block

Per the L1 closeout order:

`02_dictionaries_resolution_profiles`

Before moving forward, preserve this report as:

`tmp/module_knowledge_analysis/forprint_library/01_domain_semantics_catalog/analysis_report.md`

Do not commit/push the temporary pilot analysis workspace yet.

---

# 24. Final statement

Block 01 proves that ForPrint Library already contains a meaningful semantic/catalog core, but the correct description is narrower and more mature-aware than “Library has a catalog”.

The current truth is:

> Library has a file-backed, schema-validated, Library-owned draft canonical semantic catalog/reference layer with stable current IDs/aliases, five component catalog domains, and one controlled configurable Business Card reference. It is explicitly projection-ready but not a final production contract. It does not own pricing, operational order state, accounting truth, stock truth or production runtime.

The Stage 2 analysis should preserve that distinction exactly.

**Final L2 Block 01 status: `PASS_FOR_ANALYSIS_WITH_RECONCILIATION_CANDIDATES`.**
```

# Part E — Blueprint context

## Blueprint context

**Path:** `coordination/module_policy/forprint_library/module_policy.md`
**SHA256:** `60010ad1b6ae83a18ee0828139708a4523d01c67a424143b7c427b70c3c5414c`

```markdown
# Module Policy — ForPrint Library

## Module ID

```text
forprint_library
```

## Priority

```text
p1
```

## Development status

```text
active_development
```

## Strategic role

Canonical semantic, catalog, naming, alias and contract-definition authority for products, services, materials, operations and templates.

## Main goals

- `Own canonical product/service/material/operation IDs.`
- `Maintain aliases and naming rules.`
- `Provide semantic resolution for module ambiguity.`
- `Keep contract definitions and catalog semantics versioned.`
- `Publish the versioned shared ForPrint UI design-system package and reusable component catalog.`
- `Expose searchable semantic and reusable-capability references before modules create competing implementations.`

## Owns

- `product_catalog_semantics`
- `service_catalog_semantics`
- `material_catalog_semantics`
- `operation_catalog_semantics`
- `aliases`
- `templates`
- `technical_cards`
- `contract_definitions`
- `ui_design_system_publication`
- `shared_ui_component_catalog`
- `ui_component_version_and_adoption_metadata`

## Must not own

- `operational_orders`
- `client_database`
- `accounting_truth`
- `production_runtime`
- `crm_workflow`
- `domain_business_rules_outside_library_semantics`

## Next focus

- `Canonical Product/Service ID and Alias Governance.`
- `Define ambiguity routing and approval lifecycle.`
- `Prepare contract registry direction.`
- `Publish the first versioned shared UI component/catalog surface.`
- `Strengthen reusable semantic/capability discoverability without absorbing domain ownership.`

## Adoption rule

This module policy is strategic guidance. It does not automatically authorize large refactors or broad rewrites. The module should compare this policy with its current implementation and report alignment, conflicts or questions to Blueprint.
```

## Blueprint context

**Path:** `coordination/human_intent/modules/forprint_library.yaml`
**SHA256:** `920d0f2d76b0d4af1667aef8514fc9c790c875ff8e6bfb8c045686be60eaf248`

```yaml
schema_version: forprint_module_human_intent_ledger_v0_1
module_id: forprint_library
display_name: ForPrint Library
authority: planning_context_not_release_authority
status: active_planning_context
append_only: true
intents:
  - status: RECOVERED
    text: Library володіє stable canonical IDs і versioned schemas для products/materials/services/operations.
    context: Price/accounting/operational state від цього відділений.
    roadmap: ''
    intent_id: HI-FP-LIBRARY-001
  - status: RECOVERED
    text: Aliases, supplier part numbers, alternate names, normalization rules і provenance/confidence мають бути
      частиною semantic layer.
    context: Це дозволяє безпечно мапити зовнішні джерела.
    roadmap: ''
    intent_id: HI-FP-LIBRARY-002
  - status: RECOVERED
    text: External catalog ingestion повинен зберігати source/provider/fetched-at/key/hash/raw snapshot refs і давати
      human review для ambiguous merge.
    context: Не переписувати canonical truth без підтвердження.
    roadmap: ''
    intent_id: HI-FP-LIBRARY-003
  - status: AGREED
    text: Library є canonical owner calibration profiles для фізичних вимірювань Operations Assistant, включно з
      параметрами товщини/ваги/толерансів.
    context: Сам Assistant лише використовує профіль.
    roadmap: ''
    intent_id: HI-FP-LIBRARY-004
  - status: RECOVERED
    text: Library -> Calculator reference input має бути deterministic, typed, versioned і read-only.
    context: Pricing formulas залишаються в Calculator.
    roadmap: ''
    intent_id: HI-FP-LIBRARY-005
  - status: AGREED
    text: Library повинна зберігати SOP/instruction/media knowledge для contextual work guidance.
    context: Operations Assistant показує потрібну інструкцію з контексту.
    roadmap: ''
    intent_id: HI-FP-LIBRARY-006
  - status: RECOVERED
    text: Canonical ForPrint Design System owner закріплений за Library; Website та інші UI мають мігрувати до нього
      без page-local систем.
    context: Це вже було окремо додано в Blueprint.
    roadmap: ''
    intent_id: HI-FP-LIBRARY-007
  - status: AGREED
    text: Reference photos/product media можуть індексуватися Semantic Retrieval, але Library лишається owner canonical
      assets/metadata.
    context: Пошуковий індекс — projection.
    roadmap: ''
    intent_id: HI-FP-LIBRARY-008
  - intent_id: HI-FP-LIBRARY-009
    status: AGREED
    text: Library owns canonical aliases, common misspellings, short production tokens, naming profiles and profile-specific
      defaults for materials/operations/device capabilities.
    context: Calculator consumes these definitions instead of maintaining a private vocabulary.
    roadmap: LIB-FILE-01
  - intent_id: HI-FP-LIBRARY-010
    status: AGREED
    text: A short human filename may omit common information only when the active naming profile defines the default
      unambiguously.
    context: 'Example: Ricoh lamMat represents the agreed default thin matte roll lamination.'
    roadmap: LIB-FILE-02
  - intent_id: HI-FP-LIBRARY-011
    status: AGREED
    text: The same short token may have different meaning across equipment/production profiles, so structured profile/capability
      context must remain explicit.
    context: Do not globally interpret a token without its naming/production profile.
    roadmap: LIB-FILE-03
  - intent_id: HI-FP-LIBRARY-012
    status: AGREED
    text: Library semantic changes that affect inter-module payloads must flow through a versioned Contract Registry/adoption
      process rather than being changed locally in one consumer.
    context: Avoid modules drifting onto different meanings of the same field/token.
    roadmap: LIB-FILE-04
  - intent_id: HI-FP-LIBRARY-013
    status: AGREED
    text: Library should eventually provide standardized visual/SOP instructions for Job Ticket and Operations Assistant
      steps, with manager-provided notes/images as fallback when no standard exists.
    context: Human guidance is a Library knowledge responsibility; execution truth remains OCR.
    roadmap: LIB-FILE-05
  - intent_id: HI-FP-LIBRARY-014
    status: AGREED
    text: Library is publication owner for shared ForPrint UI tokens, themes, reusable components, component catalog,
      versions and adoption metadata.
    context: Blueprint governs; consumers compose; Inspector validates.
    roadmap: LIB-UI-01
  - intent_id: HI-FP-LIBRARY-015
    status: AGREED
    text: Shared indexes should help modules discover reusable technical primitives and semantic definitions before
      creating competing implementations.
    context: Domain business rules still belong to domain owners.
    roadmap: LIB-INDEX-01
  - intent_id: HI-LIBRARY-U131-20260906-001
    status: AGREED
    text: ForPrint Library is the shared semantic and contract reference authority; modules should consult its existing
      canonical/recommended semantics before creating significant competing shared implementations.
    context: This extends the Library role already present in module policy; it does not move domain business ownership
      into Library.
    roadmap: LIB-SEMANTIC-REGISTRY
  - intent_id: HI-LIBRARY-U131-20260906-002
    status: AGREED
    text: A first registered semantic ID may remain stable while maturity, recommended implementation names, aliases
      and contract versions evolve.
    context: Registration does not automatically mean CANONICAL.
    roadmap: LIB-SEMANTIC-REGISTRY
  - intent_id: HI-LIBRARY-U131-20260906-003
    status: AGREED
    text: Semantic registration should prioritize module-public, cross-module, external-boundary, high-criticality
      and widely reused surfaces rather than every local helper.
    context: Interaction scope and criticality are independent signals for standardization review.
    roadmap: LIB-SEMANTIC-REGISTRY
  - intent_id: HI-LIBRARY-U131-20260906-004
    status: AGREED
    text: Library should batch unresolved semantic registration/enrichment proposals and publish versioned semantic
      changes; Blueprint remains responsible for rollout timing and adoption mode across affected modules.
    context: Adoption may be informational, new-code-only, migrate-on-touch, roadmap-required or migration-required.
    roadmap: LIB-SEMANTIC-REGISTRY
  - intent_id: HI-LIBRARY-ARCH-20260919-001
    status: RECOVERED
    text: Historical/reference asset indexing should use stable asset and revision semantics with provenance; an index/search
      result is a projection and must not become canonical asset, order or production truth.
    context: Recovered from the 2026-09-19 historical asset indexing discussion.
    roadmap: ''
    source_refs:
    - coordination/internal_work/blueprint/evening_reviews/2026-09-19/forprint_evening_architecture_handoff_20260919_v0_1/00_README.md
    - coordination/internal_work/blueprint/evening_reviews/2026-09-19/forprint_evening_architecture_handoff_20260919_v0_1/10_portfolio_reconciliation_20260921_v0_1.yaml
```

## Blueprint context

**Path:** `coordination/repository_knowledge/module_knowledge_stabilization/library_pilot_execution_plan_v0_1.md`
**SHA256:** `ebe71f6dcd1cb4fa8ea726e44d197ea5d13a6e14bae156461d102c01642b4d32`

```markdown
# Library Pilot Execution Plan v0.1

## Goal

Use `forprint_library` to prove the complete Module Knowledge Stabilization procedure before automating it or applying it to high-risk legacy modules.

The pilot is analysis and knowledge construction, not opportunistic refactoring.

## L0 — Preflight

Capture branch, HEAD/upstream, dirty state, module policy/governance, current coordination status and known Stage 1 Library evidence.

Output: `00_preflight/module_scope_and_authority.md`.

## L1 — Inventory and segmentation

Build repository inventory and functional analysis blocks.

Do not assume directory boundaries equal capability boundaries.

Outputs:
- block directories under `tmp/module_knowledge_analysis/forprint_library/`;
- `manifest.yaml` for each block;
- module-wide file classification.

## L2 — Sequential block analysis

Analyze one block at a time.

Each `analysis_report.md` contains:
- capabilities;
- implementation paths;
- entrypoints;
- state/data;
- dependencies;
- tests;
- documents;
- roadmap/Human Intent evidence;
- duplicate/migration/reuse candidates;
- uncertainty.

Do not synthesize before all selected block reports exist.

## L3 — Module synthesis

Create stable capability IDs and merge findings.

Output: draft Module Knowledge Base.

## L4 — Document authority reconciliation

Assign authority and assistant visibility to instruction-like/documentation surfaces.

Output: Document Authority Registry.

## L5 — Capability reconciliation

Find duplicates, partial alternatives, misplaced ownership and cross-module reuse/migration candidates.

Output: Capability Reconciliation Registry.

## L6 — Roadmap ↔ implementation linkage

For every major capability record:
- roadmap explicit/implied/absent/conflicting;
- implementation current/partial/none/legacy/unknown;
- evidence.

## L7 — Publish knowledge surfaces

Produce:
- Module Knowledge Index;
- Module Knowledge Base;
- registries;
- unresolved-decision list.

## L8 — Produce cleanup work package

Only now describe cleanup/migration/document/test work for a later bounded implementation task.

## L9 — Design maintenance automation

Use:
1. proven Library data model;
2. Blueprint's existing knowledge/index implementation as behavioral reference.

Automate mechanical maintenance; keep semantic authority decisions review-gated.

## Pilot success criteria

A new assistant can answer without scanning the entire repository:
- what Library can do;
- where important capabilities live;
- which tests prove them;
- which documents are current;
- which documents are historical/conflicting;
- which duplicate/reuse/migration candidates exist;
- which roadmap ideas are already implemented;
- what the exact next work item is.
```

## Blueprint context

**Path:** `coordination/repository_knowledge/roadmap_enrichment/current_state_reconciliation/forprint_library_reconciliation_20260923_v0_1.md`
**SHA256:** `30b8f3a6af8073b4f7dd1ba86e321b08ce4dac7bc3c8423229c4683f39f9142a`

```markdown
# ForPrint Library — current-state reconciliation closeout

## Result

**CURRENT_LIBRARY_HISTORICAL_CANDIDATES_CONFIRMED**

The Library historical front is closed against committed module state at:

`bba52bf6001f256a5c13ea7dbe175336b431754c`

Branch:

`feature/library-calculator-input-contract-v01`

## Correct historical scope

The historical surface contains:

- 2 provenance/reconciliation records;
- 4 actual `*_candidate` records;
- 5 Human Intent records.

The two `*_reconciliation` records are provenance and are not counted as
implementation candidates.

### Actual candidates closed

1. `dftb_library_blueprint_standardization_calculator_contract_20260705_governance_candidate`
2. `dftb_library_blueprint_standardization_calculator_contract_20260705_calculator_candidate`
3. `dftb_library_architecture_genesis_20260516_admin_candidate`
4. `dftb_library_architecture_genesis_20260516_contract_lineage_candidate`

## Human Intent coverage

All five Human Intents have focused committed current proof surfaces:

1. `HI-FP-LIBRARY-STRUCTURE-20260705-001`
2. `HI-FP-REPORT-DEDUP-20260705-001`
3. `HI-FP-LIBRARY-ADMIN-20260516-001`
4. `HI-FP-DATA-CONTRACT-CONSISTENCY-20260516-001`
5. `HI-FP-CONTRACT-DUAL-FORM-20260516-001`

Reconciliation result:

```text
HUMAN_INTENTS_FOCUSED_CURRENT_PROOF=5
HUMAN_INTENTS_EXACT_ASSERTION_REVIEW=0
HUMAN_INTENTS_PARTIAL_CURRENT=0
HUMAN_INTENTS_NO_FOCUSED_EVIDENCE=0
```

The focused scan covered 194 committed test symbols and 287 committed production
symbols.

## Authority review

The first focused pass found four phrases that appeared to claim excessive Library
authority:

- `Library owns order state`
- `Library owns pricing logic`
- `Library owns warehouse stock truth`
- `Library owns payment/accounting truth`

Exact AST/context review proved all four are **negative validation rules / fixtures**
inside the Library reference-contract validator.

```text
SIGNAL_OCCURRENCES=4
NEGATIVE_VALIDATION_OR_FIXTURE_OCCURRENCES=4
ACTUAL_AUTHORITY_LEAKAGE_CANDIDATES=0
RELATED_TEST_FUNCTIONS=6
```

Related committed boundary tests include direct checks that Library boundaries
exclude operational ownership and operational records.

Therefore the earlier apparent authority signals are closed as false positives.

## Architectural boundary retained

Library remains owner of semantic/reference/catalog truth.

This closeout does not assign Library ownership of:

- operational order state;
- accounting/payment truth;
- warehouse stock truth;
- pricing/calculation truth;
- production or delivery state.

Those responsibilities remain with their designated modules.

## Candidate disposition

All four actual historical candidates are reconciled against current committed
Library state.

`IMPLEMENTATION_GAP=false`

No new Library implementation task is created from this historical front.

## Safety

This closeout does not:

- run Library tests or Make targets;
- mutate the Library repository;
- edit the shared source map;
- edit the Human Intent ledger;
- mutate roadmap/execution authority;
- touch CF-10.

## Next

Continue `module_current_state_analysis_and_reconciliation` with the next unresolved
historical module front.
```

## Blueprint context

**Path:** `coordination/repository_knowledge/roadmap_enrichment/current_state_reconciliation/forprint_library_reconciliation_20260923_v0_1.yaml`
**SHA256:** `163b241c0eb334af92df32ee2628d0a7abfa970d85980e1f36244dae5a91858c`

```yaml
schema_version: forprint_module_current_state_reconciliation_closeout_v0_1
status: CLOSED
module: forprint_library
reconciliation_subject: library_historical_candidates_and_human_intent_current_state
historical:
  provenance_records:
  - dftb_library_blueprint_standardization_calculator_contract_20260705_reconciliation
  - dftb_library_architecture_genesis_20260516_reconciliation
  actual_candidates:
  - dftb_library_blueprint_standardization_calculator_contract_20260705_governance_candidate
  - dftb_library_blueprint_standardization_calculator_contract_20260705_calculator_candidate
  - dftb_library_architecture_genesis_20260516_admin_candidate
  - dftb_library_architecture_genesis_20260516_contract_lineage_candidate
  human_intents:
  - HI-FP-LIBRARY-STRUCTURE-20260705-001
  - HI-FP-REPORT-DEDUP-20260705-001
  - HI-FP-LIBRARY-ADMIN-20260516-001
  - HI-FP-DATA-CONTRACT-CONSISTENCY-20260516-001
  - HI-FP-CONTRACT-DUAL-FORM-20260516-001
live_module:
  repository: /srv/software_development/forprint-project/forprint_library
  branch: feature/library-calculator-input-contract-v01
  head: bba52bf6001f256a5c13ea7dbe175336b431754c
  upstream: origin/feature/library-calculator-input-contract-v01
  upstream_head: bba52bf6001f256a5c13ea7dbe175336b431754c
  worktree_clean: true
focused_evidence:
  human_intents_verified: 5
  human_intents_focused_current_proof: 5
  human_intents_exact_assertion_review: 0
  human_intents_partial_current: 0
  human_intents_no_focused_evidence: 0
  test_symbols_scanned: 194
  production_symbols_scanned: 287
candidate_mapping:
  governance_candidate:
    candidate_id: dftb_library_blueprint_standardization_calculator_contract_20260705_governance_candidate
    primary_human_intent: HI-FP-REPORT-DEDUP-20260705-001
    secondary_human_intent: HI-FP-LIBRARY-STRUCTURE-20260705-001
  calculator_candidate:
    candidate_id: dftb_library_blueprint_standardization_calculator_contract_20260705_calculator_candidate
    current_contract_context: true
    human_intent_context:
    - HI-FP-LIBRARY-STRUCTURE-20260705-001
    - HI-FP-DATA-CONTRACT-CONSISTENCY-20260516-001
  admin_candidate:
    candidate_id: dftb_library_architecture_genesis_20260516_admin_candidate
    primary_human_intent: HI-FP-LIBRARY-ADMIN-20260516-001
  contract_lineage_candidate:
    candidate_id: dftb_library_architecture_genesis_20260516_contract_lineage_candidate
    primary_human_intent: HI-FP-DATA-CONTRACT-CONSISTENCY-20260516-001
    secondary_human_intent: HI-FP-CONTRACT-DUAL-FORM-20260516-001
authority_review:
  initial_apparent_signals: 4
  negative_validation_or_fixture_occurrences: 4
  actual_authority_leakage_candidates: 0
  final_disposition: AUTHORITY_SIGNALS_ARE_NEGATIVE_VALIDATION_FIXTURES
  phrases:
  - Library owns order state
  - Library owns pricing logic
  - Library owns warehouse stock truth
  - Library owns payment/accounting truth
  related_test_functions: 6
decision:
  disposition: CURRENT_LIBRARY_HISTORICAL_CANDIDATES_CONFIRMED
  actual_candidates_closed: 4
  implementation_gap: false
  new_library_implementation_required: false
  authority_leakage: false
  library_truth_scope: semantic_reference_catalog_truth
  operational_truth_owner: forprint_operations_control_registry
  accounting_truth_owner: forprint_accounting_registry_service
  warehouse_truth_owner: forprint_warehouse_service
  pricing_truth_owner: calculator_engine
  authority_effect: evidence_only_no_execution_activation
safety:
  test_execution_performed: false
  make_execution_performed: false
  live_module_mutated: false
  source_map_mutated: false
  human_intent_ledger_mutated: false
  roadmap_mutated: false
  cf10_touched: false
next:
  work_mode: continue_module_current_state_analysis_and_reconciliation
  forprint_library_front: closed
```

## Blueprint context

**Path:** `coordination/repository_knowledge/roadmap_enrichment/library_historical_source_enrichment_checkpoint_20260922_v0_1.yaml`
**SHA256:** `f8b1013ace56fd388bf3ec7d09b731e68c01ad49eda05e3eace8bac80943a82d`

```yaml
schema_version: forprint_library_historical_source_enrichment_checkpoint_v0_1
status: PASS
module_id: forprint_library
phase: portfolio_knowledge_saturation
closeout_scope: historical_dialogue_roadmap_enrichment
source_groups_processed: 2
primary_source_files_preserved: 2
dftb_source_groups_preserved: 2
human_intents_appended_total: 5
human_intent_semantic_duplicates_skipped_total: 0
source_map_entries_total: 8
open_reconcile_before_implementation_candidates: 4
library_canonical_boundary: REUSE_CURRENT_STRONGER
broad_library_owns_everything: superseded
repository_structure_policy: human_intent_captured
report_dedup_policy: human_intent_captured
library_admin_surface: human_intent_captured_reconcile_candidate
cross_module_data_sufficiency_testing: human_intent_captured
partner_human_machine_contract_forms: human_intent_captured
calculator_input_contract: current_acceptance_unproven_reconcile_candidate
historical_ready_for_blueprint_review: not_acceptance_not_merge
historical_library_contract_registry_role: reconcile_with_current_contract_registry
historical_sync_manager: current_module_not_proven_reconcile_candidate
semantic_id_version_migration_discipline: REUSE_CURRENT
master_memory_preferred: v3.7
canonical_roadmap_mutation: none
execution_authority_mutation: none
lifecycle_mutation: none
commit_push_merge_performed: false
new_canonical_roadmap_step: none
next_module_transition_ready: true
source_groups:
  - source_label: '2026-07-05'
    root: 'coordination/internal_work/blueprint/evening_reviews/2026-07-05_source_label/DFTB_library_blueprint_standardization_calculator_contract_v0_1'
    primary_sha256: 6a24a969300645e5dfe1903013be86e2b062ae3650be212fe7760520e93b9dd6
    dftb_sha256: 85ef5b5e5ca03b66f7071d34a546a7d9bce0fb866cbb0957413c748ad5fa574b
    recovered_human_intents: 2
    reconcile_candidates: 2
  - source_label: '2026-05-16'
    root: 'coordination/internal_work/blueprint/evening_reviews/2026-05-16_source_label/DFTB_library_architecture_genesis_canonical_boundary_v0_1'
    primary_sha256: 1e015dc8792f8d2c0d862d00bcd50bcf4f7d157a141dbaccfc834412c8102542
    dftb_sha256: 5e04c9deae8994939ef4dab5008d0bfcc7649faea1817d26229555a72941b4d9
    recovered_human_intents: 3
    reconcile_candidates: 2
verified_human_intent_ids:
  - 'HI-FP-LIBRARY-STRUCTURE-20260705-001'
  - 'HI-FP-REPORT-DEDUP-20260705-001'
  - 'HI-FP-LIBRARY-ADMIN-20260516-001'
  - 'HI-FP-DATA-CONTRACT-CONSISTENCY-20260516-001'
  - 'HI-FP-CONTRACT-DUAL-FORM-20260516-001'
verified_source_map_ids:
  - 'dftb_library_blueprint_standardization_calculator_contract_20260705'
  - 'dftb_library_blueprint_standardization_calculator_contract_20260705_reconciliation'
  - 'dftb_library_blueprint_standardization_calculator_contract_20260705_governance_candidate'
  - 'dftb_library_blueprint_standardization_calculator_contract_20260705_calculator_candidate'
  - 'dftb_library_architecture_genesis_20260516'
  - 'dftb_library_architecture_genesis_20260516_reconciliation'
  - 'dftb_library_architecture_genesis_20260516_admin_candidate'
  - 'dftb_library_architecture_genesis_20260516_contract_lineage_candidate'
notes:
  - current Library ownership and domain boundaries remain stronger than early broad historical ownership proposals
  - historical Contract Registry and Sync Manager concepts remain bounded reconciliation lineage, not newly created modules
  - Calculator Input Contract history proves proposal and historical implementation work, not current Blueprint acceptance
  - no canonical roadmap or execution authority was mutated by this closeout
```

## Blueprint context

**Path:** `coordination/roadmaps/details/forprint_system_blueprint/portfolio_rebuild_inputs/2026-08-28__forprint_library__first_pass_owner_review_v0_2.md`
**SHA256:** `8d91915947cd5a0a45bde75b377a15ae9ed92fbf45ec5af739b38944a7a9f892`

```markdown
# ForPrint Library — evening first-pass owner review

Module: `forprint_library`

Status: `FIRST_PASS_OWNER_DIRECTION_RECORDED / SYNTHETIC_MICROSTEPS_PENDING_SECOND_PASS`

## AGREED_WITH_OWNER

Library is the canonical semantic/reference layer for long-lived company truth. Any module should
be able to ask "what is the current valid X?" and get an unambiguous answer. X may be a product,
material, alias, dimension/unit, commercial-offer form, agreement/template, internal instruction,
standard, technical reference fact or other versioned reference entity.

Library must retain revision history, effective dates, deprecation, aliases and migration semantics.
It should support historical queries such as "what was current at time T?" and notify/serve dependent
modules when canonical reference truth changes.

## Working boundary

Library is not the canonical owner of physical stock, payments, active order state, CRM interaction
state or production execution. Knowledge Inventory ("what exists in our repos/capabilities") and Library
catalog ("what business/reference truth is canonically valid") are related but distinct systems.

## Synthetic roadmap expansion for pass 2

Everything below is `SYNTHETIC_CANDIDATE` unless explicitly described as owner direction.

### LIB-R0 — Inventory existing Library/reference assets
- inventory models, aliases, templates, importers and consumers
- find duplicate/shadow catalogs in other modules
- classify active, legacy, conflicting and unknown facts
### LIB-R1 — Canonical identity + lifecycle
- stable IDs independent of display names
- revision/effective-from/supersedes metadata
- states such as draft, active, deprecated-supported, retired, forbidden
- alias/synonym/migration graph
### LIB-R2 — Document/template/standard registry
- commercial offers, agreements, forms and reusable templates
- internal instructions/standards
- owner/approval/effective-date metadata
- historical and current resolution
### LIB-R3 — Materials/products/technical references
- canonical product/material/service/operation definitions
- units/dimensions/properties
- technical cards/reference profiles
- external catalog ingestion with provenance
### LIB-R4 — Typed query + discovery
- resolve current by ID
- search when exact ID unknown
- fetch exact historical revision
- explain deprecation/replacement
### LIB-R5 — Change propagation + consumer awareness
- dependency/subscriber map
- typed change/deprecation events
- consumer freshness/version markers
- compatibility for old vs new work
### LIB-R6 — Governance/audit/quality
- approval before canonical promotion
- immutable audit history
- freshness/confidence metadata
- stale-consumer reports
### LIB-R7 — Pilot and migration
- pilot one document, one material alias migration and one instruction
- connect at least two distinct consumers
- test a real change propagation flow
- expand only after evidence is stable

## Dependencies

Primary consumers: Calculator, Telegram, CRM, Operations Assistant, Accounting mappings, Prepress,
Website/catalog and other reference consumers.

## Open questions for pass 2

Library vs Contract Registry; large binary storage vs canonical pointer; push vs polling; approval roles;
exact product-catalog boundary; retention of forbidden/deprecated items.

## Target milestone

Consumers resolve current/historical reference truth without maintaining shadow semantic databases.

## Steady state

Continue measured improvement after the target milestone; the module is not considered permanently finished.
```

## Blueprint context

**Path:** `coordination/roadmaps/details/forprint_system_blueprint/portfolio_rebuild_inputs/2026-08-27__cross_module_boundaries_and_open_questions_v0_1.md`
**SHA256:** `266e530207af1312b9a72b27cb8fe31e0771407243afd1b01f01ed3bd852467d`

```markdown
# Cross-Module Boundaries and Open Questions — Reconciliation Input — 2026-08-27

Status: MIXED — AGREED / PROVISIONAL / OPEN; NOT RUNTIME AUTHORITY.

## Cross-Module Boundaries and Open Questions

### Library as canonical semantic truth — AGREED_WITH_OWNER

Library is expected to hold foundational project truth:
- material/product semantics;
- canonical names;
- configurations;
- technical/reference tables;
- long-lived project rules;
- revision/freshness/deprecation state;
- historical-but-still-contractually-valid facts where needed.

Other modules consume Library rather than invent competing semantic truth.

### Calculator / production queue — AGREED_WITH_OWNER current direction

Keep queue/scheduling inside Calculator for now because ETA depends on it continuously.
Re-evaluate only if scheduling grows into a large independent domain.

### Calculator / Warehouse / Accounting — PROVISIONAL_BOUNDARY

Likely lifecycle:
1. Calculator predicts planned need.
2. Warehouse represents physical availability/movement.
3. Actual consumption becomes a confirmed operational fact.
4. Accounting records the accounting/financial consequence.
5. Deviations feed back into coefficient tuning.

### Blueprint / Inspector / Strategic Control Plane — PROVISIONAL_BOUNDARY

Blueprint = authority and coordination.
Inspector = observation/audit/health/findings.
Strategic Control Plane = decision support only if distinct value is later proven.

### Telegram emergency/admin channel

Concept: `AGREED_WITH_OWNER`
Authority details: `OPEN_QUESTION`

Potential users:
- Blueprint blocked-executor replies;
- Inspector operational diagnostics;
- Calculator temporary coefficient/availability overrides;
- Accounting exception resolution.

Prefer one governed transport/command policy rather than multiple incompatible admin bots.

<!-- cross-module-ui-design-system-boundary-v0-1:start -->

### Shared UI / ForPrint Design System boundary — owner discussion 2026-08-27

`AGREED_WITH_OWNER`: independently developed ForPrint interfaces must converge on one shared
design-system language rather than defining unrelated colors/buttons/warnings/components.

`PROVISIONAL_BOUNDARY`:

- Blueprint owns policy/adoption contract;
- ForPrint Library owns canonical tokens, themes, component catalog/contracts and versioned
  design-system artifacts;
- UI-bearing modules consume/compose these artifacts;
- Inspector observes drift/compliance but does not own design semantics.

Website and Cloud Backup Manager are reference/inventory inputs, not cross-portfolio authority.

Propagation is "single source, controlled rollout": one canonical change feeds generated/versioned
consumer artifacts. Avoid an unversioned runtime blast radius.

<!-- cross-module-ui-design-system-boundary-v0-1:end -->

<!-- website-design-system-migration-guard-v0-2:start -->

### Website migration guard — explicit owner rule — 2026-08-27

The current Website is an existing, already-formed UI product and is a special migration case.

The shared ForPrint Design System **does not authorize an immediate Website redesign**.

Required Website transition sequence:

1. Keep the current Website visual design as the active production baseline.
2. Do not automatically replace existing Website styling/components merely because the shared
   Design System becomes available.
3. A new Website visual variant/theme may enter development only after explicit operator approval
   and a separate Website work package/prompt.
4. Develop the new Website visual variant in parallel with the existing design rather than
   destructively rewriting the active production presentation.
5. Validate the new variant on the Website's local development/test server first.
6. Do not publish the new design to hosting as a side effect of local development, design-system
   publication, Library updates or portfolio adoption.
7. Hosting deployment requires a separate explicit operator decision after local testing/review.
8. During transition, the current and new Website visual variants may coexist where the Website
   architecture permits, so rollback/comparison remains possible.
9. Migration may proceed gradually by components/pages/surfaces rather than as one all-at-once
   visual rewrite.
10. Only after the operator accepts the tested target presentation should the new design become
    the Website production default.

General portfolio rule:

- **newly created UI-bearing tools/modules** should use the canonical Design System from the start
  unless a reviewed exception exists;
- **already existing UI-bearing tools/modules** keep their current working presentation until
  their own explicit migration plan is approved;
- no assistant may infer "shared Design System exists" => "rewrite every existing interface now".

Cloud Backup Manager remains a reusable reference/seed for shared components and layout patterns,
not a command to make Website visually identical to Cloud Backup Manager.

<!-- website-design-system-migration-guard-v0-2:end -->
```

# Part F — Bounded roadmap subsets

## Roadmap subset

**Path:** `tmp/module_knowledge_analysis/forprint_library/02_dictionaries_resolution_profiles/l2_packet/context/blueprint_roadmap_subsets/portfolio_full_horizon_target_states_v0_1__forprint_library_subset.yaml`
**SHA256:** `fc8cfc6352faa31eae7a8892f938858abb5d909833fadfed25761ceaa4f1d62f`

```yaml
schema_version: forprint_l2_blueprint_roadmap_subset_v0_1
module_id: forprint_library
source_file: coordination/roadmaps/details/forprint_system_blueprint/portfolio_full_horizon_target_states_v0_1.yaml
source_sha256: f19182e4af8c4e80edcfd74ce34da499989be46d18b86b856d6d210e4db7973b
selection: recursive exact-key extraction for `forprint_library`
match_count: 1
matches:
- path:
  - modules
  - forprint_library
  value:
    strategic_priority: P0
    role: Canonical semantic/catalog/reference and shared UI publication authority
    target_state:
      agreed_or_recovered:
      - Canonical products/materials/services/operations/aliases/profiles; shared UI package publication.
      - Historical/reference asset semantics use stable asset and revision references; Library may own canonical reference-media
        metadata where applicable, while customer/order/production truth remains with its domain owners.
      - Historical Asset Index entries are projections over authoritative sources; an index/search result never becomes canonical
        asset, order or production truth.
      synthetic_or_proposed:
      - Fast capability/semantic discovery and mature version/adoption lifecycle.
    full_horizon_steps:
    - Reconcile current Library catalog, alias, template, naming-profile and UI publication evidence.
    - Confirm Library ownership of product/material/service/operation semantics and shared UI publication, excluding business
      workflows.
    - Complete capability/self-inventory for canonical IDs, aliases, misspellings, production tokens, templates and technical
      cards.
    - Define versioned naming/profile/default semantics consumed by Calculator, Prepress and operations surfaces.
    - Define material/product/service canonical identifiers and stable lookup contracts for Warehouse and other consumers.
    - 'Define UI design-system package lifecycle: lookup, proposal, prototype, Inspector review, operator approval, publish
      and adoption.'
    - Add version/adoption metadata and compatibility rules without creating live global CSS or uncontrolled defaults.
    - Plan fast capability/semantic discovery while keeping retrieval candidate-only and domain-owner truth authoritative.
    - Define deprecation/migration paths for legacy aliases/profiles and evidence requirements for consumer adoption.
    - Hold broader implementation until Contract Registry and consumer readiness are reconciled in the portfolio.
    - Define stable historical/reference asset metadata semantics including asset ID, source module, entity links, revision
      references, media type and provenance.
    - Define the boundary between Library-owned canonical reference media and customer/order/production assets owned by operational
      domains.
    dependencies_or_inputs:
    - forprint_contract_registry
    human_control_surfaces:
    - DEVELOPER_AUDIT
    - ADMIN_FACING
    inventory_state: OWNER_DIRECTION_CLEAR
    implementation_eligible_now: false
    portfolio_gate: HOLD_UNTIL_PORTFOLIO_READINESS_BASELINE_COMPLETE
    module_value_test: KEEP
```

## Roadmap subset

**Path:** `tmp/module_knowledge_analysis/forprint_library/02_dictionaries_resolution_profiles/l2_packet/context/blueprint_roadmap_subsets/portfolio_module_roadmap_approval_matrix_v0_1__forprint_library_subset.yaml`
**SHA256:** `952ccf44b5208c0e654ad512a3a0ec9b83bb99422bcca5d2ce548e864106d09f`

```yaml
schema_version: forprint_l2_blueprint_roadmap_subset_v0_1
module_id: forprint_library
source_file: coordination/roadmaps/details/forprint_system_blueprint/portfolio_module_roadmap_approval_matrix_v0_1.yaml
source_sha256: 5dd568a26524c8b2186556f79951662081575352d8b412026f88f5c83877736d
selection: recursive exact-key extraction for `forprint_library`
match_count: 2
matches:
- path:
  - modules
  - forprint_library
  value:
    identity_state: CANONICAL
    strategic_priority: P0
    role: Canonical semantic/catalog/reference and shared UI publication authority
    module_value_test: KEEP
    inventory_state: OWNER_DIRECTION_CLEAR
    dependencies_or_inputs: &id001
    - forprint_contract_registry
    owns:
    - product_catalog_semantics
    - service_catalog_semantics
    - material_catalog_semantics
    - operation_catalog_semantics
    - aliases
    - templates
    - technical_cards
    - contract_definitions
    - ui_design_system_publication
    - shared_ui_component_catalog
    - ui_component_version_and_adoption_metadata
    must_not_own:
    - operational_orders
    - client_database
    - accounting_truth
    - production_runtime
    - crm_workflow
    - domain_business_rules_outside_library_semantics
    target_state:
      agreed_or_recovered:
      - Canonical products/materials/services/operations/aliases/profiles; shared UI package publication.
      synthetic_or_proposed:
      - Fast capability/semantic discovery and mature version/adoption lifecycle.
    roadmap_status: PLANNING_ONLY_NOT_DISTRIBUTED
    steps:
    - sequence: 1
      step_id: FORPRINT_LIBRARY-H01
      title: Reconcile current Library catalog, alias, template, naming-profile and UI publication evidence.
      approval_state: AGREED_PLANNING_DIRECTION
      source_basis: current_evidence_reconciliation
      execution_authority: false
      dependency_gate: []
    - sequence: 2
      step_id: FORPRINT_LIBRARY-H02
      title: Confirm Library ownership of product/material/service/operation semantics and shared UI publication, excluding
        business workflows.
      approval_state: AGREED_PLANNING_DIRECTION
      source_basis: ownership_and_role_boundary
      execution_authority: false
      dependency_gate: []
    - sequence: 3
      step_id: FORPRINT_LIBRARY-H03
      title: Complete capability/self-inventory for canonical IDs, aliases, misspellings, production tokens, templates and
        technical cards.
      approval_state: AGREED_PLANNING_DIRECTION
      source_basis: self_inventory_requirement
      execution_authority: false
      dependency_gate: []
    - sequence: 4
      step_id: FORPRINT_LIBRARY-H04
      title: Define versioned naming/profile/default semantics consumed by Calculator, Prepress and operations surfaces.
      approval_state: AGREED_PLANNING_DIRECTION
      source_basis: dependency_and_contract_planning
      execution_authority: false
      dependency_gate: *id001
    - sequence: 5
      step_id: FORPRINT_LIBRARY-H05
      title: Define material/product/service canonical identifiers and stable lookup contracts for Warehouse and other consumers.
      approval_state: AGREED_OR_RECOVERED_TARGET
      source_basis: agreed_or_recovered_target_state
      execution_authority: false
      dependency_gate: []
    - sequence: 6
      step_id: FORPRINT_LIBRARY-H06
      title: 'Define UI design-system package lifecycle: lookup, proposal, prototype, Inspector review, operator approval,
        publish and adoption.'
      approval_state: AGREED_OR_RECOVERED_TARGET
      source_basis: agreed_or_recovered_target_state
      execution_authority: false
      dependency_gate: []
    - sequence: 7
      step_id: FORPRINT_LIBRARY-H07
      title: Add version/adoption metadata and compatibility rules without creating live global CSS or uncontrolled defaults.
      approval_state: AGREED_OR_RECOVERED_TARGET
      source_basis: agreed_or_recovered_target_state
      execution_authority: false
      dependency_gate: []
    - sequence: 8
      step_id: FORPRINT_LIBRARY-H08
      title: Plan fast capability/semantic discovery while keeping retrieval candidate-only and domain-owner truth authoritative.
      approval_state: PROPOSED_TARGET_REFINEMENT
      source_basis: proposed_mature_target
      execution_authority: false
      dependency_gate: []
    - sequence: 9
      step_id: FORPRINT_LIBRARY-H09
      title: Define deprecation/migration paths for legacy aliases/profiles and evidence requirements for consumer adoption.
      approval_state: PROPOSED_TARGET_REFINEMENT
      source_basis: proposed_mature_target
      execution_authority: false
      dependency_gate: []
    - sequence: 10
      step_id: FORPRINT_LIBRARY-H10
      title: Hold broader implementation until Contract Registry and consumer readiness are reconciled in the portfolio.
      approval_state: HOLD_FOR_FINAL_PORTFOLIO_APPROVAL
      source_basis: operator_distribution_gate
      execution_authority: false
      dependency_gate: *id001
    - sequence: 11
      step_id: FORPRINT_LIBRARY-H11
      title: Define stable historical/reference asset metadata semantics including asset ID, source module, entity links,
        revision references, media type and provenance.
      approval_state: AGREED_PLANNING_DIRECTION
      source_basis: operator_confirmed_evening_architecture_20260919
      execution_authority: false
      dependency_gate: []
    - sequence: 12
      step_id: FORPRINT_LIBRARY-H12
      title: Define the boundary between Library-owned canonical reference media and customer/order/production assets owned
        by operational domains.
      approval_state: AGREED_PLANNING_DIRECTION
      source_basis: operator_confirmed_evening_architecture_20260919
      execution_authority: false
      dependency_gate: []
- path:
  - project_cleanliness_conformance
  - modules
  - forprint_library
  value:
    status: REQUIRED_PLANNED_MODULE_LOCAL_PACK
    policy_ref: coordination/standards/governance/project_cleanliness_and_machine_surface_normalization_standard_v0_1.md
    local_repository_owner_responsible: true
    parallel_global_standard_allowed: false
    assistant_distribution_authorized: false
    implementation_authorized: false
    next_action: record local cleanliness inventory/check roadmap before future assistant distribution
```

# Part G — Packet provenance

Evidence/provenance items recorded: **52**

See `l2_packet/packet_manifest.yaml` for the machine-readable ledger.
