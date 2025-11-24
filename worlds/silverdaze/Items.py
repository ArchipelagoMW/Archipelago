from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import SDWorld
#Sawyer: This time I said screwit and went with the old system we already had, hopefully it works.
#Sawyer: The APQuest version looked mean and scary but we can do it if we must.

class SDItem(Item):
    game: str = "Silver Daze"


class ItemData(NamedTuple):
    code: int
    classification: ItemClassification = ItemClassification.filler
    category: str = 'Card'
    max_quantity: int = 1
    weight: int = 1


# Item groups for easy management

party_members = {
    "Pinn": ItemData(3001, ItemClassification.progression, "Party"),
    "Geo": ItemData(3002, ItemClassification.progression, "Party"),
    "Kani": ItemData(3003, ItemClassification.progression, "Party"),
}

mp3s = {
    "Freddie Freeloader": ItemData(1063, ItemClassification.useful, "MP3"),
    "Flossophy": ItemData(1044, ItemClassification.useful, "MP3"),
    "Big Shot": ItemData(1003, ItemClassification.useful, "MP3"),
    "Triage": ItemData(1065, ItemClassification.useful, "MP3"),
    "The Sign": ItemData(1045, ItemClassification.useful, "MP3"),
    "Wet Hands": ItemData(1010, ItemClassification.useful, "MP3"),
    "Move": ItemData(1001, ItemClassification.useful, "MP3"),
    "Low Ride": ItemData(1042, ItemClassification.useful, "MP3"),
    "Lost In Thought": ItemData(1062, ItemClassification.useful, "MP3"),
}

# In Visual Studio Code or another IDE you can collapse the dict to hide the cards
cards = {
    "Ultima": ItemData(352),
    "Finish Touch": ItemData(42),
    "Valor Drive": ItemData(25),
    "Sonic Boom": ItemData(29),
    "Hopscotch": ItemData(154),
    "CoffeBrek": ItemData(155),
    "Fine Tune": ItemData(256),
    "SmokeBreak": ItemData(311),
    "PowerNap": ItemData(72),
    "Flatten": ItemData(18),
    "Dragon": ItemData(31),
    "Variacut": ItemData(30),
    "Morning Ray": ItemData(7),
    "Zoner": ItemData(304),
    "Cold As Ice": ItemData(5),
    "Strife": ItemData(6),
    "RATD": ItemData(4, ItemClassification.useful, "Card", 2),
}

keys = {
    "Yellow Key": ItemData(2010, ItemClassification.progression, "Key"),
    "Red Key": ItemData(2014, ItemClassification.progression, "Key"),
}

consumables = {
    "Heal Token": ItemData(2002, ItemClassification.filler, "Filler", 5),
    "Evade Token": ItemData(2003, ItemClassification.filler, "Filler", 1),
    "Hi-Heal Token": ItemData(2004, ItemClassification.filler, "Filler", 1),
    # Tent Token Here
    "Sneak Token": ItemData(2006, ItemClassification.filler, "Filler", 1),
}

#Sawyer: This should give us some random fillers. Let's look into adding traps later.
def get_random_filler_item_name(world: SDWorld) -> str:
    fillers = ["Evade Token", "Sneak Token"]
    randomResult = world.random.randomint(0, len(fillers))
    return fillers[randomResult]



item_table = {
    # This includes all entries in those other dicts in this one
    **party_members,
    **cards,
    **mp3s,
    **keys,
    **consumables,

    # Events - Note that these are items!

    # Other Items
    #  "Sneak Token":          ItemData(2006,       ItemClassification.filler, "Filler",   1),
}


def create_item(self, name: str) -> Item:
    item_data = item_table[name]
    item = SDItem(name, item_data.classification, item_data.code, self.player)
    return item

def create_items(world: SDWorld):
    itempool = []

    for name, max_quantity in item_table:
        itempool += [name] * max_quantity

    # Starting Party Member given at game start
    starter_member = "Pinn"
    if (Options.StartingPartyMember == "option_geo"):
        starter_member = "Geo"
    if (Options.StartingPartyMember == "option_kani"):
        starter_member = "Kani"
    if (Options.StartingPartyMember == "option_random"):

        # TODO:
        # Sawyer: Make sure this has all party members in the final game.
        member = world.random.randint(1, 3)
        if (member == 1):
            starter_member = "Pinn"
        elif (member == 2):
            starter_member = "Geo"
        elif (member == 3):
            starter_member = "Kani"

    itempool.remove(starter_member)
    world.multiworld.push_precollected(world.create_item(starter_member))

    # other steps here maybe

    # Create Items
    itempool = [item for item in map(lambda name: world.create_item(name), itempool)]
    # Fill remaining items with randomly generated junk
    while len(itempool) < len(world.multiworld.get_unfilled_locations(world.player)):
        itempool.append(world.get_random_filler_item_name())

    world.multiworld.itempool += itempool