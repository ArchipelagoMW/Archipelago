from typing import TYPE_CHECKING

from ..CheckIds import container_check_id, brush_check_id, shop_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.RegionNames import RegionNames, MapIds
from ..Types import ExitData, LocData, EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {

}
events = {
    RegionNames.IMPERIAL_PALACE_ENTRANCE:{
        # The purpose of this event is to add this item to the pool, since it doesn't have an id...for now.
        "Imperial Palace - Prayer Slips":EventData(event_item_name="Prayer Slips"),
        # biteable items check - Can we access their vanilla spanw point ?
        "Imperial Palace - Grab Prayer Slips":EventData(required_items_events=["Prayer Slips"])
    }

}
locations = {

}
