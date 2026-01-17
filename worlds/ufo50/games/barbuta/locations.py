from typing import TYPE_CHECKING, Dict, NamedTuple, Set
from BaseClasses import Region, Location, Item, ItemClassification
from worlds.generic.Rules import add_rule

from ...constants import get_game_base_id

if TYPE_CHECKING:
    from ... import UFO50World


class LocationInfo(NamedTuple):
    id_offset: int
    region_name: str


location_table: Dict[str, LocationInfo] = {
    "Green Skull - R1C1": LocationInfo(0, "Platforms above R4C4"),  # $100
    "Egg Shop - R2C6": LocationInfo(1, "Boss Area"),  # $100 each
    "Upper Shop Candy - R3C1": LocationInfo(2, "Platforms above R4C4"),  # costs $100
    "Upper Shop Umbrella - R3C1": LocationInfo(3, "Platforms above R4C4"),  # costs $50
    "Chest - R3C2": LocationInfo(4, "Platforms above R4C4"),  # Pin chest
    "Bat Altar - R4C1": LocationInfo(5, "Bat Altar"),  # bat noises
    "Coin - R4C4": LocationInfo(6, "Starting Area"),  # $50, breakable block
    "Little Guy Breaks a Wall - R4C7": LocationInfo(7, "R3C7 above Ladders"),  # costs $500
    "Chest - R5C3": LocationInfo(8, "Blood Sword Room"),  # omelette time
    "Chest - R5C5": LocationInfo(9, "Key Room"),  # I love climbing ladders
    "Chest - R5C8": LocationInfo(10, "R6C7 and Nearby"),  # $50
    "Green Skull - R6C2": LocationInfo(11, "Starting Area"),  # $100
    "Lower Shop Umbrella - R6C2": LocationInfo(12, "Starting Area"),  # costs $100
    "Lower Shop Trash - R6C2": LocationInfo(13, "Starting Area"),  # costs $50
    "Lower Shop Pin - R6C2": LocationInfo(14, "Starting Area"),  # costs $200
    "Chest - R6C3 Door": LocationInfo(15, "R7C3 and Nearby"),  # $100
    "Chest - R6C4": LocationInfo(16, "Starting Area"),  # Umbrella chest
    "Chest - R6C5": LocationInfo(17, "Starting Area"),  # $50
    "Chest - R6C6": LocationInfo(18, "R6C7 and Nearby"),  # $100
    "Chest - R7C2": LocationInfo(19, "Starting Area"),  # $50, requires pin
    "Chest - R7C5": LocationInfo(20, "Starting Area"),  # necklace chest
    "Chest - R8C5": LocationInfo(21, "Starting Area"),  # $100, be fast before the ledge breaks
    "Chest - R8C7": LocationInfo(22, "R7C7 and Nearby"),  # $50
    "Wand Trade - R8C7": LocationInfo(23, "Wand Trade Room"),  # probably should just have it give you the check

    "Garden": LocationInfo(997, "Menu"),
    "Gold": LocationInfo(998, "Boss Area"),
    "Cherry": LocationInfo(999, "Boss Area")
}


# this is for filling out location_name_to_id, it should be static regardless of yaml options
def get_locations() -> Dict[str, int]:
    return {f"Barbuta - {name}": data.id_offset + get_game_base_id("Barbuta") for name, data in location_table.items()}


# this should return the location groups for this game, independent of yaml options
# you should include a group that contains all location for this game that is called the same thing as the game
def get_location_groups() -> Dict[str, Set[str]]:
    location_groups: Dict[str, Set[str]] = {"Barbuta": {f"Barbuta - {loc_name}" for loc_name in location_table.keys()}}
    return location_groups


# this is not a required function, but a recommended one -- the world class does not call this function
def create_locations(world: "UFO50World", regions: Dict[str, Region]) -> None:
    for loc_name, loc_data in location_table.items():
        if loc_name == "Cherry" and "Barbuta" not in world.options.cherry_allowed_games:
            break

        if loc_name in ["Gold", "Cherry"] and "Barbuta" in world.goal_games:
            if (loc_name == "Gold" and "Barbuta" not in world.options.cherry_allowed_games) or loc_name == "Cherry":
                loc = Location(world.player, f"Barbuta - {loc_name}", None, regions[loc_data.region_name])
                loc.place_locked_item(Item("Completed Barbuta", ItemClassification.progression, None, world.player))
                add_rule(world.get_location("Completed All Games"), lambda state: state.has("Completed Barbuta", world.player))
                regions[loc_data.region_name].locations.append(loc)
                break

        loc = Location(world.player, f"Barbuta - {loc_name}", get_game_base_id("Barbuta") + loc_data.id_offset,
                       regions[loc_data.region_name])
        regions[loc_data.region_name].locations.append(loc)
