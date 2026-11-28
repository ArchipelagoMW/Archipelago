from Utils import cache_self1
from .base_logic import BaseLogic, BaseLogicMixin
from ..stardew_rule import Reach, StardewRule, false_, true_
from ..strings.region_names import Region

main_outside_area = {Region.stardew_valley, Region.farm_house, Region.farm, Region.town, Region.beach, Region.mountain, Region.forest, Region.bus_stop,
                     Region.backwoods, Region.tunnel_entrance}

always_accessible_regions_without_er = {*main_outside_area, Region.hospital, Region.carpenter_house, Region.alex_house, Region.ranch, Region.farm_cave, Region.tent,
                                        Region.pierre_house, Region.saloon, Region.blacksmith_house, Region.trailer, Region.museum, Region.mayor_house,
                                        Region.haley_house, Region.sam_house, Region.jojamart, Region.fish_cabin}


class RegionLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.region = RegionLogic(*args, **kwargs)


class RegionLogic(BaseLogic):

    @cache_self1
    def can_reach(self, region_name: str) -> StardewRule:
        if self.options.entrance_randomization == self.options.entrance_randomization.option_disabled and region_name in always_accessible_regions_without_er:
            return true_

        if region_name not in self.regions:
            return false_

        return Reach(region_name, "Region", self.player)

    def can_reach_any(self, *region_names: str) -> StardewRule:
        if self.options.entrance_randomization == self.options.entrance_randomization.option_disabled and any(
                r in always_accessible_regions_without_er for r in region_names):
            return true_
        return self.logic.or_(*(self.logic.region.can_reach(spot) for spot in region_names))

    def can_reach_all(self, *region_names: str) -> StardewRule:
        return self.logic.and_(*(self.logic.region.can_reach(spot) for spot in region_names))

    def can_reach_all_except_one(self, *region_names: str) -> StardewRule:
        num_required = len(region_names) - 1
        if num_required <= 0:
            num_required = len(region_names)
        return self.logic.count(num_required, *(self.logic.region.can_reach(spot) for spot in region_names))

    @cache_self1
    def can_reach_location(self, location_name: str) -> StardewRule:
        return Reach(location_name, "Location", self.player)

    # @cache_self1
    # def can_reach_entrance(self, entrance_name: str) -> StardewRule:
    #     return Reach(entrance_name, "Entrance", self.player)
