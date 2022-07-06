import typing
from BaseClasses import MultiWorld, Region, Entrance, Location, RegionType
from .Locations import SMGLocation, location_table, locHH_table, locGE_table, \
locSJ_table, locBR_table, locBB_table, \
locGG_table, locFF_table, locDD_table, locDDune, \
locspecialstages_table, locbosses_table, \
locGL_table, locSS_table, locTT_table, \
locDN_table, locMM_table, locHL_table, \
smgcourses = ["Good Egg", "Honeyhive", "Loopdeeloop", "Flipswitch", "Bowser Jr. Robot Reactor", 
              "Space Junk", "Battlerock", "Rolling Green", "Hurry-Scurry", "Bowser's Star Reactor", 
              "Beach Bowl", "Ghostly", "Bubble Breeze", "Buoy Base", "Bowser Jr.'s Ariship Armada"
              "Gusty gardens", "Freezeflame", "Dusty Dune", "Honeyclimb", "Bowser's Dark Matter Planet",
              "Gold Leaf", "Sea Slide", "Toy Time", "Bonefin", "Bowser Jr.'s Lava Reactor",
              "Gateway", "Deep Dark", "Dreadnaught", "Melty Molton", "Matter Splatter"]
def create_regions(world MultiWorld, player int):
    regSS = Region("Menu", RegionType.Generic, "Comment Obserbatory", player, world)
    locspecialstages_names = [name for name, id in locSS_table.items()]
    locspecialstages_names += [name for name, id in locKey_table.items()]
    locspecialstages_names += [name for name, id in locCap_table.items()]
    regSS.locations += [SMGLocation(player, loc_name, location_table[loc_name], regspecialstages) for loc_name in locspecialstages_names]
    world.regions.append(regSS)
    regGE = Region("Good Egg", RegionType.Generic, "Good Egg", player, world)
    locGE_names = [name for name, id in locBoB_table.items()]
    regGE.locations += [SMGLocation(player, loc_name, location_table[loc_name], regGE) for loc_name in locGE_names]
    world.regions.append(regGE)