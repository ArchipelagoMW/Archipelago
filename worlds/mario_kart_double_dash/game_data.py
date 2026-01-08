from enum import IntEnum
from typing import NamedTuple


class Character(NamedTuple):
    id: int
    name: str
    weight: int
    default_kart: int
    item_offset: int

CHARACTERS = [
    Character(0, "Mario", 1, 8, 21),
    Character(1, "Luigi", 1, 9, 21),
    Character(2, "Peach", 1, 10, 14),
    Character(3, "Daisy", 1, 11, 14),
    Character(4, "Yoshi", 1, 12, 11),
    Character(5, "Birdo", 1, 13, 11),
    Character(6, "Baby Mario", 0, 0, 7),
    Character(7, "Baby Luigi", 0, 1, 7),
    Character(8, "Toad", 0, 6, 12),
    Character(9, "Toadette", 0, 7, 12),
    Character(10, "Koopa", 0, 2, 17),
    Character(11, "Paratroopa", 0, 3, 17),
    Character(12, "Donkey Kong", 2, 16, 4),
    Character(13, "Diddy Kong", 0, 4, 4),
    Character(14, "Bowser", 2, 17, 1),
    Character(15, "Bowser Jr.", 0, 5, 1),
    Character(16, "Wario", 2, 15, 8),
    Character(17, "Waluigi", 1, 14, 8),
    Character(18, "Petey Piranha", 2, 18, 8),
    Character(19, "King Boo", 2, 19, 8),
]

class KartStats(NamedTuple):
    speed_on_road: float
    speed_off_road_sand: float
    speed_off_road_grass: float
    speed_off_road_mud: float
    acceleration_1: float
    acceleration_2: float
    mini_turbo: float
    mass: float
    roll: float
    steer: float

class Kart(NamedTuple):
    id: int
    name: str
    weight: int
    unlock_id: int
    stats: KartStats

# Kart stats table based on work by Ralf.
#                Speed1    Speed2   Speed3   Speed4   Accel1    Accel2    Turbo     Mass    Roll   Steer
KARTS = [
    Kart(0, "Goo-Goo Buggy", 0, 5,
        KartStats(136.0,    116.0,    92.0,    20.0,    3.00,    0.010,    30.0,    1.25,    5.0,    2.0)),
    Kart(1, "Rattle Buggy", 0, 13,
        KartStats(137.0,    117.0,    92.0,    20.0,    2.00,    0.010,    30.0,    1.25,    5.0,    2.0)),
    Kart(2, "Koopa Dasher", 0, 3,
        KartStats(137.0,    117.0,    89.0,    20.0,    2.00,    0.010,    30.0,    1.50,    4.0,    2.0)),
    Kart(3, "Para-Wing", 0, 11,
        KartStats(136.0,    116.0,    89.0,    20.0,    3.00,    0.010,    30.0,    1.50,    4.0,    2.0)),
    Kart(4, "Barrel Train", 0, 9,
        KartStats(143.0,    123.0,    86.0,    20.0,    0.15,    0.005,    30.0,    2.00,    5.0,    0.9)),
    Kart(5, "Bullet Blaster", 0, 15,
        KartStats(143.0,    123.0,    68.0,    20.0,    0.30,    0.005,    30.0,    1.00,    5.0,    0.8)),
    Kart(6, "Toad Kart", 0, 16,
        KartStats(138.0,    118.0,    92.0,    20.0,    1.00,    0.010,    30.0,    1.25,    5.0,    3.0)),
    Kart(7, "Toadette Kart", 0, 17,
        KartStats(136.0,    116.0,    92.0,    20.0,    3.00,    0.010,    30.0,    1.25,    5.0,    3.0)),
    Kart(8, "Red Fire", 1, 0,
        KartStats(140.0,    120.0,    80.0,    20.0,    0.30,    0.005,    20.0,    2.00,    4.5,    1.0)),
    Kart(9, "Green Fire", 1, 8,
        KartStats(142.0,    122.0,    77.0,    20.0,    0.15,    0.005,    20.0,    1.75,    4.5,    1.0)),
    Kart(10, "Heart Coach", 1, 4,
        KartStats(139.0,    119.0,    83.0,    20.0,    1.00,    0.005,    20.0,    2.00,    5.0,    1.5)),
    Kart(11, "Bloom Coach", 1, 12,
        KartStats(141.0,    121.0,    77.0,    20.0,    0.50,    0.005,    20.0,    1.50,    5.0,    1.5)),
    Kart(12, "Turbo Yoshi", 1, 2,
        KartStats(139.0,    119.0,    80.0,    20.0,    1.00,    0.005,    20.0,    2.25,    4.5,    1.0)),
    Kart(13, "Turbo Birdo", 1, 10,
        KartStats(141.0,    121.0,    77.0,    20.0,    0.30,    0.005,    20.0,    2.50,    4.5,    1.0)),
    Kart(14, "Waluigi Racer", 1, 14,
        KartStats(140.0,    120.0,    92.0,    20.0,    0.50,    0.005,    20.0,    2.25,    4.5,    1.0)),
    Kart(15, "Wario Car", 2, 6,
        KartStats(142.0,    122.0,    74.0,    20.0,    0.15,    0.005,    10.0,    2.50,    5.0,    1.0)),
    Kart(16, "DK Jumbo", 2, 1,
        KartStats(143.0,    123.0,    71.0,    20.0,    0.10,    0.005,    10.0,    2.75,    5.0,    0.9)),
    Kart(17, "Koopa King", 2, 7,
        KartStats(144.0,    124.0,    68.0,    20.0,    0.08,    0.005,    10.0,    3.00,    5.0,    0.9)),
    Kart(18, "Piranha Pipes", 2, 19,
        KartStats(143.0,    123.0,    86.0,    20.0,    0.10,    0.005,    10.0,    3.00,    5.0,    0.9)),
    Kart(19, "Boo Pipes", 2, 18,
        KartStats(137.0,    117.0,    92.0,    20.0,    2.00,    0.010,    10.0,    3.00,    5.0,    0.9)),
    Kart(20, "Parade Kart", -1, 20,
        KartStats(142.0,    122.0,    74.0,    20.0,    0.30,    0.005,    30.0,    2.50,    5.0,    1.0)),
]

