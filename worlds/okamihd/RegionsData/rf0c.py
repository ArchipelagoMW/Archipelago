from typing import TYPE_CHECKING

from rule_builder.rules import True_, Has, HasAny, Or
from ..CheckIds import shop_check_id, container_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.OkamiEnemies import OkamiEnemies
from ..Enums.WarpType import WarpType
from ..Rules import long_swim_rule, n_ryoshima_guardian_sapling_rule
from ..Types import ExitData, EventData, LocData, WarpData
from ..Enums.RegionNames import RegionNames, MapIds

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.NORTHERN_RYOSHIMA_COAST_MANDATORY_FIGHT: [
        ExitData(RegionNames.RYOSHIMA_COAST_SEIAN, one_way=True, loading_screen=False,
                 has_events=["Northern Ryoshima Coast - Mandatory Earth Nose Fight"]),
        ExitData(RegionNames.NORTHERN_RYOSHIMA_COAST, one_way=True, loading_screen=False,
                 has_events=["Northern Ryoshima Coast - Mandatory Earth Nose Fight"])
    ],
    RegionNames.NORTHERN_RYOSHIMA_COAST: [
        ExitData(RegionNames.NORTHERN_RYOSHIMA_COAST_MANDATORY_FIGHT, one_way=True, loading_screen=False),
        ExitData(RegionNames.NORTHERN_RYOSHIMA_COAST_WATCHERS_ENCOUNTER, one_way=True, loading_screen=False),
        # Special rule to account for Orca
        ExitData(RegionNames.NORTHERN_RYOSHIMA_COAST_SAPLING, loading_screen=False,
                 special_rule=n_ryoshima_guardian_sapling_rule),
        ExitData(RegionNames.NORTHERN_RYOSHIMA_COAST_TOMB, loading_screen=False, one_way=True,
                 has_events=["Northern Ryoshima Coast - Climb to Tomb Cave"])
    ],
    RegionNames.NORTHERN_RYOSHIMA_COAST_WATCHERS_ENCOUNTER: [
        ExitData(RegionNames.NORTHERN_RYOSHIMA_COAST_WATCHERS, one_way=True, loading_screen=False,
                 has_events=["Northern Ryoshima Coast - Mandatory encounter in Watcher's Cape"])
    ],
    RegionNames.NORTHERN_RYOSHIMA_COAST_WATCHERS: [
        ExitData(RegionNames.NORTHERN_RYOSHIMA_COAST, one_way=True, loading_screen=False)
    ],
    RegionNames.NORTHERN_RYOSHIMA_COAST_TOMB: [
        ExitData(RegionNames.NORTHERN_RYOSHIMA_COAST, one_way=True, loading_screen=False)
    ]
}
events = {
    RegionNames.NORTHERN_RYOSHIMA_COAST_MANDATORY_FIGHT: {
        "Northern Ryoshima Coast - Mandatory Earth Nose Fight": EventData(mandatory_enemies=[OkamiEnemies.EARTH_NOSE])
    },
    RegionNames.NORTHERN_RYOSHIMA_COAST: {
        "Northern Ryoshima Coast - Unlock Warp Points": EventData(),
        ## Needs Holy eagle or to be able to swim to access the statue
        "Northern Ryoshima Coast - Climb to Watcher's Cape": EventData(
            required_brush_techniques=[BrushTechniques.CATWALK], special_rule=Or(long_swim_rule, Has("Holy Eagle"))),
        "Northern Ryoshima Coast - Climb to Tomb Cave": EventData(required_brush_techniques=[BrushTechniques.CATWALK]),
        "Northern Ryoshima Coast - Meet Orca": EventData(required_brush_techniques=[BrushTechniques.SUNRISE],event_item_name="Orca"),
    },
    RegionNames.NORTHERN_RYOSHIMA_COAST_WATCHERS_ENCOUNTER: {
        "Northern Ryoshima Coast - Mandatory encounter in Watcher's Cape": EventData(
            mandatory_enemies=[OkamiEnemies.BLUE_CYCLOPS]),
    }
}
locations = {
    RegionNames.NORTHERN_RYOSHIMA_COAST: {
        "Northern Ryoshima Coast - Buried Chest southwest on mainland": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 3), type=LocationType.BURIED_CHEST),
        "Northern Ryoshima Coast - Buried Chest southwest of Umi's restaurant": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 7), type=LocationType.BURIED_CHEST),
        "Northern Ryoshima Coast - Buried Chest on eastern beach mainland": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 8), type=LocationType.BURIED_CHEST),
        "Northern Ryoshima Coast - Buried Chest near Yoichi": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 18), type=LocationType.BURIED_CHEST),
        "Northern Ryoshima Coast - Buried Chest near Tomb cave entrance": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 22), type=LocationType.BURIED_CHEST),
        "Northern Ryoshima Coast - West underwater clam near Umi's restaurant 2": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 26), type=LocationType.UNDERWATER_CHEST_SHALLOW),
        "Northern Ryoshima Coast - West underwater clam near Umi's restaurant 1": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 27), type=LocationType.UNDERWATER_CHEST_SHALLOW),
        "Northern Ryoshima Coast - East underwater clam near Umi's restaurant": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 28), type=LocationType.UNDERWATER_CHEST_SHALLOW),
        "Northern Ryoshima Coast - Underwater Clam near mainland east beach 1 ": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 29), type=LocationType.UNDERWATER_CHEST_SHALLOW),
        "Northern Ryoshima Coast - Underwater Clam near mainland east beach 2 ": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 30), type=LocationType.UNDERWATER_CHEST_SHALLOW),
        "Northern Ryoshima Coast - Underwater Clam near mainland east beach 3 ": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 31), type=LocationType.UNDERWATER_CHEST_SHALLOW),
        "Northern Ryoshima Coast - Underwater Clam near mainland east beach 4 ": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 32), type=LocationType.UNDERWATER_CHEST_SHALLOW),
        "Northern Ryoshima Coast - Underwater chest in river 1": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 36), type=LocationType.UNDERWATER_CHEST),
        "Northern Ryoshima Coast - Underwater chest in river 2": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 37), type=LocationType.UNDERWATER_CHEST),
        "Northern Ryoshima Coast - Underwater chest in river 3": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 39), type=LocationType.UNDERWATER_CHEST),
        "Northern Ryoshima Coast - Underwater chest in river 4": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 38), type=LocationType.UNDERWATER_CHEST),
        "Northern Ryoshima Coast - Buried Chest south of ultimate origin mirror": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 42), type=LocationType.BURIED_CHEST),
    },
    RegionNames.NORTHERN_RYOSHIMA_COAST_WATCHERS: {
        "Northern Ryoshima Coast - Buried Chest in watcher's cape": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 5), type=LocationType.BURIED_CHEST)
    },
    RegionNames.NORTHERN_RYOSHIMA_COAST_SAPLING: {
        "Northern Ryoshima Coast - Buried Chest on guardian sapling island": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 9), type=LocationType.BURIED_CHEST),
        "Northern Ryoshima Coast - Freestanding Chest on guardian sapling island": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 67))
    },
    RegionNames.NORTHERN_RYOSHIMA_COAST_TOMB: {
        "Northern Ryoshima Coast - Chest in Tomb Cave 2": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 19)),
        "Northern Ryoshima Coast - Chest in Tomb Cave 3": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 20)),
        "Northern Ryoshima Coast - Chest in Tomb Cave 1": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 21))
    },
    RegionNames.NORTHERN_RYOSHIMA_COAST_MIST_WARP: {
        "Northern Ryoshima Coast - Chest in secret Mist Warp Area": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 33))
    }
}
warps = {
    RegionNames.NORTHERN_RYOSHIMA_COAST: [
        WarpData(WarpType.MIST_WARP, Has("Northern Ryoshima Coast - Unlock Warp Points"),
                 Has("Northern Ryoshima Coast - Unlock Warp Points")),
        WarpData(WarpType.MERMAID_SPRING, Has("Northern Ryoshima Coast - Unlock Warp Points"),
                 Has("Northern Ryoshima Coast - Unlock Warp Points"))
    ],
    RegionNames.NORTHERN_RYOSHIMA_COAST_MIST_WARP: [
        WarpData(WarpType.MIST_WARP, Has("Northern Ryoshima Coast - Unlock Warp Points"),
                 Has("Northern Ryoshima Coast - Unlock Warp Points"))
    ]
}
shop_locations = {
    RegionNames.NORTHERN_RYOSHIMA_COAST: {
        "Northern Ryoshima Coast - Shop Slot 1": LocData(shop_check_id(11, 0), type=LocationType.SHOP),
        "Northern Ryoshima Coast - Shop Slot 2": LocData(shop_check_id(11, 1), type=LocationType.SHOP),
        "Northern Ryoshima Coast - Shop Slot 3": LocData(shop_check_id(11, 2), type=LocationType.SHOP),
        "Northern Ryoshima Coast - Shop Slot 4": LocData(shop_check_id(11, 3), type=LocationType.SHOP),
        "Northern Ryoshima Coast - Shop Slot 5": LocData(shop_check_id(11, 4), type=LocationType.SHOP),
        "Northern Ryoshima Coast - Shop Slot 6": LocData(shop_check_id(11, 5), type=LocationType.SHOP),
        "Northern Ryoshima Coast - Shop Slot 7": LocData(shop_check_id(11, 6), type=LocationType.SHOP),
        "Northern Ryoshima Coast - Shop Slot 8": LocData(shop_check_id(11, 7), type=LocationType.SHOP),
        "Northern Ryoshima Coast - Shop Slot 9": LocData(shop_check_id(11, 8), type=LocationType.SHOP),
        "Northern Ryoshima Coast - Shop Slot 10": LocData(shop_check_id(11, 9), type=LocationType.SHOP),
        "Northern Ryoshima Coast - Shop Slot 11": LocData(shop_check_id(11, 10), type=LocationType.SHOP),
        "Northern Ryoshima Coast - Shop Slot 12": LocData(shop_check_id(11, 11), type=LocationType.SHOP),
    }
}
