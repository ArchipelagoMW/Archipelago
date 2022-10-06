from typing import Dict
from BaseClasses import MultiWorld
from Options import Choice, Option, DefaultOnToggle, ItemSet


class GameDifficulty(Choice):
    """The difficulty of the campaign, affects enemy AI, starting units, and game speed."""
    display_name = "Game Difficulty"
    option_casual = 0
    option_normal = 1
    option_hard = 2
    option_brutal = 3


class UpgradeBonus(Choice):
    """Determines what lab upgrade to use, whether it is Ultra-Capacitors which boost attack speed with every weapon upgrade
    or Vanadium Plating which boosts life with every armor upgrade."""
    display_name = "Upgrade Bonus"
    option_ultra_capacitors = 0
    option_vanadium_plating = 1


class BunkerUpgrade(Choice):
    """Determines what bunker lab upgrade to use, whether it is Shrike Turret which outfits bunkers with an automated turret or
    Fortified Bunker which boosts the life of bunkers."""
    display_name = "Bunker Upgrade"
    option_shrike_turret = 0
    option_fortified_bunker = 1


class AllInMap(Choice):
    """Determines what version of All-In (final map) that will be generated for the campaign."""
    display_name = "All In Map"
    option_ground = 0
    option_air = 1


class MissionOrder(Choice):
    """Determines the order the missions are played in.
    Vanilla: Keeps the standard mission order and branching from the WoL Campaign.
    Vanilla Shuffled: Keeps same branching paths from the WoL Campaign but randomizes the order of missions within.
    Mini Shuffle: Shorter version of the campaign with randomized missions and optional branches.
    Grid:  A 4x4 grid of random missions.  Start at the top left and forge a path towards All-In.
    Mini Grid:  A 3x3 version of Grid.
    Blitz:  10 random missions that open up very quickly.
    Gauntlet: Linear series of 7 random missions to complete the campaign.
    """
    display_name = "Mission Order"
    option_vanilla = 0
    option_vanilla_shuffled = 1
    option_mini_shuffle = 2
    option_grid = 3
    option_mini_grid = 4
    option_blitz = 5
    option_gauntlet = 6


class ShuffleProtoss(DefaultOnToggle):
    """Determines if the 3 protoss missions are included in the shuffle if Vanilla mission order is not enabled.
    On Vanilla Shuffled, the 3 protoss missions will be in their normal position on the Prophecy chain if not shuffled.
    On reduced mission settings, the 3 protoss missions will not appear and Protoss units are removed from the pool if not shuffled.
    """
    display_name = "Shuffle Protoss Missions"


class RelegateNoBuildMissions(DefaultOnToggle):
    """Determines if the 5 no-build missions are included in the shuffle if Vanilla mission order is not enabled.
    On Vanilla Shuffled, one no-build mission will be placed as the first mission and the rest will be placed at the end of optional routes.
    On reduced mission settings, the 5 no-build missions will not appear."""
    display_name = "Relegate No-Build Missions"


class EarlyUnit(DefaultOnToggle):
    """Guarantees that the first mission will contain a unit."""
    display_name = "Early Unit"


class LockedItems(ItemSet):
    """Guarantees that these items will appear in your world"""
    display_name = "Locked Items"


class ExcludedItems(ItemSet):
    """Guarantees that these items will not appear in your world"""
    display_name = "Excluded Items"


# noinspection PyTypeChecker
sc2wol_options: Dict[str, Option] = {
    "game_difficulty": GameDifficulty,
    "upgrade_bonus": UpgradeBonus,
    "bunker_upgrade": BunkerUpgrade,
    "all_in_map": AllInMap,
    "mission_order": MissionOrder,
    "shuffle_protoss": ShuffleProtoss,
    "relegate_no_build": RelegateNoBuildMissions,
    "early_unit": EarlyUnit,
    "locked_items": LockedItems,
    "excluded_items": ExcludedItems
}


def get_option_value(world: MultiWorld, player: int, name: str) -> int:
    option = getattr(world, name, None)

    if option == None:
        return 0

    return int(option[player].value)
