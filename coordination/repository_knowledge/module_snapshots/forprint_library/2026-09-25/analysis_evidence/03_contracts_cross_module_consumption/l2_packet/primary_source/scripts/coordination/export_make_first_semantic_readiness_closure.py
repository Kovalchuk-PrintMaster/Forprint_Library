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