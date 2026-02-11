import typing

from BaseClasses import Location
from .Names import LocationName
from .Options import Goal
from .Levels import castle_locations, ghost_house_locations, switch_palace_locations

from typing import TYPE_CHECKING, Dict
if TYPE_CHECKING:
    from . import WaffleWorld

class WaffleLocation(Location):
    game: str = "SMW: Spicy Mycena Waffles"

    def __init__(self, player: int, name: str = '', address: int = None, parent=None, prog_byte: int = None, prog_bit: int = None):
        super().__init__(player, name, address, parent)
        self.progress_byte = prog_byte
        self.progress_bit  = prog_bit

NORMAL_EXIT = 0x000000
SECRET_EXIT = 0x100000
DRAGON_COINS = 0x300000
MOON = 0x400000
HIDDEN = 0x500000
CHECKPOINT = 0x600000
PRIZE = 0x700000
ROOM = 0x800000
ENEMY = 0x900000
BLOCK = 0xA00000
GOAL = 0xF00000

YI1 = 0x29000000
YI2 = 0x2A000000
YI3 = 0x27000000
YI4 = 0x26000000
YIC = 0x25000000
YSP = 0x14000000

DP1 = 0x15000000
DP2 = 0x09000000
DP3 = 0x05000000
DP4 = 0x06000000
DS1 = 0x0A000000
DS2 = 0x2F000000
DGH = 0x04000000
DSH = 0x13000000
DPC = 0x07000000
GSP = 0x08000000

VD1 = 0x3E000000
VD2 = 0x3C000000
VD3 = 0x2E000000
VD4 = 0x3D000000
VS1 = 0x2D000000
VS2 = 0x01000000
VS3 = 0x02000000
VDH = 0x2B000000
VDF = 0x0B000000
VDC = 0x40000000
RSP = 0x3F000000

BB1 = 0x0C000000
BB2 = 0x0D000000
CBA = 0x0F000000
COM = 0x10000000
SOL = 0x11000000
TWC = 0x0E000000

FI1 = 0x42000000
FI2 = 0x44000000
FI3 = 0x47000000
FI4 = 0x43000000
FGH = 0x41000000
FSA = 0x46000000
FIF = 0x1F000000
FIC = 0x20000000
BSP = 0x45000000

CI1 = 0x22000000
CI2 = 0x24000000
CI3 = 0x23000000
CI4 = 0x1D000000
CI5 = 0x1C000000
CGH = 0x21000000
CSA = 0x3B000000
CIF = 0x1B000000
CIC = 0x1A000000

SGS = 0x18000000

VB1 = 0x3A000000
VB2 = 0x39000000
VB3 = 0x37000000
VB4 = 0x33000000
VBH = 0x38000000
VBF = 0x35000000
VBC = 0x34000000

SR1 = 0x58000000
SR2 = 0x54000000
SR3 = 0x56000000
SR4 = 0x59000000
SR5 = 0x5A000000

SZ1 = 0x4E000000
SZ2 = 0x4F000000
SZ3 = 0x50000000
SZ4 = 0x51000000
SZ5 = 0x4C000000
SZ6 = 0x4B000000
SZ7 = 0x4A000000
SZ8 = 0x49000000


level_location_table = {
    LocationName.yoshis_island_1_exit_1:  NORMAL_EXIT | YI1,
    LocationName.yoshis_island_2_exit_1:  NORMAL_EXIT | YI2,
    LocationName.yoshis_island_3_exit_1:  NORMAL_EXIT | YI3,
    LocationName.yoshis_island_4_exit_1:  NORMAL_EXIT | YI4,
    LocationName.yoshis_island_castle:    NORMAL_EXIT | YIC,

    LocationName.yellow_switch_palace: NORMAL_EXIT | YSP,

    LocationName.donut_plains_1_exit_1:     NORMAL_EXIT | DP1,
    LocationName.donut_plains_1_exit_2:     SECRET_EXIT | DP1,
    LocationName.donut_plains_2_exit_1:     NORMAL_EXIT | DP2,
    LocationName.donut_plains_2_exit_2:     SECRET_EXIT | DP2,
    LocationName.donut_plains_3_exit_1:     NORMAL_EXIT | DP3,
    LocationName.donut_plains_4_exit_1:     NORMAL_EXIT | DP4,
    LocationName.donut_secret_1_exit_1:     NORMAL_EXIT | DS1,
    LocationName.donut_secret_1_exit_2:     SECRET_EXIT | DS1,
    LocationName.donut_secret_2_exit_1:     NORMAL_EXIT | DS2,
    LocationName.donut_ghost_house_exit_1:  NORMAL_EXIT | DGH,
    LocationName.donut_ghost_house_exit_2:  SECRET_EXIT | DGH,
    LocationName.donut_secret_house_exit_1: NORMAL_EXIT | DSH,
    LocationName.donut_secret_house_exit_2: SECRET_EXIT | DSH,
    LocationName.donut_plains_castle:       NORMAL_EXIT | DPC,

    LocationName.green_switch_palace: NORMAL_EXIT | GSP,

    LocationName.vanilla_dome_1_exit_1: NORMAL_EXIT | VD1,
    LocationName.vanilla_dome_1_exit_2: SECRET_EXIT | VD1,
    LocationName.vanilla_dome_2_exit_1: NORMAL_EXIT | VD2,
    LocationName.vanilla_dome_2_exit_2: SECRET_EXIT | VD2,
    LocationName.vanilla_dome_3_exit_1: NORMAL_EXIT | VD3,
    LocationName.vanilla_dome_4_exit_1: NORMAL_EXIT | VD4,
    LocationName.vanilla_secret_1_exit_1: NORMAL_EXIT | VS1,
    LocationName.vanilla_secret_1_exit_2: SECRET_EXIT | VS1,
    LocationName.vanilla_secret_2_exit_1: NORMAL_EXIT | VS2,
    LocationName.vanilla_secret_3_exit_1: NORMAL_EXIT | VS3,
    LocationName.vanilla_ghost_house_exit_1: NORMAL_EXIT | VDH,
    LocationName.vanilla_fortress: NORMAL_EXIT | VDF,
    LocationName.vanilla_dome_castle: NORMAL_EXIT | VDC,

    LocationName.red_switch_palace: NORMAL_EXIT | RSP,

    LocationName.butter_bridge_1_exit_1: NORMAL_EXIT | BB1,
    LocationName.butter_bridge_2_exit_1: NORMAL_EXIT | BB2,
    LocationName.cheese_bridge_exit_1: NORMAL_EXIT | CBA,
    LocationName.cheese_bridge_exit_2: SECRET_EXIT | CBA,
    LocationName.cookie_mountain_exit_1: NORMAL_EXIT | COM,
    LocationName.soda_lake_exit_1: NORMAL_EXIT | SOL,
    LocationName.twin_bridges_castle:     NORMAL_EXIT | TWC,

    LocationName.forest_of_illusion_1_exit_1: NORMAL_EXIT | FI1,
    LocationName.forest_of_illusion_1_exit_2: SECRET_EXIT | FI1,
    LocationName.forest_of_illusion_2_exit_1: NORMAL_EXIT | FI2,
    LocationName.forest_of_illusion_2_exit_2: SECRET_EXIT | FI2,
    LocationName.forest_of_illusion_3_exit_1: NORMAL_EXIT | FI3,
    LocationName.forest_of_illusion_3_exit_2: SECRET_EXIT | FI3,
    LocationName.forest_of_illusion_4_exit_1: NORMAL_EXIT | FI4,
    LocationName.forest_of_illusion_4_exit_2: SECRET_EXIT | FI4,
    LocationName.forest_ghost_house_exit_1: NORMAL_EXIT | FGH,
    LocationName.forest_ghost_house_exit_2: SECRET_EXIT | FGH,
    LocationName.forest_secret_exit_1: NORMAL_EXIT | FSA,
    LocationName.forest_fortress: NORMAL_EXIT | FIF,
    LocationName.forest_castle: NORMAL_EXIT | FIC,

    LocationName.blue_switch_palace: NORMAL_EXIT | BSP,

    LocationName.chocolate_island_1_exit_1: NORMAL_EXIT | CI1,
    LocationName.chocolate_island_2_exit_1: NORMAL_EXIT | CI2,
    LocationName.chocolate_island_2_exit_2: SECRET_EXIT | CI2,
    LocationName.chocolate_island_3_exit_1: NORMAL_EXIT | CI3,
    LocationName.chocolate_island_3_exit_2: SECRET_EXIT | CI3,
    LocationName.chocolate_island_4_exit_1: NORMAL_EXIT | CI4,
    LocationName.chocolate_island_5_exit_1: NORMAL_EXIT | CI5,
    LocationName.chocolate_ghost_house_exit_1: NORMAL_EXIT | CGH,
    LocationName.chocolate_secret_exit_1: NORMAL_EXIT | CSA,
    LocationName.chocolate_fortress: NORMAL_EXIT | CIF,
    LocationName.chocolate_castle: NORMAL_EXIT | CIC,

    LocationName.sunken_ghost_ship: NORMAL_EXIT | SGS,

    LocationName.valley_of_bowser_1_exit_1: NORMAL_EXIT | VB1,
    LocationName.valley_of_bowser_2_exit_1: NORMAL_EXIT | VB2,
    LocationName.valley_of_bowser_2_exit_2: SECRET_EXIT | VB2,
    LocationName.valley_of_bowser_3_exit_1: NORMAL_EXIT | VB3,
    LocationName.valley_of_bowser_4_exit_1: NORMAL_EXIT | VB4,
    LocationName.valley_of_bowser_4_exit_2: SECRET_EXIT | VB4,
    LocationName.valley_ghost_house_exit_1: NORMAL_EXIT | VBH,
    LocationName.valley_ghost_house_exit_2: SECRET_EXIT | VBH,
    LocationName.valley_fortress: NORMAL_EXIT | VBF,
    LocationName.valley_castle: NORMAL_EXIT | VBC,

    LocationName.star_road_1_exit_1: NORMAL_EXIT | SR1,
    LocationName.star_road_1_exit_2: SECRET_EXIT | SR1,
    LocationName.star_road_2_exit_1: NORMAL_EXIT | SR2,
    LocationName.star_road_2_exit_2: SECRET_EXIT | SR2,
    LocationName.star_road_3_exit_1: NORMAL_EXIT | SR3,
    LocationName.star_road_3_exit_2: SECRET_EXIT | SR3,
    LocationName.star_road_4_exit_1: NORMAL_EXIT | SR4,
    LocationName.star_road_4_exit_2: SECRET_EXIT | SR4,
    LocationName.star_road_5_exit_1: NORMAL_EXIT | SR5,
    LocationName.star_road_5_exit_2: SECRET_EXIT | SR5,

    LocationName.special_zone_1_exit_1: NORMAL_EXIT | SZ1,
    LocationName.special_zone_2_exit_1: NORMAL_EXIT | SZ2,
    LocationName.special_zone_3_exit_1: NORMAL_EXIT | SZ3,
    LocationName.special_zone_4_exit_1: NORMAL_EXIT | SZ4,
    LocationName.special_zone_5_exit_1: NORMAL_EXIT | SZ5,
    LocationName.special_zone_6_exit_1: NORMAL_EXIT | SZ6,
    LocationName.special_zone_7_exit_1: NORMAL_EXIT | SZ7,
    LocationName.special_zone_8_exit_1: NORMAL_EXIT | SZ8,
}

