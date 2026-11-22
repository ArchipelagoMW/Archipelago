"""Refreshes the game data from OpenDota after a Dota 2 update, then the id registry.

From the repository root: python -m worlds.dota_2.tools.update_data
It adds new shop items, components and heroes, follows recipe changes and refreshes damage types, but never
overwrites what was set by hand (hero roles, data/shopOverrides.json). To drop an item Valve removed, add it to
"exclude" in data/shopOverrides.json. Then review the summary and the diff, raise world_version in
archipelago.json and run the tests (docs/updating.md).
"""
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

OPENDOTA = "https://api.opendota.com/api/constants/"
DATA = Path(__file__).resolve().parent.parent / "data"
# Fields of OpenDota's items kept in dotaShopLocations.json
SHOP_FIELDS = ["hint", "id", "img", "dname", "qual", "cost", "behavior", "target_team", "target_type", "dmg_type",
               "bkbpierce", "dispellable", "notes", "mc", "hc", "cd", "lore", "components", "created", "charges"]
HERO_FIELDS = ["id", "name", "localized_name", "primary_attr", "attack_type", "roles", "legs"]


def fetch(name: str) -> dict:
    request = urllib.request.Request(OPENDOTA + name, headers={"User-Agent": "Archipelago DOTA 2 data update"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def load(name: str):
    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)


def save(name: str, data, indent: int) -> None:
    """Writes a data file, only when its content changed (files edited by hand keep their layout)."""
    if load(name) == data:
        return
    with open(DATA / name, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)
        f.write("\n")


def components(key: str, items: dict) -> list[str]:
    """Direct components, recipes and empty names left out; Dagon 2 and the like are bought from level 1."""
    found = [c for c in (items.get(key, {}).get("components") or []) if c and not c.startswith("recipe_")]
    base = re.sub(r"_\d+$", "", key)
    if not found and base != key and base in items:
        return [base]
    return found


def requirements(key: str, items: dict, free: set[str]) -> list[str]:
    """The basic components to unlock before buying an item; a basic item needs its own unlock."""
    parts = components(key, items)
    if not parts:
        return [] if key in free else [key]
    found = []
    for part in parts:
        found += [r for r in requirements(part, items, free) if r not in found]
    return found


def update_shop(items: dict, summary: list[str]) -> dict:
    shop, overrides = load("dotaShopLocations.json"), load("shopOverrides.json")
    exclude, free, by_hand = set(overrides["exclude"]), set(overrides["free"]), overrides["requirements"]
    for key in [k for k in shop if k in exclude]:
        summary.append(f"Shop: removed {shop.pop(key)['dname']}")
    candidates = [k for k, v in items.items() if v.get("dname") and (v.get("cost") or 0) > 0
                  and not k.startswith("recipe_") and k not in exclude]
    for key in candidates:
        needed = by_hand.get(key) or requirements(key, items, free)
        if key not in shop:
            shop[key] = {**{f: items[key][f] for f in SHOP_FIELDS if f in items[key]}, "requirements": needed}
            summary.append(f"Shop: added {shop[key]['dname']} (needs {', '.join(needed) or 'nothing'})")
        elif sorted(shop[key].get("requirements") or []) != sorted(needed):
            summary.append(f"Shop: {shop[key]['dname']} now needs {', '.join(needed) or 'nothing'} "
                           f"(was {', '.join(shop[key].get('requirements') or []) or 'nothing'})")
            shop[key]["requirements"] = needed
    save("dotaShopLocations.json", shop, 2)
    return shop


def update_unlocks(shop: dict, summary: list[str]) -> None:
    """One "Unlock <component>" per basic component a purchase needs."""
    data = load("unlockDotaShopItems.json")
    needed = {r for item in shop.values() for r in item.get("requirements") or []}
    kept = [u for u in data["unlock_shop_items"] if u["name"].removeprefix("Unlock ") in needed]
    summary += [f"Components: removed {u['name']}" for u in data["unlock_shop_items"] if u not in kept]
    names, next_id = {u["name"] for u in kept}, max(u["id"] for u in data["unlock_shop_items"]) + 1
    for component in sorted(needed):
        if f"Unlock {component}" not in names:
            kept.append({"id": next_id, "name": f"Unlock {component}", "classification": "progression", "copies": 1,
                         "include_in_filler": "False"})
            next_id += 1
            summary.append(f"Components: added Unlock {component}")
    save("unlockDotaShopItems.json", {"unlock_shop_items": kept}, 4)


def update_heroes(heroes: dict, summary: list[str]) -> None:
    """New heroes are added; existing ones are kept as they are (roles were adjusted by hand)."""
    data = load("heroes.json")
    known = {h["id"] for h in data["dota_heroes"]}
    for hero in sorted(heroes.values(), key=lambda h: h["id"]):
        if hero["id"] not in known:
            data["dota_heroes"].append({f: hero.get(f) for f in HERO_FIELDS})
            summary.append(f"Heroes: added {hero['localized_name']} (roles {', '.join(hero['roles'])}: check Carry and Support)")
    save("heroes.json", data, 2)


def update_damage_types(abilities: dict, summary: list[str]) -> None:
    data = load("abilityDamageTypes.json")
    types = {k: a["dmg_type"] for k, a in sorted(abilities.items()) if a.get("dmg_type") in ("Magical", "Physical", "Pure")}
    changed = sum(1 for k in set(types) | set(data["ability_damage_types"]) if types.get(k) != data["ability_damage_types"].get(k))
    if changed:
        summary.append(f"Damage types: {changed} abilities changed")
    data["ability_damage_types"] = types
    save("abilityDamageTypes.json", data, 1)


def main() -> None:
    summary: list[str] = []
    items, heroes, abilities = fetch("items"), fetch("heroes"), fetch("abilities")
    shop = update_shop(items, summary)
    update_unlocks(shop, summary)
    update_heroes(heroes, summary)
    update_damage_types(abilities, summary)
    print("\n".join(summary) or "Game data: nothing new.", flush=True)
    # The registry reads the data files at import, so in a fresh process
    subprocess.run([sys.executable, "-m", "worlds.dota_2.tools.update_ids"], check=True)


if __name__ == "__main__":
    main()
