from typing import TYPE_CHECKING

from ..Types import ExitData, LocData, BrushTechniques, RegionNames, EventData, OkamiEnnemies

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
   RegionNames.CURSED_HANA_VALLEY:[ExitData("Cursed Hana Valley - Exit to Cursed Shinshu Field",RegionNames.CURSED_SHINSHU_FIELD),
                                    ExitData("Restore Hana Valley",RegionNames.HANA_VALLEY,has_events=["Hana Valley - Guardian Sapling Restoration"])],
   RegionNames.HANA_VALLEY:[ExitData("Hana Valley - Exit to Cursed Shinshu Field",RegionNames.CURSED_SHINSHU_FIELD,doesnt_have_events=["Shinshu Field - Restore Guardian Sapling"]),
                            ExitData("Hana Valley - Exit to Sinhsu Field",RegionNames.SHINSHU_FIELD,has_events=["Shinshu Field - Restore Guardian Sapling"])]
}
events = {
    RegionNames.CURSED_HANA_VALLEY:{
        "Hana Valley - Open the sun stone door": EventData(required_brush_techniques=[BrushTechniques.SUNRISE], mandatory_enemies=[OkamiEnnemies.GREEN_IMP,OkamiEnnemies.YELLOW_IMP]),
        "Hana Valley - Defeat Sleepy": EventData(power_slash_level=1,has_events=["Hana Valley - Open the sun stone door"]),
        "Hana Valley - Grow Guardian Sapling": EventData(required_brush_techniques=[BrushTechniques.SUNRISE],has_events=["Hana Valley - Defeat Sleepy"]),
        #FIXME: Create Region to force this event to be collected when getting Sakigami
        "Hana Valley - Guardian Sapling Restoration": EventData(required_brush_techniques=[BrushTechniques.GREENSPROUT_BLOOM],has_events=["Hana Valley - Grow Guardian Sapling"])
    }
}
locations = {
    RegionNames.CURSED_HANA_VALLEY: {
        "Hana Valley - Freestanding Chest": LocData(15),
        "Hana Valley - Sakigami" : LocData(12,has_events=["Hana Valley - Grow Guardian Sapling"])
    }
}
