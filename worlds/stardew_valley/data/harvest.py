from dataclasses import dataclass, field
from typing import List, Tuple, Protocol, Iterable, Sequence

from ..strings.season_names import Season


class HarvestSource(Protocol):
    ...


@dataclass(frozen=True)
class ForagingSource(HarvestSource):
    seasons: Tuple[str, ...] = field(default=Season.all, kw_only=True)
    regions: Tuple[str, ...] = field(kw_only=True)
    requires_hoe: bool = field(default=False, kw_only=True)


@dataclass(frozen=True)
class SeasonalForagingSource(HarvestSource):
    season: str = field(kw_only=True)
    days: Sequence[int] = field(kw_only=True)
    regions: Tuple[str, ...] = field(kw_only=True)

    def as_foraging_source(self) -> ForagingSource:
        return ForagingSource(seasons=(self.season,), regions=self.regions)


@dataclass(frozen=True)
class FruitBatsSource(HarvestSource):
    ...


@dataclass(frozen=True)
class MushroomCaveSource(HarvestSource):
    ...


@dataclass(frozen=True)
class HarvestItem:
    name: str
    harvest_sources: List[HarvestSource] = field(default_factory=list)

    def add_sources(self, sources: Iterable[HarvestSource]):
        self.harvest_sources.extend(sources)
