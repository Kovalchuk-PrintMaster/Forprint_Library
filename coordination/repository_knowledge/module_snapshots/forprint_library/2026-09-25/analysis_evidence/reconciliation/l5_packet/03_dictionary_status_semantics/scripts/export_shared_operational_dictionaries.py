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