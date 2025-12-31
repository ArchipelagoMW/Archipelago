from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

from enum import Enum, auto

from win32comext.mapi.mapitags import pidAttachReadOnlyMin

from BaseClasses import ItemClassification, Location, Region

from . import items

from .strings.region_names import Region as RegionName

from .helpers import PSORamData

if TYPE_CHECKING:
    from .world import PSOWorld


class PSOLocationType(Enum):
    """
    Specifies the types of Locations that can exist as far as Archipelago is concerned
    """

    ITEM = auto()
    EVENT = auto()

# This is the initial implementation for Location Data
# It will likely need to be expanded to include things like memory info
class PSOLocationData(NamedTuple):
    """
    Additional Data for working with Locations in PSO

    :param code: Unique ID used to identify this location to Archipelago
    :param region: Which in-game Region of PSO this item resides
    """

    code: int | None
    region: str
    type: PSOLocationType
    ram_data: PSORamData

LOCATION_TABLE: dict[str, PSOLocationData] = {
    "Tyrell Intro": PSOLocationData(
        1, RegionName.pioneer_2, PSOLocationType.ITEM, PSORamData(0x805127F9, 4)
    ),
    "Irene 1": PSOLocationData(
        2, RegionName.pioneer_2, PSOLocationType.ITEM, PSORamData(0x805127F9, 3)
    ),
    "Scientist 1 - Behind Desk": PSOLocationData(
        3, RegionName.pioneer_2, PSOLocationType.ITEM, PSORamData(0x805127F9, 2)
    ),
    "Scientist 2": PSOLocationData(
        4, RegionName.pioneer_2, PSOLocationType.ITEM, PSORamData(0x805127F9, 1)
    ),
    "Irene 2": PSOLocationData(
        5, RegionName.pioneer_2, PSOLocationType.ITEM, PSORamData(0x805127FA, 7)
    ),
    "Red Ring Rico Message 1": PSOLocationData(
        6, RegionName.pioneer_2, PSOLocationType.ITEM, PSORamData(0x805127FA, 6)
    ),
    "Enter Forest 1": PSOLocationData(
        7, RegionName.forest_1, PSOLocationType.ITEM, PSORamData(0x805127FA, 3)
    ),
    "Defeat Dragon": PSOLocationData(
        8, RegionName.forest_boss, PSOLocationType.ITEM, PSORamData(0x805127FA, 0)
    ),
    "Unlock Caves": PSOLocationData(
        9, RegionName.pioneer_2, PSOLocationType.ITEM, PSORamData(0x805127FB, 7)
    ),
    "Scientist 1 - After Dragon": PSOLocationData(
        10, RegionName.pioneer_2, PSOLocationType.ITEM, PSORamData(0x805127FB, 6)
    ),
    "Defeat De Rol Le": PSOLocationData(
        11, RegionName.caves_boss, PSOLocationType.ITEM, PSORamData(0x805127FC, 7)
    ),
    "Unlock Mines": PSOLocationData(
        12, RegionName.pioneer_2, PSOLocationType.ITEM, PSORamData(0x805127FC, 6)
    ),
    "Defeat Vol Opt": PSOLocationData(
        13, RegionName.mines_boss, PSOLocationType.ITEM, PSORamData(0x805127FD, 5)
    ),
    "Unlock Ruins": PSOLocationData(
        14, RegionName.pioneer_2, PSOLocationType.ITEM, PSORamData(0x805127FE, 7)
    ),

    "Forest 2 Pillar": PSOLocationData(
        20, RegionName.forest_2, PSOLocationType.ITEM, PSORamData(0x805127FD, 3)
    ),
    "Caves 2 Pillar": PSOLocationData(
        21, RegionName.caves_2, PSOLocationType.ITEM, PSORamData(0x805127FD, 2)
    ),
    "Mines 2 Pillar": PSOLocationData(
        22, RegionName.mines_2, PSOLocationType.ITEM, PSORamData(0x805127FD, 1)
    ),

    # "First Forest Drop": PSOLocationData(
    #     23, RegionName.forest_1, PSOLocationType.ITEM, PSORamData(0x801042A4)
    # ),

    # TODO: Get actual data for this check
    "Defeat Dark Falz": PSOLocationData(
        None, RegionName.dark_falz, PSOLocationType.EVENT, PSORamData(0xFFFFFFFF)
    )
}

# Every location must have a unique integer ID associated with it.
# We will have a lookup from location name to ID here that, in world.py, we will import and bind to the world class.
# Even if a location doesn't exist on specific options, it must be present in this lookup.

# We take the location's name and ID and discard the remaining values, since they're not relevant here
def get_location_name_to_id_dict(location_table: dict[str, PSOLocationData]) -> dict[str, int | None]:
    name = location_table.keys()
    code, *_ = zip(*location_table.values())
    return dict(zip(name, code))

LOCATION_NAME_TO_ID: dict[str, int | None] = get_location_name_to_id_dict(LOCATION_TABLE)

# Each Location instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Location class and override the "game" field.
class PSOLocation(Location):
    game = "PSO"

# Helper method but may no longer be needed...
# def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
#     return {location_name: LOCATION_TABLE[location_name].code for location_name in location_names}

def create_all_locations(world: PSOWorld) -> None:
    """
    Iterate through all locations and add them to each region's locations or events as appropriate.

    Events do not have code values (unique IDs) so we use this to sort them out when adding locations
    """
    for location_name, location_value in LOCATION_TABLE.items():
        location_region = world.get_region(LOCATION_TABLE[location_name].region)
        if location_value.code:
            location_region.add_locations({location_name: location_value.code}, PSOLocation)
        else:
            if location_name == "Defeat Dark Falz":
                location_region.add_event(location_name, "Victory", location_type=PSOLocation, item_type=items.PSOItem)
            else:
                location_region.add_event(location_name, location_type=PSOLocation)