from typing import TYPE_CHECKING

from BaseClasses import LocationProgressType
from ..CheckIds import brush_check_id, collected_object_check_id, container_check_id, shop_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.OkamiEnemies import OkamiEnemies
from ..Enums.RegionNames import RegionNames, MapIds, MapIndexes
from ..Rules import night_time_check_rule
from ..Types import ExitData, LocData, EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.STONE_KAMIKI: [
        ExitData(RegionNames.KAMIKI_VILLAGE, has_events=["Kamiki Village - Fight with Mr.Orange"], one_way=True)],
    RegionNames.KAMIKI_VILLAGE: [ExitData(RegionNames.KAMIKI_ISLANDS, needs_long_swim=True, loading_screen=False),
                                 ExitData(RegionNames.SUSANOS_HOUSE),
                                 ExitData(RegionNames.KUSHIS_HOUSE),
                                 ExitData(RegionNames.ORANGES_HOUSE),
                                 ExitData(RegionNames.CURSED_SHINSHU_FIELD,
                                          has_events=["Kamiki Village - Help Susano Train/Break the boulder"]),
                                 # One way bc this is not a logical access.
                                 ExitData(RegionNames.KAMIKI_MERCHANT,
                                          has_events=["Kamiki Village - Help Susano Train/Break the boulder"],
                                          one_way=True, loading_screen=False)],
    RegionNames.SUSANOS_HOUSE: [ExitData(RegionNames.SUSANOS_UNDERGROUD)]
}
events = {
    RegionNames.STONE_KAMIKI: {
        "Kamiki Village - Restoring the villagers": EventData(required_brush_techniques=[BrushTechniques.SUNRISE],
                                                              id=0x203, precollected=lambda o: o.OpenGameStart),
        "Kamiki Village - Fight with Mr.Orange": EventData(mandatory_enemies=[OkamiEnemies.GREEN_IMP], id=0x208,
                                                           precollected=lambda o: o.OpenGameStart,
                                                           required_items_events=[
                                                               "Kamiki Village - Restoring the villagers"]),
        "Kamiki Village - Get Orb from Hayabusa": EventData(id=145, mandatory_enemies=[OkamiEnemies.HAYABUSA],
                                                            is_event_item=lambda o: o.CanineRewards != 0,
                                                            progress_type=lambda
                                                                o: LocationProgressType.EXCLUDED if o.CanineRewards == 2
                                                            else LocationProgressType.DEFAULT,
                                                            event_item_name="Loyalty Orb",
                                                            special_rule=night_time_check_rule)

    },
    RegionNames.SUSANOS_UNDERGROUD: {
        "Kamiki Village - Wake up Susano": EventData(required_items_events=["Kamiki Village - Save the merchant"],
                                                     id=0x204, precollected=lambda o: o.OpenGameStart)
    },
    RegionNames.KAMIKI_VILLAGE: {
        "Kamiki Village - Repair Kushi's Watermill": EventData(required_brush_techniques=[BrushTechniques.REJUVENATION],
                                                               required_items_events=[
                                                                   "Kamiki Village - Wake up Susano"], id=0x205,
                                                               precollected=lambda o: o.OpenGameStart),
        "Kamiki Village - Save the merchant": EventData(
            mandatory_enemies=[OkamiEnemies.GREEN_IMP, OkamiEnemies.RED_IMP], id=0x206,
            precollected=lambda o: o.OpenGameStart),
        "Kamiki Village - Help Susano Train/Break the boulder": EventData(power_slash_level=1,
                                                                          required_items_events=["Vista of the Gods",
                                                                                                 "Kamiki Village - Wake up Susano"],
                                                                          id=0x207,
                                                                          precollected=lambda o: o.OpenGameStart),
        "Kamiki Village - Bloom every Tree": EventData(required_brush_techniques=[BrushTechniques.GREENSPROUT_BLOOM]),
        "Kamiki Village - Restore Sakuya's Tree": EventData(required_items_events=["Kamiki Village - Bloom every Tree"],
                                                            required_brush_techniques=[
                                                                BrushTechniques.GREENSPROUT_BLOOM])
    }
}
locations = {
    RegionNames.STONE_KAMIKI: {
        "Kamiki Village - Sunrise": LocData(brush_check_id(27), type=LocationType.CONSTELLATION),
        # Brush acquisition (bit 27)
    },
    RegionNames.KAMIKI_VILLAGE: {
        "Kamiki Village - Chest After Mr.Orange Yokai Fight": LocData(container_check_id(MapIds.KAMIKI_VILLAGE, 87)),
        # spawn_idx=87, Feedbag(Seeds)
        "Kamiki Village - Buried Chest near Komuso": LocData(container_check_id(MapIds.KAMIKI_VILLAGE, 0),
                                                             type=LocationType.BURIED_CHEST),
        # spawn_idx=0, Traveler's Charm
        "Kamiki Village - Underwater Chest 1": LocData(container_check_id(MapIds.KAMIKI_VILLAGE, 16),
                                                       type=LocationType.UNDERWATER_CHEST_SHALLOW),
        # spawn_idx=16, Rabbit Statue
        "Kamiki Village - Underwater Chest 2": LocData(container_check_id(MapIds.KAMIKI_VILLAGE, 33),
                                                       type=LocationType.UNDERWATER_CHEST_SHALLOW),
        # spawn_idx=33, Glass Beads
        "Kamiki Village - Underwater chest in lake near Kushi's house": LocData(
            container_check_id(MapIds.KAMIKI_VILLAGE, 32), type=LocationType.UNDERWATER_CHEST),  # spawn_idx=32, Vase
        "Kamiki Village - Hasugami": LocData(brush_check_id(5),
                                             required_items_events=["Kamiki Village - Restore Sakuya's Tree"],
                                             type=LocationType.CONSTELLATION),  # Brush acquisition (Waterlily)
        "Kamiki Village - Buried chest in field": LocData(container_check_id(MapIds.KAMIKI_VILLAGE, 13),
                                                          type=LocationType.BURIED_CHEST),
        # spawn_idx=13, Dragonfly Bead
        "Kamiki Village - Chest on Ledge": LocData(container_check_id(MapIds.KAMIKI_VILLAGE, 9),
                                                   required_brush_techniques=[BrushTechniques.GREENSPROUT_VINE]),
        # spawn_idx=9, Exorcism Slip S
        "Kamiki Village - Rafters Lower Chest": LocData(container_check_id(MapIds.KAMIKI_VILLAGE, 11)),
        # spawn_idx=11, Stray Bead
        "Kamiki Village - Rafters Upper Chest": LocData(container_check_id(MapIds.KAMIKI_VILLAGE, 10),
                                                        power_slash_level=1),  # spawn_idx=10, Glass Beads,
        # West Island doesn't require long swim
        "Kamiki Village - West Island chest ": LocData(container_check_id(MapIds.KAMIKI_VILLAGE, 48)),
        # spawn_idx=48, Dragonfly Bead
        "Kamiki Village - West Island buried chest": LocData(container_check_id(MapIds.KAMIKI_VILLAGE, 54),
                                                             type=LocationType.BURIED_CHEST),
        # spawn_idx=54, Wooden Bear
        "Kamiki Village - Vine Chest by Waterfall": LocData(container_check_id(MapIds.KAMIKI_VILLAGE, 50),
                                                            required_brush_techniques=[
                                                                BrushTechniques.GREENSPROUT_VINE])
    },
    RegionNames.ORANGES_HOUSE: {
        "Kamiki Village - Chest buried in Oranges' house": LocData(container_check_id(MapIds.KAMIKI_VILLAGE, 19),
                                                                   type=LocationType.BURIED_CHEST),
        # spawn_idx=19, Coral Fragment
    },
    RegionNames.KUSHIS_HOUSE: {
        # Kushi's Gift is not a container - it's an event/NPC reward. Keep old ID for now.
        "Kamiki Village - Kushi's Gift": LocData(collected_object_check_id(MapIndexes.KAMIKI_VILLAGE, 11),
                                                 # mapId=3 (KamikiVillage enum index)
                                                 required_items_events=["Kamiki Village - Repair Kushi's Watermill"]),
    },
    RegionNames.KAMIKI_ISLANDS: {
        "Kamiki Village - East Islands Sun fragment chest": LocData(container_check_id(MapIds.KAMIKI_VILLAGE, 42)),
        # spawn_idx=42, Sun Fragment
        "Kamiki Village - East Islands Right Buried Chest": LocData(container_check_id(MapIds.KAMIKI_VILLAGE, 7),
                                                                    type=LocationType.BURIED_CHEST),
        # spawn_idx=7, Inkfinity Stone
        "Kamiki Village - East Islands Left Buried Chest": LocData(container_check_id(MapIds.KAMIKI_VILLAGE, 8),
                                                                   type=LocationType.BURIED_CHEST),
        # spawn_idx=8, Stray Bead
    }
}

