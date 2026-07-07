from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]

PROMPT_ID = "library_coordination_foundation_alignment_v0_1"
BLUEPRINT_PROMPT_PATH = (
    "/srv/software_development/forprint-project/forprint_system_blueprint/"
    "coordination/outgoing_prompts/forprint_library/approved/"
    "2026-07-03__library__coordination_foundation_alignment_v0_1.md"
)

IMPLEMENTATION_COMMIT = "02e2cad"
IMPLEMENTATION_COMMIT_MESSAGE = "Add Library coordination foundation alignment"

REPORT_ID = (
    "2026-07-03__forprint_library__report__"
    "coordination-foundation-alignment-v0-1"
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
        "coordination_foundation_alignment_v0_1_"
        "ready_pending_blueprint_review"
    )
    data["stage"] = "coordination_foundation_alignment_v0_1_completion"
    data["updated_at"] = "2026-07-03"
    data["current_phase"] = "coordination_foundation_alignment_v0_1"
    data["last_completed_step"] = "library_coordination_foundation_alignment_ready"

    data["current_focus"] = [
        "Library coordination foundation alignment v0.1 completed",
        "prompt queue navigation confirmed",
        "document awareness confirmed",
        "context bundle no-write flow confirmed",
        "configuration and secrets policy documented",
        "project tree alignment notes documented",
        "Workbench and product modeling explicitly not started",
    ]

    data["coordination_foundation_alignment_v0_1"] = {
        "prompt_id": PROMPT_ID,
        "blueprint_prompt_path": BLUEPRINT_PROMPT_PATH,
        "implementation_commit": IMPLEMENTATION_COMMIT,
        "implementation_commit_message": IMPLEMENTATION_COMMIT_MESSAGE,
        "completion_report_id": REPORT_ID,
        "completion_report_path": str(REPORT_PATH.relative_to(ROOT)),
        "status": "completed_pending_blueprint_review",
        "makefile_rewrite": "not_needed",
        "operator_workflow": "confirmed",
        "prompt_queue_navigation": "confirmed",
        "document_awareness": "confirmed",
        "context_bundle_no_write": "confirmed",
        "configuration_policy": "documented_deferred_until_needed",
        "secrets_policy": "not_applicable_no_secrets_added",
        "project_tree_alignment": "documented",
        "check_report_visibility": "done",
        "tests": "104_passed",
        "workbench_started": False,
        "product_modeling_started": False,
        "production_runtime_changes": False,
    }

    data["next_recommended_step"] = {
        "status": "wait_for_blueprint_review",
        "recommended_action": (
            "Ask Blueprint to review Library coordination foundation "
            "alignment v0.1 and confirm readiness for the next prompt."
        ),
        "candidate_next_prompt": (
            "Library Configurable Product Workbench v0.1 — "
            "Business Card Skeleton"
        ),
    }

    write_yaml(STATUS_YAML, data)


