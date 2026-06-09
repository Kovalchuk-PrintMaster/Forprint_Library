from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_check_report_includes_shared_dictionary_checks() -> None:
    text = (ROOT / "scripts/run_library_checks.py").read_text(encoding="utf-8")

    for phrase in [
        "Shared dictionary files",
        "Dictionary schemas",
        "Dictionary group files",
        "Dictionary required values",
        "Dictionary resolver/examples",
        "Dictionary preview",
    ]:
        assert phrase in text


def test_makefile_exposes_dictionary_targets() -> None:
    text = (ROOT / "Makefile").read_text(encoding="utf-8")

    for target in [
        "dictionary-preview:",
        "status-report:",
    ]:
        assert target in text