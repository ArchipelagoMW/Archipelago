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
        access_list.append(lambda state, items=tuple(item_set): state.has_all(items, player))
    return access_list

    #Each item in the list is a separate list of rules. Each separate list is just an "OR" condition.
rules_dict: dict[str,list[list[str]]] = {
    "WV - First Visit": [
        []
    ],
    "WV - Post Office - First Visit": [
        []
    ],
    "WV - City Hall - First Visit": [
        []
    ],
    "WV - Clock Tower - First Visit": [
        []
    ],
    "WF - First Visit": [
        []
    ],
    "WF - Ski Resort - First Visit": [
        []
    ],
    "WF - Civic Center - First Visit": [
        []
    ],
    "WD - First Visit": [
        []
    ],
    "WD - Minefield - First Visit": [
        []
    ],
    "WD - Power Plant - First Visit": [
        []
    ],
    "WD - Generator Building - First Visit": [
        []
    ],
    "WL - South Shore- First Visit": [
        []
    ],
    "WL - Submarine World - First Visit": [
        []
    ],
    "WL - Scout's Hut - First Visit": [
        []
    ],
    "WL - North Shore - First Visit": [
        []
    ],
    "WL - Mayor's Villa - First Visit": [
        []
    ],
    "WV - Post Office - Shuffling The Mail": [
        []
    ],
    "WV - Smashing Snowmen": [
        []
    ],
    "WV - Painting The Mayor's Posters": [
        ["Painting Bucket"]
    ],
    "WV - Launching Eggs Into Houses": [
        ["Rotten Egg Launcher"]
    ],
    "WV - City Hall - Modifying The Mayor's Statue": [
        ["Sculpting Tools"]
    ],
    "WV - Clock Tower - Advancing The Countdown-To-Xmas Clock": [
        ["Hammer", "Rocket Spring"]
    ],
    "WV - Squashing All Gifts": [
        ["Grinch Copter", "Slime Shooter", "Rotten Egg Launcher", "Who Cloak", "Rocket Spring"]
    ],
    "WF - Making Xmas Trees Droop": [
        ["Rotten Egg Launcher"]
    ],
    "WF - Sabotaging Snow Cannon With Glue": [
        ["Glue Bucket", "Rocket Spring"],
        ["Glue Bucket", "Grinch Copter"]
    ],
    "WF - Putting Beehives In Cabins": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "WF - Ski Resort - Sliming The Mayor's Skis": [
        ["Slime Shooter", "Rotten Egg Launcher"]
    ],
    "WF - Civic Center - Replacing The Candles On The Cake With Fireworks": [
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Rotten Egg Launcher", "Octopus Climbing Device", "Rocket Spring"]
    ],
    "WF - Squashing All Gifts": [
        ["Grinch Copter", "Cable Car Access Card", "Slime Shooter", "Rotten Egg Launcher"],
        ["Octopus Climbing Device", "Rocket Spring", "Cable Car Access Card", "Slime Shooter", "Rotten Egg Launcher"]
    ],
    "WD - Stealing Food From Birds": [
        ["Rocket Spring", "Rotten Egg Launcher"]
    ],
    "WD - Feeding The Computer With Robot Parts": [
        ["Rocket Spring", "Rotten Egg Launcher"]
    ],
    "WD - Infesting The Mayor's House With Rats": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "WD - Conducting The Stinky Gas To Who-Bris' Shack": [
        ["Rocket Spring", "Rotten Egg Launcher"]
    ],
    "WD - Minefield - Shaving Who Dump Guardian": [
        ["Scissors", "Grinch Copter"],
        ["Scissors", "Slime Shooter", "Rocket Spring"]
    ],
    "WD - Generator Building - Short-Circuiting Power-Plant": [
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Rotten Egg Launcher", "Octopus Climbing Device", "Slime Shooter", "Rocket Spring"]
    ],
    "WD - Squashing All Gifts": [
        ["Grinch Copter", "Rocket Spring", "Slime Shooter", "Rotten Egg Launcher"],
        ["Octopus Climbing Device", "Rocket Spring", "Slime Shooter", "Rotten Egg Launcher"]
    ],
    "WL - South Shore - Putting Thistles In Shorts": [
        ["Rotten Egg Launcher", "Octopus Climbing Device"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "WL - South Shore - Sabotaging The Tents": [
        ["Octopus Climbing Device", "Rocket Spring"],
        ["Grinch Copter"]
    ],
    "WL - North Shore - Drilling Holes In Canoes": [
        ["Drill"]
        # ["Drill", "Max"]
    ],
    "WL - Submarine World - Modifying The Marine Mobile": [
        []
    ],
    "WL - Mayor's Villa - Hooking The Mayor's Bed To The Motorboat": [
        ["Rope", "Hook", "Rotten Egg Launcher", "Scout Clothes"]
    ],
    "WL - Squashing All Gifts": [
        ["Grinch Copter", "Marine Mobile", "Scout Clothes", "Rotten Egg Launcher", "Hook", "Rope"],
        ["Octopus Climbing Device", "Rocket Spring", "Marine Mobile", "Scout Clothes", "Rotten Egg Launcher", "Hook", "Rope"]
    ],
    "WV - Binoculars BP on Post Office Roof": [
        []
    ],
    "WV - City Hall - Binoculars BP left side of Library": [
        []
    ],
    "WV - City Hall - Binoculars BP front side of Library": [
        []
    ],
    "WV - City Hall - Binoculars BP right side of Library": [
        []
    ],
    "WV - REL BP left of City Hall": [
        []
    ],
    "WV - REL BP left of Clock Tower": [
        []
    ],
    "WV - Post Office - REL BP inside Silver Room": [
        ["Who Cloak"]
        # ["Who Cloak", "Max"]
    ],
    "WV - Post Office - REL BP at Entrance Door after Mission Completion": [
        ["Who Cloak"]
        # ["Who Cloak", "Max"]
    ],
    "WF - RS BP behind Vacuum Tube": [
        []
    ],
    "WF - RS BP in front of 2nd House near Vacuum Tube": [
        []
    ],
    "WF - RS BP near Tree House on Ground": [
        []
    ],
    "WF - RS BP behind Cable Car House": [
        []
    ],
    "WF - RS BP near Who Snowball in Cave": [
        []
    ],
    "WF - RS BP on Branch Platform closest to Glue Cannon": [
        []
    ],
    "WF - RS BP on Branch Platform Near Beast": [
        []
    ],
    "WF - RS BP on Branch Platform Elevated next to House": [
        []
    ],
    "WF - RS BP on Tree House": [
        ["Rotten Egg Launcher"],
        ["Grinch Copter"]
    ],
    "WF - SS BP in Branch Platform Elevated House": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "WF - SS BP in Branch Platform House next to Beast": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "WF - SS BP in House in front of Civic Center Cave": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "WF - SS BP in House next to Tree House": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "WF - SS BP in House across from Tree House": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "WF - SS BP in 2nd House near Vacuum Tube Right Side": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "WF - SS BP in 2nd House near Vacuum Tube Left Side": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "WF - SS BP in 2nd House near Vacuum Tube inbetween Blueprints": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "WF - SS BP in House near Vacuum Tube": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "WD - OCD BP inside Middle Pipe": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Slime Shooter", "Rocket Spring"],
        ["Slime Shooter", "Grinch Copter"]
    ],
    "WD - OCD BP inside Right Pipe": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "WD - OCD BP in Vent to Mayor's House": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "WD - OCD BP inside Left Pipe": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Slime Shooter", "Rocket Spring"],
        ["Slime Shooter", "Grinch Copter"]
    ],
    "WD - OCD BP near Right Side of Power Plant Wall": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Slime Shooter", "Rocket Spring"],
        ["Slime Shooter", "Grinch Copter"]
    ],
    "WD - OCD BP near Who-Bris' Shack": [
        ["Rotten Egg Launcher", "Rocket Spring"]
    ],
    "WD - Minefield - OCD BP on Left Side of House": [
        []
        # ["Rotten Egg Launcher", "Grinch Copter"],
        # ["Rotten Egg Launcher", "Slime Shooter", "Rocket Spring"]
        # ["Max"]
    ],
    "WD - Minefield - OCD BP on Right Side of Shack": [
        ["Grinch Copter"],
        ["Slime Shooter", "Rocket Spring"]
    ],
    "WD - Minefield - OCD BP inside Guardian's House": [
        []
        # ["Rotten Egg Launcher", "Grinch Copter"],
        # ["Rotten Egg Launcher", "Slime Shooter", "Rocket Spring"]
        # ["Max"]
    ],
    "WL - South Shore - MM BP on Bridge to Scout's Hut": [
        []
    ],
    "WL - South Shore - MM BP across from Tent near Porcupine": [
        []
    ],
    "WL - South Shore - MM BP near Outhouse": [
        []
    ],
    "WL - South Shore - MM BP near Hill Bridge": [
        []
    ],
    "WL - South Shore - MM BP on Scout's Hut Roof": [
        ["Rocket Spring"],
        ["Grinch Copter"]
    ],
    "WL - South Shore - MM BP on Grass Platform": [
        ["Rocket Spring"],
        ["Grinch Copter"]
    ],
    "WL - South Shore - MM BP across Zipline Platform": [
        ["Rocket Spring", "Octopus Climbing Device"],
        ["Grinch Copter"]
    ],
    "WL - South Shore - MM BP behind Summer Beast": [
        ["Rotten Egg Launcher", "Octopus Climbing Device"],
        ["Grinch Copter"]
    ],
    "WL - North Shore - MM BP below Bridge": [
        []
    ],
    "WL - North Shore - MM BP behind Skunk Hut": [
        []
    ],
    "WL - North Shore - MM BP inside Skunk Hut": [
        []
        # ["Max"]
    ],
    "WL - North Shore - MM BP inside House's Fence": [
        []
        # ["Max"]
    ],
    "WL - North Shore - MM BP inside Boulder Box near Bridge": [
        []
    ],
    "WL - North Shore - MM BP inside Boulder Box behind Skunk Hut": [
        []
    ],
    "WL - North Shore - MM BP inside Drill House": [
        []
    ],
    "WL - North Shore - MM BP on Crow Platform near Drill House": [
        []
    ],
    "WV - City Hall - GC BP in Safe Room": [
        []
    ],
    "WV - City Hall - GC BP in Statue Room": [
        []
    ],
    "WV - Clock Tower - GC BP in Bedroom": [
        ["Rocket Spring"]
    #   ["Max", "Rocket Spring"]
    ],
    "WV - Clock Tower - GC BP in Bell Room": [
        ["Rocket Spring"]
    ],
    "WF - Ski Resort - GC BP inside Dog's Fence": [
        []
    ],
    "WF - Ski Resort - GC BP in Max Cave": [
        []
        # ["Max"]
    ],
    "WF - Civic Center - GC BP on Left Side in Bat Cave Wall": [
        ["Grinch Copter"],
        ["Octopus Climbing Device", "Rocket Spring"]
    ],
    "WF - Civic Center - GC BP in Frozen Ice": [
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Rotten Egg Launcher", "Octopus Climbing Device", "Rocket Spring"],
        ["Slime Shooter", "Grinch Copter"],
        ["Slime Shooter", "Octopus Climbing Device", "Rocket Spring"]
    ],
    "WD - Power Plant - GC BP in Max Cave": [
        []
        # ["Max"]
    ],
    "WD - Power Plant - GC BP After First Gate": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Grinch Copter"]
    #   ["Max", "Rotten Egg Launcher", "Rocket Spring"]
    ],
    "WD - Generator Building - GC BP on the Highest Platform": [
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Rotten Egg Launcher", "Octopus Climbing Device", "Slime Shooter", "Rocket Spring"]
    ],
    "WD - Generator Building - GC BP at the Entrance after Mission Completion": [
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Rotten Egg Launcher", "Octopus Climbing Device", "Slime Shooter", "Rocket Spring"]
    ],
    "WL - Submarine World - GC BP Just Below Water Surface": [
        ["Marine Mobile"]
    ],
    "WL - Submarine World - GC BP Underwater": [
        ["Marine Mobile"]
    ],
    "WL - Mayor's Villa - GC BP on Tree Branch": [
        ["Grinch Copter"],
        ["Rotten Egg Launcher", "Rocket Spring"]
    ],
    "WL - Mayor's Villa - GC BP in Pirate's Cave": [
        ["Grinch Copter"],
        ["Rotten Egg Launcher", "Rocket Spring"]
    ],
    "MC - Sleigh Ride - Stealing All Gifts": [
        # ["Exhaust Pipes", "Tires", "Skis", "Twin-End Tuba"]
        ["Rotten Egg Launcher", "Who Forest Vacuum Tube", "Who Dump Vacuum Tube", "Who Lake Vacuum Tube", "Rocket Spring", "Marine Mobile"]
    ],
    "MC - Sleigh Ride - Neutralizing Santa": [
        # ["Exhaust Pipes", "Tires", "Skis", "Twin-End Tuba"]
        ["Rotten Egg Launcher", "Who Forest Vacuum Tube", "Who Dump Vacuum Tube", "Who Lake Vacuum Tube", "Rocket Spring", "Marine Mobile"]
    ],
    "WV - Post Office - Heart of Stone": [
        []
    ],
    "WF - Ski Resort - Heart of Stone": [
        []
    ],
    "WD - Minefield - Heart of Stone": [
        ["Grinch Copter"],
        ["Rotten Egg Launcher", "Slime Shooter", "Rocket Spring"]
    ],
    "WL - North Shore - Heart of Stone": [
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
    "WV - Exhaust Pipes": [
        ["Rotten Egg Launcher"]
    ],
    "WF - Skis": [
        ["Who Forest Vacuum Tube"]
    ],
    "WD - Tires": [
        ["Who Dump Vacuum Tube", "Rocket Spring", "Rotten Egg Launcher"]
    ],
    "WL - Submarine World - Twin-End Tuba": [
        ["Who Lake Vacuum Tube", "Marine Mobile"]
    ],
    "WL - South Shore - GPS": [
        ["Who Lake Vacuum Tube", "Rotten Egg Launcher"]
    ],
    "MC - 1st Crate Squashed": [
        []
    ],
    "MC - 2nd Crate Squashed": [
        []
    ],
    "MC - 3rd Crate Squashed": [
        []
    ],
    "MC - 4th Crate Squashed": [
        []
    ],
    "MC - 5th Crate Squashed": [
        []
    ]
    # "Green Present": [
    #     []
    # ],
    # "Red Present": [
    #     []
    # ],
    # "Pink Present": [
    #     ["Rotten Egg Launcher"],
    #     ["Pancake"]
    # ],
    # "Yellow Present": [
    #     ["Pancake"]
    # ]
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
    "Clock Tower": [
        []
    ],
    "Who Forest": [
        ["Who Forest Vacuum Tube"],
        # ["Progressive Vacuum Tube": 1]
    ],
    "Ski Resort": [
        ["Cable Car Access Card"]
    ],
    "Civic Center": [
        ["Grinch Copter"],
        ["Octopus Climbing Device"]
    ],
    "Who Dump": [
        ["Who Dump Vacuum Tube"],
        # ["Progressive Vacuum Tube": 2]
    ],
    "Minefield": [
        ["Rotten Egg Launcher", "Rocket Spring"],
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
        ["Who Lake Vacuum Tube"],
        # ["Progressive Vacuum Tube": 3]
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
    "Spin N' Win": [
        []
        # ["Spin N' Win Door Unlock"],
        # ["Progressive Supadow Door Unlock"]
    ],
    "Dankamania": [
        []
        # ["Dankamania Door Unlock"],
        # ["Progressive Supadow Door Unlock: 2"]
    ],
    "The Copter Race Contest": [
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