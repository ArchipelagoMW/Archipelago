from BaseClasses import ItemClassification
from .. import ItemTypeEnum
from ...constants import ITEMS_FILLER_OFFSET


class Fillers(ItemTypeEnum):
    SMALL_XP = ("Small Xp",ITEMS_FILLER_OFFSET + 0, ItemClassification.filler)
    SMALL_MONEY = ("Small Money", ITEMS_FILLER_OFFSET + 1, ItemClassification.filler)
    MEDIUM_XP = ("Medium Xp", ITEMS_FILLER_OFFSET + 2, ItemClassification.filler)
    MEDIUM_MONEY = ("Medium Money", ITEMS_FILLER_OFFSET + 3, ItemClassification.filler)
    LARGE_XP = ("Large Xp", ITEMS_FILLER_OFFSET + 4, ItemClassification.filler)
    LARGE_MONEY = ("Large Money", ITEMS_FILLER_OFFSET + 5, ItemClassification.filler)
    RANDOM_CARD = ("Random Card", ITEMS_FILLER_OFFSET + 6, ItemClassification.filler)
    # RANDOM_NEW_CARD = ("Random New Card", ITEMS_FILLER_OFFSET + 7, ItemClassification.filler)
    PROGRESSIVE_CUSTOMER_MONEY = ("Progressive Customer Money", ITEMS_FILLER_OFFSET + 8, ItemClassification.filler)
    INCREASE_CARD_LUCK = ("Increase Card Luck", ITEMS_FILLER_OFFSET + 9, ItemClassification.filler)

def get_filler_default_dict():
    return {
        filler.value: 50
        for filler in Fillers
    }


