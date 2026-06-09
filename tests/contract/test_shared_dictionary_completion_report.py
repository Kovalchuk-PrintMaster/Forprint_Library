from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]

REPORT_ID = "2026-06-09__forprint_library__report__shared-operational-dictionary-v0-1"
REPORT_PATH = ROOT / "coordination" / "reports" / "completion" / f"{REPORT_ID}.md"


def test_shared_dictionary_completion_report_exists() -> None:
    assert REPORT_PATH.exists()


def test_shared_dictionary_completion_report_contains_required_sections() -> None:
    text = REPORT_PATH.read_text(encoding="utf-8").casefold()

    for phrase in [
        "files added or changed",
        "dictionary groups added",
        "schemas added",
        "loader and resolver behavior",
        "examples added",
        "terminal preview summary",
        "architecture docs added",
        "tests added and results",
        "check-report result",
        "makefile targets added",
        "coordination status and report updates",
        "boundary confirmation",
        "open questions for blueprint",
        "recommended next step",
    ]:
        assert phrase in text


def test_reports_index_references_shared_dictionary_completion_report() -> None:
    data = yaml.safe_load(
        (ROOT / "coordination" / "reports" / "index.yaml").read_text(
            encoding="utf-8"
        )
    )

    report_ids = {item["id"] for item in data["completion_reports"]}

    assert REPORT_ID in report_ids


def test_current_status_marks_shared_dictionary_ready() -> None:
    data = yaml.safe_load(
        (ROOT / "coordination" / "status" / "current_status.yaml").read_text(
            encoding="utf-8"
        )
    )

    assert data["current_phase"] == "shared_operational_dictionary_v0_1"
    assert data["last_completed_step"] == "shared_operational_dictionary_ready"
    assert (
        data["status"]
        == "shared_operational_dictionary_v0_1_ready_pending_blueprint_review"
    )