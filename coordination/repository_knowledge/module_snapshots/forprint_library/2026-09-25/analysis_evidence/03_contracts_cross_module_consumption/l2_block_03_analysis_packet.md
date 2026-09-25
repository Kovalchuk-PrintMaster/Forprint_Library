# ForPrint Library — L2 Block 03 Analysis Packet

**Module:** `forprint_library`
**Block:** `03_contracts_cross_module_consumption`

This packet is evidence for analysis only. It is not implementation authority.

## Evidence boundaries

- Primary implementation population comes from the human-reviewed L1 block manifest.
- Related tests come only from L1 secondary relationships.
- Block 01 and Block 02 reports are supporting cross-block evidence only.
- Blueprint material is authority/planning/provenance context, not implementation proof.
- Historical evidence remains provenance unless current implementation confirms it.

# Part A — Block manifest

## L1 Block 03 manifest

**Path:** `tmp/module_knowledge_analysis/forprint_library/03_contracts_cross_module_consumption/manifest.yaml`
**SHA256:** `742450d5f4a753a89ff65ea1005231ad6f795e03f38bfa12a1b61ae1f8dbd7aa`

```yaml
schema_version: forprint_module_knowledge_analysis_block_manifest_v0_1
module_id: forprint_library
stage: L1_INVENTORY_AND_SEGMENTATION
block_id: 03_contracts_cross_module_consumption
title: Contracts and cross-module consumption
purpose: Library-to-consumer contracts, Calculator input, reference consumption, version/adoption semantics and cross-module
  handoffs.
mutation_performed: false
selection_method: L1 deterministic classification plus bounded human review correction v0.1; classification remains preliminary
  until L2 analysis
file_count: 16
source_paths:
- app/forprint_library/calculator_input/__init__.py
- app/forprint_library/calculator_input/contract.py
- app/forprint_library/contracts/models.py
- schemas/calculator_input/calculator_input_envelope.schema.yaml
- schemas/reference_consumption/library_reference_consumption.schema.yaml
- schemas/reference_contract/library_reference.schema.yaml
- scripts/calculator_input/validate_calculator_input_contract.py
- scripts/coordination/export_business_card_skeleton_closure.py
- scripts/coordination/export_make_first_semantic_readiness_closure.py
- scripts/coordination/export_reference_consumption_pilot_closure.py
- scripts/coordination/export_reference_contract_foundation_closure.py
- scripts/coordination/validate_completion_packet.py
- scripts/product_workbench/preview_business_card_product.py
- scripts/product_workbench/validate_business_card_product.py
- scripts/reference_consumption/validate_reference_consumption_pilot.py
- scripts/validate_semantic_reference_readiness.py
primary_capability_hypotheses:
- Library-to-Calculator reference input
- cross-module reference consumption
- versioned semantic contract surfaces
cross_block_dependencies: []
documents_present: []
tests_present: []
generated_outputs_present: []
legacy_candidates_present:
- scripts/coordination/export_business_card_skeleton_closure.py
- scripts/coordination/export_reference_consumption_pilot_closure.py
unknowns: []
confidence: medium
```

# Part B — Primary source population

## Primary source

**Path:** `app/forprint_library/calculator_input/__init__.py`
**SHA256:** `a479c324f4121a01d5859ed7d18972a22eab62edf24ed3bc1c2e00898279fc58`

```python
"""Calculator input projection contract for ForPrint Library.

This package exposes a read-only, deterministic Library projection for downstream
Calculator consumption. It does not implement prices or import Calculator code.
"""

from forprint_library.calculator_input.contract import (
    CalculatorInputContractError,
    CalculatorInputEnvelope,
    CalculatorInputErrorType,
    CalculatorReferenceIds,
    ValidationSnapshot,
    build_calculator_input,
)

__all__ = [
    "CalculatorInputContractError",
    "CalculatorInputEnvelope",
    "CalculatorInputErrorType",
    "CalculatorReferenceIds",
    "ValidationSnapshot",
    "build_calculator_input",
]
```

## Primary source

**Path:** `app/forprint_library/calculator_input/contract.py`
**SHA256:** `c3467f38d1747ce17cfeab77f3b32faf7cecf4a031eb14c692ca1c73b3adedd8`

```python
"""Read-only Calculator input projection contract.

The contract converts a validated Library configurable product selection into a
deterministic, schema-versioned envelope that Calculator can consume as reference
input. It intentionally contains no prices, formulas, costs, margins, taxes,
discounts, totals, stock truth, order writes or external integration calls.
"""

from __future__ import annotations

import copy
import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from types import MappingProxyType
from typing import Any

import yaml

SUPPORTED_PRODUCT_ID = "product.business_card"
CALCULATOR_INPUT_SCHEMA_VERSION = "calculator_input_envelope_v0_1"
VALIDATION_SNAPSHOT_SCHEMA_VERSION = "calculator_input_validation_snapshot_v0_1"
ERROR_SCHEMA_VERSION = "calculator_input_error_v0_1"

ROOT = Path(__file__).resolve().parents[3]
BUSINESS_CARD_PATH = ROOT / "catalog" / "configurable_products" / "business_card.yaml"

REQUIRED_PARAMETERS = (
    "size",
    "sides",
    "material_ref",
    "print_mode_ref",
    "quantity",
)

FORBIDDEN_MONETARY_KEYS = {
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


class CalculatorInputErrorType(StrEnum):
    """Stable public error taxonomy for Calculator input projection."""

    UNKNOWN_PRODUCT = "unknown_product"
    INVALID_CONFIGURATION = "invalid_configuration"
    MISSING_REQUIRED_PARAMETER = "missing_required_parameter"
    INVALID_REFERENCE = "invalid_reference"
    UNSUPPORTED_PROJECTION_VERSION = "unsupported_projection_version"
    INTERNAL_CONTRACT_ERROR = "internal_contract_error"


class CalculatorInputContractError(ValueError):
    """Safe typed error for Calculator input contract consumers."""

    def __init__(
        self,
        error_type: CalculatorInputErrorType,
        message: str,
        *,
        field_path: str | None = None,
        details: Mapping[str, object] | None = None,
    ) -> None:
        super().__init__(message)
        self.error_type = error_type
        self.message = message
        self.field_path = field_path
        self.details = dict(details or {})

    def to_public_error(self) -> dict[str, object]:
        """Return a stable, stack-trace-free public error payload."""

        return {
            "schema_version": ERROR_SCHEMA_VERSION,
            "error_type": self.error_type.value,
            "message": self.message,
            "field_path": self.field_path,
            "details": copy.deepcopy(self.details),
        }


@dataclass(frozen=True)
class CalculatorReferenceIds:
    """Reference identifiers projected for Calculator input context."""

    product_id: str
    size_id: str
    sides_id: str
    material_ref: Mapping[str, object]
    print_mode_ref: Mapping[str, object]
    finishing_refs: tuple[Mapping[str, object], ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "product_id": self.product_id,
            "size_id": self.size_id,
            "sides_id": self.sides_id,
            "material_ref": _unfreeze(self.material_ref),
            "print_mode_ref": _unfreeze(self.print_mode_ref),
            "finishing_refs": [_unfreeze(ref) for ref in self.finishing_refs],
        }


@dataclass(frozen=True)
class ValidationSnapshot:
    """Explicit validation result included in successful envelopes."""

    schema_version: str
    valid: bool
    errors: tuple[Mapping[str, object], ...]
    warnings: tuple[Mapping[str, object], ...]
    required_parameters: tuple[str, ...]
    normalization_notes: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "valid": self.valid,
            "errors": [_unfreeze(error) for error in self.errors],
            "warnings": [_unfreeze(warning) for warning in self.warnings],
            "required_parameters": list(self.required_parameters),
            "normalization_notes": list(self.normalization_notes),
        }


@dataclass(frozen=True)
class CalculatorInputEnvelope:
    """Versioned deterministic envelope for Calculator-ready Library input."""

    schema_version: str
    product_id: str
    configuration_id: str
    normalized_parameters: Mapping[str, object]
    reference_ids: CalculatorReferenceIds
    validation_snapshot: ValidationSnapshot

    def to_dict(self) -> dict[str, object]:
        """Serialize with stable field ordering."""

        return {
            "schema_version": self.schema_version,
            "product_id": self.product_id,
            "configuration_id": self.configuration_id,
            "normalized_parameters": _unfreeze(self.normalized_parameters),
            "reference_ids": self.reference_ids.to_dict(),
            "validation_snapshot": self.validation_snapshot.to_dict(),
        }


def build_calculator_input(
    product_id: str,
    configuration: Mapping[str, object],
    *,
    schema_version: str | None = None,
) -> CalculatorInputEnvelope:
    """Build a read-only Calculator input envelope from Library references.

    The function is deterministic, does not mutate input mappings, performs no
    writes, imports no Calculator code, and makes no network calls.
    """

    requested_schema_version = schema_version or CALCULATOR_INPUT_SCHEMA_VERSION

    if requested_schema_version != CALCULATOR_INPUT_SCHEMA_VERSION:
        raise CalculatorInputContractError(
            CalculatorInputErrorType.UNSUPPORTED_PROJECTION_VERSION,
            "Unsupported Calculator input projection schema version.",
            field_path="schema_version",
            details={
                "requested_schema_version": requested_schema_version,
                "supported_schema_version": CALCULATOR_INPUT_SCHEMA_VERSION,
            },
        )

    if product_id != SUPPORTED_PRODUCT_ID:
        raise CalculatorInputContractError(
            CalculatorInputErrorType.UNKNOWN_PRODUCT,
            "Unsupported product for Calculator input projection.",
            field_path="product_id",
            details={"product_id": product_id},
        )

    source_configuration = copy.deepcopy(dict(configuration))
    card = _load_business_card()

    normalized = _normalize_business_card_configuration(card, source_configuration)
    reference_ids = CalculatorReferenceIds(
        product_id=product_id,
        size_id=str(normalized["size"]),
        sides_id=str(normalized["sides"]),
        material_ref=_freeze(normalized["material_ref"]),
        print_mode_ref=_freeze(normalized["print_mode_ref"]),
        finishing_refs=tuple(_freeze(ref) for ref in normalized["finishing_refs"]),
    )

    validation_snapshot = ValidationSnapshot(
        schema_version=VALIDATION_SNAPSHOT_SCHEMA_VERSION,
        valid=True,
        errors=(),
        warnings=(),
        required_parameters=REQUIRED_PARAMETERS,
        normalization_notes=(
            "Output field order is stable.",
            "finishing_refs are sorted by catalog and id.",
            "Optional artwork_source is included only when supplied.",
            "No monetary, pricing, stock, production or runtime fields are projected.",
        ),
    )

    configuration_id = _build_configuration_id(
        product_id=product_id,
        schema_version=requested_schema_version,
        normalized_parameters=normalized,
        reference_ids=reference_ids,
    )

    envelope = CalculatorInputEnvelope(
        schema_version=requested_schema_version,
        product_id=product_id,
        configuration_id=configuration_id,
        normalized_parameters=_freeze(normalized),
        reference_ids=reference_ids,
        validation_snapshot=validation_snapshot,
    )

    _assert_no_forbidden_monetary_keys(envelope.to_dict())
    return envelope


def _load_business_card() -> dict[str, Any]:
    data = yaml.safe_load(BUSINESS_CARD_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INTERNAL_CONTRACT_ERROR,
            "Business card product card must be a mapping.",
            field_path="catalog/configurable_products/business_card.yaml",
        )

    if data.get("product_id") != SUPPORTED_PRODUCT_ID:
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INTERNAL_CONTRACT_ERROR,
            "Business card product card has unexpected product_id.",
            field_path="product_id",
            details={"product_id": data.get("product_id")},
        )

    return data


def _normalize_business_card_configuration(
    card: Mapping[str, object],
    configuration: Mapping[str, object],
) -> dict[str, object]:
    missing = [key for key in REQUIRED_PARAMETERS if key not in configuration]
    if missing:
        raise CalculatorInputContractError(
            CalculatorInputErrorType.MISSING_REQUIRED_PARAMETER,
            "Missing required Calculator input parameter.",
            field_path=missing[0],
            details={"missing_parameters": missing},
        )

    size = _normalize_choice(card, "size", configuration["size"])
    sides = _normalize_choice(card, "sides", configuration["sides"])
    material_ref = _normalize_reference(card, "material_ref", configuration["material_ref"])
    print_mode_ref = _normalize_reference(card, "print_mode_ref", configuration["print_mode_ref"])
    quantity = _normalize_quantity(configuration["quantity"])
    finishing_refs = _normalize_finishing_refs(card, configuration.get("finishing_refs", []))
    artwork_source = _normalize_optional_artwork_source(card, configuration.get("artwork_source"))

    _validate_sides_and_print_mode_match(card, sides, print_mode_ref)

    normalized: dict[str, object] = {
        "size": size,
        "sides": sides,
        "material_ref": material_ref,
        "print_mode_ref": print_mode_ref,
        "quantity": quantity,
        "finishing_refs": finishing_refs,
    }

    if artwork_source is not None:
        normalized["artwork_source"] = artwork_source

    return normalized


def _parameter(card: Mapping[str, object], key: str) -> Mapping[str, object]:
    parameters = card.get("constructor_parameters")
    if not isinstance(parameters, list):
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INTERNAL_CONTRACT_ERROR,
            "Product card constructor_parameters must be a list.",
            field_path="constructor_parameters",
        )

    for parameter in parameters:
        if isinstance(parameter, dict) and parameter.get("key") == key:
            return parameter

    raise CalculatorInputContractError(
        CalculatorInputErrorType.INTERNAL_CONTRACT_ERROR,
        "Product card parameter definition is missing.",
        field_path=f"constructor_parameters.{key}",
        details={"parameter_key": key},
    )


def _normalize_choice(card: Mapping[str, object], parameter_key: str, value: object) -> str:
    if not isinstance(value, str):
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INVALID_CONFIGURATION,
            "Choice parameter must be a string identifier.",
            field_path=parameter_key,
        )

    parameter = _parameter(card, parameter_key)
    allowed = {
        item["id"]
        for item in parameter.get("allowed_values", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }

    if value not in allowed:
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INVALID_CONFIGURATION,
            "Unsupported choice parameter value.",
            field_path=parameter_key,
            details={"value": value, "allowed_values": sorted(allowed)},
        )

    return value


def _normalize_reference(
    card: Mapping[str, object],
    parameter_key: str,
    value: object,
) -> dict[str, str]:
    parameter = _parameter(card, parameter_key)
    expected_catalog = parameter.get("reference_catalog")

    if not isinstance(expected_catalog, str):
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INTERNAL_CONTRACT_ERROR,
            "Reference parameter definition is missing reference_catalog.",
            field_path=f"constructor_parameters.{parameter_key}.reference_catalog",
        )

    if not isinstance(value, Mapping):
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INVALID_REFERENCE,
            "Reference parameter must be a mapping with catalog and id.",
            field_path=parameter_key,
        )

    catalog = value.get("catalog")
    ref_id = value.get("id")

    if catalog != expected_catalog or not isinstance(ref_id, str):
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INVALID_REFERENCE,
            "Reference parameter has invalid catalog or id.",
            field_path=parameter_key,
            details={"expected_catalog": expected_catalog, "value": dict(value)},
        )

    allowed = _allowed_reference_ids(parameter)

    if ref_id not in allowed:
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INVALID_REFERENCE,
            "Reference parameter id is not allowed for this product.",
            field_path=parameter_key,
            details={"reference_id": ref_id, "allowed_refs": sorted(allowed)},
        )

    return {"catalog": expected_catalog, "id": ref_id}


def _normalize_quantity(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INVALID_CONFIGURATION,
            "Quantity must be an integer.",
            field_path="quantity",
        )

    if value < 1:
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INVALID_CONFIGURATION,
            "Quantity must be greater than or equal to 1.",
            field_path="quantity",
            details={"minimum": 1, "value": value},
        )

    return value


def _normalize_finishing_refs(
    card: Mapping[str, object],
    value: object,
) -> list[dict[str, str]]:
    if value is None:
        value = []

    if not isinstance(value, list):
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INVALID_CONFIGURATION,
            "finishing_refs must be a list of references.",
            field_path="finishing_refs",
        )

    normalized = [
        _normalize_reference_value_against_parameter(card, "finishing_refs", item)
        for item in value
    ]

    unique = {(ref["catalog"], ref["id"]): ref for ref in normalized}

    return [unique[key] for key in sorted(unique)]


def _normalize_reference_value_against_parameter(
    card: Mapping[str, object],
    parameter_key: str,
    value: object,
) -> dict[str, str]:
    parameter = _parameter(card, parameter_key)
    expected_catalog = parameter.get("reference_catalog")

    if not isinstance(expected_catalog, str):
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INTERNAL_CONTRACT_ERROR,
            "Reference list parameter definition is missing reference_catalog.",
            field_path=f"constructor_parameters.{parameter_key}.reference_catalog",
        )

    if not isinstance(value, Mapping):
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INVALID_REFERENCE,
            "Reference list item must be a mapping with catalog and id.",
            field_path=parameter_key,
        )

    catalog = value.get("catalog")
    ref_id = value.get("id")

    if catalog != expected_catalog or not isinstance(ref_id, str):
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INVALID_REFERENCE,
            "Reference list item has invalid catalog or id.",
            field_path=parameter_key,
            details={"expected_catalog": expected_catalog, "value": dict(value)},
        )

    allowed = _allowed_reference_ids(parameter)

    if ref_id not in allowed:
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INVALID_REFERENCE,
            "Reference list item is not allowed for this product.",
            field_path=parameter_key,
            details={"reference_id": ref_id, "allowed_refs": sorted(allowed)},
        )

    return {"catalog": expected_catalog, "id": ref_id}


def _normalize_optional_artwork_source(card: Mapping[str, object], value: object) -> str | None:
    if value is None:
        return None

    return _normalize_choice(card, "artwork_source", value)


def _validate_sides_and_print_mode_match(
    card: Mapping[str, object],
    sides: str,
    print_mode_ref: Mapping[str, str],
) -> None:
    parameter = _parameter(card, "sides")

    for allowed_value in parameter.get("allowed_values", []):
        if not isinstance(allowed_value, Mapping):
            continue
        if allowed_value.get("id") != sides:
            continue

        expected_print_mode = allowed_value.get("print_mode_ref")
        if not isinstance(expected_print_mode, Mapping):
            return

        expected_id = expected_print_mode.get("id")
        if print_mode_ref.get("id") != expected_id:
            raise CalculatorInputContractError(
                CalculatorInputErrorType.INVALID_CONFIGURATION,
                "Selected sides and print_mode_ref are inconsistent.",
                field_path="print_mode_ref",
                details={
                    "sides": sides,
                    "expected_print_mode_ref": dict(expected_print_mode),
                    "actual_print_mode_ref": dict(print_mode_ref),
                },
            )
        return


def _allowed_reference_ids(parameter: Mapping[str, object]) -> set[str]:
    return {
        item["id"]
        for item in parameter.get("allowed_refs", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }


def _build_configuration_id(
    *,
    product_id: str,
    schema_version: str,
    normalized_parameters: Mapping[str, object],
    reference_ids: CalculatorReferenceIds,
) -> str:
    canonical = {
        "schema_version": schema_version,
        "product_id": product_id,
        "normalized_parameters": normalized_parameters,
        "reference_ids": reference_ids.to_dict(),
    }

    encoded = json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:16]
    return f"calc_input_{digest}"


def _freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({str(key): _freeze(nested) for key, nested in value.items()})

    if isinstance(value, list | tuple):
        return tuple(_freeze(item) for item in value)

    return copy.deepcopy(value)


def _unfreeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _unfreeze(nested) for key, nested in value.items()}

    if isinstance(value, tuple):
        return [_unfreeze(item) for item in value]

    if isinstance(value, list):
        return [_unfreeze(item) for item in value]

    return copy.deepcopy(value)


def _assert_no_forbidden_monetary_keys(value: object) -> None:
    found = sorted(FORBIDDEN_MONETARY_KEYS.intersection(_iter_keys(value)))
    if found:
        raise CalculatorInputContractError(
            CalculatorInputErrorType.INTERNAL_CONTRACT_ERROR,
            "Calculator input envelope contains forbidden monetary keys.",
            details={"forbidden_keys": found},
        )


def _iter_keys(value: object) -> list[str]:
    if isinstance(value, Mapping):
        keys = list(value)
        for nested in value.values():
            keys.extend(_iter_keys(nested))
        return [str(key) for key in keys]

    if isinstance(value, list | tuple):
        keys: list[str] = []
        for item in value:
            keys.extend(_iter_keys(item))
        return keys

    return []
```

