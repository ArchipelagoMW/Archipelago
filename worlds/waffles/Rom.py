import Utils
import settings
from worlds.AutoWorld import AutoWorldRegister
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension
from .Aesthetics import generate_shuffled_ow_palettes, generate_curated_level_palette_data, generate_curated_map_palette_data, generate_shuffled_sfx
from .Levels import level_info_dict, full_bowser_rooms, standard_bowser_rooms, submap_boss_rooms, ow_boss_rooms
from .Names.TextBox import generate_goal_text, title_text_mapping, generate_text_box
from .Teleports import handle_teleport_shuffle, handle_transition_shuffle, handle_silent_events
from .SNESGraphics import copy_gfx_tiles, decompress_gfx, copy_sprite_tiles, convert_3bpp, convert_name_to_4bpp
from BaseClasses import ItemClassification
from argparse import Namespace

USHASH = 'cdd3c8c37322978ca8669b34bc89c804'

import hashlib
import os
import typing
import json
import random

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import WaffleWorld

ability_rom_data = {
    #0xBC0003: [[0x1F1C, 0x7]], # Run         0x80
    0xBC0004: [[0x1F1C, 0x6]], # Carry       0x40
    0xBC0006: [[0x1F1C, 0x3]], # Spin Jump   0x08
    0xBC0007: [[0x1F1C, 0x5]], # Climb       0x20
    0xBC0009: [[0x1F1C, 0x4]], # P-Switch    0x10
    #0xBC000A: [[]]
    0xBC000B: [[0x1F2D, 0x3]], # P-Balloon   0x08
    0xBC0020: [[0x43E2, 0x1]], # Extra Defense
    0xBC0021: [[0x43E3, 0x1]], # Midway Point
    0xBC0023: [[0x43E5, 0x1]], # Item Box
    0xBC0008: [[0x43E6, 0x1], [0x43E6, 0x0]], # Yoshi
    0xBC0003: [[0x43E7, 0x1], [0x43E7, 0x0]], # Run
    0xBC0005: [[0x43E0, 0x1], [0x43E0, 0x0]], # Swim
}

progressive_items = {
    #0xBC0005: [0x03E0, 2], # Swim
    0xBC0025: [0x03E7, 2], # Run
    0xBC0024: [0x03E6, 2], # Yoshi
    0xBC000D: [0x03E1, 9], # Super Star
    0xBC0022: [0x03E4, 3], # Better Timer
}

icon_rom_data = {
    0xBC0002: [0x480C], # Yoshi Egg
    0xBC0048: [0x480E], # Trap Repellent

    0xBC0017: [0x4804], # 1 coin
    0xBC0018: [0x4806], # 5 coins
    0xBC0019: [0x4808], # 10 coins
    0xBC001A: [0x480A], # 50 coins

    0xBC0001: [0x4810], # Heart

    0xBC0040: [0x4812], # Mushroom
    0xBC0041: [0x4814], # Fire Flower
    0xBC0042: [0x4816], # Feather
    0xBC0043: [0x4818], # Star
    0xBC0044: [0x481A], # Green Yoshi
    0xBC0045: [0x481C], # Red Yoshi
    0xBC0046: [0x481E], # Blue Yoshi
    0xBC0047: [0x4820], # Yellow Yoshi
}
    
item_rom_data = {
    0xBC000E: [0x1F28, 0x1,  0x1C], # Yellow Switch Palace
    0xBC000F: [0x1F27, 0x1,  0x1C], # Green Switch Palace
    0xBC0010: [0x1F2A, 0x1,  0x1C], # Red Switch Palace
    0xBC0011: [0x1F29, 0x1,  0x1C], # Blue Switch Palace
    0xBC001B: [0x1F1E, 0x80, 0x39]  # Special Zone Clear
}

trap_rom_data = {
    0xBC0080: [0x4308, 0x1, 0x0E],  # Ice Trap
    0xBC0081: [0x18BD, 0x7F, 0x18], # Stun Trap
    0xBC0083: [0x0F31, 0x1],        # Timer Trap
    0xBC0084: [0x4300, 0x1, 0x44],  # Reverse controls trap
    0xBC0085: [0x4302, 0x1],        # Thwimp Trap
    0xBC0086: [0x4305, 0x1],        # Fishin' Boo Trap
    0xBC0087: [0x430A, 0x1],        # Screen Flip Trap
    0xBC0088: [0x430C, 15],         # Sticky Floor Trap
    0xBC0089: [0x430E, 0x1],        # Sticky Hands Trap
    0xBC008A: [0x4310, 0x1],        # Pixelate Trap
    0xBC008B: [0x4312, 0x1],        # Spotlight Trap
    0xBC008C: [0x4318, 0x1],        # Bullet Time Trap
    0xBC008D: [0x431D, 0x1],        # Invisibility Trap
    0xBC008E: [0x0DC2, 0x00, 0x44], # Empty Item Box Trap
}

visible_to_invisible_level_tiles = {
    0x66: 0x6E,
    0x68: 0x70,
    0x6A: 0x72,
    0x6C: 0x74,
    0x63: 0x7A,
}

invisible_to_visible_level_tiles = {
    0x6E: 0x66,
    0x70: 0x68,
    0x72: 0x6A,
    0x74: 0x6C,
    0x7A: 0x63,
}

