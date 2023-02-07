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
    # Difficulty Switch A
    # Difficulty Switch B
    # Freeincarnate
    # Slow Yorgle
    # Slow Grundle
    # Slow Rhindle
    # Bat Trap
    # Bat Time Out
    # "Revive Dragons": ItemData(0x100, ItemClassification.trap)
}


def get_num_items():
    return len(item_table)


event_table = {
}