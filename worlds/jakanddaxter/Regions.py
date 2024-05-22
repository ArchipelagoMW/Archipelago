import typing
from enum import Enum, auto
from BaseClasses import MultiWorld, Region
from .GameID import jak1_name
from .JakAndDaxterOptions import JakAndDaxterOptions
from .Locations import JakAndDaxterLocation, location_table
from .locs import CellLocations as Cells, ScoutLocations as Scouts, SpecialLocations as Specials


class JakAndDaxterRegion(Region):
    game: str = jak1_name


# Holds information like the level name, the number of orbs available there, etc. Applies to both Levels and SubLevels.
# We especially need orb_counts to be tracked here because we need to know how many orbs you have access to
# in order to know when you can afford the 90-orb and 120-orb payments for more checks.
class Jak1LevelInfo:
    name: str
    orb_count: int

    def __init__(self, name: str, orb_count: int):
        self.name = name
        self.orb_count = orb_count


class Jak1Level(int, Enum):
    SCOUT_FLY_POWER_CELLS = auto()  # This is a virtual location to reward you receiving 7 scout flies.
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
    FORBIDDEN_JUNGLE_SWITCH_ROOM = auto()
    FORBIDDEN_JUNGLE_PLANT_ROOM = auto()
    SENTINEL_BEACH_CANNON_TOWER = auto()
    ROCK_VILLAGE_PONTOON_BRIDGE = auto()
    BOGGY_SWAMP_FLUT_FLUT = auto()
    MOUNTAIN_PASS_SHORTCUT = auto()
    SNOWY_MOUNTAIN_FLUT_FLUT = auto()
    SNOWY_MOUNTAIN_LURKER_FORT = auto()
    SNOWY_MOUNTAIN_FROZEN_BOX = auto()
    GOL_AND_MAIAS_CITADEL_ROTATING_TOWER = auto()
    GOL_AND_MAIAS_CITADEL_FINAL_BOSS = auto()


level_table: typing.Dict[Jak1Level, Jak1LevelInfo] = {
    Jak1Level.SCOUT_FLY_POWER_CELLS:
        Jak1LevelInfo("Scout Fly Power Cells", 0),  # Virtual location.
    Jak1Level.GEYSER_ROCK:
        Jak1LevelInfo("Geyser Rock", 50),
    Jak1Level.SANDOVER_VILLAGE:
        Jak1LevelInfo("Sandover Village", 50),
    Jak1Level.FORBIDDEN_JUNGLE:
        Jak1LevelInfo("Forbidden Jungle", 99),
    Jak1Level.SENTINEL_BEACH:
        Jak1LevelInfo("Sentinel Beach", 128),
    Jak1Level.MISTY_ISLAND:
        Jak1LevelInfo("Misty Island", 150),
    Jak1Level.FIRE_CANYON:
        Jak1LevelInfo("Fire Canyon", 50),
    Jak1Level.ROCK_VILLAGE:
        Jak1LevelInfo("Rock Village", 43),
    Jak1Level.PRECURSOR_BASIN:
        Jak1LevelInfo("Precursor Basin", 200),
    Jak1Level.LOST_PRECURSOR_CITY:
        Jak1LevelInfo("Lost Precursor City", 200),
    Jak1Level.BOGGY_SWAMP:
        Jak1LevelInfo("Boggy Swamp", 177),
    Jak1Level.MOUNTAIN_PASS:
        Jak1LevelInfo("Mountain Pass", 50),
    Jak1Level.VOLCANIC_CRATER:
        Jak1LevelInfo("Volcanic Crater", 50),
    Jak1Level.SPIDER_CAVE:
        Jak1LevelInfo("Spider Cave", 200),
    Jak1Level.SNOWY_MOUNTAIN:
        Jak1LevelInfo("Snowy Mountain", 113),
    Jak1Level.LAVA_TUBE:
        Jak1LevelInfo("Lava Tube", 50),
    Jak1Level.GOL_AND_MAIAS_CITADEL:
        Jak1LevelInfo("Gol and Maia's Citadel", 180),
}

