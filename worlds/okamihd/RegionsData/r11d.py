from typing import TYPE_CHECKING

from ..CheckIds import container_check_id
from ..Types import LocData
from ..Enums.RegionNames import RegionNames, MapIds

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
}
events = {
}
locations = {
    RegionNames.NORTHERN_RYOSHIMA_COAST_TREASURE_CAVE: {
        "Northern Ryoshima Coast - Chest in treasure cave 1": LocData(container_check_id(MapIds.NORTHERN_RYOSHIMA_TREASURE, 1)),
        "Northern Ryoshima Coast - Chest in treasure cave 2": LocData(container_check_id(MapIds.NORTHERN_RYOSHIMA_TREASURE, 0)),
        "Northern Ryoshima Coast - Chest in treasure cave 3": LocData(container_check_id(MapIds.NORTHERN_RYOSHIMA_TREASURE, 2)),
    }
}
