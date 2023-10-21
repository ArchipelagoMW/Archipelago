from typing import Dict, NamedTuple, Optional

from BaseClasses import Item, ItemClassification


class CMItem(Item):
    game: str = "ChecksMate"


class CMItemData(NamedTuple):
    code: Optional[int]
    classification: ItemClassification
    quantity: int = 1 # maximum, not guaranteed
    material: int = 0 # pawns=2, minor=6, major=10, queen=18 - doubled to account for 0.5 values
    parent: str = None


item_table = {
    "Play as White": CMItemData(4_000, ItemClassification.progression, material=1),
    "Progressive Engine ELO Lobotomy": CMItemData(4_001, ItemClassification.useful, quantity=15),
    "Progressive Pawn": CMItemData(4_002, ItemClassification.progression, material=2),
    "Progressive Pawn Forwardness": CMItemData(4_003, ItemClassification.filler, parent="Progressive Pawn"),
    "Progressive Minor Piece": CMItemData(4_004, ItemClassification.progression, material=6),
    "Progressive Major Piece": CMItemData(4_005, ItemClassification.progression, material=10),
    "Progressive Major To Queen": CMItemData(4_006, ItemClassification.useful, material=8,
                                             parent="Progressive Major Piece"),
    # TODO: implement extra moves
    # "Progressive Opening Move": CMItemData(4_007, ItemClassification.useful, quantity=3),
    "Progressive Enemy Pawn": CMItemData(4_008, ItemClassification.trap, quantity=8),
    "Progressive Enemy Piece": CMItemData(4_009, ItemClassification.trap, quantity=7),
    # TODO: implement castling rule & guarantee major piece on that side for Locations
    # "Play 00 Castle": CMItemData(4_010, ItemClassification.progression),
    # "Play 000 Castle": CMItemData(4_011, ItemClassification.progression),
    # TODO: consider breaking passant into individual pawns, or progressive for outer..center pawns
    "Play En Passant": CMItemData(4_012, ItemClassification.progression),
    # Pocket pawns are playable onto home row instead of making a move
    "Progressive Pocket Pawn": CMItemData(4_020, ItemClassification.useful, quantity=3, material=1),
    # Pocket pieces start as minor pieces (e.g. Knight) - they upgrade in both Gem cost and type
    "Progressive Pocket Pawn to Piece": CMItemData(4_021, ItemClassification.useful, quantity=3, material=2,
                                                   parent="Progressive Pocket Pawn"),
    # Piece upgrades turn minor pieces into major pieces or major pieces into Queen - implementation may decide
    "Progressive Pocket Piece Promotion": CMItemData(4_022, ItemClassification.useful, quantity=6, material=2,
                                                     parent="Progressive Pocket Pawn to Piece"),
    # Gems are a way to generate filler items and limit use of Pocket items
    # Gems are generated 1/turn and Pocket pieces cost 1 Gem per their material value
    # Turn off Pocket entirely to hide this item. Also you can't yet EleGiggle
    # You can probably use excluded items though
    "Progressive Pocket Gems": CMItemData(4_023, ItemClassification.filler, parent="Progressive Pocket Pawn"),
}

lookup_id_to_name: Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}
