from dataclasses import dataclass

from Options import Choice, Range, DeathLink, PerGameCommonOptions, StartInventoryPool, OptionGroup, OptionSet
from .Levels import low_victory_checks_levels, high_victory_checks_levels, final_levels

early_level_names = {level.name for level in low_victory_checks_levels}
main_level_names = {level.name for level in high_victory_checks_levels}
final_level_names = {level.name for level in final_levels}

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


class PlayerSacrificeLimit(Range):
    """How many times the player can sacrifice a unit at the Stronghold per level attempt.
    Sacrificed units are stored in the multiworld for other players to summon."""
    display_name = "Player Sacrifice Limit"
    range_start = 0
    range_end = 5
    default = 0


class PlayerSummonLimit(Range):
    """How many times the player can summon a unit at the Stronghold per level attempt.
    Summoned units are from the multiworld which were sacrificed by other players."""
    display_name = "Player Summon Limit"
    range_start = 0
    range_end = 5
    default = 0


class AISacrificeLimit(Range):
    """How many times the AI can sacrifice a unit at the Stronghold per level attempt.
    Sacrificed units are stored in the multiworld for other AIs to summon."""
    display_name = "AI Sacrifice Limit"
    range_start = 0
    range_end = 5
    default = 0


class AISummonLimit(Range):
    """How many times the AI can summon a unit at the Stronghold per level attempt.
    Summoned units are from the multiworld which were sacrificed by other AIs.
    If a level becomes impossible, use /sacrifice_summon in the client to toggle sacrifices and summons on and off."""
    display_name = "AI Summon Limit"
    range_start = 0
    range_end = 5
    default = 0


class CustomEarlyLevelPlaylist(OptionSet):
    """
    A list of levels available after the first level.
    Removing levels from this list prevents them from showing up in the game.
    If the number of levels removed is less than the available levels, then filler levels will be in their place.
    Filler levels do not contain items and automatically provide a victory.

    Format as a comma-separated list of early level names: ["Swimming at the Docks", "Floran Trap"]
    """
    display_name = "Custom early level playlist"
    default = early_level_names
    valid_keys = frozenset(early_level_names)
    valid_keys_casefold = False


class CustomMainLevelPlaylist(OptionSet):
    """
    A list of levels available after the early levels.
    Removing levels from this list prevents them from showing up in the game.
    If the number of levels removed is less than the available levels, then filler levels will be in their place.
    Filler levels do not contain items and automatically provide a victory.

    Format as a comma-separated list of main level names: ["Wagon Freeway", "Operation Seagull"]
    """
    display_name = "Custom main level playlist"
    default = main_level_names
    valid_keys = frozenset(main_level_names)
    valid_keys_casefold = False

class CustomFinalLevelPlaylist(OptionSet):
    """
    A list of final levels available.
    Removing levels from this list prevents them from showing up in the game.
    If the number of levels removed is less than the available levels, then filler levels will be in their place.
    Filler levels will automatically provide a victory.

    Format as a comma-separated list of final level names: ["Doomed Metropolis", "Dark Mirror"]
    """
    display_name = "Custom final level playlist"
    default = final_level_names
    valid_keys = frozenset(final_level_names)
    valid_keys_casefold = False

wargroove2_option_groups = [
        OptionGroup("General Options", [
            VictoryLocations,
            ObjectiveLocations,
            LevelShuffleSeed,
            CommanderChoice,
            FinalLevels,
            DeathLink
        ]),
        OptionGroup("Filler Options", [
            IncomeBoost,
            CommanderDefenseBoost,
            GrooveBoost
        ]),
        OptionGroup("Sacrifice and Summon Options", [
            PlayerSacrificeLimit,
            PlayerSummonLimit,
            AISacrificeLimit,
            AISummonLimit
        ]),
        OptionGroup("Level Playlists", [
            CustomEarlyLevelPlaylist,
            CustomMainLevelPlaylist,
            CustomFinalLevelPlaylist
        ]),
]

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
    player_sacrifice_limit: PlayerSacrificeLimit
    player_summon_limit: PlayerSummonLimit
    ai_sacrifice_limit: AISacrificeLimit
    ai_summon_limit: AISummonLimit
    custom_early_level_playlist: CustomEarlyLevelPlaylist
    custom_main_level_playlist: CustomMainLevelPlaylist
    custom_final_level_playlist: CustomFinalLevelPlaylist
    death_link: DeathLink
    start_inventory_from_pool: StartInventoryPool
