from BaseClasses import ItemClassification
from .. import ItemTypeEnum
from ...constants import ITEMS_DIY_OFFSET


class DIYItems(ItemTypeEnum):
    PROGRESSIVE_CARD_TABLE = ("Progressive Card Table", ITEMS_DIY_OFFSET + 0, ItemClassification.progression)
    PROGRESSIVE_CARD_DISPLAY = ("Progressive Card Display", ITEMS_DIY_OFFSET + 1, ItemClassification.useful)
    PROGRESSIVE_PERSONAL_SHELF = ("Progressive Personal Shelf", ITEMS_DIY_OFFSET + 2, ItemClassification.useful)
    PROGRESSIVE_AUTO_SCENT = ("Progressive Auto Scent", ITEMS_DIY_OFFSET + 3, ItemClassification.progression)
    PROGRESSIVE_WAREHOUSE_SHELF = ("Progressive Warehouse Shelf", ITEMS_DIY_OFFSET + 4, ItemClassification.progression)
    PROGRESSIVE_WALL_DISPLAY_CASE = ("Progressive Wall Display Case", ITEMS_DIY_OFFSET + 8, ItemClassification.useful)
    PROGRESSIVE_CARD_PROJECTOR = ("Progressive Card Projector", ITEMS_DIY_OFFSET + 9, ItemClassification.progression)
    PROGRESSIVE_PACK_OPENER = ("Progressive Pack Opener", ITEMS_DIY_OFFSET + 10, ItemClassification.useful)
    PROGRESSIVE_SHELF = ("Progressive Shelf", ITEMS_DIY_OFFSET + 11, ItemClassification.progression)
    PROGRESSIVE_PLAY_TABLE = ("Progressive Play Table", ITEMS_DIY_OFFSET + 12, ItemClassification.progression)
    WORKBENCH = ("Workbench", ITEMS_DIY_OFFSET + 13, ItemClassification.progression)
    TRASH_BIN = ("Trash Bin", ITEMS_DIY_OFFSET + 14, ItemClassification.useful)
    CHECKOUT_COUNTER = ("Checkout Counter", ITEMS_DIY_OFFSET + 15, ItemClassification.progression)
    PROGRESSIVE_LARGE_SHELF = ("Progressive Large Shelf", ITEMS_DIY_OFFSET + 16, ItemClassification.useful)
    TOURNAMENT_PRIZE_SHELF = ("Tournament Prize Shelf", ITEMS_DIY_OFFSET + 17, ItemClassification.progression)
    SCANNER = ("Scanner", ITEMS_DIY_OFFSET + 18, ItemClassification.progression)
    EMPTY_BOX_STORAGE = ("Empty Box Storage", ITEMS_DIY_OFFSET + 19, ItemClassification.useful)
    BULK_DONATION_BOX = ("Bulk Donation Box", ITEMS_DIY_OFFSET + 20, ItemClassification.useful)
    CARD_STORAGE_SHELF = ("Card Storage Shelf", ITEMS_DIY_OFFSET + 21, ItemClassification.useful)