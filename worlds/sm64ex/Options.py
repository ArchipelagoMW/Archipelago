import typing
from dataclasses import dataclass
from Options import DefaultOnToggle, Range, Toggle, DeathLink, Choice, PerGameCommonOptions, OptionSet, OptionGroup
from .Items import action_item_data_table

class EnableCoinStars(Choice):
    """
    Determine logic for 100 Coin Stars.

    Off - Removed from pool. You can still collect them, but they don't do anything.
    Optimal for ignoring 100 Coin Stars entirely. Removes 15 locations from the pool.

    On - Kept in pool, potentially randomized.

    Vanilla - Kept in pool, but NOT randomized.
    """
    display_name = "Enable 100 Coin Stars"
    option_off = 0
    option_on = 1
    option_vanilla = 2

class EnableLockedPaintings(Toggle):
    """
    Determine how paintings are treated.

    Off - Paintings are not locked, as long as you can access them you can enter them (Vanilla behavior).

    On - Paintings (other than BoB) start off locked and 11 stars are replaced in the pool with items to allow access to them.
    Attempting to enter a locked painting will simply kick Mario out.
    Does not affect secrets and levels that don't have a painting (BBH, HMC, RR).
    This only affects the ability for Mario to enter a painting, the destination of the painting may change due to Entrance Randomization, if it is enabled.
    """
    display_name = "Enable Locked Paintings"

class OneUpFillerProportion(Range):
    """
    Adds 1-Ups to the item pool.

    The value you set here is a proportion. The total number of filler items is split according to the combined proportions of health restores, traps, and 1-Ups.
    """
    display_name = "1Up Filler Proportion"
    range_start = 0
    range_end = 100
    default = 100

class OneHealthPipFillerProportion(Range):
    """
    Set the proportion of 1-pip health restore filler in the filler item pool.

    Mario's total health bar is 8 pips, these items restore 1 pip.

    The value you set here is a proportion. The total number of filler items is split according to the relative proportions of all filler items.
    """
    display_name = "One Health Pip Filler Proportion"
    range_start = 0
    range_end = 100
    default = 0

class TwoHealthPipFillerProportion(Range):
    """
    Set the proportion of 2-pip health restore filler in the filler item pool.

    Mario's total health bar is 8 pips, these items restore 2 pips.

    The value you set here is a proportion. The total number of filler items is split according to the relative proportions of all filler items.
    """
    display_name = "Two Health Pip Filler Proportion"
    range_start = 0
    range_end = 100
    default = 0

class ThreeHealthPipFillerProportion(Range):
    """
    Set the proportion of 3-pip health restore filler in the filler item pool.

    Mario's total health bar is 8 pips, these items restore 3 pips.

    The value you set here is a proportion. The total number of filler items is split according to the relative proportions of all filler items.
    """
    display_name = "Three Health Pip Filler Proportion"
    range_start = 0
    range_end = 100
    default = 0

class FourHealthPipFillerProportion(Range):
    """
    Set the proportion of 4-pip health restore filler in the filler item pool.

    Mario's total health bar is 8 pips, these items restore 4 pips.

    The value you set here is a proportion. The total number of filler items is split according to the relative proportions of all filler items.
    """
    display_name = "Four Health Pip Filler Proportion"
    range_start = 0
    range_end = 100
    default = 0

class FullRestoreFillerProportion(Range):
    """
    Set the proportion of full health restore filler in the filler item pool.

    Mario's total health bar is 8 pips, these items fully restore Mario's health.

    The value you set here is a proportion. The total number of filler items is split according to the relative proportions of all filler items.
    """
    display_name = "Full Health Filler Proportion"
    range_start = 0
    range_end = 100
    default = 0

class BonkTrapFillerProportion(Range):
    """
    Set the proportion of bonk trap filler in the filler item pool.
    
    Bonk traps stop Mario in place and shove him in a random direction.

    The value you set here is a proportion. The total number of filler items is split according to the combined proportions of health restores, traps, and 1-Ups.
    """
    display_name = "Bonk Trap Filler Proportion"
    range_start = 0
    range_end = 100
    default = 0

class FireTrapFillerProportion(Range):
    """
    Set the proportion of fire trap filler in the filler item pool.
    
    Fire traps set Mario on fire, causing him to run uncontrollably.

    The value you set here is a proportion. The total number of filler items is split according to the combined proportions of health restores, traps, and 1-Ups.
    """
    display_name = "Fire Trap Filler Proportion"
    range_start = 0
    range_end = 100
    default = 0

