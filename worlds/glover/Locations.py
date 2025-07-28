import json
from BaseClasses import Entrance, Location, MultiWorld, Region
from typing import List, NamedTuple
from operator import attrgetter

from worlds.glover import GloverWorld

move_name = [
    "Cartwheel",
    "Crawl",
    "Double Jump",
    "Fist Slam",
    "Ledge",
    "Push",
    "Locate Garib",
    "Locate Ball",
    "Dribble",
    "Quick Swap",
    "Slap",
    "Throw",
    "Lob Ball",
    "Rubber Ball",
    "Bowling Ball",
    "Ball Bearing",
    "Crystal",
    "Beachball",
    "Death Potion",
    "Helicopter Potion",
    "Frog Potion",
    "Boomerang Ball",
    "Speed Potion",
    "Sticky Potion",
    "Hercules Potion",
    "Jump",
    "Not Crystal",
    "Not Bowling",
    "Sinks",
    "Floats",
    "Grab",
    "Ball Up",
    "Power Ball"
]

levels_in_order = [
#    ["AtlH", ],
    ["Atl1", "Floor", "Floor"]
#    ["Atl2", ],
#    ["Atl3", ],
#    ["Atl!", ],
#    ["Atl?", ],
#    ["CrnH", ],
#    ["Crn1", ],
#    ["Crn2", ],
#    ["Crn3", ],
#    ["Crn!", ],
#    ["Crn?", ],
#    ["PrtH", ],
#    ["Prt1", ],
#    ["Prt2", ],
#    ["Prt3", ],
#    ["Prt!", ],
#    ["Prt?", ],
#    ["PhtH", ],
#    ["Pht1", ],
#    ["Pht2", ],
#    ["Pht3", ],
#    ["Pht!", ],
#    ["Pht?", ],
#    ["FoFH", ],
#    ["FoF1", ],
#    ["FoF2", ],
#    ["FoF3", ],
#    ["FoF!", ],
#    ["FoF?", ],
#    ["OoWH", ],
#    ["OoW1", ],
#    ["OoW2", ],
#    ["OoW3", ],
#    ["OoW!", ],
#    ["OoW?", ],
#    ["Hubworld", "Main"],
#    ["Castle Cave", "Main"],
#    ["Training", "Start"]
]

class GloverLocation(Location):
    game : str = "Glover"

class AccessMethod(NamedTuple):
    region_name : str
    ball_in_region : bool
    difficulty : int
    required_items : list

def build_logic(player : int, multiworld : MultiWorld, spawn_checkpoint : List[int]):
    #Build Logic
    logic_file = open('Logic.json')
    logic_data = json.load(logic_file)
    loc_con_index = 0
    map_levels : List[RegionLevel] = []
    for world_index in 1:
        world_prefix : str = GloverWorld.world_prefixes[world_index]
        each_world = logic_data[world_index]
        #Go over the Glover worlds
        for level_key in each_world:
            each_level = each_world[level_key]
            checkpoint_entry_pairs = levels_in_order[loc_con_index]
            loc_con_index += 1
            level_prefix = GloverWorld.level_prefixes[int(level_key[-1])]
            level_name : str = world_prefix + level_prefix
            prefix : str = level_name + ": "
            map_regions : List[RegionPair] = []
            location_data_list : List[LocationData] = []
            #Get the check name
            for check_name in each_level:
                check_info = each_level[check_name]
                #Location
                if type(check_info) is list:
                    location_data_list.append(create_location_data(check_name, check_info, prefix))
                        
                #In-Level Region
                if type(check_info) is dict:
                    map_regions.append(create_region_pair(check_info, prefix, check_name, level_name, player, multiworld))
                    #You get the one from checkpoints by default
                    region_checkpoints = []
                    for check_index in range(1, checkpoint_entry_pairs.count()):
                        matching_name = checkpoint_entry_pairs[check_index]
                        if matching_name == check_name:
                            region_checkpoints.append(prefix + "Checkpoint" + str(check_index))
            #Sort the in-level regions
            map_regions = sorted(map_regions, key=attrgetter('base_id'))
            connect_region_pairs(map_regions)
            #Create the level info attached to it
            region_level : RegionLevel = create_region_level(level_name, spawn_checkpoint, player, multiworld)
            map_levels.append(region_level)
            #Attach the locations to the regions
            assign_locations_to_regions(region_level, map_regions, location_data_list)

class LocationData(NamedTuple):
    name : str
    ap_ids : List[int]
    rom_ids : List[int]
    methods : List[AccessMethod]

def create_location_data(check_name : str, check_info : list, prefix : str) -> LocationData:
    for check_pairing in check_info:
        both_ids = check_pairing[0]
        methods : List[AccessMethod] = []
        if check_pairing.count() > 1:
            for each_method in check_pairing[1]:
                methods.append(create_access_method(each_method, prefix))
    return LocationData(prefix + check_name, both_ids["AP_IDS"], both_ids["IDS"], methods)

class RegionPair(NamedTuple):
    name : str
    base_id : int
    ball_region : Region
    ball_region_methods : list[AccessMethod]
    no_ball_region : Region
    no_ball_region_methods : list[AccessMethod]

