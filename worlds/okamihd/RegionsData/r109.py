from typing import TYPE_CHECKING

from BaseClasses import LocationProgressType
from rule_builder.rules import True_, Has
from ..CheckIds import brush_check_id, container_check_id, shop_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.OkamiEnemies import OkamiEnemies
from ..Enums.RegionNames import RegionNames, MapIds
from ..Enums.WarpType import WarpType
from ..Types import EventData, ExitData, LocData, WarpData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.SASA_SANCTUARY_ENTRANCE: [
        ExitData(RegionNames.SASA_SANCTUARY, has_events=["Taka Pass - Save Chun"],loading_screen=False)],

    RegionNames.SASA_SANCTUARY: [ExitData( RegionNames.SASA_SANCTUARY_BAMBOO,
                                          has_events=["Sasa Sanctuary - Open Bamboo grove Door"],loading_screen=False)]
}
events = {
    RegionNames.SASA_SANCTUARY: {
        "Sasa Sanctuary - Dig with Mr. Bamboo.": EventData(type=LocationType.DIGGING_MINIGAME_EARLY),
        "Sasa Sanctuary - Open Bamboo grove Door": EventData(required_brush_techniques=[BrushTechniques.WATERSPOUT])
    },
    RegionNames.SASA_SANCTUARY_BAMBOO: {
        "Sasa Sanctuary - Save Take": EventData(power_slash_level=1),
        "Sasa Sanctuary - Get Orb from Take": EventData(id=144, mandatory_enemies=[OkamiEnemies.TAKE],
                                                        is_event_item=lambda o: o.CanineRewards != 0,
                                                        progress_type=lambda
                                                            o: LocationProgressType.EXCLUDED if o.CanineRewards == 2
                                                        else LocationProgressType.DEFAULT,
                                                        event_item_name="Satomi Power Orb (Duty)",
                                                        required_items_events=["Sasa Sanctuary - Save Take"])
    }
}
locations = {
    RegionNames.SASA_SANCTUARY_ENTRANCE: {
        "Sasa Sanctuary - Buried Chest near Entrance": LocData(container_check_id(MapIds.SASA_SANCTUARY, 40), type=LocationType.BURIED_CHEST)
    },
    RegionNames.SASA_SANCTUARY: {
        "Sasa Sanctuary - 4th West side chest near Papa Jamba": LocData(container_check_id(MapIds.SASA_SANCTUARY, 0), type=LocationType.NORMAL_CHEST),
        "Sasa Sanctuary - 2nd West side chest near Papa Jamba": LocData(container_check_id(MapIds.SASA_SANCTUARY, 1), type=LocationType.NORMAL_CHEST),
        "Sasa Sanctuary - 5th East side chest near Papa Jamba": LocData(container_check_id(MapIds.SASA_SANCTUARY, 2), type=LocationType.NORMAL_CHEST),
        "Sasa Sanctuary - 3rd East side chest near Papa Jamba": LocData(container_check_id(MapIds.SASA_SANCTUARY, 3), type=LocationType.NORMAL_CHEST),
        "Sasa Sanctuary - 1st East side chest near Papa Jamba": LocData(container_check_id(MapIds.SASA_SANCTUARY, 4), type=LocationType.NORMAL_CHEST),
        "Sasa Sanctuary - 4th East side chest near Papa Jamba": LocData(container_check_id(MapIds.SASA_SANCTUARY, 20), type=LocationType.NORMAL_CHEST),
        "Sasa Sanctuary - 2nd East side chest near Papa Jamba": LocData(container_check_id(MapIds.SASA_SANCTUARY, 21), type=LocationType.NORMAL_CHEST),
        "Sasa Sanctuary - 5th West side chest near Papa Jamba": LocData(container_check_id(MapIds.SASA_SANCTUARY, 22), type=LocationType.NORMAL_CHEST),
        "Sasa Sanctuary - 3rd West side chest near Papa Jamba": LocData(container_check_id(MapIds.SASA_SANCTUARY, 23), type=LocationType.NORMAL_CHEST),
        "Sasa Sanctuary - 1st West side chest near Papa Jamba": LocData(container_check_id(MapIds.SASA_SANCTUARY, 24), type=LocationType.NORMAL_CHEST),
        "Sasa Sanctuary - Buried Chest near hot springs": LocData(container_check_id(MapIds.SASA_SANCTUARY, 41), type=LocationType.BURIED_CHEST),
        "Sasa Sanctuary - Nuregami": LocData(brush_check_id(13), type=LocationType.CONSTELLATION),  # bit 13
        "Sasa Sanctuary - Daruma Doll": LocData(container_check_id(MapIds.SASA_SANCTUARY, 43), type=LocationType.DARUMA)
    },
    RegionNames.SASA_SANCTUARY_BAMBOO: {
        "Sasa Sanctuary - Buried Chest in bamboo grove stairs": LocData(container_check_id(MapIds.SASA_SANCTUARY, 42), type=LocationType.BURIED_CHEST),
        "Sasa Sanctuary - Left side Buried Chest in bamboo grove back": LocData(container_check_id(MapIds.SASA_SANCTUARY, 46), type=LocationType.BURIED_CHEST),
        "Sasa Sanctuary - Right side Buried Chest in bamboo grove back": LocData(container_check_id(MapIds.SASA_SANCTUARY, 45), type=LocationType.BURIED_CHEST),
    }
}

shop_locations={
    RegionNames.SASA_SANCTUARY:{
        "Sasa Sanctuary - Shop Slot 1": LocData(shop_check_id(15, 0), type=LocationType.SHOP),
        "Sasa Sanctuary - Shop Slot 2": LocData(shop_check_id(15, 1), type=LocationType.SHOP),
        "Sasa Sanctuary - Shop Slot 3": LocData(shop_check_id(15, 2), type=LocationType.SHOP),
        "Sasa Sanctuary - Shop Slot 4": LocData(shop_check_id(15, 3), type=LocationType.SHOP),
        "Sasa Sanctuary - Shop Slot 5": LocData(shop_check_id(15, 4), type=LocationType.SHOP),
        "Sasa Sanctuary - Shop Slot 6": LocData(shop_check_id(15, 5), type=LocationType.SHOP),
        "Sasa Sanctuary - Shop Slot 7": LocData(shop_check_id(15, 6), type=LocationType.SHOP),
        "Sasa Sanctuary - Shop Slot 8": LocData(shop_check_id(15, 7), type=LocationType.SHOP),
        "Sasa Sanctuary - Shop Slot 9": LocData(shop_check_id(15, 8), type=LocationType.SHOP),
        "Sasa Sanctuary - Shop Slot 10": LocData(shop_check_id(15, 9), type=LocationType.SHOP),
        "Sasa Sanctuary - Shop Slot 11": LocData(shop_check_id(15, 10), type=LocationType.SHOP),
        "Sasa Sanctuary - Shop Slot 12": LocData(shop_check_id(15, 11), type=LocationType.SHOP),
    }
}

warps={
    RegionNames.SASA_SANCTUARY:[
        WarpData(type=WarpType.MIST_WARP,trigger_warp_to=True_,trigger_warp_from=True_),
        WarpData(type=WarpType.MERMAID_SPRING, trigger_warp_to=Has( "Sasa Sanctuary - Dig with Mr. Bamboo."), trigger_warp_from=Has( "Sasa Sanctuary - Dig with Mr. Bamboo."))
    ]
}