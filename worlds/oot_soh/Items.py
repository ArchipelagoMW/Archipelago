from typing import Callable, Dict, NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from . import SohWorld


class SohItem(Item):
    game = "Ship of Harkinian"

soh_base_id = int = 0xFF0000

class SohItemData(NamedTuple):
    code: Optional[int] = None
    type: ItemClassification = ItemClassification.filler

item_data_table: Dict[str, SohItemData] = {
    "Green Rupee": SohItemData(
        code=soh_base_id + 0,
    ),
    "Blue Rupee": SohItemData(
        code=soh_base_id + 1,
    ),
    "Red Rupee": SohItemData(
        code=soh_base_id + 2,
    ),
    "Progressive Bomb Bag": SohItemData(
        code=soh_base_id + 3,
        type=ItemClassification.progression,
    ),
}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
