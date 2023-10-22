from typing import Dict, NamedTuple, Optional

from BaseClasses import Item, ItemClassification


class CMItem(Item):
    game: str = "ChecksMate"


class CMItemData(NamedTuple):
    code: Optional[int]
    classification: ItemClassification
    quantity: int = 1 # maximum, not guaranteed
    material: int = 0 # pawns=2, minor=6, major=10, queen=18 - doubled to account for 0.5 values
    parents: list[str] = None


item_table = {
    "Play as White": CMItemData(4_000, ItemClassification.progression, material=50),
    "Progressive Engine ELO Lobotomy": CMItemData(4_001, ItemClassification.useful, quantity=15),
    "Progressive Pawn": CMItemData(4_002, ItemClassification.progression, quantity=14, material=100),
    "Progressive Pawn Forwardness": CMItemData(4_003, ItemClassification.filler, quantity=8, parents=["Progressive Pawn"]),
    # Bishops and Knights are worth 3.25 to 3.5, but some minor pieces are worse, so we assume 3.0 conservatively
    "Progressive Minor Piece": CMItemData(4_004, ItemClassification.progression, quantity=9, material=300),
    # Rooks are worth 5.25 to 5.5, but many major pieces are worse, so we assume 4.85, which stays under 5.0
    "Progressive Major Piece": CMItemData(4_005, ItemClassification.progression, quantity=9, material=485),
    # Queen pieces are pretty good, and even the weak ones are pretty close, so queens can stay 9.0 (but not 10.0)
    "Progressive Major To Queen": CMItemData(4_006, ItemClassification.useful, quantity=7, material=415,
                                             parents=["Progressive Major Piece"]),
    # TODO: implement extra moves
    # "Progressive Opening Move": CMItemData(4_007, ItemClassification.useful, quantity=3),
    # "Progressive Enemy Pawn": CMItemData(4_008, ItemClassification.trap, quantity=8),
    # "Progressive Enemy Piece": CMItemData(4_009, ItemClassification.trap, quantity=7),
    "Enemy Pawn A": CMItemData(4_030, ItemClassification.progression),
    "Enemy Pawn B": CMItemData(4_031, ItemClassification.progression),
    "Enemy Pawn C": CMItemData(4_032, ItemClassification.progression),
    "Enemy Pawn D": CMItemData(4_033, ItemClassification.progression),
    "Enemy Pawn E": CMItemData(4_034, ItemClassification.progression),
    "Enemy Pawn F": CMItemData(4_035, ItemClassification.progression),
    "Enemy Pawn G": CMItemData(4_036, ItemClassification.progression),
    "Enemy Pawn H": CMItemData(4_037, ItemClassification.progression),
    "Enemy Piece A": CMItemData(4_038, ItemClassification.progression),
    "Enemy Piece B": CMItemData(4_039, ItemClassification.progression),
    "Enemy Piece C": CMItemData(4_040, ItemClassification.progression),
    "Enemy Piece D": CMItemData(4_041, ItemClassification.progression),
    "Enemy Piece F": CMItemData(4_042, ItemClassification.progression),
    "Enemy Piece G": CMItemData(4_043, ItemClassification.progression),
    "Enemy Piece H": CMItemData(4_044, ItemClassification.progression),
    # TODO: implement castling rule & guarantee major piece on that side for Locations
    # "Play 00 Castle": CMItemData(4_010, ItemClassification.progression),
    # "Play 000 Castle": CMItemData(4_011, ItemClassification.progression),
    # TODO: consider breaking passant into individual pawns, or progressive for outer..center pawns
    "Play En Passant": CMItemData(4_012, ItemClassification.progression),

    # Players have 3 pockets, which can be empty, or hold a pawn, minor piece, major piece, or queen.
    # Collected pocket items are distributed randomly to the 3 pockets in the above order.
    # Pocket pawns are playable onto home row instead of making a move
    # Pocket pieces start as minor pieces (e.g. Knight) - they upgrade in both Gem cost and type
    # Piece upgrades turn minor pieces into major pieces or major pieces into Queen - implementation may decide
    "Progressive Pocket": CMItemData(4_020, ItemClassification.progression, quantity=12, material=100),

    # Gems are a way to generate filler items and limit use of Pocket items
    # Gems are generated 1/turn and Pocket pieces cost 1 Gem per their material value
    # Turn off Pocket entirely to hide this item. Also you can't yet EleGiggle
    # You should probably use excluded items though.
    "Progressive Pocket Gems": CMItemData(4_023, ItemClassification.filler),
    # Allows the player to deploy pocket items one rank further from the home row, but not the opponent's home row
    "Progressive Pocket Range": CMItemData(4_024, ItemClassification.filler, quantity=6),

    # == Possible pocket implementation ==
    # "Progressive Pocket Pawn": CMItemData(4_021, ItemClassification.progression, quantity=3, material=90),
    # "Progressive Pocket Pawn to Piece": CMItemData(4_022, ItemClassification.progression, quantity=3, material=190,
    #                                               parents=["Progressive Pocket Pawn"]),
    # "Progressive Pocket Piece Promotion": parents=["Progressive Pocket Pawn to Piece",
    #          "Progressive Pocket Pawn"]),
    # == End possible pocket implementation ==
}

lookup_id_to_name: Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}


def create_item_with_correct_settings(player: int, name: str) -> Item:
    data = item_table[name]

    item = Item(name, data.classification, data.code, player)

    return item
