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
    "Whoville - First Visit": [
        []
    ],
    "Whoville's Post Office - First Visit": [
        []
    ],
    "Whoville's City Hall - First Visit": [
        []
    ],
    "Whoville's Clock Tower - First Visit": [
        []
    ],
    "Who Forest - First Visit": [
        []
    ],
    "Who Forest's Ski Resort - First Visit": [
        []
    ],
    "Who Forest's Civic Center - First Visit": [
        []
    ],
    "Who Dump - First Visit": [
        []
    ],
    "Who Dump's Minefield - First Visit": [
        []
    ],
    "Who Dump's Power Plant - First Visit": [
        []
    ],
    "Who Dump's Generator Building - First Visit": [
        []
    ],
    "Who Lake's South Shore- First Visit": [
        []
    ],
    "Who Lake's Submarine World - First Visit": [
        []
    ],
    "Who Lake's Scout's Hut - First Visit": [
        []
    ],
    "Who Lake's North Shore - First Visit": [
        []
    ],
    "Who Lake's Mayor's Villa - First Visit": [
        []
    ],
    "Whoville's Post Office - Shuffling The Mail": [
        []
    ],
    "Whoville - Smashing Snowmen": [
        []
    ],
    "Whoville - Painting The Mayor's Posters": [
        ["Painting Bucket"]
    ],
    "Whoville - Launching Eggs Into Houses": [
        ["Rotten Egg Launcher"]
    ],
    "Whoville's City Hall - Modifying The Mayor's Statue": [
        ["Sculpting Tools"]
    ],
    "Whoville's Clock Tower - Advancing The Countdown-To-Xmas Clock": [
        ["Hammer", "Rocket Spring"]
    ],
    "Whoville - Squashing All Gifts": [
        ["Grinch Copter", "Slime Shooter", "Rotten Egg Launcher", "Who Cloak", "Rocket Spring"]
    ],
    "Who Forest - Making Xmas Trees Droop": [
        ["Rotten Egg Launcher"]
    ],
    "Who Forest - Sabotaging Snow Cannon With Glue": [
        ["Glue Bucket", "Rocket Spring"],
        ["Glue Bucket", "Grinch Copter"]
    ],
    "Who Forest - Putting Beehives In Cabins": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "Who Forest's Ski Resort - Sliming The Mayor's Skis": [
        ["Slime Shooter", "Rotten Egg Launcher"]
    ],
    "Who Forest's Civic Center - Replacing The Candles On The Cake With Fireworks": [
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Rotten Egg Launcher", "Octopus Climbing Device", "Rocket Spring"]
    ],
    "Who Forest - Squashing All Gifts": [
        ["Grinch Copter", "Cable Car Access Card", "Slime Shooter", "Rotten Egg Launcher"],
        ["Octopus Climbing Device", "Rocket Spring", "Cable Car Access Card", "Slime Shooter", "Rotten Egg Launcher"]
    ],
    "Who Dump - Stealing Food From Birds": [
        ["Rocket Spring", "Rotten Egg Launcher"]
    ],
    "Who Dump - Feeding The Computer With Robot Parts": [
        ["Rocket Spring", "Rotten Egg Launcher"]
    ],
    "Who Dump - Infesting The Mayor's House With Rats": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "Who Dump - Conducting The Stinky Gas To Who-Bris' Shack": [
        ["Rocket Spring", "Rotten Egg Launcher"]
    ],
    "Who Dump's Minefield - Shaving Who Dump Guardian": [
        ["Scissors", "Grinch Copter"],
        ["Scissors", "Slime Shooter", "Rocket Spring"]
    ],
    "Who Dump's Generator Building - Short-Circuiting Power-Plant": [
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Rotten Egg Launcher", "Octopus Climbing Device", "Slime Shooter", "Rocket Spring"]
    ],
    "Who Dump - Squashing All Gifts": [
        ["Grinch Copter", "Rocket Spring", "Slime Shooter", "Rotten Egg Launcher"],
        ["Octopus Climbing Device", "Rocket Spring", "Slime Shooter", "Rotten Egg Launcher"]
    ],
    "Who Lake's South Shore - Putting Thistles In Shorts": [
        ["Rotten Egg Launcher", "Octopus Climbing Device"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "Who Lake's South Shore - Sabotaging The Tents": [
        ["Octopus Climbing Device", "Rocket Spring"],
        ["Grinch Copter"]
    ],
    "Who Lake's North Shore - Drilling Holes In Canoes": [
        ["Drill"]
        # ["Drill", "Max"]
    ],
    "Who Lake's Submarine World - Modifying The Marine Mobile": [
        []
    ],
    "Who Lake's Mayor's Villa - Hooking The Mayor's Bed To The Motorboat": [
        ["Rope", "Hook", "Rotten Egg Launcher", "Scout Clothes"]
    ],
    "Who Lake - Squashing All Gifts": [
        ["Grinch Copter", "Marine Mobile", "Scout Clothes", "Rotten Egg Launcher", "Hook", "Rope"],
        ["Octopus Climbing Device", "Rocket Spring", "Marine Mobile", "Scout Clothes", "Rotten Egg Launcher", "Hook", "Rope"]
    ],
    "Whoville - Binoculars Blueprint on Post Office Roof": [
        []
    ],
    "Whoville's City Hall - Binoculars Blueprint left side of Library": [
        []
    ],
    "Whoville's City Hall - Binoculars Blueprint front side of Library": [
        []
    ],
    "Whoville's City Hall - Binoculars Blueprint right side of Library": [
        []
    ],
    "Whoville - REL Blueprint left of City Hall": [
        []
    ],
    "Whoville - REL Blueprint left of Clock Tower": [
        []
    ],
    "Whoville's Post Office - REL Blueprint inside Silver Room": [
        ["Who Cloak"]
        # ["Who Cloak", "Max"]
    ],
    "Whoville's Post Office - REL Blueprint at Entrance Door after Mission Completion": [
        ["Who Cloak"]
        # ["Who Cloak", "Max"]
    ],
    "Who Forest - RS Blueprint behind Vacuum Tube": [
        []
    ],
    "Who Forest - RS Blueprint in front of 2nd House near Vacuum Tube": [
        []
    ],
    "Who Forest - RS Blueprint near Tree House on Ground": [
        []
    ],
    "Who Forest - RS Blueprint behind Cable Car House": [
        []
    ],
    "Who Forest - RS Blueprint near Who Snowball in Cave": [
        []
    ],
    "Who Forest - RS Blueprint on Branch Platform closest to Glue Cannon": [
        []
    ],
    "Who Forest - RS Blueprint on Branch Platform Near Beast": [
        []
    ],
    "Who Forest - RS Blueprint on Branch Platform Elevated next to House": [
        []
    ],
    "Who Forest - RS Blueprint on Tree House": [
        ["Rotten Egg Launcher"],
        ["Grinch Copter"]
    ],
    "Who Forest - SS Blueprint in Branch Platform Elevated House": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "Who Forest - SS Blueprint in Branch Platform House next to Beast": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "Who Forest - SS Blueprint in House in front of Civic Center Cave": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "Who Forest - SS Blueprint in House next to Tree House": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "Who Forest - SS Blueprint in House across from Tree House": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "Who Forest - SS Blueprint in 2nd House near Vacuum Tube Right Side": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "Who Forest - SS Blueprint in 2nd House near Vacuum Tube Left Side": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "Who Forest - SS Blueprint in 2nd House near Vacuum Tube inbetween Blueprints": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "Who Forest - SS Blueprint in House near Vacuum Tube": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "Who Dump - OCD Blueprint inside Middle Pipe": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Slime Shooter", "Rocket Spring"],
        ["Slime Shooter", "Grinch Copter"]
    ],
    "Who Dump - OCD Blueprint inside Right Pipe": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "Who Dump - OCD Blueprint in Vent to Mayor's House": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"]
    ],
    "Who Dump - OCD Blueprint inside Left Pipe": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Slime Shooter", "Rocket Spring"],
        ["Slime Shooter", "Grinch Copter"]
    ],
    "Who Dump - OCD Blueprint near Right Side of Power Plant Wall": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Slime Shooter", "Rocket Spring"],
        ["Slime Shooter", "Grinch Copter"]
    ],
    "Who Dump - OCD Blueprint near Who-Bris' Shack": [
        ["Rotten Egg Launcher", "Rocket Spring"]
    ],
    "Who Dump's Minefield - OCD Blueprint on Left Side of House": [
        []
        # ["Rotten Egg Launcher", "Grinch Copter"],
        # ["Rotten Egg Launcher", "Slime Shooter", "Rocket Spring"]
        # ["Max"]
    ],
    "Who Dump's Minefield - OCD Blueprint on Right Side of Shack": [
        ["Grinch Copter"],
        ["Slime Shooter", "Rocket Spring"]
    ],
    "Who Dump's Minefield - OCD Blueprint inside Guardian's House": [
        []
        # ["Rotten Egg Launcher", "Grinch Copter"],
        # ["Rotten Egg Launcher", "Slime Shooter", "Rocket Spring"]
        # ["Max"]
    ],
    "Who Lake's South Shore - MM Blueprint on Bridge to Scout's Hut": [
        []
    ],
    "Who Lake's South Shore - MM Blueprint across from Tent near Porcupine": [
        []
    ],
    "Who Lake's South Shore - MM Blueprint near Outhouse": [
        []
    ],
    "Who Lake's South Shore - MM Blueprint near Hill Bridge": [
        []
    ],
    "Who Lake's South Shore - MM Blueprint on Scout's Hut Roof": [
        ["Rocket Spring"],
        ["Grinch Copter"]
    ],
    "Who Lake's South Shore - MM Blueprint on Grass Platform": [
        ["Rocket Spring"],
        ["Grinch Copter"]
    ],
    "Who Lake's South Shore - MM Blueprint across Zipline Platform": [
        ["Rocket Spring", "Octopus Climbing Device"],
        ["Grinch Copter"]
    ],
    "Who Lake's South Shore - MM Blueprint behind Summer Beast": [
        ["Rotten Egg Launcher", "Octopus Climbing Device"],
        ["Grinch Copter"]
    ],
    "Who Lake's North Shore - MM Blueprint below Bridge": [
        []
    ],
    "Who Lake's North Shore - MM Blueprint behind Skunk Hut": [
        []
    ],
    "Who Lake's North Shore - MM Blueprint inside Skunk Hut": [
        []
        # ["Max"]
    ],
    "Who Lake's North Shore - MM Blueprint inside House's Fence": [
        []
        # ["Max"]
    ],
    "Who Lake's North Shore - MM Blueprint inside Boulder Box near Bridge": [
        []
    ],
    "Who Lake's North Shore - MM Blueprint inside Boulder Box behind Skunk Hut": [
        []
    ],
    "Who Lake's North Shore - MM Blueprint inside Drill House": [
        []
    ],
    "Who Lake's North Shore - MM Blueprint on Crow Platform near Drill House": [
        []
    ],
    "Whoville's City Hall - GC Blueprint in Safe Room": [
        []
    ],
    "Whoville's City Hall - GC Blueprint in Statue Room": [
        []
    ],
    "Whoville's Clock Tower - GC Blueprint in Bedroom": [
        ["Rocket Spring"]
    #   ["Max", "Rocket Spring"]
    ],
    "Whoville's Clock Tower - GC Blueprint in Bell Room": [
        ["Rocket Spring"]
    ],
    "Who Forest's Ski Resort - GC Blueprint inside Dog's Fence": [
        []
    ],
    "Who Forest's Ski Resort - GC Blueprint in Max Cave": [
        []
        # ["Max"]
    ],
    "Who Forest's Civic Center - GC Blueprint on Left Side in Bat Cave Wall": [
        ["Grinch Copter"],
        ["Octopus Climbing Device", "Rocket Spring"]
    ],
    "Who Forest's Civic Center - GC Blueprint in Frozen Ice": [
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Rotten Egg Launcher", "Octopus Climbing Device", "Rocket Spring"],
        ["Slime Shooter", "Grinch Copter"],
        ["Slime Shooter", "Octopus Climbing Device", "Rocket Spring"]
    ],
    "Who Dump's Power Plant - GC Blueprint in Max Cave": [
        []
        # ["Max"]
    ],
    "Who Dump's Power Plant - GC Blueprint After First Gate": [
        ["Rotten Egg Launcher", "Rocket Spring"],
        ["Grinch Copter"]
    #   ["Max", "Rotten Egg Launcher", "Rocket Spring"]
    ],
    "Who Dump's Generator Building - GC Blueprint on the Highest Platform": [
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Rotten Egg Launcher", "Octopus Climbing Device", "Slime Shooter", "Rocket Spring"]
    ],
    "Who Dump's Generator Building - GC Blueprint at the Entrance after Mission Completion": [
        ["Rotten Egg Launcher", "Grinch Copter"],
        ["Rotten Egg Launcher", "Octopus Climbing Device", "Slime Shooter", "Rocket Spring"]
    ],
    "Who Lake's Submarine World - GC Blueprint Just Below Water Surface": [
        ["Marine Mobile"]
    ],
    "Who Lake's Submarine World - GC Blueprint Underwater": [
        ["Marine Mobile"]
    ],
    "Who Lake's Mayor's Villa - GC Blueprint on Tree Branch": [
        ["Grinch Copter"],
        ["Rotten Egg Launcher", "Rocket Spring"]
    ],
    "Who Lake's Mayor's Villa - GC Blueprint in Pirate's Cave": [
        ["Grinch Copter"],
        ["Rotten Egg Launcher", "Rocket Spring"]
    ],
    "Mount Crumpit's Sleigh Ride - Stealing All Gifts": [
        # ["Exhaust Pipes", "Tires", "Skis", "Twin-End Tuba"]
        ["Rotten Egg Launcher", "Who Forest Vacuum Tube", "Who Dump Vacuum Tube", "Who Lake Vacuum Tube", "Rocket Spring", "Marine Mobile"]
    ],
    "Mount Crumpit's Sleigh Ride - Neutralizing Santa": [
        # ["Exhaust Pipes", "Tires", "Skis", "Twin-End Tuba"]
        ["Rotten Egg Launcher", "Who Forest Vacuum Tube", "Who Dump Vacuum Tube", "Who Lake Vacuum Tube", "Rocket Spring", "Marine Mobile"]
    ],
    "Whoville's Post Office - Heart of Stone": [
        []
    ],
    "Who Forest's Ski Resort - Heart of Stone": [
        []
    ],
    "Who Dump's Minefield - Heart of Stone": [
        ["Grinch Copter"],
        ["Rotten Egg Launcher", "Slime Shooter", "Rocket Spring"]
    ],
    "Who Lake's North Shore - Heart of Stone": [
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
    "Whoville - Exhaust Pipes": [
        ["Rotten Egg Launcher"]
    ],
    "Who Forest - Skis": [
        ["Who Forest Vacuum Tube"]
    ],
    "Who Dump - Tires": [
        ["Who Dump Vacuum Tube", "Rocket Spring", "Rotten Egg Launcher"]
    ],
    "Who Lake's Submarine World - Twin-End Tuba": [
        ["Who Lake Vacuum Tube", "Marine Mobile"]
    ],
    "Who Lake's South Shore - GPS": [
        ["Who Lake Vacuum Tube", "Rotten Egg Launcher"]
    ],
    "Mount Crumpit - 1st Crate Squashed": [
        []
    ],
    "Mount Crumpit - 2nd Crate Squashed": [
        []
    ],
    "Mount Crumpit - 3rd Crate Squashed": [
        []
    ],
    "Mount Crumpit - 4th Crate Squashed": [
        []
    ],
    "Mount Crumpit - 5th Crate Squashed": [
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