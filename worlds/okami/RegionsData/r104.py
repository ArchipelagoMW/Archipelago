from typing import TYPE_CHECKING

from ..Types import ExitData, LocData, BrushTechniques, RegionNames, EventData, OkamiEnnemies

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
   RegionNames.TSUTA_RUINS:[ExitData("Exit Tsuta Ruins",RegionNames.CURSED_AGATA_FOREST)],
}
events = {
}
locations = {
    RegionNames.TSUTA_RUINS: {
        "Tsuta Ruins - Freestanding Chest at Entrance": LocData(78),
        "Tsuta Ruins - Treasure Bud in Entrance Hall Middle": LocData(79,required_brush_techniques=[BrushTechniques.GREENSPROUT_BLOOM]),
        "Tsuta Ruins - Treasure Bud in Entrance Hall Right Side" :LocData(80,required_brush_techniques=[BrushTechniques.GREENSPROUT_BLOOM]),
    },
}
