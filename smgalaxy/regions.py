import imp
import typing
from .Options import EnablePurpleCoinStars, galaxy_options
from BaseClasses import Region, Location, Entrance, MultiWorld
from .locations import SMGLocation, location_table, locGE_table, locHH_table, \
                   locSJ_table, locBR_table, locBB_table, \
                   locGG_table, locFF_table, locDDune_table, locG_table, \
                   locGL_table, locSS_table, locTT_table, \
                   locDD_table, locDN_table, locMM_table, \
                   locbosses_table, locHL_table, locspecialstages_table, \
                   locPC_table

def create_regions(world: MultiWorld, player: int, self: int):
    #defines the special stages 
    regspecialstages = Region("Menu", player, world, "Ship")
    create_default_locs(regspecialstages, locspecialstages_table, player)
    if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_main_game_only:
       regspecialstages.locations.append(SMGLocation(player, "GG: Gateway's Purple coins", location_table["GG: Gateway's Purple coins"], regspecialstages))
    world.regions.append(regspecialstages) 
    # defines the hungry lumas region
    regHL = create_region("Hungry Lumas", player, world)
    create_default_locs(regHL, locHL_table, player)    
    world.regions.append(regHL)

    regPC = create_region("Purple Coins", player, world)
    create_default_locs(regPC, locPC_table, player)
    world.regions.append(regPC)
    
    # defines the bosses region
    regbosses = create_region("Bosses", player, world)
    create_default_locs(regbosses, locbosses_table, player)
    world.regions.append(regbosses)  
    # defines the good egg galaxy region
    regGE = create_region("Good Egg", player, world)
    create_default_locs(regGE, locGE_table, player)
    if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_all:
        regGE.locations.append(SMGLocation(player, "GE: Purple Coin Omelet", location_table["GE: Purple Coin Omelet"], regGE))
    world.regions.append(regGE)    
    # defines the honeyhive galaxey region
    regHH = create_region("Honeyhive", player, world)
    create_default_locs(regHH, locHH_table, player) 
    if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_all:
        regHH.locations.append(SMGLocation(player, "HH: The Honeyhive's Purple Coins", location_table["HH: The Honeyhive's Purple Coins"], regHH))
    world.regions.append(regHH)    
    # defines the Space Junk galaxy region
    regSJ = create_region("Space Junk", player, world)
    create_default_locs(regSJ, locSJ_table, player)
    if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_all:
        regHH.locations.append(SMGLocation(player, "SJ: Purple Coin Spacewalk", location_table["SJ: Purple Coin Spacewalk"], regSJ))
    world.regions.append(regSJ)  
    # defines the Battlerock galaxy
    regBR = create_region("Battlerock", player, world)
    create_default_locs(regBR, locBR_table, player)
    if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_all:
        regBR.locations.append(SMGLocation(player, "BR: Purple Coins on the Battlerock", location_table["BR: Purple Coins on the Battlerock"], regBR)) 
    world.regions.append(regBR)     
    # defines the Beach Bowl galaxy
    regBB = create_region("Beach Bowl", player, world)
    create_default_locs(regBB, locBB_table, player)
    if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_all:
        regBB.locations.append(SMGLocation(player, "BB: Beachcombing for Purple Coins", location_table["BB: Beachcombing for Purple Coins"], regBB))    
    world.regions.append(regBB)  
    # define Ghostly galaxy
    regG = create_region("Ghostly", player, world)
    create_default_locs(regG, locG_table, player)   
    if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_all:
        regG.locations.append(SMGLocation(player, "G: Purple Coins in the Bone Pen", location_table["G: Purple Coins in the Bone Pen"], regG))    
    world.regions.append(regG)  
    # defines the Gusty Gardens galaxy 
    regGG = create_region("Gusty Gardens", player, world)
    create_default_locs(regGG, locGG_table, player)
    if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_all:
        regGG.locations.append(SMGLocation(player, "GG: Purple Coins on the Puzzle Cube", location_table["GG: Purple Coins on the Puzzle Cube"], regGG))    
    world.regions.append(regGG)  
    # defines Freezeflame galaxy
    regFF = create_region("Freezeflame", player, world)
    create_default_locs(regFF, locFF_table, player)
    if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_all:
        regGG.locations.append(SMGLocation(player, "FF: Purple Coins on the Summit", location_table["FF: Purple Coins on the Summit"], regFF))  
    world.regions.append(regFF)  
    # defines DustyDune Galaxy
    regDDune = create_region("Dusty Dune", player, world)
    create_default_locs(regDDune, locDDune_table, player)
    if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_all:
        regDDune.locations.append(SMGLocation(player, "DDune: Purple Coin in the Desert", location_table["DDune: Purple Coin in the Desert"], regDDune))  
    world.regions.append(regDDune)  
    # defines golden leaf galaxy
    regGL = create_region("Gold Leaf", player, world)
    create_default_locs(regGL, locGL_table, player)
    if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_all:
        regGL.locations.append(SMGLocation(player, "GL: Purple Coins in the Woods", location_table["GL: Purple Coins in the Woods"], regGL)) 
    world.regions.append(regGL)  
    # defines the Sea slide galaxy
    regSS = create_region("Sea Slide", player, world)
    create_default_locs(regSS, locSS_table, player)
    if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_all:
        regSS.locations.append(SMGLocation(player, "SS: Purple Coins by the Seaside", location_table["SS: Purple Coins by the Seaside"], regSS)) 
    world.regions.append(regSS)
    # defines toy time galaxy 
    regTT = create_region("Toy Time", player, world)
    create_default_locs(regTT, locTT_table, player)
    if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_all:
        regSS.locations.append(SMGLocation(player, "TT: Luigi's Purple Coins", location_table["TT: Luigi's Purple Coins"], regSS)) 
    world.regions.append(regTT)  
    # defines deep dark galaxy
    regDD = create_region("Deep Dark", player, world)
    create_default_locs(regDD, locDD_table, player)
    if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_all:
        regDD.locations.append(SMGLocation(player, "DD: Plunder the Purple Coins", location_table["DD: Plunder the Purple Coins"], regDD)) 
    world.regions.append(regDD)  
    # defines Dreadnaught galaxy
    regDN = create_region("Dreadnaught", player, world)
    create_default_locs(regDN, locDN_table, player)
    if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_all:
        regDN.locations.append(SMGLocation(player, "DN: Battlestation's Purple Coins", location_table["DN: Battlestation's Purple Coins"], regDN)) 
    world.regions.append(regDN)  
    # defines Melty Molten galaxy
    regMM = create_region("Melty Molten", player, world)
    create_default_locs(regMM, locMM_table, player)
    if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_all:
        regMM.locations.append(SMGLocation(player, "MM: Red-Hot Purple Coins", location_table["MM: Red-Hot Purple Coins"], regMM)) 
    world.regions.append(regMM)  
    
    #defines the fountain
    regFountain = create_region("Fountain", player, world)
    world.regions.append(regFountain)
    #defines the kitchen
    regKitchen = create_region("Kitchen", player, world)
    world.regions.append(regKitchen)
    #defines the bedroom
    regBedroom = create_region("Bedroom", player, world)
    world.regions.append(regBedroom)
    #defines the Engine Room
    regEngineRoom = create_region("Engine Room", player, world)
    world.regions.append(regEngineRoom)
    #defines the garden
    regGarden = create_region("Garden", player, world)
    world.regions.append(regGarden)      

def connect_regions(world: MultiWorld, player: int, source: str, target: str, rule=None):
    sourceRegion = world.get_region(source, player)
    targetRegion = world.get_region(target, player)

    connection = Entrance(player, '', sourceRegion)
    if rule:
        connection.access_rule = rule

    sourceRegion.exits.append(connection)
    connection.connect(targetRegion)

def create_region(name: str, player: int, world: MultiWorld) -> Region:
    return Region(name, player, world, name, )

def create_default_locs(reg: Region, locs, player):
    reg_names = [name for name, id in locs.items()]
    reg.locations += [SMGLocation(player, loc_name, location_table[loc_name], reg) for loc_name in locs]

