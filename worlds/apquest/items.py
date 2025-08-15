from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import APQuestWorld

# Every item must have a unique integer ID associated with it.
# Even if an item doesn't exist on specific options, it must be present in item_name_to_id.
ITEM_NAME_TO_ID = {
    "Key": 1,
    "Sword": 2,
    "Shield": 3,
    "Health Upgrade": 4,
    "Confetti Cannon": 5,
}

# Items should have a defined default classification.
# In our case, we will make a dictionary from item name to classification.
ITEM_CLASSIFICATIONS = {
    "Key": ItemClassification.progression,
    "Sword": ItemClassification.progression | ItemClassification.useful,  # Items can have multiple classifications.
    "Shield": ItemClassification.progression,
    "Health Upgrade": ItemClassification.useful,
    "Confetti Cannon": ItemClassification.filler,
}

# It is common practice to override the base Item class to override the "game" field.
class APQuestItem(Item):
    game = "APQuest"


def create_all_items(world: "APQuestWorld") -> None:
    # This is the function in which we will create all the items that this world submits to the multiworld item pool.
    # There must be exactly as many items as there are locations.
    # In our case, there are six locations, so there must be six items.
    # Creating items should generally be done via the world's create_item method.

    world.multiworld.itempool += [
        world.create_item("Key"),
        world.create_item("Sword"),
        world.create_item("Shield"),
        world.create_item("Health Upgrade"),
        world.create_item("Health Upgrade"),
        world.create_item("Confetti Cannon"),
    ]


def create_item_with_correct_classification(world: "APQuestWorld", name: str) -> APQuestItem:
    # Our world class must have a create_item() function that can create any of our items by name at any time.
    # So, we make this helper function that creates the item by name with the correct classification.
    # Note: This function's content could just be the contents of world.create_item in world.py directly,
    # but it seemed nicer to have it in its own function over here in items.py.
    classification = ITEM_CLASSIFICATIONS[name]

    # It is perfectly normal and valid for an item's classification to differ based on the player's options.
    # In our case, Health Upgrades are only logically considered in hard mode.
    if name == "Health Upgrade" and world.options.hard_mode:
        classification = ItemClassification.progression

    return APQuestItem(name, classification, ITEM_NAME_TO_ID[name], world.player)
