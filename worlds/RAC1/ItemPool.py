from BaseClasses import ItemClassification
from .data import Items
from .data.Items import ItemData


def get_classification(item: ItemData) -> ItemClassification:
    if (item in Items.PLANETS
            or item in Items.ALL_PACKS
            or item in Items.GADGETS
            or item in Items.ALL_BOOTS
            or item in Items.GOLD_BOLTS):
        return ItemClassification.progression
    if item in [
        Items.TAUNTER,
        Items.O2_MASK,
        Items.PILOTS_HELMET,
        Items.PROGRESSIVE_HELMET,
        Items.CODEBOT,
        Items.RARITANIUM,
        Items.HOVERBOARD,
        Items.ZOOMERATOR,
        Items.PROGRESSIVE_HOVERBOARD,
        Items.BOMB_GLOVE,
        Items.PROGRESSIVE_BOMB,
        Items.BLASTER,
        Items.MINE_GLOVE,
        Items.PROGRESSIVE_MINE,
        Items.DEVASTATOR,
        Items.PROGRESSIVE_DEVASTATOR,
        Items.VISIBOMB,
        Items.RYNO,
        Items.PROGRESSIVE_TRADE,
    ]:
        return ItemClassification.progression
    if (item == Items.SONIC_SUMMONER
            or item in Items.ALL_WEAPONS
            or item in Items.ALL_EXTRA_ITEMS):
        return ItemClassification.useful

    return ItemClassification.filler
