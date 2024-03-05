from typing import Dict, NamedTuple, Optional

from BaseClasses import Item, ItemClassification
from .Names import ItemName


celeste_64_base_id: int = 0xCA0000


class Celeste64Item(Item):
    game = "Celeste 64"


class Celeste64ItemData(NamedTuple):
    code: Optional[int] = None
    type: ItemClassification = ItemClassification.filler


item_data_table: Dict[str, Celeste64ItemData] = {
    ItemName.strawberry: Celeste64ItemData(
        code = celeste_64_base_id + 0,
        type=ItemClassification.progression_skip_balancing,
    ),
    ItemName.dash_refill: Celeste64ItemData(
        code = celeste_64_base_id + 1,
        type=ItemClassification.progression,
    ),
    ItemName.double_dash_refill: Celeste64ItemData(
        code = celeste_64_base_id + 2,
        type=ItemClassification.progression,
    ),
    ItemName.feather: Celeste64ItemData(
        code = celeste_64_base_id + 3,
        type=ItemClassification.progression,
    ),
    ItemName.coin: Celeste64ItemData(
        code = celeste_64_base_id + 4,
        type=ItemClassification.progression,
    ),
    ItemName.cassette: Celeste64ItemData(
        code = celeste_64_base_id + 5,
        type=ItemClassification.progression,
    ),
    ItemName.traffic_block: Celeste64ItemData(
        code = celeste_64_base_id + 6,
        type=ItemClassification.progression,
    ),
    ItemName.spring: Celeste64ItemData(
        code = celeste_64_base_id + 7,
        type=ItemClassification.progression,
    ),
    ItemName.breakables: Celeste64ItemData(
        code = celeste_64_base_id + 8,
        type=ItemClassification.progression,
    )
}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
