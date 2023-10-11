
from .building_logic import BuildingLogic
from .has_logic import HasLogic
from .region_logic import RegionLogic
from ..options import ExcludeGingerIsland
from ..locations import LocationTags, locations_by_tag
from ..options import SpecialOrderLocations
from ..stardew_rule import StardewRule, And
from ..strings.building_names import Building
from ..strings.region_names import Region


class ShippingLogic:
    player: int
    exclude_ginger_island: ExcludeGingerIsland
    special_orders_option: SpecialOrderLocations
    has: HasLogic
    region: RegionLogic
    buildings: BuildingLogic

    def __init__(self, player: int, exclude_ginger_island: ExcludeGingerIsland, special_orders_option: SpecialOrderLocations, has: HasLogic, region: RegionLogic, buildings: BuildingLogic):
        self.player = player
        self.exclude_ginger_island = exclude_ginger_island
        self.special_orders_option = special_orders_option
        self.has = has
        self.region = region
        self.buildings = buildings

    def can_use_shipping_bin(self, item: str = "") -> StardewRule:
        return self.buildings.has_building(Building.shipping_bin)

    def can_ship(self, item: str = "") -> StardewRule:
        shipping_rule = self.region.can_reach(Region.shipping)
        if item == "":
            return shipping_rule
        return shipping_rule & self.has(item)

    def can_ship_everything(self) -> StardewRule:
        shipsanity_prefix = "Shipsanity: "
        all_items_to_ship = []
        include_island = self.exclude_ginger_island == ExcludeGingerIsland.option_false
        include_qi = self.special_orders_option == SpecialOrderLocations.option_board_qi
        for location in locations_by_tag[LocationTags.SHIPSANITY_FULL_SHIPMENT]:
            if (include_island or LocationTags.GINGER_ISLAND not in location.tags) and \
               (include_qi or LocationTags.REQUIRES_QI_ORDERS not in location.tags):
                all_items_to_ship.append(location.name[len(shipsanity_prefix):])
        return self.buildings.has_building(Building.shipping_bin) & And([self.has(item) for item in all_items_to_ship])
