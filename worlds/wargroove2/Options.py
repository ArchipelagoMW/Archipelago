from dataclasses import dataclass

from Options import Choice, Range, DeathLink, PerGameCommonOptions, StartInventoryPool, OptionGroup, OptionSet, \
    DeathLinkMixin
from .Levels import low_victory_checks_levels, high_victory_checks_levels, final_levels
from .Items import faction_table

early_level_names = {level.name for level in low_victory_checks_levels}
main_level_names = {level.name for level in high_victory_checks_levels}
final_level_names = {level.name for level in final_levels}
commander_names = {commander_data.name
                   for commander_data_list in faction_table.values()
                   for commander_data in commander_data_list }

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

class EnabledCommanders(OptionSet):
    """
    The commanders available to the player and the AI.
    If no commanders are enabled, Mercival will be the only available commander.

    Format as a comma-separated list of commander names: ["Mercia", "Valder"]
    """
    display_name = "Enabled Commanders"
    default = commander_names
    valid_keys = frozenset(commander_names)
    valid_keys_casefold = False


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


class PlayerBarracksEarlySphereCost(Range):
    """The cost multiplier of units purchased from the player's barracks in earlier spheres.
    The map's victory item determines the sphere number.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "Player Barracks Early Sphere Cost"
    range_start = 50
    range_end = 150
    default = 100


class PlayerBarracksLateSphereCost(Range):
    """The cost multiplier of units purchased from the player's barracks in later spheres.
    The map's victory item determines the sphere number.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "Player Barracks Late Sphere Cost"
    range_start = 50
    range_end = 150
    default = 100


class PlayerBarracksEarlyDistanceCost(Range):
    """The cost multiplier of units purchased from the player's barracks closer to the center.
    North levels will have a closer distance, then East levels, then South levels and
    West levels will have the farthest. North 2A will have a further distance than West 1.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "Player Barracks Early Distance Cost"
    range_start = 50
    range_end = 150
    default = 100


class PlayerBarracksLateDistanceCost(Range):
    """The cost multiplier of units purchased from the player's barracks farther from the center.
    North levels will have a closer distance, then East levels, then South levels and
    West levels will have the farthest. North 2A will have a further distance than West 1.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "Player Barracks Late Distance Cost"
    range_start = 50
    range_end = 150
    default = 100


class PlayerBarracksRandomLowCost(Range):
    """The cost multiplier of units purchased from the player's barracks determined at random.
    This multiplier will be the lowest random multiplier.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "Player Barracks Random Low Cost"
    range_start = 50
    range_end = 150
    default = 100


class PlayerBarracksRandomHighCost(Range):
    """The cost multiplier of units purchased from the player's barracks determined at random.
    This multiplier will be the highest random multiplier.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "Player Barracks Random High Cost"
    range_start = 50
    range_end = 150
    default = 100


class AIBarracksEarlySphereCost(Range):
    """The cost multiplier of units purchased from the AI's barracks in earlier spheres.
    The map's victory item determines the sphere number.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "AI Barracks Early Sphere Cost"
    range_start = 50
    range_end = 150
    default = 100


class AIBarracksLateSphereCost(Range):
    """The cost multiplier of units purchased from the AI's barracks in later spheres.
    The map's victory item determines the sphere number.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "AI Barracks Late Sphere Cost"
    range_start = 50
    range_end = 150
    default = 100


class AIBarracksEarlyDistanceCost(Range):
    """The cost multiplier of units purchased from the AI's barracks closer to the center.
    North levels will have a closer distance, then East levels, then South levels and
    West levels will have the farthest. North 2A will have a further distance than West 1.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "AI Barracks Early Distance Cost"
    range_start = 50
    range_end = 150
    default = 100


class AIBarracksLateDistanceCost(Range):
    """The cost multiplier of units purchased from the AI's barracks farther from the center.
    North levels will have a closer distance, then East levels, then South levels and
    West levels will have the farthest. North 2A will have a further distance than West 1.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "AI Barracks Late Distance Cost"
    range_start = 50
    range_end = 150
    default = 100


class AIBarracksRandomLowCost(Range):
    """The cost multiplier of units purchased from the AI's barracks determined at random.
    This multiplier will be the lowest random multiplier.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "AI Barracks Random Low Cost"
    range_start = 50
    range_end = 150
    default = 100


class AIBarracksRandomHighCost(Range):
    """The cost multiplier of units purchased from the AI's barracks determined at random.
    This multiplier will be the highest random multiplier.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "AI Barracks Random High Cost"
    range_start = 50
    range_end = 150
    default = 100


