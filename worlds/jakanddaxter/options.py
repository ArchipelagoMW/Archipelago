from dataclasses import dataclass
from functools import cached_property
from Options import PerGameCommonOptions, StartInventoryPool, Toggle, Choice, Range, DefaultOnToggle, OptionCounter
from .items import trap_item_table


class StaticGetter:
    def __init__(self, func):
        self.fget = func

    def __get__(self, instance, owner):
        return self.fget(owner)


@StaticGetter
def determine_range_end(cls) -> int:
    from . import JakAndDaxterWorld
    enforce_friendly_options = JakAndDaxterWorld.settings.enforce_friendly_options
    return cls.friendly_maximum if enforce_friendly_options else cls.absolute_maximum


class EnableMoveRandomizer(Toggle):
    """Include movement options as items in the randomizer. Until you find his other moves, Jak is limited to
    running, swimming, single-jumping, and shooting yellow eco through his goggles.

    This adds 11 items to the pool."""
    display_name = "Enable Move Randomizer"


class EnableOrbsanity(Choice):
    """Include bundles of Precursor Orbs as checks. Every time you collect the chosen number of orbs, you will trigger
    another check.

    Per Level: bundles are for each level in the game.
    Global: bundles carry over level to level.

    This adds a number of Items and Locations to the pool inversely proportional to the size of the bundle.
    For example, if your bundle size is 20 orbs, you will add 100 items to the pool. If your bundle size is 250 orbs,
    you will add 8 items to the pool."""
    display_name = "Enable Orbsanity"
    option_off = 0
    option_per_level = 1
    option_global = 2
    default = 0


class GlobalOrbsanityBundleSize(Choice):
    """The orb bundle size for Global Orbsanity. This only applies if "Enable Orbsanity" is set to "Global."
    There are 2000 orbs in the game, so your bundle size must be a factor of 2000.

    Multiplayer Minimum: 10
    Multiplayer Maximum: 200"""
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
    friendly_minimum = 10
    friendly_maximum = 200
    default = 20


class PerLevelOrbsanityBundleSize(Choice):
    """The orb bundle size for Per Level Orbsanity. This only applies if "Enable Orbsanity" is set to "Per Level."
    There are 50, 150, or 200 orbs per level, so your bundle size must be a factor of 50.

    Multiplayer Minimum: 10"""
    display_name = "Per Level Orbsanity Bundle Size"
    option_1_orb = 1
    option_2_orbs = 2
    option_5_orbs = 5
    option_10_orbs = 10
    option_25_orbs = 25
    option_50_orbs = 50
    friendly_minimum = 10
    default = 25


class FireCanyonCellCount(Range):
    """The number of power cells you need to cross Fire Canyon. This value is restricted to a safe maximum value to
    ensure valid singleplayer games and non-disruptive multiplayer games, but the host can remove this restriction by
    turning off enforce_friendly_options in host.yaml."""
    display_name = "Fire Canyon Cell Count"
    friendly_maximum = 30
    absolute_maximum = 100
    range_start = 0
    range_end = determine_range_end
    default = 20


class MountainPassCellCount(Range):
    """The number of power cells you need to reach Klaww and cross Mountain Pass. This value is restricted to a safe
    maximum value to ensure valid singleplayer games and non-disruptive multiplayer games, but the host can
    remove this restriction by turning off enforce_friendly_options in host.yaml."""
    display_name = "Mountain Pass Cell Count"
    friendly_maximum = 60
    absolute_maximum = 100
    range_start = 0
    range_end = determine_range_end
    default = 45


class LavaTubeCellCount(Range):
    """The number of power cells you need to cross Lava Tube. This value is restricted to a safe maximum value to
    ensure valid singleplayer games and non-disruptive multiplayer games, but the host can remove this restriction by
    turning off enforce_friendly_options in host.yaml."""
    display_name = "Lava Tube Cell Count"
    friendly_maximum = 90
    absolute_maximum = 100
    range_start = 0
    range_end = determine_range_end
    default = 72


class EnableOrderedCellCounts(DefaultOnToggle):
    """Reorder the Cell Count requirements for vehicle sections to be in ascending order.

    For example, if Fire Canyon Cell Count, Mountain Pass Cell Count, and Lava Tube Cell Count are 60, 30, and 40
    respectively, they will be reordered to 30, 40, and 60."""
    display_name = "Enable Ordered Cell Counts"


