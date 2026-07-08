"""This module provides options for gameplay section speedups"""
from Options import OptionCounter
from worlds.rac3.constants.options import RAC3OPTION
from worlds.rac3.constants.speedups import SPEEDUPS


class Speedups(OptionCounter):
    """
    Determines which gameplay sections are already completed.
    -----------------------------------------------------------------------------------------------
    When a speedup is enabled, the corresponding puzzle type will be skipped from the start.
    Gadget speedups require the corresponding gadget to be unlocked in order for the skip to activate.
    -----------------------------------------------------------------------------------------------
    0 = Disabled, Any other value = Enabled
    """
    min = 0
    display_name = RAC3OPTION.SPEEDUPS
    default = dict.fromkeys(SPEEDUPS, 0)
    valid_keys = SPEEDUPS
