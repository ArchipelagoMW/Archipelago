from ..GameID import jak1_id

# Precursor Orbs are not necessarily given ID's by the game.

# Of the 2000 orbs (or "money") you can pick up, only 1233 are standalone ones you find in the overworld.
# We can identify them by Actor ID's, which run from 549 to 24433. Other actors reside in this range,
# so like Power Cells these are not ordered, nor contiguous, nor exclusively orbs.

# In fact, other ID's in this range belong to actors that spawn orbs when they are activated or when they die,
# like steel crates, orb caches, Spider Cave gnawers, or jumping on the Plant Boss's head.

# These orbs that spawn from parent actors DON'T have an Actor ID themselves - the parent object keeps
# track of how many of its orbs have been picked up. If you pick up only some of its orbs, it
# will respawn when you leave the area, and only drop the remaining number of orbs when activated/killed.
# Once all the orbs are picked up, the actor will permanently "retire" and never spawn again.
# The maximum number of orbs that any actor can spawn is 30 (the orb caches in citadel). Covering
# these ID-less orbs may need to be a future enhancement. TODO ^^

# We can use 2^15 to offset them from Orb Caches, because Orb Cache ID's max out at (jak1_id + 17792).
orb_offset = 32768


# These helper functions do all the math required to get information about each
# precursor orb and translate its ID between AP and OpenGOAL.
def to_ap_id(game_id: int) -> int:
    assert game_id < jak1_id, f"Attempted to convert {game_id} to an AP ID, but it already is one."
    return jak1_id + orb_offset + game_id   # Add the offsets and the orb Actor ID.


def to_game_id(ap_id: int) -> int:
    assert ap_id >= jak1_id, f"Attempted to convert {ap_id} to a Jak 1 ID, but it already is one."
    return ap_id - jak1_id - orb_offset  # Reverse process, subtract the offsets.


# The ID's you see below correspond directly to that orb's Actor ID in the game.

# Geyser Rock
locGR_orbTable = {
}

# Sandover Village
locSV_orbTable = {
}

# Forbidden Jungle
locFJ_orbTable = {
}

# Sentinel Beach
locSB_orbTable = {
}

# Misty Island
locMI_orbTable = {
}

# Fire Canyon
locFC_orbTable = {
}

# Rock Village
locRV_orbTable = {
}

# Precursor Basin
locPB_orbTable = {
}

# Lost Precursor City
locLPC_orbTable = {
}

# Boggy Swamp
locBS_orbTable = {
}

# Mountain Pass
locMP_orbTable = {
}

# Volcanic Crater
locVC_orbTable = {
}

# Spider Cave
locSC_orbTable = {
}

# Snowy Mountain
locSM_orbTable = {
}

# Lava Tube
locLT_orbTable = {
}

# Gol and Maias Citadel
locGMC_orbTable = {
}
