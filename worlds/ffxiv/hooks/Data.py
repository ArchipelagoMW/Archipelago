import csv
import json
import pkgutil
import re
from typing import Any

# called after the game.json file has been loaded
def after_load_game_file(game_table: dict) -> dict:
    return game_table

HEADER_VALUES = ["", "Name", "ARR", "HW", "STB", "SHB", "EW", "DT"]

TANKS = ["PLD","WAR","DRK","GNB"]
HEALERS = ["WHM","SCH","AST","SGE"]
MELEE = ["MNK","DRG","NIN","SAM","RPR", "VPR"]
CASTER = ["BLM","SMN","RDM","PCT"]
RANGED = ["BRD","MCH","DNC"]
DOH = ["CRP", "BSM", "ARM", "GSM", "LTW", "WVR", "ALC", "CUL"]
DOL = ["MIN", "BTN", "FSH"]

WORLD_BOSSES = [
    "Behold Now Behemoth", "He Taketh It with His Eyes (FATE)", "Steel Reign (FATE)",
    "Long Live the Coeurl (FATE)", "Coeurls Chase Boys (FATE)", "Coeurls Chase Boys Chase Coeurls (FATE)", "Prey Online (FATE)",
    "A Horse Outside (FATE)", "Foxy Lady (FATE)",
    "Nothing Like a Trappin' Life (FATE)", "A Finale Most Formidable (FATE)", "The Head the Tail the Whole Damned Thing (FATE)",
    "Devout Pilgrims vs. Daivadipa (FATE)", "Omicron Recall: Killing Order (FATE)",
    "The Serpentlord Seethes", "Mascot Murder",
    ]

bonus_regions = {}

fate_zones = {
    "Middle La Noscea": [3,3],
    "Lower La Noscea": [3,3],
    "Eastern La Noscea": [30,30],
    "Western La Noscea": [10,10,],
    "Upper La Noscea": [20,20],
    "Outer La Noscea": [30,30],

    "Central Shroud": [4,4],
    "East Shroud": [11,11],
    "South Shroud": [21,21],
    "North Shroud": [3,3],

    "Central Thanalan": [5,5],
    "Western Thanalan": [5,5],
    "Eastern Thanalan": [15,15],
    "Southern Thanalan": [25,26],
    "Northern Thanalan": [49,49],

    "Coerthas Central Highlands": [35,35],
    "Coerthas Western Highlands": [51, 130],

    "Mor Dhona": [44,44],

    "The Sea of Clouds": [51, 130],
    "Azys Lla": [59, 145],

    "The Dravanian Forelands": [52, 130],
    "The Churning Mists": [54, 130],
    "The Dravanian Hinterlands": [58, 145],

    "The Fringes": [60,0],
    "The Peaks": [60,0],
    "The Lochs": [69,0],

    "The Ruby Sea": [62],
    "Yanxia": [64],
    "The Azim Steppe": [65],

    "Lakeland": [70],
    "Kholusia": [70],
    "Il Mheg": [72],
    "Amh Araeng": [76],
    "The Rak'tika Greatwood": [74],
    "The Tempest": [79],

    "Labyrinthos": [80],
    "Thavnair": [80],
    "Garlemald": [82],
    "Mare Lamentorum": [83],
    "Elpis": [86],
    "Ultima Thule": [88],

    "Urqopacha": [90],
    "Kozama'uka": [90],
    "Yak T'el": [94],
    "Shaaloani": [96],
    "Heritage Found": [98],
    "Living Memory": [99],
}

expansion_regex = re.compile(r"^(.*?) \(([^\)]+)\)$")

def get_duty_expansion(category: str) -> tuple[str, str]:
    if category == "PvP":
        return "PvP", "ARR"

    expansion_match = expansion_regex.search(category)
    if expansion_match:
        return expansion_match.group(1), expansion_match.group(2)
    raise ValueError

