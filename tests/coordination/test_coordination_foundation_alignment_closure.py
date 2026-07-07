from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]

REPORT_ID = (
    "2026-07-03__forprint_library__report__"
    "coordination-foundation-alignment-v0-1"
)
REPORT_PATH = ROOT / "coordination" / "reports" / "completion" / f"{REPORT_ID}.md"


def test_coordination_foundation_alignment_completion_report_exists() -> None:
    assert REPORT_PATH.exists()

    text = REPORT_PATH.read_text(encoding="utf-8")

    for expected in [
        "ForPrint Library Coordination Foundation Alignment v0.1",
        "Library coordination foundation alignment",
        "Coordination workflow, document awareness and alignment notes validate",
        "02e2cad",
        "Product modeling has not started",
    ]:
        assert expected in text


def test_current_status_marks_coordination_foundation_alignment_complete() -> None:
    data = yaml.safe_load(
        (ROOT / "coordination" / "status" / "current_status.yaml").read_text(
            encoding="utf-8"
        )
    )

    assert (
        data["status"]
        == "coordination_foundation_alignment_v0_1_ready_pending_blueprint_review"
    )
    assert data["current_phase"] == "coordination_foundation_alignment_v0_1"
    assert (
        data["last_completed_step"]
        == "library_coordination_foundation_alignment_ready"
    )

    checkpoint = data["coordination_foundation_alignment_v0_1"]

    assert checkpoint["implementation_commit"] == "02e2cad"
    assert checkpoint["check_report_visibility"] == "done"
    assert checkpoint["workbench_started"] is False
    assert checkpoint["product_modeling_started"] is False
    assert checkpoint["production_runtime_changes"] is False


def test_reports_index_references_coordination_foundation_report() -> None:
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


def test_current_status_md_mentions_coordination_foundation() -> None:
    text = (
        ROOT / "coordination" / "status" / "current_status.md"
    ).read_text(encoding="utf-8")

    assert "coordination_foundation_alignment_v0_1" in text
    assert "Makefile was not rewritten" in text
    assert "No real secrets or credentials were committed" in text