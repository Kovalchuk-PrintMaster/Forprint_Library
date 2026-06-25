from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path
from typing import Any

import yaml

MODULE_ROOT = Path(__file__).resolve().parents[1]
BLUEPRINT_ROOT = MODULE_ROOT.parent / "forprint_system_blueprint"

ACTIVE_PROMPT = (
    BLUEPRINT_ROOT
    / "coordination"
    / "outgoing_prompts"
    / "forprint_library"
    / "approved"
    / "2026-06-23__library__make_first_semantic_reference_readiness_v0_1.md"
)

LOCAL_ACTIVE_PROMPT_DIR = MODULE_ROOT / "coordination" / "prompts" / "active"
LOCAL_ACTIVE_PROMPT = LOCAL_ACTIVE_PROMPT_DIR / ACTIVE_PROMPT.name

LOCAL_STANDARDS_DIR = MODULE_ROOT / "coordination" / "standards"
LOCAL_STANDARDS_SNAPSHOT = LOCAL_STANDARDS_DIR / "blueprint_standards_available_snapshot.yaml"

COMPLETION_PACKET_DIRS = [
    MODULE_ROOT / "coordination" / "completion_packet",
    MODULE_ROOT / "coordination" / "completion_packets",
]


def print_header(title: str) -> None:
    print()
    print(title)
    print("=" * len(title))


def git_commit(path: Path) -> str:
    completed = subprocess.run(
        ["git", "-C", str(path), "log", "-1", "--oneline"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return completed.stdout.strip()


def read_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )


def require_path(path: Path, label: str) -> None:
    if not path.exists():
        raise SystemExit(f"ERROR: missing {label}: {path}")
    print(f"OK: {label}: {path}")


def action_instruction_list() -> int:
    print_header("Blueprint instruction list")
    print(f"Blueprint root: {BLUEPRINT_ROOT}")
    print(f"Blueprint commit: {git_commit(BLUEPRINT_ROOT)}")
    print(f"Active Library prompt: {ACTIVE_PROMPT}")

    outgoing_root = BLUEPRINT_ROOT / "coordination" / "outgoing_prompts" / "forprint_library"
    if outgoing_root.exists():
        for path in sorted(outgoing_root.rglob("*.md")):
            print(f"- {path.relative_to(BLUEPRINT_ROOT)}")

    return 0


def action_instruction_check() -> int:
    print_header("Blueprint instruction check")
    require_path(BLUEPRINT_ROOT, "Blueprint root")
    require_path(ACTIVE_PROMPT, "active Library outgoing prompt")

    text = ACTIVE_PROMPT.read_text(encoding="utf-8")
    required_phrases = [
        "make_first_semantic_reference_readiness_v0_1",
        "forprint_library",
        "semantic",
        "reference",
    ]

    missing = [phrase for phrase in required_phrases if phrase not in text]
    if missing:
        raise SystemExit(f"ERROR: active prompt is missing phrases: {missing}")

    print("OK: active prompt is readable and matches expected semantic readiness topic")
    return 0


def action_instruction_sync() -> int:
    print_header("Blueprint instruction sync")
    action_instruction_check()

    LOCAL_ACTIVE_PROMPT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ACTIVE_PROMPT, LOCAL_ACTIVE_PROMPT)

    print(f"OK: synced active prompt to {LOCAL_ACTIVE_PROMPT.relative_to(MODULE_ROOT)}")
    return 0


def action_standards_list() -> int:
    print_header("Blueprint standards list")
    standards_root = BLUEPRINT_ROOT / "coordination" / "standards"
    require_path(standards_root, "Blueprint standards directory")

    for path in sorted(standards_root.rglob("*")):
        if path.is_file():
            print(f"- {path.relative_to(BLUEPRINT_ROOT)}")

    return 0


def action_standards_check() -> int:
    print_header("Blueprint standards check")
    standards_root = BLUEPRINT_ROOT / "coordination" / "standards"
    require_path(standards_root, "Blueprint standards directory")

    files = [path for path in standards_root.rglob("*") if path.is_file()]
    if not files:
        raise SystemExit("ERROR: Blueprint standards directory is empty")

    print(f"OK: Blueprint standards files found: {len(files)}")
    return 0


