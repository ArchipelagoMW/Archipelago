from typing import TYPE_CHECKING
from ..Types import ExitData, LocData, BrushTechniques, RegionNames, EventData, OkamiEnnemies

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.STONE_KAMIKI: [ExitData("Restore the villagers", RegionNames.KAMIKI_VILLAGE,
                                        has_events=["Kamiki Village - Fight with Mr.Orange"])],
    RegionNames.KAMIKI_VILLAGE: [ExitData("Swim to Kamiki Islands", RegionNames.KAMIKI_ISLANDS, needs_swim=True),
                                 ExitData("Enter Susano's House",RegionNames.SUSANOS_HOUSE),
                                 ExitData("Enter Kushi's House",RegionNames.KUSHIS_HOUSE),
                                 ExitData("Enter Oranges' House",RegionNames.ORANGES_HOUSE),
                                 ExitData("Exit Village to Cursed Shinshu field",RegionNames.CURSED_SHINSHU_FIELD,has_events=["Kamiki Village - Help Susano Train/Break the boulder"])],
    RegionNames.SUSANOS_HOUSE: [ExitData("Enter meditation Chamber",RegionNames.SUSANOS_UNDERGROUD)]
}
events = {
    RegionNames.STONE_KAMIKI: {
        "Kamiki Village - Restoring the villagers": EventData(required_brush_techniques=[BrushTechniques.SUNRISE],id=0x203,precollected=lambda o:o.OpenGameStart),
        "Kamiki Village - Fight with Mr.Orange": EventData(mandatory_enemies=[OkamiEnnemies.GREEN_IMP], id=0x208,
                                                              precollected=lambda o: o.OpenGameStart,required_items_events=["Kamiki Village - Restoring the villagers"])

    },
    RegionNames.SUSANOS_UNDERGROUD:{
        "Kamiki Village - Wake up Susano": EventData(required_items_events=["Kamiki Village - Save the merchant"],id=0x204,precollected=lambda o:o.OpenGameStart)
    },
    RegionNames.KAMIKI_VILLAGE: {
        "Kamiki Village - Repair Kushi's Watermill": EventData(required_brush_techniques=[BrushTechniques.REJUVENATION],required_items_events=["Kamiki Village - Wake up Susano"],id=0x205,precollected=lambda o:o.OpenGameStart),
        "Kamiki Village - Save the merchant": EventData(mandatory_enemies=[OkamiEnnemies.GREEN_IMP, OkamiEnnemies.RED_IMP],id=0x206,precollected=lambda o:o.OpenGameStart),
        "Kamiki Village - Help Susano Train/Break the boulder":EventData (power_slash_level=1,required_items_events=["Vista of the Gods","Kamiki Village - Wake up Susano"],id=0x207,precollected=lambda o:o.OpenGameStart),
        "Kamiki Village - Bloom every Tree":EventData(required_brush_techniques=[BrushTechniques.GREENSPROUT_BLOOM]),
        "Kamiki Village - Restore Sakuya's Tree": EventData(required_items_events=["Kamiki Village - Bloom every Tree"],required_brush_techniques=[BrushTechniques.GREENSPROUT_BLOOM])
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
        "Kamiki Village - Underwater Chest 1" :LocData(13, power_slash_level=1),
        "Kamiki Village - Underwater Chest 2" :LocData(14, power_slash_level=1),
        "Kamiki Village - Underwater chest in lake near Kushi's house": LocData(21,power_slash_level=1),
        "Kamiki Village - Hasugami" : LocData(16,required_items_events=["Kamiki Village - Restore Sakuya's Tree"]),
        "Kamiki Village - Buried chest in field": LocData(19,buried=1),
        "Kamiki Village - Chest on Ledge":LocData(22, required_brush_techniques=[BrushTechniques.GREENSPROUT_VINE]),
        "Kamiki Village - Rafters Lower Chest" :LocData(75),
        "Kamiki Village - Rafters Upper Chest" :LocData(76, power_slash_level=1)
    },
    RegionNames.ORANGES_HOUSE:{
        "Kamiki Village - Chest buried in Oranges' house": LocData(45,buried=1)
    },
    RegionNames.KUSHIS_HOUSE:{
        "Kamiki Village - Kushi's Gift": LocData(11, required_items_events=["Kamiki Village - Repair Kushi's Watermill"]),
    },
    RegionNames.KAMIKI_ISLANDS: {
        "Kamiki Village - West Island chest ": LocData(9),
        "Kamiki Village - West Island buried chest": LocData(10, buried=1),
        # Waterlily tutorial,
        "Kamiki Village - East Islands Sun fragment chest": LocData(18),
        "Kamiki Village - East Islands Stray Bead Chest": LocData(44),
        "Kamiki Village - East Islands Buried Chest": LocData(20, buried=1),
    }
}
