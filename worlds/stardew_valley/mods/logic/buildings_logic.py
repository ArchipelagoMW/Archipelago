from typing import Dict

from ...stardew_rule import StardewRule
from ...logic.has_logic import HasLogic
from ...logic.money_logic import MoneyLogic
from ...options import Mods
from ...strings.artisan_good_names import ArtisanGood
from ...strings.building_names import ModBuilding
from ..mod_data import ModNames
from ...strings.metal_names import MetalBar
from ...strings.region_names import Region


class ModBuildingLogic:
    player: int
    has: HasLogic
    money: MoneyLogic
    mods_option: Mods

    def __init__(self, player: int, has: HasLogic, money: MoneyLogic, mods_option: Mods):
        self.player = player
        self.has = has
        self.money = money
        self.mods_option = mods_option

    def get_modded_building_rules(self) -> Dict[str, StardewRule]:
        buildings = dict()
        if ModNames.tractor in self.mods_option:
            tractor_rule = self.money.can_spend_at(Region.carpenter, 150000) & self.has(MetalBar.iron) & self.has(MetalBar.iridium) & self.has(ArtisanGood.battery_pack)
            buildings.update({ModBuilding.tractor_garage: tractor_rule})
        return buildings
