import typing
from enum import Enum
from BaseClasses import MultiWorld, Region
from .GameID import game_id, game_name
from .Options import JakAndDaxterOptions
from .Locations import JakAndDaxterLocation, location_table
from .locs import CellLocations, SpecialLocations, ScoutLocations


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
    GOL_AND_MAIAS_CITADEL_FINAL_BOSS = 8


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
    JakAndDaxterSubLevel.GOL_AND_MAIAS_CITADEL_ROTATING_TOWER: "Gol and Maia's Citadel Rotating Tower",
    JakAndDaxterSubLevel.GOL_AND_MAIAS_CITADEL_FINAL_BOSS: "Gol and Maia's Citadel Final Boss"
}


class JakAndDaxterRegion(Region):
    game: str = game_name


def create_regions(multiworld: MultiWorld, options: JakAndDaxterOptions, player: int):
    create_region(player, multiworld, "Menu")

    region_gr = create_region(player, multiworld, level_table[JakAndDaxterLevel.GEYSER_ROCK])
    create_locations(region_gr, {
        **CellLocations.locGR_cellTable,
        **ScoutLocations.locGR_scoutTable
    })

    region_sv = create_region(player, multiworld, level_table[JakAndDaxterLevel.SANDOVER_VILLAGE])
    create_locations(region_sv, {
        **CellLocations.locSV_cellTable,
        **ScoutLocations.locSV_scoutTable
    })

    region_fj = create_region(player, multiworld, level_table[JakAndDaxterLevel.FORBIDDEN_JUNGLE])
    create_locations(region_fj, {
        **{k: CellLocations.locFJ_cellTable[k] for k in {10, 11, 12, 14, 15, 16, 17}},
        **{k: SpecialLocations.loc_specialTable[k] for k in {2213, 2216}},
        **ScoutLocations.locFJ_scoutTable
    })

    sub_region_fjpr = create_subregion(region_fj, subLevel_table[JakAndDaxterSubLevel.FORBIDDEN_JUNGLE_PLANT_ROOM])
    create_locations(sub_region_fjpr, {k: CellLocations.locFJ_cellTable[k] for k in {13}})

    region_sb = create_region(player, multiworld, level_table[JakAndDaxterLevel.SENTINEL_BEACH])
    create_locations(region_sb, {
        **{k: CellLocations.locSB_cellTable[k] for k in {18, 19, 20, 21, 23, 24, 25}},
        **{k: SpecialLocations.loc_specialTable[k] for k in {2215}},
        **ScoutLocations.locSB_scoutTable
    })

    sub_region_sbct = create_subregion(region_sb, subLevel_table[JakAndDaxterSubLevel.SENTINEL_BEACH_CANNON_TOWER])
    create_locations(sub_region_sbct, {k: CellLocations.locSB_cellTable[k] for k in {22}})

    region_mi = create_region(player, multiworld, level_table[JakAndDaxterLevel.MISTY_ISLAND])
    create_locations(region_mi, {
        **CellLocations.locMI_cellTable,
        **ScoutLocations.locMI_scoutTable
    })

    region_fc = create_region(player, multiworld, level_table[JakAndDaxterLevel.FIRE_CANYON])
    create_locations(region_fc, {
        **CellLocations.locFC_cellTable,
        **ScoutLocations.locFC_scoutTable
    })

    region_rv = create_region(player, multiworld, level_table[JakAndDaxterLevel.ROCK_VILLAGE])
    create_locations(region_rv, {
        **CellLocations.locRV_cellTable,
        **{k: SpecialLocations.loc_specialTable[k] for k in {2217}},
        **ScoutLocations.locRV_scoutTable
    })

    region_pb = create_region(player, multiworld, level_table[JakAndDaxterLevel.PRECURSOR_BASIN])
    create_locations(region_pb, {
        **CellLocations.locPB_cellTable,
        **ScoutLocations.locPB_scoutTable
    })

    region_lpc = create_region(player, multiworld, level_table[JakAndDaxterLevel.LOST_PRECURSOR_CITY])
    create_locations(region_lpc, {
        **CellLocations.locLPC_cellTable,
        **ScoutLocations.locLPC_scoutTable
    })

    region_bs = create_region(player, multiworld, level_table[JakAndDaxterLevel.BOGGY_SWAMP])
    create_locations(region_bs, {
        **{k: CellLocations.locBS_cellTable[k] for k in {59, 60, 61, 62, 63, 64}},
        **{k: ScoutLocations.locBS_scoutTable[k] for k in {164, 165, 166, 167, 170}}
    })

    sub_region_bsff = create_subregion(region_bs, subLevel_table[JakAndDaxterSubLevel.BOGGY_SWAMP_FLUT_FLUT])
    create_locations(sub_region_bsff, {
        **{k: CellLocations.locBS_cellTable[k] for k in {58, 65}},
        **{k: ScoutLocations.locBS_scoutTable[k] for k in {168, 169}}
    })

    region_mp = create_region(player, multiworld, level_table[JakAndDaxterLevel.MOUNTAIN_PASS])
    create_locations(region_mp, {
        **{k: CellLocations.locMP_cellTable[k] for k in {66, 67, 69}},
        **ScoutLocations.locMP_scoutTable
    })

    sub_region_mps = create_subregion(region_mp, subLevel_table[JakAndDaxterSubLevel.MOUNTAIN_PASS_SHORTCUT])
    create_locations(sub_region_mps, {k: CellLocations.locMP_cellTable[k] for k in {68}})

    region_vc = create_region(player, multiworld, level_table[JakAndDaxterLevel.VOLCANIC_CRATER])
    create_locations(region_vc, {
        **CellLocations.locVC_cellTable,
        **ScoutLocations.locVC_scoutTable
    })

    region_sc = create_region(player, multiworld, level_table[JakAndDaxterLevel.SPIDER_CAVE])
    create_locations(region_sc, {
        **CellLocations.locSC_cellTable,
        **ScoutLocations.locSC_scoutTable
    })

    region_sm = create_region(player, multiworld, level_table[JakAndDaxterLevel.SNOWY_MOUNTAIN])
    create_locations(region_sm, {
        **{k: CellLocations.locSM_cellTable[k] for k in {86, 87, 88, 89, 92}},
        **{k: SpecialLocations.loc_specialTable[k] for k in {2218}},
        **{k: ScoutLocations.locSM_scoutTable[k] for k in {192, 193, 194, 195, 196}}
    })

    sub_region_smff = create_subregion(region_sm, subLevel_table[JakAndDaxterSubLevel.SNOWY_MOUNTAIN_FLUT_FLUT])
    create_locations(sub_region_smff, {
        **{k: CellLocations.locSM_cellTable[k] for k in {90}},
        **{k: SpecialLocations.loc_specialTable[k] for k in {2219}}
    })

    sub_region_smlf = create_subregion(region_sm, subLevel_table[JakAndDaxterSubLevel.SNOWY_MOUNTAIN_LURKER_FORT])
    create_locations(sub_region_smlf, {
        **{k: CellLocations.locSM_cellTable[k] for k in {91, 93}},
        **{k: ScoutLocations.locSM_scoutTable[k] for k in {197, 198}}
    })

    region_lt = create_region(player, multiworld, level_table[JakAndDaxterLevel.LAVA_TUBE])
    create_locations(region_lt, {
        **CellLocations.locLT_cellTable,
        **ScoutLocations.locLT_scoutTable
    })

    region_gmc = create_region(player, multiworld, level_table[JakAndDaxterLevel.GOL_AND_MAIAS_CITADEL])
    create_locations(region_gmc, {
        **{k: CellLocations.locGMC_cellTable[k] for k in {96, 97, 98}},
        **{k: ScoutLocations.locGMC_scoutTable[k] for k in {206, 207, 208, 209, 210, 211}},
        **{k: SpecialLocations.loc_specialTable[k] for k in {2220, 2221, 2222}}
    })

    sub_region_gmcrt = create_subregion(region_gmc,
                                        subLevel_table[JakAndDaxterSubLevel.GOL_AND_MAIAS_CITADEL_ROTATING_TOWER])
    create_locations(sub_region_gmcrt, {
        **{k: CellLocations.locGMC_cellTable[k] for k in {99, 100}},
        **{k: ScoutLocations.locGMC_scoutTable[k] for k in {212}},
        **{k: SpecialLocations.loc_specialTable[k] for k in {2223}}
    })

    create_subregion(sub_region_gmcrt, subLevel_table[JakAndDaxterSubLevel.GOL_AND_MAIAS_CITADEL_FINAL_BOSS])


def create_region(player: int, multiworld: MultiWorld, name: str) -> JakAndDaxterRegion:
    region = JakAndDaxterRegion(name, player, multiworld)

    multiworld.regions.append(region)
    return region


def create_subregion(parent: Region, name: str) -> JakAndDaxterRegion:
    region = JakAndDaxterRegion(name, parent.player, parent.multiworld)

    parent.multiworld.regions.append(region)
    return region


def create_locations(region: Region, locations: typing.Dict[int, str]):
    region.locations += [JakAndDaxterLocation(region.player, location_table[loc], game_id + loc, region)
                         for loc in locations]
