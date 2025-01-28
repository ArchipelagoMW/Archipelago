from typing import Optional, Callable

from BaseClasses import MultiWorld, Entrance
from worlds.generic.Rules import add_rule
from . import Rules
from ..AutoWorld import World

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
    "Sitting Room": "Fire"  # Fire
}


def set_ghost_type(world: World, ghost_list: dict):
    for region_name in ghost_list:
        types = ["Fire", "Water", "Ice", "No Element"]
        weights = [2, 2, 2, 8]
        ghost_type = world.random.choices(types, weights, k=1)[0]
        ghost_list.update({region_name: ghost_type})


def connect(multiworld: MultiWorld, player: int, source: str, target: str, key: Optional[str] = None,
            doorid: Optional[int] = None, rule: Optional[Callable] = None, register: Optional[bool] = False):
    source_region = multiworld.get_region(source, player)
    target_region = multiworld.get_region(target, player)
    name = source + " -> " + target
    connection = Entrance(player, name, source_region)
    if doorid in multiworld.worlds[player].open_doors.keys() and multiworld.worlds[player].open_doors[doorid] == 0:
        add_rule(connection, lambda state: state.has(key, player))

    if rule is not None:
        add_rule(connection, rule, "and")

    # Loop through regions with potential ghost rando. Register indirect connection based on spirit access spots.
    for region_to_type in multiworld.worlds[player].ghost_affected_regions:
        if region_to_type == target_region.name:
            if multiworld.worlds[player].ghost_affected_regions[region_to_type] == "Fire":  # if fire, require water
                add_rule(connection, lambda state: Rules.can_fst_water(state, player), "and")
                for r in Rules.WATER_SPIRIT_SPOT:
                    multiworld.register_indirect_condition(multiworld.get_region(r, player), connection)
            elif multiworld.worlds[player].ghost_affected_regions[region_to_type] == "Water":  # if water, require ice
                add_rule(connection, lambda state: Rules.can_fst_ice(state, player), "and")
                for r in Rules.ICE_SPIRIT_SPOT:
                    multiworld.register_indirect_condition(multiworld.get_region(r, player), connection)
            elif multiworld.worlds[player].ghost_affected_regions[region_to_type] == "Ice":  # if ice, require fire
                add_rule(connection, lambda state: Rules.can_fst_fire(state, player), "and")
                for r in Rules.FIRE_SPIRIT_SPOT:
                    multiworld.register_indirect_condition(multiworld.get_region(r, player), connection)
            else:
                pass

    source_region.exits.append(connection)
    connection.connect(target_region)


