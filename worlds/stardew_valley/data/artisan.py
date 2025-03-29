from dataclasses import dataclass

from .game_item import Source


@dataclass(frozen=True, kw_only=True)
class MachineSource(Source):
    item: str  # this should be optional (worm bin)
    machine: str
    # seasons
