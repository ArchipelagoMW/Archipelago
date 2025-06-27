from BaseClasses import ItemClassification, Location
from .options import ItemDropRandomization, Countdown, RequiredSkirmishes, IronMaidenBehavior
from .locations import cvcotm_location_info
from .items import cvcotm_item_info, MAJORS_CLASSIFICATIONS
from .data import iname

from typing import TYPE_CHECKING, Dict, List, Iterable, Tuple, NamedTuple, Optional, TypedDict

if TYPE_CHECKING:
    from . import CVCotMWorld


class StatInfo(TypedDict):
    # Amount this stat increases per Max Up the player starts with.
    amount_per: int
    # The most amount of this stat the player is allowed to start with. Problems arise if the stat  exceeds 9999, so we
    # must ensure it can't if the player raises any class to level 99 as well as collects 255 of that max up. The game
    # caps hearts at 999 automatically, so it doesn't matter so much for that one.
    max_allowed: int
    # The key variable in extra_stats that the stat max up affects.
    variable: str


extra_starting_stat_info: Dict[str, StatInfo] = {
    iname.hp_max: {"amount_per": 10,
                   "max_allowed": 5289,
                   "variable": "extra health"},
    iname.mp_max: {"amount_per": 10,
                   "max_allowed": 3129,
                   "variable": "extra magic"},
    iname.heart_max: {"amount_per": 6,
                      "max_allowed": 999,
                      "variable": "extra hearts"},
}

other_player_subtype_bytes = {
    0xE4: 0x03,
    0xE6: 0x14,
    0xE8: 0x0A
}


class OtherGameAppearancesInfo(TypedDict):
    # What type of item to place for the other player.
    type: int
    # What item to display it as for the other player.
    appearance: int


other_game_item_appearances: Dict[str, Dict[str, OtherGameAppearancesInfo]] = {
    # NOTE: Symphony of the Night and Harmony of Dissonance are custom worlds that are not core verified.
    "Symphony of the Night": {"Life Vessel": {"type": 0xE4,
                                              "appearance": 0x01},
                              "Heart Vessel": {"type": 0xE4,
                                               "appearance": 0x00}},

    "Castlevania - Harmony of Dissonance": {"Life Max Up": {"type": 0xE4,
                                                            "appearance": 0x01},
                                            "Heart Max Up": {"type": 0xE4,
                                                             "appearance": 0x00}},

    "Timespinner": {"Max HP": {"type": 0xE4,
                               "appearance": 0x01},
                    "Max Aura": {"type": 0xE4,
                                 "appearance": 0x02},
                    "Max Sand": {"type": 0xE8,
                                 "appearance": 0x0F}}
}

# 0 = Holy water  22
# 1 = Axe         24
# 2 = Knife       32
# 3 = Cross        6
# 4 = Stopwatch   12
# 5 = Small heart
# 6 = Big heart
rom_sub_weapon_offsets = {
    0xD034E: b"\x01",
    0xD0462: b"\x02",
    0xD064E: b"\x00",
    0xD06F6: b"\x02",
    0xD0882: b"\x00",
    0xD0912: b"\x02",
    0xD0C2A: b"\x02",
    0xD0C96: b"\x01",
    0xD0D92: b"\x02",
    0xD0DCE: b"\x01",
    0xD1332: b"\x00",
    0xD13AA: b"\x01",
    0xD1722: b"\x02",
    0xD17A6: b"\x01",
    0xD1926: b"\x01",
    0xD19AA: b"\x02",
    0xD1A9A: b"\x02",
    0xD1AA6: b"\x00",
    0xD1EBA: b"\x00",
    0xD1ED2: b"\x01",
    0xD2262: b"\x02",
    0xD23B2: b"\x03",
    0xD256E: b"\x02",
    0xD2742: b"\x02",
    0xD2832: b"\x04",
    0xD2862: b"\x01",
    0xD2A2A: b"\x01",
    0xD2DBA: b"\x04",
    0xD2DC6: b"\x00",
    0xD2E02: b"\x02",
    0xD2EFE: b"\x04",
    0xD2F0A: b"\x02",
    0xD302A: b"\x00",
    0xD3042: b"\x01",
    0xD304E: b"\x04",
    0xD3066: b"\x02",
    0xD322E: b"\x04",
    0xD334E: b"\x04",
    0xD3516: b"\x03",
    0xD35CA: b"\x02",
    0xD371A: b"\x01",
    0xD38EE: b"\x00",
    0xD3BE2: b"\x02",
    0xD3D1A: b"\x01",
    0xD3D56: b"\x02",
    0xD3ECA: b"\x00",
    0xD3EE2: b"\x02",
    0xD4056: b"\x01",
    0xD40E6: b"\x04",
    0xD413A: b"\x04",
    0xD4326: b"\x00",
    0xD460E: b"\x00",
    0xD48D2: b"\x00",
    0xD49E6: b"\x01",
    0xD4ABE: b"\x02",
    0xD4B8A: b"\x01",
    0xD4D0A: b"\x04",
    0xD4EAE: b"\x02",
    0xD4F0E: b"\x00",
    0xD4F92: b"\x02",
    0xD4FB6: b"\x01",
    0xD503A: b"\x03",
    0xD5646: b"\x01",
    0xD5682: b"\x02",
    0xD57C6: b"\x02",
    0xD57D2: b"\x02",
    0xD58F2: b"\x00",
    0xD5922: b"\x01",
    0xD5B9E: b"\x02",
    0xD5E26: b"\x01",
    0xD5E56: b"\x02",
    0xD5E7A: b"\x02",
    0xD5F5E: b"\x00",
    0xD69EA: b"\x02",
    0xD69F6: b"\x01",
    0xD6A02: b"\x00",
    0xD6A0E: b"\x04",
    0xD6A1A: b"\x03",
    0xD6BE2: b"\x00",
    0xD6CBA: b"\x01",
    0xD6CDE: b"\x02",
    0xD6EEE: b"\x00",
    0xD6F1E: b"\x02",
    0xD6F42: b"\x01",
    0xD6FC6: b"\x04",
    0xD706E: b"\x00",
    0xD716A: b"\x02",
    0xD72AE: b"\x01",
    0xD75BA: b"\x03",
    0xD76AA: b"\x04",
    0xD76B6: b"\x00",
    0xD76C2: b"\x01",
    0xD76CE: b"\x02",
    0xD76DA: b"\x03",
    0xD7D46: b"\x00",
    0xD7D52: b"\x00",
}

