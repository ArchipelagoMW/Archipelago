import collections
import logging
import typing

from BaseClasses import LocationProgressType, MultiWorld, Location, Region, Entrance

if typing.TYPE_CHECKING:
    import BaseClasses

    CollectionRule = typing.Callable[[BaseClasses.CollectionState], bool]
    ItemRule = typing.Callable[[BaseClasses.Item], bool]
else:
    CollectionRule = typing.Callable[[object], bool]
    ItemRule = typing.Callable[[object], bool]


def item_locality_needed(multiworld: MultiWorld) -> bool:
    for player in multiworld.player_ids:
        if multiworld.worlds[player].options.local_items.value:
            return True
        if multiworld.worlds[player].options.non_local_items.value:
            return True

    # Group
    for group_id, group in multiworld.groups.items():
        if set(multiworld.player_ids) == set(group["players"]):
            continue
        if group["local_items"]:
            return True
        if group["non_local_items"]:
            return True
    return False


def location_locality_needed(multiworld: MultiWorld) -> bool:
    """Returns whether the multiworld sets any location-specific locality settings."""
    for player in multiworld.player_ids:
        if multiworld.worlds[player].options.local_locations.value:
            return True
        if multiworld.worlds[player].options.non_local_locations.value:
            return True
    return False


def locality_rules(multiworld: MultiWorld):
    if item_locality_needed(multiworld):

        forbid_data: typing.Dict[int, typing.Dict[int, typing.Set[str]]] = \
            collections.defaultdict(lambda: collections.defaultdict(set))

        def forbid(sender: int, receiver: int, items: typing.Set[str]):
            forbid_data[sender][receiver].update(items)

        for receiving_player in multiworld.player_ids:
            local_items: typing.Set[str] = multiworld.worlds[receiving_player].options.local_items.value
            if local_items:
                for sending_player in multiworld.player_ids:
                    if receiving_player != sending_player:
                        forbid(sending_player, receiving_player, local_items)
            non_local_items: typing.Set[str] = multiworld.worlds[receiving_player].options.non_local_items.value
            if non_local_items:
                forbid(receiving_player, receiving_player, non_local_items)

        # Group
        for receiving_group_id, receiving_group in multiworld.groups.items():
            if set(multiworld.player_ids) == set(receiving_group["players"]):
                continue
            if receiving_group["local_items"]:
                for sending_player in multiworld.player_ids:
                    if sending_player not in receiving_group["players"]:
                        forbid(sending_player, receiving_group_id, receiving_group["local_items"])
            if receiving_group["non_local_items"]:
                for sending_player in multiworld.player_ids:
                    if sending_player in receiving_group["players"]:
                        forbid(sending_player, receiving_group_id, receiving_group["non_local_items"])

        # create fewer lambda's to save memory and cache misses
        func_cache = {}
        for location in multiworld.get_locations():
            if (location.player, location.item_rule) in func_cache:
                location.item_rule = func_cache[location.player, location.item_rule]
            # empty rule that just returns True, overwrite
            elif location.item_rule is Location.item_rule:
                func_cache[location.player, location.item_rule] = location.item_rule = \
                    lambda i, sending_blockers = forbid_data[location.player], \
                                            old_rule = location.item_rule: \
                    i.name not in sending_blockers[i.player]
            # special rule, needs to also be fulfilled.
            else:
                func_cache[location.player, location.item_rule] = location.item_rule = \
                    lambda i, sending_blockers = forbid_data[location.player], \
                                            old_rule = location.item_rule: \
                    i.name not in sending_blockers[i.player] and old_rule(i)

    if location_locality_needed(multiworld):

        # create fewer lambdas to save memory and cache misses
        for player in multiworld.player_ids:
            world = multiworld.worlds[player]
            local_func_cache = {}
            for loc_name in world.options.local_locations.value:
                location = world.get_location_if_available(loc_name)
                if not location:
                    continue

                if location.item_rule in local_func_cache:
                    location.item_rule = local_func_cache[location.item_rule]
                # empty rule that just returns True, overwrite
                elif location.item_rule is location.__class__.item_rule:
                    local_func_cache[location.item_rule] = location.item_rule = \
                        lambda i, p = player: i.player == p
                # special rule, needs to also be fulfilled.
                else:
                    local_func_cache[location.item_rule] = location.item_rule = \
                        lambda i, p = player, old_rule = location.item_rule: \
                        i.player == p and old_rule(i)

            non_local_func_cache = {}
            for loc_name in world.options.non_local_locations.value:
                location = world.get_location_if_available(loc_name)
                if not location:
                    continue

                location = world.get_location(loc_name)
                if location.item_rule in non_local_func_cache:
                    location.item_rule = non_local_func_cache[location.item_rule]
                # empty rule that just returns True, overwrite
                elif location.item_rule is location.__class__.item_rule:
                    non_local_func_cache[location.item_rule] = location.item_rule = \
                        lambda i, p = player: i.player != p
                # special rule, needs to also be fulfilled.
                else:
                    non_local_func_cache[location.item_rule] = location.item_rule = \
                        lambda i, p = player, old_rule = location.item_rule: \
                        i.player != p and old_rule(i)


