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
def _has_at_least_n_badges(state: CollectionState, player: int, n: int):
    num_badges = 0
    num_badges += 1 if state.has("Stone Badge", player) else 0
    num_badges += 1 if state.has("Knuckle Badge", player) else 0
    num_badges += 1 if state.has("Dynamo Badge", player) else 0
    num_badges += 1 if state.has("Heat Badge", player) else 0
    num_badges += 1 if state.has("Balance Badge", player) else 0
    num_badges += 1 if state.has("Feather Badge", player) else 0
    num_badges += 1 if state.has("Mind Badge", player) else 0
    num_badges += 1 if state.has("Rain Badge", player) else 0
    return num_badges >= n


def set_default_rules(multiworld: MultiWorld, player: int):
    location_attributes = get_location_attributes()
    name_to_label = lambda name: location_attributes[name].label

    can_cut = lambda state: _can_cut(state, player)
    can_fly = lambda state: _can_fly(state, player)
    can_surf = lambda state: _can_surf(state, player)
    can_strength = lambda state: _can_strength(state, player)
    can_flash = lambda state: _can_flash(state, player)
    can_rock_smash = lambda state: _can_rock_smash(state, player)
    can_waterfall = lambda state: _can_waterfall(state, player)
    can_dive = lambda state: _can_dive(state, player)

    # Oldale Town
    set_rule(
        multiworld.get_entrance("REGION_OLDALE_TOWN/MAIN -> REGION_ROUTE102/MAIN", player),
        lambda state: state.has("EVENT_DEFEAT_RIVAL_ROUTE_103", player)
    )

    # Route 103
    set_rule(
        multiworld.get_entrance("REGION_ROUTE103/EAST -> REGION_ROUTE103/WATER", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE103/WEST -> REGION_ROUTE103/WATER", player),
        can_surf
    )
    set_rule(
        multiworld.get_location(name_to_label("ITEM_ROUTE_103_PP_UP"), player),
        can_cut
    )
    set_rule(
        multiworld.get_location(name_to_label("ITEM_ROUTE_103_GUARD_SPEC"), player),
        can_cut
    )

    # Petalburg City
    set_rule(
        multiworld.get_entrance("REGION_PETALBURG_CITY/MAIN -> REGION_PETALBURG_CITY/SOUTH_POND", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_PETALBURG_CITY/MAIN -> REGION_PETALBURG_CITY/NORTH_POND", player),
        can_surf
    )

    set_rule(
        multiworld.get_entrance("REGION_PETALBURG_CITY/MAIN -> REGION_PETALBURG_CITY/NORTH_POND", player),
        can_surf
    )

    # Route 104
    set_rule(
        multiworld.get_entrance("REGION_ROUTE104/SOUTH -> REGION_ROUTE105/MAIN", player),
        can_surf
    )
    set_rule(
        multiworld.get_location(name_to_label("ITEM_ROUTE_104_X_ACCURACY"), player),
        lambda state: can_surf(state) or can_cut(state)
    )
    set_rule(
        multiworld.get_location(name_to_label("ITEM_ROUTE_104_PP_UP"), player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE104_MR_BRINEYS_HOUSE/MAIN -> REGION_DEWFORD_TOWN/MAIN", player),
        lambda state: state.has("EVENT_RESCUED_PEEKO", player)
    )

    # Petalburg Woods
    set_rule(
        multiworld.get_entrance("REGION_PETALBURG_WOODS/WEST_PATH -> REGION_PETALBURG_WOODS/EAST_PATH", player),
        can_cut
    )

    # Route 116
    set_rule(
        multiworld.get_entrance("REGION_ROUTE116/WEST -> REGION_ROUTE116/WEST_ABOVE_LEDGE", player),
        can_cut
    )

    # Rusturf Tunnel
    set_rule(
        multiworld.get_entrance("REGION_RUSTURF_TUNNEL/WEST -> REGION_RUSTURF_TUNNEL/EAST", player),
        can_rock_smash
    )
    set_rule(
        multiworld.get_entrance("REGION_RUSTURF_TUNNEL/EAST -> REGION_RUSTURF_TUNNEL/WEST", player),
        can_rock_smash
    )

    # Dewford Town
    set_rule(
        multiworld.get_entrance("REGION_DEWFORD_TOWN/MAIN -> REGION_ROUTE109/BEACH", player),
        lambda state:
            state.can_reach("REGION_ROUTE104_MR_BRINEYS_HOUSE/MAIN -> REGION_DEWFORD_TOWN/MAIN", "Entrance", player)
            and state.has("EVENT_RESCUED_PEEKO", player)
            and state.has("EVENT_DELIVERED_LETTER", player)
    )
    set_rule(
        multiworld.get_entrance("REGION_DEWFORD_TOWN/MAIN -> REGION_ROUTE104_MR_BRINEYS_HOUSE/MAIN", player),
        lambda state:
            state.can_reach("REGION_ROUTE104_MR_BRINEYS_HOUSE/MAIN -> REGION_DEWFORD_TOWN/MAIN", "Entrance", player)
            and state.has("EVENT_RESCUED_PEEKO", player)
    )

    # Granite Cave
    set_rule(
        multiworld.get_entrance("REGION_GRANITE_CAVE_STEVENS_ROOM/MAIN -> REGION_GRANITE_CAVE_STEVENS_ROOM/LETTER_DELIVERED", player),
        lambda state: state.has("Letter", player)
    )
    set_rule(
        multiworld.get_entrance("REGION_GRANITE_CAVE_B1F/LOWER -> REGION_GRANITE_CAVE_B1F/UPPER", player),
        lambda state: _can_use_mach_bike(state, player)
    )

    # Route 109
    set_rule(
        multiworld.get_entrance("REGION_ROUTE109/BEACH -> REGION_DEWFORD_TOWN/MAIN", player),
        lambda state:
            state.can_reach("REGION_ROUTE104_MR_BRINEYS_HOUSE/MAIN -> REGION_DEWFORD_TOWN/MAIN", "Entrance", player)
            and state.can_reach("REGION_DEWFORD_TOWN/MAIN -> REGION_ROUTE109/BEACH", "Entrance", player)
            and state.has("EVENT_RESCUED_PEEKO", player)
            and state.has("EVENT_DELIVERED_LETTER", player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE109/BEACH -> REGION_ROUTE109/SEA", player),
        can_surf
    )

    # Route 115
    set_rule(
        multiworld.get_entrance("REGION_ROUTE115/SOUTH_BELOW_LEDGE -> REGION_ROUTE115/SEA", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE115/SOUTH_ABOVE_LEDGE -> REGION_ROUTE115/SEA", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE115/SOUTH_ABOVE_LEDGE -> REGION_ROUTE115/SOUTH_BEHIND_ROCK", player),
        can_rock_smash
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE115/NORTH_BELOW_SLOPE -> REGION_ROUTE115/SEA", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE115/NORTH_BELOW_SLOPE -> REGION_ROUTE115/NORTH_ABOVE_SLOPE", player),
        lambda state: _can_use_mach_bike(state, player)
    )

    # Route 105
    set_rule(
        multiworld.get_entrance("REGION_ROUTE105/MAIN -> REGION_UNDERWATER_ROUTE105/MAIN", player),
        can_dive
    )

    # Route 106
    set_rule(
        multiworld.get_entrance("REGION_ROUTE106/EAST -> REGION_ROUTE106/SEA", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE106/WEST -> REGION_ROUTE106/SEA", player),
        can_surf
    )

    # Route 107
    set_rule(
        multiworld.get_entrance("REGION_DEWFORD_TOWN/MAIN -> REGION_ROUTE107/MAIN", player),
        can_surf
    )

    # Slateport City
    set_rule(
        multiworld.get_entrance("REGION_SLATEPORT_CITY/MAIN -> REGION_ROUTE134/WEST", player),
        can_surf
    )

    # Route 117
    set_rule(
        multiworld.get_location(name_to_label("ITEM_ROUTE_117_REVIVE"), player),
        can_cut
    )

    # Route 110
    set_rule(
        multiworld.get_entrance("REGION_ROUTE110/MAIN -> REGION_ROUTE110/SOUTH_WATER", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE110/MAIN -> REGION_ROUTE110/NORTH_WATER", player),
        can_surf
    )

    # Route 111
    set_rule(
        multiworld.get_entrance("REGION_ROUTE111/MIDDLE -> REGION_ROUTE111/DESERT", player),
        lambda state: state.has("Go Goggles", player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE111/NORTH -> REGION_ROUTE111/DESERT", player),
        lambda state: state.has("Go Goggles", player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE111/MIDDLE -> REGION_ROUTE111/SOUTH", player),
        can_rock_smash
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE111/SOUTH -> REGION_ROUTE111/MIDDLE", player),
        can_rock_smash
    )

    # Fiery Path
    set_rule(
        multiworld.get_entrance("REGION_FIERY_PATH/MAIN -> REGION_FIERY_PATH/BEHIND_BOULDER", player),
        can_strength
    )

    # Route 114
    set_rule(
        multiworld.get_entrance("REGION_ROUTE114/MAIN -> REGION_ROUTE114/ABOVE_WATERFALL", player),
        lambda state: can_surf(state) and can_waterfall(state)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE114/ABOVE_WATERFALL -> REGION_ROUTE114/MAIN", player),
        lambda state: can_surf(state) and can_waterfall(state)
    )
    set_rule(
        multiworld.get_location(name_to_label("ITEM_ROUTE_114_PROTEIN"), player),
        can_rock_smash
    )

    # Meteor Falls
    set_rule(
        multiworld.get_entrance("REGION_METEOR_FALLS_1F_1R/MAIN -> REGION_METEOR_FALLS_1F_1R/ABOVE_WATERFALL", player),
        lambda state: can_surf(state) and can_waterfall(state)
    )
    set_rule(
        multiworld.get_entrance("REGION_METEOR_FALLS_1F_1R/ABOVE_WATERFALL -> REGION_METEOR_FALLS_1F_1R/MAIN", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_METEOR_FALLS_B1F_1R/HIGHEST_LADDER -> REGION_METEOR_FALLS_B1F_1R/WATER", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_METEOR_FALLS_B1F_1R/NORTH_SHORE -> REGION_METEOR_FALLS_B1F_1R/WATER", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_METEOR_FALLS_B1F_1R/SOUTH_SHORE -> REGION_METEOR_FALLS_B1F_1R/WATER", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_METEOR_FALLS_B1F_2R/ENTRANCE -> REGION_METEOR_FALLS_B1F_2R/WATER", player),
        can_surf
    )

    # Jagged Pass
    set_rule(
        multiworld.get_entrance("REGION_JAGGED_PASS/BOTTOM -> REGION_JAGGED_PASS/MIDDLE", player),
        lambda state: _can_use_acro_bike(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_JAGGED_PASS/MIDDLE -> REGION_JAGGED_PASS/TOP", player),
        lambda state: _can_use_acro_bike(state, player)
    )

    # Mirage Tower
    set_rule(
        multiworld.get_entrance("REGION_MIRAGE_TOWER_2F/TOP -> REGION_MIRAGE_TOWER_2F/BOTTOM", player),
        lambda state: _can_use_mach_bike(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_MIRAGE_TOWER_2F/BOTTOM -> REGION_MIRAGE_TOWER_2F/TOP", player),
        lambda state: _can_use_mach_bike(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_MIRAGE_TOWER_3F/TOP -> REGION_MIRAGE_TOWER_3F/BOTTOM", player),
        can_rock_smash
    )
    set_rule(
        multiworld.get_entrance("REGION_MIRAGE_TOWER_3F/BOTTOM -> REGION_MIRAGE_TOWER_3F/TOP", player),
        can_rock_smash
    )
    set_rule(
        multiworld.get_entrance("REGION_MIRAGE_TOWER_4F/MAIN -> REGION_MIRAGE_TOWER_4F/FOSSIL_PLATFORM", player),
        can_rock_smash
    )

    # Abandoned Ship
    set_rule(
        multiworld.get_entrance("REGION_ABANDONED_SHIP_ROOMS_B1F/CENTER -> REGION_ABANDONED_SHIP_UNDERWATER1/MAIN", player),
        can_dive
    )
    set_rule(
        multiworld.get_entrance("REGION_ABANDONED_SHIP_HIDDEN_FLOOR_CORRIDORS/MAIN -> REGION_ABANDONED_SHIP_UNDERWATER2/MAIN", player),
        can_dive
    )
    set_rule(
        multiworld.get_entrance("MAP_ABANDONED_SHIP_HIDDEN_FLOOR_CORRIDORS:3/MAP_ABANDONED_SHIP_HIDDEN_FLOOR_ROOMS:6", player),
        lambda state: state.has("Room 4 Key", player)
    )
    set_rule(
        multiworld.get_entrance("MAP_ABANDONED_SHIP_HIDDEN_FLOOR_CORRIDORS:1/MAP_ABANDONED_SHIP_HIDDEN_FLOOR_ROOMS:2", player),
        lambda state: state.has("Room 1 Key", player)
    )
    set_rule(
        multiworld.get_entrance("MAP_ABANDONED_SHIP_HIDDEN_FLOOR_CORRIDORS:2/MAP_ABANDONED_SHIP_HIDDEN_FLOOR_ROOMS:4", player),
        lambda state: state.has("Room 2 Key", player)
    )
    set_rule(
        multiworld.get_entrance("MAP_ABANDONED_SHIP_HIDDEN_FLOOR_CORRIDORS:4/MAP_ABANDONED_SHIP_HIDDEN_FLOOR_ROOMS:7", player),
        lambda state: state.has("Room 6 Key", player)
    )
    set_rule(
        multiworld.get_entrance("MAP_ABANDONED_SHIP_CORRIDORS_B1F:5/MAP_ABANDONED_SHIP_ROOM_B1F:0", player),
        lambda state: state.has("Storage Key", player)
    )

    # Route 118
    set_rule(
        multiworld.get_entrance("REGION_ROUTE118/WEST -> REGION_ROUTE118/WATER", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE118/EAST -> REGION_ROUTE118/WATER", player),
        can_surf
    )

    # Route 119
    set_rule(
        multiworld.get_entrance("REGION_ROUTE119/LOWER -> REGION_ROUTE119/LOWER_WEST_BANK", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE119/LOWER_WEST_BANK -> REGION_ROUTE119/LOWER", player),
        can_surf
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
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE119/MIDDLE_RIVER -> REGION_ROUTE119/ABOVE_WATERFALL", player),
        can_waterfall
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE119/ABOVE_WATERFALL -> REGION_ROUTE119/MIDDLE_RIVER", player),
        can_waterfall
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
    set_rule(
        multiworld.get_entrance("REGION_ROUTE120/NORTH -> REGION_ROUTE120/NORTH_POND", player),
        lambda state: state.has("Devon Scope", player)
    )
    set_rule(
        multiworld.get_location(name_to_label("HIDDEN_ITEM_ROUTE_120_RARE_CANDY_1"), player),
        can_cut
    )

    # Route 121
    set_rule(
        multiworld.get_entrance("REGION_ROUTE121/MAIN -> REGION_ROUTE122/SEA", player),
        can_surf
    )
    set_rule(
        multiworld.get_location(name_to_label("HIDDEN_ITEM_ROUTE_121_NUGGET"), player),
        can_cut
    )

    # Safari Zone
    set_rule(
        multiworld.get_location(name_to_label("ITEM_SAFARI_ZONE_NORTH_WEST_TM22"), player),
        can_surf
    )
    set_rule(
        multiworld.get_location(name_to_label("ITEM_SAFARI_ZONE_SOUTH_WEST_MAX_REVIVE"), player),
        can_surf
    )
    set_rule(
        multiworld.get_location(name_to_label("ITEM_SAFARI_ZONE_SOUTH_EAST_BIG_PEARL"), player),
        can_surf
    )

    # Route 122
    set_rule(
        multiworld.get_entrance("REGION_ROUTE122/MT_PYRE_ENTRANCE -> REGION_ROUTE122/SEA", player),
        can_surf
    )

    # Route 123
    set_rule(
        multiworld.get_entrance("REGION_ROUTE123/EAST -> REGION_ROUTE122/SEA", player),
        can_surf
    )

    # Lilycove City
    set_rule(
        multiworld.get_entrance("REGION_LILYCOVE_CITY/MAIN -> REGION_LILYCOVE_CITY/SEA", player),
        can_surf
    )

    # Magma Hideout
    set_rule(
        multiworld.get_entrance("REGION_MAGMA_HIDEOUT_1F/ENTRANCE -> REGION_MAGMA_HIDEOUT_1F/MAIN", player),
        can_strength
    )
    set_rule(
        multiworld.get_entrance("REGION_MAGMA_HIDEOUT_1F/MAIN -> REGION_MAGMA_HIDEOUT_1F/ENTRANCE", player),
        can_strength
    )

    # Route 124
    set_rule(
        multiworld.get_entrance("REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/BIG_AREA", player),
        can_dive
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/SMALL_AREA_1", player),
        can_dive
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/SMALL_AREA_2", player),
        can_dive
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/SMALL_AREA_3", player),
        can_dive
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/TUNNEL_1", player),
        can_dive
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/TUNNEL_2", player),
        can_dive
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/TUNNEL_3", player),
        can_dive
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/TUNNEL_4", player),
        can_dive
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE124/NORTH_ENCLOSED_AREA_1 -> REGION_UNDERWATER_ROUTE124/TUNNEL_1", player),
        can_dive
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE124/NORTH_ENCLOSED_AREA_2 -> REGION_UNDERWATER_ROUTE124/TUNNEL_1", player),
        can_dive
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE124/NORTH_ENCLOSED_AREA_3 -> REGION_UNDERWATER_ROUTE124/TUNNEL_2", player),
        can_dive
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE124/SOUTH_ENCLOSED_AREA_1 -> REGION_UNDERWATER_ROUTE124/TUNNEL_3", player),
        can_dive
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE124/SOUTH_ENCLOSED_AREA_2 -> REGION_UNDERWATER_ROUTE124/TUNNEL_3", player),
        can_dive
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE124/SOUTH_ENCLOSED_AREA_3 -> REGION_UNDERWATER_ROUTE124/TUNNEL_4", player),
        can_dive
    )

    # Mossdeep City
    set_rule(
        multiworld.get_entrance("REGION_MOSSDEEP_CITY/MAIN -> REGION_ROUTE124/MAIN", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_MOSSDEEP_CITY/MAIN -> REGION_ROUTE125/SEA", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_MOSSDEEP_CITY/MAIN -> REGION_ROUTE127/MAIN", player),
        can_surf
    )

    # Route 126
    set_rule(
        multiworld.get_entrance("REGION_ROUTE126/MAIN -> REGION_UNDERWATER_ROUTE126/MAIN", player),
        can_dive
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE126/MAIN -> REGION_UNDERWATER_ROUTE126/SMALL_AREA_2", player),
        can_dive
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE126/NEAR_ROUTE_124 -> REGION_UNDERWATER_ROUTE126/TUNNEL", player),
        can_dive
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE126/NORTH_WEST_CORNER -> REGION_UNDERWATER_ROUTE126/TUNNEL", player),
        can_dive
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE126/WEST -> REGION_UNDERWATER_ROUTE126/MAIN", player),
        can_dive
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE126/WEST -> REGION_UNDERWATER_ROUTE126/SMALL_AREA_1", player),
        can_dive
    )

    # Sootopolis City
    set_rule(
        multiworld.get_entrance("REGION_SOOTOPOLIS_CITY/MAIN -> REGION_UNDERWATER_SOOTOPOLIS_CITY/MAIN", player),
        can_dive
    )

    # Route 127
    set_rule(
        multiworld.get_entrance("REGION_ROUTE127/MAIN -> REGION_UNDERWATER_ROUTE127/TUNNEL", player),
        can_dive
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE127/MAIN -> REGION_UNDERWATER_ROUTE127/AREA_1", player),
        can_dive
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE127/MAIN -> REGION_UNDERWATER_ROUTE127/AREA_2", player),
        can_dive
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE127/MAIN -> REGION_UNDERWATER_ROUTE127/AREA_3", player),
        can_dive
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE127/ENCLOSED_AREA -> REGION_UNDERWATER_ROUTE127/TUNNEL", player),
        can_dive
    )

    # Route 128
    set_rule(
        multiworld.get_entrance("REGION_ROUTE128/MAIN -> REGION_UNDERWATER_ROUTE128/MAIN", player),
        can_dive
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE128/MAIN -> REGION_UNDERWATER_ROUTE128/AREA_1", player),
        can_dive
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE128/MAIN -> REGION_UNDERWATER_ROUTE128/AREA_2", player),
        can_dive
    )

    # Seafloor Cavern
    set_rule(
        multiworld.get_entrance("REGION_SEAFLOOR_CAVERN_ROOM1/SOUTH -> REGION_SEAFLOOR_CAVERN_ROOM1/NORTH", player),
        lambda state: can_rock_smash(state) and can_strength(state)
    )
    set_rule(
        multiworld.get_entrance("REGION_SEAFLOOR_CAVERN_ROOM1/NORTH -> REGION_SEAFLOOR_CAVERN_ROOM1/SOUTH", player),
        can_strength
    )
    set_rule(
        multiworld.get_entrance("REGION_SEAFLOOR_CAVERN_ROOM2/SOUTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM2/NORTH_WEST", player),
        can_strength
    )
    set_rule(
        multiworld.get_entrance("REGION_SEAFLOOR_CAVERN_ROOM2/NORTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM2/SOUTH_WEST", player),
        can_strength
    )
    set_rule(
        multiworld.get_entrance("REGION_SEAFLOOR_CAVERN_ROOM2/SOUTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM2/SOUTH_EAST", player),
        can_rock_smash
    )
    set_rule(
        multiworld.get_entrance("REGION_SEAFLOOR_CAVERN_ROOM2/SOUTH_EAST -> REGION_SEAFLOOR_CAVERN_ROOM2/SOUTH_WEST", player),
        can_rock_smash
    )
    set_rule(
        multiworld.get_entrance("REGION_SEAFLOOR_CAVERN_ROOM2/NORTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM2/NORTH_EAST", player),
        lambda state: can_rock_smash(state) and can_strength(state)
    )
    set_rule(
        multiworld.get_entrance("REGION_SEAFLOOR_CAVERN_ROOM2/NORTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM2/SOUTH_EAST", player),
        lambda state: can_rock_smash(state) and can_strength(state)
    )
    set_rule(
        multiworld.get_entrance("REGION_SEAFLOOR_CAVERN_ROOM5/NORTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM5/EAST", player),
        lambda state: can_rock_smash(state) and can_strength(state)
    )
    set_rule(
        multiworld.get_entrance("REGION_SEAFLOOR_CAVERN_ROOM5/EAST -> REGION_SEAFLOOR_CAVERN_ROOM5/NORTH_WEST", player),
        can_strength
    )
    set_rule(
        multiworld.get_entrance("REGION_SEAFLOOR_CAVERN_ROOM5/NORTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM5/SOUTH_WEST", player),
        lambda state: can_rock_smash(state) and can_strength(state)
    )
    set_rule(
        multiworld.get_entrance("REGION_SEAFLOOR_CAVERN_ROOM5/SOUTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM5/NORTH_WEST", player),
        lambda state: can_rock_smash(state) and can_strength(state)
    )
    set_rule(
        multiworld.get_entrance("REGION_SEAFLOOR_CAVERN_ROOM6/NORTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM6/CAVE_ON_WATER", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_SEAFLOOR_CAVERN_ROOM6/SOUTH -> REGION_SEAFLOOR_CAVERN_ROOM6/NORTH_WEST", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_SEAFLOOR_CAVERN_ROOM6/SOUTH -> REGION_SEAFLOOR_CAVERN_ROOM6/CAVE_ON_WATER", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_SEAFLOOR_CAVERN_ROOM7/SOUTH -> REGION_SEAFLOOR_CAVERN_ROOM7/NORTH", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_SEAFLOOR_CAVERN_ROOM7/NORTH -> REGION_SEAFLOOR_CAVERN_ROOM7/SOUTH", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_SEAFLOOR_CAVERN_ROOM8/NORTH -> REGION_SEAFLOOR_CAVERN_ROOM8/SOUTH", player),
        can_strength
    )
    set_rule(
        multiworld.get_entrance("REGION_SEAFLOOR_CAVERN_ROOM8/SOUTH -> REGION_SEAFLOOR_CAVERN_ROOM8/NORTH", player),
        can_strength
    )

    # Pacifidlog Town
    set_rule(
        multiworld.get_entrance("REGION_PACIFIDLOG_TOWN/MAIN -> REGION_ROUTE131/MAIN", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_PACIFIDLOG_TOWN/MAIN -> REGION_ROUTE132/EAST", player),
        can_surf
    )

    # Sky Pillar
    set_rule(
        multiworld.get_entrance("REGION_SKY_PILLAR_2F/RIGHT -> REGION_SKY_PILLAR_2F/LEFT", player),
        lambda state: _can_use_mach_bike(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_SKY_PILLAR_2F/LEFT -> REGION_SKY_PILLAR_2F/RIGHT", player),
        lambda state: _can_use_mach_bike(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_SKY_PILLAR_4F/MAIN -> REGION_SKY_PILLAR_4F/ABOVE_3F_TOP_CENTER", player),
        lambda state: _can_use_mach_bike(state, player)
    )

    # Route 134
    set_rule(
        multiworld.get_entrance("REGION_ROUTE134/MAIN -> REGION_UNDERWATER_ROUTE134/MAIN", player),
        can_dive
    )

    # Ever Grande City
    set_rule(
        multiworld.get_entrance("REGION_EVER_GRANDE_CITY/SEA -> REGION_EVER_GRANDE_CITY/SOUTH", player),
        can_waterfall
    )
    set_rule(
        multiworld.get_entrance("REGION_EVER_GRANDE_CITY/SOUTH -> REGION_EVER_GRANDE_CITY/SEA", player),
        lambda state: can_surf(state) and can_waterfall(state)
    )

    # Victory Road
    set_rule(
        multiworld.get_entrance("REGION_VICTORY_ROAD_B1F/SOUTH_WEST_MAIN -> REGION_VICTORY_ROAD_B1F/SOUTH_WEST_LADDER_UP", player),
        lambda state: can_rock_smash(state) and can_strength(state)
    )
    set_rule(
        multiworld.get_entrance("REGION_VICTORY_ROAD_B1F/SOUTH_WEST_LADDER_UP -> REGION_VICTORY_ROAD_B1F/SOUTH_WEST_MAIN", player),
        lambda state: can_rock_smash(state) and can_strength(state)
    )
    set_rule(
        multiworld.get_entrance("REGION_VICTORY_ROAD_B1F/MAIN_UPPER -> REGION_VICTORY_ROAD_B1F/MAIN_LOWER_EAST", player),
        lambda state: can_rock_smash(state) and can_strength(state)
    )
    set_rule(
        multiworld.get_entrance("REGION_VICTORY_ROAD_B1F/MAIN_LOWER_EAST -> REGION_VICTORY_ROAD_B1F/MAIN_LOWER_WEST", player),
        can_rock_smash
    )
    set_rule(
        multiworld.get_entrance("REGION_VICTORY_ROAD_B1F/MAIN_LOWER_WEST -> REGION_VICTORY_ROAD_B1F/MAIN_LOWER_EAST", player),
        lambda state: can_rock_smash(state) and can_strength(state)
    )
    set_rule(
        multiworld.get_entrance("REGION_VICTORY_ROAD_B1F/MAIN_LOWER_WEST -> REGION_VICTORY_ROAD_B1F/MAIN_UPPER", player),
        lambda state: can_rock_smash(state) and can_strength(state)
    )
    set_rule(
        multiworld.get_location(name_to_label("ITEM_VICTORY_ROAD_B1F_FULL_RESTORE"), player),
        lambda state: can_rock_smash(state) and can_strength(state)
    )
    set_rule(
        multiworld.get_entrance("REGION_VICTORY_ROAD_B2F/LOWER_WEST -> REGION_VICTORY_ROAD_B2F/LOWER_WEST_WATER", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_VICTORY_ROAD_B2F/LOWER_WEST_ISLAND -> REGION_VICTORY_ROAD_B2F/LOWER_WEST_WATER", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_VICTORY_ROAD_B2F/LOWER_EAST -> REGION_VICTORY_ROAD_B2F/LOWER_EAST_WATER", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_VICTORY_ROAD_B2F/LOWER_WEST_WATER -> REGION_VICTORY_ROAD_B2F/UPPER_WATER", player),
        can_waterfall
    )
    set_rule(
        multiworld.get_entrance("REGION_VICTORY_ROAD_B2F/LOWER_EAST_WATER -> REGION_VICTORY_ROAD_B2F/UPPER_WATER", player),
        can_waterfall
    )
    set_rule(
        multiworld.get_entrance("REGION_VICTORY_ROAD_B2F/UPPER -> REGION_VICTORY_ROAD_B2F/UPPER_WATER", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_VICTORY_ROAD_B2F/UPPER -> REGION_VICTORY_ROAD_B2F/LOWER_EAST_WATER", player),
        can_surf
    )

    # Pokemon League
    set_rule(
        multiworld.get_entrance("REGION_EVER_GRANDE_CITY_POKEMON_LEAGUE_1F/MAIN -> REGION_EVER_GRANDE_CITY_POKEMON_LEAGUE_1F/BEHIND_BADGE_CHECKERS", player),
        lambda state: _has_at_least_n_badges(state, player, 8)
    )
