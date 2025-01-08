import typing
from dataclasses import dataclass
from Options import DefaultOnToggle, Range, Toggle, DeathLink, Choice, PerGameCommonOptions, OptionSet, OptionGroup
from .Items import action_item_table

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
    valid_keys = [action for action in action_item_table if action != 'Double Jump']
    default = valid_keys

sm64_options_groups = [
    OptionGroup("Logic Options", [
        AreaRandomizer,
        BuddyChecks,
        ExclamationBoxes,
        ProgressiveKeys,
        EnableCoinStars,
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
]

@dataclass
class SM64Options(PerGameCommonOptions):
    area_rando: AreaRandomizer
    buddy_checks: BuddyChecks
    exclamation_boxes: ExclamationBoxes
    progressive_keys: ProgressiveKeys
    enable_coin_stars: EnableCoinStars
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