LOW_ITEMS = [
    41,  # Potion
    42,  # Meat
    48,  # Mind Restore
    51,  # Heart
    46,  # Antidote
    47,  # Cure Curse

    17,  # Cotton Clothes
    18,  # Prison Garb
    12,  # Cotton Robe
    1,  # Leather Armor
    2,  # Bronze Armor
    3,  # Gold Armor

    39,  # Toy Ring
    40,  # Bear Ring
    34,  # Wristband
    36,  # Arm Guard
    37,  # Magic Gauntlet
    38,  # Miracle Armband
    35,  # Gauntlet
]

MID_ITEMS = [
    43,  # Spiced Meat
    49,  # Mind High
    52,  # Heart High

    19,  # Stylish Suit
    20,  # Night Suit
    13,  # Silk Robe
    14,  # Rainbow Robe
    4,  # Chainmail
    5,  # Steel Armor
    6,  # Platinum Armor

    24,  # Star Bracelet
    29,  # Cursed Ring
    25,  # Strength Ring
    26,  # Hard Ring
    27,  # Intelligence Ring
    28,  # Luck Ring
    23,  # Double Grips
]

HIGH_ITEMS = [
    44,  # Potion High
    45,  # Potion Ex
    50,  # Mind Ex
    53,  # Heart Ex
    54,  # Heart Mega

    21,  # Ninja Garb
    22,  # Soldier Fatigues
    15,  # Magic Robe
    16,  # Sage Robe

    7,  # Diamond Armor
    8,  # Mirror Armor
    9,  # Needle Armor
    10,  # Dark Armor

    30,  # Strength Armband
    31,  # Defense Armband
    32,  # Sage Armband
    33,  # Gambler Armband
]

COMMON_ITEMS = LOW_ITEMS + MID_ITEMS

RARE_ITEMS = LOW_ITEMS + MID_ITEMS + HIGH_ITEMS


class CVCotMEnemyData(NamedTuple):
    name: str
    hp: int
    attack: int
    defense: int
    exp: int
    type: Optional[str] = None


