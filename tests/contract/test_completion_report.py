from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]

REPORT_ID = (
    "2026-06-06__forprint_library__report__catalog-seed-v0-1-and-coordination-bootstrap"
)
REPORT_PATH = ROOT / "coordination" / "reports" / "completion" / f"{REPORT_ID}.md"


def test_completion_report_exists() -> None:
    assert REPORT_PATH.exists()


def test_completion_report_contains_required_sections() -> None:
    text = REPORT_PATH.read_text(encoding="utf-8").casefold()

    for phrase in [
        "files added or changed",
        "catalog seed contents summary",
        "schemas added",
        "tests added or updated",
        "check-report behavior",
        "makefile targets",
        "coordination files",
        "boundary confirmation",
        "open questions for blueprint",
        "recommended next step",
    ]:
        assert phrase in text


def test_reports_index_references_completion_report() -> None:
    data = yaml.safe_load(
        (ROOT / "coordination" / "reports" / "index.yaml").read_text(encoding="utf-8")
    )

    reports = data["completion_reports"]
    report_ids = {item["id"] for item in reports}

    assert REPORT_ID in report_ids


def test_current_status_keeps_known_project_phase() -> None:
    data = yaml.safe_load(
        (ROOT / "coordination" / "status" / "current_status.yaml").read_text(
            encoding="utf-8"
        )
    )

    known_statuses = {
        "bootstrap_completed_pending_blueprint_review",
        "shared_operational_dictionary_v0_1_ready_pending_blueprint_review",
        "make_first_semantic_reference_readiness_v0_1_ready_pending_blueprint_review",
    },
    known_statuses = {
        "bootstrap_completed_pending_blueprint_review",
        "shared_operational_dictionary_v0_1_ready_pending_blueprint_review",
        "make_first_semantic_reference_readiness_v0_1_ready_pending_blueprint_review",
        "reference_contract_foundation_v0_2_ready_pending_blueprint_review",
    }

    assert data["status"] in known_statuses
    assert data["module_id"] == "forprint_library"
    assert data["owner_module"] == "forprint_library"