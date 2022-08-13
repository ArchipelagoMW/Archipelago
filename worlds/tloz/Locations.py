from . import Rom

major_locations = [
    "Wooden Sword Cave",
    "White Sword Pond",
    "Magical Sword Grave",
    "Take Any Item 1",
    "Take Any Item 2",
    "Take Any Item 3",
    "Armos Knights",
    "Ocean Heart Container",
    "Letter Cave",
]

level_locations = [
    ["Level 1 Item 1", "Level 1 Item 2", "Level 1 Boss", "Level 1 Triforce",
     "Level 1 Key Drop 1", "Level 1 Key Drop 2", "Level 1 Key Drop 3", "Level 1 Key Drop 4"],

    ["Level 2 Item", "Level 2 Boss", "Level 2 Triforce", "Level 2 Rupee Drop", "Level 2 Bomb Drop",
     "Level 2 Key Drop 1", "Level 2 Key Drop 2", "Level 2 Key Drop 3", "Level 2 Key Drop 4"],

    ["Level 3 Item", "Level 3 Boss", "Level 3 Triforce", "Level 3 Bomb Drop 1", "Level 3 Bomb Drop 2",
     "Level 3 Bomb Drop 3", "Level 3 Key Drop 1", "Level 3 Key Drop 2", "Level 3 Key Drop 3", "Level 3 Key Drop 4",
     "Level 3 Key Drop 5"],

    ["Level 4 Item", "Level 4 Boss", "Level 4 Triforce", "Level 4 Key Drop 1", "Level 4 Key Drop 2"],

    ["Level 5 Item", "Level 5 Boss", "Level 5 Triforce", "Level 5 Bomb Drop 1", "Level 5 Bomb Drop 2",
     "Level 5 Key Drop 1", "Level 5 Key Drop 2", "Level 5 Key Drop 3", "Level 5 Key Drop 4"],

    ["Level 6 Item", "Level 6 Boss", "Level 6 Triforce", "Level 6 Rupee Drop", "Level 6 Key Drop"],

    ["Level 7 Item", "Level 7 Boss", "Level 7 Triforce", "Level 7 Rupee Drop 1", "Level 7 Rupee Drop 2",
     "Level 7 Rupee Drop 3", "Level 7 Bomb Drop 1", "Level 7 Bomb Drop 2", "Level 7 Bomb Drop 3",
     "Level 7 Bomb Drop 4", "Level 7 Bomb Drop 5", "Level 7 Bomb Drop 6", "Level 7 Bomb Drop 7",
     "Level 7 Key Drop 1", "Level 7 Key Drop 2"],

    ["Level 8 Item 1", "Level 8 Item 2", "Level 8 Boss", "Level 8 Triforce", "Level 8 Rupee Drop 1",
     "Level 8 Rupee Drop 2", "Level 8 Rupee Drop 3", "Level 8 Bomb Drop 1", "Level 8 Bomb Drop 2",
     "Level 8 Key Drop 1", "Level 8 Key Drop 2", "Level 8 Key Drop 3"],

    ["Level 9 Item 1", "Level 9 Item 2", "Level 9 Boss", "Level 9 Rupee Drop 1", "Level 9 Rupee Drop 2",
     "Level 9 Rupee Drop 3", "Level 9 Rupee Drop 4", "Level 9 Rupee Drop 5", "Level 9 Rupee Drop 6",
     "Level 9 Bomb Drop 1", "Level 9 Bomb Drop 2", "Level 9 Bomb Drop 3", "Level 9 Bomb Drop 4", "Level 9 Bomb Drop 5",
     "Level 9 Key Drop 1", "Level 9 Key Drop 2", "Level 9 Key Drop 3"],
]

all_level_locations = []
for level in level_locations:
    for location in level:
        all_level_locations.append(location)

shop_locations = [
    "Arrow Shop Item 1", "Arrow Shop Item 2", "Arrow Shop Item 3",
    "Candle Shop Item 1", "Candle Shop Item 2", "Candle Shop Item 3",
    "Shield Shop Item 1", "Shield Shop Item 2", "Shield Shop Item 3",
    "Blue Ring Shop Item 1", "Blue Ring Shop Item 2", "Blue Ring Shop Item 3",
    "Potion Shop Item 1", "Potion Shop Item 2", "Potion Shop Item 3"
]

