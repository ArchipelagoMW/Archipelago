"""
Logic rule definitions for Pokemon Emerald
"""
from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule

from .data import data
from .options import EliteFourRequirement, NormanRequirement, Goal

if TYPE_CHECKING:
    from . import PokemonEmeraldWorld


# Rules are organized by town/route/dungeon and ordered approximately
# by when you would first reach that place in a vanilla playthrough.
def set_rules(world: "PokemonEmeraldWorld") -> None:
    def can_cut(state: CollectionState):
        return state.has("HM01 Cut", world.player) and state.has("Stone Badge", world.player)

    def can_surf(state: CollectionState):
        return state.has("HM03 Surf", world.player) and state.has("Balance Badge", world.player)

    def can_strength(state: CollectionState):
        return state.has("HM04 Strength", world.player) and state.has("Heat Badge", world.player)

    def can_flash(state: CollectionState):
        return state.has("HM05 Flash", world.player) and state.has("Knuckle Badge", world.player)

    def can_rock_smash(state: CollectionState):
        return state.has("HM06 Rock Smash", world.player) and state.has("Dynamo Badge", world.player)

    def can_waterfall(state: CollectionState):
        return state.has("HM07 Waterfall", world.player) and state.has("Rain Badge", world.player)

    def can_dive(state: CollectionState):
        return state.has("HM08 Dive", world.player) and state.has("Mind Badge", world.player)

    def has_acro_bike(state: CollectionState):
        return state.has("Acro Bike", world.player)

    def has_mach_bike(state: CollectionState):
        return state.has("Mach Bike", world.player)
    
    def defeated_n_gym_leaders(state: CollectionState, n: int) -> bool:
        return sum([state.has(event, world.player) for event in [
            "EVENT_DEFEAT_ROXANNE",
            "EVENT_DEFEAT_BRAWLY",
            "EVENT_DEFEAT_WATTSON",
            "EVENT_DEFEAT_FLANNERY",
            "EVENT_DEFEAT_NORMAN",
            "EVENT_DEFEAT_WINONA",
            "EVENT_DEFEAT_TATE_AND_LIZA",
            "EVENT_DEFEAT_JUAN"
        ]]) >= n

    def get_entrance(entrance: str):
        return world.multiworld.get_entrance(entrance, world.player)

    def get_location(location: str):
        if location in data.locations:
            location = data.locations[location].label

        return world.multiworld.get_location(location, world.player)

    victory_event_name = "EVENT_DEFEAT_CHAMPION"
    if world.options.goal == Goal.option_steven:
        victory_event_name = "EVENT_DEFEAT_STEVEN"
    elif world.options.goal == Goal.option_norman:
        victory_event_name = "EVENT_DEFEAT_NORMAN"

    world.multiworld.completion_condition[world.player] = lambda state: state.has(victory_event_name, world.player)

    # Sky
    if world.options.fly_without_badge:
        set_rule(
            get_entrance("REGION_LITTLEROOT_TOWN/MAIN -> REGION_SKY"),
            lambda state: state.has("HM02 Fly", world.player)
        )
    else:
        set_rule(
            get_entrance("REGION_LITTLEROOT_TOWN/MAIN -> REGION_SKY"),
            lambda state: state.has("HM02 Fly", world.player) and state.has("Feather Badge", world.player)
        )
    set_rule(
        get_entrance("REGION_SKY -> REGION_LITTLEROOT_TOWN/MAIN"),
        lambda state: state.has("EVENT_VISITED_LITTLEROOT_TOWN", world.player)
    )
    set_rule(
        get_entrance("REGION_SKY -> REGION_OLDALE_TOWN/MAIN"),
        lambda state: state.has("EVENT_VISITED_OLDALE_TOWN", world.player)
    )
    set_rule(
        get_entrance("REGION_SKY -> REGION_PETALBURG_CITY/MAIN"),
        lambda state: state.has("EVENT_VISITED_PETALBURG_CITY", world.player)
    )
    set_rule(
        get_entrance("REGION_SKY -> REGION_RUSTBORO_CITY/MAIN"),
        lambda state: state.has("EVENT_VISITED_RUSTBORO_CITY", world.player)
    )
    set_rule(
        get_entrance("REGION_SKY -> REGION_DEWFORD_TOWN/MAIN"),
        lambda state: state.has("EVENT_VISITED_DEWFORD_TOWN", world.player)
    )
    set_rule(
        get_entrance("REGION_SKY -> REGION_SLATEPORT_CITY/MAIN"),
        lambda state: state.has("EVENT_VISITED_SLATEPORT_CITY", world.player)
    )
    set_rule(
        get_entrance("REGION_SKY -> REGION_MAUVILLE_CITY/MAIN"),
        lambda state: state.has("EVENT_VISITED_MAUVILLE_CITY", world.player)
    )
    set_rule(
        get_entrance("REGION_SKY -> REGION_VERDANTURF_TOWN/MAIN"),
        lambda state: state.has("EVENT_VISITED_VERDANTURF_TOWN", world.player)
    )
    set_rule(
        get_entrance("REGION_SKY -> REGION_FALLARBOR_TOWN/MAIN"),
        lambda state: state.has("EVENT_VISITED_FALLARBOR_TOWN", world.player)
    )
    set_rule(
        get_entrance("REGION_SKY -> REGION_LAVARIDGE_TOWN/MAIN"),
        lambda state: state.has("EVENT_VISITED_LAVARIDGE_TOWN", world.player)
    )
    set_rule(
        get_entrance("REGION_SKY -> REGION_FORTREE_CITY/MAIN"),
        lambda state: state.has("EVENT_VISITED_FORTREE_CITY", world.player)
    )
    set_rule(
        get_entrance("REGION_SKY -> REGION_LILYCOVE_CITY/MAIN"),
        lambda state: state.has("EVENT_VISITED_LILYCOVE_CITY", world.player)
    )
    set_rule(
        get_entrance("REGION_SKY -> REGION_MOSSDEEP_CITY/MAIN"),
        lambda state: state.has("EVENT_VISITED_MOSSDEEP_CITY", world.player)
    )
    set_rule(
        get_entrance("REGION_SKY -> REGION_SOOTOPOLIS_CITY/EAST"),
        lambda state: state.has("EVENT_VISITED_SOOTOPOLIS_CITY", world.player)
    )
    set_rule(
        get_entrance("REGION_SKY -> REGION_EVER_GRANDE_CITY/SOUTH"),
        lambda state: state.has("EVENT_VISITED_EVER_GRANDE_CITY", world.player)
    )

    # Route 103
    set_rule(
        get_entrance("REGION_ROUTE103/EAST -> REGION_ROUTE103/WATER"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_ROUTE103/WEST -> REGION_ROUTE103/WATER"),
        can_surf
    )

    # Petalburg City
    set_rule(
        get_entrance("REGION_PETALBURG_CITY/MAIN -> REGION_PETALBURG_CITY/SOUTH_POND"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_PETALBURG_CITY/MAIN -> REGION_PETALBURG_CITY/NORTH_POND"),
        can_surf
    )
    set_rule(
        get_location("NPC_GIFT_RECEIVED_HM03"),
        lambda state: state.has("EVENT_DEFEAT_NORMAN", world.player)
    )
    if world.options.norman_requirement == NormanRequirement.option_badges:
        set_rule(
            get_entrance("MAP_PETALBURG_CITY_GYM:2/MAP_PETALBURG_CITY_GYM:3"),
            lambda state: state.has_group("Badges", world.player, world.options.norman_count.value)
        )
        set_rule(
            get_entrance("MAP_PETALBURG_CITY_GYM:5/MAP_PETALBURG_CITY_GYM:6"),
            lambda state: state.has_group("Badges", world.player, world.options.norman_count.value)
        )
    else:
        set_rule(
            get_entrance("MAP_PETALBURG_CITY_GYM:2/MAP_PETALBURG_CITY_GYM:3"),
            lambda state: defeated_n_gym_leaders(state, world.options.norman_count.value)
        )
        set_rule(
            get_entrance("MAP_PETALBURG_CITY_GYM:5/MAP_PETALBURG_CITY_GYM:6"),
            lambda state: defeated_n_gym_leaders(state, world.options.norman_count.value)
        )

    # Route 104
    set_rule(
        get_entrance("REGION_ROUTE104/SOUTH -> REGION_ROUTE105/MAIN"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_ROUTE104_MR_BRINEYS_HOUSE/MAIN -> REGION_DEWFORD_TOWN/MAIN"),
        lambda state: state.has("EVENT_TALK_TO_MR_STONE", world.player)
    )

    # Petalburg Woods
    set_rule(
        get_entrance("REGION_PETALBURG_WOODS/WEST_PATH -> REGION_PETALBURG_WOODS/EAST_PATH"),
        can_cut
    )

    # Rustboro City
    set_rule(
        get_location("EVENT_RETURN_DEVON_GOODS"),
        lambda state: state.has("EVENT_RECOVER_DEVON_GOODS", world.player)
    )

    # Devon Corp
    set_rule(
        get_entrance("MAP_RUSTBORO_CITY_DEVON_CORP_1F:2/MAP_RUSTBORO_CITY_DEVON_CORP_2F:0"),
        lambda state: state.has("EVENT_RETURN_DEVON_GOODS", world.player)
    )

    # Route 116
    set_rule(
        get_entrance("REGION_ROUTE116/WEST -> REGION_ROUTE116/WEST_ABOVE_LEDGE"),
        can_cut
    )

    # Rusturf Tunnel
    set_rule(
        get_entrance("REGION_RUSTURF_TUNNEL/WEST -> REGION_RUSTURF_TUNNEL/EAST"),
        can_rock_smash
    )
    set_rule(
        get_entrance("REGION_RUSTURF_TUNNEL/EAST -> REGION_RUSTURF_TUNNEL/WEST"),
        can_rock_smash
    )
    set_rule(
        get_location("NPC_GIFT_RECEIVED_HM04"),
        can_rock_smash
    )
    set_rule(
        get_location("EVENT_RECOVER_DEVON_GOODS"),
        lambda state: state.has("EVENT_DEFEAT_ROXANNE", world.player)
    )

    # Route 115
    set_rule(
        get_entrance("REGION_ROUTE115/SOUTH_BELOW_LEDGE -> REGION_ROUTE115/SEA"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_ROUTE115/SOUTH_BEACH_NEAR_CAVE -> REGION_ROUTE115/SEA"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_ROUTE115/SOUTH_ABOVE_LEDGE -> REGION_ROUTE115/SOUTH_BEHIND_ROCK"),
        can_rock_smash
    )
    set_rule(
        get_entrance("REGION_ROUTE115/NORTH_BELOW_SLOPE -> REGION_ROUTE115/SEA"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_ROUTE115/NORTH_BELOW_SLOPE -> REGION_ROUTE115/NORTH_ABOVE_SLOPE"),
        lambda state: has_mach_bike(state)
    )
    if world.options.extra_boulders:
        set_rule(
            get_entrance("REGION_ROUTE115/SOUTH_BEACH_NEAR_CAVE -> REGION_ROUTE115/SOUTH_ABOVE_LEDGE"),
            can_strength
        )
        set_rule(
            get_entrance("REGION_ROUTE115/SOUTH_ABOVE_LEDGE -> REGION_ROUTE115/SOUTH_BEACH_NEAR_CAVE"),
            can_strength
        )

    # Route 105
    set_rule(
        get_entrance("REGION_ROUTE105/MAIN -> REGION_UNDERWATER_ROUTE105/MAIN"),
        can_dive
    )

    # Route 106
    set_rule(
        get_entrance("REGION_ROUTE106/EAST -> REGION_ROUTE106/SEA"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_ROUTE106/WEST -> REGION_ROUTE106/SEA"),
        can_surf
    )

    # Dewford Town
    set_rule(
        get_entrance("REGION_DEWFORD_TOWN/MAIN -> REGION_ROUTE109/BEACH"),
        lambda state:
            state.can_reach("REGION_ROUTE104_MR_BRINEYS_HOUSE/MAIN -> REGION_DEWFORD_TOWN/MAIN", "Entrance", world.player)
            and state.has("EVENT_TALK_TO_MR_STONE", world.player)
            and state.has("EVENT_DELIVER_LETTER", world.player)
    )
    set_rule(
        get_entrance("REGION_DEWFORD_TOWN/MAIN -> REGION_ROUTE104_MR_BRINEYS_HOUSE/MAIN"),
        lambda state:
            state.can_reach("REGION_ROUTE104_MR_BRINEYS_HOUSE/MAIN -> REGION_DEWFORD_TOWN/MAIN", "Entrance", world.player)
            and state.has("EVENT_TALK_TO_MR_STONE", world.player)
    )

    # Granite Cave
    set_rule(
        get_entrance("REGION_GRANITE_CAVE_STEVENS_ROOM/MAIN -> REGION_GRANITE_CAVE_STEVENS_ROOM/LETTER_DELIVERED"),
        lambda state: state.has("Letter", world.player)
    )
    set_rule(
        get_entrance("REGION_GRANITE_CAVE_B1F/LOWER -> REGION_GRANITE_CAVE_B1F/UPPER"),
        lambda state: has_mach_bike(state)
    )

    # Route 107
    set_rule(
        get_entrance("REGION_DEWFORD_TOWN/MAIN -> REGION_ROUTE107/MAIN"),
        can_surf
    )

    # Route 109
    set_rule(
        get_entrance("REGION_ROUTE109/BEACH -> REGION_DEWFORD_TOWN/MAIN"),
        lambda state:
            state.can_reach("REGION_ROUTE104_MR_BRINEYS_HOUSE/MAIN -> REGION_DEWFORD_TOWN/MAIN", "Entrance", world.player)
            and state.can_reach("REGION_DEWFORD_TOWN/MAIN -> REGION_ROUTE109/BEACH", "Entrance", world.player)
            and state.has("EVENT_TALK_TO_MR_STONE", world.player)
            and state.has("EVENT_DELIVER_LETTER", world.player)
    )
    set_rule(
        get_entrance("REGION_ROUTE109/BEACH -> REGION_ROUTE109/SEA"),
        can_surf
    )

    # Slateport City
    set_rule(
        get_entrance("REGION_SLATEPORT_CITY/MAIN -> REGION_ROUTE134/WEST"),
        can_surf
    )
    set_rule(
        get_location("EVENT_TALK_TO_DOCK"),
        lambda state: state.has("Devon Goods", world.player)
    )
    set_rule(
        get_entrance("MAP_SLATEPORT_CITY:5,7/MAP_SLATEPORT_CITY_OCEANIC_MUSEUM_1F:0,1"),
        lambda state: state.has("EVENT_TALK_TO_DOCK", world.player)
    )
    set_rule(
        get_location("EVENT_AQUA_STEALS_SUBMARINE"),
        lambda state: state.has("EVENT_RELEASE_GROUDON", world.player)
    )
    set_rule(
        get_entrance("REGION_SLATEPORT_CITY_HARBOR/MAIN -> REGION_SS_TIDAL_CORRIDOR/MAIN"),
        lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player)
    )

    # Route 110
    set_rule(
        get_entrance("REGION_ROUTE110/MAIN -> REGION_ROUTE110/SOUTH_WATER"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_ROUTE110/MAIN -> REGION_ROUTE110/NORTH_WATER"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_ROUTE110_SEASIDE_CYCLING_ROAD_SOUTH_ENTRANCE/WEST -> REGION_ROUTE110_SEASIDE_CYCLING_ROAD_SOUTH_ENTRANCE/EAST"),
        lambda state: has_acro_bike(state) or has_mach_bike(state)
    )
    set_rule(
        get_entrance("REGION_ROUTE110_SEASIDE_CYCLING_ROAD_NORTH_ENTRANCE/WEST -> REGION_ROUTE110_SEASIDE_CYCLING_ROAD_NORTH_ENTRANCE/EAST"),
        lambda state: has_acro_bike(state) or has_mach_bike(state)
    )
    if "Route 110 Aqua Grunts" not in world.options.remove_roadblocks.value:
        set_rule(
            get_entrance("REGION_ROUTE110/SOUTH -> REGION_ROUTE110/MAIN"),
            lambda state: state.has("EVENT_RESCUE_CAPT_STERN", world.player)
        )
        set_rule(
            get_entrance("REGION_ROUTE110/MAIN -> REGION_ROUTE110/SOUTH"),
            lambda state: state.has("EVENT_RESCUE_CAPT_STERN", world.player)
        )

    # Mauville City
    set_rule(
        get_location("NPC_GIFT_GOT_BASEMENT_KEY_FROM_WATTSON"),
        lambda state: state.has("EVENT_DEFEAT_NORMAN", world.player)
    )

    # Route 111
    set_rule(
        get_entrance("REGION_ROUTE111/MIDDLE -> REGION_ROUTE111/DESERT"),
        lambda state: state.has("Go Goggles", world.player)
    )
    set_rule(
        get_entrance("REGION_ROUTE111/NORTH -> REGION_ROUTE111/DESERT"),
        lambda state: state.has("Go Goggles", world.player)
    )
    set_rule(
        get_entrance("REGION_ROUTE111/MIDDLE -> REGION_ROUTE111/SOUTH"),
        can_rock_smash
    )
    set_rule(
        get_entrance("REGION_ROUTE111/SOUTH -> REGION_ROUTE111/SOUTH_POND"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_ROUTE111/SOUTH -> REGION_ROUTE111/MIDDLE"),
        can_rock_smash
    )
    set_rule(
        get_entrance("MAP_ROUTE111:4/MAP_TRAINER_HILL_ENTRANCE:0"),
        lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player)
    )

    # Route 112
    if "Route 112 Magma Grunts" not in world.options.remove_roadblocks.value:
        set_rule(
            get_entrance("REGION_ROUTE112/SOUTH_EAST -> REGION_ROUTE112/CABLE_CAR_STATION_ENTRANCE"),
            lambda state: state.has("EVENT_MAGMA_STEALS_METEORITE", world.player)
        )
        set_rule(
            get_entrance("REGION_ROUTE112/CABLE_CAR_STATION_ENTRANCE -> REGION_ROUTE112/SOUTH_EAST"),
            lambda state: state.has("EVENT_MAGMA_STEALS_METEORITE", world.player)
        )

    # Fiery Path
    set_rule(
        get_entrance("REGION_FIERY_PATH/MAIN -> REGION_FIERY_PATH/BEHIND_BOULDER"),
        can_strength
    )

    # Route 114
    set_rule(
        get_entrance("REGION_ROUTE114/MAIN -> REGION_ROUTE114/ABOVE_WATERFALL"),
        lambda state: can_surf(state) and can_waterfall(state)
    )
    set_rule(
        get_entrance("REGION_ROUTE114/ABOVE_WATERFALL -> REGION_ROUTE114/MAIN"),
        lambda state: can_surf(state) and can_waterfall(state)
    )
    set_rule(
        get_entrance("MAP_ROUTE114_FOSSIL_MANIACS_TUNNEL:2/MAP_DESERT_UNDERPASS:0"),
        lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player)
    )

    # Meteor Falls
    set_rule(
        get_entrance("REGION_METEOR_FALLS_1F_1R/MAIN -> REGION_METEOR_FALLS_1F_1R/ABOVE_WATERFALL"),
        lambda state: can_surf(state) and can_waterfall(state)
    )
    set_rule(
        get_entrance("REGION_METEOR_FALLS_1F_1R/ABOVE_WATERFALL -> REGION_METEOR_FALLS_1F_1R/MAIN"),
        can_surf
    )
    set_rule(
        get_entrance("MAP_METEOR_FALLS_1F_1R:5/MAP_METEOR_FALLS_STEVENS_CAVE:0"),
        lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player)
    )
    set_rule(
        get_entrance("REGION_METEOR_FALLS_B1F_1R/HIGHEST_LADDER -> REGION_METEOR_FALLS_B1F_1R/WATER"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_METEOR_FALLS_B1F_1R/NORTH_SHORE -> REGION_METEOR_FALLS_B1F_1R/WATER"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_METEOR_FALLS_B1F_1R/SOUTH_SHORE -> REGION_METEOR_FALLS_B1F_1R/WATER"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_METEOR_FALLS_B1F_2R/ENTRANCE -> REGION_METEOR_FALLS_B1F_2R/WATER"),
        can_surf
    )

    # Jagged Pass
    set_rule(
        get_entrance("REGION_JAGGED_PASS/BOTTOM -> REGION_JAGGED_PASS/MIDDLE"),
        lambda state: has_acro_bike(state)
    )
    set_rule(
        get_entrance("REGION_JAGGED_PASS/MIDDLE -> REGION_JAGGED_PASS/TOP"),
        lambda state: has_acro_bike(state)
    )
    set_rule(
        get_entrance("MAP_JAGGED_PASS:4/MAP_MAGMA_HIDEOUT_1F:0"),
        lambda state: state.has("Magma Emblem", world.player)
    )

    # Lavaridge Town
    set_rule(
        get_location("NPC_GIFT_RECEIVED_GO_GOGGLES"),
        lambda state: state.has("EVENT_DEFEAT_FLANNERY", world.player)
    )

    # Mirage Tower
    set_rule(
        get_entrance("REGION_MIRAGE_TOWER_2F/TOP -> REGION_MIRAGE_TOWER_2F/BOTTOM"),
        lambda state: has_mach_bike(state)
    )
    set_rule(
        get_entrance("REGION_MIRAGE_TOWER_2F/BOTTOM -> REGION_MIRAGE_TOWER_2F/TOP"),
        lambda state: has_mach_bike(state)
    )
    set_rule(
        get_entrance("REGION_MIRAGE_TOWER_3F/TOP -> REGION_MIRAGE_TOWER_3F/BOTTOM"),
        can_rock_smash
    )
    set_rule(
        get_entrance("REGION_MIRAGE_TOWER_3F/BOTTOM -> REGION_MIRAGE_TOWER_3F/TOP"),
        can_rock_smash
    )
    set_rule(
        get_entrance("REGION_MIRAGE_TOWER_4F/MAIN -> REGION_MIRAGE_TOWER_4F/FOSSIL_PLATFORM"),
        can_rock_smash
    )

    # Abandoned Ship
    set_rule(
        get_entrance("REGION_ABANDONED_SHIP_ROOMS_B1F/CENTER -> REGION_ABANDONED_SHIP_UNDERWATER1/MAIN"),
        can_dive
    )
    set_rule(
        get_entrance("REGION_ABANDONED_SHIP_HIDDEN_FLOOR_CORRIDORS/MAIN -> REGION_ABANDONED_SHIP_UNDERWATER2/MAIN"),
        can_dive
    )
    set_rule(
        get_entrance("MAP_ABANDONED_SHIP_HIDDEN_FLOOR_CORRIDORS:0/MAP_ABANDONED_SHIP_HIDDEN_FLOOR_ROOMS:0"),
        lambda state: state.has("Room 1 Key", world.player)
    )
    set_rule(
        get_entrance("MAP_ABANDONED_SHIP_HIDDEN_FLOOR_CORRIDORS:1/MAP_ABANDONED_SHIP_HIDDEN_FLOOR_ROOMS:2"),
        lambda state: state.has("Room 2 Key", world.player)
    )
    set_rule(
        get_entrance("MAP_ABANDONED_SHIP_HIDDEN_FLOOR_CORRIDORS:3/MAP_ABANDONED_SHIP_HIDDEN_FLOOR_ROOMS:6"),
        lambda state: state.has("Room 4 Key", world.player)
    )
    set_rule(
        get_entrance("MAP_ABANDONED_SHIP_HIDDEN_FLOOR_CORRIDORS:5/MAP_ABANDONED_SHIP_HIDDEN_FLOOR_ROOMS:8"),
        lambda state: state.has("Room 6 Key", world.player)
    )
    set_rule(
        get_entrance("MAP_ABANDONED_SHIP_CORRIDORS_B1F:5/MAP_ABANDONED_SHIP_ROOM_B1F:0"),
        lambda state: state.has("Storage Key", world.player)
    )

    # New Mauville
    set_rule(
        get_entrance("MAP_NEW_MAUVILLE_ENTRANCE:1/MAP_NEW_MAUVILLE_INSIDE:0"),
        lambda state: state.has("Basement Key", world.player)
    )

    # Route 118
    set_rule(
        get_entrance("REGION_ROUTE118/WEST -> REGION_ROUTE118/WATER"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_ROUTE118/EAST -> REGION_ROUTE118/WATER"),
        can_surf
    )

    # Route 119
    set_rule(
        get_entrance("REGION_ROUTE119/LOWER -> REGION_ROUTE119/LOWER_ACROSS_WATER"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_ROUTE119/LOWER_ACROSS_WATER -> REGION_ROUTE119/LOWER"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_ROUTE119/LOWER -> REGION_ROUTE119/LOWER_ACROSS_RAILS"),
        lambda state: has_acro_bike(state)
    )
    set_rule(
        get_entrance("REGION_ROUTE119/LOWER_ACROSS_RAILS -> REGION_ROUTE119/LOWER"),
        lambda state: has_acro_bike(state)
    )
    set_rule(
        get_entrance("REGION_ROUTE119/UPPER -> REGION_ROUTE119/MIDDLE_RIVER"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_ROUTE119/MIDDLE_RIVER -> REGION_ROUTE119/ABOVE_WATERFALL"),
        can_waterfall
    )
    set_rule(
        get_entrance("REGION_ROUTE119/ABOVE_WATERFALL -> REGION_ROUTE119/MIDDLE_RIVER"),
        can_waterfall
    )
    set_rule(
        get_entrance("REGION_ROUTE119/ABOVE_WATERFALL -> REGION_ROUTE119/ABOVE_WATERFALL_ACROSS_RAILS"),
        lambda state: has_acro_bike(state)
    )
    if "Route 119 Aqua Grunts" not in world.options.remove_roadblocks.value:
        set_rule(
            get_entrance("REGION_ROUTE119/MIDDLE -> REGION_ROUTE119/UPPER"),
            lambda state: state.has("EVENT_DEFEAT_SHELLY", world.player)
        )
        set_rule(
            get_entrance("REGION_ROUTE119/UPPER -> REGION_ROUTE119/MIDDLE"),
            lambda state: state.has("EVENT_DEFEAT_SHELLY", world.player)
        )

    # Fortree City
    set_rule(
        get_entrance("REGION_FORTREE_CITY/MAIN -> REGION_FORTREE_CITY/BEFORE_GYM"),
        lambda state: state.has("Devon Scope", world.player)
    )
    set_rule(
        get_entrance("REGION_FORTREE_CITY/BEFORE_GYM -> REGION_FORTREE_CITY/MAIN"),
        lambda state: state.has("Devon Scope", world.player)
    )

    # Route 120
    set_rule(
        get_entrance("REGION_ROUTE120/NORTH -> REGION_ROUTE120/NORTH_POND_SHORE"),
        lambda state: state.has("Devon Scope", world.player)
    )
    set_rule(
        get_entrance("REGION_ROUTE120/NORTH_POND_SHORE -> REGION_ROUTE120/NORTH"),
        lambda state: state.has("Devon Scope", world.player)
    )
    set_rule(
        get_entrance("REGION_ROUTE120/NORTH_POND_SHORE -> REGION_ROUTE120/NORTH_POND"),
        can_surf
    )

    # Route 121
    set_rule(
        get_entrance("REGION_ROUTE121/EAST -> REGION_ROUTE121/WEST"),
        can_cut
    )
    set_rule(
        get_entrance("REGION_ROUTE121/EAST -> REGION_ROUTE122/SEA"),
        can_surf
    )

    # Safari Zone
    set_rule(
        get_entrance("MAP_ROUTE121_SAFARI_ZONE_ENTRANCE:0,1/MAP_SAFARI_ZONE_SOUTH:0"),
        lambda state: state.has("Pokeblock Case", world.player)
    )
    set_rule(
        get_entrance("REGION_SAFARI_ZONE_SOUTH/MAIN -> REGION_SAFARI_ZONE_NORTH/MAIN"),
        lambda state: has_acro_bike(state)
    )
    set_rule(
        get_entrance("REGION_SAFARI_ZONE_SOUTHWEST/MAIN -> REGION_SAFARI_ZONE_NORTHWEST/MAIN"),
        lambda state: has_mach_bike(state)
    )
    if "Safari Zone Construction Workers" not in world.options.remove_roadblocks.value:
        set_rule(
            get_entrance("REGION_SAFARI_ZONE_SOUTH/MAIN -> REGION_SAFARI_ZONE_SOUTHEAST/MAIN"),
            lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player)
        )

    # Route 122
    set_rule(
        get_entrance("REGION_ROUTE122/MT_PYRE_ENTRANCE -> REGION_ROUTE122/SEA"),
        can_surf
    )

    # Route 123
    set_rule(
        get_entrance("REGION_ROUTE123/EAST -> REGION_ROUTE122/SEA"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_ROUTE123/EAST -> REGION_ROUTE123/EAST_BEHIND_TREE"),
        can_cut
    )

    # Lilycove City
    set_rule(
        get_entrance("REGION_LILYCOVE_CITY/MAIN -> REGION_LILYCOVE_CITY/SEA"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_LILYCOVE_CITY_HARBOR/MAIN -> REGION_SS_TIDAL_CORRIDOR/MAIN"),
        lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player)
    )
    if "Lilycove City Wailmer" not in world.options.remove_roadblocks.value:
        set_rule(
            get_entrance("REGION_LILYCOVE_CITY/SEA -> REGION_ROUTE124/MAIN"),
            lambda state: state.has("EVENT_CLEAR_AQUA_HIDEOUT", world.player)
        )

    # Magma Hideout
    set_rule(
        get_entrance("REGION_MAGMA_HIDEOUT_1F/ENTRANCE -> REGION_MAGMA_HIDEOUT_1F/MAIN"),
        can_strength
    )
    set_rule(
        get_entrance("REGION_MAGMA_HIDEOUT_1F/MAIN -> REGION_MAGMA_HIDEOUT_1F/ENTRANCE"),
        can_strength
    )

    # Aqua Hideout
    if "Aqua Hideout Grunts" not in world.options.remove_roadblocks.value:
        set_rule(
            get_entrance("REGION_AQUA_HIDEOUT_1F/WATER -> REGION_AQUA_HIDEOUT_1F/MAIN"),
            lambda state: state.has("EVENT_AQUA_STEALS_SUBMARINE", world.player)
        )
        set_rule(
            get_entrance("REGION_AQUA_HIDEOUT_1F/MAIN -> REGION_AQUA_HIDEOUT_1F/WATER"),
            lambda state: can_surf(state) and state.has("EVENT_AQUA_STEALS_SUBMARINE", world.player)
        )

    # Route 124
    set_rule(
        get_entrance("REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/BIG_AREA"),
        can_dive
    )
    set_rule(
        get_entrance("REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/SMALL_AREA_1"),
        can_dive
    )
    set_rule(
        get_entrance("REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/SMALL_AREA_2"),
        can_dive
    )
    set_rule(
        get_entrance("REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/SMALL_AREA_3"),
        can_dive
    )
    set_rule(
        get_entrance("REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/TUNNEL_1"),
        can_dive
    )
    set_rule(
        get_entrance("REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/TUNNEL_2"),
        can_dive
    )
    set_rule(
        get_entrance("REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/TUNNEL_3"),
        can_dive
    )
    set_rule(
        get_entrance("REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/TUNNEL_4"),
        can_dive
    )
    set_rule(
        get_entrance("REGION_ROUTE124/NORTH_ENCLOSED_AREA_1 -> REGION_UNDERWATER_ROUTE124/TUNNEL_1"),
        can_dive
    )
    set_rule(
        get_entrance("REGION_ROUTE124/NORTH_ENCLOSED_AREA_2 -> REGION_UNDERWATER_ROUTE124/TUNNEL_1"),
        can_dive
    )
    set_rule(
        get_entrance("REGION_ROUTE124/NORTH_ENCLOSED_AREA_3 -> REGION_UNDERWATER_ROUTE124/TUNNEL_2"),
        can_dive
    )
    set_rule(
        get_entrance("REGION_ROUTE124/SOUTH_ENCLOSED_AREA_1 -> REGION_UNDERWATER_ROUTE124/TUNNEL_3"),
        can_dive
    )
    set_rule(
        get_entrance("REGION_ROUTE124/SOUTH_ENCLOSED_AREA_2 -> REGION_UNDERWATER_ROUTE124/TUNNEL_3"),
        can_dive
    )
    set_rule(
        get_entrance("REGION_ROUTE124/SOUTH_ENCLOSED_AREA_3 -> REGION_UNDERWATER_ROUTE124/TUNNEL_4"),
        can_dive
    )

    # Mossdeep City
    set_rule(
        get_entrance("REGION_MOSSDEEP_CITY/MAIN -> REGION_ROUTE124/MAIN"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_MOSSDEEP_CITY/MAIN -> REGION_ROUTE125/SEA"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_MOSSDEEP_CITY/MAIN -> REGION_ROUTE127/MAIN"),
        can_surf
    )
    set_rule(
        get_location("EVENT_DEFEAT_MAXIE_AT_SPACE_STATION"),
        lambda state: state.has("EVENT_DEFEAT_TATE_AND_LIZA", world.player)
    )
    set_rule(
        get_location("EVENT_STEVEN_GIVES_DIVE"),
        lambda state: state.has("EVENT_DEFEAT_MAXIE_AT_SPACE_STATION", world.player)
    )
    set_rule(
        get_location("NPC_GIFT_RECEIVED_HM08"),
        lambda state: state.has("EVENT_DEFEAT_MAXIE_AT_SPACE_STATION", world.player)
    )

    # Shoal Cave
    set_rule(
        get_entrance("REGION_SHOAL_CAVE_ENTRANCE_ROOM/SOUTH -> REGION_SHOAL_CAVE_ENTRANCE_ROOM/HIGH_TIDE_WATER"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_SHOAL_CAVE_ENTRANCE_ROOM/NORTH_WEST_CORNER -> REGION_SHOAL_CAVE_ENTRANCE_ROOM/HIGH_TIDE_WATER"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_SHOAL_CAVE_ENTRANCE_ROOM/NORTH_EAST_CORNER -> REGION_SHOAL_CAVE_ENTRANCE_ROOM/HIGH_TIDE_WATER"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_SHOAL_CAVE_INNER_ROOM/HIGH_TIDE_EAST_MIDDLE_GROUND -> REGION_SHOAL_CAVE_INNER_ROOM/SOUTH_EAST_WATER"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_SHOAL_CAVE_INNER_ROOM/HIGH_TIDE_EAST_MIDDLE_GROUND -> REGION_SHOAL_CAVE_INNER_ROOM/EAST_WATER"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_SHOAL_CAVE_INNER_ROOM/HIGH_TIDE_EAST_MIDDLE_GROUND -> REGION_SHOAL_CAVE_INNER_ROOM/NORTH_WEST_WATER"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_SHOAL_CAVE_INNER_ROOM/SOUTH_WEST_CORNER -> REGION_SHOAL_CAVE_INNER_ROOM/NORTH_WEST_WATER"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_SHOAL_CAVE_INNER_ROOM/RARE_CANDY_PLATFORM -> REGION_SHOAL_CAVE_INNER_ROOM/SOUTH_EAST_WATER"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_SHOAL_CAVE_LOW_TIDE_LOWER_ROOM/NORTH_WEST -> REGION_SHOAL_CAVE_LOW_TIDE_LOWER_ROOM/EAST"),
        can_strength
    )
    set_rule(
        get_entrance("REGION_SHOAL_CAVE_LOW_TIDE_LOWER_ROOM/EAST -> REGION_SHOAL_CAVE_LOW_TIDE_LOWER_ROOM/NORTH_WEST"),
        can_strength
    )

    # Route 126
    set_rule(
        get_entrance("REGION_ROUTE126/MAIN -> REGION_UNDERWATER_ROUTE126/MAIN"),
        can_dive
    )
    set_rule(
        get_entrance("REGION_ROUTE126/MAIN -> REGION_UNDERWATER_ROUTE126/SMALL_AREA_2"),
        can_dive
    )
    set_rule(
        get_entrance("REGION_ROUTE126/NEAR_ROUTE_124 -> REGION_UNDERWATER_ROUTE126/TUNNEL"),
        can_dive
    )
    set_rule(
        get_entrance("REGION_ROUTE126/NORTH_WEST_CORNER -> REGION_UNDERWATER_ROUTE126/TUNNEL"),
        can_dive
    )
    set_rule(
        get_entrance("REGION_ROUTE126/WEST -> REGION_UNDERWATER_ROUTE126/MAIN"),
        can_dive
    )
    set_rule(
        get_entrance("REGION_ROUTE126/WEST -> REGION_UNDERWATER_ROUTE126/SMALL_AREA_1"),
        can_dive
    )

    # Sootopolis City
    set_rule(
        get_entrance("REGION_SOOTOPOLIS_CITY/WATER -> REGION_UNDERWATER_SOOTOPOLIS_CITY/MAIN"),
        can_dive
    )
    set_rule(
        get_entrance("REGION_SOOTOPOLIS_CITY/EAST -> REGION_SOOTOPOLIS_CITY/WATER"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_SOOTOPOLIS_CITY/WEST -> REGION_SOOTOPOLIS_CITY/WATER"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_SOOTOPOLIS_CITY/ISLAND -> REGION_SOOTOPOLIS_CITY/WATER"),
        can_surf
    )
    set_rule(
        get_entrance("MAP_SOOTOPOLIS_CITY:3/MAP_CAVE_OF_ORIGIN_ENTRANCE:0"),
        lambda state: state.has("EVENT_RELEASE_KYOGRE", world.player)
    )
    set_rule(
        get_entrance("MAP_SOOTOPOLIS_CITY:2/MAP_SOOTOPOLIS_CITY_GYM_1F:0"),
        lambda state: state.has("EVENT_WAKE_RAYQUAZA", world.player)
    )
    set_rule(
        get_location("NPC_GIFT_RECEIVED_HM07"),
        lambda state: state.has("EVENT_WAKE_RAYQUAZA", world.player)
    )

    # Route 127
    set_rule(
        get_entrance("REGION_ROUTE127/MAIN -> REGION_UNDERWATER_ROUTE127/MAIN"),
        can_dive
    )
    set_rule(
        get_entrance("REGION_ROUTE127/MAIN -> REGION_UNDERWATER_ROUTE127/TUNNEL"),
        can_dive
    )
    set_rule(
        get_entrance("REGION_ROUTE127/MAIN -> REGION_UNDERWATER_ROUTE127/AREA_1"),
        can_dive
    )
    set_rule(
        get_entrance("REGION_ROUTE127/MAIN -> REGION_UNDERWATER_ROUTE127/AREA_2"),
        can_dive
    )
    set_rule(
        get_entrance("REGION_ROUTE127/MAIN -> REGION_UNDERWATER_ROUTE127/AREA_3"),
        can_dive
    )
    set_rule(
        get_entrance("REGION_ROUTE127/ENCLOSED_AREA -> REGION_UNDERWATER_ROUTE127/TUNNEL"),
        can_dive
    )

    # Route 128
    set_rule(
        get_entrance("REGION_ROUTE128/MAIN -> REGION_UNDERWATER_ROUTE128/MAIN"),
        can_dive
    )
    set_rule(
        get_entrance("REGION_ROUTE128/MAIN -> REGION_UNDERWATER_ROUTE128/AREA_1"),
        can_dive
    )
    set_rule(
        get_entrance("REGION_ROUTE128/MAIN -> REGION_UNDERWATER_ROUTE128/AREA_2"),
        can_dive
    )

    # Seafloor Cavern
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM1/SOUTH -> REGION_SEAFLOOR_CAVERN_ROOM1/NORTH"),
        lambda state: can_rock_smash(state) and can_strength(state)
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM1/NORTH -> REGION_SEAFLOOR_CAVERN_ROOM1/SOUTH"),
        can_strength
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM2/SOUTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM2/NORTH_WEST"),
        can_strength
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM2/NORTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM2/SOUTH_WEST"),
        can_strength
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM2/SOUTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM2/SOUTH_EAST"),
        can_rock_smash
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM2/SOUTH_EAST -> REGION_SEAFLOOR_CAVERN_ROOM2/SOUTH_WEST"),
        can_rock_smash
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM2/NORTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM2/NORTH_EAST"),
        lambda state: can_rock_smash(state) and can_strength(state)
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM2/NORTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM2/SOUTH_EAST"),
        lambda state: can_rock_smash(state) and can_strength(state)
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM5/NORTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM5/EAST"),
        lambda state: can_rock_smash(state) and can_strength(state)
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM5/EAST -> REGION_SEAFLOOR_CAVERN_ROOM5/NORTH_WEST"),
        can_strength
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM5/NORTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM5/SOUTH_WEST"),
        lambda state: can_rock_smash(state) and can_strength(state)
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM5/SOUTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM5/NORTH_WEST"),
        lambda state: can_rock_smash(state) and can_strength(state)
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM6/NORTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM6/CAVE_ON_WATER"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM6/SOUTH -> REGION_SEAFLOOR_CAVERN_ROOM6/NORTH_WEST"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM6/SOUTH -> REGION_SEAFLOOR_CAVERN_ROOM6/CAVE_ON_WATER"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM7/SOUTH -> REGION_SEAFLOOR_CAVERN_ROOM7/NORTH"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM7/NORTH -> REGION_SEAFLOOR_CAVERN_ROOM7/SOUTH"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM8/NORTH -> REGION_SEAFLOOR_CAVERN_ROOM8/SOUTH"),
        can_strength
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM8/SOUTH -> REGION_SEAFLOOR_CAVERN_ROOM8/NORTH"),
        can_strength
    )
    if "Seafloor Cavern Aqua Grunt" not in world.options.remove_roadblocks.value:
        set_rule(
            get_entrance("MAP_SEAFLOOR_CAVERN_ENTRANCE:1/MAP_SEAFLOOR_CAVERN_ROOM1:0"),
            lambda state: state.has("EVENT_STEVEN_GIVES_DIVE", world.player)
        )

    # Pacifidlog Town
    set_rule(
        get_entrance("REGION_PACIFIDLOG_TOWN/MAIN -> REGION_ROUTE131/MAIN"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_PACIFIDLOG_TOWN/MAIN -> REGION_ROUTE132/EAST"),
        can_surf
    )

    # Sky Pillar
    set_rule(
        get_entrance("MAP_SKY_PILLAR_OUTSIDE:1/MAP_SKY_PILLAR_1F:0"),
        lambda state: state.has("EVENT_WALLACE_GOES_TO_SKY_PILLAR", world.player)
    )
    # Sky Pillar does not require the mach bike until Rayquaza returns, which means the top
    # is only logically locked behind the mach bike after the top has been reached already
    # set_rule(
    #     get_entrance("REGION_SKY_PILLAR_2F/RIGHT -> REGION_SKY_PILLAR_2F/LEFT"),
    #     lambda state: has_mach_bike(state)
    # )
    # set_rule(
    #     get_entrance("REGION_SKY_PILLAR_2F/LEFT -> REGION_SKY_PILLAR_2F/RIGHT"),
    #     lambda state: has_mach_bike(state)
    # )
    # set_rule(
    #     get_entrance("REGION_SKY_PILLAR_4F/MAIN -> REGION_SKY_PILLAR_4F/ABOVE_3F_TOP_CENTER"),
    #     lambda state: has_mach_bike(state)
    # )

    # Route 134
    set_rule(
        get_entrance("REGION_ROUTE134/MAIN -> REGION_UNDERWATER_ROUTE134/MAIN"),
        can_dive
    )

    # Ever Grande City
    set_rule(
        get_entrance("REGION_EVER_GRANDE_CITY/SEA -> REGION_EVER_GRANDE_CITY/SOUTH"),
        can_waterfall
    )
    set_rule(
        get_entrance("REGION_EVER_GRANDE_CITY/SOUTH -> REGION_EVER_GRANDE_CITY/SEA"),
        can_surf
    )

    # Victory Road
    set_rule(
        get_entrance("REGION_VICTORY_ROAD_B1F/SOUTH_WEST_MAIN -> REGION_VICTORY_ROAD_B1F/SOUTH_WEST_LADDER_UP"),
        lambda state: can_rock_smash(state) and can_strength(state)
    )
    set_rule(
        get_entrance("REGION_VICTORY_ROAD_B1F/SOUTH_WEST_LADDER_UP -> REGION_VICTORY_ROAD_B1F/SOUTH_WEST_MAIN"),
        lambda state: can_rock_smash(state) and can_strength(state)
    )
    set_rule(
        get_entrance("REGION_VICTORY_ROAD_B1F/MAIN_UPPER -> REGION_VICTORY_ROAD_B1F/MAIN_LOWER_EAST"),
        lambda state: can_rock_smash(state) and can_strength(state)
    )
    set_rule(
        get_entrance("REGION_VICTORY_ROAD_B1F/MAIN_LOWER_EAST -> REGION_VICTORY_ROAD_B1F/MAIN_LOWER_WEST"),
        can_rock_smash
    )
    set_rule(
        get_entrance("REGION_VICTORY_ROAD_B1F/MAIN_LOWER_WEST -> REGION_VICTORY_ROAD_B1F/MAIN_LOWER_EAST"),
        lambda state: can_rock_smash(state) and can_strength(state)
    )
    set_rule(
        get_entrance("REGION_VICTORY_ROAD_B1F/MAIN_LOWER_WEST -> REGION_VICTORY_ROAD_B1F/MAIN_UPPER"),
        lambda state: can_rock_smash(state) and can_strength(state)
    )
    set_rule(
        get_entrance("REGION_VICTORY_ROAD_B2F/LOWER_WEST -> REGION_VICTORY_ROAD_B2F/LOWER_WEST_WATER"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_VICTORY_ROAD_B2F/LOWER_WEST_ISLAND -> REGION_VICTORY_ROAD_B2F/LOWER_WEST_WATER"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_VICTORY_ROAD_B2F/LOWER_EAST -> REGION_VICTORY_ROAD_B2F/LOWER_EAST_WATER"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_VICTORY_ROAD_B2F/LOWER_WEST_WATER -> REGION_VICTORY_ROAD_B2F/UPPER_WATER"),
        can_waterfall
    )
    set_rule(
        get_entrance("REGION_VICTORY_ROAD_B2F/LOWER_EAST_WATER -> REGION_VICTORY_ROAD_B2F/UPPER_WATER"),
        can_waterfall
    )
    set_rule(
        get_entrance("REGION_VICTORY_ROAD_B2F/UPPER -> REGION_VICTORY_ROAD_B2F/UPPER_WATER"),
        can_surf
    )
    set_rule(
        get_entrance("REGION_VICTORY_ROAD_B2F/UPPER -> REGION_VICTORY_ROAD_B2F/LOWER_EAST_WATER"),
        can_surf
    )

    # Pokemon League
    if world.options.elite_four_requirement == EliteFourRequirement.option_badges:
        set_rule(
            get_entrance("REGION_EVER_GRANDE_CITY_POKEMON_LEAGUE_1F/MAIN -> REGION_EVER_GRANDE_CITY_POKEMON_LEAGUE_1F/BEHIND_BADGE_CHECKERS"),
            lambda state: state.has_group("Badges", world.player, world.options.elite_four_count.value)
        )
    else:
        set_rule(
            get_entrance("REGION_EVER_GRANDE_CITY_POKEMON_LEAGUE_1F/MAIN -> REGION_EVER_GRANDE_CITY_POKEMON_LEAGUE_1F/BEHIND_BADGE_CHECKERS"),
            lambda state: defeated_n_gym_leaders(state, world.options.elite_four_count.value)
        )

    # Battle Frontier
    # set_rule(
    #     get_entrance("REGION_BATTLE_FRONTIER_OUTSIDE_WEST/DOCK -> REGION_LILYCOVE_CITY_HARBOR/MAIN"),
    #     lambda state: state.has("S.S. Ticket", world.player) and
    #         (state.has("EVENT_DEFEAT_CHAMPION", world.player) or world.options.enable_ferry.value == Toggle.option_true)
    # )
    # set_rule(
    #     get_entrance("REGION_BATTLE_FRONTIER_OUTSIDE_WEST/DOCK -> REGION_SLATEPORT_CITY_HARBOR/MAIN"),
    #     lambda state: state.has("S.S. Ticket", world.player) and
    #         (state.has("EVENT_DEFEAT_CHAMPION", world.player) or world.options.enable_ferry.value == Toggle.option_true)
    # )
    # set_rule(
    #     get_entrance("REGION_BATTLE_FRONTIER_OUTSIDE_WEST/CAVE_ENTRANCE -> REGION_BATTLE_FRONTIER_OUTSIDE_WEST/WATER"),
    #     can_surf
    # )
    # set_rule(
    #     get_entrance("REGION_BATTLE_FRONTIER_OUTSIDE_EAST/MAIN -> REGION_BATTLE_FRONTIER_OUTSIDE_EAST/ABOVE_WATERFALL"),
    #     lambda state: state.has("Wailmer Pail", world.player) and can_surf(state)
    # )
    # set_rule(
    #     get_entrance("REGION_BATTLE_FRONTIER_OUTSIDE_EAST/ABOVE_WATERFALL -> REGION_BATTLE_FRONTIER_OUTSIDE_EAST/MAIN"),
    #     lambda state: state.has("ITEM_WAILMER_PAIL", world.player)
    # )
    # set_rule(
    #     get_entrance("REGION_BATTLE_FRONTIER_OUTSIDE_EAST/WATER -> REGION_BATTLE_FRONTIER_OUTSIDE_EAST/ABOVE_WATERFALL"),
    #     can_waterfall
    # )

    # Overworld Items
    if world.options.overworld_items:
        # Route 103
        set_rule(
            get_location("ITEM_ROUTE_103_PP_UP"),
            can_cut
        )
        set_rule(
            get_location("ITEM_ROUTE_103_GUARD_SPEC"),
            can_cut
        )

        # Route 104
        set_rule(
            get_location("ITEM_ROUTE_104_X_ACCURACY"),
            lambda state: can_surf(state) or can_cut(state)
        )
        set_rule(
            get_location("ITEM_ROUTE_104_PP_UP"),
            can_surf
        )

        # Route 117
        set_rule(
            get_location("ITEM_ROUTE_117_REVIVE"),
            can_cut
        )

        # Route 114
        set_rule(
            get_location("ITEM_ROUTE_114_PROTEIN"),
            can_rock_smash
        )

        # Safari Zone
        set_rule(
            get_location("ITEM_SAFARI_ZONE_NORTH_WEST_TM22"),
            can_surf
        )
        set_rule(
            get_location("ITEM_SAFARI_ZONE_SOUTH_WEST_MAX_REVIVE"),
            can_surf
        )
        set_rule(
            get_location("ITEM_SAFARI_ZONE_SOUTH_EAST_BIG_PEARL"),
            can_surf
        )

        # Victory Road
        set_rule(
            get_location("ITEM_VICTORY_ROAD_B1F_FULL_RESTORE"),
            lambda state: can_rock_smash(state) and can_strength(state)
        )

    # Hidden Items
    if world.options.hidden_items:
        # Route 120
        set_rule(
            get_location("HIDDEN_ITEM_ROUTE_120_RARE_CANDY_1"),
            can_cut
        )

        # Route 121
        set_rule(
            get_location("HIDDEN_ITEM_ROUTE_121_NUGGET"),
            can_cut
        )

    # NPC Gifts
    if world.options.npc_gifts:
        # Littleroot Town
        set_rule(
            get_location("NPC_GIFT_RECEIVED_AMULET_COIN"),
            lambda state: state.has("EVENT_TALK_TO_MR_STONE", world.player) and state.has("Balance Badge", world.player)
        )

        # Petalburg City
        set_rule(
            get_location("NPC_GIFT_RECEIVED_TM36"),
            lambda state: state.has("EVENT_DEFEAT_NORMAN", world.player)
        )

        # Route 104
        set_rule(
            get_location("NPC_GIFT_RECEIVED_WHITE_HERB"),
            lambda state: state.has("Dynamo Badge", world.player) and state.has("EVENT_MEET_FLOWER_SHOP_OWNER", world.player)
        )

        # Devon Corp
        set_rule(
            get_location("NPC_GIFT_RECEIVED_EXP_SHARE"),
            lambda state: state.has("EVENT_DELIVER_LETTER", world.player)
        )

        # Slateport City
        set_rule(
            get_location("NPC_GIFT_RECEIVED_DEEP_SEA_TOOTH"),
            lambda state: state.has("EVENT_AQUA_STEALS_SUBMARINE", world.player)
                          and state.has("Scanner", world.player)
                          and state.has("Mind Badge", world.player)
        )
        set_rule(
            get_location("NPC_GIFT_RECEIVED_DEEP_SEA_SCALE"),
            lambda state: state.has("EVENT_AQUA_STEALS_SUBMARINE", world.player)
                          and state.has("Scanner", world.player)
                          and state.has("Mind Badge", world.player)
        )

        # Route 116
        set_rule(
            get_location("NPC_GIFT_RECEIVED_REPEAT_BALL"),
            lambda state: state.has("EVENT_RESCUE_CAPT_STERN", world.player)
        )

        # Mauville City
        set_rule(
            get_location("NPC_GIFT_GOT_TM24_FROM_WATTSON"),
            lambda state: state.has("EVENT_DEFEAT_NORMAN", world.player) and state.has("EVENT_TURN_OFF_GENERATOR", world.player)
        )
        set_rule(
            get_location("NPC_GIFT_RECEIVED_COIN_CASE"),
            lambda state: state.has("EVENT_BUY_HARBOR_MAIL", world.player)
        )

        # Fallarbor Town
        set_rule(
            get_location("NPC_GIFT_RECEIVED_TM27"),
            lambda state: state.has("EVENT_RECOVER_METEORITE", world.player) and state.has("Meteorite", world.player)
        )

        # Fortree City
        set_rule(
            get_location("NPC_GIFT_RECEIVED_MENTAL_HERB"),
            lambda state: state.has("EVENT_WINGULL_QUEST_2", world.player)
        )

    # Ferry Items
    if world.options.enable_ferry:
        set_rule(
            get_location("NPC_GIFT_RECEIVED_SS_TICKET"),
            lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player)
        )
        set_rule(
            get_entrance("REGION_SLATEPORT_CITY_HARBOR/MAIN -> REGION_SS_TIDAL_CORRIDOR/MAIN"),
            lambda state: state.has("S.S. Ticket", world.player)
        )
        set_rule(
            get_entrance("REGION_LILYCOVE_CITY_HARBOR/MAIN -> REGION_SS_TIDAL_CORRIDOR/MAIN"),
            lambda state: state.has("S.S. Ticket", world.player)
        )

    # Add Itemfinder requirement to hidden items
    if world.options.require_itemfinder:
        for location in world.multiworld.get_locations(world.player):
            if location.tags is not None and "HiddenItem" in location.tags:
                add_rule(
                    location,
                    lambda state: state.has("Itemfinder", world.player)
                )

    # Add Flash requirements to dark caves
    if world.options.require_flash:
        # Granite Cave
        add_rule(
            get_entrance("MAP_GRANITE_CAVE_1F:2/MAP_GRANITE_CAVE_B1F:1"),
            can_flash
        )
        add_rule(
            get_entrance("MAP_GRANITE_CAVE_B1F:3/MAP_GRANITE_CAVE_B2F:1"),
            can_flash
        )

        # Victory Road
        add_rule(
            get_entrance("MAP_VICTORY_ROAD_1F:2/MAP_VICTORY_ROAD_B1F:5"),
            can_flash
        )
        add_rule(
            get_entrance("MAP_VICTORY_ROAD_1F:4/MAP_VICTORY_ROAD_B1F:4"),
            can_flash
        )
        add_rule(
            get_entrance("MAP_VICTORY_ROAD_1F:3/MAP_VICTORY_ROAD_B1F:2"),
            can_flash
        )
        add_rule(
            get_entrance("MAP_VICTORY_ROAD_B1F:3/MAP_VICTORY_ROAD_B2F:1"),
            can_flash
        )
        add_rule(
            get_entrance("MAP_VICTORY_ROAD_B1F:1/MAP_VICTORY_ROAD_B2F:2"),
            can_flash
        )
        add_rule(
            get_entrance("MAP_VICTORY_ROAD_B1F:6/MAP_VICTORY_ROAD_B2F:3"),
            can_flash
        )
        add_rule(
            get_entrance("MAP_VICTORY_ROAD_B1F:0/MAP_VICTORY_ROAD_B2F:0"),
            can_flash
        )
        add_rule(
            get_entrance("MAP_VICTORY_ROAD_B2F:3/MAP_VICTORY_ROAD_B1F:6"),
            can_flash
        )
        add_rule(
            get_entrance("MAP_VICTORY_ROAD_B2F:2/MAP_VICTORY_ROAD_B1F:1"),
            can_flash
        )
        add_rule(
            get_entrance("MAP_VICTORY_ROAD_B2F:0/MAP_VICTORY_ROAD_B1F:0"),
            can_flash
        )
        add_rule(
            get_entrance("MAP_VICTORY_ROAD_B2F:1/MAP_VICTORY_ROAD_B1F:3"),
            can_flash
        )
