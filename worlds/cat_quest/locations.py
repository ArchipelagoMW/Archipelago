from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location

from . import items
from .locationData import questLocations

if TYPE_CHECKING:
    from .world import CatQuestWorld


def create_location_name_to_id() -> dict[str, int]:
    location_id_dict = {}
    current_id = 1

    for location in questLocations:
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

    for loc in questLocations:
        Felingard.locations.append(
            CatQuestLocation(world.player, loc["name"], LOCATION_NAME_TO_ID[loc["name"]], Felingard)
    )

    #if world.options.include_temples:
        #for loc in templeLocations:
          #  Felingard.locations.append(
         #       CatQuestLocation(world.player, loc.name, LOCATION_NAME_TO_ID[loc.name], Felingard)
        #)
