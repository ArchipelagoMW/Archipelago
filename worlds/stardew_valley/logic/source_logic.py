import functools
from typing import Any, Iterable

from .base_logic import BaseLogicMixin, BaseLogic
from ..data.animal import IncubatorSource, OstrichIncubatorSource
from ..data.artisan import MachineSource
from ..data.game_item import GenericSource, Source, GameItem, CustomRuleSource
from ..data.harvest import ForagingSource, FruitBatsSource, MushroomCaveSource, SeasonalForagingSource, \
    HarvestCropSource, HarvestFruitTreeSource, ArtifactSpotSource
from ..data.shop import ShopSource, MysteryBoxSource, ArtifactTroveSource, PrizeMachineSource, FishingTreasureChestSource


class SourceLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.source = SourceLogic(*args, **kwargs)


class SourceLogic(BaseLogic):

    def has_access_to_item(self, item: GameItem):
        rules = []

        if self.content.features.cropsanity.is_included(item):
            rules.append(self.logic.received(item.name))

        rules.append(self.logic.source.has_access_to_any(item.sources))
        return self.logic.and_(*rules)

    def has_access_to_any(self, sources: Iterable[Source]):
        return self.logic.or_(*(self.logic.source.has_access_to(source) & self.logic.requirement.meet_all_requirements(source.other_requirements)
                                for source in sources))

    @functools.singledispatchmethod
    def has_access_to(self, source: Any):
        raise ValueError(f"Sources of type{type(source)} have no rule registered.")

    @has_access_to.register
    def _(self, source: GenericSource):
        return self.logic.region.can_reach_any(source.regions) if source.regions else self.logic.true_

    @has_access_to.register
    def _(self, source: CustomRuleSource):
        return source.create_rule(self.logic)

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
    def _(self, source: IncubatorSource):
        return self.logic.animal.can_incubate(source.egg_item)

    @has_access_to.register
    def _(self, source: OstrichIncubatorSource):
        return self.logic.animal.can_ostrich_incubate(source.egg_item)

    @has_access_to.register
    def _(self, source: MachineSource):
        return self.logic.artisan.can_produce_from(source)

    @has_access_to.register
    def _(self, source: MysteryBoxSource):
        return self.logic.grind.can_grind_mystery_boxes(source.amount)

    @has_access_to.register
    def _(self, source: ArtifactTroveSource):
        return self.logic.grind.can_grind_artifact_troves(source.amount)

    @has_access_to.register
    def _(self, source: PrizeMachineSource):
        return self.logic.grind.can_grind_prize_tickets(source.amount)

    @has_access_to.register
    def _(self, source: FishingTreasureChestSource):
        return self.logic.grind.can_grind_fishing_treasure_chests(source.amount)

    @has_access_to.register
    def _(self, source: ArtifactSpotSource):
        return self.logic.grind.can_grind_artifact_spots(source.amount)
