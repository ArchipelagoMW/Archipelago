from typing import NamedTuple, Optional
from BaseClasses import Region, Entrance, MultiWorld

from .Constants.Names import region_names as regname
from . import SMGWorld
from .Options import SMGOptions
from .locations import SMGLocation, location_table, locGE_table, locHH_table, \
                   locSJ_table, locBR_table, locBB_table, \
                   locGG_table, locFF_table, locDDune_table, locG_table, \
                   locGL_table, locSS_table, locTT_table, \
                   locDD_table, locDN_table, locMM_table, \
                   locbosses_table, locHL_table, locspecialstages_table, \
                   locPC_table

class SMGRegionData(NamedTuple):
    type: str  # type of randomization for GER
    entrance_regions: Optional[list[str]] # Regions with entrances to this one
    exit_regions: Optional[list[str]] # Regions with entrances from this one
    ger_exits: Optional[list[str]] # connected exit regions that can be swapped during Entrance Rando

class SMGRegion(Region):
    game: str = "Super Mario Galaxy"
    region_data: SMGRegionData

    def __init__(self, region_name: str, region_data: SMGRegionData, player: int, multiworld: MultiWorld):
        super().__init__(region_name, player, multiworld)
        self.region_data = region_data

region_list: dict[str, SMGRegionData] = {
    regname.SHIP: SMGRegionData("Hub", [],
                                [regname.TERRACE, regname.LIBRARY, regname.KITCHEN, regname.GARDEN,
                                 regname.ENGINE, regname.BEDROOM, regname.FOUNTAIN],
                                []),
    regname.TERRACE: SMGRegionData("Hub", [], [], []),
    regname.FOUNTAIN: SMGRegionData("Hub", [], [], []),
    regname.ENGINE: SMGRegionData("Hub", [], [], []),
    regname.KITCHEN: SMGRegionData("Hub", [], [], []),
    regname.BEDROOM: SMGRegionData("Hub",[], [], []),
    regname.GARDEN: SMGRegionData("Hub", [], [], []),
    regname.LIBRARY: SMGRegionData("Hub", [], [], []),

}


