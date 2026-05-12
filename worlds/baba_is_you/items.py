from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import BabaIsYouWorld

from .words import *

# Every item must have a unique integer ID associated with it.
# We will have a lookup from item name to ID here that, in world.py, we will import and bind to the world class.
# Even if an item doesn't exist on specific options, it must be present in this lookup.
ITEM_NAME_TO_ID = {
    "Speck": 1,
    "Blossom Petal": 2,
    "Blossom": 3,
    "Bonus Orb": 4,
    "Lake Key": 5,
    "Island Key": 6,
    "Ruins Key": 7,
    "Fall Key": 8,
    "Forest Key": 9,
    "Space Key": 10,
    "Garden Key": 11,
    "Chasm Key": 12,
    "Cavern Key": 13,
    "Mountain Key": 14,
    "ABC Key": 15,
    "Depths Key": 16,
    "Meta Key": 17,
    "Center Key": 18,
}

# Items should have a defined default classification.
# In our case, we will make a dictionary from item name to classification.
DEFAULT_ITEM_CLASSIFICATIONS = {
    "Speck": ItemClassification.filler,
    "Blossom Petal": ItemClassification.progression,
    "Blossom": ItemClassification.progression,
    "Bonus Orb": ItemClassification.progression,
    "Lake Key": ItemClassification.progression,
    "Island Key": ItemClassification.progression,
    "Ruins Key": ItemClassification.progression,
    "Fall Key": ItemClassification.progression,
    "Forest Key": ItemClassification.progression,
    "Space Key": ItemClassification.progression,
    "Garden Key": ItemClassification.progression,
    "Chasm Key": ItemClassification.progression,
    "Cavern Key": ItemClassification.progression,
    "Mountain Key": ItemClassification.progression,
    "ABC Key": ItemClassification.progression,
    "Depths Key": ItemClassification.progression,
    "Meta Key": ItemClassification.progression,
    "Center Key": ItemClassification.progression,
}

nextID = 101 # In case we decide to add more items, leave a large gap
# Add words to the list of items
for word in ALL_PROG_WORDS:
    ITEM_NAME_TO_ID[word] = nextID
    DEFAULT_ITEM_CLASSIFICATIONS[word] = ItemClassification.progression
    nextID += 1
for word in ALL_FILLER_WORDS:
    ITEM_NAME_TO_ID[word] = nextID
    DEFAULT_ITEM_CLASSIFICATIONS[word] = ItemClassification.filler
    nextID += 1

# Each Item instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Item class and override the "game" field.
class BabaIsYouItem(Item):
    game = "Baba Is You"


# Ontop of our regular itempool, our world must be able to create arbitrary amounts of filler as requested by core.
# To do this, it must define a function called world.get_filler_item_name(), which we will define in world.py later.
# Only one filler item exists right now.
def get_random_filler_item_name(world: BabaIsYouWorld) -> str:
    return "Speck"


def create_item_with_correct_classification(world: BabaIsYouWorld, name: str) -> BabaIsYouItem:
    # Our world class must have a create_item() function that can create any of our items by name at any time.
    # So, we make this helper function that creates the item by name with the correct classification.
    # Note: This function's content could just be the contents of world.create_item in world.py directly,
    # but it seemed nicer to have it in its own function over here in items.py.
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]
    
    # Bonuses become filler items if we aren't including "Gallery"
    # End becomes filler if reaching the end isn't our goal
    if (name == "Bonus Orb" and world.options.exclude_gallery) or (name == "End" and world.options.goal != 0):
        classification = ItemClassification.filler
    elif ITEM_NAME_TO_ID[name] > 100 and (name in ALL_PROG_WORDS):
        # Check if name is in the current progression word list; if not, mark as filler
        if not (name in get_curr_prog_words(world)):
            classification = ItemClassification.filler

    return BabaIsYouItem(name, classification, ITEM_NAME_TO_ID[name], world.player)

