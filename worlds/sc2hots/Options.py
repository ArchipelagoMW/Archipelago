from typing import Dict, FrozenSet, Union
from BaseClasses import MultiWorld
from Options import Choice, Option, Toggle, DefaultOnToggle, ItemSet, OptionSet, Range
from .MissionTables import vanilla_mission_req_table


class GameDifficulty(Choice):
    """The difficulty of the campaign, affects enemy AI, starting units, and game speed."""
    display_name = "Game Difficulty"
    option_casual = 0
    option_normal = 1
    option_hard = 2
    option_brutal = 3


class MissionOrder(Choice):
    """Determines the order the missions are played in.  The last three mission orders end in a random mission.
    Vanilla (20): Keeps the standard mission order and branching from the HotS Campaign.
    Vanilla Shuffled (20): Keeps same branching paths from the HotS Campaign but randomizes the order of missions within.
    Mini Campaign (13): Shorter version of the campaign with randomized missions and optional branches.
    Grid (16):  A 4x4 grid of random missions.  Start at the top-left and forge a path towards The Reckoning.
    Mini Grid (9):  A 3x3 version of Grid.  Complete the bottom-right mission to win.
    Blitz (12):  12 random missions that open up very quickly.  Complete the bottom-right mission to win.
    Gauntlet (7): Linear series of 7 random missions to complete the campaign."""
    display_name = "Mission Order"
    option_vanilla = 0
    option_vanilla_shuffled = 1
    option_mini_campaign = 2
    option_grid = 3
    option_mini_grid = 4
    option_blitz = 5
    option_gauntlet = 6


class PlayerColor(Choice):
    """Determines in-game team color before Kerrigan becomes Primal Kerrigan."""
    display_name = "Player Color"
    option_white = 0
    option_red = 1
    option_blue = 2
    option_teal = 3
    option_purple = 4
    option_yellow = 5
    option_orange = 6
    option_green = 7
    option_light_pink = 8
    option_violet = 9
    option_light_grey = 10
    option_dark_green = 11
    option_brown = 12
    option_light_green = 13
    option_dark_grey = 14
    option_pink = 15
    option_rainbow = 16
    default = option_orange


class PlayerColorPrimal(Choice):
    """Determines in-game team color when Kerrigan becomes Primal Kerrigan."""
    display_name = "Player Color (Primal)"
    option_white = 0
    option_red = 1
    option_blue = 2
    option_teal = 3
    option_purple = 4
    option_yellow = 5
    option_orange = 6
    option_green = 7
    option_light_pink = 8
    option_violet = 9
    option_light_grey = 10
    option_dark_green = 11
    option_brown = 12
    option_light_green = 13
    option_dark_grey = 14
    option_pink = 15
    option_rainbow = 16
    default = option_purple

class ShuffleNoBuild(DefaultOnToggle):
    """Determines if the 5 no-build missions are included in the shuffle if Vanilla or Vanilla Shuffled mission order is not enabled.
    If turned off with reduced mission settings, the 5 no-build missions will not appear."""
    display_name = "Shuffle No-Build Missions"


class EarlyUnit(DefaultOnToggle):
    """Guarantees that the first mission will contain a unit."""
    display_name = "Early Unit"


class RequiredTactics(Choice):
    """Determines the maximum tactical difficulty of the seed (separate from mission difficulty).  Higher settings
    increase randomness.

    Standard:  All missions can be completed with good micro and macro.
    Advanced:  Completing missions may require relying on starting units and micro-heavy units.
    No Logic:  Units and upgrades may be placed anywhere.  LIKELY TO RENDER THE RUN IMPOSSIBLE ON HARDER DIFFICULTIES!"""
    display_name = "Required Tactics"
    option_standard = 0
    option_advanced = 1
    option_no_logic = 2


class UnitsAlwaysHaveUpgrades(DefaultOnToggle):
    """If turned on, all upgrades as determined by the following two options will be present for each unit in the seed.
    This usually results in fewer units."""
    display_name = "Units Always Have Upgrades"


class IncludeMutations(Range):
    """Determines how many of the 3 mutations for the 7 units that have them can appear."""
    display_name = "Include Mutations"
    range_start = 0
    range_end = 3
    default = 1


class IncludeStrains(Range):
    """Determines how many of the 2 strains for the 7 units that have them can appear."""
    display_name = "Include Strains"
    range_start = 0
    range_end = 2
    default = 1


class Kerriganless(Choice):
    """Determines whether Kerrigan is playable outside of missions that require her.

    Off:  Kerrigan is playable as normal.
    On:  Kerrigan is not playable.  Other hero units stay playable,
    and locations normally requiring Kerrigan can be checked by any unit.
    Kerrigan level items, active abilities and passive abilities affecting her will not appear.
    On Without Passives:  In addition to the above, Kerrigan's passive abilities affecting other units (such as Twin Drones) will not appear."""
    display_name = "Kerriganless"
    option_off = 0
    option_on = 1
    option_on_without_passives = 2


