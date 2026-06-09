from __future__ import annotations

from forprint_library.dictionaries.loader import list_dictionary_groups, load_dictionary
from forprint_library.dictionaries.resolver import resolve_dictionary_value


def print_section(title: str) -> None:
    print()
    print(title)
    print("=" * len(title))


def print_entries(group_name: str, limit: int = 8) -> None:
    dictionary = load_dictionary(group_name)
    entries = dictionary["entries"]

    print(f"{group_name} ({len(entries)} values)")
    print("-" * 72)
    print(f"{'ID':<34} {'STATUS':<12} LABEL")
    print("-" * 72)

    for entry in entries[:limit]:
        print(f"{entry['id']:<34} {entry['status']:<12} {entry['label_en']}")

    if len(entries) > limit:
        print(f"... {len(entries) - limit} more")


def print_resolution_example(group_name: str, value: str) -> None:
    result = resolve_dictionary_value(group_name, value)
    print(
        f"{group_name:<32} input={value:<28} "
        f"status={result.status:<34} matched={result.matched_id}"
    )


def main() -> int:
    print("ForPrint Library — Shared Operational Dictionary v0.1 Preview")

    print_section("DICTIONARY GROUPS")
    groups = list_dictionary_groups()
    for group_name in groups:
        print(f"- {group_name}")

    print_section("SOURCE SYSTEMS")
    print_entries("source_system")

    print_section("ENTITY TYPES")
    print_entries("entity_type")

    print_section("ORDER / WORKFLOW STATUSES")
    for group_name in [
        "order_status",
        "order_line_status",
        "workflow_status",
        "workflow_stage_status",
        "production_status",
    ]:
        print_entries(group_name, limit=6)
        print()

    print_section("PAYMENT / MATERIAL STATUSES")
    for group_name in [
        "payment_status",
        "material_requirement_status",
        "reference_resolution_status",
        "product_service_reference_status",
    ]:
        print_entries(group_name, limit=6)
        print()

    print_section("ALERT STATUSES")
    for group_name in [
        "alert_rule_type",
        "alert_severity",
        "alert_event_status",
        "notification_status",
    ]:
        print_entries(group_name, limit=6)
        print()

    print_section("UNITS")
    print_entries("unit", limit=12)

    print_section("RESOLUTION EXAMPLES")
    for group_name, value in [
        ("source_system", "calculator_engine"),
        ("source_system", "calculator"),
        ("source_system", "not_existing_source"),
        ("reference_resolution_status", "deprecated_reference"),
        ("unit", "шт"),
        ("alert_severity", "crit"),
    ]:
        print_resolution_example(group_name, value)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())