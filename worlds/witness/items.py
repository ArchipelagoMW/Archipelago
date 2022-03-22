"""
Defines progression, junk and event items for The Witness
"""

from typing import Dict, NamedTuple, Optional

from BaseClasses import Item

from .full_logic import ALL_ITEMS, EVENT_ITEM_PAIRS
from .locations import EVENT_LOCATION_TABLE


class ItemData(NamedTuple):
    """
    ItemData for an item in The Witness
    """
    code: Optional[int]
    progression: bool
    event: bool = False


class WitnessItem(Item):
    """
    Item from the game The Witness
    """

    game: str = "The Witness"


ITEM_TABLE: Dict[str, ItemData] = {
    'Temporary Speed Boost': ItemData(158500, False, False),

    # Event Items
    'Victory': ItemData(158600, True, True)
}

EVENT_ITEM_TABLE = dict()

for event_location in EVENT_LOCATION_TABLE:
    location = EVENT_ITEM_PAIRS[event_location]
    EVENT_ITEM_TABLE[location] = ItemData(None, True, True)
    ITEM_TABLE[location] = ItemData(None, True, True)


for item in ALL_ITEMS:
    if item[0] == "11 Lasers" or item == "7 Lasers":
        continue

    ITEM_TABLE[item[0]] = ItemData(158000 + item[1], True, False)

ITEM_TABLE = dict(sorted(ITEM_TABLE.items(),
                  key=lambda item: item[1].code
                  if isinstance(item[1].code, int) else 0))

junk_weights = {
    "Temporary Speed Boost": 1
}
