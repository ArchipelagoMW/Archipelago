from . import Rom

major_locations = [
    "Starting Sword Cave",
    "White Sword Pond",
    "Magical Sword Grave",
    "Take Any Item Left",
    "Take Any Item Middle",
    "Take Any Item Right",
    "Armos Knights",
    "Ocean Heart Container",
    "Letter Cave",
]

level_locations = [
    [
        "Level 1 Item (Bow)", "Level 1 Item (Boomerang)", "Level 1 Map", "Level 1 Compass", "Level 1 Boss",
        "Level 1 Triforce", "Level 1 Key Drop (Keese Entrance)", "Level 1 Key Drop (Stalfos Middle)",
        "Level 1 Key Drop (Moblins)", "Level 1 Key Drop (Stalfos Water)",
        "Level 1 Key Drop (Stalfos Entrance)", "Level 1 Key Drop (Wallmasters)",
    ],
    [
        "Level 2 Item (Magical Boomerang)", "Level 2 Map", "Level 2 Compass", "Level 2 Boss", "Level 2 Triforce",
        "Level 2 Key Drop (Ropes West)", "Level 2 Key Drop (Moldorms)",
        "Level 2 Key Drop (Ropes Middle)", "Level 2 Key Drop (Ropes Entrance)",
        "Level 2 Bomb Drop (Keese)", "Level 2 Bomb Drop (Moblins)",
        "Level 2 Rupee Drop (Gels)",
    ],
    [
        "Level 3 Item (Raft)", "Level 3 Map", "Level 3 Compass", "Level 3 Boss", "Level 3 Triforce",
        "Level 3 Key Drop (Zols and Keese West)", "Level 3 Key Drop (Keese North)",
        "Level 3 Key Drop (Zols Central)", "Level 3 Key Drop (Zols South)",
        "Level 3 Key Drop (Zols Entrance)", "Level 3 Bomb Drop (Darknuts West)",
        "Level 3 Bomb Drop (Keese Corridor)", "Level 3 Bomb Drop (Darknuts Central)",
        "Level 3 Rupee Drop (Zols and Keese East)"
    ],
    [
        "Level 4 Item (Stepladder)", "Level 4 Map", "Level 4 Compass", "Level 4 Boss", "Level 4 Triforce",
        "Level 4 Key Drop (Keese Entrance)", "Level 4 Key Drop (Keese Central)",
        "Level 4 Key Drop (Zols)", "Level 4 Key Drop (Keese North)",
    ],
    [
        "Level 5 Item (Recorder)", "Level 5 Map", "Level 5 Compass", "Level 5 Boss", "Level 5 Triforce",
        "Level 5 Key Drop (Keese North)", "Level 5 Key Drop (Gibdos North)",
        "Level 5 Key Drop (Gibdos Central)", "Level 5 Key Drop (Pols Voice Entrance)",
        "Level 5 Key Drop (Gibdos Entrance)", "Level 5 Key Drop (Gibdos, Keese, and Pols Voice)",
        "Level 5 Key Drop (Zols)", "Level 5 Bomb Drop (Gibdos)",
        "Level 5 Bomb Drop (Dodongos)", "Level 5 Rupee Drop (Zols)",
    ],
    [
        "Level 6 Item (Magical Rod)", "Level 6 Map", "Level 6 Compass", "Level 6 Boss", "Level 6 Triforce",
        "Level 6 Key Drop (Wizzrobes Entrance)", "Level 6 Key Drop (Keese)",
        "Level 6 Key Drop (Wizzrobes North Island)", "Level 6 Key Drop (Wizzrobes North Stream)",
        "Level 6 Key Drop (Vires)", "Level 6 Bomb Drop (Wizzrobes)",
        "Level 6 Rupee Drop (Wizzrobes)"
    ],
    [
        "Level 7 Item (Red Candle)", "Level 7 Map", "Level 7 Compass", "Level 7 Boss", "Level 7 Triforce",
        "Level 7 Key Drop (Ropes)", "Level 7 Key Drop (Goriyas)", "Level 7 Key Drop (Stalfos)",
        "Level 7 Key Drop (Moldorms)", "Level 7 Bomb Drop (Goriyas South)", "Level 7 Bomb Drop (Keese and Spikes)",
        "Level 7 Bomb Drop (Moldorms South)", "Level 7 Bomb Drop (Moldorms North)",
        "Level 7 Bomb Drop (Goriyas North)", "Level 7 Bomb Drop (Dodongos)",
        "Level 7 Bomb Drop (Digdogger)", "Level 7 Rupee Drop (Goriyas Central)",
        "Level 7 Rupee Drop (Dodongos)", "Level 7 Rupee Drop (Goriyas North)",
    ],
    [
        "Level 8 Item (Magical Key)", "Level 8 Map", "Level 8 Compass", "Level 8 Item (Book of Magic)", "Level 8 Boss",
        "Level 8 Triforce", "Level 8 Key Drop (Darknuts West)",
        "Level 8 Key Drop (Darknuts Far West)", "Level 8 Key Drop (Pols Voice South)",
        "Level 8 Key Drop (Pols Voice and Keese)", "Level 8 Key Drop (Darknuts Central)",
        "Level 8 Key Drop (Keese and Zols Entrance)", "Level 8 Bomb Drop (Darknuts North)",
        "Level 8 Bomb Drop (Darknuts East)", "Level 8 Bomb Drop (Pols Voice North)",
        "Level 8 Rupee Drop (Manhandla Entrance West)", "Level 8 Rupee Drop (Manhandla Entrance North)",
        "Level 8 Rupee Drop (Darknuts and Gibdos)",
    ],
    [
        "Level 9 Item (Silver Arrow)", "Level 9 Item (Red Ring)",
        "Level 9 Map", "Level 9 Compass",
        "Level 9 Key Drop (Patra Southwest)", "Level 9 Key Drop (Like Likes and Zols East)",
        "Level 9 Key Drop (Wizzrobes and Bubbles East)", "Level 9 Key Drop (Wizzrobes East Island)",
        "Level 9 Bomb Drop (Blue Lanmolas)", "Level 9 Bomb Drop (Gels Lake)",
        "Level 9 Bomb Drop (Like Likes and Zols Corridor)", "Level 9 Bomb Drop (Patra Northeast)",
        "Level 9 Bomb Drop (Vires)", "Level 9 Rupee Drop (Wizzrobes West Island)",
        "Level 9 Rupee Drop (Red Lanmolas)", "Level 9 Rupee Drop (Keese Southwest)",
        "Level 9 Rupee Drop (Keese Central Island)", "Level 9 Rupee Drop (Wizzrobes Central)",
        "Level 9 Rupee Drop (Wizzrobes North Island)", "Level 9 Rupee Drop (Gels East)"
    ]
]

