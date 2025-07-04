from typing import TYPE_CHECKING

from BaseClasses import ItemClassification as IC
from Fill import FillError

from ..Items import ITEM_TABLE, item_factory
from ..Options import DungeonItem
from .Dungeons import get_dungeon_item_pool_player

if TYPE_CHECKING:
    from .. import TWWWorld

VANILLA_DUNGEON_ITEM_LOCATIONS: dict[str, list[str]] = {
    "DRC Small Key": [
        "Dragon Roost Cavern - First Room",
        "Dragon Roost Cavern - Boarded Up Chest",
        "Dragon Roost Cavern - Rat Room Boarded Up Chest",
        "Dragon Roost Cavern - Bird's Nest",
    ],
    "FW Small Key": [
        "Forbidden Woods - Vine Maze Right Chest"
    ],
    "TotG Small Key": [
        "Tower of the Gods - Hop Across Floating Boxes",
        "Tower of the Gods - Floating Platforms Room"
    ],
    "ET Small Key": [
        "Earth Temple - Transparent Chest in First Crypt",
        "Earth Temple - Casket in Second Crypt",
        "Earth Temple - End of Foggy Room With Floormasters",
    ],
    "WT Small Key": [
        "Wind Temple - Spike Wall Room - First Chest",
        "Wind Temple - Chest Behind Seven Armos"
    ],

    "DRC Big Key":  ["Dragon Roost Cavern - Big Key Chest"],
    "FW Big Key":   ["Forbidden Woods - Big Key Chest"],
    "TotG Big Key": ["Tower of the Gods - Big Key Chest"],
    "ET Big Key":   ["Earth Temple - Big Key Chest"],
    "WT Big Key":   ["Wind Temple - Big Key Chest"],

    "DRC Dungeon Map":  ["Dragon Roost Cavern - Alcove With Water Jugs"],
    "FW Dungeon Map":   ["Forbidden Woods - First Room"],
    "TotG Dungeon Map": ["Tower of the Gods - Chest Behind Bombable Walls"],
    "FF Dungeon Map":   ["Forsaken Fortress - Chest Outside Upper Jail Cell"],
    "ET Dungeon Map":   ["Earth Temple - Transparent Chest In Warp Pot Room"],
    "WT Dungeon Map":   ["Wind Temple - Chest In Many Cyclones Room"],

    "DRC Compass":  ["Dragon Roost Cavern - Rat Room"],
    "FW Compass":   ["Forbidden Woods - Vine Maze Left Chest"],
    "TotG Compass": ["Tower of the Gods - Skulls Room Chest"],
    "FF Compass":   ["Forsaken Fortress - Chest Guarded By Bokoblin"],
    "ET Compass":   ["Earth Temple - Chest In Three Blocks Room"],
    "WT Compass":   ["Wind Temple - Chest In Middle Of Hub Room"],
}


def generate_itempool(world: "TWWWorld") -> None:
    """
    Generate the item pool for the world.

    :param world: The Wind Waker game world.
    """
    multiworld = world.multiworld

    # Get the core pool of items.
    pool, precollected_items = get_pool_core(world)

    # Add precollected items to the multiworld's `precollected_items` list.
    for item in precollected_items:
        multiworld.push_precollected(item_factory(item, world))

    # Place a "Victory" item on "Defeat Ganondorf" for the spoiler log.
    world.get_location("Defeat Ganondorf").place_locked_item(item_factory("Victory", world))

    # Create the pool of the remaining shuffled items.
    items = item_factory(pool, world)
    world.random.shuffle(items)

    multiworld.itempool += items

    # Dungeon items should already be created, so handle those separately.
    handle_dungeon_items(world)


