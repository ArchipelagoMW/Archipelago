from BaseClasses import Region
from .Types import HexcellsInfiniteLocation
from .Locations import location_table, is_valid_location
from typing import TYPE_CHECKING

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
    lvlgroup1 = create_region_and_connect(world, "Level Group 1", "Menu -> Level Group 1", menu)
    lvlgroup2 = create_region_and_connect(world, "Level Group 2", "Level Group 1 -> Level Group 2", lvlgroup1)
    lvlgroup3 = create_region_and_connect(world, "Level Group 3", "Level Group 2 -> Level Group 3", lvlgroup2)
    lvlgroup4 = create_region_and_connect(world, "Level Group 4", "Level Group 3 -> Level Group 4", lvlgroup3)
    lvlgroup5 = create_region_and_connect(world, "Level Group 5", "Level Group 4 -> Level Group 5", lvlgroup4)
    lvlgroup6 = create_region_and_connect(world, "Level Group 6", "Level Group 5 -> Level Group 6", lvlgroup5)
    # greenhillzone = create_region_and_connect(world, "Green Hill Zone", "Menu -> Green Hill Zone", menu)
    # romania = create_region_and_connect(world, "Romania", "Menu -> Romania", menu)
    # sewer = create_region_and_connect(world, "The Sewer", "Menu -> The Sewer", menu)

    # # ---------------------------------- Green Hill Zone ----------------------------------
    # greenhillzone1 = create_region_and_connect(world, "Green Hill Zone - Act 1", "Green Hill Zone -> Green Hill Zone - Act 1", greenhillzone)
    # greenhillzone2 = create_region_and_connect(world, "Green Hill Zone - Act 2", "Green Hill Zone - Act 1 -> Green Hill Zone - Act 2", greenhillzone1)
    # create_region_and_connect(world, "Green Hill Zone - Act 3", "Green Hill Zone - Act 2 -> Green Hill Zone - Act 3", greenhillzone2)

    # # ---------------------------------- Romania ------------------------------------------
    # bucharest = create_region_and_connect(world, "Bucharest", "Romania -> Bucharest", romania)
    # sibiu = create_region_and_connect(world, "Sibiu", "Romania -> Sibiu", romania)
    # brașov = create_region_and_connect(world, "Brașov", "Romania -> Brașov", romania)
    # bucharest.connect(sibiu, "Bucharest -> Sibiu")
    # sibiu.connect(brașov, "Sibiu -> Brașov")
    # brașov.connect(bucharest, "Brașov, Bucharest")

    # # ---------------------------------- The Sewer ----------------------------------------
    # create_region_and_connect(world, "Big Hole in the Floor", "The Sewer -> Big Hole in the Floor", sewer)

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