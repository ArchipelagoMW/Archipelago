import logging
import struct
import time
import typing
import uuid
from struct import unpack, pack
from collections import defaultdict
import random

from MultiServer import mark_raw
from NetUtils import ClientStatus, color
from Utils import async_start
from worlds.AutoSNIClient import SNIClient
from .Locations import boss_locations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from SNIClient import SNIClientCommandProcessor, SNIContext

snes_logger = logging.getLogger("SNES")

# FXPAK Pro protocol memory mapping used by SNI
ROM_START = 0x000000
SRAM_1_START = 0xE00000

# KDL3
KDL3_HALKEN = SRAM_1_START + 0x80F0
KDL3_NINTEN = SRAM_1_START + 0x8FF0
KDL3_ROMNAME = SRAM_1_START + 0x8100
KDL3_DEATH_LINK_ADDR = SRAM_1_START + 0x9010
KDL3_GOAL_ADDR = SRAM_1_START + 0x9012
KDL3_CONSUMABLE_FLAG = SRAM_1_START + 0x9018
KDL3_STARS_FLAG = SRAM_1_START + 0x901A
KDL3_GIFTING_FLAG = SRAM_1_START + 0x901C
KDL3_LEVEL_ADDR = SRAM_1_START + 0x9020
KDL3_IS_DEMO = SRAM_1_START + 0x5AD5
KDL3_GAME_STATE = SRAM_1_START + 0x36D0
KDL3_GAME_SAVE = SRAM_1_START + 0x3617
KDL3_LIFE_COUNT = SRAM_1_START + 0x39CF
KDL3_KIRBY_HP = SRAM_1_START + 0x39D1
KDL3_BOSS_HP = SRAM_1_START + 0x39D5
KDL3_STAR_COUNT = SRAM_1_START + 0x39D7
KDL3_LIFE_VISUAL = SRAM_1_START + 0x39E3
KDL3_HEART_STARS = SRAM_1_START + 0x53A7
KDL3_WORLD_UNLOCK = SRAM_1_START + 0x53CB
KDL3_LEVEL_UNLOCK = SRAM_1_START + 0x53CD
KDL3_CURRENT_WORLD = SRAM_1_START + 0x53CF
KDL3_CURRENT_LEVEL = SRAM_1_START + 0x53D3
KDL3_BOSS_STATUS = SRAM_1_START + 0x53D5
KDL3_INVINCIBILITY_TIMER = SRAM_1_START + 0x54B1
KDL3_MG5_STATUS = SRAM_1_START + 0x5EE4
KDL3_BOSS_BUTCH_STATUS = SRAM_1_START + 0x5EEA
KDL3_JUMPING_STATUS = SRAM_1_START + 0x5EF0
KDL3_CURRENT_BGM = SRAM_1_START + 0x733E
KDL3_SOUND_FX = SRAM_1_START + 0x7F62
KDL3_ANIMAL_FRIENDS = SRAM_1_START + 0x8000
KDL3_ABILITY_ARRAY = SRAM_1_START + 0x8020
KDL3_RECV_COUNT = SRAM_1_START + 0x8050
KDL3_HEART_STAR_COUNT = SRAM_1_START + 0x8070
KDL3_GOOEY_TRAP = SRAM_1_START + 0x8080
KDL3_SLOWNESS_TRAP = SRAM_1_START + 0x8082
KDL3_ABILITY_TRAP = SRAM_1_START + 0x8084
KDL3_GIFTING_SEND = SRAM_1_START + 0x8086
KDL3_COMPLETED_STAGES = SRAM_1_START + 0x8200
KDL3_CONSUMABLES = SRAM_1_START + 0xA000
KDL3_STARS = SRAM_1_START + 0xB000

consumable_addrs = {
    0: 14,
    1: 15,
    2: 84,
    3: 138,
    4: 139,
    5: 204,
    6: 214,
    7: 215,
    8: 224,
    9: 330,
    10: 353,
    11: 458,
    12: 459,
    13: 522,
    14: 525,
    15: 605,
    16: 606,
    17: 630,
    18: 671,
    19: 672,
    20: 693,
    21: 791,
    22: 851,
    23: 883,
    24: 971,
    25: 985,
    26: 986,
    27: 1024,
    28: 1035,
    29: 1036,
    30: 1038,
    31: 1039,
    32: 1170,
    33: 1171,
    34: 1377,
    35: 1378,
    36: 1413,
    37: 1494,
    38: 1666,
    39: 1808,
    40: 1809,
    41: 1816,
    42: 1856,
    43: 1857,
}

