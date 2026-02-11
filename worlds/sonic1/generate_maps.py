import sys
sys.path.append("../..")

import json
import typing
import constants

maps = []
locations = []
items = []
location_lua = ["LOCATION_MAPPING = {\n"]
item_lua = ["ITEM_MAPPING = {\n"]
map_match_lua = ["AREA_MAPPING= {\n",'  [0] = {"Menu", nil},\n']
map_match_count = 1

maps.append({"name": "menu", "location_size": 22, "location_border_thickness": 1, "img": "images/menu.png"})

special_access_rules = {3141501057: '^$mzSequenceBreakCheck'}

line = 12
for z in [iz for iz in sorted(constants.zones_base[:6], key=lambda iz: iz.playedin)]:
    for stage in range(1,4): # 3 stages for each
        col = 348
        zone = f"{z.zone}{stage}"
        maps.append({
            "name": zone, "location_size": 12, "location_border_thickness": 1, "img": f"images/{zone.upper()}.png"
        })
        loco = {
            "name": zone,
            "chest_unopened_img": "images/monitor_o.png","chest_opened_img": "images/monitor_x.png",
            "children": []
        }
        zl = z.long.replace(" Zone", "")
        map_match_lua += f'  [{map_match_count}] = {{"{zl} Zone", "Act {stage}"}},\n'
        map_match_count += 1
        for m in constants.monitor_by_zone[zone]:
            c = {
                "name": m.name, 
                "map_locations": [
                    {"map": zone, "x": m.x//constants.map_data[zone]["scale"], "y": m.y//constants.map_data[zone]["scale"]},
                    {"map": "menu", "x": col, "y": line},
                ],
                "access_rules": [f"{z.long} Key"],
                "sections": [{"name": m.name}]
            }
            if m.id in special_access_rules:
              c["access_rules"] = [special_access_rules[m.id]]
            loco["children"].append(c)
            col += 24
            location_lua.append(f'  [{m.id}] = {{"{m.name}"}},\n')
        locations.append(loco)
        line += 24

countable= {
  "Special Stage Key": "consumable",
  "Shiny Ring": "consumable",
  "Gold Ring": "consumable",
  "Invincibility": "consumable",
  "Shield": "consumable",
  "Great Speed Shoes": "consumable",
  "Scary Speed Shoes": "consumable",
  "Space intentionally left blank (Junk)": "consumable"
}

for i in constants.item_by_id.values():
    item_lua += f'  [{i.id}] = {{"{i.name.replace(" ","").lower()}", "{countable.get(i.name,"toggle")}"}},\n'
    iname = typing.cast(str,i.name)
    iname.endswith
    if i.name.startswith("Ring"):
       proposed_img = "images/items/ring.png"
    elif i.name.endswith("(Junk)"):
       proposed_img = "images/items/junk.png"
    else:
       proposed_img = f'images/items/{i.name.replace(" ","").lower()}.png'

    items.append({
        "name": i.name,
        "type": countable.get(i.name,"toggle"),
        "img": proposed_img,
        "img_mods": "",
        "codes": f'{i.name.replace(" ","").lower()},{i.name}'
    })

locations.append({"name": "Bosses", "children": [
  {"name": "Green Hill 3 Boss",  "map_locations": [{"map": "menu", "x": 324, "y": 540}],
     "sections": [{"name": "Green Hill 3 Boss", "access_rules":["Green Hill Key"]}]},
  {"name": "Marble Zone 3 Boss", "map_locations": [{"map": "menu", "x": 348, "y": 540}],
     "sections": [{"name": "Marble Zone 3 Boss", "access_rules":["Marble Zone Key"]}]},
  {"name": "Spring Yard 3 Boss", "map_locations": [{"map": "menu", "x": 372, "y": 540}],
     "sections": [{"name": "Spring Yard 3 Boss", "access_rules":["Spring Yard Key"]}]},
  {"name": "Labyrinth 3 Boss",   "map_locations": [{"map": "menu", "x": 396, "y": 540}],
     "sections": [{"name": "Labyrinth 3 Boss", "access_rules":["Labyrinth Key"]}]},
  {"name": "Starlight 3 Boss",   "map_locations": [{"map": "menu", "x": 420, "y": 540}],
     "sections": [{"name": "Starlight 3 Boss", "access_rules":["Starlight Key"]}]},
  {"name": "Final Zone Boss",    "map_locations": [{"map": "menu", "x": 444, "y": 540}],
     "sections": [{"name": "Final Zone Boss", "access_rules":["$fzOpenCheck"]}]},
]})

for b in constants.boss_by_idx.values():
  location_lua.append(f'  [{b.id}] = {{"{b.name}"}},\n')

locations.extend([
  {"name": "Special Stage 1", "access_rules":["$ssKeyCheck|1"], 
    "map_locations": [{"map": "menu", "x": 372, "y": 468}],"sections": [{"name": "Special Stage 1"}]},
  {"name": "Special Stage 2", "access_rules":["$ssKeyCheck|2"],
    "map_locations": [{"map": "menu", "x": 420, "y": 468}],"sections": [{"name": "Special Stage 2"}]},
  {"name": "Special Stage 3", "access_rules":["$ssKeyCheck|3"],
    "map_locations": [{"map": "menu", "x": 468, "y": 468}],"sections": [{"name": "Special Stage 3"}]},
  {"name": "Special Stage 4", "access_rules":["$ssKeyCheck|4"],
    "map_locations": [{"map": "menu", "x": 516, "y": 468}],"sections": [{"name": "Special Stage 4"}]},
  {"name": "Special Stage 5", "access_rules":["$ssKeyCheck|5"],
    "map_locations": [{"map": "menu", "x": 564, "y": 468}],"sections": [{"name": "Special Stage 5"}]},
  {"name": "Special Stage 6", "access_rules":["$ssKeyCheck|6"],
    "map_locations": [{"map": "menu", "x": 612, "y": 468}],"sections": [{"name": "Special Stage 6"}]}
])

for i in range(1,7):
    maps.append({
        "name": f"special_stage_{i}", "location_size": 18, "location_border_thickness": 2, "img": f"images/SpecialStage_{i}.png"
    })
    map_match_lua += f'  [{map_match_count}] = {{"Special Stages", "Special Stage {i}"}},\n'
    map_match_count += 1

for b in constants.special_by_id.values():
  location_lua.append(f'  [{b.id}] = {{"{b.name}"}},\n')
    
maps.append({"name": "fz", "location_size": 18, "location_border_thickness": 2, "img": "images/FZ.png"})
map_match_lua += f'  [{map_match_count}] = {{"Final Zone", nil}},\n'
map_match_count += 1

json.dump(maps, open("tracker/maps/maps.json","w"), indent=4)
json.dump(locations, open("tracker/locations/locations.json","w"), indent=4)
json.dump(items, open("tracker/items/items.json","w"), indent=4)

location_lua += "}"
open("tracker/scripts/autotracking/location_mapping.lua","w").writelines(location_lua)
item_lua += "}"
open("tracker/scripts/autotracking/item_mapping.lua","w").writelines(item_lua)
map_match_lua += "}"
open("tracker/scripts/autotracking/map_mapping.lua","w").writelines(map_match_lua)