from Options import OptionCounter
from worlds.rac3.constants.options import RAC3OPTION
from worlds.rac3.constants.shortcuts import SHORTCUTS


class Shortcuts(OptionCounter):
    """
    Determines which shortcuts are enabled in the game. 
    When a shortcut is enabled, the corresponding puzzle type will be skipped or teleporter/taxi will be available from the start.

    1 = Enabled, 0 = Disabled
    """
    min = 0
    max = 1
    display_name = RAC3OPTION.SHORTCUTS
    default = dict.fromkeys(SHORTCUTS, 0)
    valid_keys = SHORTCUTS
