import typing
from Options import Option, Range


class MaxAnimAppear(Range):
    """Max amount of Animatronics that will appear at once."""
    display_name = "Max Animatronics Appearing"
    range_start = 1
    range_end = 4
    default = 4


FFPS_options: typing.Dict[str, type(Option)] = {
    "max_animatronics_appearing":                           MaxAnimAppear,
}
