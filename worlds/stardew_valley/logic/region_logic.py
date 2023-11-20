from typing import Tuple

from Utils import cache_self1
from .base_logic import BaseLogic
from ..stardew_rule import StardewRule, And, Or, Reach, Count


class RegionLogicMixin(BaseLogic):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.region = self

    @cache_self1
    def can_reach(self, region_name: str) -> StardewRule:
        return Reach(region_name, "Region", self.player)

    @cache_self1
    def can_reach_any(self, region_names: Tuple[str, ...]) -> StardewRule:
        return Or(*(self.region.can_reach(spot) for spot in region_names))

    @cache_self1
    def can_reach_all(self, region_names: Tuple[str, ...]) -> StardewRule:
        return And(*(self.region.can_reach(spot) for spot in region_names))

    @cache_self1
    def can_reach_all_except_one(self, region_names: Tuple[str, ...]) -> StardewRule:
        region_names = list(region_names)
        num_required = len(region_names) - 1
        if num_required <= 0:
            num_required = len(region_names)
        return Count(num_required, [self.region.can_reach(spot) for spot in region_names])

    @cache_self1
    def can_reach_location(self, location_name: str) -> StardewRule:
        return Reach(location_name, "Location", self.player)

    @cache_self1
    def can_reach_entrance(self, entrance_name: str) -> StardewRule:
        return Reach(entrance_name, "Entrance", self.player)
