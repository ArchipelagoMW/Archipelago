from BaseClasses import MultiWorld
from .Options import JakAndDaxterOptions
from .Regions import Jak1Level, Jak1SubLevel, level_table, subLevel_table
from .Locations import location_table as item_table
from .locs import CellLocations as Cells, ScoutLocations as Scouts


def set_rules(multiworld: MultiWorld, options: JakAndDaxterOptions, player: int):
    # Setting up some useful variables here because the offset numbers can get confusing
    # for access rules. Feel free to add more variables here to keep the code more readable.
    # You DO need to convert the game ID's to AP ID's here.
    gr_cells = {Cells.to_ap_id(k) for k in Cells.locGR_cellTable}
    fj_temple_top = Cells.to_ap_id(4)
    fj_blue_switch = Cells.to_ap_id(2)
    fj_plant_boss = Cells.to_ap_id(6)
    fj_fisherman = Cells.to_ap_id(5)
    sb_flut_flut = Cells.to_ap_id(17)
    fc_end = Cells.to_ap_id(69)
    pb_purple_rings = Cells.to_ap_id(58)
    lpc_sunken = Cells.to_ap_id(47)
    lpc_helix = Cells.to_ap_id(50)
    mp_klaww = Cells.to_ap_id(86)
    mp_end = Cells.to_ap_id(87)
    sm_yellow_switch = Cells.to_ap_id(60)
    sm_fort_gate = Cells.to_ap_id(63)
    lt_end = Cells.to_ap_id(89)
    gmc_blue_sage = Cells.to_ap_id(71)
    gmc_red_sage = Cells.to_ap_id(72)
    gmc_yellow_sage = Cells.to_ap_id(73)
    gmc_green_sage = Cells.to_ap_id(70)

    # Start connecting regions and set their access rules.
    connect_start(multiworld, player, Jak1Level.GEYSER_ROCK)

    connect_regions(multiworld, player,
                    Jak1Level.GEYSER_ROCK,
                    Jak1Level.SANDOVER_VILLAGE,
                    lambda state: state.has_all({item_table[k] for k in gr_cells}, player))

    connect_regions(multiworld, player,
                    Jak1Level.SANDOVER_VILLAGE,
                    Jak1Level.FORBIDDEN_JUNGLE)

    connect_region_to_sub(multiworld, player,
                          Jak1Level.FORBIDDEN_JUNGLE,
                          Jak1SubLevel.FORBIDDEN_JUNGLE_SWITCH_ROOM,
                          lambda state: state.has(item_table[fj_temple_top], player))

    connect_subregions(multiworld, player,
                       Jak1SubLevel.FORBIDDEN_JUNGLE_SWITCH_ROOM,
                       Jak1SubLevel.FORBIDDEN_JUNGLE_PLANT_ROOM,
                       lambda state: state.has(item_table[fj_blue_switch], player))

    connect_sub_to_region(multiworld, player,
                          Jak1SubLevel.FORBIDDEN_JUNGLE_PLANT_ROOM,
                          Jak1Level.FORBIDDEN_JUNGLE,
                          lambda state: state.has(item_table[fj_plant_boss], player))

    connect_regions(multiworld, player,
                    Jak1Level.SANDOVER_VILLAGE,
                    Jak1Level.SENTINEL_BEACH)

    connect_region_to_sub(multiworld, player,
                          Jak1Level.SENTINEL_BEACH,
                          Jak1SubLevel.SENTINEL_BEACH_CANNON_TOWER,
                          lambda state: state.has(item_table[fj_blue_switch], player))

    connect_regions(multiworld, player,
                    Jak1Level.SANDOVER_VILLAGE,
                    Jak1Level.MISTY_ISLAND,
                    lambda state: state.has(item_table[fj_fisherman], player))

    connect_regions(multiworld, player,
                    Jak1Level.SANDOVER_VILLAGE,
                    Jak1Level.FIRE_CANYON,
                    lambda state: state.count_group("Power Cell", player) >= 20)

    connect_regions(multiworld, player,
                    Jak1Level.FIRE_CANYON,
                    Jak1Level.ROCK_VILLAGE,
                    lambda state: state.has(item_table[fc_end], player))

    connect_regions(multiworld, player,
                    Jak1Level.ROCK_VILLAGE,
                    Jak1Level.PRECURSOR_BASIN)

    connect_region_to_sub(multiworld, player,
                          Jak1Level.PRECURSOR_BASIN,
                          Jak1SubLevel.PRECURSOR_BASIN_BLUE_RINGS,
                          lambda state: state.has(item_table[pb_purple_rings], player))

    connect_regions(multiworld, player,
                    Jak1Level.ROCK_VILLAGE,
                    Jak1Level.LOST_PRECURSOR_CITY)

    connect_region_to_sub(multiworld, player,
                          Jak1Level.LOST_PRECURSOR_CITY,
                          Jak1SubLevel.LOST_PRECURSOR_CITY_SUNKEN_ROOM)

    connect_subregions(multiworld, player,
                       Jak1SubLevel.LOST_PRECURSOR_CITY_SUNKEN_ROOM,
                       Jak1SubLevel.LOST_PRECURSOR_CITY_HELIX_ROOM)

    connect_sub_to_region(multiworld, player,
                          Jak1SubLevel.LOST_PRECURSOR_CITY_HELIX_ROOM,
                          Jak1Level.LOST_PRECURSOR_CITY,
                          lambda state: state.has(item_table[lpc_helix], player))

    connect_sub_to_region(multiworld, player,
                          Jak1SubLevel.LOST_PRECURSOR_CITY_SUNKEN_ROOM,
                          Jak1Level.ROCK_VILLAGE,
                          lambda state: state.has(item_table[lpc_sunken], player))

    connect_regions(multiworld, player,
                    Jak1Level.ROCK_VILLAGE,
                    Jak1Level.BOGGY_SWAMP)

    connect_region_to_sub(multiworld, player,
                          Jak1Level.BOGGY_SWAMP,
                          Jak1SubLevel.BOGGY_SWAMP_FLUT_FLUT,
                          lambda state: state.has(item_table[sb_flut_flut], player))

    connect_regions(multiworld, player,
                    Jak1Level.ROCK_VILLAGE,
                    Jak1Level.MOUNTAIN_PASS,
                    lambda state: state.count_group("Power Cell", player) >= 45)

    connect_region_to_sub(multiworld, player,
                          Jak1Level.MOUNTAIN_PASS,
                          Jak1SubLevel.MOUNTAIN_PASS_RACE,
                          lambda state: state.has(item_table[mp_klaww], player))

    connect_subregions(multiworld, player,
                       Jak1SubLevel.MOUNTAIN_PASS_RACE,
                       Jak1SubLevel.MOUNTAIN_PASS_SHORTCUT,
                       lambda state: state.has(item_table[sm_yellow_switch], player))

    connect_sub_to_region(multiworld, player,
                          Jak1SubLevel.MOUNTAIN_PASS_RACE,
                          Jak1Level.VOLCANIC_CRATER,
                          lambda state: state.has(item_table[mp_end], player))

    connect_regions(multiworld, player,
                    Jak1Level.VOLCANIC_CRATER,
                    Jak1Level.SPIDER_CAVE)

    connect_regions(multiworld, player,
                    Jak1Level.VOLCANIC_CRATER,
                    Jak1Level.SNOWY_MOUNTAIN)

    connect_region_to_sub(multiworld, player,
                          Jak1Level.SNOWY_MOUNTAIN,
                          Jak1SubLevel.SNOWY_MOUNTAIN_FROZEN_BOX,
                          lambda state: state.has(item_table[sm_yellow_switch], player))

    connect_region_to_sub(multiworld, player,
                          Jak1Level.SNOWY_MOUNTAIN,
                          Jak1SubLevel.SNOWY_MOUNTAIN_FLUT_FLUT,
                          lambda state: state.has(item_table[sb_flut_flut], player))

    connect_region_to_sub(multiworld, player,
                          Jak1Level.SNOWY_MOUNTAIN,
                          Jak1SubLevel.SNOWY_MOUNTAIN_LURKER_FORT,
                          lambda state: state.has(item_table[sm_fort_gate], player))

    connect_regions(multiworld, player,
                    Jak1Level.VOLCANIC_CRATER,
                    Jak1Level.LAVA_TUBE,
                    lambda state: state.count_group("Power Cell", player) >= 72)

    connect_regions(multiworld, player,
                    Jak1Level.LAVA_TUBE,
                    Jak1Level.GOL_AND_MAIAS_CITADEL,
                    lambda state: state.has(item_table[lt_end], player))

    connect_region_to_sub(multiworld, player,
                          Jak1Level.GOL_AND_MAIAS_CITADEL,
                          Jak1SubLevel.GOL_AND_MAIAS_CITADEL_ROTATING_TOWER,
                          lambda state: state.has(item_table[gmc_blue_sage], player)
                          and state.has(item_table[gmc_red_sage], player)
                          and state.has(item_table[gmc_yellow_sage], player))

    connect_subregions(multiworld, player,
                       Jak1SubLevel.GOL_AND_MAIAS_CITADEL_ROTATING_TOWER,
                       Jak1SubLevel.GOL_AND_MAIAS_CITADEL_FINAL_BOSS,
                       lambda state: state.has(item_table[gmc_green_sage], player))

    multiworld.completion_condition[player] = lambda state: state.can_reach(
        multiworld.get_region(subLevel_table[Jak1SubLevel.GOL_AND_MAIAS_CITADEL_FINAL_BOSS], player),
        "Region",
        player)