all_level_locations = [location for level in level_locations for location in level]

standard_level_locations = [location for level in level_locations for location in level if "Drop" not in location]

shop_locations = [
    "Arrow Shop Item Left", "Arrow Shop Item Middle", "Arrow Shop Item Right",
    "Candle Shop Item Left", "Candle Shop Item Middle", "Candle Shop Item Right",
    "Blue Ring Shop Item Left", "Blue Ring Shop Item Middle", "Blue Ring Shop Item Right",
    "Shield Shop Item Left", "Shield Shop Item Middle", "Shield Shop Item Right",
    "Potion Shop Item Left", "Potion Shop Item Middle", "Potion Shop Item Right"
]

take_any_locations = [
    "Take Any Item Left", "Take Any Item Middle", "Take Any Item Right"
]

sword_cave_locations = [
    "Starting Sword Cave", "White Sword Pond", "Magical Sword Grave"
]

food_locations = [
    "Level 7 Item (Red Candle)", "Level 7 Map", "Level 7 Boss", "Level 7 Triforce", "Level 7 Key Drop (Goriyas)",
    "Level 7 Bomb Drop (Moldorms North)", "Level 7 Bomb Drop (Goriyas North)",
    "Level 7 Bomb Drop (Dodongos)", "Level 7 Rupee Drop (Goriyas North)"
]

gohma_locations = [
    "Level 6 Boss", "Level 6 Triforce", "Level 8 Item (Magical Key)", "Level 8 Bomb Drop (Darknuts North)"
]

