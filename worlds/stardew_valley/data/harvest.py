from dataclasses import dataclass
from typing import Tuple, Sequence, Mapping

from .game_item import ItemSource, ItemTag
from ..strings.season_names import Season


@dataclass(frozen=True, kw_only=True)
class ForagingSource(ItemSource):
    regions: Tuple[str, ...]
    seasons: Tuple[str, ...] = Season.all


@dataclass(frozen=True, kw_only=True)
class SeasonalForagingSource(ItemSource):
    season: str
    days: Sequence[int]
    regions: Tuple[str, ...]

    def as_foraging_source(self) -> ForagingSource:
        return ForagingSource(seasons=(self.season,), regions=self.regions)


@dataclass(frozen=True, kw_only=True)
class FruitBatsSource(ItemSource):
    ...


@dataclass(frozen=True, kw_only=True)
class MushroomCaveSource(ItemSource):
    ...


@dataclass(frozen=True, kw_only=True)
class HarvestFruitTreeSource(ItemSource):
    add_tags = (ItemTag.CROPSANITY,)

    sapling: str
    seasons: Tuple[str, ...] = Season.all

    @property
    def requirement_tags(self) -> Mapping[str, Tuple[ItemTag, ...]]:
        return {
            self.sapling: (ItemTag.CROPSANITY_SEED,)
        }


@dataclass(frozen=True, kw_only=True)
class HarvestCropSource(ItemSource):
    add_tags = (ItemTag.CROPSANITY,)

    seed: str
    seasons: Tuple[str, ...] = Season.all
    """Empty means it can't be grown on the farm."""

    @property
    def requirement_tags(self) -> Mapping[str, Tuple[ItemTag, ...]]:
        return {
            self.seed: (ItemTag.CROPSANITY_SEED,)
        }


@dataclass(frozen=True, kw_only=True)
class ArtifactSpotSource(ItemSource):
    amount: int
