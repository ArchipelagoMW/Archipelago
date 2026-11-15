from ..game_id import jak1_id
from ..levels import level_table_with_global

# Precursor Orbs are not necessarily given ID's by the game.

# Of the 2000 orbs (or "money") you can pick up, only 1233 are standalone ones you find in the overworld.
# We can identify them by Actor ID's, which run from 549 to 24433. Other actors reside in this range,
# so like Power Cells these are not ordered, nor contiguous, nor exclusively orbs.

# In fact, other ID's in this range belong to actors that spawn orbs when they are activated or when they die,
# like steel crates, orb caches, Spider Cave gnawers, or jumping on the Plant Boss's head. These orbs that spawn
# from parent actors DON'T have an Actor ID themselves - the parent object keeps track of how many of its orbs
# have been picked up.

# In order to deal with this mess, we're creating 2 extra functions that will create and identify Orb Locations for us.
# These will be compatible with both Global Orbsanity and Per-Level Orbsanity, allowing us to create any
# number of Locations depending on the bundle size chosen, while also guaranteeing that each has a unique address.

# We can use 2^15 to offset them from Orb Caches, because Orb Cache ID's max out at (jak1_id + 17792).
orb_offset = 32768


# These helper functions do all the math required to get information about each
# precursor orb and translate its ID between AP and OpenGOAL.
def to_ap_id(game_id: int) -> int:
    if game_id >= jak1_id:
        raise ValueError(f"Attempted to convert {game_id} to an AP ID, but it already is one.")
    return jak1_id + orb_offset + game_id   # Add the offsets and the orb Actor ID.


def to_game_id(ap_id: int) -> int:
    if ap_id < jak1_id:
        raise ValueError(f"Attempted to convert {ap_id} to a Jak 1 ID, but it already is one.")
    return ap_id - jak1_id - orb_offset  # Reverse process, subtract the offsets.


# Use this when the Memory Reader learns that you checked a specific bundle.
# Offset each level by 200 orbs (max number in any level),      {200, 400, ...}
# then divide orb count by bundle size,                         {201, 202, ...}
# then subtract 1.                                              {200, 201, ...}
def find_address(level_index: int, orb_count: int, bundle_size: int) -> int:
    result = (level_index * 200) + (orb_count // bundle_size) - 1
    return result


# Use this when assigning addresses during region generation.
def create_address(level_index: int, bundle_index: int) -> int:
    result = (level_index * 200) + bundle_index
    return result


# What follows is our methods of generating all the name/ID pairs for location_name_to_id.
# Remember that not every bundle will be used in the actual seed, we just need a static map of strings to ints.
locGR_orbBundleTable = {create_address(level_table_with_global["Geyser Rock"]["level_index"], index):
                        f"Geyser Rock Orb Bundle {index + 1}"
                        for index in range(level_table_with_global["Geyser Rock"]["orbs"])}
locSV_orbBundleTable = {create_address(level_table_with_global["Sandover Village"]["level_index"], index):
                        f"Sandover Village Orb Bundle {index + 1}"
                        for index in range(level_table_with_global["Sandover Village"]["orbs"])}
locFJ_orbBundleTable = {create_address(level_table_with_global["Forbidden Jungle"]["level_index"], index):
                        f"Forbidden Jungle Orb Bundle {index + 1}"
                        for index in range(level_table_with_global["Forbidden Jungle"]["orbs"])}
locSB_orbBundleTable = {create_address(level_table_with_global["Sentinel Beach"]["level_index"], index):
                        f"Sentinel Beach Orb Bundle {index + 1}"
                        for index in range(level_table_with_global["Sentinel Beach"]["orbs"])}
locMI_orbBundleTable = {create_address(level_table_with_global["Misty Island"]["level_index"], index):
                        f"Misty Island Orb Bundle {index + 1}"
                        for index in range(level_table_with_global["Misty Island"]["orbs"])}
locFC_orbBundleTable = {create_address(level_table_with_global["Fire Canyon"]["level_index"], index):
                        f"Fire Canyon Orb Bundle {index + 1}"
                        for index in range(level_table_with_global["Fire Canyon"]["orbs"])}
locRV_orbBundleTable = {create_address(level_table_with_global["Rock Village"]["level_index"], index):
                        f"Rock Village Orb Bundle {index + 1}"
                        for index in range(level_table_with_global["Rock Village"]["orbs"])}
locLPC_orbBundleTable = {create_address(level_table_with_global["Lost Precursor City"]["level_index"], index):
                         f"Lost Precursor City Orb Bundle {index + 1}"
                         for index in range(level_table_with_global["Lost Precursor City"]["orbs"])}
locBS_orbBundleTable = {create_address(level_table_with_global["Boggy Swamp"]["level_index"], index):
                        f"Boggy Swamp Orb Bundle {index + 1}"
                        for index in range(level_table_with_global["Boggy Swamp"]["orbs"])}
locPB_orbBundleTable = {create_address(level_table_with_global["Precursor Basin"]["level_index"], index):
                        f"Precursor Basin Orb Bundle {index + 1}"
                        for index in range(level_table_with_global["Precursor Basin"]["orbs"])}
locMP_orbBundleTable = {create_address(level_table_with_global["Mountain Pass"]["level_index"], index):
                        f"Mountain Pass Orb Bundle {index + 1}"
                        for index in range(level_table_with_global["Mountain Pass"]["orbs"])}
locVC_orbBundleTable = {create_address(level_table_with_global["Volcanic Crater"]["level_index"], index):
                        f"Volcanic Crater Orb Bundle {index + 1}"
                        for index in range(level_table_with_global["Volcanic Crater"]["orbs"])}
locSM_orbBundleTable = {create_address(level_table_with_global["Snowy Mountain"]["level_index"], index):
                        f"Snowy Mountain Orb Bundle {index + 1}"
                        for index in range(level_table_with_global["Snowy Mountain"]["orbs"])}
locSC_orbBundleTable = {create_address(level_table_with_global["Spider Cave"]["level_index"], index):
                        f"Spider Cave Orb Bundle {index + 1}"
                        for index in range(level_table_with_global["Spider Cave"]["orbs"])}
locLT_orbBundleTable = {create_address(level_table_with_global["Lava Tube"]["level_index"], index):
                        f"Lava Tube Orb Bundle {index + 1}"
                        for index in range(level_table_with_global["Lava Tube"]["orbs"])}
locGMC_orbBundleTable = {create_address(level_table_with_global["Gol and Maia's Citadel"]["level_index"], index):
                         f"Gol and Maia's Citadel Orb Bundle {index + 1}"
                         for index in range(level_table_with_global["Gol and Maia's Citadel"]["orbs"])}
locGlobal_orbBundleTable = {create_address(level_table_with_global[""]["level_index"], index):
                            f"Orb Bundle {index + 1}"
                            for index in range(level_table_with_global[""]["orbs"])}
loc_orbBundleTable = {
    **locGR_orbBundleTable,
    **locSV_orbBundleTable,
    **locSB_orbBundleTable,
    **locFJ_orbBundleTable,
    **locMI_orbBundleTable,
    **locFC_orbBundleTable,
    **locRV_orbBundleTable,
    **locLPC_orbBundleTable,
    **locBS_orbBundleTable,
    **locPB_orbBundleTable,
    **locMP_orbBundleTable,
    **locVC_orbBundleTable,
    **locSM_orbBundleTable,
    **locSC_orbBundleTable,
    **locLT_orbBundleTable,
    **locGMC_orbBundleTable,
    **locGlobal_orbBundleTable
}
