import typing

from .Names import RName, IName

vanilla_stage_order = ["Forest of Silence", "Castle Wall", "Villa", "Tunnel", "Underground Waterway", "Castle Center",
                       "Duel Tower", "Tower of Execution", "Tower of Science", "Tower of Sorcery", "Room of Clocks",
                       "Clock Tower", "Castle Keep"]


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
    altzone_map_offset: int
    endzone_spawn_offset: int
    end_map_id: int
    end_spawn_id: int

    stages_per_path: int
    stage_number_offset_list: typing.List[int]

    stage_item_counts: typing.Dict[str, int]
    stage_junk_count: int

    def __init__(self, start_region_name: str, startzone_map_offset: typing.Optional[int], startzone_spawn_offset:
                 typing.Optional[int], start_map_id: int, start_spawn_id: int, mid_region_name: str, mid_map_id: int,
                 mid_spawn_id: int, end_region_name: str, endzone_map_offset: typing.Optional[int],
                 endzone_spawn_offset: typing.Optional[int], altzone_map_offset: typing.Optional[int],
                 end_map_id: typing.Optional[int], end_spawn_id: typing.Optional[int],  stages_per_path: int,
                 stage_number_offset_list: list, stage_item_counts: dict, stage_junk_count: int):
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
        self.end_map_id = end_map_id
        self.end_spawn_id = end_spawn_id

        self.stages_per_path = stages_per_path
        self.stage_number_offset_list = stage_number_offset_list

        self.stage_item_counts = stage_item_counts
        self.stage_junk_count = stage_junk_count


