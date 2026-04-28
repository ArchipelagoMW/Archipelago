from Options import OptionCounter
from worlds.rac3.constants.options import RAC3OPTION
from worlds.rac3.constants.region import PLANETS_WITH_HACKER_PUZZLES


class HackerSkip(OptionCounter):
    """
    Determines which planet's hacker puzzles should be skipped.
    Receiving The Hacker will instantly mark all puzzles on the enabled planets as completed.
    If The Hacker is received while on a planet with an enabled skip, the doors open automatically.

    1 = Enabled, 0 = Disabled
    """
    min = 0
    max = 1
    display_name = RAC3OPTION.HACKER_SKIP
    default = dict.fromkeys(PLANETS_WITH_HACKER_PUZZLES, 0)
    valid_keys = PLANETS_WITH_HACKER_PUZZLES
