import json
import pkgutil
from BaseClasses import Entrance, Location, MultiWorld, Region
from typing import List, NamedTuple
from operator import attrgetter

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
    ["Atl1", 0, 0]
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

file = pkgutil.get_data(__name__, "Logic.json").decode("utf-8")

#List of worlds, dictionary of levels, dictionary of locations and regions in those levels
#If it's a list, it's a location. Contains first entry AP_ID/ID, and all other entries methods
#If it's a dictionary, it's a region. B for Ball, D for No Ball, I for Local ID
#B/D in region has AP_ID/IDs, followed by methods as per Locations
logic_data : list[
    dict[str, 
        dict[str, 
            dict[str,
                list[
                    dict[str, any]] | 
                int] |
            list[
                dict[str, any]
    ]]]] = json.loads(file)

class AccessMethod(NamedTuple):
    region_index : int
    ball_in_region : bool
    difficulty : int
    required_items : list

class LocationData(NamedTuple):
    name : str
    ap_ids : List[int]
    rom_ids : List[int]
    methods : List[AccessMethod]

def create_location_data(check_name : str, check_info : list, prefix : str) -> LocationData:
    methods : List[AccessMethod] = []
    for check_index in range(1, len(check_info)):
        check_method = check_info[check_index]
        methods.append(create_access_method(check_method, prefix))
    return LocationData(prefix + check_name, check_info[0]["AP_IDS"], check_info[0]["IDS"], methods)

class RegionPair(NamedTuple):
    name : str
    base_id : int
    ball_region : Region | None
    ball_region_methods : list[AccessMethod]
    no_ball_region : Region | None
    no_ball_region_methods : list[AccessMethod]

def create_region_pair(check_info : dict, check_name : str, level_name : str, player : int, multiworld : MultiWorld) -> RegionPair:
    prefix = level_name + ": "
    region_name = prefix + check_name
    ball_region_methods : list[AccessMethod] = []
    no_ball_region_methods : list[AccessMethod] = []
    base_id : int = check_info["I"]
    ball_region = Region(region_name + " W/Ball", player, multiworld, level_name)

    for index, check_pairing in enumerate(check_info["B"]):
        if index == 0:
            continue
        #ids = check_pairing[0]
        ball_region_methods.append(create_access_method(check_pairing, prefix))
    
    no_ball_region = Region(region_name, player, multiworld, level_name)
    for index, check_pairing in enumerate(check_info["D"]):
        if index == 0:
            continue
        #ids = check_pairing[0]
        no_ball_region_methods.append(create_access_method(check_pairing, prefix))
    return RegionPair(region_name, base_id, ball_region, ball_region_methods, no_ball_region, no_ball_region_methods)

def connect_region_pairs(pairs : List[RegionPair]):
    for each_pair in pairs:
        pair_ball_connections : dict[Region, list[AccessMethod]] = {}
        pair_no_ball_connections : dict[Region, list[AccessMethod]] = {}
        for each_method in each_pair.ball_region_methods:
            region_to_connect : Region = get_region_from_method(pairs, each_method)
            if not region_to_connect in pair_ball_connections.keys():
                pair_ball_connections[region_to_connect] = [each_method]
        for each_method in each_pair.no_ball_region_methods:
            region_to_connect : Region = get_region_from_method(pairs, each_method)
            if not region_to_connect in pair_no_ball_connections.keys():
                pair_no_ball_connections[region_to_connect] = [each_method]
        for each_connection, methods in pair_ball_connections.items():
            #Create the rules using methods
            each_pair.ball_region.connect(each_connection)
        for each_connection, methods in pair_no_ball_connections.items():
            #Create the rules using methods part 2
            each_pair.no_ball_region.connect(each_connection)
        each_pair.ball_region.connect(each_pair.no_ball_region)

class RegionLevel(NamedTuple):
    name : str
    region : Region
    starting_checkpoint : int
    map_regions : List[RegionPair]

def create_region_level(level_name, checkpoint_for_use : int | None, checkpoint_entry_pairs : list, map_regions : List[RegionPair], self):
    #By default, the region level leads to the first checkpoint's region
    
    default_checkpoint : int = 1
    region : Region = Region(level_name, self.player, self.multiworld)

    #Get the checkpoint from the core levels
    if type(checkpoint_for_use) is int:
        default_checkpoint = checkpoint_for_use

    #See if you get the ball with the checkpoint
    start_without_ball : bool = default_checkpoint == 1 or level_name[:3] == "OoW"
    
    #Assign entrances required by checkpoints here
    for checkpoint_number in range(1, len(checkpoint_entry_pairs)):
        checkpoint_name : str = level_name + " Checkpoint " + str(checkpoint_number)
        level_entrances : Entrance = region.create_exit(checkpoint_name)
        connecting_region : Region
        for each_region_pair in map_regions:
            if each_region_pair.base_id == checkpoint_entry_pairs[checkpoint_number]:
                if start_without_ball:
                    connecting_region = each_region_pair.no_ball_region
                else:
                    connecting_region = each_region_pair.ball_region
                break
        level_entrances.connect(connecting_region)
        #Let's not think about access rules yet
        #if default_region != region_index:
        #    level_entrances.access_rule

    level_region : Region = Region(level_name, self.player, self.multiworld)
    return RegionLevel(level_name, level_region, default_checkpoint, map_regions)

def create_access_method(info : dict, prefix : str) -> AccessMethod:
    required_moves : list = []
    for each_key in info:
        if each_key.startswith("mv"):
            required_moves.append(move_name[info[each_key]])
        if each_key.startswith("ck"):
            required_moves.append(prefix + info[each_key])
    info["regionIndex"]
    return AccessMethod(info["regionIndex"], info["ballRequirement"], info["trickDifficulty"], required_moves)