dragon_coin_location_table = {
    LocationName.yoshis_island_1_dragon: DRAGON_COINS | YI1,
    LocationName.yoshis_island_2_dragon: DRAGON_COINS | YI2,
    LocationName.yoshis_island_3_dragon: DRAGON_COINS | YI3,
    LocationName.yoshis_island_4_dragon: DRAGON_COINS | YI4,

    LocationName.donut_plains_1_dragon: DRAGON_COINS | DP1,
    LocationName.donut_plains_2_dragon: DRAGON_COINS | DP2,
    LocationName.donut_plains_3_dragon: DRAGON_COINS | DP3,
    LocationName.donut_plains_4_dragon: DRAGON_COINS | DP4,
    LocationName.donut_secret_1_dragon: DRAGON_COINS | DS1,
    LocationName.donut_secret_2_dragon: DRAGON_COINS | DS2,

    LocationName.vanilla_dome_1_dragon: DRAGON_COINS | VD1,
    LocationName.vanilla_dome_2_dragon: DRAGON_COINS | VD2,
    LocationName.vanilla_dome_3_dragon: DRAGON_COINS | VD3,
    LocationName.vanilla_dome_4_dragon: DRAGON_COINS | VD4,
    LocationName.vanilla_secret_1_dragon: DRAGON_COINS | VS1,
    LocationName.vanilla_secret_2_dragon: DRAGON_COINS | VS2,
    LocationName.vanilla_secret_3_dragon: DRAGON_COINS | VS3,
    LocationName.vanilla_ghost_house_dragon: DRAGON_COINS | VDH,

    LocationName.butter_bridge_1_dragon: DRAGON_COINS | BB1,
    LocationName.butter_bridge_2_dragon: DRAGON_COINS | BB2,
    LocationName.cheese_bridge_dragon: DRAGON_COINS | CBA,
    LocationName.cookie_mountain_dragon: DRAGON_COINS | COM,
    LocationName.soda_lake_dragon: DRAGON_COINS | SOL,

    LocationName.forest_of_illusion_2_dragon: DRAGON_COINS | FI2,
    LocationName.forest_of_illusion_3_dragon: DRAGON_COINS | FI3,
    LocationName.forest_of_illusion_4_dragon: DRAGON_COINS | FI4,
    LocationName.forest_ghost_house_dragon: DRAGON_COINS | FGH,
    LocationName.forest_secret_dragon: DRAGON_COINS | FSA,
    LocationName.forest_castle_dragon: DRAGON_COINS | FIC,

    LocationName.chocolate_island_1_dragon: DRAGON_COINS | CI1,
    LocationName.chocolate_island_2_dragon: DRAGON_COINS | CI2,
    LocationName.chocolate_island_3_dragon: DRAGON_COINS | CI3,
    LocationName.chocolate_island_4_dragon: DRAGON_COINS | CI4,
    LocationName.chocolate_island_5_dragon: DRAGON_COINS | CI5,

    LocationName.sunken_ghost_ship_dragon: DRAGON_COINS | SGS,

    LocationName.valley_of_bowser_1_dragon: DRAGON_COINS | VB1,
    LocationName.valley_of_bowser_2_dragon: DRAGON_COINS | VB2,
    LocationName.valley_of_bowser_3_dragon: DRAGON_COINS | VB3,
    LocationName.valley_ghost_house_dragon: DRAGON_COINS | VBH,
    LocationName.valley_castle_dragon: DRAGON_COINS | VBC,

    LocationName.star_road_1_dragon: DRAGON_COINS | SR1,

    LocationName.special_zone_1_dragon: DRAGON_COINS | SZ1,
    LocationName.special_zone_2_dragon: DRAGON_COINS | SZ2,
    LocationName.special_zone_3_dragon: DRAGON_COINS | SZ3,
    LocationName.special_zone_4_dragon: DRAGON_COINS | SZ4,
    LocationName.special_zone_5_dragon: DRAGON_COINS | SZ5,
    LocationName.special_zone_6_dragon: DRAGON_COINS | SZ6,
    LocationName.special_zone_7_dragon: DRAGON_COINS | SZ7,
    LocationName.special_zone_8_dragon: DRAGON_COINS | SZ8,
}

moon_location_table = {
    LocationName.yoshis_island_1_moon: MOON | YI1,
    LocationName.donut_plains_4_moon: MOON | DP4,
    LocationName.vanilla_dome_3_moon: MOON | VD3,
    LocationName.cheese_bridge_moon: MOON | CBA,
    LocationName.forest_ghost_house_moon: MOON | FGH,
    LocationName.chocolate_island_1_moon: MOON | CI1,
    LocationName.valley_of_bowser_1_moon: MOON | VB1,
}

hidden_1ups_location_table = {
    LocationName.yoshis_island_4_hidden_1up: HIDDEN | YI4,
    LocationName.donut_plains_1_hidden_1up: HIDDEN | DP1,
    LocationName.donut_plains_4_hidden_1up: HIDDEN | DP4,
    LocationName.donut_plains_castle_hidden_1up: HIDDEN | DPC,
    LocationName.vanilla_dome_4_hidden_1up: HIDDEN | VD4,
    LocationName.vanilla_ghost_house_hidden_1up: HIDDEN | VDH,
    LocationName.vanilla_fortress_hidden_1up: HIDDEN | VDF,
    LocationName.cookie_mountain_hidden_1up: HIDDEN | COM,
    LocationName.forest_of_illusion_3_hidden_1up: HIDDEN | FI3,
    LocationName.chocolate_island_2_hidden_1up: HIDDEN | CI2,
    LocationName.chocolate_castle_hidden_1up: HIDDEN | CIC,
    LocationName.valley_of_bowser_2_hidden_1up: HIDDEN | VB2,
    LocationName.valley_castle_hidden_1up: HIDDEN | VBC,
    LocationName.special_zone_1_hidden_1up: HIDDEN | SZ1,
}

prize_location_table = {
    LocationName.yoshis_island_3_prize: PRIZE | YI3,
    LocationName.donut_plains_3_prize: PRIZE | DP3,
    LocationName.butter_bridge_1_prize: PRIZE | BB1,
    LocationName.chocolate_island_3_prize: PRIZE | CI3,
}

room_location_table = {
    LocationName.yoshis_island_1_room_1: ROOM | YI1 | 0x0105,
    LocationName.yoshis_island_1_room_2: ROOM | YI1 | 0x01CB,
    LocationName.yoshis_island_2_room_1: ROOM | YI2 | 0x0106,
    LocationName.yoshis_island_2_room_2: ROOM | YI2 | 0x01CA,
    LocationName.yoshis_island_3_room_1: ROOM | YI3 | 0x0103,
    LocationName.yoshis_island_3_room_2: ROOM | YI3 | 0x01FD,
    LocationName.yoshis_island_4_room_1: ROOM | YI4 | 0x0102,
    LocationName.yoshis_island_4_room_2: ROOM | YI4 | 0x01BE,
    LocationName.yoshis_island_4_room_3: ROOM | YI4 | 0x01FF,
    LocationName.yoshis_island_castle_room_1: ROOM | YIC | 0x0101,
    LocationName.yoshis_island_castle_room_2: ROOM | YIC | 0x01FC,
    #LocationName.yoshis_island_castle_room_3: ROOM | YIC | 0x01F6,
    LocationName.yellow_switch_palace_room_1: ROOM | YSP | 0x0014,
    LocationName.yellow_switch_palace_room_2: ROOM | YSP | 0x00CA,

    LocationName.donut_plains_1_room_1: ROOM | DP1 | 0x0015,
    LocationName.donut_plains_1_room_2: ROOM | DP1 | 0x00FD,
    LocationName.donut_plains_1_room_3: ROOM | DP1 | 0x00E3,
    LocationName.donut_plains_2_room_1: ROOM | DP2 | 0x0009,
    LocationName.donut_plains_2_room_2: ROOM | DP2 | 0x00E9,
    LocationName.donut_plains_2_room_3: ROOM | DP2 | 0x00FF,
    LocationName.donut_plains_3_room_1: ROOM | DP3 | 0x0005,
    LocationName.donut_plains_3_room_2: ROOM | DP3 | 0x00F4,
    LocationName.donut_plains_4_room_1: ROOM | DP4 | 0x0006,
    LocationName.donut_plains_4_room_2: ROOM | DP4 | 0x00C3,
    LocationName.donut_plains_4_room_3: ROOM | DP4 | 0x00D2,
    LocationName.donut_secret_1_room_1: ROOM | DS1 | 0x000A,
    LocationName.donut_secret_1_room_2: ROOM | DS1 | 0x00C2,
    LocationName.donut_secret_2_room_1: ROOM | DS2 | 0x010B,
    LocationName.donut_secret_2_room_2: ROOM | DS2 | 0x01C6,
    LocationName.donut_ghost_house_room_1: ROOM | DGH | 0x0004,
    LocationName.donut_ghost_house_room_2: ROOM | DGH | 0x00C4,
    LocationName.donut_ghost_house_room_3: ROOM | DGH | 0x00F9,
    LocationName.donut_ghost_house_room_4: ROOM | DGH | 0x00FE,
    LocationName.donut_ghost_house_room_5: ROOM | DGH | 0x00FA,
    LocationName.donut_ghost_house_room_6: ROOM | DGH | 0x00EB,
    LocationName.donut_secret_house_room_1: ROOM | DSH | 0x0013,
    LocationName.donut_secret_house_room_2: ROOM | DSH | 0x00ED,
    LocationName.donut_secret_house_room_3: ROOM | DSH | 0x00F1,
    LocationName.donut_secret_house_room_4: ROOM | DSH | 0x00F0,
    LocationName.donut_secret_house_room_5: ROOM | DSH | 0x00E4,
    LocationName.donut_plains_castle_room_1: ROOM | DPC | 0x0007,
    LocationName.donut_plains_castle_room_2: ROOM | DPC | 0x00E6,
    LocationName.donut_plains_castle_room_3: ROOM | DPC | 0x00E8,
    LocationName.donut_plains_castle_room_4: ROOM | DPC | 0x00E7,
    #LocationName.donut_plains_castle_room_5: ROOM | DPC | 0x00E5,
    LocationName.green_switch_palace_room_1: ROOM | GSP | 0x0008,
    LocationName.green_switch_palace_room_2: ROOM | GSP | 0x00C9,

    LocationName.vanilla_dome_1_room_1: ROOM | VD1 | 0x011A,
    LocationName.vanilla_dome_1_room_2: ROOM | VD1 | 0x01EF,
    LocationName.vanilla_dome_2_room_1: ROOM | VD2 | 0x0118,
    LocationName.vanilla_dome_2_room_2: ROOM | VD2 | 0x01C3,
    LocationName.vanilla_dome_3_room_1: ROOM | VD3 | 0x010A,
    LocationName.vanilla_dome_3_room_2: ROOM | VD3 | 0x01F7,
    LocationName.vanilla_dome_3_room_3: ROOM | VD3 | 0x01C2,
    LocationName.vanilla_dome_4_room_1: ROOM | VD4 | 0x0119,
    LocationName.vanilla_dome_4_room_2: ROOM | VD4 | 0x01F5,
    LocationName.vanilla_secret_1_room_1: ROOM | VS1 | 0x0109,
    LocationName.vanilla_secret_1_room_2: ROOM | VS1 | 0x01F1,
    LocationName.vanilla_secret_1_room_3: ROOM | VS1 | 0x01F0,
    LocationName.vanilla_secret_2_room_1: ROOM | VS2 | 0x0001,
    LocationName.vanilla_secret_2_room_2: ROOM | VS2 | 0x00D8,
    LocationName.vanilla_secret_3_room_1: ROOM | VS3 | 0x0002,
    LocationName.vanilla_secret_3_room_2: ROOM | VS3 | 0x00CB,
    LocationName.vanilla_ghost_house_room_1: ROOM | VDH | 0x0107,
    LocationName.vanilla_ghost_house_room_2: ROOM | VDH | 0x01EA,
    LocationName.vanilla_ghost_house_room_3: ROOM | VDH | 0x01F9,
    LocationName.vanilla_fortress_room_1: ROOM | VDF | 0x000B,
    LocationName.vanilla_fortress_room_2: ROOM | VDF | 0x10E0,
    #LocationName.vanilla_fortress_room_3: ROOM | VDF | 0x00DF,
    LocationName.vanilla_dome_castle_room_1: ROOM | VDC | 0x011C,
    LocationName.vanilla_dome_castle_room_2: ROOM | VDC | 0x01F4,
    LocationName.vanilla_dome_castle_room_3: ROOM | VDC | 0x01F3,
    #LocationName.vanilla_dome_castle_room_4: ROOM | VDC | 0x01F2,
    LocationName.red_switch_palace_room_1: ROOM | RSP | 0x011B,
    LocationName.red_switch_palace_room_2: ROOM | RSP | 0x01D8,

    LocationName.butter_bridge_1_room_1: ROOM | BB1 | 0x000C,
    LocationName.butter_bridge_1_room_2: ROOM | BB1 | 0x00F3,
    LocationName.butter_bridge_2_room_1: ROOM | BB2 | 0x000D,
    LocationName.butter_bridge_2_room_2: ROOM | BB2 | 0x00DD,
    LocationName.cheese_bridge_room_1: ROOM | CBA | 0x000F,
    LocationName.cheese_bridge_room_2: ROOM | CBA | 0x00BF,
    LocationName.cheese_bridge_room_3: ROOM | CBA | 0x20C8,
    LocationName.cookie_mountain_room_1: ROOM | COM | 0x0010,
    LocationName.cookie_mountain_room_2: ROOM | COM | 0x00C1,
    LocationName.soda_lake_room_1: ROOM | SOL | 0x0011,
    LocationName.soda_lake_room_2: ROOM | SOL | 0x00C6,
    LocationName.twin_bridges_castle_room_1: ROOM | TWC | 0x000E,
    LocationName.twin_bridges_castle_room_2: ROOM | TWC | 0x00DA,
    LocationName.twin_bridges_castle_room_3: ROOM | TWC | 0x00DC,
    LocationName.twin_bridges_castle_room_4: ROOM | TWC | 0x00DB,
    #LocationName.twin_bridges_castle_room_5: ROOM | TWC | 0x00D9,

    LocationName.forest_of_illusion_1_room_1: ROOM | FI1 | 0x011E,
    LocationName.forest_of_illusion_2_room_1: ROOM | FI2 | 0x0120,
    LocationName.forest_of_illusion_3_room_1: ROOM | FI3 | 0x0123,
    LocationName.forest_of_illusion_3_room_2: ROOM | FI3 | 0x01BC,
    LocationName.forest_of_illusion_3_room_3: ROOM | FI3 | 0x01F8,
    LocationName.forest_of_illusion_4_room_1: ROOM | FI4 | 0x011F,
    LocationName.forest_of_illusion_4_room_2: ROOM | FI4 | 0x01DF,
    LocationName.forest_of_illusion_4_room_3: ROOM | FI4 | 0x01C1,
    LocationName.forest_ghost_house_room_1: ROOM | FGH | 0x011D,
    LocationName.forest_ghost_house_room_2: ROOM | FGH | 0x01FA,
    LocationName.forest_ghost_house_room_3: ROOM | FGH | 0x01E7,
    LocationName.forest_ghost_house_room_4: ROOM | FGH | 0x01E6,
    LocationName.forest_secret_room_1: ROOM | FSA | 0x0122,
    LocationName.forest_fortress_room_1: ROOM | FIF | 0x001F,
    LocationName.forest_fortress_room_2: ROOM | FIF | 0x00D6,
    #LocationName.forest_fortress_room_3: ROOM | FIF | 0x00D5,
    LocationName.forest_castle_room_1: ROOM | FIC | 0x0020,
    #LocationName.forest_castle_room_2: ROOM | FIC | 0x00CC,
    LocationName.blue_switch_palace_room_1: ROOM | BSP | 0x0121,
    LocationName.blue_switch_palace_room_2: ROOM | BSP | 0x01D7,

    LocationName.chocolate_island_1_room_1: ROOM | CI1 | 0x0022,
    LocationName.chocolate_island_1_room_2: ROOM | CI1 | 0x00BE,
    LocationName.chocolate_island_2_room_1: ROOM | CI2 | 0x0024,
    LocationName.chocolate_island_2_room_2: ROOM | CI2 | 0x00CF,
    LocationName.chocolate_island_2_room_3: ROOM | CI2 | 0x00CE,
    LocationName.chocolate_island_2_room_4: ROOM | CI2 | 0x00CD,
    LocationName.chocolate_island_3_room_1: ROOM | CI3 | 0x0023,
    LocationName.chocolate_island_3_room_2: ROOM | CI3 | 0x00D7,
    LocationName.chocolate_island_4_room_1: ROOM | CI4 | 0x001D,
    LocationName.chocolate_island_4_room_2: ROOM | CI4 | 0x00EA,
    LocationName.chocolate_island_5_room_1: ROOM | CI5 | 0x001C,
    LocationName.chocolate_island_5_room_2: ROOM | CI5 | 0x00BD,
    LocationName.chocolate_island_5_room_3: ROOM | CI5 | 0x00C0,
    LocationName.chocolate_ghost_house_room_1: ROOM | CGH | 0x0021,
    LocationName.chocolate_ghost_house_room_2: ROOM | CGH | 0x00FC,
    LocationName.chocolate_ghost_house_room_3: ROOM | CGH | 0x00FB,
    LocationName.chocolate_secret_room_1: ROOM | CSA | 0x0117,
    LocationName.chocolate_secret_room_2: ROOM | CSA | 0x01C0,
    LocationName.chocolate_secret_room_3: ROOM | CSA | 0x01ED,
    LocationName.chocolate_secret_room_4: ROOM | CSA | 0x01EC,
    LocationName.chocolate_secret_room_5: ROOM | CSA | 0x01EE,
    LocationName.chocolate_fortress_room_1: ROOM | CIF | 0x001B,
    LocationName.chocolate_fortress_room_2: ROOM | CIF | 0x00EF,
    #LocationName.chocolate_fortress_room_3: ROOM | CIF | 0x00E2,
    LocationName.chocolate_castle_room_1: ROOM | CIC | 0x001A,
    LocationName.chocolate_castle_room_2: ROOM | CIC | 0x00D4,
    #LocationName.chocolate_castle_room_3: ROOM | CIC | 0x00D3,
    LocationName.sunken_ghost_ship_room_1: ROOM | SGS | 0x0018,
    LocationName.sunken_ghost_ship_room_2: ROOM | SGS | 0x00F8,
    LocationName.sunken_ghost_ship_room_3: ROOM | SGS | 0x00F7,

    LocationName.valley_of_bowser_1_room_1: ROOM | VB1 | 0x0116,
    LocationName.valley_of_bowser_1_room_2: ROOM | VB1 | 0x01E4,
    LocationName.valley_of_bowser_1_room_3: ROOM | VB1 | 0x01E5,
    LocationName.valley_of_bowser_2_room_1: ROOM | VB2 | 0x0115,
    LocationName.valley_of_bowser_2_room_2: ROOM | VB2 | 0x01E3,
    LocationName.valley_of_bowser_2_room_3: ROOM | VB2 | 0x01E2,
    LocationName.valley_of_bowser_3_room_1: ROOM | VB3 | 0x0113,
    LocationName.valley_of_bowser_3_room_2: ROOM | VB3 | 0x01BB,
    LocationName.valley_of_bowser_4_room_1: ROOM | VB4 | 0x010F,
    LocationName.valley_of_bowser_4_room_2: ROOM | VB4 | 0x01BF,
    LocationName.valley_ghost_house_room_1: ROOM | VBH | 0x0114,
    LocationName.valley_ghost_house_room_2: ROOM | VBH | 0x01DD,
    LocationName.valley_ghost_house_room_3: ROOM | VBH | 0x11DB,
    LocationName.valley_ghost_house_room_4: ROOM | VBH | 0x01DA,
    LocationName.valley_fortress_room_1: ROOM | VBF | 0x0111,
    #LocationName.valley_fortress_room_2: ROOM | VBF | 0x01DE,
    LocationName.valley_castle_room_1: ROOM | VBC | 0x0110,
    LocationName.valley_castle_room_2: ROOM | VBC | 0x01FE,
    #LocationName.valley_castle_room_3: ROOM | VBC | 0x01EB,

    LocationName.star_road_1_room_1: ROOM | SR1 | 0x0134,
    LocationName.star_road_1_room_2: ROOM | SR1 | 0x01D6,
    LocationName.star_road_2_room_1: ROOM | SR2 | 0x0130,
    LocationName.star_road_2_room_2: ROOM | SR2 | 0x01D5,
    LocationName.star_road_3_room_1: ROOM | SR3 | 0x0132,
    LocationName.star_road_4_room_1: ROOM | SR4 | 0x0135,
    LocationName.star_road_5_room_1: ROOM | SR5 | 0x0136,

    LocationName.special_zone_1_room_1: ROOM | SZ1 | 0x012A,
    LocationName.special_zone_1_room_2: ROOM | SZ1 | 0x11C4,
    LocationName.special_zone_2_room_1: ROOM | SZ2 | 0x012B,
    LocationName.special_zone_3_room_1: ROOM | SZ3 | 0x012C,
    LocationName.special_zone_3_room_2: ROOM | SZ3 | 0x01C9,
    LocationName.special_zone_3_room_3: ROOM | SZ3 | 0x21C8,
    LocationName.special_zone_4_room_1: ROOM | SZ4 | 0x012D,
    LocationName.special_zone_5_room_1: ROOM | SZ5 | 0x0128,
    LocationName.special_zone_6_room_1: ROOM | SZ6 | 0x0127,
    LocationName.special_zone_6_room_2: ROOM | SZ6 | 0x01E0,
    LocationName.special_zone_6_room_3: ROOM | SZ6 | 0x01E1,
    LocationName.special_zone_7_room_1: ROOM | SZ7 | 0x0126,
    LocationName.special_zone_8_room_1: ROOM | SZ8 | 0x0125,
}

