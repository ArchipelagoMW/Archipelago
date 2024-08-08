from dataclasses import dataclass
from Options import PerGameCommonOptions, StartInventoryPool, Toggle, Choice, Range


class EnableMoveRandomizer(Toggle):
    """Enable to include movement options as items in the randomizer. Jak is only able to run, swim, and single jump
    until you find his other moves.

    This adds 11 items to the pool."""
    display_name = "Enable Move Randomizer"


class EnableOrbsanity(Choice):
    """Enable to include bundles of Precursor Orbs as an ordered list of progressive checks. Every time you collect the
    chosen number of orbs, you will trigger the next release in the list.

    "Per Level" means these lists are generated and populated for each level in the game. "Global" means there
    is only one list for the entire game.

    This adds a number of Items and Locations to the pool inversely proportional to the size of the bundle.
    For example, if your bundle size is 20 orbs, you will add 100 items to the pool. If your bundle size is 250 orbs,
    you will add 8 items to the pool."""
    display_name = "Enable Orbsanity"
    option_off = 0
    option_per_level = 1
    option_global = 2
    default = 0


class GlobalOrbsanityBundleSize(Choice):
    """Set the orb bundle size for Global Orbsanity. This only applies if "Enable Orbsanity" is set to "Global."
    There are 2000 orbs in the game, so your bundle size must be a factor of 2000."""
    display_name = "Global Orbsanity Bundle Size"
    option_1_orb = 1
    option_2_orbs = 2
    option_4_orbs = 4
    option_5_orbs = 5
    option_8_orbs = 8
    option_10_orbs = 10
    option_16_orbs = 16
    option_20_orbs = 20
    option_25_orbs = 25
    option_40_orbs = 40
    option_50_orbs = 50
    option_80_orbs = 80
    option_100_orbs = 100
    option_125_orbs = 125
    option_200_orbs = 200
    option_250_orbs = 250
    option_400_orbs = 400
    option_500_orbs = 500
    option_1000_orbs = 1000
    option_2000_orbs = 2000
    default = 1


class PerLevelOrbsanityBundleSize(Choice):
    """Set the orb bundle size for Per Level Orbsanity. This only applies if "Enable Orbsanity" is set to "Per Level."
    There are 50, 150, or 200 orbs per level, so your bundle size must be a factor of 50."""
    display_name = "Per Level Orbsanity Bundle Size"
    option_1_orb = 1
    option_2_orbs = 2
    option_5_orbs = 5
    option_10_orbs = 10
    option_25_orbs = 25
    option_50_orbs = 50
    default = 1


class FireCanyonCellCount(Range):
    """Set the number of orbs you need to cross Fire Canyon."""
    display_name = "Fire Canyon Cell Count"
    range_start = 0
    range_end = 100
    default = 20


class MountainPassCellCount(Range):
    """Set the number of orbs you need to reach Klaww and cross Mountain Pass."""
    display_name = "Mountain Pass Cell Count"
    range_start = 0
    range_end = 100
    default = 45


class LavaTubeCellCount(Range):
    """Set the number of orbs you need to cross Lava Tube."""
    display_name = "Lava Tube Cell Count"
    range_start = 0
    range_end = 100
    default = 72


class CompletionCondition(Choice):
    """Set the goal for completing the game."""
    display_name = "Completion Condition"
    option_cross_fire_canyon = 69
    option_cross_mountain_pass = 87
    option_cross_lava_tube = 89
    option_defeat_dark_eco_plant = 6
    option_defeat_klaww = 86
    option_defeat_gol_and_maia = 112
    option_open_100_cell_door = 116
    default = 112


@dataclass
class JakAndDaxterOptions(PerGameCommonOptions):
    enable_move_randomizer: EnableMoveRandomizer
    enable_orbsanity: EnableOrbsanity
    global_orbsanity_bundle_size: GlobalOrbsanityBundleSize
    level_orbsanity_bundle_size: PerLevelOrbsanityBundleSize
    fire_canyon_cell_count: FireCanyonCellCount
    mountain_pass_cell_count: MountainPassCellCount
    lava_tube_cell_count: LavaTubeCellCount
    jak_completion_condition: CompletionCondition
    start_inventory_from_pool: StartInventoryPool
