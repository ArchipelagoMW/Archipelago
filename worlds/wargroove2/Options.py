from dataclasses import dataclass

from Options import Choice, Range, DeathLink, PerGameCommonOptions, StartInventoryPool


class VictoryLocations(Range):
    """How many checks are sent per level completed."""
    display_name = "Victory Locations"
    range_start = 1
    range_end = 5
    default = 2


class ObjectiveLocations(Range):
    """How many checks are sent per side objective completed."""
    display_name = "Objective Locations"
    range_start = 1
    range_end = 5
    default = 1


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


class GrooveBoost(Range):
    """How much extra groove the player's commander gets per boost received."""
    display_name = "Groove Boost"
    range_start = 0
    range_end = 10
    default = 3


class LevelShuffleSeed(Range):
    """What seed to use for level shuffling. 0 uses the world seed."""
    display_name = "Level Shuffle Seed"
    range_start = 0
    range_end = 0xFFFFFFFF
    default = 0


class CommanderChoice(Choice):
    """How the player's commander is selected for missions.

    - Locked Random: The player's commander is randomly predetermined for each level.

    - Unlockable Factions: The player starts with Mercival and can unlock playable factions.

    - Random Starting Faction:  The player starts with a random starting faction and can unlock the rest.

    When playing with unlockable factions, faction items are added to the pool."""
    display_name = "Commander Choice"
    option_locked_random = 0
    option_unlockable_factions = 1
    option_random_starting_faction = 2


class FinalLevels(Range):
    """How many final levels to beat before victory is achieved."""
    display_name = "FinalLevels"
    range_start = 1
    range_end = 4
    default = 2


@dataclass
class Wargroove2Options(PerGameCommonOptions):
    victory_locations: VictoryLocations
    objective_locations: ObjectiveLocations
    income_boost: IncomeBoost
    commander_defense_boost: CommanderDefenseBoost
    groove_boost: GrooveBoost
    level_shuffle_seed: LevelShuffleSeed
    commander_choice: CommanderChoice
    final_levels: FinalLevels
    death_link: DeathLink
    start_inventory_from_pool: StartInventoryPool
