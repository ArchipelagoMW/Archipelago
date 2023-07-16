"""
Logic rule definitions for Pokemon Emerald
"""
from BaseClasses import CollectionState, MultiWorld
from Options import Toggle

from worlds.generic.Rules import add_rule, set_rule

from .options import EliteFourRequirement, NormanRequirement, ExtraBoulders
from .util import location_name_to_label


def _can_cut(state: CollectionState, player: int):
    return state.has("HM01 Cut", player) and state.has("Stone Badge", player)


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
    return state.has("Mach Bike", player)


def _can_use_acro_bike(state: CollectionState, player: int):
    return state.has("Acro Bike", player)


def _defeated_n_gym_leaders(state: CollectionState, player: int, n: int):
    num_gym_leaders_defeated = 0
    num_gym_leaders_defeated += 1 if state.has("EVENT_DEFEAT_ROXANNE", player) else 0
    num_gym_leaders_defeated += 1 if state.has("EVENT_DEFEAT_BRAWLY", player) else 0
    num_gym_leaders_defeated += 1 if state.has("EVENT_DEFEAT_WATTSON", player) else 0
    num_gym_leaders_defeated += 1 if state.has("EVENT_DEFEAT_FLANNERY", player) else 0
    num_gym_leaders_defeated += 1 if state.has("EVENT_DEFEAT_NORMAN", player) else 0
    num_gym_leaders_defeated += 1 if state.has("EVENT_DEFEAT_WINONA", player) else 0
    num_gym_leaders_defeated += 1 if state.has("EVENT_DEFEAT_TATE_AND_LIZA", player) else 0
    num_gym_leaders_defeated += 1 if state.has("EVENT_DEFEAT_JUAN", player) else 0
    return num_gym_leaders_defeated >= n


