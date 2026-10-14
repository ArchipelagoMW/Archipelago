from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources
from Options import Choice, Range, PerGameCommonOptions

class GoalType(Choice):
    """How game completion is determined.

    - **Standard:** Win with X different characters, Have Y Total wins, and Collect Z Primordial Fragments.
    - **All Heroes:**  Unique Hero wins are checks *!!!NOT YET IMPLEMENTED!!!*
    """
    display_name = "Goal Type"
    option_standard = 0
    option_all_heroes = 1
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
    #primordial_fragments_to_unlock_final: PrimordialFragmentsToUnlockFinal
    #final_character: FinalCharacter
    # game_mode: GameMode
    # exclude_hard_locations: ExcludeHardLocations