gleeok_locations = [
    "Level 4 Boss", "Level 4 Triforce", "Level 8 Boss", "Level 8 Triforce"
]

floor_location_game_offsets_early = {
    "Level 1 Item (Bow)": 0x7F,
    "Level 1 Item (Boomerang)": 0x44,
    "Level 1 Map": 0x43,
    "Level 1 Compass": 0x54,
    "Level 1 Boss": 0x35,
    "Level 1 Triforce": 0x36,
    "Level 1 Key Drop (Keese Entrance)": 0x72,
    "Level 1 Key Drop (Moblins)": 0x23,
    "Level 1 Key Drop (Stalfos Water)": 0x33,
    "Level 1 Key Drop (Stalfos Entrance)": 0x74,
    "Level 1 Key Drop (Stalfos Middle)": 0x53,
    "Level 1 Key Drop (Wallmasters)": 0x45,
    "Level 2 Item (Magical Boomerang)": 0x4F,
    "Level 2 Map": 0x5F,
    "Level 2 Compass": 0x6F,
    "Level 2 Boss": 0x0E,
    "Level 2 Triforce": 0x0D,
    "Level 2 Key Drop (Ropes West)": 0x6C,
    "Level 2 Key Drop (Moldorms)": 0x3E,
    "Level 2 Key Drop (Ropes Middle)": 0x4E,
    "Level 2 Key Drop (Ropes Entrance)": 0x7E,
    "Level 2 Bomb Drop (Keese)": 0x3F,
    "Level 2 Bomb Drop (Moblins)": 0x1E,
    "Level 2 Rupee Drop (Gels)": 0x2F,
    "Level 3 Item (Raft)": 0x0F,
    "Level 3 Map": 0x4C,
    "Level 3 Compass": 0x5A,
    "Level 3 Boss": 0x4D,
    "Level 3 Triforce": 0x3D,
    "Level 3 Key Drop (Zols and Keese West)": 0x49,
    "Level 3 Key Drop (Keese North)": 0x2A,
    "Level 3 Key Drop (Zols Central)": 0x4B,
    "Level 3 Key Drop (Zols South)": 0x6B,
    "Level 3 Key Drop (Zols Entrance)": 0x7B,
    "Level 3 Bomb Drop (Darknuts West)": 0x69,
    "Level 3 Bomb Drop (Keese Corridor)": 0x4A,
    "Level 3 Bomb Drop (Darknuts Central)": 0x5B,
    "Level 3 Rupee Drop (Zols and Keese East)": 0x5D,
    "Level 4 Item (Stepladder)": 0x60,
    "Level 4 Map": 0x21,
    "Level 4 Compass": 0x62,
    "Level 4 Boss": 0x13,
    "Level 4 Triforce": 0x03,
    "Level 4 Key Drop (Keese Entrance)": 0x70,
    "Level 4 Key Drop (Keese Central)": 0x51,
    "Level 4 Key Drop (Zols)": 0x40,
    "Level 4 Key Drop (Keese North)": 0x01,
    "Level 5 Item (Recorder)": 0x04,
    "Level 5 Map": 0x46,
    "Level 5 Compass": 0x37,
    "Level 5 Boss": 0x24,
    "Level 5 Triforce": 0x14,
    "Level 5 Key Drop (Keese North)": 0x16,
    "Level 5 Key Drop (Gibdos North)": 0x26,
    "Level 5 Key Drop (Gibdos Central)": 0x47,
    "Level 5 Key Drop (Pols Voice Entrance)": 0x77,
    "Level 5 Key Drop (Gibdos Entrance)": 0x66,
    "Level 5 Key Drop (Gibdos, Keese, and Pols Voice)": 0x27,
    "Level 5 Key Drop (Zols)": 0x55,
    "Level 5 Bomb Drop (Gibdos)": 0x65,
    "Level 5 Bomb Drop (Dodongos)": 0x56,
    "Level 5 Rupee Drop (Zols)": 0x57,
    "Level 6 Item (Magical Rod)": 0x75,
    "Level 6 Map": 0x19,
    "Level 6 Compass": 0x68,
    "Level 6 Boss": 0x1C,
    "Level 6 Triforce": 0x0C,
    "Level 6 Key Drop (Wizzrobes Entrance)": 0x7A,
    "Level 6 Key Drop (Keese)": 0x58,
    "Level 6 Key Drop (Wizzrobes North Island)": 0x29,
    "Level 6 Key Drop (Wizzrobes North Stream)": 0x1A,
    "Level 6 Key Drop (Vires)": 0x2D,
    "Level 6 Bomb Drop (Wizzrobes)": 0x3C,
    "Level 6 Rupee Drop (Wizzrobes)": 0x28
}

