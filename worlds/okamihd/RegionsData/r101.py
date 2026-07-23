from typing import TYPE_CHECKING

from ..CheckIds import brush_check_id, container_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Types import LocData, EventData
from ..Enums.RegionNames import RegionNames, MapIds

if TYPE_CHECKING:
    pass

exits = {
}
events = {
    RegionNames.CAVE_OF_NAGI: {
        "Cave of Nagi - Repair statue": EventData(required_brush_techniques=[BrushTechniques.REJUVENATION]),
    },
}
locations = {
    RegionNames.CAVE_OF_NAGI: {
        # Containers in this file are at level 0x101.
        "Cave of Nagi - Stray Bead Chest": LocData(container_check_id(MapIds.CAVE_OF_NAGI, 14)),  # Stray Bead
        "Cave of Nagi - Tachigami": LocData(brush_check_id(12), type=LocationType.CONSTELLATION,required_items_events=["Cave of Nagi - Repair statue"]),  # Power Slash
    },

}
