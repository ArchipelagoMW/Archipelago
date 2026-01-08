EOB_ADDR = [
  0x3ef8, # 00
  0x7f23, # 01 - garbage data here
  0x7de7, # 02 - garbage data here
  0x7e54, # 03 - garbage data here
  0x7ee2, # 04
  0x7d9d, # 05
  0x7a73, # 06 - garbage data here - 128 bytes reserved for sprite expansion w/ web patcher
  0x7caa, # 07 - garbage data here
  0x7f5c, # 08
  0x7def, # 09
  0x7e08, # 0a
  0x7fa8, # 0b
  0x7f94, # 0c
  0x7eaa, # 0d
  0x7f88, # 0e
  0x7f90, # 0f
  0x7ef4, # 10
  0x7f73, # 11
  0x7e8f, # 12
  0x7ef0, # 13
  0x7acd, # 14
  0x7bfb, # 15
  0x7e03, # 16
  0x6ee3, # 17 - garbage data here (lots of space here)
  0x799e, # 18 - garbage data here
  0x7fdf, # 19
  0x7ed0, # 1a
  0x7ee0, # 1b
  0x7dc0, # 1c - garbage data here
  0x8000, # 1d
  0x8000, # 1e
  0x8000, # 1f
  0x8000, # 20
  0x8000, # 21
  0x8000, # 22
  0x8000, # 23
  0x8000, # 24
  0x8000, # 25
  0x8000, # 26
  0x8000, # 27
  0x8000, # 28
  0x8000, # 29
  0x8000, # 2a
  0x8000, # 2b
  0x8000, # 2c
  0x8000, # 2d
  0x8000, # 2e
  0x8000, # 2f
  0x8000, # 30
  0x8000, # 31
  0x8000, # 32
  0x8000, # 33
  0x8000, # 34
  0x8000, # 35
  0x8000, # 36
  0x8000, # 37
  0x6afb, # 38 - lots of space here
  0x8000, # 39
  0x8000, # 3a
  0x8000, # 3b
  0x8000, # 3c
  0x8000, # 3d
  0x8000, # 3e
  0x7d0a  # 3f 
]

