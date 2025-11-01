from typing import Callable

import Utils
from BaseClasses import CollectionState
from worlds.AutoWorld import World
from worlds.generic.Rules import add_rule
from .Items import grinch_items


# Adds all rules from access_rules_dict to locations
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


def interpret_rule(
    rule_set: list[list[str]],
    player: int,
):
    # If a region/location does not have any items required, make the section(s) return no logic.
    if len(rule_set) < 1:
        return []

    # Otherwise, if a region/location DOES have items required, make the section(s) return list of logic.

    access_list: list[Callable[[CollectionState], bool]] = []
    for item_set in rule_set:
        access_list.append(lambda state, items=tuple(item_set): state.has_all(items, player))

    return access_list

    # Each item in the list is a separate list of rules. Each separate list is just an "OR" condition.


access_rules_dict: dict[str, list[list[str]]] = {
    "Whoville": [
        [
            grinch_items.keys.WHOVILLE,
        ]
    ],
    "Post Office": [
        [
            grinch_items.level_items.WV_WHO_CLOAK,
        ]
    ],
    "City Hall": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
        ]
    ],
    "Clock Tower": [[]],
    "Who Forest": [
        [
            grinch_items.keys.WHO_FOREST,
        ],
    ],
    "Ski Resort": [
        [
            grinch_items.level_items.WF_CABLE_CAR_ACCESS_CARD,
        ]
    ],
    "Civic Center": [
        [
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
        ],
    ],
    "Who Dump": [
        [
            grinch_items.keys.WHO_DUMP,
        ],
    ],
    "Minefield": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
    ],
    "Power Plant": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
    ],
    "Generator Building": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
    ],
    "Who Lake": [
        [
            grinch_items.keys.WHO_LAKE,
        ],
    ],
    "Scout's Hut": [
        [
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.ROCKET_SPRING,
        ],
    ],
    "North Shore": [
        [
            grinch_items.level_items.WL_SCOUT_CLOTHES,
        ]
    ],
    "Mayor's Villa": [
        [
            grinch_items.level_items.WL_SCOUT_CLOTHES,
        ]
    ],
    "Submarine World": [
        [
            grinch_items.gadgets.MARINE_MOBILE,
        ]
    ],
    "Sleigh Room": [
        [
            grinch_items.keys.SLEIGH_ROOM_KEY,
        ]
    ],
    "Spin N' Win": [[]],
    "Dankamania": [],
    "The Copter Race Contest": [[]],
    "Bike Race": [[]],
}


