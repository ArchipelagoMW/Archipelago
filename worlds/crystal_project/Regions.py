from typing import List, Dict
from BaseClasses import Region, Location, MultiWorld
from .Options import CrystalProjectOptions
from .Locations import LocationData
from .rules import CrystalProjectLogic
from .Keys import *
from .KeyItems import *

class CrystalProjectLocation(Location):
    game: str = "CrystalProject"

    def __init__(self, player: int, name: str = " ", address: int = None, parent=None):
        super().__init__(player, name, address, parent)

def init_areas(world: MultiWorld, locations: List[LocationData], options: CrystalProjectOptions) -> None:
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
        create_region(world, player, locations_per_region, "Menu", excluded),
        create_region(world, player, locations_per_region, "Spawning Meadows", excluded),
        create_region(world, player, locations_per_region, "Delende", excluded),
        create_region(world, player, locations_per_region, "Soiled Den", excluded),
        create_region(world, player, locations_per_region, "Pale Grotto", excluded),
        create_region(world, player, locations_per_region, "Seaside Cliffs", excluded),
        create_region(world, player, locations_per_region, "Draft Shaft Conduit", excluded),
        create_region(world, player, locations_per_region, "Mercury Shrine", excluded),
        create_region(world, player, locations_per_region, "Yamagawa M.A.", excluded),
        create_region(world, player, locations_per_region, "Proving Meadows", excluded),
        create_region(world, player, locations_per_region, "Skumparadise", excluded),
    ]

    if (options.includedRegions == options.includedRegions.option_advanced or
        options.includedRegions == options.includedRegions.option_expert or
        options.includedRegions == options.includedRegions.option_all):
        excluded = False
    else:
        excluded = True

    advanced_regions = [
        create_region(world, player, locations_per_region, "Capital Sequoia", excluded),
        create_region(world, player, locations_per_region, "Jojo Sewers", excluded),
        create_region(world, player, locations_per_region, "Boomer Society", excluded),
        create_region(world, player, locations_per_region, "Rolling Quintar Fields", excluded),
        create_region(world, player, locations_per_region, "Quintar Nest", excluded),
        create_region(world, player, locations_per_region, "Quintar Sanctum", excluded),
        create_region(world, player, locations_per_region, "Capital Jail", excluded),
        create_region(world, player, locations_per_region, "Capital Pipeline", excluded),
        create_region(world, player, locations_per_region, "Cobblestone Crag", excluded),
        create_region(world, player, locations_per_region, "Okimoto N.S.", excluded),
        create_region(world, player, locations_per_region, "Greenshire Reprise", excluded),
        create_region(world, player, locations_per_region, "Salmon Pass", excluded),
        create_region(world, player, locations_per_region, "Salmon River", excluded),
        create_region(world, player, locations_per_region, "Shoudu Waterfront", excluded), #moved Shoudu Waterfront from Expert to Advanced
        create_region(world, player, locations_per_region, "Poko Poko Desert", excluded),
        create_region(world, player, locations_per_region, "Sara Sara Bazaar", excluded),
        create_region(world, player, locations_per_region, "Sara Sara Beach", excluded),
        create_region(world, player, locations_per_region, "Ancient Reservoir", excluded),
        create_region(world, player, locations_per_region, "Ibek Cave", excluded),
        create_region(world, player, locations_per_region, "Salmon Bay", excluded),
    ]

    if (options.includedRegions == options.includedRegions.option_expert or
        options.includedRegions == options.includedRegions.option_all):
        excluded = False
    else:
        excluded = True

    expert_regions = [
        create_region(world, player, locations_per_region, "The Open Sea", excluded),
        create_region(world, player, locations_per_region, "Shoudu Province", excluded),
        create_region(world, player, locations_per_region, "The Undercity", excluded),
        create_region(world, player, locations_per_region, "Ganymede Shrine", excluded),
        create_region(world, player, locations_per_region, "Beaurior Volcano", excluded),
        create_region(world, player, locations_per_region, "Beaurior Rock", excluded),
        create_region(world, player, locations_per_region, "Lake Delende", excluded),
        create_region(world, player, locations_per_region, "Quintar Reserve", excluded),
        create_region(world, player, locations_per_region, "Dione Shrine", excluded),
        create_region(world, player, locations_per_region, "Quintar Mausoleum", excluded),
        create_region(world, player, locations_per_region, "Eastern Chasm", excluded),
        create_region(world, player, locations_per_region, "Tall Tall Heights", excluded),
        create_region(world, player, locations_per_region, "Northern Cave", excluded),
        create_region(world, player, locations_per_region, "Lands End", excluded),
        create_region(world, player, locations_per_region, "Slip Glide Ride", excluded),
        create_region(world, player, locations_per_region, "Sequoia Athenaeum", excluded),
        create_region(world, player, locations_per_region, "Northern Stretch", excluded),
        create_region(world, player, locations_per_region, "Castle Ramparts", excluded),
        create_region(world, player, locations_per_region, "The Chalice of Tar", excluded),
        create_region(world, player, locations_per_region, "Flyers Crag", excluded),
        create_region(world, player, locations_per_region, "Jidamba Tangle", excluded),
        create_region(world, player, locations_per_region, "Jidamba Eaclaneya", excluded),
        create_region(world, player, locations_per_region, "The Deep Sea", excluded),
        create_region(world, player, locations_per_region, "Jade Cavern", excluded),
        create_region(world, player, locations_per_region, "Continental Tram", excluded),
    ]

    if options.includedRegions == options.includedRegions.option_all:
        excluded = False
    else:
        excluded = True
     
    end_game_regions = [
        create_region(world, player, locations_per_region, "Ancient Labyrinth", excluded),
        create_region(world, player, locations_per_region, "The Sequoia", excluded),
        create_region(world, player, locations_per_region, "The Depths", excluded),
        create_region(world, player, locations_per_region, "Castle Sequoia", excluded),
        create_region(world, player, locations_per_region, "The Old World", excluded),
        create_region(world, player, locations_per_region, "The New World", excluded),
    ]

    multiworld.regions += beginner_regions
    multiworld.regions += advanced_regions
    multiworld.regions += expert_regions
    multiworld.regions += end_game_regions

    connect_menu_region(world, options)

    multiworld.get_region("Spawning Meadows", player).add_exits(["Delende", "Mercury Shrine", "Poko Poko Desert", "Continental Tram", "Beaurior Volcano", "Yamagawa M.A."],
        {"Continental Tram": lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5),
        "Mercury Shrine": logic.has_vertical_movement,
        "Poko Poko Desert": lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 2),
        "Beaurior Volcano": lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 3),
        "Yamagawa M.A.": lambda state: (logic.has_swimming or logic.has_vertical_movement) and logic.is_area_in_level_range(state, 1)})
    multiworld.get_region("Delende", player).add_exits(["Spawning Meadows", "Soiled Den", "Pale Grotto", "Yamagawa M.A.", "Seaside Cliffs", "Mercury Shrine", "Jade Cavern", "Greenshire Reprise", "Salmon Pass", "Proving Meadows"],
        {"Jade Cavern": lambda state: logic.has_golden_quintar and logic.is_area_in_level_range(state, 5),
        "Salmon Pass": lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 2),
        "Greenshire Reprise": lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 2),
        "Proving Meadows": logic.has_horizontal_movement,
        "Yamagawa M.A.": lambda state: logic.is_area_in_level_range(state, 1)})
    multiworld.get_region("Soiled Den", player).add_exits(["Jade Cavern", "Delende", "Pale Grotto", "Draft Shaft Conduit"],
        {"Jade Cavern": lambda state: logic.has_golden_quintar and logic.is_area_in_level_range(state, 5),
        "Pale Grotto": logic.has_swimming,
        "Draft Shaft Conduit": logic.has_swimming})
    multiworld.get_region("Pale Grotto", player).add_exits(["Delende", "Proving Meadows", "Jojo Sewers", "Tall Tall Heights", "Salmon Pass"],
        {"Jojo Sewers": lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 1),
        "Tall Tall Heights": lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 4),
        "Salmon Pass": logic.has_swimming})
    multiworld.get_region("Seaside Cliffs", player).add_exits(["Delende", "Draft Shaft Conduit", "The Open Sea", "Mercury Shrine", "Beaurior Volcano"],
        {"Beaurior Volcano": lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 3),
        "The Open Sea": lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5),
        "Mercury Shrine": logic.has_vertical_movement})
    multiworld.get_region("Draft Shaft Conduit", player).add_exits(["Seaside Cliffs", "Soiled Den"],
        {"Soiled Den": logic.has_swimming})
    multiworld.get_region("Mercury Shrine", player).add_exits(["Delende", "Seaside Cliffs", "Beaurior Volcano"],
        {"Beaurior Volcano": lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 3)})
    multiworld.get_region("Yamagawa M.A.", player).add_exits(["Spawning Meadows", "Delende", "Lake Delende"],
        {"Lake Delende": lambda state: logic.is_area_in_level_range(state, 3)})
    multiworld.get_region("Proving Meadows", player).add_exits(["Delende", "Pale Grotto", "Skumparadise", "The Open Sea"], 
        {"Skumparadise": lambda state: logic.has_jobs(state, 3) and logic.is_area_in_level_range(state, 1),
        "The Open Sea": lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5)})
    multiworld.get_region("Skumparadise", player).add_exits(["Proving Meadows", "Capital Sequoia"],
        {"Proving Meadows": lambda state: logic.has_jobs(state, 3)})
    multiworld.get_region("Capital Sequoia", player).add_exits(["Jojo Sewers", "Rolling Quintar Fields", "Cobblestone Crag", "Greenshire Reprise", "Castle Sequoia", "Skumparadise"],
        {"Jojo Sewers": lambda state: logic.is_area_in_level_range(state, 1),
        "Rolling Quintar Fields": lambda state: logic.is_area_in_level_range(state, 1),
        "Cobblestone Crag": lambda state: logic.has_key(state, COURTYARD_KEY) or logic.has_rental_quintar or logic.has_horizontal_movement,
        "Greenshire Reprise": lambda state: logic.has_jobs(state, 5) and logic.is_area_in_level_range(state, 2),
        "Castle Sequoia": lambda state: logic.has_vertical_movement and logic.has_glide and logic.is_area_in_level_range(state, 5),
        "Skumparadise": lambda state: logic.is_area_in_level_range(state, 1)})
    multiworld.get_region("Jojo Sewers", player).add_exits(["Capital Sequoia", "Boomer Society", "Pale Grotto", "Capital Jail", "Quintar Nest"], 
        {"Capital Jail": lambda state: (logic.has_rental_quintar or logic.has_swimming) and logic.is_area_in_level_range(state, 2),
        "Pale Grotto": logic.has_swimming,
        "Quintar Nest": lambda state: (logic.has_rental_quintar or logic.has_swimming) and logic.is_area_in_level_range(state, 1)})
    multiworld.get_region("Boomer Society", player).add_exits(["Jojo Sewers", "Greenshire Reprise"],
        {"Jojo Sewers": lambda state: logic.is_area_in_level_range(state, 1),
        "Greenshire Reprise": lambda state: logic.is_area_in_level_range(state, 2)})
    multiworld.get_region("Rolling Quintar Fields", player).add_exits(["Capital Sequoia", "Quintar Nest", "Quintar Sanctum", "Quintar Reserve"], 
        {"Quintar Nest": lambda state: logic.is_area_in_level_range(state, 1),
        "Quintar Sanctum": lambda state: (logic.has_rental_quintar or logic.has_vertical_movement) and logic.is_area_in_level_range(state, 2),
        "Quintar Reserve": lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 4)})
    multiworld.get_region("Quintar Nest", player).add_exits(["Quintar Sanctum", "Cobblestone Crag", "Jojo Sewers"],
        {"Quintar Sanctum": lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 2),
        "Jojo Sewers": lambda state: logic.is_area_in_level_range(state, 1)})
    multiworld.get_region("Quintar Sanctum", player).add_exits(["Rolling Quintar Fields", "Quintar Nest", "Quintar Mausoleum"],
        {"Rolling Quintar Fields": lambda state: logic.is_area_in_level_range(state, 1),
        "Quintar Mausoleum": lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5),
        "Quintar Nest": lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 1)})
    multiworld.get_region("Capital Jail", player).add_exits(["Jojo Sewers", "Capital Pipeline"],
        {"Jojo Sewers": lambda state: logic.is_area_in_level_range(state, 1) and logic.is_area_in_level_range(state, 1),
        "Capital Pipeline": lambda state: logic.has_key(state, SOUTH_WING_KEY) and logic.has_key(state, CELL_KEY, 6) and logic.is_area_in_level_range(state, 4)})
    multiworld.get_region("Capital Pipeline", player).add_exits(["Capital Jail", "Jidamba Tangle", "Continental Tram"],
        {"Jidamba Tangle": lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 5),
        "Continental Tram": logic.has_vertical_movement})
    multiworld.get_region("Cobblestone Crag", player).add_exits(["Capital Sequoia", "The Open Sea", "Shoudu Waterfront", "Okimoto N.S."], 
        {"Shoudu Waterfront": logic.has_horizontal_movement,
        "Okimoto N.S.": lambda state: logic.has_horizontal_movement and logic.is_area_in_level_range(state, 2),
        "The Open Sea": lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5)})
    multiworld.get_region("Okimoto N.S.", player).add_exits(["Cobblestone Crag", "The Open Sea", "Flyers Crag"],
        {"The Open Sea": logic.has_swimming,
        "Flyers Crag": (logic.has_glide and logic.has_vertical_movement) or logic.has_swimming})
    multiworld.get_region("Greenshire Reprise", player).add_exits(["Capital Sequoia", "Salmon Pass", "Tall Tall Heights"],
        # if we add hard logic, it is possible to jump from the rolling quintar fields onto the cap seq walls from the southeast and manage to bypass the guard and thus the job requirement
        {"Salmon Pass": lambda state: (logic.has_rental_quintar and logic.has_jobs(state, 5)) or logic.has_vertical_movement,
        "Tall Tall Heights": lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 4)})
    multiworld.get_region("Salmon Pass", player).add_exits(["Greenshire Reprise", "Salmon River", "Delende"], 
        {"Greenshire Reprise": lambda state: (logic.has_horizontal_movement or logic.has_swimming) and logic.is_area_in_level_range(state, 2),
        "Salmon River": lambda state: logic.has_horizontal_movement and logic.is_area_in_level_range(state, 2),
        "Delende": logic.has_swimming})
    multiworld.get_region("Salmon River", player).add_exits(["Salmon Bay", "Tall Tall Heights"], 
        {"Salmon Bay": (logic.has_vertical_movement and logic.has_glide) or logic.has_swimming,
        "Tall Tall Heights": lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 4)})
    multiworld.get_region("Poko Poko Desert", player).add_exits(["Sara Sara Bazaar", "Ancient Reservoir", "Lake Delende", "Salmon Bay", "Ancient Labyrinth"], 
        {"Ancient Reservoir": lambda state: logic.has_key(state, PYRAMID_KEY) and logic.is_area_in_level_range(state, 3),
        "Lake Delende": lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 3),
        "Salmon Bay": logic.has_horizontal_movement and logic.has_vertical_movement,
        "Ancient Labyrinth": lambda state: state.has(ANCIENT_TABLET_A, player) and logic.has_vertical_movement and logic.has_glide and logic.is_area_in_level_range(state, 5)})
    multiworld.get_region("Sara Sara Bazaar", player).add_exits(["Poko Poko Desert", "Sara Sara Beach", "Shoudu Province", "The Open Sea", "Continental Tram"],
        {"Poko Poko Desert": lambda state: logic.is_area_in_level_range(state, 2),
        "Sara Sara Beach": lambda state: logic.has_horizontal_movement and logic.is_area_in_level_range(state, 3),
        "Shoudu Province": lambda state: state.has("Item - Ferry Pass", world.player) and logic.is_area_in_level_range(state, 3),
        "The Open Sea": lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5),
        "Continental Tram": lambda state: logic.has_swimming or logic.has_key(state, TRAM_KEY)})
    multiworld.get_region("Sara Sara Beach", player).add_exits(["Sara Sara Bazaar", "The Open Sea", "Beaurior Volcano", "Ibek Cave"],
        {"Ibek Cave": lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 3),
        "The Open Sea": lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5),
        "Beaurior Volcano": lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 3)})
    multiworld.get_region("Ancient Reservoir", player).add_exits(["Poko Poko Desert", "Ibek Cave", "Sara Sara Beach", "Delende"],
        {"Delende": logic.has_swimming,
        "Poko Poko Desert": lambda state: logic.is_area_in_level_range(state, 2),
        "Ibek Cave": lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 3)})
    multiworld.get_region("Ibek Cave", player).add_exits(["Sara Sara Beach"],
        {"Sara Sara Beach": lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 3)})
    multiworld.get_region("Salmon Bay", player).add_exits(["The Open Sea", "Salmon River"],
        {"The Open Sea": lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5),
        "Salmon River": lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 2)})
    multiworld.get_region("The Open Sea", player).add_exits(["Seaside Cliffs", "Proving Meadows", "Okimoto N.S.", "Shoudu Waterfront", "Sara Sara Bazaar", "Sara Sara Beach","Salmon Bay", "Shoudu Province", "The Undercity", "Beaurior Volcano", "Jidamba Tangle", "The Deep Sea"],
        {"Seaside Cliffs": logic.has_swimming,
        "Proving Meadows": logic.has_swimming,
        "Okimoto N.S.": logic.has_swimming,
        "Shoudu Waterfront": logic.has_swimming,
        "The Undercity": logic.has_swimming,
        "Sara Sara Bazaar": logic.has_swimming,
        "Sara Sara Beach": lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 3),
        "Salmon Bay": logic.has_swimming,
        "Shoudu Province": lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 3),
        "Beaurior Volcano": lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 3),
        "Jidamba Tangle": lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5),
        "The Deep Sea": lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5)})
    multiworld.get_region("Shoudu Waterfront", player).add_exits(["The Open Sea", "Shoudu Province", "Cobblestone Crag"],
        {"The Open Sea": logic.has_swimming,
        "Shoudu Province": lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 3),
        "Cobblestone Crag": logic.has_horizontal_movement})
    multiworld.get_region("Shoudu Province", player).add_exits(["Sara Sara Bazaar", "Shoudu Waterfront", "Ganymede Shrine", "The Undercity", "Quintar Reserve"],
        {"Sara Sara Bazaar": lambda state: state.has("Item - Ferry Pass", world.player),
        "Ganymede Shrine": logic.has_vertical_movement,
        "The Undercity": lambda state: logic.has_vertical_movement and logic.has_horizontal_movement and logic.is_area_in_level_range(state, 3),
        "Quintar Reserve": lambda state: logic.has_vertical_movement and state.has("Item - Elevator Part", world.player, 10) and logic.is_area_in_level_range(state, 4)})
    multiworld.get_region("The Undercity", player).add_exits(["Shoudu Province", "The Open Sea"],
        {"Shoudu Province": lambda state: logic.is_area_in_level_range(state, 3),
        "The Open Sea": lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5)})
    multiworld.get_region("Ganymede Shrine", player).add_exits(["Shoudu Province"],
        {"Shoudu Province": lambda state: logic.is_area_in_level_range(state, 3)})
    multiworld.get_region("Beaurior Volcano", player).add_exits(["Sara Sara Beach", "Beaurior Rock", "The Open Sea"],
        {"Sara Sara Beach": lambda state: logic.is_area_in_level_range(state, 3),
        "Beaurior Rock": lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 3),
        "The Open Sea": lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5)})
    multiworld.get_region("Beaurior Rock", player).add_exits(["Beaurior Volcano"])
    multiworld.get_region("Lake Delende", player).add_exits(["Poko Poko Desert", "Delende"],
        {"Poko Poko Desert": lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 2),
        "Delende": logic.has_vertical_movement})
    multiworld.get_region("Quintar Reserve", player).add_exits(["Shoudu Province", "Dione Shrine", "Quintar Mausoleum"],
        {"Shoudu Province": lambda state: logic.is_area_in_level_range(state, 3),
        "Quintar Mausoleum": lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5)})
    multiworld.get_region("Dione Shrine", player).add_exits(["Quintar Reserve", "Eastern Chasm", "Jidamba Tangle", "The Chalice of Tar"],
        {"Jidamba Tangle": lambda state: logic.has_glide and logic.is_area_in_level_range(state, 5),
        "The Chalice of Tar": lambda state: logic.has_glide and state.has("Item - Dione Stone", world.player) and logic.is_area_in_level_range(state, 5),
        "Eastern Chasm": logic.has_glide and logic.has_vertical_movement})
    multiworld.get_region("Quintar Mausoleum", player).add_exits(["Quintar Reserve", "Quintar Sanctum"],
        {"Quintar Reserve": lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 4),
        "Quintar Sanctum": lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 2)})
    multiworld.get_region("Eastern Chasm", player).add_exits(["Quintar Reserve", "The Open Sea"],
        {"Quintar Reserve": lambda state: logic.has_glide and logic.is_area_in_level_range(state, 4),
        "The Open Sea": lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5)})
    multiworld.get_region("Tall Tall Heights", player).add_exits(["Salmon River", "Greenshire Reprise", "Lands End", "Sequoia Athenaeum", "Northern Stretch", "Castle Ramparts", "The Chalice of Tar", "Pale Grotto", "Northern Cave"],
        {"Lands End": lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 4),
        "Sequoia Athenaeum": lambda state: state.has("Item - Vermillion Book", world.player) and state.has("Item - Viridian Book", world.player) and state.has("Item - Cerulean Book", world.player),
        "Northern Stretch": logic.has_glide,
        "Castle Ramparts": lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 4),
        "Pale Grotto": logic.has_swimming,
        "The Chalice of Tar": lambda state: logic.has_glide and logic.has_vertical_movement and logic.is_area_in_level_range(state, 5)})
    multiworld.get_region("Northern Cave", player).add_exits(["Tall Tall Heights", "Slip Glide Ride"],
        {"Slip Glide Ride": logic.has_glide and logic.has_vertical_movement,
        "Tall Tall Heights": lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 4)})
    multiworld.get_region("Lands End", player).add_exits(["Tall Tall Heights", "Jidamba Tangle"],
        {"Jidamba Tangle": lambda state: logic.has_glide and logic.is_area_in_level_range(state, 5),
        "Tall Tall Heights": lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 4)})
    multiworld.get_region("Slip Glide Ride", player).add_exits(["Tall Tall Heights", "Northern Cave"],
        {"Northern Cave": lambda state: logic.has_glide and logic.is_area_in_level_range(state, 4),
        "Tall Tall Heights": lambda state: logic.has_vertical_movement and logic.has_glide and logic.is_area_in_level_range(state, 4)})
    multiworld.get_region("Sequoia Athenaeum", player).add_exits(["Tall Tall Heights"],
        {"Tall Tall Heights": lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 4)})
    multiworld.get_region("Northern Stretch", player).add_exits(["Tall Tall Heights", "The Open Sea"],
        {"The Open Sea": lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5),
        "Tall Tall Heights": lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 4)})
    multiworld.get_region("Castle Ramparts", player).add_exits(["Tall Tall Heights"],
        {"Tall Tall Heights": lambda state: logic.has_vertical_movement and logic.is_area_in_level_range(state, 4)})
    multiworld.get_region("The Chalice of Tar", player).add_exits(["Tall Tall Heights", "Quintar Reserve"],
        {"Tall Tall Heights": lambda state: logic.has_glide and logic.is_area_in_level_range(state, 4),
        "Quintar Reserve": lambda state: logic.has_glide and logic.is_area_in_level_range(state, 4)})
    multiworld.get_region("Flyers Crag", player).add_exits(["Okimoto N.S.","Jidamba Tangle"],
        {"Okimoto N.S.": lambda state: logic.is_area_in_level_range(state, 2),
        "Jidamba Tangle": lambda state: logic.has_glide and logic.is_area_in_level_range(state, 5)})
    multiworld.get_region("Jidamba Tangle", player).add_exits(["The Open Sea", "Jidamba Eaclaneya"],
        {"Jidamba Eaclaneya": lambda state: logic.has_jidamba_keys and logic.is_area_in_level_range(state, 5),
        "The Open Sea": lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5)})
    multiworld.get_region("Jidamba Eaclaneya", player).add_exits(["Jidamba Tangle", "The Open Sea"],
        {"The Open Sea": lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5)})
    multiworld.get_region("The Deep Sea", player).add_exits(["The Open Sea", "The Depths", "The Sequoia"],
        {"The Open Sea": lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5),
        "The Depths": lambda state: logic.has_swimming and logic.is_area_in_level_range(state, 5),
        "The Sequoia": lambda state: logic.has_golden_quintar and logic.is_area_in_level_range(state, 5)})
    multiworld.get_region("Jade Cavern", player).add_exits(["Soiled Den", "Delende"],
        {"Soiled Den": logic.has_swimming,
        "Delende": logic.has_swimming})
    multiworld.get_region("Continental Tram", player).add_exits(["Capital Pipeline", "Sara Sara Bazaar"],
        {"Sara Sara Bazaar": lambda state: logic.has_swimming or state.has("Item - Tram Key", player)})
    multiworld.get_region("Ancient Labyrinth", player).add_exits(["Poko Poko Desert"])
    multiworld.get_region("The Sequoia", player).add_exits(["The Deep Sea"])
    multiworld.get_region("The Depths", player).add_exits(["The Deep Sea"])
    multiworld.get_region("Castle Sequoia", player).add_exits(["Capital Sequoia"])
    # regions without connections don't get parsed by Jsonifier
    multiworld.get_region("The New World", player).add_exits(["Menu"])
    multiworld.get_region("The Old World", player).add_exits(["Menu"])

