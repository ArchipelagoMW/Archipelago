from typing import Tuple, Union

from Utils import cache_self1
from .base_logic import BaseLogic, BaseLogicMixin
from .has_logic import HasLogicMixin
from ..options import EntranceRandomization
from ..stardew_rule import StardewRule, Reach, false_, true_
from ..strings.region_names import Region

main_outside_area = {Region.menu, Region.stardew_valley, Region.farm_house, Region.farm, Region.town, Region.beach, Region.mountain, Region.forest,
                     Region.bus_stop, Region.backwoods, Region.bus_tunnel, Region.tunnel_entrance}
always_accessible_regions_without_er = {*main_outside_area, Region.community_center, Region.pantry, Region.crafts_room, Region.fish_tank, Region.boiler_room,
                                        Region.vault, Region.bulletin_board, Region.mines, Region.hospital, Region.carpenter, Region.alex_house,
                                        Region.elliott_house, Region.ranch, Region.farm_cave, Region.wizard_tower, Region.tent, Region.pierre_store,
                                        Region.saloon, Region.blacksmith, Region.trailer, Region.museum, Region.mayor_house, Region.haley_house,
                                        Region.sam_house, Region.jojamart, Region.fish_shop}

always_regions_by_setting = {EntranceRandomization.option_disabled: always_accessible_regions_without_er,
                             EntranceRandomization.option_pelican_town: always_accessible_regions_without_er,
                             EntranceRandomization.option_non_progression: always_accessible_regions_without_er,
                             EntranceRandomization.option_buildings_without_house: main_outside_area,
                             EntranceRandomization.option_buildings: main_outside_area,
                             EntranceRandomization.option_chaos: always_accessible_regions_without_er}


class RegionLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.region = RegionLogic(*args, **kwargs)


class RegionLogic(BaseLogic[Union[RegionLogicMixin, HasLogicMixin]]):

    @cache_self1
    def can_reach(self, region_name: str) -> StardewRule:
        if region_name in always_regions_by_setting[self.options.entrance_randomization]:
            return true_

        if region_name not in self.regions:
            return false_

        return Reach(region_name, "Region", self.player)

    @cache_self1
    def can_reach_any(self, region_names: Tuple[str, ...]) -> StardewRule:
        if any(r in always_regions_by_setting[self.options.entrance_randomization] for r in region_names):
            return true_

        return self.logic.or_(*(self.logic.region.can_reach(spot) for spot in region_names))

    @cache_self1
    def can_reach_all(self, region_names: Tuple[str, ...]) -> StardewRule:
        return self.logic.and_(*(self.logic.region.can_reach(spot) for spot in region_names))

    @cache_self1
    def can_reach_all_except_one(self, region_names: Tuple[str, ...]) -> StardewRule:
        region_names = list(region_names)
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
