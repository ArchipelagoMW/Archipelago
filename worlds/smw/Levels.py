
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
    LocationName.donut_secret_house_pswitch_coin_block_1: [0x13, 217],
    LocationName.donut_secret_house_pswitch_coin_block_2: [0x13, 218],
    LocationName.donut_secret_house_pswitch_coin_block_3: [0x13, 219],
    LocationName.donut_secret_house_directional_coin_block_1: [0x13, 220],
    LocationName.donut_plains_1_coin_block_1: [0x15, 221],
    LocationName.donut_plains_1_coin_block_2: [0x15, 222],
    LocationName.donut_plains_1_yoshi_block_1: [0x15, 223],
    LocationName.donut_plains_1_vine_block_1: [0x15, 224],
    LocationName.donut_plains_1_green_block_1: [0x15, 225],
    LocationName.donut_plains_1_green_block_2: [0x15, 226],
    LocationName.donut_plains_1_green_block_3: [0x15, 227],
    LocationName.donut_plains_1_green_block_4: [0x15, 228],
    LocationName.donut_plains_1_green_block_5: [0x15, 229],
    LocationName.donut_plains_1_green_block_6: [0x15, 230],
    LocationName.donut_plains_1_green_block_7: [0x15, 231],
    LocationName.donut_plains_1_green_block_8: [0x15, 232],
    LocationName.donut_plains_1_green_block_9: [0x15, 233],
    LocationName.donut_plains_1_green_block_10: [0x15, 234],
    LocationName.donut_plains_1_green_block_11: [0x15, 235],
    LocationName.donut_plains_1_green_block_12: [0x15, 236],
    LocationName.donut_plains_1_green_block_13: [0x15, 237],
    LocationName.donut_plains_1_green_block_14: [0x15, 238],
    LocationName.donut_plains_1_green_block_15: [0x15, 239],
    LocationName.donut_plains_1_green_block_16: [0x15, 240],
    LocationName.donut_plains_1_yellow_block_1: [0x15, 241],
    LocationName.donut_plains_1_yellow_block_2: [0x15, 242],
    LocationName.donut_plains_1_yellow_block_3: [0x15, 243],
    LocationName.sunken_ghost_ship_powerup_block_1: [0x18, 244],
    LocationName.sunken_ghost_ship_star_block_1: [0x18, 245],
    LocationName.chocolate_castle_yellow_block_1: [0x1A, 246],
    LocationName.chocolate_castle_yellow_block_2: [0x1A, 247],
    LocationName.chocolate_castle_green_block_1: [0x1A, 248],
    LocationName.chocolate_fortress_powerup_block_1: [0x1B, 249],
    LocationName.chocolate_fortress_powerup_block_2: [0x1B, 250],
    LocationName.chocolate_fortress_coin_block_1: [0x1B, 251],
    LocationName.chocolate_fortress_coin_block_2: [0x1B, 252],
    LocationName.chocolate_fortress_green_block_1: [0x1B, 253],
    LocationName.chocolate_island_5_yoshi_block_1: [0x1C, 254],
    LocationName.chocolate_island_5_powerup_block_1: [0x1C, 255],
    LocationName.chocolate_island_5_life_block_1: [0x1C, 256],
    LocationName.chocolate_island_5_yellow_block_1: [0x1C, 257],
    LocationName.chocolate_island_4_yellow_block_1: [0x1D, 258],
    LocationName.chocolate_island_4_blue_pow_block_1: [0x1D, 259],
    LocationName.chocolate_island_4_powerup_block_1: [0x1D, 260],
    LocationName.forest_fortress_yellow_block_1: [0x1F, 261],
    LocationName.forest_fortress_powerup_block_1: [0x1F, 262],
    LocationName.forest_fortress_life_block_1: [0x1F, 263],
    LocationName.forest_fortress_life_block_2: [0x1F, 264],
    LocationName.forest_fortress_life_block_3: [0x1F, 265],
    LocationName.forest_fortress_life_block_4: [0x1F, 266],
    LocationName.forest_fortress_life_block_5: [0x1F, 267],
    LocationName.forest_fortress_life_block_6: [0x1F, 268],
    LocationName.forest_fortress_life_block_7: [0x1F, 269],
    LocationName.forest_fortress_life_block_8: [0x1F, 270],
    LocationName.forest_fortress_life_block_9: [0x1F, 271],
    LocationName.forest_castle_green_block_1: [0x20, 272],
    LocationName.chocolate_ghost_house_powerup_block_1: [0x21, 273],
    LocationName.chocolate_ghost_house_powerup_block_2: [0x21, 274],
    LocationName.chocolate_ghost_house_life_block_1: [0x21, 275],
    LocationName.chocolate_island_1_flying_block_1: [0x22, 276],
    LocationName.chocolate_island_1_flying_block_2: [0x22, 277],
    LocationName.chocolate_island_1_yoshi_block_1: [0x22, 278],
    LocationName.chocolate_island_1_green_block_1: [0x22, 279],
    LocationName.chocolate_island_1_life_block_1: [0x22, 280],
    LocationName.chocolate_island_3_powerup_block_1: [0x23, 281],
    LocationName.chocolate_island_3_powerup_block_2: [0x23, 282],
    LocationName.chocolate_island_3_powerup_block_3: [0x23, 283],
    LocationName.chocolate_island_3_green_block_1: [0x23, 284],
    LocationName.chocolate_island_3_bonus_block_1: [0x23, 285],
    LocationName.chocolate_island_3_vine_block_1: [0x23, 286],
    LocationName.chocolate_island_3_life_block_1: [0x23, 287],
    LocationName.chocolate_island_3_life_block_2: [0x23, 288],
    LocationName.chocolate_island_3_life_block_3: [0x23, 289],
    LocationName.chocolate_island_2_multi_coin_block_1: [0x24, 290],
    LocationName.chocolate_island_2_invis_coin_block_1: [0x24, 291],
    LocationName.chocolate_island_2_yoshi_block_1: [0x24, 292],
    LocationName.chocolate_island_2_coin_block_1: [0x24, 293],
    LocationName.chocolate_island_2_coin_block_2: [0x24, 294],
    LocationName.chocolate_island_2_multi_coin_block_2: [0x24, 295],
    LocationName.chocolate_island_2_powerup_block_1: [0x24, 296],
    LocationName.chocolate_island_2_blue_pow_block_1: [0x24, 297],
    LocationName.chocolate_island_2_yellow_block_1: [0x24, 298],
    LocationName.chocolate_island_2_yellow_block_2: [0x24, 299],
    LocationName.chocolate_island_2_green_block_1: [0x24, 300],
    LocationName.chocolate_island_2_green_block_2: [0x24, 301],
    LocationName.chocolate_island_2_green_block_3: [0x24, 302],
    LocationName.chocolate_island_2_green_block_4: [0x24, 303],
    LocationName.chocolate_island_2_green_block_5: [0x24, 304],
    LocationName.chocolate_island_2_green_block_6: [0x24, 305],
    LocationName.yoshis_island_castle_coin_block_1: [0x25, 306],
    LocationName.yoshis_island_castle_coin_block_2: [0x25, 307],
    LocationName.yoshis_island_castle_powerup_block_1: [0x25, 308],
    LocationName.yoshis_island_castle_coin_block_3: [0x25, 309],
    LocationName.yoshis_island_castle_coin_block_4: [0x25, 310],
    LocationName.yoshis_island_castle_flying_block_1: [0x25, 311],
    LocationName.yoshis_island_4_yellow_block_1: [0x26, 312],
    LocationName.yoshis_island_4_powerup_block_1: [0x26, 313],
    LocationName.yoshis_island_4_multi_coin_block_1: [0x26, 314],
    LocationName.yoshis_island_4_star_block_1: [0x26, 315],
    LocationName.yoshis_island_3_yellow_block_1: [0x27, 316],
    LocationName.yoshis_island_3_yellow_block_2: [0x27, 317],
    LocationName.yoshis_island_3_yellow_block_3: [0x27, 318],
    LocationName.yoshis_island_3_yellow_block_4: [0x27, 319],
    LocationName.yoshis_island_3_yellow_block_5: [0x27, 320],
    LocationName.yoshis_island_3_yellow_block_6: [0x27, 321],
    LocationName.yoshis_island_3_yellow_block_7: [0x27, 322],
    LocationName.yoshis_island_3_yellow_block_8: [0x27, 323],
    LocationName.yoshis_island_3_yellow_block_9: [0x27, 324],
    LocationName.yoshis_island_3_yellow_block_10: [0x27, 325],
    LocationName.yoshis_island_3_yellow_block_11: [0x27, 326],
    LocationName.yoshis_island_3_yellow_block_12: [0x27, 327],
    LocationName.yoshis_island_3_yellow_block_13: [0x27, 328],
    LocationName.yoshis_island_3_yellow_block_14: [0x27, 329],
    LocationName.yoshis_island_3_yellow_block_15: [0x27, 330],
    LocationName.yoshis_island_3_yellow_block_16: [0x27, 331],
    LocationName.yoshis_island_3_yellow_block_17: [0x27, 332],
    LocationName.yoshis_island_3_yellow_block_18: [0x27, 333],
    LocationName.yoshis_island_3_yellow_block_19: [0x27, 334],
    LocationName.yoshis_island_3_yellow_block_20: [0x27, 335],
    LocationName.yoshis_island_3_yellow_block_21: [0x27, 336],
    LocationName.yoshis_island_3_yellow_block_22: [0x27, 337],
    LocationName.yoshis_island_3_yellow_block_23: [0x27, 338],
    LocationName.yoshis_island_3_yellow_block_24: [0x27, 339],
    LocationName.yoshis_island_3_yellow_block_25: [0x27, 340],
    LocationName.yoshis_island_3_yellow_block_26: [0x27, 341],
    LocationName.yoshis_island_3_yellow_block_27: [0x27, 342],
    LocationName.yoshis_island_3_yellow_block_28: [0x27, 343],
    LocationName.yoshis_island_3_yellow_block_29: [0x27, 344],
    LocationName.yoshis_island_3_coin_block_1: [0x27, 345],
    LocationName.yoshis_island_3_yoshi_block_1: [0x27, 346],
    LocationName.yoshis_island_3_yellow_block_30: [0x27, 347],
    LocationName.yoshis_island_3_yellow_block_31: [0x27, 348],
    LocationName.yoshis_island_3_yellow_block_32: [0x27, 349],
    LocationName.yoshis_island_3_yellow_block_33: [0x27, 350],
    LocationName.yoshis_island_3_yellow_block_34: [0x27, 351],
    LocationName.yoshis_island_3_yellow_block_35: [0x27, 352],
    LocationName.yoshis_island_3_yellow_block_36: [0x27, 353],
    LocationName.yoshis_island_3_yellow_block_37: [0x27, 354],
    LocationName.yoshis_island_3_yellow_block_38: [0x27, 355],
    LocationName.yoshis_island_3_yellow_block_39: [0x27, 356],
    LocationName.yoshis_island_3_yellow_block_40: [0x27, 357],
    LocationName.yoshis_island_3_yellow_block_41: [0x27, 358],
    LocationName.yoshis_island_3_yellow_block_42: [0x27, 359],
    LocationName.yoshis_island_3_yellow_block_43: [0x27, 360],
    LocationName.yoshis_island_3_yellow_block_44: [0x27, 361],
    LocationName.yoshis_island_3_yellow_block_45: [0x27, 362],
    LocationName.yoshis_island_3_yellow_block_46: [0x27, 363],
    LocationName.yoshis_island_3_yellow_block_47: [0x27, 364],
    LocationName.yoshis_island_3_yellow_block_48: [0x27, 365],
    LocationName.yoshis_island_3_yellow_block_49: [0x27, 366],
    LocationName.yoshis_island_3_yellow_block_50: [0x27, 367],
    LocationName.yoshis_island_3_yellow_block_51: [0x27, 368],
    LocationName.yoshis_island_3_coin_block_2: [0x27, 369],
    LocationName.yoshis_island_3_powerup_block_1: [0x27, 370],
    LocationName.yoshis_island_3_yellow_block_52: [0x27, 371],
    LocationName.yoshis_island_3_yellow_block_53: [0x27, 372],
    LocationName.yoshis_island_3_yellow_block_54: [0x27, 373],
    LocationName.yoshis_island_3_yellow_block_55: [0x27, 374],
    LocationName.yoshis_island_3_yellow_block_56: [0x27, 375],
    LocationName.yoshis_island_3_yellow_block_57: [0x27, 376],
    LocationName.yoshis_island_3_yellow_block_58: [0x27, 377],
    LocationName.yoshis_island_3_yellow_block_59: [0x27, 378],
    LocationName.yoshis_island_3_yellow_block_60: [0x27, 379],
    LocationName.yoshis_island_3_yellow_block_61: [0x27, 380],
    LocationName.yoshis_island_3_yellow_block_62: [0x27, 381],
    LocationName.yoshis_island_3_yellow_block_63: [0x27, 382],
    LocationName.yoshis_island_3_yellow_block_64: [0x27, 383],
    LocationName.yoshis_island_3_yellow_block_65: [0x27, 384],
    LocationName.yoshis_island_3_yellow_block_66: [0x27, 385],
    LocationName.yoshis_island_3_yellow_block_67: [0x27, 386],
    LocationName.yoshis_island_3_yellow_block_68: [0x27, 387],
    LocationName.yoshis_island_3_yellow_block_69: [0x27, 388],
    LocationName.yoshis_island_3_yellow_block_70: [0x27, 389],
    LocationName.yoshis_island_3_yellow_block_71: [0x27, 390],
    LocationName.yoshis_island_3_yellow_block_72: [0x27, 391],
    LocationName.yoshis_island_3_yellow_block_73: [0x27, 392],
    LocationName.yoshis_island_3_yellow_block_74: [0x27, 393],
    LocationName.yoshis_island_3_yellow_block_75: [0x27, 394],
    LocationName.yoshis_island_3_yellow_block_76: [0x27, 395],
    LocationName.yoshis_island_3_yellow_block_77: [0x27, 396],
    LocationName.yoshis_island_3_yellow_block_78: [0x27, 397],
    LocationName.yoshis_island_3_yellow_block_79: [0x27, 398],
    LocationName.yoshis_island_3_yellow_block_80: [0x27, 399],
    LocationName.yoshis_island_3_yellow_block_81: [0x27, 400],
    LocationName.yoshis_island_3_yellow_block_82: [0x27, 401],
    LocationName.yoshis_island_3_yellow_block_83: [0x27, 402],
    LocationName.yoshis_island_3_yellow_block_84: [0x27, 403],
    LocationName.yoshis_island_3_yellow_block_85: [0x27, 404],
    LocationName.yoshis_island_3_yellow_block_86: [0x27, 405],
    LocationName.yoshis_island_3_bonus_block_1: [0x27, 406],
    LocationName.yoshis_island_1_flying_block_1: [0x29, 407],
    LocationName.yoshis_island_1_yellow_block_1: [0x29, 408],
    LocationName.yoshis_island_1_life_block_1: [0x29, 409],
    LocationName.yoshis_island_1_powerup_block_1: [0x29, 410],
    LocationName.yoshis_island_2_flying_block_1: [0x2A, 411],
    LocationName.yoshis_island_2_flying_block_2: [0x2A, 412],
    LocationName.yoshis_island_2_flying_block_3: [0x2A, 413],
    LocationName.yoshis_island_2_flying_block_4: [0x2A, 414],
    LocationName.yoshis_island_2_flying_block_5: [0x2A, 415],
    LocationName.yoshis_island_2_flying_block_6: [0x2A, 416],
    LocationName.yoshis_island_2_coin_block_1: [0x2A, 417],
    LocationName.yoshis_island_2_yellow_block_1: [0x2A, 418],
    LocationName.yoshis_island_2_coin_block_2: [0x2A, 419],
    LocationName.yoshis_island_2_coin_block_3: [0x2A, 420],
    LocationName.yoshis_island_2_yoshi_block_1: [0x2A, 421],
    LocationName.yoshis_island_2_coin_block_4: [0x2A, 422],
    LocationName.yoshis_island_2_yoshi_block_2: [0x2A, 423],
    LocationName.yoshis_island_2_coin_block_5: [0x2A, 424],
    LocationName.yoshis_island_2_vine_block_1: [0x2A, 425],
    LocationName.yoshis_island_2_yellow_block_2: [0x2A, 426],
    LocationName.vanilla_ghost_house_powerup_block_1: [0x2B, 427],
    LocationName.vanilla_ghost_house_vine_block_1: [0x2B, 428],
    LocationName.vanilla_ghost_house_powerup_block_2: [0x2B, 429],
    LocationName.vanilla_ghost_house_multi_coin_block_1: [0x2B, 430],
    LocationName.vanilla_ghost_house_blue_pow_block_1: [0x2B, 431],
    LocationName.vanilla_secret_1_coin_block_1: [0x2D, 432],
    LocationName.vanilla_secret_1_powerup_block_1: [0x2D, 433],
    LocationName.vanilla_secret_1_multi_coin_block_1: [0x2D, 434],
    LocationName.vanilla_secret_1_vine_block_1: [0x2D, 435],
    LocationName.vanilla_secret_1_vine_block_2: [0x2D, 436],
    LocationName.vanilla_secret_1_coin_block_2: [0x2D, 437],
    LocationName.vanilla_secret_1_coin_block_3: [0x2D, 438],
    LocationName.vanilla_secret_1_powerup_block_2: [0x2D, 439],
    LocationName.vanilla_dome_3_coin_block_1: [0x2E, 440],
    LocationName.vanilla_dome_3_flying_block_1: [0x2E, 441],
    LocationName.vanilla_dome_3_flying_block_2: [0x2E, 442],
    LocationName.vanilla_dome_3_powerup_block_1: [0x2E, 443],
    LocationName.vanilla_dome_3_flying_block_3: [0x2E, 444],
    LocationName.vanilla_dome_3_invis_coin_block_1: [0x2E, 445],
    LocationName.vanilla_dome_3_powerup_block_2: [0x2E, 446],
    LocationName.vanilla_dome_3_multi_coin_block_1: [0x2E, 447],
    LocationName.vanilla_dome_3_powerup_block_3: [0x2E, 448],
    LocationName.vanilla_dome_3_yoshi_block_1: [0x2E, 449],
    LocationName.vanilla_dome_3_powerup_block_4: [0x2E, 450],
    LocationName.vanilla_dome_3_pswitch_coin_block_1: [0x2E, 451],
    LocationName.vanilla_dome_3_pswitch_coin_block_2: [0x2E, 452],
    LocationName.vanilla_dome_3_pswitch_coin_block_3: [0x2E, 453],
    LocationName.vanilla_dome_3_pswitch_coin_block_4: [0x2E, 454],
    LocationName.vanilla_dome_3_pswitch_coin_block_5: [0x2E, 455],
    LocationName.vanilla_dome_3_pswitch_coin_block_6: [0x2E, 456],
    LocationName.donut_secret_2_directional_coin_block_1: [0x2F, 457],
    LocationName.donut_secret_2_vine_block_1: [0x2F, 458],
    LocationName.donut_secret_2_star_block_1: [0x2F, 459],
    LocationName.donut_secret_2_powerup_block_1: [0x2F, 460],
    LocationName.donut_secret_2_star_block_2: [0x2F, 461],
    LocationName.valley_of_bowser_4_yellow_block_1: [0x33, 462],
    LocationName.valley_of_bowser_4_powerup_block_1: [0x33, 463],
    LocationName.valley_of_bowser_4_vine_block_1: [0x33, 464],
    LocationName.valley_of_bowser_4_yoshi_block_1: [0x33, 465],
    LocationName.valley_of_bowser_4_life_block_1: [0x33, 466],
    LocationName.valley_of_bowser_4_powerup_block_2: [0x33, 467],
    LocationName.valley_castle_yellow_block_1: [0x34, 468],
    LocationName.valley_castle_yellow_block_2: [0x34, 469],
    LocationName.valley_castle_green_block_1: [0x34, 470],
    LocationName.valley_fortress_green_block_1: [0x35, 471],
    LocationName.valley_fortress_yellow_block_1: [0x35, 472],
    LocationName.valley_of_bowser_3_powerup_block_1: [0x37, 473],
    LocationName.valley_of_bowser_3_powerup_block_2: [0x37, 474],
    LocationName.valley_ghost_house_pswitch_coin_block_1: [0x38, 475],
    LocationName.valley_ghost_house_multi_coin_block_1: [0x38, 476],
    LocationName.valley_ghost_house_powerup_block_1: [0x38, 477],
    LocationName.valley_ghost_house_directional_coin_block_1: [0x38, 478],
    LocationName.valley_of_bowser_2_powerup_block_1: [0x39, 479],
    LocationName.valley_of_bowser_2_yellow_block_1: [0x39, 480],
    LocationName.valley_of_bowser_2_powerup_block_2: [0x39, 481],
    LocationName.valley_of_bowser_2_wings_block_1: [0x39, 482],
    LocationName.valley_of_bowser_1_green_block_1: [0x3A, 483],
    LocationName.valley_of_bowser_1_invis_coin_block_1: [0x3A, 484],
    LocationName.valley_of_bowser_1_invis_coin_block_2: [0x3A, 485],
    LocationName.valley_of_bowser_1_invis_coin_block_3: [0x3A, 486],
    LocationName.valley_of_bowser_1_yellow_block_1: [0x3A, 487],
    LocationName.valley_of_bowser_1_yellow_block_2: [0x3A, 488],
    LocationName.valley_of_bowser_1_yellow_block_3: [0x3A, 489],
    LocationName.valley_of_bowser_1_yellow_block_4: [0x3A, 490],
    LocationName.valley_of_bowser_1_vine_block_1: [0x3A, 491],
    LocationName.chocolate_secret_powerup_block_1: [0x3B, 492],
    LocationName.chocolate_secret_powerup_block_2: [0x3B, 493],
    LocationName.vanilla_dome_2_coin_block_1: [0x3C, 494],
    LocationName.vanilla_dome_2_powerup_block_1: [0x3C, 495],
    LocationName.vanilla_dome_2_coin_block_2: [0x3C, 496],
    LocationName.vanilla_dome_2_coin_block_3: [0x3C, 497],
    LocationName.vanilla_dome_2_vine_block_1: [0x3C, 498],
    LocationName.vanilla_dome_2_invis_life_block_1: [0x3C, 499],
    LocationName.vanilla_dome_2_coin_block_4: [0x3C, 500],
    LocationName.vanilla_dome_2_coin_block_5: [0x3C, 501],
    LocationName.vanilla_dome_2_powerup_block_2: [0x3C, 502],
    LocationName.vanilla_dome_2_powerup_block_3: [0x3C, 503],
    LocationName.vanilla_dome_2_powerup_block_4: [0x3C, 504],
    LocationName.vanilla_dome_2_multi_coin_block_1: [0x3C, 505],
    LocationName.vanilla_dome_2_multi_coin_block_2: [0x3C, 506],
    LocationName.vanilla_dome_4_powerup_block_1: [0x3D, 507],
    LocationName.vanilla_dome_4_powerup_block_2: [0x3D, 508],
    LocationName.vanilla_dome_4_coin_block_1: [0x3D, 509],
    LocationName.vanilla_dome_4_coin_block_2: [0x3D, 510],
    LocationName.vanilla_dome_4_coin_block_3: [0x3D, 511],
    LocationName.vanilla_dome_4_life_block_1: [0x3D, 512],
    LocationName.vanilla_dome_4_coin_block_4: [0x3D, 513],
    LocationName.vanilla_dome_4_coin_block_5: [0x3D, 514],
    LocationName.vanilla_dome_4_coin_block_6: [0x3D, 515],
    LocationName.vanilla_dome_4_coin_block_7: [0x3D, 516],
    LocationName.vanilla_dome_4_coin_block_8: [0x3D, 517],
    LocationName.vanilla_dome_1_flying_block_1: [0x3E, 518],
    LocationName.vanilla_dome_1_powerup_block_1: [0x3E, 519],
    LocationName.vanilla_dome_1_powerup_block_2: [0x3E, 520],
    LocationName.vanilla_dome_1_coin_block_1: [0x3E, 521],
    LocationName.vanilla_dome_1_life_block_1: [0x3E, 522],
    LocationName.vanilla_dome_1_powerup_block_3: [0x3E, 523],
    LocationName.vanilla_dome_1_vine_block_1: [0x3E, 524],
    LocationName.vanilla_dome_1_star_block_1: [0x3E, 525],
    LocationName.vanilla_dome_1_powerup_block_4: [0x3E, 526],
    LocationName.vanilla_dome_1_coin_block_2: [0x3E, 527],
    LocationName.vanilla_dome_castle_life_block_1: [0x40, 528],
    LocationName.vanilla_dome_castle_life_block_2: [0x40, 529],
    LocationName.vanilla_dome_castle_powerup_block_1: [0x40, 530],
    LocationName.vanilla_dome_castle_life_block_3: [0x40, 531],
    LocationName.vanilla_dome_castle_green_block_1: [0x40, 532],
    LocationName.forest_ghost_house_coin_block_1: [0x41, 533],
    LocationName.forest_ghost_house_powerup_block_1: [0x41, 534],
    LocationName.forest_ghost_house_flying_block_1: [0x41, 535],
    LocationName.forest_ghost_house_powerup_block_2: [0x41, 536],
    LocationName.forest_ghost_house_life_block_1: [0x41, 537],
    LocationName.forest_of_illusion_1_powerup_block_1: [0x42, 538],
    LocationName.forest_of_illusion_1_yoshi_block_1: [0x42, 539],
    LocationName.forest_of_illusion_1_powerup_block_2: [0x42, 540],
    LocationName.forest_of_illusion_1_key_block_1: [0x42, 541],
    LocationName.forest_of_illusion_1_life_block_1: [0x42, 542],
    LocationName.forest_of_illusion_4_multi_coin_block_1: [0x43, 543],
    LocationName.forest_of_illusion_4_coin_block_1: [0x43, 544],
    LocationName.forest_of_illusion_4_coin_block_2: [0x43, 545],
    LocationName.forest_of_illusion_4_coin_block_3: [0x43, 546],
    LocationName.forest_of_illusion_4_coin_block_4: [0x43, 547],
    LocationName.forest_of_illusion_4_powerup_block_1: [0x43, 548],
    LocationName.forest_of_illusion_4_coin_block_5: [0x43, 549],
    LocationName.forest_of_illusion_4_coin_block_6: [0x43, 550],
    LocationName.forest_of_illusion_4_coin_block_7: [0x43, 551],
    LocationName.forest_of_illusion_4_powerup_block_2: [0x43, 552],
    LocationName.forest_of_illusion_4_coin_block_8: [0x43, 553],
    LocationName.forest_of_illusion_4_coin_block_9: [0x43, 554],
    LocationName.forest_of_illusion_4_coin_block_10: [0x43, 555],
    LocationName.forest_of_illusion_2_green_block_1: [0x44, 556],
    LocationName.forest_of_illusion_2_powerup_block_1: [0x44, 557],
    LocationName.forest_of_illusion_2_invis_coin_block_1: [0x44, 558],
    LocationName.forest_of_illusion_2_invis_coin_block_2: [0x44, 559],
    LocationName.forest_of_illusion_2_invis_life_block_1: [0x44, 560],
    LocationName.forest_of_illusion_2_invis_coin_block_3: [0x44, 561],
    LocationName.forest_of_illusion_2_yellow_block_1: [0x44, 562],
    LocationName.forest_secret_powerup_block_1: [0x46, 563],
    LocationName.forest_secret_powerup_block_2: [0x46, 564],
    LocationName.forest_secret_life_block_1: [0x46, 565],
    LocationName.forest_of_illusion_3_yoshi_block_1: [0x47, 566],
    LocationName.forest_of_illusion_3_coin_block_1: [0x47, 567],
    LocationName.forest_of_illusion_3_multi_coin_block_1: [0x47, 568],
    LocationName.forest_of_illusion_3_coin_block_2: [0x47, 569],
    LocationName.forest_of_illusion_3_multi_coin_block_2: [0x47, 570],
    LocationName.forest_of_illusion_3_coin_block_3: [0x47, 571],
    LocationName.forest_of_illusion_3_coin_block_4: [0x47, 572],
    LocationName.forest_of_illusion_3_coin_block_5: [0x47, 573],
    LocationName.forest_of_illusion_3_coin_block_6: [0x47, 574],
    LocationName.forest_of_illusion_3_coin_block_7: [0x47, 575],
    LocationName.forest_of_illusion_3_coin_block_8: [0x47, 576],
    LocationName.forest_of_illusion_3_coin_block_9: [0x47, 577],
    LocationName.forest_of_illusion_3_coin_block_10: [0x47, 578],
    LocationName.forest_of_illusion_3_coin_block_11: [0x47, 579],
    LocationName.forest_of_illusion_3_coin_block_12: [0x47, 580],
    LocationName.forest_of_illusion_3_coin_block_13: [0x47, 581],
    LocationName.forest_of_illusion_3_coin_block_14: [0x47, 582],
    LocationName.forest_of_illusion_3_coin_block_15: [0x47, 583],
    LocationName.forest_of_illusion_3_coin_block_16: [0x47, 584],
    LocationName.forest_of_illusion_3_coin_block_17: [0x47, 585],
    LocationName.forest_of_illusion_3_coin_block_18: [0x47, 586],
    LocationName.forest_of_illusion_3_coin_block_19: [0x47, 587],
    LocationName.forest_of_illusion_3_coin_block_20: [0x47, 588],
    LocationName.forest_of_illusion_3_coin_block_21: [0x47, 589],
    LocationName.forest_of_illusion_3_coin_block_22: [0x47, 590],
    LocationName.forest_of_illusion_3_coin_block_23: [0x47, 591],
    LocationName.forest_of_illusion_3_coin_block_24: [0x47, 592],
    LocationName.special_zone_8_yoshi_block_1: [0x49, 593],
    LocationName.special_zone_8_coin_block_1: [0x49, 594],
    LocationName.special_zone_8_coin_block_2: [0x49, 595],
    LocationName.special_zone_8_coin_block_3: [0x49, 596],
    LocationName.special_zone_8_coin_block_4: [0x49, 597],
    LocationName.special_zone_8_coin_block_5: [0x49, 598],
    LocationName.special_zone_8_blue_pow_block_1: [0x49, 599],
    LocationName.special_zone_8_powerup_block_1: [0x49, 600],
    LocationName.special_zone_8_star_block_1: [0x49, 601],
    LocationName.special_zone_8_coin_block_6: [0x49, 602],
    LocationName.special_zone_8_coin_block_7: [0x49, 603],
    LocationName.special_zone_8_coin_block_8: [0x49, 604],
    LocationName.special_zone_8_coin_block_9: [0x49, 605],
    LocationName.special_zone_8_coin_block_10: [0x49, 606],
    LocationName.special_zone_8_coin_block_11: [0x49, 607],
    LocationName.special_zone_8_coin_block_12: [0x49, 608],
    LocationName.special_zone_8_coin_block_13: [0x49, 609],
    LocationName.special_zone_8_coin_block_14: [0x49, 610],
    LocationName.special_zone_8_coin_block_15: [0x49, 611],
    LocationName.special_zone_8_coin_block_16: [0x49, 612],
    LocationName.special_zone_8_coin_block_17: [0x49, 613],
    LocationName.special_zone_8_coin_block_18: [0x49, 614],
    LocationName.special_zone_8_multi_coin_block_1: [0x49, 615],
    LocationName.special_zone_8_coin_block_19: [0x49, 616],
    LocationName.special_zone_8_coin_block_20: [0x49, 617],
    LocationName.special_zone_8_coin_block_21: [0x49, 618],
    LocationName.special_zone_8_coin_block_22: [0x49, 619],
    LocationName.special_zone_8_coin_block_23: [0x49, 620],
    LocationName.special_zone_8_powerup_block_2: [0x49, 621],
    LocationName.special_zone_8_flying_block_1: [0x49, 622],
    LocationName.special_zone_7_powerup_block_1: [0x4A, 623],
    LocationName.special_zone_7_yoshi_block_1: [0x4A, 624],
    LocationName.special_zone_7_coin_block_1: [0x4A, 625],
    LocationName.special_zone_7_powerup_block_2: [0x4A, 626],
    LocationName.special_zone_7_coin_block_2: [0x4A, 627],
    LocationName.special_zone_6_powerup_block_1: [0x4B, 628],
    LocationName.special_zone_6_coin_block_1: [0x4B, 629],
    LocationName.special_zone_6_coin_block_2: [0x4B, 630],
    LocationName.special_zone_6_yoshi_block_1: [0x4B, 631],
    LocationName.special_zone_6_life_block_1: [0x4B, 632],
    LocationName.special_zone_6_multi_coin_block_1: [0x4B, 633],
    LocationName.special_zone_6_coin_block_3: [0x4B, 634],
    LocationName.special_zone_6_coin_block_4: [0x4B, 635],
    LocationName.special_zone_6_coin_block_5: [0x4B, 636],
    LocationName.special_zone_6_coin_block_6: [0x4B, 637],
    LocationName.special_zone_6_coin_block_7: [0x4B, 638],
    LocationName.special_zone_6_coin_block_8: [0x4B, 639],
    LocationName.special_zone_6_coin_block_9: [0x4B, 640],
    LocationName.special_zone_6_coin_block_10: [0x4B, 641],
    LocationName.special_zone_6_coin_block_11: [0x4B, 642],
    LocationName.special_zone_6_coin_block_12: [0x4B, 643],
    LocationName.special_zone_6_coin_block_13: [0x4B, 644],
    LocationName.special_zone_6_coin_block_14: [0x4B, 645],
    LocationName.special_zone_6_coin_block_15: [0x4B, 646],
    LocationName.special_zone_6_coin_block_16: [0x4B, 647],
    LocationName.special_zone_6_coin_block_17: [0x4B, 648],
    LocationName.special_zone_6_coin_block_18: [0x4B, 649],
    LocationName.special_zone_6_coin_block_19: [0x4B, 650],
    LocationName.special_zone_6_coin_block_20: [0x4B, 651],
    LocationName.special_zone_6_coin_block_21: [0x4B, 652],
    LocationName.special_zone_6_coin_block_22: [0x4B, 653],
    LocationName.special_zone_6_coin_block_23: [0x4B, 654],
    LocationName.special_zone_6_coin_block_24: [0x4B, 655],
    LocationName.special_zone_6_coin_block_25: [0x4B, 656],
    LocationName.special_zone_6_coin_block_26: [0x4B, 657],
    LocationName.special_zone_6_coin_block_27: [0x4B, 658],
    LocationName.special_zone_6_coin_block_28: [0x4B, 659],
    LocationName.special_zone_6_powerup_block_2: [0x4B, 660],
    LocationName.special_zone_6_coin_block_29: [0x4B, 661],
    LocationName.special_zone_6_coin_block_30: [0x4B, 662],
    LocationName.special_zone_6_coin_block_31: [0x4B, 663],
    LocationName.special_zone_6_coin_block_32: [0x4B, 664],
    LocationName.special_zone_6_coin_block_33: [0x4B, 665],
    LocationName.special_zone_5_yoshi_block_1: [0x4C, 666],
    LocationName.special_zone_1_vine_block_1: [0x4E, 667],
    LocationName.special_zone_1_vine_block_2: [0x4E, 668],
    LocationName.special_zone_1_vine_block_3: [0x4E, 669],
    LocationName.special_zone_1_vine_block_4: [0x4E, 670],
    LocationName.special_zone_1_life_block_1: [0x4E, 671],
    LocationName.special_zone_1_vine_block_5: [0x4E, 672],
    LocationName.special_zone_1_blue_pow_block_1: [0x4E, 673],
    LocationName.special_zone_1_vine_block_6: [0x4E, 674],
    LocationName.special_zone_1_powerup_block_1: [0x4E, 675],
    LocationName.special_zone_1_pswitch_coin_block_1: [0x4E, 676],
    LocationName.special_zone_1_pswitch_coin_block_2: [0x4E, 677],
    LocationName.special_zone_1_pswitch_coin_block_3: [0x4E, 678],
    LocationName.special_zone_1_pswitch_coin_block_4: [0x4E, 679],
    LocationName.special_zone_1_pswitch_coin_block_5: [0x4E, 680],
    LocationName.special_zone_1_pswitch_coin_block_6: [0x4E, 681],
    LocationName.special_zone_1_pswitch_coin_block_7: [0x4E, 682],
    LocationName.special_zone_1_pswitch_coin_block_8: [0x4E, 683],
    LocationName.special_zone_1_pswitch_coin_block_9: [0x4E, 684],
    LocationName.special_zone_1_pswitch_coin_block_10: [0x4E, 685],
    LocationName.special_zone_1_pswitch_coin_block_11: [0x4E, 686],
    LocationName.special_zone_1_pswitch_coin_block_12: [0x4E, 687],
    LocationName.special_zone_1_pswitch_coin_block_13: [0x4E, 688],
    LocationName.special_zone_2_powerup_block_1: [0x4F, 689],
    LocationName.special_zone_2_coin_block_1: [0x4F, 690],
    LocationName.special_zone_2_coin_block_2: [0x4F, 691],
    LocationName.special_zone_2_powerup_block_2: [0x4F, 692],
    LocationName.special_zone_2_coin_block_3: [0x4F, 693],
    LocationName.special_zone_2_coin_block_4: [0x4F, 694],
    LocationName.special_zone_2_powerup_block_3: [0x4F, 695],
    LocationName.special_zone_2_multi_coin_block_1: [0x4F, 696],
    LocationName.special_zone_2_coin_block_5: [0x4F, 697],
    LocationName.special_zone_2_coin_block_6: [0x4F, 698],
    LocationName.special_zone_3_powerup_block_1: [0x50, 699],
    LocationName.special_zone_3_yoshi_block_1: [0x50, 700],
    LocationName.special_zone_3_wings_block_1: [0x50, 701],
    LocationName.special_zone_4_powerup_block_1: [0x51, 702],
    LocationName.special_zone_4_star_block_1: [0x51, 703],
    LocationName.star_road_2_star_block_1: [0x54, 704],
    LocationName.star_road_3_key_block_1: [0x56, 705],
    LocationName.star_road_4_powerup_block_1: [0x59, 706],
    LocationName.star_road_4_green_block_1: [0x59, 707],
    LocationName.star_road_4_green_block_2: [0x59, 708],
    LocationName.star_road_4_green_block_3: [0x59, 709],
    LocationName.star_road_4_green_block_4: [0x59, 710],
    LocationName.star_road_4_green_block_5: [0x59, 711],
    LocationName.star_road_4_green_block_6: [0x59, 712],
    LocationName.star_road_4_green_block_7: [0x59, 713],
    LocationName.star_road_4_key_block_1: [0x59, 714],
    LocationName.star_road_5_directional_coin_block_1: [0x5A, 715],
    LocationName.star_road_5_life_block_1: [0x5A, 716],
    LocationName.star_road_5_vine_block_1: [0x5A, 717],
    LocationName.star_road_5_yellow_block_1: [0x5A, 718],
    LocationName.star_road_5_yellow_block_2: [0x5A, 719],
    LocationName.star_road_5_yellow_block_3: [0x5A, 720],
    LocationName.star_road_5_yellow_block_4: [0x5A, 721],
    LocationName.star_road_5_yellow_block_5: [0x5A, 722],
    LocationName.star_road_5_yellow_block_6: [0x5A, 723],
    LocationName.star_road_5_yellow_block_7: [0x5A, 724],
    LocationName.star_road_5_yellow_block_8: [0x5A, 725],
    LocationName.star_road_5_yellow_block_9: [0x5A, 726],
    LocationName.star_road_5_yellow_block_10: [0x5A, 727],
    LocationName.star_road_5_yellow_block_11: [0x5A, 728],
    LocationName.star_road_5_yellow_block_12: [0x5A, 729],
    LocationName.star_road_5_yellow_block_13: [0x5A, 730],
    LocationName.star_road_5_yellow_block_14: [0x5A, 731],
    LocationName.star_road_5_yellow_block_15: [0x5A, 732],
    LocationName.star_road_5_yellow_block_16: [0x5A, 733],
    LocationName.star_road_5_yellow_block_17: [0x5A, 734],
    LocationName.star_road_5_yellow_block_18: [0x5A, 735],
    LocationName.star_road_5_yellow_block_19: [0x5A, 736],
    LocationName.star_road_5_yellow_block_20: [0x5A, 737],
    LocationName.star_road_5_green_block_1: [0x5A, 738],
    LocationName.star_road_5_green_block_2: [0x5A, 739],
    LocationName.star_road_5_green_block_3: [0x5A, 740],
    LocationName.star_road_5_green_block_4: [0x5A, 741],
    LocationName.star_road_5_green_block_5: [0x5A, 742],
    LocationName.star_road_5_green_block_6: [0x5A, 743],
    LocationName.star_road_5_green_block_7: [0x5A, 744],
    LocationName.star_road_5_green_block_8: [0x5A, 745],
    LocationName.star_road_5_green_block_9: [0x5A, 746],
    LocationName.star_road_5_green_block_10: [0x5A, 747],
    LocationName.star_road_5_green_block_11: [0x5A, 748],
    LocationName.star_road_5_green_block_12: [0x5A, 749],
    LocationName.star_road_5_green_block_13: [0x5A, 750],
    LocationName.star_road_5_green_block_14: [0x5A, 751],
    LocationName.star_road_5_green_block_15: [0x5A, 752],
    LocationName.star_road_5_green_block_16: [0x5A, 753],
    LocationName.star_road_5_green_block_17: [0x5A, 754],
    LocationName.star_road_5_green_block_18: [0x5A, 755],
    LocationName.star_road_5_green_block_19: [0x5A, 756],
    LocationName.star_road_5_green_block_20: [0x5A, 757]
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
