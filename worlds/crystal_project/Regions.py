from typing import List, Dict, TYPE_CHECKING
from BaseClasses import Region, Location, MultiWorld
from .Options import CrystalProjectOptions
from .Locations import LocationData
from .rules import CrystalProjectLogic

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
        create_region(world, player, locations_per_region, "Poko Poko Desert", excluded),
        create_region(world, player, locations_per_region, "Sara Sara Bazaar", excluded),
        create_region(world, player, locations_per_region, "Sara Sara Beach", excluded),
        create_region(world, player, locations_per_region, "Ancient Reservoir", excluded),
        create_region(world, player, locations_per_region, "Salmon Bay", excluded),
    ]

    if (options.includedRegions == options.includedRegions.option_expert or
        options.includedRegions == options.includedRegions.option_all):
        excluded = False
    else:
        excluded = True

    expert_regions = [
        create_region(world, player, locations_per_region, "The Open Sea", excluded),
        create_region(world, player, locations_per_region, "Shoudu Waterfront", excluded),
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
        create_region(world, player, locations_per_region, "Tall, Tall Heights", excluded),
        create_region(world, player, locations_per_region, "Northern Cave", excluded),
        create_region(world, player, locations_per_region, "Lands End", excluded),
        create_region(world, player, locations_per_region, "Slip Glide Ride", excluded),
        create_region(world, player, locations_per_region, "Sequoia Athenaeum", excluded),
        create_region(world, player, locations_per_region, "Northern Stretch", excluded),
        create_region(world, player, locations_per_region, "Castle Ramparts", excluded),
        create_region(world, player, locations_per_region, "The Chalice of Tar", excluded),
        create_region(world, player, locations_per_region, "Flyers Crag", excluded),
        create_region(world, player, locations_per_region, "Flyers Lookout", excluded),
        create_region(world, player, locations_per_region, "Jidamba Tangle", excluded),
        create_region(world, player, locations_per_region, "Jidamba Eaclaneya", excluded),
        create_region(world, player, locations_per_region, "The Deep Sea", excluded),
        create_region(world, player, locations_per_region, "Jade Cavern", excluded),
        create_region(world, player, locations_per_region, "Continental Tram", excluded),
    ]

    if (options.includedRegions == options.includedRegions.option_all):
        excluded = False
    else:
        excluded = True
     
    end_game_regions = [

    ]

    multiworld.regions += beginner_regions
    multiworld.regions += advanced_regions
    multiworld.regions += expert_regions
    multiworld.regions += end_game_regions

    connect_menu_region(world)

    multiworld.get_region("Spawning Meadows", player).add_exits(["Delende", "Continental Tram"],
        {"Continental Tram": logic.has_swimming}) #forwards
    multiworld.get_region("Delende", player).add_exits(["Soiled Den", "Pale Grotto", "Yamagawa M.A.", "Seaside Cliffs", "Mercury Shrine", "Jade Cavern"],
        {"Jade Cavern": logic.has_swimming}) #forwards; todo check jade cavern if correct
    #todo mercury shrine has no listed connections atm including a backwards
    multiworld.get_region("Delende", player).add_exits(["Spawning Meadows"]) #backwards
    multiworld.get_region("Soiled Den", player).add_exits(["Jade Cavern"],
        {"Jade Cavern": logic.has_swimming}) #forwards;
    multiworld.get_region("Soiled Den", player).add_exits(["Delende"]) #backwards
    multiworld.get_region("Pale Grotto", player).add_exits(["Proving Meadows"]) #forwards
    multiworld.get_region("Pale Grotto", player).add_exits(["Delende"]) #backwards
    multiworld.get_region("Seaside Cliffs", player).add_exits(["Draft Shaft Conduit", "Beaurior Volcano"],
        {"Beaurior Volcano": logic.has_vertical_movement}) #forwards
    multiworld.get_region("Seaside Cliffs", player).add_exits(["Delende"]) #backwards
    #no forwards for draft shaft conduit till we do fish stuff!
    multiworld.get_region("Draft Shaft Conduit", player).add_exits(["Seaside Cliffs"]) #backwards
    multiworld.get_region("Yamagawa M.A.", player).add_exits(["Lake Delende"]) #forwards
    multiworld.get_region("Yamagawa M.A.", player).add_exits(["Delende"]) #backwards
    multiworld.get_region("Proving Meadows", player).add_exits(["Skumparadise"], 
        {"Skumparadise": lambda state: logic.has_jobs(state, 3)}) #forwards
    multiworld.get_region("Proving Meadows", player).add_exits(["Pale Grotto"]) #backwards
    multiworld.get_region("Skumparadise", player).add_exits(["Capital Sequoia"]) #forwards
    multiworld.get_region("Skumparadise", player).add_exits(["Proving Meadows"]) #backwards
    multiworld.get_region("Capital Sequoia", player).add_exits(["Jojo Sewers", "Boomer Society", "Rolling Quintar Fields", "Cobblestone Crag", "Greenshire Reprise", "Castle Ramparts"],
        {"Cobblestone Crag": lambda state: state.has_any({"Item - Courtyard Key"}, world.player), 
        "Greenshire Reprise": lambda state: logic.has_jobs(state, 6),
        "Castle Ramparts": logic.has_vertical_movement}) #forwards; todo check requirements for Castle Ramparts
    multiworld.get_region("Capital Sequoia", player).add_exits(["Proving Meadows", "Skumparadise"]) #backwards
    # todo pretty sure there's a check in the quintar nest that you get to by going through the jojo sewers? not sure if there's another way to get to it without movement items - Eme
    multiworld.get_region("Jojo Sewers", player).add_exits(["Capital Jail"], 
        {"Capital Jail": logic.has_rental_quintar})
    #Boomer Society goes here
    multiworld.get_region("Rolling Quintar Fields", player).add_exits(["Quintar Nest", "Quintar Sanctum", "Castle Ramparts"], 
        {"Quintar Sanctum": logic.has_rental_quintar,
        "Castle Ramparts": logic.has_vertical_movement}) #todo check requirements for Castle Ramparts
    multiworld.get_region("Quintar Nest", player).add_exits(["Cobblestone Crag"])
    multiworld.get_region("Quintar Sanctum", player).add_exits(["Quintar Mausoleum"],
        {"Quintar Mausoleum": logic.has_swimming}) #backwards; Todo check this is correct
    multiworld.get_region("Capital Jail", player).add_exits(["Capital Pipeline"],
        {"Capital Pipeline": lambda state: state.has("Item - South Wing Key", world.player) and state.has("Item - Cell Key", world.player, 6)})
    multiworld.get_region("Capital Pipeline", player).add_exits(["Jidamba Tangle", "Continental Tram"],
        {"Jidamba Tangle": logic.has_vertical_movement,
        "Continental Tram": logic.has_vertical_movement})
    multiworld.get_region("Cobblestone Crag", player).add_exits(["Shoudu Waterfront", "Okimoto N.S."], 
        {"Shoudu Waterfront": logic.has_horizontal_movement, 
        "Okimoto N.S.": logic.has_horizontal_movement})
    multiworld.get_region("Okimoto N.S.", player).add_exits(["Flyers Crag"],
        {"Flyers Crag": logic.has_glide and logic.has_vertical_movement})
    multiworld.get_region("Greenshire Reprise", player).add_exits(["Salmon Pass", "Tall, Tall Heights"], 
        {"Salmon Pass": logic.has_rental_quintar,
        "Tall, Tall Heights": logic.has_vertical_movement})
    multiworld.get_region("Salmon Pass", player).add_exits(["Salmon River"], 
        {"Salmon River": logic.has_horizontal_movement})
    #Salmon River goes here
    multiworld.get_region("Poko Poko Desert", player).add_exits(["Sara Sara Bazaar", "Ancient Reservoir", "Salmon Bay"], 
        {"Ancient Reservoir": lambda state: state.has("Item - Pyramid Key", world.player),
        "Salmon Bay": logic.has_horizontal_movement and logic.has_vertical_movement})
    multiworld.get_region("Sara Sara Bazaar", player).add_exits(["Sara Sara Beach", "Shoudu Province", "The Open Sea", "Continental Tram"],
        {"Shoudu Province": lambda state: state.has("Item - Ferry Pass", world.player),
        "The Open Sea": logic.has_swimming,
        "Continental Tram": lambda state: logic.has_swimming or state.has("Item - Tram Key", player)})
    multiworld.get_region("Sara Sara Beach", player).add_exits(["Beaurior Volcano"],
        {"Beaurior Volcano": logic.has_vertical_movement})
    multiworld.get_region("Ancient Reservoir", player).add_exits(["Jade Cavern"],
        {"Jade Cavern": logic.has_swimming}) #forwards; todo check if correct
    #Salmon Bay goes here
    multiworld.get_region("The Open Sea", player).add_exits(["Jidamba Tangle", "The Deep Sea"],
        {"Jidamba Tangle": logic.has_swimming,
        "The Deep Sea": logic.has_swimming,})
    multiworld.get_region("Shoudu Waterfront", player).add_exits(["Shoudu Province"],
        {"Shoudu Province": logic.has_vertical_movement})
    multiworld.get_region("Shoudu Province", player).add_exits(["Sara Sara Bazaar", "Ganymede Shrine", "The Undercity", "Quintar Reserve", "Flyers Crag"],
        {"Sara Sara Bazaar": lambda state: state.has("Item - Ferry Pass", world.player),
        "Ganymede Shrine": logic.has_vertical_movement,
        "The Undercity": logic.has_vertical_movement and logic.has_horizontal_movement, #feels like it may not actually require horizontal, i tripped into it during the rando without quintar - eme
        "Quintar Reserve": lambda state: logic.has_vertical_movement and state.has("Item - Item - Elevator Part", world.player, 10),
        "Flyers Crag": logic.has_glide and logic.has_vertical_movement})
    #The Undercity goes here
    multiworld.get_region("Ganymede Shrine", player).add_exits(["Shoudu Province"])
    multiworld.get_region("Beaurior Volcano", player).add_exits(["Beaurior Rock"])
    #Beaurior Rock goes here
    #Lake Delende goes here
    multiworld.get_region("Quintar Reserve", player).add_exits(["Dione Shrine", "Quintar Mausoleum"],
        {"Quintar Mausoleum": logic.has_swimming})
    multiworld.get_region("Dione Shrine", player).add_exits(["Quintar Reserve", "Eastern Chasm", "Lands End", "Flyers Lookout"],
        {"Lands End": logic.has_glide,
        "The Chalice of Tar": lambda state: logic.has_glide and state.has("Item - Dione Stone", world.player),
        "Flyers Lookout": logic.has_glide and logic.has_vertical_movement})
    #Quintar Mausoleum goes here
    #Eastern Chasm goes here
    multiworld.get_region("Tall, Tall Heights", player).add_exits(["Eastern Chasm", "Northern Cave", "Lands End", "Sequoia Athenaeum", "Northern Stretch", "Castle Ramparts", "The Chalice of Tar"],
        {"Eastern Chasm": logic.has_vertical_movement,
        "Sequoia Athenaeum": lambda state: state.has("Item - Vermillion Book", world.player) and state.has("Item - Viridian Book", world.player) and state.has("Item - Cerulean Book", world.player),
        "Northern Stretch": logic.has_glide,
        "Castle Ramparts": logic.has_vertical_movement,
        #todo check requirements for Castle Ramparts
        "The Chalice of Tar": logic.has_glide and logic.has_vertical_movement})
    multiworld.get_region("Northern Cave", player).add_exits(["Slip Glide Ride"],
        {"Slip Glide Ride": logic.has_glide and logic.has_vertical_movement})
    multiworld.get_region("Lands End", player).add_exits(["Jidamba Tangle"],
        {"Jidamba Tangle": logic.has_glide})
    #Slip Glide Ride goes here
    #Sequoia Athenaeum goes here
    #Northern Stretch goes here
    #Castle Ramparts goes here
    #The Chalice of Tar goes here
    multiworld.get_region("Flyers Crag", player).add_exits(["Jidamba Tangle"],
        {"Jidamba Tangle": logic.has_glide}) #Todo check
    multiworld.get_region("Flyers Lookout", player).add_exits(["Jidamba Tangle"],
        {"Jidamba Tangle": logic.has_glide}) #Todo check
    multiworld.get_region("Jidamba Tangle", player).add_exits(["Jidamba Eaclaneya"],
        {"Jidamba Eaclaneya": lambda state: state.has("Item - Foliage Key", world.player) and state.has("Item - Cave Key", world.player) and state.has("Item - Canopy Key", world.player)})
    multiworld.get_region("Jidamba Eaclaneya", player).add_exits(["The Deep Sea"],
        {"The Deep Sea": logic.has_swimming}) #Todo check
    #The Deep Sea goes here
    #Jade Cavern goes here
    #Continental Tram goes here

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