def get_pool_core(world: "TWWWorld") -> tuple[list[str], list[str]]:
    """
    Get the core pool of items and precollected items for the world.

    :param world: The Wind Waker game world.
    :return: A tuple of the item pool and precollected items.
    """
    pool: list[str] = []
    precollected_items: list[str] = []

    # Split items into three different pools: progression, useful, and filler.
    progression_pool: list[str] = []
    useful_pool: list[str] = []
    filler_pool: list[str] = []
    for item, data in ITEM_TABLE.items():
        if data.type == "Item":
            adjusted_classification = world.item_classification_overrides.get(item)
            classification = data.classification if adjusted_classification is None else adjusted_classification

            if classification & IC.progression:
                progression_pool.extend([item] * data.quantity)
            elif classification & IC.useful:
                useful_pool.extend([item] * data.quantity)
            else:
                filler_pool.extend([item] * data.quantity)

    # If the player starts with a sword, add one to the precollected items list and remove one from the item pool.
    if world.options.sword_mode == "start_with_sword":
        precollected_items.append("Progressive Sword")
        progression_pool.remove("Progressive Sword")
    # Or, if it's swordless mode, remove all swords from the item pool.
    elif world.options.sword_mode == "swordless":
        useful_pool = [item for item in useful_pool if item != "Progressive Sword"]

    # Assign useful and filler items to item pools in the world.
    world.random.shuffle(useful_pool)
    world.random.shuffle(filler_pool)
    world.useful_pool = useful_pool
    world.filler_pool = filler_pool

    # Add filler items to place into excluded locations.
    excluded_locations = world.progress_locations.intersection(world.options.exclude_locations)
    pool.extend([world.get_filler_item_name() for _ in excluded_locations])

    # The remaining of items left to place should be the same as the number of non-excluded locations in the world.
    nonexcluded_locations = [
        location
        for location in world.multiworld.get_locations(world.player)
        if location.name not in world.options.exclude_locations
    ]
    num_items_left_to_place = len(nonexcluded_locations) - 1

    # Account for the dungeon items that have already been created.
    for dungeon in world.dungeons.values():
        num_items_left_to_place -= len(dungeon.all_items)

    # All progression items are added to the item pool.
    if len(progression_pool) > num_items_left_to_place:
        raise FillError(
            "There are insufficient locations to place progression items! "
            f"Trying to place {len(progression_pool)} items in only {num_items_left_to_place} locations."
        )
    pool.extend(progression_pool)
    num_items_left_to_place -= len(progression_pool)

    # Place useful items, then filler items to fill out the remaining locations.
    pool.extend([world.get_filler_item_name(strict=False) for _ in range(num_items_left_to_place)])

    return pool, precollected_items


def handle_dungeon_items(world: "TWWWorld") -> None:
    """
    Handle the placement of dungeon items in the world.

    :param world: The Wind Waker game world.
    """
    player = world.player
    multiworld = world.multiworld
    options = world.options

    dungeon_items = [
        item
        for item in get_dungeon_item_pool_player(world)
        if item.name not in multiworld.worlds[player].dungeon_local_item_names
    ]

    for x in range(len(dungeon_items) - 1, -1, -1):
        item = dungeon_items[x]

        # Consider dungeon items in non-required dungeons as filler.
        if item.dungeon.name in world.boss_reqs.banned_dungeons:
            item.classification = IC.filler

        option: DungeonItem
        if item.type == "Big Key":
            option = options.randomize_bigkeys
        elif item.type == "Small Key":
            option = options.randomize_smallkeys
        else:
            option = options.randomize_mapcompass

        if option == "startwith":
            dungeon_items.pop(x)
            multiworld.push_precollected(item)
            multiworld.itempool.append(item_factory(world.get_filler_item_name(), world))
        elif option == "vanilla":
            for location_name in VANILLA_DUNGEON_ITEM_LOCATIONS[item.name]:
                location = world.get_location(location_name)
                if location.item is None:
                    dungeon_items.pop(x)
                    location.place_locked_item(item)
                    break
            else:
                raise FillError(f"Could not place dungeon item in vanilla location: {item}")

    multiworld.itempool.extend([item for item in dungeon_items])
