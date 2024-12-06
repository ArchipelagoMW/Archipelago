import typing
from dataclasses import dataclass

import Options
from Options import Choice
from Options import PerGameCommonOptions, Range
from Options import DefaultOnToggle

DefaultOffToggle = Options.Toggle


class CaptainShipoptions(Choice):
    """Adds 'On Captain Ship Spotted' location
    On For Each: replaces this check with a check on spotting a Sloop, Brig, and Galleon
    """
    display_name = "Spot Ships"
    option_Off = 0
    option_On = 1
    option_On_For_Each = 2
