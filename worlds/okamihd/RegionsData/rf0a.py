from typing import TYPE_CHECKING

from rule_builder.rules import Has, True_
from ..CheckIds import container_check_id, shop_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.OkamiEnemies import OkamiEnemies
from ..Enums.WarpType import WarpType
from ..Types import ExitData, EventData, LocData, WarpData
from ..Enums.RegionNames import RegionNames, MapIds

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.RYOSHIMA_COAST: [
        ExitData(RegionNames.RYOSHIMA_COAST_SEA, needs_long_swim=True, loading_screen=False),
        ExitData(RegionNames.RYOSHIMA_COAST_CATWALK_TOWER, loading_screen=False, one_way=True,
                 required_items_events=["Ryoshima Coast - Climb catwalk tower"]),
        # Special Handling for the encounter around Seian, city entrance as the enemies inside require galestrom to be beaten.
        ExitData(RegionNames.RYOSHIMA_COAST_SEIAN_ENCOUNTER, one_way=True, loading_screen=False),
        ExitData(RegionNames.RYOSHIMA_COAST_WEST_PIER, one_way=True, loading_screen=False),
        ExitData(RegionNames.ANKOKU_TEMPLE),
        ExitData(RegionNames.FAWNS_HOUSE, required_items_events=["Ryoshima Coast - Open Shortcut To Mme Fawn's"]),
        ExitData(RegionNames.RYOSHIMA_COAST_LUNAR_LAGOON, one_way=True,
                 required_items_events=["Ryoshima Coast - Open Lunar Lagoon"], loading_screen=False),
        ExitData(RegionNames.RYOSHIMA_COAST_BANDIT_SPIDER,has_events=["Ryoshima Coast - Open Bandit Spider Cave"],one_way=True),
        ExitData(RegionNames.SEIAN_CITY_TREASURE_EAST,has_events=["Ryoshima Coast - Open shortcut to Sei-an City"])

    ],
    RegionNames.RYOSHIMA_COAST_SEA: [
        ExitData(RegionNames.RYOSHIMA_COAST_DOJO, needs_long_swim=True, loading_screen=False),
        ExitData(RegionNames.RYOSHIMA_COAST_SHIP_TOP, needs_long_swim=True, loading_screen=False),
        ExitData(RegionNames.RYOSHIMA_COAST_SEA_FAR,loading_screen=False,required_items_events=["Water Tablet"])
    ],
    RegionNames.RYOSHIMA_COAST_CATWALK_TOWER: [
        ExitData(RegionNames.RYOSHIMA_COAST, required_items_events=["Ryoshima Coast - Climb back to main area"], one_way=True,
                 loading_screen=False)
    ],
    # Special Handling for the encounter around Seian, city entrance as the enemies inside require galestrom to be beaten.
    RegionNames.RYOSHIMA_COAST_SEIAN_ENCOUNTER: [
        ExitData(RegionNames.RYOSHIMA_COAST_SEIAN, loading_screen=False, one_way=True,
                 required_items_events=["Ryoshima Coast - Mandatory Ubume Encounter"]),
        ExitData(RegionNames.RYOSHIMA_COAST, loading_screen=False, one_way=True,
                 required_items_events=["Ryoshima Coast - Mandatory Ubume Encounter"])
    ],
    RegionNames.RYOSHIMA_COAST_SEIAN: [
        # Special Handling for the encounter around Seian, city entrance as the enemies inside require galestrom to be beaten.
        ExitData(RegionNames.RYOSHIMA_COAST_SEIAN_ENCOUNTER, one_way=True, loading_screen=False),
        ExitData(RegionNames.SEIAN_CITY_COMMONERS_DRY),
        ExitData(RegionNames.NORTHERN_RYOSHIMA_COAST_MANDATORY_FIGHT, has_events=["Ryoshima Coast - Open Door to North Ryoshima Coast"],one_way=True)
    ],
    RegionNames.RYOSHIMA_COAST_LUNAR_LAGOON: [
        ExitData(RegionNames.RYOSHIMA_COAST_SEA, one_way=True, loading_screen=False,needs_long_swim=True),
        ExitData(RegionNames.SUNKEN_SHIP_ENTRANCE,one_way=True)
    ],
    RegionNames.RYOSHIMA_COAST_WEST_PIER: [
        ExitData(RegionNames.RYOSHIMA_COAST_SEA, loading_screen=False)
    ]

}
# Note to myself: Warp to lunar turret : 850,1000,3250
events = {
    RegionNames.RYOSHIMA_COAST: {
        "Ryoshima Coast - Climb catwalk tower": EventData(required_brush_techniques=[BrushTechniques.CATWALK]),
        "Ryoshima Coast - Open Lunar Lagoon": EventData(required_items_events=["Holy Eagle"],
                                                        required_brush_techniques=[BrushTechniques.CRESCENT]),
        "Ryoshima Coast - Open Shortcut To Mme Fawn's": EventData(),
        "Ryoshima Coast - Clear Devil Gate near North Ryoshima Coast Entrance": EventData(mandatory_enemies=[OkamiEnemies.ICE_LIPS,OkamiEnemies.THUNDER_EAR]),
        "Ryoshima Coast - Open Bandit Spider Cave": EventData(required_items_events=["Digging Champ"]),
        "Ryoshima Coast - Open shortcut to Sei-an City":EventData(required_items_events=["Dragon Palace - Give Dragon Orb to Otohime"])

    },
    RegionNames.RYOSHIMA_COAST_CATWALK_TOWER: {
        "Ryoshima Coast - Climb back to main area": EventData(required_brush_techniques=[BrushTechniques.WATERSPOUT])
    },
    RegionNames.RYOSHIMA_COAST_DOJO: {
        # Convert these to items at some point when dojos techs/shops are randomizable
        "Ryoshima Coast - Buy Holy Eagle": EventData(event_item_name="Holy Eagle"),
        "Ryoshima Coast - Buy Digging Champ": EventData(event_item_name="Digging Champ")
    },
    RegionNames.RYOSHIMA_COAST_SEIAN_ENCOUNTER: {
        "Ryoshima Coast - Mandatory Ubume Encounter": EventData(mandatory_enemies=[OkamiEnemies.UBUME])
    },
    RegionNames.RYOSHIMA_COAST_SEIAN:{
        "Ryoshima Coast - Open Door to North Ryoshima Coast":EventData(required_items_events=["Himiko's Palace - Hear Himiko's request"])
    }
}
locations = {
    RegionNames.RYOSHIMA_COAST: {
        "Ryoshima Coast - Buried Chest behind temple": LocData(container_check_id(MapIds.HEALED_RYOSHIMA, 0),
                                                               type=LocationType.BURIED_CHEST),
        "Ryoshima Coast - Freestanding Chest at Pier's Edge": LocData(container_check_id(MapIds.HEALED_RYOSHIMA, 31)),
        "Ryoshima Coast - Eastern Clam on Beach": LocData(container_check_id(MapIds.HEALED_RYOSHIMA, 49)),
        "Ryoshima Coast - Eastern Underwater clam on Beach": LocData(container_check_id(MapIds.HEALED_RYOSHIMA, 51),
                                                                     type=LocationType.UNDERWATER_CHEST_SHALLOW),
        "Ryoshima Coast - Center Underwater clam on Beach": LocData(container_check_id(MapIds.HEALED_RYOSHIMA, 52),
                                                                    type=LocationType.UNDERWATER_CHEST_SHALLOW),
        "Ryoshima Coast - Western Underwater clam on Beach east of Pier": LocData(
            container_check_id(MapIds.HEALED_RYOSHIMA, 53), type=LocationType.UNDERWATER_CHEST_SHALLOW),
        "Ryoshima Coast - Nothern Underwater Clam west of Lunar turret": LocData(
            container_check_id(MapIds.HEALED_RYOSHIMA, 55), type=LocationType.UNDERWATER_CHEST_SHALLOW),
        "Ryoshima Coast - Southern Underwater Clam west of Lunar turret": LocData(
            container_check_id(MapIds.HEALED_RYOSHIMA, 56), type=LocationType.UNDERWATER_CHEST),
        "Ryoshima Coast - Buried Chest east of pier ramp": LocData(
            container_check_id(MapIds.HEALED_RYOSHIMA, 60), type=LocationType.BURIED_CHEST),
        "Ryoshima Coast - Buried Chest on ledge near pier": LocData(
            container_check_id(MapIds.HEALED_RYOSHIMA, 61), type=LocationType.BURIED_CHEST),
    },
    RegionNames.RYOSHIMA_COAST_SEA: {
        "Ryoshima Coast - Underwater Clam in dojo island bombable room": LocData(
            container_check_id(MapIds.HEALED_RYOSHIMA, 2), type=LocationType.UNDERWATER_CHEST_SHALLOW,
            cherry_bomb_level=1),
        "Ryoshima Coast - Underwater Clam southwest of ultimate origin mirror": LocData(
            container_check_id(MapIds.HEALED_RYOSHIMA, 57), type=LocationType.UNDERWATER_CHEST),
        "Ryoshima Coast - Eastmost Underwater Clam, south of city checkpoint warp": LocData(
            container_check_id(MapIds.HEALED_RYOSHIMA, 58), type=LocationType.UNDERWATER_CHEST),
        "Ryoshima Coast - Underwater Clam southeast of ultimate origin mirror": LocData(
            container_check_id(MapIds.HEALED_RYOSHIMA, 59), type=LocationType.UNDERWATER_CHEST),
    },
    RegionNames.RYOSHIMA_COAST_SEA_FAR:{
        "Ryoshima Coast - Clam on southernmost rocks": LocData(
            container_check_id(MapIds.HEALED_RYOSHIMA, 5)),
        "Ryoshima Coast - Clam between shimenawa rocks": LocData(container_check_id(MapIds.HEALED_RYOSHIMA, 24)),
        "Ryoshima Coast - Southern underwater Clam between shimenawa rocks": LocData(
            container_check_id(MapIds.HEALED_RYOSHIMA, 37), type=LocationType.UNDERWATER_CHEST_SHALLOW),
        "Ryoshima Coast - Northern underwater Clam between shimenawa rocks": LocData(
            container_check_id(MapIds.HEALED_RYOSHIMA, 38), type=LocationType.UNDERWATER_CHEST_SHALLOW),
        "Ryoshima Coast - Clam on easternmost rocks": LocData(container_check_id(MapIds.HEALED_RYOSHIMA, 25)),
        "Ryoshima Coast - Underwater Clam on southernmost rocks": LocData(
            container_check_id(MapIds.HEALED_RYOSHIMA, 35), type=LocationType.UNDERWATER_CHEST),
        "Ryoshima Coast - Clam on rocks northwest of shimenawa rocks": LocData(
            container_check_id(MapIds.HEALED_RYOSHIMA, 39)),
        "Ryoshima Coast - North Underwater clam on rocks northwest of shimenawa rocks": LocData(
            container_check_id(MapIds.HEALED_RYOSHIMA, 40), type=LocationType.UNDERWATER_CHEST_SHALLOW),
        "Ryoshima Coast - South Underwater clam on rocks northwest of shimenawa rocks": LocData(
            container_check_id(MapIds.HEALED_RYOSHIMA, 41), type=LocationType.UNDERWATER_CHEST_SHALLOW),
        # For whatever reason, the ship is on opposite sides between the map and in game.
        "Ryoshima Coast - Underwater clam on underwater rocks east of sunken ship": LocData(
            container_check_id(MapIds.HEALED_RYOSHIMA, 42), type=LocationType.UNDERWATER_CHEST),
        "Ryoshima Coast - Underwater clam on underwater rocks south of ultimate origin mirror": LocData(
            container_check_id(MapIds.HEALED_RYOSHIMA, 43), type=LocationType.UNDERWATER_CHEST),
        "Ryoshima Coast - Underwater Clam on easternmost rocks": LocData(
            container_check_id(MapIds.HEALED_RYOSHIMA, 44), type=LocationType.UNDERWATER_CHEST_SHALLOW),
        "Ryoshima Coast - Underwater Clam on easternmost underwater rocks": LocData(
            container_check_id(MapIds.HEALED_RYOSHIMA, 45), type=LocationType.UNDERWATER_CHEST_SHALLOW),
        "Ryoshima Coast - East Underwater Clam on rocks south of Sunken Ship": LocData(
            container_check_id(MapIds.HEALED_RYOSHIMA, 46), type=LocationType.UNDERWATER_CHEST_SHALLOW),
        "Ryoshima Coast - West Underwater Clam on rocks south of Sunken Ship": LocData(
            container_check_id(MapIds.HEALED_RYOSHIMA, 47), type=LocationType.UNDERWATER_CHEST_SHALLOW),
    },
    RegionNames.RYOSHIMA_COAST_DOJO: {
        "Ryoshima Coast - Stone Buried Chest near Dojo": LocData(container_check_id(MapIds.HEALED_RYOSHIMA, 6),
                                                                 type=LocationType.STONE_BURIED_CHEST),
        "Ryoshima Coast - Chest on top of dojo Lunar Turret": LocData(container_check_id(MapIds.HEALED_RYOSHIMA, 29),
                                                                      required_items_events=[
                                                                          "Holy Eagle"]),
        "Ryoshima Coast - Freestanding chest on bottom of dojo island": LocData(
            container_check_id(MapIds.HEALED_RYOSHIMA, 30))
    },
    RegionNames.RYOSHIMA_COAST_SHIP_TOP: {
        "Ryoshima Coast - Left Chest on top of Sunken Ship": LocData(container_check_id(MapIds.HEALED_RYOSHIMA, 20)),
        "Ryoshima Coast - Right Chest on top of Sunken Ship": LocData(container_check_id(MapIds.HEALED_RYOSHIMA, 21))
    },
    RegionNames.RYOSHIMA_COAST_CATWALK_TOWER: {
        "Ryoshima Coast - Chest on top of catwalk tower": LocData(container_check_id(MapIds.HEALED_RYOSHIMA, 22))
    },
    RegionNames.RYOSHIMA_COAST_SEIAN: {
        "Ryoshima Coast - Buried chest on ledge near Seian city entrance": LocData(
            container_check_id(MapIds.HEALED_RYOSHIMA, 33), type=LocationType.BURIED_CHEST),
        "Ryoshima Coast - Freestanding chest near Seian city entrance stake fence": LocData(
            container_check_id(MapIds.HEALED_RYOSHIMA, 34))
    },
    RegionNames.RYOSHIMA_COAST_LUNAR_LAGOON: {
        "Ryoshima Coast - Buried Clam behind Sunken ship": LocData(container_check_id(MapIds.HEALED_RYOSHIMA, 36),
                                                                   type=LocationType.BURIED_CHEST),
        "Ryoshima Coast - Buried Clam in front of Sunken ship": LocData(container_check_id(MapIds.HEALED_RYOSHIMA, 48),
                                                                        type=LocationType.BURIED_CHEST),
        "Ryoshima Coast - Buried Clam in Lunar lagoon near rocks": LocData(
            container_check_id(MapIds.HEALED_RYOSHIMA, 50),
            type=LocationType.BURIED_CHEST),
    },
    RegionNames.RYOSHIMA_COAST_WEST_PIER: {
        "Ryoshima Coast - Underwater clam, west of Pier": LocData(container_check_id(MapIds.HEALED_RYOSHIMA, 54),
                                                                  type=LocationType.UNDERWATER_CHEST_SHALLOW),
    },
    RegionNames.ANKOKU_TEMPLE: {
        "Ryoshima Coast - Chest inside Ankoku Temple": LocData(container_check_id(MapIds.HEALED_RYOSHIMA, 63))
    }

}

