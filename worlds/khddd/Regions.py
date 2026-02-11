#Regions
from typing import Dict, List, NamedTuple, Optional
from BaseClasses import MultiWorld, Region, Entrance
from .Locations import KHDDDLocation, location_data_table, KHDDDLocationData, get_locations_by_region


class KHDDDRegionData(NamedTuple):
    locations: Optional[List[str]]
    region_exits: Optional[List[str]]

#Initialize data table
region_data_table: Dict[str, KHDDDRegionData] = {}

def set_region_table():
    global region_data_table
    region_data_table = {
        "World": KHDDDRegionData(None ,["Destiny Islands"]),
        "World Map [Sora]": KHDDDRegionData([], ["World Map [Riku]", "Traverse Town [Sora]", "La Cite des Cloches [Sora]", "The Grid [Sora]", "Prankster's Paradise [Sora]", "Country of the Musketeers [Sora]", "Symphony of Sorcery [Sora]", "The World That Never Was [Sora]", "Levels"]),
        "World Map [Riku]": KHDDDRegionData([], ["Traverse Town [Riku]", "La Cite des Cloches [Riku]", "The Grid [Riku]", "Prankster's Paradise [Riku]", "Country of the Musketeers [Riku]", "Symphony of Sorcery [Riku]", "The World That Never Was [Riku]"]),
        "Traverse Town [Sora]": KHDDDRegionData([],["Traverse Town 2 [Sora]"]),
        "Levels": KHDDDRegionData([], []),
        "La Cite des Cloches [Sora]": KHDDDRegionData([],[]),
        "The Grid [Sora]": KHDDDRegionData([],[]),
        "Prankster's Paradise [Sora]": KHDDDRegionData([],[]),
        "Country of the Musketeers [Sora]": KHDDDRegionData([],[]),
        "Symphony of Sorcery [Sora]": KHDDDRegionData([],[]),
        "The World That Never Was [Sora]": KHDDDRegionData([],[]),
        "Traverse Town 2 [Sora]": KHDDDRegionData([],[]),

        "Traverse Town [Riku]": KHDDDRegionData([],["Traverse Town 2 [Riku]"]),
        "La Cite des Cloches [Riku]": KHDDDRegionData([],[]),
        "The Grid [Riku]": KHDDDRegionData([],[]),
        "Prankster's Paradise [Riku]": KHDDDRegionData([],[]),
        "Country of the Musketeers [Riku]": KHDDDRegionData([],[]),
        "Symphony of Sorcery [Riku]": KHDDDRegionData([],[]),
        "The World That Never Was [Riku]": KHDDDRegionData([],[]),
        "Traverse Town 2 [Riku]": KHDDDRegionData([],[]),

        "Destiny Islands": KHDDDRegionData([],["World Map [Sora]"]),
}

