"""
Classes and functions related to AP items for Metroid: Zero Mission
"""

from BaseClasses import Item, ItemClassification
from typing import Dict

from .patcher.items import ItemData as ZMItemData, item_data_table


AP_MZM_ID_BASE = 261300

progression = ItemClassification.progression
filler = ItemClassification.filler
useful = ItemClassification.useful
trap = ItemClassification.trap
skip_balancing = ItemClassification.progression_skip_balancing


class MZMItem(Item):
    game: str = "Metroid Zero Mission"


class ItemData:
    progression: ItemClassification
    code: int
    game_data: ZMItemData

    def __init__(self, progression: ItemClassification, id: int, name: str):
        self.progression = progression
        self.code = AP_MZM_ID_BASE + id
        self.game_data = item_data_table[name]


tank_data_table = {
    "Energy Tank":        ItemData(progression,     0, "Energy Tank"),
    "Missile Tank":       ItemData(progression,     1, "Missile Tank"),
    "Super Missile Tank": ItemData(progression,     2, "Super Missile Tank"),
    "Power Bomb Tank":    ItemData(progression,     3, "Power Bomb Tank"),
    "Metroid DNA":        ItemData(skip_balancing, 22, "Metroid DNA"),
}

major_item_data_table = {
    "Long Beam":          ItemData(progression,  4, "Long Beam"),
    "Charge Beam":        ItemData(progression,  5, "Charge Beam"),
    "Ice Beam":           ItemData(progression,  6, "Ice Beam"),
    "Wave Beam":          ItemData(progression,  7, "Wave Beam"),
    "Plasma Beam":        ItemData(progression,  8, "Plasma Beam"),
    "Bomb":               ItemData(progression,  9, "Bomb"),

    "Varia Suit":         ItemData(progression, 10, "Varia Suit"),
    "Gravity Suit":       ItemData(progression, 11, "Gravity Suit"),
    "Morph Ball":         ItemData(progression, 12, "Morph Ball"),
    "Speed Booster":      ItemData(progression, 13, "Speed Booster"),
    "Hi-Jump":            ItemData(progression, 14, "Hi-Jump"),
    "Screw Attack":       ItemData(progression, 15, "Screw Attack"),
    "Space Jump":         ItemData(progression, 16, "Space Jump"),
    "Power Grip":         ItemData(progression, 17, "Power Grip"),

    "Fully Powered Suit": ItemData(progression, 19, "Fully Powered Suit"),
    "Wall Jump":          ItemData(progression, 20, "Wall Jump"),
    "Spring Ball":        ItemData(progression, 21, "Spring Ball"),
}

extra_item_data_table = {
    "Nothing":            ItemData(filler,      18, "Nothing"),
}

item_data_table: Dict[str, ItemData] = {
    **tank_data_table,
    **major_item_data_table,
    **extra_item_data_table,
}

mzm_item_name_groups = {
    "Beams": {name for name in major_item_data_table.keys() if name.endswith("Beam")},
    "Upgrades": {
        "Bomb",
        *(name for name in major_item_data_table.keys() if not name.endswith("Beam"))
    },
    "Major Items": set(major_item_data_table.keys()),
    "Missiles": {
        "Missile Tank",
        "Super Missile Tank",
    },
}