shop_locations = {
    RegionNames.RYOSHIMA_COAST: {
        "Ryoshima Coast - Shop Slot 1": LocData(shop_check_id(14, 0), type=LocationType.SHOP),
        "Ryoshima Coast - Shop Slot 2": LocData(shop_check_id(14, 1), type=LocationType.SHOP),
        "Ryoshima Coast - Shop Slot 3": LocData(shop_check_id(14, 2), type=LocationType.SHOP),
        "Ryoshima Coast - Shop Slot 4": LocData(shop_check_id(14, 3), type=LocationType.SHOP),
        "Ryoshima Coast - Shop Slot 5": LocData(shop_check_id(14, 4), type=LocationType.SHOP),
        "Ryoshima Coast - Shop Slot 6": LocData(shop_check_id(14, 5), type=LocationType.SHOP),
        "Ryoshima Coast - Shop Slot 7": LocData(shop_check_id(14, 6), type=LocationType.SHOP),
        "Ryoshima Coast - Shop Slot 8": LocData(shop_check_id(14, 7), type=LocationType.SHOP),
        "Ryoshima Coast - Shop Slot 9": LocData(shop_check_id(14, 8), type=LocationType.SHOP),
        "Ryoshima Coast - Shop Slot 10": LocData(shop_check_id(14, 9), type=LocationType.SHOP),
        "Ryoshima Coast - Shop Slot 11": LocData(shop_check_id(14, 10), type=LocationType.SHOP),
        "Ryoshima Coast - Shop Slot 12": LocData(shop_check_id(14, 11), type=LocationType.SHOP),
    }
}

warps = {
    RegionNames.RYOSHIMA_COAST: [
        WarpData(type=WarpType.MERMAID_SPRING,
                 trigger_warp_to=Has("Ryoshima Coast - Clear Devil Gate near North Ryoshima Coast Entrance"),
                 trigger_warp_from=Has("Ryoshima Coast - Clear Devil Gate near North Ryoshima Coast Entrance")),
    ]
}