cvcotm_enemy_info: List[CVCotMEnemyData] = [
    #                Name                  HP   ATK   DEF     EXP
    CVCotMEnemyData("Medusa Head",          6,  120,   60,      2),
    CVCotMEnemyData("Zombie",              48,   70,   20,      2),
    CVCotMEnemyData("Ghoul",              100,  190,   79,      3),
    CVCotMEnemyData("Wight",              110,  235,   87,      4),
    CVCotMEnemyData("Clinking Man",        80,  135,   25,     21),
    CVCotMEnemyData("Zombie Thief",       120,  185,   30,     58),
    CVCotMEnemyData("Skeleton",            25,   65,   45,      4),
    CVCotMEnemyData("Skeleton Bomber",     20,   50,   40,      4),
    CVCotMEnemyData("Electric Skeleton",   42,   80,   50,     30),
    CVCotMEnemyData("Skeleton Spear",      30,   65,   46,      6),
    CVCotMEnemyData("Skeleton Boomerang",  60,  170,   90,    112),
    CVCotMEnemyData("Skeleton Soldier",    35,   90,   60,     16),
    CVCotMEnemyData("Skeleton Knight",     50,  140,   80,     39),
    CVCotMEnemyData("Bone Tower",          84,  201,  280,    160),
    CVCotMEnemyData("Fleaman",             60,  142,   45,     29),
    CVCotMEnemyData("Poltergeist",        105,  360,  380,    510),
    CVCotMEnemyData("Bat",                  5,   50,   15,      4),
    CVCotMEnemyData("Spirit",               9,   55,   17,      1),
    CVCotMEnemyData("Ectoplasm",           12,  165,   51,      2),
    CVCotMEnemyData("Specter",             15,  295,   95,      3),
    CVCotMEnemyData("Axe Armor",           55,  120,  130,     31),
    CVCotMEnemyData("Flame Armor",        160,  320,  300,    280),
    CVCotMEnemyData("Flame Demon",        300,  315,  270,    600),
    CVCotMEnemyData("Ice Armor",          240,  470,  520,   1500),
    CVCotMEnemyData("Thunder Armor",      204,  340,  320,    800),
    CVCotMEnemyData("Wind Armor",         320,  500,  460,   1800),
    CVCotMEnemyData("Earth Armor",        130,  230,  280,    240),
    CVCotMEnemyData("Poison Armor",       260,  382,  310,    822),
    CVCotMEnemyData("Forest Armor",       370,  390,  390,   1280),
    CVCotMEnemyData("Stone Armor",         90,  220,  320,    222),
    CVCotMEnemyData("Ice Demon",          350,  492,  510,   4200),
    CVCotMEnemyData("Holy Armor",         350,  420,  450,   1700),
    CVCotMEnemyData("Thunder Demon",      180,  270,  230,    450),
    CVCotMEnemyData("Dark Armor",         400,  680,  560,   3300),
    CVCotMEnemyData("Wind Demon",         400,  540,  490,   3600),
    CVCotMEnemyData("Bloody Sword",        30,  220,  500,    200),
    CVCotMEnemyData("Golem",              650,  520,  700,   1400),
    CVCotMEnemyData("Earth Demon",        150,   90,   85,     25),
    CVCotMEnemyData("Were-wolf",          160,  265,  110,    140),
    CVCotMEnemyData("Man Eater",          400,  330,  233,    700),
    CVCotMEnemyData("Devil Tower",         10,  140,  200,     17),
    CVCotMEnemyData("Skeleton Athlete",   100,  100,   50,     25),
    CVCotMEnemyData("Harpy",              120,  275,  200,    271),
    CVCotMEnemyData("Siren",              160,  443,  300,    880),
    CVCotMEnemyData("Imp",                 90,  220,   99,    103),
    CVCotMEnemyData("Mudman",              25,   79,   30,      2),
    CVCotMEnemyData("Gargoyle",            60,  160,   66,      3),
    CVCotMEnemyData("Slime",               40,  102,   18,     11),
    CVCotMEnemyData("Frozen Shade",       112,  490,  560,   1212),
    CVCotMEnemyData("Heat Shade",          80,  240,  200,    136),
    CVCotMEnemyData("Poison Worm",        120,   30,   20,     12),
    CVCotMEnemyData("Myconid",             50,  250,  114,     25),
    CVCotMEnemyData("Will O'Wisp",         11,  110,   16,      9),
    CVCotMEnemyData("Spearfish",           40,  360,  450,    280),
    CVCotMEnemyData("Merman",              60,  303,  301,     10),
    CVCotMEnemyData("Minotaur",           410,  520,  640,   2000),
    CVCotMEnemyData("Were-horse",         400,  540,  360,   1970),
    CVCotMEnemyData("Marionette",          80,  160,  150,    127),
    CVCotMEnemyData("Gremlin",             30,   80,   33,      2),
    CVCotMEnemyData("Hopper",              40,   87,   35,      8),
    CVCotMEnemyData("Evil Pillar",         20,  460,  800,    480),
    CVCotMEnemyData("Were-panther",       200,  300,  130,    270),
    CVCotMEnemyData("Were-jaguar",        270,  416,  170,    760),
    CVCotMEnemyData("Bone Head",           24,   60,   80,      7),
    CVCotMEnemyData("Fox Archer",          75,  130,   59,     53),
    CVCotMEnemyData("Fox Hunter",         100,  290,  140,    272),
    CVCotMEnemyData("Were-bear",          265,  250,  140,    227),
    CVCotMEnemyData("Grizzly",            600,  380,  200,    960),
    CVCotMEnemyData("Cerberus",           600,  150,  100,    500, "boss"),
    CVCotMEnemyData("Beast Demon",        150,  330,  250,    260),
    CVCotMEnemyData("Arch Demon",         320,  505,  400,   1000),
    CVCotMEnemyData("Demon Lord",         460,  660,  500,   1950),
    CVCotMEnemyData("Gorgon",             230,  215,  165,    219),
    CVCotMEnemyData("Catoblepas",         550,  500,  430,   1800),
    CVCotMEnemyData("Succubus",           150,  400,  350,    710),
    CVCotMEnemyData("Fallen Angel",       370,  770,  770,   6000),
    CVCotMEnemyData("Necromancer",        500,  200,  250,   2500, "boss"),
    CVCotMEnemyData("Hyena",               93,  140,   70,    105),
    CVCotMEnemyData("Fishhead",            80,  320,  504,    486),
    CVCotMEnemyData("Dryad",              120,  300,  360,    300),
    CVCotMEnemyData("Mimic Candle",       990,  600,  600,   6600, "candle"),
    CVCotMEnemyData("Brain Float",         20,   50,   25,     10),
    CVCotMEnemyData("Evil Hand",           52,  150,  120,     63),
    CVCotMEnemyData("Abiondarg",           88,  388,  188,    388),
    CVCotMEnemyData("Iron Golem",         640,  290,  450,   8000, "boss"),
    CVCotMEnemyData("Devil",             1080,  800,  900,  10000),
    CVCotMEnemyData("Witch",              144,  330,  290,    600),
    CVCotMEnemyData("Mummy",              100,  100,   35,      3),
    CVCotMEnemyData("Hipogriff",          300,  500,  210,    740),
    CVCotMEnemyData("Adramelech",        1800,  380,  360,  16000, "boss"),
    CVCotMEnemyData("Arachne",            330,  420,  288,   1300),
    CVCotMEnemyData("Death Mantis",       200,  318,  240,    400),
    CVCotMEnemyData("Alraune",            774,  490,  303,   2500),
    CVCotMEnemyData("King Moth",          140,  290,  160,    150),
    CVCotMEnemyData("Killer Bee",           8,  308,  108,     88),
    CVCotMEnemyData("Dragon Zombie",     1400,  390,  440,  15000, "boss"),
    CVCotMEnemyData("Lizardman",          100,  345,  400,    800),
    CVCotMEnemyData("Franken",           1200,  700,  350,   2100),
    CVCotMEnemyData("Legion",             420,  610,  375,   1590),
    CVCotMEnemyData("Dullahan",           240,  550,  440,   2200),
    CVCotMEnemyData("Death",              880,  600,  800,  60000, "boss"),
    CVCotMEnemyData("Camilla",           1500,  650,  700,  80000, "boss"),
    CVCotMEnemyData("Hugh",              1400,  570,  750, 120000, "boss"),
    CVCotMEnemyData("Dracula",           1100,  805,  850, 150000, "boss"),
    CVCotMEnemyData("Dracula",           3000, 1000, 1000,      0, "final boss"),
    CVCotMEnemyData("Skeleton Medalist",  250,  100,  100,   1500),
    CVCotMEnemyData("Were-jaguar",        320,  518,  260,   1200, "battle arena"),
    CVCotMEnemyData("Were-wolf",          340,  525,  180,   1100, "battle arena"),
    CVCotMEnemyData("Catoblepas",         560,  510,  435,   2000, "battle arena"),
    CVCotMEnemyData("Hipogriff",          500,  620,  280,   1900, "battle arena"),
    CVCotMEnemyData("Wind Demon",         490,  600,  540,   4000, "battle arena"),
    CVCotMEnemyData("Witch",              210,  480,  340,   1000, "battle arena"),
    CVCotMEnemyData("Stone Armor",        260,  585,  750,   3000, "battle arena"),
    CVCotMEnemyData("Devil Tower",         50,  560,  700,    600, "battle arena"),
    CVCotMEnemyData("Skeleton",           150,  400,  200,    500, "battle arena"),
    CVCotMEnemyData("Skeleton Bomber",    150,  400,  200,    550, "battle arena"),
    CVCotMEnemyData("Electric Skeleton",  150,  400,  200,    700, "battle arena"),
    CVCotMEnemyData("Skeleton Spear",     150,  400,  200,    580, "battle arena"),
    CVCotMEnemyData("Flame Demon",        680,  650,  600,   4500, "battle arena"),
    CVCotMEnemyData("Bone Tower",         120,  500,  650,    800, "battle arena"),
    CVCotMEnemyData("Fox Hunter",         160,  510,  220,    600, "battle arena"),
    CVCotMEnemyData("Poison Armor",       380,  680,  634,   3600, "battle arena"),
    CVCotMEnemyData("Bloody Sword",        55,  600, 1200,   2000, "battle arena"),
    CVCotMEnemyData("Abiondarg",          188,  588,  288,    588, "battle arena"),
    CVCotMEnemyData("Legion",             540,  760,  480,   2900, "battle arena"),
    CVCotMEnemyData("Marionette",         200,  420,  400,   1200, "battle arena"),
    CVCotMEnemyData("Minotaur",           580,  700,  715,   4100, "battle arena"),
    CVCotMEnemyData("Arachne",            430,  590,  348,   2400, "battle arena"),
    CVCotMEnemyData("Succubus",           300,  670,  630,   3100, "battle arena"),
    CVCotMEnemyData("Demon Lord",         590,  800,  656,   4200, "battle arena"),
    CVCotMEnemyData("Alraune",           1003,  640,  450,   5000, "battle arena"),
    CVCotMEnemyData("Hyena",              210,  408,  170,   1000, "battle arena"),
    CVCotMEnemyData("Devil Armor",        500,  804,  714,   6600),
    CVCotMEnemyData("Evil Pillar",         55,  655,  900,   1500, "battle arena"),
    CVCotMEnemyData("White Armor",        640,  770,  807,   7000),
    CVCotMEnemyData("Devil",             1530,  980, 1060,  30000, "battle arena"),
    CVCotMEnemyData("Scary Candle",       150,  300,  300,    900, "candle"),
    CVCotMEnemyData("Trick Candle",       200,  400,  400,   1400, "candle"),
    CVCotMEnemyData("Nightmare",          250,  550,  550,   2000),
    CVCotMEnemyData("Lilim",              400,  800,  800,   8000),
    CVCotMEnemyData("Lilith",             660,  960,  960,  20000),
]
# NOTE: Coffin is omitted from the end of this, as its presence doesn't
# actually impact the randomizer (all stats and drops inherited from Mummy).