def create_regions(multiworld: MultiWorld, player: int, options):
    #Attach locations to regions
    set_region_table() #Reset locations from prior DDD gens

    for name, data in location_data_table.items():

        # Skip DI locations
        if data.region == "Destiny Islands" and not options.play_destiny_islands or options.character > 1 and data.region == "Destiny Islands":
            continue

        # Skip character-specific locations
        if name.find("Superbosses") == -1:
            if options.character == 1 and name.find("Sora") == -1 or options.character == 2 and name.find("Riku") == -1:
                continue

        # Skip AVN is not needed
        if name.find("Ventus") > -1 and not options.armored_ventus_nightmare or options.goal == 1 and name.find("Ventus") > -1:
            continue

        # Skip Superbosses if not enabled
        if is_location_superboss(name):
            if not options.superbosses and options.goal == 0:
                continue

        # Skip the final superboss location if goal is not superbosses
        if name.find("All Superbosses Defeated") > -1 and options.goal == 0:
            continue

        # Skip YX if goal is not final boss
        if name.find("Young Xehanort Defeated") > -1 and options.goal == 1:
            continue

        #Skip Lord Kyroo if disabled
        if name.find("Lord Kyroo") > -1 and not options.lord_kyroo:
            continue

        if not name in region_data_table[data.region].locations:
            region_data_table[data.region].locations.append(name)

    #Set up the regions
    for name, data in region_data_table.items():
        multiworld.regions.append(create_region(multiworld, player, name, data, options))

    #Set up entrances
    multiworld.get_entrance("Traverse Town [Sora]", player).connect(multiworld.get_region("Traverse Town [Sora]", player))
    multiworld.get_entrance("Traverse Town 2 [Sora]", player).connect(multiworld.get_region("Traverse Town 2 [Sora]", player))
    multiworld.get_entrance("World Map [Sora]", player).connect(multiworld.get_region("World Map [Sora]", player))
    multiworld.get_entrance("La Cite des Cloches [Sora]", player).connect(multiworld.get_region("La Cite des Cloches [Sora]", player))
    multiworld.get_entrance("The Grid [Sora]", player).connect(multiworld.get_region("The Grid [Sora]", player))
    multiworld.get_entrance("Prankster's Paradise [Sora]", player).connect(multiworld.get_region("Prankster's Paradise [Sora]", player))
    multiworld.get_entrance("Country of the Musketeers [Sora]", player).connect(multiworld.get_region("Country of the Musketeers [Sora]", player))
    multiworld.get_entrance("Symphony of Sorcery [Sora]", player).connect(multiworld.get_region("Symphony of Sorcery [Sora]", player))
    multiworld.get_entrance("The World That Never Was [Sora]", player).connect(multiworld.get_region("The World That Never Was [Sora]", player))

    multiworld.get_entrance("Traverse Town [Riku]", player).connect(
        multiworld.get_region("Traverse Town [Riku]", player))
    multiworld.get_entrance("Traverse Town 2 [Riku]", player).connect(
        multiworld.get_region("Traverse Town 2 [Riku]", player))
    multiworld.get_entrance("World Map [Riku]", player).connect(multiworld.get_region("World Map [Riku]", player))
    multiworld.get_entrance("La Cite des Cloches [Riku]", player).connect(
        multiworld.get_region("La Cite des Cloches [Riku]", player))
    multiworld.get_entrance("The Grid [Riku]", player).connect(multiworld.get_region("The Grid [Riku]", player))
    multiworld.get_entrance("Prankster's Paradise [Riku]", player).connect(
        multiworld.get_region("Prankster's Paradise [Riku]", player))
    multiworld.get_entrance("Country of the Musketeers [Riku]", player).connect(
        multiworld.get_region("Country of the Musketeers [Riku]", player))
    multiworld.get_entrance("Symphony of Sorcery [Riku]", player).connect(
        multiworld.get_region("Symphony of Sorcery [Riku]", player))
    multiworld.get_entrance("The World That Never Was [Riku]", player).connect(
        multiworld.get_region("The World That Never Was [Riku]", player))

    multiworld.get_entrance("Destiny Islands", player).connect(multiworld.get_region("Destiny Islands", player))
    multiworld.get_entrance("Levels", player).connect(multiworld.get_region("Levels", player))

def create_region(multiworld: MultiWorld, player: int, name: str, data: KHDDDRegionData, options):
    region = Region(name, player, multiworld)
    if data.locations:
        for loc_name in data.locations:
            loc_data = location_data_table.get(loc_name)
            location = KHDDDLocation(player, loc_name, loc_data.code if loc_data else None, region)
            region.locations.append(location)


    if data.region_exits:
        for exit in data.region_exits:
            entrance = Entrance(player, exit, region)
            if not exit in region.exits:
                region.exits.append(entrance)

    return region

def is_location_superboss(locName):
    is_superboss = False

    if locName.find("Secret Portal") > -1 or locName.find("Ultima Weapon") > -1 or locName.find("Unbound") > -1:
        is_superboss = True

    return is_superboss