midway_point_location_table = {
    LocationName.yoshis_island_1_midway: CHECKPOINT | YI1,
    LocationName.yoshis_island_2_midway: CHECKPOINT | YI2,
    LocationName.yoshis_island_3_midway: CHECKPOINT | YI3,
    LocationName.yoshis_island_castle_midway: CHECKPOINT | YIC,
    LocationName.donut_plains_1_midway: CHECKPOINT | DP1,
    LocationName.donut_plains_3_midway: CHECKPOINT | DP3,
    LocationName.donut_plains_4_midway: CHECKPOINT | DP4,
    LocationName.vanilla_dome_1_midway: CHECKPOINT | VD1,
    LocationName.vanilla_dome_2_midway: CHECKPOINT | VD2,
    LocationName.vanilla_dome_3_midway: CHECKPOINT | VD3,
    LocationName.vanilla_dome_4_midway: CHECKPOINT | VD4,
    LocationName.vanilla_secret_2_midway: CHECKPOINT | VS2,
    LocationName.vanilla_secret_3_midway: CHECKPOINT | VS3,
    LocationName.vanilla_dome_castle_midway: CHECKPOINT | VDC,
    LocationName.butter_bridge_2_midway: CHECKPOINT | BB2,
    LocationName.cheese_bridge_midway: CHECKPOINT | CBA,
    LocationName.cookie_mountain_midway: CHECKPOINT | COM,
    LocationName.forest_of_illusion_1_midway: CHECKPOINT | FI1,
    LocationName.forest_of_illusion_3_midway: CHECKPOINT | FI3,
    LocationName.forest_of_illusion_4_midway: CHECKPOINT | FI4,
    LocationName.chocolate_island_1_midway: CHECKPOINT | CI1,
    LocationName.chocolate_island_3_midway: CHECKPOINT | CI3,
    LocationName.chocolate_island_5_midway: CHECKPOINT | CI5,
    LocationName.chocolate_secret_midway: CHECKPOINT | CSA,
    LocationName.chocolate_fortress_midway: CHECKPOINT | CIF,
    LocationName.chocolate_castle_midway: CHECKPOINT | CIC,
    LocationName.valley_of_bowser_1_midway: CHECKPOINT | VB1,
    LocationName.valley_of_bowser_2_midway: CHECKPOINT | VB2,
    LocationName.valley_of_bowser_3_midway: CHECKPOINT | VB3,
    LocationName.valley_of_bowser_4_midway: CHECKPOINT | VB4,
    LocationName.valley_castle_midway: CHECKPOINT | VBC,
}

