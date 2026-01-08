from ..data.Constants import *

CAVE_DATA = [
    0x3ec8,  # 00
    0x3e89,  # 01
    [  # 02
        [0x023d, 0x02a3],  # fileSelectMode5
        0x35bb  # End of bank
    ],
    0x3dd7,  # 03
    [  # 04
        [0x2776, 0x280f],  # roomTileChangesAfterLoad for trees, which are reimplemented
        0x3e12  # End of bank
    ],
    0x3e2d,  # 05
    0x3864,  # 06 - 128 bytes reserved for sprite expansion w/ web patcher
    0x3900,  # 07
    [  # 08
        [0x2395, 0x26fd],  # Bipin & Blossom child mechanic
        0x3fc0  # End of bank
    ],
    0x3f4e,  # 09
    0x3bf9,  # 0a
    [  # 0b
        [0x34ac, 0x34ee],  # Impa intro script
        [0x39b4, 0x39e9],  # Twinrova cutscene 1
        [0x39f5, 0x3a29],  # Twinrova cutscene 2
        0x3f6d  # End of bank
    ],
    0x3ea1,  # 0c
    0x3b82,  # 0d
    0x3ef3,  # 0e
    0x3f9d,  # 0f
    0x3bee,  # 10
    0x3eb0,  # 11
    0x3c8f,  # 12
    0x3bd2,  # 13
    0x2fc9,  # 14 - ton of free space here
    0x392d,  # 15
    0x3a07,  # 16
    0x3f3a,  # 17
    0x3e6d,  # 18
    0x36e1,  # 19
    0x30f0,  # 1a - here too
    0x3c40,  # 1b
    0x4000,  # 1c
    0x4000,  # 1d
    0x4000,  # 1e
    0x4000,  # 1f
    0x4000,  # 20
    0x4000,  # 21
    0x4000,  # 22
    0x4000,  # 23
    0x4000,  # 24
    0x4000,  # 25
    0x4000,  # 26
    0x4000,  # 27
    0x4000,  # 28
    0x4000,  # 29
    0x4000,  # 2a
    0x4000,  # 2b
    0x4000,  # 2c
    0x4000,  # 2d
    0x4000,  # 2e
    0x4000,  # 2f
    0x4000,  # 30
    0x4000,  # 31
    0x4000,  # 32
    0x4000,  # 33
    0x4000,  # 34
    0x4000,  # 35
    0x4000,  # 36
    0x4000,  # 37
    0x3df0,  # 38
    [  # 39
        [0x0c00, 0x0c08],  # Skipped weird call, this bank is packed so better use any room
        [0x115d, 0x1169],  # "sndd6"-"snddd", unused sound descriptors
        [0x145c, 0x1468],  # mus41, unused music descriptor
        [0x1a79, 0x1a85],  # Junk data at the end of sndde
        0x3ff2  # End of bank
    ],
    0x4000,  # 3a
    0x4000,  # 3b
    0x4000,  # 3c
    0x4000,  # 3d
    0x4000,  # 3e
    0x314b,  # 3f - also here

    # New banks
    0x0000,  # 40
]

