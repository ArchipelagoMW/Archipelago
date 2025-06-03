from typing import TYPE_CHECKING
from ..Types import ExitData, LocData, BrushTechniques, RegionNames, EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.RIVER_OF_THE_HEAVENS_KAMIKI: [ExitData("Exit to Cursed Kamiki", RegionNames.CURSED_KAMIKI,
                                                       doesnt_have_events=["Cursed Kamiki - Cutting the peach"]),
                                              ExitData("Exit to Kamiki (stone)", RegionNames.STONE_KAMIKI,
                                                       has_events=["Cursed Kamiki - Cutting the peach"]
                                                       ,
                                                       doesnt_have_events=["Kamiki Village - Restoring the villagers"]),
                                              ExitData("Exit to Kamiki", RegionNames.KAMIKI_VILLAGE,
                                                       has_events=["Cursed Kamiki - Cutting the peach",
                                                                   "Kamiki Village - Restoring the villagers"]),
                                              ExitData("Crossing the River to the Cave of Nagi",
                                                       RegionNames.RIVER_OF_THE_HEAVENS_NAGI,
                                                       has_events=["River of the Heavens - Restoring the River"])],
    RegionNames.RIVER_OF_THE_HEAVENS_NAGI: [
        ExitData("Crossing the River to Kamiki Village", RegionNames.RIVER_OF_THE_HEAVENS_KAMIKI,
                 has_events=["River of the Heavens - Restoring the River"]),
        ExitData("Exit to Cave of Nagi", RegionNames.CAVE_OF_NAGI)]
}
events = {
    RegionNames.RIVER_OF_THE_HEAVENS_KAMIKI: {
        "River of the Heavens (Kamiki Side) - Restoring the River": EventData(
            override_event_item_name="River of the Heavens - Restoring the River",
            required_brush_techniques=[BrushTechniques.REJUVENATION],
        )
    },
    # Doable from the other side too
    RegionNames.RIVER_OF_THE_HEAVENS_NAGI: {
        "River of the Heavens (Nagi Side) - Restoring the River": EventData(
            required_brush_techniques=[BrushTechniques.REJUVENATION],
            override_event_item_name="River of the Heavens - Restoring the River")
    }
}
locations = {
    RegionNames.RIVER_OF_THE_HEAVENS_KAMIKI: {
        "River of the Heavens - Ledge Chest": LocData(1),
        "River of the Heavens - Yomigami": LocData(2),
    },
    RegionNames.RIVER_OF_THE_HEAVENS_NAGI: {
        "River of the Heavens - Astral Pouch": LocData(3),
    }
}
