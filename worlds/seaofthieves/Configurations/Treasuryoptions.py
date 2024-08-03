import typing
from dataclasses import dataclass

import Options
from Options import Choice
from Options import PerGameCommonOptions, Range
from Options import DefaultOnToggle

DefaultOffToggle = Options.Toggle


class TreasurySanity(Choice):
    """Adds 'On Treasury Complete' location
    On For Each: replaces the on treasury complete check with on treasury complete for each treasury
    """
    display_name = "TreasurySanity"
    option_Off = 0
    option_On = 1
    option_On_For_Each = 2
