from enum import Enum

devBaseUrl = "https://dev.sotn.io/"
defaultOptions = "p:safe"

optionsUrls = {
    "p:safe": "https://sotn.io/",
    "p:adventure": "https://a.sotn.io/",
    "p:casual": "https://c.sotn.io/",
    "p:speedrun": "https://s.sotn.io/",
    "p:glitch": "https://g.sotn.io/",
    "p:scavenger": "https://sc.sotn.io/",
    "p:empty-hand": "https://eh.sotn.io/",
    "p:og": "https://og.sotn.io/",
    "p:gem-farmer": "https://gf.sotn.io/",

    # Tournament mode URLs
    "tp:safe": "https://t.sotn.io/",
    "tp:adventure": "https://a.t.sotn.io/",
    "tp:casual": "https://c.t.sotn.io/",
    "tp:speedrun": "https://s.t.sotn.io/",
    "tp:glitch": "https://g.t.sotn.io/",
    "tp:scavenger": "https://sc.t.sotn.io/",
    "tp:empty-hand": "https://eh.t.sotn.io/",
    "tp:og": "https://og.t.sotn.io/",
    "tp:gem-farmer": "https://gf.t.sotn.io/",
}

TYPE = {
    "HEART": 0,
    "GOLD": 1,
    "SUBWEAPON": 2,
    "POWERUP": 3,
    "WEAPON1": 4,
    "WEAPON2": 5,
    "SHIELD": 6,
    "HELMET": 7,
    "ARMOR": 8,
    "CLOAK": 9,
    "ACCESSORY": 10,
    "USABLE": 11,
}

# List of type names for logging.
typeNames = [
    "HEART", "GOLD", "SUBWEAPON", "POWERUP", "WEAPON1", "WEAPON2", "SHIELD", "HELMET", "ARMOR", "CLOAK", "ACCESSORY",
    "USABLE"
]

ZONE = {
    "ST0":   0,  # Final Stage: Bloodlines
    "ARE":   1,  # Colosseum
    "CAT":   2,  # Catacombs
    "CEN":   3,  # Center Cube
    "CHI":   4,  # Abandoned Mine
    "DAI":   5,  # Royal Chapel
    "DRE":   6,  # Nightmare
    "LIB":   7,  # Long Library
    "NO0":   8,  # Marble Gallery
    "NO1":   9,  # Outer Wall
    "NO2":  10,  # Olrox's Quarters
    "NO3":  11,  # Castle Entrance
    "NP3":  12,  # Castle Entrance (after visiting Alchemy Laboratory)
    "NO4":  13,  # Underground Caverns
    "NZ0":  14,  # Alchemy Laboratory
    "NZ1":  15,  # Clock Tower
    "TOP":  16,  # Castle Keep
    "WRP":  17,  # Warp rooms
    "RARE": 18,  # Reverse Colosseum
    "RCAT": 19,  # Floating Catacombs
    "RCEN": 20,  # Reverse Center Cube
    "RCHI": 21,  # Cave
    "RDAI": 22,  # Anti-Chapel
    "RLIB": 23,  # Forbidden Library
    "RNO0": 24,  # Black Marble Gallery
    "RNO1": 25,  # Reverse Outer Wall
    "RNO2": 26,  # Death Wing's Lair
    "RNO3": 27,  # Reverse Entrance
    "RNO4": 28,  # Reverse Caverns
    "RNZ0": 29,  # Necromancy Laboratory
    "RNZ1": 30,  # Reverse Clock Tower
    "RTOP": 31,  # Reverse Castle Keep
    "RWRP": 32,  # Reverse Warp rooms
    "BO0":  33,  # Olrox
    "BO1":  34,  # Legion
    "BO2":  35,  # Werewolf & Minotaur
    "BO3":  36,  # Scylla
    "BO4":  37,  # Doppleganger10
    "BO5":  38,  # Hippogryph
    "BO6":  39,  # Richter
    "BO7":  40,  # Cerberus
    "RBO0": 41,  # Trio
    "RBO1": 42,  # Beezlebub
    "RBO2": 43,  # Death
    "RBO3": 44,  # Medusa
    "RBO4": 45,  # Creature
    "RBO5": 46,  # Doppleganger40
    "RBO6": 47,  # Shaft/Dracula
    "RBO7": 48,  # Akmodan II
    "RBO8": 49,  # Galamoth
}

