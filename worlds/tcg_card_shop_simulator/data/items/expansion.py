from BaseClasses import ItemClassification
from .. import ItemTypeEnum
from ...constants import ITEMS_EXPANSION_OFFSET


class Expansions(ItemTypeEnum):
    SHOP_EXPANSION = ("Shop Expansion", ITEMS_EXPANSION_OFFSET + 0, ItemClassification.progression)
    WAREHOUSE_EXPANSION = ("Warehouse Expansion", ITEMS_EXPANSION_OFFSET + 1, ItemClassification.progression)