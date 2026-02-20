from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, TypedDict

from flask_caching import logger

from BaseClasses import Item, ItemClassification
from . import rules

from .rezdata import ships, outfits
from .logics import ships_to_ignore, outf_to_ignore

from .apdata.offsets import offsets_table as type_offset

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

# maxes are noted but not yet enforced or in the data
# type_offset: Dict[str, int] = {
#     "Credits": 9900, # Special case! These won't actually be set - the client will check for these ids and make its own adjustment.
#     "ship": 1550,   # 1550 - 1999 will be ships. We have 288/450 ships, so this should be safe.
#     "outf": 3100,   # 3100 - 3500 for outfs. We have 242/400 outf, should be good
# }
# ADJUSTED FOR THE 128 OFFSET START ID OF EACH TYPE
# starting_id = 128
# type_offset: Dict[str, int] = {
#     "Credits": 9900, # Special case! These won't actually be set - the client will check for these ids and make its own adjustment.
#     "ship": 1550 - starting_id,   # 1550 - 1999 will be ships. We have 288/450 ships, so this should be safe.
#     "outf": 3100 - starting_id,   # 3100 - 3500 for outfs. We have 242/400 outf, should be good
# }

# I am bothered by having to do this, or at least using this solution.
# specific_exclusions: List[int] = [
#     895 + type_offset["ship"], #escape pod
# ]

#EVNItemData = TypedDict("EVNItemData", {"name": str, "classification": ItemClassification, "code": int})
class EVNItemData(TypedDict, total=False): 
    name: str
    classification: ItemClassification
    code: int
    origin: str | None

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


def get_items() -> Dict[int, EVNItemData]:
    ret_bank: Dict[int, EVNItemData] = {}

    ret_bank[STRING_COMPLETE_BIT] = EVNItemData(
        name="Victory",
        classification=ItemClassification.progression,
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
    # turns out, the ship names are not unique due to the various models. We could add the subname, but just cat ID.
    #i = 0
    for ship in ships.ship_table.keys():
        if ship in ships_to_ignore:
            continue
        temp_ship = ships.ship_table[ship]
        item_id = type_offset["ship"] + (int)(temp_ship["id"]) # Probably a safer way to test this? Fails if not int somehow probably.
        # if item_id in specific_exclusions:
        #     continue
        #item_id = type_offset["ship"] + i # IDs started at 128 and were not guaranteed to be contiguous
        ret_bank[item_id] = EVNItemData(
            name=temp_ship["name"].strip() + temp_ship["id"], # adding ID to name to ensure uniqueness. We could also add the subname if we wanted, but ID is probably safer.
            classification=ItemClassification.progression,
            code=item_id,
            origin="ship"
        )
        #i += 1

    # outf
    #j = 0
    for outf in outfits.outf_table.keys():
        if outf in outf_to_ignore:
            continue
        temp_outf = outfits.outf_table[outf]
        item_id = type_offset["outf"] + (int)(temp_outf["id"]) # Probably a safer way to test this? Fails if not int somehow probably.
        # if item_id in specific_exclusions:
        #     continue
        #item_id = type_offset["outf"] + j
        ret_bank[item_id] = EVNItemData(
            name=temp_outf["name"].strip() + temp_outf["id"], # adding ID to name to ensure uniqueness. We could also add the subname if we wanted, but ID is probably safer.
            classification=ItemClassification.progression | ItemClassification.useful, # or useful?
            code=item_id,
            origin="outf"
        )
        #j += 1

    logger.info(f"data bank size: {len(ret_bank)}")
    return ret_bank


#ev_item_bank: Dict[int, EVNItemData] = get_items()
ev_item_bank = get_items()

def get_item_ids() -> Dict[str, int]:
    # helper function to get the item name to ID mapping from our ev_item_bank. We have to do it this way since the ev_item_bank is generated dynamically from the game's data files, so we can't just hardcode an item_name_to_id mapping like in APQuest.
    global ev_item_bank

    #return {data.name: item_id for item_id, data in ev_item_bank.items()}
    return {data["name"]: item_id for item_id, data in ev_item_bank.items()} #because it is now a dict, not a full regular class...


#item_name_to_id: Dict[str, int] = get_item_ids()
item_name_to_id = get_item_ids()

# Ontop of our regular itempool, our world must be able to create arbitrary amounts of filler as requested by core.
# To do this, it must define a function called world.get_filler_item_name(), which we will define in world.py later.
# For now, let's make a function that returns the name of a random filler item here in items.py.
def get_random_filler_item_name(world: EVNWorld) -> str:
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
        if ((item_id < 9900 or item_id >= 9906) and item_id != STRING_COMPLETE_BIT): # don't add credits to regular itempool, since they're just filler. We'll add them as needed in the filler section later.
            if (not world.options.include_outfits and ev_item_bank[item_id]["origin"] == "outf"):
                continue
            itempool.append(create_item_with_correct_classification(world, ev_item_bank[item_id]["name"]))

    
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
    #needed_number_of_filler_items = number_of_unfilled_locations - number_of_items - len(rules.COMPLETION_LOCATIONS) # also need to subtract the number of completion locations, since those will be filled with event items instead of regular items.
    # NOTE: removing 1 for the single completion location we have now that options forces story string choice.
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items - 1
    logger.info(f"number of filler items needed: {needed_number_of_filler_items}")
    #logger.info(f"number of completion locations: {len(rules.COMPLETION_LOCATIONS)}")

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

