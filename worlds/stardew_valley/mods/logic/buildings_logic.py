from typing import Dict, Union

from ..mod_data import ModNames
from ...logic.base_logic import BaseLogicMixin, BaseLogic
from ...logic.has_logic import HasLogicMixin
from ...logic.money_logic import MoneyLogicMixin
from ...stardew_rule import StardewRule
from ...strings.artisan_good_names import ArtisanGood
from ...strings.building_names import ModBuilding
from ...strings.metal_names import MetalBar
from ...strings.region_names import Region


class ModBuildingLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.building = ModBuildingLogic(*args, **kwargs)


class ModBuildingLogic(BaseLogic[Union[MoneyLogicMixin, HasLogicMixin]]):

    def get_modded_building_rules(self) -> Dict[str, StardewRule]:
        buildings = dict()
        if ModNames.tractor in self.options.mods:
            tractor_rule = (self.logic.money.can_spend_at(Region.carpenter, 150000) &
                            self.logic.has_all(MetalBar.iron, MetalBar.iridium, ArtisanGood.battery_pack))
            buildings.update({ModBuilding.tractor_garage: tractor_rule})
        return buildings
