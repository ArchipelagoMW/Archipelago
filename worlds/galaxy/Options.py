import typing
from Options import Choice, Option, Toggle, DefaultOnToggle, Range, OptionList, DefaultOffToggle


class EnablePurpleCoinStars(DefaultOffToggle):
    """tuning this on we allow purple coin stars to count as checks do note all purple coin stars are postgame only."""
    display_name = "Enable Purple Coin Stars"

smg_options: typing.Dict[str, Type(Toggle)] = {
    "EnablePurpleCoinStars": EnablePurpleCoinStars,
    
}
