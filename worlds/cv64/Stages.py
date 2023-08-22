import typing

from .Names import RName, IName


class CV64Stage:
    start_name: str
    startzone_map_offset: int
    startzone_spawn_offset: int
    start_map_id: int
    start_spawn_id: int

    mid_name: str
    mid_map_id: int
    mid_spawn_id: int

    end_name: str
    endzone_map_offset: int
    endzone_spawn_offset: int
    altzone_map_offset: int
    altzone_spawn_offset: int
    end_map_id: int
    end_spawn_id: int

    boss_count: int
    stage_number_offset_list: typing.List[int]

    stage_key_counts: typing.Dict[str, int]
    stage_non_filler_junk_counts: typing.Dict[str, int]
    stage_filler_junk_count: int
    multihit_non_filler_junk_counts: typing.Dict[str, int]
    multihit_filler_junk_count: int
    multihit_sub_weapon_counts: typing.Dict[str, int]
    sub_weapon_counts: typing.Dict[str, int]

    def __init__(self, start_region_name: str, startzone_map_offset: typing.Optional[int], startzone_spawn_offset:
                 typing.Optional[int], start_map_id: int, start_spawn_id: int, mid_region_name: str, mid_map_id: int,
                 mid_spawn_id: int, end_region_name: str, endzone_map_offset: typing.Optional[int],
                 endzone_spawn_offset: typing.Optional[int], altzone_map_offset: typing.Optional[int],
                 altzone_spawn_offset: typing.Optional[int], end_map_id: typing.Optional[int],
                 end_spawn_id: typing.Optional[int], boss_count: int, stage_number_offset_list: list,
                 stage_key_counts: dict, stage_non_filler_item_counts: dict, stage_filler_junk_count: int,
                 multihit_non_filler_item_counts: dict, multihit_filler_junk_count: int,
                 multihit_sub_weapon_counts: dict, sub_weapon_counts: dict):
        self.start_region_name = start_region_name
        self.startzone_map_offset = startzone_map_offset
        self.startzone_spawn_offset = startzone_spawn_offset
        self.start_map_id = start_map_id
        self.start_spawn_id = start_spawn_id

        self.mid_region_name = mid_region_name
        self.mid_map_id = mid_map_id
        self.mid_spawn_id = mid_spawn_id

        self.end_region_name = end_region_name
        self.endzone_map_offset = endzone_map_offset
        self.endzone_spawn_offset = endzone_spawn_offset
        self.altzone_map_offset = altzone_map_offset
        self.altzone_spawn_offset = altzone_spawn_offset
        self.end_map_id = end_map_id
        self.end_spawn_id = end_spawn_id

        self.boss_count = boss_count
        self.stage_number_offset_list = stage_number_offset_list

        self.stage_key_counts = stage_key_counts
        self.stage_non_filler_junk_counts = stage_non_filler_item_counts
        self.stage_filler_junk_count = stage_filler_junk_count
        self.multihit_non_filler_junk_counts = multihit_non_filler_item_counts
        self.multihit_filler_junk_count = multihit_filler_junk_count
        self.multihit_sub_weapon_counts = multihit_sub_weapon_counts
        self.sub_weapon_counts = sub_weapon_counts


