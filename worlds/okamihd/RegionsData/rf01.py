from typing import TYPE_CHECKING

from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.RegionNames import RegionNames
from ..Types import ExitData, LocData, EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.CURSED_SHINSHU_FIELD: [ExitData(RegionNames.CURSED_HANA_VALLEY),
                                       ExitData(RegionNames.HANA_VALLEY,has_events=["Hana Valley - Guardian Sapling Restoration"]),
                                       ExitData(RegionNames.SHINSHU_FIELD,has_events=["Shinshu Field - Restore Guardian Sapling"])],

}
events = {
    RegionNames.CURSED_SHINSHU_FIELD: {
        "Shinshu Field - Restore Guardian Sapling": EventData(
            required_brush_techniques=[BrushTechniques.GREENSPROUT_BLOOM],precollected=lambda o:o.BloomGuardianSaplings)
    },
}
locations = {
}

