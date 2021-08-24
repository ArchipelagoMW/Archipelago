import typing
from Options import Choice, Option, Range, Toggle


class Character(Choice):
    """Pick What Character you wish to play with."""
    display_name = "Character"
    option_ironclad = 0
    option_silent = 1
    option_defect = 2
    option_watcher = 3
    default = 0


class Games(Range):
    """The amount of games you will need to play."""
    display_name = "Games"
    range_start = 1
    range_end = 5
    default = 1


class Ascension(Range):
    """Pick What Character you wish to play with."""
    display_name = "Ascension"
    range_start = 0
    range_end = 20
    default = 0


class HeartRun(Toggle):
    """Whether or not you will need to collect they 3 keys to unlock the final act
     and beat the heart to finish the game."""
    display_name = "Heart Run"
    option_true = 1
    option_false = 0
    default = 0


spire_options: typing.Dict[str, type(Option)] = {
    "character": Character,
    "games": Games,
    "ascension": Ascension,
    "heart_run": HeartRun
}