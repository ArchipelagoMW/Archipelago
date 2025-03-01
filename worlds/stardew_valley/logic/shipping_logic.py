from functools import cached_property
from typing import Union, List

from Utils import cache_self1
from .base_logic import BaseLogic, BaseLogicMixin
from .building_logic import BuildingLogicMixin
from .has_logic import HasLogicMixin
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from ..locations import LocationTags, locations_by_tag
from ..options import ExcludeGingerIsland, Shipsanity
from ..options import SpecialOrderLocations
from ..stardew_rule import StardewRule
from ..strings.building_names import Building


class ShippingLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shipping = ShippingLogic(*args, **kwargs)


class ShippingLogic(BaseLogic[Union[ReceivedLogicMixin, ShippingLogicMixin, BuildingLogicMixin, RegionLogicMixin, HasLogicMixin]]):

    @cached_property
    def can_use_shipping_bin(self) -> StardewRule:
        return self.logic.building.has_building(Building.shipping_bin)

    @cache_self1
    def can_ship(self, item: str) -> StardewRule:
        return self.logic.shipping.can_use_shipping_bin & self.logic.has(item)

    def can_ship_everything(self) -> StardewRule:
        shipsanity_prefix = "Shipsanity: "
        all_items_to_ship = []
        exclude_island = self.options.exclude_ginger_island == ExcludeGingerIsland.option_true
        exclude_qi = not (self.options.special_order_locations & SpecialOrderLocations.value_qi)
        mod_list = self.options.mods.value
        for location in locations_by_tag[LocationTags.SHIPSANITY_FULL_SHIPMENT]:
            if exclude_island and LocationTags.GINGER_ISLAND in location.tags:
                continue
            if exclude_qi and LocationTags.REQUIRES_QI_ORDERS in location.tags:
                continue
            if location.mod_name and location.mod_name not in mod_list:
                continue
            all_items_to_ship.append(location.name[len(shipsanity_prefix):])
        return self.logic.building.has_building(Building.shipping_bin) & self.logic.has_all(*all_items_to_ship)

    def can_ship_everything_in_slot(self, all_location_names_in_slot: List[str]) -> StardewRule:
        if self.options.shipsanity == Shipsanity.option_none:
            return self.logic.shipping.can_ship_everything()

        rules = [self.logic.building.has_building(Building.shipping_bin)]

        for shipsanity_location in locations_by_tag[LocationTags.SHIPSANITY]:
            if shipsanity_location.name not in all_location_names_in_slot:
                continue
            rules.append(self.logic.region.can_reach_location(shipsanity_location.name))
        return self.logic.and_(*rules)
