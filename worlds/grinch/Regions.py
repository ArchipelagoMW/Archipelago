from BaseClasses import Region, MultiWorld
from .Locations import GrinchLocation, grinch_locations
from .Options import GrinchOptions
from . import GrinchWorld
from BaseClasses import Region

mainareas_list = [
    "Mount Crumpit",
    "Whoville",
    "Who Forest",
    "Who Dump",
    "Who Lake"
]

subareas_list = [
    "Post Office",
    "City Hall",
    "Countdown to X-Mas Tower",
    "Ski Resort",
    "Civic Center",
    "Minefield",
    "Power Plant",
    "Generator Building",
    "Submarine World",
    "Scout's Hut",
    "North Shore",
    "Mayor's Villa",
    "Sleigh Room"
]

supadow_list = [
    "Spin N' Win Supadow",
    "Dankamania Supadow",
    "The Copter Race Contest Supadow"
]

def create_regions(world: "GrinchWorld"):
    for mainarea in mainareas_list:
        #Each area in mainarea, create a region for the given player
        world.multiworld.regions.append(Region(mainarea, world.player, world.multiworld))
    for subarea in subareas_list:
        #Each area in subarea, create a region for the given player
        world.multiworld.regions.append(Region(subarea, world.player, world.multiworld))
    for supadow in supadow_list:
        #Each area in supadow, create a region for the given player
        world.multiworld.regions.append(Region(supadow, world.player, world.multiworld))

def grinchconnect(world: "GrinchWorld", current_region_name: str, connected_region_name: str):
    current_region = world.get_region(current_region_name)
    connected_region = world.get_region(connected_region_name)
    #Goes from current to connected
    current_region.connect(connected_region)
    #Goes from connected to current
    connected_region.connect(current_region)

def connect_regions(world: "GrinchWorld"):
    grinchconnect(world, "Mount Crumpit", "Whoville")
    grinchconnect(world, "Mount Crumpit", "Who Forest")
    grinchconnect(world, "Mount Crumpit", "Who Dump")
    grinchconnect(world, "Mount Crumpit", "Who Lake")
    grinchconnect(world, "Mount Crumpit", "Sleigh Room")
    grinchconnect(world, "Mount Crumpit", "Spin N' Win Supadow")
    grinchconnect(world, "Mount Crumpit", "Dankamania Supadow")
    grinchconnect(world, "Mount Crumpit", "The Copter Race Contest Supadow")
    grinchconnect(world, "Whoville", "Post Office")
    grinchconnect(world, "Whoville", "City Hall")
    grinchconnect(world, "Whoville", "Countdown to X-Mas Tower")
    grinchconnect(world, "Who Forest", "Ski Resort")
    grinchconnect(world, "Who Forest", "Civic Center")
    grinchconnect(world, "Who Dump", "Minefield")
    grinchconnect(world, "Who Dump", "Power Plant")
    grinchconnect(world, "Power Plant", "Generator Building")
    grinchconnect(world, "Who Lake", "Submarine World")
    grinchconnect(world, "Who Lake", "Scout's Hut")
    grinchconnect(world, "Who Lake", "North Shore")
    grinchconnect(world, "North Shore", "Mayor's Villa")
