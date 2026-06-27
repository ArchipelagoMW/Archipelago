from typing import TYPE_CHECKING

from BaseClasses import LocationProgressType
from rule_builder.rules import HasAny
from ..CheckIds import container_check_id, brush_check_id, shop_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.OkamiEnemies import OkamiEnemies
from ..Enums.RegionNames import RegionNames, MapIds
from ..Rules import oni_island_1f_thunder_rule
from ..Types import ExitData, LocData, EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.ONI_ISLAND_INTERIOR_ENTRANCE_ROOM: [
        ExitData(RegionNames.ONI_ISLAND_INTERIOR_PRE_TOBI_1, loading_screen=False,
                 required_items_events=["Oni Island - 1F Defeat Poltergeists to get Key"]),
        ExitData(RegionNames.ONI_ISLAND_INTERIOR_1F_WEST_ROOM, loading_screen=False,
                 required_items_events=["Oni Island - 1F Open West room thunder door"]),
        ExitData(RegionNames.ONI_ISLAND_INTERIOR_1F_STATUE, loading_screen=False,
                 required_items_events=["Oni Island - 1F Open Gate with Thunder Key"])
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
                 required_items_events=["Oni Island - Tobi race #3 (Terraced Passage)"])
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
    ],
    RegionNames.ONI_ISLAND_INTERIOR_LASER_BRIDGES: [
        ExitData(RegionNames.ONI_ISLAND_INTERIOR_POST_TOBI_7, loading_screen=False,
                 required_items_events=["Oni Island - Tobi race #7 (Passage of Needles)"])
    ],
    RegionNames.ONI_ISLAND_INTERIOR_POST_TOBI_7: [
        ExitData(RegionNames.ONI_ISLAND_EXTERIOR_ROOF,
                 required_items_events=["Oni Island - 3F Blow up wall to exterior roof"]),
        ExitData(RegionNames.ONI_ISLAND_INTERIOR_3F_POST_LOCKJAW, loading_screen=False,
                 required_items_events=["Oni Island - 3F Open Lockjaw"])
    ],
    RegionNames.ONI_ISLAND_INTERIOR_3F_POST_LOCKJAW: [
        ExitData(RegionNames.ONI_ISLAND_INTERIOR_3F_POST_GEKIGAMI, loading_screen=False,
                 required_items_events=["Oni Island - 3F Open thunder door after Gekigami"])
    ],
    RegionNames.ONI_ISLAND_INTERIOR_3F_POST_GEKIGAMI: [
        ExitData(RegionNames.ONI_ISLAND_INTERIOR_1F_THUNDER_KEY, loading_screen=False, one_way=True,
                 required_items_events=["Oni Island - 3F Blow up floor after Gekigami"])
    ],
    RegionNames.ONI_ISLAND_INTERIOR_1F_THUNDER_KEY: [
        ExitData(RegionNames.ONI_ISLAND_INTERIOR_1F_SLIDING_DOORS, loading_screen=False,
                 required_items_events=["Oni Island - 1F Open Thunder Door after fist thunder Key"])
    ],
    RegionNames.ONI_ISLAND_INTERIOR_1F_SLIDING_DOORS: [
        ExitData(RegionNames.ONI_ISLAND_INTERIOR_ENTRANCE_ROOM, loading_screen=False,
                 required_items_events=["Oni Island - 1F Blow up wall to exit maze"])
    ],
    RegionNames.ONI_ISLAND_INTERIOR_1F_STATUE: [
        ExitData(RegionNames.ONI_ISLAND_INTERIOR_B1F_ALARM, loading_screen=False,
                 required_items_events=["Oni Island - 1F Blow up Statue"])
    ]

}
events = {
    RegionNames.ONI_ISLAND_INTERIOR_ENTRANCE_ROOM: {
        "Oni Island - 1F Defeat Poltergeists to get Key": EventData(mandatory_enemies=[OkamiEnemies.POLTERGEIST]),
        "Oni Island - 1F Open West room thunder door": EventData(special_rule=oni_island_1f_thunder_rule),
        "Oni Island - 1F Open Gate with Thunder Key": EventData(
            required_items_events=["Oni Island - 1F Grab First Thunder Key"])
    },
    RegionNames.ONI_ISLAND_INTERIOR_PRE_TOBI_1: {
        "Oni Island - Tobi Race #1 (Simple Door)": EventData(),
    },
    RegionNames.ONI_ISLAND_INTERIOR_TOBI_1_2: {
        "Oni Island - Tobi Race #2 (Spike Platforms)": EventData(),
    },
    RegionNames.ONI_ISLAND_INTERIOR_TOBI_2_3: {
        "Oni Island - B2F Climb to 1F": EventData(required_brush_techniques=[BrushTechniques.CATWALK]),
        "Oni Island - Tobi race #3 (Terraced Passage)": EventData(
            required_items_events=["Oni Island - B2F Climb to 1F"])
    },
    RegionNames.ONI_ISLAND_INTERIOR_TOBI_3_4: {
        # Might be doable without but probably a pain
        "Oni Island - Tobi race #4 (Passage of Saws)": EventData(required_items_events=["Holy Eagle"])
    },
    RegionNames.ONI_ISLAND_INTERIOR_TOBI_4_5: {
        "Oni Island - Tobi race #5 (Demonic Wheels)": EventData(required_items_events=["Holy Eagle"])
    },
    RegionNames.ONI_ISLAND_INTERIOR_TOBI_5_6: {
        "Oni Island - Tobi race #6 (Chamber of Delay)": EventData(mandatory_enemies=[OkamiEnemies.HEADLESS_GUARDIAN])
    },
    RegionNames.ONI_ISLAND_INTERIOR_LASER_BRIDGES: {
        "Oni Island - 3F Mandatory Blue Ogre Fight": EventData(mandatory_enemies=[OkamiEnemies.BLUE_OGRE]),
        "Oni Island - Tobi race #7 (Passage of Needles)": EventData(
            required_items_events=["Oni Island - 3F Mandatory Blue Ogre Fight"])
    },
    RegionNames.ONI_ISLAND_INTERIOR_POST_TOBI_7: {
        "Oni Island - 3F Blow up wall to exterior roof": EventData(cherry_bomb_level=1),
        "Oni Island - 3F Open Lockjaw": EventData(required_items_events=["Oni Island - Grab Key on the roof"]),
    },
    RegionNames.ONI_ISLAND_INTERIOR_3F_POST_LOCKJAW: {
        # Thunderstrom tutorial
        "Oni Island - 3F Open thunder door after Gekigami": EventData(
            required_items_events=[BrushTechniques.THUNDERSTORM]),
        "Oni Island - 3F Blow up floor after Gekigami": EventData(cherry_bomb_level=1)
    },
    RegionNames.ONI_ISLAND_INTERIOR_1F_THUNDER_KEY: {
        "Oni Island - 1F Grab First Thunder Key": EventData(),
        "Oni Island - 1F Climb to thunder Door": EventData(
            special_rule=HasAny("Oni Island - 1F Grab First Thunder Key", BrushTechniques.GREENSPROUT_VINE)),
        "Oni Island - 1F Open Thunder Door after fist thunder Key": EventData(special_rule=oni_island_1f_thunder_rule)
    },
    RegionNames.ONI_ISLAND_INTERIOR_1F_SLIDING_DOORS: {
        "Oni Island - 1F Blow up wall to exit maze": EventData(cherry_bomb_level=1)
    },
    RegionNames.ONI_ISLAND_INTERIOR_1F_STATUE: {
        "Oni Island - 1F Blow up Statue": EventData(required_items_events=[BrushTechniques.THUNDERSTORM])
    },
    RegionNames.ONI_ISLAND_INTERIOR_B1F_ALARM:{
        "Oni Island - B1F Cut alarm": EventData(power_slash_level=1)
    }
}
locations = {
    RegionNames.ONI_ISLAND_INTERIOR_PRE_TOBI_1: {
        "Oni Island - 1F Chest above West stairs to B2F": LocData(container_check_id(MapIds.ONI_ISLAND_LOWER_INT, 2),
                                                                  required_items_events=["Holy Eagle"]),
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
        "Oni Island - 3F Right Chest in Labyrinth of Torment": LocData(
            container_check_id(MapIds.ONI_ISLAND_LOWER_INT, 23)),
        "Oni Island - 3F Left Chest Labyrinth of Torment": LocData(container_check_id(MapIds.ONI_ISLAND_LOWER_INT, 22))
    },
    RegionNames.ONI_ISLAND_INTERIOR_3F_POST_LOCKJAW: {
        "Oni Island - 3F Chest in Spike Room": LocData(container_check_id(MapIds.ONI_ISLAND_LOWER_INT, 24)),
        "Oni Island - Gekigami": LocData(brush_check_id(8), required_brush_techniques=[BrushTechniques.REJUVENATION])
    },
    RegionNames.ONI_ISLAND_INTERIOR_3F_POST_GEKIGAMI: {
        "Oni Island - 3F Thunder Chest after Gekigami": LocData(container_check_id(MapIds.ONI_ISLAND_LOWER_INT, 21),
                                                                type=LocationType.THUNDER_CHEST)
    },
    # see https://gamefaqs.gamespot.com/ps2/920500-okami/map/3932-oni-island-sliding-doors-of-hell-map

    RegionNames.ONI_ISLAND_INTERIOR_1F_SLIDING_DOORS: {
        "Oni Island - 1F Chest in Sliding Door Maze #1 (of 11)": LocData(
            container_check_id(MapIds.ONI_ISLAND_LOWER_INT, 6)),
        "Oni Island - 1F Chest in Sliding Door Maze #2 (of 11)": LocData(
            container_check_id(MapIds.ONI_ISLAND_LOWER_INT, 9)),
        "Oni Island - 1F Chest in Sliding Door Maze #3 (of 11)": LocData(
            container_check_id(MapIds.ONI_ISLAND_LOWER_INT, 7)),
        "Oni Island - 1F Chest in Sliding Door Maze #4 (of 11)": LocData(
            container_check_id(MapIds.ONI_ISLAND_LOWER_INT, 5)),
        "Oni Island - 1F Chest in Sliding Door Maze #5 (of 11)": LocData(
            container_check_id(MapIds.ONI_ISLAND_LOWER_INT, 8)),
        "Oni Island - 1F Chest in Sliding Door Maze #6 (of 11)": LocData(
            container_check_id(MapIds.ONI_ISLAND_LOWER_INT, 10)),
        "Oni Island - 1F Chest in Sliding Door Maze #7 (of 11)": LocData(
            container_check_id(MapIds.ONI_ISLAND_LOWER_INT, 11)),
        "Oni Island - 1F Chest in Sliding Door Maze #8 (of 11)": LocData(
            container_check_id(MapIds.ONI_ISLAND_LOWER_INT, 12)),
        "Oni Island - 1F Chest in Sliding Door Maze #9 (of 11)": LocData(
            container_check_id(MapIds.ONI_ISLAND_LOWER_INT, 15)),
        "Oni Island - 1F Chest in Sliding Door Maze #10 (of 11)": LocData(
            container_check_id(MapIds.ONI_ISLAND_LOWER_INT, 13)),
        "Oni Island - 1F Chest in Sliding Door Maze #11 (of 11)": LocData(
            container_check_id(MapIds.ONI_ISLAND_LOWER_INT, 14)),
    },
    RegionNames.ONI_ISLAND_INTERIOR_1F_WEST_ROOM: {
        "Oni Island - 1F Chest in West Room": LocData(container_check_id(MapIds.ONI_ISLAND_LOWER_INT, 16))
    },
    RegionNames.ONI_ISLAND_INTERIOR_1F_STATUE: {
        "Oni Island - 1F Left Thunder chest before statue": LocData(container_check_id(MapIds.ONI_ISLAND_LOWER_INT, 1),
                                                                    type=LocationType.THUNDER_CHEST),
        "Oni Island - 1F Right Thunder chest before statue": LocData(container_check_id(MapIds.ONI_ISLAND_LOWER_INT, 0),
                                                                     type=LocationType.THUNDER_CHEST),
        "Oni Island - 1F Left chest in front of statue": LocData(container_check_id(MapIds.ONI_ISLAND_LOWER_INT, 18)),
        "Oni Island - 1F Right chest in front of statue": LocData(container_check_id(MapIds.ONI_ISLAND_LOWER_INT, 17)),
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