starting_positions_data = {
    0: [                # Yoshi's house
        0x01,           # Initial Submap (Mario)
        0x00,           # Initial Submap (Luigi)
        0x00,           # Starting level ID
        0x0002,         # Initial animation??? (Mario)
        0x0000,         # Initial animation??? (Luigi)
        0x0068,0x0078,  # Initial X/Y position (Mario)
        0x0000,0x0000,  # Initial X/Y position (Luigi)
        0x0006,0x0007,  # Initial X/Y position / 0x10 (Mario)
        0x0000,0x0000,  # Initial X/Y position / 0x10 (Luigi)
    ],
    1: [                # Donut Plains
        0x00,           # Initial Submap (Mario)
        0x00,           # Initial Submap (Luigi)
        0x07,           # Starting level ID
        0x0002,         # Initial animation??? (Mario)
        0x0002,         # Initial animation??? (Luigi)
        0x0058,0x0118,  # Initial X/Y position (Mario)
        0x0000,0x0000,  # Initial X/Y position (Luigi)
        0x0005,0x0011,  # Initial X/Y position / 0x10 (Mario)
        0x0000,0x0000,  # Initial X/Y position / 0x10 (Luigi)
    ],
    2: [                # Vanilla Dome
        0x02,           # Initial Submap (Mario)
        0x00,           # Initial Submap (Luigi)
        0x13,           # Starting level ID
        0x0002,         # Initial animation??? (Mario)
        0x0000,         # Initial animation??? (Luigi)
        0x0058,0x0128,  # Initial X/Y position (Mario)
        0x0000,0x0000,  # Initial X/Y position (Luigi)
        0x0005,0x0012,  # Initial X/Y position / 0x10 (Mario)
        0x0000,0x0000,  # Initial X/Y position / 0x10 (Luigi)
    ],
    3: [                # Forest of Illusion
        0x03,           # Initial Submap (Mario)
        0x00,           # Initial Submap (Luigi)
        0x26,           # Starting level ID
        0x0002,         # Initial animation??? (Mario)
        0x0000,         # Initial animation??? (Luigi)
        0x0088,0x0178,  # Initial X/Y position (Mario)
        0x0000,0x0000,  # Initial X/Y position (Luigi)
        0x0008,0x0017,  # Initial X/Y position / 0x10 (Mario)
        0x0000,0x0000,  # Initial X/Y position / 0x10 (Luigi)
    ],
    4: [                # Special Zone
        0x05,           # Initial Submap (Mario)
        0x00,           # Initial Submap (Luigi)
        0x4F,           # Starting level ID
        0x0002,         # Initial animation??? (Mario)
        0x0000,         # Initial animation??? (Luigi)
        0x0138,0x0138,  # Initial X/Y position (Mario)
        0x0000,0x0000,  # Initial X/Y position (Luigi)
        0x0013,0x0013,  # Initial X/Y position / 0x10 (Mario)
        0x0000,0x0000,  # Initial X/Y position / 0x10 (Luigi)
    ],
}

