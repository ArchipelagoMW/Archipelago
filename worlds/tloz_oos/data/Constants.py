ROM_HASH = "f2dc6c4e093e4f8c6cbea80e8dbd62cb"
AGES_ROM_HASH = "c4639cc61c049e5a085526bb6cac03bb"

DIRECTION_UP = 0
DIRECTION_RIGHT = 1
DIRECTION_DOWN = 2
DIRECTION_LEFT = 3
DIRECTIONS = [
    DIRECTION_UP,
    DIRECTION_RIGHT,
    DIRECTION_DOWN,
    DIRECTION_LEFT
]

SEASON_SPRING = 0x00
SEASON_SUMMER = 0x01
SEASON_AUTUMN = 0x02
SEASON_WINTER = 0x03
SEASON_CHAOTIC = 0xFF
SEASONS = [
    SEASON_SPRING,
    SEASON_SUMMER,
    SEASON_AUTUMN,
    SEASON_WINTER
]

SEASON_NAMES = {
    SEASON_SPRING: "spring",
    SEASON_SUMMER: "summer",
    SEASON_AUTUMN: "autumn",
    SEASON_WINTER: "winter",
    SEASON_CHAOTIC: "chaotic"
}

SEASON_ITEMS = {
    SEASON_WINTER: "Rod of Seasons (Winter)",
    SEASON_SUMMER: "Rod of Seasons (Summer)",
    SEASON_SPRING: "Rod of Seasons (Spring)",
    SEASON_AUTUMN: "Rod of Seasons (Autumn)",
}

SEED_ITEMS = [
    "Ember Seeds",
    "Scent Seeds",
    "Pegasus Seeds",
    "Gale Seeds",
    "Mystery Seeds",
]

DUNGEON_NAMES = [
    "Hero's Cave",
    "Gnarled Root Dungeon",
    "Snake's Remains",
    "Poison Moth's Lair",
    "Dancing Dragon Dungeon",
    "Unicorn's Cave",
    "Ancient Ruins",
    "Explorer's Crypt",
    "Sword & Shield Dungeon"
]

VALID_RUPEE_PRICE_VALUES = [
    1, 2, 5, 10, 20, 25, 30, 40, 50, 60, 70, 80, 100, 150, 200, 300, 400, 500, 900, 999
]
VALID_RUPEE_ITEM_VALUES = [
    1, 5, 10, 20, 30, 50, 100, 200
]
VALID_ORE_ITEM_VALUES = [
    10, 25, 50
]
MARKET_LOCATIONS = ["subrosianMarket2", "subrosianMarket3", "subrosianMarket4", "subrosianMarket5"]

DEFAULT_SEASONS = {
    "EYEGLASS_LAKE": SEASON_WINTER,
    "HOLODRUM_PLAIN": SEASON_SPRING,
    "EASTERN_SUBURBS": SEASON_AUTUMN,
    "WOODS_OF_WINTER": SEASON_SUMMER,
    "SUNKEN_CITY": SEASON_SUMMER,
    "WESTERN_COAST": SEASON_WINTER,
    "SPOOL_SWAMP": SEASON_AUTUMN,
    "TEMPLE_REMAINS": SEASON_WINTER,
    "LOST_WOODS": SEASON_AUTUMN,
    "TARM_RUINS": SEASON_SPRING,
    "HORON_VILLAGE": SEASON_CHAOTIC
}

DUNGEON_CONNECTIONS = {
    "d0 entrance": "enter d0",
    "d1 entrance": "enter d1",
    "d2 entrance": "enter d2",
    "d3 entrance": "enter d3",
    "d4 entrance": "enter d4",
    "d5 entrance": "enter d5",
    "d6 entrance": "enter d6",
    "d7 entrance": "enter d7",
    "d8 entrance": "enter d8",
}

PORTAL_CONNECTIONS = {
    "eastern suburbs portal": "volcanoes east portal",
    "spool swamp portal": "subrosia market portal",
    "mt. cucco portal": "strange brothers portal",
    "horon village portal": "house of pirates portal",
    "eyeglass lake portal": "great furnace portal",
    "temple remains lower portal": "volcanoes west portal",
    "temple remains upper portal": "d8 entrance portal",
}

LOST_WOODS_ITEM_SEQUENCE = [
    [DIRECTION_LEFT, SEASON_WINTER],
    [DIRECTION_LEFT, SEASON_AUTUMN],
    [DIRECTION_LEFT, SEASON_SPRING],
    [DIRECTION_LEFT, SEASON_SUMMER],
]

