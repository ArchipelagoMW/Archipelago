from typing import Dict

from Utils import cache_self1
from .cached_logic import CachedLogic
from .has_logic import HasLogic, CachedRules
from .money_logic import MoneyLogic
from .received_logic import ReceivedLogic
from .region_logic import RegionLogic
from ..options import BuildingProgression
from ..stardew_rule import StardewRule, True_, False_, Has
from ..strings.ap_names.event_names import Event
from ..strings.artisan_good_names import ArtisanGood
from ..strings.building_names import Building
from ..strings.fish_names import WaterItem
from ..strings.material_names import Material
from ..strings.metal_names import MetalBar
from ..strings.region_names import Region


class BuildingLogic(CachedLogic):
    player: int
    building_option: BuildingProgression
    received: ReceivedLogic
    has: HasLogic
    region: RegionLogic
    money: MoneyLogic
    building_rules: Dict[str, StardewRule]

    def __init__(self, player: int, cached_rules: CachedRules, building_option: BuildingProgression,
                 received: ReceivedLogic, has: HasLogic, region: RegionLogic, money: MoneyLogic):
        super().__init__(player, cached_rules)
        self.player = player
        self.building_option = building_option
        self.received = received
        self.has = has
        self.region = region
        self.money = money
        self.building_rules = dict()

    def initialize_rules(self):
        self.building_rules.update({
            # @formatter:off
            Building.barn: self.money.can_spend(6000) & self.has((Material.wood, Material.stone)),
            Building.big_barn: self.money.can_spend(12000) & self.has((Material.wood, Material.stone)) & self.has_building(Building.barn),
            Building.deluxe_barn: self.money.can_spend(25000) & self.has((Material.wood, Material.stone)) & self.has_building(Building.big_barn),
            Building.coop: self.money.can_spend(4000) & self.has((Material.wood, Material.stone)),
            Building.big_coop: self.money.can_spend(10000) & self.has((Material.wood, Material.stone)) & self.has_building(Building.coop),
            Building.deluxe_coop: self.money.can_spend(20000) & self.has((Material.wood, Material.stone)) & self.has_building(Building.big_coop),
            Building.fish_pond: self.money.can_spend(5000) & self.has((Material.stone, WaterItem.seaweed, WaterItem.green_algae)),
            Building.mill: self.money.can_spend(2500) & self.has((Material.stone, Material.wood, ArtisanGood.cloth)),
            Building.shed: self.money.can_spend(15000) & self.has(Material.wood),
            Building.big_shed: self.money.can_spend(20000) & self.has((Material.wood, Material.stone)) & self.has_building(Building.shed),
            Building.silo: self.money.can_spend(100) & self.has((Material.stone, Material.clay, MetalBar.copper)),
            Building.slime_hutch: self.money.can_spend(10000) & self.has((Material.stone, MetalBar.quartz, MetalBar.iridium)),
            Building.stable: self.money.can_spend(10000) & self.has((Material.hardwood, MetalBar.iron)),
            Building.well: self.money.can_spend(1000) & self.has(Material.stone),
            Building.shipping_bin: self.money.can_spend(250) & self.has(Material.wood),
            Building.kitchen: self.money.can_spend(10000) & self.has(Material.wood) & self.has_house(0),
            Building.kids_room: self.money.can_spend(50000) & self.has(Material.hardwood) & self.has_house(1),
            Building.cellar: self.money.can_spend(100000) & self.has_house(2),
            # @formatter:on
        })

    def update_rules(self, new_rules: Dict[str, StardewRule]):
        self.building_rules.update(new_rules)

    @cache_self1
    def has_building(self, building: str) -> StardewRule:
        carpenter_rule = self.received(Event.can_construct_buildings)
        if not self.building_option & BuildingProgression.option_progressive:
            return Has(building, self.building_rules) & carpenter_rule

        count = 1
        if building in [Building.coop, Building.barn, Building.shed]:
            building = f"Progressive {building}"
        elif building.startswith("Big"):
            count = 2
            building = " ".join(["Progressive", *building.split(" ")[1:]])
        elif building.startswith("Deluxe"):
            count = 3
            building = " ".join(["Progressive", *building.split(" ")[1:]])
        return self.received(f"{building}", count) & carpenter_rule

    @cache_self1
    def has_house(self, upgrade_level: int) -> StardewRule:
        if upgrade_level < 1:
            return True_()

        if upgrade_level > 3:
            return False_()

        carpenter_rule = self.received(Event.can_construct_buildings)
        if self.building_option & BuildingProgression.option_progressive:
            return carpenter_rule & self.received(f"Progressive House", upgrade_level)

        if upgrade_level == 1:
            return carpenter_rule & Has(Building.kitchen, self.building_rules)

        if upgrade_level == 2:
            return carpenter_rule & Has(Building.kids_room, self.building_rules)

        # if upgrade_level == 3:
        return carpenter_rule & Has(Building.cellar, self.building_rules)
