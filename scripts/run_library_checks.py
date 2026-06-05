from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "reports"
JSON_REPORT = REPORTS_DIR / "library_check_report.json"
MD_REPORT = REPORTS_DIR / "library_check_report.md"

OK = "OK"
WARN = "WARN"
FAILED = "FAILED"

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"


@dataclass
class CheckResult:
    name: str
    expected: str
    status: str
    seconds: float
    details: str = ""


def color_status(status: str) -> str:
    if status == OK:
        return f"{GREEN}{status}{RESET}"
    if status == WARN:
        return f"{YELLOW}{status}{RESET}"
    return f"{RED}{status}{RESET}"


def run_command(name: str, expected: str, command: list[str]) -> CheckResult:
    started = time.perf_counter()
    proc = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    seconds = time.perf_counter() - started
    output = proc.stdout.strip()
    status = OK if proc.returncode == 0 else FAILED
    return CheckResult(name, expected, status, seconds, output)


def check_file_exists(name: str, expected: str, path: Path, warn_only: bool = False) -> CheckResult:
    started = time.perf_counter()
    exists = path.exists()
    seconds = time.perf_counter() - started
    if exists:
        return CheckResult(name, expected, OK, seconds, str(path.relative_to(ROOT)))
    status = WARN if warn_only else FAILED
    return CheckResult(name, expected, status, seconds, f"Missing: {path.relative_to(ROOT)}")


def check_yaml_file(name: str, expected: str, path: Path, warn_only: bool = False) -> CheckResult:
    started = time.perf_counter()
    if not path.exists():
        seconds = time.perf_counter() - started
        status = WARN if warn_only else FAILED
        return CheckResult(name, expected, status, seconds, f"Missing: {path.relative_to(ROOT)}")

    try:
        with path.open("r", encoding="utf-8") as fh:
            yaml.safe_load(fh) or {}
    except Exception as exc:  # noqa: BLE001
        seconds = time.perf_counter() - started
        return CheckResult(name, expected, FAILED, seconds, f"Invalid YAML: {exc}")

    seconds = time.perf_counter() - started
    return CheckResult(name, expected, OK, seconds, str(path.relative_to(ROOT)))


def check_make_targets() -> CheckResult:
    started = time.perf_counter()
    makefile = ROOT / "Makefile"
    required_targets = {
        "install",
        "lint",
        "lint-fix",
        "test",
        "check",
        "check-report",
        "blueprint-pull",
        "blueprint-check",
        "blueprint-sync-directives",
        "coordination-check",
        "coordination-fix",
        "module-policy-check",
    }

    if not makefile.exists():
        return CheckResult(
            "Makefile standard targets",
            "Required targets exist",
            FAILED,
            time.perf_counter() - started,
            "Missing Makefile",
        )

    text = makefile.read_text(encoding="utf-8")
    missing = sorted(target for target in required_targets if f"{target}:" not in text)
    status = OK if not missing else FAILED
    details = "All required targets found." if not missing else f"Missing targets: {missing}"
    return CheckResult(
        "Makefile standard targets",
        "Required targets exist",
        status,
        time.perf_counter() - started,
        details,
    )


def check_manifest_boundaries() -> CheckResult:
    started = time.perf_counter()
    path = ROOT / "forprint_module_manifest.yaml"
    if not path.exists():
        return CheckResult(
            "Module manifest boundary",
            "Manifest exists and forbids operational ownership",
            FAILED,
            time.perf_counter() - started,
            "Missing forprint_module_manifest.yaml",
        )

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as exc:  # noqa: BLE001
        return CheckResult(
            "Module manifest boundary",
            "Manifest exists and forbids operational ownership",
            FAILED,
            time.perf_counter() - started,
            f"Invalid YAML: {exc}",
        )

    does_not_own = set(data.get("boundaries", {}).get("does_not_own", []))
    required_forbidden = {
        "client registry",
        "order registry",
        "payment registry",
        "warehouse stock truth",
        "production runtime",
        "1C synchronization",
        "CRM workflow",
        "Telegram runtime",
        "Calculator business logic",
    }
    missing = sorted(required_forbidden - does_not_own)
    status = OK if not missing else FAILED
    if not missing:
        details = "Boundary exclusions are present."
    else:
        details = f"Missing exclusions: {missing}"
    return CheckResult(
        "Module manifest boundary",
        "Manifest exists and forbids operational ownership",
        status,
        time.perf_counter() - started,
        details,
    )


def check_catalog_seed_deferred() -> CheckResult:
    started = time.perf_counter()
    path = ROOT / "catalog" / "seeds" / "catalog_seed_v0_1.yaml"
    if path.exists():
        return CheckResult(
            "Catalog seed validation",
            "Seed exists or is deferred to Checkpoint B",
            OK,
            time.perf_counter() - started,
            "Catalog seed exists.",
        )
    return CheckResult(
        "Catalog seed validation",
        "Seed exists or is deferred to Checkpoint B",
        WARN,
        time.perf_counter() - started,
        "Deferred to Checkpoint B.",
    )


