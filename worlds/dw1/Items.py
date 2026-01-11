from enum import IntEnum
from typing import NamedTuple
from BaseClasses import Item, MultiWorld


class DigimonWorldItemCategory(IntEnum):
    CONSUMABLE = 0,
    MISC = 1,
    EVENT = 2,
    RECRUIT = 3,
    SKIP = 4,
    DV = 5,
    SOUL = 6


class DigimonWorldItemData(NamedTuple):
    name: str
    dw_code: int
    category: DigimonWorldItemCategory


class DigimonWorldItem(Item):
    game: str = "Digimon World"

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 690000
        return {item_data.name: base_id + item_data.dw_code for item_data in _all_items}


key_item_names = {
    "Progressive Stat Cap"
}
key_item_categories = {
    DigimonWorldItemCategory.SOUL, DigimonWorldItemCategory.RECRUIT
}

_all_items = [DigimonWorldItemData(row[0], row[1], row[2]) for row in [    
    ("Agumon Recruited",             1000, DigimonWorldItemCategory.RECRUIT),  
    ("Betamon Recruited",            1001, DigimonWorldItemCategory.RECRUIT),  
    ("Greymon Recruited",            1002, DigimonWorldItemCategory.RECRUIT),  
    ("Devimon Recruited",            1003, DigimonWorldItemCategory.RECRUIT),  
    ("Airdramon Recruited",            1004, DigimonWorldItemCategory.RECRUIT),  
    ("Tyrannomon Recruited",            1005, DigimonWorldItemCategory.RECRUIT),  
    ("Meramon Recruited",            1006, DigimonWorldItemCategory.RECRUIT),  
    ("Seadramon Recruited",            1007, DigimonWorldItemCategory.RECRUIT),  
    ("Numemon Recruited",            1008, DigimonWorldItemCategory.RECRUIT),  
    ("MetalGreymon Recruited",            1009, DigimonWorldItemCategory.RECRUIT),  
    ("Mamemon Recruited",            1010, DigimonWorldItemCategory.RECRUIT),  
    ("Monzaemon Recruited",            1011, DigimonWorldItemCategory.RECRUIT),  
    ("Gabumon Recruited",            1012, DigimonWorldItemCategory.RECRUIT),  
    ("Elecmon Recruited",            1013, DigimonWorldItemCategory.RECRUIT),  
    ("Kabuterimon Recruited",            1014, DigimonWorldItemCategory.RECRUIT),  
    ("Angemon Recruited",            1015, DigimonWorldItemCategory.RECRUIT),  
    ("Birdramon Recruited",            1016, DigimonWorldItemCategory.RECRUIT),  
    ("Garurumon Recruited",            1017, DigimonWorldItemCategory.RECRUIT),  
    ("Frigimon Recruited",            1018, DigimonWorldItemCategory.RECRUIT),  
    ("Whamon Recruited",            1019, DigimonWorldItemCategory.RECRUIT),  
    ("Vegiemon Recruited",            1020, DigimonWorldItemCategory.RECRUIT),  
    ("SkullGreymon Recruited",            1021, DigimonWorldItemCategory.RECRUIT),  
    ("MetalMamemon Recruited",            1022, DigimonWorldItemCategory.RECRUIT),  
    ("Vademon Recruited",            1023, DigimonWorldItemCategory.RECRUIT),  
    ("Patamon Recruited",            1024, DigimonWorldItemCategory.RECRUIT),  
    ("Kunemon Recruited",            1025, DigimonWorldItemCategory.RECRUIT),  
    ("Unimon Recruited",            1026, DigimonWorldItemCategory.RECRUIT),  
    ("Ogremon Recruited",            1027, DigimonWorldItemCategory.RECRUIT),  
    ("Shellmon Recruited",            1028, DigimonWorldItemCategory.RECRUIT),  
    ("Centarumon Recruited",            1029, DigimonWorldItemCategory.RECRUIT),  
    ("Bakemon Recruited",            1030, DigimonWorldItemCategory.RECRUIT),  
    ("Drimogemon Recruited",            1031, DigimonWorldItemCategory.RECRUIT),  
    ("Sukamon Recruited",            1032, DigimonWorldItemCategory.RECRUIT),  
    ("Andromon Recruited",            1033, DigimonWorldItemCategory.RECRUIT),  
    ("Giromon Recruited",            1034, DigimonWorldItemCategory.RECRUIT),  
    ("Etemon Recruited",            1035, DigimonWorldItemCategory.RECRUIT),  
    ("Biyomon Recruited",            1036, DigimonWorldItemCategory.RECRUIT),  
    ("Palmon Recruited",            1037, DigimonWorldItemCategory.RECRUIT),  
    ("Monochromon Recruited",            1038, DigimonWorldItemCategory.RECRUIT),  
    ("Leomon Recruited",            1039, DigimonWorldItemCategory.RECRUIT),  
    ("Coelamon Recruited",            1040, DigimonWorldItemCategory.RECRUIT),  
    ("Kokatorimon Recruited",            1041, DigimonWorldItemCategory.RECRUIT),  
    ("Kuwagamon Recruited",            1042, DigimonWorldItemCategory.RECRUIT),  
    ("Mojyamon Recruited",            1043, DigimonWorldItemCategory.RECRUIT),  
    ("Nanimon Recruited",            1044, DigimonWorldItemCategory.RECRUIT),  
    ("Megadramon Recruited",            1045, DigimonWorldItemCategory.RECRUIT),  
    ("Piximon Recruited",            1046, DigimonWorldItemCategory.RECRUIT),  
    ("Digitamamon Recruited",            1047, DigimonWorldItemCategory.RECRUIT),  
    ("Penguinmon Recruited",            1048, DigimonWorldItemCategory.RECRUIT),  
    ("Ninjamon Recruited",            1049, DigimonWorldItemCategory.RECRUIT),  
    
    ("SM Recovery",            2000, DigimonWorldItemCategory.CONSUMABLE),
    ("Med Recovery",           2001, DigimonWorldItemCategory.CONSUMABLE),
    ("Lrg Recovery",           2002, DigimonWorldItemCategory.CONSUMABLE),
    ("Sup Recovery",           2003, DigimonWorldItemCategory.CONSUMABLE),
    ("MP Floppy",              2004, DigimonWorldItemCategory.CONSUMABLE),
    ("Medium MP",              2005, DigimonWorldItemCategory.CONSUMABLE),
    ("Large MP",               2006, DigimonWorldItemCategory.CONSUMABLE),
    ("Double flop",            2007, DigimonWorldItemCategory.CONSUMABLE),
    ("Various",                2008, DigimonWorldItemCategory.CONSUMABLE),
    ("Omnipotent",             2009, DigimonWorldItemCategory.CONSUMABLE),
    ("Protection",             2010, DigimonWorldItemCategory.CONSUMABLE),
    ("Restore",                2011, DigimonWorldItemCategory.CONSUMABLE),
    ("Sup.restore",            2012, DigimonWorldItemCategory.CONSUMABLE),
    ("Bandage",                2013, DigimonWorldItemCategory.CONSUMABLE),
    ("Medicine",               2014, DigimonWorldItemCategory.CONSUMABLE),
    ("Off. Disk",              2015, DigimonWorldItemCategory.CONSUMABLE),
    ("Def. Disk",              2016, DigimonWorldItemCategory.CONSUMABLE),
    ("Hispeed dsk",            2017, DigimonWorldItemCategory.CONSUMABLE),
    ("Omni Disk",              2018, DigimonWorldItemCategory.CONSUMABLE),
    ("S.Off.disk",             2019, DigimonWorldItemCategory.CONSUMABLE),
    ("S.Def.disk",             2020, DigimonWorldItemCategory.CONSUMABLE),
    ("S.speed.disk",           2021, DigimonWorldItemCategory.CONSUMABLE),
    ("Auto Pilot",             2022, DigimonWorldItemCategory.CONSUMABLE),
    ("Off. Chip",              2023, DigimonWorldItemCategory.CONSUMABLE),
    ("Def. Chip",              2024, DigimonWorldItemCategory.CONSUMABLE),
    ("Brain Chip",             2025, DigimonWorldItemCategory.CONSUMABLE),
    ("Quick Chip",             2026, DigimonWorldItemCategory.CONSUMABLE),
    ("HP Chip",                2027, DigimonWorldItemCategory.CONSUMABLE),
    ("MP Chip",                2028, DigimonWorldItemCategory.CONSUMABLE),
    ("DV Chip A",              2029, DigimonWorldItemCategory.CONSUMABLE),
    ("DV Chip D",              2030, DigimonWorldItemCategory.CONSUMABLE),
    ("DV Chip E",              2031, DigimonWorldItemCategory.CONSUMABLE),
    ("Port. potty",            2032, DigimonWorldItemCategory.CONSUMABLE),
    ("Trn. manual",            2033, DigimonWorldItemCategory.MISC),
    ("Rest pillow",            2034, DigimonWorldItemCategory.MISC),
    ("Enemy repel",            2035, DigimonWorldItemCategory.MISC),
    ("Enemy bell",             2036, DigimonWorldItemCategory.MISC),
    ("Health shoe",            2037, DigimonWorldItemCategory.MISC),
    ("Meat",                   2038, DigimonWorldItemCategory.CONSUMABLE),
    ("Giant Meat",             2039, DigimonWorldItemCategory.CONSUMABLE),
    ("Sirloin",                2040, DigimonWorldItemCategory.CONSUMABLE),
    ("Supercarrot",            2041, DigimonWorldItemCategory.CONSUMABLE),
    ("Hawk radish",            2042, DigimonWorldItemCategory.CONSUMABLE),
    ("Spiny green",            2043, DigimonWorldItemCategory.CONSUMABLE),
    ("Digimushrm",             2044, DigimonWorldItemCategory.CONSUMABLE),
    ("Ice mushrm",             2045, DigimonWorldItemCategory.CONSUMABLE),
    ("Deluxmushrm",            2046, DigimonWorldItemCategory.CONSUMABLE),
    ("Digipine",               2047, DigimonWorldItemCategory.CONSUMABLE),
    ("Blue apple",             2048, DigimonWorldItemCategory.CONSUMABLE),
    ("Red Berry",              2049, DigimonWorldItemCategory.CONSUMABLE),
    ("Gold Acorn",             2050, DigimonWorldItemCategory.CONSUMABLE),
    ("Big Berry",              2051, DigimonWorldItemCategory.CONSUMABLE),
    ("Sweet Nut",              2052, DigimonWorldItemCategory.CONSUMABLE),
    ("Super veggy",            2053, DigimonWorldItemCategory.CONSUMABLE),
    ("Pricklypear",            2054, DigimonWorldItemCategory.CONSUMABLE),
    ("Orange bana",            2055, DigimonWorldItemCategory.CONSUMABLE),
    ("Power fruit",            2056, DigimonWorldItemCategory.CONSUMABLE),
    ("Power Ice",              2057, DigimonWorldItemCategory.CONSUMABLE),
    ("Speed Leaf",             2058, DigimonWorldItemCategory.CONSUMABLE),
    ("Sage Fruit",             2059, DigimonWorldItemCategory.CONSUMABLE),
    ("Muscle Yam",             2060, DigimonWorldItemCategory.CONSUMABLE),
    ("Calm berry",             2061, DigimonWorldItemCategory.CONSUMABLE),
    ("Digianchovy",            2062, DigimonWorldItemCategory.CONSUMABLE),
    ("Digisnapper",            2063, DigimonWorldItemCategory.CONSUMABLE),
    ("DigiTrout",              2064, DigimonWorldItemCategory.CONSUMABLE),
    ("Black trout",            2065, DigimonWorldItemCategory.CONSUMABLE),
    ("Digicatfish",            2066, DigimonWorldItemCategory.CONSUMABLE),
    ("Digiseabass",            2067, DigimonWorldItemCategory.CONSUMABLE),
    ("Moldy Meat",             2068, DigimonWorldItemCategory.CONSUMABLE),
    ("Happymushrm",            2069, DigimonWorldItemCategory.CONSUMABLE),
    ("Chain melon",            2070, DigimonWorldItemCategory.CONSUMABLE),
    ("Grey Claws",             2071, DigimonWorldItemCategory.DV),
    ("Fireball",               2072, DigimonWorldItemCategory.DV),
    ("Flamingwing",            2073, DigimonWorldItemCategory.DV),
    ("Iron Hoof",              2074, DigimonWorldItemCategory.DV),
    ("Mono Stone",             2075, DigimonWorldItemCategory.DV),
    ("Steel drill",            2076, DigimonWorldItemCategory.DV),
    ("White Fang",             2077, DigimonWorldItemCategory.DV),
    ("Black Wing",             2078, DigimonWorldItemCategory.DV),
    ("Spike Club",             2079, DigimonWorldItemCategory.DV),
    ("Flamingmane",            2080, DigimonWorldItemCategory.DV),
    ("White Wing",             2081, DigimonWorldItemCategory.DV),
    ("Torn tatter",            2082, DigimonWorldItemCategory.DV),
    ("Electo ring",            2083, DigimonWorldItemCategory.DV),
    ("Rainbowhorn",            2084, DigimonWorldItemCategory.DV),
    ("Rooster",                2085, DigimonWorldItemCategory.DV),
    ("Unihorn",                2086, DigimonWorldItemCategory.DV),
    ("Horn helmet",            2087, DigimonWorldItemCategory.DV),
    ("Scissor jaw",            2088, DigimonWorldItemCategory.DV),
    ("Fertilizer",             2089, DigimonWorldItemCategory.DV),
    ("Koga laws",              2090, DigimonWorldItemCategory.DV),
    ("Waterbottle",            2091, DigimonWorldItemCategory.DV),
    ("North Star",             2092, DigimonWorldItemCategory.DV),
    ("Red Shell",              2093, DigimonWorldItemCategory.DV),
    ("Hard Scale",             2094, DigimonWorldItemCategory.DV),
    ("Bluecrystal",            2095, DigimonWorldItemCategory.DV),
    ("Ice crystal",            2096, DigimonWorldItemCategory.DV),
    ("Hair grower",            2097, DigimonWorldItemCategory.DV),
    ("Sunglasses",             2098, DigimonWorldItemCategory.DV),
    ("Metal part",             2099, DigimonWorldItemCategory.DV),
    ("Fatal Bone",             2100, DigimonWorldItemCategory.DV),
    ("Cyber part",             2101, DigimonWorldItemCategory.DV),
    ("Mega Hand",              2102, DigimonWorldItemCategory.DV),
    ("Silver ball",            2103, DigimonWorldItemCategory.DV),
    ("Metal armor",            2104, DigimonWorldItemCategory.DV),
    ("Chainsaw",               2105, DigimonWorldItemCategory.DV),
    ("Small spear",            2106, DigimonWorldItemCategory.DV),
    ("X Bandage",              2107, DigimonWorldItemCategory.DV),
    ("Ray Gun",                2108, DigimonWorldItemCategory.DV),
    ("Gold banana",            2109, DigimonWorldItemCategory.DV),
    ("Mysty Egg",              2110, DigimonWorldItemCategory.DV),
    ("Red Ruby",               2111, DigimonWorldItemCategory.DV),
    ("Beetlepearl",            2112, DigimonWorldItemCategory.DV),
    ("Coral charm",            2113, DigimonWorldItemCategory.DV),
    ("Moon mirror",            2114, DigimonWorldItemCategory.DV),
    ("Blue Flute",             2115, DigimonWorldItemCategory.MISC),
    ("old fishrod",            2116, DigimonWorldItemCategory.MISC),
    ("Amazing rod",            2117, DigimonWorldItemCategory.MISC),
    ("Leomonstone",            2118, DigimonWorldItemCategory.MISC),
    ("Mansion key",            2119, DigimonWorldItemCategory.MISC),
    ("Gear",                   2120, DigimonWorldItemCategory.MISC),
    ("Rain Plant",             2121, DigimonWorldItemCategory.CONSUMABLE),
    ("Steak",                  2122, DigimonWorldItemCategory.CONSUMABLE),
    ("Frig Key",               2123, DigimonWorldItemCategory.MISC),
    ("AS Decoder",             2124, DigimonWorldItemCategory.MISC),
    ("Giga Hand",              2125, DigimonWorldItemCategory.DV),
    ("Noble Mane",             2126, DigimonWorldItemCategory.DV),
    ("Metalbanana",            2127, DigimonWorldItemCategory.DV),  
    
    ("Progressive Stat Cap",            3000, DigimonWorldItemCategory.MISC),  
    ("1000 Bits",            3001, DigimonWorldItemCategory.MISC),      
    ("5000 Bits",            3002, DigimonWorldItemCategory.MISC),      
    #("Bridge Fixed",            3001, DigimonWorldItemCategory.EVENT),  
    
    ("Agumon Soul",             4000, DigimonWorldItemCategory.SOUL),  
    ("Betamon Soul",            4001, DigimonWorldItemCategory.SOUL),  
    ("Greymon Soul",            4002, DigimonWorldItemCategory.SOUL),  
    ("Devimon Soul",            4003, DigimonWorldItemCategory.SOUL),  
    ("Airdramon Soul",          4004, DigimonWorldItemCategory.SOUL),  
    ("Tyrannomon Soul",         4005, DigimonWorldItemCategory.SOUL),  
    ("Meramon Soul",            4006, DigimonWorldItemCategory.SOUL),  
    ("Seadramon Soul",          4007, DigimonWorldItemCategory.SOUL),  
    ("Numemon Soul",            4008, DigimonWorldItemCategory.SOUL),  
    ("MetalGreymon Soul",       4009, DigimonWorldItemCategory.SOUL),  
    ("Mamemon Soul",            4010, DigimonWorldItemCategory.SOUL),  
    ("Monzaemon Soul",          4011, DigimonWorldItemCategory.SOUL),  
    ("Gabumon Soul",            4012, DigimonWorldItemCategory.SOUL),  
    ("Elecmon Soul",            4013, DigimonWorldItemCategory.SOUL),  
    ("Kabuterimon Soul",        4014, DigimonWorldItemCategory.SOUL),  
    ("Angemon Soul",            4015, DigimonWorldItemCategory.SOUL),  
    ("Birdramon Soul",          4016, DigimonWorldItemCategory.SOUL),  
    ("Garurumon Soul",          4017, DigimonWorldItemCategory.SOUL),  
    ("Frigimon Soul",           4018, DigimonWorldItemCategory.SOUL),  
    ("Whamon Soul",             4019, DigimonWorldItemCategory.SOUL),  
    ("Vegiemon Soul",           4020, DigimonWorldItemCategory.SOUL),  
    ("SkullGreymon Soul",       4021, DigimonWorldItemCategory.SOUL),  
    ("MetalMamemon Soul",       4022, DigimonWorldItemCategory.SOUL),  
    ("Vademon Soul",            4023, DigimonWorldItemCategory.SOUL),  
    ("Patamon Soul",            4024, DigimonWorldItemCategory.SOUL),  
    ("Kunemon Soul",            4025, DigimonWorldItemCategory.SOUL),  
    ("Unimon Soul",             4026, DigimonWorldItemCategory.SOUL),  
    ("Ogremon Soul",            4027, DigimonWorldItemCategory.SOUL),  
    ("Shellmon Soul",           4028, DigimonWorldItemCategory.SOUL),  
    ("Centarumon Soul",         4029, DigimonWorldItemCategory.SOUL),  
    ("Bakemon Soul",            4030, DigimonWorldItemCategory.SOUL),  
    ("Drimogemon Soul",         4031, DigimonWorldItemCategory.SOUL),  
    ("Sukamon Soul",            4032, DigimonWorldItemCategory.SOUL),  
    ("Andromon Soul",           4033, DigimonWorldItemCategory.SOUL),  
    ("Giromon Soul",            4034, DigimonWorldItemCategory.SOUL),  
    ("Etemon Soul",             4035, DigimonWorldItemCategory.SOUL),  
    ("Biyomon Soul",            4036, DigimonWorldItemCategory.SOUL),  
    ("Palmon Soul",             4037, DigimonWorldItemCategory.SOUL),  
    ("Monochromon Soul",        4038, DigimonWorldItemCategory.SOUL),  
    ("Leomon Soul",             4039, DigimonWorldItemCategory.SOUL),  
    ("Coelamon Soul",           4040, DigimonWorldItemCategory.SOUL),  
    ("Kokatorimon Soul",        4041, DigimonWorldItemCategory.SOUL),  
    ("Kuwagamon Soul",          4042, DigimonWorldItemCategory.SOUL),  
    ("Mojyamon Soul",           4043, DigimonWorldItemCategory.SOUL),  
    ("Nanimon Soul",            4044, DigimonWorldItemCategory.SOUL),  
    ("Megadramon Soul",         4045, DigimonWorldItemCategory.SOUL),  
    ("Piximon Soul",            4046, DigimonWorldItemCategory.SOUL),  
    ("Digitamamon Soul",        4047, DigimonWorldItemCategory.SOUL),  
    ("Penguinmon Soul",         4048, DigimonWorldItemCategory.SOUL),  
    ("Ninjamon Soul",           4049, DigimonWorldItemCategory.SOUL),  
]]

