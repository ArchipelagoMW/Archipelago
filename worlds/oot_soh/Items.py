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
    can_create: Callable[["SohWorld"], bool] = lambda world: True


item_data_table: Dict[str, SohItemData] = {
    "Green Rupee": SohItemData(
        code=soh_base_id + 0,
        type=ItemClassification.progression,
        # can_create=lambda world: world.options.death_link,
    ),
    "Blue Rupee": SohItemData(
        code=soh_base_id + 1,
    ),
    "Red Rupee": SohItemData(
        code=soh_base_id + 2,
    ),
    "Progressive Bomb Bag": SohItemData(
        code=soh_base_id + 3,
    ),
}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
