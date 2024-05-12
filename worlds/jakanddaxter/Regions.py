import typing
from enum import Enum, auto
from BaseClasses import MultiWorld, Region
from .GameID import jak1_name
from .JakAndDaxterOptions import JakAndDaxterOptions
from .Locations import JakAndDaxterLocation, location_table
from .locs import CellLocations as Cells, ScoutLocations as Scouts


class Jak1Level(int, Enum):
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


class Jak1SubLevel(int, Enum):
    MAIN_AREA = auto()
    FORBIDDEN_JUNGLE_SWITCH_ROOM = auto()
    FORBIDDEN_JUNGLE_PLANT_ROOM = auto()
    SENTINEL_BEACH_CANNON_TOWER = auto()
    PRECURSOR_BASIN_BLUE_RINGS = auto()
    LOST_PRECURSOR_CITY_SUNKEN_ROOM = auto()
    LOST_PRECURSOR_CITY_HELIX_ROOM = auto()
    BOGGY_SWAMP_FLUT_FLUT = auto()
    MOUNTAIN_PASS_RACE = auto()
    MOUNTAIN_PASS_SHORTCUT = auto()
    SNOWY_MOUNTAIN_FLUT_FLUT = auto()
    SNOWY_MOUNTAIN_LURKER_FORT = auto()
    SNOWY_MOUNTAIN_FROZEN_BOX = auto()
    GOL_AND_MAIAS_CITADEL_ROTATING_TOWER = auto()
    GOL_AND_MAIAS_CITADEL_FINAL_BOSS = auto()


level_table: typing.Dict[Jak1Level, str] = {
    Jak1Level.GEYSER_ROCK: "Geyser Rock",
    Jak1Level.SANDOVER_VILLAGE: "Sandover Village",
    Jak1Level.FORBIDDEN_JUNGLE: "Forbidden Jungle",
    Jak1Level.SENTINEL_BEACH: "Sentinel Beach",
    Jak1Level.MISTY_ISLAND: "Misty Island",
    Jak1Level.FIRE_CANYON: "Fire Canyon",
    Jak1Level.ROCK_VILLAGE: "Rock Village",
    Jak1Level.PRECURSOR_BASIN: "Precursor Basin",
    Jak1Level.LOST_PRECURSOR_CITY: "Lost Precursor City",
    Jak1Level.BOGGY_SWAMP: "Boggy Swamp",
    Jak1Level.MOUNTAIN_PASS: "Mountain Pass",
    Jak1Level.VOLCANIC_CRATER: "Volcanic Crater",
    Jak1Level.SPIDER_CAVE: "Spider Cave",
    Jak1Level.SNOWY_MOUNTAIN: "Snowy Mountain",
    Jak1Level.LAVA_TUBE: "Lava Tube",
    Jak1Level.GOL_AND_MAIAS_CITADEL: "Gol and Maia's Citadel"
}

subLevel_table: typing.Dict[Jak1SubLevel, str] = {
    Jak1SubLevel.MAIN_AREA: "Main Area",
    Jak1SubLevel.FORBIDDEN_JUNGLE_SWITCH_ROOM: "Forbidden Jungle Switch Room",
    Jak1SubLevel.FORBIDDEN_JUNGLE_PLANT_ROOM: "Forbidden Jungle Plant Room",
    Jak1SubLevel.SENTINEL_BEACH_CANNON_TOWER: "Sentinel Beach Cannon Tower",
    Jak1SubLevel.PRECURSOR_BASIN_BLUE_RINGS: "Precursor Basin Blue Rings",
    Jak1SubLevel.LOST_PRECURSOR_CITY_SUNKEN_ROOM: "Lost Precursor City Sunken Room",
    Jak1SubLevel.LOST_PRECURSOR_CITY_HELIX_ROOM: "Lost Precursor City Helix Room",
    Jak1SubLevel.BOGGY_SWAMP_FLUT_FLUT: "Boggy Swamp Flut Flut",
    Jak1SubLevel.MOUNTAIN_PASS_RACE: "Mountain Pass Race",
    Jak1SubLevel.MOUNTAIN_PASS_SHORTCUT: "Mountain Pass Shortcut",
    Jak1SubLevel.SNOWY_MOUNTAIN_FLUT_FLUT: "Snowy Mountain Flut Flut",
    Jak1SubLevel.SNOWY_MOUNTAIN_LURKER_FORT: "Snowy Mountain Lurker Fort",
    Jak1SubLevel.SNOWY_MOUNTAIN_FROZEN_BOX: "Snowy Mountain Frozen Box",
    Jak1SubLevel.GOL_AND_MAIAS_CITADEL_ROTATING_TOWER: "Gol and Maia's Citadel Rotating Tower",
    Jak1SubLevel.GOL_AND_MAIAS_CITADEL_FINAL_BOSS: "Gol and Maia's Citadel Final Boss"
}


class JakAndDaxterRegion(Region):
    game: str = jak1_name


