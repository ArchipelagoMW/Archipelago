from ..game_id import jak1_id

# Scout Flies are given ID's between 0 and 393311 by the game, explanation below.

# Each fly (or "buzzer") is given a unique 32-bit number broken into two 16-bit numbers.
# The lower 16 bits are the game-task ID of the power cell the fly corresponds to.
# The higher 16 bits are the index of the fly itself, from 000 (0) to 110 (6).

# Ex: The final scout fly on Geyser Rock
# 0000000000000110 0000000001011111
# (   Index: 6   ) (   Cell: 95   )

# Because flies are indexed from 0, each 0th fly's full ID == the power cell's ID.
# So we need to offset all of their ID's in order for Archipelago to separate them
# from their power cells. We can use 1024 (2^10) for this purpose, because scout flies
# only ever need 10 bits to identify themselves (3 for the index, 7 for the cell ID).

# We're also going to compress the ID by bit-shifting the fly index down to lower bits,
# keeping the scout fly ID range to a smaller set of numbers (1000 -> 2000, instead of 1 -> 400000).
fly_offset = 1024


# These helper functions do all the math required to get information about each
# scout fly and translate its ID between AP and OpenGOAL.
def to_ap_id(game_id: int) -> int:
    if game_id >= jak1_id:
        raise ValueError(f"Attempted to convert {game_id} to an AP ID, but it already is one.")
    cell_id = get_cell_id(game_id)                         # Get the power cell ID from the lowest 7 bits.
    buzzer_index = (game_id - cell_id) >> 9                # Get the index, bit shift it down 9 places.
    compressed_id = fly_offset + buzzer_index + cell_id    # Add the offset, the bit-shifted index, and the cell ID.
    return jak1_id + compressed_id                         # Last thing: add the game's ID.


def to_game_id(ap_id: int) -> int:
    if ap_id < jak1_id:
        raise ValueError(f"Attempted to convert {ap_id} to a Jak 1 ID, but it already is one.")
    compressed_id = ap_id - jak1_id                        # Reverse process. First thing: subtract the game's ID.
    cell_id = get_cell_id(compressed_id)                   # Get the power cell ID from the lowest 7 bits.
    buzzer_index = compressed_id - fly_offset - cell_id    # Get the bit-shifted index.
    return (buzzer_index << 9) + cell_id                   # Return the index to its normal place, re-add the cell ID.


# Get the power cell ID from the lowest 7 bits.
# Make sure to use this function ONLY when the input argument does NOT include jak1_id,
# because that number may flip some of the bottom 7 bits, and that will throw off this bit mask.
def get_cell_id(buzzer_id: int) -> int:
    if buzzer_id >= jak1_id:
        raise ValueError(f"Attempted to bit mask {buzzer_id}, but it is polluted by the game's ID {jak1_id}.")
    return buzzer_id & 0b1111111


# The ID's you see below correspond directly to that fly's 32-bit ID in the game.
# I used the decompiled entity JSON's and Jak's X/Y coordinates in Debug Mode
# to determine which box ID is which location.

# Geyser Rock
locGR_scoutTable = {
    95: "GR: Scout Fly On Ground, Front",
    327775: "GR: Scout Fly On Ground, Back",
    393311: "GR: Scout Fly On Left Ledge",
    65631: "GR: Scout Fly On Right Ledge",
    262239: "GR: Scout Fly On Middle Ledge, Left",
    131167: "GR: Scout Fly On Middle Ledge, Right",
    196703: "GR: Scout Fly On Top Ledge"
}

# Sandover Village
locSV_scoutTable = {
    262219: "SV: Scout Fly In Fisherman's House",
    327755: "SV: Scout Fly In Mayor's House",
    131147: "SV: Scout Fly Under Bridge",
    65611: "SV: Scout Fly Behind Sculptor's House",
    75: "SV: Scout Fly Overlooking Farmer's House",
    393291: "SV: Scout Fly Near Oracle",
    196683: "SV: Scout Fly In Farmer's House"
}

# Forbidden Jungle
locFJ_scoutTable = {
    393223: "FJ: Scout Fly At End Of Path",
    262151: "FJ: Scout Fly On Spiral Of Stumps",
    7: "FJ: Scout Fly Near Dark Eco Boxes",
    196615: "FJ: Scout Fly At End Of River",
    131079: "FJ: Scout Fly Behind Lurker Machine",
    327687: "FJ: Scout Fly Around Temple Spire",
    65543: "FJ: Scout Fly On Top Of Temple"
}

# Sentinel Beach
locSB_scoutTable = {
    327700: "SB: Scout Fly At Entrance",
    20: "SB: Scout Fly Overlooking Locked Boxes",
    65556: "SB: Scout Fly On Path To Flut Flut",
    262164: "SB: Scout Fly Under Wood Pillars",
    196628: "SB: Scout Fly Overlooking Blue Eco Vent",
    131092: "SB: Scout Fly Overlooking Green Eco Vents",
    393236: "SB: Scout Fly On Sentinel"
}

# Misty Island
locMI_scoutTable = {
    327708: "MI: Scout Fly Overlooking Entrance",
    65564: "MI: Scout Fly On Ledge Near Arena Entrance",
    262172: "MI: Scout Fly Near Arena Door",
    28: "MI: Scout Fly On Ledge Near Arena Exit",
    131100: "MI: Scout Fly On Ship",
    196636: "MI: Scout Fly On Barrel Ramps",
    393244: "MI: Scout Fly On Zoomer Ramps"
}