def connect_start(multiworld: MultiWorld, player: int, target: Jak1Level):
    menu_region = multiworld.get_region("Menu", player)
    start_region = multiworld.get_region(level_table[target], player)
    menu_region.connect(start_region)


def connect_regions(multiworld: MultiWorld, player: int, source: Jak1Level, target: Jak1Level, rule=None):
    source_region = multiworld.get_region(level_table[source], player)
    target_region = multiworld.get_region(level_table[target], player)
    source_region.connect(target_region, rule=rule)


def connect_region_to_sub(multiworld: MultiWorld, player: int, source: Jak1Level, target: Jak1SubLevel, rule=None):
    source_region = multiworld.get_region(level_table[source], player)
    target_region = multiworld.get_region(subLevel_table[target], player)
    source_region.connect(target_region, rule=rule)


def connect_sub_to_region(multiworld: MultiWorld, player: int, source: Jak1SubLevel, target: Jak1Level, rule=None):
    source_region = multiworld.get_region(subLevel_table[source], player)
    target_region = multiworld.get_region(level_table[target], player)
    source_region.connect(target_region, rule=rule)


def connect_subregions(multiworld: MultiWorld, player: int, source: Jak1SubLevel, target: Jak1SubLevel, rule=None):
    source_region = multiworld.get_region(subLevel_table[source], player)
    target_region = multiworld.get_region(subLevel_table[target], player)
    source_region.connect(target_region, rule=rule)
