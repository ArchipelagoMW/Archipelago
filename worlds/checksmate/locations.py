from dataclasses import dataclass
from enum import Enum, StrEnum

from BaseClasses import Location

from .geometry_progression import (
    BoardStage,
    MaterialCalibration,
    geometry_for_stage,
)


class CMLocation(Location):
    game: str = "ChecksMate"


class Tactic(Enum):
    Fork = 0
    Turns = 1


class TacticsMode(StrEnum):
    ALL = "all"
    TURNS = "turns"
    NONE = "none"


GEOMETRY_UNLOCKS_BY_STAGE = {
    stage: (
        geometry_for_stage(stage).unlocks.board_files,
        geometry_for_stage(stage).unlocks.board_ranks,
    )
    for stage in BoardStage
}

STAGE_IDS = {
    stage: geometry_for_stage(stage).stage_id
    for stage in BoardStage
}

_VICTORY_PROFILES_BY_STAGE = {
    stage: geometry_for_stage(stage).victory
    for stage in BoardStage
}
_VICTORY_LOCATION_CODES = frozenset(
    profile.location_code
    for profile in _VICTORY_PROFILES_BY_STAGE.values()
)
CHECKMATE_12_FILE_MATERIAL = 8_020  # Checkmate Maxima plus two outer attendants at about 1000 each.


@dataclass(frozen=True, slots=True)
class CMLocationData:
    code: int | None
    # suggested material required to perform task. generally an upper-end estimate. used to:
    # a. capture individual pieces
    # b. capture series of pieces and pawns within 1 game
    # c. fork/pin
    material_expectations: int | None
    # material in grand chess mode
    material_expectations_grand: int | None
    chessmen_expectations: int = 0
    is_tactic: Tactic | None = None
    required_stage: BoardStage = BoardStage.Board8x8
    use_grand_material_when_expanded: bool = False
    chessmen_expectations_grand: int | None = None
    required_stage_when_expanded: BoardStage | None = None
    compact_available: bool | None = None

    @property
    def material_calibration(self) -> MaterialCalibration:
        if (
            self.material_expectations is None
            and self.material_expectations_grand is None
        ):
            return MaterialCalibration.UNSUPPORTED
        return MaterialCalibration.CALIBRATED

    def material_requirement(
        self,
        expanded: bool,
        force_grand: bool = False,
    ) -> int | None:
        if not expanded:
            return self.material_expectations
        if self.material_expectations_grand is None:
            return self.material_expectations
        if (
            force_grand
            or self.use_grand_material_when_expanded
            or self.material_expectations is None
        ):
            return self.material_expectations_grand
        return min(
            self.material_expectations,
            self.material_expectations_grand,
        )

    def chessmen_requirement(self, expanded: bool) -> int:
        if expanded and self.chessmen_expectations_grand is not None:
            return self.chessmen_expectations_grand
        return self.chessmen_expectations

    def stage_requirement(self, expanded: bool) -> BoardStage:
        if expanded and self.required_stage_when_expanded is not None:
            return self.required_stage_when_expanded
        return self.required_stage


