from dataclasses import dataclass

from Options import Range, Toggle, Choice, PerGameCommonOptions


class Goal(Choice):
    """Vanilla: Complete level 26.
    MAM: Complete a specified level after level 26. Every level before that and a few additional options will be a
          location. It's recommended to build a Make-Anything-Machine (MAM).
    Even fasterer: Upgrade everything to a specified tier after tier 8. Every upgrade before that will be a location.
    Efficiency III: Deliver 500 blueprint shapes per second to the hub."""
    display_name = "Goal"
    option_vanilla = 0
    option_mam = 1
    option_even_fasterer = 2
    option_efficiency_iii = 3
    default = 0


class GoalAmount(Range):
    """Specify, what level or tier (when either MAM or even fasterer is chosen as goal) is required to reach the goal.
    If MAM is set as the goal and this is set to less than 27, it will raise an OptionError."""
    display_name = "Goal amount"
    range_start = 9
    range_end = 1000
    default = 27


class RequiredShapesMultiplier(Range):
    """Multiplies the amount of required shapes for levels and upgrades by value/10.
    For level 1, the amount of shapes ranges from 3 to 300.
    For level 26, it ranges from 5k to 500k."""
    display_name = "Required shapes multiplier"
    range_start = 1
    range_end = 100
    default = 10


class RandomizeLevelRequirements(Toggle):
    """Randomize the required shapes to complete levels."""
    display_name = "Randomize level requirements"
    default = True


class RandomizeUpgradeRequirements(Toggle):
    """Randomize the required shapes to buy upgrades."""
    display_name = "Randomize upgrade requirements"
    default = True


class RandomizeLevelLogic(Choice):
    """If level requirements are randomized, this sets how those random shapes are generated
    and how logic works for levels.
    Vanilla: Level 1 requires nothing, 2-4 require the cutter, 5-6 require the rotator, 7-8 require the painter,
             9-10 require the color mixer, and 11 and onwards require the stacker.
    Shuffled: Same as vanilla, but with shuffled order of buildings.
    Stretched vanilla: After every floor(maxlevel/6) levels, another building is required,
                       with the same order as vanilla.
    Stretched shuffled: Same as stretched vanilla, but with shuffled order of buildings.
    Hardcore: All levels (except level 1) have completely random shape requirements. Expect early BKs."""
    display_name = "Randomize level logic"
    option_vanilla = 0
    option_shuffled = 1
    option_stretched_vanilla = 2
    option_stretched_shuffled = 3
    option_hardcore = 4
    default = 2


class RandomizeUpgradeLogic(Choice):
    """If upgrade requirements are randomized, this sets how those random shapes are generated
    and how logic works for upgrades. All four categories will have the same logic.
    Vanilla-like: Tier II requires up to two random buildings, III requires up to three random buildings,
                  and IV and onwards require all processing buildings.
    Linear: Tier II requires nothing, III-VI require another random building each,
            and VII and onwards require all buildings.
    Hardcore: All tiers (except each tier II) have completely random shape requirements. Expect early BKs."""
    display_name = "Randomize upgrade logic"
    option_vanilla_like = 0
    option_linear = 1
    option_hardcore = 2
    default = 1


class SameLateUpgradeRequirements(Toggle):
    """If upgrade requirements are randomized, should the last 3 shapes for each category
    be the same, like in vanilla?"""
    display_name = "Same late upgrade requirements"
    default = True


# class AdditionalLocations(Choice):
#    """Achievements: Include up to 44 achievements (depending on other options) as additional locations.
#    Shapesanity: Include up to 2144 shapes as additional locations."""
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
    range_start = 0
    range_end = 2144
    default = 100


class TrapsProbability(Range):
    """The probability of any filler item (in percent) being replaced by a trap."""
    display_name = "Traps Percentage"
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
    same_late_upgrade_requirements: SameLateUpgradeRequirements
    # additional_locations: AdditionalLocations
    # exclude_softlock_achievements: ExcludeSoftlockAchievements
    # exclude_long_playtime_achievements: ExcludeLongPlaytimeAchievements
    # exclude_progression_unreasonable: ExcludeProgressionUnreasonable
    shapesanity_amount: ShapesanityAmount
    traps_percentage: TrapsProbability
#    include_background_music: IncludeBackgroundMusic