class WafflePatchExtension(APPatchExtension):
    game = "SMW: Spicy Mycena Waffles"

    @staticmethod
    def handle_uncompressed_graphics(caller: APProcedurePatch, rom: bytes) -> bytes:
        # Decompresses and moves into a expanded region the player, yoshi and animated graphics
        # This should make swapping the graphics a lot easier.
        # Maybe I should look into making a 32x32 version at some point...
        # It also moves some 8x8 tiles in GFX00, thus making some free space for indicators and other stuff
        # in VRAM during gameplay, will come super handy later.
        # 
        # FOR FUTURE REFERENCE
        # Player graphics are now located at 0xE0000
        # Player auxiliary tiles are now located at 0xE6000
        # Yoshi graphics are now located at 0xE8800
        import bsdiff4
        from .data import sprite_gfx_data

        rom = bytearray(rom)

        SMW_COMPRESSED_GFX_32 = 0x40000
        SMW_COMPRESSED_GFX_33 = 0x43FC0

        SMW_COMPRESSED_GFX_00 = 0x459F9
        SMW_COMPRESSED_GFX_01 = 0x46231
        SMW_COMPRESSED_GFX_02 = 0x46CBB
        SMW_COMPRESSED_GFX_03 = 0x47552
        SMW_COMPRESSED_GFX_04 = 0x47F7D
        SMW_COMPRESSED_GFX_05 = 0x48963
        SMW_COMPRESSED_GFX_06 = 0x4936C
        SMW_COMPRESSED_GFX_09 = 0x4AFA1
        SMW_COMPRESSED_GFX_0A = 0x4BA15
        SMW_COMPRESSED_GFX_0B = 0x4C39C
        SMW_COMPRESSED_GFX_0E = 0x4DDCB
        SMW_COMPRESSED_GFX_11 = 0x4F7AF
        SMW_COMPRESSED_GFX_12 = 0x4FFBD
        SMW_COMPRESSED_GFX_13 = 0x50910
        SMW_COMPRESSED_GFX_20 = 0x576A1
        SMW_COMPRESSED_GFX_23 = 0x591CA
        SMW_COMPRESSED_GFX_24 = 0x59AE5
        SMW_COMPRESSED_GFX_25 = 0x5A3B5

        SMW_COMPRESSED_GFX_10 = 0x4EF1E
        SMW_COMPRESSED_GFX_28 = 0x5C06C

        compressed_graphics = {
            0x00: [SMW_COMPRESSED_GFX_00, 2104, "3bpp"],
            0x01: [SMW_COMPRESSED_GFX_01, 2698, "3bpp"],
            0x02: [SMW_COMPRESSED_GFX_02, 2199, "3bpp"],
            0x03: [SMW_COMPRESSED_GFX_03, 2603, "3bpp"],
            0x04: [SMW_COMPRESSED_GFX_04, 2534, "3bpp"],
            0x05: [SMW_COMPRESSED_GFX_05, 2569, "3bpp"],
            0x06: [SMW_COMPRESSED_GFX_06, 2468, "3bpp"],
            0x09: [SMW_COMPRESSED_GFX_09, 2676, "3bpp"],
            0x0A: [SMW_COMPRESSED_GFX_0A, 2439, "3bpp"],
            0x0B: [SMW_COMPRESSED_GFX_0B, 2503, "3bpp"],
            0x0E: [SMW_COMPRESSED_GFX_0E, 2330, "3bpp"],
            0x11: [SMW_COMPRESSED_GFX_11, 2062, "3bpp"],
            0x12: [SMW_COMPRESSED_GFX_12, 2387, "3bpp"],
            0x13: [SMW_COMPRESSED_GFX_13, 2616, "3bpp"],
            0x20: [SMW_COMPRESSED_GFX_20, 2244, "3bpp"],
            0x23: [SMW_COMPRESSED_GFX_23, 2331, "3bpp"],
            0x24: [SMW_COMPRESSED_GFX_24, 2256, "3bpp"],
            0x25: [SMW_COMPRESSED_GFX_25, 2668, "3bpp"],
            0x10: [SMW_COMPRESSED_GFX_10, 2193, "3bpp"],
            0x28: [SMW_COMPRESSED_GFX_28, 1591, "2bpp"],
            0x32: [SMW_COMPRESSED_GFX_32, 16320, "4bpp"],
            0x33: [SMW_COMPRESSED_GFX_33, 6713, "3bpp"],
        }

        raw_sprite_graphics = bytearray()

        for slot, data in compressed_graphics.items():
            start = data[0]
            end = start + data[1]
            compressed_gfx = rom[start:end]
            if data[2] == "3bpp":
                raw_sprite_graphics += convert_3bpp(decompress_gfx(compressed_gfx))
                if slot == 0x33:
                    decompressed_animated_gfx = convert_3bpp(decompress_gfx(compressed_gfx))
            elif slot == 0x32:
                decompressed_player_gfx = decompress_gfx(compressed_gfx)
            else:
                raw_sprite_graphics += decompress_gfx(compressed_gfx)

        sprite_graphics = bytearray([0x00 for _ in range(0x23000)])

        offset = 0
        for _, sprite_data in sprite_gfx_data.sprite_gfx_data.items():
            if len(sprite_data) == 0:
                continue
            sprite_size = sprite_data.pop(0)
            sprite_graphics[offset:offset+sprite_size*0x400] = copy_sprite_tiles(raw_sprite_graphics, sprite_data, sprite_size)
            offset += 0x400 * sprite_size

        decompressed_gfx_00 = raw_sprite_graphics[0x0000:0x1000]
        decompressed_gfx_01 = raw_sprite_graphics[0x1000:0x2000]
        decompressed_gfx_10 = raw_sprite_graphics[0x12000:0x13000]
        decompressed_gfx_28 = raw_sprite_graphics[0x13000:0x13800]

        # Copy berry tiles
        order = [0x26C, 0x26D, 0x26E, 0x26F,
                0x27C, 0x27D, 0x27E, 0x27F,
                0x2E0, 0x2E1, 0x2E2, 0x2E3,
                0x2E4, 0x2E5, 0x2E6, 0x2E7]
        decompressed_animated_gfx += copy_gfx_tiles(decompressed_player_gfx, order, [5, 32])

        # Copy Mario's auxiliary tiles
        order = [0x80, 0x91, 0x81, 0x90, 0x82, 0x83]
        decompressed_gfx_00 += copy_gfx_tiles(decompressed_player_gfx, order, [5, 32])
        order = [0x69, 0x69, 0x0C, 0x69, 0x1A, 0x1B, 0x0D, 0x69, 0x22, 0x23, 0x32, 0x33, 0x0A, 0x0B, 0x20, 0x21,
                0x30, 0x31, 0x7E, 0x69, 0x80, 0x4A, 0x81, 0x5B, 0x82, 0x4B, 0x83, 0x5A, 0x84, 0x69, 0x85, 0x85]
        player_small_tiles = copy_gfx_tiles(decompressed_gfx_00, order, [5, 32])
        
        # Copy OW mario tiles
        order = [0x06, 0x07, 0x16, 0x17,
                0x08, 0x09, 0x18, 0x19,
                0x0A, 0x0B, 0x1A, 0x1B,
                0x0C, 0x0D, 0x1C, 0x1D,
                0x0E, 0x0F, 0x1E, 0x1F,
                0x20, 0x21, 0x30, 0x31,
                0x24, 0x25, 0x34, 0x35,
                0x46, 0x47, 0x56, 0x57,
                0x64, 0x65, 0x74, 0x75,
                0x66, 0x67, 0x76, 0x77,
                0x2E, 0x2F, 0x3E, 0x3F,
                0x40, 0x41, 0x50, 0x51,
                0x42, 0x43, 0x52, 0x53]
        
        player_map_tiles = copy_gfx_tiles(decompressed_gfx_10, order, [5, 32])

        # Copy HUD mario tiles
        order = [0x30, 0x31, 0x32, 0x33, 0x34]
        player_name_tiles = copy_gfx_tiles(decompressed_gfx_28, order, [4, 16])

        # Create inventory
        order = [
            0x0024,0x0024,0x0026,0x0026,0x000E,0x000E,0x0048,0x0048,
            0x0680,0x0680,0x0680,0x0680,0x0680,0x0680,0x0680,0x0680,
            0x0066,0x0066,0x0066,0x0066,0x0066,0x0066,0x0066,0x0066,
            0x0066,0x0066,0x0066,0x0066,0x0066,0x0066,0x0843,0x0066,
        ]
        inventory_gfx = copy_sprite_tiles(raw_sprite_graphics, order, 4)

        # Copy midway point
        order = [
            0x0104,0x0105,0x0106,0x0107,
            0x0114,0x0115,0x0116,0x0117,
            0x0124,0x0125,0x0126,0x0127,
            0x0134,0x0135,0x0136,0x0137,
        ]
        midway_point_gfx = copy_sprite_tiles(decompressed_animated_gfx, order, 4)

        # Patch graphics with modified data
        patched_sprite_graphics = bsdiff4.patch(bytes(sprite_graphics), caller.get_file("sprite_graphics.bsdiff4"))
        patched_gfx_00 = bsdiff4.patch(bytes(decompressed_gfx_00), caller.get_file("sprite_page_1.bsdiff4"))
        patched_gfx_01 = bsdiff4.patch(bytes(decompressed_gfx_01), caller.get_file("sprite_page_2.bsdiff4"))
        patched_inventory_gfx = bsdiff4.patch(bytes(inventory_gfx), caller.get_file("map_sprites.bsdiff4"))
        patched_midway_point = bsdiff4.patch(bytes(midway_point_gfx), caller.get_file("midway_point.bsdiff4"))

        rom[0xE0000:0xE0000 + len(decompressed_player_gfx)] = decompressed_player_gfx
        rom[0xE8000:0xE8000 + len(decompressed_animated_gfx)] = decompressed_animated_gfx
        rom[0xE6000:0xE6000 + len(player_small_tiles)] = player_small_tiles
        rom[0xE6400:0xE6400 + len(player_map_tiles)] = player_map_tiles
        rom[0xE6C00:0xE6C00 + len(player_name_tiles)] = player_name_tiles
        rom[0xEC000:0xEC000 + len(patched_inventory_gfx)] = bytearray(patched_inventory_gfx)
        rom[0x100000:0x100000 + len(patched_sprite_graphics)] = bytearray(patched_sprite_graphics)
        rom[0x178000:0x178000 + len(patched_gfx_00)] = bytearray(patched_gfx_00)
        rom[0x179000:0x179000 + len(patched_gfx_01)] = bytearray(patched_gfx_01)

        data = bytearray(patched_midway_point)
        rom[0xEA080:0xEA100] = data[0x0000:0x0080]
        rom[0xEA280:0xEA300] = data[0x0080:0x0100]
        rom[0xEA480:0xEA500] = data[0x0100:0x0180]
        rom[0xEA680:0xEA700] = data[0x0180:0x0200]

        return bytes(rom)

    @staticmethod
    def generate_shuffled_header_data(caller: APProcedurePatch, rom: bytes) -> bytes:
        options = json.loads(caller.get_file("options.json").decode("UTF-8"))
        if options["music_shuffle"] != 2 and options["level_palette_shuffle"] != 1:
            return rom

        from .Aesthetics import valid_foreground_palettes, valid_background_palettes, valid_background_colors

        rom = bytearray(rom)
        random.seed(options["seed"])

        for level_id in range(0, 0x200):
            layer1_ptr = int.from_bytes(rom[0x2E000 + level_id * 3:(0x2E000 + level_id * 3) + 3], "little")

            if layer1_ptr == 0x68000:
                # Unused Levels
                continue

            layer1_ptr = snes_to_pc(layer1_ptr)
            level_header = list(rom[layer1_ptr:layer1_ptr + 5])

            tileset = level_header[4] & 0x0F

            if options["music_shuffle"] == 2:
                level_header[2] &= 0x8F
                level_header[2] |= (random.randint(0, 7) << 5)

            if options["level_palette_shuffle"] == 1:
                if tileset in valid_foreground_palettes:
                    level_header[3] &= 0xF8
                    level_header[3] |= random.choice(valid_foreground_palettes[tileset])

                layer2_ptr = int.from_bytes(rom[0x2E600 + level_id * 3:(0x2E600 + level_id * 3) + 3], "little")

                if layer2_ptr in valid_background_palettes:
                    level_header[0] &= 0x1F
                    level_header[0] |= (random.choice(valid_background_palettes[layer2_ptr]) << 5)

                if layer2_ptr in valid_background_colors:
                    level_header[1] &= 0x1F
                    level_header[1] |= (random.choice(valid_background_colors[layer2_ptr]) << 5)

            rom[layer1_ptr:layer1_ptr+5] = bytearray(level_header)

        return bytes(rom)


    @staticmethod
    def replace_graphics(caller: APProcedurePatch, rom: bytes) -> bytes:
        # Get world's settings
        options = json.loads(caller.get_file("options.json").decode("UTF-8"))

        #if not world_settings or "graphics_pack" in options.keys():
        #    return rom

        graphics_setting = ""        
        if "graphics_pack" in options.keys():
            # Load local (.apwaffle) graphics pack
            graphics_setting = options["graphics_pack"]
        elif vars(Utils.persistent_load().get("graphics_pack", {}).get("SMW: Spicy Mycena Waffles", Namespace())):
            # Check persistent storage for a global graphics pack
            persistent_settings = Utils.persistent_load().get("graphics_pack", {}).get("SMW: Spicy Mycena Waffles", Namespace())
            if hasattr(persistent_settings, "selected_pack"):
                if len(persistent_settings.selected_pack) != 0:
                    graphics_setting = persistent_settings.selected_pack
        if len(graphics_setting) == 0:
            # Check if the setting is properly set and exists in data/sprites/smw
            # This is our very last resort
            world_type = AutoWorldRegister.world_types[WafflePatchExtension.game]
            world_settings = getattr(settings.get_settings(), world_type.settings_key, None)
            if not world_settings:
                return rom
            graphics_setting = world_settings.graphics_file
            
        if not os.path.isfile(graphics_setting):
            return rom
        
        # Begin replacing graphics
        import zipfile

        rom = bytearray(rom)

        file = zipfile.ZipFile(graphics_setting)
        if f"player_big.bin" in file.namelist():
            pass
        if "player.bin" in file.namelist():
            player_file = file.read('player.bin')
            rom[0xE0000:0xE0000 + len(player_file)] = player_file
        if "player_extra.bin" in file.namelist():
            player_extra_file = file.read('player_extra.bin')
            rom[0xE6000:0xE6000 + len(player_extra_file)] = player_extra_file
        if "player_map.bin" in file.namelist():
            player_map_file = file.read('player_map.bin')
            rom[0xE6400:0xE6400 + len(player_map_file)] = player_map_file
        if "player_name.bin" in file.namelist():
            player_name_file = file.read('player_name.bin')
            if len(player_name_file) == 80:
                player_name_file = convert_name_to_4bpp(player_name_file)
            rom[0x179C00:0x179C00 + len(player_name_file)] = player_name_file
        if "map.mw3" in file.namelist():
            map_file = file.read('map.mw3')
            rom[0xE6C50:0xE6C50 + len(map_file)] = map_file
            rom[0x1BFC0:0x1BFC1] = b'\x01'
        if "shared.mw3" in file.namelist():
            shared_file = file.read('shared.mw3')
            rom[0x030A0:0x030A0 + 0x7E0] = shared_file[0x0:0x7E0]
        if "yoshi+anim.bin" in file.namelist():
            yoshi_anim_file = file.read('yoshi+anim.bin')
            rom[0xE8000:0xE8000 + len(yoshi_anim_file)] = yoshi_anim_file
        if "sprites.bin" in file.namelist():
            sprites_file = file.read('sprites.bin')
            rom[0x100000:0x100000 + len(sprites_file)] = sprites_file

        return bytes(rom)
    

    @staticmethod
    def shuffle_enemies(caller: APProcedurePatch, rom: bytes) -> bytes:
        options = json.loads(caller.get_file("options.json").decode("UTF-8"))
        if options["enemy_shuffle"] == 0:
            return rom

        # Handle some special cases
        from .Enemies import SPRITE_POINTERS_ADDR, enemy_list, enemy_list_special_cases, modify_sprite_data, build_enemy_replacements, full_displacement_tags, half_displacement_tags

        rom = bytearray(rom)
        rom = modify_sprite_data(rom, options["enemy_shuffle_seed"])
        original_rom = rom.copy()
        
        random.seed(options["enemy_shuffle_seed"])

        sprite_pointers = rom[SPRITE_POINTERS_ADDR:SPRITE_POINTERS_ADDR+0x400]
        for level_id in range(0x200):
            pointer = int.from_bytes(sprite_pointers[level_id*2:(level_id*2)+2], "little") | 0x38000
            data = []
            idx = 1
            bytes_read = [0x00]
            while bytes_read[0] != 0xFF:
                bytes_read = original_rom[pointer+idx:pointer+idx+3]
                data.append(bytes_read)
                idx += 3
            data.pop()

            if not data:
                continue

            enemy_list_in_use = enemy_list.copy()
            if level_id in enemy_list_special_cases.keys():
                enemy_list_in_use.update((enemy_list_special_cases[level_id]))
                
            enemy_replacement_by_tag = build_enemy_replacements(enemy_list_in_use)

            new_data = []
            for idy, sprite in enumerate(data):
                sprite = int.from_bytes(sprite, "little")
                num = (sprite >> 16) | ((sprite >> 2) & 0x03)
                if num not in enemy_list_in_use.keys():
                    new_data += sprite.to_bytes(3, "little")
                    continue
                enemy_data = enemy_list_in_use[num]

                # Select a new sprite
                tag = random.choice(enemy_data.tags)
                if tag == "skip":
                    new_data += sprite.to_bytes(3, "little")
                    continue

                selected_id = random.choice(enemy_replacement_by_tag[tag])

                # yyyyEESY	XXXXssss	NNNNNNNN
                # NNNNNNNN XXXXssss yyyyEESY

                # Process displacement based on tags
                x_pos = (sprite >> 12) & 0x0F | (sprite >> 4) & 0xF0 | (sprite << 7) & 0x100
                y_pos = (sprite & 0xF0) >> 4 | (sprite & 0x01) << 4

                new_enemy_data = enemy_list_in_use[selected_id]
                
                y_diff = new_enemy_data.disp[1] - enemy_data.disp[1]
                x_diff = new_enemy_data.disp[0] - enemy_data.disp[0]

                if tag in full_displacement_tags:
                    y_pos -= y_diff
                    x_pos -= x_diff
                elif tag in half_displacement_tags:
                    if y_diff != 0:
                        y_diff = int(y_diff/2)
                    if x_diff != 0:
                        x_diff = int(x_diff/2)
                    y_pos -= y_diff
                    x_pos -= x_diff

                # Pack everything again
                #print (f"{sprite:06X} | {num:04X}")
                sprite = 0
                sprite |= selected_id << 16
                sprite |= (selected_id & 0x300) >> 6
                sprite |= ((x_pos & 0x0F) << 12) | ((x_pos & 0xF0) << 4) | ((x_pos & 0x100) >> 7)
                sprite |= ((y_pos & 0x0F) << 4) | ((y_pos & 0x10) >> 4)
                #num = (sprite >> 16) | ((sprite >> 2) & 0x03)
                #print (f"{sprite:06X} | {num:04X}")
                new_data += sprite.to_bytes(3, "little")

            rom[pointer+1:(pointer+1+len(data)*3)] = bytearray(new_data)

        return bytes(rom)
    
    @staticmethod
    def process_level_tiles(caller: APProcedurePatch, rom: bytes) -> bytes:
        from .Levels import full_level_list
        level_swap = list(caller.get_file("level_swap.bin"))
        level_data = list(caller.get_file("level_data.bin"))
        
        rom = bytearray(rom)
        unmodified_rom = rom.copy()

        for idx, level_id in enumerate(level_data):
            # Remove unswappable levels
            if level_id >= 0x60 or level_id == 0x00:
                continue
            
            # Get level coords and transform them into the usable index for the ROM table
            original_index = compute_level_index(full_level_list[idx])
            shuffled_index = compute_level_index(level_id)

            # Swap level tiles
            original_level_tile = rom[0x677DF+original_index]
            shuffled_level_tile = unmodified_rom[0x677DF+shuffled_index]
            if original_level_tile in visible_to_invisible_level_tiles.keys():
                new_tile = shuffled_level_tile
                if new_tile in invisible_to_visible_level_tiles.keys():
                    new_tile = invisible_to_visible_level_tiles[new_tile]
                #print (f"{level_id:02X} ({full_level_list[idx]:02X}) | {original_level_tile:02X} | {shuffled_level_tile:02X} | {new_tile:02X} | VISIBLE")
                rom[0x677DF+original_index] = new_tile
                
            elif original_level_tile in invisible_to_visible_level_tiles.keys():
                new_tile = shuffled_level_tile
                if new_tile in visible_to_invisible_level_tiles.keys():
                    new_tile = visible_to_invisible_level_tiles[new_tile]
                #print (f"{level_id:02X} ({full_level_list[idx]:02X}) | {original_level_tile:02X} | {shuffled_level_tile:02X} | {new_tile:02X} | INVISIBLE")
                rom[0x677DF+original_index] = new_tile

            # Swap tile to a big level tile/gray house if the exits are swapped
            # Also re-fetch the original level tile in case it changed
            original_level_tile = rom[0x677DF+original_index]
            if level_id in level_swap and original_level_tile in (0x6E, 0x70, 0x72, 0x74, 0x7A, 0x63, 0x68):
                new_tile = original_level_tile + 1
                if original_level_tile == 0x63:
                    new_tile = 0x7C
                rom[0x677DF+original_index] = new_tile

        return bytes(rom)
    

    @staticmethod
    def write_global_settings(caller: APProcedurePatch, rom: bytes) -> bytes:
        rom = bytearray(rom)

        settings_value = 0
        if vars(Utils.persistent_load().get("global_settings", {}).get("SMW: Spicy Mycena Waffles", Namespace())):
            # Check persistent storage for a global graphics pack
            persistent_settings = Utils.persistent_load().get("global_settings", {}).get("SMW: Spicy Mycena Waffles", Namespace())
            if hasattr(persistent_settings, "lr_wallrun"):
                if persistent_settings.lr_wallrun:
                    settings_value |= 0x02 
            if hasattr(persistent_settings, "lr_swim"):
                if persistent_settings.lr_swim:
                    settings_value |= 0x01
            if hasattr(persistent_settings, "mute_music"):
                if persistent_settings.mute_music:
                    rom[0x000179:0x00017C] = [0x4C, 0x8F, 0x81]
            
        rom[0x01BFBF] = settings_value

        return bytes(rom)

class WaffleProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = [USHASH]
    game = "SMW: Spicy Mycena Waffles"
    patch_file_ending = ".apwaffle"
    result_file_ending = ".sfc"
    name: bytearray
    procedure = [
        ("apply_bsdiff4", ["smw_sa1_basepatch.bsdiff4"]),
        ("apply_tokens", ["token_patch.bin"]),
        ("generate_shuffled_header_data", []),
        ("handle_uncompressed_graphics", []),
        ("replace_graphics", []),
        ("shuffle_enemies", []),
        ("process_level_tiles", []),
        ("write_global_settings", []),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_byte(self, offset, value):
        self.write_token(APTokenTypes.WRITE, offset, value.to_bytes(1, "little"))

    def write_bytes(self, offset, value: typing.Iterable[int]):
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))

def handle_level_effects(patch: WaffleProcedurePatch, world: "WaffleWorld"):
    from .Levels import lockable_tiles

    trap_weights = []
    trap_weights += ([1] * world.options.ice_trap_weight.value)
    trap_weights += ([2] * world.options.reverse_trap_weight.value)
    trap_weights += ([3] * world.options.screen_flip_trap_weight.value)
    trap_weights += ([4] * world.options.pixelate_trap_weight.value)
    trap_weights += ([5] * world.options.spotlight_trap_weight.value)
    trap_weights += ([6] * world.options.invisibility_trap_weight.value)
    if len(trap_weights) == 0:
        trap_weights = [1, 2, 3, 4, 5, 6]

    buffer = bytearray([0x00 for _ in range(96)])
    copy_level_tiles = lockable_tiles.copy()
    world.random.shuffle(copy_level_tiles)
    for idx in range(world.options.level_effects.value):
        idy = copy_level_tiles[idx]
        buffer[idy] = world.random.choice(trap_weights)

    patch.write_bytes(0x88AE5, buffer)