BOSS_IDS = [enemy_id for enemy_id in range(len(cvcotm_enemy_info)) if cvcotm_enemy_info[enemy_id].type == "boss"]

ENEMY_TABLE_START = 0xCB2C4

NUMBER_ITEMS = 55

COUNTDOWN_TABLE_ADDR = 0x673400
ITEM_ID_SHINNING_ARMOR = 11


def shuffle_sub_weapons(world: "CVCotMWorld") -> Dict[int, bytes]:
    """Shuffles the sub-weapons amongst themselves."""
    sub_bytes = list(rom_sub_weapon_offsets.values())
    world.random.shuffle(sub_bytes)
    return dict(zip(rom_sub_weapon_offsets, sub_bytes))


def get_countdown_flags(world: "CVCotMWorld", active_locations: Iterable[Location]) -> Dict[int, bytes]:
    """Figures out which Countdown numbers to increase for each Location after verifying the Item on the Location should
    count towards a number.

    Which number to increase is determined by the Location's "countdown" attr in its CVCotMLocationData."""

    next_pos = COUNTDOWN_TABLE_ADDR + 0x40
    countdown_flags: List[List[int]] = [[] for _ in range(16)]
    countdown_dict = {}
    ptr_offset = COUNTDOWN_TABLE_ADDR

    # Loop over every Location.
    for loc in active_locations:
        # If the Location's Item is not Progression/Useful-classified with the "Majors" Countdown being used, or if the
        # Location is the Iron Maiden switch with the vanilla Iron Maiden behavior, skip adding its flag to the arrays.
        if (not loc.item.classification & MAJORS_CLASSIFICATIONS and world.options.countdown ==
                Countdown.option_majors):
            continue

        countdown_index = cvcotm_location_info[loc.name].countdown
        # Take the Location's address if the above condition is satisfied, and get the flag value out of it.
        countdown_flags[countdown_index] += [loc.address & 0xFF, 0]

    # Write the Countdown flag arrays and array pointers correctly. Each flag list should end with a 0xFFFF to indicate
    # the end of an area's list.
    for area_flags in countdown_flags:
        countdown_dict[ptr_offset] = int.to_bytes(next_pos | 0x08000000, 4, "little")
        countdown_dict[next_pos] = bytes(area_flags + [0xFF, 0xFF])
        ptr_offset += 4
        next_pos += len(area_flags) + 2

    return countdown_dict