DEFINES = {
    "AREAFLAG_OUTDOORS":"$01",
    "BTN_A": "$01",
    "BTN_B": "$02",
    "COLLECT_PICKUP_NOFLAG":"$02",
    "COLLECT_PICKUP":"$0a",
    "COLLECT_POOF":"$1a",
    "COLLECT_FALL_KEY":"$28",
    "COLLECT_FALL":"$29",
    "COLLECT_CHEST_NOFLAG":"$30",
    "COLLECT_CHEST":"$38",
    "COLLECT_DIVE":"$49",
    "COLLECT_CHEST_MAP_OR_COMPASS":"$68",
    "SND_GETITEM":"$4c",
    "SND_CLINK":"$50",
    "SND_ERROR":"$5a",
    "SND_SOLVEPUZZLE_2":"$5b",
    "SND_TELEPORT":"$8d",
    "SND_GETSEED": "$5e",
    "SND_COMPASS": "$a2",
    "TREASURE_SHIELD":"$01",
    "TREASURE_PUNCH":"$02",
    "TREASURE_BOMBS":"$03",
    "TREASURE_CANE_OF_SOMARIA":"$04",
    "TREASURE_SWORD":"$05",
    "TREASURE_BOOMERANG":"$06",
    "TREASURE_ROD_OF_SEASONS":"$07",
    "TREASURE_MAGNET_GLOVES":"$08",
    "TREASURE_SWITCH_HOOK":"$0a",
    "TREASURE_BIGGORON_SWORD":"$0c",
    "TREASURE_FLUTE":"$0e",
    "TREASURE_SHOOTER":"$0f",
    "TREASURE_HARP":"$11",
    "TREASURE_SLINGSHOT":"$13",
    "TREASURE_BRACELET":"$16",
    "TREASURE_FEATHER":"$17",
    "TREASURE_SEED_SATCHEL":"$19",
    "TREASURE_FOOLS_ORE":"$1e",
    "TREASURE_EMBER_SEEDS":"$20",
    "TREASURE_SCENT_SEEDS":"$21",
    "TREASURE_PEGASUS_SEEDS":"$22",
    "TREASURE_GALE_SEEDS":"$23",
    "TREASURE_MYSTERY_SEEDS":"$24",
    "TREASURE_TUNE_OF_ECHOES":"$25",
    "TREASURE_TUNE_OF_CURRENTS":"$26",
    "TREASURE_TUNE_OF_AGES":"$27",
    "TREASURE_RUPEES":"$28",
    "TREASURE_HEART_REFILL":"$29",
    "TREASURE_HEART_CONTAINER":"$2a",
    "TREASURE_RING":"$2d",
    "TREASURE_FLIPPERS":"$2e",
    "TREASURE_SMALL_KEY":"$30",
    "TREASURE_BOSS_KEY":"$31",
    "TREASURE_COMPASS":"$32",
    "TREASURE_MAP":"$33",
    "TREASURE_MAKU_SEED":"$36",
    "TREASURE_ESSENCE":"$40",
    "TREASURE_TRADEITEM":"$41",
    "TREASURE_STAR_ORE":"$45",
    "TREASURE_MERMAID_SUIT":"$4a",
    "TREASURE_MASTERS_PLAQUE":"$54",
    "TREASURE_GORON_LETTER":"$59",
    "TREASURE_GNARLED_KEY":"$42",
    "TREASURE_FLOODGATE_KEY":"$43",
    "TREASURE_DRAGON_KEY":"$44",
    "TREASURE_STAR_ORE":"$45",
    "TREASURE_RIBBON":"$46",
    "TREASURE_SPRING_BANANA":"$47",
    "TREASURE_RICKY_GLOVES":"$48",
    "TREASURE_BOMB_FLOWER":"$49",
    "TREASURE_RUSTY_BELL":"$4a",
    "TREASURE_PIRATES_BELL":"$25",
    "TREASURE_TREASURE_MAP":"$4b",
    "TREASURE_ROUND_JEWEL":"$4c",
    "TREASURE_PYRAMID_JEWEL":"$4d",
    "TREASURE_SQUARE_JEWEL":"$4e",
    "TREASURE_X_SHAPED_JEWEL":"$4f",
    "TREASURE_RED_ORE":"$50",
    "TREASURE_BLUE_ORE":"$51",
    "TREASURE_HARD_ORE":"$52",
    "TREASURE_MEMBERS_CARD":"$53",
    "TREASURE_MASTERS_PLAQUE":"$54",
    "TREASURE_BOMB_FLOWER_LOWER_HALF":"$58",
    "TREASURE_POE_CLOCK":"$3d",
    "TREASURE_STATIONARY":"$3e",
    "TREASURE_STINK_BAG":"$3f",
    "TREASURE_TASTY_MEAT":"$47",
    "TREASURE_DOGGIE_MASK":"$56",
    "TREASURE_DUMBBELL":"$57",
    "TREASURE_CHEESY_MUSTACHE":"$5f",
    "TREASURE_FUNNY_JOKE":"$3c",
    "TREASURE_TOUCHING_BOOK":"$35",
    "TREASURE_MAGIC_OAR":"$38",
    "TREASURE_SEA_UKULELE":"$39",
    "TREASURE_BROKEN_SWORD":"$3a",
    "TREASURE_GASHA_SEED":"$34",
    "TREASURE_POTION":"$2f",
    "TREASURE_ZORA_POTION":"$37", # Replace Ore Chunk
    "TX_REMOTE_ITEM":"$3b",
    "DEV_RING":"$40",
    "INTERAC_MULTI_BYTE":"$7f # low byte of struct",
    "INTERACID_TREASURE":"$60",

    # script commands
    "scriptend":"$00",
    "loadscript":"$83",
    "jumptable_memoryaddress":"$87",
    "setcollisionradii":"$8d",
    "setanimation":"$8f",
    "writememory":"$91",
    "ormemory":"$92",
    "rungenericnpc":"$97",
    "showtext":"$98",
    "showloadedtext":"$9d",
    "checkabutton":"$9e",
    "checkcfc0_bit0":"$a0",
    "jumpifroomflagset":"$b0",
    "orroomflag":"$b1",
    "jumpifc6xxset":"$b3",
    "writec6xx":"$b4",
    "setdisabledobjectsto00":"$b9",
    "setdisabledobjectsto11":"$ba",
    "disableinput":"$bd",
    "enableinput":"$be",
    "callscript":"$c0",
    "retscript":"$c1",
    "jumpalways":"$c4",
    "jumpifmemoryset":"$c7",
    "jumpifmemoryeq":"$cb",
    "checkcollidedwithlink_onground":"$d0",
    "setcounter1":"$d7",
    "loseitem":"$dc",
    "spawnitem":"$dd",
    "jumpifglobalflagset":"$b5",
    "setglobalflag":"$b6",
    "giveitem":"$de",
    "jumpifitemobtained":"$df",
    "asm15":"$e0",
    "initcollisions":"$eb",
    "movedown":"$ee",
    "delay1frame":"$f0",
    "delay30frames":"$f6",
    "setdisabledobjectsto91":"$b8",
    "showtextlowindex":"$98",
    "writeobjectbyte":"$8e",
    "setspeed":"$8b",
    "moveup":"$ec",

    # hram
    "hGameboyType":"$96",
    "hRomBank":"$97",

    # wram
    "wKeysPressed":"$c481",
    "wKeysJustPressed":"$c482",
    "wAnimalRegion":"$c610",
    "wWhichGame":"$c611",
    "wFileIsCompleted":"$c614",
    "wRingsObtained":"$c616",
    "wTotalSignsDestroyed":"$c626",
    "wTextIndexL":"$cba2",
    "wTextIndexH":"$cba3",
    "wTextNumberSubstitution":"$cba8",
    "wMapMenu_mode":"$cbb3",
    "wMapMenu_cursorIndex":"$cbb6",
    "wInventorySubmenu1CursorPos":"$cbd1",
    "wRingMenu_mode":"$cbd3",
    "wNetTreasureIn":"$cbfb",
    "wNetPlayerOut":"$cbfd",
    "wNetTreasureOut":"$cbfe",
    "wIsLinkedGame":"$cc01",
    "wMenuDisabled":"$cc02",
    "wCutsceneState":"$cc03",
    "wMaxBombs": "$c6b1",
    "wLinkMaxHealth": "$c6ab",
    "wNumEmberSeeds": "$c6b9",
    "wCutsceneTrigger":"$cc04",
    "wScreenTransitionDirection":"$cd02",
    "wScreenOffsetY":"$cd08",
    "wScreenShakeCounterY":"$cd18",
    "w1Link.state":"$d004",
    "w1Link.angle":"$d009",
    "w1Link.yh":"$d00b",
    "w1Link.xh":"$d00d",
    "w7ActiveBank":"$d0d4",
    "wWarpDestGroup":"$cc47",
    "wWarpDestRoom":"$cc48",
    "wWarpTransition":"$cc49",
    "wWarpDestPos":"$cc4a",
    "wWarpTransition2":"$cc4b",
    "wBoughtItems1":"$c642",
    "wBoughtItems2":"$c643",
    "wDungeonCompasses":"$c684",

    # rom 00
    "interBankCall":"$008a",
    "getNumSetBits":"$0176",
    "compareHlToBc":"$01d6",
    "setFlag":"$020e",
    "decHlRef16WithCap":"$0237",

    # rom 3f
    "_interactionGetData":"$4437",
    "giveTreasure_body":"$44c8",

    # AGES SPECIFIC
    # constants
    "BANK_TREASURE_DATA":"$16",
    "BANK_FILE_SELECT_GFX":"$38",
    "BANK_OWL_TEXT":"$38",
    "BANK_ROOM_TREASURES":"$38",
    "STARTING_TREE_MAP_INDEX":"$78",

    # hram
    "hDirtyBgPalettes":"$a6",
    "hDirtySprPalettes":"$a7",
    "hCameraY":"$aa",
    "hCameraX":"$ac",
    "hMusicVolume":"$b6",

    # wram
    "wFeatherLevel":"$0 # not present in ages",
    "wRememberedCompanionId":"$cc24",
    "wRickyState":"$c646",
    "wDimitriState":"$c647",
    "wAnimalTutorialFlags":"$c649",
    "wDungeonBossKeys":"$c682",
    "wInventoryB":"$c688",
    "wObtainedTreasureFlags":"$c69a",
    "wNetCountInL":"$c6a8",
    "wNetCountInH":"$c6a9",
    "wSeedSatchelLevel":"$c6b4",
    "wFluteIcon":"$c6b5",
    "wEssencesObtained":"$c6bf",
    "wTradeItem":"$c6c0",
    "wSatchelSelectedSeeds": "$c6c4",
    "wActiveRing":"$c6cb",
    "wRingBoxLevel":"$c6cc",
    "wMakuMapTextPresent":"$c6e6",
    "wMakuMapTextPast":"$c6e7",
    "wMakuTreeState":"$c6e8",
    "wJabuWaterLevel":"$c6e9",
    "wStatusBarNeedsRefresh":"$cbe9",
    "wActiveGroup":"$cc2d",
    "wActiveRoom":"$cc30",
    "wAreaFlags":"$cc34",
    "wDungeonIndex":"$cc39",
    "wWarpDestGroup":"$cc47",
    "wWarpDestRoom":"$cc48",
    "wWarpTransition":"$cc49",
    "wWarpTransition2":"$cc4b",
    "wLinkGrabState":"$cc5a",
    "wDisableTransitions":"$cc91",
    "wDisabledObjects":"$cc8a",
    "wPlayingInstrument1":"$cc8d",
    "wRoomLayout":"$cf00",
    "wLinkObjectIndex":"$cc2c",
    "wMenuLoadState":"$cbcc",
    "wLinkDeathTrigger": "$cdd5",

    # rom 00
    "checkFlag": "$0205",
    "getRandomNumber":"$043e",
    "clearMemory":"$046f",
    "copyMemory":"$0486",
    "queueDmaTransfer":"$058a",
    "loadUncompressedGfxHeader":"$05da",
    "forceEnableIntroInputs":"$0886",
    "playSound":"$0c98",
    "saveFile": "$09d8",
    "setMusicVolume":"$0cad",
    "giveTreasure":"$171c",
    "loseTreasure":"$1733",
    "checkTreasureObtained":"$1748",
    "refillSeedSatchel":"$180c",
    "showTextNonExitable":"$186e",
    "showText":"$1872",
    "getThisRoomFlags":"$197d",
    "openMenu":"$1ab0",
    "linkInteractWithAButtonSensitiveObjects":"$1b5d",
    "lookupKey":"$1e06",
    "lookupCollisionTable":"$1e1f",
    "objectSetVisiblec2":"$1e45",
    "objectDelete_useActiveObjectType":"$21e0",
    "objectCopyPosition":"$2242",
    "objectCopyPosition_rawAddress":"$2247",
    "objectCreateInteraction":"$24c5",
    "createTreasure":"$27d4",
    "checkGlobalFlag":"$31f3",
    "setGlobalFlag":"$31f9",
    "fadeInFromWhite":"$3299",
    "incMakuTreeState":"$3e53",
    "interactionDelete":"$3b05",
    "clearStaticObjects":"$319f",

    # rom 02
    "_closeMenu":"$4fba",
    "clearMenu":"$50b1",
    "_mapMenu_checkCursorRoomVisited":"$6636",
    "_mapMenu_checkRoomVisited":"$6639",
    "_ringMenu_updateSelectedRingFromList":"$723b",

    # rom 04
    "applyAllTileSubstitutions":"$5fef",

    # rom 09
    "interactionCode60":"$4973",

    # rom 16
    "treasureObjectData":"$5332",

    # rom 3f
    "realignUnappraisedRings":"$466f",
    "interaction60SubidData":"$66db",

    # Existing Global Flag
    "GLOBALFLAG_WON_FAIRY_HIDING_GAME":"$0e",
    "GLOBALFLAG_TUNI_NUT_PLACED":"$29",
	"GLOBALFLAG_BOUGHT_FEATHER_FROM_TOKAY" : "$36",
	"GLOBALFLAG_BOUGHT_BRACELET_FROM_TOKAY"	: "$37",

    # Custom Global Flag
    "GLOBALFLAG_GOT_SEACHART":"$03",
    "GLOBALFLAG_WON_FIRST_DANCE":"$07",
    "GLOBALFLAG_WON_LETTER_DANCE":"$0b",
    "GLOBALFLAG_NAYRU_SAVED":"$0d",
    "GLOBALFLAG_REWARD_KING_ZORA":"$10",
    "GLOBALFLAG_TRADE_MAPLE":"$17",
    "GLOBALFLAG_REPAIRED_TUNI":"$1e",
    "GLOBALFLAG_REPAIRED_SWORD":"$2d",
    "GLOBALFLAG_VERAN_BEATEN":"$47",
    "GLOBALFLAG_GOT_TUNINUT_FROM_BROTHER":"$48",
    "GLOBALFLAG_WON_LYNNA_SHOOTING_GALLERY":"$49",
    "GLOBALFLAG_GAVE_MYST_SEED":"$4a",
}

