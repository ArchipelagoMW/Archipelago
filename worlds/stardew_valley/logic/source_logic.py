import functools
from typing import Union, Any, Iterable

from .artisan_logic import ArtisanLogicMixin
from .base_logic import BaseLogicMixin, BaseLogic
from .harvesting_logic import HarvestingLogicMixin
from .has_logic import HasLogicMixin
from .money_logic import MoneyLogicMixin
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from ..data.artisan import MachineSource
from ..data.game_item import PermanentSource, ItemSource, GameItem, ItemTag
from ..data.harvest import ForagingSource, FruitBatsSource, MushroomCaveSource, SeasonalForagingSource, HarvestCropSource, HarvestFruitTreeSource
from ..data.shop import ShopSource
from ..stardew_rule import true_


class SourceLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.source = SourceLogic(*args, **kwargs)


class SourceLogic(BaseLogic[Union[SourceLogicMixin, HasLogicMixin, ReceivedLogicMixin, HarvestingLogicMixin, MoneyLogicMixin, RegionLogicMixin,
ArtisanLogicMixin]]):

    def has_access_to_item(self, item: GameItem):
        rules = []

        # TODO I don't like having to check both the tag and the feature. Tag should not be applied if the feature is not enabled.
        #  Tags should be applied by the feature.
        if ItemTag.CROPSANITY_SEED in item.tags and self.content.features.cropsanity.is_enabled:
            rules.append(self.logic.received(item.name))

        rules.append(self.logic.source.has_access_to_any(item.sources))
        return self.logic.and_(*rules)

    def has_access_to_any(self, sources: Iterable[ItemSource]):
        return self.logic.or_(*(self.logic.source.has_access_to(source) for source in sources))

    @functools.singledispatchmethod
    def has_access_to(self, source: Any):
        raise ValueError(f"Sources of type{type(source)} have no rule registered.")

    @has_access_to.register
    def _(self, source: ForagingSource):
        return self.logic.harvesting.can_forage_from(source)

    @has_access_to.register
    def _(self, source: SeasonalForagingSource):
        # Implementation could be different with some kind of "calendar shuffle"
        return self.logic.harvesting.can_forage_from(source.as_foraging_source())

    @has_access_to.register
    def _(self, _: FruitBatsSource):
        return self.logic.harvesting.can_harvest_from_fruit_bats

    @has_access_to.register
    def _(self, _: MushroomCaveSource):
        return self.logic.harvesting.can_harvest_from_mushroom_cave

    @has_access_to.register
    def _(self, source: ShopSource):
        return self.logic.money.can_shop_from(source)

    @has_access_to.register
    def _(self, source: HarvestFruitTreeSource):
        return self.logic.harvesting.can_harvest_tree_from(source)

    @has_access_to.register
    def _(self, source: HarvestCropSource):
        return self.logic.harvesting.can_harvest_crop_from(source)

    @has_access_to.register
    def _(self, source: MachineSource):
        return self.logic.artisan.can_produce_from(source)

    @has_access_to.register
    def _(self, source: PermanentSource):
        return self.logic.region.can_reach_any(source.regions) if source.regions else true_
