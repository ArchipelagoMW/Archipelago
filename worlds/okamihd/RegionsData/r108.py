from typing import TYPE_CHECKING

from BaseClasses import LocationProgressType
from rule_builder.rules import True_
from .r102 import shop_locations
from ..CheckIds import container_check_id, shop_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.OkamiEnemies import OkamiEnemies
from ..Enums.RegionNames import RegionNames, MapIds
from ..Enums.WarpType import WarpType
from ..Types import EventData, ExitData, LocData, WarpData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.KUSA_VILLAGE: [ExitData(RegionNames.KUSA_VILLAGE_BLOCKHEAD,
                                        has_events=['Kusa Village - Defeat Blockhead'], loading_screen=False),
                               ExitData(RegionNames.BAMBOO_HOUSE),
                               ExitData(RegionNames.KUSA_INN),
                               ExitData(RegionNames.GALE_SHRINE_ENTRANCE)]
}
events = {

    RegionNames.KUSA_VILLAGE: {
        "Kusa Village - Save Fuse": EventData(mandatory_enemies=[OkamiEnemies.GREEN_IMP, OkamiEnemies.BLUE_IMP]),
        "Kusa Village - Defeat Blockhead": EventData(precollected=lambda o: o.RemoveBlockHead),
        "Kusa Village - Access Blockhead": EventData(required_brush_techniques=[BrushTechniques.GREENSPROUT_VINE]),
        "Kusa Village - Save Rei": EventData(id=128, cherry_bomb_level=1,
                                             is_event_item=lambda o: o.CanineRewards != 0,
                                             progress_type=lambda
                                                 o: LocationProgressType.EXCLUDED if o.CanineRewards == 2
                                             else LocationProgressType.DEFAULT,
                                             event_item_name="Satomi Power Orb (Rei)",
                                             required_items_events=["Kusa Village - Save Fuse"]),
        "Kusa Village - Save Shin": EventData(id=129, required_brush_techniques=[BrushTechniques.GREENSPROUT_BLOOM],
                                              is_event_item=lambda o: o.CanineRewards != 0,
                                              progress_type=lambda
                                                  o: LocationProgressType.EXCLUDED if o.CanineRewards == 2
                                              else LocationProgressType.DEFAULT,
                                              event_item_name="Satomi Power Orb (Shin)",
                                              required_items_events=["Kusa Village - Save Fuse"]),
        "Kusa Village - Save Chi": EventData(id=130, power_slash_level=1,
                                             is_event_item=lambda o: o.CanineRewards != 0,
                                             progress_type=lambda
                                                 o: LocationProgressType.EXCLUDED if o.CanineRewards == 2
                                             else LocationProgressType.DEFAULT,
                                             event_item_name="Satomi Power Orb (Chi)",
                                             required_items_events=["Kusa Village - Save Fuse"]),
        "Kusa Village - Save Ko": EventData(id=131, required_brush_techniques=[BrushTechniques.GREENSPROUT_VINE],
                                            is_event_item=lambda o: o.CanineRewards != 0,
                                            progress_type=lambda
                                                o: LocationProgressType.EXCLUDED if o.CanineRewards == 2
                                            else LocationProgressType.DEFAULT, event_item_name="Satomi Power Orb (Ko)",
                                            required_items_events=["Kusa Village - Save Fuse"]),
        # Should we add more conditions to get this one ?
        "Kusa Village - Save Tei": EventData(id=132, mandatory_enemies=[OkamiEnemies.TEI],
                                             is_event_item=lambda o: o.CanineRewards != 0,
                                             progress_type=lambda
                                                 o: LocationProgressType.EXCLUDED if o.CanineRewards == 2
                                             else LocationProgressType.DEFAULT,
                                             event_item_name="Satomi Power Orb (Tei)",
                                             required_items_events=["Satomi Power Orb (Rei)",
                                                                    "Satomi Power Orb (Shin)",
                                                                    "Satomi Power Orb (Chi)",
                                                                    "Satomi Power Orb (Ko)"])
    }
}
locations = {
    RegionNames.KUSA_VILLAGE: {
        "Kusa Village - Chest on rafters after banners": LocData(container_check_id(MapIds.KUSA_VILLAGE, 11),
                                                                 required_brush_techniques=[BrushTechniques.GALESTORM,
                                                                                            BrushTechniques.GREENSPROUT_VINE]),
        "Kusa Village - Chest on rafters before banners": LocData(container_check_id(MapIds.KUSA_VILLAGE, 42),
                                                                  required_brush_techniques=[
                                                                      BrushTechniques.GREENSPROUT_VINE]),
        "Kusa Village - Stray Bead Chest on rafters after banners": LocData(container_check_id(MapIds.KUSA_VILLAGE, 43),
                                                                            required_brush_techniques=[
                                                                                BrushTechniques.GALESTORM,
                                                                                BrushTechniques.GREENSPROUT_VINE]),
        "Kusa Village - Buried Chest near Fuse's house": LocData(container_check_id(MapIds.KUSA_VILLAGE, 53),
                                                                 type=LocationType.BURIED_CHEST),
        "Kusa Village - Buried Chest near Gale Shrine Ledge": LocData(container_check_id(MapIds.KUSA_VILLAGE, 58),
                                                                      type=LocationType.BURIED_CHEST),
        "Kusa Village - Underwater Chest near Fuse's house right": LocData(container_check_id(MapIds.KUSA_VILLAGE, 70),
                                                                           type=LocationType.UNDERWATER_CHEST),
        "Kusa Village - Underwater Chest near Fuse's house left": LocData(container_check_id(MapIds.KUSA_VILLAGE, 71),
                                                                          type=LocationType.UNDERWATER_CHEST)
    },
    RegionNames.KUSA_INN: {
        "Kusa Village - Daruma inside Inn": LocData(container_check_id(MapIds.KUSA_VILLAGE, 68),
                                                    type=LocationType.DARUMA)
    },
    RegionNames.KUSA_VILLAGE_BLOCKHEAD: {
        "Kusa Village - Chest inside Blockhead Cave": LocData(container_check_id(MapIds.KUSA_VILLAGE, 10))
    },
    RegionNames.BAMBOO_HOUSE: {
        "Kusa Village - Buried Chest inside Mr Bamboo's house": LocData(container_check_id(MapIds.KUSA_VILLAGE, 47),
                                                                        type=LocationType.BURIED_CHEST)
    }
}

