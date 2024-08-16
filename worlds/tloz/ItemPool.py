from collections import Counter

from BaseClasses import ItemClassification
from .Locations import level_locations, all_level_locations, standard_level_locations, shop_locations
from .Options import TriforceLocations, StartingPosition

# Swords are in starting_weapons
overworld_items = {
    "Letter": 1,
    "Power Bracelet": 1,
    "Heart Container": 1,
    "Sword": 1
}

# Bomb, Arrow, 1 Small Key and Red Water of Life are in guaranteed_shop_items
shop_items = {
    "Magical Shield": 3,
    "Food": 2,
    "Small Key": 1,
    "Candle": 1,
    "Recovery Heart": 1,
    "Blue Ring": 1,
    "Water of Life (Blue)": 1
}

# Magical Rod and Red Candle are in starting_weapons, Triforce Fragments are added in its section of get_pool_core
major_dungeon_items = {
    "Heart Container": 8,
    "Bow": 1,
    "Boomerang": 1,
    "Magical Boomerang": 1,
    "Raft": 1,
    "Stepladder": 1,
    "Recorder": 1,
    "Magical Key": 1,
    "Book of Magic": 1,
    "Silver Arrow": 1,
    "Red Ring": 1
}

minor_dungeon_items = {
    "Bomb": 23,
    "Small Key": 45,
    "Five Rupees": 17
}

take_any_items = {
    "Heart Container": 4
}

# Map/Compasses: 18
# Reasoning: Adding some variety to the vanilla game.

map_compass_replacements = {
    "Fairy": 6,
    "Clock": 3,
    "Water of Life (Red)": 1,
    "Water of Life (Blue)": 2,
    "Bomb": 2,
    "Small Key": 2,
    "Five Rupees": 2
}
basic_pool = Counter()
basic_pool.update(overworld_items)
basic_pool.update(shop_items)
basic_pool.update(major_dungeon_items)
basic_pool.update(map_compass_replacements)

starting_weapons = ["Sword", "White Sword", "Magical Sword", "Magical Rod", "Red Candle"]
guaranteed_shop_items = ["Small Key", "Bomb", "Water of Life (Red)", "Arrow"]
starting_weapon_locations = ["Starting Sword Cave", "Letter Cave", "Armos Knights"]
dangerous_weapon_locations = [
    "Level 1 Compass", "Level 2 Bomb Drop (Keese)", "Level 3 Key Drop (Zols Entrance)", "Level 3 Compass"]

def generate_itempool(tlozworld):
    (pool, placed_items) = get_pool_core(tlozworld)
    tlozworld.multiworld.itempool.extend([tlozworld.multiworld.create_item(item, tlozworld.player) for item in pool])
    for (location_name, item) in placed_items.items():
        location = tlozworld.multiworld.get_location(location_name, tlozworld.player)
        location.place_locked_item(tlozworld.multiworld.create_item(item, tlozworld.player))
        if item == "Bomb":
            location.item.classification = ItemClassification.progression

def get_pool_core(world):
    random = world.random

    pool = []
    placed_items = {}
    minor_items = dict(minor_dungeon_items)

    # Guaranteed Shop Items
    reserved_store_slots = random.sample(shop_locations[0:9], 4)
    for location, item in zip(reserved_store_slots, guaranteed_shop_items):
        placed_items[location] = item

    # Starting Weapon
    start_weapon_locations = starting_weapon_locations.copy()
    final_starting_weapons = [weapon for weapon in starting_weapons
                              if weapon not in world.options.non_local_items]
    if not final_starting_weapons:
        final_starting_weapons = starting_weapons
    starting_weapon = random.choice(final_starting_weapons)
    if world.options.StartingPosition == StartingPosition.option_safe:
        placed_items[start_weapon_locations[0]] = starting_weapon
    elif world.options.StartingPosition in \
            [StartingPosition.option_unsafe, StartingPosition.option_dangerous]:
        if world.options.StartingPosition == StartingPosition.option_dangerous:
            for location in dangerous_weapon_locations:
                if world.options.ExpandedPool or "Drop" not in location:
                    start_weapon_locations.append(location)
        placed_items[random.choice(start_weapon_locations)] = starting_weapon
    else:
        pool.append(starting_weapon)
    for other_weapons in starting_weapons:
        if other_weapons != starting_weapon:
            pool.append(other_weapons)

    # Triforce Fragments
    fragment = "Triforce Fragment"
    if world.options.ExpandedPool:
        possible_level_locations = [location for location in all_level_locations
                                    if location not in level_locations[8]]
    else:
        possible_level_locations = [location for location in standard_level_locations
                                    if location not in level_locations[8]]
    for location in placed_items.keys():
        if location in possible_level_locations:
            possible_level_locations.remove(location)
    for level in range(1, 9):
        if world.options.TriforceLocations == TriforceLocations.option_vanilla:
            placed_items[f"Level {level} Triforce"] = fragment
        elif world.options.TriforceLocations == TriforceLocations.option_dungeons:
            placed_items[possible_level_locations.pop(random.randint(0, len(possible_level_locations) - 1))] = fragment
        else:
            pool.append(fragment)

    # Finish Pool
    final_pool = basic_pool
    if world.options.ExpandedPool:
        final_pool = Counter()
        final_pool.update(basic_pool)
        final_pool.update(minor_items)
        final_pool.update(take_any_items)
        final_pool["Five Rupees"] -= 1
    for item in final_pool.keys():
        for i in range(0, final_pool[item]):
            pool.append(item)

    return pool, placed_items