stage_info = {
    "Forest of Silence":    CV64Stage(RName.forest_start, None, None, 0x00, 0x00,
                                      RName.forest_mid, 0x00, 0x04,
                                      RName.forest_end, 0xB6302F, 0xB6302B, None, None, 0x00, 0x01,
                                      3, [0x1049C5, 0x1049CD, 0x1049D5],
                                      {},
                                      {IName.roast_chicken: 4,
                                       IName.roast_beef: 3,
                                       IName.powerup: 1,
                                       IName.sun_card: 2,
                                       IName.moon_card: 1}, 12,
                                      {IName.roast_chicken: 1,
                                       IName.powerup: 1}, 7, {},
                                      {IName.holy_water: 1,
                                       IName.cross: 1,
                                       IName.axe: 1,
                                       IName.knife: 1}),

    "Castle Wall":          CV64Stage(RName.cw_start, None, None, 0x02, 0x00,
                                      RName.cw_start, 0x02, 0x07,
                                      RName.cw_exit, 0x109A5F, 0x109A61, None, None, 0x02, 0x10,
                                      1, [0x1049DD, 0x1049E5, 0x1049ED],
                                      {IName.left_tower_key: 1},
                                      {IName.roast_chicken: 2,
                                       IName.roast_beef: 1,
                                       IName.powerup: 1,
                                       IName.sun_card: 1,
                                       IName.moon_card: 2}, 2,
                                      {}, 10, {},
                                      {IName.holy_water: 1,
                                       IName.cross: 1,
                                       IName.axe: 1,
                                       IName.knife: 1}),

    "Villa":                CV64Stage(RName.villa_start, None, None, 0x03, 0x00,
                                      RName.villa_storeroom, 0x05, 0x04,
                                      RName.villa_crypt, 0xD9DA3, 0x109E81, 0xD9DAB, 0x109E81, 0x1A, 0x03,
                                      2, [0x1049F5, 0x1049FD, 0x104A05, 0x104A0D],
                                      {IName.storeroom_key: 1,
                                       IName.archives_key: 1,
                                       IName.garden_key: 1,
                                       IName.copper_key: 1},
                                      {IName.roast_chicken: 6,
                                       IName.roast_beef: 5,
                                       IName.purifying: 9,
                                       IName.powerup: 1,
                                       IName.sun_card: 1,
                                       IName.moon_card: 2}, 29,
                                      {IName.roast_chicken: 1,
                                       IName.purifying: 1,
                                       IName.cure_ampoule: 1}, 2, {},
                                      {IName.holy_water: 2,
                                       IName.cross: 1,
                                       IName.axe: 2,
                                       IName.knife: 3}),

    "Tunnel":               CV64Stage(RName.tunnel_start, None, None, 0x07, 0x00,
                                      RName.tunnel_end, 0x07, 0x03,
                                      RName.tunnel_end, 0x109B4F, 0x109B51, None, None, 0x07, 0x11,
                                      0, [0x104A15, 0x104A1D, 0x104A25, 0x104A2D],
                                      {},
                                      {IName.roast_chicken: 2,
                                       IName.roast_beef: 3,
                                       IName.cure_ampoule: 2,
                                       IName.powerup: 1,
                                       IName.sun_card: 2,
                                       IName.moon_card: 1}, 14,
                                      {IName.roast_chicken: 4,
                                       IName.purifying: 2,
                                       IName.cure_ampoule: 2}, 0, {},
                                      {IName.holy_water: 2,
                                       IName.cross: 2,
                                       IName.axe: 1,
                                       IName.knife: 1}),

    "Underground Waterway": CV64Stage(RName.uw_main, None, None, 0x08, 0x00,
                                      RName.uw_main, 0x08, 0x03,
                                      RName.uw_end, 0x109B67, 0x109B69, None, None, 0x08, 0x01,
                                      1, [0x104A35, 0x104A3D],
                                      {},
                                      {IName.roast_chicken: 1,
                                       IName.cure_ampoule: 1,
                                       IName.powerup: 1}, 3,
                                      {IName.roast_chicken: 3,
                                       IName.purifying: 2,
                                       IName.cure_ampoule: 2}, 2, {},
                                      {}),

    "Castle Center":        CV64Stage(RName.cc_lower, None, None, 0x19, 0x00,
                                      RName.cc_lower, 0x0E, 0x03,
                                      RName.cc_elev_top, 0x109CB7, 0x109CB9, 0x109CCF, 0x109CD1, 0x0F, 0x02,
                                      2, [0x104A45, 0x104A4D, 0x104A55, 0x104A5D, 0x104A65, 0x104A6D, 0x104A75],
                                      {IName.magical_nitro: 2,
                                       IName.mandragora: 2,
                                       IName.chamber_key: 1},
                                      {IName.roast_chicken: 4,
                                       IName.roast_beef: 5,
                                       IName.healing_kit: 1,
                                       IName.purifying: 4,
                                       IName.cure_ampoule: 2,
                                       IName.powerup: 2,
                                       IName.sun_card: 2,
                                       IName.moon_card: 1}, 27,
                                      {IName.roast_beef: 3,
                                       IName.purifying: 2,
                                       IName.cure_ampoule: 2}, 5, {},
                                      {IName.holy_water: 1,
                                       IName.cross: 1,
                                       IName.axe: 1}),

    "Duel Tower":           CV64Stage(RName.dt_main, 0x109DA7, 0x109DA9, 0x13, 0x00,
                                      RName.dt_main, 0x13, 0x15,
                                      RName.dt_main, 0x109D8F, 0x109D91, None, None, 0x13, 0x01,
                                      4, [0x104ACD],
                                      {},
                                      {IName.roast_chicken: 1,
                                       IName.roast_beef: 2,
                                       IName.powerup: 1}, 0,
                                      {}, 0, {},
                                      {IName.knife: 1}),

    "Tower of Execution":   CV64Stage(RName.toe_main, 0x109D17, 0x109D19, 0x10, 0x00,
                                      RName.toe_main, 0x10, 0x02,
                                      RName.toe_main, 0x109CFF, 0x109D01, None, None, 0x10, 0x12,
                                      0, [0x104A7D, 0x104A85],
                                      {IName.execution_key: 1},
                                      {IName.roast_chicken: 1,
                                       IName.roast_beef: 1}, 3,
                                      {IName.purifying: 1,
                                       IName.cure_ampoule: 1,
                                       IName.holy_water: 1}, 2, {},
                                      {IName.cross: 1}),

    "Tower of Science":     CV64Stage(RName.tosci_start, 0x109D77, 0x109D79, 0x12, 0x00,
                                      RName.tosci_conveyors, 0x12, 0x03,
                                      RName.tosci_conveyors, 0x109D5F, 0x109D61, None, None, 0x12, 0x04,
                                      0, [0x104A95, 0x104A9D, 0x104AA5],
                                      {IName.science_key_one: 1,
                                       IName.science_key_two: 1,
                                       IName.science_key_three: 1},
                                      {IName.roast_beef: 1}, 5,
                                      {IName.roast_chicken: 2}, 4, {},
                                      {IName.cross: 1}),

    "Tower of Sorcery":     CV64Stage(RName.tosor_main, 0x109D47, 0x109D49, 0x11, 0x00,
                                      RName.tosor_main, 0x11, 0x01,
                                      RName.tosor_main, 0x109D2F, 0x109D31, None, None, 0x11, 0x13,
                                      0, [0x104A8D],
                                      {},
                                      {IName.roast_beef: 1}, 6,
                                      {}, 0, {},
                                      {}),

    "Room of Clocks":       CV64Stage(RName.roc_main, None, None, 0x1B, 0x00,
                                      RName.roc_main, 0x1B, 0x02,
                                      RName.roc_main, 0x109EAF, 0x109EB1, None, None, 0x1B, 0x14,
                                      1, [0x104AC5],
                                      {},
                                      {IName.roast_beef: 1,
                                       IName.powerup: 2}, 0,
                                      {}, 0, {},
                                      {IName.holy_water: 1,
                                       IName.axe: 1}),

    "Clock Tower":          CV64Stage(RName.ct_start, None, None, 0x17, 0x00,
                                      RName.ct_middle, 0x17, 0x02,
                                      RName.ct_end, 0x109E37, 0x109E39, None, None, 0x17, 0x03,
                                      0, [0x104AB5, 0x104ABD],
                                      {IName.clocktower_key_one: 1,
                                       IName.clocktower_key_two: 1,
                                       IName.clocktower_key_three: 1},
                                      {}, 3,
                                      {IName.roast_chicken: 3,
                                       IName.roast_beef: 3}, 10, {},
                                      {IName.holy_water: 2,
                                       IName.cross: 1,
                                       IName.axe: 1,
                                       IName.knife: 1}),

    "Castle Keep":          CV64Stage(RName.ck_main, None, None, 0x14, 0x02,
                                      RName.ck_main, 0x14, 0x03,
                                      RName.ck_drac_chamber, None, None, None, None, None, None,
                                      2, [0x104AAD],
                                      {},
                                      {IName.healing_kit: 3}, 1,
                                      {}, 0, {},
                                      {})
}

