import typing
from Options import Choice, Option, Toggle, Range


class RouteRequired(Choice):
    """Main route of the game required to win."""
    display_name = "Required Route"
    option_neutral = 0
    option_pacifist = 1
    option_genocide = 2
    option_all_routes = 3
    default = 0


class IncludeTemy(Toggle):
    """Adds Temmy Armor to the item pool."""
    display_name = "Include Temy Armor"
    default = 1


class SoulPieces(Range):
    default = 5
    range_start = 1
    range_end = 5


class SoulHunt(Toggle):
    """Adds Soul Pieces to the item pool, you need all of them to enter the last corridor."""
    display_name = "Soul Piece Hunt"
    default = 0


class ProgressivePlot(Toggle):
    """Makes the plot items progressive."""
    display_name = "Progressive Plot"
    default = 1


class OnlyFlakes(Toggle):
    """Replaces all non-required items, except equipment, with Temmie Flakes."""
    display_name = "Only Temmie Flakes"
    default = 0


class NoEquips(Toggle):
    """Removes all equippable items."""
    display_name = "No Equippables"
    default = 0


class RandomizeLove(Toggle):
    """Adds LOVE to the pool. GENOCIDE ONLY!"""
    display_name = "Randomize LOVE"
    default = 0


class RandomizeAreas(Toggle):
    """Randomizes the order each major area of the game."""
    display_name = "Randomize Area Order"
    default = 0


class RandomizeStats(Toggle):
    """Makes each stat increase from LV a separate item. GENOCIDE ONLY!
    This may be a problem to some people, make sure everyone is okay with this option before choosing to have it on."""
    display_name = "Randomize Stats"
    default = 0


undertale_options: typing.Dict[str, type(Option)] = {
    "route_required":                           RouteRequired,
    "temy_include":                             IncludeTemy,
    "no_equips":                                NoEquips,
    "only_flakes":                              OnlyFlakes,
    "soul_hunt":                                SoulHunt,
    "soul_pieces":                              SoulPieces,
    "prog_plot":                                ProgressivePlot,
    "rando_love":                                RandomizeLove,
    "rando_area":                                RandomizeAreas,
    "rando_stats":                                RandomizeStats,
}
