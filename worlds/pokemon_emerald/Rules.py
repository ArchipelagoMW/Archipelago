from BaseClasses import CollectionState
from worlds.generic.Rules import set_rule


def can_cut(state: CollectionState, player: int):
    return state.has("HM01 Cut", player) and state.has("Stone Badge", player)
def can_fly(state: CollectionState, player: int):
    return state.has("HM02 Fly", player) and state.has("Feather Badge", player)
def can_surf(state: CollectionState, player: int):
    return state.has("HM03 Surf", player) and state.has("Balance Badge", player)
def can_strength(state: CollectionState, player: int):
    return state.has("HM04 Strength", player) and state.has("Heat Badge", player)
def can_flash(state: CollectionState, player: int):
    return state.has("HM05 Flash", player) and state.has("Knuckle Badge", player)
def can_rock_smash(state: CollectionState, player: int):
    return state.has("HM06 Rock Smash", player) and state.has("Dynamo Badge", player)
def can_waterfall(state: CollectionState, player: int):
    return state.has("HM07 Waterfall", player) and state.has("Rain Badge", player)
def can_dive(state: CollectionState, player: int):
    return state.has("HM08 Dive", player) and state.has("Mind Badge", player)


def set_default_rules(world, player):
    set_rule(
        world.get_entrance('REGION_ROUTE_103/EAST -> REGION_ROUTE_103/WATER', player),
        lambda state: can_surf(state, player)
    )
    set_rule(
        world.get_entrance('REGION_ROUTE_103/WEST -> REGION_ROUTE_103/WATER', player),
        lambda state: can_surf(state, player)
    )
    set_rule(
        world.get_entrance('REGION_PETALBURG_CITY/MAIN -> REGION_PETALBURG_CITY/SOUTH_POND', player),
        lambda state: can_surf(state, player)
    )
    set_rule(
        world.get_entrance('REGION_PETALBURG_CITY/MAIN -> REGION_PETALBURG_CITY/NORTH_POND', player),
        lambda state: can_surf(state, player)
    )
