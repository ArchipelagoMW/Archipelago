from typing import Dict

from Options import OptionDict


class Locations(OptionDict):
    """to roll settings go to https://finalfantasyrandomizer.com/"""
    display_name = "locations"


class Items(OptionDict):
    """to roll settings go to https://finalfantasyrandomizer.com/"""
    display_name = "items"


class Rules(OptionDict):
    """to roll settings go to https://finalfantasyrandomizer.com/"""
    display_name = "rules"


ff1_options: Dict[str, OptionDict] = {
    "locations": Locations,
    "items": Items,
    "rules": Rules
}