star_addrs = {
    0x770401: 0,
    0x770402: 1,
    0x770403: 2,
    0x770404: 3,
    0x770405: 4,
    0x770406: 5,
    0x770407: 7,
    0x770408: 8,
    0x770409: 9,
    0x77040a: 10,
    0x77040b: 11,
    0x77040c: 12,
    0x77040d: 13,
    0x77040e: 16,
    0x77040f: 17,
    0x770410: 19,
    0x770411: 20,
    0x770412: 21,
    0x770413: 22,
    0x770414: 23,
    0x770415: 24,
    0x770416: 25,
    0x770417: 26,
    0x770418: 65,
    0x770419: 66,
    0x77041a: 67,
    0x77041b: 68,
    0x77041c: 69,
    0x77041d: 70,
    0x77041e: 71,
    0x77041f: 72,
    0x770420: 73,
    0x770421: 74,
    0x770422: 76,
    0x770423: 77,
    0x770424: 78,
    0x770425: 79,
    0x770426: 80,
    0x770427: 81,
    0x770428: 82,
    0x770429: 83,
    0x77042a: 85,
    0x77042b: 86,
    0x77042c: 87,
    0x77042d: 128,
    0x77042e: 129,
    0x77042f: 130,
    0x770430: 131,
    0x770431: 132,
    0x770432: 133,
    0x770433: 134,
    0x770434: 135,
    0x770435: 136,
    0x770436: 137,
    0x770437: 140,
    0x770438: 141,
    0x770439: 142,
    0x77043a: 143,
    0x77043b: 144,
    0x77043c: 145,
    0x77043d: 146,
    0x77043e: 147,
    0x77043f: 148,
    0x770440: 149,
    0x770441: 150,
    0x770442: 151,
    0x770443: 152,
    0x770444: 153,
    0x770445: 154,
    0x770446: 155,
    0x770447: 156,
    0x770448: 157,
    0x770449: 158,
    0x77044a: 159,
    0x77044b: 160,
    0x77044c: 192,
    0x77044d: 193,
    0x77044e: 194,
    0x77044f: 195,
    0x770450: 197,
    0x770451: 198,
    0x770452: 199,
    0x770453: 200,
    0x770454: 201,
    0x770455: 203,
    0x770456: 205,
    0x770457: 206,
    0x770458: 207,
    0x770459: 208,
    0x77045a: 209,
    0x77045b: 210,
    0x77045c: 211,
    0x77045d: 212,
    0x77045e: 213,
    0x77045f: 216,
    0x770460: 217,
    0x770461: 218,
    0x770462: 219,
    0x770463: 220,
    0x770464: 221,
    0x770465: 222,
    0x770466: 225,
    0x770467: 227,
    0x770468: 228,
    0x770469: 229,
    0x77046a: 230,
    0x77046b: 231,
    0x77046c: 232,
    0x77046d: 233,
    0x77046e: 234,
    0x77046f: 235,
    0x770470: 236,
    0x770471: 257,
    0x770472: 258,
    0x770473: 259,
    0x770474: 260,
    0x770475: 261,
    0x770476: 262,
    0x770477: 263,
    0x770478: 264,
    0x770479: 265,
    0x77047a: 266,
    0x77047b: 267,
    0x77047c: 268,
    0x77047d: 270,
    0x77047e: 271,
    0x77047f: 272,
    0x770480: 273,
    0x770481: 275,
    0x770482: 276,
    0x770483: 277,
    0x770484: 278,
    0x770485: 279,
    0x770486: 280,
    0x770487: 281,
    0x770488: 282,
    0x770489: 283,
    0x77048a: 284,
    0x77048b: 285,
    0x77048c: 286,
    0x77048d: 287,
    0x77048e: 321,
    0x77048f: 322,
    0x770490: 323,
    0x770491: 324,
    0x770492: 325,
    0x770493: 326,
    0x770494: 327,
    0x770495: 328,
    0x770496: 329,
    0x770497: 332,
    0x770498: 334,
    0x770499: 335,
    0x77049a: 336,
    0x77049b: 337,
    0x77049c: 340,
    0x77049d: 341,
    0x77049e: 342,
    0x77049f: 343,
    0x7704a0: 345,
    0x7704a1: 346,
    0x7704a2: 347,
    0x7704a3: 348,
    0x7704a4: 349,
    0x7704a5: 350,
    0x7704a6: 351,
    0x7704a7: 354,
    0x7704a8: 355,
    0x7704a9: 356,
    0x7704aa: 357,
    0x7704ab: 384,
    0x7704ac: 385,
    0x7704ad: 386,
    0x7704ae: 387,
    0x7704af: 388,
    0x7704b0: 389,
    0x7704b1: 391,
    0x7704b2: 392,
    0x7704b3: 393,
    0x7704b4: 394,
    0x7704b5: 396,
    0x7704b6: 397,
    0x7704b7: 398,
    0x7704b8: 399,
    0x7704b9: 400,
    0x7704ba: 401,
    0x7704bb: 402,
    0x7704bc: 403,
    0x7704bd: 404,
    0x7704be: 449,
    0x7704bf: 450,
    0x7704c0: 451,
    0x7704c1: 453,
    0x7704c2: 454,
    0x7704c3: 455,
    0x7704c4: 456,
    0x7704c5: 457,
    0x7704c6: 460,
    0x7704c7: 461,
    0x7704c8: 462,
    0x7704c9: 463,
    0x7704ca: 464,
    0x7704cb: 465,
    0x7704cc: 466,
    0x7704cd: 467,
    0x7704ce: 468,
    0x7704cf: 513,
    0x7704d0: 514,
    0x7704d1: 515,
    0x7704d2: 516,
    0x7704d3: 517,
    0x7704d4: 518,
    0x7704d5: 519,
    0x7704d6: 520,
    0x7704d7: 521,
    0x7704d8: 523,
    0x7704d9: 524,
    0x7704da: 527,
    0x7704db: 528,
    0x7704dc: 529,
    0x7704dd: 531,
    0x7704de: 532,
    0x7704df: 533,
    0x7704e0: 534,
    0x7704e1: 535,
    0x7704e2: 536,
    0x7704e3: 537,
    0x7704e4: 576,
    0x7704e5: 577,
    0x7704e6: 578,
    0x7704e7: 579,
    0x7704e8: 580,
    0x7704e9: 582,
    0x7704ea: 583,
    0x7704eb: 584,
    0x7704ec: 585,
    0x7704ed: 586,
    0x7704ee: 587,
    0x7704ef: 588,
    0x7704f0: 589,
    0x7704f1: 590,
    0x7704f2: 591,
    0x7704f3: 592,
    0x7704f4: 593,
    0x7704f5: 594,
    0x7704f6: 595,
    0x7704f7: 596,
    0x7704f8: 597,
    0x7704f9: 598,
    0x7704fa: 599,
    0x7704fb: 600,
    0x7704fc: 601,
    0x7704fd: 602,
    0x7704fe: 603,
    0x7704ff: 604,
    0x770500: 607,
    0x770501: 608,
    0x770502: 609,
    0x770503: 610,
    0x770504: 611,
    0x770505: 612,
    0x770506: 613,
    0x770507: 614,
    0x770508: 615,
    0x770509: 616,
    0x77050a: 617,
    0x77050b: 618,
    0x77050c: 619,
    0x77050d: 620,
    0x77050e: 621,
    0x77050f: 622,
    0x770510: 623,
    0x770511: 624,
    0x770512: 625,
    0x770513: 626,
    0x770514: 627,
    0x770515: 628,
    0x770516: 629,
    0x770517: 640,
    0x770518: 641,
    0x770519: 642,
    0x77051a: 643,
    0x77051b: 644,
    0x77051c: 645,
    0x77051d: 646,
    0x77051e: 647,
    0x77051f: 648,
    0x770520: 649,
    0x770521: 650,
    0x770522: 651,
    0x770523: 652,
    0x770524: 653,
    0x770525: 654,
    0x770526: 655,
    0x770527: 656,
    0x770528: 657,
    0x770529: 658,
    0x77052a: 659,
    0x77052b: 660,
    0x77052c: 661,
    0x77052d: 662,
    0x77052e: 663,
    0x77052f: 664,
    0x770530: 665,
    0x770531: 666,
    0x770532: 667,
    0x770533: 668,
    0x770534: 669,
    0x770535: 670,
    0x770536: 674,
    0x770537: 675,
    0x770538: 676,
    0x770539: 677,
    0x77053a: 678,
    0x77053b: 679,
    0x77053c: 680,
    0x77053d: 681,
    0x77053e: 682,
    0x77053f: 683,
    0x770540: 684,
    0x770541: 686,
    0x770542: 687,
    0x770543: 688,
    0x770544: 689,
    0x770545: 690,
    0x770546: 691,
    0x770547: 692,
    0x770548: 694,
    0x770549: 695,
    0x77054a: 704,
    0x77054b: 705,
    0x77054c: 706,
    0x77054d: 707,
    0x77054e: 708,
    0x77054f: 709,
    0x770550: 710,
    0x770551: 711,
    0x770552: 712,
    0x770553: 713,
    0x770554: 714,
    0x770555: 715,
    0x770556: 716,
    0x770557: 717,
    0x770558: 718,
    0x770559: 719,
    0x77055a: 720,
    0x77055b: 721,
    0x77055c: 722,
    0x77055d: 723,
    0x77055e: 724,
    0x77055f: 725,
    0x770560: 726,
    0x770561: 769,
    0x770562: 770,
    0x770563: 771,
    0x770564: 772,
    0x770565: 773,
    0x770566: 774,
    0x770567: 775,
    0x770568: 776,
    0x770569: 777,
    0x77056a: 778,
    0x77056b: 779,
    0x77056c: 780,
    0x77056d: 781,
    0x77056e: 782,
    0x77056f: 783,
    0x770570: 784,
    0x770571: 785,
    0x770572: 786,
    0x770573: 787,
    0x770574: 788,
    0x770575: 789,
    0x770576: 790,
    0x770577: 832,
    0x770578: 833,
    0x770579: 834,
    0x77057a: 835,
    0x77057b: 836,
    0x77057c: 837,
    0x77057d: 838,
    0x77057e: 839,
    0x77057f: 840,
    0x770580: 841,
    0x770581: 842,
    0x770582: 843,
    0x770583: 844,
    0x770584: 845,
    0x770585: 846,
    0x770586: 847,
    0x770587: 848,
    0x770588: 849,
    0x770589: 850,
    0x77058a: 854,
    0x77058b: 855,
    0x77058c: 856,
    0x77058d: 857,
    0x77058e: 858,
    0x77058f: 859,
    0x770590: 860,
    0x770591: 861,
    0x770592: 862,
    0x770593: 863,
    0x770594: 864,
    0x770595: 865,
    0x770596: 866,
    0x770597: 867,
    0x770598: 868,
    0x770599: 869,
    0x77059a: 870,
    0x77059b: 871,
    0x77059c: 872,
    0x77059d: 873,
    0x77059e: 874,
    0x77059f: 875,
    0x7705a0: 876,
    0x7705a1: 877,
    0x7705a2: 878,
    0x7705a3: 879,
    0x7705a4: 880,
    0x7705a5: 881,
    0x7705a6: 882,
    0x7705a7: 896,
    0x7705a8: 897,
    0x7705a9: 898,
    0x7705aa: 899,
    0x7705ab: 900,
    0x7705ac: 901,
    0x7705ad: 902,
    0x7705ae: 903,
    0x7705af: 904,
    0x7705b0: 905,
    0x7705b1: 960,
    0x7705b2: 961,
    0x7705b3: 962,
    0x7705b4: 963,
    0x7705b5: 964,
    0x7705b6: 965,
    0x7705b7: 966,
    0x7705b8: 967,
    0x7705b9: 968,
    0x7705ba: 969,
    0x7705bb: 970,
    0x7705bc: 972,
    0x7705bd: 973,
    0x7705be: 974,
    0x7705bf: 975,
    0x7705c0: 977,
    0x7705c1: 978,
    0x7705c2: 979,
    0x7705c3: 980,
    0x7705c4: 981,
    0x7705c5: 982,
    0x7705c6: 983,
    0x7705c7: 984,
    0x7705c8: 1025,
    0x7705c9: 1026,
    0x7705ca: 1027,
    0x7705cb: 1028,
    0x7705cc: 1029,
    0x7705cd: 1030,
    0x7705ce: 1031,
    0x7705cf: 1032,
    0x7705d0: 1033,
    0x7705d1: 1034,
    0x7705d2: 1037,
    0x7705d3: 1040,
    0x7705d4: 1041,
    0x7705d5: 1042,
    0x7705d6: 1043,
    0x7705d7: 1044,
    0x7705d8: 1045,
    0x7705d9: 1046,
    0x7705da: 1049,
    0x7705db: 1050,
    0x7705dc: 1051,
    0x7705dd: 1052,
    0x7705de: 1053,
    0x7705df: 1054,
    0x7705e0: 1055,
    0x7705e1: 1056,
    0x7705e2: 1057,
    0x7705e3: 1058,
    0x7705e4: 1059,
    0x7705e5: 1060,
    0x7705e6: 1061,
    0x7705e7: 1062,
    0x7705e8: 1063,
    0x7705e9: 1064,
    0x7705ea: 1065,
    0x7705eb: 1066,
    0x7705ec: 1067,
    0x7705ed: 1068,
    0x7705ee: 1069,
    0x7705ef: 1070,
    0x7705f0: 1152,
    0x7705f1: 1154,
    0x7705f2: 1155,
    0x7705f3: 1156,
    0x7705f4: 1157,
    0x7705f5: 1158,
    0x7705f6: 1159,
    0x7705f7: 1160,
    0x7705f8: 1161,
    0x7705f9: 1162,
    0x7705fa: 1163,
    0x7705fb: 1164,
    0x7705fc: 1165,
    0x7705fd: 1166,
    0x7705fe: 1167,
    0x7705ff: 1168,
    0x770600: 1169,
    0x770601: 1173,
    0x770602: 1174,
    0x770603: 1175,
    0x770604: 1176,
    0x770605: 1177,
    0x770606: 1178,
    0x770607: 1216,
    0x770608: 1217,
    0x770609: 1218,
    0x77060a: 1219,
    0x77060b: 1220,
    0x77060c: 1221,
    0x77060d: 1222,
    0x77060e: 1223,
    0x77060f: 1224,
    0x770610: 1225,
    0x770611: 1226,
    0x770612: 1227,
    0x770613: 1228,
    0x770614: 1229,
    0x770615: 1230,
    0x770616: 1231,
    0x770617: 1232,
    0x770618: 1233,
    0x770619: 1234,
    0x77061a: 1235,
    0x77061b: 1236,
    0x77061c: 1237,
    0x77061d: 1238,
    0x77061e: 1239,
    0x77061f: 1240,
    0x770620: 1241,
    0x770621: 1242,
    0x770622: 1243,
    0x770623: 1244,
    0x770624: 1245,
    0x770625: 1246,
    0x770626: 1247,
    0x770627: 1248,
    0x770628: 1249,
    0x770629: 1250,
    0x77062a: 1251,
    0x77062b: 1252,
    0x77062c: 1253,
    0x77062d: 1254,
    0x77062e: 1255,
    0x77062f: 1256,
    0x770630: 1257,
    0x770631: 1258,
    0x770632: 1259,
    0x770633: 1260,
    0x770634: 1261,
    0x770635: 1262,
    0x770636: 1263,
    0x770637: 1264,
    0x770638: 1265,
    0x770639: 1266,
    0x77063a: 1267,
    0x77063b: 1268,
    0x77063c: 1269,
    0x77063d: 1280,
    0x77063e: 1281,
    0x77063f: 1282,
    0x770640: 1283,
    0x770641: 1284,
    0x770642: 1285,
    0x770643: 1286,
    0x770644: 1289,
    0x770645: 1290,
    0x770646: 1291,
    0x770647: 1292,
    0x770648: 1293,
    0x770649: 1294,
    0x77064a: 1295,
    0x77064b: 1296,
    0x77064c: 1297,
    0x77064d: 1298,
    0x77064e: 1299,
    0x77064f: 1300,
    0x770650: 1301,
    0x770651: 1302,
    0x770652: 1303,
    0x770653: 1344,
    0x770654: 1345,
    0x770655: 1346,
    0x770656: 1347,
    0x770657: 1348,
    0x770658: 1349,
    0x770659: 1350,
    0x77065a: 1351,
    0x77065b: 1352,
    0x77065c: 1354,
    0x77065d: 1355,
    0x77065e: 1356,
    0x77065f: 1357,
    0x770660: 1358,
    0x770661: 1359,
    0x770662: 1360,
    0x770663: 1361,
    0x770664: 1362,
    0x770665: 1363,
    0x770666: 1365,
    0x770667: 1366,
    0x770668: 1367,
    0x770669: 1368,
    0x77066a: 1369,
    0x77066b: 1370,
    0x77066c: 1371,
    0x77066d: 1372,
    0x77066e: 1374,
    0x77066f: 1375,
    0x770670: 1376,
    0x770671: 1379,
    0x770672: 1380,
    0x770673: 1381,
    0x770674: 1382,
    0x770675: 1383,
    0x770676: 1384,
    0x770677: 1385,
    0x770678: 1386,
    0x770679: 1387,
    0x77067a: 1388,
    0x77067b: 1389,
    0x77067c: 1390,
    0x77067d: 1391,
    0x77067e: 1392,
    0x77067f: 1393,
    0x770680: 1394,
    0x770681: 1395,
    0x770682: 1396,
    0x770683: 1397,
    0x770684: 1398,
    0x770685: 1408,
    0x770686: 1409,
    0x770687: 1410,
    0x770688: 1411,
    0x770689: 1412,
    0x77068a: 1414,
    0x77068b: 1472,
    0x77068c: 1473,
    0x77068d: 1474,
    0x77068e: 1475,
    0x77068f: 1476,
    0x770690: 1477,
    0x770691: 1478,
    0x770692: 1479,
    0x770693: 1480,
    0x770694: 1481,
    0x770695: 1482,
    0x770696: 1483,
    0x770697: 1484,
    0x770698: 1486,
    0x770699: 1487,
    0x77069a: 1488,
    0x77069b: 1489,
    0x77069c: 1490,
    0x77069d: 1491,
    0x77069e: 1495,
    0x77069f: 1496,
    0x7706a0: 1497,
    0x7706a1: 1498,
    0x7706a2: 1499,
    0x7706a3: 1500,
    0x7706a4: 1501,
    0x7706a5: 1502,
    0x7706a6: 1503,
    0x7706a7: 1504,
    0x7706a8: 1505,
    0x7706a9: 1506,
    0x7706aa: 1507,
    0x7706ab: 1508,
    0x7706ac: 1536,
    0x7706ad: 1537,
    0x7706ae: 1538,
    0x7706af: 1539,
    0x7706b0: 1540,
    0x7706b1: 1541,
    0x7706b2: 1600,
    0x7706b3: 1601,
    0x7706b4: 1602,
    0x7706b5: 1603,
    0x7706b6: 1604,
    0x7706b7: 1605,
    0x7706b8: 1606,
    0x7706b9: 1607,
    0x7706ba: 1612,
    0x7706bb: 1613,
    0x7706bc: 1614,
    0x7706bd: 1615,
    0x7706be: 1616,
    0x7706bf: 1617,
    0x7706c0: 1618,
    0x7706c1: 1619,
    0x7706c2: 1620,
    0x7706c3: 1621,
    0x7706c4: 1622,
    0x7706c5: 1664,
    0x7706c6: 1665,
    0x7706c7: 1667,
    0x7706c8: 1668,
    0x7706c9: 1670,
    0x7706ca: 1671,
    0x7706cb: 1672,
    0x7706cc: 1673,
    0x7706cd: 1674,
    0x7706ce: 1675,
    0x7706cf: 1676,
    0x7706d0: 1677,
    0x7706d1: 1678,
    0x7706d2: 1679,
    0x7706d3: 1680,
    0x7706d4: 1681,
    0x7706d5: 1682,
    0x7706d6: 1683,
    0x7706d7: 1684,
    0x7706d8: 1685,
    0x7706d9: 1686,
    0x7706da: 1730,
    0x7706db: 1732,
    0x7706dc: 1734,
    0x7706dd: 1792,
    0x7706de: 1793,
    0x7706df: 1794,
    0x7706e0: 1795,
    0x7706e1: 1796,
    0x7706e2: 1797,
    0x7706e3: 1798,
    0x7706e4: 1799,
    0x7706e5: 1800,
    0x7706e6: 1801,
    0x7706e7: 1802,
    0x7706e8: 1803,
    0x7706e9: 1804,
    0x7706ea: 1805,
    0x7706eb: 1810,
    0x7706ec: 1811,
    0x7706ed: 1812,
    0x7706ee: 1813,
    0x7706ef: 1814,
    0x7706f0: 1815,
    0x7706f1: 1817,
    0x7706f2: 1818,
    0x7706f3: 1819,
    0x7706f4: 1820,
    0x7706f5: 1821,
    0x7706f6: 1822,
    0x7706f7: 1823,
    0x7706f8: 1824,
    0x7706f9: 1825,
    0x7706fa: 1826,
    0x7706fb: 1827,
    0x7706fc: 1828,
    0x7706fd: 1831,
    0x7706fe: 1832,
    0x7706ff: 1858,
}