rules_dict: dict[str, list[list[str]]] = {
    # Rules applied to regions first via the access_list, so "First Visit" checks should ALWAYS be empty
    # First Visit Checks (ALWAYS empty)
    "WV - First Visit": [[]],
    "WV - Post Office - First Visit": [[]],
    "WV - City Hall - First Visit": [[]],
    "WV - Clock Tower - First Visit": [[]],
    "WF - First Visit": [[]],
    "WF - Ski Resort - First Visit": [[]],
    "WF - Civic Center - First Visit": [[]],
    "WD - First Visit": [[]],
    "WD - Minefield - First Visit": [[]],
    "WD - Power Plant - First Visit": [[]],
    "WD - Generator Building - First Visit": [[]],
    "WL - South Shore - First Visit": [[]],
    "WL - Submarine World - First Visit": [[]],
    "WL - Scout's Hut - First Visit": [[]],
    "WL - North Shore - First Visit": [[]],
    "WL - Mayor's Villa - First Visit": [[]],
    # Whoville Missions
    "WV - Post Office - Shuffling The Mail": [[]],
    "WV - Smashing Snowmen": [[]],
    "WV - Painting The Mayor's Posters": [
        [
            grinch_items.level_items.WV_PAINT_BUCKET,
        ]
    ],
    "WV - Launching Eggs Into Houses": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
        ]
    ],
    "WV - City Hall - Modifying The Mayor's Statue": [
        [
            grinch_items.level_items.WV_SCULPTING_TOOLS,
        ]
    ],
    "WV - Clock Tower - Advancing The Countdown-To-Xmas Clock": [
        [
            grinch_items.level_items.WV_HAMMER,
            grinch_items.gadgets.ROCKET_SPRING,
        ]
    ],
    "WV - Squashing All Gifts": [
        [
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.level_items.WV_WHO_CLOAK,
            grinch_items.gadgets.ROCKET_SPRING,
        ]
    ],
    # Who Forest Missions
    "WF - Making Xmas Trees Droop": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
        ]
        # "move_rando"
        # [grinch_items.gadgets.ROCKET_EGG_LAUNCHER, BB]
    ],
    "WF - Sabotaging Snow Cannon With Glue": [
        [
            grinch_items.level_items.WF_GLUE_BUCKET,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
        [
            grinch_items.level_items.WF_GLUE_BUCKET,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
    ],
    "WF - Putting Beehives In Cabins": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
    ],
    "WF - Ski Resort - Sliming The Mayor's Skis": [
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
        ]
    ],
    "WF - Civic Center - Replacing The Candles On The Cake With Fireworks": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
        # "move_rando"
        # [grinch_items.gadgets.ROCKET_EGG_LAUNCHER, grinch_items.gadgets.GRINCH_COPTER],
        # [grinch_items.gadgets.ROCKET_EGG_LAUNCHER, grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE, grinch_items.gadgets.ROCKET_SPRING, SN],
        # [grinch_items.gadgets.ROCKET_EGG_LAUNCHER, grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE, grinch_items.gadgets.ROCKET_SPRING, grinch_items.gadgets.SLIME_SHOOTER]
    ],
    "WF - Squashing All Gifts": [
        [
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.level_items.WF_CABLE_CAR_ACCESS_CARD,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
        ],
        [
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.level_items.WF_CABLE_CAR_ACCESS_CARD,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
        ],
    ],
    # Who Dump Missions
    "WD - Stealing Food From Birds": [
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
        ]
        # "move_rando"
        # [grinch_items.gadgets.ROCKET_SPRING, grinch_items.gadgets.ROCKET_EGG_LAUNCHER, PC]
    ],
    "WD - Feeding The Computer With Robot Parts": [
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
        ]
        # "move_rando"
        # [grinch_items.gadgets.ROCKET_SPRING, grinch_items.gadgets.ROCKET_EGG_LAUNCHER, PC]
    ],
    "WD - Infesting The Mayor's House With Rats": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        # "move_rando"
        # [grinch_items.gadgets.ROCKET_EGG_LAUNCHER, grinch_items.gadgets.ROCKET_SPRING, PC],
        # [grinch_items.gadgets.ROCKET_EGG_LAUNCHER, grinch_items.gadgets.GRINCH_COPTER, PC]
    ],
    "WD - Conducting The Stinky Gas To Who-Bris' Shack": [
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
        ]
        # "move_rando"
        # [grinch_items.gadgets.ROCKET_SPRING, grinch_items.gadgets.ROCKET_EGG_LAUNCHER, PC]
    ],
    "WD - Minefield - Shaving Who Dump Guardian": [
        [
            grinch_items.level_items.WL_SCOUT_CLOTHES,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.level_items.WL_SCOUT_CLOTHES,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
        # "move_rando"
        # [grinch_items.level_items.WL_SCOUT_CLOTHES, grinch_items.gadgets.GRINCH_COPTER, SN],
        # [grinch_items.level_items.WL_SCOUT_CLOTHES, grinch_items.gadgets.SLIME_SHOOTER, grinch_items.gadgets.ROCKET_SPRING, SN]
    ],
    "WD - Generator Building - Short-Circuiting Power-Plant": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
    ],
    "WD - Squashing All Gifts": [
        [
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
        ],
        [
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
        ],
    ],
    # Who Lake Missions
    "WL - South Shore - Putting Thistles In Shorts": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
        ],
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
    ],
    "WL - South Shore - Sabotaging The Tents": [
        [
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
        [grinch_items.gadgets.GRINCH_COPTER],
    ],
    "WL - North Shore - Drilling Holes In Canoes": [
        [
            grinch_items.level_items.WL_DRILL,
        ]
    ],
    "WL - Submarine World - Modifying The Marine Mobile": [[]],
    "WL - Mayor's Villa - Hooking The Mayor's Bed To The Motorboat": [
        [
            grinch_items.level_items.WL_ROPE,
            grinch_items.level_items.WL_HOOK,
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.level_items.WL_SCOUT_CLOTHES,
        ]
    ],
    "WL - Squashing All Gifts": [
        [
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.gadgets.MARINE_MOBILE,
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.level_items.WL_SCOUT_CLOTHES,
            grinch_items.level_items.WL_HOOK,
            grinch_items.level_items.WL_ROPE,
        ],
        [
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.gadgets.MARINE_MOBILE,
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.level_items.WL_SCOUT_CLOTHES,
            grinch_items.level_items.WL_HOOK,
            grinch_items.level_items.WL_ROPE,
        ],
    ],
    # Whoville Blueprints
    "WV - Binoculars BP on Post Office Roof": [[]],
    "WV - City Hall - Binoculars BP left side of Library": [[]],
    "WV - City Hall - Binoculars BP front side of Library": [[]],
    "WV - City Hall - Binoculars BP right side of Library": [[]],
    "WV - REL BP left of City Hall": [[]],
    "WV - REL BP left of Clock Tower": [[]],
    "WV - Post Office - REL BP inside Silver Room": [[]],
    "WV - Post Office - REL BP at Entrance Door after Mission Completion": [[]],
    "WV - City Hall - GC BP in Safe Room": [[]],
    "WV - City Hall - GC BP in Statue Room": [[]],
    "WV - Clock Tower - GC BP in Bedroom": [
        [grinch_items.gadgets.ROCKET_SPRING]
        # "move_rando"
        #   [MX, grinch_items.gadgets.ROCKET_SPRING]
    ],
    "WV - Clock Tower - GC BP in Bell Room": [
        [
            grinch_items.gadgets.ROCKET_SPRING,
        ]
    ],
    # Who Forest Blueprints
    "WF - RS BP behind Vacuum Tube": [[]],
    "WF - RS BP in front of 2nd House near Vacuum Tube": [[]],
    "WF - RS BP near Tree House on Ground": [[]],
    "WF - RS BP behind Cable Car House": [[]],
    "WF - RS BP near Who Snowball in Cave": [[]],
    "WF - RS BP on Branch Platform closest to Glue Cannon": [[]],
    "WF - RS BP on Branch Platform Near Beast": [[]],
    "WF - RS BP on Branch Platform Elevated next to House": [[]],
    "WF - RS BP on Tree House": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
        ],
        [
            grinch_items.gadgets.GRINCH_COPTER,
        ],
    ],
    "WF - SS BP in Branch Platform Elevated House": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
    ],
    "WF - SS BP in Branch Platform House next to Beast": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
    ],
    "WF - SS BP in House in front of Civic Center Cave": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
    ],
    "WF - SS BP in House next to Tree House": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
    ],
    "WF - SS BP in House across from Tree House": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
    ],
    "WF - SS BP in 2nd House near Vacuum Tube Right Side": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
    ],
    "WF - SS BP in 2nd House near Vacuum Tube Left Side": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
    ],
    "WF - SS BP in 2nd House near Vacuum Tube inbetween Blueprints": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
    ],
    "WF - SS BP in House near Vacuum Tube": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
    ],
    "WF - Ski Resort - GC BP inside Dog's Fence": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.SLIME_SHOOTER,
        ]
    ],
    "WF - Ski Resort - GC BP in Max Cave": [
        [
            grinch_items.gadgets.SLIME_SHOOTER,
        ]
    ],
    "WF - Civic Center - GC BP on Left Side in Bat Cave Wall": [
        [
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
    ],
    "WF - Civic Center - GC BP in Frozen Ice": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
    ],
    # Who Dump Blueprints
    "WD - OCD BP inside Middle Pipe": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
    ],
    "WD - OCD BP inside Right Pipe": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
    ],
    "WD - OCD BP in Vent to Mayor's House": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
    ],
    "WD - OCD BP inside Left Pipe": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
    ],
    "WD - OCD BP near Right Side of Power Plant Wall": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
    ],
    "WD - OCD BP near Who-Bris' Shack": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
        ]
    ],
    "WD - Minefield - OCD BP on Left Side of House": [
        []
        # "move_rando"
        # [grinch_items.gadgets.ROCKET_EGG_LAUNCHER, grinch_items.gadgets.GRINCH_COPTER],
        # [grinch_items.gadgets.ROCKET_EGG_LAUNCHER, grinch_items.gadgets.SLIME_SHOOTER, grinch_items.gadgets.ROCKET_SPRING]
        # [MX]
    ],
    "WD - Minefield - OCD BP on Right Side of Shack": [
        [
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
    ],
    "WD - Minefield - OCD BP inside Guardian's House": [
        []
        # "move_rando"
        # [grinch_items.gadgets.ROCKET_EGG_LAUNCHER, grinch_items.gadgets.GRINCH_COPTER],
        # [grinch_items.gadgets.ROCKET_EGG_LAUNCHER, grinch_items.gadgets.SLIME_SHOOTER, grinch_items.gadgets.ROCKET_SPRING]
        # [MX]
    ],
    "WD - Power Plant - GC BP in Max Cave": [
        []
        # "move_rando"
        # [MX]
    ],
    "WD - Power Plant - GC BP After First Gate": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
        [
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        # "move_rando"
        #   [MX, grinch_items.gadgets.ROCKET_EGG_LAUNCHER, grinch_items.gadgets.ROCKET_SPRING]
    ],
    "WD - Generator Building - GC BP on the Highest Platform": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
    ],
    "WD - Generator Building - GC BP at the Entrance after Mission Completion": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
    ],
    # Who Lake Blueprints
    "WL - South Shore - MM BP on Bridge to Scout's Hut": [[]],
    "WL - South Shore - MM BP across from Tent near Porcupine": [[]],
    "WL - South Shore - MM BP near Outhouse": [[]],
    "WL - South Shore - MM BP near Hill Bridge": [[]],
    "WL - South Shore - MM BP on Scout's Hut Roof": [
        [
            grinch_items.gadgets.ROCKET_SPRING,
        ],
        [
            grinch_items.gadgets.GRINCH_COPTER,
        ],
    ],
    "WL - South Shore - MM BP on Grass Platform": [
        [
            grinch_items.gadgets.ROCKET_SPRING,
        ],
        [
            grinch_items.gadgets.GRINCH_COPTER,
        ],
    ],
    "WL - South Shore - MM BP across Zipline Platform": [
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
        ],
        [
            grinch_items.gadgets.GRINCH_COPTER,
        ],
    ],
    "WL - South Shore - MM BP behind Summer Beast": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
        ],
        [
            grinch_items.gadgets.GRINCH_COPTER,
        ],
    ],
    "WL - North Shore - MM BP below Bridge": [[]],
    "WL - North Shore - MM BP behind Skunk Hut": [[]],
    "WL - North Shore - MM BP inside Skunk Hut": [
        []
        # "move_rando"
        # [MX]
    ],
    "WL - North Shore - MM BP inside House's Fence": [
        []
        # "move_rando"
        # [MX]
    ],
    "WL - North Shore - MM BP inside Boulder Box near Bridge": [[]],
    "WL - North Shore - MM BP inside Boulder Box behind Skunk Hut": [[]],
    "WL - North Shore - MM BP inside Drill House": [[]],
    "WL - North Shore - MM BP on Crow Platform near Drill House": [[]],
    "WL - Submarine World - GC BP Just Below Water Surface": [[grinch_items.gadgets.MARINE_MOBILE]],
    "WL - Submarine World - GC BP Underwater": [
        [
            grinch_items.gadgets.MARINE_MOBILE,
        ]
    ],
    "WL - Mayor's Villa - GC BP on Tree Branch": [
        [
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
    ],
    "WL - Mayor's Villa - GC BP in Pirate's Cave": [
        [
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
    ],
    # Finale
    "WV - Exhaust Pipes": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.keys.SLEIGH_ROOM_KEY,
        ]
    ],
    "WF - Skis": [
        [
            grinch_items.keys.SLEIGH_ROOM_KEY,
        ]
    ],
    "WD - Tires": [
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.keys.SLEIGH_ROOM_KEY,
        ]
    ],
    "WL - Submarine World - Twin-End Tuba": [
        [
            grinch_items.gadgets.MARINE_MOBILE,
            grinch_items.keys.SLEIGH_ROOM_KEY,
        ]
    ],
    "WL - South Shore - GPS": [
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.keys.SLEIGH_ROOM_KEY,
        ]
    ],
    "MC - Sleigh Ride - Stealing All Gifts": [
        # ["Exhaust Pipes", "Tires", "Skis", "Twin-End Tuba"]
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.keys.WHOVILLE,
            grinch_items.keys.WHO_FOREST,
            grinch_items.keys.WHO_DUMP,
            grinch_items.keys.WHO_LAKE,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.gadgets.MARINE_MOBILE,
        ]
    ],
    "MC - Sleigh Ride - Neutralizing Santa": [
        # ["Exhaust Pipes", "Tires", "Skis", "Twin-End Tuba"]
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.keys.WHOVILLE,
            grinch_items.keys.WHO_FOREST,
            grinch_items.keys.WHO_DUMP,
            grinch_items.keys.WHO_LAKE,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.gadgets.MARINE_MOBILE,
        ]
    ],
    # Hearts of Stone
    "WV - Post Office - Heart of Stone": [[]],
    "WF - Ski Resort - Heart of Stone": [[]],
    "WD - Minefield - Heart of Stone": [
        [
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.ROCKET_EGG_LAUNCHER,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
    ],
    "WL - North Shore - Heart of Stone": [
        []
        # "move_rando"
        # [MX]
    ],
    # Supadows
    "Spin N' Win - Easy": [[]],
    "Spin N' Win - Hard": [[]],
    "Spin N' Win - Real Tough": [[]],
    "Dankamania - Easy - 15 Points": [[]],
    "Dankamania - Hard - 15 Points": [[]],
    "Dankamania - Real Tough - 15 Points": [[]],
    "The Copter Race Contest - Easy": [[]],
    "The Copter Race Contest - Hard": [[]],
    "The Copter Race Contest - Real Tough": [[]],
    "Bike Race - 1st Place": [[]],
    "Bike Race - Top 2": [[]],
    "Bike Race - Top 3": [[]],
    # Intro
    "MC - 1st Crate Squashed": [[]],
    "MC - 2nd Crate Squashed": [[]],
    "MC - 3rd Crate Squashed": [[]],
    "MC - 4th Crate Squashed": [[]],
    "MC - 5th Crate Squashed": [[]],
    # "Green Present": [
    #     []
    # ],
    # "Red Present": [
    #     []
    # ],
    # "Pink Present": [
    #     [grinch_items.gadgets.ROCKET_EGG_LAUNCHER],
    #     [move_rando]
    #     [PC]
    # ],
    # "Yellow Present": [
    #     []
    #     "move_rando"
    #     [PC]
    # ]
}
