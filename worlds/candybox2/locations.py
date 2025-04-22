from enum import StrEnum

from BaseClasses import Location


# a location is a check

class CandyBox2Location(Location):
    game: str = "Candy Box 2"

class CandyBox2LocationName(StrEnum):
    HP_BAR_UNLOCK = "HP Bar Unlock"
    DISAPPOINTED_EMOTE_CHOCOLATE_BAR = "Disappointed Emote Chocolate Bar"
    VILLAGE_SHOP_TOP_LOLLIPOP = "Village Shop Top Lollipop"
    VILLAGE_SHOP_CENTRE_LOLLIPOP = "Village Shop Centre Lollipop"
    VILLAGE_SHOP_BOTTOM_LOLLIPOP = "Village Shop Bottom Lollipop"
    VILLAGE_SHOP_CHOCOLATE_BAR = "Village Shop Chocolate Bar"
    VILLAGE_SHOP_TIME_RING = "Village Shop Time Ring"
    VILLAGE_SHOP_CANDY_MERCHANTS_HAT = "Village Shop Candy Merchant's Hat"
    VILLAGE_SHOP_LEATHER_GLOVES = "Village Shop Leather Gloves"
    VILLAGE_SHOP_LEATHER_BOOTS = "Village Shop Leather Boots"
    VILLAGE_HOUSE_LOLLIPOP_ON_THE_BOOKSHELF = "Village House Lollipop on the bookshelf"
    VILLAGE_HOUSE_LOLLIPOP_IN_THE_BOOKSHELF = "Village House Lollipop in the bookshelf"
    VILLAGE_HOUSE_LOLLIPOP_UNDER_THE_RUG = "Village House Lollipop under the rug"
    CELLAR_QUEST_CLEARED = "Cellar Quest Cleared"
    DESERT_QUEST_CLEARED = "Desert Quest Cleared"
    DESERT_BIRD_FEATHER_ACQUIRED = "Desert Bird Feather Acquired"
    TROLL_DEFEATED = "Troll Defeated"
    THE_TROLLS_BLUDGEON_ACQUIRED = "The Troll's Bludgeon Acquired"
    CAVE_EXIT = "Cave Exit"
    CAVE_CHOCOLATE_BAR = "Cave Chocolate Bar"
    CAVE_HEART_PLUG = "Heart Plug"
    FOREST_QUEST_CLEARED = "Forest Quest Cleared"
    CASTLE_ENTRANCE_QUEST_CLEARED = "Castle Entrance Quest Cleared"
    KNIGHT_BODY_ARMOUR_ACQUIRED = "Knight Body Armour Acquired"
    GIANT_NOUGAT_MONSTER_DEFEATED = "The Giant Nougat Monster Defeated"
    SORCERESS_HUT_LOLLIPOP_ON_THE_SHELVES = "Sorceress' Hut Lollipop on the shelves"
    SORCERESS_HUT_BEGINNERS_GRIMOIRE = "Sorceress' Hut Beginner's Grimoire"
    SORCERESS_HUT_ADVANCED_GRIMOIRE = "Sorceress' Hut Advanced Grimoire"
    SORCERESS_HUT_CAULDRON = "Sorceress' Hut Cauldron"
    SORCERESS_HUT_HAT = "Sorceress' Hut Hat"
    OCTOPUS_KING_DEFEATED = "Octopus King Defeated"
    MONKEY_WIZARD_DEFEATED = "Monkey Wizard Defeated"
    EGG_ROOM_QUEST_CLEARED = "Egg Room Quest cleared"
    DEVIL_DEFEATED = "Devil Defeated"
    THE_DEVELOPER_DEFEATED = "The Developer Defeated"
    SOLVE_CYCLOPS_PUZZLE = "Solve Cyclops Puzzle"
    VILLAGE_FORGE_LOLLIPOP_ON_EXHAUST_CHUTE = "Village Forge Lollipop on Exhaust Chute"
    VILLAGE_FORGE_BUY_WOODEN_SWORD = "Village Forge Buy Wooden Sword"
    VILLAGE_FORGE_BUY_IRON_AXE = "Village Forge Buy Iron Axe"
    VILLAGE_FORGE_BUY_POLISHED_SILVER_SWORD = "Village Forge Buy Polished Silver Sword"
    VILLAGE_FORGE_BUY_LIGHTWEIGHT_BODY_ARMOUR = "Village Forge Buy Lightweight Body Armour"
    VILLAGE_FORGE_BUY_SCYTHE = "Village Forge Buy Scythe"
    ENCHANT_RED_ENCHANTED_GLOVES = "Enchant Red Enchanted Gloves"
    ENCHANT_PINK_ENCHANTED_GLOVES = "Enchant Pink Enchanted Gloves"
    ENCHANT_SUMMONING_TRIBAL_SPEAR = "Enchant Summoning Tribal Spear"
    ENCHANT_ENCHANTED_MONKEY_WIZARD_STAFF = "Enchant Enchanted Monkey Wizard Staff"
    ENCHANT_ENCHANTED_KNIGHT_BODY_ARMOUR = "Enchant Enchanted Knight Body Armour"
    ENCHANT_OCTOPUS_KING_CROWN_WITH_JASPERS = "Enchant Octopus King Crown with Jaspers"
    ENCHANT_OCTOPUS_KING_CROWN_WITH_OBSIDIAN = "Enchant Octopus King Crown with Obsidian"
    ENCHANT_GIANT_SPOON_OF_DOOM = "Enchant Giant Spoon of Doom"
    THE_HOLE_TRIBAL_WARRIOR_DEFEATED = "The Hole Tribal Warrior Defeated"
    THE_HOLE_DESERT_FORTRESS_KEY_ACQUIRED = "The Hole Desert Fortress Key Acquired"
    THE_HOLE_HEART_PENDANT_ACQUIRED = "The Hole Heart Pendant Acquired"
    THE_HOLE_BLACK_MAGIC_GRIMOIRE_ACQUIRED = "The Hole Black Magic Grimoire Acquired"
    THE_HOLE_FOUR_CHOCOLATE_BARS_ACQUIRED = "The Hole Four Chocolate Bars in The Hole Acquired"
    TEAPOT_DEFEATED = "Teapot Defeated"
    XINOPHERYDON_DEFEATED = "Xinopherydon Defeated"
    XINOPHERYDON_QUEST_UNICORN_HORN_ACQUIRED = "Xinopherydon Quest Unicorn Horn Acquired"
    ROCKET_BOOTS_ACQUIRED = "Rocket Boots Acquired"
    PITCHFORK_ACQUIRED = "Pitchfork Acquired"
    THE_SQUIRRELS_FIRST_QUESTION = "The Squirrel's first question"
    THE_SQUIRRELS_SECOND_QUESTION = "The Squirrel's second question"
    THE_SQUIRRELS_THIRD_QUESTION = "The Squirrel's third question"
    THE_SQUIRRELS_FOURTH_QUESTION = "The Squirrel's fourth question"
    THE_SQUIRRELS_FIFTH_QUESTION = "The Squirrel's fifth question"
    THE_SQUIRRELS_PUZZLE = "The Squirrel's puzzle"
    THE_SPONGE_ACQUIRED = "The Sponge Acquired"
    THE_SHELL_POWDER_ACQUIRED = "The Shell Powder Acquired"
    THE_RED_FIN_ACQUIRED = "The Red Fin Acquired"
    THE_GREEN_FIN_ACQUIRED = "The Green Fin Acquired"
    THE_PURPLE_FIN_ACQUIRED = "The Purple Fin Acquired"
    X_MARKS_THE_SPOT = "X marks the spot!"
    LOCKED_CANDY_BOX_ACQUIRED = "Locked Candy Box Acquired"
    YOURSELF_DEFEATED = "Yourself Defeated"
    BAKE_PAIN_AU_CHOCOLAT_1 = "Bake Pain au Chocolat 1"
    BAKE_PAIN_AU_CHOCOLAT_2 = "Bake Pain au Chocolat 2"
    BAKE_PAIN_AU_CHOCOLAT_3 = "Bake Pain au Chocolat 3"
    BAKE_PAIN_AU_CHOCOLAT_4 = "Bake Pain au Chocolat 4"
    BAKE_PAIN_AU_CHOCOLAT_5 = "Bake Pain au Chocolat 5"
    POGO_STICK = "Pogo Stick"

