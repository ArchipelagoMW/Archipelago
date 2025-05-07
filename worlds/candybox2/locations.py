from enum import StrEnum

from BaseClasses import Location


# a location is a check

class CandyBox2Location(Location):
    game: str = "Candy Box 2"

class CandyBox2LocationName(StrEnum):
    HP_BAR_UNLOCK = "Candy Box: HP Bar Unlock"
    DISAPPOINTED_EMOTE_CHOCOLATE_BAR = "Candy Box: Throw 1630 candies"
    VILLAGE_SHOP_TOP_LOLLIPOP = "Shop: Top Lollipop"
    VILLAGE_SHOP_CENTRE_LOLLIPOP = "Shop: Centre Lollipop"
    VILLAGE_SHOP_BOTTOM_LOLLIPOP = "Shop: Bottom Lollipop"
    VILLAGE_SHOP_CHOCOLATE_BAR = "Shop: Chocolate Bar"
    VILLAGE_SHOP_TIME_RING = "Shop: Time Ring"
    VILLAGE_SHOP_CANDY_MERCHANTS_HAT = "Shop: Candy Merchant's Hat"
    VILLAGE_SHOP_LEATHER_GLOVES = "Shop: Leather Gloves"
    VILLAGE_SHOP_LEATHER_BOOTS = "Shop: Leather Boots"
    VILLAGE_HOUSE_LOLLIPOP_ON_THE_BOOKSHELF = "Fifth House: Lollipop on bookshelf"
    VILLAGE_HOUSE_LOLLIPOP_IN_THE_BOOKSHELF = "Fifth House: Lollipop in bookshelf"
    VILLAGE_HOUSE_LOLLIPOP_UNDER_THE_RUG = "Fifth House: Lollipop under rug"
    CELLAR_QUEST_CLEARED = "Cellar Quest: Quest Cleared"
    DESERT_QUEST_CLEARED = "Desert Quest: Quest Cleared"
    DESERT_BIRD_FEATHER_ACQUIRED = "Desert Quest: Get Desert Bird Feather"
    TROLL_DEFEATED = "Bridge Quest: Troll Defeated"
    THE_TROLLS_BLUDGEON_ACQUIRED = "Bridge Quest: Get Troll's Bludgeon"
    CAVE_EXIT = "Cave: Exit"
    CAVE_CHOCOLATE_BAR = "Cave: Chocolate Bar"
    CAVE_HEART_PLUG = "Cave: Heart Plug"
    FOREST_QUEST_CLEARED = "Forest Quest: Quest Cleared"
    CASTLE_ENTRANCE_QUEST_CLEARED = "Castle Entrance Quest: Quest Cleared"
    KNIGHT_BODY_ARMOUR_ACQUIRED = "Castle Entrance Quest: Get Knight Body Armour"
    GIANT_NOUGAT_MONSTER_DEFEATED = "Nougat Monster Quest: Giant Nougat Monster Defeated"
    SORCERESS_HUT_LOLLIPOP_ON_THE_SHELVES = "Sorceress' Hut: Inconspicuous Lollipop"
    SORCERESS_HUT_BEGINNERS_GRIMOIRE = "Sorceress' Hut: Beginner's Grimoire"
    SORCERESS_HUT_ADVANCED_GRIMOIRE = "Sorceress' Hut: Advanced Grimoire"
    SORCERESS_HUT_CAULDRON = "Sorceress' Hut: Cauldron"
    SORCERESS_HUT_HAT = "Sorceress' Hut: Sorceress' Hat"
    OCTOPUS_KING_DEFEATED = "Octopus King Quest: Octopus King Defeated"
    MONKEY_WIZARD_DEFEATED = "Monkey Wizard Quest: Money Wizard Defeated"
    EGG_ROOM_QUEST_CLEARED = "Egg Room Quest: Chest Opened"
    DEVIL_DEFEATED = "Hell Quest: Devil Defeated"
    THE_DEVELOPER_DEFEATED = "Developer Quest: The Developer Defeated"
    SOLVE_CYCLOPS_PUZZLE = "Lighthouse: Solve Cyclops Puzzle"
    VILLAGE_FORGE_LOLLIPOP_ON_EXHAUST_CHUTE = "Forge: Inconspicuous Lollipop"
    VILLAGE_FORGE_BUY_WOODEN_SWORD = "Forge: Wooden Sword"
    VILLAGE_FORGE_BUY_IRON_AXE = "Forge: Iron Axe"
    VILLAGE_FORGE_BUY_POLISHED_SILVER_SWORD = "Forge: Polished Silver Sword"
    VILLAGE_FORGE_BUY_LIGHTWEIGHT_BODY_ARMOUR = "Forge: Lightweight Body Armour"
    VILLAGE_FORGE_BUY_SCYTHE = "Forge: Scythe"
    ENCHANT_RED_ENCHANTED_GLOVES = "Wishing Well: Red Enchanted Gloves"
    ENCHANT_PINK_ENCHANTED_GLOVES = "Wishing Well: Pink Enchanted Gloves"
    ENCHANT_SUMMONING_TRIBAL_SPEAR = "Wishing Well: Summoning Tribal Spear"
    ENCHANT_ENCHANTED_MONKEY_WIZARD_STAFF = "Wishing Well: Enchanted Monkey Wizard Staff"
    ENCHANT_ENCHANTED_KNIGHT_BODY_ARMOUR = "Wishing Well: Enchanted Knight Body Armour"
    ENCHANT_OCTOPUS_KING_CROWN_WITH_JASPERS = "Wishing Well: Octopus King Crown with Jaspers"
    ENCHANT_OCTOPUS_KING_CROWN_WITH_OBSIDIAN = "Wishing Well: Octopus King Crown with Obsidian"
    ENCHANT_GIANT_SPOON_OF_DOOM = "Wishing Well: Giant Spoon of Doom"
    THE_HOLE_TRIBAL_WARRIOR_DEFEATED = "Hole: Tribal Warrior Defeated"
    THE_HOLE_DESERT_FORTRESS_KEY_ACQUIRED = "Hole: Right Chest Opened"
    THE_HOLE_HEART_PENDANT_ACQUIRED = "Hole: Top Chest Opened"
    THE_HOLE_BLACK_MAGIC_GRIMOIRE_ACQUIRED = "Hole: Left Chest Opened"
    THE_HOLE_FOUR_CHOCOLATE_BARS_ACQUIRED = "Hole: Bottom Chest Opened"
    TEAPOT_DEFEATED = "Teapot Quest: Teapot Defeated"
    XINOPHERYDON_DEFEATED = "Xinopherydon Quest: Xinopherydon Defeated"
    XINOPHERYDON_QUEST_UNICORN_HORN_ACQUIRED = "Xinopherydon Quest: Unicorn Horn Acquired"
    ROCKET_BOOTS_ACQUIRED = "Ledge Quest: Chest Opened"
    PITCHFORK_ACQUIRED = "Castle Dark Room: Get Pitchfork"
    THE_SQUIRRELS_FIRST_QUESTION = "A Tree: The Squirrel's first question"
    THE_SQUIRRELS_SECOND_QUESTION = "A Tree: The Squirrel's second question"
    THE_SQUIRRELS_THIRD_QUESTION = "A Tree: The Squirrel's third question"
    THE_SQUIRRELS_FOURTH_QUESTION = "A Tree: The Squirrel's fourth question"
    THE_SQUIRRELS_FIFTH_QUESTION = "A Tree: The Squirrel's fifth question"
    THE_SQUIRRELS_PUZZLE = "A Tree: The Squirrel's puzzle"
    THE_SPONGE_ACQUIRED = "The Sea: Get Sponge"
    THE_SHELL_POWDER_ACQUIRED = "The Sea: Get Shell Powder"
    THE_RED_FIN_ACQUIRED = "The Sea: Get Red Fin"
    THE_GREEN_FIN_ACQUIRED = "The Sea: Get Green Fin"
    THE_PURPLE_FIN_ACQUIRED = "The Sea: Get Purple Fin"
    X_MARKS_THE_SPOT = "Secret Treasure Spot: X marks the spot!"
    LOCKED_CANDY_BOX_ACQUIRED = "Lonely House: Locked Candy Box Acquired"
    YOURSELF_DEFEATED = "X Potion Quest: Yourself Defeated"
    BAKE_PAIN_AU_CHOCOLAT_1 = "Castle Bakehouse: Bake Pain au Chocolat 1"
    BAKE_PAIN_AU_CHOCOLAT_2 = "Castle Bakehouse: Bake Pain au Chocolat 2"
    BAKE_PAIN_AU_CHOCOLAT_3 = "Castle Bakehouse: Bake Pain au Chocolat 3"
    BAKE_PAIN_AU_CHOCOLAT_4 = "Castle Bakehouse: Bake Pain au Chocolat 4"
    BAKE_PAIN_AU_CHOCOLAT_5 = "Castle Bakehouse: Bake Pain au Chocolat 5"
    POGO_STICK = "The Mountains: Pogo Stick"

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

hole_entrance_locations = {

}

locations: dict[CandyBox2LocationName, int] = {
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
