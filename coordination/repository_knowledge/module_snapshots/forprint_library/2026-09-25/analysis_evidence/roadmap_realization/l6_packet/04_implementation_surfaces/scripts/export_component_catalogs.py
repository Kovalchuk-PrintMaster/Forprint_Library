from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SEED_PATH = ROOT / "catalog" / "seeds" / "catalog_seed_v0_1.yaml"

SECTIONS: dict[str, str] = {
    "materials": "materials.yaml",
    "product_families": "product_families.yaml",
    "operations": "operations.yaml",
    "print_modes": "print_modes.yaml",
    "finishing_options": "finishing_options.yaml",
}


def read_seed() -> dict[str, Any]:
    data = yaml.safe_load(SEED_PATH.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError("Catalog seed must be a YAML mapping.")
    return data


def main() -> int:
    seed = read_seed()
    metadata = seed["metadata"]

    for section, filename in SECTIONS.items():
        items = seed.get(section)
        if not isinstance(items, list):
            raise ValueError(f"Seed section must be a list: {section}")

        payload = {
            "catalog_type": section,
            "metadata": metadata,
            "items": items,
        }

        target_path = ROOT / "catalog" / filename
        target_path.write_text(
            yaml.safe_dump(payload, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
        print(f"OK: wrote {target_path.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())