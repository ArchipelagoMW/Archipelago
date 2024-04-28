import logging

from .data import rname
from .regions import get_region_info
from .locations import get_location_info
from .options import WarpOrder

from typing import TYPE_CHECKING, Dict, List, Tuple, Union

if TYPE_CHECKING:
    from . import CV64World


# # #    KEY    # # #
# "start region" = The Region that the start of the stage is in. Used for connecting the previous stage's end and
#                  alternate end (if it exists) Entrances to the start of the next one.
# "start map id" = The map ID that the start of the stage is in.
# "start spawn id" = The player spawn location ID for the start of the stage. This and "start map id" are both written
#                    to the previous stage's end loading zone to make it send the player to the next stage in the
#                    world's determined stage order.
# "mid region" = The Region that the stage's middle warp point is in. Used for connecting the warp Entrances after the
#                starting stage to where they should be connecting to.
# "mid map id" = The map ID that the stage's middle warp point is in.
# "mid spawn id" = The player spawn location ID for the stage's middle warp point. This and "mid map id" are both
#                  written to the warp menu code to make it send the player to where it should be sending them.
# "end region" = The Region that the end of the stage is in. Used for connecting the next stage's beginning Entrance
#                (if it exists) to the end of the previous one.
# "end map id" = The map ID that the end of the stage is in.
# "end spawn id" = The player spawn location ID for the end of the stage. This and "end map id" are both written to the
#                  next stage's beginning loading zone (if it exists) to make it send the player to the previous stage
#                  in the world's determined stage order.
# startzone map offset = The offset in the ROM to overwrite to change where the start of the stage leads.
# startzone spawn offset = The offset in the ROM to overwrite to change what spawn location in the previous map the
#                          start of the stage puts the player at.
# endzone map offset = The offset in the ROM to overwrite to change where the end of the stage leads.
# endzone spawn offset = The offset in the ROM to overwrite to change what spawn location in the next map the end of
#                        the stage puts the player at.
# altzone map offset = The offset in the ROM to overwrite to change where the alternate end of the stage leads
#                      (if it exists).
# altzone spawn offset = The offset in the ROM to overwrite to change what spawn location in the next map the alternate
#                        end of the stage puts the player at.
# character = What character that stage is exclusively meant for normally. Used in determining what stages to leave out
#             depending on what character stage setting was chosen in the player options.
# save number offsets = The offsets to overwrite to change what stage number is displayed on the save file when saving
#                       at the stage's White Jewels.
# regions = All Regions that make up the stage. If the stage is in the world's active stages, its Regions and their
#           corresponding Locations and Entrances will all be created.
stage_info = {
    "Forest of Silence": {
        "start region": rname.forest_start, "start map id": b"\x00", "start spawn id": b"\x00",
        "mid region": rname.forest_mid, "mid map id": b"\x00", "mid spawn id": b"\x04",
        "end region": rname.forest_end, "end map id": b"\x00", "end spawn id": b"\x01",
        "endzone map offset": 0xB6302F, "endzone spawn offset": 0xB6302B,
        "save number offsets": [0x1049C5, 0x1049CD, 0x1049D5],
        "regions": [rname.forest_start,
                    rname.forest_mid,
                    rname.forest_end]
    },

    "Castle Wall": {
        "start region": rname.cw_start, "start map id": b"\x02", "start spawn id": b"\x00",
        "mid region": rname.cw_start, "mid map id": b"\x02", "mid spawn id": b"\x07",
        "end region": rname.cw_exit, "end map id": b"\x02", "end spawn id": b"\x10",
        "endzone map offset": 0x109A5F, "endzone spawn offset": 0x109A61,
        "save number offsets": [0x1049DD, 0x1049E5, 0x1049ED],
        "regions": [rname.cw_start,
                    rname.cw_exit,
                    rname.cw_ltower]
    },

    "Villa": {
        "start region": rname.villa_start, "start map id": b"\x03", "start spawn id": b"\x00",
        "mid region": rname.villa_storeroom, "mid map id": b"\x05", "mid spawn id": b"\x04",
        "end region": rname.villa_crypt, "end map id": b"\x1A", "end spawn id": b"\x03",
        "endzone map offset": 0xD9DA3, "endzone spawn offset": 0x109E81,
        "altzone map offset": 0xD9DAB, "altzone spawn offset": 0x109E81,
        "save number offsets": [0x1049F5, 0x1049FD, 0x104A05, 0x104A0D],
        "regions": [rname.villa_start,
                    rname.villa_main,
                    rname.villa_storeroom,
                    rname.villa_archives,
                    rname.villa_maze,
                    rname.villa_servants,
                    rname.villa_crypt]
    },

    "Tunnel": {
        "start region": rname.tunnel_start, "start map id": b"\x07", "start spawn id": b"\x00",
        "mid region": rname.tunnel_end, "mid map id": b"\x07", "mid spawn id": b"\x03",
        "end region": rname.tunnel_end, "end map id": b"\x07", "end spawn id": b"\x11",
        "endzone map offset": 0x109B4F, "endzone spawn offset": 0x109B51, "character": "Reinhardt",
        "save number offsets": [0x104A15, 0x104A1D, 0x104A25, 0x104A2D],
        "regions": [rname.tunnel_start,
                    rname.tunnel_end]
    },

    "Underground Waterway": {
        "start region": rname.uw_main, "start map id": b"\x08", "start spawn id": b"\x00",
        "mid region": rname.uw_main, "mid map id": b"\x08", "mid spawn id": b"\x03",
        "end region": rname.uw_end, "end map id": b"\x08", "end spawn id": b"\x01",
        "endzone map offset": 0x109B67, "endzone spawn offset": 0x109B69, "character": "Carrie",
        "save number offsets": [0x104A35, 0x104A3D],
        "regions": [rname.uw_main,
                    rname.uw_end]
    },

    "Castle Center": {
        "start region": rname.cc_main, "start map id": b"\x19", "start spawn id": b"\x00",
        "mid region": rname.cc_main, "mid map id": b"\x0E", "mid spawn id": b"\x03",
        "end region": rname.cc_elev_top, "end map id": b"\x0F", "end spawn id": b"\x02",
        "endzone map offset": 0x109CB7, "endzone spawn offset": 0x109CB9,
        "altzone map offset": 0x109CCF, "altzone spawn offset": 0x109CD1,
        "save number offsets": [0x104A45, 0x104A4D, 0x104A55, 0x104A5D, 0x104A65, 0x104A6D, 0x104A75],
        "regions": [rname.cc_main,
                    rname.cc_torture_chamber,
                    rname.cc_library,
                    rname.cc_crystal,
                    rname.cc_elev_top]
    },

    "Duel Tower": {
        "start region": rname.dt_main, "start map id": b"\x13", "start spawn id": b"\x00",
        "startzone map offset": 0x109DA7, "startzone spawn offset": 0x109DA9,
        "mid region": rname.dt_main, "mid map id": b"\x13", "mid spawn id": b"\x15",
        "end region": rname.dt_main, "end map id": b"\x13", "end spawn id": b"\x01",
        "endzone map offset": 0x109D8F, "endzone spawn offset": 0x109D91, "character": "Reinhardt",
        "save number offsets": [0x104ACD],
        "regions": [rname.dt_main]
    },

    "Tower of Execution": {
        "start region": rname.toe_main, "start map id": b"\x10", "start spawn id": b"\x00",
        "startzone map offset": 0x109D17, "startzone spawn offset": 0x109D19,
        "mid region": rname.toe_main, "mid map id": b"\x10", "mid spawn id": b"\x02",
        "end region": rname.toe_main, "end map id": b"\x10", "end spawn id": b"\x12",
        "endzone map offset": 0x109CFF, "endzone spawn offset": 0x109D01, "character": "Reinhardt",
        "save number offsets": [0x104A7D, 0x104A85],
        "regions": [rname.toe_main,
                    rname.toe_ledge]
    },

    "Tower of Science": {
        "start region": rname.tosci_start, "start map id": b"\x12", "start spawn id": b"\x00",
        "startzone map offset": 0x109D77, "startzone spawn offset": 0x109D79,
        "mid region": rname.tosci_conveyors, "mid map id": b"\x12", "mid spawn id": b"\x03",
        "end region": rname.tosci_conveyors, "end map id": b"\x12", "end spawn id": b"\x04",
        "endzone map offset": 0x109D5F, "endzone spawn offset": 0x109D61, "character": "Carrie",
        "save number offsets": [0x104A95, 0x104A9D, 0x104AA5],
        "regions": [rname.tosci_start,
                    rname.tosci_three_doors,
                    rname.tosci_conveyors,
                    rname.tosci_key3]
    },

    "Tower of Sorcery": {
        "start region": rname.tosor_main, "start map id": b"\x11", "start spawn id": b"\x00",
        "startzone map offset": 0x109D47, "startzone spawn offset": 0x109D49,
        "mid region": rname.tosor_main, "mid map id": b"\x11", "mid spawn id": b"\x01",
        "end region": rname.tosor_main, "end map id": b"\x11", "end spawn id": b"\x13",
        "endzone map offset": 0x109D2F, "endzone spawn offset": 0x109D31, "character": "Carrie",
        "save number offsets": [0x104A8D],
        "regions": [rname.tosor_main]
    },

    "Room of Clocks": {
        "start region": rname.roc_main, "start map id": b"\x1B", "start spawn id": b"\x00",
        "mid region": rname.roc_main, "mid map id": b"\x1B", "mid spawn id": b"\x02",
        "end region": rname.roc_main, "end map id": b"\x1B", "end spawn id": b"\x14",
        "endzone map offset": 0x109EAF, "endzone spawn offset": 0x109EB1,
        "save number offsets": [0x104AC5],
        "regions": [rname.roc_main]
    },

    "Clock Tower": {
        "start region": rname.ct_start, "start map id": b"\x17", "start spawn id": b"\x00",
        "mid region": rname.ct_middle, "mid map id": b"\x17", "mid spawn id": b"\x02",
        "end region": rname.ct_end, "end map id": b"\x17", "end spawn id": b"\x03",
        "endzone map offset": 0x109E37, "endzone spawn offset": 0x109E39,
        "save number offsets": [0x104AB5, 0x104ABD],
        "regions": [rname.ct_start,
                    rname.ct_middle,
                    rname.ct_end]
    },

    "Castle Keep": {
        "start region": rname.ck_main, "start map id": b"\x14", "start spawn id": b"\x02",
        "mid region": rname.ck_main, "mid map id": b"\x14", "mid spawn id": b"\x03",
        "end region": rname.ck_drac_chamber,
        "save number offsets": [0x104AAD],
        "regions": [rname.ck_main]
    },
}

