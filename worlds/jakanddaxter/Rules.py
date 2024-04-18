from BaseClasses import MultiWorld
from .GameID import game_id, cell_offset, fly_offset
from .Options import JakAndDaxterOptions
from .Regions import JakAndDaxterLevel, JakAndDaxterSubLevel, level_table, subLevel_table
from .Locations import location_table as item_table
from .locs.CellLocations import locGR_cellTable


def set_rules(multiworld: MultiWorld, options: JakAndDaxterOptions, player: int):
    # Setting up some useful variables here because the offset numbers can get confusing
    # for access rules. Feel free to add more variables here to keep the code more readable.
    gr_cells = {game_id + cell_offset + k for k in locGR_cellTable}
    fj_temple_top = game_id + cell_offset + 4
    fj_blue_switch = game_id + cell_offset + 2
    fj_plant_boss = game_id + cell_offset + 6
    fj_fisherman = game_id + cell_offset + 5
    sb_flut_flut = game_id + cell_offset + 17
    fc_end = game_id + cell_offset + 69
    pb_purple_rings = game_id + cell_offset + 58
    lpc_sunken = game_id + cell_offset + 47
    lpc_helix = game_id + cell_offset + 50
    mp_klaww = game_id + cell_offset + 86
    mp_end = game_id + cell_offset + 87
    sm_yellow_switch = game_id + cell_offset + 60
    sm_fort_gate = game_id + cell_offset + 63
    lt_end = game_id + cell_offset + 89
    gmc_blue_sage = game_id + cell_offset + 71
    gmc_red_sage = game_id + cell_offset + 72
    gmc_yellow_sage = game_id + cell_offset + 73
    gmc_green_sage = game_id + cell_offset + 70

    # Start connecting regions and set their access rules.
    connect_start(multiworld, player, JakAndDaxterLevel.GEYSER_ROCK)

    connect_regions(multiworld, player,
                    JakAndDaxterLevel.GEYSER_ROCK,
                    JakAndDaxterLevel.SANDOVER_VILLAGE,
                    lambda state: state.has_all({item_table[k] for k in gr_cells}, player))

    connect_regions(multiworld, player,
                    JakAndDaxterLevel.SANDOVER_VILLAGE,
                    JakAndDaxterLevel.FORBIDDEN_JUNGLE)

    connect_region_to_sub(multiworld, player,
                          JakAndDaxterLevel.FORBIDDEN_JUNGLE,
                          JakAndDaxterSubLevel.FORBIDDEN_JUNGLE_SWITCH_ROOM,
                          lambda state: state.has(item_table[fj_temple_top], player))

    connect_subregions(multiworld, player,
                       JakAndDaxterSubLevel.FORBIDDEN_JUNGLE_SWITCH_ROOM,
                       JakAndDaxterSubLevel.FORBIDDEN_JUNGLE_PLANT_ROOM,
                       lambda state: state.has(item_table[fj_blue_switch], player))

    connect_sub_to_region(multiworld, player,
                          JakAndDaxterSubLevel.FORBIDDEN_JUNGLE_PLANT_ROOM,
                          JakAndDaxterLevel.FORBIDDEN_JUNGLE,
                          lambda state: state.has(item_table[fj_plant_boss], player))

    connect_regions(multiworld, player,
                    JakAndDaxterLevel.SANDOVER_VILLAGE,
                    JakAndDaxterLevel.SENTINEL_BEACH)

    connect_region_to_sub(multiworld, player,
                          JakAndDaxterLevel.SENTINEL_BEACH,
                          JakAndDaxterSubLevel.SENTINEL_BEACH_CANNON_TOWER,
                          lambda state: state.has(item_table[fj_blue_switch], player))

    connect_regions(multiworld, player,
                    JakAndDaxterLevel.SANDOVER_VILLAGE,
                    JakAndDaxterLevel.MISTY_ISLAND,
                    lambda state: state.has(item_table[fj_fisherman], player))

    connect_regions(multiworld, player,
                    JakAndDaxterLevel.SANDOVER_VILLAGE,
                    JakAndDaxterLevel.FIRE_CANYON,
                    lambda state: state.count_group("Power Cell", player) >= 20)

    connect_regions(multiworld, player,
                    JakAndDaxterLevel.FIRE_CANYON,
                    JakAndDaxterLevel.ROCK_VILLAGE,
                    lambda state: state.has(item_table[fc_end], player))

    connect_regions(multiworld, player,
                    JakAndDaxterLevel.ROCK_VILLAGE,
                    JakAndDaxterLevel.PRECURSOR_BASIN)

    connect_region_to_sub(multiworld, player,
                          JakAndDaxterLevel.PRECURSOR_BASIN,
                          JakAndDaxterSubLevel.PRECURSOR_BASIN_BLUE_RINGS,
                          lambda state: state.has(item_table[pb_purple_rings], player))

    connect_regions(multiworld, player,
                    JakAndDaxterLevel.ROCK_VILLAGE,
                    JakAndDaxterLevel.LOST_PRECURSOR_CITY)

    connect_region_to_sub(multiworld, player,
                          JakAndDaxterLevel.LOST_PRECURSOR_CITY,
                          JakAndDaxterSubLevel.LOST_PRECURSOR_CITY_SUNKEN_ROOM)

    connect_subregions(multiworld, player,
                       JakAndDaxterSubLevel.LOST_PRECURSOR_CITY_SUNKEN_ROOM,
                       JakAndDaxterSubLevel.LOST_PRECURSOR_CITY_HELIX_ROOM)

    connect_sub_to_region(multiworld, player,
                          JakAndDaxterSubLevel.LOST_PRECURSOR_CITY_HELIX_ROOM,
                          JakAndDaxterLevel.LOST_PRECURSOR_CITY,
                          lambda state: state.has(item_table[lpc_helix], player))

    connect_sub_to_region(multiworld, player,
                          JakAndDaxterSubLevel.LOST_PRECURSOR_CITY_SUNKEN_ROOM,
                          JakAndDaxterLevel.ROCK_VILLAGE,
                          lambda state: state.has(item_table[lpc_sunken], player))

    connect_regions(multiworld, player,
                    JakAndDaxterLevel.ROCK_VILLAGE,
                    JakAndDaxterLevel.BOGGY_SWAMP)

    connect_region_to_sub(multiworld, player,
                          JakAndDaxterLevel.BOGGY_SWAMP,
                          JakAndDaxterSubLevel.BOGGY_SWAMP_FLUT_FLUT,
                          lambda state: state.has(item_table[sb_flut_flut], player))

    connect_regions(multiworld, player,
                    JakAndDaxterLevel.ROCK_VILLAGE,
                    JakAndDaxterLevel.MOUNTAIN_PASS,
                    lambda state: state.count_group("Power Cell", player) >= 45)

    connect_region_to_sub(multiworld, player,
                          JakAndDaxterLevel.MOUNTAIN_PASS,
                          JakAndDaxterSubLevel.MOUNTAIN_PASS_RACE,
                          lambda state: state.has(item_table[mp_klaww], player))

    connect_subregions(multiworld, player,
                       JakAndDaxterSubLevel.MOUNTAIN_PASS_RACE,
                       JakAndDaxterSubLevel.MOUNTAIN_PASS_SHORTCUT,
                       lambda state: state.has(item_table[sm_yellow_switch], player))

    connect_sub_to_region(multiworld, player,
                          JakAndDaxterSubLevel.MOUNTAIN_PASS_RACE,
                          JakAndDaxterLevel.VOLCANIC_CRATER,
                          lambda state: state.has(item_table[mp_end], player))

    connect_regions(multiworld, player,
                    JakAndDaxterLevel.VOLCANIC_CRATER,
                    JakAndDaxterLevel.SPIDER_CAVE)

    connect_regions(multiworld, player,
                    JakAndDaxterLevel.VOLCANIC_CRATER,
                    JakAndDaxterLevel.SNOWY_MOUNTAIN)

    connect_region_to_sub(multiworld, player,
                          JakAndDaxterLevel.SNOWY_MOUNTAIN,
                          JakAndDaxterSubLevel.SNOWY_MOUNTAIN_FROZEN_BOX,
                          lambda state: state.has(item_table[sm_yellow_switch], player))

    connect_region_to_sub(multiworld, player,
                          JakAndDaxterLevel.SNOWY_MOUNTAIN,
                          JakAndDaxterSubLevel.SNOWY_MOUNTAIN_FLUT_FLUT,
                          lambda state: state.has(item_table[sb_flut_flut], player))

    connect_region_to_sub(multiworld, player,
                          JakAndDaxterLevel.SNOWY_MOUNTAIN,
                          JakAndDaxterSubLevel.SNOWY_MOUNTAIN_LURKER_FORT,
                          lambda state: state.has(item_table[sm_fort_gate], player))

    connect_regions(multiworld, player,
                    JakAndDaxterLevel.VOLCANIC_CRATER,
                    JakAndDaxterLevel.LAVA_TUBE,
                    lambda state: state.count_group("Power Cell", player) >= 72)

    connect_regions(multiworld, player,
                    JakAndDaxterLevel.LAVA_TUBE,
                    JakAndDaxterLevel.GOL_AND_MAIAS_CITADEL,
                    lambda state: state.has(item_table[lt_end], player))

    connect_region_to_sub(multiworld, player,
                          JakAndDaxterLevel.GOL_AND_MAIAS_CITADEL,
                          JakAndDaxterSubLevel.GOL_AND_MAIAS_CITADEL_ROTATING_TOWER,
                          lambda state: state.has(item_table[gmc_blue_sage], player)
                          and state.has(item_table[gmc_red_sage], player)
                          and state.has(item_table[gmc_yellow_sage], player))

    connect_subregions(multiworld, player,
                       JakAndDaxterSubLevel.GOL_AND_MAIAS_CITADEL_ROTATING_TOWER,
                       JakAndDaxterSubLevel.GOL_AND_MAIAS_CITADEL_FINAL_BOSS,
                       lambda state: state.has(item_table[gmc_green_sage], player))

    multiworld.completion_condition[player] = lambda state: state.can_reach(
        multiworld.get_region(subLevel_table[JakAndDaxterSubLevel.GOL_AND_MAIAS_CITADEL_FINAL_BOSS], player),
        "Region",
        player)


