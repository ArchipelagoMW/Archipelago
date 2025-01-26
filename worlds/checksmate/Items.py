import math
from sys import maxsize
from typing import Dict, NamedTuple, Optional, List, Union

from BaseClasses import Item, ItemClassification


class CMItem(Item):
    game: str = "ChecksMate"


class CMItemData(NamedTuple):
    code: Optional[int]
    classification: ItemClassification
    quantity: int = 1  # maximum, not guaranteed
    material: int = 0  # pawns=100, minor=300, major=500, queen=900
    # for each given parent item, the maximum number of child items which may be present
    parents: List[List[Union[str, int]]] = []


item_table = {
    "Play as White": CMItemData(4_901_000, ItemClassification.progression, material=50),
    "Progressive Engine ELO Lobotomy": CMItemData(4_901_001, ItemClassification.useful, quantity=5),
    # TODO: stop counting material if the board fills up with 23 pieces+pawns
    "Progressive Pawn": CMItemData(4_901_002, ItemClassification.progression, quantity=40, material=100),
    "Progressive Pawn Forwardness": CMItemData(4_901_003, ItemClassification.filler, quantity=13, parents=[
        ["Progressive Pawn", 3]]),
    # Bishops and Knights are worth 3.25 to 3.5, but some minor pieces are worse, so we assume 3.0 conservatively
    "Progressive Minor Piece": CMItemData(4_901_004, ItemClassification.progression, quantity=15, material=300),
    # Rooks are worth 5.25 to 5.5, but many major pieces are worse, so we assume 4.85, which stays under 5.0
    "Progressive Major Piece": CMItemData(4_901_005, ItemClassification.progression, quantity=11, material=485),
    # Queen pieces are pretty good, and even the weak ones are pretty close, so queens can stay 9.0 (but not 10.0)
    "Progressive Major To Queen": CMItemData(4_901_006, ItemClassification.progression, quantity=9, material=415,
                                             parents=[["Progressive Major Piece", 1]]),
    "Victory": CMItemData(4_901_009, ItemClassification.progression),
    "Super-Size Me": CMItemData(4_901_010, ItemClassification.progression, quantity=0),  # :)
    # TODO: implement extra moves
    # "Progressive Enemy Pawn": CMItemData(4_907, ItemClassification.trap, quantity=8),
    # "Progressive Enemy Piece": CMItemData(4_908, ItemClassification.trap, quantity=7),
    # "Progressive Opening Move": CMItemData(4_013, ItemClassification.useful, quantity=3),

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

    "Progressive King Promotion": CMItemData(4_901_025, ItemClassification.progression, quantity=2, material=350),
    # Material is really about your ability to get checks, so here is the material value of a Commoner, but the AI gets
    # pretty confused when a royal piece isn't subject to check/mate, so this is a more powerful item than indicated for
    # the purpose of Checkmate Maxima. TODO: Consider adding a property "tactics", used for some complex locations.
    "Progressive Consul": CMItemData(4_901_026, ItemClassification.progression, quantity=2, material=325),

    # 4_901_030 - 4_901_044 are unused, previously N
    # TODO: implement castling rule & guarantee major piece on that side for Locations
    # "Play 00 Castle": CMItemData(4_014, ItemClassification.progression),
    # "Play 000 Castle": CMItemData(4_015, ItemClassification.progression),
    # TODO: consider breaking passant into individual pawns, or progressive for outer..center pawns
    # "Play En Passant": CMItemData(4_011, ItemClassification.progression),

    # == Possible pocket implementation ==
    # "Progressive Pocket Pawn": CMItemData(4_021, ItemClassification.progression, quantity=3, material=90),
    # "Progressive Pocket Pawn to Piece": CMItemData(4_022, ItemClassification.progression, quantity=3, material=190,
    #                                               parents=["Progressive Pocket Pawn"]),
    # "Progressive Pocket Piece Promotion": parents=["Progressive Pocket Pawn to Piece",
    #          "Progressive Pocket Pawn"]),
    # == End possible pocket implementation ==
}

lookup_id_to_name: Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}

material_items: Dict[str, CMItemData] = {
    item: item_data for (item, item_data) in item_table.items() if item_data.material > 0}
progression_items: Dict[str, CMItemData] = {
    item: item_data for (item, item_data) in item_table.items() if
    item_data.classification == ItemClassification.progression}
useful_items: Dict[str, CMItemData] = {
    item: item_data for (item, item_data) in item_table.items() if
    item_data.classification == ItemClassification.useful}
filler_items: Dict[str, CMItemData] = {
    item: item_data for (item, item_data) in item_table.items() if
    item_data.classification == ItemClassification.filler}
item_name_groups = {
    # "Pawn": {"Pawn A", "Pawn B", "Pawn C", "Pawn D", "Pawn E", "Pawn F", "Pawn G", "Pawn H"},
    # "Enemy Pawn": {"Enemy Pawn A", "Enemy Pawn B", "Enemy Pawn C", "Enemy Pawn D",
    #                "Enemy Pawn E", "Enemy Pawn F", "Enemy Pawn G", "Enemy Pawn H"},
    # "Enemy Piece": {"Enemy Piece A", "Enemy Piece B", "Enemy Piece C", "Enemy Piece D",
    #                 "Enemy Piece F", "Enemy Piece G", "Enemy Piece H"},
    "Chessmen": {"Progressive Pawn", "Progressive Minor Piece", "Progressive Major Piece", "Progressive Consul"},
}