vanilla_stage_order = ("Forest of Silence", "Castle Wall", "Villa", "Tunnel", "Underground Waterway", "Castle Center",
                       "Duel Tower", "Tower of Execution", "Tower of Science", "Tower of Sorcery", "Room of Clocks",
                       "Clock Tower", "Castle Keep")

# # #    KEY    # # #
# "prev" = The previous stage in the line.
# "next" = The next stage in the line.
# "alt" = The alternate next stage in the line (if one exists).
# "position" = The stage's number in the order of stages.
# "path" = Character indicating whether the stage is on the main path or an alternate path, similar to Rondo of Blood.
#          Used in writing the randomized stage order to the spoiler.
vanilla_stage_exits = {rname.forest_of_silence: {"prev": None, "next": rname.castle_wall,
                                                 "alt": None, "position": 1, "path": " "},
                       rname.castle_wall: {"prev": None, "next": rname.villa,
                                           "alt": None, "position": 2, "path": " "},
                       rname.villa: {"prev": None, "next": rname.tunnel,
                                     "alt": rname.underground_waterway, "position": 3, "path": " "},
                       rname.tunnel: {"prev": None, "next": rname.castle_center,
                                      "alt": None, "position": 4, "path": " "},
                       rname.underground_waterway: {"prev": None, "next": rname.castle_center,
                                                    "alt": None, "position": 4, "path": "'"},
                       rname.castle_center: {"prev": None, "next": rname.duel_tower,
                                             "alt": rname.tower_of_science, "position": 5, "path": " "},
                       rname.duel_tower: {"prev": rname.castle_center, "next": rname.tower_of_execution,
                                          "alt": None, "position": 6, "path": " "},
                       rname.tower_of_execution: {"prev": rname.duel_tower, "next": rname.room_of_clocks,
                                                  "alt": None, "position": 7, "path": " "},
                       rname.tower_of_science: {"prev": rname.castle_center, "next": rname.tower_of_sorcery,
                                                "alt": None, "position": 6, "path": "'"},
                       rname.tower_of_sorcery: {"prev": rname.tower_of_science, "next": rname.room_of_clocks,
                                                "alt": None, "position": 7, "path": "'"},
                       rname.room_of_clocks: {"prev": None, "next": rname.clock_tower,
                                              "alt": None, "position": 8, "path": " "},
                       rname.clock_tower: {"prev": None, "next": rname.castle_keep,
                                           "alt": None, "position": 9, "path": " "},
                       rname.castle_keep: {"prev": None, "next": None,
                                           "alt": None, "position": 10, "path": " "}}


