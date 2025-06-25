from typing import TYPE_CHECKING
from ..Types import ExitData, LocData, BrushTechniques, RegionNames, EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.CAVE_OF_NAGI: [ExitData("Exit to River of the Heavens", RegionNames.RIVER_OF_THE_HEAVENS_NAGI),
                               ExitData("Repair Nagi's statue", RegionNames.CAVE_OF_NAGI_TACHIGAMI,
                                        has_events=["Cave of Nagi - Repair statue"])],
    RegionNames.CAVE_OF_NAGI_TACHIGAMI: [ExitData("Clear power slash tutorial", RegionNames.CAVE_OF_NAGI,
                                                  has_events=["Cave of Nagi - Cut tutorial rock"])]
}
events = {
    RegionNames.CAVE_OF_NAGI: {
        "Cave of Nagi - Repair statue": EventData(required_brush_techniques=[BrushTechniques.REJUVENATION]),
    },
    # Never gets collected, probably bc it's assumed you can backtrack
    RegionNames.CAVE_OF_NAGI_TACHIGAMI: {
        "Cave of Nagi - Cut tutorial rock": EventData(power_slash_level=1)
    }
}
locations = {
    RegionNames.CAVE_OF_NAGI: {
        "Cave of Nagi - Stray Bead Chest": LocData(4),
    },
    RegionNames.CAVE_OF_NAGI_TACHIGAMI: {
        "Cave of Nagi - Tachigami": LocData(5),
    }
}
