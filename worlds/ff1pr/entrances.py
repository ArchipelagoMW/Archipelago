from typing import List, Dict, NamedTuple
from enum import IntEnum
from .data import regnames, entnames

class EntGroup(IntEnum):
    Region = 0,
    OverworldDungeon = 1,
    OverworldTown = 2,
    InnerDungeon = 3,
    ChaosShrine = 4,
    Fixed = 5,

class EntranceData (NamedTuple):
    name: str
    region: str
    target_point: str
    target_region: str
    type: int
    group: str
    deadend: bool = False
    access_req: bool = False

global_entrances: List[EntranceData] = [
    EntranceData(entnames.overworld_cornelia, regnames.cornelia_region, entnames.cornelia_entrance, regnames.cornelia, EntGroup.Fixed, entnames.overworld_cornelia, True),
    EntranceData(entnames.overworld_pravoka, regnames.pravoka_region, entnames.pravoka_entrance, regnames.pravoka, EntGroup.OverworldTown, entnames.overworld_pravoka, True),
    EntranceData(entnames.overworld_elfheim, regnames.innersea_region, entnames.elfheim_entrance, regnames.elfheim, EntGroup.OverworldTown, entnames.overworld_elfheim, True),
    EntranceData(entnames.overworld_melmond, regnames.melmond_region, entnames.melmond_entrance, regnames.melmond, EntGroup.OverworldTown, entnames.overworld_melmond, True),
    EntranceData(entnames.overworld_crescent_lake, regnames.crescent_region, entnames.crescent_lake_entrance, regnames.crescent_lake, EntGroup.OverworldTown, entnames.overworld_crescent_lake, True),
    EntranceData(entnames.overworld_onrac, regnames.onrac_region, entnames.onrac_entrance, regnames.onrac, EntGroup.OverworldTown, entnames.overworld_onrac, True),
    EntranceData(entnames.overworld_gaia, regnames.gaia_region, entnames.gaia_entrance, regnames.gaia, EntGroup.OverworldTown, entnames.overworld_gaia, True),
    EntranceData(entnames.overworld_lufenia, regnames.lufenia_region, entnames.lufenia_entrance, regnames.lufenia, EntGroup.OverworldTown, entnames.overworld_lufenia, True),

    EntranceData(entnames.overworld_castle_cornelia, regnames.cornelia_region, entnames.castle_cornelia_1f_entrance, regnames.castle_cornelia_1f, EntGroup.OverworldDungeon, entnames.overworld_castle_cornelia),
    EntranceData(entnames.overworld_chaos_shrine, regnames.cornelia_region, entnames.chaos_shrine_entrance, regnames.chaos_shrine, EntGroup.OverworldDungeon, entnames.overworld_chaos_shrine, True),
    EntranceData(entnames.overworld_matoyas_cave, regnames.pravoka_region, entnames.matoyas_cave_entrance, regnames.matoyas_cave, EntGroup.OverworldDungeon, entnames.overworld_matoyas_cave, True),
    EntranceData(entnames.overworld_mount_duergar, regnames.innersea_region, entnames.mount_duergar_entrance, regnames.mount_duergar, EntGroup.OverworldDungeon, entnames.overworld_mount_duergar, True),
    EntranceData(entnames.overworld_elven_castle, regnames.innersea_region, entnames.elven_castle_entrance, regnames.elven_castle, EntGroup.OverworldDungeon, entnames.overworld_elven_castle, True),
    EntranceData(entnames.overworld_western_keep, regnames.innersea_region, entnames.western_keep_entrance, regnames.western_keep, EntGroup.OverworldDungeon, entnames.overworld_western_keep, True),
    EntranceData(entnames.overworld_marsh_cave, regnames.innersea_region, entnames.marsh_cave_b1_entrance, regnames.marsh_cave_b1, EntGroup.OverworldDungeon, entnames.overworld_marsh_cave),
    EntranceData(entnames.overworld_cavern_of_earth, regnames.melmond_region, entnames.cavern_of_earth_b1_center_stairs, regnames.cavern_of_earth_b1, EntGroup.OverworldDungeon, entnames.overworld_cavern_of_earth),
    EntranceData(entnames.overworld_giants_cavern_east, regnames.melmond_region, entnames.giants_cavern_east_entrance, regnames.giants_cavern, EntGroup.OverworldDungeon, entnames.overworld_giants_cavern_east, True),
    EntranceData(entnames.overworld_giants_cavern_west, regnames.sage_region, entnames.giants_cavern_west_entrance, regnames.giants_cavern, EntGroup.OverworldDungeon, entnames.overworld_giants_cavern_west, True),
    EntranceData(entnames.overworld_sages_cave, regnames.sage_region, entnames.sages_cave_entrance, regnames.sages_cave, EntGroup.OverworldDungeon, entnames.overworld_sages_cave, True),
    EntranceData(entnames.overworld_mount_gulg, regnames.gulg_region, entnames.mount_gulg_b1_right_stairs, regnames.mount_gulg_b1, EntGroup.OverworldDungeon, entnames.overworld_mount_gulg),
    EntranceData(entnames.overworld_cavern_of_ice, regnames.ice_region, entnames.cavern_of_ice_b1_entrance_top_stairs, regnames.cavern_of_ice_b1_entrance, EntGroup.OverworldDungeon, entnames.overworld_cavern_of_ice),
    EntranceData(entnames.overworld_dragon_caves_plains, regnames.dragon_plains_island, entnames.dragon_caves_plains_entrance, regnames.dragon_caves_plains, EntGroup.OverworldDungeon, entnames.overworld_dragon_caves_plains, True),
    EntranceData(entnames.overworld_dragon_caves_top, regnames.bahamuts_island, entnames.dragon_caves_top_entrance, regnames.dragon_caves_top, EntGroup.OverworldDungeon, entnames.overworld_dragon_caves_top, True),
    EntranceData(entnames.overworld_dragon_caves_marsh, regnames.dragon_marsh_island, entnames.dragon_caves_marsh_entrance, regnames.dragon_caves_marsh, EntGroup.OverworldDungeon, entnames.overworld_dragon_caves_marsh, True),
    EntranceData(entnames.overworld_dragon_caves_small, regnames.dragon_small_island, entnames.dragon_caves_small_entrance, regnames.dragon_caves_small, EntGroup.OverworldDungeon, entnames.overworld_dragon_caves_small, True),
    EntranceData(entnames.overworld_dragon_caves_forest, regnames.dragon_forest_island, entnames.dragon_caves_forest_entrance, regnames.dragon_caves_forest, EntGroup.OverworldDungeon, entnames.overworld_dragon_caves_forest, True),
    EntranceData(entnames.overworld_dragon_caves_bahamut, regnames.bahamuts_island, entnames.dragon_caves_bahamut_entrance, regnames.dragon_caves_bahamut_corridor, EntGroup.OverworldDungeon, entnames.overworld_dragon_caves_bahamut),
    EntranceData(entnames.overworld_citadel_of_trials, regnames.trials_region, entnames.citadel_of_trials_1f_entrance, regnames.citadel_of_trials_1f, EntGroup.OverworldDungeon, entnames.overworld_citadel_of_trials, True),
    EntranceData(entnames.overworld_caravan, regnames.onrac_region, entnames.caravan_entrance, regnames.caravan_outside, EntGroup.OverworldDungeon, entnames.overworld_caravan),
    EntranceData(entnames.overworld_waterfall, regnames.onrac_region, entnames.waterfall_entrance, regnames.waterfall, EntGroup.OverworldDungeon, entnames.overworld_waterfall, True, True),
    EntranceData(entnames.overworld_mirage_tower, regnames.mirage_desert, entnames.mirage_tower_1f_right_stairs, regnames.mirage_tower_1f, EntGroup.OverworldDungeon, entnames.overworld_mirage_tower, False, True),

    EntranceData(entnames.castle_cornelia_1f_stairs, regnames.castle_cornelia_1f, entnames.castle_cornelia_2f_stairs, regnames.castle_cornelia_2f, EntGroup.InnerDungeon, entnames.overworld_castle_cornelia, True),
    EntranceData(entnames.dragon_caves_bahamut_bottom_stairs, regnames.dragon_caves_bahamut_corridor, entnames.dragon_caves_bahamut_bahamut_hall, regnames.dragon_caves_bahamut_hall, EntGroup.InnerDungeon, entnames.overworld_dragon_caves_bahamut, True),
    EntranceData(entnames.onrac_submarine_dock, regnames.onrac, entnames.sunken_shrine_3f_split_bottom_stairs, regnames.sunken_shrine_3f_split, EntGroup.Fixed, entnames.overworld_onrac, False, True),
    EntranceData(entnames.caravan_outside_tent, regnames.caravan_outside, entnames.caravan_inside_tent, regnames.caravan_tent, EntGroup.InnerDungeon, entnames.overworld_caravan, True),
    EntranceData(entnames.chaos_shrine_black_orb_warp, regnames.chaos_shrine, entnames.chaos_shrine_1f_center_warp, regnames.chaos_shrine_1f_entrance, EntGroup.Fixed, entnames.overworld_chaos_shrine, False, True),
    EntranceData(entnames.marsh_cave_b1_top_stairs, regnames.marsh_cave_b1, entnames.marsh_cave_b2_entrance, regnames.marsh_cave_b2_top, EntGroup.InnerDungeon, entnames.overworld_marsh_cave, True),
    EntranceData(entnames.marsh_cave_b1_bottom_stairs, regnames.marsh_cave_b1, entnames.marsh_cave_b2_upper_stairs, regnames.marsh_cave_b2_bottom, EntGroup.InnerDungeon, entnames.overworld_marsh_cave),
    EntranceData(entnames.marsh_cave_b2_lower_stairs, regnames.marsh_cave_b2_bottom, entnames.marsh_cave_b3_entrance, regnames.marsh_cave_b3, EntGroup.InnerDungeon, entnames.overworld_marsh_cave, True),
    EntranceData(entnames.cavern_of_earth_b1_right_stairs, regnames.cavern_of_earth_b1, entnames.cavern_of_earth_b2_left_stairs, regnames.cavern_of_earth_b2, EntGroup.InnerDungeon, entnames.overworld_cavern_of_earth),
    EntranceData(entnames.cavern_of_earth_b2_right_stairs, regnames.cavern_of_earth_b2, entnames.cavern_of_earth_b3_bottom_stairs, regnames.cavern_of_earth_b3, EntGroup.InnerDungeon, entnames.overworld_cavern_of_earth),
    EntranceData(entnames.cavern_of_earth_b3_center_stairs, regnames.cavern_of_earth_b3, entnames.cavern_of_earth_b4_right_stairs, regnames.cavern_of_earth_b4, EntGroup.InnerDungeon, entnames.overworld_cavern_of_earth, False, True),
    EntranceData(entnames.cavern_of_earth_b4_left_stairs, regnames.cavern_of_earth_b4, entnames.cavern_of_earth_b5_bottom_stairs, regnames.cavern_of_earth_b5, EntGroup.InnerDungeon, entnames.overworld_cavern_of_earth, True),
    EntranceData(entnames.mount_gulg_b1_left_stairs, regnames.mount_gulg_b1, entnames.mount_gulg_b2_right_stairs, regnames.mount_gulg_b2, EntGroup.InnerDungeon, entnames.overworld_mount_gulg),
    EntranceData(entnames.mount_gulg_b2_left_stairs, regnames.mount_gulg_b2, entnames.mount_gulg_b3_corridor_middle_stairs, regnames.mount_gulg_b3_corridor, EntGroup.InnerDungeon, entnames.overworld_mount_gulg),
    EntranceData(entnames.mount_gulg_b3_corridor_right_stairs, regnames.mount_gulg_b3_corridor, entnames.mount_gulg_b4_squares_top_stairs, regnames.mount_gulg_b4_squares, EntGroup.InnerDungeon, entnames.overworld_mount_gulg),
    EntranceData(entnames.mount_gulg_b4_squares_bottom_stairs, regnames.mount_gulg_b4_squares, entnames.mount_gulg_b3_maze_top_stairs, regnames.mount_gulg_b3_maze, EntGroup.InnerDungeon, entnames.overworld_mount_gulg),
    EntranceData(entnames.mount_gulg_b3_maze_bottom_stairs, regnames.mount_gulg_b3_maze, entnames.mount_gulg_b4_agama_top_stairs, regnames.mount_gulg_b4_agama, EntGroup.InnerDungeon, entnames.overworld_mount_gulg),
    EntranceData(entnames.mount_gulg_b4_agama_bottom_stairs, regnames.mount_gulg_b4_agama, entnames.mount_gulg_b5_center_stairs, regnames.mount_gulg_b5, EntGroup.InnerDungeon, entnames.overworld_mount_gulg, True),
    EntranceData(entnames.cavern_of_ice_b1_entrance_bottom_stairs, regnames.cavern_of_ice_b1_entrance, entnames.cavern_of_ice_b2_square_top_stairs, regnames.cavern_of_ice_b2_square, EntGroup.InnerDungeon, entnames.overworld_cavern_of_ice),
    EntranceData(entnames.cavern_of_ice_b2_square_bottom_stairs, regnames.cavern_of_ice_b2_square, entnames.cavern_of_ice_b3_small_top_stairs, regnames.cavern_of_ice_b3_small, EntGroup.InnerDungeon, entnames.overworld_cavern_of_ice),
    EntranceData(entnames.cavern_of_ice_b3_small_bottom_stairs, regnames.cavern_of_ice_b3_small, entnames.cavern_of_ice_b2_room_entrance, regnames.cavern_of_ice_b2_room, EntGroup.InnerDungeon, entnames.overworld_cavern_of_ice, True),
    EntranceData(entnames.cavern_of_ice_b2_room_hole, regnames.cavern_of_ice_b2_room, entnames.cavern_of_ice_b3_treasury_trap_room, regnames.cavern_of_ice_b3_treasury, EntGroup.Fixed, entnames.overworld_cavern_of_ice),
    EntranceData(entnames.cavern_of_ice_b3_treasury_right_stairs, regnames.cavern_of_ice_b3_treasury, entnames.cavern_of_ice_b1_backdoor_left_stairs, regnames.cavern_of_ice_b1_backdoor, EntGroup.Fixed, entnames.overworld_cavern_of_ice),
    EntranceData(entnames.cavern_of_ice_b1_backdoor_hole, regnames.cavern_of_ice_b1_backdoor, entnames.cavern_of_ice_b2_room_ledge, regnames.cavern_of_ice_b2_ledge, EntGroup.Fixed, entnames.overworld_cavern_of_ice),
    EntranceData(entnames.citadel_of_trials_1f_throne, regnames.citadel_of_trials_1f, entnames.citadel_of_trials_2f_maze, regnames.citadel_of_trials_2f, EntGroup.Fixed, entnames.overworld_citadel_of_trials,True, True),
    EntranceData(entnames.sunken_shrine_3f_split_right_stairs, regnames.sunken_shrine_3f_split, entnames.sunken_shrine_4f_tfc_top_stairs, regnames.sunken_shrine_4f_tfc, EntGroup.InnerDungeon, "Sunken Shrine"),
    EntranceData(entnames.sunken_shrine_4f_tfc_bottom_stairs, regnames.sunken_shrine_4f_tfc, entnames.sunken_shrine_5f_center_stairs, regnames.sunken_shrine_5f, EntGroup.InnerDungeon, "Sunken Shrine", True),
    EntranceData(entnames.sunken_shrine_3f_split_left_stairs, regnames.sunken_shrine_3f_split, entnames.sunken_shrine_2f_sunken_city_bottom_stairs, regnames.sunken_shrine_2f_sunken_city, EntGroup.InnerDungeon, "Sunken Shrine"),
    EntranceData(entnames.sunken_shrine_2f_sunken_city_top_stairs, regnames.sunken_shrine_2f_sunken_city, entnames.sunken_shrine_3f_small_bottom_stairs, regnames.sunken_shrine_3f_small, EntGroup.InnerDungeon, "Sunken Shrine"),
    EntranceData(entnames.sunken_shrine_3f_small_top_stairs, regnames.sunken_shrine_3f_small, entnames.sunken_shrine_4f_square_top_stairs, regnames.sunken_shrine_4f_square, EntGroup.InnerDungeon, "Sunken Shrine"),
    EntranceData(entnames.sunken_shrine_4f_square_bottom_stairs, regnames.sunken_shrine_4f_square, entnames.sunken_shrine_3f_vertical_top_stairs, regnames.sunken_shrine_3f_vertical, EntGroup.InnerDungeon, "Sunken Shrine"),
    EntranceData(entnames.sunken_shrine_3f_vertical_bottom_stairs, regnames.sunken_shrine_3f_vertical, entnames.sunken_shrine_2f_sharknado_right_stairs, regnames.sunken_shrine_2f_sharknado, EntGroup.InnerDungeon, "Sunken Shrine"),
    EntranceData(entnames.sunken_shrine_2f_sharknado_left_stairs, regnames.sunken_shrine_2f_sharknado, entnames.sunken_shrine_1f_bottom_stairs, regnames.sunken_shrine_1f, EntGroup.InnerDungeon, "Sunken Shrine", True),
    EntranceData(entnames.mirage_tower_1f_left_stairs, regnames.mirage_tower_1f, entnames.mirage_tower_2f_bottom_stairs, regnames.mirage_tower_2f, EntGroup.InnerDungeon, entnames.overworld_mirage_tower),
    EntranceData(entnames.mirage_tower_2f_top_stairs, regnames.mirage_tower_2f, entnames.mirage_tower_3f_top_stairs, regnames.mirage_tower_3f, EntGroup.InnerDungeon, entnames.overworld_mirage_tower),
    EntranceData(entnames.mirage_tower_3f_center_warp, regnames.mirage_tower_3f, entnames.flying_fortress_1f_center_warp, regnames.flying_fortress_1f, EntGroup.InnerDungeon, entnames.overworld_mirage_tower, False, True),
    EntranceData(entnames.flying_fortress_1f_top_warp, regnames.flying_fortress_1f, entnames.flying_fortress_2f_top_warp, regnames.flying_fortress_2f, EntGroup.InnerDungeon, entnames.overworld_mirage_tower),
    EntranceData(entnames.flying_fortress_2f_bottom_warp, regnames.flying_fortress_2f, entnames.flying_fortress_3f_center_warp, regnames.flying_fortress_3f, EntGroup.InnerDungeon, entnames.overworld_mirage_tower),
    EntranceData(entnames.flying_fortress_3f_left_warp, regnames.flying_fortress_3f, entnames.flying_fortress_4f_entrance_warp, regnames.flying_fortress_4f, EntGroup.InnerDungeon, entnames.overworld_mirage_tower),
    EntranceData(entnames.flying_fortress_4f_exit_warp, regnames.flying_fortress_4f, entnames.flying_fortress_5f_bottom_warp, regnames.flying_fortress_5f, EntGroup.InnerDungeon, entnames.overworld_mirage_tower, True),
    EntranceData(entnames.chaos_shrine_1f_entrance_left_stairs, regnames.chaos_shrine_1f_entrance, entnames.chaos_shrine_b1_deadend_dead_end_stairs, regnames.chaos_shrine_b1_deadend, EntGroup.ChaosShrine, "Chaos Shrine", True),
    EntranceData(entnames.chaos_shrine_1f_entrance_right_stairs, regnames.chaos_shrine_1f_entrance, entnames.chaos_shrine_2f_corridor_left_stairs, regnames.chaos_shrine_2f_corridor, EntGroup.ChaosShrine, "Chaos Shrine"),
    EntranceData(entnames.chaos_shrine_2f_corridor_right_stairs, regnames.chaos_shrine_2f_corridor, entnames.chaos_shrine_3f_plaza_left_stairs, regnames.chaos_shrine_3f_plaza, EntGroup.ChaosShrine, "Chaos Shrine"),
    EntranceData(entnames.chaos_shrine_3f_plaza_center_stairs, regnames.chaos_shrine_3f_plaza, entnames.chaos_shrine_2f_plaza_center_stairs, regnames.chaos_shrine_2f_plaza, EntGroup.ChaosShrine, "Chaos Shrine", False, True),
    EntranceData(entnames.chaos_shrine_2f_plaza_left_stairs, regnames.chaos_shrine_2f_plaza, entnames.chaos_shrine_1f_corridor_right_stairs, regnames.chaos_shrine_1f_corridor, EntGroup.ChaosShrine, "Chaos Shrine"),
    EntranceData(entnames.chaos_shrine_1f_corridor_left_stairs, regnames.chaos_shrine_1f_corridor, entnames.chaos_shrine_b1_earth_left_stairs, regnames.chaos_shrine_b1_earth, EntGroup.ChaosShrine, "Chaos Shrine"),
    EntranceData(entnames.chaos_shrine_b1_earth_right_stairs, regnames.chaos_shrine_b1_earth, entnames.chaos_shrine_b2_left_stairs, regnames.chaos_shrine_b2, EntGroup.ChaosShrine, "Chaos Shrine"),
    EntranceData(entnames.chaos_shrine_b2_right_stairs, regnames.chaos_shrine_b2, entnames.chaos_shrine_b3_top_stairs, regnames.chaos_shrine_b3, EntGroup.ChaosShrine, "Chaos Shrine"),
    EntranceData(entnames.chaos_shrine_b3_bottom_stairs, regnames.chaos_shrine_b3, entnames.chaos_shrine_b4_left_stairs, regnames.chaos_shrine_b4, EntGroup.ChaosShrine, "Chaos Shrine"),
    EntranceData(entnames.chaos_shrine_b4_right_stairs, regnames.chaos_shrine_b4, entnames.chaos_shrine_b5_top_stairs, regnames.chaos_shrine_b5, EntGroup.ChaosShrine, "Chaos Shrine", True),
]

