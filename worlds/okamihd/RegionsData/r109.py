from typing import TYPE_CHECKING

from BaseClasses import LocationProgressType
from ..CheckIds import brush_check_id, container_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.OkamiEnemies import OkamiEnemies
from ..Enums.RegionNames import RegionNames
from ..Rules import gale_shrine_access
from ..Types import EventData, ExitData, LocData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.SASA_SANCTUARY_ENTRANCE: [
        ExitData("Sasa Sanctuary Gate", RegionNames.SASA_SANCTUARY, has_events=["Taka Pass - Save Chun"])],
    RegionNames.SASA_SANCTUARY: [ExitData("To Bamboo Grove", RegionNames.SASA_SANCTUARY_BAMBOO,
                                          has_events=["Sasa Sanctuary - Open Bamboo grove Door"])]
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
                                                        event_item_name="Duty Orb",
                                                        required_items_events=["Sasa Sanctuary - Save Take"])
    }
}
locations = {
    RegionNames.SASA_SANCTUARY_ENTRANCE: {
        "Sasa Sanctuary - Buried Chest near Entrance": LocData(container_check_id(0x109, 40), type=LocationType.BURIED_CHEST)
    },
    RegionNames.SASA_SANCTUARY: {
        "Sasa Sanctuary - 4th West side chest near Papa Jamba": LocData(container_check_id(0x109, 0), type=LocationType.NORMAL_CHEST),
        "Sasa Sanctuary - 2nd West side chest near Papa Jamba": LocData(container_check_id(0x109, 1), type=LocationType.NORMAL_CHEST),
        "Sasa Sanctuary - 5th East side chest near Papa Jamba": LocData(container_check_id(0x109, 2), type=LocationType.NORMAL_CHEST),
        "Sasa Sanctuary - 3rd East side chest near Papa Jamba": LocData(container_check_id(0x109, 3), type=LocationType.NORMAL_CHEST),
        "Sasa Sanctuary - 1st East side chest near Papa Jamba": LocData(container_check_id(0x109, 4), type=LocationType.NORMAL_CHEST),
        "Sasa Sanctuary - 4th East side chest near Papa Jamba": LocData(container_check_id(0x109, 20), type=LocationType.NORMAL_CHEST),
        "Sasa Sanctuary - 2nd East side chest near Papa Jamba": LocData(container_check_id(0x109, 21), type=LocationType.NORMAL_CHEST),
        "Sasa Sanctuary - 5th West side chest near Papa Jamba": LocData(container_check_id(0x109, 22), type=LocationType.NORMAL_CHEST),
        "Sasa Sanctuary - 3rd West side chest near Papa Jamba": LocData(container_check_id(0x109, 23), type=LocationType.NORMAL_CHEST),
        "Sasa Sanctuary - 1st West side chest near Papa Jamba": LocData(container_check_id(0x109, 24), type=LocationType.NORMAL_CHEST),
        "Sasa Sanctuary - Buried Chest near hot springs": LocData(container_check_id(0x109, 41), type=LocationType.BURIED_CHEST),
        "Sasa Sanctuary - Nuregami": LocData(brush_check_id(13), type=LocationType.CONSTELLATION),  # bit 13
        "Sasa Sanctuary - Daruma Doll": LocData(container_check_id(0x109, 43), type=LocationType.DARUMA)
    },
    RegionNames.SASA_SANCTUARY_BAMBOO: {
        "Sasa Sanctuary - Buried Chest in bamboo grove stairs": LocData(container_check_id(0x109, 42), type=LocationType.BURIED_CHEST),
        "Sasa Sanctuary - Left side Buried Chest in bamboo grove back": LocData(container_check_id(0x109, 46), type=LocationType.BURIED_CHEST),
        "Sasa Sanctuary - Right side Buried Chest in bamboo grove back": LocData(container_check_id(0x109, 45), type=LocationType.BURIED_CHEST),
    }
}