def get_locations_per_region(locations: List[LocationData]) -> Dict[str, List[LocationData]]:
    per_region: Dict[str, List[LocationData]] = {}

    for location in locations:
        per_region.setdefault(location.region, []).append(location)

    return per_region

def create_region(world: MultiWorld, player: int, locations_per_region: Dict[str, List[LocationData]], name: str, excluded: bool) -> Region:
    region = Region(name, player, world.multiworld)

    #if the region isn't part of the multiworld, we still make the region so that all the exits still work,
        #but we also don't fill it with locations
    if not excluded: 
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

def connect_menu_region(world: MultiWorld, options: CrystalProjectOptions) -> None:
    starting_region_list = {
        0: "Spawning Meadows"
    }

    logic = CrystalProjectLogic(world.player, options)
    world.starting_region = starting_region_list[0]
    menu = world.multiworld.get_region("Menu", world.player)
    menu.add_exits(["Spawning Meadows", "Capital Sequoia", "Mercury Shrine", "Salmon River", "Poko Poko Desert", "Ganymede Shrine", "Dione Shrine", "Tall Tall Heights", "Lands End", "Jidamba Tangle", "The Deep Sea", "The Old World", "The New World"], 
        {"Capital Sequoia": lambda state: state.has_any({"Item - Gaea Stone"}, world.player),
        "Mercury Shrine": lambda state: state.has_any({"Item - Mercury Stone"}, world.player),
        "Salmon River": lambda state: state.has_any({"Item - Poseidon Stone"}, world.player),
        "Poko Poko Desert": lambda state: state.has_any({"Item - Mars Stone"}, world.player) and logic.is_area_in_level_range(state, 2),
        "Ganymede Shrine": lambda state: state.has_any({"Item - Ganymede Stone"}, world.player),
        "Dione Shrine": lambda state: state.has_any({"Item - Dione Stone"}, world.player),
        "Tall Tall Heights": lambda state: state.has_any({"Item - Triton Stone"}, world.player) and logic.is_area_in_level_range(state, 4),
        "Lands End": lambda state: state.has_any({"Item - Callisto Stone"}, world.player) and logic.is_area_in_level_range(state, 4),
        "Jidamba Tangle": lambda state: state.has_any({"Item - Europa Stone"}, world.player) and logic.is_area_in_level_range(state, 5),
        "The Deep Sea": lambda state: state.has_any({"Item - Neptune Stone"}, world.player) and logic.has_swimming and logic.is_area_in_level_range(state, 5),
        "The Old World": lambda state: state.has_any({"Item - Old World Stone"}, world.player) and logic.is_area_in_level_range(state, 5),
        "The New World": logic.new_world_requirements})