from .Names import LocationName

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import WaffleWorld

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

special_zone_tile_regions = [
    LocationName.special_zone_1_tile,
    LocationName.special_zone_2_tile,
    LocationName.special_zone_3_tile,
    LocationName.special_zone_4_tile,
    LocationName.special_zone_5_tile,
    LocationName.special_zone_6_tile,
    LocationName.special_zone_7_tile,
    LocationName.special_zone_8_tile,
]

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
    coords: tuple[int,int]
    levelIDAddress: int
    #eventIDAddress: int
    eventIDValue: int
    #progressByte: int
    #progressBit: int
    exit1Path: SMWPath
    exit2Path: SMWPath

    def __init__(self, levelName: str, coords: tuple[int, int], levelIDAddress: int, eventIDValue: int, exit1Path: SMWPath = None, exit2Path: SMWPath = None):
        self.levelName      = levelName
        self.coords = coords
        self.levelIDAddress = levelIDAddress
        #self.eventIDAddress = eventIDAddress # Inferred from: LevelIDValue (Dict Key): $2D608 + LevelIDValue
        self.eventIDValue   = eventIDValue
        #self.progressByte   = progressByte # Inferred from EventIDValue: (ID / 8) + $1F02
        #self.progressBit    = progressBit  # Inferred from EventIDValue: 1 << (7 - (ID % 8))
        self.exit1Path   = exit1Path
        self.exit2Path   = exit2Path


