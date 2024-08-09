import typing
from dataclasses import dataclass

import Options
from Options import Choice
from Options import PerGameCommonOptions, Range
from Options import DefaultOnToggle

DefaultOffToggle = Options.Toggle


class ShipwreckOptions(DefaultOffToggle):
    """Adds 'Discover Shipwreck'
    """
    display_name = "Shipwrecks"
