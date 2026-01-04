from typing import TYPE_CHECKING
from BaseClasses import Item, ItemClassification, Location, Region
from . import items, locations

if TYPE_CHECKING:
    from . import NoitaWorld


def create_event_item(player: int, name: str) -> Item:
    return items.NoitaItem(name, ItemClassification.progression, None, player)


def create_location(player: int, name: str, region: Region) -> Location:
    return locations.NoitaLocation(player, name, None, region)


def create_locked_location_event(player: int, region: Region, item: str) -> Location:
    new_location = create_location(player, item, region)
    new_location.place_locked_item(create_event_item(player, item))

    region.locations.append(new_location)
    return new_location


def create_all_events(world: "NoitaWorld", created_regions: dict[str, Region]) -> None:
    for region_name, event in event_locks.items():
        region = created_regions[region_name]
        create_locked_location_event(world.player, region, event)

    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)


# Maps region names to event names
event_locks: dict[str, str] = {
    "The Work": "Victory",
    "Mines": "Portal to Holy Mountain 1",
    "Coal Pits": "Portal to Holy Mountain 2",
    "Snowy Depths": "Portal to Holy Mountain 3",
    "Hiisi Base": "Portal to Holy Mountain 4",
    "Underground Jungle": "Portal to Holy Mountain 5",
    "The Vault": "Portal to Holy Mountain 6",
    "Temple of the Art": "Portal to Holy Mountain 7",
}
