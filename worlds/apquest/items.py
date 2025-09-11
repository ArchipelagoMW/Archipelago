from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import APQuestWorld

# Every item must have a unique integer ID associated with it.
# We will have a lookup from item name to ID here that, in world.py, we will import and bind to the world class.
# Even if an item doesn't exist on specific options, it must be present in this lookup.
ITEM_NAME_TO_ID = {
    "Key": 1,
    "Sword": 2,
    "Shield": 3,
    "Hammer": 4,
    "Health Upgrade": 5,
    "Confetti Cannon": 6,
}

# Items should have a defined default classification.
# In our case, we will make a dictionary from item name to classification.
ITEM_CLASSIFICATIONS = {
    "Key": ItemClassification.progression,
    "Sword": ItemClassification.progression | ItemClassification.useful,  # Items can have multiple classifications.
    "Shield": ItemClassification.progression,
    "Hammer": ItemClassification.progression,
    "Health Upgrade": ItemClassification.useful,
    "Confetti Cannon": ItemClassification.filler,
    # There is a fourth classification: ItemClassification.trap, for items that have a negative effect.
    # APQuest doesn't have any of these items, but an example would be:
    # "Slowness Trap": ItemClassification.trap
}


# It is common practice to override the base Item class to override the "game" field.
class APQuestItem(Item):
    game = "APQuest"


def create_all_items(world: APQuestWorld) -> None:
    # This is the function in which we will create all the items that this world submits to the multiworld item pool.
    # There must be exactly as many items as there are locations.
    # In our case, there are either six or seven locations.
    # We must make sure that when there are six locations, there are six items,
    # and when there are seven locations, there are seven items.

    # Creating items should generally be done via the world's create_item method.
    # First, we create a list containing all the items that always exist.

    itempool = [
        world.create_item("Key"),
        world.create_item("Sword"),
        world.create_item("Shield"),
        world.create_item("Health Upgrade"),
        world.create_item("Health Upgrade"),
    ]

    # Some items may only exist if the player enables certain options.
    # In our case, If the hammer option is enabled, the sixth item is the Hammer.
    # Otherwise, we add a filler Confetti Cannon.
    if world.options.hammer:
        # Once again, it is important to stress that even though the Hammer doesn't always exist,
        # it must be present in the worlds location_name_to_id.
        # Whether it is actually in the itempool is determined purely by whether we create and add the item here.
        itempool.append(world.create_item("Hammer"))

    # Archipelago requires that each world submits as many locations as it submits items.
    # This is what filler is for. In our case, that's the Confetti Cannon.
    # Creating filler items works the same as any other item. But there is a question:
    # How many Confetti Cannons do we actually need to create?
    # In regions.py, we created either six or seven locations depending on the "extra_starting_chest" option.
    # In this function, we have created five or six items depending on whether the "hammer" option is enabled.
    # We *could* have a really complicated if-else tree checking the options again, but there is a better way.
    # We can compare the size of our itempool so far to the amount of locations in our world.

    # The length of our itempool is easy to determine, since we have it as a list.
    amount_of_items = len(itempool)

    # The amount of locations is also easy to determine, but we have to be careful.
    # Just calling len(world.get_locations()) would report an incorrect number, because of our *event locations*.
    # What we actually want is the amount of *unfilled* locations. Luckily, there is a helper method for this:
    amount_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))

    # Now, we just subtract the amount of items from the amount of locations to get the number of empty item slots.
    needed_amount_of_filler = amount_of_unfilled_locations - amount_of_items

    # Finally, we create that many filler items and add them to the itempool.
    # Important: Make sure you're actually submitting different instances of the item!
    # In Python, it can be easy to accidentally submit two references to the same object rather than two objects.
    itempool += [world.create_item("Confetti Cannon") for _ in range(needed_amount_of_filler)]

    # Finally, we just have append our itempool to the multiworld itempool.
    world.multiworld.itempool += itempool

    # Sometimes, you might want the player to start with certain items already in their inventory.
    # These items are called "precollected items".
    # They will be sent as soon as they connect for the first time (depending on your client's item handling flag).
    # Players can add precollected items themselves via the generic "start_inventory" option.
    # If you want to add your own precollected items, you can do so via world.push_precollected().
    if world.options.start_with_one_confetti_cannon:
        # We're adding a filler item, but you can also add progression items to the player's precollected inventory.
        starting_confetti_cannon = world.create_item("Confetti Cannon")
        world.push_precollected(starting_confetti_cannon)


def create_item_with_correct_classification(world: APQuestWorld, name: str) -> APQuestItem:
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
