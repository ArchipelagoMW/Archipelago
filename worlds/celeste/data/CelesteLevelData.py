from typing import Dict, List
from ..Levels import Level, Room, PreRegion, LevelLocation, RegionConnection, RoomConnection, Door, DoorDirection, LocationType
from ..Names import ItemName

all_doors: Dict[str, Door] = {
    "0a_-1_east": Door("0a_-1_east", "0a_-1", DoorDirection.right, False, False),

    "0a_0_west": Door("0a_0_west", "0a_0", DoorDirection.left, False, False),
    "0a_0_east": Door("0a_0_east", "0a_0", DoorDirection.right, False, False),
    "0a_0_north": Door("0a_0_north", "0a_0", DoorDirection.up, False, False),

    "0a_0b_south": Door("0a_0b_south", "0a_0b", DoorDirection.down, False, False),

    "0a_1_west": Door("0a_1_west", "0a_1", DoorDirection.left, False, False),
    "0a_1_east": Door("0a_1_east", "0a_1", DoorDirection.right, False, False),

    "0a_2_west": Door("0a_2_west", "0a_2", DoorDirection.left, False, False),
    "0a_2_east": Door("0a_2_east", "0a_2", DoorDirection.right, False, False),

    "0a_3_west": Door("0a_3_west", "0a_3", DoorDirection.left, False, False),

    "1a_1_east": Door("1a_1_east", "1a_1", DoorDirection.up, False, False),

    "1a_2_west": Door("1a_2_west", "1a_2", DoorDirection.down, False, True),
    "1a_2_east": Door("1a_2_east", "1a_2", DoorDirection.up, False, False),

    "1a_3_west": Door("1a_3_west", "1a_3", DoorDirection.down, False, True),
    "1a_3_east": Door("1a_3_east", "1a_3", DoorDirection.up, False, False),

    "1a_4_west": Door("1a_4_west", "1a_4", DoorDirection.down, False, True),
    "1a_4_east": Door("1a_4_east", "1a_4", DoorDirection.up, False, False),

    "1a_3b_west": Door("1a_3b_west", "1a_3b", DoorDirection.down, False, True),
    "1a_3b_top": Door("1a_3b_top", "1a_3b", DoorDirection.up, False, False),

    "1a_5_bottom": Door("1a_5_bottom", "1a_5", DoorDirection.down, False, True),
    "1a_5_west": Door("1a_5_west", "1a_5", DoorDirection.left, False, False),
    "1a_5_south-east": Door("1a_5_south-east", "1a_5", DoorDirection.right, True, False),
    "1a_5_top": Door("1a_5_top", "1a_5", DoorDirection.up, False, False),

    "1a_5z_east": Door("1a_5z_east", "1a_5z", DoorDirection.right, False, False),

    "1a_5a_west": Door("1a_5a_west", "1a_5a", DoorDirection.left, False, False),

    "1a_6_south-west": Door("1a_6_south-west", "1a_6", DoorDirection.down, False, True),
    "1a_6_west": Door("1a_6_west", "1a_6", DoorDirection.left, False, False),
    "1a_6_east": Door("1a_6_east", "1a_6", DoorDirection.right, False, False),

    "1a_6z_north-west": Door("1a_6z_north-west", "1a_6z", DoorDirection.up, False, False),
    "1a_6z_west": Door("1a_6z_west", "1a_6z", DoorDirection.left, False, False),
    "1a_6z_east": Door("1a_6z_east", "1a_6z", DoorDirection.right, False, False),

    "1a_6zb_north-west": Door("1a_6zb_north-west", "1a_6zb", DoorDirection.up, False, True),
    "1a_6zb_east": Door("1a_6zb_east", "1a_6zb", DoorDirection.right, False, False),

    "1a_7zb_west": Door("1a_7zb_west", "1a_7zb", DoorDirection.down, False, False),
    "1a_7zb_east": Door("1a_7zb_east", "1a_7zb", DoorDirection.down, False, False),

    "1a_6a_west": Door("1a_6a_west", "1a_6a", DoorDirection.left, False, False),
    "1a_6a_east": Door("1a_6a_east", "1a_6a", DoorDirection.right, False, False),

    "1a_6b_north-west": Door("1a_6b_north-west", "1a_6b", DoorDirection.left, False, False),
    "1a_6b_south-west": Door("1a_6b_south-west", "1a_6b", DoorDirection.left, False, False),
    "1a_6b_north-east": Door("1a_6b_north-east", "1a_6b", DoorDirection.right, False, False),

    "1a_s0_west": Door("1a_s0_west", "1a_s0", DoorDirection.left, False, False),
    "1a_s0_east": Door("1a_s0_east", "1a_s0", DoorDirection.right, False, False),

    "1a_s1_east": Door("1a_s1_east", "1a_s1", DoorDirection.right, False, False),

    "1a_6c_south-west": Door("1a_6c_south-west", "1a_6c", DoorDirection.left, False, False),
    "1a_6c_north-west": Door("1a_6c_north-west", "1a_6c", DoorDirection.left, True, False),
    "1a_6c_north-east": Door("1a_6c_north-east", "1a_6c", DoorDirection.up, False, False),

    "1a_7_west": Door("1a_7_west", "1a_7", DoorDirection.down, False, True),
    "1a_7_east": Door("1a_7_east", "1a_7", DoorDirection.up, False, False),

    "1a_7z_bottom": Door("1a_7z_bottom", "1a_7z", DoorDirection.right, False, False),
    "1a_7z_top": Door("1a_7z_top", "1a_7z", DoorDirection.up, True, False),

    "1a_8z_bottom": Door("1a_8z_bottom", "1a_8z", DoorDirection.down, False, False),
    "1a_8z_top": Door("1a_8z_top", "1a_8z", DoorDirection.right, False, False),

    "1a_8zb_west": Door("1a_8zb_west", "1a_8zb", DoorDirection.left, False, False),
    "1a_8zb_east": Door("1a_8zb_east", "1a_8zb", DoorDirection.right, False, False),

    "1a_8_south-west": Door("1a_8_south-west", "1a_8", DoorDirection.down, False, True),
    "1a_8_west": Door("1a_8_west", "1a_8", DoorDirection.left, False, True),
    "1a_8_south": Door("1a_8_south", "1a_8", DoorDirection.down, False, False),
    "1a_8_south-east": Door("1a_8_south-east", "1a_8", DoorDirection.down, False, True),
    "1a_8_north": Door("1a_8_north", "1a_8", DoorDirection.up, False, False),
    "1a_8_north-east": Door("1a_8_north-east", "1a_8", DoorDirection.right, False, False),

    "1a_7a_west": Door("1a_7a_west", "1a_7a", DoorDirection.up, False, False),
    "1a_7a_east": Door("1a_7a_east", "1a_7a", DoorDirection.up, False, False),

    "1a_9z_east": Door("1a_9z_east", "1a_9z", DoorDirection.down, False, False),

    "1a_8b_west": Door("1a_8b_west", "1a_8b", DoorDirection.left, False, False),
    "1a_8b_east": Door("1a_8b_east", "1a_8b", DoorDirection.up, False, False),

    "1a_9_west": Door("1a_9_west", "1a_9", DoorDirection.down, False, True),
    "1a_9_east": Door("1a_9_east", "1a_9", DoorDirection.right, False, False),

    "1a_9b_west": Door("1a_9b_west", "1a_9b", DoorDirection.left, False, True),
    "1a_9b_north-west": Door("1a_9b_north-west", "1a_9b", DoorDirection.up, False, False),
    "1a_9b_east": Door("1a_9b_east", "1a_9b", DoorDirection.right, False, False),
    "1a_9b_north-east": Door("1a_9b_north-east", "1a_9b", DoorDirection.up, False, False),

    "1a_9c_west": Door("1a_9c_west", "1a_9c", DoorDirection.left, False, True),

    "1a_10_south-east": Door("1a_10_south-east", "1a_10", DoorDirection.down, False, False),
    "1a_10_south-west": Door("1a_10_south-west", "1a_10", DoorDirection.left, False, False),
    "1a_10_north-west": Door("1a_10_north-west", "1a_10", DoorDirection.up, False, False),
    "1a_10_north-east": Door("1a_10_north-east", "1a_10", DoorDirection.up, False, True),

    "1a_10z_west": Door("1a_10z_west", "1a_10z", DoorDirection.left, False, False),
    "1a_10z_east": Door("1a_10z_east", "1a_10z", DoorDirection.right, False, False),

    "1a_10zb_east": Door("1a_10zb_east", "1a_10zb", DoorDirection.right, False, False),

    "1a_11_south": Door("1a_11_south", "1a_11", DoorDirection.down, False, False),
    "1a_11_south-west": Door("1a_11_south-west", "1a_11", DoorDirection.down, False, False),
    "1a_11_west": Door("1a_11_west", "1a_11", DoorDirection.left, False, False),
    "1a_11_south-east": Door("1a_11_south-east", "1a_11", DoorDirection.down, False, True),
    "1a_11_north": Door("1a_11_north", "1a_11", DoorDirection.up, False, False),

    "1a_11z_east": Door("1a_11z_east", "1a_11z", DoorDirection.right, False, False),

    "1a_10a_bottom": Door("1a_10a_bottom", "1a_10a", DoorDirection.down, False, False),
    "1a_10a_top": Door("1a_10a_top", "1a_10a", DoorDirection.up, False, False),

    "1a_12_south-west": Door("1a_12_south-west", "1a_12", DoorDirection.down, False, True),
    "1a_12_north-west": Door("1a_12_north-west", "1a_12", DoorDirection.left, False, False),
    "1a_12_east": Door("1a_12_east", "1a_12", DoorDirection.right, False, True),

    "1a_12z_east": Door("1a_12z_east", "1a_12z", DoorDirection.right, False, False),

    "1a_12a_bottom": Door("1a_12a_bottom", "1a_12a", DoorDirection.left, False, False),
    "1a_12a_top": Door("1a_12a_top", "1a_12a", DoorDirection.up, False, False),

    "1a_end_south": Door("1a_end_south", "1a_end", DoorDirection.down, False, True),

    "1b_00_east": Door("1b_00_east", "1b_00", DoorDirection.up, False, False),

    "1b_01_west": Door("1b_01_west", "1b_01", DoorDirection.down, False, True),
    "1b_01_east": Door("1b_01_east", "1b_01", DoorDirection.up, False, False),

    "1b_02_west": Door("1b_02_west", "1b_02", DoorDirection.down, False, True),
    "1b_02_east": Door("1b_02_east", "1b_02", DoorDirection.up, False, False),

    "1b_02b_west": Door("1b_02b_west", "1b_02b", DoorDirection.down, False, True),
    "1b_02b_east": Door("1b_02b_east", "1b_02b", DoorDirection.up, False, False),

    "1b_03_west": Door("1b_03_west", "1b_03", DoorDirection.down, False, True),
    "1b_03_east": Door("1b_03_east", "1b_03", DoorDirection.right, False, False),

    "1b_04_west": Door("1b_04_west", "1b_04", DoorDirection.left, False, True),
    "1b_04_east": Door("1b_04_east", "1b_04", DoorDirection.up, False, False),

    "1b_05_west": Door("1b_05_west", "1b_05", DoorDirection.down, False, True),
    "1b_05_east": Door("1b_05_east", "1b_05", DoorDirection.up, False, False),

    "1b_05b_west": Door("1b_05b_west", "1b_05b", DoorDirection.down, False, True),
    "1b_05b_east": Door("1b_05b_east", "1b_05b", DoorDirection.up, False, False),

    "1b_06_west": Door("1b_06_west", "1b_06", DoorDirection.down, False, True),
    "1b_06_east": Door("1b_06_east", "1b_06", DoorDirection.right, False, False),

    "1b_07_bottom": Door("1b_07_bottom", "1b_07", DoorDirection.left, False, False),
    "1b_07_top": Door("1b_07_top", "1b_07", DoorDirection.up, False, False),

    "1b_08_west": Door("1b_08_west", "1b_08", DoorDirection.down, False, True),
    "1b_08_east": Door("1b_08_east", "1b_08", DoorDirection.up, False, False),

    "1b_08b_west": Door("1b_08b_west", "1b_08b", DoorDirection.down, False, True),
    "1b_08b_east": Door("1b_08b_east", "1b_08b", DoorDirection.up, False, False),

    "1b_09_west": Door("1b_09_west", "1b_09", DoorDirection.down, False, True),
    "1b_09_east": Door("1b_09_east", "1b_09", DoorDirection.right, False, False),

    "1b_10_west": Door("1b_10_west", "1b_10", DoorDirection.left, False, False),
    "1b_10_east": Door("1b_10_east", "1b_10", DoorDirection.right, False, False),

    "1b_11_bottom": Door("1b_11_bottom", "1b_11", DoorDirection.left, False, False),
    "1b_11_top": Door("1b_11_top", "1b_11", DoorDirection.up, False, False),

    "1b_end_west": Door("1b_end_west", "1b_end", DoorDirection.down, False, True),

    "1c_00_east": Door("1c_00_east", "1c_00", DoorDirection.right, False, False),

    "1c_01_west": Door("1c_01_west", "1c_01", DoorDirection.left, False, True),
    "1c_01_east": Door("1c_01_east", "1c_01", DoorDirection.right, False, False),

    "1c_02_west": Door("1c_02_west", "1c_02", DoorDirection.left, False, True),

    "2a_start_east": Door("2a_start_east", "2a_start", DoorDirection.right, False, False),
    "2a_start_top": Door("2a_start_top", "2a_start", DoorDirection.up, False, False),

    "2a_s0_bottom": Door("2a_s0_bottom", "2a_s0", DoorDirection.down, False, False),
    "2a_s0_top": Door("2a_s0_top", "2a_s0", DoorDirection.up, False, False),

    "2a_s1_bottom": Door("2a_s1_bottom", "2a_s1", DoorDirection.down, False, False),
    "2a_s1_top": Door("2a_s1_top", "2a_s1", DoorDirection.up, False, False),

    "2a_s2_bottom": Door("2a_s2_bottom", "2a_s2", DoorDirection.down, False, False),

    "2a_0_south-west": Door("2a_0_south-west", "2a_0", DoorDirection.left, False, False),
    "2a_0_south-east": Door("2a_0_south-east", "2a_0", DoorDirection.right, False, False),
    "2a_0_north-west": Door("2a_0_north-west", "2a_0", DoorDirection.up, False, False),
    "2a_0_north-east": Door("2a_0_north-east", "2a_0", DoorDirection.right, False, False),

    "2a_1_south-west": Door("2a_1_south-west", "2a_1", DoorDirection.left, False, False),
    "2a_1_south-east": Door("2a_1_south-east", "2a_1", DoorDirection.right, False, False),
    "2a_1_north-west": Door("2a_1_north-west", "2a_1", DoorDirection.left, False, False),
    "2a_1_south": Door("2a_1_south", "2a_1", DoorDirection.down, False, False),

    "2a_d0_north": Door("2a_d0_north", "2a_d0", DoorDirection.up, False, False),
    "2a_d0_north-west": Door("2a_d0_north-west", "2a_d0", DoorDirection.left, False, False),
    "2a_d0_west": Door("2a_d0_west", "2a_d0", DoorDirection.left, False, False),
    "2a_d0_south-west": Door("2a_d0_south-west", "2a_d0", DoorDirection.left, False, False),
    "2a_d0_south": Door("2a_d0_south", "2a_d0", DoorDirection.down, False, False),
    "2a_d0_south-east": Door("2a_d0_south-east", "2a_d0", DoorDirection.right, True, False),
    "2a_d0_east": Door("2a_d0_east", "2a_d0", DoorDirection.right, False, False),
    "2a_d0_north-east": Door("2a_d0_north-east", "2a_d0", DoorDirection.right, False, False),

    "2a_d7_west": Door("2a_d7_west", "2a_d7", DoorDirection.left, False, False),
    "2a_d7_east": Door("2a_d7_east", "2a_d7", DoorDirection.right, False, False),

    "2a_d8_west": Door("2a_d8_west", "2a_d8", DoorDirection.left, False, False),
    "2a_d8_south-east": Door("2a_d8_south-east", "2a_d8", DoorDirection.right, False, False),
    "2a_d8_north-east": Door("2a_d8_north-east", "2a_d8", DoorDirection.right, False, False),

    "2a_d3_west": Door("2a_d3_west", "2a_d3", DoorDirection.left, False, False),
    "2a_d3_south": Door("2a_d3_south", "2a_d3", DoorDirection.left, False, False),
    "2a_d3_north": Door("2a_d3_north", "2a_d3", DoorDirection.left, False, False),

    "2a_d2_west": Door("2a_d2_west", "2a_d2", DoorDirection.left, False, False),
    "2a_d2_north-west": Door("2a_d2_north-west", "2a_d2", DoorDirection.up, False, True),
    "2a_d2_east": Door("2a_d2_east", "2a_d2", DoorDirection.right, False, False),

    "2a_d9_north-west": Door("2a_d9_north-west", "2a_d9", DoorDirection.up, False, False),

    "2a_d1_north-east": Door("2a_d1_north-east", "2a_d1", DoorDirection.right, False, False),
    "2a_d1_south-east": Door("2a_d1_south-east", "2a_d1", DoorDirection.right, False, False),
    "2a_d1_south-west": Door("2a_d1_south-west", "2a_d1", DoorDirection.down, True, False),

    "2a_d6_west": Door("2a_d6_west", "2a_d6", DoorDirection.up, False, False),
    "2a_d6_east": Door("2a_d6_east", "2a_d6", DoorDirection.right, False, False),

    "2a_d4_west": Door("2a_d4_west", "2a_d4", DoorDirection.left, False, False),
    "2a_d4_east": Door("2a_d4_east", "2a_d4", DoorDirection.right, False, False),
    "2a_d4_south": Door("2a_d4_south", "2a_d4", DoorDirection.down, False, False),

    "2a_d5_west": Door("2a_d5_west", "2a_d5", DoorDirection.left, False, False),

    "2a_3x_bottom": Door("2a_3x_bottom", "2a_3x", DoorDirection.down, False, False),
    "2a_3x_top": Door("2a_3x_top", "2a_3x", DoorDirection.up, False, False),

    "2a_3_bottom": Door("2a_3_bottom", "2a_3", DoorDirection.down, False, True),
    "2a_3_top": Door("2a_3_top", "2a_3", DoorDirection.up, False, False),

    "2a_4_bottom": Door("2a_4_bottom", "2a_4", DoorDirection.down, False, True),
    "2a_4_top": Door("2a_4_top", "2a_4", DoorDirection.up, False, False),

    "2a_5_bottom": Door("2a_5_bottom", "2a_5", DoorDirection.down, False, True),
    "2a_5_top": Door("2a_5_top", "2a_5", DoorDirection.up, False, False),

    "2a_6_bottom": Door("2a_6_bottom", "2a_6", DoorDirection.down, False, True),
    "2a_6_top": Door("2a_6_top", "2a_6", DoorDirection.up, False, False),

    "2a_7_bottom": Door("2a_7_bottom", "2a_7", DoorDirection.down, False, True),
    "2a_7_top": Door("2a_7_top", "2a_7", DoorDirection.up, False, False),

    "2a_8_bottom": Door("2a_8_bottom", "2a_8", DoorDirection.down, False, True),
    "2a_8_top": Door("2a_8_top", "2a_8", DoorDirection.right, False, False),

    "2a_9_west": Door("2a_9_west", "2a_9", DoorDirection.left, False, False),
    "2a_9_north": Door("2a_9_north", "2a_9", DoorDirection.up, False, False),
    "2a_9_north-west": Door("2a_9_north-west", "2a_9", DoorDirection.up, False, False),
    "2a_9_south-east": Door("2a_9_south-east", "2a_9", DoorDirection.down, False, False),

    "2a_9b_east": Door("2a_9b_east", "2a_9b", DoorDirection.down, False, True),
    "2a_9b_west": Door("2a_9b_west", "2a_9b", DoorDirection.down, False, False),

    "2a_10_bottom": Door("2a_10_bottom", "2a_10", DoorDirection.down, False, True),
    "2a_10_top": Door("2a_10_top", "2a_10", DoorDirection.up, False, False),

    "2a_2_north-west": Door("2a_2_north-west", "2a_2", DoorDirection.up, False, False),
    "2a_2_south-west": Door("2a_2_south-west", "2a_2", DoorDirection.left, False, False),
    "2a_2_south-east": Door("2a_2_south-east", "2a_2", DoorDirection.right, False, False),

    "2a_11_west": Door("2a_11_west", "2a_11", DoorDirection.left, False, False),
    "2a_11_east": Door("2a_11_east", "2a_11", DoorDirection.right, False, False),

    "2a_12b_west": Door("2a_12b_west", "2a_12b", DoorDirection.left, False, False),
    "2a_12b_north": Door("2a_12b_north", "2a_12b", DoorDirection.up, False, False),
    "2a_12b_south": Door("2a_12b_south", "2a_12b", DoorDirection.down, False, False),
    "2a_12b_south-east": Door("2a_12b_south-east", "2a_12b", DoorDirection.down, False, True),
    "2a_12b_east": Door("2a_12b_east", "2a_12b", DoorDirection.right, False, True),

    "2a_12c_south": Door("2a_12c_south", "2a_12c", DoorDirection.down, False, False),

    "2a_12d_north-west": Door("2a_12d_north-west", "2a_12d", DoorDirection.up, False, False),
    "2a_12d_north": Door("2a_12d_north", "2a_12d", DoorDirection.up, False, False),

    "2a_12_west": Door("2a_12_west", "2a_12", DoorDirection.left, False, False),
    "2a_12_east": Door("2a_12_east", "2a_12", DoorDirection.right, False, False),

    "2a_13_west": Door("2a_13_west", "2a_13", DoorDirection.left, False, False),
    "2a_13_phone": Door("2a_13_phone", "2a_13", DoorDirection.special, False, True),

    "2a_end_0_main": Door("2a_end_0_main", "2a_end_0", DoorDirection.special, False, True),
    "2a_end_0_east": Door("2a_end_0_east", "2a_end_0", DoorDirection.right, False, False),
    "2a_end_0_top": Door("2a_end_0_top", "2a_end_0", DoorDirection.up, False, False),

    "2a_end_s0_bottom": Door("2a_end_s0_bottom", "2a_end_s0", DoorDirection.down, False, False),
    "2a_end_s0_top": Door("2a_end_s0_top", "2a_end_s0", DoorDirection.up, False, False),

    "2a_end_s1_bottom": Door("2a_end_s1_bottom", "2a_end_s1", DoorDirection.down, False, False),

    "2a_end_1_west": Door("2a_end_1_west", "2a_end_1", DoorDirection.left, False, False),
    "2a_end_1_north-east": Door("2a_end_1_north-east", "2a_end_1", DoorDirection.right, False, False),
    "2a_end_1_east": Door("2a_end_1_east", "2a_end_1", DoorDirection.right, False, False),

    "2a_end_2_north-west": Door("2a_end_2_north-west", "2a_end_2", DoorDirection.left, False, False),
    "2a_end_2_west": Door("2a_end_2_west", "2a_end_2", DoorDirection.left, False, False),
    "2a_end_2_north-east": Door("2a_end_2_north-east", "2a_end_2", DoorDirection.right, False, False),
    "2a_end_2_east": Door("2a_end_2_east", "2a_end_2", DoorDirection.right, False, False),

    "2a_end_3_north-west": Door("2a_end_3_north-west", "2a_end_3", DoorDirection.left, False, True),
    "2a_end_3_west": Door("2a_end_3_west", "2a_end_3", DoorDirection.left, False, True),
    "2a_end_3_east": Door("2a_end_3_east", "2a_end_3", DoorDirection.right, False, False),

    "2a_end_4_west": Door("2a_end_4_west", "2a_end_4", DoorDirection.left, False, False),
    "2a_end_4_east": Door("2a_end_4_east", "2a_end_4", DoorDirection.right, False, False),

    "2a_end_3b_west": Door("2a_end_3b_west", "2a_end_3b", DoorDirection.left, False, False),
    "2a_end_3b_north": Door("2a_end_3b_north", "2a_end_3b", DoorDirection.up, False, False),
    "2a_end_3b_east": Door("2a_end_3b_east", "2a_end_3b", DoorDirection.right, False, False),

    "2a_end_3cb_bottom": Door("2a_end_3cb_bottom", "2a_end_3cb", DoorDirection.down, False, False),
    "2a_end_3cb_top": Door("2a_end_3cb_top", "2a_end_3cb", DoorDirection.up, False, False),

    "2a_end_3c_bottom": Door("2a_end_3c_bottom", "2a_end_3c", DoorDirection.down, False, False),

    "2a_end_5_west": Door("2a_end_5_west", "2a_end_5", DoorDirection.left, False, False),
    "2a_end_5_east": Door("2a_end_5_east", "2a_end_5", DoorDirection.right, False, False),

    "2a_end_6_west": Door("2a_end_6_west", "2a_end_6", DoorDirection.left, False, False),

    "2b_start_east": Door("2b_start_east", "2b_start", DoorDirection.right, False, False),

    "2b_00_west": Door("2b_00_west", "2b_00", DoorDirection.left, False, False),
    "2b_00_east": Door("2b_00_east", "2b_00", DoorDirection.right, False, False),

    "2b_01_west": Door("2b_01_west", "2b_01", DoorDirection.left, False, False),
    "2b_01_east": Door("2b_01_east", "2b_01", DoorDirection.up, False, False),

    "2b_01b_west": Door("2b_01b_west", "2b_01b", DoorDirection.down, False, True),
    "2b_01b_east": Door("2b_01b_east", "2b_01b", DoorDirection.up, False, False),

    "2b_02b_west": Door("2b_02b_west", "2b_02b", DoorDirection.down, False, True),
    "2b_02b_east": Door("2b_02b_east", "2b_02b", DoorDirection.up, False, False),

    "2b_02_west": Door("2b_02_west", "2b_02", DoorDirection.down, False, True),
    "2b_02_east": Door("2b_02_east", "2b_02", DoorDirection.up, False, False),

    "2b_03_west": Door("2b_03_west", "2b_03", DoorDirection.down, False, True),
    "2b_03_east": Door("2b_03_east", "2b_03", DoorDirection.up, False, False),

    "2b_04_bottom": Door("2b_04_bottom", "2b_04", DoorDirection.down, False, True),
    "2b_04_top": Door("2b_04_top", "2b_04", DoorDirection.up, False, False),

    "2b_05_bottom": Door("2b_05_bottom", "2b_05", DoorDirection.down, False, True),
    "2b_05_top": Door("2b_05_top", "2b_05", DoorDirection.up, False, False),

    "2b_06_west": Door("2b_06_west", "2b_06", DoorDirection.down, False, True),
    "2b_06_east": Door("2b_06_east", "2b_06", DoorDirection.right, False, False),

    "2b_07_bottom": Door("2b_07_bottom", "2b_07", DoorDirection.left, False, False),
    "2b_07_top": Door("2b_07_top", "2b_07", DoorDirection.up, False, False),

    "2b_08b_west": Door("2b_08b_west", "2b_08b", DoorDirection.down, False, True),
    "2b_08b_east": Door("2b_08b_east", "2b_08b", DoorDirection.up, False, False),

    "2b_08_west": Door("2b_08_west", "2b_08", DoorDirection.down, False, True),
    "2b_08_east": Door("2b_08_east", "2b_08", DoorDirection.up, False, False),

    "2b_09_west": Door("2b_09_west", "2b_09", DoorDirection.down, False, True),
    "2b_09_east": Door("2b_09_east", "2b_09", DoorDirection.right, False, False),

    "2b_10_west": Door("2b_10_west", "2b_10", DoorDirection.left, False, False),
    "2b_10_east": Door("2b_10_east", "2b_10", DoorDirection.up, False, False),

    "2b_11_bottom": Door("2b_11_bottom", "2b_11", DoorDirection.down, False, True),
    "2b_11_top": Door("2b_11_top", "2b_11", DoorDirection.up, False, False),

    "2b_end_west": Door("2b_end_west", "2b_end", DoorDirection.down, False, True),

    "2c_00_east": Door("2c_00_east", "2c_00", DoorDirection.right, False, False),

    "2c_01_west": Door("2c_01_west", "2c_01", DoorDirection.left, False, False),
    "2c_01_east": Door("2c_01_east", "2c_01", DoorDirection.right, False, False),

    "2c_02_west": Door("2c_02_west", "2c_02", DoorDirection.left, False, True),

    "3a_s0_east": Door("3a_s0_east", "3a_s0", DoorDirection.right, False, False),

    "3a_s1_west": Door("3a_s1_west", "3a_s1", DoorDirection.left, False, False),
    "3a_s1_east": Door("3a_s1_east", "3a_s1", DoorDirection.right, False, False),
    "3a_s1_north-east": Door("3a_s1_north-east", "3a_s1", DoorDirection.right, False, False),

    "3a_s2_west": Door("3a_s2_west", "3a_s2", DoorDirection.left, False, False),
    "3a_s2_north-west": Door("3a_s2_north-west", "3a_s2", DoorDirection.left, False, False),
    "3a_s2_east": Door("3a_s2_east", "3a_s2", DoorDirection.right, False, False),

    "3a_s3_west": Door("3a_s3_west", "3a_s3", DoorDirection.left, False, False),
    "3a_s3_north": Door("3a_s3_north", "3a_s3", DoorDirection.right, False, False),
    "3a_s3_east": Door("3a_s3_east", "3a_s3", DoorDirection.right, False, False),

    "3a_0x-a_west": Door("3a_0x-a_west", "3a_0x-a", DoorDirection.left, False, True),
    "3a_0x-a_east": Door("3a_0x-a_east", "3a_0x-a", DoorDirection.right, False, False),

    "3a_00-a_west": Door("3a_00-a_west", "3a_00-a", DoorDirection.left, False, False),
    "3a_00-a_east": Door("3a_00-a_east", "3a_00-a", DoorDirection.right, False, False),

    "3a_02-a_west": Door("3a_02-a_west", "3a_02-a", DoorDirection.left, False, True),
    "3a_02-a_top": Door("3a_02-a_top", "3a_02-a", DoorDirection.up, False, False),
    "3a_02-a_east": Door("3a_02-a_east", "3a_02-a", DoorDirection.right, True, False),

    "3a_02-b_west": Door("3a_02-b_west", "3a_02-b", DoorDirection.left, False, False),
    "3a_02-b_east": Door("3a_02-b_east", "3a_02-b", DoorDirection.down, False, False),
    "3a_02-b_far-east": Door("3a_02-b_far-east", "3a_02-b", DoorDirection.right, False, False),

    "3a_01-b_west": Door("3a_01-b_west", "3a_01-b", DoorDirection.left, False, False),
    "3a_01-b_north-west": Door("3a_01-b_north-west", "3a_01-b", DoorDirection.left, False, False),
    "3a_01-b_east": Door("3a_01-b_east", "3a_01-b", DoorDirection.right, False, False),

    "3a_00-b_south-west": Door("3a_00-b_south-west", "3a_00-b", DoorDirection.left, False, False),
    "3a_00-b_south-east": Door("3a_00-b_south-east", "3a_00-b", DoorDirection.right, False, False),
    "3a_00-b_west": Door("3a_00-b_west", "3a_00-b", DoorDirection.left, False, False),
    "3a_00-b_north-west": Door("3a_00-b_north-west", "3a_00-b", DoorDirection.up, False, False),
    "3a_00-b_east": Door("3a_00-b_east", "3a_00-b", DoorDirection.right, False, False),
    "3a_00-b_north": Door("3a_00-b_north", "3a_00-b", DoorDirection.up, True, False),

    "3a_00-c_south-west": Door("3a_00-c_south-west", "3a_00-c", DoorDirection.down, False, False),
    "3a_00-c_south-east": Door("3a_00-c_south-east", "3a_00-c", DoorDirection.down, False, False),
    "3a_00-c_north-east": Door("3a_00-c_north-east", "3a_00-c", DoorDirection.right, False, False),

    "3a_0x-b_west": Door("3a_0x-b_west", "3a_0x-b", DoorDirection.left, False, False),
    "3a_0x-b_south-east": Door("3a_0x-b_south-east", "3a_0x-b", DoorDirection.right, False, False),
    "3a_0x-b_north-east": Door("3a_0x-b_north-east", "3a_0x-b", DoorDirection.right, False, False),

    "3a_03-a_west": Door("3a_03-a_west", "3a_03-a", DoorDirection.left, False, False),
    "3a_03-a_top": Door("3a_03-a_top", "3a_03-a", DoorDirection.up, False, False),
    "3a_03-a_east": Door("3a_03-a_east", "3a_03-a", DoorDirection.right, False, False),

    "3a_04-b_west": Door("3a_04-b_west", "3a_04-b", DoorDirection.left, False, False),
    "3a_04-b_east": Door("3a_04-b_east", "3a_04-b", DoorDirection.down, False, False),

    "3a_05-a_west": Door("3a_05-a_west", "3a_05-a", DoorDirection.left, False, False),
    "3a_05-a_east": Door("3a_05-a_east", "3a_05-a", DoorDirection.right, False, False),

    "3a_06-a_west": Door("3a_06-a_west", "3a_06-a", DoorDirection.left, False, False),
    "3a_06-a_east": Door("3a_06-a_east", "3a_06-a", DoorDirection.right, False, False),

    "3a_07-a_west": Door("3a_07-a_west", "3a_07-a", DoorDirection.left, False, False),
    "3a_07-a_top": Door("3a_07-a_top", "3a_07-a", DoorDirection.up, False, False),
    "3a_07-a_east": Door("3a_07-a_east", "3a_07-a", DoorDirection.right, False, False),

    "3a_07-b_bottom": Door("3a_07-b_bottom", "3a_07-b", DoorDirection.down, False, False),
    "3a_07-b_west": Door("3a_07-b_west", "3a_07-b", DoorDirection.left, False, False),
    "3a_07-b_top": Door("3a_07-b_top", "3a_07-b", DoorDirection.up, False, False),
    "3a_07-b_east": Door("3a_07-b_east", "3a_07-b", DoorDirection.right, False, False),

    "3a_06-b_west": Door("3a_06-b_west", "3a_06-b", DoorDirection.up, False, False),
    "3a_06-b_east": Door("3a_06-b_east", "3a_06-b", DoorDirection.right, False, False),

    "3a_06-c_south-west": Door("3a_06-c_south-west", "3a_06-c", DoorDirection.down, False, True),
    "3a_06-c_north-west": Door("3a_06-c_north-west", "3a_06-c", DoorDirection.left, False, False),
    "3a_06-c_south-east": Door("3a_06-c_south-east", "3a_06-c", DoorDirection.down, True, False),
    "3a_06-c_east": Door("3a_06-c_east", "3a_06-c", DoorDirection.right, False, False),

    "3a_05-c_east": Door("3a_05-c_east", "3a_05-c", DoorDirection.right, False, False),

    "3a_08-c_west": Door("3a_08-c_west", "3a_08-c", DoorDirection.left, False, False),
    "3a_08-c_east": Door("3a_08-c_east", "3a_08-c", DoorDirection.down, False, False),

    "3a_08-b_west": Door("3a_08-b_west", "3a_08-b", DoorDirection.left, False, False),
    "3a_08-b_east": Door("3a_08-b_east", "3a_08-b", DoorDirection.up, False, False),

    "3a_08-a_west": Door("3a_08-a_west", "3a_08-a", DoorDirection.left, False, True),
    "3a_08-a_bottom": Door("3a_08-a_bottom", "3a_08-a", DoorDirection.down, False, False),
    "3a_08-a_east": Door("3a_08-a_east", "3a_08-a", DoorDirection.right, False, False),

    "3a_09-b_west": Door("3a_09-b_west", "3a_09-b", DoorDirection.left, False, False),
    "3a_09-b_north-west": Door("3a_09-b_north-west", "3a_09-b", DoorDirection.up, False, False),
    "3a_09-b_south-west": Door("3a_09-b_south-west", "3a_09-b", DoorDirection.down, False, True),
    "3a_09-b_south": Door("3a_09-b_south", "3a_09-b", DoorDirection.down, False, True),
    "3a_09-b_south-east": Door("3a_09-b_south-east", "3a_09-b", DoorDirection.down, False, False),
    "3a_09-b_east": Door("3a_09-b_east", "3a_09-b", DoorDirection.right, False, False),
    "3a_09-b_north-east-right": Door("3a_09-b_north-east-right", "3a_09-b", DoorDirection.right, False, False),
    "3a_09-b_north-east-top": Door("3a_09-b_north-east-top", "3a_09-b", DoorDirection.up, False, False),
    "3a_09-b_north": Door("3a_09-b_north", "3a_09-b", DoorDirection.up, False, False),

    "3a_10-x_west": Door("3a_10-x_west", "3a_10-x", DoorDirection.up, False, False),
    "3a_10-x_south-east": Door("3a_10-x_south-east", "3a_10-x", DoorDirection.down, False, True),
    "3a_10-x_north-east-top": Door("3a_10-x_north-east-top", "3a_10-x", DoorDirection.up, False, True),
    "3a_10-x_north-east-right": Door("3a_10-x_north-east-right", "3a_10-x", DoorDirection.right, False, True),

    "3a_11-x_west": Door("3a_11-x_west", "3a_11-x", DoorDirection.left, False, False),
    "3a_11-x_south": Door("3a_11-x_south", "3a_11-x", DoorDirection.down, False, False),

    "3a_11-y_west": Door("3a_11-y_west", "3a_11-y", DoorDirection.up, False, False),
    "3a_11-y_east": Door("3a_11-y_east", "3a_11-y", DoorDirection.right, False, False),
    "3a_11-y_south": Door("3a_11-y_south", "3a_11-y", DoorDirection.down, False, False),

    "3a_12-y_west": Door("3a_12-y_west", "3a_12-y", DoorDirection.left, False, False),

    "3a_11-z_west": Door("3a_11-z_west", "3a_11-z", DoorDirection.left, False, False),
    "3a_11-z_east": Door("3a_11-z_east", "3a_11-z", DoorDirection.up, False, False),

    "3a_10-z_bottom": Door("3a_10-z_bottom", "3a_10-z", DoorDirection.right, False, False),
    "3a_10-z_top": Door("3a_10-z_top", "3a_10-z", DoorDirection.up, False, False),

    "3a_10-y_bottom": Door("3a_10-y_bottom", "3a_10-y", DoorDirection.down, False, True),
    "3a_10-y_top": Door("3a_10-y_top", "3a_10-y", DoorDirection.up, False, False),

    "3a_10-c_south-east": Door("3a_10-c_south-east", "3a_10-c", DoorDirection.down, False, False),
    "3a_10-c_north-east": Door("3a_10-c_north-east", "3a_10-c", DoorDirection.right, False, False),
    "3a_10-c_north-west": Door("3a_10-c_north-west", "3a_10-c", DoorDirection.up, False, False),
    "3a_10-c_south-west": Door("3a_10-c_south-west", "3a_10-c", DoorDirection.down, False, False),

    "3a_11-c_south-east": Door("3a_11-c_south-east", "3a_11-c", DoorDirection.down, False, True),
    "3a_11-c_east": Door("3a_11-c_east", "3a_11-c", DoorDirection.right, False, False),
    "3a_11-c_west": Door("3a_11-c_west", "3a_11-c", DoorDirection.left, False, False),
    "3a_11-c_south-west": Door("3a_11-c_south-west", "3a_11-c", DoorDirection.down, False, False),

    "3a_12-c_west": Door("3a_12-c_west", "3a_12-c", DoorDirection.left, False, False),
    "3a_12-c_top": Door("3a_12-c_top", "3a_12-c", DoorDirection.up, False, False),

    "3a_12-d_bottom": Door("3a_12-d_bottom", "3a_12-d", DoorDirection.down, False, True),
    "3a_12-d_top": Door("3a_12-d_top", "3a_12-d", DoorDirection.left, False, False),

    "3a_11-d_west": Door("3a_11-d_west", "3a_11-d", DoorDirection.left, False, False),
    "3a_11-d_east": Door("3a_11-d_east", "3a_11-d", DoorDirection.right, False, False),

    "3a_10-d_west": Door("3a_10-d_west", "3a_10-d", DoorDirection.down, False, False),
    "3a_10-d_east": Door("3a_10-d_east", "3a_10-d", DoorDirection.right, False, False),

    "3a_11-b_west": Door("3a_11-b_west", "3a_11-b", DoorDirection.left, False, False),
    "3a_11-b_north-west": Door("3a_11-b_north-west", "3a_11-b", DoorDirection.up, False, False),
    "3a_11-b_east": Door("3a_11-b_east", "3a_11-b", DoorDirection.right, False, False),
    "3a_11-b_north-east": Door("3a_11-b_north-east", "3a_11-b", DoorDirection.up, False, False),

    "3a_12-b_west": Door("3a_12-b_west", "3a_12-b", DoorDirection.left, False, False),
    "3a_12-b_east": Door("3a_12-b_east", "3a_12-b", DoorDirection.right, False, False),

    "3a_13-b_top": Door("3a_13-b_top", "3a_13-b", DoorDirection.left, False, False),
    "3a_13-b_bottom": Door("3a_13-b_bottom", "3a_13-b", DoorDirection.down, False, False),

    "3a_13-a_west": Door("3a_13-a_west", "3a_13-a", DoorDirection.up, False, False),
    "3a_13-a_south-west": Door("3a_13-a_south-west", "3a_13-a", DoorDirection.left, False, False),
    "3a_13-a_east": Door("3a_13-a_east", "3a_13-a", DoorDirection.down, False, False),

    "3a_13-x_west": Door("3a_13-x_west", "3a_13-x", DoorDirection.left, False, False),
    "3a_13-x_east": Door("3a_13-x_east", "3a_13-x", DoorDirection.up, False, False),

    "3a_12-x_west": Door("3a_12-x_west", "3a_12-x", DoorDirection.up, False, False),
    "3a_12-x_north-east": Door("3a_12-x_north-east", "3a_12-x", DoorDirection.up, False, False),
    "3a_12-x_east": Door("3a_12-x_east", "3a_12-x", DoorDirection.right, False, False),

    "3a_11-a_west": Door("3a_11-a_west", "3a_11-a", DoorDirection.left, False, False),
    "3a_11-a_south": Door("3a_11-a_south", "3a_11-a", DoorDirection.down, False, True),
    "3a_11-a_south-east-bottom": Door("3a_11-a_south-east-bottom", "3a_11-a", DoorDirection.down, False, False),
    "3a_11-a_south-east-right": Door("3a_11-a_south-east-right", "3a_11-a", DoorDirection.right, False, False),

    "3a_08-x_west": Door("3a_08-x_west", "3a_08-x", DoorDirection.up, False, False),
    "3a_08-x_east": Door("3a_08-x_east", "3a_08-x", DoorDirection.up, False, False),

    "3a_09-d_bottom": Door("3a_09-d_bottom", "3a_09-d", DoorDirection.down, False, True),
    "3a_09-d_top": Door("3a_09-d_top", "3a_09-d", DoorDirection.left, False, False),

    "3a_08-d_west": Door("3a_08-d_west", "3a_08-d", DoorDirection.left, False, False),
    "3a_08-d_east": Door("3a_08-d_east", "3a_08-d", DoorDirection.right, False, False),

    "3a_06-d_west": Door("3a_06-d_west", "3a_06-d", DoorDirection.left, False, False),
    "3a_06-d_east": Door("3a_06-d_east", "3a_06-d", DoorDirection.right, False, False),

    "3a_04-d_west": Door("3a_04-d_west", "3a_04-d", DoorDirection.left, False, False),
    "3a_04-d_south-west": Door("3a_04-d_south-west", "3a_04-d", DoorDirection.down, False, False),
    "3a_04-d_south": Door("3a_04-d_south", "3a_04-d", DoorDirection.down, False, False),
    "3a_04-d_east": Door("3a_04-d_east", "3a_04-d", DoorDirection.right, False, False),

    "3a_04-c_west": Door("3a_04-c_west", "3a_04-c", DoorDirection.left, False, False),
    "3a_04-c_north-west": Door("3a_04-c_north-west", "3a_04-c", DoorDirection.up, False, False),
    "3a_04-c_east": Door("3a_04-c_east", "3a_04-c", DoorDirection.up, False, False),

    "3a_02-c_west": Door("3a_02-c_west", "3a_02-c", DoorDirection.left, False, False),
    "3a_02-c_east": Door("3a_02-c_east", "3a_02-c", DoorDirection.right, False, False),
    "3a_02-c_south-east": Door("3a_02-c_south-east", "3a_02-c", DoorDirection.down, False, False),

    "3a_03-b_west": Door("3a_03-b_west", "3a_03-b", DoorDirection.left, False, False),
    "3a_03-b_east": Door("3a_03-b_east", "3a_03-b", DoorDirection.right, False, False),
    "3a_03-b_north": Door("3a_03-b_north", "3a_03-b", DoorDirection.up, False, False),

    "3a_01-c_west": Door("3a_01-c_west", "3a_01-c", DoorDirection.left, False, False),
    "3a_01-c_east": Door("3a_01-c_east", "3a_01-c", DoorDirection.right, False, False),

    "3a_02-d_west": Door("3a_02-d_west", "3a_02-d", DoorDirection.left, False, False),
    "3a_02-d_east": Door("3a_02-d_east", "3a_02-d", DoorDirection.right, False, False),

    "3a_00-d_west": Door("3a_00-d_west", "3a_00-d", DoorDirection.up, False, False),
    "3a_00-d_east": Door("3a_00-d_east", "3a_00-d", DoorDirection.right, False, True),

    "3a_roof00_west": Door("3a_roof00_west", "3a_roof00", DoorDirection.down, False, True),
    "3a_roof00_east": Door("3a_roof00_east", "3a_roof00", DoorDirection.right, False, False),

    "3a_roof01_west": Door("3a_roof01_west", "3a_roof01", DoorDirection.left, False, False),
    "3a_roof01_east": Door("3a_roof01_east", "3a_roof01", DoorDirection.right, False, False),

    "3a_roof02_west": Door("3a_roof02_west", "3a_roof02", DoorDirection.left, False, False),
    "3a_roof02_east": Door("3a_roof02_east", "3a_roof02", DoorDirection.right, False, False),

    "3a_roof03_west": Door("3a_roof03_west", "3a_roof03", DoorDirection.left, False, False),
    "3a_roof03_east": Door("3a_roof03_east", "3a_roof03", DoorDirection.right, False, False),

    "3a_roof04_west": Door("3a_roof04_west", "3a_roof04", DoorDirection.left, False, False),
    "3a_roof04_east": Door("3a_roof04_east", "3a_roof04", DoorDirection.right, False, False),

    "3a_roof05_west": Door("3a_roof05_west", "3a_roof05", DoorDirection.left, False, False),
    "3a_roof05_east": Door("3a_roof05_east", "3a_roof05", DoorDirection.right, False, False),

    "3a_roof06b_west": Door("3a_roof06b_west", "3a_roof06b", DoorDirection.left, False, False),
    "3a_roof06b_east": Door("3a_roof06b_east", "3a_roof06b", DoorDirection.right, False, False),

    "3a_roof06_west": Door("3a_roof06_west", "3a_roof06", DoorDirection.left, False, False),
    "3a_roof06_east": Door("3a_roof06_east", "3a_roof06", DoorDirection.right, False, False),

    "3a_roof07_west": Door("3a_roof07_west", "3a_roof07", DoorDirection.left, False, False),

    "3b_00_west": Door("3b_00_west", "3b_00", DoorDirection.left, False, False),
    "3b_00_east": Door("3b_00_east", "3b_00", DoorDirection.right, False, False),

    "3b_back_east": Door("3b_back_east", "3b_back", DoorDirection.right, False, False),

    "3b_01_west": Door("3b_01_west", "3b_01", DoorDirection.left, False, False),
    "3b_01_east": Door("3b_01_east", "3b_01", DoorDirection.right, False, False),

    "3b_02_west": Door("3b_02_west", "3b_02", DoorDirection.left, False, True),
    "3b_02_east": Door("3b_02_east", "3b_02", DoorDirection.right, False, False),

    "3b_03_west": Door("3b_03_west", "3b_03", DoorDirection.left, False, False),
    "3b_03_east": Door("3b_03_east", "3b_03", DoorDirection.right, False, False),

    "3b_04_west": Door("3b_04_west", "3b_04", DoorDirection.left, False, False),
    "3b_04_east": Door("3b_04_east", "3b_04", DoorDirection.right, False, False),

    "3b_05_west": Door("3b_05_west", "3b_05", DoorDirection.left, False, False),
    "3b_05_east": Door("3b_05_east", "3b_05", DoorDirection.right, False, False),

    "3b_06_west": Door("3b_06_west", "3b_06", DoorDirection.left, False, True),
    "3b_06_east": Door("3b_06_east", "3b_06", DoorDirection.right, False, False),

    "3b_07_west": Door("3b_07_west", "3b_07", DoorDirection.left, False, False),
    "3b_07_east": Door("3b_07_east", "3b_07", DoorDirection.right, False, False),

    "3b_08_bottom": Door("3b_08_bottom", "3b_08", DoorDirection.left, False, False),
    "3b_08_top": Door("3b_08_top", "3b_08", DoorDirection.up, False, False),

    "3b_09_west": Door("3b_09_west", "3b_09", DoorDirection.down, False, True),
    "3b_09_east": Door("3b_09_east", "3b_09", DoorDirection.right, False, False),

    "3b_10_west": Door("3b_10_west", "3b_10", DoorDirection.left, False, False),
    "3b_10_east": Door("3b_10_east", "3b_10", DoorDirection.right, False, False),

    "3b_11_west": Door("3b_11_west", "3b_11", DoorDirection.left, False, True),
    "3b_11_east": Door("3b_11_east", "3b_11", DoorDirection.right, False, False),

    "3b_13_west": Door("3b_13_west", "3b_13", DoorDirection.left, False, False),
    "3b_13_east": Door("3b_13_east", "3b_13", DoorDirection.right, False, False),

    "3b_14_west": Door("3b_14_west", "3b_14", DoorDirection.left, False, False),
    "3b_14_east": Door("3b_14_east", "3b_14", DoorDirection.right, False, False),

    "3b_15_west": Door("3b_15_west", "3b_15", DoorDirection.left, False, False),
    "3b_15_east": Door("3b_15_east", "3b_15", DoorDirection.right, False, False),

    "3b_12_west": Door("3b_12_west", "3b_12", DoorDirection.left, False, False),
    "3b_12_east": Door("3b_12_east", "3b_12", DoorDirection.right, False, False),

    "3b_16_west": Door("3b_16_west", "3b_16", DoorDirection.left, False, True),
    "3b_16_top": Door("3b_16_top", "3b_16", DoorDirection.up, True, False),

    "3b_17_west": Door("3b_17_west", "3b_17", DoorDirection.down, False, True),
    "3b_17_east": Door("3b_17_east", "3b_17", DoorDirection.right, False, False),

    "3b_18_west": Door("3b_18_west", "3b_18", DoorDirection.left, False, False),
    "3b_18_east": Door("3b_18_east", "3b_18", DoorDirection.right, False, False),

    "3b_19_west": Door("3b_19_west", "3b_19", DoorDirection.left, False, False),
    "3b_19_east": Door("3b_19_east", "3b_19", DoorDirection.right, False, False),

    "3b_21_west": Door("3b_21_west", "3b_21", DoorDirection.left, False, False),
    "3b_21_east": Door("3b_21_east", "3b_21", DoorDirection.right, False, False),

    "3b_20_west": Door("3b_20_west", "3b_20", DoorDirection.left, False, False),
    "3b_20_east": Door("3b_20_east", "3b_20", DoorDirection.down, False, False),

    "3b_end_west": Door("3b_end_west", "3b_end", DoorDirection.up, False, True),

    "3c_00_east": Door("3c_00_east", "3c_00", DoorDirection.up, False, False),

    "3c_01_west": Door("3c_01_west", "3c_01", DoorDirection.down, False, False),
    "3c_01_east": Door("3c_01_east", "3c_01", DoorDirection.right, False, False),

    "3c_02_west": Door("3c_02_west", "3c_02", DoorDirection.left, False, True),

    "4a_a-00_east": Door("4a_a-00_east", "4a_a-00", DoorDirection.right, False, False),

    "4a_a-01_west": Door("4a_a-01_west", "4a_a-01", DoorDirection.left, False, False),
    "4a_a-01_east": Door("4a_a-01_east", "4a_a-01", DoorDirection.right, False, False),

    "4a_a-01x_west": Door("4a_a-01x_west", "4a_a-01x", DoorDirection.left, False, False),
    "4a_a-01x_east": Door("4a_a-01x_east", "4a_a-01x", DoorDirection.right, False, False),

    "4a_a-02_west": Door("4a_a-02_west", "4a_a-02", DoorDirection.left, False, False),
    "4a_a-02_east": Door("4a_a-02_east", "4a_a-02", DoorDirection.right, False, False),

    "4a_a-03_west": Door("4a_a-03_west", "4a_a-03", DoorDirection.left, False, False),
    "4a_a-03_east": Door("4a_a-03_east", "4a_a-03", DoorDirection.right, False, False),

    "4a_a-04_west": Door("4a_a-04_west", "4a_a-04", DoorDirection.left, False, False),
    "4a_a-04_east": Door("4a_a-04_east", "4a_a-04", DoorDirection.right, False, False),

    "4a_a-05_west": Door("4a_a-05_west", "4a_a-05", DoorDirection.left, False, False),
    "4a_a-05_east": Door("4a_a-05_east", "4a_a-05", DoorDirection.right, False, False),

    "4a_a-06_west": Door("4a_a-06_west", "4a_a-06", DoorDirection.left, False, False),
    "4a_a-06_east": Door("4a_a-06_east", "4a_a-06", DoorDirection.right, False, False),

    "4a_a-07_west": Door("4a_a-07_west", "4a_a-07", DoorDirection.left, False, False),
    "4a_a-07_east": Door("4a_a-07_east", "4a_a-07", DoorDirection.right, False, False),

    "4a_a-08_west": Door("4a_a-08_west", "4a_a-08", DoorDirection.left, False, False),
    "4a_a-08_north-west": Door("4a_a-08_north-west", "4a_a-08", DoorDirection.left, False, False),
    "4a_a-08_east": Door("4a_a-08_east", "4a_a-08", DoorDirection.up, False, False),

    "4a_a-10_west": Door("4a_a-10_west", "4a_a-10", DoorDirection.left, False, False),
    "4a_a-10_east": Door("4a_a-10_east", "4a_a-10", DoorDirection.right, False, False),

    "4a_a-11_east": Door("4a_a-11_east", "4a_a-11", DoorDirection.right, False, False),

    "4a_a-09_bottom": Door("4a_a-09_bottom", "4a_a-09", DoorDirection.down, False, True),
    "4a_a-09_top": Door("4a_a-09_top", "4a_a-09", DoorDirection.up, False, False),

    "4a_b-00_south": Door("4a_b-00_south", "4a_b-00", DoorDirection.down, False, True),
    "4a_b-00_south-east": Door("4a_b-00_south-east", "4a_b-00", DoorDirection.right, False, False),
    "4a_b-00_east": Door("4a_b-00_east", "4a_b-00", DoorDirection.right, False, False),
    "4a_b-00_north-east": Door("4a_b-00_north-east", "4a_b-00", DoorDirection.right, False, False),
    "4a_b-00_west": Door("4a_b-00_west", "4a_b-00", DoorDirection.left, False, False),
    "4a_b-00_north-west": Door("4a_b-00_north-west", "4a_b-00", DoorDirection.left, False, False),
    "4a_b-00_north": Door("4a_b-00_north", "4a_b-00", DoorDirection.up, False, False),

    "4a_b-01_west": Door("4a_b-01_west", "4a_b-01", DoorDirection.left, False, False),

    "4a_b-04_west": Door("4a_b-04_west", "4a_b-04", DoorDirection.left, False, False),
    "4a_b-04_north-west": Door("4a_b-04_north-west", "4a_b-04", DoorDirection.up, False, False),
    "4a_b-04_east": Door("4a_b-04_east", "4a_b-04", DoorDirection.right, False, False),

    "4a_b-06_west": Door("4a_b-06_west", "4a_b-06", DoorDirection.down, False, False),
    "4a_b-06_east": Door("4a_b-06_east", "4a_b-06", DoorDirection.right, False, False),

    "4a_b-07_west": Door("4a_b-07_west", "4a_b-07", DoorDirection.up, False, False),
    "4a_b-07_east": Door("4a_b-07_east", "4a_b-07", DoorDirection.right, False, False),

    "4a_b-03_west": Door("4a_b-03_west", "4a_b-03", DoorDirection.left, False, False),
    "4a_b-03_east": Door("4a_b-03_east", "4a_b-03", DoorDirection.right, False, False),

    "4a_b-02_south-west": Door("4a_b-02_south-west", "4a_b-02", DoorDirection.left, False, False),
    "4a_b-02_north-west": Door("4a_b-02_north-west", "4a_b-02", DoorDirection.left, False, False),
    "4a_b-02_north-east": Door("4a_b-02_north-east", "4a_b-02", DoorDirection.right, True, False),
    "4a_b-02_north": Door("4a_b-02_north", "4a_b-02", DoorDirection.up, False, False),

    "4a_b-sec_west": Door("4a_b-sec_west", "4a_b-sec", DoorDirection.left, False, False),
    "4a_b-sec_east": Door("4a_b-sec_east", "4a_b-sec", DoorDirection.right, True, False),

    "4a_b-secb_west": Door("4a_b-secb_west", "4a_b-secb", DoorDirection.left, False, False),

    "4a_b-05_west": Door("4a_b-05_west", "4a_b-05", DoorDirection.down, False, False),
    "4a_b-05_center": Door("4a_b-05_center", "4a_b-05", DoorDirection.down, False, True),
    "4a_b-05_north-east": Door("4a_b-05_north-east", "4a_b-05", DoorDirection.up, False, False),
    "4a_b-05_east": Door("4a_b-05_east", "4a_b-05", DoorDirection.down, False, False),

    "4a_b-08b_west": Door("4a_b-08b_west", "4a_b-08b", DoorDirection.down, False, False),
    "4a_b-08b_east": Door("4a_b-08b_east", "4a_b-08b", DoorDirection.up, False, False),

    "4a_b-08_west": Door("4a_b-08_west", "4a_b-08", DoorDirection.down, False, False),
    "4a_b-08_east": Door("4a_b-08_east", "4a_b-08", DoorDirection.up, False, False),

    "4a_c-00_west": Door("4a_c-00_west", "4a_c-00", DoorDirection.down, False, True),
    "4a_c-00_north-west": Door("4a_c-00_north-west", "4a_c-00", DoorDirection.left, False, False),
    "4a_c-00_east": Door("4a_c-00_east", "4a_c-00", DoorDirection.right, False, False),

    "4a_c-01_east": Door("4a_c-01_east", "4a_c-01", DoorDirection.right, False, False),

    "4a_c-02_west": Door("4a_c-02_west", "4a_c-02", DoorDirection.left, False, False),
    "4a_c-02_east": Door("4a_c-02_east", "4a_c-02", DoorDirection.up, False, False),

    "4a_c-04_west": Door("4a_c-04_west", "4a_c-04", DoorDirection.down, False, True),
    "4a_c-04_east": Door("4a_c-04_east", "4a_c-04", DoorDirection.right, False, False),

    "4a_c-05_west": Door("4a_c-05_west", "4a_c-05", DoorDirection.left, False, False),
    "4a_c-05_east": Door("4a_c-05_east", "4a_c-05", DoorDirection.up, False, False),

    "4a_c-06_bottom": Door("4a_c-06_bottom", "4a_c-06", DoorDirection.down, False, False),
    "4a_c-06_west": Door("4a_c-06_west", "4a_c-06", DoorDirection.left, False, False),
    "4a_c-06_top": Door("4a_c-06_top", "4a_c-06", DoorDirection.up, False, False),

    "4a_c-06b_east": Door("4a_c-06b_east", "4a_c-06b", DoorDirection.right, False, False),

    "4a_c-09_west": Door("4a_c-09_west", "4a_c-09", DoorDirection.down, False, True),
    "4a_c-09_east": Door("4a_c-09_east", "4a_c-09", DoorDirection.up, False, False),

    "4a_c-07_west": Door("4a_c-07_west", "4a_c-07", DoorDirection.down, False, True),
    "4a_c-07_east": Door("4a_c-07_east", "4a_c-07", DoorDirection.right, False, False),

    "4a_c-08_bottom": Door("4a_c-08_bottom", "4a_c-08", DoorDirection.left, False, False),
    "4a_c-08_east": Door("4a_c-08_east", "4a_c-08", DoorDirection.right, False, False),
    "4a_c-08_top": Door("4a_c-08_top", "4a_c-08", DoorDirection.up, False, False),

    "4a_c-10_bottom": Door("4a_c-10_bottom", "4a_c-10", DoorDirection.left, False, False),
    "4a_c-10_top": Door("4a_c-10_top", "4a_c-10", DoorDirection.up, False, False),

    "4a_d-00_west": Door("4a_d-00_west", "4a_d-00", DoorDirection.down, False, True),
    "4a_d-00_south": Door("4a_d-00_south", "4a_d-00", DoorDirection.down, False, True),
    "4a_d-00_north-west": Door("4a_d-00_north-west", "4a_d-00", DoorDirection.left, False, False),
    "4a_d-00_east": Door("4a_d-00_east", "4a_d-00", DoorDirection.right, False, False),

    "4a_d-00b_east": Door("4a_d-00b_east", "4a_d-00b", DoorDirection.right, False, False),

    "4a_d-01_west": Door("4a_d-01_west", "4a_d-01", DoorDirection.left, False, False),
    "4a_d-01_east": Door("4a_d-01_east", "4a_d-01", DoorDirection.right, False, False),

    "4a_d-02_west": Door("4a_d-02_west", "4a_d-02", DoorDirection.left, False, False),
    "4a_d-02_east": Door("4a_d-02_east", "4a_d-02", DoorDirection.right, False, False),

    "4a_d-03_west": Door("4a_d-03_west", "4a_d-03", DoorDirection.left, False, False),
    "4a_d-03_east": Door("4a_d-03_east", "4a_d-03", DoorDirection.right, False, False),

    "4a_d-04_west": Door("4a_d-04_west", "4a_d-04", DoorDirection.left, False, False),
    "4a_d-04_east": Door("4a_d-04_east", "4a_d-04", DoorDirection.right, False, False),

    "4a_d-05_west": Door("4a_d-05_west", "4a_d-05", DoorDirection.left, False, False),
    "4a_d-05_east": Door("4a_d-05_east", "4a_d-05", DoorDirection.right, False, False),

    "4a_d-06_west": Door("4a_d-06_west", "4a_d-06", DoorDirection.left, False, False),
    "4a_d-06_east": Door("4a_d-06_east", "4a_d-06", DoorDirection.right, False, False),

    "4a_d-07_west": Door("4a_d-07_west", "4a_d-07", DoorDirection.left, False, False),
    "4a_d-07_east": Door("4a_d-07_east", "4a_d-07", DoorDirection.right, False, False),

    "4a_d-08_west": Door("4a_d-08_west", "4a_d-08", DoorDirection.left, False, False),
    "4a_d-08_east": Door("4a_d-08_east", "4a_d-08", DoorDirection.right, False, False),

    "4a_d-09_west": Door("4a_d-09_west", "4a_d-09", DoorDirection.left, False, False),
    "4a_d-09_east": Door("4a_d-09_east", "4a_d-09", DoorDirection.right, False, False),

    "4a_d-10_west": Door("4a_d-10_west", "4a_d-10", DoorDirection.left, False, True),

    "4b_a-00_east": Door("4b_a-00_east", "4b_a-00", DoorDirection.right, False, False),

    "4b_a-01_west": Door("4b_a-01_west", "4b_a-01", DoorDirection.left, False, False),
    "4b_a-01_east": Door("4b_a-01_east", "4b_a-01", DoorDirection.right, False, False),

    "4b_a-02_west": Door("4b_a-02_west", "4b_a-02", DoorDirection.left, False, False),
    "4b_a-02_east": Door("4b_a-02_east", "4b_a-02", DoorDirection.right, False, False),

    "4b_a-03_west": Door("4b_a-03_west", "4b_a-03", DoorDirection.left, False, False),
    "4b_a-03_east": Door("4b_a-03_east", "4b_a-03", DoorDirection.right, False, False),

    "4b_a-04_west": Door("4b_a-04_west", "4b_a-04", DoorDirection.left, False, False),
    "4b_a-04_east": Door("4b_a-04_east", "4b_a-04", DoorDirection.right, False, False),

    "4b_b-00_west": Door("4b_b-00_west", "4b_b-00", DoorDirection.left, False, False),
    "4b_b-00_east": Door("4b_b-00_east", "4b_b-00", DoorDirection.right, False, False),

    "4b_b-01_west": Door("4b_b-01_west", "4b_b-01", DoorDirection.left, False, False),
    "4b_b-01_east": Door("4b_b-01_east", "4b_b-01", DoorDirection.up, False, False),

    "4b_b-02_bottom": Door("4b_b-02_bottom", "4b_b-02", DoorDirection.down, False, True),
    "4b_b-02_top": Door("4b_b-02_top", "4b_b-02", DoorDirection.up, False, False),

    "4b_b-03_west": Door("4b_b-03_west", "4b_b-03", DoorDirection.down, False, True),
    "4b_b-03_east": Door("4b_b-03_east", "4b_b-03", DoorDirection.up, False, False),

    "4b_b-04_west": Door("4b_b-04_west", "4b_b-04", DoorDirection.down, False, True),
    "4b_b-04_east": Door("4b_b-04_east", "4b_b-04", DoorDirection.right, False, False),

    "4b_c-00_west": Door("4b_c-00_west", "4b_c-00", DoorDirection.left, False, True),
    "4b_c-00_east": Door("4b_c-00_east", "4b_c-00", DoorDirection.right, False, False),

    "4b_c-01_west": Door("4b_c-01_west", "4b_c-01", DoorDirection.left, False, False),
    "4b_c-01_east": Door("4b_c-01_east", "4b_c-01", DoorDirection.right, False, False),

    "4b_c-02_west": Door("4b_c-02_west", "4b_c-02", DoorDirection.left, False, False),
    "4b_c-02_east": Door("4b_c-02_east", "4b_c-02", DoorDirection.right, False, False),

    "4b_c-03_bottom": Door("4b_c-03_bottom", "4b_c-03", DoorDirection.left, False, False),
    "4b_c-03_top": Door("4b_c-03_top", "4b_c-03", DoorDirection.up, False, False),

    "4b_c-04_west": Door("4b_c-04_west", "4b_c-04", DoorDirection.down, False, True),
    "4b_c-04_east": Door("4b_c-04_east", "4b_c-04", DoorDirection.right, False, False),

    "4b_d-00_west": Door("4b_d-00_west", "4b_d-00", DoorDirection.left, False, False),
    "4b_d-00_east": Door("4b_d-00_east", "4b_d-00", DoorDirection.right, False, False),

    "4b_d-01_west": Door("4b_d-01_west", "4b_d-01", DoorDirection.left, False, False),
    "4b_d-01_east": Door("4b_d-01_east", "4b_d-01", DoorDirection.right, False, False),

    "4b_d-02_west": Door("4b_d-02_west", "4b_d-02", DoorDirection.left, False, False),
    "4b_d-02_east": Door("4b_d-02_east", "4b_d-02", DoorDirection.right, False, False),

    "4b_d-03_west": Door("4b_d-03_west", "4b_d-03", DoorDirection.left, False, False),
    "4b_d-03_east": Door("4b_d-03_east", "4b_d-03", DoorDirection.right, False, False),

    "4b_end_west": Door("4b_end_west", "4b_end", DoorDirection.left, False, False),

    "4c_00_east": Door("4c_00_east", "4c_00", DoorDirection.right, False, False),

    "4c_01_west": Door("4c_01_west", "4c_01", DoorDirection.left, False, False),
    "4c_01_east": Door("4c_01_east", "4c_01", DoorDirection.right, False, False),

    "4c_02_west": Door("4c_02_west", "4c_02", DoorDirection.left, False, False),

}

all_region_connections: Dict[str, RegionConnection] = {
    "0a_-1_main---0a_-1_east": RegionConnection("0a_-1_main", "0a_-1_east", []),
    "0a_-1_east---0a_-1_main": RegionConnection("0a_-1_east", "0a_-1_main", []),

    "0a_0_west---0a_0_main": RegionConnection("0a_0_west", "0a_0_main", []),
    "0a_0_main---0a_0_west": RegionConnection("0a_0_main", "0a_0_west", []),
    "0a_0_main---0a_0_east": RegionConnection("0a_0_main", "0a_0_east", []),
    "0a_0_main---0a_0_north": RegionConnection("0a_0_main", "0a_0_north", []),
    "0a_0_north---0a_0_main": RegionConnection("0a_0_north", "0a_0_main", []),
    "0a_0_east---0a_0_main": RegionConnection("0a_0_east", "0a_0_main", []),


    "0a_1_west---0a_1_main": RegionConnection("0a_1_west", "0a_1_main", []),
    "0a_1_main---0a_1_west": RegionConnection("0a_1_main", "0a_1_west", []),
    "0a_1_main---0a_1_east": RegionConnection("0a_1_main", "0a_1_east", []),
    "0a_1_east---0a_1_main": RegionConnection("0a_1_east", "0a_1_main", []),

    "0a_2_west---0a_2_main": RegionConnection("0a_2_west", "0a_2_main", []),
    "0a_2_main---0a_2_west": RegionConnection("0a_2_main", "0a_2_west", []),
    "0a_2_main---0a_2_east": RegionConnection("0a_2_main", "0a_2_east", []),
    "0a_2_east---0a_2_main": RegionConnection("0a_2_east", "0a_2_main", []),

    "0a_3_west---0a_3_main": RegionConnection("0a_3_west", "0a_3_main", []),
    "0a_3_main---0a_3_west": RegionConnection("0a_3_main", "0a_3_west", []),
    "0a_3_main---0a_3_east": RegionConnection("0a_3_main", "0a_3_east", []),
    "0a_3_east---0a_3_main": RegionConnection("0a_3_east", "0a_3_main", []),

    "1a_1_main---1a_1_east": RegionConnection("1a_1_main", "1a_1_east", []),
    "1a_1_east---1a_1_main": RegionConnection("1a_1_east", "1a_1_main", []),

    "1a_2_west---1a_2_east": RegionConnection("1a_2_west", "1a_2_east", []),
    "1a_2_east---1a_2_west": RegionConnection("1a_2_east", "1a_2_west", []),

    "1a_3_west---1a_3_east": RegionConnection("1a_3_west", "1a_3_east", []),
    "1a_3_east---1a_3_west": RegionConnection("1a_3_east", "1a_3_west", []),

    "1a_4_west---1a_4_east": RegionConnection("1a_4_west", "1a_4_east", [[ItemName.traffic_blocks, ], ]),
    "1a_4_east---1a_4_west": RegionConnection("1a_4_east", "1a_4_west", []),

    "1a_3b_west---1a_3b_east": RegionConnection("1a_3b_west", "1a_3b_east", []),
    "1a_3b_east---1a_3b_west": RegionConnection("1a_3b_east", "1a_3b_west", []),
    "1a_3b_east---1a_3b_top": RegionConnection("1a_3b_east", "1a_3b_top", []),
    "1a_3b_top---1a_3b_west": RegionConnection("1a_3b_top", "1a_3b_west", []),
    "1a_3b_top---1a_3b_east": RegionConnection("1a_3b_top", "1a_3b_east", []),

    "1a_5_bottom---1a_5_west": RegionConnection("1a_5_bottom", "1a_5_west", []),
    "1a_5_bottom---1a_5_north-west": RegionConnection("1a_5_bottom", "1a_5_north-west", [[ItemName.traffic_blocks, ], ]),
    "1a_5_bottom---1a_5_center": RegionConnection("1a_5_bottom", "1a_5_center", []),
    "1a_5_west---1a_5_bottom": RegionConnection("1a_5_west", "1a_5_bottom", []),
    "1a_5_north-west---1a_5_center": RegionConnection("1a_5_north-west", "1a_5_center", []),
    "1a_5_north-west---1a_5_bottom": RegionConnection("1a_5_north-west", "1a_5_bottom", []),
    "1a_5_center---1a_5_north-east": RegionConnection("1a_5_center", "1a_5_north-east", []),
    "1a_5_center---1a_5_bottom": RegionConnection("1a_5_center", "1a_5_bottom", []),
    "1a_5_center---1a_5_south-east": RegionConnection("1a_5_center", "1a_5_south-east", []),
    "1a_5_south-east---1a_5_north-east": RegionConnection("1a_5_south-east", "1a_5_north-east", []),
    "1a_5_south-east---1a_5_center": RegionConnection("1a_5_south-east", "1a_5_center", []),
    "1a_5_north-east---1a_5_center": RegionConnection("1a_5_north-east", "1a_5_center", []),
    "1a_5_north-east---1a_5_top": RegionConnection("1a_5_north-east", "1a_5_top", [[ItemName.springs, ], ]),
    "1a_5_top---1a_5_north-east": RegionConnection("1a_5_top", "1a_5_north-east", []),



    "1a_6_south-west---1a_6_west": RegionConnection("1a_6_south-west", "1a_6_west", []),
    "1a_6_west---1a_6_south-west": RegionConnection("1a_6_west", "1a_6_south-west", []),
    "1a_6_west---1a_6_east": RegionConnection("1a_6_west", "1a_6_east", [[ItemName.dash_refills, ], ]),
    "1a_6_east---1a_6_west": RegionConnection("1a_6_east", "1a_6_west", [[ItemName.cannot_access, ], ]),

    "1a_6z_north-west---1a_6z_west": RegionConnection("1a_6z_north-west", "1a_6z_west", []),
    "1a_6z_west---1a_6z_north-west": RegionConnection("1a_6z_west", "1a_6z_north-west", []),
    "1a_6z_west---1a_6z_east": RegionConnection("1a_6z_west", "1a_6z_east", []),
    "1a_6z_east---1a_6z_west": RegionConnection("1a_6z_east", "1a_6z_west", [[ItemName.dash_refills, ], ]),

    "1a_6zb_north-west---1a_6zb_main": RegionConnection("1a_6zb_north-west", "1a_6zb_main", []),
    "1a_6zb_main---1a_6zb_north-west": RegionConnection("1a_6zb_main", "1a_6zb_north-west", []),
    "1a_6zb_main---1a_6zb_east": RegionConnection("1a_6zb_main", "1a_6zb_east", []),
    "1a_6zb_east---1a_6zb_main": RegionConnection("1a_6zb_east", "1a_6zb_main", []),

    "1a_7zb_west---1a_7zb_east": RegionConnection("1a_7zb_west", "1a_7zb_east", [[ItemName.dash_refills, ], ]),
    "1a_7zb_east---1a_7zb_west": RegionConnection("1a_7zb_east", "1a_7zb_west", [[ItemName.springs, ItemName.dash_refills, ], ]),

    "1a_6a_west---1a_6a_east": RegionConnection("1a_6a_west", "1a_6a_east", [[ItemName.dash_refills, ], ]),
    "1a_6a_east---1a_6a_west": RegionConnection("1a_6a_east", "1a_6a_west", []),

    "1a_6b_south-west---1a_6b_north-west": RegionConnection("1a_6b_south-west", "1a_6b_north-west", [[ItemName.traffic_blocks, ], ]),
    "1a_6b_south-west---1a_6b_north-east": RegionConnection("1a_6b_south-west", "1a_6b_north-east", [[ItemName.traffic_blocks, ], ]),
    "1a_6b_north-west---1a_6b_south-west": RegionConnection("1a_6b_north-west", "1a_6b_south-west", []),
    "1a_6b_north-east---1a_6b_south-west": RegionConnection("1a_6b_north-east", "1a_6b_south-west", []),

    "1a_s0_west---1a_s0_east": RegionConnection("1a_s0_west", "1a_s0_east", []),
    "1a_s0_east---1a_s0_west": RegionConnection("1a_s0_east", "1a_s0_west", [[ItemName.traffic_blocks, ], ]),


    "1a_6c_south-west---1a_6c_north-west": RegionConnection("1a_6c_south-west", "1a_6c_north-west", [[ItemName.springs, ], ]),
    "1a_6c_south-west---1a_6c_north-east": RegionConnection("1a_6c_south-west", "1a_6c_north-east", [[ItemName.springs, ], ]),
    "1a_6c_north-west---1a_6c_south-west": RegionConnection("1a_6c_north-west", "1a_6c_south-west", []),
    "1a_6c_north-west---1a_6c_north-east": RegionConnection("1a_6c_north-west", "1a_6c_north-east", [[ItemName.dash_refills, ], ]),
    "1a_6c_north-east---1a_6c_south-west": RegionConnection("1a_6c_north-east", "1a_6c_south-west", []),

    "1a_7_west---1a_7_east": RegionConnection("1a_7_west", "1a_7_east", []),
    "1a_7_east---1a_7_west": RegionConnection("1a_7_east", "1a_7_west", []),

    "1a_7z_bottom---1a_7z_top": RegionConnection("1a_7z_bottom", "1a_7z_top", []),
    "1a_7z_top---1a_7z_bottom": RegionConnection("1a_7z_top", "1a_7z_bottom", []),

    "1a_8z_bottom---1a_8z_top": RegionConnection("1a_8z_bottom", "1a_8z_top", [[ItemName.traffic_blocks, ], ]),
    "1a_8z_top---1a_8z_bottom": RegionConnection("1a_8z_top", "1a_8z_bottom", []),

    "1a_8zb_west---1a_8zb_east": RegionConnection("1a_8zb_west", "1a_8zb_east", [[ItemName.dash_refills, ], ]),
    "1a_8zb_east---1a_8zb_west": RegionConnection("1a_8zb_east", "1a_8zb_west", [[ItemName.cannot_access, ], ]),

    "1a_8_south-west---1a_8_south": RegionConnection("1a_8_south-west", "1a_8_south", []),
    "1a_8_south-west---1a_8_north": RegionConnection("1a_8_south-west", "1a_8_north", []),
    "1a_8_west---1a_8_south-west": RegionConnection("1a_8_west", "1a_8_south-west", []),
    "1a_8_south-east---1a_8_north": RegionConnection("1a_8_south-east", "1a_8_north", []),
    "1a_8_south-east---1a_8_south": RegionConnection("1a_8_south-east", "1a_8_south", []),
    "1a_8_north---1a_8_north-east": RegionConnection("1a_8_north", "1a_8_north-east", []),
    "1a_8_north---1a_8_south": RegionConnection("1a_8_north", "1a_8_south", []),
    "1a_8_north-east---1a_8_north": RegionConnection("1a_8_north-east", "1a_8_north", []),

    "1a_7a_east---1a_7a_west": RegionConnection("1a_7a_east", "1a_7a_west", []),
    "1a_7a_west---1a_7a_east": RegionConnection("1a_7a_west", "1a_7a_east", []),


    "1a_8b_east---1a_8b_west": RegionConnection("1a_8b_east", "1a_8b_west", []),
    "1a_8b_west---1a_8b_east": RegionConnection("1a_8b_west", "1a_8b_east", [[ItemName.traffic_blocks, ], ]),

    "1a_9_east---1a_9_west": RegionConnection("1a_9_east", "1a_9_west", [[ItemName.cannot_access, ], ]),
    "1a_9_west---1a_9_east": RegionConnection("1a_9_west", "1a_9_east", [[ItemName.traffic_blocks, ], ]),

    "1a_9b_east---1a_9b_north-east": RegionConnection("1a_9b_east", "1a_9b_north-east", []),
    "1a_9b_north-east---1a_9b_east": RegionConnection("1a_9b_north-east", "1a_9b_east", []),
    "1a_9b_north-east---1a_9b_west": RegionConnection("1a_9b_north-east", "1a_9b_west", []),
    "1a_9b_west---1a_9b_east": RegionConnection("1a_9b_west", "1a_9b_east", [[ItemName.traffic_blocks, ], ]),
    "1a_9b_west---1a_9b_north-west": RegionConnection("1a_9b_west", "1a_9b_north-west", [[ItemName.traffic_blocks, ], ]),
    "1a_9b_north-west---1a_9b_west": RegionConnection("1a_9b_north-west", "1a_9b_west", []),


    "1a_10_south-east---1a_10_south-west": RegionConnection("1a_10_south-east", "1a_10_south-west", []),
    "1a_10_south-east---1a_10_north-west": RegionConnection("1a_10_south-east", "1a_10_north-west", [[ItemName.traffic_blocks, ], ]),
    "1a_10_south-west---1a_10_south-east": RegionConnection("1a_10_south-west", "1a_10_south-east", []),
    "1a_10_north-west---1a_10_south-east": RegionConnection("1a_10_north-west", "1a_10_south-east", []),
    "1a_10_north-east---1a_10_south-east": RegionConnection("1a_10_north-east", "1a_10_south-east", []),

    "1a_10z_west---1a_10z_east": RegionConnection("1a_10z_west", "1a_10z_east", []),
    "1a_10z_east---1a_10z_west": RegionConnection("1a_10z_east", "1a_10z_west", [[ItemName.springs, ], ]),


    "1a_11_south-east---1a_11_north": RegionConnection("1a_11_south-east", "1a_11_north", [[ItemName.traffic_blocks, ItemName.springs, ], ]),
    "1a_11_south-west---1a_11_south": RegionConnection("1a_11_south-west", "1a_11_south", [[ItemName.traffic_blocks, ], ]),
    "1a_11_south-west---1a_11_west": RegionConnection("1a_11_south-west", "1a_11_west", [[ItemName.traffic_blocks, ], ]),
    "1a_11_north---1a_11_south-east": RegionConnection("1a_11_north", "1a_11_south-east", []),
    "1a_11_west---1a_11_south-west": RegionConnection("1a_11_west", "1a_11_south-west", [[ItemName.traffic_blocks, ], ]),
    "1a_11_south---1a_11_south-west": RegionConnection("1a_11_south", "1a_11_south-west", []),


    "1a_10a_bottom---1a_10a_top": RegionConnection("1a_10a_bottom", "1a_10a_top", [[ItemName.dash_refills, ], ]),
    "1a_10a_top---1a_10a_bottom": RegionConnection("1a_10a_top", "1a_10a_bottom", [[ItemName.cannot_access, ], ]),

    "1a_12_south-west---1a_12_north-west": RegionConnection("1a_12_south-west", "1a_12_north-west", []),
    "1a_12_south-west---1a_12_east": RegionConnection("1a_12_south-west", "1a_12_east", []),
    "1a_12_north-west---1a_12_south-west": RegionConnection("1a_12_north-west", "1a_12_south-west", []),


    "1a_12a_bottom---1a_12a_top": RegionConnection("1a_12a_bottom", "1a_12a_top", [[ItemName.traffic_blocks, ], ]),
    "1a_12a_top---1a_12a_bottom": RegionConnection("1a_12a_top", "1a_12a_bottom", []),

    "1a_end_south---1a_end_main": RegionConnection("1a_end_south", "1a_end_main", []),
    "1a_end_main---1a_end_south": RegionConnection("1a_end_main", "1a_end_south", []),

    "1b_00_west---1b_00_east": RegionConnection("1b_00_west", "1b_00_east", []),
    "1b_00_east---1b_00_west": RegionConnection("1b_00_east", "1b_00_west", []),

    "1b_01_west---1b_01_east": RegionConnection("1b_01_west", "1b_01_east", [[ItemName.traffic_blocks, ], ]),
    "1b_01_east---1b_01_west": RegionConnection("1b_01_east", "1b_01_west", [[ItemName.cannot_access, ], ]),

    "1b_02_west---1b_02_east": RegionConnection("1b_02_west", "1b_02_east", [[ItemName.traffic_blocks, ], ]),
    "1b_02_east---1b_02_west": RegionConnection("1b_02_east", "1b_02_west", [[ItemName.cannot_access, ], ]),

    "1b_02b_west---1b_02b_east": RegionConnection("1b_02b_west", "1b_02b_east", [[ItemName.traffic_blocks, ], ]),
    "1b_02b_east---1b_02b_west": RegionConnection("1b_02b_east", "1b_02b_west", [[ItemName.cannot_access, ], ]),

    "1b_03_west---1b_03_east": RegionConnection("1b_03_west", "1b_03_east", [[ItemName.traffic_blocks, ItemName.dash_refills, ], ]),
    "1b_03_east---1b_03_west": RegionConnection("1b_03_east", "1b_03_west", [[ItemName.cannot_access, ], ]),

    "1b_04_west---1b_04_east": RegionConnection("1b_04_west", "1b_04_east", [[ItemName.traffic_blocks, ItemName.springs, ], ]),
    "1b_04_east---1b_04_west": RegionConnection("1b_04_east", "1b_04_west", [[ItemName.cannot_access, ], ]),

    "1b_05_west---1b_05_east": RegionConnection("1b_05_west", "1b_05_east", [[ItemName.traffic_blocks, ], ]),
    "1b_05_east---1b_05_west": RegionConnection("1b_05_east", "1b_05_west", [[ItemName.cannot_access, ], ]),

    "1b_05b_west---1b_05b_east": RegionConnection("1b_05b_west", "1b_05b_east", [[ItemName.springs, ItemName.dash_refills, ], ]),
    "1b_05b_east---1b_05b_west": RegionConnection("1b_05b_east", "1b_05b_west", [[ItemName.cannot_access, ], ]),

    "1b_06_west---1b_06_east": RegionConnection("1b_06_west", "1b_06_east", [[ItemName.springs, ItemName.dash_refills, ], ]),
    "1b_06_east---1b_06_west": RegionConnection("1b_06_east", "1b_06_west", [[ItemName.cannot_access, ], ]),

    "1b_07_bottom---1b_07_top": RegionConnection("1b_07_bottom", "1b_07_top", [[ItemName.traffic_blocks, ], ]),
    "1b_07_top---1b_07_bottom": RegionConnection("1b_07_top", "1b_07_bottom", []),

    "1b_08_west---1b_08_east": RegionConnection("1b_08_west", "1b_08_east", [[ItemName.traffic_blocks, ], ]),

    "1b_08b_west---1b_08b_east": RegionConnection("1b_08b_west", "1b_08b_east", [[ItemName.traffic_blocks, ItemName.dash_refills, ], ]),
    "1b_08b_east---1b_08b_west": RegionConnection("1b_08b_east", "1b_08b_west", [[ItemName.cannot_access, ], ]),

    "1b_09_west---1b_09_east": RegionConnection("1b_09_west", "1b_09_east", [[ItemName.traffic_blocks, ], ]),
    "1b_09_east---1b_09_west": RegionConnection("1b_09_east", "1b_09_west", []),

    "1b_10_west---1b_10_east": RegionConnection("1b_10_west", "1b_10_east", [[ItemName.traffic_blocks, ItemName.dash_refills, ], ]),

    "1b_11_bottom---1b_11_top": RegionConnection("1b_11_bottom", "1b_11_top", [[ItemName.traffic_blocks, ItemName.dash_refills, ], ]),
    "1b_11_top---1b_11_bottom": RegionConnection("1b_11_top", "1b_11_bottom", []),

    "1b_end_west---1b_end_goal": RegionConnection("1b_end_west", "1b_end_goal", [[ItemName.pink_cassette_blocks, ItemName.blue_cassette_blocks, ItemName.dash_refills, ], ]),

    "1c_00_west---1c_00_east": RegionConnection("1c_00_west", "1c_00_east", [[ItemName.traffic_blocks, ItemName.dash_refills, ], ]),
    "1c_00_east---1c_00_west": RegionConnection("1c_00_east", "1c_00_west", [[ItemName.cannot_access, ], ]),

    "1c_01_west---1c_01_east": RegionConnection("1c_01_west", "1c_01_east", [[ItemName.traffic_blocks, ], ]),
    "1c_01_east---1c_01_west": RegionConnection("1c_01_east", "1c_01_west", []),

    "1c_02_west---1c_02_goal": RegionConnection("1c_02_west", "1c_02_goal", [[ItemName.coins, ItemName.traffic_blocks, ], ]),

    "2a_start_main---2a_start_east": RegionConnection("2a_start_main", "2a_start_east", []),
    "2a_start_top---2a_start_east": RegionConnection("2a_start_top", "2a_start_east", []),
    "2a_start_top---2a_start_main": RegionConnection("2a_start_top", "2a_start_main", []),
    "2a_start_east---2a_start_main": RegionConnection("2a_start_east", "2a_start_main", []),
    "2a_start_east---2a_start_top": RegionConnection("2a_start_east", "2a_start_top", []),

    "2a_s0_bottom---2a_s0_top": RegionConnection("2a_s0_bottom", "2a_s0_top", []),
    "2a_s0_top---2a_s0_bottom": RegionConnection("2a_s0_top", "2a_s0_bottom", []),

    "2a_s1_bottom---2a_s1_top": RegionConnection("2a_s1_bottom", "2a_s1_top", []),
    "2a_s1_top---2a_s1_bottom": RegionConnection("2a_s1_top", "2a_s1_bottom", []),


    "2a_0_south-west---2a_0_south-east": RegionConnection("2a_0_south-west", "2a_0_south-east", []),
    "2a_0_south-east---2a_0_north-east": RegionConnection("2a_0_south-east", "2a_0_north-east", [[ItemName.dream_blocks, ], ]),
    "2a_0_south-east---2a_0_south-west": RegionConnection("2a_0_south-east", "2a_0_south-west", []),
    "2a_0_south-east---2a_0_north-west": RegionConnection("2a_0_south-east", "2a_0_north-west", [[ItemName.dream_blocks, ], ]),
    "2a_0_north-west---2a_0_south-west": RegionConnection("2a_0_north-west", "2a_0_south-west", []),
    "2a_0_north-east---2a_0_south-east": RegionConnection("2a_0_north-east", "2a_0_south-east", [[ItemName.dream_blocks, ], ]),
    "2a_0_north-east---2a_0_north-west": RegionConnection("2a_0_north-east", "2a_0_north-west", [[ItemName.dream_blocks, ], ]),

    "2a_1_south-west---2a_1_south": RegionConnection("2a_1_south-west", "2a_1_south", []),
    "2a_1_south---2a_1_south-west": RegionConnection("2a_1_south", "2a_1_south-west", []),
    "2a_1_south---2a_1_south-east": RegionConnection("2a_1_south", "2a_1_south-east", []),
    "2a_1_south-east---2a_1_south": RegionConnection("2a_1_south-east", "2a_1_south", []),

    "2a_d0_north---2a_d0_north-west": RegionConnection("2a_d0_north", "2a_d0_north-west", []),
    "2a_d0_north-west---2a_d0_north": RegionConnection("2a_d0_north-west", "2a_d0_north", []),
    "2a_d0_north-west---2a_d0_west": RegionConnection("2a_d0_north-west", "2a_d0_west", []),
    "2a_d0_north-west---2a_d0_north-east": RegionConnection("2a_d0_north-west", "2a_d0_north-east", [[ItemName.dream_blocks, ], ]),
    "2a_d0_west---2a_d0_north-west": RegionConnection("2a_d0_west", "2a_d0_north-west", []),
    "2a_d0_west---2a_d0_south-west": RegionConnection("2a_d0_west", "2a_d0_south-west", []),
    "2a_d0_west---2a_d0_east": RegionConnection("2a_d0_west", "2a_d0_east", []),
    "2a_d0_south-west---2a_d0_south": RegionConnection("2a_d0_south-west", "2a_d0_south", [[ItemName.dream_blocks, ], ]),
    "2a_d0_south-west---2a_d0_south-east": RegionConnection("2a_d0_south-west", "2a_d0_south-east", []),
    "2a_d0_south-west---2a_d0_south-east": RegionConnection("2a_d0_south-west", "2a_d0_south-east", [[ItemName.cannot_access, ], ]),
    "2a_d0_south---2a_d0_south-west": RegionConnection("2a_d0_south", "2a_d0_south-west", [[ItemName.dream_blocks, ], ]),
    "2a_d0_south-east---2a_d0_south-west": RegionConnection("2a_d0_south-east", "2a_d0_south-west", []),
    "2a_d0_south-east---2a_d0_east": RegionConnection("2a_d0_south-east", "2a_d0_east", []),
    "2a_d0_east---2a_d0_west": RegionConnection("2a_d0_east", "2a_d0_west", [[ItemName.dream_blocks, ], ]),
    "2a_d0_east---2a_d0_south-east": RegionConnection("2a_d0_east", "2a_d0_south-east", []),
    "2a_d0_north-east---2a_d0_north-west": RegionConnection("2a_d0_north-east", "2a_d0_north-west", [[ItemName.dream_blocks, ], ]),

    "2a_d7_west---2a_d7_east": RegionConnection("2a_d7_west", "2a_d7_east", [[ItemName.dash_refills, ], ]),
    "2a_d7_east---2a_d7_west": RegionConnection("2a_d7_east", "2a_d7_west", [[ItemName.cannot_access, ], ]),

    "2a_d8_west---2a_d8_south-east": RegionConnection("2a_d8_west", "2a_d8_south-east", [[ItemName.dash_refills, ], ]),
    "2a_d8_south-east---2a_d8_west": RegionConnection("2a_d8_south-east", "2a_d8_west", [[ItemName.cannot_access, ], ]),
    "2a_d8_south-east---2a_d8_north-east": RegionConnection("2a_d8_south-east", "2a_d8_north-east", []),

    "2a_d3_west---2a_d3_north": RegionConnection("2a_d3_west", "2a_d3_north", [[ItemName.dream_blocks, ], ]),
    "2a_d3_north---2a_d3_west": RegionConnection("2a_d3_north", "2a_d3_west", [[ItemName.dream_blocks, ], ]),

    "2a_d2_west---2a_d2_east": RegionConnection("2a_d2_west", "2a_d2_east", []),
    "2a_d2_north-west---2a_d2_west": RegionConnection("2a_d2_north-west", "2a_d2_west", []),
    "2a_d2_east---2a_d2_west": RegionConnection("2a_d2_east", "2a_d2_west", []),


    "2a_d1_south-west---2a_d1_south-east": RegionConnection("2a_d1_south-west", "2a_d1_south-east", []),
    "2a_d1_south-west---2a_d1_north-east": RegionConnection("2a_d1_south-west", "2a_d1_north-east", []),
    "2a_d1_south-east---2a_d1_south-west": RegionConnection("2a_d1_south-east", "2a_d1_south-west", []),
    "2a_d1_south-east---2a_d1_north-east": RegionConnection("2a_d1_south-east", "2a_d1_north-east", []),
    "2a_d1_north-east---2a_d1_south-west": RegionConnection("2a_d1_north-east", "2a_d1_south-west", []),
    "2a_d1_north-east---2a_d1_south-east": RegionConnection("2a_d1_north-east", "2a_d1_south-east", []),

    "2a_d6_west---2a_d6_east": RegionConnection("2a_d6_west", "2a_d6_east", []),
    "2a_d6_east---2a_d6_west": RegionConnection("2a_d6_east", "2a_d6_west", [[ItemName.cannot_access, ], ]),

    "2a_d4_west---2a_d4_east": RegionConnection("2a_d4_west", "2a_d4_east", []),
    "2a_d4_west---2a_d4_south": RegionConnection("2a_d4_west", "2a_d4_south", [[ItemName.dream_blocks, ], ]),
    "2a_d4_east---2a_d4_west": RegionConnection("2a_d4_east", "2a_d4_west", []),
    "2a_d4_south---2a_d4_west": RegionConnection("2a_d4_south", "2a_d4_west", [[ItemName.dream_blocks, ], ]),


    "2a_3x_bottom---2a_3x_top": RegionConnection("2a_3x_bottom", "2a_3x_top", [[ItemName.dream_blocks, ], ]),
    "2a_3x_top---2a_3x_bottom": RegionConnection("2a_3x_top", "2a_3x_bottom", [[ItemName.dream_blocks, ], ]),

    "2a_3_bottom---2a_3_top": RegionConnection("2a_3_bottom", "2a_3_top", [[ItemName.dream_blocks, ], ]),
    "2a_3_top---2a_3_bottom": RegionConnection("2a_3_top", "2a_3_bottom", [[ItemName.dream_blocks, ], ]),

    "2a_4_bottom---2a_4_top": RegionConnection("2a_4_bottom", "2a_4_top", [[ItemName.dream_blocks, ], ]),
    "2a_4_top---2a_4_bottom": RegionConnection("2a_4_top", "2a_4_bottom", [[ItemName.dream_blocks, ], ]),

    "2a_5_bottom---2a_5_top": RegionConnection("2a_5_bottom", "2a_5_top", [[ItemName.dream_blocks, ], ]),
    "2a_5_top---2a_5_bottom": RegionConnection("2a_5_top", "2a_5_bottom", [[ItemName.dream_blocks, ], ]),

    "2a_6_bottom---2a_6_top": RegionConnection("2a_6_bottom", "2a_6_top", [[ItemName.dream_blocks, ItemName.coins, ], ]),
    "2a_6_top---2a_6_bottom": RegionConnection("2a_6_top", "2a_6_bottom", [[ItemName.cannot_access, ], ]),

    "2a_7_bottom---2a_7_top": RegionConnection("2a_7_bottom", "2a_7_top", [[ItemName.dream_blocks, ItemName.coins, ], ]),
    "2a_7_top---2a_7_bottom": RegionConnection("2a_7_top", "2a_7_bottom", [[ItemName.cannot_access, ], ]),

    "2a_8_bottom---2a_8_top": RegionConnection("2a_8_bottom", "2a_8_top", [[ItemName.dream_blocks, ], ]),
    "2a_8_top---2a_8_bottom": RegionConnection("2a_8_top", "2a_8_bottom", [[ItemName.cannot_access, ], ]),

    "2a_9_west---2a_9_north": RegionConnection("2a_9_west", "2a_9_north", [[ItemName.dream_blocks, ], ]),
    "2a_9_north---2a_9_south": RegionConnection("2a_9_north", "2a_9_south", [[ItemName.dream_blocks, ], ]),
    "2a_9_north---2a_9_west": RegionConnection("2a_9_north", "2a_9_west", [[ItemName.cannot_access, ], ]),
    "2a_9_north-west---2a_9_west": RegionConnection("2a_9_north-west", "2a_9_west", []),
    "2a_9_south---2a_9_south-east": RegionConnection("2a_9_south", "2a_9_south-east", [[ItemName.coins, ], ]),

    "2a_9b_east---2a_9b_west": RegionConnection("2a_9b_east", "2a_9b_west", []),
    "2a_9b_west---2a_9b_east": RegionConnection("2a_9b_west", "2a_9b_east", []),

    "2a_10_top---2a_10_bottom": RegionConnection("2a_10_top", "2a_10_bottom", [[ItemName.dream_blocks, ItemName.dash_refills, ItemName.coins, ], ]),
    "2a_10_bottom---2a_10_top": RegionConnection("2a_10_bottom", "2a_10_top", [[ItemName.cannot_access, ], ]),

    "2a_2_north-west---2a_2_south-east": RegionConnection("2a_2_north-west", "2a_2_south-east", []),
    "2a_2_south-east---2a_2_north-west": RegionConnection("2a_2_south-east", "2a_2_north-west", []),

    "2a_11_west---2a_11_east": RegionConnection("2a_11_west", "2a_11_east", []),
    "2a_11_east---2a_11_west": RegionConnection("2a_11_east", "2a_11_west", []),

    "2a_12b_west---2a_12b_north": RegionConnection("2a_12b_west", "2a_12b_north", [[ItemName.dream_blocks, ], ]),
    "2a_12b_north---2a_12b_west": RegionConnection("2a_12b_north", "2a_12b_west", [[ItemName.dream_blocks, ], ]),
    "2a_12b_north---2a_12b_south": RegionConnection("2a_12b_north", "2a_12b_south", [[ItemName.dream_blocks, ], ]),
    "2a_12b_north---2a_12b_east": RegionConnection("2a_12b_north", "2a_12b_east", [[ItemName.dream_blocks, ], ]),
    "2a_12b_south---2a_12b_north": RegionConnection("2a_12b_south", "2a_12b_north", [[ItemName.dream_blocks, ], ]),
    "2a_12b_east---2a_12b_north": RegionConnection("2a_12b_east", "2a_12b_north", [[ItemName.dream_blocks, ], ]),
    "2a_12b_south-east---2a_12b_north": RegionConnection("2a_12b_south-east", "2a_12b_north", []),


    "2a_12d_north-west---2a_12d_north": RegionConnection("2a_12d_north-west", "2a_12d_north", []),
    "2a_12d_north---2a_12d_north-west": RegionConnection("2a_12d_north", "2a_12d_north-west", []),

    "2a_12_west---2a_12_east": RegionConnection("2a_12_west", "2a_12_east", []),
    "2a_12_east---2a_12_west": RegionConnection("2a_12_east", "2a_12_west", []),

    "2a_13_west---2a_13_phone": RegionConnection("2a_13_west", "2a_13_phone", []),
    "2a_13_phone---2a_13_west": RegionConnection("2a_13_phone", "2a_13_west", []),

    "2a_end_0_main---2a_end_0_east": RegionConnection("2a_end_0_main", "2a_end_0_east", []),
    "2a_end_0_top---2a_end_0_east": RegionConnection("2a_end_0_top", "2a_end_0_east", []),
    "2a_end_0_top---2a_end_0_main": RegionConnection("2a_end_0_top", "2a_end_0_main", []),
    "2a_end_0_east---2a_end_0_main": RegionConnection("2a_end_0_east", "2a_end_0_main", []),
    "2a_end_0_east---2a_end_0_top": RegionConnection("2a_end_0_east", "2a_end_0_top", []),

    "2a_end_s0_bottom---2a_end_s0_top": RegionConnection("2a_end_s0_bottom", "2a_end_s0_top", []),
    "2a_end_s0_top---2a_end_s0_bottom": RegionConnection("2a_end_s0_top", "2a_end_s0_bottom", []),


    "2a_end_1_west---2a_end_1_east": RegionConnection("2a_end_1_west", "2a_end_1_east", []),
    "2a_end_1_west---2a_end_1_north-east": RegionConnection("2a_end_1_west", "2a_end_1_north-east", []),
    "2a_end_1_north-east---2a_end_1_west": RegionConnection("2a_end_1_north-east", "2a_end_1_west", []),
    "2a_end_1_east---2a_end_1_west": RegionConnection("2a_end_1_east", "2a_end_1_west", []),

    "2a_end_2_north-west---2a_end_2_north-east": RegionConnection("2a_end_2_north-west", "2a_end_2_north-east", []),
    "2a_end_2_west---2a_end_2_east": RegionConnection("2a_end_2_west", "2a_end_2_east", []),
    "2a_end_2_north-east---2a_end_2_north-west": RegionConnection("2a_end_2_north-east", "2a_end_2_north-west", []),
    "2a_end_2_east---2a_end_2_west": RegionConnection("2a_end_2_east", "2a_end_2_west", []),

    "2a_end_3_north-west---2a_end_3_west": RegionConnection("2a_end_3_north-west", "2a_end_3_west", []),
    "2a_end_3_west---2a_end_3_east": RegionConnection("2a_end_3_west", "2a_end_3_east", []),
    "2a_end_3_west---2a_end_3_north-west": RegionConnection("2a_end_3_west", "2a_end_3_north-west", []),
    "2a_end_3_east---2a_end_3_west": RegionConnection("2a_end_3_east", "2a_end_3_west", []),

    "2a_end_4_west---2a_end_4_east": RegionConnection("2a_end_4_west", "2a_end_4_east", []),
    "2a_end_4_east---2a_end_4_west": RegionConnection("2a_end_4_east", "2a_end_4_west", []),

    "2a_end_3b_west---2a_end_3b_north": RegionConnection("2a_end_3b_west", "2a_end_3b_north", [[ItemName.springs, ], ]),
    "2a_end_3b_west---2a_end_3b_east": RegionConnection("2a_end_3b_west", "2a_end_3b_east", []),
    "2a_end_3b_north---2a_end_3b_west": RegionConnection("2a_end_3b_north", "2a_end_3b_west", []),
    "2a_end_3b_east---2a_end_3b_west": RegionConnection("2a_end_3b_east", "2a_end_3b_west", []),

    "2a_end_3cb_bottom---2a_end_3cb_top": RegionConnection("2a_end_3cb_bottom", "2a_end_3cb_top", []),
    "2a_end_3cb_top---2a_end_3cb_bottom": RegionConnection("2a_end_3cb_top", "2a_end_3cb_bottom", []),


    "2a_end_5_west---2a_end_5_east": RegionConnection("2a_end_5_west", "2a_end_5_east", []),
    "2a_end_5_east---2a_end_5_west": RegionConnection("2a_end_5_east", "2a_end_5_west", []),

    "2a_end_6_west---2a_end_6_main": RegionConnection("2a_end_6_west", "2a_end_6_main", []),
    "2a_end_6_main---2a_end_6_west": RegionConnection("2a_end_6_main", "2a_end_6_west", []),

    "2b_start_west---2b_start_east": RegionConnection("2b_start_west", "2b_start_east", []),
    "2b_start_east---2b_start_west": RegionConnection("2b_start_east", "2b_start_west", []),

    "2b_00_west---2b_00_east": RegionConnection("2b_00_west", "2b_00_east", [[ItemName.dream_blocks, ], ]),
    "2b_00_east---2b_00_west": RegionConnection("2b_00_east", "2b_00_west", [[ItemName.dream_blocks, ], ]),

    "2b_01_west---2b_01_east": RegionConnection("2b_01_west", "2b_01_east", [[ItemName.dream_blocks, ], ]),
    "2b_01_east---2b_01_west": RegionConnection("2b_01_east", "2b_01_west", [[ItemName.dream_blocks, ], ]),

    "2b_01b_west---2b_01b_east": RegionConnection("2b_01b_west", "2b_01b_east", [[ItemName.dream_blocks, ], ]),
    "2b_01b_east---2b_01b_west": RegionConnection("2b_01b_east", "2b_01b_west", [[ItemName.cannot_access, ], ]),

    "2b_02b_west---2b_02b_east": RegionConnection("2b_02b_west", "2b_02b_east", [[ItemName.dream_blocks, ], ]),
    "2b_02b_east---2b_02b_west": RegionConnection("2b_02b_east", "2b_02b_west", [[ItemName.cannot_access, ], ]),

    "2b_02_west---2b_02_east": RegionConnection("2b_02_west", "2b_02_east", [[ItemName.dream_blocks, ItemName.dash_refills, ], ]),
    "2b_02_east---2b_02_west": RegionConnection("2b_02_east", "2b_02_west", [[ItemName.cannot_access, ], ]),

    "2b_03_west---2b_03_east": RegionConnection("2b_03_west", "2b_03_east", [[ItemName.dream_blocks, ItemName.coins, ], ]),
    "2b_03_east---2b_03_west": RegionConnection("2b_03_east", "2b_03_west", [[ItemName.cannot_access, ], ]),

    "2b_04_bottom---2b_04_top": RegionConnection("2b_04_bottom", "2b_04_top", [[ItemName.dream_blocks, ItemName.dash_refills, ], ]),
    "2b_04_top---2b_04_bottom": RegionConnection("2b_04_top", "2b_04_bottom", [[ItemName.cannot_access, ], ]),

    "2b_05_bottom---2b_05_top": RegionConnection("2b_05_bottom", "2b_05_top", [[ItemName.dream_blocks, ItemName.dash_refills, ], ]),
    "2b_05_top---2b_05_bottom": RegionConnection("2b_05_top", "2b_05_bottom", [[ItemName.cannot_access, ], ]),

    "2b_06_west---2b_06_east": RegionConnection("2b_06_west", "2b_06_east", [[ItemName.dream_blocks, ItemName.coins, ], ]),
    "2b_06_east---2b_06_west": RegionConnection("2b_06_east", "2b_06_west", [[ItemName.cannot_access, ], ]),

    "2b_07_bottom---2b_07_top": RegionConnection("2b_07_bottom", "2b_07_top", [[ItemName.dream_blocks, ItemName.coins, ], ]),
    "2b_07_top---2b_07_bottom": RegionConnection("2b_07_top", "2b_07_bottom", [[ItemName.cannot_access, ], ]),

    "2b_08b_west---2b_08b_east": RegionConnection("2b_08b_west", "2b_08b_east", [[ItemName.dream_blocks, ItemName.springs, ], ]),
    "2b_08b_east---2b_08b_west": RegionConnection("2b_08b_east", "2b_08b_west", [[ItemName.cannot_access, ], ]),

    "2b_08_west---2b_08_east": RegionConnection("2b_08_west", "2b_08_east", [[ItemName.dream_blocks, ItemName.dash_refills, ], ]),

    "2b_09_west---2b_09_east": RegionConnection("2b_09_west", "2b_09_east", [[ItemName.dream_blocks, ], ]),

    "2b_10_west---2b_10_east": RegionConnection("2b_10_west", "2b_10_east", [[ItemName.dream_blocks, ItemName.coins, ], ]),

    "2b_11_bottom---2b_11_top": RegionConnection("2b_11_bottom", "2b_11_top", [[ItemName.springs, ItemName.dream_blocks, ItemName.dash_refills, ItemName.coins, ], ]),

    "2b_end_west---2b_end_goal": RegionConnection("2b_end_west", "2b_end_goal", [[ItemName.blue_cassette_blocks, ItemName.dash_refills, ], ]),

    "2c_00_west---2c_00_east": RegionConnection("2c_00_west", "2c_00_east", [[ItemName.dream_blocks, ], ]),
    "2c_00_east---2c_00_west": RegionConnection("2c_00_east", "2c_00_west", [[ItemName.dream_blocks, ], ]),

    "2c_01_west---2c_01_east": RegionConnection("2c_01_west", "2c_01_east", [[ItemName.dream_blocks, ItemName.coins, ], ]),

    "2c_02_west---2c_02_goal": RegionConnection("2c_02_west", "2c_02_goal", [[ItemName.coins, ItemName.dream_blocks, ItemName.dash_refills, ], ]),

    "3a_s0_main---3a_s0_east": RegionConnection("3a_s0_main", "3a_s0_east", []),
    "3a_s0_east---3a_s0_main": RegionConnection("3a_s0_east", "3a_s0_main", []),

    "3a_s1_west---3a_s1_east": RegionConnection("3a_s1_west", "3a_s1_east", []),
    "3a_s1_west---3a_s1_north-east": RegionConnection("3a_s1_west", "3a_s1_north-east", []),
    "3a_s1_east---3a_s1_west": RegionConnection("3a_s1_east", "3a_s1_west", []),
    "3a_s1_north-east---3a_s1_west": RegionConnection("3a_s1_north-east", "3a_s1_west", []),

    "3a_s2_west---3a_s2_east": RegionConnection("3a_s2_west", "3a_s2_east", []),
    "3a_s2_north-west---3a_s2_east": RegionConnection("3a_s2_north-west", "3a_s2_east", []),
    "3a_s2_east---3a_s2_west": RegionConnection("3a_s2_east", "3a_s2_west", []),
    "3a_s2_east---3a_s2_north-west": RegionConnection("3a_s2_east", "3a_s2_north-west", []),

    "3a_s3_west---3a_s3_east": RegionConnection("3a_s3_west", "3a_s3_east", [["Celestial Resort A - Front Door Key", ], ]),
    "3a_s3_east---3a_s3_west": RegionConnection("3a_s3_east", "3a_s3_west", []),

    "3a_0x-a_west---3a_0x-a_east": RegionConnection("3a_0x-a_west", "3a_0x-a_east", []),
    "3a_0x-a_east---3a_0x-a_west": RegionConnection("3a_0x-a_east", "3a_0x-a_west", []),

    "3a_00-a_west---3a_00-a_east": RegionConnection("3a_00-a_west", "3a_00-a_east", []),
    "3a_00-a_east---3a_00-a_west": RegionConnection("3a_00-a_east", "3a_00-a_west", []),

    "3a_02-a_west---3a_02-a_east": RegionConnection("3a_02-a_west", "3a_02-a_east", [[ItemName.sinking_platforms, ], [ItemName.dash_refills, ], ]),
    "3a_02-a_top---3a_02-a_west": RegionConnection("3a_02-a_top", "3a_02-a_west", [[ItemName.dash_refills, ], ]),
    "3a_02-a_top---3a_02-a_main": RegionConnection("3a_02-a_top", "3a_02-a_main", [[ItemName.dash_refills, ], ]),
    "3a_02-a_main---3a_02-a_top": RegionConnection("3a_02-a_main", "3a_02-a_top", [[ItemName.dash_refills, ], ]),
    "3a_02-a_main---3a_02-a_east": RegionConnection("3a_02-a_main", "3a_02-a_east", [["Celestial Resort A - Hallway Key 1", ], ]),
    "3a_02-a_east---3a_02-a_main": RegionConnection("3a_02-a_east", "3a_02-a_main", []),

    "3a_02-b_west---3a_02-b_east": RegionConnection("3a_02-b_west", "3a_02-b_east", []),
    "3a_02-b_east---3a_02-b_west": RegionConnection("3a_02-b_east", "3a_02-b_west", []),

    "3a_01-b_west---3a_01-b_east": RegionConnection("3a_01-b_west", "3a_01-b_east", []),
    "3a_01-b_north-west---3a_01-b_west": RegionConnection("3a_01-b_north-west", "3a_01-b_west", []),
    "3a_01-b_east---3a_01-b_west": RegionConnection("3a_01-b_east", "3a_01-b_west", []),
    "3a_01-b_east---3a_01-b_north-west": RegionConnection("3a_01-b_east", "3a_01-b_north-west", [[ItemName.springs, ], ]),

    "3a_00-b_south-west---3a_00-b_south-east": RegionConnection("3a_00-b_south-west", "3a_00-b_south-east", []),
    "3a_00-b_south-east---3a_00-b_south-west": RegionConnection("3a_00-b_south-east", "3a_00-b_south-west", []),
    "3a_00-b_west---3a_00-b_north-west": RegionConnection("3a_00-b_west", "3a_00-b_north-west", []),
    "3a_00-b_north-west---3a_00-b_west": RegionConnection("3a_00-b_north-west", "3a_00-b_west", []),
    "3a_00-b_east---3a_00-b_north": RegionConnection("3a_00-b_east", "3a_00-b_north", []),
    "3a_00-b_north---3a_00-b_east": RegionConnection("3a_00-b_north", "3a_00-b_east", []),

    "3a_00-c_south-west---3a_00-c_south-east": RegionConnection("3a_00-c_south-west", "3a_00-c_south-east", [[ItemName.dash_refills, ], ]),
    "3a_00-c_south-east---3a_00-c_south-west": RegionConnection("3a_00-c_south-east", "3a_00-c_south-west", [[ItemName.dash_refills, ], ]),
    "3a_00-c_south-east---3a_00-c_north-east": RegionConnection("3a_00-c_south-east", "3a_00-c_north-east", []),
    "3a_00-c_north-east---3a_00-c_south-east": RegionConnection("3a_00-c_north-east", "3a_00-c_south-east", []),

    "3a_0x-b_west---3a_0x-b_south-east": RegionConnection("3a_0x-b_west", "3a_0x-b_south-east", []),
    "3a_0x-b_north-east---3a_0x-b_west": RegionConnection("3a_0x-b_north-east", "3a_0x-b_west", [[ItemName.dash_refills, ], ]),

    "3a_03-a_west---3a_03-a_east": RegionConnection("3a_03-a_west", "3a_03-a_east", [[ItemName.sinking_platforms, ], ]),
    "3a_03-a_top---3a_03-a_east": RegionConnection("3a_03-a_top", "3a_03-a_east", []),
    "3a_03-a_east---3a_03-a_top": RegionConnection("3a_03-a_east", "3a_03-a_top", []),


    "3a_05-a_west---3a_05-a_east": RegionConnection("3a_05-a_west", "3a_05-a_east", [[ItemName.dash_refills, ItemName.moving_platforms, ], ]),
    "3a_05-a_east---3a_05-a_west": RegionConnection("3a_05-a_east", "3a_05-a_west", [[ItemName.dash_refills, ItemName.moving_platforms, ], ]),

    "3a_06-a_west---3a_06-a_east": RegionConnection("3a_06-a_west", "3a_06-a_east", []),

    "3a_07-a_west---3a_07-a_east": RegionConnection("3a_07-a_west", "3a_07-a_east", [["Celestial Resort A - Hallway Key 2", ItemName.dash_refills, ], ]),
    "3a_07-a_west---3a_07-a_top": RegionConnection("3a_07-a_west", "3a_07-a_top", []),
    "3a_07-a_top---3a_07-a_west": RegionConnection("3a_07-a_top", "3a_07-a_west", []),
    "3a_07-a_east---3a_07-a_west": RegionConnection("3a_07-a_east", "3a_07-a_west", [["Celestial Resort A - Hallway Key 2", ItemName.dash_refills, ], ]),

    "3a_07-b_bottom---3a_07-b_west": RegionConnection("3a_07-b_bottom", "3a_07-b_west", []),
    "3a_07-b_west---3a_07-b_bottom": RegionConnection("3a_07-b_west", "3a_07-b_bottom", []),
    "3a_07-b_east---3a_07-b_bottom": RegionConnection("3a_07-b_east", "3a_07-b_bottom", []),

    "3a_06-b_west---3a_06-b_east": RegionConnection("3a_06-b_west", "3a_06-b_east", []),
    "3a_06-b_east---3a_06-b_west": RegionConnection("3a_06-b_east", "3a_06-b_west", []),

    "3a_06-c_south-west---3a_06-c_north-west": RegionConnection("3a_06-c_south-west", "3a_06-c_north-west", []),
    "3a_06-c_south-west---3a_06-c_south-east": RegionConnection("3a_06-c_south-west", "3a_06-c_south-east", []),
    "3a_06-c_north-west---3a_06-c_south-west": RegionConnection("3a_06-c_north-west", "3a_06-c_south-west", []),
    "3a_06-c_south-east---3a_06-c_south-west": RegionConnection("3a_06-c_south-east", "3a_06-c_south-west", []),
    "3a_06-c_south-east---3a_06-c_east": RegionConnection("3a_06-c_south-east", "3a_06-c_east", []),
    "3a_06-c_east---3a_06-c_south-east": RegionConnection("3a_06-c_east", "3a_06-c_south-east", []),


    "3a_08-c_west---3a_08-c_east": RegionConnection("3a_08-c_west", "3a_08-c_east", [[ItemName.coins, ItemName.moving_platforms, ItemName.springs, ], ]),

    "3a_08-b_east---3a_08-b_west": RegionConnection("3a_08-b_east", "3a_08-b_west", [[ItemName.sinking_platforms, ItemName.coins, ], ]),

    "3a_08-a_west---3a_08-a_east": RegionConnection("3a_08-a_west", "3a_08-a_east", []),
    "3a_08-a_west---3a_08-a_bottom": RegionConnection("3a_08-a_west", "3a_08-a_bottom", [[ItemName.brown_clutter, ], [ItemName.green_clutter, ], [ItemName.pink_clutter, ], ]),
    "3a_08-a_east---3a_08-a_west": RegionConnection("3a_08-a_east", "3a_08-a_west", []),

    "3a_09-b_west---3a_09-b_center": RegionConnection("3a_09-b_west", "3a_09-b_center", []),
    "3a_09-b_north-west---3a_09-b_center": RegionConnection("3a_09-b_north-west", "3a_09-b_center", [["Celestial Resort A - Huge Mess Key", ], ]),
    "3a_09-b_center---3a_09-b_west": RegionConnection("3a_09-b_center", "3a_09-b_west", []),
    "3a_09-b_center---3a_09-b_north-west": RegionConnection("3a_09-b_center", "3a_09-b_north-west", [["Celestial Resort A - Huge Mess Key", ], ]),
    "3a_09-b_center---3a_09-b_south-west": RegionConnection("3a_09-b_center", "3a_09-b_south-west", [[ItemName.brown_clutter, ], [ItemName.green_clutter, ], [ItemName.pink_clutter, ], ]),
    "3a_09-b_center---3a_09-b_south": RegionConnection("3a_09-b_center", "3a_09-b_south", []),
    "3a_09-b_center---3a_09-b_south-east": RegionConnection("3a_09-b_center", "3a_09-b_south-east", []),
    "3a_09-b_center---3a_09-b_east": RegionConnection("3a_09-b_center", "3a_09-b_east", []),
    "3a_09-b_center---3a_09-b_north-east-right": RegionConnection("3a_09-b_center", "3a_09-b_north-east-right", []),
    "3a_09-b_center---3a_09-b_north-east-top": RegionConnection("3a_09-b_center", "3a_09-b_north-east-top", []),
    "3a_09-b_center---3a_09-b_north": RegionConnection("3a_09-b_center", "3a_09-b_north", []),
    "3a_09-b_south-west---3a_09-b_center": RegionConnection("3a_09-b_south-west", "3a_09-b_center", [[ItemName.brown_clutter, ], [ItemName.green_clutter, ], [ItemName.pink_clutter, ], ]),
    "3a_09-b_south---3a_09-b_center": RegionConnection("3a_09-b_south", "3a_09-b_center", []),
    "3a_09-b_south-east---3a_09-b_center": RegionConnection("3a_09-b_south-east", "3a_09-b_center", []),
    "3a_09-b_east---3a_09-b_center": RegionConnection("3a_09-b_east", "3a_09-b_center", []),
    "3a_09-b_north-east-right---3a_09-b_center": RegionConnection("3a_09-b_north-east-right", "3a_09-b_center", []),
    "3a_09-b_north-east-top---3a_09-b_center": RegionConnection("3a_09-b_north-east-top", "3a_09-b_center", []),
    "3a_09-b_north---3a_09-b_center": RegionConnection("3a_09-b_north", "3a_09-b_center", []),

    "3a_10-x_west---3a_10-x_south-east": RegionConnection("3a_10-x_west", "3a_10-x_south-east", []),
    "3a_10-x_south-east---3a_10-x_west": RegionConnection("3a_10-x_south-east", "3a_10-x_west", [[ItemName.brown_clutter, ], ]),
    "3a_10-x_north-east-top---3a_10-x_north-east-right": RegionConnection("3a_10-x_north-east-top", "3a_10-x_north-east-right", []),
    "3a_10-x_north-east-right---3a_10-x_north-east-top": RegionConnection("3a_10-x_north-east-right", "3a_10-x_north-east-top", []),

    "3a_11-x_west---3a_11-x_south": RegionConnection("3a_11-x_west", "3a_11-x_south", [[ItemName.coins, ], ]),

    "3a_11-y_west---3a_11-y_east": RegionConnection("3a_11-y_west", "3a_11-y_east", []),
    "3a_11-y_east---3a_11-y_east": RegionConnection("3a_11-y_east", "3a_11-y_east", []),
    "3a_11-y_east---3a_11-y_south": RegionConnection("3a_11-y_east", "3a_11-y_south", []),
    "3a_11-y_south---3a_11-y_east": RegionConnection("3a_11-y_south", "3a_11-y_east", []),


    "3a_11-z_west---3a_11-z_east": RegionConnection("3a_11-z_west", "3a_11-z_east", [[ItemName.dash_refills, ], ]),
    "3a_11-z_east---3a_11-z_west": RegionConnection("3a_11-z_east", "3a_11-z_west", [[ItemName.dash_refills, ], ]),

    "3a_10-z_bottom---3a_10-z_top": RegionConnection("3a_10-z_bottom", "3a_10-z_top", [[ItemName.sinking_platforms, ], ]),
    "3a_10-z_top---3a_10-z_bottom": RegionConnection("3a_10-z_top", "3a_10-z_bottom", []),

    "3a_10-y_bottom---3a_10-y_top": RegionConnection("3a_10-y_bottom", "3a_10-y_top", []),
    "3a_10-y_top---3a_10-y_bottom": RegionConnection("3a_10-y_top", "3a_10-y_bottom", []),

    "3a_10-c_south-east---3a_10-c_north-east": RegionConnection("3a_10-c_south-east", "3a_10-c_north-east", []),
    "3a_10-c_north-east---3a_10-c_south-east": RegionConnection("3a_10-c_north-east", "3a_10-c_south-east", []),
    "3a_10-c_north-west---3a_10-c_south-west": RegionConnection("3a_10-c_north-west", "3a_10-c_south-west", []),
    "3a_10-c_south-west---3a_10-c_north-west": RegionConnection("3a_10-c_south-west", "3a_10-c_north-west", []),

    "3a_11-c_west---3a_11-c_east": RegionConnection("3a_11-c_west", "3a_11-c_east", []),
    "3a_11-c_east---3a_11-c_west": RegionConnection("3a_11-c_east", "3a_11-c_west", []),
    "3a_11-c_south-east---3a_11-c_south-west": RegionConnection("3a_11-c_south-east", "3a_11-c_south-west", []),
    "3a_11-c_south-west---3a_11-c_south-east": RegionConnection("3a_11-c_south-west", "3a_11-c_south-east", []),

    "3a_12-c_west---3a_12-c_top": RegionConnection("3a_12-c_west", "3a_12-c_top", []),
    "3a_12-c_top---3a_12-c_west": RegionConnection("3a_12-c_top", "3a_12-c_west", []),

    "3a_12-d_bottom---3a_12-d_top": RegionConnection("3a_12-d_bottom", "3a_12-d_top", []),

    "3a_11-d_west---3a_11-d_east": RegionConnection("3a_11-d_west", "3a_11-d_east", [[ItemName.cannot_access, ], ]),
    "3a_11-d_east---3a_11-d_west": RegionConnection("3a_11-d_east", "3a_11-d_west", [[ItemName.dash_refills, ], ]),

    "3a_10-d_west---3a_10-d_main": RegionConnection("3a_10-d_west", "3a_10-d_main", [[ItemName.green_clutter, ], ]),
    "3a_10-d_main---3a_10-d_west": RegionConnection("3a_10-d_main", "3a_10-d_west", [[ItemName.dash_refills, ], ]),
    "3a_10-d_east---3a_10-d_main": RegionConnection("3a_10-d_east", "3a_10-d_main", []),

    "3a_11-b_west---3a_11-b_east": RegionConnection("3a_11-b_west", "3a_11-b_east", []),
    "3a_11-b_north-west---3a_11-b_west": RegionConnection("3a_11-b_north-west", "3a_11-b_west", []),
    "3a_11-b_east---3a_11-b_west": RegionConnection("3a_11-b_east", "3a_11-b_west", []),
    "3a_11-b_east---3a_11-b_north-east": RegionConnection("3a_11-b_east", "3a_11-b_north-east", [[ItemName.pink_clutter, ], ]),
    "3a_11-b_north-east---3a_11-b_east": RegionConnection("3a_11-b_north-east", "3a_11-b_east", [[ItemName.pink_clutter, ], ]),

    "3a_12-b_west---3a_12-b_east": RegionConnection("3a_12-b_west", "3a_12-b_east", []),
    "3a_12-b_east---3a_12-b_west": RegionConnection("3a_12-b_east", "3a_12-b_west", []),

    "3a_13-b_top---3a_13-b_bottom": RegionConnection("3a_13-b_top", "3a_13-b_bottom", []),
    "3a_13-b_bottom---3a_13-b_top": RegionConnection("3a_13-b_bottom", "3a_13-b_top", []),

    "3a_13-a_west---3a_13-a_east": RegionConnection("3a_13-a_west", "3a_13-a_east", []),
    "3a_13-a_west---3a_13-a_south-west": RegionConnection("3a_13-a_west", "3a_13-a_south-west", [[ItemName.pink_clutter, ], ]),
    "3a_13-a_south-west---3a_13-a_west": RegionConnection("3a_13-a_south-west", "3a_13-a_west", [[ItemName.pink_clutter, ], ]),

    "3a_13-x_west---3a_13-x_east": RegionConnection("3a_13-x_west", "3a_13-x_east", []),
    "3a_13-x_east---3a_13-x_west": RegionConnection("3a_13-x_east", "3a_13-x_west", []),

    "3a_12-x_west---3a_12-x_east": RegionConnection("3a_12-x_west", "3a_12-x_east", []),
    "3a_12-x_north-east---3a_12-x_east": RegionConnection("3a_12-x_north-east", "3a_12-x_east", []),
    "3a_12-x_east---3a_12-x_west": RegionConnection("3a_12-x_east", "3a_12-x_west", []),

    "3a_11-a_west---3a_11-a_south": RegionConnection("3a_11-a_west", "3a_11-a_south", []),
    "3a_11-a_south---3a_11-a_west": RegionConnection("3a_11-a_south", "3a_11-a_west", []),
    "3a_11-a_south-east-bottom---3a_11-a_south-east-right": RegionConnection("3a_11-a_south-east-bottom", "3a_11-a_south-east-right", [[ItemName.pink_clutter, ], ]),
    "3a_11-a_south-east-right---3a_11-a_south-east-bottom": RegionConnection("3a_11-a_south-east-right", "3a_11-a_south-east-bottom", [[ItemName.pink_clutter, ], ]),

    "3a_08-x_west---3a_08-x_east": RegionConnection("3a_08-x_west", "3a_08-x_east", []),
    "3a_08-x_east---3a_08-x_west": RegionConnection("3a_08-x_east", "3a_08-x_west", []),

    "3a_09-d_bottom---3a_09-d_top": RegionConnection("3a_09-d_bottom", "3a_09-d_top", []),

    "3a_08-d_east---3a_08-d_west": RegionConnection("3a_08-d_east", "3a_08-d_west", [[ItemName.dash_refills, ItemName.coins, ], ]),

    "3a_06-d_east---3a_06-d_west": RegionConnection("3a_06-d_east", "3a_06-d_west", [[ItemName.dash_refills, ], ]),

    "3a_04-d_west---3a_04-d_west": RegionConnection("3a_04-d_west", "3a_04-d_west", []),
    "3a_04-d_south-west---3a_04-d_west": RegionConnection("3a_04-d_south-west", "3a_04-d_west", []),
    "3a_04-d_south---3a_04-d_south-west": RegionConnection("3a_04-d_south", "3a_04-d_south-west", [[ItemName.cannot_access, ], ]),
    "3a_04-d_east---3a_04-d_south": RegionConnection("3a_04-d_east", "3a_04-d_south", [[ItemName.dash_refills, ], ]),

    "3a_04-c_west---3a_04-c_north-west": RegionConnection("3a_04-c_west", "3a_04-c_north-west", [["Celestial Resort A - Presidential Suite Key", ], ]),
    "3a_04-c_west---3a_04-c_east": RegionConnection("3a_04-c_west", "3a_04-c_east", []),
    "3a_04-c_north-west---3a_04-c_west": RegionConnection("3a_04-c_north-west", "3a_04-c_west", [["Celestial Resort A - Presidential Suite Key", ], ]),
    "3a_04-c_east---3a_04-c_west": RegionConnection("3a_04-c_east", "3a_04-c_west", []),

    "3a_02-c_west---3a_02-c_east": RegionConnection("3a_02-c_west", "3a_02-c_east", []),
    "3a_02-c_east---3a_02-c_west": RegionConnection("3a_02-c_east", "3a_02-c_west", [[ItemName.sinking_platforms, ], ]),
    "3a_02-c_east---3a_02-c_south-east": RegionConnection("3a_02-c_east", "3a_02-c_south-east", []),
    "3a_02-c_south-east---3a_02-c_east": RegionConnection("3a_02-c_south-east", "3a_02-c_east", []),

    "3a_03-b_west---3a_03-b_east": RegionConnection("3a_03-b_west", "3a_03-b_east", []),
    "3a_03-b_east---3a_03-b_west": RegionConnection("3a_03-b_east", "3a_03-b_west", []),
    "3a_03-b_east---3a_03-b_north": RegionConnection("3a_03-b_east", "3a_03-b_north", []),
    "3a_03-b_north---3a_03-b_east": RegionConnection("3a_03-b_north", "3a_03-b_east", []),


    "3a_02-d_west---3a_02-d_east": RegionConnection("3a_02-d_west", "3a_02-d_east", [[ItemName.cannot_access, ], ]),
    "3a_02-d_east---3a_02-d_west": RegionConnection("3a_02-d_east", "3a_02-d_west", [[ItemName.dash_refills, ], ]),

    "3a_00-d_west---3a_00-d_east": RegionConnection("3a_00-d_west", "3a_00-d_east", []),
    "3a_00-d_east---3a_00-d_west": RegionConnection("3a_00-d_east", "3a_00-d_west", []),

    "3a_roof00_west---3a_roof00_east": RegionConnection("3a_roof00_west", "3a_roof00_east", []),
    "3a_roof00_east---3a_roof00_west": RegionConnection("3a_roof00_east", "3a_roof00_west", []),

    "3a_roof01_west---3a_roof01_east": RegionConnection("3a_roof01_west", "3a_roof01_east", [[ItemName.springs, ], ]),

    "3a_roof02_west---3a_roof02_east": RegionConnection("3a_roof02_west", "3a_roof02_east", []),
    "3a_roof02_east---3a_roof02_west": RegionConnection("3a_roof02_east", "3a_roof02_west", []),

    "3a_roof03_west---3a_roof03_east": RegionConnection("3a_roof03_west", "3a_roof03_east", [[ItemName.springs, ItemName.coins, ItemName.dash_refills, ], ]),

    "3a_roof04_west---3a_roof04_east": RegionConnection("3a_roof04_west", "3a_roof04_east", []),
    "3a_roof04_east---3a_roof04_west": RegionConnection("3a_roof04_east", "3a_roof04_west", []),

    "3a_roof05_west---3a_roof05_east": RegionConnection("3a_roof05_west", "3a_roof05_east", [[ItemName.springs, ], ]),

    "3a_roof06b_west---3a_roof06b_east": RegionConnection("3a_roof06b_west", "3a_roof06b_east", [[ItemName.dash_refills, ], ]),
    "3a_roof06b_east---3a_roof06b_west": RegionConnection("3a_roof06b_east", "3a_roof06b_west", [[ItemName.dash_refills, ], ]),

    "3a_roof06_west---3a_roof06_east": RegionConnection("3a_roof06_west", "3a_roof06_east", []),
    "3a_roof06_east---3a_roof06_west": RegionConnection("3a_roof06_east", "3a_roof06_west", []),

    "3a_roof07_west---3a_roof07_main": RegionConnection("3a_roof07_west", "3a_roof07_main", []),
    "3a_roof07_main---3a_roof07_west": RegionConnection("3a_roof07_main", "3a_roof07_west", []),

    "3b_00_west---3b_00_east": RegionConnection("3b_00_west", "3b_00_east", []),
    "3b_00_east---3b_00_west": RegionConnection("3b_00_east", "3b_00_west", []),


    "3b_01_west---3b_01_east": RegionConnection("3b_01_west", "3b_01_east", [[ItemName.dash_refills, ], ]),
    "3b_01_east---3b_01_west": RegionConnection("3b_01_east", "3b_01_west", [[ItemName.dash_refills, ], ]),

    "3b_02_west---3b_02_east": RegionConnection("3b_02_west", "3b_02_east", []),
    "3b_02_east---3b_02_west": RegionConnection("3b_02_east", "3b_02_west", []),

    "3b_03_west---3b_03_east": RegionConnection("3b_03_west", "3b_03_east", [[ItemName.dash_refills, ], ]),
    "3b_03_east---3b_03_west": RegionConnection("3b_03_east", "3b_03_west", [[ItemName.dash_refills, ], ]),

    "3b_04_west---3b_04_east": RegionConnection("3b_04_west", "3b_04_east", [[ItemName.dash_refills, ], ]),
    "3b_04_east---3b_04_west": RegionConnection("3b_04_east", "3b_04_west", [[ItemName.dash_refills, ], ]),

    "3b_05_west---3b_05_east": RegionConnection("3b_05_west", "3b_05_east", [[ItemName.moving_platforms, ItemName.coins, ItemName.springs, ], ]),

    "3b_06_west---3b_06_east": RegionConnection("3b_06_west", "3b_06_east", [[ItemName.sinking_platforms, ], ]),
    "3b_06_east---3b_06_west": RegionConnection("3b_06_east", "3b_06_west", [[ItemName.sinking_platforms, ], ]),

    "3b_07_west---3b_07_east": RegionConnection("3b_07_west", "3b_07_east", []),
    "3b_07_east---3b_07_west": RegionConnection("3b_07_east", "3b_07_west", []),

    "3b_08_bottom---3b_08_top": RegionConnection("3b_08_bottom", "3b_08_top", [[ItemName.dash_refills, ], ]),
    "3b_08_top---3b_08_bottom": RegionConnection("3b_08_top", "3b_08_bottom", []),

    "3b_09_west---3b_09_east": RegionConnection("3b_09_west", "3b_09_east", []),
    "3b_09_east---3b_09_east": RegionConnection("3b_09_east", "3b_09_east", []),

    "3b_10_west---3b_10_east": RegionConnection("3b_10_west", "3b_10_east", [[ItemName.dash_refills, ], ]),

    "3b_11_west---3b_11_east": RegionConnection("3b_11_west", "3b_11_east", [[ItemName.dash_refills, ], ]),
    "3b_11_east---3b_11_west": RegionConnection("3b_11_east", "3b_11_west", [[ItemName.dash_refills, ], ]),

    "3b_13_west---3b_13_east": RegionConnection("3b_13_west", "3b_13_east", [[ItemName.springs, ], ]),
    "3b_13_east---3b_13_west": RegionConnection("3b_13_east", "3b_13_west", [[ItemName.springs, ], ]),

    "3b_14_west---3b_14_east": RegionConnection("3b_14_west", "3b_14_east", [[ItemName.dash_refills, ], ]),
    "3b_14_east---3b_14_west": RegionConnection("3b_14_east", "3b_14_west", [[ItemName.dash_refills, ], ]),

    "3b_15_west---3b_15_east": RegionConnection("3b_15_west", "3b_15_east", []),
    "3b_15_east---3b_15_west": RegionConnection("3b_15_east", "3b_15_west", []),

    "3b_12_west---3b_12_east": RegionConnection("3b_12_west", "3b_12_east", [[ItemName.springs, ], ]),
    "3b_12_east---3b_12_west": RegionConnection("3b_12_east", "3b_12_west", [[ItemName.springs, ], ]),

    "3b_16_west---3b_16_top": RegionConnection("3b_16_west", "3b_16_top", []),
    "3b_16_top---3b_16_west": RegionConnection("3b_16_top", "3b_16_west", []),

    "3b_17_west---3b_17_east": RegionConnection("3b_17_west", "3b_17_east", [[ItemName.dash_refills, ItemName.springs, ], ]),
    "3b_17_east---3b_17_west": RegionConnection("3b_17_east", "3b_17_west", [[ItemName.dash_refills, ItemName.springs, ], ]),

    "3b_18_west---3b_18_east": RegionConnection("3b_18_west", "3b_18_east", []),
    "3b_18_east---3b_18_west": RegionConnection("3b_18_east", "3b_18_west", []),

    "3b_19_west---3b_19_east": RegionConnection("3b_19_west", "3b_19_east", [[ItemName.springs, ItemName.dash_refills, ], ]),
    "3b_19_east---3b_19_west": RegionConnection("3b_19_east", "3b_19_west", [[ItemName.springs, ItemName.dash_refills, ], ]),

    "3b_21_west---3b_21_east": RegionConnection("3b_21_west", "3b_21_east", [[ItemName.dash_refills, ], ]),
    "3b_21_east---3b_21_west": RegionConnection("3b_21_east", "3b_21_west", [[ItemName.dash_refills, ], ]),

    "3b_20_west---3b_20_east": RegionConnection("3b_20_west", "3b_20_east", [[ItemName.dash_refills, ItemName.coins, ], ]),

    "3b_end_west---3b_end_goal": RegionConnection("3b_end_west", "3b_end_goal", [[ItemName.pink_cassette_blocks, ItemName.blue_cassette_blocks, ItemName.dash_refills, ItemName.springs, ItemName.coins, ], ]),

    "3c_00_west---3c_00_east": RegionConnection("3c_00_west", "3c_00_east", [[ItemName.dash_refills, ], ]),
    "3c_00_east---3c_00_west": RegionConnection("3c_00_east", "3c_00_west", [[ItemName.dash_refills, ], ]),

    "3c_01_west---3c_01_east": RegionConnection("3c_01_west", "3c_01_east", [[ItemName.sinking_platforms, ], ]),

    "3c_02_west---3c_02_goal": RegionConnection("3c_02_west", "3c_02_goal", [[ItemName.coins, ItemName.dash_refills, ], ]),

    "4a_a-00_west---4a_a-00_east": RegionConnection("4a_a-00_west", "4a_a-00_east", [[ItemName.blue_clouds, ], ]),
    "4a_a-00_east---4a_a-00_west": RegionConnection("4a_a-00_east", "4a_a-00_west", []),

    "4a_a-01_west---4a_a-01_east": RegionConnection("4a_a-01_west", "4a_a-01_east", [[ItemName.blue_boosters, ], ]),
    "4a_a-01_east---4a_a-01_west": RegionConnection("4a_a-01_east", "4a_a-01_west", [[ItemName.blue_boosters, ], ]),

    "4a_a-01x_west---4a_a-01x_east": RegionConnection("4a_a-01x_west", "4a_a-01x_east", [[ItemName.blue_boosters, ], ]),
    "4a_a-01x_east---4a_a-01x_west": RegionConnection("4a_a-01x_east", "4a_a-01x_west", [[ItemName.blue_boosters, ], ]),

    "4a_a-02_west---4a_a-02_east": RegionConnection("4a_a-02_west", "4a_a-02_east", []),
    "4a_a-02_east---4a_a-02_west": RegionConnection("4a_a-02_east", "4a_a-02_west", []),

    "4a_a-03_west---4a_a-03_east": RegionConnection("4a_a-03_west", "4a_a-03_east", [[ItemName.blue_boosters, ], ]),
    "4a_a-03_east---4a_a-03_west": RegionConnection("4a_a-03_east", "4a_a-03_west", [[ItemName.blue_boosters, ], ]),

    "4a_a-04_west---4a_a-04_east": RegionConnection("4a_a-04_west", "4a_a-04_east", [[ItemName.blue_clouds, ItemName.pink_clouds, ], ]),
    "4a_a-04_east---4a_a-04_west": RegionConnection("4a_a-04_east", "4a_a-04_west", [[ItemName.blue_clouds, ], ]),

    "4a_a-05_west---4a_a-05_east": RegionConnection("4a_a-05_west", "4a_a-05_east", [[ItemName.moving_platforms, ], ]),
    "4a_a-05_east---4a_a-05_west": RegionConnection("4a_a-05_east", "4a_a-05_west", [[ItemName.moving_platforms, ], ]),

    "4a_a-06_west---4a_a-06_east": RegionConnection("4a_a-06_west", "4a_a-06_east", []),
    "4a_a-06_east---4a_a-06_west": RegionConnection("4a_a-06_east", "4a_a-06_west", []),

    "4a_a-07_west---4a_a-07_east": RegionConnection("4a_a-07_west", "4a_a-07_east", [[ItemName.blue_boosters, ItemName.coins, ], ]),

    "4a_a-08_west---4a_a-08_north-west": RegionConnection("4a_a-08_west", "4a_a-08_north-west", [[ItemName.blue_clouds, ItemName.blue_boosters, ], ]),
    "4a_a-08_west---4a_a-08_east": RegionConnection("4a_a-08_west", "4a_a-08_east", [[ItemName.blue_clouds, ], ]),
    "4a_a-08_north-west---4a_a-08_west": RegionConnection("4a_a-08_north-west", "4a_a-08_west", []),
    "4a_a-08_east---4a_a-08_west": RegionConnection("4a_a-08_east", "4a_a-08_west", [[ItemName.blue_clouds, ], ]),

    "4a_a-10_west---4a_a-10_east": RegionConnection("4a_a-10_west", "4a_a-10_east", []),
    "4a_a-10_east---4a_a-10_west": RegionConnection("4a_a-10_east", "4a_a-10_west", []),


    "4a_a-09_bottom---4a_a-09_top": RegionConnection("4a_a-09_bottom", "4a_a-09_top", []),
    "4a_a-09_top---4a_a-09_bottom": RegionConnection("4a_a-09_top", "4a_a-09_bottom", []),

    "4a_b-00_south---4a_b-00_south-east": RegionConnection("4a_b-00_south", "4a_b-00_south-east", []),
    "4a_b-00_south---4a_b-00_west": RegionConnection("4a_b-00_south", "4a_b-00_west", [[ItemName.move_blocks, ], ]),
    "4a_b-00_south---4a_b-00_east": RegionConnection("4a_b-00_south", "4a_b-00_east", [[ItemName.move_blocks, ], ]),
    "4a_b-00_south---4a_b-00_north-east": RegionConnection("4a_b-00_south", "4a_b-00_north-east", [[ItemName.move_blocks, ], ]),
    "4a_b-00_south-east---4a_b-00_south": RegionConnection("4a_b-00_south-east", "4a_b-00_south", []),
    "4a_b-00_east---4a_b-00_south": RegionConnection("4a_b-00_east", "4a_b-00_south", []),
    "4a_b-00_east---4a_b-00_north-west": RegionConnection("4a_b-00_east", "4a_b-00_north-west", []),
    "4a_b-00_west---4a_b-00_south": RegionConnection("4a_b-00_west", "4a_b-00_south", []),
    "4a_b-00_west---4a_b-00_north-west": RegionConnection("4a_b-00_west", "4a_b-00_north-west", []),
    "4a_b-00_north-west---4a_b-00_south": RegionConnection("4a_b-00_north-west", "4a_b-00_south", []),
    "4a_b-00_north-west---4a_b-00_north": RegionConnection("4a_b-00_north-west", "4a_b-00_north", []),
    "4a_b-00_north---4a_b-00_north-west": RegionConnection("4a_b-00_north", "4a_b-00_north-west", []),


    "4a_b-04_north-west---4a_b-04_east": RegionConnection("4a_b-04_north-west", "4a_b-04_east", []),
    "4a_b-04_east---4a_b-04_west": RegionConnection("4a_b-04_east", "4a_b-04_west", [[ItemName.move_blocks, ], ]),

    "4a_b-06_west---4a_b-06_east": RegionConnection("4a_b-06_west", "4a_b-06_east", [[ItemName.cannot_access, ], ]),
    "4a_b-06_east---4a_b-06_west": RegionConnection("4a_b-06_east", "4a_b-06_west", [[ItemName.move_blocks, ItemName.blue_boosters, ], ]),

    "4a_b-07_west---4a_b-07_east": RegionConnection("4a_b-07_west", "4a_b-07_east", [[ItemName.move_blocks, ItemName.blue_boosters, ], ]),

    "4a_b-03_west---4a_b-03_east": RegionConnection("4a_b-03_west", "4a_b-03_east", []),
    "4a_b-03_east---4a_b-03_west": RegionConnection("4a_b-03_east", "4a_b-03_west", []),

    "4a_b-02_north-west---4a_b-02_north-east": RegionConnection("4a_b-02_north-west", "4a_b-02_north-east", []),
    "4a_b-02_north-west---4a_b-02_north": RegionConnection("4a_b-02_north-west", "4a_b-02_north", []),
    "4a_b-02_north-east---4a_b-02_north-west": RegionConnection("4a_b-02_north-east", "4a_b-02_north-west", []),
    "4a_b-02_north---4a_b-02_north-west": RegionConnection("4a_b-02_north", "4a_b-02_north-west", []),

    "4a_b-sec_west---4a_b-sec_east": RegionConnection("4a_b-sec_west", "4a_b-sec_east", []),
    "4a_b-sec_east---4a_b-sec_west": RegionConnection("4a_b-sec_east", "4a_b-sec_west", []),


    "4a_b-05_center---4a_b-05_west": RegionConnection("4a_b-05_center", "4a_b-05_west", [[ItemName.pink_clouds, ItemName.move_blocks, ], ]),
    "4a_b-05_north-east---4a_b-05_east": RegionConnection("4a_b-05_north-east", "4a_b-05_east", []),
    "4a_b-05_east---4a_b-05_north-east": RegionConnection("4a_b-05_east", "4a_b-05_north-east", [[ItemName.move_blocks, ], ]),

    "4a_b-08b_west---4a_b-08b_east": RegionConnection("4a_b-08b_west", "4a_b-08b_east", [[ItemName.move_blocks, ItemName.dash_refills, ], ]),
    "4a_b-08b_east---4a_b-08b_west": RegionConnection("4a_b-08b_east", "4a_b-08b_west", [[ItemName.dash_refills, ], ]),

    "4a_b-08_west---4a_b-08_east": RegionConnection("4a_b-08_west", "4a_b-08_east", [[ItemName.move_blocks, ItemName.blue_clouds, ], ]),

    "4a_c-00_west---4a_c-00_east": RegionConnection("4a_c-00_west", "4a_c-00_east", [[ItemName.blue_boosters, ], ]),
    "4a_c-00_west---4a_c-00_north-west": RegionConnection("4a_c-00_west", "4a_c-00_north-west", []),
    "4a_c-00_east---4a_c-00_west": RegionConnection("4a_c-00_east", "4a_c-00_west", [[ItemName.blue_boosters, ], ]),
    "4a_c-00_north-west---4a_c-00_west": RegionConnection("4a_c-00_north-west", "4a_c-00_west", []),


    "4a_c-02_west---4a_c-02_east": RegionConnection("4a_c-02_west", "4a_c-02_east", [[ItemName.blue_boosters, ], ]),
    "4a_c-02_east---4a_c-02_west": RegionConnection("4a_c-02_east", "4a_c-02_west", [[ItemName.blue_boosters, ], ]),

    "4a_c-04_west---4a_c-04_east": RegionConnection("4a_c-04_west", "4a_c-04_east", [[ItemName.pink_clouds, ], ]),

    "4a_c-05_west---4a_c-05_east": RegionConnection("4a_c-05_west", "4a_c-05_east", [[ItemName.blue_boosters, ItemName.move_blocks, ], ]),
    "4a_c-05_east---4a_c-05_west": RegionConnection("4a_c-05_east", "4a_c-05_west", [[ItemName.cannot_access, ], ]),

    "4a_c-06_bottom---4a_c-06_west": RegionConnection("4a_c-06_bottom", "4a_c-06_west", [[ItemName.blue_boosters, ItemName.blue_clouds, ItemName.move_blocks, ], ]),
    "4a_c-06_west---4a_c-06_bottom": RegionConnection("4a_c-06_west", "4a_c-06_bottom", []),
    "4a_c-06_west---4a_c-06_top": RegionConnection("4a_c-06_west", "4a_c-06_top", [[ItemName.move_blocks, ], ]),


    "4a_c-09_west---4a_c-09_east": RegionConnection("4a_c-09_west", "4a_c-09_east", [[ItemName.coins, ItemName.move_blocks, ], ]),

    "4a_c-07_west---4a_c-07_east": RegionConnection("4a_c-07_west", "4a_c-07_east", []),

    "4a_c-08_bottom---4a_c-08_east": RegionConnection("4a_c-08_bottom", "4a_c-08_east", [[ItemName.springs, ], ]),
    "4a_c-08_east---4a_c-08_bottom": RegionConnection("4a_c-08_east", "4a_c-08_bottom", []),
    "4a_c-08_east---4a_c-08_top": RegionConnection("4a_c-08_east", "4a_c-08_top", [[ItemName.blue_boosters, ], ]),
    "4a_c-08_top---4a_c-08_east": RegionConnection("4a_c-08_top", "4a_c-08_east", []),

    "4a_c-10_bottom---4a_c-10_top": RegionConnection("4a_c-10_bottom", "4a_c-10_top", [[ItemName.blue_boosters, ], ]),
    "4a_c-10_top---4a_c-10_bottom": RegionConnection("4a_c-10_top", "4a_c-10_bottom", [[ItemName.blue_boosters, ], ]),

    "4a_d-00_west---4a_d-00_east": RegionConnection("4a_d-00_west", "4a_d-00_east", []),
    "4a_d-00_west---4a_d-00_south": RegionConnection("4a_d-00_west", "4a_d-00_south", []),
    "4a_d-00_west---4a_d-00_north-west": RegionConnection("4a_d-00_west", "4a_d-00_north-west", []),
    "4a_d-00_south---4a_d-00_west": RegionConnection("4a_d-00_south", "4a_d-00_west", []),
    "4a_d-00_east---4a_d-00_west": RegionConnection("4a_d-00_east", "4a_d-00_west", []),
    "4a_d-00_north-west---4a_d-00_west": RegionConnection("4a_d-00_north-west", "4a_d-00_west", []),


    "4a_d-01_west---4a_d-01_east": RegionConnection("4a_d-01_west", "4a_d-01_east", []),
    "4a_d-01_east---4a_d-01_west": RegionConnection("4a_d-01_east", "4a_d-01_west", []),

    "4a_d-02_west---4a_d-02_east": RegionConnection("4a_d-02_west", "4a_d-02_east", [[ItemName.move_blocks, ItemName.coins, ItemName.pink_clouds, ItemName.blue_boosters, ], ]),

    "4a_d-03_west---4a_d-03_east": RegionConnection("4a_d-03_west", "4a_d-03_east", []),
    "4a_d-03_east---4a_d-03_west": RegionConnection("4a_d-03_east", "4a_d-03_west", []),

    "4a_d-04_west---4a_d-04_east": RegionConnection("4a_d-04_west", "4a_d-04_east", []),
    "4a_d-04_east---4a_d-04_west": RegionConnection("4a_d-04_east", "4a_d-04_west", []),

    "4a_d-05_west---4a_d-05_east": RegionConnection("4a_d-05_west", "4a_d-05_east", []),
    "4a_d-05_east---4a_d-05_west": RegionConnection("4a_d-05_east", "4a_d-05_west", []),

    "4a_d-06_west---4a_d-06_east": RegionConnection("4a_d-06_west", "4a_d-06_east", [[ItemName.blue_boosters, ], ]),
    "4a_d-06_east---4a_d-06_west": RegionConnection("4a_d-06_east", "4a_d-06_west", []),

    "4a_d-07_west---4a_d-07_east": RegionConnection("4a_d-07_west", "4a_d-07_east", [[ItemName.blue_boosters, ], ]),
    "4a_d-07_east---4a_d-07_west": RegionConnection("4a_d-07_east", "4a_d-07_west", [[ItemName.blue_boosters, ], ]),

    "4a_d-08_west---4a_d-08_east": RegionConnection("4a_d-08_west", "4a_d-08_east", [[ItemName.blue_clouds, ItemName.blue_boosters, ], ]),

    "4a_d-09_west---4a_d-09_east": RegionConnection("4a_d-09_west", "4a_d-09_east", [[ItemName.blue_boosters, ], ]),
    "4a_d-09_east---4a_d-09_west": RegionConnection("4a_d-09_east", "4a_d-09_west", [[ItemName.blue_boosters, ], ]),

    "4a_d-10_west---4a_d-10_goal": RegionConnection("4a_d-10_west", "4a_d-10_goal", []),

    "4b_a-00_west---4b_a-00_east": RegionConnection("4b_a-00_west", "4b_a-00_east", [[ItemName.blue_boosters, ], ]),
    "4b_a-00_east---4b_a-00_west": RegionConnection("4b_a-00_east", "4b_a-00_west", [[ItemName.blue_boosters, ], ]),

    "4b_a-01_west---4b_a-01_east": RegionConnection("4b_a-01_west", "4b_a-01_east", [[ItemName.moving_platforms, ], ]),
    "4b_a-01_east---4b_a-01_west": RegionConnection("4b_a-01_east", "4b_a-01_west", [[ItemName.moving_platforms, ], ]),

    "4b_a-02_west---4b_a-02_east": RegionConnection("4b_a-02_west", "4b_a-02_east", [[ItemName.blue_boosters, ], ]),

    "4b_a-03_west---4b_a-03_east": RegionConnection("4b_a-03_west", "4b_a-03_east", [[ItemName.springs, ItemName.move_blocks, ItemName.blue_boosters, ], ]),

    "4b_a-04_west---4b_a-04_east": RegionConnection("4b_a-04_west", "4b_a-04_east", [[ItemName.move_blocks, ItemName.blue_boosters, ], ]),

    "4b_b-00_west---4b_b-00_east": RegionConnection("4b_b-00_west", "4b_b-00_east", [[ItemName.blue_boosters, ], ]),

    "4b_b-01_west---4b_b-01_east": RegionConnection("4b_b-01_west", "4b_b-01_east", [[ItemName.blue_boosters, ], ]),
    "4b_b-01_east---4b_b-01_west": RegionConnection("4b_b-01_east", "4b_b-01_west", [[ItemName.cannot_access, ], ]),

    "4b_b-02_bottom---4b_b-02_top": RegionConnection("4b_b-02_bottom", "4b_b-02_top", [[ItemName.move_blocks, ItemName.springs, ItemName.dash_refills, ], ]),
    "4b_b-02_top---4b_b-02_bottom": RegionConnection("4b_b-02_top", "4b_b-02_bottom", []),

    "4b_b-03_west---4b_b-03_east": RegionConnection("4b_b-03_west", "4b_b-03_east", [[ItemName.coins, ItemName.moving_platforms, ItemName.springs, ItemName.blue_boosters, ], ]),

    "4b_b-04_west---4b_b-04_east": RegionConnection("4b_b-04_west", "4b_b-04_east", [[ItemName.blue_boosters, ], ]),

    "4b_c-00_west---4b_c-00_east": RegionConnection("4b_c-00_west", "4b_c-00_east", [[ItemName.blue_boosters, ], ]),

    "4b_c-01_west---4b_c-01_east": RegionConnection("4b_c-01_west", "4b_c-01_east", [[ItemName.moving_platforms, ], ]),
    "4b_c-01_east---4b_c-01_west": RegionConnection("4b_c-01_east", "4b_c-01_west", [[ItemName.cannot_access, ], ]),

    "4b_c-02_west---4b_c-02_east": RegionConnection("4b_c-02_west", "4b_c-02_east", [[ItemName.move_blocks, ], ]),

    "4b_c-03_bottom---4b_c-03_top": RegionConnection("4b_c-03_bottom", "4b_c-03_top", [[ItemName.move_blocks, ItemName.blue_clouds, ], ]),
    "4b_c-03_top---4b_c-03_bottom": RegionConnection("4b_c-03_top", "4b_c-03_bottom", [[ItemName.blue_clouds, ], ]),

    "4b_c-04_west---4b_c-04_east": RegionConnection("4b_c-04_west", "4b_c-04_east", [[ItemName.blue_boosters, ], ]),
    "4b_c-04_east---4b_c-04_west": RegionConnection("4b_c-04_east", "4b_c-04_west", []),

    "4b_d-00_west---4b_d-00_east": RegionConnection("4b_d-00_west", "4b_d-00_east", [[ItemName.blue_clouds, ], ]),
    "4b_d-00_east---4b_d-00_west": RegionConnection("4b_d-00_east", "4b_d-00_west", [[ItemName.blue_clouds, ], ]),

    "4b_d-01_west---4b_d-01_east": RegionConnection("4b_d-01_west", "4b_d-01_east", [[ItemName.pink_clouds, ItemName.blue_boosters, ], ]),
    "4b_d-01_east---4b_d-01_west": RegionConnection("4b_d-01_east", "4b_d-01_west", [[ItemName.cannot_access, ], ]),

    "4b_d-02_west---4b_d-02_east": RegionConnection("4b_d-02_west", "4b_d-02_east", [[ItemName.dash_refills, ItemName.blue_boosters, ItemName.coins, ], ]),
    "4b_d-02_east---4b_d-02_west": RegionConnection("4b_d-02_east", "4b_d-02_west", [[ItemName.cannot_access, ], ]),

    "4b_d-03_west---4b_d-03_east": RegionConnection("4b_d-03_west", "4b_d-03_east", [[ItemName.blue_boosters, ], ]),

    "4b_end_west---4b_end_goal": RegionConnection("4b_end_west", "4b_end_goal", [[ItemName.pink_cassette_blocks, ItemName.blue_cassette_blocks, ItemName.dash_refills, ItemName.blue_boosters, ], ]),

    "4c_00_west---4c_00_east": RegionConnection("4c_00_west", "4c_00_east", [[ItemName.blue_boosters, ], ]),

    "4c_01_west---4c_01_east": RegionConnection("4c_01_west", "4c_01_east", [[ItemName.move_blocks, ItemName.dash_refills, ], ]),
    "4c_01_east---4c_01_west": RegionConnection("4c_01_east", "4c_01_west", [[ItemName.cannot_access, ], ]),

    "4c_02_west---4c_02_goal": RegionConnection("4c_02_west", "4c_02_goal", [[ItemName.pink_clouds, ItemName.blue_boosters, ItemName.move_blocks, ], ]),

}

all_locations: Dict[str, LevelLocation] = {
    "0a_3_clear": LevelLocation("0a_3_clear", "Prologue - Level Clear", "0a_3_east", LocationType.level_clear, []),

    "1a_2_strawberry": LevelLocation("1a_2_strawberry", "Forsaken City A - Room 2 Strawberry", "1a_2_west", LocationType.strawberry, [[ItemName.springs, ], ]),
    "1a_3_strawberry": LevelLocation("1a_3_strawberry", "Forsaken City A - Room 3 Strawberry", "1a_3_east", LocationType.strawberry, []),
    "1a_3b_strawberry": LevelLocation("1a_3b_strawberry", "Forsaken City A - Room 3b Strawberry", "1a_3b_top", LocationType.strawberry, []),
    "1a_5_strawberry": LevelLocation("1a_5_strawberry", "Forsaken City A - Room 5 Strawberry", "1a_5_north-west", LocationType.strawberry, []),
    "1a_5z_strawberry": LevelLocation("1a_5z_strawberry", "Forsaken City A - Room 5z Strawberry", "1a_5z_east", LocationType.strawberry, [[ItemName.springs, ], ]),
    "1a_5a_strawberry": LevelLocation("1a_5a_strawberry", "Forsaken City A - Room 5a Strawberry", "1a_5a_west", LocationType.strawberry, [[ItemName.traffic_blocks, ], ]),
    "1a_6_strawberry": LevelLocation("1a_6_strawberry", "Forsaken City A - Room 6 Strawberry", "1a_6_east", LocationType.strawberry, [[ItemName.traffic_blocks, ], ]),
    "1a_7zb_strawberry": LevelLocation("1a_7zb_strawberry", "Forsaken City A - Room 7zb Strawberry", "1a_7zb_west", LocationType.strawberry, []),
    "1a_s1_strawberry": LevelLocation("1a_s1_strawberry", "Forsaken City A - Room s1 Strawberry", "1a_s1_east", LocationType.strawberry, []),
    "1a_s1_crystal_heart": LevelLocation("1a_s1_crystal_heart", "Forsaken City A - Crystal Heart", "1a_s1_east", LocationType.crystal_heart, []),
    "1a_7z_strawberry": LevelLocation("1a_7z_strawberry", "Forsaken City A - Room 7z Strawberry", "1a_7z_bottom", LocationType.strawberry, [[ItemName.dash_refills, ], ]),
    "1a_8zb_strawberry": LevelLocation("1a_8zb_strawberry", "Forsaken City A - Room 8zb Strawberry", "1a_8zb_west", LocationType.strawberry, [[ItemName.dash_refills, ], ]),
    "1a_7a_strawberry": LevelLocation("1a_7a_strawberry", "Forsaken City A - Room 7a Strawberry", "1a_7a_east", LocationType.strawberry, [[ItemName.traffic_blocks, ], ]),
    "1a_9z_strawberry": LevelLocation("1a_9z_strawberry", "Forsaken City A - Room 9z Strawberry", "1a_9z_east", LocationType.strawberry, [[ItemName.traffic_blocks, ], ]),
    "1a_8b_strawberry": LevelLocation("1a_8b_strawberry", "Forsaken City A - Room 8b Strawberry", "1a_8b_east", LocationType.strawberry, [[ItemName.traffic_blocks, ], ]),
    "1a_9_strawberry": LevelLocation("1a_9_strawberry", "Forsaken City A - Room 9 Strawberry", "1a_9_west", LocationType.strawberry, [[ItemName.traffic_blocks, ], ]),
    "1a_9b_strawberry": LevelLocation("1a_9b_strawberry", "Forsaken City A - Room 9b Strawberry", "1a_9b_east", LocationType.strawberry, []),
    "1a_9c_strawberry": LevelLocation("1a_9c_strawberry", "Forsaken City A - Room 9c Strawberry", "1a_9c_west", LocationType.strawberry, [[ItemName.traffic_blocks, ], ]),
    "1a_10zb_strawberry": LevelLocation("1a_10zb_strawberry", "Forsaken City A - Room 10zb Strawberry", "1a_10zb_east", LocationType.strawberry, []),
    "1a_11_strawberry": LevelLocation("1a_11_strawberry", "Forsaken City A - Room 11 Strawberry", "1a_11_south", LocationType.strawberry, []),
    "1a_11z_cassette": LevelLocation("1a_11z_cassette", "Forsaken City A - Cassette", "1a_11z_east", LocationType.cassette, [[ItemName.pink_cassette_blocks, ItemName.blue_cassette_blocks, ], ]),
    "1a_12z_strawberry": LevelLocation("1a_12z_strawberry", "Forsaken City A - Room 12z Strawberry", "1a_12z_east", LocationType.strawberry, [[ItemName.dash_refills, ], ]),
    "1a_end_clear": LevelLocation("1a_end_clear", "Forsaken City A - Level Clear", "1a_end_main", LocationType.level_clear, []),
    "1a_end_golden": LevelLocation("1a_end_golden", "Forsaken City A - Golden Strawberry", "1a_end_main", LocationType.golden_strawberry, [[ItemName.springs, ItemName.traffic_blocks, ItemName.dash_refills, ], ]),
    "1a_end_winged_golden": LevelLocation("1a_end_winged_golden", "Forsaken City A - Winged Golden Strawberry", "1a_end_main", LocationType.golden_strawberry, [[ItemName.springs, ItemName.traffic_blocks, ], ]),

    "1b_03_binoculars": LevelLocation("1b_03_binoculars", "Forsaken City B - Room 03 Binoculars", "1b_03_west", LocationType.binoculars, []),
    "1b_09_binoculars": LevelLocation("1b_09_binoculars", "Forsaken City B - Room 09 Binoculars", "1b_09_west", LocationType.binoculars, []),
    "1b_end_clear": LevelLocation("1b_end_clear", "Forsaken City B - Level Clear", "1b_end_goal", LocationType.level_clear, []),
    "1b_end_golden": LevelLocation("1b_end_golden", "Forsaken City B - Golden Strawberry", "1b_end_goal", LocationType.golden_strawberry, [[ItemName.springs, ItemName.traffic_blocks, ItemName.dash_refills, ItemName.pink_cassette_blocks, ItemName.blue_cassette_blocks, ], ]),

    "1c_01_binoculars": LevelLocation("1c_01_binoculars", "Forsaken City C - Room 01 Binoculars", "1c_01_west", LocationType.binoculars, []),
    "1c_02_binoculars": LevelLocation("1c_02_binoculars", "Forsaken City C - Room 02 Binoculars", "1c_02_west", LocationType.binoculars, []),
    "1c_02_clear": LevelLocation("1c_02_clear", "Forsaken City C - Level Clear", "1c_02_goal", LocationType.level_clear, []),
    "1c_02_golden": LevelLocation("1c_02_golden", "Forsaken City C - Golden Strawberry", "1c_02_goal", LocationType.golden_strawberry, [[ItemName.traffic_blocks, ItemName.dash_refills, ItemName.coins, ], ]),

    "2a_s2_crystal_heart": LevelLocation("2a_s2_crystal_heart", "Old Site A - Crystal Heart", "2a_s2_bottom", LocationType.crystal_heart, []),
    "2a_1_strawberry": LevelLocation("2a_1_strawberry", "Old Site A - Room 1 Strawberry", "2a_1_north-west", LocationType.strawberry, [[ItemName.dream_blocks, ], ]),
    "2a_d0_strawberry": LevelLocation("2a_d0_strawberry", "Old Site A - Room d0 Strawberry", "2a_d0_north", LocationType.strawberry, [[ItemName.dream_blocks, ], ]),
    "2a_d3_binoculars": LevelLocation("2a_d3_binoculars", "Old Site A - Room d3 Binoculars", "2a_d3_north", LocationType.binoculars, []),
    "2a_d3_strawberry": LevelLocation("2a_d3_strawberry", "Old Site A - Room d3 Strawberry", "2a_d3_south", LocationType.strawberry, []),
    "2a_d2_strawberry_1": LevelLocation("2a_d2_strawberry_1", "Old Site A - Room d2 Strawberry 1", "2a_d2_north-west", LocationType.strawberry, []),
    "2a_d2_strawberry_2": LevelLocation("2a_d2_strawberry_2", "Old Site A - Room d2 Strawberry 2", "2a_d2_east", LocationType.strawberry, []),
    "2a_d9_cassette": LevelLocation("2a_d9_cassette", "Old Site A - Cassette", "2a_d9_north-west", LocationType.cassette, [[ItemName.dream_blocks, ItemName.pink_cassette_blocks, ItemName.blue_cassette_blocks, ], ]),
    "2a_d1_strawberry": LevelLocation("2a_d1_strawberry", "Old Site A - Room d1 Strawberry", "2a_d1_south-west", LocationType.strawberry, [[ItemName.dream_blocks, ItemName.strawberry_seeds, ], ]),
    "2a_d6_strawberry": LevelLocation("2a_d6_strawberry", "Old Site A - Room d6 Strawberry", "2a_d6_west", LocationType.strawberry, []),
    "2a_d4_strawberry": LevelLocation("2a_d4_strawberry", "Old Site A - Room d4 Strawberry", "2a_d4_west", LocationType.strawberry, [[ItemName.traffic_blocks, ItemName.dream_blocks, ], ]),
    "2a_d5_strawberry": LevelLocation("2a_d5_strawberry", "Old Site A - Room d5 Strawberry", "2a_d5_west", LocationType.strawberry, [[ItemName.dream_blocks, ], ]),
    "2a_4_strawberry": LevelLocation("2a_4_strawberry", "Old Site A - Room 4 Strawberry", "2a_4_bottom", LocationType.strawberry, [[ItemName.dream_blocks, ], ]),
    "2a_5_strawberry": LevelLocation("2a_5_strawberry", "Old Site A - Room 5 Strawberry", "2a_5_bottom", LocationType.strawberry, [[ItemName.dream_blocks, ], ]),
    "2a_8_strawberry": LevelLocation("2a_8_strawberry", "Old Site A - Room 8 Strawberry", "2a_8_bottom", LocationType.strawberry, [[ItemName.dream_blocks, ], ]),
    "2a_9_strawberry": LevelLocation("2a_9_strawberry", "Old Site A - Room 9 Strawberry", "2a_9_south", LocationType.strawberry, [[ItemName.dream_blocks, ], ]),
    "2a_9b_strawberry": LevelLocation("2a_9b_strawberry", "Old Site A - Room 9b Strawberry", "2a_9b_east", LocationType.strawberry, []),
    "2a_10_strawberry": LevelLocation("2a_10_strawberry", "Old Site A - Room 10 Strawberry", "2a_10_top", LocationType.strawberry, [[ItemName.dream_blocks, ], ]),
    "2a_12c_strawberry": LevelLocation("2a_12c_strawberry", "Old Site A - Room 12c Strawberry", "2a_12c_south", LocationType.strawberry, [[ItemName.dream_blocks, ], ]),
    "2a_12d_strawberry": LevelLocation("2a_12d_strawberry", "Old Site A - Room 12d Strawberry", "2a_12d_north-west", LocationType.strawberry, [[ItemName.dream_blocks, ], ]),
    "2a_end_3c_strawberry": LevelLocation("2a_end_3c_strawberry", "Old Site A - Room end_3c Strawberry", "2a_end_3c_bottom", LocationType.strawberry, [[ItemName.springs, ], ]),
    "2a_end_6_clear": LevelLocation("2a_end_6_clear", "Old Site A - Level Clear", "2a_end_6_main", LocationType.level_clear, []),
    "2a_end_6_golden": LevelLocation("2a_end_6_golden", "Old Site A - Golden Strawberry", "2a_end_6_main", LocationType.golden_strawberry, [[ItemName.dream_blocks, ItemName.coins, ItemName.dash_refills, ], ]),

    "2b_10_binoculars": LevelLocation("2b_10_binoculars", "Old Site B - Room 10 Binoculars", "2b_10_west", LocationType.binoculars, []),
    "2b_11_binoculars": LevelLocation("2b_11_binoculars", "Old Site B - Room 11 Binoculars", "2b_11_bottom", LocationType.binoculars, []),
    "2b_end_clear": LevelLocation("2b_end_clear", "Old Site B - Level Clear", "2b_end_goal", LocationType.level_clear, []),
    "2b_end_golden": LevelLocation("2b_end_golden", "Old Site B - Golden Strawberry", "2b_end_goal", LocationType.golden_strawberry, [[ItemName.springs, ItemName.dream_blocks, ItemName.dash_refills, ItemName.coins, ItemName.blue_cassette_blocks, ], ]),

    "2c_02_binoculars": LevelLocation("2c_02_binoculars", "Old Site C - Room 02 Binoculars", "2c_02_west", LocationType.binoculars, []),
    "2c_02_clear": LevelLocation("2c_02_clear", "Old Site C - Level Clear", "2c_02_goal", LocationType.level_clear, []),
    "2c_02_golden": LevelLocation("2c_02_golden", "Old Site C - Golden Strawberry", "2c_02_goal", LocationType.golden_strawberry, [[ItemName.dream_blocks, ItemName.dash_refills, ItemName.coins, ], ]),

    "3a_s2_strawberry_1": LevelLocation("3a_s2_strawberry_1", "Celestial Resort A - Room s2 Strawberry 1", "3a_s2_west", LocationType.strawberry, []),
    "3a_s2_strawberry_2": LevelLocation("3a_s2_strawberry_2", "Celestial Resort A - Room s2 Strawberry 2", "3a_s2_north-west", LocationType.strawberry, []),
    "3a_s3_key_1": LevelLocation("3a_s3_key_1", "Celestial Resort A - Front Door Key", "3a_s3_west", LocationType.key, []),
    "3a_s3_strawberry": LevelLocation("3a_s3_strawberry", "Celestial Resort A - Room s3 Strawberry", "3a_s3_north", LocationType.strawberry, []),
    "3a_00-a_strawberry": LevelLocation("3a_00-a_strawberry", "Celestial Resort A - Room 00-a Strawberry", "3a_00-a_east", LocationType.strawberry, []),
    "3a_02-b_hallway_key_1": LevelLocation("3a_02-b_hallway_key_1", "Celestial Resort A - Hallway Key 1", "3a_02-b_east", LocationType.key, []),
    "3a_00-b_strawberry": LevelLocation("3a_00-b_strawberry", "Celestial Resort A - Room 00-b Strawberry", "3a_00-b_east", LocationType.strawberry, []),
    "3a_04-b_strawberry": LevelLocation("3a_04-b_strawberry", "Celestial Resort A - Room 04-b Strawberry", "3a_04-b_east", LocationType.strawberry, [[ItemName.dash_refills, ], ]),
    "3a_06-a_strawberry": LevelLocation("3a_06-a_strawberry", "Celestial Resort A - Room 06-a Strawberry", "3a_06-a_west", LocationType.strawberry, []),
    "3a_07-b_strawberry": LevelLocation("3a_07-b_strawberry", "Celestial Resort A - Room 07-b Strawberry", "3a_07-b_top", LocationType.strawberry, []),
    "3a_07-b_key_2": LevelLocation("3a_07-b_key_2", "Celestial Resort A - Hallway Key 2", "3a_07-b_east", LocationType.key, []),
    "3a_06-b_strawberry": LevelLocation("3a_06-b_strawberry", "Celestial Resort A - Room 06-b Strawberry", "3a_06-b_east", LocationType.strawberry, []),
    "3a_06-c_strawberry": LevelLocation("3a_06-c_strawberry", "Celestial Resort A - Room 06-c Strawberry", "3a_06-c_south-west", LocationType.strawberry, []),
    "3a_05-c_strawberry": LevelLocation("3a_05-c_strawberry", "Celestial Resort A - Room 05-c Strawberry", "3a_05-c_east", LocationType.strawberry, []),
    "3a_09-b_key_4": LevelLocation("3a_09-b_key_4", "Celestial Resort A - Huge Mess Key", "3a_09-b_center", LocationType.key, [[ItemName.brown_clutter, ItemName.green_clutter, ItemName.pink_clutter, ], ]),
    "3a_10-x_brown_clutter": LevelLocation("3a_10-x_brown_clutter", "Celestial Resort A - Brown Clutter", "3a_10-x_south-east", LocationType.clutter, []),
    "3a_12-y_strawberry": LevelLocation("3a_12-y_strawberry", "Celestial Resort A - Room 12-y Strawberry", "3a_12-y_west", LocationType.strawberry, []),
    "3a_10-y_strawberry": LevelLocation("3a_10-y_strawberry", "Celestial Resort A - Room 10-y Strawberry", "3a_10-y_bottom", LocationType.strawberry, []),
    "3a_11-c_crystal_heart": LevelLocation("3a_11-c_crystal_heart", "Celestial Resort A - Crystal Heart", "3a_11-c_south-east", LocationType.crystal_heart, []),
    "3a_12-c_strawberry": LevelLocation("3a_12-c_strawberry", "Celestial Resort A - Room 12-c Strawberry", "3a_12-c_west", LocationType.strawberry, []),
    "3a_11-d_strawberry": LevelLocation("3a_11-d_strawberry", "Celestial Resort A - Room 11-d Strawberry", "3a_11-d_east", LocationType.strawberry, [[ItemName.dash_refills, ], ]),
    "3a_10-d_green_clutter": LevelLocation("3a_10-d_green_clutter", "Celestial Resort A - Green Clutter", "3a_10-d_main", LocationType.clutter, []),
    "3a_13-b_strawberry": LevelLocation("3a_13-b_strawberry", "Celestial Resort A - Room 13-b Strawberry", "3a_13-b_top", LocationType.strawberry, []),
    "3a_13-x_strawberry": LevelLocation("3a_13-x_strawberry", "Celestial Resort A - Room 13-x Strawberry", "3a_13-x_west", LocationType.strawberry, []),
    "3a_12-x_pink_clutter": LevelLocation("3a_12-x_pink_clutter", "Celestial Resort A - Pink Clutter", "3a_12-x_east", LocationType.clutter, []),
    "3a_08-x_strawberry": LevelLocation("3a_08-x_strawberry", "Celestial Resort A - Room 08-x Strawberry", "3a_08-x_west", LocationType.strawberry, []),
    "3a_06-d_strawberry": LevelLocation("3a_06-d_strawberry", "Celestial Resort A - Room 06-d Strawberry", "3a_06-d_east", LocationType.strawberry, []),
    "3a_04-c_strawberry": LevelLocation("3a_04-c_strawberry", "Celestial Resort A - Room 04-c Strawberry", "3a_04-c_east", LocationType.strawberry, []),
    "3a_02-c_key_5": LevelLocation("3a_02-c_key_5", "Celestial Resort A - Presidential Suite Key", "3a_02-c_west", LocationType.key, []),
    "3a_03-b_strawberry_1": LevelLocation("3a_03-b_strawberry_1", "Celestial Resort A - Room 03-b Strawberry 1", "3a_03-b_west", LocationType.strawberry, []),
    "3a_03-b_strawberry_2": LevelLocation("3a_03-b_strawberry_2", "Celestial Resort A - Room 03-b Strawberry 2", "3a_03-b_west", LocationType.strawberry, [[ItemName.dash_refills, ], ]),
    "3a_01-c_cassette": LevelLocation("3a_01-c_cassette", "Celestial Resort A - Cassette", "3a_01-c_east", LocationType.cassette, [[ItemName.pink_cassette_blocks, ItemName.blue_cassette_blocks, ], ]),
    "3a_roof03_strawberry": LevelLocation("3a_roof03_strawberry", "Celestial Resort A - Room roof03 Strawberry", "3a_roof03_west", LocationType.strawberry, []),
    "3a_roof06_strawberry_1": LevelLocation("3a_roof06_strawberry_1", "Celestial Resort A - Room roof06 Strawberry 1", "3a_roof06_west", LocationType.strawberry, []),
    "3a_roof06_strawberry_2": LevelLocation("3a_roof06_strawberry_2", "Celestial Resort A - Room roof06 Strawberry 2", "3a_roof06_west", LocationType.strawberry, []),
    "3a_roof07_clear": LevelLocation("3a_roof07_clear", "Celestial Resort A - Level Clear", "3a_roof07_main", LocationType.level_clear, []),
    "3a_roof07_golden": LevelLocation("3a_roof07_golden", "Celestial Resort A - Golden Strawberry", "3a_roof07_main", LocationType.golden_strawberry, [[ItemName.dream_blocks, ItemName.coins, ItemName.dash_refills, ], ]),

    "3b_back_binoculars": LevelLocation("3b_back_binoculars", "Celestial Resort B - Room back Binoculars", "3b_back_east", LocationType.binoculars, []),
    "3b_12_binoculars": LevelLocation("3b_12_binoculars", "Celestial Resort B - Room 12 Binoculars", "3b_12_west", LocationType.binoculars, []),
    "3b_end_clear": LevelLocation("3b_end_clear", "Celestial Resort B - Level Clear", "3b_end_goal", LocationType.level_clear, []),
    "3b_end_golden": LevelLocation("3b_end_golden", "Celestial Resort B - Golden Strawberry", "3b_end_goal", LocationType.golden_strawberry, [[ItemName.pink_cassette_blocks, ItemName.blue_cassette_blocks, ItemName.dash_refills, ItemName.springs, ItemName.coins, ItemName.moving_platforms, ItemName.sinking_platforms, ], ]),

    "3c_02_binoculars": LevelLocation("3c_02_binoculars", "Celestial Resort C - Room 02 Binoculars", "3c_02_west", LocationType.binoculars, []),
    "3c_02_clear": LevelLocation("3c_02_clear", "Celestial Resort C - Level Clear", "3c_02_goal", LocationType.level_clear, []),
    "3c_02_golden": LevelLocation("3c_02_golden", "Celestial Resort C - Golden Strawberry", "3c_02_goal", LocationType.golden_strawberry, [[ItemName.sinking_platforms, ItemName.dash_refills, ItemName.coins, ], ]),

    "4a_a-01x_strawberry": LevelLocation("4a_a-01x_strawberry", "Golden Ridge A - Room a-01x Strawberry", "4a_a-01x_west", LocationType.strawberry, []),
    "4a_a-02_strawberry": LevelLocation("4a_a-02_strawberry", "Golden Ridge A - Room a-02 Strawberry", "4a_a-02_west", LocationType.strawberry, []),
    "4a_a-03_strawberry": LevelLocation("4a_a-03_strawberry", "Golden Ridge A - Room a-03 Strawberry", "4a_a-03_west", LocationType.strawberry, [[ItemName.blue_boosters, ], ]),
    "4a_a-04_strawberry": LevelLocation("4a_a-04_strawberry", "Golden Ridge A - Room a-04 Strawberry", "4a_a-04_east", LocationType.strawberry, [[ItemName.blue_clouds, ], ]),
    "4a_a-06_strawberry": LevelLocation("4a_a-06_strawberry", "Golden Ridge A - Room a-06 Strawberry", "4a_a-06_west", LocationType.strawberry, []),
    "4a_a-07_strawberry": LevelLocation("4a_a-07_strawberry", "Golden Ridge A - Room a-07 Strawberry", "4a_a-07_east", LocationType.strawberry, []),
    "4a_a-10_strawberry": LevelLocation("4a_a-10_strawberry", "Golden Ridge A - Room a-10 Strawberry", "4a_a-10_east", LocationType.strawberry, [[ItemName.strawberry_seeds, ItemName.springs, ], ]),
    "4a_a-11_binoculars": LevelLocation("4a_a-11_binoculars", "Golden Ridge A - Room a-11 Binoculars", "4a_a-11_east", LocationType.binoculars, []),
    "4a_a-11_cassette": LevelLocation("4a_a-11_cassette", "Golden Ridge A - Cassette", "4a_a-11_east", LocationType.cassette, [[ItemName.pink_cassette_blocks, ItemName.blue_cassette_blocks, ], ]),
    "4a_a-09_strawberry": LevelLocation("4a_a-09_strawberry", "Golden Ridge A - Room a-09 Strawberry", "4a_a-09_top", LocationType.strawberry, []),
    "4a_b-01_strawberry_1": LevelLocation("4a_b-01_strawberry_1", "Golden Ridge A - Room b-01 Strawberry 1", "4a_b-01_west", LocationType.strawberry, [[ItemName.move_blocks, ], ]),
    "4a_b-01_strawberry_2": LevelLocation("4a_b-01_strawberry_2", "Golden Ridge A - Room b-01 Strawberry 2", "4a_b-01_west", LocationType.strawberry, [[ItemName.move_blocks, ], ]),
    "4a_b-04_strawberry": LevelLocation("4a_b-04_strawberry", "Golden Ridge A - Room b-04 Strawberry", "4a_b-04_north-west", LocationType.strawberry, []),
    "4a_b-07_strawberry": LevelLocation("4a_b-07_strawberry", "Golden Ridge A - Room b-07 Strawberry", "4a_b-07_west", LocationType.strawberry, [[ItemName.move_blocks, ItemName.blue_boosters, ], ]),
    "4a_b-03_strawberry": LevelLocation("4a_b-03_strawberry", "Golden Ridge A - Room b-03 Strawberry", "4a_b-03_west", LocationType.strawberry, [[ItemName.move_blocks, ], ]),
    "4a_b-02_strawberry_1": LevelLocation("4a_b-02_strawberry_1", "Golden Ridge A - Room b-02 Strawberry 1", "4a_b-02_south-west", LocationType.strawberry, [[ItemName.move_blocks, ], ]),
    "4a_b-02_binoculars": LevelLocation("4a_b-02_binoculars", "Golden Ridge A - Room b-02 Binoculars", "4a_b-02_south-west", LocationType.binoculars, []),
    "4a_b-02_strawberry_2": LevelLocation("4a_b-02_strawberry_2", "Golden Ridge A - Room b-02 Strawberry 2", "4a_b-02_north-east", LocationType.strawberry, []),
    "4a_b-sec_crystal_heart": LevelLocation("4a_b-sec_crystal_heart", "Golden Ridge A - Crystal Heart", "4a_b-sec_west", LocationType.crystal_heart, [[ItemName.white_block, ], ]),
    "4a_b-secb_strawberry": LevelLocation("4a_b-secb_strawberry", "Golden Ridge A - Room b-secb Strawberry", "4a_b-secb_west", LocationType.strawberry, [[ItemName.move_blocks, ], ]),
    "4a_b-08_strawberry": LevelLocation("4a_b-08_strawberry", "Golden Ridge A - Room b-08 Strawberry", "4a_b-08_west", LocationType.strawberry, [[ItemName.move_blocks, ItemName.blue_clouds, ], ]),
    "4a_c-00_strawberry": LevelLocation("4a_c-00_strawberry", "Golden Ridge A - Room c-00 Strawberry", "4a_c-00_west", LocationType.strawberry, []),
    "4a_c-01_strawberry": LevelLocation("4a_c-01_strawberry", "Golden Ridge A - Room c-01 Strawberry", "4a_c-01_east", LocationType.strawberry, []),
    "4a_c-05_strawberry": LevelLocation("4a_c-05_strawberry", "Golden Ridge A - Room c-05 Strawberry", "4a_c-05_east", LocationType.strawberry, [[ItemName.blue_boosters, ItemName.move_blocks, ], ]),
    "4a_c-06_strawberry": LevelLocation("4a_c-06_strawberry", "Golden Ridge A - Room c-06 Strawberry", "4a_c-06_west", LocationType.strawberry, [[ItemName.coins, ItemName.move_blocks, ], ]),
    "4a_c-06b_strawberry": LevelLocation("4a_c-06b_strawberry", "Golden Ridge A - Room c-06b Strawberry", "4a_c-06b_east", LocationType.strawberry, [[ItemName.dash_refills, ItemName.blue_boosters, ], ]),
    "4a_c-08_strawberry": LevelLocation("4a_c-08_strawberry", "Golden Ridge A - Room c-08 Strawberry", "4a_c-08_east", LocationType.strawberry, [[ItemName.blue_boosters, ], ]),
    "4a_c-10_strawberry": LevelLocation("4a_c-10_strawberry", "Golden Ridge A - Room c-10 Strawberry", "4a_c-10_top", LocationType.strawberry, []),
    "4a_d-00b_strawberry": LevelLocation("4a_d-00b_strawberry", "Golden Ridge A - Room d-00b Strawberry", "4a_d-00b_east", LocationType.strawberry, [[ItemName.move_blocks, ItemName.blue_boosters, ], ]),
    "4a_d-00b_binoculars": LevelLocation("4a_d-00b_binoculars", "Golden Ridge A - Room d-00b Binoculars", "4a_d-00b_east", LocationType.binoculars, []),
    "4a_d-01_strawberry": LevelLocation("4a_d-01_strawberry", "Golden Ridge A - Room d-01 Strawberry", "4a_d-01_east", LocationType.strawberry, []),
    "4a_d-04_strawberry": LevelLocation("4a_d-04_strawberry", "Golden Ridge A - Room d-04 Strawberry", "4a_d-04_east", LocationType.strawberry, []),
    "4a_d-07_strawberry": LevelLocation("4a_d-07_strawberry", "Golden Ridge A - Room d-07 Strawberry", "4a_d-07_west", LocationType.strawberry, [[ItemName.blue_boosters, ], ]),
    "4a_d-09_strawberry": LevelLocation("4a_d-09_strawberry", "Golden Ridge A - Room d-09 Strawberry", "4a_d-09_west", LocationType.strawberry, [[ItemName.blue_boosters, ], ]),
    "4a_d-10_clear": LevelLocation("4a_d-10_clear", "Golden Ridge A - Level Clear", "4a_d-10_goal", LocationType.level_clear, []),
    "4a_d-10_golden": LevelLocation("4a_d-10_golden", "Golden Ridge A - Golden Strawberry", "4a_d-10_goal", LocationType.golden_strawberry, [[ItemName.blue_clouds, ItemName.pink_clouds, ItemName.blue_boosters, ItemName.move_blocks, ItemName.dash_refills, ItemName.springs, ItemName.coins, ], ]),

    "4b_b-02_binoculars": LevelLocation("4b_b-02_binoculars", "Golden Ridge B - Room b-02 Binoculars", "4b_b-02_bottom", LocationType.binoculars, []),
    "4b_c-03_binoculars": LevelLocation("4b_c-03_binoculars", "Golden Ridge B - Room c-03 Binoculars", "4b_c-03_bottom", LocationType.binoculars, []),
    "4b_d-01_binoculars": LevelLocation("4b_d-01_binoculars", "Golden Ridge B - Room d-01 Binoculars", "4b_d-01_west", LocationType.binoculars, []),
    "4b_end_binoculars": LevelLocation("4b_end_binoculars", "Golden Ridge B - Room end Binoculars", "4b_end_west", LocationType.binoculars, []),
    "4b_end_clear": LevelLocation("4b_end_clear", "Golden Ridge B - Level Clear", "4b_end_goal", LocationType.level_clear, []),
    "4b_end_golden": LevelLocation("4b_end_golden", "Golden Ridge B - Golden Strawberry", "4b_end_goal", LocationType.golden_strawberry, [[ItemName.pink_cassette_blocks, ItemName.blue_cassette_blocks, ItemName.dash_refills, ItemName.springs, ItemName.coins, ItemName.moving_platforms, ItemName.blue_boosters, ItemName.blue_clouds, ItemName.pink_clouds, ItemName.move_blocks, ], ]),

    "4c_01_binoculars": LevelLocation("4c_01_binoculars", "Golden Ridge C - Room 01 Binoculars", "4c_01_west", LocationType.binoculars, []),
    "4c_02_binoculars": LevelLocation("4c_02_binoculars", "Golden Ridge C - Room 02 Binoculars", "4c_02_west", LocationType.binoculars, []),
    "4c_02_clear": LevelLocation("4c_02_clear", "Golden Ridge C - Level Clear", "4c_02_goal", LocationType.level_clear, []),
    "4c_02_golden": LevelLocation("4c_02_golden", "Golden Ridge C - Golden Strawberry", "4c_02_goal", LocationType.golden_strawberry, [[ItemName.pink_clouds, ItemName.blue_boosters, ItemName.move_blocks, ItemName.dash_refills, ], ]),

}

all_regions: Dict[str, PreRegion] = {
    "0a_-1_main": PreRegion("0a_-1_main", "0a_-1", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "0a_-1_main"], [loc for _, loc in all_locations.items() if loc.region_name == "0a_-1_main"]),
    "0a_-1_east": PreRegion("0a_-1_east", "0a_-1", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "0a_-1_east"], [loc for _, loc in all_locations.items() if loc.region_name == "0a_-1_east"]),

    "0a_0_west": PreRegion("0a_0_west", "0a_0", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "0a_0_west"], [loc for _, loc in all_locations.items() if loc.region_name == "0a_0_west"]),
    "0a_0_main": PreRegion("0a_0_main", "0a_0", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "0a_0_main"], [loc for _, loc in all_locations.items() if loc.region_name == "0a_0_main"]),
    "0a_0_north": PreRegion("0a_0_north", "0a_0", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "0a_0_north"], [loc for _, loc in all_locations.items() if loc.region_name == "0a_0_north"]),
    "0a_0_east": PreRegion("0a_0_east", "0a_0", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "0a_0_east"], [loc for _, loc in all_locations.items() if loc.region_name == "0a_0_east"]),

    "0a_0b_south": PreRegion("0a_0b_south", "0a_0b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "0a_0b_south"], [loc for _, loc in all_locations.items() if loc.region_name == "0a_0b_south"]),

    "0a_1_west": PreRegion("0a_1_west", "0a_1", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "0a_1_west"], [loc for _, loc in all_locations.items() if loc.region_name == "0a_1_west"]),
    "0a_1_main": PreRegion("0a_1_main", "0a_1", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "0a_1_main"], [loc for _, loc in all_locations.items() if loc.region_name == "0a_1_main"]),
    "0a_1_east": PreRegion("0a_1_east", "0a_1", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "0a_1_east"], [loc for _, loc in all_locations.items() if loc.region_name == "0a_1_east"]),

    "0a_2_west": PreRegion("0a_2_west", "0a_2", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "0a_2_west"], [loc for _, loc in all_locations.items() if loc.region_name == "0a_2_west"]),
    "0a_2_main": PreRegion("0a_2_main", "0a_2", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "0a_2_main"], [loc for _, loc in all_locations.items() if loc.region_name == "0a_2_main"]),
    "0a_2_east": PreRegion("0a_2_east", "0a_2", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "0a_2_east"], [loc for _, loc in all_locations.items() if loc.region_name == "0a_2_east"]),

    "0a_3_west": PreRegion("0a_3_west", "0a_3", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "0a_3_west"], [loc for _, loc in all_locations.items() if loc.region_name == "0a_3_west"]),
    "0a_3_main": PreRegion("0a_3_main", "0a_3", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "0a_3_main"], [loc for _, loc in all_locations.items() if loc.region_name == "0a_3_main"]),
    "0a_3_east": PreRegion("0a_3_east", "0a_3", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "0a_3_east"], [loc for _, loc in all_locations.items() if loc.region_name == "0a_3_east"]),

    "1a_1_main": PreRegion("1a_1_main", "1a_1", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_1_main"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_1_main"]),
    "1a_1_east": PreRegion("1a_1_east", "1a_1", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_1_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_1_east"]),

    "1a_2_west": PreRegion("1a_2_west", "1a_2", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_2_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_2_west"]),
    "1a_2_east": PreRegion("1a_2_east", "1a_2", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_2_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_2_east"]),

    "1a_3_west": PreRegion("1a_3_west", "1a_3", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_3_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_3_west"]),
    "1a_3_east": PreRegion("1a_3_east", "1a_3", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_3_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_3_east"]),

    "1a_4_west": PreRegion("1a_4_west", "1a_4", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_4_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_4_west"]),
    "1a_4_east": PreRegion("1a_4_east", "1a_4", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_4_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_4_east"]),

    "1a_3b_west": PreRegion("1a_3b_west", "1a_3b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_3b_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_3b_west"]),
    "1a_3b_east": PreRegion("1a_3b_east", "1a_3b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_3b_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_3b_east"]),
    "1a_3b_top": PreRegion("1a_3b_top", "1a_3b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_3b_top"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_3b_top"]),

    "1a_5_bottom": PreRegion("1a_5_bottom", "1a_5", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_5_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_5_bottom"]),
    "1a_5_west": PreRegion("1a_5_west", "1a_5", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_5_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_5_west"]),
    "1a_5_north-west": PreRegion("1a_5_north-west", "1a_5", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_5_north-west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_5_north-west"]),
    "1a_5_center": PreRegion("1a_5_center", "1a_5", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_5_center"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_5_center"]),
    "1a_5_south-east": PreRegion("1a_5_south-east", "1a_5", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_5_south-east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_5_south-east"]),
    "1a_5_north-east": PreRegion("1a_5_north-east", "1a_5", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_5_north-east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_5_north-east"]),
    "1a_5_top": PreRegion("1a_5_top", "1a_5", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_5_top"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_5_top"]),

    "1a_5z_east": PreRegion("1a_5z_east", "1a_5z", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_5z_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_5z_east"]),

    "1a_5a_west": PreRegion("1a_5a_west", "1a_5a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_5a_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_5a_west"]),

    "1a_6_south-west": PreRegion("1a_6_south-west", "1a_6", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_6_south-west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_6_south-west"]),
    "1a_6_west": PreRegion("1a_6_west", "1a_6", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_6_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_6_west"]),
    "1a_6_east": PreRegion("1a_6_east", "1a_6", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_6_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_6_east"]),

    "1a_6z_north-west": PreRegion("1a_6z_north-west", "1a_6z", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_6z_north-west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_6z_north-west"]),
    "1a_6z_west": PreRegion("1a_6z_west", "1a_6z", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_6z_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_6z_west"]),
    "1a_6z_east": PreRegion("1a_6z_east", "1a_6z", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_6z_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_6z_east"]),

    "1a_6zb_north-west": PreRegion("1a_6zb_north-west", "1a_6zb", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_6zb_north-west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_6zb_north-west"]),
    "1a_6zb_main": PreRegion("1a_6zb_main", "1a_6zb", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_6zb_main"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_6zb_main"]),
    "1a_6zb_east": PreRegion("1a_6zb_east", "1a_6zb", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_6zb_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_6zb_east"]),

    "1a_7zb_west": PreRegion("1a_7zb_west", "1a_7zb", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_7zb_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_7zb_west"]),
    "1a_7zb_east": PreRegion("1a_7zb_east", "1a_7zb", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_7zb_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_7zb_east"]),

    "1a_6a_west": PreRegion("1a_6a_west", "1a_6a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_6a_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_6a_west"]),
    "1a_6a_east": PreRegion("1a_6a_east", "1a_6a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_6a_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_6a_east"]),

    "1a_6b_south-west": PreRegion("1a_6b_south-west", "1a_6b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_6b_south-west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_6b_south-west"]),
    "1a_6b_north-west": PreRegion("1a_6b_north-west", "1a_6b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_6b_north-west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_6b_north-west"]),
    "1a_6b_north-east": PreRegion("1a_6b_north-east", "1a_6b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_6b_north-east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_6b_north-east"]),

    "1a_s0_west": PreRegion("1a_s0_west", "1a_s0", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_s0_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_s0_west"]),
    "1a_s0_east": PreRegion("1a_s0_east", "1a_s0", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_s0_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_s0_east"]),

    "1a_s1_east": PreRegion("1a_s1_east", "1a_s1", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_s1_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_s1_east"]),

    "1a_6c_south-west": PreRegion("1a_6c_south-west", "1a_6c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_6c_south-west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_6c_south-west"]),
    "1a_6c_north-west": PreRegion("1a_6c_north-west", "1a_6c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_6c_north-west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_6c_north-west"]),
    "1a_6c_north-east": PreRegion("1a_6c_north-east", "1a_6c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_6c_north-east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_6c_north-east"]),

    "1a_7_west": PreRegion("1a_7_west", "1a_7", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_7_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_7_west"]),
    "1a_7_east": PreRegion("1a_7_east", "1a_7", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_7_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_7_east"]),

    "1a_7z_bottom": PreRegion("1a_7z_bottom", "1a_7z", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_7z_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_7z_bottom"]),
    "1a_7z_top": PreRegion("1a_7z_top", "1a_7z", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_7z_top"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_7z_top"]),

    "1a_8z_bottom": PreRegion("1a_8z_bottom", "1a_8z", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_8z_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_8z_bottom"]),
    "1a_8z_top": PreRegion("1a_8z_top", "1a_8z", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_8z_top"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_8z_top"]),

    "1a_8zb_west": PreRegion("1a_8zb_west", "1a_8zb", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_8zb_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_8zb_west"]),
    "1a_8zb_east": PreRegion("1a_8zb_east", "1a_8zb", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_8zb_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_8zb_east"]),

    "1a_8_south-west": PreRegion("1a_8_south-west", "1a_8", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_8_south-west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_8_south-west"]),
    "1a_8_west": PreRegion("1a_8_west", "1a_8", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_8_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_8_west"]),
    "1a_8_south": PreRegion("1a_8_south", "1a_8", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_8_south"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_8_south"]),
    "1a_8_south-east": PreRegion("1a_8_south-east", "1a_8", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_8_south-east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_8_south-east"]),
    "1a_8_north": PreRegion("1a_8_north", "1a_8", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_8_north"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_8_north"]),
    "1a_8_north-east": PreRegion("1a_8_north-east", "1a_8", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_8_north-east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_8_north-east"]),

    "1a_7a_east": PreRegion("1a_7a_east", "1a_7a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_7a_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_7a_east"]),
    "1a_7a_west": PreRegion("1a_7a_west", "1a_7a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_7a_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_7a_west"]),

    "1a_9z_east": PreRegion("1a_9z_east", "1a_9z", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_9z_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_9z_east"]),

    "1a_8b_east": PreRegion("1a_8b_east", "1a_8b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_8b_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_8b_east"]),
    "1a_8b_west": PreRegion("1a_8b_west", "1a_8b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_8b_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_8b_west"]),

    "1a_9_east": PreRegion("1a_9_east", "1a_9", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_9_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_9_east"]),
    "1a_9_west": PreRegion("1a_9_west", "1a_9", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_9_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_9_west"]),

    "1a_9b_east": PreRegion("1a_9b_east", "1a_9b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_9b_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_9b_east"]),
    "1a_9b_north-east": PreRegion("1a_9b_north-east", "1a_9b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_9b_north-east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_9b_north-east"]),
    "1a_9b_west": PreRegion("1a_9b_west", "1a_9b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_9b_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_9b_west"]),
    "1a_9b_north-west": PreRegion("1a_9b_north-west", "1a_9b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_9b_north-west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_9b_north-west"]),

    "1a_9c_west": PreRegion("1a_9c_west", "1a_9c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_9c_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_9c_west"]),

    "1a_10_south-east": PreRegion("1a_10_south-east", "1a_10", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_10_south-east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_10_south-east"]),
    "1a_10_south-west": PreRegion("1a_10_south-west", "1a_10", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_10_south-west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_10_south-west"]),
    "1a_10_north-west": PreRegion("1a_10_north-west", "1a_10", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_10_north-west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_10_north-west"]),
    "1a_10_north-east": PreRegion("1a_10_north-east", "1a_10", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_10_north-east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_10_north-east"]),

    "1a_10z_west": PreRegion("1a_10z_west", "1a_10z", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_10z_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_10z_west"]),
    "1a_10z_east": PreRegion("1a_10z_east", "1a_10z", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_10z_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_10z_east"]),

    "1a_10zb_east": PreRegion("1a_10zb_east", "1a_10zb", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_10zb_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_10zb_east"]),

    "1a_11_south-east": PreRegion("1a_11_south-east", "1a_11", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_11_south-east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_11_south-east"]),
    "1a_11_south-west": PreRegion("1a_11_south-west", "1a_11", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_11_south-west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_11_south-west"]),
    "1a_11_north": PreRegion("1a_11_north", "1a_11", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_11_north"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_11_north"]),
    "1a_11_west": PreRegion("1a_11_west", "1a_11", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_11_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_11_west"]),
    "1a_11_south": PreRegion("1a_11_south", "1a_11", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_11_south"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_11_south"]),

    "1a_11z_east": PreRegion("1a_11z_east", "1a_11z", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_11z_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_11z_east"]),

    "1a_10a_bottom": PreRegion("1a_10a_bottom", "1a_10a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_10a_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_10a_bottom"]),
    "1a_10a_top": PreRegion("1a_10a_top", "1a_10a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_10a_top"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_10a_top"]),

    "1a_12_south-west": PreRegion("1a_12_south-west", "1a_12", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_12_south-west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_12_south-west"]),
    "1a_12_north-west": PreRegion("1a_12_north-west", "1a_12", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_12_north-west"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_12_north-west"]),
    "1a_12_east": PreRegion("1a_12_east", "1a_12", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_12_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_12_east"]),

    "1a_12z_east": PreRegion("1a_12z_east", "1a_12z", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_12z_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_12z_east"]),

    "1a_12a_bottom": PreRegion("1a_12a_bottom", "1a_12a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_12a_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_12a_bottom"]),
    "1a_12a_top": PreRegion("1a_12a_top", "1a_12a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_12a_top"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_12a_top"]),

    "1a_end_south": PreRegion("1a_end_south", "1a_end", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_end_south"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_end_south"]),
    "1a_end_main": PreRegion("1a_end_main", "1a_end", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1a_end_main"], [loc for _, loc in all_locations.items() if loc.region_name == "1a_end_main"]),

    "1b_00_west": PreRegion("1b_00_west", "1b_00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1b_00_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1b_00_west"]),
    "1b_00_east": PreRegion("1b_00_east", "1b_00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1b_00_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1b_00_east"]),

    "1b_01_west": PreRegion("1b_01_west", "1b_01", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1b_01_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1b_01_west"]),
    "1b_01_east": PreRegion("1b_01_east", "1b_01", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1b_01_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1b_01_east"]),

    "1b_02_west": PreRegion("1b_02_west", "1b_02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1b_02_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1b_02_west"]),
    "1b_02_east": PreRegion("1b_02_east", "1b_02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1b_02_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1b_02_east"]),

    "1b_02b_west": PreRegion("1b_02b_west", "1b_02b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1b_02b_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1b_02b_west"]),
    "1b_02b_east": PreRegion("1b_02b_east", "1b_02b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1b_02b_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1b_02b_east"]),

    "1b_03_west": PreRegion("1b_03_west", "1b_03", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1b_03_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1b_03_west"]),
    "1b_03_east": PreRegion("1b_03_east", "1b_03", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1b_03_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1b_03_east"]),

    "1b_04_west": PreRegion("1b_04_west", "1b_04", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1b_04_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1b_04_west"]),
    "1b_04_east": PreRegion("1b_04_east", "1b_04", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1b_04_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1b_04_east"]),

    "1b_05_west": PreRegion("1b_05_west", "1b_05", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1b_05_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1b_05_west"]),
    "1b_05_east": PreRegion("1b_05_east", "1b_05", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1b_05_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1b_05_east"]),

    "1b_05b_west": PreRegion("1b_05b_west", "1b_05b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1b_05b_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1b_05b_west"]),
    "1b_05b_east": PreRegion("1b_05b_east", "1b_05b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1b_05b_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1b_05b_east"]),

    "1b_06_west": PreRegion("1b_06_west", "1b_06", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1b_06_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1b_06_west"]),
    "1b_06_east": PreRegion("1b_06_east", "1b_06", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1b_06_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1b_06_east"]),

    "1b_07_bottom": PreRegion("1b_07_bottom", "1b_07", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1b_07_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "1b_07_bottom"]),
    "1b_07_top": PreRegion("1b_07_top", "1b_07", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1b_07_top"], [loc for _, loc in all_locations.items() if loc.region_name == "1b_07_top"]),

    "1b_08_west": PreRegion("1b_08_west", "1b_08", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1b_08_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1b_08_west"]),
    "1b_08_east": PreRegion("1b_08_east", "1b_08", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1b_08_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1b_08_east"]),

    "1b_08b_west": PreRegion("1b_08b_west", "1b_08b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1b_08b_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1b_08b_west"]),
    "1b_08b_east": PreRegion("1b_08b_east", "1b_08b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1b_08b_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1b_08b_east"]),

    "1b_09_west": PreRegion("1b_09_west", "1b_09", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1b_09_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1b_09_west"]),
    "1b_09_east": PreRegion("1b_09_east", "1b_09", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1b_09_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1b_09_east"]),

    "1b_10_west": PreRegion("1b_10_west", "1b_10", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1b_10_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1b_10_west"]),
    "1b_10_east": PreRegion("1b_10_east", "1b_10", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1b_10_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1b_10_east"]),

    "1b_11_bottom": PreRegion("1b_11_bottom", "1b_11", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1b_11_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "1b_11_bottom"]),
    "1b_11_top": PreRegion("1b_11_top", "1b_11", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1b_11_top"], [loc for _, loc in all_locations.items() if loc.region_name == "1b_11_top"]),

    "1b_end_west": PreRegion("1b_end_west", "1b_end", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1b_end_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1b_end_west"]),
    "1b_end_goal": PreRegion("1b_end_goal", "1b_end", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1b_end_goal"], [loc for _, loc in all_locations.items() if loc.region_name == "1b_end_goal"]),

    "1c_00_west": PreRegion("1c_00_west", "1c_00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1c_00_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1c_00_west"]),
    "1c_00_east": PreRegion("1c_00_east", "1c_00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1c_00_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1c_00_east"]),

    "1c_01_west": PreRegion("1c_01_west", "1c_01", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1c_01_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1c_01_west"]),
    "1c_01_east": PreRegion("1c_01_east", "1c_01", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1c_01_east"], [loc for _, loc in all_locations.items() if loc.region_name == "1c_01_east"]),

    "1c_02_west": PreRegion("1c_02_west", "1c_02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1c_02_west"], [loc for _, loc in all_locations.items() if loc.region_name == "1c_02_west"]),
    "1c_02_goal": PreRegion("1c_02_goal", "1c_02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "1c_02_goal"], [loc for _, loc in all_locations.items() if loc.region_name == "1c_02_goal"]),

    "2a_start_main": PreRegion("2a_start_main", "2a_start", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_start_main"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_start_main"]),
    "2a_start_top": PreRegion("2a_start_top", "2a_start", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_start_top"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_start_top"]),
    "2a_start_east": PreRegion("2a_start_east", "2a_start", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_start_east"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_start_east"]),

    "2a_s0_bottom": PreRegion("2a_s0_bottom", "2a_s0", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_s0_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_s0_bottom"]),
    "2a_s0_top": PreRegion("2a_s0_top", "2a_s0", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_s0_top"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_s0_top"]),

    "2a_s1_bottom": PreRegion("2a_s1_bottom", "2a_s1", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_s1_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_s1_bottom"]),
    "2a_s1_top": PreRegion("2a_s1_top", "2a_s1", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_s1_top"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_s1_top"]),

    "2a_s2_bottom": PreRegion("2a_s2_bottom", "2a_s2", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_s2_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_s2_bottom"]),

    "2a_0_south-west": PreRegion("2a_0_south-west", "2a_0", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_0_south-west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_0_south-west"]),
    "2a_0_south-east": PreRegion("2a_0_south-east", "2a_0", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_0_south-east"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_0_south-east"]),
    "2a_0_north-west": PreRegion("2a_0_north-west", "2a_0", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_0_north-west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_0_north-west"]),
    "2a_0_north-east": PreRegion("2a_0_north-east", "2a_0", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_0_north-east"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_0_north-east"]),

    "2a_1_south-west": PreRegion("2a_1_south-west", "2a_1", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_1_south-west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_1_south-west"]),
    "2a_1_south": PreRegion("2a_1_south", "2a_1", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_1_south"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_1_south"]),
    "2a_1_south-east": PreRegion("2a_1_south-east", "2a_1", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_1_south-east"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_1_south-east"]),
    "2a_1_north-west": PreRegion("2a_1_north-west", "2a_1", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_1_north-west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_1_north-west"]),

    "2a_d0_north": PreRegion("2a_d0_north", "2a_d0", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_d0_north"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_d0_north"]),
    "2a_d0_north-west": PreRegion("2a_d0_north-west", "2a_d0", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_d0_north-west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_d0_north-west"]),
    "2a_d0_west": PreRegion("2a_d0_west", "2a_d0", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_d0_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_d0_west"]),
    "2a_d0_south-west": PreRegion("2a_d0_south-west", "2a_d0", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_d0_south-west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_d0_south-west"]),
    "2a_d0_south": PreRegion("2a_d0_south", "2a_d0", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_d0_south"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_d0_south"]),
    "2a_d0_south-east": PreRegion("2a_d0_south-east", "2a_d0", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_d0_south-east"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_d0_south-east"]),
    "2a_d0_east": PreRegion("2a_d0_east", "2a_d0", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_d0_east"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_d0_east"]),
    "2a_d0_north-east": PreRegion("2a_d0_north-east", "2a_d0", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_d0_north-east"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_d0_north-east"]),

    "2a_d7_west": PreRegion("2a_d7_west", "2a_d7", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_d7_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_d7_west"]),
    "2a_d7_east": PreRegion("2a_d7_east", "2a_d7", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_d7_east"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_d7_east"]),

    "2a_d8_west": PreRegion("2a_d8_west", "2a_d8", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_d8_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_d8_west"]),
    "2a_d8_south-east": PreRegion("2a_d8_south-east", "2a_d8", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_d8_south-east"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_d8_south-east"]),
    "2a_d8_north-east": PreRegion("2a_d8_north-east", "2a_d8", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_d8_north-east"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_d8_north-east"]),

    "2a_d3_west": PreRegion("2a_d3_west", "2a_d3", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_d3_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_d3_west"]),
    "2a_d3_north": PreRegion("2a_d3_north", "2a_d3", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_d3_north"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_d3_north"]),
    "2a_d3_south": PreRegion("2a_d3_south", "2a_d3", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_d3_south"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_d3_south"]),

    "2a_d2_west": PreRegion("2a_d2_west", "2a_d2", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_d2_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_d2_west"]),
    "2a_d2_north-west": PreRegion("2a_d2_north-west", "2a_d2", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_d2_north-west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_d2_north-west"]),
    "2a_d2_east": PreRegion("2a_d2_east", "2a_d2", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_d2_east"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_d2_east"]),

    "2a_d9_north-west": PreRegion("2a_d9_north-west", "2a_d9", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_d9_north-west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_d9_north-west"]),

    "2a_d1_south-west": PreRegion("2a_d1_south-west", "2a_d1", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_d1_south-west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_d1_south-west"]),
    "2a_d1_south-east": PreRegion("2a_d1_south-east", "2a_d1", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_d1_south-east"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_d1_south-east"]),
    "2a_d1_north-east": PreRegion("2a_d1_north-east", "2a_d1", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_d1_north-east"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_d1_north-east"]),

    "2a_d6_west": PreRegion("2a_d6_west", "2a_d6", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_d6_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_d6_west"]),
    "2a_d6_east": PreRegion("2a_d6_east", "2a_d6", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_d6_east"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_d6_east"]),

    "2a_d4_west": PreRegion("2a_d4_west", "2a_d4", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_d4_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_d4_west"]),
    "2a_d4_east": PreRegion("2a_d4_east", "2a_d4", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_d4_east"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_d4_east"]),
    "2a_d4_south": PreRegion("2a_d4_south", "2a_d4", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_d4_south"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_d4_south"]),

    "2a_d5_west": PreRegion("2a_d5_west", "2a_d5", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_d5_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_d5_west"]),

    "2a_3x_bottom": PreRegion("2a_3x_bottom", "2a_3x", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_3x_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_3x_bottom"]),
    "2a_3x_top": PreRegion("2a_3x_top", "2a_3x", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_3x_top"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_3x_top"]),

    "2a_3_bottom": PreRegion("2a_3_bottom", "2a_3", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_3_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_3_bottom"]),
    "2a_3_top": PreRegion("2a_3_top", "2a_3", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_3_top"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_3_top"]),

    "2a_4_bottom": PreRegion("2a_4_bottom", "2a_4", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_4_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_4_bottom"]),
    "2a_4_top": PreRegion("2a_4_top", "2a_4", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_4_top"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_4_top"]),

    "2a_5_bottom": PreRegion("2a_5_bottom", "2a_5", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_5_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_5_bottom"]),
    "2a_5_top": PreRegion("2a_5_top", "2a_5", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_5_top"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_5_top"]),

    "2a_6_bottom": PreRegion("2a_6_bottom", "2a_6", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_6_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_6_bottom"]),
    "2a_6_top": PreRegion("2a_6_top", "2a_6", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_6_top"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_6_top"]),

    "2a_7_bottom": PreRegion("2a_7_bottom", "2a_7", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_7_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_7_bottom"]),
    "2a_7_top": PreRegion("2a_7_top", "2a_7", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_7_top"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_7_top"]),

    "2a_8_bottom": PreRegion("2a_8_bottom", "2a_8", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_8_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_8_bottom"]),
    "2a_8_top": PreRegion("2a_8_top", "2a_8", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_8_top"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_8_top"]),

    "2a_9_west": PreRegion("2a_9_west", "2a_9", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_9_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_9_west"]),
    "2a_9_north": PreRegion("2a_9_north", "2a_9", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_9_north"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_9_north"]),
    "2a_9_north-west": PreRegion("2a_9_north-west", "2a_9", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_9_north-west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_9_north-west"]),
    "2a_9_south": PreRegion("2a_9_south", "2a_9", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_9_south"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_9_south"]),
    "2a_9_south-east": PreRegion("2a_9_south-east", "2a_9", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_9_south-east"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_9_south-east"]),

    "2a_9b_east": PreRegion("2a_9b_east", "2a_9b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_9b_east"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_9b_east"]),
    "2a_9b_west": PreRegion("2a_9b_west", "2a_9b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_9b_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_9b_west"]),

    "2a_10_top": PreRegion("2a_10_top", "2a_10", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_10_top"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_10_top"]),
    "2a_10_bottom": PreRegion("2a_10_bottom", "2a_10", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_10_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_10_bottom"]),

    "2a_2_north-west": PreRegion("2a_2_north-west", "2a_2", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_2_north-west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_2_north-west"]),
    "2a_2_south-west": PreRegion("2a_2_south-west", "2a_2", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_2_south-west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_2_south-west"]),
    "2a_2_south-east": PreRegion("2a_2_south-east", "2a_2", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_2_south-east"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_2_south-east"]),

    "2a_11_west": PreRegion("2a_11_west", "2a_11", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_11_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_11_west"]),
    "2a_11_east": PreRegion("2a_11_east", "2a_11", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_11_east"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_11_east"]),

    "2a_12b_west": PreRegion("2a_12b_west", "2a_12b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_12b_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_12b_west"]),
    "2a_12b_north": PreRegion("2a_12b_north", "2a_12b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_12b_north"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_12b_north"]),
    "2a_12b_south": PreRegion("2a_12b_south", "2a_12b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_12b_south"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_12b_south"]),
    "2a_12b_east": PreRegion("2a_12b_east", "2a_12b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_12b_east"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_12b_east"]),
    "2a_12b_south-east": PreRegion("2a_12b_south-east", "2a_12b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_12b_south-east"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_12b_south-east"]),

    "2a_12c_south": PreRegion("2a_12c_south", "2a_12c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_12c_south"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_12c_south"]),

    "2a_12d_north-west": PreRegion("2a_12d_north-west", "2a_12d", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_12d_north-west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_12d_north-west"]),
    "2a_12d_north": PreRegion("2a_12d_north", "2a_12d", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_12d_north"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_12d_north"]),

    "2a_12_west": PreRegion("2a_12_west", "2a_12", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_12_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_12_west"]),
    "2a_12_east": PreRegion("2a_12_east", "2a_12", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_12_east"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_12_east"]),

    "2a_13_west": PreRegion("2a_13_west", "2a_13", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_13_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_13_west"]),
    "2a_13_phone": PreRegion("2a_13_phone", "2a_13", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_13_phone"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_13_phone"]),

    "2a_end_0_main": PreRegion("2a_end_0_main", "2a_end_0", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_end_0_main"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_end_0_main"]),
    "2a_end_0_top": PreRegion("2a_end_0_top", "2a_end_0", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_end_0_top"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_end_0_top"]),
    "2a_end_0_east": PreRegion("2a_end_0_east", "2a_end_0", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_end_0_east"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_end_0_east"]),

    "2a_end_s0_bottom": PreRegion("2a_end_s0_bottom", "2a_end_s0", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_end_s0_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_end_s0_bottom"]),
    "2a_end_s0_top": PreRegion("2a_end_s0_top", "2a_end_s0", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_end_s0_top"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_end_s0_top"]),

    "2a_end_s1_bottom": PreRegion("2a_end_s1_bottom", "2a_end_s1", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_end_s1_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_end_s1_bottom"]),

    "2a_end_1_west": PreRegion("2a_end_1_west", "2a_end_1", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_end_1_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_end_1_west"]),
    "2a_end_1_north-east": PreRegion("2a_end_1_north-east", "2a_end_1", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_end_1_north-east"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_end_1_north-east"]),
    "2a_end_1_east": PreRegion("2a_end_1_east", "2a_end_1", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_end_1_east"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_end_1_east"]),

    "2a_end_2_north-west": PreRegion("2a_end_2_north-west", "2a_end_2", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_end_2_north-west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_end_2_north-west"]),
    "2a_end_2_west": PreRegion("2a_end_2_west", "2a_end_2", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_end_2_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_end_2_west"]),
    "2a_end_2_north-east": PreRegion("2a_end_2_north-east", "2a_end_2", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_end_2_north-east"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_end_2_north-east"]),
    "2a_end_2_east": PreRegion("2a_end_2_east", "2a_end_2", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_end_2_east"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_end_2_east"]),

    "2a_end_3_north-west": PreRegion("2a_end_3_north-west", "2a_end_3", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_end_3_north-west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_end_3_north-west"]),
    "2a_end_3_west": PreRegion("2a_end_3_west", "2a_end_3", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_end_3_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_end_3_west"]),
    "2a_end_3_east": PreRegion("2a_end_3_east", "2a_end_3", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_end_3_east"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_end_3_east"]),

    "2a_end_4_west": PreRegion("2a_end_4_west", "2a_end_4", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_end_4_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_end_4_west"]),
    "2a_end_4_east": PreRegion("2a_end_4_east", "2a_end_4", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_end_4_east"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_end_4_east"]),

    "2a_end_3b_west": PreRegion("2a_end_3b_west", "2a_end_3b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_end_3b_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_end_3b_west"]),
    "2a_end_3b_north": PreRegion("2a_end_3b_north", "2a_end_3b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_end_3b_north"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_end_3b_north"]),
    "2a_end_3b_east": PreRegion("2a_end_3b_east", "2a_end_3b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_end_3b_east"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_end_3b_east"]),

    "2a_end_3cb_bottom": PreRegion("2a_end_3cb_bottom", "2a_end_3cb", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_end_3cb_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_end_3cb_bottom"]),
    "2a_end_3cb_top": PreRegion("2a_end_3cb_top", "2a_end_3cb", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_end_3cb_top"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_end_3cb_top"]),

    "2a_end_3c_bottom": PreRegion("2a_end_3c_bottom", "2a_end_3c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_end_3c_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_end_3c_bottom"]),

    "2a_end_5_west": PreRegion("2a_end_5_west", "2a_end_5", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_end_5_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_end_5_west"]),
    "2a_end_5_east": PreRegion("2a_end_5_east", "2a_end_5", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_end_5_east"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_end_5_east"]),

    "2a_end_6_west": PreRegion("2a_end_6_west", "2a_end_6", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_end_6_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_end_6_west"]),
    "2a_end_6_main": PreRegion("2a_end_6_main", "2a_end_6", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2a_end_6_main"], [loc for _, loc in all_locations.items() if loc.region_name == "2a_end_6_main"]),

    "2b_start_west": PreRegion("2b_start_west", "2b_start", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_start_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_start_west"]),
    "2b_start_east": PreRegion("2b_start_east", "2b_start", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_start_east"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_start_east"]),

    "2b_00_west": PreRegion("2b_00_west", "2b_00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_00_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_00_west"]),
    "2b_00_east": PreRegion("2b_00_east", "2b_00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_00_east"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_00_east"]),

    "2b_01_west": PreRegion("2b_01_west", "2b_01", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_01_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_01_west"]),
    "2b_01_east": PreRegion("2b_01_east", "2b_01", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_01_east"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_01_east"]),

    "2b_01b_west": PreRegion("2b_01b_west", "2b_01b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_01b_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_01b_west"]),
    "2b_01b_east": PreRegion("2b_01b_east", "2b_01b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_01b_east"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_01b_east"]),

    "2b_02b_west": PreRegion("2b_02b_west", "2b_02b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_02b_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_02b_west"]),
    "2b_02b_east": PreRegion("2b_02b_east", "2b_02b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_02b_east"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_02b_east"]),

    "2b_02_west": PreRegion("2b_02_west", "2b_02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_02_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_02_west"]),
    "2b_02_east": PreRegion("2b_02_east", "2b_02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_02_east"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_02_east"]),

    "2b_03_west": PreRegion("2b_03_west", "2b_03", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_03_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_03_west"]),
    "2b_03_east": PreRegion("2b_03_east", "2b_03", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_03_east"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_03_east"]),

    "2b_04_bottom": PreRegion("2b_04_bottom", "2b_04", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_04_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_04_bottom"]),
    "2b_04_top": PreRegion("2b_04_top", "2b_04", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_04_top"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_04_top"]),

    "2b_05_bottom": PreRegion("2b_05_bottom", "2b_05", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_05_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_05_bottom"]),
    "2b_05_top": PreRegion("2b_05_top", "2b_05", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_05_top"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_05_top"]),

    "2b_06_west": PreRegion("2b_06_west", "2b_06", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_06_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_06_west"]),
    "2b_06_east": PreRegion("2b_06_east", "2b_06", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_06_east"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_06_east"]),

    "2b_07_bottom": PreRegion("2b_07_bottom", "2b_07", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_07_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_07_bottom"]),
    "2b_07_top": PreRegion("2b_07_top", "2b_07", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_07_top"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_07_top"]),

    "2b_08b_west": PreRegion("2b_08b_west", "2b_08b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_08b_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_08b_west"]),
    "2b_08b_east": PreRegion("2b_08b_east", "2b_08b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_08b_east"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_08b_east"]),

    "2b_08_west": PreRegion("2b_08_west", "2b_08", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_08_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_08_west"]),
    "2b_08_east": PreRegion("2b_08_east", "2b_08", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_08_east"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_08_east"]),

    "2b_09_west": PreRegion("2b_09_west", "2b_09", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_09_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_09_west"]),
    "2b_09_east": PreRegion("2b_09_east", "2b_09", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_09_east"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_09_east"]),

    "2b_10_west": PreRegion("2b_10_west", "2b_10", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_10_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_10_west"]),
    "2b_10_east": PreRegion("2b_10_east", "2b_10", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_10_east"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_10_east"]),

    "2b_11_bottom": PreRegion("2b_11_bottom", "2b_11", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_11_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_11_bottom"]),
    "2b_11_top": PreRegion("2b_11_top", "2b_11", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_11_top"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_11_top"]),

    "2b_end_west": PreRegion("2b_end_west", "2b_end", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_end_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_end_west"]),
    "2b_end_goal": PreRegion("2b_end_goal", "2b_end", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2b_end_goal"], [loc for _, loc in all_locations.items() if loc.region_name == "2b_end_goal"]),

    "2c_00_west": PreRegion("2c_00_west", "2c_00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2c_00_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2c_00_west"]),
    "2c_00_east": PreRegion("2c_00_east", "2c_00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2c_00_east"], [loc for _, loc in all_locations.items() if loc.region_name == "2c_00_east"]),

    "2c_01_west": PreRegion("2c_01_west", "2c_01", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2c_01_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2c_01_west"]),
    "2c_01_east": PreRegion("2c_01_east", "2c_01", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2c_01_east"], [loc for _, loc in all_locations.items() if loc.region_name == "2c_01_east"]),

    "2c_02_west": PreRegion("2c_02_west", "2c_02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2c_02_west"], [loc for _, loc in all_locations.items() if loc.region_name == "2c_02_west"]),
    "2c_02_goal": PreRegion("2c_02_goal", "2c_02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "2c_02_goal"], [loc for _, loc in all_locations.items() if loc.region_name == "2c_02_goal"]),

    "3a_s0_main": PreRegion("3a_s0_main", "3a_s0", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_s0_main"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_s0_main"]),
    "3a_s0_east": PreRegion("3a_s0_east", "3a_s0", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_s0_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_s0_east"]),

    "3a_s1_west": PreRegion("3a_s1_west", "3a_s1", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_s1_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_s1_west"]),
    "3a_s1_east": PreRegion("3a_s1_east", "3a_s1", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_s1_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_s1_east"]),
    "3a_s1_north-east": PreRegion("3a_s1_north-east", "3a_s1", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_s1_north-east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_s1_north-east"]),

    "3a_s2_west": PreRegion("3a_s2_west", "3a_s2", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_s2_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_s2_west"]),
    "3a_s2_north-west": PreRegion("3a_s2_north-west", "3a_s2", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_s2_north-west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_s2_north-west"]),
    "3a_s2_east": PreRegion("3a_s2_east", "3a_s2", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_s2_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_s2_east"]),

    "3a_s3_west": PreRegion("3a_s3_west", "3a_s3", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_s3_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_s3_west"]),
    "3a_s3_north": PreRegion("3a_s3_north", "3a_s3", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_s3_north"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_s3_north"]),
    "3a_s3_east": PreRegion("3a_s3_east", "3a_s3", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_s3_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_s3_east"]),

    "3a_0x-a_west": PreRegion("3a_0x-a_west", "3a_0x-a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_0x-a_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_0x-a_west"]),
    "3a_0x-a_east": PreRegion("3a_0x-a_east", "3a_0x-a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_0x-a_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_0x-a_east"]),

    "3a_00-a_west": PreRegion("3a_00-a_west", "3a_00-a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_00-a_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_00-a_west"]),
    "3a_00-a_east": PreRegion("3a_00-a_east", "3a_00-a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_00-a_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_00-a_east"]),

    "3a_02-a_west": PreRegion("3a_02-a_west", "3a_02-a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_02-a_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_02-a_west"]),
    "3a_02-a_top": PreRegion("3a_02-a_top", "3a_02-a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_02-a_top"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_02-a_top"]),
    "3a_02-a_main": PreRegion("3a_02-a_main", "3a_02-a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_02-a_main"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_02-a_main"]),
    "3a_02-a_east": PreRegion("3a_02-a_east", "3a_02-a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_02-a_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_02-a_east"]),

    "3a_02-b_west": PreRegion("3a_02-b_west", "3a_02-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_02-b_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_02-b_west"]),
    "3a_02-b_east": PreRegion("3a_02-b_east", "3a_02-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_02-b_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_02-b_east"]),
    "3a_02-b_far-east": PreRegion("3a_02-b_far-east", "3a_02-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_02-b_far-east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_02-b_far-east"]),

    "3a_01-b_west": PreRegion("3a_01-b_west", "3a_01-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_01-b_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_01-b_west"]),
    "3a_01-b_north-west": PreRegion("3a_01-b_north-west", "3a_01-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_01-b_north-west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_01-b_north-west"]),
    "3a_01-b_east": PreRegion("3a_01-b_east", "3a_01-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_01-b_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_01-b_east"]),

    "3a_00-b_south-west": PreRegion("3a_00-b_south-west", "3a_00-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_00-b_south-west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_00-b_south-west"]),
    "3a_00-b_south-east": PreRegion("3a_00-b_south-east", "3a_00-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_00-b_south-east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_00-b_south-east"]),
    "3a_00-b_west": PreRegion("3a_00-b_west", "3a_00-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_00-b_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_00-b_west"]),
    "3a_00-b_north-west": PreRegion("3a_00-b_north-west", "3a_00-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_00-b_north-west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_00-b_north-west"]),
    "3a_00-b_east": PreRegion("3a_00-b_east", "3a_00-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_00-b_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_00-b_east"]),
    "3a_00-b_north": PreRegion("3a_00-b_north", "3a_00-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_00-b_north"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_00-b_north"]),

    "3a_00-c_south-west": PreRegion("3a_00-c_south-west", "3a_00-c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_00-c_south-west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_00-c_south-west"]),
    "3a_00-c_south-east": PreRegion("3a_00-c_south-east", "3a_00-c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_00-c_south-east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_00-c_south-east"]),
    "3a_00-c_north-east": PreRegion("3a_00-c_north-east", "3a_00-c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_00-c_north-east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_00-c_north-east"]),

    "3a_0x-b_west": PreRegion("3a_0x-b_west", "3a_0x-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_0x-b_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_0x-b_west"]),
    "3a_0x-b_south-east": PreRegion("3a_0x-b_south-east", "3a_0x-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_0x-b_south-east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_0x-b_south-east"]),
    "3a_0x-b_north-east": PreRegion("3a_0x-b_north-east", "3a_0x-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_0x-b_north-east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_0x-b_north-east"]),

    "3a_03-a_west": PreRegion("3a_03-a_west", "3a_03-a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_03-a_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_03-a_west"]),
    "3a_03-a_top": PreRegion("3a_03-a_top", "3a_03-a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_03-a_top"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_03-a_top"]),
    "3a_03-a_east": PreRegion("3a_03-a_east", "3a_03-a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_03-a_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_03-a_east"]),

    "3a_04-b_west": PreRegion("3a_04-b_west", "3a_04-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_04-b_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_04-b_west"]),
    "3a_04-b_east": PreRegion("3a_04-b_east", "3a_04-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_04-b_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_04-b_east"]),

    "3a_05-a_west": PreRegion("3a_05-a_west", "3a_05-a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_05-a_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_05-a_west"]),
    "3a_05-a_east": PreRegion("3a_05-a_east", "3a_05-a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_05-a_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_05-a_east"]),

    "3a_06-a_west": PreRegion("3a_06-a_west", "3a_06-a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_06-a_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_06-a_west"]),
    "3a_06-a_east": PreRegion("3a_06-a_east", "3a_06-a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_06-a_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_06-a_east"]),

    "3a_07-a_west": PreRegion("3a_07-a_west", "3a_07-a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_07-a_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_07-a_west"]),
    "3a_07-a_top": PreRegion("3a_07-a_top", "3a_07-a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_07-a_top"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_07-a_top"]),
    "3a_07-a_east": PreRegion("3a_07-a_east", "3a_07-a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_07-a_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_07-a_east"]),

    "3a_07-b_bottom": PreRegion("3a_07-b_bottom", "3a_07-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_07-b_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_07-b_bottom"]),
    "3a_07-b_west": PreRegion("3a_07-b_west", "3a_07-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_07-b_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_07-b_west"]),
    "3a_07-b_top": PreRegion("3a_07-b_top", "3a_07-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_07-b_top"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_07-b_top"]),
    "3a_07-b_east": PreRegion("3a_07-b_east", "3a_07-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_07-b_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_07-b_east"]),

    "3a_06-b_west": PreRegion("3a_06-b_west", "3a_06-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_06-b_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_06-b_west"]),
    "3a_06-b_east": PreRegion("3a_06-b_east", "3a_06-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_06-b_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_06-b_east"]),

    "3a_06-c_south-west": PreRegion("3a_06-c_south-west", "3a_06-c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_06-c_south-west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_06-c_south-west"]),
    "3a_06-c_north-west": PreRegion("3a_06-c_north-west", "3a_06-c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_06-c_north-west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_06-c_north-west"]),
    "3a_06-c_south-east": PreRegion("3a_06-c_south-east", "3a_06-c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_06-c_south-east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_06-c_south-east"]),
    "3a_06-c_east": PreRegion("3a_06-c_east", "3a_06-c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_06-c_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_06-c_east"]),

    "3a_05-c_east": PreRegion("3a_05-c_east", "3a_05-c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_05-c_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_05-c_east"]),

    "3a_08-c_west": PreRegion("3a_08-c_west", "3a_08-c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_08-c_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_08-c_west"]),
    "3a_08-c_east": PreRegion("3a_08-c_east", "3a_08-c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_08-c_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_08-c_east"]),

    "3a_08-b_west": PreRegion("3a_08-b_west", "3a_08-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_08-b_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_08-b_west"]),
    "3a_08-b_east": PreRegion("3a_08-b_east", "3a_08-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_08-b_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_08-b_east"]),

    "3a_08-a_west": PreRegion("3a_08-a_west", "3a_08-a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_08-a_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_08-a_west"]),
    "3a_08-a_bottom": PreRegion("3a_08-a_bottom", "3a_08-a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_08-a_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_08-a_bottom"]),
    "3a_08-a_east": PreRegion("3a_08-a_east", "3a_08-a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_08-a_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_08-a_east"]),

    "3a_09-b_west": PreRegion("3a_09-b_west", "3a_09-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_09-b_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_09-b_west"]),
    "3a_09-b_north-west": PreRegion("3a_09-b_north-west", "3a_09-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_09-b_north-west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_09-b_north-west"]),
    "3a_09-b_center": PreRegion("3a_09-b_center", "3a_09-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_09-b_center"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_09-b_center"]),
    "3a_09-b_south-west": PreRegion("3a_09-b_south-west", "3a_09-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_09-b_south-west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_09-b_south-west"]),
    "3a_09-b_south": PreRegion("3a_09-b_south", "3a_09-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_09-b_south"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_09-b_south"]),
    "3a_09-b_south-east": PreRegion("3a_09-b_south-east", "3a_09-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_09-b_south-east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_09-b_south-east"]),
    "3a_09-b_east": PreRegion("3a_09-b_east", "3a_09-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_09-b_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_09-b_east"]),
    "3a_09-b_north-east-right": PreRegion("3a_09-b_north-east-right", "3a_09-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_09-b_north-east-right"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_09-b_north-east-right"]),
    "3a_09-b_north-east-top": PreRegion("3a_09-b_north-east-top", "3a_09-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_09-b_north-east-top"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_09-b_north-east-top"]),
    "3a_09-b_north": PreRegion("3a_09-b_north", "3a_09-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_09-b_north"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_09-b_north"]),

    "3a_10-x_west": PreRegion("3a_10-x_west", "3a_10-x", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_10-x_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_10-x_west"]),
    "3a_10-x_south-east": PreRegion("3a_10-x_south-east", "3a_10-x", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_10-x_south-east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_10-x_south-east"]),
    "3a_10-x_north-east-top": PreRegion("3a_10-x_north-east-top", "3a_10-x", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_10-x_north-east-top"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_10-x_north-east-top"]),
    "3a_10-x_north-east-right": PreRegion("3a_10-x_north-east-right", "3a_10-x", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_10-x_north-east-right"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_10-x_north-east-right"]),

    "3a_11-x_west": PreRegion("3a_11-x_west", "3a_11-x", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_11-x_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_11-x_west"]),
    "3a_11-x_south": PreRegion("3a_11-x_south", "3a_11-x", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_11-x_south"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_11-x_south"]),

    "3a_11-y_west": PreRegion("3a_11-y_west", "3a_11-y", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_11-y_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_11-y_west"]),
    "3a_11-y_east": PreRegion("3a_11-y_east", "3a_11-y", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_11-y_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_11-y_east"]),
    "3a_11-y_south": PreRegion("3a_11-y_south", "3a_11-y", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_11-y_south"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_11-y_south"]),

    "3a_12-y_west": PreRegion("3a_12-y_west", "3a_12-y", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_12-y_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_12-y_west"]),

    "3a_11-z_west": PreRegion("3a_11-z_west", "3a_11-z", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_11-z_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_11-z_west"]),
    "3a_11-z_east": PreRegion("3a_11-z_east", "3a_11-z", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_11-z_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_11-z_east"]),

    "3a_10-z_bottom": PreRegion("3a_10-z_bottom", "3a_10-z", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_10-z_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_10-z_bottom"]),
    "3a_10-z_top": PreRegion("3a_10-z_top", "3a_10-z", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_10-z_top"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_10-z_top"]),

    "3a_10-y_bottom": PreRegion("3a_10-y_bottom", "3a_10-y", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_10-y_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_10-y_bottom"]),
    "3a_10-y_top": PreRegion("3a_10-y_top", "3a_10-y", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_10-y_top"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_10-y_top"]),

    "3a_10-c_south-east": PreRegion("3a_10-c_south-east", "3a_10-c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_10-c_south-east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_10-c_south-east"]),
    "3a_10-c_north-east": PreRegion("3a_10-c_north-east", "3a_10-c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_10-c_north-east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_10-c_north-east"]),
    "3a_10-c_north-west": PreRegion("3a_10-c_north-west", "3a_10-c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_10-c_north-west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_10-c_north-west"]),
    "3a_10-c_south-west": PreRegion("3a_10-c_south-west", "3a_10-c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_10-c_south-west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_10-c_south-west"]),

    "3a_11-c_west": PreRegion("3a_11-c_west", "3a_11-c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_11-c_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_11-c_west"]),
    "3a_11-c_east": PreRegion("3a_11-c_east", "3a_11-c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_11-c_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_11-c_east"]),
    "3a_11-c_south-east": PreRegion("3a_11-c_south-east", "3a_11-c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_11-c_south-east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_11-c_south-east"]),
    "3a_11-c_south-west": PreRegion("3a_11-c_south-west", "3a_11-c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_11-c_south-west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_11-c_south-west"]),

    "3a_12-c_west": PreRegion("3a_12-c_west", "3a_12-c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_12-c_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_12-c_west"]),
    "3a_12-c_top": PreRegion("3a_12-c_top", "3a_12-c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_12-c_top"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_12-c_top"]),

    "3a_12-d_bottom": PreRegion("3a_12-d_bottom", "3a_12-d", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_12-d_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_12-d_bottom"]),
    "3a_12-d_top": PreRegion("3a_12-d_top", "3a_12-d", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_12-d_top"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_12-d_top"]),

    "3a_11-d_west": PreRegion("3a_11-d_west", "3a_11-d", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_11-d_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_11-d_west"]),
    "3a_11-d_east": PreRegion("3a_11-d_east", "3a_11-d", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_11-d_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_11-d_east"]),

    "3a_10-d_west": PreRegion("3a_10-d_west", "3a_10-d", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_10-d_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_10-d_west"]),
    "3a_10-d_main": PreRegion("3a_10-d_main", "3a_10-d", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_10-d_main"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_10-d_main"]),
    "3a_10-d_east": PreRegion("3a_10-d_east", "3a_10-d", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_10-d_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_10-d_east"]),

    "3a_11-b_west": PreRegion("3a_11-b_west", "3a_11-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_11-b_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_11-b_west"]),
    "3a_11-b_north-west": PreRegion("3a_11-b_north-west", "3a_11-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_11-b_north-west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_11-b_north-west"]),
    "3a_11-b_east": PreRegion("3a_11-b_east", "3a_11-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_11-b_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_11-b_east"]),
    "3a_11-b_north-east": PreRegion("3a_11-b_north-east", "3a_11-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_11-b_north-east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_11-b_north-east"]),

    "3a_12-b_west": PreRegion("3a_12-b_west", "3a_12-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_12-b_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_12-b_west"]),
    "3a_12-b_east": PreRegion("3a_12-b_east", "3a_12-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_12-b_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_12-b_east"]),

    "3a_13-b_top": PreRegion("3a_13-b_top", "3a_13-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_13-b_top"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_13-b_top"]),
    "3a_13-b_bottom": PreRegion("3a_13-b_bottom", "3a_13-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_13-b_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_13-b_bottom"]),

    "3a_13-a_west": PreRegion("3a_13-a_west", "3a_13-a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_13-a_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_13-a_west"]),
    "3a_13-a_south-west": PreRegion("3a_13-a_south-west", "3a_13-a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_13-a_south-west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_13-a_south-west"]),
    "3a_13-a_east": PreRegion("3a_13-a_east", "3a_13-a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_13-a_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_13-a_east"]),

    "3a_13-x_west": PreRegion("3a_13-x_west", "3a_13-x", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_13-x_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_13-x_west"]),
    "3a_13-x_east": PreRegion("3a_13-x_east", "3a_13-x", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_13-x_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_13-x_east"]),

    "3a_12-x_west": PreRegion("3a_12-x_west", "3a_12-x", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_12-x_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_12-x_west"]),
    "3a_12-x_north-east": PreRegion("3a_12-x_north-east", "3a_12-x", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_12-x_north-east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_12-x_north-east"]),
    "3a_12-x_east": PreRegion("3a_12-x_east", "3a_12-x", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_12-x_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_12-x_east"]),

    "3a_11-a_west": PreRegion("3a_11-a_west", "3a_11-a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_11-a_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_11-a_west"]),
    "3a_11-a_south": PreRegion("3a_11-a_south", "3a_11-a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_11-a_south"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_11-a_south"]),
    "3a_11-a_south-east-bottom": PreRegion("3a_11-a_south-east-bottom", "3a_11-a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_11-a_south-east-bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_11-a_south-east-bottom"]),
    "3a_11-a_south-east-right": PreRegion("3a_11-a_south-east-right", "3a_11-a", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_11-a_south-east-right"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_11-a_south-east-right"]),

    "3a_08-x_west": PreRegion("3a_08-x_west", "3a_08-x", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_08-x_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_08-x_west"]),
    "3a_08-x_east": PreRegion("3a_08-x_east", "3a_08-x", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_08-x_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_08-x_east"]),

    "3a_09-d_bottom": PreRegion("3a_09-d_bottom", "3a_09-d", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_09-d_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_09-d_bottom"]),
    "3a_09-d_top": PreRegion("3a_09-d_top", "3a_09-d", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_09-d_top"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_09-d_top"]),

    "3a_08-d_west": PreRegion("3a_08-d_west", "3a_08-d", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_08-d_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_08-d_west"]),
    "3a_08-d_east": PreRegion("3a_08-d_east", "3a_08-d", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_08-d_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_08-d_east"]),

    "3a_06-d_west": PreRegion("3a_06-d_west", "3a_06-d", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_06-d_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_06-d_west"]),
    "3a_06-d_east": PreRegion("3a_06-d_east", "3a_06-d", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_06-d_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_06-d_east"]),

    "3a_04-d_west": PreRegion("3a_04-d_west", "3a_04-d", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_04-d_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_04-d_west"]),
    "3a_04-d_south-west": PreRegion("3a_04-d_south-west", "3a_04-d", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_04-d_south-west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_04-d_south-west"]),
    "3a_04-d_south": PreRegion("3a_04-d_south", "3a_04-d", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_04-d_south"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_04-d_south"]),
    "3a_04-d_east": PreRegion("3a_04-d_east", "3a_04-d", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_04-d_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_04-d_east"]),

    "3a_04-c_west": PreRegion("3a_04-c_west", "3a_04-c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_04-c_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_04-c_west"]),
    "3a_04-c_north-west": PreRegion("3a_04-c_north-west", "3a_04-c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_04-c_north-west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_04-c_north-west"]),
    "3a_04-c_east": PreRegion("3a_04-c_east", "3a_04-c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_04-c_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_04-c_east"]),

    "3a_02-c_west": PreRegion("3a_02-c_west", "3a_02-c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_02-c_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_02-c_west"]),
    "3a_02-c_east": PreRegion("3a_02-c_east", "3a_02-c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_02-c_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_02-c_east"]),
    "3a_02-c_south-east": PreRegion("3a_02-c_south-east", "3a_02-c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_02-c_south-east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_02-c_south-east"]),

    "3a_03-b_west": PreRegion("3a_03-b_west", "3a_03-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_03-b_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_03-b_west"]),
    "3a_03-b_east": PreRegion("3a_03-b_east", "3a_03-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_03-b_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_03-b_east"]),
    "3a_03-b_north": PreRegion("3a_03-b_north", "3a_03-b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_03-b_north"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_03-b_north"]),

    "3a_01-c_west": PreRegion("3a_01-c_west", "3a_01-c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_01-c_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_01-c_west"]),
    "3a_01-c_east": PreRegion("3a_01-c_east", "3a_01-c", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_01-c_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_01-c_east"]),

    "3a_02-d_west": PreRegion("3a_02-d_west", "3a_02-d", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_02-d_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_02-d_west"]),
    "3a_02-d_east": PreRegion("3a_02-d_east", "3a_02-d", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_02-d_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_02-d_east"]),

    "3a_00-d_west": PreRegion("3a_00-d_west", "3a_00-d", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_00-d_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_00-d_west"]),
    "3a_00-d_east": PreRegion("3a_00-d_east", "3a_00-d", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_00-d_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_00-d_east"]),

    "3a_roof00_west": PreRegion("3a_roof00_west", "3a_roof00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_roof00_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_roof00_west"]),
    "3a_roof00_east": PreRegion("3a_roof00_east", "3a_roof00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_roof00_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_roof00_east"]),

    "3a_roof01_west": PreRegion("3a_roof01_west", "3a_roof01", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_roof01_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_roof01_west"]),
    "3a_roof01_east": PreRegion("3a_roof01_east", "3a_roof01", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_roof01_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_roof01_east"]),

    "3a_roof02_west": PreRegion("3a_roof02_west", "3a_roof02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_roof02_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_roof02_west"]),
    "3a_roof02_east": PreRegion("3a_roof02_east", "3a_roof02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_roof02_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_roof02_east"]),

    "3a_roof03_west": PreRegion("3a_roof03_west", "3a_roof03", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_roof03_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_roof03_west"]),
    "3a_roof03_east": PreRegion("3a_roof03_east", "3a_roof03", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_roof03_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_roof03_east"]),

    "3a_roof04_west": PreRegion("3a_roof04_west", "3a_roof04", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_roof04_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_roof04_west"]),
    "3a_roof04_east": PreRegion("3a_roof04_east", "3a_roof04", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_roof04_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_roof04_east"]),

    "3a_roof05_west": PreRegion("3a_roof05_west", "3a_roof05", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_roof05_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_roof05_west"]),
    "3a_roof05_east": PreRegion("3a_roof05_east", "3a_roof05", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_roof05_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_roof05_east"]),

    "3a_roof06b_west": PreRegion("3a_roof06b_west", "3a_roof06b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_roof06b_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_roof06b_west"]),
    "3a_roof06b_east": PreRegion("3a_roof06b_east", "3a_roof06b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_roof06b_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_roof06b_east"]),

    "3a_roof06_west": PreRegion("3a_roof06_west", "3a_roof06", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_roof06_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_roof06_west"]),
    "3a_roof06_east": PreRegion("3a_roof06_east", "3a_roof06", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_roof06_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_roof06_east"]),

    "3a_roof07_west": PreRegion("3a_roof07_west", "3a_roof07", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_roof07_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_roof07_west"]),
    "3a_roof07_main": PreRegion("3a_roof07_main", "3a_roof07", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3a_roof07_main"], [loc for _, loc in all_locations.items() if loc.region_name == "3a_roof07_main"]),

    "3b_00_west": PreRegion("3b_00_west", "3b_00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_00_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_00_west"]),
    "3b_00_east": PreRegion("3b_00_east", "3b_00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_00_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_00_east"]),

    "3b_back_east": PreRegion("3b_back_east", "3b_back", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_back_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_back_east"]),

    "3b_01_west": PreRegion("3b_01_west", "3b_01", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_01_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_01_west"]),
    "3b_01_east": PreRegion("3b_01_east", "3b_01", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_01_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_01_east"]),

    "3b_02_west": PreRegion("3b_02_west", "3b_02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_02_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_02_west"]),
    "3b_02_east": PreRegion("3b_02_east", "3b_02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_02_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_02_east"]),

    "3b_03_west": PreRegion("3b_03_west", "3b_03", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_03_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_03_west"]),
    "3b_03_east": PreRegion("3b_03_east", "3b_03", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_03_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_03_east"]),

    "3b_04_west": PreRegion("3b_04_west", "3b_04", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_04_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_04_west"]),
    "3b_04_east": PreRegion("3b_04_east", "3b_04", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_04_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_04_east"]),

    "3b_05_west": PreRegion("3b_05_west", "3b_05", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_05_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_05_west"]),
    "3b_05_east": PreRegion("3b_05_east", "3b_05", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_05_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_05_east"]),

    "3b_06_west": PreRegion("3b_06_west", "3b_06", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_06_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_06_west"]),
    "3b_06_east": PreRegion("3b_06_east", "3b_06", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_06_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_06_east"]),

    "3b_07_west": PreRegion("3b_07_west", "3b_07", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_07_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_07_west"]),
    "3b_07_east": PreRegion("3b_07_east", "3b_07", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_07_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_07_east"]),

    "3b_08_bottom": PreRegion("3b_08_bottom", "3b_08", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_08_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_08_bottom"]),
    "3b_08_top": PreRegion("3b_08_top", "3b_08", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_08_top"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_08_top"]),

    "3b_09_west": PreRegion("3b_09_west", "3b_09", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_09_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_09_west"]),
    "3b_09_east": PreRegion("3b_09_east", "3b_09", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_09_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_09_east"]),

    "3b_10_west": PreRegion("3b_10_west", "3b_10", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_10_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_10_west"]),
    "3b_10_east": PreRegion("3b_10_east", "3b_10", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_10_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_10_east"]),

    "3b_11_west": PreRegion("3b_11_west", "3b_11", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_11_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_11_west"]),
    "3b_11_east": PreRegion("3b_11_east", "3b_11", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_11_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_11_east"]),

    "3b_13_west": PreRegion("3b_13_west", "3b_13", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_13_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_13_west"]),
    "3b_13_east": PreRegion("3b_13_east", "3b_13", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_13_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_13_east"]),

    "3b_14_west": PreRegion("3b_14_west", "3b_14", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_14_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_14_west"]),
    "3b_14_east": PreRegion("3b_14_east", "3b_14", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_14_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_14_east"]),

    "3b_15_west": PreRegion("3b_15_west", "3b_15", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_15_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_15_west"]),
    "3b_15_east": PreRegion("3b_15_east", "3b_15", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_15_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_15_east"]),

    "3b_12_west": PreRegion("3b_12_west", "3b_12", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_12_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_12_west"]),
    "3b_12_east": PreRegion("3b_12_east", "3b_12", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_12_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_12_east"]),

    "3b_16_west": PreRegion("3b_16_west", "3b_16", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_16_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_16_west"]),
    "3b_16_top": PreRegion("3b_16_top", "3b_16", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_16_top"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_16_top"]),

    "3b_17_west": PreRegion("3b_17_west", "3b_17", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_17_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_17_west"]),
    "3b_17_east": PreRegion("3b_17_east", "3b_17", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_17_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_17_east"]),

    "3b_18_west": PreRegion("3b_18_west", "3b_18", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_18_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_18_west"]),
    "3b_18_east": PreRegion("3b_18_east", "3b_18", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_18_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_18_east"]),

    "3b_19_west": PreRegion("3b_19_west", "3b_19", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_19_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_19_west"]),
    "3b_19_east": PreRegion("3b_19_east", "3b_19", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_19_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_19_east"]),

    "3b_21_west": PreRegion("3b_21_west", "3b_21", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_21_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_21_west"]),
    "3b_21_east": PreRegion("3b_21_east", "3b_21", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_21_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_21_east"]),

    "3b_20_west": PreRegion("3b_20_west", "3b_20", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_20_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_20_west"]),
    "3b_20_east": PreRegion("3b_20_east", "3b_20", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_20_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_20_east"]),

    "3b_end_west": PreRegion("3b_end_west", "3b_end", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_end_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_end_west"]),
    "3b_end_goal": PreRegion("3b_end_goal", "3b_end", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3b_end_goal"], [loc for _, loc in all_locations.items() if loc.region_name == "3b_end_goal"]),

    "3c_00_west": PreRegion("3c_00_west", "3c_00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3c_00_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3c_00_west"]),
    "3c_00_east": PreRegion("3c_00_east", "3c_00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3c_00_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3c_00_east"]),

    "3c_01_west": PreRegion("3c_01_west", "3c_01", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3c_01_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3c_01_west"]),
    "3c_01_east": PreRegion("3c_01_east", "3c_01", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3c_01_east"], [loc for _, loc in all_locations.items() if loc.region_name == "3c_01_east"]),

    "3c_02_west": PreRegion("3c_02_west", "3c_02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3c_02_west"], [loc for _, loc in all_locations.items() if loc.region_name == "3c_02_west"]),
    "3c_02_goal": PreRegion("3c_02_goal", "3c_02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "3c_02_goal"], [loc for _, loc in all_locations.items() if loc.region_name == "3c_02_goal"]),

    "4a_a-00_west": PreRegion("4a_a-00_west", "4a_a-00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_a-00_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_a-00_west"]),
    "4a_a-00_east": PreRegion("4a_a-00_east", "4a_a-00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_a-00_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_a-00_east"]),

    "4a_a-01_west": PreRegion("4a_a-01_west", "4a_a-01", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_a-01_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_a-01_west"]),
    "4a_a-01_east": PreRegion("4a_a-01_east", "4a_a-01", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_a-01_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_a-01_east"]),

    "4a_a-01x_west": PreRegion("4a_a-01x_west", "4a_a-01x", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_a-01x_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_a-01x_west"]),
    "4a_a-01x_east": PreRegion("4a_a-01x_east", "4a_a-01x", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_a-01x_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_a-01x_east"]),

    "4a_a-02_west": PreRegion("4a_a-02_west", "4a_a-02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_a-02_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_a-02_west"]),
    "4a_a-02_east": PreRegion("4a_a-02_east", "4a_a-02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_a-02_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_a-02_east"]),

    "4a_a-03_west": PreRegion("4a_a-03_west", "4a_a-03", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_a-03_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_a-03_west"]),
    "4a_a-03_east": PreRegion("4a_a-03_east", "4a_a-03", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_a-03_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_a-03_east"]),

    "4a_a-04_west": PreRegion("4a_a-04_west", "4a_a-04", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_a-04_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_a-04_west"]),
    "4a_a-04_east": PreRegion("4a_a-04_east", "4a_a-04", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_a-04_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_a-04_east"]),

    "4a_a-05_west": PreRegion("4a_a-05_west", "4a_a-05", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_a-05_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_a-05_west"]),
    "4a_a-05_east": PreRegion("4a_a-05_east", "4a_a-05", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_a-05_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_a-05_east"]),

    "4a_a-06_west": PreRegion("4a_a-06_west", "4a_a-06", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_a-06_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_a-06_west"]),
    "4a_a-06_east": PreRegion("4a_a-06_east", "4a_a-06", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_a-06_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_a-06_east"]),

    "4a_a-07_west": PreRegion("4a_a-07_west", "4a_a-07", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_a-07_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_a-07_west"]),
    "4a_a-07_east": PreRegion("4a_a-07_east", "4a_a-07", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_a-07_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_a-07_east"]),

    "4a_a-08_west": PreRegion("4a_a-08_west", "4a_a-08", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_a-08_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_a-08_west"]),
    "4a_a-08_north-west": PreRegion("4a_a-08_north-west", "4a_a-08", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_a-08_north-west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_a-08_north-west"]),
    "4a_a-08_east": PreRegion("4a_a-08_east", "4a_a-08", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_a-08_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_a-08_east"]),

    "4a_a-10_west": PreRegion("4a_a-10_west", "4a_a-10", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_a-10_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_a-10_west"]),
    "4a_a-10_east": PreRegion("4a_a-10_east", "4a_a-10", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_a-10_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_a-10_east"]),

    "4a_a-11_east": PreRegion("4a_a-11_east", "4a_a-11", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_a-11_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_a-11_east"]),

    "4a_a-09_bottom": PreRegion("4a_a-09_bottom", "4a_a-09", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_a-09_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_a-09_bottom"]),
    "4a_a-09_top": PreRegion("4a_a-09_top", "4a_a-09", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_a-09_top"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_a-09_top"]),

    "4a_b-00_south": PreRegion("4a_b-00_south", "4a_b-00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_b-00_south"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_b-00_south"]),
    "4a_b-00_south-east": PreRegion("4a_b-00_south-east", "4a_b-00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_b-00_south-east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_b-00_south-east"]),
    "4a_b-00_east": PreRegion("4a_b-00_east", "4a_b-00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_b-00_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_b-00_east"]),
    "4a_b-00_west": PreRegion("4a_b-00_west", "4a_b-00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_b-00_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_b-00_west"]),
    "4a_b-00_north-east": PreRegion("4a_b-00_north-east", "4a_b-00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_b-00_north-east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_b-00_north-east"]),
    "4a_b-00_north-west": PreRegion("4a_b-00_north-west", "4a_b-00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_b-00_north-west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_b-00_north-west"]),
    "4a_b-00_north": PreRegion("4a_b-00_north", "4a_b-00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_b-00_north"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_b-00_north"]),

    "4a_b-01_west": PreRegion("4a_b-01_west", "4a_b-01", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_b-01_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_b-01_west"]),

    "4a_b-04_west": PreRegion("4a_b-04_west", "4a_b-04", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_b-04_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_b-04_west"]),
    "4a_b-04_north-west": PreRegion("4a_b-04_north-west", "4a_b-04", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_b-04_north-west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_b-04_north-west"]),
    "4a_b-04_east": PreRegion("4a_b-04_east", "4a_b-04", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_b-04_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_b-04_east"]),

    "4a_b-06_west": PreRegion("4a_b-06_west", "4a_b-06", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_b-06_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_b-06_west"]),
    "4a_b-06_east": PreRegion("4a_b-06_east", "4a_b-06", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_b-06_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_b-06_east"]),

    "4a_b-07_west": PreRegion("4a_b-07_west", "4a_b-07", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_b-07_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_b-07_west"]),
    "4a_b-07_east": PreRegion("4a_b-07_east", "4a_b-07", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_b-07_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_b-07_east"]),

    "4a_b-03_west": PreRegion("4a_b-03_west", "4a_b-03", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_b-03_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_b-03_west"]),
    "4a_b-03_east": PreRegion("4a_b-03_east", "4a_b-03", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_b-03_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_b-03_east"]),

    "4a_b-02_south-west": PreRegion("4a_b-02_south-west", "4a_b-02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_b-02_south-west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_b-02_south-west"]),
    "4a_b-02_north-west": PreRegion("4a_b-02_north-west", "4a_b-02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_b-02_north-west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_b-02_north-west"]),
    "4a_b-02_north-east": PreRegion("4a_b-02_north-east", "4a_b-02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_b-02_north-east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_b-02_north-east"]),
    "4a_b-02_north": PreRegion("4a_b-02_north", "4a_b-02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_b-02_north"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_b-02_north"]),

    "4a_b-sec_west": PreRegion("4a_b-sec_west", "4a_b-sec", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_b-sec_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_b-sec_west"]),
    "4a_b-sec_east": PreRegion("4a_b-sec_east", "4a_b-sec", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_b-sec_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_b-sec_east"]),

    "4a_b-secb_west": PreRegion("4a_b-secb_west", "4a_b-secb", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_b-secb_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_b-secb_west"]),

    "4a_b-05_center": PreRegion("4a_b-05_center", "4a_b-05", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_b-05_center"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_b-05_center"]),
    "4a_b-05_west": PreRegion("4a_b-05_west", "4a_b-05", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_b-05_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_b-05_west"]),
    "4a_b-05_north-east": PreRegion("4a_b-05_north-east", "4a_b-05", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_b-05_north-east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_b-05_north-east"]),
    "4a_b-05_east": PreRegion("4a_b-05_east", "4a_b-05", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_b-05_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_b-05_east"]),

    "4a_b-08b_west": PreRegion("4a_b-08b_west", "4a_b-08b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_b-08b_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_b-08b_west"]),
    "4a_b-08b_east": PreRegion("4a_b-08b_east", "4a_b-08b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_b-08b_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_b-08b_east"]),

    "4a_b-08_west": PreRegion("4a_b-08_west", "4a_b-08", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_b-08_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_b-08_west"]),
    "4a_b-08_east": PreRegion("4a_b-08_east", "4a_b-08", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_b-08_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_b-08_east"]),

    "4a_c-00_west": PreRegion("4a_c-00_west", "4a_c-00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_c-00_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_c-00_west"]),
    "4a_c-00_east": PreRegion("4a_c-00_east", "4a_c-00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_c-00_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_c-00_east"]),
    "4a_c-00_north-west": PreRegion("4a_c-00_north-west", "4a_c-00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_c-00_north-west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_c-00_north-west"]),

    "4a_c-01_east": PreRegion("4a_c-01_east", "4a_c-01", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_c-01_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_c-01_east"]),

    "4a_c-02_west": PreRegion("4a_c-02_west", "4a_c-02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_c-02_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_c-02_west"]),
    "4a_c-02_east": PreRegion("4a_c-02_east", "4a_c-02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_c-02_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_c-02_east"]),

    "4a_c-04_west": PreRegion("4a_c-04_west", "4a_c-04", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_c-04_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_c-04_west"]),
    "4a_c-04_east": PreRegion("4a_c-04_east", "4a_c-04", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_c-04_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_c-04_east"]),

    "4a_c-05_west": PreRegion("4a_c-05_west", "4a_c-05", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_c-05_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_c-05_west"]),
    "4a_c-05_east": PreRegion("4a_c-05_east", "4a_c-05", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_c-05_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_c-05_east"]),

    "4a_c-06_bottom": PreRegion("4a_c-06_bottom", "4a_c-06", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_c-06_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_c-06_bottom"]),
    "4a_c-06_west": PreRegion("4a_c-06_west", "4a_c-06", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_c-06_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_c-06_west"]),
    "4a_c-06_top": PreRegion("4a_c-06_top", "4a_c-06", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_c-06_top"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_c-06_top"]),

    "4a_c-06b_east": PreRegion("4a_c-06b_east", "4a_c-06b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_c-06b_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_c-06b_east"]),

    "4a_c-09_west": PreRegion("4a_c-09_west", "4a_c-09", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_c-09_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_c-09_west"]),
    "4a_c-09_east": PreRegion("4a_c-09_east", "4a_c-09", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_c-09_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_c-09_east"]),

    "4a_c-07_west": PreRegion("4a_c-07_west", "4a_c-07", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_c-07_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_c-07_west"]),
    "4a_c-07_east": PreRegion("4a_c-07_east", "4a_c-07", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_c-07_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_c-07_east"]),

    "4a_c-08_bottom": PreRegion("4a_c-08_bottom", "4a_c-08", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_c-08_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_c-08_bottom"]),
    "4a_c-08_east": PreRegion("4a_c-08_east", "4a_c-08", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_c-08_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_c-08_east"]),
    "4a_c-08_top": PreRegion("4a_c-08_top", "4a_c-08", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_c-08_top"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_c-08_top"]),

    "4a_c-10_bottom": PreRegion("4a_c-10_bottom", "4a_c-10", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_c-10_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_c-10_bottom"]),
    "4a_c-10_top": PreRegion("4a_c-10_top", "4a_c-10", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_c-10_top"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_c-10_top"]),

    "4a_d-00_west": PreRegion("4a_d-00_west", "4a_d-00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_d-00_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_d-00_west"]),
    "4a_d-00_south": PreRegion("4a_d-00_south", "4a_d-00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_d-00_south"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_d-00_south"]),
    "4a_d-00_east": PreRegion("4a_d-00_east", "4a_d-00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_d-00_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_d-00_east"]),
    "4a_d-00_north-west": PreRegion("4a_d-00_north-west", "4a_d-00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_d-00_north-west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_d-00_north-west"]),

    "4a_d-00b_east": PreRegion("4a_d-00b_east", "4a_d-00b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_d-00b_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_d-00b_east"]),

    "4a_d-01_west": PreRegion("4a_d-01_west", "4a_d-01", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_d-01_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_d-01_west"]),
    "4a_d-01_east": PreRegion("4a_d-01_east", "4a_d-01", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_d-01_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_d-01_east"]),

    "4a_d-02_west": PreRegion("4a_d-02_west", "4a_d-02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_d-02_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_d-02_west"]),
    "4a_d-02_east": PreRegion("4a_d-02_east", "4a_d-02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_d-02_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_d-02_east"]),

    "4a_d-03_west": PreRegion("4a_d-03_west", "4a_d-03", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_d-03_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_d-03_west"]),
    "4a_d-03_east": PreRegion("4a_d-03_east", "4a_d-03", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_d-03_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_d-03_east"]),

    "4a_d-04_west": PreRegion("4a_d-04_west", "4a_d-04", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_d-04_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_d-04_west"]),
    "4a_d-04_east": PreRegion("4a_d-04_east", "4a_d-04", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_d-04_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_d-04_east"]),

    "4a_d-05_west": PreRegion("4a_d-05_west", "4a_d-05", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_d-05_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_d-05_west"]),
    "4a_d-05_east": PreRegion("4a_d-05_east", "4a_d-05", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_d-05_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_d-05_east"]),

    "4a_d-06_west": PreRegion("4a_d-06_west", "4a_d-06", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_d-06_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_d-06_west"]),
    "4a_d-06_east": PreRegion("4a_d-06_east", "4a_d-06", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_d-06_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_d-06_east"]),

    "4a_d-07_west": PreRegion("4a_d-07_west", "4a_d-07", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_d-07_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_d-07_west"]),
    "4a_d-07_east": PreRegion("4a_d-07_east", "4a_d-07", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_d-07_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_d-07_east"]),

    "4a_d-08_west": PreRegion("4a_d-08_west", "4a_d-08", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_d-08_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_d-08_west"]),
    "4a_d-08_east": PreRegion("4a_d-08_east", "4a_d-08", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_d-08_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_d-08_east"]),

    "4a_d-09_west": PreRegion("4a_d-09_west", "4a_d-09", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_d-09_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_d-09_west"]),
    "4a_d-09_east": PreRegion("4a_d-09_east", "4a_d-09", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_d-09_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_d-09_east"]),

    "4a_d-10_west": PreRegion("4a_d-10_west", "4a_d-10", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_d-10_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_d-10_west"]),
    "4a_d-10_goal": PreRegion("4a_d-10_goal", "4a_d-10", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4a_d-10_goal"], [loc for _, loc in all_locations.items() if loc.region_name == "4a_d-10_goal"]),

    "4b_a-00_west": PreRegion("4b_a-00_west", "4b_a-00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_a-00_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_a-00_west"]),
    "4b_a-00_east": PreRegion("4b_a-00_east", "4b_a-00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_a-00_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_a-00_east"]),

    "4b_a-01_west": PreRegion("4b_a-01_west", "4b_a-01", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_a-01_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_a-01_west"]),
    "4b_a-01_east": PreRegion("4b_a-01_east", "4b_a-01", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_a-01_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_a-01_east"]),

    "4b_a-02_west": PreRegion("4b_a-02_west", "4b_a-02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_a-02_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_a-02_west"]),
    "4b_a-02_east": PreRegion("4b_a-02_east", "4b_a-02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_a-02_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_a-02_east"]),

    "4b_a-03_west": PreRegion("4b_a-03_west", "4b_a-03", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_a-03_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_a-03_west"]),
    "4b_a-03_east": PreRegion("4b_a-03_east", "4b_a-03", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_a-03_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_a-03_east"]),

    "4b_a-04_west": PreRegion("4b_a-04_west", "4b_a-04", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_a-04_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_a-04_west"]),
    "4b_a-04_east": PreRegion("4b_a-04_east", "4b_a-04", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_a-04_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_a-04_east"]),

    "4b_b-00_west": PreRegion("4b_b-00_west", "4b_b-00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_b-00_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_b-00_west"]),
    "4b_b-00_east": PreRegion("4b_b-00_east", "4b_b-00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_b-00_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_b-00_east"]),

    "4b_b-01_west": PreRegion("4b_b-01_west", "4b_b-01", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_b-01_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_b-01_west"]),
    "4b_b-01_east": PreRegion("4b_b-01_east", "4b_b-01", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_b-01_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_b-01_east"]),

    "4b_b-02_bottom": PreRegion("4b_b-02_bottom", "4b_b-02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_b-02_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_b-02_bottom"]),
    "4b_b-02_top": PreRegion("4b_b-02_top", "4b_b-02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_b-02_top"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_b-02_top"]),

    "4b_b-03_west": PreRegion("4b_b-03_west", "4b_b-03", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_b-03_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_b-03_west"]),
    "4b_b-03_east": PreRegion("4b_b-03_east", "4b_b-03", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_b-03_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_b-03_east"]),

    "4b_b-04_west": PreRegion("4b_b-04_west", "4b_b-04", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_b-04_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_b-04_west"]),
    "4b_b-04_east": PreRegion("4b_b-04_east", "4b_b-04", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_b-04_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_b-04_east"]),

    "4b_c-00_west": PreRegion("4b_c-00_west", "4b_c-00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_c-00_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_c-00_west"]),
    "4b_c-00_east": PreRegion("4b_c-00_east", "4b_c-00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_c-00_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_c-00_east"]),

    "4b_c-01_west": PreRegion("4b_c-01_west", "4b_c-01", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_c-01_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_c-01_west"]),
    "4b_c-01_east": PreRegion("4b_c-01_east", "4b_c-01", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_c-01_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_c-01_east"]),

    "4b_c-02_west": PreRegion("4b_c-02_west", "4b_c-02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_c-02_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_c-02_west"]),
    "4b_c-02_east": PreRegion("4b_c-02_east", "4b_c-02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_c-02_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_c-02_east"]),

    "4b_c-03_bottom": PreRegion("4b_c-03_bottom", "4b_c-03", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_c-03_bottom"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_c-03_bottom"]),
    "4b_c-03_top": PreRegion("4b_c-03_top", "4b_c-03", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_c-03_top"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_c-03_top"]),

    "4b_c-04_west": PreRegion("4b_c-04_west", "4b_c-04", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_c-04_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_c-04_west"]),
    "4b_c-04_east": PreRegion("4b_c-04_east", "4b_c-04", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_c-04_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_c-04_east"]),

    "4b_d-00_west": PreRegion("4b_d-00_west", "4b_d-00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_d-00_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_d-00_west"]),
    "4b_d-00_east": PreRegion("4b_d-00_east", "4b_d-00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_d-00_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_d-00_east"]),

    "4b_d-01_west": PreRegion("4b_d-01_west", "4b_d-01", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_d-01_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_d-01_west"]),
    "4b_d-01_east": PreRegion("4b_d-01_east", "4b_d-01", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_d-01_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_d-01_east"]),

    "4b_d-02_west": PreRegion("4b_d-02_west", "4b_d-02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_d-02_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_d-02_west"]),
    "4b_d-02_east": PreRegion("4b_d-02_east", "4b_d-02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_d-02_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_d-02_east"]),

    "4b_d-03_west": PreRegion("4b_d-03_west", "4b_d-03", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_d-03_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_d-03_west"]),
    "4b_d-03_east": PreRegion("4b_d-03_east", "4b_d-03", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_d-03_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_d-03_east"]),

    "4b_end_west": PreRegion("4b_end_west", "4b_end", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_end_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_end_west"]),
    "4b_end_goal": PreRegion("4b_end_goal", "4b_end", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4b_end_goal"], [loc for _, loc in all_locations.items() if loc.region_name == "4b_end_goal"]),

    "4c_00_west": PreRegion("4c_00_west", "4c_00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4c_00_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4c_00_west"]),
    "4c_00_east": PreRegion("4c_00_east", "4c_00", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4c_00_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4c_00_east"]),

    "4c_01_west": PreRegion("4c_01_west", "4c_01", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4c_01_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4c_01_west"]),
    "4c_01_east": PreRegion("4c_01_east", "4c_01", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4c_01_east"], [loc for _, loc in all_locations.items() if loc.region_name == "4c_01_east"]),

    "4c_02_west": PreRegion("4c_02_west", "4c_02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4c_02_west"], [loc for _, loc in all_locations.items() if loc.region_name == "4c_02_west"]),
    "4c_02_goal": PreRegion("4c_02_goal", "4c_02", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "4c_02_goal"], [loc for _, loc in all_locations.items() if loc.region_name == "4c_02_goal"]),

}

all_room_connections: Dict[str, RoomConnection] = {
    "0a_-1_east---0a_0_west": RoomConnection("0a", all_doors["0a_-1_east"], all_doors["0a_0_west"]),
    "0a_0_north---0a_0b_south": RoomConnection("0a", all_doors["0a_0_north"], all_doors["0a_0b_south"]),
    "0a_0_east---0a_1_west": RoomConnection("0a", all_doors["0a_0_east"], all_doors["0a_1_west"]),
    "0a_1_east---0a_2_west": RoomConnection("0a", all_doors["0a_1_east"], all_doors["0a_2_west"]),
    "0a_2_east---0a_3_west": RoomConnection("0a", all_doors["0a_2_east"], all_doors["0a_3_west"]),

    "1a_1_east---1a_2_west": RoomConnection("1a", all_doors["1a_1_east"], all_doors["1a_2_west"]),
    "1a_2_east---1a_3_west": RoomConnection("1a", all_doors["1a_2_east"], all_doors["1a_3_west"]),
    "1a_3_east---1a_4_west": RoomConnection("1a", all_doors["1a_3_east"], all_doors["1a_4_west"]),
    "1a_4_east---1a_3b_west": RoomConnection("1a", all_doors["1a_4_east"], all_doors["1a_3b_west"]),
    "1a_3b_top---1a_5_bottom": RoomConnection("1a", all_doors["1a_3b_top"], all_doors["1a_5_bottom"]),
    "1a_5_west---1a_5z_east": RoomConnection("1a", all_doors["1a_5_west"], all_doors["1a_5z_east"]),
    "1a_5_south-east---1a_5a_west": RoomConnection("1a", all_doors["1a_5_south-east"], all_doors["1a_5a_west"]),
    "1a_5_top---1a_6_south-west": RoomConnection("1a", all_doors["1a_5_top"], all_doors["1a_6_south-west"]),
    "1a_6_west---1a_6z_east": RoomConnection("1a", all_doors["1a_6_west"], all_doors["1a_6z_east"]),
    "1a_6_east---1a_6a_west": RoomConnection("1a", all_doors["1a_6_east"], all_doors["1a_6a_west"]),
    "1a_6z_north-west---1a_7zb_east": RoomConnection("1a", all_doors["1a_6z_north-west"], all_doors["1a_7zb_east"]),
    "1a_6z_west---1a_6zb_east": RoomConnection("1a", all_doors["1a_6z_west"], all_doors["1a_6zb_east"]),
    "1a_7zb_west---1a_6zb_north-west": RoomConnection("1a", all_doors["1a_7zb_west"], all_doors["1a_6zb_north-west"]),
    "1a_6a_east---1a_6b_south-west": RoomConnection("1a", all_doors["1a_6a_east"], all_doors["1a_6b_south-west"]),
    "1a_6b_north-west---1a_s0_east": RoomConnection("1a", all_doors["1a_6b_north-west"], all_doors["1a_s0_east"]),
    "1a_6b_north-east---1a_6c_south-west": RoomConnection("1a", all_doors["1a_6b_north-east"], all_doors["1a_6c_south-west"]),
    "1a_s0_west---1a_s1_east": RoomConnection("1a", all_doors["1a_s0_west"], all_doors["1a_s1_east"]),
    "1a_6c_north-west---1a_7z_bottom": RoomConnection("1a", all_doors["1a_6c_north-west"], all_doors["1a_7z_bottom"]),
    "1a_6c_north-east---1a_7_west": RoomConnection("1a", all_doors["1a_6c_north-east"], all_doors["1a_7_west"]),
    "1a_7_east---1a_8_south-west": RoomConnection("1a", all_doors["1a_7_east"], all_doors["1a_8_south-west"]),
    "1a_7z_top---1a_8z_bottom": RoomConnection("1a", all_doors["1a_7z_top"], all_doors["1a_8z_bottom"]),
    "1a_8z_top---1a_8zb_west": RoomConnection("1a", all_doors["1a_8z_top"], all_doors["1a_8zb_west"]),
    "1a_8zb_east---1a_8_west": RoomConnection("1a", all_doors["1a_8zb_east"], all_doors["1a_8_west"]),
    "1a_8_south---1a_7a_west": RoomConnection("1a", all_doors["1a_8_south"], all_doors["1a_7a_west"]),
    "1a_8_north---1a_9z_east": RoomConnection("1a", all_doors["1a_8_north"], all_doors["1a_9z_east"]),
    "1a_8_north-east---1a_8b_west": RoomConnection("1a", all_doors["1a_8_north-east"], all_doors["1a_8b_west"]),
    "1a_7a_east---1a_8_south-east": RoomConnection("1a", all_doors["1a_7a_east"], all_doors["1a_8_south-east"]),
    "1a_8b_east---1a_9_west": RoomConnection("1a", all_doors["1a_8b_east"], all_doors["1a_9_west"]),
    "1a_9_east---1a_9b_west": RoomConnection("1a", all_doors["1a_9_east"], all_doors["1a_9b_west"]),
    "1a_9b_north-west---1a_10_south-east": RoomConnection("1a", all_doors["1a_9b_north-west"], all_doors["1a_10_south-east"]),
    "1a_9b_north-east---1a_10a_bottom": RoomConnection("1a", all_doors["1a_9b_north-east"], all_doors["1a_10a_bottom"]),
    "1a_9b_east---1a_9c_west": RoomConnection("1a", all_doors["1a_9b_east"], all_doors["1a_9c_west"]),
    "1a_10_south-west---1a_10z_east": RoomConnection("1a", all_doors["1a_10_south-west"], all_doors["1a_10z_east"]),
    "1a_10_north-west---1a_11_south-west": RoomConnection("1a", all_doors["1a_10_north-west"], all_doors["1a_11_south-west"]),
    "1a_10z_west---1a_10zb_east": RoomConnection("1a", all_doors["1a_10z_west"], all_doors["1a_10zb_east"]),
    "1a_11_south---1a_10_north-east": RoomConnection("1a", all_doors["1a_11_south"], all_doors["1a_10_north-east"]),
    "1a_11_west---1a_11z_east": RoomConnection("1a", all_doors["1a_11_west"], all_doors["1a_11z_east"]),
    "1a_10a_top---1a_11_south-east": RoomConnection("1a", all_doors["1a_10a_top"], all_doors["1a_11_south-east"]),
    "1a_11_north---1a_12_south-west": RoomConnection("1a", all_doors["1a_11_north"], all_doors["1a_12_south-west"]),
    "1a_12_north-west---1a_12z_east": RoomConnection("1a", all_doors["1a_12_north-west"], all_doors["1a_12z_east"]),
    "1a_12_east---1a_12a_bottom": RoomConnection("1a", all_doors["1a_12_east"], all_doors["1a_12a_bottom"]),
    "1a_12a_top---1a_end_south": RoomConnection("1a", all_doors["1a_12a_top"], all_doors["1a_end_south"]),

    "1b_00_east---1b_01_west": RoomConnection("1b", all_doors["1b_00_east"], all_doors["1b_01_west"]),
    "1b_01_east---1b_02_west": RoomConnection("1b", all_doors["1b_01_east"], all_doors["1b_02_west"]),
    "1b_02_east---1b_02b_west": RoomConnection("1b", all_doors["1b_02_east"], all_doors["1b_02b_west"]),
    "1b_02b_east---1b_03_west": RoomConnection("1b", all_doors["1b_02b_east"], all_doors["1b_03_west"]),
    "1b_03_east---1b_04_west": RoomConnection("1b", all_doors["1b_03_east"], all_doors["1b_04_west"]),
    "1b_04_east---1b_05_west": RoomConnection("1b", all_doors["1b_04_east"], all_doors["1b_05_west"]),
    "1b_05_east---1b_05b_west": RoomConnection("1b", all_doors["1b_05_east"], all_doors["1b_05b_west"]),
    "1b_05b_east---1b_06_west": RoomConnection("1b", all_doors["1b_05b_east"], all_doors["1b_06_west"]),
    "1b_06_east---1b_07_bottom": RoomConnection("1b", all_doors["1b_06_east"], all_doors["1b_07_bottom"]),
    "1b_07_top---1b_08_west": RoomConnection("1b", all_doors["1b_07_top"], all_doors["1b_08_west"]),
    "1b_08_east---1b_08b_west": RoomConnection("1b", all_doors["1b_08_east"], all_doors["1b_08b_west"]),
    "1b_08b_east---1b_09_west": RoomConnection("1b", all_doors["1b_08b_east"], all_doors["1b_09_west"]),
    "1b_09_east---1b_10_west": RoomConnection("1b", all_doors["1b_09_east"], all_doors["1b_10_west"]),
    "1b_10_east---1b_11_bottom": RoomConnection("1b", all_doors["1b_10_east"], all_doors["1b_11_bottom"]),
    "1b_11_top---1b_end_west": RoomConnection("1b", all_doors["1b_11_top"], all_doors["1b_end_west"]),

    "1c_00_east---1c_01_west": RoomConnection("1c", all_doors["1c_00_east"], all_doors["1c_01_west"]),
    "1c_01_east---1c_02_west": RoomConnection("1c", all_doors["1c_01_east"], all_doors["1c_02_west"]),

    "2a_start_top---2a_s0_bottom": RoomConnection("2a", all_doors["2a_start_top"], all_doors["2a_s0_bottom"]),
    "2a_start_east---2a_0_south-west": RoomConnection("2a", all_doors["2a_start_east"], all_doors["2a_0_south-west"]),
    "2a_s0_top---2a_s1_bottom": RoomConnection("2a", all_doors["2a_s0_top"], all_doors["2a_s1_bottom"]),
    "2a_s1_top---2a_s2_bottom": RoomConnection("2a", all_doors["2a_s1_top"], all_doors["2a_s2_bottom"]),
    "2a_0_north-west---2a_3x_bottom": RoomConnection("2a", all_doors["2a_0_north-west"], all_doors["2a_3x_bottom"]),
    "2a_0_north-east---2a_1_north-west": RoomConnection("2a", all_doors["2a_0_north-east"], all_doors["2a_1_north-west"]),
    "2a_0_south-east---2a_1_south-west": RoomConnection("2a", all_doors["2a_0_south-east"], all_doors["2a_1_south-west"]),
    "2a_1_south---2a_d0_north": RoomConnection("2a", all_doors["2a_1_south"], all_doors["2a_d0_north"]),
    "2a_1_south-east---2a_2_south-west": RoomConnection("2a", all_doors["2a_1_south-east"], all_doors["2a_2_south-west"]),
    "2a_d0_north-west---2a_d1_north-east": RoomConnection("2a", all_doors["2a_d0_north-west"], all_doors["2a_d1_north-east"]),
    "2a_d0_west---2a_d1_south-east": RoomConnection("2a", all_doors["2a_d0_west"], all_doors["2a_d1_south-east"]),
    "2a_d0_south-west---2a_d6_east": RoomConnection("2a", all_doors["2a_d0_south-west"], all_doors["2a_d6_east"]),
    "2a_d0_south---2a_d9_north-west": RoomConnection("2a", all_doors["2a_d0_south"], all_doors["2a_d9_north-west"]),
    "2a_d0_south-east---2a_d7_west": RoomConnection("2a", all_doors["2a_d0_south-east"], all_doors["2a_d7_west"]),
    "2a_d0_east---2a_d2_west": RoomConnection("2a", all_doors["2a_d0_east"], all_doors["2a_d2_west"]),
    "2a_d0_north-east---2a_d4_west": RoomConnection("2a", all_doors["2a_d0_north-east"], all_doors["2a_d4_west"]),
    "2a_d1_south-west---2a_d6_west": RoomConnection("2a", all_doors["2a_d1_south-west"], all_doors["2a_d6_west"]),
    "2a_d7_east---2a_d8_west": RoomConnection("2a", all_doors["2a_d7_east"], all_doors["2a_d8_west"]),
    "2a_d2_east---2a_d3_north": RoomConnection("2a", all_doors["2a_d2_east"], all_doors["2a_d3_north"]),
    "2a_d4_east---2a_d5_west": RoomConnection("2a", all_doors["2a_d4_east"], all_doors["2a_d5_west"]),
    "2a_d4_south---2a_d2_north-west": RoomConnection("2a", all_doors["2a_d4_south"], all_doors["2a_d2_north-west"]),
    "2a_d8_north-east---2a_d3_west": RoomConnection("2a", all_doors["2a_d8_north-east"], all_doors["2a_d3_west"]),
    "2a_d8_south-east---2a_d3_south": RoomConnection("2a", all_doors["2a_d8_south-east"], all_doors["2a_d3_south"]),
    "2a_3x_top---2a_3_bottom": RoomConnection("2a", all_doors["2a_3x_top"], all_doors["2a_3_bottom"]),
    "2a_3_top---2a_4_bottom": RoomConnection("2a", all_doors["2a_3_top"], all_doors["2a_4_bottom"]),
    "2a_4_top---2a_5_bottom": RoomConnection("2a", all_doors["2a_4_top"], all_doors["2a_5_bottom"]),
    "2a_5_top---2a_6_bottom": RoomConnection("2a", all_doors["2a_5_top"], all_doors["2a_6_bottom"]),
    "2a_6_top---2a_7_bottom": RoomConnection("2a", all_doors["2a_6_top"], all_doors["2a_7_bottom"]),
    "2a_7_top---2a_8_bottom": RoomConnection("2a", all_doors["2a_7_top"], all_doors["2a_8_bottom"]),
    "2a_8_top---2a_9_west": RoomConnection("2a", all_doors["2a_8_top"], all_doors["2a_9_west"]),
    "2a_9_north---2a_9b_east": RoomConnection("2a", all_doors["2a_9_north"], all_doors["2a_9b_east"]),
    "2a_9_south-east---2a_10_top": RoomConnection("2a", all_doors["2a_9_south-east"], all_doors["2a_10_top"]),
    "2a_9b_west---2a_9_north-west": RoomConnection("2a", all_doors["2a_9b_west"], all_doors["2a_9_north-west"]),
    "2a_10_bottom---2a_2_north-west": RoomConnection("2a", all_doors["2a_10_bottom"], all_doors["2a_2_north-west"]),
    "2a_2_south-east---2a_11_west": RoomConnection("2a", all_doors["2a_2_south-east"], all_doors["2a_11_west"]),
    "2a_11_east---2a_12b_west": RoomConnection("2a", all_doors["2a_11_east"], all_doors["2a_12b_west"]),
    "2a_12b_north---2a_12c_south": RoomConnection("2a", all_doors["2a_12b_north"], all_doors["2a_12c_south"]),
    "2a_12b_south---2a_12d_north-west": RoomConnection("2a", all_doors["2a_12b_south"], all_doors["2a_12d_north-west"]),
    "2a_12b_east---2a_12_west": RoomConnection("2a", all_doors["2a_12b_east"], all_doors["2a_12_west"]),
    "2a_12d_north---2a_12b_south-east": RoomConnection("2a", all_doors["2a_12d_north"], all_doors["2a_12b_south-east"]),
    "2a_12_east---2a_13_west": RoomConnection("2a", all_doors["2a_12_east"], all_doors["2a_13_west"]),
    "2a_13_phone---2a_end_0_main": RoomConnection("2a", all_doors["2a_13_phone"], all_doors["2a_end_0_main"]),
    "2a_end_0_top---2a_end_s0_bottom": RoomConnection("2a", all_doors["2a_end_0_top"], all_doors["2a_end_s0_bottom"]),
    "2a_end_0_east---2a_end_1_west": RoomConnection("2a", all_doors["2a_end_0_east"], all_doors["2a_end_1_west"]),
    "2a_end_s0_top---2a_end_s1_bottom": RoomConnection("2a", all_doors["2a_end_s0_top"], all_doors["2a_end_s1_bottom"]),
    "2a_end_1_east---2a_end_2_west": RoomConnection("2a", all_doors["2a_end_1_east"], all_doors["2a_end_2_west"]),
    "2a_end_1_north-east---2a_end_2_north-west": RoomConnection("2a", all_doors["2a_end_1_north-east"], all_doors["2a_end_2_north-west"]),
    "2a_end_2_east---2a_end_3_west": RoomConnection("2a", all_doors["2a_end_2_east"], all_doors["2a_end_3_west"]),
    "2a_end_2_north-east---2a_end_3_north-west": RoomConnection("2a", all_doors["2a_end_2_north-east"], all_doors["2a_end_3_north-west"]),
    "2a_end_3_east---2a_end_4_west": RoomConnection("2a", all_doors["2a_end_3_east"], all_doors["2a_end_4_west"]),
    "2a_end_4_east---2a_end_3b_west": RoomConnection("2a", all_doors["2a_end_4_east"], all_doors["2a_end_3b_west"]),
    "2a_end_3b_north---2a_end_3cb_bottom": RoomConnection("2a", all_doors["2a_end_3b_north"], all_doors["2a_end_3cb_bottom"]),
    "2a_end_3b_east---2a_end_5_west": RoomConnection("2a", all_doors["2a_end_3b_east"], all_doors["2a_end_5_west"]),
    "2a_end_3cb_top---2a_end_3c_bottom": RoomConnection("2a", all_doors["2a_end_3cb_top"], all_doors["2a_end_3c_bottom"]),
    "2a_end_5_east---2a_end_6_west": RoomConnection("2a", all_doors["2a_end_5_east"], all_doors["2a_end_6_west"]),

    "2b_start_east---2b_00_west": RoomConnection("2b", all_doors["2b_start_east"], all_doors["2b_00_west"]),
    "2b_00_east---2b_01_west": RoomConnection("2b", all_doors["2b_00_east"], all_doors["2b_01_west"]),
    "2b_01_east---2b_01b_west": RoomConnection("2b", all_doors["2b_01_east"], all_doors["2b_01b_west"]),
    "2b_01b_east---2b_02b_west": RoomConnection("2b", all_doors["2b_01b_east"], all_doors["2b_02b_west"]),
    "2b_02b_east---2b_02_west": RoomConnection("2b", all_doors["2b_02b_east"], all_doors["2b_02_west"]),
    "2b_02_east---2b_03_west": RoomConnection("2b", all_doors["2b_02_east"], all_doors["2b_03_west"]),
    "2b_03_east---2b_04_bottom": RoomConnection("2b", all_doors["2b_03_east"], all_doors["2b_04_bottom"]),
    "2b_04_top---2b_05_bottom": RoomConnection("2b", all_doors["2b_04_top"], all_doors["2b_05_bottom"]),
    "2b_05_top---2b_06_west": RoomConnection("2b", all_doors["2b_05_top"], all_doors["2b_06_west"]),
    "2b_06_east---2b_07_bottom": RoomConnection("2b", all_doors["2b_06_east"], all_doors["2b_07_bottom"]),
    "2b_07_top---2b_08b_west": RoomConnection("2b", all_doors["2b_07_top"], all_doors["2b_08b_west"]),
    "2b_08b_east---2b_08_west": RoomConnection("2b", all_doors["2b_08b_east"], all_doors["2b_08_west"]),
    "2b_08_east---2b_09_west": RoomConnection("2b", all_doors["2b_08_east"], all_doors["2b_09_west"]),
    "2b_09_east---2b_10_west": RoomConnection("2b", all_doors["2b_09_east"], all_doors["2b_10_west"]),
    "2b_10_east---2b_11_bottom": RoomConnection("2b", all_doors["2b_10_east"], all_doors["2b_11_bottom"]),
    "2b_11_top---2b_end_west": RoomConnection("2b", all_doors["2b_11_top"], all_doors["2b_end_west"]),

    "2c_00_east---2c_01_west": RoomConnection("2c", all_doors["2c_00_east"], all_doors["2c_01_west"]),
    "2c_01_east---2c_02_west": RoomConnection("2c", all_doors["2c_01_east"], all_doors["2c_02_west"]),

    "3a_s0_east---3a_s1_west": RoomConnection("3a", all_doors["3a_s0_east"], all_doors["3a_s1_west"]),
    "3a_s1_east---3a_s2_west": RoomConnection("3a", all_doors["3a_s1_east"], all_doors["3a_s2_west"]),
    "3a_s1_north-east---3a_s2_north-west": RoomConnection("3a", all_doors["3a_s1_north-east"], all_doors["3a_s2_north-west"]),
    "3a_s2_east---3a_s3_west": RoomConnection("3a", all_doors["3a_s2_east"], all_doors["3a_s3_west"]),
    "3a_s3_east---3a_0x-a_west": RoomConnection("3a", all_doors["3a_s3_east"], all_doors["3a_0x-a_west"]),
    "3a_0x-a_east---3a_00-a_west": RoomConnection("3a", all_doors["3a_0x-a_east"], all_doors["3a_00-a_west"]),
    "3a_00-a_east---3a_02-a_west": RoomConnection("3a", all_doors["3a_00-a_east"], all_doors["3a_02-a_west"]),
    "3a_02-a_east---3a_03-a_west": RoomConnection("3a", all_doors["3a_02-a_east"], all_doors["3a_03-a_west"]),
    "3a_02-a_top---3a_02-b_east": RoomConnection("3a", all_doors["3a_02-a_top"], all_doors["3a_02-b_east"]),
    "3a_02-b_west---3a_01-b_east": RoomConnection("3a", all_doors["3a_02-b_west"], all_doors["3a_01-b_east"]),
    "3a_01-b_north-west---3a_00-b_east": RoomConnection("3a", all_doors["3a_01-b_north-west"], all_doors["3a_00-b_east"]),
    "3a_01-b_west---3a_00-b_south-east": RoomConnection("3a", all_doors["3a_01-b_west"], all_doors["3a_00-b_south-east"]),
    "3a_00-b_south-west---3a_0x-b_south-east": RoomConnection("3a", all_doors["3a_00-b_south-west"], all_doors["3a_0x-b_south-east"]),
    "3a_00-b_north---3a_00-c_south-east": RoomConnection("3a", all_doors["3a_00-b_north"], all_doors["3a_00-c_south-east"]),
    "3a_00-b_west---3a_0x-b_north-east": RoomConnection("3a", all_doors["3a_00-b_west"], all_doors["3a_0x-b_north-east"]),
    "3a_00-c_south-west---3a_00-b_north-west": RoomConnection("3a", all_doors["3a_00-c_south-west"], all_doors["3a_00-b_north-west"]),
    "3a_00-c_north-east---3a_01-c_west": RoomConnection("3a", all_doors["3a_00-c_north-east"], all_doors["3a_01-c_west"]),
    "3a_0x-b_west---3a_s3_north": RoomConnection("3a", all_doors["3a_0x-b_west"], all_doors["3a_s3_north"]),
    "3a_03-a_top---3a_04-b_east": RoomConnection("3a", all_doors["3a_03-a_top"], all_doors["3a_04-b_east"]),
    "3a_03-a_east---3a_05-a_west": RoomConnection("3a", all_doors["3a_03-a_east"], all_doors["3a_05-a_west"]),
    "3a_05-a_east---3a_06-a_west": RoomConnection("3a", all_doors["3a_05-a_east"], all_doors["3a_06-a_west"]),
    "3a_06-a_east---3a_07-a_west": RoomConnection("3a", all_doors["3a_06-a_east"], all_doors["3a_07-a_west"]),
    "3a_07-a_top---3a_07-b_bottom": RoomConnection("3a", all_doors["3a_07-a_top"], all_doors["3a_07-b_bottom"]),
    "3a_07-a_east---3a_08-a_west": RoomConnection("3a", all_doors["3a_07-a_east"], all_doors["3a_08-a_west"]),
    "3a_07-b_west---3a_06-b_east": RoomConnection("3a", all_doors["3a_07-b_west"], all_doors["3a_06-b_east"]),
    "3a_06-b_west---3a_06-c_south-west": RoomConnection("3a", all_doors["3a_06-b_west"], all_doors["3a_06-c_south-west"]),
    "3a_06-c_north-west---3a_05-c_east": RoomConnection("3a", all_doors["3a_06-c_north-west"], all_doors["3a_05-c_east"]),
    "3a_06-c_east---3a_08-c_west": RoomConnection("3a", all_doors["3a_06-c_east"], all_doors["3a_08-c_west"]),
    "3a_06-c_south-east---3a_07-b_top": RoomConnection("3a", all_doors["3a_06-c_south-east"], all_doors["3a_07-b_top"]),
    "3a_08-c_east---3a_08-b_east": RoomConnection("3a", all_doors["3a_08-c_east"], all_doors["3a_08-b_east"]),
    "3a_08-b_west---3a_07-b_east": RoomConnection("3a", all_doors["3a_08-b_west"], all_doors["3a_07-b_east"]),
    "3a_08-a_bottom---3a_08-x_west": RoomConnection("3a", all_doors["3a_08-a_bottom"], all_doors["3a_08-x_west"]),
    "3a_08-a_east---3a_09-b_west": RoomConnection("3a", all_doors["3a_08-a_east"], all_doors["3a_09-b_west"]),
    "3a_09-b_south-east---3a_10-x_north-east-top": RoomConnection("3a", all_doors["3a_09-b_south-east"], all_doors["3a_10-x_north-east-top"]),
    "3a_09-b_north-west---3a_09-d_bottom": RoomConnection("3a", all_doors["3a_09-b_north-west"], all_doors["3a_09-d_bottom"]),
    "3a_09-b_north-east-top---3a_10-c_south-east": RoomConnection("3a", all_doors["3a_09-b_north-east-top"], all_doors["3a_10-c_south-east"]),
    "3a_09-b_east---3a_11-a_west": RoomConnection("3a", all_doors["3a_09-b_east"], all_doors["3a_11-a_west"]),
    "3a_09-b_north-east-right---3a_11-b_west": RoomConnection("3a", all_doors["3a_09-b_north-east-right"], all_doors["3a_11-b_west"]),
    "3a_10-x_north-east-right---3a_11-x_west": RoomConnection("3a", all_doors["3a_10-x_north-east-right"], all_doors["3a_11-x_west"]),
    "3a_11-x_south---3a_11-y_west": RoomConnection("3a", all_doors["3a_11-x_south"], all_doors["3a_11-y_west"]),
    "3a_11-y_east---3a_12-y_west": RoomConnection("3a", all_doors["3a_11-y_east"], all_doors["3a_12-y_west"]),
    "3a_11-y_south---3a_11-z_east": RoomConnection("3a", all_doors["3a_11-y_south"], all_doors["3a_11-z_east"]),
    "3a_11-z_west---3a_10-z_bottom": RoomConnection("3a", all_doors["3a_11-z_west"], all_doors["3a_10-z_bottom"]),
    "3a_10-z_top---3a_10-y_bottom": RoomConnection("3a", all_doors["3a_10-z_top"], all_doors["3a_10-y_bottom"]),
    "3a_10-y_top---3a_10-x_south-east": RoomConnection("3a", all_doors["3a_10-y_top"], all_doors["3a_10-x_south-east"]),
    "3a_10-x_west---3a_09-b_south": RoomConnection("3a", all_doors["3a_10-x_west"], all_doors["3a_09-b_south"]),
    "3a_10-c_north-east---3a_11-c_west": RoomConnection("3a", all_doors["3a_10-c_north-east"], all_doors["3a_11-c_west"]),
    "3a_10-c_south-west---3a_09-b_north": RoomConnection("3a", all_doors["3a_10-c_south-west"], all_doors["3a_09-b_north"]),
    "3a_11-c_east---3a_12-c_west": RoomConnection("3a", all_doors["3a_11-c_east"], all_doors["3a_12-c_west"]),
    "3a_11-c_south-west---3a_11-b_north-west": RoomConnection("3a", all_doors["3a_11-c_south-west"], all_doors["3a_11-b_north-west"]),
    "3a_12-c_top---3a_12-d_bottom": RoomConnection("3a", all_doors["3a_12-c_top"], all_doors["3a_12-d_bottom"]),
    "3a_12-d_top---3a_11-d_east": RoomConnection("3a", all_doors["3a_12-d_top"], all_doors["3a_11-d_east"]),
    "3a_11-d_west---3a_10-d_east": RoomConnection("3a", all_doors["3a_11-d_west"], all_doors["3a_10-d_east"]),
    "3a_10-d_west---3a_10-c_north-west": RoomConnection("3a", all_doors["3a_10-d_west"], all_doors["3a_10-c_north-west"]),
    "3a_11-b_north-east---3a_11-c_south-east": RoomConnection("3a", all_doors["3a_11-b_north-east"], all_doors["3a_11-c_south-east"]),
    "3a_11-b_east---3a_12-b_west": RoomConnection("3a", all_doors["3a_11-b_east"], all_doors["3a_12-b_west"]),
    "3a_12-b_east---3a_13-b_top": RoomConnection("3a", all_doors["3a_12-b_east"], all_doors["3a_13-b_top"]),
    "3a_13-b_bottom---3a_13-a_west": RoomConnection("3a", all_doors["3a_13-b_bottom"], all_doors["3a_13-a_west"]),
    "3a_13-a_east---3a_13-x_east": RoomConnection("3a", all_doors["3a_13-a_east"], all_doors["3a_13-x_east"]),
    "3a_13-x_west---3a_12-x_east": RoomConnection("3a", all_doors["3a_13-x_west"], all_doors["3a_12-x_east"]),
    "3a_12-x_north-east---3a_11-a_south-east-bottom": RoomConnection("3a", all_doors["3a_12-x_north-east"], all_doors["3a_11-a_south-east-bottom"]),
    "3a_12-x_west---3a_11-a_south": RoomConnection("3a", all_doors["3a_12-x_west"], all_doors["3a_11-a_south"]),
    "3a_11-a_south-east-right---3a_13-a_south-west": RoomConnection("3a", all_doors["3a_11-a_south-east-right"], all_doors["3a_13-a_south-west"]),
    "3a_08-x_east---3a_09-b_south-west": RoomConnection("3a", all_doors["3a_08-x_east"], all_doors["3a_09-b_south-west"]),
    "3a_09-d_top---3a_08-d_east": RoomConnection("3a", all_doors["3a_09-d_top"], all_doors["3a_08-d_east"]),
    "3a_08-d_west---3a_06-d_east": RoomConnection("3a", all_doors["3a_08-d_west"], all_doors["3a_06-d_east"]),
    "3a_06-d_west---3a_04-d_east": RoomConnection("3a", all_doors["3a_06-d_west"], all_doors["3a_04-d_east"]),
    "3a_04-d_west---3a_02-d_east": RoomConnection("3a", all_doors["3a_04-d_west"], all_doors["3a_02-d_east"]),
    "3a_04-d_south---3a_04-c_east": RoomConnection("3a", all_doors["3a_04-d_south"], all_doors["3a_04-c_east"]),
    "3a_04-c_west---3a_02-c_east": RoomConnection("3a", all_doors["3a_04-c_west"], all_doors["3a_02-c_east"]),
    "3a_04-c_north-west---3a_04-d_south-west": RoomConnection("3a", all_doors["3a_04-c_north-west"], all_doors["3a_04-d_south-west"]),
    "3a_02-c_west---3a_01-c_east": RoomConnection("3a", all_doors["3a_02-c_west"], all_doors["3a_01-c_east"]),
    "3a_02-c_south-east---3a_03-b_north": RoomConnection("3a", all_doors["3a_02-c_south-east"], all_doors["3a_03-b_north"]),
    "3a_03-b_east---3a_04-b_west": RoomConnection("3a", all_doors["3a_03-b_east"], all_doors["3a_04-b_west"]),
    "3a_03-b_west---3a_02-b_far-east": RoomConnection("3a", all_doors["3a_03-b_west"], all_doors["3a_02-b_far-east"]),
    "3a_02-d_west---3a_00-d_east": RoomConnection("3a", all_doors["3a_02-d_west"], all_doors["3a_00-d_east"]),
    "3a_00-d_west---3a_roof00_west": RoomConnection("3a", all_doors["3a_00-d_west"], all_doors["3a_roof00_west"]),
    "3a_roof00_east---3a_roof01_west": RoomConnection("3a", all_doors["3a_roof00_east"], all_doors["3a_roof01_west"]),
    "3a_roof01_east---3a_roof02_west": RoomConnection("3a", all_doors["3a_roof01_east"], all_doors["3a_roof02_west"]),
    "3a_roof02_east---3a_roof03_west": RoomConnection("3a", all_doors["3a_roof02_east"], all_doors["3a_roof03_west"]),
    "3a_roof03_east---3a_roof04_west": RoomConnection("3a", all_doors["3a_roof03_east"], all_doors["3a_roof04_west"]),
    "3a_roof04_east---3a_roof05_west": RoomConnection("3a", all_doors["3a_roof04_east"], all_doors["3a_roof05_west"]),
    "3a_roof05_east---3a_roof06b_west": RoomConnection("3a", all_doors["3a_roof05_east"], all_doors["3a_roof06b_west"]),
    "3a_roof06b_east---3a_roof06_west": RoomConnection("3a", all_doors["3a_roof06b_east"], all_doors["3a_roof06_west"]),
    "3a_roof06_east---3a_roof07_west": RoomConnection("3a", all_doors["3a_roof06_east"], all_doors["3a_roof07_west"]),

    "3b_00_east---3b_01_west": RoomConnection("3b", all_doors["3b_00_east"], all_doors["3b_01_west"]),
    "3b_00_west---3b_back_east": RoomConnection("3b", all_doors["3b_00_west"], all_doors["3b_back_east"]),
    "3b_01_east---3b_02_west": RoomConnection("3b", all_doors["3b_01_east"], all_doors["3b_02_west"]),
    "3b_02_east---3b_03_west": RoomConnection("3b", all_doors["3b_02_east"], all_doors["3b_03_west"]),
    "3b_03_east---3b_04_west": RoomConnection("3b", all_doors["3b_03_east"], all_doors["3b_04_west"]),
    "3b_04_east---3b_05_west": RoomConnection("3b", all_doors["3b_04_east"], all_doors["3b_05_west"]),
    "3b_05_east---3b_06_west": RoomConnection("3b", all_doors["3b_05_east"], all_doors["3b_06_west"]),
    "3b_06_east---3b_07_west": RoomConnection("3b", all_doors["3b_06_east"], all_doors["3b_07_west"]),
    "3b_07_east---3b_08_bottom": RoomConnection("3b", all_doors["3b_07_east"], all_doors["3b_08_bottom"]),
    "3b_08_top---3b_09_west": RoomConnection("3b", all_doors["3b_08_top"], all_doors["3b_09_west"]),
    "3b_09_east---3b_10_west": RoomConnection("3b", all_doors["3b_09_east"], all_doors["3b_10_west"]),
    "3b_10_east---3b_11_west": RoomConnection("3b", all_doors["3b_10_east"], all_doors["3b_11_west"]),
    "3b_11_east---3b_13_west": RoomConnection("3b", all_doors["3b_11_east"], all_doors["3b_13_west"]),
    "3b_13_east---3b_14_west": RoomConnection("3b", all_doors["3b_13_east"], all_doors["3b_14_west"]),
    "3b_14_east---3b_15_west": RoomConnection("3b", all_doors["3b_14_east"], all_doors["3b_15_west"]),
    "3b_15_east---3b_12_west": RoomConnection("3b", all_doors["3b_15_east"], all_doors["3b_12_west"]),
    "3b_12_east---3b_16_west": RoomConnection("3b", all_doors["3b_12_east"], all_doors["3b_16_west"]),
    "3b_16_top---3b_17_west": RoomConnection("3b", all_doors["3b_16_top"], all_doors["3b_17_west"]),
    "3b_17_east---3b_18_west": RoomConnection("3b", all_doors["3b_17_east"], all_doors["3b_18_west"]),
    "3b_18_east---3b_19_west": RoomConnection("3b", all_doors["3b_18_east"], all_doors["3b_19_west"]),
    "3b_19_east---3b_21_west": RoomConnection("3b", all_doors["3b_19_east"], all_doors["3b_21_west"]),
    "3b_21_east---3b_20_west": RoomConnection("3b", all_doors["3b_21_east"], all_doors["3b_20_west"]),
    "3b_20_east---3b_end_west": RoomConnection("3b", all_doors["3b_20_east"], all_doors["3b_end_west"]),

    "3c_00_east---3c_01_west": RoomConnection("3c", all_doors["3c_00_east"], all_doors["3c_01_west"]),
    "3c_01_east---3c_02_west": RoomConnection("3c", all_doors["3c_01_east"], all_doors["3c_02_west"]),

    "4a_a-00_east---4a_a-01_west": RoomConnection("4a", all_doors["4a_a-00_east"], all_doors["4a_a-01_west"]),
    "4a_a-01_east---4a_a-01x_west": RoomConnection("4a", all_doors["4a_a-01_east"], all_doors["4a_a-01x_west"]),
    "4a_a-01x_east---4a_a-02_west": RoomConnection("4a", all_doors["4a_a-01x_east"], all_doors["4a_a-02_west"]),
    "4a_a-02_east---4a_a-03_west": RoomConnection("4a", all_doors["4a_a-02_east"], all_doors["4a_a-03_west"]),
    "4a_a-03_east---4a_a-04_west": RoomConnection("4a", all_doors["4a_a-03_east"], all_doors["4a_a-04_west"]),
    "4a_a-04_east---4a_a-05_west": RoomConnection("4a", all_doors["4a_a-04_east"], all_doors["4a_a-05_west"]),
    "4a_a-05_east---4a_a-06_west": RoomConnection("4a", all_doors["4a_a-05_east"], all_doors["4a_a-06_west"]),
    "4a_a-06_east---4a_a-07_west": RoomConnection("4a", all_doors["4a_a-06_east"], all_doors["4a_a-07_west"]),
    "4a_a-07_east---4a_a-08_west": RoomConnection("4a", all_doors["4a_a-07_east"], all_doors["4a_a-08_west"]),
    "4a_a-08_north-west---4a_a-10_east": RoomConnection("4a", all_doors["4a_a-08_north-west"], all_doors["4a_a-10_east"]),
    "4a_a-08_east---4a_a-09_bottom": RoomConnection("4a", all_doors["4a_a-08_east"], all_doors["4a_a-09_bottom"]),
    "4a_a-10_west---4a_a-11_east": RoomConnection("4a", all_doors["4a_a-10_west"], all_doors["4a_a-11_east"]),
    "4a_a-09_top---4a_b-00_south": RoomConnection("4a", all_doors["4a_a-09_top"], all_doors["4a_b-00_south"]),
    "4a_b-00_south-east---4a_b-01_west": RoomConnection("4a", all_doors["4a_b-00_south-east"], all_doors["4a_b-01_west"]),
    "4a_b-00_north-west---4a_b-04_east": RoomConnection("4a", all_doors["4a_b-00_north-west"], all_doors["4a_b-04_east"]),
    "4a_b-04_west---4a_b-06_east": RoomConnection("4a", all_doors["4a_b-04_west"], all_doors["4a_b-06_east"]),
    "4a_b-06_west---4a_b-07_west": RoomConnection("4a", all_doors["4a_b-06_west"], all_doors["4a_b-07_west"]),
    "4a_b-07_east---4a_b-03_west": RoomConnection("4a", all_doors["4a_b-07_east"], all_doors["4a_b-03_west"]),
    "4a_b-03_east---4a_b-00_west": RoomConnection("4a", all_doors["4a_b-03_east"], all_doors["4a_b-00_west"]),
    "4a_b-00_east---4a_b-02_south-west": RoomConnection("4a", all_doors["4a_b-00_east"], all_doors["4a_b-02_south-west"]),
    "4a_b-00_north-east---4a_b-02_north-west": RoomConnection("4a", all_doors["4a_b-00_north-east"], all_doors["4a_b-02_north-west"]),
    "4a_b-02_north-east---4a_b-sec_west": RoomConnection("4a", all_doors["4a_b-02_north-east"], all_doors["4a_b-sec_west"]),
    "4a_b-sec_east---4a_b-secb_west": RoomConnection("4a", all_doors["4a_b-sec_east"], all_doors["4a_b-secb_west"]),
    "4a_b-00_north---4a_b-05_center": RoomConnection("4a", all_doors["4a_b-00_north"], all_doors["4a_b-05_center"]),
    "4a_b-05_west---4a_b-04_north-west": RoomConnection("4a", all_doors["4a_b-05_west"], all_doors["4a_b-04_north-west"]),
    "4a_b-02_north---4a_b-05_east": RoomConnection("4a", all_doors["4a_b-02_north"], all_doors["4a_b-05_east"]),
    "4a_b-05_north-east---4a_b-08b_west": RoomConnection("4a", all_doors["4a_b-05_north-east"], all_doors["4a_b-08b_west"]),
    "4a_b-08b_east---4a_b-08_west": RoomConnection("4a", all_doors["4a_b-08b_east"], all_doors["4a_b-08_west"]),
    "4a_b-08_east---4a_c-00_west": RoomConnection("4a", all_doors["4a_b-08_east"], all_doors["4a_c-00_west"]),
    "4a_c-00_north-west---4a_c-01_east": RoomConnection("4a", all_doors["4a_c-00_north-west"], all_doors["4a_c-01_east"]),
    "4a_c-00_east---4a_c-02_west": RoomConnection("4a", all_doors["4a_c-00_east"], all_doors["4a_c-02_west"]),
    "4a_c-02_east---4a_c-04_west": RoomConnection("4a", all_doors["4a_c-02_east"], all_doors["4a_c-04_west"]),
    "4a_c-04_east---4a_c-05_west": RoomConnection("4a", all_doors["4a_c-04_east"], all_doors["4a_c-05_west"]),
    "4a_c-05_east---4a_c-06_bottom": RoomConnection("4a", all_doors["4a_c-05_east"], all_doors["4a_c-06_bottom"]),
    "4a_c-06_west---4a_c-06b_east": RoomConnection("4a", all_doors["4a_c-06_west"], all_doors["4a_c-06b_east"]),
    "4a_c-06_top---4a_c-09_west": RoomConnection("4a", all_doors["4a_c-06_top"], all_doors["4a_c-09_west"]),
    "4a_c-09_east---4a_c-07_west": RoomConnection("4a", all_doors["4a_c-09_east"], all_doors["4a_c-07_west"]),
    "4a_c-07_east---4a_c-08_bottom": RoomConnection("4a", all_doors["4a_c-07_east"], all_doors["4a_c-08_bottom"]),
    "4a_c-08_east---4a_c-10_bottom": RoomConnection("4a", all_doors["4a_c-08_east"], all_doors["4a_c-10_bottom"]),
    "4a_c-08_top---4a_d-00_west": RoomConnection("4a", all_doors["4a_c-08_top"], all_doors["4a_d-00_west"]),
    "4a_c-10_top---4a_d-00_south": RoomConnection("4a", all_doors["4a_c-10_top"], all_doors["4a_d-00_south"]),
    "4a_d-00_north-west---4a_d-00b_east": RoomConnection("4a", all_doors["4a_d-00_north-west"], all_doors["4a_d-00b_east"]),
    "4a_d-00_east---4a_d-01_west": RoomConnection("4a", all_doors["4a_d-00_east"], all_doors["4a_d-01_west"]),
    "4a_d-01_east---4a_d-02_west": RoomConnection("4a", all_doors["4a_d-01_east"], all_doors["4a_d-02_west"]),
    "4a_d-02_east---4a_d-03_west": RoomConnection("4a", all_doors["4a_d-02_east"], all_doors["4a_d-03_west"]),
    "4a_d-03_east---4a_d-04_west": RoomConnection("4a", all_doors["4a_d-03_east"], all_doors["4a_d-04_west"]),
    "4a_d-04_east---4a_d-05_west": RoomConnection("4a", all_doors["4a_d-04_east"], all_doors["4a_d-05_west"]),
    "4a_d-05_east---4a_d-06_west": RoomConnection("4a", all_doors["4a_d-05_east"], all_doors["4a_d-06_west"]),
    "4a_d-06_east---4a_d-07_west": RoomConnection("4a", all_doors["4a_d-06_east"], all_doors["4a_d-07_west"]),
    "4a_d-07_east---4a_d-08_west": RoomConnection("4a", all_doors["4a_d-07_east"], all_doors["4a_d-08_west"]),
    "4a_d-08_east---4a_d-09_west": RoomConnection("4a", all_doors["4a_d-08_east"], all_doors["4a_d-09_west"]),
    "4a_d-09_east---4a_d-10_west": RoomConnection("4a", all_doors["4a_d-09_east"], all_doors["4a_d-10_west"]),

    "4b_a-00_east---4b_a-01_west": RoomConnection("4b", all_doors["4b_a-00_east"], all_doors["4b_a-01_west"]),
    "4b_a-01_east---4b_a-02_west": RoomConnection("4b", all_doors["4b_a-01_east"], all_doors["4b_a-02_west"]),
    "4b_a-02_east---4b_a-03_west": RoomConnection("4b", all_doors["4b_a-02_east"], all_doors["4b_a-03_west"]),
    "4b_a-03_east---4b_a-04_west": RoomConnection("4b", all_doors["4b_a-03_east"], all_doors["4b_a-04_west"]),
    "4b_a-04_east---4b_b-00_west": RoomConnection("4b", all_doors["4b_a-04_east"], all_doors["4b_b-00_west"]),
    "4b_b-00_east---4b_b-01_west": RoomConnection("4b", all_doors["4b_b-00_east"], all_doors["4b_b-01_west"]),
    "4b_b-01_east---4b_b-02_bottom": RoomConnection("4b", all_doors["4b_b-01_east"], all_doors["4b_b-02_bottom"]),
    "4b_b-02_top---4b_b-03_west": RoomConnection("4b", all_doors["4b_b-02_top"], all_doors["4b_b-03_west"]),
    "4b_b-03_east---4b_b-04_west": RoomConnection("4b", all_doors["4b_b-03_east"], all_doors["4b_b-04_west"]),
    "4b_b-04_east---4b_c-00_west": RoomConnection("4b", all_doors["4b_b-04_east"], all_doors["4b_c-00_west"]),
    "4b_c-00_east---4b_c-01_west": RoomConnection("4b", all_doors["4b_c-00_east"], all_doors["4b_c-01_west"]),
    "4b_c-01_east---4b_c-02_west": RoomConnection("4b", all_doors["4b_c-01_east"], all_doors["4b_c-02_west"]),
    "4b_c-02_east---4b_c-03_bottom": RoomConnection("4b", all_doors["4b_c-02_east"], all_doors["4b_c-03_bottom"]),
    "4b_c-03_top---4b_c-04_west": RoomConnection("4b", all_doors["4b_c-03_top"], all_doors["4b_c-04_west"]),
    "4b_c-04_east---4b_d-00_west": RoomConnection("4b", all_doors["4b_c-04_east"], all_doors["4b_d-00_west"]),
    "4b_d-00_east---4b_d-01_west": RoomConnection("4b", all_doors["4b_d-00_east"], all_doors["4b_d-01_west"]),
    "4b_d-01_east---4b_d-02_west": RoomConnection("4b", all_doors["4b_d-01_east"], all_doors["4b_d-02_west"]),
    "4b_d-02_east---4b_d-03_west": RoomConnection("4b", all_doors["4b_d-02_east"], all_doors["4b_d-03_west"]),
    "4b_d-03_east---4b_end_west": RoomConnection("4b", all_doors["4b_d-03_east"], all_doors["4b_end_west"]),

    "4c_00_east---4c_01_west": RoomConnection("4c", all_doors["4c_00_east"], all_doors["4c_01_west"]),
    "4c_01_east---4c_02_west": RoomConnection("4c", all_doors["4c_01_east"], all_doors["4c_02_west"]),

}

all_rooms: Dict[str, Room] = {
    "0a_-1": Room("0a", "0a_-1", "Prologue - Room -1", [reg for _, reg in all_regions.items() if reg.room_name == "0a_-1"], [door for _, door in all_doors.items() if door.room_name == "0a_-1"]),
    "0a_0": Room("0a", "0a_0", "Prologue - Room 0", [reg for _, reg in all_regions.items() if reg.room_name == "0a_0"], [door for _, door in all_doors.items() if door.room_name == "0a_0"], "Start", "0a_0_west"),
    "0a_0b": Room("0a", "0a_0b", "Prologue - Room 0b", [reg for _, reg in all_regions.items() if reg.room_name == "0a_0b"], [door for _, door in all_doors.items() if door.room_name == "0a_0b"]),
    "0a_1": Room("0a", "0a_1", "Prologue - Room 1", [reg for _, reg in all_regions.items() if reg.room_name == "0a_1"], [door for _, door in all_doors.items() if door.room_name == "0a_1"]),
    "0a_2": Room("0a", "0a_2", "Prologue - Room 2", [reg for _, reg in all_regions.items() if reg.room_name == "0a_2"], [door for _, door in all_doors.items() if door.room_name == "0a_2"]),
    "0a_3": Room("0a", "0a_3", "Prologue - Room 3", [reg for _, reg in all_regions.items() if reg.room_name == "0a_3"], [door for _, door in all_doors.items() if door.room_name == "0a_3"]),

    "1a_1": Room("1a", "1a_1", "Forsaken City A - Room 1", [reg for _, reg in all_regions.items() if reg.room_name == "1a_1"], [door for _, door in all_doors.items() if door.room_name == "1a_1"], "Start", "1a_1_main"),
    "1a_2": Room("1a", "1a_2", "Forsaken City A - Room 2", [reg for _, reg in all_regions.items() if reg.room_name == "1a_2"], [door for _, door in all_doors.items() if door.room_name == "1a_2"]),
    "1a_3": Room("1a", "1a_3", "Forsaken City A - Room 3", [reg for _, reg in all_regions.items() if reg.room_name == "1a_3"], [door for _, door in all_doors.items() if door.room_name == "1a_3"]),
    "1a_4": Room("1a", "1a_4", "Forsaken City A - Room 4", [reg for _, reg in all_regions.items() if reg.room_name == "1a_4"], [door for _, door in all_doors.items() if door.room_name == "1a_4"]),
    "1a_3b": Room("1a", "1a_3b", "Forsaken City A - Room 3b", [reg for _, reg in all_regions.items() if reg.room_name == "1a_3b"], [door for _, door in all_doors.items() if door.room_name == "1a_3b"]),
    "1a_5": Room("1a", "1a_5", "Forsaken City A - Room 5", [reg for _, reg in all_regions.items() if reg.room_name == "1a_5"], [door for _, door in all_doors.items() if door.room_name == "1a_5"]),
    "1a_5z": Room("1a", "1a_5z", "Forsaken City A - Room 5z", [reg for _, reg in all_regions.items() if reg.room_name == "1a_5z"], [door for _, door in all_doors.items() if door.room_name == "1a_5z"]),
    "1a_5a": Room("1a", "1a_5a", "Forsaken City A - Room 5a", [reg for _, reg in all_regions.items() if reg.room_name == "1a_5a"], [door for _, door in all_doors.items() if door.room_name == "1a_5a"]),
    "1a_6": Room("1a", "1a_6", "Forsaken City A - Room 6", [reg for _, reg in all_regions.items() if reg.room_name == "1a_6"], [door for _, door in all_doors.items() if door.room_name == "1a_6"], "Crossing", "1a_6_south-west"),
    "1a_6z": Room("1a", "1a_6z", "Forsaken City A - Room 6z", [reg for _, reg in all_regions.items() if reg.room_name == "1a_6z"], [door for _, door in all_doors.items() if door.room_name == "1a_6z"]),
    "1a_6zb": Room("1a", "1a_6zb", "Forsaken City A - Room 6zb", [reg for _, reg in all_regions.items() if reg.room_name == "1a_6zb"], [door for _, door in all_doors.items() if door.room_name == "1a_6zb"]),
    "1a_7zb": Room("1a", "1a_7zb", "Forsaken City A - Room 7zb", [reg for _, reg in all_regions.items() if reg.room_name == "1a_7zb"], [door for _, door in all_doors.items() if door.room_name == "1a_7zb"]),
    "1a_6a": Room("1a", "1a_6a", "Forsaken City A - Room 6a", [reg for _, reg in all_regions.items() if reg.room_name == "1a_6a"], [door for _, door in all_doors.items() if door.room_name == "1a_6a"]),
    "1a_6b": Room("1a", "1a_6b", "Forsaken City A - Room 6b", [reg for _, reg in all_regions.items() if reg.room_name == "1a_6b"], [door for _, door in all_doors.items() if door.room_name == "1a_6b"]),
    "1a_s0": Room("1a", "1a_s0", "Forsaken City A - Room s0", [reg for _, reg in all_regions.items() if reg.room_name == "1a_s0"], [door for _, door in all_doors.items() if door.room_name == "1a_s0"]),
    "1a_s1": Room("1a", "1a_s1", "Forsaken City A - Room s1", [reg for _, reg in all_regions.items() if reg.room_name == "1a_s1"], [door for _, door in all_doors.items() if door.room_name == "1a_s1"]),
    "1a_6c": Room("1a", "1a_6c", "Forsaken City A - Room 6c", [reg for _, reg in all_regions.items() if reg.room_name == "1a_6c"], [door for _, door in all_doors.items() if door.room_name == "1a_6c"]),
    "1a_7": Room("1a", "1a_7", "Forsaken City A - Room 7", [reg for _, reg in all_regions.items() if reg.room_name == "1a_7"], [door for _, door in all_doors.items() if door.room_name == "1a_7"]),
    "1a_7z": Room("1a", "1a_7z", "Forsaken City A - Room 7z", [reg for _, reg in all_regions.items() if reg.room_name == "1a_7z"], [door for _, door in all_doors.items() if door.room_name == "1a_7z"]),
    "1a_8z": Room("1a", "1a_8z", "Forsaken City A - Room 8z", [reg for _, reg in all_regions.items() if reg.room_name == "1a_8z"], [door for _, door in all_doors.items() if door.room_name == "1a_8z"]),
    "1a_8zb": Room("1a", "1a_8zb", "Forsaken City A - Room 8zb", [reg for _, reg in all_regions.items() if reg.room_name == "1a_8zb"], [door for _, door in all_doors.items() if door.room_name == "1a_8zb"]),
    "1a_8": Room("1a", "1a_8", "Forsaken City A - Room 8", [reg for _, reg in all_regions.items() if reg.room_name == "1a_8"], [door for _, door in all_doors.items() if door.room_name == "1a_8"]),
    "1a_7a": Room("1a", "1a_7a", "Forsaken City A - Room 7a", [reg for _, reg in all_regions.items() if reg.room_name == "1a_7a"], [door for _, door in all_doors.items() if door.room_name == "1a_7a"]),
    "1a_9z": Room("1a", "1a_9z", "Forsaken City A - Room 9z", [reg for _, reg in all_regions.items() if reg.room_name == "1a_9z"], [door for _, door in all_doors.items() if door.room_name == "1a_9z"]),
    "1a_8b": Room("1a", "1a_8b", "Forsaken City A - Room 8b", [reg for _, reg in all_regions.items() if reg.room_name == "1a_8b"], [door for _, door in all_doors.items() if door.room_name == "1a_8b"]),
    "1a_9": Room("1a", "1a_9", "Forsaken City A - Room 9", [reg for _, reg in all_regions.items() if reg.room_name == "1a_9"], [door for _, door in all_doors.items() if door.room_name == "1a_9"]),
    "1a_9b": Room("1a", "1a_9b", "Forsaken City A - Room 9b", [reg for _, reg in all_regions.items() if reg.room_name == "1a_9b"], [door for _, door in all_doors.items() if door.room_name == "1a_9b"], "Chasm", "1a_9b_west"),
    "1a_9c": Room("1a", "1a_9c", "Forsaken City A - Room 9c", [reg for _, reg in all_regions.items() if reg.room_name == "1a_9c"], [door for _, door in all_doors.items() if door.room_name == "1a_9c"]),
    "1a_10": Room("1a", "1a_10", "Forsaken City A - Room 10", [reg for _, reg in all_regions.items() if reg.room_name == "1a_10"], [door for _, door in all_doors.items() if door.room_name == "1a_10"]),
    "1a_10z": Room("1a", "1a_10z", "Forsaken City A - Room 10z", [reg for _, reg in all_regions.items() if reg.room_name == "1a_10z"], [door for _, door in all_doors.items() if door.room_name == "1a_10z"]),
    "1a_10zb": Room("1a", "1a_10zb", "Forsaken City A - Room 10zb", [reg for _, reg in all_regions.items() if reg.room_name == "1a_10zb"], [door for _, door in all_doors.items() if door.room_name == "1a_10zb"]),
    "1a_11": Room("1a", "1a_11", "Forsaken City A - Room 11", [reg for _, reg in all_regions.items() if reg.room_name == "1a_11"], [door for _, door in all_doors.items() if door.room_name == "1a_11"]),
    "1a_11z": Room("1a", "1a_11z", "Forsaken City A - Room 11z", [reg for _, reg in all_regions.items() if reg.room_name == "1a_11z"], [door for _, door in all_doors.items() if door.room_name == "1a_11z"]),
    "1a_10a": Room("1a", "1a_10a", "Forsaken City A - Room 10a", [reg for _, reg in all_regions.items() if reg.room_name == "1a_10a"], [door for _, door in all_doors.items() if door.room_name == "1a_10a"]),
    "1a_12": Room("1a", "1a_12", "Forsaken City A - Room 12", [reg for _, reg in all_regions.items() if reg.room_name == "1a_12"], [door for _, door in all_doors.items() if door.room_name == "1a_12"]),
    "1a_12z": Room("1a", "1a_12z", "Forsaken City A - Room 12z", [reg for _, reg in all_regions.items() if reg.room_name == "1a_12z"], [door for _, door in all_doors.items() if door.room_name == "1a_12z"]),
    "1a_12a": Room("1a", "1a_12a", "Forsaken City A - Room 12a", [reg for _, reg in all_regions.items() if reg.room_name == "1a_12a"], [door for _, door in all_doors.items() if door.room_name == "1a_12a"]),
    "1a_end": Room("1a", "1a_end", "Forsaken City A - Room end", [reg for _, reg in all_regions.items() if reg.room_name == "1a_end"], [door for _, door in all_doors.items() if door.room_name == "1a_end"]),

    "1b_00": Room("1b", "1b_00", "Forsaken City B - Room 00", [reg for _, reg in all_regions.items() if reg.room_name == "1b_00"], [door for _, door in all_doors.items() if door.room_name == "1b_00"], "Start", "1b_00_west"),
    "1b_01": Room("1b", "1b_01", "Forsaken City B - Room 01", [reg for _, reg in all_regions.items() if reg.room_name == "1b_01"], [door for _, door in all_doors.items() if door.room_name == "1b_01"]),
    "1b_02": Room("1b", "1b_02", "Forsaken City B - Room 02", [reg for _, reg in all_regions.items() if reg.room_name == "1b_02"], [door for _, door in all_doors.items() if door.room_name == "1b_02"]),
    "1b_02b": Room("1b", "1b_02b", "Forsaken City B - Room 02b", [reg for _, reg in all_regions.items() if reg.room_name == "1b_02b"], [door for _, door in all_doors.items() if door.room_name == "1b_02b"]),
    "1b_03": Room("1b", "1b_03", "Forsaken City B - Room 03", [reg for _, reg in all_regions.items() if reg.room_name == "1b_03"], [door for _, door in all_doors.items() if door.room_name == "1b_03"]),
    "1b_04": Room("1b", "1b_04", "Forsaken City B - Room 04", [reg for _, reg in all_regions.items() if reg.room_name == "1b_04"], [door for _, door in all_doors.items() if door.room_name == "1b_04"], "Contraption", "1b_04_west"),
    "1b_05": Room("1b", "1b_05", "Forsaken City B - Room 05", [reg for _, reg in all_regions.items() if reg.room_name == "1b_05"], [door for _, door in all_doors.items() if door.room_name == "1b_05"]),
    "1b_05b": Room("1b", "1b_05b", "Forsaken City B - Room 05b", [reg for _, reg in all_regions.items() if reg.room_name == "1b_05b"], [door for _, door in all_doors.items() if door.room_name == "1b_05b"]),
    "1b_06": Room("1b", "1b_06", "Forsaken City B - Room 06", [reg for _, reg in all_regions.items() if reg.room_name == "1b_06"], [door for _, door in all_doors.items() if door.room_name == "1b_06"]),
    "1b_07": Room("1b", "1b_07", "Forsaken City B - Room 07", [reg for _, reg in all_regions.items() if reg.room_name == "1b_07"], [door for _, door in all_doors.items() if door.room_name == "1b_07"]),
    "1b_08": Room("1b", "1b_08", "Forsaken City B - Room 08", [reg for _, reg in all_regions.items() if reg.room_name == "1b_08"], [door for _, door in all_doors.items() if door.room_name == "1b_08"], "Scrap Pit", "1b_08_west"),
    "1b_08b": Room("1b", "1b_08b", "Forsaken City B - Room 08b", [reg for _, reg in all_regions.items() if reg.room_name == "1b_08b"], [door for _, door in all_doors.items() if door.room_name == "1b_08b"]),
    "1b_09": Room("1b", "1b_09", "Forsaken City B - Room 09", [reg for _, reg in all_regions.items() if reg.room_name == "1b_09"], [door for _, door in all_doors.items() if door.room_name == "1b_09"]),
    "1b_10": Room("1b", "1b_10", "Forsaken City B - Room 10", [reg for _, reg in all_regions.items() if reg.room_name == "1b_10"], [door for _, door in all_doors.items() if door.room_name == "1b_10"]),
    "1b_11": Room("1b", "1b_11", "Forsaken City B - Room 11", [reg for _, reg in all_regions.items() if reg.room_name == "1b_11"], [door for _, door in all_doors.items() if door.room_name == "1b_11"]),
    "1b_end": Room("1b", "1b_end", "Forsaken City B - Room end", [reg for _, reg in all_regions.items() if reg.room_name == "1b_end"], [door for _, door in all_doors.items() if door.room_name == "1b_end"]),

    "1c_00": Room("1c", "1c_00", "Forsaken City C - Room 00", [reg for _, reg in all_regions.items() if reg.room_name == "1c_00"], [door for _, door in all_doors.items() if door.room_name == "1c_00"], "Start", "1c_00_west"),
    "1c_01": Room("1c", "1c_01", "Forsaken City C - Room 01", [reg for _, reg in all_regions.items() if reg.room_name == "1c_01"], [door for _, door in all_doors.items() if door.room_name == "1c_01"]),
    "1c_02": Room("1c", "1c_02", "Forsaken City C - Room 02", [reg for _, reg in all_regions.items() if reg.room_name == "1c_02"], [door for _, door in all_doors.items() if door.room_name == "1c_02"]),

    "2a_start": Room("2a", "2a_start", "Old Site A - Room start", [reg for _, reg in all_regions.items() if reg.room_name == "2a_start"], [door for _, door in all_doors.items() if door.room_name == "2a_start"], "Start", "2a_start_main"),
    "2a_s0": Room("2a", "2a_s0", "Old Site A - Room s0", [reg for _, reg in all_regions.items() if reg.room_name == "2a_s0"], [door for _, door in all_doors.items() if door.room_name == "2a_s0"]),
    "2a_s1": Room("2a", "2a_s1", "Old Site A - Room s1", [reg for _, reg in all_regions.items() if reg.room_name == "2a_s1"], [door for _, door in all_doors.items() if door.room_name == "2a_s1"]),
    "2a_s2": Room("2a", "2a_s2", "Old Site A - Room s2", [reg for _, reg in all_regions.items() if reg.room_name == "2a_s2"], [door for _, door in all_doors.items() if door.room_name == "2a_s2"]),
    "2a_0": Room("2a", "2a_0", "Old Site A - Room 0", [reg for _, reg in all_regions.items() if reg.room_name == "2a_0"], [door for _, door in all_doors.items() if door.room_name == "2a_0"]),
    "2a_1": Room("2a", "2a_1", "Old Site A - Room 1", [reg for _, reg in all_regions.items() if reg.room_name == "2a_1"], [door for _, door in all_doors.items() if door.room_name == "2a_1"]),
    "2a_d0": Room("2a", "2a_d0", "Old Site A - Room d0", [reg for _, reg in all_regions.items() if reg.room_name == "2a_d0"], [door for _, door in all_doors.items() if door.room_name == "2a_d0"]),
    "2a_d7": Room("2a", "2a_d7", "Old Site A - Room d7", [reg for _, reg in all_regions.items() if reg.room_name == "2a_d7"], [door for _, door in all_doors.items() if door.room_name == "2a_d7"]),
    "2a_d8": Room("2a", "2a_d8", "Old Site A - Room d8", [reg for _, reg in all_regions.items() if reg.room_name == "2a_d8"], [door for _, door in all_doors.items() if door.room_name == "2a_d8"]),
    "2a_d3": Room("2a", "2a_d3", "Old Site A - Room d3", [reg for _, reg in all_regions.items() if reg.room_name == "2a_d3"], [door for _, door in all_doors.items() if door.room_name == "2a_d3"]),
    "2a_d2": Room("2a", "2a_d2", "Old Site A - Room d2", [reg for _, reg in all_regions.items() if reg.room_name == "2a_d2"], [door for _, door in all_doors.items() if door.room_name == "2a_d2"]),
    "2a_d9": Room("2a", "2a_d9", "Old Site A - Room d9", [reg for _, reg in all_regions.items() if reg.room_name == "2a_d9"], [door for _, door in all_doors.items() if door.room_name == "2a_d9"]),
    "2a_d1": Room("2a", "2a_d1", "Old Site A - Room d1", [reg for _, reg in all_regions.items() if reg.room_name == "2a_d1"], [door for _, door in all_doors.items() if door.room_name == "2a_d1"]),
    "2a_d6": Room("2a", "2a_d6", "Old Site A - Room d6", [reg for _, reg in all_regions.items() if reg.room_name == "2a_d6"], [door for _, door in all_doors.items() if door.room_name == "2a_d6"]),
    "2a_d4": Room("2a", "2a_d4", "Old Site A - Room d4", [reg for _, reg in all_regions.items() if reg.room_name == "2a_d4"], [door for _, door in all_doors.items() if door.room_name == "2a_d4"]),
    "2a_d5": Room("2a", "2a_d5", "Old Site A - Room d5", [reg for _, reg in all_regions.items() if reg.room_name == "2a_d5"], [door for _, door in all_doors.items() if door.room_name == "2a_d5"]),
    "2a_3x": Room("2a", "2a_3x", "Old Site A - Room 3x", [reg for _, reg in all_regions.items() if reg.room_name == "2a_3x"], [door for _, door in all_doors.items() if door.room_name == "2a_3x"]),
    "2a_3": Room("2a", "2a_3", "Old Site A - Room 3", [reg for _, reg in all_regions.items() if reg.room_name == "2a_3"], [door for _, door in all_doors.items() if door.room_name == "2a_3"], "Intervention", "2a_3_bottom"),
    "2a_4": Room("2a", "2a_4", "Old Site A - Room 4", [reg for _, reg in all_regions.items() if reg.room_name == "2a_4"], [door for _, door in all_doors.items() if door.room_name == "2a_4"]),
    "2a_5": Room("2a", "2a_5", "Old Site A - Room 5", [reg for _, reg in all_regions.items() if reg.room_name == "2a_5"], [door for _, door in all_doors.items() if door.room_name == "2a_5"]),
    "2a_6": Room("2a", "2a_6", "Old Site A - Room 6", [reg for _, reg in all_regions.items() if reg.room_name == "2a_6"], [door for _, door in all_doors.items() if door.room_name == "2a_6"]),
    "2a_7": Room("2a", "2a_7", "Old Site A - Room 7", [reg for _, reg in all_regions.items() if reg.room_name == "2a_7"], [door for _, door in all_doors.items() if door.room_name == "2a_7"]),
    "2a_8": Room("2a", "2a_8", "Old Site A - Room 8", [reg for _, reg in all_regions.items() if reg.room_name == "2a_8"], [door for _, door in all_doors.items() if door.room_name == "2a_8"]),
    "2a_9": Room("2a", "2a_9", "Old Site A - Room 9", [reg for _, reg in all_regions.items() if reg.room_name == "2a_9"], [door for _, door in all_doors.items() if door.room_name == "2a_9"]),
    "2a_9b": Room("2a", "2a_9b", "Old Site A - Room 9b", [reg for _, reg in all_regions.items() if reg.room_name == "2a_9b"], [door for _, door in all_doors.items() if door.room_name == "2a_9b"]),
    "2a_10": Room("2a", "2a_10", "Old Site A - Room 10", [reg for _, reg in all_regions.items() if reg.room_name == "2a_10"], [door for _, door in all_doors.items() if door.room_name == "2a_10"]),
    "2a_2": Room("2a", "2a_2", "Old Site A - Room 2", [reg for _, reg in all_regions.items() if reg.room_name == "2a_2"], [door for _, door in all_doors.items() if door.room_name == "2a_2"]),
    "2a_11": Room("2a", "2a_11", "Old Site A - Room 11", [reg for _, reg in all_regions.items() if reg.room_name == "2a_11"], [door for _, door in all_doors.items() if door.room_name == "2a_11"]),
    "2a_12b": Room("2a", "2a_12b", "Old Site A - Room 12b", [reg for _, reg in all_regions.items() if reg.room_name == "2a_12b"], [door for _, door in all_doors.items() if door.room_name == "2a_12b"]),
    "2a_12c": Room("2a", "2a_12c", "Old Site A - Room 12c", [reg for _, reg in all_regions.items() if reg.room_name == "2a_12c"], [door for _, door in all_doors.items() if door.room_name == "2a_12c"]),
    "2a_12d": Room("2a", "2a_12d", "Old Site A - Room 12d", [reg for _, reg in all_regions.items() if reg.room_name == "2a_12d"], [door for _, door in all_doors.items() if door.room_name == "2a_12d"]),
    "2a_12": Room("2a", "2a_12", "Old Site A - Room 12", [reg for _, reg in all_regions.items() if reg.room_name == "2a_12"], [door for _, door in all_doors.items() if door.room_name == "2a_12"]),
    "2a_13": Room("2a", "2a_13", "Old Site A - Room 13", [reg for _, reg in all_regions.items() if reg.room_name == "2a_13"], [door for _, door in all_doors.items() if door.room_name == "2a_13"]),
    "2a_end_0": Room("2a", "2a_end_0", "Old Site A - Room end_0", [reg for _, reg in all_regions.items() if reg.room_name == "2a_end_0"], [door for _, door in all_doors.items() if door.room_name == "2a_end_0"]),
    "2a_end_s0": Room("2a", "2a_end_s0", "Old Site A - Room end_s0", [reg for _, reg in all_regions.items() if reg.room_name == "2a_end_s0"], [door for _, door in all_doors.items() if door.room_name == "2a_end_s0"]),
    "2a_end_s1": Room("2a", "2a_end_s1", "Old Site A - Room end_s1", [reg for _, reg in all_regions.items() if reg.room_name == "2a_end_s1"], [door for _, door in all_doors.items() if door.room_name == "2a_end_s1"]),
    "2a_end_1": Room("2a", "2a_end_1", "Old Site A - Room end_1", [reg for _, reg in all_regions.items() if reg.room_name == "2a_end_1"], [door for _, door in all_doors.items() if door.room_name == "2a_end_1"]),
    "2a_end_2": Room("2a", "2a_end_2", "Old Site A - Room end_2", [reg for _, reg in all_regions.items() if reg.room_name == "2a_end_2"], [door for _, door in all_doors.items() if door.room_name == "2a_end_2"]),
    "2a_end_3": Room("2a", "2a_end_3", "Old Site A - Room end_3", [reg for _, reg in all_regions.items() if reg.room_name == "2a_end_3"], [door for _, door in all_doors.items() if door.room_name == "2a_end_3"], "Awake", "2a_end_3_west"),
    "2a_end_4": Room("2a", "2a_end_4", "Old Site A - Room end_4", [reg for _, reg in all_regions.items() if reg.room_name == "2a_end_4"], [door for _, door in all_doors.items() if door.room_name == "2a_end_4"]),
    "2a_end_3b": Room("2a", "2a_end_3b", "Old Site A - Room end_3b", [reg for _, reg in all_regions.items() if reg.room_name == "2a_end_3b"], [door for _, door in all_doors.items() if door.room_name == "2a_end_3b"]),
    "2a_end_3cb": Room("2a", "2a_end_3cb", "Old Site A - Room end_3cb", [reg for _, reg in all_regions.items() if reg.room_name == "2a_end_3cb"], [door for _, door in all_doors.items() if door.room_name == "2a_end_3cb"]),
    "2a_end_3c": Room("2a", "2a_end_3c", "Old Site A - Room end_3c", [reg for _, reg in all_regions.items() if reg.room_name == "2a_end_3c"], [door for _, door in all_doors.items() if door.room_name == "2a_end_3c"]),
    "2a_end_5": Room("2a", "2a_end_5", "Old Site A - Room end_5", [reg for _, reg in all_regions.items() if reg.room_name == "2a_end_5"], [door for _, door in all_doors.items() if door.room_name == "2a_end_5"]),
    "2a_end_6": Room("2a", "2a_end_6", "Old Site A - Room end_6", [reg for _, reg in all_regions.items() if reg.room_name == "2a_end_6"], [door for _, door in all_doors.items() if door.room_name == "2a_end_6"]),

    "2b_start": Room("2b", "2b_start", "Old Site B - Room start", [reg for _, reg in all_regions.items() if reg.room_name == "2b_start"], [door for _, door in all_doors.items() if door.room_name == "2b_start"], "Start", "2b_start_west"),
    "2b_00": Room("2b", "2b_00", "Old Site B - Room 00", [reg for _, reg in all_regions.items() if reg.room_name == "2b_00"], [door for _, door in all_doors.items() if door.room_name == "2b_00"]),
    "2b_01": Room("2b", "2b_01", "Old Site B - Room 01", [reg for _, reg in all_regions.items() if reg.room_name == "2b_01"], [door for _, door in all_doors.items() if door.room_name == "2b_01"]),
    "2b_01b": Room("2b", "2b_01b", "Old Site B - Room 01b", [reg for _, reg in all_regions.items() if reg.room_name == "2b_01b"], [door for _, door in all_doors.items() if door.room_name == "2b_01b"]),
    "2b_02b": Room("2b", "2b_02b", "Old Site B - Room 02b", [reg for _, reg in all_regions.items() if reg.room_name == "2b_02b"], [door for _, door in all_doors.items() if door.room_name == "2b_02b"]),
    "2b_02": Room("2b", "2b_02", "Old Site B - Room 02", [reg for _, reg in all_regions.items() if reg.room_name == "2b_02"], [door for _, door in all_doors.items() if door.room_name == "2b_02"]),
    "2b_03": Room("2b", "2b_03", "Old Site B - Room 03", [reg for _, reg in all_regions.items() if reg.room_name == "2b_03"], [door for _, door in all_doors.items() if door.room_name == "2b_03"], "Combination Lock", "2b_03_west"),
    "2b_04": Room("2b", "2b_04", "Old Site B - Room 04", [reg for _, reg in all_regions.items() if reg.room_name == "2b_04"], [door for _, door in all_doors.items() if door.room_name == "2b_04"]),
    "2b_05": Room("2b", "2b_05", "Old Site B - Room 05", [reg for _, reg in all_regions.items() if reg.room_name == "2b_05"], [door for _, door in all_doors.items() if door.room_name == "2b_05"]),
    "2b_06": Room("2b", "2b_06", "Old Site B - Room 06", [reg for _, reg in all_regions.items() if reg.room_name == "2b_06"], [door for _, door in all_doors.items() if door.room_name == "2b_06"]),
    "2b_07": Room("2b", "2b_07", "Old Site B - Room 07", [reg for _, reg in all_regions.items() if reg.room_name == "2b_07"], [door for _, door in all_doors.items() if door.room_name == "2b_07"]),
    "2b_08b": Room("2b", "2b_08b", "Old Site B - Room 08b", [reg for _, reg in all_regions.items() if reg.room_name == "2b_08b"], [door for _, door in all_doors.items() if door.room_name == "2b_08b"], "Dream Altar", "2b_08b_west"),
    "2b_08": Room("2b", "2b_08", "Old Site B - Room 08", [reg for _, reg in all_regions.items() if reg.room_name == "2b_08"], [door for _, door in all_doors.items() if door.room_name == "2b_08"]),
    "2b_09": Room("2b", "2b_09", "Old Site B - Room 09", [reg for _, reg in all_regions.items() if reg.room_name == "2b_09"], [door for _, door in all_doors.items() if door.room_name == "2b_09"]),
    "2b_10": Room("2b", "2b_10", "Old Site B - Room 10", [reg for _, reg in all_regions.items() if reg.room_name == "2b_10"], [door for _, door in all_doors.items() if door.room_name == "2b_10"]),
    "2b_11": Room("2b", "2b_11", "Old Site B - Room 11", [reg for _, reg in all_regions.items() if reg.room_name == "2b_11"], [door for _, door in all_doors.items() if door.room_name == "2b_11"]),
    "2b_end": Room("2b", "2b_end", "Old Site B - Room end", [reg for _, reg in all_regions.items() if reg.room_name == "2b_end"], [door for _, door in all_doors.items() if door.room_name == "2b_end"]),

    "2c_00": Room("2c", "2c_00", "Old Site C - Room 00", [reg for _, reg in all_regions.items() if reg.room_name == "2c_00"], [door for _, door in all_doors.items() if door.room_name == "2c_00"], "Start", "2c_00_west"),
    "2c_01": Room("2c", "2c_01", "Old Site C - Room 01", [reg for _, reg in all_regions.items() if reg.room_name == "2c_01"], [door for _, door in all_doors.items() if door.room_name == "2c_01"]),
    "2c_02": Room("2c", "2c_02", "Old Site C - Room 02", [reg for _, reg in all_regions.items() if reg.room_name == "2c_02"], [door for _, door in all_doors.items() if door.room_name == "2c_02"]),

    "3a_s0": Room("3a", "3a_s0", "Celestial Resort A - Room s0", [reg for _, reg in all_regions.items() if reg.room_name == "3a_s0"], [door for _, door in all_doors.items() if door.room_name == "3a_s0"], "Start", "3a_s0_main"),
    "3a_s1": Room("3a", "3a_s1", "Celestial Resort A - Room s1", [reg for _, reg in all_regions.items() if reg.room_name == "3a_s1"], [door for _, door in all_doors.items() if door.room_name == "3a_s1"]),
    "3a_s2": Room("3a", "3a_s2", "Celestial Resort A - Room s2", [reg for _, reg in all_regions.items() if reg.room_name == "3a_s2"], [door for _, door in all_doors.items() if door.room_name == "3a_s2"]),
    "3a_s3": Room("3a", "3a_s3", "Celestial Resort A - Room s3", [reg for _, reg in all_regions.items() if reg.room_name == "3a_s3"], [door for _, door in all_doors.items() if door.room_name == "3a_s3"]),
    "3a_0x-a": Room("3a", "3a_0x-a", "Celestial Resort A - Room 0x-a", [reg for _, reg in all_regions.items() if reg.room_name == "3a_0x-a"], [door for _, door in all_doors.items() if door.room_name == "3a_0x-a"]),
    "3a_00-a": Room("3a", "3a_00-a", "Celestial Resort A - Room 00-a", [reg for _, reg in all_regions.items() if reg.room_name == "3a_00-a"], [door for _, door in all_doors.items() if door.room_name == "3a_00-a"]),
    "3a_02-a": Room("3a", "3a_02-a", "Celestial Resort A - Room 02-a", [reg for _, reg in all_regions.items() if reg.room_name == "3a_02-a"], [door for _, door in all_doors.items() if door.room_name == "3a_02-a"]),
    "3a_02-b": Room("3a", "3a_02-b", "Celestial Resort A - Room 02-b", [reg for _, reg in all_regions.items() if reg.room_name == "3a_02-b"], [door for _, door in all_doors.items() if door.room_name == "3a_02-b"]),
    "3a_01-b": Room("3a", "3a_01-b", "Celestial Resort A - Room 01-b", [reg for _, reg in all_regions.items() if reg.room_name == "3a_01-b"], [door for _, door in all_doors.items() if door.room_name == "3a_01-b"]),
    "3a_00-b": Room("3a", "3a_00-b", "Celestial Resort A - Room 00-b", [reg for _, reg in all_regions.items() if reg.room_name == "3a_00-b"], [door for _, door in all_doors.items() if door.room_name == "3a_00-b"]),
    "3a_00-c": Room("3a", "3a_00-c", "Celestial Resort A - Room 00-c", [reg for _, reg in all_regions.items() if reg.room_name == "3a_00-c"], [door for _, door in all_doors.items() if door.room_name == "3a_00-c"]),
    "3a_0x-b": Room("3a", "3a_0x-b", "Celestial Resort A - Room 0x-b", [reg for _, reg in all_regions.items() if reg.room_name == "3a_0x-b"], [door for _, door in all_doors.items() if door.room_name == "3a_0x-b"]),
    "3a_03-a": Room("3a", "3a_03-a", "Celestial Resort A - Room 03-a", [reg for _, reg in all_regions.items() if reg.room_name == "3a_03-a"], [door for _, door in all_doors.items() if door.room_name == "3a_03-a"]),
    "3a_04-b": Room("3a", "3a_04-b", "Celestial Resort A - Room 04-b", [reg for _, reg in all_regions.items() if reg.room_name == "3a_04-b"], [door for _, door in all_doors.items() if door.room_name == "3a_04-b"]),
    "3a_05-a": Room("3a", "3a_05-a", "Celestial Resort A - Room 05-a", [reg for _, reg in all_regions.items() if reg.room_name == "3a_05-a"], [door for _, door in all_doors.items() if door.room_name == "3a_05-a"]),
    "3a_06-a": Room("3a", "3a_06-a", "Celestial Resort A - Room 06-a", [reg for _, reg in all_regions.items() if reg.room_name == "3a_06-a"], [door for _, door in all_doors.items() if door.room_name == "3a_06-a"]),
    "3a_07-a": Room("3a", "3a_07-a", "Celestial Resort A - Room 07-a", [reg for _, reg in all_regions.items() if reg.room_name == "3a_07-a"], [door for _, door in all_doors.items() if door.room_name == "3a_07-a"]),
    "3a_07-b": Room("3a", "3a_07-b", "Celestial Resort A - Room 07-b", [reg for _, reg in all_regions.items() if reg.room_name == "3a_07-b"], [door for _, door in all_doors.items() if door.room_name == "3a_07-b"]),
    "3a_06-b": Room("3a", "3a_06-b", "Celestial Resort A - Room 06-b", [reg for _, reg in all_regions.items() if reg.room_name == "3a_06-b"], [door for _, door in all_doors.items() if door.room_name == "3a_06-b"]),
    "3a_06-c": Room("3a", "3a_06-c", "Celestial Resort A - Room 06-c", [reg for _, reg in all_regions.items() if reg.room_name == "3a_06-c"], [door for _, door in all_doors.items() if door.room_name == "3a_06-c"]),
    "3a_05-c": Room("3a", "3a_05-c", "Celestial Resort A - Room 05-c", [reg for _, reg in all_regions.items() if reg.room_name == "3a_05-c"], [door for _, door in all_doors.items() if door.room_name == "3a_05-c"]),
    "3a_08-c": Room("3a", "3a_08-c", "Celestial Resort A - Room 08-c", [reg for _, reg in all_regions.items() if reg.room_name == "3a_08-c"], [door for _, door in all_doors.items() if door.room_name == "3a_08-c"]),
    "3a_08-b": Room("3a", "3a_08-b", "Celestial Resort A - Room 08-b", [reg for _, reg in all_regions.items() if reg.room_name == "3a_08-b"], [door for _, door in all_doors.items() if door.room_name == "3a_08-b"]),
    "3a_08-a": Room("3a", "3a_08-a", "Celestial Resort A - Room 08-a", [reg for _, reg in all_regions.items() if reg.room_name == "3a_08-a"], [door for _, door in all_doors.items() if door.room_name == "3a_08-a"], "Huge Mess", "3a_08-a_west"),
    "3a_09-b": Room("3a", "3a_09-b", "Celestial Resort A - Room 09-b", [reg for _, reg in all_regions.items() if reg.room_name == "3a_09-b"], [door for _, door in all_doors.items() if door.room_name == "3a_09-b"]),
    "3a_10-x": Room("3a", "3a_10-x", "Celestial Resort A - Room 10-x", [reg for _, reg in all_regions.items() if reg.room_name == "3a_10-x"], [door for _, door in all_doors.items() if door.room_name == "3a_10-x"]),
    "3a_11-x": Room("3a", "3a_11-x", "Celestial Resort A - Room 11-x", [reg for _, reg in all_regions.items() if reg.room_name == "3a_11-x"], [door for _, door in all_doors.items() if door.room_name == "3a_11-x"]),
    "3a_11-y": Room("3a", "3a_11-y", "Celestial Resort A - Room 11-y", [reg for _, reg in all_regions.items() if reg.room_name == "3a_11-y"], [door for _, door in all_doors.items() if door.room_name == "3a_11-y"]),
    "3a_12-y": Room("3a", "3a_12-y", "Celestial Resort A - Room 12-y", [reg for _, reg in all_regions.items() if reg.room_name == "3a_12-y"], [door for _, door in all_doors.items() if door.room_name == "3a_12-y"]),
    "3a_11-z": Room("3a", "3a_11-z", "Celestial Resort A - Room 11-z", [reg for _, reg in all_regions.items() if reg.room_name == "3a_11-z"], [door for _, door in all_doors.items() if door.room_name == "3a_11-z"]),
    "3a_10-z": Room("3a", "3a_10-z", "Celestial Resort A - Room 10-z", [reg for _, reg in all_regions.items() if reg.room_name == "3a_10-z"], [door for _, door in all_doors.items() if door.room_name == "3a_10-z"]),
    "3a_10-y": Room("3a", "3a_10-y", "Celestial Resort A - Room 10-y", [reg for _, reg in all_regions.items() if reg.room_name == "3a_10-y"], [door for _, door in all_doors.items() if door.room_name == "3a_10-y"]),
    "3a_10-c": Room("3a", "3a_10-c", "Celestial Resort A - Room 10-c", [reg for _, reg in all_regions.items() if reg.room_name == "3a_10-c"], [door for _, door in all_doors.items() if door.room_name == "3a_10-c"]),
    "3a_11-c": Room("3a", "3a_11-c", "Celestial Resort A - Room 11-c", [reg for _, reg in all_regions.items() if reg.room_name == "3a_11-c"], [door for _, door in all_doors.items() if door.room_name == "3a_11-c"]),
    "3a_12-c": Room("3a", "3a_12-c", "Celestial Resort A - Room 12-c", [reg for _, reg in all_regions.items() if reg.room_name == "3a_12-c"], [door for _, door in all_doors.items() if door.room_name == "3a_12-c"]),
    "3a_12-d": Room("3a", "3a_12-d", "Celestial Resort A - Room 12-d", [reg for _, reg in all_regions.items() if reg.room_name == "3a_12-d"], [door for _, door in all_doors.items() if door.room_name == "3a_12-d"]),
    "3a_11-d": Room("3a", "3a_11-d", "Celestial Resort A - Room 11-d", [reg for _, reg in all_regions.items() if reg.room_name == "3a_11-d"], [door for _, door in all_doors.items() if door.room_name == "3a_11-d"]),
    "3a_10-d": Room("3a", "3a_10-d", "Celestial Resort A - Room 10-d", [reg for _, reg in all_regions.items() if reg.room_name == "3a_10-d"], [door for _, door in all_doors.items() if door.room_name == "3a_10-d"]),
    "3a_11-b": Room("3a", "3a_11-b", "Celestial Resort A - Room 11-b", [reg for _, reg in all_regions.items() if reg.room_name == "3a_11-b"], [door for _, door in all_doors.items() if door.room_name == "3a_11-b"]),
    "3a_12-b": Room("3a", "3a_12-b", "Celestial Resort A - Room 12-b", [reg for _, reg in all_regions.items() if reg.room_name == "3a_12-b"], [door for _, door in all_doors.items() if door.room_name == "3a_12-b"]),
    "3a_13-b": Room("3a", "3a_13-b", "Celestial Resort A - Room 13-b", [reg for _, reg in all_regions.items() if reg.room_name == "3a_13-b"], [door for _, door in all_doors.items() if door.room_name == "3a_13-b"]),
    "3a_13-a": Room("3a", "3a_13-a", "Celestial Resort A - Room 13-a", [reg for _, reg in all_regions.items() if reg.room_name == "3a_13-a"], [door for _, door in all_doors.items() if door.room_name == "3a_13-a"]),
    "3a_13-x": Room("3a", "3a_13-x", "Celestial Resort A - Room 13-x", [reg for _, reg in all_regions.items() if reg.room_name == "3a_13-x"], [door for _, door in all_doors.items() if door.room_name == "3a_13-x"]),
    "3a_12-x": Room("3a", "3a_12-x", "Celestial Resort A - Room 12-x", [reg for _, reg in all_regions.items() if reg.room_name == "3a_12-x"], [door for _, door in all_doors.items() if door.room_name == "3a_12-x"]),
    "3a_11-a": Room("3a", "3a_11-a", "Celestial Resort A - Room 11-a", [reg for _, reg in all_regions.items() if reg.room_name == "3a_11-a"], [door for _, door in all_doors.items() if door.room_name == "3a_11-a"]),
    "3a_08-x": Room("3a", "3a_08-x", "Celestial Resort A - Room 08-x", [reg for _, reg in all_regions.items() if reg.room_name == "3a_08-x"], [door for _, door in all_doors.items() if door.room_name == "3a_08-x"]),
    "3a_09-d": Room("3a", "3a_09-d", "Celestial Resort A - Room 09-d", [reg for _, reg in all_regions.items() if reg.room_name == "3a_09-d"], [door for _, door in all_doors.items() if door.room_name == "3a_09-d"], "Elevator Shaft", "3a_09-d_bottom"),
    "3a_08-d": Room("3a", "3a_08-d", "Celestial Resort A - Room 08-d", [reg for _, reg in all_regions.items() if reg.room_name == "3a_08-d"], [door for _, door in all_doors.items() if door.room_name == "3a_08-d"]),
    "3a_06-d": Room("3a", "3a_06-d", "Celestial Resort A - Room 06-d", [reg for _, reg in all_regions.items() if reg.room_name == "3a_06-d"], [door for _, door in all_doors.items() if door.room_name == "3a_06-d"]),
    "3a_04-d": Room("3a", "3a_04-d", "Celestial Resort A - Room 04-d", [reg for _, reg in all_regions.items() if reg.room_name == "3a_04-d"], [door for _, door in all_doors.items() if door.room_name == "3a_04-d"]),
    "3a_04-c": Room("3a", "3a_04-c", "Celestial Resort A - Room 04-c", [reg for _, reg in all_regions.items() if reg.room_name == "3a_04-c"], [door for _, door in all_doors.items() if door.room_name == "3a_04-c"]),
    "3a_02-c": Room("3a", "3a_02-c", "Celestial Resort A - Room 02-c", [reg for _, reg in all_regions.items() if reg.room_name == "3a_02-c"], [door for _, door in all_doors.items() if door.room_name == "3a_02-c"]),
    "3a_03-b": Room("3a", "3a_03-b", "Celestial Resort A - Room 03-b", [reg for _, reg in all_regions.items() if reg.room_name == "3a_03-b"], [door for _, door in all_doors.items() if door.room_name == "3a_03-b"]),
    "3a_01-c": Room("3a", "3a_01-c", "Celestial Resort A - Room 01-c", [reg for _, reg in all_regions.items() if reg.room_name == "3a_01-c"], [door for _, door in all_doors.items() if door.room_name == "3a_01-c"]),
    "3a_02-d": Room("3a", "3a_02-d", "Celestial Resort A - Room 02-d", [reg for _, reg in all_regions.items() if reg.room_name == "3a_02-d"], [door for _, door in all_doors.items() if door.room_name == "3a_02-d"]),
    "3a_00-d": Room("3a", "3a_00-d", "Celestial Resort A - Room 00-d", [reg for _, reg in all_regions.items() if reg.room_name == "3a_00-d"], [door for _, door in all_doors.items() if door.room_name == "3a_00-d"], "Presidential Suite", "3a_00-d_east"),
    "3a_roof00": Room("3a", "3a_roof00", "Celestial Resort A - Room roof00", [reg for _, reg in all_regions.items() if reg.room_name == "3a_roof00"], [door for _, door in all_doors.items() if door.room_name == "3a_roof00"]),
    "3a_roof01": Room("3a", "3a_roof01", "Celestial Resort A - Room roof01", [reg for _, reg in all_regions.items() if reg.room_name == "3a_roof01"], [door for _, door in all_doors.items() if door.room_name == "3a_roof01"]),
    "3a_roof02": Room("3a", "3a_roof02", "Celestial Resort A - Room roof02", [reg for _, reg in all_regions.items() if reg.room_name == "3a_roof02"], [door for _, door in all_doors.items() if door.room_name == "3a_roof02"]),
    "3a_roof03": Room("3a", "3a_roof03", "Celestial Resort A - Room roof03", [reg for _, reg in all_regions.items() if reg.room_name == "3a_roof03"], [door for _, door in all_doors.items() if door.room_name == "3a_roof03"]),
    "3a_roof04": Room("3a", "3a_roof04", "Celestial Resort A - Room roof04", [reg for _, reg in all_regions.items() if reg.room_name == "3a_roof04"], [door for _, door in all_doors.items() if door.room_name == "3a_roof04"]),
    "3a_roof05": Room("3a", "3a_roof05", "Celestial Resort A - Room roof05", [reg for _, reg in all_regions.items() if reg.room_name == "3a_roof05"], [door for _, door in all_doors.items() if door.room_name == "3a_roof05"]),
    "3a_roof06b": Room("3a", "3a_roof06b", "Celestial Resort A - Room roof06b", [reg for _, reg in all_regions.items() if reg.room_name == "3a_roof06b"], [door for _, door in all_doors.items() if door.room_name == "3a_roof06b"]),
    "3a_roof06": Room("3a", "3a_roof06", "Celestial Resort A - Room roof06", [reg for _, reg in all_regions.items() if reg.room_name == "3a_roof06"], [door for _, door in all_doors.items() if door.room_name == "3a_roof06"]),
    "3a_roof07": Room("3a", "3a_roof07", "Celestial Resort A - Room roof07", [reg for _, reg in all_regions.items() if reg.room_name == "3a_roof07"], [door for _, door in all_doors.items() if door.room_name == "3a_roof07"]),

    "3b_00": Room("3b", "3b_00", "Celestial Resort B - Room 00", [reg for _, reg in all_regions.items() if reg.room_name == "3b_00"], [door for _, door in all_doors.items() if door.room_name == "3b_00"], "Start", "3b_00_west"),
    "3b_back": Room("3b", "3b_back", "Celestial Resort B - Room back", [reg for _, reg in all_regions.items() if reg.room_name == "3b_back"], [door for _, door in all_doors.items() if door.room_name == "3b_back"]),
    "3b_01": Room("3b", "3b_01", "Celestial Resort B - Room 01", [reg for _, reg in all_regions.items() if reg.room_name == "3b_01"], [door for _, door in all_doors.items() if door.room_name == "3b_01"]),
    "3b_02": Room("3b", "3b_02", "Celestial Resort B - Room 02", [reg for _, reg in all_regions.items() if reg.room_name == "3b_02"], [door for _, door in all_doors.items() if door.room_name == "3b_02"]),
    "3b_03": Room("3b", "3b_03", "Celestial Resort B - Room 03", [reg for _, reg in all_regions.items() if reg.room_name == "3b_03"], [door for _, door in all_doors.items() if door.room_name == "3b_03"]),
    "3b_04": Room("3b", "3b_04", "Celestial Resort B - Room 04", [reg for _, reg in all_regions.items() if reg.room_name == "3b_04"], [door for _, door in all_doors.items() if door.room_name == "3b_04"]),
    "3b_05": Room("3b", "3b_05", "Celestial Resort B - Room 05", [reg for _, reg in all_regions.items() if reg.room_name == "3b_05"], [door for _, door in all_doors.items() if door.room_name == "3b_05"]),
    "3b_06": Room("3b", "3b_06", "Celestial Resort B - Room 06", [reg for _, reg in all_regions.items() if reg.room_name == "3b_06"], [door for _, door in all_doors.items() if door.room_name == "3b_06"], "Staff Quarters", "3b_06_west"),
    "3b_07": Room("3b", "3b_07", "Celestial Resort B - Room 07", [reg for _, reg in all_regions.items() if reg.room_name == "3b_07"], [door for _, door in all_doors.items() if door.room_name == "3b_07"]),
    "3b_08": Room("3b", "3b_08", "Celestial Resort B - Room 08", [reg for _, reg in all_regions.items() if reg.room_name == "3b_08"], [door for _, door in all_doors.items() if door.room_name == "3b_08"]),
    "3b_09": Room("3b", "3b_09", "Celestial Resort B - Room 09", [reg for _, reg in all_regions.items() if reg.room_name == "3b_09"], [door for _, door in all_doors.items() if door.room_name == "3b_09"]),
    "3b_10": Room("3b", "3b_10", "Celestial Resort B - Room 10", [reg for _, reg in all_regions.items() if reg.room_name == "3b_10"], [door for _, door in all_doors.items() if door.room_name == "3b_10"]),
    "3b_11": Room("3b", "3b_11", "Celestial Resort B - Room 11", [reg for _, reg in all_regions.items() if reg.room_name == "3b_11"], [door for _, door in all_doors.items() if door.room_name == "3b_11"], "Library", "3b_11_west"),
    "3b_13": Room("3b", "3b_13", "Celestial Resort B - Room 13", [reg for _, reg in all_regions.items() if reg.room_name == "3b_13"], [door for _, door in all_doors.items() if door.room_name == "3b_13"]),
    "3b_14": Room("3b", "3b_14", "Celestial Resort B - Room 14", [reg for _, reg in all_regions.items() if reg.room_name == "3b_14"], [door for _, door in all_doors.items() if door.room_name == "3b_14"]),
    "3b_15": Room("3b", "3b_15", "Celestial Resort B - Room 15", [reg for _, reg in all_regions.items() if reg.room_name == "3b_15"], [door for _, door in all_doors.items() if door.room_name == "3b_15"]),
    "3b_12": Room("3b", "3b_12", "Celestial Resort B - Room 12", [reg for _, reg in all_regions.items() if reg.room_name == "3b_12"], [door for _, door in all_doors.items() if door.room_name == "3b_12"]),
    "3b_16": Room("3b", "3b_16", "Celestial Resort B - Room 16", [reg for _, reg in all_regions.items() if reg.room_name == "3b_16"], [door for _, door in all_doors.items() if door.room_name == "3b_16"], "Rooftop", "3b_16_west"),
    "3b_17": Room("3b", "3b_17", "Celestial Resort B - Room 17", [reg for _, reg in all_regions.items() if reg.room_name == "3b_17"], [door for _, door in all_doors.items() if door.room_name == "3b_17"]),
    "3b_18": Room("3b", "3b_18", "Celestial Resort B - Room 18", [reg for _, reg in all_regions.items() if reg.room_name == "3b_18"], [door for _, door in all_doors.items() if door.room_name == "3b_18"]),
    "3b_19": Room("3b", "3b_19", "Celestial Resort B - Room 19", [reg for _, reg in all_regions.items() if reg.room_name == "3b_19"], [door for _, door in all_doors.items() if door.room_name == "3b_19"]),
    "3b_21": Room("3b", "3b_21", "Celestial Resort B - Room 21", [reg for _, reg in all_regions.items() if reg.room_name == "3b_21"], [door for _, door in all_doors.items() if door.room_name == "3b_21"]),
    "3b_20": Room("3b", "3b_20", "Celestial Resort B - Room 20", [reg for _, reg in all_regions.items() if reg.room_name == "3b_20"], [door for _, door in all_doors.items() if door.room_name == "3b_20"]),
    "3b_end": Room("3b", "3b_end", "Celestial Resort B - Room end", [reg for _, reg in all_regions.items() if reg.room_name == "3b_end"], [door for _, door in all_doors.items() if door.room_name == "3b_end"]),

    "3c_00": Room("3c", "3c_00", "Celestial Resort C - Room 00", [reg for _, reg in all_regions.items() if reg.room_name == "3c_00"], [door for _, door in all_doors.items() if door.room_name == "3c_00"], "Start", "3c_00_west"),
    "3c_01": Room("3c", "3c_01", "Celestial Resort C - Room 01", [reg for _, reg in all_regions.items() if reg.room_name == "3c_01"], [door for _, door in all_doors.items() if door.room_name == "3c_01"]),
    "3c_02": Room("3c", "3c_02", "Celestial Resort C - Room 02", [reg for _, reg in all_regions.items() if reg.room_name == "3c_02"], [door for _, door in all_doors.items() if door.room_name == "3c_02"]),

    "4a_a-00": Room("4a", "4a_a-00", "Golden Ridge A - Room a-00", [reg for _, reg in all_regions.items() if reg.room_name == "4a_a-00"], [door for _, door in all_doors.items() if door.room_name == "4a_a-00"], "Start", "4a_a-00_west"),
    "4a_a-01": Room("4a", "4a_a-01", "Golden Ridge A - Room a-01", [reg for _, reg in all_regions.items() if reg.room_name == "4a_a-01"], [door for _, door in all_doors.items() if door.room_name == "4a_a-01"]),
    "4a_a-01x": Room("4a", "4a_a-01x", "Golden Ridge A - Room a-01x", [reg for _, reg in all_regions.items() if reg.room_name == "4a_a-01x"], [door for _, door in all_doors.items() if door.room_name == "4a_a-01x"]),
    "4a_a-02": Room("4a", "4a_a-02", "Golden Ridge A - Room a-02", [reg for _, reg in all_regions.items() if reg.room_name == "4a_a-02"], [door for _, door in all_doors.items() if door.room_name == "4a_a-02"]),
    "4a_a-03": Room("4a", "4a_a-03", "Golden Ridge A - Room a-03", [reg for _, reg in all_regions.items() if reg.room_name == "4a_a-03"], [door for _, door in all_doors.items() if door.room_name == "4a_a-03"]),
    "4a_a-04": Room("4a", "4a_a-04", "Golden Ridge A - Room a-04", [reg for _, reg in all_regions.items() if reg.room_name == "4a_a-04"], [door for _, door in all_doors.items() if door.room_name == "4a_a-04"]),
    "4a_a-05": Room("4a", "4a_a-05", "Golden Ridge A - Room a-05", [reg for _, reg in all_regions.items() if reg.room_name == "4a_a-05"], [door for _, door in all_doors.items() if door.room_name == "4a_a-05"]),
    "4a_a-06": Room("4a", "4a_a-06", "Golden Ridge A - Room a-06", [reg for _, reg in all_regions.items() if reg.room_name == "4a_a-06"], [door for _, door in all_doors.items() if door.room_name == "4a_a-06"]),
    "4a_a-07": Room("4a", "4a_a-07", "Golden Ridge A - Room a-07", [reg for _, reg in all_regions.items() if reg.room_name == "4a_a-07"], [door for _, door in all_doors.items() if door.room_name == "4a_a-07"]),
    "4a_a-08": Room("4a", "4a_a-08", "Golden Ridge A - Room a-08", [reg for _, reg in all_regions.items() if reg.room_name == "4a_a-08"], [door for _, door in all_doors.items() if door.room_name == "4a_a-08"]),
    "4a_a-10": Room("4a", "4a_a-10", "Golden Ridge A - Room a-10", [reg for _, reg in all_regions.items() if reg.room_name == "4a_a-10"], [door for _, door in all_doors.items() if door.room_name == "4a_a-10"]),
    "4a_a-11": Room("4a", "4a_a-11", "Golden Ridge A - Room a-11", [reg for _, reg in all_regions.items() if reg.room_name == "4a_a-11"], [door for _, door in all_doors.items() if door.room_name == "4a_a-11"]),
    "4a_a-09": Room("4a", "4a_a-09", "Golden Ridge A - Room a-09", [reg for _, reg in all_regions.items() if reg.room_name == "4a_a-09"], [door for _, door in all_doors.items() if door.room_name == "4a_a-09"]),
    "4a_b-00": Room("4a", "4a_b-00", "Golden Ridge A - Room b-00", [reg for _, reg in all_regions.items() if reg.room_name == "4a_b-00"], [door for _, door in all_doors.items() if door.room_name == "4a_b-00"], "Shrine", "4a_b-00_south"),
    "4a_b-01": Room("4a", "4a_b-01", "Golden Ridge A - Room b-01", [reg for _, reg in all_regions.items() if reg.room_name == "4a_b-01"], [door for _, door in all_doors.items() if door.room_name == "4a_b-01"]),
    "4a_b-04": Room("4a", "4a_b-04", "Golden Ridge A - Room b-04", [reg for _, reg in all_regions.items() if reg.room_name == "4a_b-04"], [door for _, door in all_doors.items() if door.room_name == "4a_b-04"]),
    "4a_b-06": Room("4a", "4a_b-06", "Golden Ridge A - Room b-06", [reg for _, reg in all_regions.items() if reg.room_name == "4a_b-06"], [door for _, door in all_doors.items() if door.room_name == "4a_b-06"]),
    "4a_b-07": Room("4a", "4a_b-07", "Golden Ridge A - Room b-07", [reg for _, reg in all_regions.items() if reg.room_name == "4a_b-07"], [door for _, door in all_doors.items() if door.room_name == "4a_b-07"]),
    "4a_b-03": Room("4a", "4a_b-03", "Golden Ridge A - Room b-03", [reg for _, reg in all_regions.items() if reg.room_name == "4a_b-03"], [door for _, door in all_doors.items() if door.room_name == "4a_b-03"]),
    "4a_b-02": Room("4a", "4a_b-02", "Golden Ridge A - Room b-02", [reg for _, reg in all_regions.items() if reg.room_name == "4a_b-02"], [door for _, door in all_doors.items() if door.room_name == "4a_b-02"]),
    "4a_b-sec": Room("4a", "4a_b-sec", "Golden Ridge A - Room b-sec", [reg for _, reg in all_regions.items() if reg.room_name == "4a_b-sec"], [door for _, door in all_doors.items() if door.room_name == "4a_b-sec"]),
    "4a_b-secb": Room("4a", "4a_b-secb", "Golden Ridge A - Room b-secb", [reg for _, reg in all_regions.items() if reg.room_name == "4a_b-secb"], [door for _, door in all_doors.items() if door.room_name == "4a_b-secb"]),
    "4a_b-05": Room("4a", "4a_b-05", "Golden Ridge A - Room b-05", [reg for _, reg in all_regions.items() if reg.room_name == "4a_b-05"], [door for _, door in all_doors.items() if door.room_name == "4a_b-05"]),
    "4a_b-08b": Room("4a", "4a_b-08b", "Golden Ridge A - Room b-08b", [reg for _, reg in all_regions.items() if reg.room_name == "4a_b-08b"], [door for _, door in all_doors.items() if door.room_name == "4a_b-08b"]),
    "4a_b-08": Room("4a", "4a_b-08", "Golden Ridge A - Room b-08", [reg for _, reg in all_regions.items() if reg.room_name == "4a_b-08"], [door for _, door in all_doors.items() if door.room_name == "4a_b-08"]),
    "4a_c-00": Room("4a", "4a_c-00", "Golden Ridge A - Room c-00", [reg for _, reg in all_regions.items() if reg.room_name == "4a_c-00"], [door for _, door in all_doors.items() if door.room_name == "4a_c-00"], "Old Trail", "4a_c-00_west"),
    "4a_c-01": Room("4a", "4a_c-01", "Golden Ridge A - Room c-01", [reg for _, reg in all_regions.items() if reg.room_name == "4a_c-01"], [door for _, door in all_doors.items() if door.room_name == "4a_c-01"]),
    "4a_c-02": Room("4a", "4a_c-02", "Golden Ridge A - Room c-02", [reg for _, reg in all_regions.items() if reg.room_name == "4a_c-02"], [door for _, door in all_doors.items() if door.room_name == "4a_c-02"]),
    "4a_c-04": Room("4a", "4a_c-04", "Golden Ridge A - Room c-04", [reg for _, reg in all_regions.items() if reg.room_name == "4a_c-04"], [door for _, door in all_doors.items() if door.room_name == "4a_c-04"]),
    "4a_c-05": Room("4a", "4a_c-05", "Golden Ridge A - Room c-05", [reg for _, reg in all_regions.items() if reg.room_name == "4a_c-05"], [door for _, door in all_doors.items() if door.room_name == "4a_c-05"]),
    "4a_c-06": Room("4a", "4a_c-06", "Golden Ridge A - Room c-06", [reg for _, reg in all_regions.items() if reg.room_name == "4a_c-06"], [door for _, door in all_doors.items() if door.room_name == "4a_c-06"]),
    "4a_c-06b": Room("4a", "4a_c-06b", "Golden Ridge A - Room c-06b", [reg for _, reg in all_regions.items() if reg.room_name == "4a_c-06b"], [door for _, door in all_doors.items() if door.room_name == "4a_c-06b"]),
    "4a_c-09": Room("4a", "4a_c-09", "Golden Ridge A - Room c-09", [reg for _, reg in all_regions.items() if reg.room_name == "4a_c-09"], [door for _, door in all_doors.items() if door.room_name == "4a_c-09"]),
    "4a_c-07": Room("4a", "4a_c-07", "Golden Ridge A - Room c-07", [reg for _, reg in all_regions.items() if reg.room_name == "4a_c-07"], [door for _, door in all_doors.items() if door.room_name == "4a_c-07"]),
    "4a_c-08": Room("4a", "4a_c-08", "Golden Ridge A - Room c-08", [reg for _, reg in all_regions.items() if reg.room_name == "4a_c-08"], [door for _, door in all_doors.items() if door.room_name == "4a_c-08"]),
    "4a_c-10": Room("4a", "4a_c-10", "Golden Ridge A - Room c-10", [reg for _, reg in all_regions.items() if reg.room_name == "4a_c-10"], [door for _, door in all_doors.items() if door.room_name == "4a_c-10"]),
    "4a_d-00": Room("4a", "4a_d-00", "Golden Ridge A - Room d-00", [reg for _, reg in all_regions.items() if reg.room_name == "4a_d-00"], [door for _, door in all_doors.items() if door.room_name == "4a_d-00"], "Cliff Face", "4a_d-00_west"),
    "4a_d-00b": Room("4a", "4a_d-00b", "Golden Ridge A - Room d-00b", [reg for _, reg in all_regions.items() if reg.room_name == "4a_d-00b"], [door for _, door in all_doors.items() if door.room_name == "4a_d-00b"]),
    "4a_d-01": Room("4a", "4a_d-01", "Golden Ridge A - Room d-01", [reg for _, reg in all_regions.items() if reg.room_name == "4a_d-01"], [door for _, door in all_doors.items() if door.room_name == "4a_d-01"]),
    "4a_d-02": Room("4a", "4a_d-02", "Golden Ridge A - Room d-02", [reg for _, reg in all_regions.items() if reg.room_name == "4a_d-02"], [door for _, door in all_doors.items() if door.room_name == "4a_d-02"]),
    "4a_d-03": Room("4a", "4a_d-03", "Golden Ridge A - Room d-03", [reg for _, reg in all_regions.items() if reg.room_name == "4a_d-03"], [door for _, door in all_doors.items() if door.room_name == "4a_d-03"]),
    "4a_d-04": Room("4a", "4a_d-04", "Golden Ridge A - Room d-04", [reg for _, reg in all_regions.items() if reg.room_name == "4a_d-04"], [door for _, door in all_doors.items() if door.room_name == "4a_d-04"]),
    "4a_d-05": Room("4a", "4a_d-05", "Golden Ridge A - Room d-05", [reg for _, reg in all_regions.items() if reg.room_name == "4a_d-05"], [door for _, door in all_doors.items() if door.room_name == "4a_d-05"]),
    "4a_d-06": Room("4a", "4a_d-06", "Golden Ridge A - Room d-06", [reg for _, reg in all_regions.items() if reg.room_name == "4a_d-06"], [door for _, door in all_doors.items() if door.room_name == "4a_d-06"]),
    "4a_d-07": Room("4a", "4a_d-07", "Golden Ridge A - Room d-07", [reg for _, reg in all_regions.items() if reg.room_name == "4a_d-07"], [door for _, door in all_doors.items() if door.room_name == "4a_d-07"]),
    "4a_d-08": Room("4a", "4a_d-08", "Golden Ridge A - Room d-08", [reg for _, reg in all_regions.items() if reg.room_name == "4a_d-08"], [door for _, door in all_doors.items() if door.room_name == "4a_d-08"]),
    "4a_d-09": Room("4a", "4a_d-09", "Golden Ridge A - Room d-09", [reg for _, reg in all_regions.items() if reg.room_name == "4a_d-09"], [door for _, door in all_doors.items() if door.room_name == "4a_d-09"]),
    "4a_d-10": Room("4a", "4a_d-10", "Golden Ridge A - Room d-10", [reg for _, reg in all_regions.items() if reg.room_name == "4a_d-10"], [door for _, door in all_doors.items() if door.room_name == "4a_d-10"]),

    "4b_a-00": Room("4b", "4b_a-00", "Golden Ridge B - Room a-00", [reg for _, reg in all_regions.items() if reg.room_name == "4b_a-00"], [door for _, door in all_doors.items() if door.room_name == "4b_a-00"], "Start", "4b_a-00_west"),
    "4b_a-01": Room("4b", "4b_a-01", "Golden Ridge B - Room a-01", [reg for _, reg in all_regions.items() if reg.room_name == "4b_a-01"], [door for _, door in all_doors.items() if door.room_name == "4b_a-01"]),
    "4b_a-02": Room("4b", "4b_a-02", "Golden Ridge B - Room a-02", [reg for _, reg in all_regions.items() if reg.room_name == "4b_a-02"], [door for _, door in all_doors.items() if door.room_name == "4b_a-02"]),
    "4b_a-03": Room("4b", "4b_a-03", "Golden Ridge B - Room a-03", [reg for _, reg in all_regions.items() if reg.room_name == "4b_a-03"], [door for _, door in all_doors.items() if door.room_name == "4b_a-03"]),
    "4b_a-04": Room("4b", "4b_a-04", "Golden Ridge B - Room a-04", [reg for _, reg in all_regions.items() if reg.room_name == "4b_a-04"], [door for _, door in all_doors.items() if door.room_name == "4b_a-04"]),
    "4b_b-00": Room("4b", "4b_b-00", "Golden Ridge B - Room b-00", [reg for _, reg in all_regions.items() if reg.room_name == "4b_b-00"], [door for _, door in all_doors.items() if door.room_name == "4b_b-00"], "Stepping Stones", "4b_b-00_west"),
    "4b_b-01": Room("4b", "4b_b-01", "Golden Ridge B - Room b-01", [reg for _, reg in all_regions.items() if reg.room_name == "4b_b-01"], [door for _, door in all_doors.items() if door.room_name == "4b_b-01"]),
    "4b_b-02": Room("4b", "4b_b-02", "Golden Ridge B - Room b-02", [reg for _, reg in all_regions.items() if reg.room_name == "4b_b-02"], [door for _, door in all_doors.items() if door.room_name == "4b_b-02"]),
    "4b_b-03": Room("4b", "4b_b-03", "Golden Ridge B - Room b-03", [reg for _, reg in all_regions.items() if reg.room_name == "4b_b-03"], [door for _, door in all_doors.items() if door.room_name == "4b_b-03"]),
    "4b_b-04": Room("4b", "4b_b-04", "Golden Ridge B - Room b-04", [reg for _, reg in all_regions.items() if reg.room_name == "4b_b-04"], [door for _, door in all_doors.items() if door.room_name == "4b_b-04"]),
    "4b_c-00": Room("4b", "4b_c-00", "Golden Ridge B - Room c-00", [reg for _, reg in all_regions.items() if reg.room_name == "4b_c-00"], [door for _, door in all_doors.items() if door.room_name == "4b_c-00"], "Gusty Canyon", "4b_c-00_west"),
    "4b_c-01": Room("4b", "4b_c-01", "Golden Ridge B - Room c-01", [reg for _, reg in all_regions.items() if reg.room_name == "4b_c-01"], [door for _, door in all_doors.items() if door.room_name == "4b_c-01"]),
    "4b_c-02": Room("4b", "4b_c-02", "Golden Ridge B - Room c-02", [reg for _, reg in all_regions.items() if reg.room_name == "4b_c-02"], [door for _, door in all_doors.items() if door.room_name == "4b_c-02"]),
    "4b_c-03": Room("4b", "4b_c-03", "Golden Ridge B - Room c-03", [reg for _, reg in all_regions.items() if reg.room_name == "4b_c-03"], [door for _, door in all_doors.items() if door.room_name == "4b_c-03"]),
    "4b_c-04": Room("4b", "4b_c-04", "Golden Ridge B - Room c-04", [reg for _, reg in all_regions.items() if reg.room_name == "4b_c-04"], [door for _, door in all_doors.items() if door.room_name == "4b_c-04"]),
    "4b_d-00": Room("4b", "4b_d-00", "Golden Ridge B - Room d-00", [reg for _, reg in all_regions.items() if reg.room_name == "4b_d-00"], [door for _, door in all_doors.items() if door.room_name == "4b_d-00"], "Eye of the Storm", "4b_d-00_west"),
    "4b_d-01": Room("4b", "4b_d-01", "Golden Ridge B - Room d-01", [reg for _, reg in all_regions.items() if reg.room_name == "4b_d-01"], [door for _, door in all_doors.items() if door.room_name == "4b_d-01"]),
    "4b_d-02": Room("4b", "4b_d-02", "Golden Ridge B - Room d-02", [reg for _, reg in all_regions.items() if reg.room_name == "4b_d-02"], [door for _, door in all_doors.items() if door.room_name == "4b_d-02"]),
    "4b_d-03": Room("4b", "4b_d-03", "Golden Ridge B - Room d-03", [reg for _, reg in all_regions.items() if reg.room_name == "4b_d-03"], [door for _, door in all_doors.items() if door.room_name == "4b_d-03"]),
    "4b_end": Room("4b", "4b_end", "Golden Ridge B - Room end", [reg for _, reg in all_regions.items() if reg.room_name == "4b_end"], [door for _, door in all_doors.items() if door.room_name == "4b_end"]),

    "4c_00": Room("4c", "4c_00", "Golden Ridge C - Room 00", [reg for _, reg in all_regions.items() if reg.room_name == "4c_00"], [door for _, door in all_doors.items() if door.room_name == "4c_00"], "Start", "4c_00_west"),
    "4c_01": Room("4c", "4c_01", "Golden Ridge C - Room 01", [reg for _, reg in all_regions.items() if reg.room_name == "4c_01"], [door for _, door in all_doors.items() if door.room_name == "4c_01"]),
    "4c_02": Room("4c", "4c_02", "Golden Ridge C - Room 02", [reg for _, reg in all_regions.items() if reg.room_name == "4c_02"], [door for _, door in all_doors.items() if door.room_name == "4c_02"]),

}

all_levels: Dict[str, Level] = {
    "0a": Level("0a", "Prologue", [room for _, room in all_rooms.items() if room.level_name == "0a"], [room_con for _, room_con in all_room_connections.items() if room_con.level_name == "0a"]),
    "1a": Level("1a", "Forsaken City A", [room for _, room in all_rooms.items() if room.level_name == "1a"], [room_con for _, room_con in all_room_connections.items() if room_con.level_name == "1a"]),
    "1b": Level("1b", "Forsaken City B", [room for _, room in all_rooms.items() if room.level_name == "1b"], [room_con for _, room_con in all_room_connections.items() if room_con.level_name == "1b"]),
    "1c": Level("1c", "Forsaken City C", [room for _, room in all_rooms.items() if room.level_name == "1c"], [room_con for _, room_con in all_room_connections.items() if room_con.level_name == "1c"]),
    "2a": Level("2a", "Old Site A", [room for _, room in all_rooms.items() if room.level_name == "2a"], [room_con for _, room_con in all_room_connections.items() if room_con.level_name == "2a"]),
    "2b": Level("2b", "Old Site B", [room for _, room in all_rooms.items() if room.level_name == "2b"], [room_con for _, room_con in all_room_connections.items() if room_con.level_name == "2b"]),
    "2c": Level("2c", "Old Site C", [room for _, room in all_rooms.items() if room.level_name == "2c"], [room_con for _, room_con in all_room_connections.items() if room_con.level_name == "2c"]),
    "3a": Level("3a", "Celestial Resort A", [room for _, room in all_rooms.items() if room.level_name == "3a"], [room_con for _, room_con in all_room_connections.items() if room_con.level_name == "3a"]),
    "3b": Level("3b", "Celestial Resort B", [room for _, room in all_rooms.items() if room.level_name == "3b"], [room_con for _, room_con in all_room_connections.items() if room_con.level_name == "3b"]),
    "3c": Level("3c", "Celestial Resort C", [room for _, room in all_rooms.items() if room.level_name == "3c"], [room_con for _, room_con in all_room_connections.items() if room_con.level_name == "3c"]),
    "4a": Level("4a", "Golden Ridge A", [room for _, room in all_rooms.items() if room.level_name == "4a"], [room_con for _, room_con in all_room_connections.items() if room_con.level_name == "4a"]),
    "4b": Level("4b", "Golden Ridge B", [room for _, room in all_rooms.items() if room.level_name == "4b"], [room_con for _, room_con in all_room_connections.items() if room_con.level_name == "4b"]),
    "4c": Level("4c", "Golden Ridge C", [room for _, room in all_rooms.items() if room.level_name == "4c"], [room_con for _, room_con in all_room_connections.items() if room_con.level_name == "4c"]),

}

