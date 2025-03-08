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

}

all_locations: Dict[str, LevelLocation] = {
    "0a_3_clear": LevelLocation("0a_3_clear", "Prologue - Level Clear", "0a_3_east", LocationType.level_clear, []),

    "1a_2_strawberry": LevelLocation("1a_2_strawberry", "Forsaken City A - Room 2 Strawberry", "1a_2_west", LocationType.strawberry, []),
    "1a_3_strawberry": LevelLocation("1a_3_strawberry", "Forsaken City A - Room 3 Strawberry", "1a_3_east", LocationType.strawberry, []),
    "1a_3b_strawberry": LevelLocation("1a_3b_strawberry", "Forsaken City A - Room 3b Strawberry", "1a_3b_top", LocationType.strawberry, []),
    "1a_5_strawberry": LevelLocation("1a_5_strawberry", "Forsaken City A - Room 5 Strawberry", "1a_5_north-west", LocationType.strawberry, []),
    "1a_5z_strawberry": LevelLocation("1a_5z_strawberry", "Forsaken City A - Room 5z Strawberry", "1a_5z_east", LocationType.strawberry, []),
    "1a_5a_strawberry": LevelLocation("1a_5a_strawberry", "Forsaken City A - Room 5a Strawberry", "1a_5a_west", LocationType.strawberry, []),
    "1a_6_strawberry": LevelLocation("1a_6_strawberry", "Forsaken City A - Room 6 Strawberry", "1a_6_east", LocationType.strawberry, []),
    "1a_7zb_strawberry": LevelLocation("1a_7zb_strawberry", "Forsaken City A - Room 7zb Strawberry", "1a_7zb_west", LocationType.strawberry, []),
    "1a_s1_strawberry": LevelLocation("1a_s1_strawberry", "Forsaken City A - Room s1 Strawberry", "1a_s1_east", LocationType.strawberry, []),
    "1a_s1_crystal_heart": LevelLocation("1a_s1_crystal_heart", "Forsaken City A - Crystal Heart", "1a_s1_east", LocationType.crystal_heart, []),
    "1a_7z_strawberry": LevelLocation("1a_7z_strawberry", "Forsaken City A - Room 7z Strawberry", "1a_7z_bottom", LocationType.strawberry, []),
    "1a_8zb_strawberry": LevelLocation("1a_8zb_strawberry", "Forsaken City A - Room 8zb Strawberry", "1a_8zb_west", LocationType.strawberry, []),
    "1a_7a_strawberry": LevelLocation("1a_7a_strawberry", "Forsaken City A - Room 7a Strawberry", "1a_7a_east", LocationType.strawberry, []),
    "1a_9z_strawberry": LevelLocation("1a_9z_strawberry", "Forsaken City A - Room 9z Strawberry", "1a_9z_east", LocationType.strawberry, []),
    "1a_8b_strawberry": LevelLocation("1a_8b_strawberry", "Forsaken City A - Room 8b Strawberry", "1a_8b_east", LocationType.strawberry, []),
    "1a_9_strawberry": LevelLocation("1a_9_strawberry", "Forsaken City A - Room 9 Strawberry", "1a_9_west", LocationType.strawberry, []),
    "1a_9b_strawberry": LevelLocation("1a_9b_strawberry", "Forsaken City A - Room 9b Strawberry", "1a_9b_east", LocationType.strawberry, []),
    "1a_9c_strawberry": LevelLocation("1a_9c_strawberry", "Forsaken City A - Room 9c Strawberry", "1a_9c_west", LocationType.strawberry, []),
    "1a_10zb_strawberry": LevelLocation("1a_10zb_strawberry", "Forsaken City A - Room 10zb Strawberry", "1a_10zb_east", LocationType.strawberry, []),
    "1a_11_strawberry": LevelLocation("1a_11_strawberry", "Forsaken City A - Room 11 Strawberry", "1a_11_south", LocationType.strawberry, []),
    "1a_11z_cassette": LevelLocation("1a_11z_cassette", "Forsaken City A - Cassette", "1a_11z_east", LocationType.cassette, []),
    "1a_12z_strawberry": LevelLocation("1a_12z_strawberry", "Forsaken City A - Room 12z Strawberry", "1a_12z_east", LocationType.strawberry, []),
    "1a_end_clear": LevelLocation("1a_end_clear", "Forsaken City A - Level Clear", "1a_end_main", LocationType.level_clear, []),
    "1a_end_golden": LevelLocation("1a_end_golden", "Forsaken City A - Golden Strawberry", "1a_end_main", LocationType.golden_strawberry, []),
    "1a_end_winged_golden": LevelLocation("1a_end_winged_golden", "Forsaken City A - Winged Golden Strawberry", "1a_end_main", LocationType.golden_strawberry, []),

    "1b_03_binoculars": LevelLocation("1b_03_binoculars", "Forsaken City B - Room 03 Binoculars", "1b_03_west", LocationType.binoculars, []),
    "1b_09_binoculars": LevelLocation("1b_09_binoculars", "Forsaken City B - Room 09 Binoculars", "1b_09_west", LocationType.binoculars, []),
    "1b_end_clear": LevelLocation("1b_end_clear", "Forsaken City B - Level Clear", "1b_end_goal", LocationType.level_clear, []),
    "1b_end_golden": LevelLocation("1b_end_golden", "Forsaken City B - Golden Strawberry", "1b_end_goal", LocationType.golden_strawberry, []),

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

}