LOST_WOODS_MAIN_SEQUENCE = [
    [DIRECTION_LEFT, SEASON_WINTER],
    [DIRECTION_DOWN, SEASON_AUTUMN],
    [DIRECTION_RIGHT, SEASON_SPRING],
    [DIRECTION_UP, SEASON_SUMMER],
]

# The order of keys in this dictionary matters, since it's the same as the one used inside the ROM
OLD_MAN_RUPEE_VALUES = {
    "old man in goron mountain": 300,
    "old man near blaino": 200,
    "old man near d1": 100,
    "old man near western coast house": 300,
    "old man in horon": 100,
    "old man near d6": -200,
    "old man near holly's house": -50,
    "old man near mrs. ruul": -100
}

RUPEE_OLD_MAN_LOCATIONS = [
    "Horon Village: Old Man",
    "North Horon: Old Man Near D1",
    "Holodrum Plain: Old Man Near Blaino's Gym",
    "Goron Mountain: Old Man",
    "Western Coast: Old Man",
    "Woods of Winter: Old Man",
    "Holodrum Plain: Old Man Near Mrs. Ruul's House",
    "Tarm Ruins: Old Man Near D6"
]

SCRUB_LOCATIONS = [
    "Spool Swamp: Business Scrub",
    "Snake's Remains: Business Scrub",
    "Dancing Dragon Dungeon (1F): Business Scrub",
    "Samasa Desert: Business Scrub"
]

SUBROSIA_HIDDEN_DIGGING_SPOTS_LOCATIONS = [
    "Subrosia: Hot Bath Digging Spot",
    "Subrosia: Market Portal Digging Spot",
    "Subrosia: Hard-Working Subrosian Digging Spot",
    "Subrosia: Temple of Seasons Digging Spot",
    "Subrosia: Northern Volcanoes Digging Spot",
    "Subrosia: D8 Portal Digging Spot",
    "Subrosia: Western Volcanoes Digging Spot"
]

SECRETS = [
    "Horon Village: Clock Shop Secret",
    "Western Coast: Graveyard Secret",
    "Subrosia: Subrosian Secret",
    "Sunken City: Diver Secret",
    "Subrosia: Smith Secret",
    "Subrosia: Piratian Secret",
    "Subrosia: Temple Secret",
    "Natzu Region: Deku Secret",
    "Goron Mountain: Biggoron Secret",
    "Horon Village: Mayor Secret"
]

SAMASA_GATE_CODE = [2, 2, 1, 0, 0, 3, 3, 3]

AVERAGE_PRICE_PER_LOCATION = {
    "cheap": 50,
    "reasonable": 100,
    "expensive": 200,
    "outrageous": 350
}

VANILLA_SHOP_PRICES = {
    "horonShop1": 20,
    "horonShop2": 30,
    "horonShop3": 150,
    "memberShop1": 300,
    "memberShop2": 300,
    "memberShop3": 200,
    "advanceShop1": 100,
    "advanceShop2": 100,
    "advanceShop3": 100,
    "syrupShop1": 100,
    "syrupShop2": 300,
    "syrupShop3": 300,
    "subrosianMarket2": 30,
    "subrosianMarket3": 40,
    "subrosianMarket4": 50,
    "subrosianMarket5": 60,
    "spoolSwampScrub": 100,
    "samasaCaveScrub": 100,
    "d2Scrub": 30,
    "d4Scrub": 20,
}

