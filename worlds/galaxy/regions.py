import typing
from BaseClasses import MultiWorld, Region, Location
from .locations import SMGLocation, location_table, locHH_table, locGE_table, \
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
    
    # defines the good egg galaxy region
    regGE = Region("Good Egg", RegionType.Generic, "Good Egg", player, world)
    locGE_names = [name for name, id in locBoB_table.items()]
    regGE.locations += [SMGLocation(player, loc_name, location_table[loc_name], regGE) for loc_name in locGE_names]
    world.regions.append(regGE)
    # defines the honeyhive galaxey region
    reg = Region("Honeyhive", RegionType.Generic, "Honeyhive", player, world)
    locHH_names = [name for name, id in locHH_table.items()]
    regHH.locations += [SMGLocation(player, loc_name, location_table[loc_name], regHH) for loc_name in locHH_names]
    # defines the Space Junk galaxy region
    reg = Region("Space Junk", RegionType.Generic, "Space Junk", player, world)
    locSJ_names = [name for name, id in locSJ_table.items()]
    regSJ.locations += [SMGLocation(player, loc_name, location_table[loc_name,] regSJ) for loc_name in locSJ_names]
    # defines the Battlerock galaxy
    reg = Region("Battlerock", RegionType.Generic, "Battlerock", player, world)
    locBR_names = [name for name, id in locBR_table.items()]
    regBR.locations += [SMGLocation(player, loc_name, location_table[loc_name,] regBR) for loc_name in locSJ_names]



