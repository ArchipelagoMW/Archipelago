from typing import List, Dict, TYPE_CHECKING
from BaseClasses import Region, Location
from .options import CrystalProjectOptions
from .locations import LocationData
from .rules import CrystalProjectLogic
from .constants.keys import *
from .constants.key_items import *
from .constants.regions import *

if TYPE_CHECKING:
    from . import CrystalProjectWorld

class CrystalProjectLocation(Location):
    game: str = "CrystalProject"

    def __init__(self, player: int, name: str = " ", address: int = None, parent=None):
        super().__init__(player, name, address, parent)

def init_areas(world: "CrystalProjectWorld", locations: List[LocationData], options: CrystalProjectOptions) -> None:
    multiworld = world.multiworld
    player = world.player
    logic = CrystalProjectLogic(player, options)

    locations_per_region = get_locations_per_region(locations)

    if (options.includedRegions == options.includedRegions.option_beginner or
        options.includedRegions == options.includedRegions.option_advanced or
        options.includedRegions == options.includedRegions.option_expert or
        options.includedRegions == options.includedRegions.option_all):
        excluded = False
    else:
        excluded = True

    beginner_regions = [
        create_region(world, player, locations_per_region, MENU, excluded),
        create_region(world, player, locations_per_region, SPAWNING_MEADOWS, excluded),
        create_region(world, player, locations_per_region, DELENDE, excluded),
        create_region(world, player, locations_per_region, SOILED_DEN, excluded),
        create_region(world, player, locations_per_region, PALE_GROTTO, excluded),
        create_region(world, player, locations_per_region, SEASIDE_CLIFFS, excluded),
        create_region(world, player, locations_per_region, DRAFT_SHAFT_CONDUIT, excluded),
        create_region(world, player, locations_per_region, MERCURY_SHRINE, excluded),
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
        create_region(world, player, locations_per_region, SARA_SARA_BEACH, excluded),
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

    multiworld.regions += beginner_regions
    multiworld.regions += advanced_regions
    multiworld.regions += expert_regions
    multiworld.regions += end_game_regions

    connect_menu_region(world, options)

    multiworld.get_region(SPAWNING_MEADOWS, player).add_exits([DELENDE, MERCURY_SHRINE, POKO_POKO_DESERT, CONTINENTAL_TRAM, BEAURIOR_VOLCANO, YAMAGAWA_MA],
        {CONTINENTAL_TRAM: lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5),
        MERCURY_SHRINE: logic.has_vertical_movement,
        POKO_POKO_DESERT: lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 2),
        BEAURIOR_VOLCANO: lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 3),
        YAMAGAWA_MA: lambda state: (logic.has_swimming or logic.has_vertical_movement) and logic.is_area_in_level_range(state, 1)})
    multiworld.get_region(DELENDE, player).add_exits([SPAWNING_MEADOWS, SOILED_DEN, PALE_GROTTO, YAMAGAWA_MA, SEASIDE_CLIFFS, MERCURY_SHRINE, JADE_CAVERN, GREENSHIRE_REPRISE, SALMON_PASS, PROVING_MEADOWS],
        {JADE_CAVERN: lambda state: logic.has_golden_quintar and logic.is_area_in_level_range(state, 5),
        SALMON_PASS: lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 2),
        GREENSHIRE_REPRISE: lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 2),
        PROVING_MEADOWS: logic.has_horizontal_movement,
        YAMAGAWA_MA: lambda state: logic.is_area_in_level_range(state, 1)})
    multiworld.get_region(SOILED_DEN, player).add_exits([JADE_CAVERN, DELENDE, PALE_GROTTO, DRAFT_SHAFT_CONDUIT],
        {JADE_CAVERN: lambda state: logic.has_golden_quintar and logic.is_area_in_level_range(state, 5),
        PALE_GROTTO: logic.has_swimming,
        DRAFT_SHAFT_CONDUIT: logic.has_swimming})
    multiworld.get_region(PALE_GROTTO, player).add_exits([DELENDE, PROVING_MEADOWS, JOJO_SEWERS, TALL_TALL_HEIGHTS, SALMON_PASS],
        {JOJO_SEWERS: lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 1),
        TALL_TALL_HEIGHTS: lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 4),
        SALMON_PASS: logic.has_swimming})
    multiworld.get_region(SEASIDE_CLIFFS, player).add_exits([DELENDE, DRAFT_SHAFT_CONDUIT, THE_OPEN_SEA, MERCURY_SHRINE, BEAURIOR_VOLCANO],
        {BEAURIOR_VOLCANO: lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 3),
        THE_OPEN_SEA: lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5),
        MERCURY_SHRINE: logic.has_vertical_movement})
    multiworld.get_region(DRAFT_SHAFT_CONDUIT, player).add_exits([SEASIDE_CLIFFS, SOILED_DEN],
        {SOILED_DEN: logic.has_swimming})
    multiworld.get_region(MERCURY_SHRINE, player).add_exits([DELENDE, SEASIDE_CLIFFS, BEAURIOR_VOLCANO],
        {BEAURIOR_VOLCANO: lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 3)})
    multiworld.get_region(YAMAGAWA_MA, player).add_exits([SPAWNING_MEADOWS, DELENDE, LAKE_DELENDE],
        {LAKE_DELENDE: lambda state: logic.is_area_in_level_range(state, 3)})
    multiworld.get_region(PROVING_MEADOWS, player).add_exits([DELENDE, PALE_GROTTO, SKUMPARADISE, THE_OPEN_SEA], 
        {SKUMPARADISE: lambda state: logic.has_jobs(state, 3) and logic.is_area_in_level_range(state, 1),
        THE_OPEN_SEA: lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5)})
    multiworld.get_region(SKUMPARADISE, player).add_exits([PROVING_MEADOWS, CAPITAL_SEQUOIA],
        {PROVING_MEADOWS: lambda state: logic.has_jobs(state, 3)})
    multiworld.get_region(CAPITAL_SEQUOIA, player).add_exits([JOJO_SEWERS, ROLLING_QUINTAR_FIELDS, COBBLESTONE_CRAG, GREENSHIRE_REPRISE, CASTLE_SEQUOIA, SKUMPARADISE],
        {JOJO_SEWERS: lambda state: logic.is_area_in_level_range(state, 1),
        ROLLING_QUINTAR_FIELDS: lambda state: logic.is_area_in_level_range(state, 1),
        COBBLESTONE_CRAG: lambda state: logic.has_key(state, COURTYARD_KEY) or logic.has_rental_quintar or logic.has_horizontal_movement,
        GREENSHIRE_REPRISE: lambda state: logic.has_jobs(state, 5) and logic.is_area_in_level_range(state, 2),
        CASTLE_SEQUOIA: lambda state: logic.has_vertical_movement and logic.has_glide and logic.is_area_in_level_range(state, 5),
        SKUMPARADISE: lambda state: logic.is_area_in_level_range(state, 1)})
    multiworld.get_region(JOJO_SEWERS, player).add_exits([CAPITAL_SEQUOIA, BOOMER_SOCIETY, PALE_GROTTO, CAPITAL_JAIL, QUINTAR_NEST], 
        {CAPITAL_JAIL: lambda state: (logic.has_rental_quintar or logic.has_swimming) and logic.is_area_in_level_range(state, 2),
        PALE_GROTTO: logic.has_swimming,
        QUINTAR_NEST: lambda state: (logic.has_rental_quintar or logic.has_swimming) and logic.is_area_in_level_range(state, 1)})
    multiworld.get_region(BOOMER_SOCIETY, player).add_exits([JOJO_SEWERS, GREENSHIRE_REPRISE],
        {JOJO_SEWERS: lambda state: logic.is_area_in_level_range(state, 1),
        GREENSHIRE_REPRISE: lambda state: logic.is_area_in_level_range(state, 2)})
    multiworld.get_region(ROLLING_QUINTAR_FIELDS, player).add_exits([CAPITAL_SEQUOIA, QUINTAR_NEST, QUINTAR_SANCTUM, QUINTAR_RESERVE], 
        {QUINTAR_NEST: lambda state: logic.is_area_in_level_range(state, 1),
        QUINTAR_SANCTUM: lambda state: (logic.has_rental_quintar or logic.has_vertical_movement) and logic.is_area_in_level_range(state, 2),
        QUINTAR_RESERVE: lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 4)})
    multiworld.get_region(QUINTAR_NEST, player).add_exits([QUINTAR_SANCTUM, COBBLESTONE_CRAG, JOJO_SEWERS],
        {QUINTAR_SANCTUM: lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 2),
        JOJO_SEWERS: lambda state: logic.is_area_in_level_range(state, 1)})
    multiworld.get_region(QUINTAR_SANCTUM, player).add_exits([ROLLING_QUINTAR_FIELDS, QUINTAR_NEST, QUINTAR_MAUSOLEUM],
        {ROLLING_QUINTAR_FIELDS: lambda state: logic.is_area_in_level_range(state, 1),
        QUINTAR_MAUSOLEUM: lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5),
        QUINTAR_NEST: lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 1)})
    multiworld.get_region(CAPITAL_JAIL, player).add_exits([JOJO_SEWERS, CAPITAL_PIPELINE],
        {JOJO_SEWERS: lambda state: logic.is_area_in_level_range(state, 1) and logic.is_area_in_level_range(state, 1),
        CAPITAL_PIPELINE: lambda state: logic.has_key(state, SOUTH_WING_KEY) and logic.has_key(state, CELL_KEY, 6) and logic.is_area_in_level_range(state, 4)})
    multiworld.get_region(CAPITAL_PIPELINE, player).add_exits([CAPITAL_JAIL, JIDAMBA_TANGLE, CONTINENTAL_TRAM],
        {JIDAMBA_TANGLE: lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 5),
        CONTINENTAL_TRAM: logic.has_vertical_movement})
    multiworld.get_region(COBBLESTONE_CRAG, player).add_exits([CAPITAL_SEQUOIA, THE_OPEN_SEA, SHOUDU_WATERFRONT, OKIMOTO_NS], 
        {SHOUDU_WATERFRONT: logic.has_horizontal_movement,
        OKIMOTO_NS: lambda state: logic.has_horizontal_movement and logic.is_area_in_level_range(state, 2),
        THE_OPEN_SEA: lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5)})
    multiworld.get_region(OKIMOTO_NS, player).add_exits([COBBLESTONE_CRAG, THE_OPEN_SEA, FLYERS_CRAG],
        {THE_OPEN_SEA: logic.has_swimming,
        FLYERS_CRAG: (logic.has_glide and logic.has_vertical_movement) or logic.has_swimming})
    multiworld.get_region(GREENSHIRE_REPRISE, player).add_exits([CAPITAL_SEQUOIA, SALMON_PASS, TALL_TALL_HEIGHTS],
        # if we add hard logic, it is possible to jump from the rolling quintar fields onto the cap seq walls from the southeast and manage to bypass the guard and thus the job requirement
        {SALMON_PASS: lambda state: (logic.has_rental_quintar and logic.has_jobs(state, 5)) or logic.has_vertical_movement,
        TALL_TALL_HEIGHTS: lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 4)})
    multiworld.get_region(SALMON_PASS, player).add_exits([GREENSHIRE_REPRISE, SALMON_RIVER, DELENDE], 
        {GREENSHIRE_REPRISE: lambda state: (logic.has_horizontal_movement or logic.has_swimming) and logic.is_area_in_level_range(state, 2),
        SALMON_RIVER: lambda state: logic.has_horizontal_movement and logic.is_area_in_level_range(state, 2),
        DELENDE: logic.has_swimming})
    multiworld.get_region(SALMON_RIVER, player).add_exits([SALMON_BAY, TALL_TALL_HEIGHTS], 
        {SALMON_BAY: (logic.has_vertical_movement and logic.has_glide) or logic.has_swimming,
        TALL_TALL_HEIGHTS: lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 4)})
    multiworld.get_region(POKO_POKO_DESERT, player).add_exits([SARA_SARA_BAZAAR, ANCIENT_RESERVOIR, LAKE_DELENDE, SALMON_BAY, ANCIENT_LABYRINTH], 
        {ANCIENT_RESERVOIR: lambda state: logic.has_key(state, PYRAMID_KEY) and logic.is_area_in_level_range(state, 3),
        LAKE_DELENDE: lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 3),
        SALMON_BAY: logic.has_horizontal_movement and logic.has_vertical_movement,
        ANCIENT_LABYRINTH: lambda state: state.has(ANCIENT_TABLET_A, player) and logic.has_vertical_movement and logic.has_glide and logic.is_area_in_level_range(state, 5)})
    multiworld.get_region(SARA_SARA_BAZAAR, player).add_exits([POKO_POKO_DESERT, SARA_SARA_BEACH, SHOUDU_PROVINCE, THE_OPEN_SEA, CONTINENTAL_TRAM],
        {POKO_POKO_DESERT: lambda state: logic.is_area_in_level_range(state, 2),
        SARA_SARA_BEACH: lambda state: logic.has_horizontal_movement and logic.is_area_in_level_range(state, 3),
        SHOUDU_PROVINCE: lambda state: state.has(FERRY_PASS, world.player) and logic.is_area_in_level_range(state, 3),
        THE_OPEN_SEA: lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5),
        CONTINENTAL_TRAM: lambda state: logic.has_swimming or logic.has_key(state, TRAM_KEY)})
    multiworld.get_region(SARA_SARA_BEACH, player).add_exits([SARA_SARA_BAZAAR, THE_OPEN_SEA, BEAURIOR_VOLCANO, IBEK_CAVE],
        {IBEK_CAVE: lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 3),
        THE_OPEN_SEA: lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5),
        BEAURIOR_VOLCANO: lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 3)})
    multiworld.get_region(ANCIENT_RESERVOIR, player).add_exits([POKO_POKO_DESERT, IBEK_CAVE, SARA_SARA_BEACH, DELENDE],
        {DELENDE: logic.has_swimming,
        POKO_POKO_DESERT: lambda state: logic.is_area_in_level_range(state, 2),
        IBEK_CAVE: lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 3)})
    multiworld.get_region(IBEK_CAVE, player).add_exits([SARA_SARA_BEACH],
        {SARA_SARA_BEACH: lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 3)})
    multiworld.get_region(SALMON_BAY, player).add_exits([THE_OPEN_SEA, SALMON_RIVER],
        {THE_OPEN_SEA: lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5),
        SALMON_RIVER: lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 2)})
    multiworld.get_region(THE_OPEN_SEA, player).add_exits([SEASIDE_CLIFFS, PROVING_MEADOWS, OKIMOTO_NS, SHOUDU_WATERFRONT, SARA_SARA_BAZAAR, SARA_SARA_BEACH,SALMON_BAY, SHOUDU_PROVINCE, THE_UNDERCITY, BEAURIOR_VOLCANO, JIDAMBA_TANGLE, THE_DEEP_SEA],
        {SEASIDE_CLIFFS: logic.has_swimming,
        PROVING_MEADOWS: logic.has_swimming,
        OKIMOTO_NS: logic.has_swimming,
        SHOUDU_WATERFRONT: logic.has_swimming,
        THE_UNDERCITY: logic.has_swimming,
        SARA_SARA_BAZAAR: logic.has_swimming,
        SARA_SARA_BEACH: lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 3),
        SALMON_BAY: logic.has_swimming,
        SHOUDU_PROVINCE: lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 3),
        BEAURIOR_VOLCANO: lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 3),
        JIDAMBA_TANGLE: lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5),
        THE_DEEP_SEA: lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5)})
    multiworld.get_region(SHOUDU_WATERFRONT, player).add_exits([THE_OPEN_SEA, SHOUDU_PROVINCE, COBBLESTONE_CRAG],
        {THE_OPEN_SEA: logic.has_swimming,
        SHOUDU_PROVINCE: lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 3),
        COBBLESTONE_CRAG: logic.has_horizontal_movement})
    multiworld.get_region(SHOUDU_PROVINCE, player).add_exits([SARA_SARA_BAZAAR, SHOUDU_WATERFRONT, GANYMEDE_SHRINE, THE_UNDERCITY, QUINTAR_RESERVE],
        {SARA_SARA_BAZAAR: lambda state: state.has(FERRY_PASS, world.player),
        GANYMEDE_SHRINE: logic.has_vertical_movement,
        THE_UNDERCITY: lambda state: logic.has_vertical_movement and logic.has_horizontal_movement and logic.is_area_in_level_range(state, 3),
        QUINTAR_RESERVE: lambda state: logic.has_vertical_movement and state.has(ELEVATOR_PART, world.player, 10) and logic.is_area_in_level_range(state, 4)})
    multiworld.get_region(THE_UNDERCITY, player).add_exits([SHOUDU_PROVINCE, THE_OPEN_SEA],
        {SHOUDU_PROVINCE: lambda state: logic.is_area_in_level_range(state, 3),
        THE_OPEN_SEA: lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5)})
    multiworld.get_region(GANYMEDE_SHRINE, player).add_exits([SHOUDU_PROVINCE],
        {SHOUDU_PROVINCE: lambda state: logic.is_area_in_level_range(state, 3)})
    multiworld.get_region(BEAURIOR_VOLCANO, player).add_exits([SARA_SARA_BEACH, BEAURIOR_ROCK, THE_OPEN_SEA],
        {SARA_SARA_BEACH: lambda state: logic.is_area_in_level_range(state, 3),
        BEAURIOR_ROCK: lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 3),
        THE_OPEN_SEA: lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5)})
    multiworld.get_region(BEAURIOR_ROCK, player).add_exits([BEAURIOR_VOLCANO])
    multiworld.get_region(LAKE_DELENDE, player).add_exits([POKO_POKO_DESERT, DELENDE],
        {POKO_POKO_DESERT: lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 2),
        DELENDE: logic.has_vertical_movement})
    multiworld.get_region(QUINTAR_RESERVE, player).add_exits([SHOUDU_PROVINCE, DIONE_SHRINE, QUINTAR_MAUSOLEUM],
        {SHOUDU_PROVINCE: lambda state: logic.is_area_in_level_range(state, 3),
        QUINTAR_MAUSOLEUM: lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5)})
    multiworld.get_region(DIONE_SHRINE, player).add_exits([QUINTAR_RESERVE, EASTERN_CHASM, JIDAMBA_TANGLE, THE_CHALICE_OF_TAR],
        {JIDAMBA_TANGLE: lambda state: logic.has_glide and logic.is_area_in_level_range(state, 5),
        THE_CHALICE_OF_TAR: lambda state: logic.has_glide and state.has("Item - Dione Stone", world.player) and logic.is_area_in_level_range(state, 5),
        EASTERN_CHASM: logic.has_glide and logic.has_vertical_movement})
    multiworld.get_region(QUINTAR_MAUSOLEUM, player).add_exits([QUINTAR_RESERVE, QUINTAR_SANCTUM],
        {QUINTAR_RESERVE: lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 4),
        QUINTAR_SANCTUM: lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 2)})
    multiworld.get_region(EASTERN_CHASM, player).add_exits([QUINTAR_RESERVE, THE_OPEN_SEA],
        {QUINTAR_RESERVE: lambda state: logic.has_glide and logic.is_area_in_level_range(state, 4),
        THE_OPEN_SEA: lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5)})
    multiworld.get_region(TALL_TALL_HEIGHTS, player).add_exits([SALMON_RIVER, GREENSHIRE_REPRISE, LANDS_END, SEQUOIA_ATHENAEUM, NORTHERN_STRETCH, CASTLE_RAMPARTS, THE_CHALICE_OF_TAR, PALE_GROTTO, NORTHERN_CAVE],
        {LANDS_END: lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 4),
        SEQUOIA_ATHENAEUM: lambda state: state.has(VERMILLION_BOOK, world.player) and state.has(VIRIDIAN_BOOK, world.player) and state.has(CERULEAN_BOOK, world.player),
        NORTHERN_STRETCH: logic.has_glide,
        CASTLE_RAMPARTS: lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 4),
        PALE_GROTTO: logic.has_swimming,
        THE_CHALICE_OF_TAR: lambda state: logic.has_glide and logic.has_vertical_movement and logic.is_area_in_level_range(state, 5)})
    multiworld.get_region(NORTHERN_CAVE, player).add_exits([TALL_TALL_HEIGHTS, SLIP_GLIDE_RIDE],
        {SLIP_GLIDE_RIDE: logic.has_glide and logic.has_vertical_movement,
        TALL_TALL_HEIGHTS: lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 4)})
    multiworld.get_region(LANDS_END, player).add_exits([TALL_TALL_HEIGHTS, JIDAMBA_TANGLE],
        {JIDAMBA_TANGLE: lambda state: logic.has_glide and logic.is_area_in_level_range(state, 5),
        TALL_TALL_HEIGHTS: lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 4)})
    multiworld.get_region(SLIP_GLIDE_RIDE, player).add_exits([TALL_TALL_HEIGHTS, NORTHERN_CAVE],
        {NORTHERN_CAVE: lambda state: logic.has_glide and logic.is_area_in_level_range(state, 4),
        TALL_TALL_HEIGHTS: lambda state: logic.has_vertical_movement and logic.has_glide and logic.is_area_in_level_range(state, 4)})
    multiworld.get_region(SEQUOIA_ATHENAEUM, player).add_exits([TALL_TALL_HEIGHTS],
        {TALL_TALL_HEIGHTS: lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 4)})
    multiworld.get_region(NORTHERN_STRETCH, player).add_exits([TALL_TALL_HEIGHTS, THE_OPEN_SEA],
        {THE_OPEN_SEA: lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5),
        TALL_TALL_HEIGHTS: lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 4)})
    multiworld.get_region(CASTLE_RAMPARTS, player).add_exits([TALL_TALL_HEIGHTS],
        {TALL_TALL_HEIGHTS: lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 4)})
    multiworld.get_region(THE_CHALICE_OF_TAR, player).add_exits([TALL_TALL_HEIGHTS, QUINTAR_RESERVE],
        {TALL_TALL_HEIGHTS: lambda state: logic.has_glide and logic.is_area_in_level_range(state, 4),
        QUINTAR_RESERVE: lambda state: logic.has_glide and logic.is_area_in_level_range(state, 4)})
    multiworld.get_region(FLYERS_CRAG, player).add_exits([OKIMOTO_NS,JIDAMBA_TANGLE],
        {OKIMOTO_NS: lambda state: logic.is_area_in_level_range(state, 2),
        JIDAMBA_TANGLE: lambda state: logic.has_glide and logic.is_area_in_level_range(state, 5)})
    multiworld.get_region(JIDAMBA_TANGLE, player).add_exits([THE_OPEN_SEA, JIDAMBA_EACLANEYA],
        {JIDAMBA_EACLANEYA: lambda state: logic.has_jidamba_keys and logic.is_area_in_level_range(state, 5),
        THE_OPEN_SEA: lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5)})
    multiworld.get_region(JIDAMBA_EACLANEYA, player).add_exits([JIDAMBA_TANGLE, THE_OPEN_SEA],
        {THE_OPEN_SEA: lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5)})
    multiworld.get_region(THE_DEEP_SEA, player).add_exits([THE_OPEN_SEA, NEPTUNE_SHRINE, THE_DEPTHS, THE_SEQUOIA],
        {THE_OPEN_SEA: lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5),
         NEPTUNE_SHRINE: lambda state: logic.has_swimming,
        THE_DEPTHS: lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5),
        THE_SEQUOIA: lambda state: logic.has_golden_quintar and logic.is_area_in_level_range(state, 5)})
    multiworld.get_region(NEPTUNE_SHRINE, player).add_exits([THE_DEEP_SEA],
        {THE_DEEP_SEA: lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5)})
    multiworld.get_region(JADE_CAVERN, player).add_exits([SOILED_DEN, DELENDE],
        {SOILED_DEN: logic.has_swimming,
        DELENDE: logic.has_swimming})
    multiworld.get_region(CONTINENTAL_TRAM, player).add_exits([CAPITAL_PIPELINE, SARA_SARA_BAZAAR],
        {SARA_SARA_BAZAAR: lambda state: logic.has_swimming or state.has(TRAM_KEY, player)})
    multiworld.get_region(ANCIENT_LABYRINTH, player).add_exits([POKO_POKO_DESERT])
    multiworld.get_region(THE_SEQUOIA, player).add_exits([THE_DEEP_SEA])
    multiworld.get_region(THE_DEPTHS, player).add_exits([THE_DEEP_SEA])
    multiworld.get_region(CASTLE_SEQUOIA, player).add_exits([CAPITAL_SEQUOIA])
    # regions without connections don't get parsed by Jsonifier
    multiworld.get_region(THE_NEW_WORLD, player).add_exits([MENU])
    multiworld.get_region(THE_OLD_WORLD, player).add_exits([MENU])

