from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml
from forprint_library.dictionaries.models import (
    RESOLUTION_ALIAS,
    RESOLUTION_AMBIGUOUS,
    RESOLUTION_DEPRECATED,
    RESOLUTION_EXACT,
    RESOLUTION_UNRESOLVED,
)
from forprint_library.dictionaries.resolver import (
    find_ambiguous_aliases,
    resolve_dictionary_value,
)

ROOT = Path(__file__).resolve().parents[2]


def test_dictionary_resolution_exact_match_works() -> None:
    result = resolve_dictionary_value("source_system", "calculator_engine")

    assert result.status == RESOLUTION_EXACT
    assert result.matched_id == "calculator_engine"
    assert result.matched_by == "id"


def test_dictionary_resolution_alias_match_works() -> None:
    result = resolve_dictionary_value("source_system", "calculator")

    assert result.status == RESOLUTION_ALIAS
    assert result.matched_id == "calculator_engine"
    assert result.matched_by == "alias"


def test_unknown_value_returns_unresolved() -> None:
    result = resolve_dictionary_value("source_system", "not_existing_source")

    assert result.status == RESOLUTION_UNRESOLVED
    assert result.matched_id is None
    assert result.candidates == []


def test_deprecated_value_returns_deprecated_reference() -> None:
    result = resolve_dictionary_value(
        "reference_resolution_status",
        "deprecated_reference",
    )

    assert result.status == RESOLUTION_DEPRECATED
    assert result.matched_id == "deprecated_reference"


def test_ambiguous_alias_returns_manual_review() -> None:
    dictionary = {
        "dictionary_group": "demo_group",
        "entries": [
            {
                "id": "first_demo_value",
                "status": "active",
                "aliases": ["shared_alias"],
            },
            {
                "id": "second_demo_value",
                "status": "active",
                "aliases": ["shared_alias"],
            },
        ],
    }

    result = resolve_dictionary_value(
        "demo_group",
        "shared_alias",
        dictionary=dictionary,
    )

    assert result.status == RESOLUTION_AMBIGUOUS
    assert result.matched_id is None
    assert result.candidates == [
        "first_demo_value",
        "second_demo_value",
    ]


def test_ambiguous_aliases_can_be_reported() -> None:
    dictionary = {
        "dictionary_group": "demo_group",
        "entries": [
            {
                "id": "first_demo_value",
                "status": "active",
                "aliases": ["shared_alias"],
            },
            {
                "id": "second_demo_value",
                "status": "active",
                "aliases": ["shared_alias"],
            },
        ],
    }

    ambiguous = find_ambiguous_aliases(dictionary)

    assert ambiguous == {"shared_alias": ["first_demo_value", "second_demo_value"]}


def test_dictionary_resolution_examples_exist() -> None:
    path = ROOT / "examples" / "dictionaries" / "demo_dictionary_resolution_cases.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))

    example_ids = {item["id"] for item in data["examples"]}

    for expected_id in [
        "exact_id_resolution",
        "alias_resolution",
        "unknown_value",
        "deprecated_value",
        "ambiguous_alias",
        "display_label_usage",
    ]:
        assert expected_id in example_ids


def test_demo_shared_operational_dictionary_exists() -> None:
    path = ROOT / "examples" / "dictionaries" / "demo_shared_operational_dictionary.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))

    assert data["metadata"]["owner_module"] == "forprint_library"
    assert "demo_groups" in data


def test_dictionary_preview_renders_key_sections() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/preview_shared_operational_dictionaries.py",
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )

    output = completed.stdout.casefold()

    assert completed.returncode == 0
    for phrase in [
        "dictionary groups",
        "source systems",
        "entity types",
        "order / workflow statuses",
        "payment / material statuses",
        "alert statuses",
        "units",
        "resolution examples",
    ]:
        assert phrase in output