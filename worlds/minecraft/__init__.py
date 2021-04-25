import logging
from random import Random
from .Locations import MinecraftAdvancement, advancement_table, exclusion_table, events_table
from .Items import MinecraftItem, item_table, item_frequencies
from .Rules import set_rules

from BaseClasses import Region, Entrance, Location, MultiWorld, Item
from Options import minecraft_options

logger = logging.getLogger("Minecraft")

logic_version = (0, 3)


def minecraft_create_regions(world: MultiWorld, player: int):

    def MCRegion(region_name: str):
        ret = Region(region_name, None, region_name, player)
        ret.world = world
        ret.locations = [ MinecraftAdvancement(player, loc_name, loc_data.id, ret) 
            for loc_name, loc_data in advancement_table.items() 
            if loc_data.region == region_name ]
        return ret

    # Creating regions. 
    menu = MCRegion("Menu")
    overworld = MCRegion("Overworld")
    nether = MCRegion("The Nether")
    end = MCRegion("The End")
    village = MCRegion("Village")
    outpost = MCRegion("Pillager Outpost")
    fortress = MCRegion("Nether Fortress")
    bastion = MCRegion("Bastion Remnant")
    end_city = MCRegion("End City")

    # Creating entrances to link regions. 
    start = Entrance(player, "New World", menu)
    portal_nether = Entrance(player, "Nether Portal", overworld)
    portal_end = Entrance(player, "End Portal", overworld)
    ow_struct_1 = Entrance(player, "Overworld Structure 1", overworld)
    ow_struct_2 = Entrance(player, "Overworld Structure 2", overworld)
    nether_struct_1 = Entrance(player, "Nether Structure 1", nether)
    nether_struct_2 = Entrance(player, "Nether Structure 2", nether)
    end_struct = Entrance(player, "The End Structure", end)

    # Hook up mandatory connections
    menu.exits.append(start)
    overworld.exits.extend([portal_nether, portal_end, ow_struct_1, ow_struct_2])
    nether.exits.extend([nether_struct_1, nether_struct_2])
    end.exits.append(end_struct)
    start.connect(overworld)
    portal_nether.connect(nether)
    portal_end.connect(end)

    world.regions += [menu, overworld, nether, end, village, outpost, fortress, bastion, end_city]

def link_minecraft_structures(world: MultiWorld, player: int):

    exits = ["Overworld Structure 1", "Overworld Structure 2", "Nether Structure 1", "Nether Structure 2", "The End Structure"]
    structs = ["Village", "Pillager Outpost", "Nether Fortress", "Bastion Remnant", "End City"]

    if world.shuffle_structures[player]: 
        # Can't put Nether Fortress in the End
        end_struct = world.random.choice([s for s in structs if s != 'Nether Fortress'])
        structs.remove(end_struct)
        world.random.shuffle(structs)
        structs.append(end_struct)

    for exit, struct in zip(exits, structs):
        world.get_entrance(exit, player).connect(world.get_region(struct, player))
        world.spoiler.set_entrance(exit, struct, 'entrance', player)

def fill_minecraft_slot_data(world: MultiWorld, player: int): 
    slot_data = {}
    seed = world.rom_seeds[player]
    for option_name in minecraft_options:
        option = getattr(world, option_name)[player]
        slot_data[option_name] = int(option.value)
    slot_data['minecraft_world_seed'] = Random(seed).getrandbits(32) # consistent and doesn't interfere with other generation
    slot_data['logic_version'] = logic_version
    return slot_data

# Generates the item pool given the table and frequencies in Items.py. 
def minecraft_gen_item_pool(world: MultiWorld, player: int):

    pool = []
    for item_name, item_data in item_table.items():
        for count in range(item_frequencies.get(item_name, 1)):
            pool.append(MinecraftItem(item_name, item_data.progression, item_data.code, player))

    prefill_pool = {}
    prefill_pool.update(events_table)
    exclusion_pools = ['hard', 'insane', 'postgame']
    for key in exclusion_pools: 
        if not getattr(world, f"include_{key}_advancements")[player]: 
            prefill_pool.update(exclusion_table[key])

    for loc_name, item_name in prefill_pool.items():
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