# List of zone strings for logging.
zoneNames = [
    "ST0", "ARE", "CAT", "CEN", "CHI", "DAI", "DRE", "LIB", "NO0", "NO1", "NO2", "NO3", "NP3", "NO4", "NZ0", "NZ1",
    "TOP", "WRP", "RARE", "RCAT", "RCEN", "RCHI", "RDAI", "RLIB", "RNO0", "RNO1", "RNO2", "RNO3", "RNO4", "RNZ0",
    "RNZ1", "RTOP", "RWRP", "BO0", "BO1", "BO2", "BO3", "BO4", "BO5", "BO6", "BO7", "RBO0", "RBO1", "RBO2", "RBO3",
    "RBO4", "RBO5", "RBO6", "RBO7", "RBO8"
]

# Offsets in the bin of each zone file.
zones = {
        ZONE["ST0"]: {"pos": 0x0533efc8, "len": 271812, "items": 0x0a60},
        ZONE["ARE"]: {"pos": 0x043c2018, "len": 352636, "items": 0x0fe8},
        ZONE["CAT"]: {"pos": 0x0448f938, "len": 361920, "items": 0x174c},
        ZONE["CEN"]: {"pos": 0x0455bff8, "len": 119916},
        ZONE["CHI"]: {"pos": 0x045e8ae8, "len": 193576, "items": 0x09e4},
        ZONE["DAI"]: {"pos": 0x04675f08, "len": 373764, "items": 0x0ec0},
        ZONE["DRE"]: {"pos": 0x05af2478, "len": 147456},
        ZONE["LIB"]: {"pos": 0x047a1ae8, "len": 348876, "items": 0x1a90},
        ZONE["NO0"]: {"pos": 0x048f9a38, "len": 390540, "items": 0x1100},
        ZONE["NO1"]: {"pos": 0x049d18b8, "len": 356452, "items": 0x1a2c},
        ZONE["NO2"]: {"pos": 0x04aa0438, "len": 327100, "items": 0x0fec},
        ZONE["NO3"]: {"pos": 0x04b665e8, "len": 359960, "items": 0x1c8c},
        ZONE["NP3"]: {"pos": 0x053f4708, "len": 341044, "items": 0x1618},
        ZONE["NO4"]: {"pos": 0x04c307e8, "len": 391260, "items": 0x1928},
        ZONE["NZ0"]: {"pos": 0x054b0c88, "len": 309120, "items": 0x13b0},
        ZONE["NZ1"]: {"pos": 0x055724b8, "len": 271168, "items": 0x111c},
        ZONE["TOP"]: {"pos": 0x0560e7b8, "len": 247132, "items": 0x0d10},
        ZONE["WRP"]: {"pos": 0x05883408, "len": 83968},
        ZONE["RARE"]: {"pos": 0x057509e8, "len": 234384, "items": 0x0a3c},
        ZONE["RCAT"]: {"pos": 0x04cfa0b8, "len": 278188, "items": 0x13c8},
        ZONE["RCEN"]: {"pos": 0x056bd9e8, "len": 186368},
        ZONE["RCHI"]: {"pos": 0x04da4968, "len": 174880, "items": 0x07cc},
        ZONE["RDAI"]: {"pos": 0x04e31458, "len": 295736, "items": 0x0d2c},
        ZONE["RLIB"]: {"pos": 0x04ee2218, "len": 201776, "items": 0x0bc8},
        ZONE["RNO0"]: {"pos": 0x04f84a28, "len": 347020, "items": 0x0f8c},
        ZONE["RNO1"]: {"pos": 0x0504f558, "len": 357020, "items": 0x0ae4},
        ZONE["RNO2"]: {"pos": 0x050f7948, "len": 313816, "items": 0x0d40},
        ZONE["RNO3"]: {"pos": 0x051ac758, "len": 304428, "items": 0x0f10},
        ZONE["RNO4"]: {"pos": 0x0526a868, "len": 384020, "items": 0x1620},
        ZONE["RNZ0"]: {"pos": 0x05902278, "len": 281512, "items": 0x0cc8},
        ZONE["RNZ1"]: {"pos": 0x059bb0d8, "len": 260960, "items": 0x0ec8, "rewards": 0x2570},
        ZONE["RTOP"]: {"pos": 0x057df998, "len": 200988, "items": 0x07c8},
        ZONE["RWRP"]: {"pos": 0x05a6e358, "len": 92160},
        ZONE["BO0"]: {"pos": 0x05fa9dc8, "len": 320948, "rewards": 0x24d4},
        ZONE["BO1"]: {"pos": 0x0606dab8, "len": 205756, "rewards": 0x1b98},
        ZONE["BO2"]: {"pos": 0x060fca68, "len": 223540, "rewards": 0x181c},
        ZONE["BO3"]: {"pos": 0x061a60b8, "len": 210224, "items": 0x108c, "rewards": 0x1c60},
        ZONE["BO4"]: {"pos": 0x06246d38, "len": 347704, "rewards": 0x42b0},
        ZONE["BO5"]: {"pos": 0x06304e48, "len": 218672, "rewards": 0x18b8},
        ZONE["BO6"]: {"pos": 0x063aa448, "len": 333544, "rewards": 0x2f90},
        ZONE["BO7"]: {"pos": 0x066b32f8, "len": 144480, "rewards": 0x1440},
        ZONE["RBO0"]: {"pos": 0x064705f8, "len": 160988, "rewards": 0x1998},
        ZONE["RBO1"]: {"pos": 0x06590a18, "len": 139104, "rewards": 0x1550},
        ZONE["RBO2"]: {"pos": 0x06620c28, "len": 190792, "rewards": 0x1788},
        ZONE["RBO3"]: {"pos": 0x067422a8, "len": 132656, "rewards": 0x12a8},
        ZONE["RBO4"]: {"pos": 0x067cfff8, "len": 154660, "rewards": 0x13b4},
        ZONE["RBO5"]: {"pos": 0x06861468, "len": 345096, "rewards": 0x4348},
        ZONE["RBO6"]: {"pos": 0x0692b668, "len": 213060},
        ZONE["RBO7"]: {"pos": 0x069d1598, "len": 142572, "rewards": 0x1300},
        ZONE["RBO8"]: {"pos": 0x06a5f2e8, "len": 161212, "rewards": 0x2334}
    }