def action_standards_sync() -> int:
    print_header("Blueprint standards sync")
    action_standards_check()

    standards_root = BLUEPRINT_ROOT / "coordination" / "standards"
    files = [
        str(path.relative_to(BLUEPRINT_ROOT))
        for path in sorted(standards_root.rglob("*"))
        if path.is_file()
    ]

    snapshot = {
        "module_id": "forprint_library",
        "snapshot_type": "blueprint_standards_available_snapshot",
        "blueprint_root": str(BLUEPRINT_ROOT),
        "blueprint_commit": git_commit(BLUEPRINT_ROOT),
        "standards_files": files,
        "notes": [
            "This is a safe local availability snapshot.",
            "It does not override Blueprint standards.",
        ],
    }

    write_yaml(LOCAL_STANDARDS_SNAPSHOT, snapshot)
    print(f"OK: wrote {LOCAL_STANDARDS_SNAPSHOT.relative_to(MODULE_ROOT)}")
    return 0


def action_prompts_list() -> int:
    print_header("Blueprint prompts list")
    prompt_root = BLUEPRINT_ROOT / "coordination" / "outgoing_prompts" / "forprint_library"
    require_path(prompt_root, "Blueprint Library outgoing prompts directory")

    for path in sorted(prompt_root.rglob("*.md")):
        print(f"- {path.relative_to(BLUEPRINT_ROOT)}")

    return 0


def action_prompts_check() -> int:
    print_header("Blueprint prompts check")
    return action_instruction_check()


def action_prompts_sync() -> int:
    print_header("Blueprint prompts sync")
    return action_instruction_sync()


def action_prompt_read() -> int:
    print_header("Active Blueprint prompt for Library")
    action_instruction_check()

    print()
    print(ACTIVE_PROMPT.read_text(encoding="utf-8"))
    return 0


def action_blueprint_sync() -> int:
    print_header("Blueprint sync summary")
    action_instruction_check()
    action_standards_check()
    action_prompts_check()
    action_standards_sync()
    action_prompts_sync()
    print("OK: Blueprint prompts and standards snapshots are available locally")
    return 0


def action_report_clean() -> int:
    print_header("Report clean")
    patterns = [
        "__pycache__",
        ".pytest_cache",
        ".ruff_cache",
    ]

    removed = 0
    for pattern in patterns:
        for path in MODULE_ROOT.rglob(pattern):
            if path.is_dir():
                shutil.rmtree(path)
                removed += 1
                print(f"removed: {path.relative_to(MODULE_ROOT)}")

    for path in MODULE_ROOT.rglob("*.egg-info"):
        if path.is_dir():
            shutil.rmtree(path)
            removed += 1
            print(f"removed: {path.relative_to(MODULE_ROOT)}")

    print(f"OK: report clean completed, removed directories: {removed}")
    return 0


def completion_packet_status() -> tuple[bool, list[Path]]:
    existing = [path for path in COMPLETION_PACKET_DIRS if path.exists()]
    return bool(existing), existing


def action_completion_packet_validate() -> int:
    print_header("Completion packet validate")
    exists, paths = completion_packet_status()

    if not exists:
        print("DEFERRED: completion packet automation is not configured in Library yet.")
        print("Missing one of:")
        for path in COMPLETION_PACKET_DIRS:
            print(f"- {path.relative_to(MODULE_ROOT)}")
        print("This target is safe and explicit: no packet is applied or faked.")
        return 0

    for path in paths:
        print(f"OK: completion packet directory exists: {path.relative_to(MODULE_ROOT)}")

    return 0


def action_completion_packet_apply() -> int:
    print_header("Completion packet apply")
    exists, _paths = completion_packet_status()

    if not exists:
        print("DEFERRED: no completion packet automation exists, nothing to apply.")
        print("No files were changed.")
        return 0

    print("DEFERRED: apply logic is intentionally not implemented without Blueprint approval.")
    print("No files were changed.")
    return 0


def action_completion_packet_check() -> int:
    print_header("Completion packet check")
    action_completion_packet_validate()
    action_completion_packet_apply()
    return 0


ACTIONS = {
    "instruction-list": action_instruction_list,
    "instruction-check": action_instruction_check,
    "instruction-sync": action_instruction_sync,
    "standards-list": action_standards_list,
    "standards-check": action_standards_check,
    "standards-sync": action_standards_sync,
    "prompts-list": action_prompts_list,
    "prompts-check": action_prompts_check,
    "prompts-sync": action_prompts_sync,
    "prompt-read": action_prompt_read,
    "blueprint-sync": action_blueprint_sync,
    "report-clean": action_report_clean,
    "completion-packet-validate": action_completion_packet_validate,
    "completion-packet-apply": action_completion_packet_apply,
    "completion-packet-check": action_completion_packet_check,
}


def main() -> int:
    parser = argparse.ArgumentParser(description="ForPrint Library make-first workflow helper")
    parser.add_argument("action", choices=sorted(ACTIONS))
    args = parser.parse_args()

    return ACTIONS[args.action]()


if __name__ == "__main__":
    raise SystemExit(main())