"""
Classes and functions related to AP locations for Pokemon Emerald
"""
from typing import TYPE_CHECKING, Dict, Optional, FrozenSet, Iterable

from BaseClasses import Location, Region

from .data import BASE_OFFSET, POKEDEX_OFFSET, data
from .items import offset_item_value

if TYPE_CHECKING:
    from . import PokemonEmeraldWorld


LOCATION_GROUPS = {
    "Badges": {
        "Rustboro Gym - Stone Badge",
        "Dewford Gym - Knuckle Badge",
        "Mauville Gym - Dynamo Badge",
        "Lavaridge Gym - Heat Badge",
        "Petalburg Gym - Balance Badge",
        "Fortree Gym - Feather Badge",
        "Mossdeep Gym - Mind Badge",
        "Sootopolis Gym - Rain Badge",
    },
    "Gym TMs": {
        "Rustboro Gym - TM39 from Roxanne",
        "Dewford Gym - TM08 from Brawly",
        "Mauville Gym - TM34 from Wattson",
        "Lavaridge Gym - TM50 from Flannery",
        "Petalburg Gym - TM42 from Norman",
        "Fortree Gym - TM40 from Winona",
        "Mossdeep Gym - TM04 from Tate and Liza",
        "Sootopolis Gym - TM03 from Juan",
    },
    "Trick House": {
        "Trick House Puzzle 1 - Item",
        "Trick House Puzzle 2 - Item 1",
        "Trick House Puzzle 2 - Item 2",
        "Trick House Puzzle 3 - Item 1",
        "Trick House Puzzle 3 - Item 2",
        "Trick House Puzzle 4 - Item",
        "Trick House Puzzle 6 - Item",
        "Trick House Puzzle 7 - Item",
        "Trick House Puzzle 8 - Item",
        "Trick House Puzzle 1 - Reward",
        "Trick House Puzzle 2 - Reward",
        "Trick House Puzzle 3 - Reward",
        "Trick House Puzzle 4 - Reward",
        "Trick House Puzzle 5 - Reward",
        "Trick House Puzzle 6 - Reward",
        "Trick House Puzzle 7 - Reward",
    }
}


VISITED_EVENT_NAME_TO_ID = {
    "EVENT_VISITED_LITTLEROOT_TOWN": 0,
    "EVENT_VISITED_OLDALE_TOWN": 1,
    "EVENT_VISITED_PETALBURG_CITY": 2,
    "EVENT_VISITED_RUSTBORO_CITY": 3,
    "EVENT_VISITED_DEWFORD_TOWN": 4,
    "EVENT_VISITED_SLATEPORT_CITY": 5,
    "EVENT_VISITED_MAUVILLE_CITY": 6,
    "EVENT_VISITED_VERDANTURF_TOWN": 7,
    "EVENT_VISITED_FALLARBOR_TOWN": 8,
    "EVENT_VISITED_LAVARIDGE_TOWN": 9,
    "EVENT_VISITED_FORTREE_CITY": 10,
    "EVENT_VISITED_LILYCOVE_CITY": 11,
    "EVENT_VISITED_MOSSDEEP_CITY": 12,
    "EVENT_VISITED_SOOTOPOLIS_CITY": 13,
    "EVENT_VISITED_PACIFIDLOG_TOWN": 14,
    "EVENT_VISITED_EVER_GRANDE_CITY": 15,
    "EVENT_VISITED_BATTLE_FRONTIER": 16,
    "EVENT_VISITED_SOUTHERN_ISLAND": 17,
}


class PokemonEmeraldLocation(Location):
    game: str = "Pokemon Emerald"
    item_address: Optional[int]
    default_item_code: Optional[int]
    tags: FrozenSet[str]

    def __init__(
            self,
            player: int,
            name: str,
            address: Optional[int],
            parent: Optional[Region] = None,
            item_address: Optional[int] = None,
            default_item_value: Optional[int] = None,
            tags: FrozenSet[str] = frozenset()) -> None:
        super().__init__(player, name, address, parent)
        self.default_item_code = None if default_item_value is None else offset_item_value(default_item_value)
        self.item_address = item_address
        self.tags = tags


def offset_flag(flag: int) -> int:
    """
    Returns the AP location id (address) for a given flag
    """
    if flag is None:
        return None
    return flag + BASE_OFFSET


def reverse_offset_flag(location_id: int) -> int:
    """
    Returns the flag id for a given AP location id (address)
    """
    if location_id is None:
        return None
    return location_id - BASE_OFFSET


