from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import Schedule1World

ITEM_NAME_TO_ID = {}
DEFAULT_ITEM_CLASSIFICATIONS = {}

def load_items_data(data):
    """Load item data from JSON and populate ITEM_NAME_TO_ID and DEFAULT_ITEM_CLASSIFICATIONS."""
    global ITEM_NAME_TO_ID, DEFAULT_ITEM_CLASSIFICATIONS
    ITEM_NAME_TO_ID = {item.name: item.modern_id for item in data.items.values()}
    DEFAULT_ITEM_CLASSIFICATIONS = {item.name: item.classification for item in data.items.values()}

# Each Item instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Item class and override the "game" field.
class Schedule1Item(Item):
    game = "Schedule1"

# To do this, it must define a function called world.get_filler_item_name(), which we will define in world.py later.
# For now, let's make a function that returns the name of a random filler item here in items.py.
def get_random_filler_item_name(world: Schedule1World, data) -> str:
    # For this purpose, we need to use a random generator.

    # IMPORTANT: Whenever you need to use a random generator, you must use world.random.
    # This ensures that generating with the same generator seed twice yields the same output.
    # DO NOT use a bare random object from Python's built-in random module.
    
    filler_pool_type = world.options.filler_item_pool_type
    
    if filler_pool_type == 0:
        # Random distribution: All items classified as filler
        all_fillers = [item.name for item in data.items.values() 
                       if item.classification == ItemClassification.filler]
        return world.random.choice(all_fillers)
    
    elif filler_pool_type == 1:
        # Random No Bad Items: All fillers NOT tagged "Bad Filler"
        non_bad_fillers = [item.name for item in data.items.values() 
                          if item.classification == ItemClassification.filler 
                          and "Bad Filler" not in item.tags]
        return world.random.choice(non_bad_fillers)
    
    elif filler_pool_type == 2:
        # Random Only Good Items: All fillers NOT tagged "Bad Filler" or "Basic Filler"
        good_fillers = [item.name for item in data.items.values() 
                       if item.classification == ItemClassification.filler 
                       and "Bad Filler" not in item.tags 
                       and "Basic Filler" not in item.tags]
        return world.random.choice(good_fillers)
    
    # Fallback to a default filler. SHOULD NEVER HAPPEN.
    return "OG Kush Seed"


def create_item_with_correct_classification(world: Schedule1World, name: str) -> Schedule1Item:
    # Our world class must have a create_item() function that can create any of our items by name at any time.
    # So, we make this helper function that creates the item by name with the correct classification.
    # Note: This function's content could just be the contents of world.create_item in world.py directly,
    # but it seemed nicer to have it in its own function over here in items.py.
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]

    # Item classification does not need to change based on options in Schedule1's case,
    return Schedule1Item(name, classification, ITEM_NAME_TO_ID[name], world.player)


# With those two helper functions defined, let's now get to actually creating and submitting our itempool.
def create_all_items(world: Schedule1World, data) -> None:
    # Creating items should generally be done via the world's create_item method.
    # First, we create a list containing all the items that always exist.

    itempool: list[Item] = []
    
    # Create bundles bundles
    # Hard coding the bundles here based on options is more efficient than adding them through the json data
    for _ in range(world.options.number_of_cash_bundles):
        itempool += [world.create_item("Cash Bundle")]
    
    for _ in range(world.options.number_of_xp_bundles):
        itempool += [world.create_item("XP Bundle")]

    if world.options.randomize_level_unlocks:
        # If the randomize_level_unlocks option is enabled, create all items tagged as "Level Up Reward".
        itempool += [world.create_item(item.name) for item in data.items.values() 
                     if "Level Up Reward" in item.tags]

    # Add cartel influence items based on options
    if world.options.randomize_cartel_influence:
        itempool += [world.create_item(item.name) for item in data.items.values() 
                     if "Cartel Influence" in item.tags]

    if world.options.randomize_business_properties:
        itempool += [world.create_item(item.name) for item in data.items.values() 
                     if "Business Property" in item.tags]
    
    if world.options.randomize_drug_making_properties:
        itempool += [world.create_item(item.name) for item in data.items.values() 
                     if "Drug Making Property" in item.tags]

    if world.options.randomize_dealers:
        itempool += [world.create_item(item.name) for item in data.items.values() 
                     if "Dealer" in item.tags]

    if world.options.randomize_customers:
        itempool += [world.create_item(item.name) for item in data.items.values() 
                     if "Customer" in item.tags]

    # The length of our itempool is easy to determine, since we have it as a list.
    number_of_items = len(itempool)

    # What we actually want is the number of *unfilled* locations. Luckily, there is a helper method for this:
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))

    # Now, we just subtract the number of items from the number of locations to get the number of empty item slots.
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    # Finally, we create that many filler items and add them to the itempool.
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    # This is how the generator actually knows about the existence of our items.
    world.multiworld.itempool += itempool