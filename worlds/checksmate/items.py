from enum import StrEnum
from sys import maxsize
from typing import Any, NamedTuple

from BaseClasses import Item, ItemClassification


LEGACY_CHESSMEN_GROUP = "Legacy Chessmen"
LEGACY_MATERIAL_ITEMS = frozenset({
    "Progressive Pawn",
    "Progressive Pawn Forwardness",
    "Progressive Minor Piece",
    "Progressive Major Piece",
    "Progressive Major To Queen",
    "Progressive Jack",
})
FUNDAMENTAL_ITEMS = frozenset({"Chessmen", "Material", "Castler"})
GEOMETRY_ITEMS = frozenset({"Board Files", "Board Ranks"})
INTERNAL_ITEMS = frozenset({"Victory", "Play as White", "Super-Size Me"})


class ItemizationMode(StrEnum):
    LEGACY = "legacy"
    FUNDAMENTAL = "fundamental"


def itemization_mode(options: Any) -> ItemizationMode:
    option = getattr(options, "progression_itemization", None)
    if option is not None and option.value == option.option_fundamental:
        return ItemizationMode.FUNDAMENTAL
    return ItemizationMode.LEGACY


class CMItem(Item):
    game: str = "ChecksMate"


class CMItemData(NamedTuple):
    code: int | None
    classification: ItemClassification
    quantity: int = 1  # maximum, not guaranteed
    material: int = 0  # pawns=100, minor=300, major=500, queen=900
    parents: tuple[tuple[str, int], ...] = ()


item_table = {
    "Play as White": CMItemData(4_901_000, ItemClassification.progression, material=50),
    "Progressive AI Intelligence Malus": CMItemData(4_901_001, ItemClassification.useful, quantity=5),
    # TODO: stop counting material if the board fills up with 23 pieces+pawns
    "Progressive Pawn": CMItemData(4_901_002, ItemClassification.progression, quantity=60, material=100),
    "Progressive Pawn Forwardness": CMItemData(
        4_901_003,
        ItemClassification.filler,
        quantity=13,
        parents=(("Progressive Pawn", 3),),
    ),
    # Bishops and Knights are worth 3.25 to 3.5, but some minor pieces are worse, so we assume 3.0 conservatively
    "Progressive Minor Piece": CMItemData(4_901_004, ItemClassification.progression, quantity=15, material=300),
    # Rooks are worth 5.25 to 5.5, but many major pieces are worse, so we assume 4.85, which stays under 5.0
    "Progressive Major Piece": CMItemData(4_901_005, ItemClassification.progression, quantity=11, material=485),
    # Queen pieces are pretty good, and even the weak ones are pretty close, so queens can stay 9.0 (but not 10.0)
    "Progressive Major To Queen": CMItemData(
        4_901_006,
        ItemClassification.progression,
        quantity=9,
        material=415,
        parents=(("Progressive Major Piece", 1),),
    ),
    "Progressive Jack": CMItemData(4_901_007, ItemClassification.progression, quantity=9, material=700),
    "Chessmen": CMItemData(4_901_008, ItemClassification.progression, quantity=107, material=100),
    "Victory": CMItemData(4_901_009, ItemClassification.progression),
    "Super-Size Me": CMItemData(4_901_010, ItemClassification.progression, quantity=0),  # :)
    "Material": CMItemData(4_901_011, ItemClassification.progression, quantity=321, material=400),
    "Castler": CMItemData(4_901_012, ItemClassification.progression, quantity=2, material=0),
    "Board Files": CMItemData(4_901_013, ItemClassification.progression, quantity=2, material=0),
    "Board Ranks": CMItemData(4_901_014, ItemClassification.progression, quantity=2, material=0),

    # Players have 3 pockets, which can be empty, or hold a pawn, minor piece, major piece, or queen.
    # Collected pocket items are distributed randomly to the 3 pockets in the above order.
    # Pocket pawns are playable onto home row instead of making a move
    # Pocket pieces start as minor pieces (e.g. Knight) - they upgrade in both Gem cost and type
    # Piece upgrades turn minor pieces into major pieces or major pieces into Queen - implementation may decide
    "Progressive Pocket": CMItemData(4_901_020, ItemClassification.progression, quantity=12, material=110),

    # Gems are a way to generate filler items and limit use of Pocket items
    # Gems are generated 1/turn and Pocket pieces cost 1 Gem per their material value
    # Turn off Pocket entirely to hide this item.
    "Progressive Pocket Gems": CMItemData(4_901_023, ItemClassification.filler, quantity=maxsize),
    # Allows the player to deploy pocket items one rank further from the home row, but not the opponent's home row
    "Progressive Pocket Range": CMItemData(4_901_024, ItemClassification.filler, quantity=6),

    "Progressive King Promotion": CMItemData(4_901_025, ItemClassification.progression, quantity=2, material=425),
    # Material is really about your ability to get checks, so here is the material value of a Commoner, but the AI gets
    # pretty confused when a royal piece isn't subject to check/mate, so this is a more powerful item than indicated for
    # the purpose of Checkmate Maxima.
    "Progressive Consul": CMItemData(4_901_026, ItemClassification.progression, quantity=2, material=325),
}

lookup_id_to_name: dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}

material_items: dict[str, CMItemData] = {
    item: item_data for (item, item_data) in item_table.items() if item_data.material > 0}
progression_items: dict[str, CMItemData] = {
    item: item_data for (item, item_data) in item_table.items() if
    item_data.classification == ItemClassification.progression}
useful_items: dict[str, CMItemData] = {
    item: item_data for (item, item_data) in item_table.items() if
    item_data.classification == ItemClassification.useful}
filler_items: dict[str, CMItemData] = {
    item: item_data for (item, item_data) in item_table.items() if
    item_data.classification == ItemClassification.filler}
item_name_groups = {
    # "Pawn": {"Pawn A", "Pawn B", "Pawn C", "Pawn D", "Pawn E", "Pawn F", "Pawn G", "Pawn H"},
    # "Enemy Pawn": {"Enemy Pawn A", "Enemy Pawn B", "Enemy Pawn C", "Enemy Pawn D",
    #                "Enemy Pawn E", "Enemy Pawn F", "Enemy Pawn G", "Enemy Pawn H"},
    # "Enemy Piece": {"Enemy Piece A", "Enemy Piece B", "Enemy Piece C", "Enemy Piece D",
    #                 "Enemy Piece F", "Enemy Piece G", "Enemy Piece H"},
    LEGACY_CHESSMEN_GROUP: {
        "Progressive Pawn",
        "Progressive Minor Piece",
        "Progressive Major Piece",
        "Progressive Jack",
        "Progressive Consul",
    },
    "Chessmen Pieces": {
        "Progressive Pawn",
        "Progressive Minor Piece",
        "Progressive Major Piece",
        "Progressive Jack",
        "Progressive Consul",
    },
}


def item_allowed_in_mode(
    item_name: str,
    itemization: ItemizationMode | str,
) -> bool:
    mode = ItemizationMode(itemization)
    if mode is ItemizationMode.FUNDAMENTAL:
        return item_name not in LEGACY_MATERIAL_ITEMS
    return item_name not in FUNDAMENTAL_ITEMS