exe = {"pos": 0x0abb28, "len": 703272}
enemyListOff = 0xe90
enemyListLen = 292
enemyDataOff = 0x8900
enemyDataLen = 0x28
handEquipmentListOff = 0x4b04
handEquipmentListLen = 169
armorListOff = 0x7718
armorListLen = 26
helmetListOff = 0x7a58
helmetListLen = 22
cloakListOff = 0x7d18
cloakListLen = 9
accessoryListOff = 0x7e38
accessoryListLen = 33

RELIC = {
    "SOUL_OF_BAT": "B",
    "FIRE_OF_BAT": "f",
    "ECHO_OF_BAT": "E",
    "FORCE_OF_ECHO": "e",
    "SOUL_OF_WOLF": "W",
    "POWER_OF_WOLF": "p",
    "SKILL_OF_WOLF": "s",
    "FORM_OF_MIST": "M",
    "POWER_OF_MIST": "P",
    "GAS_CLOUD": "c",
    "CUBE_OF_ZOE": "z",
    "SPIRIT_ORB": "o",
    "GRAVITY_BOOTS": "V",
    "LEAP_STONE": "L",
    "HOLY_SYMBOL": "y",
    "FAERIE_SCROLL": "l",
    "JEWEL_OF_OPEN": "J",
    "MERMAN_STATUE": "U",
    "BAT_CARD": "b",
    "GHOST_CARD": "g",
    "FAERIE_CARD": "a",
    "DEMON_CARD": "d",
    "SWORD_CARD": "w",
    "SPRITE_CARD": "t",
    "NOSEDEVIL_CARD": "n",
    "HEART_OF_VLAD": "A",
    "TOOTH_OF_VLAD": "T",
    "RIB_OF_VLAD": "R",
    "RING_OF_VLAD": "N",
    "EYE_OF_VLAD": "I",
    "GOLD_RING": "G",
    "SILVER_RING": "S",
    "SPIKE_BREAKER": "K",
    "HOLY_GLASSES": "H",
    "THRUST_SWORD": "D",
}

tileIdOffset = 0x80

# This is applied to helmet, armor, cloak, and other ids that are sold in
# the librarian's shop menu or are in an equipment slot.
equipIdOffset = -0xa9

# This is applied to equipment ids to get the inventory slot it occupies.
equipmentInvIdOffset = 0x798a

SLOT = {
    "RIGHT_HAND": "r",
    "LEFT_HAND": "l",
    "HEAD": "h",
    "BODY": "b",
    "CLOAK": "c",
    "OTHER": "o",
    "OTHER2": "o2",
    "AXEARMOR": "a",
    "LUCK_MODE": "x",
}

