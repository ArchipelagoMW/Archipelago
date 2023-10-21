from typing import Dict, NamedTuple, Optional

from BaseClasses import Location


class CMLocation(Location):
    game: str = "ChecksMate"


class CMLocationData(NamedTuple):
    code: Optional[int]
    capture: bool
    difficult: bool


location_table = {
    # capture individual pieces and pawns
    "Capture Pawn A": CMLocationData(4_000, True, False),
    "Capture Pawn B": CMLocationData(4_001, True, False),
    "Capture Pawn C": CMLocationData(4_002, True, False),
    "Capture Pawn D": CMLocationData(4_003, True, False),
    "Capture Pawn E": CMLocationData(4_004, True, False),
    "Capture Pawn F": CMLocationData(4_005, True, False),
    "Capture Pawn G": CMLocationData(4_006, True, False),
    "Capture Pawn H": CMLocationData(4_007, True, False),
    "Capture Piece A": CMLocationData(4_008, True, False),
    "Capture Piece B": CMLocationData(4_010, True, False),
    "Capture Piece C": CMLocationData(4_012, True, False),
    "Capture Piece D": CMLocationData(4_014, True, False),
    "Capture Piece F": CMLocationData(4_013, True, False),
    "Capture Piece G": CMLocationData(4_011, True, False),
    "Capture Piece H": CMLocationData(4_009, True, False),
    # some first locations
    "Bongcloud Once": CMLocationData(4_015, True, False),
    "Bongcloud Center": CMLocationData(4_016, True, False),
    "Bongcloud A File": CMLocationData(4_017, True, False),
    "Bongcloud Capture": CMLocationData(4_018, True, False),
    "Bongcloud Promotion": CMLocationData(4_019, True, False),
    # capture series of pieces and pawns within 1 game
    "Capture 2 Pawns": CMLocationData(4_020, True, False),
    "Capture 3 Pawns": CMLocationData(4_021, True, False),
    "Capture 4 Pawns": CMLocationData(4_022, True, False),
    "Capture 5 Pawns": CMLocationData(4_023, True, False),
    "Capture 6 Pawns": CMLocationData(4_024, True, False),
    "Capture 7 Pawns": CMLocationData(4_025, True, False),
    "Capture 8 Pawns": CMLocationData(4_026, True, False),
    "Capture 2 Pieces": CMLocationData(4_030, True, False),
    "Capture 3 Pieces": CMLocationData(4_031, True, False),
    "Capture 4 Pieces": CMLocationData(4_032, True, False),
    "Capture 5 Pieces": CMLocationData(4_033, True, False),
    "Capture 6 Pieces": CMLocationData(4_034, True, False),
    "Capture 7 Pieces": CMLocationData(4_035, True, False),
    # special moves and tactics
    "00 Castle": CMLocationData(4_040, True, False),
    "000 Castle": CMLocationData(4_041, True, False),
    "Fork": CMLocationData(4_042, True, False),
    "Royal Fork": CMLocationData(4_043, True, True),
    "Pin": CMLocationData(4_044, True, False),
    "French Move": CMLocationData(4_045, True, False),
    # goal requires that you successively checkmate your opponent as they gain material
    "Checkmate Minima": CMLocationData(4_050, True, False),
    "Checkmate One Piece": CMLocationData(4_051, True, False),
    "Checkmate 2 Pieces": CMLocationData(4_052, True, False),
    "Checkmate 3 Pieces": CMLocationData(4_053, True, False),
    "Checkmate 4 Pieces": CMLocationData(4_054, True, False),
    "Checkmate 5 Pieces": CMLocationData(4_055, True, False),
    "Checkmate 6 Pieces": CMLocationData(4_056, True, False),
    "Checkmate 7 Pieces": CMLocationData(4_057, True, False),
    "Checkmate 8 Pieces": CMLocationData(4_058, True, False),
    "Checkmate 9 Pieces": CMLocationData(4_059, True, False),
    "Checkmate 10 Pieces": CMLocationData(4_060, True, False),
    "Checkmate 11 Pieces": CMLocationData(4_061, True, False),
    "Checkmate 12 Pieces": CMLocationData(4_062, True, False),
    "Checkmate 13 Pieces": CMLocationData(4_063, True, False),
    "Checkmate 14 Pieces": CMLocationData(4_064, True, False),
    "Checkmate Maxima": CMLocationData(4_065, True, False),

}

lookup_id_to_name: Dict[int, str] = {data.code: item_name for item_name, data in location_table.items() if data.code}