all_room_connections: Dict[str, RoomConnection] = {
    "0a_-1---0a_0": RoomConnection("0a", all_doors["0a_-1_east"], all_doors["0a_0_west"]),
    "0a_0---0a_0b": RoomConnection("0a", all_doors["0a_0_north"], all_doors["0a_0b_south"]),
    "0a_0---0a_1": RoomConnection("0a", all_doors["0a_0_east"], all_doors["0a_1_west"]),
    "0a_1---0a_2": RoomConnection("0a", all_doors["0a_1_east"], all_doors["0a_2_west"]),
    "0a_2---0a_3": RoomConnection("0a", all_doors["0a_2_east"], all_doors["0a_3_west"]),

    "1a_1---1a_2": RoomConnection("1a", all_doors["1a_1_east"], all_doors["1a_2_west"]),
    "1a_2---1a_3": RoomConnection("1a", all_doors["1a_2_east"], all_doors["1a_3_west"]),
    "1a_3---1a_4": RoomConnection("1a", all_doors["1a_3_east"], all_doors["1a_4_west"]),
    "1a_4---1a_3b": RoomConnection("1a", all_doors["1a_4_east"], all_doors["1a_3b_west"]),
    "1a_3b---1a_5": RoomConnection("1a", all_doors["1a_3b_top"], all_doors["1a_5_bottom"]),
    "1a_5---1a_5z": RoomConnection("1a", all_doors["1a_5_west"], all_doors["1a_5z_east"]),
    "1a_5---1a_5a": RoomConnection("1a", all_doors["1a_5_south-east"], all_doors["1a_5a_west"]),
    "1a_5---1a_6": RoomConnection("1a", all_doors["1a_5_top"], all_doors["1a_6_south-west"]),
    "1a_6---1a_6z": RoomConnection("1a", all_doors["1a_6_west"], all_doors["1a_6z_east"]),
    "1a_6---1a_6a": RoomConnection("1a", all_doors["1a_6_east"], all_doors["1a_6a_west"]),
    "1a_6z---1a_7zb": RoomConnection("1a", all_doors["1a_6z_north-west"], all_doors["1a_7zb_east"]),
    "1a_6z---1a_6zb": RoomConnection("1a", all_doors["1a_6z_west"], all_doors["1a_6zb_east"]),
    "1a_7zb---1a_6zb": RoomConnection("1a", all_doors["1a_7zb_west"], all_doors["1a_6zb_north-west"]),
    "1a_6a---1a_6b": RoomConnection("1a", all_doors["1a_6a_east"], all_doors["1a_6b_south-west"]),
    "1a_6b---1a_s0": RoomConnection("1a", all_doors["1a_6b_north-west"], all_doors["1a_s0_east"]),
    "1a_6b---1a_6c": RoomConnection("1a", all_doors["1a_6b_north-east"], all_doors["1a_6c_south-west"]),
    "1a_s0---1a_s1": RoomConnection("1a", all_doors["1a_s0_west"], all_doors["1a_s1_east"]),
    "1a_6c---1a_7z": RoomConnection("1a", all_doors["1a_6c_north-west"], all_doors["1a_7z_bottom"]),
    "1a_6c---1a_7": RoomConnection("1a", all_doors["1a_6c_north-east"], all_doors["1a_7_west"]),
    "1a_7---1a_8": RoomConnection("1a", all_doors["1a_7_east"], all_doors["1a_8_south-west"]),
    "1a_7z---1a_8z": RoomConnection("1a", all_doors["1a_7z_top"], all_doors["1a_8z_bottom"]),
    "1a_8z---1a_8zb": RoomConnection("1a", all_doors["1a_8z_top"], all_doors["1a_8zb_west"]),
    "1a_8zb---1a_8": RoomConnection("1a", all_doors["1a_8zb_east"], all_doors["1a_8_west"]),
    "1a_8---1a_7a": RoomConnection("1a", all_doors["1a_8_south"], all_doors["1a_7a_west"]),
    "1a_8---1a_9z": RoomConnection("1a", all_doors["1a_8_north"], all_doors["1a_9z_east"]),
    "1a_8---1a_8b": RoomConnection("1a", all_doors["1a_8_north-east"], all_doors["1a_8b_west"]),
    "1a_7a---1a_8": RoomConnection("1a", all_doors["1a_7a_east"], all_doors["1a_8_south-east"]),
    "1a_8b---1a_9": RoomConnection("1a", all_doors["1a_8b_east"], all_doors["1a_9_west"]),
    "1a_9---1a_9b": RoomConnection("1a", all_doors["1a_9_east"], all_doors["1a_9b_west"]),
    "1a_9b---1a_10": RoomConnection("1a", all_doors["1a_9b_north-west"], all_doors["1a_10_south-east"]),
    "1a_9b---1a_10a": RoomConnection("1a", all_doors["1a_9b_north-east"], all_doors["1a_10a_bottom"]),
    "1a_9b---1a_9c": RoomConnection("1a", all_doors["1a_9b_east"], all_doors["1a_9c_west"]),
    "1a_10---1a_10z": RoomConnection("1a", all_doors["1a_10_south-west"], all_doors["1a_10z_east"]),
    "1a_10---1a_11": RoomConnection("1a", all_doors["1a_10_north-west"], all_doors["1a_11_south-west"]),
    "1a_10z---1a_10zb": RoomConnection("1a", all_doors["1a_10z_west"], all_doors["1a_10zb_east"]),
    "1a_11---1a_10": RoomConnection("1a", all_doors["1a_11_south"], all_doors["1a_10_north-east"]),
    "1a_11---1a_11z": RoomConnection("1a", all_doors["1a_11_west"], all_doors["1a_11z_east"]),
    "1a_10a---1a_11": RoomConnection("1a", all_doors["1a_10a_top"], all_doors["1a_11_south-east"]),
    "1a_11---1a_12": RoomConnection("1a", all_doors["1a_11_north"], all_doors["1a_12_south-west"]),
    "1a_12---1a_12z": RoomConnection("1a", all_doors["1a_12_north-west"], all_doors["1a_12z_east"]),
    "1a_12---1a_12a": RoomConnection("1a", all_doors["1a_12_east"], all_doors["1a_12a_bottom"]),
    "1a_12a---1a_end": RoomConnection("1a", all_doors["1a_12a_top"], all_doors["1a_end_south"]),

    "1b_00---1b_01": RoomConnection("1b", all_doors["1b_00_east"], all_doors["1b_01_west"]),
    "1b_01---1b_02": RoomConnection("1b", all_doors["1b_01_east"], all_doors["1b_02_west"]),
    "1b_02---1b_02b": RoomConnection("1b", all_doors["1b_02_east"], all_doors["1b_02b_west"]),
    "1b_02b---1b_03": RoomConnection("1b", all_doors["1b_02b_east"], all_doors["1b_03_west"]),
    "1b_03---1b_04": RoomConnection("1b", all_doors["1b_03_east"], all_doors["1b_04_west"]),
    "1b_04---1b_05": RoomConnection("1b", all_doors["1b_04_east"], all_doors["1b_05_west"]),
    "1b_05---1b_05b": RoomConnection("1b", all_doors["1b_05_east"], all_doors["1b_05b_west"]),
    "1b_05b---1b_06": RoomConnection("1b", all_doors["1b_05b_east"], all_doors["1b_06_west"]),
    "1b_06---1b_07": RoomConnection("1b", all_doors["1b_06_east"], all_doors["1b_07_bottom"]),
    "1b_07---1b_08": RoomConnection("1b", all_doors["1b_07_top"], all_doors["1b_08_west"]),
    "1b_08---1b_08b": RoomConnection("1b", all_doors["1b_08_east"], all_doors["1b_08b_west"]),
    "1b_08b---1b_09": RoomConnection("1b", all_doors["1b_08b_east"], all_doors["1b_09_west"]),
    "1b_09---1b_10": RoomConnection("1b", all_doors["1b_09_east"], all_doors["1b_10_west"]),
    "1b_10---1b_11": RoomConnection("1b", all_doors["1b_10_east"], all_doors["1b_11_bottom"]),
    "1b_11---1b_end": RoomConnection("1b", all_doors["1b_11_top"], all_doors["1b_end_west"]),

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

}

all_levels: Dict[str, Level] = {
    "0a": Level("0a", "Prologue", [room for _, room in all_rooms.items() if room.level_name == "0a"], [room_con for _, room_con in all_room_connections.items() if room_con.level_name == "0a"]),
    "1a": Level("1a", "Forsaken City A", [room for _, room in all_rooms.items() if room.level_name == "1a"], [room_con for _, room_con in all_room_connections.items() if room_con.level_name == "1a"]),
    "1b": Level("1b", "Forsaken City B", [room for _, room in all_rooms.items() if room.level_name == "1b"], [room_con for _, room_con in all_room_connections.items() if room_con.level_name == "1b"]),

}

