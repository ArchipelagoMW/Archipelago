import pkgutil
from dataclasses import dataclass

import orjson

from Options import Toggle, Choice, PerGameCommonOptions, NamedRange, Range
from .common.options import FloatRangeText

datapackage_options = orjson.loads(pkgutil.get_data(__name__, "data/options.json"))
max_levels_and_upgrades = datapackage_options["max_levels_and_upgrades"]
max_shapesanity = datapackage_options["max_shapesanity"]
del datapackage_options


class Goal(Choice):
    """Sets the goal of your world.

    - **Vanilla:** Complete level 26.
    - **MAM:** Complete a specified level after level 26. Every level before that will be a location. It's recommended
      to build a Make-Anything-Machine (MAM).
    - **Even fasterer:** Upgrade everything to a specified tier after tier 8. Every upgrade before that will be a
      location.
    - **Efficiency III:** Deliver 256 blueprint shapes per second to the hub."""
    display_name = "Goal"
    rich_text_doc = True
    option_vanilla = 0
    option_mam = 1
    option_even_fasterer = 2
    option_efficiency_iii = 3
    default = 0


class GoalAmount(NamedRange):
    """Specify, what level or tier (when either MAM or Even Fasterer is chosen as goal) is required to reach the goal.

    If MAM is set as the goal, this has to be set to 27 or more. Else it will raise an error."""
    display_name = "Goal amount"
    rich_text_doc = True
    range_start = 9
    range_end = max_levels_and_upgrades
    default = 27
    special_range_names = {
        "minimum_mam": 27,
        "recommended_mam": 50,
        "long_game_mam": 120,
        "minimum_even_fasterer": 9,
        "recommended_even_fasterer": 16,
        "long_play_even_fasterer": 35,
    }


class RequiredShapesMultiplier(Range):
    """Multiplies the amount of required shapes for levels and upgrades by value/10.

    For level 1, the amount of shapes ranges from 3 to 300.

    For level 26, it ranges from 5k to 500k."""
    display_name = "Required shapes multiplier"
    rich_text_doc = True
    range_start = 1
    range_end = 100
    default = 10


class AllowFloatingLayers(Toggle):
    """Toggle whether shape requirements are allowed to have floating layers (like the logo or the rocket shape).

    However, be aware that floating shapes make MAMs much more complex."""
    display_name = "Allow floating layers"
    rich_text_doc = True
    default = False


class RandomizeLevelRequirements(Toggle):
    """Randomize the required shapes to complete levels."""
    display_name = "Randomize level requirements"
    rich_text_doc = True
    default = True


class RandomizeUpgradeRequirements(Toggle):
    """Randomize the required shapes to buy upgrades."""
    display_name = "Randomize upgrade requirements"
    rich_text_doc = True
    default = True


class RandomizeLevelLogic(Choice):
    """If level requirements are randomized, this sets how those random shapes are generated and how logic works for
    levels. The shuffled variants shuffle the order of progression buildings obtained in the multiworld. The standard
    order is: **cutter -> rotator -> painter -> color mixer -> stacker**

    - **Vanilla:** Level 1 requires nothing, 2-4 require the first building, 5-6 require also the second, 7-8 the
      third, 9-10 the fourth, and 11 and onwards the fifth and thereby all buildings.
    - **Stretched:** After every floor(maxlevel/6) levels, another building is required.
    - **Quick:** Every Level, except level 1, requires another building, with level 6 and onwards requiring all
      buildings.
    - **Random steps:** After a random amount of levels, another building is required, with level 1 always requiring
      none. This can potentially generate like any other option.
    - **Hardcore:** All levels (except level 1) have completely random shape requirements and thus require all
      buildings. Expect early BKs.
    - **Dopamine (overflow):** All levels (except level 1 and the goal) require 2 random buildings (or none in case of
      overflow)."""
    display_name = "Randomize level logic"
    rich_text_doc = True
    option_vanilla = 0
    option_vanilla_shuffled = 1
    option_stretched = 2
    option_stretched_shuffled = 3
    option_quick = 4
    option_quick_shuffled = 5
    option_random_steps = 6
    option_random_steps_shuffled = 7
    option_hardcore = 8
    option_dopamine = 9
    option_dopamine_overflow = 10
    default = 2


class RandomizeUpgradeLogic(Choice):
    """If upgrade requirements are randomized, this sets how those random shapes are generated
    and how logic works for upgrades.

    - **Vanilla-like:** Tier II requires up to two random buildings, III requires up to three random buildings,
      and IV and onwards require all processing buildings.
    - **Linear:** Tier II requires nothing, III-VI require another random building each,
      and VII and onwards require all buildings.
    - **Category:** Belt and miner upgrades require no building up to tier V, but onwards all buildings, processors
      upgrades require the cutter (all tiers), rotator (tier III and onwards), and stacker (tier V and onwards), and
      painting upgrades require the cutter, rotator, stacker, painter (all tiers) and color mixer (tiers V and onwards).
      Tier VII and onwards will always require all buildings.
    - **Category random:** Each upgrades category (up to tier VI) requires a random amount of buildings (in order),
      with one category always requiring no buildings. Tier VII and onwards will always require all buildings.
    - **Hardcore:** All tiers (except each tier II) have completely random shape requirements and thus require all
      buildings. Expect early BKs."""
    display_name = "Randomize upgrade logic"
    rich_text_doc = True
    option_vanilla_like = 0
    option_linear = 1
    option_category = 2
    option_category_random = 3
    option_hardcore = 4
    default = 1


