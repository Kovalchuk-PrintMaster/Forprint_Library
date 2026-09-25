# ForPrint Library — L2 Block 01 Analysis Packet

**Module:** `forprint_library`
**Block:** `01_domain_semantics_catalog`

This packet is evidence for analysis only. It is not implementation authority.

## Evidence boundaries

- Primary implementation population comes from the human-reviewed L1 block manifest.
- Related tests are selected only from L1 inventory secondary relationships.
- Blueprint material is authority/planning/provenance context and is not mixed into implementation truth.
- Historical material remains provenance unless current evidence promotes it later.

# Part A — Block manifest

## L1 block manifest

**Path:** `tmp/module_knowledge_analysis/forprint_library/01_domain_semantics_catalog/manifest.yaml`
**SHA256:** `725392a3c8b7591e2257a6aad0fde48fca60c20b1df2317688077de8bfc7b995`

```yaml
schema_version: forprint_module_knowledge_analysis_block_manifest_v0_1
module_id: forprint_library
stage: L1_INVENTORY_AND_SEGMENTATION
block_id: 01_domain_semantics_catalog
title: Domain semantics and catalog
purpose: Products, services, materials, operations, print modes, finishing options, configurable-product semantics, canonical
  IDs and aliases.
mutation_performed: false
selection_method: L1 deterministic classification plus bounded human review correction v0.1; classification remains preliminary
  until L2 analysis
file_count: 20
source_paths:
- app/forprint_library/catalog/__init__.py
- app/forprint_library/catalog/loader.py
- app/forprint_library/catalog/models.py
- app/forprint_library/catalog/validation.py
- catalog/configurable_products/business_card.yaml
- catalog/finishing_options.yaml
- catalog/materials.yaml
- catalog/operations.yaml
- catalog/print_modes.yaml
- catalog/product_families.yaml
- catalog/seeds/catalog_seed_v0_1.yaml
- schemas/catalog_seed.schema.yaml
- schemas/configurable_product.schema.yaml
- schemas/finishing_option.schema.yaml
- schemas/material.schema.yaml
- schemas/operation.schema.yaml
- schemas/print_mode.schema.yaml
- schemas/product_family.schema.yaml
- scripts/coordination/export_coordination_foundation_alignment_closure.py
- scripts/coordination/validate_coordination_foundation_alignment.py
primary_capability_hypotheses:
- canonical catalog semantics
- product/material/operation reference definitions
- configurable product semantics
cross_block_dependencies:
- block_id: 05_validation_tests_quality
  linked_file_count: 1
documents_present: []
tests_present: []
generated_outputs_present: []
legacy_candidates_present: []
unknowns: []
confidence: medium
```

# Part B — Primary source population

## Primary source

**Path:** `app/forprint_library/catalog/__init__.py`
**SHA256:** `ca347ed6d310e838663faa28ac1f9eb765b07dc6e14f9244362be17b911d1309`

```python
from __future__ import annotations

from forprint_library.catalog.loader import load_all_component_catalogs, load_seed
from forprint_library.catalog.registry import CatalogRegistry
from forprint_library.catalog.validation import validate_catalog_seed

__all__ = [
    "CatalogRegistry",
    "load_all_component_catalogs",
    "load_seed",
    "validate_catalog_seed",
]
```

## Primary source

**Path:** `app/forprint_library/catalog/loader.py`
**SHA256:** `b9061c8d5077e2ef9b90abce58cbf3bf2e418740aa4e17fb158111161233f303`

```python
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from forprint_library.catalog.models import COMPONENT_CATALOG_FILES

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_SEED_PATH = PROJECT_ROOT / "catalog" / "seeds" / "catalog_seed_v0_1.yaml"


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML file must contain a mapping: {path}")

    return data


def load_seed(path: Path | None = None) -> dict[str, Any]:
    return load_yaml(path or DEFAULT_SEED_PATH)


def load_component_catalog(section: str, project_root: Path | None = None) -> dict[str, Any]:
    root = project_root or PROJECT_ROOT
    relative_path = COMPONENT_CATALOG_FILES[section]
    return load_yaml(root / relative_path)


def load_all_component_catalogs(project_root: Path | None = None) -> dict[str, dict[str, Any]]:
    return {
        section: load_component_catalog(section, project_root=project_root)
        for section in COMPONENT_CATALOG_FILES
    }
```

## Primary source

**Path:** `app/forprint_library/catalog/models.py`
**SHA256:** `7666d3323eeb34575fe6135518453c9fc9193c8e09b25b06b7da86f16cbee2b1`

```python
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
```

## Primary source

**Path:** `app/forprint_library/catalog/validation.py`
**SHA256:** `15a9659a4773301d2eb6a54e1663a6d990b5c4ad9aec3b01327722650b121710`

```python
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
```

## Primary source

**Path:** `catalog/configurable_products/business_card.yaml`
**SHA256:** `461ec437136b09218c3c9e1dfce9ca7a8bb4582600736a5fabae128d5e0de912`

```yaml
schema_version: configurable_product_card_v0_1
product_id: product.business_card
kind: configurable_product
status: draft_reference
version: "0.1"
owner_module: forprint_library
names:
  uk: Візитки
  en: Business cards
aliases:
  - візитки
  - візитка
  - business cards
  - business card
compatibility_aliases:
  - product:business_cards
product_family_ref:
  catalog: product_families
  id: business_card
  label: Візитка
description:
  uk: Контрольна configurable product card для друкованих візиток.
  en: Controlled configurable product card for printed business cards.
constructor_parameters:
  - key: size
    label:
      uk: Розмір
      en: Size
    type: choice
    required: true
    library_owned: true
    allowed_values:
      - id: size_90x50_mm
        label: 90x50 mm
        width_mm: 90
        height_mm: 50
      - id: size_85x55_mm
        label: 85x55 mm
        width_mm: 85
        height_mm: 55
  - key: sides
    label:
      uk: Сторони друку
      en: Printed sides
    type: choice
    required: true
    library_owned: true
    allowed_values:
      - id: one_sided
        label: 4+0
        print_mode_ref:
          catalog: print_modes
          id: color_4_0
      - id: two_sided
        label: 4+4
        print_mode_ref:
          catalog: print_modes
          id: color_4_4
  - key: material_ref
    label:
      uk: Матеріал
      en: Material
    type: reference_choice
    required: true
    library_owned: true
    reference_catalog: materials
    allowed_refs:
      - catalog: materials
        id: paper_300g_matte
      - catalog: materials
        id: paper_350g_gloss
  - key: print_mode_ref
    label:
      uk: Режим друку
      en: Print mode
    type: reference_choice
    required: true
    library_owned: true
    reference_catalog: print_modes
    allowed_refs:
      - catalog: print_modes
        id: color_4_0
      - catalog: print_modes
        id: color_4_4
  - key: quantity
    label:
      uk: Кількість
      en: Quantity
    type: numeric_input_context
    required: true
    consumer_owned_value: true
    minimum: 1
    example_values:
      - 100
      - 500
      - 1000
    notes: Quantity is input context only. Library does not calculate price.
  - key: finishing_refs
    label:
      uk: Постобробка
      en: Finishing
    type: reference_list
    required: false
    library_owned: true
    reference_catalog: finishing_options
    allowed_refs:
      - catalog: finishing_options
        id: none
      - catalog: finishing_options
        id: matte_lamination
      - catalog: finishing_options
        id: gloss_lamination
      - catalog: finishing_options
        id: corner_rounding
  - key: artwork_source
    label:
      uk: Джерело макета
      en: Artwork source
    type: choice
    required: false
    consumer_owned_value: true
    allowed_values:
      - id: customer_print_ready_file
        label: Customer provides print-ready file
      - id: customer_needs_design
        label: Customer needs design
      - id: customer_needs_prepress_check
        label: Customer needs prepress check
consumer_usage_notes:
  telegram_bot:
    allowed_use: May use product.business_card and aliases as route hints only.
    forbidden_use: Must not treat this card as Telegram runtime behavior.
  calculator_engine:
    allowed_use: May later use constructor parameters as pricing input context.
    forbidden_use: No formula or final price is implemented in Library.
  forprint_operational_registry:
    allowed_use: May store product.business_card as foreign-domain metadata.
    forbidden_use: Library does not create orders or operational records.
boundary_notes:
  library_owned:
    - product_id
    - names
    - aliases
    - product_family_ref
    - constructor parameter definitions
    - references to Library catalog IDs
  consumer_owned:
    - selected parameter values
    - channel routing context
    - pricing input context
    - operational foreign metadata
  explicit_non_goals:
    - No full product catalog
    - No product modeling UI
    - No production catalog database
    - No live API
    - No 1C import
    - No 1C synchronization
    - No Calculator integration
    - No Telegram Bot integration
    - No Operational Registry write
    - No CRM write
    - No Website write
    - No price calculation
    - No final price formula
    - No material write-off logic
    - No warehouse stock truth
    - No production task creation
    - No real client or order data
    - No production runtime
```

## Primary source

**Path:** `catalog/finishing_options.yaml`
**SHA256:** `85b6dd494d15f87bd7271204eddcb15d21211c0c0cdc83723f19749985f13736`

```yaml
catalog_type: finishing_options
metadata:
  id: canonical_catalog_seed_v0_1
  name: Canonical Catalog Seed v0.1
  version: '0.1'
  catalog_status: draft_canonical_seed
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  notes: 'Draft canonical seed for projection use by dependent ForPrint modules. This
    is not a final production contract.

    '
items:
- id: none
  name_uk: Без постобробки
  name_en: No finishing
  aliases:
  - без постобробки
  - no finishing
  - без додаткової обробки
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft finishing option entry.
- id: matte_lamination
  name_uk: Матова ламінація
  name_en: Matte lamination
  aliases:
  - матова ламінація
  - matte lamination
  - матове ламінування
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft finishing option entry.
- id: gloss_lamination
  name_uk: Глянцева ламінація
  name_en: Gloss lamination
  aliases:
  - глянцева ламінація
  - gloss lamination
  - глянцеве ламінування
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft finishing option entry.
- id: corner_rounding
  name_uk: Заокруглення кутів як опція
  name_en: Corner rounding finish
  aliases:
  - заокруглені кути
  - corner rounding finish
  - круглі кути
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft finishing option entry.
- id: finishing_folding
  name_uk: Фальцювання як опція
  name_en: Folding finish
  aliases:
  - фальцювання як опція
  - folding finish
  - згин як постобробка
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft finishing option entry.
```

## Primary source

**Path:** `catalog/materials.yaml`
**SHA256:** `8d113c1b375965bfbb2efef3de9c4dce45b867d31cb1d8cf33d56feb903215ad`

```yaml
catalog_type: materials
metadata:
  id: canonical_catalog_seed_v0_1
  name: Canonical Catalog Seed v0.1
  version: '0.1'
  catalog_status: draft_canonical_seed
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  notes: 'Draft canonical seed for projection use by dependent ForPrint modules. This
    is not a final production contract.

    '
items:
- id: paper_300g_matte
  name_uk: Папір 300 г матовий
  name_en: 300 gsm matte paper
  aliases:
  - папір 300 мат
  - 300gsm matte
  - матовий папір 300 г
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Synthetic draft material entry.
- id: paper_350g_gloss
  name_uk: Папір 350 г глянцевий
  name_en: 350 gsm gloss paper
  aliases:
  - папір 350 глянц
  - 350gsm gloss
  - мелований 350 г
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Synthetic draft material entry.
- id: paper_130g_matte
  name_uk: Папір 130 г матовий
  name_en: 130 gsm matte paper
  aliases:
  - папір 130 мат
  - 130gsm matte
  - матовий папір 130 г
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Synthetic draft material entry.
- id: banner_440g
  name_uk: Банер 440 г
  name_en: 440 gsm banner material
  aliases:
  - банер 440
  - 440gsm banner
  - банерна тканина 440 г
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Synthetic draft material entry.
- id: pvc_3mm
  name_uk: ПВХ 3 мм
  name_en: 3 mm PVC sheet
  aliases:
  - пвх 3мм
  - pvc 3mm
  - пластик пвх 3 мм
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Synthetic draft material entry.
- id: self_adhesive_vinyl
  name_uk: Самоклеюча вінілова плівка
  name_en: Self-adhesive vinyl
  aliases:
  - самоклейка вініл
  - self adhesive vinyl
  - вінілова плівка з клеєм
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Synthetic draft material entry.
```

