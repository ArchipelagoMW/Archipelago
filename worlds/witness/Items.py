import typing

from BaseClasses import Item
from typing import Dict


from .FullLogic import overallAllItems, eventPanels, checksByHex, eventItemPairs
from .Locations import event_location_table

class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool
    event: bool = False

class WitnessItem(Item):
    game: str = "The Witness"


item_table: Dict[str, ItemData] = {
    'Temporary Speed Boost' : ItemData(158500, False, False),

    # Event Items
    'Victory': ItemData(158600, True, True)
}

event_item_table = dict()

for event_location in event_location_table:
    event_item_table[eventItemPairs[event_location]] = ItemData(None, True, True)
    item_table[eventItemPairs[event_location]] = ItemData(None, True, True)


for item in overallAllItems:
    if item[0] == "11 Lasers" or item == "7 Lasers":
        continue

    item_table[item[0]] = ItemData(158000 + item[1], True, False)

junk_weights = {
    "Temporary Speed Boost": 1
}