slots = {
    "r": 0x097c00,
    "l": 0x097c04,
    "h": 0x097c08,
    "b": 0x097c0c,
    "c": 0x097c10,
    "o": 0x097c14,
    "o2": 0x097c18,
}

EXTENSION = {
    "GUARDED": "guarded",
    "EQUIPMENT": "equipment",
    "SPREAD": "spread",
    "TOURIST": "tourist",
    "WANDERER": "wanderer",
}

defaultExtension = EXTENSION["GUARDED"]

LOCATION = {
    "CRYSTAL_CLOAK": "Crystal cloak",
    "MORMEGIL": "Mormegil",
    "DARK_BLADE": "Dark Blade",
    "RING_OF_ARCANA": "Ring of Arcana",
    "TRIO": "Trio",
    "HOLY_MAIL": "Holy mail",
    "JEWEL_SWORD": "Jewel sword",
    "BASILARD": "Basilard",
    "SUNGLASSES": "Sunglasses",
    "CLOTH_CAPE": "Cloth cape",
    "MYSTIC_PENDANT": "Mystic pendant",
    "ANKH_OF_LIFE": "Ankh of Life",
    "MORNING_STAR": "Morningstar",
    "GOGGLES": "Goggles",
    "SILVER_PLATE": "Silver plate",
    "CUTLASS": "Cutlass",
    "PLATINUM_MAIL": "Platinum mail",
    "FALCHION": "Falchion",
    "GOLD_PLATE": "Gold plate",
    "BEKATOWA": "Bekatowa",
    "GLADIUS": "Gladius",
    "JEWEL_KNUCKLES": "Jewel knuckles",
    "HOLY_ROD": "Holy rod",
    "LIBRARY_ONYX": "Library Onyx",
    "BRONZE_CUIRASS": "Bronze cuirass",
    "ALUCART_SWORD": "Alucart sword",
    "BROADSWORD": "Broadsword",
    "ESTOC": "Estoc",
    "OLROX_GARNET": "Olrox Garnet",
    "BLOOD_CLOAK": "Blood cloak",
    "SHIELD_ROD": "Shield rod",
    "KNIGHT_SHIELD": "Knight shield",
    "HOLY_SWORD": "Holy sword",
    "BANDANNA": "Bandanna",
    "SECRET_BOOTS": "Secret boots",
    "NUNCHAKU": "Nunchaku",
    "KNUCKLE_DUSTER": "Knuckle duster",
    "CAVERNS_ONYX": "Caverns Onyx",
    "COMBAT_KNIFE": "Combat knife",
    "RING_OF_ARES": "Ring of Ares",
    "BLOODSTONE": "Bloodstone",
    "ICEBRAND": "Icebrand",
    "WALK_ARMOR": "Walk armor",
    "BERYL_CIRCLET": "Beryl circlet",
    "TALISMAN": "Talisman",
    "KATANA": "Katana",
    "GODDESS_SHIELD": "Goddess shield",
    "TWILIGHT_CLOAK": "Twilight cloak",
    "TALWAR": "Talwar",
    "SWORD_OF_DAWN": "Sword of Dawn",
    "BASTARD_SWORD": "Bastard sword",
    "ROYAL_CLOAK": "Royal cloak",
    "LIGHTNING_MAIL": "Lightning mail",
    "MOON_ROD": "Moon rod",
    "SUNSTONE": "Sunstone",
    "LUMINUS": "Luminus",
    "DRAGON_HELM": "Dragon helm",
    "SHOTEL": "Shotel",
    "STAUROLITE": "Staurolite",
    "BADELAIRE": "Badelaire",
    "FORBIDDEN_LIBRARY_OPAL": "Forbidden Library Opal",
    "REVERSE_CAVERNS_DIAMOND": "Reverse Caverns Diamond",
    "REVERSE_CAVERNS_OPAL": "Reverse Caverns Opal",
    "REVERSE_CAVERNS_GARNET": "Reverse Caverns Garnet",
    "OSAFUNE_KATANA": "Osafune katana",
    "ALUCARD_SHIELD": "Alucard shield",
    "ALUCARD_SWORD": "Alucard sword",
    "NECKLACE_OF_J": "Necklace of J",
    "FLOATING_CATACOMBS_DIAMOND": "Floating Catacombs Diamond",
    "SWORD_OF_HADOR": "Sword of Hador",
    "ALUCARD_MAIL": "Alucard mail",
    "GRAM": "Gram",
    "FURY_PLATE": "Fury plate",
    "CONFESSIONAL": "Confessional",
    "COLOSSEUM_GREEN_TEA": "Colosseum Green tea",
    "CLOCK_TOWER_CLOAKED_KNIGHT": "Clock Tower Cloaked knight",
    "TELESCOPE": "Telescope",
    "WATERFALL_CAVE": "Waterfall Cave",
    "FLOATING_CATACOMBS_ELIXIR": "Floating Catacombs Elixir",
    "REVERSE_ENTRANCE_ANTIVENOM": "Reverse Entrance Antivenom",
    "REVERSE_FORBIDDEN_ROUTE": "Reverse Forbidden Route",
    "CAVE_LIFE_APPLE": "Cave Life apple",
    "REVERSE_COLOSSEUM_ZIRCON": "Reverse Colosseum Zircon",
    "BLACK_MARBLE_GALLERY_VAT": "Black Marble Gallery Vat",
    "BLACK_MARBLE_MEAL_TICKET": "Black Marble Meal Ticket",
    "REVERSE_KEEP_HIGH_POTION": "Reverse Keep High Potion",
}

