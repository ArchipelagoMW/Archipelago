from typing import TYPE_CHECKING

from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.RegionNames import RegionNames
from ..Types import ExitData, LocData, EventData

if TYPE_CHECKING:
    from .. import OkamiWorld, OkamiOptions

exits = {
    RegionNames.RIVER_OF_THE_HEAVENS_KAMIKI: [ExitData("Crossing the River to the Cave of Nagi",
                                                       RegionNames.RIVER_OF_THE_HEAVENS_NAGI,
                                                       has_events=["River of the Heavens - Restoring the River"])],
    RegionNames.RIVER_OF_THE_HEAVENS_NAGI: [ExitData("Exit to Cave of Nagi", RegionNames.CAVE_OF_NAGI)]
}
events = {
    RegionNames.RIVER_OF_THE_HEAVENS_KAMIKI: {
        "River of the Heavens - Restoring the River": EventData(id=0x200,
                                                                required_brush_techniques=[
                                                                    BrushTechniques.REJUVENATION],
                                                                precollected=lambda o: o.OpenGameStart)
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
