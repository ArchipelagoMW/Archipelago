from typing import TYPE_CHECKING

from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.OkamiEnnemies import OkamiEnnemies
from ..Enums.RegionNames import RegionNames
from ..Types import ExitData, LocData, EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.TSUTA_RUINS_1F_MAIN_PART: [
        ExitData("Tsuta Ruins - Push the glass ball", RegionNames.TSUTA_RUINS_MUSHROOMS),
        ExitData("Tsuta Ruins - Left side door", RegionNames.TSUTA_RUINS_LEFT_SIDE,
                 has_events=["Tsuta Ruins - Defeat Blockhead"]),
        ExitData("Tsuta Ruins - Enter Inner Status",RegionNames.TSUTA_RUINS_CENTRAL_STATUE, has_events=["Tsuta Ruins - Destroy Poison Pots"])],
    RegionNames.TSUTA_RUINS_MUSHROOMS: [
        ExitData("Tsuta Ruins - Cross flimsy bridge to left side", RegionNames.TSUTA_RUINS_LEFT_SIDE,
                 has_events=["Tsuta Ruins - Blow up weakened wall above Mushrooms"])],
    RegionNames.TSUTA_RUINS_LEFT_SIDE: [
        ExitData("Tsuta Ruins - Cross the repaired Bridge", RegionNames.TSUTA_RUINS_DEVIL_GATES,
                 has_events=["Tsuta Ruins - Restore Bridge to Devil Gates' room"])
    ]
}
events = {
    RegionNames.TSUTA_RUINS_1F_MAIN_PART: {
        "Tsuta Ruins - Mandatory Single Ogre Fight": EventData(mandatory_enemies=[OkamiEnnemies.BUD_OGRE])
    },
    RegionNames.TSUTA_RUINS_MUSHROOMS: {
        "Tsuta Ruins - Mandatory Double Ogre Fight": EventData(mandatory_enemies=[OkamiEnnemies.BUD_OGRE]),
        "Tsuta Ruins - Grow the Mushrooms": EventData(required_brush_techniques=[BrushTechniques.SUNRISE],
                                                      required_items_events=[
                                                          "Tsuta Ruins - Mandatory Double Ogre Fight"]),
        "Tsuta Ruins - Blow up weakened wall above Mushrooms": EventData(cherry_bomb_level=1, required_items_events=[
            "Tsuta Ruins - Grow Mushrooms in 1F Rightside Room"])

    },
    RegionNames.TSUTA_RUINS_LEFT_SIDE: {
        # Maybe add a check that Celestial Brush is unlocked to do this, i'm not sure this matters a lot for now
        "Tsuta Ruins - Defeat Blockhead": EventData(),
        "Tsuta Ruins - Open Lockjaw with Exorcising Arrow": EventData(
            required_items_events=["Tsuta Ruins - Defeat Blockhead"]),
        "Tsuta Ruins - Restore Bridge to Devil Gates' room": EventData(
            required_items_events=["Tsuta Ruins - Open Lockjaw with Exorcising Arrow"],
            required_brush_techniques=[BrushTechniques.REJUVENATION])
    },
    RegionNames.TSUTA_RUINS_DEVIL_GATES: {
        # TODO: Check enemies in those gates, if they're similiar, this could be simplified.
        "Tsuta Ruins - Defeat Devil Gate 1": EventData(mandatory_enemies=[]),
        "Tsuta Ruins - Defeat Devil Gate 2": EventData(mandatory_enemies=[]),
        "Tsuta Ruins - Defeat Devil Gate 3": EventData(mandatory_enemies=[]),
        "Tsuta Ruins - Grow Mushrooms in Devil Gates Room": EventData(
            required_items_events=["Tsuta Ruins - Defeat Devil Gate 1", "Tsuta Ruins - Defeat Devil Gate 2",
                                   "Tsuta Ruins - Defeat Devil Gate 3"],
            required_brush_techniques=[BrushTechniques.SUNRISE]),
        "Tsuta Ruins - Destroy Poison Pots": EventData(
            required_items_events=["Tsuta Ruins - Grow Mushrooms in Devil Gates Room"])
    }
}
locations = {
    RegionNames.TSUTA_RUINS_1F_MAIN_PART: {
        "Tsuta Ruins - Freestanding Chest at Entrance": LocData(78),
        "Tsuta Ruins - Treasure Bud in Entrance Hall Middle": LocData(79, required_brush_techniques=[
            BrushTechniques.GREENSPROUT_BLOOM]),
        "Tsuta Ruins - Treasure Bud in Entrance Hall Right Side": LocData(80, required_brush_techniques=[
            BrushTechniques.GREENSPROUT_BLOOM]),
        "Tsuta Ruins - Chest in Entrance Hall near right side door": LocData(81),
        "Tsuta Ruins - Treasure Bud on 1F rightside path before ledge": LocData(82, required_brush_techniques=[
            BrushTechniques.GREENSPROUT_BLOOM]),
        "Tsuta Ruins - Treasure Bud near glass ball": LocData(83, required_brush_techniques=[
            BrushTechniques.GREENSPROUT_BLOOM]),
    },
    RegionNames.TSUTA_RUINS_MUSHROOMS: {
        "Tsuta Ruins - Treasure bud behind logs in Mushrooms room": LocData(84, power_slash_level=1,
                                                                            required_brush_techniques=[
                                                                                BrushTechniques.GREENSPROUT_BLOOM])
    },
    RegionNames.TSUTA_RUINS_LEFT_SIDE: {
        "Tsuta Ruins - Treasure Bud behind hidden bombable wall on third plaform.": LocData(85, cherry_bomb_level=1,
                                                                                            required_brush_techniques=[
                                                                                                BrushTechniques.GREENSPROUT_BLOOM]),
        "Tsuta Ruins - Treasure Bud behind Lockjaw": LocData(86, required_brush_techniques=[
            BrushTechniques.GREENSPROUT_BLOOM], required_items_events=[
            "Tsuta Ruins - Open Lockjaw with Exorcising Arrow"])
    },
    RegionNames.TSUTA_RUINS_DEVIL_GATES: {
        "Tsuta Ruins - Treasure Bud near Devil gates": LocData(87, required_brush_techniques=[
            BrushTechniques.GREENSPROUT_BLOOM]),
        "Tsuta Ruins - Treasure Bud #2 near Devil gates": LocData(88, required_brush_techniques=[
            BrushTechniques.GREENSPROUT_BLOOM]),
        "Tsuta Ruins - Map Chest near poison pots": LocData(89, required_items_events=[
            "Tsuta Ruins - Grow Mushrooms in Devil Gates Room"]),
        "Tsuta Ruins - Treasure Bud behind waterfall bombable wall": LocData(90, required_items_events=[
            "Tsuta Ruins - Destroy Poison Pots"], cherry_bomb_level=1, required_brush_techniques=[
            BrushTechniques.GREENSPROUT_BLOOM])
    }
}
