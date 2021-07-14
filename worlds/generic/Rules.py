def locality_rules(world, player):
    if world.local_items[player]:
        for location in world.get_locations():
            if location.player != player:
                forbid_items_for_player(location, world.local_items[player], player)
    if world.non_local_items[player]:
        for location in world.get_locations():
            if location.player == player:
                forbid_items_for_player(location, world.non_local_items[player], player)


def exclusion_rules(world, player: int, excluded_locations: set):
    for loc_name in excluded_locations:
        location = world.get_location(loc_name, player)
        add_item_rule(location, lambda i: not (i.advancement or i.smallkey or i.bigkey))


def set_rule(spot, rule):
    spot.access_rule = rule


def add_rule(spot, rule, combine='and'):
    old_rule = spot.access_rule
    if combine == 'or':
        spot.access_rule = lambda state: rule(state) or old_rule(state)
    else:
        spot.access_rule = lambda state: rule(state) and old_rule(state)


def forbid_item(location, item, player: int):
    old_rule = location.item_rule
    location.item_rule = lambda i: (i.name != item or i.player != player) and old_rule(i)


def forbid_items_for_player(location, items: set, player: int):
    old_rule = location.item_rule
    location.item_rule = lambda i: (i.player != player or i.name not in items) and old_rule(i)


def forbid_items(location, items: set):
    """unused, but kept as a debugging tool."""
    old_rule = location.item_rule
    location.item_rule = lambda i: i.name not in items and old_rule(i)


def add_item_rule(location, rule):
    old_rule = location.item_rule
    location.item_rule = lambda item: rule(item) and old_rule(item)


def item_in_locations(state, item, player, locations):
    for location in locations:
        if item_name(state, location[0], location[1]) == (item, player):
            return True
    return False


def item_name(state, location, player):
    location = state.world.get_location(location, player)
    if location.item is None:
        return None
    return (location.item.name, location.item.player)