vanilla_stage_order = ["Forest of Silence", "Castle Wall", "Villa", "Tunnel", "Underground Waterway", "Castle Center",
                       "Duel Tower", "Tower of Execution", "Tower of Science", "Tower of Sorcery", "Room of Clocks",
                       "Clock Tower", "Castle Keep"]

vanilla_stage_exits = {RName.forest_of_silence:    {"prev": None, "next": RName.castle_wall,
                                                    "alt": None, "position": 1, "path": " "},
                       RName.castle_wall:          {"prev": None, "next": RName.villa,
                                                    "alt": None, "position": 2, "path": " "},
                       RName.villa:                {"prev": None, "next": RName.tunnel,
                                                    "alt": RName.underground_waterway, "position": 3, "path": " "},
                       RName.tunnel:               {"prev": None, "next": RName.castle_center,
                                                    "alt": None, "position": 4, "path": " "},
                       RName.underground_waterway: {"prev": None, "next": RName.castle_center,
                                                    "alt": None, "position": 4, "path": "'"},
                       RName.castle_center:        {"prev": None, "next": RName.duel_tower,
                                                    "alt": RName.tower_of_science, "position": 5, "path": " "},
                       RName.duel_tower:           {"prev": RName.castle_center, "next": RName.tower_of_execution,
                                                    "alt": None, "position": 6, "path": " "},
                       RName.tower_of_execution:   {"prev": RName.duel_tower, "next": RName.room_of_clocks,
                                                    "alt": None, "position": 7, "path": " "},
                       RName.tower_of_science:     {"prev": RName.castle_center, "next": RName.tower_of_sorcery,
                                                    "alt": None, "position": 6, "path": "'"},
                       RName.tower_of_sorcery:     {"prev": RName.tower_of_science, "next": RName.room_of_clocks,
                                                    "alt": None, "position": 7, "path": "'"},
                       RName.room_of_clocks:       {"prev": None, "next": RName.clock_tower,
                                                    "alt": None, "position": 8, "path": " "},
                       RName.clock_tower:          {"prev": None, "next": RName.castle_keep,
                                                    "alt": None, "position": 9, "path": " "},
                       RName.castle_keep:          {"prev": None, "next": None,
                                                    "alt": None, "position": 10, "path": " "}}