ysp_block_location_table = {
    LocationName.donut_plains_castle_yellow_block_1: BLOCK | DPC | 29,
    LocationName.donut_plains_2_yellow_block_1: BLOCK | DP2 | 42,
    LocationName.donut_plains_2_yellow_block_2: BLOCK | DP2 | 47,
    LocationName.vanilla_fortress_yellow_block_1: BLOCK | VDF | 61,
    LocationName.donut_plains_1_yellow_block_1: BLOCK | DP1 | 136,
    LocationName.donut_plains_1_yellow_block_2: BLOCK | DP1 | 137,
    LocationName.donut_plains_1_yellow_block_3: BLOCK | DP1 | 138,
    LocationName.chocolate_castle_yellow_block_1: BLOCK | CIC | 141,
    LocationName.chocolate_castle_yellow_block_2: BLOCK | CIC | 142,
    LocationName.chocolate_island_5_yellow_block_1: BLOCK | CI5 | 152,
    LocationName.chocolate_island_4_yellow_block_1: BLOCK | CI4 | 153,
    LocationName.forest_fortress_yellow_block_1: BLOCK | FIF | 156,
    LocationName.chocolate_island_2_yellow_block_1: BLOCK | CI2 | 192,
    LocationName.chocolate_island_2_yellow_block_2: BLOCK | CI2 | 193,
    LocationName.yoshis_island_4_yellow_block_1: BLOCK | YI4 | 206,
    LocationName.yoshis_island_3_yellow_block_1: BLOCK | YI3 | 210,
    LocationName.yoshis_island_3_yellow_block_2: BLOCK | YI3 | 211,
    LocationName.yoshis_island_3_yellow_block_3: BLOCK | YI3 | 212,
    LocationName.yoshis_island_3_yellow_block_4: BLOCK | YI3 | 213,
    LocationName.yoshis_island_3_yellow_block_5: BLOCK | YI3 | 214,
    LocationName.yoshis_island_3_yellow_block_6: BLOCK | YI3 | 215,
    LocationName.yoshis_island_3_yellow_block_7: BLOCK | YI3 | 216,
    LocationName.yoshis_island_3_yellow_block_8: BLOCK | YI3 | 217,
    LocationName.yoshis_island_3_yellow_block_9: BLOCK | YI3 | 218,
    LocationName.yoshis_island_3_yellow_block_10: BLOCK | YI3 | 219,
    LocationName.yoshis_island_3_yellow_block_11: BLOCK | YI3 | 220,
    LocationName.yoshis_island_3_yellow_block_12: BLOCK | YI3 | 221,
    LocationName.yoshis_island_3_yellow_block_13: BLOCK | YI3 | 222,
    LocationName.yoshis_island_3_yellow_block_14: BLOCK | YI3 | 223,
    LocationName.yoshis_island_3_yellow_block_15: BLOCK | YI3 | 224,
    LocationName.yoshis_island_3_yellow_block_16: BLOCK | YI3 | 225,
    LocationName.yoshis_island_3_yellow_block_17: BLOCK | YI3 | 226,
    LocationName.yoshis_island_3_yellow_block_18: BLOCK | YI3 | 227,
    LocationName.yoshis_island_3_yellow_block_19: BLOCK | YI3 | 228,
    LocationName.yoshis_island_3_yellow_block_20: BLOCK | YI3 | 229,
    LocationName.yoshis_island_3_yellow_block_21: BLOCK | YI3 | 230,
    LocationName.yoshis_island_3_yellow_block_22: BLOCK | YI3 | 231,
    LocationName.yoshis_island_3_yellow_block_23: BLOCK | YI3 | 232,
    LocationName.yoshis_island_3_yellow_block_24: BLOCK | YI3 | 233,
    LocationName.yoshis_island_3_yellow_block_25: BLOCK | YI3 | 234,
    LocationName.yoshis_island_3_yellow_block_26: BLOCK | YI3 | 235,
    LocationName.yoshis_island_3_yellow_block_27: BLOCK | YI3 | 236,
    LocationName.yoshis_island_3_yellow_block_28: BLOCK | YI3 | 237,
    LocationName.yoshis_island_3_yellow_block_29: BLOCK | YI3 | 238,
    LocationName.yoshis_island_3_yellow_block_30: BLOCK | YI3 | 241,
    LocationName.yoshis_island_3_yellow_block_31: BLOCK | YI3 | 242,
    LocationName.yoshis_island_3_yellow_block_32: BLOCK | YI3 | 243,
    LocationName.yoshis_island_3_yellow_block_33: BLOCK | YI3 | 244,
    LocationName.yoshis_island_3_yellow_block_34: BLOCK | YI3 | 245,
    LocationName.yoshis_island_3_yellow_block_35: BLOCK | YI3 | 246,
    LocationName.yoshis_island_3_yellow_block_36: BLOCK | YI3 | 247,
    LocationName.yoshis_island_3_yellow_block_37: BLOCK | YI3 | 248,
    LocationName.yoshis_island_3_yellow_block_38: BLOCK | YI3 | 249,
    LocationName.yoshis_island_3_yellow_block_39: BLOCK | YI3 | 250,
    LocationName.yoshis_island_3_yellow_block_40: BLOCK | YI3 | 251,
    LocationName.yoshis_island_3_yellow_block_41: BLOCK | YI3 | 252,
    LocationName.yoshis_island_3_yellow_block_42: BLOCK | YI3 | 253,
    LocationName.yoshis_island_3_yellow_block_43: BLOCK | YI3 | 254,
    LocationName.yoshis_island_3_yellow_block_44: BLOCK | YI3 | 255,
    LocationName.yoshis_island_3_yellow_block_45: BLOCK | YI3 | 256,
    LocationName.yoshis_island_3_yellow_block_46: BLOCK | YI3 | 257,
    LocationName.yoshis_island_3_yellow_block_47: BLOCK | YI3 | 258,
    LocationName.yoshis_island_3_yellow_block_48: BLOCK | YI3 | 259,
    LocationName.yoshis_island_3_yellow_block_49: BLOCK | YI3 | 260,
    LocationName.yoshis_island_3_yellow_block_50: BLOCK | YI3 | 261,
    LocationName.yoshis_island_3_yellow_block_51: BLOCK | YI3 | 262,
    LocationName.yoshis_island_3_yellow_block_52: BLOCK | YI3 | 265,
    LocationName.yoshis_island_3_yellow_block_53: BLOCK | YI3 | 266,
    LocationName.yoshis_island_3_yellow_block_54: BLOCK | YI3 | 267,
    LocationName.yoshis_island_3_yellow_block_55: BLOCK | YI3 | 268,
    LocationName.yoshis_island_3_yellow_block_56: BLOCK | YI3 | 269,
    LocationName.yoshis_island_3_yellow_block_57: BLOCK | YI3 | 270,
    LocationName.yoshis_island_3_yellow_block_58: BLOCK | YI3 | 271,
    LocationName.yoshis_island_3_yellow_block_59: BLOCK | YI3 | 272,
    LocationName.yoshis_island_3_yellow_block_60: BLOCK | YI3 | 273,
    LocationName.yoshis_island_3_yellow_block_61: BLOCK | YI3 | 274,
    LocationName.yoshis_island_3_yellow_block_62: BLOCK | YI3 | 275,
    LocationName.yoshis_island_3_yellow_block_63: BLOCK | YI3 | 276,
    LocationName.yoshis_island_3_yellow_block_64: BLOCK | YI3 | 277,
    LocationName.yoshis_island_3_yellow_block_65: BLOCK | YI3 | 278,
    LocationName.yoshis_island_3_yellow_block_66: BLOCK | YI3 | 279,
    LocationName.yoshis_island_3_yellow_block_67: BLOCK | YI3 | 280,
    LocationName.yoshis_island_3_yellow_block_68: BLOCK | YI3 | 281,
    LocationName.yoshis_island_3_yellow_block_69: BLOCK | YI3 | 282,
    LocationName.yoshis_island_3_yellow_block_70: BLOCK | YI3 | 283,
    LocationName.yoshis_island_3_yellow_block_71: BLOCK | YI3 | 284,
    LocationName.yoshis_island_3_yellow_block_72: BLOCK | YI3 | 285,
    LocationName.yoshis_island_3_yellow_block_73: BLOCK | YI3 | 286,
    LocationName.yoshis_island_3_yellow_block_74: BLOCK | YI3 | 287,
    LocationName.yoshis_island_3_yellow_block_75: BLOCK | YI3 | 288,
    LocationName.yoshis_island_3_yellow_block_76: BLOCK | YI3 | 289,
    LocationName.yoshis_island_3_yellow_block_77: BLOCK | YI3 | 290,
    LocationName.yoshis_island_3_yellow_block_78: BLOCK | YI3 | 291,
    LocationName.yoshis_island_3_yellow_block_79: BLOCK | YI3 | 292,
    LocationName.yoshis_island_3_yellow_block_80: BLOCK | YI3 | 293,
    LocationName.yoshis_island_3_yellow_block_81: BLOCK | YI3 | 294,
    LocationName.yoshis_island_3_yellow_block_82: BLOCK | YI3 | 295,
    LocationName.yoshis_island_3_yellow_block_83: BLOCK | YI3 | 296,
    LocationName.yoshis_island_3_yellow_block_84: BLOCK | YI3 | 297,
    LocationName.yoshis_island_3_yellow_block_85: BLOCK | YI3 | 298,
    LocationName.yoshis_island_3_yellow_block_86: BLOCK | YI3 | 299,
    LocationName.yoshis_island_1_yellow_block_1: BLOCK | YI1 | 301,
    LocationName.yoshis_island_2_yellow_block_1: BLOCK | YI2 | 311,
    LocationName.yoshis_island_2_yellow_block_2: BLOCK | YI2 | 319,
    LocationName.valley_of_bowser_4_yellow_block_1: BLOCK | VB4 | 355,
    LocationName.valley_castle_yellow_block_1: BLOCK | VBC | 361,
    LocationName.valley_castle_yellow_block_2: BLOCK | VBC | 362,
    LocationName.valley_fortress_yellow_block_1: BLOCK | VBF | 365,
    LocationName.valley_of_bowser_2_yellow_block_1: BLOCK | VB2 | 373,
    LocationName.valley_of_bowser_1_yellow_block_1: BLOCK | VB1 | 380,
    LocationName.valley_of_bowser_1_yellow_block_2: BLOCK | VB1 | 381,
    LocationName.valley_of_bowser_1_yellow_block_3: BLOCK | VB1 | 382,
    LocationName.valley_of_bowser_1_yellow_block_4: BLOCK | VB1 | 383,
    LocationName.forest_of_illusion_2_yellow_block_1: BLOCK | FI2 | 456,
    LocationName.star_road_5_yellow_block_1: BLOCK | SR5 | 612,
    LocationName.star_road_5_yellow_block_2: BLOCK | SR5 | 613,
    LocationName.star_road_5_yellow_block_3: BLOCK | SR5 | 614,
    LocationName.star_road_5_yellow_block_4: BLOCK | SR5 | 615,
    LocationName.star_road_5_yellow_block_5: BLOCK | SR5 | 616,
    LocationName.star_road_5_yellow_block_6: BLOCK | SR5 | 617,
    LocationName.star_road_5_yellow_block_7: BLOCK | SR5 | 618,
    LocationName.star_road_5_yellow_block_8: BLOCK | SR5 | 619,
    LocationName.star_road_5_yellow_block_9: BLOCK | SR5 | 620,
    LocationName.star_road_5_yellow_block_10: BLOCK | SR5 | 621,
    LocationName.star_road_5_yellow_block_11: BLOCK | SR5 | 622,
    LocationName.star_road_5_yellow_block_12: BLOCK | SR5 | 623,
    LocationName.star_road_5_yellow_block_13: BLOCK | SR5 | 624,
    LocationName.star_road_5_yellow_block_14: BLOCK | SR5 | 625,
    LocationName.star_road_5_yellow_block_15: BLOCK | SR5 | 626,
    LocationName.star_road_5_yellow_block_16: BLOCK | SR5 | 627,
    LocationName.star_road_5_yellow_block_17: BLOCK | SR5 | 628,
    LocationName.star_road_5_yellow_block_18: BLOCK | SR5 | 629,
    LocationName.star_road_5_yellow_block_19: BLOCK | SR5 | 630,
    LocationName.star_road_5_yellow_block_20: BLOCK | SR5 | 631,
}


gsp_block_location_table = {
    LocationName.vanilla_secret_2_green_block_1: BLOCK | VS2 | 1,
    LocationName.donut_plains_3_green_block_1: BLOCK | DP3 | 20,
    LocationName.donut_plains_castle_green_block_1: BLOCK | DPC | 38,
    LocationName.donut_plains_2_green_block_1: BLOCK | DP2 | 46,
    LocationName.butter_bridge_2_green_block_1: BLOCK | BB2 | 68,
    LocationName.donut_plains_1_green_block_1: BLOCK | DP1 | 120,
    LocationName.donut_plains_1_green_block_2: BLOCK | DP1 | 121,
    LocationName.donut_plains_1_green_block_3: BLOCK | DP1 | 122,
    LocationName.donut_plains_1_green_block_4: BLOCK | DP1 | 123,
    LocationName.donut_plains_1_green_block_5: BLOCK | DP1 | 124,
    LocationName.donut_plains_1_green_block_6: BLOCK | DP1 | 125,
    LocationName.donut_plains_1_green_block_7: BLOCK | DP1 | 126,
    LocationName.donut_plains_1_green_block_8: BLOCK | DP1 | 127,
    LocationName.donut_plains_1_green_block_9: BLOCK | DP1 | 128,
    LocationName.donut_plains_1_green_block_10: BLOCK | DP1 | 129,
    LocationName.donut_plains_1_green_block_11: BLOCK | DP1 | 130,
    LocationName.donut_plains_1_green_block_12: BLOCK | DP1 | 131,
    LocationName.donut_plains_1_green_block_13: BLOCK | DP1 | 132,
    LocationName.donut_plains_1_green_block_14: BLOCK | DP1 | 133,
    LocationName.donut_plains_1_green_block_15: BLOCK | DP1 | 134,
    LocationName.donut_plains_1_green_block_16: BLOCK | DP1 | 135,
    LocationName.chocolate_castle_green_block_1: BLOCK | CIC | 143,
    LocationName.chocolate_fortress_green_block_1: BLOCK | CIF | 148,
    LocationName.forest_castle_green_block_1: BLOCK | FIC | 167,
    LocationName.chocolate_island_1_green_block_1: BLOCK | CI1 | 174,
    LocationName.chocolate_island_3_green_block_1: BLOCK | CI3 | 179,
    LocationName.chocolate_island_2_green_block_1: BLOCK | CI2 | 194,
    LocationName.chocolate_island_2_green_block_2: BLOCK | CI2 | 195,
    LocationName.chocolate_island_2_green_block_3: BLOCK | CI2 | 196,
    LocationName.chocolate_island_2_green_block_4: BLOCK | CI2 | 197,
    LocationName.chocolate_island_2_green_block_5: BLOCK | CI2 | 198,
    LocationName.chocolate_island_2_green_block_6: BLOCK | CI2 | 199,
    LocationName.valley_castle_green_block_1: BLOCK | VBC | 363,
    LocationName.valley_fortress_green_block_1: BLOCK | VBF | 364,
    LocationName.valley_of_bowser_1_green_block_1: BLOCK | VB1 | 376,
    LocationName.vanilla_dome_castle_green_block_1: BLOCK | VDC | 426,
    LocationName.forest_of_illusion_2_green_block_1: BLOCK | FI2 | 450,
    LocationName.star_road_4_green_block_1: BLOCK | SR4 | 601,
    LocationName.star_road_4_green_block_2: BLOCK | SR4 | 602,
    LocationName.star_road_4_green_block_3: BLOCK | SR4 | 603,
    LocationName.star_road_4_green_block_4: BLOCK | SR4 | 604,
    LocationName.star_road_4_green_block_5: BLOCK | SR4 | 605,
    LocationName.star_road_4_green_block_6: BLOCK | SR4 | 606,
    LocationName.star_road_4_green_block_7: BLOCK | SR4 | 607,
    LocationName.star_road_5_green_block_1: BLOCK | SR5 | 632,
    LocationName.star_road_5_green_block_2: BLOCK | SR5 | 633,
    LocationName.star_road_5_green_block_3: BLOCK | SR5 | 634,
    LocationName.star_road_5_green_block_4: BLOCK | SR5 | 635,
    LocationName.star_road_5_green_block_5: BLOCK | SR5 | 636,
    LocationName.star_road_5_green_block_6: BLOCK | SR5 | 637,
    LocationName.star_road_5_green_block_7: BLOCK | SR5 | 638,
    LocationName.star_road_5_green_block_8: BLOCK | SR5 | 639,
    LocationName.star_road_5_green_block_9: BLOCK | SR5 | 640,
    LocationName.star_road_5_green_block_10: BLOCK | SR5 | 641,
    LocationName.star_road_5_green_block_11: BLOCK | SR5 | 642,
    LocationName.star_road_5_green_block_12: BLOCK | SR5 | 643,
    LocationName.star_road_5_green_block_13: BLOCK | SR5 | 644,
    LocationName.star_road_5_green_block_14: BLOCK | SR5 | 645,
    LocationName.star_road_5_green_block_15: BLOCK | SR5 | 646,
    LocationName.star_road_5_green_block_16: BLOCK | SR5 | 647,
    LocationName.star_road_5_green_block_17: BLOCK | SR5 | 648,
    LocationName.star_road_5_green_block_18: BLOCK | SR5 | 649,
    LocationName.star_road_5_green_block_19: BLOCK | SR5 | 650,
    LocationName.star_road_5_green_block_20: BLOCK | SR5 | 651,
}


