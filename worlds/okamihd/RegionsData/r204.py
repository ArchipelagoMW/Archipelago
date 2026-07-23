from typing import TYPE_CHECKING

from rule_builder.rules import  HasAny
from ..CheckIds import container_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.OkamiEnemies import OkamiEnemies
from ..Types import LocData, EventData, ExitData
from ..Enums.RegionNames import RegionNames, MapIds

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.INSIDE_THE_DRAGON: [
        ExitData(RegionNames.INSIDE_THE_DRAGON_DEEP, required_items_events=["Inside the dragon - Cross to deeper part"])
    ],
    RegionNames.INSIDE_THE_DRAGON_DEEP: [
        ExitData(RegionNames.INSIDE_THE_DRAGON_ORB, required_items_events=["Inside the dragon - Open door to dragon orb"])
    ]
}
events = {
    RegionNames.INSIDE_THE_DRAGON: {
        "Inside the dragon - Cross to deeper part": EventData(
            special_rule=HasAny(BrushTechniques.WATERSPOUT, "Holy Eagle")),
        "Inside the dragon - Grab the key": EventData(required_brush_techniques=[BrushTechniques.WATERSPOUT])

    },
    RegionNames.INSIDE_THE_DRAGON_DEEP: {
        "Inside the dragon - Open door to dragon orb": EventData(
            required_items_events=["Inside the dragon - Grab the key"])
    },
    RegionNames.INSIDE_THE_DRAGON_ORB: {
        "Inside the dragon - Flood with acid": EventData(
            required_brush_techniques=[BrushTechniques.WATERSPOUT],needs_long_swim=True),
        "Inside the dragon - Get Dragon Orb": EventData(
            required_brush_techniques=[BrushTechniques.WATERSPOUT], needs_long_swim=True ,mandatory_enemies=[OkamiEnemies.TUBE_FOX]),
    }

}
locations = {
    RegionNames.INSIDE_THE_DRAGON: {
        "Inside the dragon - Clam on pillar near entrance": LocData(container_check_id(MapIds.INSIDE_THE_DRAGON, 3)),
        "Inside the dragon - Freestanding Clam near entrance 1": LocData(
            container_check_id(MapIds.INSIDE_THE_DRAGON, 4)),
        "Inside the dragon - Freestanding Clam near entrance 2": LocData(
            container_check_id(MapIds.INSIDE_THE_DRAGON, 0)),
        "Inside the dragon - Freestanding Clam on high east pillar near entrance": LocData(
            container_check_id(MapIds.INSIDE_THE_DRAGON, 1)),
        "Inside the dragon - Clam on first pillar after tunnel": LocData(
            container_check_id(MapIds.INSIDE_THE_DRAGON, 2),
            special_rule=HasAny(BrushTechniques.WATERSPOUT, "Holy Eagle")),
        "Inside the dragon - Clam on middle pillar after tunnel": LocData(
            container_check_id(MapIds.INSIDE_THE_DRAGON, 5),
            special_rule=HasAny(BrushTechniques.WATERSPOUT, "Holy Eagle")),
        "Inside the dragon - Clam on last pillars after tunnel high": LocData(
            container_check_id(MapIds.INSIDE_THE_DRAGON, 7),
            special_rule=HasAny(BrushTechniques.WATERSPOUT, "Holy Eagle")),
        "Inside the dragon - Clam on last pillars after tunnel low": LocData(
            container_check_id(MapIds.INSIDE_THE_DRAGON, 6),
            special_rule=HasAny(BrushTechniques.WATERSPOUT, "Holy Eagle")),

        "Inside the dragon - Buried Clam near entrance west of river": LocData(
            container_check_id(MapIds.INSIDE_THE_DRAGON, 9), type=LocationType.STONE_BURIED_CHEST),
        "Inside the dragon - Buried Clam before small bridge": LocData(
            container_check_id(MapIds.INSIDE_THE_DRAGON, 10), type=LocationType.STONE_BURIED_CHEST),
    },
    RegionNames.INSIDE_THE_DRAGON_DEEP: {
        "Inside the dragon - Chest in hidden waterspout area near origin mirror": LocData(
            container_check_id(MapIds.INSIDE_THE_DRAGON, 8), required_brush_techniques=[BrushTechniques.WATERSPOUT]),
        "Inside the dragon - Buried Clam After crossing pillars": LocData(
            container_check_id(MapIds.INSIDE_THE_DRAGON, 11), type=LocationType.STONE_BURIED_CHEST),
        "Inside the dragon - Buried Clam near origin mirror": LocData(
            container_check_id(MapIds.INSIDE_THE_DRAGON, 12), type=LocationType.STONE_BURIED_CHEST),
    }
}
