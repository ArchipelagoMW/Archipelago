from functools import cached_property

from Utils import cache_self1
from .base_logic import BaseLogic, BaseLogicMixin
from ..locations import LocationTags, locations_by_tag
from ..stardew_rule import StardewRule
from ..strings.building_names import Building


class ShippingLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shipping = ShippingLogic(*args, **kwargs)


class ShippingLogic(BaseLogic):

    @cached_property
    def can_use_shipping_bin(self) -> StardewRule:
        return self.logic.building.has_building(Building.shipping_bin)

    @cache_self1
    def can_ship(self, item: str) -> StardewRule:
        return self.logic.shipping.can_use_shipping_bin & self.logic.has(item)

    def can_ship_everything(self) -> StardewRule:
        shipsanity_prefix = "Shipsanity: "
        all_items_to_ship = []
        for location in locations_by_tag[LocationTags.SHIPSANITY_FULL_SHIPMENT]:
            if not self.content.are_all_enabled(location.content_packs):
                continue
            all_items_to_ship.append(location.name[len(shipsanity_prefix):])
        return self.logic.building.has_building(Building.shipping_bin) & self.logic.has_all(*all_items_to_ship)
