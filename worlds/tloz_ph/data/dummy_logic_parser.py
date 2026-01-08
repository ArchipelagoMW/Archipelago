
import json
from worlds.tloz_ph.Logic import make_overworld_logic
from worlds.tloz_ph.data.Locations import LOCATIONS_DATA
from worlds.tloz_ph.data.Constants import *

# Create logic data, with 2 way connections
one_way_logic_data = make_overworld_logic()
logic_data = one_way_logic_data.copy()
for r1, r2, tw, *args in one_way_logic_data:

    if tw:
        logic_data += [[r2, r1, tw, *args]]


# Create helper maps
areas = ISLANDS + DUNGEON_NAMES + SEA_REGIONS
area_dict = {}
reverse_area_dict = {}
for area in areas:
    area_dict[area] = LOCATION_GROUPS[area]
    for location in LOCATION_GROUPS[area]:
        reverse_area_dict[location] = area

overworld = []
loc_regions = {data["region_id"]: loc_name for loc_name, data in LOCATIONS_DATA.items()}

area_to_location = {}
for loc_name, loc_data in LOCATIONS_DATA.items():
    if loc_name not in ["GOAL: Triforce Door", "GOAL: Beat Bellumbeck"]:
        area = reverse_area_dict[loc_name]

# Items that don't need to use helper functions
logic_map = {}
simple_items = [
    "sword",
    "boomerang",
    "bombs",
    "chus",
    "bow",
    "bombchus",
    "grapple",
    "grappling_hook",
    "hammer",
    "shovel",
    "spade",

    "cannon",
    "cyclone_slate",

]

# Create access rules map
for r1, r2, two_way, logic, *args in logic_data:
    logic_map.setdefault(r2, [])
    if logic:
        reg = "@" + r1.title().replace(" ","")
        arg = ":" + str(args[0]) if args else ""
        if logic in simple_items:
            logic_map[r2].append(reg + ", " + logic + arg)
        else:
            logic_map[r2].append(reg + ", " + "$" + logic + arg)
    else:
        reg = "@" + r2.title().replace(" ", "")
        logic_map[r2].append(reg)

# Adjust access rules map
for k, v in logic_map.items():
    logic_map[k] = set(v)
    logic_map[k] = list(logic_map[k])
    if not v:
        logic_map[k].append("")

# Create final json structure
for area, loc_list in area_dict.items():

    children = []
    for location in loc_list:
        access_rules = logic_map.get(LOCATIONS_DATA[location]["region_id"], [])
        children += [{"name": location,
                      "sections": [{
                          "access_rules": access_rules
                      }]
                      }]
    reg_object = {"name": area,
                  "children": [] + children}

    overworld += [reg_object.copy()]

# print(overworld)
print(json.dumps(overworld, indent=2))
