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