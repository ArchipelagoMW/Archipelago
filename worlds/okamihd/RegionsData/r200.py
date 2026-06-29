from typing import TYPE_CHECKING

from BaseClasses import LocationProgressType
from rule_builder.rules import True_, Has
from ..CheckIds import container_check_id, brush_check_id, shop_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.RegionNames import RegionNames, MapIds
from ..Enums.WarpType import WarpType
from ..Rules import gen_thunder_chest_rule
from ..Types import ExitData, LocData, EventData, WarpData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.SEIAN_CITY_BRIDGE_COMMONERS: [
        ExitData(RegionNames.SEIAN_CITY_BRIDGE_ARISTOCRATIC,
                 required_items_events=["Sei-an City (Aristocratic Quarter) - Fish The Living Sword with Benkei"],
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
                 required_items_events=["Sei-an City (Aristocratic Quarter) - Climb clock tower"]),
        ExitData(RegionNames.SEIAN_CITY_ARISTOCRATIC, loading_screen=False,
                 required_items_events=["Imperial Palace - Defeat Blight"]),
        ExitData(RegionNames.IMPERIAL_PALACE_ENTRANCE)
    ],
    RegionNames.SEIAN_CITY_CLOCK_TOWER: [
        ExitData(RegionNames.SEIAN_CITY_ARISTOCRATIC_SICK, one_way=True)
    ],
    RegionNames.SEIAN_CITY_ARISTOCRATIC: [
        ExitData(RegionNames.SEIAN_CITY_HIMIKO, one_way=True, loading_screen=False),
        ExitData(RegionNames.SEIAN_CITY_GUARDS),
        ExitData(RegionNames.SEIAN_CITY_LAKE, needs_long_swim=True, loading_screen=False)
    ],
    RegionNames.SEIAN_CITY_HIMIKO: [
        ExitData(RegionNames.SEIAN_CITY_ARISTOCRATIC, one_way=True, loading_screen=False),
        ExitData(RegionNames.SEIAN_CITY_ARISTOCRATIC_SICK, one_way=True, loading_screen=False),
        ExitData(RegionNames.SEIAN_CITY_TREASURE_WEST),
        ExitData(RegionNames.SEIAN_CITY_TREASURE_EAST),
        ExitData(RegionNames.HIMIKO_PALACE)
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
        "Sei-an City (Aristocratic Quarter) - Fool Himiko's Guards": EventData(
            required_brush_techniques=[BrushTechniques.VEIL_OF_MIST])
    },
    RegionNames.SEIAN_CITY_LECTURE_HALL: {
        # biteable check #2, do we have access to Rao to give her the item ?
        "Sei-an City (Aristocratic Quarter) - Give Prayer Slips to Rao": EventData(
            required_items_events=["Imperial Palace - Grab Prayer Slips"])
    },
    RegionNames.SEIAN_CITY_CLOCK_TOWER: {
        "Sei-an City(Aristocratic Quarter) - Give Gimmick gear to Gen": EventData(
            required_items_events=["Gimmick Gear"])
    },
    RegionNames.SEIAN_CITY_HIMIKO: {
        "Sei-an City (Aristocratic Quarter) - Mourn Himiko": EventData(
            required_brush_techniques=[BrushTechniques.WATERSPOUT])
    }
}
locations = {
    RegionNames.SEIAN_CITY_LECTURE_HALL: {
        "Sei-an City (Aristocratic Quarter) - West chest in lecture hall": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 14)),
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
            container_check_id(MapIds.SEIAN_ARISTORATIC, 41), type=LocationType.UNDERWATER_CHEST_SHALLOW),
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
    RegionNames.SEIAN_CITY_CLOCK_TOWER: {
        "Sei-an City (Aristocratic Quarter) - Thunder Chest in Clock Tower": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 10), type=LocationType.THUNDER_CHEST_SPECIAL_SOURCE,
            special_rule=gen_thunder_chest_rule),
        "Sei-an City (Aristocratic Quarter) - Chest after thunderbolt": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 0),
            required_items_events=["Sei-an City(Aristocratic Quarter) - Give Gimmick gear to Gen"],
            progress_type=LocationProgressType.EXCLUDED),
        "Sei-an City (Aristocratic Quarter) - Gekigami (Thunderbolt)": LocData(
            brush_check_id(9),
            required_items_events=["Sei-an City(Aristocratic Quarter) - Give Gimmick gear to Gen"],
            progress_type=LocationProgressType.EXCLUDED)
    },
    RegionNames.SEIAN_CITY_HIMIKO: {
        "Sei-an City (Aristocratic Quarter) - East buried chest behind Himiko's guards": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 7), type=LocationType.BURIED_CHEST),
        "Sei-an City (Aristocratic Quarter) - Northeast Freestanding chest in Himiko's palace entrance": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 6)),
        "Sei-an City (Aristocratic Quarter) - Freestanding chest behind Himiko's palace": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 47)),
        "Sei-an City (Aristocratic Quarter) - Chest after deluge": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 1),
            required_items_events=["Sei-an City (Aristocratic Quarter) - Mourn Himiko"],
            progress_type=LocationProgressType.EXCLUDED),
        "Sei-an City (Aristocratic Quarter) - Nuregami (Deluge)": LocData(
            brush_check_id(14),
            required_items_events=["Sei-an City (Aristocratic Quarter) - Mourn Himiko"],
            progress_type=LocationProgressType.EXCLUDED)
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
        "Sei-an City (Aristocratic Quarter) - East freestanding chest inside Himiko's east treasure room": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 12)),
    },
    RegionNames.SEIAN_CITY_ARISTOCRATIC: {
        "Sei-an City (Aristocratic Quarter) - Chest in Canal near easter water wheel": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 42), type=LocationType.UNDERWATER_CHEST_SHALLOW),
        "Sei-an City (Aristocratic Quarter) - Chest in Canal near western water wheel": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 30), type=LocationType.UNDERWATER_CHEST_SHALLOW),
        "Sei-an City (Aristocratic Quarter) - Freestanding chest west of bridge gate": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 28)),
        "Sei-an City (Aristocratic Quarter) - Buried chest west of bridge gate": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 29), type=LocationType.BURIED_CHEST),
        "Sei-an City (Aristocratic Quarter) - Buried chest east of bridge gate": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 15), type=LocationType.BURIED_CHEST),
        "Sei-an City (Aristocratic Quarter) - Freestanding chest near guard house": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 23)),
        "Sei-an City (Aristocratic Quarter) - Buried chest near guard house": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 24), type=LocationType.BURIED_CHEST)
    },
    RegionNames.SEIAN_CITY_GUARDS: {
        "Sei-an City (Aristocratic Quarter) - Chest inside guard house": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 45))
    },
    RegionNames.SEIAN_CITY_LAKE: {
        "Sei-an City (Aristocratic Quarter) - Underwater chest in Lake Beewa": LocData(
            container_check_id(MapIds.SEIAN_ARISTORATIC, 43)
        )
    }
}
warps = {
    RegionNames.SEIAN_CITY_ARISTOCRATIC: [
        WarpData(WarpType.MERMAID_SPRING, Has("Imperial Palace - Defeat Blight"),
                 Has("Imperial Palace - Defeat Blight"))
    ]
}
