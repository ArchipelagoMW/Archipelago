from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources
from typing import Any
from Options import Choice, Range, PerGameCommonOptions, OptionSet, OptionDict

from .challenges import FAMILIES, DISABLEABLE_CHECKS, VALUES, MULTI_VALUES, MAX_THRESHOLDS
from .constants import MAX_HERO_GROUPS

class GoalType(Choice):
    """How game completion is determined.

    - **Standard:** Win with X different characters, Have Y Total wins, and Collect Z Primordial Fragments.
    """
    display_name = "Goal Type"
    option_standard = 0
    default = 0

class UniqueCharactersToWin(Range):
    """Number of unique characters you must win with to finish (1-20)."""
    display_name = "Unique Characters to Win"
    range_start = 1
    range_end = 127
    default = 5


class TotalWinsToWin(Range):
    """Number of total match wins you must achieve to finish."""
    display_name = "Total Wins to Win"
    range_start = 1
    range_end = 127
    default = 5


class PrimordialFragmentsToWin(Range):
    """Number of Primordial Fragments (MacGuffin) you must collect to finish. Will Always be 10 more in the item pool then selected."""
    display_name = "Primordial Fragments to Win"
    range_start = 10
    range_end = 50 #will always add 10 more than chosen
    default = 10

class CrownFall(Choice):
    """Adds the Crownfall minigames as locations, each minigame has it's own unlock.
    """
    display_name = "Crownfall Minigames"
    option_off = 0
    option_on = 1
    default = 0

class StartingHeroes(Range):
    """Number of heroes playable from the start."""
    display_name = "Starting Heroes"
    range_start = 5
    range_end = 120
    default = 30


class HeroGroups(Range):
    """Number of hero groups to unlock. The other heroes are split evenly between them."""
    display_name = "Hero Groups"
    range_start = 1
    range_end = MAX_HERO_GROUPS
    default = 7


class DisabledChecks(OptionSet):
    """Checks to remove: families or check names. Hero group wins and the goal always stay.
    Families: Attribute Wins, Attack Type Wins, Legs Wins, Role Wins, Purchases, Kills, Assists, Dewards, Last Hits,
    Denies, Healing, Physical Damage, Magical Damage, Physical Hit, Magical Hit, First Blood, Courier Kill, Runes,
    Buyback, Aegis, Positions, Short Win, Long Win, Roshan Win, Quests, Stack Camps, Place Wards, Damage Buildings,
    Heal Heroes"""
    display_name = "Disabled Checks"
    valid_keys = sorted(FAMILIES) + DISABLEABLE_CHECKS


class CheckValues(OptionDict):
    """Numbers used by checks. Stats count in one match, quests over the whole seed; a list gives one check per number,
    e.g. Last Hits: [300, 450]. Hits are one hit on a hero. Short Win needs no leaver or bot. Roshan Kills are your
    team's, in a win."""
    display_name = "Check Values"
    valid_keys = list(VALUES)
    default = {name: default for name, (default, _, _) in VALUES.items()}

    def __init__(self, value: dict[str, Any]) -> None:
        super().__init__(value)
        errors = []
        for key, v in self.value.items():
            if key not in VALUES:
                continue  # unknown keys are reported by the key check
            _, low, high = VALUES[key]
            many = isinstance(v, (list, tuple))
            if many and key not in MULTI_VALUES:
                errors.append(f"{key} takes a single number, got {v}.")
                continue
            numbers = list(v) if many else [v]
            if not numbers or (many and len(numbers) > MAX_THRESHOLDS):
                errors.append(f"{key} takes 1 to {MAX_THRESHOLDS} thresholds, got {len(numbers)}.")
            elif any(not isinstance(n, int) or isinstance(n, bool) for n in numbers):
                errors.append(f"{key} must be whole numbers, got {v}.")
            elif any(not low <= n <= high for n in numbers):
                errors.append(f"{key} must be between {low} and {high}, got {v}.")
            elif len(set(numbers)) != len(numbers):
                errors.append(f"{key} thresholds must be different, got {v}.")
        if errors:
            raise ValueError("\n".join([f"For option {self.__class__.__name__}:"] + errors))


# class PrimordialFragmentsToUnlockFinal(Range):
#     """Number of Primordial Fragments (MacGuffin) you must collect to unlock your final character (Win with Character goal).

#     The world caps this below the usual Primordial Fragments max by three: the final hero's three win checks require
#     this many Primordial Fragments first and may themselves contain Primordial Fragments, so the threshold must be reachable using
#     other locations only.
#     """
#     display_name = "Spirits to Unlock Final Character"
#     range_start = 1
#     range_end = 10
#     default = 5

# _FINAL_CHARACTER_NAMES: list[str] = _load_hero_names()

# def _hero_name_to_option_key(name: str) -> str:
#     return name.lower().replace(" ", "_").replace("&", "and")

# Build FinalCharacter with all option_* in the class namespace at creation time so the
# Choice metaclass (AssembleOptions) sees them and populates .options / .name_lookup.
# _final_char_attrs: dict = {
#     "__module__": __name__,
#     "display_name": "Final Character (Win With)",
#     "default": 0,
# }
# for _i, _name in enumerate(_FINAL_CHARACTER_NAMES):
#     _final_char_attrs[f"option_{_hero_name_to_option_key(_name)}"] = _i

# FinalCharacter = type("FinalCharacter", (Choice,), _final_char_attrs)


@dataclass
class DOTA2Options(PerGameCommonOptions):
    goal_type: GoalType
    unique_characters_to_win: UniqueCharactersToWin
    total_wins_to_win: TotalWinsToWin
    primordial_fragments_to_win: PrimordialFragmentsToWin
    crownfall: CrownFall
    starting_heroes: StartingHeroes
    hero_groups: HeroGroups
    disabled_checks: DisabledChecks
    check_values: CheckValues
    #primordial_fragments_to_unlock_final: PrimordialFragmentsToUnlockFinal
    #final_character: FinalCharacter
    # game_mode: GameMode
    # exclude_hard_locations: ExcludeHardLocations