# Fire Canyon
locFC_scoutTable = {
    393284: "FC: Scout Fly 1",
    68: "FC: Scout Fly 2",
    65604: "FC: Scout Fly 3",
    196676: "FC: Scout Fly 4",
    131140: "FC: Scout Fly 5",
    262212: "FC: Scout Fly 6",
    327748: "FC: Scout Fly 7"
}

# Rock Village
locRV_scoutTable = {
    76: "RV: Scout Fly Behind Sage's Hut",
    131148: "RV: Scout Fly Near Waterfall",
    196684: "RV: Scout Fly Behind Geologist",
    262220: "RV: Scout Fly Behind Fiery Boulder",
    65612: "RV: Scout Fly On Dock",
    327756: "RV: Scout Fly At Pontoon Bridge",
    393292: "RV: Scout Fly At Boggy Swamp Entrance"
}

# Precursor Basin
locPB_scoutTable = {
    196665: "PB: Scout Fly Overlooking Entrance",
    393273: "PB: Scout Fly Near Mole Hole",
    131129: "PB: Scout Fly At Purple Ring Start",
    65593: "PB: Scout Fly Near Dark Eco Plant, Above",
    57: "PB: Scout Fly At Blue Ring Start",
    262201: "PB: Scout Fly Before Big Jump",
    327737: "PB: Scout Fly Near Dark Eco Plant, Below"
}

# Lost Precursor City
locLPC_scoutTable = {
    262193: "LPC: Scout Fly First Room",
    131121: "LPC: Scout Fly Before Second Room",
    393265: "LPC: Scout Fly Second Room, Near Orb Vent",
    196657: "LPC: Scout Fly Second Room, On Path To Cell",
    49: "LPC: Scout Fly Second Room, Green Pipe",  # Sunken Pipe Game, special cases. See `got-buzzer?`
    65585: "LPC: Scout Fly Second Room, Blue Pipe",  # Sunken Pipe Game, special cases. See `got-buzzer?`
    327729: "LPC: Scout Fly Across Steam Vents"
}

# Boggy Swamp
locBS_scoutTable = {
    43: "BS: Scout Fly Near Entrance",
    393259: "BS: Scout Fly Over First Jump Pad",
    65579: "BS: Scout Fly Over Second Jump Pad",
    262187: "BS: Scout Fly Across Black Swamp",
    327723: "BS: Scout Fly Overlooking Flut Flut",
    131115: "BS: Scout Fly On Flut Flut Platforms",
    196651: "BS: Scout Fly In Field Of Boxes"
}

# Mountain Pass
locMP_scoutTable = {
    88: "MP: Scout Fly 1",
    65624: "MP: Scout Fly 2",
    131160: "MP: Scout Fly 3",
    196696: "MP: Scout Fly 4",
    262232: "MP: Scout Fly 5",
    327768: "MP: Scout Fly 6",
    393304: "MP: Scout Fly 7"
}

# Volcanic Crater
locVC_scoutTable = {
    262221: "VC: Scout Fly In Miner's Cave",
    393293: "VC: Scout Fly Near Oracle",
    196685: "VC: Scout Fly On Stone Platforms",
    131149: "VC: Scout Fly Near Lava Tube",
    77: "VC: Scout Fly At Minecart Junction",
    65613: "VC: Scout Fly Near Spider Cave",
    327757: "VC: Scout Fly Near Mountain Pass"
}

# Spider Cave
locSC_scoutTable = {
    327765: "SC: Scout Fly Near Dark Cave Entrance",
    262229: "SC: Scout Fly In Dark Cave",
    393301: "SC: Scout Fly Main Cave, Overlooking Entrance",
    196693: "SC: Scout Fly Main Cave, Near Dark Crystal",
    131157: "SC: Scout Fly Main Cave, Near Robot Cave Entrance",
    85: "SC: Scout Fly Robot Cave, At Bottom Level",
    65621: "SC: Scout Fly Robot Cave, At Top Level",
}

# Snowy Mountain
locSM_scoutTable = {
    65: "SM: Scout Fly Near Entrance",
    327745: "SM: Scout Fly Near Frozen Box",
    65601: "SM: Scout Fly Near Yellow Eco Switch",
    131137: "SM: Scout Fly On Cliff near Flut Flut",
    393281: "SM: Scout Fly Under Bridge To Fort",
    196673: "SM: Scout Fly On Top Of Fort Tower",
    262209: "SM: Scout Fly On Top Of Fort"
}

# Lava Tube
locLT_scoutTable = {
    90: "LT: Scout Fly 1",
    65626: "LT: Scout Fly 2",
    327770: "LT: Scout Fly 3",
    262234: "LT: Scout Fly 4",
    131162: "LT: Scout Fly 5",
    196698: "LT: Scout Fly 6",
    393306: "LT: Scout Fly 7"
}

# Gol and Maias Citadel
locGMC_scoutTable = {
    91: "GMC: Scout Fly At Entrance",
    65627: "GMC: Scout Fly Main Room, Left of Robot",
    196699: "GMC: Scout Fly Main Room, Right of Robot",
    262235: "GMC: Scout Fly Before Jumping Lurkers",
    393307: "GMC: Scout Fly At Blast Furnace",
    131163: "GMC: Scout Fly At Launch Pad Room",
    327771: "GMC: Scout Fly Top Of Rotating Tower"
}
