from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import GatoRobotoWorld

ITEM_NAME_TO_ID = {
    "Rocket": 10210,
    "Spin Jump": 10215,
    "Dash": 10216,
    "Hopper": 10214,
    "Cooler": 10211,
    "Decoder": 10209,
    "Big Shot": 10212,
    "Repeater": 10213,
    "Health Upgrade": 10208,
    "Palette 02": 10002,
    "Palette 03": 10003,
    "Palette 04": 10004,
    "Palette 05": 10005,
    "Palette 06": 10006,
    "Palette 07": 10007,
    "Palette 08": 10008,
    "Palette 09": 10009,
    "Palette 10": 10010,
    "Palette 11": 10011,
    "Palette 12": 10012,
    "Palette 13": 10013,
    "Palette 14": 10014,
    "Palette 15": 10015,
    "Water Level": 10237,
    "Hotboy defeated": 10254,
    "Lava Cooled": 10257,
    "Vent Level": 10268,
    "Cute Meow": 10001,
}

DEFAULT_ITEM_CLASSIFICATIONS = {
    "Rocket": ItemClassification.progression | ItemClassification.useful,
    "Spin Jump": ItemClassification.progression,
    "Dash": ItemClassification.progression,
    "Hopper": ItemClassification.progression,
    "Cooler": ItemClassification.progression,
    "Decoder": ItemClassification.progression,
    "Big Shot": ItemClassification.useful,
    "Repeater": ItemClassification.useful,
    "Palette 02": ItemClassification.progression_deprioritized_skip_balancing,
    "Palette 03": ItemClassification.progression_deprioritized_skip_balancing,
    "Palette 04": ItemClassification.progression_deprioritized_skip_balancing,
    "Palette 05": ItemClassification.progression_deprioritized_skip_balancing,
    "Palette 06": ItemClassification.progression_deprioritized_skip_balancing,
    "Palette 07": ItemClassification.progression_deprioritized_skip_balancing,
    "Palette 08": ItemClassification.progression_deprioritized_skip_balancing,
    "Palette 09": ItemClassification.progression_deprioritized_skip_balancing,
    "Palette 10": ItemClassification.progression_deprioritized_skip_balancing,
    "Palette 11": ItemClassification.progression_deprioritized_skip_balancing,
    "Palette 12": ItemClassification.progression_deprioritized_skip_balancing,
    "Palette 13": ItemClassification.progression_deprioritized_skip_balancing,
    "Palette 14": ItemClassification.progression_deprioritized_skip_balancing,
    "Palette 15": ItemClassification.progression_deprioritized_skip_balancing,
    "Health Upgrade": ItemClassification.useful,
    "Water Level": ItemClassification.progression,
    "Hotboy defeated": ItemClassification.progression,
    "Lava Cooled": ItemClassification.progression,
    "Vent Level": ItemClassification.progression_skip_balancing,
    "Cute Meow": ItemClassification.filler,
}

class GatoRobotoItem(Item):
    game = "Gato Roboto B-Side"

def create_item_with_correct_classification(world: GatoRobotoWorld, name: str) -> GatoRobotoItem:
    # Our world class must have a create_item() function that can create any of our items by name at any time.
    # So, we make this helper function that creates the item by name with the correct classification.
    # Note: This function's content could just be the contents of world.create_item in world.py directly,
    # but it seemed nicer to have it in its own function over here in items.py.
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]
    if name == "Big Shot" and world.options.use_smallmech:
        classification = ItemClassification.trap

    return GatoRobotoItem(name, classification, ITEM_NAME_TO_ID[name], world.player)

# With those two helper functions defined, let's now get to actually creating and submitting our itempool.
def create_all_items(world: GatoRobotoWorld) -> None:
    # This is the function in which we will create all the items that this world submits to the multiworld item pool.
    # There must be exactly as many items as there are locations.
    # In our case, there are either six or seven locations.
    # We must make sure that when there are six locations, there are six items,
    # and when there are seven locations, there are seven items.

    # Creating items should generally be done via the world's create_item method.
    # First, we create a list containing all the items that always exist.

    itempool: list[Item] = [
        world.create_item("Rocket"),
        world.create_item("Dash"),
        world.create_item("Spin Jump"),
        world.create_item("Hopper"),
        world.create_item("Cooler"),
        world.create_item("Decoder"),
        world.create_item("Big Shot"),
        world.create_item("Repeater"),
        world.create_item("Palette 02"),
        world.create_item("Palette 03"),
        world.create_item("Palette 04"),
        world.create_item("Palette 05"),
        world.create_item("Palette 06"),
        world.create_item("Palette 07"),
        world.create_item("Palette 08"),
        world.create_item("Palette 09"),
        world.create_item("Palette 10"),
        world.create_item("Palette 11"),
        world.create_item("Palette 12"),
        world.create_item("Palette 13"),
        world.create_item("Palette 14"),
        world.create_item("Palette 15"),
    ]
    for i in range(10):
        itempool.append(world.create_item(f"Health Upgrade"))
    for i in range(3):
        itempool.append(world.create_item(f"Water Level"))

    for i in range(3):
        itempool.append(world.create_item(f"Vent Level"))

    if world.options.gato_tech == 3 and not world.options.use_smallmech:
        # Lock it!
        lava_cooled = world.get_location("Cooler (Heater Core-0113)")
        lava_cooled.place_locked_item(world.create_item("Lava Cooled"))
    else:
        itempool.append(world.create_item("Lava Cooled"))

    # Lock the hot boys
    lava_cooled = world.get_location("Hotboy 1 (Heater Core-0019)")
    lava_cooled.place_locked_item(world.create_item("Hotboy defeated"))
    lava_cooled = world.get_location("Hotboy 2 (Heater Core-0313)")
    lava_cooled.place_locked_item(world.create_item("Hotboy defeated"))

    # Make the final item for rebba quest... not very useful :)
    #rebba_quest = world.get_location("Rebba quest 2 (Nexus-1716)")
    #rebba_quest.place_locked_item(world.create_item("Health Upgrade"))

    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    # Anyway. With our world's itempool finalized, we now need to submit it to the multiworld itempool.
    # This is how the generator actually knows about the existence of our items.
    world.multiworld.itempool += itempool

def generate_early(world: GatoRobotoWorld) -> None:


    # Early Starter items
    '''if world.options.unlock_all_warps:
        starter_pick = world.random.choice(["Rocket Start", "Spin Jump Start"])
    else:'''
    starter_pick = "Rocket Start"

    if starter_pick == "Rocket Start":
        if world.options.local_start:
            world.multiworld.local_early_items[world.player]["Rocket"] = 1
        else:
            world.multiworld.early_items[world.player]["Rocket"] = 1
    else:
        if world.options.local_start:
            world.multiworld.local_early_items[world.player]["Spin Jump"] = 1
            world.multiworld.local_early_items[world.player]["Dash"] = 1
        else:
            world.multiworld.early_items[world.player]["Spin Jump"] = 1
            world.multiworld.early_items[world.player]["Dash"] = 1

