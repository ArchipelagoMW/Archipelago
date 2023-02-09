import typing

from .Names import RegionName


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
    end_scene_id: int
    end_spawn_id: int

    stage_number_offset_list: typing.List[int]

    def __init__(self, start_region_name: str, startzone_map_offset: int, startzone_spawn_offset: int, start_map_id: int,
                 start_spawn_id: int, mid_region_name: str, mid_map_id: int, mid_spawn_id: int, end_region_name: str,
                 endzone_map_offset: int, endzone_spawn_offset: int, end_scene_id: int, end_spawn_id: int,
                 stage_number_offset_list: list):
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
        self.end_scene_id = end_scene_id
        self.end_spawn_id = end_spawn_id

        self.stage_number_offset_list = stage_number_offset_list


stage_dict = {
    "Forest of Silence":    CV64Stage(RegionName.forest_start, 0xFFFFFF, 0xFFFFFF, 0x00, 0x00,
                                      RegionName.forest_mid, 0x00, 0x04,
                                      RegionName.forest_end, 0xB6302F, 0xB6302B, 0x00, 0x01,
                                      [0x1049C5, 0x1049CD, 0x1049D5]),
    "Castle Wall":          CV64Stage(RegionName.cw_start, 0xFFFFFF, 0xFFFFFF, 0x02, 0x00,
                                      RegionName.cw_start, 0x02, 0x07,
                                      RegionName.cw_exit, 0x109A5F, 0x109A61, 0x02, 0x10,
                                      [0x1049DD, 0x1049E5, 0x1049ED]),
    "Villa":                CV64Stage(RegionName.villa_start, 0xFFFFFF, 0xFFFFFF, 0x03, 0x00,
                                      RegionName.villa_storeroom, 0x05, 0x04,
                                      RegionName.villa_crypt, 0x0D9DA3, 0x109E81, 0x1A, 0x03,
                                      [0x1049F5, 0x1049FD, 0x104A05, 0x104A0D]),
    "Tunnel":               CV64Stage(RegionName.tunnel_start, 0xFFFFFF, 0xFFFFFF, 0x07, 0x00,
                                      RegionName.tunnel_end, 0x07, 0x03,
                                      RegionName.tunnel_end, 0x109B4F, 0x109B51, 0x07, 0x11,
                                      [0x104A15, 0x104A1D, 0x104A25, 0x104A2D]),
    "Underground Waterway": CV64Stage(RegionName.uw_main, 0xFFFFFF, 0xFFFFFF, 0x08, 0x00,
                                      RegionName.uw_main, 0x08, 0x03,
                                      RegionName.uw_end, 0x109B67, 0x109B69, 0x08, 0x01,
                                      [0x104A35, 0x104A3D]),
    "Castle Center":        CV64Stage(RegionName.cc_main, 0xFFFFFF, 0xFFFFFF, 0x19, 0x00,
                                      RegionName.cc_main, 0x0E, 0x03,
                                      RegionName.cc_elev_top, 0x109CB7, 0x109CB9, 0x0F, 0x02,
                                      [0x104A45, 0x104A4D, 0x104A55, 0x104A5D, 0x104A65, 0x104A6D, 0x104A75]),
    "Duel Tower":           CV64Stage(RegionName.duel_tower, 0x109DA7, 0x109DA9, 0x13, 0x00,
                                      RegionName.duel_tower, 0x13, 0x15,
                                      RegionName.duel_tower, 0x109D8F, 0x109D91, 0x13, 0x01,
                                      [0x104ACD]),
    "Tower of Execution":   CV64Stage(RegionName.toe_main, 0x109D17, 0x109D19, 0x10, 0x00,
                                      RegionName.toe_main, 0x10, 0x02,
                                      RegionName.toe_main, 0x109CFF, 0x109D01, 0x10, 0x12,
                                      [0x104A7D, 0x104A85]),
    "Tower of Science":     CV64Stage(RegionName.tosci_start, 0x109D77, 0x109D79, 0x12, 0x00,
                                      RegionName.tosci_conveyors, 0x12, 0x03,
                                      RegionName.tosci_conveyors, 0x109D5F, 0x109D61, 0x12, 0x04,
                                      [0x104A95, 0x104A9D, 0x104AA5]),
    "Tower of Sorcery":     CV64Stage(RegionName.tower_of_sorcery, 0x109D47, 0x109D49, 0x11, 0x00,
                                      RegionName.tower_of_sorcery, 0x11, 0x01,
                                      RegionName.tower_of_sorcery, 0x109D2F, 0x109D31, 0x11, 0x13,
                                      [0x104A8D]),
    "Room of Clocks":       CV64Stage(RegionName.room_of_clocks, 0xFFFFFF, 0xFFFFFF, 0x1B, 0x00,
                                      RegionName.room_of_clocks, 0x1B, 0x02,
                                      RegionName.room_of_clocks, 0x109EAF, 0x109EB1, 0x1B, 0x14,
                                      [0x104AC5]),
    "Clock Tower":          CV64Stage(RegionName.ct_start, 0xFFFFFF, 0xFFFFFF, 0x17, 0x00,
                                      RegionName.ct_middle, 0x17, 0x02,
                                      RegionName.ct_end, 0x109E37, 0x109E39, 0x17, 0x03,
                                      [0x104AB5, 0x104ABD]),
    "Castle Keep":          CV64Stage(RegionName.castle_keep, 0xFFFFFF, 0xFFFFFF, 0x14, 0x02,
                                      RegionName.castle_keep, 0x14, 0x03,
                                      RegionName.drac_chamber, 0xFFFFFF, 0xFFFFFF, 0xFF, 0xFF,
                                      [0x104AAD])
}

vanilla_stage_order = ["Forest of Silence", "Castle Wall", "Villa", "Tunnel", "Underground Waterway", "Castle Center",
                       "Duel Tower", "Tower of Execution", "Tower of Science", "Tower of Sorcery", "Room of Clocks",
                       "Clock Tower", "Castle Keep"]
