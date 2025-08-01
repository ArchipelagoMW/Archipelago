from typing import List, Dict, Tuple, Callable, Optional, Union, Iterable, TYPE_CHECKING
from BaseClasses import Region, Location, CollectionState
from .options import CrystalProjectOptions
from .locations import LocationData
from .items import region_name_to_pass_dict
from .rules import CrystalProjectLogic
from .constants.keys import *
from .constants.key_items import *
from .constants.regions import *
from .constants.teleport_stones import *
from .constants.region_passes import *

if TYPE_CHECKING:
    from . import CrystalProjectWorld

region_levels_dictionary: Dict[str, Tuple[int, int]] = {
    #Beginner
    MENU: (0, 0),
    SPAWNING_MEADOWS: (3, 3),
    DELENDE: (5, 10),
    SOILED_DEN: (7, 7),
    THE_PALE_GROTTO: (7, 10),
    SEASIDE_CLIFFS: (10, 15),
    DRAFT_SHAFT_CONDUIT: (12, 12),
    MERCURY_SHRINE: (0, 0),
    YAMAGAWA_MA: (15, 15),
    PROVING_MEADOWS: (0, 0),
    SKUMPARADISE: (15, 17),
    # #Advanced
    CAPITAL_SEQUOIA: (0, 0),
    JOJO_SEWERS: (20, 22),
    BOOMER_SOCIETY: (0, 0),
    ROLLING_QUINTAR_FIELDS: (18, 21),
    QUINTAR_NEST: (18, 22),
    QUINTAR_SANCTUM: (21, 21),
    CAPITAL_JAIL: (24, 27),
    CAPITAL_PIPELINE: (50, 50),
    COBBLESTONE_CRAG: (0, 0),
    OKIMOTO_NS: (27, 31),
    GREENSHIRE_REPRISE: (33, 33),
    SALMON_PASS: (0, 0),
    SALMON_RIVER: (26, 29),
    SHOUDU_WATERFRONT: (0, 0),
    POKO_POKO_DESERT: (30, 32),
    SARA_SARA_BAZAAR: (0, 0),
    SARA_SARA_BEACH_EAST: (30, 30),
    SARA_SARA_BEACH_WEST: (38, 40),
    ANCIENT_RESERVOIR: (33, 35),
    IBEK_CAVE: (35, 35),
    SALMON_BAY: (0, 0),
    # #Expert
    THE_OPEN_SEA: (54, 56),
    SHOUDU_PROVINCE: (36, 37),
    THE_UNDERCITY: (37, 39),
    GANYMEDE_SHRINE: (0, 0),
    BEAURIOR_VOLCANO: (37, 37),
    BEAURIOR_ROCK: (38, 40),
    LAKE_DELENDE: (40, 40),
    QUINTAR_RESERVE: (0, 0),
    DIONE_SHRINE: (0, 0),
    QUINTAR_MAUSOLEUM: (54, 56),
    EASTERN_CHASM: (0, 0),
    TALL_TALL_HEIGHTS: (41, 45),
    NORTHERN_CAVE: (43, 44),
    LANDS_END: (44, 47),
    SLIP_GLIDE_RIDE: (46, 48),
    SEQUOIA_ATHENAEUM: (0, 0),
    NORTHERN_STRETCH: (0, 0),
    CASTLE_RAMPARTS: (50, 50),
    THE_CHALICE_OF_TAR: (60, 60),
    FLYERS_CRAG: (0, 0),
    JIDAMBA_TANGLE: (50, 54),
    JIDAMBA_EACLANEYA: (54, 57),
    THE_DEEP_SEA: (58, 64),
    NEPTUNE_SHRINE: (0, 0),
    JADE_CAVERN: (57, 57),
    CONTINENTAL_TRAM: (0, 0),
    # #End Game
    ANCIENT_LABYRINTH: (62, 66),
    THE_SEQUOIA: (60, 63),
    THE_DEPTHS: (63, 65),
    CASTLE_SEQUOIA: (56, 59),
    THE_OLD_WORLD: (0, 0),
    THE_NEW_WORLD: (60, 60),
    MODDED_ZONE: (30, 30),
}

rules_on_regions: Dict[str, Callable[[CollectionState], bool]] = {}

class CrystalProjectLocation(Location):
    game: str = "CrystalProject"

    def __init__(self, player: int, name: str = " ", address = None, parent=None):
        super().__init__(player, name, address, parent)