class AmpTrapFillerProportion(Range):
    """
    Set the proportion of fire trap filler in the filler item pool.
    
    Amp traps shock Mario, like an Amp does, and take some health.

    The value you set here is a proportion. The total number of filler items is split according to the combined proportions of health restores, traps, and 1-Ups.
    """
    display_name = "Amp Trap Filler Proportion"
    range_start = 0
    range_end = 100
    default = 0

class ChuckyaTrapFillerProportion(Range):
    """
    Set the proportion of Chuckya trap filler in the filler item pool.
    
    Chuckya traps throw Mario in a random direction.

    The value you set here is a proportion. The total number of filler items is split according to the combined proportions of health restores, traps, and 1-Ups.
    """
    display_name = "Chuckya Trap Filler Proportion"
    range_start = 0
    range_end = 100
    default = 0

class SpinTrapFillerProportion(Range):
    """
    Set the proportion of spin trap filler in the filler item pool.
    
    Spin traps spin Mario up into the air like a Tweester.

    The value you set here is a proportion. The total number of filler items is split according to the combined proportions of health restores, traps, and 1-Ups.
    """
    display_name = "Spin Trap Filler Proportion"
    range_start = 0
    range_end = 100
    default = 0

class GustTrapFillerProportion(Range):
    """
    Set the proportion of gust trap filler in the filler item pool.
    
    Gust traps blow Mario away in a random direction like the giant snowman in Snowman's Land.

    The value you set here is a proportion. The total number of filler items is split according to the combined proportions of health restores, traps, and 1-Ups.
    """
    display_name = "Gust Trap Filler Proportion"
    range_start = 0
    range_end = 100
    default = 0

class StrictCapRequirements(DefaultOnToggle):
    """If disabled, Stars that expect special caps may have to be acquired without the caps"""
    display_name = "Strict Cap Requirements"


class StrictCannonRequirements(DefaultOnToggle):
    """If disabled, Stars that expect cannons may have to be acquired without them.
    Has no effect if Buddy Checks and Move Randomizer are disabled"""
    display_name = "Strict Cannon Requirements"


class FirstBowserStarDoorCost(Range):
    """What percent of the total stars are required at the Star Door to Bowser in the Dark World"""
    display_name = "First Star Door Cost %"
    range_start = 0
    range_end = 40
    default = 7


class BasementStarDoorCost(Range):
    """What percent of the total stars are required at the Star Door in the Basement"""
    display_name = "Basement Star Door %"
    range_start = 0
    range_end = 50
    default = 25


class SecondFloorStarDoorCost(Range):
    """What percent of the total stars are required to access the third floor"""
    display_name = 'Second Floor Star Door %'
    range_start = 0
    range_end = 70
    default = 42


class MIPS1Cost(Range):
    """What percent of the total stars are required to spawn MIPS the first time"""
    display_name = "MIPS 1 Star %"
    range_start = 0
    range_end = 35
    default = 12


class MIPS2Cost(Range):
    """What percent of the total stars are required to spawn MIPS the second time."""
    display_name = "MIPS 2 Star %"
    range_start = 0
    range_end = 70
    default = 42


class StarsToFinish(Range):
    """What percent of the total stars are required at the infinite stairs"""
    display_name = "Endless Stairs Star %"
    range_start = 0
    range_end = 90
    default = 58


class AmountOfStars(Range):
    """How many stars exist.
    If there aren't enough locations to hold the given total, the total will be reduced."""
    display_name = "Total Power Stars"
    range_start = 35
    range_end = 120
    default = 120


class AreaRandomizer(Choice):
    """Randomize Entrances"""
    display_name = "Entrance Randomizer"
    option_Off = 0
    option_Courses_Only = 1
    option_Courses_and_Secrets_Separate = 2
    option_Courses_and_Secrets = 3


class BuddyChecks(Toggle):
    """Bob-omb Buddies are checks, Cannon Unlocks are items"""
    display_name = "Bob-omb Buddy Checks"


class ExclamationBoxes(Toggle):
    """Include 1Up Exclamation Boxes during randomization.
    Adds 29 locations to the pool."""
    display_name = "Randomize 1Up !-Blocks"
    alias_1Ups_Only = 1


