import typing
from Options import Option, DefaultOnToggle

class EnableCoinStars(DefaultOnToggle):
    """Disable to Ignore 100 Coin Stars. You can still collect them, but they don't do anything"""
    displayname = "Enable 100 Coin Stars"

class StrictCapRequirements(DefaultOnToggle):
    """If disabled, Stars that expect special caps may have to be acquired without the caps"""
    displayname = "Strict Cap Requirements"

sm64_options: typing.Dict[str,type(Option)] = {
    "EnableCoinStars": EnableCoinStars,
    "StrictCapRequirements": StrictCapRequirements
} 