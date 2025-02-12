from dataclasses import dataclass

from Options import Choice, Range, Toggle, DeathLink, DefaultOnToggle, OptionGroup, PerGameCommonOptions


class Goal(Choice):
    """
    Determines the goal of the seed

    Final Battle: Beat Boss Cass in Final Battle and rescue your parents from The Dreaming
    """
    display_name = "Goal"
    option_final_battle = 0
    default = 0


class GoalRequiresBosses(Toggle):
    """
    Determines if beating all bosses is a requirement to complete the goal
    """
    display_name = "Goal Requires Bosses"


class LogicDifficulty(Choice):
    """
    What set of logic to use

    Standard: The logic assumes elemental rangs are required to enter hubs

    Advanced: Assumes hubs may be entered early and elemental rangs are optional
    """
    display_name = "Logic Difficulty"
    option_standard = 0
    option_advanced = 1
    default = 0


class ProgressiveElementals(DefaultOnToggle):
    """
    Determines if elemental rangs are a progressive check
    """
    display_name = "Progressive Elemental Rangs"


class StartWithBoom(DefaultOnToggle):
    """
    Determines if Ty starts with his boomerang (only for progressive elementals)
    """
    display_name = "Start With Boomerang"


class LevelShuffle(Toggle):
    """
    Determines whether the levels that portals lead to will be shuffled
    """
    display_name = "Level Shuffle"


class BossShuffle(Toggle):
    """
    Determines whether the first three bosses will be shuffled
    """
    display_name = "Boss Shuffle"


class LevelUnlockStyle(Choice):
    """
    Determines how levels are unlocked

    Vanilla: All levels are unlocked from the start of the world

    Checks: The first level is unlocked from the start but all other levels are unlocked via checks

    Checks - No Bosses: The first level is unlocked from the start. Bosses are unlocked via hub Thunder Egg counts. All other levels are unlocked via checks
    """
    display_name = "Level Unlock Style"
    option_vanilla = 0
    option_checks = 1
    option_checks_no_bosses = 2
    default = 1


class ProgressiveLevel(DefaultOnToggle):
    """
    Determines if level unlocks are progressive (only if levels are check based)
    """
    display_name = "Progressive Level"


class ThunderEggGating(Range):
    """
    If bosses are unlocked via hub Thunder Egg counts, required count per hub can be set here
    This also sets the required Thunder Egg count to receive the elemental attribute check after completing bosses
    """
    display_name = "Thunder Egg Gating"
    range_start = 0
    range_end = 24
    default = 17


class ExtraThunderEggs(Range):
    """
    Sets number of additional thunder eggs of each type to add to the pool
    WARNING - Setting this value high without sanity is likely to lead to generation failures
    """
    display_name = "Extra Thunder Eggs"
    range_start = 0
    range_end = 24
    default = 7


class CogGating(Range):
    """
    Cog requirement count for each attribute check in Julius' lab
    """
    display_name = "Cog Gating"
    range_start = 0
    range_end = 15
    default = 10


class ExtraCogs(Range):
    """
    Sets number of additional golden cogs to add to the pool
    WARNING - Setting this value high without sanity is likely to lead to generation failures
    """
    display_name = "Extra Cogs"
    range_start = 0
    range_end = 90
    default = 30


class GateTimeAttacks(Toggle):
    """
    If true, adds Stopwatch items to the pool which unlock the time attacks for each level
    If false, time attacks are unlocked by completing the main objective thunder egg check for the level (vanilla)
    Also adds checks for beating specific times in the time attacks
    """
    display_name = "Gate Time Attacks"


class Framesanity(Choice):
    """
    Determines how collecting Picture Frames grants checks

    All: Every frame grants a check (127 Locations - Bonus Worlds not included)

    Per Level: Collecting all frames in a level grants a check (9 Locations - Bonus Worlds not included)

    None: Frames do not grant any checks
    """
    display_name = "Framesanity"
    option_all = 0
    option_per_level = 1
    option_none = 2
    default = 0


class FramesRequireInfra(Toggle):
    """
    Determines whether the generator considers picture frames checks to be logically locked behind the infrarang
    """
    display_name = "Frames Require Infra"


class Scalesanity(Toggle):
    """
    Determines whether each rainbow scale grants a check as well as the attribute check for finding all 25. Also adds extra health to the pool.
    """
    display_name = "Scalesanity"


ty1_option_groups = [
    OptionGroup("Goal Options", [
        Goal,
        GoalRequiresBosses,
    ]),
    OptionGroup("Logic Options", [
        LogicDifficulty,
        ProgressiveElementals,
        StartWithBoom,
        FramesRequireInfra,
        ThunderEggGating,
        ExtraThunderEggs,
        CogGating,
        ExtraCogs,
        LevelShuffle,
        BossShuffle,
        LevelUnlockStyle,
        ProgressiveLevel,
        GateTimeAttacks,
    ]),
    OptionGroup("Sanity Options", [
        Framesanity,
        Scalesanity,
    ]),
    OptionGroup("Death Link", [
        DeathLink
    ]),
]


@dataclass
class Ty1Options(PerGameCommonOptions):
    goal: Goal
    req_bosses: GoalRequiresBosses

    logic_difficulty: LogicDifficulty
    progressive_elementals: ProgressiveElementals
    start_with_boom: StartWithBoom

    thegg_gating: ThunderEggGating
    extra_theggs: ExtraThunderEggs
    cog_gating: CogGating
    extra_cogs: ExtraCogs
    gate_time_attacks: GateTimeAttacks

    level_shuffle: LevelShuffle
    boss_shuffle: BossShuffle
    level_unlock_style: LevelUnlockStyle
    progressive_level: ProgressiveLevel

    framesanity: Framesanity
    frames_require_infra: FramesRequireInfra
    scalesanity: Scalesanity

    death_link: DeathLink
