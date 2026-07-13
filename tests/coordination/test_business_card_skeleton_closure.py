
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]

PROMPT_ID = "library_configurable_product_workbench_business_card_skeleton_v0_1"
REPORT_ID = "2026-07-11__forprint_library__report__business-card-skeleton-v0-1"
IMPLEMENTATION_COMMIT = "b8eb062"

REPORT = ROOT / "coordination" / "reports" / "completion" / f"{REPORT_ID}.md"
REPORTS_INDEX = ROOT / "coordination" / "reports" / "index.yaml"
CURRENT_STATUS_YAML = ROOT / "coordination" / "status" / "current_status.yaml"
CURRENT_STATUS_MD = ROOT / "coordination" / "status" / "current_status.md"
NEXT_QUESTIONS = ROOT / "coordination" / "status" / "next_questions_for_blueprint.md"


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def assert_clean_text_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    assert text.endswith("\n")
    assert not text.endswith("\n\n")


def test_business_card_completion_report_exists() -> None:
    assert REPORT.exists()
    text = REPORT.read_text(encoding="utf-8")

    assert PROMPT_ID in text
    assert IMPLEMENTATION_COMMIT in text
    assert "product.business_card" in text
    assert "catalog/configurable_products/business_card.yaml" in text
    assert "schemas/configurable_product.schema.yaml" in text
    assert "Business card product skeleton" in text
    assert "Business card product preview" in text
    assert "No Blueprint repository writes" in text
    assert "No price calculation" in text
    assert "No final price formula" in text
    assert "No material write-off logic" in text
    assert "No open questions" in text


def test_business_card_completion_report_mentions_completion_packet_boundary() -> None:
    text = REPORT.read_text(encoding="utf-8")

    assert "Generic completion packet automation was not available" in text
    assert "Library-side exporter generated" in text
    assert "No files were written directly into the Blueprint repository" in text


def test_reports_index_contains_business_card_completion_report() -> None:
    data = load_yaml(REPORTS_INDEX)
    reports = data["reports"]

    matching = [
        report
        for report in reports
        if isinstance(report, dict) and report.get("id") == REPORT_ID
    ]
    assert len(matching) == 1

    report = matching[0]
    assert report["prompt_id"] == PROMPT_ID
    assert report["implementation_commit"] == IMPLEMENTATION_COMMIT
    assert report["status"] == "completed_pending_blueprint_review"


def test_current_status_yaml_tracks_business_card_checkpoint() -> None:
    data = load_yaml(CURRENT_STATUS_YAML)

    assert data["status"] == "business_card_skeleton_v0_1_ready_pending_blueprint_review"
    assert data["current_phase"] == "business_card_skeleton_v0_1"
    assert data["last_completed_step"] == "library_business_card_skeleton_ready"

    checkpoint = data["configurable_product_workbench_business_card_skeleton_v0_1"]
    assert checkpoint["prompt_id"] == PROMPT_ID
    assert checkpoint["status"] == "completed_pending_blueprint_review"
    assert checkpoint["implementation_commit"] == IMPLEMENTATION_COMMIT
    assert checkpoint["product_id"] == "product.business_card"

    assert checkpoint["boundaries"]["price_calculation_added"] is False
    assert checkpoint["boundaries"]["final_price_formula_added"] is False
    assert checkpoint["boundaries"]["material_write_off_added"] is False
    assert checkpoint["boundaries"]["blueprint_repository_written"] is False


def test_current_status_yaml_preserves_previous_history() -> None:
    data = load_yaml(CURRENT_STATUS_YAML)

    assert "make_first_semantic_reference_readiness_v0_1" in data
    assert "reference_contract_foundation_v0_2" in data
    assert "coordination_foundation_alignment_v0_1" in data
    assert "reference_consumption_pilot_v0_3" in data


def test_current_status_md_mentions_business_card_checkpoint() -> None:
    text = CURRENT_STATUS_MD.read_text(encoding="utf-8")

    assert PROMPT_ID in text
    assert "business_card_skeleton_v0_1_ready_pending_blueprint_review" in text
    assert "product.business_card" in text
    assert "No full product catalog" in text
    assert "No 1C import" in text
    assert "No Calculator integration" in text
    assert "No Telegram Bot integration" in text
    assert "No Operational Registry write" in text
    assert "No Blueprint repository writes" in text
    assert "Previous completed checkpoints" in text
    assert "reference_consumption_pilot_v0_3" in text


def test_next_questions_has_no_open_questions() -> None:
    text = NEXT_QUESTIONS.read_text(encoding="utf-8")

    assert PROMPT_ID in text
    assert "No open questions" in text
    assert f"coordination/reports/completion/{REPORT_ID}.md" in text


def test_business_card_closure_text_files_are_clean() -> None:
    assert_clean_text_file(REPORT)
    assert_clean_text_file(CURRENT_STATUS_MD)
    assert_clean_text_file(NEXT_QUESTIONS)