## Primary source

**Path:** `catalog/operations.yaml`
**SHA256:** `8fdeccc5de0742ce02d5191eab27f4b855628b8c5a50a5794c5e8c213d843cd5`

```yaml
catalog_type: operations
metadata:
  id: canonical_catalog_seed_v0_1
  name: Canonical Catalog Seed v0.1
  version: '0.1'
  catalog_status: draft_canonical_seed
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  notes: 'Draft canonical seed for projection use by dependent ForPrint modules. This
    is not a final production contract.

    '
items:
- id: digital_print
  name_uk: Цифровий друк
  name_en: Digital print
  aliases:
  - цифровий друк
  - digital print
  - друк цифровий
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft operation entry.
- id: large_format_print
  name_uk: Широкоформатний друк
  name_en: Large-format print
  aliases:
  - широкоформатний друк
  - large format print
  - друк на банері
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft operation entry.
- id: cutting
  name_uk: Різання
  name_en: Cutting
  aliases:
  - різання
  - cutting
  - порізка
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft operation entry.
- id: lamination
  name_uk: Ламінування
  name_en: Lamination
  aliases:
  - ламінування
  - lamination
  - покриття плівкою
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft operation entry.
- id: rounding
  name_uk: Заокруглення кутів
  name_en: Corner rounding
  aliases:
  - заокруглення кутів
  - corner rounding
  - округлення кутів
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft operation entry.
- id: folding
  name_uk: Фальцювання
  name_en: Folding
  aliases:
  - фальцювання
  - folding operation
  - згинання продукції
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft operation entry.
- id: scoring
  name_uk: Бігування
  name_en: Scoring
  aliases:
  - бігування
  - scoring
  - лінія згину
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft operation entry.
```

## Primary source

**Path:** `catalog/print_modes.yaml`
**SHA256:** `4a0e5466a206a117ab0d094eb8fbb719302a6955410d4536066d25fc271f757e`

```yaml
catalog_type: print_modes
metadata:
  id: canonical_catalog_seed_v0_1
  name: Canonical Catalog Seed v0.1
  version: '0.1'
  catalog_status: draft_canonical_seed
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  notes: 'Draft canonical seed for projection use by dependent ForPrint modules. This
    is not a final production contract.

    '
items:
- id: color_4_0
  name_uk: 4+0
  name_en: Full color one side
  aliases:
  - 4+0
  - односторонній повноколір
  - full color one side
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft print mode entry.
- id: color_4_4
  name_uk: 4+4
  name_en: Full color both sides
  aliases:
  - 4+4
  - двосторонній повноколір
  - full color both sides
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft print mode entry.
- id: color_1_0
  name_uk: 1+0
  name_en: One color one side
  aliases:
  - 1+0
  - односторонній один колір
  - one color one side
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft print mode entry.
- id: color_1_1
  name_uk: 1+1
  name_en: One color both sides
  aliases:
  - 1+1
  - двосторонній один колір
  - one color both sides
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft print mode entry.
```

## Primary source

**Path:** `catalog/product_families.yaml`
**SHA256:** `525b3c1ab5b7446dce72484078970b27e737ad533cb1a9c55eb681a78bd6a85e`

```yaml
catalog_type: product_families
metadata:
  id: canonical_catalog_seed_v0_1
  name: Canonical Catalog Seed v0.1
  version: '0.1'
  catalog_status: draft_canonical_seed
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  notes: 'Draft canonical seed for projection use by dependent ForPrint modules. This
    is not a final production contract.

    '
items:
- id: business_card
  name_uk: Візитка
  name_en: Business card
  aliases:
  - візитка
  - business card
  - карточка
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft product family for small-format contact cards.
- id: flyer
  name_uk: Флаєр
  name_en: Flyer
  aliases:
  - флаєр
  - flyer
  - рекламна листівка
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft product family for simple promotional leaflets.
- id: leaflet
  name_uk: Буклет
  name_en: Leaflet
  aliases:
  - буклет
  - leaflet
  - складна листівка
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft product family for folded informational products.
- id: poster
  name_uk: Плакат
  name_en: Poster
  aliases:
  - плакат
  - poster
  - афіша
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft product family for posters and display prints.
- id: banner
  name_uk: Банер
  name_en: Banner
  aliases:
  - банер
  - banner
  - банерна продукція
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft product family for large-format banners.
- id: sticker
  name_uk: Наліпка
  name_en: Sticker
  aliases:
  - наліпка
  - sticker
  - стікер
  status: draft
  version: '0.1'
  owner_module: forprint_library
  schema_status: unstable_v0_1
  notes: Draft product family for adhesive labels and stickers.
```

## Primary source

**Path:** `catalog/seeds/catalog_seed_v0_1.yaml`
**SHA256:** `25654e306bacaee4c5350b83f9343a000075c1a242e8f02b7984ed6c3c019da7`

```yaml
metadata:
  id: canonical_catalog_seed_v0_1
  name: Canonical Catalog Seed v0.1
  version: "0.1"
  catalog_status: draft_canonical_seed
  schema_status: unstable_v0_1
  usage: allowed_for_projection_use
  contract_status: not_final_contract
  owner_module: forprint_library
  notes: >
    Draft canonical seed for projection use by dependent ForPrint modules.
    This is not a final production contract.

materials:
  - id: paper_300g_matte
    name_uk: Папір 300 г матовий
    name_en: 300 gsm matte paper
    aliases:
      - папір 300 мат
      - 300gsm matte
      - матовий папір 300 г
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Synthetic draft material entry.

  - id: paper_350g_gloss
    name_uk: Папір 350 г глянцевий
    name_en: 350 gsm gloss paper
    aliases:
      - папір 350 глянц
      - 350gsm gloss
      - мелований 350 г
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Synthetic draft material entry.

  - id: paper_130g_matte
    name_uk: Папір 130 г матовий
    name_en: 130 gsm matte paper
    aliases:
      - папір 130 мат
      - 130gsm matte
      - матовий папір 130 г
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Synthetic draft material entry.

  - id: banner_440g
    name_uk: Банер 440 г
    name_en: 440 gsm banner material
    aliases:
      - банер 440
      - 440gsm banner
      - банерна тканина 440 г
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Synthetic draft material entry.

  - id: pvc_3mm
    name_uk: ПВХ 3 мм
    name_en: 3 mm PVC sheet
    aliases:
      - пвх 3мм
      - pvc 3mm
      - пластик пвх 3 мм
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Synthetic draft material entry.

  - id: self_adhesive_vinyl
    name_uk: Самоклеюча вінілова плівка
    name_en: Self-adhesive vinyl
    aliases:
      - самоклейка вініл
      - self adhesive vinyl
      - вінілова плівка з клеєм
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Synthetic draft material entry.

product_families:
  - id: business_card
    name_uk: Візитка
    name_en: Business card
    aliases:
      - візитка
      - business card
      - карточка
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft product family for small-format contact cards.

  - id: flyer
    name_uk: Флаєр
    name_en: Flyer
    aliases:
      - флаєр
      - flyer
      - рекламна листівка
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft product family for simple promotional leaflets.

  - id: leaflet
    name_uk: Буклет
    name_en: Leaflet
    aliases:
      - буклет
      - leaflet
      - складна листівка
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft product family for folded informational products.

  - id: poster
    name_uk: Плакат
    name_en: Poster
    aliases:
      - плакат
      - poster
      - афіша
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft product family for posters and display prints.

  - id: banner
    name_uk: Банер
    name_en: Banner
    aliases:
      - банер
      - banner
      - банерна продукція
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft product family for large-format banners.

  - id: sticker
    name_uk: Наліпка
    name_en: Sticker
    aliases:
      - наліпка
      - sticker
      - стікер
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft product family for adhesive labels and stickers.

operations:
  - id: digital_print
    name_uk: Цифровий друк
    name_en: Digital print
    aliases:
      - цифровий друк
      - digital print
      - друк цифровий
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft operation entry.

  - id: large_format_print
    name_uk: Широкоформатний друк
    name_en: Large-format print
    aliases:
      - широкоформатний друк
      - large format print
      - друк на банері
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft operation entry.

  - id: cutting
    name_uk: Різання
    name_en: Cutting
    aliases:
      - різання
      - cutting
      - порізка
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft operation entry.

  - id: lamination
    name_uk: Ламінування
    name_en: Lamination
    aliases:
      - ламінування
      - lamination
      - покриття плівкою
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft operation entry.

  - id: rounding
    name_uk: Заокруглення кутів
    name_en: Corner rounding
    aliases:
      - заокруглення кутів
      - corner rounding
      - округлення кутів
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft operation entry.

  - id: folding
    name_uk: Фальцювання
    name_en: Folding
    aliases:
      - фальцювання
      - folding operation
      - згинання продукції
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft operation entry.

  - id: scoring
    name_uk: Бігування
    name_en: Scoring
    aliases:
      - бігування
      - scoring
      - лінія згину
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft operation entry.

print_modes:
  - id: color_4_0
    name_uk: 4+0
    name_en: Full color one side
    aliases:
      - 4+0
      - односторонній повноколір
      - full color one side
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft print mode entry.

  - id: color_4_4
    name_uk: 4+4
    name_en: Full color both sides
    aliases:
      - 4+4
      - двосторонній повноколір
      - full color both sides
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft print mode entry.

  - id: color_1_0
    name_uk: 1+0
    name_en: One color one side
    aliases:
      - 1+0
      - односторонній один колір
      - one color one side
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft print mode entry.

  - id: color_1_1
    name_uk: 1+1
    name_en: One color both sides
    aliases:
      - 1+1
      - двосторонній один колір
      - one color both sides
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft print mode entry.

finishing_options:
  - id: none
    name_uk: Без постобробки
    name_en: No finishing
    aliases:
      - без постобробки
      - no finishing
      - без додаткової обробки
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft finishing option entry.

  - id: matte_lamination
    name_uk: Матова ламінація
    name_en: Matte lamination
    aliases:
      - матова ламінація
      - matte lamination
      - матове ламінування
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft finishing option entry.

  - id: gloss_lamination
    name_uk: Глянцева ламінація
    name_en: Gloss lamination
    aliases:
      - глянцева ламінація
      - gloss lamination
      - глянцеве ламінування
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft finishing option entry.

  - id: corner_rounding
    name_uk: Заокруглення кутів як опція
    name_en: Corner rounding finish
    aliases:
      - заокруглені кути
      - corner rounding finish
      - круглі кути
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft finishing option entry.

  - id: finishing_folding
    name_uk: Фальцювання як опція
    name_en: Folding finish
    aliases:
      - фальцювання як опція
      - folding finish
      - згин як постобробка
    status: draft
    version: "0.1"
    owner_module: forprint_library
    schema_status: unstable_v0_1
    notes: Draft finishing option entry.
```

## Primary source

**Path:** `schemas/catalog_seed.schema.yaml`
**SHA256:** `7369da57d72df233a1432ba86ba68c72a40ca1a89e0f4b6fb7e5f766a7a0acdb`

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: ForPrint Catalog Seed
type: object
required:
- metadata
- materials
- product_families
- operations
- print_modes
- finishing_options
properties:
  metadata:
    type: object
    required:
    - id
    - version
    - catalog_status
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
        type: string
      catalog_status:
        const: draft_canonical_seed
      schema_status:
        const: unstable_v0_1
      usage:
        const: allowed_for_projection_use
      contract_status:
        const: not_final_contract
      owner_module:
        const: forprint_library
      notes:
        type: string
    additionalProperties: true
  materials:
    type: array
    minItems: 1
    items:
      $ref: '#/$defs/catalog_item'
  product_families:
    type: array
    minItems: 1
    items:
      $ref: '#/$defs/catalog_item'
  operations:
    type: array
    minItems: 1
    items:
      $ref: '#/$defs/catalog_item'
  print_modes:
    type: array
    minItems: 1
    items:
      $ref: '#/$defs/catalog_item'
  finishing_options:
    type: array
    minItems: 1
    items:
      $ref: '#/$defs/catalog_item'
