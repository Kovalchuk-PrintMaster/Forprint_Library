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