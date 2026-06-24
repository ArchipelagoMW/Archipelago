from typing import TYPE_CHECKING

from BaseClasses import LocationProgressType
from ..CheckIds import container_check_id, brush_check_id, shop_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.OkamiEnemies import OkamiEnemies
from ..Enums.RegionNames import RegionNames, MapIds
from ..Types import ExitData, LocData, EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.ONI_ISLAND_INTERIOR_ENTRANCE_ROOM: [
        ExitData(RegionNames.ONI_ISLAND_INTERIOR_PRE_TOBI_1, loading_screen=False,
                 required_items_events=["Oni Island - Defeat Poltergeists to get Key"])
    ],
    RegionNames.ONI_ISLAND_INTERIOR_PRE_TOBI_1: [
        ExitData(RegionNames.ONI_ISLAND_INTERIOR_TOBI_1_2, loading_screen=False,
                 required_items_events=["Oni Island - Tobi Race #1 (Simple Door)"]),
    ],
    RegionNames.ONI_ISLAND_INTERIOR_TOBI_1_2: [
        ExitData(RegionNames.ONI_ISLAND_INTERIOR_TOBI_2_3, loading_screen=False,
                 required_items_events=["Oni Island - Tobi Race #2 (Spike Platforms)"])
    ],
    RegionNames.ONI_ISLAND_INTERIOR_TOBI_2_3: [
        ExitData(RegionNames.ONI_ISLAND_INTERIOR_TOBI_3_4, loading_screen=False,
                 required_items_events=["Oni Island - Tobi race #3 (Platforms and ledges)"])
    ],
    RegionNames.ONI_ISLAND_INTERIOR_TOBI_3_4: [
        ExitData(RegionNames.ONI_ISLAND_INTERIOR_TOBI_4_5, loading_screen=False,
                 required_items_events=["Oni Island - Tobi race #4 (Passage of Saws)"])
    ],
    RegionNames.ONI_ISLAND_INTERIOR_TOBI_4_5: [
        ExitData(RegionNames.ONI_ISLAND_INTERIOR_TOBI_5_6, loading_screen=False,
                 required_items_events=["Oni Island - Tobi race #5 (Demonic Wheels)"])
    ],
    RegionNames.ONI_ISLAND_INTERIOR_TOBI_5_6: [
        ExitData(RegionNames.ONI_ISLAND_INTERIOR_LASER_BRIDGES, loading_screen=False,
                 required_items_events=["Oni Island - Tobi race #6 (Chamber of Delay)"])
    ]

}
events = {
    RegionNames.ONI_ISLAND_INTERIOR_ENTRANCE_ROOM: {
        "Oni Island - Defeat Poltergeists to get Key": EventData(mandatory_enemies=[OkamiEnemies.POLTERGEIST]),
    },
    RegionNames.ONI_ISLAND_INTERIOR_PRE_TOBI_1: {
        "Oni Island - Tobi Race #1 (Simple Door)": EventData(),
    },
    RegionNames.ONI_ISLAND_INTERIOR_TOBI_1_2: {
        "Oni Island - Tobi Race #2 (Spike Platforms)": EventData(),
    },
    RegionNames.ONI_ISLAND_INTERIOR_TOBI_2_3: {
        "Oni Island - B2F Climb to 1F": EventData(required_brush_techniques=[BrushTechniques.CATWALK]),
        "Oni Island - Tobi race #3 (Platforms and ledges)": EventData(
            required_items_events=["Oni Island - B2F Climb to 1F"])
    },
    RegionNames.ONI_ISLAND_INTERIOR_TOBI_3_4: {
        # FIXME: Check if this require holy eagle
        "Oni Island - Tobi race #4 (Passage of Saws)": EventData()
    },
    RegionNames.ONI_ISLAND_INTERIOR_TOBI_4_5: {
        "Oni Island - Tobi race #5 (Demonic Wheels)": EventData()
    },
    RegionNames.ONI_ISLAND_INTERIOR_TOBI_5_6: {
        "Oni Island - Tobi race #6 (Chamber of Delay)": EventData(mandatory_enemies=[OkamiEnemies.HEADLESS_GUARDIAN])
    },
    RegionNames.ONI_ISLAND_INTERIOR_LASER_BRIDGES: {
        "Oni Island - 3F Mandatory Blue Ogre Fight" :EventData(mandatory_enemies=[OkamiEnemies.BLUE_OGRE]),
        "Oni Island - Tobi race #7 (Passage of Needles)": EventData(required_items_events=["Oni Island - 3F Mandatory Blue Ogre Fight"])
    }
}
locations = {
    RegionNames.ONI_ISLAND_INTERIOR_PRE_TOBI_1: {
        # FIXME: Check if this require holy eagle
        "Oni Island - 1F Chest above West stairs to B2F": LocData(container_check_id(MapIds.ONI_ISLAND_LOWER_INT, 2)),
    },
    RegionNames.ONI_ISLAND_INTERIOR_TOBI_2_3: {
        "Oni Island - B2F Chest behind stairs after spike room": LocData(
            container_check_id(MapIds.ONI_ISLAND_LOWER_INT, 19))
    },
    RegionNames.ONI_ISLAND_INTERIOR_TOBI_4_5: {
        "Oni Island - 1F Chest after passage of Saws": LocData(container_check_id(MapIds.ONI_ISLAND_LOWER_INT, 3))
    },
    RegionNames.ONI_ISLAND_INTERIOR_TOBI_5_6: {
        "Oni Island - 2F Chest after demonic wheels": LocData(container_check_id(MapIds.ONI_ISLAND_LOWER_INT, 4))
    },
    RegionNames.ONI_ISLAND_INTERIOR_LASER_BRIDGES: {
        "Oni Island - 2F Chest after Chamber of delay": LocData(container_check_id(MapIds.ONI_ISLAND_LOWER_INT, 20)),
        "Oni Island - 3F Right Chest in Labyrinth of Torment": LocData(container_check_id(MapIds.ONI_ISLAND_LOWER_INT, 23)),
        "Oni Island - 3F Left Chest Labyrinth of Torment": LocData(container_check_id(MapIds.ONI_ISLAND_LOWER_INT, 22))
    }
}
shop_locations = {
    RegionNames.ONI_ISLAND_INTERIOR_ENTRANCE_ROOM: {
        "Oni Island - Shop Slot 1": LocData(shop_check_id(12, 0), type=LocationType.SHOP),
        "Oni Island - Shop Slot 2": LocData(shop_check_id(12, 1), type=LocationType.SHOP),
        "Oni Island - Shop Slot 3": LocData(shop_check_id(12, 2), type=LocationType.SHOP),
        "Oni Island - Shop Slot 4": LocData(shop_check_id(12, 3), type=LocationType.SHOP),
        "Oni Island - Shop Slot 5": LocData(shop_check_id(12, 4), type=LocationType.SHOP),
        "Oni Island - Shop Slot 6": LocData(shop_check_id(12, 5), type=LocationType.SHOP),
        "Oni Island - Shop Slot 7": LocData(shop_check_id(12, 6), type=LocationType.SHOP),
        "Oni Island - Shop Slot 8": LocData(shop_check_id(12, 7), type=LocationType.SHOP),
        "Oni Island - Shop Slot 9": LocData(shop_check_id(12, 8), type=LocationType.SHOP),
        "Oni Island - Shop Slot 10": LocData(shop_check_id(12, 9), type=LocationType.SHOP),
        "Oni Island - Shop Slot 11": LocData(shop_check_id(12, 10), type=LocationType.SHOP),
        "Oni Island - Shop Slot 12": LocData(shop_check_id(12, 11), type=LocationType.SHOP)
    },
}
