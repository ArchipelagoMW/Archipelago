from BaseClasses import ItemClassification
from .. import ItemTypeEnum
from ...constants import ITEMS_PROGRESSIVE_BLOCKERS_OFFSET


class Blockers(ItemTypeEnum):
    GRADING_UNLOCK = ("Grading Unlock", ITEMS_PROGRESSIVE_BLOCKERS_OFFSET + 0, ItemClassification.progression)