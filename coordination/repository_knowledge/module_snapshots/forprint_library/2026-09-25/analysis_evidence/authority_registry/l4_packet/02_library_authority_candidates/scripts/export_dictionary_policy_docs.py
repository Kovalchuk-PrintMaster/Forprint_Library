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