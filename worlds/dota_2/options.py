from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources
from Options import Choice, Range, PerGameCommonOptions, OptionSet, OptionCounter

from .challenges import FAMILIES, CHALLENGE_CHECKS, VALUES

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

class DisabledChecks(OptionSet):
    """Global checks to remove from the seed. All of them are in the seed by default.

    List families or single checks. Families: First Blood, Courier Kill, Runes, Buyback, Aegis, Positions,
    Short Win, Long Win, Roshan Win, Quests.
    Example: ["Runes", "Kill a Courier"]
    """
    display_name = "Disabled Checks"
    valid_keys = sorted(FAMILIES) + CHALLENGE_CHECKS


class CheckValues(OptionCounter):
    """Change the values used by global checks. Only list the ones you want to change.

    - Short Win Minutes (default 30, 15 to 45): win faster than this, with no leaver or bot in the match.
    - Long Win Minutes (default 60, 40 to 90): win a match lasting at least this long.
    - Roshan Kills (default 1, 1 to 4): win a match where your team killed Roshan at least this many times.
    - Camps Stacked (default 10, 1 to 100): camps to stack over the whole seed.
    - Wards Placed (default 15, 1 to 200): observer and sentry wards to place over the whole seed.
    - Building Damage (default 10000, 1000 to 200000): damage to deal to buildings over the whole seed.
    Example: {"Short Win Minutes": 25, "Wards Placed": 20}
    """
    display_name = "Check Values"
    valid_keys = list(VALUES)

    def __init__(self, value: dict[str, int]) -> None:
        super().__init__(value)
        errors = [f"{key} must be between {VALUES[key][1]} and {VALUES[key][2]}, got {v}."
                  for key, v in self.value.items() if key in VALUES and not VALUES[key][1] <= v <= VALUES[key][2]]
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
    disabled_checks: DisabledChecks
    check_values: CheckValues
    #primordial_fragments_to_unlock_final: PrimordialFragmentsToUnlockFinal
    #final_character: FinalCharacter
    # game_mode: GameMode
    # exclude_hard_locations: ExcludeHardLocations

