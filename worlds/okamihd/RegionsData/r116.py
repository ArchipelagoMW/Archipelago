from typing import TYPE_CHECKING

from ..CheckIds import container_check_id, brush_check_id
from ..Enums.LocationType import LocationType
from ..Enums.OkamiEnemies import OkamiEnemies
from ..Types import LocData, EventData, ExitData
from ..Enums.RegionNames import RegionNames, MapIds

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
}
events = {
    RegionNames.NORTHERN_RYOSHIMA_COAST_PS2_CAVE:{
        "Northern Ryoshima Coast - Offer 60,000 yen in Power Slash 2 Fountain": EventData()
    }
}
locations = {
    RegionNames.NORTHERN_RYOSHIMA_COAST_PS2_CAVE: {
        # Brush upgrade id 12
        "Northern Ryoshima Coast - Tachigami (Power Slash 2)": LocData(12, type=LocationType.CONSTELLATION),
        "Northern Ryoshima Coast - Chest after Power Slash 2": LocData(container_check_id(MapIds.POWER_SLASH_2_CAVE, 0))
    }

}
