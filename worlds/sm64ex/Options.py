import typing
from Options import Option, DefaultOnToggle, Range

class EnableCoinStars(DefaultOnToggle):
    """Disable to Ignore 100 Coin Stars. You can still collect them, but they don't do anything"""
    displayname = "Enable 100 Coin Stars"

class StrictCapRequirements(DefaultOnToggle):
    """If disabled, Stars that expect special caps may have to be acquired without the caps"""
    displayname = "Strict Cap Requirements"

class StarsToFinish(Range):
    """How many stars are required at the infinite stairs"""
    range_start = 50
    range_end = 100
    default = 70

sm64_options: typing.Dict[str,type(Option)] = {
    "EnableCoinStars": EnableCoinStars,
    "StrictCapRequirements": StrictCapRequirements,
    "StarsToFinish": StarsToFinish
} 