all_stages = {
    RName.forest_of_silence:    CV64Stage(RName.forest_start, None, None, 0x00, 0x00,
                                          RName.forest_mid, 0x00, 0x04,
                                          RName.forest_end, 0xB6302F, 0xB6302B, None, 0x00, 0x01,
                                          0, [0x1049C5, 0x1049CD, 0x1049D5],
                                          {IName.roast_chicken: 4,
                                           IName.roast_beef: 3,
                                           IName.powerup: 1,
                                           IName.sun_card: 2,
                                           IName.moon_card: 1}, 12),

    RName.castle_wall:          CV64Stage(RName.cw_start, None, None, 0x02, 0x00,
                                          RName.cw_start, 0x02, 0x07,
                                          RName.cw_exit, 0x109A5F, 0x109A61, None, 0x02, 0x10,
                                          0, [0x1049DD, 0x1049E5, 0x1049ED],
                                          {IName.roast_chicken: 2,
                                           IName.roast_beef: 1,
                                           IName.powerup: 1,
                                           IName.sun_card: 1,
                                           IName.moon_card: 2,
                                           IName.left_tower_key: 1}, 2),

    RName.villa:                CV64Stage(RName.villa_start, None, None, 0x03, 0x00,
                                          RName.villa_storeroom, 0x05, 0x04,
                                          RName.villa_crypt, 0xD9DA3, 0x109E81, 0xD9DAB, 0x1A, 0x03,
                                          1, [0x1049F5, 0x1049FD, 0x104A05, 0x104A0D],
                                          {IName.roast_chicken: 6,
                                           IName.roast_beef: 5,
                                           IName.purifying: 9,
                                           IName.powerup: 1,
                                           IName.sun_card: 1,
                                           IName.moon_card: 2,
                                           IName.storeroom_key: 1,
                                           IName.archives_key: 1,
                                           IName.garden_key: 1,
                                           IName.copper_key: 1}, 28),

    RName.tunnel:               CV64Stage(RName.tunnel_start, None, None, 0x07, 0x00,
                                          RName.tunnel_end, 0x07, 0x03,
                                          RName.tunnel_end, 0x109B4F, 0x109B51, None, 0x07, 0x11,
                                          0, [0x104A15, 0x104A1D, 0x104A25, 0x104A2D],
                                          {IName.roast_chicken: 2,
                                           IName.roast_beef: 3,
                                           IName.cure_ampoule: 2,
                                           IName.powerup: 1,
                                           IName.sun_card: 2,
                                           IName.moon_card: 1}, 14),

    RName.underground_waterway: CV64Stage(RName.uw_main, None, None, 0x08, 0x00,
                                          RName.uw_main, 0x08, 0x03,
                                          RName.uw_end, 0x109B67, 0x109B69, None, 0x08, 0x01,
                                          0, [0x104A35, 0x104A3D],
                                          {IName.roast_chicken: 1,
                                           IName.cure_ampoule: 1,
                                           IName.powerup: 1}, 3),

    RName.castle_center:        CV64Stage(RName.cc_main, None, None, 0x19, 0x00,
                                          RName.cc_main, 0x0E, 0x03,
                                          RName.cc_elev_top, 0x109CB7, 0x109CB9, 0x109CCF, 0x0F, 0x02,
                                          2, [0x104A45, 0x104A4D, 0x104A55, 0x104A5D, 0x104A65, 0x104A6D, 0x104A75],
                                          {IName.roast_chicken: 4,
                                           IName.roast_beef: 5,
                                           IName.healing_kit: 1,
                                           IName.purifying: 4,
                                           IName.cure_ampoule: 2,
                                           IName.powerup: 2,
                                           IName.sun_card: 2,
                                           IName.moon_card: 1,
                                           IName.magical_nitro: 2,
                                           IName.mandragora: 2,
                                           IName.chamber_key: 1}, 25),

    RName.duel_tower:           CV64Stage(RName.dt_main, 0x109DA7, 0x109DA9, 0x13, 0x00,
                                          RName.dt_main, 0x13, 0x15,
                                          RName.dt_main, 0x109D8F, 0x109D91, None, 0x13, 0x01,
                                          0, [0x104ACD],
                                          {IName.roast_chicken: 1,
                                           IName.roast_beef: 2,
                                           IName.powerup: 1}, 0),

    RName.tower_of_execution:   CV64Stage(RName.toe_main, 0x109D17, 0x109D19, 0x10, 0x00,
                                          RName.toe_main, 0x10, 0x02,
                                          RName.toe_main, 0x109CFF, 0x109D01, None, 0x10, 0x12,
                                          0, [0x104A7D, 0x104A85],
                                          {IName.roast_chicken: 1,
                                           IName.roast_beef: 1,
                                           IName.execution_key: 1}, 3),

    RName.tower_of_science:     CV64Stage(RName.tosci_start, 0x109D77, 0x109D79, 0x12, 0x00,
                                          RName.tosci_conveyors, 0x12, 0x03,
                                          RName.tosci_conveyors, 0x109D5F, 0x109D61, None, 0x12, 0x04,
                                          0, [0x104A95, 0x104A9D, 0x104AA5],
                                          {IName.roast_beef: 1,
                                           IName.science_key_one: 1,
                                           IName.science_key_two: 1,
                                           IName.science_key_three: 1}, 5),

    RName.tower_of_sorcery:     CV64Stage(RName.tosor_main, 0x109D47, 0x109D49, 0x11, 0x00,
                                          RName.tosor_main, 0x11, 0x01,
                                          RName.tosor_main, 0x109D2F, 0x109D31, None, 0x11, 0x13,
                                          0, [0x104A8D],
                                          {IName.roast_beef: 1}, 6),

    RName.room_of_clocks:       CV64Stage(RName.roc_main, None, None, 0x1B, 0x00,
                                          RName.roc_main, 0x1B, 0x02,
                                          RName.roc_main, 0x109EAF, 0x109EB1, None, 0x1B, 0x14,
                                          0, [0x104AC5],
                                          {IName.roast_beef: 1,
                                           IName.powerup: 2}, 0),

    RName.clock_tower:          CV64Stage(RName.ct_start, None, None, 0x17, 0x00,
                                          RName.ct_middle, 0x17, 0x02,
                                          RName.ct_end, 0x109E37, 0x109E39, None, 0x17, 0x03,
                                          0, [0x104AB5, 0x104ABD],
                                          {IName.clocktower_key_one: 1,
                                           IName.clocktower_key_two: 1,
                                           IName.clocktower_key_three: 1}, 3),

    RName.castle_keep:          CV64Stage(RName.ck_main, None, None, 0x14, 0x02,
                                          RName.ck_main, 0x14, 0x03,
                                          RName.ck_drac_chamber, None, None, None, None, None,
                                          0, [0x104AAD],
                                          {IName.healing_kit: 3}, 1)
}


def get_stage_exits(multiworld, full_stage_list, main_stage_list, reinhardt_stage_list, carrie_stage_list):
    stage_exits_dict = {}
    prev_stage = None
    next_stage = None
    alt_stage = None

    for i in range(0, len(full_stage_list)):
        # Previous stage
        if all_stages[full_stage_list[i]].startzone_map_offset and i - 1 >= 0:
            if reinhardt_stage_list and carrie_stage_list:
                if full_stage_list[i - 1] == RName.villa:
                    prev_stage = reinhardt_stage_list[0]
                elif full_stage_list[i - 1] == RName.castle_center:
                    prev_stage = reinhardt_stage_list[2]
                elif full_stage_list[i] == reinhardt_stage_list[0] or full_stage_list[i] == carrie_stage_list[0]:
                    prev_stage = RName.villa
                elif full_stage_list[i] == reinhardt_stage_list[1] or full_stage_list[i] == carrie_stage_list[1]:
                    prev_stage = RName.castle_center
                elif full_stage_list[i] in main_stage_list:
                    prev_stage = main_stage_list[full_stage_list[i]].index() - 1
                else:
                    prev_stage = full_stage_list[i - 1]
            else:
                prev_stage = full_stage_list[i - 1]
            # multiworld.offsets_to_ids[all_stages[full_stage_list[i]].startzone_map_offset] = all_stages[prev_stage].\
                # end_map_id
            # multiworld.offsets_to_ids[all_stages[full_stage_list[i]].startzone_spawn_offset] = all_stages[prev_stage].\
                # end_spawn_id

        # Next stage
        if all_stages[full_stage_list[i]].endzone_map_offset:
            if reinhardt_stage_list and carrie_stage_list:
                if full_stage_list[i] == RName.villa:
                    next_stage = reinhardt_stage_list[0]
                elif full_stage_list[i] == RName.castle_center:
                    next_stage = reinhardt_stage_list[1]
                elif full_stage_list[i] == reinhardt_stage_list[0] or full_stage_list[i] == carrie_stage_list[0]:
                    next_stage = full_stage_list[full_stage_list.index(RName.villa) + 1]
                elif full_stage_list[i] == reinhardt_stage_list[2] or full_stage_list[i] == carrie_stage_list[2]:
                    next_stage = full_stage_list[full_stage_list.index(RName.castle_center) + 1]
                elif full_stage_list[i] in main_stage_list:
                    prev_stage = main_stage_list[full_stage_list[i]].index() + 1
                else:
                    next_stage = full_stage_list[i + 1]
            else:
                next_stage = full_stage_list[i + 1]
            # multiworld.offsets_to_ids[all_stages[full_stage_list[i]].endzone_map_offset] = all_stages[next_stage].\
                # start_map_id
            # multiworld.offsets_to_ids[all_stages[full_stage_list[i]].endzone_spawn_offset] = all_stages[next_stage].\
                # start_spawn_id

        # Alternate next stage
        if all_stages[full_stage_list[i]].altzone_map_offset:
            if reinhardt_stage_list and carrie_stage_list:
                if full_stage_list[i] == RName.villa:
                    alt_stage = carrie_stage_list[0]
                else:
                    alt_stage = carrie_stage_list[1]
            else:
                alt_stage = full_stage_list[i + 1]
            # multiworld.offsets_to_ids[all_stages[full_stage_list[i]].altzone_map_offset] = all_stages[alt_stage].\
                # start_map_id

        stage_exits_dict[full_stage_list[i]] = [prev_stage, next_stage, alt_stage]

    return stage_exits_dict
