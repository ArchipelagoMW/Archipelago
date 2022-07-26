import typing
from BaseClasses import MultiWorld, Region, Entrance, Location
from .Locations import SM64Location, location_table, locBoB_table, locWhomp_table, locJRB_table, locCCM_table, \
    locBBH_table, \
    locHMC_table, locLLL_table, locSSL_table, locDDD_table, locSL_table, \
    locWDW_table, locTTM_table, locTHI_table, locTTC_table, locRR_table, \
    locPSS_table, locSA_table, locBitDW_table, locTotWC_table, locCotMC_table, \
    locVCutM_table, locBitFS_table, locWMotR_table, locBitS_table, locSS_table

# List of all courses, including secrets, without BitS as that one is static
sm64courses = ["Bob-omb Battlefield", "Whomp's Fortress", "Jolly Roger Bay", "Cool, Cool Mountain", "Big Boo's Haunt",
               "Hazy Maze Cave", "Lethal Lava Land", "Shifting Sand Land", "Dire, Dire Docks", "Snowman's Land",
               "Wet-Dry World", "Tall, Tall Mountain", "Tiny-Huge Island", "Tick Tock Clock", "Rainbow Ride",
               "The Princess's Secret Slide", "The Secret Aquarium", "Bowser in the Dark World", "Tower of the Wing Cap",
               "Cavern of the Metal Cap", "Vanish Cap under the Moat", "Bowser in the Fire Sea", "Wing Mario over the Rainbow"]

# sm64paintings is list of entrances, format LEVEL | AREA. String Reference below
sm64paintings   = [91,241,121,51,41,71,221,81,231,101,111,361,132,131,141,151]
sm64paintings_s = ["BOB", "WF", "JRB", "CCM", "BBH", "HMC", "LLL", "SSL", "DDD", "SL", "WDW", "TTM", "THI Tiny", "THI Huge", "TTC", "RR"]
# sm64secrets is list of secret areas
sm64secrets = [271, 201, 171, 291, 281, 181, 191, 311]
sm64secrets_s = ["PSS", "SA", "BitDW", "TOTWC", "COTMC", "VCUTM", "BitFS", "WMOTR"]

sm64entrances = sm64paintings + sm64secrets
sm64entrances_s = sm64paintings_s + sm64secrets_s
sm64_internalloc_to_string = dict(zip(sm64paintings+sm64secrets, sm64entrances_s))
sm64_internalloc_to_regionid = dict(zip(sm64paintings+sm64secrets, list(range(13)) + [12,13,14] + list(range(15,15+len(sm64secrets)))))

