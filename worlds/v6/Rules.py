from BaseClasses import CollectionState, MultiWorld
from .Regions import v6_areas
from ..generic.Rules import add_rule


def has_trinket_range(state: CollectionState, player: int, start: int, end: int) -> bool:
    for i in range(start, end):
        return state.has(f"Trinket {str(i + 1).zfill(2)}", player)


def can_reach_all_areas(state: CollectionState, player: int) -> bool:
    return state.can_reach("Laboratory", "Entrance", player) and \
           state.can_reach("The Tower", "Entrance", player) and \
           state.can_reach("Space Station 2", "Entrance", player) and \
           state.can_reach("Warp Zone", "Entrance", player)


def can_reach_npc_trinket(state: CollectionState, player: int) -> bool:
    return state.can_reach("Laboratory", "Entrance", player) or (
           state.can_reach("The Tower", "Entrance", player) and
           state.can_reach("Space Station 2", "Entrance", player) and
           state.can_reach("Warp Zone", "Entrance", player))


def set_rules(multiworld: MultiWorld, player: int):
    for index, region in enumerate(v6_areas, start=1):
        multiworld.get_entrance(region, player).access_rule = lambda state: has_trinket_range(
            state,
            player,
            multiworld.DoorCost[player] * (multiworld.worlds[player].area_cost_map[index] - 1),
            multiworld.DoorCost[player] * multiworld.worlds[player].area_cost_map[index],
        )

    # Special Rule for V
    add_rule(multiworld.get_location("V", player), lambda state: can_reach_all_areas(state, player))

    # Special Rule for NPC Trinket
    add_rule(multiworld.get_location("NPC Trinket", player), lambda state: can_reach_npc_trinket(state, player))

    # Victory condition
    if multiworld.DoorCost[player] == 0:
        multiworld.completion_condition[player] = lambda state: True
    else:
        multiworld.completion_condition[player] = lambda state: state.can_reach("V", "Location", player)
