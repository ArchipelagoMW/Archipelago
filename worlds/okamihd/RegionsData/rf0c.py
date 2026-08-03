from typing import TYPE_CHECKING

from rule_builder.rules import Has, Or, True_
from ..CheckIds import shop_check_id, container_check_id, brush_check_id
from ..Enums.BrushTechniques import BrushTechniques
from ..Enums.LocationType import LocationType
from ..Enums.OkamiEnemies import OkamiEnemies
from ..Enums.WarpType import WarpType
from ..Rules import long_swim_rule, n_ryoshima_guardian_sapling_rule, n_ryoshima_islands_dragon_rule, \
    night_time_check_rule
from ..Types import ExitData, EventData, LocData, WarpData
from ..Enums.RegionNames import RegionNames, MapIds

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    RegionNames.NORTHERN_RYOSHIMA_COAST_MANDATORY_FIGHT: [
        ExitData(RegionNames.RYOSHIMA_COAST_SEIAN, one_way=True, loading_screen=False,
                 required_items_events=["Northern Ryoshima Coast - Mandatory Earth Nose Fight"]),
        ExitData(RegionNames.NORTHERN_RYOSHIMA_COAST, one_way=True, loading_screen=False,
                 required_items_events=["Northern Ryoshima Coast - Mandatory Earth Nose Fight"])
    ],
    RegionNames.NORTHERN_RYOSHIMA_COAST: [
        ExitData(RegionNames.NORTHERN_RYOSHIMA_COAST_MANDATORY_FIGHT, one_way=True, loading_screen=False),
        ExitData(RegionNames.NORTHERN_RYOSHIMA_COAST_WATCHERS_ENCOUNTER, one_way=True, loading_screen=False,required_items_events=["Northern Ryoshima Coast - Climb to Watcher's Cape"]),
        # Special rule to account for Orca
        ExitData(RegionNames.NORTHERN_RYOSHIMA_COAST_SAPLING, loading_screen=False,
                 special_rule=n_ryoshima_guardian_sapling_rule),
        ExitData(RegionNames.NORTHERN_RYOSHIMA_COAST_TOMB, loading_screen=False, one_way=True,
                 required_items_events=["Northern Ryoshima Coast - Climb to Tomb Cave"]),
        ExitData(RegionNames.NORTHERN_RYOSHIMA_COAST_WESTERN_ISLAND, loading_screen=False,
                 special_rule=n_ryoshima_islands_dragon_rule),
        ExitData(RegionNames.NORTHERN_RYOSHIMA_COAST_CATCALL_NORTH, loading_screen=False,
                 special_rule=n_ryoshima_islands_dragon_rule),
        ExitData(RegionNames.NORTHERN_RYOSHIMA_COAST_UMI),
        ExitData(RegionNames.NORTHERN_RYOSHIMA_COAST_CB2_ISLAND, loading_screen=False,
                 special_rule=n_ryoshima_islands_dragon_rule),
        ExitData(RegionNames.NORTHERN_RYOSHIMA_COAST_PS2_ISLAND, loading_screen=False,
                 special_rule=n_ryoshima_islands_dragon_rule),
        ExitData(RegionNames.NORTHERN_RYOSHIMA_COAST_BANDIT_SPIDER_ISLAND, loading_screen=False,
                 special_rule=n_ryoshima_islands_dragon_rule),
        ExitData(RegionNames.NORTHERN_RYOSHIMA_COAST_SEA, loading_screen=False,
                 special_rule=n_ryoshima_islands_dragon_rule),
        ExitData(RegionNames.NORTHERN_RYOSHIMA_COAST_CATCALL_ISLAND, loading_screen=False,
                 special_rule=n_ryoshima_islands_dragon_rule),
        ExitData(RegionNames.NORTHERN_RYOSHIMA_COAST_TREASURE_CAVE,
                 required_items_events=["Northern Ryoshima Coast - Open Treasure Cave"]),
        ExitData(RegionNames.DRAGON_PALACE, loading_screen=False,
                 special_rule=n_ryoshima_islands_dragon_rule,required_items_events=["Northern Ryoshima Coast - Open Whirlpool"]),

    ],
    RegionNames.NORTHERN_RYOSHIMA_COAST_WATCHERS_ENCOUNTER: [
        ExitData(RegionNames.NORTHERN_RYOSHIMA_COAST_WATCHERS, one_way=True, loading_screen=False,
                 required_items_events=["Northern Ryoshima Coast - Mandatory encounter in Watcher's Cape"])
    ],
    RegionNames.NORTHERN_RYOSHIMA_COAST_WATCHERS: [
        ExitData(RegionNames.NORTHERN_RYOSHIMA_COAST, one_way=True, loading_screen=False),
        ExitData(RegionNames.ONI_ISLAND_ENTRANCE, required_items_events=["Himiko's Palace - Get Oni Island Location"])
    ],
    RegionNames.NORTHERN_RYOSHIMA_COAST_TOMB: [
        ExitData(RegionNames.NORTHERN_RYOSHIMA_COAST, one_way=True, loading_screen=False)
    ],
    RegionNames.NORTHERN_RYOSHIMA_COAST_PS2_ISLAND: [
        ExitData(RegionNames.NORTHERN_RYOSHIMA_COAST_PS2_CAVE,
                 required_items_events=["Northern Ryoshima Coast - Open Power Slash 2 Cave"])
    ],
    RegionNames.NORTHERN_RYOSHIMA_COAST_CB2_ISLAND: [
        ExitData(RegionNames.NORTHERN_RYOSHIMA_COAST_CB2_CAVE,
                 required_items_events=["Northern Ryoshima Coast - Open Cherry Bomb 2 Cave"])
    ],
    RegionNames.NORTHERN_RYOSHIMA_COAST_BANDIT_SPIDER_ISLAND: [
        ExitData(RegionNames.NORTHERN_RYOSHIMA_COAST_BANDIT_SPIDER_CAVE,
                 required_items_events=["Northern Ryoshima Coast - Open Bandit Spider Cave"],
                 one_way=True)
    ],
    RegionNames.NORTHERN_RYOSHIMA_COAST_CATCALL_ISLAND:[
        ExitData(RegionNames.CATCALL_TOWER_BOTTOM)
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
        "Northern Ryoshima Coast - Meet Orca": EventData(required_brush_techniques=[BrushTechniques.SUNRISE],
                                                         event_item_name="Orca"),
        "Northern Ryoshima Coast - Open Treasure Cave": EventData(required_items_events=["Digging Champ"]),
    },
    RegionNames.NORTHERN_RYOSHIMA_COAST_WATCHERS_ENCOUNTER: {
        "Northern Ryoshima Coast - Mandatory encounter in Watcher's Cape": EventData(
            mandatory_enemies=[OkamiEnemies.BLUE_CYCLOPS]),
    },
    RegionNames.NORTHERN_RYOSHIMA_COAST_WATCHERS:{
        "Northern Ryoshima Coast - Open Whirlpool":EventData(required_brush_techniques=[BrushTechniques.GALESTORM],special_rule=night_time_check_rule),
        "Northern Ryoshima Coast - Open Bridge to Oni Island":EventData(required_items_events=["Himiko's Palace - Get Oni Island Location"])
    },
    RegionNames.NORTHERN_RYOSHIMA_COAST_WESTERN_ISLAND: {
        "Northern Ryoshima Coast - Fish Marlin": EventData(
            type=LocationType.FISHING_MINIGAME,
            required_items_events=["Marlin Rod"])
    },
    RegionNames.NORTHERN_RYOSHIMA_COAST_PS2_ISLAND: {
        "Northern Ryoshima Coast - Open Power Slash 2 Cave": EventData(power_slash_level=1)
    },
    RegionNames.NORTHERN_RYOSHIMA_COAST_CB2_ISLAND: {
        "Northern Ryoshima Coast - Open Cherry Bomb 2 Cave": EventData(cherry_bomb_level=1)
    },
    RegionNames.NORTHERN_RYOSHIMA_COAST_BANDIT_SPIDER_ISLAND: {
        "Northern Ryoshima Coast - Open Bandit Spider Cave": EventData(required_items_events=["Digging Champ"])
    }
}
locations = {
    RegionNames.NORTHERN_RYOSHIMA_COAST_UMI: {
        "Northern Ryoshima Coast - Kazegami (Whirlwind)": LocData(
            brush_check_id(7), required_items_events=["Northern Ryoshima Coast - Fish Marlin"],
            type=LocationType.CONSTELLATION),
        "Northern Ryoshima Coast - Chest after Whirlwind": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 0),
            required_items_events=["Northern Ryoshima Coast - Fish Marlin"]),
    },
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
    },
    RegionNames.NORTHERN_RYOSHIMA_COAST_CATCALL_NORTH: {
        "Northern Ryoshima Coast - Southern Buried Chest on island north of catcall tower": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 11), type=LocationType.BURIED_CHEST),
        "Northern Ryoshima Coast - Northern Buried Chest on island north of catcall tower": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 91), type=LocationType.BURIED_CHEST),
    },
    RegionNames.NORTHERN_RYOSHIMA_COAST_CB2_ISLAND: {
        "Northern Ryoshima Coast - Burning Chest on Cherry Bomb 2 Island": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 12), type=LocationType.BURNING_CHEST),
    },
    RegionNames.NORTHERN_RYOSHIMA_COAST_WESTERN_ISLAND: {
        "Northern Ryoshima Coast - Buried Chest on Westernmost island beach": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 17), type=LocationType.BURIED_CHEST),
        "Northern Ryoshima Coast - Freestanding Chest on Westernmost island": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 24)),
        "Northern Ryoshima Coast - Underwater Clam on Westernmost island beach 2": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 75), type=LocationType.UNDERWATER_CHEST_SHALLOW),
        "Northern Ryoshima Coast - Underwater Clam on Westernmost island beach 3": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 76), type=LocationType.UNDERWATER_CHEST_SHALLOW),
        "Northern Ryoshima Coast - Underwater Clam on Westernmost island beach 1": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 77), type=LocationType.UNDERWATER_CHEST_SHALLOW),
        "Northern Ryoshima Coast - Buried Chest on Westernmost island": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 83), type=LocationType.BURIED_CHEST),
    },
    RegionNames.NORTHERN_RYOSHIMA_COAST_BANDIT_SPIDER_ISLAND: {
        "Northern Ryoshima Coast - Buried Chest on bandit spider island": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 25), type=LocationType.BURIED_CHEST),
    },
    # All of these require Orca, even though you can get some without - This is for bot my and the player's sanity
    RegionNames.NORTHERN_RYOSHIMA_COAST_SEA: {
        "Northern Ryoshima Coast - Underwater Clam on rocks west of watcher's cape": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 95), type=LocationType.UNDERWATER_CHEST),
        "Northern Ryoshima Coast - Underwater Clam on rocks north of Guardian Sapling": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 96), type=LocationType.UNDERWATER_CHEST),
        "Northern Ryoshima Coast - Underwater Clam on rocks southwest of watcher's cape": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 97), type=LocationType.UNDERWATER_CHEST),
        "Northern Ryoshima Coast - Underwater Clam on rocks north of bandit spider island": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 98), type=LocationType.UNDERWATER_CHEST),
        "Northern Ryoshima Coast - Underwater Clam on rocks west of watcher's cape 2": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 99), type=LocationType.UNDERWATER_CHEST),
        "Northern Ryoshima Coast - Underwater Clam on rocks between Power Slash 2 and Cherry Bomb 2 Island 1": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 100), type=LocationType.UNDERWATER_CHEST),
        "Northern Ryoshima Coast - Underwater Clam on rocks between Power Slash 2 and Cherry Bomb 2 Island 2": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 101), type=LocationType.UNDERWATER_CHEST),
        "Northern Ryoshima Coast - Underwater Clam on rocks north of Catcall Tower": LocData(
            container_check_id(MapIds.NORTHERN_RYOSHIMA, 102), type=LocationType.UNDERWATER_CHEST)
    }
}
warps = {
    RegionNames.NORTHERN_RYOSHIMA_COAST: [
        WarpData(WarpType.MIST_WARP, Has("Mist Warp Unlock - North Ryoshima Coast"),
                 True_),
        WarpData(WarpType.MERMAID_SPRING, Has("Mist Warp Unlock - North Ryoshima Coast (Rocky Area)"),
                 True_)
    ],
    RegionNames.NORTHERN_RYOSHIMA_COAST_MIST_WARP: [
        WarpData(WarpType.MIST_WARP, Has("Mermaid Sping Unlock - Northen Ryoshima Coast"),
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
