import typing
from BaseClasses import Item


class JakAndDaxterItem(Item):
    game: str = "Jak and Daxter: The Precursor Legacy"


# Items Found Multiple Times
generic_item_table = {
    0: "Power Cell",
    101: "Scout Fly",
    213: "Precursor Orb"
}

# Items Only Found Once
special_item_table = {
    2213: "Fisherman's Boat",
    # 2214: "Sculptor's Muse", # Unused?
    2215: "Flut Flut",
    2216: "Blue Eco Switch",
    2217: "Gladiator's Pontoons",
    2218: "Yellow Eco Switch",
    2219: "Lurker Fort Gate"
}

# All Items
item_table = {**generic_item_table, **special_item_table}
