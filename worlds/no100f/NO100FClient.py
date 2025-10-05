import asyncio
import os.path
import shutil
import subprocess
import sys
import time
import traceback
import zipfile
from enum import Enum
from enum import Flag
from typing import Callable, Optional, Any, Dict

from worlds.no100f import NO100FContainer
import dolphin_memory_engine

import Utils
from CommonClient import CommonContext, server_loop, gui_enabled, ClientCommandProcessor, logger, \
    get_base_parser


class CheckTypes(Flag):
    UPGRADES = 1
    MONSTERTOKENS = 2
    KEYS = 3
    SNACKS = 4
    WARPGATES = 5


CONNECTION_REFUSED_GAME_STATUS = "Dolphin Connection refused due to invalid Game. Please load the US Version of NO100F."
CONNECTION_REFUSED_SAVE_STATUS = "Dolphin Connection refused due to invalid Save. " \
                                 "Please make sure you loaded a save file used on this slot and seed."
CONNECTION_LOST_STATUS = "Dolphin Connection was lost. Please restart your emulator and make sure NO100F is running."
CONNECTION_CONNECTED_STATUS = "Dolphin Connected"
CONNECTION_INITIAL_STATUS = "Dolphin Connection has not been initiated"

SCENE_OBJ_LIST_PTR_ADDR = 0x8025f0e0
SCENE_OBJ_LIST_SIZE_ADDR = 0x8025e5ac

CUR_SCENE_ADDR = 0x8025f0d0

HEALTH_ADDR = 0x80234DC8
SNACK_COUNT_ADDR = 0x80235094  # 4 Bytes
UPGRADE_INVENTORY_ADDR = 0x80235098  # 4 Bytes
MONSTER_TOKEN_INVENTORY_ADDR = 0x8023509C  # 4 Bytes
MAX_GUM_COUNT_ADDR = 0x802350A8
MAX_SOAP_COUNT_ADDR = 0x802350AC
PLAYER_CONTROL_OWNER = 0x80234e90
MAP_ADDR = 0x8025F140
WARP_ADDR = 0x801b7ef4
VISITED_SCENES_ADDR = 0x8026af70

SLOT_NAME_ADDR = 0x801c5c9c
SEED_ADDR = SLOT_NAME_ADDR + 0x40
# we currently write/read 0x20 bytes starting from 0x817f0000 to/from save game
# expected received item index
EXPECTED_INDEX_ADDR = 0x817f0000
KEY_COUNT_ADDR = 0x817f0004
# Free space for 0F-14
STORED_SNACK_ADDR = 0x817f0015
BOSS_KILLS_ADDR = 0x817f0019
# Free space for 1A and 1B
SAVED_WARP_ADDR = 0x817f001C
# delayed item
SAVED_SLOT_NAME_ADDR = 0x817f0020
SAVED_SEED_ADDR = SAVED_SLOT_NAME_ADDR + 0x40


class Upgrades(Enum):              # Bit assigned at 0x80235098
    GumPower = 0xD4FD7D3C          # xxxx xxxx xxxx xxxx x000 0000 0000 0001
    SoapPower = 0xE8A3B45F         # xxxx xxxx xxxx xxxx x000 0000 0000 0010
    BootsPower = 0x9133CECD        # xxxx xxxx xxxx xxxx x000 0000 0000 0100
    PlungerPower = 0xDA82A36C      # xxxx xxxx xxxx xxxx x000 0000 0000 1000
    SlippersPower = 0x9AD0813E     # xxxx xxxx xxxx xxxx x000 0000 0001 0000
    LampshadePower = 0x6FAFFB01    # xxxx xxxx xxxx xxxx x000 0000 0010 0000
    BlackKnightPower = 0xB00E719E  # xxxx xxxx xxxx xxxx x000 0000 0100 0000
    SpringPower = 0xD88133D6       # xxxx xxxx xxxx xxxx x000 0010 0000 0000
    PoundPower = 0x84D3E950        # xxxx xxxx xxxx xxxx x000 0100 0000 0000
    HelmetPower = 0x2F03BFDC       # xxxx xxxx xxxx xxxx x000 1000 0000 0000
    UmbrellaPower = 0xC889BB9E     # xxxx xxxx xxxx xxxx x001 0000 0000 0000
    ShovelPower = 0x866C5887       # xxxx xxxx xxxx xxxx x010 0000 0000 0000
    ShockwavePower = 0x1B0ADE07    # xxxx xxxx xxxx xxxx x100 0000 0000 0000
    GumOverAcid2 = 0xEAF330FE      # Gum upgrades increment 0x802350A8 by 5.
    GumPack = 0xFFD0E61E
    GumMaxAmmo = 0xFFFD7A85
    Gum_Upgrade = 0x362E34B4
    GumUpgrade = 0x7EDE8BAD
    BubblePack = 0xBF9B5D09
    Soap__Box = 0xD656A182         # Soap upgrades increment 0x802350AC by 5
    SoapBox1 = 0x3550C423
    SoapOverAcid2 = 0x0C7A534E
    Soap_Box = 0xDEC7BAA7
    SoapBox = 0xB380CBF0
    SoapPack = 0xDCC4E558


class MonsterTokens(Enum):       # Bit assigned at 0x8023509C
    MT_BLACKKNIGHT = 0x3A6FCC38  # xxxx xxxx xxx0 0000 0000 0000 0000 0001
    MT_MOODY = 0xDC98824E        # xxxx xxxx xxx0 0000 0000 0000 0000 0010
    MT_CAVEMAN = 0x56400EF1      # xxxx xxxx xxx0 0000 0000 0000 0000 0100
    MT_CREEPER = 0xDFA0C15E      # xxxx xxxx xxx0 0000 0000 0000 0000 1000
    MT_GARGOYLE = 0xFBBC715F     # xxxx xxxx xxx0 0000 0000 0000 0001 0000
    MT_GERONIMO = 0x94C56BF0     # xxxx xxxx xxx0 0000 0000 0000 0010 0000
    MT_GHOST = 0x74004B8A        # xxxx xxxx xxx0 0000 0000 0000 0100 0000
    MT_GHOSTDIVER = 0x2ACB9327   # xxxx xxxx xxx0 0000 0000 0000 1000 0000
    MT_GREENGHOST = 0xF077B0E1   # xxxx xxxx xxx0 0000 0000 0001 0000 0000
    MT_HEADLESS = 0x52CE630A     # xxxx xxxx xxx0 0000 0000 0010 0000 0000
    MT_MASTERMIND = 0x08D04C9B   # xxxx xxxx xxx0 0000 0000 0100 0000 0000
    MT_ROBOT = 0x699623C9        # xxxx xxxx xxx0 0000 0000 1000 0000 0000
    MT_REDBEARD = 0x0F7F79CB     # xxxx xxxx xxx0 0000 0001 0000 0000 0000
    MT_SCARECROW = 0xAB19F726    # xxxx xxxx xxx0 0000 0010 0000 0000 0000
    MT_SEACREATURE = 0x6CC29412  # xxxx xxxx xxx0 0000 0100 0000 0000 0000
    MT_SPACEKOOK = 0xFC42FAAC    # xxxx xxxx xxx0 0000 1000 0000 0000 0000
    MT_TARMONSTER = 0x2E849EB9   # xxxx xxxx xxx0 0001 0000 0000 0000 0000
    MT_WITCH = 0x8CFF4526        # xxxx xxxx xxx0 0010 0000 0000 0000 0000
    MT_WITCHDOC = 0x55794316     # xxxx xxxx xxx0 0100 0000 0000 0000 0000
    MT_WOLFMAN = 0x51D4A7D2      # xxxx xxxx xxx0 1000 0000 0000 0000 0000
    MT_ZOMBIE = 0x818F2933       # xxxx xxxx xxx1 0000 0000 0000 0000 0000


class Keys(Enum):
    DOORKEY = 0x13109411
    DOORKEY1 = 0xC17BC4E4
    DOORKEY2 = 0xC17BC4E5
    DOORKEY3 = 0xC17BC4E6
    DOORKEY4 = 0xC17BC4E7
    DUG_FISHING_KEY = 0xBB82B3B3
    HEDGE_KEY = 0xBBFA4948
    KEY = 0x0013C74B
    KEY_01 = 0x76E9B34A
    KEY_02 = 0x76E9B34B
    KEY_03 = 0x76E9B34C
    KEY_1 = 0x2DDAB334
    KEY_2 = 0x2DDAB335
    KEY_3 = 0x2DDAB336
    KEY_4 = 0x2DDAB337
    KEY01 = 0x2DDABB64
    KEY02 = 0x2DDABB65
    KEY03 = 0x2DDABB66
    KEY04 = 0x2DDABB67
    KEY1 = 0x0A1EFB92
    KEY2 = 0x0A1EFB93
    KEY3 = 0x0A1EFB94
    KEY4 = 0x0A1EFB95
    KEY5 = 0x0A1EFB96


class Warpgates(Enum):
    WARPPOINT = 0xD7341DE8
    WARP_GATE = 0x8B8D6C9B
    WARPGATE_POWERUP = 0xD399D40F


# Snacks are notated nearly exactly as they are in the game, but Space characters are replaced with "__"
class Snacks(Enum):
    BOX__O__SNACKS__UNDER__SWINGER   = 0x3DC34C5A
    BOX__O__SNACKS__UNDER__SWINGER0  = 0x9AF0123E
    BOX__O__SNACKS__UNDER__SWINGER00 = 0x48D955EA
    BOX__OF__SNACKS__01              = 0x19A254BC
    BOX__OF__SNACKS__02              = 0x19A254BD
    BOX__OF__SNACKS__03              = 0x19A254BE
    BOX__OF__SNACKS__04              = 0x19A254BF
    BOX__OF__SNACKS__05              = 0x19A254C0
    BOX__OF__SNACKS__06              = 0x19A254C1
    BOX__OF__SNACKS__07              = 0x19A254C2
    BOX__OF__SNACKS__1               = 0xAE1E8D5A
    BOX__OF__SNACKS__2               = 0xAE1E8D5B
    BOX__OF__SNACKS__3               = 0xAE1E8D5C
    BOX__OF__SNACKS__4               = 0xAE1E8D5D
    BOX__OF__SNACKS__5               = 0xAE1E8D5E
    BOX__OVER__WITCH                 = 0xE1FAF4E8
    BOX1                             = 0x08ECDEF6
    BOX10__SNACKBOX                  = 0x877821AB
    BOX11__SNACKBOX                  = 0x5B4EC30E
    BOX13__SNACKBOX                  = 0x02FC05D4
    BOX2__SNACKBOX                   = 0xC8AB113A
    BOX3__SNACKBOX                   = 0x9C81B29D
    BOX5__SNACKBOX                   = 0x442EF563
    BOX6__SNACKBOX                   = 0x180596C6
    BOX8__SNACKBOX                   = 0xBFB2D98C
    BP_SS03                          = 0xBE2F67E0
    BP_SS04                          = 0xBE2F67E1
    BP_SS05                          = 0xBE2F67E2
    BP_SSBOX01                       = 0x7480B71F
    BP_SSBOX03                       = 0x7480B721
    BP_SSBOX04                       = 0x7480B722
    CLIFF_SSBOX01                    = 0x2A668829
    CLIFF_SSBOX02                    = 0x2A66882A
    CLIFF_SSBOX03                    = 0x2A66882B
    CLIFF_SSBOX04                    = 0x2A66882C
    CLIFF_SSBOX05                    = 0x2A66882D
    CLIFF_SSBOX06                    = 0x2A66882E
    CRATE__1__PRIZE                  = 0xA225F566
    CRATE__2__PRIZE                  = 0x56D8913F
    CRATE__3__PRIZE                  = 0x0B8B2D18
    CRATE__PRIZE__1                  = 0x29CED7DE
    CRATE__PRIZE__10                 = 0x64D876CA
    CRATE__SNACKBOX__1               = 0x90B3757F
    CRATE__SNACKBOX__2               = 0x90B37580
    CRATE__SNACKBOX__3               = 0x90B37581
    CRATE__SNACKBOX__4               = 0x90B37582
    CRATE02__SNACKBOX                = 0x94DF954C
    CRATE03__SNACKBOX                = 0x68B636AF
    CRATE04__SNACKBOX                = 0x3C8CD812
    CRATE06__SNACKBOX                = 0xE43A1AD8
    CRATE07__SNACKBOX                = 0xB810BC3B
    CRATE08__SNACKBOX                = 0x8BE75D9E
    CRATE_SNACK01                    = 0x2C5EAF43
    CRATE_SNACK02                    = 0x2C5EAF44
    CRATE_SNACK03                    = 0x2C5EAF45
    CRATE_SNACK04                    = 0x2C5EAF46
    CRATE_SNACK05                    = 0x2C5EAF47
    CRATE_SNACK06                    = 0x2C5EAF48
    CRATE_SNACK08                    = 0x2C5EAF4A
    CRATE_SNACK09                    = 0x2C5EAF4B
    CRATE_SSBOX07                    = 0x2920E992
    DIG__2__SNACKBOX                 = 0x7433780D
    DIG__2__POWERUP                  = 0x5AE6DE74
    DRYER__SNACKBOX__1               = 0x12E62152
    DRYER__SNACKBOX__2               = 0x12E62153
    EX__CLUE__SNACK__BOX__1          = 0x5D5D7730
    EX__CLUE__SNACK__BOX__2          = 0x5D5D7731
    EX__CLUE__SNACK__BOX__3          = 0x5D5D7732
    EX__CLUE__SNACK__BOX__4          = 0x5D5D7733
    EX__CLUE__SNACK__BOX2            = 0xD7ACAEE7
    EX__CLUE__SNACK__BOX3            = 0xD7ACAEE8
    EX__CLUE__SNACK__BOX5            = 0xD7ACAEEA
    EX__CLUE__SNACKBOX__1            = 0x2E3F1530
    EX__CLUE__SNACKBOX__2            = 0x2E3F1531
    EX__CLUE__SNACKBOX__3            = 0x2E3F1532
    EX__CLUE__SNACKBOX__4            = 0x2E3F1533
    EX__CLUE__SNACKBOX1              = 0x1BB638E6
    EX__CLUE__SNACKBOX2              = 0x1BB638E7
    EX__CLUE__SNACKBOX3              = 0x1BB638E8
    EX__CLUE__SNACKBOX30             = 0x2E3F1EE8
    EX__CLUE__SNACKBOX300            = 0xAA4CD0E8
    EX__CLUE__SNACKBOX3000           = 0x254EE6E8
    EX__CLUE__SNACKBOX4              = 0x1BB638E9
    EX__CLUE__SNACKBOX5              = 0x1BB638EA
    EXCLUE__SNACKBOX__1              = 0xED64A6B6
    FOOD1                            = 0xD76A9FBF
    FOOD11                           = 0x3B8FBEEE
    FOOD12                           = 0x3B8FBEEF
    HIGH__SNACK__BOX                 = 0x4EB043B5
    HIGH__SNACKBOX__1                = 0xA542AA10
    HIGH__SNACKBOX__10               = 0x911D0660
    LASTFLOAT_SS02                   = 0xCD84873F
    LASTFLOAT_SS03                   = 0xCD848740
    LASTFLOAT_SS04                   = 0xCD848741
    NEW__SNACKBOX                    = 0x7BB83B61
    NEW__SNACKBOX__2                 = 0x910489FB
    PLAT04_SS01                      = 0x181491B9
    PLAT04_SS010                     = 0x528691DB
    PLAT04_SS011                     = 0x528691DC
    PLAT04_SS012                     = 0x528691DD
    PLAT04_SS013                     = 0x528691DE
    PLAT06_SS01                      = 0x0F1D289F
    PLAT06_SS010                     = 0xBBEBC98D
    PLAT06_SS011                     = 0xBBEBC98E
    PLAT06_SS012                     = 0xBBEBC98F
    PLAT06_SS013                     = 0xBBEBC990
    REEF_SS01                        = 0x3F115974
    REEF_SS02                        = 0x3F115975
    REEF_SS03                        = 0x3F115976
    REEF_SS04                        = 0x3F115977
    REEF_SS05                        = 0x3F115978
    REEF_SS06                        = 0x3F115979
    REEF_SS07                        = 0x3F11597A
    REEF_SS08                        = 0x3F11597B
    REEF_SS09                        = 0x3F11597C
    REEF_SS10                        = 0x3F1159F6
    REEF_SS11                        = 0x3F1159F7
    REEF_SS12                        = 0x3F1159F8
    REEF_SS13                        = 0x3F1159F9
    REEF_SS14                        = 0x3F1159FA
    REEF_SS15                        = 0x3F1159FB
    S01                              = 0x0015D4AC
    S010                             = 0x0B2BD434
    S011                             = 0x0B2BD435
    S012                             = 0x0B2BD436
    S013                             = 0x0B2BD437
    S014                             = 0x0B2BD438
    S015                             = 0x0B2BD439
    S016                             = 0x0B2BD43A
    S01_AIR                          = 0x27A289E7
    S02                              = 0x0015D4AD
    S020                             = 0x0B2BD4B7
    S021                             = 0x0B2BD4B8
    S022                             = 0x0B2BD4B9
    S023                             = 0x0B2BD4BA
    S024                             = 0x0B2BD4BB
    S025                             = 0x0B2BD4BC
    S027                             = 0x0B2BD4BE
    S029                             = 0x0B2BD4C0
    S02_AIR                          = 0x39304038
    S03                              = 0x0015D4AE
    S030                             = 0x0B2BD53A
    S031                             = 0x0B2BD53B
    S032                             = 0x0B2BD53C
    S033                             = 0x0B2BD53D
    S034                             = 0x0B2BD53E
    S04                              = 0x0015D4AF
    S040                             = 0x0B2BD5BD
    S041                             = 0x0B2BD5BE
    S0411                            = 0xB76E606B
    S0413                            = 0xB76E606D
    S0415                            = 0xB76E606F
    S0417                            = 0xB76E6071
    S04181                           = 0xDD7B5A87
    S04183                           = 0xDD7B5A89
    S04185                           = 0xDD7B5A8B
    S042                             = 0x0B2BD5BF
    S043                             = 0x0B2BD5C0
    S044                             = 0x0B2BD5C1
    S045                             = 0x0B2BD5C2
    S046                             = 0x0B2BD5C3
    S047                             = 0x0B2BD5C4
    S049                             = 0x0B2BD5C6
    S05                              = 0x0015D4B0
    S06                              = 0x0015D4B1
    S07                              = 0x0015D4B2
    S08                              = 0x0015D4B3
    S080                             = 0x0B2BD7C9
    S09                              = 0x0015D4B4
    S090                             = 0x0B2BD84C
    S1                               = 0x00002AAA
    S10                              = 0x0015D52E
    S100                             = 0x0B2C16BA
    S10B                             = 0x0B2C16CC
    S10C                             = 0x0B2C16CD
    S10D                             = 0x0B2C16CE
    S11                              = 0x0015D52F
    S12                              = 0x0015D530
    S121                             = 0x0B2C17C1
    S123                             = 0x0B2C17C3
    S13                              = 0x0015D531
    S130                             = 0x0B2C1843
    S132                             = 0x0B2C1845
    S14                              = 0x0015D532
    S15                              = 0x0015D533
    S16                              = 0x0015D534
    S17                              = 0x0015D535
    S170                             = 0x0B2C1A4F
    S171                             = 0x0B2C1A50
    S172                             = 0x0B2C1A51
    S173                             = 0x0B2C1A52
    S174                             = 0x0B2C1A53
    S18                              = 0x0015D536
    S18B                             = 0x0B2C1AE4
    S19                              = 0x0015D537
    S190                             = 0x0B2C1B55
    S191                             = 0x0B2C1B56
    S192                             = 0x0B2C1B57
    S193                             = 0x0B2C1B58
    S195                             = 0x0B2C1B5A
    S197                             = 0x0B2C1B5C
    S199                             = 0x0B2C1B5E
    S19B                             = 0x0B2C1B67
    S2                               = 0x00002AAB
    S20                              = 0x0015D5B1
    S200                             = 0x0B2C59C3
    S201                             = 0x0B2C59C4
    S202                             = 0x0B2C59C5
    S203                             = 0x0B2C59C6
    S204                             = 0x0B2C59C7
    S205                             = 0x0B2C59C8
    S2061                            = 0xB7B1F20C
    S20611                           = 0x000EDC55
    S206121                          = 0x079AC033
    S2063                            = 0xB7B1F20E
    S2065                            = 0xB7B1F210
    S2067                            = 0xB7B1F212
    S2069                            = 0xB7B1F214
    S20B                             = 0x0B2C59D5
    S20C                             = 0x0B2C59D6
    S20D                             = 0x0B2C59D7
    S21                              = 0x0015D5B2
    S210                             = 0x0B2C5A46
    S211                             = 0x0B2C5A47
    S212                             = 0x0B2C5A48
    S213                             = 0x0B2C5A49
    S214                             = 0x0B2C5A4A
    S215                             = 0x0B2C5A4B
    S22                              = 0x0015D5B3
    S23                              = 0x0015D5B4
    S24                              = 0x0015D5B5
    S25                              = 0x0015D5B6
    S26                              = 0x0015D5B7
    S27                              = 0x0015D5B8
    S28                              = 0x0015D5B9
    S29                              = 0x0015D5BA
    S3                               = 0x00002AAC
    S30                              = 0x0015D634
    S300                             = 0x0B2C9CCC
    S302                             = 0x0B2C9CCE
    S31                              = 0x0015D635
    S310                             = 0x0B2C9D4F
    S311                             = 0x0B2C9D50
    S312                             = 0x0B2C9D51
    S313                             = 0x0B2C9D52
    S314                             = 0x0B2C9D53
    S315                             = 0x0B2C9D54
    S316                             = 0x0B2C9D55
    S317                             = 0x0B2C9D56
    S32                              = 0x0015D636
    S321                             = 0x0B2C9DD3
    S322                             = 0x0B2C9DD4
    S323                             = 0x0B2C9DD5
    S324                             = 0x0B2C9DD6
    S325                             = 0x0B2C9DD7
    S326                             = 0x0B2C9DD8
    S33                              = 0x0015D637
    S330                             = 0x0B2C9E55
    S331                             = 0x0B2C9E56
    S332                             = 0x0B2C9E57
    S333                             = 0x0B2C9E58
    S334                             = 0x0B2C9E59
    S335                             = 0x0B2C9E5A
    S3350                            = 0xB7D5083E
    S3351                            = 0xB7D5083F
    S3352                            = 0xB7D50840
    S3353                            = 0xB7D50841
    S3354                            = 0xB7D50842
    S34                              = 0x0015D638
    S340                             = 0x0B2C9ED8
    S341                             = 0x0B2C9ED9
    S342                             = 0x0B2C9EDA
    S343                             = 0x0B2C9EDB
    S344                             = 0x0B2C9EDC
    S345                             = 0x0B2C9EDD
    S346                             = 0x0B2C9EDE
    S3460                            = 0xB7D54BCA
    S3461                            = 0xB7D54BCB
    S3462                            = 0xB7D54BCC
    S3463                            = 0xB7D54BCD
    S3464                            = 0xB7D54BCE
    S34_COUNT30                      = 0xB81C6EF1
    S36                              = 0x0015D63A
    S37                              = 0x0015D63B
    S38                              = 0x0015D63C
    S39                              = 0x0015D63D
    S4                               = 0x00002AAD
    S40                              = 0x0015D6B7
    S41                              = 0x0015D6B8
    S42                              = 0x0015D6B9
    S43                              = 0x0015D6BA
    S44                              = 0x0015D6BB
    S45                              = 0x0015D6BC
    S450                             = 0x0B2CE264
    S471                             = 0x0B2CE36B
    S472                             = 0x0B2CE36C
    S475                             = 0x0B2CE36F
    S476                             = 0x0B2CE370
    S5                               = 0x00002AAE
    S51                              = 0x0015D73B
    S53                              = 0x0015D73D
    S55                              = 0x0015D73F
    S56                              = 0x0015D740
    S561                             = 0x0B2D25F1
    S563                             = 0x0B2D25F3
    S565                             = 0x0B2D25F5
    S8                               = 0x00002AB1
    S89                              = 0x0015D8CC
    S90                              = 0x0015D946
    S91                              = 0x0015D947
    S92                              = 0x0015D948
    S93                              = 0x0015D949
    S94                              = 0x0015D94A
    S95                              = 0x0015D94B
    S96                              = 0x0015D94C
    S97                              = 0x0015D94D
    S98                              = 0x0015D94E
    S99                              = 0x0015D94F
    SB__UP__TOP1                     = 0xE774B4DC
    SB__UP__TOP2                     = 0xE774B4DD
    SCARE__SNACK__BOX                = 0xF2FCE769
    SLOPE_SS01                       = 0xC961F215
    SLOPE_SS02                       = 0xC961F216
    SLOPE_SS03                       = 0xC961F217
    SLOPE_SS05                       = 0xC961F219
    SLOPE_SS06                       = 0xC961F21A
    SLOPE_SS07                       = 0xC961F21B
    SLOPE_SS09                       = 0xC961F21D
    SLOPE_SS10                       = 0xC961F297
    SLOPE_SSBOX04                    = 0xCAFAF16F
    SLOPE_SSBOX08                    = 0xCAFAF173
    SM100                            = 0xBB50615B
    SM68                             = 0x0B336ED0
    SM69                             = 0x0B336ED1
    SM70                             = 0x0B336F4B
    SM71                             = 0x0B336F4C
    SM72                             = 0x0B336F4D
    SM73                             = 0x0B336F4E
    SM74                             = 0x0B336F4F
    SM75                             = 0x0B336F50
    SM76                             = 0x0B336F51
    SM77                             = 0x0B336F52
    SM78                             = 0x0B336F53
    SM79                             = 0x0B336F54
    SM80                             = 0x0B336FCE
    SM81                             = 0x0B336FCF
    SM82                             = 0x0B336FD0
    SM83                             = 0x0B336FD1
    SM84                             = 0x0B336FD2
    SM85                             = 0x0B336FD3
    SM86                             = 0x0B336FD4
    SM87                             = 0x0B336FD5
    SM88                             = 0x0B336FD6
    SM89                             = 0x0B336FD7
    SM90                             = 0x0B337051
    SM91                             = 0x0B337052
    SM92                             = 0x0B337053
    SM93                             = 0x0B337054
    SM94                             = 0x0B337055
    SM95                             = 0x0B337056
    SM96                             = 0x0B337057
    SM97                             = 0x0B337058
    SM98                             = 0x0B337059
    SM99                             = 0x0B33705A
    SN1                              = 0x0015E406
    SN10                             = 0x0B33AF42
    SN100                            = 0xBB72AEF6
    SN101                            = 0xBB72AEF7
    SN102                            = 0xBB72AEF8
    SN103                            = 0xBB72AEF9
    SN104                            = 0xBB72AEFA
    SN105                            = 0xBB72AEFB
    SN11                             = 0x0B33AF43
    SN12                             = 0x0B33AF44
    SN13                             = 0x0B33AF45
    SN14                             = 0x0B33AF46
    SN15                             = 0x0B33AF47
    SN16                             = 0x0B33AF48
    SN17                             = 0x0B33AF49
    SN18                             = 0x0B33AF4A
    SN19                             = 0x0B33AF4B
    SN2                              = 0x0015E407
    SN20                             = 0x0B33AFC5
    SN21                             = 0x0B33AFC6
    SN22                             = 0x0B33AFC7
    SN23                             = 0x0B33AFC8
    SN24                             = 0x0B33AFC9
    SN25                             = 0x0B33AFCA
    SN26                             = 0x0B33AFCB
    SN27                             = 0x0B33AFCC
    SN28                             = 0x0B33AFCD
    SN29                             = 0x0B33AFCE
    SN3                              = 0x0015E408
    SN30                             = 0x0B33B048
    SN31                             = 0x0B33B049
    SN32                             = 0x0B33B04A
    SN33                             = 0x0B33B04B
    SN34                             = 0x0B33B04C
    SN35                             = 0x0B33B04D
    SN36                             = 0x0B33B04E
    SN37                             = 0x0B33B04F
    SN38                             = 0x0B33B050
    SN39                             = 0x0B33B051
    SN4                              = 0x0015E409
    SN40                             = 0x0B33B0CB
    SN41                             = 0x0B33B0CC
    SN42                             = 0x0B33B0CD
    SN43                             = 0x0B33B0CE
    SN44                             = 0x0B33B0CF
    SN45                             = 0x0B33B0D0
    SN46                             = 0x0B33B0D1
    SN47                             = 0x0B33B0D2
    SN48                             = 0x0B33B0D3
    SN480                            = 0xBB737C29
    SN49                             = 0x0B33B0D4
    SN5                              = 0x0015E40A
    SN50                             = 0x0B33B14E
    SN51                             = 0x0B33B14F
    SN52                             = 0x0B33B150
    SN53                             = 0x0B33B151
    SN54                             = 0x0B33B152
    SN55                             = 0x0B33B153
    SN56                             = 0x0B33B154
    SN57                             = 0x0B33B155
    SN58                             = 0x0B33B156
    SN59                             = 0x0B33B157
    SN6                              = 0x0015E40B
    SN60                             = 0x0B33B1D1
    SN61                             = 0x0B33B1D2
    SN62                             = 0x0B33B1D3
    SN63                             = 0x0B33B1D4
    SN64                             = 0x0B33B1D5
    SN65                             = 0x0B33B1D6
    SN66                             = 0x0B33B1D7
    SN67                             = 0x0B33B1D8
    SN68                             = 0x0B33B1D9
    SN680                            = 0xBB74023B
    SN6800                           = 0xEC5D2461
    SN69                             = 0x0B33B1DA
    SN7                              = 0x0015E40C
    SN70                             = 0x0B33B254
    SN71                             = 0x0B33B255
    SN72                             = 0x0B33B256
    SN73                             = 0x0B33B257
    SN74                             = 0x0B33B258
    SN75                             = 0x0B33B259
    SN76                             = 0x0B33B25A
    SN77                             = 0x0B33B25B
    SN78                             = 0x0B33B25C
    SN79                             = 0x0B33B25D
    SN8                              = 0x0015E40D
    SN80                             = 0x0B33B2D7
    SN81                             = 0x0B33B2D8
    SN82                             = 0x0B33B2D9
    SN83                             = 0x0B33B2DA
    SN84                             = 0x0B33B2DB
    SN840                            = 0xBB748641
    SN841                            = 0xBB748642
    SN842                            = 0xBB748643
    SN843                            = 0xBB748644
    SN844                            = 0xBB748645
    SN845                            = 0xBB748646
    SN846                            = 0xBB748647
    SN847                            = 0xBB748648
    SN85                             = 0x0B33B2DC
    SN86                             = 0x0B33B2DD
    SN87                             = 0x0B33B2DE
    SN88                             = 0x0B33B2DF
    SN89                             = 0x0B33B2E0
    SN9                              = 0x0015E40E
    SN90                             = 0x0B33B35A
    SN91                             = 0x0B33B35B
    SN92                             = 0x0B33B35C
    SN93                             = 0x0B33B35D
    SN94                             = 0x0B33B35E
    SN95                             = 0x0B33B35F
    SN96                             = 0x0B33B360
    SN97                             = 0x0B33B361
    SN98                             = 0x0B33B362
    SN99                             = 0x0B33B363
    SNACK__001                       = 0x5F6E2F4B
    SNACK__0010                      = 0xD5623391
    SNACK__0012                      = 0xD5623393
    SNACK__0013                      = 0xD5623394
    SNACK__01                        = 0x432BD55F
    SNACK__010                       = 0x5F6E2FCD
    SNACK__011                       = 0x5F6E2FCE
    SNACK__0110                      = 0xD562769A
    SNACK__012                       = 0x5F6E2FCF
    SNACK__013                       = 0x5F6E2FD0
    SNACK__014                       = 0x5F6E2FD1
    SNACK__015                       = 0x5F6E2FD2
    SNACK__016                       = 0x5F6E2FD3
    SNACK__017                       = 0x5F6E2FD4
    SNACK__02                        = 0x432BD560
    SNACK__020                       = 0x5F6E3050
    SNACK__021                       = 0x5F6E3051
    SNACK__022                       = 0x5F6E3052
    SNACK__023                       = 0x5F6E3053
    SNACK__024                       = 0x5F6E3054
    SNACK__025                       = 0x5F6E3055
    SNACK__03                        = 0x432BD561
    SNACK__030                       = 0x5F6E30D3
    SNACK__031                       = 0x5F6E30D4
    SNACK__032                       = 0x5F6E30D5
    SNACK__033                       = 0x5F6E30D6
    SNACK__0330                      = 0xD562FDB2
    SNACK__0331                      = 0xD562FDB3
    SNACK__0332                      = 0xD562FDB4
    SNACK__0333                      = 0xD562FDB5
    SNACK__034                       = 0x5F6E30D7
    SNACK__035                       = 0x5F6E30D8
    SNACK__036                       = 0x5F6E30D9
    SNACK__037                       = 0x5F6E30DA
    SNACK__038                       = 0x5F6E30DB
    SNACK__039                       = 0x5F6E30DC
    SNACK__04                        = 0x432BD562
    SNACK__040                       = 0x5F6E3156
    SNACK__041                       = 0x5F6E3157
    SNACK__042                       = 0x5F6E3158
    SNACK__0420                      = 0xD5634038
    SNACK__0421                      = 0xD5634039
    SNACK__0422                      = 0xD563403A
    SNACK__043                       = 0x5F6E3159
    SNACK__044                       = 0x5F6E315A
    SNACK__045                       = 0x5F6E315B
    SNACK__046                       = 0x5F6E315C
    SNACK__047                       = 0x5F6E315D
    SNACK__048                       = 0x5F6E315E
    SNACK__049                       = 0x5F6E315F
    SNACK__05                        = 0x432BD563
    SNACK__050                       = 0x5F6E31D9
    SNACK__051                       = 0x5F6E31DA
    SNACK__052                       = 0x5F6E31DB
    SNACK__053                       = 0x5F6E31DC
    SNACK__054                       = 0x5F6E31DD
    SNACK__055                       = 0x5F6E31DE
    SNACK__056                       = 0x5F6E31DF
    SNACK__06                        = 0x432BD564
    SNACK__060                       = 0x5F6E325C
    SNACK__061                       = 0x5F6E325D
    SNACK__0610                      = 0xD563C5C7
    SNACK__062                       = 0x5F6E325E
    SNACK__063                       = 0x5F6E325F
    SNACK__064                       = 0x5F6E3260
    SNACK__065                       = 0x5F6E3261
    SNACK__066                       = 0x5F6E3262
    SNACK__067                       = 0x5F6E3263
    SNACK__068                       = 0x5F6E3264
    SNACK__07                        = 0x432BD565
    SNACK__070                       = 0x5F6E32DF
    SNACK__071                       = 0x5F6E32E0
    SNACK__072                       = 0x5F6E32E1
    SNACK__0720                      = 0xD5640953
    SNACK__0721                      = 0xD5640954
    SNACK__0722                      = 0xD5640955
    SNACK__073                       = 0x5F6E32E2
    SNACK__07330                     = 0x32310A3B
    SNACK__07331                     = 0x32310A3C
    SNACK__07332                     = 0x32310A3D
    SNACK__07333                     = 0x32310A3E
    SNACK__07334                     = 0x32310A3F
    SNACK__07335                     = 0x32310A40
    SNACK__07336                     = 0x32310A41
    SNACK__074                       = 0x5F6E32E3
    SNACK__075                       = 0x5F6E32E4
    SNACK__076                       = 0x5F6E32E5
    SNACK__077                       = 0x5F6E32E6
    SNACK__078                       = 0x5F6E32E7
    SNACK__079                       = 0x5F6E32E8
    SNACK__0790                      = 0xD5640CE8
    SNACK__0791                      = 0xD5640CE9
    SNACK__0792                      = 0xD5640CEA
    SNACK__0793                      = 0xD5640CEB
    SNACK__0794                      = 0xD5640CEC
    SNACK__08                        = 0x432BD566
    SNACK__080                       = 0x5F6E3362
    SNACK__081                       = 0x5F6E3363
    SNACK__082                       = 0x5F6E3364
    SNACK__083                       = 0x5F6E3365
    SNACK__0830                      = 0xD5644CDF
    SNACK__0831                      = 0xD5644CE0
    SNACK__0832                      = 0xD5644CE1
    SNACK__08320                     = 0x32535753
    SNACK__08321                     = 0x32535754
    SNACK__08322                     = 0x32535755
    SNACK__0833                      = 0xD5644CE2
    SNACK__084                       = 0x5F6E3366
    SNACK__085                       = 0x5F6E3367
    SNACK__09                        = 0x432BD567
    SNACK__090                       = 0x5F6E33E5
    SNACK__091                       = 0x5F6E33E6
    SNACK__092                       = 0x5F6E33E7
    SNACK__093                       = 0x5F6E33E8
    SNACK__094                       = 0x5F6E33E9
    SNACK__095                       = 0x5F6E33EA
    SNACK__096                       = 0x5F6E33EB
    SNACK__1                         = 0xB640D2BB
    SNACK__1__MIL                    = 0x40B0A1E7
    SNACK__10                        = 0x432BD5E1
    SNACK__100                       = 0x5F6E7253
    SNACK__101                       = 0x5F6E7254
    SNACK__102                       = 0x5F6E7255
    SNACK__103                       = 0x5F6E7256
    SNACK__104                       = 0x5F6E7257
    SNACK__105                       = 0x5F6E7258
    SNACK__106                       = 0x5F6E7259
    SNACK__107                       = 0x5F6E725A
    SNACK__108                       = 0x5F6E725B
    SNACK__109                       = 0x5F6E725C
    SNACK__11                        = 0x432BD5E2
    SNACK__110                       = 0x5F6E72D6
    SNACK__111                       = 0x5F6E72D7
    SNACK__112                       = 0x5F6E72D8
    SNACK__113                       = 0x5F6E72D9
    SNACK__1130                      = 0xD584C53B
    SNACK__1131                      = 0xD584C53C
    SNACK__114                       = 0x5F6E72DA
    SNACK__12                        = 0x432BD5E3
    SNACK__120                       = 0x5F6E7359
    SNACK__121                       = 0x5F6E735A
    SNACK__122                       = 0x5F6E735B
    SNACK__123                       = 0x5F6E735C
    SNACK__124                       = 0x5F6E735D
    SNACK__125                       = 0x5F6E735E
    SNACK__126                       = 0x5F6E735F
    SNACK__127                       = 0x5F6E7360
    SNACK__128                       = 0x5F6E7361
    SNACK__129                       = 0x5F6E7362
    SNACK__13                        = 0x432BD5E4
    SNACK__130                       = 0x5F6E73DC
    SNACK__131                       = 0x5F6E73DD
    SNACK__1310                      = 0xD5854A47
    SNACK__132                       = 0x5F6E73DE
    SNACK__133                       = 0x5F6E73DF
    SNACK__1330                      = 0xD5854B4D
    SNACK__1331                      = 0xD5854B4E
    SNACK__1332                      = 0xD5854B4F
    SNACK__1333                      = 0xD5854B50
    SNACK__138                       = 0x5F6E73E4
    SNACK__139                       = 0x5F6E73E5
    SNACK__14                        = 0x432BD5E5
    SNACK__140                       = 0x5F6E745F
    SNACK__141                       = 0x5F6E7460
    SNACK__142                       = 0x5F6E7461
    SNACK__143                       = 0x5F6E7462
    SNACK__144                       = 0x5F6E7463
    SNACK__15                        = 0x432BD5E6
    SNACK__150                       = 0x5F6E74E2
    SNACK__151                       = 0x5F6E74E3
    SNACK__152                       = 0x5F6E74E4
    SNACK__153                       = 0x5F6E74E5
    SNACK__154                       = 0x5F6E74E6
    SNACK__155                       = 0x5F6E74E7
    SNACK__156                       = 0x5F6E74E8
    SNACK__157                       = 0x5F6E74E9
    SNACK__158                       = 0x5F6E74EA
    SNACK__159                       = 0x5F6E74EB
    SNACK__16                        = 0x432BD5E7
    SNACK__160                       = 0x5F6E7565
    SNACK__161                       = 0x5F6E7566
    SNACK__162                       = 0x5F6E7567
    SNACK__163                       = 0x5F6E7568
    SNACK__164                       = 0x5F6E7569
    SNACK__165                       = 0x5F6E756A
    SNACK__17                        = 0x432BD5E8
    SNACK__170                       = 0x5F6E75E8
    SNACK__171                       = 0x5F6E75E9
    SNACK__172                       = 0x5F6E75EA
    SNACK__173                       = 0x5F6E75EB
    SNACK__174                       = 0x5F6E75EC
    SNACK__175                       = 0x5F6E75ED
    SNACK__176                       = 0x5F6E75EE
    SNACK__177                       = 0x5F6E75EF
    SNACK__178                       = 0x5F6E75F0
    SNACK__18                        = 0x432BD5E9
    SNACK__180                       = 0x5F6E766B
    SNACK__181                       = 0x5F6E766C
    SNACK__182                       = 0x5F6E766D
    SNACK__183                       = 0x5F6E766E
    SNACK__184                       = 0x5F6E766F
    SNACK__185                       = 0x5F6E7670
    SNACK__186                       = 0x5F6E7671
    SNACK__187                       = 0x5F6E7672
    SNACK__188                       = 0x5F6E7673
    SNACK__189                       = 0x5F6E7674
    SNACK__19                        = 0x432BD5EA
    SNACK__190                       = 0x5F6E76EE
    SNACK__191                       = 0x5F6E76EF
    SNACK__1910                      = 0xD586DC7D
    SNACK__1911                      = 0xD586DC7E
    SNACK__1912                      = 0xD586DC7F
    SNACK__1913                      = 0xD586DC80
    SNACK__1914                      = 0xD586DC81
    SNACK__1915                      = 0xD586DC82
    SNACK__1916                      = 0xD586DC83
    SNACK__1917                      = 0xD586DC84
    SNACK__1918                      = 0xD586DC85
    SNACK__1919                      = 0xD586DC86
    SNACK__192                       = 0x5F6E76F0
    SNACK__193                       = 0x5F6E76F1
    SNACK__194                       = 0x5F6E76F2
    SNACK__195                       = 0x5F6E76F3
    SNACK__196                       = 0x5F6E76F4
    SNACK__197                       = 0x5F6E76F5
    SNACK__198                       = 0x5F6E76F6
    SNACK__199                       = 0x5F6E76F7
    SNACK__2                         = 0xB640D2BC
    SNACK__20                        = 0X432BD664
    SNACK__200                       = 0x5F6EB55C
    SNACK__201                       = 0x5F6EB55D
    SNACK__202                       = 0x5F6EB55E
    SNACK__203                       = 0x5F6EB55F
    SNACK__2030                      = 0xD5A6CFCD
    SNACK__2031                      = 0xD5A6CFCE
    SNACK__2032                      = 0xD5A6CFCF
    SNACK__2033                      = 0xD5A6CFD0
    SNACK__20340                     = 0x545C5823
    SNACK__203400                    = 0x2B411A19
    SNACK__203401                    = 0x2B411A1A
    SNACK__203402                    = 0x2B411A1B
    SNACK__203403                    = 0x2B411A1C
    SNACK__2034040                   = 0x22505D07
    SNACK__20340400                  = 0x8F1F9AC5
    SNACK__20340401                  = 0x8F1F9AC6
    SNACK__20340402                  = 0x8F1F9AC7
    SNACK__20340403                  = 0x8F1F9AC8
    SNACK__20340404                  = 0x8F1F9AC9
    SNACK__204                       = 0x5F6EB560
    SNACK__21                        = 0x432BD665
    SNACK__210                       = 0x5F6EB5DF
    SNACK__211                       = 0x5F6EB5E0
    SNACK__2110                      = 0xD5A711D0
    SNACK__2112                      = 0xD5A711D2
    SNACK__2114                      = 0xD5A711D4
    SNACK__2116                      = 0xD5A711D6
    SNACK__212                       = 0x5F6EB5E1
    SNACK__213                       = 0x5F6EB5E2
    SNACK__214                       = 0x5F6EB5E3
    SNACK__2140                      = 0xD5A71359
    SNACK__21400                     = 0x547EE6BB
    SNACK__21401                     = 0x547EE6BC
    SNACK__21402                     = 0x547EE6BD
    SNACK__21403                     = 0x547EE6BE
    SNACK__21404                     = 0x547EE6BF
    SNACK__216                       = 0x5F6EB5E5
    SNACK__217                       = 0x5F6EB5E6
    SNACK__22                        = 0x432BD666
    SNACK__220                       = 0x5F6EB662
    SNACK__221                       = 0x5F6EB663
    SNACK__2210                      = 0xD5A754D9
    SNACK__2212                      = 0xD5A754DB
    SNACK__2214                      = 0xD5A754DD
    SNACK__2216                      = 0xD5A754DF
    SNACK__2218                      = 0xD5A754E1
    SNACK__222                       = 0x5F6EB664
    SNACK__223                       = 0x5F6EB665
    SNACK__224                       = 0x5F6EB666
    SNACK__226                       = 0x5F6EB668
    SNACK__228                       = 0x5F6EB66A
    SNACK__23                        = 0x432BD667
    SNACK__230                       = 0x5F6EB6E5
    SNACK__231                       = 0x5F6EB6E6
    SNACK__232                       = 0x5F6EB6E7
    SNACK__233                       = 0x5F6EB6E8
    SNACK__24                        = 0x432BD668
    SNACK__243                       = 0x5F6EB76B
    SNACK__244                       = 0x5F6EB76C
    SNACK__245                       = 0x5F6EB76D
    SNACK__246                       = 0x5F6EB76E
    SNACK__25                        = 0X432BD669
    SNACK__250                       = 0x5F6EB7EB
    SNACK__251                       = 0x5F6EB7EC
    SNACK__252                       = 0x5F6EB7ED
    SNACK__2520                      = 0xD5A81E77
    SNACK__2521                      = 0xD5A81E78
    SNACK__2522                      = 0xD5A81E79
    SNACK__25221                     = 0x5507981C
    SNACK__25222                     = 0x5507981D
    SNACK__252220                    = 0x82E2D707
    SNACK__252221                    = 0x82E2D708
    SNACK__252222                    = 0x82E2D709
    SNACK__2522220                   = 0xFA1409CB
    SNACK__2522221                   = 0xFA1409CC
    SNACK__2522222                   = 0xFA1409CD
    SNACK__25222220                  = 0xF8410417
    SNACK__25222221                  = 0xF8410418
    SNACK__25222222                  = 0xF8410419
    SNACK__252222220                 = 0x094518FB
    SNACK__252222221                 = 0x094518FC
    SNACK__252222222                 = 0x094518FD
    SNACK__2523                      = 0xD5A81E7A
    SNACK__253                       = 0x5F6EB7EE
    SNACK__2530                      = 0xD5A81EFA
    SNACK__2531                      = 0xD5A81EFB
    SNACK__2532                      = 0xD5A81EFC
    SNACK__254                       = 0x5F6EB7EF
    SNACK__255                       = 0x5F6EB7F0
    SNACK__256                       = 0x5F6EB7F1
    SNACK__257                       = 0x5F6EB7F2
    SNACK__258                       = 0x5F6EB7F3
    SNACK__259                       = 0x5F6EB7F4
    SNACK__260                       = 0x5F6EB86E
    SNACK__2610                      = 0xD5A860FD
    SNACK__2612                      = 0xD5A860FF
    SNACK__2614                      = 0xD5A86101
    SNACK__2616                      = 0xD5A86103
    SNACK__2618                      = 0xD5A86105
    SNACK__262                       = 0x5F6EB870
    SNACK__2620                      = 0xD5A86180
    SNACK__2622                      = 0xD5A86182
    SNACK__264                       = 0x5F6EB872
    SNACK__266                       = 0x5F6EB874
    SNACK__268                       = 0x5F6EB876
    SNACK__27                        = 0X432BD66B
    SNACK__270                       = 0x5F6EB8F1
    SNACK__271                       = 0x5F6EB8F2
    SNACK__272                       = 0x5F6EB8F3
    SNACK__273                       = 0x5F6EB8F4
    SNACK__274                       = 0x5F6EB8F5
    SNACK__275                       = 0x5F6EB8F6
    SNACK__276                       = 0x5F6EB8F7
    SNACK__277                       = 0x5F6EB8F8
    SNACK__278                       = 0x5F6EB8F9
    SNACK__28                        = 0x432BD66C
    SNACK__280                       = 0x5F6EB974
    SNACK__281                       = 0x5F6EB975
    SNACK__282                       = 0x5F6EB976
    SNACK__283                       = 0x5F6EB977
    SNACK__29                        = 0X432BD66D
    SNACK__292                       = 0x5F6EB9F9
    SNACK__3                         = 0xB640D2BD
    SNACK__30                        = 0x432BD6E7
    SNACK__300                       = 0x5F6EF865
    SNACK__301                       = 0x5F6EF866
    SNACK__3010                      = 0xD5C91C62
    SNACK__3011                      = 0xD5C91C63
    SNACK__3012                      = 0xD5C91C64
    SNACK__3013                      = 0xD5C91C65
    SNACK__3014                      = 0xD5C91C66
    SNACK__302                       = 0x5F6EF867
    SNACK__3020                      = 0xD5C91CE5
    SNACK__3021                      = 0xD5C91CE6
    SNACK__3022                      = 0xD5C91CE7
    SNACK__30220                     = 0x65E9CA65
    SNACK__30221                     = 0x65E9CA66
    SNACK__30222                     = 0x65E9CA67
    SNACK__303                       = 0x5F6EF868
    SNACK__3030                      = 0xD5C91D68
    SNACK__30300                     = 0x65EA0C68
    SNACK__30301                     = 0x65EA0C69
    SNACK__30302                     = 0x65EA0C6A
    SNACK__30303                     = 0x65EA0C6B
    SNACK__304                       = 0x5F6EF869
    SNACK__305                       = 0x5F6EF86A
    SNACK__306                       = 0x5F6EF86B
    SNACK__307                       = 0x5F6EF86C
    SNACK__308                       = 0x5F6EF86D
    SNACK__309                       = 0x5F6EF86E
    SNACK__31                        = 0x432BD6E8
    SNACK__310                       = 0x5F6EF8E8
    SNACK__311                       = 0x5F6EF8E9
    SNACK__312                       = 0x5F6EF8EA
    SNACK__313                       = 0x5F6EF8EB
    SNACK__3130                      = 0xD5C96071
    SNACK__31300                     = 0x660C5A03
    SNACK__31301                     = 0x660C5A04
    SNACK__31302                     = 0x660C5A05
    SNACK__31303                     = 0x660C5A06
    SNACK__313030                    = 0x38521142
    SNACK__313031                    = 0x38521143
    SNACK__313032                    = 0x38521144
    SNACK__313033                    = 0x38521145
    SNACK__314                       = 0x5F6EF8EC
    SNACK__32                        = 0x432BD6E9
    SNACK__320                       = 0x5F6EF96B
    SNACK__321                       = 0x5F6EF96C
    SNACK__3211                      = 0xD5C9A275
    SNACK__3213                      = 0xD5C9A277
    SNACK__322                       = 0x5F6EF96D
    SNACK__3220                      = 0xD5C9A2F7
    SNACK__3221                      = 0xD5C9A2F8
    SNACK__3222                      = 0xD5C9A2F9
    SNACK__32220                     = 0x662E659B
    SNACK__32221                     = 0x662E659C
    SNACK__32222                     = 0x662E659D
    SNACK__322220                    = 0x49BDFF87
    SNACK__322221                    = 0x49BDFF88
    SNACK__322222                    = 0x49BDFF89
    SNACK__323                       = 0x5F6EF96E
    SNACK__325                       = 0x5F6EF970
    SNACK__327                       = 0x5F6EF972
    SNACK__329                       = 0x5F6EF974
    SNACK__33                        = 0x432BD6EA
    SNACK__330                       = 0x5F6EF9EE
    SNACK__331                       = 0x5F6EF9EF
    SNACK__332                       = 0x5F6EF9F0
    SNACK__3320                      = 0xD5C9E600
    SNACK__3321                      = 0xD5C9E601
    SNACK__3322                      = 0xD5C9E602
    SNACK__333                       = 0x5F6EF9F1
    SNACK__334                       = 0x5F6EF9F2
    SNACK__340                       = 0x5F6EFA71
    SNACK__341                       = 0x5F6EFA72
    SNACK__3410                      = 0xD5CA2886
    SNACK__342                       = 0x5F6EFA73
    SNACK__343                       = 0x5F6EFA74
    SNACK__344                       = 0x5F6EFA75
    SNACK__345                       = 0x5F6EFA76
    SNACK__346                       = 0x5F6EFA77
    SNACK__347                       = 0x5F6EFA78
    SNACK__348                       = 0x5F6EFA79
    SNACK__349                       = 0x5F6EFA7A
    SNACK__355                       = 0x5F6EFAF9
    SNACK__3550                      = 0xD5CA6D9B
    SNACK__3552                      = 0xD5CA6D9D
    SNACK__3554                      = 0xD5CA6D9F
    SNACK__3556                      = 0xD5CA6DA1
    SNACK__36                        = 0x432BD6ED
    SNACK__361                       = 0x5F6EFB78
    SNACK__363                       = 0x5F6EFB7A
    SNACK__374                       = 0x5F6EFBFE
    SNACK__380                       = 0x5F6EFC7D
    SNACK__381                       = 0x5F6EFC7E
    SNACK__382                       = 0x5F6EFC7F
    SNACK__383                       = 0x5F6EFC80
    SNACK__390                       = 0x5F6EFD00
    SNACK__391                       = 0x5F6EFD01
    SNACK__392                       = 0x5F6EFD02
    SNACK__393                       = 0x5F6EFD03
    SNACK__4                         = 0xB640D2BE
    SNACK__40                        = 0x432BD76A
    SNACK__41                        = 0x432BD76B
    SNACK__42                        = 0x432BD76C
    SNACK__43                        = 0x432BD76D
    SNACK__5                         = 0xB640D2BF
    SNACK__50                        = 0x432BD7ED
    SNACK__51                        = 0x432BD7EE
    SNACK__52                        = 0x432BD7EF
    SNACK__53                        = 0x432BD7F0
    SNACK__530                       = 0x5F6F8000
    SNACK__531                       = 0x5F6F8001
    SNACK__6                         = 0xB640D2C0
    SNACK__60                        = 0x432BD870
    SNACK__600                       = 0x5F6FC180
    SNACK__602                       = 0x5F6FC182
    SNACK__603                       = 0x5F6FC183
    SNACK__606                       = 0x5F6FC186
    SNACK__608                       = 0x5F6FC188
    SNACK__61                        = 0x432BD76C
    SNACK__666                       = 0x5F6FC498
    SNACK__7                         = 0xB640D2C1
    SNACK__70                        = 0x432BD8F3
    SNACK__700                       = 0x5F700489
    SNACK__701                       = 0x5F70048A
    SNACK__702                       = 0x5F70048B
    SNACK__703                       = 0x5F70048C
    SNACK__704                       = 0x5F70048D
    SNACK__705                       = 0x5F70048E
    SNACK__706                       = 0x5F70048F
    SNACK__71                        = 0x432BD8F4
    SNACK__72                        = 0x432BD8F5
    SNACK__73                        = 0x432BD8F6
    SNACK__74                        = 0x432BD8F7
    SNACK__8                         = 0xB640D2C2
    SNACK__80                        = 0x432BD976
    SNACK__800                       = 0x5F704792
    SNACK__801                       = 0x5F704793
    SNACK__802                       = 0x5F704794
    SNACK__803                       = 0x5F704795
    SNACK__804                       = 0x5F704796
    SNACK__805                       = 0x5F704797
    SNACK__806                       = 0x5F704798
    SNACK__807                       = 0x5F704799
    SNACK__808                       = 0x5F70479A
    SNACK__809                       = 0x5F70479B
    SNACK__81                        = 0x432BD977
    SNACK__9                         = 0xB640D2C3
    SNACK__90                        = 0x432BD9F9
    SNACK__91                        = 0x432BD9FA
    SNACK__BOX__1                    = 0x7168C90A
    SNACK__BOX__1__MILLION           = 0x243EF716
    SNACK__BOX__10                   = 0x089EE04E
    SNACK__BOX__2                    = 0x7168C90B
    SNACK__BOX__BEHIND__MOODY        = 0xD659DFC3
    SNACK__BOX__IN__SECRET           = 0x85D92D10
    SNACK__BOX__LEFT__CORRIDOR       = 0xD4B54FC4
    SNACK__BOX__LEFT__CORRIDOR__2    = 0xEE402A76
    SNACK__BOX__OVER__PIT            = 0x8D92876E
    SNACK__BOX__OVER__PIT__2         = 0x53989D70
    SNACK001                         = 0x433005EF
    SNACK01                          = 0xB640DAEB
    SNACK010                         = 0x43300671
    SNACK011                         = 0x43300672
    SNACK012                         = 0x43300673
    SNACK013                         = 0x43300674
    SNACK014                         = 0x43300675
    SNACK015                         = 0x43300676
    SNACK02                          = 0xB640DAEC
    SNACK020                         = 0x433006F4
    SNACK022                         = 0x433006F6
    SNACK023                         = 0x433006F7
    SNACK03                          = 0xB640DAED
    SNACK030                         = 0x43300777
    SNACK031                         = 0x43300778
    SNACK032                         = 0x43300779
    SNACK040                         = 0x433007FA
    SNACK041                         = 0x433007FB
    SNACK042                         = 0x433007FC
    SNACK043                         = 0x433007FD
    SNACK050                         = 0x4330087D
    SNACK051                         = 0x4330087E
    SNACK052                         = 0x4330087F
    SNACK053                         = 0x43300880
    SNACK0530                        = 0x619459B0
    SNACK05300                       = 0xEEE9E540
    SNACK05301                       = 0xEEE9E541
    SNACK05302                       = 0xEEE9E542
    SNACK07                          = 0xB640DAF1
    SNACK070                         = 0x43300983
    SNACK071                         = 0x43300984
    SNACK08                          = 0xB640DAF2
    SNACK080                         = 0x43300A06
    SNACK081                         = 0x43300A07
    SNACK082                         = 0x43300A08
    SNACK083                         = 0x43300A09
    SNACK09                          = 0xB640DAF3
    SNACK090                         = 0x43300A89
    SNACK091                         = 0x43300A8A
    SNACK092                         = 0x43300A8B
    SNACK093                         = 0x43300A8C
    SNACK0930                        = 0x619565D4
    SNACK09300                       = 0xEF731BAC
    SNACK09301                       = 0xEF731BAD
    SNACK09303                       = 0xEF731BAF
    SNACK09304                       = 0xEF731BB0
    SNACK09305                       = 0xEF731BB1
    SNACK1                           = 0xEDD9693F
    SNACK10                          = 0xB640DB6D
    SNACK11                          = 0xB640DB6E
    SNACK110                         = 0x4330497A
    SNACK1101                        = 0x61B5999F
    SNACK110101                      = 0xF6971C58
    SNACK110103                      = 0xF6971C5A
    SNACK110105                      = 0xF6971C5C
    SNACK110107                      = 0xF6971C5E
    SNACK110109                      = 0xF6971C60
    SNACK1103                        = 0x61B599A1
    SNACK1105                        = 0x61B599A3
    SNACK1107                        = 0x61B599A5
    SNACK1109                        = 0x61B599A7
    SNACK111                         = 0x4330497B
    SNACK112                         = 0x4330497C
    SNACK1120                        = 0x61B59AA4
    SNACK1121                        = 0x61B59AA5
    SNACK11210                       = 0xFFEE229F
    SNACK11211                       = 0xFFEE22A0
    SNACK1122                        = 0x61B59AA6
    SNACK1123                        = 0x61B59AA7
    SNACK1124                        = 0x61B59AA8
    SNACK1125                        = 0x61B59AA9
    SNACK1126                        = 0x61B59AAA
    SNACK1127                        = 0x61B59AAB
    SNACK1128                        = 0x61B59AAC
    SNACK1129                        = 0x61B59AAD
    SNACK113                         = 0x4330497D
    SNACK114                         = 0x4330497E
    SNACK115                         = 0x4330497F
    SNACK116                         = 0x43304980
    SNACK117                         = 0x43304981
    SNACK118                         = 0x43304982
    SNACK119                         = 0x43304983
    SNACK12                          = 0xB640DB6F
    SNACK120                         = 0x433049FD
    SNACK1200                        = 0x61B5DCA7
    SNACK12010                       = 0x000FEA28
    SNACK12012                       = 0x000FEA2A
    SNACK12014                       = 0x000FEA2C
    SNACK12016                       = 0x000FEA2E
    SNACK12018                       = 0x000FEA30
    SNACK1202                        = 0x61B5DCA9
    SNACK1204                        = 0x61B5DCAB
    SNACK1206                        = 0x61B5DCAD
    SNACK1208                        = 0x61B5DCAF
    SNACK121                         = 0x433049FE
    SNACK122                         = 0x433049FF
    SNACK123                         = 0x43304A00
    SNACK124                         = 0x43304A01
    SNACK125                         = 0x43304A02
    SNACK1271                        = 0x61B5E03D
    SNACK12710                       = 0x0011BF67
    SNACK1272                        = 0x61B5E03E
    SNACK1273                        = 0x61B5E03F
    SNACK1274                        = 0x61B5E040
    SNACK1275                        = 0x61B5E041
    SNACK1276                        = 0x61B5E042
    SNACK1277                        = 0x61B5E043
    SNACK1278                        = 0x61B5E044
    SNACK1279                        = 0x61B5E045
    SNACK13                          = 0xB640DB70
    SNACK130                         = 0x43304A80
    SNACK1300                        = 0x61B61FB0
    SNACK132                         = 0x43304A82
    SNACK133                         = 0x43304A83
    SNACK14                          = 0xB640DB71
    SNACK140                         = 0x43304B03
    SNACK141                         = 0x43304B04
    SNACK142                         = 0x43304B05
    SNACK143                         = 0x43304B06
    SNACK15                          = 0xB640DB72
    SNACK16                          = 0xB640DB73
    SNACK17                          = 0xB640DB74
    SNACK18                          = 0xB640DB75
    SNACK19                          = 0xB640DB76
    SNACK190                         = 0x43304D92
    SNACK191                         = 0x43304D93
    SNACK192                         = 0x43304D94
    SNACK193                         = 0x43304D95
    SNACK194                         = 0x43304D96
    SNACK21                          = 0xB640DBF1
    SNACK210                         = 0x43308C83
    SNACK211                         = 0x43308C84
    SNACK212                         = 0x43308C85
    SNACK213                         = 0x43308C86
    SNACK2130                        = 0x61D7E8C2
    SNACK21300                       = 0x117C1B76
    SNACK21301                       = 0x117C1B77
    SNACK21303                       = 0x117C1B79
    SNACK21304                       = 0x117C1B7A
    SNACK21305                       = 0x117C1B7B
    SNACK240                         = 0x43308E0C
    SNACK241                         = 0x43308E0D
    SNACK242                         = 0x43308E0E
    SNACK243                         = 0x43308E0F
    SNACK26                          = 0xB640DBF6
    SNACK260                         = 0x43308F12
    SNACK261                         = 0x43308F13
    SNACK262                         = 0x43308F14
    SNACK263                         = 0x43308F15
    SNACK264                         = 0x43308F16
    SNACK27                          = 0xB640DBF7
    SNACK270                         = 0x43308F95
    SNACK271                         = 0x43308F96
    SNACK272                         = 0x43308F97
    SNACK273                         = 0x43308F98
    SNACK274                         = 0x43308F99
    SNACK29                          = 0xB640DBF9
    SNACK290                         = 0x4330909B
    SNACK291                         = 0x4330909C
    SNACK293                         = 0x4330909E
    SNACK294                         = 0x4330909F
    SNACK295                         = 0x433090A0
    SNACK296                         = 0x433090A1
    SNACK31                          = 0xB640DC74
    SNACK310                         = 0x4330CF8C
    SNACK311                         = 0x4330CF8D
    SNACK312                         = 0x4330CF8E
    SNACK313                         = 0x4330CF8F
    SNACK314                         = 0x4330CF90
    SNACK315                         = 0x4330CF91
    SNACK32                          = 0xB640DC75
    SNACK320                         = 0x4330D00F
    SNACK321                         = 0x4330D010
    SNACK322                         = 0x4330D011
    SNACK323                         = 0x4330D012
    SNACK324                         = 0x4330D013
    SNACK325                         = 0x4330D014
    SNACK326                         = 0x4330D015
    SNACK33                          = 0xB640DC76
    SNACK330                         = 0x4330D092
    SNACK331                         = 0x4330D093
    SNACK332                         = 0x4330D094
    SNACK333                         = 0x4330D095
    SNACK334                         = 0x4330D096
    SNACK335                         = 0x4330D097
    SNACK35                          = 0xB640DC78
    SNACK36                          = 0xB640DC79
    SNACK360                         = 0x4330D21B
    SNACK361                         = 0x4330D21C
    SNACK362                         = 0x4330D21D
    SNACK363                         = 0x4330D21E
    SNACK364                         = 0x4330D21F
    SNACK365                         = 0x4330D220
    SNACK37                          = 0xB640DC7A
    SNACK370                         = 0x4330D29E
    SNACK371                         = 0x4330D29F
    SNACK372                         = 0x4330D2A0
    SNACK373                         = 0x4330D2A1
    SNACK39                          = 0xB640DC7C
    SNACK390                         = 0x4330D3A4
    SNACK391                         = 0x4330D3A5
    SNACK392                         = 0x4330D3A6
    SNACK393                         = 0x4330D3A7
    SNACK40                          = 0xB640DCF6
    SNACK400                         = 0x43311212
    SNACK401                         = 0x43311213
    SNACK402                         = 0x43311214
    SNACK403                         = 0x43311215
    SNACK404                         = 0x43311216
    SNACK43                          = 0xB640DCF9
    SNACK51                          = 0xB640DD7A
    SNACK52                          = 0xB640DD7B
    SNACK53                          = 0xB640DD7C
    SNACK54                          = 0xB640DD7D
    SNACK55                          = 0xB640DD7E
    SNACK57                          = 0xB640DD80
    SNACK58                          = 0xB640DD81
    SNACK59                          = 0xB640DD82
    SNACK60                          = 0xB640DDFC
    SNACK61                          = 0xB640DDFD
    SNACK62                          = 0xB640DDFE
    SNACK63                          = 0xB640DDFF
    SNACK64                          = 0xB640DE00
    SNACK65                          = 0xB640DE01
    SNACK66                          = 0xB640DE02
    SNACK67                          = 0xB640DE03
    SNACK68                          = 0xB640DE04
    SNACK69                          = 0xB640DE05
    SNACK70                          = 0xB640DE7F
    SNACK71                          = 0xB640DE80
    SNACK72                          = 0xB640DE81
    SNACK73                          = 0xB640DE82
    SNACKBOX                         = 0x4334CC95
    SNACKBOX__0                      = 0x2E6640CD
    SNACKBOX__1                      = 0x2E6640CE
    SNACKBOX__1__1                   = 0x648E41CF
    SNACKBOX__1__10                  = 0x74CBAD1D
    SNACKBOX__1__11                  = 0x74CBAD1E
    SNACKBOX__1__12                  = 0x74CBAD1F
    SNACKBOX__2                      = 0x2E6640CF
    SNACKBOX__2__1                   = 0x648E84D8
    SNACKBOX__2__10                  = 0x74EDFAB8
    SNACKBOX__2__11                  = 0x74EDFAB9
    SNACKBOX__2__12                  = 0x74EDFABA
    SNACKBOX__2ND__LEVEL__1          = 0xC9F5AB9A
    SNACKBOX__2ND__LEVEL__2          = 0xC9F5AB9B
    SNACKBOX__3                      = 0x2E6640D0
    SNACKBOX__3__1                   = 0x648EC7E1
    SNACKBOX__3__10                  = 0x75104853
    SNACKBOX__3__11                  = 0x75104854
    SNACKBOX__3__12                  = 0x75104855
    SNACKBOX__4                      = 0x2E6640D1
    SNACKBOX__4__1                   = 0x648F0AEA
    SNACKBOX__4__10                  = 0x753295EE
    SNACKBOX__4__11                  = 0x753295EF
    SNACKBOX__4__12                  = 0x753295F0
    SNACKBOX__5                      = 0x2E6640D2
    SNACKBOX__CHAND__2               = 0x166AA4F9
    SNACKBOX__FOR__TOKEN2            = 0x249E50CB
    SNACKBOX__FOR__TOKEN3            = 0x249E50CC
    SNACKBOX__FOR__TOKEN4            = 0x249E50CD
    SNACKBOX__FOR__TOKEN5            = 0x249E50CE
    SNACKBOX__SECRET__AREA           = 0xE911A8EE
    SNACKBOX0                        = 0x6404B06F
    SNACKBOX00                       = 0x2E6648FD
    SNACKBOX1                        = 0x6404B070
    SNACKBOX10                       = 0x2E664980
    SNACKBOX11                       = 0x2E664981
    SNACKBOX1MILLION                 = 0xCF7E693C
    SNACKBOX1MILLION1                = 0x2DAFD9E5
    SNACKBOX2                        = 0x6404B071
    SNACKBOX3                        = 0x6404B072
    SNACKBOX30                       = 0x2E664A86
    SNACKBOX5                        = 0x6404B074
    SNACKS__040                      = 0x5278AD8D
    SNACKS__041                      = 0x5278AD8E
    SNACKS__042                      = 0x5278AD8F
    SS__999                          = 0x412F5051
    SS01                             = 0x0B34FDED
    SS010                            = 0xBC1DF077
    SS0100                           = 0x43520D15
    SS0101                           = 0x43520D16
    SS0102                           = 0x43520D17
    SS0103                           = 0x43520D18
    SS0104                           = 0x43520D19
    SS011                            = 0xBC1DF078
    SS0110                           = 0x43520D98
    SS0111                           = 0x43520D99
    SS012                            = 0xBC1DF079
    SS013                            = 0xBC1DF07A
    SS014                            = 0xBC1DF07B
    SS015                            = 0xBC1DF07C
    SS016                            = 0xBC1DF07D
    SS017                            = 0xBC1DF07E
    SS018                            = 0xBC1DF07F
    SS019                            = 0xBC1DF080
    SS01A                            = 0xBC1DF088
    SS01A1                           = 0x435215C9
    SS01A3                           = 0x435215CB
    SS01A5                           = 0x435215CD
    SS01A7                           = 0x435215CF
    SS01B                            = 0xBC1DF089
    SS02                             = 0x0B34FDEE
    SS020                            = 0xBC1DF0FA
    SS021                            = 0xBC1DF0FB
    SS0210                           = 0x435250A1
    SS0211                           = 0x435250A2
    SS022                            = 0xBC1DF0FC
    SS023                            = 0xBC1DF0FD
    SS024                            = 0xBC1DF0FE
    SS025                            = 0xBC1DF0FF
    SS026                            = 0xBC1DF100
    SS027                            = 0xBC1DF101
    SS029                            = 0xBC1DF103
    SS02A                            = 0xBC1DF10B
    SS02A1                           = 0x435258D2
    SS02A3                           = 0x435258D4
    SS02A5                           = 0x435258D6
    SS02A7                           = 0x435258D8
    SS02B                            = 0xBC1DF10C
    SS03                             = 0x0B34FDEF
    SS030                            = 0xBC1DF17D
    SS031                            = 0xBC1DF17E
    SS032                            = 0xBC1DF17F
    SS033                            = 0xBC1DF180
    SS034                            = 0xBC1DF181
    SS035                            = 0xBC1DF182
    SS037                            = 0xBC1DF184
    SS03A                            = 0xBC1DF18E
    SS03B                            = 0xBC1DF18F
    SS03B1                           = 0x43529C5E
    SS03B3                           = 0x43529C60
    SS03B5                           = 0x43529C62
    SS03B7                           = 0x43529C64
    SS04                             = 0x0B34FDF0
    SS040                            = 0xBC1DF200
    SS041                            = 0xBC1DF201
    SS0410                           = 0x4352D6B3
    SS0411                           = 0x4352D6B4
    SS0412                           = 0x4352D6B5
    SS042                            = 0xBC1DF202
    SS043                            = 0xBC1DF203
    SS045                            = 0xBC1DF205
    SS047                            = 0xBC1DF207
    SS048                            = 0xBC1DF208
    SS049                            = 0xBC1DF209
    SS04A                            = 0xBC1DF211
    SS04B                            = 0xBC1DF212
    SS04B1                           = 0x4352DF67
    SS04B3                           = 0x4352DF69
    SS04B5                           = 0x4352DF6B
    SS04B7                           = 0x4352DF6D
    SS05                             = 0x0B34FDF1
    SS050                            = 0xBC1DF283
    SS051                            = 0xBC1DF284
    SS052                            = 0xBC1DF285
    SS053                            = 0xBC1DF286
    SS054                            = 0xBC1DF287
    SS055                            = 0xBC1DF288
    SS057                            = 0xBC1DF28A
    SS058                            = 0xBC1DF28B
    SS05A                            = 0xBC1DF294
    SS05B                            = 0xBC1DF295
    SS06                             = 0x0B34FDF2
    SS061                            = 0xBC1DF307
    SS0610                           = 0x43535CC5
    SS0611                           = 0x43535CC6
    SS06110                          = 0x73A87982
    SS06111                          = 0x73A87983
    SS06112                          = 0x73A87984
    SS061130                         = 0x2F362F3F
    SS061131                         = 0x2F362F40
    SS061132                         = 0x2F362F41
    SS061133                         = 0x2F362F42
    SS0611330                        = 0x28BA2EF6
    SS06113310                       = 0xD7460895
    SS061133100                      = 0x28D6646F
    SS0611331010                     = 0xE5B56580
    SS0611331011                     = 0xE5B56581
    SS0611331012                     = 0xE5B56582
    SS0611331013                     = 0xE5B56583
    SS06113310130                    = 0x8BD2F239
    SS0612                           = 0x43535CC7
    SS0614                           = 0x43535CC9
    SS0615                           = 0x43535CCA
    SS06150                          = 0x73A87B8E
    SS06151                          = 0x73A87B8F
    SS06152                          = 0x73A87B90
    SS06153                          = 0x73A87B91
    SS061530                         = 0x2F373B63
    SS061531                         = 0x2F373B64
    SS061532                         = 0x2F373B65
    SS061533                         = 0x2F373B66
    SS063                            = 0xBC1DF309
    SS064                            = 0xBC1DF30A
    SS065                            = 0xBC1DF30B
    SS066                            = 0xBC1DF30C
    SS067                            = 0xBC1DF30D
    SS068                            = 0xBC1DF30E
    SS069                            = 0xBC1DF30F
    SS06A                            = 0xBC1DF317
    SS06B                            = 0xBC1DF318
    SS07                             = 0x0B34FDF3
    SS070                            = 0xBC1DF389
    SS071                            = 0xBC1DF38A
    SS0711                           = 0x43539FCF
    SS0713                           = 0x43539FD1
    SS0715                           = 0x43539FD3
    SS0717                           = 0x43539FD5
    SS0719                           = 0x43539FD7
    SS072                            = 0xBC1DF38B
    SS0721                           = 0x4353A052
    SS0723                           = 0x4353A054
    SS0725                           = 0x4353A056
    SS073                            = 0xBC1DF38C
    SS075                            = 0xBC1DF38E
    SS077                            = 0xBC1DF390
    SS079                            = 0xBC1DF392
    SS07A                            = 0xBC1DF39A
    SS07B                            = 0xBC1DF39B
    SS08                             = 0x0B34FDF4
    SS080                            = 0xBC1DF40C
    SS081                            = 0xBC1DF40D
    SS08A                            = 0xBC1DF41D
    SS08B                            = 0xBC1DF41E
    SS09                             = 0x0B34FDF5
    SS090                            = 0xBC1DF48F
    SS091                            = 0xBC1DF490
    SS092                            = 0xBC1DF491
    SS093                            = 0xBC1DF492
    SS09A                            = 0xBC1DF4A0
    SS09B                            = 0xBC1DF4A1
    SS1                              = 0x0015E695
    SS10                             = 0x0B34FE6F
    SS100                            = 0xBC1E32FD
    SS1000                           = 0x437417A7
    SS1001                           = 0x437417A8
    SS1002                           = 0x437417A9
    SS10020                          = 0x84681BAB
    SS10021                          = 0x84681BAC
    SS10022                          = 0x84681BAD
    SS1003                           = 0x437417AA
    SS1004                           = 0x437417AB
    SS10040                          = 0x84681CB1
    SS1005                           = 0x437417AC
    SS10050                          = 0x84681D34
    SS10051                          = 0x84681D35
    SS1006                           = 0x437417AD
    SS10060                          = 0x84681DB7
    SS10061                          = 0x84681DB8
    SS1007                           = 0x437417AE
    SS10070                          = 0x84681E3A
    SS10071                          = 0x84681E3B
    SS1008                           = 0x437417AF
    SS10080                          = 0x84681EBD
    SS10081                          = 0x84681EBE
    SS10082                          = 0x84681EBF
    SS10083                          = 0x84681EC0
    SS1009                           = 0x437417B0
    SS10090                          = 0x84681F40
    SS10091                          = 0x84681F41
    SS10092                          = 0x84681F42
    SS10093                          = 0x84681F43
    SS101                            = 0xBC1E32FE
    SS1010                           = 0x4374182A
    SS1011                           = 0x4374182B
    SS1012                           = 0x4374182C
    SS10120                          = 0x84685EB4
    SS10121                          = 0x84685EB5
    SS10122                          = 0x84685EB6
    SS10123                          = 0x84685EB7
    SS10124                          = 0x84685EB8
    SS10125                          = 0x84685EB9
    SS102                            = 0xBC1E32FF
    SS1020                           = 0x437418AD
    SS1021                           = 0x437418AE
    SS1022                           = 0x437418AF
    SS1023                           = 0x437418B0
    SS10230                          = 0x8468A240
    SS10231                          = 0x8468A241
    SS103                            = 0xBC1E3300
    SS1030                           = 0x8468A240
    SS1031                           = 0x8468A241
    SS104                            = 0xBC1E3301
    SS1040                           = 0x437419B3
    SS1041                           = 0x437419B4
    SS1042                           = 0x437419B5
    SS1043                           = 0x437419B6
    SS105                            = 0xBC1E3302
    SS1050                           = 0x43741A36
    SS1051                           = 0x43741A37
    SS1052                           = 0x43741A38
    SS1053                           = 0x43741A39
    SS106                            = 0xBC1E3303
    SS1060                           = 0x43741AB9
    SS1061                           = 0x43741ABA
    SS1062                           = 0x43741ABB
    SS1063                           = 0x43741ABC
    SS1064                           = 0x43741ABD
    SS1065                           = 0x43741ABE
    SS107                            = 0xBC1E3304
    SS1070                           = 0x43741B3C
    SS1071                           = 0x43741B3D
    SS1072                           = 0x43741B3E
    SS108                            = 0xBC1E3305
    SS1080                           = 0x43741BBF
    SS1081                           = 0x43741BC0
    SS1082                           = 0x43741BC1
    SS109                            = 0xBC1E3306
    SS1090                           = 0x43741C42
    SS1091                           = 0x43741C43
    SS1092                           = 0x43741C44
    SS11                             = 0x0B34FE70
    SS110                            = 0xBC1E3380
    SS1100                           = 0x43745AB0
    SS11000                          = 0x848A6840
    SS110000                         = 0xD2D358F0
    SS1100000                        = 0xE2268300
    SS11000000                       = 0xB9B50930
    SS1101                           = 0x43745AB1
    SS1102                           = 0x43745AB2
    SS11020                          = 0x848A6946
    SS11021                          = 0x848A6947
    SS11022                          = 0x848A6948
    SS1103                           = 0x43745AB3
    SS1104                           = 0x43745AB4
    SS1105                           = 0x43745AB5
    SS1106                           = 0x43745AB6
    SS1107                           = 0x43745AB7
    SS1109                           = 0x43745AB9
    SS111                            = 0xBC1E3381
    SS1110                           = 0x43745B33
    SS1111                           = 0x43745B34
    SS1112                           = 0x43745B35
    SS1113                           = 0x43745B36
    SS11131                          = 0x848AACD3
    SS11132                          = 0x848AACD4
    SS11133                          = 0x848AACD5
    SS111330                         = 0xD2F6712F
    SS111331                         = 0xD2F67130
    SS111332                         = 0xD2F67131
    SS111333                         = 0xD2F67132
    SS1113330                        = 0xF41BECC6
    SS1113331                        = 0xF41BECC7
    SS1113332                        = 0xF41BECC8
    SS112                            = 0xBC1E3382
    SS113                            = 0xBC1E3383
    SS114                            = 0xBC1E3384
    SS114_COUNT70                    = 0xD89099C9
    SS115                            = 0xBC1E3385
    SS1150                           = 0x43745D3F
    SS1151                           = 0x43745D40
    SS1152                           = 0x43745D41
    SS1153                           = 0x43745D42
    SS1154                           = 0x43745D43
    SS1155                           = 0x43745D44
    SS1156                           = 0x43745D45
    SS116                            = 0xBC1E3386
    SS1163                           = 0x43745DC5
    SS117                            = 0xBC1E3387
    SS119                            = 0xBC1E3389
    SS11A                            = 0xBC1E3391
    SS12                             = 0x0B34FE71
    SS120                            = 0xBC1E3403
    SS121                            = 0xBC1E3404
    SS1210                           = 0x43749E3C
    SS122                            = 0xBC1E3405
    SS123                            = 0xBC1E3406
    SS1233                           = 0x43749F45
    SS124                            = 0xBC1E3407
    SS1240                           = 0x43749FC5
    SS1241                           = 0x43749FC6
    SS12410                          = 0x84ADC282
    SS124100                         = 0xE4EA88B6
    SS124101                         = 0xE4EA88B7
    SS125                            = 0xBC1E3408
    SS126                            = 0xBC1E3409
    SS128                            = 0xBC1E340B
    SS12A                            = 0xBC1E3414
    SS12B                            = 0xBC1E3415
    SS13                             = 0x0B34FE72
    SS130                            = 0xBC1E3486
    SS131                            = 0xBC1E3487
    SS132                            = 0xBC1E3488
    SS133                            = 0xBC1E3489
    SS134                            = 0xBC1E348A
    SS135                            = 0xBC1E348B
    SS136                            = 0xBC1E348C
    SS13A                            = 0xBC1E3497
    SS13B                            = 0xBC1E3498
    SS14                             = 0x0B34FE73
    SS140                            = 0xBC1E3509
    SS141                            = 0xBC1E350A
    SS142                            = 0xBC1E350B
    SS143                            = 0xBC1E350C
    SS144                            = 0xBC1E350D
    SS145                            = 0xBC1E350E
    SS147                            = 0xBC1E3510
    SS14B                            = 0xBC1E351B
    SS15                             = 0x0B34FE74
    SS150                            = 0xBC1E358C
    SS1500                           = 0x437566D4
    SS150000                         = 0x190A3234
    SS151                            = 0xBC1E358D
    SS1510                           = 0x43756757
    SS152                            = 0xBC1E358E
    SS1520                           = 0x437567DA
    SS153                            = 0xBC1E358F
    SS1530                           = 0x4375685D
    SS154                            = 0xBC1E3590
    SS1540                           = 0x437568E0
    SS155                            = 0xBC1E3591
    SS157                            = 0xBC1E3593
    SS16                             = 0x0B34FE75
    SS160                            = 0xBC1E360F
    SS1600                           = 0x4375A9DD
    SS161                            = 0xBC1E3610
    SS162                            = 0xBC1E3611
    SS16222                          = 0x85367361
    SS163                            = 0xBC1E3612
    SS164                            = 0xBC1E3613
    SS165                            = 0xBC1E3614
    SS167                            = 0xBC1E3616
    SS17                             = 0x0B34FE76
    SS170                            = 0xBC1E3692
    SS1700                           = 0x4375ECE6
    SS171                            = 0xBC1E3693
    SS172                            = 0xBC1E3694
    SS173                            = 0xBC1E3695
    SS174                            = 0xBC1E3696
    SS175                            = 0xBC1E3697
    SS177                            = 0xBC1E3699
    SS18                             = 0x0B34FE77
    SS180                            = 0xBC1E3715
    SS181                            = 0xBC1E3716
    SS1811                           = 0x43763073
    SS182                            = 0xBC1E3717
    SS183                            = 0xBC1E3718
    SS184                            = 0xBC1E3719
    SS185                            = 0xBC1E371A
    SS1851                           = 0x4376327F
    SS1853                           = 0x43763281
    SS1855                           = 0x43763283
    SS1861                           = 0x43763302
    SS1862                           = 0x43763303
    SS1863                           = 0x43763304
    SS187                            = 0xBC1E371C
    SS189                            = 0xBC1E371E
    SS1891                           = 0x4376348B
    SS1893                           = 0x4376348D
    SS1895                           = 0x4376348F
    SS19                             = 0x0B34FE78
    SS190                            = 0xBC1E3798
    SS191                            = 0xBC1E3799
    SS192                            = 0xBC1E379A
    SS1920                           = 0x437673FE
    SS1921                           = 0x437673FF
    SS193                            = 0xBC1E379B
    SS194                            = 0xBC1E379C
    SS195                            = 0xBC1E379D
    SS196                            = 0xBC1E379E
    SS1960                           = 0x4376760A
    SS1961                           = 0x4376760B
    SS1962                           = 0x4376760C
    SS1963                           = 0x4376760D
    SS1964                           = 0x4376760E
    SS1965                           = 0x4376760F
    SS1972                           = 0x4376768F
    SS1974                           = 0x43767691
    SS2                              = 0x0015e696
    SS20                             = 0x0B34FEF2
    SS200                            = 0xBC1E7606
    SS2000                           = 0x43966542
    SS20000                          = 0x95F5D0F6
    SS200000                         = 0xBCC9EE12
    SS2000000                        = 0x9B54D366
    SS20000000                       = 0x7C682D62
    SS200000000                      = 0xA94F3956
    SS201                            = 0xBC1E7607
    SS2010                           = 0x439665C5
    SS2011                           = 0x439665C6
    SS202                            = 0xBC1E7608
    SS203                            = 0xBC1E7609
    SS204                            = 0xBC1E760A
    SS205                            = 0xBC1E760B
    SS206                            = 0xBC1E760C
    SS207                            = 0xBC1E760D
    SS208                            = 0xBC1E760E
    SS209                            = 0xBC1E760F
    SS21                             = 0x0B34FEF3
    SS210                            = 0xBC1E7689
    SS211                            = 0xBC1E768A
    SS212                            = 0xBC1E768B
    SS2120                           = 0x4396A951
    SS2121                           = 0x4396A952
    SS21210                          = 0x9618A526
    SS21211                          = 0x9618A527
    SS21212                          = 0x9618A528
    SS21213                          = 0x9618A529
    SS21214                          = 0x9618A52A
    SS21215                          = 0x9618A52B
    SS21216                          = 0x9618A52C
    SS2122                           = 0x4396A953
    SS2123                           = 0x4396A954
    SS2124                           = 0x4396A955
    SS2126                           = 0x4396A957
    SS2129                           = 0x4396A95A
    SS213                            = 0xBC1E768C
    SS214                            = 0xBC1E768D
    SS215                            = 0xBC1E768E
    SS216                            = 0xBC1E768F
    SS22                             = 0x0B34FEF4
    SS220                            = 0xBC1E770C
    SS221                            = 0xBC1E770D
    SS222                            = 0xBC1E770E
    SS2220                           = 0x4396EC5A
    SS2221                           = 0x4396EC5B
    SS22210                          = 0x963AF2C1
    SS22211                          = 0x963AF2C2
    SS22212                          = 0x963AF2C3
    SS22213                          = 0x963AF2C4
    SS22214                          = 0x963AF2C5
    SS22215                          = 0x963AF2C6
    SS22216                          = 0x963AF2C7
    SS22217                          = 0x963AF2C8
    SS22218                          = 0x963AF2C9
    SS223                            = 0xBC1E770F
    SS224                            = 0xBC1E7710
    SS23                             = 0x0B34FEF5
    SS230                            = 0xBC1E778F
    SS231                            = 0xBC1E7790
    SS233                            = 0xBC1E7792
    SS235                            = 0xBC1E7794
    SS237                            = 0xBC1E7796
    SS24                             = 0x0B34FEF6
    SS240                            = 0xBC1E7812
    SS2400                           = 0x43977166
    SS241                            = 0xBC1E7813
    SS243                            = 0xBC1E7815
    SS245                            = 0xBC1E7817
    SS247                            = 0xBC1E7819
    SS25                             = 0x0B34FEF7
    SS250                            = 0xBC1E7895
    SS251                            = 0xBC1E7896
    SS26                             = 0x0B34FEF8
    SS260                            = 0xBC1E7918
    SS2600                           = 0x4397F778
    SS2601                           = 0x4397F779
    SS2602                           = 0x4397F77A
    SS2603                           = 0x4397F77B
    SS2604                           = 0x4397F77C
    SS2605                           = 0x4397F77D
    SS2606                           = 0x4397F77E
    SS2607                           = 0x4397F77F
    SS261                            = 0xBC1E7919
    SS263                            = 0xBC1E791B
    SS265                            = 0xBC1E791D
    SS267                            = 0xBC1E791F
    SS268                            = 0xBC1E7920
    SS2681                           = 0x4397FB91
    SS2683                           = 0x4397FB93
    SS2685                           = 0x4397FB95
    SS2687                           = 0x4397FB97
    SS27                             = 0x0B34FEF9
    SS270                            = 0xBC1E799B
    SS271                            = 0xBC1E799C
    SS2711                           = 0x43983B05
    SS272                            = 0xBC1E799D
    SS274                            = 0xBC1E799F
    SS275                            = 0xBC1E79A0
    SS28                             = 0x0B34FEFA
    SS280                            = 0xBC1E7A1E
    SS281                            = 0xBC1E7A1F
    SS29                             = 0x0B34FEFB
    SS29300                          = 0x972B5484
    SS293020                         = 0x5B2C40C2
    SS2930210                        = 0xA7A523F9
    SS29302105                       = 0xC98168A0
    SS3                              = 0x0015e697
    SS30                             = 0x0B34FF75
    SS300                            = 0xBC1EB90F
    SS301                            = 0xBC1EB910
    SS3010                           = 0x43B8B360
    SS3011                           = 0x43B8B361
    SS3012                           = 0x43B8B362
    SS3013                           = 0x43B8B363
    SS3014                           = 0x43B8B364
    SS302                            = 0xBC1EB911
    SS303                            = 0xBC1EB912
    SS3030                           = 0x43B8B466
    SS3031                           = 0x43B8B467
    SS3032                           = 0x43B8B468
    SS3033                           = 0x43B8B469
    SS3034                           = 0x43B8B46A
    SS304                            = 0xBC1EB913
    SS305                            = 0xBC1EB914
    SS31                             = 0x0B34FF76
    SS32                             = 0x0B34FF77
    SS33                             = 0x0B34FF78
    SS34                             = 0x0B34FF79
    SS35                             = 0x0B34FF7A
    SS350                            = 0xBC1EBB9E
    SS351                            = 0xBC1EBB9F
    SS352                            = 0xBC1EBBA0
    SS353                            = 0xBC1EBBA1
    SS36                             = 0x0B34FF7B
    SS360                            = 0xBC1EBC21
    SS361                            = 0xBC1EBC22
    SS362                            = 0xBC1EBC23
    SS363                            = 0xBC1EBC24
    SS364                            = 0xBC1EBC25
    SS365                            = 0xBC1EBC26
    SS37                             = 0x0B34FF7C
    SS370                            = 0xBC1EBCA4
    SS371                            = 0xBC1EBCA5
    SS372                            = 0xBC1EBCA6
    SS373                            = 0xBC1EBCA7
    SS38                             = 0x0B34FF7D
    SS380                            = 0xBC1EBD27
    SS381                            = 0xBC1EBD27
    SS382                            = 0xBC1EBD27
    SS383                            = 0xBC1EBD27
    SS384                            = 0xBC1EBD27
    SS385                            = 0xBC1EBD27
    SS386                            = 0xBC1EBD27
    SS387                            = 0xBC1EBD27
    SS39                             = 0x0B34FF7E
    SS4                              = 0x0015e698
    SS40                             = 0x0B34FFF8
    SS400                            = 0xBC1EFC18
    SS401                            = 0xBC1EFC19
    SS4010                           = 0x43DB00FB
    SS4011                           = 0x43DB00FC
    SS40110                          = 0xB9118124
    SS4012                           = 0x43DB00FD
    SS4014                           = 0x43DB00FF
    SS4015                           = 0x43DB0100
    SS4016                           = 0x43DB0101
    SS402                            = 0xBC1EFC1A
    SS403                            = 0xBC1EFC1B
    SS4030                           = 0x43DB0201
    SS40300                          = 0xB91206B3
    SS40301                          = 0xB91206B4
    SS40302                          = 0xB91206B5
    SS40303                          = 0xB91206B6
    SS40304                          = 0xB91206B7
    SS40305                          = 0xB91206B8
    SS40306                          = 0xB91206B9
    SS40307                          = 0xB91206BA
    SS40308                          = 0xB91206BB
    SS40309                          = 0xB91206BC
    SS404                            = 0xBC1EFC1C
    SS405                            = 0xBC1EFC1D
    SS406                            = 0xBC1EFC1E
    SS407                            = 0xBC1EFC1F
    SS408                            = 0xBC1EFC20
    SS409                            = 0xBC1EFC21
    SS41                             = 0x0B34FFF9
    SS42                             = 0x0B34FFFA
    SS43                             = 0x0B34FFFB
    SS430                            = 0xBC1EFDA1
    SS431                            = 0xBC1EFDA2
    SS4310                           = 0x43DBCA16
    SS4311                           = 0x43DBCA17
    SS43110                          = 0xB97869F5
    SS43111                          = 0xB97869F6
    SS431110                         = 0xE89E3912
    SS44                             = 0x0B34FFFC
    SS45                             = 0x0B34FFFD
    SS46                             = 0x0B34FFFE
    SS47                             = 0x0B34FFFF
    SS470                            = 0xBC1EFFAD
    SS471                            = 0xBC1EFFAE
    SS472                            = 0xBC1EFFAF
    SS473                            = 0xBC1EFFB0
    SS48                             = 0x0B350000
    SS480                            = 0xBC1F0030
    SS481                            = 0xBC1F0031
    SS482                            = 0xBC1F0032
    SS483                            = 0xBC1F0033
    SS484                            = 0xBC1F0034
    SS49                             = 0x0B350001
    SS5                              = 0x0015e699
    SS50                             = 0x0B35007B
    SS500                            = 0xBC1F3F21
    SS501                            = 0xBC1F3F22
    SS502                            = 0xBC1F3F23
    SS503                            = 0xBC1F3F24
    SS504                            = 0xBC1F3F25
    SS5040                           = 0x43FD501F
    SS50400                          = 0xCAA0000D
    SS50401                          = 0xCAA0000E
    SS50402                          = 0xCAA0000F
    SS50403                          = 0xCAA00010
    SS50404                          = 0xCAA00011
    SS50405                          = 0xCAA00012
    SS50406                          = 0xCAA00013
    SS50407                          = 0xCAA00014
    SS50408                          = 0xCAA00015
    SS50409                          = 0xCAA00016
    SS505                            = 0xBC1F3F26
    SS506                            = 0xBC1F3F27
    SS508                            = 0xBC1F3F29
    SS509                            = 0xBC1F3F2A
    SS51                             = 0x0B35007C
    SS511                            = 0xBC1F3FA5
    SS512                            = 0xBC1F3FA6
    SS513                            = 0xBC1F3FA7
    SS52                             = 0x0B35007D
    SS53                             = 0x0B35007E
    SS54                             = 0x0B35007F
    SS541                            = 0xBC1F412E
    SS543_COUNT40                    = 0xD6558D6C
    SS55                             = 0x0B350080
    SS550                            = 0xBC1F41B0
    SS551                            = 0xBC1F41B1
    SS5510                           = 0x43FE9DC3
    SS5511                           = 0x43FE9DC4
    SS5512                           = 0x43FE9DC5
    SS552                            = 0xBC1F41B2
    SS553                            = 0xBC1F41B3
    SS554                            = 0xBC1F41B4
    SS555                            = 0xBC1F41B5
    SS556                            = 0xBC1F41B6
    SS557                            = 0xBC1F41B7
    SS558                            = 0xBC1F41B8
    SS559                            = 0xBC1F41B9
    SS56                             = 0x0B350081
    SS57                             = 0x0B350082
    SS58                             = 0x0B350083
    SS59                             = 0x0B350084
    SS6                              = 0x0015e69A
    SS60                             = 0x0B3500FE
    SS600                            = 0xBC1F822A
    SS6000                           = 0x441F9BAE
    SS601                            = 0xBC1F822B
    SS602                            = 0xBC1F822C
    SS6020                           = 0x441F9CB4
    SS60200                          = 0xDC2D304C
    SS6021                           = 0x441F9CB5
    SS6022                           = 0x441F9CB6
    SS61                             = 0x0B3500FF
    SS610                            = 0xBC1F82AD
    SS62                             = 0x0B350100
    SS63                             = 0x0B350101
    SS64                             = 0x0B350102
    SS65                             = 0x0B350103
    SS650                            = 0xBC1F84B9
    SS651                            = 0xBC1F84BA
    SS652                            = 0xBC1F84BB
    SS66                             = 0x0B350104
    SS67                             = 0x0B350105
    SS68                             = 0x0B350106
    SS69                             = 0x0B350107
    SS690                            = 0xBC1F86C5
    SS691                            = 0xBC1F86C6
    SS692                            = 0xBC1F86C7
    SS7                              = 0x0015e69B
    SS70                             = 0x0B350181
    SS700                            = 0xBC1FC533
    SS7000                           = 0x4441E949
    SS701                            = 0xBC1FC534
    SS702                            = 0xBC1FC535
    SS71                             = 0x0B350182
    SS72                             = 0x0B350183
    SS73                             = 0x0B350184
    SS730                            = 0xBC1FC6BC
    SS732                            = 0xBC1FC6BE
    SS74                             = 0x0B350185
    SS75                             = 0x0B350186
    SS76                             = 0x0B350187
    SS77                             = 0x0B350188
    SS7741                           = 0x4443C095
    SS77411                          = 0xEEAB8C70
    SS77412                          = 0xEEAB8C71
    SS77413                          = 0xEEAB8C72
    SS774130                         = 0x21C8DE86
    SS77414                          = 0xEEAB8C73
    SS78                             = 0x0B350189
    SS79                             = 0x0B35018A
    SS8                              = 0x0015e69C
    SS80                             = 0x0B350204
    SS800                            = 0xBC20083C
    SS801                            = 0xBC20083D
    SS802_COUNT50                    = 0xA26783BD
    SS803                            = 0xBC20083F
    SS804                            = 0xBC200840
    SS805                            = 0xBC200841
    SS81                             = 0x0B350205
    SS82                             = 0x0B350206
    SS83                             = 0x0B350207
    SS84                             = 0x0B350208
    SS85                             = 0x0B350209
    SS850                            = 0xBC200ACB
    SS852                            = 0xBC200ACD
    SS854                            = 0xBC200ACF
    SS86                             = 0x0B35020A
    SS87                             = 0x0B35020B
    SS88                             = 0x0B35020C
    SS89                             = 0x0B35020D
    SS9                              = 0x0015e69D
    SS90                             = 0x0B350287
    SS91                             = 0x0B350288
    SS910                            = 0xBC204BC8
    SS9100                           = 0x4486C788
    SS9101                           = 0x4486C789
    SS9102                           = 0x4486C78A
    SS9103                           = 0x4486C78B
    SS9105                           = 0x4486C78D
    SS9106                           = 0x4486C78E
    SS9107                           = 0x4486C78F
    SS9108                           = 0x4486C790
    SS911                            = 0xBC204BC9
    SS912                            = 0xBC204BCA
    SS913                            = 0xBC204BCB
    SS914                            = 0xBC204BCC
    SS92                             = 0x0B350289
    SS93                             = 0x0B35028A
    SS94                             = 0x0B35028B
    SS95                             = 0x0B35028C
    SS96                             = 0x0B35028D
    SS97                             = 0x0B35028E
    SS98                             = 0x0B35028F
    SS99                             = 0x0B350290
    SS990                            = 0xBC204FE0
    SS991                            = 0xBC204FE1
    SS9910                           = 0x4488E053
    SS9911                           = 0x4488E054
    SS9912                           = 0x4488E055
    SS9913                           = 0x4488E056
    SS9915                           = 0x4488E058
    SS9916                           = 0x4488E059
    SS9918                           = 0x4488E05B
    SS99181                          = 0x120ACEC2
    SS9919                           = 0x4488E05C
    SS992                            = 0xBC204FE2
    SS9921                           = 0x4488E0D7
    SS9923                           = 0x4488E0D9
    SS9925                           = 0x4488E0DB
    SS99251                          = 0x120B1042
    SS993                            = 0xBC204FE3
    SS994                            = 0xBC204FE4
    SS995                            = 0xBC204FE5
    SS996                            = 0xBC204FE6
    SS997                            = 0xBC204FE7
    SS998                            = 0xBC204FE8
    SS999                            = 0xBC204FE9
    SSBOX01                          = 0xB3031534
    SSBOX02                          = 0xB3031535
    SSBOX03                          = 0xB3031536
    SSBOX03_AIR                      = 0x26981191
    SSBOX04                          = 0xB3031537
    SSBOX04_AIR                      = 0x3825C7E2
    SSBOX05                          = 0xB3031538
    SSBOX06                          = 0xB3031539
    SSBOX07                          = 0xB303153A
    SSBOX08                          = 0xB303153B
    SSBOX09                          = 0xB303153C
    SSBOX10                          = 0xB30315B6
    SSBOX11                          = 0xB30315B7
    SSBOX12                          = 0xB30315B8
    SSBOX13                          = 0xB30315B9
    SSBOX14                          = 0xB30315BA
    SSBOX18                          = 0xB30315BE
    SSBOX25                          = 0xB303163E
    SSBOX26                          = 0xB303163F
    SSBOX27                          = 0xB3031640
    SSBOX28                          = 0xB3031641
    SSBOX87                          = 0xB3031952
    SSBOX_GD01A                      = 0xAF517AB7
    SSBOX_GD01B                      = 0xAF517AB8
    SSBOX_GD02A                      = 0xAF517B3A
    SSBOX_GD02B                      = 0xAF517B3B
    SSCONV                           = 0x45E5BA24
    SSCONV1                          = 0xC48E409D
    SSCONV11                         = 0x94CB1088
    SSCONV13                         = 0x94CB108A
    SSCONV15                         = 0x94CB108C
    SSCONV151                        = 0x23E977D5
    SSCONV1511                       = 0x60785230
    SSCONV1513                       = 0x60785232
    SSCONV153                        = 0x23E977D7
    SSCONV155                        = 0x23E977D9
    SSCONV157                        = 0x23E977DB
    SSCONV159                        = 0x23E977DD
    SSCONV3                          = 0xC48E409F
    SSCONV5                          = 0xC48E40A1
    SSCONV7                          = 0xC48E40A3
    SSCONV9                          = 0xC48E40A5
    SSRP01                           = 0x47E879C3
    SSRP010                          = 0xCBF64EF9
    SSRP011                          = 0xCBF64EFA
    SSRP01_BOX                       = 0x1752664F
    SSRP02                           = 0x47E879C4
    SSRP020                          = 0xCBF64F7C
    SSRP021                          = 0xCBF64F7D
    SSRP03                           = 0x47E879C5
    SSRP030                          = 0xCBF64FFF
    SSRP031                          = 0xCBF65000
    SSRP04                           = 0x47E879C6
    SSRP040                          = 0xCBF65082
    SSRP041                          = 0xCBF65083
    SSRP05                           = 0x47E879C7
    SSRP051                          = 0xCBF65106
    SS_BP04                          = 0xAE50B33D
    SS_BP09                          = 0xAE50B342
    SS_BP14                          = 0xAE50B3C0
    SS_BP26                          = 0xAE50B445
    SS_BP28                          = 0xAE50B447
    SS_BP31                          = 0xAE50B4C3
    SS_BP34                          = 0xAE50B4C6
    SS_BP46                          = 0xAE50B54B
    SS_BP55                          = 0xAE50B5CD
    SS_BP64                          = 0xAE50B64F
    SWINGER__SNACK__LINE             = 0xBB80E483
    SWINGER__SNACK__LINE0            = 0xF2F4EF39
    SWINGER__SNACK__LINE00           = 0x53566A5B
    SWINGER__SNACK__LINE1            = 0xF2F4EF3A
    SWINGER__SNACK__LINE10           = 0x53566ADE
    SWINGER__SNACK__LINE100          = 0xA538AFCA
    SWINGER01_SS01                   = 0x73A97170
    SWINGER01_SS010                  = 0x2FB50C80
    SWINGER01_SS011                  = 0x2FB50C81
    SWINGER01_SS012                  = 0x2FB50C82
    SWINGER01_SS013                  = 0x2FB50C83
    SWINGER01_SS014                  = 0x2FB50C84
    SWINGER01_SS015                  = 0x2FB50C85
    SWINGER01_SS016                  = 0x2FB50C86
    SWINGER01_SS017                  = 0x2FB50C87
    SWINGER01_SS018                  = 0x2FB50C88
    SWINGER01_SS019                  = 0x2FB50C89
    SWINGER02_SS01                   = 0x6F2DBCE3
    SWINGER02_SS010                  = 0xE467A859
    SWINGER02_SS011                  = 0xE467A85A
    SWINGER02_SS012                  = 0xE467A85B
    SWINGER02_SS013                  = 0xE467A85C
    SWINGER02_SS014                  = 0xE467A85D
    SWINGER02_SS015                  = 0xE467A85E
    SWINGER02_SS016                  = 0xE467A85F
    SWINGER02_SS017                  = 0xE467A860
    SWINGER02_SS018                  = 0xE467A861
    SWINGER02_SS019                  = 0xE467A862
    SWINGER03_SS01                   = 0x6AB20856
    SWINGER03_SS010                  = 0x991A4432
    SWINGER03_SS011                  = 0x991A4433
    SWINGER03_SS012                  = 0x991A4434
    SWINGER03_SS013                  = 0x991A4435
    SWINGER03_SS014                  = 0x991A4436
    SWINGER03_SS015                  = 0x991A4437
    SWINGER03_SS016                  = 0x991A4438
    SWINGER03_SS017                  = 0x991A4439
    SWINGER03_SS018                  = 0x991A443A
    SWINGER03_SS019                  = 0x991A443B
    SWINGER04_SS01                   = 0x663653C9
    SWINGER04_SS010                  = 0x4DCCE00B
    SWINGER04_SS011                  = 0x4DCCE00C
    SWINGER04_SS012                  = 0x4DCCE00D
    SWINGER04_SS013                  = 0x4DCCE00E
    SWINGER04_SS014                  = 0x4DCCE00F
    SWINGER04_SS015                  = 0x4DCCE010
    SWINGER04_SS016                  = 0x4DCCE011
    SWINGER04_SS017                  = 0x4DCCE012
    SWINGER04_SS018                  = 0x4DCCE013
    SWINGER04_SS019                  = 0x4DCCE014
    SWINGER10_SS01                   = 0x2CD7C1D6
    SWINGER10_SS02                   = 0x2CD7C1D7
    SWINGER10_SS03                   = 0x2CD7C1D8
    SWINGER10_SS04                   = 0x2CD7C1D9
    SWINGER10_SS06                   = 0x2CD7C1DB
    SWINGER10_SS07                   = 0x2CD7C1DC
    SWINGER10_SS08                   = 0x2CD7C1DD
    SWINGER10_SSBOX05                = 0x0A6EC84B
    SWINGER10_SSBOX09                = 0x0A6EC84F
    SWINGER5_SS01                    = 0x6E1FBE36
    SWINGER5_SS02                    = 0x6E1FBE37
    SWINGER5_SS03                    = 0x6E1FBE38
    SWINGER5_SS04                    = 0x6E1FBE39
    SWINGER5_SS06                    = 0x6E1FBE3B
    SWINGER5_SS07                    = 0x6E1FBE3C
    SWINGER5_SSBOX05                 = 0xBCAD766B
    SWINGER6_SS01                    = 0x69A409A9
    SWINGER6_SS02                    = 0x69A409AA
    SWINGER6_SS03                    = 0x69A409AB
    SWINGER6_SS04                    = 0x69A409AC
    SWINGER6_SS06                    = 0x69A409AE
    SWINGER6_SS07                    = 0x69A409AF
    SWINGER6_SSBOX05                 = 0xD5BEBC0C
    SWINGER7_SS01                    = 0x6528551C
    SWINGER7_SS02                    = 0x6528551D
    SWINGER7_SS03                    = 0x6528551E
    SWINGER7_SS04                    = 0x6528551F
    SWINGER7_SS06                    = 0x65285521
    SWINGER7_SS07                    = 0x65285522
    SWINGER7_SSBOX05                 = 0xEED001AD
    SWINGER8_SS01                    = 0x60ACA08F
    SWINGER8_SS02                    = 0x60ACA090
    SWINGER8_SS03                    = 0x60ACA091
    SWINGER8_SS04                    = 0x60ACA092
    SWINGER8_SS06                    = 0x60ACA094
    SWINGER8_SS07                    = 0x60ACA095
    SWINGER8_SSBOX05                 = 0x07E1474E
    SWINGER9_SS01                    = 0x5C30EC02
    SWINGER9_SS02                    = 0x5C30EC03
    SWINGER9_SS03                    = 0x5C30EC04
    SWINGER9_SS04                    = 0x5C30EC05
    SWINGER9_SS06                    = 0x5C30EC07
    SWINGER9_SS07                    = 0x5C30EC08
    SWINGER9_SSBOX05                 = 0x20F28CEF
    TUNNEL__SNACK__BOX               = 0x32F808A5
    UPPERDECK_SSBOX04                = 0x35BD5EFF
    UPPERDECK_SSBOX06                = 0x35BD5F01
    UPPER_SS01                       = 0x4EC52DEE
    UPPER_SS02                       = 0x4EC52DEF
    UPPER_SS03                       = 0x4EC52DF0
    UPPER_SS04                       = 0x4EC52DF1
    UPPER_SS05                       = 0x4EC52DF2
    UPPER_SS06                       = 0x4EC52DF3
    UPPER_SS08                       = 0x4EC52DF5
    UPPER_SS09                       = 0x4EC52DF6
    UPPER_SS10                       = 0x4EC52E70
    URN__1__PRIZE                    = 0x1D62FF04
    URN__2__PRIZE                    = 0xD2159ADD
    CRATE_SANDWICH                   = 0x6049890F
    LOW__BOX                         = 0x3E5DA6E7


base_id = 1495000

UPGRADES_PICKUP_IDS = {
    (base_id + 0): (b'W028', Upgrades.GumPower.value),
    (base_id + 1): (b'B004', Upgrades.SoapPower.value),
    (base_id + 2): (b'O008', Upgrades.BootsPower.value),
    (base_id + 3): (b'P003', Upgrades.PlungerPower.value),
    (base_id + 4): (b'E002', Upgrades.SlippersPower.value),
    (base_id + 5): (b'E002', Upgrades.LampshadePower.value),
    (base_id + 6): (b'R004', Upgrades.BlackKnightPower.value),
    (base_id + 7): (b'F010', Upgrades.SpringPower.value),
    (base_id + 8): (b'L017', Upgrades.PoundPower.value),
    (base_id + 9): (b'E009', Upgrades.HelmetPower.value),
    (base_id + 10): (b'G009', Upgrades.UmbrellaPower.value),
    (base_id + 11): (b'H001', Upgrades.ShovelPower.value),
    (base_id + 12): (b'C007', Upgrades.ShockwavePower.value),
    (base_id + 13): (b'C003', Upgrades.GumPack.value),
    (base_id + 14): (b'L011', Upgrades.GumMaxAmmo.value),
    (base_id + 15): (b'F003', Upgrades.GumUpgrade.value),
    (base_id + 16): (b'S005', Upgrades.GumOverAcid2.value),
    (base_id + 17): (b'O001', Upgrades.Gum_Upgrade.value),
    (base_id + 18): (b'G006', Upgrades.GumPack.value),
    (base_id + 19): (b'R020', Upgrades.BubblePack.value),
    (base_id + 20): (b'E007', Upgrades.SoapBox1.value),
    (base_id + 21): (b'G003', Upgrades.Soap__Box.value),
    (base_id + 22): (b'R005', Upgrades.SoapPack.value),
    (base_id + 23): (b'R021', Upgrades.SoapPack.value),
    (base_id + 24): (b'L019', Upgrades.SoapBox.value),
    (base_id + 25): (b'S005', Upgrades.SoapOverAcid2.value),
    (base_id + 26): (b'W023', Upgrades.SoapBox.value),
    (base_id + 27): (b'F001', Upgrades.Soap_Box.value),
}

MONSTERTOKENS_PICKUP_IDS = {
    (base_id + 100 + 0): (b'O001', MonsterTokens.MT_BLACKKNIGHT.value),
    (base_id + 100 + 1): (b'W022', MonsterTokens.MT_MOODY.value),
    (base_id + 100 + 2): (b'L013', MonsterTokens.MT_CAVEMAN.value),
    (base_id + 100 + 3): (b'O002', MonsterTokens.MT_CREEPER.value),
    (base_id + 100 + 4): (b'H002', MonsterTokens.MT_GARGOYLE.value),
    (base_id + 100 + 5): (b'I005', MonsterTokens.MT_GERONIMO.value),
    (base_id + 100 + 6): (b'G005', MonsterTokens.MT_GHOST.value),
    (base_id + 100 + 7): (b'F007', MonsterTokens.MT_GHOSTDIVER.value),
    (base_id + 100 + 8): (b'C005', MonsterTokens.MT_GREENGHOST.value),
    (base_id + 100 + 9): (b'I001', MonsterTokens.MT_HEADLESS.value),
    (base_id + 100 + 10): (b'S003', MonsterTokens.MT_MASTERMIND.value),
    (base_id + 100 + 11): (b'S002', MonsterTokens.MT_ROBOT.value),
    (base_id + 100 + 12): (b'W025', MonsterTokens.MT_REDBEARD.value),
    (base_id + 100 + 13): (b'G008', MonsterTokens.MT_SCARECROW.value),
    (base_id + 100 + 14): (b'L014', MonsterTokens.MT_SEACREATURE.value),
    (base_id + 100 + 15): (b'B001', MonsterTokens.MT_SPACEKOOK.value),
    (base_id + 100 + 16): (b'F004', MonsterTokens.MT_TARMONSTER.value),
    (base_id + 100 + 17): (b'E003', MonsterTokens.MT_WITCH.value),
    (base_id + 100 + 18): (b'R020', MonsterTokens.MT_WITCHDOC.value),
    (base_id + 100 + 19): (b'E001', MonsterTokens.MT_WOLFMAN.value),
    (base_id + 100 + 20): (b'G002', MonsterTokens.MT_ZOMBIE.value),
}

KEYS_PICKUP_IDS = {
    # +3
    (base_id + 200 + 0): (b'B002', Keys.KEY1.value),
    (base_id + 200 + 1): (b'B002', Keys.KEY2.value),
    (base_id + 200 + 2): (b'B002', Keys.KEY3.value),

    # +4
    (base_id + 200 + 3): (b'B003', Keys.KEY1.value),
    (base_id + 200 + 4): (b'B003', Keys.KEY2.value),
    (base_id + 200 + 5): (b'B003', Keys.KEY3.value),
    (base_id + 200 + 6): (b'B003', Keys.KEY4.value),

    # +5
    (base_id + 200 + 7): (b'C005', Keys.KEY_1.value),
    (base_id + 200 + 8): (b'C005', Keys.KEY_2.value),
    (base_id + 200 + 9): (b'C005', Keys.KEY_3.value),
    (base_id + 200 + 10): (b'C005', Keys.KEY_4.value),

    # +6
    (base_id + 200 + 11): (b'F005', Keys.KEY01.value),
    (base_id + 200 + 12): (b'F005', Keys.KEY02.value),
    (base_id + 200 + 13): (b'F005', Keys.KEY03.value),
    (base_id + 200 + 14): (b'F005', Keys.KEY04.value),

    # +7
    (base_id + 200 + 15): (b'G001', Keys.KEY_01.value),
    (base_id + 200 + 16): (b'G001', Keys.KEY_02.value),
    (base_id + 200 + 17): (b'G001', Keys.KEY_03.value),

    # +8
    (base_id + 200 + 18): (b'G007', Keys.KEY.value),

    # +9
    (base_id + 200 + 19): (b'G009', Keys.KEY_1.value),
    (base_id + 200 + 20): (b'G009', Keys.KEY_2.value),

    # +1
    (base_id + 200 + 21): (b'H001', Keys.HEDGE_KEY.value),

    # +2
    (base_id + 200 + 22): (b'H001', Keys.DUG_FISHING_KEY.value),

    # +0
    (base_id + 200 + 23): (b'I001', Keys.KEY.value),

    # +10
    (base_id + 200 + 24): (b'I003', Keys.DOORKEY.value),

    # +11
    (base_id + 200 + 25): (b'I005', Keys.DOORKEY1.value),
    (base_id + 200 + 26): (b'I005', Keys.DOORKEY2.value),
    (base_id + 200 + 27): (b'I005', Keys.DOORKEY3.value),
    (base_id + 200 + 28): (b'I005', Keys.DOORKEY4.value),

    # +12
    (base_id + 200 + 29): (b'L011', Keys.KEY01.value),
    (base_id + 200 + 30): (b'L011', Keys.KEY02.value),
    (base_id + 200 + 31): (b'L011', Keys.KEY03.value),
    (base_id + 200 + 32): (b'L011', Keys.KEY04.value),

    # +13
    (base_id + 200 + 33): (b'O003', Keys.KEY1.value),
    (base_id + 200 + 34): (b'O003', Keys.KEY2.value),
    (base_id + 200 + 35): (b'O003', Keys.KEY3.value),

    # +14
    (base_id + 200 + 36): (b'O006', Keys.KEY1.value),
    (base_id + 200 + 37): (b'O006', Keys.KEY2.value),
    (base_id + 200 + 38): (b'O006', Keys.KEY3.value),
    (base_id + 200 + 39): (b'O006', Keys.KEY4.value),

    # +15
    (base_id + 200 + 40): (b'P002', Keys.KEY1.value),
    (base_id + 200 + 41): (b'P002', Keys.KEY2.value),
    (base_id + 200 + 42): (b'P002', Keys.KEY3.value),
    (base_id + 200 + 43): (b'P002', Keys.KEY4.value),
    (base_id + 200 + 44): (b'P002', Keys.KEY5.value),

    # +16
    (base_id + 200 + 45): (b'P003', Keys.KEY1.value),
    (base_id + 200 + 46): (b'P003', Keys.KEY2.value),
    (base_id + 200 + 47): (b'P003', Keys.KEY3.value),

    # +17
    (base_id + 200 + 48): (b'P004', Keys.KEY1.value),

    # +18
    (base_id + 200 + 49): (b'P005', Keys.KEY1.value),
    (base_id + 200 + 50): (b'P005', Keys.KEY2.value),
    (base_id + 200 + 51): (b'P005', Keys.KEY3.value),
    (base_id + 200 + 52): (b'P005', Keys.KEY4.value),

    # +19
    (base_id + 200 + 53): (b'R005', Keys.KEY1.value),
    (base_id + 200 + 54): (b'R005', Keys.KEY2.value),
    (base_id + 200 + 55): (b'R005', Keys.KEY3.value),

    # 20
    (base_id + 200 + 56): (b'W027', Keys.KEY01.value),
    (base_id + 200 + 57): (b'W027', Keys.KEY02.value),
    (base_id + 200 + 58): (b'W027', Keys.KEY03.value),
    (base_id + 200 + 59): (b'W027', Keys.KEY04.value),
}

WARPGATE_PICKUP_IDS = {
    (base_id + 300 + 0): (b'B004', Warpgates.WARP_GATE.value),
    (base_id + 300 + 1): (b'C004', Warpgates.WARPPOINT.value),
    (base_id + 300 + 2): (b'E004', Warpgates.WARPPOINT.value),
    (base_id + 300 + 3): (b'E006', Warpgates.WARPPOINT.value),
    (base_id + 300 + 4): (b'E009', Warpgates.WARPPOINT.value),
    (base_id + 300 + 5): (b'F003', Warpgates.WARPPOINT.value),
    (base_id + 300 + 6): (b'F007', Warpgates.WARPPOINT.value),
    (base_id + 300 + 7): (b'O001', Warpgates.WARPPOINT.value),
    (base_id + 300 + 8): (b'G005', Warpgates.WARPPOINT.value),
    (base_id + 300 + 9): (b'G008', Warpgates.WARPPOINT.value),
    (base_id + 300 + 11): (b'I003', Warpgates.WARPPOINT.value),
    (base_id + 300 + 12): (b'I006', Warpgates.WARPPOINT.value),
    (base_id + 300 + 13): (b'L014', Warpgates.WARPPOINT.value),
    (base_id + 300 + 14): (b'L018', Warpgates.WARPPOINT.value),
    (base_id + 300 + 15): (b'O004', Warpgates.WARPPOINT.value),
    (base_id + 300 + 16): (b'O006', Warpgates.WARPPOINT.value),
    (base_id + 300 + 17): (b'P003', Warpgates.WARP_GATE.value),
    (base_id + 300 + 18): (b'P005', Warpgates.WARPPOINT.value),
    (base_id + 300 + 19): (b'R003', Warpgates.WARPPOINT.value),
    (base_id + 300 + 20): (b'S002', Warpgates.WARPPOINT.value),
    (base_id + 300 + 21): (b'W022', Warpgates.WARPPOINT.value),
    (base_id + 300 + 22): (b'W026', Warpgates.WARPPOINT.value),
    (base_id + 300 + 23): (b'L015', Warpgates.WARPPOINT.value),
    (base_id + 300 + 24): (b'G001', Warpgates.WARPPOINT.value),
    (base_id + 300 + 25): (b'H003', Warpgates.WARPGATE_POWERUP.value),
}

SNACK_PICKUP_IDS = {
    (base_id + 400 + 0): (b'B001', Snacks.SS1.value),
    (base_id + 400 + 1): (b'B001', Snacks.SS2.value),
    (base_id + 400 + 2): (b'B001', Snacks.SS3.value),
    (base_id + 400 + 3): (b'B001', Snacks.SS4.value),
    (base_id + 400 + 4): (b'B001', Snacks.SS5.value),
    (base_id + 400 + 5): (b'B001', Snacks.SS6.value),
    (base_id + 400 + 6): (b'B001', Snacks.SS7.value),
    (base_id + 400 + 7): (b'B001', Snacks.SS8.value),
    (base_id + 400 + 8): (b'B001', Snacks.SS9.value),
    (base_id + 400 + 9): (b'B001', Snacks.SS10.value),
    (base_id + 400 + 10): (b'B001', Snacks.SS11.value),
    (base_id + 400 + 11): (b'B001', Snacks.SS12.value),
    (base_id + 400 + 12): (b'B001', Snacks.SS19.value),
    (base_id + 400 + 13): (b'B001', Snacks.SS190.value),
    (base_id + 400 + 14): (b'B001', Snacks.SS191.value),
    (base_id + 400 + 15): (b'B001', Snacks.EX__CLUE__SNACKBOX4.value),
    (base_id + 400 + 16): (b'B001', Snacks.HIGH__SNACKBOX__1.value),
    (base_id + 400 + 17): (b'B001', Snacks.HIGH__SNACKBOX__10.value),
    (base_id + 400 + 18): (b'B001', Snacks.EX__CLUE__SNACKBOX2.value),
    (base_id + 400 + 19): (b'B001', Snacks.EX__CLUE__SNACKBOX3.value),         # Accessed from B003
    (base_id + 400 + 20): (b'B001', Snacks.EX__CLUE__SNACKBOX30.value),
    (base_id + 400 + 21): (b'B001', Snacks.EX__CLUE__SNACKBOX300.value),
    (base_id + 400 + 22): (b'B001', Snacks.EX__CLUE__SNACKBOX3000.value),

    (base_id + 400 + 23): (b'B002', Snacks.SNACK10.value),
    (base_id + 400 + 24): (b'B002', Snacks.SNACK1200.value),
    (base_id + 400 + 25): (b'B002', Snacks.SNACK12.value),
    (base_id + 400 + 26): (b'B002', Snacks.SNACK1202.value),
    (base_id + 400 + 27): (b'B002', Snacks.SNACK14.value),
    (base_id + 400 + 28): (b'B002', Snacks.SNACK1204.value),
    (base_id + 400 + 29): (b'B002', Snacks.SNACK16.value),
    (base_id + 400 + 30): (b'B002', Snacks.SNACK1206.value),
    (base_id + 400 + 31): (b'B002', Snacks.SNACK18.value),
    (base_id + 400 + 32): (b'B002', Snacks.SNACK1208.value),
    (base_id + 400 + 33): (b'B002', Snacks.SNACK110.value),
    (base_id + 400 + 34): (b'B002', Snacks.SNACK12010.value),
    (base_id + 400 + 35): (b'B002', Snacks.SNACK112.value),
    (base_id + 400 + 36): (b'B002', Snacks.SNACK12012.value),
    (base_id + 400 + 37): (b'B002', Snacks.SNACK114.value),
    (base_id + 400 + 38): (b'B002', Snacks.SNACK12014.value),
    (base_id + 400 + 39): (b'B002', Snacks.SNACK116.value),
    (base_id + 400 + 40): (b'B002', Snacks.SNACK12016.value),
    (base_id + 400 + 41): (b'B002', Snacks.SNACK118.value),
    (base_id + 400 + 42): (b'B002', Snacks.SNACK12018.value),
    (base_id + 400 + 43): (b'B002', Snacks.SS4.value),                      # Snacks in the air
    (base_id + 400 + 44): (b'B002', Snacks.EX__CLUE__SNACKBOX__2.value),
    (base_id + 400 + 45): (b'B002', Snacks.SS601.value),
    (base_id + 400 + 46): (b'B002', Snacks.SS60.value),
    (base_id + 400 + 47): (b'B002', Snacks.SS6.value),
    (base_id + 400 + 48): (b'B002', Snacks.SS600.value),
    (base_id + 400 + 49): (b'B002', Snacks.EX__CLUE__SNACKBOX__3.value),
    (base_id + 400 + 50): (b'B002', Snacks.EX__CLUE__SNACKBOX__1.value),

    (base_id + 400 + 51): (b'B003', Snacks.SS513.value),
    (base_id + 400 + 52): (b'B003', Snacks.SS512.value),
    (base_id + 400 + 53): (b'B003', Snacks.SS511.value),
    (base_id + 400 + 54): (b'B003', Snacks.SS5.value),
    (base_id + 400 + 55): (b'B003', Snacks.SS50.value),
    (base_id + 400 + 56): (b'B003', Snacks.SS51.value),
    (base_id + 400 + 57): (b'B003', Snacks.SS52.value),
    (base_id + 400 + 58): (b'B003', Snacks.SS53.value),
    (base_id + 400 + 59): (b'B003', Snacks.SS54.value),
    (base_id + 400 + 60): (b'B003', Snacks.SNACKBOX1MILLION1.value),
    (base_id + 400 + 61): (b'B003', Snacks.SS7741.value),
    (base_id + 400 + 62): (b'B003', Snacks.SS774130.value),
    (base_id + 400 + 63): (b'B003', Snacks.SS77411.value),
    (base_id + 400 + 64): (b'B003', Snacks.SS77412.value),
    (base_id + 400 + 65): (b'B003', Snacks.SS77413.value),
    (base_id + 400 + 66): (b'B003', Snacks.SS77414.value),
    (base_id + 400 + 67): (b'B003', Snacks.SS850.value),
    (base_id + 400 + 68): (b'B003', Snacks.SS852.value),
    (base_id + 400 + 69): (b'B003', Snacks.SS854.value),
    (base_id + 400 + 70): (b'B003', Snacks.SS43.value),
    (base_id + 400 + 71): (b'B003', Snacks.SS36.value),
    (base_id + 400 + 72): (b'B003', Snacks.SS32.value),
    (base_id + 400 + 73): (b'B003', Snacks.SS31.value),
    (base_id + 400 + 74): (b'B003', Snacks.SS30.value),
    (base_id + 400 + 75): (b'B003', Snacks.SS29.value),
    (base_id + 400 + 76): (b'B003', Snacks.SNACKBOX1MILLION.value),
    (base_id + 400 + 77): (b'B003', Snacks.SS__999.value),                  # Helmet Needed
    (base_id + 400 + 78): (b'B003', Snacks.EX__CLUE__SNACKBOX3.value),
    (base_id + 400 + 79): (b'B003', Snacks.SS190.value),
    (base_id + 400 + 80): (b'B003', Snacks.SS191.value),
    (base_id + 400 + 81): (b'B003', Snacks.SS192.value),
    (base_id + 400 + 82): (b'B003', Snacks.EX__CLUE__SNACKBOX5.value),
    (base_id + 400 + 83): (b'B003', Snacks.SS1972.value),
    (base_id + 400 + 84): (b'B003', Snacks.SS1974.value),
    (base_id + 400 + 85): (b'B003', Snacks.EX__CLUE__SNACKBOX4.value),

    (base_id + 400 + 86): (b'B004', Snacks.SS6.value),
    (base_id + 400 + 87): (b'B004', Snacks.SS7.value),
    (base_id + 400 + 88): (b'B004', Snacks.SS70.value),
    (base_id + 400 + 89): (b'B004', Snacks.SS24.value),
    (base_id + 400 + 90): (b'B004', Snacks.SNACKBOX3.value),
    (base_id + 400 + 91): (b'B004', Snacks.SS5.value),
    (base_id + 400 + 92): (b'B004', Snacks.SS1.value),
    (base_id + 400 + 93): (b'B004', Snacks.SS8.value),
    (base_id + 400 + 94): (b'B004', Snacks.SS2400.value),
    (base_id + 400 + 95): (b'B004', Snacks.SS4.value),
    (base_id + 400 + 96): (b'B004', Snacks.SS2.value),
    (base_id + 400 + 97): (b'B004', Snacks.SS3.value),
    (base_id + 400 + 98): (b'B004', Snacks.SNACKBOX5.value),
    (base_id + 400 + 99): (b'B004', Snacks.SS100.value),
    (base_id + 400 + 100): (b'B004', Snacks.SS9.value),
    (base_id + 400 + 101): (b'B004', Snacks.SS10.value),
    (base_id + 400 + 102): (b'B004', Snacks.SNACK10.value),  # Soap Area
    (base_id + 400 + 103): (b'B004', Snacks.SNACK12.value),
    (base_id + 400 + 104): (b'B004', Snacks.SNACK14.value),
    (base_id + 400 + 105): (b'B004', Snacks.SNACK16.value),
    (base_id + 400 + 106): (b'B004', Snacks.SNACK18.value),
    (base_id + 400 + 107): (b'B004', Snacks.SNACK110.value),
    (base_id + 400 + 108): (b'B004', Snacks.SNACK1120.value),
    (base_id + 400 + 109): (b'B004', Snacks.SNACK1122.value),
    (base_id + 400 + 110): (b'B004', Snacks.SNACK1124.value),
    (base_id + 400 + 111): (b'B004', Snacks.SNACK1126.value),
    (base_id + 400 + 112): (b'B004', Snacks.SNACK1128.value),
    (base_id + 400 + 113): (b'B004', Snacks.SNACK11210.value),
    (base_id + 400 + 114): (b'B004', Snacks.SS20.value),
    (base_id + 400 + 115): (b'B004', Snacks.SS21.value),
    (base_id + 400 + 116): (b'B004', Snacks.SS22.value),
    (base_id + 400 + 117): (b'B004', Snacks.SS23.value),
    (base_id + 400 + 118): (b'B004', Snacks.SNACKBOX2.value),
    (base_id + 400 + 119): (b'B004', Snacks.DRYER__SNACKBOX__1.value),
    (base_id + 400 + 120): (b'B004', Snacks.DRYER__SNACKBOX__2.value),

    (base_id + 400 + 121): (b'C001', Snacks.SS2.value),
    (base_id + 400 + 122): (b'C001', Snacks.SS20.value),
    (base_id + 400 + 123): (b'C001', Snacks.SS21.value),
    (base_id + 400 + 124): (b'C001', Snacks.SS42.value),
    (base_id + 400 + 125): (b'C001', Snacks.SS23.value),
    (base_id + 400 + 126): (b'C001', Snacks.SS24.value),
    (base_id + 400 + 127): (b'C001', Snacks.SS3.value),
    (base_id + 400 + 128): (b'C001', Snacks.SS4.value),
    (base_id + 400 + 129): (b'C001', Snacks.SS40.value),
    (base_id + 400 + 130): (b'C001', Snacks.SS41.value),
    (base_id + 400 + 131): (b'C001', Snacks.SNACK__1.value),
    (base_id + 400 + 132): (b'C001', Snacks.SS43.value),
    (base_id + 400 + 133): (b'C001', Snacks.SS44.value),
    (base_id + 400 + 134): (b'C001', Snacks.SS5.value),
    (base_id + 400 + 135): (b'C001', Snacks.SS100.value),
    (base_id + 400 + 136): (b'C001', Snacks.SS1000.value),
    (base_id + 400 + 137): (b'C001', Snacks.SS1001.value),
    (base_id + 400 + 138): (b'C001', Snacks.SS1002.value),
    (base_id + 400 + 139): (b'C001', Snacks.SS1003.value),
    (base_id + 400 + 140): (b'C001', Snacks.SS101.value),
    (base_id + 400 + 141): (b'C001', Snacks.SS102.value),
    (base_id + 400 + 142): (b'C001', Snacks.BOX__OF__SNACKS__3.value),
    (base_id + 400 + 143): (b'C001', Snacks.SS104.value),
    (base_id + 400 + 144): (b'C001', Snacks.SS1040.value),
    (base_id + 400 + 145): (b'C001', Snacks.SS1041.value),
    (base_id + 400 + 146): (b'C001', Snacks.SS1042.value),
    (base_id + 400 + 147): (b'C001', Snacks.SS1043.value),  # Helmet
    (base_id + 400 + 148): (b'C001', Snacks.SS550.value),
    (base_id + 400 + 149): (b'C001', Snacks.SS551.value),
    (base_id + 400 + 150): (b'C001', Snacks.SS552.value),
    (base_id + 400 + 151): (b'C001', Snacks.SS553.value),
    (base_id + 400 + 152): (b'C001', Snacks.SS554.value),
    (base_id + 400 + 153): (b'C001', Snacks.SS555.value),
    (base_id + 400 + 154): (b'C001', Snacks.SS556.value),
    (base_id + 400 + 155): (b'C001', Snacks.SS557.value),
    (base_id + 400 + 156): (b'C001', Snacks.SS558.value),
    (base_id + 400 + 157): (b'C001', Snacks.SS559.value),
    (base_id + 400 + 158): (b'C001', Snacks.SS5510.value),
    (base_id + 400 + 159): (b'C001', Snacks.SS5511.value),
    (base_id + 400 + 160): (b'C001', Snacks.SS5512.value),
    (base_id + 400 + 161): (b'C001', Snacks.SS16.value),
    (base_id + 400 + 162): (b'C001', Snacks.BOX__OF__SNACKS__2.value),
    (base_id + 400 + 163): (b'C001', Snacks.SS19.value),
    (base_id + 400 + 164): (b'C001', Snacks.SS190.value),
    (base_id + 400 + 165): (b'C001', Snacks.SS191.value),
    (base_id + 400 + 166): (b'C001', Snacks.SS192.value),
    (base_id + 400 + 167): (b'C001', Snacks.SS193.value),
    (base_id + 400 + 168): (b'C001', Snacks.SS194.value),
    (base_id + 400 + 169): (b'C001', Snacks.SS195.value),
    (base_id + 400 + 170): (b'C001', Snacks.SS22.value),
    (base_id + 400 + 171): (b'C001', Snacks.SS274.value),
    (base_id + 400 + 172): (b'C001', Snacks.SS275.value),
    (base_id + 400 + 173): (b'C001', Snacks.SS28.value),
    (base_id + 400 + 174): (b'C001', Snacks.SS280.value),
    (base_id + 400 + 175): (b'C001', Snacks.SS29.value),
    (base_id + 400 + 176): (b'C001', Snacks.BOX__OF__SNACKS__4.value),
    (base_id + 400 + 177): (b'C001', Snacks.SS387.value),
    (base_id + 400 + 178): (b'C001', Snacks.SS386.value),
    (base_id + 400 + 179): (b'C001', Snacks.SS385.value),
    (base_id + 400 + 180): (b'C001', Snacks.SS384.value),
    (base_id + 400 + 181): (b'C001', Snacks.SS383.value),
    (base_id + 400 + 182): (b'C001', Snacks.SS382.value),
    (base_id + 400 + 183): (b'C001', Snacks.SS381.value),
    (base_id + 400 + 184): (b'C001', Snacks.SS380.value),
    (base_id + 400 + 185): (b'C001', Snacks.SS38.value),
    (base_id + 400 + 186): (b'C001', Snacks.SS35.value),
    (base_id + 400 + 187): (b'C001', Snacks.SS350.value),
    (base_id + 400 + 188): (b'C001', Snacks.SS351.value),
    (base_id + 400 + 189): (b'C001', Snacks.SS352.value),
    (base_id + 400 + 190): (b'C001', Snacks.SS353.value),
    (base_id + 400 + 191): (b'C001', Snacks.SS36.value),
    (base_id + 400 + 192): (b'C001', Snacks.SS373.value),
    (base_id + 400 + 193): (b'C001', Snacks.SS372.value),
    (base_id + 400 + 194): (b'C001', Snacks.SS371.value),
    (base_id + 400 + 195): (b'C001', Snacks.SS370.value),
    (base_id + 400 + 196): (b'C001', Snacks.SS37.value),
    (base_id + 400 + 197): (b'C001', Snacks.SS1053.value),
    (base_id + 400 + 198): (b'C001', Snacks.SS1052.value),
    (base_id + 400 + 199): (b'C001', Snacks.SS1051.value),
    (base_id + 400 + 200): (b'C001', Snacks.SS1050.value),
    (base_id + 400 + 201): (b'C001', Snacks.SS105.value),

    (base_id + 400 + 202): (b'C002', Snacks.SNACK__01.value),
    (base_id + 400 + 203): (b'C002', Snacks.SNACK__02.value),
    (base_id + 400 + 204): (b'C002', Snacks.SNACK__03.value),
    (base_id + 400 + 205): (b'C002', Snacks.SNACK__04.value),
    (base_id + 400 + 206): (b'C002', Snacks.BOX__OF__SNACKS__1.value),
    (base_id + 400 + 207): (b'C002', Snacks.SNACK__06.value),
    (base_id + 400 + 208): (b'C002', Snacks.SNACK__07.value),
    (base_id + 400 + 209): (b'C002', Snacks.SNACK__08.value),
    (base_id + 400 + 210): (b'C002', Snacks.SNACK__09.value),
    (base_id + 400 + 211): (b'C002', Snacks.SNACK__10.value),
    (base_id + 400 + 212): (b'C002', Snacks.SNACK__112.value),
    (base_id + 400 + 213): (b'C002', Snacks.SNACK__111.value),
    (base_id + 400 + 214): (b'C002', Snacks.SNACK__110.value),
    (base_id + 400 + 215): (b'C002', Snacks.SNACK__11.value),
    (base_id + 400 + 216): (b'C002', Snacks.SNACK__12.value),
    (base_id + 400 + 217): (b'C002', Snacks.SNACK__13.value),
    (base_id + 400 + 218): (b'C002', Snacks.SNACK__14.value),
    (base_id + 400 + 219): (b'C002', Snacks.SNACK__15.value),
    (base_id + 400 + 220): (b'C002', Snacks.SNACK__150.value),
    (base_id + 400 + 221): (b'C002', Snacks.SNACK__151.value),
    (base_id + 400 + 222): (b'C002', Snacks.SNACK__152.value),
    (base_id + 400 + 223): (b'C002', Snacks.SNACK__153.value),
    (base_id + 400 + 224): (b'C002', Snacks.SNACK__154.value),
    (base_id + 400 + 225): (b'C002', Snacks.SNACK__155.value),
    (base_id + 400 + 226): (b'C002', Snacks.SNACK__156.value),
    (base_id + 400 + 227): (b'C002', Snacks.SNACK__157.value),
    (base_id + 400 + 228): (b'C002', Snacks.SNACK__158.value),
    (base_id + 400 + 229): (b'C002', Snacks.SNACK__159.value),
    (base_id + 400 + 230): (b'C002', Snacks.SNACK__165.value),
    (base_id + 400 + 231): (b'C002', Snacks.SNACK__164.value),
    (base_id + 400 + 232): (b'C002', Snacks.SNACK__163.value),
    (base_id + 400 + 233): (b'C002', Snacks.SNACK__162.value),
    (base_id + 400 + 234): (b'C002', Snacks.SNACK__161.value),
    (base_id + 400 + 235): (b'C002', Snacks.SNACK__160.value),
    (base_id + 400 + 236): (b'C002', Snacks.SNACK__16.value),
    (base_id + 400 + 237): (b'C002', Snacks.SNACK__17.value),
    (base_id + 400 + 238): (b'C002', Snacks.SNACK__18.value),
    (base_id + 400 + 239): (b'C002', Snacks.SNACK__19.value),
    (base_id + 400 + 240): (b'C002', Snacks.SNACK__20.value),
    (base_id + 400 + 241): (b'C002', Snacks.BOX__OF__SNACKS__2.value),
    (base_id + 400 + 242): (b'C002', Snacks.SNACK__25.value),
    (base_id + 400 + 243): (b'C002', Snacks.SNACK__250.value),
    (base_id + 400 + 244): (b'C002', Snacks.SNACK__251.value),
    (base_id + 400 + 245): (b'C002', Snacks.SNACK__252.value),
    (base_id + 400 + 246): (b'C002', Snacks.SNACK__253.value),
    (base_id + 400 + 247): (b'C002', Snacks.SNACK__2530.value),
    (base_id + 400 + 248): (b'C002', Snacks.SNACK__2531.value),
    (base_id + 400 + 249): (b'C002', Snacks.SNACK__2532.value),
    (base_id + 400 + 250): (b'C002', Snacks.SNACK__067.value),  # Umbrella
    (base_id + 400 + 251): (b'C002', Snacks.SNACK__060.value),
    (base_id + 400 + 252): (b'C002', Snacks.SNACK__061.value),
    (base_id + 400 + 253): (b'C002', Snacks.SNACK__062.value),
    (base_id + 400 + 254): (b'C002', Snacks.SNACK__063.value),
    (base_id + 400 + 255): (b'C002', Snacks.SNACK__064.value),
    (base_id + 400 + 256): (b'C002', Snacks.SNACK__065.value),
    (base_id + 400 + 257): (b'C002', Snacks.SNACK__066.value),

    (base_id + 400 + 258): (b'C003', Snacks.SNACK__01.value),
    (base_id + 400 + 259): (b'C003', Snacks.SNACK__010.value),
    (base_id + 400 + 260): (b'C003', Snacks.SNACK__011.value),
    (base_id + 400 + 261): (b'C003', Snacks.SNACK__012.value),
    (base_id + 400 + 262): (b'C003', Snacks.SNACK__013.value),
    (base_id + 400 + 263): (b'C003', Snacks.SNACK__014.value),
    (base_id + 400 + 264): (b'C003', Snacks.SNACK__015.value),
    (base_id + 400 + 265): (b'C003', Snacks.SNACK__016.value),
    (base_id + 400 + 266): (b'C003', Snacks.SNACK__017.value),
    (base_id + 400 + 267): (b'C003', Snacks.SNACK__06.value),
    (base_id + 400 + 268): (b'C003', Snacks.SNACK__18.value),
    (base_id + 400 + 269): (b'C003', Snacks.SNACK__19.value),
    (base_id + 400 + 270): (b'C003', Snacks.SNACK__190.value),
    (base_id + 400 + 271): (b'C003', Snacks.SNACK__191.value),
    (base_id + 400 + 272): (b'C003', Snacks.SNACK__192.value),
    (base_id + 400 + 273): (b'C003', Snacks.SNACK__193.value),
    (base_id + 400 + 274): (b'C003', Snacks.BOX__OF__SNACKS__1.value),
    (base_id + 400 + 275): (b'C003', Snacks.SNACK__04.value),
    (base_id + 400 + 276): (b'C003', Snacks.SNACKS__040.value),
    (base_id + 400 + 277): (b'C003', Snacks.SNACKS__041.value),
    (base_id + 400 + 278): (b'C003', Snacks.SNACKS__042.value),
    (base_id + 400 + 279): (b'C003', Snacks.SNACK__05.value),
    (base_id + 400 + 280): (b'C003', Snacks.SNACK__050.value),
    (base_id + 400 + 281): (b'C003', Snacks.SNACK__051.value),
    (base_id + 400 + 282): (b'C003', Snacks.SNACK__052.value),
    (base_id + 400 + 283): (b'C003', Snacks.BOX__OF__SNACKS__2.value),
    (base_id + 400 + 284): (b'C003', Snacks.SNACK__14.value),   # To Button
    (base_id + 400 + 285): (b'C003', Snacks.SNACK__15.value),
    (base_id + 400 + 286): (b'C003', Snacks.SNACK__16.value),
    (base_id + 400 + 287): (b'C003', Snacks.SNACK__17.value),   # End To Button
    (base_id + 400 + 288): (b'C003', Snacks.SNACK__220.value),
    (base_id + 400 + 289): (b'C003', Snacks.SNACK__222.value),
    (base_id + 400 + 290): (b'C003', Snacks.SNACK__224.value),
    (base_id + 400 + 291): (b'C003', Snacks.SNACK__226.value),
    (base_id + 400 + 292): (b'C003', Snacks.SNACK__228.value),
    (base_id + 400 + 293): (b'C003', Snacks.SNACK__2210.value),
    (base_id + 400 + 294): (b'C003', Snacks.SNACK__2212.value),
    (base_id + 400 + 295): (b'C003', Snacks.SNACK__2214.value),
    (base_id + 400 + 296): (b'C003', Snacks.SNACK__2216.value),
    (base_id + 400 + 297): (b'C003', Snacks.SNACK__2218.value),
    (base_id + 400 + 298): (b'C003', Snacks.SNACK__07.value),
    (base_id + 400 + 299): (b'C003', Snacks.SNACK__2116.value),
    (base_id + 400 + 300): (b'C003', Snacks.SNACK__2114.value),
    (base_id + 400 + 301): (b'C003', Snacks.SNACK__2112.value),
    (base_id + 400 + 302): (b'C003', Snacks.SNACK__2110.value),
    (base_id + 400 + 303): (b'C003', Snacks.SNACK__217.value),
    (base_id + 400 + 304): (b'C003', Snacks.SNACK__216.value),
    (base_id + 400 + 305): (b'C003', Snacks.SNACK__214.value),
    (base_id + 400 + 306): (b'C003', Snacks.SNACK__212.value),
    (base_id + 400 + 307): (b'C003', Snacks.SNACK__210.value),
    (base_id + 400 + 308): (b'C003', Snacks.SNACK__246.value),  # Button Ledge
    (base_id + 400 + 309): (b'C003', Snacks.SNACK__245.value),
    (base_id + 400 + 310): (b'C003', Snacks.SNACK__244.value),
    (base_id + 400 + 311): (b'C003', Snacks.SNACK__243.value),
    (base_id + 400 + 312): (b'C003', Snacks.SNACK__231.value),
    (base_id + 400 + 313): (b'C003', Snacks.SNACK__230.value),
    (base_id + 400 + 314): (b'C003', Snacks.SNACK__23.value),
    (base_id + 400 + 315): (b'C003', Snacks.SNACK__1310.value),
    (base_id + 400 + 316): (b'C003', Snacks.SNACK__139.value),
    (base_id + 400 + 317): (b'C003', Snacks.SNACK__138.value),
    (base_id + 400 + 318): (b'C003', Snacks.SNACK__130.value),
    (base_id + 400 + 319): (b'C003', Snacks.SNACK__131.value),
    (base_id + 400 + 320): (b'C003', Snacks.SNACK__132.value),
    (base_id + 400 + 321): (b'C003', Snacks.SNACK__13.value),   # End Button Ledge
    (base_id + 400 + 322): (b'C003', Snacks.BOX__OF__SNACKS__3.value),
    (base_id + 400 + 323): (b'C003', Snacks.SNACK__30.value),
    (base_id + 400 + 324): (b'C003', Snacks.SNACK__300.value),
    (base_id + 400 + 325): (b'C003', Snacks.SNACK__301.value),
    (base_id + 400 + 326): (b'C003', Snacks.SNACK__302.value),
    (base_id + 400 + 327): (b'C003', Snacks.SNACK__303.value),
    (base_id + 400 + 328): (b'C003', Snacks.SNACK__304.value),
    (base_id + 400 + 329): (b'C003', Snacks.SNACK__305.value),
    (base_id + 400 + 330): (b'C003', Snacks.SNACK__306.value),
    (base_id + 400 + 331): (b'C003', Snacks.SNACK__307.value),
    (base_id + 400 + 332): (b'C003', Snacks.SNACK__308.value),
    (base_id + 400 + 333): (b'C003', Snacks.SNACK__309.value),
    (base_id + 400 + 334): (b'C003', Snacks.SNACK__3010.value),
    (base_id + 400 + 335): (b'C003', Snacks.SNACK__3011.value),
    (base_id + 400 + 336): (b'C003', Snacks.SNACK__3012.value),
    (base_id + 400 + 337): (b'C003', Snacks.SNACK__3013.value),
    (base_id + 400 + 338): (b'C003', Snacks.SNACK__3014.value),

    (base_id + 400 + 339): (b'C004', Snacks.SNACK__07.value),
    (base_id + 400 + 340): (b'C004', Snacks.SNACK__071.value),
    (base_id + 400 + 341): (b'C004', Snacks.SNACK__073.value),
    (base_id + 400 + 342): (b'C004', Snacks.SNACK__075.value),
    (base_id + 400 + 343): (b'C004', Snacks.SNACK__076.value),
    (base_id + 400 + 344): (b'C004', Snacks.BOX__OF__SNACKS__01.value),
    (base_id + 400 + 345): (b'C004', Snacks.SNACK__06.value),
    (base_id + 400 + 346): (b'C004', Snacks.SNACK__061.value),
    (base_id + 400 + 347): (b'C004', Snacks.SNACK__064.value),
    (base_id + 400 + 348): (b'C004', Snacks.SNACK__066.value),
    (base_id + 400 + 349): (b'C004', Snacks.SNACK__068.value),
    (base_id + 400 + 350): (b'C004', Snacks.SNACK__0610.value),
    (base_id + 400 + 351): (b'C004', Snacks.SNACK__12.value),
    (base_id + 400 + 352): (b'C004', Snacks.SNACK__121.value),
    (base_id + 400 + 353): (b'C004', Snacks.SNACK__123.value),
    (base_id + 400 + 354): (b'C004', Snacks.SNACK__13.value),
    (base_id + 400 + 355): (b'C004', Snacks.SNACK__14.value),
    (base_id + 400 + 356): (b'C004', Snacks.SNACK__380.value),
    (base_id + 400 + 357): (b'C004', Snacks.SNACK__381.value),
    (base_id + 400 + 358): (b'C004', Snacks.SNACK__382.value),
    (base_id + 400 + 359): (b'C004', Snacks.SNACK__383.value),
    (base_id + 400 + 360): (b'C004', Snacks.SNACK__150.value),
    (base_id + 400 + 361): (b'C004', Snacks.SNACK__151.value),
    (base_id + 400 + 362): (b'C004', Snacks.SNACK__152.value),
    (base_id + 400 + 363): (b'C004', Snacks.SNACK__390.value),
    (base_id + 400 + 364): (b'C004', Snacks.SNACK__391.value),
    (base_id + 400 + 365): (b'C004', Snacks.SNACK__392.value),
    (base_id + 400 + 366): (b'C004', Snacks.SNACK__393.value),
    (base_id + 400 + 367): (b'C004', Snacks.BOX__OF__SNACKS__02.value),
    (base_id + 400 + 368): (b'C004', Snacks.SNACK__171.value),
    (base_id + 400 + 369): (b'C004', Snacks.SNACK__172.value),
    (base_id + 400 + 370): (b'C004', Snacks.SNACK__173.value),
    (base_id + 400 + 371): (b'C004', Snacks.SNACK__174.value),
    (base_id + 400 + 372): (b'C004', Snacks.SNACK__175.value),
    (base_id + 400 + 373): (b'C004', Snacks.SNACK__176.value),
    (base_id + 400 + 374): (b'C004', Snacks.SNACK__177.value),
    (base_id + 400 + 375): (b'C004', Snacks.SNACK__178.value),
    (base_id + 400 + 376): (b'C004', Snacks.SNACK__180.value),
    (base_id + 400 + 377): (b'C004', Snacks.SNACK__182.value),
    (base_id + 400 + 378): (b'C004', Snacks.SNACK__184.value),
    (base_id + 400 + 379): (b'C004', Snacks.SNACK__186.value),
    (base_id + 400 + 380): (b'C004', Snacks.SNACK__188.value),
    (base_id + 400 + 381): (b'C004', Snacks.SNACK__19.value),
    (base_id + 400 + 382): (b'C004', Snacks.BOX__OF__SNACKS__03.value),
    (base_id + 400 + 383): (b'C004', Snacks.SNACK__60.value),    # Umbrella
    (base_id + 400 + 384): (b'C004', Snacks.SNACK__600.value),
    (base_id + 400 + 385): (b'C004', Snacks.SNACK__602.value),
    (base_id + 400 + 386): (b'C004', Snacks.SNACK__603.value),
    (base_id + 400 + 387): (b'C004', Snacks.SNACK__606.value),
    (base_id + 400 + 388): (b'C004', Snacks.SNACK__608.value),
    (base_id + 400 + 389): (b'C004', Snacks.SNACK__70.value),
    (base_id + 400 + 390): (b'C004', Snacks.SNACK__700.value),
    (base_id + 400 + 391): (b'C004', Snacks.SNACK__701.value),
    (base_id + 400 + 392): (b'C004', Snacks.SNACK__702.value),
    (base_id + 400 + 393): (b'C004', Snacks.SNACK__703.value),
    (base_id + 400 + 394): (b'C004', Snacks.SNACK__704.value),
    (base_id + 400 + 395): (b'C004', Snacks.SNACK__705.value),
    (base_id + 400 + 396): (b'C004', Snacks.SNACK__706.value),  # End Umbrella
    (base_id + 400 + 397): (b'C004', Snacks.SNACK__32.value),
    (base_id + 400 + 398): (b'C004', Snacks.SNACK__321.value),
    (base_id + 400 + 399): (b'C004', Snacks.SNACK__323.value),
    (base_id + 400 + 400): (b'C004', Snacks.SNACK__325.value),
    (base_id + 400 + 401): (b'C004', Snacks.SNACK__327.value),
    (base_id + 400 + 402): (b'C004', Snacks.SNACK__329.value),
    (base_id + 400 + 403): (b'C004', Snacks.SNACK__3211.value),
    (base_id + 400 + 404): (b'C004', Snacks.SNACK__3213.value),
    (base_id + 400 + 405): (b'C004', Snacks.SNACK__36.value),
    (base_id + 400 + 406): (b'C004', Snacks.SNACK__361.value),
    (base_id + 400 + 407): (b'C004', Snacks.SNACK__363.value),
    (base_id + 400 + 408): (b'C004', Snacks.SNACK__41.value),
    (base_id + 400 + 409): (b'C004', Snacks.BOX__OF__SNACKS__05.value),
    (base_id + 400 + 410): (b'C004', Snacks.BOX__OF__SNACKS__04.value),
    (base_id + 400 + 411): (b'C004', Snacks.BOX__OF__SNACKS__06.value),
    (base_id + 400 + 412): (b'C004', Snacks.SNACK__260.value),
    (base_id + 400 + 413): (b'C004', Snacks.SNACK__262.value),
    (base_id + 400 + 414): (b'C004', Snacks.SNACK__264.value),
    (base_id + 400 + 415): (b'C004', Snacks.SNACK__266.value),
    (base_id + 400 + 416): (b'C004', Snacks.SNACK__268.value),
    (base_id + 400 + 417): (b'C004', Snacks.SNACK__2610.value),
    (base_id + 400 + 418): (b'C004', Snacks.SNACK__2612.value),
    (base_id + 400 + 419): (b'C004', Snacks.SNACK__2614.value),
    (base_id + 400 + 420): (b'C004', Snacks.SNACK__2616.value),
    (base_id + 400 + 421): (b'C004', Snacks.SNACK__2618.value),
    (base_id + 400 + 422): (b'C004', Snacks.SNACK__2620.value),
    (base_id + 400 + 423): (b'C004', Snacks.SNACK__2622.value),
    (base_id + 400 + 424): (b'C004', Snacks.BOX__OF__SNACKS__07.value),
    (base_id + 400 + 425): (b'C004', Snacks.SNACK__31.value),
    (base_id + 400 + 426): (b'C004', Snacks.SNACK__310.value),
    (base_id + 400 + 427): (b'C004', Snacks.SNACK__311.value),
    (base_id + 400 + 428): (b'C004', Snacks.SNACK__312.value),
    (base_id + 400 + 429): (b'C004', Snacks.SNACK__313.value),
    (base_id + 400 + 430): (b'C004', Snacks.SNACK__3130.value),
    (base_id + 400 + 431): (b'C004', Snacks.SNACK__31300.value),
    (base_id + 400 + 432): (b'C004', Snacks.SNACK__31301.value),
    (base_id + 400 + 433): (b'C004', Snacks.SNACK__31302.value),
    (base_id + 400 + 434): (b'C004', Snacks.SNACK__313030.value),
    (base_id + 400 + 435): (b'C004', Snacks.SNACK__31303.value),
    (base_id + 400 + 436): (b'C004', Snacks.SNACK__313031.value),
    (base_id + 400 + 437): (b'C004', Snacks.SNACK__313032.value),
    (base_id + 400 + 438): (b'C004', Snacks.SNACK__313033.value),
    (base_id + 400 + 439): (b'C004', Snacks.SNACK__355.value),
    (base_id + 400 + 440): (b'C004', Snacks.SNACK__3550.value),
    (base_id + 400 + 441): (b'C004', Snacks.SNACK__3552.value),
    (base_id + 400 + 442): (b'C004', Snacks.SNACK__3554.value),
    (base_id + 400 + 443): (b'C004', Snacks.SNACK__3556.value),
    (base_id + 400 + 444): (b'C004', Snacks.SNACK__340.value),
    (base_id + 400 + 445): (b'C004', Snacks.SNACK__341.value),
    (base_id + 400 + 446): (b'C004', Snacks.SNACK__342.value),
    (base_id + 400 + 447): (b'C004', Snacks.SNACK__343.value),
    (base_id + 400 + 448): (b'C004', Snacks.SNACK__344.value),
    (base_id + 400 + 449): (b'C004', Snacks.SNACK__345.value),
    (base_id + 400 + 450): (b'C004', Snacks.SNACK__346.value),
    (base_id + 400 + 451): (b'C004', Snacks.SNACK__347.value),
    (base_id + 400 + 452): (b'C004', Snacks.SNACK__348.value),
    (base_id + 400 + 453): (b'C004', Snacks.SNACK__349.value),
    (base_id + 400 + 454): (b'C004', Snacks.SNACK__3410.value),

    (base_id + 400 + 456): (b'C005', Snacks.SNACKBOX__1.value),
    (base_id + 400 + 457): (b'C005', Snacks.SNACK__01.value),
    (base_id + 400 + 458): (b'C005', Snacks.SNACK__02.value),
    (base_id + 400 + 459): (b'C005', Snacks.SNACK__03.value),
    (base_id + 400 + 460): (b'C005', Snacks.SNACK__04.value),
    (base_id + 400 + 461): (b'C005', Snacks.SNACK__05.value),
    (base_id + 400 + 462): (b'C005', Snacks.SNACK__06.value),
    (base_id + 400 + 463): (b'C005', Snacks.SNACK__07.value),
    (base_id + 400 + 464): (b'C005', Snacks.SNACK__08.value),
    (base_id + 400 + 465): (b'C005', Snacks.SNACK__09.value),
    (base_id + 400 + 466): (b'C005', Snacks.SNACK__10.value),
    (base_id + 400 + 467): (b'C005', Snacks.SNACK__100.value),
    (base_id + 400 + 468): (b'C005', Snacks.SNACK__101.value),
    (base_id + 400 + 469): (b'C005', Snacks.SNACK__102.value),
    (base_id + 400 + 470): (b'C005', Snacks.SNACK__103.value),
    (base_id + 400 + 471): (b'C005', Snacks.SNACK__104.value),
    (base_id + 400 + 472): (b'C005', Snacks.SNACK__105.value),
    (base_id + 400 + 473): (b'C005', Snacks.SNACK__106.value),
    (base_id + 400 + 474): (b'C005', Snacks.SNACK__107.value),
    (base_id + 400 + 475): (b'C005', Snacks.SNACK__108.value),
    (base_id + 400 + 476): (b'C005', Snacks.SNACK__109.value),
    (base_id + 400 + 477): (b'C005', Snacks.SNACK__12.value),
    (base_id + 400 + 478): (b'C005', Snacks.SNACK__120.value),
    (base_id + 400 + 479): (b'C005', Snacks.SNACK__121.value),
    (base_id + 400 + 480): (b'C005', Snacks.SNACK__122.value),
    (base_id + 400 + 481): (b'C005', Snacks.SNACK__123.value),
    (base_id + 400 + 482): (b'C005', Snacks.SNACK__124.value),
    (base_id + 400 + 483): (b'C005', Snacks.SNACK__125.value),
    (base_id + 400 + 484): (b'C005', Snacks.SNACK__126.value),
    (base_id + 400 + 485): (b'C005', Snacks.SNACK__127.value),
    (base_id + 400 + 486): (b'C005', Snacks.SNACK__128.value),
    (base_id + 400 + 487): (b'C005', Snacks.SNACK__129.value),
    (base_id + 400 + 488): (b'C005', Snacks.SNACKBOX__2.value),
    (base_id + 400 + 489): (b'C005', Snacks.SNACKBOX__3.value),
    (base_id + 400 + 490): (b'C005', Snacks.SNACK__19.value),
    (base_id + 400 + 491): (b'C005', Snacks.SNACK__190.value),
    (base_id + 400 + 492): (b'C005', Snacks.SNACK__191.value),
    (base_id + 400 + 493): (b'C005', Snacks.SNACK__192.value),
    (base_id + 400 + 494): (b'C005', Snacks.SNACK__193.value),
    (base_id + 400 + 495): (b'C005', Snacks.SNACK__194.value),
    (base_id + 400 + 496): (b'C005', Snacks.SNACK__195.value),
    (base_id + 400 + 497): (b'C005', Snacks.SNACK__196.value),
    (base_id + 400 + 498): (b'C005', Snacks.SNACK__197.value),
    (base_id + 400 + 499): (b'C005', Snacks.SNACK__198.value),
    (base_id + 400 + 500): (b'C005', Snacks.SNACK__199.value),
    (base_id + 400 + 501): (b'C005', Snacks.SNACK__1910.value),
    (base_id + 400 + 502): (b'C005', Snacks.SNACK__1911.value),
    (base_id + 400 + 503): (b'C005', Snacks.SNACK__1912.value),
    (base_id + 400 + 504): (b'C005', Snacks.SNACK__1913.value),
    (base_id + 400 + 505): (b'C005', Snacks.SNACK__1914.value),
    (base_id + 400 + 506): (b'C005', Snacks.SNACK__1915.value),
    (base_id + 400 + 507): (b'C005', Snacks.SNACK__1916.value),
    (base_id + 400 + 508): (b'C005', Snacks.SNACK__1917.value),
    (base_id + 400 + 509): (b'C005', Snacks.SNACK__1918.value),
    (base_id + 400 + 510): (b'C005', Snacks.SNACK__1919.value),

    (base_id + 400 + 511): (b'C006', Snacks.SNACK__01.value),
    (base_id + 400 + 512): (b'C006', Snacks.SNACK__010.value),
    (base_id + 400 + 513): (b'C006', Snacks.SNACK__011.value),
    (base_id + 400 + 514): (b'C006', Snacks.SNACK__012.value),
    (base_id + 400 + 515): (b'C006', Snacks.SNACK__013.value),
    (base_id + 400 + 516): (b'C006', Snacks.SNACK__014.value),
    (base_id + 400 + 517): (b'C006', Snacks.SNACK__02.value),
    (base_id + 400 + 518): (b'C006', Snacks.SNACK__020.value),
    (base_id + 400 + 519): (b'C006', Snacks.SNACK__021.value),
    (base_id + 400 + 520): (b'C006', Snacks.SNACK__022.value),
    (base_id + 400 + 521): (b'C006', Snacks.SNACK__023.value),
    (base_id + 400 + 522): (b'C006', Snacks.SNACK__024.value),
    (base_id + 400 + 523): (b'C006', Snacks.CRATE__SNACKBOX__1.value),
    (base_id + 400 + 524): (b'C006', Snacks.CRATE__SNACKBOX__2.value),
    (base_id + 400 + 525): (b'C006', Snacks.SNACK__03.value),
    (base_id + 400 + 526): (b'C006', Snacks.SNACK__030.value),
    (base_id + 400 + 527): (b'C006', Snacks.SNACK__031.value),
    (base_id + 400 + 528): (b'C006', Snacks.SNACK__032.value),
    (base_id + 400 + 529): (b'C006', Snacks.SNACK__033.value),
    (base_id + 400 + 530): (b'C006', Snacks.SNACK__034.value),
    (base_id + 400 + 531): (b'C006', Snacks.SNACK__05.value),
    (base_id + 400 + 532): (b'C006', Snacks.SNACK__050.value),
    (base_id + 400 + 533): (b'C006', Snacks.SNACK__051.value),
    (base_id + 400 + 534): (b'C006', Snacks.SNACK__052.value),
    (base_id + 400 + 535): (b'C006', Snacks.SNACK__053.value),
    (base_id + 400 + 536): (b'C006', Snacks.SNACK__07.value),
    (base_id + 400 + 537): (b'C006', Snacks.SNACK__070.value),
    (base_id + 400 + 538): (b'C006', Snacks.SNACK__071.value),
    (base_id + 400 + 539): (b'C006', Snacks.SNACK__072.value),
    (base_id + 400 + 540): (b'C006', Snacks.SNACK__0720.value),
    (base_id + 400 + 541): (b'C006', Snacks.SNACK__0721.value),
    (base_id + 400 + 542): (b'C006', Snacks.SNACK__0722.value),
    (base_id + 400 + 543): (b'C006', Snacks.SNACK__804.value),
    (base_id + 400 + 544): (b'C006', Snacks.SNACK__803.value),
    (base_id + 400 + 545): (b'C006', Snacks.SNACK__802.value),
    (base_id + 400 + 546): (b'C006', Snacks.SNACK__801.value),
    (base_id + 400 + 547): (b'C006', Snacks.SNACK__800.value),
    (base_id + 400 + 548): (b'C006', Snacks.SNACK__80.value),
    (base_id + 400 + 549): (b'C006', Snacks.SNACK__805.value),
    (base_id + 400 + 550): (b'C006', Snacks.SNACK__806.value),
    (base_id + 400 + 551): (b'C006', Snacks.SNACK__807.value),
    (base_id + 400 + 552): (b'C006', Snacks.SNACK__808.value),
    (base_id + 400 + 553): (b'C006', Snacks.SNACK__809.value),
    (base_id + 400 + 554): (b'C006', Snacks.SNACKBOX__3.value),
    (base_id + 400 + 555): (b'C006', Snacks.SNACK__BOX__2.value),

    (base_id + 400 + 556): (b'C007', Snacks.BOX__OF__SNACKS__1.value),
    (base_id + 400 + 557): (b'C007', Snacks.SNACK__01.value),
    (base_id + 400 + 558): (b'C007', Snacks.SNACK__010.value),
    (base_id + 400 + 559): (b'C007', Snacks.SNACK__011.value),
    (base_id + 400 + 560): (b'C007', Snacks.SNACK__012.value),
    (base_id + 400 + 561): (b'C007', Snacks.SNACK__013.value),
    (base_id + 400 + 562): (b'C007', Snacks.SNACK__014.value),
    (base_id + 400 + 563): (b'C007', Snacks.SNACK__015.value),
    (base_id + 400 + 564): (b'C007', Snacks.SNACK__03.value),
    (base_id + 400 + 565): (b'C007', Snacks.SNACK__030.value),
    (base_id + 400 + 566): (b'C007', Snacks.SNACK__031.value),
    (base_id + 400 + 567): (b'C007', Snacks.SNACK__032.value),
    (base_id + 400 + 568): (b'C007', Snacks.SNACK__033.value),
    (base_id + 400 + 569): (b'C007', Snacks.SNACK__034.value),
    (base_id + 400 + 570): (b'C007', Snacks.SNACK__04.value),
    (base_id + 400 + 571): (b'C007', Snacks.SNACK__040.value),
    (base_id + 400 + 572): (b'C007', Snacks.SNACK__041.value),
    (base_id + 400 + 573): (b'C007', Snacks.SNACK__042.value),
    (base_id + 400 + 574): (b'C007', Snacks.SNACK__043.value),
    (base_id + 400 + 575): (b'C007', Snacks.SNACK__044.value),
    (base_id + 400 + 576): (b'C007', Snacks.SNACK__045.value),
    (base_id + 400 + 577): (b'C007', Snacks.BOX__OF__SNACKS__3.value),
    (base_id + 400 + 578): (b'C007', Snacks.SNACK__074.value),
    (base_id + 400 + 579): (b'C007', Snacks.SNACK__073.value),
    (base_id + 400 + 580): (b'C007', Snacks.SNACK__072.value),
    (base_id + 400 + 581): (b'C007', Snacks.SNACK__071.value),
    (base_id + 400 + 582): (b'C007', Snacks.SNACK__070.value),
    (base_id + 400 + 583): (b'C007', Snacks.SNACK__07.value),
    (base_id + 400 + 584): (b'C007', Snacks.SNACK__075.value),
    (base_id + 400 + 585): (b'C007', Snacks.SNACK__076.value),
    (base_id + 400 + 586): (b'C007', Snacks.SNACK__077.value),
    (base_id + 400 + 587): (b'C007', Snacks.SNACK__078.value),
    (base_id + 400 + 588): (b'C007', Snacks.SNACK__079.value),
    (base_id + 400 + 589): (b'C007', Snacks.SNACK__0790.value),
    (base_id + 400 + 590): (b'C007', Snacks.SNACK__0791.value),
    (base_id + 400 + 591): (b'C007', Snacks.SNACK__0792.value),
    (base_id + 400 + 592): (b'C007', Snacks.SNACK__0793.value),
    (base_id + 400 + 593): (b'C007', Snacks.SNACK__0794.value),
    (base_id + 400 + 594): (b'C007', Snacks.SNACK__10.value),
    (base_id + 400 + 595): (b'C007', Snacks.SNACK__100.value),
    (base_id + 400 + 596): (b'C007', Snacks.SNACK__101.value),
    (base_id + 400 + 597): (b'C007', Snacks.SNACK__102.value),
    (base_id + 400 + 598): (b'C007', Snacks.SNACK__103.value),
    (base_id + 400 + 599): (b'C007', Snacks.SNACK__104.value),
    (base_id + 400 + 600): (b'C007', Snacks.SNACK__105.value),
    (base_id + 400 + 601): (b'C007', Snacks.SNACK__106.value),
    (base_id + 400 + 602): (b'C007', Snacks.SNACK__12.value),
    (base_id + 400 + 603): (b'C007', Snacks.SNACK__120.value),
    (base_id + 400 + 604): (b'C007', Snacks.SNACK__121.value),
    (base_id + 400 + 605): (b'C007', Snacks.SNACK__122.value),
    (base_id + 400 + 606): (b'C007', Snacks.SNACK__123.value),
    (base_id + 400 + 607): (b'C007', Snacks.SNACK__124.value),
    (base_id + 400 + 608): (b'C007', Snacks.SNACK__125.value),
    (base_id + 400 + 609): (b'C007', Snacks.SNACK__164.value),
    (base_id + 400 + 610): (b'C007', Snacks.SNACK__163.value),
    (base_id + 400 + 611): (b'C007', Snacks.SNACK__162.value),
    (base_id + 400 + 612): (b'C007', Snacks.SNACK__161.value),
    (base_id + 400 + 613): (b'C007', Snacks.SNACK__160.value),
    (base_id + 400 + 614): (b'C007', Snacks.SNACK__16.value),
    (base_id + 400 + 615): (b'C007', Snacks.SNACK__17.value),
    (base_id + 400 + 616): (b'C007', Snacks.SNACK__174.value),
    (base_id + 400 + 617): (b'C007', Snacks.SNACK__175.value),
    (base_id + 400 + 618): (b'C007', Snacks.SNACK__176.value),
    (base_id + 400 + 619): (b'C007', Snacks.SNACK__177.value),
    (base_id + 400 + 620): (b'C007', Snacks.SNACK__178.value),
    (base_id + 400 + 621): (b'C007', Snacks.BOX__OF__SNACKS__4.value),
    (base_id + 400 + 622): (b'C007', Snacks.SNACK__180.value),
    (base_id + 400 + 623): (b'C007', Snacks.SNACK__181.value),
    (base_id + 400 + 624): (b'C007', Snacks.SNACK__182.value),
    (base_id + 400 + 625): (b'C007', Snacks.SNACK__183.value),
    (base_id + 400 + 626): (b'C007', Snacks.SNACK__184.value),
    (base_id + 400 + 627): (b'C007', Snacks.SNACK__185.value),
    (base_id + 400 + 628): (b'C007', Snacks.SNACK__186.value),
    (base_id + 400 + 629): (b'C007', Snacks.SNACK__187.value),
    (base_id + 400 + 630): (b'C007', Snacks.SNACK__188.value),
    (base_id + 400 + 631): (b'C007', Snacks.SNACK__189.value),
    (base_id + 400 + 632): (b'C007', Snacks.SNACK__193.value),
    (base_id + 400 + 633): (b'C007', Snacks.SNACK__192.value),
    (base_id + 400 + 634): (b'C007', Snacks.SNACK__191.value),
    (base_id + 400 + 635): (b'C007', Snacks.SNACK__190.value),
    (base_id + 400 + 636): (b'C007', Snacks.SNACK__19.value),
    (base_id + 400 + 637): (b'C007', Snacks.SNACK__194.value),
    (base_id + 400 + 638): (b'C007', Snacks.SNACK__195.value),
    (base_id + 400 + 639): (b'C007', Snacks.SNACK__196.value),
    (base_id + 400 + 640): (b'C007', Snacks.SNACK__197.value),
    (base_id + 400 + 641): (b'C007', Snacks.SNACK__198.value),
    (base_id + 400 + 642): (b'C007', Snacks.BOX__OF__SNACKS__2.value),
    (base_id + 400 + 643): (b'C007', Snacks.SNACK__204.value),
    (base_id + 400 + 644): (b'C007', Snacks.SNACK__203.value),
    (base_id + 400 + 645): (b'C007', Snacks.SNACK__202.value),
    (base_id + 400 + 646): (b'C007', Snacks.SNACK__201.value),
    (base_id + 400 + 647): (b'C007', Snacks.SNACK__200.value),
    (base_id + 400 + 648): (b'C007', Snacks.SNACK__20.value),
    (base_id + 400 + 649): (b'C007', Snacks.SNACK__213.value),
    (base_id + 400 + 650): (b'C007', Snacks.SNACK__212.value),
    (base_id + 400 + 651): (b'C007', Snacks.SNACK__211.value),
    (base_id + 400 + 652): (b'C007', Snacks.SNACK__210.value),
    (base_id + 400 + 653): (b'C007', Snacks.SNACK__21.value),
    (base_id + 400 + 654): (b'C007', Snacks.SNACK__223.value),
    (base_id + 400 + 655): (b'C007', Snacks.SNACK__222.value),
    (base_id + 400 + 656): (b'C007', Snacks.SNACK__221.value),
    (base_id + 400 + 657): (b'C007', Snacks.SNACK__220.value),
    (base_id + 400 + 658): (b'C007', Snacks.SNACK__22.value),
    (base_id + 400 + 659): (b'C007', Snacks.CRATE__PRIZE__1.value),
    (base_id + 400 + 660): (b'C007', Snacks.CRATE__PRIZE__10.value),

    (base_id + 400 + 661): (b'E001', Snacks.SNACK__01.value),
    (base_id + 400 + 662): (b'E001', Snacks.SNACK__010.value),
    (base_id + 400 + 663): (b'E001', Snacks.SNACK__011.value),
    (base_id + 400 + 664): (b'E001', Snacks.SNACK__012.value),
    (base_id + 400 + 665): (b'E001', Snacks.SNACK__013.value),
    (base_id + 400 + 666): (b'E001', Snacks.SNACK__02.value),
    (base_id + 400 + 667): (b'E001', Snacks.SNACK__020.value),
    (base_id + 400 + 668): (b'E001', Snacks.SNACK__03.value),
    (base_id + 400 + 669): (b'E001', Snacks.SNACK__030.value),
    (base_id + 400 + 670): (b'E001', Snacks.SNACK__18.value),
    (base_id + 400 + 671): (b'E001', Snacks.SNACK__20.value),
    (base_id + 400 + 672): (b'E001', Snacks.SNACK__21.value),
    (base_id + 400 + 673): (b'E001', Snacks.SNACK__04.value),
    (base_id + 400 + 674): (b'E001', Snacks.SNACK__22.value),
    (base_id + 400 + 675): (b'E001', Snacks.SNACK__19.value),
    (base_id + 400 + 676): (b'E001', Snacks.SNACKBOX__3.value),
    (base_id + 400 + 677): (b'E001', Snacks.SNACK__054.value),
    (base_id + 400 + 678): (b'E001', Snacks.SNACK__053.value),
    (base_id + 400 + 679): (b'E001', Snacks.SNACK__052.value),
    (base_id + 400 + 680): (b'E001', Snacks.SNACK__051.value),
    (base_id + 400 + 681): (b'E001', Snacks.SNACK__050.value),
    (base_id + 400 + 682): (b'E001', Snacks.SNACK__05.value),
    (base_id + 400 + 683): (b'E001', Snacks.SNACK__06.value),
    (base_id + 400 + 684): (b'E001', Snacks.SNACK__060.value),
    (base_id + 400 + 685): (b'E001', Snacks.SNACK__061.value),
    (base_id + 400 + 686): (b'E001', Snacks.SNACK__062.value),
    (base_id + 400 + 687): (b'E001', Snacks.SNACK__063.value),
    (base_id + 400 + 688): (b'E001', Snacks.SNACK__074.value),
    (base_id + 400 + 689): (b'E001', Snacks.SNACK__073.value),
    (base_id + 400 + 690): (b'E001', Snacks.SNACK__072.value),
    (base_id + 400 + 691): (b'E001', Snacks.SNACK__071.value),
    (base_id + 400 + 692): (b'E001', Snacks.SNACK__070.value),
    (base_id + 400 + 693): (b'E001', Snacks.SNACK__07.value),
    (base_id + 400 + 694): (b'E001', Snacks.SNACKBOX__2.value),
    (base_id + 400 + 695): (b'E001', Snacks.SNACK__23.value),
    (base_id + 400 + 696): (b'E001', Snacks.SNACK__08.value),
    (base_id + 400 + 697): (b'E001', Snacks.SNACK__09.value),
    (base_id + 400 + 698): (b'E001', Snacks.SNACK__24.value),
    (base_id + 400 + 699): (b'E001', Snacks.SNACKBOX__1.value),
    (base_id + 400 + 700): (b'E001', Snacks.SNACK__15.value),
    (base_id + 400 + 701): (b'E001', Snacks.SNACK__150.value),
    (base_id + 400 + 702): (b'E001', Snacks.SNACK__151.value),
    (base_id + 400 + 703): (b'E001', Snacks.SNACK__152.value),
    (base_id + 400 + 704): (b'E001', Snacks.SNACK__153.value),
    (base_id + 400 + 705): (b'E001', Snacks.SNACK__154.value),
    (base_id + 400 + 706): (b'E001', Snacks.SNACK__155.value),
    (base_id + 400 + 707): (b'E001', Snacks.SNACK__156.value),
    (base_id + 400 + 708): (b'E001', Snacks.SNACK__10.value),
    (base_id + 400 + 709): (b'E001', Snacks.SNACK__100.value),
    (base_id + 400 + 710): (b'E001', Snacks.SNACK__101.value),
    (base_id + 400 + 711): (b'E001', Snacks.SNACK__102.value),
    (base_id + 400 + 712): (b'E001', Snacks.SNACK__103.value),
    (base_id + 400 + 713): (b'E001', Snacks.SNACK__104.value),
    (base_id + 400 + 714): (b'E001', Snacks.SNACK__105.value),
    (base_id + 400 + 715): (b'E001', Snacks.SNACK__106.value),
    (base_id + 400 + 716): (b'E001', Snacks.SNACK__12.value),
    (base_id + 400 + 717): (b'E001', Snacks.SNACK__120.value),
    (base_id + 400 + 718): (b'E001', Snacks.SNACK__121.value),
    (base_id + 400 + 719): (b'E001', Snacks.SNACK__122.value),
    (base_id + 400 + 720): (b'E001', Snacks.SNACK__123.value),
    (base_id + 400 + 721): (b'E001', Snacks.SNACK__13.value),
    (base_id + 400 + 722): (b'E001', Snacks.SNACK__130.value),
    (base_id + 400 + 723): (b'E001', Snacks.SNACK__131.value),
    (base_id + 400 + 724): (b'E001', Snacks.SNACK__132.value),
    (base_id + 400 + 725): (b'E001', Snacks.SNACK__133.value),
    (base_id + 400 + 726): (b'E001', Snacks.SNACK__14.value),
    (base_id + 400 + 727): (b'E001', Snacks.SNACK__140.value),
    (base_id + 400 + 728): (b'E001', Snacks.SNACK__141.value),
    (base_id + 400 + 729): (b'E001', Snacks.SNACK__142.value),
    (base_id + 400 + 730): (b'E001', Snacks.SNACK__143.value),
    (base_id + 400 + 731): (b'E001', Snacks.SNACK__253.value),
    (base_id + 400 + 732): (b'E001', Snacks.SNACK__252.value),
    (base_id + 400 + 733): (b'E001', Snacks.SNACK__251.value),
    (base_id + 400 + 734): (b'E001', Snacks.SNACK__250.value),
    (base_id + 400 + 735): (b'E001', Snacks.SNACK__25.value),
    (base_id + 400 + 736): (b'E001', Snacks.SNACK__255.value),
    (base_id + 400 + 737): (b'E001', Snacks.SNACK__256.value),
    (base_id + 400 + 738): (b'E001', Snacks.SNACK__257.value),
    (base_id + 400 + 739): (b'E001', Snacks.SNACK__258.value),
    (base_id + 400 + 740): (b'E001', Snacks.SNACK__259.value),

    (base_id + 400 + 741): (b'E002', Snacks.SNACK39.value),
    (base_id + 400 + 742): (b'E002', Snacks.SNACK390.value),
    (base_id + 400 + 743): (b'E002', Snacks.SNACK391.value),
    (base_id + 400 + 744): (b'E002', Snacks.SNACK392.value),
    (base_id + 400 + 745): (b'E002', Snacks.SNACK393.value),
    (base_id + 400 + 746): (b'E002', Snacks.SNACK11.value),
    (base_id + 400 + 747): (b'E002', Snacks.SNACK110.value),
    (base_id + 400 + 748): (b'E002', Snacks.SNACK365.value),
    (base_id + 400 + 749): (b'E002', Snacks.SNACK112.value),
    (base_id + 400 + 750): (b'E002', Snacks.SNACK113.value),
    (base_id + 400 + 751): (b'E002', Snacks.SNACK13.value),
    (base_id + 400 + 756): (b'E002', Snacks.SNACK130.value),
    (base_id + 400 + 757): (b'E002', Snacks.SNACK1300.value),
    (base_id + 400 + 758): (b'E002', Snacks.SNACK132.value),
    (base_id + 400 + 759): (b'E002', Snacks.SNACK133.value),
    (base_id + 400 + 760): (b'E002', Snacks.SNACKBOX__2.value),
    (base_id + 400 + 761): (b'E002', Snacks.SNACK19.value),
    (base_id + 400 + 762): (b'E002', Snacks.SNACK190.value),
    (base_id + 400 + 763): (b'E002', Snacks.SNACK191.value),
    (base_id + 400 + 764): (b'E002', Snacks.SNACK192.value),
    (base_id + 400 + 765): (b'E002', Snacks.SNACK193.value),
    (base_id + 400 + 766): (b'E002', Snacks.SNACK194.value),
    (base_id + 400 + 767): (b'E002', Snacks.SNACK210.value),
    (base_id + 400 + 768): (b'E002', Snacks.SNACK211.value),
    (base_id + 400 + 769): (b'E002', Snacks.SNACK212.value),
    (base_id + 400 + 770): (b'E002', Snacks.SNACK213.value),
    (base_id + 400 + 771): (b'E002', Snacks.SNACKBOX__4.value),
    (base_id + 400 + 772): (b'E002', Snacks.SNACKBOX__3.value),
    (base_id + 400 + 773): (b'E002', Snacks.SNACK240.value),
    (base_id + 400 + 774): (b'E002', Snacks.SNACK241.value),
    (base_id + 400 + 775): (b'E002', Snacks.SNACK242.value),
    (base_id + 400 + 776): (b'E002', Snacks.SNACK243.value),
    (base_id + 400 + 777): (b'E002', Snacks.SNACK26.value),
    (base_id + 400 + 778): (b'E002', Snacks.SNACK260.value),
    (base_id + 400 + 779): (b'E002', Snacks.SNACK261.value),
    (base_id + 400 + 780): (b'E002', Snacks.SNACK262.value),
    (base_id + 400 + 781): (b'E002', Snacks.SNACK263.value),
    (base_id + 400 + 782): (b'E002', Snacks.SNACK264.value),
    (base_id + 400 + 783): (b'E002', Snacks.SNACK27.value),
    (base_id + 400 + 784): (b'E002', Snacks.SNACK270.value),
    (base_id + 400 + 785): (b'E002', Snacks.SNACK271.value),
    (base_id + 400 + 786): (b'E002', Snacks.SNACK272.value),
    (base_id + 400 + 787): (b'E002', Snacks.SNACK273.value),
    (base_id + 400 + 788): (b'E002', Snacks.SNACK274.value),
    (base_id + 400 + 789): (b'E002', Snacks.SNACK296.value),
    (base_id + 400 + 790): (b'E002', Snacks.SNACK295.value),
    (base_id + 400 + 791): (b'E002', Snacks.SNACK294.value),
    (base_id + 400 + 792): (b'E002', Snacks.SNACK293.value),
    (base_id + 400 + 793): (b'E002', Snacks.SNACK__292.value),
    (base_id + 400 + 794): (b'E002', Snacks.SNACK291.value),
    (base_id + 400 + 795): (b'E002', Snacks.SNACK290.value),
    (base_id + 400 + 796): (b'E002', Snacks.SNACK29.value),
    (base_id + 400 + 797): (b'E002', Snacks.SNACK01.value),
    (base_id + 400 + 798): (b'E002', Snacks.SNACK010.value),
    (base_id + 400 + 799): (b'E002', Snacks.SNACK011.value),
    (base_id + 400 + 800): (b'E002', Snacks.SNACK012.value),
    (base_id + 400 + 801): (b'E002', Snacks.SNACK013.value),
    (base_id + 400 + 802): (b'E002', Snacks.SNACK014.value),
    (base_id + 400 + 803): (b'E002', Snacks.SNACK015.value),
    (base_id + 400 + 804): (b'E002', Snacks.SNACKBOX__5.value),
    (base_id + 400 + 805): (b'E002', Snacks.SNACK09.value),
    (base_id + 400 + 806): (b'E002', Snacks.SNACK10.value),
    (base_id + 400 + 807): (b'E002', Snacks.SNACK31.value),
    (base_id + 400 + 808): (b'E002', Snacks.SNACK310.value),
    (base_id + 400 + 809): (b'E002', Snacks.SNACK311.value),
    (base_id + 400 + 810): (b'E002', Snacks.SNACK312.value),
    (base_id + 400 + 811): (b'E002', Snacks.SNACK313.value),
    (base_id + 400 + 812): (b'E002', Snacks.SNACK314.value),
    (base_id + 400 + 813): (b'E002', Snacks.SNACK315.value),
    (base_id + 400 + 814): (b'E002', Snacks.SNACK32.value),
    (base_id + 400 + 815): (b'E002', Snacks.SNACK320.value),
    (base_id + 400 + 816): (b'E002', Snacks.SNACK321.value),
    (base_id + 400 + 817): (b'E002', Snacks.SNACK322.value),
    (base_id + 400 + 818): (b'E002', Snacks.SNACK323.value),
    (base_id + 400 + 819): (b'E002', Snacks.SNACK324.value),
    (base_id + 400 + 820): (b'E002', Snacks.SNACK325.value),
    (base_id + 400 + 821): (b'E002', Snacks.SNACK326.value),
    (base_id + 400 + 822): (b'E002', Snacks.SNACK33.value),
    (base_id + 400 + 823): (b'E002', Snacks.SNACK330.value),
    (base_id + 400 + 824): (b'E002', Snacks.SNACK331.value),
    (base_id + 400 + 825): (b'E002', Snacks.SNACK332.value),
    (base_id + 400 + 826): (b'E002', Snacks.SNACK333.value),
    (base_id + 400 + 827): (b'E002', Snacks.SNACK334.value),
    (base_id + 400 + 828): (b'E002', Snacks.SNACK335.value),
    (base_id + 400 + 829): (b'E002', Snacks.SNACK35.value),
    (base_id + 400 + 830): (b'E002', Snacks.SNACK36.value),
    (base_id + 400 + 831): (b'E002', Snacks.SNACK360.value),
    (base_id + 400 + 832): (b'E002', Snacks.SNACK361.value),
    (base_id + 400 + 833): (b'E002', Snacks.SNACK362.value),
    (base_id + 400 + 834): (b'E002', Snacks.SNACK363.value),
    (base_id + 400 + 835): (b'E002', Snacks.SNACK364.value),
    (base_id + 400 + 836): (b'E002', Snacks.SNACK37.value),
    (base_id + 400 + 837): (b'E002', Snacks.SNACK370.value),
    (base_id + 400 + 838): (b'E002', Snacks.SNACK371.value),
    (base_id + 400 + 839): (b'E002', Snacks.SNACK372.value),
    (base_id + 400 + 840): (b'E002', Snacks.SNACK373.value),
    (base_id + 400 + 841): (b'E002', Snacks.SNACK__374.value),
    (base_id + 400 + 842): (b'E002', Snacks.SNACK40.value),
    (base_id + 400 + 844): (b'E002', Snacks.SNACK400.value),
    (base_id + 400 + 845): (b'E002', Snacks.SNACK401.value),
    (base_id + 400 + 846): (b'E002', Snacks.SNACK402.value),
    (base_id + 400 + 847): (b'E002', Snacks.SNACK403.value),
    (base_id + 400 + 848): (b'E002', Snacks.SNACK404.value),

    (base_id + 400 + 849): (b'E003', Snacks.SNACK__21.value),
    (base_id + 400 + 850): (b'E003', Snacks.SNACK__210.value),
    (base_id + 400 + 851): (b'E003', Snacks.SNACK__211.value),
    (base_id + 400 + 852): (b'E003', Snacks.SNACK__212.value),
    (base_id + 400 + 853): (b'E003', Snacks.SNACK__213.value),
    (base_id + 400 + 854): (b'E003', Snacks.SNACK__214.value),
    (base_id + 400 + 855): (b'E003', Snacks.SNACK__2140.value),
    (base_id + 400 + 856): (b'E003', Snacks.SNACK__21400.value),
    (base_id + 400 + 857): (b'E003', Snacks.SNACK__21401.value),
    (base_id + 400 + 858): (b'E003', Snacks.SNACK__21402.value),
    (base_id + 400 + 859): (b'E003', Snacks.SNACK__21403.value),
    (base_id + 400 + 860): (b'E003', Snacks.SNACK__21404.value),
    (base_id + 400 + 861): (b'E003', Snacks.SNACK__01.value),
    (base_id + 400 + 862): (b'E003', Snacks.SNACK__010.value),
    (base_id + 400 + 863): (b'E003', Snacks.SNACK__011.value),
    (base_id + 400 + 864): (b'E003', Snacks.SNACK__012.value),
    (base_id + 400 + 865): (b'E003', Snacks.SNACK__013.value),
    (base_id + 400 + 866): (b'E003', Snacks.SNACK__014.value),
    (base_id + 400 + 867): (b'E003', Snacks.SNACK__015.value),
    (base_id + 400 + 868): (b'E003', Snacks.SNACK__02.value),
    (base_id + 400 + 869): (b'E003', Snacks.SNACK__020.value),
    (base_id + 400 + 870): (b'E003', Snacks.SNACK__021.value),
    (base_id + 400 + 871): (b'E003', Snacks.SNACK__022.value),
    (base_id + 400 + 872): (b'E003', Snacks.SNACK__023.value),
    (base_id + 400 + 873): (b'E003', Snacks.SNACK__024.value),
    (base_id + 400 + 874): (b'E003', Snacks.SNACK__025.value),
    (base_id + 400 + 875): (b'E003', Snacks.SNACK__05.value),
    (base_id + 400 + 876): (b'E003', Snacks.SNACK__050.value),
    (base_id + 400 + 877): (b'E003', Snacks.SNACK__051.value),
    (base_id + 400 + 878): (b'E003', Snacks.SNACK__052.value),
    (base_id + 400 + 879): (b'E003', Snacks.SNACK__053.value),
    (base_id + 400 + 880): (b'E003', Snacks.SNACK__054.value),
    (base_id + 400 + 881): (b'E003', Snacks.SNACK__06.value),
    (base_id + 400 + 882): (b'E003', Snacks.SNACK__060.value),
    (base_id + 400 + 883): (b'E003', Snacks.SNACK__061.value),
    (base_id + 400 + 884): (b'E003', Snacks.SNACK__062.value),
    (base_id + 400 + 885): (b'E003', Snacks.SNACK__063.value),
    (base_id + 400 + 886): (b'E003', Snacks.SNACK__064.value),
    (base_id + 400 + 887): (b'E003', Snacks.SNACK__07.value),
    (base_id + 400 + 888): (b'E003', Snacks.SNACK__070.value),
    (base_id + 400 + 889): (b'E003', Snacks.SNACK__071.value),
    (base_id + 400 + 890): (b'E003', Snacks.SNACK__072.value),
    (base_id + 400 + 891): (b'E003', Snacks.SNACK__073.value),
    (base_id + 400 + 892): (b'E003', Snacks.SNACK__12.value),
    (base_id + 400 + 893): (b'E003', Snacks.SNACK__120.value),
    (base_id + 400 + 894): (b'E003', Snacks.SNACK__121.value),
    (base_id + 400 + 895): (b'E003', Snacks.SNACK__122.value),
    (base_id + 400 + 896): (b'E003', Snacks.SNACK__123.value),
    (base_id + 400 + 897): (b'E003', Snacks.SNACK__124.value),
    (base_id + 400 + 898): (b'E003', Snacks.SNACK__03.value),
    (base_id + 400 + 899): (b'E003', Snacks.SNACK__030.value),
    (base_id + 400 + 900): (b'E003', Snacks.SNACK__031.value),
    (base_id + 400 + 901): (b'E003', Snacks.SNACK__032.value),
    (base_id + 400 + 902): (b'E003', Snacks.SNACK__033.value),
    (base_id + 400 + 903): (b'E003', Snacks.SNACK__034.value),
    (base_id + 400 + 904): (b'E003', Snacks.SNACKBOX__1.value),
    (base_id + 400 + 905): (b'E003', Snacks.SNACKBOX__2.value),

    (base_id + 400 + 906): (b'E004', Snacks.SNACK02.value),
    (base_id + 400 + 907): (b'E004', Snacks.SNACK020.value),
    (base_id + 400 + 908): (b'E004', Snacks.SNACK__021.value),
    (base_id + 400 + 909): (b'E004', Snacks.SNACK022.value),
    (base_id + 400 + 910): (b'E004', Snacks.SNACK023.value),
    (base_id + 400 + 911): (b'E004', Snacks.SNACK__001.value),
    (base_id + 400 + 912): (b'E004', Snacks.SNACK__0010.value),
    (base_id + 400 + 913): (b'E004', Snacks.SNACKBOX__3.value),
    (base_id + 400 + 914): (b'E004', Snacks.SNACK__0012.value),
    (base_id + 400 + 915): (b'E004', Snacks.SNACK__0013.value),
    (base_id + 400 + 916): (b'E004', Snacks.SNACK03.value),
    (base_id + 400 + 917): (b'E004', Snacks.SNACK030.value),
    (base_id + 400 + 918): (b'E004', Snacks.SNACK031.value),
    (base_id + 400 + 919): (b'E004', Snacks.SNACK032.value),
    (base_id + 400 + 920): (b'E004', Snacks.SNACK040.value),
    (base_id + 400 + 921): (b'E004', Snacks.SNACK041.value),
    (base_id + 400 + 922): (b'E004', Snacks.SNACK042.value),
    (base_id + 400 + 923): (b'E004', Snacks.SNACK043.value),
    (base_id + 400 + 924): (b'E004', Snacks.SNACK050.value),
    (base_id + 400 + 925): (b'E004', Snacks.SNACK051.value),
    (base_id + 400 + 926): (b'E004', Snacks.SNACK052.value),
    (base_id + 400 + 927): (b'E004', Snacks.SNACK053.value),
    (base_id + 400 + 928): (b'E004', Snacks.SNACK0530.value),
    (base_id + 400 + 929): (b'E004', Snacks.SNACK05300.value),
    (base_id + 400 + 930): (b'E004', Snacks.SNACK05301.value),
    (base_id + 400 + 931): (b'E004', Snacks.SNACK05302.value),
    (base_id + 400 + 932): (b'E004', Snacks.SNACK__3030.value),
    (base_id + 400 + 933): (b'E004', Snacks.SNACK__30300.value),
    (base_id + 400 + 934): (b'E004', Snacks.SNACK__30301.value),
    (base_id + 400 + 935): (b'E004', Snacks.SNACK__30302.value),
    (base_id + 400 + 936): (b'E004', Snacks.SNACK__30303.value),
    (base_id + 400 + 937): (b'E004', Snacks.SNACK07.value),
    (base_id + 400 + 938): (b'E004', Snacks.SNACK070.value),
    (base_id + 400 + 939): (b'E004', Snacks.SNACK071.value),
    (base_id + 400 + 940): (b'E004', Snacks.SNACK08.value),
    (base_id + 400 + 941): (b'E004', Snacks.SNACK080.value),
    (base_id + 400 + 942): (b'E004', Snacks.SNACK081.value),
    (base_id + 400 + 943): (b'E004', Snacks.SNACK082.value),
    (base_id + 400 + 944): (b'E004', Snacks.SNACK083.value),
    (base_id + 400 + 945): (b'E004', Snacks.SNACK09.value),
    (base_id + 400 + 946): (b'E004', Snacks.SNACK090.value),
    (base_id + 400 + 947): (b'E004', Snacks.SNACK091.value),
    (base_id + 400 + 948): (b'E004', Snacks.SNACK092.value),
    (base_id + 400 + 949): (b'E004', Snacks.SNACK093.value),
    (base_id + 400 + 950): (b'E004', Snacks.SNACK0930.value),
    (base_id + 400 + 951): (b'E004', Snacks.SNACK09300.value),
    (base_id + 400 + 952): (b'E004', Snacks.SNACK09301.value),
    (base_id + 400 + 953): (b'E004', Snacks.SNACKBOX__1.value),
    (base_id + 400 + 954): (b'E004', Snacks.SNACK09303.value),
    (base_id + 400 + 955): (b'E004', Snacks.SNACK09304.value),
    (base_id + 400 + 956): (b'E004', Snacks.SNACK09305.value),
    (base_id + 400 + 957): (b'E004', Snacks.SNACK12.value),
    (base_id + 400 + 958): (b'E004', Snacks.SNACK120.value),
    (base_id + 400 + 959): (b'E004', Snacks.SNACK121.value),
    (base_id + 400 + 960): (b'E004', Snacks.SNACK122.value),
    (base_id + 400 + 961): (b'E004', Snacks.SNACK123.value),
    (base_id + 400 + 962): (b'E004', Snacks.SNACK14.value),
    (base_id + 400 + 963): (b'E004', Snacks.SNACK140.value),
    (base_id + 400 + 964): (b'E004', Snacks.SNACK141.value),
    (base_id + 400 + 965): (b'E004', Snacks.SNACK142.value),
    (base_id + 400 + 966): (b'E004', Snacks.SNACK143.value),
    (base_id + 400 + 967): (b'E004', Snacks.SNACK21.value),
    (base_id + 400 + 968): (b'E004', Snacks.SNACK210.value),
    (base_id + 400 + 969): (b'E004', Snacks.SNACK211.value),
    (base_id + 400 + 970): (b'E004', Snacks.SNACK212.value),
    (base_id + 400 + 971): (b'E004', Snacks.SNACK213.value),
    (base_id + 400 + 972): (b'E004', Snacks.SNACK2130.value),
    (base_id + 400 + 973): (b'E004', Snacks.SNACK21300.value),
    (base_id + 400 + 974): (b'E004', Snacks.SNACK21301.value),
    (base_id + 400 + 975): (b'E004', Snacks.SNACKBOX__2.value),
    (base_id + 400 + 976): (b'E004', Snacks.SNACK21303.value),
    (base_id + 400 + 977): (b'E004', Snacks.SNACK21304.value),
    (base_id + 400 + 978): (b'E004', Snacks.SNACK21305.value),
    (base_id + 400 + 979): (b'E004', Snacks.SNACK19.value),
    (base_id + 400 + 980): (b'E004', Snacks.SNACK190.value),
    (base_id + 400 + 981): (b'E004', Snacks.SNACK191.value),
    (base_id + 400 + 982): (b'E004', Snacks.SNACK192.value),
    (base_id + 400 + 983): (b'E004', Snacks.SNACK193.value),

    (base_id + 400 + 5344): (b'E005', Snacks.SNACK__01.value),
    (base_id + 400 + 984): (b'E005', Snacks.SNACK__010.value),
    (base_id + 400 + 985): (b'E005', Snacks.SNACK__011.value),
    (base_id + 400 + 986): (b'E005', Snacks.SNACK__012.value),
    (base_id + 400 + 987): (b'E005', Snacks.SNACK__013.value),
    (base_id + 400 + 988): (b'E005', Snacks.SNACK__03.value),
    (base_id + 400 + 989): (b'E005', Snacks.SNACK__030.value),
    (base_id + 400 + 990): (b'E005', Snacks.SNACK__031.value),
    (base_id + 400 + 991): (b'E005', Snacks.SNACK__032.value),
    (base_id + 400 + 992): (b'E005', Snacks.SNACK__033.value),
    (base_id + 400 + 993): (b'E005', Snacks.SNACK__034.value),
    (base_id + 400 + 994): (b'E005', Snacks.SNACK__04.value),
    (base_id + 400 + 995): (b'E005', Snacks.SNACK__040.value),
    (base_id + 400 + 996): (b'E005', Snacks.SNACK__041.value),
    (base_id + 400 + 997): (b'E005', Snacks.SNACK__042.value),
    (base_id + 400 + 998): (b'E005', Snacks.SNACK__043.value),
    (base_id + 400 + 999): (b'E005', Snacks.SNACK__02.value),
    (base_id + 400 + 1000): (b'E005', Snacks.SNACK__020.value),
    (base_id + 400 + 1001): (b'E005', Snacks.SNACK__021.value),
    (base_id + 400 + 1002): (b'E005', Snacks.SNACK__022.value),
    (base_id + 400 + 1003): (b'E005', Snacks.SNACK__023.value),
    (base_id + 400 + 1004): (b'E005', Snacks.SNACK__024.value),
    (base_id + 400 + 1005): (b'E005', Snacks.SNACK__025.value),
    (base_id + 400 + 1006): (b'E005', Snacks.SNACK__06.value),
    (base_id + 400 + 1007): (b'E005', Snacks.SNACK__08.value),
    (base_id + 400 + 1008): (b'E005', Snacks.SNACK__20.value),
    (base_id + 400 + 1009): (b'E005', Snacks.SNACK__200.value),
    (base_id + 400 + 1010): (b'E005', Snacks.SNACK__201.value),
    (base_id + 400 + 1011): (b'E005', Snacks.SNACK__202.value),
    (base_id + 400 + 1012): (b'E005', Snacks.SNACK__203.value),
    (base_id + 400 + 1013): (b'E005', Snacks.SNACK__2030.value),
    (base_id + 400 + 1014): (b'E005', Snacks.SNACK__2031.value),
    (base_id + 400 + 1015): (b'E005', Snacks.SNACK__2032.value),
    (base_id + 400 + 1016): (b'E005', Snacks.SNACK__2033.value),
    (base_id + 400 + 1017): (b'E005', Snacks.SNACK__20340.value),
    (base_id + 400 + 1018): (b'E005', Snacks.SNACK__203400.value),
    (base_id + 400 + 1019): (b'E005', Snacks.SNACK__203401.value),
    (base_id + 400 + 1020): (b'E005', Snacks.SNACK__203402.value),
    (base_id + 400 + 1021): (b'E005', Snacks.SNACK__203403.value),
    (base_id + 400 + 1022): (b'E005', Snacks.SNACK__2034040.value),
    (base_id + 400 + 1023): (b'E005', Snacks.SNACK__20340400.value),
    (base_id + 400 + 1024): (b'E005', Snacks.SNACK__20340401.value),
    (base_id + 400 + 1025): (b'E005', Snacks.SNACK__20340402.value),
    (base_id + 400 + 1026): (b'E005', Snacks.SNACK__20340403.value),
    (base_id + 400 + 1027): (b'E005', Snacks.SNACK__20340404.value),
    (base_id + 400 + 1028): (b'E005', Snacks.SNACK__09.value),
    (base_id + 400 + 1029): (b'E005', Snacks.SNACK__090.value),
    (base_id + 400 + 1030): (b'E005', Snacks.SNACK__091.value),
    (base_id + 400 + 1031): (b'E005', Snacks.SNACK__092.value),
    (base_id + 400 + 1032): (b'E005', Snacks.SNACK__093.value),
    (base_id + 400 + 1033): (b'E005', Snacks.SNACK__10.value),
    (base_id + 400 + 1034): (b'E005', Snacks.SNACK__100.value),
    (base_id + 400 + 1035): (b'E005', Snacks.SNACK__101.value),
    (base_id + 400 + 1036): (b'E005', Snacks.SNACK__102.value),
    (base_id + 400 + 1037): (b'E005', Snacks.SNACK__103.value),
    (base_id + 400 + 1038): (b'E005', Snacks.SNACK__13.value),
    (base_id + 400 + 1039): (b'E005', Snacks.SNACK__130.value),
    (base_id + 400 + 1040): (b'E005', Snacks.SNACK__131.value),
    (base_id + 400 + 1041): (b'E005', Snacks.SNACK__132.value),
    (base_id + 400 + 1042): (b'E005', Snacks.SNACK__133.value),
    (base_id + 400 + 1043): (b'E005', Snacks.SNACK__143.value),
    (base_id + 400 + 1044): (b'E005', Snacks.SNACK__142.value),
    (base_id + 400 + 1045): (b'E005', Snacks.SNACK__141.value),
    (base_id + 400 + 1046): (b'E005', Snacks.SNACK__140.value),
    (base_id + 400 + 1047): (b'E005', Snacks.SNACK__14.value),
    (base_id + 400 + 1048): (b'E005', Snacks.SNACK__11.value),
    (base_id + 400 + 1049): (b'E005', Snacks.SNACK__110.value),
    (base_id + 400 + 1050): (b'E005', Snacks.SNACK__111.value),
    (base_id + 400 + 1051): (b'E005', Snacks.SNACK__112.value),
    (base_id + 400 + 1052): (b'E005', Snacks.SNACK__15.value),
    (base_id + 400 + 1053): (b'E005', Snacks.SNACK__114.value),
    (base_id + 400 + 1054): (b'E005', Snacks.SNACKBOX__1.value),
    (base_id + 400 + 1055): (b'E005', Snacks.SNACKBOX__2.value),
    (base_id + 400 + 1056): (b'E005', Snacks.SNACKBOX__3.value),

    (base_id + 400 + 1057): (b'E006', Snacks.SNACK__02.value),
    (base_id + 400 + 1058): (b'E006', Snacks.SNACK__020.value),
    (base_id + 400 + 1059): (b'E006', Snacks.SNACK__021.value),
    (base_id + 400 + 1060): (b'E006', Snacks.SNACK__022.value),
    (base_id + 400 + 1061): (b'E006', Snacks.SNACK__023.value),
    (base_id + 400 + 1062): (b'E006', Snacks.SNACK__024.value),
    (base_id + 400 + 1063): (b'E006', Snacks.SNACK__03.value),
    (base_id + 400 + 1064): (b'E006', Snacks.SNACK__030.value),
    (base_id + 400 + 1065): (b'E006', Snacks.SNACK__031.value),
    (base_id + 400 + 1066): (b'E006', Snacks.SNACK__032.value),
    (base_id + 400 + 1067): (b'E006', Snacks.SNACK__033.value),
    (base_id + 400 + 1068): (b'E006', Snacks.SNACK__034.value),
    (base_id + 400 + 1069): (b'E006', Snacks.SNACK__05.value),
    (base_id + 400 + 1070): (b'E006', Snacks.SNACK__050.value),
    (base_id + 400 + 1071): (b'E006', Snacks.SNACK__051.value),
    (base_id + 400 + 1072): (b'E006', Snacks.SNACK__052.value),
    (base_id + 400 + 1073): (b'E006', Snacks.SNACK__09.value),
    (base_id + 400 + 1074): (b'E006', Snacks.SNACK__090.value),
    (base_id + 400 + 1075): (b'E006', Snacks.SNACK__091.value),
    (base_id + 400 + 1076): (b'E006', Snacks.SNACK__092.value),
    (base_id + 400 + 1077): (b'E006', Snacks.SNACK__093.value),
    (base_id + 400 + 1078): (b'E006', Snacks.SNACK__094.value),
    (base_id + 400 + 1079): (b'E006', Snacks.SNACK__11.value),
    (base_id + 400 + 1080): (b'E006', Snacks.SNACK__110.value),
    (base_id + 400 + 1081): (b'E006', Snacks.SNACK__111.value),
    (base_id + 400 + 1082): (b'E006', Snacks.SNACK__112.value),
    (base_id + 400 + 1083): (b'E006', Snacks.SNACK__113.value),
    (base_id + 400 + 1084): (b'E006', Snacks.SNACK__114.value),
    (base_id + 400 + 1085): (b'E006', Snacks.SNACK__13.value),
    (base_id + 400 + 1086): (b'E006', Snacks.SNACK__130.value),
    (base_id + 400 + 1087): (b'E006', Snacks.SNACK__131.value),
    (base_id + 400 + 1088): (b'E006', Snacks.SNACK__132.value),
    (base_id + 400 + 1089): (b'E006', Snacks.SNACK__133.value),
    (base_id + 400 + 1090): (b'E006', Snacks.SNACK__16.value),
    (base_id + 400 + 1091): (b'E006', Snacks.SNACK__160.value),
    (base_id + 400 + 1092): (b'E006', Snacks.SNACK__161.value),
    (base_id + 400 + 1093): (b'E006', Snacks.SNACK__162.value),
    (base_id + 400 + 1094): (b'E006', Snacks.SNACKBOX__2.value),
    (base_id + 400 + 1095): (b'E006', Snacks.SNACKBOX__3.value),
    (base_id + 400 + 1096): (b'E006', Snacks.SNACKBOX__4.value),
    (base_id + 400 + 1097): (b'E006', Snacks.SNACKBOX__1.value),

    (base_id + 400 + 1098): (b'E007', Snacks.SNACK__05.value),
    (base_id + 400 + 1099): (b'E007', Snacks.SNACK__050.value),
    (base_id + 400 + 1100): (b'E007', Snacks.SNACK__051.value),
    (base_id + 400 + 1101): (b'E007', Snacks.SNACK__052.value),
    (base_id + 400 + 1102): (b'E007', Snacks.SNACK__053.value),
    (base_id + 400 + 1103): (b'E007', Snacks.SNACK__03.value),
    (base_id + 400 + 1104): (b'E007', Snacks.SNACK__030.value),
    (base_id + 400 + 1105): (b'E007', Snacks.SNACK__031.value),
    (base_id + 400 + 1106): (b'E007', Snacks.SNACK__032.value),
    (base_id + 400 + 1107): (b'E007', Snacks.SNACK__04.value),
    (base_id + 400 + 1108): (b'E007', Snacks.SNACK__040.value),
    (base_id + 400 + 1109): (b'E007', Snacks.SNACK__041.value),
    (base_id + 400 + 1110): (b'E007', Snacks.SNACK__042.value),
    (base_id + 400 + 1111): (b'E007', Snacks.SNACK__07.value),
    (base_id + 400 + 1112): (b'E007', Snacks.SNACK__08.value),
    (base_id + 400 + 1113): (b'E007', Snacks.SNACK__080.value),
    (base_id + 400 + 1114): (b'E007', Snacks.SNACK__081.value),
    (base_id + 400 + 1115): (b'E007', Snacks.SNACK__083.value),
    (base_id + 400 + 1116): (b'E007', Snacks.SNACK__0830.value),
    (base_id + 400 + 1117): (b'E007', Snacks.SNACK__0831.value),
    (base_id + 400 + 1118): (b'E007', Snacks.SNACK__0832.value),
    (base_id + 400 + 1119): (b'E007', Snacks.SNACK__0833.value),
    (base_id + 400 + 1120): (b'E007', Snacks.SNACK__09.value),
    (base_id + 400 + 1121): (b'E007', Snacks.SNACK__090.value),
    (base_id + 400 + 1122): (b'E007', Snacks.SNACK__091.value),
    (base_id + 400 + 1123): (b'E007', Snacks.SNACK__092.value),
    (base_id + 400 + 1124): (b'E007', Snacks.SNACK__093.value),
    (base_id + 400 + 1125): (b'E007', Snacks.SNACK__11.value),
    (base_id + 400 + 1126): (b'E007', Snacks.SNACK__110.value),
    (base_id + 400 + 1127): (b'E007', Snacks.SNACK__111.value),
    (base_id + 400 + 1128): (b'E007', Snacks.SNACK__112.value),
    (base_id + 400 + 1129): (b'E007', Snacks.SNACK__113.value),
    (base_id + 400 + 1130): (b'E007', Snacks.SNACK__114.value),
    (base_id + 400 + 1131): (b'E007', Snacks.SNACK__12.value),
    (base_id + 400 + 1132): (b'E007', Snacks.SNACK__120.value),
    (base_id + 400 + 1133): (b'E007', Snacks.SNACK__121.value),
    (base_id + 400 + 1134): (b'E007', Snacks.SNACK__122.value),
    (base_id + 400 + 1135): (b'E007', Snacks.SNACK__123.value),
    (base_id + 400 + 1136): (b'E007', Snacks.SNACK__124.value),
    (base_id + 400 + 1137): (b'E007', Snacks.SNACK__14.value),
    (base_id + 400 + 1138): (b'E007', Snacks.SNACK__140.value),
    (base_id + 400 + 1139): (b'E007', Snacks.SNACK__141.value),
    (base_id + 400 + 1140): (b'E007', Snacks.SNACK__22.value),
    (base_id + 400 + 1141): (b'E007', Snacks.SNACK__220.value),
    (base_id + 400 + 1142): (b'E007', Snacks.SNACK__221.value),
    (base_id + 400 + 1143): (b'E007', Snacks.SNACK__222.value),
    (base_id + 400 + 1144): (b'E007', Snacks.SNACK__223.value),
    (base_id + 400 + 1145): (b'E007', Snacks.SNACK__23.value),
    (base_id + 400 + 1146): (b'E007', Snacks.SNACK__230.value),
    (base_id + 400 + 1147): (b'E007', Snacks.SNACK__231.value),
    (base_id + 400 + 1148): (b'E007', Snacks.SNACK__232.value),
    (base_id + 400 + 1149): (b'E007', Snacks.SNACK__233.value),
    (base_id + 400 + 1150): (b'E007', Snacks.SNACK__16.value),
    (base_id + 400 + 1151): (b'E007', Snacks.SNACK__160.value),
    (base_id + 400 + 1152): (b'E007', Snacks.SNACK__161.value),
    (base_id + 400 + 1153): (b'E007', Snacks.SNACK__162.value),
    (base_id + 400 + 1154): (b'E007', Snacks.SNACK__163.value),
    (base_id + 400 + 1155): (b'E007', Snacks.SNACK__164.value),
    (base_id + 400 + 1156): (b'E007', Snacks.SNACK__17.value),
    (base_id + 400 + 1157): (b'E007', Snacks.SNACK__170.value),
    (base_id + 400 + 1158): (b'E007', Snacks.SNACK__171.value),
    (base_id + 400 + 1159): (b'E007', Snacks.SNACK__172.value),
    (base_id + 400 + 1160): (b'E007', Snacks.SNACK__173.value),
    (base_id + 400 + 1161): (b'E007', Snacks.SNACK__18.value),
    (base_id + 400 + 1162): (b'E007', Snacks.SNACK__180.value),
    (base_id + 400 + 1163): (b'E007', Snacks.SNACK__181.value),
    (base_id + 400 + 1164): (b'E007', Snacks.SNACK__182.value),
    (base_id + 400 + 1165): (b'E007', Snacks.SNACK__183.value),
    (base_id + 400 + 1166): (b'E007', Snacks.SNACK__20.value),
    (base_id + 400 + 1167): (b'E007', Snacks.SNACK__200.value),
    (base_id + 400 + 1168): (b'E007', Snacks.SNACK__201.value),
    (base_id + 400 + 1169): (b'E007', Snacks.SNACK__202.value),
    (base_id + 400 + 1170): (b'E007', Snacks.SNACK__203.value),
    (base_id + 400 + 1171): (b'E007', Snacks.SNACK__204.value),
    (base_id + 400 + 1172): (b'E007', Snacks.SNACK__21.value),
    (base_id + 400 + 1173): (b'E007', Snacks.SNACK__210.value),
    (base_id + 400 + 1174): (b'E007', Snacks.SNACK__211.value),
    (base_id + 400 + 1175): (b'E007', Snacks.SNACK__212.value),
    (base_id + 400 + 1176): (b'E007', Snacks.SNACK__213.value),
    (base_id + 400 + 1177): (b'E007', Snacks.SNACK__214.value),
    (base_id + 400 + 1178): (b'E007', Snacks.SNACK__19.value),
    (base_id + 400 + 1179): (b'E007', Snacks.SNACK__190.value),
    (base_id + 400 + 1180): (b'E007', Snacks.SNACK__191.value),
    (base_id + 400 + 1181): (b'E007', Snacks.SNACK__192.value),
    (base_id + 400 + 1182): (b'E007', Snacks.SNACK__193.value),
    (base_id + 400 + 1183): (b'E007', Snacks.SNACK__194.value),
    (base_id + 400 + 1184): (b'E007', Snacks.SNACK__195.value),
    (base_id + 400 + 1185): (b'E007', Snacks.SNACKBOX__2.value),
    (base_id + 400 + 1186): (b'E007', Snacks.DIG__2__SNACKBOX.value),

    (base_id + 400 + 1287): (b'E008', Snacks.SNACK__010.value),
    (base_id + 400 + 1288): (b'E008', Snacks.SNACK__011.value),
    (base_id + 400 + 1289): (b'E008', Snacks.SNACK__012.value),
    (base_id + 400 + 1290): (b'E008', Snacks.SNACK__013.value),
    (base_id + 400 + 1291): (b'E008', Snacks.SNACK__03.value),
    (base_id + 400 + 1292): (b'E008', Snacks.SNACK__030.value),
    (base_id + 400 + 1293): (b'E008', Snacks.SNACK__031.value),
    (base_id + 400 + 1294): (b'E008', Snacks.SNACK__032.value),
    (base_id + 400 + 1295): (b'E008', Snacks.SNACK__033.value),
    (base_id + 400 + 1296): (b'E008', Snacks.SNACK__0330.value),
    (base_id + 400 + 1297): (b'E008', Snacks.SNACK__0331.value),
    (base_id + 400 + 1298): (b'E008', Snacks.SNACK__0332.value),
    (base_id + 400 + 1299): (b'E008', Snacks.SNACK__0333.value),
    (base_id + 400 + 1300): (b'E008', Snacks.SNACK__05.value),
    (base_id + 400 + 1301): (b'E008', Snacks.SNACK__050.value),
    (base_id + 400 + 1302): (b'E008', Snacks.SNACK__051.value),
    (base_id + 400 + 1303): (b'E008', Snacks.SNACK__052.value),
    (base_id + 400 + 1304): (b'E008', Snacks.SNACK__053.value),
    (base_id + 400 + 1305): (b'E008', Snacks.SNACK__06.value),
    (base_id + 400 + 1306): (b'E008', Snacks.SNACK__08.value),
    (base_id + 400 + 1307): (b'E008', Snacks.SNACK__080.value),
    (base_id + 400 + 1308): (b'E008', Snacks.SNACK__081.value),
    (base_id + 400 + 1309): (b'E008', Snacks.SNACK__082.value),
    (base_id + 400 + 1310): (b'E008', Snacks.SNACK__09.value),
    (base_id + 400 + 1311): (b'E008', Snacks.SNACK__090.value),
    (base_id + 400 + 1312): (b'E008', Snacks.SNACK__091.value),
    (base_id + 400 + 1313): (b'E008', Snacks.SNACK__092.value),
    (base_id + 400 + 1314): (b'E008', Snacks.SNACK__25.value),
    (base_id + 400 + 1315): (b'E008', Snacks.SNACK__250.value),
    (base_id + 400 + 1316): (b'E008', Snacks.SNACK__251.value),
    (base_id + 400 + 1317): (b'E008', Snacks.SNACK__252.value),
    (base_id + 400 + 1318): (b'E008', Snacks.SNACK__2520.value),
    (base_id + 400 + 1319): (b'E008', Snacks.SNACK__2521.value),
    (base_id + 400 + 1320): (b'E008', Snacks.SNACK__2522.value),
    (base_id + 400 + 1321): (b'E008', Snacks.SNACK__2523.value),
    (base_id + 400 + 1322): (b'E008', Snacks.SNACK__25221.value),
    (base_id + 400 + 1323): (b'E008', Snacks.SNACK__25222.value),
    (base_id + 400 + 1324): (b'E008', Snacks.SNACK__252220.value),
    (base_id + 400 + 1325): (b'E008', Snacks.SNACK__252221.value),
    (base_id + 400 + 1326): (b'E008', Snacks.SNACK__252222.value),
    (base_id + 400 + 1327): (b'E008', Snacks.SNACK__2522220.value),
    (base_id + 400 + 1328): (b'E008', Snacks.SNACK__2522221.value),
    (base_id + 400 + 1329): (b'E008', Snacks.SNACK__2522222.value),
    (base_id + 400 + 1330): (b'E008', Snacks.SNACK__25222220.value),
    (base_id + 400 + 1331): (b'E008', Snacks.SNACK__25222221.value),
    (base_id + 400 + 1332): (b'E008', Snacks.SNACK__25222222.value),
    (base_id + 400 + 1333): (b'E008', Snacks.SNACK__252222220.value),
    (base_id + 400 + 1334): (b'E008', Snacks.SNACK__252222221.value),
    (base_id + 400 + 1335): (b'E008', Snacks.SNACK__252222222.value),
    (base_id + 400 + 1336): (b'E008', Snacks.SNACK__30.value),
    (base_id + 400 + 1337): (b'E008', Snacks.SNACK__300.value),
    (base_id + 400 + 1338): (b'E008', Snacks.SNACK__301.value),
    (base_id + 400 + 1339): (b'E008', Snacks.SNACK__302.value),
    (base_id + 400 + 1340): (b'E008', Snacks.SNACK__3020.value),
    (base_id + 400 + 1341): (b'E008', Snacks.SNACK__3021.value),
    (base_id + 400 + 1342): (b'E008', Snacks.SNACK__3022.value),
    (base_id + 400 + 1343): (b'E008', Snacks.SNACK__30220.value),
    (base_id + 400 + 1344): (b'E008', Snacks.SNACK__30221.value),
    (base_id + 400 + 1345): (b'E008', Snacks.SNACK__30222.value),
    (base_id + 400 + 1346): (b'E008', Snacks.SNACK__32.value),
    (base_id + 400 + 1347): (b'E008', Snacks.SNACK__320.value),
    (base_id + 400 + 1348): (b'E008', Snacks.SNACK__321.value),
    (base_id + 400 + 1349): (b'E008', Snacks.SNACK__322.value),
    (base_id + 400 + 1350): (b'E008', Snacks.SNACK__3220.value),
    (base_id + 400 + 1351): (b'E008', Snacks.SNACK__3221.value),
    (base_id + 400 + 1352): (b'E008', Snacks.SNACK__3222.value),
    (base_id + 400 + 1353): (b'E008', Snacks.SNACK__32220.value),
    (base_id + 400 + 1354): (b'E008', Snacks.SNACK__32221.value),
    (base_id + 400 + 1355): (b'E008', Snacks.SNACK__32222.value),
    (base_id + 400 + 1356): (b'E008', Snacks.SNACK__322220.value),
    (base_id + 400 + 1357): (b'E008', Snacks.SNACK__322221.value),
    (base_id + 400 + 1358): (b'E008', Snacks.SNACK__322222.value),
    (base_id + 400 + 1359): (b'E008', Snacks.SNACK__330.value),
    (base_id + 400 + 1360): (b'E008', Snacks.SNACK__331.value),
    (base_id + 400 + 1361): (b'E008', Snacks.SNACK__332.value),
    (base_id + 400 + 1362): (b'E008', Snacks.SNACK__3320.value),
    (base_id + 400 + 1363): (b'E008', Snacks.SNACK__3321.value),
    (base_id + 400 + 1364): (b'E008', Snacks.SNACK__3322.value),
    (base_id + 400 + 1365): (b'E008', Snacks.SNACKBOX__1.value),
    (base_id + 400 + 1366): (b'E008', Snacks.SNACKBOX__2.value),

    (base_id + 400 + 1367): (b'E009', Snacks.SNACK__25.value),
    (base_id + 400 + 1368): (b'E009', Snacks.SNACK__250.value),
    (base_id + 400 + 1369): (b'E009', Snacks.SNACK__251.value),
    (base_id + 400 + 1370): (b'E009', Snacks.SNACK__252.value),
    (base_id + 400 + 1371): (b'E009', Snacks.SNACK__253.value),
    (base_id + 400 + 1372): (b'E009', Snacks.SNACK__254.value),
    (base_id + 400 + 1373): (b'E009', Snacks.SNACK__255.value),
    (base_id + 400 + 1374): (b'E009', Snacks.SNACK__256.value),
    (base_id + 400 + 1375): (b'E009', Snacks.SNACK__257.value),
    (base_id + 400 + 1376): (b'E009', Snacks.SNACK__258.value),
    (base_id + 400 + 1377): (b'E009', Snacks.SNACK__259.value),
    (base_id + 400 + 1378): (b'E009', Snacks.SNACK__11.value),
    (base_id + 400 + 1379): (b'E009', Snacks.SNACK__110.value),
    (base_id + 400 + 1380): (b'E009', Snacks.SNACK__111.value),
    (base_id + 400 + 1381): (b'E009', Snacks.SNACK__112.value),
    (base_id + 400 + 1382): (b'E009', Snacks.SNACK__113.value),
    (base_id + 400 + 1383): (b'E009', Snacks.SNACK__114.value),
    (base_id + 400 + 1384): (b'E009', Snacks.SNACK__12.value),
    (base_id + 400 + 1385): (b'E009', Snacks.SNACK__120.value),
    (base_id + 400 + 1386): (b'E009', Snacks.SNACK__121.value),
    (base_id + 400 + 1387): (b'E009', Snacks.SNACK__122.value),
    (base_id + 400 + 1388): (b'E009', Snacks.SNACK__123.value),
    (base_id + 400 + 1389): (b'E009', Snacks.SNACK__274.value),
    (base_id + 400 + 1390): (b'E009', Snacks.SNACK__273.value),
    (base_id + 400 + 1391): (b'E009', Snacks.SNACK__272.value),
    (base_id + 400 + 1392): (b'E009', Snacks.SNACK__271.value),
    (base_id + 400 + 1393): (b'E009', Snacks.SNACK__270.value),
    (base_id + 400 + 1394): (b'E009', Snacks.SNACK__27.value),
    (base_id + 400 + 1395): (b'E009', Snacks.SNACK__275.value),
    (base_id + 400 + 1396): (b'E009', Snacks.SNACK__276.value),
    (base_id + 400 + 1397): (b'E009', Snacks.SNACK__277.value),
    (base_id + 400 + 1398): (b'E009', Snacks.SNACK__278.value),
    (base_id + 400 + 1399): (b'E009', Snacks.SNACK__28.value),
    (base_id + 400 + 1400): (b'E009', Snacks.SNACK__280.value),
    (base_id + 400 + 1401): (b'E009', Snacks.SNACK__281.value),
    (base_id + 400 + 1402): (b'E009', Snacks.SNACK__282.value),
    (base_id + 400 + 1403): (b'E009', Snacks.SNACK__283.value),
    (base_id + 400 + 1404): (b'E009', Snacks.SNACK__29.value),
    (base_id + 400 + 1405): (b'E009', Snacks.SNACK__303.value),
    (base_id + 400 + 1406): (b'E009', Snacks.SNACK__302.value),
    (base_id + 400 + 1407): (b'E009', Snacks.SNACK__301.value),
    (base_id + 400 + 1408): (b'E009', Snacks.SNACK__300.value),
    (base_id + 400 + 1409): (b'E009', Snacks.SNACK__30.value),
    (base_id + 400 + 1410): (b'E009', Snacks.SNACK__304.value),
    (base_id + 400 + 1411): (b'E009', Snacks.SNACK__305.value),
    (base_id + 400 + 1412): (b'E009', Snacks.SNACK__306.value),
    (base_id + 400 + 1413): (b'E009', Snacks.SNACK__307.value),
    (base_id + 400 + 1414): (b'E009', Snacks.SNACK__308.value),
    (base_id + 400 + 1415): (b'E009', Snacks.SNACK__17.value),
    (base_id + 400 + 1416): (b'E009', Snacks.SNACK__170.value),
    (base_id + 400 + 1417): (b'E009', Snacks.SNACK__171.value),
    (base_id + 400 + 1418): (b'E009', Snacks.SNACK__172.value),
    (base_id + 400 + 1419): (b'E009', Snacks.SNACK__18.value),
    (base_id + 400 + 1420): (b'E009', Snacks.SNACK__180.value),
    (base_id + 400 + 1421): (b'E009', Snacks.SNACK__181.value),
    (base_id + 400 + 1422): (b'E009', Snacks.SNACK__182.value),
    (base_id + 400 + 1423): (b'E009', Snacks.SNACK__183.value),
    (base_id + 400 + 1424): (b'E009', Snacks.SNACK__19.value),
    (base_id + 400 + 1425): (b'E009', Snacks.SNACK__190.value),
    (base_id + 400 + 1426): (b'E009', Snacks.SNACK__191.value),
    (base_id + 400 + 1427): (b'E009', Snacks.SNACK__192.value),
    (base_id + 400 + 1428): (b'E009', Snacks.SNACK__193.value),
    (base_id + 400 + 1429): (b'E009', Snacks.SNACK__04.value),
    (base_id + 400 + 1430): (b'E009', Snacks.SNACK__040.value),
    (base_id + 400 + 1431): (b'E009', Snacks.SNACK__041.value),
    (base_id + 400 + 1432): (b'E009', Snacks.SNACK__042.value),
    (base_id + 400 + 1433): (b'E009', Snacks.SNACK__043.value),
    (base_id + 400 + 1434): (b'E009', Snacks.SNACK__20.value),
    (base_id + 400 + 1435): (b'E009', Snacks.SNACK__200.value),
    (base_id + 400 + 1436): (b'E009', Snacks.SNACK__201.value),
    (base_id + 400 + 1437): (b'E009', Snacks.SNACK__202.value),
    (base_id + 400 + 1438): (b'E009', Snacks.SNACK__203.value),
    (base_id + 400 + 1439): (b'E009', Snacks.SNACK__21.value),
    (base_id + 400 + 1440): (b'E009', Snacks.SNACK__210.value),
    (base_id + 400 + 1441): (b'E009', Snacks.SNACK__211.value),
    (base_id + 400 + 1442): (b'E009', Snacks.SNACK__212.value),
    (base_id + 400 + 1443): (b'E009', Snacks.SNACK__213.value),
    (base_id + 400 + 1444): (b'E009', Snacks.SNACK__314.value),
    (base_id + 400 + 1445): (b'E009', Snacks.SNACK__313.value),
    (base_id + 400 + 1446): (b'E009', Snacks.SNACK__312.value),
    (base_id + 400 + 1447): (b'E009', Snacks.SNACK__311.value),
    (base_id + 400 + 1448): (b'E009', Snacks.SNACK__310.value),
    (base_id + 400 + 1449): (b'E009', Snacks.SNACK__31.value),
    (base_id + 400 + 1450): (b'E009', Snacks.SNACK__334.value),
    (base_id + 400 + 1451): (b'E009', Snacks.SNACK__333.value),
    (base_id + 400 + 1452): (b'E009', Snacks.SNACK__332.value),
    (base_id + 400 + 1453): (b'E009', Snacks.SNACK__331.value),
    (base_id + 400 + 1454): (b'E009', Snacks.SNACK__330.value),
    (base_id + 400 + 1455): (b'E009', Snacks.SNACK__33.value),
    (base_id + 400 + 1456): (b'E009', Snacks.SNACKBOX__2.value),
    (base_id + 400 + 1457): (b'E009', Snacks.SNACKBOX__1.value),
    (base_id + 400 + 1458): (b'E009', Snacks.SNACKBOX__3.value),
    (base_id + 400 + 1459): (b'E009', Snacks.CRATE__SNACKBOX__1.value),
    (base_id + 400 + 1460): (b'E009', Snacks.CRATE__SNACKBOX__2.value),
    (base_id + 400 + 1461): (b'E009', Snacks.CRATE__SNACKBOX__3.value),
    (base_id + 400 + 1462): (b'E009', Snacks.CRATE__SNACKBOX__4.value),

    (base_id + 400 + 1463): (b'F001', Snacks.S01.value),
    (base_id + 400 + 1464): (b'F001', Snacks.S02.value),
    (base_id + 400 + 1465): (b'F001', Snacks.S03.value),
    (base_id + 400 + 1466): (b'F001', Snacks.S31.value),
    (base_id + 400 + 1467): (b'F001', Snacks.S32.value),
    (base_id + 400 + 1468): (b'F001', Snacks.S33.value),
    (base_id + 400 + 1469): (b'F001', Snacks.S34_COUNT30.value),
    (base_id + 400 + 1470): (b'F001', Snacks.S06.value),
    (base_id + 400 + 1471): (b'F001', Snacks.S05.value),
    (base_id + 400 + 1472): (b'F001', Snacks.S36.value),
    (base_id + 400 + 1473): (b'F001', Snacks.S07.value),
    (base_id + 400 + 1474): (b'F001', Snacks.S38.value),
    (base_id + 400 + 1475): (b'F001', Snacks.S37.value),
    (base_id + 400 + 1476): (b'F001', Snacks.S39.value),
    (base_id + 400 + 1477): (b'F001', Snacks.S40.value),
    (base_id + 400 + 1478): (b'F001', Snacks.S41.value),
    (base_id + 400 + 1479): (b'F001', Snacks.S43.value),
    (base_id + 400 + 1480): (b'F001', Snacks.S44.value),
    (base_id + 400 + 1481): (b'F001', Snacks.SS54.value),
    (base_id + 400 + 1482): (b'F001', Snacks.SS541.value),
    (base_id + 400 + 1483): (b'F001', Snacks.SS543_COUNT40.value),
    (base_id + 400 + 1484): (b'F001', Snacks.SS701.value),
    (base_id + 400 + 1485): (b'F001', Snacks.SS702.value),
    (base_id + 400 + 1486): (b'F001', Snacks.SS800.value),
    (base_id + 400 + 1487): (b'F001', Snacks.SS801.value),
    (base_id + 400 + 1488): (b'F001', Snacks.SS802_COUNT50.value),
    (base_id + 400 + 1489): (b'F001', Snacks.SS803.value),
    (base_id + 400 + 1490): (b'F001', Snacks.SS804.value),
    (base_id + 400 + 1491): (b'F001', Snacks.SS805.value),
    (base_id + 400 + 1492): (b'F001', Snacks.SS87.value),
    (base_id + 400 + 1493): (b'F001', Snacks.SS1000.value),
    (base_id + 400 + 1494): (b'F001', Snacks.SS1002.value),
    (base_id + 400 + 1495): (b'F001', Snacks.SS1004.value),
    (base_id + 400 + 1496): (b'F001', Snacks.SS1006.value),
    (base_id + 400 + 1497): (b'F001', Snacks.SS1008.value),
    (base_id + 400 + 1498): (b'F001', Snacks.SS116.value),
    (base_id + 400 + 1499): (b'F001', Snacks.SS114_COUNT70.value),
    (base_id + 400 + 1500): (b'F001', Snacks.SS1163.value),
    (base_id + 400 + 1501): (b'F001', Snacks.SS_BP04.value),
    (base_id + 400 + 1502): (b'F001', Snacks.SS_BP09.value),
    (base_id + 400 + 1503): (b'F001', Snacks.SS_BP14.value),
    (base_id + 400 + 1504): (b'F001', Snacks.SS_BP26.value),
    (base_id + 400 + 1505): (b'F001', Snacks.SS_BP28.value),
    (base_id + 400 + 1506): (b'F001', Snacks.SS_BP31.value),
    (base_id + 400 + 1507): (b'F001', Snacks.SS_BP34.value),
    (base_id + 400 + 1508): (b'F001', Snacks.SS_BP46.value),
    (base_id + 400 + 1509): (b'F001', Snacks.SS_BP55.value),
    (base_id + 400 + 1510): (b'F001', Snacks.SS_BP64.value),
    (base_id + 400 + 1511): (b'F001', Snacks.BP_SSBOX03.value),
    (base_id + 400 + 1512): (b'F001', Snacks.SSBOX01.value),
    (base_id + 400 + 1513): (b'F001', Snacks.SSBOX02.value),
    (base_id + 400 + 1514): (b'F001', Snacks.SSBOX08.value),

    (base_id + 400 + 1515): (b'F003', Snacks.SS18.value),
    (base_id + 400 + 1516): (b'F003', Snacks.SS181.value),
    (base_id + 400 + 1517): (b'F003', Snacks.SS183.value),
    (base_id + 400 + 1518): (b'F003', Snacks.SS185.value),
    (base_id + 400 + 1519): (b'F003', Snacks.SS189.value),
    (base_id + 400 + 1520): (b'F003', Snacks.SS1891.value),
    (base_id + 400 + 1521): (b'F003', Snacks.SS1893.value),
    (base_id + 400 + 1522): (b'F003', Snacks.SS1895.value),
    (base_id + 400 + 1523): (b'F003', Snacks.S01_AIR.value),
    (base_id + 400 + 1524): (b'F003', Snacks.S02_AIR.value),
    (base_id + 400 + 1525): (b'F003', Snacks.S4.value),
    (base_id + 400 + 1526): (b'F003', Snacks.S30.value),
    (base_id + 400 + 1527): (b'F003', Snacks.SS196.value),
    (base_id + 400 + 1528): (b'F003', Snacks.SS1960.value),
    (base_id + 400 + 1529): (b'F003', Snacks.SS1961.value),
    (base_id + 400 + 1530): (b'F003', Snacks.SS1962.value),
    (base_id + 400 + 1531): (b'F003', Snacks.SS1963.value),
    (base_id + 400 + 1532): (b'F003', Snacks.SS1964.value),
    (base_id + 400 + 1533): (b'F003', Snacks.SS1965.value),
    (base_id + 400 + 1534): (b'F003', Snacks.SS20.value),
    (base_id + 400 + 1535): (b'F003', Snacks.SS201.value),
    (base_id + 400 + 1536): (b'F003', Snacks.SS203.value),
    (base_id + 400 + 1537): (b'F003', Snacks.SS205.value),
    (base_id + 400 + 1538): (b'F003', Snacks.SS207.value),
    (base_id + 400 + 1539): (b'F003', Snacks.SS209.value),
    (base_id + 400 + 1540): (b'F003', Snacks.S11.value),
    (base_id + 400 + 1541): (b'F003', Snacks.S12.value),
    (base_id + 400 + 1542): (b'F003', Snacks.S13.value),
    (base_id + 400 + 1543): (b'F003', Snacks.S14.value),
    (base_id + 400 + 1544): (b'F003', Snacks.S15.value),
    (base_id + 400 + 1545): (b'F003', Snacks.SS1500.value),
    (base_id + 400 + 1546): (b'F003', Snacks.SS150000.value),
    (base_id + 400 + 1547): (b'F003', Snacks.SS162.value),
    (base_id + 400 + 1548): (b'F003', Snacks.SS16222.value),
    (base_id + 400 + 1549): (b'F003', Snacks.S01.value),
    (base_id + 400 + 1550): (b'F003', Snacks.SS15.value),
    (base_id + 400 + 1551): (b'F003', Snacks.BOX1.value),
    (base_id + 400 + 1552): (b'F003', Snacks.SSBOX05.value),
    (base_id + 400 + 1553): (b'F003', Snacks.SSBOX06.value),
    (base_id + 400 + 1554): (b'F003', Snacks.S8.value),         # Barrel Snack
    (base_id + 400 + 1555): (b'F003', Snacks.SSBOX01.value),
    (base_id + 400 + 1556): (b'F003', Snacks.SSBOX02.value),
    (base_id + 400 + 1557): (b'F003', Snacks.SSBOX03_AIR.value),
    (base_id + 400 + 1558): (b'F003', Snacks.SSBOX04_AIR.value),

    (base_id + 400 + 1559): (b'F004', Snacks.S010.value),
    (base_id + 400 + 1560): (b'F004', Snacks.S011.value),
    (base_id + 400 + 1561): (b'F004', Snacks.S012.value),
    (base_id + 400 + 1562): (b'F004', Snacks.S013.value),
    (base_id + 400 + 1563): (b'F004', Snacks.S014.value),
    (base_id + 400 + 1564): (b'F004', Snacks.S015.value),
    (base_id + 400 + 1565): (b'F004', Snacks.S016.value),
    (base_id + 400 + 1566): (b'F004', Snacks.S02.value),
    (base_id + 400 + 1567): (b'F004', Snacks.S021.value),
    (base_id + 400 + 1568): (b'F004', Snacks.S023.value),
    (base_id + 400 + 1569): (b'F004', Snacks.S025.value),
    (base_id + 400 + 1570): (b'F004', Snacks.S027.value),
    (base_id + 400 + 1571): (b'F004', Snacks.S029.value),
    (base_id + 400 + 1572): (b'F004', Snacks.S030.value),
    (base_id + 400 + 1573): (b'F004', Snacks.S031.value),
    (base_id + 400 + 1574): (b'F004', Snacks.S033.value),
    (base_id + 400 + 1575): (b'F004', Snacks.S04.value),
    (base_id + 400 + 1576): (b'F004', Snacks.S041.value),
    (base_id + 400 + 1577): (b'F004', Snacks.S0411.value),
    (base_id + 400 + 1578): (b'F004', Snacks.S0413.value),
    (base_id + 400 + 1579): (b'F004', Snacks.S0415.value),
    (base_id + 400 + 1580): (b'F004', Snacks.S0417.value),
    (base_id + 400 + 1581): (b'F004', Snacks.S04181.value),
    (base_id + 400 + 1582): (b'F004', Snacks.S04183.value),
    (base_id + 400 + 1583): (b'F004', Snacks.S04185.value),
    (base_id + 400 + 1584): (b'F004', Snacks.S043.value),
    (base_id + 400 + 1585): (b'F004', Snacks.S045.value),
    (base_id + 400 + 1586): (b'F004', Snacks.S047.value),
    (base_id + 400 + 1587): (b'F004', Snacks.S049.value),
    (base_id + 400 + 1588): (b'F004', Snacks.S05.value),
    (base_id + 400 + 1589): (b'F004', Snacks.S06.value),
    (base_id + 400 + 1590): (b'F004', Snacks.S07.value),
    (base_id + 400 + 1591): (b'F004', Snacks.S08.value),
    (base_id + 400 + 1592): (b'F004', Snacks.S080.value),
    (base_id + 400 + 1593): (b'F004', Snacks.S09.value),
    (base_id + 400 + 1594): (b'F004', Snacks.S090.value),
    (base_id + 400 + 1595): (b'F004', Snacks.S10.value),
    (base_id + 400 + 1596): (b'F004', Snacks.S12.value),
    (base_id + 400 + 1597): (b'F004', Snacks.S121.value),
    (base_id + 400 + 1598): (b'F004', Snacks.S123.value),
    (base_id + 400 + 1599): (b'F004', Snacks.S13.value),
    (base_id + 400 + 1600): (b'F004', Snacks.S130.value),
    (base_id + 400 + 1601): (b'F004', Snacks.S132.value),
    (base_id + 400 + 1602): (b'F004', Snacks.S15.value),
    (base_id + 400 + 1603): (b'F004', Snacks.S16.value),
    (base_id + 400 + 1604): (b'F004', Snacks.S17.value),
    (base_id + 400 + 1605): (b'F004', Snacks.S18.value),
    (base_id + 400 + 1606): (b'F004', Snacks.S19.value),
    (base_id + 400 + 1607): (b'F004', Snacks.S191.value),
    (base_id + 400 + 1608): (b'F004', Snacks.S193.value),
    (base_id + 400 + 1609): (b'F004', Snacks.S195.value),
    (base_id + 400 + 1610): (b'F004', Snacks.S197.value),
    (base_id + 400 + 1611): (b'F004', Snacks.S199.value),
    (base_id + 400 + 1612): (b'F004', Snacks.S20.value),
    (base_id + 400 + 1613): (b'F004', Snacks.S201.value),
    (base_id + 400 + 1614): (b'F004', Snacks.S203.value),
    (base_id + 400 + 1615): (b'F004', Snacks.S205.value),
    (base_id + 400 + 1616): (b'F004', Snacks.S2061.value),
    (base_id + 400 + 1617): (b'F004', Snacks.S20611.value),
    (base_id + 400 + 1618): (b'F004', Snacks.S206121.value),
    (base_id + 400 + 1619): (b'F004', Snacks.S2063.value),
    (base_id + 400 + 1620): (b'F004', Snacks.S2065.value),
    (base_id + 400 + 1621): (b'F004', Snacks.S2067.value),
    (base_id + 400 + 1622): (b'F004', Snacks.S2069.value),
    (base_id + 400 + 1623): (b'F004', Snacks.S21.value),
    (base_id + 400 + 1624): (b'F004', Snacks.S23.value),
    (base_id + 400 + 1625): (b'F004', Snacks.S25.value),
    (base_id + 400 + 1626): (b'F004', Snacks.S27.value),
    (base_id + 400 + 1627): (b'F004', Snacks.S29.value),
    (base_id + 400 + 1628): (b'F004', Snacks.S31.value),
    (base_id + 400 + 1629): (b'F004', Snacks.S311.value),
    (base_id + 400 + 1630): (b'F004', Snacks.S313.value),
    (base_id + 400 + 1631): (b'F004', Snacks.S315.value),
    (base_id + 400 + 1632): (b'F004', Snacks.S32.value),
    (base_id + 400 + 1633): (b'F004', Snacks.S321.value),
    (base_id + 400 + 1634): (b'F004', Snacks.S322.value),
    (base_id + 400 + 1635): (b'F004', Snacks.S323.value),
    (base_id + 400 + 1636): (b'F004', Snacks.S324.value),
    (base_id + 400 + 1637): (b'F004', Snacks.S325.value),
    (base_id + 400 + 1638): (b'F004', Snacks.S326.value),
    (base_id + 400 + 1639): (b'F004', Snacks.S90.value),
    (base_id + 400 + 1640): (b'F004', Snacks.S91.value),
    (base_id + 400 + 1641): (b'F004', Snacks.S92.value),
    (base_id + 400 + 1642): (b'F004', Snacks.S94.value),
    (base_id + 400 + 1643): (b'F004', Snacks.SS010.value),
    (base_id + 400 + 1644): (b'F004', Snacks.SS012.value),
    (base_id + 400 + 1645): (b'F004', Snacks.SS014.value),
    (base_id + 400 + 1646): (b'F004', Snacks.SS016.value),
    (base_id + 400 + 1647): (b'F004', Snacks.SS31.value),
    (base_id + 400 + 1648): (b'F004', Snacks.SS32.value),
    (base_id + 400 + 1649): (b'F004', Snacks.SSBOX01.value),
    (base_id + 400 + 1650): (b'F004', Snacks.SSBOX02.value),
    (base_id + 400 + 1651): (b'F004', Snacks.SSBOX03.value),
    (base_id + 400 + 1652): (b'F004', Snacks.SSBOX04.value),

    (base_id + 400 + 1653): (b'F005', Snacks.PLAT04_SS01.value),
    (base_id + 400 + 1654): (b'F005', Snacks.PLAT04_SS010.value),
    (base_id + 400 + 1655): (b'F005', Snacks.PLAT04_SS011.value),
    (base_id + 400 + 1656): (b'F005', Snacks.PLAT04_SS012.value),
    (base_id + 400 + 1657): (b'F005', Snacks.PLAT04_SS013.value),
    (base_id + 400 + 1658): (b'F005', Snacks.PLAT06_SS01.value),
    (base_id + 400 + 1659): (b'F005', Snacks.PLAT06_SS010.value),
    (base_id + 400 + 1660): (b'F005', Snacks.PLAT06_SS011.value),
    (base_id + 400 + 1661): (b'F005', Snacks.PLAT06_SS012.value),
    (base_id + 400 + 1662): (b'F005', Snacks.PLAT06_SS013.value),
    (base_id + 400 + 1663): (b'F005', Snacks.S01.value),
    (base_id + 400 + 1664): (b'F005', Snacks.S02.value),
    (base_id + 400 + 1665): (b'F005', Snacks.S03.value),
    (base_id + 400 + 1666): (b'F005', Snacks.S04.value),
    (base_id + 400 + 1667): (b'F005', Snacks.S05.value),
    (base_id + 400 + 1668): (b'F005', Snacks.S12.value),
    (base_id + 400 + 1669): (b'F005', Snacks.S13.value),
    (base_id + 400 + 1670): (b'F005', Snacks.S14.value),
    (base_id + 400 + 1671): (b'F005', Snacks.S15.value),
    (base_id + 400 + 1672): (b'F005', Snacks.S16.value),
    (base_id + 400 + 1673): (b'F005', Snacks.S17.value),
    (base_id + 400 + 1674): (b'F005', Snacks.S18.value),
    (base_id + 400 + 1675): (b'F005', Snacks.S19.value),
    (base_id + 400 + 1676): (b'F005', Snacks.S20.value),
    (base_id + 400 + 1677): (b'F005', Snacks.S21.value),
    (base_id + 400 + 1678): (b'F005', Snacks.S22.value),
    (base_id + 400 + 1679): (b'F005', Snacks.S23.value),
    (base_id + 400 + 1680): (b'F005', Snacks.S24.value),
    (base_id + 400 + 1681): (b'F005', Snacks.S25.value),
    (base_id + 400 + 1682): (b'F005', Snacks.S26.value),
    (base_id + 400 + 1683): (b'F005', Snacks.S27.value),
    (base_id + 400 + 1684): (b'F005', Snacks.S28.value),
    (base_id + 400 + 1685): (b'F005', Snacks.S29.value),
    (base_id + 400 + 1686): (b'F005', Snacks.S30.value),
    (base_id + 400 + 1687): (b'F005', Snacks.S31.value),
    (base_id + 400 + 1688): (b'F005', Snacks.S32.value),
    (base_id + 400 + 1689): (b'F005', Snacks.S33.value),
    (base_id + 400 + 1690): (b'F005', Snacks.SS400.value),
    (base_id + 400 + 1691): (b'F005', Snacks.SS401.value),
    (base_id + 400 + 1692): (b'F005', Snacks.SS4010.value),
    (base_id + 400 + 1693): (b'F005', Snacks.SS4011.value),
    (base_id + 400 + 1694): (b'F005', Snacks.SS40110.value),
    (base_id + 400 + 1695): (b'F005', Snacks.SS402.value),
    (base_id + 400 + 1696): (b'F005', Snacks.SS403.value),
    (base_id + 400 + 1697): (b'F005', Snacks.SS4030.value),
    (base_id + 400 + 1698): (b'F005', Snacks.SS40300.value),
    (base_id + 400 + 1699): (b'F005', Snacks.SS40301.value),
    (base_id + 400 + 1700): (b'F005', Snacks.SS40302.value),
    (base_id + 400 + 1701): (b'F005', Snacks.SS40303.value),
    (base_id + 400 + 1702): (b'F005', Snacks.SS40304.value),
    (base_id + 400 + 1703): (b'F005', Snacks.SS40305.value),
    (base_id + 400 + 1704): (b'F005', Snacks.SS40306.value),
    (base_id + 400 + 1705): (b'F005', Snacks.SS40307.value),
    (base_id + 400 + 1706): (b'F005', Snacks.SS40308.value),
    (base_id + 400 + 1707): (b'F005', Snacks.SS40309.value),
    (base_id + 400 + 1708): (b'F005', Snacks.SS404.value),
    (base_id + 400 + 1709): (b'F005', Snacks.SS405.value),
    (base_id + 400 + 1710): (b'F005', Snacks.SS406.value),
    (base_id + 400 + 1711): (b'F005', Snacks.SS407.value),
    (base_id + 400 + 1712): (b'F005', Snacks.SS408.value),
    (base_id + 400 + 1713): (b'F005', Snacks.SS409.value),
    (base_id + 400 + 1714): (b'F005', Snacks.SS50.value),
    (base_id + 400 + 1715): (b'F005', Snacks.SS500.value),
    (base_id + 400 + 1716): (b'F005', Snacks.SS501.value),
    (base_id + 400 + 1717): (b'F005', Snacks.SS502.value),
    (base_id + 400 + 1718): (b'F005', Snacks.SS503.value),
    (base_id + 400 + 1719): (b'F005', Snacks.SS504.value),
    (base_id + 400 + 1720): (b'F005', Snacks.SS5040.value),
    (base_id + 400 + 1721): (b'F005', Snacks.SS50400.value),
    (base_id + 400 + 1722): (b'F005', Snacks.SS50401.value),
    (base_id + 400 + 1723): (b'F005', Snacks.SS50402.value),
    (base_id + 400 + 1724): (b'F005', Snacks.SS50403.value),
    (base_id + 400 + 1725): (b'F005', Snacks.SS50404.value),
    (base_id + 400 + 1726): (b'F005', Snacks.SS50405.value),
    (base_id + 400 + 1727): (b'F005', Snacks.SS50406.value),
    (base_id + 400 + 1728): (b'F005', Snacks.SS50407.value),
    (base_id + 400 + 1729): (b'F005', Snacks.SS50408.value),
    (base_id + 400 + 1730): (b'F005', Snacks.SS50409.value),
    (base_id + 400 + 1731): (b'F005', Snacks.SS505.value),
    (base_id + 400 + 1732): (b'F005', Snacks.SS506.value),
    (base_id + 400 + 1733): (b'F005', Snacks.SS508.value),
    (base_id + 400 + 1734): (b'F005', Snacks.SS509.value),
    (base_id + 400 + 1735): (b'F005', Snacks.SSBOX01.value),
    (base_id + 400 + 1736): (b'F005', Snacks.SSBOX02.value),

    (base_id + 400 + 1737): (b'F006', Snacks.S01.value),
    (base_id + 400 + 1738): (b'F006', Snacks.S02.value),
    (base_id + 400 + 1739): (b'F006', Snacks.S03.value),
    (base_id + 400 + 1740): (b'F006', Snacks.S04.value),
    (base_id + 400 + 1741): (b'F006', Snacks.S05.value),
    (base_id + 400 + 1742): (b'F006', Snacks.S06.value),
    (base_id + 400 + 1743): (b'F006', Snacks.S07.value),
    (base_id + 400 + 1744): (b'F006', Snacks.S09.value),
    (base_id + 400 + 1745): (b'F006', Snacks.S10.value),
    (base_id + 400 + 1746): (b'F006', Snacks.S10B.value),
    (base_id + 400 + 1747): (b'F006', Snacks.S10C.value),
    (base_id + 400 + 1748): (b'F006', Snacks.S10D.value),
    (base_id + 400 + 1749): (b'F006', Snacks.S11.value),
    (base_id + 400 + 1750): (b'F006', Snacks.S12.value),
    (base_id + 400 + 1751): (b'F006', Snacks.S13.value),
    (base_id + 400 + 1752): (b'F006', Snacks.S14.value),
    (base_id + 400 + 1753): (b'F006', Snacks.S15.value),
    (base_id + 400 + 1754): (b'F006', Snacks.S16.value),
    (base_id + 400 + 1755): (b'F006', Snacks.S17.value),
    (base_id + 400 + 1756): (b'F006', Snacks.S18.value),
    (base_id + 400 + 1757): (b'F006', Snacks.S18B.value),
    (base_id + 400 + 1758): (b'F006', Snacks.S19.value),
    (base_id + 400 + 1759): (b'F006', Snacks.S19B.value),
    (base_id + 400 + 1760): (b'F006', Snacks.S20.value),
    (base_id + 400 + 1761): (b'F006', Snacks.S20B.value),
    (base_id + 400 + 1762): (b'F006', Snacks.S20C.value),
    (base_id + 400 + 1763): (b'F006', Snacks.S20D.value),
    (base_id + 400 + 1764): (b'F006', Snacks.SS21.value),
    (base_id + 400 + 1765): (b'F006', Snacks.SS22.value),
    (base_id + 400 + 1766): (b'F006', Snacks.SS210.value),
    (base_id + 400 + 1767): (b'F006', Snacks.SS211.value),
    (base_id + 400 + 1768): (b'F006', Snacks.SS212.value),
    (base_id + 400 + 1769): (b'F006', Snacks.SS220.value),
    (base_id + 400 + 1770): (b'F006', Snacks.SS221.value),
    (base_id + 400 + 1771): (b'F006', Snacks.SS222.value),
    (base_id + 400 + 1772): (b'F006', Snacks.SS2120.value),
    (base_id + 400 + 1773): (b'F006', Snacks.SS2121.value),
    (base_id + 400 + 1774): (b'F006', Snacks.SS2122.value),
    (base_id + 400 + 1775): (b'F006', Snacks.SS2123.value),
    (base_id + 400 + 1776): (b'F006', Snacks.SS2124.value),
    (base_id + 400 + 1777): (b'F006', Snacks.SS2126.value),
    (base_id + 400 + 1778): (b'F006', Snacks.SS2129.value),
    (base_id + 400 + 1779): (b'F006', Snacks.SS2220.value),
    (base_id + 400 + 1780): (b'F006', Snacks.SS2221.value),
    (base_id + 400 + 1781): (b'F006', Snacks.SS21210.value),
    (base_id + 400 + 1782): (b'F006', Snacks.SS21211.value),
    (base_id + 400 + 1783): (b'F006', Snacks.SS21212.value),
    (base_id + 400 + 1784): (b'F006', Snacks.SS21213.value),
    (base_id + 400 + 1785): (b'F006', Snacks.SS21214.value),
    (base_id + 400 + 1786): (b'F006', Snacks.SS21215.value),
    (base_id + 400 + 1787): (b'F006', Snacks.SS21216.value),
    (base_id + 400 + 1788): (b'F006', Snacks.SS22210.value),
    (base_id + 400 + 1789): (b'F006', Snacks.SS22211.value),
    (base_id + 400 + 1790): (b'F006', Snacks.SS22212.value),
    (base_id + 400 + 1791): (b'F006', Snacks.SS22213.value),
    (base_id + 400 + 1792): (b'F006', Snacks.SS22214.value),
    (base_id + 400 + 1793): (b'F006', Snacks.SS22215.value),
    (base_id + 400 + 1794): (b'F006', Snacks.SS22216.value),
    (base_id + 400 + 1795): (b'F006', Snacks.SS22217.value),
    (base_id + 400 + 1796): (b'F006', Snacks.SS22218.value),
    (base_id + 400 + 1797): (b'F006', Snacks.SSBOX01.value),
    (base_id + 400 + 1798): (b'F006', Snacks.SSBOX02.value),

    (base_id + 400 + 1799): (b'F007', Snacks.S010.value),
    (base_id + 400 + 1800): (b'F007', Snacks.S011.value),
    (base_id + 400 + 1801): (b'F007', Snacks.S012.value),
    (base_id + 400 + 1802): (b'F007', Snacks.S013.value),
    (base_id + 400 + 1803): (b'F007', Snacks.S014.value),
    (base_id + 400 + 1804): (b'F007', Snacks.S020.value),
    (base_id + 400 + 1805): (b'F007', Snacks.S021.value),
    (base_id + 400 + 1806): (b'F007', Snacks.S022.value),
    (base_id + 400 + 1807): (b'F007', Snacks.S023.value),
    (base_id + 400 + 1808): (b'F007', Snacks.S024.value),
    (base_id + 400 + 1809): (b'F007', Snacks.S030.value),
    (base_id + 400 + 1810): (b'F007', Snacks.S031.value),
    (base_id + 400 + 1811): (b'F007', Snacks.S032.value),
    (base_id + 400 + 1812): (b'F007', Snacks.S033.value),
    (base_id + 400 + 1813): (b'F007', Snacks.S034.value),
    (base_id + 400 + 1814): (b'F007', Snacks.S04.value),
    (base_id + 400 + 1815): (b'F007', Snacks.S040.value),
    (base_id + 400 + 1816): (b'F007', Snacks.S041.value),
    (base_id + 400 + 1817): (b'F007', Snacks.S042.value),
    (base_id + 400 + 1818): (b'F007', Snacks.S043.value),
    (base_id + 400 + 1819): (b'F007', Snacks.S05.value),
    (base_id + 400 + 1820): (b'F007', Snacks.S06.value),
    (base_id + 400 + 1821): (b'F007', Snacks.S07.value),
    (base_id + 400 + 1822): (b'F007', Snacks.S08.value),
    (base_id + 400 + 1823): (b'F007', Snacks.S09.value),
    (base_id + 400 + 1824): (b'F007', Snacks.S10.value),
    (base_id + 400 + 1825): (b'F007', Snacks.S11.value),
    (base_id + 400 + 1826): (b'F007', Snacks.S12.value),
    (base_id + 400 + 1827): (b'F007', Snacks.S13.value),
    (base_id + 400 + 1828): (b'F007', Snacks.S14.value),
    (base_id + 400 + 1829): (b'F007', Snacks.S15.value),
    (base_id + 400 + 1830): (b'F007', Snacks.S16.value),
    (base_id + 400 + 1831): (b'F007', Snacks.S17.value),
    (base_id + 400 + 1832): (b'F007', Snacks.S170.value),
    (base_id + 400 + 1833): (b'F007', Snacks.S171.value),
    (base_id + 400 + 1834): (b'F007', Snacks.S172.value),
    (base_id + 400 + 1835): (b'F007', Snacks.S19.value),
    (base_id + 400 + 1836): (b'F007', Snacks.S190.value),
    (base_id + 400 + 1837): (b'F007', Snacks.S191.value),
    (base_id + 400 + 1838): (b'F007', Snacks.S192.value),
    (base_id + 400 + 1839): (b'F007', Snacks.S193.value),
    (base_id + 400 + 1840): (b'F007', Snacks.S200.value),
    (base_id + 400 + 1841): (b'F007', Snacks.S202.value),
    (base_id + 400 + 1842): (b'F007', Snacks.S204.value),
    (base_id + 400 + 1843): (b'F007', Snacks.S21.value),
    (base_id + 400 + 1844): (b'F007', Snacks.S22.value),
    (base_id + 400 + 1845): (b'F007', Snacks.S24.value),
    (base_id + 400 + 1846): (b'F007', Snacks.S25.value),
    (base_id + 400 + 1847): (b'F007', Snacks.S26.value),
    (base_id + 400 + 1848): (b'F007', Snacks.S300.value),
    (base_id + 400 + 1849): (b'F007', Snacks.S302.value),
    (base_id + 400 + 1850): (b'F007', Snacks.S31.value),
    (base_id + 400 + 1851): (b'F007', Snacks.S310.value),
    (base_id + 400 + 1852): (b'F007', Snacks.S311.value),
    (base_id + 400 + 1853): (b'F007', Snacks.S312.value),
    (base_id + 400 + 1854): (b'F007', Snacks.S314.value),
    (base_id + 400 + 1855): (b'F007', Snacks.S315.value),
    (base_id + 400 + 1856): (b'F007', Snacks.S316.value),
    (base_id + 400 + 1857): (b'F007', Snacks.S317.value),
    (base_id + 400 + 1858): (b'F007', Snacks.S41.value),
    (base_id + 400 + 1859): (b'F007', Snacks.S42.value),
    (base_id + 400 + 1860): (b'F007', Snacks.S43.value),
    (base_id + 400 + 1861): (b'F007', Snacks.S44.value),
    (base_id + 400 + 1862): (b'F007', Snacks.S45.value),
    (base_id + 400 + 1863): (b'F007', Snacks.S450.value),
    (base_id + 400 + 1864): (b'F007', Snacks.SS01.value),
    (base_id + 400 + 1865): (b'F007', Snacks.SS02.value),
    (base_id + 400 + 1866): (b'F007', Snacks.SS03.value),
    (base_id + 400 + 1867): (b'F007', Snacks.SS04.value),
    (base_id + 400 + 1868): (b'F007', Snacks.SS05.value),
    (base_id + 400 + 1869): (b'F007', Snacks.SS99.value),
    (base_id + 400 + 1870): (b'F007', Snacks.SS990.value),
    (base_id + 400 + 1871): (b'F007', Snacks.SS991.value),
    (base_id + 400 + 1872): (b'F007', Snacks.SS9910.value),
    (base_id + 400 + 1873): (b'F007', Snacks.SS9911.value),
    (base_id + 400 + 1874): (b'F007', Snacks.SS9912.value),
    (base_id + 400 + 1875): (b'F007', Snacks.SS9913.value),
    (base_id + 400 + 1876): (b'F007', Snacks.SS9915.value),
    (base_id + 400 + 1877): (b'F007', Snacks.SS9916.value),
    (base_id + 400 + 1878): (b'F007', Snacks.SS9918.value),
    (base_id + 400 + 1879): (b'F007', Snacks.SS99181.value),
    (base_id + 400 + 1880): (b'F007', Snacks.SS9919.value),
    (base_id + 400 + 1881): (b'F007', Snacks.SS992.value),
    (base_id + 400 + 1882): (b'F007', Snacks.SS9921.value),
    (base_id + 400 + 1883): (b'F007', Snacks.SS9923.value),
    (base_id + 400 + 1884): (b'F007', Snacks.SS9925.value),
    (base_id + 400 + 1885): (b'F007', Snacks.SS99251.value),
    (base_id + 400 + 1886): (b'F007', Snacks.SS993.value),
    (base_id + 400 + 1887): (b'F007', Snacks.SS994.value),
    (base_id + 400 + 1888): (b'F007', Snacks.SS995.value),
    (base_id + 400 + 1889): (b'F007', Snacks.SS996.value),
    (base_id + 400 + 1890): (b'F007', Snacks.SS997.value),
    (base_id + 400 + 1891): (b'F007', Snacks.SS998.value),
    (base_id + 400 + 1892): (b'F007', Snacks.SS999.value),
    (base_id + 400 + 1893): (b'F007', Snacks.SSBOX01.value),
    (base_id + 400 + 1894): (b'F007', Snacks.SSBOX02.value),
    (base_id + 400 + 1895): (b'F007', Snacks.SSBOX03.value),
    (base_id + 400 + 1896): (b'F007', Snacks.SSBOX04.value),

    (base_id + 400 + 1897): (b'F008', Snacks.S010.value),
    (base_id + 400 + 1898): (b'F008', Snacks.S011.value),
    (base_id + 400 + 1899): (b'F008', Snacks.S012.value),
    (base_id + 400 + 1900): (b'F008', Snacks.S013.value),
    (base_id + 400 + 1901): (b'F008', Snacks.S020.value),
    (base_id + 400 + 1902): (b'F008', Snacks.S021.value),
    (base_id + 400 + 1903): (b'F008', Snacks.S022.value),
    (base_id + 400 + 1904): (b'F008', Snacks.S03.value),
    (base_id + 400 + 1905): (b'F008', Snacks.S030.value),
    (base_id + 400 + 1906): (b'F008', Snacks.S031.value),
    (base_id + 400 + 1907): (b'F008', Snacks.S04.value),
    (base_id + 400 + 1908): (b'F008', Snacks.S040.value),
    (base_id + 400 + 1909): (b'F008', Snacks.S041.value),
    (base_id + 400 + 1910): (b'F008', Snacks.S042.value),
    (base_id + 400 + 1911): (b'F008', Snacks.S043.value),
    (base_id + 400 + 1912): (b'F008', Snacks.S044.value),
    (base_id + 400 + 1913): (b'F008', Snacks.S045.value),
    (base_id + 400 + 1914): (b'F008', Snacks.S046.value),
    (base_id + 400 + 1915): (b'F008', Snacks.S05.value),
    (base_id + 400 + 1916): (b'F008', Snacks.S06.value),
    (base_id + 400 + 1917): (b'F008', Snacks.S07.value),
    (base_id + 400 + 1918): (b'F008', Snacks.S08.value),
    (base_id + 400 + 1919): (b'F008', Snacks.S09.value),
    (base_id + 400 + 1920): (b'F008', Snacks.S10.value),
    (base_id + 400 + 1921): (b'F008', Snacks.S11.value),
    (base_id + 400 + 1922): (b'F008', Snacks.S12.value),
    (base_id + 400 + 1923): (b'F008', Snacks.S13.value),
    (base_id + 400 + 1924): (b'F008', Snacks.S14.value),
    (base_id + 400 + 1925): (b'F008', Snacks.S15.value),
    (base_id + 400 + 1926): (b'F008', Snacks.S16.value),
    (base_id + 400 + 1927): (b'F008', Snacks.S170.value),
    (base_id + 400 + 1928): (b'F008', Snacks.S171.value),
    (base_id + 400 + 1929): (b'F008', Snacks.S172.value),
    (base_id + 400 + 1930): (b'F008', Snacks.S173.value),
    (base_id + 400 + 1931): (b'F008', Snacks.S174.value),
    (base_id + 400 + 1932): (b'F008', Snacks.S18.value),
    (base_id + 400 + 1933): (b'F008', Snacks.S19.value),
    (base_id + 400 + 1934): (b'F008', Snacks.S20.value),
    (base_id + 400 + 1935): (b'F008', Snacks.S21.value),
    (base_id + 400 + 1936): (b'F008', Snacks.S210.value),
    (base_id + 400 + 1937): (b'F008', Snacks.S211.value),
    (base_id + 400 + 1938): (b'F008', Snacks.S212.value),
    (base_id + 400 + 1939): (b'F008', Snacks.S213.value),
    (base_id + 400 + 1940): (b'F008', Snacks.S214.value),
    (base_id + 400 + 1941): (b'F008', Snacks.S215.value),
    (base_id + 400 + 1942): (b'F008', Snacks.SS01.value),
    (base_id + 400 + 1943): (b'F008', Snacks.SS010.value),
    (base_id + 400 + 1944): (b'F008', Snacks.SS011.value),
    (base_id + 400 + 1945): (b'F008', Snacks.SS012.value),
    (base_id + 400 + 1946): (b'F008', Snacks.SS013.value),
    (base_id + 400 + 1947): (b'F008', Snacks.SS014.value),
    (base_id + 400 + 1948): (b'F008', Snacks.SS015.value),
    (base_id + 400 + 1949): (b'F008', Snacks.SS016.value),
    (base_id + 400 + 1950): (b'F008', Snacks.SS017.value),
    (base_id + 400 + 1951): (b'F008', Snacks.SS018.value),
    (base_id + 400 + 1952): (b'F008', Snacks.SS019.value),
    (base_id + 400 + 1953): (b'F008', Snacks.SS10.value),
    (base_id + 400 + 1954): (b'F008', Snacks.SS11.value),
    (base_id + 400 + 1955): (b'F008', Snacks.SS12.value),
    (base_id + 400 + 1956): (b'F008', Snacks.SS13.value),
    (base_id + 400 + 1957): (b'F008', Snacks.SS22.value),
    (base_id + 400 + 1958): (b'F008', Snacks.SSBOX01.value),

    (base_id + 400 + 1959): (b'F009', Snacks.S010.value),
    (base_id + 400 + 1960): (b'F009', Snacks.S02.value),
    (base_id + 400 + 1961): (b'F009', Snacks.S05.value),
    (base_id + 400 + 1962): (b'F009', Snacks.S06.value),
    (base_id + 400 + 1963): (b'F009', Snacks.S07.value),
    (base_id + 400 + 1964): (b'F009', Snacks.S08.value),
    (base_id + 400 + 1965): (b'F009', Snacks.S09.value),
    (base_id + 400 + 1966): (b'F009', Snacks.S11.value),
    (base_id + 400 + 1967): (b'F009', Snacks.S12.value),
    (base_id + 400 + 1968): (b'F009', Snacks.S13.value),
    (base_id + 400 + 1969): (b'F009', Snacks.S14.value),
    (base_id + 400 + 1970): (b'F009', Snacks.S15.value),
    (base_id + 400 + 1971): (b'F009', Snacks.S33.value),
    (base_id + 400 + 1972): (b'F009', Snacks.S330.value),
    (base_id + 400 + 1973): (b'F009', Snacks.S331.value),
    (base_id + 400 + 1974): (b'F009', Snacks.S332.value),
    (base_id + 400 + 1975): (b'F009', Snacks.S333.value),
    (base_id + 400 + 1976): (b'F009', Snacks.S334.value),
    (base_id + 400 + 1977): (b'F009', Snacks.S335.value),
    (base_id + 400 + 1978): (b'F009', Snacks.S3350.value),
    (base_id + 400 + 1979): (b'F009', Snacks.S3351.value),
    (base_id + 400 + 1980): (b'F009', Snacks.S3352.value),
    (base_id + 400 + 1981): (b'F009', Snacks.S3353.value),
    (base_id + 400 + 1982): (b'F009', Snacks.S3354.value),
    (base_id + 400 + 1983): (b'F009', Snacks.S34.value),
    (base_id + 400 + 1984): (b'F009', Snacks.S340.value),
    (base_id + 400 + 1985): (b'F009', Snacks.S341.value),
    (base_id + 400 + 1986): (b'F009', Snacks.S342.value),
    (base_id + 400 + 1987): (b'F009', Snacks.S343.value),
    (base_id + 400 + 1988): (b'F009', Snacks.S344.value),
    (base_id + 400 + 1989): (b'F009', Snacks.S345.value),
    (base_id + 400 + 1990): (b'F009', Snacks.S346.value),
    (base_id + 400 + 1991): (b'F009', Snacks.S3460.value),
    (base_id + 400 + 1992): (b'F009', Snacks.S3461.value),
    (base_id + 400 + 1993): (b'F009', Snacks.S3462.value),
    (base_id + 400 + 1994): (b'F009', Snacks.S3463.value),
    (base_id + 400 + 1995): (b'F009', Snacks.S3464.value),
    (base_id + 400 + 1996): (b'F009', Snacks.SS01.value),
    (base_id + 400 + 1997): (b'F009', Snacks.SS010.value),
    (base_id + 400 + 1998): (b'F009', Snacks.SS011.value),
    (base_id + 400 + 1999): (b'F009', Snacks.SS012.value),
    (base_id + 400 + 2000): (b'F009', Snacks.SS013.value),
    (base_id + 400 + 2001): (b'F009', Snacks.SS014.value),
    (base_id + 400 + 2002): (b'F009', Snacks.SS015.value),
    (base_id + 400 + 2003): (b'F009', Snacks.SS016.value),
    (base_id + 400 + 2004): (b'F009', Snacks.SS017.value),
    (base_id + 400 + 2005): (b'F009', Snacks.SS018.value),
    (base_id + 400 + 2006): (b'F009', Snacks.SS21.value),
    (base_id + 400 + 2007): (b'F009', Snacks.SS23.value),
    (base_id + 400 + 2008): (b'F009', Snacks.SS25.value),
    (base_id + 400 + 2009): (b'F009', Snacks.SS26.value),
    (base_id + 400 + 2010): (b'F009', Snacks.SS27.value),
    (base_id + 400 + 2011): (b'F009', Snacks.SS28.value),
    (base_id + 400 + 2012): (b'F009', Snacks.SS30.value),
    (base_id + 400 + 2013): (b'F009', Snacks.SS31.value),
    (base_id + 400 + 2014): (b'F009', Snacks.SS32.value),
    (base_id + 400 + 2015): (b'F009', Snacks.SSBOX01.value),
    (base_id + 400 + 2016): (b'F009', Snacks.SSBOX02.value),
    (base_id + 400 + 2017): (b'F009', Snacks.SSBOX03.value),

    (base_id + 400 + 2018): (b'F010', Snacks.BP_SS03.value),
    (base_id + 400 + 2019): (b'F010', Snacks.BP_SS04.value),
    (base_id + 400 + 2020): (b'F010', Snacks.BP_SS05.value),
    (base_id + 400 + 2021): (b'F010', Snacks.BP_SSBOX01.value),
    (base_id + 400 + 2022): (b'F010', Snacks.BP_SSBOX04.value),
    (base_id + 400 + 2023): (b'F010', Snacks.CRATE_SNACK01.value),
    (base_id + 400 + 2024): (b'F010', Snacks.CRATE_SNACK02.value),
    (base_id + 400 + 2025): (b'F010', Snacks.CRATE_SNACK03.value),
    (base_id + 400 + 2026): (b'F010', Snacks.CRATE_SNACK04.value),
    (base_id + 400 + 2027): (b'F010', Snacks.CRATE_SNACK05.value),
    (base_id + 400 + 2028): (b'F010', Snacks.CRATE_SNACK06.value),
    (base_id + 400 + 2029): (b'F010', Snacks.CRATE_SNACK08.value),
    (base_id + 400 + 2030): (b'F010', Snacks.CRATE_SNACK09.value),
    (base_id + 400 + 2031): (b'F010', Snacks.CRATE_SSBOX07.value),
    (base_id + 400 + 2032): (b'F010', Snacks.SS18.value),
    (base_id + 400 + 2033): (b'F010', Snacks.SS180.value),
    (base_id + 400 + 2034): (b'F010', Snacks.SS181.value),
    (base_id + 400 + 2035): (b'F010', Snacks.SS1811.value),
    (base_id + 400 + 2036): (b'F010', Snacks.SS182.value),
    (base_id + 400 + 2037): (b'F010', Snacks.SS183.value),
    (base_id + 400 + 2038): (b'F010', Snacks.SS184.value),
    (base_id + 400 + 2039): (b'F010', Snacks.SS185.value),
    (base_id + 400 + 2040): (b'F010', Snacks.SS1851.value),
    (base_id + 400 + 2041): (b'F010', Snacks.SS1853.value),
    (base_id + 400 + 2042): (b'F010', Snacks.SS1855.value),
    (base_id + 400 + 2043): (b'F010', Snacks.SS187.value),
    (base_id + 400 + 2044): (b'F010', Snacks.SS189.value),
    (base_id + 400 + 2045): (b'F010', Snacks.SS20.value),
    (base_id + 400 + 2046): (b'F010', Snacks.SS8.value),
    (base_id + 400 + 2047): (b'F010', Snacks.SSBOX02.value),
    (base_id + 400 + 2048): (b'F010', Snacks.UPPERDECK_SSBOX04.value),
    (base_id + 400 + 2049): (b'F010', Snacks.UPPERDECK_SSBOX06.value),

    (base_id + 400 + 2050): (b'G001', Snacks.BOX__OF__SNACKS__1.value),
    (base_id + 400 + 2051): (b'G001', Snacks.BOX__OF__SNACKS__2.value),
    (base_id + 400 + 2052): (b'G001', Snacks.BOX__OF__SNACKS__3.value),
    (base_id + 400 + 2053): (b'G001', Snacks.SNACK__01.value),
    (base_id + 400 + 2054): (b'G001', Snacks.SNACK__011.value),
    (base_id + 400 + 2055): (b'G001', Snacks.SNACK__0110.value),
    (base_id + 400 + 2056): (b'G001', Snacks.SNACK__012.value),
    (base_id + 400 + 2057): (b'G001', Snacks.SNACK__013.value),
    (base_id + 400 + 2058): (b'G001', Snacks.SNACK__014.value),
    (base_id + 400 + 2059): (b'G001', Snacks.SNACK__02.value),
    (base_id + 400 + 2060): (b'G001', Snacks.SNACK__04.value),
    (base_id + 400 + 2061): (b'G001', Snacks.SNACK__040.value),
    (base_id + 400 + 2062): (b'G001', Snacks.SNACK__041.value),
    (base_id + 400 + 2063): (b'G001', Snacks.SNACK__042.value),
    (base_id + 400 + 2064): (b'G001', Snacks.SNACK__043.value),
    (base_id + 400 + 2065): (b'G001', Snacks.SNACK__07.value),
    (base_id + 400 + 2066): (b'G001', Snacks.SNACK__070.value),
    (base_id + 400 + 2067): (b'G001', Snacks.SNACK__071.value),
    (base_id + 400 + 2068): (b'G001', Snacks.SNACK__072.value),
    (base_id + 400 + 2069): (b'G001', Snacks.SNACK__073.value),
    (base_id + 400 + 2070): (b'G001', Snacks.SNACK__09.value),
    (base_id + 400 + 2071): (b'G001', Snacks.SNACK__090.value),
    (base_id + 400 + 2072): (b'G001', Snacks.SNACK__091.value),
    (base_id + 400 + 2073): (b'G001', Snacks.SNACK__092.value),
    (base_id + 400 + 2074): (b'G001', Snacks.SNACK__093.value),
    (base_id + 400 + 2075): (b'G001', Snacks.SNACK__10.value),
    (base_id + 400 + 2076): (b'G001', Snacks.SNACK__100.value),
    (base_id + 400 + 2077): (b'G001', Snacks.SNACK__101.value),
    (base_id + 400 + 2078): (b'G001', Snacks.SNACK__102.value),
    (base_id + 400 + 2079): (b'G001', Snacks.SNACK__103.value),
    (base_id + 400 + 2080): (b'G001', Snacks.SNACK__104.value),
    (base_id + 400 + 2081): (b'G001', Snacks.SS1.value),
    (base_id + 400 + 2082): (b'G001', Snacks.SS10.value),
    (base_id + 400 + 2083): (b'G001', Snacks.SS11.value),
    (base_id + 400 + 2084): (b'G001', Snacks.SS110.value),
    (base_id + 400 + 2085): (b'G001', Snacks.SS1100.value),
    (base_id + 400 + 2086): (b'G001', Snacks.SS1101.value),
    (base_id + 400 + 2087): (b'G001', Snacks.SS1102.value),
    (base_id + 400 + 2088): (b'G001', Snacks.SS1103.value),
    (base_id + 400 + 2089): (b'G001', Snacks.SS1104.value),
    (base_id + 400 + 2090): (b'G001', Snacks.SS1105.value),
    (base_id + 400 + 2091): (b'G001', Snacks.SS1106.value),
    (base_id + 400 + 2092): (b'G001', Snacks.SS1107.value),
    (base_id + 400 + 2093): (b'G001', Snacks.SS1109.value),
    (base_id + 400 + 2094): (b'G001', Snacks.SS12.value),
    (base_id + 400 + 2095): (b'G001', Snacks.SS13.value),
    (base_id + 400 + 2096): (b'G001', Snacks.SS15.value),
    (base_id + 400 + 2097): (b'G001', Snacks.SS16.value),
    (base_id + 400 + 2098): (b'G001', Snacks.SS17.value),
    (base_id + 400 + 2099): (b'G001', Snacks.SS18.value),
    (base_id + 400 + 2100): (b'G001', Snacks.SS19.value),

    (base_id + 400 + 2101): (b'G002', Snacks.BOX__OF__SNACKS__01.value),
    (base_id + 400 + 2102): (b'G002', Snacks.SNACK__1.value),
    (base_id + 400 + 2103): (b'G002', Snacks.SNACK__10.value),
    (base_id + 400 + 2104): (b'G002', Snacks.SNACK__100.value),
    (base_id + 400 + 2105): (b'G002', Snacks.SNACK__11.value),
    (base_id + 400 + 2106): (b'G002', Snacks.SNACK__12.value),
    (base_id + 400 + 2107): (b'G002', Snacks.SNACK__120.value),
    (base_id + 400 + 2108): (b'G002', Snacks.SNACK__13.value),
    (base_id + 400 + 2109): (b'G002', Snacks.SNACK__131.value),
    (base_id + 400 + 2110): (b'G002', Snacks.SNACK__132.value),
    (base_id + 400 + 2111): (b'G002', Snacks.SNACK__133.value),
    (base_id + 400 + 2112): (b'G002', Snacks.SNACK__15.value),
    (base_id + 400 + 2113): (b'G002', Snacks.SNACK__16.value),
    (base_id + 400 + 2114): (b'G002', Snacks.SNACK__17.value),
    (base_id + 400 + 2115): (b'G002', Snacks.SNACK__18.value),
    (base_id + 400 + 2116): (b'G002', Snacks.SNACK__2.value),
    (base_id + 400 + 2117): (b'G002', Snacks.SNACK__20.value),
    (base_id + 400 + 2118): (b'G002', Snacks.SNACK__21.value),
    (base_id + 400 + 2119): (b'G002', Snacks.SNACK__3.value),
    (base_id + 400 + 2120): (b'G002', Snacks.SNACK__30.value),
    (base_id + 400 + 2121): (b'G002', Snacks.SNACK__31.value),
    (base_id + 400 + 2122): (b'G002', Snacks.SNACK__32.value),
    (base_id + 400 + 2123): (b'G002', Snacks.SNACK__4.value),
    (base_id + 400 + 2124): (b'G002', Snacks.SNACK__40.value),
    (base_id + 400 + 2125): (b'G002', Snacks.SNACK__41.value),
    (base_id + 400 + 2126): (b'G002', Snacks.SNACK__42.value),
    (base_id + 400 + 2127): (b'G002', Snacks.SNACK__43.value),
    (base_id + 400 + 2128): (b'G002', Snacks.SNACK__7.value),
    (base_id + 400 + 2129): (b'G002', Snacks.SNACK__70.value),
    (base_id + 400 + 2130): (b'G002', Snacks.SNACK__71.value),
    (base_id + 400 + 2131): (b'G002', Snacks.SNACK__8.value),
    (base_id + 400 + 2132): (b'G002', Snacks.SNACK__80.value),
    (base_id + 400 + 2133): (b'G002', Snacks.SNACK__81.value),
    (base_id + 400 + 2134): (b'G002', Snacks.SNACK__9.value),
    (base_id + 400 + 2135): (b'G002', Snacks.SNACK__90.value),
    (base_id + 400 + 2136): (b'G002', Snacks.SNACK__91.value),
    (base_id + 400 + 2137): (b'G002', Snacks.SS10.value),
    (base_id + 400 + 2138): (b'G002', Snacks.SS11.value),
    (base_id + 400 + 2139): (b'G002', Snacks.SS12.value),
    (base_id + 400 + 2140): (b'G002', Snacks.SS13.value),
    (base_id + 400 + 2141): (b'G002', Snacks.SS130.value),
    (base_id + 400 + 2142): (b'G002', Snacks.SS131.value),
    (base_id + 400 + 2143): (b'G002', Snacks.SS132.value),
    (base_id + 400 + 2144): (b'G002', Snacks.SS134.value),
    (base_id + 400 + 2145): (b'G002', Snacks.SS135.value),
    (base_id + 400 + 2146): (b'G002', Snacks.SS136.value),
    (base_id + 400 + 2147): (b'G002', Snacks.SS14.value),
    (base_id + 400 + 2148): (b'G002', Snacks.SS15.value),
    (base_id + 400 + 2149): (b'G002', Snacks.SS16.value),

    (base_id + 400 + 2150): (b'G003', Snacks.SS110.value),
    (base_id + 400 + 2151): (b'G003', Snacks.SS111.value),
    (base_id + 400 + 2152): (b'G003', Snacks.SS112.value),
    (base_id + 400 + 2153): (b'G003', Snacks.BOX__OF__SNACKS__1.value),
    (base_id + 400 + 2154): (b'G003', Snacks.BOX__OF__SNACKS__2.value),
    (base_id + 400 + 2155): (b'G003', Snacks.SNACK__01.value),
    (base_id + 400 + 2156): (b'G003', Snacks.SNACK__03.value),
    (base_id + 400 + 2157): (b'G003', Snacks.SNACK__04.value),
    (base_id + 400 + 2158): (b'G003', Snacks.SNACK__05.value),
    (base_id + 400 + 2159): (b'G003', Snacks.SNACK__06.value),
    (base_id + 400 + 2160): (b'G003', Snacks.SNACK__07.value),
    (base_id + 400 + 2161): (b'G003', Snacks.SNACK__08.value),
    (base_id + 400 + 2162): (b'G003', Snacks.SNACK__09.value),
    (base_id + 400 + 2163): (b'G003', Snacks.SNACK__010.value),
    (base_id + 400 + 2164): (b'G003', Snacks.SNACK__011.value),
    (base_id + 400 + 2165): (b'G003', Snacks.SNACK__11.value),
    (base_id + 400 + 2166): (b'G003', Snacks.SNACK__012.value),
    (base_id + 400 + 2167): (b'G003', Snacks.SNACK__013.value),
    (base_id + 400 + 2168): (b'G003', Snacks.SNACK__14.value),
    (base_id + 400 + 2169): (b'G003', Snacks.SNACK__15.value),
    (base_id + 400 + 2170): (b'G003', Snacks.SNACK__16.value),
    (base_id + 400 + 2171): (b'G003', Snacks.SNACK__17.value),
    (base_id + 400 + 2172): (b'G003', Snacks.SNACK__18.value),
    (base_id + 400 + 2173): (b'G003', Snacks.SNACK__050.value),
    (base_id + 400 + 2174): (b'G003', Snacks.SNACK__060.value),
    (base_id + 400 + 2175): (b'G003', Snacks.SNACK__070.value),
    (base_id + 400 + 2176): (b'G003', Snacks.SNACK__080.value),
    (base_id + 400 + 2177): (b'G003', Snacks.SNACK__090.value),
    (base_id + 400 + 2178): (b'G003', Snacks.SNACK__091.value),
    (base_id + 400 + 2179): (b'G003', Snacks.SNACK__092.value),
    (base_id + 400 + 2180): (b'G003', Snacks.SNACK__093.value),
    (base_id + 400 + 2181): (b'G003', Snacks.SNACK__110.value),
    (base_id + 400 + 2182): (b'G003', Snacks.SNACK__111.value),
    (base_id + 400 + 2183): (b'G003', Snacks.SNACK__112.value),
    (base_id + 400 + 2184): (b'G003', Snacks.SNACK__113.value),
    (base_id + 400 + 2185): (b'G003', Snacks.SNACK__160.value),
    (base_id + 400 + 2186): (b'G003', Snacks.SNACK__170.value),
    (base_id + 400 + 2187): (b'G003', Snacks.SNACK__171.value),
    (base_id + 400 + 2188): (b'G003', Snacks.SNACK__172.value),
    (base_id + 400 + 2189): (b'G003', Snacks.SNACK__174.value),
    (base_id + 400 + 2190): (b'G003', Snacks.SNACK__1130.value),
    (base_id + 400 + 2191): (b'G003', Snacks.SNACK__1131.value),
    (base_id + 400 + 2192): (b'G003', Snacks.SNACKBOX__3.value),
    (base_id + 400 + 2193): (b'G003', Snacks.SS1.value),
    (base_id + 400 + 2194): (b'G003', Snacks.SS10.value),
    (base_id + 400 + 2195): (b'G003', Snacks.SS11.value),
    (base_id + 400 + 2196): (b'G003', Snacks.SS12.value),
    (base_id + 400 + 2197): (b'G003', Snacks.SS13.value),
    (base_id + 400 + 2198): (b'G003', Snacks.SS14.value),
    (base_id + 400 + 2199): (b'G003', Snacks.SS15.value),
    (base_id + 400 + 2200): (b'G003', Snacks.SS16.value),
    (base_id + 400 + 2201): (b'G003', Snacks.SS17.value),
    (base_id + 400 + 2202): (b'G003', Snacks.SS18.value),
    (base_id + 400 + 2203): (b'G003', Snacks.SS19.value),

    (base_id + 400 + 2204): (b'G004', Snacks.SNACK__061.value),
    (base_id + 400 + 2205): (b'G004', Snacks.SNACK__062.value),
    (base_id + 400 + 2206): (b'G004', Snacks.SNACK__063.value),
    (base_id + 400 + 2207): (b'G004', Snacks.SNACK__064.value),
    (base_id + 400 + 2208): (b'G004', Snacks.SNACK__065.value),
    (base_id + 400 + 2209): (b'G004', Snacks.SNACK__01.value),
    (base_id + 400 + 2210): (b'G004', Snacks.SNACK__02.value),
    (base_id + 400 + 2211): (b'G004', Snacks.SNACK__03.value),
    (base_id + 400 + 2212): (b'G004', Snacks.SNACK__04.value),
    (base_id + 400 + 2213): (b'G004', Snacks.SNACK__06.value),
    (base_id + 400 + 2214): (b'G004', Snacks.SNACK__010.value),
    (base_id + 400 + 2215): (b'G004', Snacks.SNACK__011.value),
    (base_id + 400 + 2216): (b'G004', Snacks.SNACK__012.value),
    (base_id + 400 + 2217): (b'G004', Snacks.SNACK__013.value),
    (base_id + 400 + 2218): (b'G004', Snacks.SNACK__014.value),
    (base_id + 400 + 2219): (b'G004', Snacks.SNACK__015.value),
    (base_id + 400 + 2220): (b'G004', Snacks.SNACK__020.value),
    (base_id + 400 + 2221): (b'G004', Snacks.SNACK__021.value),
    (base_id + 400 + 2223): (b'G004', Snacks.SNACK__023.value),
    (base_id + 400 + 2224): (b'G004', Snacks.SNACK__024.value),
    (base_id + 400 + 2225): (b'G004', Snacks.SNACK__025.value),
    (base_id + 400 + 2226): (b'G004', Snacks.SNACK__030.value),
    (base_id + 400 + 2227): (b'G004', Snacks.SNACK__031.value),
    (base_id + 400 + 2228): (b'G004', Snacks.SNACK__032.value),
    (base_id + 400 + 2229): (b'G004', Snacks.SNACK__033.value),
    (base_id + 400 + 2230): (b'G004', Snacks.SNACK__034.value),
    (base_id + 400 + 2231): (b'G004', Snacks.SNACK__035.value),
    (base_id + 400 + 2232): (b'G004', Snacks.SNACK__036.value),
    (base_id + 400 + 2233): (b'G004', Snacks.SNACK__037.value),
    (base_id + 400 + 2234): (b'G004', Snacks.SNACK__038.value),
    (base_id + 400 + 2235): (b'G004', Snacks.SNACK__039.value),
    (base_id + 400 + 2236): (b'G004', Snacks.SNACK__040.value),
    (base_id + 400 + 2237): (b'G004', Snacks.SNACK__041.value),
    (base_id + 400 + 2238): (b'G004', Snacks.SNACK__042.value),
    (base_id + 400 + 2239): (b'G004', Snacks.SNACK__043.value),
    (base_id + 400 + 2240): (b'G004', Snacks.SNACK__044.value),
    (base_id + 400 + 2241): (b'G004', Snacks.SNACK__045.value),
    (base_id + 400 + 2242): (b'G004', Snacks.SNACK__046.value),
    (base_id + 400 + 2243): (b'G004', Snacks.SNACK__047.value),
    (base_id + 400 + 2244): (b'G004', Snacks.SNACK__048.value),
    (base_id + 400 + 2245): (b'G004', Snacks.SNACK__049.value),
    (base_id + 400 + 2246): (b'G004', Snacks.SNACK__060.value),

    (base_id + 400 + 2247): (b'G005', Snacks.SNACK__01.value),
    (base_id + 400 + 2248): (b'G005', Snacks.SNACK__010.value),
    (base_id + 400 + 2249): (b'G005', Snacks.SNACK__011.value),
    (base_id + 400 + 2250): (b'G005', Snacks.SNACK__012.value),
    (base_id + 400 + 2251): (b'G005', Snacks.SNACK__013.value),
    (base_id + 400 + 2252): (b'G005', Snacks.SNACK__014.value),
    (base_id + 400 + 2253): (b'G005', Snacks.SNACK__015.value),
    (base_id + 400 + 2254): (b'G005', Snacks.SNACK__016.value),
    (base_id + 400 + 2255): (b'G005', Snacks.SNACK__04.value),
    (base_id + 400 + 2256): (b'G005', Snacks.SNACK__06.value),
    (base_id + 400 + 2257): (b'G005', Snacks.SNACK__07.value),
    (base_id + 400 + 2258): (b'G005', Snacks.SNACK__08.value),
    (base_id + 400 + 2259): (b'G005', Snacks.SNACK__080.value),
    (base_id + 400 + 2260): (b'G005', Snacks.SNACK__081.value),
    (base_id + 400 + 2261): (b'G005', Snacks.SNACK__082.value),
    (base_id + 400 + 2262): (b'G005', Snacks.SNACK__083.value),
    (base_id + 400 + 2263): (b'G005', Snacks.SNACK__0830.value),
    (base_id + 400 + 2264): (b'G005', Snacks.SNACK__0831.value),
    (base_id + 400 + 2265): (b'G005', Snacks.SNACK__0832.value),
    (base_id + 400 + 2266): (b'G005', Snacks.SNACK__08320.value),
    (base_id + 400 + 2267): (b'G005', Snacks.SNACK__08321.value),
    (base_id + 400 + 2268): (b'G005', Snacks.SNACK__08322.value),
    (base_id + 400 + 2269): (b'G005', Snacks.SNACK__09.value),
    (base_id + 400 + 2270): (b'G005', Snacks.SNACK__090.value),
    (base_id + 400 + 2271): (b'G005', Snacks.SNACK__091.value),
    (base_id + 400 + 2272): (b'G005', Snacks.SNACK__092.value),
    (base_id + 400 + 2273): (b'G005', Snacks.SNACK__093.value),
    (base_id + 400 + 2274): (b'G005', Snacks.SNACK__094.value),
    (base_id + 400 + 2275): (b'G005', Snacks.SNACK__11.value),
    (base_id + 400 + 2276): (b'G005', Snacks.SNACK__110.value),
    (base_id + 400 + 2277): (b'G005', Snacks.SNACK__111.value),
    (base_id + 400 + 2278): (b'G005', Snacks.SNACK__112.value),
    (base_id + 400 + 2279): (b'G005', Snacks.SNACK__113.value),
    (base_id + 400 + 2280): (b'G005', Snacks.SNACK__114.value),
    (base_id + 400 + 2281): (b'G005', Snacks.SNACK__12.value),
    (base_id + 400 + 2282): (b'G005', Snacks.SNACK__120.value),
    (base_id + 400 + 2283): (b'G005', Snacks.SNACK__121.value),
    (base_id + 400 + 2284): (b'G005', Snacks.SNACK__122.value),
    (base_id + 400 + 2285): (b'G005', Snacks.SNACK__123.value),
    (base_id + 400 + 2286): (b'G005', Snacks.SNACK__124.value),
    (base_id + 400 + 2287): (b'G005', Snacks.SNACK__13.value),
    (base_id + 400 + 2288): (b'G005', Snacks.SNACK__130.value),
    (base_id + 400 + 2289): (b'G005', Snacks.SNACK__131.value),
    (base_id + 400 + 2290): (b'G005', Snacks.SNACK__132.value),
    (base_id + 400 + 2291): (b'G005', Snacks.SNACK__133.value),
    (base_id + 400 + 2292): (b'G005', Snacks.SNACK__1330.value),
    (base_id + 400 + 2293): (b'G005', Snacks.SNACK__1331.value),
    (base_id + 400 + 2294): (b'G005', Snacks.SNACK__1332.value),
    (base_id + 400 + 2295): (b'G005', Snacks.SNACK__1333.value),
    (base_id + 400 + 2296): (b'G005', Snacks.SNACK__14.value),
    (base_id + 400 + 2297): (b'G005', Snacks.SNACK__140.value),
    (base_id + 400 + 2298): (b'G005', Snacks.SNACK__141.value),
    (base_id + 400 + 2299): (b'G005', Snacks.SNACK__142.value),
    (base_id + 400 + 2300): (b'G005', Snacks.SNACK__143.value),
    (base_id + 400 + 2301): (b'G005', Snacks.SNACK__144.value),
    (base_id + 400 + 2302): (b'G005', Snacks.SNACKBOX__1.value),

    (base_id + 400 + 2303): (b'G006', Snacks.SNACK__01.value),
    (base_id + 400 + 2304): (b'G006', Snacks.SNACK__010.value),
    (base_id + 400 + 2305): (b'G006', Snacks.SNACK__011.value),
    (base_id + 400 + 2306): (b'G006', Snacks.SNACK__012.value),
    (base_id + 400 + 2307): (b'G006', Snacks.SNACK__013.value),
    (base_id + 400 + 2308): (b'G006', Snacks.SNACK__014.value),
    (base_id + 400 + 2309): (b'G006', Snacks.SNACK__015.value),
    (base_id + 400 + 2310): (b'G006', Snacks.SNACK__07.value),
    (base_id + 400 + 2311): (b'G006', Snacks.SNACK__070.value),
    (base_id + 400 + 2312): (b'G006', Snacks.SNACK__071.value),
    (base_id + 400 + 2313): (b'G006', Snacks.SNACK__072.value),
    (base_id + 400 + 2314): (b'G006', Snacks.SNACK__073.value),
    (base_id + 400 + 2315): (b'G006', Snacks.SNACK__07330.value),
    (base_id + 400 + 2316): (b'G006', Snacks.SNACK__07331.value),
    (base_id + 400 + 2317): (b'G006', Snacks.SNACK__07332.value),
    (base_id + 400 + 2318): (b'G006', Snacks.SNACK__07333.value),
    (base_id + 400 + 2319): (b'G006', Snacks.SNACK__07334.value),
    (base_id + 400 + 2320): (b'G006', Snacks.SNACK__07335.value),
    (base_id + 400 + 2321): (b'G006', Snacks.SNACK__07336.value),
    (base_id + 400 + 2322): (b'G006', Snacks.SNACK__10.value),
    (base_id + 400 + 2323): (b'G006', Snacks.SNACK__100.value),
    (base_id + 400 + 2324): (b'G006', Snacks.SNACK__101.value),
    (base_id + 400 + 2325): (b'G006', Snacks.SNACK__102.value),
    (base_id + 400 + 2326): (b'G006', Snacks.SNACK__103.value),
    (base_id + 400 + 2327): (b'G006', Snacks.SNACK__104.value),
    (base_id + 400 + 2328): (b'G006', Snacks.SNACK__14.value),
    (base_id + 400 + 2329): (b'G006', Snacks.SNACK__140.value),
    (base_id + 400 + 2330): (b'G006', Snacks.SNACK__141.value),
    (base_id + 400 + 2331): (b'G006', Snacks.SNACK__142.value),
    (base_id + 400 + 2332): (b'G006', Snacks.SNACK__143.value),
    (base_id + 400 + 2333): (b'G006', Snacks.SNACK__17.value),
    (base_id + 400 + 2334): (b'G006', Snacks.SNACK__170.value),
    (base_id + 400 + 2335): (b'G006', Snacks.SNACK__171.value),
    (base_id + 400 + 2336): (b'G006', Snacks.SNACK__172.value),
    (base_id + 400 + 2337): (b'G006', Snacks.SNACK__173.value),
    (base_id + 400 + 2338): (b'G006', Snacks.SNACK__174.value),
    (base_id + 400 + 2339): (b'G006', Snacks.SNACK__BOX__1.value),
    (base_id + 400 + 2340): (b'G006', Snacks.SNACKBOX__3.value),
    (base_id + 400 + 2341): (b'G006', Snacks.URN__1__PRIZE.value),
    (base_id + 400 + 2342): (b'G006', Snacks.URN__2__PRIZE.value),

    (base_id + 400 + 2343): (b'G007', Snacks.BOX__OF__SNACKS__1.value),
    (base_id + 400 + 2344): (b'G007', Snacks.BOX__OF__SNACKS__2.value),
    (base_id + 400 + 2345): (b'G007', Snacks.BOX__OF__SNACKS__5.value),
    (base_id + 400 + 2346): (b'G007', Snacks.SNACK__02.value),
    (base_id + 400 + 2347): (b'G007', Snacks.SNACK__020.value),
    (base_id + 400 + 2348): (b'G007', Snacks.SNACK__021.value),
    (base_id + 400 + 2349): (b'G007', Snacks.SNACK__023.value),
    (base_id + 400 + 2350): (b'G007', Snacks.SNACK__024.value),
    (base_id + 400 + 2351): (b'G007', Snacks.SNACK__025.value),
    (base_id + 400 + 2352): (b'G007', Snacks.SNACK__04.value),
    (base_id + 400 + 2353): (b'G007', Snacks.SNACK__040.value),
    (base_id + 400 + 2354): (b'G007', Snacks.SNACK__041.value),
    (base_id + 400 + 2355): (b'G007', Snacks.SNACK__042.value),
    (base_id + 400 + 2356): (b'G007', Snacks.SNACK__043.value),
    (base_id + 400 + 2357): (b'G007', Snacks.SNACK__044.value),
    (base_id + 400 + 2358): (b'G007', Snacks.SNACK__045.value),
    (base_id + 400 + 2359): (b'G007', Snacks.SNACK__05.value),
    (base_id + 400 + 2360): (b'G007', Snacks.SNACK__050.value),
    (base_id + 400 + 2361): (b'G007', Snacks.SNACK__051.value),
    (base_id + 400 + 2362): (b'G007', Snacks.SNACK__052.value),
    (base_id + 400 + 2363): (b'G007', Snacks.SNACK__053.value),
    (base_id + 400 + 2364): (b'G007', Snacks.SNACK__054.value),
    (base_id + 400 + 2365): (b'G007', Snacks.SNACK__055.value),
    (base_id + 400 + 2366): (b'G007', Snacks.SNACK__056.value),
    (base_id + 400 + 2367): (b'G007', Snacks.SNACK__06.value),
    (base_id + 400 + 2368): (b'G007', Snacks.SNACK__060.value),
    (base_id + 400 + 2369): (b'G007', Snacks.SNACK__061.value),
    (base_id + 400 + 2370): (b'G007', Snacks.SNACK__062.value),
    (base_id + 400 + 2371): (b'G007', Snacks.SNACK__063.value),
    (base_id + 400 + 2372): (b'G007', Snacks.SNACK__064.value),
    (base_id + 400 + 2373): (b'G007', Snacks.SNACK__065.value),
    (base_id + 400 + 2374): (b'G007', Snacks.SNACK__066.value),
    (base_id + 400 + 2375): (b'G007', Snacks.SNACK__067.value),
    (base_id + 400 + 2376): (b'G007', Snacks.SNACK__068.value),
    (base_id + 400 + 2377): (b'G007', Snacks.SNACK__08.value),
    (base_id + 400 + 2378): (b'G007', Snacks.SNACK__080.value),
    (base_id + 400 + 2379): (b'G007', Snacks.SNACK__081.value),
    (base_id + 400 + 2380): (b'G007', Snacks.SNACK__082.value),
    (base_id + 400 + 2381): (b'G007', Snacks.SNACK__083.value),
    (base_id + 400 + 2382): (b'G007', Snacks.SNACK__084.value),
    (base_id + 400 + 2383): (b'G007', Snacks.SNACK__085.value),
    (base_id + 400 + 2384): (b'G007', Snacks.SNACK__09.value),
    (base_id + 400 + 2385): (b'G007', Snacks.SNACK__090.value),
    (base_id + 400 + 2386): (b'G007', Snacks.SNACK__091.value),
    (base_id + 400 + 2387): (b'G007', Snacks.SNACK__092.value),
    (base_id + 400 + 2388): (b'G007', Snacks.SNACK__093.value),
    (base_id + 400 + 2389): (b'G007', Snacks.SNACK__094.value),
    (base_id + 400 + 2390): (b'G007', Snacks.SNACK__095.value),
    (base_id + 400 + 2391): (b'G007', Snacks.SNACK__096.value),
    (base_id + 400 + 2392): (b'G007', Snacks.SNACK__666.value),
    (base_id + 400 + 2393): (b'G007', Snacks.SS1.value),
    (base_id + 400 + 2394): (b'G007', Snacks.SS10.value),
    (base_id + 400 + 2395): (b'G007', Snacks.SS11.value),
    (base_id + 400 + 2396): (b'G007', Snacks.SS12.value),
    (base_id + 400 + 2397): (b'G007', Snacks.SS13.value),
    (base_id + 400 + 2398): (b'G007', Snacks.SS15.value),
    (base_id + 400 + 2399): (b'G007', Snacks.SS16.value),
    (base_id + 400 + 2400): (b'G007', Snacks.SS17.value),
    (base_id + 400 + 2401): (b'G007', Snacks.SS18.value),
    (base_id + 400 + 2402): (b'G007', Snacks.SS19.value),

    (base_id + 400 + 2403): (b'G008', Snacks.SNACK__010.value),
    (base_id + 400 + 2404): (b'G008', Snacks.SNACK__011.value),
    (base_id + 400 + 2405): (b'G008', Snacks.SNACK__012.value),
    (base_id + 400 + 2406): (b'G008', Snacks.SNACK__013.value),
    (base_id + 400 + 2407): (b'G008', Snacks.SNACK__014.value),
    (base_id + 400 + 2408): (b'G008', Snacks.SNACK__015.value),
    (base_id + 400 + 2409): (b'G008', Snacks.SNACK__07.value),
    (base_id + 400 + 2410): (b'G008', Snacks.SNACK__070.value),
    (base_id + 400 + 2411): (b'G008', Snacks.SNACK__071.value),
    (base_id + 400 + 2412): (b'G008', Snacks.SNACK__072.value),
    (base_id + 400 + 2413): (b'G008', Snacks.SNACK__073.value),
    (base_id + 400 + 2414): (b'G008', Snacks.SNACK__074.value),
    (base_id + 400 + 2415): (b'G008', Snacks.SNACK__075.value),
    (base_id + 400 + 2416): (b'G008', Snacks.SNACK__08.value),
    (base_id + 400 + 2417): (b'G008', Snacks.SNACK__080.value),
    (base_id + 400 + 2418): (b'G008', Snacks.SNACK__081.value),
    (base_id + 400 + 2419): (b'G008', Snacks.SNACK__082.value),
    (base_id + 400 + 2420): (b'G008', Snacks.SNACK__083.value),
    (base_id + 400 + 2421): (b'G008', Snacks.SNACK__084.value),
    (base_id + 400 + 2422): (b'G008', Snacks.SNACK__09.value),
    (base_id + 400 + 2423): (b'G008', Snacks.SNACK__090.value),
    (base_id + 400 + 2424): (b'G008', Snacks.SNACK__091.value),
    (base_id + 400 + 2425): (b'G008', Snacks.SNACK__092.value),
    (base_id + 400 + 2426): (b'G008', Snacks.SNACK__093.value),
    (base_id + 400 + 2427): (b'G008', Snacks.SNACK__094.value),
    (base_id + 400 + 2428): (b'G008', Snacks.SNACK__095.value),
    (base_id + 400 + 2429): (b'G008', Snacks.SNACK__11.value),
    (base_id + 400 + 2430): (b'G008', Snacks.SNACK__110.value),
    (base_id + 400 + 2431): (b'G008', Snacks.SNACK__111.value),
    (base_id + 400 + 2432): (b'G008', Snacks.SNACK__112.value),
    (base_id + 400 + 2433): (b'G008', Snacks.SNACK__113.value),
    (base_id + 400 + 2434): (b'G008', Snacks.SNACK__114.value),
    (base_id + 400 + 2435): (b'G008', Snacks.SNACK__18.value),
    (base_id + 400 + 2436): (b'G008', Snacks.SNACK__180.value),
    (base_id + 400 + 2437): (b'G008', Snacks.SNACK__181.value),
    (base_id + 400 + 2438): (b'G008', Snacks.SNACK__182.value),
    (base_id + 400 + 2439): (b'G008', Snacks.SNACK__183.value),
    (base_id + 400 + 2440): (b'G008', Snacks.SNACK__184.value),
    (base_id + 400 + 2441): (b'G008', Snacks.SNACK__185.value),
    (base_id + 400 + 2442): (b'G008', Snacks.SNACK__186.value),
    (base_id + 400 + 2443): (b'G008', Snacks.SNACK__187.value),
    (base_id + 400 + 2444): (b'G008', Snacks.SNACK__188.value),
    (base_id + 400 + 2445): (b'G008', Snacks.SNACK__189.value),
    (base_id + 400 + 2446): (b'G008', Snacks.SNACK001.value),
    (base_id + 400 + 2447): (b'G008', Snacks.SNACKBOX__0.value),
    (base_id + 400 + 2448): (b'G008', Snacks.SNACKBOX__1__1.value),
    (base_id + 400 + 2449): (b'G008', Snacks.SNACKBOX__1__10.value),
    (base_id + 400 + 2450): (b'G008', Snacks.SNACKBOX__1__11.value),
    (base_id + 400 + 2451): (b'G008', Snacks.SNACKBOX__1__12.value),
    (base_id + 400 + 2452): (b'G008', Snacks.SNACKBOX__2__1.value),
    (base_id + 400 + 2453): (b'G008', Snacks.SNACKBOX__2__10.value),
    (base_id + 400 + 2454): (b'G008', Snacks.SNACKBOX__2__11.value),
    (base_id + 400 + 2455): (b'G008', Snacks.SNACKBOX__2__12.value),
    (base_id + 400 + 2456): (b'G008', Snacks.SNACKBOX__3__1.value),
    (base_id + 400 + 2457): (b'G008', Snacks.SNACKBOX__3__10.value),
    (base_id + 400 + 2458): (b'G008', Snacks.SNACKBOX__3__11.value),
    (base_id + 400 + 2459): (b'G008', Snacks.SNACKBOX__3__12.value),
    (base_id + 400 + 2460): (b'G008', Snacks.SNACKBOX__4__1.value),
    (base_id + 400 + 2461): (b'G008', Snacks.SNACKBOX__4__10.value),
    (base_id + 400 + 2462): (b'G008', Snacks.SNACKBOX__4__11.value),
    (base_id + 400 + 2463): (b'G008', Snacks.SNACKBOX__4__12.value),
    (base_id + 400 + 2464): (b'G008', Snacks.SS10.value),
    (base_id + 400 + 2465): (b'G008', Snacks.SS11.value),
    (base_id + 400 + 2466): (b'G008', Snacks.SS12.value),
    (base_id + 400 + 2467): (b'G008', Snacks.SS13.value),
    (base_id + 400 + 2468): (b'G008', Snacks.SS14.value),

    (base_id + 400 + 2469): (b'G009', Snacks.SNACK__01.value),
    (base_id + 400 + 2470): (b'G009', Snacks.SNACK__010.value),
    (base_id + 400 + 2471): (b'G009', Snacks.SNACK__011.value),
    (base_id + 400 + 2472): (b'G009', Snacks.SNACK__012.value),
    (base_id + 400 + 2473): (b'G009', Snacks.SNACK__013.value),
    (base_id + 400 + 2474): (b'G009', Snacks.SNACK__014.value),
    (base_id + 400 + 2475): (b'G009', Snacks.SNACK__015.value),
    (base_id + 400 + 2476): (b'G009', Snacks.SNACK__03.value),
    (base_id + 400 + 2477): (b'G009', Snacks.SNACK__030.value),
    (base_id + 400 + 2478): (b'G009', Snacks.SNACK__031.value),
    (base_id + 400 + 2479): (b'G009', Snacks.SNACK__032.value),
    (base_id + 400 + 2480): (b'G009', Snacks.SNACK__033.value),
    (base_id + 400 + 2481): (b'G009', Snacks.SNACK__034.value),
    (base_id + 400 + 2482): (b'G009', Snacks.SNACK__035.value),
    (base_id + 400 + 2483): (b'G009', Snacks.SNACK__036.value),
    (base_id + 400 + 2484): (b'G009', Snacks.SNACK__037.value),
    (base_id + 400 + 2485): (b'G009', Snacks.SNACK__038.value),
    (base_id + 400 + 2486): (b'G009', Snacks.SNACK__039.value),
    (base_id + 400 + 2487): (b'G009', Snacks.SNACK__04.value),
    (base_id + 400 + 2488): (b'G009', Snacks.SNACK__040.value),
    (base_id + 400 + 2489): (b'G009', Snacks.SNACK__041.value),
    (base_id + 400 + 2490): (b'G009', Snacks.SNACK__042.value),
    (base_id + 400 + 2491): (b'G009', Snacks.SNACK__0420.value),
    (base_id + 400 + 2492): (b'G009', Snacks.SNACK__0421.value),
    (base_id + 400 + 2493): (b'G009', Snacks.SNACK__0422.value),
    (base_id + 400 + 2494): (b'G009', Snacks.SNACK__07.value),
    (base_id + 400 + 2495): (b'G009', Snacks.SNACK__070.value),
    (base_id + 400 + 2496): (b'G009', Snacks.SNACK__071.value),
    (base_id + 400 + 2497): (b'G009', Snacks.SNACK__072.value),
    (base_id + 400 + 2498): (b'G009', Snacks.SNACK__073.value),
    (base_id + 400 + 2499): (b'G009', Snacks.SNACK__074.value),
    (base_id + 400 + 2500): (b'G009', Snacks.SNACK__075.value),
    (base_id + 400 + 2501): (b'G009', Snacks.SNACK__08.value),
    (base_id + 400 + 2502): (b'G009', Snacks.SNACK__080.value),
    (base_id + 400 + 2503): (b'G009', Snacks.SNACK__081.value),
    (base_id + 400 + 2504): (b'G009', Snacks.SNACK__082.value),
    (base_id + 400 + 2505): (b'G009', Snacks.SNACK__083.value),
    (base_id + 400 + 2506): (b'G009', Snacks.SNACK__11.value),
    (base_id + 400 + 2507): (b'G009', Snacks.SNACK__110.value),
    (base_id + 400 + 2508): (b'G009', Snacks.SNACK__111.value),
    (base_id + 400 + 2509): (b'G009', Snacks.SNACK__112.value),
    (base_id + 400 + 2510): (b'G009', Snacks.SNACK__113.value),
    (base_id + 400 + 2511): (b'G009', Snacks.SNACKBOX__1.value),
    (base_id + 400 + 2512): (b'G009', Snacks.SNACKBOX__2.value),
    (base_id + 400 + 2513): (b'G009', Snacks.SNACKBOX__3.value),
    (base_id + 400 + 2514): (b'G009', Snacks.SNACKBOX__4.value),

    (base_id + 400 + 2515): (b'H001', Snacks.SNACK__1.value),
    (base_id + 400 + 2516): (b'H001', Snacks.SNACK__10.value),
    (base_id + 400 + 2517): (b'H001', Snacks.SNACK__11.value),
    (base_id + 400 + 2518): (b'H001', Snacks.SNACK__12.value),
    (base_id + 400 + 2519): (b'H001', Snacks.SNACK__13.value),
    (base_id + 400 + 2520): (b'H001', Snacks.SNACK__2.value),
    (base_id + 400 + 2521): (b'H001', Snacks.SNACK__20.value),
    (base_id + 400 + 2522): (b'H001', Snacks.SNACK__21.value),
    (base_id + 400 + 2523): (b'H001', Snacks.SNACK__22.value),
    (base_id + 400 + 2524): (b'H001', Snacks.SNACK__23.value),
    (base_id + 400 + 2525): (b'H001', Snacks.SNACK__3.value),
    (base_id + 400 + 2526): (b'H001', Snacks.SNACK__30.value),
    (base_id + 400 + 2527): (b'H001', Snacks.SNACK__31.value),
    (base_id + 400 + 2528): (b'H001', Snacks.SNACK__32.value),
    (base_id + 400 + 2529): (b'H001', Snacks.SNACK__33.value),
    (base_id + 400 + 2530): (b'H001', Snacks.SNACK__4.value),
    (base_id + 400 + 2531): (b'H001', Snacks.SNACK__40.value),
    (base_id + 400 + 2532): (b'H001', Snacks.SNACK__41.value),
    (base_id + 400 + 2533): (b'H001', Snacks.SNACK__42.value),
    (base_id + 400 + 2534): (b'H001', Snacks.SNACK__43.value),
    (base_id + 400 + 2535): (b'H001', Snacks.SNACK__5.value),
    (base_id + 400 + 2536): (b'H001', Snacks.SNACK__50.value),
    (base_id + 400 + 2537): (b'H001', Snacks.SNACK__51.value),
    (base_id + 400 + 2538): (b'H001', Snacks.SNACK__52.value),
    (base_id + 400 + 2539): (b'H001', Snacks.SNACK__53.value),
    (base_id + 400 + 2540): (b'H001', Snacks.SNACK__530.value),
    (base_id + 400 + 2541): (b'H001', Snacks.SNACK__531.value),
    (base_id + 400 + 2542): (b'H001', Snacks.SNACK__6.value),
    (base_id + 400 + 2543): (b'H001', Snacks.SNACK__60.value),
    (base_id + 400 + 2544): (b'H001', Snacks.SNACK__61.value),
    (base_id + 400 + 2545): (b'H001', Snacks.SNACK__7.value),
    (base_id + 400 + 2546): (b'H001', Snacks.SNACK__70.value),
    (base_id + 400 + 2547): (b'H001', Snacks.SNACK__71.value),
    (base_id + 400 + 2548): (b'H001', Snacks.SNACK__72.value),
    (base_id + 400 + 2549): (b'H001', Snacks.SNACK__73.value),
    (base_id + 400 + 2550): (b'H001', Snacks.SNACK__74.value),

    (base_id + 400 + 2551): (b'H002', Snacks.SS1.value),
    (base_id + 400 + 2552): (b'H002', Snacks.SS10.value),
    (base_id + 400 + 2553): (b'H002', Snacks.SS11.value),
    (base_id + 400 + 2554): (b'H002', Snacks.SS12.value),
    (base_id + 400 + 2555): (b'H002', Snacks.SS13.value),
    (base_id + 400 + 2556): (b'H002', Snacks.SS14.value),
    (base_id + 400 + 2557): (b'H002', Snacks.SS15.value),
    (base_id + 400 + 2558): (b'H002', Snacks.SS16.value),
    (base_id + 400 + 2559): (b'H002', Snacks.SS160.value),
    (base_id + 400 + 2560): (b'H002', Snacks.SS161.value),
    (base_id + 400 + 2561): (b'H002', Snacks.SS162.value),
    (base_id + 400 + 2562): (b'H002', Snacks.SS163.value),
    (base_id + 400 + 2563): (b'H002', Snacks.SS164.value),
    (base_id + 400 + 2564): (b'H002', Snacks.SS165.value),
    (base_id + 400 + 2565): (b'H002', Snacks.SS2.value),
    (base_id + 400 + 2566): (b'H002', Snacks.SS20.value),
    (base_id + 400 + 2567): (b'H002', Snacks.SS200.value),
    (base_id + 400 + 2568): (b'H002', Snacks.SS2000.value),
    (base_id + 400 + 2569): (b'H002', Snacks.SS20000.value),
    (base_id + 400 + 2570): (b'H002', Snacks.SS200000.value),
    (base_id + 400 + 2571): (b'H002', Snacks.SS2000000.value),
    (base_id + 400 + 2572): (b'H002', Snacks.SS20000000.value),
    (base_id + 400 + 2573): (b'H002', Snacks.SS3.value),
    (base_id + 400 + 2574): (b'H002', Snacks.SS30.value),
    (base_id + 400 + 2575): (b'H002', Snacks.SS31.value),
    (base_id + 400 + 2576): (b'H002', Snacks.SS4.value),
    (base_id + 400 + 2577): (b'H002', Snacks.SS40.value),
    (base_id + 400 + 2578): (b'H002', Snacks.SS41.value),
    (base_id + 400 + 2579): (b'H002', Snacks.SS42.value),
    (base_id + 400 + 2580): (b'H002', Snacks.SS43.value),
    (base_id + 400 + 2581): (b'H002', Snacks.SS44.value),
    (base_id + 400 + 2582): (b'H002', Snacks.SS45.value),
    (base_id + 400 + 2583): (b'H002', Snacks.SS46.value),
    (base_id + 400 + 2584): (b'H002', Snacks.SS47.value),
    (base_id + 400 + 2585): (b'H002', Snacks.SS48.value),
    (base_id + 400 + 2586): (b'H002', Snacks.SS5.value),
    (base_id + 400 + 2587): (b'H002', Snacks.SS50.value),
    (base_id + 400 + 2588): (b'H002', Snacks.SS500.value),
    (base_id + 400 + 2589): (b'H002', Snacks.SS51.value),
    (base_id + 400 + 2590): (b'H002', Snacks.SS6.value),
    (base_id + 400 + 2591): (b'H002', Snacks.SS60.value),
    (base_id + 400 + 2592): (b'H002', Snacks.SS600.value),
    (base_id + 400 + 2593): (b'H002', Snacks.SS6000.value),
    (base_id + 400 + 2594): (b'H002', Snacks.SS601.value),
    (base_id + 400 + 2595): (b'H002', Snacks.SS602.value),
    (base_id + 400 + 2596): (b'H002', Snacks.SS6020.value),
    (base_id + 400 + 2597): (b'H002', Snacks.SS61.value),
    (base_id + 400 + 2598): (b'H002', Snacks.SS610.value),
    (base_id + 400 + 2599): (b'H002', Snacks.SS62.value),
    (base_id + 400 + 2600): (b'H002', Snacks.SS7.value),
    (base_id + 400 + 2601): (b'H002', Snacks.SS70.value),
    (base_id + 400 + 2602): (b'H002', Snacks.SS700.value),
    (base_id + 400 + 2603): (b'H002', Snacks.SS7000.value),
    (base_id + 400 + 2604): (b'H002', Snacks.SS8.value),
    (base_id + 400 + 2605): (b'H002', Snacks.SS80.value),
    (base_id + 400 + 2606): (b'H002', Snacks.SS81.value),
    (base_id + 400 + 2607): (b'H002', Snacks.SS82.value),
    (base_id + 400 + 2608): (b'H002', Snacks.SS83.value),
    (base_id + 400 + 2609): (b'H002', Snacks.SS84.value),
    (base_id + 400 + 2610): (b'H002', Snacks.SS85.value),
    (base_id + 400 + 2611): (b'H002', Snacks.SS86.value),
    (base_id + 400 + 2612): (b'H002', Snacks.SS87.value),
    (base_id + 400 + 2613): (b'H002', Snacks.SS9.value),
    (base_id + 400 + 2614): (b'H002', Snacks.SS90.value),
    (base_id + 400 + 2615): (b'H002', Snacks.SS91.value),
    (base_id + 400 + 2616): (b'H002', Snacks.SS92.value),
    (base_id + 400 + 2617): (b'H002', Snacks.SS93.value),
    (base_id + 400 + 2618): (b'H002', Snacks.SS94.value),
    (base_id + 400 + 2619): (b'H002', Snacks.SS95.value),
    (base_id + 400 + 2620): (b'H002', Snacks.SS96.value),
    (base_id + 400 + 2621): (b'H002', Snacks.SS97.value),
    (base_id + 400 + 2622): (b'H002', Snacks.SS98.value),
    (base_id + 400 + 2623): (b'H002', Snacks.SS99.value),
    (base_id + 400 + 2624): (b'H002', Snacks.SS990.value),
    (base_id + 400 + 2625): (b'H002', Snacks.SS991.value),
    (base_id + 400 + 2626): (b'H002', Snacks.SS992.value),
    (base_id + 400 + 2627): (b'H002', Snacks.SS993.value),
    (base_id + 400 + 2628): (b'H002', Snacks.SS994.value),
    (base_id + 400 + 2629): (b'H002', Snacks.SS995.value),
    (base_id + 400 + 2630): (b'H002', Snacks.SS996.value),
    (base_id + 400 + 2631): (b'H002', Snacks.SS997.value),
    (base_id + 400 + 2632): (b'H002', Snacks.SS998.value),

    (base_id + 400 + 2633): (b'I001', Snacks.SN1.value),
    (base_id + 400 + 2634): (b'I001', Snacks.SN11.value),
    (base_id + 400 + 2635): (b'I001', Snacks.SN12.value),
    (base_id + 400 + 2636): (b'I001', Snacks.SN14.value),
    (base_id + 400 + 2637): (b'I001', Snacks.SN19.value),
    (base_id + 400 + 2638): (b'I001', Snacks.SN20.value),
    (base_id + 400 + 2639): (b'I001', Snacks.SN21.value),
    (base_id + 400 + 2640): (b'I001', Snacks.SN22.value),
    (base_id + 400 + 2641): (b'I001', Snacks.SN23.value),
    (base_id + 400 + 2642): (b'I001', Snacks.SN24.value),
    (base_id + 400 + 2643): (b'I001', Snacks.SN25.value),
    (base_id + 400 + 2644): (b'I001', Snacks.SN26.value),
    (base_id + 400 + 2645): (b'I001', Snacks.SN27.value),
    (base_id + 400 + 2646): (b'I001', Snacks.SN29.value),
    (base_id + 400 + 2647): (b'I001', Snacks.SN3.value),
    (base_id + 400 + 2648): (b'I001', Snacks.SN30.value),
    (base_id + 400 + 2649): (b'I001', Snacks.SN33.value),
    (base_id + 400 + 2650): (b'I001', Snacks.SN34.value),
    (base_id + 400 + 2651): (b'I001', Snacks.SN35.value),
    (base_id + 400 + 2652): (b'I001', Snacks.SN36.value),
    (base_id + 400 + 2653): (b'I001', Snacks.SN4.value),
    (base_id + 400 + 2654): (b'I001', Snacks.SN43.value),
    (base_id + 400 + 2655): (b'I001', Snacks.SN44.value),
    (base_id + 400 + 2656): (b'I001', Snacks.SN45.value),
    (base_id + 400 + 2657): (b'I001', Snacks.SN46.value),
    (base_id + 400 + 2658): (b'I001', Snacks.SN47.value),
    (base_id + 400 + 2659): (b'I001', Snacks.SN48.value),
    (base_id + 400 + 2660): (b'I001', Snacks.SN6.value),
    (base_id + 400 + 2661): (b'I001', Snacks.SN7.value),
    (base_id + 400 + 2662): (b'I001', Snacks.SN8.value),
    (base_id + 400 + 2663): (b'I001', Snacks.SNACKBOX.value),
    (base_id + 400 + 2664): (b'I001', Snacks.SNACKBOX__CHAND__2.value),
    (base_id + 400 + 2665): (b'I001', Snacks.SNACKBOX__SECRET__AREA.value),
    (base_id + 400 + 2666): (b'I001', Snacks.SNACKBOX2.value),
    (base_id + 400 + 2667): (b'I001', Snacks.SNACKBOX3.value),

    (base_id + 400 + 2668): (b'I003', Snacks.EX__CLUE__SNACKBOX1.value),
    (base_id + 400 + 2669): (b'I003', Snacks.EX__CLUE__SNACKBOX4.value),
    (base_id + 400 + 2670): (b'I003', Snacks.EX__CLUE__SNACKBOX5.value),
    (base_id + 400 + 2671): (b'I003', Snacks.SN1.value),
    (base_id + 400 + 2672): (b'I003', Snacks.SN13.value),
    (base_id + 400 + 2673): (b'I003', Snacks.SN14.value),
    (base_id + 400 + 2674): (b'I003', Snacks.SN15.value),
    (base_id + 400 + 2675): (b'I003', Snacks.SN16.value),
    (base_id + 400 + 2676): (b'I003', Snacks.SN17.value),
    (base_id + 400 + 2677): (b'I003', Snacks.SN18.value),
    (base_id + 400 + 2678): (b'I003', Snacks.SN19.value),
    (base_id + 400 + 2679): (b'I003', Snacks.SN2.value),
    (base_id + 400 + 2680): (b'I003', Snacks.SN20.value),
    (base_id + 400 + 2681): (b'I003', Snacks.SN21.value),
    (base_id + 400 + 2682): (b'I003', Snacks.SN22.value),
    (base_id + 400 + 2683): (b'I003', Snacks.SN23.value),
    (base_id + 400 + 2684): (b'I003', Snacks.SN24.value),
    (base_id + 400 + 2685): (b'I003', Snacks.SN25.value),
    (base_id + 400 + 2686): (b'I003', Snacks.SN26.value),
    (base_id + 400 + 2687): (b'I003', Snacks.SN27.value),
    (base_id + 400 + 2688): (b'I003', Snacks.SN28.value),
    (base_id + 400 + 2689): (b'I003', Snacks.SN29.value),
    (base_id + 400 + 2690): (b'I003', Snacks.SN30.value),
    (base_id + 400 + 2691): (b'I003', Snacks.SN31.value),
    (base_id + 400 + 2692): (b'I003', Snacks.SN32.value),
    (base_id + 400 + 2693): (b'I003', Snacks.SN33.value),
    (base_id + 400 + 2694): (b'I003', Snacks.SN34.value),
    (base_id + 400 + 2695): (b'I003', Snacks.SN45.value),
    (base_id + 400 + 2696): (b'I003', Snacks.SN46.value),
    (base_id + 400 + 2697): (b'I003', Snacks.SN47.value),
    (base_id + 400 + 2698): (b'I003', Snacks.SN48.value),
    (base_id + 400 + 2699): (b'I003', Snacks.SN52.value),
    (base_id + 400 + 2700): (b'I003', Snacks.SN53.value),
    (base_id + 400 + 2701): (b'I003', Snacks.SN54.value),
    (base_id + 400 + 2702): (b'I003', Snacks.SN92.value),
    (base_id + 400 + 2703): (b'I003', Snacks.SN93.value),
    (base_id + 400 + 2704): (b'I003', Snacks.SN94.value),
    (base_id + 400 + 2705): (b'I003', Snacks.SN95.value),
    (base_id + 400 + 2706): (b'I003', Snacks.SNACK__BOX__10.value),

    (base_id + 400 + 2707): (b'I004', Snacks.EX__CLUE__SNACK__BOX__1.value),
    (base_id + 400 + 2708): (b'I004', Snacks.EX__CLUE__SNACK__BOX__2.value),
    (base_id + 400 + 2709): (b'I004', Snacks.EX__CLUE__SNACK__BOX__3.value),
    (base_id + 400 + 2710): (b'I004', Snacks.EX__CLUE__SNACK__BOX__4.value),
    (base_id + 400 + 2711): (b'I004', Snacks.NEW__SNACKBOX.value),
    (base_id + 400 + 2712): (b'I004', Snacks.NEW__SNACKBOX__2.value),
    (base_id + 400 + 2713): (b'I004', Snacks.SN15.value),
    (base_id + 400 + 2714): (b'I004', Snacks.SN16.value),
    (base_id + 400 + 2715): (b'I004', Snacks.SN17.value),
    (base_id + 400 + 2716): (b'I004', Snacks.SN18.value),
    (base_id + 400 + 2717): (b'I004', Snacks.SN2.value),
    (base_id + 400 + 2718): (b'I004', Snacks.SN22.value),
    (base_id + 400 + 2719): (b'I004', Snacks.SN24.value),
    (base_id + 400 + 2720): (b'I004', Snacks.SN25.value),
    (base_id + 400 + 2721): (b'I004', Snacks.SN26.value),
    (base_id + 400 + 2722): (b'I004', Snacks.SN27.value),
    (base_id + 400 + 2723): (b'I004', Snacks.SN3.value),
    (base_id + 400 + 2724): (b'I004', Snacks.SN37.value),
    (base_id + 400 + 2725): (b'I004', Snacks.SN38.value),
    (base_id + 400 + 2726): (b'I004', Snacks.SN4.value),
    (base_id + 400 + 2727): (b'I004', Snacks.SN45.value),
    (base_id + 400 + 2728): (b'I004', Snacks.SN46.value),
    (base_id + 400 + 2729): (b'I004', Snacks.SN48.value),
    (base_id + 400 + 2730): (b'I004', Snacks.SN5.value),
    (base_id + 400 + 2731): (b'I004', Snacks.SN6.value),
    (base_id + 400 + 2732): (b'I004', Snacks.SN7.value),
    (base_id + 400 + 2733): (b'I004', Snacks.SN9.value),

    (base_id + 400 + 2734): (b'I005', Snacks.BOX__OVER__WITCH.value),
    (base_id + 400 + 2735): (b'I005', Snacks.SN13.value),
    (base_id + 400 + 2736): (b'I005', Snacks.SN17.value),
    (base_id + 400 + 2737): (b'I005', Snacks.SN18.value),
    (base_id + 400 + 2738): (b'I005', Snacks.SN25.value),
    (base_id + 400 + 2739): (b'I005', Snacks.SN26.value),
    (base_id + 400 + 2740): (b'I005', Snacks.SN27.value),
    (base_id + 400 + 2741): (b'I005', Snacks.SN30.value),
    (base_id + 400 + 2742): (b'I005', Snacks.SN4.value),
    (base_id + 400 + 2743): (b'I005', Snacks.SN45.value),
    (base_id + 400 + 2744): (b'I005', Snacks.SN46.value),
    (base_id + 400 + 2745): (b'I005', Snacks.SN47.value),
    (base_id + 400 + 2746): (b'I005', Snacks.SN48.value),
    (base_id + 400 + 2747): (b'I005', Snacks.SN480.value),
    (base_id + 400 + 2748): (b'I005', Snacks.SN5.value),
    (base_id + 400 + 2749): (b'I005', Snacks.SN50.value),
    (base_id + 400 + 2750): (b'I005', Snacks.SN51.value),
    (base_id + 400 + 2751): (b'I005', Snacks.SN53.value),
    (base_id + 400 + 2752): (b'I005', Snacks.SN54.value),
    (base_id + 400 + 2753): (b'I005', Snacks.SN55.value),
    (base_id + 400 + 2754): (b'I005', Snacks.SN6.value),
    (base_id + 400 + 2755): (b'I005', Snacks.SN60.value),
    (base_id + 400 + 2756): (b'I005', Snacks.SN63.value),
    (base_id + 400 + 2757): (b'I005', Snacks.SN64.value),
    (base_id + 400 + 2758): (b'I005', Snacks.SN68.value),
    (base_id + 400 + 2759): (b'I005', Snacks.SN680.value),
    (base_id + 400 + 2760): (b'I005', Snacks.SN6800.value),
    (base_id + 400 + 2761): (b'I005', Snacks.SN75.value),
    (base_id + 400 + 2762): (b'I005', Snacks.SN76.value),
    (base_id + 400 + 2763): (b'I005', Snacks.SN77.value),
    (base_id + 400 + 2764): (b'I005', Snacks.SN8.value),
    (base_id + 400 + 2765): (b'I005', Snacks.SN80.value),
    (base_id + 400 + 2766): (b'I005', Snacks.SN81.value),
    (base_id + 400 + 2767): (b'I005', Snacks.SN82.value),
    (base_id + 400 + 2768): (b'I005', Snacks.SN83.value),
    (base_id + 400 + 2769): (b'I005', Snacks.SN84.value),
    (base_id + 400 + 2770): (b'I005', Snacks.SN85.value),
    (base_id + 400 + 2771): (b'I005', Snacks.SN86.value),
    (base_id + 400 + 2772): (b'I005', Snacks.SN87.value),
    (base_id + 400 + 2773): (b'I005', Snacks.SN89.value),
    (base_id + 400 + 2774): (b'I005', Snacks.SN9.value),
    (base_id + 400 + 2775): (b'I005', Snacks.SN90.value),
    (base_id + 400 + 2776): (b'I005', Snacks.SN91.value),
    (base_id + 400 + 2777): (b'I005', Snacks.SN92.value),
    (base_id + 400 + 2778): (b'I005', Snacks.CRATE_SANDWICH.value),

    (base_id + 400 + 2779): (b'I006', Snacks.SN1.value),
    (base_id + 400 + 2780): (b'I006', Snacks.SN10.value),
    (base_id + 400 + 2781): (b'I006', Snacks.SN100.value),
    (base_id + 400 + 2782): (b'I006', Snacks.SN11.value),
    (base_id + 400 + 2783): (b'I006', Snacks.SN12.value),
    (base_id + 400 + 2784): (b'I006', Snacks.SN13.value),
    (base_id + 400 + 2785): (b'I006', Snacks.SN14.value),
    (base_id + 400 + 2786): (b'I006', Snacks.SN15.value),
    (base_id + 400 + 2787): (b'I006', Snacks.SN16.value),
    (base_id + 400 + 2788): (b'I006', Snacks.SN17.value),
    (base_id + 400 + 2789): (b'I006', Snacks.SN18.value),
    (base_id + 400 + 2790): (b'I006', Snacks.SN19.value),
    (base_id + 400 + 2791): (b'I006', Snacks.SN2.value),
    (base_id + 400 + 2792): (b'I006', Snacks.SN20.value),
    (base_id + 400 + 2793): (b'I006', Snacks.SN21.value),
    (base_id + 400 + 2794): (b'I006', Snacks.SN22.value),
    (base_id + 400 + 2795): (b'I006', Snacks.SN23.value),
    (base_id + 400 + 2796): (b'I006', Snacks.SN24.value),
    (base_id + 400 + 2797): (b'I006', Snacks.SN25.value),
    (base_id + 400 + 2798): (b'I006', Snacks.SN26.value),
    (base_id + 400 + 2799): (b'I006', Snacks.SN27.value),
    (base_id + 400 + 2800): (b'I006', Snacks.SN28.value),
    (base_id + 400 + 2801): (b'I006', Snacks.SN29.value),
    (base_id + 400 + 2802): (b'I006', Snacks.SN3.value),
    (base_id + 400 + 2803): (b'I006', Snacks.SN30.value),
    (base_id + 400 + 2804): (b'I006', Snacks.SN31.value),
    (base_id + 400 + 2805): (b'I006', Snacks.SN32.value),
    (base_id + 400 + 2806): (b'I006', Snacks.SN33.value),
    (base_id + 400 + 2807): (b'I006', Snacks.SN34.value),
    (base_id + 400 + 2808): (b'I006', Snacks.SN35.value),
    (base_id + 400 + 2809): (b'I006', Snacks.SN36.value),
    (base_id + 400 + 2810): (b'I006', Snacks.SN37.value),
    (base_id + 400 + 2811): (b'I006', Snacks.SN38.value),
    (base_id + 400 + 2812): (b'I006', Snacks.SN39.value),
    (base_id + 400 + 2813): (b'I006', Snacks.SN4.value),
    (base_id + 400 + 2814): (b'I006', Snacks.SN40.value),
    (base_id + 400 + 2815): (b'I006', Snacks.SN41.value),
    (base_id + 400 + 2816): (b'I006', Snacks.SN42.value),
    (base_id + 400 + 2817): (b'I006', Snacks.SN43.value),
    (base_id + 400 + 2818): (b'I006', Snacks.SN44.value),
    (base_id + 400 + 2819): (b'I006', Snacks.SN45.value),
    (base_id + 400 + 2820): (b'I006', Snacks.SN46.value),
    (base_id + 400 + 2821): (b'I006', Snacks.SN47.value),
    (base_id + 400 + 2822): (b'I006', Snacks.SN48.value),
    (base_id + 400 + 2823): (b'I006', Snacks.SN49.value),
    (base_id + 400 + 2824): (b'I006', Snacks.SN5.value),
    (base_id + 400 + 2825): (b'I006', Snacks.SN50.value),
    (base_id + 400 + 2826): (b'I006', Snacks.SN51.value),
    (base_id + 400 + 2827): (b'I006', Snacks.SN52.value),
    (base_id + 400 + 2828): (b'I006', Snacks.SN53.value),
    (base_id + 400 + 2829): (b'I006', Snacks.SN54.value),
    (base_id + 400 + 2830): (b'I006', Snacks.SN55.value),
    (base_id + 400 + 2831): (b'I006', Snacks.SN56.value),
    (base_id + 400 + 2832): (b'I006', Snacks.SN57.value),
    (base_id + 400 + 2833): (b'I006', Snacks.SN58.value),
    (base_id + 400 + 2834): (b'I006', Snacks.SN59.value),
    (base_id + 400 + 2835): (b'I006', Snacks.SN6.value),
    (base_id + 400 + 2836): (b'I006', Snacks.SN60.value),
    (base_id + 400 + 2837): (b'I006', Snacks.SN61.value),
    (base_id + 400 + 2838): (b'I006', Snacks.SN62.value),
    (base_id + 400 + 2839): (b'I006', Snacks.SN63.value),
    (base_id + 400 + 2840): (b'I006', Snacks.SN64.value),
    (base_id + 400 + 2841): (b'I006', Snacks.SN7.value),
    (base_id + 400 + 2842): (b'I006', Snacks.SN73.value),
    (base_id + 400 + 2843): (b'I006', Snacks.SN74.value),
    (base_id + 400 + 2844): (b'I006', Snacks.SN75.value),
    (base_id + 400 + 2845): (b'I006', Snacks.SN76.value),
    (base_id + 400 + 2846): (b'I006', Snacks.SN77.value),
    (base_id + 400 + 2847): (b'I006', Snacks.SN78.value),
    (base_id + 400 + 2848): (b'I006', Snacks.SN79.value),
    (base_id + 400 + 2849): (b'I006', Snacks.SN8.value),
    (base_id + 400 + 2850): (b'I006', Snacks.SN80.value),
    (base_id + 400 + 2851): (b'I006', Snacks.SN81.value),
    (base_id + 400 + 2852): (b'I006', Snacks.SN82.value),
    (base_id + 400 + 2853): (b'I006', Snacks.SN83.value),
    (base_id + 400 + 2854): (b'I006', Snacks.SN84.value),
    (base_id + 400 + 2855): (b'I006', Snacks.SN85.value),
    (base_id + 400 + 2856): (b'I006', Snacks.SN86.value),
    (base_id + 400 + 2857): (b'I006', Snacks.SN87.value),
    (base_id + 400 + 2858): (b'I006', Snacks.SN88.value),
    (base_id + 400 + 2859): (b'I006', Snacks.SN89.value),
    (base_id + 400 + 2860): (b'I006', Snacks.SN9.value),
    (base_id + 400 + 2861): (b'I006', Snacks.SN90.value),
    (base_id + 400 + 2862): (b'I006', Snacks.SN91.value),
    (base_id + 400 + 2863): (b'I006', Snacks.SN92.value),
    (base_id + 400 + 2864): (b'I006', Snacks.SN93.value),
    (base_id + 400 + 2865): (b'I006', Snacks.SN94.value),
    (base_id + 400 + 2866): (b'I006', Snacks.SN95.value),
    (base_id + 400 + 2867): (b'I006', Snacks.SN96.value),
    (base_id + 400 + 2868): (b'I006', Snacks.SN97.value),
    (base_id + 400 + 2869): (b'I006', Snacks.SN98.value),
    (base_id + 400 + 2870): (b'I006', Snacks.SN99.value),
    (base_id + 400 + 2871): (b'I006', Snacks.SNACKBOX.value),
    (base_id + 400 + 2872): (b'I006', Snacks.SNACKBOX__2.value),
    (base_id + 400 + 2873): (b'I006', Snacks.SNACKBOX__3.value),

    (base_id + 400 + 2874): (b'I020', Snacks.SN1.value),
    (base_id + 400 + 2875): (b'I020', Snacks.SN10.value),
    (base_id + 400 + 2876): (b'I020', Snacks.SN11.value),
    (base_id + 400 + 2877): (b'I020', Snacks.SN12.value),
    (base_id + 400 + 2878): (b'I020', Snacks.SN13.value),
    (base_id + 400 + 2879): (b'I020', Snacks.SN14.value),
    (base_id + 400 + 2880): (b'I020', Snacks.SN15.value),
    (base_id + 400 + 2881): (b'I020', Snacks.SN16.value),
    (base_id + 400 + 2882): (b'I020', Snacks.SN17.value),
    (base_id + 400 + 2883): (b'I020', Snacks.SN18.value),
    (base_id + 400 + 2884): (b'I020', Snacks.SN19.value),
    (base_id + 400 + 2885): (b'I020', Snacks.SN20.value),
    (base_id + 400 + 2886): (b'I020', Snacks.SN21.value),
    (base_id + 400 + 2887): (b'I020', Snacks.SN22.value),
    (base_id + 400 + 2888): (b'I020', Snacks.SN23.value),
    (base_id + 400 + 2889): (b'I020', Snacks.SN24.value),
    (base_id + 400 + 2890): (b'I020', Snacks.SN25.value),
    (base_id + 400 + 2891): (b'I020', Snacks.SN26.value),
    (base_id + 400 + 2892): (b'I020', Snacks.SN32.value),
    (base_id + 400 + 2893): (b'I020', Snacks.SN33.value),
    (base_id + 400 + 2894): (b'I020', Snacks.SN34.value),
    (base_id + 400 + 2895): (b'I020', Snacks.SN35.value),
    (base_id + 400 + 2896): (b'I020', Snacks.SN36.value),
    (base_id + 400 + 2897): (b'I020', Snacks.SN37.value),
    (base_id + 400 + 2898): (b'I020', Snacks.SN40.value),
    (base_id + 400 + 2899): (b'I020', Snacks.SN41.value),
    (base_id + 400 + 2900): (b'I020', Snacks.SN42.value),
    (base_id + 400 + 2901): (b'I020', Snacks.SN48.value),
    (base_id + 400 + 2902): (b'I020', Snacks.SN49.value),
    (base_id + 400 + 2903): (b'I020', Snacks.SNACK__BOX__OVER__PIT.value),
    (base_id + 400 + 2904): (b'I020', Snacks.SNACK__BOX__OVER__PIT__2.value),
    (base_id + 400 + 2905): (b'I020', Snacks.SNACKBOX1.value),
    (base_id + 400 + 2906): (b'I020', Snacks.SNACKBOX2.value),
    (base_id + 400 + 2907): (b'I020', Snacks.SNACKBOX3.value),
    (base_id + 400 + 2908): (b'I020', Snacks.SS1.value),

    (base_id + 400 + 2909): (b'I021', Snacks.SCARE__SNACK__BOX.value),
    (base_id + 400 + 2910): (b'I021', Snacks.SN1.value),
    (base_id + 400 + 2911): (b'I021', Snacks.SN16.value),
    (base_id + 400 + 2912): (b'I021', Snacks.SN17.value),
    (base_id + 400 + 2913): (b'I021', Snacks.SN18.value),
    (base_id + 400 + 2914): (b'I021', Snacks.SN19.value),
    (base_id + 400 + 2915): (b'I021', Snacks.SN2.value),
    (base_id + 400 + 2916): (b'I021', Snacks.SN24.value),
    (base_id + 400 + 2917): (b'I021', Snacks.SN25.value),
    (base_id + 400 + 2918): (b'I021', Snacks.SN27.value),
    (base_id + 400 + 2919): (b'I021', Snacks.SN28.value),
    (base_id + 400 + 2920): (b'I021', Snacks.SN29.value),
    (base_id + 400 + 2921): (b'I021', Snacks.SN3.value),
    (base_id + 400 + 2922): (b'I021', Snacks.SN36.value),
    (base_id + 400 + 2923): (b'I021', Snacks.SN37.value),
    (base_id + 400 + 2924): (b'I021', Snacks.SN38.value),
    (base_id + 400 + 2925): (b'I021', Snacks.SN39.value),
    (base_id + 400 + 2926): (b'I021', Snacks.SN4.value),
    (base_id + 400 + 2927): (b'I021', Snacks.SN47.value),
    (base_id + 400 + 2928): (b'I021', Snacks.SN48.value),
    (base_id + 400 + 2929): (b'I021', Snacks.SN49.value),
    (base_id + 400 + 2930): (b'I021', Snacks.SN5.value),
    (base_id + 400 + 2931): (b'I021', Snacks.SN50.value),
    (base_id + 400 + 2932): (b'I021', Snacks.SN6.value),
    (base_id + 400 + 2933): (b'I021', Snacks.SN7.value),
    (base_id + 400 + 2934): (b'I021', Snacks.SN8.value),
    (base_id + 400 + 2935): (b'I021', Snacks.SNACK__BOX__IN__SECRET.value),
    (base_id + 400 + 2936): (b'I021', Snacks.SNACKBOX__FOR__TOKEN2.value),
    (base_id + 400 + 2937): (b'I021', Snacks.SNACKBOX__FOR__TOKEN3.value),
    (base_id + 400 + 2938): (b'I021', Snacks.SNACKBOX__FOR__TOKEN4.value),
    (base_id + 400 + 2939): (b'I021', Snacks.SNACKBOX__FOR__TOKEN5.value),

    (base_id + 400 + 2940): (b'L011', Snacks.BOX10__SNACKBOX.value),
    (base_id + 400 + 2941): (b'L011', Snacks.BOX11__SNACKBOX.value),
    (base_id + 400 + 2942): (b'L011', Snacks.BOX13__SNACKBOX.value),
    (base_id + 400 + 2943): (b'L011', Snacks.BOX2__SNACKBOX.value),
    (base_id + 400 + 2944): (b'L011', Snacks.BOX3__SNACKBOX.value),
    (base_id + 400 + 2945): (b'L011', Snacks.BOX5__SNACKBOX.value),
    (base_id + 400 + 2946): (b'L011', Snacks.BOX6__SNACKBOX.value),
    (base_id + 400 + 2947): (b'L011', Snacks.BOX8__SNACKBOX.value),
    (base_id + 400 + 2948): (b'L011', Snacks.CLIFF_SSBOX01.value),
    (base_id + 400 + 2949): (b'L011', Snacks.CLIFF_SSBOX02.value),
    (base_id + 400 + 2950): (b'L011', Snacks.CLIFF_SSBOX03.value),
    (base_id + 400 + 2951): (b'L011', Snacks.CLIFF_SSBOX04.value),
    (base_id + 400 + 2952): (b'L011', Snacks.CLIFF_SSBOX05.value),
    (base_id + 400 + 2953): (b'L011', Snacks.CLIFF_SSBOX06.value),
    (base_id + 400 + 2954): (b'L011', Snacks.LASTFLOAT_SS02.value),
    (base_id + 400 + 2955): (b'L011', Snacks.LASTFLOAT_SS03.value),
    (base_id + 400 + 2956): (b'L011', Snacks.LASTFLOAT_SS04.value),
    (base_id + 400 + 2957): (b'L011', Snacks.SLOPE_SS01.value),
    (base_id + 400 + 2958): (b'L011', Snacks.SLOPE_SS02.value),
    (base_id + 400 + 2959): (b'L011', Snacks.SLOPE_SS03.value),
    (base_id + 400 + 2960): (b'L011', Snacks.SLOPE_SS05.value),
    (base_id + 400 + 2961): (b'L011', Snacks.SLOPE_SS06.value),
    (base_id + 400 + 2962): (b'L011', Snacks.SLOPE_SS07.value),
    (base_id + 400 + 2963): (b'L011', Snacks.SLOPE_SS09.value),
    (base_id + 400 + 2964): (b'L011', Snacks.SLOPE_SS10.value),
    (base_id + 400 + 2965): (b'L011', Snacks.SLOPE_SSBOX04.value),
    (base_id + 400 + 2966): (b'L011', Snacks.SLOPE_SSBOX08.value),
    (base_id + 400 + 2967): (b'L011', Snacks.SNACK__090.value),
    (base_id + 400 + 2968): (b'L011', Snacks.SNACK__11.value),
    (base_id + 400 + 2969): (b'L011', Snacks.SNACK__15.value),
    (base_id + 400 + 2970): (b'L011', Snacks.SNACK__150.value),
    (base_id + 400 + 2971): (b'L011', Snacks.SNACK__151.value),
    (base_id + 400 + 2972): (b'L011', Snacks.SNACK__16.value),
    (base_id + 400 + 2973): (b'L011', Snacks.SNACK__18.value),
    (base_id + 400 + 2974): (b'L011', Snacks.SNACK__19.value),
    (base_id + 400 + 2975): (b'L011', Snacks.SNACK39.value),
    (base_id + 400 + 2976): (b'L011', Snacks.SNACK43.value),
    (base_id + 400 + 2977): (b'L011', Snacks.SNACK51.value),
    (base_id + 400 + 2978): (b'L011', Snacks.SNACK52.value),
    (base_id + 400 + 2979): (b'L011', Snacks.SNACK53.value),
    (base_id + 400 + 2980): (b'L011', Snacks.SNACK54.value),
    (base_id + 400 + 2981): (b'L011', Snacks.SNACK55.value),
    (base_id + 400 + 2982): (b'L011', Snacks.SNACK57.value),
    (base_id + 400 + 2983): (b'L011', Snacks.SNACK58.value),
    (base_id + 400 + 2984): (b'L011', Snacks.SNACK59.value),
    (base_id + 400 + 2985): (b'L011', Snacks.SNACK60.value),
    (base_id + 400 + 2986): (b'L011', Snacks.SNACK61.value),
    (base_id + 400 + 2987): (b'L011', Snacks.SNACK62.value),
    (base_id + 400 + 2988): (b'L011', Snacks.SNACK63.value),
    (base_id + 400 + 2989): (b'L011', Snacks.SNACK64.value),
    (base_id + 400 + 2990): (b'L011', Snacks.SNACK65.value),
    (base_id + 400 + 2991): (b'L011', Snacks.SNACK66.value),
    (base_id + 400 + 2992): (b'L011', Snacks.SNACK67.value),
    (base_id + 400 + 2993): (b'L011', Snacks.SNACK68.value),
    (base_id + 400 + 2994): (b'L011', Snacks.SNACK69.value),
    (base_id + 400 + 2995): (b'L011', Snacks.SNACK70.value),
    (base_id + 400 + 2996): (b'L011', Snacks.SNACK71.value),
    (base_id + 400 + 2997): (b'L011', Snacks.SNACK72.value),
    (base_id + 400 + 2998): (b'L011', Snacks.SNACK73.value),
    (base_id + 400 + 2999): (b'L011', Snacks.SS01.value),
    (base_id + 400 + 3000): (b'L011', Snacks.SS010.value),
    (base_id + 400 + 3001): (b'L011', Snacks.SS011.value),
    (base_id + 400 + 3002): (b'L011', Snacks.SS0110.value),
    (base_id + 400 + 3003): (b'L011', Snacks.SS0111.value),
    (base_id + 400 + 3004): (b'L011', Snacks.SS012.value),
    (base_id + 400 + 3005): (b'L011', Snacks.SS013.value),
    (base_id + 400 + 3006): (b'L011', Snacks.SS014.value),
    (base_id + 400 + 3007): (b'L011', Snacks.SS015.value),
    (base_id + 400 + 3008): (b'L011', Snacks.SS016.value),
    (base_id + 400 + 3009): (b'L011', Snacks.SS017.value),
    (base_id + 400 + 3010): (b'L011', Snacks.SS018.value),
    (base_id + 400 + 3011): (b'L011', Snacks.SS019.value),
    (base_id + 400 + 3012): (b'L011', Snacks.SS02.value),
    (base_id + 400 + 3013): (b'L011', Snacks.SS03.value),
    (base_id + 400 + 3014): (b'L011', Snacks.SS04.value),
    (base_id + 400 + 3015): (b'L011', Snacks.SSBOX01.value),
    (base_id + 400 + 3016): (b'L011', Snacks.SSBOX02.value),
    (base_id + 400 + 3017): (b'L011', Snacks.SSBOX04.value),
    (base_id + 400 + 3018): (b'L011', Snacks.SSBOX05.value),
    (base_id + 400 + 3019): (b'L011', Snacks.SSBOX06.value),
    (base_id + 400 + 3020): (b'L011', Snacks.UPPER_SS01.value),
    (base_id + 400 + 3021): (b'L011', Snacks.UPPER_SS02.value),
    (base_id + 400 + 3022): (b'L011', Snacks.UPPER_SS03.value),
    (base_id + 400 + 3023): (b'L011', Snacks.UPPER_SS04.value),
    (base_id + 400 + 3024): (b'L011', Snacks.UPPER_SS05.value),
    (base_id + 400 + 3025): (b'L011', Snacks.UPPER_SS06.value),
    (base_id + 400 + 3026): (b'L011', Snacks.UPPER_SS08.value),
    (base_id + 400 + 3027): (b'L011', Snacks.UPPER_SS09.value),
    (base_id + 400 + 3028): (b'L011', Snacks.UPPER_SS10.value),

    (base_id + 400 + 3029): (b'L013', Snacks.SNACK10.value),
    (base_id + 400 + 3030): (b'L013', Snacks.SNACK11.value),
    (base_id + 400 + 3031): (b'L013', Snacks.SNACK110.value),
    (base_id + 400 + 3032): (b'L013', Snacks.SNACK111.value),
    (base_id + 400 + 3033): (b'L013', Snacks.SNACK112.value),
    (base_id + 400 + 3034): (b'L013', Snacks.SNACK113.value),
    (base_id + 400 + 3035): (b'L013', Snacks.SNACK114.value),
    (base_id + 400 + 3036): (b'L013', Snacks.SNACK115.value),
    (base_id + 400 + 3037): (b'L013', Snacks.SNACK116.value),
    (base_id + 400 + 3038): (b'L013', Snacks.SNACK117.value),
    (base_id + 400 + 3039): (b'L013', Snacks.SNACK118.value),
    (base_id + 400 + 3040): (b'L013', Snacks.SNACK119.value),
    (base_id + 400 + 3041): (b'L013', Snacks.SNACK12.value),
    (base_id + 400 + 3042): (b'L013', Snacks.SNACK120.value),
    (base_id + 400 + 3043): (b'L013', Snacks.SNACK121.value),
    (base_id + 400 + 3044): (b'L013', Snacks.SNACK122.value),
    (base_id + 400 + 3045): (b'L013', Snacks.SNACK13.value),
    (base_id + 400 + 3046): (b'L013', Snacks.SNACK14.value),
    (base_id + 400 + 3047): (b'L013', Snacks.SNACK15.value),
    (base_id + 400 + 3048): (b'L013', Snacks.SNACK16.value),
    (base_id + 400 + 3049): (b'L013', Snacks.SNACK17.value),
    (base_id + 400 + 3050): (b'L013', Snacks.SNACK18.value),
    (base_id + 400 + 3051): (b'L013', Snacks.SNACK19.value),
    (base_id + 400 + 3052): (b'L013', Snacks.SS01.value),
    (base_id + 400 + 3053): (b'L013', Snacks.SS010.value),
    (base_id + 400 + 3054): (b'L013', Snacks.SS011.value),
    (base_id + 400 + 3055): (b'L013', Snacks.SS012.value),
    (base_id + 400 + 3056): (b'L013', Snacks.SS013.value),
    (base_id + 400 + 3057): (b'L013', Snacks.SS014.value),
    (base_id + 400 + 3058): (b'L013', Snacks.SS02.value),
    (base_id + 400 + 3059): (b'L013', Snacks.SS020.value),
    (base_id + 400 + 3060): (b'L013', Snacks.SS021.value),
    (base_id + 400 + 3061): (b'L013', Snacks.SS022.value),
    (base_id + 400 + 3062): (b'L013', Snacks.SS023.value),
    (base_id + 400 + 3063): (b'L013', Snacks.SS024.value),
    (base_id + 400 + 3064): (b'L013', Snacks.SS025.value),
    (base_id + 400 + 3065): (b'L013', Snacks.SS026.value),
    (base_id + 400 + 3066): (b'L013', Snacks.SS027.value),
    (base_id + 400 + 3067): (b'L013', Snacks.SS03.value),
    (base_id + 400 + 3068): (b'L013', Snacks.SS04.value),
    (base_id + 400 + 3069): (b'L013', Snacks.SS040.value),
    (base_id + 400 + 3070): (b'L013', Snacks.SS041.value),
    (base_id + 400 + 3071): (b'L013', Snacks.SS05.value),
    (base_id + 400 + 3072): (b'L013', Snacks.SS050.value),
    (base_id + 400 + 3073): (b'L013', Snacks.SS051.value),
    (base_id + 400 + 3074): (b'L013', Snacks.SS052.value),
    (base_id + 400 + 3075): (b'L013', Snacks.SS053.value),
    (base_id + 400 + 3076): (b'L013', Snacks.SS054.value),
    (base_id + 400 + 3077): (b'L013', Snacks.SS3.value),
    (base_id + 400 + 3078): (b'L013', Snacks.SS4.value),
    (base_id + 400 + 3079): (b'L013', Snacks.SS5.value),
    (base_id + 400 + 3080): (b'L013', Snacks.SS6.value),
    (base_id + 400 + 3081): (b'L013', Snacks.SS7.value),
    (base_id + 400 + 3082): (b'L013', Snacks.SSBOX01.value),
    (base_id + 400 + 3083): (b'L013', Snacks.SSBOX02.value),
    (base_id + 400 + 3084): (b'L013', Snacks.SSBOX03.value),
    (base_id + 400 + 3085): (b'L013', Snacks.SSBOX04.value),
    (base_id + 400 + 3086): (b'L013', Snacks.SSBOX05.value),
    (base_id + 400 + 3087): (b'L013', Snacks.SSBOX06.value),
    (base_id + 400 + 3088): (b'L013', Snacks.SSBOX07.value),
    (base_id + 400 + 3089): (b'L013', Snacks.SSBOX08.value),
    (base_id + 400 + 3090): (b'L013', Snacks.SSBOX09.value),
    (base_id + 400 + 3091): (b'L013', Snacks.SSBOX10.value),
    (base_id + 400 + 3092): (b'L013', Snacks.SSBOX11.value),

    (base_id + 400 + 3093): (b'L014', Snacks.SS10.value),
    (base_id + 400 + 3094): (b'L014', Snacks.SS11.value),
    (base_id + 400 + 3095): (b'L014', Snacks.SS110.value),
    (base_id + 400 + 3096): (b'L014', Snacks.SS111.value),
    (base_id + 400 + 3097): (b'L014', Snacks.SS112.value),
    (base_id + 400 + 3098): (b'L014', Snacks.SS113.value),
    (base_id + 400 + 3099): (b'L014', Snacks.SS114.value),
    (base_id + 400 + 3100): (b'L014', Snacks.SS115.value),
    (base_id + 400 + 3101): (b'L014', Snacks.SS12.value),
    (base_id + 400 + 3102): (b'L014', Snacks.SS120.value),
    (base_id + 400 + 3103): (b'L014', Snacks.SS121.value),
    (base_id + 400 + 3104): (b'L014', Snacks.SS122.value),
    (base_id + 400 + 3105): (b'L014', Snacks.SS123.value),
    (base_id + 400 + 3106): (b'L014', Snacks.SS124.value),
    (base_id + 400 + 3107): (b'L014', Snacks.SS125.value),
    (base_id + 400 + 3108): (b'L014', Snacks.SS13.value),
    (base_id + 400 + 3109): (b'L014', Snacks.SS130.value),
    (base_id + 400 + 3110): (b'L014', Snacks.SS131.value),
    (base_id + 400 + 3111): (b'L014', Snacks.SS132.value),
    (base_id + 400 + 3112): (b'L014', Snacks.SS133.value),
    (base_id + 400 + 3113): (b'L014', Snacks.SS134.value),
    (base_id + 400 + 3114): (b'L014', Snacks.SS135.value),
    (base_id + 400 + 3115): (b'L014', Snacks.SS14.value),
    (base_id + 400 + 3116): (b'L014', Snacks.SS15.value),
    (base_id + 400 + 3117): (b'L014', Snacks.SS16.value),
    (base_id + 400 + 3118): (b'L014', Snacks.SS17.value),
    (base_id + 400 + 3119): (b'L014', Snacks.SS18.value),
    (base_id + 400 + 3120): (b'L014', Snacks.SS2.value),
    (base_id + 400 + 3121): (b'L014', Snacks.SS200.value),
    (base_id + 400 + 3122): (b'L014', Snacks.SS201.value),
    (base_id + 400 + 3123): (b'L014', Snacks.SS2010.value),
    (base_id + 400 + 3124): (b'L014', Snacks.SS2011.value),
    (base_id + 400 + 3125): (b'L014', Snacks.SS202.value),
    (base_id + 400 + 3126): (b'L014', Snacks.SS203.value),
    (base_id + 400 + 3127): (b'L014', Snacks.SS204.value),
    (base_id + 400 + 3128): (b'L014', Snacks.SS205.value),
    (base_id + 400 + 3129): (b'L014', Snacks.SS206.value),
    (base_id + 400 + 3130): (b'L014', Snacks.SS207.value),
    (base_id + 400 + 3131): (b'L014', Snacks.SS208.value),
    (base_id + 400 + 3132): (b'L014', Snacks.SS209.value),
    (base_id + 400 + 3133): (b'L014', Snacks.SS210.value),
    (base_id + 400 + 3134): (b'L014', Snacks.SS211.value),
    (base_id + 400 + 3135): (b'L014', Snacks.SS212.value),
    (base_id + 400 + 3136): (b'L014', Snacks.SS213.value),
    (base_id + 400 + 3137): (b'L014', Snacks.SS214.value),
    (base_id + 400 + 3138): (b'L014', Snacks.SS215.value),
    (base_id + 400 + 3139): (b'L014', Snacks.SS216.value),
    (base_id + 400 + 3140): (b'L014', Snacks.SS3.value),
    (base_id + 400 + 3141): (b'L014', Snacks.SS30.value),
    (base_id + 400 + 3142): (b'L014', Snacks.SS300.value),
    (base_id + 400 + 3143): (b'L014', Snacks.SS301.value),
    (base_id + 400 + 3144): (b'L014', Snacks.SS302.value),
    (base_id + 400 + 3145): (b'L014', Snacks.SS303.value),
    (base_id + 400 + 3146): (b'L014', Snacks.SS304.value),
    (base_id + 400 + 3147): (b'L014', Snacks.SS305.value),
    (base_id + 400 + 3148): (b'L014', Snacks.SS4.value),
    (base_id + 400 + 3149): (b'L014', Snacks.SS5.value),
    (base_id + 400 + 3150): (b'L014', Snacks.SS6.value),
    (base_id + 400 + 3151): (b'L014', Snacks.SS7.value),
    (base_id + 400 + 3152): (b'L014', Snacks.SS8.value),
    (base_id + 400 + 3153): (b'L014', Snacks.SS9.value),
    (base_id + 400 + 3154): (b'L014', Snacks.SSBOX01.value),
    (base_id + 400 + 3155): (b'L014', Snacks.SSBOX02.value),
    (base_id + 400 + 3156): (b'L014', Snacks.SSBOX04.value),
    (base_id + 400 + 3157): (b'L014', Snacks.SSBOX06.value),
    (base_id + 400 + 3158): (b'L014', Snacks.SSBOX07.value),
    (base_id + 400 + 3159): (b'L014', Snacks.SSBOX08.value),
    (base_id + 400 + 3160): (b'L014', Snacks.SSBOX09.value),

    (base_id + 400 + 3161): (b'L015', Snacks.SNACK1.value),
    (base_id + 400 + 3162): (b'L015', Snacks.SNACK10.value),
    (base_id + 400 + 3163): (b'L015', Snacks.SNACK11.value),
    (base_id + 400 + 3164): (b'L015', Snacks.SNACK110.value),
    (base_id + 400 + 3165): (b'L015', Snacks.SNACK111.value),
    (base_id + 400 + 3166): (b'L015', Snacks.SNACK112.value),
    (base_id + 400 + 3167): (b'L015', Snacks.SNACK113.value),
    (base_id + 400 + 3168): (b'L015', Snacks.SNACK114.value),
    (base_id + 400 + 3169): (b'L015', Snacks.SNACK115.value),
    (base_id + 400 + 3170): (b'L015', Snacks.SNACK116.value),
    (base_id + 400 + 3171): (b'L015', Snacks.SNACK117.value),
    (base_id + 400 + 3172): (b'L015', Snacks.SNACK118.value),
    (base_id + 400 + 3173): (b'L015', Snacks.SNACK119.value),
    (base_id + 400 + 3174): (b'L015', Snacks.SNACK12.value),
    (base_id + 400 + 3175): (b'L015', Snacks.SNACK13.value),
    (base_id + 400 + 3176): (b'L015', Snacks.SNACK14.value),
    (base_id + 400 + 3177): (b'L015', Snacks.SNACK15.value),
    (base_id + 400 + 3178): (b'L015', Snacks.SNACK16.value),
    (base_id + 400 + 3179): (b'L015', Snacks.SNACK17.value),
    (base_id + 400 + 3180): (b'L015', Snacks.SNACK18.value),
    (base_id + 400 + 3181): (b'L015', Snacks.SNACK19.value),
    (base_id + 400 + 3182): (b'L015', Snacks.SS03.value),
    (base_id + 400 + 3183): (b'L015', Snacks.SS030.value),
    (base_id + 400 + 3184): (b'L015', Snacks.SS031.value),
    (base_id + 400 + 3185): (b'L015', Snacks.SS032.value),
    (base_id + 400 + 3186): (b'L015', Snacks.SS033.value),
    (base_id + 400 + 3187): (b'L015', Snacks.SS034.value),
    (base_id + 400 + 3188): (b'L015', Snacks.SS11.value),
    (base_id + 400 + 3189): (b'L015', Snacks.SS12.value),
    (base_id + 400 + 3190): (b'L015', Snacks.SS13.value),
    (base_id + 400 + 3191): (b'L015', Snacks.SS15.value),
    (base_id + 400 + 3192): (b'L015', Snacks.SS16.value),
    (base_id + 400 + 3193): (b'L015', Snacks.SS17.value),
    (base_id + 400 + 3194): (b'L015', Snacks.SS18.value),
    (base_id + 400 + 3195): (b'L015', Snacks.SS19.value),
    (base_id + 400 + 3196): (b'L015', Snacks.SS20.value),
    (base_id + 400 + 3197): (b'L015', Snacks.SS21.value),
    (base_id + 400 + 3198): (b'L015', Snacks.SS22.value),
    (base_id + 400 + 3199): (b'L015', Snacks.SS23.value),
    (base_id + 400 + 3200): (b'L015', Snacks.SS24.value),
    (base_id + 400 + 3201): (b'L015', Snacks.SS25.value),
    (base_id + 400 + 3202): (b'L015', Snacks.SS26.value),
    (base_id + 400 + 3203): (b'L015', Snacks.SS27.value),
    (base_id + 400 + 3204): (b'L015', Snacks.SS270.value),
    (base_id + 400 + 3205): (b'L015', Snacks.SS271.value),
    (base_id + 400 + 3206): (b'L015', Snacks.SS2711.value),
    (base_id + 400 + 3207): (b'L015', Snacks.SS28.value),
    (base_id + 400 + 3208): (b'L015', Snacks.SS29.value),
    (base_id + 400 + 3209): (b'L015', Snacks.SS300.value),
    (base_id + 400 + 3210): (b'L015', Snacks.SS301.value),
    (base_id + 400 + 3211): (b'L015', Snacks.SS3010.value),
    (base_id + 400 + 3212): (b'L015', Snacks.SS3011.value),
    (base_id + 400 + 3213): (b'L015', Snacks.SS3012.value),
    (base_id + 400 + 3214): (b'L015', Snacks.SS3013.value),
    (base_id + 400 + 3215): (b'L015', Snacks.SS3014.value),
    (base_id + 400 + 3216): (b'L015', Snacks.SS302.value),
    (base_id + 400 + 3217): (b'L015', Snacks.SS303.value),
    (base_id + 400 + 3218): (b'L015', Snacks.SS3030.value),
    (base_id + 400 + 3219): (b'L015', Snacks.SS3031.value),
    (base_id + 400 + 3220): (b'L015', Snacks.SS3032.value),
    (base_id + 400 + 3221): (b'L015', Snacks.SS3033.value),
    (base_id + 400 + 3222): (b'L015', Snacks.SS3034.value),
    (base_id + 400 + 3223): (b'L015', Snacks.SS4.value),
    (base_id + 400 + 3224): (b'L015', Snacks.SS40.value),
    (base_id + 400 + 3225): (b'L015', Snacks.SS400.value),
    (base_id + 400 + 3226): (b'L015', Snacks.SS401.value),
    (base_id + 400 + 3227): (b'L015', Snacks.SS4010.value),
    (base_id + 400 + 3228): (b'L015', Snacks.SS4011.value),
    (base_id + 400 + 3229): (b'L015', Snacks.SS4012.value),
    (base_id + 400 + 3230): (b'L015', Snacks.SS4014.value),
    (base_id + 400 + 3231): (b'L015', Snacks.SS4015.value),
    (base_id + 400 + 3232): (b'L015', Snacks.SS4016.value),
    (base_id + 400 + 3233): (b'L015', Snacks.SS41.value),
    (base_id + 400 + 3234): (b'L015', Snacks.SS42.value),
    (base_id + 400 + 3235): (b'L015', Snacks.SS43.value),
    (base_id + 400 + 3236): (b'L015', Snacks.SS430.value),
    (base_id + 400 + 3237): (b'L015', Snacks.SS431.value),
    (base_id + 400 + 3238): (b'L015', Snacks.SS4310.value),
    (base_id + 400 + 3239): (b'L015', Snacks.SS4311.value),
    (base_id + 400 + 3240): (b'L015', Snacks.SS43110.value),
    (base_id + 400 + 3241): (b'L015', Snacks.SS43111.value),
    (base_id + 400 + 3242): (b'L015', Snacks.SS431110.value),
    (base_id + 400 + 3243): (b'L015', Snacks.SS500.value),
    (base_id + 400 + 3244): (b'L015', Snacks.SS501.value),
    (base_id + 400 + 3245): (b'L015', Snacks.SS502.value),
    (base_id + 400 + 3246): (b'L015', Snacks.SS503.value),
    (base_id + 400 + 3247): (b'L015', Snacks.SS60.value),
    (base_id + 400 + 3248): (b'L015', Snacks.SS600.value),
    (base_id + 400 + 3249): (b'L015', Snacks.SS601.value),
    (base_id + 400 + 3250): (b'L015', Snacks.SS602.value),
    (base_id + 400 + 3251): (b'L015', Snacks.SS6020.value),
    (base_id + 400 + 3252): (b'L015', Snacks.SS60200.value),
    (base_id + 400 + 3253): (b'L015', Snacks.SS6021.value),
    (base_id + 400 + 3254): (b'L015', Snacks.SS6022.value),
    (base_id + 400 + 3255): (b'L015', Snacks.SS7.value),
    (base_id + 400 + 3256): (b'L015', Snacks.SS9.value),
    (base_id + 400 + 3257): (b'L015', Snacks.SSBOX01.value),
    (base_id + 400 + 3258): (b'L015', Snacks.SSBOX02.value),
    (base_id + 400 + 3259): (b'L015', Snacks.SSBOX03.value),
    (base_id + 400 + 3260): (b'L015', Snacks.SSBOX04.value),
    (base_id + 400 + 3261): (b'L015', Snacks.SSBOX05.value),

    (base_id + 400 + 3262): (b'L017', Snacks.CRATE02__SNACKBOX.value),
    (base_id + 400 + 3263): (b'L017', Snacks.CRATE03__SNACKBOX.value),
    (base_id + 400 + 3264): (b'L017', Snacks.CRATE04__SNACKBOX.value),
    (base_id + 400 + 3265): (b'L017', Snacks.CRATE06__SNACKBOX.value),
    (base_id + 400 + 3266): (b'L017', Snacks.CRATE07__SNACKBOX.value),
    (base_id + 400 + 3267): (b'L017', Snacks.CRATE08__SNACKBOX.value),
    (base_id + 400 + 3268): (b'L017', Snacks.SS100.value),
    (base_id + 400 + 3269): (b'L017', Snacks.SS1000.value),
    (base_id + 400 + 3270): (b'L017', Snacks.SS1001.value),
    (base_id + 400 + 3271): (b'L017', Snacks.SS1002.value),
    (base_id + 400 + 3272): (b'L017', Snacks.SS10020.value),
    (base_id + 400 + 3273): (b'L017', Snacks.SS10021.value),
    (base_id + 400 + 3274): (b'L017', Snacks.SS10022.value),
    (base_id + 400 + 3275): (b'L017', Snacks.SS1003.value),
    (base_id + 400 + 3276): (b'L017', Snacks.SS1004.value),
    (base_id + 400 + 3277): (b'L017', Snacks.SS10040.value),
    (base_id + 400 + 3278): (b'L017', Snacks.SS1005.value),
    (base_id + 400 + 3279): (b'L017', Snacks.SS10050.value),
    (base_id + 400 + 3280): (b'L017', Snacks.SS10051.value),
    (base_id + 400 + 3281): (b'L017', Snacks.SS1006.value),
    (base_id + 400 + 3282): (b'L017', Snacks.SS10060.value),
    (base_id + 400 + 3283): (b'L017', Snacks.SS10061.value),
    (base_id + 400 + 3284): (b'L017', Snacks.SS1007.value),
    (base_id + 400 + 3285): (b'L017', Snacks.SS10070.value),
    (base_id + 400 + 3286): (b'L017', Snacks.SS10071.value),
    (base_id + 400 + 3287): (b'L017', Snacks.SS1008.value),
    (base_id + 400 + 3288): (b'L017', Snacks.SS10080.value),
    (base_id + 400 + 3289): (b'L017', Snacks.SS10081.value),
    (base_id + 400 + 3290): (b'L017', Snacks.SS10082.value),
    (base_id + 400 + 3291): (b'L017', Snacks.SS10083.value),
    (base_id + 400 + 3292): (b'L017', Snacks.SS1009.value),
    (base_id + 400 + 3293): (b'L017', Snacks.SS10090.value),
    (base_id + 400 + 3294): (b'L017', Snacks.SS10091.value),
    (base_id + 400 + 3295): (b'L017', Snacks.SS10092.value),
    (base_id + 400 + 3296): (b'L017', Snacks.SS10093.value),
    (base_id + 400 + 3297): (b'L017', Snacks.SS101.value),
    (base_id + 400 + 3298): (b'L017', Snacks.SS1010.value),
    (base_id + 400 + 3299): (b'L017', Snacks.SS1011.value),
    (base_id + 400 + 3300): (b'L017', Snacks.SS1012.value),
    (base_id + 400 + 3301): (b'L017', Snacks.SS102.value),
    (base_id + 400 + 3302): (b'L017', Snacks.SS1020.value),
    (base_id + 400 + 3303): (b'L017', Snacks.SS1021.value),
    (base_id + 400 + 3304): (b'L017', Snacks.SS1022.value),
    (base_id + 400 + 3305): (b'L017', Snacks.SS1023.value),
    (base_id + 400 + 3306): (b'L017', Snacks.SS10230.value),
    (base_id + 400 + 3307): (b'L017', Snacks.SS10231.value),
    (base_id + 400 + 3308): (b'L017', Snacks.SS103.value),
    (base_id + 400 + 3309): (b'L017', Snacks.SS1030.value),
    (base_id + 400 + 3310): (b'L017', Snacks.SS1031.value),
    (base_id + 400 + 3311): (b'L017', Snacks.SS104.value),
    (base_id + 400 + 3312): (b'L017', Snacks.SS1040.value),
    (base_id + 400 + 3313): (b'L017', Snacks.SS1041.value),
    (base_id + 400 + 3314): (b'L017', Snacks.SS1042.value),
    (base_id + 400 + 3315): (b'L017', Snacks.SS1043.value),
    (base_id + 400 + 3316): (b'L017', Snacks.SS105.value),
    (base_id + 400 + 3317): (b'L017', Snacks.SS1050.value),
    (base_id + 400 + 3318): (b'L017', Snacks.SS1051.value),
    (base_id + 400 + 3319): (b'L017', Snacks.SS1052.value),
    (base_id + 400 + 3320): (b'L017', Snacks.SS1053.value),
    (base_id + 400 + 3321): (b'L017', Snacks.SS106.value),
    (base_id + 400 + 3322): (b'L017', Snacks.SS1060.value),
    (base_id + 400 + 3323): (b'L017', Snacks.SS1061.value),
    (base_id + 400 + 3324): (b'L017', Snacks.SS1062.value),
    (base_id + 400 + 3325): (b'L017', Snacks.SS107.value),
    (base_id + 400 + 3326): (b'L017', Snacks.SS1070.value),
    (base_id + 400 + 3327): (b'L017', Snacks.SS1071.value),
    (base_id + 400 + 3328): (b'L017', Snacks.SS1072.value),
    (base_id + 400 + 3329): (b'L017', Snacks.SS108.value),
    (base_id + 400 + 3330): (b'L017', Snacks.SS1080.value),
    (base_id + 400 + 3331): (b'L017', Snacks.SS1081.value),
    (base_id + 400 + 3332): (b'L017', Snacks.SS1082.value),
    (base_id + 400 + 3333): (b'L017', Snacks.SS109.value),
    (base_id + 400 + 3334): (b'L017', Snacks.SS1090.value),
    (base_id + 400 + 3335): (b'L017', Snacks.SS1091.value),
    (base_id + 400 + 3336): (b'L017', Snacks.SS1092.value),
    (base_id + 400 + 3337): (b'L017', Snacks.SS110.value),
    (base_id + 400 + 3338): (b'L017', Snacks.SS1100.value),
    (base_id + 400 + 3339): (b'L017', Snacks.SS1101.value),
    (base_id + 400 + 3340): (b'L017', Snacks.SS1102.value),
    (base_id + 400 + 3341): (b'L017', Snacks.SS11020.value),
    (base_id + 400 + 3342): (b'L017', Snacks.SS11021.value),
    (base_id + 400 + 3343): (b'L017', Snacks.SS11022.value),
    (base_id + 400 + 3344): (b'L017', Snacks.SS111.value),
    (base_id + 400 + 3345): (b'L017', Snacks.SS1110.value),
    (base_id + 400 + 3346): (b'L017', Snacks.SS1111.value),
    (base_id + 400 + 3347): (b'L017', Snacks.SS1112.value),
    (base_id + 400 + 3348): (b'L017', Snacks.SS1113.value),
    (base_id + 400 + 3349): (b'L017', Snacks.SS11131.value),
    (base_id + 400 + 3350): (b'L017', Snacks.SS11132.value),
    (base_id + 400 + 3351): (b'L017', Snacks.SS11133.value),
    (base_id + 400 + 3352): (b'L017', Snacks.SS111330.value),
    (base_id + 400 + 3353): (b'L017', Snacks.SS111331.value),
    (base_id + 400 + 3354): (b'L017', Snacks.SS111332.value),
    (base_id + 400 + 3355): (b'L017', Snacks.SS111333.value),
    (base_id + 400 + 3356): (b'L017', Snacks.SS1113330.value),
    (base_id + 400 + 3357): (b'L017', Snacks.SS1113331.value),
    (base_id + 400 + 3358): (b'L017', Snacks.SS1113332.value),
    (base_id + 400 + 3359): (b'L017', Snacks.SS112.value),
    (base_id + 400 + 3360): (b'L017', Snacks.SSBOX01.value),
    (base_id + 400 + 3361): (b'L017', Snacks.SSBOX02.value),

    (base_id + 400 + 3362): (b'L018', Snacks.SS10.value),
    (base_id + 400 + 3363): (b'L018', Snacks.SS11.value),
    (base_id + 400 + 3364): (b'L018', Snacks.SS12.value),
    (base_id + 400 + 3365): (b'L018', Snacks.SS120.value),
    (base_id + 400 + 3366): (b'L018', Snacks.SS121.value),
    (base_id + 400 + 3367): (b'L018', Snacks.SS122.value),
    (base_id + 400 + 3368): (b'L018', Snacks.SS123.value),
    (base_id + 400 + 3369): (b'L018', Snacks.SS124.value),
    (base_id + 400 + 3370): (b'L018', Snacks.SS1240.value),
    (base_id + 400 + 3371): (b'L018', Snacks.SS1241.value),
    (base_id + 400 + 3372): (b'L018', Snacks.SS12410.value),
    (base_id + 400 + 3373): (b'L018', Snacks.SS124100.value),
    (base_id + 400 + 3374): (b'L018', Snacks.SS124101.value),
    (base_id + 400 + 3375): (b'L018', Snacks.SS14.value),
    (base_id + 400 + 3376): (b'L018', Snacks.SS15.value),
    (base_id + 400 + 3377): (b'L018', Snacks.SS16.value),
    (base_id + 400 + 3378): (b'L018', Snacks.SS20.value),
    (base_id + 400 + 3379): (b'L018', Snacks.SS21.value),
    (base_id + 400 + 3380): (b'L018', Snacks.SS22.value),
    (base_id + 400 + 3381): (b'L018', Snacks.SS23.value),
    (base_id + 400 + 3382): (b'L018', Snacks.SS24.value),
    (base_id + 400 + 3383): (b'L018', Snacks.SS25.value),
    (base_id + 400 + 3384): (b'L018', Snacks.SS26.value),
    (base_id + 400 + 3385): (b'L018', Snacks.SS27.value),
    (base_id + 400 + 3386): (b'L018', Snacks.SS28.value),
    (base_id + 400 + 3387): (b'L018', Snacks.SS30.value),
    (base_id + 400 + 3388): (b'L018', Snacks.SS31.value),
    (base_id + 400 + 3389): (b'L018', Snacks.SS32.value),
    (base_id + 400 + 3390): (b'L018', Snacks.SS33.value),
    (base_id + 400 + 3391): (b'L018', Snacks.SS34.value),
    (base_id + 400 + 3392): (b'L018', Snacks.SS36.value),
    (base_id + 400 + 3393): (b'L018', Snacks.SS360.value),
    (base_id + 400 + 3394): (b'L018', Snacks.SS361.value),
    (base_id + 400 + 3395): (b'L018', Snacks.SS362.value),
    (base_id + 400 + 3396): (b'L018', Snacks.SS363.value),
    (base_id + 400 + 3397): (b'L018', Snacks.SS364.value),
    (base_id + 400 + 3398): (b'L018', Snacks.SS365.value),
    (base_id + 400 + 3399): (b'L018', Snacks.SS37.value),
    (base_id + 400 + 3400): (b'L018', Snacks.SS370.value),
    (base_id + 400 + 3401): (b'L018', Snacks.SS371.value),
    (base_id + 400 + 3402): (b'L018', Snacks.SS372.value),
    (base_id + 400 + 3403): (b'L018', Snacks.SS373.value),
    (base_id + 400 + 3404): (b'L018', Snacks.SS38.value),
    (base_id + 400 + 3405): (b'L018', Snacks.SS380.value),
    (base_id + 400 + 3406): (b'L018', Snacks.SS381.value),
    (base_id + 400 + 3407): (b'L018', Snacks.SS382.value),
    (base_id + 400 + 3408): (b'L018', Snacks.SS383.value),
    (base_id + 400 + 3409): (b'L018', Snacks.SS384.value),
    (base_id + 400 + 3410): (b'L018', Snacks.SS39.value),
    (base_id + 400 + 3411): (b'L018', Snacks.SS4.value),
    (base_id + 400 + 3412): (b'L018', Snacks.SS5.value),
    (base_id + 400 + 3413): (b'L018', Snacks.SS7.value),
    (base_id + 400 + 3414): (b'L018', Snacks.SS70.value),
    (base_id + 400 + 3415): (b'L018', Snacks.SS71.value),
    (base_id + 400 + 3416): (b'L018', Snacks.SS72.value),
    (base_id + 400 + 3417): (b'L018', Snacks.SS73.value),
    (base_id + 400 + 3418): (b'L018', Snacks.SS8.value),
    (base_id + 400 + 3419): (b'L018', Snacks.SS9.value),
    (base_id + 400 + 3420): (b'L018', Snacks.SSBOX01.value),
    (base_id + 400 + 3421): (b'L018', Snacks.SSBOX02.value),
    (base_id + 400 + 3422): (b'L018', Snacks.SSBOX03.value),
    (base_id + 400 + 3423): (b'L018', Snacks.SSBOX04.value),
    (base_id + 400 + 3424): (b'L018', Snacks.SSBOX05.value),
    (base_id + 400 + 3425): (b'L018', Snacks.SSBOX06.value),

    (base_id + 400 + 3426): (b'L019', Snacks.SS01A.value),
    (base_id + 400 + 3427): (b'L019', Snacks.SS01B.value),
    (base_id + 400 + 3428): (b'L019', Snacks.SS03.value),
    (base_id + 400 + 3429): (b'L019', Snacks.SS05A.value),
    (base_id + 400 + 3430): (b'L019', Snacks.SS05B.value),
    (base_id + 400 + 3431): (b'L019', Snacks.SS06A.value),
    (base_id + 400 + 3432): (b'L019', Snacks.SS06B.value),
    (base_id + 400 + 3433): (b'L019', Snacks.SS07A.value),
    (base_id + 400 + 3434): (b'L019', Snacks.SS07B.value),
    (base_id + 400 + 3435): (b'L019', Snacks.SS08A.value),
    (base_id + 400 + 3436): (b'L019', Snacks.SS08B.value),
    (base_id + 400 + 3437): (b'L019', Snacks.SS09A.value),
    (base_id + 400 + 3438): (b'L019', Snacks.SS09B.value),
    (base_id + 400 + 3439): (b'L019', Snacks.SS10.value),
    (base_id + 400 + 3440): (b'L019', Snacks.SS11.value),
    (base_id + 400 + 3441): (b'L019', Snacks.SS110.value),
    (base_id + 400 + 3442): (b'L019', Snacks.SS11A.value),
    (base_id + 400 + 3443): (b'L019', Snacks.SS12.value),
    (base_id + 400 + 3444): (b'L019', Snacks.SS12A.value),
    (base_id + 400 + 3445): (b'L019', Snacks.SS12B.value),
    (base_id + 400 + 3446): (b'L019', Snacks.SS13.value),
    (base_id + 400 + 3447): (b'L019', Snacks.SS13A.value),
    (base_id + 400 + 3448): (b'L019', Snacks.SS13B.value),
    (base_id + 400 + 3449): (b'L019', Snacks.SS14.value),
    (base_id + 400 + 3450): (b'L019', Snacks.SS14B.value),
    (base_id + 400 + 3451): (b'L019', Snacks.SS15.value),
    (base_id + 400 + 3452): (b'L019', Snacks.SS16.value),
    (base_id + 400 + 3453): (b'L019', Snacks.SS17.value),
    (base_id + 400 + 3454): (b'L019', Snacks.SS18.value),
    (base_id + 400 + 3455): (b'L019', Snacks.SS20.value),
    (base_id + 400 + 3456): (b'L019', Snacks.SS4.value),
    (base_id + 400 + 3457): (b'L019', Snacks.SS40.value),
    (base_id + 400 + 3458): (b'L019', Snacks.SS41.value),
    (base_id + 400 + 3459): (b'L019', Snacks.SS42.value),
    (base_id + 400 + 3460): (b'L019', Snacks.SS5.value),
    (base_id + 400 + 3461): (b'L019', Snacks.SS6.value),
    (base_id + 400 + 3462): (b'L019', Snacks.SS7.value),
    (base_id + 400 + 3463): (b'L019', Snacks.SS8.value),
    (base_id + 400 + 3464): (b'L019', Snacks.SS9.value),
    (base_id + 400 + 3465): (b'L019', Snacks.SSBOX01.value),
    (base_id + 400 + 3466): (b'L019', Snacks.SSBOX02.value),

    (base_id + 400 + 3467): (b'O002', Snacks.SS1.value),
    (base_id + 400 + 3468): (b'O002', Snacks.SS10.value),
    (base_id + 400 + 3469): (b'O002', Snacks.SS11.value),
    (base_id + 400 + 3470): (b'O002', Snacks.SS12.value),
    (base_id + 400 + 3471): (b'O002', Snacks.SS13.value),
    (base_id + 400 + 3472): (b'O002', Snacks.SS14.value),
    (base_id + 400 + 3473): (b'O002', Snacks.SS15.value),
    (base_id + 400 + 3474): (b'O002', Snacks.SS16.value),
    (base_id + 400 + 3475): (b'O002', Snacks.SS17.value),
    (base_id + 400 + 3476): (b'O002', Snacks.SS18.value),
    (base_id + 400 + 3477): (b'O002', Snacks.SS19.value),
    (base_id + 400 + 3478): (b'O002', Snacks.SS2.value),
    (base_id + 400 + 3479): (b'O002', Snacks.SS20.value),
    (base_id + 400 + 3480): (b'O002', Snacks.SS21.value),
    (base_id + 400 + 3481): (b'O002', Snacks.SS22.value),
    (base_id + 400 + 3482): (b'O002', Snacks.SS23.value),
    (base_id + 400 + 3483): (b'O002', Snacks.SS24.value),
    (base_id + 400 + 3484): (b'O002', Snacks.SS25.value),
    (base_id + 400 + 3485): (b'O002', Snacks.SS26.value),
    (base_id + 400 + 3486): (b'O002', Snacks.SS27.value),
    (base_id + 400 + 3487): (b'O002', Snacks.SS28.value),
    (base_id + 400 + 3488): (b'O002', Snacks.SS29.value),
    (base_id + 400 + 3489): (b'O002', Snacks.SS3.value),
    (base_id + 400 + 3490): (b'O002', Snacks.SS30.value),
    (base_id + 400 + 3491): (b'O002', Snacks.SS31.value),
    (base_id + 400 + 3492): (b'O002', Snacks.SS32.value),
    (base_id + 400 + 3493): (b'O002', Snacks.SS34.value),
    (base_id + 400 + 3494): (b'O002', Snacks.SS35.value),
    (base_id + 400 + 3495): (b'O002', Snacks.SS36.value),
    (base_id + 400 + 3496): (b'O002', Snacks.SS39.value),
    (base_id + 400 + 3497): (b'O002', Snacks.SS4.value),
    (base_id + 400 + 3498): (b'O002', Snacks.SS40.value),
    (base_id + 400 + 3499): (b'O002', Snacks.SS41.value),
    (base_id + 400 + 3500): (b'O002', Snacks.SS42.value),
    (base_id + 400 + 3501): (b'O002', Snacks.SS43.value),
    (base_id + 400 + 3502): (b'O002', Snacks.SS44.value),
    (base_id + 400 + 3503): (b'O002', Snacks.SS45.value),
    (base_id + 400 + 3504): (b'O002', Snacks.SS46.value),
    (base_id + 400 + 3505): (b'O002', Snacks.SS47.value),
    (base_id + 400 + 3506): (b'O002', Snacks.SS48.value),
    (base_id + 400 + 3507): (b'O002', Snacks.SS5.value),
    (base_id + 400 + 3508): (b'O002', Snacks.SS50.value),
    (base_id + 400 + 3509): (b'O002', Snacks.SS51.value),
    (base_id + 400 + 3510): (b'O002', Snacks.SS52.value),
    (base_id + 400 + 3511): (b'O002', Snacks.SS53.value),
    (base_id + 400 + 3512): (b'O002', Snacks.SS54.value),
    (base_id + 400 + 3513): (b'O002', Snacks.SS55.value),
    (base_id + 400 + 3514): (b'O002', Snacks.SS56.value),
    (base_id + 400 + 3515): (b'O002', Snacks.SS57.value),
    (base_id + 400 + 3516): (b'O002', Snacks.SS58.value),
    (base_id + 400 + 3517): (b'O002', Snacks.SS59.value),
    (base_id + 400 + 3518): (b'O002', Snacks.SS6.value),
    (base_id + 400 + 3519): (b'O002', Snacks.SS60.value),
    (base_id + 400 + 3520): (b'O002', Snacks.SS61.value),
    (base_id + 400 + 3521): (b'O002', Snacks.SS63.value),
    (base_id + 400 + 3522): (b'O002', Snacks.SS7.value),
    (base_id + 400 + 3523): (b'O002', Snacks.SS8.value),
    (base_id + 400 + 3524): (b'O002', Snacks.SS9.value),
    (base_id + 400 + 3525): (b'O002', Snacks.SSBOX01.value),
    (base_id + 400 + 3526): (b'O002', Snacks.SSBOX02.value),
    (base_id + 400 + 3527): (b'O002', Snacks.SSBOX03.value),

    (base_id + 400 + 3528): (b'O003', Snacks.SN1.value),
    (base_id + 400 + 3529): (b'O003', Snacks.SN10.value),
    (base_id + 400 + 3530): (b'O003', Snacks.SN11.value),
    (base_id + 400 + 3531): (b'O003', Snacks.SN12.value),
    (base_id + 400 + 3532): (b'O003', Snacks.SN13.value),
    (base_id + 400 + 3533): (b'O003', Snacks.SN14.value),
    (base_id + 400 + 3534): (b'O003', Snacks.SN15.value),
    (base_id + 400 + 3535): (b'O003', Snacks.SN16.value),
    (base_id + 400 + 3536): (b'O003', Snacks.SN17.value),
    (base_id + 400 + 3537): (b'O003', Snacks.SN18.value),
    (base_id + 400 + 3538): (b'O003', Snacks.SN19.value),
    (base_id + 400 + 3539): (b'O003', Snacks.SN2.value),
    (base_id + 400 + 3540): (b'O003', Snacks.SN20.value),
    (base_id + 400 + 3541): (b'O003', Snacks.SN21.value),
    (base_id + 400 + 3542): (b'O003', Snacks.SN22.value),
    (base_id + 400 + 3543): (b'O003', Snacks.SN23.value),
    (base_id + 400 + 3544): (b'O003', Snacks.SN24.value),
    (base_id + 400 + 3545): (b'O003', Snacks.SN25.value),
    (base_id + 400 + 3546): (b'O003', Snacks.SN26.value),
    (base_id + 400 + 3547): (b'O003', Snacks.SN27.value),
    (base_id + 400 + 3548): (b'O003', Snacks.SN28.value),
    (base_id + 400 + 3549): (b'O003', Snacks.SN29.value),
    (base_id + 400 + 3550): (b'O003', Snacks.SN3.value),
    (base_id + 400 + 3551): (b'O003', Snacks.SN30.value),
    (base_id + 400 + 3552): (b'O003', Snacks.SN31.value),
    (base_id + 400 + 3553): (b'O003', Snacks.SN32.value),
    (base_id + 400 + 3554): (b'O003', Snacks.SN33.value),
    (base_id + 400 + 3555): (b'O003', Snacks.SN34.value),
    (base_id + 400 + 3556): (b'O003', Snacks.SN35.value),
    (base_id + 400 + 3557): (b'O003', Snacks.SN36.value),
    (base_id + 400 + 3558): (b'O003', Snacks.SN37.value),
    (base_id + 400 + 3559): (b'O003', Snacks.SN38.value),
    (base_id + 400 + 3560): (b'O003', Snacks.SN4.value),
    (base_id + 400 + 3561): (b'O003', Snacks.SN40.value),
    (base_id + 400 + 3562): (b'O003', Snacks.SN42.value),
    (base_id + 400 + 3563): (b'O003', Snacks.SN43.value),
    (base_id + 400 + 3564): (b'O003', Snacks.SN44.value),
    (base_id + 400 + 3565): (b'O003', Snacks.SN45.value),
    (base_id + 400 + 3566): (b'O003', Snacks.SN46.value),
    (base_id + 400 + 3567): (b'O003', Snacks.SN47.value),
    (base_id + 400 + 3568): (b'O003', Snacks.SN48.value),
    (base_id + 400 + 3569): (b'O003', Snacks.SN49.value),
    (base_id + 400 + 3570): (b'O003', Snacks.SN5.value),
    (base_id + 400 + 3571): (b'O003', Snacks.SN50.value),
    (base_id + 400 + 3572): (b'O003', Snacks.SN51.value),
    (base_id + 400 + 3573): (b'O003', Snacks.SN52.value),
    (base_id + 400 + 3574): (b'O003', Snacks.SN53.value),
    (base_id + 400 + 3575): (b'O003', Snacks.SN54.value),
    (base_id + 400 + 3576): (b'O003', Snacks.SN55.value),
    (base_id + 400 + 3577): (b'O003', Snacks.SN57.value),
    (base_id + 400 + 3578): (b'O003', Snacks.SN58.value),
    (base_id + 400 + 3579): (b'O003', Snacks.SN59.value),
    (base_id + 400 + 3580): (b'O003', Snacks.SN6.value),
    (base_id + 400 + 3581): (b'O003', Snacks.SN60.value),
    (base_id + 400 + 3582): (b'O003', Snacks.SN61.value),
    (base_id + 400 + 3583): (b'O003', Snacks.SN62.value),
    (base_id + 400 + 3584): (b'O003', Snacks.SN63.value),
    (base_id + 400 + 3585): (b'O003', Snacks.SN64.value),
    (base_id + 400 + 3586): (b'O003', Snacks.SN65.value),
    (base_id + 400 + 3587): (b'O003', Snacks.SN66.value),
    (base_id + 400 + 3588): (b'O003', Snacks.SN7.value),
    (base_id + 400 + 3589): (b'O003', Snacks.SN74.value),
    (base_id + 400 + 3590): (b'O003', Snacks.SN75.value),
    (base_id + 400 + 3591): (b'O003', Snacks.SN8.value),
    (base_id + 400 + 3592): (b'O003', Snacks.SN9.value),
    (base_id + 400 + 3593): (b'O003', Snacks.SSBOX01.value),
    (base_id + 400 + 3594): (b'O003', Snacks.SSBOX02.value),

    (base_id + 400 + 3595): (b'O004', Snacks.SN1.value),
    (base_id + 400 + 3596): (b'O004', Snacks.SN10.value),
    (base_id + 400 + 3597): (b'O004', Snacks.SN100.value),
    (base_id + 400 + 3598): (b'O004', Snacks.SN11.value),
    (base_id + 400 + 3599): (b'O004', Snacks.SN12.value),
    (base_id + 400 + 3600): (b'O004', Snacks.SN13.value),
    (base_id + 400 + 3601): (b'O004', Snacks.SN14.value),
    (base_id + 400 + 3602): (b'O004', Snacks.SN15.value),
    (base_id + 400 + 3603): (b'O004', Snacks.SN16.value),
    (base_id + 400 + 3604): (b'O004', Snacks.SN17.value),
    (base_id + 400 + 3605): (b'O004', Snacks.SN18.value),
    (base_id + 400 + 3606): (b'O004', Snacks.SN19.value),
    (base_id + 400 + 3607): (b'O004', Snacks.SN2.value),
    (base_id + 400 + 3608): (b'O004', Snacks.SN20.value),
    (base_id + 400 + 3609): (b'O004', Snacks.SN21.value),
    (base_id + 400 + 3610): (b'O004', Snacks.SN22.value),
    (base_id + 400 + 3611): (b'O004', Snacks.SN23.value),
    (base_id + 400 + 3612): (b'O004', Snacks.SN24.value),
    (base_id + 400 + 3613): (b'O004', Snacks.SN25.value),
    (base_id + 400 + 3614): (b'O004', Snacks.SN26.value),
    (base_id + 400 + 3615): (b'O004', Snacks.SN27.value),
    (base_id + 400 + 3616): (b'O004', Snacks.SN28.value),
    (base_id + 400 + 3617): (b'O004', Snacks.SN29.value),
    (base_id + 400 + 3618): (b'O004', Snacks.SN3.value),
    (base_id + 400 + 3619): (b'O004', Snacks.SN30.value),
    (base_id + 400 + 3620): (b'O004', Snacks.SN31.value),
    (base_id + 400 + 3621): (b'O004', Snacks.SN32.value),
    (base_id + 400 + 3622): (b'O004', Snacks.SN33.value),
    (base_id + 400 + 3623): (b'O004', Snacks.SN34.value),
    (base_id + 400 + 3624): (b'O004', Snacks.SN35.value),
    (base_id + 400 + 3625): (b'O004', Snacks.SN36.value),
    (base_id + 400 + 3626): (b'O004', Snacks.SN37.value),
    (base_id + 400 + 3627): (b'O004', Snacks.SN38.value),
    (base_id + 400 + 3628): (b'O004', Snacks.SN39.value),
    (base_id + 400 + 3629): (b'O004', Snacks.SN4.value),
    (base_id + 400 + 3630): (b'O004', Snacks.SN40.value),
    (base_id + 400 + 3631): (b'O004', Snacks.SN41.value),
    (base_id + 400 + 3632): (b'O004', Snacks.SN42.value),
    (base_id + 400 + 3633): (b'O004', Snacks.SN43.value),
    (base_id + 400 + 3634): (b'O004', Snacks.SN44.value),
    (base_id + 400 + 3635): (b'O004', Snacks.SN45.value),
    (base_id + 400 + 3636): (b'O004', Snacks.SN46.value),
    (base_id + 400 + 3637): (b'O004', Snacks.SN47.value),
    (base_id + 400 + 3638): (b'O004', Snacks.SN48.value),
    (base_id + 400 + 3639): (b'O004', Snacks.SN49.value),
    (base_id + 400 + 3640): (b'O004', Snacks.SN5.value),
    (base_id + 400 + 3641): (b'O004', Snacks.SN50.value),
    (base_id + 400 + 3642): (b'O004', Snacks.SN51.value),
    (base_id + 400 + 3643): (b'O004', Snacks.SN52.value),
    (base_id + 400 + 3644): (b'O004', Snacks.SN53.value),
    (base_id + 400 + 3645): (b'O004', Snacks.SN54.value),
    (base_id + 400 + 3646): (b'O004', Snacks.SN55.value),
    (base_id + 400 + 3647): (b'O004', Snacks.SN56.value),
    (base_id + 400 + 3648): (b'O004', Snacks.SN57.value),
    (base_id + 400 + 3649): (b'O004', Snacks.SN58.value),
    (base_id + 400 + 3650): (b'O004', Snacks.SN59.value),
    (base_id + 400 + 3651): (b'O004', Snacks.SN6.value),
    (base_id + 400 + 3652): (b'O004', Snacks.SN60.value),
    (base_id + 400 + 3653): (b'O004', Snacks.SN61.value),
    (base_id + 400 + 3654): (b'O004', Snacks.SN62.value),
    (base_id + 400 + 3655): (b'O004', Snacks.SN63.value),
    (base_id + 400 + 3656): (b'O004', Snacks.SN64.value),
    (base_id + 400 + 3657): (b'O004', Snacks.SN65.value),
    (base_id + 400 + 3658): (b'O004', Snacks.SN66.value),
    (base_id + 400 + 3659): (b'O004', Snacks.SN67.value),
    (base_id + 400 + 3660): (b'O004', Snacks.SN68.value),
    (base_id + 400 + 3661): (b'O004', Snacks.SN69.value),
    (base_id + 400 + 3662): (b'O004', Snacks.SN7.value),
    (base_id + 400 + 3663): (b'O004', Snacks.SN70.value),
    (base_id + 400 + 3664): (b'O004', Snacks.SN71.value),
    (base_id + 400 + 3665): (b'O004', Snacks.SN72.value),
    (base_id + 400 + 3666): (b'O004', Snacks.SN73.value),
    (base_id + 400 + 3667): (b'O004', Snacks.SN74.value),
    (base_id + 400 + 3668): (b'O004', Snacks.SN75.value),
    (base_id + 400 + 3669): (b'O004', Snacks.SN76.value),
    (base_id + 400 + 3670): (b'O004', Snacks.SN77.value),
    (base_id + 400 + 3671): (b'O004', Snacks.SN78.value),
    (base_id + 400 + 3672): (b'O004', Snacks.SN79.value),
    (base_id + 400 + 3673): (b'O004', Snacks.SN8.value),
    (base_id + 400 + 3674): (b'O004', Snacks.SN80.value),
    (base_id + 400 + 3675): (b'O004', Snacks.SN81.value),
    (base_id + 400 + 3676): (b'O004', Snacks.SN82.value),
    (base_id + 400 + 3677): (b'O004', Snacks.SN83.value),
    (base_id + 400 + 3678): (b'O004', Snacks.SN84.value),
    (base_id + 400 + 3679): (b'O004', Snacks.SN85.value),
    (base_id + 400 + 3680): (b'O004', Snacks.SN86.value),
    (base_id + 400 + 3681): (b'O004', Snacks.SN87.value),
    (base_id + 400 + 3682): (b'O004', Snacks.SN88.value),
    (base_id + 400 + 3683): (b'O004', Snacks.SN89.value),
    (base_id + 400 + 3684): (b'O004', Snacks.SN9.value),
    (base_id + 400 + 3685): (b'O004', Snacks.SN90.value),
    (base_id + 400 + 3686): (b'O004', Snacks.SN91.value),
    (base_id + 400 + 3687): (b'O004', Snacks.SN92.value),
    (base_id + 400 + 3688): (b'O004', Snacks.SN93.value),
    (base_id + 400 + 3689): (b'O004', Snacks.SN94.value),
    (base_id + 400 + 3690): (b'O004', Snacks.SN95.value),
    (base_id + 400 + 3691): (b'O004', Snacks.SN96.value),
    (base_id + 400 + 3692): (b'O004', Snacks.SN97.value),
    (base_id + 400 + 3693): (b'O004', Snacks.SN98.value),
    (base_id + 400 + 3694): (b'O004', Snacks.SN99.value),
    (base_id + 400 + 3695): (b'O004', Snacks.SSBOX01.value),
    (base_id + 400 + 3696): (b'O004', Snacks.SSBOX02.value),
    (base_id + 400 + 3697): (b'O004', Snacks.SSBOX03.value),
    (base_id + 400 + 3698): (b'O004', Snacks.SSBOX04.value),
    (base_id + 400 + 3699): (b'O004', Snacks.SSBOX05.value),
    (base_id + 400 + 3700): (b'O004', Snacks.SSBOX06.value),

    (base_id + 400 + 3701): (b'O005', Snacks.SM100.value),
    (base_id + 400 + 3702): (b'O005', Snacks.SM68.value),
    (base_id + 400 + 3703): (b'O005', Snacks.SM69.value),
    (base_id + 400 + 3704): (b'O005', Snacks.SM70.value),
    (base_id + 400 + 3705): (b'O005', Snacks.SM71.value),
    (base_id + 400 + 3706): (b'O005', Snacks.SM72.value),
    (base_id + 400 + 3707): (b'O005', Snacks.SM73.value),
    (base_id + 400 + 3708): (b'O005', Snacks.SM74.value),
    (base_id + 400 + 3709): (b'O005', Snacks.SM75.value),
    (base_id + 400 + 3710): (b'O005', Snacks.SM76.value),
    (base_id + 400 + 3711): (b'O005', Snacks.SM77.value),
    (base_id + 400 + 3712): (b'O005', Snacks.SM78.value),
    (base_id + 400 + 3713): (b'O005', Snacks.SM79.value),
    (base_id + 400 + 3714): (b'O005', Snacks.SM80.value),
    (base_id + 400 + 3715): (b'O005', Snacks.SM81.value),
    (base_id + 400 + 3716): (b'O005', Snacks.SM82.value),
    (base_id + 400 + 3717): (b'O005', Snacks.SM83.value),
    (base_id + 400 + 3718): (b'O005', Snacks.SM84.value),
    (base_id + 400 + 3719): (b'O005', Snacks.SM85.value),
    (base_id + 400 + 3720): (b'O005', Snacks.SM86.value),
    (base_id + 400 + 3721): (b'O005', Snacks.SM87.value),
    (base_id + 400 + 3722): (b'O005', Snacks.SM88.value),
    (base_id + 400 + 3723): (b'O005', Snacks.SM89.value),
    (base_id + 400 + 3724): (b'O005', Snacks.SM90.value),
    (base_id + 400 + 3725): (b'O005', Snacks.SM91.value),
    (base_id + 400 + 3726): (b'O005', Snacks.SM92.value),
    (base_id + 400 + 3727): (b'O005', Snacks.SM93.value),
    (base_id + 400 + 3728): (b'O005', Snacks.SM94.value),
    (base_id + 400 + 3729): (b'O005', Snacks.SM95.value),
    (base_id + 400 + 3730): (b'O005', Snacks.SM96.value),
    (base_id + 400 + 3731): (b'O005', Snacks.SM97.value),
    (base_id + 400 + 3732): (b'O005', Snacks.SM98.value),
    (base_id + 400 + 3733): (b'O005', Snacks.SM99.value),
    (base_id + 400 + 3734): (b'O005', Snacks.SN1.value),
    (base_id + 400 + 3735): (b'O005', Snacks.SN10.value),
    (base_id + 400 + 3736): (b'O005', Snacks.SN11.value),
    (base_id + 400 + 3737): (b'O005', Snacks.SN12.value),
    (base_id + 400 + 3738): (b'O005', Snacks.SN13.value),
    (base_id + 400 + 3739): (b'O005', Snacks.SN14.value),
    (base_id + 400 + 3740): (b'O005', Snacks.SN15.value),
    (base_id + 400 + 3741): (b'O005', Snacks.SN16.value),
    (base_id + 400 + 3742): (b'O005', Snacks.SN17.value),
    (base_id + 400 + 3743): (b'O005', Snacks.SN18.value),
    (base_id + 400 + 3744): (b'O005', Snacks.SN19.value),
    (base_id + 400 + 3745): (b'O005', Snacks.SN2.value),
    (base_id + 400 + 3746): (b'O005', Snacks.SN20.value),
    (base_id + 400 + 3747): (b'O005', Snacks.SN21.value),
    (base_id + 400 + 3748): (b'O005', Snacks.SN22.value),
    (base_id + 400 + 3749): (b'O005', Snacks.SN23.value),
    (base_id + 400 + 3750): (b'O005', Snacks.SN24.value),
    (base_id + 400 + 3751): (b'O005', Snacks.SN25.value),
    (base_id + 400 + 3752): (b'O005', Snacks.SN26.value),
    (base_id + 400 + 3753): (b'O005', Snacks.SN27.value),
    (base_id + 400 + 3754): (b'O005', Snacks.SN28.value),
    (base_id + 400 + 3755): (b'O005', Snacks.SN3.value),
    (base_id + 400 + 3756): (b'O005', Snacks.SN32.value),
    (base_id + 400 + 3757): (b'O005', Snacks.SN33.value),
    (base_id + 400 + 3758): (b'O005', Snacks.SN4.value),
    (base_id + 400 + 3759): (b'O005', Snacks.SN40.value),
    (base_id + 400 + 3760): (b'O005', Snacks.SN41.value),
    (base_id + 400 + 3761): (b'O005', Snacks.SN42.value),
    (base_id + 400 + 3762): (b'O005', Snacks.SN43.value),
    (base_id + 400 + 3763): (b'O005', Snacks.SN44.value),
    (base_id + 400 + 3764): (b'O005', Snacks.SN45.value),
    (base_id + 400 + 3765): (b'O005', Snacks.SN46.value),
    (base_id + 400 + 3766): (b'O005', Snacks.SN47.value),
    (base_id + 400 + 3767): (b'O005', Snacks.SN48.value),
    (base_id + 400 + 3768): (b'O005', Snacks.SN49.value),
    (base_id + 400 + 3769): (b'O005', Snacks.SN5.value),
    (base_id + 400 + 3770): (b'O005', Snacks.SN50.value),
    (base_id + 400 + 3771): (b'O005', Snacks.SN51.value),
    (base_id + 400 + 3772): (b'O005', Snacks.SN52.value),
    (base_id + 400 + 3773): (b'O005', Snacks.SN53.value),
    (base_id + 400 + 3774): (b'O005', Snacks.SN54.value),
    (base_id + 400 + 3775): (b'O005', Snacks.SN55.value),
    (base_id + 400 + 3776): (b'O005', Snacks.SN56.value),
    (base_id + 400 + 3777): (b'O005', Snacks.SN58.value),
    (base_id + 400 + 3778): (b'O005', Snacks.SN59.value),
    (base_id + 400 + 3779): (b'O005', Snacks.SN6.value),
    (base_id + 400 + 3780): (b'O005', Snacks.SN60.value),
    (base_id + 400 + 3781): (b'O005', Snacks.SN61.value),
    (base_id + 400 + 3782): (b'O005', Snacks.SN62.value),
    (base_id + 400 + 3783): (b'O005', Snacks.SN63.value),
    (base_id + 400 + 3784): (b'O005', Snacks.SN64.value),
    (base_id + 400 + 3785): (b'O005', Snacks.SN65.value),
    (base_id + 400 + 3786): (b'O005', Snacks.SN66.value),
    (base_id + 400 + 3787): (b'O005', Snacks.SN67.value),
    (base_id + 400 + 3788): (b'O005', Snacks.SN7.value),
    (base_id + 400 + 3789): (b'O005', Snacks.SN8.value),
    (base_id + 400 + 3790): (b'O005', Snacks.SN9.value),
    (base_id + 400 + 3791): (b'O005', Snacks.SSBOX01.value),
    (base_id + 400 + 3792): (b'O005', Snacks.SSBOX02.value),
    (base_id + 400 + 3793): (b'O005', Snacks.SSBOX03.value),
    (base_id + 400 + 3794): (b'O005', Snacks.SSBOX04.value),
    (base_id + 400 + 3795): (b'O005', Snacks.SSBOX05.value),
    (base_id + 400 + 3796): (b'O005', Snacks.SSBOX06.value),

    (base_id + 400 + 3797): (b'O006', Snacks.S100.value),
    (base_id + 400 + 3798): (b'O006', Snacks.S89.value),
    (base_id + 400 + 3799): (b'O006', Snacks.S90.value),
    (base_id + 400 + 3800): (b'O006', Snacks.S91.value),
    (base_id + 400 + 3801): (b'O006', Snacks.S92.value),
    (base_id + 400 + 3802): (b'O006', Snacks.S93.value),
    (base_id + 400 + 3803): (b'O006', Snacks.S94.value),
    (base_id + 400 + 3804): (b'O006', Snacks.S95.value),
    (base_id + 400 + 3805): (b'O006', Snacks.S96.value),
    (base_id + 400 + 3806): (b'O006', Snacks.S97.value),
    (base_id + 400 + 3807): (b'O006', Snacks.S98.value),
    (base_id + 400 + 3808): (b'O006', Snacks.S99.value),
    (base_id + 400 + 3809): (b'O006', Snacks.SN1.value),
    (base_id + 400 + 3810): (b'O006', Snacks.SN10.value),
    (base_id + 400 + 3811): (b'O006', Snacks.SN11.value),
    (base_id + 400 + 3812): (b'O006', Snacks.SN12.value),
    (base_id + 400 + 3813): (b'O006', Snacks.SN13.value),
    (base_id + 400 + 3814): (b'O006', Snacks.SN14.value),
    (base_id + 400 + 3815): (b'O006', Snacks.SN15.value),
    (base_id + 400 + 3816): (b'O006', Snacks.SN16.value),
    (base_id + 400 + 3817): (b'O006', Snacks.SN17.value),
    (base_id + 400 + 3818): (b'O006', Snacks.SN18.value),
    (base_id + 400 + 3819): (b'O006', Snacks.SN19.value),
    (base_id + 400 + 3820): (b'O006', Snacks.SN2.value),
    (base_id + 400 + 3821): (b'O006', Snacks.SN20.value),
    (base_id + 400 + 3822): (b'O006', Snacks.SN21.value),
    (base_id + 400 + 3823): (b'O006', Snacks.SN22.value),
    (base_id + 400 + 3824): (b'O006', Snacks.SN23.value),
    (base_id + 400 + 3825): (b'O006', Snacks.SN24.value),
    (base_id + 400 + 3826): (b'O006', Snacks.SN25.value),
    (base_id + 400 + 3827): (b'O006', Snacks.SN26.value),
    (base_id + 400 + 3828): (b'O006', Snacks.SN27.value),
    (base_id + 400 + 3829): (b'O006', Snacks.SN28.value),
    (base_id + 400 + 3830): (b'O006', Snacks.SN29.value),
    (base_id + 400 + 3831): (b'O006', Snacks.SN3.value),
    (base_id + 400 + 3832): (b'O006', Snacks.SN30.value),
    (base_id + 400 + 3833): (b'O006', Snacks.SN31.value),
    (base_id + 400 + 3834): (b'O006', Snacks.SN32.value),
    (base_id + 400 + 3835): (b'O006', Snacks.SN33.value),
    (base_id + 400 + 3836): (b'O006', Snacks.SN34.value),
    (base_id + 400 + 3837): (b'O006', Snacks.SN35.value),
    (base_id + 400 + 3838): (b'O006', Snacks.SN38.value),
    (base_id + 400 + 3839): (b'O006', Snacks.SN39.value),
    (base_id + 400 + 3840): (b'O006', Snacks.SN4.value),
    (base_id + 400 + 3841): (b'O006', Snacks.SN42.value),
    (base_id + 400 + 3842): (b'O006', Snacks.SN44.value),
    (base_id + 400 + 3843): (b'O006', Snacks.SN45.value),
    (base_id + 400 + 3844): (b'O006', Snacks.SN46.value),
    (base_id + 400 + 3845): (b'O006', Snacks.SN47.value),
    (base_id + 400 + 3846): (b'O006', Snacks.SN48.value),
    (base_id + 400 + 3847): (b'O006', Snacks.SN49.value),
    (base_id + 400 + 3848): (b'O006', Snacks.SN5.value),
    (base_id + 400 + 3849): (b'O006', Snacks.SN50.value),
    (base_id + 400 + 3850): (b'O006', Snacks.SN51.value),
    (base_id + 400 + 3851): (b'O006', Snacks.SN52.value),
    (base_id + 400 + 3852): (b'O006', Snacks.SN53.value),
    (base_id + 400 + 3853): (b'O006', Snacks.SN54.value),
    (base_id + 400 + 3854): (b'O006', Snacks.SN55.value),
    (base_id + 400 + 3855): (b'O006', Snacks.SN56.value),
    (base_id + 400 + 3856): (b'O006', Snacks.SN57.value),
    (base_id + 400 + 3857): (b'O006', Snacks.SN58.value),
    (base_id + 400 + 3858): (b'O006', Snacks.SN59.value),
    (base_id + 400 + 3859): (b'O006', Snacks.SN6.value),
    (base_id + 400 + 3860): (b'O006', Snacks.SN60.value),
    (base_id + 400 + 3861): (b'O006', Snacks.SN61.value),
    (base_id + 400 + 3862): (b'O006', Snacks.SN62.value),
    (base_id + 400 + 3863): (b'O006', Snacks.SN63.value),
    (base_id + 400 + 3864): (b'O006', Snacks.SN64.value),
    (base_id + 400 + 3865): (b'O006', Snacks.SN65.value),
    (base_id + 400 + 3866): (b'O006', Snacks.SN66.value),
    (base_id + 400 + 3867): (b'O006', Snacks.SN67.value),
    (base_id + 400 + 3868): (b'O006', Snacks.SN68.value),
    (base_id + 400 + 3869): (b'O006', Snacks.SN69.value),
    (base_id + 400 + 3870): (b'O006', Snacks.SN7.value),
    (base_id + 400 + 3871): (b'O006', Snacks.SN70.value),
    (base_id + 400 + 3872): (b'O006', Snacks.SN71.value),
    (base_id + 400 + 3873): (b'O006', Snacks.SN72.value),
    (base_id + 400 + 3874): (b'O006', Snacks.SN73.value),
    (base_id + 400 + 3875): (b'O006', Snacks.SN74.value),
    (base_id + 400 + 3876): (b'O006', Snacks.SN75.value),
    (base_id + 400 + 3877): (b'O006', Snacks.SN76.value),
    (base_id + 400 + 3878): (b'O006', Snacks.SN77.value),
    (base_id + 400 + 3879): (b'O006', Snacks.SN78.value),
    (base_id + 400 + 3880): (b'O006', Snacks.SN79.value),
    (base_id + 400 + 3881): (b'O006', Snacks.SN8.value),
    (base_id + 400 + 3882): (b'O006', Snacks.SN80.value),
    (base_id + 400 + 3883): (b'O006', Snacks.SN81.value),
    (base_id + 400 + 3884): (b'O006', Snacks.SN82.value),
    (base_id + 400 + 3885): (b'O006', Snacks.SN83.value),
    (base_id + 400 + 3886): (b'O006', Snacks.SN84.value),
    (base_id + 400 + 3887): (b'O006', Snacks.SN85.value),
    (base_id + 400 + 3888): (b'O006', Snacks.SN86.value),
    (base_id + 400 + 3889): (b'O006', Snacks.SN87.value),
    (base_id + 400 + 3890): (b'O006', Snacks.SN88.value),
    (base_id + 400 + 3891): (b'O006', Snacks.SN9.value),
    (base_id + 400 + 3892): (b'O006', Snacks.SSBOX01.value),
    (base_id + 400 + 3893): (b'O006', Snacks.SSBOX02.value),
    (base_id + 400 + 3894): (b'O006', Snacks.SSBOX03.value),
    (base_id + 400 + 3895): (b'O006', Snacks.SSBOX04.value),
    (base_id + 400 + 3896): (b'O006', Snacks.SSBOX05.value),

    (base_id + 400 + 3897): (b'P001', Snacks.EX__CLUE__SNACKBOX__1.value),
    (base_id + 400 + 3898): (b'P001', Snacks.EX__CLUE__SNACKBOX__2.value),
    (base_id + 400 + 3899): (b'P001', Snacks.HIGH__SNACK__BOX.value),
    (base_id + 400 + 3900): (b'P001', Snacks.SNACK__BOX__BEHIND__MOODY.value),
    (base_id + 400 + 3901): (b'P001', Snacks.SNACK__BOX__LEFT__CORRIDOR.value),
    (base_id + 400 + 3902): (b'P001', Snacks.SNACK__BOX__LEFT__CORRIDOR__2.value),
    (base_id + 400 + 3903): (b'P001', Snacks.SS115.value),
    (base_id + 400 + 3904): (b'P001', Snacks.SS1150.value),
    (base_id + 400 + 3905): (b'P001', Snacks.SS1151.value),
    (base_id + 400 + 3906): (b'P001', Snacks.SS1152.value),
    (base_id + 400 + 3907): (b'P001', Snacks.SS1153.value),
    (base_id + 400 + 3908): (b'P001', Snacks.SS16.value),
    (base_id + 400 + 3909): (b'P001', Snacks.SS160.value),
    (base_id + 400 + 3910): (b'P001', Snacks.SS1600.value),
    (base_id + 400 + 3911): (b'P001', Snacks.SS17.value),
    (base_id + 400 + 3912): (b'P001', Snacks.SS170.value),
    (base_id + 400 + 3913): (b'P001', Snacks.SS171.value),
    (base_id + 400 + 3914): (b'P001', Snacks.SS172.value),
    (base_id + 400 + 3915): (b'P001', Snacks.SS173.value),
    (base_id + 400 + 3916): (b'P001', Snacks.SS174.value),
    (base_id + 400 + 3917): (b'P001', Snacks.SS175.value),
    (base_id + 400 + 3918): (b'P001', Snacks.SS18.value),
    (base_id + 400 + 3919): (b'P001', Snacks.SS180.value),
    (base_id + 400 + 3920): (b'P001', Snacks.SS181.value),
    (base_id + 400 + 3921): (b'P001', Snacks.SS182.value),
    (base_id + 400 + 3922): (b'P001', Snacks.SS183.value),
    (base_id + 400 + 3923): (b'P001', Snacks.SS47.value),
    (base_id + 400 + 3924): (b'P001', Snacks.SS470.value),
    (base_id + 400 + 3925): (b'P001', Snacks.SS471.value),
    (base_id + 400 + 3926): (b'P001', Snacks.SS472.value),
    (base_id + 400 + 3927): (b'P001', Snacks.SS473.value),

    (base_id + 400 + 3928): (b'P002', Snacks.EX__CLUE__SNACKBOX__2.value),
    (base_id + 400 + 3929): (b'P002', Snacks.EX__CLUE__SNACKBOX__3.value),
    (base_id + 400 + 3930): (b'P002', Snacks.SNACK12.value),
    (base_id + 400 + 3931): (b'P002', Snacks.SNACK120.value),
    (base_id + 400 + 3932): (b'P002', Snacks.SNACK14.value),
    (base_id + 400 + 3933): (b'P002', Snacks.SNACK16.value),
    (base_id + 400 + 3934): (b'P002', Snacks.SNACK18.value),
    (base_id + 400 + 3935): (b'P002', Snacks.SNACKBOX1.value),
    (base_id + 400 + 3936): (b'P002', Snacks.SNACKBOX2.value),
    (base_id + 400 + 3937): (b'P002', Snacks.SNACKBOX3.value),
    (base_id + 400 + 3938): (b'P002', Snacks.SNACKBOX30.value),
    (base_id + 400 + 3939): (b'P002', Snacks.SS12.value),
    (base_id + 400 + 3940): (b'P002', Snacks.SS13.value),
    (base_id + 400 + 3941): (b'P002', Snacks.SS14.value),
    (base_id + 400 + 3942): (b'P002', Snacks.SS15.value),
    (base_id + 400 + 3943): (b'P002', Snacks.SS17.value),
    (base_id + 400 + 3944): (b'P002', Snacks.SS170.value),
    (base_id + 400 + 3945): (b'P002', Snacks.SS171.value),
    (base_id + 400 + 3946): (b'P002', Snacks.SS172.value),
    (base_id + 400 + 3947): (b'P002', Snacks.SS173.value),
    (base_id + 400 + 3948): (b'P002', Snacks.SS18.value),
    (base_id + 400 + 3949): (b'P002', Snacks.SS180.value),
    (base_id + 400 + 3950): (b'P002', Snacks.SS181.value),
    (base_id + 400 + 3951): (b'P002', Snacks.SS182.value),
    (base_id + 400 + 3952): (b'P002', Snacks.SS5.value),
    (base_id + 400 + 3953): (b'P002', Snacks.SS6.value),
    (base_id + 400 + 3954): (b'P002', Snacks.TUNNEL__SNACK__BOX.value),

    (base_id + 400 + 3955): (b'P003', Snacks.BOX__O__SNACKS__UNDER__SWINGER.value),
    (base_id + 400 + 3956): (b'P003', Snacks.BOX__O__SNACKS__UNDER__SWINGER0.value),
    (base_id + 400 + 3957): (b'P003', Snacks.BOX__O__SNACKS__UNDER__SWINGER00.value),
    (base_id + 400 + 3958): (b'P003', Snacks.EXCLUE__SNACKBOX__1.value),
    (base_id + 400 + 3959): (b'P003', Snacks.SNACKBOX0.value),
    (base_id + 400 + 3960): (b'P003', Snacks.SS16.value),
    (base_id + 400 + 3961): (b'P003', Snacks.SS160.value),
    (base_id + 400 + 3962): (b'P003', Snacks.SS1600.value),
    (base_id + 400 + 3963): (b'P003', Snacks.SS170.value),
    (base_id + 400 + 3964): (b'P003', Snacks.SS1700.value),
    (base_id + 400 + 3965): (b'P003', Snacks.SS181.value),
    (base_id + 400 + 3966): (b'P003', Snacks.SS182.value),
    (base_id + 400 + 3967): (b'P003', Snacks.SS183.value),
    (base_id + 400 + 3968): (b'P003', Snacks.SS1861.value),
    (base_id + 400 + 3969): (b'P003', Snacks.SS1862.value),
    (base_id + 400 + 3970): (b'P003', Snacks.SS1863.value),
    (base_id + 400 + 3971): (b'P003', Snacks.SS192.value),
    (base_id + 400 + 3972): (b'P003', Snacks.SS1920.value),
    (base_id + 400 + 3973): (b'P003', Snacks.SS1921.value),
    (base_id + 400 + 3974): (b'P003', Snacks.SS2.value),
    (base_id + 400 + 3975): (b'P003', Snacks.SS20.value),
    (base_id + 400 + 3976): (b'P003', Snacks.SS2000.value),
    (base_id + 400 + 3977): (b'P003', Snacks.SS20000.value),
    (base_id + 400 + 3978): (b'P003', Snacks.SS200000.value),
    (base_id + 400 + 3979): (b'P003', Snacks.SS2000000.value),
    (base_id + 400 + 3980): (b'P003', Snacks.SS20000000.value),
    (base_id + 400 + 3981): (b'P003', Snacks.SS200000000.value),
    (base_id + 400 + 3982): (b'P003', Snacks.SS3.value),
    (base_id + 400 + 3983): (b'P003', Snacks.SS4.value),
    (base_id + 400 + 3984): (b'P003', Snacks.SWINGER__SNACK__LINE.value),
    (base_id + 400 + 3985): (b'P003', Snacks.SWINGER__SNACK__LINE0.value),
    (base_id + 400 + 3986): (b'P003', Snacks.SWINGER__SNACK__LINE00.value),
    (base_id + 400 + 3987): (b'P003', Snacks.SWINGER__SNACK__LINE1.value),
    (base_id + 400 + 3988): (b'P003', Snacks.SWINGER__SNACK__LINE10.value),
    (base_id + 400 + 3989): (b'P003', Snacks.SWINGER__SNACK__LINE100.value),

    (base_id + 400 + 3990): (b'P004', Snacks.S1.value),
    (base_id + 400 + 3991): (b'P004', Snacks.S10.value),
    (base_id + 400 + 3992): (b'P004', Snacks.S11.value),
    (base_id + 400 + 3993): (b'P004', Snacks.S14.value),
    (base_id + 400 + 3994): (b'P004', Snacks.S16.value),
    (base_id + 400 + 3995): (b'P004', Snacks.S18.value),
    (base_id + 400 + 3996): (b'P004', Snacks.S2.value),
    (base_id + 400 + 3997): (b'P004', Snacks.S21.value),
    (base_id + 400 + 3998): (b'P004', Snacks.S23.value),
    (base_id + 400 + 3999): (b'P004', Snacks.S25.value),
    (base_id + 400 + 4000): (b'P004', Snacks.S27.value),
    (base_id + 400 + 4001): (b'P004', Snacks.S3.value),
    (base_id + 400 + 4002): (b'P004', Snacks.S30.value),
    (base_id + 400 + 4003): (b'P004', Snacks.S31.value),
    (base_id + 400 + 4004): (b'P004', Snacks.S32.value),
    (base_id + 400 + 4005): (b'P004', Snacks.S33.value),
    (base_id + 400 + 4006): (b'P004', Snacks.S4.value),
    (base_id + 400 + 4007): (b'P004', Snacks.S40.value),
    (base_id + 400 + 4008): (b'P004', Snacks.S43.value),
    (base_id + 400 + 4009): (b'P004', Snacks.S44.value),
    (base_id + 400 + 4010): (b'P004', Snacks.S471.value),
    (base_id + 400 + 4011): (b'P004', Snacks.S472.value),
    (base_id + 400 + 4012): (b'P004', Snacks.S475.value),
    (base_id + 400 + 4013): (b'P004', Snacks.S476.value),
    (base_id + 400 + 4014): (b'P004', Snacks.SNACK__BOX__1__MILLION.value),
    (base_id + 400 + 4015): (b'P004', Snacks.SNACK12.value),
    (base_id + 400 + 4016): (b'P004', Snacks.SNACK120.value),
    (base_id + 400 + 4017): (b'P004', Snacks.SNACK121.value),
    (base_id + 400 + 4018): (b'P004', Snacks.SNACK123.value),
    (base_id + 400 + 4019): (b'P004', Snacks.SNACK124.value),
    (base_id + 400 + 4020): (b'P004', Snacks.SNACK125.value),
    (base_id + 400 + 4021): (b'P004', Snacks.SNACKBOX1.value),
    (base_id + 400 + 4022): (b'P004', Snacks.SNACKBOX10.value),
    (base_id + 400 + 4023): (b'P004', Snacks.SNACKBOX11.value),
    (base_id + 400 + 4024): (b'P004', Snacks.SS1.value),
    (base_id + 400 + 4025): (b'P004', Snacks.SS2.value),
    (base_id + 400 + 4026): (b'P004', Snacks.SS3.value),
    (base_id + 400 + 4027): (b'P004', Snacks.SS4.value),
    (base_id + 400 + 4028): (b'P004', Snacks.SS5.value),

    (base_id + 400 + 4029): (b'P005', Snacks.SS115.value),
    (base_id + 400 + 4030): (b'P005', Snacks.SS190.value),
    (base_id + 400 + 4031): (b'P005', Snacks.SS220.value),
    (base_id + 400 + 4032): (b'P005', Snacks.EX__CLUE__SNACKBOX__2.value),
    (base_id + 400 + 4033): (b'P005', Snacks.EX__CLUE__SNACKBOX__3.value),
    (base_id + 400 + 4034): (b'P005', Snacks.EX__CLUE__SNACKBOX__4.value),
    (base_id + 400 + 4035): (b'P005', Snacks.S5.value),
    (base_id + 400 + 4036): (b'P005', Snacks.S51.value),
    (base_id + 400 + 4037): (b'P005', Snacks.S53.value),
    (base_id + 400 + 4038): (b'P005', Snacks.S55.value),
    (base_id + 400 + 4039): (b'P005', Snacks.S56.value),
    (base_id + 400 + 4040): (b'P005', Snacks.S561.value),
    (base_id + 400 + 4041): (b'P005', Snacks.S563.value),
    (base_id + 400 + 4042): (b'P005', Snacks.S565.value),
    (base_id + 400 + 4043): (b'P005', Snacks.SS1.value),
    (base_id + 400 + 4044): (b'P005', Snacks.SS4.value),
    (base_id + 400 + 4045): (b'P005', Snacks.SS5.value),
    (base_id + 400 + 4046): (b'P005', Snacks.SS8.value),
    (base_id + 400 + 4047): (b'P005', Snacks.SS9.value),
    (base_id + 400 + 4048): (b'P005', Snacks.SS10.value),
    (base_id + 400 + 4049): (b'P005', Snacks.SS11.value),
    (base_id + 400 + 4050): (b'P005', Snacks.SS12.value),
    (base_id + 400 + 4051): (b'P005', Snacks.SS13.value),
    (base_id + 400 + 4052): (b'P005', Snacks.SS18.value),
    (base_id + 400 + 4053): (b'P005', Snacks.SS19.value),
    (base_id + 400 + 4054): (b'P005', Snacks.SS22.value),
    (base_id + 400 + 4055): (b'P005', Snacks.SS40.value),
    (base_id + 400 + 4056): (b'P005', Snacks.SS42.value),
    (base_id + 400 + 4057): (b'P005', Snacks.SS43.value),
    (base_id + 400 + 4058): (b'P005', Snacks.SS44.value),
    (base_id + 400 + 4059): (b'P005', Snacks.SS45.value),
    (base_id + 400 + 4060): (b'P005', Snacks.SS46.value),
    (base_id + 400 + 4061): (b'P005', Snacks.SS50.value),
    (base_id + 400 + 4062): (b'P005', Snacks.SS51.value),
    (base_id + 400 + 4063): (b'P005', Snacks.SS52.value),
    (base_id + 400 + 4064): (b'P005', Snacks.SS53.value),
    (base_id + 400 + 4065): (b'P005', Snacks.SS54.value),
    (base_id + 400 + 4066): (b'P005', Snacks.SS55.value),
    (base_id + 400 + 4067): (b'P005', Snacks.SS110.value),
    (base_id + 400 + 4068): (b'P005', Snacks.SS111.value),
    (base_id + 400 + 4069): (b'P005', Snacks.SS112.value),
    (base_id + 400 + 4070): (b'P005', Snacks.SS113.value),
    (base_id + 400 + 4071): (b'P005', Snacks.SS114.value),

    # (base_id + 400 + 4072): (b'R001', Snacks.CRATE__1__PRIZE.value),   This is evidently not a snack, oops
    (base_id + 400 + 4073): (b'R001', Snacks.CRATE__2__PRIZE.value),
    (base_id + 400 + 4074): (b'R001', Snacks.SNACKBOX1.value),
    (base_id + 400 + 4075): (b'R001', Snacks.SNACKBOX2.value),
    (base_id + 400 + 4076): (b'R001', Snacks.SS10.value),
    (base_id + 400 + 4077): (b'R001', Snacks.SS100.value),
    (base_id + 400 + 4078): (b'R001', Snacks.SS11.value),
    (base_id + 400 + 4079): (b'R001', Snacks.SS12.value),
    (base_id + 400 + 4080): (b'R001', Snacks.SS13.value),
    (base_id + 400 + 4081): (b'R001', Snacks.SS14.value),
    (base_id + 400 + 4082): (b'R001', Snacks.SS15.value),
    (base_id + 400 + 4083): (b'R001', Snacks.SS16.value),
    (base_id + 400 + 4084): (b'R001', Snacks.SS17.value),
    (base_id + 400 + 4085): (b'R001', Snacks.SS18.value),
    (base_id + 400 + 4086): (b'R001', Snacks.SS19.value),
    (base_id + 400 + 4087): (b'R001', Snacks.SS2.value),
    (base_id + 400 + 4088): (b'R001', Snacks.SS20.value),
    (base_id + 400 + 4089): (b'R001', Snacks.SS21.value),
    (base_id + 400 + 4090): (b'R001', Snacks.SS22.value),
    (base_id + 400 + 4091): (b'R001', Snacks.SS23.value),
    (base_id + 400 + 4092): (b'R001', Snacks.SS24.value),
    (base_id + 400 + 4093): (b'R001', Snacks.SS25.value),
    (base_id + 400 + 4094): (b'R001', Snacks.SS26.value),
    (base_id + 400 + 4095): (b'R001', Snacks.SS27.value),
    (base_id + 400 + 4096): (b'R001', Snacks.SS28.value),
    (base_id + 400 + 4097): (b'R001', Snacks.SS29.value),
    (base_id + 400 + 4098): (b'R001', Snacks.SS3.value),
    (base_id + 400 + 4099): (b'R001', Snacks.SS30.value),
    (base_id + 400 + 4100): (b'R001', Snacks.SS31.value),
    (base_id + 400 + 4101): (b'R001', Snacks.SS32.value),
    (base_id + 400 + 4102): (b'R001', Snacks.SS33.value),
    (base_id + 400 + 4103): (b'R001', Snacks.SS34.value),
    (base_id + 400 + 4104): (b'R001', Snacks.SS35.value),
    (base_id + 400 + 4105): (b'R001', Snacks.SS36.value),
    (base_id + 400 + 4106): (b'R001', Snacks.SS37.value),
    (base_id + 400 + 4107): (b'R001', Snacks.SS39.value),
    (base_id + 400 + 4108): (b'R001', Snacks.SS4.value),
    (base_id + 400 + 4109): (b'R001', Snacks.SS40.value),
    (base_id + 400 + 4110): (b'R001', Snacks.SS41.value),
    (base_id + 400 + 4111): (b'R001', Snacks.SS42.value),
    (base_id + 400 + 4112): (b'R001', Snacks.SS43.value),
    (base_id + 400 + 4113): (b'R001', Snacks.SS44.value),
    (base_id + 400 + 4114): (b'R001', Snacks.SS45.value),
    (base_id + 400 + 4115): (b'R001', Snacks.SS46.value),
    (base_id + 400 + 4116): (b'R001', Snacks.SS47.value),
    (base_id + 400 + 4117): (b'R001', Snacks.SS48.value),
    (base_id + 400 + 4118): (b'R001', Snacks.SS480.value),
    (base_id + 400 + 4119): (b'R001', Snacks.SS481.value),
    (base_id + 400 + 4120): (b'R001', Snacks.SS482.value),
    (base_id + 400 + 4121): (b'R001', Snacks.SS483.value),
    (base_id + 400 + 4122): (b'R001', Snacks.SS484.value),
    (base_id + 400 + 4123): (b'R001', Snacks.SS54.value),
    (base_id + 400 + 4124): (b'R001', Snacks.SS55.value),
    (base_id + 400 + 4125): (b'R001', Snacks.SS56.value),
    (base_id + 400 + 4126): (b'R001', Snacks.SS57.value),
    (base_id + 400 + 4127): (b'R001', Snacks.SS58.value),
    (base_id + 400 + 4128): (b'R001', Snacks.SS59.value),
    (base_id + 400 + 4129): (b'R001', Snacks.SS6.value),
    (base_id + 400 + 4130): (b'R001', Snacks.SS60.value),
    (base_id + 400 + 4131): (b'R001', Snacks.SS61.value),
    (base_id + 400 + 4132): (b'R001', Snacks.SS62.value),
    (base_id + 400 + 4133): (b'R001', Snacks.SS63.value),
    (base_id + 400 + 4134): (b'R001', Snacks.SS64.value),
    (base_id + 400 + 4135): (b'R001', Snacks.SS65.value),
    (base_id + 400 + 4136): (b'R001', Snacks.SS66.value),
    (base_id + 400 + 4137): (b'R001', Snacks.SS67.value),
    (base_id + 400 + 4138): (b'R001', Snacks.SS68.value),
    (base_id + 400 + 4139): (b'R001', Snacks.SS69.value),
    (base_id + 400 + 4140): (b'R001', Snacks.SS7.value),
    (base_id + 400 + 4141): (b'R001', Snacks.SS70.value),
    (base_id + 400 + 4142): (b'R001', Snacks.SS71.value),
    (base_id + 400 + 4143): (b'R001', Snacks.SS72.value),
    (base_id + 400 + 4144): (b'R001', Snacks.SS73.value),
    (base_id + 400 + 4145): (b'R001', Snacks.SS74.value),
    (base_id + 400 + 4146): (b'R001', Snacks.SS75.value),
    (base_id + 400 + 4147): (b'R001', Snacks.SS76.value),
    (base_id + 400 + 4148): (b'R001', Snacks.SS77.value),
    (base_id + 400 + 4149): (b'R001', Snacks.SS78.value),
    (base_id + 400 + 4150): (b'R001', Snacks.SS79.value),
    (base_id + 400 + 4151): (b'R001', Snacks.SS8.value),
    (base_id + 400 + 4152): (b'R001', Snacks.SS80.value),
    (base_id + 400 + 4153): (b'R001', Snacks.SS81.value),
    (base_id + 400 + 4154): (b'R001', Snacks.SS82.value),
    (base_id + 400 + 4155): (b'R001', Snacks.SS83.value),
    (base_id + 400 + 4156): (b'R001', Snacks.SS84.value),
    (base_id + 400 + 4157): (b'R001', Snacks.SS85.value),
    (base_id + 400 + 4158): (b'R001', Snacks.SS86.value),
    (base_id + 400 + 4159): (b'R001', Snacks.SS87.value),
    (base_id + 400 + 4160): (b'R001', Snacks.SS88.value),
    (base_id + 400 + 4161): (b'R001', Snacks.SS89.value),
    (base_id + 400 + 4162): (b'R001', Snacks.SS9.value),
    (base_id + 400 + 4163): (b'R001', Snacks.SS90.value),
    (base_id + 400 + 4164): (b'R001', Snacks.SS91.value),
    (base_id + 400 + 4165): (b'R001', Snacks.SS92.value),
    (base_id + 400 + 4166): (b'R001', Snacks.SS93.value),
    (base_id + 400 + 4167): (b'R001', Snacks.SS94.value),
    (base_id + 400 + 4168): (b'R001', Snacks.SS95.value),
    (base_id + 400 + 4169): (b'R001', Snacks.SS96.value),
    (base_id + 400 + 4170): (b'R001', Snacks.SS97.value),
    (base_id + 400 + 4171): (b'R001', Snacks.SS98.value),
    (base_id + 400 + 4172): (b'R001', Snacks.SS99.value),

    (base_id + 400 + 4173): (b'R003', Snacks.CRATE__2__PRIZE.value),
    (base_id + 400 + 4174): (b'R003', Snacks.CRATE__3__PRIZE.value),
    (base_id + 400 + 4175): (b'R003', Snacks.SNACKBOX__1.value),
    (base_id + 400 + 4176): (b'R003', Snacks.SS1.value),
    (base_id + 400 + 4177): (b'R003', Snacks.SS11.value),
    (base_id + 400 + 4178): (b'R003', Snacks.SS12.value),
    (base_id + 400 + 4179): (b'R003', Snacks.SS13.value),
    (base_id + 400 + 4180): (b'R003', Snacks.SS14.value),
    (base_id + 400 + 4181): (b'R003', Snacks.SS15.value),
    (base_id + 400 + 4182): (b'R003', Snacks.SS16.value),
    (base_id + 400 + 4183): (b'R003', Snacks.SS17.value),
    (base_id + 400 + 4184): (b'R003', Snacks.SS18.value),
    (base_id + 400 + 4185): (b'R003', Snacks.SS19.value),
    (base_id + 400 + 4186): (b'R003', Snacks.SS2.value),
    (base_id + 400 + 4187): (b'R003', Snacks.SS20.value),
    (base_id + 400 + 4188): (b'R003', Snacks.SS21.value),
    (base_id + 400 + 4189): (b'R003', Snacks.SS22.value),
    (base_id + 400 + 4190): (b'R003', Snacks.SS23.value),
    (base_id + 400 + 4191): (b'R003', Snacks.SS24.value),
    (base_id + 400 + 4192): (b'R003', Snacks.SS25.value),
    (base_id + 400 + 4193): (b'R003', Snacks.SS26.value),
    (base_id + 400 + 4194): (b'R003', Snacks.SS27.value),
    (base_id + 400 + 4195): (b'R003', Snacks.SS28.value),
    (base_id + 400 + 4196): (b'R003', Snacks.SS29.value),
    (base_id + 400 + 4197): (b'R003', Snacks.SS3.value),
    (base_id + 400 + 4198): (b'R003', Snacks.SS30.value),
    (base_id + 400 + 4199): (b'R003', Snacks.SS32.value),
    (base_id + 400 + 4200): (b'R003', Snacks.SS33.value),
    (base_id + 400 + 4201): (b'R003', Snacks.SS34.value),
    (base_id + 400 + 4202): (b'R003', Snacks.SS35.value),
    (base_id + 400 + 4203): (b'R003', Snacks.SS4.value),
    (base_id + 400 + 4204): (b'R003', Snacks.SS44.value),
    (base_id + 400 + 4205): (b'R003', Snacks.SS45.value),
    (base_id + 400 + 4206): (b'R003', Snacks.SS46.value),
    (base_id + 400 + 4207): (b'R003', Snacks.SS47.value),
    (base_id + 400 + 4208): (b'R003', Snacks.SS48.value),
    (base_id + 400 + 4209): (b'R003', Snacks.SS49.value),
    (base_id + 400 + 4210): (b'R003', Snacks.SS5.value),
    (base_id + 400 + 4211): (b'R003', Snacks.SS50.value),
    (base_id + 400 + 4212): (b'R003', Snacks.SS51.value),
    (base_id + 400 + 4213): (b'R003', Snacks.SS52.value),
    (base_id + 400 + 4214): (b'R003', Snacks.SS53.value),
    (base_id + 400 + 4215): (b'R003', Snacks.SS54.value),
    (base_id + 400 + 4216): (b'R003', Snacks.SS55.value),
    (base_id + 400 + 4217): (b'R003', Snacks.SS6.value),
    (base_id + 400 + 4218): (b'R003', Snacks.SS7.value),
    (base_id + 400 + 4219): (b'R003', Snacks.SS8.value),
    (base_id + 400 + 4220): (b'R003', Snacks.SS9.value),

    (base_id + 400 + 4221): (b'R004', Snacks.SN1.value),
    (base_id + 400 + 4222): (b'R004', Snacks.SN10.value),
    (base_id + 400 + 4223): (b'R004', Snacks.SN101.value),
    (base_id + 400 + 4224): (b'R004', Snacks.SN102.value),
    (base_id + 400 + 4225): (b'R004', Snacks.SN103.value),
    (base_id + 400 + 4226): (b'R004', Snacks.SN104.value),
    (base_id + 400 + 4227): (b'R004', Snacks.SN105.value),
    (base_id + 400 + 4228): (b'R004', Snacks.SN11.value),
    (base_id + 400 + 4229): (b'R004', Snacks.SN12.value),
    (base_id + 400 + 4230): (b'R004', Snacks.SN13.value),
    (base_id + 400 + 4231): (b'R004', Snacks.SN15.value),
    (base_id + 400 + 4232): (b'R004', Snacks.SN16.value),
    (base_id + 400 + 4233): (b'R004', Snacks.SN17.value),
    (base_id + 400 + 4234): (b'R004', Snacks.SN18.value),
    (base_id + 400 + 4235): (b'R004', Snacks.SN19.value),
    (base_id + 400 + 4236): (b'R004', Snacks.SN2.value),
    (base_id + 400 + 4237): (b'R004', Snacks.SN20.value),
    (base_id + 400 + 4238): (b'R004', Snacks.SN21.value),
    (base_id + 400 + 4239): (b'R004', Snacks.SN22.value),
    (base_id + 400 + 4240): (b'R004', Snacks.SN23.value),
    (base_id + 400 + 4241): (b'R004', Snacks.SN24.value),
    (base_id + 400 + 4242): (b'R004', Snacks.SN25.value),
    (base_id + 400 + 4243): (b'R004', Snacks.SN26.value),
    (base_id + 400 + 4244): (b'R004', Snacks.SN27.value),
    (base_id + 400 + 4245): (b'R004', Snacks.SN28.value),
    (base_id + 400 + 4246): (b'R004', Snacks.SN29.value),
    (base_id + 400 + 4247): (b'R004', Snacks.SN3.value),
    (base_id + 400 + 4248): (b'R004', Snacks.SN30.value),
    (base_id + 400 + 4249): (b'R004', Snacks.SN31.value),
    (base_id + 400 + 4250): (b'R004', Snacks.SN32.value),
    (base_id + 400 + 4251): (b'R004', Snacks.SN33.value),
    (base_id + 400 + 4252): (b'R004', Snacks.SN34.value),
    (base_id + 400 + 4253): (b'R004', Snacks.SN35.value),
    (base_id + 400 + 4254): (b'R004', Snacks.SN36.value),
    (base_id + 400 + 4255): (b'R004', Snacks.SN37.value),
    (base_id + 400 + 4256): (b'R004', Snacks.SN38.value),
    (base_id + 400 + 4257): (b'R004', Snacks.SN39.value),
    (base_id + 400 + 4258): (b'R004', Snacks.SN4.value),
    (base_id + 400 + 4259): (b'R004', Snacks.SN40.value),
    (base_id + 400 + 4260): (b'R004', Snacks.SN41.value),
    (base_id + 400 + 4261): (b'R004', Snacks.SN42.value),
    (base_id + 400 + 4262): (b'R004', Snacks.SN43.value),
    (base_id + 400 + 4263): (b'R004', Snacks.SN44.value),
    (base_id + 400 + 4264): (b'R004', Snacks.SN45.value),
    (base_id + 400 + 4265): (b'R004', Snacks.SN46.value),
    (base_id + 400 + 4266): (b'R004', Snacks.SN47.value),
    (base_id + 400 + 4267): (b'R004', Snacks.SN48.value),
    (base_id + 400 + 4268): (b'R004', Snacks.SN49.value),
    (base_id + 400 + 4269): (b'R004', Snacks.SN5.value),
    (base_id + 400 + 4270): (b'R004', Snacks.SN50.value),
    (base_id + 400 + 4271): (b'R004', Snacks.SN51.value),
    (base_id + 400 + 4272): (b'R004', Snacks.SN52.value),
    (base_id + 400 + 4273): (b'R004', Snacks.SN53.value),
    (base_id + 400 + 4274): (b'R004', Snacks.SN54.value),
    (base_id + 400 + 4275): (b'R004', Snacks.SN55.value),
    (base_id + 400 + 4276): (b'R004', Snacks.SN56.value),
    (base_id + 400 + 4277): (b'R004', Snacks.SN57.value),
    (base_id + 400 + 4278): (b'R004', Snacks.SN58.value),
    (base_id + 400 + 4279): (b'R004', Snacks.SN59.value),
    (base_id + 400 + 4280): (b'R004', Snacks.SN6.value),
    (base_id + 400 + 4281): (b'R004', Snacks.SN60.value),
    (base_id + 400 + 4282): (b'R004', Snacks.SN61.value),
    (base_id + 400 + 4283): (b'R004', Snacks.SN62.value),
    (base_id + 400 + 4284): (b'R004', Snacks.SN63.value),
    (base_id + 400 + 4285): (b'R004', Snacks.SN64.value),
    (base_id + 400 + 4286): (b'R004', Snacks.SN65.value),
    (base_id + 400 + 4287): (b'R004', Snacks.SN66.value),
    (base_id + 400 + 4288): (b'R004', Snacks.SN67.value),
    (base_id + 400 + 4289): (b'R004', Snacks.SN68.value),
    (base_id + 400 + 4290): (b'R004', Snacks.SN69.value),
    (base_id + 400 + 4291): (b'R004', Snacks.SN7.value),
    (base_id + 400 + 4292): (b'R004', Snacks.SN70.value),
    (base_id + 400 + 4293): (b'R004', Snacks.SN71.value),
    (base_id + 400 + 4294): (b'R004', Snacks.SN72.value),
    (base_id + 400 + 4295): (b'R004', Snacks.SN73.value),
    (base_id + 400 + 4296): (b'R004', Snacks.SN74.value),
    (base_id + 400 + 4297): (b'R004', Snacks.SN75.value),
    (base_id + 400 + 4298): (b'R004', Snacks.SN76.value),
    (base_id + 400 + 4299): (b'R004', Snacks.SN77.value),
    (base_id + 400 + 4300): (b'R004', Snacks.SN78.value),
    (base_id + 400 + 4301): (b'R004', Snacks.SN79.value),
    (base_id + 400 + 4302): (b'R004', Snacks.SN80.value),
    (base_id + 400 + 4303): (b'R004', Snacks.SN81.value),
    (base_id + 400 + 4304): (b'R004', Snacks.SN82.value),
    (base_id + 400 + 4305): (b'R004', Snacks.SN83.value),
    (base_id + 400 + 4306): (b'R004', Snacks.SN84.value),
    (base_id + 400 + 4307): (b'R004', Snacks.SN85.value),
    (base_id + 400 + 4308): (b'R004', Snacks.SN86.value),
    (base_id + 400 + 4309): (b'R004', Snacks.SN88.value),
    (base_id + 400 + 4310): (b'R004', Snacks.SN89.value),
    (base_id + 400 + 4311): (b'R004', Snacks.SN9.value),
    (base_id + 400 + 4312): (b'R004', Snacks.SN90.value),
    (base_id + 400 + 4313): (b'R004', Snacks.SN91.value),
    (base_id + 400 + 4314): (b'R004', Snacks.SN92.value),
    (base_id + 400 + 4315): (b'R004', Snacks.SN93.value),
    (base_id + 400 + 4316): (b'R004', Snacks.SN94.value),
    (base_id + 400 + 4317): (b'R004', Snacks.SN95.value),
    (base_id + 400 + 4318): (b'R004', Snacks.SN96.value),
    (base_id + 400 + 4319): (b'R004', Snacks.SN97.value),
    (base_id + 400 + 4320): (b'R004', Snacks.SN98.value),
    (base_id + 400 + 4321): (b'R004', Snacks.SNACKBOX__1.value),
    (base_id + 400 + 4322): (b'R004', Snacks.SNACKBOX__2.value),

    (base_id + 400 + 4323): (b'R005', Snacks.SNACKBOX.value),
    (base_id + 400 + 4324): (b'R005', Snacks.SS1.value),
    (base_id + 400 + 4325): (b'R005', Snacks.SS10.value),
    (base_id + 400 + 4326): (b'R005', Snacks.SS11.value),
    (base_id + 400 + 4327): (b'R005', Snacks.SS12.value),
    (base_id + 400 + 4328): (b'R005', Snacks.SS13.value),
    (base_id + 400 + 4329): (b'R005', Snacks.SS14.value),
    (base_id + 400 + 4330): (b'R005', Snacks.SS15.value),
    (base_id + 400 + 4331): (b'R005', Snacks.SS16.value),
    (base_id + 400 + 4332): (b'R005', Snacks.SS17.value),
    (base_id + 400 + 4333): (b'R005', Snacks.SS18.value),
    (base_id + 400 + 4334): (b'R005', Snacks.SS19.value),
    (base_id + 400 + 4335): (b'R005', Snacks.SS2.value),
    (base_id + 400 + 4336): (b'R005', Snacks.SS20.value),
    (base_id + 400 + 4337): (b'R005', Snacks.SS21.value),
    (base_id + 400 + 4338): (b'R005', Snacks.SS22.value),
    (base_id + 400 + 4339): (b'R005', Snacks.SS23.value),
    (base_id + 400 + 4340): (b'R005', Snacks.SS24.value),
    (base_id + 400 + 4341): (b'R005', Snacks.SS25.value),
    (base_id + 400 + 4342): (b'R005', Snacks.SS26.value),
    (base_id + 400 + 4343): (b'R005', Snacks.SS27.value),
    (base_id + 400 + 4344): (b'R005', Snacks.SS28.value),
    (base_id + 400 + 4345): (b'R005', Snacks.SS29.value),
    (base_id + 400 + 4346): (b'R005', Snacks.SS3.value),
    (base_id + 400 + 4347): (b'R005', Snacks.SS30.value),
    (base_id + 400 + 4348): (b'R005', Snacks.SS31.value),
    (base_id + 400 + 4349): (b'R005', Snacks.SS32.value),
    (base_id + 400 + 4350): (b'R005', Snacks.SS33.value),
    (base_id + 400 + 4351): (b'R005', Snacks.SS34.value),
    (base_id + 400 + 4352): (b'R005', Snacks.SS35.value),
    (base_id + 400 + 4353): (b'R005', Snacks.SS36.value),
    (base_id + 400 + 4354): (b'R005', Snacks.SS37.value),
    (base_id + 400 + 4355): (b'R005', Snacks.SS38.value),
    (base_id + 400 + 4356): (b'R005', Snacks.SS39.value),
    (base_id + 400 + 4357): (b'R005', Snacks.SS4.value),
    (base_id + 400 + 4358): (b'R005', Snacks.SS40.value),
    (base_id + 400 + 4359): (b'R005', Snacks.SS41.value),
    (base_id + 400 + 4360): (b'R005', Snacks.SS42.value),
    (base_id + 400 + 4361): (b'R005', Snacks.SS43.value),
    (base_id + 400 + 4362): (b'R005', Snacks.SS44.value),
    (base_id + 400 + 4363): (b'R005', Snacks.SS45.value),
    (base_id + 400 + 4364): (b'R005', Snacks.SS46.value),
    (base_id + 400 + 4365): (b'R005', Snacks.SS47.value),
    (base_id + 400 + 4366): (b'R005', Snacks.SS470.value),
    (base_id + 400 + 4367): (b'R005', Snacks.SS48.value),
    (base_id + 400 + 4368): (b'R005', Snacks.SS49.value),
    (base_id + 400 + 4369): (b'R005', Snacks.SS5.value),
    (base_id + 400 + 4370): (b'R005', Snacks.SS50.value),
    (base_id + 400 + 4371): (b'R005', Snacks.SS6.value),

    (base_id + 400 + 4372): (b'R020', Snacks.SN1.value),
    (base_id + 400 + 4373): (b'R020', Snacks.SN10.value),
    (base_id + 400 + 4374): (b'R020', Snacks.SN11.value),
    (base_id + 400 + 4375): (b'R020', Snacks.SN12.value),
    (base_id + 400 + 4376): (b'R020', Snacks.SN13.value),
    (base_id + 400 + 4377): (b'R020', Snacks.SN14.value),
    (base_id + 400 + 4378): (b'R020', Snacks.SN15.value),
    (base_id + 400 + 4379): (b'R020', Snacks.SN16.value),
    (base_id + 400 + 4380): (b'R020', Snacks.SN17.value),
    (base_id + 400 + 4381): (b'R020', Snacks.SN18.value),
    (base_id + 400 + 4382): (b'R020', Snacks.SN19.value),
    (base_id + 400 + 4383): (b'R020', Snacks.SN2.value),
    (base_id + 400 + 4384): (b'R020', Snacks.SN20.value),
    (base_id + 400 + 4385): (b'R020', Snacks.SN21.value),
    (base_id + 400 + 4386): (b'R020', Snacks.SN22.value),
    (base_id + 400 + 4387): (b'R020', Snacks.SN23.value),
    (base_id + 400 + 4388): (b'R020', Snacks.SN24.value),
    (base_id + 400 + 4389): (b'R020', Snacks.SN25.value),
    (base_id + 400 + 4390): (b'R020', Snacks.SN26.value),
    (base_id + 400 + 4391): (b'R020', Snacks.SN27.value),
    (base_id + 400 + 4392): (b'R020', Snacks.SN28.value),
    (base_id + 400 + 4393): (b'R020', Snacks.SN29.value),
    (base_id + 400 + 4394): (b'R020', Snacks.SN3.value),
    (base_id + 400 + 4395): (b'R020', Snacks.SN30.value),
    (base_id + 400 + 4396): (b'R020', Snacks.SN31.value),
    (base_id + 400 + 4397): (b'R020', Snacks.SN32.value),
    (base_id + 400 + 4398): (b'R020', Snacks.SN33.value),
    (base_id + 400 + 4399): (b'R020', Snacks.SN34.value),
    (base_id + 400 + 4400): (b'R020', Snacks.SN35.value),
    (base_id + 400 + 4401): (b'R020', Snacks.SN36.value),
    (base_id + 400 + 4402): (b'R020', Snacks.SN37.value),
    (base_id + 400 + 4403): (b'R020', Snacks.SN38.value),
    (base_id + 400 + 4404): (b'R020', Snacks.SN39.value),
    (base_id + 400 + 4405): (b'R020', Snacks.SN4.value),
    (base_id + 400 + 4406): (b'R020', Snacks.SN40.value),
    (base_id + 400 + 4407): (b'R020', Snacks.SN41.value),
    (base_id + 400 + 4408): (b'R020', Snacks.SN42.value),
    (base_id + 400 + 4409): (b'R020', Snacks.SN43.value),
    (base_id + 400 + 4410): (b'R020', Snacks.SN44.value),
    (base_id + 400 + 4411): (b'R020', Snacks.SN45.value),
    (base_id + 400 + 4412): (b'R020', Snacks.SN46.value),
    (base_id + 400 + 4413): (b'R020', Snacks.SN47.value),
    (base_id + 400 + 4414): (b'R020', Snacks.SN48.value),
    (base_id + 400 + 4415): (b'R020', Snacks.SN49.value),
    (base_id + 400 + 4416): (b'R020', Snacks.SN5.value),
    (base_id + 400 + 4417): (b'R020', Snacks.SN50.value),
    (base_id + 400 + 4418): (b'R020', Snacks.SN51.value),
    (base_id + 400 + 4419): (b'R020', Snacks.SN52.value),
    (base_id + 400 + 4420): (b'R020', Snacks.SN53.value),
    (base_id + 400 + 4421): (b'R020', Snacks.SN54.value),
    (base_id + 400 + 4422): (b'R020', Snacks.SN55.value),
    (base_id + 400 + 4423): (b'R020', Snacks.SN56.value),
    (base_id + 400 + 4424): (b'R020', Snacks.SN57.value),
    (base_id + 400 + 4425): (b'R020', Snacks.SN58.value),
    (base_id + 400 + 4426): (b'R020', Snacks.SN59.value),
    (base_id + 400 + 4427): (b'R020', Snacks.SN6.value),
    (base_id + 400 + 4428): (b'R020', Snacks.SN60.value),
    (base_id + 400 + 4429): (b'R020', Snacks.SN61.value),
    (base_id + 400 + 4430): (b'R020', Snacks.SN62.value),
    (base_id + 400 + 4431): (b'R020', Snacks.SN63.value),
    (base_id + 400 + 4432): (b'R020', Snacks.SN64.value),
    (base_id + 400 + 4433): (b'R020', Snacks.SN65.value),
    (base_id + 400 + 4434): (b'R020', Snacks.SN66.value),
    (base_id + 400 + 4435): (b'R020', Snacks.SN67.value),
    (base_id + 400 + 4436): (b'R020', Snacks.SN68.value),
    (base_id + 400 + 4437): (b'R020', Snacks.SN69.value),
    (base_id + 400 + 4438): (b'R020', Snacks.SN7.value),
    (base_id + 400 + 4439): (b'R020', Snacks.SN70.value),
    (base_id + 400 + 4440): (b'R020', Snacks.SN71.value),
    (base_id + 400 + 4441): (b'R020', Snacks.SN72.value),
    (base_id + 400 + 4442): (b'R020', Snacks.SN73.value),
    (base_id + 400 + 4443): (b'R020', Snacks.SN74.value),
    (base_id + 400 + 4444): (b'R020', Snacks.SN75.value),
    (base_id + 400 + 4445): (b'R020', Snacks.SN76.value),
    (base_id + 400 + 4446): (b'R020', Snacks.SN77.value),
    (base_id + 400 + 4447): (b'R020', Snacks.SN78.value),
    (base_id + 400 + 4448): (b'R020', Snacks.SN79.value),
    (base_id + 400 + 4449): (b'R020', Snacks.SN8.value),
    (base_id + 400 + 4450): (b'R020', Snacks.SN80.value),
    (base_id + 400 + 4451): (b'R020', Snacks.SN81.value),
    (base_id + 400 + 4452): (b'R020', Snacks.SN82.value),
    (base_id + 400 + 4453): (b'R020', Snacks.SN83.value),
    (base_id + 400 + 4454): (b'R020', Snacks.SN84.value),
    (base_id + 400 + 4455): (b'R020', Snacks.SN85.value),
    (base_id + 400 + 4456): (b'R020', Snacks.SN86.value),
    (base_id + 400 + 4457): (b'R020', Snacks.SN87.value),
    (base_id + 400 + 4458): (b'R020', Snacks.SN88.value),
    (base_id + 400 + 4459): (b'R020', Snacks.SN89.value),
    (base_id + 400 + 4460): (b'R020', Snacks.SN9.value),
    (base_id + 400 + 4461): (b'R020', Snacks.SN90.value),
    (base_id + 400 + 4462): (b'R020', Snacks.SN91.value),
    (base_id + 400 + 4463): (b'R020', Snacks.SN92.value),
    (base_id + 400 + 4464): (b'R020', Snacks.SN93.value),
    (base_id + 400 + 4465): (b'R020', Snacks.SN94.value),
    (base_id + 400 + 4466): (b'R020', Snacks.SN95.value),
    (base_id + 400 + 4467): (b'R020', Snacks.SN96.value),
    (base_id + 400 + 4468): (b'R020', Snacks.SN97.value),
    (base_id + 400 + 4469): (b'R020', Snacks.SN98.value),

    (base_id + 400 + 4470): (b'R021', Snacks.CRATE__2__PRIZE.value),
    (base_id + 400 + 4471): (b'R021', Snacks.CRATE__3__PRIZE.value),
    (base_id + 400 + 4472): (b'R021', Snacks.SN1.value),
    (base_id + 400 + 4473): (b'R021', Snacks.SN10.value),
    (base_id + 400 + 4474): (b'R021', Snacks.SN100.value),
    (base_id + 400 + 4475): (b'R021', Snacks.SN11.value),
    (base_id + 400 + 4476): (b'R021', Snacks.SN12.value),
    (base_id + 400 + 4477): (b'R021', Snacks.SN13.value),
    (base_id + 400 + 4478): (b'R021', Snacks.SN14.value),
    (base_id + 400 + 4479): (b'R021', Snacks.SN15.value),
    (base_id + 400 + 4480): (b'R021', Snacks.SN16.value),
    (base_id + 400 + 4481): (b'R021', Snacks.SN17.value),
    (base_id + 400 + 4482): (b'R021', Snacks.SN18.value),
    (base_id + 400 + 4483): (b'R021', Snacks.SN19.value),
    (base_id + 400 + 4484): (b'R021', Snacks.SN2.value),
    (base_id + 400 + 4485): (b'R021', Snacks.SN20.value),
    (base_id + 400 + 4486): (b'R021', Snacks.SN21.value),
    (base_id + 400 + 4487): (b'R021', Snacks.SN22.value),
    (base_id + 400 + 4488): (b'R021', Snacks.SN23.value),
    (base_id + 400 + 4489): (b'R021', Snacks.SN24.value),
    (base_id + 400 + 4490): (b'R021', Snacks.SN25.value),
    (base_id + 400 + 4491): (b'R021', Snacks.SN26.value),
    (base_id + 400 + 4492): (b'R021', Snacks.SN27.value),
    (base_id + 400 + 4493): (b'R021', Snacks.SN28.value),
    (base_id + 400 + 4494): (b'R021', Snacks.SN29.value),
    (base_id + 400 + 4495): (b'R021', Snacks.SN3.value),
    (base_id + 400 + 4496): (b'R021', Snacks.SN30.value),
    (base_id + 400 + 4497): (b'R021', Snacks.SN31.value),
    (base_id + 400 + 4498): (b'R021', Snacks.SN32.value),
    (base_id + 400 + 4499): (b'R021', Snacks.SN33.value),
    (base_id + 400 + 4500): (b'R021', Snacks.SN34.value),
    (base_id + 400 + 4501): (b'R021', Snacks.SN35.value),
    (base_id + 400 + 4502): (b'R021', Snacks.SN36.value),
    (base_id + 400 + 4503): (b'R021', Snacks.SN37.value),
    (base_id + 400 + 4504): (b'R021', Snacks.SN38.value),
    (base_id + 400 + 4505): (b'R021', Snacks.SN39.value),
    (base_id + 400 + 4506): (b'R021', Snacks.SN4.value),
    (base_id + 400 + 4507): (b'R021', Snacks.SN40.value),
    (base_id + 400 + 4508): (b'R021', Snacks.SN41.value),
    (base_id + 400 + 4509): (b'R021', Snacks.SN42.value),
    (base_id + 400 + 4510): (b'R021', Snacks.SN43.value),
    (base_id + 400 + 4511): (b'R021', Snacks.SN44.value),
    (base_id + 400 + 4512): (b'R021', Snacks.SN45.value),
    (base_id + 400 + 4513): (b'R021', Snacks.SN46.value),
    (base_id + 400 + 4514): (b'R021', Snacks.SN47.value),
    (base_id + 400 + 4515): (b'R021', Snacks.SN48.value),
    (base_id + 400 + 4516): (b'R021', Snacks.SN49.value),
    (base_id + 400 + 4517): (b'R021', Snacks.SN5.value),
    (base_id + 400 + 4518): (b'R021', Snacks.SN50.value),
    (base_id + 400 + 4519): (b'R021', Snacks.SN51.value),
    (base_id + 400 + 4520): (b'R021', Snacks.SN52.value),
    (base_id + 400 + 4521): (b'R021', Snacks.SN53.value),
    (base_id + 400 + 4522): (b'R021', Snacks.SN54.value),
    (base_id + 400 + 4523): (b'R021', Snacks.SN55.value),
    (base_id + 400 + 4524): (b'R021', Snacks.SN56.value),
    (base_id + 400 + 4525): (b'R021', Snacks.SN57.value),
    (base_id + 400 + 4526): (b'R021', Snacks.SN58.value),
    (base_id + 400 + 4527): (b'R021', Snacks.SN59.value),
    (base_id + 400 + 4528): (b'R021', Snacks.SN6.value),
    (base_id + 400 + 4529): (b'R021', Snacks.SN60.value),
    (base_id + 400 + 4530): (b'R021', Snacks.SN61.value),
    (base_id + 400 + 4531): (b'R021', Snacks.SN62.value),
    (base_id + 400 + 4532): (b'R021', Snacks.SN63.value),
    (base_id + 400 + 4533): (b'R021', Snacks.SN64.value),
    (base_id + 400 + 4534): (b'R021', Snacks.SN65.value),
    (base_id + 400 + 4535): (b'R021', Snacks.SN66.value),
    (base_id + 400 + 4536): (b'R021', Snacks.SN67.value),
    (base_id + 400 + 4537): (b'R021', Snacks.SN68.value),
    (base_id + 400 + 4538): (b'R021', Snacks.SN69.value),
    (base_id + 400 + 4539): (b'R021', Snacks.SN7.value),
    (base_id + 400 + 4540): (b'R021', Snacks.SN70.value),
    (base_id + 400 + 4541): (b'R021', Snacks.SN71.value),
    (base_id + 400 + 4542): (b'R021', Snacks.SN72.value),
    (base_id + 400 + 4543): (b'R021', Snacks.SN73.value),
    (base_id + 400 + 4544): (b'R021', Snacks.SN74.value),
    (base_id + 400 + 4545): (b'R021', Snacks.SN75.value),
    (base_id + 400 + 4546): (b'R021', Snacks.SN8.value),
    (base_id + 400 + 4547): (b'R021', Snacks.SN84.value),
    (base_id + 400 + 4548): (b'R021', Snacks.SN840.value),
    (base_id + 400 + 4549): (b'R021', Snacks.SN841.value),
    (base_id + 400 + 4550): (b'R021', Snacks.SN842.value),
    (base_id + 400 + 4551): (b'R021', Snacks.SN843.value),
    (base_id + 400 + 4552): (b'R021', Snacks.SN844.value),
    (base_id + 400 + 4553): (b'R021', Snacks.SN845.value),
    (base_id + 400 + 4554): (b'R021', Snacks.SN846.value),
    (base_id + 400 + 4555): (b'R021', Snacks.SN847.value),
    (base_id + 400 + 4556): (b'R021', Snacks.SN85.value),
    (base_id + 400 + 4557): (b'R021', Snacks.SN86.value),
    (base_id + 400 + 4558): (b'R021', Snacks.SN87.value),
    (base_id + 400 + 4559): (b'R021', Snacks.SN88.value),
    (base_id + 400 + 4560): (b'R021', Snacks.SN89.value),
    (base_id + 400 + 4561): (b'R021', Snacks.SN9.value),
    (base_id + 400 + 4562): (b'R021', Snacks.SN90.value),
    (base_id + 400 + 4563): (b'R021', Snacks.SN91.value),
    (base_id + 400 + 4564): (b'R021', Snacks.SN92.value),
    (base_id + 400 + 4565): (b'R021', Snacks.SN93.value),
    (base_id + 400 + 4566): (b'R021', Snacks.SN94.value),
    (base_id + 400 + 4567): (b'R021', Snacks.SN95.value),
    (base_id + 400 + 4568): (b'R021', Snacks.SN96.value),
    (base_id + 400 + 4569): (b'R021', Snacks.SN97.value),
    (base_id + 400 + 4570): (b'R021', Snacks.SN98.value),
    (base_id + 400 + 4571): (b'R021', Snacks.SN99.value),
    (base_id + 400 + 4572): (b'R021', Snacks.SNACKBOX.value),
    (base_id + 400 + 4573): (b'R021', Snacks.SNACKBOX2.value),

    (base_id + 400 + 4574): (b'S001', Snacks.EX__CLUE__SNACK__BOX__1.value),
    (base_id + 400 + 4575): (b'S001', Snacks.EX__CLUE__SNACK__BOX2.value),
    (base_id + 400 + 4576): (b'S001', Snacks.SB__UP__TOP1.value),
    (base_id + 400 + 4577): (b'S001', Snacks.SB__UP__TOP2.value),
    (base_id + 400 + 4578): (b'S001', Snacks.SS1.value),
    (base_id + 400 + 4579): (b'S001', Snacks.SS110.value),
    (base_id + 400 + 4580): (b'S001', Snacks.SS115.value),
    (base_id + 400 + 4581): (b'S001', Snacks.SS1150.value),
    (base_id + 400 + 4582): (b'S001', Snacks.SS1151.value),
    (base_id + 400 + 4583): (b'S001', Snacks.SS1154.value),
    (base_id + 400 + 4584): (b'S001', Snacks.SS1155.value),
    (base_id + 400 + 4585): (b'S001', Snacks.SS1156.value),
    (base_id + 400 + 4586): (b'S001', Snacks.SS116.value),
    (base_id + 400 + 4587): (b'S001', Snacks.SS117.value),
    (base_id + 400 + 4588): (b'S001', Snacks.SS1233.value),
    (base_id + 400 + 4589): (b'S001', Snacks.SS3.value),
    (base_id + 400 + 4590): (b'S001', Snacks.SS30.value),
    (base_id + 400 + 4591): (b'S001', Snacks.SS31.value),
    (base_id + 400 + 4592): (b'S001', Snacks.SS32.value),
    (base_id + 400 + 4593): (b'S001', Snacks.SS33.value),
    (base_id + 400 + 4594): (b'S001', Snacks.SS34.value),
    (base_id + 400 + 4595): (b'S001', Snacks.SS4.value),
    (base_id + 400 + 4596): (b'S001', Snacks.SS40.value),
    (base_id + 400 + 4597): (b'S001', Snacks.SS41.value),
    (base_id + 400 + 4598): (b'S001', Snacks.SS43.value),
    (base_id + 400 + 4599): (b'S001', Snacks.SS44.value),
    (base_id + 400 + 4600): (b'S001', Snacks.SS45.value),
    (base_id + 400 + 4601): (b'S001', Snacks.SS8.value),
    (base_id + 400 + 4602): (b'S001', Snacks.SS80.value),
    (base_id + 400 + 4603): (b'S001', Snacks.SS81.value),
    (base_id + 400 + 4604): (b'S001', Snacks.SS82.value),
    (base_id + 400 + 4605): (b'S001', Snacks.SS83.value),
    (base_id + 400 + 4606): (b'S001', Snacks.SS84.value),
    (base_id + 400 + 4607): (b'S001', Snacks.SS85.value),
    (base_id + 400 + 4608): (b'S001', Snacks.SS9.value),
    (base_id + 400 + 4609): (b'S001', Snacks.SS90.value),
    (base_id + 400 + 4610): (b'S001', Snacks.SS91.value),
    (base_id + 400 + 4611): (b'S001', Snacks.SS92.value),
    (base_id + 400 + 4612): (b'S001', Snacks.SS93.value),

    (base_id + 400 + 4613): (b'S002', Snacks.EX__CLUE__SNACK__BOX2.value),
    (base_id + 400 + 4614): (b'S002', Snacks.EX__CLUE__SNACK__BOX3.value),
    (base_id + 400 + 4615): (b'S002', Snacks.EX__CLUE__SNACK__BOX5.value),
    (base_id + 400 + 4616): (b'S002', Snacks.SNACK__1__MIL.value),
    (base_id + 400 + 4617): (b'S002', Snacks.SNACKBOX2.value),
    (base_id + 400 + 4618): (b'S002', Snacks.SNACKBOX3.value),
    (base_id + 400 + 4619): (b'S002', Snacks.SS2.value),
    (base_id + 400 + 4620): (b'S002', Snacks.SS26.value),
    (base_id + 400 + 4621): (b'S002', Snacks.SS261.value),
    (base_id + 400 + 4622): (b'S002', Snacks.SS263.value),
    (base_id + 400 + 4623): (b'S002', Snacks.SS265.value),
    (base_id + 400 + 4624): (b'S002', Snacks.SS267.value),
    (base_id + 400 + 4625): (b'S002', Snacks.SS268.value),
    (base_id + 400 + 4626): (b'S002', Snacks.SS2681.value),
    (base_id + 400 + 4627): (b'S002', Snacks.SS2683.value),
    (base_id + 400 + 4628): (b'S002', Snacks.SS2685.value),
    (base_id + 400 + 4629): (b'S002', Snacks.SS2687.value),
    (base_id + 400 + 4630): (b'S002', Snacks.SS3.value),
    (base_id + 400 + 4631): (b'S002', Snacks.SS4.value),
    (base_id + 400 + 4632): (b'S002', Snacks.SS5.value),
    (base_id + 400 + 4633): (b'S002', Snacks.SS7.value),
    (base_id + 400 + 4634): (b'S002', Snacks.SS8.value),
    (base_id + 400 + 4635): (b'S002', Snacks.SS9100.value),
    (base_id + 400 + 4636): (b'S002', Snacks.SS9101.value),
    (base_id + 400 + 4637): (b'S002', Snacks.SS9102.value),
    (base_id + 400 + 4638): (b'S002', Snacks.SS9103.value),
    (base_id + 400 + 4639): (b'S002', Snacks.SS9105.value),
    (base_id + 400 + 4640): (b'S002', Snacks.SS9106.value),
    (base_id + 400 + 4641): (b'S002', Snacks.SS9107.value),
    (base_id + 400 + 4642): (b'S002', Snacks.SS9108.value),

    (base_id + 400 + 4643): (b'S003', Snacks.SNACK11.value),
    (base_id + 400 + 4644): (b'S003', Snacks.SNACK1101.value),
    (base_id + 400 + 4645): (b'S003', Snacks.SNACK110101.value),
    (base_id + 400 + 4646): (b'S003', Snacks.SNACK110103.value),
    (base_id + 400 + 4647): (b'S003', Snacks.SNACK110105.value),
    (base_id + 400 + 4648): (b'S003', Snacks.SNACK110107.value),
    (base_id + 400 + 4649): (b'S003', Snacks.SNACK110109.value),
    (base_id + 400 + 4650): (b'S003', Snacks.SNACK1103.value),
    (base_id + 400 + 4651): (b'S003', Snacks.SNACK1105.value),
    (base_id + 400 + 4652): (b'S003', Snacks.SNACK1107.value),
    (base_id + 400 + 4653): (b'S003', Snacks.SNACK1109.value),
    (base_id + 400 + 4654): (b'S003', Snacks.SNACK111.value),
    (base_id + 400 + 4655): (b'S003', Snacks.SNACK113.value),
    (base_id + 400 + 4656): (b'S003', Snacks.SNACK115.value),
    (base_id + 400 + 4657): (b'S003', Snacks.SNACK117.value),
    (base_id + 400 + 4658): (b'S003', Snacks.SNACK119.value),
    (base_id + 400 + 4659): (b'S003', Snacks.SNACK13.value),
    (base_id + 400 + 4660): (b'S003', Snacks.SNACK15.value),
    (base_id + 400 + 4661): (b'S003', Snacks.SNACK17.value),
    (base_id + 400 + 4662): (b'S003', Snacks.SNACK19.value),
    (base_id + 400 + 4663): (b'S003', Snacks.SNACKBOX.value),
    (base_id + 400 + 4664): (b'S003', Snacks.SNACKBOX__2ND__LEVEL__1.value),
    (base_id + 400 + 4665): (b'S003', Snacks.SNACKBOX__2ND__LEVEL__2.value),
    (base_id + 400 + 4666): (b'S003', Snacks.SNACKBOX0.value),
    (base_id + 400 + 4667): (b'S003', Snacks.SNACKBOX00.value),
    (base_id + 400 + 4668): (b'S003', Snacks.SS10.value),
    (base_id + 400 + 4669): (b'S003', Snacks.SS11.value),
    (base_id + 400 + 4670): (b'S003', Snacks.SS110.value),
    (base_id + 400 + 4671): (b'S003', Snacks.SS1100.value),
    (base_id + 400 + 4672): (b'S003', Snacks.SS11000.value),
    (base_id + 400 + 4673): (b'S003', Snacks.SS110000.value),
    (base_id + 400 + 4674): (b'S003', Snacks.SS1100000.value),
    (base_id + 400 + 4675): (b'S003', Snacks.SS11000000.value),
    (base_id + 400 + 4676): (b'S003', Snacks.SS6.value),
    (base_id + 400 + 4677): (b'S003', Snacks.SS7.value),

    (base_id + 400 + 4678): (b'S004', Snacks.SNACK1.value),
    (base_id + 400 + 4679): (b'S004', Snacks.SNACK10.value),
    (base_id + 400 + 4680): (b'S004', Snacks.SNACK11.value),
    (base_id + 400 + 4681): (b'S004', Snacks.SNACK110.value),
    (base_id + 400 + 4682): (b'S004', Snacks.SNACK111.value),
    (base_id + 400 + 4683): (b'S004', Snacks.SNACK112.value),
    (base_id + 400 + 4684): (b'S004', Snacks.SNACK1120.value),
    (base_id + 400 + 4685): (b'S004', Snacks.SNACK1121.value),
    (base_id + 400 + 4686): (b'S004', Snacks.SNACK11210.value),
    (base_id + 400 + 4687): (b'S004', Snacks.SNACK11211.value),
    (base_id + 400 + 4688): (b'S004', Snacks.SNACK1122.value),
    (base_id + 400 + 4689): (b'S004', Snacks.SNACK1123.value),
    (base_id + 400 + 4690): (b'S004', Snacks.SNACK1124.value),
    (base_id + 400 + 4691): (b'S004', Snacks.SNACK1125.value),
    (base_id + 400 + 4692): (b'S004', Snacks.SNACK1126.value),
    (base_id + 400 + 4693): (b'S004', Snacks.SNACK1127.value),
    (base_id + 400 + 4694): (b'S004', Snacks.SNACK1128.value),
    (base_id + 400 + 4695): (b'S004', Snacks.SNACK1129.value),
    (base_id + 400 + 4696): (b'S004', Snacks.SNACK114.value),
    (base_id + 400 + 4697): (b'S004', Snacks.SNACK115.value),
    (base_id + 400 + 4698): (b'S004', Snacks.SNACK116.value),
    (base_id + 400 + 4699): (b'S004', Snacks.SNACK117.value),
    (base_id + 400 + 4700): (b'S004', Snacks.SNACK118.value),
    (base_id + 400 + 4701): (b'S004', Snacks.SNACK119.value),
    (base_id + 400 + 4702): (b'S004', Snacks.SNACK12.value),
    (base_id + 400 + 4703): (b'S004', Snacks.SNACK120.value),
    (base_id + 400 + 4704): (b'S004', Snacks.SNACK121.value),
    (base_id + 400 + 4705): (b'S004', Snacks.SNACK122.value),
    (base_id + 400 + 4706): (b'S004', Snacks.SNACK123.value),
    (base_id + 400 + 4707): (b'S004', Snacks.SNACK124.value),
    (base_id + 400 + 4708): (b'S004', Snacks.SNACK125.value),
    (base_id + 400 + 4709): (b'S004', Snacks.SNACK1271.value),
    (base_id + 400 + 4710): (b'S004', Snacks.SNACK12710.value),
    (base_id + 400 + 4711): (b'S004', Snacks.SNACK1272.value),
    (base_id + 400 + 4712): (b'S004', Snacks.SNACK1273.value),
    (base_id + 400 + 4713): (b'S004', Snacks.SNACK1274.value),
    (base_id + 400 + 4714): (b'S004', Snacks.SNACK1275.value),
    (base_id + 400 + 4715): (b'S004', Snacks.SNACK1276.value),
    (base_id + 400 + 4716): (b'S004', Snacks.SNACK1277.value),
    (base_id + 400 + 4717): (b'S004', Snacks.SNACK1278.value),
    (base_id + 400 + 4718): (b'S004', Snacks.SNACK1279.value),
    (base_id + 400 + 4719): (b'S004', Snacks.SNACK13.value),
    (base_id + 400 + 4720): (b'S004', Snacks.SNACK14.value),
    (base_id + 400 + 4721): (b'S004', Snacks.SNACK15.value),
    (base_id + 400 + 4722): (b'S004', Snacks.SNACK16.value),
    (base_id + 400 + 4723): (b'S004', Snacks.SNACK17.value),
    (base_id + 400 + 4724): (b'S004', Snacks.SNACK18.value),
    (base_id + 400 + 4725): (b'S004', Snacks.SNACK19.value),
    (base_id + 400 + 4726): (b'S004', Snacks.SS1.value),
    (base_id + 400 + 4727): (b'S004', Snacks.SS10.value),
    (base_id + 400 + 4728): (b'S004', Snacks.SS11.value),
    (base_id + 400 + 4729): (b'S004', Snacks.SS12.value),
    (base_id + 400 + 4730): (b'S004', Snacks.SS13.value),
    (base_id + 400 + 4731): (b'S004', Snacks.SS14.value),
    (base_id + 400 + 4732): (b'S004', Snacks.SS15.value),
    (base_id + 400 + 4733): (b'S004', Snacks.SS16.value),
    (base_id + 400 + 4734): (b'S004', Snacks.SS2.value),
    (base_id + 400 + 4735): (b'S004', Snacks.SS3.value),
    (base_id + 400 + 4736): (b'S004', Snacks.SS4.value),
    (base_id + 400 + 4737): (b'S004', Snacks.SS5.value),
    (base_id + 400 + 4738): (b'S004', Snacks.SS6.value),
    (base_id + 400 + 4739): (b'S004', Snacks.SS7.value),
    (base_id + 400 + 4740): (b'S004', Snacks.SS8.value),
    (base_id + 400 + 4741): (b'S004', Snacks.SS9.value),

    (base_id + 400 + 4742): (b'W020', Snacks.SS01.value),
    (base_id + 400 + 4743): (b'W020', Snacks.SS02.value),
    (base_id + 400 + 4744): (b'W020', Snacks.SS04.value),
    (base_id + 400 + 4745): (b'W020', Snacks.SS06.value),
    (base_id + 400 + 4746): (b'W020', Snacks.SS0610.value),
    (base_id + 400 + 4747): (b'W020', Snacks.SS0611.value),
    (base_id + 400 + 4748): (b'W020', Snacks.SS06110.value),
    (base_id + 400 + 4749): (b'W020', Snacks.SS06111.value),
    (base_id + 400 + 4750): (b'W020', Snacks.SS06112.value),
    (base_id + 400 + 4751): (b'W020', Snacks.SS061130.value),
    (base_id + 400 + 4752): (b'W020', Snacks.SS061131.value),
    (base_id + 400 + 4753): (b'W020', Snacks.SS061132.value),
    (base_id + 400 + 4754): (b'W020', Snacks.SS061133.value),
    (base_id + 400 + 4755): (b'W020', Snacks.SS0611330.value),
    (base_id + 400 + 4756): (b'W020', Snacks.SS06113310.value),
    (base_id + 400 + 4757): (b'W020', Snacks.SS061133100.value),
    (base_id + 400 + 4758): (b'W020', Snacks.SS0611331010.value),
    (base_id + 400 + 4759): (b'W020', Snacks.SS0611331011.value),
    (base_id + 400 + 4760): (b'W020', Snacks.SS0611331012.value),
    (base_id + 400 + 4761): (b'W020', Snacks.SS0611331013.value),
    (base_id + 400 + 4762): (b'W020', Snacks.SS06113310130.value),
    (base_id + 400 + 4763): (b'W020', Snacks.SS0612.value),
    (base_id + 400 + 4764): (b'W020', Snacks.SS0614.value),
    (base_id + 400 + 4765): (b'W020', Snacks.SS0615.value),
    (base_id + 400 + 4766): (b'W020', Snacks.SS06150.value),
    (base_id + 400 + 4767): (b'W020', Snacks.SS06151.value),
    (base_id + 400 + 4768): (b'W020', Snacks.SS06152.value),
    (base_id + 400 + 4769): (b'W020', Snacks.SS06153.value),
    (base_id + 400 + 4770): (b'W020', Snacks.SS061530.value),
    (base_id + 400 + 4771): (b'W020', Snacks.SS061531.value),
    (base_id + 400 + 4772): (b'W020', Snacks.SS061532.value),
    (base_id + 400 + 4773): (b'W020', Snacks.SS061533.value),
    (base_id + 400 + 4774): (b'W020', Snacks.SS064.value),
    (base_id + 400 + 4775): (b'W020', Snacks.SS065.value),
    (base_id + 400 + 4776): (b'W020', Snacks.SS066.value),
    (base_id + 400 + 4777): (b'W020', Snacks.SS067.value),
    (base_id + 400 + 4778): (b'W020', Snacks.SS068.value),
    (base_id + 400 + 4779): (b'W020', Snacks.SS069.value),
    (base_id + 400 + 4780): (b'W020', Snacks.SS07.value),
    (base_id + 400 + 4781): (b'W020', Snacks.SS08.value),
    (base_id + 400 + 4782): (b'W020', Snacks.SS09.value),
    (base_id + 400 + 4783): (b'W020', Snacks.SS10.value),
    (base_id + 400 + 4784): (b'W020', Snacks.SS20.value),
    (base_id + 400 + 4785): (b'W020', Snacks.SS30.value),
    (base_id + 400 + 4786): (b'W020', Snacks.SS40.value),
    (base_id + 400 + 4787): (b'W020', Snacks.SS43.value),
    (base_id + 400 + 4788): (b'W020', Snacks.SS50.value),
    (base_id + 400 + 4789): (b'W020', Snacks.SS51.value),
    (base_id + 400 + 4790): (b'W020', Snacks.SS52.value),
    (base_id + 400 + 4791): (b'W020', Snacks.SS53.value),
    (base_id + 400 + 4792): (b'W020', Snacks.SS55.value),
    (base_id + 400 + 4793): (b'W020', Snacks.SS58.value),
    (base_id + 400 + 4794): (b'W020', Snacks.SS60.value),
    (base_id + 400 + 4795): (b'W020', Snacks.SS61.value),
    (base_id + 400 + 4796): (b'W020', Snacks.SS62.value),
    (base_id + 400 + 4797): (b'W020', Snacks.SS63.value),
    (base_id + 400 + 4798): (b'W020', Snacks.SS64.value),
    (base_id + 400 + 4799): (b'W020', Snacks.SS65.value),
    (base_id + 400 + 4800): (b'W020', Snacks.SS650.value),
    (base_id + 400 + 4801): (b'W020', Snacks.SS651.value),
    (base_id + 400 + 4802): (b'W020', Snacks.SS652.value),
    (base_id + 400 + 4803): (b'W020', Snacks.SS67.value),
    (base_id + 400 + 4804): (b'W020', Snacks.SS68.value),
    (base_id + 400 + 4805): (b'W020', Snacks.SS69.value),
    (base_id + 400 + 4806): (b'W020', Snacks.SS690.value),
    (base_id + 400 + 4807): (b'W020', Snacks.SS691.value),
    (base_id + 400 + 4808): (b'W020', Snacks.SS692.value),
    (base_id + 400 + 4809): (b'W020', Snacks.SS70.value),
    (base_id + 400 + 4810): (b'W020', Snacks.SS730.value),
    (base_id + 400 + 4811): (b'W020', Snacks.SS732.value),
    (base_id + 400 + 4812): (b'W020', Snacks.SS74.value),
    (base_id + 400 + 4813): (b'W020', Snacks.SS78.value),
    (base_id + 400 + 4814): (b'W020', Snacks.SS80.value),
    (base_id + 400 + 4815): (b'W020', Snacks.SS82.value),
    (base_id + 400 + 4816): (b'W020', Snacks.SS910.value),
    (base_id + 400 + 4817): (b'W020', Snacks.SS911.value),
    (base_id + 400 + 4818): (b'W020', Snacks.SS912.value),
    (base_id + 400 + 4819): (b'W020', Snacks.SS913.value),
    (base_id + 400 + 4820): (b'W020', Snacks.SS914.value),
    (base_id + 400 + 4821): (b'W020', Snacks.SSBOX87.value),

    (base_id + 400 + 4822): (b'W021', Snacks.SS02A.value),
    (base_id + 400 + 4823): (b'W021', Snacks.SS02B.value),
    (base_id + 400 + 4824): (b'W021', Snacks.SS03A.value),
    (base_id + 400 + 4825): (b'W021', Snacks.SS03B.value),
    (base_id + 400 + 4826): (b'W021', Snacks.SS04A.value),
    (base_id + 400 + 4827): (b'W021', Snacks.SS04B.value),
    (base_id + 400 + 4828): (b'W021', Snacks.SS100.value),
    (base_id + 400 + 4829): (b'W021', Snacks.SS101.value),
    (base_id + 400 + 4830): (b'W021', Snacks.SS102.value),
    (base_id + 400 + 4831): (b'W021', Snacks.SS103.value),
    (base_id + 400 + 4832): (b'W021', Snacks.SS104.value),
    (base_id + 400 + 4833): (b'W021', Snacks.SS110.value),
    (base_id + 400 + 4834): (b'W021', Snacks.SS111.value),
    (base_id + 400 + 4835): (b'W021', Snacks.SS112.value),
    (base_id + 400 + 4836): (b'W021', Snacks.SS113.value),
    (base_id + 400 + 4837): (b'W021', Snacks.SS114.value),
    (base_id + 400 + 4838): (b'W021', Snacks.SS120.value),
    (base_id + 400 + 4839): (b'W021', Snacks.SS121.value),
    (base_id + 400 + 4840): (b'W021', Snacks.SS122.value),
    (base_id + 400 + 4841): (b'W021', Snacks.SS123.value),
    (base_id + 400 + 4842): (b'W021', Snacks.SS124.value),
    (base_id + 400 + 4843): (b'W021', Snacks.SS140.value),
    (base_id + 400 + 4844): (b'W021', Snacks.SS141.value),
    (base_id + 400 + 4845): (b'W021', Snacks.SS142.value),
    (base_id + 400 + 4846): (b'W021', Snacks.SS143.value),
    (base_id + 400 + 4847): (b'W021', Snacks.SS144.value),
    (base_id + 400 + 4848): (b'W021', Snacks.SS150.value),
    (base_id + 400 + 4849): (b'W021', Snacks.SS151.value),
    (base_id + 400 + 4850): (b'W021', Snacks.SS152.value),
    (base_id + 400 + 4851): (b'W021', Snacks.SS153.value),
    (base_id + 400 + 4852): (b'W021', Snacks.SS154.value),
    (base_id + 400 + 4853): (b'W021', Snacks.SS160.value),
    (base_id + 400 + 4854): (b'W021', Snacks.SS161.value),
    (base_id + 400 + 4855): (b'W021', Snacks.SS162.value),
    (base_id + 400 + 4856): (b'W021', Snacks.SS163.value),
    (base_id + 400 + 4857): (b'W021', Snacks.SS164.value),
    (base_id + 400 + 4858): (b'W021', Snacks.SS170.value),
    (base_id + 400 + 4859): (b'W021', Snacks.SS171.value),
    (base_id + 400 + 4860): (b'W021', Snacks.SS172.value),
    (base_id + 400 + 4861): (b'W021', Snacks.SS173.value),
    (base_id + 400 + 4862): (b'W021', Snacks.SS174.value),
    (base_id + 400 + 4863): (b'W021', Snacks.SS190.value),
    (base_id + 400 + 4864): (b'W021', Snacks.SS191.value),
    (base_id + 400 + 4865): (b'W021', Snacks.SS192.value),
    (base_id + 400 + 4866): (b'W021', Snacks.SS193.value),
    (base_id + 400 + 4867): (b'W021', Snacks.SS194.value),
    (base_id + 400 + 4868): (b'W021', Snacks.SS200.value),
    (base_id + 400 + 4869): (b'W021', Snacks.SS201.value),
    (base_id + 400 + 4870): (b'W021', Snacks.SS202.value),
    (base_id + 400 + 4871): (b'W021', Snacks.SS203.value),
    (base_id + 400 + 4872): (b'W021', Snacks.SS204.value),
    (base_id + 400 + 4873): (b'W021', Snacks.SS210.value),
    (base_id + 400 + 4874): (b'W021', Snacks.SS211.value),
    (base_id + 400 + 4875): (b'W021', Snacks.SS212.value),
    (base_id + 400 + 4876): (b'W021', Snacks.SS213.value),
    (base_id + 400 + 4877): (b'W021', Snacks.SS214.value),
    (base_id + 400 + 4878): (b'W021', Snacks.SS220.value),
    (base_id + 400 + 4879): (b'W021', Snacks.SS221.value),
    (base_id + 400 + 4880): (b'W021', Snacks.SS222.value),
    (base_id + 400 + 4881): (b'W021', Snacks.SS223.value),
    (base_id + 400 + 4882): (b'W021', Snacks.SS224.value),
    (base_id + 400 + 4883): (b'W021', Snacks.SS24.value),
    (base_id + 400 + 4884): (b'W021', Snacks.SS240.value),
    (base_id + 400 + 4885): (b'W021', Snacks.SS241.value),
    (base_id + 400 + 4886): (b'W021', Snacks.SS25.value),
    (base_id + 400 + 4887): (b'W021', Snacks.SS250.value),
    (base_id + 400 + 4888): (b'W021', Snacks.SS251.value),
    (base_id + 400 + 4889): (b'W021', Snacks.SS26.value),
    (base_id + 400 + 4890): (b'W021', Snacks.SS260.value),
    (base_id + 400 + 4891): (b'W021', Snacks.SS2600.value),
    (base_id + 400 + 4892): (b'W021', Snacks.SS2601.value),
    (base_id + 400 + 4893): (b'W021', Snacks.SS2602.value),
    (base_id + 400 + 4894): (b'W021', Snacks.SS2603.value),
    (base_id + 400 + 4895): (b'W021', Snacks.SS2604.value),
    (base_id + 400 + 4896): (b'W021', Snacks.SS2605.value),
    (base_id + 400 + 4897): (b'W021', Snacks.SS2606.value),
    (base_id + 400 + 4898): (b'W021', Snacks.SS2607.value),
    (base_id + 400 + 4899): (b'W021', Snacks.SSBOX01.value),
    (base_id + 400 + 4900): (b'W021', Snacks.SSBOX02.value),
    (base_id + 400 + 4901): (b'W021', Snacks.SSBOX03.value),
    (base_id + 400 + 4902): (b'W021', Snacks.SSBOX04.value),
    (base_id + 400 + 4903): (b'W021', Snacks.SSBOX05.value),
    (base_id + 400 + 4904): (b'W021', Snacks.SSBOX06.value),
    (base_id + 400 + 4905): (b'W021', Snacks.SSBOX07.value),

    (base_id + 400 + 4906): (b'W022', Snacks.SS010.value),
    (base_id + 400 + 4907): (b'W022', Snacks.SS011.value),
    (base_id + 400 + 4908): (b'W022', Snacks.SS012.value),
    (base_id + 400 + 4909): (b'W022', Snacks.SS020.value),
    (base_id + 400 + 4910): (b'W022', Snacks.SS021.value),
    (base_id + 400 + 4911): (b'W022', Snacks.SS022.value),
    (base_id + 400 + 4912): (b'W022', Snacks.SS03.value),
    (base_id + 400 + 4913): (b'W022', Snacks.SS030.value),
    (base_id + 400 + 4914): (b'W022', Snacks.SS04.value),
    (base_id + 400 + 4915): (b'W022', Snacks.SS040.value),
    (base_id + 400 + 4916): (b'W022', Snacks.SS041.value),
    (base_id + 400 + 4917): (b'W022', Snacks.SS042.value),
    (base_id + 400 + 4918): (b'W022', Snacks.SS05.value),
    (base_id + 400 + 4919): (b'W022', Snacks.SS050.value),
    (base_id + 400 + 4920): (b'W022', Snacks.SS051.value),
    (base_id + 400 + 4921): (b'W022', Snacks.SS07.value),
    (base_id + 400 + 4922): (b'W022', Snacks.SS070.value),
    (base_id + 400 + 4923): (b'W022', Snacks.SS071.value),
    (base_id + 400 + 4924): (b'W022', Snacks.SS072.value),
    (base_id + 400 + 4925): (b'W022', Snacks.SS08.value),
    (base_id + 400 + 4926): (b'W022', Snacks.SS080.value),
    (base_id + 400 + 4927): (b'W022', Snacks.SS081.value),
    (base_id + 400 + 4928): (b'W022', Snacks.SS09.value),
    (base_id + 400 + 4929): (b'W022', Snacks.SS090.value),
    (base_id + 400 + 4930): (b'W022', Snacks.SS091.value),
    (base_id + 400 + 4931): (b'W022', Snacks.SS10.value),
    (base_id + 400 + 4932): (b'W022', Snacks.SS100.value),
    (base_id + 400 + 4933): (b'W022', Snacks.SS101.value),
    (base_id + 400 + 4934): (b'W022', Snacks.SS102.value),
    (base_id + 400 + 4935): (b'W022', Snacks.SS16.value),
    (base_id + 400 + 4936): (b'W022', Snacks.SS17.value),
    (base_id + 400 + 4937): (b'W022', Snacks.SS18.value),
    (base_id + 400 + 4938): (b'W022', Snacks.SS20.value),
    (base_id + 400 + 4939): (b'W022', Snacks.SS200.value),
    (base_id + 400 + 4940): (b'W022', Snacks.SS201.value),
    (base_id + 400 + 4941): (b'W022', Snacks.SS21.value),
    (base_id + 400 + 4942): (b'W022', Snacks.SS210.value),
    (base_id + 400 + 4943): (b'W022', Snacks.SS211.value),
    (base_id + 400 + 4944): (b'W022', Snacks.SS22.value),
    (base_id + 400 + 4945): (b'W022', Snacks.SS220.value),
    (base_id + 400 + 4946): (b'W022', Snacks.SS221.value),
    (base_id + 400 + 4947): (b'W022', Snacks.SS23.value),
    (base_id + 400 + 4948): (b'W022', Snacks.SS230.value),
    (base_id + 400 + 4949): (b'W022', Snacks.SS231.value),
    (base_id + 400 + 4950): (b'W022', Snacks.SS24.value),
    (base_id + 400 + 4951): (b'W022', Snacks.SS241.value),
    (base_id + 400 + 4952): (b'W022', Snacks.SS25.value),
    (base_id + 400 + 4953): (b'W022', Snacks.SS250.value),
    (base_id + 400 + 4954): (b'W022', Snacks.SS251.value),
    (base_id + 400 + 4955): (b'W022', Snacks.SS27.value),
    (base_id + 400 + 4956): (b'W022', Snacks.SS271.value),
    (base_id + 400 + 4957): (b'W022', Snacks.SS272.value),
    (base_id + 400 + 4958): (b'W022', Snacks.SS28.value),
    (base_id + 400 + 4959): (b'W022', Snacks.SS281.value),
    (base_id + 400 + 4960): (b'W022', Snacks.SS31.value),
    (base_id + 400 + 4961): (b'W022', Snacks.SS32.value),
    (base_id + 400 + 4962): (b'W022', Snacks.SS33.value),
    (base_id + 400 + 4963): (b'W022', Snacks.SSBOX12.value),
    (base_id + 400 + 4964): (b'W022', Snacks.SSBOX13.value),
    (base_id + 400 + 4965): (b'W022', Snacks.SSBOX14.value),

    (base_id + 400 + 4966): (b'W023', Snacks.SS01.value),
    (base_id + 400 + 4967): (b'W023', Snacks.SS02.value),
    (base_id + 400 + 4968): (b'W023', Snacks.SS0210.value),
    (base_id + 400 + 4969): (b'W023', Snacks.SS0211.value),
    (base_id + 400 + 4970): (b'W023', Snacks.SS03.value),
    (base_id + 400 + 4971): (b'W023', Snacks.SS031.value),
    (base_id + 400 + 4972): (b'W023', Snacks.SS033.value),
    (base_id + 400 + 4973): (b'W023', Snacks.SS035.value),
    (base_id + 400 + 4974): (b'W023', Snacks.SS037.value),
    (base_id + 400 + 4975): (b'W023', Snacks.SS04.value),
    (base_id + 400 + 4976): (b'W023', Snacks.SS041.value),
    (base_id + 400 + 4977): (b'W023', Snacks.SS043.value),
    (base_id + 400 + 4978): (b'W023', Snacks.SS045.value),
    (base_id + 400 + 4979): (b'W023', Snacks.SS047.value),
    (base_id + 400 + 4980): (b'W023', Snacks.SS05.value),
    (base_id + 400 + 4981): (b'W023', Snacks.SS06.value),
    (base_id + 400 + 4982): (b'W023', Snacks.SS07.value),
    (base_id + 400 + 4983): (b'W023', Snacks.SS10.value),
    (base_id + 400 + 4984): (b'W023', Snacks.SS100.value),
    (base_id + 400 + 4985): (b'W023', Snacks.SS1010.value),
    (base_id + 400 + 4986): (b'W023', Snacks.SS104.value),
    (base_id + 400 + 4987): (b'W023', Snacks.SS106.value),
    (base_id + 400 + 4988): (b'W023', Snacks.SS108.value),
    (base_id + 400 + 4989): (b'W023', Snacks.SS11.value),
    (base_id + 400 + 4990): (b'W023', Snacks.SS12.value),
    (base_id + 400 + 4991): (b'W023', Snacks.SS120.value),
    (base_id + 400 + 4992): (b'W023', Snacks.SS1210.value),
    (base_id + 400 + 4993): (b'W023', Snacks.SS124.value),
    (base_id + 400 + 4994): (b'W023', Snacks.SS126.value),
    (base_id + 400 + 4995): (b'W023', Snacks.SS128.value),
    (base_id + 400 + 4996): (b'W023', Snacks.SS13.value),
    (base_id + 400 + 4997): (b'W023', Snacks.SS14.value),
    (base_id + 400 + 4998): (b'W023', Snacks.SS141.value),
    (base_id + 400 + 4999): (b'W023', Snacks.SS143.value),
    (base_id + 400 + 5000): (b'W023', Snacks.SS145.value),
    (base_id + 400 + 5001): (b'W023', Snacks.SS147.value),
    (base_id + 400 + 5002): (b'W023', Snacks.SS15.value),
    (base_id + 400 + 5003): (b'W023', Snacks.SS151.value),
    (base_id + 400 + 5004): (b'W023', Snacks.SS153.value),
    (base_id + 400 + 5005): (b'W023', Snacks.SS155.value),
    (base_id + 400 + 5006): (b'W023', Snacks.SS157.value),
    (base_id + 400 + 5007): (b'W023', Snacks.SS16.value),
    (base_id + 400 + 5008): (b'W023', Snacks.SS161.value),
    (base_id + 400 + 5009): (b'W023', Snacks.SS163.value),
    (base_id + 400 + 5010): (b'W023', Snacks.SS165.value),
    (base_id + 400 + 5011): (b'W023', Snacks.SS167.value),
    (base_id + 400 + 5012): (b'W023', Snacks.SS17.value),
    (base_id + 400 + 5013): (b'W023', Snacks.SS171.value),
    (base_id + 400 + 5014): (b'W023', Snacks.SS173.value),
    (base_id + 400 + 5015): (b'W023', Snacks.SS175.value),
    (base_id + 400 + 5016): (b'W023', Snacks.SS177.value),
    (base_id + 400 + 5017): (b'W023', Snacks.SS23.value),
    (base_id + 400 + 5018): (b'W023', Snacks.SS231.value),
    (base_id + 400 + 5019): (b'W023', Snacks.SS233.value),
    (base_id + 400 + 5020): (b'W023', Snacks.SS235.value),
    (base_id + 400 + 5021): (b'W023', Snacks.SS237.value),
    (base_id + 400 + 5022): (b'W023', Snacks.SS24.value),
    (base_id + 400 + 5023): (b'W023', Snacks.SS241.value),
    (base_id + 400 + 5024): (b'W023', Snacks.SS243.value),
    (base_id + 400 + 5025): (b'W023', Snacks.SS245.value),
    (base_id + 400 + 5026): (b'W023', Snacks.SS247.value),
    (base_id + 400 + 5027): (b'W023', Snacks.SS29300.value),
    (base_id + 400 + 5028): (b'W023', Snacks.SS293020.value),
    (base_id + 400 + 5029): (b'W023', Snacks.SS2930210.value),
    (base_id + 400 + 5030): (b'W023', Snacks.SS29302105.value),
    (base_id + 400 + 5031): (b'W023', Snacks.SSBOX05.value),
    (base_id + 400 + 5032): (b'W023', Snacks.SSBOX06.value),
    (base_id + 400 + 5033): (b'W023', Snacks.SSBOX18.value),
    (base_id + 400 + 5034): (b'W023', Snacks.SSBOX25.value),
    (base_id + 400 + 5035): (b'W023', Snacks.SSBOX26.value),
    (base_id + 400 + 5036): (b'W023', Snacks.SSBOX27.value),
    (base_id + 400 + 5037): (b'W023', Snacks.SSBOX28.value),

    (base_id + 400 + 5038): (b'W025', Snacks.SS010.value),
    (base_id + 400 + 5039): (b'W025', Snacks.SS0100.value),
    (base_id + 400 + 5040): (b'W025', Snacks.SS0101.value),
    (base_id + 400 + 5041): (b'W025', Snacks.SS0102.value),
    (base_id + 400 + 5042): (b'W025', Snacks.SS0103.value),
    (base_id + 400 + 5043): (b'W025', Snacks.SS0104.value),
    (base_id + 400 + 5044): (b'W025', Snacks.SS011.value),
    (base_id + 400 + 5045): (b'W025', Snacks.SS02.value),
    (base_id + 400 + 5046): (b'W025', Snacks.SS020.value),
    (base_id + 400 + 5047): (b'W025', Snacks.SS021.value),
    (base_id + 400 + 5048): (b'W025', Snacks.SS022.value),
    (base_id + 400 + 5049): (b'W025', Snacks.SS023.value),
    (base_id + 400 + 5050): (b'W025', Snacks.SS024.value),
    (base_id + 400 + 5051): (b'W025', Snacks.SS0410.value),
    (base_id + 400 + 5052): (b'W025', Snacks.SS0411.value),
    (base_id + 400 + 5053): (b'W025', Snacks.SS0412.value),
    (base_id + 400 + 5054): (b'W025', Snacks.SS048.value),
    (base_id + 400 + 5055): (b'W025', Snacks.SS049.value),
    (base_id + 400 + 5056): (b'W025', Snacks.SS05.value),
    (base_id + 400 + 5057): (b'W025', Snacks.SS051.value),
    (base_id + 400 + 5058): (b'W025', Snacks.SS055.value),
    (base_id + 400 + 5059): (b'W025', Snacks.SS057.value),
    (base_id + 400 + 5060): (b'W025', Snacks.SS058.value),
    (base_id + 400 + 5061): (b'W025', Snacks.SS06.value),
    (base_id + 400 + 5062): (b'W025', Snacks.SS061.value),
    (base_id + 400 + 5063): (b'W025', Snacks.SS063.value),
    (base_id + 400 + 5064): (b'W025', Snacks.SS065.value),
    (base_id + 400 + 5065): (b'W025', Snacks.SS067.value),
    (base_id + 400 + 5066): (b'W025', Snacks.SS068.value),
    (base_id + 400 + 5067): (b'W025', Snacks.SS07.value),
    (base_id + 400 + 5068): (b'W025', Snacks.SS071.value),
    (base_id + 400 + 5069): (b'W025', Snacks.SS0711.value),
    (base_id + 400 + 5070): (b'W025', Snacks.SS0713.value),
    (base_id + 400 + 5071): (b'W025', Snacks.SS0715.value),
    (base_id + 400 + 5072): (b'W025', Snacks.SS0717.value),
    (base_id + 400 + 5073): (b'W025', Snacks.SS0719.value),
    (base_id + 400 + 5074): (b'W025', Snacks.SS0721.value),
    (base_id + 400 + 5075): (b'W025', Snacks.SS0723.value),
    (base_id + 400 + 5076): (b'W025', Snacks.SS0725.value),
    (base_id + 400 + 5077): (b'W025', Snacks.SS073.value),
    (base_id + 400 + 5078): (b'W025', Snacks.SS075.value),
    (base_id + 400 + 5079): (b'W025', Snacks.SS077.value),
    (base_id + 400 + 5080): (b'W025', Snacks.SS079.value),
    (base_id + 400 + 5081): (b'W025', Snacks.SS08.value),
    (base_id + 400 + 5082): (b'W025', Snacks.SS080.value),
    (base_id + 400 + 5083): (b'W025', Snacks.SS081.value),
    (base_id + 400 + 5084): (b'W025', Snacks.SS09.value),
    (base_id + 400 + 5085): (b'W025', Snacks.SS090.value),
    (base_id + 400 + 5086): (b'W025', Snacks.SS091.value),
    (base_id + 400 + 5087): (b'W025', Snacks.SS092.value),
    (base_id + 400 + 5088): (b'W025', Snacks.SS093.value),
    # (base_id + 400 + 5089): (b'W025', Snacks.SS10.value), This is a Sandwich
    (base_id + 400 + 5090): (b'W025', Snacks.SS100.value),
    (base_id + 400 + 5091): (b'W025', Snacks.SS101.value),
    (base_id + 400 + 5092): (b'W025', Snacks.SS104.value),
    (base_id + 400 + 5093): (b'W025', Snacks.SS105.value),
    (base_id + 400 + 5094): (b'W025', Snacks.SS106.value),
    (base_id + 400 + 5095): (b'W025', Snacks.SS107.value),
    (base_id + 400 + 5096): (b'W025', Snacks.SS110.value),
    # (base_id + 400 + 5097): (b'W025', Snacks.SS111.value), This is unfortunately also a Sandwich
    (base_id + 400 + 5098): (b'W025', Snacks.SS112.value),
    (base_id + 400 + 5099): (b'W025', Snacks.SS113.value),
    (base_id + 400 + 5100): (b'W025', Snacks.SS114.value),
    (base_id + 400 + 5101): (b'W025', Snacks.SS115.value),
    (base_id + 400 + 5102): (b'W025', Snacks.SS12.value),
    (base_id + 400 + 5103): (b'W025', Snacks.SS120.value),
    (base_id + 400 + 5104): (b'W025', Snacks.SS121.value),
    (base_id + 400 + 5105): (b'W025', Snacks.SS122.value),
    (base_id + 400 + 5106): (b'W025', Snacks.SS124.value),
    (base_id + 400 + 5107): (b'W025', Snacks.SS125.value),
    (base_id + 400 + 5108): (b'W025', Snacks.SS126.value),
    (base_id + 400 + 5109): (b'W025', Snacks.SS13.value),
    (base_id + 400 + 5110): (b'W025', Snacks.SS130.value),
    (base_id + 400 + 5111): (b'W025', Snacks.SS131.value),
    (base_id + 400 + 5112): (b'W025', Snacks.SS132.value),
    (base_id + 400 + 5113): (b'W025', Snacks.SS133.value),
    (base_id + 400 + 5114): (b'W025', Snacks.SS134.value),
    (base_id + 400 + 5115): (b'W025', Snacks.SS135.value),
    (base_id + 400 + 5116): (b'W025', Snacks.SS136.value),
    (base_id + 400 + 5117): (b'W025', Snacks.SS14.value),
    (base_id + 400 + 5118): (b'W025', Snacks.SS140.value),
    (base_id + 400 + 5119): (b'W025', Snacks.SS141.value),
    (base_id + 400 + 5120): (b'W025', Snacks.SS142.value),
    (base_id + 400 + 5121): (b'W025', Snacks.SS143.value),
    (base_id + 400 + 5122): (b'W025', Snacks.SS15.value),
    (base_id + 400 + 5123): (b'W025', Snacks.SS150.value),
    (base_id + 400 + 5124): (b'W025', Snacks.SS1500.value),
    (base_id + 400 + 5125): (b'W025', Snacks.SS151.value),
    (base_id + 400 + 5126): (b'W025', Snacks.SS1510.value),
    (base_id + 400 + 5127): (b'W025', Snacks.SS152.value),
    (base_id + 400 + 5128): (b'W025', Snacks.SS1520.value),
    (base_id + 400 + 5129): (b'W025', Snacks.SS153.value),
    (base_id + 400 + 5130): (b'W025', Snacks.SS1530.value),
    (base_id + 400 + 5131): (b'W025', Snacks.SS154.value),
    (base_id + 400 + 5132): (b'W025', Snacks.SS1540.value),
    (base_id + 400 + 5133): (b'W025', Snacks.SS155.value),
    (base_id + 400 + 5134): (b'W025', Snacks.SSBOX01.value),
    (base_id + 400 + 5135): (b'W025', Snacks.SSBOX02.value),
    (base_id + 400 + 5136): (b'W025', Snacks.SSBOX03.value),
    (base_id + 400 + 5137): (b'W025', Snacks.SSBOX04.value),
    (base_id + 400 + 5138): (b'W025', Snacks.SSBOX05.value),
    (base_id + 400 + 5139): (b'W025', Snacks.SSBOX06.value),
    (base_id + 400 + 5140): (b'W025', Snacks.SSBOX07.value),
    (base_id + 400 + 5141): (b'W025', Snacks.SSBOX08.value),
    (base_id + 400 + 5142): (b'W025', Snacks.SSBOX09.value),
    (base_id + 400 + 5143): (b'W025', Snacks.SSBOX10.value),

    (base_id + 400 + 5144): (b'W026', Snacks.REEF_SS01.value),
    (base_id + 400 + 5145): (b'W026', Snacks.REEF_SS02.value),
    (base_id + 400 + 5146): (b'W026', Snacks.REEF_SS03.value),
    (base_id + 400 + 5147): (b'W026', Snacks.REEF_SS04.value),
    (base_id + 400 + 5148): (b'W026', Snacks.REEF_SS05.value),
    (base_id + 400 + 5149): (b'W026', Snacks.REEF_SS06.value),
    (base_id + 400 + 5150): (b'W026', Snacks.REEF_SS07.value),
    (base_id + 400 + 5151): (b'W026', Snacks.REEF_SS08.value),
    (base_id + 400 + 5152): (b'W026', Snacks.REEF_SS09.value),
    (base_id + 400 + 5153): (b'W026', Snacks.REEF_SS10.value),
    (base_id + 400 + 5154): (b'W026', Snacks.REEF_SS11.value),
    (base_id + 400 + 5155): (b'W026', Snacks.REEF_SS12.value),
    (base_id + 400 + 5156): (b'W026', Snacks.REEF_SS13.value),
    (base_id + 400 + 5157): (b'W026', Snacks.REEF_SS14.value),
    (base_id + 400 + 5158): (b'W026', Snacks.REEF_SS15.value),
    (base_id + 400 + 5159): (b'W026', Snacks.SWINGER01_SS01.value),
    (base_id + 400 + 5160): (b'W026', Snacks.SWINGER01_SS010.value),
    (base_id + 400 + 5161): (b'W026', Snacks.SWINGER01_SS011.value),
    (base_id + 400 + 5162): (b'W026', Snacks.SWINGER01_SS012.value),
    (base_id + 400 + 5163): (b'W026', Snacks.SWINGER01_SS013.value),
    (base_id + 400 + 5164): (b'W026', Snacks.SWINGER01_SS014.value),
    (base_id + 400 + 5165): (b'W026', Snacks.SWINGER01_SS015.value),
    (base_id + 400 + 5166): (b'W026', Snacks.SWINGER01_SS016.value),
    (base_id + 400 + 5167): (b'W026', Snacks.SWINGER01_SS017.value),
    (base_id + 400 + 5168): (b'W026', Snacks.SWINGER01_SS018.value),
    (base_id + 400 + 5169): (b'W026', Snacks.SWINGER01_SS019.value),
    (base_id + 400 + 5170): (b'W026', Snacks.SWINGER02_SS01.value),
    (base_id + 400 + 5171): (b'W026', Snacks.SWINGER02_SS010.value),
    (base_id + 400 + 5172): (b'W026', Snacks.SWINGER02_SS011.value),
    (base_id + 400 + 5173): (b'W026', Snacks.SWINGER02_SS012.value),
    (base_id + 400 + 5174): (b'W026', Snacks.SWINGER02_SS013.value),
    (base_id + 400 + 5175): (b'W026', Snacks.SWINGER02_SS014.value),
    (base_id + 400 + 5176): (b'W026', Snacks.SWINGER02_SS015.value),
    (base_id + 400 + 5177): (b'W026', Snacks.SWINGER02_SS016.value),
    (base_id + 400 + 5178): (b'W026', Snacks.SWINGER02_SS017.value),
    (base_id + 400 + 5179): (b'W026', Snacks.SWINGER02_SS018.value),
    (base_id + 400 + 5180): (b'W026', Snacks.SWINGER02_SS019.value),
    (base_id + 400 + 5181): (b'W026', Snacks.SWINGER03_SS01.value),
    (base_id + 400 + 5182): (b'W026', Snacks.SWINGER03_SS010.value),
    (base_id + 400 + 5183): (b'W026', Snacks.SWINGER03_SS011.value),
    (base_id + 400 + 5184): (b'W026', Snacks.SWINGER03_SS012.value),
    (base_id + 400 + 5185): (b'W026', Snacks.SWINGER03_SS013.value),
    (base_id + 400 + 5186): (b'W026', Snacks.SWINGER03_SS014.value),
    (base_id + 400 + 5187): (b'W026', Snacks.SWINGER03_SS015.value),
    (base_id + 400 + 5188): (b'W026', Snacks.SWINGER03_SS016.value),
    (base_id + 400 + 5189): (b'W026', Snacks.SWINGER03_SS017.value),
    (base_id + 400 + 5190): (b'W026', Snacks.SWINGER03_SS018.value),
    (base_id + 400 + 5191): (b'W026', Snacks.SWINGER03_SS019.value),
    (base_id + 400 + 5192): (b'W026', Snacks.SWINGER04_SS01.value),
    (base_id + 400 + 5193): (b'W026', Snacks.SWINGER04_SS010.value),
    (base_id + 400 + 5194): (b'W026', Snacks.SWINGER04_SS011.value),
    (base_id + 400 + 5195): (b'W026', Snacks.SWINGER04_SS012.value),
    (base_id + 400 + 5196): (b'W026', Snacks.SWINGER04_SS013.value),
    (base_id + 400 + 5197): (b'W026', Snacks.SWINGER04_SS014.value),
    (base_id + 400 + 5198): (b'W026', Snacks.SWINGER04_SS015.value),
    (base_id + 400 + 5199): (b'W026', Snacks.SWINGER04_SS016.value),
    (base_id + 400 + 5200): (b'W026', Snacks.SWINGER04_SS017.value),
    (base_id + 400 + 5201): (b'W026', Snacks.SWINGER04_SS018.value),
    (base_id + 400 + 5202): (b'W026', Snacks.SWINGER04_SS019.value),
    (base_id + 400 + 5203): (b'W026', Snacks.SWINGER10_SS01.value),
    (base_id + 400 + 5204): (b'W026', Snacks.SWINGER10_SS02.value),
    (base_id + 400 + 5205): (b'W026', Snacks.SWINGER10_SS03.value),
    (base_id + 400 + 5206): (b'W026', Snacks.SWINGER10_SS04.value),
    (base_id + 400 + 5207): (b'W026', Snacks.SWINGER10_SS06.value),
    (base_id + 400 + 5208): (b'W026', Snacks.SWINGER10_SS07.value),
    (base_id + 400 + 5209): (b'W026', Snacks.SWINGER10_SS08.value),
    (base_id + 400 + 5210): (b'W026', Snacks.SWINGER10_SSBOX05.value),
    (base_id + 400 + 5211): (b'W026', Snacks.SWINGER10_SSBOX09.value),
    (base_id + 400 + 5212): (b'W026', Snacks.SWINGER5_SS01.value),
    (base_id + 400 + 5213): (b'W026', Snacks.SWINGER5_SS02.value),
    (base_id + 400 + 5214): (b'W026', Snacks.SWINGER5_SS03.value),
    (base_id + 400 + 5215): (b'W026', Snacks.SWINGER5_SS04.value),
    (base_id + 400 + 5216): (b'W026', Snacks.SWINGER5_SS06.value),
    (base_id + 400 + 5217): (b'W026', Snacks.SWINGER5_SS07.value),
    (base_id + 400 + 5218): (b'W026', Snacks.SWINGER5_SSBOX05.value),
    (base_id + 400 + 5219): (b'W026', Snacks.SWINGER6_SS01.value),
    (base_id + 400 + 5220): (b'W026', Snacks.SWINGER6_SS02.value),
    (base_id + 400 + 5221): (b'W026', Snacks.SWINGER6_SS03.value),
    (base_id + 400 + 5222): (b'W026', Snacks.SWINGER6_SS04.value),
    (base_id + 400 + 5223): (b'W026', Snacks.SWINGER6_SS06.value),
    (base_id + 400 + 5224): (b'W026', Snacks.SWINGER6_SS07.value),
    (base_id + 400 + 5225): (b'W026', Snacks.SWINGER6_SSBOX05.value),
    (base_id + 400 + 5226): (b'W026', Snacks.SWINGER7_SS01.value),
    (base_id + 400 + 5227): (b'W026', Snacks.SWINGER7_SS02.value),
    (base_id + 400 + 5228): (b'W026', Snacks.SWINGER7_SS03.value),
    (base_id + 400 + 5229): (b'W026', Snacks.SWINGER7_SS04.value),
    (base_id + 400 + 5230): (b'W026', Snacks.SWINGER7_SS06.value),
    (base_id + 400 + 5231): (b'W026', Snacks.SWINGER7_SS07.value),
    (base_id + 400 + 5232): (b'W026', Snacks.SWINGER7_SSBOX05.value),
    (base_id + 400 + 5233): (b'W026', Snacks.SWINGER8_SS01.value),
    (base_id + 400 + 5234): (b'W026', Snacks.SWINGER8_SS02.value),
    (base_id + 400 + 5235): (b'W026', Snacks.SWINGER8_SS03.value),
    (base_id + 400 + 5236): (b'W026', Snacks.SWINGER8_SS04.value),
    (base_id + 400 + 5237): (b'W026', Snacks.SWINGER8_SS06.value),
    (base_id + 400 + 5238): (b'W026', Snacks.SWINGER8_SS07.value),
    (base_id + 400 + 5239): (b'W026', Snacks.SWINGER8_SSBOX05.value),
    (base_id + 400 + 5240): (b'W026', Snacks.SWINGER9_SS01.value),
    (base_id + 400 + 5241): (b'W026', Snacks.SWINGER9_SS02.value),
    (base_id + 400 + 5242): (b'W026', Snacks.SWINGER9_SS03.value),
    (base_id + 400 + 5243): (b'W026', Snacks.SWINGER9_SS04.value),
    (base_id + 400 + 5244): (b'W026', Snacks.SWINGER9_SS06.value),
    (base_id + 400 + 5245): (b'W026', Snacks.SWINGER9_SS07.value),
    (base_id + 400 + 5246): (b'W026', Snacks.SWINGER9_SSBOX05.value),

    (base_id + 400 + 5247): (b'W027', Snacks.SS011.value),
    (base_id + 400 + 5248): (b'W027', Snacks.SS013.value),
    (base_id + 400 + 5249): (b'W027', Snacks.SS015.value),
    (base_id + 400 + 5250): (b'W027', Snacks.SS017.value),
    (base_id + 400 + 5251): (b'W027', Snacks.SS019.value),
    (base_id + 400 + 5252): (b'W027', Snacks.SS01A.value),
    (base_id + 400 + 5253): (b'W027', Snacks.SS01A1.value),
    (base_id + 400 + 5254): (b'W027', Snacks.SS01A3.value),
    (base_id + 400 + 5255): (b'W027', Snacks.SS01A5.value),
    (base_id + 400 + 5256): (b'W027', Snacks.SS01A7.value),
    (base_id + 400 + 5257): (b'W027', Snacks.SS021.value),
    (base_id + 400 + 5258): (b'W027', Snacks.SS023.value),
    (base_id + 400 + 5259): (b'W027', Snacks.SS025.value),
    (base_id + 400 + 5260): (b'W027', Snacks.SS027.value),
    (base_id + 400 + 5261): (b'W027', Snacks.SS029.value),
    (base_id + 400 + 5262): (b'W027', Snacks.SS02A.value),
    (base_id + 400 + 5263): (b'W027', Snacks.SS02A1.value),
    (base_id + 400 + 5264): (b'W027', Snacks.SS02A3.value),
    (base_id + 400 + 5265): (b'W027', Snacks.SS02A5.value),
    (base_id + 400 + 5266): (b'W027', Snacks.SS02A7.value),
    (base_id + 400 + 5267): (b'W027', Snacks.SS03B.value),
    (base_id + 400 + 5268): (b'W027', Snacks.SS03B1.value),
    (base_id + 400 + 5269): (b'W027', Snacks.SS03B3.value),
    (base_id + 400 + 5270): (b'W027', Snacks.SS03B5.value),
    (base_id + 400 + 5271): (b'W027', Snacks.SS03B7.value),
    (base_id + 400 + 5272): (b'W027', Snacks.SS04B.value),
    (base_id + 400 + 5273): (b'W027', Snacks.SS04B1.value),
    (base_id + 400 + 5274): (b'W027', Snacks.SS04B3.value),
    (base_id + 400 + 5275): (b'W027', Snacks.SS04B5.value),
    (base_id + 400 + 5276): (b'W027', Snacks.SS04B7.value),
    (base_id + 400 + 5277): (b'W027', Snacks.SS10.value),
    (base_id + 400 + 5278): (b'W027', Snacks.SS100.value),
    (base_id + 400 + 5279): (b'W027', Snacks.SS101.value),
    (base_id + 400 + 5280): (b'W027', Snacks.SS1010.value),
    (base_id + 400 + 5281): (b'W027', Snacks.SS1011.value),
    (base_id + 400 + 5282): (b'W027', Snacks.SS1012.value),
    (base_id + 400 + 5283): (b'W027', Snacks.SS10120.value),
    (base_id + 400 + 5284): (b'W027', Snacks.SS10121.value),
    (base_id + 400 + 5285): (b'W027', Snacks.SS10122.value),
    (base_id + 400 + 5286): (b'W027', Snacks.SS10123.value),
    (base_id + 400 + 5287): (b'W027', Snacks.SS10124.value),
    (base_id + 400 + 5288): (b'W027', Snacks.SS10125.value),
    (base_id + 400 + 5289): (b'W027', Snacks.SS102.value),
    (base_id + 400 + 5290): (b'W027', Snacks.SS103.value),
    (base_id + 400 + 5291): (b'W027', Snacks.SS104.value),
    (base_id + 400 + 5292): (b'W027', Snacks.SS105.value),
    (base_id + 400 + 5293): (b'W027', Snacks.SS106.value),
    (base_id + 400 + 5294): (b'W027', Snacks.SS1060.value),
    (base_id + 400 + 5295): (b'W027', Snacks.SS1061.value),
    (base_id + 400 + 5296): (b'W027', Snacks.SS1062.value),
    (base_id + 400 + 5297): (b'W027', Snacks.SS1063.value),
    (base_id + 400 + 5298): (b'W027', Snacks.SS1064.value),
    (base_id + 400 + 5299): (b'W027', Snacks.SS1065.value),
    (base_id + 400 + 5300): (b'W027', Snacks.SS107.value),
    (base_id + 400 + 5301): (b'W027', Snacks.SS108.value),
    (base_id + 400 + 5302): (b'W027', Snacks.SS109.value),
    (base_id + 400 + 5303): (b'W027', Snacks.SS11.value),
    (base_id + 400 + 5304): (b'W027', Snacks.SS111.value),
    (base_id + 400 + 5305): (b'W027', Snacks.SS113.value),
    (base_id + 400 + 5306): (b'W027', Snacks.SS115.value),
    (base_id + 400 + 5307): (b'W027', Snacks.SS117.value),
    (base_id + 400 + 5308): (b'W027', Snacks.SS119.value),
    (base_id + 400 + 5309): (b'W027', Snacks.SSBOX_GD01A.value),
    (base_id + 400 + 5310): (b'W027', Snacks.SSBOX_GD01B.value),
    (base_id + 400 + 5311): (b'W027', Snacks.SSBOX_GD02A.value),
    (base_id + 400 + 5312): (b'W027', Snacks.SSBOX_GD02B.value),
    (base_id + 400 + 5313): (b'W027', Snacks.SSCONV.value),
    (base_id + 400 + 5314): (b'W027', Snacks.SSCONV1.value),
    (base_id + 400 + 5315): (b'W027', Snacks.SSCONV11.value),
    (base_id + 400 + 5316): (b'W027', Snacks.SSCONV13.value),
    (base_id + 400 + 5317): (b'W027', Snacks.SSCONV15.value),
    (base_id + 400 + 5318): (b'W027', Snacks.SSCONV151.value),
    (base_id + 400 + 5319): (b'W027', Snacks.SSCONV1511.value),
    (base_id + 400 + 5320): (b'W027', Snacks.SSCONV1513.value),
    (base_id + 400 + 5321): (b'W027', Snacks.SSCONV153.value),
    (base_id + 400 + 5322): (b'W027', Snacks.SSCONV155.value),
    (base_id + 400 + 5323): (b'W027', Snacks.SSCONV157.value),
    (base_id + 400 + 5324): (b'W027', Snacks.SSCONV159.value),
    (base_id + 400 + 5325): (b'W027', Snacks.SSCONV3.value),
    (base_id + 400 + 5326): (b'W027', Snacks.SSCONV5.value),
    (base_id + 400 + 5327): (b'W027', Snacks.SSCONV7.value),
    (base_id + 400 + 5328): (b'W027', Snacks.SSCONV9.value),
    (base_id + 400 + 5329): (b'W027', Snacks.SSRP01.value),
    (base_id + 400 + 5330): (b'W027', Snacks.SSRP01_BOX.value),
    (base_id + 400 + 5331): (b'W027', Snacks.SSRP010.value),
    (base_id + 400 + 5332): (b'W027', Snacks.SSRP011.value),
    (base_id + 400 + 5333): (b'W027', Snacks.SSRP02.value),
    (base_id + 400 + 5334): (b'W027', Snacks.SSRP020.value),
    (base_id + 400 + 5335): (b'W027', Snacks.SSRP021.value),
    (base_id + 400 + 5336): (b'W027', Snacks.SSRP03.value),
    (base_id + 400 + 5337): (b'W027', Snacks.SSRP030.value),
    (base_id + 400 + 5338): (b'W027', Snacks.SSRP031.value),
    (base_id + 400 + 5339): (b'W027', Snacks.SSRP04.value),
    (base_id + 400 + 5340): (b'W027', Snacks.SSRP040.value),
    (base_id + 400 + 5341): (b'W027', Snacks.SSRP041.value),
    (base_id + 400 + 5342): (b'W027', Snacks.SSRP05.value),
    (base_id + 400 + 5343): (b'W027', Snacks.SSRP051.value),

    # Missed Initial Snacks, cleanup later and reorder
    (base_id + 400 + 5344): (b'E005', Snacks.SNACK__01.value),
    (base_id + 400 + 5345): (b'F001', Snacks.FOOD11.value),
    (base_id + 400 + 5346): (b'F001', Snacks.FOOD12.value),
    (base_id + 400 + 5347): (b'I006', Snacks.FOOD1.value),
    (base_id + 400 + 5348): (b'O001', Snacks.SN10.value),
    (base_id + 400 + 5349): (b'O001', Snacks.SN11.value),
    (base_id + 400 + 5350): (b'O001', Snacks.SN12.value),
    (base_id + 400 + 5351): (b'O001', Snacks.SN13.value),
    (base_id + 400 + 5352): (b'O001', Snacks.SN14.value),
    (base_id + 400 + 5353): (b'O001', Snacks.SN15.value),
    (base_id + 400 + 5354): (b'O001', Snacks.SN17.value),
    (base_id + 400 + 5355): (b'O001', Snacks.SN18.value),
    (base_id + 400 + 5356): (b'O001', Snacks.SN19.value),
    (base_id + 400 + 5357): (b'O001', Snacks.SN20.value),
    (base_id + 400 + 5358): (b'O001', Snacks.SN21.value),
    (base_id + 400 + 5359): (b'O001', Snacks.SN22.value),
    (base_id + 400 + 5360): (b'O001', Snacks.SN23.value),
    (base_id + 400 + 5361): (b'O001', Snacks.SN24.value),
    (base_id + 400 + 5362): (b'O001', Snacks.SN25.value),
    (base_id + 400 + 5363): (b'O001', Snacks.SN26.value),
    (base_id + 400 + 5364): (b'O001', Snacks.SN27.value),
    (base_id + 400 + 5365): (b'O001', Snacks.SN28.value),
    (base_id + 400 + 5366): (b'O001', Snacks.SN29.value),
    (base_id + 400 + 5367): (b'O001', Snacks.SN30.value),
    (base_id + 400 + 5368): (b'O001', Snacks.SN31.value),
    (base_id + 400 + 5369): (b'O001', Snacks.SN32.value),
    (base_id + 400 + 5370): (b'O001', Snacks.SN33.value),
    (base_id + 400 + 5371): (b'O001', Snacks.SN34.value),
    (base_id + 400 + 5372): (b'O001', Snacks.SN35.value),
    (base_id + 400 + 5373): (b'O001', Snacks.SN36.value),
    (base_id + 400 + 5374): (b'O001', Snacks.SN37.value),
    (base_id + 400 + 5375): (b'O001', Snacks.SN38.value),
    (base_id + 400 + 5376): (b'O001', Snacks.SN39.value),
    (base_id + 400 + 5377): (b'O001', Snacks.SN40.value),
    (base_id + 400 + 5378): (b'O001', Snacks.SN41.value),
    (base_id + 400 + 5379): (b'O001', Snacks.SN42.value),
    (base_id + 400 + 5380): (b'O001', Snacks.SN43.value),
    (base_id + 400 + 5381): (b'O001', Snacks.SN44.value),
    (base_id + 400 + 5382): (b'O001', Snacks.SN45.value),
    (base_id + 400 + 5383): (b'O001', Snacks.SN46.value),
    (base_id + 400 + 5384): (b'O001', Snacks.SN47.value),
    (base_id + 400 + 5385): (b'O001', Snacks.SN49.value),
    (base_id + 400 + 5386): (b'O001', Snacks.SN52.value),
    (base_id + 400 + 5387): (b'O001', Snacks.SN57.value),
    (base_id + 400 + 5388): (b'O001', Snacks.SN60.value),
    (base_id + 400 + 5389): (b'O001', Snacks.SN70.value),
    (base_id + 400 + 5390): (b'O001', Snacks.SN8.value),
    (base_id + 400 + 5391): (b'O001', Snacks.SN9.value),
    (base_id + 400 + 5392): (b'O001', Snacks.SSBOX01.value),
    (base_id + 400 + 5393): (b'O001', Snacks.SSBOX02.value),
    (base_id + 400 + 5394): (b'O001', Snacks.SSBOX03.value),
    (base_id + 400 + 5395): (b'O001', Snacks.SSBOX04.value),
    (base_id + 400 + 5396): (b'f010', Snacks.LOW__BOX.value),
    (base_id + 400 + 5397): (b'e003', Snacks.DIG__2__POWERUP.value),
}

valid_scenes = [
    b'B001', b'B002', b'B003', b'B004',
    b'C001', b'C002', b'C003', b'C004', b'C005', b'C006', b'C007',
    b'E001', b'E002', b'E003', b'E004', b'E005', b'E006', b'E007', b'E008', b'E009',
    b'F001', b'F003', b'F004', b'F005', b'F006', b'F007', b'F008', b'F009', b'F010',
    b'G001', b'G002', b'G003', b'G004', b'G005', b'G006', b'G007', b'G008', b'G009',
    b'H001', b'H002', b'H003', b'h001',
    b'I001', b'I003', b'I004', b'I005', b'I006', b'I020', b'I021',
    b'L011', b'L013', b'L014', b'L015', b'L017', b'L018', b'L019',
    b'O001', b'O002', b'O003', b'O004', b'O005', b'O006', b'O008',
    b'P001', b'P002', b'P003', b'P004', b'P005',
    b'R001', b'R002', b'R003', b'R004', b'R005', b'R020', b'R021',
    b'S001', b'S002', b'S003', b'S004', b'S005', b'S006',
    b'W020', b'W021', b'W022', b'W023', b'W025', b'W026', b'W027', b'W028',
]

invalid_scenes = [
    b'MNU3', b'MNU4',  # menus
]


class NO100FCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_dolphin(self):
        """Check Dolphin Connection State"""
        if isinstance(self.ctx, NO100FContext):
            logger.info(f"Dolphin Status: {self.ctx.dolphin_status}")

    def _cmd_resetscooby(self):
        """Force Kill Scooby to escape softlocks"""
        if dolphin_memory_engine.is_hooked():
            dolphin_memory_engine.write_word(HEALTH_ADDR, 69)
            logger.info("Killing Scooby :(")

    def _cmd_resend(self):
        """Use this command if somehow an item has erroneously not made it to your game"""
        if dolphin_memory_engine.is_hooked():
            dolphin_memory_engine.write_word(MONSTER_TOKEN_INVENTORY_ADDR, 0x0000)
            dolphin_memory_engine.write_word(UPGRADE_INVENTORY_ADDR, 0x0000)
            for i in range(0, 21):
                dolphin_memory_engine.write_word(KEY_COUNT_ADDR + i, 0x0)
            dolphin_memory_engine.write_word(EXPECTED_INDEX_ADDR, 0x0000)
            logger.info("Resending Inventory")

    def _cmd_keys(self):
        """Displays current key counts and the number expected in a room"""

        count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR) % 0x10
        if count > 1:
            count = 1
        logger.info(f"Clamor 1 Keys {count}/1")

        count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR) // 0x10
        if count > 1:
            count = 1
        logger.info(f"Hedge Maze Keys {count}/1")

        count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 1) % 0x10
        if count > 1:
            count = 1
        logger.info(f"Fishing Village Keys {count}/1")

        count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 1) // 0x10
        if count > 3:
            count = 3
        logger.info(f"Cellar 2 Keys {count}/3")

        count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 2) % 0x10
        if count > 4:
            count = 4
        logger.info(f"Cellar 3 Keys {count}/4")

        count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 2) // 0x10
        if count > 4:
            count = 4
        logger.info(f"Cavein Keys {count}/4")

        count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 3) % 0x10
        if count > 4:
            count = 4
        logger.info(f"Fishy Clues Keys {count}/4")

        count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 3) // 0x10
        if count > 3:
            count = 3
        logger.info(f"Graveplot Keys {count}/3")

        count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 4) % 0x10
        if count > 1:
            count = 1
        logger.info(f"Tomb 1 Keys {count}/1")

        count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 4) // 0x10
        if count > 2:
            count = 2
        logger.info(f"Tomb 3 Keys {count}/2")

        count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 5) % 0x10
        if count > 1:
            count = 1
        logger.info(f"Clamor 4 Keys {count}/1")

        count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 5) // 0x10
        if count > 4:
            count = 4
        logger.info(f"MYM Keys {count}/4")

        count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 6) % 0x10
        if count > 4:
            count = 4
        logger.info(f"Coast Keys {count}/4")

        count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 6) // 0x10
        if count > 3:
            count = 3
        logger.info(f"Attic Keys {count}/3")

        count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 7) % 0x10
        if count > 4:
            count = 4
        logger.info(f"Knight Keys {count}/4")

        count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 7) // 0x10
        if count > 5:
            count = 5
        logger.info(f"Creepy 2 Keys {count}/5")

        count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 8) % 0x10
        if count > 3:
            count = 3
        logger.info(f"Creepy 3 Keys {count}/3")

        count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 8) // 0x10
        if count > 1:
            count = 1
        logger.info(f"Gusts 1 Keys {count}/1")

        count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 9) % 0x10
        if count > 4:
            count = 4
        logger.info(f"Gusts 2 Keys {count}/4")

        count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 9) // 0x10
        if count > 3:
            count = 3
        logger.info(f"DLD Keys {count}/3")

        count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 10) % 0x10
        if count > 4:
            count = 4
        logger.info(f"Shiver Keys {count}/4")


class NO100FContext(CommonContext):
    command_processor = NO100FCommandProcessor
    game = "Scooby-Doo! Night of 100 Frights"
    items_handling = 0b111  # full remote

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.items_received_2 = []
        self.dolphin_sync_task = None
        self.dolphin_status = CONNECTION_INITIAL_STATUS
        self.awaiting_rom = False
        self.LAST_STATE = [bytes([0, 0]), bytes([0, 0]), bytes([0, 0])]
        self.last_rev_index = -1
        self.has_send_death = False
        self.forced_death = False
        self.post_boss = False
        self.last_death_link_send = time.time()
        self.current_scene_key = None
        self.use_tokens = False
        self.use_keys = 0
        self.use_warpgates = False
        self.use_speedster = False
        self.use_snacks = False
        self.current_scene = None
        self.previous_scene = None
        self.CitM1_key = 0
        self.hedge_key = 0
        self.fish_key = 0
        self.WYitC2_keys = 0
        self.WYitC3_keys = 0
        self.MCaC_keys = 0
        self.FCfS_keys = 0
        self.TSfaGP_keys = 0
        self.GDDitT1_key = 0
        self.GDDitT3_keys = 0
        self.CitM4_key = 0
        self.MyM2_keys = 0
        self.CfsG1_keys = 0
        self.PitA2_keys = 0
        self.ADaSK2_keys = 0
        self.CCitH2_keys = 0
        self.CCitH3_keys = 0
        self.GAU1_key = 0
        self.GAU2_keys = 0
        self.DLDS2_keys = 0
        self.SYTS1_keys = 0

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.auth = None
        await super().disconnect(allow_autoreconnect)

    def on_package(self, cmd: str, args: dict):
        if cmd == 'Connected':
            self.current_scene_key = f"NO100F_current_scene_T{self.team}_P{self.slot}"
            self.set_notify(self.current_scene_key)
            self.last_rev_index = -1
            self.items_received_2 = []
            self.included_check_types = CheckTypes.UPGRADES
            if 'death_link' in args['slot_data']:
                Utils.async_start(self.update_death_link(bool(args['slot_data']['death_link'])))
            if 'include_monster_tokens' in args['slot_data'] and args['slot_data']['include_monster_tokens']:
                self.use_tokens = True
            if 'include_keys' in args['slot_data']:
                self.use_keys = args['slot_data']['include_keys']
            if 'include_warpgates' in args['slot_data'] and args['slot_data']['include_warpgates']:
                self.use_warpgates = True
            if 'include_snacks' in args['slot_data'] and args['slot_data']['include_snacks']:
                self.use_snacks = True
            if 'speedster' in args['slot_data'] and args['slot_data']['speedster']:
                self.use_speedster = True
            if 'completion_goal' in args['slot_data']:
                self.completion_goal = args['slot_data']['completion_goal']
                if self.completion_goal > 3 and not self.use_snacks:
                    self.completion_goal -= 4  # Negate Snack selection if Snacksanity is disabled
            if 'boss_count' in args['slot_data']:
                self.boss_count = args['slot_data']['boss_count']
            if 'token_count' in args['slot_data']:
                self.token_count = args['slot_data']['token_count']
            if 'snack_count' in args['slot_data']:
                self.snack_count = args['slot_data']['snack_count']
        if cmd == 'ReceivedItems':
            if args["index"] >= self.last_rev_index:
                self.last_rev_index = args["index"]
                for item in args['items']:
                    self.items_received_2.append((item, self.last_rev_index))
                    self.last_rev_index += 1
            self.items_received_2.sort(key=lambda v: v[1])

    def on_deathlink(self, data: Dict[str, Any]) -> None:
        super().on_deathlink(data)
        _give_death(self)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            logger.info('Enter the password required to join this game:')
            self.password = await self.console_input()
        if not self.auth:
            if self.awaiting_rom:
                return
            self.awaiting_rom = True
            logger.info('Awaiting connection to Dolphin to get player information')
            return
        await self.send_connect()

    def run_gui(self):
        from kvui import GameManager

        class NO100FManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Scooby Doo: Night of 100 Frights Client"

        self.ui = NO100FManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


def _is_ptr_valid(ptr):
    return 0x80000000 <= ptr < 0x817fffff


def _is_scene_visited(target_scene: bytes):
    current_index = VISITED_SCENES_ADDR
    current_value = 1
    while not current_value == 0:
        current_value = dolphin_memory_engine.read_word(current_index)
        if current_value == int.from_bytes(target_scene, "big"):
            return True
        current_index += 0x10
    return False


def _find_obj_in_obj_table(id: int, ptr: Optional[int] = None, size: Optional[int] = None):
    if size is None:
        size = dolphin_memory_engine.read_word(SCENE_OBJ_LIST_SIZE_ADDR)
    if ptr is None:
        ptr = dolphin_memory_engine.read_word(SCENE_OBJ_LIST_PTR_ADDR)
        if not _is_ptr_valid(ptr): return None
    try:
        counter_list_entry = 0
        # this is our initial index "guess"
        idx = id & (size - 1)
        skip = False
        for i in range(0, size):
            # addr for entry in the list at idx
            counter_list_entry = ptr + idx * 0x8
            if not _is_ptr_valid(counter_list_entry):
                return None
            # get id from the entry
            obj_id = dolphin_memory_engine.read_word(counter_list_entry)
            # if the id matches, we are at the right entry
            if obj_id == id:
                break
            # returns NULL if it encounters id 0, so just skip if we do
            if obj_id == 0:
                break
            # we are not at the right entry so look at the next
            idx += 1
            # rollover at end of list
            if idx == size:
                idx = 0
        if skip: return -1
        # read counter pointer from the entry
        obj_ptr = dolphin_memory_engine.read_word(counter_list_entry + 0x4)
        if not _is_ptr_valid(obj_ptr):
            return None
        return obj_ptr
    except:
        return None


def _give_snack(ctx: NO100FContext, offset: int):
    cur_snack_count = dolphin_memory_engine.read_word(STORED_SNACK_ADDR)
    if offset == 1:
        cur_snack_count += 5
    else:
        cur_snack_count += 1

    dolphin_memory_engine.write_word(STORED_SNACK_ADDR, cur_snack_count)


def _give_powerup(ctx: NO100FContext, bit: int):
    cur_upgrades = dolphin_memory_engine.read_word(UPGRADE_INVENTORY_ADDR)

    if bit == 4:    # Progressive Sneak Upgrade
        if not cur_upgrades & 2 ** 4:
            cur_upgrades += 2 ** 4
        elif not cur_upgrades & 2 ** 5:
            cur_upgrades += 2 ** 5
        elif not cur_upgrades & 2 ** 6:
            cur_upgrades += 2 ** 6
        dolphin_memory_engine.write_word(UPGRADE_INVENTORY_ADDR, cur_upgrades)

    if bit == 9:    # Progressive Jump Upgrade
        if not cur_upgrades & 2 ** 9:
            cur_upgrades += 2 ** 9
        elif not cur_upgrades & 2 ** 12:
            cur_upgrades += 2 ** 12
        dolphin_memory_engine.write_word(UPGRADE_INVENTORY_ADDR, cur_upgrades)

    if (bit == 13) and cur_upgrades & 2 ** 7:  # Player is getting a shovel and currently has the fake
        cur_upgrades -= 2 ** 7
        dolphin_memory_engine.write_word(UPGRADE_INVENTORY_ADDR, cur_upgrades)

    if cur_upgrades & 2 ** bit == 0:
        dolphin_memory_engine.write_word(UPGRADE_INVENTORY_ADDR, cur_upgrades + 2 ** bit)


def _give_gum_upgrade(ctx: NO100FContext):
    cur_max_gum = dolphin_memory_engine.read_word(MAX_GUM_COUNT_ADDR)
    dolphin_memory_engine.write_word(MAX_GUM_COUNT_ADDR, cur_max_gum + 5)


def _give_soap_upgrade(ctx: NO100FContext):
    cur_max_soap = dolphin_memory_engine.read_word(MAX_SOAP_COUNT_ADDR)
    dolphin_memory_engine.write_word(MAX_SOAP_COUNT_ADDR, cur_max_soap + 5)


def _give_monstertoken(ctx: NO100FContext):
    cur_monster_tokens = dolphin_memory_engine.read_word(MONSTER_TOKEN_INVENTORY_ADDR)
    i = 0
    while cur_monster_tokens & 2 ** i and i < 21:  #Advance Index to the smallest non-high bit
        i += 1

    dolphin_memory_engine.write_word(MONSTER_TOKEN_INVENTORY_ADDR, cur_monster_tokens + 2 ** i)


def _give_key(ctx: NO100FContext, offset: int):

    cur_count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + offset // 2)

    if (offset % 2) > 0:    # The Key is in an Odd Position in Memory
        cur_count += 0x10
    else:
        cur_count += 1

    dolphin_memory_engine.write_byte(KEY_COUNT_ADDR + offset // 2, cur_count)

def _give_keyring(ctx: NO100FContext, offset: int):
    i = 6
    while i > 0:
        _give_key(ctx, offset)
        i -= 1

def _give_warp(ctx: NO100FContext, offset: int):
    cur_warps = dolphin_memory_engine.read_word(SAVED_WARP_ADDR)
    if not cur_warps & 2 ** offset == 2 ** offset:
        cur_warps += 2 ** offset
        dolphin_memory_engine.write_word(SAVED_WARP_ADDR, cur_warps)


def _give_death(ctx: NO100FContext):
    PauseRead1 = dolphin_memory_engine.read_byte(0x80234DCF)
    PauseRead2 = dolphin_memory_engine.read_byte(0x80234E80)
    isPaused = (PauseRead1 == 0 and PauseRead2 == 0)
    if ctx.slot and dolphin_memory_engine.is_hooked() and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS \
            and check_ingame(ctx) and check_control_owner(ctx, lambda owner: owner == 1) and not isPaused:
        dolphin_memory_engine.write_word(HEALTH_ADDR, 0)


def _check_cur_scene(ctx: NO100FContext, scene_id: bytes, scene_ptr: Optional[int] = None):
    cur_scene = dolphin_memory_engine.read_bytes(CUR_SCENE_ADDR, 0x4)
    return cur_scene == scene_id


def _give_item(ctx: NO100FContext, item_id: int):
    true_id = item_id - base_id  # Use item_id to generate offset for use with functions
    if 0 <= true_id <= 106:  # ID is expected value

        if true_id < 7:
            _give_powerup(ctx, true_id)

        elif true_id < 13:
            _give_powerup(ctx, true_id + 2)  # There are 2 unused bits at 8 and 9, offset remaining actual upgrades.

        elif true_id == 13:
            _give_gum_upgrade(ctx)

        elif true_id == 14:
            _give_soap_upgrade(ctx)

        if true_id == 35:
            _give_monstertoken(ctx)

        if 36 <= true_id <= 56:
            _give_key(ctx, true_id - 36)

        if 57 <= true_id <= 82:
            _give_warp(ctx, true_id - 57)

        if 83 <= true_id <= 103:
            _give_keyring(ctx, true_id - 83)

        if true_id == 104:
            _give_snack(ctx, 0)

        if 105 <= true_id <= 106:
            _give_snack(ctx, true_id - 105)

    else:
        logger.warning(f"Received unknown item with id {item_id}")


def _set_platform_state(ctx: NO100FContext, ptr, state):
    if not ptr == None:
        dolphin_memory_engine.write_byte(ptr + 0x14, state)


def _set_platform_collision_state(ctx: NO100FContext, ptr, state):
    if not ptr == None:
        dolphin_memory_engine.write_byte(ptr + 0x28, state)


def _check_platform_state(ctx: NO100FContext, ptr):
    if not ptr == None:
        return dolphin_memory_engine.read_byte(ptr + 0x14)


def _set_trigger_state(ctx: NO100FContext, ptr, state):
    if not ptr == None:
        dolphin_memory_engine.write_byte(ptr + 0x7, state)


def _set_counter_value(ctx: NO100FContext, ptr, count):
    if not ptr == None:
        dolphin_memory_engine.write_byte(ptr + 0x15, count)


def _set_pickup_active(ctx: NO100FContext, ptr, state):
    if not ptr == None:
        dolphin_memory_engine.write_byte(ptr + 0x7, state)


async def apply_key_fixes(ctx: NO100FContext):
    scene = dolphin_memory_engine.read_bytes(CUR_SCENE_ADDR, 0x4)
    ptr = dolphin_memory_engine.read_word(SCENE_OBJ_LIST_PTR_ADDR)
    if not _is_ptr_valid(ptr):
        return
    size = dolphin_memory_engine.read_word(SCENE_OBJ_LIST_SIZE_ADDR)

    if scene == b'I001':
        fix_ptr = _find_obj_in_obj_table(0x1e1157c3, ptr, size)
        if not fix_ptr == None:
            if ctx.CitM1_key >= 1:  # The Key is collected, allow door to open
                fix_ptr = _find_obj_in_obj_table(0x1e1157c3, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1d)
                fix_ptr = _find_obj_in_obj_table(0x586E19B9, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1d)

            if ctx.CitM1_key == 0:  # The Key is not collected, block door from opening
                fix_ptr = _find_obj_in_obj_table(0x586E19B9, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1c)

    if scene == b'H001' or b'h001':
        fix_ptr = _find_obj_in_obj_table(0xC20224F3, ptr, size)
        if not fix_ptr == None:
            if ctx.hedge_key >= 1:  # The Hedge key is collected, open the gate
                fix_ptr = _find_obj_in_obj_table(0xC20224F3, ptr, size)
                _set_platform_state(ctx, fix_ptr, 0)

                fix_ptr = _find_obj_in_obj_table(0xE8B3FF9B, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1c)

                fix_ptr = _find_obj_in_obj_table(0xD72B66B7, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1d)

            else:  # Hedge Key is not collected, make sure the gate is closed
                fix_ptr = _find_obj_in_obj_table(0xC20224F3, ptr, size)
                _set_platform_state(ctx, fix_ptr, 1)

                fix_ptr = _find_obj_in_obj_table(0xE8B3FF9B, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1d)

                fix_ptr = _find_obj_in_obj_table(0xD72B66B7, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1c)

        fix_ptr = _find_obj_in_obj_table(0x42A3128E, ptr, size)
        if not fix_ptr == None:
            if ctx.fish_key >= 1:  # The Fishing key is collected, open the gate
                fix_ptr = _find_obj_in_obj_table(0x42A3128E, ptr, size)
                _set_platform_state(ctx, fix_ptr, 0)

                fix_ptr = _find_obj_in_obj_table(0xD74DB452, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1f)

                fix_ptr = _find_obj_in_obj_table(0x2E8B6D0E, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1E)

            else:  # Fishing Key is not collected, make sure the gate is closed
                fix_ptr = _find_obj_in_obj_table(0x42A3128E, ptr, size)
                _set_platform_state(ctx, fix_ptr, 1)

                fix_ptr = _find_obj_in_obj_table(0xD74DB452, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1e)

                fix_ptr = _find_obj_in_obj_table(0x2E8B6D0E, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1f)

    if scene == b'B002':
        fix_ptr = _find_obj_in_obj_table(0xc71019dc, ptr, size)
        if not fix_ptr == None:
            if ctx.WYitC2_keys >= 3:
                fix_ptr = _find_obj_in_obj_table(0xc71019dc, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1d)

                fix_ptr = _find_obj_in_obj_table(0x0dcb1cd3, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1c)

            else:
                fix_ptr = _find_obj_in_obj_table(0xc71019dc, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1c)

                fix_ptr = _find_obj_in_obj_table(0x0dcb1cd3, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1d)

    if scene == b'B003':
        fix_ptr = _find_obj_in_obj_table(0x060e343c, ptr, size)
        if not fix_ptr == None:
            if ctx.WYitC3_keys >= 4:
                fix_ptr = _find_obj_in_obj_table(0xE7196747, ptr, size)
                _set_platform_collision_state(ctx, fix_ptr, 0)
                _set_platform_state(ctx, fix_ptr, 0)
                return
            else:
                _set_counter_value(ctx, fix_ptr, 4)

    if scene == b'C005':
        fix_ptr = _find_obj_in_obj_table(0xD6E6CB86, ptr, size)
        if not fix_ptr == None:
            if ctx.MCaC_keys >= 4:  # Keys collected, open the gate
                fix_ptr = _find_obj_in_obj_table(0xD6E6CB86, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1f)

                fix_ptr = _find_obj_in_obj_table(0x44BC97A7, ptr, size)
                _set_platform_state(ctx, fix_ptr, 0)

                fix_ptr = _find_obj_in_obj_table(0x44BC97A8, ptr, size)
                _set_platform_state(ctx, fix_ptr, 0)

                fix_ptr = _find_obj_in_obj_table(0x44BC97A9, ptr, size)
                _set_platform_state(ctx, fix_ptr, 0)

                fix_ptr = _find_obj_in_obj_table(0x44BC97AA, ptr, size)
                _set_platform_state(ctx, fix_ptr, 0)

            else:  # Keys not collected, make sure the gate is closed
                fix_ptr = _find_obj_in_obj_table(0xD6E6CB86, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1e)

                fix_ptr = _find_obj_in_obj_table(0x44BC97A7, ptr, size)
                _set_platform_state(ctx, fix_ptr, 1)

                fix_ptr = _find_obj_in_obj_table(0x44BC97A8, ptr, size)
                _set_platform_state(ctx, fix_ptr, 1)

                fix_ptr = _find_obj_in_obj_table(0x44BC97A9, ptr, size)
                _set_platform_state(ctx, fix_ptr, 1)

                fix_ptr = _find_obj_in_obj_table(0x44BC97AA, ptr, size)
                _set_platform_state(ctx, fix_ptr, 1)

    if scene == b'F005':
        fix_ptr = _find_obj_in_obj_table(0xD0798EC6, ptr, size)
        if not fix_ptr == None:
            if ctx.FCfS_keys >= 4:  # Keys collected, open the gate
                fix_ptr = _find_obj_in_obj_table(0xD0798EC6, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1d)

                fix_ptr = _find_obj_in_obj_table(0x7D81EA8F, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1c)

                fix_ptr = _find_obj_in_obj_table(0x1F0FB518, ptr, size)
                _set_platform_state(ctx, fix_ptr, 0)

                fix_ptr = _find_obj_in_obj_table(0x1F0FB519, ptr, size)
                _set_platform_state(ctx, fix_ptr, 0)

                fix_ptr = _find_obj_in_obj_table(0x1F0FB51A, ptr, size)
                _set_platform_state(ctx, fix_ptr, 0)

                fix_ptr = _find_obj_in_obj_table(0x1F0FB51B, ptr, size)
                _set_platform_state(ctx, fix_ptr, 0)

            else:  # Keys not collected, make sure the gate is closed
                fix_ptr = _find_obj_in_obj_table(0xD0798EC6, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1c)

                fix_ptr = _find_obj_in_obj_table(0x7D81EA8F, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1d)

                fix_ptr = _find_obj_in_obj_table(0x1F0FB518, ptr, size)
                _set_platform_state(ctx, fix_ptr, 1)

                fix_ptr = _find_obj_in_obj_table(0x1F0FB519, ptr, size)
                _set_platform_state(ctx, fix_ptr, 1)

                fix_ptr = _find_obj_in_obj_table(0x1F0FB51A, ptr, size)
                _set_platform_state(ctx, fix_ptr, 1)

                fix_ptr = _find_obj_in_obj_table(0x1F0FB51B, ptr, size)
                _set_platform_state(ctx, fix_ptr, 1)

    if scene == b'G001':
        fix_ptr = _find_obj_in_obj_table(0x7fcdbe0f, ptr, size)
        if not fix_ptr == None:
            if ctx.TSfaGP_keys >= 3:  # The keys are collected, open the gate
                fix_ptr = _find_obj_in_obj_table(0x7fcdbe0f, ptr, size)
                _set_platform_state(ctx, fix_ptr, 0)

                fix_ptr = _find_obj_in_obj_table(0xD77001EE, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1f)

                fix_ptr = _find_obj_in_obj_table(0xA433F2EC, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1e)

            else:  # Keys not collected, make sure the gate is closed
                fix_ptr = _find_obj_in_obj_table(0x7fcdbe0f, ptr, size)
                _set_platform_state(ctx, fix_ptr, 1)

                fix_ptr = _find_obj_in_obj_table(0xD77001EE, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1e)

                fix_ptr = _find_obj_in_obj_table(0xA433F2EC, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1f)

    if scene == b'G007':
        fix_ptr = _find_obj_in_obj_table(0x0013c74b, ptr, size)
        if not fix_ptr == None:
            if ctx.GDDitT1_key >= 1:
                fix_ptr2 = _find_obj_in_obj_table(0x4A884EB4, ptr, size)
                _set_platform_collision_state(ctx, fix_ptr2, 0)
                _set_platform_state(ctx, fix_ptr2, 0)

                fix_ptr2 = _find_obj_in_obj_table(0x4A884EB5, ptr, size)
                _set_platform_collision_state(ctx, fix_ptr2, 0)
                _set_platform_state(ctx, fix_ptr2, 0)

                fix_ptr2 = _find_obj_in_obj_table(0x7FCDBE0F, ptr, size)
                if _check_platform_state(ctx, fix_ptr2) == 1:
                    _set_pickup_active(ctx, fix_ptr, 0x1f)
                    _set_platform_state(ctx, fix_ptr, 1)
                    _set_pickup_state(ctx, fix_ptr, 0x41)
                else:
                    _set_pickup_state(ctx, fix_ptr, 0x48)

            else:
                _set_pickup_active(ctx, fix_ptr, 0x1e)
                _set_platform_state(ctx, fix_ptr, 1)

    if scene == b'G009':
        fix_ptr = _find_obj_in_obj_table(0x060e343c, ptr, size)
        if not fix_ptr == None:
            if ctx.GDDitT3_keys >= 2:
                return
            else:
                _set_counter_value(ctx, fix_ptr, 2)

    if scene == b'I003':
        fix_ptr = _find_obj_in_obj_table(0x13109411, ptr, size)
        if not fix_ptr == None:
            if ctx.CitM4_key >= 1:
                _set_pickup_active(ctx, fix_ptr, 0x1d)
                fix_ptr = _find_obj_in_obj_table(0x7B5AC815, ptr, size)
                _set_platform_collision_state(ctx, fix_ptr, 0)
                _set_platform_state(ctx, fix_ptr, 0)

                fix_ptr = _find_obj_in_obj_table(0xDa0349cc, ptr, size)
                _set_platform_state(ctx, fix_ptr, 0x1e)
            else:
                _set_pickup_active(ctx, fix_ptr, 0x1c)

    if scene == b'I005':
        fix_ptr = _find_obj_in_obj_table(0x060e343c, ptr, size)
        if not fix_ptr == None:
            if ctx.MyM2_keys >= 4:
                fix_ptr = _find_obj_in_obj_table(0xD4FBFFD9, ptr, size)
                _set_platform_collision_state(ctx, fix_ptr, 0)
                _set_platform_state(ctx, fix_ptr, 0)
                return
            else:
                _set_counter_value(ctx, fix_ptr, 4)

    if scene == b'L011':
        fix_ptr = _find_obj_in_obj_table(0xD14760E8, ptr, size)
        if not fix_ptr == None:
            if ctx.CfsG1_keys >= 4:  # Keys collected, open the gate
                fix_ptr = _find_obj_in_obj_table(0xD14760E8, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1d)

                fix_ptr = _find_obj_in_obj_table(0x7334b00b, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1e)

                fix_ptr = _find_obj_in_obj_table(0x1F0FB518, ptr, size)
                _set_platform_state(ctx, fix_ptr, 0)

                fix_ptr = _find_obj_in_obj_table(0x1F0FB519, ptr, size)
                _set_platform_state(ctx, fix_ptr, 0)

                fix_ptr = _find_obj_in_obj_table(0x1F0FB51A, ptr, size)
                _set_platform_state(ctx, fix_ptr, 0)

                fix_ptr = _find_obj_in_obj_table(0x1F0FB51B, ptr, size)
                _set_platform_state(ctx, fix_ptr, 0)

            else:  # Keys not collected, make sure the gate is closed
                fix_ptr = _find_obj_in_obj_table(0xD14760E8, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1c)

                fix_ptr = _find_obj_in_obj_table(0x7334b00b, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1f)

                fix_ptr = _find_obj_in_obj_table(0x1F0FB518, ptr, size)
                _set_platform_state(ctx, fix_ptr, 1)

                fix_ptr = _find_obj_in_obj_table(0x1F0FB519, ptr, size)
                _set_platform_state(ctx, fix_ptr, 1)

                fix_ptr = _find_obj_in_obj_table(0x1F0FB51A, ptr, size)
                _set_platform_state(ctx, fix_ptr, 1)

                fix_ptr = _find_obj_in_obj_table(0x1F0FB51B, ptr, size)
                _set_platform_state(ctx, fix_ptr, 1)

    if scene == b'O003':
        fix_ptr = _find_obj_in_obj_table(0xB418244E, ptr, size)
        if not fix_ptr == None:
            if ctx.PitA2_keys >= 3:  # Keys collected, open the gate
                fix_ptr = _find_obj_in_obj_table(0xB418244E, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1f)

                fix_ptr = _find_obj_in_obj_table(0x9F625B9C, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1e)

                fix_ptr = _find_obj_in_obj_table(0x1F0FB518, ptr, size)
                _set_platform_state(ctx, fix_ptr, 0)

                fix_ptr = _find_obj_in_obj_table(0x1F0FB519, ptr, size)
                _set_platform_state(ctx, fix_ptr, 0)

                fix_ptr = _find_obj_in_obj_table(0x1F0FB51A, ptr, size)
                _set_platform_state(ctx, fix_ptr, 0)

            else:  # Keys not collected, make sure the gate is closed
                fix_ptr = _find_obj_in_obj_table(0xB418244E, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1e)

                fix_ptr = _find_obj_in_obj_table(0x09F625B9C, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1f)

                fix_ptr = _find_obj_in_obj_table(0x1F0FB518, ptr, size)
                _set_platform_state(ctx, fix_ptr, 1)

                fix_ptr = _find_obj_in_obj_table(0x1F0FB519, ptr, size)
                _set_platform_state(ctx, fix_ptr, 1)

                fix_ptr = _find_obj_in_obj_table(0x1F0FB51A, ptr, size)
                _set_platform_state(ctx, fix_ptr, 1)

    if scene == b'O006':
        fix_ptr = _find_obj_in_obj_table(0x060e343c, ptr, size)
        if not fix_ptr == None:
            if ctx.ADaSK2_keys >= 4:
                fix_ptr = _find_obj_in_obj_table(0x4DE2CB91, ptr, size)
                _set_platform_collision_state(ctx, fix_ptr, 0)
                _set_platform_state(ctx, fix_ptr, 0)
                fix_ptr = _find_obj_in_obj_table(0xc9e0fb6A, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1e)
                return
            else:
                _set_counter_value(ctx, fix_ptr, 4)

    if scene == b'P002':
        fix_ptr = _find_obj_in_obj_table(0x060e343c, ptr, size)
        if not fix_ptr == None:
            if ctx.CCitH2_keys >= 4:
                fix_ptr = _find_obj_in_obj_table(0xE7196746, ptr, size)
                _set_platform_collision_state(ctx, fix_ptr, 0)
                _set_platform_state(ctx, fix_ptr, 0)
                fix_ptr = _find_obj_in_obj_table(0x4ac3ac06, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1e)
            else:
                _set_counter_value(ctx, fix_ptr, 4)

            fix_ptr = _find_obj_in_obj_table(0x0a1efb96, ptr, size)
            if ctx.CCitH2_keys >= 5:
                _set_pickup_active(ctx, fix_ptr, 0x1f)
                fix_ptr = _find_obj_in_obj_table(0xE7196749, ptr, size)
                _set_platform_collision_state(ctx, fix_ptr, 0)
                _set_platform_state(ctx, fix_ptr, 0)
    
                fix_ptr = _find_obj_in_obj_table(0xE719674B, ptr, size)
                _set_platform_collision_state(ctx, fix_ptr, 0)
                _set_platform_state(ctx, fix_ptr, 0)

    if scene == b'P003':
        fix_ptr = _find_obj_in_obj_table(0x060e343c, ptr, size)
        if not fix_ptr == None:
            if ctx.CCitH3_keys >= 3:
                return
            else:
                _set_counter_value(ctx, fix_ptr, 3)

    if scene == b'P004':
        fix_ptr = _find_obj_in_obj_table(0x0a1efb92, ptr, size)
        if not fix_ptr == None:
            if ctx.GAU1_key >= 1:
                _set_pickup_active(ctx, fix_ptr, 0x1d)
                fix_ptr = _find_obj_in_obj_table(0xE7196747, ptr, size)
                _set_platform_collision_state(ctx, fix_ptr, 0)
                _set_platform_state(ctx, fix_ptr, 0)

                fix_ptr = _find_obj_in_obj_table(0x18E5F2D9, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1c)
            else:
                _set_pickup_active(ctx, fix_ptr, 0x1c)

    if scene == b'P005':
        fix_ptr = _find_obj_in_obj_table(0x060e343c, ptr, size)
        if not fix_ptr == None:
            if ctx.GAU2_keys >= 4:
                fix_ptr = _find_obj_in_obj_table(0xB3FDF2CE, ptr, size)
                _set_platform_collision_state(ctx, fix_ptr, 0)
                _set_platform_state(ctx, fix_ptr, 0)

                fix_ptr = _find_obj_in_obj_table(0xA25C26B4, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1e)
                _set_platform_state(ctx, fix_ptr, 0)
                return
            else:
                _set_counter_value(ctx, fix_ptr, 4)

    if scene == b'R005':
        fix_ptr = _find_obj_in_obj_table(0xc71019dc, ptr, size)
        if not fix_ptr == None:
            if ctx.DLDS2_keys >= 3:
                fix_ptr = _find_obj_in_obj_table(0xc71019dc, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1f)

                fix_ptr = _find_obj_in_obj_table(0x510f16db, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1E)

            else:
                fix_ptr = _find_obj_in_obj_table(0xc71019dc, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1e)

                fix_ptr = _find_obj_in_obj_table(0x510f16db, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1f)

    if scene == b'W027':
        fix_ptr = _find_obj_in_obj_table(0xD2c0b719, ptr, size)
        if not fix_ptr == None:
            if ctx.SYTS1_keys >= 4:  # Keys collected, open the gate
                fix_ptr = _find_obj_in_obj_table(0xD2c0b719, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1f)

                fix_ptr = _find_obj_in_obj_table(0x7D81EA8F, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1e)

                fix_ptr = _find_obj_in_obj_table(0x1F0FB518, ptr, size)
                _set_platform_state(ctx, fix_ptr, 0)

                fix_ptr = _find_obj_in_obj_table(0x1F0FB519, ptr, size)
                _set_platform_state(ctx, fix_ptr, 0)

                fix_ptr = _find_obj_in_obj_table(0x1F0FB51A, ptr, size)
                _set_platform_state(ctx, fix_ptr, 0)

                fix_ptr = _find_obj_in_obj_table(0x1F0FB51B, ptr, size)
                _set_platform_state(ctx, fix_ptr, 0)

            else:  # Keys not collected, make sure the gate is closed
                fix_ptr = _find_obj_in_obj_table(0xD2c0b719, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1e)

                fix_ptr = _find_obj_in_obj_table(0x7D81EA8F, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1f)

                fix_ptr = _find_obj_in_obj_table(0x1F0FB518, ptr, size)
                _set_platform_state(ctx, fix_ptr, 1)

                fix_ptr = _find_obj_in_obj_table(0x1F0FB519, ptr, size)
                _set_platform_state(ctx, fix_ptr, 1)

                fix_ptr = _find_obj_in_obj_table(0x1F0FB51A, ptr, size)
                _set_platform_state(ctx, fix_ptr, 1)

                fix_ptr = _find_obj_in_obj_table(0x1F0FB51B, ptr, size)
                _set_platform_state(ctx, fix_ptr, 1)


async def update_key_items(ctx: NO100FContext):
    count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR) % 0x10
    ctx.CitM1_key = count

    count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR) // 0x10
    ctx.hedge_key = count

    count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 1) % 0x10
    ctx.fish_key = count

    count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 1) // 0x10
    ctx.WYitC2_keys = count

    count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 2) % 0x10
    ctx.WYitC3_keys = count

    count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 2) // 0x10
    ctx.MCaC_keys = count

    count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 3) % 0x10
    ctx.FCfS_keys = count

    count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 3) // 0x10
    ctx.TSfaGP_keys = count

    count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 4) % 0x10
    ctx.GDDitT1_key = count

    count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 4) // 0x10
    ctx.GDDitT3_keys = count

    count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 5) % 0x10
    ctx.CitM4_key = count

    count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 5) // 0x10
    ctx.MyM2_keys = count

    count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 6) % 0x10
    ctx.CfsG1_keys = count

    count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 6) // 0x10
    ctx.PitA2_keys = count

    count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 7) % 0x10
    ctx.ADaSK2_keys = count

    count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 7) // 0x10
    ctx.CCitH2_keys = count

    count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 8) % 0x10
    ctx.CCitH3_keys = count

    count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 8) // 0x10
    ctx.GAU1_key = count

    count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 9) % 0x10
    ctx.GAU2_keys = count

    count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 9) // 0x10
    ctx.DLDS2_keys = count

    count = dolphin_memory_engine.read_byte(KEY_COUNT_ADDR + 10) % 0x10
    ctx.SYTS1_keys = count


async def give_items(ctx: NO100FContext):
    if not ctx.use_keys == 0:
        await update_key_items(ctx)
    expected_idx = dolphin_memory_engine.read_word(EXPECTED_INDEX_ADDR)
    # we need to loop some items
    for item, idx in ctx.items_received_2:
        if check_control_owner(ctx, lambda owner: owner == 0):
            return
        if expected_idx <= idx:
            item_id = item.item
            _give_item(ctx, item_id)
            dolphin_memory_engine.write_word(EXPECTED_INDEX_ADDR, idx + 1)
            await asyncio.sleep(.01)  # wait a bit for values to update


def _check_pickup_state(ctx: NO100FContext, obj_ptr: int):
    if not _is_ptr_valid(obj_ptr + 0xec):
        return False
    obj_state = dolphin_memory_engine.read_word(obj_ptr + 0xec)
    return obj_state & 0x08 > 0 and obj_state & 0x37 == 0


def _set_pickup_state(ctx: NO100FContext, obj_ptr: int, state: int):
    if not _is_ptr_valid(obj_ptr + 0xef):
        return False
    dolphin_memory_engine.write_byte(obj_ptr + 0xef, state)


async def _check_objects_by_id(ctx: NO100FContext, locations_checked: set, id_table: dict, check_cb: Callable):
    scene = dolphin_memory_engine.read_bytes(CUR_SCENE_ADDR, 0x4)

    if scene == b'h001':
        scene = b'H001'

    ptr = dolphin_memory_engine.read_word(SCENE_OBJ_LIST_PTR_ADDR)
    if not _is_ptr_valid(ptr):
        return
    size = dolphin_memory_engine.read_word(SCENE_OBJ_LIST_SIZE_ADDR)

    for k, v in id_table.items():
        if k in locations_checked:
            continue
        if v[0] is not None and v[0] != scene:
            continue
        for i in range(1, len(v)):
            obj_ptr = _find_obj_in_obj_table(v[i], ptr, size)
            if obj_ptr is None: break
            if obj_ptr == -1: continue  

            # Shovel Fix
            if v[1] == Upgrades.ShovelPower.value:  # Only do this for the Shovel Power Up in H001

                fix_ptr = _find_obj_in_obj_table(0xD5159008, ptr, size)
                if fix_ptr is None: break

                dolphin_memory_engine.write_byte(fix_ptr + 0x7, 0x1d)  # Force Shovel Pickup Availability

            # Slippers Fix
            if v[1] == Upgrades.SlippersPower.value:  # Only do this for the Slippers Powerup in E002

                fix_ptr = _find_obj_in_obj_table(0xF08C8F07, ptr, size)
                if fix_ptr is None: break

                _set_counter_value(ctx, fix_ptr, 0xa0)  # Force Counter to large value

            # Black Knight Fix
            if v[1] == Upgrades.BootsPower.value:  #Only do this for the Boots Power Up in O008

                fix_ptr = _find_obj_in_obj_table(0x7B9BA1C7, ptr, size)
                if fix_ptr is None: break

                BK_Alive = dolphin_memory_engine.read_byte(fix_ptr + 0x15)  #Check Fight Over Counter
                if BK_Alive == 0:  #Is he dead?
                    locations_checked.add(k)
                    ctx.post_boss = True
                    boss_kills = dolphin_memory_engine.read_byte(BOSS_KILLS_ADDR)
                    boss_kills += 1
                    dolphin_memory_engine.write_byte(BOSS_KILLS_ADDR, boss_kills)

            # Green Ghost Fix
            if v[1] == Upgrades.UmbrellaPower.value:  # Only do this for the Umbrella Power Up in G009

                # Fix Check Itself
                fix_ptr = _find_obj_in_obj_table(0xB6C6E412, ptr, size)
                if fix_ptr is None: break

                GG_Defeated = dolphin_memory_engine.read_byte(fix_ptr + 0x16)
                if GG_Defeated == 0x1f:
                    locations_checked.add(k)
                    ctx.post_boss = True
                    boss_kills = dolphin_memory_engine.read_byte(BOSS_KILLS_ADDR)
                    boss_kills += 1
                    dolphin_memory_engine.write_byte(BOSS_KILLS_ADDR, boss_kills)

                # Fix Broken Fight Trigger
                fix_ptr1 = _find_obj_in_obj_table(0x060E343c, ptr, size)
                if fix_ptr1 is None: break

                dolphin_memory_engine.write_byte(fix_ptr1 + 0x7, 0x1d)  # Re-enable Key Counter
                GG_Alive = dolphin_memory_engine.read_byte(fix_ptr + 0x14)

                fix_ptr2 = _find_obj_in_obj_table(0xA11635BD, ptr, size)
                if fix_ptr2 is None: break

                if GG_Alive == 0 and GG_Defeated == 0x1b:  # Green Ghost has not been defeated, and he is not yet present
                    dolphin_memory_engine.write_byte(fix_ptr2 + 0x7, 0x1f)
                else:
                    dolphin_memory_engine.write_byte(fix_ptr2 + 0x7, 0x1e)

            # Red Beard Fix
            if v[1] == Upgrades.GumPower.value:  # Only do this for the Gum Powerup in W028

                fix_ptr = _find_obj_in_obj_table(0x5A3B5C98, ptr, size)
                if fix_ptr is None: break

                RB_Alive = dolphin_memory_engine.read_byte(fix_ptr + 0x15)  # Check Fight Over Counter
                if RB_Alive == 0:  # Is he dead?
                    locations_checked.add(k)
                    ctx.post_boss = True
                    boss_kills = dolphin_memory_engine.read_byte(BOSS_KILLS_ADDR)
                    boss_kills += 1
                    dolphin_memory_engine.write_byte(BOSS_KILLS_ADDR, boss_kills)

            if scene == b'P002':
                if v[1] == Keys.KEY1.value:

                    fix_ptr = _find_obj_in_obj_table(Keys.KEY1.value)
                    if fix_ptr is None: break

                    key_gone = _check_platform_state(ctx, fix_ptr)
                    if key_gone == 0:  # Key is Gone, but check has not been sent
                        locations_checked.add(k)

                if v[1] == Keys.KEY2.value:

                    fix_ptr = _find_obj_in_obj_table(Keys.KEY2.value)
                    if fix_ptr is None: break

                    key_gone = _check_platform_state(ctx, fix_ptr)
                    if key_gone == 0:  # Key is Gone, but check has not been sent
                        locations_checked.add(k)

                if v[1] == Keys.KEY3.value:

                    fix_ptr = _find_obj_in_obj_table(Keys.KEY3.value)
                    if fix_ptr is None: break

                    key_gone = _check_platform_state(ctx, fix_ptr)
                    if key_gone == 0:  # Key is Gone, but check has not been sent
                        locations_checked.add(k)

                if v[1] == Keys.KEY4.value:

                    fix_ptr = _find_obj_in_obj_table(Keys.KEY4.value)
                    if fix_ptr is None: break

                    key_gone = _check_platform_state(ctx, fix_ptr)
                    if key_gone == 0:  # Key is Gone, but check has not been sent
                        locations_checked.add(k)


            if check_cb(ctx, obj_ptr):
                locations_checked.add(k)

                # Lampshade/Slippers Fix
                if v[1] == Upgrades.SlippersPower.value:  # We are checking the slipper power up
                    locations_checked.add(k + 1)  # Add the lampshade check as well

                    fix_ptr = _find_obj_in_obj_table(0xF08C8F07, ptr, size)
                    _set_counter_value(ctx, fix_ptr, 0x1)  # Force Counter to 1

                break


async def _check_upgrades(ctx: NO100FContext, locations_checked: set):
    await _check_objects_by_id(ctx, locations_checked, UPGRADES_PICKUP_IDS, _check_pickup_state)


async def _check_monstertokens(ctx: NO100FContext, locations_checked: set):
    await _check_objects_by_id(ctx, locations_checked, MONSTERTOKENS_PICKUP_IDS, _check_pickup_state)


async def _check_keys(ctx: NO100FContext, locations_checked: set):
    await _check_objects_by_id(ctx, locations_checked, KEYS_PICKUP_IDS, _check_pickup_state)


async def _check_warpgates(ctx: NO100FContext, locations_checked: set):
    await _check_warpgates_location(ctx, locations_checked, WARPGATE_PICKUP_IDS)


async def _check_snacks(ctx: NO100FContext, locations_checked: set):
    await _check_objects_by_id(ctx, locations_checked, SNACK_PICKUP_IDS, _check_pickup_state)


async def _check_warpgates_location(ctx: NO100FContext, locations_checked: set, id_table : dict):
    scene = dolphin_memory_engine.read_bytes(CUR_SCENE_ADDR, 0x4)
    ptr = dolphin_memory_engine.read_word(SCENE_OBJ_LIST_PTR_ADDR)
    if not _is_ptr_valid(ptr):
        return
    size = dolphin_memory_engine.read_word(SCENE_OBJ_LIST_SIZE_ADDR)

    for k, v in id_table.items():
        if k in locations_checked:
            continue
        if v[0] is not None and v[0] != scene:
            continue
        bit = k - 300 - base_id
        value = dolphin_memory_engine.read_word(WARP_ADDR + (12 * bit))
        if value == 1:
            locations_checked.add(k)

    await load_warp_gates(ctx)

async def enable_map_warping(ctx: NO100FContext):
    scene = dolphin_memory_engine.read_bytes(CUR_SCENE_ADDR, 0x4)
    ptr = dolphin_memory_engine.read_word(SCENE_OBJ_LIST_PTR_ADDR)
    if not _is_ptr_valid(ptr):
        return
    size = dolphin_memory_engine.read_word(SCENE_OBJ_LIST_SIZE_ADDR)

    fix_ptr = _find_obj_in_obj_table(0x8542BAD4, ptr, size)
    if not fix_ptr == None:
        for i in range(18):
            if i == 6:
                saved_warps = dolphin_memory_engine.read_word(SAVED_WARP_ADDR)
                if not saved_warps & 2**8:
                    _set_trigger_state(ctx, fix_ptr + (0x14 * i), 0x1c)
                else:
                    _set_trigger_state(ctx, fix_ptr + (0x14 * i), 0x1d)

            else:
                _set_trigger_state(ctx, fix_ptr + (0x14 * i), 0x1d)

    fix_ptr = _find_obj_in_obj_table(0x6887e731, ptr, size)
    if not fix_ptr == None:
        for i in range(7):
            _set_trigger_state(ctx, fix_ptr + (0x14 * i), 0x1d)
        if ctx.use_warpgates:
            saved_warps = dolphin_memory_engine.read_word(SAVED_WARP_ADDR)
            if ((not saved_warps & 2**8) and saved_warps & 2**9):  # Give G005 Warp if we have received G008 as an item (Thanks Heavy Iron)
                fix_ptr = _find_obj_in_obj_table(0x78A1C3B8, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1c)
                dolphin_memory_engine.write_word(0x801B7F54, 1)
            if (saved_warps & 2**8 and (not saved_warps & 2**9)):  # Prevent G008 Warp if we have received G005 as an item (Thanks Heavy Iron)
                fix_ptr = _find_obj_in_obj_table(0x6B2EA611, ptr, size)
                _set_trigger_state(ctx, fix_ptr, 0x1c)

async def apply_level_fixes(ctx: NO100FContext):
    scene = dolphin_memory_engine.read_bytes(CUR_SCENE_ADDR, 0x4)
    ptr = dolphin_memory_engine.read_word(SCENE_OBJ_LIST_PTR_ADDR)
    if not _is_ptr_valid(ptr):
        return
    size = dolphin_memory_engine.read_word(SCENE_OBJ_LIST_SIZE_ADDR)

    dolphin_memory_engine.write_word(MAP_ADDR, 0x1)  # Force the Map Into Inventory
    if scene == b'I001':
        upgrades = dolphin_memory_engine.read_word(UPGRADE_INVENTORY_ADDR)
        if not upgrades & 2 ** 13:  # Player does not have the shovel, give them a fake
            upgrades += (2 ** 13 + 2 ** 7)
            dolphin_memory_engine.write_word(UPGRADE_INVENTORY_ADDR, upgrades)

        fix_ptr = _find_obj_in_obj_table(0x22B1A6E6, ptr, size)  # Holly Trigger #1
        _set_trigger_state(ctx, fix_ptr, 0x1c)

        fix_ptr = _find_obj_in_obj_table(0xC0E867E2, ptr, size)  # Holly Trigger #2
        _set_trigger_state(ctx, fix_ptr, 0x1e)

        fix_ptr = _find_obj_in_obj_table(0xFA854786, ptr, size)  # Holly Collision and Visibility Disabled
        _set_platform_collision_state(ctx, fix_ptr, 0)
        _set_platform_state(ctx, fix_ptr, 0)

        if _is_scene_visited(b'R001'):
            fix_ptr = _find_obj_in_obj_table(0x4f81e846, ptr, size)  # Doorway Trigger
            _set_trigger_state(ctx, fix_ptr, 0x1d)

            fix_ptr = _find_obj_in_obj_table(0xDE90259F, ptr, size)  # Text Trigger
            _set_trigger_state(ctx, fix_ptr, 0x1c)

        if _is_scene_visited(b'S005'):
            fix_ptr = _find_obj_in_obj_table(0xB0d216d1, ptr, size)  # Load Trigger
            _set_trigger_state(ctx, fix_ptr, 0x1d)

            fix_ptr = _find_obj_in_obj_table(0xc402cded, ptr, size)  # Disable Armoire Collision and Visibility
            _set_platform_collision_state(ctx, fix_ptr, 0)
            _set_platform_state(ctx, fix_ptr, 0x1c)

    if scene == b'E001':
        upgrades = dolphin_memory_engine.read_word(UPGRADE_INVENTORY_ADDR)
        if not upgrades & 2 ** 13:  # Player does not have the shovel, give them a fake
            upgrades += (2 ** 13 + 2 ** 7)
            dolphin_memory_engine.write_word(UPGRADE_INVENTORY_ADDR, upgrades)

        if upgrades & 2 ** 7:  # Player has a fake shovel, don't let them dig
            fix_ptr = _find_obj_in_obj_table(0xb37f36c7, ptr, size)
            _set_trigger_state(ctx, fix_ptr, 0x1c)

    if scene == b'F001':
        upgrades = dolphin_memory_engine.read_word(UPGRADE_INVENTORY_ADDR)
        if not upgrades & 2 ** 13:  # Player does not have the shovel, give them a fake
            upgrades += (2 ** 13 + 2 ** 7)
            dolphin_memory_engine.write_word(UPGRADE_INVENTORY_ADDR, upgrades)

    if scene == b'H002':
        upgrades = dolphin_memory_engine.read_word(UPGRADE_INVENTORY_ADDR)
        if not upgrades & 2 ** 13:  # Player does not have the shovel, give them a fake
            upgrades += (2 ** 13 + 2 ** 7)
            dolphin_memory_engine.write_word(UPGRADE_INVENTORY_ADDR, upgrades)

    if scene == b'H003':
        upgrades = dolphin_memory_engine.read_word(UPGRADE_INVENTORY_ADDR)
        if not upgrades & 2 ** 13:  # Player does not have the shovel, give them a fake
            upgrades += (2 ** 13 + 2 ** 7)
            dolphin_memory_engine.write_word(UPGRADE_INVENTORY_ADDR, upgrades)

    if not (scene == b'I001' or scene == b'E001' or scene == b'F001' or scene == b'H002' or scene == b'H003'):
        upgrades = dolphin_memory_engine.read_word(UPGRADE_INVENTORY_ADDR)
        if upgrades & 2 ** 7:  # Player has a fake shovel, get rid of it
            upgrades -= (2 ** 7 + 2 ** 13)
            dolphin_memory_engine.write_word(UPGRADE_INVENTORY_ADDR, upgrades)

    if scene == b'h001':
        if ctx.use_warpgates and not ctx.use_snacks:
            cur_snacks = dolphin_memory_engine.read_word(SNACK_COUNT_ADDR)
            if cur_snacks == 0:
                dolphin_memory_engine.write_word(SNACK_COUNT_ADDR, 400)

    if scene == b'H001' or b'h001':

        # Clear Monster Gallery Snack Gate
        fix_ptr = _find_obj_in_obj_table(0x7E8E16F5, ptr, size)
        if not fix_ptr == None and not ctx.use_snacks:
            _set_platform_state(ctx, fix_ptr, 0)
            fix_ptr = _find_obj_in_obj_table(0xD7924F8A, ptr, size)
            _set_trigger_state(ctx, fix_ptr, 0x1f)

        if ctx.use_keys == 0:
            fix_ptr = _find_obj_in_obj_table(0xBBFA4948, ptr, size)
            if not fix_ptr == None:
                if _check_pickup_state(ctx, fix_ptr):  #The Hedge key is collected, open the gate
                    fix_ptr = _find_obj_in_obj_table(0xC20224F3, ptr, size)
                    _set_platform_state(ctx, fix_ptr, 0)

                    fix_ptr = _find_obj_in_obj_table(0xE8B3FF9B, ptr, size)
                    _set_trigger_state(ctx, fix_ptr, 0x1c)

                    fix_ptr = _find_obj_in_obj_table(0xD72B66B7, ptr, size)
                    _set_trigger_state(ctx, fix_ptr, 0x1d)

            fix_ptr = _find_obj_in_obj_table(0xBB82B3B3, ptr, size)
            if not fix_ptr == None:
                if _check_pickup_state(ctx, fix_ptr):  #The Fishing key is collected, open the gate
                    fix_ptr = _find_obj_in_obj_table(0x42A3128E, ptr, size)
                    _set_platform_state(ctx, fix_ptr, 0)

    if scene == b'R021':
        if _is_scene_visited(b'R003'):
            fix_ptr = _find_obj_in_obj_table(0xcbd0A98D, ptr, size)  # Holly Collision and Visibility Disabled
            _set_platform_collision_state(ctx, fix_ptr, 0)
            _set_platform_state(ctx, fix_ptr, 0)

    if scene == b"P003":
        fix_ptr = _find_obj_in_obj_table(0x0A1EFB92, ptr, size)
        if not fix_ptr == None:
            if ctx.previous_scene == b'P004' and _check_platform_state(ctx, fix_ptr) == 1:
                dolphin_memory_engine.write_word(HEALTH_ADDR, 5)    # Give scooby health to teleport out if entering creepy backwards

    # Credits Location
    if scene == b"S005":  #We are in the final room

        if not ctx.completion_goal == 0:
            fix_ptr = _find_obj_in_obj_table(0x79f90e17, ptr, size)
            if fix_ptr is not None:
                in_arena = dolphin_memory_engine.read_byte(fix_ptr + 0x7)
                fix_ptr = _find_obj_in_obj_table(0x11498CF8, ptr, size)
                cutscene_played = dolphin_memory_engine.read_byte(fix_ptr + 0x23)

                if cutscene_played == 2:
                    fix_ptr = _find_obj_in_obj_table(0x2b2cea8a, ptr, size)
                    _set_trigger_state(ctx, fix_ptr, 0x1e)

                conditions_met = False
                bossesKilled = dolphin_memory_engine.read_byte(BOSS_KILLS_ADDR)
                tokens = dolphin_memory_engine.read_word(MONSTER_TOKEN_INVENTORY_ADDR)
                snacks = dolphin_memory_engine.read_word(STORED_SNACK_ADDR)
                sum_tokens = 0
                for i in range(21):
                    if tokens & 2 ** i == 2 ** i:
                        sum_tokens += 1

                if ctx.completion_goal == 1:    # Fixes for all bosses
                    if bossesKilled >= ctx.boss_count:
                        conditions_met = True

                if ctx.completion_goal == 2:
                    if sum_tokens >= ctx.token_count:
                        conditions_met = True

                if ctx.completion_goal == 3:
                    if bossesKilled >= ctx.boss_count and sum_tokens >= ctx.token_count:
                        conditions_met = True

                if ctx.completion_goal == 4:
                    if snacks >= ctx.snack_count:
                        conditions_met = True

                if ctx.completion_goal == 5:
                    if snacks >= ctx.snack_count and bossesKilled >= ctx.boss_count:
                        conditions_met = True

                if ctx.completion_goal == 6:
                    if snacks >= ctx.snack_count and sum_tokens >= ctx.token_count:
                        conditions_met = True

                if ctx.completion_goal == 7:
                    if bossesKilled >= ctx.boss_count and sum_tokens >= ctx.token_count and snacks >= ctx.snack_count:
                        conditions_met = True

                if conditions_met and in_arena == 0x1d and cutscene_played == 0:
                    fix_ptr = _find_obj_in_obj_table(0x2b2cea8a, ptr, size)
                    _set_trigger_state(ctx, fix_ptr, 0x1f)
                elif not conditions_met:
                    fix_ptr = _find_obj_in_obj_table(0x2b2cea8a, ptr, size)
                    _set_trigger_state(ctx, fix_ptr, 0x1e)
                    fix_ptr = _find_obj_in_obj_table(0x78CFEF58, ptr, size)
                    _set_trigger_state(ctx, fix_ptr, 0x1c)
                    fix_ptr = _find_obj_in_obj_table(0x3C433393, ptr, size)
                    _set_trigger_state(ctx, fix_ptr, 0x1c)
                    fix_ptr = _find_obj_in_obj_table(0x0C413492, ptr, size)
                    _set_platform_state(ctx, fix_ptr, 0)
                    fix_ptr = _find_obj_in_obj_table(0x9AA96044, ptr, size)
                    _set_platform_state(ctx, fix_ptr, 0)
                    fix_ptr = _find_obj_in_obj_table(0xCF095CD7, ptr, size)
                    _set_platform_state(ctx, fix_ptr, 0)
                    fix_ptr = _find_obj_in_obj_table(0x1480DF86, ptr, size)
                    _set_platform_state(ctx, fix_ptr, 0)
                    fix_ptr = _find_obj_in_obj_table(0xD046F599, ptr, size)
                    _set_platform_state(ctx, fix_ptr, 0)
                    fix_ptr = _find_obj_in_obj_table(0x08E9D051, ptr, size)
                    _set_platform_state(ctx, fix_ptr, 0)

                if not conditions_met and in_arena == 0x1c:
                    fix_ptr = _find_obj_in_obj_table(0x2854c118, ptr, size)
                    _set_platform_collision_state(ctx, fix_ptr, 0)
                    _set_platform_state(ctx, fix_ptr, 0)

        if not ctx.finished_game:  # We have not finished
            fix_ptr = _find_obj_in_obj_table(0x21D3EDA4, ptr, size)
            if fix_ptr is not None:
                MM_Alive = dolphin_memory_engine.read_byte(fix_ptr + 0x15)
                if MM_Alive == 0:
                    print("send done")
                    await ctx.send_msgs([
                        {"cmd": "StatusUpdate",
                         "status": 30}
                    ])
                    ctx.finished_game = True
                    ctx.post_boss = True


async def check_locations(ctx: NO100FContext):
    await _check_upgrades(ctx, ctx.locations_checked)
    if ctx.use_tokens:
        await _check_monstertokens(ctx, ctx.locations_checked)
    if not ctx.use_keys == 0:
        await _check_keys(ctx, ctx.locations_checked)
    if ctx.use_warpgates:
        await _check_warpgates(ctx, ctx.locations_checked)
    if ctx.use_snacks:
        await _check_snacks(ctx, ctx.locations_checked)

    # ignore already in server state
    locations_checked = ctx.locations_checked.difference(ctx.checked_locations)
    if locations_checked:
        await ctx.send_msgs([
            {"cmd": "LocationChecks",
             "locations": locations_checked}
        ])
        print([ctx.location_names[location] for location in locations_checked])


async def check_alive(ctx: NO100FContext):
    cur_health = dolphin_memory_engine.read_word(HEALTH_ADDR)
    return not (cur_health <= 0 or check_control_owner(ctx, lambda owner: owner == 0))


async def check_death(ctx: NO100FContext):
    cur_health = dolphin_memory_engine.read_word(HEALTH_ADDR)

    if cur_health > 0:
        ctx.forced_death = False

    if cur_health <= 0 and not ctx.forced_death and not ctx.post_boss:
        if dolphin_memory_engine.read_bytes(CUR_SCENE_ADDR,
                                            0x4) == b'F003':  # Avoid Creepy Early Trigger causing erroneous DL Sends
            await asyncio.sleep(3)
            if dolphin_memory_engine.read_bytes(CUR_SCENE_ADDR, 0x4) != b'F003':
                return
        if not ctx.has_send_death and time.time() >= ctx.last_death_link + 3:
            ctx.has_send_death = True
            await ctx.send_death("NO100F")
    else:
        ctx.has_send_death = False


def check_ingame(ctx: NO100FContext, ignore_control_owner: bool = False) -> bool:
    scene = dolphin_memory_engine.read_bytes(CUR_SCENE_ADDR, 0x4)
    if scene not in valid_scenes:
        return False
    update_current_scene(ctx, scene.decode('ascii'))
    return True


def update_current_scene(ctx: NO100FContext, scene: str):
    if not ctx.slot and not ctx.auth:
        return
    if ctx.current_scene_key is None or ctx.current_scene_key not in ctx.stored_data:
        return
    if ctx.stored_data[ctx.current_scene_key] == scene:
        return
    Utils.async_start(ctx.send_msgs([{
        "cmd": "Set",
        "key": ctx.current_scene_key,
        "default": None,
        "want_reply": True,
        "operations": [{
            "operation": "replace",
            "value": scene,
        }],
    }]))


def check_control_owner(ctx: NO100FContext, check_cb: Callable[[int], bool]) -> bool:
    owner = dolphin_memory_engine.read_word(PLAYER_CONTROL_OWNER)
    return check_cb(owner)


async def save_warp_gates(ctx: NO100FContext):
    warp_gate_map = 0
    await asyncio.sleep(1)
    for i in range(26):
        cur_gate = dolphin_memory_engine.read_word(WARP_ADDR + (12 * i))
        if cur_gate == 1:
            warp_gate_map += 2 ** i

    if warp_gate_map & 0x400 == 0:
        warp_gate_map += 0x400

    dolphin_memory_engine.write_word(SAVED_WARP_ADDR, warp_gate_map)


async def load_warp_gates(ctx: NO100FContext):
    warp_gates = dolphin_memory_engine.read_word(SAVED_WARP_ADDR)
    if warp_gates & 0x400 == 0:
        warp_gates += 0x400
        
    dolphin_memory_engine.write_word(SAVED_WARP_ADDR, warp_gates)

    for i in range(26):
        if warp_gates & 2 ** i == 2 ** i:
            dolphin_memory_engine.write_word(WARP_ADDR + (12 * i), 1)
        else:
            dolphin_memory_engine.write_word(WARP_ADDR + (12 * i), 0)


async def force_death(ctx: NO100FContext):
    cur_health = dolphin_memory_engine.read_word(HEALTH_ADDR)

    if cur_health == 69 and not ctx.post_boss:  # Funny number, but also good luck accidentally setting your health this high
        ctx.forced_death = True
        dolphin_memory_engine.write_word(HEALTH_ADDR, 0)


def validate_save(ctx: NO100FContext) -> bool:
    saved_slot_bytes = dolphin_memory_engine.read_bytes(SAVED_SLOT_NAME_ADDR, 0x40).strip(b'\0')
    slot_bytes = dolphin_memory_engine.read_bytes(SLOT_NAME_ADDR, 0x40).strip(b'\0')
    saved_seed_bytes = dolphin_memory_engine.read_bytes(SAVED_SEED_ADDR, 0x10).strip(b'\0')
    seed_bytes = dolphin_memory_engine.read_bytes(SEED_ADDR, 0x10).strip(b'\0')
    if len(slot_bytes) > 0 and len(seed_bytes) > 0:
        if len(saved_slot_bytes) == 0 and len(saved_seed_bytes) == 0:
            # write info to save
            dolphin_memory_engine.write_bytes(SAVED_SLOT_NAME_ADDR, slot_bytes)
            dolphin_memory_engine.write_bytes(SAVED_SEED_ADDR, seed_bytes)
            return True
        elif slot_bytes == saved_slot_bytes and seed_bytes == saved_seed_bytes:
            return True
    return False


async def dolphin_sync_task(ctx: NO100FContext):
    logger.info("Starting Dolphin connector. Use /dolphin for status information")
    while not ctx.exit_event.is_set():
        try:
            if dolphin_memory_engine.is_hooked() and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                if not check_ingame(ctx):
                    # reset AP values when on main menu
                    if _check_cur_scene(ctx, b'MNU3'):
                        ctx.current_scene = b'MNU3'
                        for i in range(0, 0x80, 0x4):
                            cur_val = dolphin_memory_engine.read_word(EXPECTED_INDEX_ADDR + i)
                            if cur_val != 0:
                                dolphin_memory_engine.write_word(EXPECTED_INDEX_ADDR + i, 0)

                    await asyncio.sleep(.1)
                    continue
                if ctx.slot:
                    if not validate_save(ctx):
                        logger.info(CONNECTION_REFUSED_SAVE_STATUS)
                        ctx.dolphin_status = CONNECTION_REFUSED_SAVE_STATUS
                        dolphin_memory_engine.un_hook()
                        await ctx.disconnect()
                        await asyncio.sleep(5)
                        continue
                    ctx.current_scene_key = f"NO100F_current_scene_T{ctx.team}_P{ctx.slot}"
                    ctx.set_notify(ctx.current_scene_key)
                    if not _check_cur_scene(ctx, ctx.current_scene):
                        scene = dolphin_memory_engine.read_bytes(CUR_SCENE_ADDR, 4)
                        ctx.previous_scene = ctx.current_scene
                        ctx.current_scene = scene
                    if "DeathLink" in ctx.tags:
                        await check_death(ctx)
                    await give_items(ctx)
                    await check_locations(ctx)
                    await apply_level_fixes(ctx)
                    if not ctx.use_warpgates:
                        if ctx.previous_scene == b'MNU3':
                            await load_warp_gates(ctx)
                        else:
                            await save_warp_gates(ctx)
                    if not ctx.use_keys == 0:
                        await apply_key_fixes(ctx)
                    if ctx.use_snacks:
                        cur_snacks = dolphin_memory_engine.read_word(STORED_SNACK_ADDR)
                        dolphin_memory_engine.write_word(SNACK_COUNT_ADDR, cur_snacks)
                    await force_death(ctx)
                    await enable_map_warping(ctx)

                    if(ctx.use_speedster):
                        dolphin_memory_engine.write_word(0x80235084, 0xFFFF)

                    if not (_check_cur_scene(ctx, b'O008') or _check_cur_scene(ctx, b'S005') or
                            _check_cur_scene(ctx, b'G009') or _check_cur_scene(ctx, b'W028')):

                        ctx.post_boss = False
                else:
                    if not ctx.auth:
                        ctx.auth = dolphin_memory_engine.read_bytes(SLOT_NAME_ADDR, 0x40).decode('utf-8').strip(
                            '\0')
                        if ctx.auth == '\x02\x00\x00\x00\x04\x00\x00\x00\x02\x00\x00\x00\x04\x00\x00\x00\x02\x00\x00' \
                                       '\x00\x02\x00\x00\x00\x04\x00\x00\x00\x04':
                            logger.info("Vanilla game detected. Please load the patched game.")
                            ctx.dolphin_status = CONNECTION_REFUSED_GAME_STATUS
                            ctx.awaiting_rom = False
                            dolphin_memory_engine.un_hook()
                            await ctx.disconnect()
                            await asyncio.sleep(5)
                    if ctx.awaiting_rom:
                        await ctx.server_auth()
                await asyncio.sleep(.5)
            else:
                if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                    logger.info("Connection to Dolphin lost, reconnecting...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                logger.info("Attempting to connect to Dolphin")
                dolphin_memory_engine.hook()
                if dolphin_memory_engine.is_hooked():
                    if dolphin_memory_engine.read_bytes(0x80000000, 6) == b'GIHE78':
                        logger.info(CONNECTION_CONNECTED_STATUS)
                        ctx.dolphin_status = CONNECTION_CONNECTED_STATUS
                        ctx.locations_checked = set()
                    else:
                        logger.info(CONNECTION_REFUSED_GAME_STATUS)
                        ctx.dolphin_status = CONNECTION_REFUSED_GAME_STATUS
                        dolphin_memory_engine.un_hook()
                        await asyncio.sleep(1)
                else:
                    logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                    await ctx.disconnect()
                    await asyncio.sleep(5)
                    continue
        except Exception:
            dolphin_memory_engine.un_hook()
            logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
            logger.error(traceback.format_exc())
            ctx.dolphin_status = CONNECTION_LOST_STATUS
            await ctx.disconnect()
            await asyncio.sleep(5)
            continue


async def patch_and_run_game(ctx: NO100FContext, patch_file):
    try:
        result_path = os.path.splitext(patch_file)[0] + NO100FContainer.result_file_ending
        with zipfile.ZipFile(patch_file, 'r') as patch_archive:
            if not NO100FContainer.check_version(patch_archive):
                logger.error(
                    "apNO100F version doesn't match this client.  Make sure your generator and client are the same")
                raise Exception("apNO100F version doesn't match this client.")

        # check hash
        NO100FContainer.check_hash()

        shutil.copy(NO100FContainer.get_rom_path(), result_path)
        await NO100FContainer.apply_binary_changes(zipfile.ZipFile(patch_file, 'r'), result_path)

        logger.info('--patching success--')
        if sys.platform == "win32":
            os.startfile(result_path)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, result_path])

    except Exception as msg:
        logger.info(msg, extra={'compact_gui': True})
        logger.debug(traceback.format_exc())
        ctx.gui_error('Error', msg)


def main(connect=None, password=None, patch_file=None):
    # Text Mode to use !hint and such with games that have no text entry
    Utils.init_logging("NO100FClient")

    async def _main(connect, password, patch_file):
        ctx = NO100FContext(connect, password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        ctx.patch_task = None
        if patch_file:
            ext = os.path.splitext(patch_file)[1]
            if ext == NO100FContainer.patch_file_ending:
                logger.info("apNO100F file supplied, beginning patching process...")
                ctx.patch_task = asyncio.create_task(patch_and_run_game(ctx, patch_file), name="PatchGame")
            elif ext == NO100FContainer.result_file_ending:
                if sys.platform == "win32":
                    os.startfile(patch_file)
                else:
                    opener = "open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, patch_file])
            else:
                logger.warning(f"Unknown patch file extension {ext}")

        if ctx.patch_task:
            await ctx.patch_task

        await asyncio.sleep(1)

        ctx.dolphin_sync_task = asyncio.create_task(dolphin_sync_task(ctx), name="DolphinSync")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.dolphin_sync_task:
            await asyncio.sleep(3)
            await ctx.dolphin_sync_task

    import colorama

    colorama.init()
    asyncio.run(_main(connect, password, patch_file))
    colorama.deinit()


if __name__ == '__main__':
    parser = get_base_parser()
    parser.add_argument('patch_file', default="", type=str, nargs="?",
                        help='Path to an .apno100f patch file')
    args = parser.parse_args()
    main(args.connect, args.password, args.patch_file)
