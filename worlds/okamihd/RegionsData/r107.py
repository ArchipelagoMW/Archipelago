from typing import TYPE_CHECKING

from BaseClasses import LocationProgressType
from ..CheckIds import brush_check_id, container_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.OkamiEnemies import OkamiEnemies
from ..Enums.RegionNames import RegionNames, MapIds
from ..Rules import gale_shrine_access
from ..Types import EventData, ExitData, LocData

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.GALE_SHRINE_ENTRANCE: [
        ExitData(RegionNames.GALE_SHRINE, required_items_events=["Gale Shrine - Open Door"], loading_screen=False)],
    RegionNames.GALE_SHRINE: [ExitData(RegionNames.GALE_SHRINE_LIFT, loading_screen=False),
                              ExitData(RegionNames.GALE_SHRINE_BACK,
                                       required_items_events=["Gale Shrine - Move the Windmill Bridges"], loading_screen=False)
                              ],
    RegionNames.GALE_SHRINE_LIFT: [
        ExitData(RegionNames.GALE_SHRINE_2F, required_items_events=["Gale Shrine - Use Lift"], loading_screen=False),
        ExitData(RegionNames.GALE_SHRINE_3F,
                 required_items_events=["Gale Shrine - Use Lift", "Gale Shrine - 2F Cursed Scroll"], loading_screen=False)],
    RegionNames.GALE_SHRINE_BACK: [ExitData(RegionNames.GALE_SHRINE_BOSS,
                                            required_items_events=["Gale Shrine - Cross flame Hallway"])]
}
events = {
    RegionNames.GALE_SHRINE_ENTRANCE: {
        "Gale Shrine - Open Door": EventData(special_rule=gale_shrine_access),
    },
    RegionNames.GALE_SHRINE: {
        # Gives a key
        "Gale Shrine - Cursed Door in 1F right side room": EventData(mandatory_enemies=[OkamiEnemies.CHIMERA]),
        "Gale Shrine - Open Lift": EventData(required_items_events=["Gale Shrine - Cursed Door in 1F right side room"]),
        "Gale Shrine - Move the Windmill Bridges": EventData(required_brush_techniques=[BrushTechniques.GALESTORM])
    },
    RegionNames.GALE_SHRINE_LIFT: {
        "Gale Shrine - Use Lift": EventData(cherry_bomb_level=1)
    },
    RegionNames.GALE_SHRINE_2F: {
        # Gives a key
        "Gale Shrine - 2F Cursed Scroll": EventData(mandatory_enemies=[OkamiEnemies.CHIMERA]),
    },
    RegionNames.GALE_SHRINE_BACK: {
        "Gale Shrine - Cross flame Hallway": EventData(required_brush_techniques=[BrushTechniques.GALESTORM])
    },
    RegionNames.GALE_SHRINE_BOSS: {
        # Techinally galestrom is already required to beat the boss,
        # but if we ever randomize enemies/bosses, I've added the following Susano cutscene requirements here.
        "Gale Shrine - Defeat Crimson Helm": EventData(mandatory_enemies=[OkamiEnemies.CRIMSON_HELM],
                                                       power_slash_level=1,
                                                       required_brush_techniques=[BrushTechniques.GALESTORM],
                                                       ),
        "Gale Shrine - Get Serpent Crystal": EventData(
            required_items_events=["Gale Shrine - Defeat Crimson Helm"],
            event_item_name="Serpent Crystal",
            is_event_item=lambda o: o.MoonCaveAccess == 0,
            precollected=lambda o: o.MoonCaveAccess == 2,
            id=191
        )
    }
}
locations = {
    RegionNames.GALE_SHRINE: {
        "Gale Shrine - 1st Underwater Chest in entrance room": LocData(container_check_id(MapIds.GALE_SHRINE, 26),
                                                                       type=LocationType.UNDERWATER_CHEST),
        "Gale Shrine - 2nd Underwater Chest in entrance room": LocData(container_check_id(MapIds.GALE_SHRINE, 27),
                                                                       type=LocationType.UNDERWATER_CHEST),
        "Gale Shrine - 3rd Underwater Chest in entrance room": LocData(container_check_id(MapIds.GALE_SHRINE, 28),
                                                                       type=LocationType.UNDERWATER_CHEST),
    },
    RegionNames.GALE_SHRINE_LIFT: {
        "Gale Shrine - 1st Chest Under Lift ": LocData(container_check_id(MapIds.GALE_SHRINE, 22),
                                                       required_items_events=["Gale Shrine - Use Lift"]),
        "Gale Shrine - 2nd Chest Under Lift ": LocData(container_check_id(MapIds.GALE_SHRINE, 23),
                                                       required_items_events=["Gale Shrine - Use Lift"]),
        "Gale Shrine - 3rd Chest Under Lift ": LocData(container_check_id(MapIds.GALE_SHRINE, 24),
                                                       required_items_events=["Gale Shrine - Use Lift"])
    },
    RegionNames.GALE_SHRINE_2F: {
        "Gale Shrine - 2F Burning Chest": LocData(container_check_id(MapIds.GALE_SHRINE, 2),
                                                  type=LocationType.BURNING_CHEST_NO_WATER)
    },
    RegionNames.GALE_SHRINE_3F: {
        "Gale Shrine - Kazegami": LocData(brush_check_id(6), type=LocationType.CONSTELLATION,progress_type=LocationProgressType.EXCLUDED),  # bit 6
        "Gale Shrine - 3F Sun Fragment chest near Kazegami": LocData(container_check_id(MapIds.GALE_SHRINE, 0)),
        "Gale Shrine - 3F Burning Chest": LocData(container_check_id(MapIds.GALE_SHRINE, 1),
                                                  type=LocationType.BURNING_CHEST_NO_WATER)
    },
    RegionNames.GALE_SHRINE_BACK: {
        "Gale Shrine - 1F Chest after windmills": LocData(container_check_id(MapIds.GALE_SHRINE, 25)),
        "Gale Shrine - 1F Burning Chest in banner room": LocData(container_check_id(MapIds.GALE_SHRINE, 16),
                                                                 type=LocationType.BURNING_CHEST_NO_WATER),
        "Gale Shrine - 1F Burning Chest in banner room rafters center": LocData(
            container_check_id(MapIds.GALE_SHRINE, 17),
            type=LocationType.BURNING_CHEST_NO_WATER,
            required_brush_techniques=[
                BrushTechniques.GREENSPROUT_VINE]),
        "Gale Shrine - 1F Burning Chest in banner room rafters front": LocData(
            container_check_id(MapIds.GALE_SHRINE, 19),
            type=LocationType.BURNING_CHEST_NO_WATER,
            required_brush_techniques=[
                BrushTechniques.GREENSPROUT_VINE]),
        "Gale Shrine - 1F Chest in banner room rafters top": LocData(container_check_id(MapIds.GALE_SHRINE, 18),
                                                                     required_brush_techniques=[
                                                                         BrushTechniques.GREENSPROUT_VINE]),
        "Gale Shrine - 1F Chest in banner room between banners": LocData(container_check_id(MapIds.GALE_SHRINE, 20),
                                                                         required_brush_techniques=[
                                                                             BrushTechniques.GALESTORM]),
        "Gale Shrine - 1F Chest in banner room after banners": LocData(container_check_id(MapIds.GALE_SHRINE, 21),
                                                                       required_brush_techniques=[
                                                                           BrushTechniques.GALESTORM])
    },
    RegionNames.GALE_SHRINE_BOSS: {
        "Gale Shrine - Crimson Helm Reward": LocData(29, required_items_events=["Gale Shrine - Defeat Crimson Helm"],progress_type=LocationProgressType.EXCLUDED)
    }
}