additionalProperties: false
$defs:
  catalog_item:
    type: object
    required:
    - id
    - name_uk
    - name_en
    - aliases
    - status
    - version
    - owner_module
    - schema_status
    - notes
    properties:
      id:
        type: string
        pattern: ^[a-z0-9_]+$
      name_uk:
        type: string
        minLength: 1
      name_en:
        type: string
        minLength: 1
      aliases:
        type: array
        minItems: 1
        items:
          type: string
          minLength: 1
      status:
        enum:
        - draft
        - active
        - deprecated
        - experimental
      version:
        type: string
      owner_module:
        const: forprint_library
      schema_status:
        const: unstable_v0_1
      notes:
        type: string
    additionalProperties: true
```

## Primary source

**Path:** `schemas/configurable_product.schema.yaml`
**SHA256:** `ba6c6941e13f047a6d7b198b0c8164a366ad180c615b1b7e0540014229b41ddc`

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: ForPrint Configurable Product Card
type: object
required:
  - schema_version
  - product_id
  - kind
  - status
  - version
  - owner_module
  - names
  - aliases
  - constructor_parameters
  - consumer_usage_notes
  - boundary_notes
properties:
  schema_version:
    const: configurable_product_card_v0_1
  product_id:
    type: string
    pattern: ^product\.[a-z0-9_]+$
  kind:
    const: configurable_product
  status:
    enum:
      - draft_reference
      - active_reference
      - deprecated_reference
  version:
    type: string
  owner_module:
    const: forprint_library
  names:
    type: object
    required:
      - uk
      - en
    properties:
      uk:
        type: string
        minLength: 1
      en:
        type: string
        minLength: 1
    additionalProperties: true
  aliases:
    type: array
    minItems: 1
    items:
      type: string
      minLength: 1
  compatibility_aliases:
    type: array
    items:
      type: string
      minLength: 1
  product_family_ref:
    type: object
    required:
      - catalog
      - id
    properties:
      catalog:
        const: product_families
      id:
        type: string
    additionalProperties: true
  constructor_parameters:
    type: array
    minItems: 1
    items:
      type: object
      required:
        - key
        - type
        - required
      properties:
        key:
          type: string
          pattern: ^[a-z0-9_]+$
        type:
          type: string
        required:
          type: boolean
      additionalProperties: true
  consumer_usage_notes:
    type: object
    additionalProperties: true
  boundary_notes:
    type: object
    additionalProperties: true
additionalProperties: true
```

## Primary source

**Path:** `schemas/finishing_option.schema.yaml`
**SHA256:** `ad22428258457bd45347fe97ce8b0a7665ed5c5798619c81558f948012a00505`

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: ForPrint Finishing Option Catalog
type: object
required:
- catalog_type
- metadata
- items
properties:
  catalog_type:
    const: finishing_options
  metadata:
    type: object
    required:
    - id
    - version
    - catalog_status
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
        type: string
      catalog_status:
        const: draft_canonical_seed
      schema_status:
        const: unstable_v0_1
      usage:
        const: allowed_for_projection_use
      contract_status:
        const: not_final_contract
      owner_module:
        const: forprint_library
      notes:
        type: string
    additionalProperties: true
  items:
    type: array
    minItems: 1
    items:
      type: object
      required:
      - id
      - name_uk
      - name_en
      - aliases
      - status
      - version
      - owner_module
      - schema_status
      - notes
      properties:
        id:
          type: string
          pattern: ^[a-z0-9_]+$
        name_uk:
          type: string
          minLength: 1
        name_en:
          type: string
          minLength: 1
        aliases:
          type: array
          minItems: 1
          items:
            type: string
            minLength: 1
        status:
          enum:
          - draft
          - active
          - deprecated
          - experimental
        version:
          type: string
        owner_module:
          const: forprint_library
        schema_status:
          const: unstable_v0_1
        notes:
          type: string
      additionalProperties: true
additionalProperties: false
```

## Primary source

**Path:** `schemas/material.schema.yaml`
**SHA256:** `f363b1a32fe60f275282427068444576a024a6dc519265e44f8a1ca74526486e`

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: ForPrint Material Catalog
type: object
required:
- catalog_type
- metadata
- items
properties:
  catalog_type:
    const: materials
  metadata:
    type: object
    required:
    - id
    - version
    - catalog_status
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
        type: string
      catalog_status:
        const: draft_canonical_seed
      schema_status:
        const: unstable_v0_1
      usage:
        const: allowed_for_projection_use
      contract_status:
        const: not_final_contract
      owner_module:
        const: forprint_library
      notes:
        type: string
    additionalProperties: true
  items:
    type: array
    minItems: 1
    items:
      type: object
      required:
      - id
      - name_uk
      - name_en
      - aliases
      - status
      - version
      - owner_module
      - schema_status
      - notes
      properties:
        id:
          type: string
          pattern: ^[a-z0-9_]+$
        name_uk:
          type: string
          minLength: 1
        name_en:
          type: string
          minLength: 1
        aliases:
          type: array
          minItems: 1
          items:
            type: string
            minLength: 1
        status:
          enum:
          - draft
          - active
          - deprecated
          - experimental
        version:
          type: string
        owner_module:
          const: forprint_library
        schema_status:
          const: unstable_v0_1
        notes:
          type: string
      additionalProperties: true
additionalProperties: false
```

## Primary source

**Path:** `schemas/operation.schema.yaml`
**SHA256:** `b6b7f80b7fbfb016d6599502b1bc39aa2311b6bb701ced1f3194bbe53b9c288d`

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: ForPrint Operation Catalog
type: object
required:
- catalog_type
- metadata
- items
properties:
  catalog_type:
    const: operations
  metadata:
    type: object
    required:
    - id
    - version
    - catalog_status
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
        type: string
      catalog_status:
        const: draft_canonical_seed
      schema_status:
        const: unstable_v0_1
      usage:
        const: allowed_for_projection_use
      contract_status:
        const: not_final_contract
      owner_module:
        const: forprint_library
      notes:
        type: string
    additionalProperties: true
  items:
    type: array
    minItems: 1
    items:
      type: object
      required:
      - id
      - name_uk
      - name_en
      - aliases
      - status
      - version
      - owner_module
      - schema_status
      - notes
      properties:
        id:
          type: string
          pattern: ^[a-z0-9_]+$
        name_uk:
          type: string
          minLength: 1
        name_en:
          type: string
          minLength: 1
        aliases:
          type: array
          minItems: 1
          items:
            type: string
            minLength: 1
        status:
          enum:
          - draft
          - active
          - deprecated
          - experimental
        version:
          type: string
        owner_module:
          const: forprint_library
        schema_status:
          const: unstable_v0_1
        notes:
          type: string
      additionalProperties: true
additionalProperties: false
```

## Primary source

**Path:** `schemas/print_mode.schema.yaml`
**SHA256:** `a73dad6ae5d41b5b8be7275a2cd39792ce9192addfdfb65ceebf6cc153844e0f`

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: ForPrint Print Mode Catalog
type: object
required:
- catalog_type
- metadata
- items
properties:
  catalog_type:
    const: print_modes
  metadata:
    type: object
    required:
    - id
    - version
    - catalog_status
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
        type: string
      catalog_status:
        const: draft_canonical_seed
      schema_status:
        const: unstable_v0_1
      usage:
        const: allowed_for_projection_use
      contract_status:
        const: not_final_contract
      owner_module:
        const: forprint_library
      notes:
        type: string
    additionalProperties: true
  items:
    type: array
    minItems: 1
    items:
      type: object
      required:
      - id
      - name_uk
      - name_en
      - aliases
      - status
      - version
      - owner_module
      - schema_status
      - notes
      properties:
        id:
          type: string
          pattern: ^[a-z0-9_]+$
        name_uk:
          type: string
          minLength: 1
        name_en:
          type: string
          minLength: 1
        aliases:
          type: array
          minItems: 1
          items:
            type: string
            minLength: 1
        status:
          enum:
          - draft
          - active
          - deprecated
          - experimental
        version:
          type: string
        owner_module:
          const: forprint_library
        schema_status:
          const: unstable_v0_1
        notes:
          type: string
      additionalProperties: true
additionalProperties: false
```

## Primary source

**Path:** `schemas/product_family.schema.yaml`
**SHA256:** `6544b3cc1c7fc267a477544fa39847236e63454a1698aad659f7b687b57bbaab`

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: ForPrint Product Family Catalog
type: object
required:
- catalog_type
- metadata
- items
properties:
  catalog_type:
    const: product_families
  metadata:
    type: object
    required:
    - id
    - version
    - catalog_status
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
        type: string
      catalog_status:
        const: draft_canonical_seed
      schema_status:
        const: unstable_v0_1
      usage:
        const: allowed_for_projection_use
      contract_status:
        const: not_final_contract
      owner_module:
        const: forprint_library
      notes:
        type: string
    additionalProperties: true
  items:
    type: array
    minItems: 1
    items:
      type: object
      required:
      - id
      - name_uk
      - name_en
      - aliases
      - status
      - version
      - owner_module
      - schema_status
      - notes
      properties:
        id:
          type: string
          pattern: ^[a-z0-9_]+$
        name_uk:
          type: string
          minLength: 1
        name_en:
          type: string
          minLength: 1
        aliases:
          type: array
          minItems: 1
          items:
            type: string
            minLength: 1
        status:
          enum:
          - draft
          - active
          - deprecated
          - experimental
        version:
          type: string
        owner_module:
          const: forprint_library
        schema_status:
          const: unstable_v0_1
        notes:
          type: string
      additionalProperties: true
additionalProperties: false
```

## Primary source

**Path:** `scripts/coordination/export_coordination_foundation_alignment_closure.py`
**SHA256:** `ca0d10084715f118592fbdcef6ba55ccb5f81a12db9f20311c64e8e7a137c2d6`

```python
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]

PROMPT_ID = "library_coordination_foundation_alignment_v0_1"
BLUEPRINT_PROMPT_PATH = (
    "/srv/software_development/forprint-project/forprint_system_blueprint/"
    "coordination/outgoing_prompts/forprint_library/approved/"
    "2026-07-03__library__coordination_foundation_alignment_v0_1.md"
)

IMPLEMENTATION_COMMIT = "02e2cad"
IMPLEMENTATION_COMMIT_MESSAGE = "Add Library coordination foundation alignment"

REPORT_ID = (
    "2026-07-03__forprint_library__report__"
    "coordination-foundation-alignment-v0-1"
)
REPORT_PATH = ROOT / "coordination" / "reports" / "completion" / f"{REPORT_ID}.md"

STATUS_YAML = ROOT / "coordination" / "status" / "current_status.yaml"
STATUS_MD = ROOT / "coordination" / "status" / "current_status.md"
REPORTS_INDEX = ROOT / "coordination" / "reports" / "index.yaml"


def read_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}

    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")

    return data


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )


def ensure_list(data: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = data.setdefault(key, [])

    if not isinstance(value, list):
        raise ValueError(f"Expected list at key '{key}'")

    return value


def upsert_by_id(items: list[dict[str, Any]], item: dict[str, Any]) -> None:
    item_id = item["id"]

    for index, existing in enumerate(items):
        if isinstance(existing, dict) and existing.get("id") == item_id:
            items[index] = item
            return

    items.append(item)


def update_current_status_yaml() -> None:
    data = read_yaml(STATUS_YAML)

    data["module_id"] = "forprint_library"
    data["owner_module"] = "forprint_library"
    data["status"] = (
        "coordination_foundation_alignment_v0_1_"
        "ready_pending_blueprint_review"
    )
    data["stage"] = "coordination_foundation_alignment_v0_1_completion"
    data["updated_at"] = "2026-07-03"
    data["current_phase"] = "coordination_foundation_alignment_v0_1"
    data["last_completed_step"] = "library_coordination_foundation_alignment_ready"

    data["current_focus"] = [
        "Library coordination foundation alignment v0.1 completed",
        "prompt queue navigation confirmed",
        "document awareness confirmed",
        "context bundle no-write flow confirmed",
        "configuration and secrets policy documented",
        "project tree alignment notes documented",
        "Workbench and product modeling explicitly not started",
    ]

    data["coordination_foundation_alignment_v0_1"] = {
        "prompt_id": PROMPT_ID,
        "blueprint_prompt_path": BLUEPRINT_PROMPT_PATH,
        "implementation_commit": IMPLEMENTATION_COMMIT,
        "implementation_commit_message": IMPLEMENTATION_COMMIT_MESSAGE,
        "completion_report_id": REPORT_ID,
        "completion_report_path": str(REPORT_PATH.relative_to(ROOT)),
        "status": "completed_pending_blueprint_review",
        "makefile_rewrite": "not_needed",
        "operator_workflow": "confirmed",
        "prompt_queue_navigation": "confirmed",
        "document_awareness": "confirmed",
        "context_bundle_no_write": "confirmed",
        "configuration_policy": "documented_deferred_until_needed",
        "secrets_policy": "not_applicable_no_secrets_added",
        "project_tree_alignment": "documented",
        "check_report_visibility": "done",
        "tests": "104_passed",
        "workbench_started": False,
        "product_modeling_started": False,
        "production_runtime_changes": False,
    }

    data["next_recommended_step"] = {
        "status": "wait_for_blueprint_review",
        "recommended_action": (
            "Ask Blueprint to review Library coordination foundation "
            "alignment v0.1 and confirm readiness for the next prompt."
        ),
        "candidate_next_prompt": (
            "Library Configurable Product Workbench v0.1 — "
            "Business Card Skeleton"
        ),
    }

    write_yaml(STATUS_YAML, data)


def update_current_status_md() -> None:
    lines = [
        "# ForPrint Library Current Status",
        "",
        "## Status",
        "",
        "`coordination_foundation_alignment_v0_1_ready_pending_blueprint_review`",
        "",
        "## Current phase",
        "",
        "`coordination_foundation_alignment_v0_1`",
        "",
        "## Last completed step",
        "",
        "`library_coordination_foundation_alignment_ready`",
        "",
        "## Blueprint prompt",
        "",
        f"Prompt ID: `{PROMPT_ID}`",
        "",
        "Prompt path:",
        "",
        "```text",
        BLUEPRINT_PROMPT_PATH,
        "```",
        "",
        "## Implementation commit",
        "",
        "```text",
        f"{IMPLEMENTATION_COMMIT} {IMPLEMENTATION_COMMIT_MESSAGE}",
        "```",
        "",
        "## Completed",
        "",
        "- Coordination foundation alignment document.",
        "- Local Blueprint awareness alignment YAML.",
        "- Coordination foundation alignment validator.",
        "- Focused coordination tests.",
        "- Check-report row for coordination foundation alignment.",
        "- Configuration, secrets and project-tree alignment notes.",
        "",
        "## Validation result",
        "",
        "```text",
        "coordination foundation validator: OK",
        "make lint: OK",
        "make test: 104 passed",
        "make check-report: OK",
        "make check: OK",
        "make governance-check: OK",
        "make module-validate: OK",
        "```",
        "",
        "## Makefile policy",
        "",
        "Makefile was not rewritten.",
        "",
        "Existing operator targets were confirmed sufficient for this checkpoint.",
        "",
        "## Manual Blueprint mode",
        "",
        "Blueprint communication is temporarily handled through chat.",
        "",
        "The active prompt was handled through `prompt-read-next` and manual",
        "operator coordination.",
        "",
        "## Configuration and secrets",
        "",
        "No production config was added.",
        "",
        "No `.env` file was added.",
        "",
        "No real secrets or credentials were committed.",
        "",
        "Secrets checks are not applicable for the current Library scope.",
        "",
        "## Non-goals preserved",
        "",
        "This checkpoint did not implement:",
        "",
        "```text",
        "Configurable Product Workbench",
        "business_card product skeleton",
        "new product catalog generation",
        "1C import",
        "1C database parsing",
        "Calculator Engine integration",
        "production write",
        "price calculation",
        "material write-off logic",
        "CRM/client/carrier entities",
        "large repository refactor",
        "production catalog database",
        "live API",
        "runtime integration",
        "```",
        "",
        "## Completion report",
        "",
        "```text",
        str(REPORT_PATH.relative_to(ROOT)),
        "```",
        "",
        "## Next recommended step",
        "",
        "Wait for Blueprint review.",
        "",
        "Candidate next prompt:",
        "",
        "```text",
        "Library Configurable Product Workbench v0.1 — Business Card Skeleton",
        "```",
        "",
    ]

    STATUS_MD.parent.mkdir(parents=True, exist_ok=True)
    STATUS_MD.write_text("\n".join(lines), encoding="utf-8")


def update_reports_index() -> None:
    data = read_yaml(REPORTS_INDEX)

    completion_reports = ensure_list(data, "completion_reports")
    upsert_by_id(
        completion_reports,
        {
            "id": REPORT_ID,
            "module_id": "forprint_library",
            "type": "completion_report",
            "status": "completed_pending_blueprint_review",
            "path": str(REPORT_PATH.relative_to(ROOT)),
            "related_prompt_id": PROMPT_ID,
            "implementation_commit": IMPLEMENTATION_COMMIT,
            "created_at": "2026-07-03",
        },
    )

    commit_reports = ensure_list(data, "commit_reports")
    upsert_by_id(
        commit_reports,
        {
            "id": "forprint_library_coordination_foundation_alignment_commit_02e2cad",
            "module_id": "forprint_library",
            "type": "commit_report",
            "status": "pushed",
            "commit": IMPLEMENTATION_COMMIT,
            "message": IMPLEMENTATION_COMMIT_MESSAGE,
            "related_prompt_id": PROMPT_ID,
            "created_at": "2026-07-03",
        },
    )

    write_yaml(REPORTS_INDEX, data)


def write_completion_report() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# ForPrint Library Coordination Foundation Alignment v0.1",
        "",
        "## Completion Report",
        "",
        f"Report ID: `{REPORT_ID}`",
        "",
        "Module: `forprint_library`",
        "",
        "Status: `completed_pending_blueprint_review`",
        "",
        "Date: `2026-07-03`",
        "",
        "## Blueprint prompt",
        "",
        f"Prompt ID: `{PROMPT_ID}`",
        "",
        "Prompt path:",
        "",
        "```text",
        BLUEPRINT_PROMPT_PATH,
        "```",
        "",
        "## Implementation commit",
        "",
        "```text",
        f"{IMPLEMENTATION_COMMIT} {IMPLEMENTATION_COMMIT_MESSAGE}",
        "```",
        "",
        "Push status: `pushed to origin/main`",
        "",
        "## Changed files",
        "",
        "```text",
        "docs/architecture/coordination_foundation_alignment.md",
        "coordination/blueprint_awareness/library_coordination_foundation_alignment_v0_1.yaml",
        "scripts/coordination/validate_coordination_foundation_alignment.py",
        "tests/coordination/test_coordination_foundation_alignment.py",
        "scripts/run_library_checks.py",
        "reports/library_check_report.json",
        "reports/library_check_report.md",
        "```",
        "",
        "## Structural and coordination scope completed",
        "",
        "- Makefile/operator workflow inspected and confirmed.",
        "- Prompt queue navigation confirmed through `prompt-read-next`.",
        "- Document awareness dashboard confirmed.",
        "- Context bundle no-write flow confirmed.",
        "- Module validation confirmed.",
        "- Configuration architecture documented as deferred until needed.",
        "- Secrets and `.env` policy documented as not applicable for this scope.",
        "- Project tree alignment notes documented.",
        "- Completion reporting prepared.",
        "",
        "## Check-report visibility",
        "",
        "The check report now includes:",
        "",
        "```text",
        "Library coordination foundation alignment",
        "```",
        "",
        "Expected result:",
        "",
        "```text",
        "Coordination workflow, document awareness and alignment notes validate",
        "```",
        "",
        "Status: `OK`.",
        "",
        "## Validation results",
        "",
        "```text",
        "coordination foundation validator: OK",
        "make lint: OK",
        "make test: 104 passed",
        "make check-report: OK",
        "make check: OK",
        "make governance-check: OK",
        "make module-validate: OK",
        "git diff --check: OK",
        "```",
        "",
        "## Deferred items",
        "",
        "```text",
        "formal exhaustive review of all unseen Blueprint standards",
        "config/ runtime configuration",
        ".env.example",
        "secrets-check implementation",
        "Configurable Product Workbench",
        "business_card product skeleton",
        "1C import",
        "Calculator Engine integration",
        "production catalog database",
        "live API",
        "runtime integrations",
        "large repository refactor",
        "```",
        "",
        "## Readiness statement",
        "",
        "Library is coordination-ready for the next Blueprint-controlled prompt.",
        "",
        "Product modeling has not started.",
        "",
        "## Blueprint review request",
        "",
        "Blueprint should review this coordination foundation alignment and",
        "confirm whether Library may proceed to:",
        "",
        "```text",
        "Library Configurable Product Workbench v0.1 — Business Card Skeleton",
        "```",
        "",
    ]

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    update_current_status_yaml()
    update_current_status_md()
    update_reports_index()
    write_completion_report()

    print(f"OK: wrote {REPORT_PATH.relative_to(ROOT)}")
    print(f"OK: updated {STATUS_YAML.relative_to(ROOT)}")
    print(f"OK: updated {STATUS_MD.relative_to(ROOT)}")
    print(f"OK: updated {REPORTS_INDEX.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Primary source

**Path:** `scripts/coordination/validate_coordination_foundation_alignment.py`
**SHA256:** `87077132b2a1a3327b38a1531b870456ff8a59702259c61b08e3e3534d1314dc`

```python
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]

DOC_PATH = ROOT / "docs" / "architecture" / "coordination_foundation_alignment.md"
ALIGNMENT_PATH = (
    ROOT
    / "coordination"
    / "blueprint_awareness"
    / "library_coordination_foundation_alignment_v0_1.yaml"
)

REQUIRED_COORDINATION_PATHS = [
    ROOT / "coordination" / "blueprint_source.yaml",
    ROOT / "coordination" / "prompts" / "index.yaml",
    ROOT / "coordination" / "reports" / "index.yaml",
    ROOT / "coordination" / "reports" / "completion",
    ROOT / "coordination" / "status" / "current_status.yaml",
    ROOT / "coordination" / "status" / "current_status.md",
    ROOT / "coordination" / "status" / "next_questions_for_blueprint.md",
    ROOT / "coordination" / "blueprint_awareness" / "document_review_ledger.yaml",
]

REQUIRED_TARGETS = {
    "blueprint-pull",
    "prompt-read-next",
    "document-awareness",
    "context-bundle",
    "module-validate",
    "prompt-queue-validate",
    "document-manifest",
    "check",
    "check-report",
    "governance-check",
}

NON_GOAL_FLAGS = {
    "workbench_started",
    "configurable_product_workbench_started",
    "business_card_product_skeleton_started",
    "product_modeling_started",
    "one_c_import_started",
    "calculator_integration_started",
    "production_catalog_database_started",
    "live_api_started",
    "production_runtime_changes",
    "production_writes_added",
    "runtime_integrations_added",
}


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise AssertionError(f"Missing file: {path.relative_to(ROOT)}")

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}

    if not isinstance(data, dict):
        raise AssertionError(f"YAML root must be a mapping: {path.relative_to(ROOT)}")

    return data


def validate_required_files() -> None:
    for path in [DOC_PATH, ALIGNMENT_PATH, *REQUIRED_COORDINATION_PATHS]:
        if not path.exists():
            raise AssertionError(f"Missing path: {path.relative_to(ROOT)}")


def validate_doc() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")

    required_phrases = [
        "Library Coordination Foundation Alignment v0.1",
        "library_coordination_foundation_alignment_v0_1",
        "Manual Blueprint communication mode",
        "No destructive Makefile rewrite is required",
        "controlled coordination backlog",
        "Secrets checks are considered not applicable",
        "Configurable Product Workbench",
        "business_card product skeleton",
        "Library Configurable Product Workbench v0.1",
    ]

    for phrase in required_phrases:
        if phrase not in text:
            raise AssertionError(f"Document is missing phrase: {phrase}")


def validate_alignment_yaml(data: dict[str, Any]) -> None:
    if data.get("schema_version") != "library_coordination_foundation_alignment_v0_1":
        raise AssertionError("Unexpected schema_version")

    if data.get("module_id") != "forprint_library":
        raise AssertionError("Unexpected module_id")

    if data.get("prompt_id") != "library_coordination_foundation_alignment_v0_1":
        raise AssertionError("Unexpected prompt_id")

    operator_workflow = data.get("operator_workflow", {})
    if not isinstance(operator_workflow, dict):
        raise AssertionError("operator_workflow must be a mapping")

    confirmed_targets = set(operator_workflow.get("confirmed_targets", []))
    missing_targets = sorted(REQUIRED_TARGETS - confirmed_targets)
    if missing_targets:
        raise AssertionError(f"Missing confirmed targets: {missing_targets}")

    if operator_workflow.get("makefile_rewrite") is not False:
        raise AssertionError("makefile_rewrite must be false")

    if operator_workflow.get("destructive_makefile_rewrite") is not False:
        raise AssertionError("destructive_makefile_rewrite must be false")

    coordination_structure = data.get("coordination_structure", {})
    if not isinstance(coordination_structure, dict):
        raise AssertionError("coordination_structure must be a mapping")

    if coordination_structure.get("backlog_is_blocker") is not False:
        raise AssertionError("coordination backlog must not be a blocker")

    configuration = data.get("configuration_alignment", {})
    if not isinstance(configuration, dict):
        raise AssertionError("configuration_alignment must be a mapping")

    if configuration.get("config_directory_required_now") is not False:
        raise AssertionError("config directory must be deferred for this checkpoint")

    if configuration.get("production_runtime_config_added") is not False:
        raise AssertionError("production runtime config must not be added")

    secrets = data.get("secrets_alignment", {})
    if not isinstance(secrets, dict):
        raise AssertionError("secrets_alignment must be a mapping")

    if secrets.get("secrets_required_now") is not False:
        raise AssertionError("secrets must not be required now")

    if secrets.get("real_secrets_committed") is not False:
        raise AssertionError("real secrets must not be committed")

    tree = data.get("project_tree_alignment", {})
    if not isinstance(tree, dict):
        raise AssertionError("project_tree_alignment must be a mapping")

    for key in [
        "large_refactor",
        "application_code_moved",
        "deep_nesting_added",
        "workbench_directories_created",
        "production_runtime_directories_created",
    ]:
        if tree.get(key) is not False:
            raise AssertionError(f"{key} must be false")

    non_goals = data.get("non_goals", {})
    if not isinstance(non_goals, dict):
        raise AssertionError("non_goals must be a mapping")

    for key in NON_GOAL_FLAGS:
        if non_goals.get(key) is not False:
            raise AssertionError(f"non-goal flag must be false: {key}")

    readiness = data.get("readiness", {})
    if not isinstance(readiness, dict):
        raise AssertionError("readiness must be a mapping")

    if readiness.get("coordination_ready_for_next_prompt") is not True:
        raise AssertionError("coordination readiness must be true")

    if readiness.get("product_ready") is not False:
        raise AssertionError("product readiness must remain false")


def main() -> int:
    validate_required_files()
    validate_doc()
    validate_alignment_yaml(load_yaml(ALIGNMENT_PATH))

    print("OK: Library coordination foundation alignment validates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

# Part C — Related tests

## Related test

**Path:** `tests/content/test_business_card_product_card.py`
**SHA256:** `dffe8d8f8437fe45b4b1fb1136670bf14b2dfc8a75a1206fb3c6b3fff3b7f9ca`

```python
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
```

## Related test

**Path:** `tests/content/test_calculator_input_contract.py`
**SHA256:** `2df2de6764e6f5f3fd0924fe2ab39b986193200a12167e6264ccb850fb96fab8`

```python
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
```

## Related test

**Path:** `tests/content/test_library_reference_contract.py`
**SHA256:** `2b55b490e9a69ce04166ee99f5c820caf78c077ba4a416c6863f430fe7bb49cf`

```python
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]

