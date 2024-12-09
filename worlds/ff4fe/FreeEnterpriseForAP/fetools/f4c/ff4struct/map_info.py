from .bitutil import *

class MapInfo:
    def __init__(self):
        self.battle_background = 0
        self.can_warp = False
        self.can_exit = False
        self.battle_background_alt_palette = False
        self.magnetic = False
        self.grid = 0
        self.tileset = 0
        self.placements = 0
        self.border_tile = 0
        self.border_no_exit = False
        self.palette = 0
        self.npc_palette_0 = 0
        self.npc_palette_1 = 0
        self.music = 0
        self.bg_grid = 0
        self.bg_translucent = False
        self.bg_scroll_vertical = False
        self.bg_scroll_horizontal = False
        self.bit75 = False
        self.bg_direction = 0
        self.bg_speed = 0
        self.underground_map_grid = False
        self.bits81to86 = 0
        self.underground_npcs = False
        self.name = 0
        self.treasure_index = 0

    def encode(self):
        return [
            pack_byte('4bbbb', self.battle_background, self.can_warp, self.can_exit, self.battle_background_alt_palette, self.magnetic),
            self.grid,
            self.tileset,
            self.placements,
            pack_byte('7b', self.border_tile, self.border_no_exit),
            self.palette,
            pack_byte('44', self.npc_palette_0, self.npc_palette_1),
            self.music,
            self.bg_grid,
            pack_byte('bbbb22', self.bg_translucent, self.bg_scroll_vertical, self.bg_scroll_horizontal, self.bit75, self.bg_direction, self.bg_speed),
            pack_byte('b6b', self.underground_map_grid, self.bits81to86, self.underground_npcs),
            self.name,
            self.treasure_index
        ]


def decode(byte_list):
    mi = MapInfo()
    mi.battle_background, mi.can_warp, mi.can_exit, mi.battle_background_alt_palette, mi.magnetic = unpack_byte('4bbbb', byte_list[0])
    mi.grid = byte_list[1]
    mi.tileset = byte_list[2]
    mi.placements = byte_list[3]
    mi.border_tile, mi.border_no_exit = unpack_byte('7b', byte_list[4])
    mi.palette = byte_list[5]
    mi.npc_palette_0, mi.npc_palette_1 = unpack_byte('44', byte_list[6])
    mi.music = byte_list[7]
    mi.bg_grid = byte_list[8]
    mi.bg_translucent, mi.bg_scroll_vertical, mi.bg_scroll_horizontal, mi.bit75, mi.bg_direction, mi.bg_speed = unpack_byte('bbbb22', byte_list[9])
    mi.underground_map_grid, mi.bits81to86, mi.underground_npcs = unpack_byte('b6b', byte_list[10])
    mi.name = byte_list[11]
    mi.treasure_index = byte_list[12]
    return mi