deathlink_messages = defaultdict(lambda: " was defeated.", {
    0x0200: " was bonked by apples from Whispy Woods.",
    0x0201: " was out-maneuvered by Acro.",
    0x0202: " was out-numbered by Pon & Con.",
    0x0203: " was defeated by Ado's powerful paintings.",
    0x0204: " was clobbered by King Dedede.",
    0x0205: " lost their battle against Dark Matter."
})
kdl3_gifting_options = {
    "AcceptsAnyGift": True,
    "DesiredTraits": [
        "Consumable", "Food", "Drink", "Candy", "Tomato",
        "Invincible", "Life", "Heal", "Health", "Trap",
        "Goo", "Gel", "Slow", "Slowness", "Eject", "Removal"
    ]
}

kdl3_gifts = {
    1: {
        "Item": {
            "Name": "1-Up",
            "Amount": 1,
            "Value": 400000
        },
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 1,
                "Duration": 1,
            },
            {
                "Trait": "Life",
                "Quality": 1,
                "Duration": 1
            }
        ]
    },
    2: {
        "Item": {
            "Name": "Maxim Tomato",
            "Amount": 1,
            "Value": 500000
        },
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 5,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 5,
                "Duration": 1,
            },
            {
                "Trait": "Food",
                "Quality": 1,
                "Duration": 1,
            },
            {
                "Trait": "Tomato",
                "Quality": 5,
                "Duration": 1,
            }
        ]
    },
    3: {
        "Item": {
            "Name": "Energy Drink",
            "Amount": 1,
            "Value": 100000
        },
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 1,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 1,
                "Duration": 1,
            },
            {
                "Trait": "Drink",
                "Quality": 1,
                "Duration": 1,
            },
        ]
    },
    5: {
        "Item": {
            "Name": "Small Star Piece",
            "Amount": 1,
            "Value": 10000
        },
        "Traits": [
            {
                "Trait": "Currency",
                "Quality": 1,
                "Duration": 1,
            },
            {
                "Trait": "Money",
                "Quality": 1,
                "Duration": 1,
            },
            {
                "Trait": "Star",
                "Quality": 1,
                "Duration": 1
            }
        ]
    },
    6: {
        "Item": {
            "Name": "Medium Star Piece",
            "Amount": 1,
            "Value": 30000
        },
        "Traits": [
            {
                "Trait": "Currency",
                "Quality": 3,
                "Duration": 1,
            },
            {
                "Trait": "Money",
                "Quality": 3,
                "Duration": 1,
            },
            {
                "Trait": "Star",
                "Quality": 3,
                "Duration": 1
            }
        ]
    },
    7: {
        "Item": {
            "Name": "Large Star Piece",
            "Amount": 1,
            "Value": 50000
        },
        "Traits": [
            {
                "Trait": "Currency",
                "Quality": 5,
                "Duration": 1,
            },
            {
                "Trait": "Money",
                "Quality": 5,
                "Duration": 1,
            },
            {
                "Trait": "Star",
                "Quality": 5,
                "Duration": 1
            }
        ]
    },
}