class PlayerTowerEarlySphereCost(Range):
    """The cost multiplier of units purchased from the player's tower in earlier spheres.
    The map's victory item determines the sphere number.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "Player Tower Early Sphere Cost"
    range_start = 50
    range_end = 150
    default = 100


class PlayerTowerLateSphereCost(Range):
    """The cost multiplier of units purchased from the player's tower in later spheres.
    The map's victory item determines the sphere number.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "Player Tower Late Sphere Cost"
    range_start = 50
    range_end = 150
    default = 100


class PlayerTowerEarlyDistanceCost(Range):
    """The cost multiplier of units purchased from the player's tower closer to the center.
    North levels will have a closer distance, then East levels, then South levels and
    West levels will have the farthest. North 2A will have a further distance than West 1.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "Player Tower Early Distance Cost"
    range_start = 50
    range_end = 150
    default = 100


class PlayerTowerLateDistanceCost(Range):
    """The cost multiplier of units purchased from the player's tower farther from the center.
    North levels will have a closer distance, then East levels, then South levels and
    West levels will have the farthest. North 2A will have a further distance than West 1.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "Player Tower Late Distance Cost"
    range_start = 50
    range_end = 150
    default = 100


class PlayerTowerRandomLowCost(Range):
    """The cost multiplier of units purchased from the player's tower determined at random.
    This multiplier will be the lowest random multiplier.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "Player Tower Random Low Cost"
    range_start = 50
    range_end = 150
    default = 100


class PlayerTowerRandomHighCost(Range):
    """The cost multiplier of units purchased from the player's tower determined at random.
    This multiplier will be the highest random multiplier.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "Player Tower Random High Cost"
    range_start = 50
    range_end = 150
    default = 100


class AITowerEarlySphereCost(Range):
    """The cost multiplier of units purchased from the AI's tower in earlier spheres.
    The map's victory item determines the sphere number.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "AI Tower Early Sphere Cost"
    range_start = 50
    range_end = 150
    default = 100


class AITowerLateSphereCost(Range):
    """The cost multiplier of units purchased from the AI's tower in later spheres.
    The map's victory item determines the sphere number.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "AI Tower Late Sphere Cost"
    range_start = 50
    range_end = 150
    default = 100


class AITowerEarlyDistanceCost(Range):
    """The cost multiplier of units purchased from the AI's tower closer to the center.
    North levels will have a closer distance, then East levels, then South levels and
    West levels will have the farthest. North 2A will have a further distance than West 1.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "AI Tower Early Distance Cost"
    range_start = 50
    range_end = 150
    default = 100


class AITowerLateDistanceCost(Range):
    """The cost multiplier of units purchased from the AI's tower farther from the center.
    North levels will have a closer distance, then East levels, then South levels and
    West levels will have the farthest. North 2A will have a further distance than West 1.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "AI Tower Late Distance Cost"
    range_start = 50
    range_end = 150
    default = 100


class AITowerRandomLowCost(Range):
    """The cost multiplier of units purchased from the AI's tower determined at random.
    This multiplier will be the lowest random multiplier.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "AI Tower Random Low Cost"
    range_start = 50
    range_end = 150
    default = 100


class AITowerRandomHighCost(Range):
    """The cost multiplier of units purchased from the AI's tower determined at random.
    This multiplier will be the highest random multiplier.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "AI Tower Random High Cost"
    range_start = 50
    range_end = 150
    default = 100


class PlayerHideoutEarlySphereCost(Range):
    """The cost multiplier of units purchased from the player's hideout in earlier spheres.
    The map's victory item determines the sphere number.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "Player Hideout Early Sphere Cost"
    range_start = 50
    range_end = 150
    default = 100


class PlayerHideoutLateSphereCost(Range):
    """The cost multiplier of units purchased from the player's hideout in later spheres.
    The map's victory item determines the sphere number.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "Player Hideout Late Sphere Cost"
    range_start = 50
    range_end = 150
    default = 100