level_info_dict = {
    0x28: SMWLevel(LocationName.yoshis_house, (0x07, 0x27), 0x37A76, 0x00),
    0x29: SMWLevel(LocationName.yoshis_island_1_region, (0x04, 0x28), 0x37A83, 0x01, SMWPath(0x08, 0x70, 0x04)),
    0x14: SMWLevel(LocationName.yellow_switch_palace, (0x02, 0x11), 0x37812, 0x02),
    0x2A: SMWLevel(LocationName.yoshis_island_2_region, (0x0A, 0x28), 0x37A89, 0x03, SMWPath(0x08, 0x27, 0x04)),
    0x27: SMWLevel(LocationName.yoshis_island_3_region, (0x0A, 0x26), 0x37A69, 0x04, SMWPath(0x01, 0x26, 0x04)),
    0x26: SMWLevel(LocationName.yoshis_island_4_region, (0x0C, 0x24), 0x37A4B, 0x05, SMWPath(0x08, 0x25, 0x01)),
    0x25: SMWLevel(LocationName.yoshis_island_castle_region, (0x00, 0x00), 0x37A29, 0x06, SMWPath(0x08, 0x72, 0x04)),

    0x15: SMWLevel(LocationName.donut_plains_1_region, (0x05, 0x11), 0x37815, 0x07, SMWPath(0x02, 0x09, 0x04), SMWPath(0x08, 0x0A, 0x04)),
    0x09: SMWLevel(LocationName.donut_plains_2_region, (0x03, 0x0D), 0x376D3, 0x09, SMWPath(0x08, 0x04, 0x02), SMWPath(0x02, 0x08, 0x01)),
    0x0A: SMWLevel(LocationName.donut_secret_1_region, (0x05, 0x0E), 0x376E5, 0x10, SMWPath(0x08, 0x04, 0x04), SMWPath(0x01, 0x13, 0x08)),
    0x08: SMWLevel(LocationName.green_switch_palace, (0x01, 0x0D), 0x376D1, 0x28),
    0x04: SMWLevel(LocationName.donut_ghost_house_region, (0x05, 0x0A), 0x376A5, 0x0B, SMWPath(0x08, 0x03, 0x04), SMWPath(0x01, 0x05, 0x02)),
    0x13: SMWLevel(LocationName.donut_secret_house_region, (0x07, 0x10), 0x37807, 0x12, SMWPath(0x01, 0x60, 0x04), SMWPath(0x04, 0x16, 0x08)), # SMW_TODO: Check this wrt pipe behavior
    0x05: SMWLevel(LocationName.donut_plains_3_region, (0x09, 0x0A), 0x376A9, 0x0D, SMWPath(0x01, 0x06, 0x08)),
    0x06: SMWLevel(LocationName.donut_plains_4_region, (0x0B, 0x0C), 0x376CB, 0x0E, SMWPath(0x01, 0x07, 0x02)),
    0x2F: SMWLevel(LocationName.donut_secret_2_region, (0x11, 0x21), 0x37B10, 0x14, SMWPath(0x01, 0x62, 0x04)),
    0x07: SMWLevel(LocationName.donut_plains_castle_region, (0x0D, 0x0C), 0x376CD, 0x0F, SMWPath(0x08, 0x74, 0x04)),
    0x03: SMWLevel(LocationName.donut_plains_top_secret, (0x05, 0x08), 0x37685, 0xFF),
    0x16: SMWLevel(LocationName.donut_plains_star_road, (0x07, 0x12), 0x37827, 0xFF),

    0x3E: SMWLevel(LocationName.vanilla_dome_1_region, (0x06, 0x32), 0x37C25, 0x15, SMWPath(0x01, 0x3C, 0x04), SMWPath(0x02, 0x2D, 0x04)),
    0x3C: SMWLevel(LocationName.vanilla_dome_2_region, (0x09, 0x30), 0x37C08, 0x17, SMWPath(0x08, 0x2B, 0x04), SMWPath(0x01, 0x3F, 0x08)),
    0x2D: SMWLevel(LocationName.vanilla_secret_1_region, (0x04, 0x2E), 0x37AE3, 0x1D, SMWPath(0x08, 0x66, 0x02), SMWPath(0x02, 0x2C, 0x01)),
    0x2B: SMWLevel(LocationName.vanilla_ghost_house_region, (0x09, 0x2C), 0x37AC8, 0x19, SMWPath(0x01, 0x2E, 0x08)),
    0x2E: SMWLevel(LocationName.vanilla_dome_3_region, (0x0D, 0x2E), 0x37AEC, 0x1A, SMWPath(0x04, 0x3D, 0x08)),
    0x3D: SMWLevel(LocationName.vanilla_dome_4_region, (0x0D, 0x30), 0x37C0C, 0x1B, SMWPath(0x04, 0x40, 0x08)),
    0x3F: SMWLevel(LocationName.red_switch_palace, (0x0B, 0x32), 0x37C2A, 0x29),
    0x01: SMWLevel(LocationName.vanilla_secret_2_region, (0x0C, 0x03), 0x3763C, 0x1F, SMWPath(0x01, 0x02, 0x02)),
    0x02: SMWLevel(LocationName.vanilla_secret_3_region, (0x0E, 0x03), 0x3763E, 0x20, SMWPath(0x01, 0x0B, 0x02)),
    0x0B: SMWLevel(LocationName.vanilla_fortress_region, (0x10, 0x03), 0x37730, 0x21, SMWPath(0x01, 0x0C, 0x02)),
    0x40: SMWLevel(LocationName.vanilla_dome_castle_region, (0x0D, 0x32), 0x37C2C, 0x1C, SMWPath(0x04, 0x64, 0x02)),
    0x2C: SMWLevel(LocationName.vanilla_dome_star_road, (0x01, 0x2E), 0x37AE0, 0xFF),

    0x0C: SMWLevel(LocationName.butter_bridge_1_region, (0x14, 0x03), 0x37734, 0x22, SMWPath(0x01, 0x0D, 0x02)),
    0x0D: SMWLevel(LocationName.butter_bridge_2_region, (0x16, 0x03), 0x37736, 0x23, SMWPath(0x01, 0x0E, 0x02)),
    0x0F: SMWLevel(LocationName.cheese_bridge_region, (0x14, 0x05), 0x37754, 0x25, SMWPath(0x01, 0x10, 0x02), SMWPath(0x04, 0x11, 0x08)),
    0x11: SMWLevel(LocationName.soda_lake_region, (0x14, 0x08), 0x37784, 0x60, SMWPath(0x04, 0x12, 0x04)),
    0x10: SMWLevel(LocationName.cookie_mountain_region, (0x17, 0x05), 0x37757, 0x27, SMWPath(0x04, 0x0E, 0x04)),
    0x0E: SMWLevel(LocationName.twin_bridges_castle_region, (0x1A, 0x03), 0x3773A, 0x24, SMWPath(0x01, 0x76, 0x08)),
    0x12: SMWLevel(LocationName.twin_bridges_star_road, (0x10, 0x0F), 0x377F0, 0xFF),

    0x42: SMWLevel(LocationName.forest_of_illusion_1_region, (0x09, 0x37), 0x37C78, 0x2A, SMWPath(0x01, 0x44, 0x08), SMWPath(0x02, 0x41, 0x01)),
    0x44: SMWLevel(LocationName.forest_of_illusion_2_region, (0x0B, 0x3A), 0x37CAA, 0x2C, SMWPath(0x04, 0x47, 0x08), SMWPath(0x01, 0x45, 0x02)),
    0x47: SMWLevel(LocationName.forest_of_illusion_3_region, (0x09, 0x3C), 0x37CC8, 0x2E, SMWPath(0x02, 0x41, 0x04), SMWPath(0x04, 0x78, 0x01)),
    0x43: SMWLevel(LocationName.forest_of_illusion_4_region, (0x05, 0x3A), 0x37CA4, 0x32, SMWPath(0x01, 0x44, 0x02), SMWPath(0x04, 0x46, 0x08)),
    0x41: SMWLevel(LocationName.forest_ghost_house_region, (0x07, 0x37), 0x37C76, 0x30, SMWPath(0x01, 0x42, 0x02), SMWPath(0x02, 0x43, 0x08)),
    0x46: SMWLevel(LocationName.forest_secret_region, (0x05, 0x3C), 0x37CC4, 0x34, SMWPath(0x04, 0x7A, 0x01)),
    0x45: SMWLevel(LocationName.blue_switch_palace, (0x0D, 0x3A), 0x37CAC, 0x37),
    0x1F: SMWLevel(LocationName.forest_fortress_region, (0x16, 0x10), 0x37906, 0x35, SMWPath(0x02, 0x1E, 0x01)),
    0x20: SMWLevel(LocationName.forest_castle_region, (0x18, 0x12), 0x37928, 0x61, SMWPath(0x04, 0x22, 0x08)),
    0x1E: SMWLevel(LocationName.forest_star_road, (0x14, 0x10), 0x37904, 0x36),

    0x22: SMWLevel(LocationName.chocolate_island_1_region, (0x18, 0x16), 0x37968, 0x62, SMWPath(0x02, 0x21, 0x01)),
    0x24: SMWLevel(LocationName.chocolate_island_2_region, (0x15, 0x1B), 0x379B5, 0x46, SMWPath(0x02, 0x23, 0x01), SMWPath(0x04, 0x68, 0x01)),
    0x23: SMWLevel(LocationName.chocolate_island_3_region, (0x13, 0x1B), 0x379B3, 0x48, SMWPath(0x04, 0x23, 0x08), SMWPath(0x02, 0x1B, 0x01)),
    0x1D: SMWLevel(LocationName.chocolate_island_4_region, (0x0F, 0x1D), 0x378DF, 0x4B, SMWPath(0x02, 0x1C, 0x01)),
    0x1C: SMWLevel(LocationName.chocolate_island_5_region, (0x0C, 0x1D), 0x378DC, 0x4C, SMWPath(0x08, 0x1A, 0x04)),
    0x21: SMWLevel(LocationName.chocolate_ghost_house_region, (0x15, 0x16), 0x37965, 0x63, SMWPath(0x04, 0x24, 0x08)),
    0x1B: SMWLevel(LocationName.chocolate_fortress_region, (0x0F, 0x1B), 0x378BF, 0x4A, SMWPath(0x04, 0x1D, 0x08)),
    0x3B: SMWLevel(LocationName.chocolate_secret_region, (0x18, 0x29), 0x37B97, 0x4F, SMWPath(0x02, 0x6A, 0x02)),
    0x1A: SMWLevel(LocationName.chocolate_castle_region, (0x0C, 0x1B), 0x378BC, 0x4D, SMWPath(0x08, 0x18, 0x02)),

    0x18: SMWLevel(LocationName.sunken_ghost_ship_region, (0x0E, 0x17), 0x3787E, 0x4E, SMWPath(0x08, 0x7C, 0x01)),
    0x3A: SMWLevel(LocationName.valley_of_bowser_1_region, (0x1C, 0x27), 0x37B7B, 0x38, SMWPath(0x02, 0x39, 0x01)),
    0x39: SMWLevel(LocationName.valley_of_bowser_2_region, (0x1A, 0x27), 0x37B79, 0x39, SMWPath(0x02, 0x38, 0x01), SMWPath(0x08, 0x35, 0x04)),
    0x37: SMWLevel(LocationName.valley_of_bowser_3_region, (0x15, 0x27), 0x37B74, 0x3D, SMWPath(0x08, 0x33, 0x04)),
    0x33: SMWLevel(LocationName.valley_of_bowser_4_region, (0x15, 0x25), 0x37B54, 0x3E, SMWPath(0x01, 0x34, 0x02), SMWPath(0x08, 0x30, 0x04)),
    0x38: SMWLevel(LocationName.valley_ghost_house_region, (0x18, 0x27), 0x37B77, 0x3B, SMWPath(0x02, 0x37, 0x01), SMWPath(0x08, 0x34, 0x04)),
    0x35: SMWLevel(LocationName.valley_fortress_region, (0x1A, 0x25), 0x37B59, 0x41, SMWPath(0x08, 0x32, 0x04)),
    0x34: SMWLevel(LocationName.valley_castle_region, (0x18, 0x25), 0x37B57, 0x40, SMWPath(0x08, 0x31, 0x04)),
    0x31: SMWLevel(LocationName.front_door, (0x18, 0x23), 0x37B37, 0x45),
    0x81: SMWLevel(LocationName.front_door, (0x18, 0x23), 0x37B37, 0x45), # Fake Extra Front Door
    0x32: SMWLevel(LocationName.back_door, (0x1A, 0x23), 0x37B39, 0x42),
    0x82: SMWLevel(LocationName.back_door, (0x1A, 0x23), 0x37B39, 0x42), # Fake Extra Back Door
    0x30: SMWLevel(LocationName.valley_star_road, (0x15, 0x23), 0x37B34, 0x44),

    0x5B: SMWLevel(LocationName.star_road_donut, (0x13, 0x3D), 0x37DD3, 0x50),
    0x58: SMWLevel(LocationName.star_road_1_region, (0x15, 0x3A), 0x37DA4, 0x51, None, SMWPath(0x02, 0x53, 0x04)),
    0x53: SMWLevel(LocationName.star_road_vanilla, (0x13, 0x38), 0x37D82, 0x53),
    0x54: SMWLevel(LocationName.star_road_2_region, (0x16, 0x38), 0x37D85, 0x54, None, SMWPath(0x08, 0x52, 0x02)),
    0x52: SMWLevel(LocationName.star_road_twin_bridges, (0x18, 0x36), 0x37D67, 0x56),
    0x56: SMWLevel(LocationName.star_road_3_region, (0x1A, 0x38), 0x37D89, 0x57, None, SMWPath(0x01, 0x57, 0x02)),
    0x57: SMWLevel(LocationName.star_road_forest, (0x1D, 0x38), 0x37D8C, 0x59),
    0x59: SMWLevel(LocationName.star_road_4_region, (0x1B, 0x3A), 0x37DAA, 0x5A, None, SMWPath(0x04, 0x5C, 0x08)),
    0x5C: SMWLevel(LocationName.star_road_valley, (0x1D, 0x3D), 0x37DDC, 0x5C),
    0x5A: SMWLevel(LocationName.star_road_5_region, (0x18, 0x3B), 0x37DB7, 0x5D, SMWPath(0x02, 0x5B, 0x01), SMWPath(0x08, 0x55, 0x04)),
    0x55: SMWLevel(LocationName.star_road_special, (0x18, 0x38), 0x37D87, 0x5F),

    0x4D: SMWLevel(LocationName.special_star_road, (0x12, 0x33), 0x37D31, 0x64),
    0x4E: SMWLevel(LocationName.special_zone_1_region, (0x14, 0x33), 0x37D33, 0x65, SMWPath(0x01, 0x4F, 0x02)),
    0x4F: SMWLevel(LocationName.special_zone_2_region, (0x17, 0x33), 0x37D36, 0x66, SMWPath(0x01, 0x50, 0x02)),
    0x50: SMWLevel(LocationName.special_zone_3_region, (0x1A, 0x33), 0x37D39, 0x67, SMWPath(0x01, 0x51, 0x02)),
    0x51: SMWLevel(LocationName.special_zone_4_region, (0x1D, 0x33), 0x37D3C, 0x68, SMWPath(0x01, 0x4C, 0x01)),
    0x4C: SMWLevel(LocationName.special_zone_5_region, (0x1D, 0x31), 0x37D1C, 0x69, SMWPath(0x02, 0x4B, 0x01)),
    0x4B: SMWLevel(LocationName.special_zone_6_region, (0x1A, 0x31), 0x37D19, 0x6A, SMWPath(0x02, 0x4A, 0x01)),
    0x4A: SMWLevel(LocationName.special_zone_7_region, (0x17, 0x31), 0x37D16, 0x6B, SMWPath(0x02, 0x49, 0x01)),
    0x49: SMWLevel(LocationName.special_zone_8_region, (0x14, 0x31), 0x37D13, 0x6C, SMWPath(0x02, 0x48, 0x01)),
    0x48: SMWLevel(LocationName.special_complete, (0x12, 0x31), 0x37D11, 0x6D),

    0x60: SMWLevel(LocationName.donut_plains_entrance_pipe, (0x09, 0x10), 0xFFFFFF, 0xFF),
    0x61: SMWLevel(LocationName.valley_donut_exit_pipe, (0x11, 0x23), 0xFFFFFF, 0xFF),
    0x62: SMWLevel(LocationName.valley_donut_entrance_pipe, (0x13, 0x21), 0xFFFFFF, 0xFF),
    0x63: SMWLevel(LocationName.donut_plains_exit_pipe, (0x0B, 0x0E), 0xFFFFFF, 0xFF),
    0x64: SMWLevel(LocationName.vanilla_dome_bottom_entrance_pipe, (0x0B, 0x34), 0xFFFFFF, 0xFF),
    0x65: SMWLevel(LocationName.twin_bridges_exit_pipe, (0x11, 0x07), 0xFFFFFF, 0xFF),
    0x66: SMWLevel(LocationName.vanilla_dome_top_entrance_pipe, (0x04, 0x2B), 0xFFFFFF, 0xFF),
    0x67: SMWLevel(LocationName.vanilla_dome_top_exit_pipe, (0x0A, 0x03), 0xFFFFFF, 0xFF),
    0x68: SMWLevel(LocationName.chocolate_island_entrance_pipe, (0x12, 0x17), 0xFFFFFF, 0xFF),
    0x69: SMWLevel(LocationName.valley_chocolate_exit_pipe, (0x1D, 0x29), 0xFFFFFF, 0xFF),
    0x6A: SMWLevel(LocationName.valley_chocolate_entrance_pipe, (0x15, 0x29), 0xFFFFFF, 0xFF),
    0x6B: SMWLevel(LocationName.chocolate_island_exit_pipe, (0x0A, 0x18), 0xFFFFFF, 0xFF),

    0x70: SMWLevel(LocationName.yi_to_ysp, (0x00, 0x00), 0xFFFFFF, 0xFF),
    0x71: SMWLevel(LocationName.ysp_from_yi, (0x00, 0x00), 0xFFFFFF, 0xFF),
    0x72: SMWLevel(LocationName.yi_to_dp, (0x00, 0x00), 0xFFFFFF, 0xFF),
    0x73: SMWLevel(LocationName.dp_from_yi, (0x00, 0x00), 0xFFFFFF, 0xFF),
    0x74: SMWLevel(LocationName.dp_to_vd, (0x00, 0x00), 0xFFFFFF, 0xFF),
    0x75: SMWLevel(LocationName.vd_from_dp, (0x00, 0x00), 0xFFFFFF, 0xFF),
    0x76: SMWLevel(LocationName.tw_to_foi, (0x00, 0x00), 0xFFFFFF, 0xFF),
    0x77: SMWLevel(LocationName.foi_from_tw, (0x00, 0x00), 0xFFFFFF, 0xFF),
    0x78: SMWLevel(LocationName.foi_to_ci, (0x00, 0x00), 0xFFFFFF, 0xFF),
    0x79: SMWLevel(LocationName.ci_from_foi, (0x00, 0x00), 0xFFFFFF, 0xFF),
    0x7A: SMWLevel(LocationName.foi_to_sr, (0x00, 0x00), 0xFFFFFF, 0xFF),
    0x7B: SMWLevel(LocationName.sr_from_foi, (0x00, 0x00), 0xFFFFFF, 0xFF),
    0x7C: SMWLevel(LocationName.ci_to_vob, (0x00, 0x00), 0xFFFFFF, 0xFF),
    0x7D: SMWLevel(LocationName.vob_from_ci, (0x00, 0x00), 0xFFFFFF, 0xFF),
}


