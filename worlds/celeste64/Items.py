from typing import Dict, NamedTuple, Optional

from BaseClasses import Item, ItemClassification
from .Names import ItemName


celeste_64_base_id: int = 0xCA0000


class Celeste64Item(Item):
    game = "Celeste 64"


class Celeste64ItemData(NamedTuple):
    code: Optional[int] = None
    type: ItemClassification = ItemClassification.filler


collectable_item_data_table: Dict[str, Celeste64ItemData] = {
    ItemName.strawberry: Celeste64ItemData(celeste_64_base_id + 0x0, ItemClassification.progression_skip_balancing),
    ItemName.raspberry:  Celeste64ItemData(celeste_64_base_id + 0x9, ItemClassification.filler),
}

unlockable_item_data_table: Dict[str, Celeste64ItemData] = {
    ItemName.dash_refill:        Celeste64ItemData(celeste_64_base_id + 0x1, ItemClassification.progression),
    ItemName.double_dash_refill: Celeste64ItemData(celeste_64_base_id + 0x2, ItemClassification.progression),
    ItemName.feather:            Celeste64ItemData(celeste_64_base_id + 0x3, ItemClassification.progression),
    ItemName.coin:               Celeste64ItemData(celeste_64_base_id + 0x4, ItemClassification.progression),
    ItemName.cassette:           Celeste64ItemData(celeste_64_base_id + 0x5, ItemClassification.progression),
    ItemName.traffic_block:      Celeste64ItemData(celeste_64_base_id + 0x6, ItemClassification.progression),
    ItemName.spring:             Celeste64ItemData(celeste_64_base_id + 0x7, ItemClassification.progression),
    ItemName.breakables:         Celeste64ItemData(celeste_64_base_id + 0x8, ItemClassification.progression),
}

move_item_data_table: Dict[str, Celeste64ItemData] = {
    ItemName.ground_dash: Celeste64ItemData(celeste_64_base_id + 0xA, ItemClassification.progression),
    ItemName.air_dash:    Celeste64ItemData(celeste_64_base_id + 0xB, ItemClassification.progression),
    ItemName.skid_jump:   Celeste64ItemData(celeste_64_base_id + 0xC, ItemClassification.progression),
    ItemName.climb:       Celeste64ItemData(celeste_64_base_id + 0xD, ItemClassification.progression),
}

item_data_table: Dict[str, Celeste64ItemData] = {**collectable_item_data_table, **unlockable_item_data_table, **move_item_data_table}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
