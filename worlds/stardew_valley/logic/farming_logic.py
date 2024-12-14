from functools import cached_property
from typing import Union, Tuple

from Utils import cache_self1
from .base_logic import BaseLogicMixin, BaseLogic
from ..content.vanilla.ginger_island import ginger_island_content_pack
from ..stardew_rule import StardewRule
from ..strings.fertilizer_names import Fertilizer
from ..strings.region_names import Region, LogicRegion
from ..strings.season_names import Season
from ..strings.tool_names import Tool

farming_region_by_season = {
    Season.spring: LogicRegion.spring_farming,
    Season.summer: LogicRegion.summer_farming,
    Season.fall: LogicRegion.fall_farming,
    Season.winter: LogicRegion.winter_farming,
}


class FarmingLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.farming = FarmingLogic(*args, **kwargs)


class FarmingLogic(BaseLogic):

    @cached_property
    def has_farming_tools(self) -> StardewRule:
        return self.logic.tool.has_tool(Tool.hoe) & self.logic.tool.can_water()

    def has_fertilizer(self, tier: int) -> StardewRule:
        assert 0 <= tier <= 3
        if tier == 0:
            return self.logic.true_
        if tier == 1:
            return self.logic.has(Fertilizer.basic)
        if tier == 2:
            return self.logic.has(Fertilizer.quality)
        if tier == 3:
            return self.logic.has(Fertilizer.deluxe)

        return self.logic.false_

    @cache_self1
    def can_plant_and_grow_item(self, seasons: Union[str, Tuple[str]]) -> StardewRule:
        if seasons == ():  # indoor farming
            return (self.logic.region.can_reach(Region.greenhouse) | self.logic.farming.has_island_farm()) & self.logic.farming.has_farming_tools

        if isinstance(seasons, str):
            seasons = (seasons,)

        return self.logic.or_(*(self.logic.region.can_reach(farming_region_by_season[season]) for season in seasons))

    def has_island_farm(self) -> StardewRule:
        if self.content.is_enabled(ginger_island_content_pack):
            return self.logic.region.can_reach(Region.island_west)
        return self.logic.false_
