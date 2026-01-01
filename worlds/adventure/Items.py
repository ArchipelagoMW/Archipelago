from typing import Optional
from BaseClasses import ItemClassification, Item

base_adventure_item_id = 118000000


class AdventureItem(Item):
    def __init__(self, name: str, classification: ItemClassification, code: Optional[int], player: int):
        super().__init__(name, classification, code, player)


class ItemData:
    def __init__(self, id: int, classification: ItemClassification):
        self.classification = classification
        self.id = None if id is None else id + base_adventure_item_id
        self.table_index = id


nothing_item_id = base_adventure_item_id

# base IDs are the index in the static item data table, which is
# not the same order as the items in RAM (but offset 0 is a 16-bit address of
# location of room and position data)
item_table = {
    "Yellow Key": ItemData(0xB, ItemClassification.progression_skip_balancing),
    "White Key": ItemData(0xC, ItemClassification.progression),
    "Black Key": ItemData(0xD, ItemClassification.progression),
    "Bridge": ItemData(0xA, ItemClassification.progression),
    "Magnet": ItemData(0x11, ItemClassification.progression),
    "Sword": ItemData(0x9, ItemClassification.progression),
    "Chalice": ItemData(0x10, ItemClassification.progression_skip_balancing),
    # Non-ROM Adventure items, managed by lua
    "Left Difficulty Switch": ItemData(0x100, ItemClassification.filler),
    "Right Difficulty Switch": ItemData(0x101, ItemClassification.filler),
    # Can use these instead of 'nothing'
    "Freeincarnate": ItemData(0x102, ItemClassification.filler),
    # These should only be enabled if fast dragons is on?
    "Slow Yorgle": ItemData(0x103, ItemClassification.filler),
    "Slow Grundle": ItemData(0x104, ItemClassification.filler),
    "Slow Rhindle": ItemData(0x105, ItemClassification.filler),
    # this should only be enabled if opted into?  For now, I'll just exclude them
    "Revive Dragons": ItemData(0x106, ItemClassification.trap),
    "nothing": ItemData(0x0, ItemClassification.filler)
    # Bat Trap
    # Bat Time Out
    # "Revive Dragons": ItemData(0x110, ItemClassification.trap)
}

standard_item_max = item_table["Magnet"].id


event_table = {
}