def connect_menu_region(world: MultiWorld) -> None:
    starting_region_list = {
        0: "Spawning Meadows"
    }

    world.starting_region = starting_region_list[0]
    menu = world.multiworld.get_region("Menu", world.player)
    menu.add_exits(["Spawning Meadows", "Capital Sequoia", "Mercury Shrine", "Salmon River", "Poko Poko Desert", "Ganymede Shrine", "Dione Shrine", "Tall, Tall Heights", "Jidamba Tangle", "The Deep Sea"], 
        {"Capital Sequoia": lambda state: state.has_any({"Item - Gaea Stone"}, world.player),
        "Mercury Shrine": lambda state: state.has_any({"Item - Mercury Stone"}, world.player),
        "Salmon River": lambda state: state.has_any({"Item - Poseidon Stone"}, world.player),
        "Poko Poko Desert": lambda state: state.has_any({"Item - Mars Stone"}, world.player),
        "Ganymede Shrine": lambda state: state.has_any({"Item - Ganymede Stone"}, world.player),
        "Dione Shrine": lambda state: state.has_any({"Item - Dione Stone"}, world.player),
        "Tall, Tall Heights": lambda state: state.has_any({"Item - Triton Stone"}, world.player),
        "Jidamba Tangle": lambda state: state.has_any({"Item - Europa Stone"}, world.player),
        "The Deep Sea": lambda state: state.has_any({"Item - Neptune Stone"}, world.player),
        })