from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]

REPORT_ID = (
    "2026-06-29__forprint_library__report__"
    "reference-contract-foundation-v0-2"
)
REPORT_PATH = ROOT / "coordination" / "reports" / "completion" / f"{REPORT_ID}.md"


def test_reference_contract_foundation_completion_report_exists() -> None:
    assert REPORT_PATH.exists()

    text = REPORT_PATH.read_text(encoding="utf-8")

    for expected in [
        "ForPrint Library Reference Contract Foundation v0.2",
        "Library reference contract foundation",
        "Reference contract docs, schemas and examples validate",
        "78bd7e1",
        "Makefile active prompt was intentionally not changed",
    ]:
        assert expected in text


def test_current_status_keeps_reference_contract_foundation_record() -> None:
    data = yaml.safe_load(
        (ROOT / "coordination" / "status" / "current_status.yaml").read_text(
            encoding="utf-8"
        )
    )

    assert data["module_id"] == "forprint_library"
    assert data["owner_module"] == "forprint_library"

    checkpoint = data["reference_contract_foundation_v0_2"]

    assert checkpoint["implementation_commit"] == "78bd7e1"
    assert checkpoint["check_report_visibility"] == "done"
    assert checkpoint["makefile_changes"] == "not_changed_manual_blueprint_mode"
    assert checkpoint["status"] in {
        "completed_pending_blueprint_review",
        "accepted_by_blueprint",
    }

def test_reports_index_references_reference_contract_foundation_report() -> None:
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


def test_reference_contract_report_mentions_manual_blueprint_mode() -> None:
    text = REPORT_PATH.read_text(encoding="utf-8")

    assert "reference_contract_foundation_v0_2" in text
    assert "Makefile active prompt was intentionally not changed" in text
    assert "manual" in text.lower()