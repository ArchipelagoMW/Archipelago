from typing import TYPE_CHECKING

from ..CheckIds import container_check_id, brush_check_id, shop_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.RegionNames import RegionNames, MapIds
from ..Types import ExitData, LocData, EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.SEIAN_CITY_BRIDGE_COMMONERS: [
        ExitData(RegionNames.SEIAN_CITY_BRIDGE_ARISTOCRATIC,
                 has_events=["Sei-an City (Aristocratic Quarter) - Fish The Living Sword with Benkei"],
                 loading_screen=False)
    ],
    RegionNames.SEIAN_CITY_BRIDGE_ARISTOCRATIC: [
        ExitData(RegionNames.SEIAN_CITY_LECTURE_HALL)
    ],
    RegionNames.SEIAN_CITY_LECTURE_HALL: [
        ExitData(RegionNames.SEIAN_CITY_ARISTOCRATIC_SICK)
    ],
    RegionNames.SEIAN_CITY_ARISTOCRATIC_SICK: [
        ExitData(RegionNames.SEIAN_CITY_OKUNI),
        ExitData(RegionNames.SEIAN_CITY_ARISTOCRATIC_NORTH_EAST),
        ExitData(RegionNames.SEIAN_CITY_CLOCK_TOWER, one_way=True,
                 has_events=["Sei-an City (Aristocratic Quarter) - Climb clock tower"]),
        ExitData(RegionNames.SEIAN_CITY_ARISTOCRATIC, loading_screen=False,
                 has_events=["Inside the Emperor - Defeat Blight"]),
        ExitData(RegionNames.IMPERIAL_PALACE_ENTRANCE)
    ],
    RegionNames.SEIAN_CITY_CLOCK_TOWER: [
        ExitData(RegionNames.SEIAN_CITY_ARISTOCRATIC_SICK, one_way=True)
    ],
    RegionNames.SEIAN_CITY_ARISTOCRATIC: [
        ExitData(RegionNames.SEIAN_CITY_HIMIKO, one_way=True, loading_screen=False)
    ],
    RegionNames.SEIAN_CITY_HIMIKO: [
        ExitData(RegionNames.SEIAN_CITY_ARISTOCRATIC, one_way=True, loading_screen=False),
        ExitData(RegionNames.SEIAN_CITY_ARISTOCRATIC_SICK, one_way=True, loading_screen=False),
        ExitData(RegionNames.SEIAN_CITY_TREASURE_WEST),
        ExitData(RegionNames.SEIAN_CITY_TREASURE_EAST)
    ]
}
events = {
    RegionNames.SEIAN_CITY_BRIDGE_COMMONERS: {
        "Sei-an City (Aristocratic Quarter) - Fish The Living Sword with Benkei": EventData(
            required_items_events=["Sei-an City (Commoner's Quarter) - Dig water source", "Blinding Snow"],
            type=LocationType.FISHING_MINIGAME)
    },
    RegionNames.SEIAN_CITY_ARISTOCRATIC_SICK: {
        "Sei-an City (Aristocratic Quarter) - Climb clock tower": EventData(
            required_brush_techniques=[BrushTechniques.CATWALK])
    },
    RegionNames.SEIAN_CITY_ARISTOCRATIC: {
        "Sei-an City (Aristocratic Quarter) - Fool Himiko's Guards": EventData(required_brush_techniques=[BrushTechniques.VEIL_OF_MIST])
    },
    RegionNames.SEIAN_CITY_LECTURE_HALL:{
        #biteable check #2, do we have access to Rao to give her the item ?
        "Sei-an City (Aristocratic Quarter) - Give Prayer Slips to Rao": EventData(required_items_events=["Imperial Palace - Grab Prayer Slips"])
    }
}
locations = {
    RegionNames.SEIAN_CITY_LECTURE_HALL: {
        "Sei-an City (Aristocratic Quarter) - West chest in lecture hall": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 9)),
        "Sei-an City (Aristocratic Quarter) - East chest in lecture hall": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 13))
    },
    RegionNames.SEIAN_CITY_OKUNI: {
        "Sei-an City (Aristocratic Quarter) - Chest in Okuni's house": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 21))
    },
    RegionNames.SEIAN_CITY_ARISTOCRATIC_SICK: {
        "Sei-an City (Aristocratic Quarter) - Freestanding Chest outside Okuni's house": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 19)),
        "Sei-an City (Aristocratic Quarter) - Buried chest outside Okuni's house": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 20), type=LocationType.BURIED_CHEST),
        "Sei-an City (Aristocratic Quarter) - Underwater chest east of central bridge": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 41), type=LocationType.UNDERWATER_CHEST),
        "Sei-an City (Aristocratic Quarter) - Freestanding Chest outside northeast house": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 4)),
        "Sei-an City (Aristocratic Quarter) - Buried chest outside northeast house": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 5), type=LocationType.BURIED_CHEST),
        "Sei-an City (Aristocratic Quarter) - Buried chest east of Himiko's palace guards": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 2), type=LocationType.BURIED_CHEST),
        "Sei-an City (Aristocratic Quarter) - Buried chest behind clock tower": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 3), type=LocationType.BURIED_CHEST),
    },
    RegionNames.SEIAN_CITY_ARISTOCRATIC_NORTH_EAST: {
        "Sei-an City (Aristocratic Quarter) - Chest in northeast house": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 40)),
    },
    # In Vanilla ,clock tower checks require story progression
    RegionNames.SEIAN_CITY_CLOCK_TOWER: {

    },
    RegionNames.SEIAN_CITY_HIMIKO: {
        "Sei-an City (Aristocratic Quarter) - East buried chest behind Himiko's guards": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 7), type=LocationType.BURIED_CHEST),
        "Sei-an City (Aristocratic Quarter) - Northeast Freestanding chest in Himiko's palace entrance": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 6)),
        "Sei-an City (Aristocratic Quarter) - Freestanding chest behind Himiko's palace": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 47)),
    },
    RegionNames.SEIAN_CITY_TREASURE_WEST: {
        "Sei-an City (Aristocratic Quarter) - Daruma doll inside Himiko's west treasure room": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 48)),
        "Sei-an City (Aristocratic Quarter) - Freestanding chest inside Himiko's west treasure room": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 9)),
    },
    RegionNames.SEIAN_CITY_TREASURE_EAST: {
        "Sei-an City (Aristocratic Quarter) - West freestanding chest inside Himiko's east treasure room": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 11)),
        "Sei-an City (Aristocratic Quarter) - West freestanding chest inside Himiko's east treasure room 2": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 8)),
        "Sei-an City (Aristocratic Quarter) - East freestanding chest inside Himiko's east treasure room 2": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 12)),

    }
}
