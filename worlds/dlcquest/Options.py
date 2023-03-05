import typing
from Options import Option, DeathLink, Choice

class FalseDoubleJump(Choice):
    """If you can do a double jump without the pack for it (bug)."""
    internal_name = "double_jump_bug"
    display_name = "Double Jump Bug"
    option_none = 0
    option_simple = 1
    option_all = 2
    default = 0


DLCquest_options: typing.Dict[str,type(Option)] = {
    "FalseDoubleJump": FalseDoubleJump,
    "death_link": DeathLink
}