banned_spoiler_levels = (
    0x00,
    0x28,
    0x03,
    0x16,
    0x2C,
    0x12,
    0x1E,
    0x31,
    0x32,
    0x30,
    0x5B,
    0x53,
    0x52,
    0x57,
    0x5C,
    0x55,
    0x4D,
    0x48,
)


lockable_tiles = [
    0x14,

    0x15,
    0x09,
    0x0A,
    0x08,
    0x04,
    0x13,
    0x05,
    0x06,
    0x2F,
    0x07,

    0x3E,
    0x3C,
    0x2D,
    0x2B,
    0x2E,
    0x3D,
    0x3F,
    0x01,
    0x02,
    0x0B,
    0x40,

    0x0C,
    0x0D,
    0x0F,
    0x11,
    0x10,
    0x0E,

    0x42,
    0x44,
    0x47,
    0x43,
    0x41,
    0x46,
    0x45,
    0x1F,
    0x20,

    0x22,
    0x24,
    0x23,
    0x1D,
    0x1C,
    0x21,
    0x1B,
    0x3B,
    0x1A,

    0x18,
    0x3A,
    0x39,
    0x37,
    0x33,
    0x38,
    0x35,
    0x34,
    0x58,
    0x54,
    0x56,
    0x59,
    0x5A,
    0x4E,
    0x4F,
    0x50,
    0x51,
    0x4C,
    0x4B,
    0x4A,
    0x49,
]

