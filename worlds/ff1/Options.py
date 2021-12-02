from typing import Dict

from Options import OptionDict


class Locations(OptionDict):
    displayname = "locations"


class Items(OptionDict):
    displayname = "items"


class Rules(OptionDict):
    displayname = "rules"


ff1_options: Dict[str, OptionDict] = {
    "locations": Locations,
    "items": Items,
    "rules": Rules
}
