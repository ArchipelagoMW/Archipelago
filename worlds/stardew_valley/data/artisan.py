from dataclasses import dataclass

from .game_item import ItemSource


@dataclass(frozen=True, kw_only=True)
class MachineSource(ItemSource):
    item: str  # this should be optional (worm bin)
    machine: str
    # seasons
