from BaseClasses import Item, MultiWorld, Region, Location, ItemClassification
from . import Items, Locations


def create_event(player: int, name: str) -> Item:
    return Items.NoitaItem(name, ItemClassification.progression, None, player)


def create_location(player: int, name: str, region: Region) -> Location:
    return Locations.NoitaLocation(player, name, None, region)


def create_locked_location_event(world: MultiWorld, player: int, region_name: str, event_name: str) -> Location:
    region = world.get_region(region_name, player)

    new_location = create_location(player, event_name, region)
    new_location.place_locked_item(create_event(player, event_name))

    region.locations.append(new_location)
    return new_location


def create_victory_events(world: MultiWorld, player: int) -> None:
    # Generate Victory shenanigans (TODO this is temporary)
    create_locked_location_event(world, player, "The Work", "Victory")
    world.completion_condition[player] = lambda state: state.has("Victory", player)


def create_chest_events(world: MultiWorld, player: int) -> None:
    total_locations = world.total_locations[player].value

    # Iterates all our generated chests and makes sure that they are accessible in a specific
    # logical order (?) TODO: Revisit and confirm this
    for i in range(1, 1 + total_locations):
        event_loc = create_locked_location_event(world, player, "Forest", f"Pickup{(i + 1)}")
        event_loc.access_rule = lambda state, i=i: state.can_reach(f"Chest{i}", "Location", player)


def create_all_events(world: MultiWorld, player: int) -> None:
    create_victory_events(world, player)
    create_chest_events(world, player)