def create_locations_with_tags(world: "PokemonEmeraldWorld", regions: Dict[str, Region], tags: Iterable[str]) -> None:
    """
    Iterates through region data and adds locations to the multiworld if
    those locations include any of the provided tags.
    """
    tags = set(tags)

    for region_name, region_data in data.regions.items():
        region = regions[region_name]
        filtered_locations = [loc for loc in region_data.locations if len(tags & data.locations[loc].tags) > 0]

        for location_name in filtered_locations:
            location_data = data.locations[location_name]

            location_id = offset_flag(location_data.flag)
            if location_data.flag == 0:
                location_id += POKEDEX_OFFSET + int(location_name[15:])

            location = PokemonEmeraldLocation(
                world.player,
                location_data.label,
                location_id,
                region,
                location_data.address,
                location_data.default_item,
                location_data.tags
            )
            region.locations.append(location)


def create_location_label_to_id_map() -> Dict[str, int]:
    """
    Creates a map from location labels to their AP location id (address)
    """
    label_to_id_map: Dict[str, int] = {}
    for region_data in data.regions.values():
        for location_name in region_data.locations:
            location_data = data.locations[location_name]

            if location_data.flag == 0:
                label_to_id_map[location_data.label] = BASE_OFFSET + POKEDEX_OFFSET + int(location_data.name[15:])
            else:
                label_to_id_map[location_data.label] = offset_flag(location_data.flag)

    return label_to_id_map


def set_free_fly(world: "PokemonEmeraldWorld") -> None:
    # Set our free fly location
    # If not enabled, set it to Littleroot Town by default
    fly_location_name = "EVENT_VISITED_LITTLEROOT_TOWN"
    if world.options.free_fly_location:
        fly_location_name = world.random.choice([
            "EVENT_VISITED_SLATEPORT_CITY",
            "EVENT_VISITED_MAUVILLE_CITY",
            "EVENT_VISITED_VERDANTURF_TOWN",
            "EVENT_VISITED_FALLARBOR_TOWN",
            "EVENT_VISITED_LAVARIDGE_TOWN",
            "EVENT_VISITED_FORTREE_CITY",
            "EVENT_VISITED_LILYCOVE_CITY",
            "EVENT_VISITED_MOSSDEEP_CITY",
            "EVENT_VISITED_SOOTOPOLIS_CITY",
            "EVENT_VISITED_EVER_GRANDE_CITY",
        ])

    world.free_fly_location_id = VISITED_EVENT_NAME_TO_ID[fly_location_name]

    free_fly_location_location = world.multiworld.get_location("FREE_FLY_LOCATION", world.player)
    free_fly_location_location.item = None
    free_fly_location_location.place_locked_item(world.create_event(fly_location_name))


def set_legendary_cave_entrances(world: "PokemonEmeraldWorld") -> None:
    # Set Marine Cave and Terra Cave entrances
    terra_cave_location_name = world.random.choice([
        "TERRA_CAVE_ROUTE_114_1",
        "TERRA_CAVE_ROUTE_114_2",
        "TERRA_CAVE_ROUTE_115_1",
        "TERRA_CAVE_ROUTE_115_2",
        "TERRA_CAVE_ROUTE_116_1",
        "TERRA_CAVE_ROUTE_116_2",
        "TERRA_CAVE_ROUTE_118_1",
        "TERRA_CAVE_ROUTE_118_2",
    ])

    terra_cave_location_location = world.multiworld.get_location("TERRA_CAVE_LOCATION", world.player)
    terra_cave_location_location.item = None
    terra_cave_location_location.place_locked_item(world.create_event(terra_cave_location_name))
    
    marine_cave_location_name = world.random.choice([
        "MARINE_CAVE_ROUTE_105_1",
        "MARINE_CAVE_ROUTE_105_2",
        "MARINE_CAVE_ROUTE_125_1",
        "MARINE_CAVE_ROUTE_125_2",
        "MARINE_CAVE_ROUTE_127_1",
        "MARINE_CAVE_ROUTE_127_2",
        "MARINE_CAVE_ROUTE_129_1",
        "MARINE_CAVE_ROUTE_129_2",
    ])

    marine_cave_location_location = world.multiworld.get_location("MARINE_CAVE_LOCATION", world.player)
    marine_cave_location_location.item = None
    marine_cave_location_location.place_locked_item(world.create_event(marine_cave_location_name))
