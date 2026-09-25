from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

EXPECTED_MODULE_ID = "forprint_library"
EXPECTED_PROMPT_ID = "forprint_library_calculator_input_contract_v0_1"
EXPECTED_PHASE = "calculator_input_contract_v0_1"
EXPECTED_REPORT_PATH = (
    "coordination/reports/completion/"
    "forprint_library_calculator_input_contract_v0_1_completion.md"
)

REQUIRED_STRING_FIELDS = (
    "schema_version",
    "packet_id",
    "module_id",
    "prompt_id",
    "phase",
    "created_at",
    "report_path",
    "base_commit",
    "implementation_commit",
    "completion_commit",
)

REQUIRED_CHECKS = (
    "focused_tests",
    "completion_report_tests",
    "full_suite",
    "lint",
    "format_check",
    "governance_check",
    "module_validate",
    "check_report",
    "check_report_full",
    "git_diff_check",
)

REQUIRED_BOUNDARY_FLAGS = (
    "no_production_api",
    "no_live_external_integrations",
    "no_production_write",
    "no_automatic_posting",
    "no_calculator_final_price_ownership",
    "no_order_creation",
    "no_telegram_runtime_ui",
    "no_logistics_ownership",
    "no_crm_or_gateway_write",
    "no_accounting_or_payment_write",
    "no_stock_or_production_write",
    "no_blueprint_repository_write",
)

COMMIT_RE = re.compile(r"^[0-9a-f]{7,40}$")


class CompletionPacketValidationError(ValueError):
    """Completion packet does not match the Library/Blueprint intake contract."""


def _fail(message: str) -> None:
    raise CompletionPacketValidationError(message)


def _require_mapping(value: Any, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        _fail(f"completion packet field `{field}` must be a mapping")
    return value


def _require_string(data: dict[str, Any], field: str) -> str:
    value = data.get(field)
    if not isinstance(value, str) or not value.strip():
        _fail(f"completion packet field `{field}` must be a non-empty string")
    return value.strip()


def _require_commit(data: dict[str, Any], field: str) -> str:
    value = _require_string(data, field)
    if not COMMIT_RE.fullmatch(value):
        _fail(f"completion packet field `{field}` must be a git commit hash")
    return value


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        _fail(f"invalid YAML in completion packet: {exc}")
    except UnicodeDecodeError as exc:
        _fail(f"completion packet is not valid UTF-8: {exc}")

    if not isinstance(loaded, dict):
        _fail("completion packet root must be a mapping")
    return loaded


def _resolve_packet_path(packet_path: str | Path, root: Path) -> Path:
    raw = str(packet_path)
    if not raw.strip():
        _fail("PACKET path is required")
    path = Path(raw)
    if not path.is_absolute():
        path = root / path
    if not path.exists():
        _fail(f"completion packet file is missing: {path}")
    if not path.is_file():
        _fail(f"completion packet path is not a file: {path}")
    return path


def _validate_required_identity(data: dict[str, Any]) -> None:
    for field in REQUIRED_STRING_FIELDS:
        _require_string(data, field)

    if data["module_id"] != EXPECTED_MODULE_ID:
        _fail("completion packet field `module_id` has wrong value")
    if data["prompt_id"] != EXPECTED_PROMPT_ID:
        _fail("completion packet field `prompt_id` has wrong value")
    if data["phase"] != EXPECTED_PHASE:
        _fail("completion packet field `phase` has wrong value")
    if data["report_path"] != EXPECTED_REPORT_PATH:
        _fail("completion packet field `report_path` has wrong value")

    _require_commit(data, "base_commit")
    _require_commit(data, "implementation_commit")
    _require_commit(data, "completion_commit")


def _validate_report_path(data: dict[str, Any], root: Path) -> None:
    report_path = root / data["report_path"]
    if not report_path.exists():
        _fail(f"completion packet report_path does not exist: {data['report_path']}")
    if not report_path.is_file():
        _fail(f"completion packet report_path is not a file: {data['report_path']}")


def _validate_checks(data: dict[str, Any]) -> None:
    checks = _require_mapping(data.get("checks"), "checks")
    for check_name in REQUIRED_CHECKS:
        check = _require_mapping(checks.get(check_name), f"checks.{check_name}")
        if check.get("exit_code") != 0:
            _fail(f"completion packet check `{check_name}` must have exit_code 0")

    for check_name in ("focused_tests", "completion_report_tests", "full_suite"):
        check = checks[check_name]
        passed = check.get("passed")
        if not isinstance(passed, int) or passed <= 0:
            _fail(f"completion packet check `{check_name}` must record passed tests")

    for check_name in ("check_report", "check_report_full"):
        totals = _require_mapping(checks[check_name].get("totals"), f"{check_name}.totals")
        for field in ("total_checks", "ok", "failed", "other"):
            value = totals.get(field)
            if not isinstance(value, int) or value < 0:
                _fail(f"completion packet `{check_name}.totals.{field}` must be >= 0")
        counted = totals["ok"] + totals["failed"] + totals["other"]
        if totals["total_checks"] != counted:
            _fail(f"completion packet `{check_name}` totals do not add up")


def _validate_boundary_confirmation(data: dict[str, Any]) -> None:
    boundary = _require_mapping(
        data.get("boundary_confirmation"),
        "boundary_confirmation",
    )
    for flag in REQUIRED_BOUNDARY_FLAGS:
        if boundary.get(flag) is not True:
            _fail(f"completion packet boundary_confirmation `{flag}` must be true")


def validate_packet(packet_path: str | Path, *, root: Path | None = None) -> dict[str, Any]:
    module_root = root or Path.cwd()
    packet = _resolve_packet_path(packet_path, module_root)
    data = _load_yaml(packet)

    _validate_required_identity(data)
    _validate_report_path(data, module_root)
    _validate_checks(data)
    _validate_boundary_confirmation(data)

    return data


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("ERROR: usage: validate_completion_packet.py <PACKET>", file=sys.stderr)
        return 2

    try:
        data = validate_packet(args[0])
    except CompletionPacketValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print("OK: completion packet schema validates")
    print(f"module_id: {data['module_id']}")
    print(f"prompt_id: {data['prompt_id']}")
    print(f"implementation_commit: {data['implementation_commit']}")
    print(f"completion_commit: {data['completion_commit']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