pswitch_block_location_table = {
    LocationName.vanilla_dome_3_pswitch_coin_block_1: BLOCK | VD3 | 344,
    LocationName.vanilla_dome_3_pswitch_coin_block_2: BLOCK | VD3 | 345,
    LocationName.vanilla_dome_3_pswitch_coin_block_3: BLOCK | VD3 | 346,
    LocationName.vanilla_dome_3_pswitch_coin_block_4: BLOCK | VD3 | 347,
    LocationName.vanilla_dome_3_pswitch_coin_block_5: BLOCK | VD3 | 348,
    LocationName.vanilla_dome_3_pswitch_coin_block_6: BLOCK | VD3 | 349,
    LocationName.valley_ghost_house_pswitch_coin_block_1: BLOCK | VBH | 368,
    LocationName.special_zone_1_pswitch_coin_block_1: BLOCK | SZ1 | 570,
    LocationName.special_zone_1_pswitch_coin_block_2: BLOCK | SZ1 | 571,
    LocationName.special_zone_1_pswitch_coin_block_3: BLOCK | SZ1 | 572,
    LocationName.special_zone_1_pswitch_coin_block_4: BLOCK | SZ1 | 573,
    LocationName.special_zone_1_pswitch_coin_block_5: BLOCK | SZ1 | 574,
    LocationName.special_zone_1_pswitch_coin_block_6: BLOCK | SZ1 | 575,
    LocationName.special_zone_1_pswitch_coin_block_7: BLOCK | SZ1 | 576,
    LocationName.special_zone_1_pswitch_coin_block_8: BLOCK | SZ1 | 577,
    LocationName.special_zone_1_pswitch_coin_block_9: BLOCK | SZ1 | 578,
    LocationName.special_zone_1_pswitch_coin_block_10: BLOCK | SZ1 | 579,
    LocationName.special_zone_1_pswitch_coin_block_11: BLOCK | SZ1 | 580,
    LocationName.special_zone_1_pswitch_coin_block_12: BLOCK | SZ1 | 581,
    LocationName.special_zone_1_pswitch_coin_block_13: BLOCK | SZ1 | 582,
}


flying_block_location_table = {
    LocationName.donut_plains_2_flying_block_1: BLOCK | DP2 | 45,
    LocationName.chocolate_island_1_flying_block_1: BLOCK | CI1 | 171,
    LocationName.chocolate_island_1_flying_block_2: BLOCK | CI1 | 172,
    LocationName.yoshis_island_castle_flying_block_1: BLOCK | YIC | 205,
    LocationName.yoshis_island_1_flying_block_1: BLOCK | YI1 | 300,
    LocationName.yoshis_island_2_flying_block_1: BLOCK | YI2 | 304,
    LocationName.yoshis_island_2_flying_block_2: BLOCK | YI2 | 305,
    LocationName.yoshis_island_2_flying_block_3: BLOCK | YI2 | 306,
    LocationName.yoshis_island_2_flying_block_4: BLOCK | YI2 | 307,
    LocationName.yoshis_island_2_flying_block_5: BLOCK | YI2 | 308,
    LocationName.yoshis_island_2_flying_block_6: BLOCK | YI2 | 309,
    LocationName.vanilla_dome_3_flying_block_1: BLOCK | VD3 | 334,
    LocationName.vanilla_dome_3_flying_block_2: BLOCK | VD3 | 335,
    LocationName.vanilla_dome_3_flying_block_3: BLOCK | VD3 | 337,
    LocationName.vanilla_dome_1_flying_block_1: BLOCK | VD1 | 412,
    LocationName.forest_ghost_house_flying_block_1: BLOCK | FGH | 429,
    LocationName.special_zone_8_flying_block_1: BLOCK | SZ8 | 516,
}


invisible_block_location_table = {
    LocationName.donut_plains_castle_invis_life_block_1: BLOCK | DPC | 34,
    LocationName.chocolate_island_2_invis_coin_block_1: BLOCK | CI2 | 185,
    LocationName.vanilla_dome_3_invis_coin_block_1: BLOCK | VD3 | 338,
    LocationName.valley_of_bowser_1_invis_coin_block_1: BLOCK | VB1 | 377,
    LocationName.valley_of_bowser_1_invis_coin_block_2: BLOCK | VB1 | 378,
    LocationName.valley_of_bowser_1_invis_coin_block_3: BLOCK | VB1 | 379,
    LocationName.vanilla_dome_2_invis_life_block_1: BLOCK | VD2 | 392,
    LocationName.forest_of_illusion_2_invis_coin_block_1: BLOCK | FI2 | 452,
    LocationName.forest_of_illusion_2_invis_coin_block_2: BLOCK | FI2 | 453,
    LocationName.forest_of_illusion_2_invis_life_block_1: BLOCK | FI2 | 454,
    LocationName.forest_of_illusion_2_invis_coin_block_3: BLOCK | FI2 | 455,
}


