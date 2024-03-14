import typing

from BaseClasses import Item
from typing import Dict


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool
    event: bool = False


item_table: Dict[str, ItemData] = {
    'Card Draw': ItemData(8000, True),
    'Rare Card Draw': ItemData(8001, True),
    'Relic': ItemData(8002, True),
    'Boss Relic': ItemData(8003, True),

    # Event Items
    'Victory': ItemData(None, True, True),
    'Beat Act 1 Boss': ItemData(None, True, True),
    'Beat Act 2 Boss': ItemData(None, True, True),
    'Beat Act 3 Boss': ItemData(None, True, True),

}

item_pool: Dict[str, int] = {
    'Card Draw': 15,
    'Rare Card Draw': 2,
    'Relic': 10,
    'Boss Relic': 2
}

event_item_pairs: Dict[str, str] = {
    "Heart Room": "Victory",
    "Act 1 Boss": "Beat Act 1 Boss",
    "Act 2 Boss": "Beat Act 2 Boss",
    "Act 3 Boss": "Beat Act 3 Boss"
}