hard_gameplay_levels = [
    LocationName.vanilla_secret_3_region,
    LocationName.vanilla_fortress_region,
    LocationName.butter_bridge_2_region,
    LocationName.forest_of_illusion_2_region,
    LocationName.forest_fortress_region,
    LocationName.chocolate_fortress_region,
    LocationName.sunken_ghost_ship_region,
    LocationName.valley_of_bowser_4_region,
    LocationName.valley_castle_region,
    LocationName.special_zone_2_region,
    LocationName.special_zone_3_region,
    LocationName.special_zone_5_region,
    LocationName.front_door,
    LocationName.back_door,
]

very_hard_gameplay_levels = [
    LocationName.chocolate_castle_region,
    LocationName.valley_fortress_region,
    LocationName.special_zone_4_region,
    LocationName.special_zone_6_region,
    LocationName.special_zone_7_region,
    LocationName.special_zone_8_region,
]

switch_palace_locations = [
    LocationName.yellow_switch_palace, 
    LocationName.green_switch_palace,
    LocationName.red_switch_palace,
    LocationName.blue_switch_palace
]
castle_locations = [
    LocationName.yoshis_island_castle,
    LocationName.donut_plains_castle,
    LocationName.vanilla_dome_castle,
    LocationName.vanilla_fortress,
    LocationName.twin_bridges_castle,
    LocationName.forest_castle,
    LocationName.forest_fortress,
    LocationName.chocolate_castle,
    LocationName.chocolate_fortress,
    LocationName.valley_castle,
    LocationName.valley_fortress,
]
ghost_house_locations = [
    LocationName.donut_ghost_house_exit_1,
    LocationName.donut_ghost_house_exit_2,
    LocationName.donut_secret_house_exit_1,
    LocationName.donut_secret_house_exit_2,
    LocationName.vanilla_ghost_house_exit_1,
    LocationName.forest_ghost_house_exit_1,
    LocationName.forest_ghost_house_exit_2,
    LocationName.chocolate_ghost_house_exit_1,
    LocationName.valley_ghost_house_exit_1,
    LocationName.valley_ghost_house_exit_2,
]

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