categorizedLocationNames: dict[tuple[str, str, int], list[str]] = {}  # (dutyType, dutyExpansion, dutyDifficulty) -> [locationName, ...]

def generate_duty_list() -> tuple[list[dict], list[dict]]:
    duty_list = []
    extra_list = []
    difficulties = ["None", "Normal", "Extreme", "Savage", "Endgame"]
    sizes = ["Solo", "Light Party", "Full Party", "Alliance"]
    dutyreader = csv.reader(pkgutil.get_data(__name__, "duties.csv").decode().splitlines(), delimiter=',', quotechar='|')
    _id = 0
    _xid = 30_000
    prev_category = "Dungeon (ARR)"

    for row in dutyreader:
        row = [x.strip() for x in row]
        if row[0] not in HEADER_VALUES:
            requires_str = "{anyClassLevel(" + row[2] + ")}"
            requires_str += (" and |" + row[7] + "|") if  (row[7] != "") else ""
            location = {
                    "name": row[0],
                    "duty_name": row[0],
                    "region": row[4],
                    "category": [row[1], row[4]],
                    "requires": requires_str,
                    "level" : row[2],
                    "party" : sizes.index(row[5]),
                    "diff" : difficulties.index(row[6]),
                    "is_dungeon": "Dungeon" in row[1],
                }
            content_type, expansion = get_duty_expansion(row[1])
            if expansion is not None:
                location["expansion"] = expansion
            if row[1] != prev_category:
                _id += 50
                prev_category = row[1]
                location["id"] = _id
            if row[4] == "Gangos":
                location["category"].append("Bozja")
            duty_list.append(location)
            categorizedLocationNames.setdefault((content_type, expansion, location["diff"]), []).append(row[0])
            if "Dungeon" in row[1]:
                for i in range(1, 10):
                    extra_list.append({
                        "id": _xid,
                        "name": f"{row[0]} {i + 1}",
                        "duty_name": row[0],
                        "region": row[4],
                        "category": [row[1], row[4]],
                        "requires": requires_str,
                        "level" : row[2],
                        "party" : sizes.index(row[5]),
                        "diff" : difficulties.index(row[6]),
                        "is_dungeon": True,
                        "extra_number": i,
                    })
                    _xid += 1

    return duty_list, extra_list

