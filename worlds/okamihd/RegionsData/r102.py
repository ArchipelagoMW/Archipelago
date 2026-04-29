from typing import TYPE_CHECKING

from BaseClasses import LocationProgressType
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.OkamiEnemies import OkamiEnemies
from ..Enums.RegionNames import RegionNames
from ..Rules import night_time_check_rule
from ..Types import ExitData, LocData, EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.STONE_KAMIKI: [ExitData("Restore the villagers", RegionNames.KAMIKI_VILLAGE,
                                        has_events=["Kamiki Village - Fight with Mr.Orange"])],
    RegionNames.KAMIKI_VILLAGE: [ExitData("Swim to Kamiki Islands", RegionNames.KAMIKI_ISLANDS, needs_long_swim=True),
                                 ExitData("Enter Susano's House", RegionNames.SUSANOS_HOUSE),
                                 ExitData("Enter Kushi's House", RegionNames.KUSHIS_HOUSE),
                                 ExitData("Enter Oranges' House", RegionNames.ORANGES_HOUSE),
                                 ExitData("Exit Village to Cursed Shinshu field", RegionNames.CURSED_SHINSHU_FIELD,
                                          has_events=["Kamiki Village - Help Susano Train/Break the boulder"])],
    RegionNames.SUSANOS_HOUSE: [ExitData("Enter meditation Chamber", RegionNames.SUSANOS_UNDERGROUD)]
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
                                                            special_rule=lambda s,w:night_time_check_rule(s,w))

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
    # Container IDs: 900000 + (0x102 << 8) + spawn_idx = 966048 + spawn_idx
    RegionNames.STONE_KAMIKI: {
        "Kamiki Village - Sunrise": LocData(200027, type=LocationType.CONSTELLATION),  # Brush acquisition (bit 27)
    },
    RegionNames.KAMIKI_VILLAGE: {
        "Kamiki Village - Chest After Mr.Orange Yokai Fight": LocData(966135),  # spawn_idx=87, Feedbag(Seeds)
        "Kamiki Village - Buried Chest near Komuso": LocData(966048, type=LocationType.BURIED_CHEST),  # spawn_idx=0, Traveler's Charm
        "Kamiki Village - Underwater Chest 1": LocData(966064, type=LocationType.UNDERWATER_CHEST_SHALLOW),  # spawn_idx=16, Rabbit Statue
        "Kamiki Village - Underwater Chest 2": LocData(966081, type=LocationType.UNDERWATER_CHEST_SHALLOW),  # spawn_idx=33, Glass Beads
        "Kamiki Village - Underwater chest in lake near Kushi's house": LocData(966080, type=LocationType.UNDERWATER_CHEST),  # spawn_idx=32, Vase
        "Kamiki Village - Hasugami": LocData(200005, required_items_events=["Kamiki Village - Restore Sakuya's Tree"],
                                             type=LocationType.CONSTELLATION),  # Brush acquisition (Waterlily)
        "Kamiki Village - Buried chest in field": LocData(966061, type=LocationType.BURIED_CHEST),  # spawn_idx=13, Dragonfly Bead
        "Kamiki Village - Chest on Ledge": LocData(966057, required_brush_techniques=[BrushTechniques.GREENSPROUT_VINE]),  # spawn_idx=9, Exorcism Slip S
        "Kamiki Village - Rafters Lower Chest": LocData(966059),  # spawn_idx=11, Stray Bead
        "Kamiki Village - Rafters Upper Chest": LocData(966058, power_slash_level=1),  # spawn_idx=10, Glass Beads,
        # West Island doesn't require long swim
        "Kamiki Village - West Island chest ": LocData(966096),  # spawn_idx=48, Dragonfly Bead
        "Kamiki Village - West Island buried chest": LocData(966102, type=LocationType.BURIED_CHEST),# spawn_idx=54, Wooden Bear
    },
    RegionNames.ORANGES_HOUSE: {
        "Kamiki Village - Chest buried in Oranges' house": LocData(966067, type=LocationType.BURIED_CHEST),  # spawn_idx=19, Coral Fragment
    },
    RegionNames.KUSHIS_HOUSE: {
        # Kushi's Gift is not a container - it's an event/NPC reward. Keep old ID for now.
        "Kamiki Village - Kushi's Gift": LocData(500000 + 3 * 10000 + 11,  # mapId=3 (KamikiVillage enum index)
                                                 required_items_events=["Kamiki Village - Repair Kushi's Watermill"]),
    },
    RegionNames.KAMIKI_ISLANDS: {
        "Kamiki Village - East Islands Sun fragment chest": LocData(966090),  # spawn_idx=42, Sun Fragment
        "Kamiki Village - East Islands Right Buried Chest": LocData(966055, type=LocationType.BURIED_CHEST),  # spawn_idx=7, Inkfinity Stone
        "Kamiki Village - East Islands Left Buried Chest": LocData(966056, type=LocationType.BURIED_CHEST),  # spawn_idx=8, Stray Bead
    }
}

# Shop locations (shopId=5): 300000 + 5*1000 + slot = 305000 + slot
# These are added separately and conditionally created based on RandomizeShops option
shop_locations = {
    RegionNames.KAMIKI_VILLAGE: {
        "Kamiki Village - Shop Slot 1": LocData(305000, type=LocationType.SHOP),
        "Kamiki Village - Shop Slot 2": LocData(305001, type=LocationType.SHOP),
        "Kamiki Village - Shop Slot 3": LocData(305002, type=LocationType.SHOP),
        "Kamiki Village - Shop Slot 4": LocData(305003, type=LocationType.SHOP),
        "Kamiki Village - Shop Slot 5": LocData(305004, type=LocationType.SHOP),
        "Kamiki Village - Shop Slot 6": LocData(305005, type=LocationType.SHOP),
        "Kamiki Village - Shop Slot 7": LocData(305006, type=LocationType.SHOP),
        "Kamiki Village - Shop Slot 8": LocData(305007, type=LocationType.SHOP),
        "Kamiki Village - Shop Slot 9": LocData(305008, type=LocationType.SHOP),
        "Kamiki Village - Shop Slot 10": LocData(305009, type=LocationType.SHOP),
        "Kamiki Village - Shop Slot 11": LocData(305010, type=LocationType.SHOP),
        "Kamiki Village - Shop Slot 12": LocData(305011, type=LocationType.SHOP),
    }
}
