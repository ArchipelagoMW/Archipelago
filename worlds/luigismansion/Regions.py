from typing import Optional, Callable, TYPE_CHECKING

from . import Rules
if TYPE_CHECKING:
    from . import Rules, LMWorld

vanilla_door_state = {
        34: 1,
        38: 0,
        43: 1,
        41: 1,
        33: 0,
        32: 1,
        31: 0,
        27: 0,
        28: 0,
        3: 0,
        1: 1,
        4: 0,
        5: 1,
        7: 0,
        11: 1,
        14: 0,
        15: 0,
        10: 1,
        17: 0,
        18: 1,
        20: 1,
        16: 0,
        74: 0,
        75: 1,
        23: 1,
        21: 0,
        25: 0,
        24: 1,
        42: 0,
        29: 0,
        30: 1,
        44: 1,
        40: 1,
        45: 1,
        48: 1,
        49: 1,
        47: 1,
        51: 0,
        63: 0,
        52: 1,
        59: 0,
        62: 0,
        55: 1,
        53: 0,
        56: 0,
        50: 1,
        65: 0,
        9: 1,
        71: 0,
        68: 0,
        67: 1,
        69: 0,
        70: 1,
        72: 0
    }

GHOST_TO_ROOM = {
    "Wardrobe": "No Element",
    "Laundry Room": "No Element",
    "Hidden Room": "Ice",  # "Ice",
    "Storage Room": "No Element",
    "Kitchen": "Ice",  # "Ice",
    "1F Bathroom": "No Element",
    "Courtyard": "No Element",
    "Ballroom": "No Element",
    "Tea Room": "No Element",
    "2F Washroom": "Fire",  # "Fire",
    "Projection Room": "No Element",
    "Safari Room": "Water",  # "Water",
    "Cellar": "No Element",
    "Roof": "No Element",
    "Sealed Room": "No Element",
    "Telephone Room": "No Element",
    "Armory": "No Element",
    "Pipe Room": "No Element",
    "Artist's Studio": "No Element",
    "Mirror Room": "No Element",
    "Graveyard": "No Element",
    "Anteroom": "No Element",
    # "Sitting Room": "Fire"  # Fire
}

spawn_locations: dict[str,dict[str, int]] = {
    "Hidden":       {"room_no": 1, "pos_x": 1, "pos_y": 1, "pos_z": 1}, # Hidden
    "Armory":       {"room_no": 48, "pos_x": -2541.662600, "pos_y": 1100.000000, "pos_z": -40.361595}, # Armory
    "Courtyard":    {"room_no": 23, "pos_x": 1, "pos_y": 1, "pos_z": 1}, # Courtyard
    "Roof":         {"room_no": 30, "pos_x": 1, "pos_y": 1, "pos_z": 1}, # Roof
    "Clockwork":    {"room_no": 56, "pos_x": 1, "pos_y": 1, "pos_z": 1}, # Clockwork
    "Foyer":        {"room_no": 2, "pos_x": -7.640748, "pos_y": 0.000000, "pos_z": 145.174300}, # Foyer
    "Rec Room":     {"room_no": 22, "pos_x": 1, "pos_y": 1, "pos_z": 1}, # Rec Room
}

exp_spawns: dict[str,dict[str, int]] = {
    "Telephone":    {"room_no": 50, "pos_x": 1, "pos_y": 1, "pos_z": 1},  # Telephone
    "Laundry":      {"room_no": 5, "pos_x": 1, "pos_y": 1, "pos_z": 1}, # Laundry
}


def set_ghost_type(world: "LMWorld", ghost_list: dict):
    for region_name in ghost_list:
        types = ["Fire", "Water", "Ice", "No Element"]
        weights = [2, 2, 2, 8]
        ghost_type = world.random.choices(types, weights, k=1)[0]
        ghost_list.update({region_name: ghost_type})


def lmconnect(world: "LMWorld", source: str, target: str, key: Optional[str] = None,
            doorid: Optional[int] = None, rule: Optional[Callable] = None):
    player = world.player

    if world.open_doors.get(doorid) == 0:
        extra_rule = lambda state: state.has(key, player)
        if rule is not None:
            rule = lambda state, orig_rule=rule: orig_rule(state) and extra_rule(state)
        else:
            rule = extra_rule

    source_region = world.get_region(source)
    target_region = world.get_region(target)
    source_region.connect(target_region, rule=rule)
    target_region.connect(source_region, rule=rule)


