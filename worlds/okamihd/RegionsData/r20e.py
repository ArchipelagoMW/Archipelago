from typing import TYPE_CHECKING


from rule_builder.rules import And
from ..CheckIds import container_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.OkamiEnemies import OkamiEnemies
from ..Enums.RegionNames import RegionNames, MapIds
from ..Rules import oni_island_5f_thunder_rule, slowdown_rule
from ..Types import ExitData, LocData, EventData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.ONI_ISLAND_INTERIOR_4F: [
        ExitData(RegionNames.ONI_ISLAND_INTERIOR_5F, one_way=True, loading_screen=False,
                 required_items_events=["Oni Island - 4F Climb on platforms"]),
        ExitData(RegionNames.ONI_ISLAND_INTERIOR_4F_STAIRS, one_way=True, loading_screen=False,
                 required_items_events=["Oni Island - 4F Grab Thunder Key"])
    ],
    RegionNames.ONI_ISLAND_INTERIOR_5F: [
        ExitData(RegionNames.ONI_ISLAND_INTERIOR_4F, one_way=True, loading_screen=False),
        ExitData(RegionNames.ONI_ISLAND_INTERIOR_4F_KEY, one_way=True, loading_screen=False,
                 required_items_events=["Oni Island - 5F Cross Spider"])
    ],
    RegionNames.ONI_ISLAND_INTERIOR_4F_KEY: [
        ExitData(RegionNames.ONI_ISLAND_INTERIOR_4F_STAIRS, required_items_events=["Oni Island - 4F Blow up wall"],
                 loading_screen=False)
    ],
    RegionNames.ONI_ISLAND_INTERIOR_4F_STAIRS: [
        ExitData(RegionNames.ONI_ISLAND_INTERIOR_4F, one_way=True, loading_screen=False,
                 required_items_events=["Oni Island - 4F use vine to cross poison"]),
        ExitData(RegionNames.ONI_ISLAND_INTERIOR_PRE_TOBI_8, loading_screen=False,
                 required_items_events=["Oni Island - 4F Open lockjaw"])
    ],
    RegionNames.ONI_ISLAND_INTERIOR_PRE_TOBI_8: [
        ExitData(RegionNames.ONI_ISLAND_INTERIOR_6F, loading_screen=False,
                 required_items_events=["Oni Island - Tobi Race #8"])
    ],
    RegionNames.ONI_ISLAND_INTERIOR_6F: [
        ExitData(RegionNames.ONI_ISLAND_INTERIOR_PRE_TOBI_9, loading_screen=False,
                 required_items_events=["Oni Island - Defeat Blockhead"])
    ],
    RegionNames.ONI_ISLAND_INTERIOR_PRE_TOBI_9: [
        ExitData(RegionNames.ONI_ISLAND_INTERIOR_POST_TOBI_9, loading_screen=False,
                 required_items_events=["Oni Island - Tobi Race #9 (Final)"])
    ],
    RegionNames.ONI_ISLAND_INTERIOR_POST_TOBI_9: [
        ExitData(RegionNames.ONI_ISLAND_NINETAILS)
    ]
}
events = {
    RegionNames.ONI_ISLAND_INTERIOR_4F: {
        "Oni Island - 4F Grab Thunder Key": EventData(),
        "Oni Island - 4F Climb on platforms": EventData(
            required_items_events=["Oni Island - 4F Grab Thunder Key", "Holy Eagle"])
    },
    RegionNames.ONI_ISLAND_INTERIOR_5F: {
        "Oni Island - 5F Cross Spider": EventData(special_rule=slowdown_rule)
    },
    RegionNames.ONI_ISLAND_INTERIOR_4F_KEY: {
        "Oni Island - 4F Grab Key": EventData(),
        "Oni Island - 4F Blow up wall": EventData(cherry_bomb_level=1)
    },
    RegionNames.ONI_ISLAND_INTERIOR_4F_STAIRS: {
        "Oni Island - 4F Open lockjaw": EventData(required_items_events=["Oni Island - 4F Grab Key"]),
        "Oni Island - 4F use vine to cross poison": EventData(
            required_brush_techniques=[BrushTechniques.GREENSPROUT_VINE])
    },
    RegionNames.ONI_ISLAND_INTERIOR_PRE_TOBI_8: {
        "Oni Island - Tobi Race #8": EventData(special_rule=slowdown_rule,
                                               required_items_events=["Oni Island - 4F Grab Thunder Key"])
    },
    RegionNames.ONI_ISLAND_INTERIOR_6F: {
        "Oni Island - Mandatory 6F Fight": EventData(mandatory_enemies=[OkamiEnemies.BLUE_OGRE, OkamiEnemies.RED_OGRE]),
        "Oni Island - 6F Climb to Cat statue": EventData(
            required_items_events=["Oni Island - Mandatory 6F Fight", "Holy Eagle", "Oni Island - 4F Grab Thunder Key"],
            required_brush_techniques=[BrushTechniques.CATWALK]),
        "Oni Island - Second Mandatory 6F Fight": EventData(
            mandatory_enemies=[OkamiEnemies.HEADLESS_GUARDIAN, OkamiEnemies.EXECUTIONER_GUARDIAN],
            required_items_events=["Oni Island - 6F Climb to Cat statue"]),
        "Oni Island - Defeat Blockhead": EventData(required_items_events=["Oni Island - Second Mandatory 6F Fight"])
    },
    RegionNames.ONI_ISLAND_INTERIOR_PRE_TOBI_9: {
        "Oni Island - Tobi Race #9 (Final)": EventData(required_brush_techniques=[BrushTechniques.GREENSPROUT_VINE],
                                                       cherry_bomb_level=1, required_items_events=["Holy Eagle"])
    }
}