innersea_entrances: List[str] = [
    entnames.overworld_cornelia,
    entnames.overworld_castle_cornelia,
    entnames.overworld_chaos_shrine,
    entnames.overworld_matoyas_cave,
    entnames.overworld_pravoka,
    entnames.overworld_mount_duergar,
    entnames.overworld_western_keep,
    entnames.overworld_marsh_cave,
    entnames.overworld_elven_castle,
    entnames.overworld_elfheim,
    entnames.overworld_cavern_of_ice,
    entnames.overworld_mount_gulg,
    entnames.overworld_crescent_lake,
]

town_entrances: List[str] = [
    entnames.overworld_pravoka,
    entnames.overworld_elfheim,
    entnames.overworld_melmond,
    entnames.overworld_crescent_lake,
    entnames.overworld_onrac,
    entnames.overworld_gaia,
    entnames.overworld_lufenia
]

safe_entrances_overworld_only: List[str] = [
    entnames.overworld_chaos_shrine,
    entnames.overworld_matoyas_cave,
    entnames.overworld_dragon_caves_marsh,
    entnames.overworld_dragon_caves_plains,
    entnames.overworld_dragon_caves_forest,
]

safe_entrances = safe_entrances_overworld_only + [entnames.sunken_shrine_4f_tfc_bottom_stairs]

