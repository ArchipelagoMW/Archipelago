from typing import TYPE_CHECKING

from rule_builder.rules import True_, Has
from ..CheckIds import container_check_id, shop_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.OkamiEnemies import OkamiEnemies
from ..Enums.RegionNames import RegionNames, MapIds
from ..Enums.WarpType import WarpType
from ..Types import EventData, ExitData, LocData, WarpData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits={
    RegionNames.TAKA_PASS:[ExitData(RegionNames.KUSA_VILLAGE),
                           ExitData(RegionNames.SASA_SANCTUARY_ENTRANCE),
                           ExitData(RegionNames.CITY_CHECKPOINT_TAKA)]

}
events={
    RegionNames.TAKA_PASS:{
        "Taka Pass - Clear Devil gate near waterfall": EventData(mandatory_enemies=[OkamiEnemies.BUD_OGRE,OkamiEnemies.YELLOW_IMP]),
        "Taka Pass - Save Chun" : EventData(cherry_bomb_level=1,mandatory_enemies=[OkamiEnemies.CUTTERS])
    }
}

locations = {
    RegionNames.TAKA_PASS:{
        "Taka Pass - Chest under leaf pile near Guardian Sapling" : LocData(container_check_id(MapIds.HEALED_TAKA,42), type=LocationType.BURIED_UNDER_LEAF_PILE,required_items_events=["Taka pass - Restore Bridge to Guardian Sapling"]),
        "Taka Pass - Chest on top of big rock above ledge": LocData(container_check_id(MapIds.HEALED_TAKA, 0),required_brush_techniques=[BrushTechniques.GREENSPROUT_VINE]),
        # Find better names for those 2 a
        "Taka Pass - Chest under leaf pile after cave": LocData(container_check_id(MapIds.HEALED_TAKA,41),type=LocationType.BURIED_UNDER_LEAF_PILE),
        "Taka Pass - Chest under leaf pile near cave west": LocData(container_check_id(MapIds.HEALED_TAKA,62), type=LocationType.BURIED_UNDER_LEAF_PILE),

        "Taka Pass - Chest under leaf pile near Ultimate Origin mirror": LocData(container_check_id(MapIds.HEALED_TAKA,60), type=LocationType.BURIED_UNDER_LEAF_PILE),
        "Taka Pass - Chest on top of Gutters' House":LocData(container_check_id(MapIds.HEALED_TAKA, 1),required_brush_techniques=[BrushTechniques.GREENSPROUT_VINE]),
        "Taka Pass - Chest across banners": LocData(container_check_id(MapIds.HEALED_TAKA, 3), required_brush_techniques=[BrushTechniques.GREENSPROUT_VINE, BrushTechniques.GALESTORM]),
        "Taka Pass - Buried chest near Gutters' house":LocData(container_check_id(MapIds.HEALED_TAKA,25),type=LocationType.BURIED_CHEST),
        "Taka Pass - Buried chest near mermaid spring": LocData(container_check_id(MapIds.HEALED_TAKA,32), type=LocationType.BURIED_CHEST),
        "Taka Pass - Buried chest near tea house": LocData(container_check_id(MapIds.HEALED_TAKA,36), type=LocationType.BURIED_CHEST),
        "Taka Pass - Buried chest near treasure hunter": LocData(container_check_id(MapIds.HEALED_TAKA,37), type=LocationType.BURIED_CHEST),
        #Find a better name
        "Taka Pass - Buried under leaf pile near city checkpoint exit": LocData(container_check_id(MapIds.HEALED_TAKA,38), type=LocationType.BURIED_UNDER_LEAF_PILE),
        #Find out which house
        "Taka Pass - Chest under leaf pile behind Gutters' house": LocData(container_check_id(MapIds.HEALED_TAKA,43), type=LocationType.BURIED_UNDER_LEAF_PILE),
        "Taka Pass - Chest under leaf pile near mermaid spring": LocData(container_check_id(MapIds.HEALED_TAKA,44), type=LocationType.BURIED_UNDER_LEAF_PILE),
        "Taka Pass - Chest under leaf pile near city checkpoint exit #2": LocData(container_check_id(MapIds.HEALED_TAKA,59), type=LocationType.BURIED_UNDER_LEAF_PILE),
        "Taka Pass - Chest under leaf pile near moles gang": LocData(container_check_id(MapIds.HEALED_TAKA,61),type=LocationType.BURIED_UNDER_LEAF_PILE),
    }

}

# These are added separately and conditionally created based on RandomizeShops option
shop_locations = {
    RegionNames.TAKA_PASS: {
        "Taka Pass - Shop Slot 1": LocData(shop_check_id(19, 0), type=LocationType.SHOP),
        "Taka Pass - Shop Slot 2": LocData(shop_check_id(19, 1), type=LocationType.SHOP),
        "Taka Pass - Shop Slot 3": LocData(shop_check_id(19, 2), type=LocationType.SHOP),
        "Taka Pass - Shop Slot 4": LocData(shop_check_id(19, 3), type=LocationType.SHOP),
        "Taka Pass - Shop Slot 5": LocData(shop_check_id(19, 4), type=LocationType.SHOP),
        "Taka Pass - Shop Slot 6": LocData(shop_check_id(19, 5), type=LocationType.SHOP),
        "Taka Pass - Shop Slot 7": LocData(shop_check_id(19, 6), type=LocationType.SHOP),
        "Taka Pass - Shop Slot 8": LocData(shop_check_id(19, 7), type=LocationType.SHOP),
        "Taka Pass - Shop Slot 9": LocData(shop_check_id(19, 8), type=LocationType.SHOP),
        "Taka Pass - Shop Slot 10": LocData(shop_check_id(19, 9), type=LocationType.SHOP),
        "Taka Pass - Shop Slot 11": LocData(shop_check_id(19, 10), type=LocationType.SHOP),
        "Taka Pass - Shop Slot 12": LocData(shop_check_id(19, 11), type=LocationType.SHOP),
    }
}

warps={
    RegionNames.TAKA_PASS:[
        WarpData(type=WarpType.MERMAID_SPRING, trigger_warp_to=Has("Taka Pass - Clear Devil gate near waterfall"), trigger_warp_from=Has("Taka Pass - Clear Devil gate near waterfall"))
    ]
}
