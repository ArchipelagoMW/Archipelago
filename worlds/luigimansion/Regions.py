from typing import Optional, Callable

from BaseClasses import MultiWorld, Entrance
from worlds.generic.Rules import add_rule


def set_ghost_type(multiworld: MultiWorld, ghost_list: dict):
    for region_name in ghost_list:
        ghost_type = multiworld.random.choice(["Fire", "Water", "Ice", "No Element"])
        ghost_list.update({region_name: ghost_type})


def connect(multiworld: MultiWorld, player: int, source: str, target: str,
            rule: Optional[Callable] = None):
    source_region = multiworld.get_region(source, player)
    target_region = multiworld.get_region(target, player)
    name = source + " -> " + target
    connection = Entrance(player, name, source_region)

    if rule is not None:
        add_rule(connection, rule, "and")

    for region_to_type in multiworld.worlds[player].ghost_affected_regions:
        if region_to_type == target_region.name:
            if multiworld.worlds[player].ghost_affected_regions[region_to_type] == "Fire":
                add_rule(connection, lambda state: state.has("Water Element Medal", player))
            elif multiworld.worlds[player].ghost_affected_regions[region_to_type] == "Water":
                add_rule(connection, lambda state: state.has("Ice Element Medal", player))
            elif multiworld.worlds[player].ghost_affected_regions[region_to_type] == "Ice":
                add_rule(connection, lambda state: state.has("Fire Element Medal", player))

    source_region.exits.append(connection)
    connection.connect(target_region)


def connect_regions(multiworld: MultiWorld, player: int):
    connect(multiworld, player, "Menu", "Foyer")
    connect(multiworld, player, "Foyer", "Parlor")
    connect(multiworld, player, "Parlor", "Anteroom",
            lambda state: state.has("Anteroom Key", player))
    connect(multiworld, player, "Anteroom", "Wardrobe")
    connect(multiworld, player, "Wardrobe", "Wardrobe Balcony")
    connect(multiworld, player, "Foyer", "2F Front Hallway",
            lambda state: state.has("Front Hallway Key", player))
    connect(multiworld, player, "Foyer", "1F Hallway",
            lambda state: state.has("Heart Key", player))
    connect(multiworld, player, "2F Front Hallway", "Study")
    connect(multiworld, player, "2F Front Hallway", "Master Bedroom",
            lambda state: state.has("Master Bedroom Key", player))
    connect(multiworld, player, "2F Front Hallway", "Nursery",
            lambda state: state.has("Nursery Key", player))
    connect(multiworld, player, "2F Front Hallway", "Twins' Room",
            lambda state: state.has("Twins Bedroom Key", player))
    connect(multiworld, player, "1F Hallway", "Basement Stairwell")
    connect(multiworld, player, "1F Hallway", "2F Stairwell",
            lambda state: state.has("2F Stairwell Key", player))
    connect(multiworld, player, "1F Hallway", "Courtyard",
            lambda state: state.has("Club Key", player))
    connect(multiworld, player, "1F Hallway", "1F Bathroom")
    connect(multiworld, player, "1F Hallway", "Conservatory",
            lambda state: state.has("Conservatory Key", player))
    connect(multiworld, player, "1F Hallway", "Billiards Room",
            lambda state: state.has("Billiards Key", player))
    connect(multiworld, player, "1F Hallway", "1F Washroom",
            lambda state: state.has("Boo", player, multiworld.worlds[player].options.washroom_boo_count))
    connect(multiworld, player, "1F Hallway", "Ballroom",
            lambda state: state.has("Ballroom Key", player))
    connect(multiworld, player, "1F Hallway", "Dining Room",
            lambda state: state.has("Dining Room Key", player))
    connect(multiworld, player, "1F Hallway", "Laundry Room",
            lambda state: state.has("Laundry Key", player))
    connect(multiworld, player, "1F Hallway", "Fortune-Teller's Room",
            lambda state: state.has("Fortune Teller Key", player))
    connect(multiworld, player, "Courtyard", "Rec Room",
            lambda state: state.has("Rec Room Key", player))
    connect(multiworld, player, "Rec Room", "Courtyard",
            lambda state: state.has("Rec Room Key", player))
    connect(multiworld, player, "Ballroom", "Storage Room",
            lambda state: state.has("Storage Room Key", player))
    connect(multiworld, player, "Dining Room", "Kitchen")
    connect(multiworld, player, "Kitchen", "Boneyard",
            lambda state: state.has("Water Element Medal", player))
    connect(multiworld, player, "Boneyard", "Graveyard",
            lambda state: state.has("Water Element Medal", player))
    connect(multiworld, player, "Billiards Room", "Projection Room")
    connect(multiworld, player, "Fortune-Teller's Room", "Mirror Room",
            lambda state: state.has("Fire Element Medal", player))
    connect(multiworld, player, "Laundry Room", "Butler's Room")
    connect(multiworld, player, "Butler's Room", "Hidden Room")
    connect(multiworld, player, "Courtyard", "The Well")
    connect(multiworld, player, "Rec Room", "2F Stairwell")
    connect(multiworld, player, "2F Stairwell", "Tea Room",
            lambda state: state.has("Water Element Medal", player))
    connect(multiworld, player, "2F Stairwell", "Rec Room")
    connect(multiworld, player, "2F Stairwell", "2F Rear Hallway")
    connect(multiworld, player, "2F Rear Hallway", "2F Bathroom")
    connect(multiworld, player, "2F Rear Hallway", "2F Washroom")
    connect(multiworld, player, "2F Rear Hallway", "Nana's Room")
    connect(multiworld, player, "2F Rear Hallway", "Astral Hall")
    connect(multiworld, player, "2F Rear Hallway", "Sitting Room",
            lambda state: state.has("Sitting Room Key", player))
    connect(multiworld, player, "2F Rear Hallway", "Safari Room",
            lambda state: state.has("Safari Key", player))
    connect(multiworld, player, "Astral Hall", "Observatory",
            lambda state: state.has("Fire Element Medal", player))
    connect(multiworld, player, "Sitting Room", "Guest Room",
            lambda state: state.has("Fire Element Medal", player) and state.has("Water Element Medal", player))
    connect(multiworld, player, "Safari Room", "3F Right Hallway")
    connect(multiworld, player, "3F Right Hallway", "Artist's Studio",
            lambda state: state.has("Art Studio Key", player))
    connect(multiworld, player, "3F Right Hallway", "Balcony",
            lambda state: state.has("Balcony Key", player) and state.has("Boo", player,
                                                                         multiworld.worlds[player].options.balcony_boo_count))
    connect(multiworld, player, "Balcony", "3F Left Hallway",
            lambda state: state.has("Diamond Key", player))
    connect(multiworld, player, "3F Left Hallway", "Armory",
            lambda state: state.has("Armory Key", player))
    connect(multiworld, player, "3F Left Hallway", "Telephone Room")
    connect(multiworld, player, "Telephone Room", "Clockwork Room",
            lambda state: state.has("Clockwork Key", player))
    connect(multiworld, player, "Armory", "Ceramics Studio")
    connect(multiworld, player, "Clockwork Room", "Roof")
    connect(multiworld, player, "Roof", "Sealed Room"),
    connect(multiworld, player, "Basement Stairwell", "Breaker Room")
    connect(multiworld, player, "Basement Stairwell", "Cellar",
            lambda state: state.has("Cellar Key", player))
    connect(multiworld, player, "Cellar", "Basement Hallway")
    connect(multiworld, player, "Basement Hallway", "Cold Storage",
            lambda state: state.has("Cold Storage Key", player))
    connect(multiworld, player, "Basement Hallway", "Pipe Room",
            lambda state: state.has("Pipe Room Key", player))
    connect(multiworld, player, "Basement Hallway", "Secret Altar",
            lambda state: state.has("Spade Key", player) and state.has("Boo", player, multiworld.worlds[player].options.final_boo_count))