location_table = {
    # capture individual pieces and pawns
    # AI prefers not to use edge pawns early - thus they stay defended longer
    "Capture Pawn A": CMLocationData(4_902_000, 490, 1010),
    "Capture Pawn B": CMLocationData(4_902_001, 340, 810),
    # AI prefers to open queenside as developing queen has more tempo
    "Capture Pawn C": CMLocationData(4_902_002, 220, 660),
    "Capture Pawn D": CMLocationData(4_902_003, 100, 520),
    "Capture Pawn E": CMLocationData(4_902_004, 100, 320),
    "Capture Pawn F": CMLocationData(4_902_005, 320, 320),
    "Capture Pawn G": CMLocationData(4_902_006, 390, 620, compact_available=False),
    # AI prefers not to use edge pawns early - thus they stay defended longer
    "Capture Pawn H": CMLocationData(4_902_007, 490, 860, compact_available=False),
    "Capture Pawn I": CMLocationData(4_902_101, None, 810, required_stage=BoardStage.Board10x8),
    "Capture Pawn J": CMLocationData(4_902_102, None, 890, required_stage=BoardStage.Board10x8),
    "Capture Pawn K": CMLocationData(4_902_103, None, 970, required_stage=BoardStage.Board12x10),
    "Capture Pawn L": CMLocationData(4_902_104, None, 1050, required_stage=BoardStage.Board12x10),
    # bishops are less deployable than knights, and rooks are even more stuck back there
    "Capture Piece Queen's Rook": CMLocationData(4_902_008, 1500, 2850),
    "Capture Piece Queen's Knight": CMLocationData(4_902_010, 700, 1200),
    "Capture Piece Queen's Bishop": CMLocationData(4_902_012, 1040, 1200),
    "Capture Piece Queen": CMLocationData(4_902_014, 1300, 4100, compact_available=False),
    "Checkmate 6x8": CMLocationData(
        _VICTORY_PROFILES_BY_STAGE[BoardStage.Board6x8].location_code,
        None,
        None,
        required_stage=BoardStage.Board6x8,
    ),
    "Checkmate Minima": CMLocationData(
        _VICTORY_PROFILES_BY_STAGE[BoardStage.Board8x8].location_code,
        4020,
        4020,
        compact_available=False,
    ),
    "Checkmate Maxima": CMLocationData(
        _VICTORY_PROFILES_BY_STAGE[BoardStage.Board10x8].location_code,
        None,
        6020,
        required_stage=BoardStage.Board10x8,
    ),
    "Checkmate 10x10": CMLocationData(
        _VICTORY_PROFILES_BY_STAGE[BoardStage.Board10x10].location_code,
        None,
        6020,
        required_stage=BoardStage.Board10x10,
    ),
    "Checkmate 12x10": CMLocationData(
        _VICTORY_PROFILES_BY_STAGE[BoardStage.Board12x10].location_code,
        None,
        CHECKMATE_12_FILE_MATERIAL,
        required_stage=BoardStage.Board12x10,
    ),
    "Checkmate 12x12": CMLocationData(
        _VICTORY_PROFILES_BY_STAGE[BoardStage.Board12x12].location_code,
        None,
        CHECKMATE_12_FILE_MATERIAL,
        required_stage=BoardStage.Board12x12,
    ),
    # AI prefers not to open kingside as developing queen has more tempo
    "Capture Piece King's Bishop": CMLocationData(4_902_013, 1140, 1400),
    "Capture Piece King's Knight": CMLocationData(4_902_011, 1040, 1400),
    "Capture Piece King's Rook": CMLocationData(
        4_902_009, 1900, 3250, compact_available=False
    ),
    "Capture Piece Queen's Attendant": CMLocationData(
        4_902_109, None, 3950, required_stage=BoardStage.Board10x8
    ),
    "Capture Piece King's Attendant": CMLocationData(
        4_902_110, None, 4030, required_stage=BoardStage.Board10x8
    ),
    "Capture Piece Queen's Outer Attendant": CMLocationData(
        4_902_111, None, 4110, required_stage=BoardStage.Board12x10
    ),
    "Capture Piece King's Outer Attendant": CMLocationData(
        4_902_112, None, 4190, required_stage=BoardStage.Board12x10
    ),
    # some first locations
    # for strategic analysis see: https://en.wikipedia.org/wiki/Bongcloud_Attack
    "King to E2/E7 Early": CMLocationData(4_902_015, 0, 0),
    "King to Center": CMLocationData(4_902_016, 50, 50),
    "King to A File": CMLocationData(4_902_017, 0, 150),
    "King Captures Anything": CMLocationData(4_902_018, 150, 350),
    "King to Back Rank": CMLocationData(4_902_019, 2250, 5150),  # requires reaching a rather late-game state
    # capture series of pieces and pawns within 1 game
    "Capture 2 Pawns": CMLocationData(4_902_020, 750, 1650, 1),
    "Capture 3 Pawns": CMLocationData(4_902_021, 1450, 2450, 2),
    "Capture 4 Pawns": CMLocationData(4_902_022, 2240, 3240, 3),
    "Capture 5 Pawns": CMLocationData(4_902_023, 2620, 3620, 4),
    "Capture 6 Pawns": CMLocationData(4_902_024, 2975, 3975, 5),
    "Capture 7 Pawns": CMLocationData(4_902_025, 3255, 4255, 6, compact_available=False),
    "Capture 8 Pawns": CMLocationData(4_902_026, 3545, 4545, 7, compact_available=False),
    "Capture 9 Pawns": CMLocationData(
        4_902_120, None, 4645, 8, required_stage=BoardStage.Board10x8
    ),
    "Capture 10 Pawns": CMLocationData(
        4_902_121, None, 5245, 9, required_stage=BoardStage.Board10x8
    ),
    "Capture 11 Pawns": CMLocationData(
        4_902_124, None, 5845, 10, required_stage=BoardStage.Board12x10
    ),
    "Capture 12 Pawns": CMLocationData(
        4_902_125, None, 6445, 11, required_stage=BoardStage.Board12x10
    ),
    # Specific pieces should not be guaranteed to be accessible early, so we add +4 material (1piece+1pawn more)
    "Capture 2 Pieces": CMLocationData(4_902_027, 1450, 3000, 1),
    "Capture 3 Pieces": CMLocationData(4_902_028, 2100, 3400, 2),
    "Capture 4 Pieces": CMLocationData(4_902_029, 2770, 3750, 3),
    "Capture 5 Pieces": CMLocationData(4_902_030, 2950, 4150, 4),
    "Capture 6 Pieces": CMLocationData(4_902_031, 3300, 4500, 5, compact_available=False),
    "Capture 7 Pieces": CMLocationData(4_902_032, 3750, 4900, 6, compact_available=False),
    "Capture 8 Pieces": CMLocationData(
        4_902_122, None, 5200, 7, required_stage=BoardStage.Board10x8
    ),
    "Capture 9 Pieces": CMLocationData(
        4_902_123, None, 5400, 8, required_stage=BoardStage.Board10x8
    ),
    "Capture 10 Pieces": CMLocationData(
        4_902_126, None, 6100, 9, required_stage=BoardStage.Board12x10
    ),
    "Capture 11 Pieces": CMLocationData(
        4_902_127, None, 6800, 10, required_stage=BoardStage.Board12x10
    ),
    "Capture 2 Of Each": CMLocationData(4_902_033, 2250, 4150, 3),
    "Capture 3 Of Each": CMLocationData(4_902_034, 2650, 4550, 5),
    "Capture 4 Of Each": CMLocationData(4_902_035, 2950, 4900, 7),
    "Capture 5 Of Each": CMLocationData(4_902_036, 3200, 5200, 9),
    "Capture 6 Of Each": CMLocationData(4_902_037, 3500, 5450, 11, compact_available=False),
    "Capture 7 Of Each": CMLocationData(4_902_038, 3850, 5650, 13, compact_available=False),
    "Capture 8 Of Each": CMLocationData(
        4_902_130, None, 5850, 15, required_stage=BoardStage.Board10x8
    ),
    "Capture 9 Of Each": CMLocationData(
        4_902_131, None, 5950, 17, required_stage=BoardStage.Board10x8
    ),
    "Capture 10 Of Each": CMLocationData(
        4_902_132, None, 6900, 19, required_stage=BoardStage.Board12x10
    ),
    "Capture 11 Of Each": CMLocationData(
        4_902_133, None, 7850, 21, required_stage=BoardStage.Board12x10
    ),
    "Capture Everything": CMLocationData(
        4_902_039,
        4020,
        8050,
        14,
        use_grand_material_when_expanded=True,
        chessmen_expectations_grand=22,
        required_stage_when_expanded=BoardStage.Board12x10,
    ),
    "Capture Any 2": CMLocationData(4_902_070, 750, 1650, 1),
    "Capture Any 3": CMLocationData(4_902_071, 1450, 2450, 2),
    "Capture Any 4": CMLocationData(4_902_072, 2240, 3240, 3),
    "Capture Any 5": CMLocationData(4_902_073, 2500, 3500, 4),
    "Capture Any 6": CMLocationData(4_902_074, 2700, 3700, 5),
    "Capture Any 7": CMLocationData(4_902_075, 2850, 3850, 6),
    "Capture Any 8": CMLocationData(4_902_076, 3000, 4000, 7),
    "Capture Any 9": CMLocationData(4_902_077, 3150, 4150, 8),
    "Capture Any 10": CMLocationData(4_902_078, 3300, 4350, 9),
    "Capture Any 11": CMLocationData(4_902_079, 3450, 4650, 10, compact_available=False),
    "Capture Any 12": CMLocationData(4_902_080, 3600, 5000, 11, compact_available=False),
    "Capture Any 13": CMLocationData(4_902_081, 3750, 5350, 12, compact_available=False),
    "Capture Any 14": CMLocationData(4_902_082, 3900, 5600, 13, compact_available=False),
    "Capture Any 15": CMLocationData(
        4_902_083, None, 5750, 14, required_stage=BoardStage.Board10x8
    ),
    "Capture Any 16": CMLocationData(
        4_902_084, None, 5850, 15, required_stage=BoardStage.Board10x8
    ),
    "Capture Any 17": CMLocationData(
        4_902_085, None, 5950, 16, required_stage=BoardStage.Board10x8
    ),
    "Capture Any 18": CMLocationData(
        4_902_086, None, 6000, 17, required_stage=BoardStage.Board10x8
    ),
    "Capture Any 19": CMLocationData(
        4_902_087, None, 6400, 18, required_stage=BoardStage.Board12x10
    ),
    "Capture Any 20": CMLocationData(
        4_902_088, None, 6900, 19, required_stage=BoardStage.Board12x10
    ),
    "Capture Any 21": CMLocationData(
        4_902_089, None, 7450, 20, required_stage=BoardStage.Board12x10
    ),
    "Capture Any 22": CMLocationData(
        4_902_090, None, 8000, 21, required_stage=BoardStage.Board12x10
    ),
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
    "Fork, Sacrificial": CMLocationData(4_902_052, 700, 1100, 6, is_tactic=Tactic.Fork),
    "Fork, Sacrificial Triple": CMLocationData(4_902_053, 3300, 2700, 9, is_tactic=Tactic.Fork),
    # AI really hates getting royal forked
    "Fork, Sacrificial Royal": CMLocationData(4_902_054, 3600, 5200, 12, is_tactic=Tactic.Fork),
    "Fork, True": CMLocationData(4_902_055, 3150, 4550, 10, is_tactic=Tactic.Fork),
    "Fork, True Triple": CMLocationData(4_902_056, 3850, 5850, 12, is_tactic=Tactic.Fork),
    # I sincerely believe this should be filler
    "Fork, True Royal": CMLocationData(4_902_057, 4020, 6020, 14, is_tactic=Tactic.Fork),
    "O-O Castle": CMLocationData(4_902_058, 0, 0, 2),
    "O-O-O Castle": CMLocationData(4_902_059, 0, 0, 2),
    # "Discovered Attack": CMLocationData(4_902_060, 0),
    # "Pin": CMLocationData(4_902_061, 600),
    # "Skewer": CMLocationData(4_902_062, 600),
    # "Pawn Promotion": CMLocationData(4_902_063, 3000),
    # "Multiple Queens": CMLocationData(4_902_064, 3900),
    # Board-series transitions successively checkmate stronger formations.

}