coin_block_location_table = {
    LocationName.vanilla_secret_2_multi_coin_block_1: BLOCK | VS2 | 4,
    LocationName.vanilla_secret_2_coin_block_1: BLOCK | VS2 | 6,
    LocationName.vanilla_secret_2_coin_block_2: BLOCK | VS2 | 7,
    LocationName.vanilla_secret_2_coin_block_3: BLOCK | VS2 | 8,
    LocationName.vanilla_secret_2_coin_block_4: BLOCK | VS2 | 9,
    LocationName.vanilla_secret_2_coin_block_5: BLOCK | VS2 | 10,
    LocationName.vanilla_secret_2_coin_block_6: BLOCK | VS2 | 11,
    LocationName.donut_plains_3_coin_block_1: BLOCK | DP3 | 21,
    LocationName.donut_plains_3_coin_block_2: BLOCK | DP3 | 22,
    LocationName.donut_plains_4_coin_block_1: BLOCK | DP4 | 25,
    LocationName.donut_plains_4_coin_block_2: BLOCK | DP4 | 27,
    LocationName.donut_plains_castle_coin_block_1: BLOCK | DPC | 30,
    LocationName.donut_plains_castle_coin_block_2: BLOCK | DPC | 32,
    LocationName.donut_plains_castle_coin_block_3: BLOCK | DPC | 35,
    LocationName.donut_plains_castle_coin_block_4: BLOCK | DPC | 36,
    LocationName.donut_plains_castle_coin_block_5: BLOCK | DPC | 37,
    LocationName.donut_plains_2_coin_block_1: BLOCK | DP2 | 39,
    LocationName.donut_plains_2_coin_block_2: BLOCK | DP2 | 40,
    LocationName.donut_plains_2_coin_block_3: BLOCK | DP2 | 41,
    LocationName.donut_plains_2_multi_coin_block_1: BLOCK | DP2 | 44,
    LocationName.donut_secret_1_coin_block_1: BLOCK | DS1 | 49,
    LocationName.donut_secret_1_coin_block_2: BLOCK | DS1 | 50,
    LocationName.donut_secret_1_coin_block_3: BLOCK | DS1 | 52,
    LocationName.butter_bridge_1_multi_coin_block_1: BLOCK | BB1 | 63,
    LocationName.butter_bridge_1_multi_coin_block_2: BLOCK | BB1 | 64,
    LocationName.butter_bridge_1_multi_coin_block_3: BLOCK | BB1 | 65,
    LocationName.cookie_mountain_coin_block_1: BLOCK | COM | 75,
    LocationName.cookie_mountain_coin_block_2: BLOCK | COM | 76,
    LocationName.cookie_mountain_coin_block_3: BLOCK | COM | 77,
    LocationName.cookie_mountain_coin_block_4: BLOCK | COM | 78,
    LocationName.cookie_mountain_coin_block_5: BLOCK | COM | 79,
    LocationName.cookie_mountain_coin_block_6: BLOCK | COM | 80,
    LocationName.cookie_mountain_coin_block_7: BLOCK | COM | 81,
    LocationName.cookie_mountain_coin_block_8: BLOCK | COM | 82,
    LocationName.cookie_mountain_coin_block_9: BLOCK | COM | 83,
    LocationName.cookie_mountain_coin_block_10: BLOCK | COM | 88,
    LocationName.cookie_mountain_coin_block_11: BLOCK | COM | 89,
    LocationName.cookie_mountain_coin_block_12: BLOCK | COM | 91,
    LocationName.cookie_mountain_coin_block_13: BLOCK | COM | 92,
    LocationName.cookie_mountain_coin_block_14: BLOCK | COM | 93,
    LocationName.cookie_mountain_coin_block_15: BLOCK | COM | 94,
    LocationName.cookie_mountain_coin_block_16: BLOCK | COM | 95,
    LocationName.cookie_mountain_coin_block_17: BLOCK | COM | 96,
    LocationName.cookie_mountain_coin_block_18: BLOCK | COM | 97,
    LocationName.cookie_mountain_coin_block_19: BLOCK | COM | 98,
    LocationName.cookie_mountain_coin_block_20: BLOCK | COM | 99,
    LocationName.cookie_mountain_coin_block_21: BLOCK | COM | 100,
    LocationName.cookie_mountain_coin_block_22: BLOCK | COM | 101,
    LocationName.cookie_mountain_coin_block_23: BLOCK | COM | 102,
    LocationName.cookie_mountain_coin_block_24: BLOCK | COM | 103,
    LocationName.cookie_mountain_coin_block_25: BLOCK | COM | 104,
    LocationName.cookie_mountain_coin_block_26: BLOCK | COM | 105,
    LocationName.cookie_mountain_coin_block_27: BLOCK | COM | 106,
    LocationName.cookie_mountain_coin_block_28: BLOCK | COM | 107,
    LocationName.cookie_mountain_coin_block_29: BLOCK | COM | 108,
    LocationName.cookie_mountain_coin_block_30: BLOCK | COM | 109,
    LocationName.donut_secret_house_multi_coin_block_1: BLOCK | DSH | 112,
    LocationName.donut_plains_1_coin_block_1: BLOCK | DP1 | 116,
    LocationName.donut_plains_1_coin_block_2: BLOCK | DP1 | 117,
    LocationName.chocolate_fortress_coin_block_1: BLOCK | CIF | 146,
    LocationName.chocolate_fortress_coin_block_2: BLOCK | CIF | 147,
    LocationName.chocolate_island_2_multi_coin_block_1: BLOCK | CI2 | 184,
    LocationName.chocolate_island_2_coin_block_1: BLOCK | CI2 | 187,
    LocationName.chocolate_island_2_coin_block_2: BLOCK | CI2 | 188,
    LocationName.chocolate_island_2_multi_coin_block_2: BLOCK | CI2 | 189,
    LocationName.yoshis_island_castle_coin_block_1: BLOCK | YIC | 200,
    LocationName.yoshis_island_castle_coin_block_2: BLOCK | YIC | 201,
    LocationName.yoshis_island_castle_coin_block_3: BLOCK | YIC | 203,
    LocationName.yoshis_island_castle_coin_block_4: BLOCK | YIC | 204,
    LocationName.yoshis_island_4_multi_coin_block_1: BLOCK | YI4 | 208,
    LocationName.yoshis_island_3_coin_block_1: BLOCK | YI3 | 239,
    LocationName.yoshis_island_3_coin_block_2: BLOCK | YI3 | 263,
    LocationName.yoshis_island_2_coin_block_1: BLOCK | YI2 | 310,
    LocationName.yoshis_island_2_coin_block_2: BLOCK | YI2 | 312,
    LocationName.yoshis_island_2_coin_block_3: BLOCK | YI2 | 313,
    LocationName.yoshis_island_2_coin_block_4: BLOCK | YI2 | 315,
    LocationName.yoshis_island_2_coin_block_5: BLOCK | YI2 | 317,
    LocationName.vanilla_ghost_house_multi_coin_block_1: BLOCK | VDH | 323,
    LocationName.vanilla_secret_1_coin_block_1: BLOCK | VS1 | 325,
    LocationName.vanilla_secret_1_multi_coin_block_1: BLOCK | VS1 | 327,
    LocationName.vanilla_secret_1_coin_block_2: BLOCK | VS1 | 330,
    LocationName.vanilla_secret_1_coin_block_3: BLOCK | VS1 | 331,
    LocationName.vanilla_dome_3_coin_block_1: BLOCK | VD3 | 333,
    LocationName.vanilla_dome_3_multi_coin_block_1: BLOCK | VD3 | 340,
    LocationName.valley_ghost_house_multi_coin_block_1: BLOCK | VBH | 369,
    LocationName.vanilla_dome_2_coin_block_1: BLOCK | VD2 | 387,
    LocationName.vanilla_dome_2_coin_block_2: BLOCK | VD2 | 389,
    LocationName.vanilla_dome_2_coin_block_3: BLOCK | VD2 | 390,
    LocationName.vanilla_dome_2_coin_block_4: BLOCK | VD2 | 393,
    LocationName.vanilla_dome_2_coin_block_5: BLOCK | VD2 | 394,
    LocationName.vanilla_dome_2_multi_coin_block_1: BLOCK | VD2 | 399,
    LocationName.vanilla_dome_2_multi_coin_block_2: BLOCK | VD2 | 400,
    LocationName.vanilla_dome_4_coin_block_1: BLOCK | VD4 | 403,
    LocationName.vanilla_dome_4_coin_block_2: BLOCK | VD4 | 404,
    LocationName.vanilla_dome_4_coin_block_3: BLOCK | VD4 | 405,
    LocationName.vanilla_dome_4_coin_block_4: BLOCK | VD4 | 407,
    LocationName.vanilla_dome_4_coin_block_5: BLOCK | VD4 | 408,
    LocationName.vanilla_dome_4_coin_block_6: BLOCK | VD4 | 409,
    LocationName.vanilla_dome_4_coin_block_7: BLOCK | VD4 | 410,
    LocationName.vanilla_dome_4_coin_block_8: BLOCK | VD4 | 411,
    LocationName.vanilla_dome_1_coin_block_1: BLOCK | VD1 | 415,
    LocationName.vanilla_dome_1_coin_block_2: BLOCK | VD1 | 421,
    LocationName.forest_ghost_house_coin_block_1: BLOCK | FGH | 427,
    LocationName.forest_of_illusion_4_multi_coin_block_1: BLOCK | FI4 | 437,
    LocationName.forest_of_illusion_4_coin_block_1: BLOCK | FI4 | 438,
    LocationName.forest_of_illusion_4_coin_block_2: BLOCK | FI4 | 439,
    LocationName.forest_of_illusion_4_coin_block_3: BLOCK | FI4 | 440,
    LocationName.forest_of_illusion_4_coin_block_4: BLOCK | FI4 | 441,
    LocationName.forest_of_illusion_4_coin_block_5: BLOCK | FI4 | 443,
    LocationName.forest_of_illusion_4_coin_block_6: BLOCK | FI4 | 444,
    LocationName.forest_of_illusion_4_coin_block_7: BLOCK | FI4 | 445,
    LocationName.forest_of_illusion_4_coin_block_8: BLOCK | FI4 | 447,
    LocationName.forest_of_illusion_4_coin_block_9: BLOCK | FI4 | 448,
    LocationName.forest_of_illusion_4_coin_block_10: BLOCK | FI4 | 449,
    LocationName.forest_of_illusion_3_coin_block_1: BLOCK | FI3 | 461,
    LocationName.forest_of_illusion_3_multi_coin_block_1: BLOCK | FI3 | 462,
    LocationName.forest_of_illusion_3_coin_block_2: BLOCK | FI3 | 463,
    LocationName.forest_of_illusion_3_multi_coin_block_2: BLOCK | FI3 | 464,
    LocationName.forest_of_illusion_3_coin_block_3: BLOCK | FI3 | 465,
    LocationName.forest_of_illusion_3_coin_block_4: BLOCK | FI3 | 466,
    LocationName.forest_of_illusion_3_coin_block_5: BLOCK | FI3 | 467,
    LocationName.forest_of_illusion_3_coin_block_6: BLOCK | FI3 | 468,
    LocationName.forest_of_illusion_3_coin_block_7: BLOCK | FI3 | 469,
    LocationName.forest_of_illusion_3_coin_block_8: BLOCK | FI3 | 470,
    LocationName.forest_of_illusion_3_coin_block_9: BLOCK | FI3 | 471,
    LocationName.forest_of_illusion_3_coin_block_10: BLOCK | FI3 | 472,
    LocationName.forest_of_illusion_3_coin_block_11: BLOCK | FI3 | 473,
    LocationName.forest_of_illusion_3_coin_block_12: BLOCK | FI3 | 474,
    LocationName.forest_of_illusion_3_coin_block_13: BLOCK | FI3 | 475,
    LocationName.forest_of_illusion_3_coin_block_14: BLOCK | FI3 | 476,
    LocationName.forest_of_illusion_3_coin_block_15: BLOCK | FI3 | 477,
    LocationName.forest_of_illusion_3_coin_block_16: BLOCK | FI3 | 478,
    LocationName.forest_of_illusion_3_coin_block_17: BLOCK | FI3 | 479,
    LocationName.forest_of_illusion_3_coin_block_18: BLOCK | FI3 | 480,
    LocationName.forest_of_illusion_3_coin_block_19: BLOCK | FI3 | 481,
    LocationName.forest_of_illusion_3_coin_block_20: BLOCK | FI3 | 482,
    LocationName.forest_of_illusion_3_coin_block_21: BLOCK | FI3 | 483,
    LocationName.forest_of_illusion_3_coin_block_22: BLOCK | FI3 | 484,
    LocationName.forest_of_illusion_3_coin_block_23: BLOCK | FI3 | 485,
    LocationName.forest_of_illusion_3_coin_block_24: BLOCK | FI3 | 486,
    LocationName.special_zone_8_coin_block_1: BLOCK | SZ8 | 488,
    LocationName.special_zone_8_coin_block_2: BLOCK | SZ8 | 489,
    LocationName.special_zone_8_coin_block_3: BLOCK | SZ8 | 490,
    LocationName.special_zone_8_coin_block_4: BLOCK | SZ8 | 491,
    LocationName.special_zone_8_coin_block_5: BLOCK | SZ8 | 492,
    LocationName.special_zone_8_coin_block_6: BLOCK | SZ8 | 496,
    LocationName.special_zone_8_coin_block_7: BLOCK | SZ8 | 497,
    LocationName.special_zone_8_coin_block_8: BLOCK | SZ8 | 498,
    LocationName.special_zone_8_coin_block_9: BLOCK | SZ8 | 499,
    LocationName.special_zone_8_coin_block_10: BLOCK | SZ8 | 500,
    LocationName.special_zone_8_coin_block_11: BLOCK | SZ8 | 501,
    LocationName.special_zone_8_coin_block_12: BLOCK | SZ8 | 502,
    LocationName.special_zone_8_coin_block_13: BLOCK | SZ8 | 503,
    LocationName.special_zone_8_coin_block_14: BLOCK | SZ8 | 504,
    LocationName.special_zone_8_coin_block_15: BLOCK | SZ8 | 505,
    LocationName.special_zone_8_coin_block_16: BLOCK | SZ8 | 506,
    LocationName.special_zone_8_coin_block_17: BLOCK | SZ8 | 507,
    LocationName.special_zone_8_coin_block_18: BLOCK | SZ8 | 508,
    LocationName.special_zone_8_multi_coin_block_1: BLOCK | SZ8 | 509,
    LocationName.special_zone_8_coin_block_19: BLOCK | SZ8 | 510,
    LocationName.special_zone_8_coin_block_20: BLOCK | SZ8 | 511,
    LocationName.special_zone_8_coin_block_21: BLOCK | SZ8 | 512,
    LocationName.special_zone_8_coin_block_22: BLOCK | SZ8 | 513,
    LocationName.special_zone_8_coin_block_23: BLOCK | SZ8 | 514,
    LocationName.special_zone_7_coin_block_1: BLOCK | SZ7 | 519,
    LocationName.special_zone_7_coin_block_2: BLOCK | SZ7 | 521,
    LocationName.special_zone_6_coin_block_1: BLOCK | SZ6 | 523,
    LocationName.special_zone_6_coin_block_2: BLOCK | SZ6 | 524,
    LocationName.special_zone_6_multi_coin_block_1: BLOCK | SZ6 | 527,
    LocationName.special_zone_6_coin_block_3: BLOCK | SZ6 | 528,
    LocationName.special_zone_6_coin_block_4: BLOCK | SZ6 | 529,
    LocationName.special_zone_6_coin_block_5: BLOCK | SZ6 | 530,
    LocationName.special_zone_6_coin_block_6: BLOCK | SZ6 | 531,
    LocationName.special_zone_6_coin_block_7: BLOCK | SZ6 | 532,
    LocationName.special_zone_6_coin_block_8: BLOCK | SZ6 | 533,
    LocationName.special_zone_6_coin_block_9: BLOCK | SZ6 | 534,
    LocationName.special_zone_6_coin_block_10: BLOCK | SZ6 | 535,
    LocationName.special_zone_6_coin_block_11: BLOCK | SZ6 | 536,
    LocationName.special_zone_6_coin_block_12: BLOCK | SZ6 | 537,
    LocationName.special_zone_6_coin_block_13: BLOCK | SZ6 | 538,
    LocationName.special_zone_6_coin_block_14: BLOCK | SZ6 | 539,
    LocationName.special_zone_6_coin_block_15: BLOCK | SZ6 | 540,
    LocationName.special_zone_6_coin_block_16: BLOCK | SZ6 | 541,
    LocationName.special_zone_6_coin_block_17: BLOCK | SZ6 | 542,
    LocationName.special_zone_6_coin_block_18: BLOCK | SZ6 | 543,
    LocationName.special_zone_6_coin_block_19: BLOCK | SZ6 | 544,
    LocationName.special_zone_6_coin_block_20: BLOCK | SZ6 | 545,
    LocationName.special_zone_6_coin_block_21: BLOCK | SZ6 | 546,
    LocationName.special_zone_6_coin_block_22: BLOCK | SZ6 | 547,
    LocationName.special_zone_6_coin_block_23: BLOCK | SZ6 | 548,
    LocationName.special_zone_6_coin_block_24: BLOCK | SZ6 | 549,
    LocationName.special_zone_6_coin_block_25: BLOCK | SZ6 | 550,
    LocationName.special_zone_6_coin_block_26: BLOCK | SZ6 | 551,
    LocationName.special_zone_6_coin_block_27: BLOCK | SZ6 | 552,
    LocationName.special_zone_6_coin_block_28: BLOCK | SZ6 | 553,
    LocationName.special_zone_6_coin_block_29: BLOCK | SZ6 | 555,
    LocationName.special_zone_6_coin_block_30: BLOCK | SZ6 | 556,
    LocationName.special_zone_6_coin_block_31: BLOCK | SZ6 | 557,
    LocationName.special_zone_6_coin_block_32: BLOCK | SZ6 | 558,
    LocationName.special_zone_6_coin_block_33: BLOCK | SZ6 | 559,
    LocationName.special_zone_2_coin_block_1: BLOCK | SZ2 | 584,
    LocationName.special_zone_2_coin_block_2: BLOCK | SZ2 | 585,
    LocationName.special_zone_2_coin_block_3: BLOCK | SZ2 | 587,
    LocationName.special_zone_2_coin_block_4: BLOCK | SZ2 | 588,
    LocationName.special_zone_2_multi_coin_block_1: BLOCK | SZ2 | 590,
    LocationName.special_zone_2_coin_block_5: BLOCK | SZ2 | 591,
    LocationName.special_zone_2_coin_block_6: BLOCK | SZ2 | 592,
}


