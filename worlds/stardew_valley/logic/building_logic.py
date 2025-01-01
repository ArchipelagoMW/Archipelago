from functools import cached_property
from typing import Dict, Union

from Utils import cache_self1
from .base_logic import BaseLogic, BaseLogicMixin
from .has_logic import HasLogicMixin
from .money_logic import MoneyLogicMixin
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from ..options import BuildingProgression
from ..stardew_rule import StardewRule, True_, False_, Has
from ..strings.artisan_good_names import ArtisanGood
from ..strings.building_names import Building
from ..strings.fish_names import WaterItem
from ..strings.material_names import Material
from ..strings.metal_names import MetalBar
from ..strings.region_names import Region

has_group = "building"


class BuildingLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.building = BuildingLogic(*args, **kwargs)


class BuildingLogic(BaseLogic[Union[BuildingLogicMixin, MoneyLogicMixin, RegionLogicMixin, ReceivedLogicMixin, HasLogicMixin]]):
    def initialize_rules(self):
        self.registry.building_rules.update({
            # @formatter:off
            Building.barn: self.logic.money.can_spend(6000) & self.logic.has_all(Material.wood, Material.stone),
            Building.big_barn: self.logic.money.can_spend(12000) & self.logic.has_all(Material.wood, Material.stone) & self.logic.building.has_building(Building.barn),
            Building.deluxe_barn: self.logic.money.can_spend(25000) & self.logic.has_all(Material.wood, Material.stone) & self.logic.building.has_building(Building.big_barn),
            Building.coop: self.logic.money.can_spend(4000) & self.logic.has_all(Material.wood, Material.stone),
            Building.big_coop: self.logic.money.can_spend(10000) & self.logic.has_all(Material.wood, Material.stone) & self.logic.building.has_building(Building.coop),
            Building.deluxe_coop: self.logic.money.can_spend(20000) & self.logic.has_all(Material.wood, Material.stone) & self.logic.building.has_building(Building.big_coop),
            Building.fish_pond: self.logic.money.can_spend(5000) & self.logic.has_all(Material.stone, WaterItem.seaweed, WaterItem.green_algae),
            Building.mill: self.logic.money.can_spend(2500) & self.logic.has_all(Material.stone, Material.wood, ArtisanGood.cloth),
            Building.shed: self.logic.money.can_spend(15000) & self.logic.has(Material.wood),
            Building.big_shed: self.logic.money.can_spend(20000) & self.logic.has_all(Material.wood, Material.stone) & self.logic.building.has_building(Building.shed),
            Building.silo: self.logic.money.can_spend(100) & self.logic.has_all(Material.stone, Material.clay, MetalBar.copper),
            Building.slime_hutch: self.logic.money.can_spend(10000) & self.logic.has_all(Material.stone, MetalBar.quartz, MetalBar.iridium),
            Building.stable: self.logic.money.can_spend(10000) & self.logic.has_all(Material.hardwood, MetalBar.iron),
            Building.well: self.logic.money.can_spend(1000) & self.logic.has(Material.stone),
            Building.shipping_bin: self.logic.money.can_spend(250) & self.logic.has(Material.wood),
            Building.kitchen: self.logic.money.can_spend(10000) & self.logic.has(Material.wood) & self.logic.building.has_house(0),
            Building.kids_room: self.logic.money.can_spend(65000) & self.logic.has(Material.hardwood) & self.logic.building.has_house(1),
            Building.cellar: self.logic.money.can_spend(100000) & self.logic.building.has_house(2),
            # @formatter:on
        })

    def update_rules(self, new_rules: Dict[str, StardewRule]):
        self.registry.building_rules.update(new_rules)

    @cache_self1
    def has_building(self, building: str) -> StardewRule:
        # Shipping bin is special. The mod auto-builds it when received, no need to go to Robin.
        if building is Building.shipping_bin:
            if not self.options.building_progression & BuildingProgression.option_progressive:
                return True_()
            return self.logic.received(building)

        carpenter_rule = self.logic.building.can_construct_buildings
        if not self.options.building_progression & BuildingProgression.option_progressive:
            return Has(building, self.registry.building_rules, has_group) & carpenter_rule

        count = 1
        if building in [Building.coop, Building.barn, Building.shed]:
            building = f"Progressive {building}"
        elif building.startswith("Big"):
            count = 2
            building = " ".join(["Progressive", *building.split(" ")[1:]])
        elif building.startswith("Deluxe"):
            count = 3
            building = " ".join(["Progressive", *building.split(" ")[1:]])
        return self.logic.received(building, count) & carpenter_rule

    @cached_property
    def can_construct_buildings(self) -> StardewRule:
        return self.logic.region.can_reach(Region.carpenter)

    @cache_self1
    def has_house(self, upgrade_level: int) -> StardewRule:
        if upgrade_level < 1:
            return True_()

        if upgrade_level > 3:
            return False_()

        carpenter_rule = self.logic.building.can_construct_buildings
        if self.options.building_progression & BuildingProgression.option_progressive:
            return carpenter_rule & self.logic.received(f"Progressive House", upgrade_level)

        if upgrade_level == 1:
            return carpenter_rule & Has(Building.kitchen, self.registry.building_rules, has_group)

        if upgrade_level == 2:
            return carpenter_rule & Has(Building.kids_room, self.registry.building_rules, has_group)

        # if upgrade_level == 3:
        return carpenter_rule & Has(Building.cellar, self.registry.building_rules, has_group)
