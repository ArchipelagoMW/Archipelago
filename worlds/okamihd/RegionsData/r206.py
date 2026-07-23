from typing import TYPE_CHECKING

from ..CheckIds import container_check_id
from ..Enums.LocationType import LocationType
from ..Enums.RegionNames import RegionNames, MapIds
from ..Types import ExitData, LocData, EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.IMPERIAL_PALACE_ENTRANCE: [
        ExitData(RegionNames.IMPERIAL_PALACE_SMALL_ENTRANCE, required_items_events=["Imperial Palace - Become Smol"]),
        ExitData(RegionNames.IMPERIAL_PALACE, required_items_events=["Imperial Palace - Defeat Blight"])
    ],

}
events = {
    RegionNames.IMPERIAL_PALACE_ENTRANCE: {
        # The purpose of this event is to add this item to the pool, since it doesn't have an id...for now.
        "Imperial Palace - Prayer Slips": EventData(event_item_name="Prayer Slips"),
        # biteable items check - Can we access their vanilla spawn point ?
        "Imperial Palace - Grab Prayer Slips": EventData(required_items_events=["Prayer Slips"]),
        "Imperial Palace - Become Smol": EventData(required_items_events=["Sunken Ship - Get Chased by water Dragon"]),
    }

}
locations = {
    RegionNames.IMPERIAL_PALACE: {
        "Imperial Palace - Chest near the Emperor": LocData(container_check_id(MapIds.IMPERIAL_PALACE, 6)),
        "Imperial Palace - Buried chest 1": LocData(
            container_check_id(MapIds.IMPERIAL_PALACE, 4), type=LocationType.BURIED_CHEST),
        "Imperial Palace - Buried chest 2": LocData(
            container_check_id(MapIds.IMPERIAL_PALACE, 1), type=LocationType.BURIED_CHEST),
        "Imperial Palace - Buried chest 3": LocData(
            container_check_id(MapIds.IMPERIAL_PALACE, 2), type=LocationType.BURIED_CHEST),
        "Imperial Palace - Buried chest 4": LocData(
            container_check_id(MapIds.IMPERIAL_PALACE, 5), type=LocationType.BURIED_CHEST),
        "Imperial Palace - Buried chest 5": LocData(
            container_check_id(MapIds.IMPERIAL_PALACE, 3), type=LocationType.BURIED_CHEST),
        # FIXME: Chest not randomized for now; It only spawns when you buy mist warp. which you can't do if you already have it/
        #"Imperial Palace - chest after buying Mist warp": LocData(container_check_id(MapIds.IMPERIAL_PALACE, 0)),

    }
}
