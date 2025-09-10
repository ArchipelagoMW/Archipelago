from BaseClasses import Region
from .Types import HexcellsInfiniteLocation
from .Locations import location_table, is_valid_location
from typing import TYPE_CHECKING
from . import Options

if TYPE_CHECKING:
    from . import HexcellsInfiniteWorld

# This is where you will create your imaginary game world
# IE: connect rooms and areas together
# This is NOT where you'll add requirements for how to get to certain locations thats in Rules.py
# This is also long and tediouos
def create_regions(world: "HexcellsInfiniteWorld"):
    # The functions that are being used here will be located at the bottom to view
    # The important part is that if its not a dead end and connects to another place then name it
    # Otherwise you can just create the connection. Not that naming it is bad

    # You can technically name your connections whatever you want as well
    # You'll use those connection names in Rules.py
    menu = create_region(world, "Menu")
    
    # if(options.LevelUnlockType == Options.LevelUnlockType.option_vanilla):

    lvlgroup1 = create_region_and_connect(world, "Level Group 1", "Menu -> Level Group 1", menu)
    lvlgroup2 = create_region_and_connect(world, "Level Group 2", "Level Group 1 -> Level Group 2", lvlgroup1)
    lvlgroup3 = create_region_and_connect(world, "Level Group 3", "Level Group 2 -> Level Group 3", lvlgroup2)
    lvlgroup4 = create_region_and_connect(world, "Level Group 4", "Level Group 3 -> Level Group 4", lvlgroup3)
    lvlgroup5 = create_region_and_connect(world, "Level Group 5", "Level Group 4 -> Level Group 5", lvlgroup4)
    lvlgroup6 = create_region_and_connect(world, "Level Group 6", "Level Group 5 -> Level Group 6", lvlgroup5)

    # elif(options.LevelUnlockType == Options.LevelUnlockType.option_individual):
    #     lvl1 = create_region_and_connect(world, "1-1", "Menu -> 1-1", menu)
    #     lvl2 = create_region_and_connect(world, "1-2", "Menu -> 1-2", menu)
    #     lvl3 = create_region_and_connect(world, "1-3", "Menu -> 1-3", menu)
    #     lvl4 = create_region_and_connect(world, "1-4", "Menu -> 1-4", menu)
    #     lvl5 = create_region_and_connect(world, "1-5", "Menu -> 1-5", menu)
    #     lvl6 = create_region_and_connect(world, "1-6", "Menu -> 1-6", menu)

    #     lvl7 = create_region_and_connect(world, "2-1", "Menu -> 2-1", menu)
    #     lvl8 = create_region_and_connect(world, "2-2", "Menu -> 2-2", menu)
    #     lvl9 = create_region_and_connect(world, "2-3", "Menu -> 2-3", menu)
    #     lvl10 = create_region_and_connect(world, "2-4", "Menu -> 2-4", menu)
    #     lvl11 = create_region_and_connect(world, "2-5", "Menu -> 2-5", menu)
    #     lvl12 = create_region_and_connect(world, "2-6", "Menu -> 2-6", menu)
        
    #     lvl13 = create_region_and_connect(world, "3-1", "Menu -> 3-1", menu)
    #     lvl14 = create_region_and_connect(world, "3-2", "Menu -> 3-2", menu)
    #     lvl15 = create_region_and_connect(world, "3-3", "Menu -> 3-3", menu)
    #     lvl16 = create_region_and_connect(world, "3-4", "Menu -> 3-4", menu)
    #     lvl17 = create_region_and_connect(world, "3-5", "Menu -> 3-5", menu)
    #     lvl18 = create_region_and_connect(world, "3-6", "Menu -> 3-6", menu)

        # lvl19 = create_region_and_connect(world, "4-1", "Menu -> 4-1", menu)
        # lvl20 = create_region_and_connect(world, "4-2", "Menu -> 4-2", menu)
        # lvl21 = create_region_and_connect(world, "4-3", "Menu -> 4-3", menu)
        # lvl22 = create_region_and_connect(world, "4-4", "Menu -> 4-4", menu)
        # lvl23 = create_region_and_connect(world, "4-5", "Menu -> 4-5", menu)
        # lvl24 = create_region_and_connect(world, "4-6", "Menu -> 4-6", menu)

        # lvl25 = create_region_and_connect(world, "5-1", "Menu -> 5-1", menu)
        # lvl26 = create_region_and_connect(world, "5-2", "Menu -> 5-2", menu)
        # lvl27 = create_region_and_connect(world, "5-3", "Menu -> 5-3", menu)
        # lvl28 = create_region_and_connect(world, "5-4", "Menu -> 5-4", menu)
        # lvl29 = create_region_and_connect(world, "5-5", "Menu -> 5-5", menu)
        # lvl30 = create_region_and_connect(world, "5-6", "Menu -> 5-6", menu)

        # lvl31 = create_region_and_connect(world, "6-1", "Menu -> 6-1", menu)
        # lvl32 = create_region_and_connect(world, "6-2", "Menu -> 6-2", menu)
        # lvl33 = create_region_and_connect(world, "6-3", "Menu -> 6-3", menu)
        # lvl34 = create_region_and_connect(world, "6-4", "Menu -> 6-4", menu)
        # lvl35 = create_region_and_connect(world, "6-5", "Menu -> 6-5", menu)
        # lvl36 = create_region_and_connect(world, "6-6", "Menu -> 6-6", menu)


def create_region(world: "HexcellsInfiniteWorld", name: str) -> Region:
    reg = Region(name, world.player, world.multiworld)

    # When we create the region we go through all the locations we made and check if they are in that region
    # If they are and are valid, we attach it to the region
    for (key, data) in location_table.items():
        if data.region == name:
            if not is_valid_location(world, key):
                continue
            location = HexcellsInfiniteLocation(world.player, key, data.ap_code, reg)
            reg.locations.append(location)
    
    world.multiworld.regions.append(reg)
    return reg

# This runs the create region function while also connecting to another region
# Just simplifies process since you woill be connecting a lot of regions
def create_region_and_connect(world: "HexcellsInfiniteWorld",
                               name: str, entrancename: str, connected_region: Region) -> Region:
    reg: Region = create_region(world, name)
    connected_region.connect(reg, entrancename)
    return reg