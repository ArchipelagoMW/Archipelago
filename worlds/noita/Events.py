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


def create_victory_events(world: MultiWorld, player: int) -> None:
    # Generate Victory shenanigans (TODO this is temporary)
    create_locked_location_event(world, player, "The Work", "Victory")
    world.completion_condition[player] = lambda state: state.has("Victory", player)


def create_all_events(world: MultiWorld, player: int) -> None:
    create_victory_events(world, player)
