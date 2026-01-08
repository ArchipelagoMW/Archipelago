from typing import Dict, Set, NamedTuple, Optional
from BaseClasses import ItemClassification


class ItemData(NamedTuple):
    category: str
    code: Optional[int]
    classification: ItemClassification
    amount: Optional[int] = 1


item_table: Dict[str, ItemData] = {
    "Candle": ItemData("Items", 0x01, ItemClassification.progression),
    "Handy Glove": ItemData("Items", 0x02, ItemClassification.progression),
    "Raft": ItemData("Items", 0x03, ItemClassification.progression),
    "Boots": ItemData("Items", 0x04, ItemClassification.progression),
    "Flute": ItemData("Items", 0x05, ItemClassification.progression),
    "Cross": ItemData("Items", 0x06, ItemClassification.progression),
    "Hammer": ItemData("Items", 0x07, ItemClassification.progression),
    "Magical Key": ItemData("Items", 0x08, ItemClassification.progression_skip_balancing, 0),

    "Shield Spell": ItemData("Items", 0x10, ItemClassification.useful, 0),
    "Jump Spell": ItemData("Spells", 0x11, ItemClassification.progression, 0),
    "Life Spell": ItemData("Spells", 0x12, ItemClassification.useful, 0),
    "Fairy Spell": ItemData("Spells", 0x13, ItemClassification.progression, 0),
    "Fire Spell": ItemData("Spells", 0x14, ItemClassification.filler, 0),
    "Reflect Spell": ItemData("Spells", 0x15, ItemClassification.progression, 0),
    "Spell Spell": ItemData("Spells", 0x16, ItemClassification.progression, 0),
    "Thunder Spell": ItemData("Spells", 0x17, ItemClassification.progression, 0),

    "Magic Container": ItemData("Containers", 0x20, ItemClassification.progression, 4),
    "Heart Container": ItemData("Containers", 0x21, ItemClassification.useful, 4),

    "Down Thrust": ItemData("Attacks", 0x30, ItemClassification.progression),
    "Up Thrust": ItemData("Attacks", 0x31, ItemClassification.progression),
    "Trophy": ItemData("Key Items", 0x32, ItemClassification.progression),
    "Water of Life": ItemData("Key Items", 0x33, ItemClassification.progression),
    "Child": ItemData("Key Items", 0x34, ItemClassification.progression),
    "Bagu's Letter": ItemData("Key Items", 0x35, ItemClassification.progression),

    "1-Up Doll": ItemData("Collectibles", 0x40, ItemClassification.useful, 3),
    "Blue Magic Jar": ItemData("Collectibles", 0x41, ItemClassification.filler, 0),
    "Red Magic Jar": ItemData("Collectibles", 0x42, ItemClassification.useful, 0),
    "50 Point P-Bag": ItemData("Collectibles", 0x43, ItemClassification.filler, 0),
    "100 Point P-Bag": ItemData("Collectibles", 0x44, ItemClassification.filler, 0),
    "200 Point P-Bag": ItemData("Collectibles", 0x45, ItemClassification.useful, 0),
    "500 Point P-Bag": ItemData("Collectibles", 0x46, ItemClassification.useful, 0),

    "Parapa Palace Key": ItemData("Keys", 0x50, ItemClassification.progression, 0),
    "Midoro Palace Key": ItemData("Keys", 0x51, ItemClassification.progression, 0),
    "Island Palace Key": ItemData("Keys", 0x52, ItemClassification.progression, 0),
    "Maze Palace Key": ItemData("Keys", 0x53, ItemClassification.progression, 0),
    "Sea Palace Key": ItemData("Keys", 0x54, ItemClassification.progression, 0),
    "Three-Eye Rock Palace Key": ItemData("Keys", 0x55, ItemClassification.progression, 0),

    "Triforce of Courage": ItemData("Events", None, ItemClassification.progression, 0),
    "Crystal Returned": ItemData("Events", None, ItemClassification.progression, 0),
}


def get_item_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in item_table.items():
        if data.category != "Events":
            categories.setdefault(data.category, set()).add(name)

    return categories
