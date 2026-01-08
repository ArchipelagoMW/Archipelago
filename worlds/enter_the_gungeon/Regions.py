import typing
from BaseClasses import MultiWorld, Region, Entrance, Location
from .Locations import GungeonLocation, location_table, event_location_table
from .Items import item_table
from .Options import GungeonOptions

def get_total_chests(options: GungeonOptions):
    total_locations = options.random_gun_tier_d.value
    total_locations += options.random_gun_tier_c.value
    total_locations += options.random_gun_tier_b.value
    total_locations += options.random_gun_tier_a.value
    total_locations += options.random_gun_tier_s.value
    total_locations += options.random_item_tier_d.value
    total_locations += options.random_item_tier_c.value
    total_locations += options.random_item_tier_b.value
    total_locations += options.random_item_tier_a.value
    total_locations += options.random_item_tier_s.value
    # Gnawed Key, Old Crest, Weird Egg
    total_locations += 3
    total_locations += options.pickup_amount.value
    total_locations += options.trap_amount.value
    return total_locations

def create_regions(world: MultiWorld, options: GungeonOptions, player: int):
    region = Region("Menu", player, world, "")

    # Fill in locations equal to our item amount
    for i in range(0, get_total_chests(options)):
        loc_name = f"Chest {i + 1} (Any Rarity)"
        region.locations.append(GungeonLocation(player, loc_name, location_table[loc_name], region))

    # Add event locations
    for name in event_location_table:
        region.locations.append(GungeonLocation(player, name, None, region))
        
    world.regions.append(region)