lookup_id_to_name: dict[int, str] = {data.code: item_name for item_name, data in location_table.items() if data.code}

piece_names_small = ["Queen's Rook", "Queen's Knight", "Queen's Bishop", "Queen",
                     "King's Rook", "King's Knight", "King's Bishop"]
piece_names = ["Queen's Rook", "Queen's Knight", "Queen's Bishop", "Queen",
               "King's Rook", "King's Knight", "King's Bishop",
               "Queen's Attendant", "King's Attendant",
               "Queen's Outer Attendant", "King's Outer Attendant"]


def tactics_mode_for_options(options) -> TacticsMode:
    tactics = options.enable_tactics
    if tactics.value == tactics.option_none:
        return TacticsMode.NONE
    if tactics.value == tactics.option_turns:
        return TacticsMode.TURNS
    return TacticsMode.ALL


def location_available_at_stage(
    name: str,
    stage: BoardStage,
) -> bool:
    data = location_table[name]
    if stage == BoardStage.Board6x8:
        if data.compact_available is not None:
            return data.compact_available
        return data.required_stage <= BoardStage.Board8x8
    return data.required_stage <= stage


def location_names_for_stage(
    stage: BoardStage,
    tactics_mode: TacticsMode | str = TacticsMode.ALL,
    progression_start: BoardStage | None = None,
) -> tuple[str, ...]:
    try:
        mode = TacticsMode(tactics_mode)
    except ValueError as error:
        raise ValueError(f"Unknown tactics mode: {tactics_mode}") from error
    if progression_start is None:
        progression_start = (
            BoardStage.Board6x8
            if stage == BoardStage.Board6x8
            else BoardStage.Board8x8
        )

    return tuple(
        name for name, data in location_table.items()
        if location_available_at_stage(name, stage)
        and not (
            data.code in _VICTORY_LOCATION_CODES
            and data.required_stage < progression_start
        )
        and not (mode is TacticsMode.NONE and data.is_tactic is not None)
        and not (mode is TacticsMode.TURNS and data.is_tactic == Tactic.Fork)
    )


