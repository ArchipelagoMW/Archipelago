import typing
from ..generic.Rules import add_rule
from .Regions import v6areas


def _has_trinket_range(state, player, start, end) -> bool:
    for i in range(start, end):
        if not state.has("Trinket " + str(i + 1).zfill(2), player):
            return False
    return True


def set_rules(multiworld, options, player, area_connections: typing.Dict[int, int], area_cost_map: typing.Dict[int, int]):
    areashuffle = list(range(len(v6areas)))
    if options.area_rando:
        multiworld.random.shuffle(areashuffle)
    area_connections.update({(index + 1): (value + 1) for index, value in enumerate(areashuffle)})
    area_connections.update({0: 0})
    if options.area_cost:
        multiworld.random.shuffle(areashuffle)
    area_cost_map.update({(index + 1): (value + 1) for index, value in enumerate(areashuffle)})
    area_cost_map.update({0: 0})

    menu_region = multiworld.get_region("Menu", player)
    for i in range(1, 5):
        target_region = multiworld.get_region(v6areas[area_connections[i] - 1], player)
        menu_region.connect(connecting_region=target_region,
                            rule=lambda state, i=i: _has_trinket_range(state, player,
                                                                       options.door_cost * (area_cost_map[i] - 1),
                                                                       options.door_cost * area_cost_map[i]))

    # Special Rule for V
    add_rule(multiworld.get_location("V", player), lambda state: state.can_reach("Laboratory", 'Region', player) and
                                                            state.can_reach("The Tower", 'Region', player) and
                                                            state.can_reach("Space Station 2", 'Region', player) and
                                                            state.can_reach("Warp Zone", 'Region', player))

    # Special Rule for NPC Trinket
    add_rule(multiworld.get_location("NPC Trinket", player),
             lambda state: state.can_reach("Laboratory", 'Region', player) or
                           (state.can_reach("The Tower", 'Region', player) and
                            state.can_reach("Space Station 2", 'Region', player) and
                            state.can_reach("Warp Zone", 'Region', player)))

    multiworld.completion_condition[player] = lambda state: state.can_reach("V", 'Location', player)
