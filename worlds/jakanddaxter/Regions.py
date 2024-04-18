import typing
from enum import Enum, auto
from BaseClasses import MultiWorld, Region
from .GameID import game_id, game_name, cell_offset, fly_offset
from .Options import JakAndDaxterOptions
from .Locations import JakAndDaxterLocation, location_table
from .locs import CellLocations, ScoutLocations


class JakAndDaxterLevel(int, Enum):
    GEYSER_ROCK = auto()
    SANDOVER_VILLAGE = auto()
    FORBIDDEN_JUNGLE = auto()
    SENTINEL_BEACH = auto()
    MISTY_ISLAND = auto()
    FIRE_CANYON = auto()
    ROCK_VILLAGE = auto()
    PRECURSOR_BASIN = auto()
    LOST_PRECURSOR_CITY = auto()
    BOGGY_SWAMP = auto()
    MOUNTAIN_PASS = auto()
    VOLCANIC_CRATER = auto()
    SPIDER_CAVE = auto()
    SNOWY_MOUNTAIN = auto()
    LAVA_TUBE = auto()
    GOL_AND_MAIAS_CITADEL = auto()


class JakAndDaxterSubLevel(int, Enum):
    MAIN_AREA = auto()
    FORBIDDEN_JUNGLE_SWITCH_ROOM = auto()
    FORBIDDEN_JUNGLE_PLANT_ROOM = auto()
    SENTINEL_BEACH_CANNON_TOWER = auto()
    PRECURSOR_BASIN_BLUE_RINGS = auto()
    BOGGY_SWAMP_FLUT_FLUT = auto()
    MOUNTAIN_PASS_RACE = auto()
    MOUNTAIN_PASS_SHORTCUT = auto()
    SNOWY_MOUNTAIN_FLUT_FLUT = auto()
    SNOWY_MOUNTAIN_LURKER_FORT = auto()
    SNOWY_MOUNTAIN_FROZEN_BOX = auto()
    GOL_AND_MAIAS_CITADEL_ROTATING_TOWER = auto()
    GOL_AND_MAIAS_CITADEL_FINAL_BOSS = auto()


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
    JakAndDaxterSubLevel.FORBIDDEN_JUNGLE_SWITCH_ROOM: "Forbidden Jungle Switch Room",
    JakAndDaxterSubLevel.FORBIDDEN_JUNGLE_PLANT_ROOM: "Forbidden Jungle Plant Room",
    JakAndDaxterSubLevel.SENTINEL_BEACH_CANNON_TOWER: "Sentinel Beach Cannon Tower",
    JakAndDaxterSubLevel.PRECURSOR_BASIN_BLUE_RINGS: "Precursor Basin Blue Rings",
    JakAndDaxterSubLevel.BOGGY_SWAMP_FLUT_FLUT: "Boggy Swamp Flut Flut",
    JakAndDaxterSubLevel.MOUNTAIN_PASS_RACE: "Mountain Pass Race",
    JakAndDaxterSubLevel.MOUNTAIN_PASS_SHORTCUT: "Mountain Pass Shortcut",
    JakAndDaxterSubLevel.SNOWY_MOUNTAIN_FLUT_FLUT: "Snowy Mountain Flut Flut",
    JakAndDaxterSubLevel.SNOWY_MOUNTAIN_LURKER_FORT: "Snowy Mountain Lurker Fort",
    JakAndDaxterSubLevel.SNOWY_MOUNTAIN_FROZEN_BOX: "Snowy Mountain Frozen Box",
    JakAndDaxterSubLevel.GOL_AND_MAIAS_CITADEL_ROTATING_TOWER: "Gol and Maia's Citadel Rotating Tower",
    JakAndDaxterSubLevel.GOL_AND_MAIAS_CITADEL_FINAL_BOSS: "Gol and Maia's Citadel Final Boss"
}


class JakAndDaxterRegion(Region):
    game: str = game_name


