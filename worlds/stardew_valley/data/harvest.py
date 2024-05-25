from dataclasses import dataclass
from typing import Tuple, Sequence, Mapping

from .game_item import ItemSource, source_dataclass_args, ItemTag
from ..strings.season_names import Season


@dataclass(**source_dataclass_args)
class ForagingSource(ItemSource):
    regions: Tuple[str, ...]
    seasons: Tuple[str, ...] = Season.all
    requires_hoe: bool = False


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


@dataclass(**source_dataclass_args)
class HarvestFruitTreeSource(ItemSource):
    add_tags = (ItemTag.CROPSANITY,)

    sapling: str
    seasons: Tuple[str, ...] = Season.all

    @property
    def requirement_tags(self) -> Mapping[str, Tuple[ItemTag, ...]]:
        return {
            self.sapling: (ItemTag.CROPSANITY_SEED,)
        }


@dataclass(**source_dataclass_args)
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
