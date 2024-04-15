import typing
from BaseClasses import MultiWorld, Region, Entrance, Location
from .Options import JakAndDaxterOptions
from .Locations import JakAndDaxterLocation, location_table
import locs.CellLocations

class JakAndDaxterLevel(int, Enum):
    GEYSER_ROCK = 0
    SANDOVER_VILLAGE = 1
    FORBIDDEN_JUNGLE = 2
    SENTINEL_BEACH = 3
    MISTY_ISLAND = 4
    FIRE_CANYON = 5
    ROCK_VILLAGE = 6
    PRECURSOR_BASIN = 7
    LOST_PRECURSOR_CITY = 8
    BOGGY_SWAMP = 9
    MOUNTAIN_PASS = 10
    VOLCANIC_CRATER = 11
    SPIDER_CAVE = 12
    SNOWY_MOUNTAIN = 13
    LAVA_TUBE = 14
    GOL_AND_MAIAS_CITADEL = 15

class JakAndDaxterSubLevel(int, Enum):
    MAIN_AREA = 0
    FORBIDDEN_JUNGLE_PLANT_ROOM = 1
    SENTINEL_BEACH_CANNON_TOWER = 2
    BOGGY_SWAMP_FLUT_FLUT = 3
    MOUNTAIN_PASS_SHORTCUT = 4
    SNOWY_MOUNTAIN_FLUT_FLUT = 5
    SNOWY_MOUNTAIN_LURKER_FORT = 6
    GOL_AND_MAIAS_CITADEL_ROTATING_TOWER = 7

level_table: typing.Dict[JakAndDaxterLevel, str] = {
    JakAndDaxterLevel.GEYSER_ROCK: "Geyser Rock",
    JakAndDaxterLevel.SANDOVER_VILLAGE: "Sandover Village",
    JakAndDaxterLevel.FORBIDDEN_JUNGLE: "Forbidden Jungle",
    JakAndDaxterLevel.SENTINEL_BEACH: "Sentinel Beach",
    JakAndDaxterLevel.MISTY_ISLAND: "Misty Island",
    JakAndDaxterLevel.FIRE_CANYON: "Fire Canyon",
    JakAndDaxterLevel.ROCK_VILLAGE: "Rock Village",
    JakAndDaxterLevel.PRECURSOR_BASIN: "Precursor Basin",
    JakAndDaxterLevel.LOST_PRECURSOR_CITY: "Lost Precursor City",
    JakAndDaxterLevel.BOGGY_SWAMP: "Boggy Swamp",
    JakAndDaxterLevel.MOUNTAIN_PASS: "Mountain Pass",
    JakAndDaxterLevel.VOLCANIC_CRATER: "Volcanic Crater",
    JakAndDaxterLevel.SPIDER_CAVE: "Spider Cave",
    JakAndDaxterLevel.SNOWY_MOUNTAIN: "Snowy Mountain",
    JakAndDaxterLevel.LAVA_TUBE: "Lava Tube",
    JakAndDaxterLevel.GOL_AND_MAIAS_CITADEL: "Gol and Maia's Citadel"
}

subLevel_table: typing.Dict[JakAndDaxterSubLevel, str] = {
    JakAndDaxterSubLevel.MAIN_AREA: "Main Area",
    JakAndDaxterSubLevel.FORBIDDEN_JUNGLE_PLANT_ROOM: "Forbidden Jungle Plant Room",
    JakAndDaxterSubLevel.SENTINEL_BEACH_CANNON_TOWER: "Sentinel Beach Cannon Tower",
    JakAndDaxterSubLevel.BOGGY_SWAMP_FLUT_FLUT: "Boggy Swamp Flut Flut",
    JakAndDaxterSubLevel.MOUNTAIN_PASS_SHORTCUT: "Mountain Pass Shortcut",
    JakAndDaxterSubLevel.SNOWY_MOUNTAIN_FLUT_FLUT: "Snowy Mountain Flut Flut",
    JakAndDaxterSubLevel.SNOWY_MOUNTAIN_LURKER_FORT: "Snowy Mountain Lurker Fort",
    JakAndDaxterSubLevel.GOL_AND_MAIAS_CITADEL_ROTATING_TOWER: "Gol and Maia's Citadel Rotating Tower"
}

class JakAndDaxterRegion(Region):
    game: str = "Jak and Daxter: The Precursor Legacy"

