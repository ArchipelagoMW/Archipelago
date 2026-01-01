from dataclasses import dataclass

from Options import OptionDict, PerGameCommonOptions


class Locations(OptionDict):
    """to roll settings go to https://finalfantasyrandomizer.com/"""
    display_name = "locations"


class Items(OptionDict):
    """to roll settings go to https://finalfantasyrandomizer.com/"""
    display_name = "items"


class Rules(OptionDict):
    """to roll settings go to https://finalfantasyrandomizer.com/"""
    display_name = "rules"


@dataclass
class FF1Options(PerGameCommonOptions):
    locations: Locations
    items: Items
    rules: Rules
