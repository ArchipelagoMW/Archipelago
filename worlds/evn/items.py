from __future__ import annotations

from typing import TYPE_CHECKING, Dict, TypedDict

from flask_caching import logger

from BaseClasses import Item, ItemClassification
from . import rules

from .rezdata import ships

if TYPE_CHECKING:
    from .world import EVNWorld

GAME_NAME = "EV Nova"

STRING_COMPLETE_BIT = 9500

CREDIT_IDS = {
    "Credits1": 9900,
    "Credits5": 9901,
    "Credits10": 9902,
    "Credits50": 9903,
    "Credits100": 9904,
    "Credits500": 9905,
}

# # Every item must have a unique integer ID associated with it.
# # We will have a lookup from item name to ID here that, in world.py, we will import and bind to the world class.
# # Even if an item doesn't exist on specific options, it must be present in this lookup.
# ITEM_NAME_TO_ID = {
#     "Credits": 100,
#     "Starbridge": 130,
#     "Fed Patrol Boat": 142,
# }

# # Items should have a defined default classification.
# # In our case, we will make a dictionary from item name to classification.
# DEFAULT_ITEM_CLASSIFICATIONS = {
#     # "Key": ItemClassification.progression,
#     # "Sword": ItemClassification.progression | ItemClassification.useful,  # Items can have multiple classifications.
#     # "Shield": ItemClassification.progression,
#     # "Hammer": ItemClassification.progression,
#     # "Health Upgrade": ItemClassification.useful,
#     # "Confetti Cannon": ItemClassification.filler,
#     # "Math Trap": ItemClassification.trap,
#     "Credits": ItemClassification.filler,
#     "Fed Patrol Boat": ItemClassification.useful,
#     "Starbridge": ItemClassification.progression,
# }

type_offset: Dict[str, int] = {
    "Credits": 9900, # Special case! These won't actually be set - the client will check for these ids and make its own adjustment.
    "ship": 1550,   # 1550 - 1999 will be ships. We have 450 ships, so this should be safe.
}

# the int key will be our control bit used by the client to identify the item
ev_item_bank: Dict[int, EVNItem] = {}

item_name_to_id: Dict[str, int] = {}
#item_name_to_id: Dict[str, int] = {data.name: item_id for item_id, data in ev_item_bank.items()}

# Each Item instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Item class and override the "game" field.
class EVNItem(Item):
    #game = EVNWorld.game
    game = GAME_NAME
    #bid = int # bit ID value. The control bit ID the client will use to unlock the item.
    # game: str = "Generic"
    # __slots__ = ("name", "classification", "code", "player", "location")
    # name: str
    # classification: ItemClassification
    # code: Optional[int]
    # """an item with code None is called an Event, and does not get written to multidata"""
    # player: int
    # location: Optional[Location]


def create_item_bank(world: EVNWorld) -> None:
    # wild. For some reason this was updating ev_item_bank, but treating item_name_to_id as a local variable and not updating it, even though we declared it as global. So, explicity informing the function that both are globals.
    global ev_item_bank, item_name_to_id
    # Completion / Victory
    ev_item_bank[STRING_COMPLETE_BIT] = EVNItem(
        "Victory",
        ItemClassification.progression,
        STRING_COMPLETE_BIT,
        world.player,
    )

    # Credits
    # issues with fillers not being copies / new versions... can't reuse these.
    # for credit_name in CREDIT_IDS.keys():
    #     item_id = CREDIT_IDS[credit_name]
    #     ev_item_bank[item_id] = EVNItem(
    #         credit_name,
    #         ItemClassification.filler,
    #         item_id,
    #         world.player,
    #     )

    # ships
    # turns out, the ship names are not unique due to the various models. We could add the subname, but just cat ID.
    for ship in ships.ship_table.keys():
        temp_ship = ships.ship_table[ship]
        item_id = type_offset["ship"] + (int)(temp_ship["id"]) # Probably a safer way to test this? Fails if not int somehow probably.
        ev_item_bank[item_id] = EVNItem(
            temp_ship["name"].strip() + temp_ship["id"], # adding ID to name to ensure uniqueness. We could also add the subname if we wanted, but ID is probably safer.
            ItemClassification.progression,
            item_id,
            world.player,
        )
    
    # misn

    logger.info(f"data bank size: {len(ev_item_bank)}")

    item_name_to_id = {data.name: item_id for item_id, data in ev_item_bank.items()}  

