"""Compile canonical flat item front matter into Ren'Py registrations (stdlib only).

Values use YAML-compatible JSON scalars/arrays/maps. Unknown prices remain TBD.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "docs/world/items"
OUTPUT = ROOT / "game/content/items.rpy"


def read_cards():
    result = []
    for path in sorted(CARDS.glob("*.md")):
        if path.name == "README.md": continue
        text = path.read_text(encoding="utf-8")
        header = text.split("---", 2)[1]
        definition = {}
        for line in header.splitlines():
            if not line.strip(): continue
            key, value = line.split(":", 1)
            value = value.strip()
            definition[key] = None if value == "TBD" else json.loads(value)
        result.append(definition)
    ids = [item["id"] for item in result]
    if len(ids) != len(set(ids)): raise ValueError("Duplicate item ids")
    return result


def render():
    lines = ["# Generated from docs/world/items by tools/sync_items.py. Do not edit.", "init -50 python:"]
    for item in read_cards():
        item = dict(item)
        item_id = item.pop("id")
        item.pop("status", None)
        register = "register_clothing" if item["storage"] == "wardrobe" else "register_item"
        lines.append("    %s(%r, **%r)" % (register, item_id, item))
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = render()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != expected:
            raise SystemExit("Item registrations differ from canonical cards")
        print("Item cards and runtime synchronized")
    else:
        OUTPUT.write_text(expected, encoding="utf-8")
