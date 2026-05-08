from typing import TYPE_CHECKING

from ..Enums.BrushTechniques import BrushTechniques
from ..Types import ExitData, EventData, LocData
from ..Enums.RegionNames import RegionNames

if TYPE_CHECKING:
    pass

exits = {
    RegionNames.CURSED_RYOSHIMA_COAST: [
        ExitData('Enter Guardian Sapling Cave', RegionNames.CURSED_RYOSHIMA_COAST_GUARDIAN_SAPLING_CAVE,
                 has_events=["Ryoshima Coast - Open Guardian Sapling Cave"])
    ],
    RegionNames.CURSED_RYOSHIMA_COAST_GUARDIAN_SAPLING_CAVE:[
        ExitData('Ryoshima Coast Restoration',RegionNames.RYOSHIMA_COAST,has_events=["Ryoshima Coast - Bloom the Guardian Sapling"])
    ]
}
events = {
    RegionNames.CURSED_RYOSHIMA_COAST: {
        "Ryoshima Coast - Open Guardian Sapling Cave": EventData(cherry_bomb_level=1)
    },
    RegionNames.CURSED_RYOSHIMA_COAST_GUARDIAN_SAPLING_CAVE: {
        "Ryoshima Coast - Water the Guardian Sapling": EventData(
            required_brush_techniques=[BrushTechniques.WATERSPOUT]),
        "Ryoshima Coast - Bloom the Guardian Sapling": EventData(
            required_brush_techniques=[BrushTechniques.GREENSPROUT_BLOOM],
            required_items_events=["Ryoshima Coast - Water the Guardian Sapling"])
    }
}
locations = {
}
