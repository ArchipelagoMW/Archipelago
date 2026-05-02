from typing import TYPE_CHECKING

from ..CheckIds import container_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.OkamiEnemies import OkamiEnemies
from ..Enums.RegionNames import RegionNames, MapIds
from ..Types import EventData, ExitData, LocData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits={
    RegionNames.CURSED_TAKA_PASS:[ExitData("To Taka pass cave",RegionNames.CURSED_TAKA_PASS_WAKA,has_events=["Taka Pass - Blow up boulder to cave"])],
    # Region for mandatory waka encounter
    RegionNames.CURSED_TAKA_PASS_WAKA: [ExitData("Defeat Waka Again",RegionNames.CURSED_TAKA_PASS_CAVE, has_events=["Taka Pass - Rematch with Waka"])],
    RegionNames.CURSED_TAKA_PASS_CAVE : [ExitData("Cross Bridge to Guardian Sapling",RegionNames.CURSED_TAKA_PASS_GUARDIAN_SAPLING,has_events=["Taka pass - Restore Bridge to Guardian Sapling"])],
    RegionNames.CURSED_TAKA_PASS_GUARDIAN_SAPLING: [ExitData("Taka Pass Restoration",RegionNames.TAKA_PASS,has_events=["Taka pass - Restore Guardian Sapling"])]
}
events={
    RegionNames.CURSED_TAKA_PASS:{
        "Taka Pass - Blow up boulder to cave" : EventData(cherry_bomb_level=1)
    },
    RegionNames.CURSED_TAKA_PASS_WAKA:{
        "Taka Pass - Rematch with Waka":EventData(mandatory_enemies=[OkamiEnemies.WAKA_2])
    },
    RegionNames.CURSED_TAKA_PASS_CAVE:{
        "Taka pass - Restore Bridge to Guardian Sapling":EventData(required_brush_techniques=[BrushTechniques.REJUVENATION])
    },
    RegionNames.CURSED_TAKA_PASS_GUARDIAN_SAPLING: {
        "Taka pass - Restore Guardian Sapling": EventData(
            required_brush_techniques=[BrushTechniques.GREENSPROUT_BLOOM],precollected=lambda o:o.BloomGuardianSaplings)
    },
}

locations = {
    RegionNames.CURSED_TAKA_PASS_CAVE:{
        "Taka pass - Stray bead chest in cave pond" : LocData(container_check_id(MapIds.CURSED_TAKA, 63), type=LocationType.UNDERWATER_CHEST),
        "Taka pass - Burning chest in cave upper": LocData(container_check_id(MapIds.CURSED_TAKA, 15), type=LocationType.BURNING_CHEST),
        "Taka pass - Second Burning chest in cave upper": LocData(container_check_id(MapIds.CURSED_TAKA, 9), type=LocationType.BURNING_CHEST_NO_WATER),
    }

}