# Use the original game ID's for each item to tell the Region which Locations are available in it.
# You do NOT need to add the item offsets or game ID, that will be handled by create_*_locations.
def create_regions(multiworld: MultiWorld, options: JakAndDaxterOptions, player: int):
    create_region(player, multiworld, "Menu")

    region_gr = create_region(player, multiworld, level_table[Jak1Level.GEYSER_ROCK])
    create_cell_locations(region_gr, Cells.locGR_cellTable)
    create_fly_locations(region_gr, Scouts.locGR_scoutTable)

    region_sv = create_region(player, multiworld, level_table[Jak1Level.SANDOVER_VILLAGE])
    create_cell_locations(region_sv, Cells.locSV_cellTable)
    create_fly_locations(region_sv, Scouts.locSV_scoutTable)

    region_fj = create_region(player, multiworld, level_table[Jak1Level.FORBIDDEN_JUNGLE])
    create_cell_locations(region_fj, {k: Cells.locFJ_cellTable[k] for k in {3, 4, 5, 8, 9, 7}})
    create_fly_locations(region_fj, Scouts.locFJ_scoutTable)

    sub_region_fjsr = create_subregion(region_fj, subLevel_table[Jak1SubLevel.FORBIDDEN_JUNGLE_SWITCH_ROOM])
    create_cell_locations(sub_region_fjsr, {k: Cells.locFJ_cellTable[k] for k in {2}})

    sub_region_fjpr = create_subregion(sub_region_fjsr, subLevel_table[Jak1SubLevel.FORBIDDEN_JUNGLE_PLANT_ROOM])
    create_cell_locations(sub_region_fjpr, {k: Cells.locFJ_cellTable[k] for k in {6}})

    region_sb = create_region(player, multiworld, level_table[Jak1Level.SENTINEL_BEACH])
    create_cell_locations(region_sb, {k: Cells.locSB_cellTable[k] for k in {15, 17, 16, 18, 21, 22, 20}})
    create_fly_locations(region_sb, Scouts.locSB_scoutTable)

    sub_region_sbct = create_subregion(region_sb, subLevel_table[Jak1SubLevel.SENTINEL_BEACH_CANNON_TOWER])
    create_cell_locations(sub_region_sbct, {k: Cells.locSB_cellTable[k] for k in {19}})

    region_mi = create_region(player, multiworld, level_table[Jak1Level.MISTY_ISLAND])
    create_cell_locations(region_mi, Cells.locMI_cellTable)
    create_fly_locations(region_mi, Scouts.locMI_scoutTable)

    region_fc = create_region(player, multiworld, level_table[Jak1Level.FIRE_CANYON])
    create_cell_locations(region_fc, Cells.locFC_cellTable)
    create_fly_locations(region_fc, Scouts.locFC_scoutTable)

    region_rv = create_region(player, multiworld, level_table[Jak1Level.ROCK_VILLAGE])
    create_cell_locations(region_rv, Cells.locRV_cellTable)
    create_fly_locations(region_rv, Scouts.locRV_scoutTable)

    region_pb = create_region(player, multiworld, level_table[Jak1Level.PRECURSOR_BASIN])
    create_cell_locations(region_pb, {k: Cells.locPB_cellTable[k] for k in {54, 53, 52, 56, 55, 58, 57}})
    create_fly_locations(region_pb, Scouts.locPB_scoutTable)

    sub_region_pbbr = create_subregion(region_pb, subLevel_table[Jak1SubLevel.PRECURSOR_BASIN_BLUE_RINGS])
    create_cell_locations(sub_region_pbbr, {k: Cells.locPB_cellTable[k] for k in {59}})

    region_lpc = create_region(player, multiworld, level_table[Jak1Level.LOST_PRECURSOR_CITY])
    create_cell_locations(region_lpc, {k: Cells.locLPC_cellTable[k] for k in {45, 48, 44, 51}})
    create_fly_locations(region_lpc, {k: Scouts.locLPC_scoutTable[k]
                                      for k in {262193, 131121, 393265, 196657, 49, 65585}})

    sub_region_lpcsr = create_subregion(region_lpc, subLevel_table[Jak1SubLevel.LOST_PRECURSOR_CITY_SUNKEN_ROOM])
    create_cell_locations(sub_region_lpcsr, {k: Cells.locLPC_cellTable[k] for k in {47, 49}})
    create_fly_locations(region_lpc, {k: Scouts.locLPC_scoutTable[k] for k in {327729}})

    sub_region_lpchr = create_subregion(region_lpc, subLevel_table[Jak1SubLevel.LOST_PRECURSOR_CITY_HELIX_ROOM])
    create_cell_locations(sub_region_lpchr, {k: Cells.locLPC_cellTable[k] for k in {46, 50}})

    region_bs = create_region(player, multiworld, level_table[Jak1Level.BOGGY_SWAMP])
    create_cell_locations(region_bs, {k: Cells.locBS_cellTable[k] for k in {36, 38, 39, 40, 41, 42}})
    create_fly_locations(region_bs, {k: Scouts.locBS_scoutTable[k] for k in {43, 393259, 65579, 262187, 196651}})

    sub_region_bsff = create_subregion(region_bs, subLevel_table[Jak1SubLevel.BOGGY_SWAMP_FLUT_FLUT])
    create_cell_locations(sub_region_bsff, {k: Cells.locBS_cellTable[k] for k in {43, 37}})
    create_fly_locations(sub_region_bsff, {k: Scouts.locBS_scoutTable[k] for k in {327723, 131115}})

    region_mp = create_region(player, multiworld, level_table[Jak1Level.MOUNTAIN_PASS])
    create_cell_locations(region_mp, {k: Cells.locMP_cellTable[k] for k in {86}})

    sub_region_mpr = create_subregion(region_mp, subLevel_table[Jak1SubLevel.MOUNTAIN_PASS_RACE])
    create_cell_locations(sub_region_mpr, {k: Cells.locMP_cellTable[k] for k in {87, 88}})
    create_fly_locations(sub_region_mpr, Scouts.locMP_scoutTable)

    sub_region_mps = create_subregion(sub_region_mpr, subLevel_table[Jak1SubLevel.MOUNTAIN_PASS_SHORTCUT])
    create_cell_locations(sub_region_mps, {k: Cells.locMP_cellTable[k] for k in {110}})

    region_vc = create_region(player, multiworld, level_table[Jak1Level.VOLCANIC_CRATER])
    create_cell_locations(region_vc, Cells.locVC_cellTable)
    create_fly_locations(region_vc, Scouts.locVC_scoutTable)

    region_sc = create_region(player, multiworld, level_table[Jak1Level.SPIDER_CAVE])
    create_cell_locations(region_sc, Cells.locSC_cellTable)
    create_fly_locations(region_sc, Scouts.locSC_scoutTable)

    region_sm = create_region(player, multiworld, level_table[Jak1Level.SNOWY_MOUNTAIN])
    create_cell_locations(region_sm, {k: Cells.locSM_cellTable[k] for k in {60, 61, 66, 64}})
    create_fly_locations(region_sm, {k: Scouts.locSM_scoutTable[k] for k in {65, 327745, 65601, 131137, 393281}})

    sub_region_smfb = create_subregion(region_sm, subLevel_table[Jak1SubLevel.SNOWY_MOUNTAIN_FROZEN_BOX])
    create_cell_locations(sub_region_smfb, {k: Cells.locSM_cellTable[k] for k in {67}})

    sub_region_smff = create_subregion(region_sm, subLevel_table[Jak1SubLevel.SNOWY_MOUNTAIN_FLUT_FLUT])
    create_cell_locations(sub_region_smff, {k: Cells.locSM_cellTable[k] for k in {63}})

    sub_region_smlf = create_subregion(region_sm, subLevel_table[Jak1SubLevel.SNOWY_MOUNTAIN_LURKER_FORT])
    create_cell_locations(sub_region_smlf, {k: Cells.locSM_cellTable[k] for k in {62, 65}})
    create_fly_locations(sub_region_smlf, {k: Scouts.locSM_scoutTable[k] for k in {196673, 262209}})

    region_lt = create_region(player, multiworld, level_table[Jak1Level.LAVA_TUBE])
    create_cell_locations(region_lt, Cells.locLT_cellTable)
    create_fly_locations(region_lt, Scouts.locLT_scoutTable)

    region_gmc = create_region(player, multiworld, level_table[Jak1Level.GOL_AND_MAIAS_CITADEL])
    create_cell_locations(region_gmc, {k: Cells.locGMC_cellTable[k] for k in {71, 72, 73}})
    create_fly_locations(region_gmc, {k: Scouts.locGMC_scoutTable[k]
                                      for k in {91, 65627, 196699, 262235, 393307, 131163}})

    sub_region_gmcrt = create_subregion(region_gmc, subLevel_table[Jak1SubLevel.GOL_AND_MAIAS_CITADEL_ROTATING_TOWER])
    create_cell_locations(sub_region_gmcrt, {k: Cells.locGMC_cellTable[k] for k in {70, 91}})
    create_fly_locations(sub_region_gmcrt, {k: Scouts.locGMC_scoutTable[k] for k in {327771}})

    create_subregion(sub_region_gmcrt, subLevel_table[Jak1SubLevel.GOL_AND_MAIAS_CITADEL_FINAL_BOSS])


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
                                              location_table[Cells.to_ap_id(loc)],
                                              Cells.to_ap_id(loc),
                                              region) for loc in locations]


def create_fly_locations(region: Region, locations: typing.Dict[int, str]):
    region.locations += [JakAndDaxterLocation(region.player,
                                              location_table[Scouts.to_ap_id(loc)],
                                              Scouts.to_ap_id(loc),
                                              region) for loc in locations]
