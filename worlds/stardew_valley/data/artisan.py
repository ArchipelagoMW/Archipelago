from dataclasses import dataclass

from .game_item import source_dataclass_args, ItemSource


@dataclass(**source_dataclass_args)
class MachineSource(ItemSource):
    item: str  # this should be optional (worm bin)
    machine: str
    # seasons
