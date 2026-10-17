from BaseClasses import ItemClassification
from .. import ItemTypeEnum
from ...constants import ITEMS_GHOST_OFFSET


class RandomGhosts(ItemTypeEnum):
    ONE_GHOST_CARD = ("One Ghost Card", ITEMS_GHOST_OFFSET + 1, ItemClassification.progression)
    TWO_GHOST_CARD = ("Two Ghost Cards", ITEMS_GHOST_OFFSET + 2, ItemClassification.progression)
    THREE_GHOST_CARD = ("Three Ghost Cards", ITEMS_GHOST_OFFSET + 3, ItemClassification.progression)
    FOUR_GHOST_CARD = ("Four Ghost Cards", ITEMS_GHOST_OFFSET + 4, ItemClassification.progression)
    FIVE_GHOST_CARD = ("Five Ghost Cards", ITEMS_GHOST_OFFSET + 5, ItemClassification.progression)

GHOST_ITEM_BY_ID = {
    item.item_id: item
    for item in RandomGhosts
}