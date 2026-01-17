from typing import NamedTuple

from BaseClasses import Item
from .Names import ItemName


class DiddyKongRacingItem(Item):
    game: str = "Diddy Kong Racing"


class ItemData(NamedTuple):
    dkr_id: int
    count: int


BALLOON_TABLE: dict[str, ItemData] = {
    ItemName.TIMBERS_ISLAND_BALLOON: ItemData(1616000, 7),
    ItemName.DINO_DOMAIN_BALLOON: ItemData(1616001, 8),
    ItemName.SNOWFLAKE_MOUNTAIN_BALLOON: ItemData(1616002, 8),
    ItemName.SHERBET_ISLAND_BALLOON: ItemData(1616003, 8),
    ItemName.DRAGON_FOREST_BALLOON: ItemData(1616004, 8),
    ItemName.FUTURE_FUN_LAND_BALLOON: ItemData(1616005, 8)
}

KEY_TABLE: dict[str, ItemData] = {
    ItemName.FIRE_MOUNTAIN_KEY: ItemData(1616006, 1),
    ItemName.ICICLE_PYRAMID_KEY: ItemData(1616007, 1),
    ItemName.DARKWATER_BEACH_KEY: ItemData(1616008, 1),
    ItemName.SMOKEY_CASTLE_KEY: ItemData(1616009, 1)
}

AMULET_TABLE: dict[str, ItemData] = {
    ItemName.WIZPIG_AMULET_PIECE: ItemData(1616010, 4),
    ItemName.TT_AMULET_PIECE: ItemData(1616011, 4)
}

ALL_ITEM_TABLE: dict[str, ItemData] = {
    **BALLOON_TABLE,
    **KEY_TABLE,
    **AMULET_TABLE
}

ITEM_NAME_GROUPS: dict[str, set[str]] = {
    "Balloons": {ItemName.TIMBERS_ISLAND_BALLOON, ItemName.DINO_DOMAIN_BALLOON, ItemName.SNOWFLAKE_MOUNTAIN_BALLOON,
                 ItemName.SHERBET_ISLAND_BALLOON, ItemName.FUTURE_FUN_LAND_BALLOON},
    "Keys": {ItemName.FIRE_MOUNTAIN_KEY, ItemName.ICICLE_PYRAMID_KEY, ItemName.DARKWATER_BEACH_KEY,
             ItemName.SMOKEY_CASTLE_KEY},
    "Amulets": {ItemName.WIZPIG_AMULET_PIECE, ItemName.TT_AMULET_PIECE},
    "TI Balloon": {ItemName.TIMBERS_ISLAND_BALLOON},
    "DD Balloon": {ItemName.DINO_DOMAIN_BALLOON},
    "SM Balloon": {ItemName.SNOWFLAKE_MOUNTAIN_BALLOON},
    "SI Balloon": {ItemName.SHERBET_ISLAND_BALLOON},
    "DF Balloon": {ItemName.DRAGON_FOREST_BALLOON},
    "FFL Balloon": {ItemName.FUTURE_FUN_LAND_BALLOON},
    "Wizpig Amulet": {ItemName.WIZPIG_AMULET_PIECE},
    "TT Amulet": {ItemName.TT_AMULET_PIECE}
}
