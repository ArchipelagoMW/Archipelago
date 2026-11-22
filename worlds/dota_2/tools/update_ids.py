"""Gives an id in data/ids.json to every location and item name that doesn't have one yet, at the end.

From the repository root: python -m worlds.dota_2.tools.update_ids (update_data runs it).
"""
import json
from pathlib import Path

from ..items import FILLER_ITEM_NAME, load_item_defs
from ..locations import all_location_defs

REGISTRY = Path(__file__).resolve().parent.parent / "data" / "ids.json"


def add_names(ids: dict[str, int], names: list[str]) -> list[str]:
    added = [name for name in dict.fromkeys(names) if name not in ids]
    for next_id, name in enumerate(added, max(ids.values()) + 1):
        ids[name] = next_id
    return added


def main() -> None:
    with open(REGISTRY, encoding="utf-8") as f:
        registry = json.load(f)
    added = add_names(registry["locations"], [d.name for d in all_location_defs()])
    added += add_names(registry["items"], [d.name for d in load_item_defs()] + [FILLER_ITEM_NAME])
    with open(REGISTRY, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print("Ids: " + (", ".join(added) if added else "nothing new") + ".")


if __name__ == "__main__":
    main()