ITEM_GROUPS = {
    "Small Keys": [
        "Small Key (Hero's Cave)",
        "Small Key (Gnarled Root Dungeon)",
        "Small Key (Snake's Remains)",
        "Small Key (Poison Moth's Lair)",
        "Small Key (Dancing Dragon Dungeon)",
        "Small Key (Unicorn's Cave)",
        "Small Key (Ancient Ruins)",
        "Small Key (Explorer's Crypt)",
        "Small Key (Sword & Shield Dungeon)",
    ],
    "Boss Keys": [
        "Boss Key (Gnarled Root Dungeon)",
        "Boss Key (Snake's Remains)",
        "Boss Key (Poison Moth's Lair)",
        "Boss Key (Dancing Dragon Dungeon)",
        "Boss Key (Unicorn's Cave)",
        "Boss Key (Ancient Ruins)",
        "Boss Key (Explorer's Crypt)",
        "Boss Key (Sword & Shield Dungeon)",
    ],
    "Compasses": [
        "Compass (Gnarled Root Dungeon)",
        "Compass (Snake's Remains)",
        "Compass (Poison Moth's Lair)",
        "Compass (Dancing Dragon Dungeon)",
        "Compass (Unicorn's Cave)",
        "Compass (Ancient Ruins)",
        "Compass (Explorer's Crypt)",
        "Compass (Sword & Shield Dungeon)",
    ],
    "Dungeon Maps": [
        "Dungeon Map (Gnarled Root Dungeon)",
        "Dungeon Map (Snake's Remains)",
        "Dungeon Map (Poison Moth's Lair)",
        "Dungeon Map (Dancing Dragon Dungeon)",
        "Dungeon Map (Unicorn's Cave)",
        "Dungeon Map (Ancient Ruins)",
        "Dungeon Map (Explorer's Crypt)",
        "Dungeon Map (Sword & Shield Dungeon)",
    ],
    "Master Keys": [
        "Master Key (Hero's Cave)",
        "Master Key (Gnarled Root Dungeon)",
        "Master Key (Snake's Remains)",
        "Master Key (Poison Moth's Lair)",
        "Master Key (Dancing Dragon Dungeon)",
        "Master Key (Unicorn's Cave)",
        "Master Key (Ancient Ruins)",
        "Master Key (Explorer's Crypt)",
        "Master Key (Sword & Shield Dungeon)",
    ],
    "Essences": [
        "Fertile Soil",
        "Gift of Time",
        "Bright Sun",
        "Soothing Rain",
        "Nurturing Warmth",
        "Blowing Wind",
        "Seed of Life",
        "Changing Seasons",
    ],
    "Jewels": [
        "Square Jewel",
        "Pyramid Jewel",
        "Round Jewel",
        "X-Shaped Jewel"
    ]
}