class PlayerHideoutEarlyDistanceCost(Range):
    """The cost multiplier of units purchased from the player's hideout closer to the center.
    North levels will have a closer distance, then East levels, then South levels and
    West levels will have the farthest. North 2A will have a further distance than West 1.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "Player Hideout Early Distance Cost"
    range_start = 50
    range_end = 150
    default = 100


class PlayerHideoutLateDistanceCost(Range):
    """The cost multiplier of units purchased from the player's hideout farther from the center.
    North levels will have a closer distance, then East levels, then South levels and
    West levels will have the farthest. North 2A will have a further distance than West 1.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "Player Hideout Late Distance Cost"
    range_start = 50
    range_end = 150
    default = 100


class PlayerHideoutRandomLowCost(Range):
    """The cost multiplier of units purchased from the player's hideout determined at random.
    This multiplier will be the lowest random multiplier.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "Player Hideout Random Low Cost"
    range_start = 50
    range_end = 150
    default = 100


class PlayerHideoutRandomHighCost(Range):
    """The cost multiplier of units purchased from the player's hideout determined at random.
    This multiplier will be the highest random multiplier.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "Player Hideout Random High Cost"
    range_start = 50
    range_end = 150
    default = 100


class AIHideoutEarlySphereCost(Range):
    """The cost multiplier of units purchased from the AI's hideout in earlier spheres.
    The map's victory item determines the sphere number.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "AI Hideout Early Sphere Cost"
    range_start = 50
    range_end = 150
    default = 100


class AIHideoutLateSphereCost(Range):
    """The cost multiplier of units purchased from the AI's hideout in later spheres.
    The map's victory item determines the sphere number.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "AI Hideout Late Sphere Cost"
    range_start = 50
    range_end = 150
    default = 100


class AIHideoutEarlyDistanceCost(Range):
    """The cost multiplier of units purchased from the AI's hideout closer to the center.
    North levels will have a closer distance, then East levels, then South levels and
    West levels will have the farthest. North 2A will have a further distance than West 1.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "AI Hideout Early Distance Cost"
    range_start = 50
    range_end = 150
    default = 100


class AIHideoutLateDistanceCost(Range):
    """The cost multiplier of units purchased from the AI's hideout farther from the center.
    North levels will have a closer distance, then East levels, then South levels and
    West levels will have the farthest. North 2A will have a further distance than West 1.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "AI Hideout Late Distance Cost"
    range_start = 50
    range_end = 150
    default = 100


class AIHideoutRandomLowCost(Range):
    """The cost multiplier of units purchased from the AI's hideout determined at random.
    This multiplier will be the lowest random multiplier.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "AI Hideout Random Low Cost"
    range_start = 50
    range_end = 150
    default = 100


class AIHideoutRandomHighCost(Range):
    """The cost multiplier of units purchased from the AI's hideout determined at random.
    This multiplier will be the highest random multiplier.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "AI Hideout Random High Cost"
    range_start = 50
    range_end = 150
    default = 100


class PlayerPortEarlySphereCost(Range):
    """The cost multiplier of units purchased from the player's port in earlier spheres.
    The map's victory item determines the sphere number.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "Player Port Early Sphere Cost"
    range_start = 50
    range_end = 150
    default = 100


class PlayerPortLateSphereCost(Range):
    """The cost multiplier of units purchased from the player's port in later spheres.
    The map's victory item determines the sphere number.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "Player Port Late Sphere Cost"
    range_start = 50
    range_end = 150
    default = 100


class PlayerPortEarlyDistanceCost(Range):
    """The cost multiplier of units purchased from the player's port closer to the center.
    North levels will have a closer distance, then East levels, then South levels and
    West levels will have the farthest. North 2A will have a further distance than West 1.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "Player Port Early Distance Cost"
    range_start = 50
    range_end = 150
    default = 100


class PlayerPortLateDistanceCost(Range):
    """The cost multiplier of units purchased from the player's port farther from the center.
    North levels will have a closer distance, then East levels, then South levels and
    West levels will have the farthest. North 2A will have a further distance than West 1.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "Player Port Late Distance Cost"
    range_start = 50
    range_end = 150
    default = 100


class PlayerPortRandomLowCost(Range):
    """The cost multiplier of units purchased from the player's port determined at random.
    This multiplier will be the lowest random multiplier.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "Player Port Random Low Cost"
    range_start = 50
    range_end = 150
    default = 100


class PlayerPortRandomHighCost(Range):
    """The cost multiplier of units purchased from the player's port determined at random.
    This multiplier will be the highest random multiplier.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "Player Port Random High Cost"
    range_start = 50
    range_end = 150
    default = 100


