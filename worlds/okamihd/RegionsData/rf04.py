from typing import TYPE_CHECKING

from BaseClasses import LocationProgressType
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.OkamiEnemies import OkamiEnemies
from ..Enums.RegionNames import RegionNames
from ..Types import ExitData, LocData, EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    # small region to force waka fight to be cleared before acessing the rest of the forest.
    RegionNames.AGATA_FOREST_WAKA: [
        ExitData("Agata Forest Waka cutscene", RegionNames.AGATA_FOREST, has_events=["Agata Forest - Defeat Waka"])],
    RegionNames.AGATA_FOREST: [ExitData("Agata Forest - To Taka Pass", RegionNames.CURSED_TAKA_PASS,
                                        has_events=["Agata Forest - Repair Bridge with Kokari"])
        , ExitData("Agata Ruins - Enter Tsuta Ruins", RegionNames.TSUTA_RUINS_1F_MAIN_PART,
                   has_events=["Agata Forest - Open Ruins Door"])]
}
events = {
    RegionNames.AGATA_FOREST_WAKA: {
        "Agata Forest - Defeat Waka": EventData(mandatory_enemies=[OkamiEnemies.WAKA_1])
    },
    RegionNames.AGATA_FOREST: {
        "Agata Forest - Open Ruins Door": EventData(required_items_events=["Tsuta Ruins Key"]),
        # Probably might be changed to not reuquire beating Tsuta. Or to be open from the start.
        "Agata Forest - Repair Bridge with Kokari": EventData(
            required_brush_techniques=[BrushTechniques.GREENSPROUT_VINE],
            required_items_events=["Tsuta Ruins - Defeat the spider queen"]),
        "Agata Forest - Fill Kushi's Barrel": EventData(required_brush_techniques=[BrushTechniques.WATERSPOUT]),
        "Agata Forest - Fight with Susano": EventData(power_slash_level=1,
                                                      required_items_events=["Agata Forest - Fill Kushi's Barrel"]),
        "Agata Forest - Fish Whopper with Kokari": EventData(power_slash_level=1,
                                                             required_items_events=[
                                                                 "Agata Forest - Fight with Susano"]),
        "Agata Forest - Get Orb from Ume": EventData(id=127, mandatory_enemies=[OkamiEnemies.UME],
                                                     is_event_item=lambda o: o.CanineRewards != 0,
                                                     progress_type=lambda
                                                         o: LocationProgressType.EXCLUDED if o.CanineRewards == 2 else LocationProgressType.DEFAULT,
                                                     event_item_name="Justice Orb",
                                                     required_items_events=["Agata Forest - Fish Whopper with Kokari"])
    }
}
locations = {
    RegionNames.AGATA_FOREST: {
        # the names here could be better.
        "Agata Forest - Treasure Bud near Guardian Sapling Cave": LocData(1884064, type=LocationType.TREASURE_BUD),
        "Agata Forest - Treasure Bud 1": LocData(47, type=LocationType.TREASURE_BUD),
        "Agata Forest - Treasure Bud on big island": LocData(48, type=LocationType.TREASURE_BUD),
        "Agata Forest - Treasure Bud on lone tree island near Kokari": LocData(1884067, type=LocationType.TREASURE_BUD),
        "Agata Forest - Treasure Bud near Karude's house": LocData(1884068, type=LocationType.TREASURE_BUD),
        "Agata Forest - Treasure Bud near Karude's house cursed patch": LocData(1884069, type=LocationType.TREASURE_BUD),
        "Agata Forest - Treasure Bud near waterfall": LocData(1884070, type=LocationType.TREASURE_BUD),
        "Agata Forest - Treasure Bud near Mme. Fawn's Cave": LocData(1884071, type=LocationType.TREASURE_BUD),
        "Agata Forest - Treasure Bud 2": LocData(54, type=LocationType.TREASURE_BUD),
        "Agata Forest - Treasure Bud Inside Tree": LocData(1884081, type=LocationType.TREASURE_BUD),
        "Agata Forest - Chest at Guardian Sapling": LocData(1884082),
        "Agata Forest - Buried chest near shortcut": LocData(1884083, type=LocationType.BURIED_CHEST),
        # Probably needs something more to get on top
        "Agata Forest - Chest on top of the big tree": LocData(1884087, type=LocationType.UNDERWATER_CHEST,
                                                               required_brush_techniques=[
                                                                   BrushTechniques.GREENSPROUT_VINE]),
        "Agata Forest - Freestanding stray Bead": LocData(1884088,
                                                          required_brush_techniques=[BrushTechniques.GREENSPROUT_VINE],
                                                          type=LocationType.FREESTANDING_ITEM),
        "Agata Forest - Freestanding Bull Horn": LocData(1884089,
                                                         required_brush_techniques=[BrushTechniques.GREENSPROUT_VINE],
                                                         type=LocationType.FREESTANDING_ITEM),
        "Agata Forest - Buried Chest on Lake shore": LocData(1884096, type=LocationType.BURIED_CHEST),
        "Agata Forest - Buried Chest behind Karude's house": LocData(1884097, type=LocationType.BURIED_CHEST),
        "Agata Forest - Buried Chest on Island": LocData(1884098, type=LocationType.BURIED_CHEST),
        "Agata Forest - Chest under leaf pile near Shinshu Field entrance": LocData(1884107,
                                                                                    type=LocationType.BURIED_UNDER_LEAF_PILE),
        "Agata Forest - Chest under leaf pile on ledge": LocData(1884108, type=LocationType.BURIED_UNDER_LEAF_PILE),
        "Agata Forest - Chest under leaf pile near river": LocData(1884109, type=LocationType.BURIED_UNDER_LEAF_PILE),
        "Agata Forest - Buried chest near Tsuta Ruins entrance": LocData(1884110, type=LocationType.STONE_BURIED_CHEST),
        "Agata Forest - Chest after Bridge cutscene": LocData(1884111,required_items_events=["Agata Forest - Repair Bridge with Kokari"]),
        "Agata Forest - Chest near Demon Fang merchant": LocData(1884113),
        "Agata Forest - Chest near Tusta ruins door": LocData(1884114),
        "Agata Forest - Fish Giant Salmon with Kokari": LocData(77, power_slash_level=1),
        "Agata Forest - Yumigami": LocData(200018, type=LocationType.CONSTELLATION,  # bit 18
                                           required_items_events=["Agata Forest - Fish Whopper with Kokari"])
    }
}
