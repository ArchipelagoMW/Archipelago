"""
Logic rule definitions for Pokemon Emerald
"""
from typing import TYPE_CHECKING, Literal

from rule_builder.rules import (Rule, CanReachEntrance, Has, HasAll, HasAny, HasFromListUnique, HasGroupUnique,
                                OptionFilter, True_)

from .data import LocationCategory, NATIONAL_ID_TO_SPECIES_ID, NUM_REAL_SPECIES, data
from .locations import PokemonEmeraldLocation
from .options import (DarkCavesRequireFlash, EliteFourRequirement, NormanRequirement, Goal, ModifyRoute118,
                      ExtraBoulders, ExtraBumpySlope, RemoveRoadblocks)

if TYPE_CHECKING:
    from . import PokemonEmeraldWorld


# Rules are organized by town/route/dungeon and ordered approximately
# by when you would first reach that place in a vanilla playthrough.
def set_rules(world: "PokemonEmeraldWorld") -> None:
    entrance_rules: dict[str, Rule] = {}
    location_rules: dict[str, Rule] = {}

    def add_rule(rule_dict: dict[str, Rule], name: str, rule: Rule, operation: Literal["AND"] | Literal["OR"] = "AND"):
        if name not in rule_dict:
            rule_dict[name] = True_()

        match operation:
            case "AND":
                rule_dict[name] &= rule
            case "OR":
                rule_dict[name] &= rule
            case _:
                raise ValueError(f'Invalid operation. Must be "AND" or "OR": {operation}')

    hm_rules: dict[str, Rule] = {}
    for hm, badges in world.hm_requirements.items():
        if isinstance(badges, list):
            hm_rules[hm] = Has(hm) & HasAll(*badges)
        else:
            hm_rules[hm] = Has(hm) & HasGroupUnique("Badge", badges)

    def create_defeated_n_gym_leaders_rule(n: int) -> Rule:
        return HasFromListUnique(
            "EVENT_DEFEAT_ROXANNE",
            "EVENT_DEFEAT_BRAWLY",
            "EVENT_DEFEAT_WATTSON",
            "EVENT_DEFEAT_FLANNERY",
            "EVENT_DEFEAT_NORMAN",
            "EVENT_DEFEAT_WINONA",
            "EVENT_DEFEAT_TATE_AND_LIZA",
            "EVENT_DEFEAT_JUAN",
            count=n
        )

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

    world.set_completion_rule(
        (OptionFilter(Goal, Goal.option_champion) & Has("EVENT_DEFEAT_CHAMPION")) |
        (OptionFilter(Goal, Goal.option_steven) & Has("EVENT_DEFEAT_STEVEN")) |
        (OptionFilter(Goal, Goal.option_norman) & Has("EVENT_DEFEAT_NORMAN")) |
        (OptionFilter(Goal, Goal.option_legendary_hunt) & HasFromListUnique(*huntable_legendary_events))
    )

    if world.options.legendary_hunt_catch:
        location_rules["EVENT_ENCOUNTER_GROUDON"] = Has("EVENT_DEFEAT_CHAMPION")
        location_rules["EVENT_ENCOUNTER_KYOGRE"] = Has("EVENT_DEFEAT_CHAMPION")
        location_rules["EVENT_ENCOUNTER_RAYQUAZA"] = Has("EVENT_DEFEAT_CHAMPION")
        location_rules["EVENT_ENCOUNTER_LATIAS"] = Has("EVENT_DEFEAT_CHAMPION")
        # Latios already only requires defeating the champion and access to Route 117
        # location_rules["EVENT_ENCOUNTER_LATIOS"] = Has("EVENT_DEFEAT_CHAMPION")
        location_rules["EVENT_ENCOUNTER_REGIROCK"] = Has("EVENT_DEFEAT_CHAMPION")
        location_rules["EVENT_ENCOUNTER_REGICE"] = Has("EVENT_DEFEAT_CHAMPION")
        location_rules["EVENT_ENCOUNTER_REGISTEEL"] = Has("EVENT_DEFEAT_CHAMPION")
        location_rules["EVENT_ENCOUNTER_MEW"] = Has("EVENT_DEFEAT_CHAMPION")
        location_rules["EVENT_ENCOUNTER_DEOXYS"] = Has("EVENT_DEFEAT_CHAMPION")
        location_rules["EVENT_ENCOUNTER_HO_OH"] = Has("EVENT_DEFEAT_CHAMPION")
        location_rules["EVENT_ENCOUNTER_LUGIA"] = Has("EVENT_DEFEAT_CHAMPION")

    # Sky
    entrance_rules["REGION_LITTLEROOT_TOWN/MAIN -> REGION_SKY"] = hm_rules["HM02 Fly"]
    entrance_rules["REGION_SKY -> REGION_LITTLEROOT_TOWN/MAIN"] = Has("EVENT_VISITED_LITTLEROOT_TOWN")
    entrance_rules["REGION_SKY -> REGION_OLDALE_TOWN/MAIN"] = Has("EVENT_VISITED_OLDALE_TOWN")
    entrance_rules["REGION_SKY -> REGION_PETALBURG_CITY/MAIN"] = Has("EVENT_VISITED_PETALBURG_CITY")
    entrance_rules["REGION_SKY -> REGION_RUSTBORO_CITY/MAIN"] = Has("EVENT_VISITED_RUSTBORO_CITY")
    entrance_rules["REGION_SKY -> REGION_DEWFORD_TOWN/MAIN"] = Has("EVENT_VISITED_DEWFORD_TOWN")
    entrance_rules["REGION_SKY -> REGION_SLATEPORT_CITY/MAIN"] = Has("EVENT_VISITED_SLATEPORT_CITY")
    entrance_rules["REGION_SKY -> REGION_MAUVILLE_CITY/MAIN"] = Has("EVENT_VISITED_MAUVILLE_CITY")
    entrance_rules["REGION_SKY -> REGION_VERDANTURF_TOWN/MAIN"] = Has("EVENT_VISITED_VERDANTURF_TOWN")
    entrance_rules["REGION_SKY -> REGION_FALLARBOR_TOWN/MAIN"] = Has("EVENT_VISITED_FALLARBOR_TOWN")
    entrance_rules["REGION_SKY -> REGION_LAVARIDGE_TOWN/MAIN"] = Has("EVENT_VISITED_LAVARIDGE_TOWN")
    entrance_rules["REGION_SKY -> REGION_FORTREE_CITY/MAIN"] = Has("EVENT_VISITED_FORTREE_CITY")
    entrance_rules["REGION_SKY -> REGION_LILYCOVE_CITY/MAIN"] = Has("EVENT_VISITED_LILYCOVE_CITY")
    entrance_rules["REGION_SKY -> REGION_MOSSDEEP_CITY/MAIN"] = Has("EVENT_VISITED_MOSSDEEP_CITY")
    entrance_rules["REGION_SKY -> REGION_SOOTOPOLIS_CITY/EAST"] = Has("EVENT_VISITED_SOOTOPOLIS_CITY")
    entrance_rules["REGION_SKY -> REGION_EVER_GRANDE_CITY/SOUTH"] = Has("EVENT_VISITED_EVER_GRANDE_CITY")

    # Littleroot Town
    location_rules["NPC_GIFT_RECEIVED_SS_TICKET"] = Has("EVENT_DEFEAT_CHAMPION")
    location_rules["NPC_GIFT_RECEIVED_AURORA_TICKET"] = Has("EVENT_DEFEAT_CHAMPION")
    location_rules["NPC_GIFT_RECEIVED_EON_TICKET"] = Has("EVENT_DEFEAT_CHAMPION")
    location_rules["NPC_GIFT_RECEIVED_MYSTIC_TICKET"] = Has("EVENT_DEFEAT_CHAMPION")
    location_rules["NPC_GIFT_RECEIVED_OLD_SEA_MAP"] = Has("EVENT_DEFEAT_CHAMPION")

    # Route 102
    entrance_rules["REGION_ROUTE102/MAIN -> REGION_ROUTE102/POND"] = hm_rules["HM03 Surf"]

    # Route 103
    entrance_rules["REGION_ROUTE103/EAST -> REGION_ROUTE103/WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_ROUTE103/WEST -> REGION_ROUTE103/WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_ROUTE103/EAST -> REGION_ROUTE103/EAST_TREE_MAZE"] = hm_rules["HM01 Cut"]

    # Petalburg City
    location_rules["NPC_GIFT_RECEIVED_HM_SURF"] = Has("EVENT_DEFEAT_NORMAN")

    entrance_rules["REGION_PETALBURG_CITY/MAIN -> REGION_PETALBURG_CITY/SOUTH_POND"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_PETALBURG_CITY/MAIN -> REGION_PETALBURG_CITY/NORTH_POND"] = hm_rules["HM03 Surf"]
    entrance_rules["MAP_PETALBURG_CITY_GYM:2/MAP_PETALBURG_CITY_GYM:3"] = (
        (
            OptionFilter(NormanRequirement, NormanRequirement.option_badges) &
            HasGroupUnique("Badge", world.options.norman_count.value)
        ) |
        (
            OptionFilter(NormanRequirement, NormanRequirement.option_gyms) &
            create_defeated_n_gym_leaders_rule(world.options.norman_count.value)
        )
    )
    entrance_rules["MAP_PETALBURG_CITY_GYM:5/MAP_PETALBURG_CITY_GYM:6"] = (
        (
            OptionFilter(NormanRequirement, NormanRequirement.option_badges) &
            HasGroupUnique("Badge", world.options.norman_count.value)
        ) |
        (
            OptionFilter(NormanRequirement, NormanRequirement.option_gyms) &
            create_defeated_n_gym_leaders_rule(world.options.norman_count.value)
        )
    )

    # Route 104
    entrance_rules["REGION_ROUTE104/SOUTH -> REGION_ROUTE104/SOUTH_WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_ROUTE104/NORTH -> REGION_ROUTE104/NORTH_POND"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_ROUTE104/NORTH -> REGION_ROUTE104/TREE_ALCOVE_2"] = hm_rules["HM01 Cut"]
    entrance_rules["REGION_ROUTE104_MR_BRINEYS_HOUSE/MAIN -> REGION_DEWFORD_TOWN/MAIN"] = Has("EVENT_TALK_TO_MR_STONE")

    # Petalburg Woods
    entrance_rules["REGION_PETALBURG_WOODS/WEST_PATH -> REGION_PETALBURG_WOODS/EAST_PATH"] = hm_rules["HM01 Cut"]

    # Rustboro City
    location_rules["EVENT_RETURN_DEVON_GOODS"] = Has("EVENT_RECOVER_DEVON_GOODS")
    if world.options.trainersanity:
        location_rules["TRAINER_BRENDAN_RUSTBORO_MUDKIP_REWARD"] = Has("EVENT_RETURN_DEVON_GOODS")

    # Devon Corp
    entrance_rules["MAP_RUSTBORO_CITY_DEVON_CORP_1F:2/MAP_RUSTBORO_CITY_DEVON_CORP_2F:0"] = Has("EVENT_RETURN_DEVON_GOODS")

    # Route 116
    entrance_rules["REGION_ROUTE116/WEST -> REGION_ROUTE116/WEST_ABOVE_LEDGE"] = hm_rules["HM01 Cut"]
    entrance_rules["REGION_ROUTE116/EAST -> REGION_TERRA_CAVE_ENTRANCE/MAIN"] = (
        HasAll("EVENT_DEFEAT_CHAMPION", "TERRA_CAVE_ROUTE_116_1", "EVENT_DEFEAT_SHELLY")
    )
    entrance_rules["REGION_ROUTE116/WEST -> REGION_TERRA_CAVE_ENTRANCE/MAIN"] = (
        HasAll("EVENT_DEFEAT_CHAMPION", "TERRA_CAVE_ROUTE_116_2", "EVENT_DEFEAT_SHELLY")
    )

    # Rusturf Tunnel
    location_rules["NPC_GIFT_RECEIVED_HM_STRENGTH"] = hm_rules["HM06 Rock Smash"]
    location_rules["EVENT_RECOVER_DEVON_GOODS"] = Has("EVENT_DEFEAT_ROXANNE")

    entrance_rules["REGION_RUSTURF_TUNNEL/WEST -> REGION_RUSTURF_TUNNEL/EAST"] = hm_rules["HM06 Rock Smash"]
    entrance_rules["REGION_RUSTURF_TUNNEL/EAST -> REGION_RUSTURF_TUNNEL/WEST"] = hm_rules["HM06 Rock Smash"]

    # Route 115
    entrance_rules["REGION_ROUTE115/SOUTH_BELOW_LEDGE -> REGION_ROUTE115/SEA"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_ROUTE115/SOUTH_BEACH_NEAR_CAVE -> REGION_ROUTE115/SEA"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_ROUTE115/SOUTH_ABOVE_LEDGE -> REGION_ROUTE115/SOUTH_BEHIND_ROCK"] = hm_rules["HM06 Rock Smash"]
    entrance_rules["REGION_ROUTE115/NORTH_BELOW_SLOPE -> REGION_ROUTE115/SEA"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_ROUTE115/NORTH_BELOW_SLOPE -> REGION_ROUTE115/NORTH_ABOVE_SLOPE"] = Has("Mach Bike")
    entrance_rules["REGION_ROUTE115/NORTH_BELOW_SLOPE -> REGION_TERRA_CAVE_ENTRANCE/MAIN"] = (
        HasAll("EVENT_DEFEAT_CHAMPION", "TERRA_CAVE_ROUTE_115_1", "EVENT_DEFEAT_SHELLY")
    )
    entrance_rules["REGION_ROUTE115/NORTH_ABOVE_SLOPE -> REGION_TERRA_CAVE_ENTRANCE/MAIN"] = (
        HasAll("EVENT_DEFEAT_CHAMPION", "TERRA_CAVE_ROUTE_115_2", "EVENT_DEFEAT_SHELLY")
    )
    entrance_rules["REGION_ROUTE115/SOUTH_BEACH_NEAR_CAVE -> REGION_ROUTE115/SOUTH_ABOVE_LEDGE"] = (
        (OptionFilter(ExtraBoulders, ExtraBoulders.option_true) & hm_rules["HM04 Strength"]) |
        (OptionFilter(ExtraBoulders, ExtraBoulders.option_false))
    )
    entrance_rules["REGION_ROUTE115/SOUTH_ABOVE_LEDGE -> REGION_ROUTE115/SOUTH_BEACH_NEAR_CAVE"] = (
        (OptionFilter(ExtraBoulders, ExtraBoulders.option_true) & hm_rules["HM04 Strength"]) |
        (OptionFilter(ExtraBoulders, ExtraBoulders.option_false))
    )
    entrance_rules["REGION_ROUTE115/SOUTH_BELOW_LEDGE -> REGION_ROUTE115/SOUTH_ABOVE_LEDGE"] = (
        OptionFilter(ExtraBumpySlope, ExtraBumpySlope.option_true) & Has("Acro Bike")
    )

    # Route 105
    entrance_rules["REGION_UNDERWATER_ROUTE105/MARINE_CAVE_ENTRANCE_1 -> REGION_UNDERWATER_MARINE_CAVE/MAIN"] = (
        hm_rules["HM08 Dive"] & HasAll("EVENT_DEFEAT_CHAMPION", "MARINE_CAVE_ROUTE_105_1", "EVENT_DEFEAT_SHELLY")
    )
    entrance_rules["REGION_UNDERWATER_ROUTE105/MARINE_CAVE_ENTRANCE_2 -> REGION_UNDERWATER_MARINE_CAVE/MAIN"] = (
        hm_rules["HM08 Dive"] & HasAll("EVENT_DEFEAT_CHAMPION", "MARINE_CAVE_ROUTE_105_2", "EVENT_DEFEAT_SHELLY")
    )
    entrance_rules["MAP_ROUTE105:0/MAP_ISLAND_CAVE:0"] = Has("EVENT_UNDO_REGI_SEAL")

    # Route 106
    entrance_rules["REGION_ROUTE106/EAST -> REGION_ROUTE106/SEA"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_ROUTE106/WEST -> REGION_ROUTE106/SEA"] = hm_rules["HM03 Surf"]

    # Dewford Town
    entrance_rules["REGION_DEWFORD_TOWN/MAIN -> REGION_ROUTE109/BEACH"] = (
        CanReachEntrance("REGION_ROUTE104_MR_BRINEYS_HOUSE/MAIN -> REGION_DEWFORD_TOWN/MAIN") &
        HasAll("EVENT_TALK_TO_MR_STONE", "EVENT_DELIVER_LETTER")
    )
    entrance_rules["REGION_DEWFORD_TOWN/MAIN -> REGION_ROUTE104_MR_BRINEYS_HOUSE/MAIN"] = (
        CanReachEntrance("REGION_ROUTE104_MR_BRINEYS_HOUSE/MAIN -> REGION_DEWFORD_TOWN/MAIN") &
        Has("EVENT_TALK_TO_MR_STONE")
    )
    entrance_rules["REGION_DEWFORD_TOWN/MAIN -> REGION_DEWFORD_TOWN/WATER"] = hm_rules["HM03 Surf"]

    # Granite Cave
    entrance_rules["REGION_GRANITE_CAVE_STEVENS_ROOM/MAIN -> REGION_GRANITE_CAVE_STEVENS_ROOM/LETTER_DELIVERED"] = Has("Letter")
    entrance_rules["REGION_GRANITE_CAVE_B1F/LOWER -> REGION_GRANITE_CAVE_B1F/UPPER"] = Has("Mach Bike")

    # Route 107
    entrance_rules["REGION_DEWFORD_TOWN/MAIN -> REGION_ROUTE107/MAIN"] = hm_rules["HM03 Surf"]

    # Route 109
    entrance_rules["REGION_ROUTE109/BEACH -> REGION_DEWFORD_TOWN/MAIN"] = (
        CanReachEntrance("REGION_ROUTE104_MR_BRINEYS_HOUSE/MAIN -> REGION_DEWFORD_TOWN/MAIN") &
        CanReachEntrance("REGION_DEWFORD_TOWN/MAIN -> REGION_ROUTE109/BEACH") &
        HasAll("EVENT_TALK_TO_MR_STONE", "EVENT_DELIVER_LETTER")
    )
    entrance_rules["REGION_ROUTE109/BEACH -> REGION_ROUTE109/SEA"] = hm_rules["HM03 Surf"]

    # Slateport City
    location_rules["EVENT_TALK_TO_DOCK"] = Has("Devon Goods")
    location_rules["EVENT_AQUA_STEALS_SUBMARINE"] = Has("EVENT_RELEASE_GROUDON")

    entrance_rules["REGION_SLATEPORT_CITY/MAIN -> REGION_SLATEPORT_CITY/WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["MAP_SLATEPORT_CITY:5,7/MAP_SLATEPORT_CITY_OCEANIC_MUSEUM_1F:0,1"] = Has("EVENT_TALK_TO_DOCK")
    entrance_rules["REGION_SLATEPORT_CITY_HARBOR/MAIN -> REGION_SS_TIDAL_CORRIDOR/MAIN"] = Has("S.S. Ticket")

    # Route 110
    entrance_rules["REGION_ROUTE110/MAIN -> REGION_ROUTE110/SOUTH_WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_ROUTE110/MAIN -> REGION_ROUTE110/NORTH_WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_ROUTE110_SEASIDE_CYCLING_ROAD_SOUTH_ENTRANCE/WEST -> REGION_ROUTE110_SEASIDE_CYCLING_ROAD_SOUTH_ENTRANCE/EAST"] = HasAny("Acro Bike", "Mach Bike")
    entrance_rules["REGION_ROUTE110_SEASIDE_CYCLING_ROAD_NORTH_ENTRANCE/WEST -> REGION_ROUTE110_SEASIDE_CYCLING_ROAD_NORTH_ENTRANCE/EAST"] = HasAny("Acro Bike", "Mach Bike")
    entrance_rules["REGION_ROUTE110/SOUTH -> REGION_ROUTE110/MAIN"] = (
        OptionFilter(RemoveRoadblocks, "Route 110 Aqua Grunts", "contains") | Has("EVENT_RESCUE_CAPT_STERN")
    )
    entrance_rules["REGION_ROUTE110/MAIN -> REGION_ROUTE110/SOUTH"] = (
        OptionFilter(RemoveRoadblocks, "Route 110 Aqua Grunts", "contains") | Has("EVENT_RESCUE_CAPT_STERN")
    )

    # Trick House
    entrance_rules["REGION_ROUTE110_TRICK_HOUSE_PUZZLE1/ENTRANCE -> REGION_ROUTE110_TRICK_HOUSE_PUZZLE1/REWARDS"] = hm_rules["HM01 Cut"]
    entrance_rules["REGION_ROUTE110_TRICK_HOUSE_ENTRANCE/MAIN -> REGION_ROUTE110_TRICK_HOUSE_PUZZLE2/ENTRANCE"] = HasAll("Dynamo Badge", "EVENT_COMPLETE_TRICK_HOUSE_1")
    entrance_rules["REGION_ROUTE110_TRICK_HOUSE_ENTRANCE/MAIN -> REGION_ROUTE110_TRICK_HOUSE_PUZZLE3/ENTRANCE"] = HasAll("Heat Badge", "EVENT_COMPLETE_TRICK_HOUSE_2")
    entrance_rules["REGION_ROUTE110_TRICK_HOUSE_PUZZLE3/ENTRANCE -> REGION_ROUTE110_TRICK_HOUSE_PUZZLE3/REWARDS"] = hm_rules["HM06 Rock Smash"]
    entrance_rules["REGION_ROUTE110_TRICK_HOUSE_ENTRANCE/MAIN -> REGION_ROUTE110_TRICK_HOUSE_PUZZLE4/ENTRANCE"] = HasAll("Balance Badge", "EVENT_COMPLETE_TRICK_HOUSE_3")
    entrance_rules["REGION_ROUTE110_TRICK_HOUSE_PUZZLE4/ENTRANCE -> REGION_ROUTE110_TRICK_HOUSE_PUZZLE4/REWARDS"] = hm_rules["HM04 Strength"]
    entrance_rules["REGION_ROUTE110_TRICK_HOUSE_ENTRANCE/MAIN -> REGION_ROUTE110_TRICK_HOUSE_PUZZLE5/ENTRANCE"] = HasAll("Feather Badge", "EVENT_COMPLETE_TRICK_HOUSE_4")
    entrance_rules["REGION_ROUTE110_TRICK_HOUSE_ENTRANCE/MAIN -> REGION_ROUTE110_TRICK_HOUSE_PUZZLE6/ENTRANCE"] = HasAll("Mind Badge", "EVENT_COMPLETE_TRICK_HOUSE_5")
    entrance_rules["REGION_ROUTE110_TRICK_HOUSE_ENTRANCE/MAIN -> REGION_ROUTE110_TRICK_HOUSE_PUZZLE7/ENTRANCE"] = HasAll("Rain Badge", "EVENT_COMPLETE_TRICK_HOUSE_6")
    entrance_rules["REGION_ROUTE110_TRICK_HOUSE_ENTRANCE/MAIN -> REGION_ROUTE110_TRICK_HOUSE_PUZZLE8/ENTRANCE"] = HasAll("EVENT_DEFEAT_CHAMPION", "EVENT_COMPLETE_TRICK_HOUSE_7")

    # Mauville City
    location_rules["NPC_GIFT_GOT_BASEMENT_KEY_FROM_WATTSON"] = Has("EVENT_DEFEAT_NORMAN")
    location_rules["NPC_GIFT_RECEIVED_COIN_CASE"] = Has("EVENT_BUY_HARBOR_MAIL")

    # Route 117
    location_rules["EVENT_ENCOUNTER_LATIOS"] = Has("EVENT_DEFEAT_CHAMPION")

    entrance_rules["REGION_ROUTE117/MAIN -> REGION_ROUTE117/PONDS"] = hm_rules["HM03 Surf"]

    # Route 111
    entrance_rules["REGION_ROUTE111/MIDDLE -> REGION_ROUTE111/DESERT"] = Has("Go Goggles")
    entrance_rules["REGION_ROUTE111/NORTH -> REGION_ROUTE111/DESERT"] = Has("Go Goggles")
    entrance_rules["REGION_ROUTE111/NORTH -> REGION_ROUTE111/ABOVE_SLOPE"] = Has("Mach Bike")
    entrance_rules["REGION_ROUTE111/MIDDLE -> REGION_ROUTE111/SOUTH"] = hm_rules["HM06 Rock Smash"]
    entrance_rules["REGION_ROUTE111/SOUTH -> REGION_ROUTE111/SOUTH_POND"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_ROUTE111/SOUTH -> REGION_ROUTE111/MIDDLE"] = hm_rules["HM06 Rock Smash"]
    entrance_rules["MAP_ROUTE111:4/MAP_TRAINER_HILL_ENTRANCE:0"] = Has("EVENT_DEFEAT_CHAMPION")
    entrance_rules["MAP_ROUTE111:1/MAP_DESERT_RUINS:0"] = Has("EVENT_UNDO_REGI_SEAL")
    entrance_rules["MAP_DESERT_RUINS:0/MAP_ROUTE111:1"] = hm_rules["HM06 Rock Smash"]

    # Route 112
    entrance_rules["REGION_ROUTE112/SOUTH_EAST -> REGION_ROUTE112/CABLE_CAR_STATION_ENTRANCE"] = (
        OptionFilter(RemoveRoadblocks, "Route 112 Magma Grunts", "contains") | Has("EVENT_MAGMA_STEALS_METEORITE")
    )
    entrance_rules["REGION_ROUTE112/CABLE_CAR_STATION_ENTRANCE -> REGION_ROUTE112/SOUTH_EAST"] = (
        OptionFilter(RemoveRoadblocks, "Route 112 Magma Grunts", "contains") | Has("EVENT_MAGMA_STEALS_METEORITE")
    )

    # Fiery Path
    entrance_rules["REGION_FIERY_PATH/MAIN -> REGION_FIERY_PATH/BEHIND_BOULDER"] = hm_rules["HM04 Strength"]

    # Route 114
    entrance_rules["REGION_ROUTE114/MAIN -> REGION_ROUTE114/WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_ROUTE114/WATER -> REGION_ROUTE114/ABOVE_WATERFALL"] = hm_rules["HM07 Waterfall"]
    entrance_rules["MAP_ROUTE114_FOSSIL_MANIACS_TUNNEL:2/MAP_DESERT_UNDERPASS:0"] = Has("EVENT_DEFEAT_CHAMPION")
    entrance_rules["REGION_ROUTE114/ABOVE_WATERFALL -> REGION_TERRA_CAVE_ENTRANCE/MAIN"] = (
        HasAll("EVENT_DEFEAT_CHAMPION", "TERRA_CAVE_ROUTE_114_1", "EVENT_DEFEAT_SHELLY")
    )
    entrance_rules["REGION_ROUTE114/MAIN -> REGION_TERRA_CAVE_ENTRANCE/MAIN"] = (
        HasAll("EVENT_DEFEAT_CHAMPION", "TERRA_CAVE_ROUTE_114_2", "EVENT_DEFEAT_SHELLY")
    )

    # Meteor Falls
    entrance_rules["REGION_METEOR_FALLS_1F_1R/MAIN -> REGION_METEOR_FALLS_1F_1R/WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_METEOR_FALLS_1F_1R/WATER -> REGION_METEOR_FALLS_1F_1R/WATER_ABOVE_WATERFALL"] = hm_rules["HM07 Waterfall"]
    entrance_rules["REGION_METEOR_FALLS_1F_1R/ABOVE_WATERFALL -> REGION_METEOR_FALLS_1F_1R/WATER_ABOVE_WATERFALL"] = hm_rules["HM03 Surf"]
    entrance_rules["MAP_METEOR_FALLS_1F_1R:5/MAP_METEOR_FALLS_STEVENS_CAVE:0"] = Has("EVENT_DEFEAT_CHAMPION")
    entrance_rules["REGION_METEOR_FALLS_1F_2R/LEFT_SPLIT -> REGION_METEOR_FALLS_1F_2R/LEFT_SPLIT_WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_METEOR_FALLS_1F_2R/RIGHT_SPLIT -> REGION_METEOR_FALLS_1F_2R/RIGHT_SPLIT_WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_METEOR_FALLS_B1F_1R/HIGHEST_LADDER -> REGION_METEOR_FALLS_B1F_1R/WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_METEOR_FALLS_B1F_1R/NORTH_SHORE -> REGION_METEOR_FALLS_B1F_1R/WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_METEOR_FALLS_B1F_1R/SOUTH_SHORE -> REGION_METEOR_FALLS_B1F_1R/WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_METEOR_FALLS_B1F_2R/ENTRANCE -> REGION_METEOR_FALLS_B1F_2R/WATER"] = hm_rules["HM03 Surf"]

    # Jagged Pass
    entrance_rules["REGION_JAGGED_PASS/BOTTOM -> REGION_JAGGED_PASS/MIDDLE"] = Has("Acro Bike")
    entrance_rules["REGION_JAGGED_PASS/MIDDLE -> REGION_JAGGED_PASS/TOP"] = Has("Acro Bike")
    entrance_rules["MAP_JAGGED_PASS:4/MAP_MAGMA_HIDEOUT_1F:0"] = Has("Magma Emblem")

    # Lavaridge Town
    location_rules["NPC_GIFT_RECEIVED_GO_GOGGLES"] = Has("EVENT_DEFEAT_FLANNERY")

    # Mirage Tower
    entrance_rules["REGION_MIRAGE_TOWER_2F/TOP -> REGION_MIRAGE_TOWER_2F/BOTTOM"] = Has("Mach Bike")
    entrance_rules["REGION_MIRAGE_TOWER_2F/BOTTOM -> REGION_MIRAGE_TOWER_2F/TOP"] = Has("Mach Bike")
    entrance_rules["REGION_MIRAGE_TOWER_3F/TOP -> REGION_MIRAGE_TOWER_3F/BOTTOM"] = hm_rules["HM06 Rock Smash"]
    entrance_rules["REGION_MIRAGE_TOWER_3F/BOTTOM -> REGION_MIRAGE_TOWER_3F/TOP"] = hm_rules["HM06 Rock Smash"]
    entrance_rules["REGION_MIRAGE_TOWER_4F/MAIN -> REGION_MIRAGE_TOWER_4F/FOSSIL_PLATFORM"] = hm_rules["HM06 Rock Smash"]

    # Abandoned Ship
    entrance_rules["REGION_ABANDONED_SHIP_ROOMS_B1F/CENTER -> REGION_ABANDONED_SHIP_UNDERWATER1/MAIN"] = hm_rules["HM08 Dive"]
    entrance_rules["REGION_ABANDONED_SHIP_HIDDEN_FLOOR_CORRIDORS/MAIN -> REGION_ABANDONED_SHIP_UNDERWATER2/MAIN"] = hm_rules["HM08 Dive"]
    entrance_rules["MAP_ABANDONED_SHIP_HIDDEN_FLOOR_CORRIDORS:0/MAP_ABANDONED_SHIP_HIDDEN_FLOOR_ROOMS:0"] = Has("Room 1 Key")
    entrance_rules["MAP_ABANDONED_SHIP_HIDDEN_FLOOR_CORRIDORS:1/MAP_ABANDONED_SHIP_HIDDEN_FLOOR_ROOMS:2"] = Has("Room 2 Key")
    entrance_rules["MAP_ABANDONED_SHIP_HIDDEN_FLOOR_CORRIDORS:3/MAP_ABANDONED_SHIP_HIDDEN_FLOOR_ROOMS:6"] = Has("Room 4 Key")
    entrance_rules["MAP_ABANDONED_SHIP_HIDDEN_FLOOR_CORRIDORS:5/MAP_ABANDONED_SHIP_HIDDEN_FLOOR_ROOMS:8"] = Has("Room 6 Key")
    entrance_rules["MAP_ABANDONED_SHIP_CORRIDORS_B1F:5/MAP_ABANDONED_SHIP_ROOM_B1F:0"] = Has("Storage Key")

    # New Mauville
    entrance_rules["MAP_NEW_MAUVILLE_ENTRANCE:1/MAP_NEW_MAUVILLE_INSIDE:0"] = Has("Basement Key")

    # Route 118
    entrance_rules["REGION_ROUTE118/WEST -> REGION_ROUTE118/EAST"] = (
        OptionFilter(ModifyRoute118, ModifyRoute118.option_true) & Has("Acro Bike")
    )
    entrance_rules["REGION_ROUTE118/EAST -> REGION_ROUTE118/WEST"] = (
        OptionFilter(ModifyRoute118, ModifyRoute118.option_true) & Has("Acro Bike")
    )
    entrance_rules["REGION_ROUTE118/WEST_WATER -> REGION_ROUTE118/EAST_WATER"] = (
        OptionFilter(ModifyRoute118, ModifyRoute118.option_false) & True_()
    )
    entrance_rules["REGION_ROUTE118/EAST_WATER -> REGION_ROUTE118/WEST_WATER"] = (
        OptionFilter(ModifyRoute118, ModifyRoute118.option_false) & True_()
    )
    entrance_rules["REGION_ROUTE118/WEST -> REGION_ROUTE118/WEST_WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_ROUTE118/EAST -> REGION_ROUTE118/EAST_WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_ROUTE118/EAST -> REGION_TERRA_CAVE_ENTRANCE/MAIN"] = (
        HasAll("EVENT_DEFEAT_CHAMPION", "TERRA_CAVE_ROUTE_118_1", "EVENT_DEFEAT_SHELLY")
    )
    entrance_rules["REGION_ROUTE118/WEST -> REGION_TERRA_CAVE_ENTRANCE/MAIN"] = (
        HasAll("EVENT_DEFEAT_CHAMPION", "TERRA_CAVE_ROUTE_118_2", "EVENT_DEFEAT_SHELLY")
    )

    # Route 119
    entrance_rules["REGION_ROUTE119/LOWER -> REGION_ROUTE119/LOWER_WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_ROUTE119/LOWER -> REGION_ROUTE119/LOWER_ACROSS_RAILS"] = Has("Acro Bike")
    entrance_rules["REGION_ROUTE119/LOWER_ACROSS_RAILS -> REGION_ROUTE119/LOWER"] = Has("Acro Bike")
    entrance_rules["REGION_ROUTE119/UPPER -> REGION_ROUTE119/MIDDLE_RIVER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_ROUTE119/MIDDLE_RIVER -> REGION_ROUTE119/ABOVE_WATERFALL"] = hm_rules["HM07 Waterfall"]
    entrance_rules["REGION_ROUTE119/ABOVE_WATERFALL -> REGION_ROUTE119/MIDDLE_RIVER"] = hm_rules["HM07 Waterfall"]
    entrance_rules["REGION_ROUTE119/ABOVE_WATERFALL -> REGION_ROUTE119/ABOVE_WATERFALL_ACROSS_RAILS"] = Has("Acro Bike")
    entrance_rules["REGION_ROUTE119/MIDDLE -> REGION_ROUTE119/UPPER"] = (
        OptionFilter(RemoveRoadblocks, "Route 119 Aqua Grunts", "contains") | Has("EVENT_DEFEAT_SHELLY")
    )
    entrance_rules["REGION_ROUTE119/UPPER -> REGION_ROUTE119/MIDDLE"] = (
        OptionFilter(RemoveRoadblocks, "Route 119 Aqua Grunts", "contains") | Has("EVENT_DEFEAT_SHELLY")
    )

    # Fortree City
    entrance_rules["REGION_FORTREE_CITY/MAIN -> REGION_FORTREE_CITY/BEFORE_GYM"] = Has("Devon Scope")
    entrance_rules["REGION_FORTREE_CITY/BEFORE_GYM -> REGION_FORTREE_CITY/MAIN"] = Has("Devon Scope")

    # Route 120
    entrance_rules["REGION_ROUTE120/NORTH -> REGION_ROUTE120/NORTH_POND_SHORE"] = Has("Devon Scope")
    entrance_rules["REGION_ROUTE120/NORTH_POND_SHORE -> REGION_ROUTE120/NORTH"] = Has("Devon Scope")
    entrance_rules["REGION_ROUTE120/NORTH_POND_SHORE -> REGION_ROUTE120/NORTH_POND"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_ROUTE120/SOUTH -> REGION_ROUTE120/SOUTH_ALCOVE"] = hm_rules["HM01 Cut"]
    entrance_rules["REGION_ROUTE120/SOUTH -> REGION_ROUTE120/SOUTH_PONDS"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_ROUTE120/SOUTH_ALCOVE -> REGION_ROUTE120/SOUTH"] = hm_rules["HM01 Cut"]
    entrance_rules["MAP_ROUTE120:0/MAP_ANCIENT_TOMB:0"] = Has("EVENT_UNDO_REGI_SEAL")
    entrance_rules["MAP_ANCIENT_TOMB:1/MAP_ANCIENT_TOMB:2"] = hm_rules["HM05 Flash"]

    # Route 121
    entrance_rules["REGION_ROUTE121/EAST -> REGION_ROUTE121/WEST"] = hm_rules["HM01 Cut"]
    entrance_rules["REGION_ROUTE121/EAST -> REGION_ROUTE121/WATER"] = hm_rules["HM03 Surf"]

    # Safari Zone
    entrance_rules["MAP_ROUTE121_SAFARI_ZONE_ENTRANCE:0,1/MAP_SAFARI_ZONE_SOUTH:0"] = Has("Pokeblock Case")
    entrance_rules["REGION_SAFARI_ZONE_NORTHWEST/MAIN -> REGION_SAFARI_ZONE_NORTHWEST/POND"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_SAFARI_ZONE_SOUTH/MAIN -> REGION_SAFARI_ZONE_NORTH/MAIN"] = Has("Acro Bike")
    entrance_rules["REGION_SAFARI_ZONE_SOUTHWEST/MAIN -> REGION_SAFARI_ZONE_NORTHWEST/MAIN"] = Has("Mach Bike")
    entrance_rules["REGION_SAFARI_ZONE_SOUTHWEST/MAIN -> REGION_SAFARI_ZONE_SOUTHWEST/POND"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_SAFARI_ZONE_SOUTHEAST/MAIN -> REGION_SAFARI_ZONE_SOUTHEAST/WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_SAFARI_ZONE_SOUTH/MAIN -> REGION_SAFARI_ZONE_SOUTHEAST/MAIN"] = (
        OptionFilter(RemoveRoadblocks, "Safari Zone Construction Workers", "contains") | Has("EVENT_DEFEAT_CHAMPION")
    )

    # Route 122
    entrance_rules["REGION_ROUTE122/MT_PYRE_ENTRANCE -> REGION_ROUTE122/SEA"] = hm_rules["HM03 Surf"]

    # Route 123
    entrance_rules["REGION_ROUTE123/EAST -> REGION_ROUTE122/SEA"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_ROUTE123/EAST -> REGION_ROUTE123/POND"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_ROUTE123/EAST -> REGION_ROUTE123/EAST_BEHIND_TREE"] = hm_rules["HM01 Cut"]

    # Lilycove City
    entrance_rules["REGION_LILYCOVE_CITY/MAIN -> REGION_LILYCOVE_CITY/SEA"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_LILYCOVE_CITY_HARBOR/MAIN -> REGION_SS_TIDAL_CORRIDOR/MAIN"] = Has("S.S. Ticket")
    entrance_rules["REGION_LILYCOVE_CITY_HARBOR/MAIN -> REGION_SOUTHERN_ISLAND_EXTERIOR/MAIN"] = Has("Eon Ticket")
    entrance_rules["REGION_LILYCOVE_CITY_HARBOR/MAIN -> REGION_FARAWAY_ISLAND_ENTRANCE/MAIN"] = Has("Old Sea Map")
    entrance_rules["REGION_LILYCOVE_CITY_HARBOR/MAIN -> REGION_BIRTH_ISLAND_HARBOR/MAIN"] = Has("Aurora Ticket")
    entrance_rules["REGION_LILYCOVE_CITY_HARBOR/MAIN -> REGION_NAVEL_ROCK_HARBOR/MAIN"] = Has("Mystic Ticket")
    entrance_rules["REGION_LILYCOVE_CITY/SEA -> REGION_ROUTE124/MAIN"] = (
        OptionFilter(RemoveRoadblocks, "Lilycove City Wailmer", "contains") | Has("EVENT_CLEAR_AQUA_HIDEOUT")
    )
    entrance_rules["REGION_ROUTE124/MAIN -> REGION_LILYCOVE_CITY/SEA"] = (
        OptionFilter(RemoveRoadblocks, "Lilycove City Wailmer", "contains") | Has("EVENT_CLEAR_AQUA_HIDEOUT")
    )

    # Magma Hideout
    entrance_rules["REGION_MAGMA_HIDEOUT_1F/ENTRANCE -> REGION_MAGMA_HIDEOUT_1F/MAIN"] = hm_rules["HM04 Strength"]
    entrance_rules["REGION_MAGMA_HIDEOUT_1F/MAIN -> REGION_MAGMA_HIDEOUT_1F/ENTRANCE"] = hm_rules["HM04 Strength"]

    # Aqua Hideout
    entrance_rules["REGION_AQUA_HIDEOUT_1F/WATER -> REGION_AQUA_HIDEOUT_1F/MAIN"] = (
        OptionFilter(RemoveRoadblocks, "Aqua Hideout Grunts", "contains") | Has("EVENT_AQUA_STEALS_SUBMARINE")
    )
    entrance_rules["REGION_AQUA_HIDEOUT_1F/MAIN -> REGION_AQUA_HIDEOUT_1F/WATER"] = (
        OptionFilter(RemoveRoadblocks, "Aqua Hideout Grunts", "contains") |
        (hm_rules["HM03 Surf"] & Has("EVENT_AQUA_STEALS_SUBMARINE"))
    )

    # Route 124
    entrance_rules["REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/BIG_AREA"] = hm_rules["HM08 Dive"]
    entrance_rules["REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/SMALL_AREA_1"] = hm_rules["HM08 Dive"]
    entrance_rules["REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/SMALL_AREA_2"] = hm_rules["HM08 Dive"]
    entrance_rules["REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/SMALL_AREA_3"] = hm_rules["HM08 Dive"]
    entrance_rules["REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/TUNNEL_1"] = hm_rules["HM08 Dive"]
    entrance_rules["REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/TUNNEL_2"] = hm_rules["HM08 Dive"]
    entrance_rules["REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/TUNNEL_3"] = hm_rules["HM08 Dive"]
    entrance_rules["REGION_ROUTE124/MAIN -> REGION_UNDERWATER_ROUTE124/TUNNEL_4"] = hm_rules["HM08 Dive"]
    entrance_rules["REGION_ROUTE124/NORTH_ENCLOSED_AREA_1 -> REGION_UNDERWATER_ROUTE124/TUNNEL_1"] = hm_rules["HM08 Dive"]
    entrance_rules["REGION_ROUTE124/NORTH_ENCLOSED_AREA_2 -> REGION_UNDERWATER_ROUTE124/TUNNEL_1"] = hm_rules["HM08 Dive"]
    entrance_rules["REGION_ROUTE124/NORTH_ENCLOSED_AREA_3 -> REGION_UNDERWATER_ROUTE124/TUNNEL_2"] = hm_rules["HM08 Dive"]
    entrance_rules["REGION_ROUTE124/SOUTH_ENCLOSED_AREA_1 -> REGION_UNDERWATER_ROUTE124/TUNNEL_3"] = hm_rules["HM08 Dive"]
    entrance_rules["REGION_ROUTE124/SOUTH_ENCLOSED_AREA_2 -> REGION_UNDERWATER_ROUTE124/TUNNEL_3"] = hm_rules["HM08 Dive"]
    entrance_rules["REGION_ROUTE124/SOUTH_ENCLOSED_AREA_3 -> REGION_UNDERWATER_ROUTE124/TUNNEL_4"] = hm_rules["HM08 Dive"]

    # Mossdeep City
    location_rules["EVENT_DEFEAT_MAXIE_AT_SPACE_STATION"] = Has("EVENT_DEFEAT_TATE_AND_LIZA")
    location_rules["EVENT_STEVEN_GIVES_DIVE"] = Has("EVENT_DEFEAT_MAXIE_AT_SPACE_STATION")
    location_rules["NPC_GIFT_RECEIVED_HM_DIVE"] = Has("EVENT_DEFEAT_MAXIE_AT_SPACE_STATION")

    entrance_rules["REGION_MOSSDEEP_CITY/MAIN -> REGION_MOSSDEEP_CITY/WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_MOSSDEEP_CITY/MAIN -> REGION_ROUTE124/MAIN"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_MOSSDEEP_CITY/MAIN -> REGION_ROUTE125/SEA"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_MOSSDEEP_CITY/MAIN -> REGION_ROUTE127/MAIN"] = hm_rules["HM03 Surf"]

    # Route 125
    entrance_rules["REGION_UNDERWATER_ROUTE125/MARINE_CAVE_ENTRANCE_1 -> REGION_UNDERWATER_MARINE_CAVE/MAIN"] = (
        hm_rules["HM08 Dive"] & HasAll("EVENT_DEFEAT_CHAMPION", "MARINE_CAVE_ROUTE_125_1", "EVENT_DEFEAT_SHELLY")
    )
    entrance_rules["REGION_UNDERWATER_ROUTE125/MARINE_CAVE_ENTRANCE_2 -> REGION_UNDERWATER_MARINE_CAVE/MAIN"] = (
        hm_rules["HM08 Dive"] & HasAll("EVENT_DEFEAT_CHAMPION", "MARINE_CAVE_ROUTE_125_2", "EVENT_DEFEAT_SHELLY")
    )

    # Shoal Cave
    entrance_rules["REGION_SHOAL_CAVE_ENTRANCE_ROOM/SOUTH -> REGION_SHOAL_CAVE_ENTRANCE_ROOM/HIGH_TIDE_WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_SHOAL_CAVE_ENTRANCE_ROOM/NORTH_WEST_CORNER -> REGION_SHOAL_CAVE_ENTRANCE_ROOM/HIGH_TIDE_WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_SHOAL_CAVE_ENTRANCE_ROOM/NORTH_EAST_CORNER -> REGION_SHOAL_CAVE_ENTRANCE_ROOM/HIGH_TIDE_WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_SHOAL_CAVE_INNER_ROOM/HIGH_TIDE_EAST_MIDDLE_GROUND -> REGION_SHOAL_CAVE_INNER_ROOM/SOUTH_EAST_WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_SHOAL_CAVE_INNER_ROOM/HIGH_TIDE_EAST_MIDDLE_GROUND -> REGION_SHOAL_CAVE_INNER_ROOM/EAST_WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_SHOAL_CAVE_INNER_ROOM/HIGH_TIDE_EAST_MIDDLE_GROUND -> REGION_SHOAL_CAVE_INNER_ROOM/NORTH_WEST_WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_SHOAL_CAVE_INNER_ROOM/SOUTH_WEST_CORNER -> REGION_SHOAL_CAVE_INNER_ROOM/NORTH_WEST_WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_SHOAL_CAVE_INNER_ROOM/RARE_CANDY_PLATFORM -> REGION_SHOAL_CAVE_INNER_ROOM/SOUTH_EAST_WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_SHOAL_CAVE_LOW_TIDE_LOWER_ROOM/NORTH_WEST -> REGION_SHOAL_CAVE_LOW_TIDE_LOWER_ROOM/EAST"] = hm_rules["HM04 Strength"]
    entrance_rules["REGION_SHOAL_CAVE_LOW_TIDE_LOWER_ROOM/EAST -> REGION_SHOAL_CAVE_LOW_TIDE_LOWER_ROOM/NORTH_WEST"] = hm_rules["HM04 Strength"]

    # Route 126
    entrance_rules["REGION_ROUTE126/MAIN -> REGION_UNDERWATER_ROUTE126/MAIN"] = hm_rules["HM08 Dive"]
    entrance_rules["REGION_ROUTE126/MAIN -> REGION_UNDERWATER_ROUTE126/SMALL_AREA_2"] = hm_rules["HM08 Dive"]
    entrance_rules["REGION_ROUTE126/NEAR_ROUTE_124 -> REGION_UNDERWATER_ROUTE126/TUNNEL"] = hm_rules["HM08 Dive"]
    entrance_rules["REGION_ROUTE126/NORTH_WEST_CORNER -> REGION_UNDERWATER_ROUTE126/TUNNEL"] = hm_rules["HM08 Dive"]
    entrance_rules["REGION_ROUTE126/WEST -> REGION_UNDERWATER_ROUTE126/MAIN"] = hm_rules["HM08 Dive"]
    entrance_rules["REGION_ROUTE126/WEST -> REGION_UNDERWATER_ROUTE126/SMALL_AREA_1"] = hm_rules["HM08 Dive"]

    # Sootopolis City
    location_rules["NPC_GIFT_RECEIVED_HM_WATERFALL"] = Has("EVENT_RAYQUAZA_STOPS_FIGHT")
    location_rules["EVENT_RAYQUAZA_STOPS_FIGHT"] = Has("EVENT_RELEASE_KYOGRE")

    entrance_rules["REGION_SOOTOPOLIS_CITY/WATER -> REGION_UNDERWATER_SOOTOPOLIS_CITY/MAIN"] = hm_rules["HM08 Dive"]
    entrance_rules["REGION_SOOTOPOLIS_CITY/EAST -> REGION_SOOTOPOLIS_CITY/WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_SOOTOPOLIS_CITY/WEST -> REGION_SOOTOPOLIS_CITY/WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_SOOTOPOLIS_CITY/ISLAND -> REGION_SOOTOPOLIS_CITY/WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["MAP_SOOTOPOLIS_CITY:3/MAP_CAVE_OF_ORIGIN_ENTRANCE:0"] = Has("EVENT_RELEASE_KYOGRE")
    entrance_rules["MAP_SOOTOPOLIS_CITY:2/MAP_SOOTOPOLIS_CITY_GYM_1F:0"] = Has("EVENT_RAYQUAZA_STOPS_FIGHT")

    # Route 127
    entrance_rules["REGION_ROUTE127/MAIN -> REGION_UNDERWATER_ROUTE127/MAIN"] = hm_rules["HM08 Dive"]
    entrance_rules["REGION_ROUTE127/MAIN -> REGION_UNDERWATER_ROUTE127/TUNNEL"] = hm_rules["HM08 Dive"]
    entrance_rules["REGION_ROUTE127/MAIN -> REGION_UNDERWATER_ROUTE127/AREA_1"] = hm_rules["HM08 Dive"]
    entrance_rules["REGION_ROUTE127/MAIN -> REGION_UNDERWATER_ROUTE127/AREA_2"] = hm_rules["HM08 Dive"]
    entrance_rules["REGION_ROUTE127/MAIN -> REGION_UNDERWATER_ROUTE127/AREA_3"] = hm_rules["HM08 Dive"]
    entrance_rules["REGION_ROUTE127/ENCLOSED_AREA -> REGION_UNDERWATER_ROUTE127/TUNNEL"] = hm_rules["HM08 Dive"]
    entrance_rules["REGION_UNDERWATER_ROUTE127/MARINE_CAVE_ENTRANCE_1 -> REGION_UNDERWATER_MARINE_CAVE/MAIN"] = (
        hm_rules["HM08 Dive"] & HasAll("EVENT_DEFEAT_CHAMPION", "MARINE_CAVE_ROUTE_127_1", "EVENT_DEFEAT_SHELLY")
    )
    entrance_rules["REGION_UNDERWATER_ROUTE127/MARINE_CAVE_ENTRANCE_2 -> REGION_UNDERWATER_MARINE_CAVE/MAIN"] = (
        hm_rules["HM08 Dive"] & HasAll("EVENT_DEFEAT_CHAMPION", "MARINE_CAVE_ROUTE_127_2", "EVENT_DEFEAT_SHELLY")
    )

    # Route 128
    entrance_rules["REGION_ROUTE128/MAIN -> REGION_UNDERWATER_ROUTE128/MAIN"] = hm_rules["HM08 Dive"]
    entrance_rules["REGION_ROUTE128/MAIN -> REGION_UNDERWATER_ROUTE128/AREA_1"] = hm_rules["HM08 Dive"]
    entrance_rules["REGION_ROUTE128/MAIN -> REGION_UNDERWATER_ROUTE128/AREA_2"] = hm_rules["HM08 Dive"]

    # Seafloor Cavern
    entrance_rules["REGION_SEAFLOOR_CAVERN_ENTRANCE/MAIN -> REGION_SEAFLOOR_CAVERN_ENTRANCE/WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_SEAFLOOR_CAVERN_ENTRANCE/WATER -> REGION_UNDERWATER_SEAFLOOR_CAVERN/MAIN"] = hm_rules["HM08 Dive"]
    entrance_rules["REGION_SEAFLOOR_CAVERN_ROOM1/SOUTH -> REGION_SEAFLOOR_CAVERN_ROOM1/NORTH"] = hm_rules["HM06 Rock Smash"] & hm_rules["HM04 Strength"]
    entrance_rules["REGION_SEAFLOOR_CAVERN_ROOM1/NORTH -> REGION_SEAFLOOR_CAVERN_ROOM1/SOUTH"] = hm_rules["HM04 Strength"]
    entrance_rules["REGION_SEAFLOOR_CAVERN_ROOM2/SOUTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM2/NORTH_WEST"] = hm_rules["HM04 Strength"]
    entrance_rules["REGION_SEAFLOOR_CAVERN_ROOM2/NORTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM2/SOUTH_WEST"] = hm_rules["HM04 Strength"]
    entrance_rules["REGION_SEAFLOOR_CAVERN_ROOM2/SOUTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM2/SOUTH_EAST"] = hm_rules["HM06 Rock Smash"]
    entrance_rules["REGION_SEAFLOOR_CAVERN_ROOM2/SOUTH_EAST -> REGION_SEAFLOOR_CAVERN_ROOM2/SOUTH_WEST"] = hm_rules["HM06 Rock Smash"]
    entrance_rules["REGION_SEAFLOOR_CAVERN_ROOM2/NORTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM2/NORTH_EAST"] = hm_rules["HM06 Rock Smash"] & hm_rules["HM04 Strength"]
    entrance_rules["REGION_SEAFLOOR_CAVERN_ROOM2/NORTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM2/SOUTH_EAST"] = hm_rules["HM06 Rock Smash"] & hm_rules["HM04 Strength"]
    entrance_rules["REGION_SEAFLOOR_CAVERN_ROOM5/NORTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM5/EAST"] = hm_rules["HM06 Rock Smash"] & hm_rules["HM04 Strength"]
    entrance_rules["REGION_SEAFLOOR_CAVERN_ROOM5/EAST -> REGION_SEAFLOOR_CAVERN_ROOM5/NORTH_WEST"] = hm_rules["HM04 Strength"]
    entrance_rules["REGION_SEAFLOOR_CAVERN_ROOM5/NORTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM5/SOUTH_WEST"] = hm_rules["HM06 Rock Smash"] & hm_rules["HM04 Strength"]
    entrance_rules["REGION_SEAFLOOR_CAVERN_ROOM5/SOUTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM5/NORTH_WEST"] = hm_rules["HM06 Rock Smash"] & hm_rules["HM04 Strength"]
    entrance_rules["REGION_SEAFLOOR_CAVERN_ROOM6/NORTH_WEST -> REGION_SEAFLOOR_CAVERN_ROOM6/WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_SEAFLOOR_CAVERN_ROOM6/SOUTH -> REGION_SEAFLOOR_CAVERN_ROOM6/WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_SEAFLOOR_CAVERN_ROOM7/SOUTH -> REGION_SEAFLOOR_CAVERN_ROOM7/WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_SEAFLOOR_CAVERN_ROOM7/NORTH -> REGION_SEAFLOOR_CAVERN_ROOM7/WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_SEAFLOOR_CAVERN_ROOM8/NORTH -> REGION_SEAFLOOR_CAVERN_ROOM8/SOUTH"] = hm_rules["HM04 Strength"]
    entrance_rules["REGION_SEAFLOOR_CAVERN_ROOM8/SOUTH -> REGION_SEAFLOOR_CAVERN_ROOM8/NORTH"] = hm_rules["HM04 Strength"]
    entrance_rules["MAP_SEAFLOOR_CAVERN_ENTRANCE:1/MAP_SEAFLOOR_CAVERN_ROOM1:0"] = (
        OptionFilter(RemoveRoadblocks, "Seafloor Cavern Aqua Grunt", "contains") | Has("EVENT_STEVEN_GIVES_DIVE")
    )

    # Route 129
    entrance_rules["REGION_UNDERWATER_ROUTE129/MARINE_CAVE_ENTRANCE_1 -> REGION_UNDERWATER_MARINE_CAVE/MAIN"] = (
        hm_rules["HM08 Dive"] & HasAll("EVENT_DEFEAT_CHAMPION", "MARINE_CAVE_ROUTE_129_1", "EVENT_DEFEAT_SHELLY")
    )
    entrance_rules["REGION_UNDERWATER_ROUTE129/MARINE_CAVE_ENTRANCE_2 -> REGION_UNDERWATER_MARINE_CAVE/MAIN"] = (
        hm_rules["HM08 Dive"] & HasAll("EVENT_DEFEAT_CHAMPION", "MARINE_CAVE_ROUTE_129_2", "EVENT_DEFEAT_SHELLY")
    )

    # Pacifidlog Town
    entrance_rules["REGION_PACIFIDLOG_TOWN/MAIN -> REGION_PACIFIDLOG_TOWN/WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_PACIFIDLOG_TOWN/MAIN -> REGION_ROUTE131/MAIN"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_PACIFIDLOG_TOWN/MAIN -> REGION_ROUTE132/EAST"] = hm_rules["HM03 Surf"]

    # Sky Pillar
    location_rules["EVENT_ENCOUNTER_RAYQUAZA"] = Has("EVENT_RAYQUAZA_STOPS_FIGHT")

    entrance_rules["MAP_SKY_PILLAR_OUTSIDE:1/MAP_SKY_PILLAR_1F:0"] = Has("EVENT_RELEASE_KYOGRE")
    entrance_rules["REGION_SKY_PILLAR_2F/RIGHT -> REGION_SKY_PILLAR_2F/LEFT"] = Has("Mach Bike")
    entrance_rules["REGION_SKY_PILLAR_2F/LEFT -> REGION_SKY_PILLAR_2F/RIGHT"] = Has("Mach Bike")
    entrance_rules["REGION_SKY_PILLAR_4F/MAIN -> REGION_SKY_PILLAR_4F/ABOVE_3F_TOP_CENTER"] = Has("Mach Bike")

    # Route 134
    location_rules["EVENT_UNDO_REGI_SEAL"] = HasAll("CATCH_SPECIES_WAILORD", "CATCH_SPECIES_RELICANTH")

    entrance_rules["REGION_ROUTE134/MAIN -> REGION_UNDERWATER_ROUTE134/MAIN"] = hm_rules["HM08 Dive"]
    entrance_rules["REGION_SEALED_CHAMBER_OUTER_ROOM/MAIN -> REGION_SEALED_CHAMBER_OUTER_ROOM/CRUMBLED_WALL"] = Has("EVENT_MOVE_TUTOR_DIG")

    # Ever Grande City
    entrance_rules["REGION_EVER_GRANDE_CITY/SEA -> REGION_EVER_GRANDE_CITY/SOUTH"] = hm_rules["HM07 Waterfall"]
    entrance_rules["REGION_EVER_GRANDE_CITY/SOUTH -> REGION_EVER_GRANDE_CITY/SEA"] = hm_rules["HM03 Surf"]

    # Victory Road
    entrance_rules["REGION_VICTORY_ROAD_B1F/SOUTH_WEST_MAIN -> REGION_VICTORY_ROAD_B1F/SOUTH_WEST_LADDER_UP"] = hm_rules["HM06 Rock Smash"] & hm_rules["HM04 Strength"]
    entrance_rules["REGION_VICTORY_ROAD_B1F/SOUTH_WEST_LADDER_UP -> REGION_VICTORY_ROAD_B1F/SOUTH_WEST_MAIN"] = hm_rules["HM06 Rock Smash"] & hm_rules["HM04 Strength"]
    entrance_rules["REGION_VICTORY_ROAD_B1F/MAIN_UPPER -> REGION_VICTORY_ROAD_B1F/MAIN_LOWER_EAST"] = hm_rules["HM06 Rock Smash"] & hm_rules["HM04 Strength"]
    entrance_rules["REGION_VICTORY_ROAD_B1F/MAIN_LOWER_EAST -> REGION_VICTORY_ROAD_B1F/MAIN_LOWER_WEST"] = hm_rules["HM06 Rock Smash"]
    entrance_rules["REGION_VICTORY_ROAD_B1F/MAIN_LOWER_WEST -> REGION_VICTORY_ROAD_B1F/MAIN_LOWER_EAST"] = hm_rules["HM06 Rock Smash"] & hm_rules["HM04 Strength"]
    entrance_rules["REGION_VICTORY_ROAD_B1F/MAIN_LOWER_WEST -> REGION_VICTORY_ROAD_B1F/MAIN_UPPER"] = hm_rules["HM06 Rock Smash"] & hm_rules["HM04 Strength"]
    entrance_rules["REGION_VICTORY_ROAD_B2F/LOWER_WEST -> REGION_VICTORY_ROAD_B2F/LOWER_WEST_WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_VICTORY_ROAD_B2F/LOWER_WEST_ISLAND -> REGION_VICTORY_ROAD_B2F/LOWER_WEST_WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_VICTORY_ROAD_B2F/LOWER_EAST -> REGION_VICTORY_ROAD_B2F/LOWER_EAST_WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_VICTORY_ROAD_B2F/LOWER_WEST_WATER -> REGION_VICTORY_ROAD_B2F/UPPER_WATER"] = hm_rules["HM07 Waterfall"]
    entrance_rules["REGION_VICTORY_ROAD_B2F/LOWER_EAST_WATER -> REGION_VICTORY_ROAD_B2F/UPPER_WATER"] = hm_rules["HM07 Waterfall"]
    entrance_rules["REGION_VICTORY_ROAD_B2F/UPPER -> REGION_VICTORY_ROAD_B2F/UPPER_WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_VICTORY_ROAD_B2F/UPPER -> REGION_VICTORY_ROAD_B2F/LOWER_EAST_WATER"] = hm_rules["HM03 Surf"]

    # Pokemon League
    entrance_rules["REGION_EVER_GRANDE_CITY_POKEMON_LEAGUE_1F/MAIN -> REGION_EVER_GRANDE_CITY_POKEMON_LEAGUE_1F/BEHIND_BADGE_CHECKERS"] = (
        (
            OptionFilter(EliteFourRequirement, EliteFourRequirement.option_badges) &
            HasGroupUnique("Badge", world.options.elite_four_count.value)
        ) |
        (
            OptionFilter(EliteFourRequirement, EliteFourRequirement.option_gyms) &
            create_defeated_n_gym_leaders_rule(world.options.elite_four_count.value)
        )
    )

    # Battle Frontier
    entrance_rules["REGION_BATTLE_FRONTIER_OUTSIDE_WEST/DOCK -> REGION_SS_TIDAL_CORRIDOR/MAIN"] = Has("S.S. Ticket")
    entrance_rules["REGION_BATTLE_FRONTIER_OUTSIDE_WEST/CAVE_ENTRANCE -> REGION_BATTLE_FRONTIER_OUTSIDE_WEST/WATER"] = hm_rules["HM03 Surf"]
    entrance_rules["REGION_BATTLE_FRONTIER_OUTSIDE_EAST/MAIN -> REGION_BATTLE_FRONTIER_OUTSIDE_EAST/ABOVE_WATERFALL"] = Has("Wailmer Pail") & hm_rules["HM03 Surf"]
    entrance_rules["REGION_BATTLE_FRONTIER_OUTSIDE_EAST/ABOVE_WATERFALL -> REGION_BATTLE_FRONTIER_OUTSIDE_EAST/MAIN"] = Has("Wailmer Pail")
    entrance_rules["REGION_BATTLE_FRONTIER_OUTSIDE_EAST/WATER -> REGION_BATTLE_FRONTIER_OUTSIDE_EAST/ABOVE_WATERFALL"] = hm_rules["HM07 Waterfall"]

    # Pokedex Rewards
    if world.options.dexsanity:
        for i in range(NUM_REAL_SPECIES):
            species = data.species[NATIONAL_ID_TO_SPECIES_ID[i + 1]]

            if species.species_id in world.blacklisted_wilds:
                continue

            location_rules[f"Pokedex - {species.label}"] = Has(f"CATCH_{species.name}")

        # Legendary hunt prevents Latios from being a wild spawn so the roamer
        # can be tracked, and also guarantees that the roamer is a Latios.
        if world.options.goal == Goal.option_legendary_hunt and \
                data.constants["SPECIES_LATIOS"] not in world.blacklisted_wilds:
            location_rules[f"Pokedex - Latios"] = Has("EVENT_ENCOUNTER_LATIOS")

    # Overworld Items
    if world.options.overworld_items:
        # Route 117
        location_rules["ITEM_ROUTE_117_REVIVE"] = hm_rules["HM01 Cut"]

        # Route 114
        location_rules["ITEM_ROUTE_114_PROTEIN"] = hm_rules["HM06 Rock Smash"]

        # Victory Road
        location_rules["ITEM_VICTORY_ROAD_B1F_FULL_RESTORE"] = hm_rules["HM06 Rock Smash"] & hm_rules["HM04 Strength"]

    # Hidden Items
    if world.options.hidden_items:
        # Route 120
        location_rules["HIDDEN_ITEM_ROUTE_120_RARE_CANDY_1"] = hm_rules["HM01 Cut"]

        # Route 121
        location_rules["HIDDEN_ITEM_ROUTE_121_NUGGET"] = hm_rules["HM01 Cut"]

    # NPC Gifts
    if world.options.npc_gifts:
        # Littleroot Town
        location_rules["NPC_GIFT_RECEIVED_AMULET_COIN"] = HasAll("EVENT_TALK_TO_MR_STONE", "Balance Badge")

        # Route 104
        location_rules["NPC_GIFT_RECEIVED_WHITE_HERB"] = HasAll("Dynamo Badge", "EVENT_MEET_FLOWER_SHOP_OWNER")

        # Devon Corp
        location_rules["NPC_GIFT_RECEIVED_EXP_SHARE"] = Has("EVENT_DELIVER_LETTER")

        # Route 116
        location_rules["NPC_GIFT_RECEIVED_REPEAT_BALL"] = Has("EVENT_RESCUE_CAPT_STERN")

        # Dewford Town
        location_rules["NPC_GIFT_RECEIVED_TM_SLUDGE_BOMB"] = Has("EVENT_DEFEAT_NORMAN")

        # Slateport City
        location_rules["NPC_GIFT_RECEIVED_DEEP_SEA_TOOTH"] = (
            HasAll("EVENT_AQUA_STEALS_SUBMARINE", "Scanner", "Mind Badge")
        )
        location_rules["NPC_GIFT_RECEIVED_DEEP_SEA_SCALE"] = (
            HasAll("EVENT_AQUA_STEALS_SUBMARINE", "Scanner", "Mind Badge")
        )

        # Mauville City
        location_rules["NPC_GIFT_GOT_TM_THUNDERBOLT_FROM_WATTSON"] = (
            HasAll("EVENT_DEFEAT_NORMAN", "EVENT_TURN_OFF_GENERATOR")
        )

        # Fallarbor Town
        location_rules["NPC_GIFT_RECEIVED_TM_RETURN"] = HasAll("EVENT_RECOVER_METEORITE", "Meteorite")

        # Fortree City
        location_rules["NPC_GIFT_RECEIVED_MENTAL_HERB"] = Has("EVENT_WINGULL_QUEST_2")

    # Add Itemfinder requirement to hidden items
    if world.options.require_itemfinder:
        for location in world.multiworld.get_locations(world.player):
            assert isinstance(location, PokemonEmeraldLocation)
            if location.key is not None and data.locations[location.key].category == LocationCategory.HIDDEN_ITEM:
                add_rule(location_rules, location.key, Has("Itemfinder"))

    # Add Flash requirements to dark caves
    # Granite Cave
    if world.options.require_flash in [DarkCavesRequireFlash.option_only_granite_cave, DarkCavesRequireFlash.option_both]:
        add_rule(entrance_rules, "MAP_GRANITE_CAVE_1F:2/MAP_GRANITE_CAVE_B1F:1", hm_rules["HM05 Flash"])
        add_rule(entrance_rules, "MAP_GRANITE_CAVE_B1F:3/MAP_GRANITE_CAVE_B2F:1", hm_rules["HM05 Flash"])

    # Victory Road
    if world.options.require_flash in [DarkCavesRequireFlash.option_only_victory_road, DarkCavesRequireFlash.option_both]:
        add_rule(entrance_rules, "MAP_VICTORY_ROAD_1F:2/MAP_VICTORY_ROAD_B1F:5", hm_rules["HM05 Flash"])
        add_rule(entrance_rules, "MAP_VICTORY_ROAD_1F:4/MAP_VICTORY_ROAD_B1F:4", hm_rules["HM05 Flash"])
        add_rule(entrance_rules, "MAP_VICTORY_ROAD_1F:3/MAP_VICTORY_ROAD_B1F:2", hm_rules["HM05 Flash"])
        add_rule(entrance_rules, "MAP_VICTORY_ROAD_B1F:3/MAP_VICTORY_ROAD_B2F:1", hm_rules["HM05 Flash"])
        add_rule(entrance_rules, "MAP_VICTORY_ROAD_B1F:1/MAP_VICTORY_ROAD_B2F:2", hm_rules["HM05 Flash"])
        add_rule(entrance_rules, "MAP_VICTORY_ROAD_B1F:6/MAP_VICTORY_ROAD_B2F:3", hm_rules["HM05 Flash"])
        add_rule(entrance_rules, "MAP_VICTORY_ROAD_B1F:0/MAP_VICTORY_ROAD_B2F:0", hm_rules["HM05 Flash"])
        add_rule(entrance_rules, "MAP_VICTORY_ROAD_B2F:3/MAP_VICTORY_ROAD_B1F:6", hm_rules["HM05 Flash"])
        add_rule(entrance_rules, "MAP_VICTORY_ROAD_B2F:2/MAP_VICTORY_ROAD_B1F:1", hm_rules["HM05 Flash"])
        add_rule(entrance_rules, "MAP_VICTORY_ROAD_B2F:0/MAP_VICTORY_ROAD_B1F:0", hm_rules["HM05 Flash"])
        add_rule(entrance_rules, "MAP_VICTORY_ROAD_B2F:1/MAP_VICTORY_ROAD_B1F:3", hm_rules["HM05 Flash"])

    for name, rule in entrance_rules.items():
        world.set_rule(world.get_entrance(name), rule)

    for name, rule in location_rules.items():
        if name in data.locations:
            name = data.locations[name].label
        world.set_rule(world.get_location(name), rule)