# These are added separately and conditionally created based on RandomizeShops option
shop_locations = {
    RegionNames.KAMIKI_MERCHANT: {
        "Kamiki Village - Shop Slot 1": LocData(shop_check_id(5, 0), type=LocationType.SHOP),
        "Kamiki Village - Shop Slot 2": LocData(shop_check_id(5, 1), type=LocationType.SHOP),
        "Kamiki Village - Shop Slot 3": LocData(shop_check_id(5, 2), type=LocationType.SHOP),
        "Kamiki Village - Shop Slot 4": LocData(shop_check_id(5, 3), type=LocationType.SHOP),
        "Kamiki Village - Shop Slot 5": LocData(shop_check_id(5, 4), type=LocationType.SHOP),
        "Kamiki Village - Shop Slot 6": LocData(shop_check_id(5, 5), type=LocationType.SHOP),
        "Kamiki Village - Shop Slot 7": LocData(shop_check_id(5, 6), type=LocationType.SHOP),
        "Kamiki Village - Shop Slot 8": LocData(shop_check_id(5, 7), type=LocationType.SHOP),
        "Kamiki Village - Shop Slot 9": LocData(shop_check_id(5, 8), type=LocationType.SHOP),
        "Kamiki Village - Shop Slot 10": LocData(shop_check_id(5, 9), type=LocationType.SHOP),
        "Kamiki Village - Shop Slot 11": LocData(shop_check_id(5, 10), type=LocationType.SHOP),
        "Kamiki Village - Shop Slot 12": LocData(shop_check_id(5, 11), type=LocationType.SHOP),
    }
}
