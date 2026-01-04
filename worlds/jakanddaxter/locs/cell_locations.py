from ..game_id import jak1_id

# Power Cells are given ID's between 0 and 116 by the game.

# The game tracks all game-tasks as integers.
# 101 of these ID's correspond directly to power cells, but they are not
# necessarily ordered, nor are they the first 101 in the task list.
# The remaining ones are cutscenes and other events.


# These helper functions do all the math required to get information about each
# power cell and translate its ID between AP and OpenGOAL.
def to_ap_id(game_id: int) -> int:
    if game_id >= jak1_id:
        raise ValueError(f"Attempted to convert {game_id} to an AP ID, but it already is one.")
    return jak1_id + game_id


def to_game_id(ap_id: int) -> int:
    if ap_id < jak1_id:
        raise ValueError(f"Attempted to convert {ap_id} to a Jak 1 ID, but it already is one.")
    return ap_id - jak1_id


# The ID's you see below correspond directly to that cell's game-task ID.

# The "Free 7 Scout Flies" Power Cells will be unlocked separately from their respective levels.
loc7SF_cellTable = {
    95: "GR: Free 7 Scout Flies",
    75: "SV: Free 7 Scout Flies",
    7:  "FJ: Free 7 Scout Flies",
    20: "SB: Free 7 Scout Flies",
    28: "MI: Free 7 Scout Flies",
    68: "FC: Free 7 Scout Flies",
    76: "RV: Free 7 Scout Flies",
    57: "PB: Free 7 Scout Flies",
    49: "LPC: Free 7 Scout Flies",
    43: "BS: Free 7 Scout Flies",
    88: "MP: Free 7 Scout Flies",
    77: "VC: Free 7 Scout Flies",
    85: "SC: Free 7 Scout Flies",
    65: "SM: Free 7 Scout Flies",
    90: "LT: Free 7 Scout Flies",
    91: "GMC: Free 7 Scout Flies",
}

# Geyser Rock
locGR_cellTable = {
    92: "GR: Find The Cell On The Path",
    93: "GR: Open The Precursor Door",
    94: "GR: Climb Up The Cliff",
}

# Sandover Village
locSV_cellTable = {
    11: "SV: Bring 90 Orbs To The Mayor",
    12: "SV: Bring 90 Orbs to Your Uncle",
    10: "SV: Herd The Yakows Into The Pen",
    13: "SV: Bring 120 Orbs To The Oracle (1)",
    14: "SV: Bring 120 Orbs To The Oracle (2)",
}

# Forbidden Jungle
locFJ_cellTable = {
    3: "FJ: Connect The Eco Beams",
    4: "FJ: Get To The Top Of The Temple",
    2: "FJ: Find The Blue Vent Switch",
    6: "FJ: Defeat The Dark Eco Plant",
    5: "FJ: Catch 200 Pounds Of Fish",
    8: "FJ: Follow The Canyon To The Sea",
    9: "FJ: Open The Locked Temple Door",
}

# Sentinel Beach
locSB_cellTable = {
    15: "SB: Unblock The Eco Harvesters",
    17: "SB: Push The Flut Flut Egg Off The Cliff",
    16: "SB: Get The Power Cell From The Pelican",
    18: "SB: Chase The Seagulls",
    19: "SB: Launch Up To The Cannon Tower",
    21: "SB: Explore The Beach",
    22: "SB: Climb The Sentinel",
}

# Misty Island
locMI_cellTable = {
    23: "MI: Catch The Sculptor's Muse",
    24: "MI: Climb The Lurker Ship",
    26: "MI: Stop The Cannon",
    25: "MI: Return To The Dark Eco Pool",
    27: "MI: Destroy the Balloon Lurkers",
    29: "MI: Use Zoomer To Reach Power Cell",
    30: "MI: Use Blue Eco To Reach Power Cell",
}

# Fire Canyon
locFC_cellTable = {
    69: "FC: Reach The End Of Fire Canyon",
}

# Rock Village
locRV_cellTable = {
    31: "RV: Bring 90 Orbs To The Gambler",
    32: "RV: Bring 90 Orbs To The Geologist",
    33: "RV: Bring 90 Orbs To The Warrior",
    34: "RV: Bring 120 Orbs To The Oracle (1)",
    35: "RV: Bring 120 Orbs To The Oracle (2)",
}

# Precursor Basin
locPB_cellTable = {
    54: "PB: Herd The Moles Into Their Hole",
    53: "PB: Catch The Flying Lurkers",
    52: "PB: Beat Record Time On The Gorge",
    56: "PB: Get The Power Cell Over The Lake",
    55: "PB: Cure Dark Eco Infected Plants",
    58: "PB: Navigate The Purple Precursor Rings",
    59: "PB: Navigate The Blue Precursor Rings",
}

# Lost Precursor City
locLPC_cellTable = {
    47: "LPC: Raise The Chamber",
    45: "LPC: Follow The Colored Pipes",
    46: "LPC: Reach The Bottom Of The City",
    48: "LPC: Quickly Cross The Dangerous Pool",
    44: "LPC: Match The Platform Colors",
    50: "LPC: Climb The Slide Tube",
    51: "LPC: Reach The Center Of The Complex",
}

# Boggy Swamp
locBS_cellTable = {
    37: "BS: Ride The Flut Flut",
    36: "BS: Protect Farthy's Snacks",
    38: "BS: Defeat The Lurker Ambush",
    39: "BS: Break The Tethers To The Zeppelin (1)",
    40: "BS: Break The Tethers To The Zeppelin (2)",
    41: "BS: Break The Tethers To The Zeppelin (3)",
    42: "BS: Break The Tethers To The Zeppelin (4)",
}

# Mountain Pass
locMP_cellTable = {
    86: "MP: Defeat Klaww",
    87: "MP: Reach The End Of The Mountain Pass",
    110: "MP: Find The Hidden Power Cell",
}

# Volcanic Crater
locVC_cellTable = {
    96: "VC: Bring 90 Orbs To The Miners (1)",
    97: "VC: Bring 90 Orbs To The Miners (2)",
    98: "VC: Bring 90 Orbs To The Miners (3)",
    99: "VC: Bring 90 Orbs To The Miners (4)",
    100: "VC: Bring 120 Orbs To The Oracle (1)",
    101: "VC: Bring 120 Orbs To The Oracle (2)",
    74: "VC: Find The Hidden Power Cell",
}

# Spider Cave
locSC_cellTable = {
    78: "SC: Use Your Goggles To Shoot The Gnawing Lurkers",
    79: "SC: Destroy The Dark Eco Crystals",
    80: "SC: Explore The Dark Cave",
    81: "SC: Climb The Giant Robot",
    82: "SC: Launch To The Poles",
    83: "SC: Navigate The Spider Tunnel",
    84: "SC: Climb the Precursor Platforms",
}

# Snowy Mountain
locSM_cellTable = {
    60: "SM: Find The Yellow Vent Switch",
    61: "SM: Stop The 3 Lurker Glacier Troops",
    66: "SM: Deactivate The Precursor Blockers",
    67: "SM: Open The Frozen Crate",
    63: "SM: Open The Lurker Fort Gate",
    62: "SM: Get Through The Lurker Fort",
    64: "SM: Survive The Lurker Infested Cave",
}

# Lava Tube
locLT_cellTable = {
    89: "LT: Cross The Lava Tube",
}

# Gol and Maias Citadel
locGMC_cellTable = {
    71: "GMC: Free The Blue Sage",
    72: "GMC: Free The Red Sage",
    73: "GMC: Free The Yellow Sage",
    70: "GMC: Free The Green Sage",
}
