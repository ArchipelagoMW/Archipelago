from typing import Dict
from BaseClasses import Item, MultiWorld, Region, Location, ItemClassification
from . import Items, Locations


def create_event(player: int, name: str) -> Item:
    return Items.NoitaItem(name, ItemClassification.progression, None, player)


def create_location(player: int, name: str, region: Region) -> Location:
    return Locations.NoitaLocation(player, name, None, region)


def create_locked_location_event(world: MultiWorld, player: int, region_name: str, item: str) -> Location:
    region = world.get_region(region_name, player)

    new_location = create_location(player, item, region)
    new_location.place_locked_item(create_event(player, item))

    region.locations.append(new_location)
    return new_location


def create_all_events(world: MultiWorld, player: int) -> None:
    for region, event in event_locks.items():
        create_locked_location_event(world, player, region, event)

    world.completion_condition[player] = lambda state: state.has("Victory", player)


event_locks: Dict[str, str] = {
    "The Work": "Victory",
    "Mines": "Portal to Holy Mountain 1",
    "Coal Pits": "Portal to Holy Mountain 2",
    "Snowy Depths": "Portal to Holy Mountain 3",
    "Hiisi Base": "Portal to Holy Mountain 4",
    "Underground Jungle": "Portal to Holy Mountain 5",
    "The Vault": "Portal to Holy Mountain 6",
    "Temple of the Art": "Portal to Holy Mountain 7",
}