def init_areas(world: "CrystalProjectWorld", locations: List[LocationData], options: CrystalProjectOptions) -> None:
    multiworld = world.multiworld
    player = world.player
    logic = CrystalProjectLogic(player, options)
    rules_on_regions[MODDED_ZONE] = lambda state: True

    for region in region_levels_dictionary:
        if world.options.regionsanity.value == world.options.regionsanity.option_true and region != MODDED_ZONE:
            rules_on_regions[region] = lambda state, lambda_region = region: (logic.is_area_in_level_range(state, region_levels_dictionary[lambda_region][0])
                                                                            and state.has(region_name_to_pass_dict[lambda_region], player))

            rules_on_regions[MODDED_ZONE] = combine_callables(rules_on_regions[MODDED_ZONE], rules_on_regions[region])
        else:
            rules_on_regions[region] = lambda state, lambda_region = region: (logic.is_area_in_level_range(state, region_levels_dictionary[lambda_region][0]))

    locations_per_region = get_locations_per_region(locations)

    excluded = False

    beginner_regions = [
        create_region(world, player, locations_per_region, MENU, excluded),
        create_region(world, player, locations_per_region, SPAWNING_MEADOWS, excluded),
        create_region(world, player, locations_per_region, DELENDE, excluded),
        # bumped up mercury shrine because region order influences shop price NOTE TO DRAGONS, DO NOT MOVE WITHOUT REASON!!
        create_region(world, player, locations_per_region, MERCURY_SHRINE, excluded),
        create_region(world, player, locations_per_region, SOILED_DEN, excluded),
        create_region(world, player, locations_per_region, THE_PALE_GROTTO, excluded),
        create_region(world, player, locations_per_region, SEASIDE_CLIFFS, excluded),
        create_region(world, player, locations_per_region, DRAFT_SHAFT_CONDUIT, excluded),
        create_region(world, player, locations_per_region, YAMAGAWA_MA, excluded),
        create_region(world, player, locations_per_region, PROVING_MEADOWS, excluded),
        create_region(world, player, locations_per_region, SKUMPARADISE, excluded),
    ]

    if (options.includedRegions == options.includedRegions.option_advanced or
        options.includedRegions == options.includedRegions.option_expert or
        options.includedRegions == options.includedRegions.option_all):
        excluded = False
    else:
        excluded = True

    advanced_regions = [
        create_region(world, player, locations_per_region, CAPITAL_SEQUOIA, excluded),
        create_region(world, player, locations_per_region, JOJO_SEWERS, excluded),
        create_region(world, player, locations_per_region, BOOMER_SOCIETY, excluded),
        create_region(world, player, locations_per_region, ROLLING_QUINTAR_FIELDS, excluded),
        create_region(world, player, locations_per_region, QUINTAR_NEST, excluded),
        create_region(world, player, locations_per_region, QUINTAR_SANCTUM, excluded),
        create_region(world, player, locations_per_region, CAPITAL_JAIL, excluded),
        create_region(world, player, locations_per_region, CAPITAL_PIPELINE, excluded),
        create_region(world, player, locations_per_region, COBBLESTONE_CRAG, excluded),
        create_region(world, player, locations_per_region, OKIMOTO_NS, excluded),
        create_region(world, player, locations_per_region, GREENSHIRE_REPRISE, excluded),
        create_region(world, player, locations_per_region, SALMON_PASS, excluded),
        create_region(world, player, locations_per_region, SALMON_RIVER, excluded),
        create_region(world, player, locations_per_region, SHOUDU_WATERFRONT, excluded), #moved from Expert to Advanced
        create_region(world, player, locations_per_region, POKO_POKO_DESERT, excluded),
        create_region(world, player, locations_per_region, SARA_SARA_BAZAAR, excluded),
        create_region(world, player, locations_per_region, SARA_SARA_BEACH_EAST, excluded),
        create_region(world, player, locations_per_region, SARA_SARA_BEACH_WEST, excluded),
        create_region(world, player, locations_per_region, ANCIENT_RESERVOIR, excluded),
        create_region(world, player, locations_per_region, IBEK_CAVE, excluded),
        create_region(world, player, locations_per_region, SALMON_BAY, excluded),
    ]

    if (options.includedRegions == options.includedRegions.option_expert or
        options.includedRegions == options.includedRegions.option_all):
        excluded = False
    else:
        excluded = True

    expert_regions = [
        create_region(world, player, locations_per_region, THE_OPEN_SEA, excluded),
        create_region(world, player, locations_per_region, SHOUDU_PROVINCE, excluded),
        create_region(world, player, locations_per_region, THE_UNDERCITY, excluded),
        create_region(world, player, locations_per_region, GANYMEDE_SHRINE, excluded),
        create_region(world, player, locations_per_region, BEAURIOR_VOLCANO, excluded),
        create_region(world, player, locations_per_region, BEAURIOR_ROCK, excluded),
        create_region(world, player, locations_per_region, LAKE_DELENDE, excluded),
        create_region(world, player, locations_per_region, QUINTAR_RESERVE, excluded),
        create_region(world, player, locations_per_region, DIONE_SHRINE, excluded),
        create_region(world, player, locations_per_region, QUINTAR_MAUSOLEUM, excluded),
        create_region(world, player, locations_per_region, EASTERN_CHASM, excluded),
        create_region(world, player, locations_per_region, TALL_TALL_HEIGHTS, excluded),
        create_region(world, player, locations_per_region, NORTHERN_CAVE, excluded),
        create_region(world, player, locations_per_region, LANDS_END, excluded),
        create_region(world, player, locations_per_region, SLIP_GLIDE_RIDE, excluded),
        create_region(world, player, locations_per_region, SEQUOIA_ATHENAEUM, excluded),
        create_region(world, player, locations_per_region, NORTHERN_STRETCH, excluded),
        create_region(world, player, locations_per_region, CASTLE_RAMPARTS, excluded),
        create_region(world, player, locations_per_region, THE_CHALICE_OF_TAR, excluded),
        create_region(world, player, locations_per_region, FLYERS_CRAG, excluded),
        create_region(world, player, locations_per_region, JIDAMBA_TANGLE, excluded),
        create_region(world, player, locations_per_region, JIDAMBA_EACLANEYA, excluded),
        create_region(world, player, locations_per_region, THE_DEEP_SEA, excluded),
        create_region(world, player, locations_per_region, NEPTUNE_SHRINE, excluded),
        create_region(world, player, locations_per_region, JADE_CAVERN, excluded),
        create_region(world, player, locations_per_region, CONTINENTAL_TRAM, excluded),
    ]

    if options.includedRegions == options.includedRegions.option_all:
        excluded = False
    else:
        excluded = True
     
    end_game_regions = [
        create_region(world, player, locations_per_region, ANCIENT_LABYRINTH, excluded),
        create_region(world, player, locations_per_region, THE_SEQUOIA, excluded),
        create_region(world, player, locations_per_region, THE_DEPTHS, excluded),
        create_region(world, player, locations_per_region, CASTLE_SEQUOIA, excluded),
        create_region(world, player, locations_per_region, THE_OLD_WORLD, excluded),
        create_region(world, player, locations_per_region, THE_NEW_WORLD, excluded),
    ]

    if options.useMods:
        excluded = False
    else:
        excluded = True

    modded_regions = [
        create_region(world, player, locations_per_region, MODDED_ZONE, excluded),
    ]

    multiworld.regions += beginner_regions
    multiworld.regions += advanced_regions
    multiworld.regions += expert_regions
    multiworld.regions += end_game_regions
    multiworld.regions += modded_regions

    connect_menu_region(world, options)

    fancy_add_exits(world, SPAWNING_MEADOWS, [DELENDE, MERCURY_SHRINE, POKO_POKO_DESERT, CONTINENTAL_TRAM, BEAURIOR_VOLCANO, YAMAGAWA_MA],
                    {CONTINENTAL_TRAM: lambda state: logic.has_swimming(state) and options.obscureRoutes.value == options.obscureRoutes.option_true,
                    MERCURY_SHRINE: lambda state: logic.has_vertical_movement(state),
                    POKO_POKO_DESERT: lambda state: logic.has_vertical_movement(state) or options.obscureRoutes.value == options.obscureRoutes.option_true,
                    BEAURIOR_VOLCANO: lambda state: logic.has_vertical_movement(state),
                    YAMAGAWA_MA: lambda state: logic.has_swimming(state) or logic.has_vertical_movement(state)})
    fancy_add_exits(world, DELENDE, [SPAWNING_MEADOWS, SOILED_DEN, THE_PALE_GROTTO, YAMAGAWA_MA, SEASIDE_CLIFFS, MERCURY_SHRINE, JADE_CAVERN, ANCIENT_RESERVOIR, GREENSHIRE_REPRISE, SALMON_PASS, PROVING_MEADOWS, LAKE_DELENDE],
                    {JADE_CAVERN: lambda state: logic.has_golden_quintar(state),
                    ANCIENT_RESERVOIR: lambda state: logic.has_swimming(state),
                    SALMON_PASS: lambda state: logic.has_swimming(state),
                    GREENSHIRE_REPRISE: lambda state: logic.has_swimming(state) or options.obscureRoutes.value == options.obscureRoutes.option_true,
                    PROVING_MEADOWS: lambda state: logic.has_horizontal_movement(state) or logic.has_vertical_movement(state),
                    LAKE_DELENDE: lambda state: logic.has_vertical_movement(state) or options.obscureRoutes.value == options.obscureRoutes.option_true})
    fancy_add_exits(world, MERCURY_SHRINE, [DELENDE, SEASIDE_CLIFFS, BEAURIOR_VOLCANO],
                    {BEAURIOR_VOLCANO: lambda state: logic.has_vertical_movement(state)})
    fancy_add_exits(world, SOILED_DEN, [JADE_CAVERN, DELENDE, THE_PALE_GROTTO, DRAFT_SHAFT_CONDUIT],
                    {JADE_CAVERN: lambda state: logic.has_golden_quintar(state),
                    THE_PALE_GROTTO: lambda state: logic.has_swimming(state),
                    DRAFT_SHAFT_CONDUIT: lambda state: logic.has_swimming(state)})
    fancy_add_exits(world, THE_PALE_GROTTO, [DELENDE, SOILED_DEN, PROVING_MEADOWS, JOJO_SEWERS, TALL_TALL_HEIGHTS, SALMON_PASS],
                    {SOILED_DEN: lambda state: logic.has_swimming(state),
                    JOJO_SEWERS: lambda state: logic.has_swimming(state),
                    TALL_TALL_HEIGHTS: lambda state: logic.has_swimming(state),
                    SALMON_PASS: lambda state: logic.has_swimming(state)})
    fancy_add_exits(world, SEASIDE_CLIFFS, [DELENDE, DRAFT_SHAFT_CONDUIT, THE_OPEN_SEA, MERCURY_SHRINE, BEAURIOR_VOLCANO],
                    {BEAURIOR_VOLCANO: lambda state: logic.has_vertical_movement(state),
                    THE_OPEN_SEA: lambda state: logic.has_swimming(state),
                    MERCURY_SHRINE: lambda state: logic.has_vertical_movement(state)})
    fancy_add_exits(world, DRAFT_SHAFT_CONDUIT, [SEASIDE_CLIFFS, SOILED_DEN],
                    {SOILED_DEN: lambda state: logic.has_swimming(state)})
    fancy_add_exits(world, YAMAGAWA_MA, [SPAWNING_MEADOWS, DELENDE, LAKE_DELENDE],
                    {LAKE_DELENDE: lambda state: logic.has_vertical_movement(state) or options.obscureRoutes.value == options.obscureRoutes.option_true})
    fancy_add_exits(world, PROVING_MEADOWS, [DELENDE, THE_PALE_GROTTO, SKUMPARADISE, THE_OPEN_SEA],
                    {SKUMPARADISE: lambda state: logic.has_jobs(state, 3),
                    THE_OPEN_SEA: lambda state: logic.has_swimming(state)})
    fancy_add_exits(world, SKUMPARADISE, [PROVING_MEADOWS, CAPITAL_SEQUOIA],
                    {PROVING_MEADOWS: lambda state: logic.has_jobs(state, 3)})
    fancy_add_exits(world, CAPITAL_SEQUOIA, [JOJO_SEWERS, BOOMER_SOCIETY, ROLLING_QUINTAR_FIELDS, COBBLESTONE_CRAG, GREENSHIRE_REPRISE, CASTLE_SEQUOIA, SKUMPARADISE],
                    # why rental and horizontal both listed?
                    {BOOMER_SOCIETY: lambda state: logic.has_vertical_movement(state) or logic.has_glide(state),
                    COBBLESTONE_CRAG: lambda state: logic.has_key(state, COURTYARD_KEY) or logic.has_rental_quintar(state, ROLLING_QUINTAR_FIELDS) or logic.has_horizontal_movement(state),
                    GREENSHIRE_REPRISE: lambda state: logic.has_jobs(state, 5),
                    #note for eme: technically possible to get into the first dungeon with quintar instead of glide, but it's hard lol; come from Quintar Sanctum save point and go west up mountain and fall down through grate (that part's easy) then the quintar jump to the lamp is hard
                    CASTLE_SEQUOIA: lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)})
    fancy_add_exits(world, JOJO_SEWERS, [CAPITAL_SEQUOIA, BOOMER_SOCIETY, THE_PALE_GROTTO, CAPITAL_JAIL, QUINTAR_NEST],
                    {BOOMER_SOCIETY: lambda state: state.has(JOJO_SEWERS_PASS, player) or logic.options.regionsanity.value == logic.options.regionsanity.option_false or logic.has_swimming(state),
                    CAPITAL_JAIL: lambda state: logic.has_rental_quintar(state, ROLLING_QUINTAR_FIELDS) or logic.has_swimming(state),
                    THE_PALE_GROTTO: lambda state: logic.has_swimming(state),
                    QUINTAR_NEST: lambda state: (logic.has_rental_quintar(state, ROLLING_QUINTAR_FIELDS) or logic.has_swimming(state))})
    fancy_add_exits(world, BOOMER_SOCIETY, [CAPITAL_SEQUOIA, JOJO_SEWERS, GREENSHIRE_REPRISE])
    fancy_add_exits(world, ROLLING_QUINTAR_FIELDS, [CAPITAL_SEQUOIA, QUINTAR_NEST, QUINTAR_SANCTUM, QUINTAR_RESERVE],
                    {QUINTAR_SANCTUM: lambda state: (logic.has_rental_quintar(state, ROLLING_QUINTAR_FIELDS) or logic.has_vertical_movement(state)),
                    QUINTAR_RESERVE: lambda state: logic.has_vertical_movement(state)})
    fancy_add_exits(world, QUINTAR_NEST, [QUINTAR_SANCTUM, COBBLESTONE_CRAG, JOJO_SEWERS],
                    {QUINTAR_SANCTUM: lambda state: logic.has_swimming(state)})
    fancy_add_exits(world, QUINTAR_SANCTUM, [ROLLING_QUINTAR_FIELDS, QUINTAR_NEST, QUINTAR_MAUSOLEUM],
                    {QUINTAR_MAUSOLEUM: lambda state: logic.has_swimming(state),
                    QUINTAR_NEST: lambda state: logic.has_swimming(state)})
    fancy_add_exits(world, CAPITAL_JAIL, [JOJO_SEWERS, CAPITAL_PIPELINE],
                    {CAPITAL_PIPELINE: lambda state: logic.has_key(state, SOUTH_WING_KEY) and logic.has_key(state, CELL_KEY, 6)})
    fancy_add_exits(world, CAPITAL_PIPELINE, [CAPITAL_JAIL, JIDAMBA_TANGLE, CONTINENTAL_TRAM],
                    {JIDAMBA_TANGLE: lambda state: logic.has_vertical_movement(state),
                    CONTINENTAL_TRAM: lambda state: logic.has_vertical_movement(state)})
    fancy_add_exits(world, COBBLESTONE_CRAG, [CAPITAL_SEQUOIA, THE_OPEN_SEA, SHOUDU_WATERFRONT, OKIMOTO_NS],
                    {SHOUDU_WATERFRONT: lambda state: logic.has_horizontal_movement(state),
                    OKIMOTO_NS: lambda state: logic.has_horizontal_movement(state),
                    THE_OPEN_SEA: lambda state: logic.has_swimming(state)})
    fancy_add_exits(world, OKIMOTO_NS, [COBBLESTONE_CRAG, THE_OPEN_SEA, FLYERS_CRAG],
                    {THE_OPEN_SEA: lambda state: logic.has_swimming(state),
                    FLYERS_CRAG: lambda state: (logic.has_glide(state) and logic.has_vertical_movement(state)) or logic.has_swimming(state)})
    fancy_add_exits(world, GREENSHIRE_REPRISE, [CAPITAL_SEQUOIA, SALMON_PASS, TALL_TALL_HEIGHTS],
                    # if we add hard logic, it is possible to jump from the rolling quintar fields onto the cap seq walls from the southeast and manage to bypass the guard and thus the job requirement
                    {SALMON_PASS: lambda state: (logic.has_rental_quintar(state, ROLLING_QUINTAR_FIELDS) and logic.has_jobs(state, 5)) or logic.has_vertical_movement(state),
                    TALL_TALL_HEIGHTS: lambda state: logic.has_vertical_movement(state)})
    fancy_add_exits(world, SALMON_PASS, [GREENSHIRE_REPRISE, SALMON_RIVER, DELENDE],
                    {GREENSHIRE_REPRISE: lambda state: (logic.has_horizontal_movement(state) or logic.has_swimming(state)),
                    SALMON_RIVER: lambda state: logic.has_horizontal_movement(state) or logic.has_swimming(state),
                    DELENDE: lambda state: logic.has_swimming(state)})
    fancy_add_exits(world, SALMON_RIVER, [SALMON_PASS, SALMON_BAY, TALL_TALL_HEIGHTS],
                    {SALMON_BAY: lambda state: (logic.has_vertical_movement(state) and logic.has_glide(state)) or logic.has_swimming(state),
                    TALL_TALL_HEIGHTS: lambda state: logic.has_vertical_movement(state)})
    fancy_add_exits(world, POKO_POKO_DESERT, [SARA_SARA_BAZAAR, ANCIENT_RESERVOIR, LAKE_DELENDE, SALMON_BAY, ANCIENT_LABYRINTH],
                    {ANCIENT_RESERVOIR: lambda state: logic.has_key(state, PYRAMID_KEY),
                    LAKE_DELENDE: lambda state: logic.has_vertical_movement(state),
                    SALMON_BAY: lambda state: logic.has_horizontal_movement(state) and logic.has_vertical_movement(state),
                    ANCIENT_LABYRINTH: lambda state: (state.has(ANCIENT_TABLET_A, player) or options.obscureRoutes.value == options.obscureRoutes.option_true) and logic.has_vertical_movement(state) and logic.has_glide(state)})
    fancy_add_exits(world, SARA_SARA_BAZAAR, [POKO_POKO_DESERT, SARA_SARA_BEACH_EAST, SARA_SARA_BEACH_WEST, SHOUDU_PROVINCE, THE_OPEN_SEA, CONTINENTAL_TRAM],
                    {SARA_SARA_BEACH_WEST: lambda state: logic.has_rental_quintar(state, SARA_SARA_BAZAAR),
                    SHOUDU_PROVINCE: lambda state: state.has(FERRY_PASS, player),
                    THE_OPEN_SEA: lambda state: logic.has_swimming(state),
                    CONTINENTAL_TRAM: lambda state: logic.has_swimming(state) or logic.has_key(state, TRAM_KEY)})
    fancy_add_exits(world, SARA_SARA_BEACH_EAST, [SARA_SARA_BAZAAR, THE_OPEN_SEA, IBEK_CAVE, BEAURIOR_VOLCANO],
                    {IBEK_CAVE: lambda state: logic.has_vertical_movement(state),
                    THE_OPEN_SEA: lambda state: logic.has_swimming(state),
                    BEAURIOR_VOLCANO: lambda state: logic.has_vertical_movement(state)})
    fancy_add_exits(world, SARA_SARA_BEACH_WEST, [POKO_POKO_DESERT, SARA_SARA_BAZAAR, THE_OPEN_SEA],
                    {POKO_POKO_DESERT: lambda state: logic.has_vertical_movement(state),
                    SARA_SARA_BAZAAR: lambda state: logic.has_horizontal_movement(state),
                    THE_OPEN_SEA: lambda state: logic.has_swimming(state)})
    fancy_add_exits(world, ANCIENT_RESERVOIR, [POKO_POKO_DESERT, IBEK_CAVE, DELENDE],
                    {DELENDE: lambda state: logic.has_swimming(state),
                    IBEK_CAVE: lambda state: logic.has_vertical_movement(state)})
    fancy_add_exits(world, IBEK_CAVE, [SARA_SARA_BEACH_EAST],
                    {SARA_SARA_BEACH_EAST: lambda state: logic.has_vertical_movement(state)})
    fancy_add_exits(world, SALMON_BAY, [THE_OPEN_SEA, SALMON_RIVER],
                    {THE_OPEN_SEA: lambda state: logic.has_swimming(state),
                    SALMON_RIVER: lambda state: logic.has_swimming(state)})
    fancy_add_exits(world, THE_OPEN_SEA, [SEASIDE_CLIFFS, PROVING_MEADOWS, OKIMOTO_NS, SHOUDU_WATERFRONT, SARA_SARA_BAZAAR, SARA_SARA_BEACH_EAST, SARA_SARA_BEACH_WEST, SALMON_BAY, SHOUDU_PROVINCE, THE_UNDERCITY, JIDAMBA_TANGLE, THE_DEEP_SEA],
                    {SEASIDE_CLIFFS: lambda state: logic.has_swimming(state),
                    PROVING_MEADOWS: lambda state: logic.has_swimming(state),
                    OKIMOTO_NS: lambda state: logic.has_swimming(state),
                    SHOUDU_WATERFRONT: lambda state: logic.has_swimming(state),
                    THE_UNDERCITY: lambda state: logic.has_swimming(state),
                    SARA_SARA_BAZAAR: lambda state: logic.has_swimming(state),
                    SARA_SARA_BEACH_EAST: lambda state: logic.has_swimming(state),
                    SARA_SARA_BEACH_WEST: lambda state: logic.has_swimming(state),
                    SALMON_BAY: lambda state: logic.has_swimming(state),
                    SHOUDU_PROVINCE: lambda state: logic.has_swimming(state),
                    JIDAMBA_TANGLE: lambda state: logic.has_swimming(state),
                    THE_DEEP_SEA: lambda state: logic.has_swimming(state)})
    fancy_add_exits(world, SHOUDU_WATERFRONT, [THE_OPEN_SEA, SHOUDU_PROVINCE, COBBLESTONE_CRAG],
                    {THE_OPEN_SEA: lambda state: logic.has_swimming(state),
                    SHOUDU_PROVINCE: lambda state: logic.has_vertical_movement(state),
                    COBBLESTONE_CRAG: lambda state: logic.has_horizontal_movement(state)})
    fancy_add_exits(world, SHOUDU_PROVINCE, [SARA_SARA_BAZAAR, SHOUDU_WATERFRONT, GANYMEDE_SHRINE, THE_UNDERCITY, QUINTAR_RESERVE],
                    {SARA_SARA_BAZAAR: lambda state: state.has(FERRY_PASS, player),
                    GANYMEDE_SHRINE: lambda state: logic.has_vertical_movement(state),
                    QUINTAR_RESERVE: lambda state: logic.has_vertical_movement(state) and state.has(ELEVATOR_PART, player, 10)})
    fancy_add_exits(world, THE_UNDERCITY, [SHOUDU_PROVINCE, THE_OPEN_SEA],
                    {THE_OPEN_SEA: lambda state: logic.has_swimming(state)})
    fancy_add_exits(world, GANYMEDE_SHRINE, [SHOUDU_PROVINCE])
    fancy_add_exits(world, BEAURIOR_VOLCANO, [SARA_SARA_BEACH_EAST, BEAURIOR_ROCK, THE_OPEN_SEA],
                    {BEAURIOR_ROCK: lambda state: logic.has_vertical_movement(state),
                    THE_OPEN_SEA: lambda state: logic.has_swimming(state)})
    fancy_add_exits(world, BEAURIOR_ROCK, [BEAURIOR_VOLCANO])
    fancy_add_exits(world, LAKE_DELENDE, [POKO_POKO_DESERT, DELENDE],
                    {POKO_POKO_DESERT: lambda state: logic.has_vertical_movement(state),
                    DELENDE: lambda state: logic.has_vertical_movement(state)})
    fancy_add_exits(world, QUINTAR_RESERVE, [SHOUDU_PROVINCE, DIONE_SHRINE, QUINTAR_MAUSOLEUM],
                    {QUINTAR_MAUSOLEUM: lambda state: logic.has_swimming(state)})
    fancy_add_exits(world, DIONE_SHRINE, [QUINTAR_RESERVE, EASTERN_CHASM, JIDAMBA_TANGLE, THE_CHALICE_OF_TAR],
                    {JIDAMBA_TANGLE: lambda state: logic.has_glide(state),
                    THE_CHALICE_OF_TAR: lambda state: logic.has_glide(state) and state.has(DIONE_STONE, player),
                    EASTERN_CHASM: lambda state: logic.has_glide(state) and logic.has_vertical_movement(state)})
    fancy_add_exits(world, QUINTAR_MAUSOLEUM, [QUINTAR_RESERVE, QUINTAR_SANCTUM],
                    {QUINTAR_RESERVE: lambda state: logic.has_swimming(state),
                    QUINTAR_SANCTUM: lambda state: logic.has_swimming(state)})
    fancy_add_exits(world, EASTERN_CHASM, [QUINTAR_RESERVE, THE_OPEN_SEA],
                    {QUINTAR_RESERVE: lambda state: logic.has_glide(state),
                    THE_OPEN_SEA: lambda state: logic.has_swimming(state)})
    fancy_add_exits(world, TALL_TALL_HEIGHTS, [SALMON_RIVER, GREENSHIRE_REPRISE, LANDS_END, SEQUOIA_ATHENAEUM, NORTHERN_STRETCH, CASTLE_RAMPARTS, THE_CHALICE_OF_TAR, THE_PALE_GROTTO, NORTHERN_CAVE],
                    {LANDS_END: lambda state: logic.has_vertical_movement(state),
                    SEQUOIA_ATHENAEUM: lambda state: state.has(VERMILLION_BOOK, player) and state.has(VIRIDIAN_BOOK, player) and state.has(CERULEAN_BOOK, player),
                    NORTHERN_STRETCH: lambda state: logic.has_glide(state),
                    CASTLE_RAMPARTS: lambda state: logic.has_vertical_movement(state),
                    THE_PALE_GROTTO: lambda state: logic.has_swimming(state),
                    THE_CHALICE_OF_TAR: lambda state: logic.has_glide(state) and logic.has_vertical_movement(state)})
    fancy_add_exits(world, NORTHERN_CAVE, [TALL_TALL_HEIGHTS, SLIP_GLIDE_RIDE],
                    {SLIP_GLIDE_RIDE: lambda state: logic.has_glide(state) and logic.has_vertical_movement(state),
                    TALL_TALL_HEIGHTS: lambda state: logic.has_vertical_movement(state)})
    fancy_add_exits(world, LANDS_END, [TALL_TALL_HEIGHTS, JIDAMBA_TANGLE],
                    {JIDAMBA_TANGLE: lambda state: logic.has_glide(state),
                    TALL_TALL_HEIGHTS: lambda state: logic.has_vertical_movement(state)})
    fancy_add_exits(world, SLIP_GLIDE_RIDE, [TALL_TALL_HEIGHTS, NORTHERN_CAVE],
                    {NORTHERN_CAVE: lambda state: logic.has_glide(state),
                    TALL_TALL_HEIGHTS: lambda state: logic.has_vertical_movement(state) and logic.has_glide(state)})
    fancy_add_exits(world, SEQUOIA_ATHENAEUM, [TALL_TALL_HEIGHTS],
                    {TALL_TALL_HEIGHTS: lambda state: logic.has_vertical_movement(state)})
    fancy_add_exits(world, NORTHERN_STRETCH, [TALL_TALL_HEIGHTS, THE_OPEN_SEA],
                    {THE_OPEN_SEA: lambda state: logic.has_swimming(state),
                    TALL_TALL_HEIGHTS: lambda state: logic.has_vertical_movement(state)})
    fancy_add_exits(world, CASTLE_RAMPARTS, [TALL_TALL_HEIGHTS, CASTLE_SEQUOIA],
                    {TALL_TALL_HEIGHTS: lambda state: logic.has_vertical_movement(state),
                     CASTLE_SEQUOIA: lambda state: logic.has_vertical_movement(state) and logic.has_glide(state)})
    fancy_add_exits(world, THE_CHALICE_OF_TAR, [TALL_TALL_HEIGHTS, QUINTAR_RESERVE],
                    {TALL_TALL_HEIGHTS: lambda state: logic.has_glide(state),
                    QUINTAR_RESERVE: lambda state: logic.has_glide(state)})
    fancy_add_exits(world, FLYERS_CRAG, [OKIMOTO_NS, JIDAMBA_TANGLE],
                    {JIDAMBA_TANGLE: lambda state: logic.has_glide(state)})
    fancy_add_exits(world, JIDAMBA_TANGLE, [THE_OPEN_SEA, JIDAMBA_EACLANEYA],
                    {JIDAMBA_EACLANEYA: lambda state: (logic.has_glide(state) or logic.has_swimming(state)) and logic.has_jidamba_keys(state),
                    THE_OPEN_SEA: lambda state: logic.has_swimming(state)})
    fancy_add_exits(world, JIDAMBA_EACLANEYA, [JIDAMBA_TANGLE, THE_OPEN_SEA],
                    {THE_OPEN_SEA: lambda state: logic.has_swimming(state)})
    fancy_add_exits(world, THE_DEEP_SEA, [THE_OPEN_SEA, NEPTUNE_SHRINE, THE_DEPTHS, THE_SEQUOIA],
                    {THE_OPEN_SEA: lambda state: logic.has_swimming(state),
                    NEPTUNE_SHRINE: lambda state: logic.has_swimming(state),
                    THE_DEPTHS: lambda state: logic.has_swimming(state),
                    THE_SEQUOIA: lambda state: logic.has_golden_quintar(state)})
    fancy_add_exits(world, NEPTUNE_SHRINE, [THE_DEEP_SEA],
                    {THE_DEEP_SEA: lambda state: logic.has_swimming(state)})
    fancy_add_exits(world, JADE_CAVERN, [SOILED_DEN, DELENDE],
                    {SOILED_DEN: lambda state: logic.has_swimming(state),
                    DELENDE: lambda state: logic.has_swimming(state)})
    fancy_add_exits(world, CONTINENTAL_TRAM, [CAPITAL_PIPELINE, SARA_SARA_BAZAAR],
                    {SARA_SARA_BAZAAR: lambda state: logic.has_swimming(state) or state.has(TRAM_KEY, player)})
    fancy_add_exits(world, ANCIENT_LABYRINTH, [POKO_POKO_DESERT])
    fancy_add_exits(world, THE_SEQUOIA, [THE_DEEP_SEA])
    fancy_add_exits(world, THE_DEPTHS, [THE_DEEP_SEA])
    fancy_add_exits(world, CASTLE_SEQUOIA, [CAPITAL_SEQUOIA])
    # regions without connections don't get parsed by Jsonifier
    fancy_add_exits(world, THE_NEW_WORLD, [MENU])
    fancy_add_exits(world, THE_OLD_WORLD, [MENU])
    fancy_add_exits(world, MODDED_ZONE, [MENU])

