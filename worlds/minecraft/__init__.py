from random import Random
from .Items import MinecraftItem, item_table, item_frequencies
from .Locations import exclusion_table, events_table
from .Regions import link_minecraft_structures
from .Rules import set_rules

from BaseClasses import Region, Entrance, Location, MultiWorld, Item
from Options import minecraft_options

client_version = (0, 3)

def get_mc_data(world: MultiWorld, player: int):
    exits = ["Overworld Structure 1", "Overworld Structure 2", "Nether Structure 1", "Nether Structure 2", "The End Structure"]
    return {
        'world_seed': Random(world.rom_seeds[player]).getrandbits(32), # consistent and doesn't interfere with other generation
        'seed_name': world.seed_name,
        'player_name': world.get_player_names(player),
        'player_id': player,
        'client_version': client_version,
        'structures': {exit: world.get_entrance(exit, player).connected_region.name for exit in exits}
    }

def generate_mc_data(world: MultiWorld, player: int): 
    import base64, json
    from Utils import output_path

    data = get_mc_data(world, player)
    filename = f"AP_{world.seed_name}_P{player}_{world.get_player_names(player)}.apmc"
    with open(output_path(filename), 'wb') as f: 
        f.write(base64.b64encode(bytes(json.dumps(data), 'utf-8')))

def fill_minecraft_slot_data(world: MultiWorld, player: int): 
    slot_data = get_mc_data(world, player)
    for option_name in minecraft_options:
        option = getattr(world, option_name)[player]
        slot_data[option_name] = int(option.value)
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
        world.push_item(location, item, collect=False)
        pool.remove(item)
        location.event = item_data.progression
        location.locked = True

    world.itempool += pool

# Generate Minecraft world. 
def gen_minecraft(world: MultiWorld, player: int):
    link_minecraft_structures(world, player)
    minecraft_gen_item_pool(world, player)
    set_rules(world, player)

