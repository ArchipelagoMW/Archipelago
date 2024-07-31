
from worlds.AutoWorld import World
from .Names import LocationName


class BowserRoom():
    name: str
    exitAddress: int
    roomID: int

    def __init__(self, name: str, exitAddress: int, roomID: int):
        self.name        = name
        self.exitAddress = exitAddress
        self.roomID      = roomID

full_bowser_rooms = [
    BowserRoom("Hallway 1 - Door 1", 0x3A680, 0x0D),
    BowserRoom("Hallway 1 - Door 2", 0x3A684, 0x0D),
    BowserRoom("Hallway 1 - Door 3", 0x3A688, 0x0D),
    BowserRoom("Hallway 1 - Door 4", 0x3A68C, 0x0D),
    BowserRoom("Hallway 2 - Door 1", 0x3A8CB, 0xD0),
    BowserRoom("Hallway 2 - Door 2", 0x3A8CF, 0xD0),
    BowserRoom("Hallway 2 - Door 3", 0x3A8D3, 0xD0),
    BowserRoom("Hallway 2 - Door 4", 0x3A8D7, 0xD0),

    BowserRoom("Room 1", 0x3A705, 0xD4),
    BowserRoom("Room 2", 0x3A763, 0xD3),
    BowserRoom("Room 3", 0x3A800, 0xD2),
    BowserRoom("Room 4", 0x3A83D, 0xD1),
    BowserRoom("Room 5", 0x3A932, 0xCF),
    BowserRoom("Room 6", 0x3A9E1, 0xCE),
    BowserRoom("Room 7", 0x3AA75, 0xCD),
    BowserRoom("Room 8", 0x3AAC7, 0xCC),
]

standard_bowser_rooms = [
    BowserRoom("Room 1", 0x3A705, 0xD4),
    BowserRoom("Room 2", 0x3A763, 0xD3),
    BowserRoom("Room 3", 0x3A800, 0xD2),
    BowserRoom("Room 4", 0x3A83D, 0xD1),
    BowserRoom("Room 5", 0x3A932, 0xCF),
    BowserRoom("Room 6", 0x3A9E1, 0xCE),
    BowserRoom("Room 7", 0x3AA75, 0xCD),
    BowserRoom("Room 8", 0x3AAC7, 0xCC),
]


class BossRoom():
    name: str
    exitAddress: int
    exitAddressAlt: int
    roomID: int

    def __init__(self, name: str, exitAddress: int, roomID: int, exitAddressAlt=None):
        self.name           = name
        self.exitAddress    = exitAddress
        self.roomID         = roomID
        self.exitAddressAlt = exitAddressAlt


submap_boss_rooms = [
    BossRoom("#1 Lemmy Koopa", 0x311E3, 0xF6), # Submap 0x1F6
    BossRoom("#3 Lemmy Koopa", 0x33749, 0xF2), # Submap 0x1F2
    BossRoom("Valley Reznor", 0x3A132, 0xDE),  # Submap 0x1DE
    BossRoom("#7 Larry Koopa", 0x3A026, 0xEB), # Submap 0x1EB
]

ow_boss_rooms = [
    BossRoom("#2 Morton Koopa Jr.", 0x3209B, 0xE5),    # OW 0x0E5
    BossRoom("Vanilla Reznor", 0x33EAB, 0xDF),         # OW 0x0DF
    BossRoom("#4 Ludwig von Koopa", 0x346EA, 0xD9),    # OW 0x0D9
    BossRoom("Forest Reznor", 0x3643E, 0xD5, 0x36442), # OW 0x0D5
    BossRoom("#5 Roy Koopa", 0x35ABC, 0xCC),           # OW 0x0CC
    BossRoom("Chocolate Reznor", 0x3705B, 0xE2),       # OW 0x0E2
    BossRoom("#6 Wendy O. Koopa", 0x38BB5, 0xD3),      # OW 0x0D3
]