def generate_fate_list():
    fate_list = []

    _id = 8000
    for key in list(fate_zones.keys()):
        level = fate_zones[key][0]
        #ilvl = fate_zones[key][1]
        fate_list.append(create_FATE_location(1,key,level, _id))
        fate_list.append(create_FATE_location(2,key,level))
        fate_list.append(create_FATE_location(3,key,level))
        fate_list.append(create_FATE_location(4,key,level))
        fate_list.append(create_FATE_location(5,key,level))
        fate_list.append(create_FATE_location(6,key,level))
        fate_list.append(create_FATE_location(7,key,level))
        fate_list.append(create_FATE_location(8,key,level))
        fate_list.append(create_FATE_location(9,key,level))
        fate_list.append(create_FATE_location(10,key,level))
        _id += 10

    missing_fatesanity_zones = fate_zones.copy()
    fatereader = csv.reader(pkgutil.get_data(__name__, "fates.csv").decode().splitlines(), delimiter=',', quotechar='"')
    _id = 10_000

    for row in fatereader:
        _id += 1
        row = [x.strip() for x in row]
        if row[0] not in HEADER_VALUES:
            name = row[0]
            level = int(row[1])

            if '(Removed)' in name:
                continue

            if row[2] == 'The Firmament':
                name += " (FETE)"
                fate_list.append(
                    {
                        "name": name,
                        "region": row[2],
                        "category": ["FATEsanity", row[2]],
                        "requires": "{anyCrafterLevel(" + str(max(level - 5, level // 10 * 10)) + ")}",
                        "level" : row[1],
                        "filler": True,
                        "id": _id
                    }
                )
                continue

            if "(FATE)" not in name:
                name += " (FATE)"

            location = {
                    "name": name,
                    "region": row[2],
                    "category": ["FATEsanity", row[2]],
                    "requires": "",
                    "level" : row[1],
                    "id": _id
                }
            if level > 5:
                location["requires"] = "{anyClassLevel(" + str(max(level - 5, level // 10 * 10)) + ")}"
            # if level > 30:
            #     location["filler"] = True

            fate_list.append(location)
            # remove generic FATEs from fate_zones if they exist
            if row[2] in missing_fatesanity_zones:
                missing_fatesanity_zones.pop(row[2])

    if missing_fatesanity_zones:
        # This is hacky, but it lets me slowly scrape the wiki for FATEs without abusing the API
        for key in list(missing_fatesanity_zones.keys()):
            from . import wiki_scraper
            import os
            additional = wiki_scraper.find_fates(key)
            fates_path = os.path.join(os.path.dirname(__file__), 'fates.csv')
            with open(fates_path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for line in additional:
                    writer.writerow(line.split(','))

    return fate_list

def generate_fish_list() -> list[dict]:
    _id = 20_000
    from ..Helpers import load_data_file
    fish = load_data_file("fish.json")
    removed_fish = load_data_file("removed_locations.json")

    locations = []
    for name, data in fish.items():
        requires = f"|5 FSH Levels:{data['lvl'] // 5}|"

        zones = data['zones']
        if not zones:
            _id += 1
            continue
        if len(zones) > 1:
            # cry
            region = name
            bonus_regions[name] = {
                "entrance_requires": {k: '|' + '| OR |'.join(v) + '| OR {YamlDisabled(fishsanity)}' for k, v in zones.items() if v}
            }
        else:
            region = next(iter(zones.keys()))
            if not zones[region]:
                _id += 1
                continue
            requires += f" and |{zones[region][0]}|"

        loc = {
            "name": name,
            "category": ['Fish', "fishsanity"] + list(zones.keys()) + (["Big Fishing"] if data.get('bigfish') else []) + (["Timed Fish"] if data.get('timed') else []),
            "region": region,
            "requires": requires,
            "id": _id,
            "level": data['lvl'],
        }
        if data.get('tribal'):
            if name not in removed_fish:
                del loc['category']
                removed_fish[name] = loc
                with open("removed_locations.json", "w") as f:
                    json.dump(removed_fish, f, indent=2)
            _id += 1
            continue

        locations.append(loc)
        _id += 1

    return locations


def generate_bait_list() -> list[dict]:
    from ..Helpers import load_data_file
    bait = load_data_file("bait.json")
    items = []
    for name, data in bait.items():
        if data.get('mooch'):
            continue
        items.append({
            "name": name,
            "progression": True,
            "category": ['Bait', "fishsanity"]
        })
    return items

# called after the items.json file has been loaded, before any item loading or processing has occurred
# if you need access to the items after processing to add ids, etc., you should use the hooks in World.py
def after_load_item_file(item_table: list) -> list:
    item_table.extend(generate_bait_list())
    classes = TANKS + HEALERS + MELEE + RANGED + CASTER + ["BLU"]
    # crafters
    DOH = [
        "CRP",
        "BSM",
        "ARM",
        "GSM",
        "LTW",
        "WVR",
        "ALC",
        "CUL",
    ]

    # gatherers
    DOL = [
        "MIN",
        "BTN",
        "FSH",
        ]
    max_level = 100
    max_blu = 80

    for job in classes:
        n = max_level / 5
        if job == "BLU":
            n = max_blu / 5

        item_table.append({
            "name": f"5 {job} Levels",
            "category": ["Class Level", "DOW/DOM"],
            "count": n,
            "filler": True,
        })

    for job in DOH:
        item_table.append({
            "name": f"5 {job} Levels",
            "category": ["Class Level", "DOH"],
            "count": max_level / 5,
            "filler": True,
        })
    for job in DOL:
        item_table.append({
            "name": f"5 {job} Levels",
            "category": ["Class Level", "DOL"],
            "count": max_level / 5,
            "filler": True,
        })

    return item_table

# NOTE: Progressive items are not currently supported in Manual. Once they are,
#       this hook will provide the ability to meaningfully change those.
def after_load_progressive_item_file(progressive_item_table: list) -> list:
    return progressive_item_table

# called after the locations.json file has been loaded, before any location loading or processing has occurred
# if you need access to the locations after processing to add ids, etc., you should use the hooks in World.py
def after_load_location_file(location_table: list) -> list:
    #add FATE locations
    duty_locations, extra_duty_locations = generate_duty_list()

    location_table.extend(duty_locations)
    location_table.extend(generate_fate_list())
    location_table.extend(ocean_fishing())
    location_table.extend(generate_fish_list())
    location_table.extend(extra_duty_locations)

    return location_table

# called after the locations.json file has been loaded, before any location loading or processing has occurred
# if you need access to the locations after processing to add ids, etc., you should use the hooks in World.py
def after_load_region_file(region_table: dict) -> dict:
    region_table.update(bonus_regions)
    for r in bonus_regions:
        for e in bonus_regions[r]['entrance_requires']:
            if 'connects_to' not in region_table[e]:
                region_table[e]['connects_to'] = []
                print(f'Warning: {e} missing connects_to')
            region_table[e]['connects_to'].append(r)
    return region_table

def create_FATE_location(number: int, key: str, lvl: int, _id: int = None):
    location = {
            "name": key + ": FATE #" + str(number),
            "region": key,
            "category": ["FATEs", key],
            "requires": "",
            "level" : lvl,
            "fate_number": number,
        }
    if lvl > 0:
        location["requires"] = "{anyClassLevel(" + str(lvl) + ")}"
    if lvl > 30 and number > 2:
        location["filler"] = True
    if _id:
        location["id"] = _id
    return location

def ocean_fishing():
    indigo_route = ["Rhotano Sea", "Bloodbrine Sea", "Rothlyt Sound", "Northern Strait of Merlthor"]
    ruby_route = ["Ruby Sea", "One River"]

    locations = []
    for route in indigo_route:
        locations.append({
            "name": "Ocean Fishing: " + route,
            "region": "Ocean Fishing",
            "category": ["Ocean Fishing", "Indigo Route"],
            "requires": "|5 FSH Levels:1|",
            "level": 1,
            "prehint": True,
        })
    for route in ruby_route:
        locations.append({
            "name": "Ocean Fishing: " + route,
            "region": "Ocean Fishing",
            "category": ["Ocean Fishing", "Ruby Route"],
            "requires": "|5 FSH Levels:12| and |Kugane Access:1|",  # Level 60, because that's the minumum for the Ruby Route
            "level": 60,
            "prehint": True,
        })
    return locations

# called after the categories.json file has been loaded
def after_load_category_file(category_table: dict) -> dict:
    return category_table

# called after the categories.json file has been loaded
def after_load_option_file(option_table: dict) -> dict:
    # option_table["core"] is the dictionary of modification of existing options
    # option_table["user"] is the dictionary of custom options
    return option_table

# called after the meta.json file has been loaded and just before the properties of the apworld are defined. You can use this hook to change what is displayed on the webhost
# for more info check https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md#webworld-class
def after_load_meta_file(meta_table: dict) -> dict:
    return meta_table

# called when an external tool (eg Univeral Tracker) ask for slot data to be read
# use this if you want to restore more data
# return True if you want to trigger a regeneration if you changed anything
def hook_interpret_slot_data(world, player: int, slot_data: dict[str, Any]) -> bool:
    prog_classes = slot_data.get("prog_classes", [])
    if not prog_classes:
        prog_classes = TANKS + HEALERS + MELEE + CASTER + RANGED + DOH + ["FSH"]

    for job in prog_classes:
        world.item_name_to_item["5 " + job + " Levels"]["progression"] = True
    return False
