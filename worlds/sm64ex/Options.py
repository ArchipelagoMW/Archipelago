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

class BLJLogic(Choice):
    """Determine if and how BLJs (Backwards Long Jumps) are treated in logic.
    (Currently only adds BLJs for the most well-known ones inside the castle. Other BLJ skips may or may not be added in the future.)

    Vanilla - BLJs are not required, and are considered as Out of Logic.

    LBLJ - LBLJ (Lobby BLJ) is required and considered as In Logic.
    It is the skip to bypass the first Bowser door star requirment. This option will also include BBLJ, US BLJ, and IS BLJ.

    BBLJ - BBLJ (Basement BLJ) is required and considered as In Logic.
    It is the skip to bypass the second Bowser door star requirement.
    It also expects you to skip the Dire Dire Docks painting (possible with enough speed).
    This option will also include US BLJ and IS BLJ.

    US_BLJ - US BLJ (Upstairs Staircase BLJ) is required and considered as In Logic.
    It is the skip to bypass the door to the third floor's star requirement. This option will also include IS BLJ.

    IS_BLJ - IS BLJ (Infinite Stairs BLJ) is required and considered as In Logic.
    It is the skip to bypass the infinite stairs star requirement. This option won't include any other BLJ.

    Turning on any BLJ option will most likely lower how much of the game you need to complete, especially LBLJ.
    Consider turning on area randomizer, move randomizer, locked paintings, progressive keys and all Bowser stages set as your goal to increase the possibility
    of more needed overall game completion and a more varied experience when using BLJ logic.
    Or don't for runs that are expected to be quick.
    """
    display_name = "BLJ Logic"
    option_Vanilla = 0
    option_LBLJ = 1
    option_BBLJ = 2
    option_US_BLJ = 3
    option_IS_BLJ = 4

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
        BLJLogic,
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
    amount_of_stars: AmountOfStars
    first_bowser_star_door_cost: FirstBowserStarDoorCost
    basement_star_door_cost: BasementStarDoorCost
    second_floor_star_door_cost: SecondFloorStarDoorCost
    mips1_cost: MIPS1Cost
    mips2_cost: MIPS2Cost
    stars_to_finish: StarsToFinish
    death_link: DeathLink
    completion_type: CompletionType
    blj_logic: BLJLogic