def get_location_data(world: "CVCotMWorld", active_locations: Iterable[Location]) -> Dict[int, bytes]:
    """Gets ALL the Item data to go into the ROM. Items consist of four bytes; the first two represent the object ID
    for the "category" of item that it belongs to, the third is the sub-value for which item within that "category" it
    is, and the fourth controls the appearance it takes."""

    location_bytes = {}

    for loc in active_locations:
        # Figure out the item ID bytes to put in each Location's offset here.
        # If it's a CotM Item, always write the Item's primary type byte.
        if loc.item.game == "Castlevania - Circle of the Moon":
            type_byte = cvcotm_item_info[loc.item.name].code >> 8

            # If the Item is for this player, set the subtype to actually be that Item.
            # Otherwise, set a dummy subtype value that is different for every item type.
            if loc.item.player == world.player:
                subtype_byte = cvcotm_item_info[loc.item.name].code & 0xFF
            else:
                subtype_byte = other_player_subtype_bytes[type_byte]

            # If it's a DSS Card, set the appearance based on whether it's progression or not; freeze combo cards should
            # all appear blue in color while the others are standard purple/yellow. Otherwise, set the appearance the
            # same way as the subtype for local items regardless of whether it's actually local or not.
            if type_byte == 0xE6:
                if loc.item.advancement:
                    appearance_byte = 1
                else:
                    appearance_byte = 0
            else:
                appearance_byte = cvcotm_item_info[loc.item.name].code & 0xFF

        # If it's not a CotM Item at all, always set the primary type to that of a Magic Item and the subtype to that of
        # a dummy item. The AP Items are all under Magic Items.
        else:
            type_byte = 0xE8
            subtype_byte = 0x0A
            # Decide which AP Item to use to represent the other game item.
            if loc.item.classification & ItemClassification.progression and \
                    loc.item.classification & ItemClassification.useful:
                appearance_byte = 0x0E  # Progression + Useful
            elif loc.item.classification & ItemClassification.progression:
                appearance_byte = 0x0C  # Progression
            elif loc.item.classification & ItemClassification.useful:
                appearance_byte = 0x0B  # Useful
            elif loc.item.classification & ItemClassification.trap:
                appearance_byte = 0x0D  # Trap
            else:
                appearance_byte = 0x0A  # Filler

            # Check if the Item's game is in the other game item appearances' dict, and if so, if the Item is under that
            # game's name. If it is, change the appearance accordingly.
            # Right now, only SotN and Timespinner stat ups are supported.
            other_game_name = world.multiworld.worlds[loc.item.player].game
            if other_game_name in other_game_item_appearances:
                if loc.item.name in other_game_item_appearances[other_game_name]:
                    type_byte = other_game_item_appearances[other_game_name][loc.item.name]["type"]
                    subtype_byte = other_player_subtype_bytes[type_byte]
                    appearance_byte = other_game_item_appearances[other_game_name][loc.item.name]["appearance"]

        # Create the correct bytes object for the Item on that Location.
        location_bytes[cvcotm_location_info[loc.name].offset] = bytes([type_byte, 1, subtype_byte, appearance_byte])
    return location_bytes


