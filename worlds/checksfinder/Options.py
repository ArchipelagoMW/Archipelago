import typing
from Options import Choice, Option, Toggle, Range, OptionList, DeathLink


class MaxWidth(Range):
    """The goal width of the board."""
    display_name = "Goal Width"
    range_start = 10
    range_end = 25
    default = 10


class MaxHeight(Range):
    """The goal height of the board."""
    display_name = "Goal Height"
    range_start = 10
    range_end = 25
    default = 10


class MaxBombs(Range):
    """The goal amount of bombs on the board."""
    display_name = "Goal Bombs"
    range_start = 10
    range_end = 40
    default = 20


class noneOption(Toggle):
    """There are no options."""
    display_name = "None"


checksfinder_options: typing.Dict[str, type(Option)] = {
    "none":                     noneOption,
}