sub_level_table: typing.Dict[Jak1SubLevel, Jak1LevelInfo] = {
    Jak1SubLevel.FORBIDDEN_JUNGLE_SWITCH_ROOM:
        Jak1LevelInfo("Forbidden Jungle Switch Room", 24),
    Jak1SubLevel.FORBIDDEN_JUNGLE_PLANT_ROOM:
        Jak1LevelInfo("Forbidden Jungle Plant Room", 27),
    Jak1SubLevel.SENTINEL_BEACH_CANNON_TOWER:
        Jak1LevelInfo("Sentinel Beach Cannon Tower", 22),
    Jak1SubLevel.ROCK_VILLAGE_PONTOON_BRIDGE:
        Jak1LevelInfo("Rock Village Pontoon Bridge", 7),
    Jak1SubLevel.BOGGY_SWAMP_FLUT_FLUT:
        Jak1LevelInfo("Boggy Swamp Flut Flut", 23),
    Jak1SubLevel.MOUNTAIN_PASS_SHORTCUT:
        Jak1LevelInfo("Mountain Pass Shortcut", 0),
    Jak1SubLevel.SNOWY_MOUNTAIN_FLUT_FLUT:
        Jak1LevelInfo("Snowy Mountain Flut Flut", 15),
    Jak1SubLevel.SNOWY_MOUNTAIN_LURKER_FORT:
        Jak1LevelInfo("Snowy Mountain Lurker Fort", 72),
    Jak1SubLevel.SNOWY_MOUNTAIN_FROZEN_BOX:
        Jak1LevelInfo("Snowy Mountain Frozen Box", 0),
    Jak1SubLevel.GOL_AND_MAIAS_CITADEL_ROTATING_TOWER:
        Jak1LevelInfo("Gol and Maia's Citadel Rotating Tower", 20),
    Jak1SubLevel.GOL_AND_MAIAS_CITADEL_FINAL_BOSS:
        Jak1LevelInfo("Gol and Maia's Citadel Final Boss", 0),
}