def populate_enemy_drops(world: "CVCotMWorld") -> Dict[int, bytes]:
    """Randomizes the enemy-dropped items throughout the game within each other. There are three tiers of item drops:
    Low, Mid, and High. Each enemy has two item slots that can both drop its own item; a Common slot and a Rare one.

    On Normal item randomization, easy enemies (below 61 HP) will only have Low-tier drops in both of their stats,
    bosses and candle enemies will be guaranteed to have High drops in one or both of their slots respectively (bosses
    are made to only drop one slot 100% of the time), and everything else can have a Low or Mid-tier item in its Common
    drop slot and a Low, Mid, OR High-tier item in its Rare drop slot.

    If Item Drop Randomization is set to Tiered, the HP threshold for enemies being considered "easily" will raise to
    below 144, enemies in the 144-369 HP range (inclusive) will have a Low-tier item in its Common slot and a Mid-tier
    item in its rare slot, and enemies with more than 369 HP will have a Mid-tier in its Common slot and a High-tier in
    its Rare slot. Candles and bosses still have Rares in all their slots, but now the guaranteed drops that land on
    bosses will be exclusive to them; no other enemy in the game will have their item.

    This and select_drop are the most directly adapted code from upstream CotMR in this package by far. Credit where
    it's due to Spooky for writing the original, and Malaert64 for further refinements and updating what used to be
    Random Item Hardmode to instead be Tiered Item Mode. The original C code this was adapted from can be found here:
    https://github.com/calm-palm/cotm-randomizer/blob/master/Program/randomizer.c#L1028"""

    placed_low_items = [0] * len(LOW_ITEMS)
    placed_mid_items = [0] * len(MID_ITEMS)
    placed_high_items = [0] * len(HIGH_ITEMS)

    placed_common_items = [0] * len(COMMON_ITEMS)
    placed_rare_items = [0] * len(RARE_ITEMS)

    regular_drops = [0] * len(cvcotm_enemy_info)
    regular_drop_chances = [0] * len(cvcotm_enemy_info)
    rare_drops = [0] * len(cvcotm_enemy_info)
    rare_drop_chances = [0] * len(cvcotm_enemy_info)

    # Set boss items first to prevent boss drop duplicates.
    # If Tiered mode is enabled, make these items exclusive to these enemies by adding an arbitrary integer larger
    # than could be reached normally (e.g.the total number of enemies) and use the placed high items array instead of
    # the placed rare items one.
    if world.options.item_drop_randomization == ItemDropRandomization.option_tiered:
        for boss_id in BOSS_IDS:
            regular_drops[boss_id] = select_drop(world, HIGH_ITEMS, placed_high_items, True)
    else:
        for boss_id in BOSS_IDS:
            regular_drops[boss_id] = select_drop(world, RARE_ITEMS, placed_rare_items, start_index=len(COMMON_ITEMS))

    # Setting drop logic for all enemies.
    for i in range(len(cvcotm_enemy_info)):

        # Give Dracula II Shining Armor occasionally as a joke.
        if cvcotm_enemy_info[i].type == "final boss":
            regular_drops[i] = rare_drops[i] = ITEM_ID_SHINNING_ARMOR
            regular_drop_chances[i] = rare_drop_chances[i] = 5000

        # Set bosses' secondary item to none since we already set the primary item earlier.
        elif cvcotm_enemy_info[i].type == "boss":
            # Set rare drop to none.
            rare_drops[i] = 0

            # Max out rare boss drops (normally, drops are capped to 50% and 25% for common and rare respectively, but
            # Fuse's patch AllowAlwaysDrop.ips allows setting the regular item drop chance to 10000 to force a drop
            # always)
            regular_drop_chances[i] = 10000
            rare_drop_chances[i] = 0

        # Candle enemies use a similar placement logic to the bosses, except items that land on them are NOT exclusive
        # to them on Tiered mode.
        elif cvcotm_enemy_info[i].type == "candle":
            if world.options.item_drop_randomization == ItemDropRandomization.option_tiered:
                regular_drops[i] = select_drop(world, HIGH_ITEMS, placed_high_items)
                rare_drops[i] = select_drop(world, HIGH_ITEMS, placed_high_items)
            else:
                regular_drops[i] = select_drop(world, RARE_ITEMS, placed_rare_items, start_index=len(COMMON_ITEMS))
                rare_drops[i] = select_drop(world, RARE_ITEMS, placed_rare_items, start_index=len(COMMON_ITEMS))

            # Set base drop chances at 20-30% for common and 15-20% for rare.
            regular_drop_chances[i] = 2000 + world.random.randint(0, 1000)
            rare_drop_chances[i] = 1500 + world.random.randint(0, 500)

        # On All Bosses and Battle Arena Required, the Shinning Armor at the end of Battle Arena is removed.
        # We compensate for this by giving the Battle Arena Devil a 100% chance to drop Shinning Armor.
        elif cvcotm_enemy_info[i].name == "Devil" and cvcotm_enemy_info[i].type == "battle arena" and \
                world.options.required_skirmishes == RequiredSkirmishes.option_all_bosses_and_arena:
            regular_drops[i] = ITEM_ID_SHINNING_ARMOR
            rare_drops[i] = 0

            regular_drop_chances[i] = 10000
            rare_drop_chances[i] = 0

        # Low-tier items drop from enemies that are trivial to farm (60 HP or less)
        # on Normal drop logic, or enemies under 144 HP on Tiered logic.
        elif (world.options.item_drop_randomization == ItemDropRandomization.option_normal and
              cvcotm_enemy_info[i].hp <= 60) or \
                (world.options.item_drop_randomization == ItemDropRandomization.option_tiered and
                 cvcotm_enemy_info[i].hp <= 143):
            # Low-tier enemy drops.
            regular_drops[i] = select_drop(world, LOW_ITEMS, placed_low_items)
            rare_drops[i] = select_drop(world, LOW_ITEMS, placed_low_items)

            # Set base drop chances at 6-10% for common and 3-6% for rare.
            regular_drop_chances[i] = 600 + world.random.randint(0, 400)
            rare_drop_chances[i] = 300 + world.random.randint(0, 300)

        # Rest of Tiered logic, by Malaert64.
        elif world.options.item_drop_randomization == ItemDropRandomization.option_tiered:
            # If under 370 HP, mid-tier enemy.
            if cvcotm_enemy_info[i].hp <= 369:
                regular_drops[i] = select_drop(world, LOW_ITEMS, placed_low_items)
                rare_drops[i] = select_drop(world, MID_ITEMS, placed_mid_items)
            # Otherwise, enemy HP is 370+, thus high-tier enemy.
            else:
                regular_drops[i] = select_drop(world, MID_ITEMS, placed_mid_items)
                rare_drops[i] = select_drop(world, HIGH_ITEMS, placed_high_items)

            # Set base drop chances at 6-10% for common and 3-6% for rare.
            regular_drop_chances[i] = 600 + world.random.randint(0, 400)
            rare_drop_chances[i] = 300 + world.random.randint(0, 300)

        # Regular enemies outside Tiered logic.
        else:
            # Select a random regular and rare drop for every enemy from their respective lists.
            regular_drops[i] = select_drop(world, COMMON_ITEMS, placed_common_items)
            rare_drops[i] = select_drop(world, RARE_ITEMS, placed_rare_items)

            # Set base drop chances at 6-10% for common and 3-6% for rare.
            regular_drop_chances[i] = 600 + world.random.randint(0, 400)
            rare_drop_chances[i] = 300 + world.random.randint(0, 300)

    # Return the randomized drop data as bytes with their respective offsets.
    enemy_address = ENEMY_TABLE_START
    drop_data = {}
    for i, enemy_info in enumerate(cvcotm_enemy_info):
        drop_data[enemy_address] = bytes([regular_drops[i], 0, regular_drop_chances[i] & 0xFF,
                                          regular_drop_chances[i] >> 8, rare_drops[i], 0, rare_drop_chances[i] & 0xFF,
                                          rare_drop_chances[i] >> 8])
        enemy_address += 20

    return drop_data


