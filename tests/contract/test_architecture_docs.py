from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_DOCS = [
    "docs/architecture/library_boundaries.md",
    "docs/architecture/catalog_seed_policy.md",
    "docs/architecture/canonical_id_policy.md",
    "docs/architecture/alias_policy.md",
    "docs/architecture/dependent_module_usage.md",
]


def read_lower(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8").casefold()


def test_required_architecture_docs_exist() -> None:
    for relative_path in REQUIRED_DOCS:
        assert (ROOT / relative_path).exists(), relative_path


def test_canonical_id_policy_explains_stable_ids() -> None:
    text = read_lower("docs/architecture/canonical_id_policy.md")

    assert "canonical ids are stable internal truth" in text
    assert "dependent modules must reference canonical ids" in text
    assert "not a final production contract" in text


def test_alias_policy_explains_conflict_handling() -> None:
    text = read_lower("docs/architecture/alias_policy.md")

    assert "aliases are lookup helpers" in text
    assert "not canonical truth" in text
    assert "must not silently resolve" in text
    assert "unresolved" in text


def test_dependent_module_usage_documents_consumers() -> None:
    text = read_lower("docs/architecture/dependent_module_usage.md")

    for phrase in [
        "calculator engine",
        "telegram bot",
        "operational registry",
        "accounting registry",
        "prepress hub",
    ]:
        assert phrase in text


def test_catalog_seed_policy_documents_required_status_terms() -> None:
    text = read_lower("docs/architecture/catalog_seed_policy.md")

    for phrase in [
        "draft_canonical_seed",
        "unstable_v0_1",
        "allowed_for_projection_use",
        "not_final_contract",
        "forprint_library",
    ]:
        assert phrase in text


def test_library_boundaries_exclude_operational_ownership() -> None:
    text = read_lower("docs/architecture/library_boundaries.md")

    for phrase in [
        "clients",
        "orders",
        "payments",
        "warehouse stock truth",
        "production runtime",
        "1c synchronization",
        "crm workflow",
        "telegram runtime",
        "calculator logic",
    ]:
        assert phrase in text