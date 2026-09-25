from __future__ import annotations


def normalize_semantic_alias(value: str) -> str:
    return " ".join(value.casefold().strip().split())