NORMAL_CUPS = [
    "Mushroom Cup",
    "Flower Cup",
    "Star Cup",
    "Special Cup",
]
CUPS = NORMAL_CUPS + ["All Cup Tour"]
CUP_ALL_CUP_TOUR = 4

class CourseType(IntEnum):
    RACE = 0
    BATTLE = 1
    CEREMONY = 2

class Course(NamedTuple):
    name: str = ""
    id: int = -1
    type: CourseType = CourseType.RACE
    staff_time: float = 0
    good_time: float = 0
    owners: list[int] = []
    laps: int = 3


RACE_COURSES = [
    # Race courses:
    Course("Luigi Circuit",     0x24, staff_time =  86.277, good_time = 95, owners = [1]),
    Course("Peach Beach",       0x22, staff_time =  80.404, good_time = 90, owners = [2]),
    Course("Baby Park",         0x21, staff_time =  71.108, good_time = 80, owners = [6, 7], laps = 7),
    Course("Dry Dry Desert",    0x32, staff_time = 110.755, good_time = 120),
    Course("Mushroom Bridge",   0x28, staff_time =  91.458, good_time = 100),
    Course("Mario Circuit",     0x25, staff_time = 101.384, good_time = 115, owners = [0]),
    Course("Daisy Cruiser",     0x23, staff_time = 112.207, good_time = 120, owners = [3]),
    Course("Waluigi Stadium",   0x2a, staff_time = 119.658, good_time = 130, owners = [17]),
    Course("Sherbet Land",      0x33, staff_time =  85.904, good_time = 100),
    Course("Mushroom City",     0x29, staff_time = 110.663, good_time = 120),
    Course("Yoshi Circuit",     0x26, staff_time = 119.866, good_time = 135, owners = [4]),
    Course("DK Mountain",       0x2d, staff_time = 132.639, good_time = 140, owners = [12]),
    Course("Wario Colosseum",   0x2b, staff_time = 141.106, good_time = 155, owners = [16], laps = 2),
    Course("Dino Dino Jungle",  0x2c, staff_time = 120.908, good_time = 140),
    Course("Bowser's Castle",   0x2f, staff_time = 164.690, good_time = 185, owners = [14]),
    Course("Rainbow Road",      0x31, staff_time = 196.476, good_time = 210),
]

COURSES = RACE_COURSES + [
    # Battle courses:
    Course("Cookie Land", 0x3a, CourseType.BATTLE),
    Course("Pipe Plaza", 0x3b, CourseType.BATTLE),
    Course("Block City", 0x36, CourseType.BATTLE),
    Course("Nintendo Gamecube", 0x35, CourseType.BATTLE),
    Course("Luigi's Mansion", 0x34, CourseType.BATTLE),
    Course("Tilt-A-Kart", 0x38, CourseType.BATTLE),
    # Award Ceremony
    Course("Award Ceremony", 0x44, CourseType.CEREMONY),
]

class Modes(IntEnum):
    TIMETRIAL = 1
    GRANDPRIX = 2
    VERSUS = 3
    BATTLE_BALLOON = 4
    BATTLE_SHINE = 7
    BATTLE_BOMB = 6
    CEREMONY = 8

class Item(NamedTuple):
    id: int
    name: str
    short_name: str
    usefulness: int = 0
    weight_table: list[int] = []