def create_regions(multiworld: MultiWorld, options: JakAndDaxterOptions, player: int):
    regionMenu = Region("Menu", player, multiworld)

    regionGR = create_region(player, multiworld, level_table[JakAndDaxterLevel.GEYSER_ROCK])
    create_locations(regionGR, locGR_cellTable)

    regionSV = create_region(player, multiworld, level_table[JakAndDaxterLevel.SANDOVER_VILLAGE])
    create_locations(regionSV, locSV_cellTable)

    regionFJ = create_region(player, multiworld, level_table[JakAndDaxterLevel.FORBIDDEN_JUNGLE])
    create_locations(regionFJ, {k: locFJ_cellTable[k] for k in {10, 11, 12, 14, 15, 16, 17}})

    subRegionFJPR = create_subregion(regionFJ, subLevel_table[JakAndDaxterSubLevel.FORBIDDEN_JUNGLE_PLANT_ROOM])
    create_locations(subRegionFJPR, {k: locFJ_cellTable[k] for k in {13}})

    regionSB = create_region(player, multiworld, level_table[JakAndDaxterLevel.SENTINEL_BEACH])
    create_locations(regionSB, {k: locSB_cellTable[k] for k in {18, 19, 20, 21, 23, 24, 25}})

    subRegionSBCT = create_subregion(regionSB, subLevel_table[JakAndDaxterSubLevel.SENTINEL_BEACH_CANNON_TOWER])
    create_locations(subRegionSBCT, {k: locSB_cellTable[k] for k in {22}})

    regionMI = create_region(player, multiworld, level_table[JakAndDaxterLevel.MISTY_ISLAND])
    create_locations(regionMI, locMI_cellTable)

    regionFC = create_region(player, multiworld, level_table[JakAndDaxterLevel.FIRE_CANYON])
    create_locations(regionFC, locFC_cellTable)

    regionRV = create_region(player, multiworld, level_table[JakAndDaxterLevel.ROCK_VILLAGE])
    create_locations(regionRV, locRV_cellTable)

    regionPB = create_region(player, multiworld, level_table[JakAndDaxterLevel.PRECURSOR_BASIN])
    create_locations(regionPB, locPB_cellTable)

    regionLPC = create_region(player, multiworld, level_table[JakAndDaxterLevel.LOST_PRECURSOR_CITY])
    create_locations(regionLPC, locPB_cellTable)

    regionBS = create_region(player, multiworld, level_table[JakAndDaxterLevel.BOGGY_SWAMP])
    create_locations(regionBS, {k: locBS_cellTable[k] for k in {59, 60, 61, 62, 63, 64}})

    subRegionBSFF = create_subregion(regionBS, subLevel_table[JakAndDaxterSubLevel.BOGGY_SWAMP_FLUT_FLUT])
    create_locations(subRegionBSFF, {k: locBS_cellTable[k] for k in {58, 65}})

    regionMP = create_region(player, multiworld, level_table[JakAndDaxterLevel.MOUNTAIN_PASS])
    create_locations(regionMP, {k: locMP_cellTable[k] for k in {66, 67, 69}})

    subRegionMPS = create_subregion(regionMP, subLevel_table[JakAndDaxterSubLevel.MOUNTAIN_PASS_SHORTCUT])
    create_locations(subRegionMPS, {k: locMP_cellTable[k] for k in {68}})

    regionVC = create_region(player, multiworld, level_table[JakAndDaxterLevel.VOLCANIC_CRATER])
    create_locations(regionVC, locVC_cellTable)

    regionSC = create_region(player, multiworld, level_table[JakAndDaxterLevel.SPIDER_CAVE])
    create_locations(regionSC, locSC_cellTable)

    regionSM = create_region(player, multiworld, level_table[JakAndDaxterLevel.SNOWY_MOUNTAIN])
    create_locations(regionSM, {k: locSM_cellTable[k] for k in {86, 87, 88, 89, 92}})

    subRegionSMFF = create_subregion(regionSM, subLevel_table[JakAndDaxterSubLevel.SNOWY_MOUNTAIN_FLUT_FLUT])
    create_locations(subRegionSMFF, {k: locSM_cellTable[k] for k in {90}})

    subRegionSMLF = create_subregion(regionSM, subLevel_table[JakAndDaxterSubLevel.SNOWY_MOUNTAIN_LURKER_FORT])
    create_locations(subRegionSMLF, {k: locSM_cellTable[k] for k in {91, 93}})

    regionLT = create_region(player, multiworld, level_table[JakAndDaxterLevel.LAVA_TUBE])
    create_locations(regionLT, locLT_cellTable)

    regionGMC = create_region(player, multiworld, level_table[JakAndDaxterLevel.GOL_AND_MAIAS_CITADEL])
    create_locations(regionGMC, {k: locGMC_cellTable[k] for k in {96, 97, 98}})

    subRegionGMCRT = create_subregion(regionSM, subLevel_table[JakAndDaxterSubLevel.GOL_AND_MAIAS_CITADEL_ROTATING_TOWER])
    create_locations(subRegionGMCRT, {k: locGMC_cellTable[k] for k in {99, 100}})

def create_region(player: int, multiworld: MultiWorld, name: str) -> JakAndDaxterRegion:
    region = JakAndDaxterRegion(name, player, multiworld)

    multiworld.regions.append(region)
    return region

def create_subregion(parent: Region, name: str) -> JakAndDaxterRegion:
    region = JakAndDaxterRegion(name, parent.player, parent.multiworld)

    connection = Entrance(parent.player, name, parent)
    connection.connect(region)
    parent.entrances.append(connection)

    parent.multiworld.regions.append(region)
    return region

def create_locations(region: Region, locs: typing.Dict[int, str]):
    region.locations += [JakAndDaxterLocation(region.player, loc, location_table[loc], region) for loc in locs]
