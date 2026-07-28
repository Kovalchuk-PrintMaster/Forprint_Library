from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REPORT = (
    ROOT
    / "coordination"
    / "reports"
    / "completion"
    / "forprint_library_calculator_input_contract_v0_1_completion.md"
)


def test_calculator_input_contract_completion_report_exists() -> None:
    assert REPORT.exists()


def test_calculator_input_contract_completion_report_records_prompt_and_result() -> None:
    text = REPORT.read_text(encoding="utf-8")

    assert "forprint_library_calculator_input_contract_v0_1" in text
    assert "RESULT: READY_FOR_BLUEPRINT_REVIEW" in text
    assert "completed_pending_blueprint_review" in text
    assert "product.business_card" in text


def test_calculator_input_contract_completion_report_records_artifacts() -> None:
    text = REPORT.read_text(encoding="utf-8")

    required_paths = [
        "app/forprint_library/calculator_input/contract.py",
        "schemas/calculator_input/calculator_input_envelope.schema.yaml",
        "examples/calculator_input_contract/minimal_valid_business_card.yaml",
        "scripts/calculator_input/validate_calculator_input_contract.py",
        "tests/content/test_calculator_input_contract.py",
        "docs/architecture/library_calculator_input_contract.md",
        "docs/operations/library_calculator_input_contract_runbook.md",
        "docs/operations/library_calculator_input_contract_recovery.md",
    ]

    for path in required_paths:
        assert path in text


def test_calculator_input_contract_completion_report_records_validation() -> None:
    text = REPORT.read_text(encoding="utf-8")

    assert "25 passed" in text
    assert "160 passed" in text
    assert "LINT_EXIT: 0" in text
    assert "FORMAT_CHECK_EXIT: 0" in text
    assert "CHECK_EXIT: 0" in text
    assert "GOVERNANCE_CHECK_EXIT: 0" in text
    assert "MODULE_VALIDATE_EXIT: 0" in text
    assert "CHECK_REPORT_EXIT: 0" in text
    assert "CHECK_REPORT_FULL_EXIT: 0" in text
    assert "DIFF_CHECK_FINAL_EXIT: 0" in text


def test_calculator_input_contract_completion_report_records_boundaries() -> None:
    text = REPORT.read_text(encoding="utf-8")

    forbidden_scope = [
        "price formulas",
        "quote totals",
        "Calculator internals",
        "Telegram Bot changes",
        "Logistics changes",
        "CRM changes",
        "Gateway changes",
        "1C changes",
        "stock writes",
        "production writes",
        "Blueprint repository writes",
    ]

    for item in forbidden_scope:
        assert item in text