# I like to define item groups here. Item groups must be formatted exactly as a dictionary containing sets.
# The dictionary key is the name of the group that you can hint for, and the set inside contains everything in that group.
# You can do the same with location_name_groups in locations.py (or anywhere) if you like.
# I have only added the words seen in words.py so far. If others are included in the pool somewhere, add them as well.
item_name_groups = {
    "Nouns": {"Baba", "Flag", "Wall", "Rock", "Skull", "Lava", "Star", "Crab", "Keke", "Love",
              "Pillar", "Jelly", "Key", "Door", "Belt", "Rose", "Violet", "Water", "Robot", "Bolt",
              "Cog", "Box", "Ghost", "Ice", "Leaf", "Fence", "Me", "Tree", "Bug", "Fungus",
              "Cloud", "Rocket", "UFO", "Moon", "Dust", "Grass", "Hand", "Fruit", "Bat", "Fire", 
              "Bird", "Sun", "Tile", "Orb", "Hedge", "Cliff", "Line", "Cake", "Anni"},
    "Verbs": {"Is", "Has", "Make", "Write"},
    "Properties": {"You", "Win", "Stop", "Push", "Sink", "Defeat", "Move", "Open", "Shut", "Shift",
                   "End", "Red", "Blue", "Float", "Hot", "Weak", "Melt", "Tele", "Pull", "Up",
                   "Right", "Swap", "Best", "Fall", "More", "Word", "Sleep", "Hide", "Bonus", "Done"},
    "Conditions": {"On", "Facing", "Lonely", "Near"},
    "Special Nouns": {"Text", "Empty", "All", "Group", "Level", "Cursor", "Image"},
    "Letters": {"A", "AB", "B", "BA", "C", "E", "F", "G", "H", "I",
                "L", "M", "N", "O", "R", "S", "T", "U", "V", "W",
                "X"},
    "Misc": {"Not", "And"},
    "World Keys": {"Lake Key", "Island Key", "Ruins Key", "Fall Key", "Forest Key",
                   "Space Key", "Garden Key", "Chasm Key", "Cavern Key", "Mountain Key",
                   "ABC Key", "Depths Key", "Meta Key", "Center Key"},
}


# With those two helper functions defined, let's now get to actually creating and submitting our itempool.
def create_all_items(world: BabaIsYouWorld) -> None:
    # This is the function in which we will create all the items that this world submits to the multiworld item pool.
    # There must be exactly as many items as there are locations.

    # Creating items should generally be done via the world's create_item method.
    # First, we create a list containing all the items that always exist.

    itempool: list[Item] = []

    # Create blossoms and bonuses based on selected options
    itempool += [world.create_item("Blossom Petal") for _ in range(world.options.blossom_petals)]
    itempool += [world.create_item("Blossom") for _ in range(world.options.blossoms)]
    itempool += [world.create_item("Bonus Orb") for _ in range(3)]

    # Create keys if enabled
    if world.options.world_keys:
        itempool.append(world.create_item("Lake Key"))
        itempool.append(world.create_item("Island Key"))
        itempool.append(world.create_item("Ruins Key"))
        itempool.append(world.create_item("Fall Key"))
        itempool.append(world.create_item("Forest Key"))
        itempool.append(world.create_item("Space Key"))
        itempool.append(world.create_item("Garden Key"))
        itempool.append(world.create_item("Chasm Key"))
        itempool.append(world.create_item("Cavern Key"))
        itempool.append(world.create_item("Mountain Key"))
        if world.options.area_access >= 2: # ??? level access
            itempool.append(world.create_item("ABC Key"))
            itempool.append(world.create_item("Depths Key"))
        if world.options.area_access >= 3: # Depths level access
            itempool.append(world.create_item("Meta Key"))
        if world.options.area_access >= 4: # Center level access
            itempool.append(world.create_item("Center Key"))
    
    # Create all word items
    for word in ALL_WORDS:
        if world.options.start_with_default_words and word in DEFAULT_WORDS:
            # Start with the words in "Baba Is You"
            world.push_precollected(world.create_item(word))
        else:
            itempool.append(world.create_item(word))

    # Archipelago requires that each world submits as many locations as it submits items.
    # This is where we can use our filler and trap items.

    # The length of our itempool is easy to determine, since we have it as a list.
    number_of_items = len(itempool)

    # The number of locations is also easy to determine, but we have to be careful.
    # Just calling len(world.get_locations()) would report an incorrect number, because of our *event locations*.
    # What we actually want is the number of *unfilled* locations. Luckily, there is a helper method for this:
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))

    # Now, we just subtract the number of items from the number of locations to get the number of empty item slots.
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    # Finally, we create that many filler items and add them to the itempool.
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    # With our world's itempool finalized, we now need to submit it to the multiworld itempool.
    # This is how the generator actually knows about the existence of our items.
    world.multiworld.itempool += itempool
