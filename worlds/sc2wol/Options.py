from typing import Dict, FrozenSet, Union
from BaseClasses import MultiWorld
from Options import Choice, Option, Toggle, DefaultOnToggle, ItemSet, OptionSet, Range
from .MissionTables import vanilla_mission_req_table

ORDER_VANILLA = 0
ORDER_VANILLA_SHUFFLED = 1

class GameDifficulty(Choice):
    """
    The difficulty of the campaign, affects enemy AI, starting units, and game speed.

    For those unfamiliar with the Archipelago randomizer, the recommended settings are one difficulty level
    lower than the vanilla game
    """
    display_name = "Game Difficulty"
    option_casual = 0
    option_normal = 1
    option_hard = 2
    option_brutal = 3
    default = 1

class GameSpeed(Choice):
    """Optional setting to override difficulty-based game speed."""
    display_name = "Game Speed"
    option_default = 0
    option_slower = 1
    option_slow = 2
    option_normal = 3
    option_fast = 4
    option_faster = 5
    default = option_default

class FinalMap(Choice):
    """
    Determines if the final map and goal of the campaign.
    All in: You need to beat All-in map
    Random Hard: A random hard mission is selected as a goal.
                Beat this mission in order to complete the game.
                All-in map won't be in the campaign

    Vanilla mission order always ends with All in mission!

    Warning: Using All-in with a short mission order (7 or fewer missions) is not recommended,
        as there might not be enough locations to place all the required items,
        any excess required items will be placed into the player's starting inventory!

    This option is short-lived. It may be changed in the future
    """
    display_name = "Final Map"
    option_all_in = 0
    option_random_hard = 1

class AllInMap(Choice):
    """Determines what version of All-In (final map) that will be generated for the campaign."""
    display_name = "All In Map"
    option_ground = 0
    option_air = 1


class MissionOrder(Choice):
    """
    Determines the order the missions are played in.  The last three mission orders end in a random mission.
    Vanilla (29): Keeps the standard mission order and branching from the WoL Campaign.
    Vanilla Shuffled (29): Keeps same branching paths from the WoL Campaign but randomizes the order of missions within.
    Mini Campaign (15): Shorter version of the campaign with randomized missions and optional branches.
    Grid (16):  A 4x4 grid of random missions.  Start at the top-left and forge a path towards bottom-right mission to win.
    Mini Grid (9):  A 3x3 version of Grid.  Complete the bottom-right mission to win.
    Blitz (12):  12 random missions that open up very quickly.  Complete the bottom-right mission to win.
    Gauntlet (7): Linear series of 7 random missions to complete the campaign.
    Mini Gauntlet (4): Linear series of 4 random missions to complete the campaign.
    Tiny Grid (4): A 2x2 version of Grid.  Complete the bottom-right mission to win.
    """
    display_name = "Mission Order"
    option_vanilla = 0
    option_vanilla_shuffled = 1
    option_mini_campaign = 2
    option_grid = 3
    option_mini_grid = 4
    option_blitz = 5
    option_gauntlet = 6
    option_mini_gauntlet = 7
    option_tiny_grid = 8


class PlayerColor(Choice):
    """Determines in-game team color."""
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
    option_default = 17
    default = option_default


class ShuffleProtoss(DefaultOnToggle):
    """Determines if the 3 protoss missions are included in the shuffle if Vanilla mission order is not enabled.
    If turned off, the 3 protoss missions will not appear and Protoss units are removed from the pool."""
    display_name = "Shuffle Protoss Missions"


class ShuffleNoBuild(DefaultOnToggle):
    """Determines if the 5 no-build missions are included in the shuffle if Vanilla mission order is not enabled.
    If turned off, the 5 no-build missions will not appear."""
    display_name = "Shuffle No-Build Missions"


class EarlyUnit(DefaultOnToggle):
    """
    Guarantees that the first mission will contain a unit.

    Each mission available to be the first mission has a pre-defined location where the unit should spawn.
    This location gets overriden over any exclusion. It's guaranteed to be reachable with an empty inventory.
    """
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
    """
    If turned on, all upgrades will be present for each unit and structure in the seed.
    This usually results in fewer units.

    See also: Max Number of Upgrades
    """
    display_name = "Units Always Have Upgrades"


