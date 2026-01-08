import typing as t
from dataclasses import dataclass

from BaseClasses import CollectionState

@dataclass
class LogicContext:
    displacement_warp_enabled: bool
    flight_enabled: bool
    floor_grapple_clip_enabled: bool
    brown_rocket_jump_enabled: bool
    red_rocket_jump_enabled: bool
    roof_grapple_clip_enabled: bool
    start_location: int
    obscure_skips: bool
    require_nodes: bool
    wall_grapple_clip_difficulty: int
    player: int


AccessRule = t.Callable[[CollectionState, LogicContext], bool]
