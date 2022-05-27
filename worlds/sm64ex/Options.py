import typing
from Options import Option, DefaultOnToggle, Range, Toggle, DeathLink

class EnableCoinStars(DefaultOnToggle):
    """Disable to Ignore 100 Coin Stars. You can still collect them, but they don't do anything"""
    display_name = "Enable 100 Coin Stars"

class StrictCapRequirements(DefaultOnToggle):
    """If disabled, Stars that expect special caps may have to be acquired without the caps"""
    display_name = "Strict Cap Requirements"

class StrictCannonRequirements(DefaultOnToggle):
    """If disabled, Stars that expect cannons may have to be acquired without them. Only makes a difference if Buddy Checks are enabled"""
    display_name = "Strict Cannon Requirements"

class StarsToFinish(Range):
    """How many stars are required at the infinite stairs"""
    range_start = 50
    range_end = 100
    default = 70

class ExtraStars(Range):
    """How many stars exist beyond those set for StarsToFinish"""
    range_start = 0
    range_end = 50
    default = 50

class AreaRandomizer(Toggle):
    """Randomize Entrances to Courses"""
    display_name = "Course Randomizer"

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
    "StarsToFinish": StarsToFinish,
    "ExtraStars": ExtraStars,
    "death_link": DeathLink,
    "BuddyChecks": BuddyChecks,
} 