locations = {
    RegionNames.ONI_ISLAND_INTERIOR_4F: {
        "Oni Island - 4F Thunder chest": LocData(container_check_id(MapIds.ONI_ISLAND_UPPER_INT, 3),
                                                 type=LocationType.THUNDER_CHEST),
    },
    RegionNames.ONI_ISLAND_INTERIOR_5F: {
        # Technically a special source, but since you already nedd the key to access it...
        "Oni Island - 5F Thunder chest": LocData(container_check_id(MapIds.ONI_ISLAND_UPPER_INT, 0),
                                                 type=LocationType.THUNDER_CHEST)
    },
    RegionNames.ONI_ISLAND_INTERIOR_4F_KEY: {
        "Oni Island - 4F chest in key area": LocData(container_check_id(MapIds.ONI_ISLAND_UPPER_INT, 7))
    },
    RegionNames.ONI_ISLAND_INTERIOR_PRE_TOBI_8: {
        "Oni Island - 5F Thunder chest above stairs to 4F": LocData(container_check_id(MapIds.ONI_ISLAND_UPPER_INT, 5),
                                                                    type=LocationType.THUNDER_CHEST_SPECIAL_SOURCE,
                                                                    special_rule=oni_island_5f_thunder_rule),
        "Oni Island - 5F Thunder chest above stairs in tobi race #8": LocData(
            container_check_id(MapIds.ONI_ISLAND_UPPER_INT, 6),
            type=LocationType.THUNDER_CHEST_SPECIAL_SOURCE,
            special_rule=oni_island_5f_thunder_rule, required_items_events=["Oni Island - Tobi Race #8"])

    },
    RegionNames.ONI_ISLAND_INTERIOR_6F: {
        "Oni Island - 7F Thunder chest behind spider": LocData(container_check_id(MapIds.ONI_ISLAND_UPPER_INT, 1),
                                                               required_brush_techniques=[BrushTechniques.CATWALK],
                                                               type=LocationType.THUNDER_CHEST_SPECIAL_SOURCE,
                                                               special_rule=And(oni_island_5f_thunder_rule,
                                                                                slowdown_rule),
                                                               required_items_events=[
                                                                   "Oni Island - 6F Climb to Cat statue",
                                                                   "Holy Eagle"]),
        "Oni Island - 7F Thunder chest opposite of spider": LocData(container_check_id(MapIds.ONI_ISLAND_UPPER_INT, 4),
                                                                    required_brush_techniques=[
                                                                        BrushTechniques.CATWALK, ],
                                                                    type=LocationType.THUNDER_CHEST_SPECIAL_SOURCE,
                                                                    special_rule=oni_island_5f_thunder_rule,
                                                                    required_items_events=[
                                                                        "Oni Island - 6F Climb to Cat statue",
                                                                        "Holy Eagle"]),
    },
    RegionNames.ONI_ISLAND_INTERIOR_POST_TOBI_9: {
        # Not set a special source since thunder key is required to access it anyway
        "Oni Island - 7F Thunder Chest above railing": LocData(container_check_id(MapIds.ONI_ISLAND_UPPER_INT, 2),
                                                               required_items_events=["Holy Eagle",
                                                                                      "Oni Island - 4F Grab Thunder Key"],
                                                               type=LocationType.THUNDER_CHEST)
    }
}
