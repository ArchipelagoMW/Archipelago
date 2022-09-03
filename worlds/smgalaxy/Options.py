import typing
from Options import Choice, Option, Toggle, DefaultOnToggle, Range, OptionList


class EnablePurpleCoinStars(DefaultOnToggle):
    """tuning this off we allow purple coin stars to count as checks do note all purple coin stars are postgame only but one."""
    display_name = "Disable Purple Coin Stars"

smg_options: typing.Dict[str, type(DefaultOnToggle)] = {
    "EnablePurpleCoinStars": EnablePurpleCoinStars,

}
