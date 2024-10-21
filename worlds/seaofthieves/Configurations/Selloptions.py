import typing
from dataclasses import dataclass
from Options import PerGameCommonOptions, Range
from Options import Toggle


class SellRange(Range):
    range_start = 0
    range_end = 10
    default = 10


class GhSellRange(SellRange):
    """Adds a location on selling a unique object for a specific faction (does not matter what vendor object is sold to)"""
    display_name = "Shuffle Unique Sells (GH)"


class MaSellRange(SellRange):
    """Adds a location on selling a unique object for a specific faction (does not matter what vendor object is sold to)"""
    display_name = "Shuffle Unique Sells (MA)"


class OosSellRange(SellRange):
    """Adds a location on selling a unique object for a specific faction (does not matter what vendor object is sold to)"""
    display_name = "Shuffle Unique Sells (OoS)"


class AfSellRange(SellRange):
    """Adds a location on selling a unique object for a specific faction (does not matter what vendor object is sold to)"""
    display_name = "Shuffle Unique Sells (AF)"
    default = 5


class RbSellRange(SellRange):
    """Adds a location on selling a unique object for a specific faction (does not matter what vendor object is sold to)"""
    display_name = "Shuffle Unique Sells (RB)"
    default = 2
