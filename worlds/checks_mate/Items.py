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
    "Progressive Pawn": CMItemData(4_002, ItemClassification.useful, material=100),
    "Progressive Pawn Forwardness": CMItemData(4_003, ItemClassification.filler, parents=["Progressive Pawn"]),
    "Progressive Minor Piece": CMItemData(4_004, ItemClassification.progression, material=350),
    "Progressive Major Piece": CMItemData(4_005, ItemClassification.progression, material=550),
    "Progressive Major To Queen": CMItemData(4_006, ItemClassification.useful, material=350,
                                             parents=["Progressive Major Piece"]),
    # TODO: implement extra moves
    # "Progressive Opening Move": CMItemData(4_007, ItemClassification.useful, quantity=3),
    # "Progressive Enemy Pawn": CMItemData(4_008, ItemClassification.trap, quantity=8),
    "Enemy Pawn A": CMItemData(4_030, ItemClassification.trap),
    "Enemy Pawn B": CMItemData(4_031, ItemClassification.trap),
    "Enemy Pawn C": CMItemData(4_032, ItemClassification.trap),
    "Enemy Pawn D": CMItemData(4_033, ItemClassification.trap),
    "Enemy Pawn E": CMItemData(4_034, ItemClassification.trap),
    "Enemy Pawn F": CMItemData(4_035, ItemClassification.trap),
    "Enemy Pawn G": CMItemData(4_036, ItemClassification.trap),
    "Enemy Pawn H": CMItemData(4_037, ItemClassification.trap),
    "Enemy Piece A": CMItemData(4_038, ItemClassification.trap),
    "Enemy Piece B": CMItemData(4_039, ItemClassification.trap),
    "Enemy Piece C": CMItemData(4_040, ItemClassification.trap),
    "Enemy Piece D": CMItemData(4_041, ItemClassification.trap),
    "Enemy Piece F": CMItemData(4_042, ItemClassification.trap),
    "Enemy Piece G": CMItemData(4_043, ItemClassification.trap),
    "Enemy Piece H": CMItemData(4_044, ItemClassification.trap),
    # "Progressive Enemy Piece": CMItemData(4_009, ItemClassification.trap, quantity=7),
    # TODO: implement castling rule & guarantee major piece on that side for Locations
    # "Play 00 Castle": CMItemData(4_010, ItemClassification.progression),
    # "Play 000 Castle": CMItemData(4_011, ItemClassification.progression),
    # TODO: consider breaking passant into individual pawns, or progressive for outer..center pawns
    "Play En Passant": CMItemData(4_012, ItemClassification.progression),
    # Pocket pawns are playable onto home row instead of making a move
    "Progressive Pocket Pawn": CMItemData(4_020, ItemClassification.useful, quantity=3, material=90),
    # Pocket pieces start as minor pieces (e.g. Knight) - they upgrade in both Gem cost and type
    "Progressive Pocket Pawn to Piece": CMItemData(4_021, ItemClassification.useful, quantity=3, material=190,
                                                   parents=["Progressive Pocket Pawn"]),
    # Piece upgrades turn minor pieces into major pieces or major pieces into Queen - implementation may decide
    "Progressive Pocket Piece Promotion": CMItemData(4_022, ItemClassification.useful, quantity=6, material=150,
                                                     parents=["Progressive Pocket Pawn to Piece",
                                                              "Progressive Pocket Pawn"]),
    # Gems are a way to generate filler items and limit use of Pocket items
    # Gems are generated 1/turn and Pocket pieces cost 1 Gem per their material value
    # Turn off Pocket entirely to hide this item. Also you can't yet EleGiggle
    # You can probably use excluded items though
    "Progressive Pocket Gems": CMItemData(4_023, ItemClassification.filler),
}

lookup_id_to_name: Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}
