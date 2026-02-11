from typing import TYPE_CHECKING
from ..data.Entrances import ENTRANCES, entrance_id_to_region

if TYPE_CHECKING:
    from ..__init__ import PhantomHourglassWorld

MAP_INDEX = {
    0x2b00: 65, 0x12b00: 65,
    0x3000: 82, 0x13000: 82,
    0x2c00: 77, 0x12c00: 77,
    0x2e00: 90, 0x12e00: 90,
    0x2d00: 97, 0x12d00: 97,
    0x2a00: 72, 0x12a00: 72,
    0x2f00: 105, 0x12f00: 105,
    0x2700: 110, 0x12700: 110,
    0x2701: 111, 0x12701: 111,
    0x1c00: 61, 0x11c00: 61,
    0x1c01: 62, 0x11c01: 62,
    0x1c02: 63, 0x11c02: 63,
    0x1c03: 64, 0x11c03: 64,
    0x2900: 78, 0x12900: 78,
    0x2901: 79, 0x12901: 79,
    0x2902: 80, 0x12902: 80,
    0x2903: 81, 0x12903: 81,
    0x2904: 83, 0x12904: 83,
    0x2600: 41, 0x12600: 41,
    0x2500: 42, 0x12500: 42,
    0x2501: 43, 0x12501: 43,
    0x2502: 44, 0x12502: 44,
    0x2503: 45, 0x12503: 45,
    0x2504: 46, 0x12504: 46,
    0x2505: 47, 0x12505: 47,
    0x2506: 48, 0x12506: 48,
    0x2507: 49, 0x12507: 49,
    0x2508: 50, 0x12508: 50,
    0x2509: 51, 0x12509: 51,
    0x250A: 52, 0x1250A: 52,
    0x250B: 53, 0x1250B: 53,
    0x250C: 54, 0x1250C: 54,
    0x250D: 55, 0x1250D: 55,
    0x250E: 56, 0x1250E: 56,
    0x250F: 57, 0x1250F: 57,
    0x2510: 58, 0x12510: 58,
    0x2511: 59, 0x12511: 59,
    0x2512: 60, 0x12512: 60,
    0x1e00: 73, 0x11e00: 73,
    0x1e01: 74, 0x11e01: 74,
    0x1e02: 75, 0x11e02: 75,
    0x1e03: 76, 0x11e03: 76,
    0x2000: 84, 0x12000: 84,
    0x2001: 85, 0x12001: 85,
    0x2002: 86, 0x12002: 86,
    0x2003: 87, 0x12003: 87,
    0x2004: 88, 0x12004: 88,
    0x2005: 89, 0x12005: 89,
    0x200A: 91, 0x1200A: 91,
    0x2800: 125, 0x12800: 125,
    0x1f00: 92, 0x11f00: 92,
    0x1f01: 93, 0x11f01: 93,
    0x1f02: 94, 0x11f02: 94,
    0x1f03: 95, 0x11f03: 95,
    0x1f05: 96, 0x11f05: 96,
    0x1f06: 98, 0x11f06: 98,
    0x1d00: 66, 0x11d00: 66,
    0x1d01: 67, 0x11d01: 67,
    0x1d02: 68, 0x11d02: 68,
    0x1d03: 69, 0x11d03: 69,
    0x1d04: 70, 0x11d04: 70,
    0x1d05: 71, 0x11d05: 71,
    0x2100: 99, 0x12100: 99,
    0x2101: 100, 0x12101: 100,
    0x2102: 101, 0x12102: 101,
    0x2103: 102, 0x12103: 102,
    0x2104: 103, 0x12104: 103,
    0x2105: 104, 0x12105: 104,
    0x2106: 106, 0x12106: 106,
    0x2200: 169, 0x12200: 169,
    0x2201: 170, 0x12201: 170,
    0x2300: 171, 0x12300: 171,
    0x2400: 172, 0x12400: 172,
    0xd0a: 119, 0x10d0a: 119,
    0xd0b: 121, 0x10d0b: 121,
    0xd0c: 122, 0x10d0c: 122,
    0xd14: 120, 0x10d14: 120,
    0x1401: 135, 0x11401: 135,
    0x140a: 136, 0x1140a: 136,
    0x1400: 9, 0x11400: 9,
    0xb0a: 107, 0x10b0a: 107,
    0xb0b: 108, 0x10b0b: 108,
    0xb0c: 112, 0x10b0c: 112,
    0xb0f: 114, 0x10b0f: 114,
    0xb0e: 115, 0x10b0e: 115,
    0xb0d: 116, 0x10b0d: 116,
    0xb10: 117, 0x10b10: 117,
    0xb11: 113, 0x10b11: 113,
    0xb12: 118, 0x10b12: 118,
    0xb13: 109, 0x10b13: 109,
    0x1501: 157, 0x11501: 157,
    0x1502: 158, 0x11502: 158,
    0x1503: 159, 0x11503: 159,
    0x1504: 160, 0x11504: 160,
    0x1505: 161, 0x11505: 161,
    0x1506: 162, 0x11506: 162,
    0x1507: 163, 0x11507: 163,
    0x1508: 164, 0x11508: 164,
    0x1509: 165, 0x11509: 165,
    0x150a: 166, 0x1150a: 166,
    0x1500: 16, 0x11500: 16,
    0xc0a: 130, 0x10c0a: 130,
    0xc0b: 126, 0x10c0b: 126,
    0xc0c: 127, 0x10c0c: 127,
    0xc0d: 128, 0x10c0d: 128,
    0xc0e: 129, 0x10c0e: 129,
    0xc0f: 131, 0x10c0f: 131,
    0x100a: 146, 0x1100a: 146,
    0x100b: 140, 0x1100b: 140,
    0x100c: 141, 0x1100c: 141,
    0x100d: 142, 0x1100d: 142,
    0x100f: 143, 0x1100f: 143,
    0x100e: 144, 0x1100e: 144,
    0x1014: 145, 0x11014: 145,
    0x1701: 132, 0x11701: 132,
    0x1700: 7, 0x11700: 7,
    0x1800: 14, 0x11800: 14,
    0x1900: 18, 0x11900: 18,
    0x1a0a: 137, 0x11a0a: 137,
    0x1a0b: 138, 0x11a0b: 138,
    0x1a00: 10, 0x11a00: 10,
    0x1b00: 13, 0x11b00: 13,
    0x130a: 123, 0x1130a: 123,
    0x130b: 124, 0x1130b: 124,
    0x1300: 5, 0x11300: 5,
    0xf0a: 147, 0x10f0a: 147,
    0xf0b: 148, 0x10f0b: 148,
    0xf0c: 149, 0x10f0c: 149,
    0xf0d: 150, 0x10f0d: 150,
    0xf0e: 151, 0x10f0e: 151,
    0xf0f: 152, 0x10f0f: 152,
    0xf10: 153, 0x10f10: 153,
    0xf11: 154, 0x10f11: 154,
    0xf12: 155, 0x10f12: 155,
    0xf13: 156, 0x10f13: 156,
    0xe0a: 133, 0x10e0a: 133,
    0xe0b: 134, 0x10e0b: 134,
    0x110B: 168, 0x1110B: 168,
    0x120B: 168, 0x1120B: 168,
    0x110a: 167, 0x1110a: 167,
    0x120a: 167, 0x1120a: 167,
    0x160a: 139, 0x1160a: 139,
    0x1600: 11, 0x11600: 11,
    0x800: 179, 0x10800: 179,
    0x700: 176, 0x10700: 176,
    0xa00: 175, 0x10a00: 175,
    0x900: 177, 0x10900: 177,
    0x400: 173, 0x10400: 173,
    0x500: 174, 0x10500: 174,
    0x600: 178, 0x10600: 178,
    0x10D00: 23,
    0x10D01: 24,
    0x10B00: 19,
    0x10B01: 20,
    0x10B02: 21,
    0x10b03: 22,
    0x10c00: 25,
    0x10c01: 26,
    0x11000: 29,
    0x11001: 30,
    0x11002: 31,
    0x11003: 32,
    0x10f00: 33,
    0x10f01: 34,
    0x10f02: 35,
    0x10f03: 36,
    0x10e00: 27,
    0x10e01: 28,
    0x11100: 37,
    0x11101: 38,
    0x11102: 39,
    0x11103: 40,
    0x11200: 37,
    0x11201: 38,
    0x11202: 39,
    0x11203: 40,
    0x0: 0,
    0x1: 2,
    0xD00: 4,
    0xD01: 4,
    0xB00: 3,
    0xB01: 3,
    0xB02: 3,
    0xb03: 3,
    0xc00: 6,
    0xc01: 6,
    0x1000: 12,
    0x1001: 12,
    0x1002: 12,
    0x1003: 12,
    0xf00: 15,
    0xf01: 15,
    0xf02: 15,
    0xf03: 15,
    0xe00: 8,
    0xe01: 8,
    0x1100: 17,
    0x1101: 17,
    0x1102: 17,
    0x1103: 17,
    0x1200: 17,
    0x1201: 17,
    0x1202: 17,
    0x1203: 17,
}

