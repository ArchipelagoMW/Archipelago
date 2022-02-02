import typing
from BaseClasses import MultiWorld, Region, Entrance, Location, RegionType
from .Locations import SM64Location, location_table,locBoB_table,locWhomp_table,locJRB_table,locCCM_table,locBBH_table, \
                                                    locHMC_table,locLLL_table,locSSL_table,locDDD_table,locSL_table, \
                                                    locWDW_table,locTTM_table,locTHI_table,locTTC_table,locRR_table, \
                                                    locBitDW_table, locBitFS_table, locSS_table, locCap_table

sm64courses = ["Bob-omb Battlefield", "Whomp's Fortress", "Jolly Roger Bay", "Cool, Cool Mountain", "Big Boo's Haunt",
               "Hazy Maze Cave", "Lethal Lava Land", "Shifting Sand Land", "Dire, Dire Docks", "Snowman's Land", "Wet-Dry World",
               "Tall, Tall Mountain", "Tiny-Huge Island", "Tick Tock Clock", "Rainbow Ride"]

def create_regions(world: MultiWorld, player: int):

    regSS = Region("Menu", RegionType.Generic, "Castle Area", player, world)
    locSS_names = [name for name, id in locSS_table.items()]
    locSS_names += [name for name, id in locCap_table.items()]
    regSS.locations += [SM64Location(player, loc_name, location_table[loc_name], regSS) for loc_name in locSS_names]
    world.regions.append(regSS)

    regBoB = Region("Bob-omb Battlefield", RegionType.Generic, "Bob-omb Battlefield", player, world)
    locBoB_names = [name for name, id in locBoB_table.items()]
    regBoB.locations += [SM64Location(player, loc_name, location_table[loc_name], regBoB) for loc_name in locBoB_names]
    if (world.EnableCoinStars[player].value):
        regBoB.locations.append(SM64Location(player, "BoB: 100 Coins", location_table["BoB: 100 Coins"], regBoB))
    world.regions.append(regBoB)

    regWhomp = Region("Whomp's Fortress", RegionType.Generic, "Whomp's Fortress", player, world)
    locWhomp_names = [name for name, id in locWhomp_table.items()]
    regWhomp.locations += [SM64Location(player, loc_name, location_table[loc_name], regWhomp) for loc_name in locWhomp_names]
    if (world.EnableCoinStars[player].value):
        regWhomp.locations.append(SM64Location(player, "WF: 100 Coins", location_table["WF: 100 Coins"], regWhomp))
    world.regions.append(regWhomp)

    regJRB = Region("Jolly Roger Bay", RegionType.Generic, "Jolly Roger Bay", player, world)
    locJRB_names = [name for name, id in locJRB_table.items()]
    regJRB.locations += [SM64Location(player, loc_name, location_table[loc_name], regJRB) for loc_name in locJRB_names]
    if (world.EnableCoinStars[player].value):
        regJRB.locations.append(SM64Location(player, "JRB: 100 Coins", location_table["JRB: 100 Coins"], regJRB))
    world.regions.append(regJRB)

    regCCM = Region("Cool, Cool Mountain", RegionType.Generic, "Cool, Cool Mountain", player, world)
    locCCM_names = [name for name, id in locCCM_table.items()]
    regCCM.locations += [SM64Location(player, loc_name, location_table[loc_name], regCCM) for loc_name in locCCM_names]
    if (world.EnableCoinStars[player].value):
        regCCM.locations.append(SM64Location(player, "CCM: 100 Coins", location_table["CCM: 100 Coins"], regCCM))
    world.regions.append(regCCM)

    regBBH = Region("Big Boo's Haunt", RegionType.Generic, "Big Boo's Haunt", player, world)
    locBBH_names = [name for name, id in locBBH_table.items()]
    regBBH.locations += [SM64Location(player, loc_name, location_table[loc_name], regBBH) for loc_name in locBBH_names]
    if (world.EnableCoinStars[player].value):
        regBBH.locations.append(SM64Location(player, "BBH: 100 Coins", location_table["BBH: 100 Coins"], regBBH))
    world.regions.append(regBBH)

    regBitDW = Region("Bowser in the Dark World", RegionType.Generic, "Bowser in the Dark World", player, world)
    locBitDW_names = [name for name, id in locBitDW_table.items()]
    regBitDW.locations += [SM64Location(player, loc_name, location_table[loc_name], regBitDW) for loc_name in locBitDW_names]
    world.regions.append(regBitDW)

    regBasement = Region("Basement", RegionType.Generic, "Basement", player, world)
    world.regions.append(regBasement)

    regHMC = Region("Hazy Maze Cave", RegionType.Generic, "Hazy Maze Cave", player, world)
    locHMC_names = [name for name, id in locHMC_table.items()]
    regHMC.locations += [SM64Location(player, loc_name, location_table[loc_name], regHMC) for loc_name in locHMC_names]
    if (world.EnableCoinStars[player].value):
        regHMC.locations.append(SM64Location(player, "HMC: 100 Coins", location_table["HMC: 100 Coins"], regHMC))
    world.regions.append(regHMC)

    regLLL = Region("Lethal Lava Land", RegionType.Generic, "Lethal Lava Land", player, world)
    locLLL_names = [name for name, id in locLLL_table.items()]
    regLLL.locations += [SM64Location(player, loc_name, location_table[loc_name], regLLL) for loc_name in locLLL_names]
    if (world.EnableCoinStars[player].value):
        regLLL.locations.append(SM64Location(player, "LLL: 100 Coins", location_table["LLL: 100 Coins"], regLLL))
    world.regions.append(regLLL)

    regSSL = Region("Shifting Sand Land", RegionType.Generic, "Shifting Sand Land", player, world)
    locSSL_names = [name for name, id in locSSL_table.items()]
    regSSL.locations += [SM64Location(player, loc_name, location_table[loc_name], regSSL) for loc_name in locSSL_names]
    if (world.EnableCoinStars[player].value):
        regSSL.locations.append(SM64Location(player, "SSL: 100 Coins", location_table["SSL: 100 Coins"], regSSL))
    world.regions.append(regSSL)

    regDDD = Region("Dire, Dire Docks", RegionType.Generic, "Dire, Dire Docks", player, world)
    locDDD_names = [name for name, id in locDDD_table.items()]
    regDDD.locations += [SM64Location(player, loc_name, location_table[loc_name], regDDD) for loc_name in locDDD_names]
    if (world.EnableCoinStars[player].value):
        regDDD.locations.append(SM64Location(player, "DDD: 100 Coins", location_table["DDD: 100 Coins"], regDDD))
    world.regions.append(regDDD)

    regBitFS = Region("Bowser in the Fire Sea", RegionType.Generic, "Bowser in the Fire Sea", player, world)
    locBitFS_names = [name for name, id in locBitFS_table.items()]
    regBitFS.locations += [SM64Location(player, loc_name, location_table[loc_name], regBitFS) for loc_name in locBitFS_names]
    world.regions.append(regBitFS)

    regFloor2 = Region("Second Floor", RegionType.Generic, "Second Floor", player, world)
    world.regions.append(regFloor2)

    regSL = Region("Snowman's Land", RegionType.Generic, "Snowman's Land", player, world)
    locSL_names = [name for name, id in locSL_table.items()]
    regSL.locations += [SM64Location(player, loc_name, location_table[loc_name], regSL) for loc_name in locSL_names]
    if (world.EnableCoinStars[player].value):
        regSL.locations.append(SM64Location(player, "SL: 100 Coins", location_table["SL: 100 Coins"], regSL))
    world.regions.append(regSL)

    regWDW = Region("Wet-Dry World", RegionType.Generic, "Wet-Dry World", player, world)
    locWDW_names = [name for name, id in locWDW_table.items()]
    regWDW.locations += [SM64Location(player, loc_name, location_table[loc_name], regWDW) for loc_name in locWDW_names]
    if (world.EnableCoinStars[player].value):
        regWDW.locations.append(SM64Location(player, "WDW: 100 Coins", location_table["WDW: 100 Coins"], regWDW))
    world.regions.append(regWDW)

    regTTM = Region("Tall, Tall Mountain", RegionType.Generic, "Tall, Tall Mountain", player, world)
    locTTM_names = [name for name, id in locTTM_table.items()]
    regTTM.locations += [SM64Location(player, loc_name, location_table[loc_name], regTTM) for loc_name in locTTM_names]
    if (world.EnableCoinStars[player].value):
        regTTM.locations.append(SM64Location(player, "TTM: 100 Coins", location_table["TTM: 100 Coins"], regTTM))
    world.regions.append(regTTM)

    regTHI = Region("Tiny-Huge Island", RegionType.Generic, "Tiny-Huge Island", player, world)
    locTHI_names = [name for name, id in locTHI_table.items()]
    regTHI.locations += [SM64Location(player, loc_name, location_table[loc_name], regTHI) for loc_name in locTHI_names]
    if (world.EnableCoinStars[player].value):
        regTHI.locations.append(SM64Location(player, "THI: 100 Coins", location_table["THI: 100 Coins"], regTHI))
    world.regions.append(regTHI)

    regFloor3 = Region("Third Floor", RegionType.Generic, "Third Floor", player, world)
    world.regions.append(regFloor3)

    regTTC = Region("Tick Tock Clock", RegionType.Generic, "Tick Tock Clock", player, world)
    locTTC_names = [name for name, id in locTTC_table.items()]
    regTTC.locations += [SM64Location(player, loc_name, location_table[loc_name], regTTC) for loc_name in locTTC_names]
    if (world.EnableCoinStars[player].value):
        regTTC.locations.append(SM64Location(player, "TTC: 100 Coins", location_table["TTC: 100 Coins"], regTTC))
    world.regions.append(regTTC)

    regRR = Region("Rainbow Ride", RegionType.Generic, "Rainbow Ride", player, world)
    locRR_names = [name for name, id in locRR_table.items()]
    regRR.locations += [SM64Location(player, loc_name, location_table[loc_name], regRR) for loc_name in locRR_names]
    if (world.EnableCoinStars[player].value):
        regRR.locations.append(SM64Location(player, "RR: 100 Coins", location_table["RR: 100 Coins"], regRR))
    world.regions.append(regRR)


def connect_regions(world: MultiWorld, player: int, source: str, target: str, rule):
    sourceRegion = world.get_region(source, player)
    targetRegion = world.get_region(target, player)

    connection = Entrance(player,'', sourceRegion)
    connection.access_rule = rule

    sourceRegion.exits.append(connection)
    connection.connect(targetRegion) 