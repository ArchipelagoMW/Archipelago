import typing
from Options import Option, DefaultOnToggle

class EnableCoinStars(DefaultOnToggle):
    """Disable to Ignore 100 Coin Stars. You can still collect them, but they don't do anything"""
    displayname = "Enable 100 Coin Stars"

sm64_options: typing.Dict[str,type(Option)] = {
    "EnableCoinStars": EnableCoinStars
} 