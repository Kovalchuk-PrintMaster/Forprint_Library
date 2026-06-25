from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def test_semantic_reference_preview_contains_required_reference_types() -> None:
    data = yaml.safe_load(
        (ROOT / "examples" / "semantic_reference_preview.yaml").read_text(
            encoding="utf-8"
        )
    )

    reference_types = {
        item["reference_type"] for item in data["canonical_references"]
    }

    assert {
        "product_service",
        "material",
        "operation",
        "template",
    }.issubset(reference_types)


def test_semantic_reference_preview_keeps_library_boundaries() -> None:
    data = yaml.safe_load(
        (ROOT / "examples" / "semantic_reference_preview.yaml").read_text(
            encoding="utf-8"
        )
    )

    forbidden_values = {
        value
        for item in data["canonical_references"]
        for value in item["forbidden_usage"]
    }

    for expected in [
        "pricing_formula",
        "warehouse_stock_truth",
        "operational_order_state",
    ]:
        assert expected in forbidden_values


def test_semantic_reference_docs_exist_and_define_handoff_boundaries() -> None:
    readiness = (
        ROOT / "docs" / "architecture" / "semantic_reference_readiness.md"
    ).read_text(encoding="utf-8").casefold()

    handoff = (
        ROOT / "docs" / "architecture" / "downstream_reference_contract_notes.md"
    ).read_text(encoding="utf-8").casefold()

    assert "not to build the full production catalog database" in readiness
    assert "calculator engine may reference canonical ids" in readiness
    assert "operational registry may store library ids as operational projections" in handoff
    assert "no downstream module should silently invent" in handoff


def test_semantic_reference_readiness_validator_passes_all_checks() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/validate_semantic_reference_readiness.py",
            "--check",
            "all",
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )

    assert completed.returncode == 0, completed.stdout
    assert "OK: semantic reference readiness check 'all' passed." in completed.stdout