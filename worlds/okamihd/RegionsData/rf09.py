from typing import TYPE_CHECKING

from rule_builder.rules import True_
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.WarpType import WarpType
from ..Types import ExitData, EventData, LocData, WarpData
from ..Enums.RegionNames import RegionNames

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.CURSED_RYOSHIMA_COAST: [
        ExitData(RegionNames.CURSED_RYOSHIMA_COAST_GUARDIAN_SAPLING_CAVE,
                 has_events=["Ryoshima Coast - Open Guardian Sapling Cave"], loading_screen=False)
    ],
    RegionNames.CURSED_RYOSHIMA_COAST_GUARDIAN_SAPLING_CAVE: [
        ExitData(RegionNames.RYOSHIMA_COAST, has_events=["Ryoshima Coast - Bloom the Guardian Sapling"], one_way=True)
    ]
}
events = {
    RegionNames.CURSED_RYOSHIMA_COAST: {
        "Ryoshima Coast - Open Guardian Sapling Cave": EventData(cherry_bomb_level=1)
    },
    RegionNames.CURSED_RYOSHIMA_COAST_GUARDIAN_SAPLING_CAVE: {
        "Ryoshima Coast - Water the Guardian Sapling": EventData(
            required_brush_techniques=[BrushTechniques.WATERSPOUT]),
        "Ryoshima Coast - Bloom the Guardian Sapling": EventData(
            required_brush_techniques=[BrushTechniques.GREENSPROUT_BLOOM],
            required_items_events=["Ryoshima Coast - Water the Guardian Sapling"])
    }
}
locations = {
}
warps = {
    RegionNames.CURSED_RYOSHIMA_COAST: [
        WarpData(type=WarpType.MIST_WARP, trigger_warp_to=True_, trigger_warp_from=True_)
    ]
}
