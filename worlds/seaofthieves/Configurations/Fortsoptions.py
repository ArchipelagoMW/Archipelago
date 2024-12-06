import typing
from dataclasses import dataclass

import Options
from Options import Choice
from Options import PerGameCommonOptions, Range
from Options import DefaultOnToggle

DefaultOffToggle = Options.Toggle


class FortressSanity(Choice):
    """Adds 'On Fortress Complete' location
    On For Each: replaces the on fortress complete check with on fortress complete for each fortress
    """
    display_name = "Shuffle Fortress Comp Checks"
    option_Off = 0
    option_On = 1
    option_On_For_Each = 2
