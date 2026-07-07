from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]

DOC_PATH = ROOT / "docs" / "architecture" / "coordination_foundation_alignment.md"
ALIGNMENT_PATH = (
    ROOT
    / "coordination"
    / "blueprint_awareness"
    / "library_coordination_foundation_alignment_v0_1.yaml"
)

REQUIRED_COORDINATION_PATHS = [
    ROOT / "coordination" / "blueprint_source.yaml",
    ROOT / "coordination" / "prompts" / "index.yaml",
    ROOT / "coordination" / "reports" / "index.yaml",
    ROOT / "coordination" / "reports" / "completion",
    ROOT / "coordination" / "status" / "current_status.yaml",
    ROOT / "coordination" / "status" / "current_status.md",
    ROOT / "coordination" / "status" / "next_questions_for_blueprint.md",
    ROOT / "coordination" / "blueprint_awareness" / "document_review_ledger.yaml",
]

REQUIRED_TARGETS = {
    "blueprint-pull",
    "prompt-read-next",
    "document-awareness",
    "context-bundle",
    "module-validate",
    "prompt-queue-validate",
    "document-manifest",
    "check",
    "check-report",
    "governance-check",
}

NON_GOAL_FLAGS = {
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
}


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise AssertionError(f"Missing file: {path.relative_to(ROOT)}")

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}

    if not isinstance(data, dict):
        raise AssertionError(f"YAML root must be a mapping: {path.relative_to(ROOT)}")

    return data


def validate_required_files() -> None:
    for path in [DOC_PATH, ALIGNMENT_PATH, *REQUIRED_COORDINATION_PATHS]:
        if not path.exists():
            raise AssertionError(f"Missing path: {path.relative_to(ROOT)}")


def validate_doc() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")

    required_phrases = [
        "Library Coordination Foundation Alignment v0.1",
        "library_coordination_foundation_alignment_v0_1",
        "Manual Blueprint communication mode",
        "No destructive Makefile rewrite is required",
        "controlled coordination backlog",
        "Secrets checks are considered not applicable",
        "Configurable Product Workbench",
        "business_card product skeleton",
        "Library Configurable Product Workbench v0.1",
    ]

    for phrase in required_phrases:
        if phrase not in text:
            raise AssertionError(f"Document is missing phrase: {phrase}")


def validate_alignment_yaml(data: dict[str, Any]) -> None:
    if data.get("schema_version") != "library_coordination_foundation_alignment_v0_1":
        raise AssertionError("Unexpected schema_version")

    if data.get("module_id") != "forprint_library":
        raise AssertionError("Unexpected module_id")

    if data.get("prompt_id") != "library_coordination_foundation_alignment_v0_1":
        raise AssertionError("Unexpected prompt_id")

    operator_workflow = data.get("operator_workflow", {})
    if not isinstance(operator_workflow, dict):
        raise AssertionError("operator_workflow must be a mapping")

    confirmed_targets = set(operator_workflow.get("confirmed_targets", []))
    missing_targets = sorted(REQUIRED_TARGETS - confirmed_targets)
    if missing_targets:
        raise AssertionError(f"Missing confirmed targets: {missing_targets}")

    if operator_workflow.get("makefile_rewrite") is not False:
        raise AssertionError("makefile_rewrite must be false")

    if operator_workflow.get("destructive_makefile_rewrite") is not False:
        raise AssertionError("destructive_makefile_rewrite must be false")

    coordination_structure = data.get("coordination_structure", {})
    if not isinstance(coordination_structure, dict):
        raise AssertionError("coordination_structure must be a mapping")

    if coordination_structure.get("backlog_is_blocker") is not False:
        raise AssertionError("coordination backlog must not be a blocker")

    configuration = data.get("configuration_alignment", {})
    if not isinstance(configuration, dict):
        raise AssertionError("configuration_alignment must be a mapping")

    if configuration.get("config_directory_required_now") is not False:
        raise AssertionError("config directory must be deferred for this checkpoint")

    if configuration.get("production_runtime_config_added") is not False:
        raise AssertionError("production runtime config must not be added")

    secrets = data.get("secrets_alignment", {})
    if not isinstance(secrets, dict):
        raise AssertionError("secrets_alignment must be a mapping")

    if secrets.get("secrets_required_now") is not False:
        raise AssertionError("secrets must not be required now")

    if secrets.get("real_secrets_committed") is not False:
        raise AssertionError("real secrets must not be committed")

    tree = data.get("project_tree_alignment", {})
    if not isinstance(tree, dict):
        raise AssertionError("project_tree_alignment must be a mapping")

    for key in [
        "large_refactor",
        "application_code_moved",
        "deep_nesting_added",
        "workbench_directories_created",
        "production_runtime_directories_created",
    ]:
        if tree.get(key) is not False:
            raise AssertionError(f"{key} must be false")

    non_goals = data.get("non_goals", {})
    if not isinstance(non_goals, dict):
        raise AssertionError("non_goals must be a mapping")

    for key in NON_GOAL_FLAGS:
        if non_goals.get(key) is not False:
            raise AssertionError(f"non-goal flag must be false: {key}")

    readiness = data.get("readiness", {})
    if not isinstance(readiness, dict):
        raise AssertionError("readiness must be a mapping")

    if readiness.get("coordination_ready_for_next_prompt") is not True:
        raise AssertionError("coordination readiness must be true")

    if readiness.get("product_ready") is not False:
        raise AssertionError("product readiness must remain false")


def main() -> int:
    validate_required_files()
    validate_doc()
    validate_alignment_yaml(load_yaml(ALIGNMENT_PATH))

    print("OK: Library coordination foundation alignment validates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())