DOC_PATH = ROOT / "docs" / "architecture" / "reference_contract_foundation.md"
EXAMPLES_PATH = (
    ROOT / "examples" / "reference_contract" / "library_reference_examples.yaml"
)
SCHEMA_PATH = ROOT / "schemas" / "reference_contract" / "library_reference.schema.yaml"
VALIDATOR = (
    ROOT / "scripts" / "reference_contract" / "validate_library_reference_contract.py"
)

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


def load_examples() -> dict:
    data = yaml.safe_load(EXAMPLES_PATH.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def test_library_reference_contract_files_exist() -> None:
    for path in [DOC_PATH, EXAMPLES_PATH, SCHEMA_PATH, VALIDATOR]:
        assert path.exists(), path


def test_library_reference_contract_examples_cover_required_types() -> None:
    data = load_examples()

    examples = data["examples"]

    seen_types = {
        example["downstream_payload"]["library_reference"]["reference_type"]
        for example in examples
    }

    assert EXPECTED_REFERENCE_TYPES.issubset(seen_types)


def test_library_reference_contract_examples_cover_required_statuses() -> None:
    data = load_examples()

    examples = data["examples"]

    seen_statuses = {
        example["downstream_payload"]["library_reference"]["resolution_status"]
        for example in examples
    }

    assert EXPECTED_STATUSES.issubset(seen_statuses)


def test_library_reference_contract_examples_have_required_fields() -> None:
    data = load_examples()

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

    for example in data["examples"]:
        reference = example["downstream_payload"]["library_reference"]

        assert required_fields.issubset(reference)
        assert reference["schema_version"] == "library_reference_v0_2"


def test_library_reference_contract_schema_defines_version_type_and_status() -> None:
    schema = yaml.safe_load(SCHEMA_PATH.read_text(encoding="utf-8"))

    assert schema["$id"] == "forprint_library.reference_contract.library_reference_v0_2"
    assert "schema_version" in schema["required"]
    assert "reference_type" in schema["required"]
    assert "resolution_status" in schema["required"]

    assert set(schema["properties"]["reference_type"]["enum"]) == EXPECTED_REFERENCE_TYPES
    assert set(schema["properties"]["resolution_status"]["enum"]) == EXPECTED_STATUSES


def test_library_reference_contract_docs_keep_boundaries_clear() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "Downstream modules must not become owners" in text
    assert "Library must not own" in text
    assert "production catalog database" in text
    assert "live API" in text
    assert "Calculator pricing logic" in text


def test_library_reference_contract_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "OK: Library reference contract foundation validates" in result.stdout
```

## Related test

**Path:** `tests/contract/test_architecture_docs.py`
**SHA256:** `44e43e4da7b68f58b33b201a4a7c423942d335e9a69c291daa9339528122a169`

```python
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_DOCS = [
    "docs/architecture/library_boundaries.md",
    "docs/architecture/catalog_seed_policy.md",
    "docs/architecture/canonical_id_policy.md",
    "docs/architecture/alias_policy.md",
    "docs/architecture/dependent_module_usage.md",
]


def read_lower(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8").casefold()


def test_required_architecture_docs_exist() -> None:
    for relative_path in REQUIRED_DOCS:
        assert (ROOT / relative_path).exists(), relative_path


def test_canonical_id_policy_explains_stable_ids() -> None:
    text = read_lower("docs/architecture/canonical_id_policy.md")

    assert "canonical ids are stable internal truth" in text
    assert "dependent modules must reference canonical ids" in text
    assert "not a final production contract" in text


def test_alias_policy_explains_conflict_handling() -> None:
    text = read_lower("docs/architecture/alias_policy.md")

    assert "aliases are lookup helpers" in text
    assert "not canonical truth" in text
    assert "must not silently resolve" in text
    assert "unresolved" in text


def test_dependent_module_usage_documents_consumers() -> None:
    text = read_lower("docs/architecture/dependent_module_usage.md")

    for phrase in [
        "calculator engine",
        "telegram bot",
        "operational registry",
        "accounting registry",
        "prepress hub",
    ]:
        assert phrase in text


def test_catalog_seed_policy_documents_required_status_terms() -> None:
    text = read_lower("docs/architecture/catalog_seed_policy.md")

    for phrase in [
        "draft_canonical_seed",
        "unstable_v0_1",
        "allowed_for_projection_use",
        "not_final_contract",
        "forprint_library",
    ]:
        assert phrase in text


def test_library_boundaries_exclude_operational_ownership() -> None:
    text = read_lower("docs/architecture/library_boundaries.md")

    for phrase in [
        "clients",
        "orders",
        "payments",
        "warehouse stock truth",
        "production runtime",
        "1c synchronization",
        "crm workflow",
        "telegram runtime",
        "calculator logic",
    ]:
        assert phrase in text
```

## Related test

**Path:** `tests/contract/test_catalog_seed_v0_1.py`
**SHA256:** `1d1ad2fe1fac4e3d0a51d800038e892babe3f1caac01c23fd635b6e7a9c1b945`

```python
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
```

## Related test

**Path:** `tests/contract/test_completion_report.py`
**SHA256:** `8aabf59cf455b05d240d64c1cbdde86ae5f600ff14c46ec9b8ecc322abdf6ccb`

```python
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]

REPORT_ID = (
    "2026-06-06__forprint_library__report__catalog-seed-v0-1-and-coordination-bootstrap"
)
REPORT_PATH = ROOT / "coordination" / "reports" / "completion" / f"{REPORT_ID}.md"


def test_completion_report_exists() -> None:
    assert REPORT_PATH.exists()


def test_completion_report_contains_required_sections() -> None:
    text = REPORT_PATH.read_text(encoding="utf-8").casefold()

    for phrase in [
        "files added or changed",
        "catalog seed contents summary",
        "schemas added",
        "tests added or updated",
        "check-report behavior",
        "makefile targets",
        "coordination files",
        "boundary confirmation",
        "open questions for blueprint",
        "recommended next step",
    ]:
        assert phrase in text


def test_reports_index_references_completion_report() -> None:
    data = yaml.safe_load(
        (ROOT / "coordination" / "reports" / "index.yaml").read_text(encoding="utf-8")
    )

    reports = data["completion_reports"]
    report_ids = {item["id"] for item in reports}

    assert REPORT_ID in report_ids


def test_current_status_keeps_known_project_phase() -> None:
    data = yaml.safe_load(
        (ROOT / "coordination" / "status" / "current_status.yaml").read_text(
            encoding="utf-8"
        )
    )

    known_statuses = {
        "completed_pending_blueprint_review",
        "bootstrap_completed_pending_blueprint_review",
        "shared_operational_dictionary_v0_1_ready_pending_blueprint_review",
        "make_first_semantic_reference_readiness_v0_1_ready_pending_blueprint_review",
        "reference_contract_foundation_v0_2_ready_pending_blueprint_review",
        "reference_contract_foundation_v0_2_accepted_by_blueprint",
        "coordination_foundation_alignment_v0_1_ready_pending_blueprint_review",
        "reference_consumption_pilot_v0_3_ready_pending_blueprint_review",
        "business_card_skeleton_v0_1_ready_pending_blueprint_review",
    }

    assert data["status"] in known_statuses
    assert data["module_id"] == "forprint_library"
    assert data["owner_module"] == "forprint_library"
```

## Related test

**Path:** `tests/contract/test_dictionary_policy_docs.py`
**SHA256:** `aecf2f0a6a518d3db80ddca1b21b33a64d2bf6df0945a4941addebf7394f8dea`

```python
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_DICTIONARY_DOCS = [
    "docs/architecture/shared_operational_dictionary_policy.md",
    "docs/architecture/status_dictionary_policy.md",
    "docs/architecture/source_system_dictionary_policy.md",
    "docs/architecture/entity_type_dictionary_policy.md",
    "docs/architecture/unit_dictionary_policy.md",
    "docs/architecture/dictionary_consumption_policy.md",
    "docs/architecture/dictionary_versioning_policy.md",
]


def read_lower(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8").casefold()


def test_required_dictionary_policy_docs_exist() -> None:
    for relative_path in REQUIRED_DICTIONARY_DOCS:
        assert (ROOT / relative_path).exists(), relative_path


def test_shared_operational_dictionary_policy_confirms_library_ownership() -> None:
    text = read_lower("docs/architecture/shared_operational_dictionary_policy.md")

    assert "library owns canonical shared operational dictionary definitions" in text
    assert "other modules may consume" in text
    assert "must not become independent permanent dictionary authorities" in text


def test_status_dictionary_policy_mentions_consuming_modules() -> None:
    text = read_lower("docs/architecture/status_dictionary_policy.md")

    for phrase in [
        "operational registry",
        "calculator engine",
        "telegram bot",
        "crm",
        "accounting registry",
    ]:
        assert phrase in text


def test_source_system_policy_mentions_required_sources() -> None:
    text = read_lower("docs/architecture/source_system_dictionary_policy.md")

    for phrase in [
        "forprint_operational_registry",
        "forprint_library",
        "calculator_engine",
        "accounting_registry_service",
        "telegram_bot",
        "one_c_bas",
        "manual_entry",
        "unknown",
    ]:
        assert phrase in text


def test_entity_type_policy_mentions_required_entities() -> None:
    text = read_lower("docs/architecture/entity_type_dictionary_policy.md")

    for phrase in [
        "client_account",
        "order",
        "order_line",
        "material_requirement",
        "payment_projection",
        "workflow_stage",
    ]:
        assert phrase in text


def test_unit_policy_marks_not_final_inventory_unit_system() -> None:
    text = read_lower("docs/architecture/unit_dictionary_policy.md")

    assert "not_final_inventory_unit_system" in text
    assert "not a final inventory" in text


def test_dictionary_consumption_policy_prevents_local_id_invention() -> None:
    text = read_lower("docs/architecture/dictionary_consumption_policy.md")

    assert "should reference canonical ids" in text
    assert "not invent new internal ids" in text


def test_dictionary_versioning_policy_mentions_deprecation() -> None:
    text = read_lower("docs/architecture/dictionary_versioning_policy.md")

    assert "deprecated values must remain readable" in text
    assert "historical records" in text


def test_library_boundary_prevents_operational_records() -> None:
    text = read_lower("docs/architecture/shared_operational_dictionary_policy.md")

    for phrase in [
        "real operational orders",
        "real clients",
        "real payments",
        "real material stock",
        "calculator formulas",
        "telegram runtime",
        "crm dashboard",
        "1c synchronization",
    ]:
        assert phrase in text
```

## Related test

**Path:** `tests/contract/test_semantic_reference_readiness.py`
**SHA256:** `3bacc230b727ef14de68dc11c591d4ef7ff8bbbbb840203d1f076380bad190bc`

```python
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def test_semantic_reference_preview_contains_required_reference_types() -> None:
    data = yaml.safe_load(
        (ROOT / "examples" / "semantic_reference_preview.yaml").read_text(
            encoding="utf-8"
        )
    )

    reference_types = {
        item["reference_type"] for item in data["canonical_references"]
    }

    assert {
        "product_service",
        "material",
        "operation",
        "template",
    }.issubset(reference_types)


def test_semantic_reference_preview_keeps_library_boundaries() -> None:
    data = yaml.safe_load(
        (ROOT / "examples" / "semantic_reference_preview.yaml").read_text(
            encoding="utf-8"
        )
    )

    forbidden_values = {
        value
        for item in data["canonical_references"]
        for value in item["forbidden_usage"]
    }

    for expected in [
        "pricing_formula",
        "warehouse_stock_truth",
        "operational_order_state",
    ]:
        assert expected in forbidden_values


def test_semantic_reference_docs_exist_and_define_handoff_boundaries() -> None:
    readiness = (
        ROOT / "docs" / "architecture" / "semantic_reference_readiness.md"
    ).read_text(encoding="utf-8").casefold()

    handoff = (
        ROOT / "docs" / "architecture" / "downstream_reference_contract_notes.md"
    ).read_text(encoding="utf-8").casefold()

    assert "not to build the full production catalog database" in readiness
    assert "calculator engine may reference canonical ids" in readiness
    assert "operational registry may store library ids as operational projections" in handoff
    assert "no downstream module should silently invent" in handoff


def test_semantic_reference_readiness_validator_passes_all_checks() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/validate_semantic_reference_readiness.py",
            "--check",
            "all",
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )

    assert completed.returncode == 0, completed.stdout
    assert "OK: semantic reference readiness check 'all' passed." in completed.stdout
```

## Related test

**Path:** `tests/contract/test_shared_dictionary_completion_report.py`
**SHA256:** `dfb705183e1cfb578c559e3062750a1a519d2d24e28940b803b21ca681a5f9b9`

```python
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]

