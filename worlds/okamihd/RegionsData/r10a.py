from typing import TYPE_CHECKING

from ..CheckIds import container_check_id
from ..Types import LocData
from ..Enums.RegionNames import RegionNames, MapIds

if TYPE_CHECKING:
   from .. import OkamiWorld

exits = {
}
events = {
}
locations = {
    RegionNames.FAWNS_HOUSE: {
        "Agata Forest - Stray Bead in Madame Fawn's": LocData(container_check_id(MapIds.AGATA_FOREST_MME_FAWN, 0))
    }
}