def get_stage_info(stage: str, info: str) -> Union[str, int, Union[List[int], List[str]], None]:
    return stage_info[stage].get(info, None)


def get_locations_from_stage(stage: str) -> List[str]:
    overall_locations = []
    for region in get_stage_info(stage, "regions"):
        stage_locations = get_region_info(region, "locations")
        if stage_locations is not None:
            overall_locations += stage_locations

    final_locations = []
    for loc in overall_locations:
        if get_location_info(loc, "code") is not None:
            final_locations.append(loc)
    return final_locations


def verify_character_stage(world: "CV64World", stage: str) -> bool:
    # Verify a character stage is in the world if the given stage is a character stage.
    stage_char = get_stage_info(stage, "character")
    return stage_char is None or (world.reinhardt_stages and stage_char == "Reinhardt") or \
        (world.carrie_stages and stage_char == "Carrie")


def get_normal_stage_exits(world: "CV64World") -> Dict[str, dict]:
    exits = {name: vanilla_stage_exits[name].copy() for name in vanilla_stage_exits}
    non_branching_pos = 1

    for stage in stage_info:
        # Remove character stages that are not enabled.
        if not verify_character_stage(world, stage):
            del exits[stage]
            continue

        # If branching pathways are not enabled, update the exit info to converge said stages on a single path.
        if world.branching_stages:
            continue
        if world.carrie_stages and not world.reinhardt_stages and exits[stage]["alt"] is not None:
            exits[stage]["next"] = exits[stage]["alt"]
        elif world.carrie_stages and world.reinhardt_stages and stage != rname.castle_keep:
            exits[stage]["next"] = vanilla_stage_order[vanilla_stage_order.index(stage) + 1]
        exits[stage]["alt"] = None
        exits[stage]["position"] = non_branching_pos
        exits[stage]["path"] = " "
        non_branching_pos += 1

    return exits


