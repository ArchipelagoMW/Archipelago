from typing import TYPE_CHECKING


from ..CheckIds import container_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.RegionNames import RegionNames, MapIds
from ..Types import ExitData, LocData, EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.ONI_ISLAND_SIDESCROLLER: [
        ExitData(RegionNames.ONI_ISLAND_INTERIOR_4F, required_items_events=["Oni Island - Sidescroller grab key"])
    ]
}
events = {
    RegionNames.ONI_ISLAND_SIDESCROLLER: {
        "Oni Island - Sidescroller start wheels": EventData(required_brush_techniques=[BrushTechniques.THUNDERSTORM]),
        "Oni Island - Sidescroller grab key": EventData(required_brush_techniques=[BrushTechniques.CATWALK],
                                                        power_slash_level=1,
                                                        required_items_events=["Oni Island - Sidescroller start wheels",
                                                                               "Holy Eagle"])
    }
}
locations = {
    RegionNames.ONI_ISLAND_SIDESCROLLER: {
        "Oni Island - Chest above sidescroller key": LocData(container_check_id(MapIds.ONI_ISLAND_SIDESCROLLER, 1),
                                                             required_items_events=[
                                                                 "Oni Island - Sidescroller start wheels",
                                                                 "Holy Eagle"], power_slash_level=1,
                                                             required_brush_techniques=[BrushTechniques.CATWALK,
                                                                                        BrushTechniques.GREENSPROUT_VINE]),
        "Oni Island - Chest in sidescroller west secret passage": LocData(
            container_check_id(MapIds.ONI_ISLAND_SIDESCROLLER, 0),
            required_items_events=[
                "Oni Island - Sidescroller start wheels",
                "Holy Eagle"], power_slash_level=1,
            required_brush_techniques=[BrushTechniques.CATWALK,
                                       BrushTechniques.GREENSPROUT_VINE]),
    }

}
