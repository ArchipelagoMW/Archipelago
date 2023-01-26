from typing import Optional
from BaseClasses import ItemClassification, Item

base_adventure_item_id = 118000000


class AdventureItem(Item):
    def __init__(self, name: str, classification: ItemClassification, code: Optional[int], player: int):
        super().__init__(name, classification, code, player)


class ItemData:
    def __init__(self, id, classification):
        self.classification = classification
        self.id = None if id is None else id + base_adventure_item_id
        self.table_index = id


nothing_item_id = 0

# base IDs are the index in the static item data table, which is
# not the same order as the items in RAM (but offsets 0-1 is the 16-bit
# location of room and position data
item_table = {
    "YellowKey": ItemData(0xB, ItemClassification.progression_skip_balancing),
    "WhiteKey": ItemData(0xC, ItemClassification.progression),
    "BlackKey": ItemData(0xD, ItemClassification.progression),
    "Bridge": ItemData(0xA, ItemClassification.progression),
    "Magnet": ItemData(0x11, ItemClassification.progression),
    "Sword": ItemData(0x9, ItemClassification.progression),
    "Chalice": ItemData(0x10, ItemClassification.progression_skip_balancing),
    # "Dragon_Revival": ItemData(0x100, ItemClassification.trap) or would this be an event?
    # "Big_Sword":
}

event_table = {
}