import json
import pkgutil
from BaseClasses import Entrance, Location, MultiWorld, Region
from typing import TYPE_CHECKING, Any, List, NamedTuple
from operator import attrgetter

from .Options import GaribLogic, DifficultyLogic
from .Rules import move_lookup, switches_to_event_items, access_methods_to_rules
from worlds.generic.Rules import add_rule, set_rule

if TYPE_CHECKING:
    from . import GloverWorld
else:
    GloverWorld = object


#Level name, followed by the region indexes of each checkpoint
levels_in_order = [
    ["AtlH", 0],
    ["Atl1", 0, 0],
    ["Atl2", 0, 4, 8],
    ["Atl3", 0, 3, 10],
    ["Atl!", 0],
    ["Atl?", 0],
    ["CrnH", 0],
    ["Crn1", 0, 2, 5, 9],
    ["Crn2", 0, 3, 6, 13, 15],
    ["Crn3", 0, 5, 9, 13],
    ["Crn!", 0],
    ["Crn?", 0],
    ["PrtH", 0],
    ["Prt1", 0, 11, 15],
    ["Prt2", 0, 3, 5],
    ["Prt3", 0, 5, 15, 19],
    ["Prt!", 0],
    ["Prt?", 0],
    ["PhtH", 0],
    ["Pht1", 0, 9, 12],
    ["Pht2", 0, 13, 18, 19],
    ["Pht3", 0, 5, 8, 11],
    ["Pht!", 0],
    ["Pht?", 0],
    ["FoFH", 0],
    ["FoF1", 0, 6, 13],
    ["FoF2", 0, 2, 7],
    ["FoF3", 0, 3, 4, 11, 17],
    ["FoF!", 0],
    ["FoF?", 0],
    ["OoWH", 0],
    ["OoW1", 0, 9],
    ["OoW2", 0],
    ["OoW3", 0, 2, 12, 17],
    ["OoW!", 0],
    ["OoW?", 0],
    ["Hubworld", 0],
    ["Castle Cave", 0],
    ["Training", 0]
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
    required_items : list[str]

location_type_lookup = ["SWITCH", "GARIB", "LIFE", "CHECKPOINT", "POTION", "GOAL", "TIP", "LOADING_ZONE", "REGION", "MISC", "ENEMY", "INSECT"]

class LocationData(NamedTuple):
    name : str
    #The same index as in location type lookup
    type : int
    default_region : int
    default_needs_ball : bool
    ap_ids : List[int]
    rom_ids : List[int]
    methods : List[AccessMethod]

def remove_higher_difficulty_methods(self : GloverWorld, check_methods : list[AccessMethod]) -> list[AccessMethod]:
    out_methods : list[AccessMethod] = []
    #Find something of the correct difficulty based on logic methods
    difficulty_cutoff : int = 3
    match self.options.difficulty_logic:
        case DifficultyLogic.option_intended:
            difficulty_cutoff = 0
        case DifficultyLogic.option_easy_tricks:
            difficulty_cutoff = 1
        case DifficultyLogic.option_hard_tricks:
            difficulty_cutoff = 2
    for each_method in check_methods:
        #Difficulty Logic
        if each_method.difficulty <= difficulty_cutoff:
            out_methods.append(each_method)
    return out_methods


def create_location_data(self : GloverWorld, check_name : str, check_info : list, level_name : str) -> list[LocationData]:
    prefix = level_name + ": "
    outputs : List[LocationData] = []
    methods : List[AccessMethod] = []
    for check_index in range(1, len(check_info)):
        check_method = check_info[check_index]
        new_method = create_access_method(self, check_method, level_name)
        if new_method != None:
            methods.append(new_method)
    #Only create if there's a method for it
    methods = remove_higher_difficulty_methods(self, methods)
    if len(methods) == 0:
        return outputs
    ap_ids : list[int] = []
    rom_ids : list[int] = []
    for each_id in non_blank_ap_ids(check_info[0]["AP_IDS"]):
        ap_ids.append(int(each_id, 0))
    for each_id in non_blank_ap_ids(check_info[0]["IDS"]):
        if each_id == "" or each_id == "N/A" or each_id == "?":
            continue
        if each_id.isdigit():
            rom_ids.append(int(each_id, 0))
        else:
            rom_ids.append(-1)
    
    #Is it an enemy?
    enemy_with_garibs : bool = check_info[0]["TYPE"] == 10
    if enemy_with_garibs:
        #If so, are there garibs with this enemy?
        enemy_with_garibs = len(ap_ids) > check_info[0]["COUNT"]

    #When you have enemies with garibs
    if enemy_with_garibs:
        #Enemies get the first half of the array, garibs create the second
        garib_ap_ids = []
        garib_rom_ids = []
        for _ in range(check_info[0]["COUNT"]):
            garib_ap_ids.append(ap_ids.pop())
            garib_rom_ids.append(rom_ids.pop())
        garib_ap_ids.reverse()
        garib_rom_ids.reverse()
        outputs.append(LocationData(prefix + check_name.removesuffix("s") + " Garibs", 1, check_info[0]["REGION"], check_info[0]["NEEDS_BALL"], garib_ap_ids, garib_rom_ids, methods))
        outputs.append(LocationData(prefix + check_name, 10, check_info[0]["REGION"], check_info[0]["NEEDS_BALL"], ap_ids, rom_ids, methods))
    #All other checks
    else:
        outputs.append(LocationData(prefix + check_name, check_info[0]["TYPE"], check_info[0]["REGION"], check_info[0]["NEEDS_BALL"], ap_ids, rom_ids, methods))
    return outputs

class RegionPair(NamedTuple):
    name : str
    base_id : int
    ball_region_methods : list[AccessMethod]
    no_ball_region_methods : list[AccessMethod]
    ball_region_exists : bool
    no_ball_region_exists : bool

def create_region_pair(self : GloverWorld, check_info : dict, check_name : str, level_name : str) -> RegionPair:
    prefix = level_name + ": "
    player : int = self.player
    multiworld : MultiWorld = self.multiworld
    region_name = prefix + check_name
    ball_region_methods : list[AccessMethod] = []
    no_ball_region_methods : list[AccessMethod] = []
    base_id : int = check_info["I"]
    ball_region = Region(region_name + " W/Ball", player, multiworld, level_name)
    for index, check_pairing in enumerate(check_info["B"]):
        #Skip the settings entry
        if index == 0:
            continue
        #All other entries are methods
        new_method = create_access_method(self, check_pairing, level_name)
        if new_method != None:
            ball_region_methods.append(new_method)
    
    no_ball_region = Region(region_name, player, multiworld, level_name)
    for index, check_pairing in enumerate(check_info["D"]):
        #Skip the settings entry
        if index == 0:
            continue
        new_method = create_access_method(self, check_pairing, level_name)
        if new_method != None:
            no_ball_region_methods.append(new_method)
    
    #Ball regions that work
    ball_region_exists : bool = False
    ball_region_methods = remove_higher_difficulty_methods(self, ball_region_methods)
    if len(ball_region_methods) > 0:
        multiworld.regions.append(ball_region)
        ball_region_exists = True
        ball_region_methods = list(filter(lambda a, b = base_id, c = True: self_ref_region(a, b, c), ball_region_methods))

    #No ball regions that exist
    no_ball_region_exists : bool = False
    no_ball_region_methods = remove_higher_difficulty_methods(self, no_ball_region_methods)
    if len(no_ball_region_methods) > 0:
        multiworld.regions.append(no_ball_region)
        no_ball_region_exists = True
        no_ball_region_methods = list(filter(lambda a, b = base_id, c = True: self_ref_region(a, b, c), no_ball_region_methods))

    return RegionPair(region_name, base_id, ball_region_methods, no_ball_region_methods, ball_region_exists, no_ball_region_exists)

def self_ref_region(check_method : AccessMethod, base_region : int, base_ball : bool) -> bool:
    return len(check_method.required_items) > 0 or check_method.region_index != base_region or check_method.ball_in_region != base_ball

def connect_region_pairs(self : GloverWorld, pairs : List[RegionPair]):
    multiworld : MultiWorld = self.multiworld
    player : int = self.player
    for each_pair in pairs:
        #If there's a ball region
        if each_pair.ball_region_exists:
            #Construct it
            ball_region = multiworld.get_region(each_pair.name + " W/Ball", player)
            #Gather methods
            pair_ball_connections : dict[Region, list[AccessMethod]] = {}
            for each_method in each_pair.ball_region_methods:
                region_to_connect : Region = get_region_from_method(multiworld, player, pairs, each_method)
                if region_to_connect == None:
                    continue
                if not region_to_connect in pair_ball_connections.keys():
                    pair_ball_connections[region_to_connect] = [each_method]
            #Create the rules using methods
            for each_connection, methods in pair_ball_connections.items():
                entrance : Entrance | Any = each_connection.connect(ball_region)
                access_methods_to_rules(self, methods, entrance)
        #If there's a no ball region
        if each_pair.no_ball_region_exists:
            #Construct it
            pair_no_ball_connections : dict[Region, list[AccessMethod]] = {}
            for each_method in each_pair.no_ball_region_methods:
                region_to_connect : Region = get_region_from_method(multiworld, player, pairs, each_method)
                if region_to_connect == None:
                    continue
                if not region_to_connect in pair_no_ball_connections.keys():
                    pair_no_ball_connections[region_to_connect] = [each_method]
            no_ball_region = multiworld.get_region(each_pair.name, player)
            #Create the rules using methods
            for each_connection, methods in pair_no_ball_connections.items():
                entrance : Entrance | Any = each_connection.connect(no_ball_region)
                access_methods_to_rules(self, methods, entrance)
        
        #Ball region always leads to no ball region
        if each_pair.ball_region_exists and each_pair.no_ball_region_exists:
            ball_region.connect(no_ball_region)

class RegionLevel(NamedTuple):
    name : str
    #region : Region | None
    starting_checkpoint : int
    map_regions : List[RegionPair]
    start_without_ball : bool

def create_region_level(self : GloverWorld, level_name : str, checkpoint_for_use : int | None, checkpoint_entry_pairs : list, map_regions : List[RegionPair]):
    #By default, the region level leads to the first checkpoint's region
    multiworld : MultiWorld = self.multiworld
    player : int = self.player

    default_checkpoint : int = 1
    region : Region = Region(level_name, player, multiworld)

    #Get the checkpoint from the core levels
    if type(checkpoint_for_use) is int:
        default_checkpoint = checkpoint_for_use

    #See if you get the ball with the checkpoint
    start_without_ball : bool = level_name[3:4] == "1" or level_name[:3] == "OoW"

    #If you can get the ball in the level, you can use it to checkpoint warp with it to a later spot.
    ball_regions : list[Region] = []
    if start_without_ball:
        ball_access_location = region.add_event(level_name + ": Ball", level_name + " Ball").location
        for region_index, each_region_pair in enumerate(map_regions):
            if each_region_pair.ball_region_exists:
                ball_region = multiworld.get_region(each_region_pair.name + " W/Ball", player)
                ball_regions.append(ball_region)
                if region_index == 0:
                    set_rule(ball_access_location, lambda state, in_player = player, ball_reg = ball_region.name : state.can_reach_region(ball_reg, in_player))
                else:
                    add_rule(ball_access_location, lambda state, in_player = player, ball_reg = ball_region.name : state.can_reach_region(ball_reg, in_player), "or")

    #Assign entrances required by checkpoints here
    for checkpoint_number in range(1, len(checkpoint_entry_pairs)):
        #Create a checkpoint connection
        checkpoint_name : str = level_name + " Checkpoint " + str(checkpoint_number)
        for each_region_pair in map_regions:
            #If the checkpoint leads to that region
            if each_region_pair.base_id == checkpoint_entry_pairs[checkpoint_number]:
                is_default = default_checkpoint == checkpoint_number

                #If you normally spawn without the ball, the logic goes here
                if start_without_ball:
                    if each_region_pair.no_ball_region_exists:
                        connecting_region : Region = multiworld.get_region(each_region_pair.name, player)
                        checkpoint_bridge(self, region, connecting_region, checkpoint_name, is_default)
                
                #You can theoretically always spawn with the ball, if you can reach it
                if each_region_pair.ball_region_exists:
                    connecting_region : Region = multiworld.get_region(each_region_pair.name + " W/Ball", player)
                    checkpoint_bridge(self, region, connecting_region, checkpoint_name, is_default, start_without_ball, ball_regions)
        
    multiworld.regions.append(region)
    return RegionLevel(level_name, default_checkpoint, map_regions, start_without_ball)

def checkpoint_bridge(self : GloverWorld, region : Region, connecting_region : Region, checkpoint_name : str, is_default : bool, requires_ball_access = False, ball_regions : list[Region] = []):
    name_suffix : str = ""
    if requires_ball_access:
        name_suffix += " W/Ball"
    entrance : Entrance | Any = region.connect(connecting_region, checkpoint_name + name_suffix)
    requirements : list[str] = []
    #The default checkpoint's always useable
    if not is_default:
        requirements.append(checkpoint_name)
    if requires_ball_access:
        ball_access = checkpoint_name.split(" ")[0]+ " Ball"
        requirements.append(ball_access)
        #Notify that getting the ball can let you use the checkpoint for the region sweeper
        for each_ball_region in ball_regions:
            self.multiworld.register_indirect_condition(each_ball_region, entrance)
    if len(requirements) > 0:
        #Other ones need the checkpoint item
        set_rule(entrance, lambda state, reqs = requirements, in_player = self.player : state.has_all(reqs, in_player))

def create_access_method(self, info : dict, level_name : str) -> AccessMethod:#
    required_moves : list = []
    for each_key, each_result in info.items():
        if each_key.startswith("mv"):
            each_move = move_lookup[each_result]
            required_moves.append(each_move)
        if each_key.startswith("ck"):
            required_moves.append(level_name + " " + each_result)
    #Remove Power Ball methods
    if "Power Ball" in required_moves and (not self.options.include_power_ball and self.starting_ball != "Power Ball"):
        return None
    #Combine Not Bowling and Not Crystal into Not Bowling Or Crystal
    if "Not Bowling" in required_moves and "Not Crystal" in required_moves:
        required_moves.remove("Not Bowling")
        required_moves.remove("Not Crystal")
        required_moves.append("Not Bowling or Crystal")
    #Make sure there's a jump required for double jumps
    if not "Jump" in required_moves and ("Double Jump" in required_moves):
        required_moves.append("Jump")
    #Here's the access method!
    return AccessMethod(info["regionIndex"], info["ballRequirement"], info["trickDifficulty"], required_moves)

def assign_locations_to_regions(self : GloverWorld, region_level : RegionLevel, map_regions : List[RegionPair], location_data_list : List[LocationData], target_score : int):
    player : int = self.player
    multiworld : MultiWorld = self.multiworld
    score_locations : list[Location] = []
    for each_location_data in location_data_list:
        #Should this location be generated?
        ap_ids : list[int] = each_location_data.ap_ids
        match each_location_data.type:
            case 0:
                #Switches
                if not self.options.switches_checks:
                    ap_ids.clear()
            case 3:
                #Checkpoints don't give their starting location
                if region_level.starting_checkpoint == int(each_location_data.name[-1]):
                    continue
                #As Events
                if not self.options.checkpoint_checks:
                    ap_ids.clear()
            case 6:
                #Tip hints
                if self.options.mr_hints:
                    self.tip_locations[each_location_data.name] = ap_ids[0]
                #Tips
                if not self.options.mr_tip_checks:
                    continue
            case 7:
                #Loading Zones
                if not self.options.bonus_levels:
                    #Bonus loading zones
                    if each_location_data.name.endswith("Entry Bonus"):
                        continue
            #case 9:
                #Misc
            case 10:
                #Enemysanity
                if not self.options.enemysanity:
                    ap_ids.clear()
            case 11:
                #Insectity
                if not self.options.insectity:
                    ap_ids.clear()
                
        rules_applied : bool = False

        #Is this a mono location?
        location_regions : dict[str, list[AccessMethod]] = {}
        for each_method in each_location_data.methods:
            region_index = each_method.region_index
            region_exists : bool = False
            region_name : str
            for each_pair in map_regions:
                #If you're in the right region
                if region_index == each_pair.base_id:
                    #That's a valid region name
                    region_name = each_pair.name
                    if each_method.ball_in_region:
                        region_name = region_name + " W/Ball"
                        region_exists = each_pair.ball_region_exists
                    else:
                        region_exists = each_pair.no_ball_region_exists
            #If the region exists, assign it to the location regions
            if region_exists:
                if not region_name in location_regions:
                    location_regions[region_name] = []
                location_regions[region_name].append(each_method)
        #Depending on if it is or not
        region_for_use : Region
        if len(location_regions) > 1:
            #Multi location construction creates a shared region to reach this location
            region_for_use = Region(each_location_data.name + " Region", player, multiworld, region_level.name)
            #Apply the rules here
            rules_applied = True
            for each_region_name, each_region_methods in location_regions.items():
                #Only use the methods relevant to this entrance from the target region
                entrance : Entrance | Any = multiworld.get_region(each_region_name, player).connect(region_for_use, each_location_data.name + " from " + each_region_name)
                access_methods_to_rules(self, each_region_methods, entrance)
        elif len(location_regions) == 1:
            #Single location construction assigns to the specific element in the RegionPair
            region_for_use = multiworld.get_region(list(location_regions.keys())[0], player)
        else:
            #If there are no methods, continue
            continue
        
        #Construct location data
        if each_location_data.type == 1:
            #Garibsanity
            if self.options.garib_logic == GaribLogic.option_garibsanity:
                for each_garib_index in range(len(each_location_data.ap_ids)):
                    each_garib = each_location_data.ap_ids[each_garib_index]
                    location_name : str = each_location_data.name.removesuffix("s")
                    location_name += " " + str(each_garib_index + 1)
                    location : Location = Location(player, location_name, each_garib, region_for_use)
                    region_for_use.locations.append(location)
                    if not rules_applied:
                        access_methods_to_rules(self, each_location_data.methods, location)
                    #Garibs give score
                    score_locations.append(location)
            #Garib Groups
            elif self.options.garib_logic == GaribLogic.option_garib_groups:
                #Regular Locations
                group_offset : int = each_location_data.ap_ids[0]
                if len(ap_ids) > 1:
                    group_offset += 10000
                location : Location = Location(player, each_location_data.name, group_offset, region_for_use)
                region_for_use.locations.append(location)
                if not rules_applied:
                    access_methods_to_rules(self, each_location_data.methods, location)
                #Garibs give score
                score_locations.append(location)
            #All Garibs in Level
            else:
                #It's an event location, with an event item
                location : Location = Location(player, each_location_data.name, None, region_for_use)
                region_for_use.locations.append(location)
                if not rules_applied:
                    access_methods_to_rules(self, each_location_data.methods, location)
                #These are used to create star gate unlock logic
                location.place_locked_item(self.create_event(each_location_data.name + " Reached"))
                score_locations.append(location)
        else:
            #Regular Locations
            address : int | None = None
            #Single AP Item
            if len(each_location_data.ap_ids) == 1:
                address = each_location_data.ap_ids[0]
                location : Location = Location(player, each_location_data.name, address, region_for_use)
                region_for_use.locations.append(location)
                if not rules_applied:
                        access_methods_to_rules(self, each_location_data.methods, location)
                #Lives, Potions and Enemies give Score
                if each_location_data.type in [2, 4, 10]:
                    score_locations.append(location)
                    score_locations.append(location)
            #Multiple AP Items
            elif len(each_location_data.ap_ids) > 1:
                for each_index in range(len(each_location_data.ap_ids)):
                    each_ap_id = each_location_data.ap_ids[each_index]
                    location_name : str = each_location_data.name.removesuffix("s")
                    location_name += " " + str(each_index + 1)
                    location : Location = Location(player, location_name, each_ap_id, region_for_use)
                    region_for_use.locations.append(location)
                    if not rules_applied:
                        access_methods_to_rules(self, each_location_data.methods, location)
                    #Lives, Potions and Enemies give Score
                    if each_location_data.type in [2, 4, 10]:
                        score_locations.append(location)
                        score_locations.append(location)
            else:
                #Event Item
                location : Location = Location(player, each_location_data.name, address, region_for_use)
                region_for_use.locations.append(location)
                if not rules_applied:
                    access_methods_to_rules(self, each_location_data.methods, location)
                match each_location_data.type:
                    #Switches with no paired level event store their level event 
                    #items as event items rather than AP items.
                    case 0:
                        new_event_item : str = switches_to_event_items[each_location_data.name]
                        location.place_locked_item(self.create_event(new_event_item))
                    #Enemies contribute to score even if disabled
                    case 10:
                        new_event_item : str = each_location_data.name.replace(":", "")
                        location.place_locked_item(self.create_event(new_event_item))
                        score_locations.append(location)
                    #Checkpoints & Level Warps
                    case _:
                        new_event_item : str = each_location_data.name.replace(":", "")
                        location.place_locked_item(self.create_event(new_event_item))
    
    #Create score addresses anywhere that score is something you can get
    #(AKA any non-boss level, excluding Space Boss)
    world_index = 1 + self.world_from_string(region_level.name)
    level_index = self.level_from_string(region_level.name)
    if (world_index == 6 or level_index != 4) and level_index != 0:
        #Score location at root
        score_address = None
        if target_score != 0:
            score_address = ((world_index * 10) + level_index) * 100000
        level_root = self.get_region(region_level.name)
        score_location = Location(player, region_level.name + ": Score", score_address, level_root)
        if score_address == None:
            score_location.place_locked_item(self.create_event(region_level.name + " Score"))
        level_root.locations.append(score_location)
        for each_index, each_location in enumerate(score_locations):
            if each_index == 0:
                set_rule(score_location, lambda state, plr = player, scl = each_location: state.can_reach(scl, plr))
            else:
                add_rule(score_location, lambda state, plr = player, scl = each_location: state.can_reach(scl, plr), "or")

def get_region_from_method(multiworld : MultiWorld, player : int, region_pairs : List[RegionPair], method : AccessMethod) -> Region:
    for each_pair in region_pairs:
        lookup_name = each_pair.name
        if method.ball_in_region:
            lookup_name += " W/Ball"
        if each_pair.base_id == method.region_index:
            if method.ball_in_region:
                if not each_pair.ball_region_exists:
                    return None
            elif not each_pair.no_ball_region_exists:
                return None
            return multiworld.get_region(lookup_name, player)
    raise IndexError(region_pairs[0].name.split(':')[0] + " method calls for region indexed " + str(method.region_index) + " that does not exist!")

def build_data(self : GloverWorld) -> List[RegionLevel]:
    all_levels : List[RegionLevel] = []

    #Build Logic
    loc_con_index = 0
    for world_index, each_world in enumerate(logic_data):
        world_prefix : str = create_world_prefix(self.world_prefixes, world_index)
        #Go over the Glover worlds
        for level_index, level_key in enumerate(each_world):
            if level_index == 5 and not self.options.bonus_levels:
                loc_con_index += 1
                continue
            each_level = each_world[level_key]
            checkpoint_entry_pairs : list = levels_in_order[loc_con_index]
            loc_con_index += 1
            level_prefix = create_level_prefix(self.level_prefixes, world_index, level_index)
            level_name : str = world_prefix + level_prefix
            prefix : str = level_name + ": "
            map_regions : List[RegionPair] = []
            location_data_list : List[LocationData] = []
            
            #Bonus levels
            if not (level_index == 5 and not self.options.bonus_levels):
                for check_name in each_level:
                    check_info = each_level[check_name]
                    #Location
                    if type(check_info) is list:
                        location_data_list.extend(create_location_data(self, check_name, check_info, level_name))
                    #In-Level Region
                    if type(check_info) is dict:
                        new_region_pair = create_region_pair(self, check_info, check_name, level_name)
                        map_regions.append(new_region_pair)
            
            #Sort the in-level regions
            map_regions = sorted(map_regions, key=attrgetter('base_id'))
            connect_region_pairs(self, map_regions)
            
            #Create the level info attached to it
            checkpoint_for_use : int | None = None
            if level_index > 0 and level_index < 4 and world_index < 6:
                checkpoint_for_use = self.spawn_checkpoint[(world_index * 3) + (level_index - 1)]
            region_level : RegionLevel = create_region_level(self, level_name, checkpoint_for_use, checkpoint_entry_pairs, map_regions)
            
            #Target Score
            target_score = 0
            if level_name in self.options.level_scores.value:
                target_score = self.options.level_scores.value[level_name]

            #Attach the locations to the regions
            assign_locations_to_regions(self, region_level, map_regions, location_data_list, target_score)
            
            #Aside from the wayrooms, the hubworld and the castle cave, levels have star marks
            if (world_index < 6 and not level_index == 0) or level_index == 2:
                create_star_mark(self, level_index, world_index, prefix, location_data_list)
            
            #Append it to the level list
            all_levels.append(region_level)

    return all_levels

def create_star_mark(self, level_index : int, world_index : int, prefix : str, location_data_list : List[LocationData]):
    player : int = self.player
    
    #Does this location have a star mark item, or a random one?
    star_mark_ap_id : int | None = None
    if self.options.portalsanity:
        #They contain a random item
        star_mark_ap_id = 30000 + level_index + (world_index * 10)
    secondary_condition : str
    #Does it unlock via garibs?
    level_has_garibs : bool = level_index != 4 and world_index < 6
    if level_has_garibs:
        #Yes
        secondary_condition = "All Garibs"
    else:
        #No
        secondary_condition = "Completion"
        #Which means, don't give them a second item here
        star_mark_ap_id = None
    #Otherwise, they contain the star marks
    menu_region : Region = self.multiworld.get_region("Menu", player)
    star_mark_location = Location(player, prefix + secondary_condition, star_mark_ap_id, menu_region)
    #Boss levels and the well just give you it if you reach the goal
    if not level_has_garibs:
        goal_location : Location
        #Boss levels look for the location 'Boss'
        if level_index == 4:
            goal_location = self.multiworld.get_location(prefix + "Boss", player)
        else:
        #The tutorial well looks for the locaiton 'Goal'
            goal_location = self.multiworld.get_location(prefix + "Goal", player)
        set_rule(star_mark_location, lambda state, for_completion = goal_location: state.can_reach(for_completion, player))
    #Level garibs means you take all garib methods from before
    elif self.options.garib_logic == GaribLogic.option_level_garibs:
        all_garibs_rule(self, star_mark_location, location_data_list)
    menu_region.locations.append(star_mark_location)

def all_garibs_rule(self, star_mark_location : Location, location_data_list : List[LocationData]):
    #If it's all garibs in level logic, logic construction looks diffrent
    garib_location_names : List[str] = []
    for each_garib_location in location_data_list:
        #Skip non-garibs obviously
        if not each_garib_location.type == 1:
            continue
        garib_location_names.append(each_garib_location.name + " Reached")
    set_rule(star_mark_location, lambda state, required_garibs = garib_location_names: state.has_all(required_garibs, self.player))


def build_location_pairings(base_name : str, check_info : dict, ap_ids : list[str]) -> list[list]:
    #Nothing at all
    if len(ap_ids) == 0:
        return []
    #If the location data accounts for 1 location
    if len(ap_ids) == 1:
        return [[base_name, ap_ids[0]]]
    #A single enemy
    if len(ap_ids) == 2 and check_info["TYPE"] == 10:
        if check_info["COUNT"] == 1:
            return [[base_name, ap_ids[0]], [base_name + " Garib", ap_ids[1]]]
    output : list[list] = []
    #If the location accounts for multiple locations
    for each_ap_id_index, each_ap_id in enumerate(ap_ids):
        sublocation_name : str = base_name.removesuffix("s")
        #Not enemies
        if check_info["TYPE"] != 10:
            sublocation_name += " " + str(each_ap_id_index + 1)
        else:
            #Enemies
            if each_ap_id_index < check_info["COUNT"]:
                sublocation_name += " " + str(each_ap_id_index + 1)
            else:
                sublocation_name += " Garib " + str(each_ap_id_index + 1 - check_info["COUNT"])
        output.append([sublocation_name, each_ap_id])
    return output

def non_blank_ap_ids(ap_ids : list[str]) -> list[str]:
    return list(filter(lambda a: a != "", ap_ids))

def create_world_prefix(world_prefixes : list[str], index : int) -> str:
    if index < 6:
        return world_prefixes[index]
    else:
        return ""

def create_level_prefix(level_prefixes : list[str], world_index : int, level_index : int) -> str:
    if world_index == 6:
        match level_index:
            case 0:
                return "Hubworld"
            case 1:
                return "Castle Cave"
            case 2:
                return "Training"
    else:
        return level_prefixes[level_index]

def generate_location_information(world_prefixes : list[str], level_prefixes : list[str]) -> list:
    location_name_to_id : dict = {}
    #Setup the location types here
    location_name_groups : dict = {}
    for each_type in location_type_lookup:
        if each_type == "LOADING_ZONE" or each_type == "REGION":
            continue
        group_name = each_type.title()
        location_name_groups[group_name] = []
    location_name_groups["Score"] = []
    location_name_groups["Crystals"] = []
    #Each World
    for each_world_index, each_world in enumerate(logic_data):
        world_prefix : str = create_world_prefix(world_prefixes, each_world_index)
        for level_key, level_data in each_world.items():
            level_prefix : str = create_level_prefix(level_prefixes, each_world_index, int(level_key[-1]))
            level_name = world_prefix + level_prefix
            prefix : str = level_name + ": "
            location_name_groups[level_name] = []
            for location_name in level_data:
                #Not regions
                if type(level_data[location_name]) is dict:
                    continue
                #Only locations remain
                ap_ids : list[str] = level_data[location_name][0]["AP_IDS"]
                ap_ids = non_blank_ap_ids(ap_ids)
                for each_pairing in build_location_pairings(prefix + location_name, level_data[location_name][0], ap_ids):
                    #Name to ID
                    location_name_to_id[each_pairing[0]] = int(each_pairing[1], 0)
                    #Name Groups
                    location_name_groups[level_name].append(each_pairing[0])
                    location_type : str = location_type_lookup[level_data[location_name][0]["TYPE"]]
                    location_name_groups[location_type.title()].append(each_pairing[0])
                #Garib Groups
                if level_data[location_name][0]["TYPE"] == 1 and len(ap_ids) > 1:
                    group_id : int = int(ap_ids[0], 0) + 10000
                    location_name_to_id[prefix + location_name] = group_id
                #Enemy Garib Groups
                if level_data[location_name][0]["TYPE"] == 10:
                    enemy_count = level_data[location_name][0]["COUNT"]
                    if enemy_count < len(ap_ids):
                        group_id : int = int(ap_ids[enemy_count], 0) + 10000
                        location_name_to_id[prefix + location_name.removesuffix("s") + " Garibs"] = group_id
            #Levels with garibs in them
            if each_world_index < 6:
                match level_key:
                    case "l1":
                        location_name_to_id[prefix + "All Garibs"] = 30000 + (each_world_index * 10) + 1
                    case "l2":
                        location_name_to_id[prefix + "All Garibs"] = 30000 + (each_world_index * 10) + 2
                    case "l3":
                        location_name_to_id[prefix + "All Garibs"] = 30000 + (each_world_index * 10) + 3
                    case "l5":
                        location_name_to_id[prefix + "All Garibs"] = 30000 + (each_world_index * 10) + 5
    #Scores
    for world_index, world_prefix in enumerate(world_prefixes, 1):
        for level_index, level_prefix in enumerate(level_prefixes):
            level_score_address = 100000 * ((world_index * 10) + level_index)
            if (level_index != 4 or world_index == 6) and level_index != 0:
                level_name = world_prefix + level_prefix
                prefix = level_name + ": "
                location_name_to_id[prefix + "Score"] = level_score_address
                location_name_groups["Score"].append(prefix + "Score")
                location_name_groups[level_name].append(prefix + "Score")
    for each_score in range(10000, 100000000, 10000):
        location_name_to_id[str(each_score) + " Score"] = 100000000 + each_score
        location_name_groups["Score"].append(str(each_score) + " Score")
    
    for each_crystal in range(1,8):
        turn_in_name = "Crystal Cave: Ball Turn-In " + str(each_crystal)
        location_name_groups["Crystals"].append(turn_in_name)
    return [location_name_to_id, location_name_groups]