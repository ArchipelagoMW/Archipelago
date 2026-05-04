from typing import TYPE_CHECKING

from BaseClasses import LocationProgressType
from ..CheckIds import brush_check_id, container_check_id, shop_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.OkamiEnemies import OkamiEnemies
from ..Enums.RegionNames import RegionNames, MapIds
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
        "Agata Forest - Treasure Bud near big rocks": LocData(container_check_id(MapIds.HEALED_AGATA, 0), type=LocationType.TREASURE_BUD),
        "Agata Forest - Treasure Bud on lone tree island next to big rocks": LocData(container_check_id(MapIds.HEALED_AGATA, 1), type=LocationType.TREASURE_BUD),
        "Agata Forest - Treasure Bud near big rocks 2": LocData(container_check_id(MapIds.HEALED_AGATA, 2), type=LocationType.TREASURE_BUD),
        "Agata Forest - Treasure Bud on lone tree island near Kokari": LocData(container_check_id(MapIds.HEALED_AGATA, 3), type=LocationType.TREASURE_BUD),
        "Agata Forest - Treasure Bud near Karude's house": LocData(container_check_id(MapIds.HEALED_AGATA, 4), type=LocationType.TREASURE_BUD),
        "Agata Forest - Treasure Bud near Karude's house cursed patch": LocData(container_check_id(MapIds.HEALED_AGATA, 5), type=LocationType.TREASURE_BUD),
        "Agata Forest - Treasure Bud near waterfall": LocData(container_check_id(MapIds.HEALED_AGATA, 6), type=LocationType.TREASURE_BUD),
        "Agata Forest - Treasure Bud near Mme. Fawn's Cave": LocData(container_check_id(MapIds.HEALED_AGATA, 7), type=LocationType.TREASURE_BUD),
        "Agata Forest - Treasure Bud on center lone tree island": LocData(container_check_id(MapIds.HEALED_AGATA, 8), type=LocationType.TREASURE_BUD),
        "Agata Forest - Treasure Bud inside tree at Hitoshio Spring": LocData(container_check_id(MapIds.HEALED_AGATA, 17), type=LocationType.TREASURE_BUD,required_brush_techniques=[BrushTechniques.GREENSPROUT_BLOOM]),
        "Agata Forest - Chest at Guardian Sapling": LocData(container_check_id(MapIds.HEALED_AGATA, 18)),
        "Agata Forest - Buried chest on ledge near Tsuta Ruins Entrance": LocData(container_check_id(MapIds.HEALED_AGATA, 19), type=LocationType.BURIED_CHEST),

        "Agata Forest - Chest on top of the big tree at Hitoshio Spring": LocData(container_check_id(MapIds.HEALED_AGATA, 23), type=LocationType.UNDERWATER_CHEST,
                                                               required_brush_techniques=[
                                                                   BrushTechniques.GREENSPROUT_VINE]),
        "Agata Forest - Freestanding stray Bead": LocData(container_check_id(MapIds.HEALED_AGATA, 24),
                                                          required_brush_techniques=[BrushTechniques.GREENSPROUT_VINE],
                                                          type=LocationType.FREESTANDING_ITEM),
        "Agata Forest - Freestanding Bull Horn": LocData(container_check_id(MapIds.HEALED_AGATA, 25),
                                                         required_brush_techniques=[BrushTechniques.GREENSPROUT_VINE],
                                                         type=LocationType.FREESTANDING_ITEM),
        "Agata Forest - Buried Chest on Lake shore": LocData(container_check_id(MapIds.HEALED_AGATA, 32), type=LocationType.BURIED_CHEST),
        "Agata Forest - Buried Chest behind Karude's house": LocData(container_check_id(MapIds.HEALED_AGATA, 33), type=LocationType.BURIED_CHEST),
        "Agata Forest - Buried Chest on center lone tree island": LocData(container_check_id(MapIds.HEALED_AGATA, 34), type=LocationType.BURIED_CHEST),
        "Agata Forest - Chest under leaf pile near Shinshu Field entrance": LocData(container_check_id(MapIds.HEALED_AGATA, 43),
                                                                                    type=LocationType.BURIED_UNDER_LEAF_PILE),
        "Agata Forest - Buried Chest under leaf pile near shortcut": LocData(container_check_id(MapIds.HEALED_AGATA, 44), type=LocationType.BURIED_UNDER_LEAF_PILE),
        "Agata Forest - Chest under leaf pile near river": LocData(container_check_id(MapIds.HEALED_AGATA, 45), type=LocationType.BURIED_UNDER_LEAF_PILE),
        "Agata Forest - Buried chest near Tsuta Ruins entrance": LocData(container_check_id(MapIds.HEALED_AGATA, 46), type=LocationType.STONE_BURIED_CHEST),
        "Agata Forest - Chest after Bridge cutscene": LocData(container_check_id(MapIds.HEALED_AGATA, 47),required_items_events=["Agata Forest - Repair Bridge with Kokari"]),
        "Agata Forest - Chest near Kiba": LocData(container_check_id(MapIds.HEALED_AGATA, 49)),
        "Agata Forest - Chest near Tusta ruins door": LocData(container_check_id(MapIds.HEALED_AGATA, 50)),
        ## Special check
        "Agata Forest - Fish Giant Salmon with Kokari": LocData(77, power_slash_level=1),
        "Agata Forest - Yumigami": LocData(brush_check_id(18), type=LocationType.CONSTELLATION,  # bit 18
                                           required_items_events=["Agata Forest - Fish Whopper with Kokari"])
    }
}

shop_locations = {
    RegionNames.AGATA_FOREST: {
        "Agata Forest - Shop Slot 1": LocData(shop_check_id(0, 0), type=LocationType.SHOP),
        "Agata Forest - Shop Slot 2": LocData(shop_check_id(0, 1), type=LocationType.SHOP),
        "Agata Forest - Shop Slot 3": LocData(shop_check_id(0, 2), type=LocationType.SHOP),
        "Agata Forest - Shop Slot 4": LocData(shop_check_id(0, 3), type=LocationType.SHOP),
        "Agata Forest - Shop Slot 5": LocData(shop_check_id(0, 4), type=LocationType.SHOP),
        "Agata Forest - Shop Slot 6": LocData(shop_check_id(0, 5), type=LocationType.SHOP),
        "Agata Forest - Shop Slot 7": LocData(shop_check_id(0, 6), type=LocationType.SHOP),
        "Agata Forest - Shop Slot 8": LocData(shop_check_id(0, 7), type=LocationType.SHOP),
        "Agata Forest - Shop Slot 9": LocData(shop_check_id(0, 8), type=LocationType.SHOP),
        "Agata Forest - Shop Slot 10": LocData(shop_check_id(0, 9), type=LocationType.SHOP),
        "Agata Forest - Shop Slot 11": LocData(shop_check_id(0, 10), type=LocationType.SHOP),
        "Agata Forest - Shop Slot 12": LocData(shop_check_id(0, 11), type=LocationType.SHOP),
    }
}