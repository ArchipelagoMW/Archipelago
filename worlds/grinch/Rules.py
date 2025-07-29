from worlds.AutoWorld import World
# from .Options import GrinchOptions
from worlds.generic.Rules import add_rule
import logging
logger = logging.getLogger()

def set_rules(world: World):
    all_locations = world.get_locations()
    for location in all_locations:
        loc_rules = rules_dict[location.name]
        rule = interpret_rule(loc_rules, world.player)
        add_rule(location, rule)


rules_dict: dict[str,list[list[str]]] = {
    "Enter Whoville": [
        []
    ],
    "Enter the Post Office": [
        []
    ],
    "Enter the Town Hall": [
        []
    ],
    "Enter the Countdown-To-Xmas Clock Tower": [
        []
    ],
    "Enter Who Forest": [
        []
    ],
    "Enter the Ski Resort": [
        []
    ],
    "Enter the Civic Center": [
        []
    ],
    "Enter Who Dump": [
        []
    ],
    "Enter the Minefield": [
        []
    ],
    "Enter the Power Plant": [
        []
    ],
    "Enter the Generator Building": [
        []
    ],
    "Enter Who Lake": [
        []
    ],
    "Enter the Submarine World": [
        []
    ],
    "Enter the Scout's Hut": [
        []
    ],
    "Enter the North Shore": [
        []
    ],
    "Enter the Mayor's Villa": [
        []
    ],
    "Smashing Snowmen": [
        []
    ],
    "Shuffling The Mail": [
        []
    ],
    "Painting The Mayor's Posters": [
        ["Painting Bucket"]
    ],
    "Launching Eggs Into Houses": [
        ["Rotten Egg Launcher"]
    ],
    "Modifying The Mayor's Statue": [
        ["Sculpting Tools"]
    ],
    "Advancing The Countdown-To-Xmas Clock": [
        ["Hammer", "Rocket Spring"]
    ],
    "Making Xmas Trees Droop": [
        ["Rotten Egg Launcher"]
    ],
    "Sabotaging Snow Cannon With Glue": [
        ["Glue Bucket", "Rocket Spring"],
        ["Glue Bucket", "Grinch Copter"]
    ],
    "Putting Beehives In Cabins": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "Sliming The Mayor's Skis": [
        ["Slime Shooter", "Rotten Egg Launcher"]
    ],
    "Replacing The Candles On The Cake With Fireworks": [
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Rotten Egg Launcher", "Octopus Climbing Device", "Rocket Spring"]
    ],
    "Stealing Food From Birds": [
        ["Rocket Spring", "Rotten Egg Launcher"]
    ],
    "Feeding The Computer With Robot Parts": [
        ["Rocket Spring", "Rotten Egg Launcher"]
    ],
    "Infesting The Mayor's House With Rats": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "Conducting The Stinky Gas To Who-Bris' Shack": [
        ["Rocket Spring", "Rotten Egg Launcher"]
    ],
    "Shaving Who Dump Guardian": [
        ["Scissors", "Grinch Copter"],
        ["Scissors", "Slime Shooter", "Rotten Egg Launcher", "Rocket Spring"]
    ],
    "Short-Circuiting Power-Plant": [
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Rotten Egg Launcher", "Octopus Climbing Device", "Slime Shooter", "Rocket Spring"]
    ],
    "Putting Thistles In Shorts": [
        ["Rotten Egg Launcher", "Octopus Climbing Device"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "Sabotaging The Tents": [
        ["Octopus Climbing Device", "Rocket Spring"],
        ["Grinch Copter"]
    ],
    "Drilling Holes In Canoes": [
        ["Drill"]
    ],
    "Modifying The Marine Mobile": [
        []
    ],
    "Hooking The Mayor's Bed To The Motorboat": [
        ["Rope", "Hook", "Rotten Egg Launcher", "Scout Clothes"]
    ],
    "Binoculars Blueprint - Post Office Roof": [
        []
    ],
    "Binoculars Blueprint - City Hall Library - Left Side": [
        []
    ],
    "Binoculars Blueprint - City Hall Library - Front Side": [
        []
    ],
    "Binoculars Blueprint - City Hall Library - Right Side": [
        []
    ],
    "Rotten Egg Launcher Blueprint - Outside City Hall": [
        []
    ],
    "Rotten Egg Launcher Blueprint - Outside Clock Tower": [
        []
    ],
    "Rotten Egg Launcher Blueprint - Post Office - Front of Silver Door": [
        ["Who Cloak"]
    ],
    "Rotten Egg Launcher Blueprint - Post Office - After Mission Completion": [
        ["Who Cloak"]
    ],
    "Rocket Spring Blueprint - Behind Vacuum": [
        []
    ],
    "Rocket Spring Blueprint - Front of 2nd House near entrance": [
        []
    ],
    "Rocket Spring Blueprint - Near Tree House on Ground": [
        []
    ],
    "Rocket Spring Blueprint - Near Cable Car House": [
        []
    ],
    "Rocket Spring Blueprint - Near Who Snowball in Cave": [
        []
    ],
    "Rocket Spring Blueprint - Branch Platform Closest to Glue Cannon": [
        []
    ],
    "Rocket Spring Blueprint - Branch Platform Near Beast": [
        []
    ],
    "Rocket Spring Blueprint - Branch Platform Ledge Grab House": [
        []
    ],
    "Rocket Spring Blueprint - On Tree House": [
        ["Rotten Egg Launcher"],
        ["Grinch Copter"]
    ],
    "Slime Shooter Blueprint - Branch Platform Elevated House": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "Slime Shooter Blueprint - Branch Platform House next to Beast": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "Slime Shooter Blueprint - House near Civic Center Cave": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "Slime Shooter Blueprint - House next to Tree House": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "Slime Shooter Blueprint - House across from Tree House": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "Slime Shooter Blueprint - 2nd House near entrance right side": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "Slime Shooter Blueprint - 2nd House near entrance left side": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "Slime Shooter Blueprint - 2nd House near entrance inbetween blueprints": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "Slime Shooter Blueprint - House near entrance": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "Octopus Climbing Device Blueprint - Middle Pipe": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Slime Shooter", "Rocket Spring"],
        ["Slime Shooter", "Grinch Copter"]
    ],
    "Octopus Climbing Device Blueprint - Right Pipe": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "Octopus Climbing Device Blueprint - Mayor's House Rat Vent": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "Octopus Climbing Device Blueprint - Left Pipe": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Slime Shooter", "Rocket Spring"],
        ["Slime Shooter", "Grinch Copter"]
    ],
    "Octopus Climbing Device Blueprint - Near Power Plant Wall on right side": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Slime Shooter", "Rocket Spring"],
        ["Slime Shooter", "Grinch Copter"]
    ],
    "Octopus Climbing Device Blueprint - Near Who-Bris' Shack": [
        ["Rotten Egg Launcher", "Rocket Spring"]
    ],
    "Octopus Climbing Device Blueprint - Guardian's House - Left Side": [
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Rotten Egg Launcher", "Slime Shooter", "Rocket Spring"]
    ],
    "Octopus Climbing Device Blueprint - Guardian's House - Right Side": [
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Rotten Egg Launcher", "Slime Shooter", "Rocket Spring"]
    ],
    "Octopus Climbing Device Blueprint - Inside Guardian's House": [
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Rotten Egg Launcher", "Slime Shooter", "Rocket Spring"]
    ],
    "Marine Mobile Blueprint - South Shore - Bridge to Scout's Hut": [
        []
    ],
    "Marine Mobile Blueprint - South Shore - Tent near Porcupine": [
        []
    ],
    "Marine Mobile Blueprint - South Shore - Near Outhouse": [
        []
    ],
    "Marine Mobile Blueprint - South Shore - Near Hill Bridge": [
        []
    ],
    "Marine Mobile Blueprint - South Shore - Scout's Hut Roof": [
        ["Rocket Spring"],
        ["Grinch Copter"]
    ],
    "Marine Mobile Blueprint - South Shore - Grass Platform": [
        ["Rocket Spring"],
        ["Grinch Copter"]
    ],
    "Marine Mobile Blueprint - South Shore - Zipline by Beast": [
        ["Rocket Spring", "Octopus Climbing Device"],
        ["Grinch Copter"]
    ],
    "Marine Mobile Blueprint - South Shore - Behind Summer Beast": [
        ["Rotten Egg Launcher", "Octopus Climbing Device"],
        ["Grinch Copter"]
    ],
    "Marine Mobile Blueprint - South Shore - Below Bridge": [
        []
    ],
    "Marine Mobile Blueprint - North Shore - Below Bridge": [
        []
    ],
    "Marine Mobile Blueprint - North Shore - Behind Skunk Hut": [
        []
    ],
    "Marine Mobile Blueprint - North Shore - Inside Skunk Hut": [
        []
    ],
    "Marine Mobile Blueprint - North Shore - Fenced in Area": [
        []
    ],
    "Marine Mobile Blueprint - North Shore - Boulder Box near Bridge": [
        []
    ],
    "Marine Mobile Blueprint - North Shore - Boulder Box behind Skunk Hut": [
        []
    ],
    "Marine Mobile Blueprint - North Shore - Inside Drill House": [
        []
    ],
    "Marine Mobile Blueprint - North Shore - Crow Platform near Drill House": [
        []
    ],
    "Grinch Copter Blueprint - Whoville City Hall - Safe Room": [
        []
    ],
    "Grinch Copter Blueprint - Whoville City Hall - Statue Room": [
        []
    ],
    "Grinch Copter Blueprint - Whoville Clock Tower - Before Bells": [
        ["Rocket Spring"]
    ],
    "Grinch Copter Blueprint - Whoville Clock Tower - After Bells": [
        ["Rocket Spring"]
    ],
    "Grinch Copter Blueprint - Who Forest Ski Resort - Inside Dog's Fence": [
        []
    ],
    "Grinch Copter Blueprint - Who Forest Ski Resort - Max Cave": [
        []
    ],
    "Grinch Copter Blueprint - Who Forest Civic Center - Climb across Bat Cave wall": [
        ["Grinch Copter"],
        ["Octopus Climbing Device", "Rocket Spring"]
    ],
    "Grinch Copter Blueprint - Who Forest Civic Center - Shoot Icicle in Bat Entrance": [
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Rotten Egg Launcher", "Octopus Climbing Device", "Rocket Spring"],
        ["Slime Shooter", "Grinch Copter"],
        ["Slime Shooter", "Octopus Climbing Device", "Rocket Spring"]
    ],
    "Grinch Copter Blueprint - Who Dump Power Plant - Max Cave": [
        []
    ],
    "Grinch Copter Blueprint - Who Dump Power Plant - After First Gate": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Grinch Copter"]
    ],
    "Grinch Copter Blueprint - Who Dump Generator Building - Before Mission": [
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Rotten Egg Launcher", "Octopus Climbing Device", "Slime Shooter", "Rocket Spring"]
    ],
    "Grinch Copter Blueprint - Who Dump Generator Building - After Mission": [
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Rotten Egg Launcher", "Octopus Climbing Device", "Slime Shooter", "Rocket Spring"]
    ],
    "Grinch Copter Blueprint - Who Lake South Shore - Submarine World - Above Surface": [
        ["Marine Mobile"]
    ],
    "Grinch Copter Blueprint - Who Lake South Shore - Submarine World - Underwater": [
        ["Marine Mobile"]
    ],
    "Grinch Copter Blueprint - Who Lake North Shore - Mayor's Villa - Tree Branch": [
        ["Grinch Copter"],
        ["Rotten Egg Launcher", "Rocket Spring"]
    ],
    "Grinch Copter Blueprint - Who Lake North Shore - Mayor's Villa - Cave": [
        ["Grinch Copter"],
        ["Rotten Egg Launcher", "Rocket Spring"]
    ],
    "Stealing All Gifts": [
        ["Exhaust Pipes", "GPS", "Tires", "Skis", "Twin-End Tuba"]
    ],
    "Neutralizing Santa": [
        ["Exhaust Pipes", "GPS", "Tires", "Skis", "Twin-End Tuba"]
    ]
}


