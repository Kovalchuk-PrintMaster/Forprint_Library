from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
CARD_PATH = ROOT / "catalog" / "configurable_products" / "business_card.yaml"


def load_card() -> dict[str, Any]:
    data = yaml.safe_load(CARD_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise AssertionError("Business card product card must be a mapping")
    return data


def main() -> int:
    card = load_card()

    print(f"Product card: {card['names']['uk']}")
    print(f"Product ID: {card['product_id']}")
    print(f"Kind: {card['kind']}")
    print(f"Status: {card['status']}")
    print()
    print("Constructor parameters:")
    for parameter in card["constructor_parameters"]:
        print(f"- {parameter['key']}")
    print()
    print("Consumer notes:")
    notes = card["consumer_usage_notes"]
    print(f"- Telegram Bot: {notes['telegram_bot']['allowed_use']}")
    print(f"- Calculator Engine: {notes['calculator_engine']['allowed_use']}")
    print(
        "- Operational Registry: "
        f"{notes['forprint_operational_registry']['allowed_use']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())