import typing

from enum import Enum

from BaseClasses import MultiWorld, Region, Entrance, Location
from .Locations import SM64Location, location_table, locBoB_table, locWhomp_table, locJRB_table, locCCM_table, \
    locBBH_table, \
    locHMC_table, locLLL_table, locSSL_table, locDDD_table, locSL_table, \
    locWDW_table, locTTM_table, locTHI_table, locTTC_table, locRR_table, \
    locPSS_table, locSA_table, locBitDW_table, locTotWC_table, locCotMC_table, \
    locVCutM_table, locBitFS_table, locWMotR_table, locBitS_table, locSS_table    

class SM64Levels(int, Enum):
    BOB_OMB_BATTLEFIELD = 91
    WHOMPS_FORTRESS = 241
    JOLLY_ROGER_BAY = 121
    COOL_COOL_MOUNTAIN = 51
    BIG_BOOS_HAUNT = 41
    HAZY_MAZE_CAVE = 71
    LETHAL_LAVA_LAND = 221
    SHIFTING_SAND_LAND = 81
    DIRE_DIRE_DOCKS = 231
    SNOWMANS_LAND = 101
    WET_DRY_WORLD = 111
    TALL_TALL_MOUNTAIN = 361
    TINY_HUGE_ISLAND_TINY = 132
    TINY_HUGE_ISLAND_HUGE = 131
    TICK_TOCK_CLOCK = 141
    RAINBOW_RIDE = 151
    THE_PRINCESS_SECRET_SLIDE = 271
    THE_SECRET_AQUARIUM = 201
    BOWSER_IN_THE_DARK_WORLD = 171
    TOWER_OF_THE_WING_CAP = 291
    CAVERN_OF_THE_METAL_CAP = 281
    VANISH_CAP_UNDER_THE_MOAT = 181
    BOWSER_IN_THE_FIRE_SEA = 191
    WING_MARIO_OVER_THE_RAINBOW = 311

# sm64paintings is a dict of entrances, format LEVEL | AREA
sm64_level_to_paintings: typing.Dict[SM64Levels, str] = {
    SM64Levels.BOB_OMB_BATTLEFIELD: "Bob-omb Battlefield",
    SM64Levels.WHOMPS_FORTRESS: "Whomp's Fortress",
    SM64Levels.JOLLY_ROGER_BAY: "Jolly Roger Bay",
    SM64Levels.COOL_COOL_MOUNTAIN: "Cool, Cool Mountain",
    SM64Levels.BIG_BOOS_HAUNT: "Big Boo's Haunt",
    SM64Levels.HAZY_MAZE_CAVE: "Hazy Maze Cave",
    SM64Levels.LETHAL_LAVA_LAND: "Lethal Lava Land",
    SM64Levels.SHIFTING_SAND_LAND: "Shifting Sand Land",
    SM64Levels.DIRE_DIRE_DOCKS: "Dire, Dire Docks",
    SM64Levels.SNOWMANS_LAND: "Snowman's Land",
    SM64Levels.WET_DRY_WORLD: "Wet-Dry World",
    SM64Levels.TALL_TALL_MOUNTAIN: "Tall, Tall Mountain",
    SM64Levels.TINY_HUGE_ISLAND_TINY: "Tiny-Huge Island (Tiny)",
    SM64Levels.TINY_HUGE_ISLAND_HUGE: "Tiny-Huge Island (Huge)",
    SM64Levels.TICK_TOCK_CLOCK: "Tick Tock Clock",
    SM64Levels.RAINBOW_RIDE: "Rainbow Ride"
}
sm64_paintings_to_level = { painting: level for (level,painting) in sm64_level_to_paintings.items() }

# sm64secrets is a dict of secret areas, same format as sm64paintings
sm64_level_to_secrets: typing.Dict[SM64Levels, str] = {
    SM64Levels.THE_PRINCESS_SECRET_SLIDE: "The Princess's Secret Slide",
    SM64Levels.THE_SECRET_AQUARIUM: "The Secret Aquarium",
    SM64Levels.BOWSER_IN_THE_DARK_WORLD: "Bowser in the Dark World",
    SM64Levels.TOWER_OF_THE_WING_CAP: "Tower of the Wing Cap",
    SM64Levels.CAVERN_OF_THE_METAL_CAP: "Cavern of the Metal Cap",
    SM64Levels.VANISH_CAP_UNDER_THE_MOAT: "Vanish Cap under the Moat",
    SM64Levels.BOWSER_IN_THE_FIRE_SEA: "Bowser in the Fire Sea",
    SM64Levels.WING_MARIO_OVER_THE_RAINBOW: "Wing Mario over the Rainbow"
}
sm64_secrets_to_level = { secret: level for (level,secret) in sm64_level_to_secrets.items() }

sm64_entrances_to_level = { **sm64_paintings_to_level, **sm64_secrets_to_level }
sm64_level_to_entrances = { **sm64_level_to_paintings, **sm64_level_to_secrets }

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

    regTHIT = create_region("Tiny-Huge Island (Tiny)", player, world)
    create_default_locs(regTHIT, locTHI_table, player)
    if (world.EnableCoinStars[player].value):
        regTHIT.locations.append(SM64Location(player, "THI: 100 Coins", location_table["THI: 100 Coins"], regTHIT))
    world.regions.append(regTHIT)
    regTHIH = create_region("Tiny-Huge Island (Huge)", player, world)
    world.regions.append(regTHIH)

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
