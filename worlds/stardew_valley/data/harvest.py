from dataclasses import dataclass, field
from typing import Tuple, Sequence

from .game_item import ItemSource
from ..strings.season_names import Season


@dataclass(frozen=True)
class ForagingSource(ItemSource):
    seasons: Tuple[str, ...] = field(default=Season.all, kw_only=True)
    regions: Tuple[str, ...] = field(kw_only=True)
    requires_hoe: bool = field(default=False, kw_only=True)


@dataclass(frozen=True)
class SeasonalForagingSource(ItemSource):
    season: str = field(kw_only=True)
    days: Sequence[int] = field(kw_only=True)
    regions: Tuple[str, ...] = field(kw_only=True)

    def as_foraging_source(self) -> ForagingSource:
        return ForagingSource(seasons=(self.season,), regions=self.regions)


@dataclass(frozen=True)
class FruitBatsSource(ItemSource):
    ...


@dataclass(frozen=True)
class MushroomCaveSource(ItemSource):
    ...
