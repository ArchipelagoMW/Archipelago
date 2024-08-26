from dataclasses import dataclass

from Options import Range, Toggle, Choice, PerGameCommonOptions


class Goal(Choice):
    """Sets the goal of your world.

    - **Vanilla:** Complete level 26.
    - **MAM:** Complete a specified level after level 26. Every level before that and a few additional options will be a
    location. It's recommended to build a Make-Anything-Machine (MAM).
    - **Even fasterer:** Upgrade everything to a specified tier after tier 8. Every upgrade before that will be a location.
    - **Efficiency III:** Deliver 500 blueprint shapes per second to the hub."""
    display_name = "Goal"
    rich_text_doc = True
    option_vanilla = 0
    option_mam = 1
    option_even_fasterer = 2
    option_efficiency_iii = 3
    default = 0


class GoalAmount(Range):
    """Specify, what level or tier (when either MAM or even fasterer is chosen as goal) is required to reach the goal.
    If MAM is set as the goal and this is set to less than 27, it will raise an OptionError."""
    display_name = "Goal amount"
    rich_text_doc = True
    range_start = 9
    range_end = 1000
    default = 27


class RequiredShapesMultiplier(Range):
    """Multiplies the amount of required shapes for levels and upgrades by value/10.
    For level 1, the amount of shapes ranges from 3 to 300.
    For level 26, it ranges from 5k to 500k."""
    display_name = "Required shapes multiplier"
    rich_text_doc = True
    range_start = 1
    range_end = 100
    default = 10


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
    order is cutter, rotator, painter, color mixer, and stacker.

    - **Vanilla:** Level 1 requires nothing, 2-4 require the first building, 5-6 require also the second, 7-8 the
    third, 9-10 the fourth, and 11 and onwards all buildings.
    - **Stretched:** After every floor(maxlevel/6) levels, another building is required.
    - **Quick:** Every Level, except level 1, requires another building, with level 6 and onwards requiring all
    buildings.
    - **Random steps:** After a random amount of levels, another building is required, with level 1 always requiring none.
    This can potentially behave like any other option.
    - **Hardcore:** All levels (except level 1) have completely random shape requirements and thus require all
    buildings. Expect early BKs."""
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
    default = 2


class RandomizeUpgradeLogic(Choice):
    """If upgrade requirements are randomized, this sets how those random shapes are generated
    and how logic works for upgrades. All four categories will have the same logic.

    - **Vanilla-like:** Tier II requires up to two random buildings, III requires up to three random buildings,
    and IV and onwards require all processing buildings.
    - **Linear:** Tier II requires nothing, III-VI require another random building each,
    and VII and onwards require all buildings.
    - **Category:** Belt and miner upgrades require no building, processors upgrades require the cutter (all tiers),
    rotator (tier IV and onwards), and stacker (tier VI and onwards, and painting upgrades require the cutter, rotator,
    stacker, painter (all tiers) and color mixer (tiers V and onwards). Tier VII and onwards will always require all
    buildings.
    - **Category random:** Each upgrades category (all tiers each) requires a random amount of buildings (in order),
    with one category always requiring no buildings.Tier VII and onwards will always require all buildings.
    - **Hardcore:** All tiers (except each tier II) have completely random shape requirements. Expect early BKs."""
    display_name = "Randomize upgrade logic"
    rich_text_doc = True
    option_vanilla_like = 0
    option_linear = 1
    option_category = 2
    option_category_random = 3
    option_hardcore = 4
    default = 1


class ThroughputLevelsRatio(Range):
    """If level requirements are randomized, this sets the ratio of how many levels (approximately) will require either
    a total amount or per second amount (throughput) of shapes delivered.
    0 means only total, 100 means only throughput, and -1 means vanilla (only levels 14, 27 and beyond have throughput).
    """
    display_name = "Throughput levels ratio"
    rich_text_doc = True
    range_start = -1
    range_end = 100
    default = 0


class SameLateUpgradeRequirements(Toggle):
    """If upgrade requirements are randomized, should the last 3 shapes for each category be the same,
    like in vanilla?"""
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
    """Locks Belts and Extractors and adds them into the item pool.
    **Be careful with this option, as every single location in this game needs both of them.**"""
    display_name = "Lock Belt and Extractor"
    rich_text_doc = True
    default = False


# class AdditionalLocations(Choice):
#    """Achievements: Include up to 44 achievements (depending on other options) as additional locations.
#    Shapesanity: Include up to 5664 shapes as additional locations."""
#    display_name = "Additional locations"
#    option_achievements = 0
#    option_shapesanity = 1
#    option_both = 2
#    default = 0


# class ExcludeSoftlockAchievements(Toggle):
#    """Exclude 6 achievements, that can become unreachable in a save file, if not achieved until a certain level."""
#    display_name = "Exclude softlock achievements"
#    default = True


# class ExcludeLongPlaytimeAchievements(Toggle):
#    """Exclude 2 achievements, that require actively playing for a really long time."""
#    display_name = "Exclude long playtime achievements"
#    default = True


# class ExcludeProgressionUnreasonable(Toggle):
#    """Exclude progression and useful items from being placed into softlock and long playtime achievements."""
#    display_name = "Exclude progression items in softlock and long playtime achievements"
#    default = True


class ShapesanityAmount(Range):
    """Amount of one-layer-shapes that will be included as locations."""
    display_name = "Shapesanity amount"
    rich_text_doc = True
    range_start = 4
    range_end = 5664
    default = 100


class TrapsProbability(Range):
    """The probability of any filler item (in percent) being replaced by a trap."""
    display_name = "Traps Percentage"
    rich_text_doc = True
    range_start = 0
    range_end = 100
    default = 0


@dataclass
class ShapezOptions(PerGameCommonOptions):
    goal: Goal
    goal_amount: GoalAmount
    required_shapes_multiplier: RequiredShapesMultiplier
    randomize_level_requirements: RandomizeLevelRequirements
    randomize_upgrade_requirements: RandomizeUpgradeRequirements
    randomize_level_logic: RandomizeLevelLogic
    randomize_upgrade_logic: RandomizeUpgradeLogic
    throughput_levels_ratio: ThroughputLevelsRatio
    same_late_upgrade_requirements: SameLateUpgradeRequirements
    early_balancer_tunnel_and_trash: EarlyBalancerTunnelAndTrash
    lock_belt_and_extractor: LockBeltAndExtractor
    # additional_locations: AdditionalLocations
    # exclude_softlock_achievements: ExcludeSoftlockAchievements
    # exclude_long_playtime_achievements: ExcludeLongPlaytimeAchievements
    # exclude_progression_unreasonable: ExcludeProgressionUnreasonable
    shapesanity_amount: ShapesanityAmount
    traps_percentage: TrapsProbability
#    include_background_music: IncludeBackgroundMusic