floor_location_game_ids_early = {}
for key, value in floor_location_game_offsets_early.items():
    floor_location_game_ids_early[key] = value + Rom.first_quest_dungeon_items_early

floor_location_game_offsets_late = {
    "Level 7 Item (Red Candle)": 0x4A,
    "Level 7 Map": 0x18,
    "Level 7 Compass": 0x5A,
    "Level 7 Boss": 0x2A,
    "Level 7 Triforce": 0x2B,
    "Level 7 Key Drop (Ropes)": 0x78,
    "Level 7 Key Drop (Goriyas)": 0x0A,
    "Level 7 Key Drop (Stalfos)": 0x6D,
    "Level 7 Key Drop (Moldorms)": 0x3A,
    "Level 7 Bomb Drop (Goriyas South)": 0x69,
    "Level 7 Bomb Drop (Keese and Spikes)": 0x68,
    "Level 7 Bomb Drop (Moldorms South)": 0x7A,
    "Level 7 Bomb Drop (Moldorms North)": 0x0B,
    "Level 7 Bomb Drop (Goriyas North)": 0x1B,
    "Level 7 Bomb Drop (Dodongos)": 0x0C,
    "Level 7 Bomb Drop (Digdogger)": 0x6C,
    "Level 7 Rupee Drop (Goriyas Central)": 0x38,
    "Level 7 Rupee Drop (Dodongos)": 0x58,
    "Level 7 Rupee Drop (Goriyas North)": 0x09,
    "Level 8 Item (Magical Key)": 0x0F,
    "Level 8 Item (Book of Magic)": 0x6F,
    "Level 8 Map": 0x2E,
    "Level 8 Compass": 0x5F,
    "Level 8 Boss": 0x3C,
    "Level 8 Triforce": 0x2C,
    "Level 8 Key Drop (Darknuts West)": 0x5C,
    "Level 8 Key Drop (Darknuts Far West)": 0x4B,
    "Level 8 Key Drop (Pols Voice South)": 0x4C,
    "Level 8 Key Drop (Pols Voice and Keese)": 0x5D,
    "Level 8 Key Drop (Darknuts Central)": 0x5E,
    "Level 8 Key Drop (Keese and Zols Entrance)": 0x7F,
    "Level 8 Bomb Drop (Darknuts North)": 0x0E,
    "Level 8 Bomb Drop (Darknuts East)": 0x3F,
    "Level 8 Bomb Drop (Pols Voice North)": 0x1D,
    "Level 8 Rupee Drop (Manhandla Entrance West)": 0x7D,
    "Level 8 Rupee Drop (Manhandla Entrance North)": 0x6E,
    "Level 8 Rupee Drop (Darknuts and Gibdos)": 0x4E,
    "Level 9 Item (Silver Arrow)": 0x4F,
    "Level 9 Item (Red Ring)": 0x00,
    "Level 9 Map": 0x27,
    "Level 9 Compass": 0x35,
    "Level 9 Key Drop (Patra Southwest)": 0x61,
    "Level 9 Key Drop (Like Likes and Zols East)": 0x56,
    "Level 9 Key Drop (Wizzrobes and Bubbles East)": 0x47,
    "Level 9 Key Drop (Wizzrobes East Island)": 0x57,
    "Level 9 Bomb Drop (Blue Lanmolas)": 0x11,
    "Level 9 Bomb Drop (Gels Lake)": 0x23,
    "Level 9 Bomb Drop (Like Likes and Zols Corridor)": 0x25,
    "Level 9 Bomb Drop (Patra Northeast)": 0x16,
    "Level 9 Bomb Drop (Vires)": 0x37,
    "Level 9 Rupee Drop (Wizzrobes West Island)": 0x40,
    "Level 9 Rupee Drop (Red Lanmolas)": 0x12,
    "Level 9 Rupee Drop (Keese Southwest)": 0x62,
    "Level 9 Rupee Drop (Keese Central Island)": 0x34,
    "Level 9 Rupee Drop (Wizzrobes Central)": 0x44,
    "Level 9 Rupee Drop (Wizzrobes North Island)": 0x15,
    "Level 9 Rupee Drop (Gels East)": 0x26
}

