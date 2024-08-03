import typing
from dataclasses import dataclass

import Options
from Options import Choice
from Options import PerGameCommonOptions, Range
from Options import DefaultOnToggle

DefaultOffToggle = Options.Toggle


class FishSanity(Choice):
    """Adds 'On Fish Caught' location
    On For Each: replaces the on caught check with on caught for each fish
    No Life: replaces the on caught check with on caught for each descriptor+fish (Will add hours to your run)"""
    display_name = "Shuffle Catch Fish Checks"
    option_Off = 0
    option_On = 1
    option_On_For_Each = 2
    option_No_Life = 3