def handle_level_shuffle(patch: WaffleProcedurePatch, active_level_dict):
    for level_id, level_data in level_info_dict.items():
        if level_id not in active_level_dict.keys():
            continue

        tile_id = active_level_dict[level_id]
        tile_data = level_info_dict[tile_id]

        if level_id > 0x80:
            level_id = level_id - 0x50

        patch.write_byte(tile_data.levelIDAddress, level_id)
        patch.write_byte(0x2D608 + level_id, tile_data.eventIDValue)

    for level_id, tile_id in active_level_dict.items():
        patch.write_byte(0x37F70 + level_id, tile_id)
        patch.write_byte(0x37F00 + tile_id, level_id)


def handle_starting_location(patch: WaffleProcedurePatch, world: "WaffleWorld"):
    data = starting_positions_data[world.options.starting_location.value].copy()

    # Fix initial map
    initial_map = data.pop(0)
    patch.write_byte(0x01EF0, initial_map)
    patch.write_byte(0x20EFA, initial_map)
    patch.write_byte(0x01EF1, data.pop(0))

    # Force level name to appear
    level_offset = data.pop(0)
    patch.write_byte(0x01BFAE, world.options.starting_location.value)
    patch.write_byte(0x01BFAF, list(world.active_level_dict.keys())[level_offset])

    # Fix X/Y positions
    for idx, entry in enumerate(data):
        patch.write_bytes(0x01EF2 + (idx*2), entry.to_bytes(2, "little"))
        if idx == 2:
            entry &= 0xFF
            patch.write_byte(0x20F01, entry)
        elif idx == 3:
            entry &= 0xFF
            patch.write_byte(0x218F0, entry)
            patch.write_byte(0x2B15C, entry+0x16)
            patch.write_byte(0x20F08, entry+0x16)


