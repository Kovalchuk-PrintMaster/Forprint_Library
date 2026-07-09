from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]

REPORT_ID = "2026-07-08__forprint_library__report__reference-consumption-pilot-v0-3"
PROMPT_ID = "library_reference_consumption_pilot_v0_3"
IMPLEMENTATION_COMMIT = "7e000cb"

REPORT = ROOT / "coordination" / "reports" / "completion" / f"{REPORT_ID}.md"
REPORTS_INDEX = ROOT / "coordination" / "reports" / "index.yaml"
STATUS_YAML = ROOT / "coordination" / "status" / "current_status.yaml"
STATUS_MD = ROOT / "coordination" / "status" / "current_status.md"
NEXT_QUESTIONS = ROOT / "coordination" / "status" / "next_questions_for_blueprint.md"


def load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def test_reference_consumption_completion_report_exists() -> None:
    assert REPORT.exists()

    text = REPORT.read_text(encoding="utf-8")

    assert "Library Reference Consumption Pilot v0.3" in text
    assert PROMPT_ID in text
    assert IMPLEMENTATION_COMMIT in text
    assert "Library reference consumption pilot" in text
    assert "completed_pending_blueprint_review" in text
    assert "No Configurable Product Workbench" in text
    assert "No Blueprint repository writes" in text


def test_reference_consumption_report_index_updated() -> None:
    data = load_yaml(REPORTS_INDEX)

    reports = data["completion_reports"]
    matching = [item for item in reports if item["id"] == REPORT_ID]

    assert len(matching) == 1

    report = matching[0]
    assert report["module_id"] == "forprint_library"
    assert report["type"] == "completion_report"
    assert report["status"] == "completed_pending_blueprint_review"
    assert report["related_prompt_id"] == PROMPT_ID
    assert report["implementation_commit"] == IMPLEMENTATION_COMMIT


def test_reference_consumption_commit_record_indexed() -> None:
    data = load_yaml(REPORTS_INDEX)

    commit_reports = data["commit_reports"]
    matching = [
        item
        for item in commit_reports
        if item["id"] == "forprint_library_reference_consumption_pilot_commit_7e000cb"
    ]

    assert len(matching) == 1

    commit = matching[0]
    assert commit["module_id"] == "forprint_library"
    assert commit["type"] == "commit_record"
    assert commit["status"] == "pushed"
    assert commit["commit"] == IMPLEMENTATION_COMMIT
    assert commit["related_prompt_id"] == PROMPT_ID


def test_reference_consumption_current_status_updated() -> None:
    data = load_yaml(STATUS_YAML)

    assert data["status"] == (
        "reference_consumption_pilot_v0_3_ready_pending_blueprint_review"
    )
    assert data["current_phase"] == "reference_consumption_pilot_v0_3"

    checkpoint = data["reference_consumption_pilot_v0_3"]
    assert checkpoint["status"] == "completed_pending_blueprint_review"
    assert checkpoint["prompt_id"] == PROMPT_ID
    assert checkpoint["implementation_commit"] == IMPLEMENTATION_COMMIT
    assert checkpoint["validation"]["full_tests"] == "115 passed"

    boundaries = checkpoint["boundaries"]
    assert boundaries["configurable_product_workbench_started"] is False
    assert boundaries["blueprint_repository_written"] is False
    assert boundaries["price_calculation_added"] is False
    assert boundaries["material_write_off_added"] is False


def test_reference_consumption_status_markdown_updated() -> None:
    text = STATUS_MD.read_text(encoding="utf-8")

    assert "reference_consumption_pilot_v0_3_ready_pending_blueprint_review" in text
    assert PROMPT_ID in text
    assert IMPLEMENTATION_COMMIT in text
    assert "No Configurable Product Workbench" in text
    assert "No Blueprint repository writes" in text


def test_reference_consumption_next_questions_updated() -> None:
    text = NEXT_QUESTIONS.read_text(encoding="utf-8")

    assert PROMPT_ID in text
    assert "completed_pending_blueprint_review" in text
    assert f"coordination/reports/completion/{REPORT_ID}.md" in text