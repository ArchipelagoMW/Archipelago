from ..game_id import jak1_id

# These are special checks that the game normally does not track. They are not game entities and thus
# don't have game ID's.

# Normally, for example, completing the fishing minigame is what gives you access to the
# fisherman's boat to get to Misty Island. The game treats completion of the fishing minigame as well as the
# power cell you receive as one and the same. The fisherman only gives you one item, a power cell.

# We're significantly altering the game logic here to decouple these concepts. First, completing the fishing minigame
# now counts as 2 Location checks. Second, the fisherman should give you a power cell (a generic item) as well as
# the "keys" to his boat (a special item). It is the "keys" that we are defining in this file, and the respective
# Item representing those keys will be defined in Items.py. These aren't real in the sense that
# they have a model and texture, they are just the logical representation of the boat unlock.

# We can use 2^11 to offset these from scout flies, just like we offset scout flies from power cells
# by 2^10. Even with the high-16 reminder bits, scout flies don't exceed an ID of (jak1_id + 1887).
special_offset = 2048


# These helper functions do all the math required to get information about each
# special check and translate its ID between AP and OpenGOAL.
def to_ap_id(game_id: int) -> int:
    if game_id >= jak1_id:
        raise ValueError(f"Attempted to convert {game_id} to an AP ID, but it already is one.")
    return jak1_id + special_offset + game_id   # Add the offsets and the orb Actor ID.


def to_game_id(ap_id: int) -> int:
    if ap_id < jak1_id:
        raise ValueError(f"Attempted to convert {ap_id} to a Jak 1 ID, but it already is one.")
    return ap_id - jak1_id - special_offset  # Reverse process, subtract the offsets.


# The ID's you see below correlate to each of their respective game-tasks, even though they are separate.
# This makes it easier for the new game logic to know what relates to what. I hope. God I hope.

loc_specialTable = {
    5: "Fisherman's Boat",
    4: "Jungle Elevator",
    2: "Blue Eco Switch",
    17: "Flut Flut",
    33: "Warrior's Pontoons",
    105: "Snowy Mountain Gondola",
    60: "Yellow Eco Switch",
    63: "Snowy Fort Gate",
    71: "Freed The Blue Sage",
    72: "Freed The Red Sage",
    73: "Freed The Yellow Sage",
    70: "Freed The Green Sage",
}
