from typing import Callable

import Utils
from BaseClasses import CollectionState
from worlds.AutoWorld import World
from worlds.generic.Rules import add_rule
from .Items import *

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
        [REL]
    ],
    "WV - City Hall - Modifying The Mayor's Statue": [
        ["Sculpting Tools"]
    ],
    "WV - Clock Tower - Advancing The Countdown-To-Xmas Clock": [
        ["Hammer", RS]
    ],
    "WV - Squashing All Gifts": [
        [GC, SS, REL, "Who Cloak", RS]
    ],
    "WF - Making Xmas Trees Droop": [
        [REL]
    ],
    "WF - Sabotaging Snow Cannon With Glue": [
        ["Glue Bucket", RS],
        ["Glue Bucket", GC]
    ],
    "WF - Putting Beehives In Cabins": [
        [REL, RS],
        [REL, GC]
    ],
    "WF - Ski Resort - Sliming The Mayor's Skis": [
        [SS, REL]
    ],
    "WF - Civic Center - Replacing The Candles On The Cake With Fireworks": [
        [REL, GC],
        [REL, OCD, RS]
    ],
    "WF - Squashing All Gifts": [
        [GC, "Cable Car Access Card", SS, REL],
        [OCD, RS, "Cable Car Access Card", SS, REL]
    ],
    "WD - Stealing Food From Birds": [
        [RS, REL]
    ],
    "WD - Feeding The Computer With Robot Parts": [
        [RS, REL]
    ],
    "WD - Infesting The Mayor's House With Rats": [
        [REL, RS],
        [REL, GC]
    ],
    "WD - Conducting The Stinky Gas To Who-Bris' Shack": [
        [RS, REL]
    ],
    "WD - Minefield - Shaving Who Dump Guardian": [
        ["Scissors", GC],
        ["Scissors", SS, RS]
    ],
    "WD - Generator Building - Short-Circuiting Power-Plant": [
        [REL, GC],
        [REL, OCD, SS, RS]
    ],
    "WD - Squashing All Gifts": [
        [GC, RS, SS, REL],
        [OCD, RS, SS, REL]
    ],
    "WL - South Shore - Putting Thistles In Shorts": [
        [REL, OCD],
        [REL, GC]
    ],
    "WL - South Shore - Sabotaging The Tents": [
        [OCD, RS],
        [GC]
    ],
    "WL - North Shore - Drilling Holes In Canoes": [
        ["Drill"]
        # ["Drill", "Max"]
    ],
    "WL - Submarine World - Modifying The Marine Mobile": [
        []
    ],
    "WL - Mayor's Villa - Hooking The Mayor's Bed To The Motorboat": [
        ["Rope", "Hook", REL, "Scout Clothes"]
    ],
    "WL - Squashing All Gifts": [
        [GC, MM, "Scout Clothes", REL, "Hook", "Rope"],
        [OCD, RS, MM, "Scout Clothes", REL, "Hook", "Rope"]
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
        [REL],
        [GC]
    ],
    "WF - SS BP in Branch Platform Elevated House": [
        [REL, RS],
        [REL, GC]
    ],
    "WF - SS BP in Branch Platform House next to Beast": [
        [REL, RS],
        [REL, GC]
    ],
    "WF - SS BP in House in front of Civic Center Cave": [
        [REL, RS],
        [REL, GC]
    ],
    "WF - SS BP in House next to Tree House": [
        [REL, RS],
        [REL, GC]
    ],
    "WF - SS BP in House across from Tree House": [
        [REL, RS],
        [REL, GC]
    ],
    "WF - SS BP in 2nd House near Vacuum Tube Right Side": [
        [REL, RS],
        [REL, GC]
    ],
    "WF - SS BP in 2nd House near Vacuum Tube Left Side": [
        [REL, RS],
        [REL, GC]
    ],
    "WF - SS BP in 2nd House near Vacuum Tube inbetween Blueprints": [
        [REL, RS],
        [REL, GC]
    ],
    "WF - SS BP in House near Vacuum Tube": [
        [REL, RS],
        [REL, GC]
    ],
    "WD - OCD BP inside Middle Pipe": [
        [REL, RS],
        [REL, GC],
        [SS, RS],
        [SS, GC]
    ],
    "WD - OCD BP inside Right Pipe": [
        [REL, RS],
        [REL, GC]
    ],
    "WD - OCD BP in Vent to Mayor's House": [
        [REL, RS],
        [REL, GC]
    ],
    "WD - OCD BP inside Left Pipe": [
        [REL, RS],
        [REL, GC],
        [SS, RS],
        [SS, GC]
    ],
    "WD - OCD BP near Right Side of Power Plant Wall": [
        [REL, RS],
        [REL, GC],
        [SS, RS],
        [SS, GC]
    ],
    "WD - OCD BP near Who-Bris' Shack": [
        [REL, RS]
    ],
    "WD - Minefield - OCD BP on Left Side of House": [
        []
        # [REL, GC],
        # [REL, SS, RS]
        # ["Max"]
    ],
    "WD - Minefield - OCD BP on Right Side of Shack": [
        [GC],
        [SS, RS]
    ],
    "WD - Minefield - OCD BP inside Guardian's House": [
        []
        # [REL, GC],
        # [REL, SS, RS]
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
        [RS],
        [GC]
    ],
    "WL - South Shore - MM BP on Grass Platform": [
        [RS],
        [GC]
    ],
    "WL - South Shore - MM BP across Zipline Platform": [
        [RS, OCD],
        [GC]
    ],
    "WL - South Shore - MM BP behind Summer Beast": [
        [REL, OCD],
        [GC]
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
        [RS]
    #   ["Max", RS]
    ],
    "WV - Clock Tower - GC BP in Bell Room": [
        [RS]
    ],
    "WF - Ski Resort - GC BP inside Dog's Fence": [
        []
    ],
    "WF - Ski Resort - GC BP in Max Cave": [
        []
        # ["Max"]
    ],
    "WF - Civic Center - GC BP on Left Side in Bat Cave Wall": [
        [GC],
        [OCD, RS]
    ],
    "WF - Civic Center - GC BP in Frozen Ice": [
        [REL, GC],
        [REL, OCD, RS],
        [SS, GC],
        [SS, OCD, RS]
    ],
    "WD - Power Plant - GC BP in Max Cave": [
        []
        # ["Max"]
    ],
    "WD - Power Plant - GC BP After First Gate": [
        [REL, RS],
        [GC]
    #   ["Max", REL, RS]
    ],
    "WD - Generator Building - GC BP on the Highest Platform": [
        [REL, GC],
        [REL, OCD, SS, RS]
    ],
    "WD - Generator Building - GC BP at the Entrance after Mission Completion": [
        [REL, GC],
        [REL, OCD, SS, RS]
    ],
    "WL - Submarine World - GC BP Just Below Water Surface": [
        [MM]
    ],
    "WL - Submarine World - GC BP Underwater": [
        [MM]
    ],
    "WL - Mayor's Villa - GC BP on Tree Branch": [
        [GC],
        [REL, RS]
    ],
    "WL - Mayor's Villa - GC BP in Pirate's Cave": [
        [GC],
        [REL, RS]
    ],
    "MC - Sleigh Ride - Stealing All Gifts": [
        # ["Exhaust Pipes", "Tires", "Skis", "Twin-End Tuba"]
        [REL, "Who Forest Vacuum Tube", "Who Dump Vacuum Tube", "Who Lake Vacuum Tube", RS, MM]
    ],
    "MC - Sleigh Ride - Neutralizing Santa": [
        # ["Exhaust Pipes", "Tires", "Skis", "Twin-End Tuba"]
        [REL, "Who Forest Vacuum Tube", "Who Dump Vacuum Tube", "Who Lake Vacuum Tube", RS, MM]
    ],
    "WV - Post Office - Heart of Stone": [
        []
    ],
    "WF - Ski Resort - Heart of Stone": [
        []
    ],
    "WD - Minefield - Heart of Stone": [
        [GC],
        [REL, SS, RS]
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
        [REL]
    ],
    "WF - Skis": [
        ["Who Forest Vacuum Tube"]
    ],
    "WD - Tires": [
        ["Who Dump Vacuum Tube", RS, REL]
    ],
    "WL - Submarine World - Twin-End Tuba": [
        ["Who Lake Vacuum Tube", MM]
    ],
    "WL - South Shore - GPS": [
        ["Who Lake Vacuum Tube", REL]
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
    #     [REL],
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
        [REL]
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
        [GC],
        [OCD]
    ],
    "Who Dump": [
        ["Who Dump Vacuum Tube"],
        # ["Progressive Vacuum Tube": 2]
    ],
    "Minefield": [
        [REL, RS],
        [REL, GC]
    ],
    "Power Plant": [
        [REL, GC],
        [SS, GC],
        [REL, OCD, SS, RS]
    ],
    "Generator Building": [
        [REL, GC],
        [REL, OCD, SS, RS]
    ],
    "Who Lake": [
        ["Who Lake Vacuum Tube"],
        # ["Progressive Vacuum Tube": 3]
    ],
    "Scout's Hut": [
        [GC],
        [RS]
    ],
    "North Shore": [
        ["Scout Clothes"]
    ],
    "Mayor's Villa": [
        ["Scout Clothes"]
    ],
    "Submarine World": [
        [MM]
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