ghost_house_level_ids = [
    0x38,
    0x21,
    0x41,
    0x2B,
    0x04,
    0x13,
]

single_levels = easy_single_levels.copy() + hard_single_levels.copy() + special_zone_levels.copy()
double_levels = easy_double_levels.copy() + hard_double_levels.copy()
castle_levels = easy_castle_fortress_levels.copy() + hard_castle_fortress_levels.copy()

reachable_levels_per_path = {
    LocationName.yoshis_house_tile: [
        0x29, 0x2A, 0x27, 0x26, 0x25,
    ],
    LocationName.ysp_from_yi: [
    ],
    LocationName.dp_from_yi: [
        0x15, 0x09, 0x0A, 0x04, 0x13, 0x05, 0x06, 0x07,
    ],
    LocationName.valley_donut_exit_pipe: [
        0x2F, 
    ],
    LocationName.donut_plains_exit_pipe: [
        0x05, 0x06, 0x07, 
    ],
    LocationName.vd_from_dp: [
        0x3E, 0x3C, 0x2D, 0x2B, 0x2E, 0x3D, 0x40,
    ],
    LocationName.twin_bridges_exit_pipe: [
        0x0F, 0x11, 0x10, 0x0E, 
    ],
    LocationName.vanilla_dome_top_exit_pipe: [
        0x01, 0x02, 0x0B, 0x0C, 0x0D, 0x0E, 
    ],
    LocationName.foi_from_tw: [
        0x42, 0x44, 0x47, 0x43, 0x41, 0x46, 
    ],
    LocationName.sr_from_foi: [
        0x1F, 
    ],
    LocationName.ci_from_foi: [
        0x20, 0x22, 0x24, 0x23, 0x1D, 0x1C, 0x21, 0x1B, 0x1A, 
    ],
    LocationName.chocolate_island_exit_pipe: [
        0x1A, 
    ],
    LocationName.valley_chocolate_exit_pipe: [
        0x3B, 
    ],
    LocationName.vob_from_ci: [
        0x3A, 0x39, 0x37, 0x33, 0x38, 0x35, 0x34, 0x31, 0x32,
    ],
    LocationName.star_road_donut: [
        0x58, 0x54, 0x56, 0x59, 0x5A, 
    ],
    LocationName.star_road_vanilla: [
        0x58, 0x54, 0x56, 0x59, 0x5A, 
    ],
    LocationName.star_road_twin_bridges: [
        0x58, 0x54, 0x56, 0x59, 0x5A, 
    ],
    LocationName.star_road_forest: [
        0x58, 0x54, 0x56, 0x59, 0x5A, 
    ],
    LocationName.star_road_valley: [
        0x58, 0x54, 0x56, 0x59, 0x5A, 
    ],
    LocationName.special_star_road: [
        0x4D, 0x4E, 0x4F, 0x50, 0x51, 0x4C, 0x4B, 0x4A, 0x49, 
    ],
}

