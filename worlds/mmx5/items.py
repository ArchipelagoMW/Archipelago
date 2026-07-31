from typing import Dict, NamedTuple, Optional

from BaseClasses import Item, ItemClassification

from . import names

BASE_ID = 5450000  # Mega Man X5 item/location id namespace


class MMX5Item(Item):
    game = "Mega Man X5"


class ItemData(NamedTuple):
    code: Optional[int]
    classification: ItemClassification
    count: int = 1  # copies placed in the pool


# Weapons are progression: weakness-based boss logic and several collectibles
# gated behind specific weapons will use them once rules are fleshed out.
item_table: Dict[str, ItemData] = {
    names.CSHOT:       ItemData(BASE_ID + 0, ItemClassification.progression),
    names.DARK_HOLD:   ItemData(BASE_ID + 1, ItemClassification.progression),
    names.GOO_SHAVER:  ItemData(BASE_ID + 2, ItemClassification.progression),
    names.GROUND_FIRE: ItemData(BASE_ID + 3, ItemClassification.progression),
    names.TRI_THUNDER: ItemData(BASE_ID + 4, ItemClassification.progression),
    names.F_LASER:     ItemData(BASE_ID + 5, ItemClassification.progression),
    names.SPIKE_BALL:  ItemData(BASE_ID + 6, ItemClassification.progression),
    names.WING_SPIRAL: ItemData(BASE_ID + 7, ItemClassification.progression),

    names.HEART_TANK:  ItemData(BASE_ID + 10, ItemClassification.useful, 8),
    names.SUB_TANK:    ItemData(BASE_ID + 11, ItemClassification.useful, 2),
    names.W_TANK:      ItemData(BASE_ID + 12, ItemClassification.useful),
    names.EX_TANK:     ItemData(BASE_ID + 13, ItemClassification.useful),

    names.FALCON_HEAD: ItemData(BASE_ID + 20, ItemClassification.progression),
    names.FALCON_BODY: ItemData(BASE_ID + 21, ItemClassification.progression),
    names.FALCON_ARM:  ItemData(BASE_ID + 22, ItemClassification.progression),
    names.FALCON_LEG:  ItemData(BASE_ID + 23, ItemClassification.progression),
    names.GAEA_HEAD:   ItemData(BASE_ID + 24, ItemClassification.progression),
    names.GAEA_BODY:   ItemData(BASE_ID + 25, ItemClassification.progression),
    names.GAEA_ARM:    ItemData(BASE_ID + 26, ItemClassification.progression),
    names.GAEA_LEG:    ItemData(BASE_ID + 27, ItemClassification.progression),

    # filler
    names.SMALL_ENERGY: ItemData(BASE_ID + 40, ItemClassification.filler, 0),
}

event_table: Dict[str, ItemData] = {
    names.VICTORY: ItemData(None, ItemClassification.progression),
}

item_groups = {
    "Weapons": {names.CSHOT, names.DARK_HOLD, names.GOO_SHAVER, names.GROUND_FIRE,
                names.TRI_THUNDER, names.F_LASER, names.SPIKE_BALL, names.WING_SPIRAL},
    "Falcon Armor": {names.FALCON_HEAD, names.FALCON_BODY, names.FALCON_ARM, names.FALCON_LEG},
    "Gaea Armor": {names.GAEA_HEAD, names.GAEA_BODY, names.GAEA_ARM, names.GAEA_LEG},
}
