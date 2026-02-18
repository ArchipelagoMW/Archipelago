from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import Schedule1World

ITEM_NAME_TO_ID = {}
RAW_ITEM_CLASSIFICATIONS = {}

fillers = []
traps = []

# Mapping from JSON classification strings to ItemClassification flags
CLASSIFICATION_MAP = {
    "USEFUL": ItemClassification.useful,
    "PROGRESSION": ItemClassification.progression,
    "FILLER": ItemClassification.filler,
    "PROGRESSION_SKIP_BALANCING": ItemClassification.progression_skip_balancing,
    "TRAP": ItemClassification.trap
}

def load_items_data(data):
    """Load item data from JSON and populate ITEM_NAME_TO_ID and RAW_ITEM_CLASSIFICATIONS."""
    global ITEM_NAME_TO_ID, RAW_ITEM_CLASSIFICATIONS

    ITEM_NAME_TO_ID = {item.name: item.modern_id for item in data.items.values()}
    RAW_ITEM_CLASSIFICATIONS = {item.name: item.classification for item in data.items.values()}


# Each Item instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Item class and override the "game" field.
class Schedule1Item(Item):
    game = "Schedule I"

# To do this, it must define a function called world.get_filler_item_name(), which we will define in world.py later.
# For now, let's make a function that returns the name of a random filler item here in items.py.
def get_random_filler_item_name(world: Schedule1World) -> str:
    # For this purpose, we need to use a random generator.

    # IMPORTANT: Whenever you need to use a random generator, you must use world.random.
    # This ensures that generating with the same generator seed twice yields the same output.
    # DO NOT use a bare random object from Python's built-in random module.

    # Check if we should generate a trap item based on the trap_chance option.
    if world.random.randint(0, 99) < world.options.trap_chance:
        return world.random.choice(traps)
    
    # Otherwise, return a random filler item.
    return world.random.choice(fillers)


def check_option_enabled(world: Schedule1World, option_name: str) -> bool:
    """Check if an option is enabled based on option name string."""
    option_map = {
        "randomize_customers": world.options.randomize_customers,
        "randomize_dealers": world.options.randomize_dealers,
        "randomize_suppliers": world.options.randomize_suppliers,
        "randomize_level_unlocks": world.options.randomize_level_unlocks,
        "randomize_cartel_influence": world.options.randomize_cartel_influence,
        "randomize_business_properties": world.options.randomize_business_properties,
        "randomize_drug_making_properties": world.options.randomize_drug_making_properties,
    }
    return bool(option_map.get(option_name, False))


def check_option_condition(world: Schedule1World, condition_key: str) -> bool:
    """
    Parse and evaluate a compound option condition string.
    
    Supports:
    - Simple: "randomize_level_unlocks" (option must be true)
    - Negation: "!randomize_level_unlocks" (option must be false)
    - Compound AND: "randomize_level_unlocks&!randomize_customers" 
      (first must be true AND second must be false)
    
    Returns True if the condition is satisfied, False otherwise.
    """
    parts = condition_key.split('&')
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
        
        if part.startswith('!'):
            option_name = part[1:]
            expected_value = False
        else:
            option_name = part
            expected_value = True
        
        actual_value = check_option_enabled(world, option_name)
        
        if actual_value != expected_value:
            return False
    
    return True


def resolve_classification(world: Schedule1World, classification_data) -> ItemClassification:
    """
    Resolve the classification from raw JSON data based on world options.
    
    classification_data can be:
    - A string: "PROGRESSION"
    - A list: ["PROGRESSION", "USEFUL"]
    - A dict with conditions: {"!randomize_customers": ["PROGRESSION", "USEFUL"], "default": ["USEFUL"]}
    """
    # Determine which classification strings to use
    if isinstance(classification_data, dict):
        # Conditional classification - find matching condition
        classification_strings = None
        for condition_key, value in classification_data.items():
            if condition_key == "default":
                continue  # Handle default last
            if check_option_condition(world, condition_key):
                classification_strings = value
                break
        
        # Fall back to default if no condition matched
        if classification_strings is None:
            classification_strings = classification_data.get("default", "FILLER")
    else:
        classification_strings = classification_data
    
    # Convert to ItemClassification
    if isinstance(classification_strings, list):
        classification = CLASSIFICATION_MAP[classification_strings[0]]
        for class_name in classification_strings[1:]:
            classification |= CLASSIFICATION_MAP[class_name]
    else:
        classification = CLASSIFICATION_MAP[classification_strings]
    
    return classification