# def set_custom_stage_order(multiworld, player, active_stage_list, active_stage_exits):
#     valid = True
#     branching_valid = True
#     if len(multiworld.custom_stage_order[player]) == 12:
#         for stage in multiworld.custom_stage_order[player]:


def shuffle_stages(multiworld, player, active_stage_list, active_stage_exits, stage_1_blacklist):
    new_stage_order = []
    villa_cc_ids = [2, 3]
    alt_villa_stage = []
    alt_cc_stages = []

    active_stage_list.remove(RName.castle_keep)
    total_stages = len(active_stage_list)

    # If there are branching stages, remove Villa and CC from the list and determine their placements first.
    if multiworld.character_stages[player].value == 0:
        villa_cc_ids = multiworld.random.sample(range(0, 6), 2)
        active_stage_list.remove(RName.villa)
        active_stage_list.remove(RName.castle_center)

    for i in range(total_stages):
        # If we're on Villa or CC's ID while in branching stage mode, put the respective stage in the slot.
        if multiworld.character_stages[player].value == 0 and i == villa_cc_ids[0] and \
                RName.villa not in new_stage_order:
            new_stage_order.append(RName.villa)
            villa_cc_ids[1] += 2
        elif multiworld.character_stages[player].value == 0 and i == villa_cc_ids[1] and \
                RName.castle_center not in new_stage_order:
            new_stage_order.append(RName.castle_center)
            villa_cc_ids[0] += 4
        else:
            # If neither of the above are true, draw a random stage from the active list and delete it from there.
            new_stage_order.append(active_stage_list[multiworld.random.randint(0, len(active_stage_list) - 1)])
            # If the grabbed Stage 1 is blacklisted, then keep trying until a non-blacklisted one is drawn.
            while i == 0 and new_stage_order[0] in stage_1_blacklist:
                new_stage_order[i] = active_stage_list[multiworld.random.randint(0, len(active_stage_list) - 1)]
            active_stage_list.remove(new_stage_order[i])

        # If we're looking at an alternate stage slot, put the stage in one of these lists to indicate it as such
        if multiworld.character_stages[player].value == 0:
            if i - 2 >= 0:
                if new_stage_order[i - 2] == RName.villa:
                    alt_villa_stage.append(new_stage_order[i])
            if i - 3 >= 0:
                if new_stage_order[i - 3] == RName.castle_center:
                    alt_cc_stages.append(new_stage_order[i])
            if i - 4 >= 0:
                if new_stage_order[i - 4] == RName.castle_center:
                    alt_cc_stages.append(new_stage_order[i])

    new_stage_order.append(RName.castle_keep)
    active_stage_list.extend(new_stage_order)

    # Update the dictionary of stage exits
    current_stage_number = 1
    for i in range(len(active_stage_list)):
        # Stage position number and alternate path indicator
        active_stage_exits[active_stage_list[i]]["position"] = current_stage_number
        if active_stage_list[i] in alt_villa_stage + alt_cc_stages:
            active_stage_exits[active_stage_list[i]]["path"] = "'"
        else:
            active_stage_exits[active_stage_list[i]]["path"] = " "

        # Previous stage
        if active_stage_exits[active_stage_list[i]]["prev"]:
            if i - 1 < 0:
                active_stage_exits[active_stage_list[i]]["prev"] = "Menu"
            elif multiworld.character_stages[player].value == 0:
                if active_stage_list[i - 1] == alt_villa_stage[0] or active_stage_list[i] == alt_villa_stage[0]:
                    active_stage_exits[active_stage_list[i]]["prev"] = active_stage_list[i - 2]
                elif active_stage_list[i - 1] == alt_cc_stages[1] or active_stage_list[i] == alt_cc_stages[0]:
                    active_stage_exits[active_stage_list[i]]["prev"] = active_stage_list[i - 3]
                else:
                    active_stage_exits[active_stage_list[i]]["prev"] = active_stage_list[i - 1]
            else:
                active_stage_exits[active_stage_list[i]]["prev"] = active_stage_list[i - 1]

        # Next stage
        if active_stage_exits[active_stage_list[i]]["next"]:
            if multiworld.character_stages[player].value == 0:
                if active_stage_list[i + 1] == alt_villa_stage[0]:
                    active_stage_exits[active_stage_list[i]]["next"] = active_stage_list[i + 2]
                    current_stage_number -= 1
                elif active_stage_list[i + 1] == alt_cc_stages[0]:
                    active_stage_exits[active_stage_list[i]]["next"] = active_stage_list[i + 3]
                    current_stage_number -= 2
                else:
                    active_stage_exits[active_stage_list[i]]["next"] = active_stage_list[i + 1]
            else:
                active_stage_exits[active_stage_list[i]]["next"] = active_stage_list[i + 1]

        # Alternate next stage
        if active_stage_exits[active_stage_list[i]]["alt"]:
            if multiworld.character_stages[player].value == 0:
                if active_stage_list[i] == RName.villa:
                    active_stage_exits[active_stage_list[i]]["alt"] = alt_villa_stage[0]
                else:
                    active_stage_exits[active_stage_list[i]]["alt"] = alt_cc_stages[0]
            else:
                active_stage_exits[active_stage_list[i]]["alt"] = active_stage_list[i + 1]

        current_stage_number += 1
