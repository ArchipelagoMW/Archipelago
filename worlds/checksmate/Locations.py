from typing import Dict, NamedTuple, Optional

from BaseClasses import Location


class CMLocation(Location):
    game: str = "ChecksMate"


class CMLocationData(NamedTuple):
    code: Optional[int]
    # suggested material required to perform task. generally an upper-end estimate. used to:
    # a. capture individual pieces
    # b. capture series of pieces and pawns within 1 game
    # c. fork/pin
    material_expectations: int
    chessmen_expectations: int = 0


location_table = {
    # capture individual pieces and pawns
    # AI prefers not to use edge pawns early - thus they stay defended longer
    "Capture Pawn A": CMLocationData(4_902_000, 190),
    "Capture Pawn B": CMLocationData(4_902_001, 140),
    "Capture Pawn C": CMLocationData(4_902_002, 100),
    "Capture Pawn D": CMLocationData(4_902_003, 100),
    "Capture Pawn E": CMLocationData(4_902_004, 100),
    # AI prefers not to open kingside as developing queen has more tempo
    "Capture Pawn F": CMLocationData(4_902_005, 140),
    "Capture Pawn G": CMLocationData(4_902_006, 240),
    # AI prefers not to use edge pawns early - thus they stay defended longer
    "Capture Pawn H": CMLocationData(4_902_007, 290),
    "Capture Piece A": CMLocationData(4_902_008, 900),  # rook
    "Capture Piece B": CMLocationData(4_902_010, 700),  # knight
    "Capture Piece C": CMLocationData(4_902_012, 700),  # bishop
    "Capture Piece D": CMLocationData(4_902_014, 1300),  # queen
    "Checkmate Maxima": CMLocationData(4_902_099, 4020),  # king (this is the game's goal / completion condition)
    # AI prefers not to open kingside as developing queen has more tempo
    "Capture Piece F": CMLocationData(4_902_013, 1040),  # bishop
    "Capture Piece G": CMLocationData(4_902_011, 1040),  # knight
    "Capture Piece H": CMLocationData(4_902_009, 1240),  # rook
    # some first locations
    # for strategic analysis see: https://en.wikipedia.org/wiki/Bongcloud_Attack
    "King to E2/E7 Early": CMLocationData(4_902_015, 0),
    "King to Center": CMLocationData(4_902_016, 50),
    "King to A File": CMLocationData(4_902_017, 0),
    "King Captures Anything": CMLocationData(4_902_018, 150),
    "King to Back Rank": CMLocationData(4_902_019, 1950),  # requires reaching a rather late-game state
    # capture series of pieces and pawns within 1 game
    "Capture 2 Pawns": CMLocationData(4_902_020, 550, 1),
    "Capture 3 Pawns": CMLocationData(4_902_021, 950, 2),
    "Capture 4 Pawns": CMLocationData(4_902_022, 1440, 3),
    "Capture 5 Pawns": CMLocationData(4_902_023, 1920, 4),
    "Capture 6 Pawns": CMLocationData(4_902_024, 2375, 5),
    "Capture 7 Pawns": CMLocationData(4_902_025, 2855, 6),
    "Capture 8 Pawns": CMLocationData(4_902_026, 3345, 7),
    # Specific pieces should not be guaranteed to be accessible early, so we add +4 material (1piece+1pawn more)
    "Capture 2 Pieces": CMLocationData(4_902_027, 1300, 1),
    "Capture 3 Pieces": CMLocationData(4_902_028, 1900, 2),
    "Capture 4 Pieces": CMLocationData(4_902_029, 2150, 3),
    "Capture 5 Pieces": CMLocationData(4_902_030, 2550, 4),
    "Capture 6 Pieces": CMLocationData(4_902_031, 2900, 5),
    "Capture 7 Pieces": CMLocationData(4_902_032, 3600, 6),
    "Capture 2 Of Each": CMLocationData(4_902_033, 1600, 3),
    "Capture 3 Of Each": CMLocationData(4_902_034, 2150, 5),
    "Capture 4 Of Each": CMLocationData(4_902_035, 2550, 7),
    "Capture 5 Of Each": CMLocationData(4_902_036, 3000, 9),
    "Capture 6 Of Each": CMLocationData(4_902_037, 3500, 11),
    "Capture 7 Of Each": CMLocationData(4_902_038, 3850, 13),
    "Capture Everything": CMLocationData(4_902_039, 4020, 14),
    "Threaten Pawn": CMLocationData(4_902_040, 0),
    "Threaten Minor": CMLocationData(4_902_041, 200),
    "Threaten Major": CMLocationData(4_902_042, 200),
    "Threaten Queen": CMLocationData(4_902_043, 300),
    "Threaten King": CMLocationData(4_902_044, 1000),
    # special moves and tactics
    # TODO: Getting a french move on the AI occurs seldom - maybe I can tweak the evaluation or something?
    # "French Move": CMLocationData(4_902_050, 0),
    "Fork, Sacrificial": CMLocationData(4_902_052, 700),
    "Fork, Sacrificial Triple": CMLocationData(4_902_053, 1700),
    "Fork, Sacrificial Royal": CMLocationData(4_902_054, 3200),  # AI really hates getting royal forked
    "Fork, True": CMLocationData(4_902_055, 2550),
    "Fork, True Triple": CMLocationData(4_902_056, 3450),
    "Fork, True Royal": CMLocationData(4_902_057, 4020),  # I sincerely believe this should be filler
    # TODO: prevent castle from holding enemy pieces (progression item) in case of "Oops all queens."
    "O-O Castle": CMLocationData(4_902_058, 0),
    "O-O-O Castle": CMLocationData(4_902_059, 0),
    # "Discovered Attack": CMLocationData(4_902_060, 0),
    # "Pin": CMLocationData(4_902_061, 600),
    # "Skewer": CMLocationData(4_902_062, 600),
    # "Pawn Promotion": CMLocationData(4_902_063, 3000),
    # "Multiple Queens": CMLocationData(4_902_064, 3900),
    # goal 1+ requires that you successively checkmate your opponent as they gain material
    # "Checkmate Minima": CMLocationData(4_902_084, 0),
    # "Checkmate One Piece": CMLocationData(4_902_085, 0),
    # "Checkmate 2 Pieces": CMLocationData(4_902_086, 0),
    # "Checkmate 3 Pieces": CMLocationData(4_902_087, 0),
    # "Checkmate 4 Pieces": CMLocationData(4_902_088, 0),
    # "Checkmate 5 Pieces": CMLocationData(4_902_089, 0),
    # "Checkmate 6 Pieces": CMLocationData(4_902_090, 0),
    # "Checkmate 7 Pieces": CMLocationData(4_902_091, 0),
    # "Checkmate 8 Pieces": CMLocationData(4_902_092, 0),
    # "Checkmate 9 Pieces": CMLocationData(4_902_093, 0),
    # "Checkmate 10 Pieces": CMLocationData(4_902_094, 0),
    # "Checkmate 11 Pieces": CMLocationData(4_902_095, 0),
    # "Checkmate 12 Pieces": CMLocationData(4_902_096, 0),
    # "Checkmate 13 Pieces": CMLocationData(4_902_097, 0),
    # "Checkmate 14 Pieces": CMLocationData(4_902_098, 0),

}

lookup_id_to_name: Dict[int, str] = {data.code: item_name for item_name, data in location_table.items() if data.code}

# unused because we can never run out of pawn locations
highest_chessmen_requirement = max([location_table[location].chessmen_expectations for location in location_table])
