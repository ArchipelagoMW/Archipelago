"""
Logic rule definitions for Pokemon Emerald
"""
from typing import TYPE_CHECKING, Callable, Dict

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule

from .data import LocationCategory, NATIONAL_ID_TO_SPECIES_ID, NUM_REAL_SPECIES, data
from .locations import PokemonEmeraldLocation
from .options import DarkCavesRequireFlash, EliteFourRequirement, NormanRequirement, Goal

if TYPE_CHECKING:
    from . import PokemonEmeraldWorld


# Rules are organized by town/route/dungeon and ordered approximately
# by when you would first reach that place in a vanilla playthrough.
def set_rules(world: "PokemonEmeraldWorld") -> None:
    hm_rules: Dict[str, Callable[[CollectionState], bool]] = {}
    for hm, badges in world.hm_requirements.items():
        if isinstance(badges, list):
            hm_rules[hm] = lambda state, hm=hm, badges=badges: \
                state.has(hm, world.player) and state.has_all(badges, world.player)
        else:
            hm_rules[hm] = lambda state, hm=hm, badges=badges: \
                state.has(hm, world.player) and state.has_group_unique("Badge", world.player, badges)

    def has_acro_bike(state: CollectionState):
        return state.has("Acro Bike", world.player)

    def has_mach_bike(state: CollectionState):
        return state.has("Mach Bike", world.player)

    def defeated_n_gym_leaders(state: CollectionState, n: int) -> bool:
        return state.has_from_list_unique([
            "EVENT_DEFEAT_ROXANNE",
            "EVENT_DEFEAT_BRAWLY",
            "EVENT_DEFEAT_WATTSON",
            "EVENT_DEFEAT_FLANNERY",
            "EVENT_DEFEAT_NORMAN",
            "EVENT_DEFEAT_WINONA",
            "EVENT_DEFEAT_TATE_AND_LIZA",
            "EVENT_DEFEAT_JUAN",
        ], world.player, n)

    huntable_legendary_events = [
        f"EVENT_ENCOUNTER_{key}"
        for name, key in {
            "Groudon": "GROUDON",
            "Kyogre": "KYOGRE",
            "Rayquaza": "RAYQUAZA",
            "Latias": "LATIAS",
            "Latios": "LATIOS",
            "Regirock": "REGIROCK",
            "Regice": "REGICE",
            "Registeel": "REGISTEEL",
            "Mew": "MEW",
            "Deoxys": "DEOXYS",
            "Ho-Oh": "HO_OH",
            "Lugia": "LUGIA",
        }.items()
        if name in world.options.allowed_legendary_hunt_encounters.value
    ]

    def encountered_n_legendaries(state: CollectionState, n: int) -> bool:
        return state.has_from_list_unique(huntable_legendary_events, world.player, n)

    def get_entrance(entrance: str):
        return world.multiworld.get_entrance(entrance, world.player)

    def get_location(location: str):
        if location in data.locations:
            location = data.locations[location].label

        return world.multiworld.get_location(location, world.player)

    if world.options.goal == Goal.option_champion:
        completion_condition = lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player)
    elif world.options.goal == Goal.option_steven:
        completion_condition = lambda state: state.has("EVENT_DEFEAT_STEVEN", world.player)
    elif world.options.goal == Goal.option_norman:
        completion_condition = lambda state: state.has("EVENT_DEFEAT_NORMAN", world.player)
    elif world.options.goal == Goal.option_legendary_hunt:
        completion_condition = lambda state: encountered_n_legendaries(state, world.options.legendary_hunt_count.value)

    world.multiworld.completion_condition[world.player] = completion_condition

    if world.options.legendary_hunt_catch:
        set_rule(get_location("EVENT_ENCOUNTER_GROUDON"),
                 lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player))
        set_rule(get_location("EVENT_ENCOUNTER_KYOGRE"),
                 lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player))
        set_rule(get_location("EVENT_ENCOUNTER_RAYQUAZA"),
                 lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player))
        set_rule(get_location("EVENT_ENCOUNTER_LATIAS"),
                 lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player))
        # Latios already only requires defeating the champion and access to Route 117
        # set_rule(get_location("EVENT_ENCOUNTER_LATIOS"),
        #          lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player))
        set_rule(get_location("EVENT_ENCOUNTER_REGIROCK"),
                 lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player))
        set_rule(get_location("EVENT_ENCOUNTER_REGICE"),
                 lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player))
        set_rule(get_location("EVENT_ENCOUNTER_REGISTEEL"),
                 lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player))
        set_rule(get_location("EVENT_ENCOUNTER_MEW"),
                 lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player))
        set_rule(get_location("EVENT_ENCOUNTER_DEOXYS"),
                 lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player))
        set_rule(get_location("EVENT_ENCOUNTER_HO_OH"),
                 lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player))
        set_rule(get_location("EVENT_ENCOUNTER_LUGIA"),
                 lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player))

    # Sky
    set_rule(
        get_entrance("REGION_LITTLEROOT_TOWN/MAIN -> REGION_SKY"),
        hm_rules["HM02 Fly"]
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

    # Littleroot Town
    set_rule(
        get_location("NPC_GIFT_RECEIVED_SS_TICKET"),
        lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player)
    )
    set_rule(
        get_location("NPC_GIFT_RECEIVED_AURORA_TICKET"),
        lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player)
    )
    set_rule(
        get_location("NPC_GIFT_RECEIVED_EON_TICKET"),
        lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player)
    )
    set_rule(
        get_location("NPC_GIFT_RECEIVED_MYSTIC_TICKET"),
        lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player)
    )
    set_rule(
        get_location("NPC_GIFT_RECEIVED_OLD_SEA_MAP"),
        lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player)
    )

    # Route 102
    set_rule(
        get_entrance("REGION_ROUTE102/MAIN -> REGION_ROUTE102/POND"),
        hm_rules["HM03 Surf"]
    )

    # Route 103
    set_rule(
        get_entrance("REGION_ROUTE103/EAST -> REGION_ROUTE103/WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_ROUTE103/WEST -> REGION_ROUTE103/WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_ROUTE103/EAST -> REGION_ROUTE103/EAST_TREE_MAZE"),
        hm_rules["HM01 Cut"]
    )

    # Petalburg City
    set_rule(
        get_entrance("REGION_PETALBURG_CITY/MAIN -> REGION_PETALBURG_CITY/SOUTH_POND"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_PETALBURG_CITY/MAIN -> REGION_PETALBURG_CITY/NORTH_POND"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_location("NPC_GIFT_RECEIVED_HM_SURF"),
        lambda state: state.has("EVENT_DEFEAT_NORMAN", world.player)
    )
    if world.options.norman_requirement == NormanRequirement.option_badges:
        set_rule(
            get_entrance("MAP_PETALBURG_CITY_GYM:2/MAP_PETALBURG_CITY_GYM:3"),
            lambda state: state.has_group_unique("Badge", world.player, world.options.norman_count.value)
        )
        set_rule(
            get_entrance("MAP_PETALBURG_CITY_GYM:5/MAP_PETALBURG_CITY_GYM:6"),
            lambda state: state.has_group_unique("Badge", world.player, world.options.norman_count.value)
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
        get_entrance("REGION_ROUTE104/SOUTH -> REGION_ROUTE104/SOUTH_WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_ROUTE104/NORTH -> REGION_ROUTE104/NORTH_POND"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_ROUTE104/NORTH -> REGION_ROUTE104/TREE_ALCOVE_2"),
        hm_rules["HM01 Cut"]
    )
    set_rule(
        get_entrance("REGION_ROUTE104_MR_BRINEYS_HOUSE/MAIN -> REGION_DEWFORD_TOWN/MAIN"),
        lambda state: state.has("EVENT_TALK_TO_MR_STONE", world.player)
    )

    # Petalburg Woods
    set_rule(
        get_entrance("REGION_PETALBURG_WOODS/WEST_PATH -> REGION_PETALBURG_WOODS/EAST_PATH"),
        hm_rules["HM01 Cut"]
    )

    # Rustboro City
    set_rule(
        get_location("EVENT_RETURN_DEVON_GOODS"),
        lambda state: state.has("EVENT_RECOVER_DEVON_GOODS", world.player)
    )
    if world.options.trainersanity:
        set_rule(
            get_location("TRAINER_BRENDAN_RUSTBORO_MUDKIP_REWARD"),
            lambda state: state.has("EVENT_RETURN_DEVON_GOODS", world.player)
        )

    # Devon Corp
    set_rule(
        get_entrance("MAP_RUSTBORO_CITY_DEVON_CORP_1F:2/MAP_RUSTBORO_CITY_DEVON_CORP_2F:0"),
        lambda state: state.has("EVENT_RETURN_DEVON_GOODS", world.player)
    )

    # Route 116
    set_rule(
        get_entrance("REGION_ROUTE116/WEST -> REGION_ROUTE116/WEST_ABOVE_LEDGE"),
        hm_rules["HM01 Cut"]
    )
    set_rule(
        get_entrance("REGION_ROUTE116/EAST -> REGION_TERRA_CAVE_ENTRANCE/MAIN"),
        lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player)
            and state.has("TERRA_CAVE_ROUTE_116_1", world.player)
            and state.has("EVENT_DEFEAT_SHELLY", world.player)
    )
    set_rule(
        get_entrance("REGION_ROUTE116/WEST -> REGION_TERRA_CAVE_ENTRANCE/MAIN"),
        lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player)
            and state.has("TERRA_CAVE_ROUTE_116_2", world.player)
            and state.has("EVENT_DEFEAT_SHELLY", world.player)
    )

    # Rusturf Tunnel
    set_rule(
        get_entrance("REGION_RUSTURF_TUNNEL/WEST -> REGION_RUSTURF_TUNNEL/EAST"),
        hm_rules["HM06 Rock Smash"]
    )
    set_rule(
        get_entrance("REGION_RUSTURF_TUNNEL/EAST -> REGION_RUSTURF_TUNNEL/WEST"),
        hm_rules["HM06 Rock Smash"]
    )
    set_rule(
        get_location("NPC_GIFT_RECEIVED_HM_STRENGTH"),
        hm_rules["HM06 Rock Smash"]
    )
    set_rule(
        get_location("EVENT_RECOVER_DEVON_GOODS"),
        lambda state: state.has("EVENT_DEFEAT_ROXANNE", world.player)
    )

    # Route 115
    set_rule(
        get_entrance("REGION_ROUTE115/SOUTH_BELOW_LEDGE -> REGION_ROUTE115/SEA"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_ROUTE115/SOUTH_BEACH_NEAR_CAVE -> REGION_ROUTE115/SEA"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_ROUTE115/SOUTH_ABOVE_LEDGE -> REGION_ROUTE115/SOUTH_BEHIND_ROCK"),
        hm_rules["HM06 Rock Smash"]
    )
    set_rule(
        get_entrance("REGION_ROUTE115/NORTH_BELOW_SLOPE -> REGION_ROUTE115/SEA"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_ROUTE115/NORTH_BELOW_SLOPE -> REGION_ROUTE115/NORTH_ABOVE_SLOPE"),
        has_mach_bike
    )
    set_rule(
        get_entrance("REGION_ROUTE115/NORTH_BELOW_SLOPE -> REGION_TERRA_CAVE_ENTRANCE/MAIN"),
        lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player)
            and state.has("TERRA_CAVE_ROUTE_115_1", world.player)
            and state.has("EVENT_DEFEAT_SHELLY",  world.player)
    )
    set_rule(
        get_entrance("REGION_ROUTE115/NORTH_ABOVE_SLOPE -> REGION_TERRA_CAVE_ENTRANCE/MAIN"),
        lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player)
            and state.has("TERRA_CAVE_ROUTE_115_2", world.player)
            and state.has("EVENT_DEFEAT_SHELLY",  world.player)
    )

    if world.options.extra_boulders:
        set_rule(
            get_entrance("REGION_ROUTE115/SOUTH_BEACH_NEAR_CAVE -> REGION_ROUTE115/SOUTH_ABOVE_LEDGE"),
            hm_rules["HM04 Strength"]
        )
        set_rule(
            get_entrance("REGION_ROUTE115/SOUTH_ABOVE_LEDGE -> REGION_ROUTE115/SOUTH_BEACH_NEAR_CAVE"),
            hm_rules["HM04 Strength"]
        )

    if world.options.extra_bumpy_slope:
        set_rule(
            get_entrance("REGION_ROUTE115/SOUTH_BELOW_LEDGE -> REGION_ROUTE115/SOUTH_ABOVE_LEDGE"),
            has_acro_bike
        )
    else:
        set_rule(
            get_entrance("REGION_ROUTE115/SOUTH_BELOW_LEDGE -> REGION_ROUTE115/SOUTH_ABOVE_LEDGE"),
            lambda state: False
        )

    # Route 105
    set_rule(
        get_entrance("REGION_UNDERWATER_ROUTE105/MARINE_CAVE_ENTRANCE_1 -> REGION_UNDERWATER_MARINE_CAVE/MAIN"),
        lambda state: hm_rules["HM08 Dive"](state)
            and state.has("EVENT_DEFEAT_CHAMPION", world.player)
            and state.has("MARINE_CAVE_ROUTE_105_1", world.player)
            and state.has("EVENT_DEFEAT_SHELLY", world.player)
    )
    set_rule(
        get_entrance("REGION_UNDERWATER_ROUTE105/MARINE_CAVE_ENTRANCE_2 -> REGION_UNDERWATER_MARINE_CAVE/MAIN"),
        lambda state: hm_rules["HM08 Dive"](state)
            and state.has("EVENT_DEFEAT_CHAMPION", world.player)
            and state.has("MARINE_CAVE_ROUTE_105_2", world.player)
            and state.has("EVENT_DEFEAT_SHELLY", world.player)
    )
    set_rule(
        get_entrance("MAP_ROUTE105:0/MAP_ISLAND_CAVE:0"),
        lambda state: state.has("EVENT_UNDO_REGI_SEAL", world.player)
    )

    # Route 106
    set_rule(
        get_entrance("REGION_ROUTE106/EAST -> REGION_ROUTE106/SEA"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_ROUTE106/WEST -> REGION_ROUTE106/SEA"),
        hm_rules["HM03 Surf"]
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
    set_rule(
        get_entrance("REGION_DEWFORD_TOWN/MAIN -> REGION_DEWFORD_TOWN/WATER"),
        hm_rules["HM03 Surf"]
    )

    # Granite Cave
    set_rule(
        get_entrance("REGION_GRANITE_CAVE_STEVENS_ROOM/MAIN -> REGION_GRANITE_CAVE_STEVENS_ROOM/LETTER_DELIVERED"),
        lambda state: state.has("Letter", world.player)
    )
    set_rule(
        get_entrance("REGION_GRANITE_CAVE_B1F/LOWER -> REGION_GRANITE_CAVE_B1F/UPPER"),
        has_mach_bike
    )

    # Route 107
    set_rule(
        get_entrance("REGION_DEWFORD_TOWN/MAIN -> REGION_ROUTE107/MAIN"),
        hm_rules["HM03 Surf"]
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
        hm_rules["HM03 Surf"]
    )

    # Slateport City
    set_rule(
        get_entrance("REGION_SLATEPORT_CITY/MAIN -> REGION_SLATEPORT_CITY/WATER"),
        hm_rules["HM03 Surf"]
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
        lambda state: state.has("S.S. Ticket", world.player)
    )

    # Route 110
    set_rule(
        get_entrance("REGION_ROUTE110/MAIN -> REGION_ROUTE110/SOUTH_WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_ROUTE110/MAIN -> REGION_ROUTE110/NORTH_WATER"),
        hm_rules["HM03 Surf"]
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

    # Trick House
    set_rule(
        get_entrance("REGION_ROUTE110_TRICK_HOUSE_PUZZLE1/ENTRANCE -> REGION_ROUTE110_TRICK_HOUSE_PUZZLE1/REWARDS"),
        hm_rules["HM01 Cut"]
    )
    set_rule(
        get_entrance("REGION_ROUTE110_TRICK_HOUSE_ENTRANCE/MAIN -> REGION_ROUTE110_TRICK_HOUSE_PUZZLE2/ENTRANCE"),
        lambda state: state.has("Dynamo Badge", world.player) and state.has("EVENT_COMPLETE_TRICK_HOUSE_1", world.player)
    )
    set_rule(
        get_entrance("REGION_ROUTE110_TRICK_HOUSE_ENTRANCE/MAIN -> REGION_ROUTE110_TRICK_HOUSE_PUZZLE3/ENTRANCE"),
        lambda state: state.has("Heat Badge", world.player) and state.has("EVENT_COMPLETE_TRICK_HOUSE_2", world.player)
    )
    set_rule(
        get_entrance("REGION_ROUTE110_TRICK_HOUSE_PUZZLE3/ENTRANCE -> REGION_ROUTE110_TRICK_HOUSE_PUZZLE3/REWARDS"),
        hm_rules["HM06 Rock Smash"]
    )
    set_rule(
        get_entrance("REGION_ROUTE110_TRICK_HOUSE_ENTRANCE/MAIN -> REGION_ROUTE110_TRICK_HOUSE_PUZZLE4/ENTRANCE"),
        lambda state: state.has("Balance Badge", world.player) and state.has("EVENT_COMPLETE_TRICK_HOUSE_3", world.player)
    )
    set_rule(
        get_entrance("REGION_ROUTE110_TRICK_HOUSE_PUZZLE4/ENTRANCE -> REGION_ROUTE110_TRICK_HOUSE_PUZZLE4/REWARDS"),
        hm_rules["HM04 Strength"]
    )
    set_rule(
        get_entrance("REGION_ROUTE110_TRICK_HOUSE_ENTRANCE/MAIN -> REGION_ROUTE110_TRICK_HOUSE_PUZZLE5/ENTRANCE"),
        lambda state: state.has("Feather Badge", world.player) and state.has("EVENT_COMPLETE_TRICK_HOUSE_4", world.player)
    )
    set_rule(
        get_entrance("REGION_ROUTE110_TRICK_HOUSE_ENTRANCE/MAIN -> REGION_ROUTE110_TRICK_HOUSE_PUZZLE6/ENTRANCE"),
        lambda state: state.has("Mind Badge", world.player) and state.has("EVENT_COMPLETE_TRICK_HOUSE_5", world.player)
    )
    set_rule(
        get_entrance("REGION_ROUTE110_TRICK_HOUSE_ENTRANCE/MAIN -> REGION_ROUTE110_TRICK_HOUSE_PUZZLE7/ENTRANCE"),
        lambda state: state.has("Rain Badge", world.player) and state.has("EVENT_COMPLETE_TRICK_HOUSE_6", world.player)
    )
    set_rule(
        get_entrance("REGION_ROUTE110_TRICK_HOUSE_ENTRANCE/MAIN -> REGION_ROUTE110_TRICK_HOUSE_PUZZLE8/ENTRANCE"),
        lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player) and state.has("EVENT_COMPLETE_TRICK_HOUSE_7", world.player)
    )

    # Mauville City
    set_rule(
        get_location("NPC_GIFT_GOT_BASEMENT_KEY_FROM_WATTSON"),
        lambda state: state.has("EVENT_DEFEAT_NORMAN", world.player)
    )
    set_rule(
        get_location("NPC_GIFT_RECEIVED_COIN_CASE"),
        lambda state: state.has("EVENT_BUY_HARBOR_MAIL", world.player)
    )

    # Route 117
    set_rule(
        get_entrance("REGION_ROUTE117/MAIN -> REGION_ROUTE117/PONDS"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_location("EVENT_ENCOUNTER_LATIOS"),
        lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player)
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
        get_entrance("REGION_ROUTE111/NORTH -> REGION_ROUTE111/ABOVE_SLOPE"),
        has_mach_bike
    )
    set_rule(
        get_entrance("REGION_ROUTE111/MIDDLE -> REGION_ROUTE111/SOUTH"),
        hm_rules["HM06 Rock Smash"]
    )
    set_rule(
        get_entrance("REGION_ROUTE111/SOUTH -> REGION_ROUTE111/SOUTH_POND"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_ROUTE111/SOUTH -> REGION_ROUTE111/MIDDLE"),
        hm_rules["HM06 Rock Smash"]
    )
    set_rule(
        get_entrance("MAP_ROUTE111:4/MAP_TRAINER_HILL_ENTRANCE:0"),
        lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player)
    )
    set_rule(
        get_entrance("MAP_ROUTE111:1/MAP_DESERT_RUINS:0"),
        lambda state: state.has("EVENT_UNDO_REGI_SEAL", world.player)
    )
    set_rule(
        get_entrance("MAP_DESERT_RUINS:0/MAP_ROUTE111:1"),
        hm_rules["HM06 Rock Smash"]
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
        hm_rules["HM04 Strength"]
    )

    # Route 114
    set_rule(
        get_entrance("REGION_ROUTE114/MAIN -> REGION_ROUTE114/WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_ROUTE114/WATER -> REGION_ROUTE114/ABOVE_WATERFALL"),
        hm_rules["HM07 Waterfall"]
    )
    set_rule(
        get_entrance("MAP_ROUTE114_FOSSIL_MANIACS_TUNNEL:2/MAP_DESERT_UNDERPASS:0"),
        lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player)
    )
    set_rule(
        get_entrance("REGION_ROUTE114/ABOVE_WATERFALL -> REGION_TERRA_CAVE_ENTRANCE/MAIN"),
        lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player)
            and state.has("TERRA_CAVE_ROUTE_114_1", world.player)
            and state.has("EVENT_DEFEAT_SHELLY", world.player)
    )
    set_rule(
        get_entrance("REGION_ROUTE114/MAIN -> REGION_TERRA_CAVE_ENTRANCE/MAIN"),
        lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player)
            and state.has("TERRA_CAVE_ROUTE_114_2", world.player)
            and state.has("EVENT_DEFEAT_SHELLY", world.player)
    )

    # Meteor Falls
    set_rule(
        get_entrance("REGION_METEOR_FALLS_1F_1R/MAIN -> REGION_METEOR_FALLS_1F_1R/WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_METEOR_FALLS_1F_1R/WATER -> REGION_METEOR_FALLS_1F_1R/WATER_ABOVE_WATERFALL"),
        hm_rules["HM07 Waterfall"]
    )
    set_rule(
        get_entrance("REGION_METEOR_FALLS_1F_1R/ABOVE_WATERFALL -> REGION_METEOR_FALLS_1F_1R/WATER_ABOVE_WATERFALL"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("MAP_METEOR_FALLS_1F_1R:5/MAP_METEOR_FALLS_STEVENS_CAVE:0"),
        lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player)
    )
    set_rule(
        get_entrance("REGION_METEOR_FALLS_1F_2R/LEFT_SPLIT -> REGION_METEOR_FALLS_1F_2R/LEFT_SPLIT_WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_METEOR_FALLS_1F_2R/RIGHT_SPLIT -> REGION_METEOR_FALLS_1F_2R/RIGHT_SPLIT_WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_METEOR_FALLS_B1F_1R/HIGHEST_LADDER -> REGION_METEOR_FALLS_B1F_1R/WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_METEOR_FALLS_B1F_1R/NORTH_SHORE -> REGION_METEOR_FALLS_B1F_1R/WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_METEOR_FALLS_B1F_1R/SOUTH_SHORE -> REGION_METEOR_FALLS_B1F_1R/WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_METEOR_FALLS_B1F_2R/ENTRANCE -> REGION_METEOR_FALLS_B1F_2R/WATER"),
        hm_rules["HM03 Surf"]
    )

    # Jagged Pass
    set_rule(
        get_entrance("REGION_JAGGED_PASS/BOTTOM -> REGION_JAGGED_PASS/MIDDLE"),
        has_acro_bike
    )
    set_rule(
        get_entrance("REGION_JAGGED_PASS/MIDDLE -> REGION_JAGGED_PASS/TOP"),
        has_acro_bike
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
        has_mach_bike
    )
    set_rule(
        get_entrance("REGION_MIRAGE_TOWER_2F/BOTTOM -> REGION_MIRAGE_TOWER_2F/TOP"),
        has_mach_bike
    )
    set_rule(
        get_entrance("REGION_MIRAGE_TOWER_3F/TOP -> REGION_MIRAGE_TOWER_3F/BOTTOM"),
        hm_rules["HM06 Rock Smash"]
    )
    set_rule(
        get_entrance("REGION_MIRAGE_TOWER_3F/BOTTOM -> REGION_MIRAGE_TOWER_3F/TOP"),
        hm_rules["HM06 Rock Smash"]
    )
    set_rule(
        get_entrance("REGION_MIRAGE_TOWER_4F/MAIN -> REGION_MIRAGE_TOWER_4F/FOSSIL_PLATFORM"),
        hm_rules["HM06 Rock Smash"]
    )

    # Abandoned Ship
    set_rule(
        get_entrance("REGION_ABANDONED_SHIP_ROOMS_B1F/CENTER -> REGION_ABANDONED_SHIP_UNDERWATER1/MAIN"),
        hm_rules["HM08 Dive"]
    )
    set_rule(
        get_entrance("REGION_ABANDONED_SHIP_HIDDEN_FLOOR_CORRIDORS/MAIN -> REGION_ABANDONED_SHIP_UNDERWATER2/MAIN"),
        hm_rules["HM08 Dive"]
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
    if world.options.modify_118:
        set_rule(
            get_entrance("REGION_ROUTE118/WEST -> REGION_ROUTE118/EAST"),
            has_acro_bike
        )
        set_rule(
            get_entrance("REGION_ROUTE118/EAST -> REGION_ROUTE118/WEST"),
            has_acro_bike
        )
        set_rule(
            get_entrance("REGION_ROUTE118/WEST_WATER -> REGION_ROUTE118/EAST_WATER"),
            lambda state: False
        )
        set_rule(
            get_entrance("REGION_ROUTE118/EAST_WATER -> REGION_ROUTE118/WEST_WATER"),
            lambda state: False
        )
    else:
        set_rule(
            get_entrance("REGION_ROUTE118/WEST -> REGION_ROUTE118/EAST"),
            lambda state: False
        )
        set_rule(
            get_entrance("REGION_ROUTE118/EAST -> REGION_ROUTE118/WEST"),
            lambda state: False
        )

    set_rule(
        get_entrance("REGION_ROUTE118/WEST -> REGION_ROUTE118/WEST_WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_ROUTE118/EAST -> REGION_ROUTE118/EAST_WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_ROUTE118/EAST -> REGION_TERRA_CAVE_ENTRANCE/MAIN"),
        lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player)
            and state.has("TERRA_CAVE_ROUTE_118_1", world.player)
            and state.has("EVENT_DEFEAT_SHELLY", world.player)
    )
    set_rule(
        get_entrance("REGION_ROUTE118/WEST -> REGION_TERRA_CAVE_ENTRANCE/MAIN"),
        lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player)
            and state.has("TERRA_CAVE_ROUTE_118_2", world.player)
            and state.has("EVENT_DEFEAT_SHELLY", world.player)
    )

    # Route 119
    set_rule(
        get_entrance("REGION_ROUTE119/LOWER -> REGION_ROUTE119/LOWER_WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_ROUTE119/LOWER -> REGION_ROUTE119/LOWER_ACROSS_RAILS"),
        has_acro_bike
    )
    set_rule(
        get_entrance("REGION_ROUTE119/LOWER_ACROSS_RAILS -> REGION_ROUTE119/LOWER"),
        has_acro_bike
    )
    set_rule(
        get_entrance("REGION_ROUTE119/UPPER -> REGION_ROUTE119/MIDDLE_RIVER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_ROUTE119/MIDDLE_RIVER -> REGION_ROUTE119/ABOVE_WATERFALL"),
        hm_rules["HM07 Waterfall"]
    )
    set_rule(
        get_entrance("REGION_ROUTE119/ABOVE_WATERFALL -> REGION_ROUTE119/MIDDLE_RIVER"),
        hm_rules["HM07 Waterfall"]
    )
    set_rule(
        get_entrance("REGION_ROUTE119/ABOVE_WATERFALL -> REGION_ROUTE119/ABOVE_WATERFALL_ACROSS_RAILS"),
        has_acro_bike
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
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_ROUTE120/SOUTH -> REGION_ROUTE120/SOUTH_ALCOVE"),
        hm_rules["HM01 Cut"]
    )
    set_rule(
        get_entrance("REGION_ROUTE120/SOUTH -> REGION_ROUTE120/SOUTH_PONDS"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_ROUTE120/SOUTH_ALCOVE -> REGION_ROUTE120/SOUTH"),
        hm_rules["HM01 Cut"]
    )
    set_rule(
        get_entrance("MAP_ROUTE120:0/MAP_ANCIENT_TOMB:0"),
        lambda state: state.has("EVENT_UNDO_REGI_SEAL", world.player)
    )
    set_rule(
        get_entrance("MAP_ANCIENT_TOMB:1/MAP_ANCIENT_TOMB:2"),
        hm_rules["HM05 Flash"]
    )

    # Route 121
    set_rule(
        get_entrance("REGION_ROUTE121/EAST -> REGION_ROUTE121/WEST"),
        hm_rules["HM01 Cut"]
    )
    set_rule(
        get_entrance("REGION_ROUTE121/EAST -> REGION_ROUTE121/WATER"),
        hm_rules["HM03 Surf"]
    )

    # Safari Zone
    set_rule(
        get_entrance("MAP_ROUTE121_SAFARI_ZONE_ENTRANCE:0,1/MAP_SAFARI_ZONE_SOUTH:0"),
        lambda state: state.has("Pokeblock Case", world.player)
    )
    set_rule(
        get_entrance("REGION_SAFARI_ZONE_NORTHWEST/MAIN -> REGION_SAFARI_ZONE_NORTHWEST/POND"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_SAFARI_ZONE_SOUTH/MAIN -> REGION_SAFARI_ZONE_NORTH/MAIN"),
        has_acro_bike
    )
    set_rule(
        get_entrance("REGION_SAFARI_ZONE_SOUTHWEST/MAIN -> REGION_SAFARI_ZONE_NORTHWEST/MAIN"),
        has_mach_bike
    )
    set_rule(
        get_entrance("REGION_SAFARI_ZONE_SOUTHWEST/MAIN -> REGION_SAFARI_ZONE_SOUTHWEST/POND"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_SAFARI_ZONE_SOUTHEAST/MAIN -> REGION_SAFARI_ZONE_SOUTHEAST/WATER"),
        hm_rules["HM03 Surf"]
    )
    if "Safari Zone Construction Workers" not in world.options.remove_roadblocks.value:
        set_rule(
            get_entrance("REGION_SAFARI_ZONE_SOUTH/MAIN -> REGION_SAFARI_ZONE_SOUTHEAST/MAIN"),
            lambda state: state.has("EVENT_DEFEAT_CHAMPION", world.player)
        )

    # Route 122
    set_rule(
        get_entrance("REGION_ROUTE122/MT_PYRE_ENTRANCE -> REGION_ROUTE122/SEA"),
        hm_rules["HM03 Surf"]
    )

    # Route 123
    set_rule(
        get_entrance("REGION_ROUTE123/EAST -> REGION_ROUTE122/SEA"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_ROUTE123/EAST -> REGION_ROUTE123/POND"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_ROUTE123/EAST -> REGION_ROUTE123/EAST_BEHIND_TREE"),
        hm_rules["HM01 Cut"]
    )

    # Lilycove City
    set_rule(
        get_entrance("REGION_LILYCOVE_CITY/MAIN -> REGION_LILYCOVE_CITY/SEA"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_LILYCOVE_CITY_HARBOR/MAIN -> REGION_SS_TIDAL_CORRIDOR/MAIN"),
        lambda state: state.has("S.S. Ticket", world.player)
    )
    set_rule(
        get_entrance("REGION_LILYCOVE_CITY_HARBOR/MAIN -> REGION_SOUTHERN_ISLAND_EXTERIOR/MAIN"),
        lambda state: state.has("Eon Ticket", world.player)
    )
    set_rule(
        get_entrance("REGION_LILYCOVE_CITY_HARBOR/MAIN -> REGION_FARAWAY_ISLAND_ENTRANCE/MAIN"),
        lambda state: state.has("Old Sea Map", world.player)
    )
    set_rule(
        get_entrance("REGION_LILYCOVE_CITY_HARBOR/MAIN -> REGION_BIRTH_ISLAND_HARBOR/MAIN"),
        lambda state: state.has("Aurora Ticket", world.player)
    )
    set_rule(
        get_entrance("REGION_LILYCOVE_CITY_HARBOR/MAIN -> REGION_NAVEL_ROCK_HARBOR/MAIN"),
        lambda state: state.has("Mystic Ticket", world.player)
    )

    if "Lilycove City Wailmer" not in world.options.remove_roadblocks.value:
        set_rule(
            get_entrance("REGION_LILYCOVE_CITY/SEA -> REGION_ROUTE124/MAIN"),
            lambda state: state.has("EVENT_CLEAR_AQUA_HIDEOUT", world.player)
        )
        set_rule(
            get_entrance("REGION_ROUTE124/MAIN -> REGION_LILYCOVE_CITY/SEA"),
            lambda state: state.has("EVENT_CLEAR_AQUA_HIDEOUT", world.player)
        )

    # Magma Hideout
    set_rule(
        get_entrance("REGION_MAGMA_HIDEOUT_1F/ENTRANCE -> REGION_MAGMA_HIDEOUT_1F/MAIN"),
        hm_rules["HM04 Strength"]
    )
    set_rule(
        get_entrance("REGION_MAGMA_HIDEOUT_1F/MAIN -> REGION_MAGMA_HIDEOUT_1F/ENTRANCE"),
        hm_rules["HM04 Strength"]
    )

    # Aqua Hideout
    if "Aqua Hideout Grunts" not in world.options.remove_roadblocks.value:
        set_rule(
            get_entrance("REGION_AQUA_HIDEOUT_1F/WATER -> REGION_AQUA_HIDEOUT_1F/MAIN"),
            lambda state: state.has("EVENT_AQUA_STEALS_SUBMARINE", world.player)
        )
        set_rule(
            get_entrance("REGION_AQUA_HIDEOUT_1F/MAIN -> REGION_AQUA_HIDEOUT_1F/WATER"),
            lambda state: hm_rules["HM03 Surf"](state) and state.has("EVENT_AQUA_STEALS_SUBMARINE", world.player)
        )

    # Route 124
    set_rule(
        get_entrance("REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/BIG_AREA"),
        hm_rules["HM08 Dive"]
    )
    set_rule(
        get_entrance("REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/SMALL_AREA_1"),
        hm_rules["HM08 Dive"]
    )
    set_rule(
        get_entrance("REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/SMALL_AREA_2"),
        hm_rules["HM08 Dive"]
    )
    set_rule(
        get_entrance("REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/SMALL_AREA_3"),
        hm_rules["HM08 Dive"]
    )
    set_rule(
        get_entrance("REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/TUNNEL_1"),
        hm_rules["HM08 Dive"]
    )
    set_rule(
        get_entrance("REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/TUNNEL_2"),
        hm_rules["HM08 Dive"]
    )
    set_rule(
        get_entrance("REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/TUNNEL_3"),
        hm_rules["HM08 Dive"]
    )
    set_rule(
        get_entrance("REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/TUNNEL_4"),
        hm_rules["HM08 Dive"]
    )
    set_rule(
        get_entrance("REGION_ROUTE124/NORTH_ENCLOSED_AREA_1 -> REGION_UNDERWATER_ROUTE124/TUNNEL_1"),
        hm_rules["HM08 Dive"]
    )
    set_rule(
        get_entrance("REGION_ROUTE124/NORTH_ENCLOSED_AREA_2 -> REGION_UNDERWATER_ROUTE124/TUNNEL_1"),
        hm_rules["HM08 Dive"]
    )
    set_rule(
        get_entrance("REGION_ROUTE124/NORTH_ENCLOSED_AREA_3 -> REGION_UNDERWATER_ROUTE124/TUNNEL_2"),
        hm_rules["HM08 Dive"]
    )
    set_rule(
        get_entrance("REGION_ROUTE124/SOUTH_ENCLOSED_AREA_1 -> REGION_UNDERWATER_ROUTE124/TUNNEL_3"),
        hm_rules["HM08 Dive"]
    )
    set_rule(
        get_entrance("REGION_ROUTE124/SOUTH_ENCLOSED_AREA_2 -> REGION_UNDERWATER_ROUTE124/TUNNEL_3"),
        hm_rules["HM08 Dive"]
    )
    set_rule(
        get_entrance("REGION_ROUTE124/SOUTH_ENCLOSED_AREA_3 -> REGION_UNDERWATER_ROUTE124/TUNNEL_4"),
        hm_rules["HM08 Dive"]
    )

    # Mossdeep City
    set_rule(
        get_entrance("REGION_MOSSDEEP_CITY/MAIN -> REGION_MOSSDEEP_CITY/WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_MOSSDEEP_CITY/MAIN -> REGION_ROUTE124/MAIN"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_MOSSDEEP_CITY/MAIN -> REGION_ROUTE125/SEA"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_MOSSDEEP_CITY/MAIN -> REGION_ROUTE127/MAIN"),
        hm_rules["HM03 Surf"]
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
        get_location("NPC_GIFT_RECEIVED_HM_DIVE"),
        lambda state: state.has("EVENT_DEFEAT_MAXIE_AT_SPACE_STATION", world.player)
    )

    # Route 125
    set_rule(
        get_entrance("REGION_UNDERWATER_ROUTE125/MARINE_CAVE_ENTRANCE_1 -> REGION_UNDERWATER_MARINE_CAVE/MAIN"),
        lambda state: hm_rules["HM08 Dive"](state)
            and state.has("EVENT_DEFEAT_CHAMPION", world.player)
            and state.has("MARINE_CAVE_ROUTE_125_1", world.player)
            and state.has("EVENT_DEFEAT_SHELLY", world.player)
    )
    set_rule(
        get_entrance("REGION_UNDERWATER_ROUTE125/MARINE_CAVE_ENTRANCE_2 -> REGION_UNDERWATER_MARINE_CAVE/MAIN"),
        lambda state: hm_rules["HM08 Dive"](state)
            and state.has("EVENT_DEFEAT_CHAMPION", world.player)
            and state.has("MARINE_CAVE_ROUTE_125_2", world.player)
            and state.has("EVENT_DEFEAT_SHELLY", world.player)
    )

    # Shoal Cave
    set_rule(
        get_entrance("REGION_SHOAL_CAVE_ENTRANCE_ROOM/SOUTH -> REGION_SHOAL_CAVE_ENTRANCE_ROOM/HIGH_TIDE_WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_SHOAL_CAVE_ENTRANCE_ROOM/NORTH_WEST_CORNER -> REGION_SHOAL_CAVE_ENTRANCE_ROOM/HIGH_TIDE_WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_SHOAL_CAVE_ENTRANCE_ROOM/NORTH_EAST_CORNER -> REGION_SHOAL_CAVE_ENTRANCE_ROOM/HIGH_TIDE_WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_SHOAL_CAVE_INNER_ROOM/HIGH_TIDE_EAST_MIDDLE_GROUND -> REGION_SHOAL_CAVE_INNER_ROOM/SOUTH_EAST_WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_SHOAL_CAVE_INNER_ROOM/HIGH_TIDE_EAST_MIDDLE_GROUND -> REGION_SHOAL_CAVE_INNER_ROOM/EAST_WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_SHOAL_CAVE_INNER_ROOM/HIGH_TIDE_EAST_MIDDLE_GROUND -> REGION_SHOAL_CAVE_INNER_ROOM/NORTH_WEST_WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_SHOAL_CAVE_INNER_ROOM/SOUTH_WEST_CORNER -> REGION_SHOAL_CAVE_INNER_ROOM/NORTH_WEST_WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_SHOAL_CAVE_INNER_ROOM/RARE_CANDY_PLATFORM -> REGION_SHOAL_CAVE_INNER_ROOM/SOUTH_EAST_WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_SHOAL_CAVE_LOW_TIDE_LOWER_ROOM/NORTH_WEST -> REGION_SHOAL_CAVE_LOW_TIDE_LOWER_ROOM/EAST"),
        hm_rules["HM04 Strength"]
    )
    set_rule(
        get_entrance("REGION_SHOAL_CAVE_LOW_TIDE_LOWER_ROOM/EAST -> REGION_SHOAL_CAVE_LOW_TIDE_LOWER_ROOM/NORTH_WEST"),
        hm_rules["HM04 Strength"]
    )

    # Route 126
    set_rule(
        get_entrance("REGION_ROUTE126/MAIN -> REGION_UNDERWATER_ROUTE126/MAIN"),
        hm_rules["HM08 Dive"]
    )
    set_rule(
        get_entrance("REGION_ROUTE126/MAIN -> REGION_UNDERWATER_ROUTE126/SMALL_AREA_2"),
        hm_rules["HM08 Dive"]
    )
    set_rule(
        get_entrance("REGION_ROUTE126/NEAR_ROUTE_124 -> REGION_UNDERWATER_ROUTE126/TUNNEL"),
        hm_rules["HM08 Dive"]
    )
    set_rule(
        get_entrance("REGION_ROUTE126/NORTH_WEST_CORNER -> REGION_UNDERWATER_ROUTE126/TUNNEL"),
        hm_rules["HM08 Dive"]
    )
    set_rule(
        get_entrance("REGION_ROUTE126/WEST -> REGION_UNDERWATER_ROUTE126/MAIN"),
        hm_rules["HM08 Dive"]
    )
    set_rule(
        get_entrance("REGION_ROUTE126/WEST -> REGION_UNDERWATER_ROUTE126/SMALL_AREA_1"),
        hm_rules["HM08 Dive"]
    )

    # Sootopolis City
    set_rule(
        get_entrance("REGION_SOOTOPOLIS_CITY/WATER -> REGION_UNDERWATER_SOOTOPOLIS_CITY/MAIN"),
        hm_rules["HM08 Dive"]
    )
    set_rule(
        get_entrance("REGION_SOOTOPOLIS_CITY/EAST -> REGION_SOOTOPOLIS_CITY/WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_SOOTOPOLIS_CITY/WEST -> REGION_SOOTOPOLIS_CITY/WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_SOOTOPOLIS_CITY/ISLAND -> REGION_SOOTOPOLIS_CITY/WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("MAP_SOOTOPOLIS_CITY:3/MAP_CAVE_OF_ORIGIN_ENTRANCE:0"),
        lambda state: state.has("EVENT_RELEASE_KYOGRE", world.player)
    )
    set_rule(
        get_entrance("MAP_SOOTOPOLIS_CITY:2/MAP_SOOTOPOLIS_CITY_GYM_1F:0"),
        lambda state: state.has("EVENT_RAYQUAZA_STOPS_FIGHT", world.player)
    )
    set_rule(
        get_location("NPC_GIFT_RECEIVED_HM_WATERFALL"),
        lambda state: state.has("EVENT_RAYQUAZA_STOPS_FIGHT", world.player)
    )
    set_rule(
        get_location("EVENT_RAYQUAZA_STOPS_FIGHT"),
        lambda state: state.has("EVENT_RELEASE_KYOGRE", world.player)
    )

    # Route 127
    set_rule(
        get_entrance("REGION_ROUTE127/MAIN -> REGION_UNDERWATER_ROUTE127/MAIN"),
        hm_rules["HM08 Dive"]
    )
    set_rule(
        get_entrance("REGION_ROUTE127/MAIN -> REGION_UNDERWATER_ROUTE127/TUNNEL"),
        hm_rules["HM08 Dive"]
    )
    set_rule(
        get_entrance("REGION_ROUTE127/MAIN -> REGION_UNDERWATER_ROUTE127/AREA_1"),
        hm_rules["HM08 Dive"]
    )
    set_rule(
        get_entrance("REGION_ROUTE127/MAIN -> REGION_UNDERWATER_ROUTE127/AREA_2"),
        hm_rules["HM08 Dive"]
    )
    set_rule(
        get_entrance("REGION_ROUTE127/MAIN -> REGION_UNDERWATER_ROUTE127/AREA_3"),
        hm_rules["HM08 Dive"]
    )
    set_rule(
        get_entrance("REGION_ROUTE127/ENCLOSED_AREA -> REGION_UNDERWATER_ROUTE127/TUNNEL"),
        hm_rules["HM08 Dive"]
    )
    set_rule(
        get_entrance("REGION_UNDERWATER_ROUTE127/MARINE_CAVE_ENTRANCE_1 -> REGION_UNDERWATER_MARINE_CAVE/MAIN"),
        lambda state: hm_rules["HM08 Dive"](state)
            and state.has("EVENT_DEFEAT_CHAMPION", world.player)
            and state.has("MARINE_CAVE_ROUTE_127_1", world.player)
            and state.has("EVENT_DEFEAT_SHELLY", world.player)
    )
    set_rule(
        get_entrance("REGION_UNDERWATER_ROUTE127/MARINE_CAVE_ENTRANCE_2 -> REGION_UNDERWATER_MARINE_CAVE/MAIN"),
        lambda state: hm_rules["HM08 Dive"](state)
            and state.has("EVENT_DEFEAT_CHAMPION", world.player)
            and state.has("MARINE_CAVE_ROUTE_127_2", world.player)
            and state.has("EVENT_DEFEAT_SHELLY", world.player)
    )

    # Route 128
    set_rule(
        get_entrance("REGION_ROUTE128/MAIN -> REGION_UNDERWATER_ROUTE128/MAIN"),
        hm_rules["HM08 Dive"]
    )
    set_rule(
        get_entrance("REGION_ROUTE128/MAIN -> REGION_UNDERWATER_ROUTE128/AREA_1"),
        hm_rules["HM08 Dive"]
    )
    set_rule(
        get_entrance("REGION_ROUTE128/MAIN -> REGION_UNDERWATER_ROUTE128/AREA_2"),
        hm_rules["HM08 Dive"]
    )

    # Seafloor Cavern
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ENTRANCE/MAIN -> REGION_SEAFLOOR_CAVERN_ENTRANCE/WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ENTRANCE/WATER -> REGION_UNDERWATER_SEAFLOOR_CAVERN/MAIN"),
        hm_rules["HM08 Dive"]
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM1/SOUTH -> REGION_SEAFLOOR_CAVERN_ROOM1/NORTH"),
        lambda state: hm_rules["HM06 Rock Smash"](state) and hm_rules["HM04 Strength"](state)
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM1/NORTH -> REGION_SEAFLOOR_CAVERN_ROOM1/SOUTH"),
        hm_rules["HM04 Strength"]
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM2/SOUTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM2/NORTH_WEST"),
        hm_rules["HM04 Strength"]
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM2/NORTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM2/SOUTH_WEST"),
        hm_rules["HM04 Strength"]
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM2/SOUTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM2/SOUTH_EAST"),
        hm_rules["HM06 Rock Smash"]
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM2/SOUTH_EAST -> REGION_SEAFLOOR_CAVERN_ROOM2/SOUTH_WEST"),
        hm_rules["HM06 Rock Smash"]
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM2/NORTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM2/NORTH_EAST"),
        lambda state: hm_rules["HM06 Rock Smash"](state) and hm_rules["HM04 Strength"](state)
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM2/NORTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM2/SOUTH_EAST"),
        lambda state: hm_rules["HM06 Rock Smash"](state) and hm_rules["HM04 Strength"](state)
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM5/NORTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM5/EAST"),
        lambda state: hm_rules["HM06 Rock Smash"](state) and hm_rules["HM04 Strength"](state)
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM5/EAST -> REGION_SEAFLOOR_CAVERN_ROOM5/NORTH_WEST"),
        hm_rules["HM04 Strength"]
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM5/NORTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM5/SOUTH_WEST"),
        lambda state: hm_rules["HM06 Rock Smash"](state) and hm_rules["HM04 Strength"](state)
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM5/SOUTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM5/NORTH_WEST"),
        lambda state: hm_rules["HM06 Rock Smash"](state) and hm_rules["HM04 Strength"](state)
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM6/NORTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM6/WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM6/SOUTH -> REGION_SEAFLOOR_CAVERN_ROOM6/WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM7/SOUTH -> REGION_SEAFLOOR_CAVERN_ROOM7/WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM7/NORTH -> REGION_SEAFLOOR_CAVERN_ROOM7/WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM8/NORTH -> REGION_SEAFLOOR_CAVERN_ROOM8/SOUTH"),
        hm_rules["HM04 Strength"]
    )
    set_rule(
        get_entrance("REGION_SEAFLOOR_CAVERN_ROOM8/SOUTH -> REGION_SEAFLOOR_CAVERN_ROOM8/NORTH"),
        hm_rules["HM04 Strength"]
    )
    if "Seafloor Cavern Aqua Grunt" not in world.options.remove_roadblocks.value:
        set_rule(
            get_entrance("MAP_SEAFLOOR_CAVERN_ENTRANCE:1/MAP_SEAFLOOR_CAVERN_ROOM1:0"),
            lambda state: state.has("EVENT_STEVEN_GIVES_DIVE", world.player)
        )

    # Route 129
    set_rule(
        get_entrance("REGION_UNDERWATER_ROUTE129/MARINE_CAVE_ENTRANCE_1 -> REGION_UNDERWATER_MARINE_CAVE/MAIN"),
        lambda state: hm_rules["HM08 Dive"](state)
            and state.has("EVENT_DEFEAT_CHAMPION", world.player)
            and state.has("MARINE_CAVE_ROUTE_129_1", world.player)
            and state.has("EVENT_DEFEAT_SHELLY", world.player)
    )
    set_rule(
        get_entrance("REGION_UNDERWATER_ROUTE129/MARINE_CAVE_ENTRANCE_2 -> REGION_UNDERWATER_MARINE_CAVE/MAIN"),
        lambda state: hm_rules["HM08 Dive"](state)
            and state.has("EVENT_DEFEAT_CHAMPION", world.player)
            and state.has("MARINE_CAVE_ROUTE_129_2", world.player)
            and state.has("EVENT_DEFEAT_SHELLY", world.player)
    )

    # Pacifidlog Town
    set_rule(
        get_entrance("REGION_PACIFIDLOG_TOWN/MAIN -> REGION_PACIFIDLOG_TOWN/WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_PACIFIDLOG_TOWN/MAIN -> REGION_ROUTE131/MAIN"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_PACIFIDLOG_TOWN/MAIN -> REGION_ROUTE132/EAST"),
        hm_rules["HM03 Surf"]
    )

    # Sky Pillar
    set_rule(
        get_entrance("MAP_SKY_PILLAR_OUTSIDE:1/MAP_SKY_PILLAR_1F:0"),
        lambda state: state.has("EVENT_RELEASE_KYOGRE", world.player)
    )
    add_rule(
        get_location("EVENT_ENCOUNTER_RAYQUAZA"),
        lambda state: state.has("EVENT_RAYQUAZA_STOPS_FIGHT", world.player)
    )
    set_rule(
        get_entrance("REGION_SKY_PILLAR_2F/RIGHT -> REGION_SKY_PILLAR_2F/LEFT"),
        has_mach_bike
    )
    set_rule(
        get_entrance("REGION_SKY_PILLAR_2F/LEFT -> REGION_SKY_PILLAR_2F/RIGHT"),
        has_mach_bike
    )
    set_rule(
        get_entrance("REGION_SKY_PILLAR_4F/MAIN -> REGION_SKY_PILLAR_4F/ABOVE_3F_TOP_CENTER"),
        has_mach_bike
    )

    # Route 134
    set_rule(
        get_entrance("REGION_ROUTE134/MAIN -> REGION_UNDERWATER_ROUTE134/MAIN"),
        hm_rules["HM08 Dive"]
    )
    set_rule(
        get_location("EVENT_UNDO_REGI_SEAL"),
        lambda state: state.has("CATCH_SPECIES_WAILORD", world.player) and state.has("CATCH_SPECIES_RELICANTH", world.player)
    )
    set_rule(
        get_entrance("REGION_SEALED_CHAMBER_OUTER_ROOM/MAIN -> REGION_SEALED_CHAMBER_OUTER_ROOM/CRUMBLED_WALL"),
        lambda state: state.has("EVENT_MOVE_TUTOR_DIG", world.player)
    )

    # Ever Grande City
    set_rule(
        get_entrance("REGION_EVER_GRANDE_CITY/SEA -> REGION_EVER_GRANDE_CITY/SOUTH"),
        hm_rules["HM07 Waterfall"]
    )
    set_rule(
        get_entrance("REGION_EVER_GRANDE_CITY/SOUTH -> REGION_EVER_GRANDE_CITY/SEA"),
        hm_rules["HM03 Surf"]
    )

    # Victory Road
    set_rule(
        get_entrance("REGION_VICTORY_ROAD_B1F/SOUTH_WEST_MAIN -> REGION_VICTORY_ROAD_B1F/SOUTH_WEST_LADDER_UP"),
        lambda state: hm_rules["HM06 Rock Smash"](state) and hm_rules["HM04 Strength"](state)
    )
    set_rule(
        get_entrance("REGION_VICTORY_ROAD_B1F/SOUTH_WEST_LADDER_UP -> REGION_VICTORY_ROAD_B1F/SOUTH_WEST_MAIN"),
        lambda state: hm_rules["HM06 Rock Smash"](state) and hm_rules["HM04 Strength"](state)
    )
    set_rule(
        get_entrance("REGION_VICTORY_ROAD_B1F/MAIN_UPPER -> REGION_VICTORY_ROAD_B1F/MAIN_LOWER_EAST"),
        lambda state: hm_rules["HM06 Rock Smash"](state) and hm_rules["HM04 Strength"](state)
    )
    set_rule(
        get_entrance("REGION_VICTORY_ROAD_B1F/MAIN_LOWER_EAST -> REGION_VICTORY_ROAD_B1F/MAIN_LOWER_WEST"),
        hm_rules["HM06 Rock Smash"]
    )
    set_rule(
        get_entrance("REGION_VICTORY_ROAD_B1F/MAIN_LOWER_WEST -> REGION_VICTORY_ROAD_B1F/MAIN_LOWER_EAST"),
        lambda state: hm_rules["HM06 Rock Smash"](state) and hm_rules["HM04 Strength"](state)
    )
    set_rule(
        get_entrance("REGION_VICTORY_ROAD_B1F/MAIN_LOWER_WEST -> REGION_VICTORY_ROAD_B1F/MAIN_UPPER"),
        lambda state: hm_rules["HM06 Rock Smash"](state) and hm_rules["HM04 Strength"](state)
    )
    set_rule(
        get_entrance("REGION_VICTORY_ROAD_B2F/LOWER_WEST -> REGION_VICTORY_ROAD_B2F/LOWER_WEST_WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_VICTORY_ROAD_B2F/LOWER_WEST_ISLAND -> REGION_VICTORY_ROAD_B2F/LOWER_WEST_WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_VICTORY_ROAD_B2F/LOWER_EAST -> REGION_VICTORY_ROAD_B2F/LOWER_EAST_WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_VICTORY_ROAD_B2F/LOWER_WEST_WATER -> REGION_VICTORY_ROAD_B2F/UPPER_WATER"),
        hm_rules["HM07 Waterfall"]
    )
    set_rule(
        get_entrance("REGION_VICTORY_ROAD_B2F/LOWER_EAST_WATER -> REGION_VICTORY_ROAD_B2F/UPPER_WATER"),
        hm_rules["HM07 Waterfall"]
    )
    set_rule(
        get_entrance("REGION_VICTORY_ROAD_B2F/UPPER -> REGION_VICTORY_ROAD_B2F/UPPER_WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_VICTORY_ROAD_B2F/UPPER -> REGION_VICTORY_ROAD_B2F/LOWER_EAST_WATER"),
        hm_rules["HM03 Surf"]
    )

    # Pokemon League
    if world.options.elite_four_requirement == EliteFourRequirement.option_badges:
        set_rule(
            get_entrance("REGION_EVER_GRANDE_CITY_POKEMON_LEAGUE_1F/MAIN -> REGION_EVER_GRANDE_CITY_POKEMON_LEAGUE_1F/BEHIND_BADGE_CHECKERS"),
            lambda state: state.has_group_unique("Badge", world.player, world.options.elite_four_count.value)
        )
    else:
        set_rule(
            get_entrance("REGION_EVER_GRANDE_CITY_POKEMON_LEAGUE_1F/MAIN -> REGION_EVER_GRANDE_CITY_POKEMON_LEAGUE_1F/BEHIND_BADGE_CHECKERS"),
            lambda state: defeated_n_gym_leaders(state, world.options.elite_four_count.value)
        )

    # Battle Frontier
    set_rule(
        get_entrance("REGION_BATTLE_FRONTIER_OUTSIDE_WEST/DOCK -> REGION_SS_TIDAL_CORRIDOR/MAIN"),
        lambda state: state.has("S.S. Ticket", world.player)
    )
    set_rule(
        get_entrance("REGION_BATTLE_FRONTIER_OUTSIDE_WEST/CAVE_ENTRANCE -> REGION_BATTLE_FRONTIER_OUTSIDE_WEST/WATER"),
        hm_rules["HM03 Surf"]
    )
    set_rule(
        get_entrance("REGION_BATTLE_FRONTIER_OUTSIDE_EAST/MAIN -> REGION_BATTLE_FRONTIER_OUTSIDE_EAST/ABOVE_WATERFALL"),
        lambda state: state.has("Wailmer Pail", world.player) and hm_rules["HM03 Surf"](state)
    )
    set_rule(
        get_entrance("REGION_BATTLE_FRONTIER_OUTSIDE_EAST/ABOVE_WATERFALL -> REGION_BATTLE_FRONTIER_OUTSIDE_EAST/MAIN"),
        lambda state: state.has("Wailmer Pail", world.player)
    )
    set_rule(
        get_entrance("REGION_BATTLE_FRONTIER_OUTSIDE_EAST/WATER -> REGION_BATTLE_FRONTIER_OUTSIDE_EAST/ABOVE_WATERFALL"),
        hm_rules["HM07 Waterfall"]
    )

    # Pokedex Rewards
    if world.options.dexsanity:
        for i in range(NUM_REAL_SPECIES):
            species = data.species[NATIONAL_ID_TO_SPECIES_ID[i + 1]]

            if species.species_id in world.blacklisted_wilds:
                continue

            set_rule(
                get_location(f"Pokedex - {species.label}"),
                lambda state, species_name=species.name: state.has(f"CATCH_{species_name}", world.player)
            )

        # Legendary hunt prevents Latios from being a wild spawn so the roamer
        # can be tracked, and also guarantees that the roamer is a Latios.
        if world.options.goal == Goal.option_legendary_hunt and \
                data.constants["SPECIES_LATIOS"] not in world.blacklisted_wilds:
            set_rule(
                get_location(f"Pokedex - Latios"),
                lambda state: state.has("EVENT_ENCOUNTER_LATIOS", world.player)
            )

    # Overworld Items
    if world.options.overworld_items:
        # Route 117
        set_rule(
            get_location("ITEM_ROUTE_117_REVIVE"),
            hm_rules["HM01 Cut"]
        )

        # Route 114
        set_rule(
            get_location("ITEM_ROUTE_114_PROTEIN"),
            hm_rules["HM06 Rock Smash"]
        )

        # Victory Road
        set_rule(
            get_location("ITEM_VICTORY_ROAD_B1F_FULL_RESTORE"),
            lambda state: hm_rules["HM06 Rock Smash"](state) and hm_rules["HM04 Strength"](state)
        )

    # Hidden Items
    if world.options.hidden_items:
        # Route 120
        set_rule(
            get_location("HIDDEN_ITEM_ROUTE_120_RARE_CANDY_1"),
            hm_rules["HM01 Cut"]
        )

        # Route 121
        set_rule(
            get_location("HIDDEN_ITEM_ROUTE_121_NUGGET"),
            hm_rules["HM01 Cut"]
        )

    # NPC Gifts
    if world.options.npc_gifts:
        # Littleroot Town
        set_rule(
            get_location("NPC_GIFT_RECEIVED_AMULET_COIN"),
            lambda state: state.has("EVENT_TALK_TO_MR_STONE", world.player) and state.has("Balance Badge", world.player)
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

        # Route 116
        set_rule(
            get_location("NPC_GIFT_RECEIVED_REPEAT_BALL"),
            lambda state: state.has("EVENT_RESCUE_CAPT_STERN", world.player)
        )

        # Dewford Town
        set_rule(
            get_location("NPC_GIFT_RECEIVED_TM_SLUDGE_BOMB"),
            lambda state: state.has("EVENT_DEFEAT_NORMAN", world.player)
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

        # Mauville City
        set_rule(
            get_location("NPC_GIFT_GOT_TM_THUNDERBOLT_FROM_WATTSON"),
            lambda state: state.has("EVENT_DEFEAT_NORMAN", world.player) and state.has("EVENT_TURN_OFF_GENERATOR", world.player)
        )

        # Fallarbor Town
        set_rule(
            get_location("NPC_GIFT_RECEIVED_TM_RETURN"),
            lambda state: state.has("EVENT_RECOVER_METEORITE", world.player) and state.has("Meteorite", world.player)
        )

        # Fortree City
        set_rule(
            get_location("NPC_GIFT_RECEIVED_MENTAL_HERB"),
            lambda state: state.has("EVENT_WINGULL_QUEST_2", world.player)
        )

    # Add Itemfinder requirement to hidden items
    if world.options.require_itemfinder:
        for location in world.multiworld.get_locations(world.player):
            assert isinstance(location, PokemonEmeraldLocation)
            if location.key is not None and data.locations[location.key].category == LocationCategory.HIDDEN_ITEM:
                add_rule(
                    location,
                    lambda state: state.has("Itemfinder", world.player)
                )

    # Add Flash requirements to dark caves
    # Granite Cave
    if world.options.require_flash in [DarkCavesRequireFlash.option_only_granite_cave, DarkCavesRequireFlash.option_both]:
        add_rule(
            get_entrance("MAP_GRANITE_CAVE_1F:2/MAP_GRANITE_CAVE_B1F:1"),
            hm_rules["HM05 Flash"]
        )
        add_rule(
            get_entrance("MAP_GRANITE_CAVE_B1F:3/MAP_GRANITE_CAVE_B2F:1"),
            hm_rules["HM05 Flash"]
        )

    # Victory Road
    if world.options.require_flash in [DarkCavesRequireFlash.option_only_victory_road, DarkCavesRequireFlash.option_both]:
        add_rule(
            get_entrance("MAP_VICTORY_ROAD_1F:2/MAP_VICTORY_ROAD_B1F:5"),
            hm_rules["HM05 Flash"]
        )
        add_rule(
            get_entrance("MAP_VICTORY_ROAD_1F:4/MAP_VICTORY_ROAD_B1F:4"),
            hm_rules["HM05 Flash"]
        )
        add_rule(
            get_entrance("MAP_VICTORY_ROAD_1F:3/MAP_VICTORY_ROAD_B1F:2"),
            hm_rules["HM05 Flash"]
        )
        add_rule(
            get_entrance("MAP_VICTORY_ROAD_B1F:3/MAP_VICTORY_ROAD_B2F:1"),
            hm_rules["HM05 Flash"]
        )
        add_rule(
            get_entrance("MAP_VICTORY_ROAD_B1F:1/MAP_VICTORY_ROAD_B2F:2"),
            hm_rules["HM05 Flash"]
        )
        add_rule(
            get_entrance("MAP_VICTORY_ROAD_B1F:6/MAP_VICTORY_ROAD_B2F:3"),
            hm_rules["HM05 Flash"]
        )
        add_rule(
            get_entrance("MAP_VICTORY_ROAD_B1F:0/MAP_VICTORY_ROAD_B2F:0"),
            hm_rules["HM05 Flash"]
        )
        add_rule(
            get_entrance("MAP_VICTORY_ROAD_B2F:3/MAP_VICTORY_ROAD_B1F:6"),
            hm_rules["HM05 Flash"]
        )
        add_rule(
            get_entrance("MAP_VICTORY_ROAD_B2F:2/MAP_VICTORY_ROAD_B1F:1"),
            hm_rules["HM05 Flash"]
        )
        add_rule(
            get_entrance("MAP_VICTORY_ROAD_B2F:0/MAP_VICTORY_ROAD_B1F:0"),
            hm_rules["HM05 Flash"]
        )
        add_rule(
            get_entrance("MAP_VICTORY_ROAD_B2F:1/MAP_VICTORY_ROAD_B1F:3"),
            hm_rules["HM05 Flash"]
        )
