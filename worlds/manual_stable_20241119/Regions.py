from BaseClasses import Entrance, MultiWorld, Region
from .Helpers import is_category_enabled, is_location_enabled
from .Data import region_table
from .Locations import ManualLocation, location_name_to_location
from worlds.AutoWorld import World


if not region_table:
    region_table = {}

regionMap = { **region_table }
starting_regions = [ name for name in regionMap if "starting" in regionMap[name].keys() and regionMap[name]["starting"] ]

if len(starting_regions) == 0:
    starting_regions = region_table.keys() # the Manual region connects to all user-defined regions automatically if you specify no starting regions

regionMap["Manual"] = {
    "requires": [],
    "connects_to": starting_regions
}


def create_regions(world: World, multiworld: MultiWorld, player: int):
    # Create regions and assign locations to each region
    for region in regionMap:
        if "connects_to" not in regionMap[region]:
            exit_array = None
        else:
            exit_array = regionMap[region]["connects_to"] or None

        # safeguard for bad value at the end
        if not exit_array:
            exit_array = None

        locations = []
        for location in world.location_table:
            if "region" in location and location["region"] == region:
                if is_location_enabled(multiworld, player, location):
                    locations.append(location["name"])

        new_region = create_region(world, multiworld, player, region, locations, exit_array)
        multiworld.regions += [new_region]

    menu = create_region(world, multiworld, player, "Menu", None, ["Manual"])
    multiworld.regions += [menu]
    menuConn = multiworld.get_entrance("MenuToManual", player)
    menuConn.connect(multiworld.get_region("Manual", player))

    # Link regions together
    for region in regionMap:
        if "connects_to" in regionMap[region] and regionMap[region]["connects_to"]:
            for linkedRegion in regionMap[region]["connects_to"]:
                connection = multiworld.get_entrance(getConnectionName(region, linkedRegion), player)
                connection.connect(multiworld.get_region(linkedRegion, player))

def create_region(world: World, multiworld: MultiWorld, player: int, name: str, locations=None, exits=None):
    ret = Region(name, player, multiworld)

    if locations:
        for location in locations:
            loc_id = world.location_name_to_id.get(location, 0)
            locationObj = ManualLocation(player, location, loc_id, ret)
            if location_name_to_location[location].get('prehint'):
                world.options.start_location_hints.value.add(location)
            ret.locations.append(locationObj)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, getConnectionName(name, exit), ret))
    return ret

def getConnectionName(entranceName: str, exitName: str):
    return entranceName + "To" + exitName
