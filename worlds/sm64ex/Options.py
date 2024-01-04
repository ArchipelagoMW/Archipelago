import typing
from Options import Option, DefaultOnToggle, Range, Toggle, DeathLink, Choice
from .Items import action_item_table

class EnableCoinStars(DefaultOnToggle):
    """Disable to Ignore 100 Coin Stars. You can still collect them, but they don't do anything.
    Removes 15 locations from the pool."""
    display_name = "Enable 100 Coin Stars"


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


class ExclamationBoxes(Choice):
    """Include 1Up Exclamation Boxes during randomization.
    Adds 29 locations to the pool."""
    display_name = "Randomize 1Up !-Blocks"
    option_Off = 0
    option_1Ups_Only = 1


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

def getMoveRandomizerOption(action: str):
    class MoveRandomizerOption(Toggle):
        """Mario is unable to perform this action until a corresponding item is picked up.
        This option is incompatible with builds using a 'nomoverando' branch."""
        display_name = f"Randomize {action}"
    return MoveRandomizerOption


sm64_options: typing.Dict[str, type(Option)] = {
    "AreaRandomizer": AreaRandomizer,
    "BuddyChecks": BuddyChecks,
    "ExclamationBoxes": ExclamationBoxes,
    "ProgressiveKeys": ProgressiveKeys,
    "EnableCoinStars": EnableCoinStars,
    "StrictCapRequirements": StrictCapRequirements,
    "StrictCannonRequirements": StrictCannonRequirements,
    "StrictMoveRequirements": StrictMoveRequirements,
    "AmountOfStars": AmountOfStars,
    "FirstBowserStarDoorCost": FirstBowserStarDoorCost,
    "BasementStarDoorCost": BasementStarDoorCost,
    "SecondFloorStarDoorCost": SecondFloorStarDoorCost,
    "MIPS1Cost": MIPS1Cost,
    "MIPS2Cost": MIPS2Cost,
    "StarsToFinish": StarsToFinish,
    "death_link": DeathLink,
    "CompletionType": CompletionType,
}

for action in action_item_table:
    # HACK: Disable randomization of double jump
    if action == 'Double Jump': continue
    sm64_options[f"MoveRandomizer{action.replace(' ','')}"] = getMoveRandomizerOption(action)