# Ontop of our regular itempool, our world must be able to create arbitrary amounts of filler as requested by core.
# To do this, it must define a function called world.get_filler_item_name(), which we will define in world.py later.
# For now, let's make a function that returns the name of a random filler item here in items.py.
def get_random_filler_item_name(world: EVNWorld) -> str:
    # APQuest has an option called "trap_chance".
    # This is the percentage chance that each filler item is a Math Trap instead of a Confetti Cannon.
    # For this purpose, we need to use a random generator.

    # IMPORTANT: Whenever you need to use a random generator, you must use world.random.
    # This ensures that generating with the same generator seed twice yields the same output.
    # DO NOT use a bare random object from Python's built-in random module.
    # if world.random.randint(0, 99) < world.options.trap_chance:
    #     return "Math Trap"
    # return "Confetti Cannon"

    # TODO: rando between 9900 and 9905 for various amounts of credits.
    # Credits1 = 10k
    # Credits5 = 50k
    # Creadits10 = 100k
    # Credits50 = 500k
    # Credits100 = 1mil
    # Credits500 = 5mil # super rare, but can be used to make some really interesting item placements if it shows up early.
    #return "Credits"
    # return a weighted random selection
    return world.random.choices(
        #population=["Credits1", "Credits5", "Credits10", "Credits50", "Credits100", "Credits500"],
        population=sorted(CREDIT_IDS.keys(), key=lambda x: CREDIT_IDS[x]), # we're assuming they pop in order I suppose...
        weights=[0.1, 0.35, 0.25, 0.15, 0.1, 0.05], # 70% chance for Credits, 20% for Fed Patrol Boat, 10% for Starbridge
        k=1
    )[0]


def create_item_with_correct_classification(world: EVNWorld, name: str) -> EVNItem:
    # # Our world class must have a create_item() function that can create any of our items by name at any time.
    # # So, we make this helper function that creates the item by name with the correct classification.
    # # Note: This function's content could just be the contents of world.create_item in world.py directly,
    # # but it seemed nicer to have it in its own function over here in items.py.
    # classification = DEFAULT_ITEM_CLASSIFICATIONS[name]

    # # It is perfectly normal and valid for an item's classification to differ based on the player's options.
    # # In our case, Health Upgrades are only relevant to logic (and thus labeled as "progression") in hard mode.
    # # if name == "Health Upgrade" and world.options.hard_mode:
    # #     classification = ItemClassification.progression

    # return EVNItem(name, classification, ITEM_NAME_TO_ID[name], world.player)
    #if (itempool.)
    if name in CREDIT_IDS:
        item_id = CREDIT_IDS[name]
        return EVNItem(
            name,
            ItemClassification.filler,
            item_id,
            world.player,
        )

    # Instead of using a predefined lookup table like ITEM_NAME_TO_ID, we can also just look up the item in our ev_item_bank by name and return it.
    if (not ev_item_bank or ev_item_bank == {}):
        create_item_bank(world)
    # Surely there is a simpler way? This seems inefficient. 
    #return ev_item_bank[[item_id for item_id in ev_item_bank if ev_item_bank[item_id].name == name][0]]
    #return ev_item_bank[item_name_to_id[name]]
    item_id = item_name_to_id[name]
    return ev_item_bank[item_id]


