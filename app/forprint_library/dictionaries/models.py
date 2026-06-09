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