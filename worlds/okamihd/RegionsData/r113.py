from typing import TYPE_CHECKING

from ..CheckIds import container_check_id
from ..Enums.OkamiEnemies import OkamiEnemies
from ..Types import LocData, EventData, ExitData
from ..Enums.RegionNames import RegionNames, MapIds

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.RYOSHIMA_COAST_BANDIT_SPIDER: [
        ExitData(RegionNames.RYOSHIMA_COAST, one_way=True, required_items_events=["Ryoshima Coast - Defeat Bandit Spider in cave"])
    ]
}
events = {
    RegionNames.RYOSHIMA_COAST_BANDIT_SPIDER: {
        "Ryoshima Coast - Defeat Bandit Spider in cave": EventData(mandatory_enemies=[OkamiEnemies.BANDIT_SPIDER]),
        "Ryoshima Coast - Clear 10 Devil Gates in cave": EventData(
            mandatory_enemies=[OkamiEnemies.GREEN_IMP, OkamiEnemies.RED_IMP, OkamiEnemies.YELLOW_IMP,
                               OkamiEnemies.DEAD_FISH, OkamiEnemies.BUD_OGRE, OkamiEnemies.BLUE_IMP,
                               OkamiEnemies.CROW_TENGU, OkamiEnemies.CHIMERA, OkamiEnemies.BLACK_IMP,
                               OkamiEnemies.ICE_LIPS, OkamiEnemies.FIRE_EYE],required_items_events=["Ryoshima Coast - Defeat Bandit Spider in cave"]),
    }

}
locations = {
    RegionNames.RYOSHIMA_COAST_BANDIT_SPIDER: {
        "Ryoshima Coast - Chest after Bandit Spider": LocData(container_check_id(MapIds.RYOSHIMA_BANDIT_SPIDER, 0),required_items_events=["Ryoshima Coast - Defeat Bandit Spider in cave"]),
        "Ryoshima Coast - Chest after 10 devil gates": LocData(container_check_id(MapIds.RYOSHIMA_BANDIT_SPIDER, 1),required_items_events=["Ryoshima Coast - Clear 10 Devil Gates in cave"])
    }
}