shop_locations = {
    RegionNames.KUSA_VILLAGE: {
        "Kusa Village - Shop Slot 1": LocData(shop_check_id(8, 0), type=LocationType.SHOP),
        "Kusa Village - Shop Slot 2": LocData(shop_check_id(8, 1), type=LocationType.SHOP),
        "Kusa Village - Shop Slot 3": LocData(shop_check_id(8, 2), type=LocationType.SHOP),
        "Kusa Village - Shop Slot 4": LocData(shop_check_id(8, 3), type=LocationType.SHOP),
        "Kusa Village - Shop Slot 5": LocData(shop_check_id(8, 4), type=LocationType.SHOP),
        "Kusa Village - Shop Slot 6": LocData(shop_check_id(8, 5), type=LocationType.SHOP),
        "Kusa Village - Shop Slot 7": LocData(shop_check_id(8, 6), type=LocationType.SHOP),
        "Kusa Village - Shop Slot 8": LocData(shop_check_id(8, 7), type=LocationType.SHOP),
        "Kusa Village - Shop Slot 9": LocData(shop_check_id(8, 8), type=LocationType.SHOP),
        "Kusa Village - Shop Slot 10": LocData(shop_check_id(8, 9), type=LocationType.SHOP),
        "Kusa Village - Shop Slot 11": LocData(shop_check_id(8, 10), type=LocationType.SHOP),
        "Kusa Village - Shop Slot 12": LocData(shop_check_id(8, 11), type=LocationType.SHOP),
    }
}

warps = {
    RegionNames.KUSA_VILLAGE: [
        WarpData(type=WarpType.MIST_WARP, trigger_warp_to=True_, trigger_warp_from=True_)
    ]
}
