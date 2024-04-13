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
    ItemName.strawberry: Celeste64ItemData(celeste_64_base_id + 0, ItemClassification.progression_skip_balancing),
    ItemName.raspberry:  Celeste64ItemData(celeste_64_base_id + 9, ItemClassification.filler),
}

unlockable_item_data_table: Dict[str, Celeste64ItemData] = {
    ItemName.dash_refill:        Celeste64ItemData(celeste_64_base_id + 1, ItemClassification.progression),
    ItemName.double_dash_refill: Celeste64ItemData(celeste_64_base_id + 2, ItemClassification.progression),
    ItemName.feather:            Celeste64ItemData(celeste_64_base_id + 3, ItemClassification.progression),
    ItemName.coin:               Celeste64ItemData(celeste_64_base_id + 4, ItemClassification.progression),
    ItemName.cassette:           Celeste64ItemData(celeste_64_base_id + 5, ItemClassification.progression),
    ItemName.traffic_block:      Celeste64ItemData(celeste_64_base_id + 6, ItemClassification.progression),
    ItemName.spring:             Celeste64ItemData(celeste_64_base_id + 7, ItemClassification.progression),
    ItemName.breakables:         Celeste64ItemData(celeste_64_base_id + 8, ItemClassification.progression),
}

item_data_table: Dict[str, Celeste64ItemData] = {**collectable_item_data_table, **unlockable_item_data_table}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