def connect_regions(world: "LMWorld"):
    lmconnect(world, "Menu", "Foyer")
    lmconnect(world, "Foyer", "Parlor", "Parlor Key", 34)
    lmconnect(world, "Parlor", "Anteroom", "Anteroom Key", 38)
    lmconnect(world, "Anteroom", "Wardrobe", "Wardrobe Key", 43)
    lmconnect(world, "Wardrobe", "Wardrobe Balcony", "Wardrobe Balcony Key", 41)
    lmconnect(world, "Foyer", "Family Hallway", "Family Hallway Key", 33)
    lmconnect(world, "Foyer", "1F Hallway", "Heart Key", 3)
    lmconnect(world, "Family Hallway", "Study", "Study Key", 32)
    lmconnect(world, "Family Hallway", "Master Bedroom", "Master Bedroom Key", 31)
    lmconnect(world, "Family Hallway", "Nursery", "Nursery Key", 27)
    lmconnect(world, "Family Hallway", "Twins' Room", "Twins Bedroom Key", 28)
    lmconnect(world, "1F Hallway", "Basement Stairwell", "Basement Stairwell Key", 9)
    lmconnect(world, "1F Hallway", "2F Stairwell", "Lower 2F Stairwell Key", 74)
    lmconnect(world, "1F Hallway", "Courtyard", "Club Key", 42)
    lmconnect(world, "1F Hallway", "1F Bathroom", "1F Bathroom Key", 23)
    lmconnect(world, "1F Hallway", "Conservatory", "Conservatory Key", 21)
    lmconnect(world, "1F Hallway", "Billiards Room", "Billiards Key", 17)
    lmconnect(world, "1F Hallway", "1F Washroom", "1F Washroom Key", 20,
            lambda state, boo_count=world.options.washroom_boo_count: state.has_group("Boo", world.player, boo_count)
                          or state.has("Boo", world.player, boo_count))
    lmconnect(world, "1F Hallway", "Ballroom", "Ballroom Key", 15)
    lmconnect(world, "1F Hallway", "Dining Room", "Dining Room Key", 14)
    lmconnect(world, "1F Hallway", "Laundry Room", "Laundry Room Key", 7)
    lmconnect(world, "1F Hallway", "Fortune-Teller's Room", "Fortune Teller Key", 4)
    lmconnect(world, "Courtyard", "Rec Room", "North Rec Room Key", 25)
    lmconnect(world, "Ballroom", "Storage Room", "Storage Room Key", 16)
    lmconnect(world, "Dining Room", "Kitchen", "Kitchen Key", 11)
    lmconnect(world, "Kitchen", "Boneyard", "Boneyard Key", 10,
            lambda state: Rules.can_fst_water(state, world.player))
    lmconnect(world, "Boneyard", "Graveyard",
            rule=lambda state: Rules.can_fst_water(state, world.player))
    lmconnect(world, "Billiards Room", "Projection Room", "Projection Room Key", 18)
    lmconnect(world, "Fortune-Teller's Room", "Mirror Room", "Mirror Room Key", 5)
    lmconnect(world, "Laundry Room", "Butler's Room", "Butler's Room Key", 1)
    lmconnect(world, "Butler's Room", "Hidden Room")
    lmconnect(world, "Courtyard", "The Well")
    lmconnect(world, "Rec Room", "2F Stairwell", "South Rec Room Key", 24)
    lmconnect(world, "2F Stairwell", "Tea Room", "Tea Room Key", 47,
            lambda state: Rules.can_fst_water(state, world.player))
    lmconnect(world, "2F Stairwell", "2F Rear Hallway", "Upper 2F Stairwell Key", 75)
    lmconnect(world, "2F Rear Hallway", "2F Bathroom", "2F Bathroom Key", 48)
    lmconnect(world, "2F Rear Hallway", "2F Washroom", "2F Washroom Key", 45)
    lmconnect(world, "2F Rear Hallway", "Nana's Room", "Nana's Room Key", 49)
    lmconnect(world, "2F Rear Hallway", "Astral Hall", "Astral Hall Key", 44)
    lmconnect(world, "2F Rear Hallway", "Sitting Room", "Sitting Room Key", 29)
    lmconnect(world, "2F Rear Hallway", "Safari Room", "Safari Room Key", 56)
    lmconnect(world, "Astral Hall", "Observatory", "Observatory Key", 40,
            lambda state: Rules.can_fst_fire(state, world.player))
    lmconnect(world, "Sitting Room", "Guest Room", "Guest Room Key", 30)
    lmconnect(world, "Safari Room", "East Attic Hallway", "East Attic Hallway Key", 55)
    lmconnect(world, "East Attic Hallway", "Artist's Studio", "Artist's Studio Key", 63)
    lmconnect(world, "East Attic Hallway", "Balcony", "Balcony Key", 62,
            lambda state, boo_count=world.options.balcony_boo_count: state.has_group("Boo", world.player, boo_count)
                          or state.has("Boo", world.player, boo_count))
    lmconnect(world, "Balcony", "West Attic Hallway", "Diamond Key", 59)
    lmconnect(world, "West Attic Hallway", "Armory", "Armory Key", 51)
    lmconnect(world, "West Attic Hallway", "Telephone Room", "Telephone Room Key", 52)
    lmconnect(world, "Telephone Room", "Clockwork Room", "Clockwork Key", 53)
    lmconnect(world, "Armory", "Ceramics Studio", "Ceramics Studio Key", 50)
    lmconnect(world, "Clockwork Room", "Roof")
    lmconnect(world, "Roof", "Sealed Room"),
    lmconnect(world, "Basement Stairwell", "Breaker Room", "Breaker Room Key", 71)
    lmconnect(world, "Basement Stairwell", "Cellar", "Cellar Key", 68)
    lmconnect(world, "Cellar", "Basement Hallway", "Basement Hallway Key", 67)
    lmconnect(world, "Basement Hallway", "Cold Storage", "Cold Storage Key", 65)
    lmconnect(world, "Basement Hallway", "Pipe Room", "Pipe Room Key", 69)
    lmconnect(world, "Basement Hallway", "Altar Hallway", "Altar Hallway Key", 70)
    lmconnect(world, "Altar Hallway", "Secret Altar", "Spade Key", 72,
            lambda state, boo_count=world.options.final_boo_count: state.has_group("Boo", world.player, boo_count)
                          or state.has("Boo", world.player, boo_count))