def get_locations_per_region(locations: List[LocationData]) -> Dict[str, List[LocationData]]:
    per_region: Dict[str, List[LocationData]] = {}

    for location in locations:
        per_region.setdefault(location.region, []).append(location)

    return per_region

def create_region(world: "CrystalProjectWorld", player: int, locations_per_region: Dict[str, List[LocationData]], name: str, excluded: bool) -> Region:
    logic = CrystalProjectLogic(player, world.options)
    region = Region(name, player, world.multiworld)

    region_completion: Location | None = None

    #if the region isn't part of the multiworld, we still make the region so that all the exits still work,
        #but we also don't fill it with locations
    if not excluded:
        world.included_regions.append(region.name)
        if name in locations_per_region:
            for location_data in locations_per_region[name]:
                location = create_location(player, location_data, region)
                region.locations.append(location)
                if location_data.regionsanity:
                    region_completion = location

    # This is for the region completion location
    if world.options.regionsanity.value == world.options.regionsanity.option_true and region_completion is not None:
        for location in region.locations:
            if location != region_completion:
                region_completion.access_rule = combine_callables(region_completion.access_rule, location.access_rule)

    # This is for making sure players can earn money for required shop checks in shopsanity + regionsanity
    if world.options.regionsanity.value == world.options.regionsanity.option_true and world.options.shopsanity.value != world.options.shopsanity.option_disabled:
        for location in region.locations:
            if "Shop -" in location.name:
                location.access_rule = combine_callables(location.access_rule, lambda state: logic.can_earn_money(state, region.name))

    return region

