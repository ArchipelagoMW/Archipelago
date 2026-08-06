from typing import NamedTuple

from BaseClasses import Item, ItemClassification

from . import names

BASE_ID = 5450000  # Mega Man X5 item/location id namespace


class MMX5Item(Item):
    game = "Mega Man X5"


class ItemData(NamedTuple):
    code: int | None
    classification: ItemClassification
    count: int = 1  # copies placed in the pool


# Weapons are progression: weakness-based boss logic and several collectibles
# gated behind specific weapons will use them once rules are fleshed out.
item_table: dict[str, ItemData] = {
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

    # Launcher parts: progression under the launch goal (completion requires
    # all 8); useful otherwise (they still power launches for story flavor).
    # Classification resolved per-seed in create_item via options.
    names.ENIGMA_PART:  ItemData(BASE_ID + 14, ItemClassification.useful, 4),
    names.SHUTTLE_PART: ItemData(BASE_ID + 15, ItemClassification.useful, 4),

    names.FALCON_HEAD: ItemData(BASE_ID + 20, ItemClassification.progression),
    names.FALCON_BODY: ItemData(BASE_ID + 21, ItemClassification.progression),
    names.FALCON_ARM:  ItemData(BASE_ID + 22, ItemClassification.progression),
    names.FALCON_LEG:  ItemData(BASE_ID + 23, ItemClassification.progression),
    names.GAEA_HEAD:   ItemData(BASE_ID + 24, ItemClassification.progression),
    names.GAEA_BODY:   ItemData(BASE_ID + 25, ItemClassification.progression),
    names.GAEA_ARM:    ItemData(BASE_ID + 26, ItemClassification.progression),
    names.GAEA_LEG:    ItemData(BASE_ID + 27, ItemClassification.progression),

    # Secret armors (Zero Space capsule id 8), option-gated: count is set to 0
    # here and raised to 1 per item in create_items when the option is on.
    # `useful`, never progression - no location requires them, and each only
    # benefits one of the two characters.
    names.ULTIMATE_ARMOR: ItemData(BASE_ID + 28, ItemClassification.useful, 0),
    names.BLACK_ZERO:     ItemData(BASE_ID + 29, ItemClassification.useful, 0),

    # Stage access (option-gated, count 0 here). Progression whenever they
    # exist - with the option on, every location in a stage sits behind its
    # codes, so a seed is only beatable if fill respects them. One is
    # precollected as the starting stage; the other seven go in the pool.
    **{name: ItemData(BASE_ID + 30 + i, ItemClassification.progression, 0)
       for i, name in enumerate(names.ACCESS_ITEMS)},

    # filler
    names.SMALL_ENERGY: ItemData(BASE_ID + 40, ItemClassification.filler, 0),
}

event_table: dict[str, ItemData] = {
    names.VICTORY: ItemData(None, ItemClassification.progression),
}

item_groups = {
    "Weapons": {names.CSHOT, names.DARK_HOLD, names.GOO_SHAVER, names.GROUND_FIRE,
                names.TRI_THUNDER, names.F_LASER, names.SPIKE_BALL, names.WING_SPIRAL},
    "Falcon Armor": {names.FALCON_HEAD, names.FALCON_BODY, names.FALCON_ARM, names.FALCON_LEG},
    "Gaea Armor": {names.GAEA_HEAD, names.GAEA_BODY, names.GAEA_ARM, names.GAEA_LEG},
    # Hint/item-link aliases.
    "Armor": {names.FALCON_HEAD, names.FALCON_BODY, names.FALCON_ARM, names.FALCON_LEG,
              names.GAEA_HEAD, names.GAEA_BODY, names.GAEA_ARM, names.GAEA_LEG},
    "Tanks": {names.SUB_TANK, names.W_TANK, names.EX_TANK},
    "Launcher Parts": {names.ENIGMA_PART, names.SHUTTLE_PART},
    "Secret Armors": {names.ULTIMATE_ARMOR, names.BLACK_ZERO},
    "Access Codes": set(names.ACCESS_ITEMS),
}
