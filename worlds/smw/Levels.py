
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
    LocationName.yoshis_island_2_exit_1:  [0x2A, 0],
    LocationName.yoshis_island_2_dragon:  [0x2A, 2],
    LocationName.yoshis_island_3_exit_1:  [0x27, 0],
    LocationName.yoshis_island_3_dragon:  [0x27, 2],
    LocationName.yoshis_island_4_exit_1:  [0x26, 0],
    LocationName.yoshis_island_4_dragon:  [0x26, 2],
    LocationName.yoshis_island_castle:    [0x25, 0],
    LocationName.yoshis_island_koopaling: [0x25, 0],
    LocationName.yellow_switch_palace:    [0x14, 0],

    LocationName.donut_plains_1_exit_1:     [0x15, 0],
    LocationName.donut_plains_1_exit_2:     [0x15, 1],
    LocationName.donut_plains_1_dragon:     [0x15, 2],
    LocationName.donut_plains_2_exit_1:     [0x09, 0],
    LocationName.donut_plains_2_exit_2:     [0x09, 1],
    LocationName.donut_plains_2_dragon:     [0x09, 2],
    LocationName.donut_plains_3_exit_1:     [0x05, 0],
    LocationName.donut_plains_3_dragon:     [0x05, 2],
    LocationName.donut_plains_4_exit_1:     [0x06, 0],
    LocationName.donut_plains_4_dragon:     [0x06, 2],
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
    LocationName.vanilla_dome_4_exit_1:      [0x3D, 0],
    LocationName.vanilla_dome_4_dragon:      [0x3D, 2],
    LocationName.vanilla_secret_1_exit_1:    [0x2D, 0],
    LocationName.vanilla_secret_1_exit_2:    [0x2D, 1],
    LocationName.vanilla_secret_1_dragon:    [0x2D, 2],
    LocationName.vanilla_secret_2_exit_1:    [0x01, 0],
    LocationName.vanilla_secret_2_dragon:    [0x01, 2],
    LocationName.vanilla_secret_3_exit_1:    [0x02, 0],
    LocationName.vanilla_secret_3_dragon:    [0x02, 2],
    LocationName.vanilla_ghost_house_exit_1: [0x2B, 0],
    LocationName.vanilla_ghost_house_dragon: [0x2B, 2],
    LocationName.vanilla_fortress:           [0x0B, 0],
    LocationName.vanilla_reznor:             [0x0B, 0],
    LocationName.vanilla_dome_castle:        [0x40, 0],
    LocationName.vanilla_dome_koopaling:     [0x40, 0],
    LocationName.red_switch_palace:          [0x3F, 0],

    LocationName.butter_bridge_1_exit_1: [0x0C, 0],
    LocationName.butter_bridge_1_dragon: [0x0C, 2],
    LocationName.butter_bridge_2_exit_1: [0x0D, 0],
    LocationName.butter_bridge_2_dragon: [0x0D, 2],
    LocationName.cheese_bridge_exit_1:   [0x0F, 0],
    LocationName.cheese_bridge_exit_2:   [0x0F, 1],
    LocationName.cheese_bridge_dragon:   [0x0F, 2],
    LocationName.cookie_mountain_exit_1: [0x10, 0],
    LocationName.cookie_mountain_dragon: [0x10, 2],
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
    LocationName.forest_of_illusion_4_exit_1: [0x43, 0],
    LocationName.forest_of_illusion_4_exit_2: [0x43, 1],
    LocationName.forest_of_illusion_4_dragon: [0x43, 2],
    LocationName.forest_ghost_house_exit_1:   [0x41, 0],
    LocationName.forest_ghost_house_exit_2:   [0x41, 1],
    LocationName.forest_ghost_house_dragon:   [0x41, 2],
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
    LocationName.chocolate_island_2_exit_1:    [0x24, 0],
    LocationName.chocolate_island_2_exit_2:    [0x24, 1],
    LocationName.chocolate_island_2_dragon:    [0x24, 2],
    LocationName.chocolate_island_3_exit_1:    [0x23, 0],
    LocationName.chocolate_island_3_exit_2:    [0x23, 1],
    LocationName.chocolate_island_3_dragon:    [0x23, 2],
    LocationName.chocolate_island_4_exit_1:    [0x1D, 0],
    LocationName.chocolate_island_4_dragon:    [0x1D, 2],
    LocationName.chocolate_island_5_exit_1:    [0x1C, 0],
    LocationName.chocolate_island_5_dragon:    [0x1C, 2],
    LocationName.chocolate_ghost_house_exit_1: [0x21, 0],
    LocationName.chocolate_secret_exit_1:      [0x3B, 0],
    LocationName.chocolate_fortress:           [0x1B, 0],
    LocationName.chocolate_reznor:             [0x1B, 0],
    LocationName.chocolate_castle:             [0x1A, 0],
    LocationName.chocolate_koopaling:          [0x1A, 0],

    LocationName.sunken_ghost_ship:        [0x18, 0],
    LocationName.sunken_ghost_ship_dragon: [0x18, 2],

    LocationName.valley_of_bowser_1_exit_1: [0x3A, 0],
    LocationName.valley_of_bowser_1_dragon: [0x3A, 2],
    LocationName.valley_of_bowser_2_exit_1: [0x39, 0],
    LocationName.valley_of_bowser_2_exit_2: [0x39, 1],
    LocationName.valley_of_bowser_2_dragon: [0x39, 2],
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
}

def generate_level_list(world, player):

    if not world.level_shuffle[player]:
        out_level_list = full_level_list.copy()
        out_level_list[0x00] = 0x03
        out_level_list[0x11] = 0x28

        if world.bowser_castle_doors[player] == "fast":
            out_level_list[0x41] = 0x82
            out_level_list[0x42] = 0x32
        elif world.bowser_castle_doors[player] == "slow":
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
    if not world.exclude_special_zone[player]:
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
    if world.bowser_castle_doors[player] == "fast":
        shuffled_level_list.append(0x82)
        shuffled_level_list.append(0x32)
    elif world.bowser_castle_doors[player] == "slow":
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
    if not world.exclude_special_zone[player]:
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