location_descriptions = {
    CandyBox2LocationName.HP_BAR_UNLOCK: ""
}

candy_box_locations = {
    CandyBox2LocationName.HP_BAR_UNLOCK: 1,
    CandyBox2LocationName.DISAPPOINTED_EMOTE_CHOCOLATE_BAR: 2
}

village_locations = {}

village_shop_locations = {
    CandyBox2LocationName.VILLAGE_SHOP_TOP_LOLLIPOP: 100,
    CandyBox2LocationName.VILLAGE_SHOP_CENTRE_LOLLIPOP: 101,
    CandyBox2LocationName.VILLAGE_SHOP_BOTTOM_LOLLIPOP: 102,
    CandyBox2LocationName.VILLAGE_SHOP_CHOCOLATE_BAR: 103,
    CandyBox2LocationName.VILLAGE_SHOP_TIME_RING: 104,
    CandyBox2LocationName.VILLAGE_SHOP_CANDY_MERCHANTS_HAT: 105,
    CandyBox2LocationName.VILLAGE_SHOP_LEATHER_GLOVES: 106,
    CandyBox2LocationName.VILLAGE_SHOP_LEATHER_BOOTS: 107
}

village_house_1_locations = {
    CandyBox2LocationName.VILLAGE_HOUSE_LOLLIPOP_ON_THE_BOOKSHELF: 200,
    CandyBox2LocationName.VILLAGE_HOUSE_LOLLIPOP_IN_THE_BOOKSHELF: 201,
    CandyBox2LocationName.VILLAGE_HOUSE_LOLLIPOP_UNDER_THE_RUG: 202
}

