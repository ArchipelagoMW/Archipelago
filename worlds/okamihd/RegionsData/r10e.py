from typing import TYPE_CHECKING

from ..CheckIds import container_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.OkamiEnemies import OkamiEnemies
from ..Enums.RegionNames import RegionNames, MapIds
from ..Types import ExitData, LocData, EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.CALCIFIED_CAVERN: [ExitData(RegionNames.MOON_CAVE, has_events=["Calcified Cavern - Fool Yokai Guards"])]
}
events = {
    RegionNames.CALCIFIED_CAVERN: {
        "Calcified Cavern - Defeat devil gate": EventData(mandatory_enemies=[OkamiEnemies.BLACK_IMP]),

        "Calcified Cavern - Fool Yokai Guards": EventData(required_items_events=["Mask","Thunder Brew"])
    }
}
locations = {
    RegionNames.CALCIFIED_CAVERN: {
        "Calcified Cavern - Freestanding item": LocData(container_check_id(MapIds.CALCIFIED_CAVERN, 0),
                                                        type=LocationType.FREESTANDING_ITEM),

        "Calcified Cavern - Chest after devil gate": LocData(container_check_id(MapIds.CALCIFIED_CAVERN, 1), required_items_events=["Calcified Cavern - Defeat devil gate"]),
        "Calcified Cavern - Left Side chest": LocData(container_check_id(MapIds.CALCIFIED_CAVERN, 2)),
        "Calcified Cavern - Frozen Chest": LocData(container_check_id(MapIds.CALCIFIED_CAVERN, 3),
                                                   type=LocationType.FROZEN_CHEST,
                                                   required_items_events=[BrushTechniques.WATERSPOUT])
    }
}