class CompletionType(Choice):
    """Set goal for game completion"""
    display_name = "Completion Goal"
    option_Last_Bowser_Stage = 0
    option_All_Bowser_Stages = 1


class ProgressiveKeys(DefaultOnToggle):
    """Keys will first grant you access to the Basement, then to the Second Floor"""
    display_name = "Progressive Keys"

class StrictMoveRequirements(DefaultOnToggle):
    """If disabled, Stars that expect certain moves may have to be acquired without them. Only makes a difference
    if Move Randomization is enabled"""
    display_name = "Strict Move Requirements"

class EnableMoveRandomizer(Toggle):
    """Mario is unable to perform some actions until a corresponding item is picked up.
    This option is incompatible with builds using a 'nomoverando' branch.
    Specific actions to randomize can be specified in the YAML."""
    display_name = "Enable Move Randomizer"

class MoveRandomizerActions(OptionSet):
    """Which actions to randomize when Move Randomizer is enabled"""
    display_name = "Randomized Moves"
    # HACK: Disable randomization for double jump
    valid_keys = [action for action in action_item_data_table if action != 'Double Jump']
    default = valid_keys

sm64_options_groups = [
    OptionGroup("Logic Options", [
        AreaRandomizer,
        BuddyChecks,
        ExclamationBoxes,
        ProgressiveKeys,
        EnableCoinStars,
        EnableLockedPaintings,
        StrictCapRequirements,
        StrictCannonRequirements,
    ]),
    OptionGroup("Ability Options", [
        EnableMoveRandomizer,
        MoveRandomizerActions,
        StrictMoveRequirements,
    ]),
    OptionGroup("Star Options", [
        AmountOfStars,
        FirstBowserStarDoorCost,
        BasementStarDoorCost,
        SecondFloorStarDoorCost,
        MIPS1Cost,
        MIPS2Cost,
        StarsToFinish,
    ]),
    OptionGroup("Filler Options", [
        OneUpFillerProportion,
        OneHealthPipFillerProportion,
        TwoHealthPipFillerProportion,
        ThreeHealthPipFillerProportion,
        FourHealthPipFillerProportion,
        FullRestoreFillerProportion,
        BonkTrapFillerProportion,
        FireTrapFillerProportion,
        AmpTrapFillerProportion,
        ChuckyaTrapFillerProportion,
        SpinTrapFillerProportion,
        GustTrapFillerProportion,
    ]),
]

@dataclass
class SM64Options(PerGameCommonOptions):
    area_rando: AreaRandomizer
    buddy_checks: BuddyChecks
    exclamation_boxes: ExclamationBoxes
    progressive_keys: ProgressiveKeys
    enable_coin_stars: EnableCoinStars
    enable_locked_paintings: EnableLockedPaintings
    enable_move_rando: EnableMoveRandomizer
    move_rando_actions: MoveRandomizerActions
    strict_cap_requirements: StrictCapRequirements
    strict_cannon_requirements: StrictCannonRequirements
    strict_move_requirements: StrictMoveRequirements
    one_up_filler_proportion: OneUpFillerProportion
    one_health_pip_filler_proportion: OneHealthPipFillerProportion
    two_health_pip_filler_proportion: TwoHealthPipFillerProportion
    three_health_pip_filler_proportion: ThreeHealthPipFillerProportion
    four_health_pip_filler_proportion: FourHealthPipFillerProportion
    full_restore_filler_proportion: FullRestoreFillerProportion
    bonk_trap_filler_proportion: BonkTrapFillerProportion
    fire_trap_filler_proprtion: FireTrapFillerProportion
    amp_trap_filler_proportion: AmpTrapFillerProportion
    chukya_trap_filler_proportion: ChuckyaTrapFillerProportion
    spin_trap_filler_proportion: SpinTrapFillerProportion
    gust_trap_filler_proportion: GustTrapFillerProportion
    amount_of_stars: AmountOfStars
    first_bowser_star_door_cost: FirstBowserStarDoorCost
    basement_star_door_cost: BasementStarDoorCost
    second_floor_star_door_cost: SecondFloorStarDoorCost
    mips1_cost: MIPS1Cost
    mips2_cost: MIPS2Cost
    stars_to_finish: StarsToFinish
    death_link: DeathLink
    completion_type: CompletionType
