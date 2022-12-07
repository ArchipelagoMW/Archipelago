import typing

from BaseClasses import MultiWorld
from .Regions import connect_regions, v6areas
from ..AutoWorld import LogicMixin
from ..generic.Rules import add_rule


class V6Logic(LogicMixin):
    def has_trinket_range(self, player, start, end) -> bool:
        for i in range(start, end):
            return self.has("Trinket " + str(i + 1).zfill(2), player)


def set_rules(multiworld: MultiWorld, player: int, area_connections: typing.Dict[int, int], area_cost_map: typing.Dict[int, int]):
    area_shuffle = list(range(len(v6areas)))
    if multiworld.AreaRandomizer[player].value:
        multiworld.random.shuffle(area_shuffle)
    area_connections.update({(index + 1): (value + 1) for index, value in enumerate(area_shuffle)})
    area_connections.update({0: 0})
    if multiworld.AreaCostRandomizer[player].value:
        multiworld.random.shuffle(area_shuffle)
    area_cost_map.update({(index + 1): (value + 1) for index, value in enumerate(area_shuffle)})
    area_cost_map.update({0: 0})

    for i in range(1, 5):
        connect_regions(multiworld, player, "Menu", v6areas[area_connections[i] - 1],
                        lambda state, i=i: _has_trinket_range(state, player,
                                                              multiworld.DoorCost[player].value * (area_cost_map[i] - 1),
                                                              multiworld.DoorCost[player].value * area_cost_map[i]))

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