class GenericUpgradeMissions(Range):
    """Determines the percentage of missions in the mission order that must be completed before
    level 1 of all weapon and armor upgrades is unlocked.  Level 2 upgrades require double the amount of missions,
    and level 3 requires triple the amount.  The required amounts are always rounded down.
    If set to 0, upgrades are instead added to the item pool and must be found to be used."""
    display_name = "Generic Upgrade Missions"
    range_start = 0
    range_end = 100
    default = 0


class GenericUpgradeResearch(Choice):
    """Determines how weapon and armor upgrades affect missions once unlocked.

    Vanilla:  Upgrades must be researched as normal.
    Auto In No-Build:  In No-Build missions, upgrades are automatically researched.
    In all other missions, upgrades must be researched as normal.
    Auto In Build:  In No-Build missions, upgrades are unavailable as normal.
    In all other missions, upgrades are automatically researched.
    Always Auto:  Upgrades are automatically researched in all missions."""
    display_name = "Generic Upgrade Research"
    option_vanilla = 0
    option_auto_in_no_build = 1
    option_auto_in_build = 2
    option_always_auto = 3


class GenericUpgradeItems(Choice):
    """Determines how weapon and armor upgrades are split into items.  All options produce 3 levels of each item.
    Does nothing if upgrades are unlocked by completed mission counts.

    Individual Items:  All weapon and armor upgrades are each an item,
    resulting in 18 total upgrade items.
    Bundle Weapon And Armor:  All types of weapon upgrades are one item,
    and all types of armor upgrades are one item,
    resulting in 6 total items.
    Bundle Unit Class:  Weapon and armor upgrades are merged,
    but Infantry, Vehicle, and Starship upgrades are bundled separately,
    resulting in 9 total items.
    Bundle All:  All weapon and armor upgrades are one item,
    resulting in 3 total items."""
    display_name = "Generic Upgrade Items"
    option_individual_items = 0
    option_bundle_weapon_and_armor = 1
    option_bundle_unit_class = 2
    option_bundle_all = 3


class NovaCovertOpsItems(Toggle):
    """If turned on, the equipment upgrades from Nova Covert Ops may be present in the world."""
    display_name = "Nova Covert Ops Items"
    default = Toggle.option_true


class BroodWarItems(Toggle):
    """If turned on, returning items from StarCraft: Brood War may appear in the world."""
    display_name = "Brood War Items"
    default = Toggle.option_true


class ExtendedItems(Toggle):
    """If turned on, original items that did not appear in Campaign mode may appear in the world."""
    display_name = "Extended Items"
    default = Toggle.option_true


class MaxNumberOfUpgrades(Range):
    """
    Set a maximum to the number of upgrades a unit/structure can have. -1 is used to define unlimited.
    Note that most unit have 4 or 6 upgrades.

    If used with Units Always Have Upgrades, each unit has this given amount of upgrades (if there enough upgrades exist)

    See also: Units Always Have Upgrades
    """
    display_name = "Maximum number of upgrades per unit/structure"
    range_start = -1
    # Do not know the maximum, but it is less than 123!
    range_end = 123
    default = -1


class LockedItems(ItemSet):
    """Guarantees that these items will be unlockable"""
    display_name = "Locked Items"


class ExcludedItems(ItemSet):
    """Guarantees that these items will not be unlockable"""
    display_name = "Excluded Items"


class ExcludedMissions(OptionSet):
    """Guarantees that these missions will not appear in the campaign
    Doesn't apply to vanilla mission order.
    It may be impossible to build a valid campaign if too many missions are excluded."""
    display_name = "Excluded Missions"
    valid_keys = {mission_name for mission_name in vanilla_mission_req_table.keys() if mission_name != 'All-In'}


class LocationInclusion(Choice):
    option_enabled = 0
    option_trash = 1
    option_nothing = 2


