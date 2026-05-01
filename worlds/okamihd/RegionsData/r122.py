from typing import TYPE_CHECKING

from ..CheckIds import brush_check_id, container_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
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
        "River of the Heavens - Ledge Chest": LocData(container_check_id(0x122, 0)),  # spawn_idx=0, Holy Bone S
        "River of the Heavens - Yomigami": LocData(brush_check_id(22), type=LocationType.CONSTELLATION),  # Brush acquisition (bit 22)
    },
    RegionNames.RIVER_OF_THE_HEAVENS_NAGI: {
        "River of the Heavens - Astral Pouch": LocData(container_check_id(0x122, 12)),  # spawn_idx=12, Astral Pouch
    }
}
