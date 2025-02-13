from typing import Dict, NamedTuple, Optional

from BaseClasses import Item, ItemClassification
from .Names import ItemName


celeste_base_id: int = 0xCA1000


class CelesteItem(Item):
    game = "Celeste"


class CelesteItemData(NamedTuple):
    code: Optional[int] = None
    type: ItemClassification = ItemClassification.filler


collectable_item_data_table: Dict[str, CelesteItemData] = {
    ItemName.strawberry: CelesteItemData(celeste_base_id + 0x0, ItemClassification.progression_skip_balancing),
    ItemName.raspberry:  CelesteItemData(celeste_base_id + 0x1, ItemClassification.filler),
}

item_data_table: Dict[str, CelesteItemData] = {**collectable_item_data_table}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
