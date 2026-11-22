from __future__ import annotations

import json
import textwrap
from dataclasses import dataclass
from importlib import resources
from typing import Any
from Options import Choice, Range, PerGameCommonOptions, OptionSet, OptionDict

from .challenges import FAMILIES, DISABLEABLE_CHECKS, VALUES, SCALES, MAX_THRESHOLDS
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
    """Checks to remove: families or check names. Hero group wins and the goal always stay."""
    display_name = "Disabled Checks"
    valid_keys = sorted(FAMILIES) + DISABLEABLE_CHECKS


DisabledChecks.__doc__ += "\n" + textwrap.fill("Families: " + ", ".join(FAMILIES), 116)


class CheckValues(OptionDict):
    """Numbers used by checks: stats in one match, quests over the seed. A list gives one check per number on the
    stat's grid, e.g. Last Hits: [300, 450]. Stun times are in seconds. Short Win needs no leaver or bot; Roshan Kills are your team's."""
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
            if many and key not in SCALES:
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
            elif key in SCALES and any((n - low) % SCALES[key].step for n in numbers):
                errors.append(f"{key} goes by steps of {SCALES[key].step} from {low}, got {v}.")
        if errors:
            raise ValueError("\n".join([f"For option {self.__class__.__name__}:"] + errors))



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