entrance_files = [
    "entrances/overworld_transitions.json",
    "entrances/bosses.json",
    "entrances/caves.json",
    "entrances/dungeons.json",
    "entrances/houses.json",
    "entrances/ports.json",
    "entrances/entrances_overview.json",
    "entrances/sea_overview_entrances.json"]

loc_files = [
    "locations/locations.json",
    "locations/interior_checks.json",
    "locations/overview_houses.json",
    "locations/overview_astrid_houses.json",
    "locations/overview_bosses.json",
    "locations/overview_caves.json",
    "locations/overview_dungeons_full.json",
    "locations/sea_overview.json",
    # "locations/overview_dungeons.json",
    ]

TRACKER_WORLD = {"map_page_folder": "tracker",
                 "map_page_maps": [
                                   "maps/maps.json"
                                   ],
                 "map_page_locations": loc_files + entrance_files,
                 "map_page_settings_key": "{slot}_{team}_UT_MAP",
                 "map_page_index": lambda i: MAP_INDEX.get(i, 0)
                 }

def get_hidden_entrances(world: "PhantomHourglassWorld"):
    import json
    import pkgutil
    pack_name = world.__class__.__module__

    def get_json(files):
        res = []
        for f in files:
            res += json.loads(
                pkgutil.get_data(
                    pack_name,
                    f"/tracker/{f}").decode('utf-8-sig'))
        return res

    entr_data = get_json(entrance_files)
    loc_data = get_json(loc_files)
    active_entrances = [int(i) for i in world.ut_pairings]
    # print(f"active entrances: {[i for i in active_entrances]}")
    entr_hidden: dict[str, list[str]] = {}
    locs_hidden: dict[str, list[int]] = {}
    events_hidden = {}
    map_coord_checks = {}
    # Move event data from locations to entrances
    for loc in loc_data.copy():
        event_names = [s.get("name") for s in loc.get("sections", []) if "EVENT" in s.get("name") or "GOAL" in s.get("name")]
        if event_names:
            entr_data.append(loc)
            loc_data.remove(loc)
    # Handle entrances
    for entrance in entr_data:
        entr_grouping = entrance.get("name")
        entr_names = [s.get("name") for s in entrance.get("sections", [])]
        map_locs = entrance.get("map_locations", [])
        maps = map_locs[0].get("map", "Check Overview")
        for entr_name in entr_names:
            if entr_name not in ENTRANCES:
                print(f"Wrong Entrance in tracker data: {entr_name}")
            elif ENTRANCES[entr_name].id not in active_entrances:
                entr_hidden.setdefault(maps, []).append(entr_name)
            else:
                coords = [(i["x"], i["y"]) for i in map_locs]
                map_coord_checks.setdefault(maps, []).append(coords)
    # Handle locations and coord check entrances
    for loc in loc_data:
        loc_names = [s.get("name") for s in loc.get("sections", [])]
        loc_map_locations = loc.get("map_locations")
        loc_maps = [l["map"] for l in loc_map_locations]
        loc_coords = [(l["x"], l["y"]) for l in loc_map_locations]

        for loc_map in loc_maps:
            if loc_map in map_coord_checks:
                #print(f"Testing {loc_map} coords {loc_coords} in {[i[0] for i in map_coord_checks[loc_map]]}")
                for c in loc_coords:
                    if c in [i[0] for i in map_coord_checks[loc_map]]:
                        loc_ids = []
                        for loc2 in loc_names:
                            if "EVENT" in loc2 or "GOAL" in loc2:
                                entr_hidden.setdefault(loc_map, []).append(loc2)
                            else:
                                loc_ids.append(world.location_name_to_id[loc2])
                        locs_hidden.setdefault(loc_map, [])
                        locs_hidden[loc_map] += loc_ids

    # Special Cases
    if ENTRANCES["Bannan West Hut"].id in active_entrances:
        entr_hidden.setdefault("Bannan Island", []).append("EVENT: Meet Wayfarer")
    if ENTRANCES["Astrid's Stairs"].id in active_entrances:
        locs_hidden.setdefault("Isle of Ember", []).append(87)
        locs_hidden.setdefault("Isle of Ember (West)", []).append(87)
    else:  # Astrid's Stairs is offset by default, needs a manual removal
        entr_hidden.setdefault("Isle of Ember", []).append("Astrid's Stairs")
        entr_hidden.setdefault("Isle of Ember (West)", []).append("Astrid's Stairs")
    if ENTRANCES["Ember West Astrid's House"].id in active_entrances:
        entr_hidden.setdefault("Isle of Ember", []).append("Astrid's Stairs")
        entr_hidden.setdefault("Isle of Ember (West)", []).append("Astrid's Stairs")
    if ENTRANCES["Ruins NW Pyramid"].id in active_entrances:
        entr_hidden.setdefault("Isle of Ruins", []).append("EVENT: Bremeur's Temple Lower Water")
        entr_hidden.setdefault("Isle of Ruins NW", []).append("EVENT: Bremeur's Temple Lower Water")
    if ENTRANCES["Fuzo's Interior Door"].id not in active_entrances:
        entr_hidden.setdefault("Cannon Island", []).append("EVENT: Open Eddo's Door")
        entr_hidden.setdefault("Eddo's Workshop", []).append("EVENT: Open Eddo's Door")
        entr_hidden.setdefault("Check Overview", []).append("EVENT: Open Eddo's Door")
    if ENTRANCES["Cannon Workshop East"].id in active_entrances:
        entr_hidden.setdefault("Cannon Island", []).append("EVENT: Open Eddo's Door")
    # Bosses
    if ENTRANCES["ToF Enter Boss"].id in active_entrances:
        locs_hidden.setdefault("Isle of Ember", []).extend([99, 100])
        locs_hidden.setdefault("Isle of Ember (East)", []).extend([99, 100])
        locs_hidden.setdefault("Temple of Fire 3F", []).extend([99, 100])
        entr_hidden.setdefault("Isle of Ember (East)", []).append("EVENT: Defeat Blaaz")
        entr_hidden.setdefault("Isle of Ember", []).append("EVENT: Defeat Blaaz")
    if ENTRANCES["ToW Enter Boss"].id in active_entrances:
        locs_hidden.setdefault("Isle of Gusts", []).extend([156, 157, 158])
        locs_hidden.setdefault("Isle of Gusts (North)", []).extend([156, 157, 158])
        entr_hidden.setdefault("Isle of Gusts (North)", []).append("EVENT: Defeat Cyclok")
        entr_hidden.setdefault("Isle of Gusts", []).append("EVENT: Defeat Cyclok")
        locs_hidden.setdefault("Temple of Wind 1F", []).extend([156, 157, 158])
    if ENTRANCES["ToC Enter Boss"].id in active_entrances:
        locs_hidden.setdefault("Molida Island", []).extend([129, 130, 131])
        locs_hidden.setdefault("Molida Island (North)", []).extend([129, 130, 131])
        entr_hidden.setdefault("Molida Island", []).append("EVENT: Defeat Crayk")
        entr_hidden.setdefault("Molida Island (North)", []).append("EVENT: Defeat Crayk")
        locs_hidden.setdefault("Temple of Courage 2F", []).extend([129, 130, 131])
    if ENTRANCES["GT Enter Boss"].id in active_entrances:
        locs_hidden.setdefault("Goron Island", []).extend([204, 205, 206])
        locs_hidden.setdefault("Goron Island (NW)", []).extend([204, 205, 206])
        entr_hidden.setdefault("Goron Island", []).append("EVENT: Defeat Dongorongo")
        entr_hidden.setdefault("Goron Island (NW)", []).append("EVENT: Defeat Dongorongo")
        locs_hidden.setdefault("Goron Temple B3", []).extend([204, 205, 206])
    if ENTRANCES["ToI Enter Boss"].id in active_entrances:
        locs_hidden.setdefault("Isle of Frost", []).extend([239, 240, 241])
        locs_hidden.setdefault("Isle of Frost (NE)", []).extend([239, 240, 241])
        entr_hidden.setdefault("Isle of Frost", []).append("EVENT: Defeat Gleeok")
        entr_hidden.setdefault("Isle of Frost (NE)", []).append("EVENT: Defeat Gleeok")
    if ENTRANCES["MT Enter Boss"].id in active_entrances:
        locs_hidden.setdefault("Isle of Ruins", []).extend([266, 267, 268])
        locs_hidden.setdefault("Isle of Ruins NE", []).extend([266, 267, 268])
        entr_hidden.setdefault("Isle of Ruins", []).append("EVENT: Defeat Eox")
        entr_hidden.setdefault("Isle of Ruins NE", []).append("EVENT: Defeat Eox")
        locs_hidden.setdefault("Mutoh's Temple B2", []).extend([266, 267, 268])
    # Dungeon entrances & events
    if ENTRANCES["Ember Enter Temple"].id in active_entrances:
        entr_hidden.setdefault("Isle of Ember (East)", []).append("EVENT: Defeat Blaaz")
        entr_hidden.setdefault("Isle of Ember", []).append("EVENT: Defeat Blaaz")
    if ENTRANCES["Gust Enter Temple"].id in active_entrances:
        entr_hidden.setdefault("Isle of Gusts (North)", []).append("EVENT: Defeat Cyclok")
        entr_hidden.setdefault("Isle of Gusts", []).append("EVENT: Defeat Cyclok")
    if ENTRANCES["Molida North Enter Temple"].id in active_entrances:
        entr_hidden.setdefault("Molida Island", []).append("EVENT: Defeat Crayk")
        entr_hidden.setdefault("Molida Island (North)", []).append("EVENT: Defeat Crayk")
    if ENTRANCES["Goron Enter Temple"].id in active_entrances:
        entr_hidden.setdefault("Goron Island", []).append("EVENT: Defeat Dongorongo")
        entr_hidden.setdefault("Goron Island (NW)", []).append("EVENT: Defeat Dongorongo")
    if ENTRANCES["Frost NE Enter Temple"].id in active_entrances:
        entr_hidden.setdefault("Isle of Frost", []).append("EVENT: Defeat Gleeok")
        entr_hidden.setdefault("Isle of Frost (NE)", []).append("EVENT: Defeat Gleeok")
    if ENTRANCES["Ruins Enter Temple"].id in active_entrances:
        entr_hidden.setdefault("Isle of Ruins", []).append("EVENT: Defeat Eox")
        entr_hidden.setdefault("Isle of Ruins NE", []).append("EVENT: Defeat Eox")


    # for i, v in entr_hidden.items():
    #     print(f"{i}: {v}")
    # for m, locs in locs_hidden.items():
    #     print(f"{m}: {[world.location_id_to_name[loc] for loc in locs]}")
    # for m, locs in events_hidden.items():
    #     print(f"{m}: {locs}")

    return locs_hidden, entr_hidden


