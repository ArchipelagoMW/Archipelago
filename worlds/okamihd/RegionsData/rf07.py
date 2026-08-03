from typing import TYPE_CHECKING

from rule_builder.rules import True_, Has
from ..CheckIds import container_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.OkamiEnemies import OkamiEnemies
from ..Enums.RegionNames import RegionNames, MapIds
from ..Enums.WarpType import WarpType
from ..Types import EventData, ExitData, LocData, WarpData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.TAKA_COMMON_LOGIC:[
        ExitData(RegionNames.AGATA_FOREST_TAKA,one_way=True)
    ],
    RegionNames.CURSED_TAKA_PASS: [
        ExitData(RegionNames.CURSED_TAKA_PASS_WAKA, required_items_events=["Taka Pass - Blow up boulder to cave"],
                 loading_screen=False)],
    # Region for mandatory waka encounter
    RegionNames.CURSED_TAKA_PASS_WAKA: [
        ExitData(RegionNames.CURSED_TAKA_PASS_CAVE, required_items_events=["Taka Pass - Rematch with Waka"], loading_screen=False),
        ExitData(RegionNames.TAKA_COMMON_LOGIC, one_way=True, loading_screen=False)
        ],
    RegionNames.CURSED_TAKA_PASS_CAVE: [ExitData(RegionNames.CURSED_TAKA_PASS_GUARDIAN_SAPLING,
                                                 required_items_events=["Taka pass - Restore Bridge to Guardian Sapling"],
                                                 loading_screen=False)],
    RegionNames.CURSED_TAKA_PASS_GUARDIAN_SAPLING: [
        ExitData(RegionNames.TAKA_PASS, required_items_events=["Taka pass - Restore Guardian Sapling"], one_way=True)]
}
events = {
    RegionNames.CURSED_TAKA_PASS: {
        "Taka Pass - Blow up boulder to cave": EventData(cherry_bomb_level=1)
    },
    RegionNames.CURSED_TAKA_PASS_WAKA: {
        "Taka Pass - Rematch with Waka": EventData(mandatory_enemies=[OkamiEnemies.WAKA_2])
    },
    RegionNames.CURSED_TAKA_PASS_CAVE: {
        "Taka pass - Restore Bridge to Guardian Sapling": EventData(
            required_brush_techniques=[BrushTechniques.REJUVENATION])
    },
    RegionNames.CURSED_TAKA_PASS_GUARDIAN_SAPLING: {
        "Taka pass - Restore Guardian Sapling": EventData(
            required_brush_techniques=[BrushTechniques.GREENSPROUT_BLOOM],
            precollected=lambda o: o.BloomGuardianSaplings)
    },
}

locations = {
    RegionNames.TAKA_COMMON_LOGIC: {
        "Taka pass - Stray bead chest in cave pond": LocData(container_check_id(MapIds.HEALED_TAKA, 63),
                                                             type=LocationType.UNDERWATER_CHEST),
        "Taka pass - Burning chest in cave upper": LocData(container_check_id(MapIds.HEALED_TAKA, 15),
                                                           type=LocationType.BURNING_CHEST),
        "Taka pass - Second Burning chest in cave upper": LocData(container_check_id(MapIds.HEALED_TAKA, 9),
                                                                  type=LocationType.BURNING_CHEST_NO_WATER),
    }
}

warps = {
    RegionNames.CURSED_TAKA_PASS: [
        WarpData(type=WarpType.MIST_WARP, trigger_warp_to=Has("Mist Warp Unlock - Cursed Taka Pass"), trigger_warp_from=True_)
    ]
}
