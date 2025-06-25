from typing import TYPE_CHECKING
from ..Types import ExitData, LocData, BrushTechniques, RegionNames, EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.CURSED_SHINSHU_FIELD: [ExitData("Cursed Shinshu field - To Cursed Hana Valley", RegionNames.CURSED_HANA_VALLEY),
                                       ExitData("Shinshu field restoration",RegionNames.SHINSHU_FIELD,has_events=["Shinshu Field - Restore Guardian Sapling"])],

}
events = {
    RegionNames.CURSED_SHINSHU_FIELD: {
        "Shinshu Field - Restore Guardian Sapling": EventData(
            required_brush_techniques=[BrushTechniques.GREENSPROUT_BLOOM])
    },
}
locations = {
}