safe_overworld_entrances_early: List[str] = [
    entnames.overworld_chaos_shrine,
    entnames.overworld_castle_cornelia,
    entnames.overworld_matoyas_cave,
]

safe_overworld_entrances_west: List[str] = [
    entnames.overworld_chaos_shrine,
    entnames.overworld_castle_cornelia,
    entnames.overworld_mount_duergar
]

internal_dungeons: List[str] = [
    entnames.overworld_marsh_cave,
    entnames.overworld_cavern_of_earth,
    entnames.overworld_mount_gulg,
    entnames.overworld_cavern_of_ice,
    "Sunken Shrine",
    entnames.overworld_mirage_tower
]

internal_dungeons_ext: List[str] = [
    entnames.overworld_waterfall,
    entnames.overworld_citadel_of_trials,
    *internal_dungeons
]

split_regions: List[str] = [
    regnames.marsh_cave_b1,
    regnames.sunken_shrine_3f_split,
    regnames.chaos_shrine_1f_entrance
]
titan_regions: Dict[str, List[str]] = {
    regnames.innersea_region: [entnames.overworld_cornelia, entnames.overworld_chaos_shrine, entnames.overworld_matoyas_cave, entnames.overworld_pravoka, entnames.overworld_mount_duergar, entnames.overworld_western_keep, entnames.overworld_marsh_cave, entnames.overworld_elfheim, entnames.overworld_elven_castle, entnames.overworld_crescent_lake, entnames.overworld_mount_gulg, entnames.overworld_cavern_of_ice],
    regnames.melmond_region: [entnames.overworld_melmond, entnames.overworld_cavern_of_earth, entnames.overworld_giants_cavern_east],
    regnames.sage_region: [entnames.overworld_sages_cave, entnames.overworld_giants_cavern_west],
    regnames.onrac_region: [entnames.overworld_onrac, entnames.overworld_caravan, entnames.overworld_waterfall],
    regnames.bahamuts_island: [entnames.overworld_dragon_caves_bahamut, entnames.overworld_dragon_caves_top]
}




