from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import constants
from . import items

if TYPE_CHECKING:
    from .world import TombaWorld

LOCATIONS = [
    constants.VILLAGE_OF_ALL_BEGINNINGS_MAILBOX
]

LOCATION_NAME_TO_ID  = {name: id for
                        id, name in enumerate(LOCATIONS, constants.BASE_ID)}


class TombaLocation(Location):
    game = constants.GAME


def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: TombaWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: TombaWorld) -> None:
    village_of_all_beginnings = world.get_region(constants.VILLAGE_OF_ALL_BEGINNINGS)

    village_of_all_beginnings_locations = get_location_names_with_ids(
        [
            constants.VILLAGE_OF_ALL_BEGINNINGS_MAILBOX,
            constants.VILLAGE_OF_ALL_BEGINNINGS_FOG
        ]
    )

    village_of_all_beginnings.add_locations(village_of_all_beginnings_locations, TombaLocation)


def create_events(world: TombaWorld) -> None:
    village_of_all_beginnings = world.get_region(constants.VILLAGE_OF_ALL_BEGINNINGS)

    village_of_all_beginnings.add_event(
        constants.FOG_DISSIPATED, constants.VICTORY, location_type=TombaLocation, item_type=items.TombaItem
    )