def update_current_status_md() -> None:
    lines = [
        "# ForPrint Library Current Status",
        "",
        "## Status",
        "",
        "`coordination_foundation_alignment_v0_1_ready_pending_blueprint_review`",
        "",
        "## Current phase",
        "",
        "`coordination_foundation_alignment_v0_1`",
        "",
        "## Last completed step",
        "",
        "`library_coordination_foundation_alignment_ready`",
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
        "- Coordination foundation alignment document.",
        "- Local Blueprint awareness alignment YAML.",
        "- Coordination foundation alignment validator.",
        "- Focused coordination tests.",
        "- Check-report row for coordination foundation alignment.",
        "- Configuration, secrets and project-tree alignment notes.",
        "",
        "## Validation result",
        "",
        "```text",
        "coordination foundation validator: OK",
        "make lint: OK",
        "make test: 104 passed",
        "make check-report: OK",
        "make check: OK",
        "make governance-check: OK",
        "make module-validate: OK",
        "```",
        "",
        "## Makefile policy",
        "",
        "Makefile was not rewritten.",
        "",
        "Existing operator targets were confirmed sufficient for this checkpoint.",
        "",
        "## Manual Blueprint mode",
        "",
        "Blueprint communication is temporarily handled through chat.",
        "",
        "The active prompt was handled through `prompt-read-next` and manual",
        "operator coordination.",
        "",
        "## Configuration and secrets",
        "",
        "No production config was added.",
        "",
        "No `.env` file was added.",
        "",
        "No real secrets or credentials were committed.",
        "",
        "Secrets checks are not applicable for the current Library scope.",
        "",
        "## Non-goals preserved",
        "",
        "This checkpoint did not implement:",
        "",
        "```text",
        "Configurable Product Workbench",
        "business_card product skeleton",
        "new product catalog generation",
        "1C import",
        "1C database parsing",
        "Calculator Engine integration",
        "production write",
        "price calculation",
        "material write-off logic",
        "CRM/client/carrier entities",
        "large repository refactor",
        "production catalog database",
        "live API",
        "runtime integration",
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
        "Wait for Blueprint review.",
        "",
        "Candidate next prompt:",
        "",
        "```text",
        "Library Configurable Product Workbench v0.1 — Business Card Skeleton",
        "```",
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
            "created_at": "2026-07-03",
        },
    )

    commit_reports = ensure_list(data, "commit_reports")
    upsert_by_id(
        commit_reports,
        {
            "id": "forprint_library_coordination_foundation_alignment_commit_02e2cad",
            "module_id": "forprint_library",
            "type": "commit_report",
            "status": "pushed",
            "commit": IMPLEMENTATION_COMMIT,
            "message": IMPLEMENTATION_COMMIT_MESSAGE,
            "related_prompt_id": PROMPT_ID,
            "created_at": "2026-07-03",
        },
    )

    write_yaml(REPORTS_INDEX, data)


def write_completion_report() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# ForPrint Library Coordination Foundation Alignment v0.1",
        "",
        "## Completion Report",
        "",
        f"Report ID: `{REPORT_ID}`",
        "",
        "Module: `forprint_library`",
        "",
        "Status: `completed_pending_blueprint_review`",
        "",
        "Date: `2026-07-03`",
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
        "docs/architecture/coordination_foundation_alignment.md",
        "coordination/blueprint_awareness/library_coordination_foundation_alignment_v0_1.yaml",
        "scripts/coordination/validate_coordination_foundation_alignment.py",
        "tests/coordination/test_coordination_foundation_alignment.py",
        "scripts/run_library_checks.py",
        "reports/library_check_report.json",
        "reports/library_check_report.md",
        "```",
        "",
        "## Structural and coordination scope completed",
        "",
        "- Makefile/operator workflow inspected and confirmed.",
        "- Prompt queue navigation confirmed through `prompt-read-next`.",
        "- Document awareness dashboard confirmed.",
        "- Context bundle no-write flow confirmed.",
        "- Module validation confirmed.",
        "- Configuration architecture documented as deferred until needed.",
        "- Secrets and `.env` policy documented as not applicable for this scope.",
        "- Project tree alignment notes documented.",
        "- Completion reporting prepared.",
        "",
        "## Check-report visibility",
        "",
        "The check report now includes:",
        "",
        "```text",
        "Library coordination foundation alignment",
        "```",
        "",
        "Expected result:",
        "",
        "```text",
        "Coordination workflow, document awareness and alignment notes validate",
        "```",
        "",
        "Status: `OK`.",
        "",
        "## Validation results",
        "",
        "```text",
        "coordination foundation validator: OK",
        "make lint: OK",
        "make test: 104 passed",
        "make check-report: OK",
        "make check: OK",
        "make governance-check: OK",
        "make module-validate: OK",
        "git diff --check: OK",
        "```",
        "",
        "## Deferred items",
        "",
        "```text",
        "formal exhaustive review of all unseen Blueprint standards",
        "config/ runtime configuration",
        ".env.example",
        "secrets-check implementation",
        "Configurable Product Workbench",
        "business_card product skeleton",
        "1C import",
        "Calculator Engine integration",
        "production catalog database",
        "live API",
        "runtime integrations",
        "large repository refactor",
        "```",
        "",
        "## Readiness statement",
        "",
        "Library is coordination-ready for the next Blueprint-controlled prompt.",
        "",
        "Product modeling has not started.",
        "",
        "## Blueprint review request",
        "",
        "Blueprint should review this coordination foundation alignment and",
        "confirm whether Library may proceed to:",
        "",
        "```text",
        "Library Configurable Product Workbench v0.1 — Business Card Skeleton",
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