from typing import TYPE_CHECKING

from ..Types import ExitData, LocData, BrushTechniques, RegionNames, EventData, OkamiEnnemies

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
   RegionNames.CURSED_HANA_VALLEY:[ExitData("Cursed Hana Valley - Exit to Cursed Shinshu Field",RegionNames.CURSED_SHINSHU_FIELD),
                                    ExitData("Enter Sakigami sequence",RegionNames.HANA_VALLEY_SAKIGAMI,has_events=["Hana Valley - Grow Guardian Sapling"])],
   RegionNames.HANA_VALLEY_SAKIGAMI:[ExitData("Hana Valley Restoration",RegionNames.HANA_VALLEY,has_events=["Hana Valley - Guardian Sapling Restoration"])],
   RegionNames.HANA_VALLEY:[ExitData("Hana Valley - Exit to Cursed Shinshu Field",RegionNames.CURSED_SHINSHU_FIELD,doesnt_have_events=["Shinshu Field - Restore Guardian Sapling"]),
                            ExitData("Hana Valley - Exit to Sinhsu Field",RegionNames.SHINSHU_FIELD,has_events=["Shinshu Field - Restore Guardian Sapling"])]
}
events = {
    RegionNames.CURSED_HANA_VALLEY:{
        "Hana Valley - Open the sun stone door": EventData(required_brush_techniques=[BrushTechniques.SUNRISE], mandatory_enemies=[OkamiEnnemies.GREEN_IMP,OkamiEnnemies.YELLOW_IMP]),
        "Hana Valley - Defeat Sleepy": EventData(power_slash_level=1,required_items_events=["Hana Valley - Open the sun stone door"]),
        "Hana Valley - Grow Guardian Sapling": EventData(required_brush_techniques=[BrushTechniques.SUNRISE],required_items_events=["Hana Valley - Defeat Sleepy"]),
    },
    # Never gets collected, probably bc it's assumed you can backtrack
    RegionNames.HANA_VALLEY_SAKIGAMI:{
        "Hana Valley - Guardian Sapling Restoration": EventData(
            required_brush_techniques=[BrushTechniques.GREENSPROUT_BLOOM])
    }
}
locations = {
    RegionNames.CURSED_HANA_VALLEY: {
        "Hana Valley - Freestanding Chest": LocData(15),
        "Hana Valley - Buried chest near tunnel": LocData(23, buried=True),
        "Hana Valley - Buried chest at entrance boulder" :LocData(24,buried=True),
    },
    RegionNames.HANA_VALLEY_SAKIGAMI:{
        "Hana Valley - Sakigami": LocData(12)
    },
    RegionNames.HANA_VALLEY:{
      "Hana Valley - Chest on Island":LocData(25),
      "Hana Valley - Sun Fragment Chest (Bloom every Tree)": LocData(26, required_brush_techniques=[BrushTechniques.GREENSPROUT_BLOOM],power_slash_level=1)
    }
}