def create_item_with_correct_classification(world: Schedule1World, name: str) -> Schedule1Item:
    # Our world class must have a create_item() function that can create any of our items by name at any time.
    # So, we make this helper function that creates the item by name with the correct classification.
    # Note: This function's content could just be the contents of world.create_item in world.py directly,
    # but it seemed nicer to have it in its own function over here in items.py.
    classification = resolve_classification(world, RAW_ITEM_CLASSIFICATIONS[name])

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
        if not world.options.randomize_customers:
            for _ in range(world.options.cartel_influence_items_per_region):
                itempool += [world.create_item(item.name) for item in data.items.values() 
                            if "Cartel Influence" in item.tags and "Westville" not in item.tags
                            and "Suburbia" not in item.tags]
       
        # Suburbia is required for Finishing the Job
        for _ in range(world.options.cartel_influence_items_per_region):
            itempool += [world.create_item(item.name) for item in data.items.values() 
                        if "Cartel Influence" in item.tags and "Suburbia" in item.tags]
            
        # Westville starts at 500 less cartel influence. Will have 5 less cartel items as well to declutter
        # Westville is required for Vibin the Cybin
        for _ in range(world.options.cartel_influence_items_per_region - 5):
            itempool += [world.create_item(item.name) for item in data.items.values() 
                        if "Cartel Influence" in item.tags and "Westville" in item.tags]
            
    if world.options.randomize_business_properties:
        itempool += [world.create_item(item.name) for item in data.items.values() 
                     if "Business Property" in item.tags]
    
    if world.options.randomize_drug_making_properties:
        itempool += [world.create_item(item.name) for item in data.items.values() 
                     if "Drug Making Property" in item.tags]

    if world.options.randomize_dealers:
        itempool += [world.create_item(item.name) for item in data.items.values() 
                     if "Dealer" in item.tags and "Default" not in item.tags]

    if world.options.randomize_customers:
        itempool += [world.create_item(item.name) for item in data.items.values() 
                     if "Customer" in item.tags and "Default" not in item.tags]
        
    if world.options.randomize_suppliers:
        itempool += [world.create_item(item.name) for item in data.items.values() 
                     if "Supplier" in item.tags and "Default" not in item.tags]

    if world.options.randomize_sewer_key:
        itempool += [world.create_item(item.name) for item in data.items.values() 
                     if "Sewer" in item.tags]

    # Removed these from checks
    if world.options.randomize_customers:
        starting_kyle_cooley = world.create_item("Kyle Cooley Unlocked")
        world.push_precollected(starting_kyle_cooley)
        starting_austin_steiner = world.create_item("Austin Steiner Unlocked")
        world.push_precollected(starting_austin_steiner)
        starting_kathy_henderson = world.create_item("Kathy Henderson Unlocked")
        world.push_precollected(starting_kathy_henderson)
        starting_jessi_waters = world.create_item("Jessi Waters Unlocked")
        world.push_precollected(starting_jessi_waters)
        starting_sam_thompson = world.create_item("Sam Thompson Unlocked")
        world.push_precollected(starting_sam_thompson)
        starting_mick_lubbin = world.create_item("Mick Lubbin Unlocked")
        world.push_precollected(starting_mick_lubbin)
        
    # Set up traps
    for item in data.items.values():
        resolved_classification = resolve_classification(world, item.classification)
        if resolved_classification == ItemClassification.trap:
            # Create list of traps
            traps.append(item.name)

    filler_conditions = {
        "Bad Filler" : world.options.ban_bad_filler_items, 
        "Ban Progression Skip" : world.options.ban_progression_skip_items}
    
    # set up fillers
    for item in data.items.values():
        resolved_classification = resolve_classification(world, item.classification)
        if resolved_classification == ItemClassification.filler:
            is_valid = True
            for tag, should_ban in filler_conditions.items():
                if should_ban and tag in item.tags:
                    is_valid = False
                    break
            if is_valid:
                fillers.append(item.name)

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
    