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
    # material in grand chess mode
    material_expectations_grand: int
    chessmen_expectations: int = 0
    is_tactic: bool = False


location_table = {
    # capture individual pieces and pawns
    # AI prefers not to use edge pawns early - thus they stay defended longer
    "Capture Pawn A": CMLocationData(4_902_000, 190, 310),
    "Capture Pawn B": CMLocationData(4_902_001, 140, 210),
    "Capture Pawn C": CMLocationData(4_902_002, 100, 160),
    "Capture Pawn D": CMLocationData(4_902_003, 100, 120),
    "Capture Pawn E": CMLocationData(4_902_004, 100, 120),
    # AI prefers not to open kingside as developing queen has more tempo
    "Capture Pawn F": CMLocationData(4_902_005, 140, 120),
    "Capture Pawn G": CMLocationData(4_902_006, 240, 120),
    # AI prefers not to use edge pawns early - thus they stay defended longer
    "Capture Pawn H": CMLocationData(4_902_007, 290, 160),
    "Capture Pawn I": CMLocationData(4_902_101, -1, 310),
    "Capture Pawn J": CMLocationData(4_902_102, -1, 390),
    "Capture Queen's Rook": CMLocationData(4_902_008, 900, 1650),
    "Capture Queen's Knight": CMLocationData(4_902_010, 700, 1200),
    "Capture Queen's Bishop": CMLocationData(4_902_012, 700, 1200),
    "Capture Queen": CMLocationData(4_902_014, 1300, 1900),
    "Checkmate Minima": CMLocationData(4_902_098, 4020, 4020),  # (this is the game's goal / completion condition)
    "Checkmate Maxima": CMLocationData(4_902_099, -1, 6020),  # (this is the game's goal / completion condition)
    # AI prefers not to open kingside as developing queen has more tempo
    "Capture King's Bishop": CMLocationData(4_902_013, 1040, 1400),
    "Capture King's Knight": CMLocationData(4_902_011, 1040, 1400),
    "Capture King's Rook": CMLocationData(4_902_009, 1240, 2050),
    "Capture Queen's Attendant": CMLocationData(4_902_109, -1, 1950),
    "Capture King's Attendant": CMLocationData(4_902_110, -1, 2030),
    # some first locations
    # for strategic analysis see: https://en.wikipedia.org/wiki/Bongcloud_Attack
    "King to E2/E7 Early": CMLocationData(4_902_015, 0, 0),
    "King to Center": CMLocationData(4_902_016, 50, 50),
    "King to A File": CMLocationData(4_902_017, 0, 0),
    "King Captures Anything": CMLocationData(4_902_018, 150, 150),
    "King to Back Rank": CMLocationData(4_902_019, 1950, 3150),  # requires reaching a rather late-game state
    # capture series of pieces and pawns within 1 game
    "Capture 2 Pawns": CMLocationData(4_902_020, 550, 550, 1),
    "Capture 3 Pawns": CMLocationData(4_902_021, 950, 950, 2),
    "Capture 4 Pawns": CMLocationData(4_902_022, 1440, 1440, 3),
    "Capture 5 Pawns": CMLocationData(4_902_023, 1920, 1920, 4),
    "Capture 6 Pawns": CMLocationData(4_902_024, 2375, 2375, 5),
    "Capture 7 Pawns": CMLocationData(4_902_025, 2855, 2855, 6),
    "Capture 8 Pawns": CMLocationData(4_902_026, 3345, 3345, 7),
    "Capture 9 Pawns": CMLocationData(4_902_120, -1, 3745, 8),
    "Capture 10 Pawns": CMLocationData(4_902_121, -1, 4145, 9),
    # Specific pieces should not be guaranteed to be accessible early, so we add +4 material (1piece+1pawn more)
    "Capture 2 Pieces": CMLocationData(4_902_027, 1300, 1300, 1),
    "Capture 3 Pieces": CMLocationData(4_902_028, 1900, 1900, 2),
    "Capture 4 Pieces": CMLocationData(4_902_029, 2150, 2150, 3),
    "Capture 5 Pieces": CMLocationData(4_902_030, 2550, 2550, 4),
    "Capture 6 Pieces": CMLocationData(4_902_031, 2900, 2900, 5),
    "Capture 7 Pieces": CMLocationData(4_902_032, 3600, 3600, 6),
    "Capture 8 Pieces": CMLocationData(4_902_032, -1, 3600, 7),
    "Capture 9 Pieces": CMLocationData(4_902_032, -1, 3600, 8),
    "Capture 2 Of Each": CMLocationData(4_902_033, 1600, 1600, 3),
    "Capture 3 Of Each": CMLocationData(4_902_034, 2150, 2150, 5),
    "Capture 4 Of Each": CMLocationData(4_902_035, 2550, 2550, 7),
    "Capture 5 Of Each": CMLocationData(4_902_036, 3000, 3000, 9),
    "Capture 6 Of Each": CMLocationData(4_902_037, 3500, 3500, 11),
    "Capture 7 Of Each": CMLocationData(4_902_038, 3850, 3850, 13),
    "Capture 8 Of Each": CMLocationData(4_902_130, -1, 3850, 15),
    "Capture 9 Of Each": CMLocationData(4_902_131, -1, 3850, 17),
    "Capture Everything": CMLocationData(4_902_039, -1, 6050, 14),
    "Capture Any 2": CMLocationData(4_902_070, 600, 750, 1),
    "Capture Any 3": CMLocationData(4_902_071, 1050, 1350, 2),
    "Capture Any 4": CMLocationData(4_902_072, 1450, 2050, 3),
    "Capture Any 5": CMLocationData(4_902_073, 1850, 2750, 4),
    "Capture Any 6": CMLocationData(4_902_074, 2100, 3100, 5),
    "Capture Any 7": CMLocationData(4_902_075, 2450, 3450, 6),
    "Capture Any 8": CMLocationData(4_902_076, 2700, 3700, 7),
    "Capture Any 9": CMLocationData(4_902_077, 3050, 4050, 8),
    "Capture Any 10": CMLocationData(4_902_078, 3400, 4400, 9),
    "Capture Any 11": CMLocationData(4_902_079, 3650, 4650, 10),
    "Capture Any 12": CMLocationData(4_902_080, 3850, 4750, 11),
    "Capture Any 13": CMLocationData(4_902_081, 3950, 5050, 12),
    "Capture Any 14": CMLocationData(4_902_082, 4000, 5400, 13),
    "Capture Any 15": CMLocationData(4_902_082, -1, 5650, 14),
    "Capture Any 16": CMLocationData(4_902_083, -1, 5750, 15),
    "Capture Any 17": CMLocationData(4_902_084, -1, 5850, 16),
    "Capture Any 18": CMLocationData(4_902_085, -1, 5900, 17),
    # some easier interaction moves
    "Threaten Pawn": CMLocationData(4_902_040, 0, 0),
    "Threaten Minor": CMLocationData(4_902_041, 200, 400),
    "Threaten Major": CMLocationData(4_902_042, 300, 500),
    "Threaten Queen": CMLocationData(4_902_043, 300, 500),
    "Threaten King": CMLocationData(4_902_044, 1000, 1800),
    # special moves and tactics
    # TODO: Getting a french move on the AI occurs seldom - maybe I can tweak the evaluation or something?
    # "French Move": CMLocationData(4_902_050, 0),
    "Fork, Sacrificial": CMLocationData(4_902_052, 700, 700, 6, is_tactic=True),
    "Fork, Sacrificial Triple": CMLocationData(4_902_053, 1700, 2700, 9, is_tactic=True),
    # AI really hates getting royal forked
    "Fork, Sacrificial Royal": CMLocationData(4_902_054, 3200, 5200, 12, is_tactic=True),
    "Fork, True": CMLocationData(4_902_055, 2550, 4550, 10, is_tactic=True),
    "Fork, True Triple": CMLocationData(4_902_056, 3450, 5450, 12, is_tactic=True),
    # I sincerely believe this should be filler
    "Fork, True Royal": CMLocationData(4_902_057, 4020, 6020, 14, is_tactic=True),
    # TODO: prevent castle from holding enemy pieces (progression item) in case of "Oops all queens."
    "O-O Castle": CMLocationData(4_902_058, 0, 0, 2),
    "O-O-O Castle": CMLocationData(4_902_059, 0, 0, 2),
    # "Discovered Attack": CMLocationData(4_902_060, 0),
    # "Pin": CMLocationData(4_902_061, 600),
    # "Skewer": CMLocationData(4_902_062, 600),
    # "Pawn Promotion": CMLocationData(4_902_063, 3000),
    # "Multiple Queens": CMLocationData(4_902_064, 3900),
    # goal 1+ requires that you successively checkmate your opponent as they gain material

}

lookup_id_to_name: Dict[int, str] = {data.code: item_name for item_name, data in location_table.items() if data.code}

piece_names = ["Queen's Rook", "Queen's Knight", "Queen's Bishop", "Queen",
               "King's Rook", "King's Knight", "King's Bishop",
               "Queen's Attendant", "King's Attendant"]


# unused because we can never run out of pawn locations
highest_chessmen_requirement_small = max([
    location_table[location].chessmen_expectations for location in location_table if
    location_table[location].material_expectations != -1])
highest_chessmen_requirement = max([
    location_table[location].chessmen_expectations for location in location_table])
