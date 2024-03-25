from dataclasses import dataclass, field
from typing import Tuple, Sequence

from .game_item import ItemSource, source_dataclass_args
from ..strings.season_names import Season


@dataclass(**source_dataclass_args)
class ForagingSource(ItemSource):
    regions: Tuple[str, ...]
    seasons: Tuple[str, ...] = field(default=Season.all)
    requires_hoe: bool = field(default=False)


@dataclass(**source_dataclass_args)
class SeasonalForagingSource(ItemSource):
    season: str
    days: Sequence[int]
    regions: Tuple[str, ...]

    def as_foraging_source(self) -> ForagingSource:
        return ForagingSource(seasons=(self.season,), regions=self.regions)


@dataclass(**source_dataclass_args)
class FruitBatsSource(ItemSource):
    ...


@dataclass(**source_dataclass_args)
class MushroomCaveSource(ItemSource):
    ...
