from typing import Dict

from Options import OptionDict


class Locations(OptionDict):
    display_name = "locations"


class Items(OptionDict):
    display_name = "items"


class Rules(OptionDict):
    display_name = "rules"


ff1_options: Dict[str, OptionDict] = {
    "locations": Locations,
    "items": Items,
    "rules": Rules
}
