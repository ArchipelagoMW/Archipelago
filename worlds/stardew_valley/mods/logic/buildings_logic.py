from typing import Dict

from ..mod_data import ModNames
from ...logic.base_logic import LogicRegistry
from ...logic.has_logic import HasLogicMixin
from ...logic.money_logic import MoneyLogic
from ...options import Mods
from ...stardew_rule import StardewRule
from ...strings.artisan_good_names import ArtisanGood
from ...strings.building_names import ModBuilding
from ...strings.metal_names import MetalBar
from ...strings.region_names import Region


class ModBuildingLogic(HasLogicMixin):
    player: int
    money: MoneyLogic
    mods_option: Mods

    def __init__(self, player: int, registry: LogicRegistry, money: MoneyLogic, mods_option: Mods):
        super().__init__(player, registry)
        self.money = money
        self.mods_option = mods_option

    def get_modded_building_rules(self) -> Dict[str, StardewRule]:
        buildings = dict()
        if ModNames.tractor in self.mods_option:
            tractor_rule = self.money.can_spend_at(Region.carpenter, 150000) & self.has(MetalBar.iron) & self.has(MetalBar.iridium) & self.has(
                ArtisanGood.battery_pack)
            buildings.update({ModBuilding.tractor_garage: tractor_rule})
        return buildings