GLOBAL_DROP = "Global"
globalDropsCount = 32

WORKER_ACTION = {
    "STATS": 1,
    "RELICS": 2,
    "ITEMS": 3,
    "FINALIZE": 4,
}

MUSIC = {
    "LOST_PAINTING": 0x01,
    "CURSE_ZONE": 0x03,
    "REQUIEM_FOR_THE_GODS": 0x05,
    "RAINBOW_CEMETARY": 0x07,
    "WOOD_CARVING_PARTITA": 0x09,
    "CRYSTAL_TEARDROPS": 0x0b,
    "MARBLE_GALLERY": 0x0d,
    "DRACULAS_CASTLE": 0x0f,
    "THE_TRAGIC_PRINCE": 0x11,
    "TOWER_OF_MIST": 0x13,
    "DOOR_OF_HOLY_SPIRITS": 0x15,
    "DANCE_OF_PALES": 0x17,
    "ABANDONED_PIT": 0x19,
    "HEAVENLY_DOORWAY": 0x1b,
    "FESTIVAL_OF_SERVANTS": 0x1d,
    "WANDERING_GHOSTS": 0x23,
    "THE_DOOR_TO_THE_ABYSS": 0x25,
    "DANCE_OF_GOLD": 0x2e,
    "ENCHANTED_BANQUET": 0x30,
    "DEATH_BALLAD": 0x34,
    "FINAL_TOCCATA": 0x38,
    "NOCTURNE": 0x3f,
}

HAND_TYPE = {
    "SHORT_SWORD": 0x00,
    "SWORD": 0x01,
    "THROWING_SWORD": 0x02,
    "FIST": 0x03,
    "CLUB": 0x04,
    "TWO_HANDED_SWORD": 0x05,
    "FOOD": 0x06,
    "DAMAGE_CONSUMABLE": 0x07,
    "PROJECTILE_CONSUMABLE": 0x08,
    "SHIELD": 0x09,
    "OTHER": 0x0a,
}


handTypeNames = [
    "SHORT_SWORD", "SWORD", "THROWING_SWORD", "FIST", "BLUNT_WEAPON", "TWO_HANDED_SWORD", "FOOD", "DAMAGE_CONSUMABLE",
    "PROJECTILE_CONSUMABLE", "SHIELD", "OTHER"
]

faerieScrollForceAddresses = [
    0x04403938, 0x044d4948, 0x045702c0, 0x0460bcb8, 0x046c70ec, 0x047eadd4, 0x04947e2c, 0x04a1da54, 0x04ae1d98,
    0x04bb25e0, 0x04c86ae4, 0x04d367a4, 0x04dc4068, 0x04e6e350, 0x04f0ab84, 0x04fc4c08, 0x050800a0, 0x051373c4,
    0x051e8da4, 0x052c0628, 0x0537889c, 0x05436b40, 0x054f34d8, 0x055a6164, 0x05643614, 0x056e3670, 0x0577dcb4,
    0x05807b68, 0x0588d50c, 0x05936448, 0x059ef674, 0x05a7a89c, 0x05b0d6c4, 0x05fef940, 0x06099584, 0x0612aac4,
    0x061d2f48, 0x06286480, 0x06332188, 0x063dae48, 0x0648f038, 0x06518314, 0x065a9958, 0x06648254, 0x066cdacc,
    0x06758d7c, 0x067ed580, 0x0689f884, 0x06956f20, 0x069eb4c8, 0x06a7da5c
]

