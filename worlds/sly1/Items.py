from BaseClasses import Item, ItemClassification
from .Types import ItemData, Sly1Item, EpisodeType, episode_type_to_name, episode_type_to_shortened_name
from .Locations import get_total_locations, get_bundle_amount_for_level, did_avoid_early_bk, hourglasses_roll, \
    did_include_hourglasses
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from . import Sly1World


def create_itempool(world: "Sly1World") -> List[Item]:
    itempool: List[Item] = []

    # Determine if this player has AvoidEarlyBK enabled
    need_to_modify_item_pool = did_avoid_early_bk(world)
    starting_episode = episode_type_to_shortened_name[EpisodeType(world.options.StartingEpisode)]
    if starting_episode == "All" and need_to_modify_item_pool:
        starting_episode = world.random_episode

    # Create a local copy of item_table to modify only for the current player
    # We won't modify the global item_table directly
    final_item_table = item_table.copy() if need_to_modify_item_pool or hourglasses_roll(world) else item_table

    # If AvoidEarlyBK is enabled, adjust the key count for the starting episode
    if need_to_modify_item_pool:
        starting_key_name = f"{starting_episode} Key"
        if starting_key_name in final_item_table:
            starting_key = final_item_table[starting_key_name]
            final_item_table[starting_key_name] = starting_key._replace(count=starting_key.count - 1)

    if did_include_hourglasses(world) and hourglasses_roll(world):
        roll_name = "Progressive Roll"
        for key, item in final_item_table.items():
            if key == roll_name and item.classification == ItemClassification.useful:
                final_item_table[key] = item._replace(classification=ItemClassification.progression)

    # Create episodes except for the starting episode as items
    for episode in sly_episodes.keys():
        if starting_episode == "All":
            break
        if starting_episode == episode:
            continue
        itempool.append(create_item(world, episode))

    # Use the modified final_item_table to add items to the item pool
    for name in final_item_table.keys():
        item_type: ItemClassification = final_item_table.get(name).classification
        item_amount: int = final_item_table.get(name).count

        # Add items based on the modified final_item_table
        itempool += create_multiple_items(world, name, item_amount, item_type)

    # Create Bottle Bundles if applicable
    if world.options.CluesanityBundleSize.value > 0:
        for name, data in bottles.items():
            bundle_amount = get_bundle_amount_for_level(world, name.rsplit(' ', 1)[0])
            itempool += create_multiple_items(world, name, bundle_amount, data.classification)

    # Add the Victory item to the pool
    victory = create_item(world, "Victory")
    world.multiworld.get_location("Beat Clockwerk", world.player).place_locked_item(victory)

    # Add junk items to the pool if necessary
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
        if trap_chance > 0 and world.random.randint(1, 100) <= trap_chance:
            junk_pool.append(world.create_item(
                world.random.choices(list(trap_list.keys()), weights=list(trap_list.values()), k=1)[0]))
        else:
            junk_pool.append(world.create_item(
                world.random.choices(list(junk_list.keys()), weights=list(junk_list.values()), k=1)[0]))

    return junk_pool


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
    "Tide of Terror": ItemData(10020021, ItemClassification.progression, 0),
    "Sunset Snake Eyes": ItemData(10020022, ItemClassification.progression, 0),
    "Vicious Voodoo": ItemData(10020023, ItemClassification.progression, 0),
    "Fire in the Sky": ItemData(10020024, ItemClassification.progression, 0),
}

bottles = {
    "Stealthy Approach Bottle(s)": ItemData(10020030, ItemClassification.progression, 0),
    "Into the Machine Bottle(s)": ItemData(10020031, ItemClassification.progression, 0),
    "High Class Heist Bottle(s)": ItemData(10020032, ItemClassification.progression, 0),
    "Fire Down Below Bottle(s)": ItemData(10020033, ItemClassification.progression, 0),
    "Cunning Disguise Bottle(s)": ItemData(10020034, ItemClassification.progression, 0),
    "Gunboat Graveyard Bottle(s)": ItemData(10020035, ItemClassification.progression, 0),

    "Rocky Start Bottle(s)": ItemData(10020036, ItemClassification.progression, 0),
    "Boneyard Casino Bottle(s)": ItemData(10020037, ItemClassification.progression, 0),
    "Straight to the Top Bottle(s)": ItemData(10020038, ItemClassification.progression, 0),
    "Two to Tango Bottle(s)": ItemData(10020039, ItemClassification.progression, 0),
    "Back Alley Heist Bottle(s)": ItemData(10020040, ItemClassification.progression, 0),

    "Dread Swamp Path Bottle(s)": ItemData(10020041, ItemClassification.progression, 0),
    "Lair of the Beast Bottle(s)": ItemData(10020042, ItemClassification.progression, 0),
    "Grave Undertaking Bottle(s)": ItemData(10020043, ItemClassification.progression, 0),
    "Descent into Danger Bottle(s)": ItemData(10020044, ItemClassification.progression, 0),

    "Perilous Ascent Bottle(s)": ItemData(10020045, ItemClassification.progression, 0),
    "Flaming Temple of Flame Bottle(s)": ItemData(10020046, ItemClassification.progression, 0),
    "Unseen Foe Bottle(s)": ItemData(10020047, ItemClassification.progression, 0),
    "Duel by the Dragon Bottle(s)": ItemData(10020048, ItemClassification.progression, 0)
}

junk_items = {
    # Junk
    "Charm": ItemData(10020019, ItemClassification.filler, 0),
    "1-Up": ItemData(10020020, ItemClassification.filler, 0),

    # Traps
    "Ice Physics Trap": ItemData(10020026, ItemClassification.trap, 0),
    "Speed Change Trap": ItemData(10020027, ItemClassification.trap, 0),

    "Ball Trap": ItemData(10020028, ItemClassification.trap, 0),
    "Bentley Jumpscare Trap": ItemData(10020029, ItemClassification.trap, 0),
}

junk_weights = {
    "Charm": 40,
    "1-Up": 20
}

item_table = {
    **sly_items,
    **sly_episodes,
    **junk_items,
    **bottles
}

event_item_pairs: Dict[str, str] = {
    "Beat Raleigh": "Beat Raleigh",
    "Beat Muggshot": "Beat Muggshot",
    "Beat Mz. Ruby": "Beat Mz. Ruby",
    "Beat Panda King": "Beat Panda King"
}
