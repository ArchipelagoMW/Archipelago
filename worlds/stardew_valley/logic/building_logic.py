from functools import cached_property
from typing import Dict, Union

from Utils import cache_self1
from .base_logic import BaseLogic, BaseLogicMixin
from .has_logic import HasLogicMixin
from .money_logic import MoneyLogicMixin
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from ..stardew_rule import StardewRule, Has, true_
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
            Building.big_barn: self.logic.money.can_spend(12_000) & self.logic.has_all(Material.wood, Material.stone) & self.logic.building.has_building(Building.barn),
            Building.deluxe_barn: self.logic.money.can_spend(25_000) & self.logic.has_all(Material.wood, Material.stone) & self.logic.building.has_building(Building.big_barn),
            Building.coop: self.logic.money.can_spend(4000) & self.logic.has_all(Material.wood, Material.stone),
            Building.big_coop: self.logic.money.can_spend(10_000) & self.logic.has_all(Material.wood, Material.stone) & self.logic.building.has_building(Building.coop),
            Building.deluxe_coop: self.logic.money.can_spend(20_000) & self.logic.has_all(Material.wood, Material.stone) & self.logic.building.has_building(Building.big_coop),
            Building.fish_pond: self.logic.money.can_spend(5000) & self.logic.has_all(Material.stone, WaterItem.seaweed, WaterItem.green_algae),
            Building.mill: self.logic.money.can_spend(2500) & self.logic.has_all(Material.stone, Material.wood, ArtisanGood.cloth),
            Building.shed: self.logic.money.can_spend(15_000) & self.logic.has(Material.wood),
            Building.big_shed: self.logic.money.can_spend(20_000) & self.logic.has_all(Material.wood, Material.stone) & self.logic.building.has_building(Building.shed),
            Building.silo: self.logic.money.can_spend(100) & self.logic.has_all(Material.stone, Material.clay, MetalBar.copper),
            Building.slime_hutch: self.logic.money.can_spend(10_000) & self.logic.has_all(Material.stone, MetalBar.quartz, MetalBar.iridium),
            Building.stable: self.logic.money.can_spend(10_000) & self.logic.has_all(Material.hardwood, MetalBar.iron),
            Building.well: self.logic.money.can_spend(1000) & self.logic.has(Material.stone),
            Building.shipping_bin: self.logic.money.can_spend(250) & self.logic.has(Material.wood),
            Building.kitchen: self.logic.money.can_spend(10_000) & self.logic.has(Material.wood) & self.logic.building.has_building(Building.farm_house),
            Building.kids_room: self.logic.money.can_spend(65_000) & self.logic.has(Material.hardwood) & self.logic.building.has_building(Building.kitchen),
            Building.cellar: self.logic.money.can_spend(100_000) & self.logic.building.has_building(Building.kids_room),
            # @formatter:on
        })

    def update_rules(self, new_rules: Dict[str, StardewRule]):
        self.registry.building_rules.update(new_rules)

    @cache_self1
    def has_building(self, building: str) -> StardewRule:
        building_progression = self.content.features.building_progression

        if building in building_progression.starting_buildings:
            return true_

        # Shipping bin is special. The mod auto-builds it when received, no need to go to Robin.
        if building == Building.shipping_bin and building_progression.is_progressive:
            return self.logic.received(Building.shipping_bin)

        carpenter_rule = self.logic.building.can_construct_buildings
        if building_progression.is_progressive:
            item, count = building_progression.to_progressive_item(building)
            return self.logic.received(item, count) & carpenter_rule

        return Has(building, self.registry.building_rules, has_group) & carpenter_rule

    @cached_property
    def can_construct_buildings(self) -> StardewRule:
        return self.logic.region.can_reach(Region.carpenter)