# Use the original game ID's for each item to tell the Region which Locations are available in it.
# You do NOT need to add the item offsets or game ID, that will be handled by create_*_locations.
def create_regions(multiworld: MultiWorld, options: JakAndDaxterOptions, player: int):

    # Always start with Menu.
    multiworld.regions.append(JakAndDaxterRegion("Menu", player, multiworld))

    region_7sf = create_region(player, multiworld, Jak1Level.SCOUT_FLY_POWER_CELLS)
    create_cell_locations(region_7sf, Cells.loc7SF_cellTable)

    region_gr = create_region(player, multiworld, Jak1Level.GEYSER_ROCK)
    create_cell_locations(region_gr, Cells.locGR_cellTable)
    create_fly_locations(region_gr, Scouts.locGR_scoutTable)

    region_sv = create_region(player, multiworld, Jak1Level.SANDOVER_VILLAGE)
    create_cell_locations(region_sv, Cells.locSV_cellTable)
    create_fly_locations(region_sv, Scouts.locSV_scoutTable)

    region_fj = create_region(player, multiworld, Jak1Level.FORBIDDEN_JUNGLE)
    create_cell_locations(region_fj, {k: Cells.locFJ_cellTable[k] for k in {3, 4, 5, 8, 9}})
    create_fly_locations(region_fj, Scouts.locFJ_scoutTable)
    create_special_locations(region_fj, {k: Specials.loc_specialTable[k] for k in {4, 5}})

    sub_region_fjsr = create_subregion(region_fj, Jak1SubLevel.FORBIDDEN_JUNGLE_SWITCH_ROOM)
    create_cell_locations(sub_region_fjsr, {k: Cells.locFJ_cellTable[k] for k in {2}})
    create_special_locations(sub_region_fjsr, {k: Specials.loc_specialTable[k] for k in {2}})

    sub_region_fjpr = create_subregion(sub_region_fjsr, Jak1SubLevel.FORBIDDEN_JUNGLE_PLANT_ROOM)
    create_cell_locations(sub_region_fjpr, {k: Cells.locFJ_cellTable[k] for k in {6}})

    region_sb = create_region(player, multiworld, Jak1Level.SENTINEL_BEACH)
    create_cell_locations(region_sb, {k: Cells.locSB_cellTable[k] for k in {15, 17, 16, 18, 21, 22}})
    create_fly_locations(region_sb, Scouts.locSB_scoutTable)
    create_special_locations(region_sb, {k: Specials.loc_specialTable[k] for k in {17}})

    sub_region_sbct = create_subregion(region_sb, Jak1SubLevel.SENTINEL_BEACH_CANNON_TOWER)
    create_cell_locations(sub_region_sbct, {k: Cells.locSB_cellTable[k] for k in {19}})

    region_mi = create_region(player, multiworld, Jak1Level.MISTY_ISLAND)
    create_cell_locations(region_mi, Cells.locMI_cellTable)
    create_fly_locations(region_mi, Scouts.locMI_scoutTable)

    region_fc = create_region(player, multiworld, Jak1Level.FIRE_CANYON)
    create_cell_locations(region_fc, Cells.locFC_cellTable)
    create_fly_locations(region_fc, Scouts.locFC_scoutTable)

    region_rv = create_region(player, multiworld, Jak1Level.ROCK_VILLAGE)
    create_cell_locations(region_rv, Cells.locRV_cellTable)
    create_fly_locations(region_rv, {k: Scouts.locRV_scoutTable[k]
                                     for k in {76, 131148, 196684, 262220, 65612, 327756}})
    create_special_locations(region_rv, {k: Specials.loc_specialTable[k] for k in {33}})

    sub_region_rvpb = create_subregion(region_rv, Jak1SubLevel.ROCK_VILLAGE_PONTOON_BRIDGE)
    create_fly_locations(sub_region_rvpb, {k: Scouts.locRV_scoutTable[k] for k in {393292}})

    region_pb = create_region(player, multiworld, Jak1Level.PRECURSOR_BASIN)
    create_cell_locations(region_pb, Cells.locPB_cellTable)
    create_fly_locations(region_pb, Scouts.locPB_scoutTable)

    region_lpc = create_region(player, multiworld, Jak1Level.LOST_PRECURSOR_CITY)
    create_cell_locations(region_lpc, Cells.locLPC_cellTable)
    create_fly_locations(region_lpc, Scouts.locLPC_scoutTable)

    region_bs = create_region(player, multiworld, Jak1Level.BOGGY_SWAMP)
    create_cell_locations(region_bs, {k: Cells.locBS_cellTable[k] for k in {36, 38, 39, 40, 41, 42}})
    create_fly_locations(region_bs, {k: Scouts.locBS_scoutTable[k] for k in {43, 393259, 65579, 262187, 196651}})

    sub_region_bsff = create_subregion(region_bs, Jak1SubLevel.BOGGY_SWAMP_FLUT_FLUT)
    create_cell_locations(sub_region_bsff, {k: Cells.locBS_cellTable[k] for k in {37}})
    create_fly_locations(sub_region_bsff, {k: Scouts.locBS_scoutTable[k] for k in {327723, 131115}})

    region_mp = create_region(player, multiworld, Jak1Level.MOUNTAIN_PASS)
    create_cell_locations(region_mp, {k: Cells.locMP_cellTable[k] for k in {86, 87}})
    create_fly_locations(region_mp, Scouts.locMP_scoutTable)

    sub_region_mps = create_subregion(region_mp, Jak1SubLevel.MOUNTAIN_PASS_SHORTCUT)
    create_cell_locations(sub_region_mps, {k: Cells.locMP_cellTable[k] for k in {110}})

    region_vc = create_region(player, multiworld, Jak1Level.VOLCANIC_CRATER)
    create_cell_locations(region_vc, Cells.locVC_cellTable)
    create_fly_locations(region_vc, Scouts.locVC_scoutTable)
    create_special_locations(region_vc, {k: Specials.loc_specialTable[k] for k in {105}})

    region_sc = create_region(player, multiworld, Jak1Level.SPIDER_CAVE)
    create_cell_locations(region_sc, Cells.locSC_cellTable)
    create_fly_locations(region_sc, Scouts.locSC_scoutTable)

    region_sm = create_region(player, multiworld, Jak1Level.SNOWY_MOUNTAIN)
    create_cell_locations(region_sm, {k: Cells.locSM_cellTable[k] for k in {60, 61, 66, 64}})
    create_fly_locations(region_sm, {k: Scouts.locSM_scoutTable[k] for k in {65, 327745, 65601, 131137, 393281}})
    create_special_locations(region_sm, {k: Specials.loc_specialTable[k] for k in {60}})

    sub_region_smfb = create_subregion(region_sm, Jak1SubLevel.SNOWY_MOUNTAIN_FROZEN_BOX)
    create_cell_locations(sub_region_smfb, {k: Cells.locSM_cellTable[k] for k in {67}})

    sub_region_smff = create_subregion(region_sm, Jak1SubLevel.SNOWY_MOUNTAIN_FLUT_FLUT)
    create_cell_locations(sub_region_smff, {k: Cells.locSM_cellTable[k] for k in {63}})
    create_special_locations(sub_region_smff, {k: Specials.loc_specialTable[k] for k in {63}})

    sub_region_smlf = create_subregion(region_sm, Jak1SubLevel.SNOWY_MOUNTAIN_LURKER_FORT)
    create_cell_locations(sub_region_smlf, {k: Cells.locSM_cellTable[k] for k in {62}})
    create_fly_locations(sub_region_smlf, {k: Scouts.locSM_scoutTable[k] for k in {196673, 262209}})

    region_lt = create_region(player, multiworld, Jak1Level.LAVA_TUBE)
    create_cell_locations(region_lt, Cells.locLT_cellTable)
    create_fly_locations(region_lt, Scouts.locLT_scoutTable)

    region_gmc = create_region(player, multiworld, Jak1Level.GOL_AND_MAIAS_CITADEL)
    create_cell_locations(region_gmc, {k: Cells.locGMC_cellTable[k] for k in {71, 72, 73}})
    create_fly_locations(region_gmc, {k: Scouts.locGMC_scoutTable[k]
                                      for k in {91, 65627, 196699, 262235, 393307, 131163}})
    create_special_locations(region_gmc, {k: Specials.loc_specialTable[k] for k in {71, 72, 73}})

    sub_region_gmcrt = create_subregion(region_gmc, Jak1SubLevel.GOL_AND_MAIAS_CITADEL_ROTATING_TOWER)
    create_cell_locations(sub_region_gmcrt, {k: Cells.locGMC_cellTable[k] for k in {70}})
    create_fly_locations(sub_region_gmcrt, {k: Scouts.locGMC_scoutTable[k] for k in {327771}})
    create_special_locations(sub_region_gmcrt, {k: Specials.loc_specialTable[k] for k in {70}})

    create_subregion(sub_region_gmcrt, Jak1SubLevel.GOL_AND_MAIAS_CITADEL_FINAL_BOSS)


def create_region(player: int, multiworld: MultiWorld, level: Jak1Level) -> JakAndDaxterRegion:
    name = level_table[level].name
    region = JakAndDaxterRegion(name, player, multiworld)
    multiworld.regions.append(region)
    return region


def create_subregion(parent: Region, sub_level: Jak1SubLevel) -> JakAndDaxterRegion:
    name = sub_level_table[sub_level].name
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


# Special Locations should be matched alongside their respective Power Cell Locations,
# so you get 2 unlocks for these rather than 1.
def create_special_locations(region: Region, locations: typing.Dict[int, str]):
    region.locations += [JakAndDaxterLocation(region.player,
                                              location_table[Specials.to_ap_id(loc)],
                                              Specials.to_ap_id(loc),
                                              region) for loc in locations]
