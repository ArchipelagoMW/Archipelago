from typing import TYPE_CHECKING

from ..CheckIds import container_check_id, brush_check_id, shop_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.OkamiEnemies import OkamiEnemies
from ..Enums.RegionNames import RegionNames, MapIds
from ..Types import ExitData, LocData, EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.SUNKEN_SHIP_ENTRANCE: [
        ExitData(RegionNames.SUNKEN_SHIP_SW_LOW, has_events=["Sunken Ship - Open entrance Door"]
                 , loading_screen=False),
    ],
    RegionNames.SUNKEN_SHIP_SW_LOW: [
        ExitData(RegionNames.SUNKEN_SHIP_BONES_LOW, loading_screen=False)
    ],
    RegionNames.SUNKEN_SHIP_BONES_LOW: [
        ExitData(RegionNames.SUNKEN_SHIP_NW_LOW, loading_screen=False,
                 has_events=["Sunken Ship - Open Northwest cursed door"])
    ],
    RegionNames.SUNKEN_SHIP_NW_LOW: [
        ExitData(RegionNames.SUNKEN_SHIP_NW_HIGH, one_way=True, loading_screen=False,
                 has_events=["Sunken Ship - Raise water level"]),
        ExitData(RegionNames.SUNKEN_SHIP_HANDS_LOW, one_way=True, loading_screen=False,
                 has_events=["Sunken Ship - Set barrel on Scales"])
    ],
    RegionNames.SUNKEN_SHIP_NW_HIGH: [
        ExitData(RegionNames.SUNKEN_SHIP_NW_LOW, one_way=True, loading_screen=False,
                 has_events=["Sunken Ship - Drain water level"]),
        ExitData(RegionNames.SUNKEN_SHIP_BONES_HIGH, loading_screen=False,
                 has_events=["Sunken Ship - Open Northwest cursed door"])
    ],
    RegionNames.SUNKEN_SHIP_BONES_HIGH: [
        ExitData(RegionNames.SUNKEN_SHIP_SW_HIGH, has_events=["Sunken Ship - Mandatory Ichiro fight"])
    ],
    RegionNames.SUNKEN_SHIP_SW_HIGH: [
        ExitData(RegionNames.SUNKEN_SHIP_SE_HIGH, loading_screen=False, one_way=True),
        ExitData(RegionNames.SUNKEN_SHIP_S_LEDGE, loading_screen=False, one_way=True)
    ],
    RegionNames.SUNKEN_SHIP_SE_HIGH: [
        ExitData(RegionNames.SUNKEN_SHIP_E_HALLWAY_HIGH, loading_screen=False),
        ExitData(RegionNames.SUNKEN_SHIP_SE_CHESTS, one_way=True, loading_screen=False, needs_long_swim=True),
        ExitData(RegionNames.SUNKEN_SHIP_SW_HIGH, loading_screen=False, one_way=True, needs_long_swim=True),
        ExitData(RegionNames.SUNKEN_SHIP_S_LEDGE, loading_screen=False, one_way=True, needs_long_swim=True)
    ],
    RegionNames.SUNKEN_SHIP_SE_LOW: [
        ExitData(RegionNames.SUNKEN_SHIP_SE_CHESTS, one_way=True, loading_screen=False),
        ExitData(RegionNames.SUNKEN_SHIP_SW_LOW, one_way=True, loading_screen=False,
                 has_events=["Sunken Ship - climb Waterspout pillar to southwest room"]),
        ExitData(RegionNames.SUNKEN_SHIP_S_LEDGE, loading_screen=False, one_way=True,
                 has_events=["Sunken Ship - climb Waterspout pillar to southwest room"]),
        ExitData(RegionNames.SUNKEN_SHIP_TREASURE, loading_screen=False,
                 has_events=["Sunken Ship - Open final cursed door"])
    ],
    RegionNames.SUNKEN_SHIP_E_HALLWAY_HIGH: [
        ExitData(RegionNames.SUNKEN_SHIP_HANDS_HIGH, loading_screen=False)
    ],
    RegionNames.SUNKEN_SHIP_HANDS_HIGH: [
        ExitData(RegionNames.SUNKEN_SHIP_NW_HIGH, loading_screen=False, one_way=True)
    ],
    RegionNames.SUNKEN_SHIP_HANDS_LOW: [
        ExitData(RegionNames.SUNKEN_SHIP_NW_LOW, one_way=True, loading_screen=False),
        ExitData(RegionNames.SUNKEN_SHIP_E_HALLWAY_LOW, loading_screen=False)
    ],
    RegionNames.SUNKEN_SHIP_E_HALLWAY_LOW: [
        ExitData(RegionNames.SUNKEN_SHIP_SE_LOW, loading_screen=False)
    ]

}
events = {
    RegionNames.SUNKEN_SHIP_ENTRANCE: {
        "Sunken Ship - Rao climbs on Ama's back": EventData(
            required_items_events=["Sei-an City (Aristocratic Quarter) - Give Prayer Slips to Rao"]),
        "Sunken Ship - Open entrance Door": EventData(required_items_events=["Sunken Ship - Rao climbs on Ama's back"])
    },
    RegionNames.SUNKEN_SHIP_SW_LOW: {
        "Sunken Ship - Mandatory Jiro & Saburo fight": EventData(
            mandatory_enemies=[OkamiEnemies.JIRO, OkamiEnemies.SABURO]),
        "Sunken Ship - Open Northwest cursed door": EventData(
            required_items_events=["Sunken Ship - Rao climbs on Ama's back",
                                   "Sunken Ship - Mandatory Jiro & Saburo fight"])
    },
    RegionNames.SUNKEN_SHIP_NW_LOW: {
        "Sunken Ship - Raise water level": EventData(required_brush_techniques=[BrushTechniques.SUNRISE])
    },
    RegionNames.SUNKEN_SHIP_NW_HIGH: {
        "Sunken Ship - Drain water level": EventData(required_brush_techniques=[BrushTechniques.CRESCENT])
    },
    RegionNames.SUNKEN_SHIP_BONES_HIGH: {
        "Sunken Ship - Mandatory Ichiro fight": EventData(mandatory_enemies=[OkamiEnemies.ICHIRO])
    },
    RegionNames.SUNKEN_SHIP_SE_HIGH: {
        "Sunken Ship - use Cannon in southeast room (High water) ": EventData(cherry_bomb_level=1,
                                                                              event_item_name="Sunken Ship - use Cannon in southeast room")
    },
    RegionNames.SUNKEN_SHIP_SE_LOW: {
        "Sunken Ship - use Cannon in southeast room (Low water) ": EventData(cherry_bomb_level=1,
                                                                             event_item_name="Sunken Ship - use Cannon in southeast room"),
        "Sunken Ship - climb Waterspout pillar to southwest room": EventData(
            required_brush_techniques=[BrushTechniques.WATERSPOUT]),
        "Sunken Ship - Open lockjaw": EventData(required_items_events=["Sunken Ship - use Cannon in southeast room"]),
        "Sunken Ship - Open final cursed door": EventData(
            required_items_events=["Sunken Ship - Open lockjaw", "Sunken Ship - Rao climbs on Ama's back"])
    },
    RegionNames.SUNKEN_SHIP_HANDS_HIGH: {
        "Sunken Ship - Set barrel on Scales": EventData(power_slash_level=1)
    }
}
locations = {
    RegionNames.SUNKEN_SHIP_SW_LOW: {
        "Sunken Ship - Chest in Southwest room 1": LocData(container_check_id(MapIds.SUNKEN_SHIP, 1)),
        "Sunken Ship - Chest in Southwest room 2": LocData(container_check_id(MapIds.SUNKEN_SHIP, 0)),
        "Sunken Ship - Chest in Southwest room 3": LocData(container_check_id(MapIds.SUNKEN_SHIP, 2)),
    },
    RegionNames.SUNKEN_SHIP_SE_CHESTS: {
        # Check if these are accessible in low water with holy eagle
        "Sunken Ship - Lower Chest in Southeast room behind canon walls": LocData(
            container_check_id(MapIds.SUNKEN_SHIP, 12),
            required_items_events=["Sunken Ship - use Cannon in southeast room"]),
        "Sunken Ship - Higher Chest in Southeast room behind canon walls": LocData(
            container_check_id(MapIds.SUNKEN_SHIP, 4),
            required_items_events=["Sunken Ship - use Cannon in southeast room"]),
    },
    RegionNames.SUNKEN_SHIP_E_HALLWAY_HIGH: {
        "Sunken Ship - Southern chest in eastern hallway": LocData(container_check_id(MapIds.SUNKEN_SHIP, 5)),
        "Sunken Ship - Northern chest in eastern hallway": LocData(container_check_id(MapIds.SUNKEN_SHIP, 6))
    },
    RegionNames.SUNKEN_SHIP_HANDS_HIGH: {
        "Sunken Ship - Chest on ledge in hands room": LocData(container_check_id(MapIds.SUNKEN_SHIP, 11))
    },
    RegionNames.SUNKEN_SHIP_TREASURE: {
        "Sunken Ship - Chest in treasure room 1": LocData(container_check_id(MapIds.SUNKEN_SHIP, 9)),
        # Vanilla Lucky mallet,triggers a cutscene
        "Sunken Ship - Chest in treasure room 2": LocData(container_check_id(MapIds.SUNKEN_SHIP, 7)),
        "Sunken Ship - Chest in treasure room 3": LocData(container_check_id(MapIds.SUNKEN_SHIP, 8))
    },
    RegionNames.SUNKEN_SHIP_S_LEDGE: {
        "Sunken Ship - Chest in southern central ledge": LocData(container_check_id(MapIds.SUNKEN_SHIP, 10))
    }

}