LOCATION_GROUPS = {
    "D0": [
        "Hero's Cave: Topmost Chest",
        "Hero's Cave: Final Chest",
        "Hero's Cave: Item in Basement Under Keese Room",
        "Hero's Cave: Alternative Entrance Chest",
    ],
    "D1": [
        "Gnarled Root Dungeon: Drop in Right Stalfos Room",
        "Gnarled Root Dungeon: Item in Basement",
        "Gnarled Root Dungeon: Chest in Block-pushing Room",
        "Gnarled Root Dungeon: Chest Near Railway",
        "Gnarled Root Dungeon: Chest in Floormaster Room",
        "Gnarled Root Dungeon: Chest Near Railway Lever",
        "Gnarled Root Dungeon: Chest in Left Stalfos Room",
        "Gnarled Root Dungeon: Hidden Chest Revealed by Button",
        "Gnarled Root Dungeon: Chest in Goriya Room",
        "Gnarled Root Dungeon: Boss Reward",
        "Gnarled Root Dungeon: Essence",
    ],
    "D2": [
        "Snake's Remains: Drop in Left Rope Room",
        "Snake's Remains: Chest in Distant Moblins Room",
        "Snake's Remains: Chest in Rollers Section",
        "Snake's Remains: Chest Left from Entrance",
        "Snake's Remains: Chest Behind Pots in Hardhat Room",
        "Snake's Remains: Chest in Right Rope Room",
        "Snake's Remains: Chest in Moving Blades Room",
        "Snake's Remains: Chest in Bomb Spiral Maze Room",
        "Snake's Remains: Chest on Terrace",
        "Snake's Remains: Business Scrub",
        "Snake's Remains: Boss Reward",
        "Snake's Remains: Essence",
    ],
    "D3": [
        "Poison Moth's Lair (B1F): Chest in Roller Room",
        "Poison Moth's Lair (1F): Chest in Mimics Room",
        "Poison Moth's Lair (1F): Chest Above East Trampoline",
        "Poison Moth's Lair (B1F): Chest in Watery Room",
        "Poison Moth's Lair (B1F): Chest on Quicksand Terrace",
        "Poison Moth's Lair (1F): Chest in Moldorm Room",
        "Poison Moth's Lair (1F): Chest Above West Trampoline & Owl",
        "Poison Moth's Lair (1F): Chest in Room Behind Hidden Cracked Wall",
        "Poison Moth's Lair (B1F): Chest in Moving Blade Room",
        "Poison Moth's Lair (1F): Boss Reward",
        "Poison Moth's Lair: Essence",
    ],
    "D4": [
        "Dancing Dragon Dungeon (2F): Pots on Buttons Puzzle Drop",
        "Dancing Dragon Dungeon (2F): Chest North of Entrance",
        "Dancing Dragon Dungeon (1F): Chest in Southwest Quadrant of Beamos Room",
        "Dancing Dragon Dungeon (1F): Dark Room Chest",
        "Dancing Dragon Dungeon (2F): Chest in Water Donut Room",
        "Dancing Dragon Dungeon (2F): Pool Drop",
        "Dancing Dragon Dungeon (1F): Chest on Small Terrace",
        "Dancing Dragon Dungeon (1F): Chest Revealed by Minecart Torches",
        "Dancing Dragon Dungeon (1F): Crumbling Room Chest",
        "Dancing Dragon Dungeon (1F): Eye Diving Spot Item",
        "Dancing Dragon Dungeon (B1F): Boss Reward",
        "Dancing Dragon Dungeon (1F): Business Scrub",
        "Dancing Dragon Dungeon: Essence",
    ],
    "D5": [
        "Unicorn's Cave: Right Cart Chest",
        "Unicorn's Cave: Chest Left from Entrance",
        "Unicorn's Cave: Magnet Gloves Chest",
        "Unicorn's Cave: Terrace Chest",
        "Unicorn's Cave: Armos Puzzle Room Chest",
        "Unicorn's Cave: Gibdo Room Chest",
        "Unicorn's Cave: Quicksand Spiral Chest",
        "Unicorn's Cave: Magnet Spinner Chest",
        "Unicorn's Cave: Chest in Right Half of Minecart Bay Room",
        "Unicorn's Cave: Treadmills Basement Item",
        "Unicorn's Cave: Boss Reward",
        "Unicorn's Cave: Essence",
    ],
    "D6": [
        "Ancient Ruins (1F): Magnet Ball Puzzle Drop",
        "Ancient Ruins (2F): Chest North of Main Spinner",
        "Ancient Ruins (3F): Armos Hall Chest",
        "Ancient Ruins (1F): Crystal Maze Room Chest",
        "Ancient Ruins (1F): Crumbling Ground Room Chest",
        "Ancient Ruins (2F): Chest in Gibdo Room",
        "Ancient Ruins (2F): Chest Between 4 Armos",
        "Ancient Ruins (1F): Chest in Beamos Room",
        "Ancient Ruins (1F): Chest on Terrace Left of Entrance",
        "Ancient Ruins (2F): Chest After Time Trial",
        "Ancient Ruins (2F): Chest on Red Terrace Before Vire",
        "Ancient Ruins (5F): Boss Reward",
        "Ancient Ruins: Essence",
    ],
    "D7": [
        "Explorer's Crypt (1F): Chest in Wizzrobe Room",
        "Explorer's Crypt (B1F): Chest in Fast Moving Platform Room",
        "Explorer's Crypt (B2F): Stair Maze Chest",
        "Explorer's Crypt (1F): Chest Right of Entrance",
        "Explorer's Crypt (1F): Chest Behind Cracked Wall",
        "Explorer's Crypt (B1F): Zol Button Drop",
        "Explorer's Crypt (B2F): Armos Puzzle Drop",
        "Explorer's Crypt (B1F): Chest Connected to Magnet Ball Button",
        "Explorer's Crypt (1F): Chest Above Trampoline Near 2nd Poe",
        "Explorer's Crypt (B2F): Drop in Room North of Stair Maze",
        "Explorer's Crypt (B1F): Chest in Jumping Stalfos Room",
        "Explorer's Crypt (B1F): Boss Reward",
        "Explorer's Crypt: Essence",
    ],
    "D8": [
        "Sword & Shield Dungeon (1F): Eye Drop Near Entrance",
        "Sword & Shield Dungeon (1F): Three Eyes Chest",
        "Sword & Shield Dungeon (1F): Drop in Hardhat & Magnet Ball Room",
        "Sword & Shield Dungeon (1F): U-Shaped Spiky Freezer Chest",
        "Sword & Shield Dungeon (B1F): Chest Right of Spinner",
        "Sword & Shield Dungeon (1F): Top Chest in Lava Bridge Room",
        "Sword & Shield Dungeon (1F): Bottom Chest in Lava Bridge Room",
        "Sword & Shield Dungeon (1F): Chest in Bombable Blocks Room",
        "Sword & Shield Dungeon (1F): Chest on Terrace After Pols Voice Room",
        "Sword & Shield Dungeon (1F): Ghost Armos Puzzle Drop",
        "Sword & Shield Dungeon (B1F): Southeast Lava Chest",
        "Sword & Shield Dungeon (B1F): Southwest Lava Chest",
        "Sword & Shield Dungeon (1F): Chest in Sparks & Pots Room",
        "Sword & Shield Dungeon (B1F): Boss Reward",
        "Sword & Shield Dungeon: Essence",
    ],
    "Trade Sequence": [
        "Horon Village: Dr. Left Reward",
        "North Horon: Malon Trade",
        "Maple Trade",
        "Holodrum Plain: Mrs. Ruul Trade",
        "Subrosia: Subrosian Chef Trade",
        "Goron Mountain: Biggoron Trade",
        "Sunken City: Ingo Trade",
        "North Horon: Yelling Old Man Trade",
        "Mt. Cucco: Talon Trade",
        "Sunken City: Syrup Trade",
        "Horon Village: Tick Tock Trade",
        "Eastern Suburbs: Guru-Guru Trade",
        "Mt. Cucco: Chest Behind Talon",
        "Sunken City: Syrup Shop #1",
        "Sunken City: Syrup Shop #2",
        "Sunken City: Syrup Shop #3",
    ]
}

