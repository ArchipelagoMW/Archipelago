from typing import TYPE_CHECKING

from ..CheckIds import container_check_id, shop_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Types import LocData, EventData, ExitData
from ..Enums.RegionNames import RegionNames, MapIds

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.DRAGON_PALACE: [
        ExitData(RegionNames.DRAGON_PALACE_SPRING, one_way=True,
                 has_events=["Dragon Palace - Get Shell Amulet from Otohime"])
    ],
    RegionNames.DRAGON_PALACE_SPRING: [
        ExitData(RegionNames.DRAGON_PALACE, one_way=True)
    ]
}
events = {
    RegionNames.DRAGON_PALACE: {
        "Dragon Palace - Open Secret Cave": EventData(cherry_bomb_level=1),
        # FIXME: Change this to a location later
        "Dragon Palace - Get Shell Amulet from Otohime": EventData(),
    },
    RegionNames.DRAGON_PALACE_SPRING:{
        "Dragon Palace - Restore the soothing spring":EventData(type=LocationType.DIGGING_MINIGAME_LATER,required_items_events=["Digging Champ"])
    }
}
locations = {
    RegionNames.DRAGON_PALACE: {
        "Dragon Palace - West Clam at entrance 1": LocData(container_check_id(MapIds.DRAGON_PALACE, 3)),
        "Dragon Palace - West Clam at entrance 2": LocData(container_check_id(MapIds.DRAGON_PALACE, 4)),
        "Dragon Palace - East Clam at entrance": LocData(container_check_id(MapIds.DRAGON_PALACE, 5)),
        "Dragon Palace - Chest inside guardhouse": LocData(container_check_id(MapIds.DRAGON_PALACE, 1))
    },
    RegionNames.DRAGON_PALACE_SPRING: {
        "Dragon Palace - North Clam near Soothing Spring": LocData(container_check_id(MapIds.DRAGON_PALACE, 10)),
        "Dragon Palace - West Clam near Soothing Spring": LocData(container_check_id(MapIds.DRAGON_PALACE, 9)),
        "Dragon Palace -Chest on Pillars": LocData(container_check_id(MapIds.DRAGON_PALACE, 2),
                                                   required_brush_techniques=[BrushTechniques.REJUVENATION],
                                                   required_items_events=["Holy Eagle"])
    }
}
shop_locations = {
    RegionNames.DRAGON_PALACE: {
        "Dragon Palace - Ms. Turtle's Shop Slot 1": LocData(shop_check_id(3, 0), type=LocationType.SHOP),
        "Dragon Palace - Ms. Turtle's Shop Slot 2": LocData(shop_check_id(3, 1), type=LocationType.SHOP),
        "Dragon Palace - Ms. Turtle's Shop Slot 3": LocData(shop_check_id(3, 2), type=LocationType.SHOP),
        "Dragon Palace - Ms. Turtle's Shop Slot 4": LocData(shop_check_id(3, 3), type=LocationType.SHOP),
        "Dragon Palace - Ms. Turtle's Shop Slot 5": LocData(shop_check_id(3, 4), type=LocationType.SHOP),
        "Dragon Palace - Ms. Turtle's Shop Slot 6": LocData(shop_check_id(3, 5), type=LocationType.SHOP),
        "Dragon Palace - Ms. Turtle's Shop Slot 7": LocData(shop_check_id(3, 6), type=LocationType.SHOP),
        "Dragon Palace - Ms. Turtle's Shop Slot 8": LocData(shop_check_id(3, 7), type=LocationType.SHOP),
        "Dragon Palace - Ms. Turtle's Shop Slot 9": LocData(shop_check_id(3, 8), type=LocationType.SHOP),
        "Dragon Palace - Ms. Turtle's Shop Slot 10": LocData(shop_check_id(3, 9), type=LocationType.SHOP),
        "Dragon Palace - Ms. Turtle's Shop Slot 11": LocData(shop_check_id(3, 10), type=LocationType.SHOP),
        "Dragon Palace - Ms. Turtle's Shop Slot 12": LocData(shop_check_id(3, 11), type=LocationType.SHOP)
    }
}
warps={

}