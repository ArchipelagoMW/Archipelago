from worlds.minecraft_fabric.item.item_manager import needed, useful, filler, trap, needed_bl, blank_filler

vanilla_items = [
    # PROGRESSION ######################################################################################################
    needed("Ruby"),
    # Togglable
    needed("Swim"),
    needed("Sprint"),
    needed("Jump"),
    needed("Chests & Barrels"),
    # Progressive
    needed("Progressive Tools"),
    needed("Progressive Weapons"),
    needed("Progressive Smelting"),
    needed("Progressive Armor"),
    needed("Progressive Archery"),
    needed("Progressive Dye Recipes"),
    # Ability
    needed_bl("Sleeping"),
    needed_bl("Wither Summoning"),
    needed_bl("Villager Trading"),
    needed_bl("Piglin Bartering"),
    # Station
    needed_bl("Brewing"),
    needed_bl("Enchanting"),
    needed_bl("Smithing"),
    needed_bl("Other Crafting Stations"),
    # Recipe
    needed_bl("Bucket Recipes"),
    needed_bl("Flint and Steel Recipes"),
    needed_bl("Minecart Recipes"),
    needed_bl("Brush Recipes"),
    needed_bl("Spyglass Recipes"),
    needed_bl("Shear Recipes"),
    needed_bl("Eye of Ender Recipes"),
    needed_bl("Fishing Rod Recipes"),
    needed_bl("Glass Bottle Recipes"),
    needed_bl("Resource Compacting Recipes"),
    needed_bl("Shield Recipes"),
    needed_bl("Bundle Recipes"),
    # USEFUL ###########################################################################################################
    # Materials
    useful("4 Emeralds"),
    useful("8 Emeralds"),
    useful("Netherite Scrap"),
    useful("Redstone Dust"),
    useful("Lapis Lazuli"),
    useful("Ender Pearls"),
    useful("Prismarine Shards"),
    useful("Prismarine Crystals"),
    # Enchants
    useful("Looting III"),
    useful("Sharpness III"),
    useful("Silk Touch"),
    useful("Channeling"),
    useful("Piercing IV"),
    useful("Unbreaking I"),
    useful("Unbreaking II"),
    useful("Unbreaking III"),
    # Potions
    useful("Potion of Fire Resistance"),
    useful("Potion of Swiftness"),
    useful("Potion of Luck"),
    useful("Potion of Healing"),
    useful("Strong Potion of Healing"),
    # Ore Vein
    useful("Iron Ore Vein"),
    useful("Gold Ore Vein"),
    useful("Diamond Ore Vein"),
    useful("Emerald Ore Vein"),
    # Large Ore Vein
    useful("Large Iron Ore Vein"),
    useful("Large Gold Ore Vein"),
    useful("Large Diamond Ore Vein"),
    useful("Large Emerald Ore Vein"),
    # Misc
    useful("Saddle"),
    # FILLER ###########################################################################################################
    # Experience
    filler("5 Experience"),
    filler("10 Experience"),
    filler("1 Experience Level"),
    filler("2 Experience Levels"),
    filler("5 Experience Levels"),
    # Arrows
    filler("1 Arrow"),
    filler("8 Arrows"),
    filler("16 Arrows"),
    filler("32 Arrows"),
    # Blocks
    filler("Wooden Planks"),
    filler("Stone"),
    filler("Andesite"),
    filler("Diorite"),
    filler("Granite"),
    # Ores
    filler("Coal Ore Vein"),
    filler("Large Coal Ore Vein"),
    # Foods
    filler("Apples"),
    filler("Golden Carrots"),
    filler("Baked Potatos"),
    filler("Cookies"),
    filler("Steak"),
    filler("Porkchops"),
    filler("Chicken"),
    filler("Mutton"),
    # Bad Foods
    filler("Rotten Flesh"),
    filler("Tropical Fish"),
    filler("Pufferfish"),
    filler("Poisonous Potato"),
    filler("Suspicious Stew"),
    filler("Strong Potion of Harming"),
    # Misc
    filler("Random Dye"),
    # BLANK FILLER #####################################################################################################
    blank_filler("Air"),
    blank_filler("Cave Air"),
    blank_filler("Void Air"),
    blank_filler("Stack of 0 Items"),
    blank_filler("Missing Item"),
    blank_filler("Imaginary Cookie"),
    blank_filler("Nothing"),
    # TRAPS ############################################################################################################
    trap("Reverse Controls Trap"),
    trap("Inverted Mouse Trap"),
    trap("Ice Trap"),
    trap("Random Status Trap"),
    trap("Stun Trap"),
    trap("TNT Trap"),
    trap("Teleport Trap"),
    trap("Bee Trap"),
    trap("Literature Trap")
]