def create_region_pair(check_info : dict, check_name : str, level_name : str, player : int, multiworld : MultiWorld) -> RegionPair:
    prefix = level_name + ": "
    region_name = prefix + check_name
    ball_region_methods : list[AccessMethod] = []
    no_ball_region_methods : list[AccessMethod] = []
    base_id : int = check_info["I"]
    for check_pairing in check_info["B"]:
        #ids = check_pairing[0]
        if check_pairing.count() > 1:
            for each_method in check_pairing[1]:
                ball_region_methods.append(create_access_method(each_method, prefix))
    ball_region = Region(prefix + level_name, player, multiworld, level_name)
    for check_pairing in check_info["D"]:
        #ids = check_pairing[0]
        if check_pairing.count() > 1:
            for each_method in check_pairing[1]:
                no_ball_region_methods.append(create_access_method(each_method, prefix))
    no_ball_region = Region(prefix + level_name, player, multiworld, level_name)
    return RegionPair(region_name, base_id, ball_region, ball_region_methods, no_ball_region, no_ball_region_methods)

def connect_region_pairs(pairs : List[RegionPair]):
    for each_pair in pairs:
        for each_method in each_pair.ball_region_methods:
            each_method.region_name
        for each_method in each_pair.no_ball_region_methods:
            each_method.region_name

class RegionLevel(NamedTuple):
    name : str
    region : Region
    map_regions : List[RegionPair]

def create_region_level(level_name, spawn_checkpoint : List[int] | None, starting_checkpoint : int | None, map_regions : List[RegionPair], player : int, multiworld : MultiWorld, self : GloverWorld):
    #By default, the region level leads to the first checkpoint's region
    level_checkpoint_region : List[str] = levels_in_order[level_name]
    default_region : int = 0
    region : Region = Region(level_name, player, multiworld)

    #Check if it's a core level
    level_offset : int | None = None
    match level_name[3:4]:
        case "1":
            level_offset = 0
        case "2":
            level_offset = 1
        case "3":
            level_offset = 2
    
    #Get the checkpoint from the core levels
    if type(level_offset) is int:
        world_offset : int = self.world_from_string(level_name)
        default_region : int = spawn_checkpoint[level_offset + (world_offset * 3)] - 1

    #See if you get the ball with the checkpoint
    start_without_ball : bool = level_offset == 0 or level_name[:3] == "OoW"
    
    #Assign entrances required by checkpoints here
    for region_index in level_checkpoint_region.count():
        checkpoint_name : str = level_name + " Checkpoint " + str(region_index + 1)
        level_entrances : Entrance = region.create_exit(checkpoint_name)
        region_pair : RegionPair = map_regions[region_index]
        connecting_region : Region
        if start_without_ball:
            connecting_region = region_pair.no_ball_region
        else:
            connecting_region = region_pair.ball_region
        level_entrances.connect(connecting_region)
        #Let's not think about access rules yet
        #if default_region != region_index:
        #    level_entrances.access_rule

    return RegionLevel(level_name, region, starting_checkpoint, map_regions)

def create_access_method(info : dict, prefix : str) -> AccessMethod:
    required_moves : list = []
    for each_key in info:
        if each_key.startswith("mv"):
            required_moves.append(move_name[info[each_key]])
        if each_key.startswith("ck"):
            required_moves.append(prefix + info[each_key])
    info["regionIndex"]
    return AccessMethod(info["regionIndex"], info["ballRequirement"], info["trickDifficulty"], required_moves)

def assign_locations_to_regions(region_level : RegionLevel, map_regions : List[RegionPair], location_data_list : List[LocationData], player : int, multiworld : MultiWorld):
    for each_location_data in location_data_list:
        #Is this a mono location?
        location_regions : List[str] = []
        for each_method in each_location_data.methods:
            region_name = each_method.region_name
            if each_method.ball_in_region:
                region_name = region_name + " W/Ball"
            if not region_name in location_regions:
                location_regions.append(region_name)
        #Depending on if it is or not
        region_for_use : Region
        if location_regions.count() > 1:
            #Multi location construction creates a shared region to reach this location
            region_for_use = Region(each_location_data.name + " Region", player, multiworld, region_level.name)
        else:
            #Single location construction assigns to the specific element in the RegionPair
            region_for_use = map_regions[0]
        #Construct location data
        #The garib sorting stuff has to go here! Don't forget to do that later
        locations : List[Location] = []
        if each_location_data.ap_ids.count() == 1:
            #If the location data accounts for 1 location
            locations.append(Location(player, each_location_data.name, each_location_data.ap_ids[0], region_for_use))
        else:
            #If the location accounts for multiple locations
            for each_ap_id_index in each_location_data.ap_ids.count():
                each_ap_id = each_location_data.ap_ids[each_ap_id_index]
                sublocation_name : str = each_location_data.name
                sublocation_name.removesuffix("s")
                locations.append(Location(player, sublocation_name + " " + str(each_ap_id_index + 1), each_ap_id, region_for_use))
        