GASHA_SPOT_REGIONS = [
    "impa gasha spot",
    "horon gasha spot",
    "suburbs gasha spot",
    "holodrum plain gasha spot",
    "holodrum plain island gasha spot",
    "spool swamp north gasha spot",
    "spool swamp south gasha spot",
    "sunken city gasha spot",
    "mt cucco gasha spot",
    "goron mountain left gasha spot",
    "goron mountain right gasha spot",
    "eyeglass lake gasha spot",
    "tarm ruins gasha spot",
    "western coast gasha spot",
    "samasa desert gasha spot",
    "onox gasha spot",
]

TREASURE_SPAWN_INSTANT = 0x00
TREASURE_SPAWN_POOF = 0x10
TREASURE_SPAWN_DROP = 0x20
TREASURE_SPAWN_CHEST = 0x30
TREASURE_SPAWN_DIVE = 0x40
TREASURE_SPAWN_DIG = 0x50
TREASURE_SPAWN_DELAYED_CHEST = 0x60

TREASURE_GRAB_INSTANT = 0x00
TREASURE_GRAB_ONE_HAND = 0x01
TREASURE_GRAB_TWO_HANDS = 0x02
TREASURE_GRAB_SPIN_SLASH = 0x03

TREASURE_SET_ITEM_ROOM_FLAG = 0x08

COLLECT_TOUCH = TREASURE_SPAWN_INSTANT | TREASURE_GRAB_TWO_HANDS | TREASURE_SET_ITEM_ROOM_FLAG
COLLECT_POOF = TREASURE_SPAWN_POOF | TREASURE_GRAB_TWO_HANDS | TREASURE_SET_ITEM_ROOM_FLAG
COLLECT_DROP = TREASURE_SPAWN_DROP | TREASURE_GRAB_ONE_HAND | TREASURE_SET_ITEM_ROOM_FLAG
COLLECT_CHEST = TREASURE_SPAWN_CHEST | TREASURE_SET_ITEM_ROOM_FLAG
COLLECT_DIVE = TREASURE_SPAWN_DIVE | TREASURE_GRAB_ONE_HAND | TREASURE_SET_ITEM_ROOM_FLAG
COLLECT_DIG = TREASURE_SPAWN_DIG | TREASURE_GRAB_TWO_HANDS | TREASURE_SET_ITEM_ROOM_FLAG
COLLECT_DELAYED_CHEST = TREASURE_SPAWN_DELAYED_CHEST | TREASURE_GRAB_INSTANT | TREASURE_SET_ITEM_ROOM_FLAG
COLLECT_SPINSLASH = TREASURE_SPAWN_INSTANT | TREASURE_GRAB_SPIN_SLASH
COLLECT_FAKE_POOF = TREASURE_SPAWN_POOF | TREASURE_GRAB_INSTANT | TREASURE_SET_ITEM_ROOM_FLAG
COLLECT_KEYDROP = TREASURE_SPAWN_DROP | TREASURE_GRAB_INSTANT | TREASURE_SET_ITEM_ROOM_FLAG
COLLECT_DIVER_ROOM = 0x80
COLLECT_POE_SKIP_ROOM = 0x81
COLLECT_MAKU_TREE = 0x82
COLLECT_D5_ARMOS_PUZZLE = 0x83
COLLECT_D4_SCRUB_ROOM = 0x84
