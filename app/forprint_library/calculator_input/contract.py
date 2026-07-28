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
