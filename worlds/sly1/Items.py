import random

from BaseClasses import Item, ItemClassification
from .Types import ItemData, Sly1Item, EpisodeType, episode_type_to_name, episode_type_to_shortened_name
from .Locations import get_total_locations
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from . import Sly1World

def create_itempool(world: "Sly1World") -> List[Item]:
    itempool: List[Item] = []

    # Remove starting episode
    starting_episode = (episode_type_to_name[EpisodeType(world.options.StartingEpisode)])
    if starting_episode == "All":
        for episode in sly_episodes.keys():
            del item_table[episode]
    else:
        del item_table[starting_episode]

    for name in item_table.keys():
        item_type: ItemClassification = item_table.get(name).classification
        item_amount: int = item_table.get(name).count
    
        itempool += create_multiple_items(world, name, item_amount, item_type)

    victory = create_item(world, "Victory")
    world.multiworld.get_location("Beat Clockwerk", world.player).place_locked_item(victory)

    itempool += create_junk_items(world, get_total_locations(world) - len(itempool) - len(event_item_pairs) - 1)
    return itempool

def create_item(world: "Sly1World", name: str) -> Item:
    data = item_table[name]
    return Sly1Item(name, data.classification, data.ap_code, world.player)

def create_multiple_items(world: "Sly1World", name: str, count: int = 1,
                          item_type: ItemClassification = ItemClassification.progression) -> List[Item]:
    data = item_table[name]
    itemlist: List[Item] = []

    for i in range(count):
        itemlist += [Sly1Item(name, item_type, data.ap_code, world.player)]

    return itemlist

def create_junk_items(world: "Sly1World", count: int) -> List[Item]:
    trap_chance = world.options.TrapChance.value
    junk_pool: List[Item] = []
    junk_list: Dict[str, int] = {}
    trap_list: Dict[str, int] = {}

    for name in item_table.keys():
        ic = item_table[name].classification
        if ic == ItemClassification.filler:
            junk_list[name] = junk_weights.get(name)

        elif trap_chance > 0 and ic == ItemClassification.trap:
            if name == "Ice Physics Trap":
                trap_list[name] = world.options.IcePhysicsTrapWeight.value
            elif name == "Speed Change Trap":
                trap_list[name] = world.options.SpeedChangeTrapWeight.value
            elif name == "Bentley Jumpscare Trap":
                trap_list[name] = world.options.BentleyJumpscareTrapWeight.value
            elif name == "Ball Trap":
                trap_list[name] = world.options.BallTrapWeight.value

    for i in range(count):
        if trap_chance > 0 and world.random.randint(1,100) <= trap_chance:
            junk_pool.append(world.create_item(
                world.random.choices(list(trap_list.keys()), weights=list(trap_list.values()), k=1)[0]))
        else:
            junk_pool.append(world.create_item(
                world.random.choices(list(junk_list.keys()), weights=list(junk_list.values()), k=1)[0]))

    return junk_pool

def set_keys(starting_episode: str):
    starting_key = f'{starting_episode} Key'
    key = item_table[starting_key]
    updated_key = ItemData(key.ap_code, key.classification, key.count - 1)
    item_table.update({starting_key: updated_key})

sly_items = {
    # Progressive Moves
    "Progressive Dive Attack": ItemData(10020001, ItemClassification.useful, 2),
    "Progressive Roll": ItemData(10020002, ItemClassification.useful, 2),
    "Progressive Slow Motion": ItemData(10020003, ItemClassification.useful, 3),
    "Progressive Safety": ItemData(10020007, ItemClassification.useful, 2),
    "Progressive Invisibility": ItemData(10020010, ItemClassification.progression, 2),
    
    # Non-progressive Moves
    "Coin Magnet": ItemData(10020004, ItemClassification.useful),
    "Mine": ItemData(10020005, ItemClassification.useful),
    "Fast": ItemData(10020006, ItemClassification.useful),
    "Decoy": ItemData(10020008, ItemClassification.useful),
    "Hacking": ItemData(10020009, ItemClassification.useful),

    # Blueprints
    "ToT Blueprints": ItemData(10020011, ItemClassification.useful),
    "SSE Blueprints": ItemData(10020012, ItemClassification.useful),
    "VV Blueprints": ItemData(10020013, ItemClassification.useful),
    "FitS Blueprints": ItemData(10020014, ItemClassification.useful),

    # Keys
    "ToT Key": ItemData(10020015, ItemClassification.progression, 7),
    "SSE Key": ItemData(10020016, ItemClassification.progression, 7),
    "VV Key": ItemData(10020017, ItemClassification.progression, 7),
    "FitS Key": ItemData(10020018, ItemClassification.progression, 7),

    # Victory
    "Victory": ItemData(10020025, ItemClassification.progression, 0)
}

sly_episodes = {
    "Tide of Terror": ItemData(10020021, ItemClassification.progression),
    "Sunset Snake Eyes": ItemData(10020022, ItemClassification.progression),
    "Vicious Voodoo": ItemData(10020023, ItemClassification.progression),
    "Fire in the Sky": ItemData(10020024, ItemClassification.progression),
}

junk_items = {
    # Junk
    "Charm": ItemData(10020019, ItemClassification.filler, 0),
    "1-Up": ItemData(10020020, ItemClassification.filler, 0),

    # Traps
    "Ice Physics Trap": ItemData(10020021, ItemClassification.trap, 0),
    "Speed Change Trap": ItemData(10020022, ItemClassification.trap, 0),

    "Ball Trap": ItemData(10020023, ItemClassification.trap, 0),
    "Bentley Jumpscare Trap": ItemData(10020024, ItemClassification.trap, 0),
}

junk_weights = {
    "Charm": 40,
    "1-Up": 20
}

item_table = {
    **sly_items,
    **sly_episodes,
    **junk_items
}

event_item_pairs: Dict[str, str] = {
    "Beat Raleigh": "Beat Raleigh",
    "Beat Muggshot": "Beat Muggshot",
    "Beat Mz. Ruby": "Beat Mz. Ruby",
    "Beat Panda King": "Beat Panda King"
}