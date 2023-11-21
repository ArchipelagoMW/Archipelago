from functools import cached_property
from typing import Union

from Utils import cache_self1
from .base_logic import BaseLogic, BaseLogicMixin
from .building_logic import BuildingLogicMixin
from .has_logic import HasLogicMixin
from .region_logic import RegionLogicMixin
from ..locations import LocationTags, locations_by_tag
from ..options import ExcludeGingerIsland
from ..options import SpecialOrderLocations
from ..stardew_rule import StardewRule, And
from ..strings.building_names import Building
from ..strings.region_names import Region


class ShippingLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shipping = ShippingLogic(*args, **kwargs)


class ShippingLogic(BaseLogic[Union[ShippingLogicMixin, BuildingLogicMixin, RegionLogicMixin, HasLogicMixin]]):

    @cached_property
    def can_use_shipping_bin(self) -> StardewRule:
        return self.logic.buildings.has_building(Building.shipping_bin)

    @cache_self1
    def can_ship(self, item: str) -> StardewRule:
        return self.logic.shipping.can_ship_items & self.logic.has(item)

    @cached_property
    def can_ship_items(self) -> StardewRule:
        return self.logic.region.can_reach(Region.shipping)

    def can_ship_everything(self) -> StardewRule:
        shipsanity_prefix = "Shipsanity: "
        all_items_to_ship = []
        exclude_island = self.options.exclude_ginger_island == ExcludeGingerIsland.option_true
        exclude_qi = self.options.special_order_locations != SpecialOrderLocations.option_board_qi
        mod_list = self.options.mods.value
        for location in locations_by_tag[LocationTags.SHIPSANITY_FULL_SHIPMENT]:
            if exclude_island and LocationTags.GINGER_ISLAND in location.tags:
                continue
            if exclude_qi and LocationTags.REQUIRES_QI_ORDERS in location.tags:
                continue
            if location.mod_name and location.mod_name not in mod_list:
                continue
            all_items_to_ship.append(location.name[len(shipsanity_prefix):])
        return self.logic.buildings.has_building(Building.shipping_bin) & And(*(self.logic.has(item) for item in all_items_to_ship))
