import typing
from Options import Option, DefaultOnToggle, Range, Toggle, DeathLink, Choice

class EnableCoinStars(DefaultOnToggle):
    """Disable to Ignore 100 Coin Stars. You can still collect them, but they don't do anything"""
    display_name = "Enable 100 Coin Stars"

class StrictCapRequirements(DefaultOnToggle):
    """If disabled, Stars that expect special caps may have to be acquired without the caps"""
    display_name = "Strict Cap Requirements"

class StrictCannonRequirements(DefaultOnToggle):
    """If disabled, Stars that expect cannons may have to be acquired without them. Only makes a difference if Buddy Checks are enabled"""
    display_name = "Strict Cannon Requirements"

class FirstBowserStarDoorCost(Range):
    """How many stars are required at the Star Door to Bowser in the Dark World"""
    range_start = 0
    range_end = 20
    default = 8

class BasementStarDoorCost(Range):
    """How many stars are required at the Star Door in the Basement"""
    range_start = 0
    range_end = 50
    default = 30

class SecondFloorStarDoorCost(Range):
    """How many stars are required to access the third floor"""
    range_start = 0
    range_end = 50
    default = 50

class StarsToFinish(Range):
    """How many stars are required at the infinite stairs"""
    display_name = "Endless Stairs Stars"
    range_start = 0
    range_end = 100
    default = 70

class ExtraStars(Range):
    """How many stars exist beyond those set for StarsToFinish"""
    range_start = 0
    range_end = 50
    default = 50

class AreaRandomizer(Choice):
    """Randomize Entrances"""
    display_name = "Entrance Randomizer"
    alias_false = 0
    option_Off = 0
    option_Courses_Only = 1
    option_Courses_and_Secrets = 2

class BuddyChecks(Toggle):
    """Bob-omb Buddies are checks, Cannon Unlocks are items"""
    display_name = "Bob-omb Buddy Checks"

class ProgressiveKeys(DefaultOnToggle):
    """Keys will first grant you access to the Basement, then to the Secound Floor"""
    display_name = "Progressive Keys"

sm64_options: typing.Dict[str,type(Option)] = {
    "AreaRandomizer": AreaRandomizer,
    "ProgressiveKeys": ProgressiveKeys,
    "EnableCoinStars": EnableCoinStars,
    "StrictCapRequirements": StrictCapRequirements,
    "StrictCannonRequirements": StrictCannonRequirements,
    "FirstBowserStarDoorCost": FirstBowserStarDoorCost,
    "BasementStarDoorCost": BasementStarDoorCost,
    "SecondFloorStarDoorCost": SecondFloorStarDoorCost,
    "StarsToFinish": StarsToFinish,
    "ExtraStars": ExtraStars,
    "death_link": DeathLink,
    "BuddyChecks": BuddyChecks,
} 