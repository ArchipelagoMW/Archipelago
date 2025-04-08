from dataclasses import dataclass

from Options import Choice, DeathLink, DefaultOnToggle, ExcludeLocations, NamedRange, OptionDict, \
    OptionGroup, PerGameCommonOptions, Range, Removed, Toggle

## Game Options

class EndingCondition(Choice):
    """Ending Condition"""
    display_name = "Ending Condition"  # this is the option name as it's displayed to the user on the webhost and in the spoiler log
    option_elden_beast = 0
    alias_false = 0
    option_consort = 1
    alias_true = 1

class GreatRunesRequired(Range):
    """How many great runes are required to enter leyndell"""
    display_name = "Leyndell Great Rune Required"
    range_start = 1
    range_end = 7
    default = 2


class EnableDLC(Toggle):
    """Enable DLC"""
    display_name = "Enable DLC"  # this is the option name as it's displayed to the user on the webhost and in the spoiler log

class LateDLCOption(Choice):
    """Guarantee that you don't need to enter the DLC until later in the run.

    - **Off:** You may have to enter the DLC with quest item.
    - **Medallion:** You won't have to enter the DLC until after getting Haligtree Secret Medallion and Rold Medallion.
    """
    display_name = "Late DLC"
    option_off = 0
    alias_false = 0
    option_after_medallion = 1
    alias_true = 1

## Item & Location

class RandomizeStartingLoadout(DefaultOnToggle):
    """Randomizes the equipment characters begin with."""
    display_name = "Randomize Starting Loadout"


class AutoEquipOption(Toggle):
    """Automatically equips any received armor or left/right weapons."""
    display_name = "Auto-Equip"

class ERExcludeLocations(ExcludeLocations):
    """Prevent these locations from having an important item."""
    default = frozenset({"Hidden", "Missable"})

class ExcludedLocationBehaviorOption(Choice):
    """How to choose items for excluded locations in ER.

    - **Randomize:** Progression items can be placed in excluded locations.
    - **Randomize Unimportant:** Progression items can't be placed in excluded locations.
    - **Do Not Randomize:** Excluded locations always contain the same item as in vanilla EldenRing.

    A "progression item" is anything that's required to unlock another location in some game. A
    "useful item" is something each game defines individually, usually items that are quite
    desirable but not strictly necessary.
    """
    display_name = "Excluded Locations Behavior"
    option_randomize = 0
    option_randomize_unimportant = 1
    option_do_not_randomize = 2
    default = 0

class MissableLocationBehaviorOption(Choice):
    """Which items can be placed in locations that can be permanently missed.

    - **Randomize:** Progression items can be placed in missable locations.
    - **Randomize Unimportant:** Progression items can't be placed in missable locations.
    - **Do Not Randomize:** Missable locations always contain the same item as in vanilla EldenRing.

    A "progression item" is anything that's required to unlock another location in some game. A
    "useful item" is something each game defines individually, usually items that are quite
    desirable but not strictly necessary.
    """
    display_name = "Missable Locations Behavior"
    option_randomize = 0
    option_randomize_unimportant = 1
    option_do_not_randomize = 2
    default = 1

@dataclass
class EROptions(PerGameCommonOptions):
    ending_condition: EndingCondition
    great_runes_required: GreatRunesRequired
    enable_dlc: EnableDLC
    late_dlc: LateDLCOption
    death_link: DeathLink

    random_start: RandomizeStartingLoadout
    auto_equip: AutoEquipOption

    exclude_locations: ERExcludeLocations
    excluded_location_behavior: ExcludedLocationBehaviorOption
    missable_location_behavior: MissableLocationBehaviorOption

option_groups = [
    OptionGroup("Equipment", [
        RandomizeStartingLoadout,
        AutoEquipOption,
    ]),
    OptionGroup("Item & Location Options", [
        ERExcludeLocations,
        ExcludedLocationBehaviorOption,
        MissableLocationBehaviorOption,
    ])
]
