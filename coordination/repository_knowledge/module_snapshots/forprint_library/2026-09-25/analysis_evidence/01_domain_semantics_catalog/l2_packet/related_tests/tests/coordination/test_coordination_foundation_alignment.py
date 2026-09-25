from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]

DOC_PATH = ROOT / "docs" / "architecture" / "coordination_foundation_alignment.md"
ALIGNMENT_PATH = (
    ROOT
    / "coordination"
    / "blueprint_awareness"
    / "library_coordination_foundation_alignment_v0_1.yaml"
)
VALIDATOR = (
    ROOT / "scripts" / "coordination" / "validate_coordination_foundation_alignment.py"
)


def load_alignment() -> dict:
    data = yaml.safe_load(ALIGNMENT_PATH.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def test_coordination_foundation_alignment_files_exist() -> None:
    for path in [DOC_PATH, ALIGNMENT_PATH, VALIDATOR]:
        assert path.exists(), path


def test_coordination_foundation_alignment_records_prompt_and_manual_mode() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "library_coordination_foundation_alignment_v0_1" in text
    assert "Manual Blueprint communication mode" in text
    assert "The Library Makefile is not rewritten" in text


def test_coordination_foundation_alignment_yaml_confirms_operator_targets() -> None:
    data = load_alignment()

    targets = set(data["operator_workflow"]["confirmed_targets"])

    for target in [
        "prompt-read-next",
        "document-awareness",
        "context-bundle",
        "module-validate",
        "prompt-queue-validate",
        "document-manifest",
    ]:
        assert target in targets

    assert data["operator_workflow"]["makefile_rewrite"] is False
    assert data["operator_workflow"]["destructive_makefile_rewrite"] is False


def test_coordination_foundation_alignment_keeps_non_goals_false() -> None:
    data = load_alignment()

    non_goals = data["non_goals"]

    for key in [
        "workbench_started",
        "configurable_product_workbench_started",
        "business_card_product_skeleton_started",
        "product_modeling_started",
        "one_c_import_started",
        "calculator_integration_started",
        "production_catalog_database_started",
        "live_api_started",
        "production_runtime_changes",
        "production_writes_added",
        "runtime_integrations_added",
    ]:
        assert non_goals[key] is False


def test_coordination_foundation_alignment_documents_config_and_secrets_policy() -> None:
    data = load_alignment()

    assert data["configuration_alignment"]["config_directory_required_now"] is False
    assert data["configuration_alignment"]["env_example_required_now"] is False
    assert data["configuration_alignment"]["production_runtime_config_added"] is False

    assert data["secrets_alignment"]["secrets_required_now"] is False
    assert data["secrets_alignment"]["secrets_check"] == "not_applicable"
    assert data["secrets_alignment"]["real_secrets_committed"] is False


def test_coordination_foundation_alignment_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "OK: Library coordination foundation alignment validates" in result.stdout