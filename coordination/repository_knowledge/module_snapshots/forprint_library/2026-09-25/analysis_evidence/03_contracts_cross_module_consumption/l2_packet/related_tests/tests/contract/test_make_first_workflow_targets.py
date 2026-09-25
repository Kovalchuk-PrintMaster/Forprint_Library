from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_TARGETS = [
    "blueprint-instruction-list",
    "blueprint-instruction-check",
    "blueprint-instruction-sync",
    "blueprint-instruction",
    "blueprint-standards-list",
    "blueprint-standards-check",
    "blueprint-standards-sync",
    "blueprint-standards",
    "blueprint-prompts-list",
    "blueprint-prompts-check",
    "blueprint-prompts-sync",
    "blueprint-prompts",
    "prompt-read",
    "blueprint-sync",
    "module-start",
    "module-sync",
    "module-validate",
    "module-finish",
    "report-clean",
    "completion-packet-validate",
    "completion-packet-apply",
    "completion-packet-check",
]


def test_makefile_contains_make_first_targets() -> None:
    text = (ROOT / "Makefile").read_text(encoding="utf-8")

    for target in REQUIRED_TARGETS:
        assert f"{target}:" in text


def test_makefile_exposes_make_first_targets_as_phony() -> None:
    text = (ROOT / "Makefile").read_text(encoding="utf-8")

    phony_sections = [
        line
        for line in text.splitlines()
        if line.startswith(".PHONY:") or line.startswith("\t")
    ]
    phony_text = "\n".join(phony_sections)

    for target in REQUIRED_TARGETS:
        assert target in phony_text


def test_make_first_workflow_helper_exists() -> None:
    path = ROOT / "scripts" / "make_first_workflow.py"

    assert path.exists()
    assert "completion packet automation is not configured" in path.read_text(
        encoding="utf-8"
    )