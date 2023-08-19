import typing
from Options import Option, DefaultOnToggle, Range, Toggle, DeathLink, Choice


class EnableCoinStars(DefaultOnToggle):
    """Disable to Ignore 100 Coin Stars. You can still collect them, but they don't do anything"""
    display_name = "Enable 100 Coin Stars"


class StrictCapRequirements(DefaultOnToggle):
    """If disabled, Stars that expect special caps may have to be acquired without the caps"""
    display_name = "Strict Cap Requirements"


class StrictCannonRequirements(DefaultOnToggle):
    """If disabled, Stars that expect cannons may have to be acquired without them. Only makes a difference if Buddy
    Checks are enabled"""
    display_name = "Strict Cannon Requirements"


class FirstBowserStarDoorCost(Range):
    """How many stars are required at the Star Door to Bowser in the Dark World"""
    range_start = 0
    range_end = 50
    default = 8


class BasementStarDoorCost(Range):
    """How many stars are required at the Star Door in the Basement"""
    range_start = 0
    range_end = 70
    default = 30


class SecondFloorStarDoorCost(Range):
    """How many stars are required to access the third floor"""
    range_start = 0
    range_end = 90
    default = 50


class MIPS1Cost(Range):
    """How many stars are required to spawn MIPS the first time"""
    range_start = 0
    range_end = 40
    default = 15


class MIPS2Cost(Range):
    """How many stars are required to spawn MIPS the second time."""
    range_start = 0
    range_end = 80
    default = 50


class StarsToFinish(Range):
    """How many stars are required at the infinite stairs"""
    display_name = "Endless Stairs Stars"
    range_start = 0
    range_end = 100
    default = 70


class AmountOfStars(Range):
    """How many stars exist. Disabling 100 Coin Stars removes 15 from the Pool. At least max of any Cost set"""
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
    """Include 1Up Exclamation Boxes during randomization"""
    display_name = "Randomize 1Up !-Blocks"
    option_Off = 0
    option_1Ups_Only = 1

class CompletionType(Choice):
    """Set goal for game completion"""
    display_name = "Completion Goal"
    option_Last_Bowser_Stage = 0
    option_All_Bowser_Stages = 1


class ProgressiveKeys(DefaultOnToggle):
    """Keys will first grant you access to the Basement, then to the Secound Floor"""
    display_name = "Progressive Keys"


sm64_options: typing.Dict[str, type(Option)] = {
    "AreaRandomizer": AreaRandomizer,
    "ProgressiveKeys": ProgressiveKeys,
    "EnableCoinStars": EnableCoinStars,
    "AmountOfStars": AmountOfStars,
    "StrictCapRequirements": StrictCapRequirements,
    "StrictCannonRequirements": StrictCannonRequirements,
    "FirstBowserStarDoorCost": FirstBowserStarDoorCost,
    "BasementStarDoorCost": BasementStarDoorCost,
    "SecondFloorStarDoorCost": SecondFloorStarDoorCost,
    "MIPS1Cost": MIPS1Cost,
    "MIPS2Cost": MIPS2Cost,
    "StarsToFinish": StarsToFinish,
    "death_link": DeathLink,
    "BuddyChecks": BuddyChecks,
    "ExclamationBoxes": ExclamationBoxes,
    "CompletionType" : CompletionType,
}
