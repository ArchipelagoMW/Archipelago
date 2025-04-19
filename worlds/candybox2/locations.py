from BaseClasses import Location


# a location is a check

class CandyBox2Location(Location):
    game: str = "Candy Box 2"


location_descriptions = {
    "HP Bar Unlock": ""
}

candy_box_locations = {
    "HP Bar Unlock": 1,
    "Disappointed Emote Chocolate Bar": 2
}

village_locations = {}

village_shop_locations = {
    "Village Shop Top Lollipop": 100,
    "Village Shop Centre Lollipop": 101,
    "Village Shop Bottom Lollipop": 102,
    "Village Shop Chocolate Bar": 103,
    "Village Shop Time Ring": 104,
    "Village Shop Candy Merchant's Hat": 105,
    "Village Shop Leather Gloves": 106,
    "Village Shop Leather Boots": 107
}

village_house_1_locations = {
    "Village House Lollipop on the bookshelf": 200,
    "Village House Lollipop in the bookshelf": 201,
    "Village House Lollipop under the rug": 202
}

village_cellar_locations = {
    "Cellar Quest Cleared": 300
}

# Cleared rat quest
map_stage_1_locations = {}

# Cleared desert quest
map_stage_2_locations = {}

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
    "Desert Quest Cleared": 1100,
    "Desert Bird Feather Acquired": 1101,
}

bridge_locations = {
    "Troll Defeated": 1200,
    "The Troll's Bludgeon Acquired": 1201
}

cave_locations = {
    "Cave Exit": 1300,
    "Cave Chocolate Bar": 1301,
    "Heart Plug": 1302,
}

forest_locations = {
    "Forest Quest Cleared": 1400
}

castle_entrance_locations = {
    "Castle Entrance Quest Cleared": 1500,
    "Knight Body Armour Acquired": 1501,
}

giant_nougat_monster_locations = {
    "The Giant Nougat Monster Defeated": 1600
}

village_house_2_locations = {}

sorceress_hut_locations = {
    "Sorceress' Hut Lollipop on the shelves": 1800,
    "Sorceress' Hut Beginner's Grimoire": 1801,
    "Sorceress' Hut Advanced Grimoire": 1802,
    "Sorceress' Hut Cauldron": 1803,
    "Sorceress' Hut Hat": 1804,
}

octopus_king_locations = {
    "Octopus King Defeated": 1900
}

naked_monkey_wizard_locations = {
    "Monkey Wizard Defeated": 2000,
}

castle_egg_room_locations = {
    "Egg Room Quest cleared": 2100
}

dragon_locations = {}

hell_locations = {
    "Devil Defeated": 2300
}

the_developer_fight_locations = {
    "The Developer Defeated": 2400
}

lighthouse_locations = {
    "Solve Cyclops Puzzle": 2500
}

forge_1_locations = {
    "Village Forge Lollipop on Exhaust Chute": 2600,
    "Village Forge Buy Wooden Sword": 2601
}

forge_2_locations = {
    "Village Forge Buy Iron Axe": 2700
}

forge_3_locations = {
    "Village Forge Buy Polished Silver Sword": 2800,
}

forge_4_locations = {
    "Village Forge Buy Lightweight Body Armour": 2900
}

forge_5_locations = {
    "Village Forge Buy Scythe": 3000
}

wishing_well_locations = {
    "Enchant Red Enchanted Gloves": 3100,
    "Enchant Pink Enchanted Gloves": 3101,
    "Enchant Summoning Tribal Spear": 3200,
    "Enchant Enchanted Monkey Wizard Staff": 3300,
    "Enchant Enchanted Knight Body Armour": 3400,
    "Enchant Octopus King Crown with Jaspers": 3500,
    "Enchant Octopus King Crown with Obsidian": 3501,
    "Enchant Giant Spoon of Doom": 3600
}

hole_locations = {
    "The Hole Tribal Warrior Defeated": 3700,
    "The Hole Desert Fortress Key Acquired": 3701,
    "The Hole Heart Pendant Acquired": 3702,
    "The Hole Black Magic Grimoire Acquired": 3703,
    "The Hole Four Chocolate Bars in The Hole Acquired": 3704
}

desert_fortress_locations = {}

teapot_quest_locations = {
    "Teapot Defeated": 3900
}

xinopherydon_quest_locations = {
    "Xinopherydon Defeated": 4000,
    "Xinopherydon Quest Unicorn Horn Acquired": 4001
}

ledge_room_quest_locations = {
    "Rocket Boots Acquired": 4100
}

castle_trap_room_locations = {}

castle_dark_room_locations = {
    "Pitchfork Acquired": 4300
}

squirrel_tree_locations = {
    "The Squirrel's first question": 4400,
    "The Squirrel's second question": 4401,
    "The Squirrel's third question": 4402,
    "The Squirrel's fourth question": 4403,
    "The Squirrel's fifth question": 4404,
    "The Squirrel's puzzle": 4405
}

the_sea_locations = {
    "The Sponge Acquired": 4500,
    "The Shell Powder Acquired": 4501,
    "The Red Fin Acquired": 4502,
    "The Green Fin Acquired": 4503,
    "The Purple Fin Acquired": 4504,
}

dig_spot_locations = {
    "X marks the spot!": 4600
}

lonely_house_locations = {
    "Locked Candy Box Acquired": 4700
}

yourself_fight_locations = {
    "Yourself Defeated": 4800
}

castle_bakehouse_locations = {
    "Bake Pain au Chocolat 1": 4900,
    "Bake Pain au Chocolat 2": 4901,
    "Bake Pain au Chocolat 3": 4902,
    "Bake Pain au Chocolat 4": 4903,
    "Bake Pain au Chocolat 5": 4904,
}

pogo_stick_spot_locations = {
    "Pogo Stick": 500,
}

pier_locations = {

}

lollipop_farm_locations = {

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
    **wishing_well_locations,
    **hole_locations,
    **desert_fortress_locations,
    **teapot_quest_locations,
    **xinopherydon_quest_locations,
    **ledge_room_quest_locations,
    **castle_trap_room_locations,
    **castle_dark_room_locations,
    **squirrel_tree_locations,
    **the_sea_locations,
    **dig_spot_locations,
    **lonely_house_locations,
    **yourself_fight_locations,
    **castle_bakehouse_locations,
    **pogo_stick_spot_locations,
    **pier_locations,
    **lollipop_farm_locations
}