DEFINES = {
    # WRAM addresses
    "wSubscreen1CurrentSlotIndex": "$c085",
    "wOriginalMinimapGroup": "$c09d",  # Custom address
    "wOriginalDungeonIndex": "$c09e",  # Custom address
    "wMinimapCycleToNextMode": "$c09f",  # Custom address
    "wKeysPressed": "$c481",
    "wKeysJustPressed": "$c482",
    "wPaletteThread_mode": "$c4ab",
    "wCustomBuffer": "$c4bf",  # Custom address
    "wAnimalRegion": "$c610",
    "wRingsObtained": "$c616",
    "wTotalSignsDestroyed": "$c626",
    "wDeathRespawnBuffer": "$c62b",
    "wMinimapGroup": "$c63a",
    "wBoughtShopItems2": "$c640",
    "wBoughtSubrosianItems": "$c642",
    "wDimitriState": "$c644",
    "wAnimalTutorialFlags": "$c646",
    "wGashaSpotFlags": "$c649",
    "wDungeonCompasses": "$c67c",
    "wDungeonMaps": "$c67e",
    "wSeedSatchelLevel": "$c680",  # Moved from c6ae
    "<wSeedSatchelLevel": "$80",
    "wSwitchHookLevel": "$c681",
    "<wSwitchHookLevel": "$81",
    "wObtainedTreasureFlags": "$c692",
    "wNetCountIn": "$c6a0",
    "wLinkMaxHealth": "$c6a3",
    "wShieldLevel": "$c6a9",
    "wCurrentBombs": "$c6aa",
    "wMaxBombs": "$c6ab",
    "wNumBombchus": "$c6ad",
    "wMaxBombchus": "$c6ae",
    "wFluteIcon": "$c6af",
    "wFeatherLevel": "$c6b4",
    "wNumEmberSeeds": "$c6b5",
    "wEssencesObtained": "$c6bb",
    "wShooterSelectedSeeds": "$c6bd",  # Replaces wPirateBellState
    "<wShooterSelectedSeeds": "$bd",
    "wSatchelSelectedSeeds": "$c6be",
    "wActiveRing": "$c6c5",
    "wRingBoxLevel": "$c6c6",
    "wInsertedJewels": "$c6e1",
    "wInventoryB": "$c6e8",  # Moved from c680
    "wInventoryA": "$c6e9",  # Moved from c681
    "wInventoryStorage": "$c6ea",  # Moved from c682-691
    "<wInventoryB": "$e8",
    "<wInventoryA": "$e9",
    "<wInventoryStorage": "$ea",
    "wTextIndexL": "$cba2",
    "wTextIndexH": "$cba3",
    "wTextNumberSubstitution": "$cba8",
    "wDungeonMapScroll": "$cbb4",
    "wMapMenuMode": "$cbb3",
    "wMapMenuCursorIndex": "$cbb6",
    "wMenuLoadState": "$cbcc",
    "wMenuActiveState": "$cbcd",
    "wDungeonMapScrollState": "$cbce",
    "wInventorySubmenu0CursorPos": "$cbd0",
    "wInventorySubmenu1CursorPos": "$cbd1",
    "wRingMenu_mode": "$cbd3",
    "wStatusBarNeedsRefresh": "$cbea",
    "wNetTreasureIn": "$cbfb",  # Custom address
    "wSwitchHookState": "$cbfc",  # Custom address
    "wFrameCounter": "$cc00",
    "wIsLinkedGame": "$cc01",
    "wMenuDisabled": "$cc02",
    "wLinkDeathTrigger": "$cc34",
    "wRememberedCompanionRoom": "$cc42",
    "wRememberedCompanionY": "$cc43",
    "wLinkObjectIndex": "$cc48",
    "wActiveGroup": "$cc49",
    "wActiveRoom": "$cc4c",
    "wActiveRoomPack": "$cc4d",
    "wRoomStateModifier": "$cc4e",
    "wActiveMusic": "$cc51",
    "wLostWoodsTransitionCounter1": "$cc53",
    "wLostWoodsTransitionCounter2": "$cc54",
    "wDungeonIndex": "$cc55",
    "wDungeonFloor": "$cc57",
    "wWarpDestGroup": "$cc63",
    "wWarpDestRoom": "$cc64",
    "wWarpTransition": "$cc65",
    "wWarpDestPos": "$cc66",
    "wWarpTransition2": "$cc67",
    "wLinkGrabState": "$cc75",
    "wLinkSwimmingState": "$cc78",
    "wLinkImmobilized": "$cc7c",
    "wDisabledObjects": "$cca4",
    "wRoomEdgeY": "$cca0",
    "wRoomEdgeX": "$cca1",
    "wDisableWarpTiles": "$ccaa",
    "wScreenTransitionDirection": "$cd02",
    "wScreenOffsetY": "$cd08",

    "w1Link.yh": "$d00b",
    "w1Link.xh": "$d00d",
    "w7ActiveBank": "$d0d4",

    # High RAM offsets (FF00 + offset)
    "hRomBank": "$97",

    # Bank 0 functions
    "addAToDe": "$0068",
    "addAToBc": "$006d",
    "interBankCall": "$008a",
    "getNumSetBits": "$0176",
    "checkFlag": "$0205",
    "setFlag": "$020e",
    "decHlRef16WithCap": "$0237",
    "disableLcd": "$02c1",
    "getRandomNumber": "$041a",
    "queueDmaTransfer": "$0566",
    "loadUncompressedGfxHeader": "$05b6",
    "forceEnableIntroInputs": "$0862",
    "saveFile": "$09b4",
    "playSound": "$0c74",
    "setMusicVolume": "$0c89",
    "giveTreasure": "$16eb",
    "loseTreasure": "$1702",
    "checkTreasureObtained": "$1717",
    "refillSeedSatchel": "$17e5",
    "showTextNonExitable": "$1847",
    "showText": "$184b",
    "getThisRoomFlags": "$1956",
    "getRoomFlags": "$1963",
    "openMenu": "$1a76",
    "linkInteractWithAButtonSensitiveObjects": "$1b23",
    "checkLinkCollisionsEnabled": "$1cf0",
    "lookupKey": "$1dc4",
    "lookupCollisionTable": "$1ddd",
    "objectSetVisiblec2": "$1e03",
    "objectSetInvisible": "$1e39",
    "convertShortToLongPosition": "$2089",
    "objectCopyPosition": "$21fd",
    "objectCopyPosition_rawAddress": "$2202",
    "interactionIncState": "$239b",
    "interactionSetScript": "$24fe",
    "createTreasure": "$271b",
    "setLinkIdOverride": "$2a16",
    "clearStaticObjects": "$3076",
    "checkGlobalFlag": "$30c7",
    "setGlobalFlag": "$30cd",
    "unsetGlobalFlag": "$30d3",
    "fastFadeoutToWhite": "$313b",
    "loadScreenMusicAndSetRoomPack": "$32dc",
    "setTile": "$3a52",
    "getFreeInteractionSlot": "$3ac6",
    "interactionDelete": "$3ad9",
    "getFreePartSlot": "$3ea7",

    # Byte constants
    "INVENTORY_CAPACITY": "$14",
    "TEXT_WARP_PROTECTION_MARGIN": "$09",
    "STARTING_TREE_MAP_INDEX": "$f8",
    "INTERACID_TREASURE": "$60",
    "BTN_A": "$01",
    "BTN_B": "$02",
    "BTN_SELECT": "$04",
    "BTN_START": "$08",
    "BTN_RIGHT": "$10",
    "BTN_LEFT": "$20",
    "BTN_UP": "$40",
    "BTN_DOWN": "$80",
    "COLLECT_PICKUP": "$0a",
    "COLLECT_PICKUP_NOFLAG": "$02",
    "COLLECT_CHEST": "$38",
    "COLLECT_CHEST_NOFLAG": "$30",
    # "COLLECT_CHEST_MAP_OR_COMPASS": "$68",
    "COLLECT_FALL": "$29",
    "COLLECT_FALL_KEY": "$28",

    "SND_SOLVEPUZZLE_2": "$5b",
    "SND_GETSEED": "$5e",
    "SND_TELEPORT": "$8d",
    "SND_COMPASS": "$a2",

    "SEASON_SPRING": "$00",
    "SEASON_SUMMER": "$01",
    "SEASON_AUTUMN": "$02",
    "SEASON_WINTER": "$03",

    "TREASURE_SHIELD": "$01",
    "TREASURE_PUNCH": "$02",
    "TREASURE_BOMBS": "$03",
    "TREASURE_CANE_OF_SOMARIA": "$04",
    "TREASURE_SWORD": "$05",
    "TREASURE_BOOMERANG": "$06",
    "TREASURE_ROD_OF_SEASONS": "$07",
    "TREASURE_MAGNET_GLOVES": "$08",
    "TREASURE_SWITCH_HOOK": "$0a",
    "TREASURE_BOMBCHUS": "$0d",
    "TREASURE_FLUTE": "$0e",
    "TREASURE_SHOOTER": "$0f",
    "TREASURE_SLINGSHOT": "$13",
    "TREASURE_BRACELET": "$16",
    "TREASURE_FEATHER": "$17",
    "TREASURE_SEED_SATCHEL": "$19",
    "TREASURE_FOOLS_ORE": "$1e",
    "TREASURE_EMBER_SEEDS": "$20",
    "TREASURE_SCENT_SEEDS": "$21",
    "TREASURE_PEGASUS_SEEDS": "$22",
    "TREASURE_GALE_SEEDS": "$23",
    "TREASURE_MYSTERY_SEEDS": "$24",
    "TREASURE_PIRATES_BELL": "$25",  # Rando specific ID
    "TREASURE_RUPEES": "$28",
    "TREASURE_HEART_REFILL": "$29",
    "TREASURE_HEART_CONTAINER": "$2a",
    "TREASURE_RING": "$2d",
    "TREASURE_FLIPPERS": "$2e",
    "TREASURE_POTION": "$2f",
    "TREASURE_SMALL_KEY": "$30",
    "TREASURE_BOSS_KEY": "$31",
    "TREASURE_COMPASS": "$32",
    "TREASURE_MAP": "$33",
    "TREASURE_GASHA_SEED": "$34",
    "TREASURE_MAKU_SEED": "$36",
    "TREASURE_ORE_CHUNKS": "$37",
    "TREASURE_ESSENCE": "$40",
    "TREASURE_GNARLED_KEY": "$42",
    "TREASURE_FLOODGATE_KEY": "$43",
    "TREASURE_DRAGON_KEY": "$44",
    "TREASURE_STAR_ORE": "$45",
    "TREASURE_RIBBON": "$46",
    "TREASURE_SPRING_BANANA": "$47",
    "TREASURE_RICKY_GLOVES": "$48",
    "TREASURE_BOMB_FLOWER": "$49",
    "TREASURE_RUSTY_BELL": "$4a",
    "TREASURE_TREASURE_MAP": "$4b",
    "TREASURE_ROUND_JEWEL": "$4c",
    "TREASURE_PYRAMID_JEWEL": "$4d",
    "TREASURE_SQUARE_JEWEL": "$4e",
    "TREASURE_X_SHAPED_JEWEL": "$4f",
    "TREASURE_RED_ORE": "$50",
    "TREASURE_BLUE_ORE": "$51",
    "TREASURE_HARD_ORE": "$52",
    "TREASURE_MEMBERS_CARD": "$53",
    "TREASURE_MASTERS_PLAQUE": "$54",
    "TREASURE_BOMB_FLOWER_LOWER_HALF": "$58",
    "TREASURE_CUCCODEX": "$55",  # Rando specific ID
    "TREASURE_LON_LON_EGG": "$56",  # Rando specific ID
    "TREASURE_GHASTLY_DOLL": "$57",  # Rando specific ID
    "TREASURE_IRON_POT": "$35",  # Rando specific ID
    "TREASURE_LAVA_SOUP": "$38",  # Rando specific ID
    "TREASURE_GORON_VASE": "$39",  # Rando specific ID
    "TREASURE_FISH": "$3a",  # Rando specific ID
    "TREASURE_MEGAPHONE": "$3b",  # Rando specific ID
    "TREASURE_MUSHROOM": "$3c",  # Rando specific ID
    "TREASURE_WOODEN_BIRD": "$3d",  # Rando specific ID
    "TREASURE_ENGINE_GREASE": "$3e",  # Rando specific ID
    "TREASURE_PHONOGRAPH": "$3f",  # Rando specific ID

    # Scripting
    "scriptend": "$00",
    "loadscript": "$83",
    "jumptable_memoryaddress": "$87",
    "setcollisionradii": "$8d",
    "setanimation": "$8f",
    "writememory": "$91",
    "ormemory": "$92",
    "rungenericnpc": "$97",
    "showtext": "$98",
    "checkabutton": "$9e",
    "checkcfc0_bit0": "$a0",
    "jumpifroomflagset": "$b0",
    "orroomflag": "$b1",
    "script_d1Entrance": "$b2",
    "jumpifc6xxset": "$b3",
    "writec6xx": "$b4",
    "setglobalflag": "$b6",
    "script_nop": "$b7",
    "setdisabledobjectsto00": "$b9",
    "setdisabledobjectsto11": "$ba",
    "disableinput": "$bd",
    "enableinput": "$be",
    "callscript": "$c0",
    "retscript": "$c1",
    "jumpalways": "$c4",
    "jumpifmemoryset": "$c7",
    "jumpifmemoryeq": "$cb",
    "checkcollidedwithlink_onground": "$d0",
    "setcounter1": "$d7",
    "loseitem": "$dc",
    "spawnitem": "$dd",
    "giveitem": "$de",
    "jumpifitemobtained": "$df",
    "asm15": "$e0",
    "initcollisions": "$eb",
    "movedown": "$ee",
    "delay1frame": "$f0",
    "delay30frames": "$f6",
    "setdisabledobjectsto91": "$b8",
    "showtextlowindex": "$98",
    "writeobjectbyte": "$8e",
    "setspeed": "$8b",
    "moveup": "$ec",
}

