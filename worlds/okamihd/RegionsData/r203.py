from typing import TYPE_CHECKING

from BaseClasses import LocationProgressType
from rule_builder.rules import Has
from ..CheckIds import container_check_id, shop_check_id, brush_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.WarpType import WarpType
from ..Types import LocData, EventData, ExitData, WarpData
from ..Enums.RegionNames import RegionNames, MapIds

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.DRAGON_PALACE: [
        ExitData(RegionNames.DRAGON_PALACE_SPRING, one_way=True,
                 has_events=["Dragon Palace - Get Shell Amulet from Otohime"]),
        ExitData(RegionNames.DRAGON_PALACE_GARDEN, one_way=True,
                 has_events=["Dragon Palace - Get Shell Amulet from Otohime"]),
        ExitData(RegionNames.DRAGON_PALACE_CAVE, has_events=["Dragon Palace - Open Treasure Cave behind stairs"])
    ],
    RegionNames.DRAGON_PALACE_SPRING: [
        ExitData(RegionNames.DRAGON_PALACE, one_way=True)
    ],
    RegionNames.DRAGON_PALACE_GARDEN: [
        ExitData(RegionNames.DRAGON_PALACE, one_way=True)
    ]
}
events = {
    RegionNames.DRAGON_PALACE: {
        "Dragon Palace - Open Treasure Cave behind stairs": EventData(cherry_bomb_level=1),
        # FIXME: This should give shell amulet, and it should be removed from pool since it can't be picked up rn
        # FIXME: Change this to a location later
        "Dragon Palace - Get Shell Amulet from Otohime": EventData()
    },
    RegionNames.DRAGON_PALACE_SPRING: {
        "Dragon Palace - Restore the soothing spring": EventData(type=LocationType.DIGGING_MINIGAME_HARD,
                                                                 required_items_events=["Digging Champ"])
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
                                                   required_items_events=["Holy Eagle"]),
        "Dragon Palace - Nuregami (Fountain)": LocData(brush_check_id(16), required_items_events=[
            "Dragon Palace - Restore the soothing spring"]),
        # FIXME: This chest doesn't have a cotnainer id !
        "Dragon Palace - Chest after fountain": LocData(1001, required_items_events=[
            "Dragon Palace - Restore the soothing spring"], progress_type=LocationProgressType.EXCLUDED)
    },
    RegionNames.DRAGON_PALACE_GARDEN: {
        "Dragon Palace - East Clam in garden": LocData(container_check_id(MapIds.DRAGON_PALACE, 8)),
        "Dragon Palace - North Clam in garden": LocData(container_check_id(MapIds.DRAGON_PALACE, 7)),
        "Dragon Palace - North Clam on ledge in garden": LocData(container_check_id(MapIds.DRAGON_PALACE, 6)),
        "Dragon Palace - Chest after blooming the dragon's remains": LocData(
            container_check_id(MapIds.DRAGON_PALACE, 0), required_brush_techniques=[BrushTechniques.GREENSPROUT_BLOOM])
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
warps = {
    RegionNames.DRAGON_PALACE_SPRING: [
        WarpData(WarpType.MERMAID_SPRING, Has("Dragon Palace - Restore the soothing spring"),
                 Has("Dragon Palace - Restore the soothing spring"))
    ]
}