REPORT_ID = "2026-06-09__forprint_library__report__shared-operational-dictionary-v0-1"
REPORT_PATH = ROOT / "coordination" / "reports" / "completion" / f"{REPORT_ID}.md"


def test_shared_dictionary_completion_report_exists() -> None:
    assert REPORT_PATH.exists()


def test_shared_dictionary_completion_report_contains_required_sections() -> None:
    text = REPORT_PATH.read_text(encoding="utf-8").casefold()

    for phrase in [
        "files added or changed",
        "dictionary groups added",
        "schemas added",
        "loader and resolver behavior",
        "examples added",
        "terminal preview summary",
        "architecture docs added",
        "tests added and results",
        "check-report result",
        "makefile targets added",
        "coordination status and report updates",
        "boundary confirmation",
        "open questions for blueprint",
        "recommended next step",
    ]:
        assert phrase in text


def test_reports_index_references_shared_dictionary_completion_report() -> None:
    data = yaml.safe_load(
        (ROOT / "coordination" / "reports" / "index.yaml").read_text(
            encoding="utf-8"
        )
    )

    report_ids = {item["id"] for item in data["completion_reports"]}

    assert REPORT_ID in report_ids


def test_current_status_keeps_shared_dictionary_completion_record() -> None:
    data = yaml.safe_load(
        (ROOT / "coordination" / "status" / "current_status.yaml").read_text(
            encoding="utf-8"
        )
    )

    assert data["module_id"] == "forprint_library"
    assert data["owner_module"] == "forprint_library"

    shared_dictionary = data["shared_operational_dictionary_v0_1"]

    assert (
        shared_dictionary["dictionary_status"]
        == "draft_shared_operational_dictionary_v0_1"
    )
    assert shared_dictionary["coordination_report"] == "done"
    assert shared_dictionary["check_report_extension"] == "done"
```

## Related test

**Path:** `tests/contract/test_shared_operational_dictionary_v0_1.py`
**SHA256:** `84097bcc0bdd831eb721fae17c897965175760607cd6051a77dd8633d7427de8`

```python
from __future__ import annotations

from pathlib import Path

import yaml
from forprint_library.dictionaries.loader import (
    load_all_dictionaries,
    load_dictionary,
    load_shared_dictionary,
)
from forprint_library.dictionaries.models import (
    DICTIONARY_GROUPS,
    EXPECTED_SHARED_METADATA,
    REQUIRED_DICTIONARY_ENTRY_FIELDS,
)
from forprint_library.dictionaries.validation import (
    collect_shared_dictionary_entries,
    find_duplicate_aliases,
    validate_dictionary_group,
    validate_shared_dictionary,
)
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]


def test_shared_dictionary_loads() -> None:
    shared_dictionary = load_shared_dictionary()

    validate_shared_dictionary(shared_dictionary)
    assert shared_dictionary["metadata"]["id"] == "shared_operational_dictionary_v0_1"


def test_all_dictionary_groups_exist() -> None:
    shared_dictionary = load_shared_dictionary()
    groups = shared_dictionary["dictionary_groups"]

    for group_name in DICTIONARY_GROUPS:
        assert group_name in groups
        assert isinstance(groups[group_name], list)
        assert groups[group_name]


def test_group_dictionary_files_load_and_validate() -> None:
    dictionaries = load_all_dictionaries()

    for group_name in DICTIONARY_GROUPS:
        dictionary = dictionaries[group_name]
        validate_dictionary_group(group_name, dictionary)
        assert dictionary["dictionary_group"] == group_name
        assert dictionary["entries"]


def test_all_entry_ids_are_unique_within_group() -> None:
    dictionaries = load_all_dictionaries()

    for group_name, dictionary in dictionaries.items():
        ids = [entry["id"] for entry in dictionary["entries"]]
        assert len(ids) == len(set(ids)), group_name


def test_all_entries_have_required_fields() -> None:
    entries = collect_shared_dictionary_entries(load_shared_dictionary())

    for entry in entries:
        for field in REQUIRED_DICTIONARY_ENTRY_FIELDS:
            assert field in entry, f"{entry.get('id')} missing {field}"


def test_aliases_are_lists() -> None:
    entries = collect_shared_dictionary_entries(load_shared_dictionary())

    for entry in entries:
        assert isinstance(entry["aliases"], list), entry["id"]


def test_duplicate_aliases_are_not_present_within_groups() -> None:
    entries = collect_shared_dictionary_entries(load_shared_dictionary())

    assert find_duplicate_aliases(entries) == {}


def test_shared_metadata_has_required_status_terms() -> None:
    metadata = load_shared_dictionary()["metadata"]

    for key, expected_value in EXPECTED_SHARED_METADATA.items():
        assert metadata[key] == expected_value

    assert metadata["unit_dictionary_status"] == "not_final_inventory_unit_system"


def test_source_system_contains_required_values() -> None:
    entries = load_dictionary("source_system")["entries"]
    ids = {entry["id"] for entry in entries}

    for required_id in [
        "forprint_operational_registry",
        "calculator_engine",
        "forprint_library",
        "accounting_registry_service",
        "telegram_bot",
        "one_c_bas",
    ]:
        assert required_id in ids


def test_entity_type_contains_required_values() -> None:
    entries = load_dictionary("entity_type")["entries"]
    ids = {entry["id"] for entry in entries}

    for required_id in [
        "order",
        "order_line",
        "client_account",
        "workflow_stage",
        "payment_projection",
        "material_requirement",
    ]:
        assert required_id in ids


def test_order_status_contains_required_values() -> None:
    entries = load_dictionary("order_status")["entries"]
    ids = {entry["id"] for entry in entries}

    for required_id in [
        "draft",
        "confirmed",
        "completed",
        "cancelled",
        "manual_review_required",
    ]:
        assert required_id in ids


def test_payment_status_contains_required_values() -> None:
    entries = load_dictionary("payment_status")["entries"]
    ids = {entry["id"] for entry in entries}

    for required_id in [
        "unpaid",
        "partially_paid",
        "overdue",
        "paid_reference_confirmed",
    ]:
        assert required_id in ids


def test_workflow_stage_status_contains_required_values() -> None:
    entries = load_dictionary("workflow_stage_status")["entries"]
    ids = {entry["id"] for entry in entries}

    for required_id in [
        "waiting_external_contractor",
        "late",
        "manual_review_required",
    ]:
        assert required_id in ids