floor_location_game_offsets_early = {
    "Level 1 Item 1": 0x7F,
    "Level 1 Item 2": 0x44,
    "Level 1 Boss": 0x35,
    "Level 1 Triforce": 0x36,
    "Level 2 Item": 0x4F,
    "Level 2 Boss": 0x0E,
    "Level 2 Triforce": 0x0D,
    "Level 3 Item": 0x0F,
    "Level 3 Boss": 0x4D,
    "Level 3 Triforce": 0x3D,
    "Level 4 Item": 0x70,
    "Level 4 Boss": 0x13,
    "Level 4 Triforce": 0x03,
    "Level 5 Item": 0x04,
    "Level 5 Boss": 0x24,
    "Level 5 Triforce": 0x14,
    "Level 6 Item": 0x75,
    "Level 6 Boss": 0x1C,
    "Level 6 Triforce": 0x0C,
    "Level 6 Rupee Drop": 0x28,
    "Level 2 Rupee Drop": 0x2F,
    "Level 5 Bomb Drop 1": 0x65,
    "Level 5 Bomb Drop 2": 0x56,
    "Level 3 Bomb Drop 1": 0x69,
    "Level 3 Bomb Drop 2": 0x4A,
    "Level 3 Bomb Drop 3": 0x5B,
    "Level 2 Bomb Drop": 0x3F,
    "Level 4 Key Drop 1": 0x70,
    "Level 4 Key Drop 2": 0x51,
    "Level 1 Key Drop 1": 0x72,
    "Level 1 Key Drop 2": 0x23,
    "Level 1 Key Drop 3": 0x33,
    "Level 1 Key Drop 4": 0x74,
    "Level 1 Key Drop 5": 0x53,
    "Level 5 Key Drop 1": 0x16,
    "Level 5 Key Drop 2": 0x26,
    "Level 5 Key Drop 3": 0x47,
    "Level 5 Key Drop 4": 0x77,
    "Level 3 Key Drop 1": 0x58,
    "Level 3 Key Drop 2": 0x49,
    "Level 6 Key Drop": 0x2A,
    "Level 3 Key Drop 3": 0x4B,
    "Level 3 Key Drop 4": 0x6B,
    "Level 3 Key Drop 5": 0x7B,
    "Level 2 Key Drop 1": 0x6C,
    "Level 2 Key Drop 2": 0x3E,
    "Level 2 Key Drop 3": 0x4E,
    "Level 2 Key Drop 4": 0x7E
}
floor_location_game_ids_early = {}
floor_location_game_ids_late = {}
for key, value in floor_location_game_offsets_early.items():
    floor_location_game_ids_early[key] = value + Rom.first_quest_dungeon_items_early

floor_location_game_offsets_late = {
    "Level 7 Item": 0x4A,
    "Level 7 Boss": 0x2A,
    "Level 7 Triforce": 0x2B,
    "Level 8 Item 1": 0x0F,
    "Level 8 Item 2": 0x6F,
    "Level 8 Boss": 0x3C,
    "Level 8 Triforce": 0x2C,
    "Level 9 Item 1": 0x4F,
    "Level 9 Item 2": 0x00,
    "Level 9 Rupee Drop 1": 0x40,
    "Level 9 Rupee Drop 2": 0x12,
    "Level 9 Rupee Drop 3": 0x62,
    "Level 9 Rupee Drop 4": 0x43,
    "Level 9 Rupee Drop 5": 0x44,
    "Level 9 Rupee Drop 6": 0x26,
    "Level 7 Rupee Drop 1": 0x38,
    "Level 7 Rupee Drop 2": 0x58,
    "Level 7 Rupee Drop 3": 0x09,
    "Level 8 Rupee Drop 1": 0x7D,
    "Level 8 Rupee Drop 2": 0x4E,
    "Level 8 Rupee Drop 3": 0x6E,
    "Level 9 Bomb Drop 1": 0x11,
    "Level 9 Bomb Drop 2": 0x23,
    "Level 9 Bomb Drop 3": 0x25,
    "Level 9 Bomb Drop 4": 0x16,
    "Level 9 Bomb Drop 5": 0x37,
    "Level 7 Bomb Drop 1": 0x69,
    "Level 7 Bomb Drop 2": 0x7A,
    "Level 7 Bomb Drop 3": 0x0B,
    "Level 7 Bomb Drop 4": 0x1B,
    "Level 7 Bomb Drop 5": 0x0C,
    "Level 7 Bomb Drop 6": 0x6C,
    "Level 7 Bomb Drop 7": 0x0D,
    "Level 8 Bomb Drop 1": 0x0E,
    "Level 8 Bomb Drop 2": 0x3F,
    "Level 9 Key Drop 1": 0x61,
    "Level 9 Key Drop 2": 0x56,
    "Level 9 Key Drop 3": 0x47,
    "Level 7 Key Drop 1": 0x78,
    "Level 7 Key Drop 2": 0x0A,
    "Level 8 Key Drop 1": 0x5C,
    "Level 8 Key Drop 2": 0x6D,
    "Level 8 Key Drop 3": 0x5E
}

