from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
BLUEPRINT_SOURCE = ROOT / "coordination" / "blueprint_source.yaml"


@dataclass
class PathCheck:
    label: str
    path: Path
    required: bool


def load_blueprint_config() -> dict:
    if not BLUEPRINT_SOURCE.exists():
        raise FileNotFoundError(f"Missing {BLUEPRINT_SOURCE.relative_to(ROOT)}")

    data = yaml.safe_load(BLUEPRINT_SOURCE.read_text(encoding="utf-8")) or {}
    source = data.get("blueprint_source", {})
    if not isinstance(source, dict):
        raise ValueError("blueprint_source.yaml must contain blueprint_source mapping")
    return source


def main() -> int:
    try:
        source = load_blueprint_config()
    except Exception as exc:  # noqa: BLE001
        print(f"FAILED: {exc}")
        return 1

    blueprint_root = Path(source.get("blueprint_root", ""))
    if not blueprint_root.is_absolute():
        blueprint_root = (ROOT / blueprint_root).resolve()

    checks = [
        PathCheck("Blueprint root", blueprint_root, True),
        PathCheck(
            "Global policy",
            blueprint_root / source.get("global_policy_path", "coordination/global_policy"),
            True,
        ),
        PathCheck(
            "Standards",
            blueprint_root / source.get("standards_path", "coordination/standards"),
            True,
        ),
        PathCheck(
            "Module policy",
            blueprint_root
            / source.get(
                "module_policy_path",
                "coordination/module_policy/forprint_library/module_policy.md",
            ),
            True,
        ),
        PathCheck(
            "Global directives index",
            blueprint_root / "coordination/directives/global/index.yaml",
            True,
        ),
        PathCheck(
            "Module directives index",
            blueprint_root
            / source.get(
                "module_directives_index",
                "coordination/directives/modules/forprint_library/index.yaml",
            ),
            False,
        ),
    ]

    failed = False
    for check in checks:
        if check.path.exists():
            print(f"OK: {check.label}: {check.path}")
            continue

        if check.required:
            print(f"FAILED: {check.label} missing: {check.path}")
            failed = True
        else:
            print(f"WARN: {check.label} missing/deferred: {check.path}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())