def select_drop(world: "CVCotMWorld", drop_list: List[int], drops_placed: List[int], exclusive_drop: bool = False,
                start_index: int = 0) -> int:
    """Chooses a drop from a given list of drops based on another given list of how many drops from that list were
    selected before. In order to ensure an even number of drops are distributed, drops that were selected the least are
    the ones that will be picked from.

    Calling this with exclusive_drop param being True will force the number of the chosen item really high to ensure it
    will never be picked again."""

    # Take the list of placed item drops beginning from the starting index.
    drops_from_start_index = drops_placed[start_index:]

    # Determine the lowest drop counts and the indices with that drop count.
    lowest_number = min(drops_from_start_index)
    indices_with_lowest_number = [index for index, placed in enumerate(drops_from_start_index) if
                                  placed == lowest_number]

    random_index = world.random.choice(indices_with_lowest_number)
    random_index += start_index  # Add start_index back on

    # Increment the number of this item placed, unless it should be exclusive to the boss / candle, in which case
    # set it to an arbitrarily large number to make it exclusive.
    if exclusive_drop:
        drops_placed[random_index] += 999
    else:
        drops_placed[random_index] += 1

    # Return the in-game item ID of the chosen item.
    return drop_list[random_index]


def get_start_inventory_data(world: "CVCotMWorld") -> Tuple[Dict[int, bytes], bool]:
    """Calculate and return the starting inventory arrays. Different items go into different arrays, so they all have
    to be handled accordingly."""
    start_inventory_data = {}

    magic_items_array = [0 for _ in range(8)]
    cards_array = [0 for _ in range(20)]
    extra_stats = {"extra health": 0,
                   "extra magic": 0,
                   "extra hearts": 0}
    start_with_detonator = False
    # If the Iron Maiden Behavior option is set to Start Broken, consider ourselves starting with the Maiden Detonator.
    if world.options.iron_maiden_behavior == IronMaidenBehavior.option_start_broken:
        start_with_detonator = True

    # Always start with the Dash Boots.
    magic_items_array[0] = 1

    for item in world.multiworld.precollected_items[world.player]:

        array_offset = item.code & 0xFF

        # If it's a Maiden Detonator we're starting with, set the boolean for it to True.
        if item.name == iname.ironmaidens:
            start_with_detonator = True
        # If it's a Max Up we're starting with, check if increasing the extra amount of that stat will put us over the
        # max amount of the stat allowed. If it will, set the current extra amount to the max. Otherwise, increase it by
        # the amount that it should.
        elif "Max Up" in item.name:
            info = extra_starting_stat_info[item.name]
            if extra_stats[info["variable"]] + info["amount_per"] > info["max_allowed"]:
                extra_stats[info["variable"]] = info["max_allowed"]
            else:
                extra_stats[info["variable"]] += info["amount_per"]
        # If it's a DSS card we're starting with, set that card's value in the cards array.
        elif "Card" in item.name:
            cards_array[array_offset] = 1
        # If it's none of the above, it has to be a regular Magic Item.
        # Increase that Magic Item's value in the Magic Items array if it's not greater than 240. Last Keys are the only
        # Magic Item wherein having more than one is relevant.
        else:
            # Decrease the Magic Item array offset by 1 if it's higher than the unused Map's item value.
            if array_offset > 5:
                array_offset -= 1
            if magic_items_array[array_offset] < 240:
                magic_items_array[array_offset] += 1

    # Add the start inventory arrays to the offset data in bytes form.
    start_inventory_data[0x680080] = bytes(magic_items_array)
    start_inventory_data[0x6800A0] = bytes(cards_array)

    # Add the extra max HP/MP/Hearts to all classes' base stats. Doing it this way makes us less likely to hit the max
    # possible Max Ups.
    # Vampire Killer
    start_inventory_data[0xE08C6] = int.to_bytes(100 + extra_stats["extra health"], 2, "little")
    start_inventory_data[0xE08CE] = int.to_bytes(100 + extra_stats["extra magic"], 2, "little")
    start_inventory_data[0xE08D4] = int.to_bytes(50 + extra_stats["extra hearts"], 2, "little")

    # Magician
    start_inventory_data[0xE090E] = int.to_bytes(50 + extra_stats["extra health"], 2, "little")
    start_inventory_data[0xE0916] = int.to_bytes(400 + extra_stats["extra magic"], 2, "little")
    start_inventory_data[0xE091C] = int.to_bytes(50 + extra_stats["extra hearts"], 2, "little")

    # Fighter
    start_inventory_data[0xE0932] = int.to_bytes(200 + extra_stats["extra health"], 2, "little")
    start_inventory_data[0xE093A] = int.to_bytes(50 + extra_stats["extra magic"], 2, "little")
    start_inventory_data[0xE0940] = int.to_bytes(50 + extra_stats["extra hearts"], 2, "little")

    # Shooter
    start_inventory_data[0xE0832] = int.to_bytes(50 + extra_stats["extra health"], 2, "little")
    start_inventory_data[0xE08F2] = int.to_bytes(100 + extra_stats["extra magic"], 2, "little")
    start_inventory_data[0xE08F8] = int.to_bytes(250 + extra_stats["extra hearts"], 2, "little")

    # Thief
    start_inventory_data[0xE0956] = int.to_bytes(50 + extra_stats["extra health"], 2, "little")
    start_inventory_data[0xE095E] = int.to_bytes(50 + extra_stats["extra magic"], 2, "little")
    start_inventory_data[0xE0964] = int.to_bytes(50 + extra_stats["extra hearts"], 2, "little")

    return start_inventory_data, start_with_detonator