## Primary source

**Path:** `app/forprint_library/contracts/models.py`
**SHA256:** `e0c46c169100c7216028668291abb5db8862021a81e9629a8a66a5a021cf518a`

```python
"""Моделі контрактів forprint_library.

Контракт описує форму взаємодії між модулями, а ContractVersion описує
конкретну версію цього контракту.
"""

from datetime import date
from typing import Any

from forprint_library.core.enums import ChangeLevel, ContractStatus
from pydantic import BaseModel, Field


class Contract(BaseModel):
    """Логічний контракт без прив'язки до конкретної версії."""

    code: str = Field(..., examples=["prepress.job_request"])
    name: str
    domain: str = Field(..., examples=["prepress"])
    description: str = ""
    owner_module: str | None = None


class ContractVersion(BaseModel):
    """Окрема версія контракту."""

    contract_code: str
    version: str = Field(..., examples=["1.0.0"])
    status: ContractStatus = ContractStatus.DRAFT

    # Дати життєвого циклу.
    effective_from: date | None = None
    deprecated_from: date | None = None
    blocked_from: date | None = None

    # Машинна JSON Schema.
    json_schema: dict[str, Any]

    # Людинозрозуміла документація.
    human_description: str = ""
    human_changelog: str = ""

    # Машинний опис змін, який потім читатиме sync_manager.
    machine_changelog: dict[str, Any] = Field(default_factory=dict)
    change_level: ChangeLevel = ChangeLevel.COSMETIC

    # Політики міграції.
    auto_migration_allowed: bool = False
    migration_strategy: str | None = None
    migration_rules: list[dict[str, Any]] = Field(default_factory=list)

    # Історична сумісність.
    archive_read_allowed: bool = True

    def allows_new_input(self) -> bool:
        """Чи можна приймати нові документи по цій версії."""

        return self.status not in {
            ContractStatus.BLOCKED_FOR_INPUT,
            ContractStatus.READ_ONLY,
            ContractStatus.ARCHIVED,
        }

    def allows_archive_read(self) -> bool:
        """Чи можна читати архівні документи по цій версії."""

        return self.archive_read_allowed
```

## Primary source

**Path:** `schemas/calculator_input/calculator_input_envelope.schema.yaml`
**SHA256:** `26146654e9a3317d1792c51ef1cd32d8e1b4d41de160e421b3c1a3b1074e64c8`

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: ForPrint Library Calculator Input Envelope
type: object
required:
  - schema_version
  - product_id
  - configuration_id
  - normalized_parameters
  - reference_ids
  - validation_snapshot
properties:
  schema_version:
    const: calculator_input_envelope_v0_1
  product_id:
    const: product.business_card
  configuration_id:
    type: string
    pattern: ^calc_input_[a-f0-9]{16}$
  normalized_parameters:
    type: object
    required:
      - size
      - sides
      - material_ref
      - print_mode_ref
      - quantity
      - finishing_refs
    additionalProperties: true
  reference_ids:
    type: object
    required:
      - product_id
      - size_id
      - sides_id
      - material_ref
      - print_mode_ref
      - finishing_refs
    additionalProperties: true
  validation_snapshot:
    type: object
    required:
      - schema_version
      - valid
      - errors
      - warnings
      - required_parameters
      - normalization_notes
    additionalProperties: true
additionalProperties: false
```

## Primary source

**Path:** `schemas/reference_consumption/library_reference_consumption.schema.yaml`
**SHA256:** `eb6dde5077a4712f77a992245afdee46159074398ede7fe3bba4001ef71d90f8`

```yaml
$id: forprint_library.reference_consumption.library_reference_consumption_v0_3
title: ForPrint Library Reference Consumption Pilot v0.3
type: object
description: >
  Local schema for example downstream consumer payloads that consume
  Library-owned reference contract identifiers without redefining Library
  semantics or adding runtime ownership to Library.
required:
  - schema_version
  - pilot_id
  - owner_module
  - reference_contract_source
  - valid_consumer_payloads
  - invalid_consumer_payloads
properties:
  schema_version:
    type: string
    const: library_reference_consumption_examples_v0_3
  pilot_id:
    type: string
    const: library_reference_consumption_pilot_v0_3
  owner_module:
    type: string
    const: forprint_library
  description:
    type: string
  reference_contract_source:
    type: object
    required:
      - schema_version
      - path
    properties:
      schema_version:
        type: string
        const: library_reference_v0_2
      path:
        type: string
      note:
        type: string
  valid_consumer_payloads:
    type: array
  invalid_consumer_payloads:
    type: array
additionalProperties: false

consumer_payload_shape:
  required:
    - id
    - description
    - consumer_module
    - consumer_payload_id
    - library_owned_reference
    - consumer_owned_fields
    - foreign_module_references
    - boundary_assertions
  library_owned_reference_required:
    - schema_version
    - reference_type
    - reference_id
    - display_label
    - resolution_status
  allowed_consumer_modules:
    - calculator_engine
    - telegram_bot
    - forprint_operational_registry
    - forprint_accounting_registry_service
    - forprint_prepress_hub
    - forprint_integration_gateway
  forbidden_consumer_fields:
    - canonical_name_override
    - semantic_definition_override
    - library_alias_write
    - library_reference_write
    - final_price
    - price_formula
    - stock_mutation
    - material_write_off
    - order_creation
    - client_creation
    - payment_posting
    - production_runtime_write
    - telegram_runtime_behavior
    - calculator_runtime_integration
    - operational_registry_write
    - one_c_sync
    - one_c_import
```

## Primary source

**Path:** `schemas/reference_contract/library_reference.schema.yaml`
**SHA256:** `06124b7a5d378a4068a5c7d0b41cb9dcd24c249c50a313bf5b8c46906f2165a9`

```yaml
$id: forprint_library.reference_contract.library_reference_v0_2
title: ForPrint Library Reference Contract v0.2
type: object
description: >
  JSON-schema-like local schema for downstream references to Library-owned
  semantic/catalog entities.
required:
  - schema_version
  - reference_type
  - reference_id
  - display_label
  - resolution_status
  - source_module
properties:
  schema_version:
    type: string
    const: library_reference_v0_2
  reference_type:
    type: string
    enum:
      - product_service
      - material
      - operation
      - unit
      - template
      - technical_card
  reference_id:
    type:
      - string
      - "null"
    description: >
      Canonical Library reference id when known. Unknown references may keep
      this field null and preserve alias_input for review.
  display_label:
    type: string
  resolution_status:
    type: string
    enum:
      - library_reference_confirmed
      - library_reference_pending
      - ambiguous_manual_review_required
      - deprecated_reference
      - unknown
  source_module:
    type: string
    enum:
      - calculator_engine
      - forprint_operational_registry
      - forprint_integration_gateway
      - telegram_bot
      - future_forprint_crm
      - forprint_library
  alias_input:
    type:
      - string
      - "null"
  deprecation:
    type: object
    required:
      - is_deprecated
      - replaced_by
      - message
    properties:
      is_deprecated:
        type: boolean
      replaced_by:
        type:
          - string
          - "null"
      message:
        type:
          - string
          - "null"
  manual_review:
    type: object
    required:
      - required
      - reason
    properties:
      required:
        type: boolean
      reason:
        type:
          - string
          - "null"
additionalProperties: false
```

## Primary source

**Path:** `scripts/calculator_input/validate_calculator_input_contract.py`
**SHA256:** `2443f2342b9552f871b0ebb64ae51e9f04b1e82686d16493a922334ef335c8b0`

```python
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "app"))

from forprint_library.calculator_input import (  # noqa: E402
    CalculatorInputContractError,
    CalculatorInputErrorType,
    build_calculator_input,
)

FIXTURE_DIR = ROOT / "examples" / "calculator_input_contract"
SCHEMA_PATH = ROOT / "schemas" / "calculator_input" / "calculator_input_envelope.schema.yaml"

VALID_FIXTURES = {
    "minimal_valid_business_card": "minimal_valid_business_card.yaml",
    "business_card_with_finishing": "business_card_with_finishing.yaml",
    "business_card_with_artwork_source": "business_card_with_artwork_source.yaml",
}

INVALID_FIXTURES = {
    "invalid_missing_material": (
        "invalid_missing_material.yaml",
        CalculatorInputErrorType.MISSING_REQUIRED_PARAMETER,
    ),
    "invalid_print_mode_reference": (
        "invalid_print_mode_reference.yaml",
        CalculatorInputErrorType.INVALID_REFERENCE,
    ),
    "invalid_quantity": (
        "invalid_quantity.yaml",
        CalculatorInputErrorType.INVALID_CONFIGURATION,
    ),
}