possible_starting_entrances = [
    LocationName.yoshis_house_tile,
    LocationName.dp_from_yi,
    LocationName.vd_from_dp,
    LocationName.foi_from_tw,
    LocationName.special_star_road,
]

def generate_level_list(world: "WaffleWorld"):
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

    easy_single_levels_copy = easy_single_levels.copy()
    hard_single_levels_copy = hard_single_levels.copy()
    easy_double_levels_copy = easy_double_levels.copy()
    hard_double_levels_copy = hard_double_levels.copy()
    easy_castle_fortress_levels_copy = easy_castle_fortress_levels.copy()
    hard_castle_fortress_levels_copy = hard_castle_fortress_levels.copy()
    switch_palace_levels_copy = switch_palace_levels.copy()
    special_zone_levels_copy = special_zone_levels.copy()

    # Move levels to another list depending on certain settings
    if world.options.game_logic_difficulty == "easy":
        # Move Butter Bridge 2 to hard levels on easy logic
        swap_level(0x0D, easy_single_levels_copy, hard_single_levels_copy)
    
    if "Yellow Switch Palace Blocks" in world.options.block_checks.value:
        # Move Yoshi's Island 3 to hard levels if block checks are enabled
        swap_level(0x27, easy_single_levels_copy, hard_single_levels_copy)

    if "Green Switch Palace Blocks" in world.options.block_checks.value:
        # Move Donut Plains 1 to hard levels if block checks are enabled
        swap_level(0x15, easy_double_levels_copy, hard_double_levels_copy)

    if world.options.enemy_shuffle:
        # Move Butter Bridge 1 to hard levels if enemy shuffle is enabled
        swap_level(0x0C, easy_single_levels_copy, hard_single_levels_copy)
        # Move Butter Bridge 2 to hard levels if enemy shuffle is enabled
        swap_level(0x0D, easy_single_levels_copy, hard_single_levels_copy)

    # Shuffle levels
    world.random.shuffle(easy_castle_fortress_levels_copy)
    world.random.shuffle(hard_castle_fortress_levels_copy)
    world.random.shuffle(easy_single_levels_copy)
    world.random.shuffle(hard_single_levels_copy)
    world.random.shuffle(easy_double_levels_copy)
    world.random.shuffle(hard_double_levels_copy)
    world.random.shuffle(switch_palace_levels_copy)

    # Ensure the dict has a very specific order
    shuffled_level_dict = {level_id: 0x00 for level_id in full_level_list}

    # Hardcode some levels/stars
    shuffled_level_dict[0x28] = 0x03
    shuffled_level_dict[0x14] = 0x14
    shuffled_level_dict[0x08] = 0x08
    shuffled_level_dict[0x03] = 0x28
    shuffled_level_dict[0x16] = 0x16
    shuffled_level_dict[0x3F] = 0x3F
    shuffled_level_dict[0x2C] = 0x2C
    shuffled_level_dict[0x12] = 0x12
    shuffled_level_dict[0x45] = 0x45
    shuffled_level_dict[0x1E] = 0x1E
    shuffled_level_dict[0x18] = 0x18
    shuffled_level_dict[0x30] = 0x30
    shuffled_level_dict[0x5B] = 0x5B
    shuffled_level_dict[0x53] = 0x53
    shuffled_level_dict[0x52] = 0x52
    shuffled_level_dict[0x57] = 0x57
    shuffled_level_dict[0x5C] = 0x5C
    shuffled_level_dict[0x55] = 0x55
    shuffled_level_dict[0x48] = 0x48

    if world.options.bowser_castle_doors == "fast":
        shuffled_level_dict[0x31] = 0x82
        shuffled_level_dict[0x32] = 0x32
    elif world.options.bowser_castle_doors == "slow":
        shuffled_level_dict[0x31] = 0x31
        shuffled_level_dict[0x32] = 0x81
    else:
        shuffled_level_dict[0x31] = 0x31
        shuffled_level_dict[0x32] = 0x32
    
    single_levels_copy = (easy_single_levels_copy.copy() + hard_single_levels_copy.copy())
    #if world.options.exclude_special_zone:
    #     for level_id in special_zone_levels:
    #         shuffled_level_dict[level_id] = level_id
    #else:
    #    single_levels_copy.extend(special_zone_levels_copy.copy())
    single_levels_copy.extend(special_zone_levels_copy.copy())

    double_levels_copy = (easy_double_levels_copy.copy() + hard_double_levels_copy.copy())
    castle_fortress_levels_copy = (easy_castle_fortress_levels_copy.copy() + hard_castle_fortress_levels_copy.copy())
        
    remaining_exits = list(world.local_region_mapping.keys())
    starting_location = possible_starting_entrances[world.options.starting_location.value]
    check_next_exits = [starting_location]
    path_count = 0

    while len(remaining_exits) != 0:
        cache_exits = check_next_exits.copy()
        for exit in cache_exits:
            if exit not in remaining_exits:
                continue
            remaining_exits.remove(exit)
            check_next_exits.remove(exit)
            for entrance in world.local_region_mapping[exit]:
                if entrance not in world.local_mapping.keys():
                    continue
                check_next_exits.append(world.local_mapping[entrance])

            # Shuffle everything once we visit 4 paths
            path_count += 1
            if path_count == 4:
                world.random.shuffle(single_levels_copy)
                world.random.shuffle(castle_fortress_levels_copy)
                world.random.shuffle(double_levels_copy)

            if len(reachable_levels_per_path[exit]) == 0:
                continue

            for level_id in reachable_levels_per_path[exit]:
                if shuffled_level_dict[level_id] != 0x00:
                    continue
                if level_id in single_levels:
                    shuffled_level_dict[level_id] = single_levels_copy.pop(0)
                elif level_id in double_levels:
                    level_pop = double_levels_copy.pop(0)
                    shuffled_level_dict[level_id] = level_pop
                    if level_pop not in world.ordered_double_exits:
                        world.ordered_double_exits.append(level_pop)
                elif level_id in castle_levels:
                    shuffled_level_dict[level_id] = castle_fortress_levels_copy.pop(0)

    shuffled_level_list = []
    for level_id in full_level_list:
        shuffled_level_list.append(shuffled_level_dict[level_id])

    return shuffled_level_list


