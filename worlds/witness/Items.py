import typing

from BaseClasses import Item
from typing import Dict


from .FullLogic import overallAllItems, eventPanels, checksByHex

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

for event_item in eventPanels:
    event_item_table[checksByHex[event_item[0]]["checkName"] + " Event"] = ItemData(None, True, True)
    item_table[checksByHex[event_item[0]]["checkName"] + " Event"] = ItemData(None, True, True)

print(item_table)

counter = 0

for item in overallAllItems:
    if item == "11 Lasers" or item == "7 Lasers":
        continue

    item_table[item] = ItemData(158000 + counter, True, False)
    
    counter += 1

junk_weights = {
    "Temporary Speed Boost": 1
}
