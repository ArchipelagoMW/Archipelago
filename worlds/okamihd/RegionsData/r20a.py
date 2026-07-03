from typing import TYPE_CHECKING

from rule_builder.rules import Has
from ..CheckIds import container_check_id, brush_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.WarpType import WarpType
from ..Types import LocData, ExitData, WarpData, EventData
from ..Enums.RegionNames import RegionNames, MapIds

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.CATCALL_TOWER_BOTTOM: [
        ExitData(RegionNames.CATCALL_TOWER, loading_screen=False),
    ],
    RegionNames.CATCALL_TOWER: [
        ExitData(RegionNames.CATCALL_TOWER_TOP, loading_screen=False)
    ]
}
events = {
    RegionNames.CATCALL_TOWER_TOP: {
        "Catcall Tower - Unlock warp": EventData()
    }
}
locations = {
    RegionNames.CATCALL_TOWER_BOTTOM: {
        "Catcall Tower - Freestanding Chest in front of tower": LocData(container_check_id(MapIds.CATCALL_TOWER, 11)),
        "Catcall Tower - Freestanding Chest on west pillar": LocData(container_check_id(MapIds.CATCALL_TOWER, 10),
                                                                     required_brush_techniques=[
                                                                         BrushTechniques.CATWALK]),
        "Catcall Tower - Freestanding Chest on east pillar": LocData(container_check_id(MapIds.CATCALL_TOWER, 9),
                                                                     required_brush_techniques=[
                                                                         BrushTechniques.CATWALK])
    },
    RegionNames.CATCALL_TOWER: {
        "Catcall Tower - Chest on 3rd cloud platform": LocData(container_check_id(MapIds.CATCALL_TOWER, 8)),
        "Catcall Tower - Chest on stone platform above 3rd cloud platform": LocData(
            container_check_id(MapIds.CATCALL_TOWER, 7)),
        "Catcall Tower - Chest on 4th cloud platform": LocData(container_check_id(MapIds.CATCALL_TOWER, 6)),
        "Catcall Tower - Chest on stone platform above 4th cloud platform": LocData(
            container_check_id(MapIds.CATCALL_TOWER, 5)),
        "Catcall Tower - Chest on 5th cloud platform": LocData(container_check_id(MapIds.CATCALL_TOWER, 4)),
    },
    RegionNames.CATCALL_TOWER_TOP: {
        "Catcall Tower - Freestanding chest near mermaid spring": LocData(container_check_id(MapIds.CATCALL_TOWER, 3)),
        "Catcall Tower - Freestanding chest on top of tower 2F": LocData(container_check_id(MapIds.CATCALL_TOWER, 0)),
        # Requires Feedbag fish - Maybe place one guaranteed in the tower ?
        "Catcall Tower - Kabegami": LocData(brush_check_id(30),type=LocationType.CONSTELLATION),
        "Catcall Tower - Freestanding chest on top of tower behind cat statue": LocData(container_check_id(MapIds.CATCALL_TOWER, 2)),
        "Catcall Tower - Secret chest after climbing the tower twice": LocData(container_check_id(MapIds.CATCALL_TOWER, 1)),
    }

}
warps = {
    RegionNames.CATCALL_TOWER_TOP: [
        WarpData(WarpType.MERMAID_SPRING, Has("Catcall Tower - Unlock warp"), Has("Catcall Tower - Unlock warp"))
    ]
}