kdl3_trap_gifts = {
    0: {
        "Item": {
            "Name": "Gooey Bag",
            "Amount": 1,
            "Value": 10000
        },
        "Traits": [
            {
                "Trait": "Trap",
                "Quality": 1,
                "Duration": 1,
            },
            {
                "Trait": "Goo",
                "Quality": 1,
                "Duration": 1,
            },
            {
                "Trait": "Gel",
                "Quality": 1,
                "Duration": 1
            }
        ]
    },
    1: {
        "Item": {
            "Name": "Slowness",
            "Amount": 1,
            "Value": 10000
        },
        "Traits": [
            {
                "Trait": "Trap",
                "Quality": 1,
                "Duration": 1,
            },
            {
                "Trait": "Slow",
                "Quality": 1,
                "Duration": 1,
            },
            {
                "Trait": "Slowness",
                "Quality": 1,
                "Duration": 1
            }
        ]
    },
    2: {
        "Item": {
            "Name": "Eject Ability",
            "Amount": 1,
            "Value": 10000
        },
        "Traits": [
            {
                "Trait": "Trap",
                "Quality": 1,
                "Duration": 1,
            },
            {
                "Trait": "Eject",
                "Quality": 1,
                "Duration": 1,
            },
            {
                "Trait": "Removal",
                "Quality": 1,
                "Duration": 1
            }
        ]
    },
    3: {
        "Item": {
            "Name": "Bad Meal",
            "Amount": 1,
            "Value": 10000
        },
        "Traits": [
            {
                "Trait": "Trap",
                "Quality": 1,
                "Duration": 1,
            },
            {
                "Trait": "Damage",
                "Quality": 1,
                "Duration": 1,
            },
            {
                "Trait": "Food",
                "Quality": 1,
                "Duration": 1
            }
        ]
    },
}