def create_regions(world: MultiWorld, player: int):
    regSS = Region("Menu", player, world, "Castle Area")
    create_default_locs(regSS, locSS_table, player)
    world.regions.append(regSS)

    regBoB = create_region("Bob-omb Battlefield", player, world)
    create_default_locs(regBoB, locBoB_table, player)
    if (world.EnableCoinStars[player].value):
        regBoB.locations.append(SM64Location(player, "BoB: 100 Coins", location_table["BoB: 100 Coins"], regBoB))
    world.regions.append(regBoB)

    regWhomp = create_region("Whomp's Fortress", player, world)
    create_default_locs(regWhomp, locWhomp_table, player)
    if (world.EnableCoinStars[player].value):
        regWhomp.locations.append(SM64Location(player, "WF: 100 Coins", location_table["WF: 100 Coins"], regWhomp))
    world.regions.append(regWhomp)

    regJRB = create_region("Jolly Roger Bay", player, world)
    create_default_locs(regJRB, locJRB_table, player)
    if (world.EnableCoinStars[player].value):
        regJRB.locations.append(SM64Location(player, "JRB: 100 Coins", location_table["JRB: 100 Coins"], regJRB))
    world.regions.append(regJRB)

    regCCM = create_region("Cool, Cool Mountain", player, world)
    create_default_locs(regCCM, locCCM_table, player)
    if (world.EnableCoinStars[player].value):
        regCCM.locations.append(SM64Location(player, "CCM: 100 Coins", location_table["CCM: 100 Coins"], regCCM))
    world.regions.append(regCCM)

    regBBH = create_region("Big Boo's Haunt", player, world)
    create_default_locs(regBBH, locBBH_table, player)
    if (world.EnableCoinStars[player].value):
        regBBH.locations.append(SM64Location(player, "BBH: 100 Coins", location_table["BBH: 100 Coins"], regBBH))
    world.regions.append(regBBH)

    regPSS = create_region("The Princess's Secret Slide", player, world)
    create_default_locs(regPSS, locPSS_table, player)
    world.regions.append(regPSS)

    regSA = create_region("The Secret Aquarium", player, world)
    create_default_locs(regSA, locSA_table, player)
    world.regions.append(regSA)

    regTotWC = create_region("Tower of the Wing Cap", player, world)
    create_default_locs(regTotWC, locTotWC_table, player)
    world.regions.append(regTotWC)

    regBitDW = create_region("Bowser in the Dark World", player, world)
    create_default_locs(regBitDW, locBitDW_table, player)
    world.regions.append(regBitDW)

    regBasement = create_region("Basement", player, world)
    world.regions.append(regBasement)

    regHMC = create_region("Hazy Maze Cave", player, world)
    create_default_locs(regHMC, locHMC_table, player)
    if (world.EnableCoinStars[player].value):
        regHMC.locations.append(SM64Location(player, "HMC: 100 Coins", location_table["HMC: 100 Coins"], regHMC))
    world.regions.append(regHMC)

    regLLL = create_region("Lethal Lava Land", player, world)
    create_default_locs(regLLL, locLLL_table, player)
    if (world.EnableCoinStars[player].value):
        regLLL.locations.append(SM64Location(player, "LLL: 100 Coins", location_table["LLL: 100 Coins"], regLLL))
    world.regions.append(regLLL)

    regSSL = create_region("Shifting Sand Land", player, world)
    create_default_locs(regSSL, locSSL_table, player)
    if (world.EnableCoinStars[player].value):
        regSSL.locations.append(SM64Location(player, "SSL: 100 Coins", location_table["SSL: 100 Coins"], regSSL))
    world.regions.append(regSSL)

    regDDD = create_region("Dire, Dire Docks", player, world)
    create_default_locs(regDDD, locDDD_table, player)
    if (world.EnableCoinStars[player].value):
        regDDD.locations.append(SM64Location(player, "DDD: 100 Coins", location_table["DDD: 100 Coins"], regDDD))
    world.regions.append(regDDD)

    regCotMC = create_region("Cavern of the Metal Cap", player, world)
    create_default_locs(regCotMC, locCotMC_table, player)
    world.regions.append(regCotMC)

    regVCutM = create_region("Vanish Cap under the Moat", player, world)
    create_default_locs(regVCutM, locVCutM_table, player)
    world.regions.append(regVCutM)

    regBitFS = create_region("Bowser in the Fire Sea", player, world)
    create_default_locs(regBitFS, locBitFS_table, player)
    world.regions.append(regBitFS)

    regFloor2 = create_region("Second Floor", player, world)
    world.regions.append(regFloor2)

    regSL = create_region("Snowman's Land", player, world)
    create_default_locs(regSL, locSL_table, player)
    if (world.EnableCoinStars[player].value):
        regSL.locations.append(SM64Location(player, "SL: 100 Coins", location_table["SL: 100 Coins"], regSL))
    world.regions.append(regSL)

    regWDW = create_region("Wet-Dry World", player, world)
    create_default_locs(regWDW, locWDW_table, player)
    if (world.EnableCoinStars[player].value):
        regWDW.locations.append(SM64Location(player, "WDW: 100 Coins", location_table["WDW: 100 Coins"], regWDW))
    world.regions.append(regWDW)

    regTTM = create_region("Tall, Tall Mountain", player, world)
    create_default_locs(regTTM, locTTM_table, player)
    if (world.EnableCoinStars[player].value):
        regTTM.locations.append(SM64Location(player, "TTM: 100 Coins", location_table["TTM: 100 Coins"], regTTM))
    world.regions.append(regTTM)

    regTHI = create_region("Tiny-Huge Island", player, world)
    create_default_locs(regTHI, locTHI_table, player)
    if (world.EnableCoinStars[player].value):
        regTHI.locations.append(SM64Location(player, "THI: 100 Coins", location_table["THI: 100 Coins"], regTHI))
    world.regions.append(regTHI)

    regFloor3 = create_region("Third Floor", player, world)
    world.regions.append(regFloor3)

    regTTC = create_region("Tick Tock Clock", player, world)
    create_default_locs(regTTC, locTTC_table, player)
    if (world.EnableCoinStars[player].value):
        regTTC.locations.append(SM64Location(player, "TTC: 100 Coins", location_table["TTC: 100 Coins"], regTTC))
    world.regions.append(regTTC)

    regRR = create_region("Rainbow Ride", player, world)
    create_default_locs(regRR, locRR_table, player)
    if (world.EnableCoinStars[player].value):
        regRR.locations.append(SM64Location(player, "RR: 100 Coins", location_table["RR: 100 Coins"], regRR))
    world.regions.append(regRR)

    regWMotR = create_region("Wing Mario over the Rainbow", player, world)
    create_default_locs(regWMotR, locWMotR_table, player)
    world.regions.append(regWMotR)

    regBitS = create_region("Bowser in the Sky", player, world)
    create_default_locs(regBitS, locBitS_table, player)
    world.regions.append(regBitS)


def connect_regions(world: MultiWorld, player: int, source: str, target: str, rule=None):
    sourceRegion = world.get_region(source, player)
    targetRegion = world.get_region(target, player)

    connection = Entrance(player, '', sourceRegion)
    if rule:
        connection.access_rule = rule

    sourceRegion.exits.append(connection)
    connection.connect(targetRegion)

def create_region(name: str, player: int, world: MultiWorld) -> Region:
    return Region(name, player, world)

def create_default_locs(reg: Region, locs, player):
    reg_names = [name for name, id in locs.items()]
    reg.locations += [SM64Location(player, loc_name, location_table[loc_name], reg) for loc_name in locs]
