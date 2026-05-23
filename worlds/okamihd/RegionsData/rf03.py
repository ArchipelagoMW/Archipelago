from typing import TYPE_CHECKING

from rule_builder.rules import True_
from ..CheckIds import container_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.RegionNames import RegionNames, MapIds
from ..Enums.WarpType import WarpType
from ..Types import ExitData, LocData, EventData, WarpData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.CURSED_AGATA_FOREST: [ExitData(RegionNames.AGATA_FOREST_WAKA,has_events=["Agata Forest - Restore Guardian Sapling"],one_way=True),
                                      ExitData(RegionNames.FAWNS_HOUSE)],
}
events = {
    RegionNames.CURSED_AGATA_FOREST: {
        "Agata Forest - Restore Guardian Sapling": EventData(
            required_brush_techniques=[BrushTechniques.GREENSPROUT_BLOOM],cherry_bomb_level=1, precollected=lambda o:o.BloomGuardianSaplings)
    },
}
locations = {
    RegionNames.CURSED_AGATA_FOREST:{
        "Agata Forest - Burning Chest near Madame Fawn's 1": LocData(container_check_id(MapIds.HEALED_AGATA, 20),type=LocationType.BURNING_CHEST),
        "Agata Forest - Burning Chest near Madame Fawn's 2": LocData(container_check_id(MapIds.HEALED_AGATA, 21),type=LocationType.BURNING_CHEST),
        "Agata Forest - Burning Chest near Madame Fawn's 3": LocData(container_check_id(MapIds.HEALED_AGATA, 22),type=LocationType.BURNING_CHEST),
        "Agata Forest - Ledge chest near Madame Fawn's ": LocData(container_check_id(MapIds.HEALED_AGATA, 26), required_brush_techniques=[BrushTechniques.WATERSPOUT]),
    },

}
warps = {
    RegionNames.CURSED_AGATA_FOREST:[
        WarpData(type=WarpType.MIST_WARP, trigger_warp_to=True_, trigger_warp_from=True_),
    ]
}
