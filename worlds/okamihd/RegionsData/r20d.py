from typing import TYPE_CHECKING

from rule_builder.rules import True_, Has
from ..CheckIds import container_check_id, brush_check_id, shop_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.OkamiEnemies import OkamiEnemies
from ..Enums.RegionNames import RegionNames, MapIds
from ..Enums.WarpType import WarpType
from ..Rules import gen_thunder_chest_rule
from ..Types import ExitData, LocData, EventData, WarpData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.ONI_ISLAND_ENTRANCE: [
        ExitData(RegionNames.ONI_ISLAND_ENTRANCE_BRIDGE,
                 required_items_events=["Fire Tablet", BrushTechniques.INFERNO], one_way=True, loading_screen=False)
    ],
    RegionNames.ONI_ISLAND_ENTRANCE_SEA_OF_FIRE: [

        ExitData(RegionNames.ONI_ISLAND_ENTRANCE_UPPER, one_way=True, loading_screen=False,
                 required_items_events=["Fire Tablet", BrushTechniques.INFERNO])
    ],
    RegionNames.ONI_ISLAND_ENTRANCE_BRIDGE: [
        ExitData(RegionNames.ONI_ISLAND_ENTRANCE, one_way=True, loading_screen=False),
        ExitData(RegionNames.ONI_ISLAND_ENTRANCE_SEA_OF_FIRE,one_way=True,loading_screen=False,required_items_events=["Fire Tablet"])
    ],
    RegionNames.ONI_ISLAND_ENTRANCE_UPPER: [
        ExitData(RegionNames.ONI_ISLAND_ENTRANCE_SEA_OF_FIRE, one_way=True, loading_screen=False),
        ExitData(RegionNames.ONI_ISLAND_ENTRANCE_BRIDGE, one_way=True, loading_screen=False),
        ExitData(RegionNames.ONI_ISLAND_INTERIOR_ENTRANCE_ROOM,required_items_events=["Oni Island - Mandatory Fight before entrance"])
    ]

}
events = {
    RegionNames.ONI_ISLAND_ENTRANCE_UPPER:{
        "Oni Island - Mandatory Fight before entrance":EventData(mandatory_enemies=[OkamiEnemies.RED_OGRE,OkamiEnemies.BLUE_OGRE])
    },
    RegionNames.ONI_ISLAND_EXTERIOR_ROOF:{
        "Oni Island - Grab Key on the roof":EventData(required_brush_techniques=[BrushTechniques.CATWALK])
    }
}
locations = {
    RegionNames.ONI_ISLAND_ENTRANCE_SEA_OF_FIRE: {
        "Oni Island - East Vine Island chest on sea of fire": LocData(container_check_id(MapIds.ONI_ISLAND_EXT, 0),
                                                                      required_brush_techniques=[
                                                                          BrushTechniques.GREENSPROUT_VINE],required_items_events=["Fire Tablet"]),
        "Oni Island - West Vine Island chest on sea of fire": LocData(container_check_id(MapIds.ONI_ISLAND_EXT, 1),
                                                                      required_brush_techniques=[
                                                                          BrushTechniques.GREENSPROUT_VINE],required_items_events=["Fire Tablet"]),
    },
    RegionNames.ONI_ISLAND_ENTRANCE_UPPER: {
        "Oni Island - West chest on sea upper center": LocData(container_check_id(MapIds.ONI_ISLAND_EXT, 2),
                                                               required_brush_techniques=[
                                                                   BrushTechniques.GREENSPROUT_VINE]),
        "Oni Island - East chest on sea upper center": LocData(container_check_id(MapIds.ONI_ISLAND_EXT, 3),
                                                               required_brush_techniques=[
                                                                   BrushTechniques.GREENSPROUT_VINE])
    }
}
warps = {
}