for key, value in floor_location_game_offsets_late.items():
    floor_location_game_ids_late[key] = value + Rom.first_quest_dungeon_items_late

dungeon_items = {**floor_location_game_ids_early, **floor_location_game_ids_late}

shop_location_ids = {
    "Arrow Shop Item 1": 0x18637,
    "Arrow Shop Item 2": 0x18638,
    "Arrow Shop Item 3": 0x18639,
    "Candle Shop Item 1": 0x1863A,
    "Candle Shop Item 2": 0x1863B,
    "Candle Shop Item 3": 0x1863C,
    "Shield Shop Item 1": 0x1863D,
    "Shield Shop Item 2": 0x1863E,
    "Shield Shop Item 3": 0x1863F,
    "Blue Ring Shop Item 1": 0x18640,
    "Blue Ring Shop Item 2": 0x18641,
    "Blue Ring Shop Item 3": 0x18642,
    "Potion Shop Item 1": 0x1862E,
    "Potion Shop Item 2": 0x1862F,
    "Potion Shop Item 3": 0x18630
}

shop_price_location_ids = {
    "Arrow Shop Item 1": 0x18673,
    "Arrow Shop Item 2": 0x18674,
    "Arrow Shop Item 3": 0x18675,
    "Candle Shop Item 1": 0x18676,
    "Candle Shop Item 2": 0x18677,
    "Candle Shop Item 3": 0x18678,
    "Shield Shop Item 1": 0x18679,
    "Shield Shop Item 2": 0x1867A,
    "Shield Shop Item 3": 0x1867B,
    "Blue Ring Shop Item 1": 0x1867C,
    "Blue Ring Shop Item 2": 0x1867D,
    "Blue Ring Shop Item 3": 0x1867E,
    "Potion Shop Item 1": 0x1866A,
    "Potion Shop Item 2": 0x1866B,
    "Potion Shop Item 3": 0x1866C
}

secret_money_ids = {
    "Secret Money 1": 0x18680,
    "Secret Money 2": 0x18683,
    "Secret Money 3": 0x18686
}

major_location_ids = {
    "Wooden Sword Cave": 0x18611,
    "White Sword Pond": 0x18617,
    "Magical Sword Grave": 0x1861A,
    "Letter Cave": 0x18629,
    "Take Any Item 1": 0x18613,
    "Take Any Item 2": 0x18614,
    "Take Any Item 3": 0x18615,
    "Armos Knights": 0x10D05,
    "Ocean Heart Container": 0x1789A
}

major_location_offsets = {
    "Wooden Sword Cave": 0x77,
    "White Sword Pond": 0x0A,
    "Magical Sword Grave": 0x21,
    "Letter Cave": 0x0E,
    "Take Any Item 1": 0x7B,
    "Take Any Item 2": 0x2C,
    "Take Any Item 3": 0x47,
    "Armos Knights": 0x24,
    "Ocean Heart Container": 0x5F
}

overworld_locations = [
    "Wooden Sword Cave",
    "White Sword Pond",
    "Magical Sword Grave",
    "Letter Cave",
    "Armos Knights",
    "Ocean Heart Container"
]

underworld1_locations = [*floor_location_game_offsets_early.keys()]

underworld2_locations = [*floor_location_game_offsets_late.keys()]

cave_locations = ["Take Any Item 1", "Take Any Item 2", "Take Any Item 3"] + [*shop_locations]

location_table_base = [x for x in major_locations] + \
                      [y for y in all_level_locations] + \
                      [z for z in shop_locations]
location_table = {}
for i, location in enumerate(location_table_base):
    location_table[location] = i

location_ids = {**dungeon_items, **shop_location_ids, **major_location_ids}