FORBIDDEN_KEYS = {
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


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise AssertionError(f"YAML root must be mapping: {path.relative_to(ROOT)}")
    return data


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


def assert_no_forbidden_keys(data: dict[str, Any]) -> None:
    found = sorted(FORBIDDEN_KEYS.intersection(iter_keys(data)))
    if found:
        raise AssertionError(f"Forbidden monetary/pricing keys found: {found}")


def validate_schema_file() -> None:
    schema = load_yaml(SCHEMA_PATH)
    assert schema["title"] == "ForPrint Library Calculator Input Envelope"
    assert schema["properties"]["schema_version"]["const"] == "calculator_input_envelope_v0_1"
    assert schema["properties"]["product_id"]["const"] == "product.business_card"


def validate_valid_fixture(case_id: str, filename: str) -> None:
    fixture = load_yaml(FIXTURE_DIR / filename)
    assert fixture["schema_version"] == "calculator_input_fixture_v0_1"
    assert fixture["case_id"] == case_id
    assert fixture["product_id"] == "product.business_card"

    output = build_calculator_input(
        "product.business_card",
        fixture["input_configuration"],
    ).to_dict()

    assert output == fixture["expected_output"]
    assert_no_forbidden_keys(output)


def validate_invalid_fixture(
    case_id: str,
    filename: str,
    error_type: CalculatorInputErrorType,
) -> None:
    fixture = load_yaml(FIXTURE_DIR / filename)
    assert fixture["schema_version"] == "calculator_input_error_fixture_v0_1"
    assert fixture["case_id"] == case_id
    assert fixture["product_id"] == "product.business_card"

    try:
        build_calculator_input("product.business_card", fixture["input_configuration"])
    except CalculatorInputContractError as exc:
        error = exc.to_public_error()
    else:
        raise AssertionError(f"{case_id}: expected CalculatorInputContractError")

    assert error["error_type"] == error_type.value
    assert error == fixture["expected_error"]
    assert_no_forbidden_keys(error)


def main() -> int:
    validate_schema_file()

    for case_id, filename in VALID_FIXTURES.items():
        validate_valid_fixture(case_id, filename)

    for case_id, (filename, error_type) in INVALID_FIXTURES.items():
        validate_invalid_fixture(case_id, filename, error_type)

    print("OK: Library Calculator input contract validates")
    print(f"Fixtures: {FIXTURE_DIR.relative_to(ROOT)}")
    print(f"Schema: {SCHEMA_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Primary source

**Path:** `scripts/coordination/export_business_card_skeleton_closure.py`
**SHA256:** `10a1f3feaeab8756b6805d7f1188d7cc5bb87eb2bfa3a39aeafc25c8409a1cd6`

```python
from __future__ import annotations

from pathlib import Path
from textwrap import dedent
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]

PROMPT_ID = "library_configurable_product_workbench_business_card_skeleton_v0_1"
PROMPT_TITLE = "Library Configurable Product Workbench v0.1 — Business Card Skeleton"
PROMPT_DATE = "2026-07-11"
REPORT_ID = "2026-07-11__forprint_library__report__business-card-skeleton-v0-1"
IMPLEMENTATION_COMMIT = "b8eb062"
IMPLEMENTATION_COMMIT_MESSAGE = "Add Library business card product skeleton"
BLUEPRINT_PROMPT_PATH = (
    "coordination/outgoing_prompts/forprint_library/approved/"
    "2026-07-11__library__configurable_product_workbench_business_card_skeleton_v0_1.md"
)

REPORT_PATH = ROOT / "coordination" / "reports" / "completion" / f"{REPORT_ID}.md"
REPORTS_INDEX = ROOT / "coordination" / "reports" / "index.yaml"
CURRENT_STATUS_YAML = ROOT / "coordination" / "status" / "current_status.yaml"
CURRENT_STATUS_MD = ROOT / "coordination" / "status" / "current_status.md"
NEXT_QUESTIONS = ROOT / "coordination" / "status" / "next_questions_for_blueprint.md"


def clean_text(text: str) -> str:
    lines = dedent(text).strip().splitlines()
    return "\n".join(line.rstrip() for line in lines) + "\n"


def write_text_clean(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(clean_text(text), encoding="utf-8")


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected YAML mapping: {path.relative_to(ROOT)}")
    return data


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    rendered = yaml.safe_dump(
        data,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    )
    write_text_clean(path, rendered)


def write_completion_report() -> None:
    write_text_clean(
        REPORT_PATH,
        f"""# ForPrint Library completion report

## Prompt

```text
{PROMPT_ID}
Title

{PROMPT_TITLE}

Branch
main
Implementation commit
{IMPLEMENTATION_COMMIT} {IMPLEMENTATION_COMMIT_MESSAGE}
Final module commit hash

The final module commit hash will be the closure/reporting commit that contains
this completion packet. It must be reported back to Blueprint after commit and
push.

Summary

Library Configurable Product Workbench v0.1 — Business Card Skeleton is
implemented inside the Library repository.

The checkpoint adds the first controlled configurable product reference for
business cards / візитки:

product.business_card

The product card is small and intentionally scoped. It describes stable Library
semantics, aliases, constructor parameters, existing Library references,
consumer notes and explicit boundaries without implementing pricing, orders,
production, stock, 1C synchronization, Calculator runtime, Telegram runtime or
Operational Registry writes.

Files changed
catalog/configurable_products/business_card.yaml
schemas/configurable_product.schema.yaml
examples/product_cards/business_card_product_card.yaml
docs/architecture/configurable_product_workbench.md
docs/architecture/business_card_skeleton.md
scripts/product_workbench/validate_business_card_product.py
scripts/product_workbench/preview_business_card_product.py
tests/content/test_business_card_product_card.py
scripts/run_library_checks.py
reports/library_check_report.json
reports/library_check_report.md
coordination/reports/completion/{REPORT_ID}.md
coordination/reports/index.yaml
coordination/status/current_status.yaml
coordination/status/current_status.md
coordination/status/next_questions_for_blueprint.md
Implemented work
Created one configurable product card for product.business_card.
Added Ukrainian and English display names.
Added required aliases and compatibility alias product:business_cards.
Added constructor parameters:
- size
- sides
- material_ref
- print_mode_ref
- quantity
- finishing_refs
- artwork_source

Connected product card references to existing Library catalog IDs.
Added consumer usage examples for:
- Telegram Bot
- Calculator Engine
- Operational Registry

Added schema marker and schema file for configurable product cards.
Added validator and preview script.

Added tests for:
- file existence
- stable product ID
- aliases
- constructor parameters
- Library references
- validator output
- preview output
- forbidden ownership fields

Added check-report visibility for:
- Business card product skeleton
- Business card product preview
Checks passed
business card validator: OK
business card preview: OK
focused tests: 8 passed
make lint: OK
make test: 129 passed
make check-report: OK
make check: OK
make governance-check: OK
make module-validate: OK
git diff --check: OK
Known warnings
Blueprint module directives index is missing/deferred for forprint_library.
This warning existed in the governance flow and did not block Library validation.
Document awareness still reports unseen Blueprint documents;
This is advisory and outside this checkpoint's implementation scope.
Completion packet automation

Generic completion packet automation was not available or was deferred for this
module step.

A checkpoint-specific Library-side exporter generated the required module-side
coordination files inside the Library repository.

No files were written directly into the Blueprint repository.

Explicit boundary confirmation
No full product catalog
No product modeling UI
No production catalog database
No live API
No 1C import
No 1C synchronization
No Calculator integration
No Telegram Bot integration
No Operational Registry write
No CRM write
No Website write
No price calculation
No final price formula
No material write-off logic
No warehouse stock truth
No production task creation
No real client or order data
No production runtime
No Blueprint repository writes
Open questions

No open questions.
""",
)

def update_reports_index() -> None:
    data = load_yaml(REPORTS_INDEX)

    data.setdefault("module_id", "forprint_library")
    data.setdefault("schema_version", "module_reports_index_v0_1")

    reports = data.get("reports")
    if not isinstance(reports, list):
        reports = []

    entry = {
        "id": REPORT_ID,
        "type": "completion_report",
        "prompt_id": PROMPT_ID,
        "title": PROMPT_TITLE,
        "status": "completed_pending_blueprint_review",
        "path": f"coordination/reports/completion/{REPORT_ID}.md",
        "report_file": f"coordination/reports/completion/{REPORT_ID}.md",
        "implementation_commit": IMPLEMENTATION_COMMIT,
        "blueprint_prompt_path": BLUEPRINT_PROMPT_PATH,
        "created_at": PROMPT_DATE,
    }
    reports = [
        report
        for report in reports
        if not (isinstance(report, dict) and report.get("id") == REPORT_ID)
    ]
    reports.append(entry)
    data["reports"] = reports

    write_yaml(REPORTS_INDEX, data)

def update_current_status_yaml() -> None:
    data = load_yaml(CURRENT_STATUS_YAML)

    data["module_id"] = "forprint_library"
    data["status"] = "business_card_skeleton_v0_1_ready_pending_blueprint_review"
    data["current_phase"] = "business_card_skeleton_v0_1"
    data["last_completed_step"] = "library_business_card_skeleton_ready"
    data["updated_at"] = PROMPT_DATE

    data["current_focus"] = [
        (
            "Configurable Product Workbench v0.1 Business Card Skeleton "
            "completed in Library repository."
        ),
        (
            "product.business_card is available as the first controlled "
            "configurable product reference."
        ),
        (
            "Business card product card includes aliases, constructor parameters, "
            "Library references and consumer usage notes."
        ),
        (
            "No pricing, order, production, stock, 1C or downstream runtime "
            "integration was added."
        ),
        "Waiting for Blueprint review.",
    ]

    data.setdefault(
        "make_first_semantic_reference_readiness_v0_1",
        {
            "status": "accepted_by_blueprint",
            "prompt_id": "library_make_first_semantic_reference_readiness_v0_1",
            "implementation_commit": "935e51b",
        },
    )

    data.setdefault(
        "reference_contract_foundation_v0_2",
        {
            "status": "accepted_by_blueprint",
            "prompt_id": "library_reference_contract_foundation_v0_2",
            "implementation_commit": "78bd7e1",
            "completion_commit": "6343f65",
        },
    )

    data.setdefault(
        "coordination_foundation_alignment_v0_1",
        {
            "status": "accepted_by_blueprint",
            "prompt_id": "library_coordination_foundation_alignment_v0_1",
            "implementation_commit": "02e2cad",
            "completion_commit": "8031d3e",
            "commit_report": (
                "coordination/reports/commits/"
                "2026-07-07__forprint_library__commit-report__"
                "coordination-foundation-alignment-v0-1.md"
            ),
        },
    )

    data.setdefault(
        "reference_consumption_pilot_v0_3",
        {
            "status": "accepted_by_blueprint",
            "prompt_id": "library_reference_consumption_pilot_v0_3",
            "implementation_commit": "7e000cb",
            "completion_commit": "15e1c8c",
            "completion_report": (
                "coordination/reports/completion/"
                "2026-07-08__forprint_library__report__"
                "reference-consumption-pilot-v0-3.md"
            ),
        },
    )

    data["configurable_product_workbench_business_card_skeleton_v0_1"] = {
        "status": "completed_pending_blueprint_review",
        "prompt_id": PROMPT_ID,
        "title": PROMPT_TITLE,
        "implementation_commit": IMPLEMENTATION_COMMIT,
        "completion_report": f"coordination/reports/completion/{REPORT_ID}.md",
        "blueprint_prompt_path": BLUEPRINT_PROMPT_PATH,
        "product_id": "product.business_card",
        "added_artifacts": [
            "catalog/configurable_products/business_card.yaml",
            "schemas/configurable_product.schema.yaml",
            "examples/product_cards/business_card_product_card.yaml",
            "docs/architecture/configurable_product_workbench.md",
            "docs/architecture/business_card_skeleton.md",
            "scripts/product_workbench/validate_business_card_product.py",
            "scripts/product_workbench/preview_business_card_product.py",
            "tests/content/test_business_card_product_card.py",
        ],
        "check_report_visibility": [
            "Business card product skeleton",
            "Business card product preview",
        ],
        "validation": {
            "business_card_validator": "OK",
            "business_card_preview": "OK",
            "focused_tests": "8 passed",
            "full_tests": "129 passed",
            "check_report": "OK",
            "make_check": "OK",
            "governance_check": "OK",
            "module_validate": "OK",
            "git_diff_check": "OK",
        },
        "boundaries": {
            "full_product_catalog_added": False,
            "product_modeling_ui_added": False,
            "production_catalog_database_added": False,
            "live_api_added": False,
            "one_c_import_added": False,
            "one_c_synchronization_added": False,
            "calculator_integration_added": False,
            "telegram_bot_integration_added": False,
            "operational_registry_write_added": False,
            "crm_write_added": False,
            "website_write_added": False,
            "price_calculation_added": False,
            "final_price_formula_added": False,
            "material_write_off_added": False,
            "warehouse_stock_truth_added": False,
            "production_task_creation_added": False,
            "real_client_order_data_added": False,
            "production_runtime_added": False,
            "blueprint_repository_written": False,
        },
        "next_recommended_step": "Blueprint review of module-side completion report.",
    }

    write_yaml(CURRENT_STATUS_YAML, data)

def write_current_status_md() -> None:
    write_text_clean(
    CURRENT_STATUS_MD,
    f"""# ForPrint Library Current Status

    Status

    business_card_skeleton_v0_1_ready_pending_blueprint_review

    Current phase

    business_card_skeleton_v0_1

    Last completed step

    library_business_card_skeleton_ready

    Completed prompt
    {PROMPT_ID}
    Product reference
    product.business_card
    Implementation commit
    {IMPLEMENTATION_COMMIT} {IMPLEMENTATION_COMMIT_MESSAGE}
    Completion report
    coordination/reports/completion/{REPORT_ID}.md
    Summary

    Library Configurable Product Workbench v0.1 — Business Card Skeleton is
    completed in the Library repository.

    The checkpoint adds one controlled configurable product reference for business
    cards / візитки. It includes stable Library semantics, aliases, constructor
    parameters, references to existing Library catalog IDs, consumer notes, schema,
    validator, preview and tests.

    Completed artifacts
    catalog/configurable_products/business_card.yaml
    schemas/configurable_product.schema.yaml
    examples/product_cards/business_card_product_card.yaml
    docs/architecture/configurable_product_workbench.md
    docs/architecture/business_card_skeleton.md
    scripts/product_workbench/validate_business_card_product.py
    scripts/product_workbench/preview_business_card_product.py
    tests/content/test_business_card_product_card.py
    scripts/run_library_checks.py
    reports/library_check_report.json
    reports/library_check_report.md
    Validation
    business card validator: OK
    business card preview: OK
    focused tests: 8 passed
    make lint: OK
    make test: 129 passed
    make check-report: OK
    make check: OK
    make governance-check: OK
    make module-validate: OK
    git diff --check: OK
    Boundaries preserved
    No full product catalog
    No product modeling UI
    No production catalog database
    No live API
    No 1C import
    No 1C synchronization
    No Calculator integration
    No Telegram Bot integration
    No Operational Registry write
    No CRM write
    No Website write
    No price calculation
    No final price formula
    No material write-off logic
    No warehouse stock truth
    No production task creation
    No real client or order data
    No production runtime
    No Blueprint repository writes

    Previous completed checkpoints
    make_first_semantic_reference_readiness_v0_1
    - Accepted by Blueprint before the business card skeleton checkpoint.

    reference_contract_foundation_v0_2
    - Accepted by Blueprint before the business card skeleton checkpoint.

    coordination_foundation_alignment_v0_1
    - Makefile was not rewritten.
    - No real secrets or credentials were committed.
    - Coordination foundation alignment remains recorded as a historical checkpoint.

    reference_consumption_pilot_v0_3
    - Reference consumption pilot remains recorded as a historical checkpoint.
    - Previous rolling status: reference_consumption_pilot_v0_3_ready_pending_blueprint_review

    Next step

    Waiting for Blueprint review.

    Blueprint should read the module-side completion report and decide whether to
    accept {PROMPT_ID} or return it for fixes.
    """,
    )

def write_next_questions() -> None:
    write_text_clean(
    NEXT_QUESTIONS,
    f"""# Next questions for Blueprint

    Current checkpoint
    {PROMPT_ID}
    Open questions

    No open questions.

    Review request

    Please review the Library-side completion report:

    coordination/reports/completion/{REPORT_ID}.md

    The module is waiting for Blueprint acceptance or requested fixes.
    """,
    )

def main() -> int:
    write_completion_report()
    update_reports_index()
    update_current_status_yaml()
    write_current_status_md()
    write_next_questions()

    print("OK: Business card skeleton closure exported")
    print(f"Report: {REPORT_PATH.relative_to(ROOT)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

## Primary source

**Path:** `scripts/coordination/export_make_first_semantic_readiness_closure.py`
**SHA256:** `85cc11c0f55f0128ad1de399596110d511f89e0d41777683da64f7782998aa64`

```python
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]

REPORT_ID = (
    "2026-06-25__forprint_library__report__"
    "make-first-semantic-reference-readiness-v0-1"
)
REPORT_PATH = ROOT / "coordination" / "reports" / "completion" / f"{REPORT_ID}.md"

STATUS_YAML = ROOT / "coordination" / "status" / "current_status.yaml"
STATUS_MD = ROOT / "coordination" / "status" / "current_status.md"
REPORTS_INDEX = ROOT / "coordination" / "reports" / "index.yaml"

PROMPT_ID = "make_first_semantic_reference_readiness_v0_1"
BLUEPRINT_COMMIT = "2d49d63"
IMPLEMENTATION_COMMIT = "28fe2d0"

BLUEPRINT_PROMPT_PATH = (
    "/srv/software_development/forprint-project/forprint_system_blueprint/"
    "coordination/outgoing_prompts/forprint_library/approved/"
    "2026-06-23__library__make_first_semantic_reference_readiness_v0_1.md"
)


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
        "make_first_semantic_reference_readiness_v0_1_"
        "ready_pending_blueprint_review"
    )
    data["stage"] = "make_first_semantic_reference_readiness_v0_1_completion"
    data["updated_at"] = "2026-06-25"
    data["current_phase"] = "make_first_semantic_reference_readiness_v0_1"
    data["last_completed_step"] = "make_first_semantic_reference_ready"

    data["current_focus"] = [
        "Blueprint Make Command Standard v0.2 alignment completed",
        "make module-start and make module-validate are passing",
        "minimal semantic/reference readiness checkpoint completed",
        "semantic/reference examples are local non-production fixtures",
        "downstream handoff notes for Calculator and Operational Registry added",
        "completion packet automation is explicitly deferred-safe",
    ]

    data["make_first_semantic_reference_readiness_v0_1"] = {
        "prompt_id": PROMPT_ID,
        "blueprint_prompt_path": BLUEPRINT_PROMPT_PATH,
        "blueprint_commit": BLUEPRINT_COMMIT,
        "implementation_commit": IMPLEMENTATION_COMMIT,
        "completion_report_id": REPORT_ID,
        "completion_report_path": str(REPORT_PATH.relative_to(ROOT)),
        "status": "completed_pending_blueprint_review",
        "makefile_alignment": "done",
        "make_first_targets": "done",
        "module_start": "passing",
        "module_validate": "passing",
        "prompt_read": "passing",
        "report_clean": "passing_without_git_or_venv_scan",
        "semantic_reference_examples": "done",
        "semantic_reference_docs": "done",
        "downstream_handoff_notes": "done",
        "check_report_visibility": "done",
        "tests": "83_passed",
        "completion_packet_automation": "deferred_safe_not_faked",
        "production_catalog_database": "not_implemented",
        "live_api": "not_implemented",
        "runtime_integrations": "not_implemented",
    }

    data["next_recommended_step"] = {
        "status": "wait_for_blueprint_review",
        "recommended_action": (
            "Ask Blueprint to review Library semantic/reference readiness "
            "and decide downstream alignment for Operational Registry "
            "and Calculator."
        ),
        "candidate_followups": [
            "Operational Registry reference projection alignment",
            "Calculator Engine reference input context alignment",
            "Blueprint completion packet contract decision for Library",
            "Library semantic readiness v0.2 after downstream feedback",
        ],
    }

    write_yaml(STATUS_YAML, data)


def update_current_status_md() -> None:
    lines = [
        "# ForPrint Library Current Status",
        "",
        "## Status",
        "",
        "`make_first_semantic_reference_readiness_v0_1_ready_pending_blueprint_review`",
        "",
        "## Current phase",
        "",
        "`make_first_semantic_reference_readiness_v0_1`",
        "",
        "## Last completed step",
        "",
        "`make_first_semantic_reference_ready`",
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
        "Blueprint commit:",
        "",
        "```text",
        f"{BLUEPRINT_COMMIT} Add Library make-first semantic readiness prompt",
        "```",
        "",
        "## Implementation commit",
        "",
        "```text",
        f"{IMPLEMENTATION_COMMIT} Align Library make-first semantic readiness workflow",
        "```",
        "",
        "## Completed",
        "",
        "- Blueprint Make Command Standard v0.2 alignment.",
        "- `make module-start`.",
        "- `make module-validate`.",
        "- `make prompt-read`.",
        "- `make blueprint-sync`.",
        "- `make report-clean`.",
        "- Minimal semantic/reference readiness examples.",
        "- Architecture docs for semantic readiness.",
        "- Downstream reference handoff notes.",
        "- Check-report visibility for semantic readiness.",
        "- Tests for Makefile targets and semantic readiness.",
        "",
        "## Validation result",
        "",
        "```text",
        "ruff: OK",
        "semantic validator: OK",
        "semantic tests: 4 passed",
        "make test: 83 passed",
        "check-report: OK",
        "module-validate: OK",
        "report-clean: OK",
        "```",
        "",
        "## Completion packet automation",
        "",
        "Completion packet automation is deferred-safe.",
        "",
        "It is not faked.",
        "",
        "Current targets:",
        "",
        "```text",
        "completion-packet-validate",
        "completion-packet-apply",
        "completion-packet-check",
        "```",
        "",
        "## Boundaries",
        "",
        "Library remains the canonical semantic/catalog authority.",
        "",
        "Library does not own:",
        "",
        "```text",
        "operational order registry",
        "client database",
        "payment/accounting truth",
        "warehouse stock truth",
        "CRM workflow engine",
        "Telegram runtime adapter",
        "Calculator pricing engine",
        "production runtime controller",
        "1C sync/write",
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
        "Wait for Blueprint review and downstream alignment decision.",
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
            "blueprint_commit": BLUEPRINT_COMMIT,
            "implementation_commit": IMPLEMENTATION_COMMIT,
            "created_at": "2026-06-25",
        },
    )

    commit_reports = ensure_list(data, "commit_reports")
    upsert_by_id(
        commit_reports,
        {
            "id": "forprint_library_make_first_semantic_readiness_commit_28fe2d0",
            "module_id": "forprint_library",
            "type": "commit_report",
            "status": "pushed",
            "commit": IMPLEMENTATION_COMMIT,
            "message": "Align Library make-first semantic readiness workflow",
            "related_prompt_id": PROMPT_ID,
            "created_at": "2026-06-25",
        },
    )

    write_yaml(REPORTS_INDEX, data)


def write_completion_report() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# ForPrint Library Make-First Semantic Reference Readiness v0.1",
        "",
        "## Completion Report",
        "",
        f"Report ID: `{REPORT_ID}`",
        "",
        "Module: `forprint_library`",
        "",
        "Status: `completed_pending_blueprint_review`",
        "",
        "Date: `2026-06-25`",
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
        "Blueprint commit:",
        "",
        "```text",
        f"{BLUEPRINT_COMMIT} Add Library make-first semantic readiness prompt",
        "```",
        "",
        "## Implementation commit",
        "",
        "```text",
        f"{IMPLEMENTATION_COMMIT} Align Library make-first semantic readiness workflow",
        "```",
        "",
        "Push status: `pushed to origin/main`",
        "",
        "## Changed files",
        "",
        "```text",
        "Makefile",
        "coordination/prompts/active/",
        "coordination/standards/blueprint_standards_available_snapshot.txt",
        "docs/architecture/downstream_reference_contract_notes.md",
        "docs/architecture/semantic_reference_readiness.md",
        "examples/semantic_reference_preview.yaml",
        "reports/library_check_report.json",
        "reports/library_check_report.md",
        "scripts/make_first_workflow.py",
        "scripts/run_library_checks.py",
        "scripts/validate_semantic_reference_readiness.py",
        "tests/contract/test_make_first_workflow_targets.py",
        "tests/contract/test_semantic_reference_readiness.py",
        "```",
        "",
        "## Makefile targets added or aligned",
        "",
        "```text",
        "blueprint-instruction-list",
        "blueprint-instruction-check",
        "blueprint-instruction-sync",
        "blueprint-instruction",
        "blueprint-standards-list",
        "blueprint-standards-check",
        "blueprint-standards-sync",
        "blueprint-standards",
        "blueprint-prompts-list",
        "blueprint-prompts-check",
        "blueprint-prompts-sync",
        "blueprint-prompts",
        "prompt-read",
        "blueprint-sync",
        "module-start",
        "module-sync",
        "module-validate",
        "module-finish",
        "report-clean",
        "completion-packet-validate",
        "completion-packet-apply",
        "completion-packet-check",
        "```",
        "",
        "## Semantic/reference readiness files",
        "",
        "```text",
        "docs/architecture/semantic_reference_readiness.md",
        "docs/architecture/downstream_reference_contract_notes.md",
        "examples/semantic_reference_preview.yaml",
        "scripts/validate_semantic_reference_readiness.py",
        "tests/contract/test_semantic_reference_readiness.py",
        "```",
        "",
        "## Semantic/reference readiness summary",
        "",
        "The checkpoint adds a minimal local semantic/reference readiness layer.",
        "",
        "It includes examples for:",
        "",
        "```text",
        "product_service.business_card.standard",
        "material.paper.mondi_color_copy_300gsm",
        "operation.print.digital_color",
        "template.business_card.90x50",
        "```",
        "",
        "It documents canonical ID usage, alias handling, ambiguous names,",
        "unresolved references, downstream handoff and ownership boundaries.",
        "",
        "## Downstream handoff",
        "",
        "Calculator Engine may use canonical Library IDs as input context.",
        "",
        "Operational Registry may store canonical IDs as projections.",
        "",
        "No downstream module should silently invent new Library IDs.",
        "",
        "## Check-report visibility",
        "",
        "The check report now includes:",
        "",
        "```text",
        "Make-first workflow alignment",
        "Blueprint prompt visibility",
        "Blueprint standards visibility",
        "Semantic reference readiness",
        "```",
        "",
        "All rows are passing.",
        "",
        "## Validation results",
        "",
        "```text",
        "ruff: OK",
        "semantic validator: OK",
        "semantic tests: 4 passed",
        "make test: 83 passed",
        "check-report: OK",
        "module-validate: OK",
        "report-clean: OK",
        "```",
        "",
        "## Completion packet automation",
        "",
        "Completion packet automation is not implemented as a real contract yet.",
        "",
        "It is explicitly deferred-safe and not faked.",
        "",
        "Current targets:",
        "",
        "```text",
        "completion-packet-validate",
        "completion-packet-apply",
        "completion-packet-check",
        "```",
        "",
        "## Boundaries confirmed",
        "",
        "This checkpoint does not implement:",
        "",
        "```text",
        "production catalog database",
        "live API",
        "CRM integration",
        "Telegram integration",
        "Operational Registry write",
        "Calculator pricing logic",
        "warehouse stock logic",
        "accounting/payment logic",
        "1C sync/write",
        "automatic posting",
        "production runtime service",
        "```",
        "",
        "Library remains responsible for semantic/catalog authority,",
        "canonical meanings, aliases, examples and handoff notes.",
        "",
        "## Blueprint review request",
        "",
        "Blueprint should review this checkpoint and decide:",
        "",
        "1. Whether Operational Registry should map local projections to Library.",
        "2. Whether Calculator should consume IDs as input context.",
        "3. Whether Library needs a formal completion packet contract.",
        "4. Whether semantic/reference readiness should proceed to v0.2.",
        "",
        "## Recommended next step",
        "",
        "Wait for Blueprint review.",
        "",
        "Suggested next directive:",
        "",
        "```text",
        "Review ForPrint Library semantic reference readiness v0.1.",
        "Issue downstream alignment guidance for Operational Registry.",
        "Issue downstream alignment guidance for Calculator Engine.",
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

**Path:** `scripts/coordination/export_reference_consumption_pilot_closure.py`
**SHA256:** `3a726ec6f7fd9470a5a3daa000b949e262d200418e4199c9f35df048c5023bc4`

```python
from __future__ import annotations

from pathlib import Path
from textwrap import dedent
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]

PROMPT_ID = "library_reference_consumption_pilot_v0_3"
PROMPT_TITLE = "Library Reference Consumption Pilot v0.3"
IMPLEMENTATION_COMMIT = "7e000cb"
IMPLEMENTATION_COMMIT_MESSAGE = "Add Library reference consumption pilot"

REPORT_ID = "2026-07-08__forprint_library__report__reference-consumption-pilot-v0-3"
REPORT_PATH = (
    ROOT
    / "coordination"
    / "reports"
    / "completion"
    / f"{REPORT_ID}.md"
)

REPORT_INDEX_PATH = ROOT / "coordination" / "reports" / "index.yaml"
CURRENT_STATUS_YAML = ROOT / "coordination" / "status" / "current_status.yaml"
CURRENT_STATUS_MD = ROOT / "coordination" / "status" / "current_status.md"
NEXT_QUESTIONS = ROOT / "coordination" / "status" / "next_questions_for_blueprint.md"

BLUEPRINT_PROMPT_PATH = (
    "/srv/software_development/forprint-project/forprint_system_blueprint/"
    "coordination/outgoing_prompts/forprint_library/approved/"
    "2026-07-08__library__reference_consumption_pilot_v0_3.md"
)

def clean_text(text: str) -> str:
    """Remove common indentation, trailing whitespace and keep one EOF newline."""
    lines = dedent(text).strip().splitlines()
    return "\n".join(line.rstrip() for line in lines) + "\n"

def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if data is None:
        return {}

    if not isinstance(data, dict):
        raise AssertionError(f"YAML root must be a mapping: {path.relative_to(ROOT)}")

    return data


def write_text_clean(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(clean_text(text))

def write_yaml(path: Path, data: dict[str, Any]) -> None:
    rendered = yaml.safe_dump(
        data,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    )
    write_text_clean(path, rendered)


def upsert_report_index() -> None:
    data = load_yaml(REPORT_INDEX_PATH)

    data["module_id"] = "forprint_library"
    data["index_type"] = "coordination_reports"
    data["updated_at"] = "2026-07-08"

    completion_reports = data.setdefault("completion_reports", [])
    if not isinstance(completion_reports, list):
        raise AssertionError("completion_reports must be a list")

    completion_reports[:] = [
        item
        for item in completion_reports
        if not isinstance(item, dict) or item.get("id") != REPORT_ID
    ]

    completion_reports.append(
        {
            "id": REPORT_ID,
            "module_id": "forprint_library",
            "type": "completion_report",
            "status": "completed_pending_blueprint_review",
            "path": f"coordination/reports/completion/{REPORT_ID}.md",
            "related_prompt_id": PROMPT_ID,
            "implementation_commit": IMPLEMENTATION_COMMIT,
            "created_at": "2026-07-08",
        }
    )

    commit_reports = data.setdefault("commit_reports", [])
    if not isinstance(commit_reports, list):
        raise AssertionError("commit_reports must be a list")

    commit_id = "forprint_library_reference_consumption_pilot_commit_7e000cb"
    commit_reports[:] = [
        item
        for item in commit_reports
        if not isinstance(item, dict) or item.get("id") != commit_id
    ]

    commit_reports.append(
        {
            "id": commit_id,
            "module_id": "forprint_library",
            "type": "commit_record",
            "status": "pushed",
            "commit": IMPLEMENTATION_COMMIT,
            "message": IMPLEMENTATION_COMMIT_MESSAGE,
            "related_prompt_id": PROMPT_ID,
            "completion_report": f"coordination/reports/completion/{REPORT_ID}.md",
            "created_at": "2026-07-08",
        }
    )

    write_yaml(REPORT_INDEX_PATH, data)


def write_completion_report() -> None:
    write_text_clean(
        REPORT_PATH,
        f"""# ForPrint Library Completion Report

## Subject

{PROMPT_TITLE}

## Module

`forprint_library`

## Prompt ID

`{PROMPT_ID}`

## Status

`completed_pending_blueprint_review`

## Date

`2026-07-08`

## Blueprint prompt path

Read-only reference:

```text
{BLUEPRINT_PROMPT_PATH}
Implementation commit
{IMPLEMENTATION_COMMIT} {IMPLEMENTATION_COMMIT_MESSAGE}
Purpose

This checkpoint adds a small, controlled, local and read-only reference
consumption pilot inside ForPrint Library.

The pilot demonstrates how downstream ForPrint modules may consume
Library-owned reference contract identifiers without making Library responsible
for downstream runtime behavior.

Completed scope

The implementation added:

examples/reference_consumption/library_reference_consumption_examples.yaml
schemas/reference_consumption/library_reference_consumption.schema.yaml
scripts/reference_consumption/validate_reference_consumption_pilot.py
docs/architecture/reference_consumption_pilot.md
tests/coordination/test_reference_consumption_pilot.py
scripts/run_library_checks.py
reports/library_check_report.json
reports/library_check_report.md
Consumer examples

The pilot includes valid local examples for:

calculator_engine consuming a Library product/service reference as pricing context
telegram_bot consuming a Library template reference as a channel-local hint
forprint_operational_registry consuming a Library material reference as foreign-domain metadata

The pilot also includes invalid examples for:

unknown Library reference id
consumer semantic redefinition
consumer runtime ownership/write fields
Reference IDs used

The pilot consumes controlled reference contract example IDs from:

examples/reference_contract/library_reference_examples.yaml

Examples include:

product_service.business_card.standard
template.business_card.90x50
material.paper.mondi_color_copy_300gsm

These are controlled reference contract examples, not production catalog records.

Validation behavior

The validator confirms that:

referenced Library IDs exist in the existing reference contract examples
valid consumer payloads pass
invalid consumer payloads fail clearly
consumer payloads do not redefine Library-owned semantics
consumer payloads do not introduce downstream runtime ownership into Library
human-readable preview output renders
Check-report visibility

The Library check report now includes:

Library reference consumption pilot

Expected result:

Reference consumption examples, schema and validator work

Status:

OK
Validation performed

The implementation was validated with:

reference consumption validator: OK
reference consumption preview: OK
focused tests: 7 passed
make lint: OK
make test: 115 passed
make check-report: OK
make check: OK
make governance-check: OK
make module-validate: OK
git diff --check: OK
Repository ownership boundary

All files were created or updated inside the Library repository only.

Library did not write into:

/srv/software_development/forprint-project/forprint_system_blueprint/...

Blueprint-side incoming report registration, review metadata, prompt queue
acceptance and next-prompt issuance remain Blueprint-owned actions.

Explicit non-goals preserved
No Configurable Product Workbench
No Business Card Skeleton
No product modeling UI
No production catalog database
No live API
No 1C import
No 1C synchronization
No Calculator integration
No Telegram Bot integration
No Operational Registry write
No production write
No price calculation
No material write-off logic
No Blueprint repository writes

Completion packet automation is not used for this checkpoint.

The module-side completion report, reports index and current status files are
updated by a local Library closure exporter.

This does not perform Blueprint-side intake, review or acceptance.

Readiness statement

Library is ready for Blueprint review of:

{PROMPT_ID}

The next step belongs to Blueprint: review this module-side completion output,
record Blueprint-side acceptance or return-for-fix metadata, and decide the next
approved prompt.
""",
)

def update_current_status_yaml() -> None:
    data = load_yaml(CURRENT_STATUS_YAML)

    data["module_id"] = "forprint_library"
    data["status"] = "reference_consumption_pilot_v0_3_ready_pending_blueprint_review"
    data["current_phase"] = "reference_consumption_pilot_v0_3"
    data["last_completed_step"] = "library_reference_consumption_pilot_ready"
    data["updated_at"] = "2026-07-08"

    data["current_focus"] = [
        "Reference Consumption Pilot v0.3 completed in Library repository.",
        "Local read-only consumer examples demonstrate safe reference consumption.",
        "Valid and invalid consumer payloads are covered by tests.",
        "No downstream runtime ownership or integration was added.",
        "Waiting for Blueprint review.",
    ]

    data.setdefault(
        "make_first_semantic_reference_readiness_v0_1",
        {
            "status": "accepted_by_blueprint",
            "prompt_id": "library_make_first_semantic_reference_readiness_v0_1",
            "implementation_commit": "935e51b",
        },
    )

    data.setdefault(
        "reference_contract_foundation_v0_2",
        {
            "status": "accepted_by_blueprint",
            "prompt_id": "library_reference_contract_foundation_v0_2",
            "implementation_commit": "78bd7e1",
            "completion_commit": "6343f65",
        },
    )

    data.setdefault(
        "coordination_foundation_alignment_v0_1",
        {
            "status": "accepted_by_blueprint",
            "prompt_id": "library_coordination_foundation_alignment_v0_1",
            "implementation_commit": "02e2cad",
            "completion_commit": "8031d3e",
            "commit_report": (
                "coordination/reports/commits/"
                "2026-07-07__forprint_library__commit-report__"
                "coordination-foundation-alignment-v0-1.md"
            ),
        },
    )

    data["reference_consumption_pilot_v0_3"] = {
        "status": "completed_pending_blueprint_review",
        "prompt_id": PROMPT_ID,
        "implementation_commit": IMPLEMENTATION_COMMIT,
        "completion_report": f"coordination/reports/completion/{REPORT_ID}.md",
        "blueprint_prompt_path": BLUEPRINT_PROMPT_PATH,
        "added_artifacts": [
            "examples/reference_consumption/library_reference_consumption_examples.yaml",
            "schemas/reference_consumption/library_reference_consumption.schema.yaml",
            "scripts/reference_consumption/validate_reference_consumption_pilot.py",
            "docs/architecture/reference_consumption_pilot.md",
            "tests/coordination/test_reference_consumption_pilot.py",
        ],
        "check_report_visibility": "Library reference consumption pilot",
        "validation": {
            "focused_tests": "7 passed",
            "full_tests": "115 passed",
            "check_report": "OK",
            "make_check": "OK",
            "governance_check": "OK",
            "module_validate": "OK",
            "git_diff_check": "OK",
        },
        "boundaries": {
            "configurable_product_workbench_started": False,
            "business_card_skeleton_started": False,
            "product_modeling_ui_added": False,
            "production_catalog_database_added": False,
            "live_api_added": False,
            "one_c_import_added": False,
            "calculator_integration_added": False,
            "telegram_integration_added": False,
            "operational_registry_write_added": False,
            "production_write_added": False,
            "price_calculation_added": False,
            "material_write_off_added": False,
            "blueprint_repository_written": False,
        },
        "next_recommended_step": "Blueprint review of module-side completion report.",
    }

    write_yaml(CURRENT_STATUS_YAML, data)

def write_current_status_md() -> None:
    write_text_clean(
        CURRENT_STATUS_MD,
        f"""# ForPrint Library Current Status

## Status

reference_consumption_pilot_v0_3_ready_pending_blueprint_review

## Current phase

reference_consumption_pilot_v0_3

## Last completed step

library_reference_consumption_pilot_ready

## Completed prompt

{PROMPT_ID}

## Implementation commit

```text
{IMPLEMENTATION_COMMIT} {IMPLEMENTATION_COMMIT_MESSAGE}

Completion report
coordination/reports/completion/{REPORT_ID}.md
Summary

Library Reference Consumption Pilot v0.3 is completed in the Library repository.

The checkpoint adds local, read-only examples showing how downstream modules may
consume Library-owned reference IDs without making Library responsible for
downstream runtime behavior.

Completed artifacts
examples/reference_consumption/library_reference_consumption_examples.yaml
schemas/reference_consumption/library_reference_consumption.schema.yaml
scripts/reference_consumption/validate_reference_consumption_pilot.py
docs/architecture/reference_consumption_pilot.md
tests/coordination/test_reference_consumption_pilot.py
scripts/run_library_checks.py
reports/library_check_report.json
reports/library_check_report.md
Validation
reference consumption validator: OK
reference consumption preview: OK
focused tests: 7 passed
make lint: OK
make test: 115 passed
make check-report: OK
make check: OK
make governance-check: OK
make module-validate: OK
git diff --check: OK
Boundaries preserved
No Configurable Product Workbench
No Business Card Skeleton
No product modeling UI
No production catalog database
No live API
No 1C import
No 1C synchronization
No Calculator integration
No Telegram Bot integration
No Operational Registry write
No production write
No price calculation
No material write-off logic
No Blueprint repository writes
No real secrets or credentials were committed
Previous completed checkpoints
coordination_foundation_alignment_v0_1
- Makefile was not rewritten.
- No real secrets or credentials were committed.
- Coordination foundation alignment remains recorded as a historical checkpoint.

reference_contract_foundation_v0_2
- Reference contract foundation remains recorded as a historical checkpoint.

make_first_semantic_reference_readiness_v0_1
- Make-first semantic reference readiness remains recorded as a historical checkpoint.
Next step

Waiting for Blueprint review.

Blueprint should read the module-side completion report and decide whether to
accept library_reference_consumption_pilot_v0_3 or return it for fixes.
""",
)

def write_next_questions() -> None:
    write_text_clean(
    NEXT_QUESTIONS,
    f"""# Next Questions for Blueprint

    Current module

    forprint_library

    Current checkpoint

    {PROMPT_ID}

    Status

    completed_pending_blueprint_review

    Question

    Please review the module-side completion report:

    coordination/reports/completion/{REPORT_ID}.md

    Should Library proceed to the next approved prompt after Blueprint acceptance?

    Boundary note

    Library did not start Configurable Product Workbench, Business Card Skeleton,
    runtime integrations, production writes, 1C import, Calculator integration,
    Telegram integration or Operational Registry writes.
    """,
    )

def main() -> int:
    write_completion_report()
    upsert_report_index()
    update_current_status_yaml()
    write_current_status_md()
    write_next_questions()

    print("OK: Reference consumption pilot closure exported")
    print(f"Report: {REPORT_PATH.relative_to(ROOT)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

## Primary source

**Path:** `scripts/coordination/export_reference_contract_foundation_closure.py`
**SHA256:** `f58565b957b1379495a3d2bbbef0b6346132fd34a1596277862a691c02a4ef9d`

```python
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]

PROMPT_ID = "reference_contract_foundation_v0_2"
BLUEPRINT_PROMPT_PATH = (
    "/srv/software_development/forprint-project/forprint_system_blueprint/"
    "coordination/outgoing_prompts/forprint_library/approved/"
    "2026-06-29__library__reference_contract_foundation_v0_2.md"
)

IMPLEMENTATION_COMMIT = "78bd7e1"
IMPLEMENTATION_COMMIT_MESSAGE = "Add Library reference contract foundation"

REPORT_ID = (
    "2026-06-29__forprint_library__report__"
    "reference-contract-foundation-v0-2"
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
        "reference_contract_foundation_v0_2_"
        "ready_pending_blueprint_review"
    )
    data["stage"] = "reference_contract_foundation_v0_2_completion"
    data["updated_at"] = "2026-06-29"
    data["current_phase"] = "reference_contract_foundation_v0_2"
    data["last_completed_step"] = "library_reference_contract_foundation_ready"

    data["current_focus"] = [
        "Library reference contract foundation v0.2 completed",
        "safe downstream Library reference payload examples added",
        "reference schema added",
        "reference contract validator added",
        "focused content tests added",
        "check-report visibility added",
        "Makefile left unchanged due manual Blueprint communication mode",
    ]

    data["reference_contract_foundation_v0_2"] = {
        "prompt_id": PROMPT_ID,
        "blueprint_prompt_path": BLUEPRINT_PROMPT_PATH,
        "implementation_commit": IMPLEMENTATION_COMMIT,
        "implementation_commit_message": IMPLEMENTATION_COMMIT_MESSAGE,
        "completion_report_id": REPORT_ID,
        "completion_report_path": str(REPORT_PATH.relative_to(ROOT)),
        "status": "completed_pending_blueprint_review",
        "docs": "done",
        "examples": "done",
        "schemas": "done",
        "validator": "done",
        "tests": "94_passed",
        "check_report_visibility": "done",
        "makefile_changes": "not_changed_manual_blueprint_mode",
        "completion_packet_automation": "deferred_safe_not_faked",
        "production_catalog_database": "not_implemented",
        "live_api": "not_implemented",
        "runtime_integrations": "not_implemented",
    }

    data["next_recommended_step"] = {
        "status": "wait_for_blueprint_review",
        "recommended_action": (
            "Ask Blueprint to review Library reference contract foundation "
            "v0.2 and decide downstream alignment expectations."
        ),
        "candidate_followups": [
            "Operational Registry Library reference projection adoption",
            "Calculator Engine Library reference input context adoption",
            "Integration Gateway Library reference envelope alignment",
            "Telegram Bot intake alias-to-reference handoff alignment",
            "Library reference contract v0.3 after downstream feedback",
        ],
    }

    write_yaml(STATUS_YAML, data)


def update_current_status_md() -> None:
    lines = [
        "# ForPrint Library Current Status",
        "",
        "## Status",
        "",
        "`reference_contract_foundation_v0_2_ready_pending_blueprint_review`",
        "",
        "## Current phase",
        "",
        "`reference_contract_foundation_v0_2`",
        "",
        "## Last completed step",
        "",
        "`library_reference_contract_foundation_ready`",
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
        "- Library reference contract foundation v0.2.",
        "- Reference contract architecture document.",
        "- Downstream Library reference YAML examples.",
        "- Local schema for Library reference payloads.",
        "- Reference contract validator script.",
        "- Focused content tests.",
        "- Check-report row for Library reference contract foundation.",
        "",
        "## Validation result",
        "",
        "```text",
        "reference contract validator: OK",
        "ruff: OK",
        "make test: 94 passed",
        "check-report: OK",
        "governance-check: OK",
        "module-validate: OK",
        "```",
        "",
        "## Makefile policy",
        "",
        "Makefile was intentionally not changed.",
        "",
        "Blueprint communication is temporarily handled manually through chat",
        "while the workflow policy is being adjusted.",
        "",
        "## Completion packet automation",
        "",
        "Completion packet automation remains deferred-safe.",
        "",
        "It is not faked.",
        "",
        "## Boundaries",
        "",
        "Library remains the canonical semantic/catalog authority.",
        "",
        "This checkpoint does not implement:",
        "",
        "```text",
        "production catalog database",
        "live API",
        "CRM integration",
        "Telegram integration",
        "Operational Registry write",
        "Calculator pricing logic",
        "warehouse stock logic",
        "accounting/payment logic",
        "1C sync/write",
        "automatic posting",
        "production runtime service",
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
        "Wait for Blueprint review and downstream alignment guidance.",
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
            "created_at": "2026-06-29",
        },
    )

    commit_reports = ensure_list(data, "commit_reports")
    upsert_by_id(
        commit_reports,
        {
            "id": "forprint_library_reference_contract_foundation_commit_78bd7e1",
            "module_id": "forprint_library",
            "type": "commit_report",
            "status": "pushed",
            "commit": IMPLEMENTATION_COMMIT,
            "message": IMPLEMENTATION_COMMIT_MESSAGE,
            "related_prompt_id": PROMPT_ID,
            "created_at": "2026-06-29",
        },
    )

    write_yaml(REPORTS_INDEX, data)


def write_completion_report() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# ForPrint Library Reference Contract Foundation v0.2",
        "",
        "## Completion Report",
        "",
        f"Report ID: `{REPORT_ID}`",
        "",
        "Module: `forprint_library`",
        "",
        "Status: `completed_pending_blueprint_review`",
        "",
        "Date: `2026-06-29`",
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
        "docs/architecture/reference_contract_foundation.md",
        "examples/reference_contract/library_reference_examples.yaml",
        "schemas/reference_contract/library_reference.schema.yaml",
        "scripts/reference_contract/validate_library_reference_contract.py",
        "tests/content/test_library_reference_contract.py",
        "scripts/run_library_checks.py",
        "reports/library_check_report.json",
        "reports/library_check_report.md",
        "```",
        "",
        "## Created or updated docs",
        "",
        "```text",
        "docs/architecture/reference_contract_foundation.md",
        "```",
        "",
        "## Created or updated examples",
        "",
        "```text",
        "examples/reference_contract/library_reference_examples.yaml",
        "```",
        "",
        "## Created or updated schemas",
        "",
        "```text",
        "schemas/reference_contract/library_reference.schema.yaml",
        "```",
        "",
        "## Created or updated tests",
        "",
        "```text",
        "tests/content/test_library_reference_contract.py",
        "```",
        "",
        "## Reference contract scope",
        "",
        "The checkpoint defines a small Library reference contract layer.",
        "",
        "It covers:",
        "",
        "```text",
        "canonical Library reference id format",
        "reference type / entity type",
        "display label",
        "optional alias input",
        "reference resolution status",
        "source module",
        "schema/version marker",
        "deprecation handling",
        "ambiguous/manual-review handling",
        "unknown/unresolved references",
        "example downstream payloads",
        "```",
        "",
        "Reference examples cover:",
        "",
        "```text",
        "product_service",
        "material",
        "operation",
        "unit",
        "template",
        "technical_card",
        "```",
        "",
        "Resolution statuses represented:",
        "",
        "```text",
        "library_reference_confirmed",
        "library_reference_pending",
        "ambiguous_manual_review_required",
        "deprecated_reference",
        "unknown",
        "```",
        "",
        "## Check-report visibility",
        "",
        "The check report now includes:",
        "",
        "```text",
        "Library reference contract foundation",
        "```",
        "",
        "Expected result:",
        "",
        "```text",
        "Reference contract docs, schemas and examples validate",
        "```",
        "",
        "Status: `OK`.",
        "",
        "## Validation results",
        "",
        "```text",
        "reference contract validator: OK",
        "make lint: OK",
        "make test: 94 passed",
        "make check-report: OK",
        "make governance-check: OK",
        "make module-validate: OK",
        "git diff --check: OK",
        "```",
        "",
        "## Manual Blueprint mode note",
        "",
        "Makefile active prompt was intentionally not changed.",
        "",
        "The project is temporarily using manual chat-based Blueprint prompt",
        "intake and reporting while the work policy is being adjusted.",
        "",
        "## Deferred items",
        "",
        "```text",
        "production catalog database",
        "live API",
        "CRM integration",
        "Telegram integration",
        "Operational Registry write",
        "Calculator pricing logic",
        "warehouse stock logic",
        "accounting/payment logic",
        "1C sync/write",
        "automatic posting",
        "production runtime service",
        "formal completion packet automation",
        "```",
        "",
        "## Blueprint review request",
        "",
        "Blueprint should review Library reference contract foundation v0.2.",
        "",
        "Requested decisions:",
        "",
        "1. Confirm the Library reference payload shape for downstream use.",
        "2. Decide Operational Registry projection expectations.",
        "3. Decide Calculator Engine reference input expectations.",
        "4. Decide Integration Gateway and Telegram reference handoff guidance.",
        "5. Decide whether v0.3 should follow after downstream feedback.",
        "",
        "## Recommended next step",
        "",
        "Wait for Blueprint review and downstream alignment guidance.",
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

**Path:** `scripts/coordination/validate_completion_packet.py`
**SHA256:** `4b338c9859a8486ca79ff79d0a868f27fa16cda5a42df4961cb351576bde91b2`

```python
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

EXPECTED_MODULE_ID = "forprint_library"
EXPECTED_PROMPT_ID = "forprint_library_calculator_input_contract_v0_1"
EXPECTED_PHASE = "calculator_input_contract_v0_1"
EXPECTED_REPORT_PATH = (
    "coordination/reports/completion/"
    "forprint_library_calculator_input_contract_v0_1_completion.md"
)

REQUIRED_STRING_FIELDS = (
    "schema_version",
    "packet_id",
    "module_id",
    "prompt_id",
    "phase",
    "created_at",
    "report_path",
    "base_commit",
    "implementation_commit",
    "completion_commit",
)

REQUIRED_CHECKS = (
    "focused_tests",
    "completion_report_tests",
    "full_suite",
    "lint",
    "format_check",
    "governance_check",
    "module_validate",
    "check_report",
    "check_report_full",
    "git_diff_check",
)

REQUIRED_BOUNDARY_FLAGS = (
    "no_production_api",
    "no_live_external_integrations",
    "no_production_write",
    "no_automatic_posting",
    "no_calculator_final_price_ownership",
    "no_order_creation",
    "no_telegram_runtime_ui",
    "no_logistics_ownership",
    "no_crm_or_gateway_write",
    "no_accounting_or_payment_write",
    "no_stock_or_production_write",
    "no_blueprint_repository_write",
)

COMMIT_RE = re.compile(r"^[0-9a-f]{7,40}$")


class CompletionPacketValidationError(ValueError):
    """Completion packet does not match the Library/Blueprint intake contract."""


def _fail(message: str) -> None:
    raise CompletionPacketValidationError(message)


def _require_mapping(value: Any, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        _fail(f"completion packet field `{field}` must be a mapping")
    return value


def _require_string(data: dict[str, Any], field: str) -> str:
    value = data.get(field)
    if not isinstance(value, str) or not value.strip():
        _fail(f"completion packet field `{field}` must be a non-empty string")
    return value.strip()


def _require_commit(data: dict[str, Any], field: str) -> str:
    value = _require_string(data, field)
    if not COMMIT_RE.fullmatch(value):
        _fail(f"completion packet field `{field}` must be a git commit hash")
    return value


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        _fail(f"invalid YAML in completion packet: {exc}")
    except UnicodeDecodeError as exc:
        _fail(f"completion packet is not valid UTF-8: {exc}")

    if not isinstance(loaded, dict):
        _fail("completion packet root must be a mapping")
    return loaded


def _resolve_packet_path(packet_path: str | Path, root: Path) -> Path:
    raw = str(packet_path)
    if not raw.strip():
        _fail("PACKET path is required")
    path = Path(raw)
    if not path.is_absolute():
        path = root / path
    if not path.exists():
        _fail(f"completion packet file is missing: {path}")
    if not path.is_file():
        _fail(f"completion packet path is not a file: {path}")
    return path


def _validate_required_identity(data: dict[str, Any]) -> None:
    for field in REQUIRED_STRING_FIELDS:
        _require_string(data, field)

    if data["module_id"] != EXPECTED_MODULE_ID:
        _fail("completion packet field `module_id` has wrong value")
    if data["prompt_id"] != EXPECTED_PROMPT_ID:
        _fail("completion packet field `prompt_id` has wrong value")
    if data["phase"] != EXPECTED_PHASE:
        _fail("completion packet field `phase` has wrong value")
    if data["report_path"] != EXPECTED_REPORT_PATH:
        _fail("completion packet field `report_path` has wrong value")

    _require_commit(data, "base_commit")
    _require_commit(data, "implementation_commit")
    _require_commit(data, "completion_commit")


def _validate_report_path(data: dict[str, Any], root: Path) -> None:
    report_path = root / data["report_path"]
    if not report_path.exists():
        _fail(f"completion packet report_path does not exist: {data['report_path']}")
    if not report_path.is_file():
        _fail(f"completion packet report_path is not a file: {data['report_path']}")


def _validate_checks(data: dict[str, Any]) -> None:
    checks = _require_mapping(data.get("checks"), "checks")
    for check_name in REQUIRED_CHECKS:
        check = _require_mapping(checks.get(check_name), f"checks.{check_name}")
        if check.get("exit_code") != 0:
            _fail(f"completion packet check `{check_name}` must have exit_code 0")

    for check_name in ("focused_tests", "completion_report_tests", "full_suite"):
        check = checks[check_name]
        passed = check.get("passed")
        if not isinstance(passed, int) or passed <= 0:
            _fail(f"completion packet check `{check_name}` must record passed tests")

    for check_name in ("check_report", "check_report_full"):
        totals = _require_mapping(checks[check_name].get("totals"), f"{check_name}.totals")
        for field in ("total_checks", "ok", "failed", "other"):
            value = totals.get(field)
            if not isinstance(value, int) or value < 0:
                _fail(f"completion packet `{check_name}.totals.{field}` must be >= 0")
        counted = totals["ok"] + totals["failed"] + totals["other"]
        if totals["total_checks"] != counted:
            _fail(f"completion packet `{check_name}` totals do not add up")


def _validate_boundary_confirmation(data: dict[str, Any]) -> None:
    boundary = _require_mapping(
        data.get("boundary_confirmation"),
        "boundary_confirmation",
    )
    for flag in REQUIRED_BOUNDARY_FLAGS:
        if boundary.get(flag) is not True:
            _fail(f"completion packet boundary_confirmation `{flag}` must be true")


def validate_packet(packet_path: str | Path, *, root: Path | None = None) -> dict[str, Any]:
    module_root = root or Path.cwd()
    packet = _resolve_packet_path(packet_path, module_root)
    data = _load_yaml(packet)

    _validate_required_identity(data)
    _validate_report_path(data, module_root)
    _validate_checks(data)
    _validate_boundary_confirmation(data)

    return data


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("ERROR: usage: validate_completion_packet.py <PACKET>", file=sys.stderr)
        return 2

    try:
        data = validate_packet(args[0])
    except CompletionPacketValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print("OK: completion packet schema validates")
    print(f"module_id: {data['module_id']}")
    print(f"prompt_id: {data['prompt_id']}")
    print(f"implementation_commit: {data['implementation_commit']}")
    print(f"completion_commit: {data['completion_commit']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Primary source

**Path:** `scripts/product_workbench/preview_business_card_product.py`
**SHA256:** `01fe38c52f482b985452e650e5655b1119980b63bb97c51a12e68202f89e61e0`

```python
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
CARD_PATH = ROOT / "catalog" / "configurable_products" / "business_card.yaml"


def load_card() -> dict[str, Any]:
    data = yaml.safe_load(CARD_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise AssertionError("Business card product card must be a mapping")
    return data


def main() -> int:
    card = load_card()

    print(f"Product card: {card['names']['uk']}")
    print(f"Product ID: {card['product_id']}")
    print(f"Kind: {card['kind']}")
    print(f"Status: {card['status']}")
    print()
    print("Constructor parameters:")
    for parameter in card["constructor_parameters"]:
        print(f"- {parameter['key']}")
    print()
    print("Consumer notes:")
    notes = card["consumer_usage_notes"]
    print(f"- Telegram Bot: {notes['telegram_bot']['allowed_use']}")
    print(f"- Calculator Engine: {notes['calculator_engine']['allowed_use']}")
    print(
        "- Operational Registry: "
        f"{notes['forprint_operational_registry']['allowed_use']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Primary source

**Path:** `scripts/product_workbench/validate_business_card_product.py`
**SHA256:** `af2d9a937e3f78d88b8197a48d4e7732ee059e13b3aef03545c295fe2c82af8f`

```python
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
```

## Primary source

**Path:** `scripts/reference_consumption/validate_reference_consumption_pilot.py`
**SHA256:** `bc8b38f0e9d6476bd7f0595d4730d034410c290d2d6715e653405aebba4e03ec`

```python
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]

EXAMPLES_PATH = (
    ROOT
    / "examples"
    / "reference_consumption"
    / "library_reference_consumption_examples.yaml"
)
SCHEMA_PATH = (
    ROOT
    / "schemas"
    / "reference_consumption"
    / "library_reference_consumption.schema.yaml"
)
REFERENCE_CONTRACT_EXAMPLES_PATH = (
    ROOT / "examples" / "reference_contract" / "library_reference_examples.yaml"
)
DOC_PATH = ROOT / "docs" / "architecture" / "reference_consumption_pilot.md"

EXPECTED_SCHEMA_VERSION = "library_reference_consumption_examples_v0_3"
EXPECTED_PILOT_ID = "library_reference_consumption_pilot_v0_3"
EXPECTED_OWNER_MODULE = "forprint_library"
EXPECTED_REFERENCE_SCHEMA_VERSION = "library_reference_v0_2"

ALLOWED_CONSUMER_MODULES = {
    "calculator_engine",
    "telegram_bot",
    "forprint_operational_registry",
    "forprint_accounting_registry_service",
    "forprint_prepress_hub",
    "forprint_integration_gateway",
}

ALLOWED_REFERENCE_TYPES = {
    "product_service",
    "material",
    "operation",
    "unit",
    "template",
    "technical_card",
}

ALLOWED_RESOLUTION_STATUSES = {
    "library_reference_confirmed",
    "library_reference_pending",
    "ambiguous_manual_review_required",
    "deprecated_reference",
}

FORBIDDEN_CONSUMER_FIELDS = {
    "canonical_name_override",
    "semantic_definition_override",
    "library_alias_write",
    "library_reference_write",
    "final_price",
    "price_formula",
    "stock_mutation",
    "material_write_off",
    "order_creation",
    "client_creation",
    "payment_posting",
    "production_runtime_write",
    "telegram_runtime_behavior",
    "calculator_runtime_integration",
    "operational_registry_write",
    "one_c_sync",
    "one_c_import",
}


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise AssertionError(f"Missing file: {path.relative_to(ROOT)}")

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise AssertionError(f"YAML root must be a mapping: {path.relative_to(ROOT)}")

    return data


def require_files() -> None:
    for path in [EXAMPLES_PATH, SCHEMA_PATH, REFERENCE_CONTRACT_EXAMPLES_PATH, DOC_PATH]:
        if not path.exists():
            raise AssertionError(f"Missing file: {path.relative_to(ROOT)}")


def collect_known_library_reference_ids() -> set[str]:
    data = load_yaml(REFERENCE_CONTRACT_EXAMPLES_PATH)
    examples = data.get("examples", [])

    if not isinstance(examples, list) or not examples:
        raise AssertionError("Reference contract examples must be a non-empty list")

    known_ids: set[str] = set()

    for example in examples:
        if not isinstance(example, dict):
            raise AssertionError("Reference contract example must be a mapping")

        reference = (
            example.get("downstream_payload", {})
            .get("library_reference", {})
        )

        if not isinstance(reference, dict):
            raise AssertionError("Reference contract library_reference must be a mapping")

        reference_id = reference.get("reference_id")
        if isinstance(reference_id, str) and reference_id:
            known_ids.add(reference_id)

    if not known_ids:
        raise AssertionError("No known Library reference IDs found")

    return known_ids


def validate_schema_file() -> None:
    schema = load_yaml(SCHEMA_PATH)

    if schema.get("$id") != (
        "forprint_library.reference_consumption.library_reference_consumption_v0_3"
    ):
        raise AssertionError("Unexpected reference consumption schema $id")

    if schema.get("title") != "ForPrint Library Reference Consumption Pilot v0.3":
        raise AssertionError("Unexpected reference consumption schema title")

    required = set(schema.get("required", []))
    expected_required = {
        "schema_version",
        "pilot_id",
        "owner_module",
        "reference_contract_source",
        "valid_consumer_payloads",
        "invalid_consumer_payloads",
    }

    missing = sorted(expected_required - required)
    if missing:
        raise AssertionError(f"Schema is missing required fields: {missing}")

    shape = schema.get("consumer_payload_shape")
    if not isinstance(shape, dict):
        raise AssertionError("Schema must document consumer_payload_shape")

    forbidden = set(shape.get("forbidden_consumer_fields", []))
    missing_forbidden = sorted(FORBIDDEN_CONSUMER_FIELDS - forbidden)
    if missing_forbidden:
        raise AssertionError(
            f"Schema is missing forbidden consumer fields: {missing_forbidden}"
        )


def iter_mapping_keys(value: Any) -> list[str]:
    keys: list[str] = []

    if isinstance(value, dict):
        for key, nested in value.items():
            keys.append(str(key))
            keys.extend(iter_mapping_keys(nested))
    elif isinstance(value, list):
        for item in value:
            keys.extend(iter_mapping_keys(item))

    return keys


def validate_no_forbidden_fields(payload: dict[str, Any], payload_id: str) -> None:
    keys = set(iter_mapping_keys(payload))
    forbidden = sorted(keys & FORBIDDEN_CONSUMER_FIELDS)

    if forbidden:
        raise AssertionError(f"{payload_id}: forbidden field(s): {forbidden}")


def validate_reference(
    reference: Any,
    *,
    payload_id: str,
    known_reference_ids: set[str],
) -> None:
    if not isinstance(reference, dict):
        raise AssertionError(f"{payload_id}: library_owned_reference must be a mapping")

    required_fields = {
        "schema_version",
        "reference_type",
        "reference_id",
        "display_label",
        "resolution_status",
    }

    missing = sorted(required_fields - set(reference))
    if missing:
        raise AssertionError(f"{payload_id}: missing library reference fields: {missing}")

    if reference["schema_version"] != EXPECTED_REFERENCE_SCHEMA_VERSION:
        raise AssertionError(f"{payload_id}: invalid library reference schema_version")

    if reference["reference_type"] not in ALLOWED_REFERENCE_TYPES:
        raise AssertionError(f"{payload_id}: invalid library reference type")

    if reference["resolution_status"] not in ALLOWED_RESOLUTION_STATUSES:
        raise AssertionError(f"{payload_id}: invalid library reference status")

    reference_id = reference["reference_id"]
    if not isinstance(reference_id, str) or not reference_id:
        raise AssertionError(f"{payload_id}: reference_id must be a non-empty string")

    if reference_id not in known_reference_ids:
        raise AssertionError(f"{payload_id}: unknown Library reference id: {reference_id}")

    display_label = reference["display_label"]
    if not isinstance(display_label, str) or not display_label:
        raise AssertionError(f"{payload_id}: display_label must be a non-empty string")


def validate_boundary_assertions(assertions: Any, payload_id: str) -> None:
    if not isinstance(assertions, dict):
        raise AssertionError(f"{payload_id}: boundary_assertions must be a mapping")

    required_true_flags = {
        "example_only",
        "no_library_semantic_redefinition",
        "no_downstream_runtime_write",
    }

    for flag in required_true_flags:
        if assertions.get(flag) is not True:
            raise AssertionError(f"{payload_id}: boundary assertion must be true: {flag}")


def validate_payload(
    payload: dict[str, Any],
    *,
    known_reference_ids: set[str],
) -> None:
    payload_id = str(payload.get("id", "<missing id>"))

    required_fields = {
        "id",
        "description",
        "consumer_module",
        "consumer_payload_id",
        "library_owned_reference",
        "consumer_owned_fields",
        "foreign_module_references",
        "boundary_assertions",
    }

    missing = sorted(required_fields - set(payload))
    if missing:
        raise AssertionError(f"{payload_id}: missing required fields: {missing}")

    consumer_module = payload["consumer_module"]
    if consumer_module not in ALLOWED_CONSUMER_MODULES:
        raise AssertionError(f"{payload_id}: invalid consumer_module: {consumer_module}")

    if not isinstance(payload["consumer_payload_id"], str) or not payload["consumer_payload_id"]:
        raise AssertionError(f"{payload_id}: consumer_payload_id must be a string")

    if not isinstance(payload["consumer_owned_fields"], dict):
        raise AssertionError(f"{payload_id}: consumer_owned_fields must be a mapping")

    if not isinstance(payload["foreign_module_references"], dict):
        raise AssertionError(f"{payload_id}: foreign_module_references must be a mapping")

    validate_no_forbidden_fields(payload, payload_id)
    validate_reference(
        payload["library_owned_reference"],
        payload_id=payload_id,
        known_reference_ids=known_reference_ids,
    )
    validate_boundary_assertions(payload["boundary_assertions"], payload_id)


def validate_examples() -> dict[str, Any]:
    data = load_yaml(EXAMPLES_PATH)
    known_reference_ids = collect_known_library_reference_ids()

    if data.get("schema_version") != EXPECTED_SCHEMA_VERSION:
        raise AssertionError("Unexpected reference consumption examples schema_version")

    if data.get("pilot_id") != EXPECTED_PILOT_ID:
        raise AssertionError("Unexpected reference consumption pilot_id")

    if data.get("owner_module") != EXPECTED_OWNER_MODULE:
        raise AssertionError("Unexpected reference consumption owner_module")

    source = data.get("reference_contract_source")
    if not isinstance(source, dict):
        raise AssertionError("reference_contract_source must be a mapping")

    if source.get("schema_version") != EXPECTED_REFERENCE_SCHEMA_VERSION:
        raise AssertionError("reference_contract_source schema_version mismatch")

    valid_payloads = data.get("valid_consumer_payloads", [])
    invalid_payloads = data.get("invalid_consumer_payloads", [])

    if not isinstance(valid_payloads, list) or not valid_payloads:
        raise AssertionError("valid_consumer_payloads must be a non-empty list")

    if not isinstance(invalid_payloads, list) or not invalid_payloads:
        raise AssertionError("invalid_consumer_payloads must be a non-empty list")

    for payload in valid_payloads:
        if not isinstance(payload, dict):
            raise AssertionError("Each valid payload must be a mapping")
        validate_payload(payload, known_reference_ids=known_reference_ids)

    for payload in invalid_payloads:
        if not isinstance(payload, dict):
            raise AssertionError("Each invalid payload must be a mapping")

        expected_error = payload.get("expected_error_contains")
        if not isinstance(expected_error, str) or not expected_error:
            raise AssertionError(
                f"{payload.get('id', '<missing id>')}: expected_error_contains required"
            )

        try:
            validate_payload(payload, known_reference_ids=known_reference_ids)
        except AssertionError as exc:
            if expected_error not in str(exc):
                raise AssertionError(
                    f"{payload.get('id', '<missing id>')}: expected error "
                    f"containing {expected_error!r}, got {exc!s}"
                ) from exc
        else:
            raise AssertionError(
                f"{payload.get('id', '<missing id>')}: invalid payload unexpectedly passed"
            )

    return data


def validate_docs() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")

    required_phrases = [
        "Library Reference Consumption Pilot v0.3",
        "Library-owned reference IDs",
        "consumer-owned runtime fields",
        "foreign module references",
        "must not redefine Library-owned semantics",
        "does not implement Calculator formulas",
        "does not implement Telegram runtime behavior",
        "does not implement Operational Registry storage",
        "does not start Configurable Product Workbench",
    ]

    for phrase in required_phrases:
        if phrase not in text:
            raise AssertionError(f"Document is missing phrase: {phrase}")


def render_preview(data: dict[str, Any]) -> None:
    print("ForPrint Library Reference Consumption Pilot v0.3")
    print("Mode: local read-only examples")
    print("")

    for payload in data["valid_consumer_payloads"]:
        reference = payload["library_owned_reference"]
        assertions = payload["boundary_assertions"]

        print(f"- Consumer: {payload['consumer_module']}")
        print(f"  Payload: {payload['consumer_payload_id']}")
        print(
            "  Uses Library reference: "
            f"{reference['reference_type']}::{reference['reference_id']}"
        )
        print(
            "  Boundary: "
            "no semantic redefinition, no downstream runtime write"
        )
        print(f"  Example only: {assertions.get('example_only')}")
        print("")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Render a human-readable preview of valid consumer payloads.",
    )
    args = parser.parse_args()

    require_files()
    validate_schema_file()
    validate_docs()
    data = validate_examples()

    if args.preview:
        render_preview(data)
    else:
        print("OK: Library reference consumption pilot validates")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Primary source

**Path:** `scripts/validate_semantic_reference_readiness.py`
**SHA256:** `238ec54bf5fe4d2ada58c970d98b844afc1bdcd3d75f34d1a5f56d6cecacd566`

```python

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]

EXAMPLE_PATH = ROOT / "examples" / "semantic_reference_preview.yaml"

READINESS_DOC = (
    ROOT / "docs" / "architecture" / "semantic_reference_readiness.md"
)

HANDOFF_DOC = (
    ROOT / "docs" / "architecture" / "downstream_reference_contract_notes.md"
)

MAKEFILE = ROOT / "Makefile"
ACTIVE_PROMPT_DIR = ROOT / "coordination" / "prompts" / "active"

STANDARDS_SNAPSHOT = (
    ROOT
    / "coordination"
    / "standards"
    / "blueprint_standards_available_snapshot.txt"
)

REQUIRED_REFERENCE_TYPES = {
    "product_service",
    "material",
    "operation",
    "template",
}

REQUIRED_MAKE_TARGETS = {
    "blueprint-sync",
    "module-start",
    "module-sync",
    "module-validate",
    "module-finish",
    "prompt-read",
    "report-clean",
    "completion-packet-check",
}


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise AssertionError(f"Missing file: {path.relative_to(ROOT)}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise AssertionError(f"YAML root must be a mapping: {path.relative_to(ROOT)}")
    return data


def read_text(path: Path) -> str:
    if not path.exists():
        raise AssertionError(f"Missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8").casefold()


def check_semantic_reference_readiness() -> None:
    data = load_yaml(EXAMPLE_PATH)

    metadata = data.get("metadata", {})
    assert metadata.get("owner_module") == "forprint_library"
    assert metadata.get("status") == "draft_semantic_reference_readiness_v0_1"
    assert metadata.get("production_catalog_status") == "not_production_catalog_database"

    references = data.get("canonical_references", [])
    assert isinstance(references, list)
    assert references

    reference_types = {item.get("reference_type") for item in references}
    missing_types = REQUIRED_REFERENCE_TYPES - reference_types
    assert not missing_types, f"Missing reference types: {sorted(missing_types)}"

    for item in references:
        assert item["id"]
        assert item["label_uk"]
        assert item["label_en"]
        assert item["reference_type"] in REQUIRED_REFERENCE_TYPES
        assert isinstance(item.get("aliases"), list)
        assert item["readiness_status"] == "ready_for_reference_example"
        assert "calculator_engine" in item["downstream_usage"]
        assert "forprint_operational_registry" in item["downstream_usage"]
        assert isinstance(item.get("forbidden_usage"), list)
        assert item["forbidden_usage"]

    alias_examples = data.get("alias_resolution_examples", [])
    assert alias_examples
    assert any(
        item.get("expected_resolution_status") == "confirmed_with_alias"
        for item in alias_examples
    )
    assert any(
        item.get("expected_resolution_status") == "unresolved_manual_review_required"
        for item in alias_examples
    )

    ambiguous_examples = data.get("ambiguous_naming_examples", [])
    assert ambiguous_examples
    assert (
        ambiguous_examples[0]["expected_resolution_status"]
        == "ambiguous_manual_review_required"
    )


def check_docs() -> None:
    readiness = read_text(READINESS_DOC)
    handoff = read_text(HANDOFF_DOC)

    for phrase in [
        "not to build the full production catalog database",
        "product_service.business_card.standard",
        "confirmed_with_alias",
        "ambiguous_manual_review_required",
        "pricing formulas",
        "warehouse stock truth",
        "operational order state",
    ]:
        assert phrase in readiness

    for phrase in [
        "calculator engine",
        "operational registry",
        "store library ids as operational projections",
        "no downstream module should silently invent",
        "not a final production catalog contract",
    ]:
        assert phrase in handoff


def check_make_first_alignment() -> None:
    text = MAKEFILE.read_text(encoding="utf-8")

    for target in REQUIRED_MAKE_TARGETS:
        assert f"{target}:" in text

    assert ".PHONY:" in text


def check_blueprint_visibility() -> None:
    assert ACTIVE_PROMPT_DIR.exists(), "Missing synced active prompt directory"
    assert any(ACTIVE_PROMPT_DIR.glob("*.md")), "No synced active prompt files found"
    assert STANDARDS_SNAPSHOT.exists(), "Missing Blueprint standards snapshot"


CHECKS = {
    "semantic": check_semantic_reference_readiness,
    "docs": check_docs,
    "make-first": check_make_first_alignment,
    "blueprint-visibility": check_blueprint_visibility,
    "all": lambda: [
        check_make_first_alignment(),
        check_blueprint_visibility(),
        check_semantic_reference_readiness(),
        check_docs(),
    ],
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", choices=sorted(CHECKS), default="all")
    args = parser.parse_args()

    CHECKS[args.check]()
    print(f"OK: semantic reference readiness check '{args.check}' passed.")
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

**Path:** `tests/contract/test_blueprint_prompt_consumer_compatibility.py`
**SHA256:** `689cb2a6782c561e10c6f77d7e8be6ceeee308ea024f2785cf0a1045874bb69b`

```python
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAKEFILE = ROOT / "Makefile"


def test_blueprint_prompt_consumer_uses_path_only_resolver_mode() -> None:
    text = MAKEFILE.read_text(encoding="utf-8")

    assert "--path-only" in text
    assert "resolve_next_prompt.py" in text
    assert "/^Path: /" not in text
    assert "awk -F': '" not in text


def test_blueprint_prompt_check_and_sync_targets_are_present() -> None:
    text = MAKEFILE.read_text(encoding="utf-8")

    assert ".PHONY: blueprint-instruction-check" in text
    assert "blueprint-instruction-check:" in text
    assert ".PHONY: blueprint-instruction-sync" in text
    assert "blueprint-instruction-sync: blueprint-instruction-check" in text
    assert ".PHONY: blueprint-prompts-check" in text
    assert "blueprint-prompts-check: blueprint-instruction-check" in text


def test_blueprint_prompt_consumer_keeps_manual_override_fallback() -> None:
    text = MAKEFILE.read_text(encoding="utf-8")

    assert "ACTIVE_BLUEPRINT_PROMPT ?=" in text
    assert "manual active prompt override" in text
    assert "Prompt Queue next prompt is readable" in text
    assert "synced Prompt Queue next prompt" in text
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

**Path:** `tests/contract/test_make_first_workflow_targets.py`
**SHA256:** `68079ca9bf1d29286ebd7c9fb8aedbd4840cd2c5fadc0d856981a544a126034a`

```python
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_TARGETS = [
    "blueprint-instruction-list",
    "blueprint-instruction-check",
    "blueprint-instruction-sync",
    "blueprint-instruction",
    "blueprint-standards-list",
    "blueprint-standards-check",
    "blueprint-standards-sync",
    "blueprint-standards",
    "blueprint-prompts-list",
    "blueprint-prompts-check",
    "blueprint-prompts-sync",
    "blueprint-prompts",
    "prompt-read",
    "blueprint-sync",
    "module-start",
    "module-sync",
    "module-validate",
    "module-finish",
    "report-clean",
    "completion-packet-validate",
    "completion-packet-apply",
    "completion-packet-check",
]


def test_makefile_contains_make_first_targets() -> None:
    text = (ROOT / "Makefile").read_text(encoding="utf-8")

    for target in REQUIRED_TARGETS:
        assert f"{target}:" in text


def test_makefile_exposes_make_first_targets_as_phony() -> None:
    text = (ROOT / "Makefile").read_text(encoding="utf-8")

    phony_sections = [
        line
        for line in text.splitlines()
        if line.startswith(".PHONY:") or line.startswith("\t")
    ]
    phony_text = "\n".join(phony_sections)

    for target in REQUIRED_TARGETS:
        assert target in phony_text


def test_make_first_workflow_helper_exists() -> None:
    path = ROOT / "scripts" / "make_first_workflow.py"

    assert path.exists()
    assert "completion packet automation is not configured" in path.read_text(
        encoding="utf-8"
    )
```

## Related test

**Path:** `tests/contract/test_required_validation_targets.py`
**SHA256:** `097143c7d5dc25674454a0c3ce48ddbdd27eca0b7feed44dd70261f39cc1287a`

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAKEFILE = ROOT / "Makefile"


def test_format_check_target_exists_and_is_changed_file_scoped() -> None:
    text = MAKEFILE.read_text(encoding="utf-8")

    assert ".PHONY: format-check" in text
    assert "format-check:" in text
    assert "ruff format --check $$changed_files" in text
    assert "git diff --name-only --diff-filter=ACMRTUXB origin/main...HEAD" in text
    assert "git ls-files --others --exclude-standard -- app scripts tests" in text
    assert "ruff format --check app scripts tests" not in text


def test_check_report_full_target_exists_as_blueprint_compatibility_alias() -> None:
    text = MAKEFILE.read_text(encoding="utf-8")

    assert ".PHONY: check-report-full" in text
    assert "check-report-full: check-report" in text


def test_help_lists_required_validation_targets() -> None:
    text = MAKEFILE.read_text(encoding="utf-8")

    assert 'make format-check' in text
    assert 'make check-report-full' in text
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

**Path:** `tests/contract/test_shared_dictionary_check_report_surface.py`
**SHA256:** `c5208c62a69cb180ac9e7acb714e67ec45e0b7ede747417c44b6f3ce704961df`

```python
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_check_report_includes_shared_dictionary_checks() -> None:
    text = (ROOT / "scripts/run_library_checks.py").read_text(encoding="utf-8")

    for phrase in [
        "Shared dictionary files",
        "Dictionary schemas",
        "Dictionary group files",
        "Dictionary required values",
        "Dictionary resolver/examples",
        "Dictionary preview",
    ]:
        assert phrase in text


def test_makefile_exposes_dictionary_targets() -> None:
    text = (ROOT / "Makefile").read_text(encoding="utf-8")

    for target in [
        "dictionary-preview:",
        "status-report:",
    ]:
        assert target in text
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

**Path:** `tests/coordination/test_completion_packet_validator.py`
**SHA256:** `a558ea6cc2e133fc464e10f7aff341d947c3df1073fb5fda55f6ced49c0a5d09`

```python
from __future__ import annotations

import copy
import subprocess
from pathlib import Path
from typing import Any

import pytest
import yaml

from scripts.coordination.validate_completion_packet import (
    CompletionPacketValidationError,
    validate_packet,
)

ROOT = Path(__file__).resolve().parents[2]
PACKET = (
    ROOT
    / "coordination"
    / "completion_packets"
    / "records"
    / "2026-07-29__forprint_library__calculator_input_contract_v0_1_completion.yaml"
)


def _packet_data() -> dict[str, Any]:
    loaded = yaml.safe_load(PACKET.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _write_packet(tmp_path: Path, data: dict[str, Any], name: str = "packet.yaml") -> Path:
    path = tmp_path / name
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return path


def _invalid_packet(tmp_path: Path, field: str, value: Any = None) -> Path:
    data = copy.deepcopy(_packet_data())
    if value is None:
        data.pop(field, None)
    else:
        data[field] = value
    return _write_packet(tmp_path, data)


def test_valid_library_completion_packet_passes() -> None:
    packet = validate_packet(PACKET, root=ROOT)

    assert packet["module_id"] == "forprint_library"
    assert packet["prompt_id"] == "forprint_library_calculator_input_contract_v0_1"
    assert packet["implementation_commit"] == "0b8cbce"
    assert packet["completion_commit"] == "89c4ec6"


@pytest.mark.parametrize("value", [None, ""])
def test_implementation_commit_required(tmp_path: Path, value: Any) -> None:
    packet = _invalid_packet(tmp_path, "implementation_commit", value)

    with pytest.raises(CompletionPacketValidationError, match="implementation_commit"):
        validate_packet(packet, root=ROOT)


@pytest.mark.parametrize("value", [None, ""])
def test_completion_commit_required(tmp_path: Path, value: Any) -> None:
    packet = _invalid_packet(tmp_path, "completion_commit", value)

    with pytest.raises(CompletionPacketValidationError, match="completion_commit"):
        validate_packet(packet, root=ROOT)


def test_wrong_prompt_id_fails(tmp_path: Path) -> None:
    packet = _invalid_packet(tmp_path, "prompt_id", "wrong_prompt")

    with pytest.raises(CompletionPacketValidationError, match="prompt_id"):
        validate_packet(packet, root=ROOT)


def test_wrong_module_id_fails(tmp_path: Path) -> None:
    packet = _invalid_packet(tmp_path, "module_id", "wrong_module")

    with pytest.raises(CompletionPacketValidationError, match="module_id"):
        validate_packet(packet, root=ROOT)


@pytest.mark.parametrize("value", [None, ""])
def test_report_path_required(tmp_path: Path, value: Any) -> None:
    packet = _invalid_packet(tmp_path, "report_path", value)

    with pytest.raises(CompletionPacketValidationError, match="report_path"):
        validate_packet(packet, root=ROOT)


def test_invalid_yaml_fails(tmp_path: Path) -> None:
    packet = tmp_path / "invalid.yaml"
    packet.write_text("module_id: [\n", encoding="utf-8")

    with pytest.raises(CompletionPacketValidationError, match="invalid YAML"):
        validate_packet(packet, root=ROOT)


def test_make_target_respects_packet_path(tmp_path: Path) -> None:
    packet = _invalid_packet(tmp_path, "implementation_commit", "")

    result = subprocess.run(
        ["make", "completion-packet-validate", f"PACKET={packet}"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode != 0
    assert "implementation_commit" in result.stderr
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

**Path:** `tests/coordination/test_reference_contract_foundation_closure.py`
**SHA256:** `2d669c2d4676c1a98b7b5de0e77e0a888cc56354744aa14ea73bf52f7acc3940`

```python
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]

REPORT_ID = (
    "2026-06-29__forprint_library__report__"
    "reference-contract-foundation-v0-2"
)
REPORT_PATH = ROOT / "coordination" / "reports" / "completion" / f"{REPORT_ID}.md"


def test_reference_contract_foundation_completion_report_exists() -> None:
    assert REPORT_PATH.exists()

    text = REPORT_PATH.read_text(encoding="utf-8")

    for expected in [
        "ForPrint Library Reference Contract Foundation v0.2",
        "Library reference contract foundation",
        "Reference contract docs, schemas and examples validate",
        "78bd7e1",
        "Makefile active prompt was intentionally not changed",
    ]:
        assert expected in text


def test_current_status_keeps_reference_contract_foundation_record() -> None:
    data = yaml.safe_load(
        (ROOT / "coordination" / "status" / "current_status.yaml").read_text(
            encoding="utf-8"
        )
    )

    assert data["module_id"] == "forprint_library"
    assert data["owner_module"] == "forprint_library"

    checkpoint = data["reference_contract_foundation_v0_2"]

    assert checkpoint["implementation_commit"] == "78bd7e1"
    assert checkpoint["check_report_visibility"] == "done"
    assert checkpoint["makefile_changes"] == "not_changed_manual_blueprint_mode"
    assert checkpoint["status"] in {
        "completed_pending_blueprint_review",
        "accepted_by_blueprint",
    }

def test_reports_index_references_reference_contract_foundation_report() -> None:
    data = yaml.safe_load(
        (ROOT / "coordination" / "reports" / "index.yaml").read_text(
            encoding="utf-8"
        )
    )

    completion_ids = {
        item["id"]
        for item in data.get("completion_reports", [])
        if isinstance(item, dict)
    }

    assert REPORT_ID in completion_ids


def test_reference_contract_report_mentions_manual_blueprint_mode() -> None:
    text = REPORT_PATH.read_text(encoding="utf-8")

    assert "reference_contract_foundation_v0_2" in text
    assert "Makefile active prompt was intentionally not changed" in text
    assert "manual" in text.lower()
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

## Related test

**Path:** `tests/unit/test_checkpoint_a_standard.py`
**SHA256:** `845ae07fc668470fb70a7a507a49190fd53ecb2a9f782ac20ff98a2db0734cb5`

```python
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def test_standard_coordination_files_exist() -> None:
    required = [
        "coordination/blueprint_source.yaml",
        "coordination/README.md",
        "coordination/status/current_status.yaml",
        "coordination/status/current_status.md",
        "coordination/status/next_questions_for_blueprint.md",
        "coordination/prompts/index.yaml",
        "coordination/reports/index.yaml",
    ]

    for relative_path in required:
        assert (ROOT / relative_path).exists(), relative_path


def test_blueprint_source_yaml_is_valid() -> None:
    path = ROOT / "coordination/blueprint_source.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))

    assert data["blueprint_source"]["module_id"] == "forprint_library"
    assert "forprint_system_blueprint" in data["blueprint_source"]["blueprint_root"]
    assert data["blueprint_source"]["module_directives_index_status"] in {
        "pending_blueprint_directive_index",
        "active",
    }


def test_makefile_exposes_required_standard_targets() -> None:
    text = (ROOT / "Makefile").read_text(encoding="utf-8")
    required_targets = [
        "install",
        "lint",
        "lint-fix",
        "test",
        "check",
        "check-report",
        "blueprint-pull",
        "blueprint-check",
        "blueprint-sync-directives",
        "coordination-check",
        "coordination-fix",
        "module-policy-check",
    ]

    for target in required_targets:
        assert f"{target}:" in text


def test_module_manifest_boundary_exclusions() -> None:
    data = yaml.safe_load((ROOT / "forprint_module_manifest.yaml").read_text(encoding="utf-8"))
    does_not_own = set(data["boundaries"]["does_not_own"])

    required_exclusions = {
        "client registry",
        "order registry",
        "payment registry",
        "warehouse stock truth",
        "production runtime",
        "1C synchronization",
        "CRM workflow",
        "Telegram runtime",
        "Calculator business logic",
    }

    assert required_exclusions.issubset(does_not_own)


def test_check_report_script_exists() -> None:
    path = ROOT / "scripts/run_library_checks.py"
    assert path.exists()
    assert "ForPrint Library" in path.read_text(encoding="utf-8")
```

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

## Prior L2 Block 02 supporting analysis

**Path:** `tmp/module_knowledge_analysis/forprint_library/02_dictionaries_resolution_profiles/analysis_report.md`
**SHA256:** `5ceb47259fd453982f1c722a15c250a71333591fee7a0acdbde53ce1a1dac612`

```markdown
# ForPrint Library — Module Knowledge Stabilization Pilot
## L2 Block Analysis Report — `02_dictionaries_resolution_profiles`

**Module:** `forprint_library`  
**Stage:** `L2 — Sequential Block Analysis`  
**Block:** `02_dictionaries_resolution_profiles`  
**Analysis status:** `ANALYZED_WITH_RECONCILIATION_CANDIDATES`  
**Block closeout recommendation:** `PASS_FOR_L2_WITH_CARRIED_SEMANTIC_RECONCILIATION`  
**Date:** 2026-09-24  
**Mutation performed:** false  
**Implementation authority:** none  
**Roadmap mutation authority:** none  
**Primary evidence packet:** `l2_block_02_analysis_packet.md`  
**Primary source population:** 36 files  
**Direct related-test population in this packet:** 0 files  
**Prior L2 supporting context:** Block 01 analysis  
**Blueprint/context evidence:** 8 files + 2 bounded roadmap subsets

---

# 1. Executive conclusion

Block `02_dictionaries_resolution_profiles` proves that ForPrint Library already contains a real current semantic dictionary and reference-resolution layer.

The strongest current implementation facts are:

1. A **Shared Operational Dictionary v0.1** exists and is Library-owned.

2. It currently contains **18 dictionary groups** and **158 dictionary entries**.

3. Entry lifecycle distribution in the captured evidence is:
   - 156 `active`;
   - 2 `deprecated`;
   - 0 `draft`.

4. The dictionary as a whole is nevertheless explicitly **draft / unstable / projection-only**:
   - `dictionary_status: draft_shared_operational_dictionary_v0_1`
   - `schema_status: unstable_v0_1`
   - `usage: allowed_for_projection_use`
   - `contract_status: not_final_contract`
   - `unit_dictionary_status: not_final_inventory_unit_system`

5. Current group dictionaries are exact per-group projections of the combined shared dictionary.

6. A generator script exists that currently defines the dictionary value lists, label overrides, aliases and deprecated values and writes:
   - the combined shared dictionary;
   - all group dictionary YAML files;
   - both dictionary schemas.

7. A real group-scoped resolver exists. It supports:
   - exact ID resolution;
   - alias resolution;
   - unresolved input;
   - ambiguous alias detection;
   - deprecated reference detection.

8. Dictionary identity is **group-scoped**, not globally ID-scoped:
   - IDs such as `unknown`, `cancelled`, `completed`, `in_progress` intentionally repeat across groups;
   - callers must preserve `dictionary_group` context.

9. `CatalogRegistry` source is present in this packet. This closes the Block 01 uncertainty where its behavior was test-visible but its implementation source was absent.

10. Naming profiles, profile-specific defaults, production tokens, device/equipment capability context and misspelling governance are **not implemented by the Block 02 primary source population**.

11. The packet contains **zero direct related test files** because L1 secondary test relationships did not associate tests with Block 02. Existing tests are referenced by prior Block 01 analysis, but their source is not direct evidence in this packet.

12. Several semantic and structural reconciliation candidates were discovered:
   - three overlapping resolution-status vocabularies;
   - three equivalent alias-normalization functions;
   - current dictionary generator/source-direction ambiguity at the authority/documentation level;
   - several scripts misclassified into Block 02;
   - a stale mutating coordination exporter that must not be treated as current operational authority;
   - partial Ukrainian localization;
   - no mature profile-aware naming layer despite roadmap intent.

The block is valid and useful current implementation, but it is not yet the mature target semantic-profile system.

---

# 2. Evidence boundary

This report distinguishes:

## 2.1 Current implementation evidence

The 36 files selected by the reviewed L1 Block 02 manifest.

Used to determine:

- dictionary data;
- resolver behavior;
- loader/validation implementation;
- generator direction;
- current schema/maturity;
- current semantic helper surfaces.

## 2.2 Direct test evidence

`RELATED_TEST_COUNT=0`.

Therefore this report does **not** independently claim a Block 02 pytest result from the packet.

The packet build itself passed; that is not equivalent to test execution.

## 2.3 Prior L2 supporting evidence

Block 01 analysis is present as supporting cross-block context.

It identifies existing adjacent tests for:

- dictionary policy docs;
- shared dictionary completion report;
- shared operational dictionary v0.1;
- dictionary resolver and preview.

Their presence is useful context, but their source bodies are not included as direct Block 02 test evidence.

## 2.4 Blueprint / Human Intent / roadmap context

Used for intended ownership and future direction.

Planning context does not prove implementation.

---

# 3. Block population review

The reviewed L1 manifest selected 36 primary files.

## 3.1 Strongly in-scope core implementation

### Dictionary Python layer

- `app/forprint_library/dictionaries/__init__.py`
- `app/forprint_library/dictionaries/loader.py`
- `app/forprint_library/dictionaries/models.py`
- `app/forprint_library/dictionaries/resolver.py`
- `app/forprint_library/dictionaries/validation.py`

### Semantic helpers

- `app/forprint_library/semantic/__init__.py`
- `app/forprint_library/semantic/aliases.py`
- `app/forprint_library/semantic/resolver.py`

### Dictionary data

- 18 group dictionary YAML files;
- `dictionaries/shared_operational_dictionary_v0_1.yaml`

### Schemas

- `schemas/dictionary_entry.schema.yaml`
- `schemas/shared_operational_dictionary.schema.yaml`

### Generator

- `scripts/export_shared_operational_dictionaries.py`

This generator is strongly relevant because it currently constructs and writes the dictionary population and schemas.

---

# 4. Block-boundary reclassification candidates

No file should be moved during L2.

These are reconciliation candidates only.

## RECLASS-CAND-LIB-B02-001 — Catalog registry

**Path:**
`app/forprint_library/catalog/registry.py`

**Observed responsibility:**

- loads the catalog seed;
- validates the catalog seed;
- indexes catalog entries by ID;
- builds global catalog alias index;
- resolves catalog aliases.

**Primary functional fit:**

`01_domain_semantics_catalog`

**Candidate disposition:**

`RECLASSIFY_PRIMARY_TO_01_DOMAIN_SEMANTICS_CATALOG`

This file closes Block 01 uncertainty `UNC-LIB-B01-001`.

---

## RECLASS-CAND-LIB-B02-002 — Dictionary policy document exporter

**Path:**
`scripts/export_dictionary_policy_docs.py`

**Observed responsibility:**

Writes architecture/policy documentation from embedded static strings.

**Primary functional fit:**

`07_documentation_architecture`

Potential secondary relation:

`02_dictionaries_resolution_profiles`

L1 already marked this file as a legacy candidate.

---

## RECLASS-CAND-LIB-B02-003 — Coordination artifact exporter

**Path:**
`scripts/export_shared_dictionary_coordination_artifacts.py`

**Observed responsibility:**

Mutates:

- `coordination/status/current_status.yaml`
- `coordination/status/current_status.md`
- `coordination/reports/index.yaml`
- a completion report.

**Primary functional fit:**

`06_coordination_governance_intake`

**Important safety note:**

The script embeds an earlier checkpoint state dated `2026-06-09` and writes status such as:

`shared_operational_dictionary_v0_1_ready_pending_blueprint_review`

It must not be treated as a current status authority or casually re-run during Stage 2.

Candidate disposition:

`LEGACY_OR_CHECKPOINT_SPECIFIC_MUTATING_COORDINATION_EXPORTER_RECONCILE_BEFORE_REUSE`

---

## RECLASS-CAND-LIB-B02-004 — Preview tool

**Path:**
`scripts/preview_shared_operational_dictionaries.py`

**Primary functional fit:**

`04_exports_previews_examples`

Secondary capability support:

Block 02 dictionary consumption.

---

## RECLASS-CAND-LIB-B02-005 — Reference Contract validator

**Path:**
`scripts/reference_contract/validate_library_reference_contract.py`

**Primary functional fit:**

`03_contracts_cross_module_consumption`
or
`05_validation_tests_quality`

It validates the Library Reference Contract, not the shared dictionary itself.

---

## RECLASS-CAND-LIB-B02-006 — Shared dictionary validation CLI

**Path:**
`scripts/validate_shared_operational_dictionaries.py`

**Primary functional fit:**

`05_validation_tests_quality`

It is an important validation surface for Block 02 but functionally belongs to quality/check tooling.

---

# 5. Current Shared Operational Dictionary population

The current dictionary model declares 18 groups.

| Dictionary group | Entries | Active | Deprecated | Aliases |
|---|---:|---:|---:|---:|
| `source_system` | 16 | 16 | 0 | 12 |
| `entity_type` | 23 | 23 | 0 | 1 |
| `order_status` | 10 | 10 | 0 | 8 |
| `order_line_status` | 8 | 8 | 0 | 7 |
| `payment_status` | 8 | 8 | 0 | 7 |
| `production_status` | 8 | 8 | 0 | 5 |
| `workflow_status` | 7 | 7 | 0 | 5 |
| `workflow_stage_status` | 10 | 10 | 0 | 8 |
| `material_requirement_status` | 8 | 8 | 0 | 4 |
| `reference_resolution_status` | 6 | 5 | 1 | 1 |
| `product_service_reference_status` | 6 | 5 | 1 | 1 |
| `contractor_reference_status` | 6 | 6 | 0 | 3 |
| `deadline_type` | 6 | 6 | 0 | 1 |
| `alert_rule_type` | 7 | 7 | 0 | 1 |
| `alert_severity` | 5 | 5 | 0 | 3 |
| `alert_event_status` | 6 | 6 | 0 | 1 |
| `notification_status` | 6 | 6 | 0 | 1 |
| `unit` | 12 | 12 | 0 | 8 |
| **Total** | **158** | **156** | **2** | **77** |

Every group currently includes an `unknown` entry.

No duplicate IDs within a group were observed in the captured data.

No duplicate normalized aliases within a group were observed in the captured data.

---

# 6. Critical maturity distinction

The entry field:

`status: active`

does **not** mean the dictionary contract is production-final.

Current global dictionary metadata remains:

- draft;
- schema unstable;
- projection-use only;
- not a final contract.

Therefore the correct interpretation is:

> Entries are active members of the current draft dictionary vocabulary.

Not:

> These values are final production contract values.

This distinction must be preserved in future knowledge projections.

---

# 7. Provisional capability map

Capability IDs below are L2 candidates only.

Do not finalize stable capability IDs before L3.

---

## CAP-CAND-LIB-B02-01 — Shared Operational Dictionary v0.1

**Implementation state:** `VERIFIED_CURRENT_DRAFT_PROJECTION`

**Confidence:** HIGH

### Purpose

Provide a Library-owned shared semantic vocabulary for cross-module operational/reference concepts without owning operational facts.

### Implementation

- `dictionaries/shared_operational_dictionary_v0_1.yaml`
- group YAML projections;
- dictionary schemas;
- dictionary Python loader/model/validation layer.

### Current maturity

`draft_shared_operational_dictionary_v0_1`

### Boundary

The dictionary defines language/reference semantics.

It does not create:

- real orders;
- clients;
- payments;
- stock;
- production runtime;
- Calculator pricing;
- CRM workflow;
- 1C accounting truth.

---

## CAP-CAND-LIB-B02-02 — Dictionary generator / projection builder

**Implementation state:** `VERIFIED_CURRENT`

**Confidence:** HIGH

### Implementation

`scripts/export_shared_operational_dictionaries.py`

### Observed generation direction

The script defines:

- `DICTIONARY_VALUES`
- `UK_LABEL_OVERRIDES`
- `ALIASES`
- `DEPRECATED_VALUES`
- metadata

and generates:

1. combined shared dictionary;
2. 18 group dictionary files;
3. dictionary entry schema;
4. shared dictionary schema.

The captured generated group data is consistent with the combined shared dictionary.

### Important authority question

Behaviorally, the Python generator is an upstream generation surface.

However, L2 does not establish that the generator is the formally declared human-editing authority.

Carry to L4/L5:

`GENERATOR_VS_GENERATED_DICTIONARY_AUTHORITY_REQUIRES_EXPLICIT_DECLARATION`

---

## CAP-CAND-LIB-B02-03 — Group dictionary projections

**Implementation state:** `VERIFIED_CURRENT_GENERATED_PROJECTION`

**Confidence:** HIGH

### Evidence

18 individual group YAML files.

Their `entries` are consistent with the corresponding sections of the combined shared dictionary in the captured evidence.

### Interpretation

These should not be treated as 18 unrelated independent truth stores.

Observed current pattern:

`generator definitions -> shared dictionary -> group dictionary projections`

---

## CAP-CAND-LIB-B02-04 — Dictionary loading and enumeration

**Implementation state:** `VERIFIED_CURRENT`

**Confidence:** HIGH

### Entry points

- `load_shared_dictionary(...)`
- `load_dictionary(group_name, ...)`
- `load_all_dictionaries(...)`
- `list_dictionary_groups()`

### Behavior

File-backed, read-only loading.

Unknown dictionary groups fail with `KeyError`.

---

## CAP-CAND-LIB-B02-05 — Dictionary structural validation

**Implementation state:** `VERIFIED_CURRENT`

**Confidence:** HIGH

### Validates

- metadata structure;
- expected draft maturity values;
- required entry fields;
- Library ownership;
- version `0.1`;
- allowed lifecycle statuses;
- expected dictionary group;
- duplicate IDs within groups;
- duplicate aliases within groups.

### Current schema model

Entry fields include:

- `id`
- `label_uk`
- `label_en`
- `description`
- `status`
- `aliases`
- `owner_module`
- `dictionary_group`
- `version`
- `notes`

---

## CAP-CAND-LIB-B02-06 — Group-scoped dictionary resolver

**Implementation state:** `VERIFIED_CURRENT`

**Confidence:** HIGH

### Entry point

`resolve_dictionary_value(group_name, value_or_alias, dictionary=None)`

### Resolution order

1. normalize input;
2. exact ID match;
3. alias matches;
4. detect multiple alias matches;
5. return one alias match;
6. otherwise unresolved.

### Runtime result states

- `confirmed`
- `confirmed_with_alias`
- `unresolved`
- `ambiguous_manual_review_required`
- `deprecated_reference`

### Important semantics

The resolver is group-scoped.

`group_name` is required.

This is correct for values that intentionally repeat across semantic domains.

---

## CAP-CAND-LIB-B02-07 — Ambiguity detection

**Implementation state:** `VERIFIED_CURRENT_DETECTION_ONLY`

**Confidence:** HIGH

### Entry point

`find_ambiguous_aliases(dictionary)`

### What exists

Detection of aliases that map to more than one ID within a dictionary group.

### What does not exist

No approval workflow, human-review queue, or ambiguity-resolution lifecycle is implemented in this block.

Therefore Blueprint goal:

`Define ambiguity routing and approval lifecycle`

is only partially implemented.

---

## CAP-CAND-LIB-B02-08 — Deprecated reference recognition

**Implementation state:** `VERIFIED_CURRENT_PRIMITIVE`

**Confidence:** HIGH

The dictionary resolver recognizes deprecated entries and returns:

`deprecated_reference`

The result property `is_resolved` treats deprecated references as technically resolved.

This means:

- semantic identity can be found;
- lifecycle state still warns that the reference is deprecated.

No migration/supersession graph is implemented here.

---

## CAP-CAND-LIB-B02-09 — Catalog registry / catalog alias lookup

**Implementation state:** `VERIFIED_CURRENT`

**Confidence:** HIGH

### Source

`app/forprint_library/catalog/registry.py`

### Cross-block finding

This capability belongs primarily to Block 01.

The source now confirms the behavior previously established only by tests:

- validates catalog seed;
- indexes by ID;
- builds normalized global alias index;
- `get(item_id)`;
- `resolve_alias(alias)`.

### Block 01 uncertainty resolution

`UNC-LIB-B01-001 = RESOLVED_BY_BLOCK02_SOURCE_EVIDENCE`

Carry this resolution to L3 synthesis.

---

## CAP-CAND-LIB-B02-10 — Semantic alias normalization helper

**Implementation state:** `CURRENT_BUT_THIN`

**Confidence:** HIGH

### Source

`app/forprint_library/semantic/aliases.py`

### Entry point

`normalize_semantic_alias(value)`

### Behavior

- casefold;
- trim;
- collapse whitespace.

This is currently a very small primitive.

It does not implement:

- misspelling dictionaries;
- transliteration;
- punctuation normalization;
- naming profiles;
- token context;
- device context;
- profile defaults.

---

## CAP-CAND-LIB-B02-11 — Semantic catalog resolver facade

**Implementation state:** `CURRENT_THIN_FACADE`

**Confidence:** HIGH

### Source

`app/forprint_library/semantic/resolver.py`

### Behavior

`resolve_catalog_alias(...)`

delegates directly to:

`CatalogRegistry.resolve_alias(...)`

This is not yet a unified semantic resolver.

---

# 8. Identity model: dictionary group + ID

A critical semantic rule emerges from current implementation.

Dictionary IDs are not globally unique.

Examples such as:

- `unknown`
- `cancelled`
- `completed`
- `in_progress`
- `manual_review_required`

occur in multiple dictionary groups.

Therefore the stable semantic identity is effectively:

`(dictionary_group, id)`

not:

`id`

alone.

This is reinforced by:

- `DictionaryResolutionResult.group_name`;
- group-specific loading;
- group-prefixed duplicate-alias validation.

Future contracts must preserve group context when an ID is not otherwise field-scoped unambiguously.

---

# 9. Alias behavior and normalization

## 9.1 Dictionary alias normalization

Current function:

`normalize_dictionary_lookup_value`

performs:

- `casefold()`
- trim
- whitespace collapse.

## 9.2 Catalog alias normalization

Block 01 found equivalent behavior in catalog normalization.

## 9.3 Generic semantic alias normalization

`normalize_semantic_alias`

also performs the same normalization.

### Reconciliation candidate

Three equivalent normalization primitives currently exist:

- catalog normalization;
- dictionary normalization;
- generic semantic normalization.

Candidate:

`DUP-CAND-LIB-B02-01_ALIAS_NORMALIZATION`

Disposition:

`RECONCILE_BEFORE_IMPLEMENTATION`

Do not consolidate during L2.

A future decision should determine whether:

- one shared normalizer is correct;
- namespace-specific normalizers are intentional;
- future profile-aware normalization makes them diverge.

---

# 10. Generator model limitations

The current generator stores alias definitions as:

`ALIASES[value]`

rather than:

`ALIASES[(group, value)]`

This means entries with the same ID across groups inherit the same alias list.

The same pattern applies to many label overrides.

This is acceptable for the current draft population but cannot express group/profile-specific meaning where the same token or ID needs different aliases/defaults in different contexts.

This directly matters to future naming-profile work.

Candidate:

`MODEL_LIMITATION_GROUP_OR_PROFILE_SPECIFIC_ALIAS_CONTEXT_NOT_SUPPORTED`

---

# 11. Resolution-status semantic reconciliation

This is the strongest semantic reconciliation issue found in Block 02.

There are currently at least three related status vocabularies.

## 11.1 Dictionary resolver runtime statuses

Code constants:

- `confirmed`
- `confirmed_with_alias`
- `unresolved`
- `ambiguous_manual_review_required`
- `deprecated_reference`

## 11.2 Shared dictionary `reference_resolution_status`

Current dictionary values:

- `draft_display_only`
- `reference_pending`
- `reference_confirmed`
- `ambiguous_manual_review_required`
- `deprecated_reference`
- `unknown`

## 11.3 Library Reference Contract statuses

The current Reference Contract validator expects:

- `library_reference_confirmed`
- `library_reference_pending`
- `ambiguous_manual_review_required`
- `deprecated_reference`
- `unknown`

## Interpretation

These may represent three intentionally different layers:

1. internal resolver outcome;
2. shared operational reference state;
3. cross-module Library Reference Contract state.

But their semantic overlap is high and the naming is not self-evidently mapped.

No explicit mapping layer is proven in Block 02.

### Candidate

`SEMANTIC-RECON-LIB-B02-001_RESOLUTION_STATUS_LAYER_MAPPING`

Disposition:

`RECONCILE_BEFORE_NEW_CONSUMER_IMPLEMENTATION`

Do not collapse the vocabularies automatically.

---

# 12. Catalog resolver vs dictionary resolver

These are related but distinct mechanisms.

## Catalog registry

- global catalog seed;
- ID lookup;
- global alias lookup;
- current catalog validation prevents duplicate normalized aliases;
- unknown returns `None`;
- no rich ambiguity result at runtime.

## Dictionary resolver

- explicit group context;
- exact ID then alias;
- supports ambiguity;
- supports deprecated state;
- returns structured `DictionaryResolutionResult`.

### Conclusion

They are **not exact duplicates**.

Candidate relation:

`DISTINCT_RESOLUTION_DOMAINS_WITH_SHARED_NORMALIZATION_CONCERN`

A future unified semantic facade may wrap both, but L2 does not authorize such refactor.

---

# 13. Naming profiles / production tokens assessment

The L1 block title hypothesized:

- dictionaries;
- resolution;
- naming profiles.

Current source proves the first two.

It does **not** prove the third.

No primary implementation was found for:

- naming profile objects;
- profile IDs;
- equipment/device profiles;
- production-token dictionaries;
- profile-specific defaults;
- filename grammar;
- profile-aware token resolver;
- common misspelling registry;
- profile-scoped ambiguity;
- capability context.

The only `profile`-like primary data occurrence is an entity-type value such as `legal_entity_profile`, which is not naming-profile implementation.

Therefore:

`NAMING_PROFILE_IMPLEMENTATION_PROVEN=false`

`PRODUCTION_TOKEN_IMPLEMENTATION_PROVEN=false`

`PROFILE_SPECIFIC_DEFAULTS_IMPLEMENTATION_PROVEN=false`

These remain Human Intent / roadmap targets.

---

# 14. Human Intent relation

## HI-FP-LIBRARY-002 — aliases, alternate names, normalization, provenance/confidence

**Relation:** `PARTIAL_CURRENT`

Implemented:

- aliases;
- basic normalization.

Not proven:

- supplier part numbers;
- provider provenance;
- confidence;
- ambiguous external-merge workflow.

---

## HI-FP-LIBRARY-009 — aliases, misspellings, production tokens, naming profiles/defaults

**Relation:** `PARTIAL_CURRENT`

Implemented:

- canonical aliases;
- basic dictionary/catalog resolution.

Not proven:

- common misspelling model;
- short production-token model;
- naming profiles;
- device/equipment context;
- profile-specific defaults.

---

## HI-FP-LIBRARY-010 — filename omission via profile defaults

**Relation:** `NOT_IMPLEMENTED_IN_BLOCK`

---

## HI-FP-LIBRARY-011 — same token meaning varies by profile

**Relation:** `NOT_IMPLEMENTED_IN_BLOCK`

Current generator is not profile-aware.

---

## HI-FP-LIBRARY-012 — Contract Registry/adoption flow

**Relation:** `NOT_IMPLEMENTED_IN_BLOCK`

Dependency remains roadmap-level.

---

## Semantic registry/discovery intents

Current local resolvers are useful primitives.

They do not constitute the planned shared semantic registration/discovery system.

Relation:

`EARLY_LOCAL_PRIMITIVES_ONLY`

---

# 15. Roadmap ↔ implementation relation

Roadmap and implementation states remain separate.

## FORPRINT_LIBRARY-H01
Reconcile catalog, alias, template, naming-profile and UI evidence.

**Block 02 implementation:** `PARTIAL_CURRENT`

Proven:

- aliases;
- dictionary resolution.

Not proven:

- naming profiles;
- templates;
- UI publication.

---

## FORPRINT_LIBRARY-H02
Confirm semantic ownership excluding business workflows.

**Block 02 implementation:** `CURRENT_ALIGNED`

Shared dictionary definitions remain semantic vocabulary and do not create business records.

---

## FORPRINT_LIBRARY-H03
Inventory IDs, aliases, misspellings, production tokens, templates and technical cards.

**Block 02 implementation:** `PARTIAL_CURRENT`

Proven:

- dictionary IDs;
- aliases.

Not proven:

- misspellings as a governed layer;
- production tokens;
- templates;
- technical cards.

---

## FORPRINT_LIBRARY-H04
Define versioned naming/profile/default semantics.

**Block 02 implementation:** `NOT_PROVEN`

---

## FORPRINT_LIBRARY-H08
Fast capability/semantic discovery.

**Block 02 implementation:** `LOCAL_LOOKUP_PRIMITIVES_ONLY`

---

## FORPRINT_LIBRARY-H09
Deprecation/migration for legacy aliases/profiles.

**Block 02 implementation:** `PARTIAL_PRIMITIVE`

Implemented:

- `deprecated` status;
- deprecated-reference resolver outcome.

Not implemented:

- supersession target;
- migration graph;
- adoption evidence;
- profile migration.

---

# 16. Localization assessment

The generator uses explicit Ukrainian overrides for a subset of IDs.

For values without an override, it falls back to title-casing the identifier.

As a result, many `label_uk` values are currently identical to `label_en`.

In the captured data, **68 of 158** entries have identical UK/EN label text.

Some of these are legitimate names/system identifiers.

Others are ordinary business terms and therefore indicate incomplete Ukrainian localization.

The current schema validates only non-empty strings; it does not validate language quality.

Candidate:

`QUALITY-CAND-LIB-B02-001_PARTIAL_UK_LOCALIZATION`

Do not change labels during L2.

---

# 17. Unit dictionary boundary

Current units include:

- `pcs`
- `set`
- `m`
- `m2`
- `kg`
- `g`
- `l`
- `ml`
- `hour`
- `minute`
- `service`
- `unknown`

Metadata explicitly says:

`unit_dictionary_status: not_final_inventory_unit_system`

Therefore the current unit dictionary must not be treated as:

- Warehouse inventory-unit authority;
- conversion engine;
- accounting unit system;
- measurement/calibration system.

It is a draft shared semantic vocabulary.

---

# 18. Operational-looking statuses do not create operational ownership

The dictionary includes semantic values for:

- order statuses;
- payment statuses;
- production statuses;
- workflow statuses;
- alerts;
- deadlines.

This does **not** mean Library owns:

- order state;
- payment truth;
- production runtime;
- workflow execution.

Current policy and Stage 1 reconciliation consistently preserve those boundaries.

Correct interpretation:

> Library owns shared vocabulary/reference semantics for these concepts; domain modules own the facts and transitions.

---

# 19. Validation assessment

Current Python validation verifies:

- expected dictionary metadata;
- required entry fields;
- group consistency;
- Library ownership;
- version;
- supported lifecycle status;
- duplicate IDs within groups;
- duplicate aliases within groups.

The validation CLI additionally checks:

- shared dictionary schema;
- group dictionaries;
- JSON Schemas;
- selected required IDs.

## Current-data inspection result

Within the captured dictionary population:

- no duplicate IDs within groups were observed;
- no duplicate normalized aliases within groups were observed;
- no alias-to-other-ID collision was observed.

## Validation gap candidate

Current duplicate-alias validation does not explicitly reject:

- a duplicate alias repeated twice on the same entry;
- an alias equal to another entry's ID.

No such collision was observed in current data.

Candidate:

`QUALITY-CAND-LIB-B02-002_ALIAS_ID_COLLISION_GUARD_NOT_EXPLICIT`

Low-to-medium priority; carry to L5/L8.

---

# 20. Direct test-evidence gap

The packet run report states:

`related_test_count: 0`

Yet prior Block 01 analysis identifies adjacent dictionary tests:

- `tests/contract/test_dictionary_policy_docs.py`
- `tests/contract/test_shared_dictionary_completion_report.py`
- `tests/contract/test_shared_operational_dictionary_v0_1.py`
- `tests/integration/test_dictionary_resolver_and_preview.py`

This means the issue is not necessarily absence of tests.

It is an L1 relationship/packet-selection gap.

Candidate:

`ANALYSIS-CAND-LIB-B02-001_TEST_RELATIONSHIP_UNDERLINKED`

Disposition:

- do not reopen L1;
- carry to L3/L5;
- when module-wide synthesis is created, treat these tests as likely Block 02 evidence only after their direct source is inspected in their own block or a bounded follow-up.

---

# 21. Stale mutating coordination exporter risk

`scripts/export_shared_dictionary_coordination_artifacts.py` is especially important.

It contains hard-coded checkpoint metadata from June 2026 and writes current coordination status surfaces.

If executed now, it could project an earlier module phase back into current status files.

Therefore:

`CURRENT_OPERATOR_SAFE_TO_RUN=false`

until reconciled.

Candidate:

`CLEANUP-CAND-LIB-B02-001_STALE_COORDINATION_EXPORTER`

Recommended later disposition options for L8, after authority review:

- archive;
- convert to immutable historical reproduction tool;
- guard against modern HEAD/state;
- replace with current generalized exporter;
- remove from operator surface if obsolete.

No action is authorized in L2.

---

# 22. Dictionary policy-doc generator risk

`scripts/export_dictionary_policy_docs.py` contains full policy documents as embedded static strings and overwrites architecture docs.

This creates a potential source-authority conflict between:

- script-embedded policy;
- generated docs;
- later manually maintained docs.

L1 already marked it as a legacy candidate.

Carry to L4:

`DOCUMENT_AUTHORITY_REQUIRES_RECONCILIATION`

Do not re-run casually.

---

# 23. Duplicate / overlap candidates

## DUP-CAND-LIB-B02-01 — alias normalization

Three equivalent normalization implementations.

Disposition:

`RECONCILE_BEFORE_IMPLEMENTATION`

---

## DUP-CAND-LIB-B02-02 — combined dictionary vs group YAML files

Observed generated parallel representation.

Disposition:

`INTENTIONAL_GENERATED_PROJECTION_LIKELY`

Authority direction still needs explicit documentation.

---

## DUP-CAND-LIB-B02-03 — resolver status vocabularies

Not exact duplicate data, but overlapping concepts across three layers.

Disposition:

`SEMANTIC_MAPPING_REQUIRED`

---

## DUP-CAND-LIB-B02-04 — semantic resolver wrapper

`semantic.resolver.resolve_catalog_alias` is a thin delegate to `CatalogRegistry`.

Disposition:

`POSSIBLE_COMPATIBILITY_OR_FACADE_SURFACE`

Do not remove until public-use evidence is analyzed.

---

# 24. Reuse candidates

## REUSE-CAND-LIB-B02-01 — group-scoped resolver

Potential canonical Library primitive for resolving shared dictionary values.

Consumers should consume it or its contract, rather than recreate independent vocabulary resolution.

## REUSE-CAND-LIB-B02-02 — DictionaryResolutionResult

Useful typed result pattern:

- group;
- input;
- status;
- matched ID;
- match mode;
- entry;
- candidate IDs.

## REUSE-CAND-LIB-B02-03 — dictionary metadata maturity pattern

The explicit draft/projection/not-final metadata is a useful model for preventing premature production authority.

## REUSE-CAND-LIB-B02-04 — generated group projections

Group-specific projections can serve consumers that do not need the full combined dictionary, provided source direction remains clear.

---

# 25. Migration candidates

## MIG-CAND-LIB-B02-01 — mature version/adoption lifecycle

Current `version: 0.1` and `deprecated` status are primitives only.

Future target requires:

- revision identity;
- effective dates;
- supersedes/replaced-by;
- consumer adoption state;
- migration evidence.

## MIG-CAND-LIB-B02-02 — naming/profile system

Future migration from flat aliases toward profile-aware naming may be needed.

Current implementation must not be silently retrofitted without explicit contract design.

## MIG-CAND-LIB-B02-03 — consumer shadow dictionaries

Blueprint intent says consumers should not become independent dictionary authorities.

Cross-module shadow vocabularies should be discovered later and migrated deliberately.

No external module migration is authorized by this report.

---

# 26. Wrong-owner assessment

No confirmed wrong-owner business capability was found.

The dictionary contains operational-looking terms, but only as semantic references.

No evidence in Block 02 shows Library executing:

- order transitions;
- payment posting;
- stock updates;
- production state changes;
- CRM workflows.

Therefore:

`AUTHORITY_LEAKAGE_CONFIRMED=false`

---

# 27. Architecture fit

**Architecture generation fit:**

`BLUEPRINT_ALIGNED_DRAFT_SEMANTIC_LAYER_WITH_PRE_MATURE_PROFILE_SYSTEM`

Why:

- semantic ownership aligns with Blueprint;
- operational truth remains excluded;
- dictionary maturity is explicitly draft;
- ambiguity/deprecation primitives exist;
- consumer vocabulary centralization is represented;
- profile-aware naming and mature adoption/versioning are still absent.

---

# 28. Key maturity warnings for future assistants

Do not say:

> Library has a final shared operational dictionary.

Correct:

> Library has Shared Operational Dictionary v0.1 marked draft, unstable, projection-use and not-final-contract.

Do not say:

> `active` dictionary entries are production-final.

Correct:

> `active` is entry lifecycle inside the current draft dictionary.

Do not say:

> Dictionary IDs are globally unique.

Correct:

> Dictionary identity is group-scoped; the same ID may appear in multiple groups.

Do not say:

> Library owns order/payment/production state because it defines those statuses.

Correct:

> Library owns canonical vocabulary; domain owners own operational facts.

Do not say:

> Naming profiles are implemented.

Correct:

> Naming profiles/tokens/profile defaults are current Human Intent/roadmap targets and are not proven by Block 02.

Do not say:

> There is one unified reference-resolution status model.

Correct:

> Several related status vocabularies currently coexist and require reconciliation/mapping.

---

# 29. Uncertainty / reconciliation register

## UNC-LIB-B02-001 — Formal source authority of dictionary generator

**Severity:** MEDIUM

Observed generation direction is clear.

Formal document/edit authority is not yet reconciled.

Carry to L4/L5.

## UNC-LIB-B02-002 — Direct test linkage absent

**Severity:** MEDIUM

Tests likely exist but direct Block 02 packet linkage is missing.

Carry to L3/L5.

## UNC-LIB-B02-003 — Resolution status mapping

**Severity:** HIGH for future consumer work

Three related vocabularies need explicit relationship mapping before broad new integration.

## UNC-LIB-B02-004 — Naming/profile target absent

**Severity:** EXPECTED ROADMAP GAP

No current implementation.

## UNC-LIB-B02-005 — Localization completeness

**Severity:** LOW-MEDIUM

Schema-valid but many Ukrainian labels are not actually localized.

## UNC-LIB-B02-006 — Generic semantic facade maturity

**Severity:** LOW-MEDIUM

Current semantic package is thin and not a unified resolver.

## UNC-LIB-B02-007 — stale coordination exporter

**Severity:** HIGH if executed casually

Tracked source exists but should not be treated as current operational workflow.

---

# 30. Cross-block updates

## Block 01

Resolved:

`UNC-LIB-B01-001 — CatalogRegistry implementation source absent`

New status:

`RESOLVED_BY_BLOCK02_EVIDENCE`

The source implementation is now directly visible.

## Block 03

Requires later reconciliation for:

- Library Reference Contract status vocabulary;
- Contract Registry/adoption relation;
- downstream reference-resolution mapping.

## Block 04

Requires later reconciliation for:

- preview tool;
- generated projections;
- generation/export direction.

## Block 05

Requires later reconciliation for:

- dictionary validation CLI;
- direct pytest coverage;
- schema/validation test authority.

## Block 06

Requires later reconciliation for:

- stale dictionary coordination exporter;
- checkpoint-specific completion/status mutation.

## Block 07

Requires later reconciliation for:

- generated dictionary policy documents;
- document authority vs embedded script text.

---

# 31. Evidence-to-capability matrix

| Capability candidate | Current evidence | State | Confidence |
|---|---|---|---|
| Shared Operational Dictionary v0.1 | combined YAML + model/schema | VERIFIED_CURRENT_DRAFT_PROJECTION | HIGH |
| 18 group dictionaries | group YAMLs | VERIFIED_CURRENT_GENERATED_PROJECTION | HIGH |
| dictionary generator | export script | VERIFIED_CURRENT | HIGH |
| dictionary loading | loader.py | VERIFIED_CURRENT | HIGH |
| dictionary validation | validation.py | VERIFIED_CURRENT | HIGH |
| group-scoped resolution | resolver.py | VERIFIED_CURRENT | HIGH |
| ambiguity detection | resolver.py | VERIFIED_CURRENT_DETECTION_ONLY | HIGH |
| deprecated-reference recognition | resolver/model | VERIFIED_CURRENT_PRIMITIVE | HIGH |
| CatalogRegistry implementation | catalog/registry.py | VERIFIED_CURRENT / PRIMARY FIT BLOCK01 | HIGH |
| generic semantic alias normalization | semantic/aliases.py | CURRENT_THIN_PRIMITIVE | HIGH |
| semantic catalog resolver facade | semantic/resolver.py | CURRENT_THIN_FACADE | HIGH |
| naming profiles | none | NOT_PROVEN | HIGH |
| production tokens | none | NOT_PROVEN | HIGH |
| profile-specific defaults | none | NOT_PROVEN | HIGH |
| misspelling governance | none beyond explicit aliases | NOT_PROVEN_AS_SEPARATE_LAYER | HIGH |
| mature adoption/migration lifecycle | none | NOT_PROVEN | HIGH |
| final inventory unit system | explicitly excluded | NOT_IMPLEMENTED | HIGH |

---

# 32. L2 Block 02 disposition

## Analysis result

`L2_BLOCK_02=PASS_FOR_ANALYSIS`

## Knowledge result

`CURRENT_SHARED_DICTIONARY_AND_GROUP_RESOLUTION_CORE_CONFIRMED`

## Maturity result

`DRAFT_PROJECTION_NOT_FINAL_CONTRACT`

## Naming-profile result

`NAMING_PROFILE_IMPLEMENTATION_PROVEN=false`

## Production-token result

`PRODUCTION_TOKEN_IMPLEMENTATION_PROVEN=false`

## Authority result

`SEMANTIC_VOCABULARY_OWNERSHIP_ALIGNED_NO_BUSINESS_TRUTH_LEAKAGE`

## Direct test packet result

`DIRECT_RELATED_TEST_EVIDENCE=ABSENT_DUE_TO_L1_RELATIONSHIP_GAP`

## Implementation action created

`NONE`

## Source mutation

`NONE`

## Roadmap mutation

`NONE`

---

# 33. Carry-forward to L3

Carry provisional capabilities:

- shared operational dictionary;
- dictionary generator;
- group projections;
- loader;
- validator;
- group-scoped resolver;
- ambiguity detector;
- deprecated reference handling;
- generic semantic-normalization primitive;
- thin semantic resolver facade.

Carry cross-block correction:

- CatalogRegistry belongs primarily with catalog semantics and closes Block 01 source gap.

Carry unresolved semantic reconciliation:

- resolver-status layer mapping;
- alias-normalization duplication;
- generator authority;
- profile-aware future model.

Do not finalize stable capability IDs until all L2 blocks are complete.

---

# 34. Carry-forward to L4

Document authority review must include:

- dictionary policy docs;
- dictionary versioning policy;
- dictionary consumption policy;
- generator-embedded policy strings;
- shared dictionary maturity metadata;
- stale coordination completion report/status exporter.

Key question:

> Which artifact is current authority, and which is generated/supporting/historical?

---

# 35. Carry-forward to L5

Capability reconciliation must explicitly decide:

1. catalog normalization vs dictionary normalization vs semantic normalization;
2. catalog resolver vs dictionary resolver vs Reference Contract resolution status;
3. generator source vs generated YAML authority;
4. generic semantic facade responsibility;
5. profile-aware naming architecture;
6. deprecation/migration lifecycle;
7. whether group-scoped dictionary identity needs a formal reference type.

---

# 36. Next sequential block

Per L1 closeout order:

`03_contracts_cross_module_consumption`

Before moving forward, preserve this report as:

`tmp/module_knowledge_analysis/forprint_library/02_dictionaries_resolution_profiles/analysis_report.md`

Do not commit/push the temporary pilot analysis workspace yet.

---

# 37. Final statement

Block 02 proves that ForPrint Library already has a substantial shared semantic vocabulary and deterministic group-scoped resolution implementation.

The accurate current description is:

> Library owns a draft Shared Operational Dictionary v0.1 with 18 groups, 158 current semantic entries, generated group projections, schemas, validation, aliases and deterministic group-scoped resolution including ambiguity and deprecation handling. This is a semantic/reference layer only. It is not a final contract, operational state engine, final inventory-unit system, or naming-profile system.

The most important reconciliation requirement discovered here is that several overlapping resolution-status vocabularies and normalization surfaces currently coexist. Future integrations should not invent another variant before these are mapped during L5.

**Final L2 Block 02 status: `PASS_FOR_ANALYSIS_WITH_SEMANTIC_RECONCILIATION_CANDIDATES`.**
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

**Path:** `tmp/module_knowledge_analysis/forprint_library/03_contracts_cross_module_consumption/l2_packet/context/blueprint_roadmap_subsets/portfolio_full_horizon_target_states_v0_1__forprint_library_subset.yaml`
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

**Path:** `tmp/module_knowledge_analysis/forprint_library/03_contracts_cross_module_consumption/l2_packet/context/blueprint_roadmap_subsets/portfolio_module_roadmap_approval_matrix_v0_1__forprint_library_subset.yaml`
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

Evidence/provenance items recorded: **57**

See `l2_packet/packet_manifest.yaml` for the machine-readable ledger.
