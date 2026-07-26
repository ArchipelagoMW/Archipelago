from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, TypedDict

# TODO: Fix this reference. Wtf is flask_caching? It doesn't work with AP Launcher.
# from flask_caching import logger

from BaseClasses import Item, ItemClassification

from .rezdata import ships, outfits
from .logics import ships_to_ignore, outf_to_ignore

from .apdata.offsets import offsets_table as type_offset

if TYPE_CHECKING:
    from .world import EVNWorld

GAME_NAME = "EV Nova"

STRING_COMPLETE_BIT = 9500

# Every item must have a unique integer ID associated with it.
# maxes are noted but not yet enforced or in the data

# Custom items. The client has been adjusted to listen for these as well.
# These are not interactable like customoutf.py
CREDIT_IDS = {
    "Credits1": 9900,
    "Credits5": 9901,
    "Credits10": 9902,
    "Credits50": 9903,
    "Credits100": 9904,
    "Credits500": 9905,
}

class EVNItemData(TypedDict, total=False): 
    name: str
    classification: ItemClassification
    code: int
    origin: str | None

# Each Item instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Item class and override the "game" field.
class EVNItem(Item):
    game = GAME_NAME


def get_items() -> Dict[int, EVNItemData]:
    ret_bank: Dict[int, EVNItemData] = {}

    ret_bank[STRING_COMPLETE_BIT] = EVNItemData(
        name="Victory",
        classification=ItemClassification.progression,  # Odd, changing this to "skip_balancing" made the server think the game was unbeatable.
        code=STRING_COMPLETE_BIT,
    )

    # Wait, we do need the credits... d'oh
    for credAmount in CREDIT_IDS.keys():
        ret_bank[CREDIT_IDS[credAmount]] = EVNItemData(
            name=credAmount,
            classification=ItemClassification.filler,
            code=CREDIT_IDS[credAmount],
        )

    # ships
    # turns out, the ship names are not unique due to the various models, so we concat ID.
    for ship in ships.ship_table.keys():
        # In logics, we define ship ids we don't want in game.
        # Check for, and skip, as necessary.
        if ship in ships_to_ignore:
            continue
        temp_ship = ships.ship_table[ship]
        item_id = type_offset["ship"] + (int)(temp_ship["id"]) # Probably a safer way to test this? Fails if not int somehow probably.
        ret_bank[item_id] = EVNItemData(
            # NOTE: WARNING - If we change these names, make sure to change them in rules.py as well!!!
            name=temp_ship["name"].strip() + temp_ship["id"], # adding ID to name to ensure uniqueness. We could also add the subname if we wanted, but ID is probably safer.
            classification=ItemClassification.progression,
            code=item_id,
            origin="ship"
        )

    # outf
    for outf in outfits.outf_table.keys():
        if outf in outf_to_ignore:
            continue
        temp_outf = outfits.outf_table[outf]
        item_id = type_offset["outf"] + (int)(temp_outf["id"]) # Probably a safer way to test this? Fails if not int somehow probably.
        ret_bank[item_id] = EVNItemData(
            name=temp_outf["name"].strip() + temp_outf["id"], # adding ID to name to ensure uniqueness. We could also add the subname if we wanted, but ID is probably safer.
            classification=ItemClassification.progression | ItemClassification.useful, # or useful?
            code=item_id,
            origin="outf"
        )

    #logger.info(f"data bank size: {len(ret_bank)}")
    return ret_bank


ev_item_bank = get_items()


def get_item_ids() -> Dict[str, int]:
    # helper function to get the item name to ID mapping from our ev_item_bank. We have to do it this way since the ev_item_bank is generated dynamically from the game's data files, so we can't just hardcode an item_name_to_id mapping like in APQuest.
    global ev_item_bank

    return {data["name"]: item_id for item_id, data in ev_item_bank.items()} #because it is now a dict, not a full regular class...


item_name_to_id = get_item_ids()