def handle_exit_shuffle(patch: WaffleProcedurePatch, world: "WaffleWorld"):
    exit_shuffle_info = bytearray([0x00 for _ in range(96)])
    for level_id in world.swapped_exits:
        exit_shuffle_info[level_id] = 0x01
    patch.write_bytes(0x88A85, exit_shuffle_info)


def handle_keyhole_shuffle(patch: WaffleProcedurePatch, world: "WaffleWorld"):
    keyhole_shuffle_info = bytearray([0x00 for _ in range(96)])
    for level_id in world.carryless_exits:
        keyhole_shuffle_info[level_id] = 0x01
    patch.write_bytes(0x88B45, keyhole_shuffle_info)


def handle_texts(patch: WaffleProcedurePatch, world: "WaffleWorld"):
    goal_text = generate_goal_text(world)
    patch.write_bytes(0x2A6E2, goal_text)
    
    intro_text = generate_text_box("Bowser has stolen all of Mario's abilities. Can you help Mario travel across Dinosaur land to get them back and save the Princess from him?")
    patch.write_bytes(0x2A5D9, intro_text)

    message_indexes = [
        0x0291,
        0x041D,
        0x0518,
        0x061D,
        0x08B7,
        0x07B2,
        0x030B,
        0x083C,
        0x099D,
        0x0A9E,
        0x04A0,
        0x0A2C,
        0x06A6,
        0x0730,
        0x0911,
        0x05A4,
        0x038F,
    ]

    entrance_list = list(world.teleport_pairs.keys()) + list(world.transition_pairs.keys())

    world.random.shuffle(message_indexes)
    world.random.shuffle(entrance_list)

    for idx in message_indexes:
        entrance: str = entrance_list.pop(0)
        if "Transition" in entrance:
            entrance_text = entrance.split("Transition - ")[1].split(" to ")[0]
            exit = world.transition_pairs[entrance]
            exit_text = exit.split("Transition - ")[1].split(" from ")[0]
            text = generate_text_box(f"{entrance_text} leads to {exit_text}")
        else:
            entrance_text = entrance.split(" - ")[0]
            exit = world.teleport_pairs[entrance]
            exit_text = exit.split(" - ")[0]
            text = generate_text_box(f"{entrance_text} connects to {exit_text}")
        patch.write_bytes(0x2A5D9 + idx, text)
        

def handle_location_item_info(patch: WaffleProcedurePatch, world: "WaffleWorld"):
    block_info = bytearray([0x00 for _ in range(652)])
    normal_exit_info = bytearray([0x00 for _ in range(96)])
    secret_exit_info = bytearray([0x00 for _ in range(96)])
    bonus_block_info = bytearray([0x00 for _ in range(96)])
    moon_info = bytearray([0x00 for _ in range(96)])
    dragon_coin_info = bytearray([0x00 for _ in range(96)])
    hidden_1up_info = bytearray([0x00 for _ in range(96)])
    midway_point_info = bytearray([0x00 for _ in range(96)])
    locations = world.multiworld.get_filled_locations(world.player)
    for location in locations:
        classification = 0
        if ItemClassification.progression in location.item.classification or ItemClassification.trap in location.item.classification:
            classification = 2
        elif ItemClassification.useful in location.item.classification:
            classification = 4
        
        level_id = location.address >> 24
        loc_type = (location.address >> 20 & 0x0F)
        level_data = location.address & 0x0F

        if level_id in world.swapped_exits:
            loc_type = loc_type ^ 1

        if loc_type == 0x00 and level_data == 0x00:
            normal_exit_info[level_id] = classification
        elif loc_type == 0x01 and level_data == 0x00:
            secret_exit_info[level_id] = classification
        elif loc_type == 0x03:
            dragon_coin_info[level_id] = classification
        elif loc_type == 0x04:
            moon_info[level_id] = classification
        elif loc_type == 0x05:
            hidden_1up_info[level_id] = classification
        elif loc_type == 0x06:
            midway_point_info[level_id] = classification
        elif loc_type == 0x07:
            bonus_block_info[level_id] = classification
        elif loc_type == 0x0A:
            block_index = location.address & 0xFFFF
            block_info[block_index] = classification

    patch.write_bytes(0x88553, normal_exit_info)
    patch.write_bytes(0x885B3, secret_exit_info)
    patch.write_bytes(0x88493, dragon_coin_info)
    patch.write_bytes(0x884F3, moon_info)
    patch.write_bytes(0x88673, hidden_1up_info)
    patch.write_bytes(0x88613, bonus_block_info)
    patch.write_bytes(0x88207, block_info)
    patch.write_bytes(0x886D3, midway_point_info)


