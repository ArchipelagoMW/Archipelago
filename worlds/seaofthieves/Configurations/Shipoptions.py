import typing
from dataclasses import dataclass
from Options import PerGameCommonOptions, Range
from Options import DefaultOnToggle


class ShipSanity(DefaultOnToggle):
    """Adds play music, drink, sit, and sleep to location pool"""
    display_name = "Silly Ship"
    default = 1
