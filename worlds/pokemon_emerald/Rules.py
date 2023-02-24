from BaseClasses import CollectionState, MultiWorld
from worlds.generic.Rules import set_rule


def _can_cut(state: CollectionState, player: int):
    return state.has("HM01 Cut", player) and state.has("Stone Badge", player)
def _can_fly(state: CollectionState, player: int):
    return state.has("HM02 Fly", player) and state.has("Feather Badge", player)
def _can_surf(state: CollectionState, player: int):
    return state.has("HM03 Surf", player) and state.has("Balance Badge", player)
def _can_strength(state: CollectionState, player: int):
    return state.has("HM04 Strength", player) and state.has("Heat Badge", player)
def _can_flash(state: CollectionState, player: int):
    return state.has("HM05 Flash", player) and state.has("Knuckle Badge", player)
def _can_rock_smash(state: CollectionState, player: int):
    return state.has("HM06 Rock Smash", player) and state.has("Dynamo Badge", player)
def _can_waterfall(state: CollectionState, player: int):
    return state.has("HM07 Waterfall", player) and state.has("Rain Badge", player)
def _can_dive(state: CollectionState, player: int):
    return state.has("HM08 Dive", player) and state.has("Mind Badge", player)


def set_default_rules(world: MultiWorld, player):
    set_rule(
        world.get_entrance("REGION_OLDALE_TOWN/MAIN -> REGION_ROUTE102/MAIN", player),
        lambda state: state.has("EVENT_DEFEAT_RIVAL_ROUTE_103", player)
    )

    set_rule(
        world.get_entrance("REGION_ROUTE103/EAST -> REGION_ROUTE103/WATER", player),
        lambda state: _can_surf(state, player)
    )
    set_rule(
        world.get_entrance("REGION_ROUTE103/WEST -> REGION_ROUTE103/WATER", player),
        lambda state: _can_surf(state, player)
    )

    set_rule(
        world.get_entrance("REGION_PETALBURG_CITY/MAIN -> REGION_PETALBURG_CITY/SOUTH_POND", player),
        lambda state: _can_surf(state, player)
    )
    set_rule(
        world.get_entrance("REGION_PETALBURG_CITY/MAIN -> REGION_PETALBURG_CITY/NORTH_POND", player),
        lambda state: _can_surf(state, player)
    )
