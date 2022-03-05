import typing
from Options import Choice, Option, Toggle, Range, OptionList, DeathLink


class MaxWidth(Range):
    """The max width of the board."""
    display_name = "Max Width"
    range_start = 10
    range_end = 25
    default = 10


class MaxHeight(Range):
    """The max height of the board."""
    display_name = "Max Height"
    range_start = 10
    range_end = 25
    default = 10


class MaxBombs(Range):
    """The max amount of bombs on the board."""
    display_name = "Max Bombs"
    range_start = 10
    range_end = 40
    default = 20


checksfinder_options: typing.Dict[str, type(Option)] = {
    "max_width":                     MaxWidth,
    "max_height":                     MaxHeight,
    "max_bombs":                     MaxBombs,
}