village_cellar_locations = {
    CandyBox2LocationName.CELLAR_QUEST_CLEARED: 300
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
    CandyBox2LocationName.DESERT_QUEST_CLEARED: 1100,
    CandyBox2LocationName.DESERT_BIRD_FEATHER_ACQUIRED: 1101,
}

bridge_locations = {
    CandyBox2LocationName.TROLL_DEFEATED: 1200,
    CandyBox2LocationName.THE_TROLLS_BLUDGEON_ACQUIRED: 1201
}

cave_locations = {
    CandyBox2LocationName.CAVE_EXIT: 1300,
    CandyBox2LocationName.CAVE_CHOCOLATE_BAR: 1301,
    CandyBox2LocationName.CAVE_HEART_PLUG: 1302,
}

forest_locations = {
    CandyBox2LocationName.FOREST_QUEST_CLEARED: 1400
}

castle_entrance_locations = {
    CandyBox2LocationName.CASTLE_ENTRANCE_QUEST_CLEARED: 1500,
    CandyBox2LocationName.KNIGHT_BODY_ARMOUR_ACQUIRED: 1501,
}

giant_nougat_monster_locations = {
    CandyBox2LocationName.GIANT_NOUGAT_MONSTER_DEFEATED: 1600
}

village_house_2_locations = {}

sorceress_hut_locations = {
    CandyBox2LocationName.SORCERESS_HUT_LOLLIPOP_ON_THE_SHELVES: 1800,
    CandyBox2LocationName.SORCERESS_HUT_BEGINNERS_GRIMOIRE: 1801,
    CandyBox2LocationName.SORCERESS_HUT_ADVANCED_GRIMOIRE: 1802,
    CandyBox2LocationName.SORCERESS_HUT_CAULDRON: 1803,
    CandyBox2LocationName.SORCERESS_HUT_HAT: 1804,
}

octopus_king_locations = {
    CandyBox2LocationName.OCTOPUS_KING_DEFEATED: 1900
}

naked_monkey_wizard_locations = {
    CandyBox2LocationName.MONKEY_WIZARD_DEFEATED: 2000,
}

castle_egg_room_locations = {
    CandyBox2LocationName.EGG_ROOM_QUEST_CLEARED: 2100
}

dragon_locations = {}

hell_locations = {
    CandyBox2LocationName.DEVIL_DEFEATED: 2300
}

the_developer_fight_locations = {
    CandyBox2LocationName.THE_DEVELOPER_DEFEATED: 2400
}

lighthouse_locations = {
    CandyBox2LocationName.SOLVE_CYCLOPS_PUZZLE: 2500
}

forge_locations = {
    CandyBox2LocationName.VILLAGE_FORGE_LOLLIPOP_ON_EXHAUST_CHUTE: 2600,
    CandyBox2LocationName.VILLAGE_FORGE_BUY_WOODEN_SWORD: 2601,
    CandyBox2LocationName.VILLAGE_FORGE_BUY_IRON_AXE: 2700,
    CandyBox2LocationName.VILLAGE_FORGE_BUY_POLISHED_SILVER_SWORD: 2800,
    CandyBox2LocationName.VILLAGE_FORGE_BUY_LIGHTWEIGHT_BODY_ARMOUR: 2900,
    CandyBox2LocationName.VILLAGE_FORGE_BUY_SCYTHE: 3000
}