item_block_location_table = {
    LocationName.vanilla_secret_2_yoshi_block_1: BLOCK | VS2 | 0,
    LocationName.vanilla_secret_2_powerup_block_1: BLOCK | VS2 | 2,
    LocationName.vanilla_secret_2_powerup_block_2: BLOCK | VS2 | 3,
    LocationName.vanilla_secret_2_gray_pow_block_1: BLOCK | VS2 | 5,
    LocationName.vanilla_secret_3_powerup_block_1: BLOCK | VS3 | 12,
    LocationName.vanilla_secret_3_powerup_block_2: BLOCK | VS3 | 13,
    LocationName.donut_ghost_house_vine_block_1: BLOCK | DGH | 14,
    LocationName.donut_ghost_house_directional_coin_block_1: BLOCK | DGH | 15,
    LocationName.donut_ghost_house_life_block_1: BLOCK | DGH | 16,
    LocationName.donut_ghost_house_life_block_2: BLOCK | DGH | 17,
    LocationName.donut_ghost_house_life_block_3: BLOCK | DGH | 18,
    LocationName.donut_ghost_house_life_block_4: BLOCK | DGH | 19,
    LocationName.donut_plains_3_vine_block_1: BLOCK | DP3 | 23,
    LocationName.donut_plains_3_powerup_block_1: BLOCK | DP3 | 24,
    LocationName.donut_plains_4_powerup_block_1: BLOCK | DP4 | 26,
    LocationName.donut_plains_4_yoshi_block_1: BLOCK | DP4 | 28,
    LocationName.donut_plains_castle_powerup_block_1: BLOCK | DPC | 31,
    LocationName.donut_plains_castle_vine_block_1: BLOCK | DPC | 33,
    LocationName.donut_plains_2_powerup_block_1: BLOCK | DP2 | 43,
    LocationName.donut_plains_2_vine_block_1: BLOCK | DP2 | 48,
    LocationName.donut_secret_1_powerup_block_1: BLOCK | DS1 | 51,
    LocationName.donut_secret_1_powerup_block_2: BLOCK | DS1 | 53,
    LocationName.donut_secret_1_powerup_block_3: BLOCK | DS1 | 54,
    LocationName.donut_secret_1_life_block_1: BLOCK | DS1 | 55,
    LocationName.donut_secret_1_powerup_block_4: BLOCK | DS1 | 56,
    LocationName.donut_secret_1_powerup_block_5: BLOCK | DS1 | 57,
    LocationName.donut_secret_1_key_block_1: BLOCK | DS1 | 58,
    LocationName.vanilla_fortress_powerup_block_1: BLOCK | VDF | 59,
    LocationName.vanilla_fortress_powerup_block_2: BLOCK | VDF | 60,
    LocationName.butter_bridge_1_powerup_block_1: BLOCK | BB1 | 62,
    LocationName.butter_bridge_1_life_block_1: BLOCK | BB1 | 66,
    LocationName.butter_bridge_2_powerup_block_1: BLOCK | BB2 | 67,
    LocationName.butter_bridge_2_yoshi_block_1: BLOCK | BB2 | 69,
    LocationName.twin_bridges_castle_powerup_block_1: BLOCK | TWC | 70,
    LocationName.cheese_bridge_powerup_block_1: BLOCK | CBA | 71,
    LocationName.cheese_bridge_powerup_block_2: BLOCK | CBA | 72,
    LocationName.cheese_bridge_wings_block_1: BLOCK | CBA | 73,
    LocationName.cheese_bridge_powerup_block_3: BLOCK | CBA | 74,
    LocationName.cookie_mountain_powerup_block_1: BLOCK | COM | 84,
    LocationName.cookie_mountain_life_block_1: BLOCK | COM | 85,
    LocationName.cookie_mountain_vine_block_1: BLOCK | COM | 86,
    LocationName.cookie_mountain_yoshi_block_1: BLOCK | COM | 87,
    LocationName.cookie_mountain_powerup_block_2: BLOCK | COM | 90,
    LocationName.soda_lake_powerup_block_1: BLOCK | SOL | 110,
    LocationName.donut_secret_house_powerup_block_1: BLOCK | DSH | 111,
    LocationName.donut_secret_house_life_block_1: BLOCK | DSH | 113,
    LocationName.donut_secret_house_vine_block_1: BLOCK | DSH | 114,
    LocationName.donut_secret_house_directional_coin_block_1: BLOCK | DSH | 115,
    LocationName.donut_plains_1_yoshi_block_1: BLOCK | DP1 | 118,
    LocationName.donut_plains_1_vine_block_1: BLOCK | DP1 | 119,
    LocationName.sunken_ghost_ship_powerup_block_1: BLOCK | SGS | 139,
    LocationName.sunken_ghost_ship_star_block_1: BLOCK | SGS | 140,
    LocationName.chocolate_fortress_powerup_block_1: BLOCK | CIF | 144,
    LocationName.chocolate_fortress_powerup_block_2: BLOCK | CIF | 145,
    LocationName.chocolate_island_5_yoshi_block_1: BLOCK | CI5 | 149,
    LocationName.chocolate_island_5_powerup_block_1: BLOCK | CI5 | 150,
    LocationName.chocolate_island_5_life_block_1: BLOCK | CI5 | 151,
    LocationName.chocolate_island_4_blue_pow_block_1: BLOCK | CI4 | 154,
    LocationName.chocolate_island_4_powerup_block_1: BLOCK | CI4 | 155,
    LocationName.forest_fortress_powerup_block_1: BLOCK | FIF | 157,
    LocationName.forest_fortress_life_block_1: BLOCK | FIF | 158,
    LocationName.forest_fortress_life_block_2: BLOCK | FIF | 159,
    LocationName.forest_fortress_life_block_3: BLOCK | FIF | 160,
    LocationName.forest_fortress_life_block_4: BLOCK | FIF | 161,
    LocationName.forest_fortress_life_block_5: BLOCK | FIF | 162,
    LocationName.forest_fortress_life_block_6: BLOCK | FIF | 163,
    LocationName.forest_fortress_life_block_7: BLOCK | FIF | 164,
    LocationName.forest_fortress_life_block_8: BLOCK | FIF | 165,
    LocationName.forest_fortress_life_block_9: BLOCK | FIF | 166,
    LocationName.chocolate_ghost_house_powerup_block_1: BLOCK | CGH | 168,
    LocationName.chocolate_ghost_house_powerup_block_2: BLOCK | CGH | 169,
    LocationName.chocolate_ghost_house_life_block_1: BLOCK | CGH | 170,
    LocationName.chocolate_island_1_yoshi_block_1: BLOCK | CI1 | 173,
    LocationName.chocolate_island_1_life_block_1: BLOCK | CI1 | 175,
    LocationName.chocolate_island_3_powerup_block_1: BLOCK | CI3 | 176,
    LocationName.chocolate_island_3_powerup_block_2: BLOCK | CI3 | 177,
    LocationName.chocolate_island_3_powerup_block_3: BLOCK | CI3 | 178,
    LocationName.chocolate_island_3_vine_block_1: BLOCK | CI3 | 180,
    LocationName.chocolate_island_3_life_block_1: BLOCK | CI3 | 181,
    LocationName.chocolate_island_3_life_block_2: BLOCK | CI3 | 182,
    LocationName.chocolate_island_3_life_block_3: BLOCK | CI3 | 183,
    LocationName.chocolate_island_2_yoshi_block_1: BLOCK | CI2 | 186,
    LocationName.chocolate_island_2_powerup_block_1: BLOCK | CI2 | 190,
    LocationName.chocolate_island_2_blue_pow_block_1: BLOCK | CI2 | 191,
    LocationName.yoshis_island_castle_powerup_block_1: BLOCK | YIC | 202,
    LocationName.yoshis_island_4_powerup_block_1: BLOCK | YI4 | 207,
    LocationName.yoshis_island_4_star_block_1: BLOCK | YI4 | 209,
    LocationName.yoshis_island_3_yoshi_block_1: BLOCK | YI3 | 240,
    LocationName.yoshis_island_3_powerup_block_1: BLOCK | YI3 | 264,
    LocationName.yoshis_island_1_life_block_1: BLOCK | YI1 | 302,
    LocationName.yoshis_island_1_powerup_block_1: BLOCK | YI1 | 303,
    LocationName.yoshis_island_2_yoshi_block_1: BLOCK | YI2 | 314,
    LocationName.yoshis_island_2_yoshi_block_2: BLOCK | YI2 | 316,
    LocationName.yoshis_island_2_vine_block_1: BLOCK | YI2 | 318,
    LocationName.vanilla_ghost_house_powerup_block_1: BLOCK | VDH | 320,
    LocationName.vanilla_ghost_house_vine_block_1: BLOCK | VDH | 321,
    LocationName.vanilla_ghost_house_powerup_block_2: BLOCK | VDH | 322,
    LocationName.vanilla_ghost_house_blue_pow_block_1: BLOCK | VDH | 324,
    LocationName.vanilla_secret_1_powerup_block_1: BLOCK | VS1 | 326,
    LocationName.vanilla_secret_1_vine_block_1: BLOCK | VS1 | 328,
    LocationName.vanilla_secret_1_vine_block_2: BLOCK | VS1 | 329,
    LocationName.vanilla_secret_1_powerup_block_2: BLOCK | VS1 | 332,
    LocationName.vanilla_dome_3_powerup_block_1: BLOCK | VD3 | 336,
    LocationName.vanilla_dome_3_powerup_block_2: BLOCK | VD3 | 339,
    LocationName.vanilla_dome_3_powerup_block_3: BLOCK | VD3 | 341,
    LocationName.vanilla_dome_3_yoshi_block_1: BLOCK | VD3 | 342,
    LocationName.vanilla_dome_3_powerup_block_4: BLOCK | VD3 | 343,
    LocationName.donut_secret_2_directional_coin_block_1: BLOCK | DS2 | 350,
    LocationName.donut_secret_2_vine_block_1: BLOCK | DS2 | 351,
    LocationName.donut_secret_2_star_block_1: BLOCK | DS2 | 352,
    LocationName.donut_secret_2_powerup_block_1: BLOCK | DS2 | 353,
    LocationName.donut_secret_2_star_block_2: BLOCK | DS2 | 354,
    LocationName.valley_of_bowser_4_powerup_block_1: BLOCK | VB4 | 356,
    LocationName.valley_of_bowser_4_vine_block_1: BLOCK | VB4 | 357,
    LocationName.valley_of_bowser_4_yoshi_block_1: BLOCK | VB4 | 358,
    LocationName.valley_of_bowser_4_life_block_1: BLOCK | VB4 | 359,
    LocationName.valley_of_bowser_4_powerup_block_2: BLOCK | VB4 | 360,
    LocationName.valley_of_bowser_3_powerup_block_1: BLOCK | VB3 | 366,
    LocationName.valley_of_bowser_3_powerup_block_2: BLOCK | VB3 | 367,
    LocationName.valley_ghost_house_powerup_block_1: BLOCK | VBH | 370,
    LocationName.valley_ghost_house_directional_coin_block_1: BLOCK | VBH | 371,
    LocationName.valley_of_bowser_2_powerup_block_1: BLOCK | VB2 | 372,
    LocationName.valley_of_bowser_2_powerup_block_2: BLOCK | VB2 | 374,
    LocationName.valley_of_bowser_2_wings_block_1: BLOCK | VB2 | 375,
    LocationName.valley_of_bowser_1_vine_block_1: BLOCK | VB1 | 384,
    LocationName.chocolate_secret_powerup_block_1: BLOCK | CSA | 385,
    LocationName.chocolate_secret_powerup_block_2: BLOCK | CSA | 386,
    LocationName.vanilla_dome_2_powerup_block_1: BLOCK | VD2 | 388,
    LocationName.vanilla_dome_2_vine_block_1: BLOCK | VD2 | 391,
    LocationName.vanilla_dome_2_powerup_block_2: BLOCK | VD2 | 395,
    LocationName.vanilla_dome_2_powerup_block_3: BLOCK | VD2 | 396,
    LocationName.vanilla_dome_2_powerup_block_4: BLOCK | VD2 | 397,
    LocationName.vanilla_dome_2_powerup_block_5: BLOCK | VD2 | 398,
    LocationName.vanilla_dome_4_powerup_block_1: BLOCK | VD4 | 401,
    LocationName.vanilla_dome_4_powerup_block_2: BLOCK | VD4 | 402,
    LocationName.vanilla_dome_4_life_block_1: BLOCK | VD4 | 406,
    LocationName.vanilla_dome_1_powerup_block_1: BLOCK | VD1 | 413,
    LocationName.vanilla_dome_1_powerup_block_2: BLOCK | VD1 | 414,
    LocationName.vanilla_dome_1_life_block_1: BLOCK | VD1 | 416,
    LocationName.vanilla_dome_1_powerup_block_3: BLOCK | VD1 | 417,
    LocationName.vanilla_dome_1_vine_block_1: BLOCK | VD1 | 418,
    LocationName.vanilla_dome_1_star_block_1: BLOCK | VD1 | 419,
    LocationName.vanilla_dome_1_powerup_block_4: BLOCK | VD1 | 420,
    LocationName.vanilla_dome_castle_life_block_1: BLOCK | VDC | 422,
    LocationName.vanilla_dome_castle_life_block_2: BLOCK | VDC | 423,
    LocationName.vanilla_dome_castle_powerup_block_1: BLOCK | VDC | 424,
    LocationName.vanilla_dome_castle_life_block_3: BLOCK | VDC | 425,
    LocationName.forest_ghost_house_powerup_block_1: BLOCK | FGH | 428,
    LocationName.forest_ghost_house_powerup_block_2: BLOCK | FGH | 430,
    LocationName.forest_ghost_house_life_block_1: BLOCK | FGH | 431,
    LocationName.forest_of_illusion_1_powerup_block_1: BLOCK | FI1 | 432,
    LocationName.forest_of_illusion_1_yoshi_block_1: BLOCK | FI1 | 433,
    LocationName.forest_of_illusion_1_powerup_block_2: BLOCK | FI1 | 434,
    LocationName.forest_of_illusion_1_key_block_1: BLOCK | FI1 | 435,
    LocationName.forest_of_illusion_1_life_block_1: BLOCK | FI1 | 436,
    LocationName.forest_of_illusion_4_powerup_block_1: BLOCK | FI4 | 442,
    LocationName.forest_of_illusion_4_powerup_block_2: BLOCK | FI4 | 446,
    LocationName.forest_of_illusion_2_powerup_block_1: BLOCK | FI2 | 451,
    LocationName.forest_secret_powerup_block_1: BLOCK | FSA | 457,
    LocationName.forest_secret_powerup_block_2: BLOCK | FSA | 458,
    LocationName.forest_secret_life_block_1: BLOCK | FSA | 459,
    LocationName.forest_of_illusion_3_yoshi_block_1: BLOCK | FI3 | 460,
    LocationName.special_zone_8_yoshi_block_1: BLOCK | SZ8 | 487,
    LocationName.special_zone_8_blue_pow_block_1: BLOCK | SZ8 | 493,
    LocationName.special_zone_8_powerup_block_1: BLOCK | SZ8 | 494,
    LocationName.special_zone_8_star_block_1: BLOCK | SZ8 | 495,
    LocationName.special_zone_8_powerup_block_2: BLOCK | SZ8 | 515,
    LocationName.special_zone_7_powerup_block_1: BLOCK | SZ7 | 517,
    LocationName.special_zone_7_yoshi_block_1: BLOCK | SZ7 | 518,
    LocationName.special_zone_7_powerup_block_2: BLOCK | SZ7 | 520,
    LocationName.special_zone_6_powerup_block_1: BLOCK | SZ6 | 522,
    LocationName.special_zone_6_yoshi_block_1: BLOCK | SZ6 | 525,
    LocationName.special_zone_6_life_block_1: BLOCK | SZ6 | 526,
    LocationName.special_zone_6_powerup_block_2: BLOCK | SZ6 | 554,
    LocationName.special_zone_5_yoshi_block_1: BLOCK | SZ5 | 560,
    LocationName.special_zone_1_vine_block_1: BLOCK | SZ1 | 561,
    LocationName.special_zone_1_vine_block_2: BLOCK | SZ1 | 562,
    LocationName.special_zone_1_vine_block_3: BLOCK | SZ1 | 563,
    LocationName.special_zone_1_vine_block_4: BLOCK | SZ1 | 564,
    LocationName.special_zone_1_life_block_1: BLOCK | SZ1 | 565,
    LocationName.special_zone_1_vine_block_5: BLOCK | SZ1 | 566,
    LocationName.special_zone_1_blue_pow_block_1: BLOCK | SZ1 | 567,
    LocationName.special_zone_1_vine_block_6: BLOCK | SZ1 | 568,
    LocationName.special_zone_1_powerup_block_1: BLOCK | SZ1 | 569,
    LocationName.special_zone_2_powerup_block_1: BLOCK | SZ2 | 583,
    LocationName.special_zone_2_powerup_block_2: BLOCK | SZ2 | 586,
    LocationName.special_zone_2_powerup_block_3: BLOCK | SZ2 | 589,
    LocationName.special_zone_3_powerup_block_1: BLOCK | SZ3 | 593,
    LocationName.special_zone_3_yoshi_block_1: BLOCK | SZ3 | 594,
    LocationName.special_zone_3_wings_block_1: BLOCK | SZ3 | 595,
    LocationName.special_zone_4_powerup_block_1: BLOCK | SZ4 | 596,
    LocationName.special_zone_4_star_block_1: BLOCK | SZ4 | 597,
    LocationName.star_road_2_star_block_1: BLOCK | SR2 | 598,
    LocationName.star_road_3_key_block_1: BLOCK | SR3 | 599,
    LocationName.star_road_4_powerup_block_1: BLOCK | SR4 | 600,
    LocationName.star_road_4_key_block_1: BLOCK | SR4 | 608,
    LocationName.star_road_5_directional_coin_block_1: BLOCK | SR5 | 609,
    LocationName.star_road_5_life_block_1: BLOCK | SR5 | 610,
    LocationName.star_road_5_vine_block_1: BLOCK | SR5 | 611,
}


