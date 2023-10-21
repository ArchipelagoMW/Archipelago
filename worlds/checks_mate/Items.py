from typing import Dict, NamedTuple, Optional

from BaseClasses import Item, ItemClassification


class CMItem(Item):
    game: str = "ChecksMate"


class CMItemData(NamedTuple):
    code: Optional[int]
    classification: ItemClassification
    value: int


item_table = {
    "Pawn A": CMItemData(4_000, ItemClassification.useful, 1),
    "Pawn B": CMItemData(4_001, ItemClassification.progression, 1),
    "Pawn C": CMItemData(4_002, ItemClassification.useful, 1),
    "Pawn D": CMItemData(4_003, ItemClassification.progression, 1),
    "Pawn E": CMItemData(4_004, ItemClassification.progression, 1),
    "Pawn F": CMItemData(4_005, ItemClassification.useful, 1),
    "Pawn G": CMItemData(4_006, ItemClassification.progression, 1),
    "Pawn H": CMItemData(4_007, ItemClassification.useful, 1),
    "Rook A": CMItemData(4_008, ItemClassification.useful, 5),
    "Rook H": CMItemData(4_009, ItemClassification.progression, 5),
    "Bishop B": CMItemData(4_010, ItemClassification.progression, 3),
    "Bishop G": CMItemData(4_011, ItemClassification.useful, 3),
    "Knight C": CMItemData(4_012, ItemClassification.useful, 3),
    "Knight F": CMItemData(4_013, ItemClassification.progression, 3),
    "Queen": CMItemData(4_014, ItemClassification.progression, 9)
}

lookup_id_to_name: Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}
