import typing

from BaseClasses import LocationProgressType

if typing.TYPE_CHECKING:
    import BaseClasses

    CollectionRule = typing.Callable[[BaseClasses.CollectionState], bool]
    ItemRule = typing.Callable[[BaseClasses.Item], bool]
else:
    CollectionRule = typing.Callable[[object], bool]
    ItemRule = typing.Callable[[object], bool]


def group_locality_rules(world):
    for group_id, group in world.groups.items():
        if set(world.player_ids) == set(group["players"]):
            continue
        if group["local_items"]:
            for location in world.get_locations():
                if location.player not in group["players"]:
                    forbid_items_for_player(location, group["local_items"], group_id)
        if group["non_local_items"]:
            for location in world.get_locations():
                if location.player in group["players"]:
                    forbid_items_for_player(location, group["non_local_items"], group_id)


def locality_rules(world, player: int):
    if world.local_items[player].value:
        for location in world.get_locations():
            if location.player != player:
                forbid_items_for_player(location, world.local_items[player].value, player)
    if world.non_local_items[player].value:
        for location in world.get_locations():
            if location.player == player:
                forbid_items_for_player(location, world.non_local_items[player].value, player)


def exclusion_rules(world, player: int, exclude_locations: typing.Set[str]):
    for loc_name in exclude_locations:
        try:
            location = world.get_location(loc_name, player)
        except KeyError as e:  # failed to find the given location. Check if it's a legitimate location
            if loc_name not in world.worlds[player].location_name_to_id:
                raise Exception(f"Unable to exclude location {loc_name} in player {player}'s world.") from e
        else: 
            add_item_rule(location, lambda i: not (i.advancement or i.useful))
            location.progress_type = LocationProgressType.EXCLUDED


def set_rule(spot: typing.Union["BaseClasses.Location", "BaseClasses.Entrance"], rule: CollectionRule):
    spot.access_rule = rule


def add_rule(spot: typing.Union["BaseClasses.Location", "BaseClasses.Entrance"], rule: CollectionRule, combine='and'):
    old_rule = spot.access_rule
    if combine == 'or':
        spot.access_rule = lambda state: rule(state) or old_rule(state)
    else:
        spot.access_rule = lambda state: rule(state) and old_rule(state)


def forbid_item(location: "BaseClasses.Location", item: str, player: int):
    old_rule = location.item_rule
    location.item_rule = lambda i: (i.name != item or i.player != player) and old_rule(i)


def forbid_items_for_player(location: "BaseClasses.Location", items: typing.Set[str], player: int):
    old_rule = location.item_rule
    location.item_rule = lambda i: (i.player != player or i.name not in items) and old_rule(i)


def forbid_items(location: "BaseClasses.Location", items: typing.Set[str]):
    """unused, but kept as a debugging tool."""
    old_rule = location.item_rule
    location.item_rule = lambda i: i.name not in items and old_rule(i)


def add_item_rule(location: "BaseClasses.Location", rule: ItemRule):
    old_rule = location.item_rule
    location.item_rule = lambda item: rule(item) and old_rule(item)


def item_in_locations(state: "BaseClasses.CollectionState", item: str, player: int,
                      locations: typing.Sequence["BaseClasses.Location"]) -> bool:
    for location in locations:
        if item_name(state, location[0], location[1]) == (item, player):
            return True
    return False


def item_name(state: "BaseClasses.CollectionState", location: str, player: int) -> \
        typing.Optional[typing.Tuple[str, int]]:
    location = state.world.get_location(location, player)
    if location.item is None:
        return None
    return location.item.name, location.item.player
