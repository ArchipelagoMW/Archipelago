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
    
    
class Portals(Toggle):
    """Wether or not you want to have act portals enabled. Reach boss chest of previous act to activate it on future runs.
    Using a portal will use arbitrary checkpoints on locations to help you progress with them"""
    display_name = "Portals"
    option_true = 1
    option_false = 0
    default = 1
    
    

spire_options: typing.Dict[str, type(Option)] = {
    "character": Character,
    "ascension": Ascension,
    "heart_run": HeartRun,
    "portals": Portals
}
