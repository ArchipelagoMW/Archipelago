import typing
from dataclasses import dataclass
from Options import PerGameCommonOptions, Range
from Options import DefaultOnToggle


class EmPriceRange(Range):
    range_start = 1000
    range_end = 50000
    default = 10000


class EmAfPrice(EmPriceRange):
    """Once the Athena's Fortune flag is aquired, and you sell X amount to the faction, you aquire the item on the Athena's Seal check"""
    display_name = "Seal Requirement (AF)"


class EmRbPrice(EmPriceRange):
    """Once the Reaper's Bone flag is aquired, and you sell X amount to the faction, you aquire the item on the Reaper's Seal check"""
    display_name = "Seal Requirement (RB)"


class EmGhPrice(EmPriceRange):
    """Once the Gold Hoarder's flag is aquired, and you sell X amount to the faction, you aquire the item on the Gold Hoarder's Seal check"""
    display_name = "Seal Requirement (GH)"


class EmMaPrice(EmPriceRange):
    """Once the Merchant Alliance flag is aquired, and you sell X amount to the faction, you aquire the item on the Merchant Alliance's Seal check"""
    display_name = "Seal Requirement (MA)"


class EmOosPrice(EmPriceRange):
    """Once the Order of Souls flag is aquired, and you sell X amount to the faction, you aquire the item on the Order of Souls's Seal check"""
    display_name = "Seal Requirement (OoS)"