characterMap = {
    ",": [0x81, 0x43],
    ".": [0x81, 0x44],
    ":": [0x81, 0x46],
    ";": [0x81, 0x47],
    "?": [0x81, 0x48],
    "!": [0x81, 0x49],
    "`": [0x81, 0x4d],
    "\"": [0x81, 0x4e],
    "^": [0x81, 0x4f],
    "_": [0x81, 0x51],
    "~": [0x81, 0x60],
    "\\": [0x81, 0x66],
    "(": [0x81, 0x69],
    ")": [0x81, 0x6a],
    "[": [0x81, 0x6d],
    "]": [0x81, 0x6e],
    "{": [0x81, 0x6f],
    "}": [0x81, 0x70],
    "+": [0x81, 0x7b],
    "-": [0x81, 0x7c],
    "%": [0x81, 0x93],
    "0": [0x82, 0x4f],
    "1": [0x82, 0x50],
    "2": [0x82, 0x51],
    "3": [0x82, 0x52],
    "4": [0x82, 0x53],
    "5": [0x82, 0x54],
    "6": [0x82, 0x55],
    "7": [0x82, 0x56],
    "8": [0x82, 0x57],
    "9": [0x82, 0x58],
}

adjectivesNormal = [
    "Invincible", "Burning", "Preposterous", "Grumpy", "SuperDuper", "Boring", "Sorry", "Hot", "Used", "Afraid",
    "Tall", "Large", "Terrible", "Distorted", "Curious", "Pregnant", "Useful", "Decent", "Enhanced", "Asleep",
    "Cultural", "Indistinguishable", "Exciting", "Healthy", "Logical", "Popular", "Overdriven", "Unhappy", "Known",
    "Critical", "Ugly", "Legal", "Powerful", "Hungry", "Angry", "Aware", "Scared", "Tiny", "Wooden", "Informal",
    "Happy", "Strict", "Obvious", "Federal", "Nice", "Every", "Relevant", "Friendly", "Distinct", "Ancient", "Unlikely",
    "Odd", "Weak", "Suitable", "Severe", "Capable", "Unfair", "Lonely", "Entire", "Similar", "Obscure", "Redundant",
    "Intelligent", "Yellow", "Sinister", "Spectacular", "Mint", "Fuzzy", "Chipped", "Squishy", "Corrupted",
    "Predictable", "Super",  "Sharp", "Junior", "Riveting", "Perfect", "EX", "Supreme", "Dark", "Volcanic", "Colorful",
    "Flimsy", "Silly", "Shin", "Denjin", "Surprising", "Optimal", "Suboptimal", "Ultra", "Counter", "Cowardly", "Hairy",
    "Rage", "Vegan", "Epic", "Turbo", "Undead", "Chill", "True", "Moody", "Frozen", "Flawless", "Pointless", "Shinku",
    "Mesatsu", "Terran", "Protoss", "Zerg", "Orcish", "Elvish", "Tarot", "Bohemian", "Arcane", "Mystic",  "Light",
    "Red", "Crimson", "Garnet", "Ruby", "Blue", "Azure", "Lapis", "Cobalt", "Sapphire", "White", "Pearl", "Ivory",
    "Crystal", "Diamond", "Topaz", "Amber", "Jade", "Obsidian", "Emerald", "Fine", "Strong", "Grand", "Valiant",
    "Glorious", "Blessed", "Saintly", "Awesome", "Holy", "Godly", "Bronze", "Iron", "Steel", "Silver", "Gold",
    "Platinum", "Mithril", "Meteoric", "Weird", "Strange", "Jagged", "Deadly", "Heavy", "Vicious", "Brutal", "Massive",
    "Savage", "Ruthless", "Merciless", "Khajit", "Argonian", "Redguard", "Breton", "Nord", "Dunmer", "Altmer", "Falmer",
    "Bosmer", "Plentiful", "Bountiful", "Angels", "Arch-Angels", "Final", "Mandalorian", "Prototype", "Sith", "Jedi",
    "Battle", "Autobot", "Decepticon", "Primal", "Whovian", "Golgari", "Azorius", "Boros", "Simic", "Dimir", "Selesnya",
    "Gruul", "Orzhov", "Rakdos", "Izzet", "Infinite", "Eldritch", "Bucolic", "Serendipitous", "Angsty", "Death",
    "Chase", "Urzas", "Dank", "Borg", "Romulan", "Klingon", "Cardassian", "Jaffa", "Goauld", "Asgardian", "Vulcan",
    "Spark", "Armored", "Launch", "Boomer", "Sting", "Storm", "Flame", "Wheel", "Bubble", "Morph", "Magna", "Overdrive",
    "Wire", "Blast", "Blizzard", "Toxic", "Tunnel", "Volt", "Crush", "Neon", "Gravity", "Web", "Split", "Cyber",
    "Magma", "Frost", "Jet", "Slash", "Crescent", "Tidal", "Shining", "Spiral", "Burn", "Spike", "Ground", "Blaze",
    "Rainy", "Metal", "Shield", "Infinity", "Commander", "Soldier", "Tornado", "Splash", "Ride", "Snipe", "Wind",
    "Vanishing", "Bamboo", "Optic", "Earthrock", "Gigabolt", "Avalanche", "Green", "Bridge", "Jungle", "Labyrinth",
    "Scrap", "Sky", "Special", "Metropolis", "Chemical", "Aquatic", "Casino", "Hill", "Oil", "Wing", "Wood", "Genocide",
    "Rock", "Sand", "Egg", "Proto", "Boss", "Hidden", "Angel", "Hydrocity", "Marble", "Carnival", "Icecap", "Mushroom",
    "Flying", "Sandopolis", "Lava", "The", "Balloon", "Chrome", "Desert", "Endless", "Bob-Omb", "Whomps", "JollyRoger",
    "CoolCool", "BigBoos", "Hazy", "Lethal", "ShiftingSand", "DireDire", "Snowmans", "WetDry", "TallTall", "Sacred",
    "TinyHuge", "TickTock", "Rainbow"
    ]

