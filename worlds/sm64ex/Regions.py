import typing
from enum import Enum

from BaseClasses import MultiWorld, Region, Entrance, Location
from .Options import SM64Options
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


class SM64Region(Region):
    subregions: typing.List[Region] = []


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
sm64_paintings_to_level = {painting: level for (level, painting) in sm64_level_to_paintings.items() }

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
sm64_secrets_to_level = {secret: level for (level,secret) in sm64_level_to_secrets.items() }

sm64_entrances_to_level = {**sm64_paintings_to_level, **sm64_secrets_to_level }
sm64_level_to_entrances = {**sm64_level_to_paintings, **sm64_level_to_secrets }

def create_regions(world: MultiWorld, options: SM64Options, player: int):
    regSS = Region("Menu", player, world, "Castle Area")
    create_default_locs(regSS, locSS_table)
    world.regions.append(regSS)

    regBoB = create_region("Bob-omb Battlefield", player, world)
    create_locs(regBoB, "BoB: Big Bob-Omb on the Summit", "BoB: Footrace with Koopa The Quick",
                        "BoB: Mario Wings to the Sky", "BoB: Behind Chain Chomp's Gate", "BoB: Bob-omb Buddy")
    bob_island = create_subregion(regBoB, "BoB: Island", "BoB: Shoot to the Island in the Sky", "BoB: Find the 8 Red Coins")
    regBoB.subregions = [bob_island]
    if options.enable_coin_stars:
        create_locs(regBoB, "BoB: 100 Coins")

    regWhomp = create_region("Whomp's Fortress", player, world)
    create_locs(regWhomp, "WF: Chip Off Whomp's Block", "WF: Shoot into the Wild Blue", "WF: Red Coins on the Floating Isle",
                          "WF: Fall onto the Caged Island", "WF: Blast Away the Wall")
    wf_tower = create_subregion(regWhomp, "WF: Tower", "WF: To the Top of the Fortress", "WF: Bob-omb Buddy")
    regWhomp.subregions = [wf_tower]
    if options.enable_coin_stars:
        create_locs(regWhomp, "WF: 100 Coins")

    regJRBDoor = create_region("Jolly Roger Bay Door", player, world)
    regJRB = create_region("Jolly Roger Bay", player, world)
    create_locs(regJRB, "JRB: Plunder in the Sunken Ship", "JRB: Can the Eel Come Out to Play?", "JRB: Treasure of the Ocean Cave",
                        "JRB: Blast to the Stone Pillar", "JRB: Through the Jet Stream", "JRB: Bob-omb Buddy")
    jrb_upper = create_subregion(regJRB, 'JRB: Upper', "JRB: Red Coins on the Ship Afloat")
    regJRB.subregions = [jrb_upper]
    if options.enable_coin_stars:
        create_locs(jrb_upper, "JRB: 100 Coins")

    regCCM = create_region("Cool, Cool Mountain", player, world)
    create_default_locs(regCCM, locCCM_table)
    if options.enable_coin_stars:
        create_locs(regCCM, "CCM: 100 Coins")

    regBBH = create_region("Big Boo's Haunt", player, world)
    create_locs(regBBH, "BBH: Go on a Ghost Hunt", "BBH: Ride Big Boo's Merry-Go-Round",
                        "BBH: Secret of the Haunted Books", "BBH: Seek the 8 Red Coins")
    bbh_third_floor = create_subregion(regBBH, "BBH: Third Floor", "BBH: Eye to Eye in the Secret Room")
    bbh_roof = create_subregion(bbh_third_floor, "BBH: Roof", "BBH: Big Boo's Balcony", "BBH: 1Up Block Top of Mansion")
    regBBH.subregions = [bbh_third_floor, bbh_roof]
    if options.enable_coin_stars:
        create_locs(regBBH, "BBH: 100 Coins")

    regPSS = create_region("The Princess's Secret Slide", player, world)
    create_default_locs(regPSS, locPSS_table)

    regSA = create_region("The Secret Aquarium", player, world)
    create_default_locs(regSA, locSA_table)

    regTotWC = create_region("Tower of the Wing Cap", player, world)
    create_default_locs(regTotWC, locTotWC_table)

    regBitDW = create_region("Bowser in the Dark World", player, world)
    create_default_locs(regBitDW, locBitDW_table)

    create_region("Basement", player, world)

    regHMC = create_region("Hazy Maze Cave", player, world)
    create_locs(regHMC, "HMC: Swimming Beast in the Cavern", "HMC: Metal-Head Mario Can Move!",
                        "HMC: Watch for Rolling Rocks", "HMC: Navigating the Toxic Maze","HMC: 1Up Block Past Rolling Rocks")
    hmc_red_coin_area = create_subregion(regHMC, "HMC: Red Coin Area", "HMC: Elevate for 8 Red Coins")
    hmc_pit_islands = create_subregion(regHMC, "HMC: Pit Islands", "HMC: A-Maze-Ing Emergency Exit", "HMC: 1Up Block above Pit")
    regHMC.subregions = [hmc_red_coin_area, hmc_pit_islands]
    if options.enable_coin_stars:
        create_locs(hmc_red_coin_area, "HMC: 100 Coins")

    regLLL = create_region("Lethal Lava Land", player, world)
    create_locs(regLLL, "LLL: Boil the Big Bully", "LLL: Bully the Bullies",
                        "LLL: 8-Coin Puzzle with 15 Pieces", "LLL: Red-Hot Log Rolling")
    lll_upper_volcano = create_subregion(regLLL, "LLL: Upper Volcano", "LLL: Hot-Foot-It into the Volcano", "LLL: Elevator Tour in the Volcano")
    regLLL.subregions = [lll_upper_volcano]
    if options.enable_coin_stars:
        create_locs(regLLL, "LLL: 100 Coins")

    regSSL = create_region("Shifting Sand Land", player, world)
    create_locs(regSSL, "SSL: In the Talons of the Big Bird", "SSL: Shining Atop the Pyramid",
                        "SSL: Free Flying for 8 Red Coins", "SSL: Bob-omb Buddy",
                        "SSL: 1Up Block Outside Pyramid", "SSL: 1Up Block Pyramid Left Path", "SSL: 1Up Block Pyramid Back")
    ssl_upper_pyramid = create_subregion(regSSL, "SSL: Upper Pyramid", "SSL: Inside the Ancient Pyramid",
                                         "SSL: Stand Tall on the Four Pillars", "SSL: Pyramid Puzzle")
    regSSL.subregions = [ssl_upper_pyramid]
    if options.enable_coin_stars:
        create_locs(regSSL, "SSL: 100 Coins")

    regDDD = create_region("Dire, Dire Docks", player, world)
    create_locs(regDDD, "DDD: Board Bowser's Sub", "DDD: Chests in the Current", "DDD: Through the Jet Stream",
                        "DDD: The Manta Ray's Reward", "DDD: Collect the Caps...", "DDD: Pole-Jumping for Red Coins")
    if options.enable_coin_stars:
        create_locs(regDDD, "DDD: 100 Coins")

    regCotMC = create_region("Cavern of the Metal Cap", player, world)
    create_default_locs(regCotMC, locCotMC_table)

    regVCutM = create_region("Vanish Cap under the Moat", player, world)
    create_default_locs(regVCutM, locVCutM_table)

    regBitFS = create_region("Bowser in the Fire Sea", player, world)
    bitfs_upper = create_subregion(regBitFS, "BitFS: Upper", *locBitFS_table.keys())
    regBitFS.subregions = [bitfs_upper]

    create_region("Second Floor", player, world)

    regSL = create_region("Snowman's Land", player, world)
    create_default_locs(regSL, locSL_table)
    if options.enable_coin_stars:
        create_locs(regSL, "SL: 100 Coins")

    regWDW = create_region("Wet-Dry World", player, world)
    create_locs(regWDW, "WDW: Express Elevator--Hurry Up!")
    wdw_top = create_subregion(regWDW, "WDW: Top", "WDW: Shocking Arrow Lifts!", "WDW: Top o' the Town",
                                                   "WDW: Secrets in the Shallows & Sky", "WDW: Bob-omb Buddy")
    wdw_downtown = create_subregion(regWDW, "WDW: Downtown", "WDW: Go to Town for Red Coins", "WDW: Quick Race Through Downtown!", "WDW: 1Up Block in Downtown")
    regWDW.subregions = [wdw_top, wdw_downtown]
    if options.enable_coin_stars:
        create_locs(wdw_top, "WDW: 100 Coins")

    regTTM = create_region("Tall, Tall Mountain", player, world)
    ttm_middle = create_subregion(regTTM, "TTM: Middle", "TTM: Scary 'Shrooms, Red Coins", "TTM: Blast to the Lonely Mushroom",
                                                         "TTM: Bob-omb Buddy", "TTM: 1Up Block on Red Mushroom")
    ttm_top = create_subregion(ttm_middle, "TTM: Top", "TTM: Scale the Mountain", "TTM: Mystery of the Monkey Cage",
                                                       "TTM: Mysterious Mountainside", "TTM: Breathtaking View from Bridge")
    regTTM.subregions = [ttm_middle, ttm_top]
    if options.enable_coin_stars:
        create_locs(ttm_top, "TTM: 100 Coins")

    create_region("Tiny-Huge Island (Huge)", player, world)
    create_region("Tiny-Huge Island (Tiny)", player, world)
    regTHI = create_region("Tiny-Huge Island", player, world)
    create_locs(regTHI, "THI: 1Up Block THI Small near Start")
    thi_pipes = create_subregion(regTHI, "THI: Pipes", "THI: The Tip Top of the Huge Island", "THI: Pluck the Piranha Flower", "THI: Rematch with Koopa the Quick",
                                                       "THI: Five Itty Bitty Secrets", "THI: Wiggler's Red Coins", "THI: Bob-omb Buddy",
                                                       "THI: 1Up Block THI Large near Start", "THI: 1Up Block Windy Area")
    thi_large_top = create_subregion(thi_pipes, "THI: Large Top", "THI: Make Wiggler Squirm")
    regTHI.subregions = [thi_pipes, thi_large_top]
    if options.enable_coin_stars:
        create_locs(thi_large_top, "THI: 100 Coins")

    regFloor3 = create_region("Third Floor", player, world)

    regTTC = create_region("Tick Tock Clock", player, world)
    create_locs(regTTC, "TTC: Stop Time for Red Coins")
    ttc_lower = create_subregion(regTTC, "TTC: Lower", "TTC: Roll into the Cage", "TTC: Get a Hand")
    ttc_upper = create_subregion(ttc_lower, "TTC: Upper", "TTC: Timed Jumps on Moving Bars", "TTC: The Pit and the Pendulums")
    ttc_top = create_subregion(ttc_upper, "TTC: Top", "TTC: 1Up Block Midway Up", "TTC: Stomp on the Thwomp", "TTC: 1Up Block at the Top")
    regTTC.subregions = [ttc_lower, ttc_upper, ttc_top]
    if options.enable_coin_stars:
        create_locs(ttc_top, "TTC: 100 Coins")

    regRR = create_region("Rainbow Ride", player, world)
    create_locs(regRR, "RR: Swingin' in the Breeze", "RR: Tricky Triangles!",
                       "RR: 1Up Block Top of Red Coin Maze", "RR: 1Up Block Under Fly Guy", "RR: Bob-omb Buddy")
    rr_maze = create_subregion(regRR, "RR: Maze", "RR: Coins Amassed in a Maze")
    rr_cruiser = create_subregion(regRR, "RR: Cruiser", "RR: Cruiser Crossing the Rainbow", "RR: Somewhere Over the Rainbow")
    rr_house = create_subregion(regRR, "RR: House", "RR: The Big House in the Sky", "RR: 1Up Block On House in the Sky")
    regRR.subregions = [rr_maze, rr_cruiser, rr_house]
    if options.enable_coin_stars:
        create_locs(rr_maze, "RR: 100 Coins")

    regWMotR = create_region("Wing Mario over the Rainbow", player, world)
    create_default_locs(regWMotR, locWMotR_table)

    regBitS = create_region("Bowser in the Sky", player, world)
    create_locs(regBitS, "Bowser in the Sky 1Up Block")
    bits_top = create_subregion(regBitS, "BitS: Top", "Bowser in the Sky Red Coins")
    regBitS.subregions = [bits_top]


def connect_regions(world: MultiWorld, player: int, source: str, target: str, rule=None) -> Entrance:
    sourceRegion = world.get_region(source, player)
    targetRegion = world.get_region(target, player)
    return sourceRegion.connect(targetRegion, rule=rule)


def create_region(name: str, player: int, world: MultiWorld) -> SM64Region:
    region = SM64Region(name, player, world)
    world.regions.append(region)
    return region


def create_subregion(source_region: Region, name: str, *locs: str) -> SM64Region:
    region = SM64Region(name, source_region.player, source_region.multiworld)
    connection = Entrance(source_region.player, name, source_region)
    source_region.exits.append(connection)
    connection.connect(region)
    source_region.multiworld.regions.append(region)
    create_locs(region, *locs)
    return region


def set_subregion_access_rule(world, player, region_name: str, rule):
    world.get_entrance(world, player, region_name).access_rule = rule


def create_default_locs(reg: Region, default_locs: dict):
    create_locs(reg, *default_locs.keys())


def create_locs(reg: Region, *locs: str):
    reg.locations += [SM64Location(reg.player, loc_name, location_table[loc_name], reg) for loc_name in locs]