def generate_swapped_exits(world: "WaffleWorld"):
    if world.options.swap_exit_count.value:
        if len(world.ordered_double_exits) == 0:
            level_list = easy_double_levels + hard_double_levels
        else:
            level_list = world.ordered_double_exits.copy()
        level_list.remove(0x5A)
        level_list.remove(0x13)
        level_list.reverse()
        level_weights = [100-((x+1)*15) if 100-((x+1)*15) >= 45 else 45 for x in range(len(level_list))]
        remaining = world.options.swap_exit_count.value
        while remaining > 0:
            chance = level_weights.pop(0)
            level_id = level_list.pop(0)
            if world.random.randint(0, 100) <= chance:
                world.swapped_exits.append(level_id)
                remaining -= 1
            else:
                level_weights.append(chance+10)
                level_list.append(level_id)

    if world.options.swap_donut_gh_exits and 0x04 not in world.swapped_exits:
        world.swapped_exits.append(0x04)


def generate_carryless_exits(world: "WaffleWorld"):
    if world.options.carryless_exits.value:
        if len(world.ordered_double_exits) == 0:
            level_list = easy_double_levels + hard_double_levels
        else:
            level_list = world.ordered_double_exits.copy()
        level_list.remove(0x04)
        level_list.remove(0x13)
        level_list.remove(0x2D)
        level_list.remove(0x0F)
        level_list.remove(0x41)
        level_list.remove(0x23)
        level_weights = [100-((x+2)*8) if 100-((x+2)*8) >= 50 else 50 for x in range(len(level_list))]
        remaining = world.options.carryless_exits.value
        while remaining > 0:
            chance = level_weights.pop(0)
            level_id = level_list.pop(0)
            if world.random.randint(0, 100) <= chance:
                world.carryless_exits.append(level_id)
                remaining -= 1
            else:
                level_weights.append(chance+10)
                level_list.append(level_id)


def swap_level(level_id: int, source: list[int], destination: list[int]):
    if level_id not in source:
        return
    source.remove(level_id)
    destination.append(level_id)