floor_location_game_ids_late = {}
for key, value in floor_location_game_offsets_late.items():
    floor_location_game_ids_late[key] = value + Rom.first_quest_dungeon_items_late

dungeon_items = {**floor_location_game_ids_early, **floor_location_game_ids_late}

shop_location_ids = {
    "Arrow Shop Item Left": 0x18637,
    "Arrow Shop Item Middle": 0x18638,
    "Arrow Shop Item Right": 0x18639,
    "Candle Shop Item Left": 0x1863A,
    "Candle Shop Item Middle": 0x1863B,
    "Candle Shop Item Right": 0x1863C,
    "Shield Shop Item Left": 0x1863D,
    "Shield Shop Item Middle": 0x1863E,
    "Shield Shop Item Right": 0x1863F,
    "Blue Ring Shop Item Left": 0x18640,
    "Blue Ring Shop Item Middle": 0x18641,
    "Blue Ring Shop Item Right": 0x18642,
    "Potion Shop Item Left": 0x1862E,
    "Potion Shop Item Middle": 0x1862F,
    "Potion Shop Item Right": 0x18630
}

shop_price_location_ids = {
    "Arrow Shop Item Left": 0x18673,
    "Arrow Shop Item Middle": 0x18674,
    "Arrow Shop Item Right": 0x18675,
    "Candle Shop Item Left": 0x18676,
    "Candle Shop Item Middle": 0x18677,
    "Candle Shop Item Right": 0x18678,
    "Shield Shop Item Left": 0x18679,
    "Shield Shop Item Middle": 0x1867A,
    "Shield Shop Item Right": 0x1867B,
    "Blue Ring Shop Item Left": 0x1867C,
    "Blue Ring Shop Item Middle": 0x1867D,
    "Blue Ring Shop Item Right": 0x1867E,
    "Potion Shop Item Left": 0x1866A,
    "Potion Shop Item Middle": 0x1866B,
    "Potion Shop Item Right": 0x1866C
}

secret_money_ids = {
    "Secret Money 1": 0x18680,
    "Secret Money 2": 0x18683,
    "Secret Money 3": 0x18686
}

major_location_ids = {
    "Starting Sword Cave": 0x18611,
    "White Sword Pond": 0x18617,
    "Magical Sword Grave": 0x1861A,
    "Letter Cave": 0x18629,
    "Take Any Item Left": 0x18613,
    "Take Any Item Middle": 0x18614,
    "Take Any Item Right": 0x18615,
    "Armos Knights": 0x10D05,
    "Ocean Heart Container": 0x1789A
}

major_location_offsets = {
    "Starting Sword Cave": 0x77,
    "White Sword Pond": 0x0A,
    "Magical Sword Grave": 0x21,
    "Letter Cave": 0x0E,
    # "Take Any Item Left": 0x7B,
    # "Take Any Item Middle": 0x2C,
    # "Take Any Item Right": 0x47,
    "Armos Knights": 0x24,
    "Ocean Heart Container": 0x5F
}

overworld_locations = [
    "Starting Sword Cave",
    "White Sword Pond",
    "Magical Sword Grave",
    "Letter Cave",
    "Armos Knights",
    "Ocean Heart Container"
]

underworld1_locations = [*floor_location_game_offsets_early.keys()]

underworld2_locations = [*floor_location_game_offsets_late.keys()]

#cave_locations = ["Take Any Item Left", "Take Any Item Middle", "Take Any Item Right"] + [*shop_locations]

location_table_base = [x for x in major_locations] + \
                      [y for y in all_level_locations] + \
                      [z for z in shop_locations]
location_table = {}
for i, location in enumerate(location_table_base):
    location_table[location] = i

location_ids = {**dungeon_items, **shop_location_ids, **major_location_ids}