class RequirePunchForKlaww(DefaultOnToggle):
    """Force the Punch move to come before Klaww. Disabling this setting may require Jak to fight Klaww
    and Gol and Maia by shooting yellow eco through his goggles. This only applies if "Enable Move Randomizer" is ON."""
    display_name = "Require Punch For Klaww"


# 222 is the absolute maximum because there are 9 citizen trades and 2000 orbs to trade (2000/9 = 222).
class CitizenOrbTradeAmount(Range):
    """The number of orbs you need to trade to citizens for a power cell (Mayor, Uncle, etc.).

    Along with Oracle Orb Trade Amount, this setting cannot exceed the total number of orbs in the game (2000).
    The equation to determine the total number of trade orbs is (9 * Citizen Trades) + (6 * Oracle Trades).

    This value is restricted to a safe maximum value to ensure valid singleplayer games and non-disruptive
    multiplayer games, but the host can remove this restriction by turning off enforce_friendly_options in host.yaml."""
    display_name = "Citizen Orb Trade Amount"
    friendly_maximum = 120
    absolute_maximum = 222
    range_start = 0
    range_end = determine_range_end
    default = 90


# 333 is the absolute maximum because there are 6 oracle trades and 2000 orbs to trade (2000/6 = 333).
class OracleOrbTradeAmount(Range):
    """The number of orbs you need to trade to the Oracles for a power cell.

    Along with Citizen Orb Trade Amount, this setting cannot exceed the total number of orbs in the game (2000).
    The equation to determine the total number of trade orbs is (9 * Citizen Trades) + (6 * Oracle Trades).

    This value is restricted to a safe maximum value to ensure valid singleplayer games and non-disruptive
    multiplayer games, but the host can remove this restriction by turning off enforce_friendly_options in host.yaml."""
    display_name = "Oracle Orb Trade Amount"
    friendly_maximum = 150
    absolute_maximum = 333
    range_start = 0
    range_end = determine_range_end
    default = 120


class FillerPowerCellsReplacedWithTraps(Range):
    """
    The number of filler power cells that will be replaced with traps. This does not affect the number of progression
    power cells.

    If this value is greater than the number of filler power cells, then they will all be replaced with traps.
    """
    display_name = "Filler Power Cells Replaced With Traps"
    range_start = 0
    range_end = 100
    default = 0


class FillerOrbBundlesReplacedWithTraps(Range):
    """
    The number of filler orb bundles that will be replaced with traps. This does not affect the number of progression
    orb bundles. This only applies if "Enable Orbsanity" is set to "Per Level" or "Global."

    If this value is greater than the number of filler orb bundles, then they will all be replaced with traps.
    """
    display_name = "Filler Orb Bundles Replaced With Traps"
    range_start = 0
    range_end = 2000
    default = 0


class TrapEffectDuration(Range):
    """
    The length of time, in seconds, that a trap effect lasts.
    """
    display_name = "Trap Effect Duration"
    range_start = 5
    range_end = 60
    default = 30


class TrapWeights(OptionCounter):
    """
    The list of traps and corresponding weights that will be randomly added to the item pool. A trap with weight 10 is
    twice as likely to appear as a trap with weight 5. Set a weight to 0 to prevent that trap from appearing altogether.
    If all weights are 0, no traps are created, overriding the values of "Filler * Replaced With Traps."
    """
    display_name = "Trap Weights"
    min = 0
    default = {trap: 1 for trap in trap_item_table.values()}
    valid_keys = sorted({trap for trap in trap_item_table.values()})

    @cached_property
    def weights_pair(self) -> tuple[list[str], list[int]]:
        return list(self.value.keys()), list(self.value.values())


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
    enable_ordered_cell_counts: EnableOrderedCellCounts
    require_punch_for_klaww: RequirePunchForKlaww
    citizen_orb_trade_amount: CitizenOrbTradeAmount
    oracle_orb_trade_amount: OracleOrbTradeAmount
    filler_power_cells_replaced_with_traps: FillerPowerCellsReplacedWithTraps
    filler_orb_bundles_replaced_with_traps: FillerOrbBundlesReplacedWithTraps
    trap_effect_duration: TrapEffectDuration
    trap_weights: TrapWeights
    jak_completion_condition: CompletionCondition
    start_inventory_from_pool: StartInventoryPool
