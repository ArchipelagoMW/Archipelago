from typing import TYPE_CHECKING

from ..Types import ExitData, LocData, BrushTechniques, RegionNames, EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
   RegionNames.CURSED_HANA_VALLEY:[ExitData("Exit to Cursed Shinshu Field",RegionNames.CURSED_SHINSHU_FIELD),
                                    ExitData("Restore Hana Valley",RegionNames.HANA_VALLEY,has_events=["Hana Valley - Guardian Sapling Restoration"])]
}
events = {
    RegionNames.CURSED_HANA_VALLEY:{
        "Hana Valley - Open the sun stone door": EventData(required_brush_techniques=[BrushTechniques.SUNRISE]),
        "Hana Valley - Defeat Sleepy": EventData(power_slash_level=1,has_events=["Hana Valley - Open the sun stone door"]),
        "Hana Valley - Grow Guardian Sapling": EventData(required_brush_techniques=[BrushTechniques.SUNRISE],has_events=["Hana Valley - Defeat Sleepy"]),
        "Hana Valley - Guardian Sapling Restoration": EventData(required_brush_techniques=[BrushTechniques.GREENSPROUT_BLOOM],has_events=["Hana Valley - Grow Guardian Sapling"])
    }
}
locations = {
    RegionNames.CURSED_HANA_VALLEY: {
        "Hana Valley - Freestanding Chest": LocData(15),
        "Hana Valley - Sakigami" : LocData(12,has_events=["Hana Valley - Grow Guardian Sapling"])
    }
}
