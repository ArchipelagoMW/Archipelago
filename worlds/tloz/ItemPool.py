from BaseClasses import ItemClassification
from .Locations import level_locations, all_level_locations, standard_level_locations, shop_locations

# Swords are in starting_weapons
overworld_items = {
    "Letter": 1,
    "Power Bracelet": 1,
    "Heart Container": 1
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
basic_pool = {
    item: overworld_items.get(item, 0) + shop_items.get(item, 0)
    + major_dungeon_items.get(item, 0) + map_compass_replacements.get(item, 0)
    for item in set(overworld_items) | set(shop_items) | set(major_dungeon_items) | set(map_compass_replacements)
}

starting_weapons = ["Sword", "White Sword", "Magical Sword", "Magical Rod", "Red Candle"]
guaranteed_shop_items = ["Small Key", "Bomb", "Water of Life (Red)", "Arrow"]
starting_weapon_locations = ["Starting Sword Cave", "Letter Cave", "Armos Knights"]
dangerous_weapon_locations = starting_weapon_locations + [
    "Level 1 Compass", "Level 2 Bomb Drop (Keese)", "Level 3 Key Drop (Zols Entrance)", "Level 3 Compass"]

def generate_itempool(tlozworld):
    (pool, placed_items) = get_pool_core(tlozworld)
    tlozworld.multiworld.itempool = [tlozworld.multiworld.create_item(item, tlozworld.player) for item in pool]
    for (location_name, item) in placed_items.items():
        location = tlozworld.multiworld.get_location(location_name, tlozworld.player)
        location.place_locked_item(tlozworld.multiworld.create_item(item, tlozworld.player))
        if item == "Bomb":
            location.item.classification = ItemClassification.progression

def get_pool_core(world):
    random = world.multiworld.random

    pool = []
    placed_items = {}

    reserved_store_slots = random.sample(shop_locations[0:9], 4)

    # Guaranteed Shop Items
    for location, item in zip(reserved_store_slots, guaranteed_shop_items):
        placed_items[location] = item

    # Starting Weapon
    starting_weapon = random.choice(starting_weapons)
    if world.multiworld.StartingPosition[world.player] == 0:
        placed_items[starting_weapon_locations[0]] = starting_weapon
    elif world.multiworld.StartingPosition[world.player] == 1:
        placed_items[random.choice(starting_weapon_locations)] = starting_weapon
    elif world.multiworld.StartingPosition[world.player] == 2:
        placed_items[random.choice(dangerous_weapon_locations)] = starting_weapon
    else:
        pool.append(starting_weapon)
    for other_weapons in starting_weapons:
        if other_weapons != starting_weapon:
            pool.append(other_weapons)

    # Triforce Fragments
    fragment = "Triforce Fragment"
    if world.multiworld.ExpandedPool[world.player]:
        possible_level_locations = [location for location in all_level_locations
                                    if location not in level_locations[8]]
    else:
        possible_level_locations = [location for location in standard_level_locations
                                    if location not in level_locations[8]]
    for level in range(1, 9):
        if world.multiworld.TriforceLocations[world.player] == 0:
            placed_items[f"Level {level} Triforce"] = fragment
        elif world.multiworld.TriforceLocations[world.player] == 1:
            placed_items[possible_level_locations.pop(random.randint(0, len(possible_level_locations) - 1))] = fragment
        else:
            pool.append(fragment)

    final_pool = basic_pool
    if world.multiworld.ExpandedPool[world.player]:
        final_pool = {
            item: basic_pool.get(item, 0) + minor_dungeon_items.get(item, 0)
            for item in set(basic_pool) | set(minor_dungeon_items)
        }
    for item in final_pool.keys():
        for i in range(0, final_pool[item]):
            pool.append(item)

    return pool, placed_items