# With those two helper functions defined, let's now get to actually creating and submitting our itempool.
def create_all_items(world: EVNWorld) -> None:
    # This is the function in which we will create all the items that this world submits to the multiworld item pool.
    # There must be exactly as many items as there are locations.
    # In our case, there are either six or seven locations.
    # We must make sure that when there are six locations, there are six items,
    # and when there are seven locations, there are seven items.

    # Creating items should generally be done via the world's create_item method.
    # First, we create a list containing all the items that always exist.

    # itempool: list[Item] = [
    #     world.create_item("Fed Patrol Boat"),
    #     world.create_item("Starbridge"),
    #     # world.create_item("Key"),
    #     # world.create_item("Sword"),
    #     # world.create_item("Shield"),
    #     # world.create_item("Health Upgrade"),
    #     # world.create_item("Health Upgrade"),
    # ]

    if (not ev_item_bank or ev_item_bank == {}):
        create_item_bank(world)

    # copy might be expensive, but need to because we'll add duplicates due to filler later
    #itempool = ev_item_bank.values().__copy__()
    #itempool = []
    # for item_id in ev_item_bank:
    #     if (item_id < 9900 or item_id >= 9906): # don't add credits to regular itempool, since they're just filler. We'll add them as needed in the filler section later.
    #         itempool.append(ev_item_bank[item_id])

    # TESTING: Just add a few to match with our testing locations for now, and then we can expand the itempool later.
    # itempool = [
    #     world.create_item("Fed Patrol Boat"),
    #     world.create_item("Starbridge"),
    #     world.create_item("Rebel Dragon"),
    #     world.create_item("Vell-os Javelin"),
    #     world.create_item("Unrelenting"),
    #     world.create_item("Abomination"),
    # ]

    # logger.info(f"items in ev_item_bank: {[ev_item_bank[item_id].name for item_id in ev_item_bank]}")
    # logger.info(f"item_name_to_id keys: {list(item_name_to_id.keys())}")
    # for item in item_name_to_id.keys():
    #     logger.info(f"item_name_to_id key: {item}, value: {item_name_to_id[item]}")

    itempool = [
        world.create_item("Fed Patrol Boat215"),
        world.create_item("Pirate Starbridge148"),
        world.create_item("Rebel Dragon180"),
        world.create_item("Vell-os Arrow382"),
        world.create_item("Unrelenting374"),
        world.create_item("Abomination384"),
    ]

    # Some items may only exist if the player enables certain options.
    # In our case, If the hammer option is enabled, the sixth item is the Hammer.
    # Otherwise, we add a filler Confetti Cannon.
    # if world.options.hammer:
    #     # Once again, it is important to stress that even though the Hammer doesn't always exist,
    #     # it must be present in the worlds item_name_to_id.
    #     # Whether it is actually in the itempool is determined purely by whether we create and add the item here.
    #     itempool.append(world.create_item("Hammer"))

    # Archipelago requires that each world submits as many locations as it submits items.
    # This is where we can use our filler and trap items.
    # APQuest has two of these: The Confetti Cannon and the Math Trap.
    # (Unfortunately, Archipelago is a bit ambiguous about its terminology here:
    #  "filler" is an ItemClassification separate from "trap", but in a lot of its functions,
    #  Archipelago will use "filler" to just mean "an additional item created to fill out the itempool".
    #  "Filler" in this sense can technically have any ItemClassification,
    #  but most commonly ItemClassification.filler or ItemClassification.trap.
    #  Starting here, the word "filler" will be used to collectively refer to APQuest's Confetti Cannon and Math Trap,
    #  which are ItemClassification.filler and ItemClassification.trap respectively.)
    # Creating filler items works the same as any other item. But there is a question:
    # How many filler items do we actually need to create?
    # In regions.py, we created either six or seven locations depending on the "extra_starting_chest" option.
    # In this function, we have created five or six items depending on whether the "hammer" option is enabled.
    # We *could* have a really complicated if-else tree checking the options again, but there is a better way.
    # We can compare the size of our itempool so far to the number of locations in our world.

    # The length of our itempool is easy to determine, since we have it as a list.
    number_of_items = len(itempool)
    logger.info(f"number of items before filler: {number_of_items}")
    #number_of_items = len(ev_item_bank)

    # The number of locations is also easy to determine, but we have to be careful.
    # Just calling len(world.get_locations()) would report an incorrect number, because of our *event locations*.
    # What we actually want is the number of *unfilled* locations. Luckily, there is a helper method for this:
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    logger.info(f"number of unfilled locations: {number_of_unfilled_locations}")

    # Now, we just subtract the number of items from the number of locations to get the number of empty item slots.
    #needed_number_of_filler_items = number_of_unfilled_locations - number_of_items
    # There's probably a more elegant way to do this, but we also need to subtract the number of completion locations, since those will be filled with event items instead of regular items.
    # basically, they aren't created *until* we start filling locations over in rules... so we have to account for them here.
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items - len(rules.COMPLETION_LOCATIONS) # also need to subtract the number of completion locations, since those will be filled with event items instead of regular items.
    logger.info(f"number of filler items needed: {needed_number_of_filler_items}")
    logger.info(f"number of completion locations: {len(rules.COMPLETION_LOCATIONS)}")

    # Finally, we create that many filler items and add them to the itempool.
    # To create our filler, we could just use world.create_item("Confetti Cannon").
    # But there is an alternative that works even better for most worlds, including APQuest.
    # As discussed above, our world must have a get_filler_item_name() function defined,
    # which must return the name of an infinitely repeatable filler item.
    # Defining this function enables the use of a helper function called world.create_filler().
    # You can just use this function directly to create as many filler items as you need to complete your itempool.
    if (needed_number_of_filler_items > 0):
        itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    # But... is that the right option for your game? Let's explore that.
    # For some games, the concepts of "regular itempool filler" and "additionally created filler" are different.
    # These games might want / require specific amounts of specific filler items in their regular pool.
    # To achieve this, they will have to intentionally create the correct quantities using world.create_item().
    # They may still use world.create_filler() to fill up the rest of their itempool with "repeatable filler",
    # after creating their "specific quantity" filler and still having room left over.

    # But there are many other games which *only* have infinitely repeatable filler items.
    # They don't care about specific amounts of specific filler items, instead only caring about the proportions.
    # In this case, world.create_filler() can just be used for the entire filler itempool.
    # APQuest is one of these games:
    # Regardless of whether it's filler for the regular itempool or additional filler for item links / etc.,
    # we always just want a Confetti Cannon or a Math Trap depending on the "trap_chance" option.
    # We defined this behavior in our get_random_filler_item_name() function, which in world.py,
    # we'll bind to world.get_filler_item_name(). So, we can just use world.create_filler() for all of our filler.

    # Anyway. With our world's itempool finalized, we now need to submit it to the multiworld itempool.
    # This is how the generator actually knows about the existence of our items.
    world.multiworld.itempool += itempool

    # Sometimes, you might want the player to start with certain items already in their inventory.
    # These items are called "precollected items".
    # They will be sent as soon as they connect for the first time (depending on your client's item handling flag).
    # Players can add precollected items themselves via the generic "start_inventory" option.
    # If you want to add your own precollected items, you can do so via world.push_precollected().
    # if world.options.start_with_one_confetti_cannon:
    #     # We're adding a filler item, but you can also add progression items to the player's precollected inventory.
    #     starting_confetti_cannon = world.create_item("Confetti Cannon")
    #     world.push_precollected(starting_confetti_cannon)