def shuffle_stages(world: "CV64World", stage_1_blacklist: List[str]) \
        -> Tuple[Dict[str, Dict[str, Union[str, int, None]]], str, List[str]]:
    """Woah, this is a lot! I should probably summarize what's happening in here, huh?

    So, in the vanilla game, all the stages are basically laid out on a linear "timeline" with some stages being
    different depending on who you are playing as. The different character stages, in question, are the one following
    Villa and the two following Castle Center. The ends of these two stages are considered the route divergences and, in
    this rando, the game's behavior has been changed in such that both characters can access each other's exclusive
    stages (thereby making the entire game playable in just one character run). With this in mind, when shuffling the
    stages around, there is one particularly big rule that must be kept in mind to ensure things don't get too wacky.
    That being:

    Villa and Castle Center cannot appear in branching path stage slots; they can only be on "main" path slots.

    So for this reason, generating a new stage layout is not as simple as just scrambling a list of stages around. It
    must be done in such a way that whatever stages directly follow Villa or CC is not the other stage. The exception is
    if branching stages are not a thing at all due to the player settings, in which case everything I said above does
    not matter. Consider the following representation of a stage "timeline", wherein each "-" represents a main stage
    and a "=" represents a pair of branching stages:

    -==---=---

    In the above example, CC is the first "-" and Villa is the fourth. CC and Villa can only be "-"s whereas every other
    stage can be literally anywhere, including on one of the "=" dashes. Villa will always be followed by one pair of
    branching stages and CC will be followed by two pairs.

    This code starts by first generating a singular list of stages that fit the criteria of Castle Center not being in
    the next two entries following Villa and Villa not being in the next four entries after Castle Center. Once that has
    been figured out, it will then generate a dictionary of stages with the appropriate information regarding what
    stages come before and after them to then be used for Entrance creation as well as what position in the list they
    are in for the purposes of the spoiler log and extended hint information.

    I opted to use the Rondo of Blood "'" stage notation to represent Carrie stage slots specifically. If a main stage
    with a backwards connection connects backwards into a pair of branching stages, it will be the non-"'" stage
    (Reinhardt's) that it connects to. The Carrie stage slot cannot be accessed this way.

    If anyone has any ideas or suggestions on how to improve this, I'd love to hear them! Because it's only going to get
    uglier come Legacy of Darkness and Cornell's funny side route later on.
    """

    starting_stage_value = world.options.starting_stage.value

    # Verify the starting stage is valid. If it isn't, pick a stage at random.
    if vanilla_stage_order[starting_stage_value] not in stage_1_blacklist and \
            verify_character_stage(world, vanilla_stage_order[starting_stage_value]):
        starting_stage = vanilla_stage_order[starting_stage_value]
    else:
        logging.warning(f"[{world.multiworld.player_name[world.player]}] {vanilla_stage_order[starting_stage_value]} "
                        f"cannot be the starting stage with the chosen settings. Picking a different stage instead...")
        possible_stages = []
        for stage in vanilla_stage_order:
            if stage in world.active_stage_exits and stage != rname.castle_keep:
                possible_stages.append(stage)
        starting_stage = world.random.choice(possible_stages)
        world.options.starting_stage.value = vanilla_stage_order.index(starting_stage)

    remaining_stage_pool = [stage for stage in world.active_stage_exits]
    remaining_stage_pool.remove(rname.castle_keep)

    total_stages = len(remaining_stage_pool)

    new_stage_order = []
    villa_cc_ids = [2, 3]
    alt_villa_stage = []
    alt_cc_stages = []

    # If there are branching stages, remove Villa and CC from the list and determine their placements first.
    if world.branching_stages:
        villa_cc_ids = world.random.sample(range(1, 5), 2)
        remaining_stage_pool.remove(rname.villa)
        remaining_stage_pool.remove(rname.castle_center)

    # Remove the starting stage from the remaining pool if it's in there at this point.
    if starting_stage in remaining_stage_pool:
        remaining_stage_pool.remove(starting_stage)

    # If Villa or CC is our starting stage, force its respective ID to be 0 and re-randomize the other.
    if starting_stage == rname.villa:
        villa_cc_ids[0] = 0
        villa_cc_ids[1] = world.random.randint(1, 5)
    elif starting_stage == rname.castle_center:
        villa_cc_ids[1] = 0
        villa_cc_ids[0] = world.random.randint(1, 5)

    for i in range(total_stages):
        # If we're on Villa or CC's ID while in branching stage mode, put the respective stage in the slot.
        if world.branching_stages and i == villa_cc_ids[0] and rname.villa not in new_stage_order:
            new_stage_order.append(rname.villa)
            villa_cc_ids[1] += 2
        elif world.branching_stages and i == villa_cc_ids[1] and rname.castle_center not in new_stage_order:
            new_stage_order.append(rname.castle_center)
            villa_cc_ids[0] += 4
        else:
            # If neither of the above are true, if we're looking at Stage 1, append the starting stage.
            # Otherwise, draw a random stage from the active list and delete it from there.
            if i == 0:
                new_stage_order.append(starting_stage)
            else:
                new_stage_order.append(world.random.choice(remaining_stage_pool))
                remaining_stage_pool.remove(new_stage_order[i])

        # If we're looking at an alternate stage slot, put the stage in one of these lists to indicate it as such
        if not world.branching_stages:
            continue
        if i - 2 >= 0:
            if new_stage_order[i - 2] == rname.villa:
                alt_villa_stage.append(new_stage_order[i])
        if i - 3 >= 0:
            if new_stage_order[i - 3] == rname.castle_center:
                alt_cc_stages.append(new_stage_order[i])
        if i - 4 >= 0:
            if new_stage_order[i - 4] == rname.castle_center:
                alt_cc_stages.append(new_stage_order[i])

    new_stage_order.append(rname.castle_keep)

    # Update the dictionary of stage exits
    current_stage_number = 1
    for i in range(len(new_stage_order)):
        # Stage position number and alternate path indicator
        world.active_stage_exits[new_stage_order[i]]["position"] = current_stage_number
        if new_stage_order[i] in alt_villa_stage + alt_cc_stages:
            world.active_stage_exits[new_stage_order[i]]["path"] = "'"
        else:
            world.active_stage_exits[new_stage_order[i]]["path"] = " "

        # Previous stage
        if world.active_stage_exits[new_stage_order[i]]["prev"]:
            if i - 1 < 0:
                world.active_stage_exits[new_stage_order[i]]["prev"] = "Menu"
            elif world.branching_stages:
                if new_stage_order[i - 1] == alt_villa_stage[0] or new_stage_order[i] == alt_villa_stage[0]:
                    world.active_stage_exits[new_stage_order[i]]["prev"] = new_stage_order[i - 2]
                elif new_stage_order[i - 1] == alt_cc_stages[1] or new_stage_order[i] == alt_cc_stages[0]:
                    world.active_stage_exits[new_stage_order[i]]["prev"] = new_stage_order[i - 3]
                else:
                    world.active_stage_exits[new_stage_order[i]]["prev"] = new_stage_order[i - 1]
            else:
                world.active_stage_exits[new_stage_order[i]]["prev"] = new_stage_order[i - 1]

        # Next stage
        if world.active_stage_exits[new_stage_order[i]]["next"]:
            if world.branching_stages:
                if new_stage_order[i + 1] == alt_villa_stage[0]:
                    world.active_stage_exits[new_stage_order[i]]["next"] = new_stage_order[i + 2]
                    current_stage_number -= 1
                elif new_stage_order[i + 1] == alt_cc_stages[0]:
                    world.active_stage_exits[new_stage_order[i]]["next"] = new_stage_order[i + 3]
                    current_stage_number -= 2
                else:
                    world.active_stage_exits[new_stage_order[i]]["next"] = new_stage_order[i + 1]
            else:
                world.active_stage_exits[new_stage_order[i]]["next"] = new_stage_order[i + 1]

        # Alternate next stage
        if world.active_stage_exits[new_stage_order[i]]["alt"]:
            if world.branching_stages:
                if new_stage_order[i] == rname.villa:
                    world.active_stage_exits[new_stage_order[i]]["alt"] = alt_villa_stage[0]
                else:
                    world.active_stage_exits[new_stage_order[i]]["alt"] = alt_cc_stages[0]
            else:
                world.active_stage_exits[new_stage_order[i]]["alt"] = None

        current_stage_number += 1

    return world.active_stage_exits, starting_stage, new_stage_order


