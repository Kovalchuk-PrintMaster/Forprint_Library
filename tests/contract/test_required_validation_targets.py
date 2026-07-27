from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAKEFILE = ROOT / "Makefile"


def test_format_check_target_exists_and_is_changed_file_scoped() -> None:
    text = MAKEFILE.read_text(encoding="utf-8")

    assert ".PHONY: format-check" in text
    assert "format-check:" in text
    assert "ruff format --check $$changed_files" in text
    assert "git diff --name-only --diff-filter=ACMRTUXB origin/main...HEAD" in text
    assert "git ls-files --others --exclude-standard -- app scripts tests" in text
    assert "ruff format --check app scripts tests" not in text


def test_check_report_full_target_exists_as_blueprint_compatibility_alias() -> None:
    text = MAKEFILE.read_text(encoding="utf-8")

    assert ".PHONY: check-report-full" in text
    assert "check-report-full: check-report" in text


def test_help_lists_required_validation_targets() -> None:
    text = MAKEFILE.read_text(encoding="utf-8")

    assert 'make format-check' in text
    assert 'make check-report-full' in text
