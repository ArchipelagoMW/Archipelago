from typing import Dict

from Options import OptionDict


class Locations(OptionDict):
    display_name = "locations"


class Locations2(OptionDict):
    display_name = "locations2"


class Items(OptionDict):
    display_name = "items"


class Rules(OptionDict):
    display_name = "rules"


ff1_options: Dict[str, OptionDict] = {
    "locations": Locations,
    "locations2": Locations2,
    "items": Items,
    "rules": Rules
}
