ZONE = {
    "ST0":  0,  # Final Stage: Bloodlines
    "ARE":  1,  # Colosseum
    "CAT":  2,  # Catacombs
    "CEN":  3,  # Center Cube
    "CHI":  4,  # Abandoned Mine
    "DAI":  5,  # Royal Chapel
    "DRE":  6,  # Nightmare
    "LIB":  7,  # Long Library
    "NO0":  8,  # Marble Gallery
    "NO1":  9,  # Outer Wall
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

# Title screen and cinematic area_flag = 0xeed8
zones = {
    ZONE["ST0"]:
        {
            "name": "Final Stage: Bloodlines",
            "pos": 0x0533efc8,
            "len": 271812,
            "items": 0x0a60,
            "area_flag": 0x189c
        },
    ZONE["ARE"]:
        {
            "name": "Colosseum",
            "pos": 0x043c2018,
            "len": 352636,
            "items": 0x0fe8,
            "area_flag": 0x8704,
            "loot_flag": 0x03bf06,
            "loot_size": 2
        },
    ZONE["CAT"]:
        {
            "name": "Catacombs",
            "pos": 0x0448f938,
            "len": 361920,
            "items": 0x174c,
            "area_flag": 0xb6d4,
            "loot_flag": 0x03befc,
            "loot_size": 3
        },
    ZONE["CEN"]:
        {
            "name": "Center Cube",
            "pos": 0x0455bff8,
            "len": 119916,
            "area_flag": 0x0e7c,
            "loot_flag": 0x03beec,
            "loot_size": 2
        },
    ZONE["CHI"]:
        {
            "name": "Abandoned Mine",
            "pos": 0x045e8ae8,
            "len": 193576,
            "items": 0x09e4,
            "area_flag": 0xdea4,
            "loot_flag": 0x03bf02,
            "loot_size": 2
        },
    ZONE["DAI"]:
        {
            "name": "Royal Chapel",
            "pos": 0x04675f08,
            "len": 373764,
            "items": 0x0ec0,
            "area_flag": 0x5fb8,
            "loot_flag": 0x03beff,
            "loot_size": 3
        },
    ZONE["DRE"]:
        {
            "name": "Nightmare",
            "pos": 0x05af2478,
            "len": 147456,
            "items": 0x1928,
            "area_flag": 0x6fc0,
            "loot_flag": 0x03bef4,
            "loot_size": 5
        },
    ZONE["LIB"]:
        {
            "name": "Long Library",
            "pos": 0x047a1ae8,
            "len": 348876,
            "items": 0x1a90,
            "area_flag": 0xf160,
            "loot_flag": 0x03befa,
            "loot_size": 2
        },
    ZONE["NO0"]:
        {
            "name": "Marble Gallery",
            "pos": 0x048f9a38,
            "len": 390540,
            "items": 0x1100,
            "area_flag": 0x37b8,
            "loot_flag": 0x03beec,
            "loot_size": 2
        },
    ZONE["NO1"]:
        {
            "name": "Outer Wall",
            "pos": 0x049d18b8,
            "len": 356452,
            "items": 0x1a2c,
            "area_flag": 0x1a20,
            "loot_flag": 0x03beee,
            "loot_size": 2
        },
    ZONE["NO2"]:
        {
            "name": "Olrox\'s Quarters",
            "pos": 0x04aa0438,
            "len": 327100,
            "items": 0x0fec,
            "area_flag": 0x8744,
            "loot_flag": 0x03bef0,
            "loot_size": 2
        },
    ZONE["NO3"]:
        {
            "name": "Castle Entrance",
            "pos": 0x04b665e8,
            "len": 359960,
            "items": 0x1c8c,
            "area_flag": 0x187c,
            "loot_flag": 0x03bef2,
            "loot_size": 2
        },
    ZONE["NP3"]:
        {
            "name": "Castle Entrance (after visiting Alchemy Laboratory)",
            "pos": 0x053f4708,
            "len": 341044,
            "items": 0x1618,
            "area_flag": 0x90ec,
            "loot_flag": 0x03bef2,
            "loot_size": 2
        },
    ZONE["NO4"]:
        {
            "name": "Underground Caverns",
            "pos": 0x04c307e8,
            "len": 391260,
            "items": 0x1928,
            "area_flag": 0xa620,
            "loot_flag": 0x03bef4,
            "loot_size": 5
        },
    ZONE["NZ0"]:
        {
            "name": "Alchemy Laboratory",
            "pos": 0x054b0c88,
            "len": 309120,
            "items": 0x13b0,
            "area_flag": 0x9504,
            "loot_flag": 0x03bf0b,
            "loot_size": 2
        },
    ZONE["NZ1"]:
        {
            "name": "Clock Tower",
            "pos": 0x055724b8,
            "len": 271168,
            "items": 0x111c,
            "area_flag": 0xc710,
            "loot_flag": 0x03bf0d,
            "loot_size": 2
        },
    ZONE["TOP"]:
        {
            "name": "Castle Keep",
            "pos": 0x0560e7b8,
            "len": 247132,
            "items": 0x0d10,
            "area_flag": 0xd660,
            "loot_flag": 0x03bf08,
            "loot_size": 3
        },
    ZONE["WRP"]:
        {
            "name": "Warp rooms",
            "pos": 0x05883408,
            "len": 83968,
            "area_flag": 0x8218
        },
    ZONE["RARE"]:
        {
            "name": "Reverse Colosseum",
            "pos": 0x057509e8,
            "len": 234384,
            "items": 0x0a3c,
            "area_flag": 0x6b70,
            "loot_flag": 0x03bf3b,
            "loot_size": 2
        },
    ZONE["RCAT"]:
        {
            "name": "Floating Catacombs",
            "pos": 0x04cfa0b8,
            "len": 278188,
            "items": 0x13c8,
            "area_flag": 0x3f80,
            "loot_flag": 0x03bf2b,
            "loot_size": 4
        },
    ZONE["RCEN"]:
        {
            "name": "Reverse Center Cube",
            "pos": 0x056bd9e8,
            "len": 186368,
            "area_flag": 0x049c
        },
    ZONE["RCHI"]:
        {
            "name": "Cave",
            "pos": 0x04da4968,
            "len": 174880,
            "items": 0x07cc,
            "area_flag": 0xac24,
            "loot_flag": 0x03bf33,
            "loot_size": 2
        },
    ZONE["RDAI"]:
        {
            "name": "Anti-Chapel",
            "pos": 0x04e31458,
            "len": 295736,
            "items": 0x0d2c,
            "area_flag": 0x465c,
            "loot_flag": 0x03bf2f,
            "loot_size": 3
        },
    ZONE["RLIB"]:
        {
            "name": "Forbidden Library",
            "pos": 0x04ee2218,
            "len": 201776,
            "items": 0x0bc8,
            "area_flag": 0x2b90,
            "loot_flag": 0x03bf27,
            "loot_size": 2
        },
    ZONE["RNO0"]:
        {
            "name": "Black Marble Gallery",
            "pos": 0x04f84a28,
            "len": 347020,
            "items": 0x0f8c,
            "area_flag": 0x7354,
            "loot_flag": 0x03bf13,
            "loot_size": 2
        },
    ZONE["RNO1"]:
        {
            "name": "Reverse Outer Wall",
            "pos": 0x0504f558,
            "len": 357020,
            "items": 0x0ae4,
            "area_flag": 0x9ccc,
            "loot_flag": 0x03bf17,
            "loot_size": 2
        },
    ZONE["RNO2"]:
        {
            "name": "Death Wing\'s Lair",
            "pos": 0x050f7948,
            "len": 313816,
            "items": 0x0d40,
            "area_flag": 0x6d20,
            "loot_flag": 0x03bf1b,
            "loot_size": 2
        },
    ZONE["RNO3"]:
        {
            "name": "Reverse Entrance",
            "pos": 0x051ac758,
            "len": 304428,
            "items": 0x0f10,
            "area_flag": 0x3ee0,
            "loot_flag": 0x03bf1f,
            "loot_size": 2
        },
    ZONE["RNO4"]:
        {
            "name": "Reverse Caverns",
            "pos": 0x0526a868,
            "len": 384020,
            "items": 0x1620,
            "area_flag": 0xa214,
            "loot_flag": 0x03bf23,
            "loot_size": 4
    },
    ZONE["RNZ0"]:
        {
            "name": "Necromancy Laboratory",
            "pos": 0x05902278,
            "len": 281512,
            "items": 0x0cc8,
            "area_flag": 0xcc34,
            "loot_flag": 0x03bf43,
            "loot_size": 2
    },
    ZONE["RNZ1"]:
        {
            "name": "Reverse Clock Tower",
            "pos": 0x059bb0d8,
            "len": 260960,
            "items": 0x0ec8,
            "rewards": 0x2570,
            "area_flag": 0xced0,
            "loot_flag": 0x03bf47,
            "loot_size": 2
    },
    ZONE["RTOP"]:
        {
            "name": "Reverse Castle Keep",
            "pos": 0x057df998,
            "len": 200988,
            "items": 0x07c8,
            "area_flag": 0x2524,
            "loot_flag": 0x03bf3f,
            "loot_size": 4
        },
    ZONE["RWRP"]:
        {
            "name": "Reverse Warp rooms",
            "pos": 0x05a6e358,
            "len": 92160,
            "area_flag": 0xa198
        },
    ZONE["BO0"]:
        {
            "name": "Olrox",
            "pos": 0x05fa9dc8,
            "len": 320948,
            "rewards": 0x24d4,
            "area_flag": 0xc10c,
            "loot_flag": 0x03bef0,
            "loot_size": 2
    },
    ZONE["BO1"]:
        {
            "name": "Granfaloon",
            "pos": 0x0606dab8,
            "len": 205756,
            "rewards": 0x1b98,
            "area_flag": 0x55d0,
            "loot_flag": 0x03befc,
            "loot_size": 3
        },
    ZONE["BO2"]:
        {
            "name": "Werewolf & Minotaur",
            "pos": 0x060fca68,
            "len": 223540,
            "rewards": 0x181c,
            "area_flag": 0x76a0,
            "loot_flag": 0x03bf06,
            "loot_size": 2
        },
    ZONE["BO3"]:
        {
            "name": "Scylla",
            "pos": 0x061a60b8,
            "len": 210224,
            "items": 0x108c,
            "rewards": 0x1c60,
            "area_flag": 0x6734,
            "loot_flag": 0x03bef4,
            "loot_size": 5
        },
    ZONE["BO4"]:
        {
            "name": "Doppleganger10",
            "pos": 0x06246d38,
            "len": 347704,
            "rewards": 0x42b0,
            "area_flag": 0x69ec,
            "loot_flag": 0x03beee,
            "loot_size": 2
        },
    ZONE["BO5"]:
        {
            "name": "Hippogryph",
            "pos": 0x06304e48,
            "len": 218672,
            "rewards": 0x18b8,
            "area_flag": 0x6be4,
            "loot_flag": 0x03beff,
            "loot_size": 3
        },
    ZONE["BO6"]:
        {
            "name": "Richter",
            "pos": 0x063aa448,
            "len": 333544,
            "rewards": 0x2f90,
            "area_flag": 0x9b84
        },
    ZONE["BO7"]:
        {
            "name": "Cerberus",
            "pos": 0x066b32f8,
            "len": 144480,
            "rewards": 0x1440,
            "area_flag": 0x6678,
            "loot_flag": 0x03bf02,
            "loot_size": 2
        },
    ZONE["RBO0"]:
        {
            "name": "Trio",
            "pos": 0x064705f8,
            "len": 160988,
            "rewards": 0x1988,
            "area_flag": 0xa094,
            "loot_flag": 0x03bf3b,
            "loot_size": 2
        },
    ZONE["RBO1"]:
        {
            "name": "Beezlebub",
            "pos": 0x06590a18,
            "len": 139104,
            "rewards": 0x1550,
            "area_flag": 0x5174,
            "loot_flag": 0x03bf43,
            "loot_size": 2
        },
    ZONE["RBO2"]:
        {
            "name": "Death",
            "pos": 0x06620c28,
            "len": 190792,
            "rewards": 0x1788,
            "area_flag": 0x1ab0,
            "loot_flag": 0x03bf33,
            "loot_size": 2
        },
    ZONE["RBO3"]:
        {
            "name": "Medusa",
            "pos": 0x067422a8,
            "len": 132656,
            "rewards": 0x12a8,
            "area_flag": 0x31c8,
            "loot_flag": 0x03bf2f,
            "loot_size": 3
        },
    ZONE["RBO4"]:
        {
            "name": "Creature",
            "pos": 0x067cfff8,
            "len": 154660,
            "rewards": 0x13b4,
            "area_flag": 0x8e3c,
            "loot_flag": 0x03bf17,
            "loot_size": 2
        },
    ZONE["RBO5"]:
        {
            "name": "Doppleganger40",
            "pos": 0x06861468,
            "len": 345096,
            "rewards": 0x4348,
            "area_flag": 0x5920,
            "loot_flag": 0x03bf23,
            "loot_size": 4
        },
    ZONE["RBO6"]:
        {
            "name": "Shaft/Dracula",
            "pos": 0x0692b668,
            "len": 213060,
            "area_flag": 0x54ec
        },
    ZONE["RBO7"]:
        {
            "name": "Akmodan II",
            "pos": 0x069d1598,
            "len": 142572,
            "rewards": 0x1300,
            "area_flag": 0x5f04,
            "loot_flag": 0x03bf1b,
            "loot_size": 2
        },
    ZONE["RBO8"]:
        {
            "name": "Galamoth",
            "pos": 0x06a5f2e8,
            "len": 161212,
            "rewards": 0x2334,
            "area_flag": 0x9dc8,
            "loot_flag": 0x03bf2b,
            "loot_size": 4
        }
}

ZONE_TO_NAME = {v: k for k, v in ZONE.items()}
AREA_FLAG_TO_ZONE = {}
for k, v in zones.items():
    v["zone"] = k
    AREA_FLAG_TO_ZONE[v["area_flag"]] = v


