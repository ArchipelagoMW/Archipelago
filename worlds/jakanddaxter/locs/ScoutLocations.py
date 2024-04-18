# Scout Flies are given ID's between 0 and 393311 by the game, explanation below.

# Each fly is given a unique 32-bit number broken into two 16-bit numbers.
# The lower 16 bits are the game-task ID of the power cell the fly corresponds to.
# The higher 16 bits are the index of the fly itself, from 000 (0) to 110 (6).

# Ex: The final scout fly on Geyser Rock
# 0000000000000110 0000000001011111
# (   Index: 6   ) (   Cell: 95   )

# Because flies are indexed from 0, each 0th fly's full ID == the power cell's ID.
# So we need to offset all of their ID's in order for Archipelago to separate them
# from their power cells. We use 128 (2^7) for this purpose, because scout flies
# never use the 8th lowest bit to describe themselves.

# TODO - The ID's you see below correspond directly to that fly's 32-bit ID in the game.

# Geyser Rock
locGR_scoutTable = {
    101: "GR: Scout Fly On Ground, Front",
    102: "GR: Scout Fly On Ground, Back",
    103: "GR: Scout Fly On Left Ledge",
    104: "GR: Scout Fly On Right Ledge",
    105: "GR: Scout Fly On Middle Ledge, Left",
    106: "GR: Scout Fly On Middle Ledge, Right",
    107: "GR: Scout Fly On Top Ledge"
}

# Sandover Village
locSV_scoutTable = {
    108: "SV: Scout Fly In Fisherman's House",
    109: "SV: Scout Fly In Mayor's House",
    110: "SV: Scout Fly Under Bridge",
    111: "SV: Scout Fly Behind Sculptor's House",
    112: "SV: Scout Fly Overlooking Farmer's House",
    113: "SV: Scout Fly Near Oracle",
    114: "SV: Scout Fly In Farmer's House"
}

# Forbidden Jungle
locFJ_scoutTable = {
    115: "FJ: Scout Fly At End Of Path",
    116: "FJ: Scout Fly On Spiral Of Stumps",
    117: "FJ: Scout Fly Under Bridge",
    118: "FJ: Scout Fly At End Of River",
    119: "FJ: Scout Fly Behind Lurker Machine",
    120: "FJ: Scout Fly Around Temple Spire",
    121: "FJ: Scout Fly On Top Of Temple"
}

# Sentinel Beach
locSB_scoutTable = {
    122: "SB: Scout Fly At Entrance",
    123: "SB: Scout Fly Overlooking Locked Boxes",
    124: "SB: Scout Fly On Path To Flut Flut",
    125: "SB: Scout Fly Under Wood Pillars",
    126: "SB: Scout Fly Overlooking Blue Eco Vents",
    127: "SB: Scout Fly Overlooking Green Eco Vents",
    128: "SB: Scout Fly On Sentinel"
}

# Misty Island
locMI_scoutTable = {
    129: "MI: Scout Fly Overlooking Entrance",
    130: "MI: Scout Fly On Ledge Path, First",
    131: "MI: Scout Fly On Ledge Path, Second",
    132: "MI: Scout Fly Overlooking Shipyard",
    133: "MI: Scout Fly On Ship",
    134: "MI: Scout Fly On Barrel Ramps",
    135: "MI: Scout Fly On Zoomer Ramps"
}

# Fire Canyon
locFC_scoutTable = {
    136: "FC: Scout Fly 1",
    137: "FC: Scout Fly 2",
    138: "FC: Scout Fly 3",
    139: "FC: Scout Fly 4",
    140: "FC: Scout Fly 5",
    141: "FC: Scout Fly 6",
    142: "FC: Scout Fly 7"
}

# Rock Village
locRV_scoutTable = {
    143: "RV: Scout Fly Behind Sage's Hut",
    144: "RV: Scout Fly On Path To Village",
    145: "RV: Scout Fly Behind Geologist",
    146: "RV: Scout Fly Behind Fiery Boulder",
    147: "RV: Scout Fly On Dock",
    148: "RV: Scout Fly At Pontoon Bridge",
    149: "RV: Scout Fly At Boggy Swamp Entrance"
}

