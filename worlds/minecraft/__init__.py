import logging
from .Locations import MinecraftAdvancement, advancement_table
from .Items import MinecraftItem, item_table, item_frequencies
from .Rules import set_rules

from BaseClasses import Region, Entrance, Location, MultiWorld, Item

logger = logging.getLogger("Minecraft") 

# Creates regions. Only has the menu and the associated world, which contains all the locations. 
def minecraft_create_regions(world: MultiWorld, player: int):
    menu = Region("Menu", None, "Menu", player)
    start = Entrance(player, "New World", menu)
    menu.exits.append(start)
    minecraft = Region("Minecraft", None, "Minecraft", player)
    menu.world = minecraft.world = world
    for adv_name, adv_data in advancement_table.items():
        adv = MinecraftAdvancement(player, adv_name, adv_data.address, minecraft, adv_data.hard_advancement)
        minecraft.locations.append(adv)
    start.connect(minecraft)
    world.regions += [menu, minecraft]

# Generates the item pool given the table and frequencies in Items.py. 
def minecraft_gen_item_pool(world: MultiWorld, player: int):
    pool = []
    for item_name, item_data in item_table.items():
        for count in range(item_frequencies.get(item_name, 1)):
            pool.append(MinecraftItem(item_name, item_data.progression, item_data.code, player))
    world.itempool += pool

# Sets hard advancements and postgame advancements to junk items (XP rewards)
def set_junk_locations(world: MultiWorld, player: int):
    pass

# Generate Minecraft world. 
def gen_minecraft(world: MultiWorld, player: int):
    minecraft_gen_item_pool(world, player)
    # set_junk_locations(world, player)
    set_rules(world, player)

