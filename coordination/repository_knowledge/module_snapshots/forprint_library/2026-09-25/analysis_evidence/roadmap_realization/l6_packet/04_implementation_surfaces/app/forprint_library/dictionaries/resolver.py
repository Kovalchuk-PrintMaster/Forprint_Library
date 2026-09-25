from __future__ import annotations

from collections import defaultdict
from typing import Any

from forprint_library.dictionaries.loader import load_dictionary
from forprint_library.dictionaries.models import (
    RESOLUTION_ALIAS,
    RESOLUTION_AMBIGUOUS,
    RESOLUTION_DEPRECATED,
    RESOLUTION_EXACT,
    RESOLUTION_UNRESOLVED,
    DictionaryResolutionResult,
)
from forprint_library.dictionaries.validation import normalize_dictionary_lookup_value


def resolve_dictionary_value(
    group_name: str,
    value_or_alias: str,
    dictionary: dict[str, Any] | None = None,
) -> DictionaryResolutionResult:
    active_dictionary = dictionary or load_dictionary(group_name)
    entries = active_dictionary.get("entries", [])

    normalized_input = normalize_dictionary_lookup_value(value_or_alias)

    for entry in entries:
        if normalize_dictionary_lookup_value(entry["id"]) == normalized_input:
            if entry["status"] == "deprecated":
                return DictionaryResolutionResult(
                    group_name=group_name,
                    input_value=value_or_alias,
                    status=RESOLUTION_DEPRECATED,
                    matched_id=entry["id"],
                    matched_by="id",
                    entry=dict(entry),
                    candidates=[entry["id"]],
                )

            return DictionaryResolutionResult(
                group_name=group_name,
                input_value=value_or_alias,
                status=RESOLUTION_EXACT,
                matched_id=entry["id"],
                matched_by="id",
                entry=dict(entry),
                candidates=[entry["id"]],
            )

    alias_matches: dict[str, dict[str, Any]] = {}
    for entry in entries:
        for alias in entry["aliases"]:
            if normalize_dictionary_lookup_value(alias) == normalized_input:
                alias_matches[entry["id"]] = entry

    if len(alias_matches) > 1:
        return DictionaryResolutionResult(
            group_name=group_name,
            input_value=value_or_alias,
            status=RESOLUTION_AMBIGUOUS,
            matched_id=None,
            matched_by="alias",
            entry=None,
            candidates=sorted(alias_matches),
        )

    if len(alias_matches) == 1:
        entry = next(iter(alias_matches.values()))
        if entry["status"] == "deprecated":
            return DictionaryResolutionResult(
                group_name=group_name,
                input_value=value_or_alias,
                status=RESOLUTION_DEPRECATED,
                matched_id=entry["id"],
                matched_by="alias",
                entry=dict(entry),
                candidates=[entry["id"]],
            )

        return DictionaryResolutionResult(
            group_name=group_name,
            input_value=value_or_alias,
            status=RESOLUTION_ALIAS,
            matched_id=entry["id"],
            matched_by="alias",
            entry=dict(entry),
            candidates=[entry["id"]],
        )

    return DictionaryResolutionResult(
        group_name=group_name,
        input_value=value_or_alias,
        status=RESOLUTION_UNRESOLVED,
        matched_id=None,
        matched_by=None,
        entry=None,
        candidates=[],
    )


def find_ambiguous_aliases(dictionary: dict[str, Any]) -> dict[str, list[str]]:
    alias_map: dict[str, list[str]] = defaultdict(list)

    for entry in dictionary.get("entries", []):
        for alias in entry["aliases"]:
            alias_map[normalize_dictionary_lookup_value(alias)].append(entry["id"])

    return {
        alias: sorted(set(entry_ids))
        for alias, entry_ids in alias_map.items()
        if len(set(entry_ids)) > 1
    }