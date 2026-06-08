from typing import TYPE_CHECKING

from BaseClasses import LocationProgressType
from ..CheckIds import brush_check_id, collected_object_check_id, container_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.OkamiEnemies import OkamiEnemies
from ..Enums.RegionNames import RegionNames, MapIds, MapIndexes
from ..Types import ExitData, LocData,EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
   RegionNames.CURSED_HANA_VALLEY:[ExitData(RegionNames.HANA_VALLEY_SAKIGAMI,required_items_events=["Hana Valley - Grow Guardian Sapling"],one_way=True,loading_screen=False)],
   RegionNames.HANA_VALLEY_SAKIGAMI:[ExitData(RegionNames.HANA_VALLEY,required_items_events=["Hana Valley - Guardian Sapling Restoration"],one_way=True)],
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
        "Hana Valley - Freestanding Chest": LocData(container_check_id(MapIds.HANA_VALLEY, 9)),  # spawn_idx=9, Traveler's Charm
        "Hana Valley - Buried chest near tunnel": LocData(container_check_id(MapIds.HANA_VALLEY, 5), type=LocationType.BURIED_CHEST),  # spawn_idx=5, Stray Bead
        #Not present in cursed hana
        "Hana Valley - Buried chest at entrance boulder": LocData(container_check_id(MapIds.HANA_VALLEY, 6), type=LocationType.BURIED_CHEST,required_items_events=["Hana Valley - Guardian Sapling Restoration"]),  # spawn_idx=6, Coral Fragment
    },
    RegionNames.HANA_VALLEY_SAKIGAMI: {
        "Hana Valley - Sakigami": LocData(brush_check_id(4), type=LocationType.CONSTELLATION,progress_type=LocationProgressType.EXCLUDED),  # Brush acquisition (Bloom)
    },
    RegionNames.HANA_VALLEY: {
        "Hana Valley - Chest on Island": LocData(container_check_id(MapIds.HANA_VALLEY, 10),required_items_events=["Hana Valley - Guardian Sapling Restoration"]),  # spawn_idx=10, Travel Guide: Digging Tips
        # Note: Sun Fragment chest (idx=80 in spreadsheet) may use a different system - keeping as collected object for now
        "Hana Valley - Sun Fragment Chest (Bloom every Tree)": LocData(collected_object_check_id(MapIndexes.HANA_VALLEY, 80),  # mapId=4 (HanaValley enum index)
            required_brush_techniques=[BrushTechniques.GREENSPROUT_BLOOM], power_slash_level=1,progress_type=LocationProgressType.EXCLUDED),
    }
}