RUPEE_VALUES = {
    0: 0x00,
    1: 0x01,
    2: 0x02,
    5: 0x03,
    10: 0x04,
    20: 0x05,
    40: 0x06,
    30: 0x07,
    60: 0x08,
    70: 0x09,
    25: 0x0a,
    50: 0x0b,
    100: 0x0c,
    200: 0x0d,
    400: 0x0e,
    150: 0x0f,
    300: 0x10,
    500: 0x11,
    900: 0x12,
    80: 0x13,
    999: 0x14,
}

DUNGEON_ENTRANCES = {
    "d0": {
        "addr": 0x13651,
        "map_tile": 0xd4,
        "room": 0xd4,
        "group": 0x00,
        "position": 0x54
    },
    "d1": {
        "addr": 0x1346d,
        "map_tile": 0x96,
        "room": 0x96,
        "group": 0x00,
        "position": 0x44
    },
    "d2": {
        "addr": 0x13659,
        "map_tile": 0x8d,
        "room": 0x8d,
        "group": 0x00,
        "position": 0x24
    },
    "d3": {
        "addr": 0x13671,
        "map_tile": 0x60,
        "room": 0x60,
        "group": 0x00,
        "position": 0x25
    },
    "d4": {
        "addr": 0x13479,
        "map_tile": 0x1d,
        "room": 0x1d,
        "group": 0x00,
        "position": 0x13
    },
    "d5": {
        "addr": 0x1347d,
        "map_tile": 0x8a,
        "room": 0x8a,
        "group": 0x00,
        "position": 0x25
    },
    "d6": {
        "addr": 0x13481,
        "map_tile": 0x00,
        "room": 0x00,
        "group": 0x00,
        "position": 0x34
    },
    "d7": {
        "addr": 0x13485,
        "map_tile": 0xd0,
        "room": 0xd0,
        "group": 0x00,
        "position": 0x34
    },
    "d8": {
        "addr": 0x1369d,
        "map_tile": 0x04,
        "room": 0x00,
        "group": 0x01,
        "position": 0x23
    },
}

