import typing
from Options import Choice, Option, Toggle


class RouteRequired(Choice):
    """Main route of the game required to win."""
    display_name = "Required Route"
    option_neutral = 0
    option_pacifist = 1
    option_genocide = 2
    default = 0


class IncludeTemy(Toggle):
    """Adds Temmy Armor to the item pool."""
    display_name = "Include Temy Armor"
    default = 1


undertale_options: typing.Dict[str, type(Option)] = {
    "route_required":                           RouteRequired,
    "temy_include":                              IncludeTemy,
}
