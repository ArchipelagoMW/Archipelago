import json
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional
from BaseClasses import MultiWorld, Region, Entrance


class LandstalkerRegion(Region):
    code: str

    def __init__(self, code: str, name: str, player: int, multiworld: MultiWorld, hint: Optional[str] = None):
        super().__init__(name, player, multiworld, hint)
        self.code = code


class LandstalkerRegionData(NamedTuple):
    locations: Optional[List[str]]
    region_exits: Optional[List[str]]


def create_regions(multiworld: MultiWorld, player: int):
    regions_table: Dict[str, LandstalkerRegion] = {}
    script_folder = Path(__file__)

    # Create the hardcoded starting "Menu" region
    menu_region = LandstalkerRegion("menu", "Menu", player, multiworld)
    regions_table["menu"] = menu_region
    multiworld.regions.append(menu_region)

    # Create regions from world_nodes
    with open((script_folder.parent / "data/world_node.json").resolve(), "r") as file:
        regions_data = json.load(file)
        for code, region_data in regions_data.items():
            region = LandstalkerRegion(code, region_data["name"], player, multiworld)
            regions_table[code] = region
            multiworld.regions.append(region)

    # Create exits/entrances from world_paths
    with open((script_folder.parent / "data/world_path.json").resolve(), "r") as file:
        entrances_data = json.load(file)
        for data in entrances_data:
            two_way = data["twoWay"] if "twoWay" in data else False
            create_entrance(data["fromId"], data["toId"], two_way, player, regions_table)

    # Create a path between the fake Menu location and the starting location
    starting_region = get_starting_region(multiworld, player, regions_table)
    game_entrance = Entrance(player, "menu -> " + starting_region.code, menu_region)
    menu_region.exits.append(game_entrance)
    game_entrance.connect(starting_region)

    # If Gumi boulder is removed, add a path from "route_gumi_ryuma" to "gumi"
    if multiworld.remove_gumi_boulder[player].value is True:
        create_entrance("route_gumi_ryuma", "gumi", False, player, regions_table)

    # If enemy jumping is in logic, Mountainous Area can be reached from route to Lake Shrine by doing a "ghost jump"
    # at crossroads map
    if multiworld.handle_enemy_jumping_in_logic[player].value is True:
        create_entrance("route_lake_shrine", "route_lake_shrine_cliff", False, player, regions_table)

    # If using Einstein Whistle behind trees is allowed, add a new logic path there to reflect that change
    if multiworld.allow_whistle_usage_behind_trees[player].value is True:
        create_entrance("greenmaze_post_whistle", "greenmaze_pre_whistle", False, player, regions_table)

    return regions_table


def create_entrance(from_id: str, to_id: str, two_way: bool, player: int, regions_table: Dict[str, LandstalkerRegion]):
    name = from_id + " -> " + to_id
    from_region = regions_table[from_id]
    to_region = regions_table[to_id]

    entrance = Entrance(player, name, from_region)
    from_region.exits.append(entrance)
    entrance.connect(to_region)

    # If two-way, also create a reverse path
    if two_way:
        reverse_name = to_id + " -> " + from_id
        entrance = Entrance(player, reverse_name, to_region)
        to_region.exits.append(entrance)
        entrance.connect(from_region)

def get_starting_region(multiworld: MultiWorld, player: int, regions_table: Dict[str, LandstalkerRegion]):
    spawn_id = multiworld.spawn_region[player].value
    region_id = "massan"

    script_folder = Path(__file__)
    with open((script_folder.parent / "data/spawn_location.json").resolve(), "r") as file:
        spawns_data = json.load(file)
        for current_id, data in spawns_data.items():
            if current_id == spawn_id:
                region_id = data["nodeId"]
                break

    return regions_table[region_id]


def get_darkenable_regions():
    darkenable_region_ids = {}
    script_folder = Path(__file__)
    with open((script_folder.parent / "data/world_region.json").resolve(), "r") as file:
        regions_data = json.load(file)
        for data in regions_data:
            if "darkMapIds" in data:
                darkenable_region_ids[data["name"]] = data["nodeIds"]
    return darkenable_region_ids
