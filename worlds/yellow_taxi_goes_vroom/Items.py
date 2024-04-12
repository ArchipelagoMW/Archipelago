from typing import NamedTuple
from BaseClasses import Item, ItemClassification
from .Constants import YTGV_BASE_ID
from .Names import ItemName

class YTGVItem(Item):
    game = "Yellow Taxi Goes Vroom"

class YTGVItemData(NamedTuple):
    id: int
    classification: ItemClassification

item_data_table = {
    ItemName.GEAR: YTGVItemData(
        id = YTGV_BASE_ID + 0,
        classification = ItemClassification.progression,
    ),
}

name_to_id = {
    ItemName.GEAR: YTGV_BASE_ID + 0
}