def check_architecture_docs_deferred() -> CheckResult:
    started = time.perf_counter()
    required = [
        ROOT / "docs" / "architecture" / "canonical_id_policy.md",
        ROOT / "docs" / "architecture" / "alias_policy.md",
        ROOT / "docs" / "architecture" / "dependent_module_usage.md",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if not missing:
        status = OK
        details = "Required architecture docs exist."
    else:
        status = WARN
        details = f"Deferred to Checkpoint C: {missing}"
    return CheckResult(
        "Required architecture docs",
        "Docs exist or are deferred to Checkpoint C",
        status,
        time.perf_counter() - started,
        details,
    )


def collect_results(skip_external: bool = False) -> list[CheckResult]:
    python = sys.executable

    results = [
        run_command("Ruff lint", "No lint errors", 
                    [python, "-m", "ruff", "check", "app", "scripts", "tests"]),
        run_command("Pytest", "All tests pass", [python, "-m", "pytest"]),
        check_catalog_seed_deferred(),
        check_architecture_docs_deferred(),
        check_yaml_file(
            "Blueprint source config",
            "blueprint_source.yaml is valid",
            ROOT / "coordination" / "blueprint_source.yaml",
        ),
        check_yaml_file(
            "Prompts index",
            "coordination/prompts/index.yaml is valid",
            ROOT / "coordination" / "prompts" / "index.yaml",
        ),
        check_yaml_file(
            "Reports index",
            "coordination/reports/index.yaml is valid",
            ROOT / "coordination" / "reports" / "index.yaml",
        ),
        check_file_exists(
            "Coordination status YAML",
            "current_status.yaml exists",
            ROOT / "coordination" / "status" / "current_status.yaml",
        ),
        check_file_exists(
            "Coordination status MD",
            "current_status.md exists",
            ROOT / "coordination" / "status" / "current_status.md",
        ),
        check_file_exists(
            "Next questions",
            "next_questions_for_blueprint.md exists",
            ROOT / "coordination" / "status" / "next_questions_for_blueprint.md",
        ),
        check_manifest_boundaries(),
        check_make_targets(),
    ]

    if not skip_external:
        results.append(
            run_command(
                "Blueprint policy check",
                "Blueprint paths readable; module directives may be deferred",
                [python, "scripts/check_blueprint_instructions.py"],
            )
        )

    return results


def write_reports(results: list[CheckResult]) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    payload: dict[str, Any] = {
        "module_id": "forprint_library",
        "report": "library_check_report",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "summary": {
            "ok": sum(1 for item in results if item.status == OK),
            "warn": sum(1 for item in results if item.status == WARN),
            "failed": sum(1 for item in results if item.status == FAILED),
        },
        "checks": [asdict(item) for item in results],
    }

    JSON_REPORT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    lines = [
        "# ForPrint Library Check Report",
        "",
        f"Generated at: `{payload['generated_at']}`",
        "",
        "| Check | Expected result | Status | Time | Details |",
        "|---|---|---:|---:|---|",
    ]
    for item in results:
        details = item.details.replace("\n", "<br>")
        lines.append(
            f"| {item.name} | {item.expected} | {item.status} | {item.seconds:.2f}s | {details} |"
        )

    MD_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def print_table(results: list[CheckResult]) -> None:
    print("\nForPrint Library — check report\n")

    headers = ("Check", "Expected result", "Status", "Time")
    rows = [
        (item.name, item.expected, color_status(item.status), f"{item.seconds:.2f}s")
        for item in results
    ]

    plain_rows = [(item.name, item.expected, item.status, 
                   f"{item.seconds:.2f}s") for item in results]
    widths = [
        max(len(headers[index]), *(len(row[index]) for row in plain_rows))
        for index in range(len(headers))
    ]

    def line(left: str, middle: str, right: str) -> str:
        return left + middle.join("─" * (width + 2) for width in widths) + right

    print(line("┌", "┬", "┐"))
    print(
        "│ "
        + " │ ".join(headers[index].ljust(widths[index]) for index in range(len(headers)))
        + " │"
    )
    print(line("├", "┼", "┤"))
    for row in rows:
        print(
            "│ "
            + " │ ".join(str(row[index]).ljust(widths[index]) for index in range(len(headers)))
            + " │"
        )
    print(line("└", "┴", "┘"))
    print(
        "\nReports written:"
        f"\n- {JSON_REPORT.relative_to(ROOT)}"
        f"\n- {MD_REPORT.relative_to(ROOT)}\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-external", action="store_true")
    args = parser.parse_args()

    results = collect_results(skip_external=args.skip_external)
    write_reports(results)
    print_table(results)

    failed = [item for item in results if item.status == FAILED]
    if failed:
        print("FAILED checks:")
        for item in failed:
            print(f"- {item.name}: {item.details}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())