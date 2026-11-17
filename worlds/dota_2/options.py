from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources
from Options import Choice, Range, PerGameCommonOptions, OptionSet, OptionCounter

from .challenges import FAMILIES, DISABLEABLE_CHECKS, VALUES, STATS, stat_check, resolve_values
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
    """Number of heroes you can play from the start. The other heroes are split into groups to unlock."""
    display_name = "Starting Heroes"
    range_start = 5
    range_end = 120
    default = 30


class HeroGroups(Range):
    """Number of hero groups to unlock, each with a "Progressive Group Unlock". The heroes left after the starting
    pool are split evenly between them. There can't be more groups than heroes left."""
    display_name = "Hero Groups"
    range_start = 1
    range_end = MAX_HERO_GROUPS
    default = 7


class DisabledChecks(OptionSet):
    """Checks to remove from the seed. All checks are in the seed by default.

    List families or single checks (by their name). Wins with a hero group and the goal can't be removed.
    Families: Attribute Wins, Attack Type Wins, Legs Wins, Role Wins, Kills, Assists, Dewards, Last Hits,
    Denies, Purchases, First Blood, Courier Kill, Runes, Buyback, Aegis, Positions, Short Win, Long Win,
    Roshan Win, Quests.
    Example: ["Runes", "Legs Wins", "Divine Rapier"]
    """
    display_name = "Disabled Checks"
    valid_keys = sorted(FAMILIES) + DISABLEABLE_CHECKS


class CheckValues(OptionCounter):
    """Change the values checks use. Only list the ones you want to change.

    Stat tiers, in one match (each tier must be at least the one before):
    - Kills Tier 1 / 2 / 3 (default 1 / 5 / 10, up to 50)
    - Assists Tier 1 / 2 / 3 (default 5 / 10 / 20, up to 60)
    - Dewards Tier 1 / 2 / 3 (default 1 / 3 / 7, up to 30)
    - Last Hits Tier 1 / 2 / 3 (default 75 / 125 / 175, up to 800)
    - Denies Tier 1 / 2 / 3 (default 8 / 16 / 32, up to 100)
    Global challenges:
    - Short Win Minutes (default 30, 15 to 45): win faster than this, with no leaver or bot in the match.
    - Long Win Minutes (default 60, 40 to 90): win a match lasting at least this long.
    - Roshan Kills (default 1, 1 to 4): win a match where your team killed Roshan at least this many times.
    Quests, over the whole seed:
    - Camps Stacked (default 10, 1 to 100)
    - Wards Placed (default 15, 1 to 200): observer and sentry wards.
    - Building Damage (default 10000, 1000 to 200000)
    Example: {"Kills Tier 3": 15, "Short Win Minutes": 25, "Wards Placed": 20}
    """
    display_name = "Check Values"
    valid_keys = list(VALUES)

    def __init__(self, value: dict[str, int]) -> None:
        super().__init__(value)
        errors = [f"{key} must be between {VALUES[key][1]} and {VALUES[key][2]}, got {v}."
                  for key, v in self.value.items() if key in VALUES and not VALUES[key][1] <= v <= VALUES[key][2]]
        values = resolve_values(self.value)
        for label, _, _, _ in STATS:
            tiers = [values[stat_check(label, t)] for t in (1, 2, 3)]
            if tiers != sorted(tiers):
                errors.append(f"{label} tiers must go up: got {' / '.join(map(str, tiers))}.")
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

