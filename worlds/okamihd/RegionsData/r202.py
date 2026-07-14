from typing import TYPE_CHECKING

from BaseClasses import LocationProgressType
from ..CheckIds import container_check_id, brush_check_id, shop_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.RegionNames import RegionNames, MapIds
from ..Types import ExitData, LocData, EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.HIMIKO_PALACE:[
        ExitData(RegionNames.HIMIKO_CHAMBERS,required_items_events=["Himiko's Palace - Cross sea of fire"],loading_screen=False)
    ]
}
events = {
    RegionNames.HIMIKO_PALACE: {
        "Himiko's Palace - Cross sea of fire": EventData(required_items_events=["Fire Tablet"])
    },
    RegionNames.HIMIKO_CHAMBERS: {
        # Vanilla event that opens N. Ryoshima Coast - to replace with something else when needed.
        "Himiko's Palace - Hear Himiko's request": EventData(),
        "Himiko's Palace - Get Oni Island Location": EventData(
            required_items_events=["Dragon Palace - Give Dragon Orb to Otohime",
                                   "Ryoshima Coast - Open shortcut to Sei-an City"])
    }
}
locations = {
    RegionNames.HIMIKO_PALACE: {
        "Himiko's Palace - Chest behind elevator": LocData(container_check_id(MapIds.HIMIKO_PALACE, 0)),
        # Only spawns if you have Fire tablet
        "Himiko's Palace - Freestanding item before sea of Fire": LocData(container_check_id(MapIds.HIMIKO_PALACE, 1),
                                                                          required_items_events=["Fire Tablet"])
    },
    # Special check
    RegionNames.HIMIKO_CHAMBERS: {
        "Himiko's Palace - Get Border Key from Queen Himiko": LocData(1000, progress_type=LocationProgressType.EXCLUDED)
    }
}