class MissionProgressLocations(LocationInclusion):
    """
    Enables or disables item rewards for progressing (not finishing) a mission.
    Progressing a mission is usually a task of completing or progressing into a main objective.
    Clearing an expansion base also counts here.

    Enabled: All locations fitting into this do their normal rewards
    Trash: Forces a trash item in
    Nothing: No rewards for this type of tasks, effectively disabling such locations

    Note: Individual locations subject to plando are always enabled, so the plando can be placed properly.
    See also: Excluded Locations, Item Plando (https://archipelago.gg/tutorial/Archipelago/plando/en#item-plando)
    """
    display_name = "Mission Progress Locations"


class BonusLocations(LocationInclusion):
    """
    Enables or disables item rewards for completing bonus tasks.
    Bonus tasks are those giving you a campaign-wide or mission-wide bonus in vanilla game:
    Research, credits, bonus units or resources, etc.

    Enabled: All locations fitting into this do their normal rewards
    Trash: Forces a trash item in
    Nothing: No rewards for this type of tasks, effectively disabling such locations

    Note: Individual locations subject to plando are always enabled, so the plando can be placed properly.
    See also: Excluded Locations, Item Plando (https://archipelago.gg/tutorial/Archipelago/plando/en#item-plando)
    """
    display_name = "Bonus Locations"


class ChallengeLocations(LocationInclusion):
    """
    Enables or disables item rewards for completing challenge tasks.
    Challenges are tasks that have usually higher requirements to be completed
    than to complete the mission they're in successfully.
    You might be required to visit the same mission later when getting stronger in order to finish these tasks.

    Enabled: All locations fitting into this do their normal rewards
    Trash: Forces a trash item in
    Nothing: No rewards for this type of tasks, effectively disabling such locations

    Note: Individual locations subject to plando are always enabled, so the plando can be placed properly.
    See also: Excluded Locations, Item Plando (https://archipelago.gg/tutorial/Archipelago/plando/en#item-plando)
    """
    display_name = "Challenge Locations"


class OptionalBossLocations(LocationInclusion):
    """
    Enables or disables item rewards for defeating optional bosses.
    An optional boss is any boss that's not required to kill in order to finish the mission successfully.
    All Brutalisks, Loki, etc. belongs here.

    Enabled: All locations fitting into this do their normal rewards
    Trash: Forces a trash item in
    Nothing: No rewards for this type of tasks, effectively disabling such locations

    Note: Individual locations subject to plando are always enabled, so the plando can be placed properly.
    See also: Excluded Locations, Item Plando (https://archipelago.gg/tutorial/Archipelago/plando/en#item-plando)
    """
    display_name = "Optional Boss Locations"


# noinspection PyTypeChecker
sc2wol_options: Dict[str, Option] = {
    "game_difficulty": GameDifficulty,
    "game_speed": GameSpeed,
    "all_in_map": AllInMap,
    "final_map": FinalMap,
    "mission_order": MissionOrder,
    "player_color": PlayerColor,
    "shuffle_protoss": ShuffleProtoss,
    "shuffle_no_build": ShuffleNoBuild,
    "early_unit": EarlyUnit,
    "required_tactics": RequiredTactics,
    "units_always_have_upgrades": UnitsAlwaysHaveUpgrades,
    "max_number_of_upgrades": MaxNumberOfUpgrades,
    "generic_upgrade_missions": GenericUpgradeMissions,
    "generic_upgrade_research": GenericUpgradeResearch,
    "generic_upgrade_items": GenericUpgradeItems,
    "locked_items": LockedItems,
    "excluded_items": ExcludedItems,
    "excluded_missions": ExcludedMissions,
    "nco_items": NovaCovertOpsItems,
    "bw_items": BroodWarItems,
    "ext_items": ExtendedItems,
    "mission_progress_locations": MissionProgressLocations,
    "bonus_locations": BonusLocations,
    "challenge_locations": ChallengeLocations,
    "optional_boss_locations": OptionalBossLocations
}


def get_option_value(multiworld: MultiWorld, player: int, name: str) -> Union[int,  FrozenSet]:
    if multiworld is None:
        return sc2wol_options[name].default

    player_option = getattr(multiworld, name)[player]

    return player_option.value
