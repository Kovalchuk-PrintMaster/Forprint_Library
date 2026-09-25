from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]

DOC_PATH = ROOT / "docs" / "architecture" / "reference_contract_foundation.md"
EXAMPLES_PATH = (
    ROOT / "examples" / "reference_contract" / "library_reference_examples.yaml"
)
SCHEMA_PATH = ROOT / "schemas" / "reference_contract" / "library_reference.schema.yaml"
VALIDATOR = (
    ROOT / "scripts" / "reference_contract" / "validate_library_reference_contract.py"
)

EXPECTED_REFERENCE_TYPES = {
    "product_service",
    "material",
    "operation",
    "unit",
    "template",
    "technical_card",
}

EXPECTED_STATUSES = {
    "library_reference_confirmed",
    "library_reference_pending",
    "ambiguous_manual_review_required",
    "deprecated_reference",
    "unknown",
}


def load_examples() -> dict:
    data = yaml.safe_load(EXAMPLES_PATH.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def test_library_reference_contract_files_exist() -> None:
    for path in [DOC_PATH, EXAMPLES_PATH, SCHEMA_PATH, VALIDATOR]:
        assert path.exists(), path


def test_library_reference_contract_examples_cover_required_types() -> None:
    data = load_examples()

    examples = data["examples"]

    seen_types = {
        example["downstream_payload"]["library_reference"]["reference_type"]
        for example in examples
    }

    assert EXPECTED_REFERENCE_TYPES.issubset(seen_types)


def test_library_reference_contract_examples_cover_required_statuses() -> None:
    data = load_examples()

    examples = data["examples"]

    seen_statuses = {
        example["downstream_payload"]["library_reference"]["resolution_status"]
        for example in examples
    }

    assert EXPECTED_STATUSES.issubset(seen_statuses)


def test_library_reference_contract_examples_have_required_fields() -> None:
    data = load_examples()

    required_fields = {
        "schema_version",
        "reference_type",
        "reference_id",
        "display_label",
        "resolution_status",
        "source_module",
        "alias_input",
        "deprecation",
        "manual_review",
    }

    for example in data["examples"]:
        reference = example["downstream_payload"]["library_reference"]

        assert required_fields.issubset(reference)
        assert reference["schema_version"] == "library_reference_v0_2"


def test_library_reference_contract_schema_defines_version_type_and_status() -> None:
    schema = yaml.safe_load(SCHEMA_PATH.read_text(encoding="utf-8"))

    assert schema["$id"] == "forprint_library.reference_contract.library_reference_v0_2"
    assert "schema_version" in schema["required"]
    assert "reference_type" in schema["required"]
    assert "resolution_status" in schema["required"]

    assert set(schema["properties"]["reference_type"]["enum"]) == EXPECTED_REFERENCE_TYPES
    assert set(schema["properties"]["resolution_status"]["enum"]) == EXPECTED_STATUSES


def test_library_reference_contract_docs_keep_boundaries_clear() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "Downstream modules must not become owners" in text
    assert "Library must not own" in text
    assert "production catalog database" in text
    assert "live API" in text
    assert "Calculator pricing logic" in text


def test_library_reference_contract_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "OK: Library reference contract foundation validates" in result.stdout