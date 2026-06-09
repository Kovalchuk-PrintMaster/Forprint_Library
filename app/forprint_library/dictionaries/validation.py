from __future__ import annotations

from collections import defaultdict
from typing import Any

from forprint_library.dictionaries.models import (
    ALLOWED_ENTRY_STATUSES,
    DICTIONARY_GROUPS,
    EXPECTED_SHARED_METADATA,
    REQUIRED_DICTIONARY_ENTRY_FIELDS,
    REQUIRED_SHARED_METADATA_FIELDS,
    DictionaryValidationError,
)


def normalize_dictionary_lookup_value(value: str) -> str:
    return " ".join(value.casefold().strip().split())


def collect_shared_dictionary_entries(shared_dictionary: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []

    groups = shared_dictionary.get("dictionary_groups")
    if not isinstance(groups, dict):
        raise DictionaryValidationError("Shared dictionary must contain dictionary_groups mapping.")

    for group_name in DICTIONARY_GROUPS:
        group_entries = groups.get(group_name)
        if not isinstance(group_entries, list):
            raise DictionaryValidationError(f"Dictionary group must be a list: {group_name}")

        for entry in group_entries:
            if not isinstance(entry, dict):
                raise DictionaryValidationError(
                    f"Dictionary entry must be a mapping in group: {group_name}"
                )

            entries.append(dict(entry))

    return entries


def validate_shared_metadata(shared_dictionary: dict[str, Any]) -> None:
    metadata = shared_dictionary.get("metadata")
    if not isinstance(metadata, dict):
        raise DictionaryValidationError("Shared dictionary must contain metadata mapping.")

    missing = [field for field in REQUIRED_SHARED_METADATA_FIELDS if field not in metadata]
    if missing:
        raise DictionaryValidationError(f"Shared dictionary metadata missing fields: {missing}")

    mismatched = {
        key: {"expected": expected, "actual": metadata.get(key)}
        for key, expected in EXPECTED_SHARED_METADATA.items()
        if metadata.get(key) != expected
    }
    if mismatched:
        raise DictionaryValidationError(
            f"Shared dictionary metadata has unexpected values: {mismatched}"
        )


def validate_dictionary_entry(entry: dict[str, Any], expected_group: str | None = None) -> None:
    missing = [field for field in REQUIRED_DICTIONARY_ENTRY_FIELDS if field not in entry]
    if missing:
        entry_id = entry.get("id", "<missing-id>")
        raise DictionaryValidationError(f"Dictionary entry {entry_id} missing fields: {missing}")

    entry_id = entry["id"]

    if not isinstance(entry_id, str) or not entry_id.strip():
        raise DictionaryValidationError("Dictionary entry id must be a non-empty string.")

    if entry["status"] not in ALLOWED_ENTRY_STATUSES:
        raise DictionaryValidationError(
            f"Dictionary entry {entry_id} has unsupported status: {entry['status']}"
        )

    if not isinstance(entry["aliases"], list):
        raise DictionaryValidationError(f"Dictionary entry {entry_id} aliases must be a list.")

    for alias in entry["aliases"]:
        if not isinstance(alias, str) or not alias.strip():
            raise DictionaryValidationError(
                f"Dictionary entry {entry_id} contains invalid alias: {alias!r}"
            )

    if entry["owner_module"] != "forprint_library":
        raise DictionaryValidationError(
            f"Dictionary entry {entry_id} must be owned by forprint_library."
        )

    if entry["version"] != "0.1":
        raise DictionaryValidationError(f"Dictionary entry {entry_id} must use version 0.1.")

    if expected_group is not None and entry["dictionary_group"] != expected_group:
        raise DictionaryValidationError(
            f"Dictionary entry {entry_id} group mismatch: "
            f"expected {expected_group}, got {entry['dictionary_group']}"
        )


def validate_dictionary_group(group_name: str, dictionary: dict[str, Any]) -> None:
    if dictionary.get("dictionary_group") != group_name:
        raise DictionaryValidationError(
            f"Dictionary group mismatch: expected {group_name}, "
            f"got {dictionary.get('dictionary_group')}"
        )

    metadata = dictionary.get("metadata")
    if not isinstance(metadata, dict):
        raise DictionaryValidationError(f"Dictionary {group_name} must contain metadata.")

    entries = dictionary.get("entries")
    if not isinstance(entries, list):
        raise DictionaryValidationError(f"Dictionary {group_name} entries must be a list.")

    seen_ids: set[str] = set()
    for entry in entries:
        validate_dictionary_entry(entry, expected_group=group_name)

        entry_id = entry["id"]
        if entry_id in seen_ids:
            raise DictionaryValidationError(
                f"Duplicate dictionary entry id in {group_name}: {entry_id}"
            )
        seen_ids.add(entry_id)


def find_duplicate_aliases(entries: list[dict[str, Any]]) -> dict[str, list[str]]:
    alias_map: dict[str, list[str]] = defaultdict(list)

    for entry in entries:
        entry_id = entry["id"]
        group_name = entry["dictionary_group"]
        for alias in entry["aliases"]:
            alias_map[f"{group_name}:{normalize_dictionary_lookup_value(alias)}"].append(
                entry_id
            )

    return {
        alias_key: sorted(set(entry_ids))
        for alias_key, entry_ids in alias_map.items()
        if len(set(entry_ids)) > 1
    }


def validate_no_duplicate_ids_within_groups(entries: list[dict[str, Any]]) -> None:
    ids_by_group: dict[str, set[str]] = defaultdict(set)

    for entry in entries:
        group_name = entry["dictionary_group"]
        entry_id = entry["id"]

        if entry_id in ids_by_group[group_name]:
            raise DictionaryValidationError(
                f"Duplicate dictionary entry id in {group_name}: {entry_id}"
            )

        ids_by_group[group_name].add(entry_id)


def validate_shared_dictionary(shared_dictionary: dict[str, Any]) -> None:
    validate_shared_metadata(shared_dictionary)
    entries = collect_shared_dictionary_entries(shared_dictionary)

    for entry in entries:
        validate_dictionary_entry(entry, expected_group=entry["dictionary_group"])

    validate_no_duplicate_ids_within_groups(entries)

    duplicates = find_duplicate_aliases(entries)
    if duplicates:
        raise DictionaryValidationError(f"Duplicate dictionary aliases detected: {duplicates}")