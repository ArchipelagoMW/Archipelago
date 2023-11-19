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
    "Capture Pawn A": CMLocationData(4_902_000, True, False),
    "Capture Pawn B": CMLocationData(4_902_001, True, False),
    "Capture Pawn C": CMLocationData(4_902_002, True, False),
    "Capture Pawn D": CMLocationData(4_902_003, True, False),
    "Capture Pawn E": CMLocationData(4_902_004, True, False),
    "Capture Pawn F": CMLocationData(4_902_005, True, False),
    "Capture Pawn G": CMLocationData(4_902_006, True, False),
    "Capture Pawn H": CMLocationData(4_902_007, True, False),
    "Capture Piece A": CMLocationData(4_902_008, True, False),
    "Capture Piece B": CMLocationData(4_902_010, True, False),
    "Capture Piece C": CMLocationData(4_902_012, True, False),
    "Capture Piece D": CMLocationData(4_902_014, True, False),
    "Capture Piece F": CMLocationData(4_902_013, True, False),
    "Capture Piece G": CMLocationData(4_902_011, True, False),
    "Capture Piece H": CMLocationData(4_902_009, True, False),
    # some first locations
    # for strategic analysis see: https://en.wikipedia.org/wiki/Bongcloud_Attack
    "Bongcloud Once": CMLocationData(4_902_015, True, False),
    "Bongcloud Center": CMLocationData(4_902_016, True, False),
    "Bongcloud A File": CMLocationData(4_902_017, True, False),
    "Bongcloud Capture": CMLocationData(4_902_018, True, False),
    "Bongcloud Promotion": CMLocationData(4_902_019, True, False),
    # capture series of pieces and pawns within 1 game
    "Capture 2 Pawns": CMLocationData(4_902_020, True, False),
    "Capture 3 Pawns": CMLocationData(4_902_021, True, False),
    "Capture 4 Pawns": CMLocationData(4_902_022, True, False),
    "Capture 5 Pawns": CMLocationData(4_902_023, True, False),
    "Capture 6 Pawns": CMLocationData(4_902_024, True, False),
    "Capture 7 Pawns": CMLocationData(4_902_025, True, False),
    "Capture 8 Pawns": CMLocationData(4_902_026, True, False),
    "Capture 2 Pieces": CMLocationData(4_902_027, True, False),
    "Capture 3 Pieces": CMLocationData(4_902_028, True, False),
    "Capture 4 Pieces": CMLocationData(4_902_029, True, False),
    "Capture 5 Pieces": CMLocationData(4_902_030, True, False),
    "Capture 6 Pieces": CMLocationData(4_902_031, True, False),
    "Capture 7 Pieces": CMLocationData(4_902_032, True, False),
    "Capture 2 Of Each": CMLocationData(4_902_033, True, False),
    "Capture 3 Of Each": CMLocationData(4_902_034, True, False),
    "Capture 4 Of Each": CMLocationData(4_902_035, True, False),
    "Capture 5 Of Each": CMLocationData(4_902_036, True, False),
    "Capture 6 Of Each": CMLocationData(4_902_037, True, False),
    "Capture 7 Of Each": CMLocationData(4_902_038, True, False),
    "Capture Everything": CMLocationData(4_902_039, True, False),
    "Threaten Pawn": CMLocationData(4_902_040, True, False),
    "Threaten Minor": CMLocationData(4_902_041, True, False),
    "Threaten Major": CMLocationData(4_902_042, True, False),
    "Threaten Queen": CMLocationData(4_902_043, True, False),
    "Threaten King": CMLocationData(4_902_044, True, False),
    # special moves and tactics
    # TODO: Getting a french move on the AI seems nigh impossible - maybe I can tweak the evaluation or something
    # "French Move": CMLocationData(4_902_050, True, False),
    # "Discovered Attack": CMLocationData(4_902_051, True, False),
    "Fork, Sacrificial": CMLocationData(4_902_052, True, False),
    "Fork, Sacrificial Triple": CMLocationData(4_902_053, True, False),
    "Fork, Sacrificial Royal": CMLocationData(4_902_054, True, True),
    "Fork, True": CMLocationData(4_902_055, True, False),
    "Fork, True Triple": CMLocationData(4_902_056, True, False),
    "Fork, True Royal": CMLocationData(4_902_057, True, True),
    # TODO: prevent castle from holding enemy pieces (progression item) in case of "Oops all queens."
    "O-O Castle": CMLocationData(4_902_058, True, False),
    "O-O-O Castle": CMLocationData(4_902_059, True, False),
    # "Discovered Attack": CMLocationData(4_902_060, True, False),
    # "Pin": CMLocationData(4_902_061, True, False),
    # "Skewer": CMLocationData(4_902_062, True, False),
    # goal 1+ requires that you successively checkmate your opponent as they gain material
    # "Checkmate Minima": CMLocationData(4_902_084, True, False),
    # "Checkmate One Piece": CMLocationData(4_902_085, True, False),
    # "Checkmate 2 Pieces": CMLocationData(4_902_086, True, False),
    # "Checkmate 3 Pieces": CMLocationData(4_902_087, True, False),
    # "Checkmate 4 Pieces": CMLocationData(4_902_088, True, False),
    # "Checkmate 5 Pieces": CMLocationData(4_902_089, True, False),
    # "Checkmate 6 Pieces": CMLocationData(4_902_090, True, False),
    # "Checkmate 7 Pieces": CMLocationData(4_902_091, True, False),
    # "Checkmate 8 Pieces": CMLocationData(4_902_092, True, False),
    # "Checkmate 9 Pieces": CMLocationData(4_902_093, True, False),
    # "Checkmate 10 Pieces": CMLocationData(4_902_094, True, False),
    # "Checkmate 11 Pieces": CMLocationData(4_902_095, True, False),
    # "Checkmate 12 Pieces": CMLocationData(4_902_096, True, False),
    # "Checkmate 13 Pieces": CMLocationData(4_902_097, True, False),
    # "Checkmate 14 Pieces": CMLocationData(4_902_098, True, False),
    "Checkmate Maxima": CMLocationData(4_902_099, True, False),

}

lookup_id_to_name: Dict[int, str] = {data.code: item_name for item_name, data in location_table.items() if data.code}
