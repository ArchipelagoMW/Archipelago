import typing
from dataclasses import dataclass

import Options
from Options import Choice
from Options import PerGameCommonOptions, Range
from Options import DefaultOnToggle

DefaultOffToggle = Options.Toggle


class ServantSanity(Choice):
    """Adds 'On Hourglass Guardian of Fortune Sunk' location
    On For Each: replaces the On Hourglass Guardian of Fortune Sunk check with a check on Guardian of Fortune sloop, brig, and galleon check
    """
    display_name = "(PVP) Servant"
    option_Off = 0
    option_On = 1
    option_On_For_Each = 2