def assign_locations_to_regions(region_level : RegionLevel, map_regions : List[RegionPair], location_data_list : List[LocationData], player : int, multiworld : MultiWorld) -> List[Location]:
    locations : List[Location] = []
    for each_location_data in location_data_list:
        #Is this a mono location?
        location_regions : List[str] = []
        for each_method in each_location_data.methods:
            region_index = each_method.region_index
            region_name : str
            for each_pair in map_regions:
                if region_index == each_pair.base_id:
                    region_name = each_pair.name
            if each_method.ball_in_region:
                region_name = region_name + " W/Ball"
            if not region_name in location_regions:
                location_regions.append(region_name)
        #Depending on if it is or not
        region_for_use : Region
        if len(location_regions) > 1:
            #Multi location construction creates a shared region to reach this location
            region_for_use = Region(each_location_data.name + " Region", player, multiworld, region_level.name)
            for each_region_name in location_regions:
                #Make sure to apply the correct rules here later
                get_region_from_name(map_regions, each_region_name).connect(region_for_use, each_location_data.name + " from " + each_region_name)
        elif len(location_regions) == 1:
            #Single location construction assigns to the specific element in the RegionPair
            region_for_use = get_region_from_name(map_regions, location_regions[0])
        #Construct location data
        #The garib sorting stuff has to go here! Don't forget to do that later
        for each_pairing in build_location_pairings(each_location_data.name, each_location_data.ap_ids):
            locations.append(Location(player, each_pairing[0], each_pairing[1], region_for_use))
    return locations

def get_region_from_method(region_pairs : List[RegionPair], method : AccessMethod) -> Region:
    for each_pair in region_pairs:
        if method.ball_in_region:
            if each_pair.base_id == method.region_index:
                return each_pair.ball_region
        else:
            if each_pair.base_id == method.region_index:
                return each_pair.no_ball_region


def get_region_from_name(region_pairs : List[RegionPair], lookup_key : str) -> Region:
    ball_region : bool = lookup_key.endswith("W/Ball")
    for each_pair in region_pairs:
        if ball_region:
            if each_pair.name + " W/Ball" == lookup_key:
                return each_pair.ball_region
        else:
            if each_pair.name == lookup_key:
                return each_pair.no_ball_region

class JsonInfo(NamedTuple):
    all_levels : List[RegionLevel] = []
    locations : List[Location] = []

def build_data(self) -> JsonInfo:
    all_levels : List[RegionLevel] = []
    locations : List[Location] = []

    #Build Logic
    loc_con_index = 0
    for world_index in range(1):
        world_prefix : str = self.world_prefixes[world_index]
        each_world = logic_data[world_index]
        #Go over the Glover worlds
        for level_key in each_world:
            each_level = each_world[level_key]
            checkpoint_entry_pairs : list = levels_in_order[loc_con_index]
            loc_con_index += 1
            level_int : int = int(level_key[-1])
            level_prefix = self.level_prefixes[level_int]
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
                    new_region_pair = create_region_pair(check_info, check_name, level_name, self.player, self.multiworld)
                    map_regions.append(new_region_pair)
                    #You get the one from checkpoints by default
                    region_checkpoints = []
                    for check_index in range(1, len(checkpoint_entry_pairs)):
                        matching_name = checkpoint_entry_pairs[check_index]
                        if matching_name == check_name:
                            region_checkpoints.append(prefix + "Checkpoint" + str(check_index))
            #Sort the in-level regions
            map_regions = sorted(map_regions, key=attrgetter('base_id'))
            connect_region_pairs(map_regions)
            #Create the level info attached to it
            checkpoint_for_use : int | None 
            if level_int > 0 & level_int < 4:
                checkpoint_for_use = self.spawn_checkpoint[(world_index * 3) + level_int]
            region_level : RegionLevel = create_region_level(level_name, checkpoint_for_use, checkpoint_entry_pairs, map_regions, self)
            all_levels.append(region_level)
            #Attach the locations to the regions
            locations.extend(assign_locations_to_regions(region_level, map_regions, location_data_list, self.player, self.multiworld))
    return JsonInfo(all_levels, locations)

def build_location_pairings(base_name : str, ap_ids : list) -> list[list]:
    if len(ap_ids) == 1:
        #If the location data accounts for 1 location
        return [[base_name, ap_ids[0]]]
    output : list[list] = []
    #If the location accounts for multiple locations
    for each_ap_id_index, each_ap_id in enumerate(ap_ids):
        sublocation_name : str = base_name
        sublocation_name.removesuffix("s")
        sublocation_name + " " + str(each_ap_id_index + 1), each_ap_id
        output.append([sublocation_name, each_ap_id])
    #I don't know if garib groups are their own location, but if they are, uncomment this
    #output.append(list[base_name, ap_ids[0] + 10000])
    return output
    
def generate_location_name_to_id(world_prefixes, level_prefixes) -> dict:
    output : dict = {}
    #Each World
    for each_world_index, each_world in enumerate(logic_data):
        world_prefix : str = world_prefixes[each_world_index]
        for level_key, level_data in each_world.items():
            prefix : str = world_prefix + level_prefixes[int(level_key[-1])] + ": "
            for location_name in level_data:
                #Not regions
                if type(level_data[location_name]) is dict:
                    continue
                #Only locations remain
                ap_ids : list = level_data[location_name][0]["AP_IDS"]
                for each_pairing in build_location_pairings(prefix + location_name, ap_ids):
                    output[each_pairing[0]] = each_pairing[1]
    return output