# Use the original ID's for each item to tell the Region which Locations are available in it.
# You do NOT need to add the item offsets, that will be handled by create_*_locations.
def create_regions(multiworld: MultiWorld, options: JakAndDaxterOptions, player: int):
    create_region(player, multiworld, "Menu")

    region_gr = create_region(player, multiworld, level_table[JakAndDaxterLevel.GEYSER_ROCK])
    create_cell_locations(region_gr, CellLocations.locGR_cellTable)
    create_fly_locations(region_gr, ScoutLocations.locGR_scoutTable)

    region_sv = create_region(player, multiworld, level_table[JakAndDaxterLevel.SANDOVER_VILLAGE])
    create_cell_locations(region_sv, CellLocations.locSV_cellTable)
    create_fly_locations(region_sv, ScoutLocations.locSV_scoutTable)

    region_fj = create_region(player, multiworld, level_table[JakAndDaxterLevel.FORBIDDEN_JUNGLE])
    create_cell_locations(region_fj, {k: CellLocations.locFJ_cellTable[k] for k in {3, 4, 5, 8, 9, 7}})
    create_fly_locations(region_fj, ScoutLocations.locFJ_scoutTable)

    sub_region_fjsr = create_subregion(region_fj, subLevel_table[JakAndDaxterSubLevel.FORBIDDEN_JUNGLE_SWITCH_ROOM])
    create_cell_locations(sub_region_fjsr, {k: CellLocations.locFJ_cellTable[k] for k in {2}})

    sub_region_fjpr = create_subregion(sub_region_fjsr, subLevel_table[JakAndDaxterSubLevel
                                       .FORBIDDEN_JUNGLE_PLANT_ROOM])
    create_cell_locations(sub_region_fjpr, {k: CellLocations.locFJ_cellTable[k] for k in {6}})

    region_sb = create_region(player, multiworld, level_table[JakAndDaxterLevel.SENTINEL_BEACH])
    create_cell_locations(region_sb, {k: CellLocations.locSB_cellTable[k] for k in {15, 17, 16, 18, 21, 22, 20}})
    create_fly_locations(region_sb, ScoutLocations.locSB_scoutTable)

    sub_region_sbct = create_subregion(region_sb, subLevel_table[JakAndDaxterSubLevel.SENTINEL_BEACH_CANNON_TOWER])
    create_cell_locations(sub_region_sbct, {k: CellLocations.locSB_cellTable[k] for k in {19}})

    region_mi = create_region(player, multiworld, level_table[JakAndDaxterLevel.MISTY_ISLAND])
    create_cell_locations(region_mi, CellLocations.locMI_cellTable)
    create_fly_locations(region_mi, ScoutLocations.locMI_scoutTable)

    region_fc = create_region(player, multiworld, level_table[JakAndDaxterLevel.FIRE_CANYON])
    create_cell_locations(region_fc, CellLocations.locFC_cellTable)
    create_fly_locations(region_fc, ScoutLocations.locFC_scoutTable)

    region_rv = create_region(player, multiworld, level_table[JakAndDaxterLevel.ROCK_VILLAGE])
    create_cell_locations(region_rv, CellLocations.locRV_cellTable)
    create_fly_locations(region_rv, ScoutLocations.locRV_scoutTable)

    region_pb = create_region(player, multiworld, level_table[JakAndDaxterLevel.PRECURSOR_BASIN])
    create_cell_locations(region_pb, {k: CellLocations.locPB_cellTable[k] for k in {54, 53, 52, 56, 55, 58, 57}})
    create_fly_locations(region_pb, ScoutLocations.locPB_scoutTable)

    sub_region_pbbr = create_subregion(region_pb, subLevel_table[JakAndDaxterSubLevel.PRECURSOR_BASIN_BLUE_RINGS])
    create_cell_locations(sub_region_pbbr, {k: CellLocations.locPB_cellTable[k] for k in {59}})

    region_lpc = create_region(player, multiworld, level_table[JakAndDaxterLevel.LOST_PRECURSOR_CITY])
    create_cell_locations(region_lpc, CellLocations.locLPC_cellTable)
    create_fly_locations(region_lpc, ScoutLocations.locLPC_scoutTable)

    region_bs = create_region(player, multiworld, level_table[JakAndDaxterLevel.BOGGY_SWAMP])
    create_cell_locations(region_bs, {k: CellLocations.locBS_cellTable[k] for k in {36, 38, 39, 40, 41, 42}})
    create_fly_locations(region_bs, {k: ScoutLocations.locBS_scoutTable[k] for k in {164, 165, 166, 167, 170}})

    sub_region_bsff = create_subregion(region_bs, subLevel_table[JakAndDaxterSubLevel.BOGGY_SWAMP_FLUT_FLUT])
    create_cell_locations(sub_region_bsff, {k: CellLocations.locBS_cellTable[k] for k in {43, 37}})
    create_fly_locations(sub_region_bsff, {k: ScoutLocations.locBS_scoutTable[k] for k in {168, 169}})

    region_mp = create_region(player, multiworld, level_table[JakAndDaxterLevel.MOUNTAIN_PASS])
    create_cell_locations(region_mp, {k: CellLocations.locMP_cellTable[k] for k in {86}})

    sub_region_mpr = create_subregion(region_mp, subLevel_table[JakAndDaxterSubLevel.MOUNTAIN_PASS_RACE])
    create_cell_locations(sub_region_mpr, {k: CellLocations.locMP_cellTable[k] for k in {87, 88}})
    create_fly_locations(sub_region_mpr, ScoutLocations.locMP_scoutTable)

    sub_region_mps = create_subregion(sub_region_mpr, subLevel_table[JakAndDaxterSubLevel.MOUNTAIN_PASS_SHORTCUT])
    create_cell_locations(sub_region_mps, {k: CellLocations.locMP_cellTable[k] for k in {110}})

    region_vc = create_region(player, multiworld, level_table[JakAndDaxterLevel.VOLCANIC_CRATER])
    create_cell_locations(region_vc, CellLocations.locVC_cellTable)
    create_fly_locations(region_vc, ScoutLocations.locVC_scoutTable)

    region_sc = create_region(player, multiworld, level_table[JakAndDaxterLevel.SPIDER_CAVE])
    create_cell_locations(region_sc, CellLocations.locSC_cellTable)
    create_fly_locations(region_sc, ScoutLocations.locSC_scoutTable)

    region_sm = create_region(player, multiworld, level_table[JakAndDaxterLevel.SNOWY_MOUNTAIN])
    create_cell_locations(region_sm, {k: CellLocations.locSM_cellTable[k] for k in {60, 61, 66, 64}})
    create_fly_locations(region_sm, {k: ScoutLocations.locSM_scoutTable[k] for k in {192, 193, 194, 195, 196}})

    sub_region_smfb = create_subregion(region_sm, subLevel_table[JakAndDaxterSubLevel.SNOWY_MOUNTAIN_FROZEN_BOX])
    create_cell_locations(sub_region_smfb, {k: CellLocations.locSM_cellTable[k] for k in {67}})

    sub_region_smff = create_subregion(region_sm, subLevel_table[JakAndDaxterSubLevel.SNOWY_MOUNTAIN_FLUT_FLUT])
    create_cell_locations(sub_region_smff, {k: CellLocations.locSM_cellTable[k] for k in {63}})

    sub_region_smlf = create_subregion(region_sm, subLevel_table[JakAndDaxterSubLevel.SNOWY_MOUNTAIN_LURKER_FORT])
    create_cell_locations(sub_region_smlf, {k: CellLocations.locSM_cellTable[k] for k in {62, 65}})
    create_fly_locations(sub_region_smlf, {k: ScoutLocations.locSM_scoutTable[k] for k in {197, 198}})

    region_lt = create_region(player, multiworld, level_table[JakAndDaxterLevel.LAVA_TUBE])
    create_cell_locations(region_lt, CellLocations.locLT_cellTable)
    create_fly_locations(region_lt, ScoutLocations.locLT_scoutTable)

    region_gmc = create_region(player, multiworld, level_table[JakAndDaxterLevel.GOL_AND_MAIAS_CITADEL])
    create_cell_locations(region_gmc, {k: CellLocations.locGMC_cellTable[k] for k in {71, 72, 73}})
    create_fly_locations(region_gmc, {k: ScoutLocations.locGMC_scoutTable[k] for k in {206, 207, 208, 209, 210, 211}})

    sub_region_gmcrt = create_subregion(region_gmc, subLevel_table[JakAndDaxterSubLevel
                                        .GOL_AND_MAIAS_CITADEL_ROTATING_TOWER])
    create_cell_locations(sub_region_gmcrt, {k: CellLocations.locGMC_cellTable[k] for k in {70, 91}})
    create_fly_locations(sub_region_gmcrt, {k: ScoutLocations.locGMC_scoutTable[k] for k in {212}})

    create_subregion(sub_region_gmcrt, subLevel_table[JakAndDaxterSubLevel.GOL_AND_MAIAS_CITADEL_FINAL_BOSS])


def create_region(player: int, multiworld: MultiWorld, name: str) -> JakAndDaxterRegion:
    region = JakAndDaxterRegion(name, player, multiworld)
    multiworld.regions.append(region)
    return region


def create_subregion(parent: Region, name: str) -> JakAndDaxterRegion:
    region = JakAndDaxterRegion(name, parent.player, parent.multiworld)
    parent.multiworld.regions.append(region)
    return region


def create_cell_locations(region: Region, locations: typing.Dict[int, str]):
    region.locations += [JakAndDaxterLocation(region.player,
                                              location_table[game_id + cell_offset + loc],
                                              game_id + cell_offset + loc,
                                              region) for loc in locations]


def create_fly_locations(region: Region, locations: typing.Dict[int, str]):
    region.locations += [JakAndDaxterLocation(region.player,
                                              location_table[game_id + fly_offset + loc],
                                              game_id + fly_offset + loc,
                                              region) for loc in locations]
