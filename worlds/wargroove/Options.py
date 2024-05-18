import typing
from dataclasses import dataclass
from Options import Choice, Option, Range, PerGameCommonOptions


class IncomeBoost(Range):
    """How much extra income the player gets per turn per boost received."""
    display_name = "Income Boost"
    range_start = 0
    range_end = 100
    default = 25


class CommanderDefenseBoost(Range):
    """How much extra defense the player's commander gets per boost received."""
    display_name = "Commander Defense Boost"
    range_start = 0
    range_end = 8
    default = 2


class CommanderChoice(Choice):
    """How the player's commander is selected for missions.
    Locked Random: The player's commander is randomly predetermined for each level.
    Unlockable Factions: The player starts with Mercival and can unlock playable factions.
    Random Starting Faction:  The player starts with a random starting faction and can unlock the rest.
    When playing with unlockable factions, faction items are added to the pool.
    Extra faction items after the first also reward starting Groove charge."""
    display_name = "Commander Choice"
    option_locked_random = 0
    option_unlockable_factions = 1
    option_random_starting_faction = 2

@dataclass
class WargrooveOptions(PerGameCommonOptions):
    income_boost: IncomeBoost
    commander_defense_boost: CommanderDefenseBoost
    commander_choice: CommanderChoice
