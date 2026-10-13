from BaseClasses import ItemClassification
from .. import ItemTypeEnum
from ...constants import ITEMS_GHOST_OFFSET


class RandomGhosts(ItemTypeEnum):
    ONE_GHOST_CARD = ("One Ghost Card", ITEMS_GHOST_OFFSET + 0, ItemClassification.progression)
    TWO_GHOST_CARD = ("Two Ghost Cards", ITEMS_GHOST_OFFSET + 0, ItemClassification.progression)
    THREE_GHOST_CARD = ("Three Ghost Cards", ITEMS_GHOST_OFFSET + 0, ItemClassification.progression)
    FOUR_GHOST_CARD = ("Four Ghost Cards", ITEMS_GHOST_OFFSET + 0, ItemClassification.progression)
    FIVE_GHOST_CARD = ("Five Ghost Cards", ITEMS_GHOST_OFFSET + 0, ItemClassification.progression)