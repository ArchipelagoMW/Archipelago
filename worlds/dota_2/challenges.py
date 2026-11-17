"""Checks players can turn off or tune in their YAML, and the rules deciding what a match completes.

Shared by the world (locations and options) and the client. Covers the stat tiers, the wins by hero trait,
the purchases, and the global challenges and quests any hero can do.
"""
from __future__ import annotations

import json
from importlib import resources
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .dota_api import DotaMatchData

# Stat checks have three tiers each: (label, DotaMatchData field, default tiers, maximum value)
STATS = [
    ("Kills", "kills", (1, 5, 10), 50),
    ("Assists", "assists", (5, 10, 20), 60),
    ("Dewards", "dewards", (1, 3, 7), 30),
    ("Last Hits", "last_hits", (75, 125, 175), 800),
    ("Denies", "denies", (8, 16, 32), 100),
]


def stat_check(label: str, tier: int) -> str:
    return f"{label} Tier {tier}"


# OpenDota rune keys are the game's DOTA_RUNE values
RUNES = {
    "0": "Double Damage", "1": "Haste", "2": "Illusion", "3": "Invisibility", "4": "Regeneration",
    "5": "Bounty", "6": "Arcane", "7": "Water", "8": "Wisdom", "9": "Shield",
}


def rune_check(rune: str) -> str:
    article = "an" if rune[0] in "AEIOU" else "a"
    return f"Pick up {article} {rune} Rune"


# Quests add up over the whole seed: (check name, save total key, value that sets the target)
QUESTS = [
    ("Quest: Stack Camps", "camps_stacked", "Camps Stacked"),
    ("Quest: Place Wards", "wards_placed", "Wards Placed"),
    ("Quest: Damage Buildings", "building_damage", "Building Damage"),
]

# Global challenges, in location order. New checks go at the end so existing location ids don't move.
CHALLENGE_FAMILIES: dict[str, list[str]] = {
    "First Blood": ["Get First Blood"],
    "Courier Kill": ["Kill a Courier"],
    "Runes": [rune_check(r) for r in RUNES.values()],
    "Buyback": ["Use a Buyback"],
    "Aegis": ["Pick up the Aegis"],
    "Positions": [f"Win as Position {i}" for i in range(1, 6)],
    "Short Win": ["Win a Short Match"],
    "Long Win": ["Win a Long Match"],
    "Roshan Win": ["Win a Match Where Your Team Took Roshan"],
    "Quests": [name for name, _, _ in QUESTS],
}
CHALLENGE_CHECKS = [name for names in CHALLENGE_FAMILIES.values() for name in names]


def _purchase_checks() -> list[str]:
    with resources.files(__package__).joinpath("data/dotaShopLocations.json").open("r", encoding="utf-8") as f:
        return [item["dname"] for item in json.load(f).values() if item.get("dname")]


# Every family a YAML can turn off. Hero group wins and the goal stay, since the seed's progression relies on them.
FAMILIES: dict[str, list[str]] = {
    "Attribute Wins": ["Win as a Strength Hero", "Win as a Agility Hero", "Win as a Intelligence Hero", "Win as a Universal Hero"],
    "Attack Type Wins": ["Win as a Melee Hero", "Win as a Ranged Hero"],
    "Legs Wins": ["Win as a 0 Legged Hero", "Win as a 2 Legged Hero", "Win as a 4+ Legged Hero"],
    "Role Wins": ["Win as a Carry Hero", "Win as a Support Hero"],
    **{label: [stat_check(label, t) for t in (1, 2, 3)] for label, _, _, _ in STATS},
    "Purchases": _purchase_checks(),
    **CHALLENGE_FAMILIES,
}
DISABLEABLE_CHECKS = sorted({name for names in FAMILIES.values() for name in names})

# Values players can change in their YAML: name -> (default, minimum, maximum)
VALUES: dict[str, tuple[int, int, int]] = {
    **{stat_check(label, t): (default, 1, maximum)
       for label, _, defaults, maximum in STATS for t, default in enumerate(defaults, 1)},
    "Short Win Minutes": (30, 15, 45),
    "Long Win Minutes": (60, 40, 90),
    "Roshan Kills": (1, 1, 4),
    "Camps Stacked": (10, 1, 100),
    "Wards Placed": (15, 1, 200),
    "Building Damage": (10000, 1000, 200000),
}


def resolve_disabled(disabled: set[str]) -> set[str]:
    """Check names disabled by the YAML, families expanded."""
    return {name for key in disabled for name in FAMILIES.get(key, [key])}


def resolve_values(chosen: dict[str, int]) -> dict[str, int]:
    """Defaults, overridden by what the YAML sets."""
    return {name: int(chosen.get(name, default)) for name, (default, _, _) in VALUES.items()}


def challenge_values(slot_data: dict[str, Any]) -> dict[str, int]:
    """Values for this seed, as sent in slot_data."""
    return resolve_values(slot_data.get("check_values") or {})


def stat_checks(m: DotaMatchData, values: dict[str, int]) -> list[str]:
    """Stat tiers reached in a match."""
    return [stat_check(label, t) for label, field, _, _ in STATS for t in (1, 2, 3)
            if getattr(m, field) >= values[stat_check(label, t)]]


def match_challenges(m: DotaMatchData, values: dict[str, int]) -> list[str]:
    """Challenge checks completed by a single match (quests are counted separately, over the seed)."""
    won = m.win == 1
    checks = []
    if m.first_blood:
        checks.append("Get First Blood")
    if m.courier_kills > 0:
        checks.append("Kill a Courier")
    checks += [rune_check(RUNES[key]) for key, count in m.runes.items() if count and key in RUNES]
    if m.buybacks > 0:
        checks.append("Use a Buyback")
    if m.aegis:
        checks.append("Pick up the Aegis")
    if won and 1 <= m.position <= 5:
        checks.append(f"Win as Position {m.position}")
    # A match ended early by a leaver or with bots doesn't count as a short win
    if won and m.all_players_stayed and m.duration < values["Short Win Minutes"] * 60:
        checks.append("Win a Short Match")
    if won and m.duration >= values["Long Win Minutes"] * 60:
        checks.append("Win a Long Match")
    if won and m.team_roshan_kills >= values["Roshan Kills"]:
        checks.append("Win a Match Where Your Team Took Roshan")
    return checks


def quest_amounts(m: DotaMatchData) -> dict[str, int]:
    """What a match adds to each quest total."""
    return {"camps_stacked": m.camps_stacked, "wards_placed": m.wards_placed, "building_damage": m.building_damage}


def completed_quests(totals: dict[str, int], values: dict[str, int]) -> list[str]:
    return [name for name, key, value in QUESTS if totals.get(key, 0) >= values[value]]