def exclusion_rules(multiworld: MultiWorld, player: int, exclude_locations: typing.Set[str]) -> None:
    for loc_name in exclude_locations:
        location = multiworld.get_location_if_available(loc_name, player)
        if not location:
            continue

        if not location.advancement:
            location.progress_type = LocationProgressType.EXCLUDED
        else:
            logging.warning(f"Unable to exclude location {loc_name} in player {player}'s world.")


def set_rule(spot: typing.Union["BaseClasses.Location", "BaseClasses.Entrance"], rule: CollectionRule):
    spot.access_rule = rule


def add_rule(spot: typing.Union["BaseClasses.Location", "BaseClasses.Entrance"], rule: CollectionRule, combine="and"):
    old_rule = spot.access_rule
    # empty rule, replace instead of add
    if old_rule is Location.access_rule or old_rule is Entrance.access_rule:
        spot.access_rule = rule if combine == "and" else old_rule
    else:
        if combine == "and":
            spot.access_rule = lambda state: rule(state) and old_rule(state)
        else:
            spot.access_rule = lambda state: rule(state) or old_rule(state)


def forbid_item(location: "BaseClasses.Location", item: str, player: int):
    old_rule = location.item_rule
    # empty rule
    if old_rule is Location.item_rule:
        location.item_rule = lambda i: i.name != item or i.player != player
    else:
        location.item_rule = lambda i: (i.name != item or i.player != player) and old_rule(i)


def forbid_items_for_player(location: "BaseClasses.Location", items: typing.Set[str], player: int):
    old_rule = location.item_rule
    location.item_rule = lambda i: (i.player != player or i.name not in items) and old_rule(i)


def forbid_items(location: "BaseClasses.Location", items: typing.Set[str]):
    """unused, but kept as a debugging tool."""
    old_rule = location.item_rule
    location.item_rule = lambda i: i.name not in items and old_rule(i)


def add_item_rule(location: "BaseClasses.Location", rule: ItemRule, combine: str = "and"):
    old_rule = location.item_rule
    # empty rule, replace instead of add
    if old_rule is Location.item_rule:
        location.item_rule = rule if combine == "and" else old_rule
    else:
        if combine == "and":
            location.item_rule = lambda item: rule(item) and old_rule(item)
        else:
            location.item_rule = lambda item: rule(item) or old_rule(item)


def item_name_in_location_names(state: "BaseClasses.CollectionState", item: str, player: int,
                                location_name_player_pairs: typing.Sequence[typing.Tuple[str, int]]) -> bool:
    for location in location_name_player_pairs:
        if location_item_name(state, location[0], location[1]) == (item, player):
            return True
    return False


def item_name_in_locations(item: str, player: int,
                           locations: typing.Sequence["BaseClasses.Location"]) -> bool:
    for location in locations:
        if location.item and location.item.name == item and location.item.player == player:
            return True
    return False


def location_item_name(state: "BaseClasses.CollectionState", location: str, player: int) -> \
        typing.Optional[typing.Tuple[str, int]]:
    location = state.multiworld.get_location(location, player)
    if location.item is None:
        return None
    return location.item.name, location.item.player


def allow_self_locking_items(spot: typing.Union[Location, Region], *item_names: str) -> None:
    """
    This function sets rules on the supplied spot, such that the supplied item_name(s) can possibly be placed there.

    spot: Location or Region that the item(s) are allowed to be placed in
    item_names: item name or names that are allowed to be placed in the Location or Region
    """
    player = spot.player

    def add_allowed_rules(area: typing.Union[Location, Entrance], location: Location) -> None:
        def set_always_allow(location: Location, rule: typing.Callable) -> None:
            location.always_allow = rule

        for item_name in item_names:
            add_rule(area, lambda state, item_name=item_name:
                     location_item_name(state, location.name, player) == (item_name, player), "or")
        set_always_allow(location, lambda state, item:
                         item.player == player and item.name in [item_name for item_name in item_names])

    if isinstance(spot, Region):
        for entrance in spot.entrances:
            for location in spot.locations:
                add_allowed_rules(entrance, location)
    else:
        add_allowed_rules(spot, spot)
