from functools import cached_property

from Utils import cache_self1
from .base_logic import BaseLogicMixin, BaseLogic
from ..data.harvest import ForagingSource, HarvestFruitTreeSource, HarvestCropSource
from ..stardew_rule import StardewRule
from ..strings.ap_names.community_upgrade_names import CommunityUpgrade
from ..strings.region_names import Region


class HarvestingLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.harvesting = HarvestingLogic(*args, **kwargs)


class HarvestingLogic(BaseLogic):

    @cached_property
    def can_harvest_from_fruit_bats(self) -> StardewRule:
        return self.logic.region.can_reach(Region.farm_cave) & self.logic.received(CommunityUpgrade.fruit_bats)

    @cached_property
    def can_harvest_from_mushroom_cave(self) -> StardewRule:
        return self.logic.region.can_reach(Region.farm_cave) & self.logic.received(CommunityUpgrade.mushroom_boxes)

    @cache_self1
    def can_forage_from(self, source: ForagingSource) -> StardewRule:
        seasons_rule = self.logic.season.has_any(source.seasons)
        if source.require_all_regions:
            regions_rule = self.logic.region.can_reach_all(*source.regions)
        else:
            regions_rule = self.logic.region.can_reach_any(*source.regions)
        if source.grind_months == 0:
            return seasons_rule & regions_rule
        else:
            return seasons_rule & regions_rule & self.logic.time.has_lived_months(source.grind_months)

    @cache_self1
    def can_harvest_tree_from(self, source: HarvestFruitTreeSource) -> StardewRule:
        # FIXME tool not required for this
        region_to_grow_rule = self.logic.farming.can_plant_and_grow_item(source.seasons)
        sapling_rule = self.logic.has(source.sapling)
        # Because it takes 1 month to grow the sapling
        time_rule = self.logic.time.has_lived_months(1)

        return region_to_grow_rule & sapling_rule & time_rule

    @cache_self1
    def can_harvest_crop_from(self, source: HarvestCropSource) -> StardewRule:
        region_to_grow_rule = self.logic.farming.can_plant_and_grow_item(source.seasons)
        seed_rule = self.logic.has(source.seed)
        return region_to_grow_rule & seed_rule
