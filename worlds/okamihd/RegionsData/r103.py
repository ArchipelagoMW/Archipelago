from typing import TYPE_CHECKING

from ..CheckIds import brush_check_id, collected_object_check_id, container_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.OkamiEnemies import OkamiEnemies
from ..Enums.RegionNames import RegionNames
from ..Types import ExitData, LocData,EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
   RegionNames.CURSED_HANA_VALLEY:[ ExitData("Enter Sakigami sequence",RegionNames.HANA_VALLEY_SAKIGAMI,has_events=["Hana Valley - Grow Guardian Sapling"])],
   RegionNames.HANA_VALLEY_SAKIGAMI:[ExitData("Hana Valley Restoration",RegionNames.HANA_VALLEY,has_events=["Hana Valley - Guardian Sapling Restoration"])],
}
events = {
    RegionNames.CURSED_HANA_VALLEY:{
        "Hana Valley - Open the sun stone door": EventData(required_brush_techniques=[BrushTechniques.SUNRISE], mandatory_enemies=[OkamiEnemies.GREEN_IMP,OkamiEnemies.YELLOW_IMP]),
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
        "Hana Valley - Freestanding Chest": LocData(container_check_id(0x103, 9)),  # spawn_idx=9, Traveler's Charm
        "Hana Valley - Buried chest near tunnel": LocData(container_check_id(0x103, 5), type=LocationType.BURIED_CHEST),  # spawn_idx=5, Stray Bead
        "Hana Valley - Buried chest at entrance boulder": LocData(container_check_id(0x103, 6), type=LocationType.BURIED_CHEST),  # spawn_idx=6, Coral Fragment
    },
    RegionNames.HANA_VALLEY_SAKIGAMI: {
        "Hana Valley - Sakigami": LocData(brush_check_id(4), type=LocationType.CONSTELLATION),  # Brush acquisition (Bloom)
    },
    RegionNames.HANA_VALLEY: {
        "Hana Valley - Chest on Island": LocData(container_check_id(0x103, 10)),  # spawn_idx=10, Travel Guide: Digging Tips
        # Note: Sun Fragment chest (idx=80 in spreadsheet) may use a different system - keeping as collected object for now
        "Hana Valley - Sun Fragment Chest (Bloom every Tree)": LocData(collected_object_check_id(4, 80),  # mapId=4 (HanaValley enum index)
            required_brush_techniques=[BrushTechniques.GREENSPROUT_BLOOM], power_slash_level=1),
    }
}