ITEMS = [
    Item(0, "Green Shell", "GrSh",          2, [ 90,  50,  25,  10,   1,   1,   1,   1]),
    Item(1, "Bowser's Shell", "BoSh",       3, [ 30,  60, 100, 100, 100,  90,  40,   1]),
    Item(2, "Red Shell", "ReSh",            3, [ 10,  55,  70,  70,  70,  50,  40,  20]),
    Item(3, "Banana", "Ba",                 1, [ 70,  35,  15,   5,   1,   1,   1,   1]),
    Item(4, "Giant Banana", "GBa",          2, [120, 100,  90,  60,  30,   1,   1,   1]),
    Item(5, "Mushroom", "Mu",               4, [  1,  40,  65,  75,  65,  35,  10,  10]),
    Item(6, "Star", "St",                   5, [  1,   1,   1,  10,  20,  30,  40,  40]),
    Item(7, "Chain Chomp", "CC",            4, [  0,   0,   1,   3,  20,  60, 130, 180]),
    Item(8, "Bob-omb", "Bo",                1, [ 10,  70, 100, 100, 100,  90,  40,   0]),
    Item(10, "Lightning", "Li",             3, [  0,   0,   1,   1,   3,  10,  20,  30]),
    Item(11, "Yoshi Egg", "Eg",             4, [ 50,  70,  80,  80,  80,  70,  60,  40]),
    Item(12, "Golden Mushroom", "GMu",      6, [  0,   3,  10,  30,  50,  80, 100, 120]),
    Item(13, "Spiny Shell", "SpSh",         0, [  0,   0,   5,  10,  10,  20,  20,  20]),
    Item(14, "Heart", "He",                 4, [  1,   1,   3,  10,  30,  90, 110, 130]),
    Item(15, "Fake Item", "FI",             0, [ 30,  20,  10,   0,   0,   0,   0,   1]),
    Item(17, "Triple Green Shells", "3GS",  3, [ 20,  50, 100, 100, 100,  90,  40,   1]),
    Item(18, "Triple Mushrooms", "3Mu",     6, [  1,   1,  10,  20,  35,  50,  70,  90]),
    Item(19, "Triple Red Shells", "3RS",    4, [  5,  40,  60,  70,  70,  50,  50,  30]),
    Item(21, "Fireballs", "Fi",             2, [ 30,  70, 100, 100, 100,  90,  40,   1]),
    Item(20, "None", "",                    0, [  0,   0,   0,   0,   0,   0,   0,   0]),
]

ITEM_GREEN_SHELL = ITEMS[0]
ITEM_BOWSER_SHELL = ITEMS[1]
ITEM_RED_SHELL = ITEMS[2]
ITEM_BANANA = ITEMS[3]
ITEM_GIANT_BANANA = ITEMS[4]
ITEM_MUSHROOM = ITEMS[5]
ITEM_STAR = ITEMS[6]
ITEM_CHAIN_CHOMP = ITEMS[7]
ITEM_BOBOMB = ITEMS[8]
ITEM_LIGHTNING = ITEMS[9]
ITEM_YOSHI_EGG = ITEMS[10]
ITEM_GOLDEN_MUSHROOM = ITEMS[11]
ITEM_SPINY_SHELL = ITEMS[12]
ITEM_HEART = ITEMS[13]
ITEM_FAKE_ITEM = ITEMS[14]
ITEM_TRIPLE_GREEN_SHELLS = ITEMS[15]
ITEM_TRIPLE_MUSHROOMS = ITEMS[16]
ITEM_TRIPLE_RED_SHELLS = ITEMS[17]
ITEM_FIREBALLS = ITEMS[18]
ITEM_NONE = ITEMS[19]

TT_ITEM_TABLE = [
    bytes([ITEM_NONE.id, ITEM_MUSHROOM.id]),
    bytes([ITEM_MUSHROOM.id, ITEM_MUSHROOM.id]),
    bytes([ITEM_NONE.id, ITEM_TRIPLE_MUSHROOMS.id]),
    bytes([ITEM_STAR.id, ITEM_TRIPLE_MUSHROOMS.id]),
]


class KartUpgrade(NamedTuple):
    id: int
    name: str
    short_name: str
    usefulness: int

KART_UPGRADES = [
    KartUpgrade(0, "Acceleration Boost", "ACC", 10),
    KartUpgrade(1, "Mini-turbo Extender", "TUR", 10),
    KartUpgrade(2, "Off-road Tires", "OFR", 8),
    KartUpgrade(3, "Extra Weight", "WEI", 2),
    KartUpgrade(4, "Power Steering", "STE", 8),
]

KART_UPGRADE_ACC = KART_UPGRADES[0]
KART_UPGRADE_TURBO = KART_UPGRADES[1]
KART_UPGRADE_OFFROAD = KART_UPGRADES[2]
KART_UPGRADE_WEIGHT = KART_UPGRADES[3]
KART_UPGRADE_STEER = KART_UPGRADES[4]

ENGINE_UPGRADE_USEFULNESS = 50
SKIP_DIFFICULTY_USEFULNESS = 200
