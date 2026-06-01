from typing import TYPE_CHECKING

from ..CheckIds import container_check_id
from ..Enums.OkamiEnemies import OkamiEnemies
from ..Types import LocData, EventData, ExitData
from ..Enums.RegionNames import RegionNames, MapIds

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.NORTHERN_RYOSHIMA_COAST_BANDIT_SPIDER_CAVE: [
        ExitData(RegionNames.NORTHERN_RYOSHIMA_COAST_BANDIT_SPIDER_ISLAND, one_way=True, has_events=["Northern Ryoshima Coast - Defeat Bandit Spider in cave"])
    ]
}
events = {
    RegionNames.NORTHERN_RYOSHIMA_COAST_BANDIT_SPIDER_CAVE: {
        "Northern Ryoshima Coast - Defeat Bandit Spider in cave": EventData(mandatory_enemies=[OkamiEnemies.BANDIT_SPIDER]),
        #FIXME: Add enemies, requires game progression to appear.
        "Northern Ryoshima Coast - Clear 10 Devil Gates in cave": EventData(
            mandatory_enemies=[]),
    }

}
locations = {
    RegionNames.NORTHERN_RYOSHIMA_COAST_BANDIT_SPIDER_CAVE: {
        "Northern Ryoshima Coast - Chest after Bandit Spider": LocData(container_check_id(MapIds.NORTHERN_RYOSHIMA_BANDIT_SPIDER, 0)),
        "Northern Ryoshima Coast - Chest after 10 devil gates": LocData(container_check_id(MapIds.NORTHERN_RYOSHIMA_BANDIT_SPIDER, 1))
    }
}
