from dataclasses import dataclass

from .game_item import kw_only, ItemSource


@dataclass(frozen=True, **kw_only)
class MachineSource(ItemSource):
    item: str  # this should be optional (worm bin)
    machine: str
    # seasons