def create_location(player: int, location_data: LocationData, region: Region) -> Location:
    location = CrystalProjectLocation(player, location_data.name, location_data.code, region)

    if location_data.rule:
        location.access_rule = location_data.rule

    return location

def combine_callables(callable1: Callable[[CollectionState], bool], callable2: Callable[[CollectionState], bool]) -> Callable[[CollectionState], bool]:
    return lambda state, a=callable1, b=callable2: a(state) and b(state)

def fancy_add_exits(self, region: str, exits: Union[Iterable[str], Dict[str, Optional[str]]],
                    rules: Dict[str, Callable[[CollectionState], bool]] | None = None):
    if rules is not None:
        for region_rule in rules:
            if not region_rule in exits:
                raise Exception(f"A rule was defined for the entrance {region} -> {region_rule} but {region_rule} isn't in the list of exits from {region}")

    for region_exit in exits:
        if rules is None:
            rules = {}
        if region_exit in rules:
            rules[region_exit] = combine_callables(rules[region_exit], rules_on_regions[region_exit])
        else:
            rules[region_exit] = rules_on_regions[region_exit]
    self.multiworld.get_region(region, self.player).add_exits(exits, rules)

def connect_menu_region(world: "CrystalProjectWorld", options: CrystalProjectOptions) -> None:
    logic = CrystalProjectLogic(world.player, options)

    fancy_add_exits(world, MENU, [SPAWNING_MEADOWS, CAPITAL_SEQUOIA, MERCURY_SHRINE, SALMON_RIVER, POKO_POKO_DESERT, GANYMEDE_SHRINE, DIONE_SHRINE, TALL_TALL_HEIGHTS, LANDS_END, JIDAMBA_TANGLE, NEPTUNE_SHRINE, THE_OLD_WORLD, THE_NEW_WORLD, MODDED_ZONE],
                    {CAPITAL_SEQUOIA: lambda state: state.has(GAEA_STONE, world.player),
                    MERCURY_SHRINE: lambda state: state.has(MERCURY_STONE, world.player),
                    SALMON_RIVER: lambda state: state.has(POSEIDON_STONE, world.player),
                    POKO_POKO_DESERT: lambda state: state.has(MARS_STONE, world.player),
                    GANYMEDE_SHRINE: lambda state: state.has(GANYMEDE_STONE, world.player),
                    DIONE_SHRINE: lambda state: state.has(DIONE_STONE, world.player),
                    TALL_TALL_HEIGHTS: lambda state: state.has(TRITON_STONE, world.player),
                    LANDS_END: lambda state: state.has(CALLISTO_STONE, world.player),
                    JIDAMBA_TANGLE: lambda state: state.has(EUROPA_STONE, world.player),
                    NEPTUNE_SHRINE: lambda state: state.has(NEPTUNE_STONE, world.player),
                    THE_OLD_WORLD: lambda state: logic.old_world_requirements(state),
                    THE_NEW_WORLD: lambda state: logic.new_world_requirements(state)})