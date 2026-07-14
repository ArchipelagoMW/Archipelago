from typing import TYPE_CHECKING

from rule_builder.rules import Has
from ..CheckIds import container_check_id, brush_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.WarpType import WarpType
from ..Types import LocData, ExitData, WarpData, EventData
from ..Enums.RegionNames import RegionNames, MapIds

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
}
events = {

}
locations = {
    RegionNames.SEIN_CITY_KIMONO:{
        "Sei-an City (Commoner's Quarter) - Buried chest in kimono shop" :LocData(container_check_id(MapIds.SEIAN_KIMONO,0))
    }

}

