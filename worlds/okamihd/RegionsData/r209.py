from typing import TYPE_CHECKING

from BaseClasses import LocationProgressType
from ..Enums.OkamiEnemies import OkamiEnemies
from ..Enums.RegionNames import RegionNames
from ..Types import LocData, EventData

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
