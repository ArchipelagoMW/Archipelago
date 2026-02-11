from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location

from . import items
from .locationData import questLocations, templeLocations, monumentLocations

if TYPE_CHECKING:
    from .world import CatQuestWorld

ALL_LOCATIONS: list[Location] = questLocations + templeLocations + monumentLocations

def create_location_name_to_id() -> dict[str, int]:
    location_id_dict = {}
    current_id = 1

    for location in ALL_LOCATIONS:
        location_id_dict[location["name"]] = current_id
        current_id += 1
    
    return location_id_dict

LOCATION_NAME_TO_ID = create_location_name_to_id()


class CatQuestLocation(Location):
    game = "Cat Quest"

def create_all_locations(world: CatQuestWorld) -> dict[int, str]:
    create_regular_locations(world)

def create_regular_locations(world: CatQuestWorld) -> None:
    Felingard = world.get_region("Felingard")

    included_locations = []

    included_locations.extend(questLocations)

    if world.options.include_temples:
        included_locations.extend(templeLocations)
    
    if world.options.include_monuments:
        included_locations.extend(monumentLocations)

    for loc in included_locations:
        Felingard.locations.append(
            CatQuestLocation(world.player, loc["name"], LOCATION_NAME_TO_ID[loc["name"]], Felingard)
        )
