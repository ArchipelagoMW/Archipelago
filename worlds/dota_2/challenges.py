"""Checks players can turn off or tune in their YAML, and the rules deciding what a match completes.

Shared by the world (locations and options) and the client. Covers the stats, the wins by hero trait,
the purchases, and the global challenges and quests any hero can do.
"""
from __future__ import annotations

import json
from importlib import resources
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .dota_api import DotaMatchData

MAX_THRESHOLDS = 5  # checks per stat or quest, one per threshold

# Stats, in one match: one check per threshold set in the YAML. Defaults are round numbers a bit above what a player
# in the most favourable position reaches one match in four (OpenDota public matches).
# (label, DotaMatchData field, default thresholds, maximum threshold)
STATS = [
    ("Kills", "kills", [15], 50),
    ("Assists", "assists", [30], 60),
    ("Dewards", "dewards", [5], 30),
    ("Last Hits", "last_hits", [450], 800),
    ("Denies", "denies", [20], 100),
    ("Healing", "healing", [2000], 50000),
    ("Physical Damage", "physical_damage", [25000], 200000),
    ("Magical Damage", "magical_damage", [20000], 200000),
    ("Physical Hit", "physical_hit", [500], 5000),
    ("Magical Hit", "magical_hit", [500], 5000),
    ("Stun Time", "stun_time", [60], 600),  # seconds of stun on enemy heroes
]
ORIGINAL_STATS = ["Kills", "Assists", "Dewards", "Last Hits", "Denies"]  # their #1 to #3 reuse the original locations
ORIGINAL_STAT_CHECKS = 3

# Quests add up over the whole seed, with a lower and a full target by default.
# (label, save total key and DotaMatchData field, value name, default thresholds, maximum threshold)
QUESTS = [
    ("Stack Camps", "camps_stacked", "Camps Stacked", [10, 20], 100),
    ("Place Wards", "wards_placed", "Wards Placed", [50, 100], 300),
    ("Damage Buildings", "building_damage", "Building Damage", [25000, 50000], 200000),
    ("Heal Heroes", "healing", "Total Healing", [7500, 15000], 500000),
    ("Deal Physical Damage", "physical_damage", "Total Physical Damage", [75000, 150000], 2000000),
    ("Deal Magical Damage", "magical_damage", "Total Magical Damage", [60000, 120000], 2000000),
    ("Stun Enemies", "stun_time", "Total Stun Time", [200, 400], 10000),
]


def numbered(label: str, n: int) -> str:
    """Name of the n-th check of a stat or quest, by increasing threshold. Names can't hold the threshold, which
    depends on the YAML."""
    return f"{label} #{n}"


stat_check = numbered

# OpenDota rune keys are the game's DOTA_RUNE values
RUNES = {
    "0": "Double Damage", "1": "Haste", "2": "Illusion", "3": "Invisibility", "4": "Regeneration",
    "5": "Bounty", "6": "Arcane", "7": "Water", "8": "Wisdom", "9": "Shield",
}


def rune_check(rune: str) -> str:
    article = "an" if rune[0] in "AEIOU" else "a"
    return f"Pick up {article} {rune} Rune"


# Global challenges of one match, in location order
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
}
QUEST_FAMILIES = {label: [numbered(label, n) for n in range(1, MAX_THRESHOLDS + 1)] for label, _, _, _, _ in QUESTS}
# New locations, in location order: challenges, then quests
CHALLENGE_CHECKS = [name for names in [*CHALLENGE_FAMILIES.values(), *QUEST_FAMILIES.values()] for name in names]


def _purchase_checks() -> list[str]:
    with resources.files(__package__).joinpath("data/dotaShopLocations.json").open("r", encoding="utf-8") as f:
        return [item["dname"] for item in json.load(f).values() if item.get("dname")]


# Every family a YAML can turn off. Hero group wins and the goal stay, since the seed's progression relies on them.
FAMILIES: dict[str, list[str]] = {
    "Attribute Wins": ["Win as a Strength Hero", "Win as a Agility Hero", "Win as a Intelligence Hero", "Win as a Universal Hero"],
    "Attack Type Wins": ["Win as a Melee Hero", "Win as a Ranged Hero"],
    "Legs Wins": ["Win as a 0 Legged Hero", "Win as a 2 Legged Hero", "Win as a 4+ Legged Hero"],
    "Role Wins": ["Win as a Carry Hero", "Win as a Support Hero"],
    **{label: [numbered(label, n) for n in range(1, MAX_THRESHOLDS + 1)] for label, _, _, _ in STATS},
    "Purchases": _purchase_checks(),
    **CHALLENGE_FAMILIES,
    **QUEST_FAMILIES,
    "Quests": [name for names in QUEST_FAMILIES.values() for name in names],
}
DISABLEABLE_CHECKS = sorted({name for names in FAMILIES.values() for name in names})

# Values players can change in their YAML: name -> (default, minimum, maximum).
# Stats and quests take one threshold, or a list of up to MAX_THRESHOLDS thresholds (one check each).
VALUES: dict[str, tuple[Any, int, int]] = {
    **{label: (default, 1, maximum) for label, _, default, maximum in STATS},
    "Short Win Minutes": (30, 15, 45),
    "Long Win Minutes": (60, 40, 90),
    "Roshan Kills": (1, 1, 4),
    **{value: (default, 1, maximum) for _, _, value, default, maximum in QUESTS},
}
# Values that take a list of thresholds, and the checks each one numbers
MULTI_VALUES = {**{label: label for label, _, _, _ in STATS}, **{value: label for label, _, value, _, _ in QUESTS}}


def resolve_disabled(disabled: set[str]) -> set[str]:
    """Check names disabled by the YAML, families expanded."""
    return {name for key in disabled for name in FAMILIES.get(key, [key])}


def thresholds(value: int | list[int]) -> list[int]:
    return sorted({int(v) for v in value}) if isinstance(value, (list, tuple, set)) else [int(value)]


def resolve_values(chosen: dict[str, Any]) -> dict[str, Any]:
    """Defaults, overridden by what the YAML sets. Stats and quests become sorted lists of thresholds."""
    return {name: thresholds(chosen.get(name, default)) if name in MULTI_VALUES else int(chosen.get(name, default))
            for name, (default, _, _) in VALUES.items()}


def numbered_checks_in_seed(values: dict[str, Any]) -> dict[str, bool]:
    """For each numbered check (Kills #2, Stack Camps #1...), whether this seed's values give it a threshold."""
    return {numbered(label, n): n <= len(values[value]) for value, label in MULTI_VALUES.items()
            for n in range(1, MAX_THRESHOLDS + 1)}


def challenge_values(slot_data: dict[str, Any]) -> dict[str, Any]:
    """Values for this seed, as sent in slot_data."""
    return resolve_values(slot_data.get("check_values") or {})


def stat_checks(m: DotaMatchData, values: dict[str, Any]) -> list[str]:
    """Stat thresholds reached in a match."""
    return [numbered(label, n) for label, field, _, _ in STATS
            for n, threshold in enumerate(values[label], 1) if getattr(m, field) >= threshold]


def match_challenges(m: DotaMatchData, values: dict[str, Any]) -> list[str]:
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
    return {key: getattr(m, key) for _, key, _, _, _ in QUESTS}


def completed_quests(totals: dict[str, int], values: dict[str, Any]) -> list[str]:
    return [numbered(label, n) for label, key, value, _, _ in QUESTS
            for n, threshold in enumerate(values[value], 1) if totals.get(key, 0) >= threshold]
