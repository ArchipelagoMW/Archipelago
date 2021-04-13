import logging
from .Locations import MinecraftAdvancement, advancement_table, exclusion_table
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
    for adv_name, adv_id in advancement_table.items():
        adv = MinecraftAdvancement(player, adv_name, adv_id, minecraft)
        minecraft.locations.append(adv)
    start.connect(minecraft)
    world.regions += [menu, minecraft]

# Generates the item pool given the table and frequencies in Items.py. 
def minecraft_gen_item_pool(world: MultiWorld, player: int):

    pool = []
    for item_name, item_data in item_table.items():
        for count in range(item_frequencies.get(item_name, 1)):
            pool.append(MinecraftItem(item_name, item_data.progression, item_data.code, player))

    to_exclude = {}
    exclusion_pools = ['hard', 'insane', 'postgame']
    for key in exclusion_pools: 
        if getattr(world, f"exclude_{key}_advancements")[player]: 
            to_exclude.update(exclusion_table[key])

    for loc_name, item_name in to_exclude.items():
        item_data = item_table[item_name]
        location = world.get_location(loc_name, player)
        item = MinecraftItem(item_name, item_data.progression, item_data.code, player)
        world.push_item(location, item)
        pool.remove(item)
        location.event = item_data.progression
        location.locked = True

    world.itempool += pool

# Generate Minecraft world. 
def gen_minecraft(world: MultiWorld, player: int):
    minecraft_gen_item_pool(world, player)
    set_rules(world, player)