REGION_LIST = {
    35: "Parlor",
    2: "Foyer",
    29: "Family Hallway",
    6: "1F Hallway",
    39: "Anteroom",
    69: "The Well",
    38: "Wardrobe",
    37: "Wardrobe Balcony",
    34: "Study",
    33: "Master Bedroom",
    24: "Nursery",
    25: "Twins' Room",
    5: "Laundry Room",
    0: "Butler's Room",
    3: "Fortune-Teller's Room",
    10: "Ballroom",
    9: "Dining Room",
    17: "1F Washroom",
    20: "1F Bathroom",
    21: "Conservatory",
    12: "Billiards Room",
    65: "Basement Stairwell",
    13: "Projection Room",
    8: "Kitchen",
    11: "Boneyard",
    16: "Graveyard",
    1: "Hidden Room",
    14: "Storage Room",
    4: "Mirror Room",
    22: "Rec Room",
    23: "Courtyard",
    19: "2F Stairwell",
    63: "Cellar",
    67: "Breaker Room",
    62: "Basement Hallway",
    61: "Cold Storage",
    66: "Pipe Room",
    70: "Secret Altar",
    47: "Tea Room",
    46: "Nana's Room",
    26: "2F Rear Hallway",
    42: "2F Washroom",
    45: "2F Bathroom",
    40: "Astral Hall",
    41: "Observatory",
    36: "Sealed Room",
    27: "Sitting Room",
    28: "Guest Room",
    52: "Safari Room",
    51: "East Attic Hallway",
    49: "West Attic Hallway",
    57: "Artist's Studio",
    59: "Balcony",
    48: "Armory",
    55: "Ceramics Studio",
    50: "Telephone Room",
    56: "Clockwork Room",
    60: "Roof",
    68: "Altar Hallway"
}

# ROOM_EXITS = []

# THis dict maps exits to entrances located in that exit
# ENTRANCE_ACCESSIBILITY: dict[str, list[str]] = {
#    "Foyer": [
#        "Dungeon Entrance on Dragon Roost Island",
#        ],