DUNGEON_EXITS = {
    "d0": 0x13909,
    "d1": 0x1390d,
    "d2": 0x13911,
    "d3": 0x13915,
    "d4": 0x13919,
    "d5": 0x1391d,
    "d6": 0x13921,
    "d7": 0x13a89,
    "d8": 0x13a8d,
}

PORTAL_WARPS = {
    "eastern suburbs portal": {
        "addr": 0x134fd,
        "map_tile": 0x9a,
        "in_subrosia": False,
        "text_index": 0x0,
    },
    "spool swamp portal": {
        "addr": 0x13501,
        "map_tile": 0xb0,
        "in_subrosia": False,
        "text_index": 0x1,
    },
    "mt. cucco portal": {
        "addr": 0x13601,
        "map_tile": 0x1e,
        "in_subrosia": False,
        "text_index": 0x2,
    },
    "eyeglass lake portal": {
        "addr": 0x13509,
        "map_tile": 0xb9,
        "in_subrosia": False,
        "text_index": 0x3,
    },
    "horon village portal": {
        "addr": 0x13905,
        "map_tile": 0xf7,
        "in_subrosia": False,
        "text_index": 0x4,
    },
    "temple remains lower portal": {
        "addr": 0x1350d,
        "map_tile": 0x25,
        "in_subrosia": False,
        "text_index": 0x5,
    },
    "temple remains upper portal": {
        "addr": 0x1388d,
        "map_tile": 0x04,
        "in_subrosia": False,
        "text_index": 0x6,
    },

    "volcanoes east portal": {
        "addr": 0x136b5,
        "map_tile": 0x05,
        "in_subrosia": True,
        "text_index": 0x7,
    },
    "subrosia market portal": {
        "addr": 0x136b9,
        "map_tile": 0x3e,
        "in_subrosia": True,
        "text_index": 0x8,
    },
    "strange brothers portal": {
        "addr": 0x136bd,
        "map_tile": 0x3a,
        "in_subrosia": True,
        "text_index": 0x9,
    },
    "great furnace portal": {
        "addr": 0x136c1,
        "map_tile": 0x36,
        "in_subrosia": True,
        "text_index": 0xa,
    },
    "house of pirates portal": {
        "addr": 0x13729,
        "map_tile": 0x4f,
        "in_subrosia": True,
        "text_index": 0xb,
    },
    "volcanoes west portal": {
        "addr": 0x136c5,
        "map_tile": 0x0e,
        "in_subrosia": True,
        "text_index": 0xc,
    },
    "d8 entrance portal": {
        "addr": 0x136c9,
        "map_tile": 0x16,
        "in_subrosia": True,
        "text_index": 0xd,
    }
}

PALETTE_BYTES = {
    "green": 0x00,
    "blue": 0x01,
    "red": 0x02,
    "orange": 0x03,
}

# Scripting constants
DELAY_6 = 0xf6
CALL_SCRIPT = 0xc0
MOVE_UP = 0xec
MOVE_DOWN = 0xee
MOVE_LEFT = 0xef
MOVE_RIGHT = 0xed
WRITE_OBJECT_BYTE = 0x8e
SHOW_TEXT_LOW_INDEX = 0x98
ENABLE_ALL_OBJECTS = 0xb9

DIRECTION_STRINGS = {
    DIRECTION_UP: "⬆ ",
    DIRECTION_DOWN: "⬇ ",
    DIRECTION_LEFT: "⬅ ",
    DIRECTION_RIGHT: "➡ ",
}

SEASON_STRINGS = {
    SEASON_SPRING: "Spring",
    SEASON_SUMMER: "Summer",
    SEASON_AUTUMN: "Autumn",
    SEASON_WINTER: "Winter"
}
