"""Global challenge checks: things any hero can do in a match, read from OpenDota's parsed match data.

Shared by the world (locations and options) and the client (which decides what a match completes).
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .dota_api import DotaMatchData

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

# Families of checks, in location order. New checks go at the end so existing location ids don't move.
FAMILIES: dict[str, list[str]] = {
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
CHALLENGE_CHECKS = [name for names in FAMILIES.values() for name in names]

# Values players can change in their YAML: name -> (default, minimum, maximum)
VALUES: dict[str, tuple[int, int, int]] = {
    "Short Win Minutes": (30, 15, 45),
    "Long Win Minutes": (60, 40, 90),
    "Roshan Kills": (2, 1, 4),
    "Camps Stacked": (10, 1, 100),
    "Wards Placed": (15, 1, 200),
    "Building Damage": (10000, 1000, 200000),
}


def resolve_disabled(disabled: set[str]) -> set[str]:
    """Check names disabled by the YAML, families expanded."""
    return {name for key in disabled for name in FAMILIES.get(key, [key])}


def challenge_values(slot_data: dict[str, Any]) -> dict[str, int]:
    """Values for this seed: defaults, overridden by the YAML (sent in slot_data)."""
    chosen = slot_data.get("check_values") or {}
    return {name: int(chosen.get(name, default)) for name, (default, _, _) in VALUES.items()}


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
