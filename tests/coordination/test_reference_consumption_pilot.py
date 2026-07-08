from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = (
    ROOT
    / "scripts"
    / "reference_consumption"
    / "validate_reference_consumption_pilot.py"
)
EXAMPLES = (
    ROOT
    / "examples"
    / "reference_consumption"
    / "library_reference_consumption_examples.yaml"
)
SCHEMA = (
    ROOT
    / "schemas"
    / "reference_consumption"
    / "library_reference_consumption.schema.yaml"
)
DOC = ROOT / "docs" / "architecture" / "reference_consumption_pilot.md"


def run_validator(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )


def load_examples() -> dict:
    data = yaml.safe_load(EXAMPLES.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def test_reference_consumption_files_exist() -> None:
    assert SCRIPT.exists()
    assert EXAMPLES.exists()
    assert SCHEMA.exists()
    assert DOC.exists()


def test_reference_consumption_validator_passes() -> None:
    result = run_validator()

    assert "OK: Library reference consumption pilot validates" in result.stdout


def test_reference_consumption_preview_renders() -> None:
    result = run_validator("--preview")

    assert "ForPrint Library Reference Consumption Pilot v0.3" in result.stdout
    assert "Consumer: calculator_engine" in result.stdout
    assert "product_service.business_card.standard" in result.stdout
    assert "no semantic redefinition" in result.stdout


def test_valid_payloads_are_present() -> None:
    data = load_examples()
    valid_ids = {item["id"] for item in data["valid_consumer_payloads"]}

    assert "calculator_pricing_context_reference" in valid_ids
    assert "telegram_channel_hint_reference" in valid_ids
    assert "operational_registry_foreign_reference" in valid_ids


def test_invalid_payloads_are_present() -> None:
    data = load_examples()
    invalid_ids = {item["id"] for item in data["invalid_consumer_payloads"]}

    assert "invalid_unknown_library_reference_id" in invalid_ids
    assert "invalid_consumer_redefines_library_semantics" in invalid_ids
    assert "invalid_consumer_runtime_ownership" in invalid_ids


def test_valid_payloads_use_known_reference_contract_ids() -> None:
    data = load_examples()

    reference_ids = {
        item["library_owned_reference"]["reference_id"]
        for item in data["valid_consumer_payloads"]
    }

    assert "product_service.business_card.standard" in reference_ids
    assert "template.business_card.90x50" in reference_ids
    assert "material.paper.mondi_color_copy_300gsm" in reference_ids


def test_invalid_payloads_document_expected_errors() -> None:
    data = load_examples()

    for payload in data["invalid_consumer_payloads"]:
        assert payload["expected_error_contains"]