def get_locations_per_region(locations: List[LocationData]) -> Dict[str, List[LocationData]]:
    per_region: Dict[str, List[LocationData]] = {}

    for location in locations:
        per_region.setdefault(location.region, []).append(location)

    return per_region

def create_region(world: "CrystalProjectWorld", player: int, locations_per_region: Dict[str, List[LocationData]], name: str, excluded: bool) -> Region:
    region = Region(name, player, world.multiworld)

    #if the region isn't part of the multiworld, we still make the region so that all the exits still work,
        #but we also don't fill it with locations
    if not excluded:
        world.included_regions.append(region.name)
        if name in locations_per_region:
            for location_data in locations_per_region[name]:
                location = create_location(player, location_data, region)
                region.locations.append(location)

    return region

def create_location(player: int, location_data: LocationData, region: Region) -> Location:
    location = CrystalProjectLocation(player, location_data.name, location_data.code, region)
    location.region = location_data.region

    if location_data.rule:
        location.access_rule = location_data.rule

    return location

def connect_menu_region(world: "CrystalProjectWorld", options: CrystalProjectOptions) -> None:
    starting_region_list = {
        0: MENU
    }

    logic = CrystalProjectLogic(world.player, options)
    world.starting_region = starting_region_list[0]
    menu = world.multiworld.get_region(MENU, world.player)
    menu.add_exits([SPAWNING_MEADOWS, CAPITAL_SEQUOIA, MERCURY_SHRINE, SALMON_RIVER, POKO_POKO_DESERT, GANYMEDE_SHRINE, DIONE_SHRINE, TALL_TALL_HEIGHTS, LANDS_END, JIDAMBA_TANGLE, NEPTUNE_SHRINE, THE_OLD_WORLD, THE_NEW_WORLD], 
        {CAPITAL_SEQUOIA: lambda state: state.has_any({"Item - Gaea Stone"}, world.player),
        MERCURY_SHRINE: lambda state: state.has_any({"Item - Mercury Stone"}, world.player),
        SALMON_RIVER: lambda state: state.has_any({"Item - Poseidon Stone"}, world.player),
        POKO_POKO_DESERT: lambda state: state.has_any({"Item - Mars Stone"}, world.player) and logic.is_area_in_level_range(state, 2),
        GANYMEDE_SHRINE: lambda state: state.has_any({"Item - Ganymede Stone"}, world.player),
        DIONE_SHRINE: lambda state: state.has_any({"Item - Dione Stone"}, world.player),
        TALL_TALL_HEIGHTS: lambda state: state.has_any({"Item - Triton Stone"}, world.player) and logic.is_area_in_level_range(state, 4),
        LANDS_END: lambda state: state.has_any({"Item - Callisto Stone"}, world.player) and logic.is_area_in_level_range(state, 4),
        JIDAMBA_TANGLE: lambda state: state.has_any({"Item - Europa Stone"}, world.player) and logic.is_area_in_level_range(state, 5),
        NEPTUNE_SHRINE: lambda state: state.has_any({"Item - Neptune Stone"}, world.player),
        THE_OLD_WORLD: logic.old_world_requirements,
        THE_NEW_WORLD: logic.new_world_requirements})