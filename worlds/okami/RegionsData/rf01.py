from typing import TYPE_CHECKING
from ..Types import ExitData, LocData, BrushTechniques, RegionNames, EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.CURSED_SHINSHU_FIELD: [ExitData("To Cursed Hana Valley", RegionNames.CURSED_HANA_VALLEY,
                                                doesnt_have_events=["Hana Valley - Guardian Sapling Restoration"]),
                                       ExitData("To Hana Valley", RegionNames.HANA_VALLEY,
                                                has_events=["Hana Valley - Guardian Sapling Restoration"])]
}
events = {
    RegionNames.CURSED_SHINSHU_FIELD:{
        "Shinshu Field - Restore Guardian Sapling": EventData(required_brush_techniques=[BrushTechniques.GREENSPROUT_BLOOM])
    }
}
locations = {
}