def test_material_requirement_status_contains_required_values() -> None:
    entries = load_dictionary("material_requirement_status")["entries"]
    ids = {entry["id"] for entry in entries}

    assert "warehouse_reference_pending" in ids


def test_alert_severity_contains_required_values() -> None:
    entries = load_dictionary("alert_severity")["entries"]
    ids = {entry["id"] for entry in entries}

    for required_id in ["warning", "high", "critical"]:
        assert required_id in ids


def test_unit_contains_required_values() -> None:
    entries = load_dictionary("unit")["entries"]
    ids = {entry["id"] for entry in entries}

    for required_id in ["pcs", "m2", "kg", "service", "unknown"]:
        assert required_id in ids


def test_shared_dictionary_schema_validates_shared_dictionary() -> None:
    instance = yaml.safe_load(
        (ROOT / "dictionaries/shared_operational_dictionary_v0_1.yaml").read_text(
            encoding="utf-8"
        )
    )
    schema = yaml.safe_load(
        (ROOT / "schemas/shared_operational_dictionary.schema.yaml").read_text(
            encoding="utf-8"
        )
    )

    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(instance)


def test_dictionary_schema_files_are_valid_json_schemas() -> None:
    schema_paths = [
        ROOT / "schemas/dictionary_entry.schema.yaml",
        ROOT / "schemas/shared_operational_dictionary.schema.yaml",
    ]

    for schema_path in schema_paths:
        schema = yaml.safe_load(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)


def test_no_real_operational_records_are_created() -> None:
    forbidden_paths = [
        ROOT / "orders",
        ROOT / "clients",
        ROOT / "payments",
        ROOT / "warehouse_stock",
        ROOT / "production_runtime",
    ]

    for path in forbidden_paths:
        assert not path.exists(), path
```

## Related test

**Path:** `tests/coordination/test_business_card_skeleton_closure.py`
**SHA256:** `cdcf0c853ed83f0cb509a85b5e15d92884c3e0e16df381ddd10937ca7eb2bc76`

```python

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]

PROMPT_ID = "library_configurable_product_workbench_business_card_skeleton_v0_1"
REPORT_ID = "2026-07-11__forprint_library__report__business-card-skeleton-v0-1"
IMPLEMENTATION_COMMIT = "b8eb062"

REPORT = ROOT / "coordination" / "reports" / "completion" / f"{REPORT_ID}.md"
REPORTS_INDEX = ROOT / "coordination" / "reports" / "index.yaml"
CURRENT_STATUS_YAML = ROOT / "coordination" / "status" / "current_status.yaml"
CURRENT_STATUS_MD = ROOT / "coordination" / "status" / "current_status.md"
NEXT_QUESTIONS = ROOT / "coordination" / "status" / "next_questions_for_blueprint.md"


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def assert_clean_text_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    assert text.endswith("\n")
    assert not text.endswith("\n\n")


def test_business_card_completion_report_exists() -> None:
    assert REPORT.exists()
    text = REPORT.read_text(encoding="utf-8")

    assert PROMPT_ID in text
    assert IMPLEMENTATION_COMMIT in text
    assert "product.business_card" in text
    assert "catalog/configurable_products/business_card.yaml" in text
    assert "schemas/configurable_product.schema.yaml" in text
    assert "Business card product skeleton" in text
    assert "Business card product preview" in text
    assert "No Blueprint repository writes" in text
    assert "No price calculation" in text
    assert "No final price formula" in text
    assert "No material write-off logic" in text
    assert "No open questions" in text


def test_business_card_completion_report_mentions_completion_packet_boundary() -> None:
    text = REPORT.read_text(encoding="utf-8")

    assert "Generic completion packet automation was not available" in text
    assert "Library-side exporter generated" in text
    assert "No files were written directly into the Blueprint repository" in text


def test_reports_index_contains_business_card_completion_report() -> None:
    data = load_yaml(REPORTS_INDEX)
    reports = data["reports"]

    matching = [
        report
        for report in reports
        if isinstance(report, dict) and report.get("id") == REPORT_ID
    ]
    assert len(matching) == 1

    report = matching[0]
    assert report["prompt_id"] == PROMPT_ID
    assert report["implementation_commit"] == IMPLEMENTATION_COMMIT
    assert report["status"] == "completed_pending_blueprint_review"


def test_current_status_yaml_tracks_business_card_checkpoint() -> None:
    data = load_yaml(CURRENT_STATUS_YAML)

    assert data["status"] == "completed_pending_blueprint_review"
    assert data["current_phase"] == "business_card_skeleton_v0_1"
    assert data["last_completed_step"] == "library_business_card_skeleton_ready"

    checkpoint = data["configurable_product_workbench_business_card_skeleton_v0_1"]
    assert checkpoint["prompt_id"] == PROMPT_ID
    assert checkpoint["status"] == "completed_pending_blueprint_review"
    assert checkpoint["implementation_commit"] == IMPLEMENTATION_COMMIT
    assert checkpoint["product_id"] == "product.business_card"

    assert checkpoint["boundaries"]["price_calculation_added"] is False
    assert checkpoint["boundaries"]["final_price_formula_added"] is False
    assert checkpoint["boundaries"]["material_write_off_added"] is False
    assert checkpoint["boundaries"]["blueprint_repository_written"] is False


def test_current_status_yaml_preserves_previous_history() -> None:
    data = load_yaml(CURRENT_STATUS_YAML)

    assert "make_first_semantic_reference_readiness_v0_1" in data
    assert "reference_contract_foundation_v0_2" in data
    assert "coordination_foundation_alignment_v0_1" in data
    assert "reference_consumption_pilot_v0_3" in data


def test_current_status_md_mentions_business_card_checkpoint() -> None:
    text = CURRENT_STATUS_MD.read_text(encoding="utf-8")

    assert PROMPT_ID in text
    assert "business_card_skeleton_v0_1_ready_pending_blueprint_review" in text
    assert "product.business_card" in text
    assert "No full product catalog" in text
    assert "No 1C import" in text
    assert "No Calculator integration" in text
    assert "No Telegram Bot integration" in text
    assert "No Operational Registry write" in text
    assert "No Blueprint repository writes" in text
    assert "Previous completed checkpoints" in text
    assert "reference_consumption_pilot_v0_3" in text


def test_next_questions_has_no_open_questions() -> None:
    text = NEXT_QUESTIONS.read_text(encoding="utf-8")

    assert PROMPT_ID in text
    assert "No open questions" in text
    assert f"coordination/reports/completion/{REPORT_ID}.md" in text


def test_business_card_closure_text_files_are_clean() -> None:
    assert_clean_text_file(REPORT)
    assert_clean_text_file(CURRENT_STATUS_MD)
    assert_clean_text_file(NEXT_QUESTIONS)
```

## Related test

**Path:** `tests/coordination/test_calculator_input_contract_completion.py`
**SHA256:** `f592730268f00f0d38e9cfba8633e0c24441963787b03e9a841b0fc0c1920788`

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORT = (
    ROOT
    / "coordination"
    / "reports"
    / "completion"
    / "forprint_library_calculator_input_contract_v0_1_completion.md"
)


def test_calculator_input_contract_completion_report_exists() -> None:
    assert REPORT.exists()


def test_calculator_input_contract_completion_report_records_prompt_and_result() -> None:
    text = REPORT.read_text(encoding="utf-8")

    assert "forprint_library_calculator_input_contract_v0_1" in text
    assert "RESULT: READY_FOR_BLUEPRINT_REVIEW" in text
    assert "completed_pending_blueprint_review" in text
    assert "product.business_card" in text


def test_calculator_input_contract_completion_report_records_artifacts() -> None:
    text = REPORT.read_text(encoding="utf-8")

    required_paths = [
        "app/forprint_library/calculator_input/contract.py",
        "schemas/calculator_input/calculator_input_envelope.schema.yaml",
        "examples/calculator_input_contract/minimal_valid_business_card.yaml",
        "scripts/calculator_input/validate_calculator_input_contract.py",
        "tests/content/test_calculator_input_contract.py",
        "docs/architecture/library_calculator_input_contract.md",
        "docs/operations/library_calculator_input_contract_runbook.md",
        "docs/operations/library_calculator_input_contract_recovery.md",
    ]

    for path in required_paths:
        assert path in text


def test_calculator_input_contract_completion_report_records_validation() -> None:
    text = REPORT.read_text(encoding="utf-8")

    assert "25 passed" in text
    assert "160 passed" in text
    assert "LINT_EXIT: 0" in text
    assert "FORMAT_CHECK_EXIT: 0" in text
    assert "CHECK_EXIT: 0" in text
    assert "GOVERNANCE_CHECK_EXIT: 0" in text
    assert "MODULE_VALIDATE_EXIT: 0" in text
    assert "CHECK_REPORT_EXIT: 0" in text
    assert "CHECK_REPORT_FULL_EXIT: 0" in text
    assert "DIFF_CHECK_FINAL_EXIT: 0" in text


def test_calculator_input_contract_completion_report_records_boundaries() -> None:
    text = REPORT.read_text(encoding="utf-8")

    forbidden_scope = [
        "price formulas",
        "quote totals",
        "Calculator internals",
        "Telegram Bot changes",
        "Logistics changes",
        "CRM changes",
        "Gateway changes",
        "1C changes",
        "stock writes",
        "production writes",
        "Blueprint repository writes",
    ]

    for item in forbidden_scope:
        assert item in text
```

## Related test

**Path:** `tests/coordination/test_coordination_foundation_alignment.py`
**SHA256:** `df3adff50f108a2a3b5fb02efc4c3fb0420e1c616379152c8b4e1b5e32b4c8d2`

```python
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]

DOC_PATH = ROOT / "docs" / "architecture" / "coordination_foundation_alignment.md"
ALIGNMENT_PATH = (
    ROOT
    / "coordination"
    / "blueprint_awareness"
    / "library_coordination_foundation_alignment_v0_1.yaml"
)
VALIDATOR = (
    ROOT / "scripts" / "coordination" / "validate_coordination_foundation_alignment.py"
)


def load_alignment() -> dict:
    data = yaml.safe_load(ALIGNMENT_PATH.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def test_coordination_foundation_alignment_files_exist() -> None:
    for path in [DOC_PATH, ALIGNMENT_PATH, VALIDATOR]:
        assert path.exists(), path


def test_coordination_foundation_alignment_records_prompt_and_manual_mode() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "library_coordination_foundation_alignment_v0_1" in text
    assert "Manual Blueprint communication mode" in text
    assert "The Library Makefile is not rewritten" in text


def test_coordination_foundation_alignment_yaml_confirms_operator_targets() -> None:
    data = load_alignment()

    targets = set(data["operator_workflow"]["confirmed_targets"])

    for target in [
        "prompt-read-next",
        "document-awareness",
        "context-bundle",
        "module-validate",
        "prompt-queue-validate",
        "document-manifest",
    ]:
        assert target in targets

    assert data["operator_workflow"]["makefile_rewrite"] is False
    assert data["operator_workflow"]["destructive_makefile_rewrite"] is False


def test_coordination_foundation_alignment_keeps_non_goals_false() -> None:
    data = load_alignment()

    non_goals = data["non_goals"]

    for key in [
        "workbench_started",
        "configurable_product_workbench_started",
        "business_card_product_skeleton_started",
        "product_modeling_started",
        "one_c_import_started",
        "calculator_integration_started",
        "production_catalog_database_started",
        "live_api_started",
        "production_runtime_changes",
        "production_writes_added",
        "runtime_integrations_added",
    ]:
        assert non_goals[key] is False


def test_coordination_foundation_alignment_documents_config_and_secrets_policy() -> None:
    data = load_alignment()

    assert data["configuration_alignment"]["config_directory_required_now"] is False
    assert data["configuration_alignment"]["env_example_required_now"] is False
    assert data["configuration_alignment"]["production_runtime_config_added"] is False

    assert data["secrets_alignment"]["secrets_required_now"] is False
    assert data["secrets_alignment"]["secrets_check"] == "not_applicable"
    assert data["secrets_alignment"]["real_secrets_committed"] is False


def test_coordination_foundation_alignment_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "OK: Library coordination foundation alignment validates" in result.stdout
```

