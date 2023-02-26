from BaseClasses import CollectionState, MultiWorld
from worlds.generic.Rules import set_rule, add_rule
from .Data import get_location_attributes


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
def _can_use_mach_bike(state: CollectionState, player: int):
    return state.has("EVENT_RECEIVE_BIKE", player)
def _can_use_acro_bike(state: CollectionState, player: int):
    return state.has("EVENT_RECEIVE_BIKE", player)


def set_default_rules(multiworld: MultiWorld, player: int):
    location_attributes = get_location_attributes()
    name_to_label = lambda name: location_attributes[name].label

    # Oldale Town
    set_rule(
        multiworld.get_entrance("REGION_OLDALE_TOWN/MAIN -> REGION_ROUTE102/MAIN", player),
        lambda state: state.has("EVENT_DEFEAT_RIVAL_ROUTE_103", player)
    )

    # Route 103
    set_rule(
        multiworld.get_entrance("REGION_ROUTE103/EAST -> REGION_ROUTE103/WATER", player),
        lambda state: _can_surf(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE103/WEST -> REGION_ROUTE103/WATER", player),
        lambda state: _can_surf(state, player)
    )

    # Petalburg City
    set_rule(
        multiworld.get_entrance("REGION_PETALBURG_CITY/MAIN -> REGION_PETALBURG_CITY/SOUTH_POND", player),
        lambda state: _can_surf(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_PETALBURG_CITY/MAIN -> REGION_PETALBURG_CITY/NORTH_POND", player),
        lambda state: _can_surf(state, player)
    )

    # Route 104
    set_rule(
        multiworld.get_entrance("REGION_ROUTE104/SOUTH -> REGION_ROUTE105/MAIN", player),
        lambda state: _can_surf(state, player)
    )
    set_rule(
        multiworld.get_location(name_to_label("ITEM_ROUTE_104_X_ACCURACY"), player),
        lambda state: _can_surf(state, player) or _can_cut(state, player)
    )
    set_rule(
        multiworld.get_location(name_to_label("ITEM_ROUTE_104_PP_UP"), player),
        lambda state: _can_surf(state, player)
    )

    # Route 109
    set_rule(
        multiworld.get_entrance("REGION_ROUTE109/BEACH -> REGION_ROUTE109/SEA", player),
        lambda state: _can_surf(state, player)
    )

    # Route 115
    set_rule(
        multiworld.get_entrance("REGION_ROUTE115/SOUTH_BELOW_LEDGE -> REGION_ROUTE115/SEA", player),
        lambda state: _can_surf(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE115/SOUTH_ABOVE_LEDGE -> REGION_ROUTE115/SEA", player),
        lambda state: _can_surf(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE115/NORTH_BELOW_SLOPE -> REGION_ROUTE115/SEA", player),
        lambda state: _can_surf(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE115/NORTH_BELOW_SLOPE -> REGION_ROUTE115/NORTH_ABOVE_SLOPE", player),
        lambda state: _can_use_mach_bike(state, player)
    )

    # Route 105
    set_rule(
        multiworld.get_entrance("REGION_ROUTE105/MAIN -> REGION_UNDERWATER_ROUTE105/MAIN", player),
        lambda state: _can_dive(state, player)
    )

    # Route 106
    set_rule(
        multiworld.get_entrance("REGION_ROUTE106/EAST -> REGION_ROUTE106/SEA", player),
        lambda state: _can_surf(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE106/WEST -> REGION_ROUTE106/SEA", player),
        lambda state: _can_surf(state, player)
    )

    # Route 107
    set_rule(
        multiworld.get_entrance("REGION_DEWFORD_TOWN/MAIN -> REGION_ROUTE107/MAIN", player),
        lambda state: _can_surf(state, player)
    )

    # Slateport City
    set_rule(
        multiworld.get_entrance("REGION_SLATEPORT_CITY/MAIN -> REGION_ROUTE134/WEST", player),
        lambda state: _can_surf(state, player)
    )

    # Route 110
    set_rule(
        multiworld.get_entrance("REGION_ROUTE110/MAIN -> REGION_ROUTE110/SOUTH_WATER", player),
        lambda state: _can_surf(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE110/MAIN -> REGION_ROUTE110/NORTH_WATER", player),
        lambda state: _can_surf(state, player)
    )

    # Route 111
    set_rule(
        multiworld.get_entrance("REGION_ROUTE111/SOUTH -> REGION_ROUTE111/DESERT", player),
        lambda state: state.has("Go Goggles", player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE111/NORTH -> REGION_ROUTE111/DESERT", player),
        lambda state: state.has("Go Goggles", player)
    )

    # Route 114
    set_rule(
        multiworld.get_entrance("REGION_ROUTE114/MAIN -> REGION_ROUTE114/ABOVE_WATERFALL", player),
        lambda state: _can_surf(state, player) and _can_waterfall(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE114/ABOVE_WATERFALL -> REGION_ROUTE114/MAIN", player),
        lambda state: _can_surf(state, player) and _can_waterfall(state, player)
    )

    # Route 119
    set_rule(
        multiworld.get_entrance("REGION_ROUTE119/LOWER -> REGION_ROUTE119/LOWER_WEST_BANK", player),
        lambda state: _can_surf(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE119/LOWER_WEST_BANK -> REGION_ROUTE119/LOWER", player),
        lambda state: _can_surf(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE119/LOWER_WEST_BANK -> REGION_ROUTE119/LOWER_ACROSS_RAILS", player),
        lambda state: _can_use_acro_bike(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE119/LOWER_ACROSS_RAILS -> REGION_ROUTE119/LOWER_WEST_BANK", player),
        lambda state: _can_use_acro_bike(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE119/UPPER -> REGION_ROUTE119/MIDDLE_RIVER", player),
        lambda state: _can_surf(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE119/MIDDLE_RIVER -> REGION_ROUTE119/ABOVE_WATERFALL", player),
        lambda state: _can_waterfall(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE119/ABOVE_WATERFALL -> REGION_ROUTE119/MIDDLE_RIVER", player),
        lambda state: _can_waterfall(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE119/ABOVE_WATERFALL -> REGION_ROUTE119/ABOVE_WATERFALL_ACROSS_RAILS", player),
        lambda state: _can_use_acro_bike(state, player)
    )

    # Fortree City
    set_rule(
        multiworld.get_entrance("REGION_FORTREE_CITY/MAIN -> REGION_FORTREE_CITY/BEFORE_GYM", player),
        lambda state: state.has("Devon Scope", player)
    )
    set_rule(
        multiworld.get_entrance("REGION_FORTREE_CITY/BEFORE_GYM -> REGION_FORTREE_CITY/MAIN", player),
        lambda state: state.has("Devon Scope", player)
    )

    # TODO: Check behavior of talking to Steven on Route 120 from west or
    # interacting with the Kecleon while having the Devon Scope and without
    # talking to Steven

    # Route 120
    # set_rule(
    #     multiworld.get_entrance("REGION_ROUTE120/NORTH -> REGION_ROUTE120/SOUTH", player),
    #     lambda state: state.has("Devon Scope", player)
    # )
    # set_rule(
    #     multiworld.get_entrance("REGION_ROUTE120/SOUTH -> REGION_ROUTE120/NORTH", player),
    #     lambda state: state.has("Devon Scope", player)
    # )

    # Route 121
    set_rule(
        multiworld.get_entrance("REGION_ROUTE121/MAIN -> REGION_ROUTE122/SEA", player),
        lambda state: _can_surf(state, player)
    )

    # Route 122
    set_rule(
        multiworld.get_entrance("REGION_ROUTE122/MT_PYRE_ENTRANCE -> REGION_ROUTE122/SEA", player),
        lambda state: _can_surf(state, player)
    )

    # Route 123
    set_rule(
        multiworld.get_entrance("REGION_ROUTE123/EAST -> REGION_ROUTE122/SEA", player),
        lambda state: _can_surf(state, player)
    )

    # Lilycove City
    set_rule(
        multiworld.get_entrance("REGION_LILYCOVE_CITY/MAIN -> REGION_LILYCOVE_CITY/SEA", player),
        lambda state: _can_surf(state, player)
    )

    # Route 124
    set_rule(
        multiworld.get_entrance("REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/BIG_AREA", player),
        lambda state: _can_dive(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/SMALL_AREA_1", player),
        lambda state: _can_dive(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/SMALL_AREA_2", player),
        lambda state: _can_dive(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/SMALL_AREA_3", player),
        lambda state: _can_dive(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/TUNNEL_1", player),
        lambda state: _can_dive(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/TUNNEL_2", player),
        lambda state: _can_dive(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/TUNNEL_3", player),
        lambda state: _can_dive(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/TUNNEL_4", player),
        lambda state: _can_dive(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE124/NORTH_ENCLOSED_AREA_1 -> REGION_UNDERWATER_ROUTE124/TUNNEL_1", player),
        lambda state: _can_dive(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE124/NORTH_ENCLOSED_AREA_2 -> REGION_UNDERWATER_ROUTE124/TUNNEL_1", player),
        lambda state: _can_dive(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE124/NORTH_ENCLOSED_AREA_3 -> REGION_UNDERWATER_ROUTE124/TUNNEL_2", player),
        lambda state: _can_dive(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE124/SOUTH_ENCLOSED_AREA_1 -> REGION_UNDERWATER_ROUTE124/TUNNEL_3", player),
        lambda state: _can_dive(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE124/SOUTH_ENCLOSED_AREA_2 -> REGION_UNDERWATER_ROUTE124/TUNNEL_3", player),
        lambda state: _can_dive(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE124/SOUTH_ENCLOSED_AREA_3 -> REGION_UNDERWATER_ROUTE124/TUNNEL_4", player),
        lambda state: _can_dive(state, player)
    )

    # Mossdeep City
    set_rule(
        multiworld.get_entrance("REGION_MOSSDEEP_CITY/MAIN -> REGION_ROUTE124/MAIN", player),
        lambda state: _can_surf(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_MOSSDEEP_CITY/MAIN -> REGION_ROUTE125/SEA", player),
        lambda state: _can_surf(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_MOSSDEEP_CITY/MAIN -> REGION_ROUTE127/MAIN", player),
        lambda state: _can_surf(state, player)
    )

    # Route 126
    set_rule(
        multiworld.get_entrance("REGION_ROUTE126/MAIN -> REGION_UNDERWATER_ROUTE126/MAIN", player),
        lambda state: _can_dive(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE126/MAIN -> REGION_UNDERWATER_ROUTE126/SMALL_AREA_2", player),
        lambda state: _can_dive(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE126/NEAR_ROUTE_124 -> REGION_UNDERWATER_ROUTE126/TUNNEL", player),
        lambda state: _can_dive(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE126/NORTH_WEST_CORNER -> REGION_UNDERWATER_ROUTE126/TUNNEL", player),
        lambda state: _can_dive(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE126/WEST -> REGION_UNDERWATER_ROUTE126/MAIN", player),
        lambda state: _can_dive(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE126/WEST -> REGION_UNDERWATER_ROUTE126/SMALL_AREA_1", player),
        lambda state: _can_dive(state, player)
    )

    # Route 127
    set_rule(
        multiworld.get_entrance("REGION_ROUTE127/MAIN -> REGION_UNDERWATER_ROUTE127/TUNNEL", player),
        lambda state: _can_dive(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE127/MAIN -> REGION_UNDERWATER_ROUTE127/AREA_1", player),
        lambda state: _can_dive(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE127/MAIN -> REGION_UNDERWATER_ROUTE127/AREA_2", player),
        lambda state: _can_dive(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE127/MAIN -> REGION_UNDERWATER_ROUTE127/AREA_3", player),
        lambda state: _can_dive(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE127/ENCLOSED_AREA -> REGION_UNDERWATER_ROUTE127/TUNNEL", player),
        lambda state: _can_dive(state, player)
    )

    # Route 128
    set_rule(
        multiworld.get_entrance("REGION_ROUTE128/MAIN -> REGION_UNDERWATER_ROUTE128/MAIN", player),
        lambda state: _can_dive(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE128/MAIN -> REGION_UNDERWATER_ROUTE128/AREA_1", player),
        lambda state: _can_dive(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE128/MAIN -> REGION_UNDERWATER_ROUTE128/AREA_2", player),
        lambda state: _can_dive(state, player)
    )

    # Pacifidlog Town
    set_rule(
        multiworld.get_entrance("REGION_PACIFIDLOG_TOWN/MAIN -> REGION_ROUTE131/MAIN", player),
        lambda state: _can_surf(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_PACIFIDLOG_TOWN/MAIN -> REGION_ROUTE132/EAST", player),
        lambda state: _can_surf(state, player)
    )

    # Route 134
    set_rule(
        multiworld.get_entrance("REGION_ROUTE134/MAIN -> REGION_UNDERWATER_ROUTE134/MAIN", player),
        lambda state: _can_dive(state, player)
    )

    # Ever Grande City
    set_rule(
        multiworld.get_entrance("REGION_EVER_GRANDE_CITY/SEA -> REGION_EVER_GRANDE_CITY/SOUTH", player),
        lambda state: _can_waterfall(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_EVER_GRANDE_CITY/SOUTH -> REGION_EVER_GRANDE_CITY/SEA", player),
        lambda state: _can_surf(state, player) and _can_waterfall(state, player)
    )

    # Pokemon League
    set_rule(
        multiworld.get_entrance("REGION_EVER_GRANDE_CITY_POKEMON_LEAGUE_1F/MAIN -> REGION_EVER_GRANDE_CITY_POKEMON_LEAGUE_1F/BEHIND_BADGE_CHECKERS", player),
        lambda state: state.has_all(["Stone Badge", "Knuckle Badge", "Dynamo Badge", "Heat Badge", "Balance Badge", "Feather Badge", "Mind Badge", "Rain Badge"], player)
    )