def geometry_unlocks_for_stage(stage: BoardStage) -> tuple[int, int]:
    metadata = geometry_for_stage(stage)
    return metadata.unlocks.board_files, metadata.unlocks.board_ranks


def stage_id(stage: BoardStage) -> str:
    return geometry_for_stage(stage).stage_id


def uses_expanded_profile(
    data: CMLocationData,
    endpoint: BoardStage,
) -> bool:
    if data.required_stage_when_expanded is not None:
        return endpoint >= data.required_stage_when_expanded
    return endpoint > BoardStage.Board8x8


def rule_stage_for_series(
    name: str,
    start: BoardStage,
    endpoint: BoardStage,
) -> BoardStage:
    data = location_table[name]
    expanded = uses_expanded_profile(data, endpoint)
    stage = data.stage_requirement(expanded)
    if (
        start == BoardStage.Board6x8
        and stage == BoardStage.Board8x8
        and location_available_at_stage(name, start)
    ):
        return start
    return max(stage, start)


def highest_chessmen_requirement_for_series(
    start: BoardStage,
    endpoint: BoardStage,
    tactics_mode: TacticsMode | str = TacticsMode.ALL,
) -> int:
    return max(
        location_table[name].chessmen_requirement(
            uses_expanded_profile(location_table[name], endpoint)
        )
        for name in location_names_for_stage(
            endpoint,
            tactics_mode,
            progression_start=start,
        )
    )


def chessmen_requirement_for_world(world) -> int:
    progression = world.geometry_progression
    return highest_chessmen_requirement_for_series(
        progression.stages[0].stage,
        progression.endpoint.stage,
        tactics_mode_for_options(world.options),
    )


highest_chessmen_requirement_small = max(
    data.chessmen_requirement(False)
    for data in location_table.values()
    if data.material_expectations is not None
)
highest_chessmen_requirement = max(
    data.chessmen_requirement(True) for data in location_table.values()
)
