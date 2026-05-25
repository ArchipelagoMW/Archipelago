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
    RegionNames.IMPERIAL_PALACE_SMALL_ENTRANCE: [
        ExitData(RegionNames.IMPERIAL_PALACE_FEET_HELL,
                 has_events=["Imperial Palace - Mandatory Thunder Doom Mirror Encounter"]),
        ExitData(RegionNames.IMPERIAL_PALACE_WEST_CAVE,
                 has_events=["Imperial Palace - Open west side lockjaw"])
    ],
    RegionNames.IMPERIAL_PALACE_WEST_CAVE: [
        ExitData(RegionNames.IMPERIAL_PALACE_SPIDER_CAVE, has_events=["Imperial Palace - Blow up west cave floor"])
    ],
    RegionNames.IMPERIAL_PALACE_SPIDER_CAVE: [
        ExitData(RegionNames.IMPERIAL_PALACE_SPIDER_CAVE_TOP, has_events=["Holy Eagle"], one_way=True,
                 loading_screen=False),
        ExitData(RegionNames.IMPERIAL_PALACE_FLASK_ROOM,
                 has_events=["Imperial Palace - Blow up wall to mist flask room"], one_way=True)
    ],
    RegionNames.IMPERIAL_PALACE_SPIDER_CAVE_TOP: [
        ExitData(RegionNames.IMPERIAL_PALACE_SPIDER_CAVE, one_way=True, loading_screen=False)
    ],
    RegionNames.IMPERIAL_PALACE_FLASK_ROOM: [
        ExitData(RegionNames.IMPERIAL_PALACE_SPIDER_CAVE, one_way=True,
                 has_events=["Imperial Palace - Outspeed the spider"])
    ],
    RegionNames.IMPERIAL_PALACE_FEET_HELL: [
        ExitData(RegionNames.IMPERIAL_PALACE_POISON_SOZU, has_events=["Imperial Palace - Outspeed the Brooms"])
    ],
    RegionNames.IMPERIAL_PALACE_POISON_SOZU: [
        ExitData(RegionNames.IMPERIAL_PALACE_EMPERORS_ROOM, has_events=["Imperial Palace - Cross the Sozu"])
    ],
    RegionNames.IMPERIAL_PALACE_EMPERORS_ROOM:[
        # Also should require Veil of Mist:
        # TODO: After changing entrances has_events.
        ExitData(RegionNames.IMPERIAL_PALACE_WEST_BEAM,has_events=["Holy Eagle"],loading_screen=False),
        # Also should require Veil of Mist:
        # TODO: After changing entrances has_events.
        ExitData(RegionNames.IMPERIAL_PALACE_INSIDE_EMPEROR,one_way=True)
    ],
    RegionNames.IMPERIAL_PALACE_INSIDE_EMPEROR:[
        ExitData(RegionNames.IMPERIAL_PALACE_EMPERORS_ROOM, one_way=True),
        ExitData(RegionNames.IMPERIAL_PALACE, one_way=True,has_events=["Imperial Palace - Defeat Blight"])
    ]
}
events = {
    RegionNames.IMPERIAL_PALACE_SMALL_ENTRANCE: {
        "Imperial Palace - Mandatory Thunder Doom Mirror Encounter": EventData(
            mandatory_enemies=[OkamiEnemies.THUNDER_DOOM_MIRROR]),
        "Imperial Palace - Open west side lockjaw": EventData(
            required_items_events=["Imperial Palace - Grab lockjaw key"])
    },
    RegionNames.IMPERIAL_PALACE_FEET_HELL: {
        "Imperial Palace - Blow up alcove walls in feet hell": EventData(cherry_bomb_level=1),
        "Imperial Palace - Grab lockjaw key": EventData(),
        "Imperial Palace - Outspeed the Brooms": EventData(required_brush_techniques=[BrushTechniques.VEIL_OF_MIST]),
    },
    RegionNames.IMPERIAL_PALACE_WEST_CAVE: {
        "Imperial Palace - Blow up west cave floor": EventData(cherry_bomb_level=1)
    },
    RegionNames.IMPERIAL_PALACE_SPIDER_CAVE: {
        "Imperial Palace - Blow up wall to mist flask room": EventData(cherry_bomb_level=1)
    },
    RegionNames.IMPERIAL_PALACE_FLASK_ROOM: {
        "Imperial Palace - Outspeed the spider": EventData(required_brush_techniques=[BrushTechniques.VEIL_OF_MIST]),
        # Not really in that room, but triggers when exiting it:
        "Imperial Palace - Mandatory Wind Doom Mirror": EventData(mandatory_enemies=[OkamiEnemies.WIND_DOOM_MIRROR])
    },
    RegionNames.IMPERIAL_PALACE_POISON_SOZU: {
        "Imperial Palace - Cross the Sozu": EventData(required_brush_techniques=[BrushTechniques.WATERSPOUT])
    },
    RegionNames.IMPERIAL_PALACE_INSIDE_EMPEROR: {
        "Imperial Palace - Defeat Blight":EventData(mandatory_enemies=[OkamiEnemies.BLIGHT])
    }

}
locations = {
    RegionNames.IMPERIAL_PALACE_SMALL_ENTRANCE: {
        # Tutorial for "Launching" Issun
        "Imperial Palace - Chest at entrance": LocData(container_check_id(MapIds.IMPERIAL_PALACE_SMALL, 0),
                                                       type=LocationType.LOCKED_CHEST),
        "Imperial Palace - Locked Chest in poison puddle": LocData(container_check_id(MapIds.IMPERIAL_PALACE_SMALL, 14),
                                                                   type=LocationType.LOCKED_CHEST),
        "Imperial Palace - Freestanding Chest on poison puddle rocks": LocData(
            container_check_id(MapIds.IMPERIAL_PALACE_SMALL, 10))
    },
    RegionNames.IMPERIAL_PALACE_FEET_HELL: {
        "Imperial Palace - Chest in feet hell northern alcove": LocData(
            container_check_id(MapIds.IMPERIAL_PALACE_SMALL, 1),
            required_items_events=["Imperial Palace - Blow up alcove walls in feet hell"]),
        "Imperial Palace - Chest in feet hell southern alcove": LocData(
            container_check_id(MapIds.IMPERIAL_PALACE_SMALL, 8),
            required_items_events=["Imperial Palace - Blow up alcove walls in feet hell"]),

    },
    RegionNames.IMPERIAL_PALACE_SPIDER_CAVE_TOP: {
        "Imperial Palace - Locked Chest in spider cave webs": LocData(
            container_check_id(MapIds.IMPERIAL_PALACE_SMALL, 9), type=LocationType.LOCKED_CHEST
        )
    },
    RegionNames.IMPERIAL_PALACE_FLASK_ROOM: {
        "Imperial Palace - Kasugami": LocData(brush_check_id(16), type=LocationType.CONSTELLATION,
                                              required_brush_techniques=[BrushTechniques.GALESTORM],
                                              power_slash_level=1,progress_type=LocationProgressType.EXCLUDED)
    },
    RegionNames.IMPERIAL_PALACE_POISON_SOZU: {
        "Imperial Palace - Locked chest near poison Sozu": LocData(container_check_id(MapIds.IMPERIAL_PALACE_SMALL, 15),
                                                                   type=LocationType.LOCKED_CHEST)
    },
    RegionNames.IMPERIAL_PALACE_EMPERORS_ROOM: {
        "Imperial Palace - Northwest locked chest in webs above the emperor's bedroom": LocData(
            container_check_id(MapIds.IMPERIAL_PALACE_SMALL, 6), type=LocationType.LOCKED_CHEST),
        "Imperial Palace - North central chest above the emperor's bedroom": LocData(
            container_check_id(MapIds.IMPERIAL_PALACE_SMALL, 5)),
        "Imperial Palace - Southwest locked chest in webs above the emperor's bedroom": LocData(
            container_check_id(MapIds.IMPERIAL_PALACE_SMALL, 7), type=LocationType.LOCKED_CHEST,
            required_brush_techniques=[BrushTechniques.VEIL_OF_MIST])
    },
    RegionNames.IMPERIAL_PALACE_WEST_BEAM:{
        "Imperial Palace - Southmost chest on west beam above the emperor's bedroom": LocData(
            container_check_id(MapIds.IMPERIAL_PALACE_SMALL, 12)),
        "Imperial Palace - Soutwest chest on west beam above the emperor's bedroom": LocData(
            container_check_id(MapIds.IMPERIAL_PALACE_SMALL, 11)),
        "Imperial Palace - center chest on west beam above the emperor's bedroom": LocData(
            container_check_id(MapIds.IMPERIAL_PALACE_SMALL, 13))
    },
    RegionNames.IMPERIAL_PALACE_INSIDE_EMPEROR:{
        "Imperial Palace - Blight Reward":LocData(999,required_items_events=["Imperial Palace - Defeat Blight"],progress_type=LocationProgressType.EXCLUDED)
    }

}