bowser_location_table = {
    LocationName.bowser: GOAL | 0,
}

yoshi_house_location_table = {
    LocationName.yoshis_house: GOAL | 2,
}

egg_location_table: dict[str, int] = {}
castle_location_table: dict[str, int] = {}
ghost_house_location_table: dict[str, int] = {}
switch_palace_location_table: dict[str, int] = {}
for loc_name, loc_id in level_location_table.items():
    egg_loc_name = f"{loc_name} (Hidden Egg)"
    egg_location_table[egg_loc_name] = loc_id | 0x01
    if loc_name in castle_locations:
        castle_location_table[egg_loc_name] = loc_id | 0x01
    if loc_name in ghost_house_locations:
        ghost_house_location_table[egg_loc_name] = loc_id | 0x01
    if loc_name in switch_palace_locations:
        switch_palace_location_table[egg_loc_name] = loc_id | 0x01

all_locations = {
    **level_location_table,
    **dragon_coin_location_table,
    **moon_location_table,
    **hidden_1ups_location_table,
    **prize_location_table,
    **midway_point_location_table,
    **ysp_block_location_table,
    **gsp_block_location_table,
    **pswitch_block_location_table,
    **flying_block_location_table,
    **invisible_block_location_table,
    **coin_block_location_table,
    **item_block_location_table,
    **bowser_location_table,
    **yoshi_house_location_table,
    **egg_location_table,
    **room_location_table,
}

sorted_locations_table: typing.Dict[int, typing.List[int]] = {}
for loc_name, loc_id in all_locations.items():
    level_num = loc_id >> 24
    if level_num not in sorted_locations_table.keys():
        sorted_locations_table[level_num] = []
    sorted_locations_table[level_num].append(loc_id)

special_zone_level_names = [
    LocationName.special_zone_1_exit_1,
    LocationName.special_zone_2_exit_1,
    LocationName.special_zone_3_exit_1,
    LocationName.special_zone_4_exit_1,
    LocationName.special_zone_5_exit_1,
    LocationName.special_zone_6_exit_1,
    LocationName.special_zone_7_exit_1,
    LocationName.special_zone_8_exit_1,
]

special_zone_dragon_coin_names = [
    LocationName.special_zone_1_dragon,
    LocationName.special_zone_2_dragon,
    LocationName.special_zone_3_dragon,
    LocationName.special_zone_4_dragon,
    LocationName.special_zone_5_dragon,
    LocationName.special_zone_6_dragon,
    LocationName.special_zone_7_dragon,
    LocationName.special_zone_8_dragon,
]

special_zone_hidden_1up_names = [
    LocationName.special_zone_1_hidden_1up
]

special_zone_blocksanity_names = [
    LocationName.special_zone_8_yoshi_block_1,
    LocationName.special_zone_8_coin_block_1,
    LocationName.special_zone_8_coin_block_2,
    LocationName.special_zone_8_coin_block_3,
    LocationName.special_zone_8_coin_block_4,
    LocationName.special_zone_8_coin_block_5,
    LocationName.special_zone_8_blue_pow_block_1,
    LocationName.special_zone_8_powerup_block_1,
    LocationName.special_zone_8_star_block_1,
    LocationName.special_zone_8_coin_block_6,
    LocationName.special_zone_8_coin_block_7,
    LocationName.special_zone_8_coin_block_8,
    LocationName.special_zone_8_coin_block_9,
    LocationName.special_zone_8_coin_block_10,
    LocationName.special_zone_8_coin_block_11,
    LocationName.special_zone_8_coin_block_12,
    LocationName.special_zone_8_coin_block_13,
    LocationName.special_zone_8_coin_block_14,
    LocationName.special_zone_8_coin_block_15,
    LocationName.special_zone_8_coin_block_16,
    LocationName.special_zone_8_coin_block_17,
    LocationName.special_zone_8_coin_block_18,
    LocationName.special_zone_8_multi_coin_block_1,
    LocationName.special_zone_8_coin_block_19,
    LocationName.special_zone_8_coin_block_20,
    LocationName.special_zone_8_coin_block_21,
    LocationName.special_zone_8_coin_block_22,
    LocationName.special_zone_8_coin_block_23,
    LocationName.special_zone_8_powerup_block_2,
    LocationName.special_zone_8_flying_block_1,
    LocationName.special_zone_7_powerup_block_1,
    LocationName.special_zone_7_yoshi_block_1,
    LocationName.special_zone_7_coin_block_1,
    LocationName.special_zone_7_powerup_block_2,
    LocationName.special_zone_7_coin_block_2,
    LocationName.special_zone_6_powerup_block_1,
    LocationName.special_zone_6_coin_block_1,
    LocationName.special_zone_6_coin_block_2,
    LocationName.special_zone_6_yoshi_block_1,
    LocationName.special_zone_6_life_block_1,
    LocationName.special_zone_6_multi_coin_block_1,
    LocationName.special_zone_6_coin_block_3,
    LocationName.special_zone_6_coin_block_4,
    LocationName.special_zone_6_coin_block_5,
    LocationName.special_zone_6_coin_block_6,
    LocationName.special_zone_6_coin_block_7,
    LocationName.special_zone_6_coin_block_8,
    LocationName.special_zone_6_coin_block_9,
    LocationName.special_zone_6_coin_block_10,
    LocationName.special_zone_6_coin_block_11,
    LocationName.special_zone_6_coin_block_12,
    LocationName.special_zone_6_coin_block_13,
    LocationName.special_zone_6_coin_block_14,
    LocationName.special_zone_6_coin_block_15,
    LocationName.special_zone_6_coin_block_16,
    LocationName.special_zone_6_coin_block_17,
    LocationName.special_zone_6_coin_block_18,
    LocationName.special_zone_6_coin_block_19,
    LocationName.special_zone_6_coin_block_20,
    LocationName.special_zone_6_coin_block_21,
    LocationName.special_zone_6_coin_block_22,
    LocationName.special_zone_6_coin_block_23,
    LocationName.special_zone_6_coin_block_24,
    LocationName.special_zone_6_coin_block_25,
    LocationName.special_zone_6_coin_block_26,
    LocationName.special_zone_6_coin_block_27,
    LocationName.special_zone_6_coin_block_28,
    LocationName.special_zone_6_powerup_block_2,
    LocationName.special_zone_6_coin_block_29,
    LocationName.special_zone_6_coin_block_30,
    LocationName.special_zone_6_coin_block_31,
    LocationName.special_zone_6_coin_block_32,
    LocationName.special_zone_6_coin_block_33,
    LocationName.special_zone_5_yoshi_block_1,
    LocationName.special_zone_1_vine_block_1,
    LocationName.special_zone_1_vine_block_2,
    LocationName.special_zone_1_vine_block_3,
    LocationName.special_zone_1_vine_block_4,
    LocationName.special_zone_1_life_block_1,
    LocationName.special_zone_1_vine_block_5,
    LocationName.special_zone_1_blue_pow_block_1,
    LocationName.special_zone_1_vine_block_6,
    LocationName.special_zone_1_powerup_block_1,
    LocationName.special_zone_1_pswitch_coin_block_1,
    LocationName.special_zone_1_pswitch_coin_block_2,
    LocationName.special_zone_1_pswitch_coin_block_3,
    LocationName.special_zone_1_pswitch_coin_block_4,
    LocationName.special_zone_1_pswitch_coin_block_5,
    LocationName.special_zone_1_pswitch_coin_block_6,
    LocationName.special_zone_1_pswitch_coin_block_7,
    LocationName.special_zone_1_pswitch_coin_block_8,
    LocationName.special_zone_1_pswitch_coin_block_9,
    LocationName.special_zone_1_pswitch_coin_block_10,
    LocationName.special_zone_1_pswitch_coin_block_11,
    LocationName.special_zone_1_pswitch_coin_block_12,
    LocationName.special_zone_1_pswitch_coin_block_13,
    LocationName.special_zone_2_powerup_block_1,
    LocationName.special_zone_2_coin_block_1,
    LocationName.special_zone_2_coin_block_2,
    LocationName.special_zone_2_powerup_block_2,
    LocationName.special_zone_2_coin_block_3,
    LocationName.special_zone_2_coin_block_4,
    LocationName.special_zone_2_powerup_block_3,
    LocationName.special_zone_2_multi_coin_block_1,
    LocationName.special_zone_2_coin_block_5,
    LocationName.special_zone_2_coin_block_6,
    LocationName.special_zone_3_powerup_block_1,
    LocationName.special_zone_3_yoshi_block_1,
    LocationName.special_zone_3_wings_block_1,
    LocationName.special_zone_4_powerup_block_1,
    LocationName.special_zone_4_star_block_1
]

location_table = {}

location_groups = {
    "Normal Exits": {location for location in level_location_table.keys() if "- Normal Exit" in location},
    "Secret Exits": {location for location in level_location_table.keys() if "- Secret Exit" in location},
    "Castles": {location for location in level_location_table.keys() if "Castle - Normal Exit" in location or "Fortress - Normal Exit" in location},
    "Ghost Houses": {location for location in level_location_table.keys() if "House" in location},
    "Switch Palaces": {location for location in level_location_table.keys() if "Switch Palace" in location},
    "Dragon Coins": {location for location in dragon_coin_location_table.keys()},
    "3-Up Moons": {location for location in moon_location_table.keys()},
    "Hidden 1-Ups": {location for location in hidden_1ups_location_table.keys()},
    "Star Blocks": {location for location in prize_location_table.keys()},
    "Midway Points": {location for location in midway_point_location_table.keys()},
    "Rooms": {location for location in room_location_table.keys()},
}

def setup_locations(world: "WaffleWorld"):
    location_table = {**level_location_table}

    if world.options.dragon_coin_checks:
        location_table.update(dragon_coin_location_table)

    if world.options.moon_checks:
        location_table.update(moon_location_table)

    if world.options.hidden_1up_checks:
        location_table.update(hidden_1ups_location_table)

    if world.options.star_block_checks:
        location_table.update(prize_location_table)

    if world.options.midway_point_checks:
        location_table.update(midway_point_location_table)

    if world.options.room_checks:
        location_table.update(room_location_table)

    if "Coin Blocks" in world.options.block_checks.value:
        location_table.update(coin_block_location_table)
    if "Item Blocks" in world.options.block_checks.value:
        location_table.update(item_block_location_table)
    if "Yellow Switch Palace Blocks" in world.options.block_checks.value:
        location_table.update(ysp_block_location_table)
    if "Green Switch Palace Blocks" in world.options.block_checks.value:
        location_table.update(gsp_block_location_table)
    if "Invisible Blocks" in world.options.block_checks.value:
        location_table.update(invisible_block_location_table)
    if "P-Switch Blocks" in world.options.block_checks.value:
        location_table.update(pswitch_block_location_table)
    if "Flying Blocks" in world.options.block_checks.value:
        location_table.update(flying_block_location_table)

    if world.options.goal == Goal.option_yoshi_house:
        location_table.update(yoshi_house_location_table)
    else:
        location_table.update(bowser_location_table)

    if "Every Level" in world.options.yoshi_egg_placement.value:
        location_table.update(egg_location_table)
    else:
        if "Castles" in world.options.yoshi_egg_placement.value:
            location_table.update(castle_location_table)
        if "Switch Palaces" in world.options.yoshi_egg_placement.value:
            location_table.update(switch_palace_location_table)
        if "Ghost Houses" in world.options.yoshi_egg_placement.value:
            location_table.update(ghost_house_location_table)

    return location_table


lookup_id_to_name: typing.Dict[int, str] = {id: name for name, _ in all_locations.items()}
