from logging import debug, error
from typing import TYPE_CHECKING, Dict, List, Set, Tuple

from BaseClasses import CollectionState, Item, Location, LocationProgressType

from .data import static_logic as static_witness_logic
from .data.utils import cast_not_none

if TYPE_CHECKING:
    from . import WitnessWorld


def get_available_early_locations(world: "WitnessWorld") -> List[Location]:
    # Pick an early item to put on Tutorial Gate Open.
    # Done after plando to avoid conflicting with it.
    # Done in fill_hook because multiworld itempool manipulation is not allowed in pre_fill.

    # Prioritize Tutorial locations in a specific order
    tutorial_checks_in_order = [
        "Tutorial Gate Open",
        "Tutorial Back Left",
        "Tutorial Back Right",
        "Tutorial Front Left",
        "Tutorial First Hallway Straight",
        "Tutorial First Hallway Bend",
        "Tutorial Patio Floor",
        "Tutorial First Hallway EP",
        "Tutorial Cloud EP",
        "Tutorial Patio Flowers EP",
    ]
    available_locations = [
        world.get_location(location_name) for location_name in tutorial_checks_in_order
        if location_name in world.reachable_early_locations  # May not actually be sphere 1 (e.g. Obelisk Keys for EPs)
    ]

    # Then, add the rest of sphere 1 in "game order"
    available_locations += sorted(
        (
            world.get_location(location_name) for location_name in world.reachable_early_locations
            if location_name not in tutorial_checks_in_order
        ),
        key=lambda location_object: static_witness_logic.ENTITIES_BY_NAME[location_object.name]["order"]
    )

    return [
        location for location in available_locations
        if not location.item and location.progress_type != LocationProgressType.EXCLUDED
    ]


def get_eligible_items_by_type_in_random_order(world: "WitnessWorld") -> Dict[str, List[str]]:
    eligible_early_items_by_type = world.player_items.get_early_items({item.name for item in world.own_itempool})

    for item_list in eligible_early_items_by_type.values():
        world.random.shuffle(item_list)

    return eligible_early_items_by_type


def grab_own_items_from_itempool(world: "WitnessWorld", itempool: List[Item], ids_to_find: Set[int]) -> List[Item]:
    found_early_items = []

    def keep_or_take_out(item: Item) -> bool:
        if item.code not in ids_to_find:
            return True  # Keep
        ids_to_find.remove(item.code)
        found_early_items.append(item)
        return False  # Take out

    local_player = world.player
    itempool[:] = [item for item in itempool if item.player != local_player or keep_or_take_out(item)]

    return found_early_items


def place_items_onto_locations(world: "WitnessWorld", items: List[Item],
                               locations: List[Location]) -> Tuple[List[Item], List[Item]]:
    fake_state = CollectionState(world.multiworld)

    placed_items = []
    unplaced_items = []

    for item in items:
        location = next(
            (location for location in locations if location.can_fill(fake_state, item, check_access=False)),
            None,
        )
        if location is not None:
            location.place_locked_item(item)
            placed_items.append(item)
            locations.remove(location)
        else:
            unplaced_items.append(item)

    return placed_items, unplaced_items


def place_early_items(world: "WitnessWorld", prog_itempool: List[Item], fill_locations: List[Location]) -> None:
    if not world.options.early_good_items.value:
        return

    # Get a list of good early locations in a determinstic order
    eligible_early_locations = get_available_early_locations(world)
    # Get a list of good early items of each desired item type
    eligible_early_items_by_type = get_eligible_items_by_type_in_random_order(world)

    if not eligible_early_items_by_type:
        return

    while any(eligible_early_items_by_type.values()) and eligible_early_locations:
        # Get one item of each type
        next_findable_items_dict = {
            item_list.pop(): item_type
            for item_type, item_list in eligible_early_items_by_type.items()
            if item_list
        }

        # Get their IDs as a set
        next_findable_item_ids = {world.item_name_to_id[item_name] for item_name in next_findable_items_dict}

        # Grab items from itempool
        found_early_items = grab_own_items_from_itempool(world, prog_itempool, next_findable_item_ids)

        # Bring found items back into Symbol -> Door -> Obelisk Key order
        # The intent is that the Symbol is always on Tutorial Gate Open / generally that the order is predictable
        correct_order = {item_name: i for i, item_name in enumerate(next_findable_items_dict)}
        found_early_items.sort(key=lambda item: correct_order[item.name])

        # Place found early items on eligible early locations.
        placed_items, unplaced_items = place_items_onto_locations(world, found_early_items, eligible_early_locations)

        for item in placed_items:
            debug(f"Placed early good item {item} on early location {item.location}.")
            # Item type is satisfied
            del eligible_early_items_by_type[next_findable_items_dict[item.name]]
            fill_locations.remove(cast_not_none(item.location))
        for item in unplaced_items:
            debug(f"Could not find a suitable placemenet for item {item}.")

    unfilled_types = list(eligible_early_items_by_type)
    if unfilled_types:
        if not eligible_early_locations:
            error(
                f'Could not find a suitable location for "early good items" of types {unfilled_types} in '
                f"{world.player_name}'s world. They are excluded or already contain plandoed items.\n"
            )
        else:
            error(
                f"Could not find any \"early good item\" of types {unfilled_types} in {world.player_name}'s world, "
                "they were all plandoed elsewhere."
            )
