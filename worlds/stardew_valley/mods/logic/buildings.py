from typing import Union

from ...strings.artisan_good_names import ArtisanGood
from ...strings.building_names import ModBuilding
from ..mod_data import ModNames
from ...strings.metal_names import MetalBar
from ...strings.region_names import Region


def get_modded_building_rules(vanilla_logic, active_mods):
    buildings = {}
    if ModNames.tractor in active_mods:
        buildings.update({
            ModBuilding.tractor_garage: vanilla_logic.can_spend_money_at(Region.carpenter, 150000) & vanilla_logic.has(MetalBar.iron) &
                                        vanilla_logic.has(MetalBar.iridium) & vanilla_logic.has(ArtisanGood.battery_pack)})
    return buildings
