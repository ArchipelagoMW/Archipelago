import typing
from Options import Option, DeathLink, Choice

class FalseDoubleJump(Choice):
    """If you can do a double jump without the pack for it (glitch)."""
    internal_name = "double_jump_glitch"
    display_name = "Double Jump glitch"
    option_none = 0
    option_simple = 1
    option_all = 2
    default = 0

class TimeIsMoney(Choice):
    """Is your time worth the money, are you ready to grind your sword by hand?"""
    internal_name = "time_is_money"
    display_name = "Time Is Money"
    option_I_want_speed = 0
    option_I_can_grind = 1
    default = 0


class CoinSanity(Choice):
    """This is for the insane it can be 825 check, it is coin sanity"""
    internal_name = "coin_sanity"
    display_name = "Coin Sanity"
    option_none = 0
    option_region = 1
    option_coin = 2
    default = 0


DLCquest_options: typing.Dict[str,type(Option)] = {
    "double_jump_glitch": FalseDoubleJump,
    "coin_sanity": CoinSanity,
    "time_is_money": TimeIsMoney,
    "death_link": DeathLink
}