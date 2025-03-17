from BaseClasses import Location


# a location is a check

class CandyBox2Location(Location):
    game: str = "Candy Box 2"


location_descriptions = {
    "HP Bar Unlock": ""
}

candy_box_locations = {
    "HP Bar Unlock": 1
}

village_locations = {}

village_shop_locations = {
    "Top Lollipop": 100,
    "Centre Lollipop": 101,
    "Bottom Lollipop": 102,
    "Chocolate Bar": 103,
    "Time Ring": 104,
    "Candy Merchant's Hat": 105,
    "Leather Gloves": 106,
    "Leather Boots": 107
}

village_house_1_locations = {
    "Lollipop on the bookshelf": 200,
    "Lollipop in the bookshelf": 201,
    "Lollipop under the rug": 202
}

village_cellar_locations = {
    "Cellar Quest": 300
}

# Cleared rat quest
map_stage_1_locations = {}

# Cleared desert quest
map_stage_2_locations = {
    "Pogo Stick": 500,
}

# Cleared bridge quest
map_stage_3_locations = {}

# Cleared cave entrance
map_stage_4_locations = {}

# Cleared forest
map_stage_5_locations = {}

# Cleared castle entrance
map_stage_6_locations = {}

# Cleared Giant Nougat Monster
map_stage_7_locations = {}

desert_locations = {
    "Desert Quest": 1100,
    "Desert Bird Feather": 1101,
}

bridge_locations = {
    "Bridge Quest": 1200,
    "The Troll's Bludgeon Acquired": 1201
}

cave_locations = {
    "Cave Exit": 1300,
    "Cave Chocolate Bar": 1301,
    "Heart Plug": 1302,
}

forest_locations = {
    "Forest Quest": 1400
}

castle_entrance_locations = {
    "Castle Entrance Quest": 1500
}

giant_nougat_monster_locations = {
    "The Giant Nougat Monster Quest": 1600
}

village_house_2_locations = {}

sorceress_hut_locations = {
    "Lollipop on the shelves": 1800,
    "Beginner's Grimoire": 1801,
    "Advanced Grimoire": 1802,
    "Sorceress' Cauldron": 1803,
    "Sorceress' Hat": 1804,
}

octopus_king_locations = {
    "Octopus King Quest": 1900
}

naked_monkey_wizard_locations = {
    "Monkey Wizard Quest": 2000,
}

castle_egg_room_locations = {
    "Egg Room Chest": 2100
}

dragon_locations = {}

hell_locations = {
    "Kill the Devil": 2300
}

the_developer_fight_locations = {
    "Kill the Developer": 2400
}

lighthouse_locations = {
    "Solve Cyclops Puzzle": 2500
}

forge_1_locations = {
    "Lollipop on Exhaust Chute": 2600,
    "Buy Wooden Sword": 2601
}

forge_2_locations = {
    "Buy Iron Axe": 2700
}

forge_3_locations = {
    "Buy Polished Silver Sword": 2800,
}

forge_4_locations = {
    "Buy Lightweight Body Armour": 2900
}

forge_5_locations = {
    "Buy Scythe": 3000
}

locations = {
    **candy_box_locations,
    **village_locations,
    **village_shop_locations,
    **village_house_1_locations,
    **village_cellar_locations,
    **map_stage_1_locations,
    **map_stage_2_locations,
    **map_stage_3_locations,
    **map_stage_4_locations,
    **map_stage_5_locations,
    **map_stage_6_locations,
    **map_stage_7_locations,
    **desert_locations,
    **bridge_locations,
    **cave_locations,
    **forest_locations,
    **castle_entrance_locations,
    **giant_nougat_monster_locations,
    **village_house_2_locations,
    **sorceress_hut_locations,
    **octopus_king_locations,
    **naked_monkey_wizard_locations,
    **castle_egg_room_locations,
    **dragon_locations,
    **hell_locations,
    **the_developer_fight_locations,
    **lighthouse_locations,
    **forge_1_locations,
    **forge_2_locations,
    **forge_3_locations,
    **forge_4_locations,
    **forge_5_locations,
}
