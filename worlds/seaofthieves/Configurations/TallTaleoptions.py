import typing
from dataclasses import dataclass

import Options
from Options import Choice
from Options import PerGameCommonOptions, Range
from Options import DefaultOnToggle

DefaultOffToggle = Options.Toggle


class TallTaleoptions(Choice):
    """Adds 'On Complete Tall Tale' location
    On For Each: replaces this check with a check each Tall Tale's completion
    """
    display_name = "Tall Tales"
    option_Off = 0
    option_On = 1
    option_On_For_Each = 2