level_blocks_data = {
    0x01: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    0x02: [12, 13],
    0x04: [14, 15, 16, 17, 18, 19],
    0x05: [20, 21, 22, 23, 24, 25],
    0x06: [26, 27, 28, 29],
    0x07: [30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
    0x09: [40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
    0x0A: [50, 51, 52, 53, 54, 55, 56, 57, 58, 59],
    0x0B: [60, 61, 62],
    0x0C: [63, 64, 65, 66, 67, 68],
    0x0D: [69, 70, 71],
    0x0E: [72],
    0x0F: [73, 74, 75, 76],
    0x10: [77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93,
        94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108,
        109, 110, 111
    ],
    0x11: [112],
    0x13: [113, 114, 115, 116, 117],
    0x15: [118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131,
        132, 133, 134, 135, 136, 137, 138, 139, 140
    ],
    0x18: [141, 142],
    0x1A: [143, 144, 145],
    0x1B: [146, 147, 148, 149, 150],
    0x1C: [151, 152, 153, 154],
    0x1D: [155, 156, 157],
    0x1F: [158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168],
    0x20: [169],
    0x21: [170, 171, 172],
    0x22: [173, 174, 175, 176, 177],
    0x23: [178, 179, 180, 181, 182, 183, 184, 185, 186],
    0x24: [187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200,
        201, 202
    ],
    0x25: [203, 204, 205, 206, 207, 208],
    0x26: [209, 210, 211, 212],
    0x27: [213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226,
        227, 228, 229
    ],
    0x29: [230, 231, 232, 233],
    0x2A: [234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247,
        248, 249
    ],
    0x2B: [250, 251, 252, 253, 254],
    0x2D: [255, 256, 257, 258, 259, 260, 261, 262],
    0x2E: [263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276,
        277, 278, 279
    ],
    0x2F: [280, 281, 282, 283, 284],
    0x33: [285, 286, 287, 288, 289, 290],
    0x34: [291, 292, 293],
    0x35: [294, 295],
    0x37: [296, 297],
    0x38: [298, 299, 300, 301],
    0x39: [302, 303, 304, 305],
    0x3A: [306, 307, 308, 309, 310, 311, 312, 313, 314],
    0x3B: [315, 316],
    0x3C: [317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330],
    0x3D: [331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341],
    0x3E: [342, 343, 344, 345, 346, 347, 348, 349, 350, 351],
    0x40: [352, 353, 354, 355, 356],
    0x41: [357, 358, 359, 360, 361],
    0x42: [362, 363, 364, 365, 366],
    0x43: [367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379],
    0x44: [380, 381, 382, 383, 384, 385, 386],
    0x46: [387, 388, 389],
    0x47: [390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403,
        404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416
    ],
    0x49: [417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430,
        431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443,
        444, 445, 446
    ],
    0x4A: [447, 448, 449, 450, 451],
    0x4B: [452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465,
        466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478,
        479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489
    ],
    0x4C: [490],
    0x4E: [491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504,
        505, 506, 507, 508, 509, 510, 511, 512
    ],
    0x4F: [513, 514, 515, 516, 517, 518, 519, 520, 521, 522],
    0x50: [523, 524, 525],
    0x51: [526, 527],
    0x54: [528],
    0x56: [529],
    0x59: [530, 531, 532, 533, 534, 535, 536, 537, 538],
    0x5A: [539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552,
        553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565,
        566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578,
        579, 580, 581
    ]
}

class SMWPath():
    thisEndDirection: int
    otherLevelID: int
    otherEndDirection: int

    def __init__(self, thisEndDirection: int, otherLevelID: int, otherEndDirection: int):
        self.thisEndDirection  = thisEndDirection
        self.otherLevelID      = otherLevelID
        self.otherEndDirection = otherEndDirection


class SMWLevel():
    levelName: str
    levelIDAddress: int
    #eventIDAddress: int
    eventIDValue: int
    #progressByte: int
    #progressBit: int
    exit1Path: SMWPath
    exit2Path: SMWPath

    def __init__(self, levelName: str, levelIDAddress: int, eventIDValue: int, exit1Path: SMWPath = None, exit2Path: SMWPath = None):
        self.levelName      = levelName
        self.levelIDAddress = levelIDAddress
        #self.eventIDAddress = eventIDAddress # Inferred from: LevelIDValue (Dict Key): $2D608 + LevelIDValue
        self.eventIDValue   = eventIDValue
        #self.progressByte   = progressByte # Inferred from EventIDValue: (ID / 8) + $1F02
        #self.progressBit    = progressBit  # Inferred from EventIDValue: 1 << (7 - (ID % 8))
        self.exit1Path   = exit1Path
        self.exit2Path   = exit2Path


level_info_dict = {
    0x28: SMWLevel(LocationName.yoshis_house, 0x37A76, 0x00),
    0x29: SMWLevel(LocationName.yoshis_island_1_region, 0x37A83, 0x01, SMWPath(0x08, 0x14, 0x04)),
    0x14: SMWLevel(LocationName.yellow_switch_palace, 0x37812, 0x02),
    0x2A: SMWLevel(LocationName.yoshis_island_2_region, 0x37A89, 0x03, SMWPath(0x08, 0x27, 0x04)),
    0x27: SMWLevel(LocationName.yoshis_island_3_region, 0x37A69, 0x04, SMWPath(0x01, 0x26, 0x04)),
    0x26: SMWLevel(LocationName.yoshis_island_4_region, 0x37A4B, 0x05, SMWPath(0x08, 0x25, 0x01)),
    0x25: SMWLevel(LocationName.yoshis_island_castle_region, 0x37A29, 0x06, SMWPath(0x08, 0x15, 0x04)),

    0x15: SMWLevel(LocationName.donut_plains_1_region, 0x37815, 0x07, SMWPath(0x02, 0x09, 0x04), SMWPath(0x08, 0x0A, 0x04)),
    0x09: SMWLevel(LocationName.donut_plains_2_region, 0x376D3, 0x09, SMWPath(0x08, 0x04, 0x02), SMWPath(0x02, 0x08, 0x01)),
    0x0A: SMWLevel(LocationName.donut_secret_1_region, 0x376E5, 0x10, SMWPath(0x08, 0x04, 0x04), SMWPath(0x01, 0x13, 0x08)),
    0x08: SMWLevel(LocationName.green_switch_palace, 0x376D1, 0x28),
    0x04: SMWLevel(LocationName.donut_ghost_house_region, 0x376A5, 0x0B, SMWPath(0x08, 0x03, 0x04), SMWPath(0x01, 0x05, 0x02)),
    0x13: SMWLevel(LocationName.donut_secret_house_region, 0x37807, 0x12, SMWPath(0x01, 0x2F, 0x04), SMWPath(0x04, 0x16, 0x08)), # SMW_TODO: Check this wrt pipe behavior
    0x05: SMWLevel(LocationName.donut_plains_3_region, 0x376A9, 0x0D, SMWPath(0x01, 0x06, 0x08)),
    0x06: SMWLevel(LocationName.donut_plains_4_region, 0x376CB, 0x0E, SMWPath(0x01, 0x07, 0x02)),
    0x2F: SMWLevel(LocationName.donut_secret_2_region, 0x37B10, 0x14, SMWPath(0x01, 0x05, 0x04)),
    0x07: SMWLevel(LocationName.donut_plains_castle_region, 0x376CD, 0x0F, SMWPath(0x08, 0x3E, 0x04)),
    0x03: SMWLevel(LocationName.donut_plains_top_secret, 0x37685, 0xFF),
    0x16: SMWLevel(LocationName.donut_plains_star_road, 0x37827, 0xFF),

    0x3E: SMWLevel(LocationName.vanilla_dome_1_region, 0x37C25, 0x15, SMWPath(0x01, 0x3C, 0x04), SMWPath(0x02, 0x2D, 0x04)),
    0x3C: SMWLevel(LocationName.vanilla_dome_2_region, 0x37C08, 0x17, SMWPath(0x08, 0x2B, 0x04), SMWPath(0x01, 0x3F, 0x08)),
    0x2D: SMWLevel(LocationName.vanilla_secret_1_region, 0x37AE3, 0x1D, SMWPath(0x08, 0x01, 0x02), SMWPath(0x02, 0x2C, 0x01)),
    0x2B: SMWLevel(LocationName.vanilla_ghost_house_region, 0x37AC8, 0x19, SMWPath(0x01, 0x2E, 0x08)),
    0x2E: SMWLevel(LocationName.vanilla_dome_3_region, 0x37AEC, 0x1A, SMWPath(0x04, 0x3D, 0x08)),
    0x3D: SMWLevel(LocationName.vanilla_dome_4_region, 0x37C0C, 0x1B, SMWPath(0x04, 0x40, 0x08)),
    0x3F: SMWLevel(LocationName.red_switch_palace, 0x37C2A, 0x29),
    0x01: SMWLevel(LocationName.vanilla_secret_2_region, 0x3763C, 0x1F, SMWPath(0x01, 0x02, 0x02)),
    0x02: SMWLevel(LocationName.vanilla_secret_3_region, 0x3763E, 0x20, SMWPath(0x01, 0x0B, 0x02)),
    0x0B: SMWLevel(LocationName.vanilla_fortress_region, 0x37730, 0x21, SMWPath(0x01, 0x0C, 0x02)),
    0x40: SMWLevel(LocationName.vanilla_dome_castle_region, 0x37C2C, 0x1C, SMWPath(0x04, 0x0F, 0x02)),
    0x2C: SMWLevel(LocationName.vanilla_dome_star_road, 0x37AE0, 0xFF),

    0x0C: SMWLevel(LocationName.butter_bridge_1_region, 0x37734, 0x22, SMWPath(0x01, 0x0D, 0x02)),
    0x0D: SMWLevel(LocationName.butter_bridge_2_region, 0x37736, 0x23, SMWPath(0x01, 0x0E, 0x02)),
    0x0F: SMWLevel(LocationName.cheese_bridge_region, 0x37754, 0x25, SMWPath(0x01, 0x10, 0x02), SMWPath(0x04, 0x11, 0x08)),
    0x11: SMWLevel(LocationName.soda_lake_region, 0x37784, 0x60, SMWPath(0x04, 0x12, 0x04)),
    0x10: SMWLevel(LocationName.cookie_mountain_region, 0x37757, 0x27, SMWPath(0x04, 0x0E, 0x04)),
    0x0E: SMWLevel(LocationName.twin_bridges_castle_region, 0x3773A, 0x24, SMWPath(0x01, 0x42, 0x08)),
    0x12: SMWLevel(LocationName.twin_bridges_star_road, 0x377F0, 0xFF),

    0x42: SMWLevel(LocationName.forest_of_illusion_1_region, 0x37C78, 0x2A, SMWPath(0x01, 0x44, 0x08), SMWPath(0x02, 0x41, 0x01)),
    0x44: SMWLevel(LocationName.forest_of_illusion_2_region, 0x37CAA, 0x2C, SMWPath(0x04, 0x47, 0x08), SMWPath(0x01, 0x45, 0x02)),
    0x47: SMWLevel(LocationName.forest_of_illusion_3_region, 0x37CC8, 0x2E, SMWPath(0x02, 0x41, 0x04), SMWPath(0x04, 0x20, 0x01)),
    0x43: SMWLevel(LocationName.forest_of_illusion_4_region, 0x37CA4, 0x32, SMWPath(0x01, 0x44, 0x02), SMWPath(0x04, 0x46, 0x08)),
    0x41: SMWLevel(LocationName.forest_ghost_house_region, 0x37C76, 0x30, SMWPath(0x01, 0x42, 0x02), SMWPath(0x02, 0x43, 0x08)),
    0x46: SMWLevel(LocationName.forest_secret_region, 0x37CC4, 0x34, SMWPath(0x04, 0x1F, 0x01)),
    0x45: SMWLevel(LocationName.blue_switch_palace, 0x37CAC, 0x37),
    0x1F: SMWLevel(LocationName.forest_fortress_region, 0x37906, 0x35, SMWPath(0x02, 0x1E, 0x01)),
    0x20: SMWLevel(LocationName.forest_castle_region, 0x37928, 0x61, SMWPath(0x04, 0x22, 0x08)),
    0x1E: SMWLevel(LocationName.forest_star_road, 0x37904, 0x36),

    0x22: SMWLevel(LocationName.chocolate_island_1_region, 0x37968, 0x62, SMWPath(0x02, 0x21, 0x01)),
    0x24: SMWLevel(LocationName.chocolate_island_2_region, 0x379B5, 0x46, SMWPath(0x02, 0x23, 0x01), SMWPath(0x04, 0x3B, 0x01)),
    0x23: SMWLevel(LocationName.chocolate_island_3_region, 0x379B3, 0x48, SMWPath(0x04, 0x23, 0x08), SMWPath(0x02, 0x1B, 0x01)),
    0x1D: SMWLevel(LocationName.chocolate_island_4_region, 0x378DF, 0x4B, SMWPath(0x02, 0x1C, 0x01)),
    0x1C: SMWLevel(LocationName.chocolate_island_5_region, 0x378DC, 0x4C, SMWPath(0x08, 0x1A, 0x04)),
    0x21: SMWLevel(LocationName.chocolate_ghost_house_region, 0x37965, 0x63, SMWPath(0x04, 0x24, 0x08)),
    0x1B: SMWLevel(LocationName.chocolate_fortress_region, 0x378BF, 0x4A, SMWPath(0x04, 0x1D, 0x08)),
    0x3B: SMWLevel(LocationName.chocolate_secret_region, 0x37B97, 0x4F, SMWPath(0x02, 0x1A, 0x02)),
    0x1A: SMWLevel(LocationName.chocolate_castle_region, 0x378BC, 0x4D, SMWPath(0x08, 0x18, 0x02)),

    0x18: SMWLevel(LocationName.sunken_ghost_ship_region, 0x3787E, 0x4E, SMWPath(0x08, 0x3A, 0x01)),
    0x3A: SMWLevel(LocationName.valley_of_bowser_1_region, 0x37B7B, 0x38, SMWPath(0x02, 0x39, 0x01)),
    0x39: SMWLevel(LocationName.valley_of_bowser_2_region, 0x37B79, 0x39, SMWPath(0x02, 0x38, 0x01), SMWPath(0x08, 0x35, 0x04)),
    0x37: SMWLevel(LocationName.valley_of_bowser_3_region, 0x37B74, 0x3D, SMWPath(0x08, 0x33, 0x04)),
    0x33: SMWLevel(LocationName.valley_of_bowser_4_region, 0x37B54, 0x3E, SMWPath(0x01, 0x34, 0x02), SMWPath(0x08, 0x30, 0x04)),
    0x38: SMWLevel(LocationName.valley_ghost_house_region, 0x37B77, 0x3B, SMWPath(0x02, 0x37, 0x01), SMWPath(0x08, 0x34, 0x04)),
    0x35: SMWLevel(LocationName.valley_fortress_region, 0x37B59, 0x41, SMWPath(0x08, 0x32, 0x04)),
    0x34: SMWLevel(LocationName.valley_castle_region, 0x37B57, 0x40, SMWPath(0x08, 0x31, 0x04)),
    0x31: SMWLevel(LocationName.front_door, 0x37B37, 0x45),
    0x81: SMWLevel(LocationName.front_door, 0x37B37, 0x45), # Fake Extra Front Door
    0x32: SMWLevel(LocationName.back_door, 0x37B39, 0x42),
    0x82: SMWLevel(LocationName.back_door, 0x37B39, 0x42), # Fake Extra Back Door
    0x30: SMWLevel(LocationName.valley_star_road, 0x37B34, 0x44),

    0x5B: SMWLevel(LocationName.star_road_donut, 0x37DD3, 0x50),
    0x58: SMWLevel(LocationName.star_road_1_region, 0x37DA4, 0x51, None, SMWPath(0x02, 0x53, 0x04)),
    0x53: SMWLevel(LocationName.star_road_vanilla, 0x37D82, 0x53),
    0x54: SMWLevel(LocationName.star_road_2_region, 0x37D85, 0x54, None, SMWPath(0x08, 0x52, 0x02)),
    0x52: SMWLevel(LocationName.star_road_twin_bridges, 0x37D67, 0x56),
    0x56: SMWLevel(LocationName.star_road_3_region, 0x37D89, 0x57, None, SMWPath(0x01, 0x57, 0x02)),
    0x57: SMWLevel(LocationName.star_road_forest, 0x37D8C, 0x59),
    0x59: SMWLevel(LocationName.star_road_4_region, 0x37DAA, 0x5A, None, SMWPath(0x04, 0x5C, 0x08)),
    0x5C: SMWLevel(LocationName.star_road_valley, 0x37DDC, 0x5C),
    0x5A: SMWLevel(LocationName.star_road_5_region, 0x37DB7, 0x5D, SMWPath(0x02, 0x5B, 0x01), SMWPath(0x08, 0x55, 0x04)),
    0x55: SMWLevel(LocationName.star_road_special, 0x37D87, 0x5F),

    0x4D: SMWLevel(LocationName.special_star_road, 0x37D31, 0x64),
    0x4E: SMWLevel(LocationName.special_zone_1_region, 0x37D33, 0x65, SMWPath(0x01, 0x4F, 0x02)),
    0x4F: SMWLevel(LocationName.special_zone_2_region, 0x37D36, 0x66, SMWPath(0x01, 0x50, 0x02)),
    0x50: SMWLevel(LocationName.special_zone_3_region, 0x37D39, 0x67, SMWPath(0x01, 0x51, 0x02)),
    0x51: SMWLevel(LocationName.special_zone_4_region, 0x37D3C, 0x68, SMWPath(0x01, 0x4C, 0x01)),
    0x4C: SMWLevel(LocationName.special_zone_5_region, 0x37D1C, 0x69, SMWPath(0x02, 0x4B, 0x01)),
    0x4B: SMWLevel(LocationName.special_zone_6_region, 0x37D19, 0x6A, SMWPath(0x02, 0x4A, 0x01)),
    0x4A: SMWLevel(LocationName.special_zone_7_region, 0x37D16, 0x6B, SMWPath(0x02, 0x49, 0x01)),
    0x49: SMWLevel(LocationName.special_zone_8_region, 0x37D13, 0x6C, SMWPath(0x02, 0x48, 0x01)),
    0x48: SMWLevel(LocationName.special_complete, 0x37D11, 0x6D),
}

full_level_list = [
    0x28, 0x29, 0x14, 0x2A, 0x27, 0x26, 0x25,
    0x15, 0x09, 0x0A, 0x08, 0x04, 0x13, 0x05, 0x06, 0x2F, 0x07, 0x03, 0x16,
    0x3E, 0x3C, 0x2D, 0x2B, 0x2E, 0x3D, 0x3F, 0x01, 0x02, 0x0B, 0x40, 0x2C,
    0x0C, 0x0D, 0x0F, 0x11, 0x10, 0x0E, 0x12,
    0x42, 0x44, 0x47, 0x43, 0x41, 0x46, 0x45, 0x1F, 0x20, 0x1E,
    0x22, 0x24, 0x23, 0x1D, 0x1C, 0x21, 0x1B, 0x3B, 0x1A,
    0x18, 0x3A, 0x39, 0x37, 0x33, 0x38, 0x35, 0x34, 0x31, 0x32, 0x30,
    0x5B, 0x58, 0x53, 0x54, 0x52, 0x56, 0x57, 0x59, 0x5C, 0x5A, 0x55,
    0x4D, 0x4E, 0x4F, 0x50, 0x51, 0x4C, 0x4B, 0x4A, 0x49, 0x48,
]

submap_level_list = [
    0x28, 0x29, 0x2A, 0x27, 0x26, 0x25,
    0x2F,
    0x3E, 0x3C, 0x2D, 0x2B, 0x2E, 0x3D, 0x3F, 0x40, 0x2C,
    0x42, 0x44, 0x47, 0x43, 0x41, 0x46, 0x45,
    0x3B,
    0x3A, 0x39, 0x37, 0x33, 0x38, 0x35, 0x34, 0x31, 0x32, 0x30,
    0x5B, 0x58, 0x53, 0x54, 0x52, 0x56, 0x57, 0x59, 0x5C, 0x5A, 0x55,
    0x4D, 0x4E, 0x4F, 0x50, 0x51, 0x4C, 0x4B, 0x4A, 0x49, 0x48,
]

easy_castle_fortress_levels = [
    0x07,
    0x40,
    0x1F,
    0x20,
    0x1B,
    0x34,
]

hard_castle_fortress_levels = [
    0x25,
    0x0B,
    0x0E,
    0x1A,
    0x35,
]

easy_single_levels = [
    0x29,
    0x2A,
    0x27,
    0x26,
    0x05,
    0x06,
    0x2F,
    0x2E,
    0x3D,
    0x01,
    0x0C,
    0x0D,
    0x46,
    0x1D,
]

hard_single_levels = [
    0x2B,
    0x02,
    0x11,
    0x10,
    0x22,
    0x1C,
    0x21,
    0x3B,
    0x3A,
    0x37,
]

special_zone_levels = [
    0x4E,
    0x4F,
    0x50,
    0x51,
    0x4C,
    0x4B,
    0x4A,
    0x49,
]

easy_double_levels = [
    0x15,
    0x09,
    0x42,
    0x43,
    0x24,
    0x39,
    0x59,
    0x56,
]

hard_double_levels = [
    0x0A,
    0x04,
    0x13,
    0x3E,
    0x3C,
    0x2D,
    0x0F, 
    0x44,
    0x47,
    0x41,
    0x23,
    0x33,
    0x38,
    0x58,
    0x54,
    0x5A,
]

switch_palace_levels = [
    0x14,
    0x08,
    0x3F,
    0x45,
]

location_id_to_level_id = {
    LocationName.yoshis_island_1_exit_1:  [0x29, 0],
    LocationName.yoshis_island_1_dragon:  [0x29, 2],
    LocationName.yoshis_island_1_moon:    [0x29, 3],
    LocationName.yoshis_island_2_exit_1:  [0x2A, 0],
    LocationName.yoshis_island_2_dragon:  [0x2A, 2],
    LocationName.yoshis_island_3_exit_1:  [0x27, 0],
    LocationName.yoshis_island_3_dragon:  [0x27, 2],
    LocationName.yoshis_island_3_bonus_block:  [0x27, 5],
    LocationName.yoshis_island_4_exit_1:  [0x26, 0],
    LocationName.yoshis_island_4_dragon:  [0x26, 2],
    LocationName.yoshis_island_4_hidden_1up:  [0x26, 4],
    LocationName.yoshis_island_castle:    [0x25, 0],
    LocationName.yoshis_island_koopaling: [0x25, 0],
    LocationName.yellow_switch_palace:    [0x14, 0],

    LocationName.donut_plains_1_exit_1:     [0x15, 0],
    LocationName.donut_plains_1_exit_2:     [0x15, 1],
    LocationName.donut_plains_1_dragon:     [0x15, 2],
    LocationName.donut_plains_1_hidden_1up:     [0x15, 4],
    LocationName.donut_plains_2_exit_1:     [0x09, 0],
    LocationName.donut_plains_2_exit_2:     [0x09, 1],
    LocationName.donut_plains_2_dragon:     [0x09, 2],
    LocationName.donut_plains_3_exit_1:     [0x05, 0],
    LocationName.donut_plains_3_dragon:     [0x05, 2],
    LocationName.donut_plains_3_bonus_block:     [0x05, 5],
    LocationName.donut_plains_4_exit_1:     [0x06, 0],
    LocationName.donut_plains_4_dragon:     [0x06, 2],
    LocationName.donut_plains_4_moon:       [0x06, 3],
    LocationName.donut_plains_4_hidden_1up:       [0x06, 4],
    LocationName.donut_secret_1_exit_1:     [0x0A, 0],
    LocationName.donut_secret_1_exit_2:     [0x0A, 1],
    LocationName.donut_secret_1_dragon:     [0x0A, 2],
    LocationName.donut_secret_2_exit_1:     [0x2F, 0],
    LocationName.donut_secret_2_dragon:     [0x2F, 2],
    LocationName.donut_ghost_house_exit_1:  [0x04, 0],
    LocationName.donut_ghost_house_exit_2:  [0x04, 1],
    LocationName.donut_secret_house_exit_1: [0x13, 0],
    LocationName.donut_secret_house_exit_2: [0x13, 1],
    LocationName.donut_plains_castle:       [0x07, 0],
    LocationName.donut_plains_castle_hidden_1up:       [0x07, 4],
    LocationName.donut_plains_koopaling:    [0x07, 0],
    LocationName.green_switch_palace:       [0x08, 0],

    LocationName.vanilla_dome_1_exit_1:      [0x3E, 0],
    LocationName.vanilla_dome_1_exit_2:      [0x3E, 1],
    LocationName.vanilla_dome_1_dragon:      [0x3E, 2],
    LocationName.vanilla_dome_2_exit_1:      [0x3C, 0],
    LocationName.vanilla_dome_2_exit_2:      [0x3C, 1],
    LocationName.vanilla_dome_2_dragon:      [0x3C, 2],
    LocationName.vanilla_dome_3_exit_1:      [0x2E, 0],
    LocationName.vanilla_dome_3_dragon:      [0x2E, 2],
    LocationName.vanilla_dome_3_moon:        [0x2E, 3],
    LocationName.vanilla_dome_4_exit_1:      [0x3D, 0],
    LocationName.vanilla_dome_4_dragon:      [0x3D, 2],
    LocationName.vanilla_dome_4_hidden_1up:      [0x3D, 4],
    LocationName.vanilla_secret_1_exit_1:    [0x2D, 0],
    LocationName.vanilla_secret_1_exit_2:    [0x2D, 1],
    LocationName.vanilla_secret_1_dragon:    [0x2D, 2],
    LocationName.vanilla_secret_2_exit_1:    [0x01, 0],
    LocationName.vanilla_secret_2_dragon:    [0x01, 2],
    LocationName.vanilla_secret_3_exit_1:    [0x02, 0],
    LocationName.vanilla_secret_3_dragon:    [0x02, 2],
    LocationName.vanilla_ghost_house_exit_1: [0x2B, 0],
    LocationName.vanilla_ghost_house_dragon: [0x2B, 2],
    LocationName.vanilla_ghost_house_hidden_1up: [0x2B, 4],
    LocationName.vanilla_fortress:           [0x0B, 0],
    LocationName.vanilla_fortress_hidden_1up:         [0x0B, 4],
    LocationName.vanilla_reznor:             [0x0B, 0],
    LocationName.vanilla_dome_castle:        [0x40, 0],
    LocationName.vanilla_dome_koopaling:     [0x40, 0],
    LocationName.red_switch_palace:          [0x3F, 0],

    LocationName.butter_bridge_1_exit_1: [0x0C, 0],
    LocationName.butter_bridge_1_dragon: [0x0C, 2],
    LocationName.butter_bridge_1_bonus_block: [0x0C, 5],
    LocationName.butter_bridge_2_exit_1: [0x0D, 0],
    LocationName.butter_bridge_2_dragon: [0x0D, 2],
    LocationName.cheese_bridge_exit_1:   [0x0F, 0],
    LocationName.cheese_bridge_exit_2:   [0x0F, 1],
    LocationName.cheese_bridge_dragon:   [0x0F, 2],
    LocationName.cheese_bridge_moon:     [0x0F, 3],
    LocationName.cookie_mountain_exit_1: [0x10, 0],
    LocationName.cookie_mountain_dragon: [0x10, 2],
    LocationName.cookie_mountain_hidden_1up: [0x10, 4],
    LocationName.soda_lake_exit_1:       [0x11, 0],
    LocationName.soda_lake_dragon:       [0x11, 2],
    LocationName.twin_bridges_castle:    [0x0E, 0],
    LocationName.twin_bridges_koopaling: [0x0E, 0],

    LocationName.forest_of_illusion_1_exit_1: [0x42, 0],
    LocationName.forest_of_illusion_1_exit_2: [0x42, 1],
    LocationName.forest_of_illusion_2_exit_1: [0x44, 0],
    LocationName.forest_of_illusion_2_exit_2: [0x44, 1],
    LocationName.forest_of_illusion_2_dragon: [0x44, 2],
    LocationName.forest_of_illusion_3_exit_1: [0x47, 0],
    LocationName.forest_of_illusion_3_exit_2: [0x47, 1],
    LocationName.forest_of_illusion_3_dragon: [0x47, 2],
    LocationName.forest_of_illusion_3_hidden_1up: [0x47, 4],
    LocationName.forest_of_illusion_4_exit_1: [0x43, 0],
    LocationName.forest_of_illusion_4_exit_2: [0x43, 1],
    LocationName.forest_of_illusion_4_dragon: [0x43, 2],
    LocationName.forest_ghost_house_exit_1:   [0x41, 0],
    LocationName.forest_ghost_house_exit_2:   [0x41, 1],
    LocationName.forest_ghost_house_dragon:   [0x41, 2],
    LocationName.forest_ghost_house_moon:     [0x41, 3],
    LocationName.forest_secret_exit_1:        [0x46, 0],
    LocationName.forest_secret_dragon:        [0x46, 2],
    LocationName.forest_fortress:             [0x1F, 0],
    LocationName.forest_reznor:               [0x1F, 0],
    LocationName.forest_castle:               [0x20, 0],
    LocationName.forest_koopaling:            [0x20, 0],
    LocationName.forest_castle_dragon:        [0x20, 2],
    LocationName.blue_switch_palace:          [0x45, 0],

    LocationName.chocolate_island_1_exit_1:    [0x22, 0],
    LocationName.chocolate_island_1_dragon:    [0x22, 2],
    LocationName.chocolate_island_1_moon:      [0x22, 3],
    LocationName.chocolate_island_2_exit_1:    [0x24, 0],
    LocationName.chocolate_island_2_exit_2:    [0x24, 1],
    LocationName.chocolate_island_2_dragon:    [0x24, 2],
    LocationName.chocolate_island_2_hidden_1up:    [0x24, 4],
    LocationName.chocolate_island_3_exit_1:    [0x23, 0],
    LocationName.chocolate_island_3_exit_2:    [0x23, 1],
    LocationName.chocolate_island_3_dragon:    [0x23, 2],
    LocationName.chocolate_island_3_bonus_block:    [0x23, 5],
    LocationName.chocolate_island_4_exit_1:    [0x1D, 0],
    LocationName.chocolate_island_4_dragon:    [0x1D, 2],
    LocationName.chocolate_island_5_exit_1:    [0x1C, 0],
    LocationName.chocolate_island_5_dragon:    [0x1C, 2],
    LocationName.chocolate_ghost_house_exit_1: [0x21, 0],
    LocationName.chocolate_secret_exit_1:      [0x3B, 0],
    LocationName.chocolate_fortress:           [0x1B, 0],
    LocationName.chocolate_reznor:             [0x1B, 0],
    LocationName.chocolate_castle:             [0x1A, 0],
    LocationName.chocolate_castle_hidden_1up:             [0x1A, 4],
    LocationName.chocolate_koopaling:          [0x1A, 0],

    LocationName.sunken_ghost_ship:        [0x18, 0],
    LocationName.sunken_ghost_ship_dragon: [0x18, 2],

    LocationName.valley_of_bowser_1_exit_1: [0x3A, 0],
    LocationName.valley_of_bowser_1_dragon: [0x3A, 2],
    LocationName.valley_of_bowser_1_moon:   [0x3A, 3],
    LocationName.valley_of_bowser_2_exit_1: [0x39, 0],
    LocationName.valley_of_bowser_2_exit_2: [0x39, 1],
    LocationName.valley_of_bowser_2_dragon: [0x39, 2],
    LocationName.valley_of_bowser_2_hidden_1up: [0x39, 4],
    LocationName.valley_of_bowser_3_exit_1: [0x37, 0],
    LocationName.valley_of_bowser_3_dragon: [0x37, 2],
    LocationName.valley_of_bowser_4_exit_1: [0x33, 0],
    LocationName.valley_of_bowser_4_exit_2: [0x33, 1],
    LocationName.valley_ghost_house_exit_1: [0x38, 0],
    LocationName.valley_ghost_house_exit_2: [0x38, 1],
    LocationName.valley_ghost_house_dragon: [0x38, 2],
    LocationName.valley_fortress:           [0x35, 0],
    LocationName.valley_reznor:             [0x35, 0],
    LocationName.valley_castle:             [0x34, 0],
    LocationName.valley_koopaling:          [0x34, 0],
    LocationName.valley_castle_dragon:      [0x34, 2],
    LocationName.valley_castle_hidden_1up:       [0x34, 4],

    LocationName.star_road_1_exit_1: [0x58, 0],
    LocationName.star_road_1_exit_2: [0x58, 1],
    LocationName.star_road_1_dragon: [0x58, 2],
    LocationName.star_road_2_exit_1: [0x54, 0],
    LocationName.star_road_2_exit_2: [0x54, 1],
    LocationName.star_road_3_exit_1: [0x56, 0],
    LocationName.star_road_3_exit_2: [0x56, 1],
    LocationName.star_road_4_exit_1: [0x59, 0],
    LocationName.star_road_4_exit_2: [0x59, 1],
    LocationName.star_road_5_exit_1: [0x5A, 0],
    LocationName.star_road_5_exit_2: [0x5A, 1],

    LocationName.special_zone_1_exit_1: [0x4E, 0],
    LocationName.special_zone_1_dragon: [0x4E, 2],
    LocationName.special_zone_1_hidden_1up: [0x4E, 4],
    LocationName.special_zone_2_exit_1: [0x4F, 0],
    LocationName.special_zone_2_dragon: [0x4F, 2],
    LocationName.special_zone_3_exit_1: [0x50, 0],
    LocationName.special_zone_3_dragon: [0x50, 2],
    LocationName.special_zone_4_exit_1: [0x51, 0],
    LocationName.special_zone_4_dragon: [0x51, 2],
    LocationName.special_zone_5_exit_1: [0x4C, 0],
    LocationName.special_zone_5_dragon: [0x4C, 2],
    LocationName.special_zone_6_exit_1: [0x4B, 0],
    LocationName.special_zone_6_dragon: [0x4B, 2],
    LocationName.special_zone_7_exit_1: [0x4A, 0],
    LocationName.special_zone_7_dragon: [0x4A, 2],
    LocationName.special_zone_8_exit_1: [0x49, 0],
    LocationName.special_zone_8_dragon: [0x49, 2],

    LocationName.vanilla_secret_2_yoshi_block_1: [0x01, 100],
    LocationName.vanilla_secret_2_green_block_1: [0x01, 101],
    LocationName.vanilla_secret_2_powerup_block_1: [0x01, 102],
    LocationName.vanilla_secret_2_powerup_block_2: [0x01, 103],
    LocationName.vanilla_secret_2_multi_coin_block_1: [0x01, 104],
    LocationName.vanilla_secret_2_gray_pow_block_1: [0x01, 105],
    LocationName.vanilla_secret_2_coin_block_1: [0x01, 106],
    LocationName.vanilla_secret_2_coin_block_2: [0x01, 107],
    LocationName.vanilla_secret_2_coin_block_3: [0x01, 108],
    LocationName.vanilla_secret_2_coin_block_4: [0x01, 109],
    LocationName.vanilla_secret_2_coin_block_5: [0x01, 110],
    LocationName.vanilla_secret_2_coin_block_6: [0x01, 111],
    LocationName.vanilla_secret_3_powerup_block_1: [0x02, 112],
    LocationName.vanilla_secret_3_powerup_block_2: [0x02, 113],
    LocationName.donut_ghost_house_vine_block_1: [0x04, 114],
    LocationName.donut_ghost_house_directional_coin_block_1: [0x04, 115],
    LocationName.donut_ghost_house_life_block_1: [0x04, 116],
    LocationName.donut_ghost_house_life_block_2: [0x04, 117],
    LocationName.donut_ghost_house_life_block_3: [0x04, 118],
    LocationName.donut_ghost_house_life_block_4: [0x04, 119],
    LocationName.donut_plains_3_green_block_1: [0x05, 120],
    LocationName.donut_plains_3_coin_block_1: [0x05, 121],
    LocationName.donut_plains_3_coin_block_2: [0x05, 122],
    LocationName.donut_plains_3_vine_block_1: [0x05, 123],
    LocationName.donut_plains_3_powerup_block_1: [0x05, 124],
    LocationName.donut_plains_3_bonus_block_1: [0x05, 125],
    LocationName.donut_plains_4_coin_block_1: [0x06, 126],
    LocationName.donut_plains_4_powerup_block_1: [0x06, 127],
    LocationName.donut_plains_4_coin_block_2: [0x06, 128],
    LocationName.donut_plains_4_yoshi_block_1: [0x06, 129],
    LocationName.donut_plains_castle_yellow_block_1: [0x07, 130],
    LocationName.donut_plains_castle_coin_block_1: [0x07, 131],
    LocationName.donut_plains_castle_powerup_block_1: [0x07, 132],
    LocationName.donut_plains_castle_coin_block_2: [0x07, 133],
    LocationName.donut_plains_castle_vine_block_1: [0x07, 134],
    LocationName.donut_plains_castle_invis_life_block_1: [0x07, 135],
    LocationName.donut_plains_castle_coin_block_3: [0x07, 136],
    LocationName.donut_plains_castle_coin_block_4: [0x07, 137],
    LocationName.donut_plains_castle_coin_block_5: [0x07, 138],
    LocationName.donut_plains_castle_green_block_1: [0x07, 139],
    LocationName.donut_plains_2_coin_block_1: [0x09, 140],
    LocationName.donut_plains_2_coin_block_2: [0x09, 141],
    LocationName.donut_plains_2_coin_block_3: [0x09, 142],
    LocationName.donut_plains_2_yellow_block_1: [0x09, 143],
    LocationName.donut_plains_2_powerup_block_1: [0x09, 144],
    LocationName.donut_plains_2_multi_coin_block_1: [0x09, 145],
    LocationName.donut_plains_2_flying_block_1: [0x09, 146],
    LocationName.donut_plains_2_green_block_1: [0x09, 147],
    LocationName.donut_plains_2_yellow_block_2: [0x09, 148],
    LocationName.donut_plains_2_vine_block_1: [0x09, 149],
    LocationName.donut_secret_1_coin_block_1: [0x0A, 150],
    LocationName.donut_secret_1_coin_block_2: [0x0A, 151],
    LocationName.donut_secret_1_powerup_block_1: [0x0A, 152],
    LocationName.donut_secret_1_coin_block_3: [0x0A, 153],
    LocationName.donut_secret_1_powerup_block_2: [0x0A, 154],
    LocationName.donut_secret_1_powerup_block_3: [0x0A, 155],
    LocationName.donut_secret_1_life_block_1: [0x0A, 156],
    LocationName.donut_secret_1_powerup_block_4: [0x0A, 157],
    LocationName.donut_secret_1_powerup_block_5: [0x0A, 158],
    LocationName.donut_secret_1_key_block_1: [0x0A, 159],
    LocationName.vanilla_fortress_powerup_block_1: [0x0B, 160],
    LocationName.vanilla_fortress_powerup_block_2: [0x0B, 161],
    LocationName.vanilla_fortress_yellow_block_1: [0x0B, 162],
    LocationName.butter_bridge_1_powerup_block_1: [0x0C, 163],
    LocationName.butter_bridge_1_multi_coin_block_1: [0x0C, 164],
    LocationName.butter_bridge_1_multi_coin_block_2: [0x0C, 165],
    LocationName.butter_bridge_1_multi_coin_block_3: [0x0C, 166],
    LocationName.butter_bridge_1_life_block_1: [0x0C, 167],
    LocationName.butter_bridge_1_bonus_block_1: [0x0C, 168],
    LocationName.butter_bridge_2_powerup_block_1: [0x0D, 169],
    LocationName.butter_bridge_2_green_block_1: [0x0D, 170],
    LocationName.butter_bridge_2_yoshi_block_1: [0x0D, 171],
    LocationName.twin_bridges_castle_powerup_block_1: [0x0E, 172],
    LocationName.cheese_bridge_powerup_block_1: [0x0F, 173],
    LocationName.cheese_bridge_powerup_block_2: [0x0F, 174],
    LocationName.cheese_bridge_wings_block_1: [0x0F, 175],
    LocationName.cheese_bridge_powerup_block_3: [0x0F, 176],
    LocationName.cookie_mountain_coin_block_1: [0x10, 177],
    LocationName.cookie_mountain_coin_block_2: [0x10, 178],
    LocationName.cookie_mountain_coin_block_3: [0x10, 179],
    LocationName.cookie_mountain_coin_block_4: [0x10, 180],
    LocationName.cookie_mountain_coin_block_5: [0x10, 181],
    LocationName.cookie_mountain_coin_block_6: [0x10, 182],
    LocationName.cookie_mountain_coin_block_7: [0x10, 183],
    LocationName.cookie_mountain_coin_block_8: [0x10, 184],
    LocationName.cookie_mountain_coin_block_9: [0x10, 185],
    LocationName.cookie_mountain_powerup_block_1: [0x10, 186],
    LocationName.cookie_mountain_life_block_1: [0x10, 187],
    LocationName.cookie_mountain_vine_block_1: [0x10, 188],
    LocationName.cookie_mountain_yoshi_block_1: [0x10, 189],
    LocationName.cookie_mountain_coin_block_10: [0x10, 190],
    LocationName.cookie_mountain_coin_block_11: [0x10, 191],
    LocationName.cookie_mountain_powerup_block_2: [0x10, 192],
    LocationName.cookie_mountain_coin_block_12: [0x10, 193],
    LocationName.cookie_mountain_coin_block_13: [0x10, 194],
    LocationName.cookie_mountain_coin_block_14: [0x10, 195],
    LocationName.cookie_mountain_coin_block_15: [0x10, 196],
    LocationName.cookie_mountain_coin_block_16: [0x10, 197],
    LocationName.cookie_mountain_coin_block_17: [0x10, 198],
    LocationName.cookie_mountain_coin_block_18: [0x10, 199],
    LocationName.cookie_mountain_coin_block_19: [0x10, 200],
    LocationName.cookie_mountain_coin_block_20: [0x10, 201],
    LocationName.cookie_mountain_coin_block_21: [0x10, 202],
    LocationName.cookie_mountain_coin_block_22: [0x10, 203],
    LocationName.cookie_mountain_coin_block_23: [0x10, 204],
    LocationName.cookie_mountain_coin_block_24: [0x10, 205],
    LocationName.cookie_mountain_coin_block_25: [0x10, 206],
    LocationName.cookie_mountain_coin_block_26: [0x10, 207],
    LocationName.cookie_mountain_coin_block_27: [0x10, 208],
    LocationName.cookie_mountain_coin_block_28: [0x10, 209],
    LocationName.cookie_mountain_coin_block_29: [0x10, 210],
    LocationName.cookie_mountain_coin_block_30: [0x10, 211],
    LocationName.soda_lake_powerup_block_1: [0x11, 212],
    LocationName.donut_secret_house_powerup_block_1: [0x13, 213],
    LocationName.donut_secret_house_multi_coin_block_1: [0x13, 214],
    LocationName.donut_secret_house_life_block_1: [0x13, 215],
    LocationName.donut_secret_house_vine_block_1: [0x13, 216],
    LocationName.donut_secret_house_directional_coin_block_1: [0x13, 217],
    LocationName.donut_plains_1_coin_block_1: [0x15, 218],
    LocationName.donut_plains_1_coin_block_2: [0x15, 219],
    LocationName.donut_plains_1_yoshi_block_1: [0x15, 220],
    LocationName.donut_plains_1_vine_block_1: [0x15, 221],
    LocationName.donut_plains_1_green_block_1: [0x15, 222],
    LocationName.donut_plains_1_green_block_2: [0x15, 223],
    LocationName.donut_plains_1_green_block_3: [0x15, 224],
    LocationName.donut_plains_1_green_block_4: [0x15, 225],
    LocationName.donut_plains_1_green_block_5: [0x15, 226],
    LocationName.donut_plains_1_green_block_6: [0x15, 227],
    LocationName.donut_plains_1_green_block_7: [0x15, 228],
    LocationName.donut_plains_1_green_block_8: [0x15, 229],
    LocationName.donut_plains_1_green_block_9: [0x15, 230],
    LocationName.donut_plains_1_green_block_10: [0x15, 231],
    LocationName.donut_plains_1_green_block_11: [0x15, 232],
    LocationName.donut_plains_1_green_block_12: [0x15, 233],
    LocationName.donut_plains_1_green_block_13: [0x15, 234],
    LocationName.donut_plains_1_green_block_14: [0x15, 235],
    LocationName.donut_plains_1_green_block_15: [0x15, 236],
    LocationName.donut_plains_1_green_block_16: [0x15, 237],
    LocationName.donut_plains_1_yellow_block_1: [0x15, 238],
    LocationName.donut_plains_1_yellow_block_2: [0x15, 239],
    LocationName.donut_plains_1_yellow_block_3: [0x15, 240],
    LocationName.sunken_ghost_ship_powerup_block_1: [0x18, 241],
    LocationName.sunken_ghost_ship_star_block_1: [0x18, 242],
    LocationName.chocolate_castle_yellow_block_1: [0x1A, 243],
    LocationName.chocolate_castle_yellow_block_2: [0x1A, 244],
    LocationName.chocolate_castle_green_block_1: [0x1A, 245],
    LocationName.chocolate_fortress_powerup_block_1: [0x1B, 246],
    LocationName.chocolate_fortress_powerup_block_2: [0x1B, 247],
    LocationName.chocolate_fortress_coin_block_1: [0x1B, 248],
    LocationName.chocolate_fortress_coin_block_2: [0x1B, 249],
    LocationName.chocolate_fortress_green_block_1: [0x1B, 250],
    LocationName.chocolate_island_5_yoshi_block_1: [0x1C, 251],
    LocationName.chocolate_island_5_powerup_block_1: [0x1C, 252],
    LocationName.chocolate_island_5_life_block_1: [0x1C, 253],
    LocationName.chocolate_island_5_yellow_block_1: [0x1C, 254],
    LocationName.chocolate_island_4_yellow_block_1: [0x1D, 255],
    LocationName.chocolate_island_4_blue_pow_block_1: [0x1D, 256],
    LocationName.chocolate_island_4_powerup_block_1: [0x1D, 257],
    LocationName.forest_fortress_yellow_block_1: [0x1F, 258],
    LocationName.forest_fortress_powerup_block_1: [0x1F, 259],
    LocationName.forest_fortress_life_block_1: [0x1F, 260],
    LocationName.forest_fortress_life_block_2: [0x1F, 261],
    LocationName.forest_fortress_life_block_3: [0x1F, 262],
    LocationName.forest_fortress_life_block_4: [0x1F, 263],
    LocationName.forest_fortress_life_block_5: [0x1F, 264],
    LocationName.forest_fortress_life_block_6: [0x1F, 265],
    LocationName.forest_fortress_life_block_7: [0x1F, 266],
    LocationName.forest_fortress_life_block_8: [0x1F, 267],
    LocationName.forest_fortress_life_block_9: [0x1F, 268],
    LocationName.forest_castle_green_block_1: [0x20, 269],
    LocationName.chocolate_ghost_house_powerup_block_1: [0x21, 270],
    LocationName.chocolate_ghost_house_powerup_block_2: [0x21, 271],
    LocationName.chocolate_ghost_house_life_block_1: [0x21, 272],
    LocationName.chocolate_island_1_flying_block_1: [0x22, 273],
    LocationName.chocolate_island_1_flying_block_2: [0x22, 274],
    LocationName.chocolate_island_1_yoshi_block_1: [0x22, 275],
    LocationName.chocolate_island_1_green_block_1: [0x22, 276],
    LocationName.chocolate_island_1_life_block_1: [0x22, 277],
    LocationName.chocolate_island_3_powerup_block_1: [0x23, 278],
    LocationName.chocolate_island_3_powerup_block_2: [0x23, 279],
    LocationName.chocolate_island_3_powerup_block_3: [0x23, 280],
    LocationName.chocolate_island_3_green_block_1: [0x23, 281],
    LocationName.chocolate_island_3_bonus_block_1: [0x23, 282],
    LocationName.chocolate_island_3_vine_block_1: [0x23, 283],
    LocationName.chocolate_island_3_life_block_1: [0x23, 284],
    LocationName.chocolate_island_3_life_block_2: [0x23, 285],
    LocationName.chocolate_island_3_life_block_3: [0x23, 286],
    LocationName.chocolate_island_2_multi_coin_block_1: [0x24, 287],
    LocationName.chocolate_island_2_invis_coin_block_1: [0x24, 288],
    LocationName.chocolate_island_2_yoshi_block_1: [0x24, 289],
    LocationName.chocolate_island_2_coin_block_1: [0x24, 290],
    LocationName.chocolate_island_2_coin_block_2: [0x24, 291],
    LocationName.chocolate_island_2_multi_coin_block_2: [0x24, 292],
    LocationName.chocolate_island_2_powerup_block_1: [0x24, 293],
    LocationName.chocolate_island_2_blue_pow_block_1: [0x24, 294],
    LocationName.chocolate_island_2_yellow_block_1: [0x24, 295],
    LocationName.chocolate_island_2_yellow_block_2: [0x24, 296],
    LocationName.chocolate_island_2_green_block_1: [0x24, 297],
    LocationName.chocolate_island_2_green_block_2: [0x24, 298],
    LocationName.chocolate_island_2_green_block_3: [0x24, 299],
    LocationName.chocolate_island_2_green_block_4: [0x24, 300],
    LocationName.chocolate_island_2_green_block_5: [0x24, 301],
    LocationName.chocolate_island_2_green_block_6: [0x24, 302],
    LocationName.yoshis_island_castle_coin_block_1: [0x25, 303],
    LocationName.yoshis_island_castle_coin_block_2: [0x25, 304],
    LocationName.yoshis_island_castle_powerup_block_1: [0x25, 305],
    LocationName.yoshis_island_castle_coin_block_3: [0x25, 306],
    LocationName.yoshis_island_castle_coin_block_4: [0x25, 307],
    LocationName.yoshis_island_castle_flying_block_1: [0x25, 308],
    LocationName.yoshis_island_4_yellow_block_1: [0x26, 309],
    LocationName.yoshis_island_4_powerup_block_1: [0x26, 310],
    LocationName.yoshis_island_4_multi_coin_block_1: [0x26, 311],
    LocationName.yoshis_island_4_star_block_1: [0x26, 312],
    LocationName.yoshis_island_3_yellow_block_1: [0x27, 313],
    LocationName.yoshis_island_3_yellow_block_2: [0x27, 314],
    LocationName.yoshis_island_3_yellow_block_3: [0x27, 315],
    LocationName.yoshis_island_3_yellow_block_4: [0x27, 316],
    LocationName.yoshis_island_3_yellow_block_5: [0x27, 317],
    LocationName.yoshis_island_3_yellow_block_6: [0x27, 318],
    LocationName.yoshis_island_3_yellow_block_7: [0x27, 319],
    LocationName.yoshis_island_3_yellow_block_8: [0x27, 320],
    LocationName.yoshis_island_3_yellow_block_9: [0x27, 321],
    LocationName.yoshis_island_3_coin_block_1: [0x27, 322],
    LocationName.yoshis_island_3_yoshi_block_1: [0x27, 323],
    LocationName.yoshis_island_3_coin_block_2: [0x27, 324],
    LocationName.yoshis_island_3_powerup_block_1: [0x27, 325],
    LocationName.yoshis_island_3_yellow_block_10: [0x27, 326],
    LocationName.yoshis_island_3_yellow_block_11: [0x27, 327],
    LocationName.yoshis_island_3_yellow_block_12: [0x27, 328],
    LocationName.yoshis_island_3_bonus_block_1: [0x27, 329],
    LocationName.yoshis_island_1_flying_block_1: [0x29, 330],
    LocationName.yoshis_island_1_yellow_block_1: [0x29, 331],
    LocationName.yoshis_island_1_life_block_1: [0x29, 332],
    LocationName.yoshis_island_1_powerup_block_1: [0x29, 333],
    LocationName.yoshis_island_2_flying_block_1: [0x2A, 334],
    LocationName.yoshis_island_2_flying_block_2: [0x2A, 335],
    LocationName.yoshis_island_2_flying_block_3: [0x2A, 336],
    LocationName.yoshis_island_2_flying_block_4: [0x2A, 337],
    LocationName.yoshis_island_2_flying_block_5: [0x2A, 338],
    LocationName.yoshis_island_2_flying_block_6: [0x2A, 339],
    LocationName.yoshis_island_2_coin_block_1: [0x2A, 340],
    LocationName.yoshis_island_2_yellow_block_1: [0x2A, 341],
    LocationName.yoshis_island_2_coin_block_2: [0x2A, 342],
    LocationName.yoshis_island_2_coin_block_3: [0x2A, 343],
    LocationName.yoshis_island_2_yoshi_block_1: [0x2A, 344],
    LocationName.yoshis_island_2_coin_block_4: [0x2A, 345],
    LocationName.yoshis_island_2_yoshi_block_2: [0x2A, 346],
    LocationName.yoshis_island_2_coin_block_5: [0x2A, 347],
    LocationName.yoshis_island_2_vine_block_1: [0x2A, 348],
    LocationName.yoshis_island_2_yellow_block_2: [0x2A, 349],
    LocationName.vanilla_ghost_house_powerup_block_1: [0x2B, 350],
    LocationName.vanilla_ghost_house_vine_block_1: [0x2B, 351],
    LocationName.vanilla_ghost_house_powerup_block_2: [0x2B, 352],
    LocationName.vanilla_ghost_house_multi_coin_block_1: [0x2B, 353],
    LocationName.vanilla_ghost_house_blue_pow_block_1: [0x2B, 354],
    LocationName.vanilla_secret_1_coin_block_1: [0x2D, 355],
    LocationName.vanilla_secret_1_powerup_block_1: [0x2D, 356],
    LocationName.vanilla_secret_1_multi_coin_block_1: [0x2D, 357],
    LocationName.vanilla_secret_1_vine_block_1: [0x2D, 358],
    LocationName.vanilla_secret_1_vine_block_2: [0x2D, 359],
    LocationName.vanilla_secret_1_coin_block_2: [0x2D, 360],
    LocationName.vanilla_secret_1_coin_block_3: [0x2D, 361],
    LocationName.vanilla_secret_1_powerup_block_2: [0x2D, 362],
    LocationName.vanilla_dome_3_coin_block_1: [0x2E, 363],
    LocationName.vanilla_dome_3_flying_block_1: [0x2E, 364],
    LocationName.vanilla_dome_3_flying_block_2: [0x2E, 365],
    LocationName.vanilla_dome_3_powerup_block_1: [0x2E, 366],
    LocationName.vanilla_dome_3_flying_block_3: [0x2E, 367],
    LocationName.vanilla_dome_3_invis_coin_block_1: [0x2E, 368],
    LocationName.vanilla_dome_3_powerup_block_2: [0x2E, 369],
    LocationName.vanilla_dome_3_multi_coin_block_1: [0x2E, 370],
    LocationName.vanilla_dome_3_powerup_block_3: [0x2E, 371],
    LocationName.vanilla_dome_3_yoshi_block_1: [0x2E, 372],
    LocationName.vanilla_dome_3_powerup_block_4: [0x2E, 373],
    LocationName.vanilla_dome_3_pswitch_coin_block_1: [0x2E, 374],
    LocationName.vanilla_dome_3_pswitch_coin_block_2: [0x2E, 375],
    LocationName.vanilla_dome_3_pswitch_coin_block_3: [0x2E, 376],
    LocationName.vanilla_dome_3_pswitch_coin_block_4: [0x2E, 377],
    LocationName.vanilla_dome_3_pswitch_coin_block_5: [0x2E, 378],
    LocationName.vanilla_dome_3_pswitch_coin_block_6: [0x2E, 379],
    LocationName.donut_secret_2_directional_coin_block_1: [0x2F, 380],
    LocationName.donut_secret_2_vine_block_1: [0x2F, 381],
    LocationName.donut_secret_2_star_block_1: [0x2F, 382],
    LocationName.donut_secret_2_powerup_block_1: [0x2F, 383],
    LocationName.donut_secret_2_star_block_2: [0x2F, 384],
    LocationName.valley_of_bowser_4_yellow_block_1: [0x33, 385],
    LocationName.valley_of_bowser_4_powerup_block_1: [0x33, 386],
    LocationName.valley_of_bowser_4_vine_block_1: [0x33, 387],
    LocationName.valley_of_bowser_4_yoshi_block_1: [0x33, 388],
    LocationName.valley_of_bowser_4_life_block_1: [0x33, 389],
    LocationName.valley_of_bowser_4_powerup_block_2: [0x33, 390],
    LocationName.valley_castle_yellow_block_1: [0x34, 391],
    LocationName.valley_castle_yellow_block_2: [0x34, 392],
    LocationName.valley_castle_green_block_1: [0x34, 393],
    LocationName.valley_fortress_green_block_1: [0x35, 394],
    LocationName.valley_fortress_yellow_block_1: [0x35, 395],
    LocationName.valley_of_bowser_3_powerup_block_1: [0x37, 396],
    LocationName.valley_of_bowser_3_powerup_block_2: [0x37, 397],
    LocationName.valley_ghost_house_pswitch_coin_block_1: [0x38, 398],
    LocationName.valley_ghost_house_multi_coin_block_1: [0x38, 399],
    LocationName.valley_ghost_house_powerup_block_1: [0x38, 400],
    LocationName.valley_ghost_house_directional_coin_block_1: [0x38, 401],
    LocationName.valley_of_bowser_2_powerup_block_1: [0x39, 402],
    LocationName.valley_of_bowser_2_yellow_block_1: [0x39, 403],
    LocationName.valley_of_bowser_2_powerup_block_2: [0x39, 404],
    LocationName.valley_of_bowser_2_wings_block_1: [0x39, 405],
    LocationName.valley_of_bowser_1_green_block_1: [0x3A, 406],
    LocationName.valley_of_bowser_1_invis_coin_block_1: [0x3A, 407],
    LocationName.valley_of_bowser_1_invis_coin_block_2: [0x3A, 408],
    LocationName.valley_of_bowser_1_invis_coin_block_3: [0x3A, 409],
    LocationName.valley_of_bowser_1_yellow_block_1: [0x3A, 410],
    LocationName.valley_of_bowser_1_yellow_block_2: [0x3A, 411],
    LocationName.valley_of_bowser_1_yellow_block_3: [0x3A, 412],
    LocationName.valley_of_bowser_1_yellow_block_4: [0x3A, 413],
    LocationName.valley_of_bowser_1_vine_block_1: [0x3A, 414],
    LocationName.chocolate_secret_powerup_block_1: [0x3B, 415],
    LocationName.chocolate_secret_powerup_block_2: [0x3B, 416],
    LocationName.vanilla_dome_2_coin_block_1: [0x3C, 417],
    LocationName.vanilla_dome_2_powerup_block_1: [0x3C, 418],
    LocationName.vanilla_dome_2_coin_block_2: [0x3C, 419],
    LocationName.vanilla_dome_2_coin_block_3: [0x3C, 420],
    LocationName.vanilla_dome_2_vine_block_1: [0x3C, 421],
    LocationName.vanilla_dome_2_invis_life_block_1: [0x3C, 422],
    LocationName.vanilla_dome_2_coin_block_4: [0x3C, 423],
    LocationName.vanilla_dome_2_coin_block_5: [0x3C, 424],
    LocationName.vanilla_dome_2_powerup_block_2: [0x3C, 425],
    LocationName.vanilla_dome_2_powerup_block_3: [0x3C, 426],
    LocationName.vanilla_dome_2_powerup_block_4: [0x3C, 427],
    LocationName.vanilla_dome_2_powerup_block_5: [0x3C, 428],
    LocationName.vanilla_dome_2_multi_coin_block_1: [0x3C, 429],
    LocationName.vanilla_dome_2_multi_coin_block_2: [0x3C, 430],
    LocationName.vanilla_dome_4_powerup_block_1: [0x3D, 431],
    LocationName.vanilla_dome_4_powerup_block_2: [0x3D, 432],
    LocationName.vanilla_dome_4_coin_block_1: [0x3D, 433],
    LocationName.vanilla_dome_4_coin_block_2: [0x3D, 434],
    LocationName.vanilla_dome_4_coin_block_3: [0x3D, 435],
    LocationName.vanilla_dome_4_life_block_1: [0x3D, 436],
    LocationName.vanilla_dome_4_coin_block_4: [0x3D, 437],
    LocationName.vanilla_dome_4_coin_block_5: [0x3D, 438],
    LocationName.vanilla_dome_4_coin_block_6: [0x3D, 439],
    LocationName.vanilla_dome_4_coin_block_7: [0x3D, 440],
    LocationName.vanilla_dome_4_coin_block_8: [0x3D, 441],
    LocationName.vanilla_dome_1_flying_block_1: [0x3E, 442],
    LocationName.vanilla_dome_1_powerup_block_1: [0x3E, 443],
    LocationName.vanilla_dome_1_powerup_block_2: [0x3E, 444],
    LocationName.vanilla_dome_1_coin_block_1: [0x3E, 445],
    LocationName.vanilla_dome_1_life_block_1: [0x3E, 446],
    LocationName.vanilla_dome_1_powerup_block_3: [0x3E, 447],
    LocationName.vanilla_dome_1_vine_block_1: [0x3E, 448],
    LocationName.vanilla_dome_1_star_block_1: [0x3E, 449],
    LocationName.vanilla_dome_1_powerup_block_4: [0x3E, 450],
    LocationName.vanilla_dome_1_coin_block_2: [0x3E, 451],
    LocationName.vanilla_dome_castle_life_block_1: [0x40, 452],
    LocationName.vanilla_dome_castle_life_block_2: [0x40, 453],
    LocationName.vanilla_dome_castle_powerup_block_1: [0x40, 454],
    LocationName.vanilla_dome_castle_life_block_3: [0x40, 455],
    LocationName.vanilla_dome_castle_green_block_1: [0x40, 456],
    LocationName.forest_ghost_house_coin_block_1: [0x41, 457],
    LocationName.forest_ghost_house_powerup_block_1: [0x41, 458],
    LocationName.forest_ghost_house_flying_block_1: [0x41, 459],
    LocationName.forest_ghost_house_powerup_block_2: [0x41, 460],
    LocationName.forest_ghost_house_life_block_1: [0x41, 461],
    LocationName.forest_of_illusion_1_powerup_block_1: [0x42, 462],
    LocationName.forest_of_illusion_1_yoshi_block_1: [0x42, 463],
    LocationName.forest_of_illusion_1_powerup_block_2: [0x42, 464],
    LocationName.forest_of_illusion_1_key_block_1: [0x42, 465],
    LocationName.forest_of_illusion_1_life_block_1: [0x42, 466],
    LocationName.forest_of_illusion_4_multi_coin_block_1: [0x43, 467],
    LocationName.forest_of_illusion_4_coin_block_1: [0x43, 468],
    LocationName.forest_of_illusion_4_coin_block_2: [0x43, 469],
    LocationName.forest_of_illusion_4_coin_block_3: [0x43, 470],
    LocationName.forest_of_illusion_4_coin_block_4: [0x43, 471],
    LocationName.forest_of_illusion_4_powerup_block_1: [0x43, 472],
    LocationName.forest_of_illusion_4_coin_block_5: [0x43, 473],
    LocationName.forest_of_illusion_4_coin_block_6: [0x43, 474],
    LocationName.forest_of_illusion_4_coin_block_7: [0x43, 475],
    LocationName.forest_of_illusion_4_powerup_block_2: [0x43, 476],
    LocationName.forest_of_illusion_4_coin_block_8: [0x43, 477],
    LocationName.forest_of_illusion_4_coin_block_9: [0x43, 478],
    LocationName.forest_of_illusion_4_coin_block_10: [0x43, 479],
    LocationName.forest_of_illusion_2_green_block_1: [0x44, 480],
    LocationName.forest_of_illusion_2_powerup_block_1: [0x44, 481],
    LocationName.forest_of_illusion_2_invis_coin_block_1: [0x44, 482],
    LocationName.forest_of_illusion_2_invis_coin_block_2: [0x44, 483],
    LocationName.forest_of_illusion_2_invis_life_block_1: [0x44, 484],
    LocationName.forest_of_illusion_2_invis_coin_block_3: [0x44, 485],
    LocationName.forest_of_illusion_2_yellow_block_1: [0x44, 486],
    LocationName.forest_secret_powerup_block_1: [0x46, 487],
    LocationName.forest_secret_powerup_block_2: [0x46, 488],
    LocationName.forest_secret_life_block_1: [0x46, 489],
    LocationName.forest_of_illusion_3_yoshi_block_1: [0x47, 490],
    LocationName.forest_of_illusion_3_coin_block_1: [0x47, 491],
    LocationName.forest_of_illusion_3_multi_coin_block_1: [0x47, 492],
    LocationName.forest_of_illusion_3_coin_block_2: [0x47, 493],
    LocationName.forest_of_illusion_3_multi_coin_block_2: [0x47, 494],
    LocationName.forest_of_illusion_3_coin_block_3: [0x47, 495],
    LocationName.forest_of_illusion_3_coin_block_4: [0x47, 496],
    LocationName.forest_of_illusion_3_coin_block_5: [0x47, 497],
    LocationName.forest_of_illusion_3_coin_block_6: [0x47, 498],
    LocationName.forest_of_illusion_3_coin_block_7: [0x47, 499],
    LocationName.forest_of_illusion_3_coin_block_8: [0x47, 500],
    LocationName.forest_of_illusion_3_coin_block_9: [0x47, 501],
    LocationName.forest_of_illusion_3_coin_block_10: [0x47, 502],
    LocationName.forest_of_illusion_3_coin_block_11: [0x47, 503],
    LocationName.forest_of_illusion_3_coin_block_12: [0x47, 504],
    LocationName.forest_of_illusion_3_coin_block_13: [0x47, 505],
    LocationName.forest_of_illusion_3_coin_block_14: [0x47, 506],
    LocationName.forest_of_illusion_3_coin_block_15: [0x47, 507],
    LocationName.forest_of_illusion_3_coin_block_16: [0x47, 508],
    LocationName.forest_of_illusion_3_coin_block_17: [0x47, 509],
    LocationName.forest_of_illusion_3_coin_block_18: [0x47, 510],
    LocationName.forest_of_illusion_3_coin_block_19: [0x47, 511],
    LocationName.forest_of_illusion_3_coin_block_20: [0x47, 512],
    LocationName.forest_of_illusion_3_coin_block_21: [0x47, 513],
    LocationName.forest_of_illusion_3_coin_block_22: [0x47, 514],
    LocationName.forest_of_illusion_3_coin_block_23: [0x47, 515],
    LocationName.forest_of_illusion_3_coin_block_24: [0x47, 516],
    LocationName.special_zone_8_yoshi_block_1: [0x49, 517],
    LocationName.special_zone_8_coin_block_1: [0x49, 518],
    LocationName.special_zone_8_coin_block_2: [0x49, 519],
    LocationName.special_zone_8_coin_block_3: [0x49, 520],
    LocationName.special_zone_8_coin_block_4: [0x49, 521],
    LocationName.special_zone_8_coin_block_5: [0x49, 522],
    LocationName.special_zone_8_blue_pow_block_1: [0x49, 523],
    LocationName.special_zone_8_powerup_block_1: [0x49, 524],
    LocationName.special_zone_8_star_block_1: [0x49, 525],
    LocationName.special_zone_8_coin_block_6: [0x49, 526],
    LocationName.special_zone_8_coin_block_7: [0x49, 527],
    LocationName.special_zone_8_coin_block_8: [0x49, 528],
    LocationName.special_zone_8_coin_block_9: [0x49, 529],
    LocationName.special_zone_8_coin_block_10: [0x49, 530],
    LocationName.special_zone_8_coin_block_11: [0x49, 531],
    LocationName.special_zone_8_coin_block_12: [0x49, 532],
    LocationName.special_zone_8_coin_block_13: [0x49, 533],
    LocationName.special_zone_8_coin_block_14: [0x49, 534],
    LocationName.special_zone_8_coin_block_15: [0x49, 535],
    LocationName.special_zone_8_coin_block_16: [0x49, 536],
    LocationName.special_zone_8_coin_block_17: [0x49, 537],
    LocationName.special_zone_8_coin_block_18: [0x49, 538],
    LocationName.special_zone_8_multi_coin_block_1: [0x49, 539],
    LocationName.special_zone_8_coin_block_19: [0x49, 540],
    LocationName.special_zone_8_coin_block_20: [0x49, 541],
    LocationName.special_zone_8_coin_block_21: [0x49, 542],
    LocationName.special_zone_8_coin_block_22: [0x49, 543],
    LocationName.special_zone_8_coin_block_23: [0x49, 544],
    LocationName.special_zone_8_powerup_block_2: [0x49, 545],
    LocationName.special_zone_8_flying_block_1: [0x49, 546],
    LocationName.special_zone_7_powerup_block_1: [0x4A, 547],
    LocationName.special_zone_7_yoshi_block_1: [0x4A, 548],
    LocationName.special_zone_7_coin_block_1: [0x4A, 549],
    LocationName.special_zone_7_powerup_block_2: [0x4A, 550],
    LocationName.special_zone_7_coin_block_2: [0x4A, 551],
    LocationName.special_zone_6_powerup_block_1: [0x4B, 552],
    LocationName.special_zone_6_coin_block_1: [0x4B, 553],
    LocationName.special_zone_6_coin_block_2: [0x4B, 554],
    LocationName.special_zone_6_yoshi_block_1: [0x4B, 555],
    LocationName.special_zone_6_life_block_1: [0x4B, 556],
    LocationName.special_zone_6_multi_coin_block_1: [0x4B, 557],
    LocationName.special_zone_6_coin_block_3: [0x4B, 558],
    LocationName.special_zone_6_coin_block_4: [0x4B, 559],
    LocationName.special_zone_6_coin_block_5: [0x4B, 560],
    LocationName.special_zone_6_coin_block_6: [0x4B, 561],
    LocationName.special_zone_6_coin_block_7: [0x4B, 562],
    LocationName.special_zone_6_coin_block_8: [0x4B, 563],
    LocationName.special_zone_6_coin_block_9: [0x4B, 564],
    LocationName.special_zone_6_coin_block_10: [0x4B, 565],
    LocationName.special_zone_6_coin_block_11: [0x4B, 566],
    LocationName.special_zone_6_coin_block_12: [0x4B, 567],
    LocationName.special_zone_6_coin_block_13: [0x4B, 568],
    LocationName.special_zone_6_coin_block_14: [0x4B, 569],
    LocationName.special_zone_6_coin_block_15: [0x4B, 570],
    LocationName.special_zone_6_coin_block_16: [0x4B, 571],
    LocationName.special_zone_6_coin_block_17: [0x4B, 572],
    LocationName.special_zone_6_coin_block_18: [0x4B, 573],
    LocationName.special_zone_6_coin_block_19: [0x4B, 574],
    LocationName.special_zone_6_coin_block_20: [0x4B, 575],
    LocationName.special_zone_6_coin_block_21: [0x4B, 576],
    LocationName.special_zone_6_coin_block_22: [0x4B, 577],
    LocationName.special_zone_6_coin_block_23: [0x4B, 578],
    LocationName.special_zone_6_coin_block_24: [0x4B, 579],
    LocationName.special_zone_6_coin_block_25: [0x4B, 580],
    LocationName.special_zone_6_coin_block_26: [0x4B, 581],
    LocationName.special_zone_6_coin_block_27: [0x4B, 582],
    LocationName.special_zone_6_coin_block_28: [0x4B, 583],
    LocationName.special_zone_6_powerup_block_2: [0x4B, 584],
    LocationName.special_zone_6_coin_block_29: [0x4B, 585],
    LocationName.special_zone_6_coin_block_30: [0x4B, 586],
    LocationName.special_zone_6_coin_block_31: [0x4B, 587],
    LocationName.special_zone_6_coin_block_32: [0x4B, 588],
    LocationName.special_zone_6_coin_block_33: [0x4B, 589],
    LocationName.special_zone_5_yoshi_block_1: [0x4C, 590],
    LocationName.special_zone_1_vine_block_1: [0x4E, 591],
    LocationName.special_zone_1_vine_block_2: [0x4E, 592],
    LocationName.special_zone_1_vine_block_3: [0x4E, 593],
    LocationName.special_zone_1_vine_block_4: [0x4E, 594],
    LocationName.special_zone_1_life_block_1: [0x4E, 595],
    LocationName.special_zone_1_vine_block_5: [0x4E, 596],
    LocationName.special_zone_1_blue_pow_block_1: [0x4E, 597],
    LocationName.special_zone_1_vine_block_6: [0x4E, 598],
    LocationName.special_zone_1_powerup_block_1: [0x4E, 599],
    LocationName.special_zone_1_pswitch_coin_block_1: [0x4E, 600],
    LocationName.special_zone_1_pswitch_coin_block_2: [0x4E, 601],
    LocationName.special_zone_1_pswitch_coin_block_3: [0x4E, 602],
    LocationName.special_zone_1_pswitch_coin_block_4: [0x4E, 603],
    LocationName.special_zone_1_pswitch_coin_block_5: [0x4E, 604],
    LocationName.special_zone_1_pswitch_coin_block_6: [0x4E, 605],
    LocationName.special_zone_1_pswitch_coin_block_7: [0x4E, 606],
    LocationName.special_zone_1_pswitch_coin_block_8: [0x4E, 607],
    LocationName.special_zone_1_pswitch_coin_block_9: [0x4E, 608],
    LocationName.special_zone_1_pswitch_coin_block_10: [0x4E, 609],
    LocationName.special_zone_1_pswitch_coin_block_11: [0x4E, 610],
    LocationName.special_zone_1_pswitch_coin_block_12: [0x4E, 611],
    LocationName.special_zone_1_pswitch_coin_block_13: [0x4E, 612],
    LocationName.special_zone_2_powerup_block_1: [0x4F, 613],
    LocationName.special_zone_2_coin_block_1: [0x4F, 614],
    LocationName.special_zone_2_coin_block_2: [0x4F, 615],
    LocationName.special_zone_2_powerup_block_2: [0x4F, 616],
    LocationName.special_zone_2_coin_block_3: [0x4F, 617],
    LocationName.special_zone_2_coin_block_4: [0x4F, 618],
    LocationName.special_zone_2_powerup_block_3: [0x4F, 619],
    LocationName.special_zone_2_multi_coin_block_1: [0x4F, 620],
    LocationName.special_zone_2_coin_block_5: [0x4F, 621],
    LocationName.special_zone_2_coin_block_6: [0x4F, 622],
    LocationName.special_zone_3_powerup_block_1: [0x50, 623],
    LocationName.special_zone_3_yoshi_block_1: [0x50, 624],
    LocationName.special_zone_3_wings_block_1: [0x50, 625],
    LocationName.special_zone_4_powerup_block_1: [0x51, 626],
    LocationName.special_zone_4_star_block_1: [0x51, 627],
    LocationName.star_road_2_star_block_1: [0x54, 628],
    LocationName.star_road_3_key_block_1: [0x56, 629],
    LocationName.star_road_4_powerup_block_1: [0x59, 630],
    LocationName.star_road_4_green_block_1: [0x59, 631],
    LocationName.star_road_4_green_block_2: [0x59, 632],
    LocationName.star_road_4_green_block_3: [0x59, 633],
    LocationName.star_road_4_green_block_4: [0x59, 634],
    LocationName.star_road_4_green_block_5: [0x59, 635],
    LocationName.star_road_4_green_block_6: [0x59, 636],
    LocationName.star_road_4_green_block_7: [0x59, 637],
    LocationName.star_road_4_key_block_1: [0x59, 638],
    LocationName.star_road_5_directional_coin_block_1: [0x5A, 639],
    LocationName.star_road_5_life_block_1: [0x5A, 640],
    LocationName.star_road_5_vine_block_1: [0x5A, 641],
    LocationName.star_road_5_yellow_block_1: [0x5A, 642],
    LocationName.star_road_5_yellow_block_2: [0x5A, 643],
    LocationName.star_road_5_yellow_block_3: [0x5A, 644],
    LocationName.star_road_5_yellow_block_4: [0x5A, 645],
    LocationName.star_road_5_yellow_block_5: [0x5A, 646],
    LocationName.star_road_5_yellow_block_6: [0x5A, 647],
    LocationName.star_road_5_yellow_block_7: [0x5A, 648],
    LocationName.star_road_5_yellow_block_8: [0x5A, 649],
    LocationName.star_road_5_yellow_block_9: [0x5A, 650],
    LocationName.star_road_5_yellow_block_10: [0x5A, 651],
    LocationName.star_road_5_yellow_block_11: [0x5A, 652],
    LocationName.star_road_5_yellow_block_12: [0x5A, 653],
    LocationName.star_road_5_yellow_block_13: [0x5A, 654],
    LocationName.star_road_5_yellow_block_14: [0x5A, 655],
    LocationName.star_road_5_yellow_block_15: [0x5A, 656],
    LocationName.star_road_5_yellow_block_16: [0x5A, 657],
    LocationName.star_road_5_yellow_block_17: [0x5A, 658],
    LocationName.star_road_5_yellow_block_18: [0x5A, 659],
    LocationName.star_road_5_yellow_block_19: [0x5A, 660],
    LocationName.star_road_5_yellow_block_20: [0x5A, 661],
    LocationName.star_road_5_green_block_1: [0x5A, 662],
    LocationName.star_road_5_green_block_2: [0x5A, 663],
    LocationName.star_road_5_green_block_3: [0x5A, 664],
    LocationName.star_road_5_green_block_4: [0x5A, 665],
    LocationName.star_road_5_green_block_5: [0x5A, 666],
    LocationName.star_road_5_green_block_6: [0x5A, 667],
    LocationName.star_road_5_green_block_7: [0x5A, 668],
    LocationName.star_road_5_green_block_8: [0x5A, 669],
    LocationName.star_road_5_green_block_9: [0x5A, 670],
    LocationName.star_road_5_green_block_10: [0x5A, 671],
    LocationName.star_road_5_green_block_11: [0x5A, 672],
    LocationName.star_road_5_green_block_12: [0x5A, 673],
    LocationName.star_road_5_green_block_13: [0x5A, 674],
    LocationName.star_road_5_green_block_14: [0x5A, 675],
    LocationName.star_road_5_green_block_15: [0x5A, 676],
    LocationName.star_road_5_green_block_16: [0x5A, 677],
    LocationName.star_road_5_green_block_17: [0x5A, 678],
    LocationName.star_road_5_green_block_18: [0x5A, 679],
    LocationName.star_road_5_green_block_19: [0x5A, 680],
    LocationName.star_road_5_green_block_20: [0x5A, 681]
}

def generate_level_list(world: World):

    if not world.options.level_shuffle:
        out_level_list = full_level_list.copy()
        out_level_list[0x00] = 0x03
        out_level_list[0x11] = 0x28

        if world.options.bowser_castle_doors == "fast":
            out_level_list[0x41] = 0x82
            out_level_list[0x42] = 0x32
        elif world.options.bowser_castle_doors == "slow":
            out_level_list[0x41] = 0x31
            out_level_list[0x42] = 0x81

        return out_level_list

    shuffled_level_list = []
    easy_castle_fortress_levels_copy = easy_castle_fortress_levels.copy()
    world.random.shuffle(easy_castle_fortress_levels_copy)
    hard_castle_fortress_levels_copy = hard_castle_fortress_levels.copy()
    world.random.shuffle(hard_castle_fortress_levels_copy)
    easy_single_levels_copy = easy_single_levels.copy()
    world.random.shuffle(easy_single_levels_copy)
    hard_single_levels_copy = hard_single_levels.copy()
    world.random.shuffle(hard_single_levels_copy)
    special_zone_levels_copy = special_zone_levels.copy()
    easy_double_levels_copy = easy_double_levels.copy()
    world.random.shuffle(easy_double_levels_copy)
    hard_double_levels_copy = hard_double_levels.copy()
    world.random.shuffle(hard_double_levels_copy)
    switch_palace_levels_copy = switch_palace_levels.copy()
    world.random.shuffle(switch_palace_levels_copy)

    # Yoshi's Island
    shuffled_level_list.append(0x03)
    shuffled_level_list.append(easy_single_levels_copy.pop(0))
    shuffled_level_list.append(0x14)
    shuffled_level_list.append(easy_single_levels_copy.pop(0))
    shuffled_level_list.append(easy_single_levels_copy.pop(0))
    shuffled_level_list.append(easy_single_levels_copy.pop(0))
    shuffled_level_list.append(easy_castle_fortress_levels_copy.pop(0))

    # Donut Plains
    shuffled_level_list.append(easy_double_levels_copy.pop(0))
    shuffled_level_list.append(easy_double_levels_copy.pop(0))
    shuffled_level_list.append(easy_double_levels_copy.pop(0))
    shuffled_level_list.append(0x08)
    shuffled_level_list.append(easy_double_levels_copy.pop(0))
    shuffled_level_list.append(easy_double_levels_copy.pop(0))
    shuffled_level_list.append(easy_single_levels_copy.pop(0))
    shuffled_level_list.append(easy_single_levels_copy.pop(0))
    shuffled_level_list.append(easy_single_levels_copy.pop(0))
    shuffled_level_list.append(easy_castle_fortress_levels_copy.pop(0))
    shuffled_level_list.append(0x28)
    shuffled_level_list.append(0x16)

    single_levels_copy = (easy_single_levels_copy.copy() + hard_single_levels_copy.copy())
    if not world.options.exclude_special_zone:
        single_levels_copy.extend(special_zone_levels_copy)
    world.random.shuffle(single_levels_copy)

    castle_fortress_levels_copy = (easy_castle_fortress_levels_copy.copy() + hard_castle_fortress_levels_copy.copy())
    world.random.shuffle(castle_fortress_levels_copy)

    double_levels_copy = (easy_double_levels_copy.copy() + hard_double_levels_copy.copy())
    world.random.shuffle(double_levels_copy)

    # Vanilla Dome
    shuffled_level_list.append(double_levels_copy.pop(0))
    shuffled_level_list.append(double_levels_copy.pop(0))
    shuffled_level_list.append(double_levels_copy.pop(0))
    shuffled_level_list.append(single_levels_copy.pop(0))
    shuffled_level_list.append(single_levels_copy.pop(0))
    shuffled_level_list.append(single_levels_copy.pop(0))
    shuffled_level_list.append(0x3F)
    shuffled_level_list.append(single_levels_copy.pop(0))
    shuffled_level_list.append(single_levels_copy.pop(0))
    shuffled_level_list.append(castle_fortress_levels_copy.pop(0))
    shuffled_level_list.append(castle_fortress_levels_copy.pop(0))
    shuffled_level_list.append(0x2C)

    # Twin Bridges
    shuffled_level_list.append(single_levels_copy.pop(0))
    shuffled_level_list.append(single_levels_copy.pop(0))
    shuffled_level_list.append(double_levels_copy.pop(0))
    shuffled_level_list.append(single_levels_copy.pop(0))
    shuffled_level_list.append(single_levels_copy.pop(0))
    shuffled_level_list.append(castle_fortress_levels_copy.pop(0))
    shuffled_level_list.append(0x12)

    # Forest of Illusion
    shuffled_level_list.append(double_levels_copy.pop(0))
    shuffled_level_list.append(double_levels_copy.pop(0))
    shuffled_level_list.append(double_levels_copy.pop(0))
    shuffled_level_list.append(double_levels_copy.pop(0))
    shuffled_level_list.append(double_levels_copy.pop(0))
    shuffled_level_list.append(single_levels_copy.pop(0))
    shuffled_level_list.append(0x45)
    shuffled_level_list.append(castle_fortress_levels_copy.pop(0))
    shuffled_level_list.append(castle_fortress_levels_copy.pop(0))
    shuffled_level_list.append(0x1E)

    # Chocolate Island
    shuffled_level_list.append(single_levels_copy.pop(0))
    shuffled_level_list.append(double_levels_copy.pop(0))
    shuffled_level_list.append(double_levels_copy.pop(0))
    shuffled_level_list.append(single_levels_copy.pop(0))
    shuffled_level_list.append(single_levels_copy.pop(0))
    shuffled_level_list.append(single_levels_copy.pop(0))
    shuffled_level_list.append(castle_fortress_levels_copy.pop(0))
    shuffled_level_list.append(single_levels_copy.pop(0))
    shuffled_level_list.append(castle_fortress_levels_copy.pop(0))

    # Valley of Bowser
    shuffled_level_list.append(0x18)
    shuffled_level_list.append(single_levels_copy.pop(0))
    shuffled_level_list.append(double_levels_copy.pop(0))
    shuffled_level_list.append(single_levels_copy.pop(0))
    shuffled_level_list.append(double_levels_copy.pop(0))
    shuffled_level_list.append(double_levels_copy.pop(0))
    shuffled_level_list.append(castle_fortress_levels_copy.pop(0))
    shuffled_level_list.append(castle_fortress_levels_copy.pop(0))

    # Front/Back Door
    if world.options.bowser_castle_doors == "fast":
        shuffled_level_list.append(0x82)
        shuffled_level_list.append(0x32)
    elif world.options.bowser_castle_doors == "slow":
        shuffled_level_list.append(0x31)
        shuffled_level_list.append(0x81)
    else:
        shuffled_level_list.append(0x31)
        shuffled_level_list.append(0x32)

    shuffled_level_list.append(0x30)

    # Star Road
    shuffled_level_list.append(0x5B)
    shuffled_level_list.append(double_levels_copy.pop(0))
    shuffled_level_list.append(0x53)
    shuffled_level_list.append(double_levels_copy.pop(0))
    shuffled_level_list.append(0x52)
    shuffled_level_list.append(double_levels_copy.pop(0))
    shuffled_level_list.append(0x57)
    shuffled_level_list.append(double_levels_copy.pop(0))
    shuffled_level_list.append(0x5C)
    shuffled_level_list.append(double_levels_copy.pop(0))
    shuffled_level_list.append(0x55)

    # Special Zone
    shuffled_level_list.append(0x4D)
    if not world.options.exclude_special_zone:
        shuffled_level_list.append(single_levels_copy.pop(0))
        shuffled_level_list.append(single_levels_copy.pop(0))
        shuffled_level_list.append(single_levels_copy.pop(0))
        shuffled_level_list.append(single_levels_copy.pop(0))
        shuffled_level_list.append(single_levels_copy.pop(0))
        shuffled_level_list.append(single_levels_copy.pop(0))
        shuffled_level_list.append(single_levels_copy.pop(0))
        shuffled_level_list.append(single_levels_copy.pop(0))
    else:
        shuffled_level_list.extend(special_zone_levels_copy)
    shuffled_level_list.append(0x48)

    return shuffled_level_list
