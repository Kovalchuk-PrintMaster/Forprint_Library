
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]

EXAMPLE_PATH = ROOT / "examples" / "semantic_reference_preview.yaml"

READINESS_DOC = (
    ROOT / "docs" / "architecture" / "semantic_reference_readiness.md"
)

HANDOFF_DOC = (
    ROOT / "docs" / "architecture" / "downstream_reference_contract_notes.md"
)

MAKEFILE = ROOT / "Makefile"
ACTIVE_PROMPT_DIR = ROOT / "coordination" / "prompts" / "active"

STANDARDS_SNAPSHOT = (
    ROOT
    / "coordination"
    / "standards"
    / "blueprint_standards_available_snapshot.txt"
)

REQUIRED_REFERENCE_TYPES = {
    "product_service",
    "material",
    "operation",
    "template",
}

REQUIRED_MAKE_TARGETS = {
    "blueprint-sync",
    "module-start",
    "module-sync",
    "module-validate",
    "module-finish",
    "prompt-read",
    "report-clean",
    "completion-packet-check",
}


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise AssertionError(f"Missing file: {path.relative_to(ROOT)}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise AssertionError(f"YAML root must be a mapping: {path.relative_to(ROOT)}")
    return data


def read_text(path: Path) -> str:
    if not path.exists():
        raise AssertionError(f"Missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8").casefold()


def check_semantic_reference_readiness() -> None:
    data = load_yaml(EXAMPLE_PATH)

    metadata = data.get("metadata", {})
    assert metadata.get("owner_module") == "forprint_library"
    assert metadata.get("status") == "draft_semantic_reference_readiness_v0_1"
    assert metadata.get("production_catalog_status") == "not_production_catalog_database"

    references = data.get("canonical_references", [])
    assert isinstance(references, list)
    assert references

    reference_types = {item.get("reference_type") for item in references}
    missing_types = REQUIRED_REFERENCE_TYPES - reference_types
    assert not missing_types, f"Missing reference types: {sorted(missing_types)}"

    for item in references:
        assert item["id"]
        assert item["label_uk"]
        assert item["label_en"]
        assert item["reference_type"] in REQUIRED_REFERENCE_TYPES
        assert isinstance(item.get("aliases"), list)
        assert item["readiness_status"] == "ready_for_reference_example"
        assert "calculator_engine" in item["downstream_usage"]
        assert "forprint_operational_registry" in item["downstream_usage"]
        assert isinstance(item.get("forbidden_usage"), list)
        assert item["forbidden_usage"]

    alias_examples = data.get("alias_resolution_examples", [])
    assert alias_examples
    assert any(
        item.get("expected_resolution_status") == "confirmed_with_alias"
        for item in alias_examples
    )
    assert any(
        item.get("expected_resolution_status") == "unresolved_manual_review_required"
        for item in alias_examples
    )

    ambiguous_examples = data.get("ambiguous_naming_examples", [])
    assert ambiguous_examples
    assert (
        ambiguous_examples[0]["expected_resolution_status"]
        == "ambiguous_manual_review_required"
    )


def check_docs() -> None:
    readiness = read_text(READINESS_DOC)
    handoff = read_text(HANDOFF_DOC)

    for phrase in [
        "not to build the full production catalog database",
        "product_service.business_card.standard",
        "confirmed_with_alias",
        "ambiguous_manual_review_required",
        "pricing formulas",
        "warehouse stock truth",
        "operational order state",
    ]:
        assert phrase in readiness

    for phrase in [
        "calculator engine",
        "operational registry",
        "store library ids as operational projections",
        "no downstream module should silently invent",
        "not a final production catalog contract",
    ]:
        assert phrase in handoff


def check_make_first_alignment() -> None:
    text = MAKEFILE.read_text(encoding="utf-8")

    for target in REQUIRED_MAKE_TARGETS:
        assert f"{target}:" in text

    assert ".PHONY:" in text


def check_blueprint_visibility() -> None:
    assert ACTIVE_PROMPT_DIR.exists(), "Missing synced active prompt directory"
    assert any(ACTIVE_PROMPT_DIR.glob("*.md")), "No synced active prompt files found"
    assert STANDARDS_SNAPSHOT.exists(), "Missing Blueprint standards snapshot"


CHECKS = {
    "semantic": check_semantic_reference_readiness,
    "docs": check_docs,
    "make-first": check_make_first_alignment,
    "blueprint-visibility": check_blueprint_visibility,
    "all": lambda: [
        check_make_first_alignment(),
        check_blueprint_visibility(),
        check_semantic_reference_readiness(),
        check_docs(),
    ],
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", choices=sorted(CHECKS), default="all")
    args = parser.parse_args()

    CHECKS[args.check]()
    print(f"OK: semantic reference readiness check '{args.check}' passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())