nounsNormal = [
    "Axelord", "Fleaman", "Nutella", "Saiyan", "Turtle", "Ranger", "Whip", "Octopus", "Slayer", "Vampire", "Zombie",
    "Skeleton", "Zerg", "Terran", "Protoss", "SCP", "Spark", "Steel", "Rage", "Connection", "Radiator", "Alien", "Dog",
    "Cat", "Setup", "Shoryuken", "Fireball", "Fist", "Dolphin", "Force", "Star", "Bug", "Beard", "Moustache", "Junior",
    "Planet", "Mist", "Wolf", "Bat", "Armor", "Axe", "Sword", "Boss", "Seed", "Cable", "Soup", "Poem", "Trebuchet",
    "Cheek", "Girl", "Spawn", "Fortune", "Revolver", "Drawing", "Grocery", "Leader", "Setting", "Security", "Office",
    "Agency", "User", "Resource", "Policy", "Love", "Extent", "Week", "Employee", "Climate", "Unit", "Union", "Person",
    "Painting", "Analysis", "Night", "City", "Church", "Surgery", "Police", "Witch", "Finding", "Viper", "Member",
    "Patience", "Computer", "Movie", "Argument", "Virus", "Courage", "Debt", "Engine", "Tooth", "Wife", "Employer",
    "Gate", "Accident", "Warning", "Dinner", "Avocado", "Banana", "Cherry", "Celery", "Proton", "Neutron", "Apple",
    "Button", "Monitor", "Controller", "Potential", "Hadoken", "Justice", "Mew", "Cannon", "TatsumakiSenpukyaku",
    "Gohado", "Orc", "Elf", "Ent", "Spider", "Death", "Demon", "Goblin", "Wurm", "Spirit", "Horror", "God", "Devil",
    "Minotaur", "Blast", "Bus", "Horse", "Moon", "Executioner", "Assassin", "Druid", "Barbarian", "Sorceress", "Wizard",
    "Necromancer", "Paladin", "Amazon", "Crusader", "Rogue", "Warrior", "Sorcerer", "Angel", "Nephalim", "Evil",
    "Lunch", "Breakfast", "Artifact", "Enchantment", "Creature", "Planeswalker", "Flux", "Tardis", "Companion",
    "Hour", "Minute", "Second", "Day", "Month", "Year", "Talisman", "Curio", "Bangle", "Broach", "Spell", "Sorcery",
    "Mummy", "Werewolf", "Werebear", "Werebat", "Knight", "Soldier", "King", "Queen", "Rebel", "Mercenary", "Error",
    "Object", "Prime", "Sage", "Butcher", "Echo", "Leyline", "Bahamut", "Cactuar", "Tonberry", "Chocobo", "Moogle",
    "Moomba", "Surge", "Eidolon", "Esper", "Leviathan", "Phoenix", "Pikachu", "Charizard", "Xenomorph", "Android",
    "Jedi", "Sith", "Maverick", "Mandalorian", "Grail", "Card", "Slime", "Mewtwo", "Fireflower", "Mushroom", "Starman",
    "Mario", "Peach", "Toad", "Luigi", "Bowser", "Mask", "Ganon", "Materia", "Fairy", "Battletoad",
    "Kombat", "Portal", "CompanionCube", "Cake", "Dervish", "Kraken", "Meme", "Jaffa", "Goauld", "Stargate",
    "Zatniktel", "Q", "Cardassian", "Klingon", "Romulan", "Vulcan", "Penguin", "Mandrill", "Armadillo", "Kuwanger",
    "Chameleon", "Eagle", "Mammoth", "Gator", "Crab", "Stag", "Moth", "Centipede", "Snail", "Ostrich", "Sponge", "Mac",
    "Hornet", "Buffalo", "Seahorse", "Rhino", "Catfish", "Crawfish", "Tiger", "Beetle", "Peacock", "Owl", "Dragoon",
    "Walrus", "Stingray", "Beast", "Grizzly", "Whale", "Firefly", "Necrobat", "Pegasus", "Dinorex", "Rosered",
    "Yammark", "Scaravich", "Heatnix", "Wolfgang", "Turtoid", "SharkPlayer", "Sheldon", "Mijinion", "Stonekong",
    "Tonion", "Warfly", "Hyenard", "Boarski", "Anteator", "Crowrang", "Gungaroo", "Pandamonium", "Sunflower", "Mantis",
    "Antonion", "Trilobyte", "ManOWar", "Yeti", "Rooster", "Zone", "Hill", "Plant", "Ruin", "Top", "Cave", "Ocean",
    "Brain", "Base", "Chase", "Fortress", "Egg", "Heart", "World", "Shower", "Gauntlet", "Palace", "Attack", "Island",
    "Garden", "Battery", "Reef", "Sanctuary", "Doomsday", "Park", "Gadget", "Mine", "Land", "Battlefield", "Bay",
    "Mountain", "Haunt", "MazeCave", "LavaLand", "Docks", "Clock", "Ride", "Goomba", "KoopaTroopa", "CharginChuck",
    "Spike", "Boo", "Rex", "ChainChomp"
    ]