class AIPortEarlySphereCost(Range):
    """The cost multiplier of units purchased from the AI's port in earlier spheres.
    The map's victory item determines the sphere number.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "AI Port Early Sphere Cost"
    range_start = 50
    range_end = 150
    default = 100


class AIPortLateSphereCost(Range):
    """The cost multiplier of units purchased from the AI's port in later spheres.
    The map's victory item determines the sphere number.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "AI Port Late Sphere Cost"
    range_start = 50
    range_end = 150
    default = 100


class AIPortEarlyDistanceCost(Range):
    """The cost multiplier of units purchased from the AI's port closer to the center.
    North levels will have a closer distance, then East levels, then South levels and
    West levels will have the farthest. North 2A will have a further distance than West 1.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "AI Port Early Distance Cost"
    range_start = 50
    range_end = 150
    default = 100


class AIPortLateDistanceCost(Range):
    """The cost multiplier of units purchased from the AI's port farther from the center.
    North levels will have a closer distance, then East levels, then South levels and
    West levels will have the farthest. North 2A will have a further distance than West 1.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "AI Port Late Distance Cost"
    range_start = 50
    range_end = 150
    default = 100


class AIPortRandomLowCost(Range):
    """The cost multiplier of units purchased from the AI's port determined at random.
    This multiplier will be the lowest random multiplier.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "AI Port Random Low Cost"
    range_start = 50
    range_end = 150
    default = 100


class AIPortRandomHighCost(Range):
    """The cost multiplier of units purchased from the AI's port determined at random.
    This multiplier will be the highest random multiplier.
    If a level becomes impossible, use /toggle_costs in the client to toggle dynamic unit costs on and off."""
    display_name = "AI Port Random High Cost"
    range_start = 50
    range_end = 150
    default = 100
    

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
            EnabledCommanders,
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
        OptionGroup("Dynamic Unit Cost Options", [
            PlayerBarracksEarlySphereCost,
            PlayerBarracksLateSphereCost,
            PlayerBarracksEarlyDistanceCost,
            PlayerBarracksLateDistanceCost,
            PlayerBarracksRandomLowCost,
            PlayerBarracksRandomHighCost,
            PlayerTowerEarlySphereCost,
            PlayerTowerLateSphereCost,
            PlayerTowerEarlyDistanceCost,
            PlayerTowerLateDistanceCost,
            PlayerTowerRandomLowCost,
            PlayerTowerRandomHighCost,
            PlayerHideoutEarlySphereCost,
            PlayerHideoutLateSphereCost,
            PlayerHideoutEarlyDistanceCost,
            PlayerHideoutLateDistanceCost,
            PlayerHideoutRandomLowCost,
            PlayerHideoutRandomHighCost,
            PlayerPortEarlySphereCost,
            PlayerPortLateSphereCost,
            PlayerPortEarlyDistanceCost,
            PlayerPortLateDistanceCost,
            PlayerPortRandomLowCost,
            PlayerPortRandomHighCost,
            AIBarracksEarlySphereCost,
            AIBarracksLateSphereCost,
            AIBarracksEarlyDistanceCost,
            AIBarracksLateDistanceCost,
            AIBarracksRandomLowCost,
            AIBarracksRandomHighCost,
            AITowerEarlySphereCost,
            AITowerLateSphereCost,
            AITowerEarlyDistanceCost,
            AITowerLateDistanceCost,
            AITowerRandomLowCost,
            AITowerRandomHighCost,
            AIHideoutEarlySphereCost,
            AIHideoutLateSphereCost,
            AIHideoutEarlyDistanceCost,
            AIHideoutLateDistanceCost,
            AIHideoutRandomLowCost,
            AIHideoutRandomHighCost,
            AIPortEarlySphereCost,
            AIPortLateSphereCost,
            AIPortEarlyDistanceCost,
            AIPortLateDistanceCost,
            AIPortRandomLowCost,
            AIPortRandomHighCost
        ]),
        OptionGroup("Level Playlists", [
            CustomEarlyLevelPlaylist,
            CustomMainLevelPlaylist,
            CustomFinalLevelPlaylist
        ]),
]

@dataclass
class Wargroove2Options(DeathLinkMixin, PerGameCommonOptions):
    victory_locations: VictoryLocations
    objective_locations: ObjectiveLocations
    income_boost: IncomeBoost
    commander_defense_boost: CommanderDefenseBoost
    groove_boost: GrooveBoost
    level_shuffle_seed: LevelShuffleSeed
    commander_choice: CommanderChoice
    enabled_commanders: EnabledCommanders
    final_levels: FinalLevels
    player_sacrifice_limit: PlayerSacrificeLimit
    player_summon_limit: PlayerSummonLimit
    ai_sacrifice_limit: AISacrificeLimit
    ai_summon_limit: AISummonLimit
    player_barracks_early_sphere: PlayerBarracksEarlySphereCost
    player_barracks_late_sphere: PlayerBarracksLateSphereCost
    player_barracks_early_distance: PlayerBarracksEarlyDistanceCost
    player_barracks_late_distance: PlayerBarracksLateDistanceCost
    player_barracks_random_low_cost: PlayerBarracksRandomLowCost
    player_barracks_random_high_cost: PlayerBarracksRandomHighCost
    player_tower_early_sphere: PlayerTowerEarlySphereCost
    player_tower_late_sphere: PlayerTowerLateSphereCost
    player_tower_early_distance: PlayerTowerEarlyDistanceCost
    player_tower_late_distance: PlayerTowerLateDistanceCost
    player_tower_random_low_cost: PlayerTowerRandomLowCost
    player_tower_random_high_cost: PlayerTowerRandomHighCost
    player_hideout_early_sphere: PlayerHideoutEarlySphereCost
    player_hideout_late_sphere: PlayerHideoutLateSphereCost
    player_hideout_early_distance: PlayerHideoutEarlyDistanceCost
    player_hideout_late_distance: PlayerHideoutLateDistanceCost
    player_hideout_random_low_cost: PlayerHideoutRandomLowCost
    player_hideout_random_high_cost: PlayerHideoutRandomHighCost
    player_port_early_sphere: PlayerPortEarlySphereCost
    player_port_late_sphere: PlayerPortLateSphereCost
    player_port_early_distance: PlayerPortEarlyDistanceCost
    player_port_late_distance: PlayerPortLateDistanceCost
    player_port_random_low_cost: PlayerPortRandomLowCost
    player_port_random_high_cost: PlayerPortRandomHighCost
    ai_barracks_early_sphere: AIBarracksEarlySphereCost
    ai_barracks_late_sphere: AIBarracksLateSphereCost
    ai_barracks_early_distance: AIBarracksEarlyDistanceCost
    ai_barracks_late_distance: AIBarracksLateDistanceCost
    ai_barracks_random_low_cost: AIBarracksRandomLowCost
    ai_barracks_random_high_cost: AIBarracksRandomHighCost
    ai_tower_early_sphere: AITowerEarlySphereCost
    ai_tower_late_sphere: AITowerLateSphereCost
    ai_tower_early_distance: AITowerEarlyDistanceCost
    ai_tower_late_distance: AITowerLateDistanceCost
    ai_tower_random_low_cost: AITowerRandomLowCost
    ai_tower_random_high_cost: AITowerRandomHighCost
    ai_hideout_early_sphere: AIHideoutEarlySphereCost
    ai_hideout_late_sphere: AIHideoutLateSphereCost
    ai_hideout_early_distance: AIHideoutEarlyDistanceCost
    ai_hideout_late_distance: AIHideoutLateDistanceCost
    ai_hideout_random_low_cost: AIHideoutRandomLowCost
    ai_hideout_random_high_cost: AIHideoutRandomHighCost
    ai_port_early_sphere: AIPortEarlySphereCost
    ai_port_late_sphere: AIPortLateSphereCost
    ai_port_early_distance: AIPortEarlyDistanceCost
    ai_port_late_distance: AIPortLateDistanceCost
    ai_port_random_low_cost: AIPortRandomLowCost
    ai_port_random_high_cost: AIPortRandomHighCost
    custom_early_level_playlist: CustomEarlyLevelPlaylist
    custom_main_level_playlist: CustomMainLevelPlaylist
    custom_final_level_playlist: CustomFinalLevelPlaylist
    start_inventory_from_pool: StartInventoryPool
