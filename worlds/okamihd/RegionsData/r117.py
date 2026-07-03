from typing import TYPE_CHECKING

from BaseClasses import LocationProgressType
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
    RegionNames.NORTHERN_RYOSHIMA_COAST_CB2_CAVE:{
        "Northern Ryoshima Coast - Offer 120,000 yen in Cherry Bomb 2 Fountain": EventData()
    }
}
locations = {
    RegionNames.NORTHERN_RYOSHIMA_COAST_PS2_CAVE: {
        # Brush upgrade id 25
        "Northern Ryoshima Coast - Bakugami (Cherry Bomb 2)": LocData(25, type=LocationType.CONSTELLATION,progress_type=LocationProgressType.EXCLUDED),
        "Northern Ryoshima Coast - Chest after Cherry Bomb 2": LocData(container_check_id(MapIds.CHERRY_BOMB_2_CAVE, 0))
    }

}