REGION_LIST = [
    "Parlor",
    "Foyer",
    "2F Front Hallway",
    "1F Hallway",
    "Anteroom",
    "The Well",
    "Wardrobe",
    "Wardrobe Balcony",
    "Study",
    "Master Bedroom",
    "Nursery",
    "Twins' Room",
    "Laundry Room",
    "Butler's Room",
    "Fortune-Teller's Room",
    "Ballroom",
    "Dining Room",
    "1F Washroom",
    "1F Bathroom",
    "Conservatory",
    "Billiards Room",
    "Basement Stairwell",
    "Projection Room",
    "Kitchen",
    "Boneyard",
    "Graveyard",
    "Butler's Room",
    "Hidden Room",
    "Storage Room",
    "Mirror Room",
    "Rec Room",
    "Courtyard",
    "2F Stairwell",
    "Cellar",
    "Breaker Room",
    "Basement Hallway",
    "Cold Storage",
    "Pipe Room",
    "Secret Altar",
    "Tea Room",
    "Nana's Room",
    "2F Rear Hallway",
    "2F Washroom",
    "2F Bathroom",
    "Astral Hall",
    "Observatory",
    "Sealed Room",
    "Sitting Room",
    "Guest Room",
    "Safari Room",
    "3F Right Hallway",
    "3F Left Hallway",
    "Artist's Studio",
    "Balcony",
    "Armory",
    "Ceramics Studio",
    "Telephone Room",
    "Clockwork Room",
    "Roof"
]

# ROOM_EXITS = []

# THis dict maps exits to entrances located in that exit
#ENTRANCE_ACCESSIBILITY: dict[str, list[str]] = {
#    "Foyer": [
#        "Dungeon Entrance on Dragon Roost Island",
#        ],
