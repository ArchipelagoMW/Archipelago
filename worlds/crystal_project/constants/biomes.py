from .regions import *

SPAWNING_MEADOWS_IDS = {1}
DELENDE_IDS = {2, 10, 155}
SOILED_DEN_IDS = {49}
PALE_GROTTO_IDS = {107, 123}
SEASIDE_CLIFF_IDS = {3, 106, 128, 160, 164}
DRAFT_SHAFT_CONDUITS_IDS = {6, 125, 126}
MERCURY_SHRINE_IDS = {9, 159}
YAMAGAWA_MA_IDS = {5, 127}
PROVING_MEADOWS_IDS = {7, 161}
SKUMPARADISE_IDS = {11, 12, 182, 183}
CAPITAL_IDS = {14, 37, 41, 48, 68, 102}
JOJO_SEWERS_IDS = {16, 47}
BOOMER_SOCIETY_IDS = {23}
ROLLING_QUINTAR_FIELDS_IDS = {15, 81}
QUINTAR_NEST_IDS = {18}
QUINTAR_SANCTUM_IDS = {39, 40}
CAPITAL_JAIL_IDS = {17, 193}
CAPITAL_PIPELINE_IDS = {24, 99}
COBBLESTONE_CRAG_IDS = {32}
OKIMOTO_IDS = {20, 192}
GREENSHIRE_IDS = {13, 158}
SALMON_PASS_IDS = {46}
SALMON_RIVER_IDS = {28, 31, 78}
POKO_POKO_IDS = {26, 51, 124, 167, 195}
SARA_SARA_IDS = {27, 122}
SARA_SARA_BEACH_IDS = {33}
ANCIENT_RESERVOIR_IDS = {30, 66, 85, 86, 87}
SALMON_BAY_IDS = {60, 67}
OPEN_SEA_IDS = {34, 129, 185}
WATERFRONT_IDS = {115}
SHOUDU_IDS = {38, 71, 83, 109}
Undercity_IDS = {43}
GANYMEDE_IDS = {50}
BEAURIOR_VOLCANO_IDS = {44}
BEAURIOR_ROCK_IDS = {19, 70, 142, 144, 145, 146, 147}
LAKE_DELENDE_IDS = {53}
QUINTAR_RESERVE_IDS = {52}
DIONE_SHRINE_IDS = {76, 105, 112, 130, 173}
QUINTAR_MAUSOLEUM_IDS = {143, 172}
EASTERN_CHASM_IDS = {132, 134, 149, 152, 166}
TALL_TALL_HEIGHTS_IDS = {8, 95, 153, 179}
NORTHERN_CAVE_IDS = {77}
LANDS_END_IDS = {62, 63, 64, 65, 88, 116, 157}
SLIP_GLIDE_RIDE_IDS = {36}
SEQUOIA_ATHENAEUM_IDS = {90, 91, 174, 175, 176}
NORTHERN_STRETCH_IDS = {131, 156}
CASTLE_RAMPARTS_IDS = {57}
CHALICE_OF_TAR_IDS = {121}
FLYERS_CRAG_IDS = {61}
JIDAMBA_IDS = {29, 54, 72, 84, 165}
EACLANEYA_IDS = {55, 89, 113, 114, 162}
DEEP_SEA_IDS = {35, 82, 96, 100, 103, 104, 120, 133, 186}
NEPTUNE_SHRINE_IDS = {135}
JADE_CAVERN_IDS = {154}
CONTINENTAL_TRAM_IDS = {79, 80}
ANCIENT_LABYRINTH_IDS = {56, 136, 137, 138, 139, 140, 150}
SEQUOIA_IDS = {22, 45, 92, 101, 188}
DEPTHS_IDS = {42, 97}
CASTLE_SEQUOIA_IDS = {58, 69, 73, 74, 75, 93, 94, 177}
NEW_WORLD_IDS = {59, 111, 180}
OLD_WORLD_IDS = {178}
#TODO Underpass, overpass