ASM_FILES = [
    "asm/util.yaml",
    "asm/new_game.yaml",
    "asm/triggers.yaml",
    "asm/cutscenes.yaml",
    "asm/layouts.yaml",
    "asm/collect.yaml",
    "asm/location.yaml",
    "asm/map_menu.yaml",
    "asm/progressives.yaml",
    "asm/animals.yaml",
    "asm/static_items.yaml",
    "asm/multi.yaml",
    "asm/rings.yaml",
    "asm/misc.yaml",
    "asm/new_treasures.yaml",
    "asm/item_events.yaml",
    "asm/timeportals.yaml",
    "asm/boss_items.yaml",
    "asm/keysanity.yaml",
    "asm/shops_handling.yaml",
    "asm/gfx.yaml",
    "asm/get_item_behavior.yaml",
    "asm/vars.yaml",
    "asm/text.yaml",
    "asm/remove_item_on_use.yaml",
    "asm/dungeon_shuffle.yaml",
    "asm/file_select_custom_string.yaml",
    "asm/impa_refill.yaml",
    "asm/combat_difficulty.yaml",
    "asm/tokay_market.yaml",
    "asm/compass_chimes.yaml",
    "asm/warp_to_start.yaml"
]

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
        "addr": 0x13728,
        "map_tile": 0x148,
        "room": 0x48,
        "group": 0x01,
        "position": 0x21,
        "shifted": False,
        "default":"d0"
    },
    "d1": {
        "addr": 0x13718,
        "map_tile": 0x08d,
        "room": 0x8d,
        "group": 0x00,
        "position": 0x26,
        "essence_exit": 0x2874f,
        "shifted": False,
        "default":"d1"
    },
    "d2 past": {
        "addr": 0x1372c,
        "map_tile": 0x183,
        "room": 0x83,
        "group": 0x01,
        "position": 0x25,
        "shifted": False,
        "default":"d2"
    },
    "d2 present": {
        "addr": 0x13000,
        "map_tile": 0x083,
        "room": 0x83,
        "group": 0x00,
        "position": 0x25,
        "shifted": False,
        "default":"N/A"
    },
    "d3": {
        "addr": 0x135c8,
        "map_tile": 0x0ba,
        "room": 0xba,
        "group": 0x00,
        "position": 0x55,
        "shifted": False,
        "default":"d3"
    },
    "d4": {
        "addr": 0x135cc,
        "map_tile": 0x003,
        "room": 0x03,
        "group": 0x00,
        "position": 0x35,
        "shifted": True,
        "default":"d4"
    },
    "d5": {
        "addr": 0x136b0,
        "map_tile": 0x00a,
        "room": 0x0a,
        "group": 0x00,
        "position": 0x17,
        "shifted": False,
        "default":"d5"
    },
    "d6 present": {
        "addr": 0x13748,
        "map_tile": 0x03c,
        "room": 0x0e,
        "group": 0x01,
        "position": 0x16,
        "shifted": False,
        "default":"d6 present"
    },
    "d7": {
        "addr": 0x13874,
        "map_tile": 0x090,
        "room": 0x90,
        "group": 0x02,
        "position": 0x45,
        "shifted": True,
        "default":"d7"
    },
    "d8": {
        "addr": 0x13730,
        "map_tile": 0x15c,
        "room": 0x5c,
        "group": 0x01,
        "position": 0x15,
        "shifted": True,
        "default":"d8"
    },
    "d6 past": {
        "addr": 0x139b4,
        "map_tile": 0x13c,
        "room": 0x0f,
        "group": 0x03,
        "position": 0x16,
        "shifted": False,
        "default":"d6 past"
    },
}

