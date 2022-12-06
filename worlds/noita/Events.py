from BaseClasses import Item, MultiWorld, Region, Location
from . import Items, Locations


def create_event(player: int, name: str) -> Item:
    return Items.NoitaItem(name, ItemClassification.progression, None, player)


def create_location(player: int, name: str, region: Region) -> Location:
    return Locations.NoitaLocation(player, name, None, region)


def create_victory_events(world: MultiWorld, player: int) -> None:
    # Generate Victory shenanigans (TODO this is temporary)
    the_work_region = world.get_region("The Work", player)
    victory_loc = create_location(player, "Victory", the_work_region)

    victory_loc.place_locked_item(create_event(player, "Victory"))
    world.completion_condition[player] = lambda state: state.has("Victory", player)

    the_work_region.locations.append(victory_loc)


def create_chest_events(world: MultiWorld, player: int) -> None:
    total_locations = world.total_locations[player].value

    # TODO This is a hack for now, we throw all the chest popups in Forest
    forest_region = world.get_region("Forest", player)

    # Iterates all our generated chests and makes sure that they are accessible in a specific
    # logical order (?) TODO: Revisit and confirm this
    for i in range(1, 1 + total_locations):
        pickup_event = create_event(player, f"Pickup{(i + 1)}")

        event_loc = create_location(player, pickup_event.name, forest_region)
        event_loc.place_locked_item(pickup_event)
        event_loc.access_rule(lambda state, i=i: state.can_reach(f"Chest{i}", "Location", player))
        forest_region.locations.append(event_loc)


def create_all_events(world: MultiWorld, player: int) -> None:
    create_victory_events(world, player)
    create_chest_events(world, player)