item_descriptions = {
}

item_dictionary = {item_data.name: item_data for item_data in _all_items}


def BuildItemPool(world: MultiWorld, count, options):
    item_pool = []
    remaining_count = count
    if(options.progressive_stats.value):
        if(options.early_statcap.value):
            remaining_count = remaining_count - 8
        else:
            remaining_count = remaining_count - 9
    consumable_count = round(remaining_count * 0.6)
    remaining_count = remaining_count - consumable_count
    dv_count = round(remaining_count * 0.8)
    remaining_count = remaining_count - dv_count
    bit_count = remaining_count
    
    if options.guaranteed_items.value:
        for item_name in options.guaranteed_items.value:
            item = item_dictionary[item_name]
            item_pool.append(item)
            bit_count -= 1
    if(options.progressive_stats.value):
        # add 9 stat cap items to the pool
        if(options.early_statcap.value):            
            for i in range(8):
                item_pool.append(item_dictionary["Progressive Stat Cap"])
        else: 
            for i in range(9):
                item_pool.append(item_dictionary["Progressive Stat Cap"])
    for i in range(consumable_count):
        consumables = [item for item in _all_items if item.category == DigimonWorldItemCategory.CONSUMABLE]
        item = world.random.choice(consumables)
        item_pool.append(item)
    for i in range(dv_count):
        dv = [item for item in _all_items if item.category == DigimonWorldItemCategory.DV]
        item = world.random.choice(dv)
        item_pool.append(item)
    for i in range(bit_count):    
        bit = [item for item in _all_items if "Bits" in item.name]
        item = world.random.choice(bit)
        item_pool.append(item)    
    world.random.shuffle(item_pool)
    return item_pool