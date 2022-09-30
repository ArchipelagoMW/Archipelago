import typing

from BaseClasses import MultiWorld
from Utils import cache_argsless
from .Options import is_option_enabled, get_option_value


def get_always_hint_items(world: MultiWorld, player: int):
    priority = [
        "Boat",
        "Mountain Bottom Floor Final Room Entry (Door)",
        "Caves Mountain Shortcut (Door)",
        "Caves Swamp Shortcut (Door)",
        "Caves Exits to Main Island",
    ]

    if is_option_enabled(world, player, "shuffle_discards"):
        priority.append("Triangles")

    return priority


def get_always_hint_locations(world: MultiWorld, player: int):
    return {
        "Swamp Purple Underwater",
        "Shipwreck Vault Box",
        "Challenge Vault Box",
        "Mountain Bottom Floor Discard",
    }


def get_priority_hint_items(world: MultiWorld, player: int):
    priority = {
        "Negative Shapers",
        "Sound Dots",
        "Colored Dots",
        "Stars + Same Colored Symbol",
        "Swamp Entry (Panel)",
        "Swamp Laser Shortcut (Door)",
    }

    if is_option_enabled(world, player, "shuffle_lasers"):
        lasers = {
            "Symmetry Laser",
            "Desert Laser",
            "Town Laser",
            "Keep Laser",
            "Swamp Laser",
            "Treehouse Laser",
            "Monastery Laser",
            "Jungle Laser",
            "Quarry Laser",
            "Bunker Laser",
            "Shadows Laser",
        }

        if get_option_value(world, player, "doors") >= 2:
            priority.add("Desert Laser")
            lasers.remove("Desert Laser")
            priority.update(world.random.sample(lasers, 2))

        else:
            priority.update(world.random.sample(lasers, 3))

    return priority


def get_priority_hint_locations(world: MultiWorld, player: int):
    return {
        "Town RGB Room Left",
        "Town RGB Room Right",
        "Treehouse Green Bridge 7",
        "Treehouse Green Bridge Discard",
        "Shipwreck Discard",
        "Desert Vault Box",
        "Mountainside Vault Box",
        "Mountainside Discard",
    }


def make_hint_from_item(world: MultiWorld, player: int, item: str):
    location_obj = world.find_item(item, player).item.location
    location_name = location_obj.name
    if location_obj.player != player:
        location_name += " (" + world.get_player_name(location_obj.player) + ")"

    return location_name, item


def make_hint_from_location(world: MultiWorld, player: int, location: str):
    item_obj = world.get_location(location, player).item
    item_name = item_obj.name
    if item_obj.player != player:
        item_name += " (" + world.get_player_name(item_obj.player) + ")"

    return location, item_name


def make_hints(world: MultiWorld, player: int, hint_amount: int):
    hints = list()

    prog_items_in_this_world = {
        item.name for item in world.get_items()
        if item.player == player and item.code and item.advancement
    }
    loc_in_this_world = {
        location.name for location in world.get_locations()
        if location.player == player and not location.event
    }

    always_locations = [
        location for location in get_always_hint_locations(world, player)
        if location in loc_in_this_world
    ]
    always_items = [
        item for item in get_always_hint_items(world, player)
        if item in prog_items_in_this_world
    ]
    priority_locations = [
        location for location in get_priority_hint_locations(world, player)
        if location in loc_in_this_world
    ]
    priority_items = [
        item for item in get_priority_hint_items(world, player)
        if item in prog_items_in_this_world
    ]

    always_hint_pairs = dict()

    for item in always_items:
        hint_pair = make_hint_from_item(world, player, item)
        always_hint_pairs[hint_pair[0]] = (hint_pair[1], True)

    for location in always_locations:
        hint_pair = make_hint_from_location(world, player, location)
        always_hint_pairs[hint_pair[0]] = (hint_pair[1], False)

    priority_hint_pairs = dict()

    for item in priority_items:
        hint_pair = make_hint_from_item(world, player, item)
        priority_hint_pairs[hint_pair[0]] = (hint_pair[1], True)

    for location in priority_locations:
        hint_pair = make_hint_from_location(world, player, location)
        priority_hint_pairs[hint_pair[0]] = (hint_pair[1], False)

    for loc, item in always_hint_pairs.items():
        if item[1]:
            hints.append((item[0], "can be found at", loc))
        else:
            hints.append((loc, "contains", item[0]))

    next_random_hint_is_item = world.random.randint(0, 2)

    prog_items_in_this_world = sorted(list(prog_items_in_this_world))
    locations_in_this_world = sorted(list(loc_in_this_world))

    world.random.shuffle(prog_items_in_this_world)
    world.random.shuffle(locations_in_this_world)

    while len(hints) < hint_amount:
        if priority_hint_pairs:
            loc = world.random.choice(list(priority_hint_pairs.keys()))
            item = priority_hint_pairs[loc]
            del priority_hint_pairs[loc]

            if item[1]:
                hints.append((item[0], "can be found at", loc))
            else:
                hints.append((loc, "contains", item[0]))
            continue

        if next_random_hint_is_item:
            if not prog_items_in_this_world:
                next_random_hint_is_item = not next_random_hint_is_item
                continue

            hint = make_hint_from_item(world, player, prog_items_in_this_world.pop())
            hints.append((hint[1], "can be found at", hint[0]))
        else:
            hint = make_hint_from_location(world, player, locations_in_this_world.pop())
            hints.append((hint[0], "contains", hint[1]))

        next_random_hint_is_item = not next_random_hint_is_item

    return hints
