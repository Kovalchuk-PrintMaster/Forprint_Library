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