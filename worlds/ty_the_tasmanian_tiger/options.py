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
    Determines if beating all bosses is a requirement to go to Final Battle
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


class LevelShuffle(Toggle):
    """
    Determines whether the levels that portals lead to will be shuffled
    """
    display_name = "Level Shuffle"


class LevelUnlockStyle(Choice):
    """
    Determines how levels are unlocked

    Vanilla: All levels are unlocked from the start of the world

    Checks: The first level is unlocked from the start but all other levels are unlocked via checks

    Checks - No Bosses: The first level will be unlocked from the start. Bosses can be unlocked via hub Thunder Egg counts. All other levels must be unlocked via checks
    """
    display_name = "Level Unlock Style"
    option_vanilla = 0
    option_checks = 1
    option_checks_no_bosses = 2
    default = 2


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
    default = 2


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


class Signsanity(Toggle):
    """
    Determines whether hitting each Maurie signpost with a boomerang grants a check.
    """
    display_name = "Signsanity"


class Lifesanity(Toggle):
    """
    Determines whether each unique extra life grants a check (not including basket lives)
    """
    display_name = "Lifesanity"


class Opalsanity(Toggle):
    """
    Determines whether each opal grants a check
    """
    display_name = "Opalsanity"


class TrapFill(Range):
    """
    Determines the percentage of the junk fill which is filled with traps.
    """
    display_name = "Trap Fill Percentage"
    range_start = 0
    range_end = 100
    default = 0


class AcidTrapWeight(Range):
    """The weight of Acid Traps in the trap pool.
    Acid Traps cause the screen to shift colors."""
    display_name = "Acid Trap Weight"
    range_start = 0
    range_end = 100
    default = 20


class ExitTrapWeight(Range):
    """The weight of Exit Traps in the trap pool.
    Exit Traps immediately force you out of the current level, putting you back in Rainbow Cliffs."""
    display_name = "Exit Trap Weight"
    range_start = 0
    range_end = 100
    default = 20


class GravityTrapWeight(Range):
    """The weight of Gravity Traps in the trap pool.
    Gravity Traps cause Ty to fall much faster, and limit his jump height."""
    display_name = "Gravity Trap Weight"
    range_start = 0
    range_end = 100
    default = 20


class KnockedDownTrapWeight(Range):
    """The weight of Knocked Down Traps in the trap pool.
    Knocked Down Traps knock you over and set your health to 1"""
    display_name = "Knocked Down Trap Weight"
    range_start = 0
    range_end = 100
    default = 20


class SlowTrapWeight(Range):
    """The weight of Slow Traps in the trap pool.
    Slow Traps cause Ty to move slower."""
    display_name = "Slow Trap Weight"
    range_start = 0
    range_end = 100
    default = 20


class MulTyLink(Toggle):
    """Whether other players connecting to the same slot should see each other.
    This is soft limited to 8 players per slot. Use with caution."""
    display_name = "Mul-Ty Link"


ty1_option_groups = [
    OptionGroup("Goal Options", [
        Goal,
        GoalRequiresBosses,
    ]),
    OptionGroup("Logic Options", [
        LogicDifficulty,
        ProgressiveElementals,
        ThunderEggGating,
        ExtraThunderEggs,
        CogGating,
        ExtraCogs,
        LevelUnlockStyle,
        ProgressiveLevel,
        LevelShuffle,
    ]),
    OptionGroup("Sanity Options", [
        GateTimeAttacks,
        Framesanity,
        FramesRequireInfra,
        Scalesanity,
        Signsanity,
        Lifesanity,
        Opalsanity
    ]),
    OptionGroup("Traps", [
        TrapFill,
        AcidTrapWeight,
        ExitTrapWeight,
        GravityTrapWeight,
        KnockedDownTrapWeight,
        SlowTrapWeight
    ]),
    OptionGroup("Death Link", [
        DeathLink
    ]),
    OptionGroup("Mul-Ty Link", [
        MulTyLink
    ])
]


@dataclass
class Ty1Options(PerGameCommonOptions):
    goal: Goal
    req_bosses: GoalRequiresBosses

    logic_difficulty: LogicDifficulty
    progressive_elementals: ProgressiveElementals

    thegg_gating: ThunderEggGating
    extra_theggs: ExtraThunderEggs
    cog_gating: CogGating
    extra_cogs: ExtraCogs
    gate_time_attacks: GateTimeAttacks

    level_shuffle: LevelShuffle
    level_unlock_style: LevelUnlockStyle
    progressive_level: ProgressiveLevel

    framesanity: Framesanity
    frames_require_infra: FramesRequireInfra
    scalesanity: Scalesanity
    signsanity: Signsanity
    lifesanity: Lifesanity
    opalsanity: Opalsanity

    death_link: DeathLink
    trap_fill_percentage: TrapFill
    acid_trap_weight: AcidTrapWeight
    exit_trap_weight: ExitTrapWeight
    gravity_trap_weight: GravityTrapWeight
    knocked_down_trap_weight: KnockedDownTrapWeight
    slow_trap_weight: SlowTrapWeight

    mul_ty_link: MulTyLink