wishing_well_locations = {
    CandyBox2LocationName.ENCHANT_RED_ENCHANTED_GLOVES: 3100,
    CandyBox2LocationName.ENCHANT_PINK_ENCHANTED_GLOVES: 3101,
    CandyBox2LocationName.ENCHANT_SUMMONING_TRIBAL_SPEAR: 3200,
    CandyBox2LocationName.ENCHANT_ENCHANTED_MONKEY_WIZARD_STAFF: 3300,
    CandyBox2LocationName.ENCHANT_ENCHANTED_KNIGHT_BODY_ARMOUR: 3400,
    CandyBox2LocationName.ENCHANT_OCTOPUS_KING_CROWN_WITH_JASPERS: 3500,
    CandyBox2LocationName.ENCHANT_OCTOPUS_KING_CROWN_WITH_OBSIDIAN: 3501,
    CandyBox2LocationName.ENCHANT_GIANT_SPOON_OF_DOOM: 3600
}

hole_locations = {
    CandyBox2LocationName.THE_HOLE_TRIBAL_WARRIOR_DEFEATED: 3700,
    CandyBox2LocationName.THE_HOLE_DESERT_FORTRESS_KEY_ACQUIRED: 3701,
    CandyBox2LocationName.THE_HOLE_HEART_PENDANT_ACQUIRED: 3702,
    CandyBox2LocationName.THE_HOLE_BLACK_MAGIC_GRIMOIRE_ACQUIRED: 3703,
    CandyBox2LocationName.THE_HOLE_FOUR_CHOCOLATE_BARS_ACQUIRED: 3704
}

desert_fortress_locations = {}

teapot_quest_locations = {
    CandyBox2LocationName.TEAPOT_DEFEATED: 3900
}

xinopherydon_quest_locations = {
    CandyBox2LocationName.XINOPHERYDON_DEFEATED: 4000,
    CandyBox2LocationName.XINOPHERYDON_QUEST_UNICORN_HORN_ACQUIRED: 4001
}

ledge_room_quest_locations = {
    CandyBox2LocationName.ROCKET_BOOTS_ACQUIRED: 4100
}

castle_trap_room_locations = {}

castle_dark_room_locations = {
    CandyBox2LocationName.PITCHFORK_ACQUIRED: 4300
}

squirrel_tree_locations = {
    CandyBox2LocationName.THE_SQUIRRELS_FIRST_QUESTION: 4400,
    CandyBox2LocationName.THE_SQUIRRELS_SECOND_QUESTION: 4401,
    CandyBox2LocationName.THE_SQUIRRELS_THIRD_QUESTION: 4402,
    CandyBox2LocationName.THE_SQUIRRELS_FOURTH_QUESTION: 4403,
    CandyBox2LocationName.THE_SQUIRRELS_FIFTH_QUESTION: 4404,
    CandyBox2LocationName.THE_SQUIRRELS_PUZZLE: 4405
}

the_sea_locations = {
    CandyBox2LocationName.THE_SPONGE_ACQUIRED: 4500,
    CandyBox2LocationName.THE_SHELL_POWDER_ACQUIRED: 4501,
    CandyBox2LocationName.THE_RED_FIN_ACQUIRED: 4502,
    CandyBox2LocationName.THE_GREEN_FIN_ACQUIRED: 4503,
    CandyBox2LocationName.THE_PURPLE_FIN_ACQUIRED: 4504,
}

dig_spot_locations = {
    CandyBox2LocationName.X_MARKS_THE_SPOT: 4600
}

lonely_house_locations = {
    CandyBox2LocationName.LOCKED_CANDY_BOX_ACQUIRED: 4700
}

yourself_fight_locations = {
    CandyBox2LocationName.YOURSELF_DEFEATED: 4800
}

castle_bakehouse_locations = {
    CandyBox2LocationName.BAKE_PAIN_AU_CHOCOLAT_1: 4900,
    CandyBox2LocationName.BAKE_PAIN_AU_CHOCOLAT_2: 4901,
    CandyBox2LocationName.BAKE_PAIN_AU_CHOCOLAT_3: 4902,
    CandyBox2LocationName.BAKE_PAIN_AU_CHOCOLAT_4: 4903,
    CandyBox2LocationName.BAKE_PAIN_AU_CHOCOLAT_5: 4904,
}

pogo_stick_spot_locations = {
    CandyBox2LocationName.POGO_STICK: 500,
}

pier_locations = {

}

lollipop_farm_locations = {

}

village_minigame_locations = {

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
    **forge_locations,
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
    **lollipop_farm_locations,
    **village_minigame_locations
}
