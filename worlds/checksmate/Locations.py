from enum import Enum
from typing import Dict, NamedTuple, Optional

from BaseClasses import Location


class CMLocation(Location):
    game: str = "ChecksMate"


class Tactic(Enum):
    Fork = 0
    Turns = 1


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
    is_tactic: Tactic = None


location_table = {
    # capture individual pieces and pawns
    # AI prefers not to use edge pawns early - thus they stay defended longer
    "Capture Pawn A": CMLocationData(4_902_000, 490, 810),
    "Capture Pawn B": CMLocationData(4_902_001, 340, 610),
    # AI prefers to open queenside as developing queen has more tempo
    "Capture Pawn C": CMLocationData(4_902_002, 220, 460),
    "Capture Pawn D": CMLocationData(4_902_003, 100, 320),
    "Capture Pawn E": CMLocationData(4_902_004, 100, 120),
    "Capture Pawn F": CMLocationData(4_902_005, 340, 120),
    "Capture Pawn G": CMLocationData(4_902_006, 390, 420),
    # AI prefers not to use edge pawns early - thus they stay defended longer
    "Capture Pawn H": CMLocationData(4_902_007, 490, 660),
    "Capture Pawn I": CMLocationData(4_902_101, -1, 810),
    "Capture Pawn J": CMLocationData(4_902_102, -1, 890),
    # bishops are less deployable than knights, and rooks are even more stuck back there
    "Capture Piece Queen's Rook": CMLocationData(4_902_008, 900, 1650),
    "Capture Piece Queen's Knight": CMLocationData(4_902_010, 700, 1200),
    "Capture Piece Queen's Bishop": CMLocationData(4_902_012, 1040, 1200),
    "Capture Piece Queen": CMLocationData(4_902_014, 1300, 1900),
    "Checkmate Minima": CMLocationData(4_902_098, 4020, 4020),  # (this is the game's goal / completion condition)
    "Checkmate Maxima": CMLocationData(4_902_099, -1, 6020),  # (this is the game's goal / completion condition)
    # AI prefers not to open kingside as developing queen has more tempo
    "Capture Piece King's Bishop": CMLocationData(4_902_013, 1140, 1400),
    "Capture Piece King's Knight": CMLocationData(4_902_011, 1040, 1400),
    "Capture Piece King's Rook": CMLocationData(4_902_009, 1240, 2050),
    "Capture Piece Queen's Attendant": CMLocationData(4_902_109, -1, 1950),
    "Capture Piece King's Attendant": CMLocationData(4_902_110, -1, 2030),
    # some first locations
    # for strategic analysis see: https://en.wikipedia.org/wiki/Bongcloud_Attack
    "King to E2/E7 Early": CMLocationData(4_902_015, 0, 0),
    "King to Center": CMLocationData(4_902_016, 50, 50),
    "King to A File": CMLocationData(4_902_017, 0, 50),
    "King Captures Anything": CMLocationData(4_902_018, 150, 350),
    "King to Back Rank": CMLocationData(4_902_019, 2250, 5150),  # requires reaching a rather late-game state
    # capture series of pieces and pawns within 1 game
    "Capture 2 Pawns": CMLocationData(4_902_020, 750, 1150, 1),
    "Capture 3 Pawns": CMLocationData(4_902_021, 1450, 1950, 2),
    "Capture 4 Pawns": CMLocationData(4_902_022, 2040, 2440, 3),
    "Capture 5 Pawns": CMLocationData(4_902_023, 2320, 2720, 4),
    "Capture 6 Pawns": CMLocationData(4_902_024, 2575, 2975, 5),
    "Capture 7 Pawns": CMLocationData(4_902_025, 2955, 3555, 6),
    "Capture 8 Pawns": CMLocationData(4_902_026, 3445, 4145, 7),
    "Capture 9 Pawns": CMLocationData(4_902_120, -1, 4645, 8),
    "Capture 10 Pawns": CMLocationData(4_902_121, -1, 5245, 9),
    # Specific pieces should not be guaranteed to be accessible early, so we add +4 material (1piece+1pawn more)
    "Capture 2 Pieces": CMLocationData(4_902_027, 1400, 3000, 1),
    "Capture 3 Pieces": CMLocationData(4_902_028, 1900, 3400, 2),
    "Capture 4 Pieces": CMLocationData(4_902_029, 2470, 3750, 3),
    "Capture 5 Pieces": CMLocationData(4_902_030, 2750, 4150, 4),
    "Capture 6 Pieces": CMLocationData(4_902_031, 3100, 4500, 5),
    "Capture 7 Pieces": CMLocationData(4_902_032, 3650, 4900, 6),
    "Capture 8 Pieces": CMLocationData(4_902_122, -1, 5200, 7),
    "Capture 9 Pieces": CMLocationData(4_902_123, -1, 5400, 8),
    "Capture 2 Of Each": CMLocationData(4_902_033, 1900, 3750, 3),
    "Capture 3 Of Each": CMLocationData(4_902_034, 2350, 4250, 5),
    "Capture 4 Of Each": CMLocationData(4_902_035, 2750, 4650, 7),
    "Capture 5 Of Each": CMLocationData(4_902_036, 3100, 5000, 9),
    "Capture 6 Of Each": CMLocationData(4_902_037, 3500, 5400, 11),
    "Capture 7 Of Each": CMLocationData(4_902_038, 3850, 5650, 13),
    "Capture 8 Of Each": CMLocationData(4_902_130, -1, 5850, 15),
    "Capture 9 Of Each": CMLocationData(4_902_131, -1, 5950, 17),
    "Capture Everything": CMLocationData(4_902_039, 4020, 6050, -1),
    "Capture Any 2": CMLocationData(4_902_070, 750, 850, 1),
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
    "Capture Any 15": CMLocationData(4_902_083, -1, 5650, 14),
    "Capture Any 16": CMLocationData(4_902_084, -1, 5750, 15),
    "Capture Any 17": CMLocationData(4_902_085, -1, 5850, 16),
    "Capture Any 18": CMLocationData(4_902_086, -1, 5900, 17),
    "Current Objective: Survive 3 Turns": CMLocationData(4_902_140, 0, 0, 0, is_tactic=Tactic.Turns),
    "Current Objective: Survive 5 Turns": CMLocationData(4_902_141, 200, 330, 2, is_tactic=Tactic.Turns),
    "Current Objective: Survive 10 Turns": CMLocationData(4_902_142, 2500, 4500, 9, is_tactic=Tactic.Turns),
    "Current Objective: Survive 20 Turns": CMLocationData(4_902_143, 3800, 5800, 15, is_tactic=Tactic.Turns),
    # some easier interaction moves
    "Threaten Pawn": CMLocationData(4_902_040, 0, 0),
    "Threaten Minor": CMLocationData(4_902_041, 200, 400),
    "Threaten Major": CMLocationData(4_902_042, 300, 500),
    "Threaten Queen": CMLocationData(4_902_043, 300, 500),
    "Threaten King": CMLocationData(4_902_044, 1000, 1800),
    # special moves and tactics
    # TODO: Getting a french move on the AI occurs seldom - maybe I can tweak the evaluation or something?
    # "French Move": CMLocationData(4_902_050, 0),
    "Fork, Sacrificial": CMLocationData(4_902_052, 700, 1100, 6, is_tactic=Tactic.Fork),
    "Fork, Sacrificial Triple": CMLocationData(4_902_053, 1700, 2700, 9, is_tactic=Tactic.Fork),
    # AI really hates getting royal forked
    "Fork, Sacrificial Royal": CMLocationData(4_902_054, 3200, 5200, 12, is_tactic=Tactic.Fork),
    "Fork, True": CMLocationData(4_902_055, 2550, 4550, 10, is_tactic=Tactic.Fork),
    "Fork, True Triple": CMLocationData(4_902_056, 3450, 5450, 12, is_tactic=Tactic.Fork),
    # I sincerely believe this should be filler
    "Fork, True Royal": CMLocationData(4_902_057, 4020, 6020, 14, is_tactic=Tactic.Fork),
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

piece_names_small = ["Queen's Rook", "Queen's Knight", "Queen's Bishop", "Queen",
                     "King's Rook", "King's Knight", "King's Bishop"]
piece_names = ["Queen's Rook", "Queen's Knight", "Queen's Bishop", "Queen",
               "King's Rook", "King's Knight", "King's Bishop",
               "Queen's Attendant", "King's Attendant"]


# unused because we can never run out of pawn locations
highest_chessmen_requirement_small = max([
    location_table[location].chessmen_expectations for location in location_table if
    location_table[location].material_expectations != -1])
highest_chessmen_requirement = max([
    location_table[location].chessmen_expectations for location in location_table])
