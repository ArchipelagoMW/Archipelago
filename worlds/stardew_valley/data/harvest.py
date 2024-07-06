from dataclasses import dataclass
from typing import Tuple, Sequence, Mapping

from .game_item import ItemSource, kw_only, ItemTag, Requirement
from ..strings.season_names import Season


@dataclass(frozen=True, **kw_only)
class ForagingSource(ItemSource):
    regions: Tuple[str, ...]
    seasons: Tuple[str, ...] = Season.all
    other_requirements: Tuple[Requirement, ...] = ()

    def __post_init__(self):
        if isinstance(self.regions, str):
            super().__setattr__("regions", (self.regions,))
        if isinstance(self.seasons, str):
            super().__setattr__("seasons", (self.seasons,))
        if isinstance(self.other_requirements, Requirement):
            super().__setattr__("other_requirements", (self.other_requirements,))


@dataclass(frozen=True, **kw_only)
class SeasonalForagingSource(ItemSource):
    season: str
    days: Sequence[int]
    regions: Tuple[str, ...]

    def as_foraging_source(self) -> ForagingSource:
        return ForagingSource(seasons=(self.season,), regions=self.regions)

    def __post_init__(self):
        if isinstance(self.regions, str):
            super().__setattr__("regions", (self.regions,))


@dataclass(frozen=True, **kw_only)
class FruitBatsSource(ItemSource):
    ...


@dataclass(frozen=True, **kw_only)
class MushroomCaveSource(ItemSource):
    ...


@dataclass(frozen=True, **kw_only)
class HarvestFruitTreeSource(ItemSource):
    add_tags = (ItemTag.CROPSANITY,)

    sapling: str
    seasons: Tuple[str, ...] = Season.all

    def __post_init__(self):
        if isinstance(self.seasons, str):
            super().__setattr__("seasons", (self.seasons,))

    @property
    def requirement_tags(self) -> Mapping[str, Tuple[ItemTag, ...]]:
        return {
            self.sapling: (ItemTag.CROPSANITY_SEED,)
        }


@dataclass(frozen=True, **kw_only)
class HarvestCropSource(ItemSource):
    add_tags = (ItemTag.CROPSANITY,)

    seed: str
    seasons: Tuple[str, ...] = Season.all
    """Empty means it can't be grown on the farm."""

    def __post_init__(self):
        if isinstance(self.seasons, str):
            super().__setattr__("seasons", (self.seasons,))

    @property
    def requirement_tags(self) -> Mapping[str, Tuple[ItemTag, ...]]:
        return {
            self.seed: (ItemTag.CROPSANITY_SEED,)
        }


@dataclass(frozen=True, **kw_only)
class ArtifactSpotSource(ItemSource):
    amount: int
