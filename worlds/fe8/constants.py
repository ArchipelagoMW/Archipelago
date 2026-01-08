CLIENT_TITLE = "FE8Client"
FE8_NAME = "Fire Emblem Sacred Stones"

FE8_ID_PREFIX = 0xFE8_000
NUM_LEVELCAPS: int = (40 - 10) // 5

HOLY_WEAPONS = {
    "Sieglinde": "Sword",
    "Siegmund": "Lance",
    "Gleipnir": "Dark",
    "Garm": "Axe",
    "Nidhogg": "Bow",
    "Vidofnir": "Lance",
    "Excalibur": "Anima",
    "Audhulma": "Sword",
    "Ivaldi": "Light",
    "Latona": "Staff",
}

WEAPON_TYPES = ["Sword", "Lance", "Axe", "Bow", "Anima", "Light", "Dark", "Staff"]
NUM_WEAPON_LEVELS = 3

FILLER_ITEMS = [
    "AngelicRobe",
    "EnergyRing",
    "SecretBook",
    "Speedwings",
    "GoddessIcon",
    "DragonShield",
    "Talisman",
    "BodyRing",
    "Boots",
    "KnightCrest",
    "HeroCrest",
    "OrionsBolt",
    "GuidingRing",
    "ElysianWhip",
    "OceanSeal",
    "MasterSeal",
]

FEMALE_JOBS = [
    (0x06, 0x05),  # Cavalier
    (0x08, 0x07),  # Paladin
    (0x0A, 0x09),  # Armour Knight
    (0x0C, 0x0B),  # General
    (0x10, 0x0F),  # Mercenary
    (0x12, 0x11),  # Hero
    (0x14, 0x13),  # Myrmidon
    (0x16, 0x15),  # Swordmaster
    (0x18, 0x17),  # Assassin
    (0x1A, 0x19),  # Archer
    (0x1C, 0x1B),  # Sniper
    (0x1E, 0x1D),  # Ranger
    (0x20, 0x1F),  # Wyvern Rider
    (0x22, 0x21),  # Wyvern Lord
    (0x24, 0x23),  # Wyvern Knight
    (0x26, 0x25),  # Mage
    (0x28, 0x27),  # Sage
    (0x2A, 0x29),  # Mage Knight
    (0x2C, 0x2B),  # Bishop
    (0x2E, 0x2D),  # Shaman
    (0x30, 0x2F),  # Druid
    (0x32, 0x31),  # Summoner
    (0x36, 0x35),  # Great Knight
]

ROM_BASE_ADDRESS = 0x08000000
ROM_NAME_ADDR = 0x080000A0

PROC_SIZE = 0x6C
PROC_POOL_ADDR = 0x02024E68
TOTAL_NUM_PROCS = 0x40

# These are literal addresses including the ROM offset because we compare
# against them, rather than reading or writing.
WM_PROC_ADDRESS = 0x08A3EE74
E_PLAYERPHASE_PROC_ADDRESS = 0x0859AAD8

LOCKPICK = 0x6B
CHEST_KEY_5 = 0x79

CHAPTER_UNIT_SIZE = 20
INVENTORY_INDEX = 0xC
INVENTORY_SIZE = 0x4
COORDS_INDEX = 4
REDA_COUNT_INDEX = 7
REDA_PTR_INDEX = 8

CHARACTER_TABLE_BASE = 0x803D30
CHARACTER_SIZE = 52
CHARACTER_WRANK_OFFSET = 20
CHARACTER_STATS_OFFSET = 12
CHARACTER_GROWTHS_OFFSET = 28
CHAR_ABILITY_4_OFFSET = 43

JOB_TABLE_BASE = 0x807110
JOB_SIZE = 84
JOB_STATS_OFFSET = 11
JOB_CAPS_OFFSET = 19
JOB_ABILITY_1_INDEX = 40

SONG_TABLE_BASE = 0x224470
SONG_SIZE = 8

STATS_COUNT = 6  # HP, Str, Skl, Spd, Def, Res (don't need Lck)

