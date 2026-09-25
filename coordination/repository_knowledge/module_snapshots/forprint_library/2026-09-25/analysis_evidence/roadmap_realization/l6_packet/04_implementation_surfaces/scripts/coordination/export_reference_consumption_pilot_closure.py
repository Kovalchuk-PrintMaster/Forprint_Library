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