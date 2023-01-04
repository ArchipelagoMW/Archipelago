import typing
from Options import TextChoice, Option, Range, Toggle


class Character(TextChoice):
    """Enter the Title of the character you wish to play as, for custom characters this should match exactly the full
     title that shows up when choosing them in the vanilla character select screen.

     Spire Take the Wheel will have your client pick a random character from the list of all your installed characters
     including custom ones.
     """
    display_name = "Character"
    option_the_ironclad = 0
    option_the_silent = 1
    option_the_defect = 2
    option_the_watcher = 3
    option_spire_take_the_wheel = 4


class Ascension(Range):
    """What Ascension do you wish to play with."""
    display_name = "Ascension"
    range_start = 0
    range_end = 20
    default = 0


class HeartRun(Toggle):
    """Whether or not you will need to collect the 3 keys and enter the final act to
    complete the game. The Heart does not need to be defeated."""
    display_name = "Heart Run"
    option_true = 1
    option_false = 0
    default = 0


spire_options: typing.Dict[str, type(Option)] = {
    "character": Character,
    "ascension": Ascension,
    "heart_run": HeartRun
}
