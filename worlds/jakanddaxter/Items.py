import typing
from BaseClasses import Item

class JakAndDaxterItem(Item):
    game: str = "Jak and Daxter: The Precursor Legacy"

# Items Found Multiple Times
generic_item_table = {
    "Power Cell": 1000,
    "Scout Fly": 2000,
    "Precursor Orb": 3000
}

# Items Only Found Once
special_item_table = {
    "Fisherman's Boat": 0,
    "Sculptor's Muse": 1,
    "Flut Flut": 2,
    "Blue Eco Switch": 3,
    "Gladiator's Pontoons": 4,
    "Yellow Eco Switch": 5
}

# All Items
item_table = {**generic_item_table, **special_item_table}