# Ontop of our regular itempool, our world must be able to create arbitrary amounts of filler as requested by core.
# To do this, it must define a function called world.get_filler_item_name(), which we will define in world.py later.
# For now, let's make a function that returns the name of a random filler item here in items.py.
def get_random_filler_item_name(world: EVNWorld) -> str:
    # Credits1 = 10k
    # Credits5 = 50k
    # Creadits10 = 100k
    # Credits50 = 500k
    # Credits100 = 1mil
    # Credits500 = 5mil # super rare, but can be used to make some really interesting item placements if it shows up early.
    
    # return a weighted random selection. Thanks doom2.
    return world.random.choices(
        population=sorted(CREDIT_IDS.keys(), key=lambda x: CREDIT_IDS[x]), # we're assuming they pop in order I suppose...
        weights=[0.1, 0.35, 0.25, 0.15, 0.1, 0.05], 
        k=1
    )[0]


def create_item_with_correct_classification(world: EVNWorld, name: str) -> EVNItem:
    """
    Helper method to return items. For custom items, defines ItemClassification. Otherwise, returns item's defined classification.
    Returns EVNItem object.
    """
    if name in CREDIT_IDS:
        item_id = CREDIT_IDS[name]
        return EVNItem(
            name,
            ItemClassification.filler,
            item_id,
            world.player,
        )

    item_id = item_name_to_id[name]
    partial_item_data = ev_item_bank[item_id]
    return EVNItem(
        partial_item_data["name"],
        partial_item_data["classification"],
        partial_item_data["code"],
        world.player,
    )


# With those two helper functions defined, let's now get to actually creating and submitting our itempool.
def create_all_items(world: EVNWorld) -> None:
    itempool = []
    for item_id in ev_item_bank: #NOTE: could probably now change to "if item.origin not blank, append"
        # don't add credits to regular itempool, since they're just filler. We'll add them as needed in the filler section later.
        if ((item_id < 9900 or item_id >= 9906) and item_id != STRING_COMPLETE_BIT): 
            # If shuffling outfits was not selected in options, skip outfit items.
            if (not world.options.include_outfits and ev_item_bank[item_id]["origin"] == "outf"):
                continue
            # Add the item to the pool.
            itempool.append(create_item_with_correct_classification(world, ev_item_bank[item_id]["name"]))

    # The length of our itempool is easy to determine, since we have it as a list.
    number_of_items = len(itempool)
    #logger.info(f"number of items before filler: {number_of_items}")

    # The number of locations is also easy to determine, but we have to be careful.
    # Just calling len(world.get_locations()) would report an incorrect number, because of our *event locations*.
    # What we actually want is the number of *unfilled* locations. Luckily, there is a helper method for this:
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    #logger.info(f"number of unfilled locations: {number_of_unfilled_locations}")

    # Now, we just subtract the number of items from the number of locations to get the number of empty item slots.
    # There's probably a more elegant way to do this, but we also need to subtract the number of completion locations, since those will be filled with event items instead of regular items.
    # basically, they aren't created *until* we start filling locations over in rules... so we have to account for them here.
    # NOTE: removing 1 for the single completion location we have now that options.py forces story string choice.
    #   AKA, the final location completes the game, so isn't a valid check (in this case). It is filled by an event we use
    #   for detecting said completion. Thus, -1 to the overall count.
    #   This will show up oddly in the generator (#items, #unfilled locations, #dif - but #dif offset by 1)
    # NOTE: EVN has so many items, this'll only really come into effect if the outfits aren't also shuffled.
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items - 1
    #logger.info(f"number of filler items needed: {needed_number_of_filler_items}")

    # Finally, we create that many filler items and add them to the itempool.
    # To create our filler, we could just use world.create_item("Confetti Cannon").
    # But there is an alternative that works even better for most worlds, including APQuest.
    # As discussed above, our world must have a get_filler_item_name() function defined,
    # which must return the name of an infinitely repeatable filler item.
    # Defining this function enables the use of a helper function called world.create_filler().
    # You can just use this function directly to create as many filler items as you need to complete your itempool.
    if (needed_number_of_filler_items > 0):
        itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool

