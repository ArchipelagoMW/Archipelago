from BaseClasses import Item
from .GameID import game_id, game_name


class JakAndDaxterItem(Item):
    game: str = game_name


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
    2219: "Lurker Fort Gate",
    2220: "Free The Yellow Sage",
    2221: "Free The Red Sage",
    2222: "Free The Blue Sage",
    2223: "Free The Green Sage"
}

# All Items
item_table = {**generic_item_table, **special_item_table}
