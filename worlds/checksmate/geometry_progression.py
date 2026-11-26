from collections.abc import Iterable
from dataclasses import dataclass
from enum import IntEnum, StrEnum


class BoardStage(IntEnum):
    Board6x8 = -1
    Board8x8 = 0
    Board10x8 = 1
    Board10x10 = 2
    Board12x10 = 3
    Board12x12 = 4


class MaterialCalibration(StrEnum):
    CALIBRATED = "calibrated"
    UNSUPPORTED = "unsupported"


@dataclass(frozen=True, slots=True)
class GeometryUnlocks:
    board_files: int
    board_ranks: int


@dataclass(frozen=True, slots=True)
class VictoryProfile:
    location_name: str
    location_code: int
    material_calibration: MaterialCalibration


@dataclass(frozen=True, slots=True)
class GeometryMetadata:
    stage: BoardStage
    stage_id: str
    files: int
    ranks: int
    unlocks: GeometryUnlocks
    cpu_pawn_count: int
    cpu_non_king_count: int
    victory: VictoryProfile
    selectable: bool


@dataclass(frozen=True, slots=True)
class GeometryProgression:
    stages: tuple[GeometryMetadata, ...]
    precollected_unlocks: GeometryUnlocks
    generated_unlocks: GeometryUnlocks
    endpoint: GeometryMetadata
    victory: VictoryProfile
    transitions: tuple["GeometryTransition", ...]

    @property
    def initial_unlocks(self) -> GeometryUnlocks:
        return self.precollected_unlocks


@dataclass(frozen=True, slots=True)
class GeometryTransition:
    source: GeometryMetadata
    destination: GeometryMetadata
    unlock_delta: GeometryUnlocks


_SELECTABLE_STAGE_ORDER = (
    BoardStage.Board6x8,
    BoardStage.Board8x8,
    BoardStage.Board10x8,
    BoardStage.Board10x10,
    BoardStage.Board12x10,
)

_LEGACY_STAGE_ORDER = _SELECTABLE_STAGE_ORDER[1:] + (
    BoardStage.Board12x12,
)

_SELECTABLE_START_STAGES = frozenset(_SELECTABLE_STAGE_ORDER[:3])


_GEOMETRY_BY_STAGE = {
    BoardStage.Board6x8: GeometryMetadata(
        BoardStage.Board6x8,
        "6x8",
        6,
        8,
        GeometryUnlocks(0, 0),
        6,
        5,
        VictoryProfile(
            "Checkmate 6x8",
            4_902_100,
            MaterialCalibration.UNSUPPORTED,
        ),
        True,
    ),
    BoardStage.Board8x8: GeometryMetadata(
        BoardStage.Board8x8,
        "8x8",
        8,
        8,
        GeometryUnlocks(1, 0),
        8,
        7,
        VictoryProfile(
            "Checkmate Minima",
            4_902_098,
            MaterialCalibration.CALIBRATED,
        ),
        True,
    ),
    BoardStage.Board10x8: GeometryMetadata(
        BoardStage.Board10x8,
        "10x8",
        10,
        8,
        GeometryUnlocks(2, 0),
        10,
        9,
        VictoryProfile(
            "Checkmate Maxima",
            4_902_099,
            MaterialCalibration.CALIBRATED,
        ),
        True,
    ),
    BoardStage.Board10x10: GeometryMetadata(
        BoardStage.Board10x10,
        "10x10",
        10,
        10,
        GeometryUnlocks(2, 1),
        10,
        9,
        VictoryProfile(
            "Checkmate 10x10",
            4_902_105,
            MaterialCalibration.CALIBRATED,
        ),
        True,
    ),
    BoardStage.Board12x10: GeometryMetadata(
        BoardStage.Board12x10,
        "12x10",
        12,
        10,
        GeometryUnlocks(3, 1),
        12,
        11,
        VictoryProfile(
            "Checkmate 12x10",
            4_902_106,
            MaterialCalibration.CALIBRATED,
        ),
        True,
    ),
    BoardStage.Board12x12: GeometryMetadata(
        BoardStage.Board12x12,
        "12x12",
        12,
        12,
        GeometryUnlocks(3, 2),
        12,
        11,
        VictoryProfile(
            "Checkmate 12x12",
            4_902_107,
            MaterialCalibration.CALIBRATED,
        ),
        False,
    ),
}


def geometry_for_stage(stage: BoardStage | int) -> GeometryMetadata:
    try:
        board_stage = BoardStage(stage)
    except ValueError as error:
        raise ValueError(f"Unknown board stage: {stage}") from error
    return _GEOMETRY_BY_STAGE[board_stage]


def _board_stage(stage: BoardStage | int, endpoint: str) -> BoardStage:
    if not isinstance(stage, int) or isinstance(stage, bool):
        raise ValueError(
            f"{endpoint} board stage must be an integer; got {stage!r}"
        )
    try:
        return BoardStage(stage)
    except ValueError as error:
        raise ValueError(
            f"{endpoint} board stage must be between -1 and 4; got {stage}"
        ) from error


def _validate_selectable(stage: BoardStage, endpoint: str) -> None:
    if not geometry_for_stage(stage).selectable:
        raise ValueError(
            f"{endpoint} board stage {stage.value} is legacy-only "
            "and not selectable"
        )


def build_geometry_progression(
    start: BoardStage | int,
    end: BoardStage | int,
) -> GeometryProgression:
    start_stage = _board_stage(start, "start")
    end_stage = _board_stage(end, "end")
    if start_stage > end_stage:
        raise ValueError(
            f"start board stage {start_stage.value} must not follow "
            f"end board stage {end_stage.value}"
        )
    if start_stage not in _SELECTABLE_START_STAGES:
        raise ValueError(
            f"start board stage {start_stage.value} is not selectable"
        )
    _validate_selectable(start_stage, "start")
    _validate_selectable(end_stage, "end")
    start_index = _SELECTABLE_STAGE_ORDER.index(start_stage)
    end_index = _SELECTABLE_STAGE_ORDER.index(end_stage)
    return _build_progression(
        geometry_for_stage(stage)
        for stage in _SELECTABLE_STAGE_ORDER[start_index:end_index + 1]
    )


def build_legacy_ordered_progression(
    start: BoardStage | int = BoardStage.Board8x8,
) -> GeometryProgression:
    start_stage = _board_stage(start, "legacy start")
    if start_stage not in (
        BoardStage.Board8x8,
        BoardStage.Board10x8,
    ):
        raise ValueError(
            "legacy ordered board stage must start at 8x8 or 10x8; "
            f"got {start_stage.value}"
        )
    start_index = _LEGACY_STAGE_ORDER.index(start_stage)
    return _build_progression(
        geometry_for_stage(stage)
        for stage in _LEGACY_STAGE_ORDER[start_index:]
    )


def _build_progression(
    stages_source: Iterable[GeometryMetadata],
) -> GeometryProgression:
    stages = tuple(stages_source)
    precollected = stages[0].unlocks
    endpoint = stages[-1]
    generated = GeometryUnlocks(
        endpoint.unlocks.board_files - precollected.board_files,
        endpoint.unlocks.board_ranks - precollected.board_ranks,
    )
    transitions = tuple(
        GeometryTransition(
            source,
            destination,
            GeometryUnlocks(
                destination.unlocks.board_files - source.unlocks.board_files,
                destination.unlocks.board_ranks - source.unlocks.board_ranks,
            ),
        )
        for source, destination in zip(stages, stages[1:])
    )
    return GeometryProgression(
        stages,
        precollected,
        generated,
        endpoint,
        endpoint.victory,
        transitions,
    )
