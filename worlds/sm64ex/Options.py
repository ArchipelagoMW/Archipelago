import typing
from Options import Option, DefaultOnToggle, Range, Toggle

class EnableCoinStars(DefaultOnToggle):
    """Disable to Ignore 100 Coin Stars. You can still collect them, but they don't do anything"""
    display_name = "Enable 100 Coin Stars"

class StrictCapRequirements(DefaultOnToggle):
    """If disabled, Stars that expect special caps may have to be acquired without the caps"""
    display_name = "Strict Cap Requirements"

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
    displayname = "Course Randomizer"

sm64_options: typing.Dict[str,type(Option)] = {
    "AreaRandomizer": AreaRandomizer,
    "EnableCoinStars": EnableCoinStars,
    "StrictCapRequirements": StrictCapRequirements,
    "StarsToFinish": StarsToFinish,
    "ExtraStars": ExtraStars
} 