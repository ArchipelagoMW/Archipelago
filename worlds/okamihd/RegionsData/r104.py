from typing import TYPE_CHECKING

from ..CheckIds import brush_check_id, container_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.OkamiEnemies import OkamiEnemies
from ..Enums.RegionNames import RegionNames, MapIds
from ..Types import ExitData, LocData, EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.TSUTA_RUINS_1F_MAIN_PART: [
        ExitData(RegionNames.TSUTA_RUINS_MUSHROOMS,
                 has_events=["Tsuta Ruins - Mandatory Single Ogre Fight"]
                 ,loading_screen=False),
        ExitData(RegionNames.TSUTA_RUINS_LEFT_SIDE,
                 has_events=["Tsuta Ruins - Defeat Blockhead"],loading_screen=False),
        ExitData(RegionNames.TSUTA_RUINS_CENTRAL_STATUE,
                 has_events=["Tsuta Ruins - Destroy Poison Pots"])
    ],
    RegionNames.TSUTA_RUINS_MUSHROOMS: [
        ExitData(RegionNames.TSUTA_RUINS_LEFT_SIDE,
                 has_events=["Tsuta Ruins - Blow up weakened wall above Mushrooms"],one_way=True,loading_screen=False)
    ],
    RegionNames.TSUTA_RUINS_LEFT_SIDE: [
        ExitData(RegionNames.TSUTA_RUINS_DEVIL_GATES,
                 has_events=["Tsuta Ruins - Restore Bridge to Devil Gates' room"],loading_screen=False)
    ],
    RegionNames.TSUTA_RUINS_CENTRAL_STATUE: [
        ExitData(RegionNames.TSUTA_RUINS_SPIDER,
                 has_events=["Tsuta Ruins - Open the top of the statue"])
    ]
}
events = {
    RegionNames.TSUTA_RUINS_1F_MAIN_PART: {
        "Tsuta Ruins - Mandatory Single Ogre Fight": EventData(mandatory_enemies=[OkamiEnemies.BUD_OGRE])
    },
    RegionNames.TSUTA_RUINS_MUSHROOMS: {
        "Tsuta Ruins - Mandatory Double Ogre Fight": EventData(mandatory_enemies=[OkamiEnemies.BUD_OGRE]),
        "Tsuta Ruins - Grow the Mushrooms": EventData(required_brush_techniques=[BrushTechniques.SUNRISE],
                                                      required_items_events=[
                                                          "Tsuta Ruins - Mandatory Double Ogre Fight"]),
        "Tsuta Ruins - Blow up weakened wall above Mushrooms": EventData(cherry_bomb_level=1, required_items_events=[
            "Tsuta Ruins - Grow the Mushrooms"])
    },
    RegionNames.TSUTA_RUINS_LEFT_SIDE: {
        # Maybe add a check that Celestial Brush is unlocked to do this, i'm not sure this matters a lot
        "Tsuta Ruins - Defeat Blockhead": EventData(precollected=lambda o:o.RemoveBlockHead),
        "Tsuta Ruins - Open Lockjaw with Exorcising Arrow": EventData(
            required_items_events=["Tsuta Ruins - Defeat Blockhead"]),
        "Tsuta Ruins - Restore Bridge to Devil Gates' room": EventData(
            required_items_events=["Tsuta Ruins - Open Lockjaw with Exorcising Arrow"],
            required_brush_techniques=[BrushTechniques.REJUVENATION])
    },
    RegionNames.TSUTA_RUINS_DEVIL_GATES: {
        "Tsuta Ruins - Defeat Devil Gate 1": EventData(
            mandatory_enemies=[OkamiEnemies.GREEN_IMP, OkamiEnemies.DEAD_FISH]),
        "Tsuta Ruins - Defeat Devil Gate 2": EventData(
            mandatory_enemies=[OkamiEnemies.GREEN_IMP, OkamiEnemies.YELLOW_IMP]),
        "Tsuta Ruins - Defeat Devil Gate 3": EventData(
            mandatory_enemies=[OkamiEnemies.RED_IMP, OkamiEnemies.BUD_OGRE]),
        "Tsuta Ruins - Grow Mushrooms in Devil Gates Room": EventData(
            required_items_events=["Tsuta Ruins - Defeat Devil Gate 1", "Tsuta Ruins - Defeat Devil Gate 2",
                                   "Tsuta Ruins - Defeat Devil Gate 3"],
            required_brush_techniques=[BrushTechniques.SUNRISE]),
        "Tsuta Ruins - Destroy Poison Pots": EventData(
            required_items_events=["Tsuta Ruins - Grow Mushrooms in Devil Gates Room"])
    },
    RegionNames.TSUTA_RUINS_CENTRAL_STATUE: {
        "Tsuta Ruins - Bloom every cursed patch inside statue": EventData(
            required_brush_techniques=[BrushTechniques.GREENSPROUT_BLOOM]),
        "Tsuta Ruins - Open the top of the statue": EventData(
            required_brush_techniques=[BrushTechniques.GREENSPROUT_VINE]),
        "Tsuta Ruins - Defeat the spider queen": EventData(mandatory_enemies=[OkamiEnemies.SPIDER_QUEEN])
    }
}
locations = {
    RegionNames.TSUTA_RUINS_1F_MAIN_PART: {
        "Tsuta Ruins - Treasure Bud in Entrance Hall Left Side": LocData(container_check_id(MapIds.TSUTA_RUINS, 13),type=LocationType.TREASURE_BUD),# spawn_idx=13, Exorcism Slip S
        "Tsuta Ruins - Freestanding Chest at Entrance": LocData(container_check_id(MapIds.TSUTA_RUINS, 17)),  # spawn_idx=17, Travel Guide: Enhancing Divinity
        "Tsuta Ruins - Treasure Bud in Entrance Hall Middle": LocData(container_check_id(MapIds.TSUTA_RUINS, 8), type=LocationType.TREASURE_BUD),  # spawn_idx=8, Traveler's Charm
        "Tsuta Ruins - Treasure Bud in Entrance Hall Right Side": LocData(container_check_id(MapIds.TSUTA_RUINS, 9), type=LocationType.TREASURE_BUD),  # spawn_idx=9, Steel Soul Sake
        "Tsuta Ruins - Chest in Entrance Hall near right side door": LocData(container_check_id(MapIds.TSUTA_RUINS, 26)),  # spawn_idx=26, Vase
        "Tsuta Ruins - Treasure Bud on 1F rightside path before ledge": LocData(container_check_id(MapIds.TSUTA_RUINS, 0), type=LocationType.TREASURE_BUD),  # spawn_idx=12, Steel Fist Sake
        "Tsuta Ruins - Treasure Bud near glass ball": LocData(container_check_id(MapIds.TSUTA_RUINS, 12), type=LocationType.TREASURE_BUD),  # spawn_idx=0, Incense Burner
        "Tsuta Ruins - Stray bead chest on 1F rightside path upper part": LocData(container_check_id(MapIds.TSUTA_RUINS, 15), required_brush_techniques=[
            BrushTechniques.GREENSPROUT_VINE], type=LocationType.TREASURE_BUD),  # spawn_idx=15, Stray Bead
    },
    RegionNames.TSUTA_RUINS_MUSHROOMS: {
        "Tsuta Ruins - Treasure bud behind logs in Mushrooms room": LocData(container_check_id(MapIds.TSUTA_RUINS, 2), power_slash_level=1,
                                                                            type=LocationType.TREASURE_BUD),  # spawn_idx=2, Vengeance Slip
    },
    RegionNames.TSUTA_RUINS_LEFT_SIDE: {
        "Tsuta Ruins - Treasure Bud behind hidden bombable wall on third plaform.": LocData(container_check_id(MapIds.TSUTA_RUINS, 1), cherry_bomb_level=1,
                                                                                            type=LocationType.TREASURE_BUD),  # spawn_idx=1, Stray Bead
        "Tsuta Ruins - Treasure Bud behind Lockjaw": LocData(container_check_id(MapIds.TSUTA_RUINS, 4), type=LocationType.TREASURE_BUD, required_items_events=[
            "Tsuta Ruins - Open Lockjaw with Exorcising Arrow"]),  # spawn_idx=4, Exorcism Slip S
        "Tsuta Ruins - Left side hidden treasure bud": LocData(container_check_id(MapIds.TSUTA_RUINS, 18), required_brush_techniques=[
            BrushTechniques.GREENSPROUT_VINE], type=LocationType.TREASURE_BUD),  # spawn_idx=18, Golden Peach
        "Tsuta Ruins - Ledge Chest behind lockjaw": LocData(container_check_id(MapIds.TSUTA_RUINS, 35),required_items_events=["Tsuta Ruins - Defeat the spider queen"]), # spawn_idx=35, Bull Horn

    },
    RegionNames.TSUTA_RUINS_DEVIL_GATES: {
        "Tsuta Ruins - Treasure Bud near Devil gates": LocData(container_check_id(MapIds.TSUTA_RUINS, 23), type=LocationType.TREASURE_BUD),  # spawn_idx=23, Lacquerware Set
        "Tsuta Ruins - Treasure Bud #2 near Devil gates": LocData(container_check_id(MapIds.TSUTA_RUINS, 24), type=LocationType.TREASURE_BUD),  # spawn_idx=24, Holy Bone S
        "Tsuta Ruins - Map Chest near poison pots": LocData(container_check_id(MapIds.TSUTA_RUINS, 34), required_items_events=[
            "Tsuta Ruins - Grow Mushrooms in Devil Gates Room"]),  # spawn_idx=34, Tsuta Ruins Map
        "Tsuta Ruins - Treasure Bud behind waterfall bombable wall": LocData(container_check_id(MapIds.TSUTA_RUINS, 25), required_items_events=[
            "Tsuta Ruins - Destroy Poison Pots"], cherry_bomb_level=1, type=LocationType.TREASURE_BUD),  # spawn_idx=25, Stray Bead
    },
    RegionNames.TSUTA_RUINS_CENTRAL_STATUE: {
        "Tsuta Ruins - Tsutagami": LocData(brush_check_id(19), required_items_events=[
            "Tsuta Ruins - Bloom every cursed patch inside statue"], type=LocationType.CONSTELLATION),  # Brush acquisition (Vine, bit 19)
    },
    RegionNames.TSUTA_RUINS_SPIDER: {
        "Tsuta Ruins - Left Chest before Spider queen": LocData(container_check_id(MapIds.TSUTA_RUINS, 21)),  # spawn_idx=21, Travel Guide: Godhood Tips
        "Tsuta Ruins - Right Chest before Spider queen": LocData(container_check_id(MapIds.TSUTA_RUINS, 22)),  # spawn_idx=22, Holy Bone S
        "Tsuta Ruins - Boss reward": LocData(container_check_id(MapIds.TSUTA_RUINS, 36), required_items_events=["Tsuta Ruins - Defeat the spider queen"]),  # spawn_idx=35, Bull Horn
    }
}
