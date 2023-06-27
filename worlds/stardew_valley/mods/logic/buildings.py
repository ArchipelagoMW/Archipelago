from ...strings.building_names import ModBuilding
from ..mod_data import ModNames
from ...strings.metal_names import MetalBar
from ...options import StardewOptions
from ... import options


def modded_buildings(self, world_options: StardewOptions):
    buildings = {}
    if ModNames.tractor in world_options[options.Mods]:
        buildings.update({
            ModBuilding.tractor_garage: self.can_spend_money(150000) & self.has(MetalBar.iron) &
                                        self.has(MetalBar.iridium) & self.has("Battery Pack")})
    return buildings
