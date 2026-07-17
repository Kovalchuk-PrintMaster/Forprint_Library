from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MAKEFILE = ROOT / "Makefile"


def test_blueprint_prompt_consumer_uses_path_only_resolver_mode() -> None:
    text = MAKEFILE.read_text(encoding="utf-8")

    assert "--path-only" in text
    assert "resolve_next_prompt.py" in text
    assert "/^Path: /" not in text
    assert "awk -F': '" not in text


def test_blueprint_prompt_check_and_sync_targets_are_present() -> None:
    text = MAKEFILE.read_text(encoding="utf-8")

    assert ".PHONY: blueprint-instruction-check" in text
    assert "blueprint-instruction-check:" in text
    assert ".PHONY: blueprint-instruction-sync" in text
    assert "blueprint-instruction-sync: blueprint-instruction-check" in text
    assert ".PHONY: blueprint-prompts-check" in text
    assert "blueprint-prompts-check: blueprint-instruction-check" in text


def test_blueprint_prompt_consumer_keeps_manual_override_fallback() -> None:
    text = MAKEFILE.read_text(encoding="utf-8")

    assert "ACTIVE_BLUEPRINT_PROMPT ?=" in text
    assert "manual active prompt override" in text
    assert "Prompt Queue next prompt is readable" in text
    assert "synced Prompt Queue next prompt" in text
