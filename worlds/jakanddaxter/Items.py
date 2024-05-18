from BaseClasses import Item
from .GameID import jak1_name
from .locs import CellLocations as Cells, ScoutLocations as Scouts, SpecialLocations as Specials


class JakAndDaxterItem(Item):
    game: str = jak1_name


# Power Cells are generic, fungible, interchangeable items. Every cell is indistinguishable from every other.
cell_item_table = {
    0:  "Power Cell",
}

# Scout flies are interchangeable within their respective sets of 7. Notice the abbreviated level name after each item.
# Also, notice that their Item ID equals their respective Power Cell's Location ID. This is necessary for
# game<->archipelago communication.
scout_item_table = {
    95: "Scout Fly - GR",
    75: "Scout Fly - SV",
    7:  "Scout Fly - FJ",
    20: "Scout Fly - SB",
    28: "Scout Fly - MI",
    68: "Scout Fly - FC",
    76: "Scout Fly - RV",
    57: "Scout Fly - PB",
    49: "Scout Fly - LPC",
    43: "Scout Fly - BS",
    88: "Scout Fly - MP",
    77: "Scout Fly - VC",
    85: "Scout Fly - SC",
    65: "Scout Fly - SM",
    90: "Scout Fly - LT",
    91: "Scout Fly - GMC",
}

# TODO - Orbs are also generic and interchangeable.
# orb_item_table = {
#     ???: "Precursor Orb",
# }

# These are special items representing unique unlocks in the world. Notice that their Item ID equals their
# respective Location ID. Like scout flies, this is necessary for game<->archipelago communication.
special_item_table = {
    5: "Fisherman's Boat",
    4: "Jungle Elevator",
    2: "Blue Eco Switch",
    17: "Flut Flut",
    60: "Yellow Eco Switch",
    63: "Snowy Fort Gate",
    71: "Freed The Blue Sage",
    72: "Freed The Red Sage",
    73: "Freed The Yellow Sage",
    70: "Freed The Green Sage",
}

# All Items
# While we're here, do all the ID conversions needed.
item_table = {
    **{Cells.to_ap_id(k): cell_item_table[k] for k in cell_item_table},
    **{Scouts.to_ap_id(k): scout_item_table[k] for k in scout_item_table},
    # **{Orbs.to_ap_id(k): orb_item_table[k] for k in orb_item_table},
    **{Specials.to_ap_id(k): special_item_table[k] for k in special_item_table},
}