async def update_object(ctx: "SNIContext", key: str, value: typing.Dict):
    await ctx.send_msgs([
        {
            "cmd": "Set",
            "key": key,
            "default": {},
            "want_reply": False,
            "operations": [
                {"operation": "update", "value": value}
            ]
        }
    ])


async def pop_object(ctx: "SNIContext", key: str, value: str):
    await ctx.send_msgs([
        {
            "cmd": "Set",
            "key": key,
            "default": {},
            "want_reply": False,
            "operations": [
                {"operation": "pop", "value": value}
            ]
        }
    ])


@mark_raw
def cmd_gift(self: "SNIClientCommandProcessor"):
    """Toggles gifting for the current game."""
    if not getattr(self.ctx, "gifting", None):
        self.ctx.gifting = True
    else:
        self.ctx.gifting = not self.ctx.gifting
    self.output(f"Gifting set to {self.ctx.gifting}")
    async_start(update_object(self.ctx, f"Giftboxes;{self.ctx.team}", {
        f"{self.ctx.slot}":
            {
                "IsOpen": self.ctx.gifting,
                **kdl3_gifting_options
            }
    }))


class KDL3SNIClient(SNIClient):
    game = "Kirby's Dream Land 3"
    levels = None
    consumables = None
    stars = None
    item_queue: typing.List = []
    initialize_gifting: bool = False
    giftbox_key: str = ""
    motherbox_key: str = ""
    client_random: random.Random = random.Random()

    async def deathlink_kill_player(self, ctx) -> None:
        from SNIClient import DeathState, snes_buffered_write, snes_flush_writes, snes_read
        game_state = await snes_read(ctx, KDL3_GAME_STATE, 1)
        if game_state[0] == 0xFF:
            return  # despite how funny it is, don't try to kill Kirby in a menu

        current_stage = await snes_read(ctx, KDL3_CURRENT_LEVEL, 1)
        if current_stage[0] == 0x7:  # boss stage
            boss_hp = await snes_read(ctx, KDL3_BOSS_HP, 1)
            if boss_hp[0] == 0:
                return  # receiving a deathlink after defeating a boss has softlock potential

        current_hp = await snes_read(ctx, KDL3_KIRBY_HP, 1)
        if current_hp[0] == 0:
            return  # don't kill Kirby while he's already dead
        snes_buffered_write(ctx, KDL3_KIRBY_HP, bytes([0x00]))

        await snes_flush_writes(ctx)

        ctx.death_state = DeathState.dead
        ctx.last_death_link = time.time()

    async def validate_rom(self, ctx) -> bool:
        from SNIClient import snes_read
        rom_name = await snes_read(ctx, KDL3_ROMNAME, 0x15)
        if rom_name is None or rom_name == bytes([0] * 0x15) or rom_name[:4] != b"KDL3":
            if "gift" in ctx.command_processor.commands:
                ctx.command_processor.commands.pop("gift")
            return False

        ctx.game = self.game
        ctx.rom = rom_name
        ctx.items_handling = 0b111  # always remote items
        ctx.allow_collect = True
        ctx.command_processor.commands["gift"] = cmd_gift

        death_link = await snes_read(ctx, KDL3_DEATH_LINK_ADDR, 1)
        if death_link:
            await ctx.update_death_link(bool(death_link[0] & 0b1))

        return True

    async def pop_item(self, ctx):
        from SNIClient import snes_buffered_write, snes_read
        if len(self.item_queue) > 0:
            item = self.item_queue.pop()
            # special handling for the remaining items
            item_idx = item.item & 0x0000FF
            if item_idx == 0x21:
                # 1-Up
                life_count = await snes_read(ctx, KDL3_LIFE_COUNT, 2)
                life_bytes = pack("H", unpack("H", life_count)[0] + 1)
                snes_buffered_write(ctx, KDL3_LIFE_COUNT, life_bytes)
                snes_buffered_write(ctx, KDL3_LIFE_VISUAL, life_bytes)
                snes_buffered_write(ctx, KDL3_SOUND_FX, bytes([0x33]))
            elif item_idx == 0x22:
                # Maxim Tomato
                # Check for Gooey
                gooey_hp = await snes_read(ctx, KDL3_KIRBY_HP + 2, 1)
                snes_buffered_write(ctx, KDL3_SOUND_FX, bytes([0x26]))
                if gooey_hp[0] > 0x00:
                    snes_buffered_write(ctx, KDL3_KIRBY_HP, bytes([0x08, 0x00]))
                    snes_buffered_write(ctx, KDL3_KIRBY_HP + 2, bytes([0x08, 0x00]))
                else:
                    snes_buffered_write(ctx, KDL3_KIRBY_HP, bytes([0x0A, 0x00]))
            elif item_idx == 0x23:
                # Invincibility Candy
                snes_buffered_write(ctx, KDL3_SOUND_FX, bytes([0x26]))
                snes_buffered_write(ctx, KDL3_INVINCIBILITY_TIMER, bytes([0x84, 0x03]))
            elif item_idx in [0x24, 0x25, 0x26]:
                # Little/Medium/Big Star
                amount = 2 * (item_idx - 0x24) + 1
                current_count = struct.unpack("H", await snes_read(ctx, KDL3_STAR_COUNT, 2))[0]
                if not 0x8000 & current_count:  # check that we just collected one in the current frame
                    # 0x8000 flags the game to check for changes in this value
                    snes_buffered_write(ctx, KDL3_STAR_COUNT, struct.pack("H", (current_count + amount) | 0x8000))
            elif item_idx == 0x40:
                check_gooey_r = await snes_read(ctx, KDL3_GOOEY_TRAP, 2)
                check_gooey = struct.unpack("H", check_gooey_r)
                if check_gooey[0] == 0:
                    snes_buffered_write(ctx, KDL3_GOOEY_TRAP, bytes([0x01, 0x00]))
                else:
                    self.item_queue.append(item)  # We can't apply this yet
            elif item_idx == 0x41:
                check_slow_r = await snes_read(ctx, KDL3_SLOWNESS_TRAP, 2)
                check_slow = struct.unpack("H", check_slow_r)
                if check_slow[0] == 0:
                    snes_buffered_write(ctx, KDL3_SLOWNESS_TRAP, bytes([0x84, 0x03]))
                    snes_buffered_write(ctx, KDL3_SOUND_FX, bytes([0xA7]))
                else:
                    self.item_queue.append(item)  # We can't apply this yet
            elif item_idx == 0x42:
                check_ability_r = await snes_read(ctx, KDL3_ABILITY_TRAP, 2)
                check_ability = struct.unpack("H", check_ability_r)
                if check_ability[0] == 0:
                    snes_buffered_write(ctx, KDL3_ABILITY_TRAP, bytes([0x01, 0x00]))
                else:
                    self.item_queue.append(item)  # We can't apply this yet

    async def pop_gift(self, ctx):
        if ctx.stored_data[self.giftbox_key]:
            from SNIClient import snes_read, snes_buffered_write
            key, gift = ctx.stored_data[self.giftbox_key].popitem()
            await pop_object(ctx, self.giftbox_key, key)
            # first, special cases
            traits = [trait["Trait"] for trait in gift["Traits"]]
            if "Candy" in traits or "Invincible" in traits:
                # apply invincibility candy
                snes_buffered_write(ctx, KDL3_INVINCIBILITY_TIMER, bytes([0x84, 0x03]))
                snes_buffered_write(ctx, KDL3_SOUND_FX, bytes([0x2B]))
            elif "Tomato" in traits:
                # apply maxim tomato
                gooey_hp = await snes_read(ctx, KDL3_KIRBY_HP + 2, 1)
                snes_buffered_write(ctx, KDL3_SOUND_FX, bytes([0x2B]))
                if gooey_hp[0] > 0x00:
                    snes_buffered_write(ctx, KDL3_KIRBY_HP, bytes([0x08, 0x00]))
                    snes_buffered_write(ctx, KDL3_KIRBY_HP + 2, bytes([0x08, 0x00]))
                else:
                    snes_buffered_write(ctx, KDL3_KIRBY_HP, bytes([0x0A, 0x00]))
            elif "Life" in traits:
                # Apply 1-Up
                life_count = await snes_read(ctx, KDL3_LIFE_COUNT, 2)
                life_bytes = pack("H", unpack("H", life_count)[0] + 1)
                snes_buffered_write(ctx, KDL3_LIFE_COUNT, life_bytes)
                snes_buffered_write(ctx, KDL3_LIFE_VISUAL, life_bytes)
                snes_buffered_write(ctx, KDL3_SOUND_FX, bytes([0x33]))
            elif "Trap" in traits:
                # find the best trap to apply
                if "Goo" in traits or "Gel" in traits:
                    check_gooey_r = await snes_read(ctx, KDL3_GOOEY_TRAP, 2)
                    check_gooey = struct.unpack("H", check_gooey_r)
                    if check_gooey[0] == 0:
                        snes_buffered_write(ctx, KDL3_GOOEY_TRAP, bytes([0x01, 0x00]))
                    else:
                        await update_object(ctx, key, {key: gift})  # We can't apply this yet
                elif "Slow" in traits or "Slowness" in traits:
                    check_slow_r = await snes_read(ctx, KDL3_SLOWNESS_TRAP, 2)
                    check_slow = struct.unpack("H", check_slow_r)
                    if check_slow[0] == 0:
                        snes_buffered_write(ctx, KDL3_SLOWNESS_TRAP, bytes([0x84, 0x03]))
                        snes_buffered_write(ctx, KDL3_SOUND_FX, bytes([0xA7]))
                    else:
                        await update_object(ctx, key, {key: gift})  # We can't apply this yet
                elif "Eject" in traits or "Removal" in traits:
                    check_ability_r = await snes_read(ctx, KDL3_ABILITY_TRAP, 2)
                    check_ability = struct.unpack("H", check_ability_r)
                    if check_ability[0] == 0:
                        snes_buffered_write(ctx, KDL3_ABILITY_TRAP, bytes([0x01, 0x00]))
                    else:
                        await update_object(ctx, key, {key: gift})  # We can't apply this yet
                else:
                    # just deal damage to Kirby
                    kirby_hp = struct.unpack("H", await snes_read(ctx, KDL3_KIRBY_HP, 2))[0]
                    snes_buffered_write(ctx, KDL3_KIRBY_HP, struct.pack("H", max(kirby_hp - 2, 0)))
            else:
                # check if it's tasty
                if any(x in traits for x in ["Consumable", "Food", "Drink", "Heal", "Health"]):
                    # it's tasty!, use quality to decide how much to heal
                    quality = max((trait["Quality"] for trait in gift["Traits"]
                                   if trait["Trait"] in ["Consumable", "Food", "Drink", "Heal", "Health"]))
                    quality = min(10, quality * 2)
                else:
                    # it's not really edible, but he'll eat it anyways
                    quality = self.client_random.choices(range(0, 2), {0: 75, 1: 25})[0]
                kirby_hp = await snes_read(ctx, KDL3_KIRBY_HP, 1)
                gooey_hp = await snes_read(ctx, KDL3_KIRBY_HP + 2, 1)
                snes_buffered_write(ctx, KDL3_SOUND_FX, bytes([0x26]))
                if gooey_hp[0] > 0x00:
                    snes_buffered_write(ctx, KDL3_KIRBY_HP, struct.pack("H", min(kirby_hp[0] + quality // 2, 8)))
                    snes_buffered_write(ctx, KDL3_KIRBY_HP + 2, struct.pack("H", min(gooey_hp[0] + quality // 2, 8)))
                else:
                    snes_buffered_write(ctx, KDL3_KIRBY_HP, struct.pack("H", min(kirby_hp[0] + quality, 10)))

    async def pick_gift_recipient(self, ctx, gift):
        if gift != 4:
            gift_base = kdl3_gifts[gift]
        else:
            gift_base = kdl3_trap_gifts[self.client_random.randint(0, 3)]
        most_applicable = -1
        most_applicable_slot = -1
        for slot, info in ctx.stored_data[self.motherbox_key].items():
            if int(slot) == ctx.slot and len(ctx.stored_data[self.motherbox_key]) > 1:
                continue
            desire = len(set(info["DesiredTraits"]).intersection([trait["Trait"] for trait in gift_base["Traits"]]))
            if desire > most_applicable:
                most_applicable = desire
                most_applicable_slot = int(slot)
        print(most_applicable, most_applicable_slot)
        Uuid = uuid.uuid4().hex
        item = {
            **gift_base,
            "ID": Uuid,
            "Sender": ctx.player_names[ctx.slot],
            "Receiver": ctx.player_names[most_applicable_slot],
            "SenderTeam": ctx.team,
            "ReceiverTeam": ctx.team,  # for the moment
            "IsRefund": False,
            "GiftValue": gift_base["Item"]["Value"] * gift_base["Item"]["Amount"]
        }
        print(item)
        await update_object(ctx, f"Giftbox;{ctx.team};{most_applicable_slot}", {
            Uuid: item,
        })

    async def game_watcher(self, ctx) -> None:
        try:
            from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
            rom = await snes_read(ctx, KDL3_ROMNAME, 0x15)
            if rom != ctx.rom:
                ctx.rom = None
            halken = await snes_read(ctx, KDL3_HALKEN, 6)
            if halken != b"halken":
                return
            ninten = await snes_read(ctx, KDL3_NINTEN, 6)
            if ninten != b"ninten":
                return
            if not ctx.server:
                return
            enable_gifting = await snes_read(ctx, KDL3_GIFTING_FLAG, 0x01)
            if not self.initialize_gifting:
                self.giftbox_key = f"Giftbox;{ctx.team};{ctx.slot}"
                self.motherbox_key = f"Giftboxes;{ctx.team}"
                ctx.set_notify(self.motherbox_key, self.giftbox_key)
                await update_object(ctx, f"Giftboxes;{ctx.team}", {f"{ctx.slot}":
                    {
                        "IsOpen": bool(enable_gifting[0]),
                        **kdl3_gifting_options
                    }})
                ctx.gifting = bool(enable_gifting[0])
                self.initialize_gifting = True
            # can't check debug anymore, without going and copying the value. might be important later.
            if self.levels is None:
                self.levels = dict()
                for i in range(5):
                    level_data = await snes_read(ctx, KDL3_LEVEL_ADDR + (14 * i), 14)
                    self.levels[i] = unpack("HHHHHHH", level_data)

            if self.consumables is None:
                consumables = await snes_read(ctx, KDL3_CONSUMABLE_FLAG, 1)
                self.consumables = consumables[0] == 0x01
            if self.stars is None:
                stars = await snes_read(ctx, KDL3_CONSUMABLE_FLAG, 1)
                self.stars = stars[0] == 0x01
            is_demo = await snes_read(ctx, KDL3_IS_DEMO, 1)  # 1 - recording a demo, 2 - playing back recorded, 3+ is a demo
            if is_demo[0] > 0x00:
                return
            current_save = await snes_read(ctx, KDL3_GAME_SAVE, 1)
            goal = await snes_read(ctx, KDL3_GOAL_ADDR, 1)
            boss_butch_status = await snes_read(ctx, KDL3_BOSS_BUTCH_STATUS + (current_save[0] * 2), 1)
            mg5_status = await snes_read(ctx, KDL3_MG5_STATUS + (current_save[0] * 2), 1)
            jumping_status = await snes_read(ctx, KDL3_JUMPING_STATUS + (current_save[0] * 2), 1)
            if boss_butch_status[0] == 0xFF:
                return  # save file is not created, ignore
            if (goal[0] == 0x00 and boss_butch_status[0] == 0x01) \
                    or (goal[0] == 0x01 and boss_butch_status[0] == 0x03) \
                    or (goal[0] == 0x02 and mg5_status[0] == 0x03) \
                    or (goal[0] == 0x03 and jumping_status[0] == 0x03):
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.finished_game = True
            current_bgm = await snes_read(ctx, KDL3_CURRENT_BGM, 1)
            if current_bgm[0] in (0x00, 0x21, 0x22, 0x23, 0x25, 0x2A, 0x2B):
                return  # null, title screen, opening, save select, true and false endings
            game_state = await snes_read(ctx, KDL3_GAME_STATE, 1)
            current_hp = await snes_read(ctx, KDL3_KIRBY_HP, 1)
            if "DeathLink" in ctx.tags and game_state[0] == 0x00 and ctx.last_death_link + 1 < time.time():
                currently_dead = current_hp[0] == 0x00
                await ctx.handle_deathlink_state(currently_dead)

            recv_count = await snes_read(ctx, KDL3_RECV_COUNT, 2)
            recv_amount = unpack("H", recv_count)[0]
            if recv_amount < len(ctx.items_received):
                item = ctx.items_received[recv_amount]
                recv_amount += 1
                logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                    color(ctx.item_names[item.item], 'red', 'bold'),
                    color(ctx.player_names[item.player], 'yellow'),
                    ctx.location_names[item.location], recv_amount, len(ctx.items_received)))

                snes_buffered_write(ctx, KDL3_RECV_COUNT, pack("H", recv_amount))
                if item.item & 0x000070 == 0:
                    ability = item.item & 0x00000F
                    snes_buffered_write(ctx, KDL3_ABILITY_ARRAY + (ability * 2), pack("H", ability))
                    snes_buffered_write(ctx, KDL3_SOUND_FX, bytes([0x32]))
                elif item.item & 0x000010 > 0:
                    friend = (item.item & 0x00000F)
                    snes_buffered_write(ctx, KDL3_SOUND_FX, bytes([0x32]))
                    snes_buffered_write(ctx, KDL3_ANIMAL_FRIENDS + (friend << 1), pack("H", friend + 1))
                elif item.item == 0x770020:
                    # Heart Star
                    heart_star_count = await snes_read(ctx, KDL3_HEART_STAR_COUNT, 2)
                    snes_buffered_write(ctx, KDL3_HEART_STAR_COUNT, pack("H", unpack("H", heart_star_count)[0] + 1))
                    snes_buffered_write(ctx, KDL3_SOUND_FX, bytes([0x16]))
                else:
                    self.item_queue.append(item)

            # handle gifts here
            if ctx.gifting:
                if enable_gifting[0]:
                    gift = await snes_read(ctx, KDL3_GIFTING_SEND, 0x01)
                    if gift[0]:
                        # we have a gift to send
                        await self.pick_gift_recipient(ctx, gift[0])
                        snes_buffered_write(ctx, KDL3_GIFTING_SEND, bytes([0x00]))
                else:
                    snes_buffered_write(ctx, KDL3_GIFTING_FLAG, bytes([0x01]))
            else:
                if enable_gifting[0]:
                    snes_buffered_write(ctx, KDL3_GIFTING_FLAG, bytes([0x00]))

            await snes_flush_writes(ctx)

            new_checks = []
            # level completion status
            world_unlocks = await snes_read(ctx, KDL3_WORLD_UNLOCK, 1)
            if world_unlocks[0] > 0x06:
                return  # save is not loaded, ignore
            stages_raw = await snes_read(ctx, KDL3_COMPLETED_STAGES, 60)
            stages = struct.unpack("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHH", stages_raw)
            for i in range(30):
                loc_id = 0x770000 + i + 1
                if stages[i] == 1 and loc_id not in ctx.checked_locations:
                    new_checks.append(loc_id)
                elif loc_id in ctx.checked_locations:
                    snes_buffered_write(ctx, KDL3_COMPLETED_STAGES + (i * 2), struct.pack("H", 1))

            # heart star status
            heart_stars = await snes_read(ctx, KDL3_HEART_STARS, 35)
            for i in range(5):
                start_ind = i * 7
                for j in range(1, 7):
                    level_ind = start_ind + j - 1
                    loc_id = 0x770100 + (6 * i) + j
                    if heart_stars[level_ind] and loc_id not in ctx.checked_locations:
                        new_checks.append(loc_id)
                    elif loc_id in ctx.checked_locations:
                        snes_buffered_write(ctx, KDL3_HEART_STARS + level_ind, bytes([0x01]))
            if self.consumables:
                consumables = await snes_read(ctx, KDL3_CONSUMABLES, 1920)
                for consumable in consumable_addrs:
                    # TODO: see if this can be sped up in any way
                    loc_id = 0x770300 + consumable
                    if loc_id not in ctx.checked_locations and consumables[consumable_addrs[consumable]] == 0x01:
                        new_checks.append(loc_id)
            if self.stars:
                stars = await snes_read(ctx, KDL3_STARS, 1920)
                for star in star_addrs:
                    if star not in ctx.checked_locations and stars[star_addrs[star]] == 0x01:
                        new_checks.append(star)
            await snes_flush_writes(ctx)

            # boss status
            boss_flag_bytes = await snes_read(ctx, KDL3_BOSS_STATUS, 2)
            boss_flag = unpack("H", boss_flag_bytes)[0]
            for bitmask, boss in zip(range(1, 11, 2), boss_locations.keys()):
                if boss_flag & (1 << bitmask) > 0 and boss not in ctx.checked_locations:
                    new_checks.append(boss)

            for new_check_id in new_checks:
                ctx.locations_checked.add(new_check_id)
                location = ctx.location_names[new_check_id]
                snes_logger.info(
                    f'New Check: {location} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
                await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [new_check_id]}])

            if game_state[0] != 0xFF:
                await self.pop_item(ctx)
                await self.pop_gift(ctx)
        except Exception as ex:
            # we crashed, so print log and clean up
            snes_logger.error("", exc_info=ex)
            if "gift" in ctx.command_processor.commands:
                ctx.command_processor.commands.pop("gift")
            ctx.rom = None
            ctx.game = None
