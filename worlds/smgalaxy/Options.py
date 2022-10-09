import imp
import typing
from Options import Option, DefaultOnToggle


class EnablePurpleCoinStars(DefaultOnToggle):
    """tuning this off we allow purple coin stars to count as checks do note all purple coin stars are postgame only but one."""
    display_name = "Enable Purple Coin Stars"

smg_options: typing.Dict[str, type(Option)] = {
    "EnablePurpleCoinStars": EnablePurpleCoinStars,
}