def handle_music_shuffle(patch: WaffleProcedurePatch, world: "WaffleWorld"):
    from .Aesthetics import generate_shuffled_level_music, generate_shuffled_ow_music, level_music_address_data, ow_music_address_data

    shuffled_level_music = generate_shuffled_level_music(world)
    for i in range(len(shuffled_level_music)):
        patch.write_byte(level_music_address_data[i], shuffled_level_music[i])

    shuffled_ow_music = generate_shuffled_ow_music(world)
    for i in range(len(shuffled_ow_music)):
        for addr in ow_music_address_data[i]:
            patch.write_byte(addr, shuffled_ow_music[i])


def handle_mario_palette(patch: WaffleProcedurePatch, world: "WaffleWorld"):
    from .Aesthetics import mario_palettes, fire_mario_palettes, ow_mario_palettes

    chosen_palette = world.options.mario_palette.value

    patch.write_bytes(0x32C8, bytes(mario_palettes[chosen_palette]))
    patch.write_bytes(0x32F0, bytes(fire_mario_palettes[chosen_palette]))
    patch.write_bytes(0x359C, bytes(ow_mario_palettes[chosen_palette]))


def handle_bowser_rooms(patch: WaffleProcedurePatch, world: "WaffleWorld"):
    if world.options.bowser_castle_rooms == "random_two_room":
        chosen_rooms = world.random.sample(standard_bowser_rooms, 2)

        patch.write_byte(0x3A680, chosen_rooms[0].roomID)
        patch.write_byte(0x3A684, chosen_rooms[0].roomID)
        patch.write_byte(0x3A688, chosen_rooms[0].roomID)
        patch.write_byte(0x3A68C, chosen_rooms[0].roomID)

        for i in range(1, len(chosen_rooms)):
            patch.write_byte(chosen_rooms[i-1].exitAddress, chosen_rooms[i].roomID)

        patch.write_byte(chosen_rooms[len(chosen_rooms)-1].exitAddress, 0xBD)

    elif world.options.bowser_castle_rooms == "random_five_room":
        chosen_rooms = world.random.sample(standard_bowser_rooms, 5)

        patch.write_byte(0x3A680, chosen_rooms[0].roomID)
        patch.write_byte(0x3A684, chosen_rooms[0].roomID)
        patch.write_byte(0x3A688, chosen_rooms[0].roomID)
        patch.write_byte(0x3A68C, chosen_rooms[0].roomID)

        for i in range(1, len(chosen_rooms)):
            patch.write_byte(chosen_rooms[i-1].exitAddress, chosen_rooms[i].roomID)

        patch.write_byte(chosen_rooms[len(chosen_rooms)-1].exitAddress, 0xBD)

    elif world.options.bowser_castle_rooms == "gauntlet":
        chosen_rooms = standard_bowser_rooms.copy()
        world.random.shuffle(chosen_rooms)

        patch.write_byte(0x3A680, chosen_rooms[0].roomID)
        patch.write_byte(0x3A684, chosen_rooms[0].roomID)
        patch.write_byte(0x3A688, chosen_rooms[0].roomID)
        patch.write_byte(0x3A68C, chosen_rooms[0].roomID)

        for i in range(1, len(chosen_rooms)):
            patch.write_byte(chosen_rooms[i-1].exitAddress, chosen_rooms[i].roomID)

        patch.write_byte(chosen_rooms[len(chosen_rooms)-1].exitAddress, 0xBD)
    elif world.options.bowser_castle_rooms == "labyrinth":
        bowser_rooms_copy = full_bowser_rooms.copy()

        entrance_point = bowser_rooms_copy.pop(0)

        world.random.shuffle(bowser_rooms_copy)

        patch.write_byte(entrance_point.exitAddress, bowser_rooms_copy[0].roomID)
        for i in range(0, len(bowser_rooms_copy) - 1):
            patch.write_byte(bowser_rooms_copy[i].exitAddress, bowser_rooms_copy[i+1].roomID)

        patch.write_byte(bowser_rooms_copy[len(bowser_rooms_copy)-1].exitAddress, 0xBD)


def handle_boss_shuffle(patch: WaffleProcedurePatch, world: "WaffleWorld"):
    if world.options.boss_shuffle == "simple":
        submap_boss_rooms_copy = submap_boss_rooms.copy()
        ow_boss_rooms_copy = ow_boss_rooms.copy()

        world.random.shuffle(submap_boss_rooms_copy)
        world.random.shuffle(ow_boss_rooms_copy)

        for i in range(len(submap_boss_rooms_copy)):
            patch.write_byte(submap_boss_rooms[i].exitAddress, submap_boss_rooms_copy[i].roomID)

        for i in range(len(ow_boss_rooms_copy)):
            patch.write_byte(ow_boss_rooms[i].exitAddress, ow_boss_rooms_copy[i].roomID)

            if ow_boss_rooms[i].exitAddressAlt is not None:
                patch.write_byte(ow_boss_rooms[i].exitAddressAlt, ow_boss_rooms_copy[i].roomID)

    elif world.options.boss_shuffle == "full":
        for i in range(len(submap_boss_rooms)):
            chosen_boss = world.random.choice(submap_boss_rooms)
            patch.write_byte(submap_boss_rooms[i].exitAddress, chosen_boss.roomID)

        for i in range(len(ow_boss_rooms)):
            chosen_boss = world.random.choice(ow_boss_rooms)
            patch.write_byte(ow_boss_rooms[i].exitAddress, chosen_boss.roomID)

            if ow_boss_rooms[i].exitAddressAlt is not None:
                patch.write_byte(ow_boss_rooms[i].exitAddressAlt, chosen_boss.roomID)

    elif world.options.boss_shuffle == "singularity":
        chosen_submap_boss = world.random.choice(submap_boss_rooms)
        chosen_ow_boss = world.random.choice(ow_boss_rooms)

        for i in range(len(submap_boss_rooms)):
            patch.write_byte(submap_boss_rooms[i].exitAddress, chosen_submap_boss.roomID)

        for i in range(len(ow_boss_rooms)):
            patch.write_byte(ow_boss_rooms[i].exitAddress, chosen_ow_boss.roomID)

            if ow_boss_rooms[i].exitAddressAlt is not None:
                patch.write_byte(ow_boss_rooms[i].exitAddressAlt, chosen_ow_boss.roomID)

