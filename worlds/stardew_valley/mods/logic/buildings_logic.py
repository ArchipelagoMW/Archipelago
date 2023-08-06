from typing import Iterable

from ...logic.has_logic import HasLogic
from ...logic.money_logic import MoneyLogic
from ...strings.artisan_good_names import ArtisanGood
from ...strings.building_names import ModBuilding
from ..mod_data import ModNames
from ...strings.metal_names import MetalBar
from ...strings.region_names import Region


class ModBuildingLogic:
    player: int
    has: HasLogic
    money: MoneyLogic
    mods_option: Iterable[str]

    def __init__(self, player: int, has: HasLogic, money: MoneyLogic, mods_option: Iterable[str]):
        self.player = player
        self.has = has
        self.money = money
        self.mods_option = mods_option

    def get_modded_building_rules(self):
        buildings = {}
        if ModNames.tractor in self.mods_option:
            tractor_rule = self.money.can_spend_at(Region.carpenter, 150000) & self.has(MetalBar.iron) & self.has(MetalBar.iridium) & self.has(ArtisanGood.battery_pack)
            buildings.update({ModBuilding.tractor_garage: tractor_rule})
        return buildings
