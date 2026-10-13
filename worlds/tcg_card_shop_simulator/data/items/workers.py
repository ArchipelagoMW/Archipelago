from BaseClasses import ItemClassification
from .. import ItemTypeEnum
from ...constants import ITEMS_WORKER_OFFSET



class Workers(ItemTypeEnum):
    ZACHERY = ("Worker - Zachery", ITEMS_WORKER_OFFSET + 0, ItemClassification.progression)
    TERENCE = ("Worker - Terence", ITEMS_WORKER_OFFSET + 1, ItemClassification.useful)
    DENNIS = ("Worker - Dennis", ITEMS_WORKER_OFFSET + 2, ItemClassification.useful)
    CLARK = ("Worker - Clark", ITEMS_WORKER_OFFSET + 3, ItemClassification.useful)
    ANGUS = ("Worker - Angus", ITEMS_WORKER_OFFSET + 4, ItemClassification.useful)
    BENJI = ("Worker - Benji", ITEMS_WORKER_OFFSET + 5, ItemClassification.useful)
    LAUREN = ("Worker - Lauren", ITEMS_WORKER_OFFSET + 6, ItemClassification.useful)
    AXEL = ("Worker - Axel", ITEMS_WORKER_OFFSET + 7, ItemClassification.useful)
    ALEXANDER = ("Worker - Alexander", ITEMS_WORKER_OFFSET + 8, ItemClassification.useful)