class ThroughputLevelsRatio(NamedRange):
    """If level requirements are randomized, this sets the ratio of how many levels (approximately) will require either
    a total amount or per second amount (throughput) of shapes delivered.

    0 means only total, 100 means only throughput, and vanilla (-1) means only levels 14, 27 and beyond have throughput.
    """
    display_name = "Throughput levels ratio"
    rich_text_doc = True
    range_start = 0
    range_end = 100
    default = 0
    special_range_names = {
        "vanilla": -1,
        "only_total": 0,
        "half_half": 50,
        "only_throughput": 100,
    }


class ComplexityGrowthGradient(FloatRangeText):
    """If level requirements are randomized, this determines how fast complexity will grow each level. In other words:
    The higher you set this value, the more difficult lategame shapes will be.

    Allowed values are floating numbers ranging from 0.0 to 10.0."""
    display_name = "Complexity growth gradient"
    rich_text_doc = True
    range_start = 0.0
    range_end = 10.0
    default = "0.5"


class SameLateUpgradeRequirements(Toggle):
    """If upgrade requirements are randomized, should the last 3 shapes for each category be the same,
    as in vanilla?"""
    display_name = "Same late upgrade requirements"
    rich_text_doc = True
    default = True


class EarlyBalancerTunnelAndTrash(Choice):
    """Makes the balancer, tunnel, and trash appear in earlier spheres.

    - **None:** Complete randomization.
    - **5 buildings:** Should be accessible before getting all 5 main buildings.
    - **3 buildings:** Should be accessible before getting the first 3 main buildings for levels and upgrades.
    - **Sphere 1:** Always accessible from start. **Beware of generation failures.**"""
    display_name = "Early balancer, tunnel, and trash"
    rich_text_doc = True
    option_none = 0
    option_5_buildings = 1
    option_3_buildings = 2
    option_sphere_1 = 3
    default = 2


class LockBeltAndExtractor(Toggle):
    """Locks Belts and Extractors and adds them to the item pool.

    **If you set this to true, achievements must also be included.**"""
    display_name = "Lock Belt and Extractor"
    rich_text_doc = True
    default = False


class IncludeAchievements(Toggle):
    """Include up to 45 achievements (depending on other options) as additional locations."""
    display_name = "Include Achievements"
    rich_text_doc = True
    default = True


class ExcludeSoftlockAchievements(Toggle):
    """Exclude 6 achievements, that can become unreachable in a save file, if not achieved until a certain level."""
    display_name = "Exclude softlock achievements"
    rich_text_doc = True
    default = True


class ExcludeLongPlaytimeAchievements(Toggle):
    """Exclude 2 achievements, that require actively playing for a really long time."""
    display_name = "Exclude long playtime achievements"
    rich_text_doc = True
    default = True


class ExcludeProgressionUnreasonable(Toggle):
    """Exclude progression and useful items from being placed into softlock and long playtime achievements."""
    display_name = "Exclude progression items in softlock and long playtime achievements"
    rich_text_doc = True
    default = True


class ShapesanityAmount(Range):
    """Amount of single-layer shapes that will be included as locations."""
    display_name = "Shapesanity amount"
    rich_text_doc = True
    range_start = 4
    range_end = max_shapesanity
    default = 50


class TrapsProbability(NamedRange):
    """The probability of any filler item (in percent) being replaced by a trap."""
    display_name = "Traps Percentage"
    rich_text_doc = True
    range_start = 0
    range_end = 100
    default = 0
    special_range_names = {
        "none": 0,
        "rare": 4,
        "occasionally": 10,
        "maximum_suffering": 100,
    }


class IncludeWhackyUpgrades(Toggle):
    """Includes some very unusual upgrade items in generation (and logic), that greatly increase or decrease building
    speeds. If the goal is set to Efficiency III or throughput levels ratio is not 0, decreasing upgrades (aka traps)
    will always be disabled."""
    display_name = "Include Whacky Upgrades"
    rich_text_doc = True
    default = False


class SplitInventoryDrainingTrap(Toggle):
    """If set to true, the inventory draining trap will be split into level, upgrade, and blueprint draining traps
    instead of executing as one of those 3 randomly."""
    display_name = "Split Inventory Draining Trap"
    rich_text_doc = True
    default = False


class ToolbarShuffling(Toggle):
    """If set to true, the toolbars (main and wires layer) will be shuffled (including bottom and top row).
    However, keybindings will still select the same building to place."""
    display_name = "Toolbar Shuffling"
    rich_text_doc = True
    default = True


@dataclass
class ShapezOptions(PerGameCommonOptions):
    goal: Goal
    goal_amount: GoalAmount
    required_shapes_multiplier: RequiredShapesMultiplier
    allow_floating_layers: AllowFloatingLayers
    randomize_level_requirements: RandomizeLevelRequirements
    randomize_upgrade_requirements: RandomizeUpgradeRequirements
    randomize_level_logic: RandomizeLevelLogic
    randomize_upgrade_logic: RandomizeUpgradeLogic
    throughput_levels_ratio: ThroughputLevelsRatio
    complexity_growth_gradient: ComplexityGrowthGradient
    same_late_upgrade_requirements: SameLateUpgradeRequirements
    early_balancer_tunnel_and_trash: EarlyBalancerTunnelAndTrash
    lock_belt_and_extractor: LockBeltAndExtractor
    include_achievements: IncludeAchievements
    exclude_softlock_achievements: ExcludeSoftlockAchievements
    exclude_long_playtime_achievements: ExcludeLongPlaytimeAchievements
    exclude_progression_unreasonable: ExcludeProgressionUnreasonable
    shapesanity_amount: ShapesanityAmount
    traps_percentage: TrapsProbability
    include_whacky_upgrades: IncludeWhackyUpgrades
    split_inventory_draining_trap: SplitInventoryDrainingTrap
    toolbar_shuffling: ToolbarShuffling
