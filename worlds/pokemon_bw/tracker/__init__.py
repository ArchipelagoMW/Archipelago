
def range_incl(a: int, b: int) -> range:
    return range(a, b+1)


mapping_single: dict[int, int] = {
    317: 1,    # => "route1"
    319: 2,    # => "route2"
    321: 3,    # => "route3"
    326: 4,    # => "route4"
    329: 5,    # => "route5"
    331: 6,    # => "route6"
    337: 7,    # => "route7"
    345: 8,    # => "route8"
    348: 9,    # => "route9"
    355: 10,   # => "route10"
    365: 11,   # => "route11"
    368: 12,   # => "route12"
    370: 13,   # => "route13"
    374: 14,   # => "route14"
    378: 15,   # => "route15"
    383: 16,   # => "route16"
    397: 17,   # => "accumulatown"
    418: 18,   # => "anvilletown"
    28: 19,    # => "casteliacity"
    96: 20,    # => "driftveilcity"
    113: 21,   # => "icirruscity"
    406: 22,   # => "lacunosatown"
    107: 23,   # => "mistraltoncity_b"
    107 + 1024: 24,  # => "mistraltoncity_w"
    16: 25,      # => "nacrenecity"
    62: 26,      # => "nimbasacity"
    64: 27,      # => "nimbasacityeast"
    389: 28,     # => "nuvematown"
    120: 29,     # => "opelucidcity_b"
    120 + 1024: 30,  # => "opelucidcity_w"
    6: 31,     # => "striatoncity"
    412: 32,   # => "undellatown"
    376: 33,   # => "abundantshrine"
    246: 35,   # => "abyssalruins2f"
    247: 36,   # => "abyssalruins3f"
    248: 37,   # => "abyssalruins4f"
    338: 38,   # => "celestialtower1f"
    339: 39,   # => "celestialtower2f"
    340: 40,   # => "celestialtower3f"
    341: 41,   # => "celestialtower4f"
    342: 42,   # => "celestialtower5f"
    352: 43,   # => "challengerscave1f"
    353: 44,   # => "challengerscaveb1f"
    354: 45,   # => "challengerscaveb2f"
    195: 46,   # => "chargestonecave1f"
    196: 47,   # => "chargestonecaveb1f"
    197: 48,   # => "chargestonecaveb2f"
    194: 49,   # => "chargestonecaveoutside"
    192: 50,   # => "coldstorage"
    193: 51,   # => "coldstoragecontainer"
    191: 52,   # => "coldstorageoutside"
    158: 53,   # => "desertresort"
    157: 4,    # => "desertresortentrance" but it's on route 4 now
    207: 54,   # => "dragonspiraltower1f"
    208: 55,   # => "dragonspiraltower2f"
    209: 56,   # => "dragonspiraltower3f"
    210: 57,   # => "dragonspiraltower4f"
    211: 58,   # => "dragonspiraltower5f"
    212: 59,   # => "dragonspiraltower6f"
    213: 60,   # => "dragonspiraltower7f"
    205: 61,   # => "dragonspiraltowerentrance"
    206: 62,   # => "dragonspiraltoweroutside"
    152: 63,   # => "dreamyard"
    153: 64,   # => "dreamyardbasement"
    253: 0,    # DRIFTVEIL DRAWBRIDGE, overworld
    231: 65,   # => "giantchasmcave"
    232: 66,   # => "giantchasmcrater"
    233: 66,   # => "giantchasmcrater"
    234: 67,   # => "giantchasmdepths"
    230: 68,   # => "giantchasmentrance"
    335: 69,   # => "guidancechamber"
    235: 70,   # => "libertygarden"
    236: 71,   # => "libertygardenlighthouse"
    237: 72,   # => "libertygardenlighthousebasement"
    385: 73,   # => "lostlornforest"
    263: 74,   # => "marvelousbridge"
    333: 75,   # => "mistraltoncave1f"
    334: 76,   # => "mistraltoncave2f"
    346: 77,   # => "mooroficirrus"
    264: 78,   # => "nscastle1f"
    265: 79,   # => "nscastle2f"
    268: 79,   # => "nscastle2frightroom"
    269: 80,   # => "nscastle3f"
    271: 80,   # => "nscastle3fcenterroom"
    272: 80,   # => "nscastle3fleftroom"
    273: 81,   # => "nscastle4f"
    275: 81,   # => "nscastle4fcenterroom"
    277: 82,   # => "nscastle5f"
    274: 81,   # => "nscastlensroom"
    278: 83,   # => "nscastlethroneroom"
    155: 84,   # => "pinwheelforest"
    154: 85,   # => "pinwheelforestoutside"
    160: 86,   # => "reliccastle1f"
    161: 87,   # => "reliccastleb1f"
    162: 88,   # => "reliccastleb2f"
    163: 89,   # => "reliccastleb3f"
    164: 90,   # => "reliccastleb4f"
    165: 91,   # => "reliccastleb5f"
    166: 92,   # => "reliccastleb7f"
    190: 94,   # => "reliccastletower1f"
    189: 95,   # => "reliccastletowerb1f"
    188: 96,   # => "reliccastletowerb2f"
    187: 97,   # => "reliccastletowerb3f"
    186: 98,   # => "reliccastletowerb4f"
    185: 99,   # => "reliccastletowerb5f"
    184: 100,  # => "reliccastletowerb6f"
    183: 101,  # => "reliccastletowerb7f"
    182: 102,  # => "reliccastlevolcaronasroom"
    156: 103,  # => "ruminationfield"
    249: 104,  # => "skyarrowbridge"
    250: 104,  # => "skyarrowbridge"
    254: 105,  # => "tubelinebridge"
    199: 106,  # => "twistmountain"
    203: 107,  # => "twistmountainicerockcave"
    202: 108,  # => "twistmountainlowerlevel"
    201: 109,  # => "twistmountainmiddlelevel"
    198: 110,  # => "twistmountainoutside"
    200: 111,  # => "twistmountainupperlevel"
    240: 112,  # => "undellabay"
    222: 113,  # => "victoryroad1fleftmostroom"
    215: 114,  # => "victoryroad1fmiddleroom"
    220: 115,  # => "victoryroad1frightmostroom"
    216: 116,  # => "victoryroad2fleftroom"
    219: 117,  # => "victoryroad2frightroom"
    223: 118,  # => "victoryroad3fleftmostroom"
    217: 119,  # => "victoryroad3fmiddleroom"
    221: 120,  # => "victoryroad3frightmostroom"
    224: 121,  # => "victoryroad4fleftmostroom"
    218: 122,  # => "victoryroad4fmiddleroom"
    227: 123,  # => "victoryroad4frightmostroom"
    225: 124,  # => "victoryroad5f"
    226: 125,  # => "victoryroad6f"
    228: 126,  # => "victoryroad7f"
    214: 127,  # => "victoryroadoutside"
    229: 128,  # => "victoryroadtrialchamber"
    255: 129,  # => "villagebridge"
    324: 130,  # => "wellspringcave1f"
    325: 131,  # => "wellspringcaveb1f"
    423: 132,  # => "route17" these all are merged to one map
    387: 132,  # => "route18" these all are merged to one map
    238: 132,  # => "p2 lab" these all are merged to one map
}

mapping_range: dict[range, int] = {
    range_incl(356, 364): 0,  # BADGE GATES, overworld
    range_incl(30, 40): 19,  # => "casteliacity"
    range_incl(136, 146): 0,  # POKÉMON LEAGUE, overworld
    range_incl(241, 245): 34,  # => "abyssalruins1f"
    range_incl(167, 181): 93,  # => "reliccastlemaze"
}


def should_change(map_id: int) -> bool:
    if map_id in mapping_single:
        return True
    for rang in mapping_range:
        if map_id in rang:
            return True
    return False


def map_page_index(data: int) -> int:
    if data in mapping_single:
        return mapping_single[data]
    for rang in mapping_range:
        if data in rang:
            return mapping_range[rang]
    return 0
