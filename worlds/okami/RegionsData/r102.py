from typing import TYPE_CHECKING
from ..Types import ExitData, LocData, BrushTechniques, RegionNames, EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.STONE_KAMIKI: [ExitData("Kamiki Village (stone) Torii", RegionNames.RIVER_OF_THE_HEAVENS_KAMIKI),
                               ExitData("Restore the villagers", RegionNames.KAMIKI_VILLAGE,
                                        has_events=["Kamiki Village - Restoring the villagers"])],
    RegionNames.KAMIKI_VILLAGE: [ExitData("Kamiki Village Torii", RegionNames.RIVER_OF_THE_HEAVENS_KAMIKI),
                                 ExitData("Swim to Kamiki Islands", RegionNames.KAMIKI_ISLANDS, needs_swim=True)],
    RegionNames.KAMIKI_ISLANDS: [ExitData("Swim to Kamiki Village", RegionNames.KAMIKI_VILLAGE, needs_swim=True)],
}
events = {
    RegionNames.STONE_KAMIKI: {
        "Kamiki Village - Restoring the villagers": EventData(required_brush_techniques=[BrushTechniques.SUNRISE])
    },
    RegionNames.KAMIKI_ISLANDS: {
        "End for now": EventData(required_brush_techniques=[BrushTechniques.CRESCENT,BrushTechniques.REJUVENATION,BrushTechniques.SUNRISE],power_slash_level=1)
    }
}
locations = {
    RegionNames.STONE_KAMIKI: {
        "Kamiki Village - Sunrise": LocData(6),
    },
    RegionNames.KAMIKI_VILLAGE: {
        "Kamiki Village - Chest After Mr.Orange Yokai Fight": LocData(7),
        "Kamiki Village - Buried Chest near Komuso": LocData(8, buried_chest=1),
    },
    RegionNames.KAMIKI_ISLANDS: {
        "Kamiki Village - Island Chest 1": LocData(9),
        "Kamiki Village - Island buried Chest 1": LocData(10, buried_chest=1),
    }
}
