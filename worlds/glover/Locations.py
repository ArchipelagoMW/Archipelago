import json
from BaseClasses import Location
import typing

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
#    ["Atl Hub", ],
    ["Atl 1", "Floor", "Floor"]
#    ["Atl 2", ],
#    ["Atl 3", ],
#    ["Atl Boss", ],
#    ["Atl Bonus", ],
#    ["Crn Hub", ],
#    ["Crn 1", ],
#    ["Crn 2", ],
#    ["Crn 3", ],
#    ["Crn Boss", ],
#    ["Crn Bonus", ],
#    ["Prt Hub", ],
#    ["Prt 1", ],
#    ["Prt 2", ],
#    ["Prt 3", ],
#    ["Prt Boss", ],
#    ["Prt Bonus", ],
#    ["Pht Hub", ],
#    ["Pht 1", ],
#    ["Pht 2", ],
#    ["Pht 3", ],
#    ["Pht Boss", ],
#    ["Pht Bonus", ],
#    ["FoF Hub", ],
#    ["FoF 1", ],
#    ["FoF 2", ],
#    ["FoF 3", ],
#    ["FoF Boss", ],
#    ["FoF Bonus", ],
#    ["OoW Hub", ],
#    ["OoW 1", ],
#    ["OoW 2", ],
#    ["OoW 3", ],
#    ["OoW Boss", ],
#    ["OoW Bonus", ],
#    ["Hubworld", "Main"],
#    ["Castle Cave", "Main"],
#    ["Training", "Start"]
]

class GloverLocation(Location):
    game : str = "Glover"

class LocationData(typing.NamedTuple):
    id : int = 0
    group : str = ""

class AccessMethod(typing.NamedTuple):
    region_name : str
    ball_in_region : bool
    difficulty : int
    required_items : list

def build_logic():
    #Build Logic
    logic_file = open('Logic.json')
    logic_data = json.load(logic_file)
    loc_con_index = 0
    for world_index in 1:
        world_prefix : str = GloverWorld.world_prefixes[world_index]
        each_world = logic_data[world_index]
        #Go over the Glover worlds
        for level_key in each_world:
            each_level = each_world[level_key]
            checkpoint_entry_pairs = levels_in_order[loc_con_index]
            loc_con_index += 1
            level_prefix = GloverWorld.level_prefixes[int(level_key[-1])]
            prefix : str = world_prefix + level_prefix + ": "
            #Get the check name
            for check_name in each_level:
                check_info = each_level[check_name]
                #Location
                if check_info is list:
                    for check_pairing in check_info:
                        ids = check_pairing[0]
                        methods = []
                        if check_pairing.count() > 1:
                            for each_method in check_pairing[1]:
                                methods.append(create_access_method(each_method, prefix))
                #In-Level Region
                if check_info is dict:
                    region_name = prefix + check_name
                    region_checkpoints = []
                    for check_pairing in check_info["B"]:
                        ids = check_pairing[0]
                        methods = []
                        if check_pairing.count() > 1:
                            for each_method in check_pairing[1]:
                                methods.append(create_access_method(each_method, prefix))
                    for check_pairing in check_info["D"]:
                        ids = check_pairing[0]
                        methods = []
                        if check_pairing.count() > 1:
                            for each_method in check_pairing[1]:
                                methods.append(create_access_method(each_method, prefix))
                    #You get the one from checkpoints by default
                    for check_index in range(1, checkpoint_entry_pairs.count()):
                        matching_name = checkpoint_entry_pairs[check_index]
                        if matching_name == check_name:
                            region_checkpoints.append(prefix + "Checkpoint" + str(check_index))

def create_access_method(info : dict, prefix : str) -> AccessMethod:
    required_moves : list = []
    for each_key in info:
        if each_key.startswith("mv"):
            required_moves.append(move_name[info[each_key]])
        if each_key.startswith("ck"):
            required_moves.append(prefix + info[each_key])
    info["regionIndex"]
    return AccessMethod(info["regionIndex"], info["ballRequirement"], info["trickDifficulty"], required_moves)