## Related test

**Path:** `tests/coordination/test_reference_consumption_pilot.py`
**SHA256:** `cc3d89a283c2b175f20e8b7655bee801b4fd8564634ec7ba22a84cc010a76e71`

```python
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = (
    ROOT
    / "scripts"
    / "reference_consumption"
    / "validate_reference_consumption_pilot.py"
)
EXAMPLES = (
    ROOT
    / "examples"
    / "reference_consumption"
    / "library_reference_consumption_examples.yaml"
)
SCHEMA = (
    ROOT
    / "schemas"
    / "reference_consumption"
    / "library_reference_consumption.schema.yaml"
)
DOC = ROOT / "docs" / "architecture" / "reference_consumption_pilot.md"


def run_validator(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )


def load_examples() -> dict:
    data = yaml.safe_load(EXAMPLES.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def test_reference_consumption_files_exist() -> None:
    assert SCRIPT.exists()
    assert EXAMPLES.exists()
    assert SCHEMA.exists()
    assert DOC.exists()


def test_reference_consumption_validator_passes() -> None:
    result = run_validator()

    assert "OK: Library reference consumption pilot validates" in result.stdout


def test_reference_consumption_preview_renders() -> None:
    result = run_validator("--preview")

    assert "ForPrint Library Reference Consumption Pilot v0.3" in result.stdout
    assert "Consumer: calculator_engine" in result.stdout
    assert "product_service.business_card.standard" in result.stdout
    assert "no semantic redefinition" in result.stdout


def test_valid_payloads_are_present() -> None:
    data = load_examples()
    valid_ids = {item["id"] for item in data["valid_consumer_payloads"]}

    assert "calculator_pricing_context_reference" in valid_ids
    assert "telegram_channel_hint_reference" in valid_ids
    assert "operational_registry_foreign_reference" in valid_ids


def test_invalid_payloads_are_present() -> None:
    data = load_examples()
    invalid_ids = {item["id"] for item in data["invalid_consumer_payloads"]}

    assert "invalid_unknown_library_reference_id" in invalid_ids
    assert "invalid_consumer_redefines_library_semantics" in invalid_ids
    assert "invalid_consumer_runtime_ownership" in invalid_ids


def test_valid_payloads_use_known_reference_contract_ids() -> None:
    data = load_examples()

    reference_ids = {
        item["library_owned_reference"]["reference_id"]
        for item in data["valid_consumer_payloads"]
    }

    assert "product_service.business_card.standard" in reference_ids
    assert "template.business_card.90x50" in reference_ids
    assert "material.paper.mondi_color_copy_300gsm" in reference_ids


def test_invalid_payloads_document_expected_errors() -> None:
    data = load_examples()

    for payload in data["invalid_consumer_payloads"]:
        assert payload["expected_error_contains"]
```

## Related test

**Path:** `tests/coordination/test_reference_consumption_pilot_closure.py`
**SHA256:** `cd0bc6992d053da4eaa677e30fdf181637d4b33f7ba155f96606cfba9a400369`

```python
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]

REPORT_ID = "2026-07-08__forprint_library__report__reference-consumption-pilot-v0-3"
PROMPT_ID = "library_reference_consumption_pilot_v0_3"
IMPLEMENTATION_COMMIT = "7e000cb"

REPORT = ROOT / "coordination" / "reports" / "completion" / f"{REPORT_ID}.md"
REPORTS_INDEX = ROOT / "coordination" / "reports" / "index.yaml"
STATUS_YAML = ROOT / "coordination" / "status" / "current_status.yaml"
STATUS_MD = ROOT / "coordination" / "status" / "current_status.md"
NEXT_QUESTIONS = ROOT / "coordination" / "status" / "next_questions_for_blueprint.md"


def load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def test_reference_consumption_completion_report_exists() -> None:
    assert REPORT.exists()

    text = REPORT.read_text(encoding="utf-8")

    assert "Library Reference Consumption Pilot v0.3" in text
    assert PROMPT_ID in text
    assert IMPLEMENTATION_COMMIT in text
    assert "Library reference consumption pilot" in text
    assert "completed_pending_blueprint_review" in text
    assert "No Configurable Product Workbench" in text
    assert "No Blueprint repository writes" in text


def test_reference_consumption_report_index_updated() -> None:
    data = load_yaml(REPORTS_INDEX)

    reports = data["completion_reports"]
    matching = [item for item in reports if item["id"] == REPORT_ID]

    assert len(matching) == 1

    report = matching[0]
    assert report["module_id"] == "forprint_library"
    assert report["type"] == "completion_report"
    assert report["status"] == "completed_pending_blueprint_review"
    assert report["related_prompt_id"] == PROMPT_ID
    assert report["implementation_commit"] == IMPLEMENTATION_COMMIT


def test_reference_consumption_commit_record_indexed() -> None:
    data = load_yaml(REPORTS_INDEX)

    commit_reports = data["commit_reports"]
    matching = [
        item
        for item in commit_reports
        if item["id"] == "forprint_library_reference_consumption_pilot_commit_7e000cb"
    ]

    assert len(matching) == 1

    commit = matching[0]
    assert commit["module_id"] == "forprint_library"
    assert commit["type"] == "commit_record"
    assert commit["status"] == "pushed"
    assert commit["commit"] == IMPLEMENTATION_COMMIT
    assert commit["related_prompt_id"] == PROMPT_ID


def test_reference_consumption_current_status_updated() -> None:
    data = load_yaml(STATUS_YAML)

    checkpoint = data["reference_consumption_pilot_v0_3"]

    assert checkpoint["prompt_id"] == PROMPT_ID
    assert checkpoint["status"] in {
        "completed_pending_blueprint_review",
        "accepted_by_blueprint",
    }
    assert checkpoint["implementation_commit"] == "7e000cb"
    assert checkpoint["completion_report"].endswith(
        "2026-07-08__forprint_library__report__reference-consumption-pilot-v0-3.md"
    )

    assert data["status"] in {
        "reference_consumption_pilot_v0_3_ready_pending_blueprint_review",
        "business_card_skeleton_v0_1_ready_pending_blueprint_review",
        "completed_pending_blueprint_review",
    }


def test_reference_consumption_status_markdown_updated() -> None:
    text = STATUS_MD.read_text(encoding="utf-8")

    assert "Previous completed checkpoints" in text
    assert "reference_consumption_pilot_v0_3" in text
    assert "reference_consumption_pilot_v0_3_ready_pending_blueprint_review" in text


def test_reference_consumption_next_questions_updated() -> None:
    text = NEXT_QUESTIONS.read_text(encoding="utf-8")

    assert "No open questions" in text
    assert "library_configurable_product_workbench_business_card_skeleton_v0_1" in text
    assert "business-card-skeleton-v0-1.md" in text
```

## Related test

**Path:** `tests/integration/test_catalog_projection_readiness.py`
**SHA256:** `fbf94f40f47a3d5fdeb4ab786c145c3ee18a8397a9aa7e37c12d7c37c49b07e3`

```python
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
```

## Related test

**Path:** `tests/integration/test_dictionary_resolver_and_preview.py`
**SHA256:** `7ef53dd40ab55483ac446f8578a7e4cfbf3a33aeeeb8ea8b62abc92a6e36b5b0`

```python
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml
from forprint_library.dictionaries.models import (
    RESOLUTION_ALIAS,
    RESOLUTION_AMBIGUOUS,
    RESOLUTION_DEPRECATED,
    RESOLUTION_EXACT,
    RESOLUTION_UNRESOLVED,
)
from forprint_library.dictionaries.resolver import (
    find_ambiguous_aliases,
    resolve_dictionary_value,
)

ROOT = Path(__file__).resolve().parents[2]


def test_dictionary_resolution_exact_match_works() -> None:
    result = resolve_dictionary_value("source_system", "calculator_engine")

    assert result.status == RESOLUTION_EXACT
    assert result.matched_id == "calculator_engine"
    assert result.matched_by == "id"


def test_dictionary_resolution_alias_match_works() -> None:
    result = resolve_dictionary_value("source_system", "calculator")

    assert result.status == RESOLUTION_ALIAS
    assert result.matched_id == "calculator_engine"
    assert result.matched_by == "alias"


def test_unknown_value_returns_unresolved() -> None:
    result = resolve_dictionary_value("source_system", "not_existing_source")

    assert result.status == RESOLUTION_UNRESOLVED
    assert result.matched_id is None
    assert result.candidates == []


def test_deprecated_value_returns_deprecated_reference() -> None:
    result = resolve_dictionary_value(
        "reference_resolution_status",
        "deprecated_reference",
    )

    assert result.status == RESOLUTION_DEPRECATED
    assert result.matched_id == "deprecated_reference"


def test_ambiguous_alias_returns_manual_review() -> None:
    dictionary = {
        "dictionary_group": "demo_group",
        "entries": [
            {
                "id": "first_demo_value",
                "status": "active",
                "aliases": ["shared_alias"],
            },
            {
                "id": "second_demo_value",
                "status": "active",
                "aliases": ["shared_alias"],
            },
        ],
    }

    result = resolve_dictionary_value(
        "demo_group",
        "shared_alias",
        dictionary=dictionary,
    )

    assert result.status == RESOLUTION_AMBIGUOUS
    assert result.matched_id is None
    assert result.candidates == [
        "first_demo_value",
        "second_demo_value",
    ]


def test_ambiguous_aliases_can_be_reported() -> None:
    dictionary = {
        "dictionary_group": "demo_group",
        "entries": [
            {
                "id": "first_demo_value",
                "status": "active",
                "aliases": ["shared_alias"],
            },
            {
                "id": "second_demo_value",
                "status": "active",
                "aliases": ["shared_alias"],
            },
        ],
    }

    ambiguous = find_ambiguous_aliases(dictionary)

    assert ambiguous == {"shared_alias": ["first_demo_value", "second_demo_value"]}


def test_dictionary_resolution_examples_exist() -> None:
    path = ROOT / "examples" / "dictionaries" / "demo_dictionary_resolution_cases.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))

    example_ids = {item["id"] for item in data["examples"]}

    for expected_id in [
        "exact_id_resolution",
        "alias_resolution",
        "unknown_value",
        "deprecated_value",
        "ambiguous_alias",
        "display_label_usage",
    ]:
        assert expected_id in example_ids


def test_demo_shared_operational_dictionary_exists() -> None:
    path = ROOT / "examples" / "dictionaries" / "demo_shared_operational_dictionary.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))

    assert data["metadata"]["owner_module"] == "forprint_library"
    assert "demo_groups" in data


def test_dictionary_preview_renders_key_sections() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/preview_shared_operational_dictionaries.py",
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )

    output = completed.stdout.casefold()

    assert completed.returncode == 0
    for phrase in [
        "dictionary groups",
        "source systems",
        "entity types",
        "order / workflow statuses",
        "payment / material statuses",
        "alert statuses",
        "units",
        "resolution examples",
    ]:
        assert phrase in output
```

# Part D — Local L0/L1 analysis context

## Local analysis context

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

## Local analysis context

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

## Local analysis context

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

## Local analysis context

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

# Part E — Blueprint authority / Human Intent / Stage 1 context

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

**Path:** `tmp/module_knowledge_analysis/forprint_library/01_domain_semantics_catalog/l2_packet/context/blueprint_roadmap_subsets/portfolio_full_horizon_target_states_v0_1__forprint_library_subset.yaml`
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

**Path:** `tmp/module_knowledge_analysis/forprint_library/01_domain_semantics_catalog/l2_packet/context/blueprint_roadmap_subsets/portfolio_module_roadmap_approval_matrix_v0_1__forprint_library_subset.yaml`
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

The machine-readable packet manifest contains the complete provenance ledger.

Evidence item count: **52**