access_rules_dict: dict[str,list[list[str]]] = {
    "Whoville": None,
    "Post Office": [
        ["Who Cloak"]
    ],
    "City Hall": [
        ["Rotten Egg Launcher"]
    ],
    "Countdown to X-Mas Clock Tower": None,
    "Who Forest": [
        ["Who Forest Vacuum Access"],
        # ["Progressive Vacuum Access": 1]
    ],
    "Ski Resort": [
        ["Cable Car Access Card"]
    ],
    "Civic Center": [
        ["Grinch Copter"],
        ["Octopus Climbing Device"]
    ],
    "Who Dump": [
        ["Who Dump Vacuum Access"],
        # ["Progressive Vacuum Access": 2]
    ],
    "Minefield": [
        ["Rotten Egg Launcher", "Slime Shooter", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "Power Plant": [
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Slime Shooter", "Grinch Copter"],
        ["Rotten Egg Launcher", "Octopus Climbing Device", "Slime Shooter", "Rocket Spring"]
    ],
    "Generator Building": [
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Rotten Egg Launcher", "Octopus Climbing Device", "Slime Shooter", "Rocket Spring"]
    ],
    "Who Lake": [
        ["Who Lake Vacuum Access"],
        # ["Progressive Vacuum Access": 3]
    ],
    "Scout's Hut": [
        ["Grinch Copter"],
        ["Rocket Spring"]
    ],
    "North Shore": [
        ["Scout Clothes"]
    ],
    "Mayor's Villa": [
        ["Scout Clothes"]
    ],
    "Submarine World": [
        ["Marine Mobile"]
    ],
    "Sleigh Room": [
        ["Exhaust Pipes", "GPS", "Tires", "Skis", "Twin-End Tuba"]
    ]
}


# def interpret_rule(rule_set: list[list[str]], player: int):
#     old_rule = lambda state: True
#     if len(rule_set) < 1:
#         return old_rule
#     else:
#         old_rule = lambda state: False
#     for item_set in rule_set:
#         logger.info("Rules to access: " + ";".join(item_set))
#         old_rule = lambda state: state.has_all(item_set, player) or old_rule
#     return old_rule

def interpret_rule(rule_set: list[list[str]], player: int):
    if not rule_set or all(not inner_list for inner_list in rule_set):
        return lambda state: True
    and_groups: list[set[str]] = []
    for inner_list in rule_set:
        and_groups.append(set(inner_list))

    return lambda target_items_raw: (
        (target_items_set := set(target_items_raw)) and
        player in target_items_set and
        any(
            all(item in target_items_set for item in and_group)
            for and_group in and_groups
        )
    )