import imp
import typing
from BaseClasses import MultiWorld, Region, Location, RegionType
from .locations import SMGLocation, location_table, locHH_table, locGE_table, \
locSJ_table, locBR_table, locBB_table, \
locGG_table, locFF_table, locDD_table, locDDune_table, \
locspecialstages_table, locbosses_table, \
locGL_table, locSS_table, locTT_table, \
locDN_table, locMM_table, locHL_table \

smgcourses = ["Good Egg", "Honeyhive", "Loopdeeloop", "Flipswitch", "Bowser Jr. Robot Reactor", 
              "Space Junk", "Battlerock", "Rolling Green", "Hurry-Scurry", "Bowser's Star Reactor", 
              "Beach Bowl", "Ghostly", "Bubble Breeze", "Buoy Base", "Bowser Jr.'s Ariship Armada",
              "Gusty gardens", "Freezeflame", "Dusty Dune", "Honeyclimb", "Bowser's Dark Matter Planet",
              "Gold Leaf", "Sea Slide", "Toy Time", "Bonefin", "Bowser Jr.'s Lava Reactor",
              "Gateway", "Deep Dark", "Dreadnaught", "Melty Molton", "Matter Splatter"]

def create_regions(world: MultiWorld, player: int):
    
    #defines the commet obserbatory
    regSS = Region("Menu", RegionType.Generic, "Comment Obserbatory", player, world)
    locSpecialstages_names = [name for name, id in locSS_table.items()]
    regSpecialstages.locations += [SMGLocation(player, loc_name, location_table[loc_name], regSpecialstages) for loc_name in locSpecialstages_names]
    world.regions.append(regspecialstages)
    # defines the good egg galaxy region
    regGE = Region("Good Egg", RegionType.Generic, "Good Egg", player, world)
    locGE_names = [name for name, id in locGE_table.items()]
    regGE.locations += [SMGLocation(player, loc_name, location_table[loc_name], regGE) for loc_name in locGE_names]
    world.regions.append(regGE)
    # defines the honeyhive galaxey region
    regHH = Region("Honeyhive", RegionType.Generic, "Honeyhive", player, world)
    locHH_names = [name for name, id in locHH_table.items()]
    regHH.locations += [SMGLocation(player, loc_name, location_table[loc_name], regHH) for loc_name in locHH_names]
    # defines the Space Junk galaxy region
    regSJ = Region("Space Junk", RegionType.Generic, "Space Junk", player, world)
    locSJ_names = [name for name, id in locSJ_table.items()]
    regSJ.locations += [SMGLocation(player, loc_name, location_table[loc_name], regSJ) for loc_name in locSJ_names]
    # defines the Battlerock galaxy
    regBR = Region("Battlerock", RegionType.Generic, "Battlerock", player, world)
    locBR_names = [name for name, id in locBR_table.items()]
    regBR.locations += [SMGLocation(player, loc_name, location_table[loc_name], regBR) for loc_name in locBR_names]
    # defines the Beach Bowl galaxy
    regBB = Region("Beach Bowl", RegionType.Generic, "Beach Bowl", player, world)
    locBB_names = [name for name, id in locBB_table.items()]
    regBB.locations += [SMGLocation(player, loc_name, location_table[loc_name], regBB) for loc_name in locBB_names]
    # define Ghostly galaxy
    regG = Region("Ghostly", RegionType.Generic, "Ghostly", player, world)
    locG_names = [name for name, id in locGG_table.items()]
    regG.locations += [SMGLocation(player, loc_name, location_table[loc_name], regG) for loc_name in locG_names]
    # defines the Gusty Gardens galaxy 
    regGG = Region("Gusty Gardens", RegionType.Generic, "Gusty Gardens", player, world)
    locGG_names = [name for name, id in locGG_table.items()]
    regGG.locations += [SMGLocation(player, loc_name, location_table[loc_name], regGG) for loc_name in locGG_names]
    # defines Freezeflame galaxy
    regFF = Region("Freezeflame", RegionType.Generic, "Freezeflame", player, world)
    locFF_names = [name for name, id in locFF_table.items()]
    regFF.locations += [SMGLocation(player, loc_name, location_table[loc_name], regFF) for loc_name in locFF_names]
    # defines golden leaf galaxy
    regGL = Region("Gold Leaf", RegionType.Generic, "Gold Leaf", player, world)
    locGL_names = [name for name, id in locGL_table.items()]
    regGL.locations += [SMGLocation(player, loc_name, location_table[loc_name], regGL) for loc_name in locGL_names]
    # defines toy time galaxy 
    regTT = Region ("Toy Time", RegionType.Generic, "Toy Time", player, world)
    locTT_names = [name for name, id in locTT_table.items()]
    regTT.locations += [SMGLocation(player, loc_name, location_table[loc_name], regTT) for loc_name in locTT_names]
    # defines deep dark galaxy
    regDD = Region("Deep Dark", RegionType.Generic, "Deep Dark", player, world)
    locDD_names = [name for name, id in locDD_table.items()]
    regDD.locations += [SMGLocation(player, loc_name, location_table[loc_name], regDD) for loc_name in locDD_names]
    # defines Dreadnought galaxy
    regDN = Region("Dreadnought", RegionType.Generic, "Dreadnought", player, world)
    locDN_names = [name for name, id in locDN_table.items()]
    regDN.locations += [SMGLocation (player, loc_name, location_table[loc_name], regDN) for loc_name in locDN_names]
    # defines Melty Molten galaxy
    regMM = Region("Melty Molten", RegionType.Generic, "Melty Molten", player, world)
    locMM_names = [name for name, id in locMM_table.items()]
    regMM.locations += [SMGLocation (player, loc_name, location_table[loc_name], regMM) for loc_name in locMM_names]
def connect_regions(world: MultiWorld, player: int, source: str, target: str, rule):
    sourceRegion = world.get_region(source, player)
    targetRegion = world.get_region(target, player)