# Rules are organized by town/route/dungeon and ordered approximately
# by when you would first reach that place in a vanilla playthrough.
def set_default_rules(multiworld: MultiWorld, player: int):
    can_cut = lambda state: _can_cut(state, player)
    can_surf = lambda state: _can_surf(state, player)
    can_strength = lambda state: _can_strength(state, player)
    can_rock_smash = lambda state: _can_rock_smash(state, player)
    can_waterfall = lambda state: _can_waterfall(state, player)
    can_dive = lambda state: _can_dive(state, player)

    # Sky
    if multiworld.fly_without_badge[player] == Toggle.option_true:
        set_rule(
            multiworld.get_entrance("REGION_LITTLEROOT_TOWN/MAIN -> REGION_SKY", player),
            lambda state: state.has("HM02 Fly", player)
        )
    else:
        set_rule(
            multiworld.get_entrance("REGION_LITTLEROOT_TOWN/MAIN -> REGION_SKY", player),
            lambda state: state.has("HM02 Fly", player) and state.has("Feather Badge", player)
        )
    set_rule(
        multiworld.get_entrance("REGION_SKY -> REGION_LITTLEROOT_TOWN/MAIN", player),
        lambda state: state.has("EVENT_VISITED_LITTLEROOT_TOWN", player)
    )
    set_rule(
        multiworld.get_entrance("REGION_SKY -> REGION_OLDALE_TOWN/MAIN", player),
        lambda state: state.has("EVENT_VISITED_OLDALE_TOWN", player)
    )
    set_rule(
        multiworld.get_entrance("REGION_SKY -> REGION_PETALBURG_CITY/MAIN", player),
        lambda state: state.has("EVENT_VISITED_PETALBURG_CITY", player)
    )
    set_rule(
        multiworld.get_entrance("REGION_SKY -> REGION_RUSTBORO_CITY/MAIN", player),
        lambda state: state.has("EVENT_VISITED_RUSTBORO_CITY", player)
    )
    set_rule(
        multiworld.get_entrance("REGION_SKY -> REGION_DEWFORD_TOWN/MAIN", player),
        lambda state: state.has("EVENT_VISITED_DEWFORD_TOWN", player)
    )
    set_rule(
        multiworld.get_entrance("REGION_SKY -> REGION_SLATEPORT_CITY/MAIN", player),
        lambda state: state.has("EVENT_VISITED_SLATEPORT_CITY", player)
    )
    set_rule(
        multiworld.get_entrance("REGION_SKY -> REGION_MAUVILLE_CITY/MAIN", player),
        lambda state: state.has("EVENT_VISITED_MAUVILLE_CITY", player)
    )
    set_rule(
        multiworld.get_entrance("REGION_SKY -> REGION_VERDANTURF_TOWN/MAIN", player),
        lambda state: state.has("EVENT_VISITED_VERDANTURF_TOWN", player)
    )
    set_rule(
        multiworld.get_entrance("REGION_SKY -> REGION_FALLARBOR_TOWN/MAIN", player),
        lambda state: state.has("EVENT_VISITED_FALLARBOR_TOWN", player)
    )
    set_rule(
        multiworld.get_entrance("REGION_SKY -> REGION_LAVARIDGE_TOWN/MAIN", player),
        lambda state: state.has("EVENT_VISITED_LAVARIDGE_TOWN", player)
    )
    set_rule(
        multiworld.get_entrance("REGION_SKY -> REGION_FORTREE_CITY/MAIN", player),
        lambda state: state.has("EVENT_VISITED_FORTREE_CITY", player)
    )
    set_rule(
        multiworld.get_entrance("REGION_SKY -> REGION_LILYCOVE_CITY/MAIN", player),
        lambda state: state.has("EVENT_VISITED_LILYCOVE_CITY", player)
    )
    set_rule(
        multiworld.get_entrance("REGION_SKY -> REGION_MOSSDEEP_CITY/MAIN", player),
        lambda state: state.has("EVENT_VISITED_MOSSDEEP_CITY", player)
    )
    set_rule(
        multiworld.get_entrance("REGION_SKY -> REGION_SOOTOPOLIS_CITY/EAST", player),
        lambda state: state.has("EVENT_VISITED_SOOTOPOLIS_CITY", player)
    )
    set_rule(
        multiworld.get_entrance("REGION_SKY -> REGION_EVER_GRANDE_CITY/SOUTH", player),
        lambda state: state.has("EVENT_VISITED_EVER_GRANDE_CITY", player)
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
        multiworld.get_location(location_name_to_label("NPC_GIFT_RECEIVED_HM03"), player),
        lambda state: state.has("EVENT_DEFEAT_NORMAN", player)
    )
    if multiworld.norman_requirement[player].value == NormanRequirement.option_badges:
        set_rule(
            multiworld.get_entrance("MAP_PETALBURG_CITY_GYM:2/MAP_PETALBURG_CITY_GYM:3", player),
            lambda state: state.has_group("Badge", player, multiworld.norman_count[player].value)
        )
        set_rule(
            multiworld.get_entrance("MAP_PETALBURG_CITY_GYM:5/MAP_PETALBURG_CITY_GYM:6", player),
            lambda state: state.has_group("Badge", player, multiworld.norman_count[player].value)
        )
    else:
        set_rule(
            multiworld.get_entrance("MAP_PETALBURG_CITY_GYM:2/MAP_PETALBURG_CITY_GYM:3", player),
            lambda state: _defeated_n_gym_leaders(state, player, multiworld.norman_count[player].value)
        )
        set_rule(
            multiworld.get_entrance("MAP_PETALBURG_CITY_GYM:5/MAP_PETALBURG_CITY_GYM:6", player),
            lambda state: _defeated_n_gym_leaders(state, player, multiworld.norman_count[player].value)
        )

    # Route 104
    set_rule(
        multiworld.get_entrance("REGION_ROUTE104/SOUTH -> REGION_ROUTE105/MAIN", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE104_MR_BRINEYS_HOUSE/MAIN -> REGION_DEWFORD_TOWN/MAIN", player),
        lambda state: state.has("EVENT_TALK_TO_MR_STONE", player)
    )

    # Petalburg Woods
    set_rule(
        multiworld.get_entrance("REGION_PETALBURG_WOODS/WEST_PATH -> REGION_PETALBURG_WOODS/EAST_PATH", player),
        can_cut
    )

    # Rustboro City
    set_rule(
        multiworld.get_location("EVENT_RETURN_DEVON_GOODS", player),
        lambda state: state.has("EVENT_RECOVER_DEVON_GOODS", player)
    )

    # Devon Corp
    set_rule(
        multiworld.get_entrance("MAP_RUSTBORO_CITY_DEVON_CORP_1F:2/MAP_RUSTBORO_CITY_DEVON_CORP_2F:0", player),
        lambda state: state.has("EVENT_RETURN_DEVON_GOODS", player)
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
    set_rule(
        multiworld.get_location(location_name_to_label("NPC_GIFT_RECEIVED_HM04"), player),
        can_rock_smash
    )
    set_rule(
        multiworld.get_location("EVENT_RECOVER_DEVON_GOODS", player),
        lambda state: state.has("EVENT_DEFEAT_ROXANNE", player)
    )

    # Route 115
    set_rule(
        multiworld.get_entrance("REGION_ROUTE115/SOUTH_BELOW_LEDGE -> REGION_ROUTE115/SEA", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE115/SOUTH_BEACH_NEAR_CAVE -> REGION_ROUTE115/SEA", player),
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
    if multiworld.extra_boulders[player].value == ExtraBoulders.option_true:
        set_rule(
            multiworld.get_entrance("REGION_ROUTE115/SOUTH_BEACH_NEAR_CAVE -> REGION_ROUTE115/SOUTH_ABOVE_LEDGE", player),
            can_strength
        )
        set_rule(
            multiworld.get_entrance("REGION_ROUTE115/SOUTH_ABOVE_LEDGE -> REGION_ROUTE115/SOUTH_BEACH_NEAR_CAVE", player),
            can_strength
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

    # Dewford Town
    set_rule(
        multiworld.get_entrance("REGION_DEWFORD_TOWN/MAIN -> REGION_ROUTE109/BEACH", player),
        lambda state:
            state.can_reach("REGION_ROUTE104_MR_BRINEYS_HOUSE/MAIN -> REGION_DEWFORD_TOWN/MAIN", "Entrance", player)
            and state.has("EVENT_TALK_TO_MR_STONE", player)
            and state.has("EVENT_DELIVER_LETTER", player)
    )
    set_rule(
        multiworld.get_entrance("REGION_DEWFORD_TOWN/MAIN -> REGION_ROUTE104_MR_BRINEYS_HOUSE/MAIN", player),
        lambda state:
            state.can_reach("REGION_ROUTE104_MR_BRINEYS_HOUSE/MAIN -> REGION_DEWFORD_TOWN/MAIN", "Entrance", player)
            and state.has("EVENT_TALK_TO_MR_STONE", player)
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

    # Route 107
    set_rule(
        multiworld.get_entrance("REGION_DEWFORD_TOWN/MAIN -> REGION_ROUTE107/MAIN", player),
        can_surf
    )

    # Route 109
    set_rule(
        multiworld.get_entrance("REGION_ROUTE109/BEACH -> REGION_DEWFORD_TOWN/MAIN", player),
        lambda state:
            state.can_reach("REGION_ROUTE104_MR_BRINEYS_HOUSE/MAIN -> REGION_DEWFORD_TOWN/MAIN", "Entrance", player)
            and state.can_reach("REGION_DEWFORD_TOWN/MAIN -> REGION_ROUTE109/BEACH", "Entrance", player)
            and state.has("EVENT_TALK_TO_MR_STONE", player)
            and state.has("EVENT_DELIVER_LETTER", player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE109/BEACH -> REGION_ROUTE109/SEA", player),
        can_surf
    )

    # Slateport City
    set_rule(
        multiworld.get_entrance("REGION_SLATEPORT_CITY/MAIN -> REGION_ROUTE134/WEST", player),
        can_surf
    )
    set_rule(
        multiworld.get_location("EVENT_TALK_TO_DOCK", player),
        lambda state: state.has("Devon Goods", player)
    )
    set_rule(
        multiworld.get_entrance("MAP_SLATEPORT_CITY:5,7/MAP_SLATEPORT_CITY_OCEANIC_MUSEUM_1F:0,1", player),
        lambda state: state.has("EVENT_TALK_TO_DOCK", player)
    )
    set_rule(
        multiworld.get_location("EVENT_AQUA_STEALS_SUBMARINE", player),
        lambda state: state.has("EVENT_RELEASE_GROUDON", player)
    )
    set_rule(
        multiworld.get_entrance("REGION_SLATEPORT_CITY_HARBOR/MAIN -> REGION_SS_TIDAL_CORRIDOR/MAIN", player),
        lambda state: state.has("EVENT_DEFEAT_CHAMPION", player)
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
    set_rule(
        multiworld.get_entrance("REGION_ROUTE110_SEASIDE_CYCLING_ROAD_SOUTH_ENTRANCE/WEST -> REGION_ROUTE110_SEASIDE_CYCLING_ROAD_SOUTH_ENTRANCE/EAST", player),
        lambda state: _can_use_acro_bike(state, player) or _can_use_mach_bike(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE110_SEASIDE_CYCLING_ROAD_NORTH_ENTRANCE/WEST -> REGION_ROUTE110_SEASIDE_CYCLING_ROAD_NORTH_ENTRANCE/EAST", player),
        lambda state: _can_use_acro_bike(state, player) or _can_use_mach_bike(state, player)
    )
    if "Route 110 Aqua Grunts" not in multiworld.remove_roadblocks[player].value:
        set_rule(
            multiworld.get_entrance("REGION_ROUTE110/SOUTH -> REGION_ROUTE110/MAIN", player),
            lambda state: state.has("EVENT_RESCUE_CAPT_STERN", player)
        )
        set_rule(
            multiworld.get_entrance("REGION_ROUTE110/MAIN -> REGION_ROUTE110/SOUTH", player),
            lambda state: state.has("EVENT_RESCUE_CAPT_STERN", player)
        )

    # Mauville City
    set_rule(
        multiworld.get_location(location_name_to_label("NPC_GIFT_GOT_BASEMENT_KEY_FROM_WATTSON"), player),
        lambda state: state.has("EVENT_DEFEAT_NORMAN", player)
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
    set_rule(
        multiworld.get_entrance("MAP_ROUTE111:4/MAP_TRAINER_HILL_ENTRANCE:0", player),
        lambda state: state.has("EVENT_DEFEAT_CHAMPION", player)
    )

    # Route 112
    if "Route 112 Magma Grunts" not in multiworld.remove_roadblocks[player].value:
        set_rule(
            multiworld.get_entrance("REGION_ROUTE112/SOUTH_EAST -> REGION_ROUTE112/CABLE_CAR_STATION_ENTRANCE", player),
            lambda state: state.has("EVENT_MAGMA_STEALS_METEORITE", player)
        )
        set_rule(
            multiworld.get_entrance("REGION_ROUTE112/CABLE_CAR_STATION_ENTRANCE -> REGION_ROUTE112/SOUTH_EAST", player),
            lambda state: state.has("EVENT_MAGMA_STEALS_METEORITE", player)
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
        multiworld.get_entrance("MAP_ROUTE114_FOSSIL_MANIACS_TUNNEL:2/MAP_DESERT_UNDERPASS:0", player),
        lambda state: state.has("EVENT_DEFEAT_CHAMPION", player)
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
        multiworld.get_entrance("MAP_METEOR_FALLS_1F_1R:5/MAP_METEOR_FALLS_STEVENS_CAVE:0", player),
        lambda state: state.has("EVENT_DEFEAT_CHAMPION", player)
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
    set_rule(
        multiworld.get_entrance("MAP_JAGGED_PASS:4/MAP_MAGMA_HIDEOUT_1F:0", player),
        lambda state: state.has("Magma Emblem", player)
    )

    # Lavaridge Town
    set_rule(
        multiworld.get_location(location_name_to_label("NPC_GIFT_RECEIVED_GO_GOGGLES"), player),
        lambda state: state.has("EVENT_DEFEAT_FLANNERY", player)
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
        multiworld.get_entrance("MAP_ABANDONED_SHIP_HIDDEN_FLOOR_CORRIDORS:0/MAP_ABANDONED_SHIP_HIDDEN_FLOOR_ROOMS:0", player),
        lambda state: state.has("Room 1 Key", player)
    )
    set_rule(
        multiworld.get_entrance("MAP_ABANDONED_SHIP_HIDDEN_FLOOR_CORRIDORS:1/MAP_ABANDONED_SHIP_HIDDEN_FLOOR_ROOMS:2", player),
        lambda state: state.has("Room 2 Key", player)
    )
    set_rule(
        multiworld.get_entrance("MAP_ABANDONED_SHIP_HIDDEN_FLOOR_CORRIDORS:3/MAP_ABANDONED_SHIP_HIDDEN_FLOOR_ROOMS:6", player),
        lambda state: state.has("Room 4 Key", player)
    )
    set_rule(
        multiworld.get_entrance("MAP_ABANDONED_SHIP_HIDDEN_FLOOR_CORRIDORS:5/MAP_ABANDONED_SHIP_HIDDEN_FLOOR_ROOMS:8", player),
        lambda state: state.has("Room 6 Key", player)
    )
    set_rule(
        multiworld.get_entrance("MAP_ABANDONED_SHIP_CORRIDORS_B1F:5/MAP_ABANDONED_SHIP_ROOM_B1F:0", player),
        lambda state: state.has("Storage Key", player)
    )

    # New Mauville
    set_rule(
        multiworld.get_entrance("MAP_NEW_MAUVILLE_ENTRANCE:1/MAP_NEW_MAUVILLE_INSIDE:0", player),
        lambda state: state.has("Basement Key", player)
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
        multiworld.get_entrance("REGION_ROUTE119/LOWER -> REGION_ROUTE119/LOWER_ACROSS_WATER", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE119/LOWER_ACROSS_WATER -> REGION_ROUTE119/LOWER", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE119/LOWER -> REGION_ROUTE119/LOWER_ACROSS_RAILS", player),
        lambda state: _can_use_acro_bike(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE119/LOWER_ACROSS_RAILS -> REGION_ROUTE119/LOWER", player),
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
    if "Route 119 Aqua Grunts" not in multiworld.remove_roadblocks[player].value:
        set_rule(
            multiworld.get_entrance("REGION_ROUTE119/MIDDLE -> REGION_ROUTE119/UPPER", player),
            lambda state: state.has("EVENT_DEFEAT_SHELLY", player)
        )
        set_rule(
            multiworld.get_entrance("REGION_ROUTE119/UPPER -> REGION_ROUTE119/MIDDLE", player),
            lambda state: state.has("EVENT_DEFEAT_SHELLY", player)
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

    # Route 120
    set_rule(
        multiworld.get_entrance("REGION_ROUTE120/NORTH -> REGION_ROUTE120/NORTH_POND", player),
        lambda state: state.has("Devon Scope", player)
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE120/NORTH_POND -> REGION_ROUTE120/NORTH", player),
        lambda state: state.has("Devon Scope", player)
    )

    # Route 121
    set_rule(
        multiworld.get_entrance("REGION_ROUTE121/EAST -> REGION_ROUTE121/WEST", player),
        can_cut
    )
    set_rule(
        multiworld.get_entrance("REGION_ROUTE121/EAST -> REGION_ROUTE122/SEA", player),
        can_surf
    )

    # Safari Zone
    set_rule(
        multiworld.get_entrance("MAP_ROUTE121_SAFARI_ZONE_ENTRANCE:0,1/MAP_SAFARI_ZONE_SOUTH:0", player),
        lambda state: state.has("Pokeblock Case", player)
    )
    set_rule(
        multiworld.get_entrance("REGION_SAFARI_ZONE_SOUTH/MAIN -> REGION_SAFARI_ZONE_NORTH/MAIN", player),
        lambda state: _can_use_acro_bike(state, player)
    )
    set_rule(
        multiworld.get_entrance("REGION_SAFARI_ZONE_SOUTHWEST/MAIN -> REGION_SAFARI_ZONE_NORTHWEST/MAIN", player),
        lambda state: _can_use_mach_bike(state, player)
    )
    if "Safari Zone Construction Workers" not in multiworld.remove_roadblocks[player].value:
        set_rule(
            multiworld.get_entrance("REGION_SAFARI_ZONE_SOUTH/MAIN -> REGION_SAFARI_ZONE_SOUTHEAST/MAIN", player),
            lambda state: state.has("EVENT_DEFEAT_CHAMPION", player)
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
    set_rule(
        multiworld.get_entrance("REGION_LILYCOVE_CITY_HARBOR/MAIN -> REGION_SS_TIDAL_CORRIDOR/MAIN", player),
        lambda state: state.has("EVENT_DEFEAT_CHAMPION", player)
    )
    if "Lilycove City Wailmer" not in multiworld.remove_roadblocks[player].value:
        set_rule(
            multiworld.get_entrance("REGION_LILYCOVE_CITY/SEA -> REGION_ROUTE124/MAIN", player),
            lambda state: state.has("EVENT_CLEAR_AQUA_HIDEOUT", player)
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

    # Aqua Hideout
    if "Aqua Hideout Grunts" not in multiworld.remove_roadblocks[player].value:
        set_rule(
            multiworld.get_entrance("REGION_AQUA_HIDEOUT_1F/WATER -> REGION_AQUA_HIDEOUT_1F/MAIN", player),
            lambda state: state.has("EVENT_AQUA_STEALS_SUBMARINE", player)
        )
        set_rule(
            multiworld.get_entrance("REGION_AQUA_HIDEOUT_1F/MAIN -> REGION_AQUA_HIDEOUT_1F/WATER", player),
            lambda state: can_surf(state) and state.has("EVENT_AQUA_STEALS_SUBMARINE", player)
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
    set_rule(
        multiworld.get_location("EVENT_DEFEAT_MAXIE_AT_SPACE_STATION", player),
        lambda state: state.has("EVENT_DEFEAT_TATE_AND_LIZA", player)
    )
    set_rule(
        multiworld.get_location("EVENT_STEVEN_GIVES_DIVE", player),
        lambda state: state.has("EVENT_DEFEAT_MAXIE_AT_SPACE_STATION", player)
    )
    set_rule(
        multiworld.get_location(location_name_to_label("NPC_GIFT_RECEIVED_HM08"), player),
        lambda state: state.has("EVENT_DEFEAT_MAXIE_AT_SPACE_STATION", player)
    )

    # Shoal Cave
    set_rule(
        multiworld.get_entrance("REGION_SHOAL_CAVE_ENTRANCE_ROOM/SOUTH -> REGION_SHOAL_CAVE_ENTRANCE_ROOM/HIGH_TIDE_WATER", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_SHOAL_CAVE_ENTRANCE_ROOM/NORTH_WEST_CORNER -> REGION_SHOAL_CAVE_ENTRANCE_ROOM/HIGH_TIDE_WATER", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_SHOAL_CAVE_ENTRANCE_ROOM/NORTH_EAST_CORNER -> REGION_SHOAL_CAVE_ENTRANCE_ROOM/HIGH_TIDE_WATER", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_SHOAL_CAVE_INNER_ROOM/HIGH_TIDE_EAST_MIDDLE_GROUND -> REGION_SHOAL_CAVE_INNER_ROOM/SOUTH_EAST_WATER", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_SHOAL_CAVE_INNER_ROOM/HIGH_TIDE_EAST_MIDDLE_GROUND -> REGION_SHOAL_CAVE_INNER_ROOM/EAST_WATER", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_SHOAL_CAVE_INNER_ROOM/HIGH_TIDE_EAST_MIDDLE_GROUND -> REGION_SHOAL_CAVE_INNER_ROOM/NORTH_WEST_WATER", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_SHOAL_CAVE_INNER_ROOM/SOUTH_WEST_CORNER -> REGION_SHOAL_CAVE_INNER_ROOM/NORTH_WEST_WATER", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_SHOAL_CAVE_INNER_ROOM/RARE_CANDY_PLATFORM -> REGION_SHOAL_CAVE_INNER_ROOM/SOUTH_EAST_WATER", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_SHOAL_CAVE_LOW_TIDE_LOWER_ROOM/NORTH_WEST -> REGION_SHOAL_CAVE_LOW_TIDE_LOWER_ROOM/EAST", player),
        can_strength
    )
    set_rule(
        multiworld.get_entrance("REGION_SHOAL_CAVE_LOW_TIDE_LOWER_ROOM/EAST -> REGION_SHOAL_CAVE_LOW_TIDE_LOWER_ROOM/NORTH_WEST", player),
        can_strength
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
        multiworld.get_entrance("REGION_SOOTOPOLIS_CITY/WATER -> REGION_UNDERWATER_SOOTOPOLIS_CITY/MAIN", player),
        can_dive
    )
    set_rule(
        multiworld.get_entrance("REGION_SOOTOPOLIS_CITY/EAST -> REGION_SOOTOPOLIS_CITY/WATER", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_SOOTOPOLIS_CITY/WEST -> REGION_SOOTOPOLIS_CITY/WATER", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("REGION_SOOTOPOLIS_CITY/ISLAND -> REGION_SOOTOPOLIS_CITY/WATER", player),
        can_surf
    )
    set_rule(
        multiworld.get_entrance("MAP_SOOTOPOLIS_CITY:3/MAP_CAVE_OF_ORIGIN_ENTRANCE:0", player),
        lambda state: state.has("EVENT_RELEASE_KYOGRE", player)
    )
    set_rule(
        multiworld.get_entrance("MAP_SOOTOPOLIS_CITY:2/MAP_SOOTOPOLIS_CITY_GYM_1F:0", player),
        lambda state: state.has("EVENT_WAKE_RAYQUAZA", player)
    )
    set_rule(
        multiworld.get_location(location_name_to_label("NPC_GIFT_RECEIVED_HM07"), player),
        lambda state: state.has("EVENT_WAKE_RAYQUAZA", player)
    )

    # Route 127
    set_rule(
        multiworld.get_entrance("REGION_ROUTE127/MAIN -> REGION_UNDERWATER_ROUTE127/MAIN", player),
        can_dive
    )
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
    if "Seafloor Cavern Aqua Grunt" not in multiworld.remove_roadblocks[player].value:
        set_rule(
            multiworld.get_entrance("MAP_SEAFLOOR_CAVERN_ENTRANCE:1/MAP_SEAFLOOR_CAVERN_ROOM1:0", player),
            lambda state: state.has("EVENT_STEVEN_GIVES_DIVE", player)
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
        multiworld.get_entrance("MAP_SKY_PILLAR_OUTSIDE:1/MAP_SKY_PILLAR_1F:0", player),
        lambda state: state.has("EVENT_WALLACE_GOES_TO_SKY_PILLAR", player)
    )
    # Sky Pillar does not require the mach bike until Rayquaza returns, which means the top
    # is only logically locked behind the mach bike after the top has been reached already
    # set_rule(
    #     multiworld.get_entrance("REGION_SKY_PILLAR_2F/RIGHT -> REGION_SKY_PILLAR_2F/LEFT", player),
    #     lambda state: _can_use_mach_bike(state, player)
    # )
    # set_rule(
    #     multiworld.get_entrance("REGION_SKY_PILLAR_2F/LEFT -> REGION_SKY_PILLAR_2F/RIGHT", player),
    #     lambda state: _can_use_mach_bike(state, player)
    # )
    # set_rule(
    #     multiworld.get_entrance("REGION_SKY_PILLAR_4F/MAIN -> REGION_SKY_PILLAR_4F/ABOVE_3F_TOP_CENTER", player),
    #     lambda state: _can_use_mach_bike(state, player)
    # )

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
        can_surf
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
    if multiworld.elite_four_requirement[player].value == EliteFourRequirement.option_badges:
        set_rule(
            multiworld.get_entrance("REGION_EVER_GRANDE_CITY_POKEMON_LEAGUE_1F/MAIN -> REGION_EVER_GRANDE_CITY_POKEMON_LEAGUE_1F/BEHIND_BADGE_CHECKERS", player),
            lambda state: state.has_group("Badge", player, multiworld.elite_four_count[player].value)
        )
    else:
        set_rule(
            multiworld.get_entrance("REGION_EVER_GRANDE_CITY_POKEMON_LEAGUE_1F/MAIN -> REGION_EVER_GRANDE_CITY_POKEMON_LEAGUE_1F/BEHIND_BADGE_CHECKERS", player),
            lambda state: _defeated_n_gym_leaders(state, player, multiworld.elite_four_count[player].value)
        )

    # Battle Frontier
    # set_rule(
    #     multiworld.get_entrance("REGION_BATTLE_FRONTIER_OUTSIDE_WEST/DOCK -> REGION_LILYCOVE_CITY_HARBOR/MAIN", player),
    #     lambda state: state.has("S.S. Ticket", player) and
    #         (state.has("EVENT_DEFEAT_CHAMPION", player) or multiworld.enable_ferry[player].value == Toggle.option_true)
    # )
    # set_rule(
    #     multiworld.get_entrance("REGION_BATTLE_FRONTIER_OUTSIDE_WEST/DOCK -> REGION_SLATEPORT_CITY_HARBOR/MAIN", player),
    #     lambda state: state.has("S.S. Ticket", player) and
    #         (state.has("EVENT_DEFEAT_CHAMPION", player) or multiworld.enable_ferry[player].value == Toggle.option_true)
    # )
    # set_rule(
    #     multiworld.get_entrance("REGION_BATTLE_FRONTIER_OUTSIDE_WEST/CAVE_ENTRANCE -> REGION_BATTLE_FRONTIER_OUTSIDE_WEST/WATER", player),
    #     can_surf
    # )
    # set_rule(
    #     multiworld.get_entrance("REGION_BATTLE_FRONTIER_OUTSIDE_EAST/MAIN -> REGION_BATTLE_FRONTIER_OUTSIDE_EAST/ABOVE_WATERFALL", player),
    #     lambda state: state.has("Wailmer Pail", player) and can_surf(state)
    # )
    # set_rule(
    #     multiworld.get_entrance("REGION_BATTLE_FRONTIER_OUTSIDE_EAST/ABOVE_WATERFALL -> REGION_BATTLE_FRONTIER_OUTSIDE_EAST/MAIN", player),
    #     lambda state: state.has("ITEM_WAILMER_PAIL", player)
    # )
    # set_rule(
    #     multiworld.get_entrance("REGION_BATTLE_FRONTIER_OUTSIDE_EAST/WATER -> REGION_BATTLE_FRONTIER_OUTSIDE_EAST/ABOVE_WATERFALL", player),
    #     can_waterfall
    # )


def set_overworld_item_rules(multiworld: MultiWorld, player: int):
    can_cut = lambda state: _can_cut(state, player)
    can_surf = lambda state: _can_surf(state, player)
    can_strength = lambda state: _can_strength(state, player)
    can_rock_smash = lambda state: _can_rock_smash(state, player)

    # Route 103
    set_rule(
        multiworld.get_location(location_name_to_label("ITEM_ROUTE_103_PP_UP"), player),
        can_cut
    )
    set_rule(
        multiworld.get_location(location_name_to_label("ITEM_ROUTE_103_GUARD_SPEC"), player),
        can_cut
    )

    # Route 104
    set_rule(
        multiworld.get_location(location_name_to_label("ITEM_ROUTE_104_X_ACCURACY"), player),
        lambda state: can_surf(state) or can_cut(state)
    )
    set_rule(
        multiworld.get_location(location_name_to_label("ITEM_ROUTE_104_PP_UP"), player),
        can_surf
    )

    # Route 117
    set_rule(
        multiworld.get_location(location_name_to_label("ITEM_ROUTE_117_REVIVE"), player),
        can_cut
    )

    # Route 114
    set_rule(
        multiworld.get_location(location_name_to_label("ITEM_ROUTE_114_PROTEIN"), player),
        can_rock_smash
    )

    # Safari Zone
    set_rule(
        multiworld.get_location(location_name_to_label("ITEM_SAFARI_ZONE_NORTH_WEST_TM22"), player),
        can_surf
    )
    set_rule(
        multiworld.get_location(location_name_to_label("ITEM_SAFARI_ZONE_SOUTH_WEST_MAX_REVIVE"), player),
        can_surf
    )
    set_rule(
        multiworld.get_location(location_name_to_label("ITEM_SAFARI_ZONE_SOUTH_EAST_BIG_PEARL"), player),
        can_surf
    )

    # Victory Road
    set_rule(
        multiworld.get_location(location_name_to_label("ITEM_VICTORY_ROAD_B1F_FULL_RESTORE"), player),
        lambda state: can_rock_smash(state) and can_strength(state)
    )


def set_hidden_item_rules(multiworld: MultiWorld, player: int):
    can_cut = lambda state: _can_cut(state, player)

    # Route 120
    set_rule(
        multiworld.get_location(location_name_to_label("HIDDEN_ITEM_ROUTE_120_RARE_CANDY_1"), player),
        can_cut
    )

    # Route 121
    set_rule(
        multiworld.get_location(location_name_to_label("HIDDEN_ITEM_ROUTE_121_NUGGET"), player),
        can_cut
    )


def set_npc_gift_rules(multiworld: MultiWorld, player: int):
    # Littleroot Town
    set_rule(
        multiworld.get_location(location_name_to_label("NPC_GIFT_RECEIVED_AMULET_COIN"), player),
        lambda state: state.has("EVENT_TALK_TO_MR_STONE", player) and state.has("Balance Badge", player)
    )

    # Petalburg City
    set_rule(
        multiworld.get_location(location_name_to_label("NPC_GIFT_RECEIVED_TM36"), player),
        lambda state: state.has("EVENT_DEFEAT_NORMAN", player)
    )

    # Route 104
    set_rule(
        multiworld.get_location(location_name_to_label("NPC_GIFT_RECEIVED_WHITE_HERB"), player),
        lambda state: state.has("Dynamo Badge", player) and state.has("EVENT_MEET_FLOWER_SHOP_OWNER", player)
    )

    # Devon Corp
    set_rule(
        multiworld.get_location(location_name_to_label("NPC_GIFT_RECEIVED_EXP_SHARE"), player),
        lambda state: state.has("EVENT_DELIVER_LETTER", player)
    )

    # Slateport City
    set_rule(
        multiworld.get_location(location_name_to_label("NPC_GIFT_RECEIVED_DEEP_SEA_TOOTH"), player),
        lambda state: state.has("EVENT_AQUA_STEALS_SUBMARINE", player)
            and state.has("Scanner", player)
            and state.has("Mind Badge", player)
    )
    set_rule(
        multiworld.get_location(location_name_to_label("NPC_GIFT_RECEIVED_DEEP_SEA_SCALE"), player),
        lambda state: state.has("EVENT_AQUA_STEALS_SUBMARINE", player)
            and state.has("Scanner", player)
            and state.has("Mind Badge", player)
    )

    # Route 116
    set_rule(
        multiworld.get_location(location_name_to_label("NPC_GIFT_RECEIVED_REPEAT_BALL"), player),
        lambda state: state.has("EVENT_RESCUE_CAPT_STERN", player)
    )

    # Mauville City
    set_rule(
        multiworld.get_location(location_name_to_label("NPC_GIFT_GOT_TM24_FROM_WATTSON"), player),
        lambda state: state.has("EVENT_DEFEAT_NORMAN", player) and state.has("EVENT_TURN_OFF_GENERATOR", player)
    )
    set_rule(
        multiworld.get_location(location_name_to_label("NPC_GIFT_RECEIVED_COIN_CASE"), player),
        lambda state: state.has("EVENT_BUY_HARBOR_MAIL", player)
    )

    # Fallarbor Town
    set_rule(
        multiworld.get_location(location_name_to_label("NPC_GIFT_RECEIVED_TM27"), player),
        lambda state: state.has("EVENT_RECOVER_METEORITE", player) and state.has("Meteorite", player)
    )

    # Fortree City
    set_rule(
        multiworld.get_location(location_name_to_label("NPC_GIFT_RECEIVED_MENTAL_HERB"), player),
        lambda state: state.has("EVENT_WINGULL_QUEST_2", player)
    )


def set_enable_ferry_rules(multiworld: MultiWorld, player: int):
    set_rule(
        multiworld.get_location(location_name_to_label("NPC_GIFT_RECEIVED_SS_TICKET"), player),
        lambda state: state.has("EVENT_DEFEAT_CHAMPION", player)
    )
    set_rule(
        multiworld.get_entrance("REGION_SLATEPORT_CITY_HARBOR/MAIN -> REGION_SS_TIDAL_CORRIDOR/MAIN", player),
        lambda state: state.has("S.S. Ticket", player)
    )
    set_rule(
        multiworld.get_entrance("REGION_LILYCOVE_CITY_HARBOR/MAIN -> REGION_SS_TIDAL_CORRIDOR/MAIN", player),
        lambda state: state.has("S.S. Ticket", player)
    )


def add_hidden_item_itemfinder_rules(multiworld: MultiWorld, player: int):
    for location in multiworld.get_locations(player):
        if location.tags is not None and "HiddenItem" in location.tags:
            add_rule(
                location,
                lambda state: state.has("Itemfinder", player)
            )


def add_flash_rules(multiworld: MultiWorld, player: int):
    can_flash = lambda state: _can_flash(state, player)

    # Granite Cave
    add_rule(
        multiworld.get_entrance("MAP_GRANITE_CAVE_1F:2/MAP_GRANITE_CAVE_B1F:1", player),
        can_flash
    )
    add_rule(
        multiworld.get_entrance("MAP_GRANITE_CAVE_B1F:3/MAP_GRANITE_CAVE_B2F:1", player),
        can_flash
    )

    # Victory Road
    add_rule(
        multiworld.get_entrance("MAP_VICTORY_ROAD_1F:2/MAP_VICTORY_ROAD_B1F:5", player),
        can_flash
    )
    add_rule(
        multiworld.get_entrance("MAP_VICTORY_ROAD_1F:4/MAP_VICTORY_ROAD_B1F:4", player),
        can_flash
    )
    add_rule(
        multiworld.get_entrance("MAP_VICTORY_ROAD_1F:3/MAP_VICTORY_ROAD_B1F:2", player),
        can_flash
    )
    add_rule(
        multiworld.get_entrance("MAP_VICTORY_ROAD_B1F:3/MAP_VICTORY_ROAD_B2F:1", player),
        can_flash
    )
    add_rule(
        multiworld.get_entrance("MAP_VICTORY_ROAD_B1F:1/MAP_VICTORY_ROAD_B2F:2", player),
        can_flash
    )
    add_rule(
        multiworld.get_entrance("MAP_VICTORY_ROAD_B1F:6/MAP_VICTORY_ROAD_B2F:3", player),
        can_flash
    )
    add_rule(
        multiworld.get_entrance("MAP_VICTORY_ROAD_B1F:0/MAP_VICTORY_ROAD_B2F:0", player),
        can_flash
    )
    add_rule(
        multiworld.get_entrance("MAP_VICTORY_ROAD_B2F:3/MAP_VICTORY_ROAD_B1F:6", player),
        can_flash
    )
    add_rule(
        multiworld.get_entrance("MAP_VICTORY_ROAD_B2F:2/MAP_VICTORY_ROAD_B1F:1", player),
        can_flash
    )
    add_rule(
        multiworld.get_entrance("MAP_VICTORY_ROAD_B2F:0/MAP_VICTORY_ROAD_B1F:0", player),
        can_flash
    )
    add_rule(
        multiworld.get_entrance("MAP_VICTORY_ROAD_B2F:1/MAP_VICTORY_ROAD_B1F:3", player),
        can_flash
    )
