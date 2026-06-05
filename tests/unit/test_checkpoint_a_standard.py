from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def test_standard_coordination_files_exist() -> None:
    required = [
        "coordination/blueprint_source.yaml",
        "coordination/README.md",
        "coordination/status/current_status.yaml",
        "coordination/status/current_status.md",
        "coordination/status/next_questions_for_blueprint.md",
        "coordination/prompts/index.yaml",
        "coordination/reports/index.yaml",
    ]

    for relative_path in required:
        assert (ROOT / relative_path).exists(), relative_path


def test_blueprint_source_yaml_is_valid() -> None:
    path = ROOT / "coordination/blueprint_source.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))

    assert data["blueprint_source"]["module_id"] == "forprint_library"
    assert "forprint_system_blueprint" in data["blueprint_source"]["blueprint_root"]
    assert data["blueprint_source"]["module_directives_index_status"] in {
        "pending_blueprint_directive_index",
        "active",
    }


def test_makefile_exposes_required_standard_targets() -> None:
    text = (ROOT / "Makefile").read_text(encoding="utf-8")
    required_targets = [
        "install",
        "lint",
        "lint-fix",
        "test",
        "check",
        "check-report",
        "blueprint-pull",
        "blueprint-check",
        "blueprint-sync-directives",
        "coordination-check",
        "coordination-fix",
        "module-policy-check",
    ]

    for target in required_targets:
        assert f"{target}:" in text


def test_module_manifest_boundary_exclusions() -> None:
    data = yaml.safe_load((ROOT / "forprint_module_manifest.yaml").read_text(encoding="utf-8"))
    does_not_own = set(data["boundaries"]["does_not_own"])

    required_exclusions = {
        "client registry",
        "order registry",
        "payment registry",
        "warehouse stock truth",
        "production runtime",
        "1C synchronization",
        "CRM workflow",
        "Telegram runtime",
        "Calculator business logic",
    }

    assert required_exclusions.issubset(does_not_own)


def test_check_report_script_exists() -> None:
    path = ROOT / "scripts/run_library_checks.py"
    assert path.exists()
    assert "ForPrint Library" in path.read_text(encoding="utf-8")