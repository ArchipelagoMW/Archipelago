from typing import TYPE_CHECKING

from ..CheckIds import container_check_id
from ..Enums.OkamiEnemies import OkamiEnemies
from ..Types import LocData, EventData, ExitData
from ..Enums.RegionNames import RegionNames, MapIds

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
}
events = {
}
locations = {
    RegionNames.DRAGON_PALACE_CAVE: {
        "Dragon Palace - Chest in treasure cave 1": LocData(container_check_id(MapIds.DRAGON_PALACE_TREASURE, 2)),
        "Dragon Palace - Chest in treasure cave 2": LocData(container_check_id(MapIds.DRAGON_PALACE_TREASURE, 1)),
        "Dragon Palace - Chest in treasure cave 3": LocData(container_check_id(MapIds.DRAGON_PALACE_TREASURE, 0)),
    }
}