def create_regions(world: SMGWorld, player: int):
    for region_name in region_list.keys():
        world.multiworld.regions.append(SMGRegion(region_name, region_list[region_name], world.player, world.multiworld))
    #defines the special stages
    regspecialstages = Region("Ship", player, world.multiworld, "Ship")
    create_default_locs(regspecialstages, locspecialstages_table, player)
    if world.options.enable_purple_coin_stars == world.options.enable_purple_coin_stars.option_main_game_only:
       regspecialstages.locations.append(SMGLocation(player, "GG: Gateway's Purple coins", regspecialstages))
    world.multiworld.regions.append(regspecialstages)
    # defines the hungry lumas region
    regHL = create_region("Hungry Lumas", world)
    create_default_locs(regHL, locHL_table, player)    
    world.multiworld.regions.append(regHL)

    regPC = create_region("Purple Coins", world)
    create_default_locs(regPC, locPC_table, player)
    world.multiworld.regions.append(regPC)
    
    # defines the bosses region
    regbosses = create_region("Bosses", world)
    create_default_locs(regbosses, locbosses_table, player)
    world.multiworld.regions.append(regbosses)
    # defines the good egg galaxy region
    regGE = create_region("Good Egg", world)
    create_default_locs(regGE, locGE_table, player)
    if world.options.enable_purple_coin_stars == world.options.enable_purple_coin_stars.option_all:
        regGE.locations.append(SMGLocation(player, "GE: Purple Coin Omelet",  regGE))
    world.multiworld.regions.append(regGE)
    # defines the honeyhive galaxey region
    regHH = create_region("Honeyhive", world)
    create_default_locs(regHH, locHH_table, player) 
    if world.options.enable_purple_coin_stars == world.options.enable_purple_coin_stars.option_all:
        regHH.locations.append(SMGLocation(player, "HH: The Honeyhive's Purple Coins",  regHH))
    world.multiworld.regions.append(regHH)
    # defines the Space Junk galaxy region
    regSJ = create_region("Space Junk", world)
    create_default_locs(regSJ, locSJ_table, player)
    if world.options.enable_purple_coin_stars == world.options.enable_purple_coin_stars.option_all:
        regHH.locations.append(SMGLocation(player, "SJ: Purple Coin Spacewalk",  regSJ))
    world.multiworld.regions.append(regSJ)
    # defines the Battlerock galaxy
    regBR = create_region("Battlerock", world)
    create_default_locs(regBR, locBR_table, player)
    if world.options.enable_purple_coin_stars == world.options.enable_purple_coin_stars.option_all:
        regBR.locations.append(SMGLocation(player, "BR: Purple Coins on the Battlerock",  regBR))
    world.multiworld.regions.append(regBR)
    # defines the Beach Bowl galaxy
    regBB = create_region("Beach Bowl", world)
    create_default_locs(regBB, locBB_table, player)
    if world.options.enable_purple_coin_stars == world.options.enable_purple_coin_stars.option_all:
        regBB.locations.append(SMGLocation(player, "BB: Beachcombing for Purple Coins",  regBB))
    world.multiworld.regions.append(regBB)
    # define Ghostly galaxy
    regG = create_region("Ghostly", world)
    create_default_locs(regG, locG_table, player)   
    if world.options.enable_purple_coin_stars == world.options.enable_purple_coin_stars.option_all:
        regG.locations.append(SMGLocation(player, "G: Purple Coins in the Bone Pen",  regG))
    world.multiworld.regions.append(regG)
    # defines the Gusty Gardens galaxy 
    regGG = create_region("Gusty Gardens", world)
    create_default_locs(regGG, locGG_table, player)
    if world.options.enable_purple_coin_stars == world.options.enable_purple_coin_stars.option_all:
        regGG.locations.append(SMGLocation(player, "GG: Purple Coins on the Puzzle Cube",  regGG))
    world.multiworld.regions.append(regGG)
    # defines Freezeflame galaxy
    regFF = create_region("Freezeflame", world)
    create_default_locs(regFF, locFF_table, player)
    if world.options.enable_purple_coin_stars == world.options.enable_purple_coin_stars.option_all:
        regGG.locations.append(SMGLocation(player, "FF: Purple Coins on the Summit",  regFF))
    world.multiworld.regions.append(regFF)
    # defines DustyDune Galaxy
    regDDune = create_region("Dusty Dune", world)
    create_default_locs(regDDune, locDDune_table, player)
    if world.options.enable_purple_coin_stars == world.options.enable_purple_coin_stars.option_all:
        regDDune.locations.append(SMGLocation(player, "DDune: Purple Coin in the Desert",  regDDune))
    world.multiworld.regions.append(regDDune)
    # defines golden leaf galaxy
    regGL = create_region("Gold Leaf", world)
    create_default_locs(regGL, locGL_table, player)
    if world.options.enable_purple_coin_stars == world.options.enable_purple_coin_stars.option_all:
        regGL.locations.append(SMGLocation(player, "GL: Purple Coins in the Woods",  regGL))
    world.multiworld.regions.append(regGL)
    # defines the Sea slide galaxy
    regSS = create_region("Sea Slide", world)
    create_default_locs(regSS, locSS_table, player)
    if world.options.enable_purple_coin_stars == world.options.enable_purple_coin_stars.option_all:
        regSS.locations.append(SMGLocation(player, "SS: Purple Coins by the Seaside", regSS))
    world.multiworld.regions.append(regSS)
    # defines toy time galaxy 
    regTT = create_region("Toy Time", world)
    create_default_locs(regTT, locTT_table, player)
    if world.options.enable_purple_coin_stars == world.options.enable_purple_coin_stars.option_all:
        regSS.locations.append(SMGLocation(player, "TT: Luigi's Purple Coins", regSS))
    world.multiworld.regions.append(regTT)
    # defines deep dark galaxy
    regDD = create_region("Deep Dark", world)
    create_default_locs(regDD, locDD_table, player)
    if world.options.enable_purple_coin_stars == world.options.enable_purple_coin_stars.option_all:
        regDD.locations.append(SMGLocation(player, "DD: Plunder the Purple Coins", regDD))
    world.multiworld.regions.append(regDD)
    # defines Dreadnaught galaxy
    regDN = create_region("Dreadnaught", world)
    create_default_locs(regDN, locDN_table, player)
    if world.options.enable_purple_coin_stars == world.options.enable_purple_coin_stars.option_all:
        regDN.locations.append(SMGLocation(player, "DN: Battlestation's Purple Coins", regDN))
    world.multiworld.regions.append(regDN)
    # defines Melty Molten galaxy
    regMM = create_region("Melty Molten", world)
    create_default_locs(regMM, locMM_table, player)
    if world.options.enable_purple_coin_stars == world.options.enable_purple_coin_stars.option_all:
        regMM.locations.append(SMGLocation(player, "MM: Red-Hot Purple Coins", regMM))
    world.multiworld.regions.append(regMM)
    
    #defines the fountain
    regFountain = create_region("Fountain", world)
    world.multiworld.regions.append(regFountain)
    #defines the kitchen
    regKitchen = create_region("Kitchen", world)
    world.multiworld.regions.append(regKitchen)
    #defines the bedroom
    regBedroom = create_region("Bedroom", world)
    world.multiworld.regions.append(regBedroom)
    #defines the Engine Room
    regEngineRoom = create_region("Engine Room", world)
    world.multiworld.regions.append(regEngineRoom)
    #defines the garden
    regGarden = create_region("Garden", world)
    world.multiworld.regions.append(regGarden)

def connect_regions(world: SMGWorld, player: int, source: str, target: str, rule=None):
    sourceRegion = world.get_region(source)
    targetRegion = world.get_region(target)

    connection = Entrance(player, '', sourceRegion)
    if rule:
        connection.access_rule = rule

    sourceRegion.exits.append(connection)
    connection.connect(targetRegion)

def create_region(name: str, world: SMGWorld) -> Region:
    return Region(name, world.player, world.multiworld, name)

def create_default_locs(reg: Region, locs, player):
    reg_names = [name for name, id in locs.items()]
    reg.locations += [SMGLocation(player, loc_name, reg) for loc_name in locs]