def get_region_by_id(region_id: int) -> str:
    if region_id in SPAWNING_MEADOWS_IDS:
        return SPAWNING_MEADOWS
    if region_id in DELENDE_IDS:
        return DELENDE
    if region_id in SOILED_DEN_IDS:
        return SOILED_DEN
    if region_id in PALE_GROTTO_IDS:
        return THE_PALE_GROTTO
    if region_id in SEASIDE_CLIFF_IDS:
        return SEASIDE_CLIFFS
    if region_id in DRAFT_SHAFT_CONDUITS_IDS:
        return DRAFT_SHAFT_CONDUIT
    if region_id in MERCURY_SHRINE_IDS:
        return MERCURY_SHRINE
    if region_id in PROVING_MEADOWS_IDS:
        return PROVING_MEADOWS
    if region_id in YAMAGAWA_MA_IDS:
        return YAMAGAWA_MA
    if region_id in SKUMPARADISE_IDS:
        return SKUMPARADISE
    if region_id in CAPITAL_IDS:
        return CAPITAL_SEQUOIA
    if region_id in JOJO_SEWERS_IDS:
        return JOJO_SEWERS
    if region_id in BOOMER_SOCIETY_IDS:
        return BOOMER_SOCIETY
    if region_id in ROLLING_QUINTAR_FIELDS_IDS:
        return ROLLING_QUINTAR_FIELDS
    if region_id in QUINTAR_NEST_IDS:
        return QUINTAR_NEST
    if region_id in QUINTAR_SANCTUM_IDS:
        return QUINTAR_SANCTUM
    if region_id in CAPITAL_JAIL_IDS:
        return CAPITAL_JAIL
    if region_id in CAPITAL_PIPELINE_IDS:
        return CAPITAL_PIPELINE
    if region_id in COBBLESTONE_CRAG_IDS:
        return COBBLESTONE_CRAG
    if region_id in OKIMOTO_IDS:
        return OKIMOTO_NS
    if region_id in GREENSHIRE_IDS:
        return GREENSHIRE_REPRISE
    if region_id in SALMON_PASS_IDS:
        return SALMON_PASS
    if region_id in SALMON_RIVER_IDS:
        return SALMON_RIVER
    if region_id in POKO_POKO_IDS:
        return POKO_POKO_DESERT
    if region_id in SARA_SARA_IDS:
        return SARA_SARA_BAZAAR
    if region_id in SARA_SARA_BEACH_IDS:
        #No idea why there are two of these now, but we have no way to know so just pick one
        return SARA_SARA_BEACH_EAST
    if region_id in ANCIENT_RESERVOIR_IDS:
        return ANCIENT_RESERVOIR
    if region_id in SALMON_BAY_IDS:
        return SALMON_BAY
    if region_id in OPEN_SEA_IDS:
        return THE_OPEN_SEA
    if region_id in WATERFRONT_IDS:
        return SHOUDU_WATERFRONT
    if region_id in SHOUDU_IDS:
        return SHOUDU_PROVINCE
    if region_id in Undercity_IDS:
        return THE_UNDERCITY
    if region_id in GANYMEDE_IDS:
        return GANYMEDE_SHRINE
    if region_id in BEAURIOR_VOLCANO_IDS:
        return BEAURIOR_VOLCANO
    if region_id in BEAURIOR_ROCK_IDS:
        return BEAURIOR_ROCK
    if region_id in LAKE_DELENDE_IDS:
        return LAKE_DELENDE
    if region_id in QUINTAR_RESERVE_IDS:
        return QUINTAR_RESERVE
    if region_id in DIONE_SHRINE_IDS:
        return DIONE_SHRINE
    if region_id in QUINTAR_MAUSOLEUM_IDS:
        return QUINTAR_MAUSOLEUM
    if region_id in EASTERN_CHASM_IDS:
        return EASTERN_CHASM
    if region_id in TALL_TALL_HEIGHTS_IDS:
        return TALL_TALL_HEIGHTS
    if region_id in NORTHERN_CAVE_IDS:
        return NORTHERN_CAVE
    if region_id in LANDS_END_IDS:
        return LANDS_END
    if region_id in SLIP_GLIDE_RIDE_IDS:
        return SLIP_GLIDE_RIDE
    if region_id in SEQUOIA_ATHENAEUM_IDS:
        return SEQUOIA_ATHENAEUM
    if region_id in NORTHERN_STRETCH_IDS:
        return NORTHERN_STRETCH
    if region_id in CASTLE_RAMPARTS_IDS:
        return CASTLE_RAMPARTS
    if region_id in CHALICE_OF_TAR_IDS:
        return THE_CHALICE_OF_TAR
    if region_id in FLYERS_CRAG_IDS:
        return FLYERS_CRAG
    if region_id in JIDAMBA_IDS:
        return JIDAMBA_TANGLE
    if region_id in EACLANEYA_IDS:
        return JIDAMBA_EACLANEYA
    if region_id in DEEP_SEA_IDS:
        return THE_DEEP_SEA
    if region_id in NEPTUNE_SHRINE_IDS:
        return NEPTUNE_SHRINE
    if region_id in JADE_CAVERN_IDS:
        return JADE_CAVERN
    if region_id in CONTINENTAL_TRAM_IDS:
        return CONTINENTAL_TRAM
    if region_id in ANCIENT_LABYRINTH_IDS:
        return ANCIENT_LABYRINTH
    if region_id in SEQUOIA_IDS:
        return THE_SEQUOIA
    if region_id in DEPTHS_IDS:
        return THE_DEPTHS
    if region_id in CASTLE_SEQUOIA_IDS:
        return CASTLE_SEQUOIA
    if region_id in NEW_WORLD_IDS:
        return THE_NEW_WORLD
    if region_id in OLD_WORLD_IDS:
        return THE_OLD_WORLD

    return MENU