def snes_to_pc(address: int):
    return (address & 0x7F0000) >> 1 | (address & 0x7FFF)


def patch_rom(world: "WaffleWorld", patch: WaffleProcedurePatch, player: int, active_level_dict: typing.Dict[int,int]) -> None:
    options_dict = {
        "seed": world.random.getrandbits(64),
        "music_shuffle": world.options.music_shuffle.value,
        "level_palette_shuffle": 2,
        "enemy_shuffle": world.options.enemy_shuffle.value,
        "enemy_shuffle_seed": world.random.getrandbits(64),
    }
    patch.write_file("options.json", json.dumps(options_dict).encode("UTF-8"))

    handle_texts(patch, world)

    handle_bowser_rooms(patch, world)
    handle_boss_shuffle(patch, world)

    # Title Screen Text
    player_name_bytes = bytearray()
    player_name = world.multiworld.get_player_name(player)
    for i in range(16):
        char = " "
        if i < len(player_name):
            char = player_name[i]
        upper_char = char.upper()
        if upper_char not in title_text_mapping:
            for byte in title_text_mapping["."]:
                player_name_bytes.append(byte)
        else:
            for byte in title_text_mapping[upper_char]:
                player_name_bytes.append(byte)

    patch.write_bytes(0x2B7F1, player_name_bytes) # MARIO A
    patch.write_bytes(0x2B726, player_name_bytes) # MARIO A

    # Handle Level Shuffle
    handle_level_shuffle(patch, active_level_dict)
    handle_starting_location(patch, world)
    handle_exit_shuffle(patch, world)
    handle_keyhole_shuffle(patch, world)
    if world.options.level_effects.value:
        handle_level_effects(patch, world)

    if world.options.map_teleport_shuffle != "off":
        handle_teleport_shuffle(patch, world)
    
    #if world.options.map_transition_shuffle:
    if world.options.map_transition_shuffle:
        handle_transition_shuffle(patch, world)
    
    if world.options.map_teleport_shuffle or world.options.map_transition_shuffle:
        handle_silent_events(patch, world)

    # Handle Music Shuffle
    if world.options.music_shuffle != "none":
        handle_music_shuffle(patch, world)

    #generate_shuffled_ow_palettes(patch, world)

    #if world.options.level_palette_shuffle == "on_curated":
    generate_curated_level_palette_data(patch, world)
    # Fix bush filler tiles
    BUSH_FILLER_ADDR = 0x68248
    patch.write_byte(BUSH_FILLER_ADDR + 0x01, 0x04)
    patch.write_byte(BUSH_FILLER_ADDR + 0x03, 0x04)
    patch.write_byte(BUSH_FILLER_ADDR + 0x05, 0x04)
    patch.write_byte(BUSH_FILLER_ADDR + 0x07, 0x04)

    #if world.options.overworld_palette_shuffle == "on_curated":
    generate_curated_map_palette_data(patch, world)
    
    if world.options.sfx_shuffle != "none":
        generate_shuffled_sfx(patch, world)

    handle_mario_palette(patch, world)

    handle_location_item_info(patch, world)

    # Store all relevant option results in ROM
    patch.write_byte(0x01BFBF, 0x00)        # Global settings
    patch.write_byte(0x01BFA0, world.options.goal.value)
    patch.write_byte(0x01BFA1, world.required_egg_count)
    patch.write_byte(0x01BFA2, world.required_egg_count)
    #patch.write_byte(0x01BFA3, world.options.display_sent_item_popups.value)
    patch.write_byte(0x01BFA4, world.options.display_received_item_popups.value)
    patch.write_byte(0x01BFA5, world.options.death_link.value)
    patch.write_byte(0x01BFA6, world.options.dragon_coin_checks.value)
    patch.write_byte(0x01BFA7, world.options.swap_donut_gh_exits.value)
    patch.write_byte(0x01BFA8, world.options.moon_checks.value)
    patch.write_byte(0x01BFA9, world.options.hidden_1up_checks.value)
    patch.write_byte(0x01BFAA, world.options.star_block_checks.value)
    patch.write_byte(0x01BFAC, world.options.midway_point_checks.value)
    patch.write_byte(0x01BFAD, world.options.room_checks.value)
    patch.write_byte(0x01BFB0, world.options.level_shuffle.value)
    setting_value = 0
    block_checks = world.options.block_checks.value
    if "Coin Blocks" in block_checks:
        setting_value |= 0x01
    if "Item Blocks" in block_checks:
        setting_value |= 0x02
    if "Yellow Switch Palace Blocks" in block_checks:
        setting_value |= 0x04
    if "Green Switch Palace Blocks" in block_checks:
        setting_value |= 0x08
    if "Invisible Blocks" in block_checks:
        setting_value |= 0x10
    if "P-Switch Blocks" in block_checks:
        setting_value |= 0x20
    if "Flying Blocks" in block_checks:
        setting_value |= 0x40
    patch.write_byte(0x01BFAB, setting_value)
    patch.write_byte(0x01BFB4, world.options.energy_link.value)

    patch.write_byte(0x01BFB7, world.options.trap_link.value)
    patch.write_byte(0x01BFB8, world.options.ring_link.value)

    from Utils import __version__
    patch.name = bytearray(f'WAFFLES{__version__.replace(".", "")[0:3]}_{player}_{world.multiworld.seed:13}\0', 'utf8')[:21]
    patch.name.extend([0] * (21 - len(patch.name)))
    patch.write_bytes(0x7FC0, patch.name)

    #patch.write_byte(0x2273, 0x00)

    patch.write_file("token_patch.bin", patch.get_token_binary())

    level_data = []
    for level_id in world.active_level_dict.keys():
        level_data.append(level_id)
    patch.write_file("level_data.bin", bytearray(level_data))

    patch.write_file("level_swap.bin", bytearray(world.swapped_exits))


def compute_level_index(level_id: int) -> int:
    level_info = level_info_dict[level_id]
    x, y = level_info.coords

    index = (x & 0x0F) | ((y & 0x0F) << 4) | ((x & 0x10) << 4) | ((y & 0x10) << 5)
    if level_id >= 0x25:
        index |= 0x400
        index -= 1

    return index

def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(Utils.read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if USHASH != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for US(1.0) release. '
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    if not file_name:
        from settings import get_settings
        file_name = get_settings()["waffles_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
