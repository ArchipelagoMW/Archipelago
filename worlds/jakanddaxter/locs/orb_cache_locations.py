from ..game_id import jak1_id

# These are the locations of Orb Caches throughout the game, unlockable only with blue eco.
# They are not game collectables and thus don't have the same kinds of game ID's. They do, however, have actor ID's.
# There are a total of 14 in the game.

# When these are opened, we can execute a hook in the mod that might be able to tell us which orb cache we opened,
# by ID, and that will allow us to map a Location object to it. We'll be using these for Move Randomizer,
# where each move is "mapped" to an Orb Cache being unlocked. Obviously, they will then be randomized, but with moves
# not being considered Items by the game, we need to conjure SOME kind of Location for them, and Orb Caches is the best
# we can do.

# We can use 2^12 to offset these from special checks, just like we offset those from scout flies
# by 2^11. Special checks don't exceed an ID of (jak1_id + 2153).
orb_cache_offset = 4096


# These helper functions do all the math required to get information about each
# special check and translate its ID between AP and OpenGOAL. Similar to Scout Flies, these large numbers are not
# necessary, and we can flatten out the range in which these numbers lie.
def to_ap_id(game_id: int) -> int:
    if game_id >= jak1_id:
        raise ValueError(f"Attempted to convert {game_id} to an AP ID, but it already is one.")
    uncompressed_id = jak1_id + orb_cache_offset + game_id   # Add the offsets and the orb cache Actor ID.
    return uncompressed_id - 10344                           # Subtract the smallest Actor ID.


def to_game_id(ap_id: int) -> int:
    if ap_id < jak1_id:
        raise ValueError(f"Attempted to convert {ap_id} to a Jak 1 ID, but it already is one.")
    uncompressed_id = ap_id + 10344                          # Reverse process, add back the smallest Actor ID.
    return uncompressed_id - jak1_id - orb_cache_offset      # Subtract the offsets.


# The ID's you see below correlate to the Actor ID of each Orb Cache.

loc_orbCacheTable = {
    10344: "Orb Cache in Sandover Village",
    10369: "Orb Cache in Forbidden Jungle",
    11072: "Orb Cache on Misty Island",
    12634: "Orb Cache near Flut Flut Egg",
    12635: "Orb Cache near Pelican's Nest",
    10945: "Orb Cache in Rock Village",
    14507: "Orb Cache in First Sunken Chamber",
    14838: "Orb Cache in Second Sunken Chamber",
    23348: "Orb Cache in Snowy Fort (1)",
    23349: "Orb Cache in Snowy Fort (2)",
    23350: "Orb Cache in Snowy Fort (3)",
    24038: "Orb Cache at End of Blast Furnace",
    24039: "Orb Cache at End of Launch Pad Room",
    24040: "Orb Cache at Start of Launch Pad Room",
}