def connect_start(multiworld: MultiWorld, player: int, target: JakAndDaxterLevel):
    menu_region = multiworld.get_region("Menu", player)
    start_region = multiworld.get_region(level_table[target], player)
    menu_region.connect(start_region)


def connect_regions(multiworld: MultiWorld, player: int, source: JakAndDaxterLevel, target: JakAndDaxterLevel,
                    rule=None):
    source_region = multiworld.get_region(level_table[source], player)
    target_region = multiworld.get_region(level_table[target], player)
    source_region.connect(target_region, rule=rule)


def connect_region_to_sub(multiworld: MultiWorld, player: int, source: JakAndDaxterLevel, target: JakAndDaxterSubLevel,
                          rule=None):
    source_region = multiworld.get_region(level_table[source], player)
    target_region = multiworld.get_region(subLevel_table[target], player)
    source_region.connect(target_region, rule=rule)


def connect_sub_to_region(multiworld: MultiWorld, player: int, source: JakAndDaxterSubLevel, target: JakAndDaxterLevel,
                          rule=None):
    source_region = multiworld.get_region(subLevel_table[source], player)
    target_region = multiworld.get_region(level_table[target], player)
    source_region.connect(target_region, rule=rule)


def connect_subregions(multiworld: MultiWorld, player: int, source: JakAndDaxterSubLevel, target: JakAndDaxterSubLevel,
                       rule=None):
    source_region = multiworld.get_region(subLevel_table[source], player)
    target_region = multiworld.get_region(subLevel_table[target], player)
    source_region.connect(target_region, rule=rule)
