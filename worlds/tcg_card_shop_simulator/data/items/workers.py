from BaseClasses import ItemClassification
from .. import ItemTypeEnum
from ...constants import ITEMS_WORKER_OFFSET



class Workers(ItemTypeEnum):
    ZACHERY = ("Zachery", ITEMS_WORKER_OFFSET + 1, ItemClassification.progression)
    TERENCE = ("Terence", ITEMS_WORKER_OFFSET + 2, ItemClassification.useful)
    DENNIS = ("Dennis", ITEMS_WORKER_OFFSET + 3, ItemClassification.useful)
    CLARK = ("Clark", ITEMS_WORKER_OFFSET + 4, ItemClassification.useful)
    ANGUS = ("Angus", ITEMS_WORKER_OFFSET + 5, ItemClassification.useful)
    BENJI = ("Benji", ITEMS_WORKER_OFFSET + 6, ItemClassification.useful)
    LAUREN = ("Lauren", ITEMS_WORKER_OFFSET + 7, ItemClassification.useful)
    AXEL = ("Axel", ITEMS_WORKER_OFFSET + 8, ItemClassification.useful)
    ALEXANDER = ("Alexander", ITEMS_WORKER_OFFSET + 9, ItemClassification.useful)


WORKERS_ITEM_BY_ID = {
    item.item_id: item
    for item in Workers
}