# Precursor Basin
locPB_scoutTable = {
    150: "PB: Scout Fly Overlooking Entrance",
    151: "PB: Scout Fly Near Mole Hole",
    152: "PB: Scout Fly At Purple Ring Start",
    153: "PB: Scout Fly Overlooking Dark Eco Plant",
    154: "PB: Scout Fly At Green Ring Start",
    155: "PB: Scout Fly Before Big Jump",
    156: "PB: Scout Fly Near Dark Eco Plant"
}

# Lost Precursor City
locLPC_scoutTable = {
    157: "LPC: Scout Fly First Room",
    158: "LPC: Scout Fly Before Second Room",
    159: "LPC: Scout Fly Second Room, Near Orb Vent",
    160: "LPC: Scout Fly Second Room, On Path To Cell",
    161: "LPC: Scout Fly Second Room, Green Switch",
    162: "LPC: Scout Fly Second Room, Blue Switch",
    163: "LPC: Scout Fly Across Steam Vents"
}

# Boggy Swamp
locBS_scoutTable = {
    164: "BS: Scout Fly Near Entrance",
    165: "BS: Scout Fly Over First Jump Pad",
    166: "BS: Scout Fly Over Second Jump Pad",
    167: "BS: Scout Fly Across Black Swamp",
    168: "BS: Scout Fly Overlooking Flut Flut",
    169: "BS: Scout Fly On Flut Flut Platforms",
    170: "BS: Scout Fly In Field Of Boxes"
}

# Mountain Pass
locMP_scoutTable = {
    171: "MP: Scout Fly 1",
    172: "MP: Scout Fly 2",
    173: "MP: Scout Fly 3",
    174: "MP: Scout Fly 4",
    175: "MP: Scout Fly 5",
    176: "MP: Scout Fly 6",
    177: "MP: Scout Fly 7"
}

# Volcanic Crater
locVC_scoutTable = {
    178: "VC: Scout Fly In Miner's Cave",
    179: "VC: Scout Fly Near Oracle",
    180: "VC: Scout Fly Overlooking Minecarts",
    181: "VC: Scout Fly On First Minecart Path",
    182: "VC: Scout Fly At Minecart Junction",
    183: "VC: Scout Fly At Spider Cave Entrance",
    184: "VC: Scout Fly Under Mountain Pass Exit"
}

# Spider Cave
locSC_scoutTable = {
    185: "SC: Scout Fly Across Dark Eco Pool",
    186: "SC: Scout Fly At Dark Area Entrance",
    187: "SC: Scout Fly First Room, Overlooking Entrance",
    188: "SC: Scout Fly First Room, Near Dark Crystal",
    189: "SC: Scout Fly First Room, Near Dark Eco Pool",
    190: "SC: Scout Fly Robot Room, First Level",
    191: "SC: Scout Fly Robot Room, Second Level",
}

# Snowy Mountain
locSM_scoutTable = {
    192: "SM: Scout Fly Near Entrance",
    193: "SM: Scout Fly Near Frozen Box",
    194: "SM: Scout Fly Near Yellow Eco Switch",
    195: "SM: Scout Fly On Cliff near Flut Flut",
    196: "SM: Scout Fly Under Bridge To Fort",
    197: "SM: Scout Fly On Top Of Fort Tower",
    198: "SM: Scout Fly On Top Of Fort"
}

# Lava Tube
locLT_scoutTable = {
    199: "LT: Scout Fly 1",
    200: "LT: Scout Fly 2",
    201: "LT: Scout Fly 3",
    202: "LT: Scout Fly 4",
    203: "LT: Scout Fly 5",
    204: "LT: Scout Fly 6",
    205: "LT: Scout Fly 7"
}

# Gol and Maias Citadel
locGMC_scoutTable = {
    206: "GMC: Scout Fly At Entrance",
    207: "GMC: Scout Fly At Jump Room Entrance",
    208: "GMC: Scout Fly On Ledge Across Rotators",
    209: "GMC: Scout Fly At Tile Color Puzzle",
    210: "GMC: Scout Fly At Blast Furnace",
    211: "GMC: Scout Fly At Path To Robot",
    212: "GMC: Scout Fly On Top Of Rotating Tower"
}