DUNGEON_EXITS = {
    # TODO
    "d0": 0x13aec,
    "d1": 0x13ad0,
    "d2": 0x13ad4,
    "d3": 0x13ad8,
    "d4": 0x13adc,
    "d5": 0x13ae0,
    "d6 present": 0x13c48,
    "d7": 0x13c60,
    "d8": 0x13c74,
    "d6 past": 0x13c54,
}

PALETTE_BYTES = {
    "green": 0x00,
    "blue": 0x01,
    "red": 0x02,
    "orange": 0x03,
}

SEED_TREE_DATA = {
    "Lynna Present" : {
        "location" : "Lynna City: Seed Tree",
        "codeAdress" : 0x49ca4,
    },
    "Lynna Past" : {
        "location" : "Lynna City: Seed Tree",
        "codeAdress" : 0x49e62,
    },
    "Ambi's Palace" : {
        "location" : "Ambi's Palace: Seed Tree",
        "codeAdress" : 0x49e5b,
    },
    "Deku Forest" : {
        "location" : "Deku Forest: Seed Tree",
        "codeAdress" : 0x4a101,
    },
    "Crescent Island" : {
        "location" : "Crescent Island: Seed Tree",
        "codeAdress" : 0x499b8,
    },
    "Symmetry city" : {
        "location" : "Symmetry city: Seed Tree",
        "codeAdress" : 0x499a1,
    },
    "Rolling Ridge West" : {
        "location" : "Rolling Ridge West: Seed Tree",
        "codeAdress" : 0x49e4d,
    },
    "Rolling Ridge East" : {
        "location" : "Rolling Ridge East: Seed Tree",
        "codeAdress" : 0x49f46,
    },
    "Zora Present" : {
        "location" : "Zora Village: Seed Tree",
        "codeAdress" : 0x499bf,
    },
    "Zora Past" : {
        "location" : "Zora Village: Seed Tree",
        "codeAdress" : 0x49e6f,
    },
}