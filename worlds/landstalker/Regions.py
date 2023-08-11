from typing import Dict, List, NamedTuple, Optional
from BaseClasses import MultiWorld, Region, Entrance
from .data.world_node import WORLD_NODES_JSON
from .data.world_path import WORLD_PATHS_JSON
from .data.world_region import WORLD_REGIONS_JSON
from .data.world_teleport_tree import WORLD_TELEPORT_TREES_JSON


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

    # Create the hardcoded starting "Menu" region
    menu_region = LandstalkerRegion("menu", "Menu", player, multiworld)
    regions_table["menu"] = menu_region
    multiworld.regions.append(menu_region)

    # Create regions from world_nodes
    for code, region_data in WORLD_NODES_JSON.items():
        random_hint_name = None
        if "hints" in region_data:
            random_hint_name = multiworld.random.choice(region_data["hints"])
        region = LandstalkerRegion(code, region_data["name"], player, multiworld, random_hint_name)
        regions_table[code] = region
        multiworld.regions.append(region)

    # Create exits/entrances from world_paths
    for data in WORLD_PATHS_JSON:
        two_way = data["twoWay"] if "twoWay" in data else False
        create_entrance(data["fromId"], data["toId"], two_way, player, regions_table)

    # Create a path between the fake Menu location and the starting location
    starting_region = get_starting_region(multiworld, player, regions_table)
    menu_region.connect(starting_region, f"menu -> {starting_region.code}")

    add_specific_paths(multiworld, player, regions_table)

    return regions_table


def add_specific_paths(multiworld: MultiWorld, player: int, regions_table: Dict[str, LandstalkerRegion]):
    # If Gumi boulder is removed, add a path from "route_gumi_ryuma" to "gumi"
    if multiworld.remove_gumi_boulder[player].value == 1:
        create_entrance("route_gumi_ryuma", "gumi", False, player, regions_table)

    # If enemy jumping is in logic, Mountainous Area can be reached from route to Lake Shrine by doing a "ghost jump"
    # at crossroads map
    if multiworld.handle_enemy_jumping_in_logic[player].value == 1:
        create_entrance("route_lake_shrine", "route_lake_shrine_cliff", False, player, regions_table)

    # If using Einstein Whistle behind trees is allowed, add a new logic path there to reflect that change
    if multiworld.allow_whistle_usage_behind_trees[player].value == 1:
        create_entrance("greenmaze_post_whistle", "greenmaze_pre_whistle", False, player, regions_table)


def create_entrance(from_id: str, to_id: str, two_way: bool, player: int, regions_table: Dict[str, LandstalkerRegion]):
    created_entrances = []

    name = from_id + " -> " + to_id
    from_region = regions_table[from_id]
    to_region = regions_table[to_id]

    entrance = Entrance(player, name, from_region)
    from_region.exits.append(entrance)
    entrance.connect(to_region)
    created_entrances.append(entrance)

    # If two-way, also create a reverse path
    if two_way:
        reverse_name = to_id + " -> " + from_id
        entrance = Entrance(player, reverse_name, to_region)
        to_region.exits.append(entrance)
        entrance.connect(from_region)
        created_entrances.append(entrance)

    return created_entrances


def get_starting_region(multiworld: MultiWorld, player: int, regions_table: Dict[str, LandstalkerRegion]):
    # Most spawn locations have the same name as the region they are bound to, but a few vary.
    spawn_id = multiworld.spawn_region[player].value
    if spawn_id == "waterfall":
        return regions_table["greenmaze_post_whistle"]
    elif spawn_id == "kado":
        return regions_table["route_gumi_ryuma"]
    elif spawn_id == "greenmaze":
        return regions_table["greenmaze_pre_whistle"]
    return regions_table[spawn_id]


def get_darkenable_regions():
    return {data["name"]: data["nodeIds"] for data in WORLD_REGIONS_JSON if "darkMapIds" in data}

def load_teleport_trees():
    pairs = []
    for pair in WORLD_TELEPORT_TREES_JSON:
        first_tree = {
            'name': pair[0]["name"],
            'region': pair[0]["nodeId"]
        }
        second_tree = {
            'name': pair[1]["name"],
            'region': pair[1]["nodeId"]
        }
        pairs.append([first_tree, second_tree])
    return pairs
