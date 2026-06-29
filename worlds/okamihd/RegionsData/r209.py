from typing import TYPE_CHECKING

from BaseClasses import LocationProgressType
from rule_builder.rules import HasAny
from ..CheckIds import container_check_id, brush_check_id, shop_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.OkamiEnemies import OkamiEnemies
from ..Enums.RegionNames import RegionNames, MapIds
from ..Rules import oni_island_1f_thunder_rule, oni_island_5f_thunder_rule
from ..Types import ExitData, LocData, EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
}
events = {
    RegionNames.ONI_ISLAND_NINETAILS: {
        "Oni Island - Defeat Ninetails": EventData(mandatory_enemies=[OkamiEnemies.NINETAILS_1])
    }
}

locations = {
    RegionNames.ONI_ISLAND_NINETAILS: {
        "Oni Island - Ninetails reward": LocData(1010, required_items_events=["Oni Island - Defeat Ninetails"],
                                                 progress_type=LocationProgressType.EXCLUDED)
    }
}
