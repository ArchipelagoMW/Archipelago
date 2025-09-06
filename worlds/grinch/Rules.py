from typing import Callable

import Utils
from BaseClasses import CollectionState
from worlds.AutoWorld import World
from worlds.generic.Rules import add_rule

#Adds all rules from access_rules_dict to locations
def set_location_rules(world: World):
    all_locations = world.get_locations()
    for location in all_locations:
        loc_rules = rules_dict[location.name]
        rule_list = interpret_rule(loc_rules, world.player)
        for access_rule in rule_list:
            if rule_list.index(access_rule) == 0:
                add_rule(location, access_rule)
            else:
                add_rule(location, access_rule, "or")

def interpret_rule(rule_set: list[list[str]], player: int):
    # If a region/location does not have any items required, make the section(s) return no logic.
    if len(rule_set) < 1:
        return True

    # Otherwise, if a region/location DOES have items required, make the section(s) return list of logic.

    access_list: list[Callable[[CollectionState], bool]] = []
    for item_set in rule_set:
        access_list.append(lambda state: state.has_all(item_set, player))
    return access_list

    #Each item in the list is a separate list of rules. Each separate list is just an "OR" condition.
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
    "Shuffling The Mail": [
        []
    ],
    "Smashing Snowmen": [
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
    "Squashing All Gifts in Whoville": [
        ["Grinch Copter", "Slime Shooter", "Rotten Egg Launcher", "Who Cloak", "Rocket Spring"]
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
    "Squashing All Gifts in Who Forest": [
        ["Grinch Copter", "Cable Car Access Card", "Slime Shooter", "Rotten Egg Launcher"],
        ["Octopus Climbing Device", "Rocket Spring", "Cable Car Access Card", "Slime Shooter", "Rotten Egg Launcher"]
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
        ["Scissors", "Slime Shooter", "Rocket Spring"]
    ],
    "Short-Circuiting Power-Plant": [
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Rotten Egg Launcher", "Octopus Climbing Device", "Slime Shooter", "Rocket Spring"]
    ],
    "Squashing All Gifts in Who Dump": [
        ["Grinch Copter", "Rocket Spring", "Slime Shooter", "Rotten Egg Launcher"],
        ["Octopus Climbing Device", "Rocket Spring", "Slime Shooter", "Rotten Egg Launcher"]
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
        # ["Drill", "Max"]
    ],
    "Modifying The Marine Mobile": [
        []
    ],
    "Hooking The Mayor's Bed To The Motorboat": [
        ["Rope", "Hook", "Rotten Egg Launcher", "Scout Clothes"]
    ],
    "Squashing All Gifts in Who Lake": [
        ["Grinch Copter", "Marine Mobile", "Scout Clothes", "Rotten Egg Launcher", "Hook", "Rope"],
        ["Octopus Climbing Device", "Rocket Spring", "Marine Mobile", "Scout Clothes", "Rotten Egg Launcher", "Hook", "Rope"]
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
    "REL Blueprint - Outside City Hall": [
        []
    ],
    "REL Blueprint - Outside Clock Tower": [
        []
    ],
    "REL Blueprint - Post Office - Inside Silver Room": [
        ["Who Cloak"]
        # ["Who Cloak", "Max"]
    ],
    "REL Blueprint - Post Office - After Mission Completion": [
        ["Who Cloak"]
        # ["Who Cloak", "Max"]
    ],
    "RS Blueprint - Behind Vacuum": [
        []
    ],
    "RS Blueprint - Front of 2nd House near entrance": [
        []
    ],
    "RS Blueprint - Near Tree House on Ground": [
        []
    ],
    "RS Blueprint - Near Cable Car House": [
        []
    ],
    "RS Blueprint - Near Who Snowball in Cave": [
        []
    ],
    "RS Blueprint - Branch Platform Closest to Glue Cannon": [
        []
    ],
    "RS Blueprint - Branch Platform Near Beast": [
        []
    ],
    "RS Blueprint - Branch Platform Ledge Grab House": [
        []
    ],
    "RS Blueprint - On Tree House": [
        ["Rotten Egg Launcher"],
        ["Grinch Copter"]
    ],
    "SS Blueprint - Branch Platform Elevated House": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "SS Blueprint - Branch Platform House next to Beast": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "SS Blueprint - House near Civic Center Cave": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "SS Blueprint - House next to Tree House": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "SS Blueprint - House across from Tree House": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "SS Blueprint - 2nd House near entrance right side": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "SS Blueprint - 2nd House near entrance left side": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "SS Blueprint - 2nd House near entrance inbetween blueprints": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "SS Blueprint - House near entrance": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "OCD Blueprint - Middle Pipe": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Slime Shooter", "Rocket Spring"],
        ["Slime Shooter", "Grinch Copter"]
    ],
    "OCD Blueprint - Right Pipe": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "OCD Blueprint - Mayor's House Rat Vent": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "OCD Blueprint - Left Pipe": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Slime Shooter", "Rocket Spring"],
        ["Slime Shooter", "Grinch Copter"]
    ],
    "OCD Blueprint - Near Power Plant Wall on right side": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Slime Shooter", "Rocket Spring"],
        ["Slime Shooter", "Grinch Copter"]
    ],
    "OCD Blueprint - Near Who-Bris' Shack": [
        ["Rotten Egg Launcher", "Rocket Spring"]
    ],
    "OCD Blueprint - Guardian's House - Left Side": [
        []
        # ["Rotten Egg Launcher", "Grinch Copter"],
        # ["Rotten Egg Launcher", "Slime Shooter", "Rocket Spring"]
        # ["Max"]
    ],
    "OCD Blueprint - Guardian's House - Right Side": [
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Slime Shooter", "Rocket Spring"]
    ],
    "OCD Blueprint - Inside Guardian's House": [
        []
        # ["Rotten Egg Launcher", "Grinch Copter"],
        # ["Rotten Egg Launcher", "Slime Shooter", "Rocket Spring"]
        # ["Max"]
    ],
    "MM Blueprint - South Shore - Bridge to Scout's Hut": [
        []
    ],
    "MM Blueprint - South Shore - Tent near Porcupine": [
        []
    ],
    "MM Blueprint - South Shore - Near Outhouse": [
        []
    ],
    "MM Blueprint - South Shore - Near Hill Bridge": [
        []
    ],
    "MM Blueprint - South Shore - Scout's Hut Roof": [
        ["Rocket Spring"],
        ["Grinch Copter"]
    ],
    "MM Blueprint - South Shore - Grass Platform": [
        ["Rocket Spring"],
        ["Grinch Copter"]
    ],
    "MM Blueprint - South Shore - Zipline by Beast": [
        ["Rocket Spring", "Octopus Climbing Device"],
        ["Grinch Copter"]
    ],
    "MM Blueprint - South Shore - Behind Summer Beast": [
        ["Rotten Egg Launcher", "Octopus Climbing Device"],
        ["Grinch Copter"]
    ],
    "MM Blueprint - South Shore - Below Bridge": [
        []
    ],
    "MM Blueprint - North Shore - Below Bridge": [
        []
    ],
    "MM Blueprint - North Shore - Behind Skunk Hut": [
        []
    ],
    "MM Blueprint - North Shore - Inside Skunk Hut": [
        []
        # ["Max"]
    ],
    "MM Blueprint - North Shore - Fenced in Area": [
        []
        # ["Max"]
    ],
    "MM Blueprint - North Shore - Boulder Box near Bridge": [
        []
    ],
    "MM Blueprint - North Shore - Boulder Box behind Skunk Hut": [
        []
    ],
    "MM Blueprint - North Shore - Inside Drill House": [
        []
    ],
    "MM Blueprint - North Shore - Crow Platform near Drill House": [
        []
    ],
    "GC Blueprint - Whoville City Hall - Safe Room": [
        []
    ],
    "GC Blueprint - Whoville City Hall - Statue Room": [
        []
    ],
    "GC Blueprint - Whoville Clock Tower - Before Bells": [
        ["Rocket Spring"]
    #   ["Max", "Rocket Spring"]
    ],
    "GC Blueprint - Whoville Clock Tower - After Bells": [
        ["Rocket Spring"]
    ],
    "GC Blueprint - Who Forest Ski Resort - Inside Dog's Fence": [
        []
    ],
    "GC Blueprint - Who Forest Ski Resort - Max Cave": [
        []
        # ["Max"]
    ],
    "GC Blueprint - Who Forest Civic Center - Climb across Bat Cave wall": [
        ["Grinch Copter"],
        ["Octopus Climbing Device", "Rocket Spring"]
    ],
    "GC Blueprint - Who Forest Civic Center - Shoot Icicle in Bat Entrance": [
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Rotten Egg Launcher", "Octopus Climbing Device", "Rocket Spring"],
        ["Slime Shooter", "Grinch Copter"],
        ["Slime Shooter", "Octopus Climbing Device", "Rocket Spring"]
    ],
    "GC Blueprint - Who Dump Power Plant - Max Cave": [
        []
        # ["Max"]
    ],
    "GC Blueprint - Who Dump Power Plant - After First Gate": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Grinch Copter"]
    #   ["Max", "Rotten Egg Launcher", "Rocket Spring"]
    ],
    "GC Blueprint - Who Dump Generator Building - Before Mission": [
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Rotten Egg Launcher", "Octopus Climbing Device", "Slime Shooter", "Rocket Spring"]
    ],
    "GC Blueprint - Who Dump Generator Building - After Mission": [
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Rotten Egg Launcher", "Octopus Climbing Device", "Slime Shooter", "Rocket Spring"]
    ],
    "GC Blueprint - Who Lake South Shore - Submarine World - Above Surface": [
        ["Marine Mobile"]
    ],
    "GC Blueprint - Who Lake South Shore - Submarine World - Underwater": [
        ["Marine Mobile"]
    ],
    "GC Blueprint - Who Lake North Shore - Mayor's Villa - Tree Branch": [
        ["Grinch Copter"],
        ["Rotten Egg Launcher", "Rocket Spring"]
    ],
    "GC Blueprint - Who Lake North Shore - Mayor's Villa - Cave": [
        ["Grinch Copter"],
        ["Rotten Egg Launcher", "Rocket Spring"]
    ],
    "Stealing All Gifts": [
        # ["Exhaust Pipes", "Tires", "Skis", "Twin-End Tuba"]
        ["Rotten Egg Launcher", "Who Forest Vacuum Access", "Who Dump Vacuum Access", "Who Lake Vacuum Access", "Rocket Spring", "Marine Mobile"]
    ],
    "Neutralizing Santa": [
        # ["Exhaust Pipes", "Tires", "Skis", "Twin-End Tuba"]
        ["Rotten Egg Launcher", "Who Forest Vacuum Access", "Who Dump Vacuum Access", "Who Lake Vacuum Access", "Rocket Spring", "Marine Mobile"]
    ],
    "Heart of Stone - Whoville's Post Office": [
        []
    ],
    "Heart of Stone - Who Forest's Ski Resort": [
        []
    ],
    "Heart of Stone - Who Dump's Minefield": [
        ["Grinch Copter"],
        ["Rotten Egg Launcher", "Slime Shooter", "Rocket Spring"]
    ],
    "Heart of Stone - Who Lake's North Shore": [
        []
        # ["Max"]
    ],
    "Spin N' Win - Easy": [
        []
    ],
    "Spin N' Win - Hard": [
        []
    ],
    "Spin N' Win - Real Tough": [
        []
    ],
    "Dankamania - Easy - 15 Points": [
        []
    ],
    "Dankamania - Hard - 15 Points": [
        []
    ],
    "Dankamania - Real Tough - 15 Points": [
        []
    ],
    "The Copter Race Contest - Easy": [
        []
    ],
    "The Copter Race Contest - Hard": [
        []
    ],
    "The Copter Race Contest - Real Tough": [
        []
    ],
    "Bike Race - 1st Place": [
        []
    ],
    "Bike Race - Top 2": [
        []
    ],
    "Bike Race - Top 3": [
        []
    ],
    "Exhaust Pipes in Whoville": [
        ["Rotten Egg Launcher"]
    ],
    "Skis in Who Forest": [
        ["Who Forest Vacuum Access"]
    ],
    "Tires in Who Dump": [
        ["Who Dump Vacuum Access", "Rocket Spring", "Rotten Egg Launcher"]
    ],
    "Twin-End Tuba in Submarine World": [
        ["Who Lake Vacuum Access", "Marine Mobile"]
    ],
    "GPS in Who Lake": [
        ["Who Lake Vacuum Access", "Rotten Egg Launcher"]
    ],
}


access_rules_dict: dict[str,list[list[str]]] = {
    "Whoville": [
        []
    ],
    "Post Office": [
        ["Who Cloak"]
    ],
    "City Hall": [
        ["Rotten Egg Launcher"]
    ],
    "Countdown to X-Mas Clock Tower": [
        []
    ],
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
        ["Sleigh Room Key"]
    ],
    "Spin N' Win Supadow": [
        []
        # ["Spin N' Win Door Unlock"],
        # ["Progressive Supadow Door Unlock"]
    ],
    "Dankamania Supadow": [
        []
        # ["Dankamania Door Unlock"],
        # ["Progressive Supadow Door Unlock: 2"]
    ],
    "The Copter Race Contest Supadow": [
        []
        # ["The Copter Race Contest Door Unlock"],
        # ["Progressive Supadow Door Unlock: 3"]
    ],
    "Bike Race": [
        []
        # ["Bike Race Access"],
        # ["Progressive Supadow Door Unlock: 4"]
    ]
}