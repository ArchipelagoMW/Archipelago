"""Checks players can turn off or tune in their YAML, and the rules deciding what a match completes.

Shared by the world (locations and options) and the client. Covers the stats, the wins by hero trait,
the purchases, and the global challenges and quests any hero can do.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .dota_api import DotaMatchData

MAX_THRESHOLDS = 5  # checks per stat or quest, one per threshold


@dataclass(frozen=True)
class Scale:
    """A stat (one match) or quest (whole seed) with thresholds on a grid, each grid value a location declared up front."""
    value: str  # key in check_values
    field: str  # DotaMatchData field, also the quest total key
    pattern: str  # location name, {} being the threshold
    default: tuple[int, ...]
    low: int
    high: int
    step: int

    def name(self, threshold: int) -> str:
        return self.pattern.replace("{}", str(threshold))

    @property
    def grid(self) -> list[int]:
        return list(range(self.low, self.high + 1, self.step))

    @property
    def names(self) -> list[str]:
        return [self.name(t) for t in self.grid]


# Stats, in one match. Defaults are round numbers a bit above what a player in the most favourable position reaches
# one match in four (OpenDota public matches). The first five keep the original apworld's location names.
STATS = [
    Scale("Kills", "kills", "Get {} Kill(s)", (15,), 1, 50, 1),
    Scale("Assists", "assists", "Get {} Assists", (30,), 1, 60, 1),
    Scale("Dewards", "dewards", "Get {} Deward(s)", (5,), 1, 30, 1),
    Scale("Last Hits", "last_hits", "Get {} Last Hits", (450,), 25, 800, 25),
    Scale("Denies", "denies", "Get {} Denies", (20,), 1, 60, 1),
    Scale("Healing", "healing", "Heal {} in a Match", (2000,), 500, 20000, 500),
    Scale("Physical Damage", "physical_damage", "Deal {} Physical Damage in a Match", (25000,), 2500, 75000, 2500),
    Scale("Magical Damage", "magical_damage", "Deal {} Magical Damage in a Match", (20000,), 2500, 75000, 2500),
    Scale("Physical Hit", "physical_hit", "Land a {} Physical Hit", (500,), 100, 3000, 100),
    Scale("Magical Hit", "magical_hit", "Land a {} Magical Hit", (500,), 100, 3000, 100),
    Scale("Stun Time", "stun_time", "Stun Enemies for {}s in a Match", (60,), 10, 300, 10),  # seconds
    Scale("Camps Stacked", "camps_stacked", "Stack {} Camps in a Match", (5,), 5, 30, 5),
]

# Quests add up over the whole seed, with a lower and a full target by default (about ten matches in the most
# favourable position for the full one).
QUESTS = [
    Scale("Total Camps Stacked", "camps_stacked", "Stack {} Camps in Total", (10, 20), 5, 100, 5),
    Scale("Total Wards Placed", "wards_placed", "Place {} Wards in Total", (50, 100), 10, 300, 10),
    Scale("Total Building Damage", "building_damage", "Deal {} Building Damage in Total", (25000, 50000), 5000, 200000, 5000),
    Scale("Total Healing", "healing", "Heal {} in Total", (7500, 15000), 2500, 100000, 2500),
    Scale("Total Physical Damage", "physical_damage", "Deal {} Physical Damage in Total", (75000, 150000), 25000, 500000, 25000),
    Scale("Total Magical Damage", "magical_damage", "Deal {} Magical Damage in Total", (60000, 120000), 20000, 500000, 20000),
    Scale("Total Stun Time", "stun_time", "Stun Enemies for {}s in Total", (200, 400), 50, 1000, 50),
    Scale("Total Runes", "rune_pickups", "Pick up {} Runes in Total", (20, 50), 10, 100, 5),  # Shrines of Wisdom not counted
]
SCALES = {s.value: s for s in STATS + QUESTS}

# OpenDota rune keys are the game's DOTA_RUNE values. Wisdom runes became Shrines of Wisdom in 7.38, still reported as key 8.
WISDOM = "8"
RUNES = {
    "0": "Double Damage", "1": "Haste", "2": "Illusion", "3": "Invisibility", "4": "Regeneration",
    "5": "Bounty", "6": "Arcane", "7": "Water", "8": "Wisdom", "9": "Shield",
}


def rune_check(rune: str) -> str:
    if rune == RUNES[WISDOM]:
        return "Use a Shrine of Wisdom"
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
CHALLENGE_CHECKS = [name for names in CHALLENGE_FAMILIES.values() for name in names]


def _purchase_checks() -> list[str]:
    with resources.files(__package__).joinpath("data/dotaShopLocations.json").open("r", encoding="utf-8") as f:
        return [item["dname"] for item in json.load(f).values() if item.get("dname")]


# Families a YAML can turn off. Hero group wins and the goal stay, since the seed's progression relies on them.
# A stat or quest is turned off as a whole: which of its names are in the seed comes from check_values.
FAMILIES: dict[str, list[str]] = {
    "Attribute Wins": ["Win as a Strength Hero", "Win as a Agility Hero", "Win as a Intelligence Hero", "Win as a Universal Hero"],
    "Attack Type Wins": ["Win as a Melee Hero", "Win as a Ranged Hero"],
    "Legs Wins": ["Win as a 0 Legged Hero", "Win as a 2 Legged Hero", "Win as a 4+ Legged Hero"],
    "Role Wins": ["Win as a Carry Hero", "Win as a Support Hero"],
    **{s.value: s.names for s in STATS},
    "Purchases": _purchase_checks(),
    **CHALLENGE_FAMILIES,
    **{s.value: s.names for s in QUESTS},
    "Quests": [name for s in QUESTS for name in s.names],
}
SCALE_NAMES = {name for s in SCALES.values() for name in s.names}
DISABLEABLE_CHECKS = sorted({name for names in FAMILIES.values() for name in names} - SCALE_NAMES)

# Values players can change in their YAML: name -> (default, minimum, maximum). Stats and quests take one threshold
# or a list of up to MAX_THRESHOLDS thresholds on their grid (one check each).
VALUES: dict[str, tuple[Any, int, int]] = {
    **{s.value: (list(s.default) if len(s.default) > 1 else s.default[0], s.low, s.high) for s in STATS},
    "Short Win Minutes": (30, 15, 40),  # at most Long Win Minutes' minimum
    "Long Win Minutes": (60, 40, 90),
    "Roshan Kills": (1, 1, 4),
    **{s.value: (list(s.default), s.low, s.high) for s in QUESTS},
}


def resolve_disabled(disabled: set[str]) -> set[str]:
    """Check names disabled by the YAML, families expanded."""
    return {name for key in disabled for name in FAMILIES.get(key, [key])}


def thresholds(value: int | list[int]) -> list[int]:
    return sorted({int(v) for v in value}) if isinstance(value, (list, tuple, set)) else [int(value)]


def resolve_values(chosen: dict[str, Any]) -> dict[str, Any]:
    """Defaults, overridden by what the YAML sets. Stats and quests become sorted lists of thresholds."""
    return {name: thresholds(chosen.get(name, default)) if name in SCALES else int(chosen.get(name, default))
            for name, (default, _, _) in VALUES.items()}


def scale_checks_in_seed(values: dict[str, Any]) -> set[str]:
    """Names of the stat and quest checks this seed's thresholds pick."""
    return {s.name(t) for key, s in SCALES.items() for t in values[key]}


def challenge_values(slot_data: dict[str, Any], seed_checks: set[str] | None = None) -> dict[str, Any]:
    """Values for this seed from slot_data. Given the seed's check names, thresholds come from them instead, which
    also covers seeds from the original apworld (no check_values)."""
    values = resolve_values(slot_data.get("check_values") or {})
    if seed_checks is not None:
        values.update({key: [t for t in s.grid if s.name(t) in seed_checks] for key, s in SCALES.items()})
    return values


def stat_checks(m: DotaMatchData, values: dict[str, Any]) -> list[str]:
    """Stat thresholds reached in a match."""
    return [s.name(t) for s in STATS for t in values[s.value] if getattr(m, s.field) >= t]


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
    return {s.field: getattr(m, s.field) for s in QUESTS}


def completed_quests(totals: dict[str, int], values: dict[str, Any]) -> list[str]:
    return [s.name(t) for s in QUESTS for t in values[s.value] if totals.get(s.field, 0) >= t]
