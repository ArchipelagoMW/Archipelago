from BaseClasses import Item
from .GameID import jak1_name, jak1_max
from .locs import (OrbLocations as Orbs,
                   CellLocations as Cells,
                   ScoutLocations as Scouts,
                   SpecialLocations as Specials,
                   OrbCacheLocations as Caches)


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

# Orbs are also generic and interchangeable.
# These items are only used by Orbsanity, and only one of these
# items will be used corresponding to the chosen bundle size.
orb_item_table = {
    1: "Precursor Orb",
    2: "Bundle of 2 Precursor Orbs",
    4: "Bundle of 4 Precursor Orbs",
    5: "Bundle of 5 Precursor Orbs",
    8: "Bundle of 8 Precursor Orbs",
    10: "Bundle of 10 Precursor Orbs",
    16: "Bundle of 16 Precursor Orbs",
    20: "Bundle of 20 Precursor Orbs",
    25: "Bundle of 25 Precursor Orbs",
    40: "Bundle of 40 Precursor Orbs",
    50: "Bundle of 50 Precursor Orbs",
    80: "Bundle of 80 Precursor Orbs",
    100: "Bundle of 100 Precursor Orbs",
    125: "Bundle of 125 Precursor Orbs",
    200: "Bundle of 200 Precursor Orbs",
    250: "Bundle of 250 Precursor Orbs",
    400: "Bundle of 400 Precursor Orbs",
    500: "Bundle of 500 Precursor Orbs",
    1000: "Bundle of 1000 Precursor Orbs",
    2000: "Bundle of 2000 Precursor Orbs",
}

# These are special items representing unique unlocks in the world. Notice that their Item ID equals their
# respective Location ID. Like scout flies, this is necessary for game<->archipelago communication.
# TODO - These numbers of checks may be inaccurate post-region refactor.
special_item_table = {
    5: "Fisherman's Boat",              # Unlocks 14 checks in Misty Island
    4: "Jungle Elevator",               # Unlocks 2 checks in Forbidden Jungle
    2: "Blue Eco Switch",               # Unlocks 1 check in Jungle and 1 in Beach
    17: "Flut Flut",                    # Unlocks 2 checks in Swamp and 2 in Snowy
    33: "Warrior's Pontoons",           # Unlocks 14 checks in Swamp and everything post-Rock Village
    105: "Snowy Mountain Gondola",      # Unlocks 15 checks in Snowy Mountain
    60: "Yellow Eco Switch",            # Unlocks 1 check in Pass and 1 in Snowy
    63: "Snowy Fort Gate",              # Unlocks 3 checks in Snowy Mountain
    71: "Freed The Blue Sage",          # 1 of 3 unlocks for the final staircase and 2 checks in Citadel
    72: "Freed The Red Sage",           # 1 of 3 unlocks for the final staircase and 2 checks in Citadel
    73: "Freed The Yellow Sage",        # 1 of 3 unlocks for the final staircase and 2 checks in Citadel
    70: "Freed The Green Sage",         # Unlocks the final elevator
}

# These are the move items for move randomizer. Notice that their Item ID equals some of the Orb Cache Location ID's.
# This was 100% arbitrary. There's no reason to tie moves to orb caches except that I need a place to put them. ;_;
move_item_table = {
    10344: "Crouch",
    10369: "Crouch Jump",
    11072: "Crouch Uppercut",
    12634: "Roll",
    12635: "Roll Jump",
    10945: "Double Jump",
    14507: "Jump Dive",
    14838: "Jump Kick",
    23348: "Punch",
    23349: "Punch Uppercut",
    23350: "Kick",
    # 24038: "Orb Cache at End of Blast Furnace",  # TODO - IDK, we didn't need all of the orb caches for move rando.
    # 24039: "Orb Cache at End of Launch Pad Room",
    # 24040: "Orb Cache at Start of Launch Pad Room",
}

# All Items
# While we're here, do all the ID conversions needed.
item_table = {
    **{Cells.to_ap_id(k): cell_item_table[k] for k in cell_item_table},
    **{Scouts.to_ap_id(k): scout_item_table[k] for k in scout_item_table},
    **{Specials.to_ap_id(k): special_item_table[k] for k in special_item_table},
    **{Caches.to_ap_id(k): move_item_table[k] for k in move_item_table},
    **{Orbs.to_ap_id(k): orb_item_table[k] for k in orb_item_table},
    jak1_max: "Green Eco Pill"  # Filler item.
}
