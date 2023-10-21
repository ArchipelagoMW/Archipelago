from typing import Dict, NamedTuple, Optional

from BaseClasses import Location


class CMLocation(Location):
    game: str = "ChecksMate"


class CMLocationData(NamedTuple):
    code: Optional[int]
    capture: bool
    difficult: bool


location_table = {
    "Capture Pawn A": CMLocationData(4_000, True, False),
    "Capture Pawn B": CMLocationData(4_001, True, False),
    "Capture Pawn C": CMLocationData(4_002, True, False),
    "Capture Pawn D": CMLocationData(4_003, True, False),
    "Capture Pawn E": CMLocationData(4_004, True, False),
    "Capture Pawn F": CMLocationData(4_005, True, False),
    "Capture Pawn G": CMLocationData(4_006, True, False),
    "Capture Pawn H": CMLocationData(4_007, True, False),
    "Capture Rook A": CMLocationData(4_008, True, False),
    "Capture Rook H": CMLocationData(4_009, True, False),
    "Capture Bishop B": CMLocationData(4_010, True, False),
    "Capture Bishop G": CMLocationData(4_011, True, False),
    "Capture Knight C": CMLocationData(4_012, True, False),
    "Capture Knight F": CMLocationData(4_013, True, False),
    "Capture Queen": CMLocationData(4_014, True, False),
    "Checkmate": CMLocationData(4_015, True, False)
}

lookup_id_to_name: Dict[int, str] = {data.code: item_name for item_name, data in location_table.items() if data.code}