adjectivesHalloween = [
    "Scary", "Terrifying", "Spooky", "Eerie", "Horrendous", "Abyssal", "Spinechilling", "Bloodcurdling", "Chilling",
    "Horrid", "Horrific", "Horrifying", "Dire", "Dreadful", "Fearsome", "Ghastly", "Disturbing", "Unnerving", "Creepy",
    "Nightmarish", "Gruesome", "Grotesque", "Hideous", "Petrifying", "Undead", "Vile", "Evil", "Unsettling",
    "Incorporeal", "Ephemeral", "Haunting", "Frightening", "Graven", "Abhorrent", "Surreal", "Insidious", "Sordid",
    "Malicious", "Unspeakable", "Defiled", "Unscrupulous", "Sinister", "Malevolent", "Haunted", "Gory", "Decapitated",
    "Disemboweled", "Deceased", "Fanged", "Paranormal"
    ]

nounsHalloween = [
    "Skeleton", "Ghost", "SCP", "Vampire", "Ghoul", "Werewolf", "Zombie", "Phantom", "Monster", "Lich", "Bulette",
    "Beholder", "Hag", "Witch", "MindFlayer", "Devil", "Demon", "Fiend", "Alien", "Lich", "Gargoyle", "Abomination",
    "Construct", "Wendigo", "Wight", "Goblin", "Crone", "Spectre", "Banshee", "Wraith", "Arachnid", "Monstrosity",
    "Yokai", "Spirit", "Wretch", "Fiend", "Oni", "Kitsune", "Chupacabra", "Basilisk", "Horror", "Nightmare",
    "Cockatrice", "Kraken", "Djinn", "Ogre", "Gorgon", "Warlock", "Ooze", "Shedim", "Asura", "Daeva", "Gallas"
    ]

adjectivesHolidays = [
    "Snowy", "Merry", "Happy", "Jolly", "Cozy", "Festive", "Relaxing", "Cheery", "Warm", "Sparkly", "Wintry", "Joyful",
    "Snow", "Giving", "Celebratory", "Joyous", "Yule", "Frosty", "Jingly",
    ]

digest = "ce01203a9df93e001b88ef4c350889c19f11ffba89d20f214bdd8dec0b2d8d7c"