class KerriganLevelDistribution(Choice):
    """Determines the amount and size of Kerrigan level items.  Kerrigan's maximum level is 70.

    Vanilla:  Uses the distribution in the vanilla campaign.
    This entails 32 individual levels and 6 packs of varying sizes.
    Smooth:  Uses a custom, condensed distribution of 10 total items,
    intended to fit more levels into settings with little room for filler while keeping some variance in level gains.
    7x10:  Uses 7 items worth 10 levels each.
    10x7:  Uses 10 items worth 7 levels each.
    14x5:  Uses 14 items worth 5 levels each.
    35x2:  Uses 35 items worth 2 level eachs.
    70x1:  Uses 70 individual levels.  As there are not enough locations in the game for this distribution,
    this will result in a greatly reduced maximum level, and is likely to remove many other items."""
    display_name = "Kerrigan Level Distribution"
    option_vanilla = 0
    option_smooth = 1
    option_7x10 = 2
    option_10x7 = 3
    option_14x5 = 4
    option_35x2 = 5
    option_70x1 = 6


class IncludeAllKerriganAbilities(Toggle):
    """If turned on, all passive abilities from every Kerrigan ability tier will be able to appear.
    There will never be more than one active ability per tier.
    If turned off, one random passive or active ability per tier will be included."""
    display_name = "Include All Kerrigan Abilities"


class StartPrimaryAbilities(Range):
    """Number of Primary Abilities (Kerrigan Tier 1, 2, and 4) to start the game with.
    """
    display_name = "Starting Primary Abilities"
    range_start = 0
    range_end = 4
    default = 0

# class UpgradeBonus(Choice):
#     """Determines what lab upgrade to use, whether it is Ultra-Capacitors which boost attack speed with every weapon
#     upgrade or Vanadium Plating which boosts life with every armor upgrade."""
#     display_name = "Upgrade Bonus"
#     option_ultra_capacitors = 0
#     option_vanadium_plating = 1


# class BunkerUpgrade(Choice):
#     """Determines what bunker lab upgrade to use, whether it is Shrike Turret which outfits bunkers with an automated
#     turret or Fortified Bunker which boosts the life of bunkers."""
#     display_name = "Bunker Upgrade"
#     option_shrike_turret = 0
#     option_fortified_bunker = 1


# class AllInMap(Choice):
#     """Determines what version of All-In (final map) that will be generated for the campaign."""
#     display_name = "All In Map"
#     option_ground = 0
#     option_air = 1


# class ShuffleProtoss(DefaultOnToggle):
#     """Determines if the 3 protoss missions are included in the shuffle if Vanilla mission order is not enabled.
#     If turned off with Vanilla Shuffled, the 3 protoss missions will be in their normal position on the Prophecy chain
#        if not shuffled.
#     If turned off with reduced mission settings, the 3 protoss missions will not appear and Protoss units are removed
#         from the pool."""
#     display_name = "Shuffle Protoss Missions"


class LockedItems(ItemSet):
    """Guarantees that these items will be unlockable"""
    display_name = "Locked Items"


class ExcludedItems(ItemSet):
    """Guarantees that these items will not be unlockable"""
    display_name = "Excluded Items"


class ExcludedMissions(OptionSet):
    """Guarantees that these missions will not appear in the campaign
    Only applies on shortened mission orders.
    It may be impossible to build a valid campaign if too many missions are excluded."""
    display_name = "Excluded Missions"
    valid_keys = {mission_name for mission_name in vanilla_mission_req_table.keys() if mission_name != 'The Reckoning'}


# noinspection PyTypeChecker
sc2hots_options: Dict[str, Option] = {
    "game_difficulty": GameDifficulty,
    "mission_order": MissionOrder,
    "player_color": PlayerColor,
    "player_color_primal": PlayerColorPrimal,
    "shuffle_no_build": ShuffleNoBuild,
    "early_unit": EarlyUnit,
    "required_tactics": RequiredTactics,
    "units_always_have_upgrades": UnitsAlwaysHaveUpgrades,
    "include_mutations": IncludeMutations,
    "include_strains": IncludeStrains,
    "kerriganless": Kerriganless,
    "kerrigan_level_distribution": KerriganLevelDistribution,
    "include_all_kerrigan_abilities": IncludeAllKerriganAbilities,
    "start_primary_abilities": StartPrimaryAbilities,
    # "upgrade_bonus": UpgradeBonus,
    # "bunker_upgrade": BunkerUpgrade,
    # "all_in_map": AllInMap,
    # "shuffle_protoss": ShuffleProtoss,
    "locked_items": LockedItems,
    "excluded_items": ExcludedItems,
    "excluded_missions": ExcludedMissions
}


def get_option_value(multiworld: MultiWorld, player: int, name: str) -> Union[int,  FrozenSet]:
    if multiworld is None:
        return sc2hots_options[name].default

    player_option = getattr(multiworld, name)[player]

    return player_option.value
