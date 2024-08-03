import typing
from dataclasses import dataclass

import Options
from Options import Choice
from Options import PerGameCommonOptions, Range
from Options import DefaultOnToggle

DefaultOffToggle = Options.Toggle


class RowboatSanity(Choice):
    """Adds 'On Rowboat Dock' location
    On For Each: replaces the On Rowboat Dock check with a check on each unique rowboat (Lantern, Harpoon, Cannon)
    """
    display_name = "Rowboats"
    option_Off = 0
    option_On = 1
    option_On_For_Each = 2