MOUNTED_AID_CANTO_MASK = 3
MOUNTED_MONSTERS = [
    0x5D,  # Tarvos
    0x5E,  # Maelduin
    0x5F,  # Mogall
    0x60,  # Mogall
    0x63,  # Gargoyle
    0x64,  # Deathgoyle
]

EIRIKA = 1
EIRIKA_LORD = 2
EIRIKA_LOCK = 1 << 4
EPHRAIM = 15
EPHRAIM_LORD = 1
EPHRAIM_LOCK = 1 << 5

EIRIKA_RAPIER_OFFSET = 0x9EF088
ROSS_CH2_HP_OFFSET = 0x9F03B8

MOVEMENT_COST_TABLE_BASE = 0x80B808
MOVEMENT_COST_ENTRY_SIZE = 65
MOVEMENT_COST_ENTRY_COUNT = 49
MOVEMENT_COST_SENTINEL = 31

IMPORTANT_TERRAIN_TYPES = [
    14,  # Thicket
    15,  # Sand
    16,  # Desert
    17,  # River
    18,  # Mountain
    19,  # Peak
    20,  # Bridge
    21,  # Bridge 2
    22,  # Sea
    23,  # Lake
    26,  # Fence 1
    39,  # Cliff
    47,  # Building 2
    51,  # Fence 2
    54,  # Sky
    55,  # Deeps
    57,  # Inn
    58,  # Barrel
    59,  # Bone
    60,  # Dark
    61,  # Water
    62,  # Gunnels
]

ITEM_TABLE_BASE = 0x809B10
ITEM_SIZE = 36
ITEM_ABILITY_1_INDEX = 8
UNBREAKABLE_FLAG = 1 << 3

HOLY_WEAPON_IDS = [
    0x85,  # Sieglinde
    0x92,  # Siegmund
    0x4A,  # Gleipnir
    0x93,  # Garm
    0x94,  # Nidhogg
    0x8E,  # Vidofnir
    0x3E,  # Excalibur
    0x91,  # Audhulma
    0x87,  # Ivaldi
]

CH15_AUTO_STEEL_LANCE = 0x086664
CH15_AUTO_STEEL_SWORD = 0x086674

AI1_INDEX = 0x10
AI1_IGNORE_LIST_12 = 0x5A8A24

INTERNAL_RANDO_CLASS_WEIGHTS_OFFS = 0x8D2060
INTERNAL_RANDO_CLASS_WEIGHT_ENTRY_SIZE = 12
INTERNAL_RANDO_CLASS_WEIGHTS_COUNT = 30
INTERNAL_RANDO_CLASS_WEIGHT_NUM_CLASSES = 5
INTERNAL_RANDO_WEAPONS_OFFS = 0x8D2440
INTERNAL_RANDO_WEAPONS_ENTRY_SIZE = 0x20
INTERNAL_RANDO_WEAPONS_NUM_ITEMS = 5
INTERNAL_RANDO_WEAPONS_MAX_CLASSES = 22

# CR-soon cam: This is stretching the definition of a "constant" and should
# probably go into a data file instead
INTERNAL_RANDO_WEAPON_TABLE_ROWS = [
    ("None", -1),
    ("Sword", 0),
    ("Sword", 1),
    ("Sword", 3),
    ("Sword", 2),
    ("Sword", 4),
    ("Lance", 0),
    # CR-soon cam: this row has both Runesword and Javelin in it.
    ("Lance", 1),
    ("Lance", 3),
    ("Lance", 2),
    ("Lance", 4),
    ("Axe", 0),
    ("Axe", 1),
    ("Axe", 3),
    ("Axe", 2),
    ("Axe", 4),
    ("Bow", 0),
    ("Bow", 1),
    ("Bow", 3),
    ("Bow", 2),
    ("Bow", 4),
    ("Claw", 0),
    ("Claw", 1),
    ("Claw", 2),
    ("Claw", 3),
    ("MonsterDark", 0),
    ("MonsterDark", 1),
    ("Fang", 0),
    ("Fang", 1),
    ("MonsterDark", 3),
]
