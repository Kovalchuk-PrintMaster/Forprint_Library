from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]

REPORT_ID = (
    "2026-06-25__forprint_library__report__"
    "make-first-semantic-reference-readiness-v0-1"
)
REPORT_PATH = ROOT / "coordination" / "reports" / "completion" / f"{REPORT_ID}.md"


def test_make_first_semantic_readiness_completion_report_exists() -> None:
    assert REPORT_PATH.exists()

    text = REPORT_PATH.read_text(encoding="utf-8")

    for expected in [
        "Makefile targets added or aligned",
        "Semantic/reference readiness files",
        "Check-report visibility",
        "Completion packet automation",
        "Blueprint review request",
        "28fe2d0",
    ]:
        assert expected in text


def test_current_status_marks_make_first_semantic_readiness_complete() -> None:
    data = yaml.safe_load(
        (ROOT / "coordination" / "status" / "current_status.yaml").read_text(
            encoding="utf-8"
        )
    )

    assert (
        data["status"]
        == "make_first_semantic_reference_readiness_v0_1_ready_pending_blueprint_review"
    )
    assert data["current_phase"] == "make_first_semantic_reference_readiness_v0_1"
    assert data["last_completed_step"] == "make_first_semantic_reference_ready"

    readiness = data["make_first_semantic_reference_readiness_v0_1"]

    assert readiness["implementation_commit"] == "28fe2d0"
    assert readiness["completion_packet_automation"] == "deferred_safe_not_faked"
    assert readiness["status"] == "completed_pending_blueprint_review"


def test_reports_index_references_make_first_semantic_readiness_report() -> None:
    data = yaml.safe_load(
        (ROOT / "coordination" / "reports" / "index.yaml").read_text(
            encoding="utf-8"
        )
    )

    completion_ids = {
        item["id"]
        for item in data.get("completion_reports", [])
        if isinstance(item, dict)
    }

    assert REPORT_ID in completion_ids


def test_current_status_md_mentions_blueprint_review() -> None:
    text = (
        ROOT / "coordination" / "status" / "current_status.md"
    ).read_text(encoding="utf-8")

    assert "make_first_semantic_reference_readiness_v0_1" in text
    assert "Wait for Blueprint review" in text