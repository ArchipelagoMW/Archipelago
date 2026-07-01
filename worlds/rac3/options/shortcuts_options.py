"""This module contains options for level shortcuts"""

from Options import OptionCounter
from worlds.rac3.constants.options import RAC3OPTION
from worlds.rac3.constants.shortcuts import RAC3SHORTCUTS, SHORTCUTS


class Shortcuts(OptionCounter):
    """
    Determines which shortcuts are enabled in the game.
    When a shortcut is enabled, the corresponding teleporter/taxi will be available from the start.
    Shortcuts will not let you skip logic, so you still need the required items to access the areas.
    Veldin Skip will force the player to start on the Starship Phoenix

    1 = Enabled, 0 = Disabled
    """
    min = 0
    max = 1
    display_name = RAC3OPTION.SHORTCUTS
    default = dict.fromkeys(SHORTCUTS, 0)
    default[RAC3SHORTCUTS.VELDIN_SKIP] = 1
    valid_keys = SHORTCUTS