def connect_regions(multiworld: MultiWorld, player: int):
    connect(multiworld, player, "Menu", "Foyer")
    connect(multiworld, player, "Foyer", "Parlor", "Parlor Key", 34)
    connect(multiworld, player, "Parlor", "Anteroom", "Anteroom Key", 38)
    connect(multiworld, player, "Anteroom", "Wardrobe", "Wardrobe Key", 43)
    connect(multiworld, player, "Wardrobe", "Wardrobe Balcony", "Wardrobe Balcony Key", 41)
    connect(multiworld, player, "Foyer", "Family Hallway", "Family Hallway Key", 33)
    connect(multiworld, player, "Foyer", "1F Hallway", "Heart Key", 3)
    connect(multiworld, player, "Family Hallway", "Study", "Study Key", 32)
    connect(multiworld, player, "Family Hallway", "Master Bedroom", "Master Bedroom Key", 31)
    connect(multiworld, player, "Family Hallway", "Nursery", "Nursery Key", 27)
    connect(multiworld, player, "Family Hallway", "Twins' Room", "Twins Bedroom Key", 28)
    connect(multiworld, player, "1F Hallway", "Basement Stairwell", "Basement Stairwell Key", 9)
    connect(multiworld, player, "1F Hallway", "2F Stairwell", "Lower 2F Stairwell Key", 74)
    connect(multiworld, player, "1F Hallway", "Courtyard", "Club Key", 42)
    connect(multiworld, player, "1F Hallway", "1F Bathroom", "1F Bathroom Key", 23)
    connect(multiworld, player, "1F Hallway", "Conservatory", "Conservatory Key", 21)
    connect(multiworld, player, "1F Hallway", "Billiards Room", "Billiards Key", 17)
    connect(multiworld, player, "1F Hallway", "1F Washroom", "1F Washroom Key", 20,
            lambda state: state.has_group("Boo", player, multiworld.worlds[player].options.washroom_boo_count)
                          or state.has("Boo", player, multiworld.worlds[player].options.washroom_boo_count))
    connect(multiworld, player, "1F Hallway", "Ballroom", "Ballroom Key", 15)
    connect(multiworld, player, "1F Hallway", "Dining Room", "Dining Room Key", 14)
    connect(multiworld, player, "1F Hallway", "Laundry Room", "Laundry Key", 7)
    connect(multiworld, player, "1F Hallway", "Fortune-Teller's Room", "Fortune Teller Key", 4)
    connect(multiworld, player, "Courtyard", "Rec Room", "North Rec Room Key", 25)
    connect(multiworld, player, "Rec Room", "Courtyard", "North Rec Room Key", 25)
    connect(multiworld, player, "Ballroom", "Storage Room", "Storage Room Key", 16)
    connect(multiworld, player, "Dining Room", "Kitchen", "Kitchen Key", 11)
    connect(multiworld, player, "Kitchen", "Boneyard", "Boneyard Key", 10,
            lambda state: Rules.can_fst_water(state, player))
    connect(multiworld, player, "Boneyard", "Graveyard",
            rule=lambda state: Rules.can_fst_water(state, player))
    connect(multiworld, player, "Billiards Room", "Projection Room", "Projection Room Key", 18)
    connect(multiworld, player, "Fortune-Teller's Room", "Mirror Room", "Mirror Room Key", 5,
            lambda state: Rules.can_fst_fire(state, player))
    connect(multiworld, player, "Laundry Room", "Butler's Room", "Butler's Room Key", 1)
    connect(multiworld, player, "Butler's Room", "Hidden Room")
    connect(multiworld, player, "Courtyard", "The Well")
    connect(multiworld, player, "Rec Room", "2F Stairwell", "South Rec Room Key", 24)
    connect(multiworld, player, "2F Stairwell", "Tea Room", "Tea Room Key", 47,
            lambda state: Rules.can_fst_water(state, player))
    connect(multiworld, player, "2F Stairwell", "Rec Room", "South Rec Room Key", 24)
    connect(multiworld, player, "2F Stairwell", "2F Rear Hallway", "Upper 2F Stairwell Key", 75)
    connect(multiworld, player, "2F Rear Hallway", "2F Bathroom", "2F Bathroom Key", 48)
    connect(multiworld, player, "2F Rear Hallway", "2F Washroom", "2F Washroom Key", 45)
    connect(multiworld, player, "2F Rear Hallway", "Nana's Room", "Nana's Room Key", 49)
    connect(multiworld, player, "2F Rear Hallway", "Astral Hall", "Astral Hall Key", 44)
    connect(multiworld, player, "2F Rear Hallway", "Sitting Room", "Sitting Room Key", 29)
    connect(multiworld, player, "2F Rear Hallway", "Safari Room", "Safari Key", 56)
    connect(multiworld, player, "Astral Hall", "Observatory", "Observatory Key", 40,
            lambda state: Rules.can_fst_fire(state, player))
    connect(multiworld, player, "Sitting Room", "Guest Room", "Guest Room Key", 30,
            lambda state: Rules.can_fst_fire(state, player))
    connect(multiworld, player, "Safari Room", "3F Right Hallway", "3F Right Hallway Key", 55)
    connect(multiworld, player, "3F Right Hallway", "Artist's Studio", "Artist's Studio Key", 63)
    connect(multiworld, player, "3F Right Hallway", "Balcony", "Balcony Key", 62,
            lambda state: state.has_group("Boo", player, multiworld.worlds[player].options.balcony_boo_count)
                          or state.has("Boo", player, multiworld.worlds[player].options.balcony_boo_count))
    connect(multiworld, player, "Balcony", "3F Left Hallway", "Diamond Key", 59,
            lambda state: Rules.can_fst_ice(state, player))
    connect(multiworld, player, "3F Left Hallway", "Armory", "Armory Key", 51)
    connect(multiworld, player, "3F Left Hallway", "Telephone Room", "Telephone Room Key", 52)
    connect(multiworld, player, "Telephone Room", "Clockwork Room", "Clockwork Key", 53)
    connect(multiworld, player, "Armory", "Ceramics Studio", "Ceramics Studio Key", 50)
    connect(multiworld, player, "Clockwork Room", "Roof")
    connect(multiworld, player, "Roof", "Sealed Room"),
    connect(multiworld, player, "Basement Stairwell", "Breaker Room", "Breaker Room Key", 71)
    connect(multiworld, player, "Basement Stairwell", "Cellar", "Cellar Key", 68)
    connect(multiworld, player, "Cellar", "Basement Hallway", "Basement Hallway Key", 67)
    connect(multiworld, player, "Basement Hallway", "Cold Storage", "Cold Storage Key", 65)
    connect(multiworld, player, "Basement Hallway", "Pipe Room", "Pipe Room Key", 69)
    connect(multiworld, player, "Basement Hallway", "Spade Hallway", "Spade Hallway Key", 70)
    connect(multiworld, player, "Spade Hallway", "Secret Altar", "Spade Key", 72,
            lambda state: state.has_group("Boo", player, multiworld.worlds[player].options.final_boo_count)
                          or state.has("Boo", player, multiworld.worlds[player].options.final_boo_count))


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
    51: "3F Right Hallway",
    49: "3F Left Hallway",
    57: "Artist's Studio",
    59: "Balcony",
    48: "Armory",
    55: "Ceramics Studio",
    50: "Telephone Room",
    56: "Clockwork Room",
    60: "Roof",
    68: "Spade Hallway"
}

# ROOM_EXITS = []

# THis dict maps exits to entrances located in that exit
# ENTRANCE_ACCESSIBILITY: dict[str, list[str]] = {
#    "Foyer": [
#        "Dungeon Entrance on Dragon Roost Island",
#        ],
