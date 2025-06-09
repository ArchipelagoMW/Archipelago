from typing import TYPE_CHECKING
from ..Types import ExitData, LocData, BrushTechniques, RegionNames, EventData, OkamiEnnemies

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.STONE_KAMIKI: [ExitData("Kamiki Village (stone) Torii", RegionNames.RIVER_OF_THE_HEAVENS_KAMIKI),
                               ExitData("Restore the villagers", RegionNames.KAMIKI_VILLAGE,
                                        has_events=["Kamiki Village - Restoring the villagers"])],
    RegionNames.KAMIKI_VILLAGE: [ExitData("Kamiki Village Torii", RegionNames.RIVER_OF_THE_HEAVENS_KAMIKI),
                                 ExitData("Swim to Kamiki Islands", RegionNames.KAMIKI_ISLANDS, needs_swim=True),
                                 ExitData("Enter Susano's House",RegionNames.SUSANOS_HOUSE),
                                 ExitData("Enter Kushi's House",RegionNames.KUSHIS_HOUSE),
                                 ExitData("Exit Village to Cursed Shinsu field",RegionNames.CURSED_SHINSHU_FIELD,has_events=["Kamiki Village - Break the Big Boulder"])],
    RegionNames.SUSANOS_HOUSE: [ExitData("Exit Susano's House",RegionNames.KAMIKI_VILLAGE),
                                ExitData("Enter meditation Chamber",RegionNames.SUSANOS_UNDERGROUD)],
    RegionNames.SUSANOS_UNDERGROUD:[ExitData("Exit meditation Chamber",RegionNames.SUSANOS_HOUSE)],
    RegionNames.KAMIKI_ISLANDS: [ExitData("Swim to Kamiki Village", RegionNames.KAMIKI_VILLAGE, needs_swim=True)],
}
events = {
    RegionNames.STONE_KAMIKI: {
        "Kamiki Village - Restoring the villagers": EventData(required_brush_techniques=[BrushTechniques.SUNRISE],mandatory_enemies=[OkamiEnnemies.GREEN_IMP])
    },
    RegionNames.SUSANOS_UNDERGROUD:{
        "Kamiki Village - Wake up Susano": EventData(has_events=["Kamiki Village - Save the merchant"])
    },
    RegionNames.KAMIKI_VILLAGE: {
        "Kamiki Village - Repair Kushi's Watermill": EventData(required_brush_techniques=[BrushTechniques.REJUVENATION]),
        "Kamiki Village - Save the merchant": EventData(mandatory_enemies=[OkamiEnnemies.GREEN_IMP, OkamiEnnemies.RED_IMP]),
        "Kamiki Village - Help Susano Train":EventData (power_slash_level=1,required_items=["Kushi's Sake"],has_events=["Kamiki Village - Wake up Susano"]),
        "Kamiki Village - Break the Big Boulder":EventData(power_slash_level=1,has_events=["Kamiki Village - Help Susano Train"]),
    },
    RegionNames.KAMIKI_ISLANDS: {
        "End for now": EventData(required_brush_techniques=[BrushTechniques.CRESCENT,BrushTechniques.REJUVENATION,BrushTechniques.SUNRISE,BrushTechniques.GREENSPROUT_BLOOM],power_slash_level=1)
    }
}
locations = {
    RegionNames.STONE_KAMIKI: {
        "Kamiki Village - Sunrise": LocData(6),
    },
    RegionNames.KAMIKI_VILLAGE: {
        "Kamiki Village - Chest After Mr.Orange Yokai Fight": LocData(7),
        "Kamiki Village - Buried Chest near Komuso": LocData(8, buried=1),
        "Kamiki Village - Kushi's Gift":LocData(11, has_events=["Kamiki Village - Repair Kushi's Watermill"]),
        "Kamiki Village - Underwater Chest 1" :LocData(13, power_slash_level=1),
        "Kamiki Village - Underwater Chest 2" :LocData(14, power_slash_level=1)
    },
    RegionNames.KAMIKI_ISLANDS: {
        "Kamiki Village - Island Chest 1": LocData(9),
        "Kamiki Village - Island buried Chest 1": LocData(10, buried=1),
    }
}