def generate_warps(world: "CV64World") -> List[str]:
    # Create a list of warps from the active stage list. They are in a random order by default and will never
    # include the starting stage.
    possible_warps = [stage for stage in world.active_stage_list]

    # Remove the starting stage from the possible warps.
    del (possible_warps[0])

    active_warp_list = world.random.sample(possible_warps, 7)

    if world.options.warp_order == WarpOrder.option_seed_stage_order:
        # Arrange the warps to be in the seed's stage order
        new_list = world.active_stage_list.copy()
        for warp in world.active_stage_list:
            if warp not in active_warp_list:
                new_list.remove(warp)
        active_warp_list = new_list
    elif world.options.warp_order == WarpOrder.option_vanilla_stage_order:
        # Arrange the warps to be in the vanilla game's stage order
        new_list = list(vanilla_stage_order)
        for warp in vanilla_stage_order:
            if warp not in active_warp_list:
                new_list.remove(warp)
        active_warp_list = new_list

    # Insert the starting stage at the start of the warp list
    active_warp_list.insert(0, world.active_stage_list[0])

    return active_warp_list


def get_region_names(active_stage_exits: Dict[str, Dict[str, Union[str, int, None]]]) -> List[str]:
    region_names = []
    for stage in active_stage_exits:
        stage_regions = get_stage_info(stage, "regions")
        for region in stage_regions:
            region_names.append(region)

    return region_names
