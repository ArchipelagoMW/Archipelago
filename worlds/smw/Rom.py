import Utils
from worlds.AutoWorld import World
from worlds.Files import APDeltaPatch
from .Aesthetics import generate_shuffled_header_data, generate_shuffled_ow_palettes, generate_curated_level_palette_data, generate_curated_map_palette_data, generate_shuffled_sfx
from .Levels import level_info_dict, full_bowser_rooms, standard_bowser_rooms, submap_boss_rooms, ow_boss_rooms
from .Names.TextBox import generate_goal_text, title_text_mapping, generate_text_box

USHASH = 'cdd3c8c37322978ca8669b34bc89c804'
ROM_PLAYER_LIMIT = 65535

import hashlib
import os
import math
import pkgutil


ability_rom_data = {
    0xBC0003: [[0x1F1C, 0x7]], # Run         0x80
    0xBC0004: [[0x1F1C, 0x6]], # Carry       0x40
    0xBC0005: [[0x1F1C, 0x2]], # Swim        0x04
    0xBC0006: [[0x1F1C, 0x3]], # Spin Jump   0x08
    0xBC0007: [[0x1F1C, 0x5]], # Climb       0x20
    0xBC0008: [[0x1F1C, 0x1]], # Yoshi       0x02
    0xBC0009: [[0x1F1C, 0x4]], # P-Switch    0x10
    #0xBC000A: [[]]
    0xBC000B: [[0x1F2D, 0x3]], # P-Balloon   0x08
    0xBC000D: [[0x1F2D, 0x4]]  # Super Star  0x10
}

icon_rom_data = {
    0xBC0002: [0x1B00C], # Yoshi Egg
    0xBC0012: [0x1B00E], # Boss Token

    0xBC0017: [0x1B004], # 1 coin
    0xBC0018: [0x1B006], # 5 coins
    0xBC0019: [0x1B008], # 10 coins
    0xBC001A: [0x1B00A], # 50 coins

    0xBC0001: [0x1B010]  # 1-Up Mushroom
}
    
item_rom_data = {
    0xBC000E: [0x1F28, 0x1,  0x1C], # Yellow Switch Palace
    0xBC000F: [0x1F27, 0x1,  0x1C], # Green Switch Palace
    0xBC0010: [0x1F2A, 0x1,  0x1C], # Red Switch Palace
    0xBC0011: [0x1F29, 0x1,  0x1C], # Blue Switch Palace
    0xBC001B: [0x1F1E, 0x80, 0x39]  # Special Zone Clear
}

trap_rom_data = {
    0xBC0013: [0x0086, 0x1, 0x0E],  # Ice Trap
    0xBC0014: [0x18BD, 0x7F, 0x18], # Stun Trap
    0xBC0016: [0x0F31, 0x1],        # Timer Trap
    0xBC001C: [0x18B4, 0x1, 0x44],  # Reverse controls trap
    0xBC001D: [0x18B7, 0x1],        # Thwimp Trap
}


class SMWDeltaPatch(APDeltaPatch):
    hash = USHASH
    game = "Super Mario World"
    patch_file_ending = ".apsmw"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


class LocalRom:

    def __init__(self, file, patch=True, vanillaRom=None, name=None, hash=None):
        self.name = name
        self.hash = hash
        self.orig_buffer = None

        with open(file, 'rb') as stream:
            self.buffer = Utils.read_snes_rom(stream)
        
    def read_bit(self, address: int, bit_number: int) -> bool:
        bitflag = (1 << bit_number)
        return ((self.buffer[address] & bitflag) != 0)

    def read_byte(self, address: int) -> int:
        return self.buffer[address]

    def read_bytes(self, startaddress: int, length: int) -> bytearray:
        return self.buffer[startaddress:startaddress + length]

    def write_byte(self, address: int, value: int):
        self.buffer[address] = value

    def write_bytes(self, startaddress: int, values):
        self.buffer[startaddress:startaddress + len(values)] = values

    def write_to_file(self, file):
        with open(file, 'wb') as outfile:
            outfile.write(self.buffer)

    def read_from_file(self, file):
        with open(file, 'rb') as stream:
            self.buffer = bytearray(stream.read())


def handle_ability_code(rom):
    # Lock Abilities

    #rom.write_byte(0xC581, 0x01) # No Stars
    #rom.write_byte(0x62E6, 0x01) # No Star Music
    #rom.write_byte(0xC300, 0x01) # No P-Balloons
    #rom.write_byte(0xC305, 0x01) # No P-Balloons

    # Run
    rom.write_bytes(0x5977, bytearray([0x22, 0x10, 0xBA, 0x03])) # JSL $03BA10
    rom.write_bytes(0x597B, bytearray([0xEA] * 0x04))

    RUN_SUB_ADDR = 0x01BA10
    rom.write_bytes(RUN_SUB_ADDR + 0x00, bytearray([0xDA]))             # PHX
    rom.write_bytes(RUN_SUB_ADDR + 0x01, bytearray([0x08]))             # PHP
    rom.write_bytes(RUN_SUB_ADDR + 0x02, bytearray([0x90, 0x03]))       # BCC +0x03
    rom.write_bytes(RUN_SUB_ADDR + 0x04, bytearray([0xC8]))             # INY
    rom.write_bytes(RUN_SUB_ADDR + 0x05, bytearray([0xA9, 0x70]))       # LDA #70
    rom.write_bytes(RUN_SUB_ADDR + 0x07, bytearray([0xAA]))             # TAX
    rom.write_bytes(RUN_SUB_ADDR + 0x08, bytearray([0xAD, 0x1C, 0x1F])) # LDA $1F1C
    rom.write_bytes(RUN_SUB_ADDR + 0x0B, bytearray([0x89, 0x80]))       # BIT #80
    rom.write_bytes(RUN_SUB_ADDR + 0x0D, bytearray([0xF0, 0x04]))       # BEQ +0x04
    rom.write_bytes(RUN_SUB_ADDR + 0x0F, bytearray([0x8A]))             # TXA
    rom.write_bytes(RUN_SUB_ADDR + 0x10, bytearray([0x8D, 0xE4, 0x13])) # STA $13E4
    rom.write_bytes(RUN_SUB_ADDR + 0x13, bytearray([0x8A]))             # TXA
    rom.write_bytes(RUN_SUB_ADDR + 0x14, bytearray([0x28]))             # PLP
    rom.write_bytes(RUN_SUB_ADDR + 0x15, bytearray([0xFA]))             # PLX
    rom.write_bytes(RUN_SUB_ADDR + 0x16, bytearray([0x6B]))             # RTL
    # End Run

    # Purple Block Carry
    rom.write_bytes(0x726F, bytearray([0x22, 0x28, 0xBA, 0x03])) # JSL $03BA28
    rom.write_bytes(0x7273, bytearray([0xEA] * 0x02))

    PURPLE_BLOCK_CARRY_SUB_ADDR = 0x01BA28
    rom.write_bytes(PURPLE_BLOCK_CARRY_SUB_ADDR + 0x00, bytearray([0x08]))             # PHP
    rom.write_bytes(PURPLE_BLOCK_CARRY_SUB_ADDR + 0x01, bytearray([0xAD, 0x1C, 0x1F])) # LDA $1F1C
    rom.write_bytes(PURPLE_BLOCK_CARRY_SUB_ADDR + 0x04, bytearray([0x89, 0x40]))       # BIT #40
    rom.write_bytes(PURPLE_BLOCK_CARRY_SUB_ADDR + 0x06, bytearray([0xF0, 0x09]))       # BEQ +0x09
    rom.write_bytes(PURPLE_BLOCK_CARRY_SUB_ADDR + 0x08, bytearray([0x28]))             # PLP
    rom.write_bytes(PURPLE_BLOCK_CARRY_SUB_ADDR + 0x09, bytearray([0xAD, 0x8F, 0x14])) # LDA $148F
    rom.write_bytes(PURPLE_BLOCK_CARRY_SUB_ADDR + 0x0C, bytearray([0x0D, 0x7A, 0x18])) # ORA $187A
    rom.write_bytes(PURPLE_BLOCK_CARRY_SUB_ADDR + 0x0F, bytearray([0x80, 0x03]))       # BRA +0x03
    rom.write_bytes(PURPLE_BLOCK_CARRY_SUB_ADDR + 0x11, bytearray([0x28]))             # PLP
    rom.write_bytes(PURPLE_BLOCK_CARRY_SUB_ADDR + 0x12, bytearray([0xA9, 0x01]))       # LDA #01
    rom.write_bytes(PURPLE_BLOCK_CARRY_SUB_ADDR + 0x14, bytearray([0x6B]))             # RTL
    # End Purple Block Carry

    # Springboard Carry
    rom.write_bytes(0xE6DA, bytearray([0x22, 0x40, 0xBA, 0x03])) # JSL $03BA40
    rom.write_bytes(0xE6DE, bytearray([0xEA] * 0x04))

    SPRINGBOARD_CARRY_SUB_ADDR = 0x01BA40
    rom.write_bytes(SPRINGBOARD_CARRY_SUB_ADDR + 0x00, bytearray([0x48]))             # PHA
    rom.write_bytes(SPRINGBOARD_CARRY_SUB_ADDR + 0x01, bytearray([0x08]))             # PHP
    rom.write_bytes(SPRINGBOARD_CARRY_SUB_ADDR + 0x02, bytearray([0xAD, 0x1C, 0x1F])) # LDA $1F1C
    rom.write_bytes(SPRINGBOARD_CARRY_SUB_ADDR + 0x05, bytearray([0x89, 0x40]))       # BIT #40
    rom.write_bytes(SPRINGBOARD_CARRY_SUB_ADDR + 0x07, bytearray([0xF0, 0x08]))       # BEQ +0x08
    rom.write_bytes(SPRINGBOARD_CARRY_SUB_ADDR + 0x09, bytearray([0xA9, 0x0B]))       # LDA #0B
    rom.write_bytes(SPRINGBOARD_CARRY_SUB_ADDR + 0x0B, bytearray([0x9D, 0xC8, 0x14])) # STA $14C8, X
    rom.write_bytes(SPRINGBOARD_CARRY_SUB_ADDR + 0x0E, bytearray([0x9E, 0x02, 0x16])) # STZ $1602, X
    rom.write_bytes(SPRINGBOARD_CARRY_SUB_ADDR + 0x11, bytearray([0x28]))             # PLP
    rom.write_bytes(SPRINGBOARD_CARRY_SUB_ADDR + 0x12, bytearray([0x68]))             # PLA
    rom.write_bytes(SPRINGBOARD_CARRY_SUB_ADDR + 0x13, bytearray([0x6B]))             # RTL
    # End Springboard Carry

    # Shell Carry
    rom.write_bytes(0xAA66, bytearray([0xAD, 0x1C, 0x1F]))       # LDA $1F1C
    rom.write_bytes(0xAA69, bytearray([0x89, 0x40]))             # BIT #40
    rom.write_bytes(0xAA6B, bytearray([0xF0, 0x07]))             # BEQ +0x07
    rom.write_bytes(0xAA6D, bytearray([0x22, 0x60, 0xBA, 0x03])) # JSL $03BA60
    rom.write_bytes(0xAA71, bytearray([0xEA] * 0x02))

    SHELL_CARRY_SUB_ADDR = 0x01BA60
    rom.write_bytes(SHELL_CARRY_SUB_ADDR + 0x00, bytearray([0x08]))             # PHP
    rom.write_bytes(SHELL_CARRY_SUB_ADDR + 0x01, bytearray([0xA9, 0x0B]))       # LDA #0B
    rom.write_bytes(SHELL_CARRY_SUB_ADDR + 0x03, bytearray([0x9D, 0xC8, 0x14])) # STA $14C8, X
    rom.write_bytes(SHELL_CARRY_SUB_ADDR + 0x06, bytearray([0xEE, 0x70, 0x14])) # INC $1470
    rom.write_bytes(SHELL_CARRY_SUB_ADDR + 0x09, bytearray([0xA9, 0x0B]))       # LDA #08
    rom.write_bytes(SHELL_CARRY_SUB_ADDR + 0x0B, bytearray([0x8D, 0x98, 0x14])) # STA $1498
    rom.write_bytes(SHELL_CARRY_SUB_ADDR + 0x0E, bytearray([0x28]))             # PLP
    rom.write_bytes(SHELL_CARRY_SUB_ADDR + 0x0F, bytearray([0x6B]))             # RTL
    # End Shell Carry

    # Yoshi Carry
    rom.write_bytes(0xF309, bytearray([0x22, 0x70, 0xBA, 0x03])) # JSL $03BA70
    rom.write_bytes(0xF30D, bytearray([0xEA] * 0x06))

    YOSHI_CARRY_SUB_ADDR = 0x01BA70
    rom.write_bytes(YOSHI_CARRY_SUB_ADDR + 0x00, bytearray([0x08]))             # PHP
    rom.write_bytes(YOSHI_CARRY_SUB_ADDR + 0x01, bytearray([0xAD, 0x1C, 0x1F])) # LDA $1F1C
    rom.write_bytes(YOSHI_CARRY_SUB_ADDR + 0x04, bytearray([0x89, 0x40]))       # BIT #40
    rom.write_bytes(YOSHI_CARRY_SUB_ADDR + 0x06, bytearray([0xF0, 0x0A]))       # BEQ +0x0A
    rom.write_bytes(YOSHI_CARRY_SUB_ADDR + 0x08, bytearray([0xA9, 0x12]))       # LDA #12
    rom.write_bytes(YOSHI_CARRY_SUB_ADDR + 0x0A, bytearray([0x8D, 0xA3, 0x14])) # STA $14A3
    rom.write_bytes(YOSHI_CARRY_SUB_ADDR + 0x0D, bytearray([0xA9, 0x21]))       # LDA #21
    rom.write_bytes(YOSHI_CARRY_SUB_ADDR + 0x0F, bytearray([0x8D, 0xFC, 0x1D])) # STA $1DFC
    rom.write_bytes(YOSHI_CARRY_SUB_ADDR + 0x12, bytearray([0x28]))             # PLP
    rom.write_bytes(YOSHI_CARRY_SUB_ADDR + 0x13, bytearray([0x6B]))             # RTL
    # End Yoshi Carry

    # Climb
    rom.write_bytes(0x4D72, bytearray([0x5C, 0x88, 0xBA, 0x03])) # JML $03BA88
    rom.write_bytes(0x4D76, bytearray([0xEA] * 0x03))

    CLIMB_SUB_ADDR = 0x01BA88
    rom.write_bytes(CLIMB_SUB_ADDR + 0x00, bytearray([0x08]))                   # PHP
    rom.write_bytes(CLIMB_SUB_ADDR + 0x01, bytearray([0xAD, 0x1C, 0x1F]))       # LDA $1F1C
    rom.write_bytes(CLIMB_SUB_ADDR + 0x04, bytearray([0x89, 0x20]))             # BIT #20
    rom.write_bytes(CLIMB_SUB_ADDR + 0x06, bytearray([0xF0, 0x09]))             # BEQ +0x09
    rom.write_bytes(CLIMB_SUB_ADDR + 0x08, bytearray([0xA5, 0x8B]))             # LDA $8B
    rom.write_bytes(CLIMB_SUB_ADDR + 0x0A, bytearray([0x85, 0x74]))             # STA $74
    rom.write_bytes(CLIMB_SUB_ADDR + 0x0C, bytearray([0x28]))                   # PLP
    rom.write_bytes(CLIMB_SUB_ADDR + 0x0D, bytearray([0x5C, 0x17, 0xDB, 0x00])) # JML $00DB17
    rom.write_bytes(CLIMB_SUB_ADDR + 0x11, bytearray([0x28]))                   # PLP
    rom.write_bytes(CLIMB_SUB_ADDR + 0x12, bytearray([0x5C, 0x76, 0xCD, 0x00])) # JML $00CD76
    # End Climb

    # Climb Rope
    rom.write_bytes(0xDA33, bytearray([0x22, 0x70, 0xBC, 0x03])) # JSL $03BC70

    CLIMB_ROPE_SUB_ADDR = 0x01BC70
    rom.write_bytes(CLIMB_ROPE_SUB_ADDR + 0x00, bytearray([0x08]))             # PHP
    rom.write_bytes(CLIMB_ROPE_SUB_ADDR + 0x01, bytearray([0xAD, 0x1C, 0x1F])) # LDA $1F1C
    rom.write_bytes(CLIMB_ROPE_SUB_ADDR + 0x04, bytearray([0x89, 0x20]))       # BIT #20
    rom.write_bytes(CLIMB_ROPE_SUB_ADDR + 0x06, bytearray([0xF0, 0x07]))       # BEQ +0x07
    rom.write_bytes(CLIMB_ROPE_SUB_ADDR + 0x08, bytearray([0x28]))             # PLP
    rom.write_bytes(CLIMB_ROPE_SUB_ADDR + 0x09, bytearray([0xA9, 0xB0]))       # LDA #B0
    rom.write_bytes(CLIMB_ROPE_SUB_ADDR + 0x0B, bytearray([0x85, 0x7D]))       # STA $7D
    rom.write_bytes(CLIMB_ROPE_SUB_ADDR + 0x0D, bytearray([0x80, 0x01]))       # BRA +0x01
    rom.write_bytes(CLIMB_ROPE_SUB_ADDR + 0x0F, bytearray([0x28]))             # PLP
    rom.write_bytes(CLIMB_ROPE_SUB_ADDR + 0x10, bytearray([0x6B]))             # RTL
    # End Climb Rope

    # P-Switch
    rom.write_bytes(0xAB1A, bytearray([0x22, 0xA0, 0xBA, 0x03])) # JSL $03BAA0
    rom.write_bytes(0xAB1E, bytearray([0xEA] * 0x01))

    P_SWITCH_SUB_ADDR = 0x01BAA0
    rom.write_bytes(P_SWITCH_SUB_ADDR + 0x00, bytearray([0x08]))             # PHP
    rom.write_bytes(P_SWITCH_SUB_ADDR + 0x01, bytearray([0xAD, 0x1C, 0x1F])) # LDA $1F1C
    rom.write_bytes(P_SWITCH_SUB_ADDR + 0x04, bytearray([0x89, 0x10]))       # BIT #10
    rom.write_bytes(P_SWITCH_SUB_ADDR + 0x06, bytearray([0xF0, 0x04]))       # BEQ +0x04
    rom.write_bytes(P_SWITCH_SUB_ADDR + 0x08, bytearray([0xA9, 0xB0]))       # LDA #B0
    rom.write_bytes(P_SWITCH_SUB_ADDR + 0x0A, bytearray([0x80, 0x02]))       # BRA +0x02
    rom.write_bytes(P_SWITCH_SUB_ADDR + 0x0C, bytearray([0xA9, 0x01]))       # LDA #01
    rom.write_bytes(P_SWITCH_SUB_ADDR + 0x0E, bytearray([0x99, 0xAD, 0x14])) # STA $14AD
    rom.write_bytes(P_SWITCH_SUB_ADDR + 0x11, bytearray([0x28]))             # PLP
    rom.write_bytes(P_SWITCH_SUB_ADDR + 0x12, bytearray([0x6B]))             # RTL
    # End P-Switch

    # Spin Jump
    rom.write_bytes(0x5645, bytearray([0xAD, 0x1C, 0x1F]))       # LDA $1F1C
    rom.write_bytes(0x5648, bytearray([0x89, 0x08]))             # BIT #08
    rom.write_bytes(0x564A, bytearray([0xF0, 0x12]))             # BEQ +0x12
    rom.write_bytes(0x564C, bytearray([0x22, 0xB8, 0xBA, 0x03])) # JSL $03BAB8

    SPIN_JUMP_SUB_ADDR = 0x01BAB8
    rom.write_bytes(SPIN_JUMP_SUB_ADDR + 0x00, bytearray([0x08]))             # PHP
    rom.write_bytes(SPIN_JUMP_SUB_ADDR + 0x01, bytearray([0x1A]))             # INC
    rom.write_bytes(SPIN_JUMP_SUB_ADDR + 0x02, bytearray([0x8D, 0x0D, 0x14])) # STA $140D
    rom.write_bytes(SPIN_JUMP_SUB_ADDR + 0x05, bytearray([0xA9, 0x04]))       # LDA #04
    rom.write_bytes(SPIN_JUMP_SUB_ADDR + 0x07, bytearray([0x8D, 0xFC, 0x1D])) # STA $1DFC
    rom.write_bytes(SPIN_JUMP_SUB_ADDR + 0x0A, bytearray([0xA4, 0x76]))       # LDY #76
    rom.write_bytes(SPIN_JUMP_SUB_ADDR + 0x0C, bytearray([0x28]))             # PLP
    rom.write_bytes(SPIN_JUMP_SUB_ADDR + 0x0D, bytearray([0x6B]))             # RTL
    # End Spin Jump

    # Spin Jump from Water
    rom.write_bytes(0x6A89, bytearray([0x22, 0xF8, 0xBB, 0x03])) # JSL $03BBF8
    rom.write_bytes(0x6A8D, bytearray([0xEA] * 0x05))

    SPIN_JUMP_WATER_SUB_ADDR = 0x01BBF8
    rom.write_bytes(SPIN_JUMP_WATER_SUB_ADDR + 0x00, bytearray([0x08]))             # PHP
    rom.write_bytes(SPIN_JUMP_WATER_SUB_ADDR + 0x01, bytearray([0xAD, 0x1C, 0x1F])) # LDA $1F1C
    rom.write_bytes(SPIN_JUMP_WATER_SUB_ADDR + 0x04, bytearray([0x89, 0x08]))       # BIT #08
    rom.write_bytes(SPIN_JUMP_WATER_SUB_ADDR + 0x06, bytearray([0xF0, 0x09]))       # BEQ +0x09
    rom.write_bytes(SPIN_JUMP_WATER_SUB_ADDR + 0x08, bytearray([0x1A]))             # INC
    rom.write_bytes(SPIN_JUMP_WATER_SUB_ADDR + 0x09, bytearray([0x8D, 0x0D, 0x14])) # STA $140D
    rom.write_bytes(SPIN_JUMP_WATER_SUB_ADDR + 0x0C, bytearray([0xA9, 0x04]))       # LDA #04
    rom.write_bytes(SPIN_JUMP_WATER_SUB_ADDR + 0x0E, bytearray([0x8D, 0xFC, 0x1D])) # STA $1DFC
    rom.write_bytes(SPIN_JUMP_WATER_SUB_ADDR + 0x11, bytearray([0x28]))             # PLP
    rom.write_bytes(SPIN_JUMP_WATER_SUB_ADDR + 0x12, bytearray([0x6B]))             # RTL
    # End Spin Jump from Water

    # Spin Jump from Springboard
    rom.write_bytes(0xE693, bytearray([0x22, 0x0C, 0xBC, 0x03])) # JSL $03BC0C
    rom.write_bytes(0xE697, bytearray([0xEA] * 0x01))

    SPIN_JUMP_SPRING_SUB_ADDR = 0x01BC0C
    rom.write_bytes(SPIN_JUMP_SPRING_SUB_ADDR + 0x00, bytearray([0x08]))             # PHP
    rom.write_bytes(SPIN_JUMP_SPRING_SUB_ADDR + 0x01, bytearray([0xAD, 0x1C, 0x1F])) # LDA $1F1C
    rom.write_bytes(SPIN_JUMP_SPRING_SUB_ADDR + 0x04, bytearray([0x89, 0x08]))       # BIT #08
    rom.write_bytes(SPIN_JUMP_SPRING_SUB_ADDR + 0x06, bytearray([0xF0, 0x05]))       # BEQ +0x05
    rom.write_bytes(SPIN_JUMP_SPRING_SUB_ADDR + 0x08, bytearray([0xA9, 0x01]))       # LDA #01
    rom.write_bytes(SPIN_JUMP_SPRING_SUB_ADDR + 0x0A, bytearray([0x8D, 0x0D, 0x14])) # STA $140D
    rom.write_bytes(SPIN_JUMP_SPRING_SUB_ADDR + 0x0D, bytearray([0x28]))             # PLP
    rom.write_bytes(SPIN_JUMP_SPRING_SUB_ADDR + 0x0E, bytearray([0x6B]))             # RTL
    # End Spin Jump from Springboard

    # Swim
    rom.write_bytes(0x5A25, bytearray([0x22, 0xC8, 0xBA, 0x03])) # JSL $03BAC8
    rom.write_bytes(0x5A29, bytearray([0xEA] * 0x04))

    SWIM_SUB_ADDR = 0x01BAC8
    rom.write_bytes(SWIM_SUB_ADDR + 0x00, bytearray([0x48]))             # PHA
    rom.write_bytes(SWIM_SUB_ADDR + 0x01, bytearray([0x08]))             # PHP
    rom.write_bytes(SWIM_SUB_ADDR + 0x02, bytearray([0xAD, 0x1C, 0x1F])) # LDA $1F1C
    rom.write_bytes(SWIM_SUB_ADDR + 0x05, bytearray([0x89, 0x04]))       # BIT #04
    rom.write_bytes(SWIM_SUB_ADDR + 0x07, bytearray([0xF0, 0x0C]))       # BEQ +0x0C
    rom.write_bytes(SWIM_SUB_ADDR + 0x09, bytearray([0x28]))             # PLP
    rom.write_bytes(SWIM_SUB_ADDR + 0x0A, bytearray([0x68]))             # PLA
    rom.write_bytes(SWIM_SUB_ADDR + 0x0B, bytearray([0xDD, 0x84, 0xD9])) # CMP $D489, X
    rom.write_bytes(SWIM_SUB_ADDR + 0x0E, bytearray([0xB0, 0x03]))       # BCS +0x03
    rom.write_bytes(SWIM_SUB_ADDR + 0x10, bytearray([0xBD, 0x84, 0xD9])) # LDA $D489, X
    rom.write_bytes(SWIM_SUB_ADDR + 0x13, bytearray([0x80, 0x0A]))       # BRA +0x0A
    rom.write_bytes(SWIM_SUB_ADDR + 0x15, bytearray([0x28]))             # PLP
    rom.write_bytes(SWIM_SUB_ADDR + 0x16, bytearray([0x68]))             # PLA
    rom.write_bytes(SWIM_SUB_ADDR + 0x17, bytearray([0xDD, 0xBE, 0xDE])) # CMP $DEBE, X
    rom.write_bytes(SWIM_SUB_ADDR + 0x1A, bytearray([0xB0, 0x03]))       # BCS +0x03
    rom.write_bytes(SWIM_SUB_ADDR + 0x1C, bytearray([0xBD, 0xBE, 0xDE])) # LDA $DEBE, X
    rom.write_bytes(SWIM_SUB_ADDR + 0x1F, bytearray([0x6B]))             # RTL
    # End Swim

    # Item Swim
    rom.write_bytes(0x59D7, bytearray([0x22, 0xE8, 0xBA, 0x03])) # JSL $03BAE8
    rom.write_bytes(0x59DB, bytearray([0xEA] * 0x02))

    SWIM_SUB_ADDR = 0x01BAE8
    rom.write_bytes(SWIM_SUB_ADDR + 0x00, bytearray([0x48]))             # PHA
    rom.write_bytes(SWIM_SUB_ADDR + 0x01, bytearray([0x08]))             # PHP
    rom.write_bytes(SWIM_SUB_ADDR + 0x02, bytearray([0xAD, 0x1C, 0x1F])) # LDA $1F1C
    rom.write_bytes(SWIM_SUB_ADDR + 0x05, bytearray([0x89, 0x04]))       # BIT #04
    rom.write_bytes(SWIM_SUB_ADDR + 0x07, bytearray([0xF0, 0x0A]))       # BEQ +0x0A
    rom.write_bytes(SWIM_SUB_ADDR + 0x09, bytearray([0x28]))             # PLP
    rom.write_bytes(SWIM_SUB_ADDR + 0x0A, bytearray([0x68]))             # PLA
    rom.write_bytes(SWIM_SUB_ADDR + 0x0B, bytearray([0xC9, 0xF0]))       # CMP #F0
    rom.write_bytes(SWIM_SUB_ADDR + 0x0D, bytearray([0xB0, 0x02]))       # BCS +0x02
    rom.write_bytes(SWIM_SUB_ADDR + 0x0F, bytearray([0xA9, 0xF0]))       # LDA #F0
    rom.write_bytes(SWIM_SUB_ADDR + 0x11, bytearray([0x80, 0x08]))       # BRA +0x08
    rom.write_bytes(SWIM_SUB_ADDR + 0x13, bytearray([0x28]))             # PLP
    rom.write_bytes(SWIM_SUB_ADDR + 0x14, bytearray([0x68]))             # PLA
    rom.write_bytes(SWIM_SUB_ADDR + 0x15, bytearray([0xC9, 0xFF]))       # CMP #FF
    rom.write_bytes(SWIM_SUB_ADDR + 0x17, bytearray([0xB0, 0x02]))       # BCS +0x02
    rom.write_bytes(SWIM_SUB_ADDR + 0x19, bytearray([0xA9, 0x00]))       # LDA #00
    rom.write_bytes(SWIM_SUB_ADDR + 0x1B, bytearray([0x6B]))             # RTL
    # End Item Swim

    # Yoshi
    rom.write_bytes(0x109FB, bytearray([0x22, 0x08, 0xBB, 0x03])) # JSL $03BB08
    rom.write_bytes(0x109FF, bytearray([0xEA] * 0x02))

    YOSHI_SUB_ADDR = 0x01BB08
    rom.write_bytes(YOSHI_SUB_ADDR + 0x00, bytearray([0x08]))             # PHP
    rom.write_bytes(YOSHI_SUB_ADDR + 0x01, bytearray([0xAD, 0x1C, 0x1F])) # LDA $1F1C
    rom.write_bytes(YOSHI_SUB_ADDR + 0x04, bytearray([0x89, 0x02]))       # BIT #02
    rom.write_bytes(YOSHI_SUB_ADDR + 0x06, bytearray([0xF0, 0x06]))       # BEQ +0x06
    rom.write_bytes(YOSHI_SUB_ADDR + 0x08, bytearray([0x28]))             # PLP
    rom.write_bytes(YOSHI_SUB_ADDR + 0x09, bytearray([0xB9, 0xA1, 0x88])) # LDA $88A1, Y
    rom.write_bytes(YOSHI_SUB_ADDR + 0x0C, bytearray([0x80, 0x04]))       # BRA +0x04
    rom.write_bytes(YOSHI_SUB_ADDR + 0x0E, bytearray([0x28]))             # PLP
    rom.write_bytes(YOSHI_SUB_ADDR + 0x0F, bytearray([0xB9, 0xA2, 0x88])) # LDA $88A2, Y
    rom.write_bytes(YOSHI_SUB_ADDR + 0x12, bytearray([0x9D, 0x1C, 0x15])) # STA $151C, X
    rom.write_bytes(YOSHI_SUB_ADDR + 0x15, bytearray([0x6B]))             # RTL
    # End Yoshi

    # Baby Yoshi
    rom.write_bytes(0xA2B8, bytearray([0x22, 0x20, 0xBB, 0x03])) # JSL $03BB20
    rom.write_bytes(0xA2BC, bytearray([0xEA] * 0x01))

    rom.write_bytes(0x1C05F, bytearray([0x22, 0x20, 0xBB, 0x03])) # JSL $03BB20
    rom.write_bytes(0x1C063, bytearray([0xEA] * 0x01))

    YOSHI_SUB_ADDR = 0x01BB20
    rom.write_bytes(YOSHI_SUB_ADDR + 0x00, bytearray([0x08]))             # PHP
    rom.write_bytes(YOSHI_SUB_ADDR + 0x01, bytearray([0x9C, 0x1E, 0x14])) # STZ $141E
    rom.write_bytes(YOSHI_SUB_ADDR + 0x04, bytearray([0xAD, 0x1C, 0x1F])) # LDA $1F1C
    rom.write_bytes(YOSHI_SUB_ADDR + 0x07, bytearray([0x89, 0x02]))       # BIT #02
    rom.write_bytes(YOSHI_SUB_ADDR + 0x09, bytearray([0xF0, 0x05]))       # BEQ +0x05
    rom.write_bytes(YOSHI_SUB_ADDR + 0x0B, bytearray([0x28]))             # PLP
    rom.write_bytes(YOSHI_SUB_ADDR + 0x0C, bytearray([0xA9, 0x35]))       # LDA #35
    rom.write_bytes(YOSHI_SUB_ADDR + 0x0E, bytearray([0x80, 0x03]))       # BRA +0x03
    rom.write_bytes(YOSHI_SUB_ADDR + 0x10, bytearray([0x28]))             # PLP
    rom.write_bytes(YOSHI_SUB_ADDR + 0x11, bytearray([0xA9, 0x70]))       # LDA #70
    rom.write_bytes(YOSHI_SUB_ADDR + 0x13, bytearray([0x6B]))             # RTL
    # End Baby Yoshi

    # Midway Gate
    rom.write_bytes(0x72E4, bytearray([0x22, 0x38, 0xBB, 0x03])) # JSL $03BB38

    MIDWAY_GATE_SUB_ADDR = 0x01BB38
    rom.write_bytes(MIDWAY_GATE_SUB_ADDR + 0x00, bytearray([0x08]))             # PHP
    rom.write_bytes(MIDWAY_GATE_SUB_ADDR + 0x01, bytearray([0xAD, 0x2D, 0x1F])) # LDA $1F2D
    rom.write_bytes(MIDWAY_GATE_SUB_ADDR + 0x04, bytearray([0x89, 0x01]))       # BIT #01
    rom.write_bytes(MIDWAY_GATE_SUB_ADDR + 0x06, bytearray([0xF0, 0x07]))       # BEQ +0x07
    rom.write_bytes(MIDWAY_GATE_SUB_ADDR + 0x08, bytearray([0x28]))             # PLP
    rom.write_bytes(MIDWAY_GATE_SUB_ADDR + 0x09, bytearray([0xA9, 0x01]))       # LDA #01
    rom.write_bytes(MIDWAY_GATE_SUB_ADDR + 0x0B, bytearray([0x85, 0x19]))       # STA $19
    rom.write_bytes(MIDWAY_GATE_SUB_ADDR + 0x0D, bytearray([0x80, 0x01]))       # BRA +0x01
    rom.write_bytes(MIDWAY_GATE_SUB_ADDR + 0x0F, bytearray([0x28]))             # PLP
    rom.write_bytes(MIDWAY_GATE_SUB_ADDR + 0x10, bytearray([0x6B]))             # RTL
    # End Midway Gate

    # Mushroom
    rom.write_bytes(0x5156, bytearray([0x22, 0x50, 0xBB, 0x03])) # JSL $03BB50
    rom.write_bytes(0x515A, bytearray([0xEA] * 0x04))

    MUSHROOM_SUB_ADDR = 0x01BB50
    rom.write_bytes(MUSHROOM_SUB_ADDR + 0x00, bytearray([0x08]))             # PHP
    rom.write_bytes(MUSHROOM_SUB_ADDR + 0x01, bytearray([0xAD, 0x2D, 0x1F])) # LDA $1F2D
    rom.write_bytes(MUSHROOM_SUB_ADDR + 0x04, bytearray([0x89, 0x01]))       # BIT #01
    rom.write_bytes(MUSHROOM_SUB_ADDR + 0x06, bytearray([0xF0, 0x05]))       # BEQ +0x05
    rom.write_bytes(MUSHROOM_SUB_ADDR + 0x08, bytearray([0x28]))             # PLP
    rom.write_bytes(MUSHROOM_SUB_ADDR + 0x09, bytearray([0xE6, 0x19]))       # INC $19
    rom.write_bytes(MUSHROOM_SUB_ADDR + 0x0B, bytearray([0x80, 0x01]))       # BRA +0x01
    rom.write_bytes(MUSHROOM_SUB_ADDR + 0x0D, bytearray([0x28]))             # PLP
    rom.write_bytes(MUSHROOM_SUB_ADDR + 0x0E, bytearray([0xA9, 0x00]))       # LDA #00
    rom.write_bytes(MUSHROOM_SUB_ADDR + 0x10, bytearray([0x85, 0x71]))       # STA $72
    rom.write_bytes(MUSHROOM_SUB_ADDR + 0x12, bytearray([0x64, 0x9D]))       # STZ $9D
    rom.write_bytes(MUSHROOM_SUB_ADDR + 0x14, bytearray([0x6B]))             # RTL
    # End Mushroom

    # Take Damage
    rom.write_bytes(0x5142, bytearray([0x22, 0x65, 0xBB, 0x03])) # JSL $03BB65
    rom.write_bytes(0x5146, bytearray([0x60] * 0x01))            # RTS

    DAMAGE_SUB_ADDR = 0x01BB65
    rom.write_bytes(DAMAGE_SUB_ADDR + 0x00, bytearray([0x8D, 0x97, 0x14])) # STA $1497
    rom.write_bytes(DAMAGE_SUB_ADDR + 0x03, bytearray([0x80, 0xF4]))       # BRA -0x0C
    # End Take Damage

    # Fire Flower Cycle
    rom.write_bytes(0x5187, bytearray([0x22, 0x6A, 0xBB, 0x03])) # JSL $03BB6A
    rom.write_bytes(0x518B, bytearray([0x60] * 0x01))            # RTS

    PALETTE_CYCLE_SUB_ADDR = 0x01BB6A
    rom.write_bytes(PALETTE_CYCLE_SUB_ADDR + 0x00, bytearray([0xCE, 0x9B, 0x14])) # DEC $149B
    rom.write_bytes(PALETTE_CYCLE_SUB_ADDR + 0x03, bytearray([0xF0, 0xEF]))       # BEQ -0x11
    rom.write_bytes(PALETTE_CYCLE_SUB_ADDR + 0x05, bytearray([0x6B]))             # RTL
    # End Fire Flower Cycle

    # Pipe Exit
    rom.write_bytes(0x526D, bytearray([0x22, 0x70, 0xBB, 0x03])) # JSL $03BB70
    rom.write_bytes(0x5271, bytearray([0x60, 0xEA] * 0x01))      # RTS, NOP

    PIPE_EXIT_SUB_ADDR = 0x01BB70
    rom.write_bytes(PIPE_EXIT_SUB_ADDR + 0x00, bytearray([0x9C, 0x19, 0x14])) # STZ $1419
    rom.write_bytes(PIPE_EXIT_SUB_ADDR + 0x03, bytearray([0xA9, 0x00]))       # LDA #00
    rom.write_bytes(PIPE_EXIT_SUB_ADDR + 0x05, bytearray([0x85, 0x71]))       # STA $72
    rom.write_bytes(PIPE_EXIT_SUB_ADDR + 0x07, bytearray([0x64, 0x9D]))       # STZ $9D
    rom.write_bytes(PIPE_EXIT_SUB_ADDR + 0x09, bytearray([0x6B]))             # RTL
    # End Pipe Exit

    # Cape Transform
    rom.write_bytes(0x5168, bytearray([0x22, 0x7A, 0xBB, 0x03])) # JSL $03BB7A
    rom.write_bytes(0x516C, bytearray([0xEA] * 0x01))            # RTS, NOP
    rom.write_bytes(0x516D, bytearray([0xF0, 0xD1]))             # BEQ -0x2F

    CAPE_TRANSFORM_SUB_ADDR = 0x01BB7A
    rom.write_bytes(CAPE_TRANSFORM_SUB_ADDR + 0x00, bytearray([0xA5, 0x19])) # LDA $19
    rom.write_bytes(CAPE_TRANSFORM_SUB_ADDR + 0x02, bytearray([0x4A]))       # LSR
    rom.write_bytes(CAPE_TRANSFORM_SUB_ADDR + 0x03, bytearray([0xD0, 0xDF])) # BNE -0x21
    rom.write_bytes(CAPE_TRANSFORM_SUB_ADDR + 0x05, bytearray([0x6B]))       # RTL
    # End Cape Transform

    # Fire Flower
    rom.write_bytes(0xC5F7, bytearray([0x22, 0x80, 0xBB, 0x03])) # JSL $03BB80

    FIRE_FLOWER_SUB_ADDR = 0x01BB80
    rom.write_bytes(FIRE_FLOWER_SUB_ADDR + 0x00, bytearray([0x08]))             # PHP
    rom.write_bytes(FIRE_FLOWER_SUB_ADDR + 0x01, bytearray([0xAD, 0x2D, 0x1F])) # LDA $1F2D
    rom.write_bytes(FIRE_FLOWER_SUB_ADDR + 0x04, bytearray([0x89, 0x02]))       # BIT #02
    rom.write_bytes(FIRE_FLOWER_SUB_ADDR + 0x06, bytearray([0xF0, 0x07]))       # BEQ +0x07
    rom.write_bytes(FIRE_FLOWER_SUB_ADDR + 0x08, bytearray([0x28]))             # PLP
    rom.write_bytes(FIRE_FLOWER_SUB_ADDR + 0x09, bytearray([0xA9, 0x03]))       # LDA #03
    rom.write_bytes(FIRE_FLOWER_SUB_ADDR + 0x0B, bytearray([0x85, 0x19]))       # STA $19
    rom.write_bytes(FIRE_FLOWER_SUB_ADDR + 0x0D, bytearray([0x80, 0x01]))       # BRA +0x01
    rom.write_bytes(FIRE_FLOWER_SUB_ADDR + 0x0F, bytearray([0x28]))             # PLP
    rom.write_bytes(FIRE_FLOWER_SUB_ADDR + 0x10, bytearray([0x6B]))             # RTL
    # End Fire Flower

    # Cape
    rom.write_bytes(0xC598, bytearray([0x22, 0x91, 0xBB, 0x03])) # JSL $03BB91

    CAPE_SUB_ADDR = 0x01BB91
    rom.write_bytes(CAPE_SUB_ADDR + 0x00, bytearray([0x08]))             # PHP
    rom.write_bytes(CAPE_SUB_ADDR + 0x01, bytearray([0xAD, 0x2D, 0x1F])) # LDA $1F2D
    rom.write_bytes(CAPE_SUB_ADDR + 0x04, bytearray([0x89, 0x04]))       # BIT #04
    rom.write_bytes(CAPE_SUB_ADDR + 0x06, bytearray([0xF0, 0x07]))       # BEQ +0x07
    rom.write_bytes(CAPE_SUB_ADDR + 0x08, bytearray([0x28]))             # PLP
    rom.write_bytes(CAPE_SUB_ADDR + 0x09, bytearray([0xA9, 0x02]))       # LDA #02
    rom.write_bytes(CAPE_SUB_ADDR + 0x0B, bytearray([0x85, 0x19]))       # STA $19
    rom.write_bytes(CAPE_SUB_ADDR + 0x0D, bytearray([0x80, 0x01]))       # BRA +0x01
    rom.write_bytes(CAPE_SUB_ADDR + 0x0F, bytearray([0x28]))             # PLP
    rom.write_bytes(CAPE_SUB_ADDR + 0x10, bytearray([0x6B]))             # RTL
    # End Cape

    # P-Balloon
    rom.write_bytes(0xC2FF, bytearray([0x22, 0xA2, 0xBB, 0x03])) # JSL $03BBA2
    rom.write_bytes(0xC303, bytearray([0xEA] * 0x06))

    P_BALLOON_SUB_ADDR = 0x01BBA2
    rom.write_bytes(P_BALLOON_SUB_ADDR + 0x00, bytearray([0x08]))             # PHP
    rom.write_bytes(P_BALLOON_SUB_ADDR + 0x01, bytearray([0xAD, 0x2D, 0x1F])) # LDA $1F2D
    rom.write_bytes(P_BALLOON_SUB_ADDR + 0x04, bytearray([0x89, 0x08]))       # BIT #08
    rom.write_bytes(P_BALLOON_SUB_ADDR + 0x06, bytearray([0xF0, 0x0D]))       # BEQ +0x0D
    rom.write_bytes(P_BALLOON_SUB_ADDR + 0x08, bytearray([0x28]))             # PLP
    rom.write_bytes(P_BALLOON_SUB_ADDR + 0x09, bytearray([0xA9, 0x09]))       # LDA #09
    rom.write_bytes(P_BALLOON_SUB_ADDR + 0x0B, bytearray([0x8D, 0xF3, 0x13])) # STA $13F3
    rom.write_bytes(P_BALLOON_SUB_ADDR + 0x0E, bytearray([0xA9, 0xFF]))       # LDA #FF
    rom.write_bytes(P_BALLOON_SUB_ADDR + 0x10, bytearray([0x8D, 0x91, 0x18])) # STA $1891
    rom.write_bytes(P_BALLOON_SUB_ADDR + 0x13, bytearray([0x80, 0x0B]))       # BRA +0x0B
    rom.write_bytes(P_BALLOON_SUB_ADDR + 0x15, bytearray([0x28]))             # PLP
    rom.write_bytes(P_BALLOON_SUB_ADDR + 0x16, bytearray([0xA9, 0x01]))       # LDA #01
    rom.write_bytes(P_BALLOON_SUB_ADDR + 0x18, bytearray([0x8D, 0xF3, 0x13])) # STA $13F3
    rom.write_bytes(P_BALLOON_SUB_ADDR + 0x1B, bytearray([0xA9, 0x01]))       # LDA #01
    rom.write_bytes(P_BALLOON_SUB_ADDR + 0x1D, bytearray([0x8D, 0x91, 0x18])) # STA $1891
    rom.write_bytes(P_BALLOON_SUB_ADDR + 0x20, bytearray([0x6B]))             # RTL
    # End P-Balloon

    # Star
    rom.write_bytes(0xC580, bytearray([0x22, 0xC8, 0xBB, 0x03])) # JSL $03BBC8
    rom.write_bytes(0xC584, bytearray([0xEA] * 0x01))

    STAR_SUB_ADDR = 0x01BBC8
    rom.write_bytes(STAR_SUB_ADDR + 0x00, bytearray([0x08]))             # PHP
    rom.write_bytes(STAR_SUB_ADDR + 0x01, bytearray([0xAD, 0x2D, 0x1F])) # LDA $1F2D
    rom.write_bytes(STAR_SUB_ADDR + 0x04, bytearray([0x89, 0x10]))       # BIT #10
    rom.write_bytes(STAR_SUB_ADDR + 0x06, bytearray([0xF0, 0x08]))       # BEQ +0x08
    rom.write_bytes(STAR_SUB_ADDR + 0x08, bytearray([0x28]))             # PLP
    rom.write_bytes(STAR_SUB_ADDR + 0x09, bytearray([0xA9, 0xFF]))       # LDA #FF
    rom.write_bytes(STAR_SUB_ADDR + 0x0B, bytearray([0x8D, 0x90, 0x14])) # STA $1490
    rom.write_bytes(STAR_SUB_ADDR + 0x0E, bytearray([0x80, 0x06]))       # BRA +0x06
    rom.write_bytes(STAR_SUB_ADDR + 0x10, bytearray([0x28]))             # PLP
    rom.write_bytes(STAR_SUB_ADDR + 0x11, bytearray([0xA9, 0x01]))       # LDA #01
    rom.write_bytes(STAR_SUB_ADDR + 0x13, bytearray([0x8D, 0x90, 0x14])) # STA $1490
    rom.write_bytes(STAR_SUB_ADDR + 0x16, bytearray([0x6B]))             # RTL
    # End Star

    # Star Timer
    rom.write_bytes(0x62E3, bytearray([0x22, 0xE0, 0xBB, 0x03])) # JSL $03BBE0

    STAR_TIMER_SUB_ADDR = 0x01BBE0
    rom.write_bytes(STAR_TIMER_SUB_ADDR + 0x00, bytearray([0x08]))             # PHP
    rom.write_bytes(STAR_TIMER_SUB_ADDR + 0x01, bytearray([0xAD, 0x2D, 0x1F])) # LDA $1F2D
    rom.write_bytes(STAR_TIMER_SUB_ADDR + 0x04, bytearray([0x89, 0x10]))       # BIT #10
    rom.write_bytes(STAR_TIMER_SUB_ADDR + 0x06, bytearray([0xF0, 0x07]))       # BEQ +0x07
    rom.write_bytes(STAR_TIMER_SUB_ADDR + 0x08, bytearray([0x28]))             # PLP
    rom.write_bytes(STAR_TIMER_SUB_ADDR + 0x09, bytearray([0xA5, 0x13]))       # LDA $13
    rom.write_bytes(STAR_TIMER_SUB_ADDR + 0x0B, bytearray([0xC0, 0x1E]))       # CPY #1E
    rom.write_bytes(STAR_TIMER_SUB_ADDR + 0x0D, bytearray([0x80, 0x05]))       # BRA +0x05
    rom.write_bytes(STAR_TIMER_SUB_ADDR + 0x0F, bytearray([0x28]))             # PLP
    rom.write_bytes(STAR_TIMER_SUB_ADDR + 0x10, bytearray([0xA5, 0x13]))       # LDA $13
    rom.write_bytes(STAR_TIMER_SUB_ADDR + 0x12, bytearray([0xC0, 0x01]))       # CPY #01
    rom.write_bytes(STAR_TIMER_SUB_ADDR + 0x14, bytearray([0x6B]))             # RTL
    # End Star Timer

    return


def handle_yoshi_box(rom):

    rom.write_bytes(0xEC3D, bytearray([0xEA] * 0x03)) # NOP Lines that cause Yoshi Rescue Box normally

    rom.write_bytes(0x2B20F, bytearray([0x20, 0x60, 0xDC])) # JSR $05DC60

    YOSHI_BOX_SUB_ADDR = 0x02DC60
    rom.write_bytes(YOSHI_BOX_SUB_ADDR + 0x00, bytearray([0x08]))                   # PHP
    rom.write_bytes(YOSHI_BOX_SUB_ADDR + 0x01, bytearray([0xAD, 0x26, 0x14]))       # LDA $1426
    rom.write_bytes(YOSHI_BOX_SUB_ADDR + 0x04, bytearray([0xC9, 0x03]))             # CMP #03
    rom.write_bytes(YOSHI_BOX_SUB_ADDR + 0x06, bytearray([0xF0, 0x06]))             # BEQ +0x06
    rom.write_bytes(YOSHI_BOX_SUB_ADDR + 0x08, bytearray([0x28]))                   # PLP
    rom.write_bytes(YOSHI_BOX_SUB_ADDR + 0x09, bytearray([0xB9, 0xD9, 0xA5]))       # LDA $A5B9, Y
    rom.write_bytes(YOSHI_BOX_SUB_ADDR + 0x0C, bytearray([0x80, 0x08]))             # BRA +0x08
    rom.write_bytes(YOSHI_BOX_SUB_ADDR + 0x0E, bytearray([0x28]))                   # PLP
    rom.write_bytes(YOSHI_BOX_SUB_ADDR + 0x0F, bytearray([0xDA]))                   # PHX
    rom.write_bytes(YOSHI_BOX_SUB_ADDR + 0x10, bytearray([0xBB]))                   # TYX
    rom.write_bytes(YOSHI_BOX_SUB_ADDR + 0x11, bytearray([0xBF, 0x00, 0xC2, 0x7E])) # LDA $7EC200, X
    rom.write_bytes(YOSHI_BOX_SUB_ADDR + 0x15, bytearray([0xFA]))                   # PLX
    rom.write_bytes(YOSHI_BOX_SUB_ADDR + 0x16, bytearray([0x60]))                   # RTS

    return


def handle_bowser_damage(rom):

    rom.write_bytes(0x1A509, bytearray([0x5C, 0x50, 0xBC, 0x03])) # JML $03BC50

    BOWSER_BALLS_SUB_ADDR = 0x01BC50
    rom.write_bytes(BOWSER_BALLS_SUB_ADDR + 0x0000, bytearray([0xAF, 0xA0, 0xBF, 0x03]))  # bowser_infinite_balls:  lda.l goal_setting
    rom.write_bytes(BOWSER_BALLS_SUB_ADDR + 0x0004, bytearray([0xD0, 0x0C]))              #                         bne .nope
    rom.write_bytes(BOWSER_BALLS_SUB_ADDR + 0x0006, bytearray([0xAD, 0x48, 0x0F]))        #                         lda $0F48
    rom.write_bytes(BOWSER_BALLS_SUB_ADDR + 0x0009, bytearray([0xCF, 0xA1, 0xBF, 0x03]))  #                         cmp.l required_bosses_setting
    rom.write_bytes(BOWSER_BALLS_SUB_ADDR + 0x000D, bytearray([0x90, 0x03]))              #                         bcc .nope
    rom.write_bytes(BOWSER_BALLS_SUB_ADDR + 0x000F, bytearray([0xEE, 0xB8, 0x14]))        #                         inc $14B8
    rom.write_bytes(BOWSER_BALLS_SUB_ADDR + 0x0012, bytearray([0xAD, 0xB8, 0x14]))        # .nope                   lda $14B8
    rom.write_bytes(BOWSER_BALLS_SUB_ADDR + 0x0015, bytearray([0x5C, 0x0F, 0xA5, 0x03]))  #                         jml $03A50F

    return


def handle_level_shuffle(rom, active_level_dict):
    rom.write_bytes(0x37600, bytearray([0x00] * 0x800)) # Duplicate Level Table

    rom.write_bytes(0x2D89C, bytearray([0x00, 0xF6, 0x06])) # Level Load Pointer
    rom.write_bytes(0x20F46, bytearray([0x00, 0xF6, 0x06])) # Mid Gate Pointer
    rom.write_bytes(0x20E7B, bytearray([0x00, 0xF6, 0x06])) # Level Name Pointer
    rom.write_bytes(0x21543, bytearray([0x00, 0xF6, 0x06])) # Also Level Name Pointer?
    rom.write_bytes(0x20F64, bytearray([0x00, 0xF6, 0x06])) # Level Beaten Pointer

    ### Fix Translevel Check
    rom.write_bytes(0x2D8AE, bytearray([0x20, 0x00, 0xDD]))       # JSR $DD00
    rom.write_bytes(0x2D8B1, bytearray([0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA])) # NOP NOP NOP NOP NOP

    rom.write_bytes(0x2D7CB, bytearray([0x20, 0x00, 0xDD]))       # JSR $DD00
    rom.write_bytes(0x2D7CE, bytearray([0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA])) # NOP NOP NOP NOP NOP

    rom.write_bytes(0x2DD00, bytearray([0xDA]))             # PHX
    rom.write_bytes(0x2DD01, bytearray([0x08]))             # PHP
    rom.write_bytes(0x2DD02, bytearray([0xE2, 0x30]))       # SEP #30
    rom.write_bytes(0x2DD04, bytearray([0xAE, 0xBF, 0x13])) # LDX $13BF
    rom.write_bytes(0x2DD07, bytearray([0xE0, 0x25]))       # CPX #25
    rom.write_bytes(0x2DD09, bytearray([0x90, 0x04]))       # BCC $DD0F
    rom.write_bytes(0x2DD0B, bytearray([0xA2, 0x01]))       # LDX #01
    rom.write_bytes(0x2DD0D, bytearray([0x80, 0x02]))       # BRA $DD11
    rom.write_bytes(0x2DD0F, bytearray([0xA2, 0x00]))       # LDX #00
    rom.write_bytes(0x2DD11, bytearray([0x86, 0x0F]))       # STX $0F
    rom.write_bytes(0x2DD13, bytearray([0x28]))             # PLP
    rom.write_bytes(0x2DD14, bytearray([0xFA]))             # PLX
    rom.write_bytes(0x2DD15, bytearray([0x60]))             # RTS
    ### End Fix Translevel Check

    ### Fix Snake Blocks
    rom.write_bytes(0x192FB, bytearray([0x20, 0x1D, 0xBC])) # JSR $03BC1D

    SNAKE_BLOCKS_SUB_ADDR = 0x01BC1D
    rom.write_bytes(SNAKE_BLOCKS_SUB_ADDR + 0x00, bytearray([0x08]))                   # PHP
    rom.write_bytes(SNAKE_BLOCKS_SUB_ADDR + 0x01, bytearray([0xAD, 0xBF, 0x13]))       # LDA $13BF
    rom.write_bytes(SNAKE_BLOCKS_SUB_ADDR + 0x04, bytearray([0xC9, 0x20]))             # CMP #20
    rom.write_bytes(SNAKE_BLOCKS_SUB_ADDR + 0x06, bytearray([0xF0, 0x05]))             # BEQ +0x05
    rom.write_bytes(SNAKE_BLOCKS_SUB_ADDR + 0x08, bytearray([0x28]))                   # PLP
    rom.write_bytes(SNAKE_BLOCKS_SUB_ADDR + 0x09, bytearray([0xA9, 0x01]))             # LDA #01
    rom.write_bytes(SNAKE_BLOCKS_SUB_ADDR + 0x0B, bytearray([0x80, 0x03]))             # BRA +0x03
    rom.write_bytes(SNAKE_BLOCKS_SUB_ADDR + 0x0D, bytearray([0x28]))                   # PLP
    rom.write_bytes(SNAKE_BLOCKS_SUB_ADDR + 0x0E, bytearray([0xA9, 0x00]))             # LDA #00
    rom.write_bytes(SNAKE_BLOCKS_SUB_ADDR + 0x10, bytearray([0x60]))                   # RTS
    ### End Fix Snake Blocks

    for level_id, level_data in level_info_dict.items():
        if level_id not in active_level_dict.keys():
            continue

        tile_id = active_level_dict[level_id]
        tile_data = level_info_dict[tile_id]

        if level_id > 0x80:
            level_id = level_id - 0x50

        rom.write_byte(tile_data.levelIDAddress, level_id)
        rom.write_byte(0x2D608 + level_id, tile_data.eventIDValue)

    for level_id, tile_id in active_level_dict.items():
        rom.write_byte(0x37F70 + level_id, tile_id)
        rom.write_byte(0x37F00 + tile_id, level_id)


def handle_collected_paths(rom):
    rom.write_bytes(0x1F5B, bytearray([0x22, 0x30, 0xBC, 0x03])) # JSL $03BC30
    rom.write_bytes(0x1F5F, bytearray([0xEA] * 0x02))

    COLLECTED_PATHS_SUB_ADDR = 0x01BC30
    rom.write_bytes(COLLECTED_PATHS_SUB_ADDR + 0x00, bytearray([0x08]))                   # PHP
    rom.write_bytes(COLLECTED_PATHS_SUB_ADDR + 0x01, bytearray([0xAD, 0x00, 0x01]))       # LDA $0100
    rom.write_bytes(COLLECTED_PATHS_SUB_ADDR + 0x04, bytearray([0xC9, 0x0B]))             # CMP #0B
    rom.write_bytes(COLLECTED_PATHS_SUB_ADDR + 0x06, bytearray([0xD0, 0x04]))             # BNE +0x04
    rom.write_bytes(COLLECTED_PATHS_SUB_ADDR + 0x08, bytearray([0x22, 0xAD, 0xDA, 0x04])) # JSL $04DAAD
    rom.write_bytes(COLLECTED_PATHS_SUB_ADDR + 0x0C, bytearray([0x28]))                   # PLP
    rom.write_bytes(COLLECTED_PATHS_SUB_ADDR + 0x0D, bytearray([0xEE, 0x00, 0x01]))       # INC $0100
    rom.write_bytes(COLLECTED_PATHS_SUB_ADDR + 0x10, bytearray([0xAD, 0xAF, 0x0D]))       # LDA $0DAF
    rom.write_bytes(COLLECTED_PATHS_SUB_ADDR + 0x13, bytearray([0x6B]))                   # RTL


def handle_vertical_scroll(rom):
    rom.write_bytes(0x285BA, bytearray([0x22, 0x80, 0xF4, 0x0F])) # JSL $0FF480

    VERTICAL_SCROLL_SUB_ADDR = 0x7F480
    rom.write_bytes(VERTICAL_SCROLL_SUB_ADDR + 0x0000, bytearray([0x4A]))                   # vertical_scroll:   lsr 
    rom.write_bytes(VERTICAL_SCROLL_SUB_ADDR + 0x0001, bytearray([0x4A]))                   #                    lsr 
    rom.write_bytes(VERTICAL_SCROLL_SUB_ADDR + 0x0002, bytearray([0x4A]))                   #                    lsr 
    rom.write_bytes(VERTICAL_SCROLL_SUB_ADDR + 0x0003, bytearray([0x4A]))                   #                    lsr 
    rom.write_bytes(VERTICAL_SCROLL_SUB_ADDR + 0x0004, bytearray([0x08]))                   #                    php 
    rom.write_bytes(VERTICAL_SCROLL_SUB_ADDR + 0x0005, bytearray([0xC9, 0x02]))             #                    cmp #$02
    rom.write_bytes(VERTICAL_SCROLL_SUB_ADDR + 0x0007, bytearray([0xD0, 0x0B]))             #                    bne +
    rom.write_bytes(VERTICAL_SCROLL_SUB_ADDR + 0x0009, bytearray([0xC2, 0x10]))             #                    rep #$10
    rom.write_bytes(VERTICAL_SCROLL_SUB_ADDR + 0x000B, bytearray([0xDA]))                   #                    phx 
    rom.write_bytes(VERTICAL_SCROLL_SUB_ADDR + 0x000C, bytearray([0xAE, 0x0B, 0x01]))       #                    ldx $010B
    rom.write_bytes(VERTICAL_SCROLL_SUB_ADDR + 0x000F, bytearray([0xBF, 0x00, 0xF5, 0x0F])) #                    lda.l vertical_scroll_levels,x
    rom.write_bytes(VERTICAL_SCROLL_SUB_ADDR + 0x0013, bytearray([0xFA]))                   #                    plx 
    rom.write_bytes(VERTICAL_SCROLL_SUB_ADDR + 0x0014, bytearray([0x28]))                   # +                  plp
    rom.write_bytes(VERTICAL_SCROLL_SUB_ADDR + 0x0015, bytearray([0x6B]))                   #                    rtl 

    vertical_scroll_table = [
        0x02, 0x01, 0x02, 0x02, 0x02, 0x01, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x01, 0x02, # Levels 000-00F
        0x01, 0x02, 0x02, 0x02, 0x02, 0x01, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x01, 0x02, 0x02, 0x02, # Levels 010-01F
        0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, # Levels 020-02F
        0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, # Levels 030-03F
        0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, # Levels 040-04F
        0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, # Levels 050-05F
        0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, # Levels 060-06F
        0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, # Levels 070-07F
        0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, # Levels 080-08F
        0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, # Levels 090-09F
        0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, # Levels 0A0-0AF
        0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, # Levels 0B0-0BF
        0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, # Levels 0C0-0CF
        0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x01, 0x02, # Levels 0D0-0DF
        0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x01, 0x02, 0x02, 0x02, 0x01, 0x02, 0x02, # Levels 0E0-0EF
        0x02, 0x02, 0x01, 0x02, 0x02, 0x01, 0x01, 0x02, 0x02, 0x01, 0x02, 0x02, 0x02, 0x02, 0x01, 0x02, # Levels 0F0-0FF
        0x02, 0x02, 0x02, 0x02, 0x02, 0x01, 0x01, 0x01, 0x02, 0x02, 0x02, 0x01, 0x02, 0x02, 0x02, 0x01, # Levels 100-10F
        0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x01, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x01, # Levels 110-11F
        0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, # Levels 120-12F
        0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, # Levels 130-13F
        0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, # Levels 140-14F
        0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, # Levels 150-15F
        0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, # Levels 160-16F
        0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, # Levels 170-17F
        0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, # Levels 180-18F
        0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, # Levels 190-19F
        0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, # Levels 1A0-1AF
        0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, # Levels 1B0-1BF
        0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, # Levels 1C0-1CF
        0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, # Levels 1D0-1DF
        0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, # Levels 1E0-1EF
        0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x01, 0x02, 0x02, 0x02, 0x02] # Levels 1F0-1FF

    rom.write_bytes(0x7F500, bytes(vertical_scroll_table))


def handle_bonus_block(rom):
    rom.write_bytes(0x71A5, bytearray([0x5C, 0x19, 0x8E, 0x05])) # JML $058E19

    BONUS_BLOCK_ADDR = 0x28E19
    rom.write_bytes(BONUS_BLOCK_ADDR + 0x00, bytearray([0xA9, 0x06]))               #           LDA #$06
    rom.write_bytes(BONUS_BLOCK_ADDR + 0x02, bytearray([0xAC, 0xC0, 0x0D]))         #           LDY $0DC0
    rom.write_bytes(BONUS_BLOCK_ADDR + 0x05, bytearray([0xD0, 0x1E]))               #           BNE IGNORE
    rom.write_bytes(BONUS_BLOCK_ADDR + 0x07, bytearray([0xDA]))                     #           PHX 
    rom.write_bytes(BONUS_BLOCK_ADDR + 0x08, bytearray([0xAD, 0xBF, 0x13]))         #           LDA $13BF
    rom.write_bytes(BONUS_BLOCK_ADDR + 0x0B, bytearray([0x4A]))                     #           LSR 
    rom.write_bytes(BONUS_BLOCK_ADDR + 0x0C, bytearray([0x4A]))                     #           LSR 
    rom.write_bytes(BONUS_BLOCK_ADDR + 0x0D, bytearray([0x4A]))                     #           LSR 
    rom.write_bytes(BONUS_BLOCK_ADDR + 0x0E, bytearray([0x48]))                     #           PHA 
    rom.write_bytes(BONUS_BLOCK_ADDR + 0x0F, bytearray([0xAD, 0xBF, 0x13]))         #           LDA $13BF
    rom.write_bytes(BONUS_BLOCK_ADDR + 0x12, bytearray([0x29, 0x07]))               #           AND #$07
    rom.write_bytes(BONUS_BLOCK_ADDR + 0x14, bytearray([0xAA]))                     #           TAX 
    rom.write_bytes(BONUS_BLOCK_ADDR + 0x15, bytearray([0xBF, 0x5B, 0xB3, 0x05]))   #           LDA $05B35B,x
    rom.write_bytes(BONUS_BLOCK_ADDR + 0x19, bytearray([0xFA]))                     #           PLX 
    rom.write_bytes(BONUS_BLOCK_ADDR + 0x1A, bytearray([0x1F, 0x00, 0xA0, 0x7F]))   #           ORA $7FA000,x
    rom.write_bytes(BONUS_BLOCK_ADDR + 0x1E, bytearray([0x9F, 0x00, 0xA0, 0x7F]))   #           STA $7FA000,x
    rom.write_bytes(BONUS_BLOCK_ADDR + 0x22, bytearray([0xFA]))                     #           PLX 
    rom.write_bytes(BONUS_BLOCK_ADDR + 0x23, bytearray([0xA9, 0x05]))               #           LDA #$05
    rom.write_bytes(BONUS_BLOCK_ADDR + 0x25, bytearray([0x5C, 0xD0, 0xF1, 0x00]))   # IGNORE:   JML $00F1D0


def handle_blocksanity(rom):
    import json 
    blocksanity_data = pkgutil.get_data(__name__, f"data/blocksanity.json").decode("utf-8")
    blocksanity_data = json.loads(blocksanity_data)
    blocksanity_coords = bytearray([])
    blocksanity_bytes = bytearray([])

    block_count = 0
    entries = 0
    for level_name, level_data in blocksanity_data.items():
        # Calculate blocksanity pointer
        if level_data == []:
            # Skip if the level doesn't have any data
            blocksanity_bytes += bytearray([0xFF, 0xFF])
            continue
        level_ptr = 0x80C0 + entries
        blocksanity_bytes += bytearray([level_ptr & 0xFF, (level_ptr >> 8) & 0xFF])
        
        # Get block data
        block_coords = bytearray([])
        for x in range(len(level_data)):
            block_coords += bytearray([
                int(level_data[x][1], 16) & 0xFF, (int(level_data[x][1], 16) >> 8) & 0xFF,
                int(level_data[x][2], 16) & 0xFF, (int(level_data[x][2], 16) >> 8) & 0xFF,
                block_count & 0xFF, (block_count >> 8) & 0xFF])
            entries += 6
            block_count += 1
        block_coords += bytearray([0xFF, 0xFF])
        entries += 2

        blocksanity_coords += block_coords

    blocksanity_bytes += blocksanity_coords

    rom.write_bytes(0x80000, blocksanity_bytes)
    rom.write_bytes(0x071D0, bytearray([0x5C, 0x00, 0xF7, 0x0F])) # org $00F1D0 : jml blocksanity_main
    rom.write_bytes(0x0AD59, bytearray([0x5C, 0x15, 0xF7, 0x0F])) # org $01AD5C : jml blocksanity_flying_init
    rom.write_bytes(0x0AE16, bytearray([0x22, 0x39, 0xF7, 0x0F])) # org $01AE16 : jsl blocksanity_flying_main

    BLOCKSANITY_ADDR = 0x7F700
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0000, bytearray([0x85, 0x05]))                       # blocksanity_main:           sta $05
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0002, bytearray([0x8B]))                             #                             phb 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0003, bytearray([0xA9, 0x10]))                       #                             lda.b #blocksanity_pointers>>16
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0005, bytearray([0x48]))                             #                             pha 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0006, bytearray([0xAB]))                             #                             plb 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0007, bytearray([0x5A]))                             #                             phy 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0008, bytearray([0x20, 0x63, 0xF7]))                 #                             jsr process_block
    rom.write_bytes(BLOCKSANITY_ADDR + 0x000B, bytearray([0x7A]))                             #                             ply 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x000C, bytearray([0xAB]))                             #                             plb 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x000D, bytearray([0xA5, 0x05]))                       #                             lda $05
    rom.write_bytes(BLOCKSANITY_ADDR + 0x000F, bytearray([0xC9, 0x05]))                       #                             cmp #$05
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0011, bytearray([0x5C, 0xD4, 0xF1, 0x00]))           #                             jml $00F1D4
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0015, bytearray([0xB5, 0xD8]))                       # blocksanity_flying_init:    lda $D8,x
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0017, bytearray([0x29, 0xF0]))                       #                             and #$F0
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0019, bytearray([0x9F, 0x20, 0xB8, 0x7F]))           #                             sta !sprite_blocksanity_y_lo,x
    rom.write_bytes(BLOCKSANITY_ADDR + 0x001D, bytearray([0xBD, 0xD4, 0x14]))                 #                             lda $14D4,x
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0020, bytearray([0x9F, 0x30, 0xB8, 0x7F]))           #                             sta !sprite_blocksanity_y_hi,x
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0024, bytearray([0xBD, 0xE0, 0x14]))                 #                             lda $14E0,x
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0027, bytearray([0x9F, 0x10, 0xB8, 0x7F]))           #                             sta !sprite_blocksanity_x_hi,x
    rom.write_bytes(BLOCKSANITY_ADDR + 0x002B, bytearray([0xB5, 0xE4]))                       #                             lda $E4,x
    rom.write_bytes(BLOCKSANITY_ADDR + 0x002D, bytearray([0x29, 0xF0]))                       #                             and #$F0
    rom.write_bytes(BLOCKSANITY_ADDR + 0x002F, bytearray([0x9F, 0x00, 0xB8, 0x7F]))           #                             sta !sprite_blocksanity_x_lo,x
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0033, bytearray([0x4A]))                             #                             lsr 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0034, bytearray([0x4A]))                             #                             lsr 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0035, bytearray([0x5C, 0x5D, 0xAD, 0x01]))           #                             jml $01AD5D
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0039, bytearray([0xBF, 0x20, 0xB8, 0x7F]))           # blocksanity_flying_main:    lda !sprite_blocksanity_y_lo,x
    rom.write_bytes(BLOCKSANITY_ADDR + 0x003D, bytearray([0x85, 0x98]))                       #                             sta $98
    rom.write_bytes(BLOCKSANITY_ADDR + 0x003F, bytearray([0xBF, 0x30, 0xB8, 0x7F]))           #                             lda !sprite_blocksanity_y_hi,x
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0043, bytearray([0x85, 0x99]))                       #                             sta $99
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0045, bytearray([0xBF, 0x00, 0xB8, 0x7F]))           #                             lda !sprite_blocksanity_x_lo,x
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0049, bytearray([0x85, 0x9A]))                       #                             sta $9A
    rom.write_bytes(BLOCKSANITY_ADDR + 0x004B, bytearray([0xBF, 0x10, 0xB8, 0x7F]))           #                             lda !sprite_blocksanity_x_hi,x
    rom.write_bytes(BLOCKSANITY_ADDR + 0x004F, bytearray([0x85, 0x9B]))                       #                             sta $9B
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0051, bytearray([0x8B]))                             #                             phb 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0052, bytearray([0xA9, 0x10]))                       #                             lda.b #blocksanity_pointers>>16
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0054, bytearray([0x48]))                             #                             pha 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0055, bytearray([0xAB]))                             #                             plb 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0056, bytearray([0x5A]))                             #                             phy 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0057, bytearray([0xDA]))                             #                             phx 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0058, bytearray([0x20, 0x63, 0xF7]))                 #                             jsr process_block
    rom.write_bytes(BLOCKSANITY_ADDR + 0x005B, bytearray([0xFA]))                             #                             plx 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x005C, bytearray([0x7A]))                             #                             ply 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x005D, bytearray([0xAB]))                             #                             plb 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x005E, bytearray([0xB5, 0xE4]))                       #                             lda $E4,x
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0060, bytearray([0x85, 0x9A]))                       #                             sta $9A
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0062, bytearray([0x6B]))                             #                             rtl 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0063, bytearray([0xA9, 0x0F]))                       # process_block:              lda #$0F
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0065, bytearray([0x14, 0x98]))                       #                             trb $98
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0067, bytearray([0x14, 0x9A]))                       #                             trb $9A
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0069, bytearray([0xC2, 0x30]))                       #                             rep #$30
    rom.write_bytes(BLOCKSANITY_ADDR + 0x006B, bytearray([0xA5, 0x60]))                       #                             lda $60
    rom.write_bytes(BLOCKSANITY_ADDR + 0x006D, bytearray([0x29, 0xFF, 0x00]))                 #                             and #$00FF
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0070, bytearray([0x0A]))                             #                             asl 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0071, bytearray([0x18]))                             #                             clc 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0072, bytearray([0x69, 0x00, 0x80]))                 #                             adc.w #blocksanity_pointers
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0075, bytearray([0x48]))                             #                             pha 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0076, bytearray([0xA0, 0x00, 0x00]))                 #                             ldy #$0000
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0079, bytearray([0xB3, 0x01]))                       #                             lda ($01,s),y
    rom.write_bytes(BLOCKSANITY_ADDR + 0x007B, bytearray([0x48]))                             #                             pha 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x007C, bytearray([0xB3, 0x01]))                       # .loop                       lda ($01,s),y
    rom.write_bytes(BLOCKSANITY_ADDR + 0x007E, bytearray([0xC9, 0xFF, 0xFF]))                 #                             cmp #$FFFF
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0081, bytearray([0xF0, 0x16]))                       #                             beq .return
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0083, bytearray([0xC5, 0x9A]))                       #                             cmp $9A
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0085, bytearray([0xD0, 0x0A]))                       #                             bne .next_block_x
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0087, bytearray([0xC8]))                             #                             iny 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0088, bytearray([0xC8]))                             #                             iny 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0089, bytearray([0xB3, 0x01]))                       #                             lda ($01,s),y
    rom.write_bytes(BLOCKSANITY_ADDR + 0x008B, bytearray([0xC5, 0x98]))                       #                             cmp $98
    rom.write_bytes(BLOCKSANITY_ADDR + 0x008D, bytearray([0xF0, 0x0F]))                       #                             beq .valid_block
    rom.write_bytes(BLOCKSANITY_ADDR + 0x008F, bytearray([0x80, 0x02]))                       #                             bra .next_block_y
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0091, bytearray([0xC8]))                             # .next_block_x               iny 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0092, bytearray([0xC8]))                             #                             iny 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0093, bytearray([0xC8]))                             # .next_block_y               iny 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0094, bytearray([0xC8]))                             #                             iny 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0095, bytearray([0xC8]))                             #                             iny 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0096, bytearray([0xC8]))                             #                             iny 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0097, bytearray([0x80, 0xE3]))                       #                             bra .loop
    rom.write_bytes(BLOCKSANITY_ADDR + 0x0099, bytearray([0x68]))                             # .return                     pla 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x009A, bytearray([0x68]))                             #                             pla 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x009B, bytearray([0xE2, 0x30]))                       #                             sep #$30
    rom.write_bytes(BLOCKSANITY_ADDR + 0x009D, bytearray([0x60]))                             #                             rts 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x009E, bytearray([0xC8]))                             # .valid_block                iny 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x009F, bytearray([0xC8]))                             #                             iny 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00A0, bytearray([0xB3, 0x01]))                       #                             lda ($01,s),y
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00A2, bytearray([0xAA]))                             #                             tax 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00A3, bytearray([0xE2, 0x20]))                       #                             sep #$20
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00A5, bytearray([0xDA]))                             #                             phx 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00A6, bytearray([0xBF, 0x00, 0xA4, 0x7F]))           #                             lda !blocksanity_data_flags,x
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00AA, bytearray([0xD0, 0x08]))                       #                             bne .processed
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00AC, bytearray([0x1A]))                             #                             inc 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00AD, bytearray([0x9F, 0x00, 0xA4, 0x7F]))           #                             sta !blocksanity_data_flags,x
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00B1, bytearray([0x20, 0xBA, 0xF7]))                 #                             jsr blocksanity_check_flags
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00B4, bytearray([0xFA]))                             # .processed                  plx 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00B5, bytearray([0xFA]))                             #                             plx 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00B6, bytearray([0xFA]))                             #                             plx 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00B7, bytearray([0xE2, 0x10]))                       #                             sep #$10
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00B9, bytearray([0x60]))                             #                             rts 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00BA, bytearray([0xC2, 0x20]))                       # blocksanity_check_flags:    rep #$20
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00BC, bytearray([0xA0, 0x00, 0x00]))                 #                             ldy #$0000
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00BF, bytearray([0xB3, 0x05]))                       # .loop                       lda ($05,s),y
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00C1, bytearray([0xC9, 0xFF, 0xFF]))                 #                             cmp #$FFFF
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00C4, bytearray([0xF0, 0x14]))                       #                             beq .check
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00C6, bytearray([0xC8]))                             #                             iny 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00C7, bytearray([0xC8]))                             #                             iny 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00C8, bytearray([0xC8]))                             #                             iny 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00C9, bytearray([0xC8]))                             #                             iny 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00CA, bytearray([0xB3, 0x05]))                       #                             lda ($05,s),y
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00CC, bytearray([0xAA]))                             #                             tax 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00CD, bytearray([0xBF, 0x00, 0xA4, 0x7F]))           #                             lda !blocksanity_data_flags,x
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00D1, bytearray([0x29, 0xFF, 0x00]))                 #                             and #$00FF
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00D4, bytearray([0xF0, 0x22]))                       #                             beq .invalid
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00D6, bytearray([0xC8]))                             #                             iny 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00D7, bytearray([0xC8]))                             #                             iny 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00D8, bytearray([0x80, 0xE5]))                       #                             bra .loop
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00DA, bytearray([0xE2, 0x20]))                       # .check                      sep #$20
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00DC, bytearray([0xA9, 0x00]))                       #                             lda #$00
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00DE, bytearray([0xEB]))                             #                             xba 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00DF, bytearray([0xA5, 0x60]))                       #                             lda $60
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00E1, bytearray([0x4A]))                             #                             lsr 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00E2, bytearray([0x4A]))                             #                             lsr 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00E3, bytearray([0x4A]))                             #                             lsr 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00E4, bytearray([0xA8]))                             #                             tay 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00E5, bytearray([0xA5, 0x60]))                       #                             lda $60
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00E7, bytearray([0x29, 0x07]))                       #                             and #$07
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00E9, bytearray([0xAA]))                             #                             tax 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00EA, bytearray([0xBF, 0x5B, 0xB3, 0x05]))           #                             lda.l $05B35B,x
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00EE, bytearray([0xBB]))                             #                             tyx 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00EF, bytearray([0x1F, 0x10, 0xA0, 0x7F]))           #                             ora !blocksanity_flags,x
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00F3, bytearray([0x9F, 0x10, 0xA0, 0x7F]))           #                             sta !blocksanity_flags,x
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00F7, bytearray([0x60]))                             #                             rts 
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00F8, bytearray([0xE2, 0x20]))                       # .invalid                    sep #$20
    rom.write_bytes(BLOCKSANITY_ADDR + 0x00FA, bytearray([0x60]))                             #                             rts 

def handle_ram(rom):
    rom.write_byte(0x07FD8, 0x02)                                 # Expand SRAM
    rom.write_bytes(0x01CF5, bytearray([0x5C, 0x00, 0xF2, 0x0F])) # org $009CF5 : jml init_sram
    rom.write_bytes(0x01C0F, bytearray([0x5C, 0x00, 0xF3, 0x0F])) # org $009C0F : jml save_sram
    rom.write_bytes(0x013BB, bytearray([0x5C, 0xA0, 0xF0, 0x0F])) # org $0093BB : jml init_ram

    INIT_SRAM_ADDR = 0x7F200
    rom.write_bytes(INIT_SRAM_ADDR + 0x0000, bytearray([0xD0, 0x74]))               # init_sram:              bne .clear
    rom.write_bytes(INIT_SRAM_ADDR + 0x0002, bytearray([0x9C, 0x09, 0x01]))         #                         stz $0109
    rom.write_bytes(INIT_SRAM_ADDR + 0x0005, bytearray([0xDA]))                     #                         phx 
    rom.write_bytes(INIT_SRAM_ADDR + 0x0006, bytearray([0x08]))                     #                         php
    rom.write_bytes(INIT_SRAM_ADDR + 0x0007, bytearray([0xE2, 0x10]))               #                         sep #$10
    rom.write_bytes(INIT_SRAM_ADDR + 0x0009, bytearray([0xA2, 0x5F]))               #                         ldx.b #$5F
    rom.write_bytes(INIT_SRAM_ADDR + 0x000B, bytearray([0xBF, 0x00, 0x08, 0x70]))   # -                       lda !level_clears_sram,x
    rom.write_bytes(INIT_SRAM_ADDR + 0x000F, bytearray([0x9F, 0x00, 0xA2, 0x7F]))   #                         sta !level_clears,x
    rom.write_bytes(INIT_SRAM_ADDR + 0x0013, bytearray([0xCA]))                     #                         dex 
    rom.write_bytes(INIT_SRAM_ADDR + 0x0014, bytearray([0x10, 0xF5]))               #                         bpl -
    rom.write_bytes(INIT_SRAM_ADDR + 0x0016, bytearray([0xA2, 0x0B]))               #                         ldx #$0B
    rom.write_bytes(INIT_SRAM_ADDR + 0x0018, bytearray([0xBF, 0x40, 0x09, 0x70]))   # -                       lda !blocksanity_sram,x
    rom.write_bytes(INIT_SRAM_ADDR + 0x001C, bytearray([0x9F, 0x10, 0xA0, 0x7F]))   #                         sta !blocksanity_flags,x
    rom.write_bytes(INIT_SRAM_ADDR + 0x0020, bytearray([0xBF, 0x10, 0x09, 0x70]))   #                         lda !moons_sram,x
    rom.write_bytes(INIT_SRAM_ADDR + 0x0024, bytearray([0x9D, 0xEE, 0x1F]))         #                         sta !moons_flags,x 
    rom.write_bytes(INIT_SRAM_ADDR + 0x0027, bytearray([0xBF, 0x00, 0x09, 0x70]))   #                         lda !yoshi_coins_sram,x
    rom.write_bytes(INIT_SRAM_ADDR + 0x002B, bytearray([0x9D, 0x2F, 0x1F]))         #                         sta !yoshi_coins_flags,x
    rom.write_bytes(INIT_SRAM_ADDR + 0x002E, bytearray([0xBF, 0x30, 0x09, 0x70]))   #                         lda !bonus_block_sram,x
    rom.write_bytes(INIT_SRAM_ADDR + 0x0032, bytearray([0x9F, 0x00, 0xA0, 0x7F]))   #                         sta !bonus_block_flags,x
    rom.write_bytes(INIT_SRAM_ADDR + 0x0036, bytearray([0xBF, 0x20, 0x09, 0x70]))   #                         lda !checkpoints_sram,x
    rom.write_bytes(INIT_SRAM_ADDR + 0x003A, bytearray([0x9D, 0x3C, 0x1F]))         #                         sta !checkpoints_flags,x
    rom.write_bytes(INIT_SRAM_ADDR + 0x003D, bytearray([0xCA]))                     #                         dex 
    rom.write_bytes(INIT_SRAM_ADDR + 0x003E, bytearray([0x10, 0xD8]))               #                         bpl -
    rom.write_bytes(INIT_SRAM_ADDR + 0x0040, bytearray([0xC2, 0x10]))               #                         rep #$10
    rom.write_bytes(INIT_SRAM_ADDR + 0x0042, bytearray([0xA2, 0x45, 0x02]))         #                         ldx.w #!blocksanity_locs-1
    rom.write_bytes(INIT_SRAM_ADDR + 0x0045, bytearray([0xBF, 0x00, 0x0A, 0x70]))   # -                       lda !blocksanity_data_sram,x
    rom.write_bytes(INIT_SRAM_ADDR + 0x0049, bytearray([0x9F, 0x00, 0xA4, 0x7F]))   #                         sta !blocksanity_data_flags,x
    rom.write_bytes(INIT_SRAM_ADDR + 0x004D, bytearray([0xCA]))                     #                         dex 
    rom.write_bytes(INIT_SRAM_ADDR + 0x004E, bytearray([0x10, 0xF5]))               #                         bpl -
    rom.write_bytes(INIT_SRAM_ADDR + 0x0050, bytearray([0xE2, 0x10]))               #                         sep #$10
    #rom.write_bytes(INIT_SRAM_ADDR + 0x0052, bytearray([0xAF, 0x50, 0x09, 0x70]))   #                         lda !received_items_count_sram+$00
    #rom.write_bytes(INIT_SRAM_ADDR + 0x0056, bytearray([0x8F, 0x0E, 0xA0, 0x7F]))   #                         sta !received_items_count+$00
    #rom.write_bytes(INIT_SRAM_ADDR + 0x005A, bytearray([0xAF, 0x51, 0x09, 0x70]))   #                         lda !received_items_count_sram+$01
    #rom.write_bytes(INIT_SRAM_ADDR + 0x005E, bytearray([0x8F, 0x0F, 0xA0, 0x7F]))   #                         sta !received_items_count+$01
    rom.write_bytes(INIT_SRAM_ADDR + 0x0052, bytearray([0xEA] * 0x17))              # Ugly, will apply be better when we port everything to a Base Patch
    #rom.write_bytes(INIT_SRAM_ADDR + 0x0062, bytearray([0xAF, 0x52, 0x09, 0x70]))   #                         lda !special_world_clear_sram
    #rom.write_bytes(INIT_SRAM_ADDR + 0x0066, bytearray([0x8D, 0xFF, 0x1F]))         #                         sta !special_world_clear_flag
    rom.write_bytes(INIT_SRAM_ADDR + 0x0069, bytearray([0xAF, 0x54, 0x09, 0x70]))   #                         lda !goal_item_count_sram
    rom.write_bytes(INIT_SRAM_ADDR + 0x006D, bytearray([0x8F, 0x1E, 0xA0, 0x7F]))   #                         sta !goal_item_count
    rom.write_bytes(INIT_SRAM_ADDR + 0x0071, bytearray([0x28]))                     #                         plp 
    rom.write_bytes(INIT_SRAM_ADDR + 0x0072, bytearray([0x5C, 0xFB, 0x9C, 0x00]))   #                         jml $009CFB
    rom.write_bytes(INIT_SRAM_ADDR + 0x0076, bytearray([0xDA]))                     # .clear                  phx 
    rom.write_bytes(INIT_SRAM_ADDR + 0x0077, bytearray([0xA2, 0x5F, 0x00]))         #                         ldx.w #$005F
    rom.write_bytes(INIT_SRAM_ADDR + 0x007A, bytearray([0xA9, 0x00]))               #                         lda #$00
    rom.write_bytes(INIT_SRAM_ADDR + 0x007C, bytearray([0x9F, 0x00, 0x08, 0x70]))   # -                       sta !level_clears_sram,x
    rom.write_bytes(INIT_SRAM_ADDR + 0x0080, bytearray([0xCA]))                     #                         dex 
    rom.write_bytes(INIT_SRAM_ADDR + 0x0081, bytearray([0x10, 0xF9]))               #                         bpl -
    rom.write_bytes(INIT_SRAM_ADDR + 0x0083, bytearray([0xA2, 0x0B, 0x00]))         #                         ldx.w #$000B
    rom.write_bytes(INIT_SRAM_ADDR + 0x0086, bytearray([0x9F, 0x40, 0x09, 0x70]))   # -                       sta !blocksanity_sram,x
    rom.write_bytes(INIT_SRAM_ADDR + 0x008A, bytearray([0x9F, 0x00, 0x09, 0x70]))   #                         sta !yoshi_coins_sram,x
    rom.write_bytes(INIT_SRAM_ADDR + 0x008E, bytearray([0x9F, 0x30, 0x09, 0x70]))   #                         sta !bonus_block_sram,x
    rom.write_bytes(INIT_SRAM_ADDR + 0x0092, bytearray([0x9F, 0x10, 0x09, 0x70]))   #                         sta !moons_sram,x
    rom.write_bytes(INIT_SRAM_ADDR + 0x0096, bytearray([0x9F, 0x20, 0x09, 0x70]))   #                         sta !checkpoints_sram,x
    rom.write_bytes(INIT_SRAM_ADDR + 0x009A, bytearray([0xCA]))                     #                         dex 
    rom.write_bytes(INIT_SRAM_ADDR + 0x009B, bytearray([0x10, 0xE9]))               #                         bpl -
    rom.write_bytes(INIT_SRAM_ADDR + 0x009D, bytearray([0xA2, 0x45, 0x02]))         #                         ldx.w #!blocksanity_locs-1
    rom.write_bytes(INIT_SRAM_ADDR + 0x00A0, bytearray([0x9F, 0x00, 0x0A, 0x70]))   # -                       sta !blocksanity_data_sram,x
    rom.write_bytes(INIT_SRAM_ADDR + 0x00A4, bytearray([0xCA]))                     #                         dex 
    rom.write_bytes(INIT_SRAM_ADDR + 0x00A5, bytearray([0x10, 0xF9]))               #                         bpl -
    rom.write_bytes(INIT_SRAM_ADDR + 0x00A7, bytearray([0x8F, 0x52, 0x09, 0x70]))   #                         sta !special_world_clear_sram
    rom.write_bytes(INIT_SRAM_ADDR + 0x00AB, bytearray([0x8F, 0x50, 0x09, 0x70]))   #                         sta !received_items_count_sram+$00
    rom.write_bytes(INIT_SRAM_ADDR + 0x00AF, bytearray([0x8F, 0x51, 0x09, 0x70]))   #                         sta !received_items_count_sram+$01
    rom.write_bytes(INIT_SRAM_ADDR + 0x00B3, bytearray([0x8F, 0x54, 0x09, 0x70]))   #                         sta !goal_item_count_sram
    rom.write_bytes(INIT_SRAM_ADDR + 0x00B7, bytearray([0xFA]))                     #                         plx 
    rom.write_bytes(INIT_SRAM_ADDR + 0x00B8, bytearray([0x5C, 0x22, 0x9D, 0x00]))   #                         jml $009D22

    SAVE_SRAM_ADDR = 0x7F300
    rom.write_bytes(SAVE_SRAM_ADDR + 0x0000, bytearray([0xE2, 0x30]))                         # save_sram:                  sep #$30
    rom.write_bytes(SAVE_SRAM_ADDR + 0x0002, bytearray([0xAB]))                               #                             plb 
    rom.write_bytes(SAVE_SRAM_ADDR + 0x0003, bytearray([0xA2, 0x5F]))                         #                             ldx.b #$5F
    rom.write_bytes(SAVE_SRAM_ADDR + 0x0005, bytearray([0xBF, 0x00, 0xA2, 0x7F]))             # -                           lda !level_clears,x
    rom.write_bytes(SAVE_SRAM_ADDR + 0x0009, bytearray([0x9F, 0x00, 0x08, 0x70]))             #                             sta !level_clears_sram,x 
    rom.write_bytes(SAVE_SRAM_ADDR + 0x000D, bytearray([0xCA]))                               #                             dex 
    rom.write_bytes(SAVE_SRAM_ADDR + 0x000E, bytearray([0x10, 0xF5]))                         #                             bpl -
    rom.write_bytes(SAVE_SRAM_ADDR + 0x0010, bytearray([0xA2, 0x0B]))                         #                             ldx #$0B
    rom.write_bytes(SAVE_SRAM_ADDR + 0x0012, bytearray([0xBF, 0x10, 0xA0, 0x7F]))             # -                           lda !blocksanity_flags,x
    rom.write_bytes(SAVE_SRAM_ADDR + 0x0016, bytearray([0x9F, 0x40, 0x09, 0x70]))             #                             sta !blocksanity_sram,x
    rom.write_bytes(SAVE_SRAM_ADDR + 0x001A, bytearray([0xBD, 0x2F, 0x1F]))                   #                             lda !yoshi_coins_flags,x
    rom.write_bytes(SAVE_SRAM_ADDR + 0x001D, bytearray([0x9F, 0x00, 0x09, 0x70]))             #                             sta !yoshi_coins_sram,x
    rom.write_bytes(SAVE_SRAM_ADDR + 0x0021, bytearray([0xBD, 0xEE, 0x1F]))                   #                             lda !moons_flags,x
    rom.write_bytes(SAVE_SRAM_ADDR + 0x0024, bytearray([0x9F, 0x10, 0x09, 0x70]))             #                             sta !moons_sram,x
    rom.write_bytes(SAVE_SRAM_ADDR + 0x0028, bytearray([0xBF, 0x00, 0xA0, 0x7F]))             #                             lda !bonus_block_flags,x
    rom.write_bytes(SAVE_SRAM_ADDR + 0x002C, bytearray([0x9F, 0x30, 0x09, 0x70]))             #                             sta !bonus_block_sram,x
    rom.write_bytes(SAVE_SRAM_ADDR + 0x0030, bytearray([0xBD, 0x3C, 0x1F]))                   #                             lda !checkpoints_flags,x
    rom.write_bytes(SAVE_SRAM_ADDR + 0x0033, bytearray([0x9F, 0x20, 0x09, 0x70]))             #                             sta !checkpoints_sram,x
    rom.write_bytes(SAVE_SRAM_ADDR + 0x0037, bytearray([0xCA]))                               #                             dex 
    rom.write_bytes(SAVE_SRAM_ADDR + 0x0038, bytearray([0x10, 0xD8]))                         #                             bpl -
    rom.write_bytes(SAVE_SRAM_ADDR + 0x003A, bytearray([0xC2, 0x10]))                         #                             rep #$10
    rom.write_bytes(SAVE_SRAM_ADDR + 0x003C, bytearray([0xA2, 0x45, 0x02]))                   #                             ldx.w #!blocksanity_locs-1
    rom.write_bytes(SAVE_SRAM_ADDR + 0x003F, bytearray([0xBF, 0x00, 0xA4, 0x7F]))             # -                           lda !blocksanity_data_flags,x
    rom.write_bytes(SAVE_SRAM_ADDR + 0x0043, bytearray([0x9F, 0x00, 0x0A, 0x70]))             #                             sta !blocksanity_data_sram,x
    rom.write_bytes(SAVE_SRAM_ADDR + 0x0047, bytearray([0xCA]))                               #                             dex 
    rom.write_bytes(SAVE_SRAM_ADDR + 0x0048, bytearray([0x10, 0xF5]))                         #                             bpl -
    rom.write_bytes(SAVE_SRAM_ADDR + 0x004A, bytearray([0xE2, 0x10]))                         #                             sep #$10
    #rom.write_bytes(SAVE_SRAM_ADDR + 0x004C, bytearray([0xAD, 0xFF, 0x1F]))                   #                             lda !special_world_clear_flag
    #rom.write_bytes(SAVE_SRAM_ADDR + 0x004F, bytearray([0x8F, 0x52, 0x09, 0x70]))             #                             sta !special_world_clear_sram
    #rom.write_bytes(SAVE_SRAM_ADDR + 0x0053, bytearray([0xAF, 0x0E, 0xA0, 0x7F]))             #                             lda !received_items_count+$00
    #rom.write_bytes(SAVE_SRAM_ADDR + 0x0057, bytearray([0x8F, 0x50, 0x09, 0x70]))             #                             sta !received_items_count_sram+$00
    #rom.write_bytes(SAVE_SRAM_ADDR + 0x005B, bytearray([0xAF, 0x0F, 0xA0, 0x7F]))             #                             lda !received_items_count+$01
    #rom.write_bytes(SAVE_SRAM_ADDR + 0x005F, bytearray([0x8F, 0x51, 0x09, 0x70]))             #                             sta !received_items_count_sram+$01
    rom.write_bytes(SAVE_SRAM_ADDR + 0x004C, bytearray([0xEA] * 0x17))                        # Ugly, will apply be better when we port everything to a Base Patch
    rom.write_bytes(SAVE_SRAM_ADDR + 0x0063, bytearray([0xAF, 0x0F, 0xA0, 0x7F]))             #                             lda !goal_item_count
    rom.write_bytes(SAVE_SRAM_ADDR + 0x0067, bytearray([0x8F, 0x51, 0x09, 0x70]))             #                             sta !goal_item_count_sram
    rom.write_bytes(SAVE_SRAM_ADDR + 0x006B, bytearray([0x6B]))                               #                             rtl 

    INIT_RAM_ADDR = 0x7F0A0
    rom.write_bytes(INIT_RAM_ADDR + 0x0000, bytearray([0xA9, 0xAA]))                # init_ram:               lda #$AA
    rom.write_bytes(INIT_RAM_ADDR + 0x0002, bytearray([0x8D, 0x00, 0x04]))          #                         sta $0400
    rom.write_bytes(INIT_RAM_ADDR + 0x0005, bytearray([0xA9, 0x00]))                # clear_level_data:       lda #$00
    rom.write_bytes(INIT_RAM_ADDR + 0x0007, bytearray([0xA2, 0x5F]))                #                         ldx #$5F
    rom.write_bytes(INIT_RAM_ADDR + 0x0009, bytearray([0x9F, 0x00, 0xA2, 0x7F]))    # .loop                   sta !level_clears,x
    rom.write_bytes(INIT_RAM_ADDR + 0x000D, bytearray([0xCA]))                      #                         dex 
    rom.write_bytes(INIT_RAM_ADDR + 0x000E, bytearray([0x10, 0xF9]))                #                         bpl .loop
    rom.write_bytes(INIT_RAM_ADDR + 0x0010, bytearray([0xC2, 0x10]))                #                         rep #$10
    rom.write_bytes(INIT_RAM_ADDR + 0x0012, bytearray([0xA2, 0x0B, 0x00]))          #                         ldx.w #$000B
    rom.write_bytes(INIT_RAM_ADDR + 0x0015, bytearray([0x9F, 0x10, 0xA0, 0x7F]))    # -                       sta !blocksanity_flags,x
    rom.write_bytes(INIT_RAM_ADDR + 0x0019, bytearray([0x9D, 0x2F, 0x1F]))          #                         sta !yoshi_coins_flags,x
    rom.write_bytes(INIT_RAM_ADDR + 0x001C, bytearray([0x9D, 0xEE, 0x1F]))          #                         sta !moons_flags,x
    rom.write_bytes(INIT_RAM_ADDR + 0x001F, bytearray([0x9F, 0x00, 0xA0, 0x7F]))    #                         sta !bonus_block_flags,x
    rom.write_bytes(INIT_RAM_ADDR + 0x0023, bytearray([0x9D, 0x3C, 0x1F]))          #                         sta !checkpoints_flags,x
    rom.write_bytes(INIT_RAM_ADDR + 0x0026, bytearray([0xCA]))                      #                         dex 
    rom.write_bytes(INIT_RAM_ADDR + 0x0027, bytearray([0x10, 0xEC]))                #                         bpl -
    rom.write_bytes(INIT_RAM_ADDR + 0x0029, bytearray([0xA2, 0x45, 0x02]))          #                         ldx.w #!blocksanity_locs-1
    rom.write_bytes(INIT_RAM_ADDR + 0x002C, bytearray([0x9F, 0x00, 0xA4, 0x7F]))    # -                       sta !blocksanity_data_flags,x
    rom.write_bytes(INIT_RAM_ADDR + 0x0030, bytearray([0xCA]))                      #                         dex 
    rom.write_bytes(INIT_RAM_ADDR + 0x0031, bytearray([0x10, 0xF9]))                #                         bpl -
    rom.write_bytes(INIT_RAM_ADDR + 0x0033, bytearray([0xA2, 0x22, 0x04]))          #                         ldx #$0422
    rom.write_bytes(INIT_RAM_ADDR + 0x0036, bytearray([0x9F, 0x00, 0xB0, 0x7F]))    # -                       sta !score_sprite_count,x
    rom.write_bytes(INIT_RAM_ADDR + 0x003A, bytearray([0xCA]))                      #                         dex 
    rom.write_bytes(INIT_RAM_ADDR + 0x003B, bytearray([0x10, 0xF9]))                #                         bpl -
    #rom.write_bytes(INIT_RAM_ADDR + 0x003D, bytearray([0x8D, 0xFF, 0x1F]))          #                         sta !special_world_clear_flag
    rom.write_bytes(INIT_RAM_ADDR + 0x003D, bytearray([0xEA, 0xEA, 0xEA]))          #                         sta !special_world_clear_flag
    rom.write_bytes(INIT_RAM_ADDR + 0x0040, bytearray([0x8F, 0x0E, 0xA0, 0x7F]))    #                         sta !received_items_count+$00
    rom.write_bytes(INIT_RAM_ADDR + 0x0044, bytearray([0x8F, 0x0F, 0xA0, 0x7F]))    #                         sta !received_items_count+$01
    rom.write_bytes(INIT_RAM_ADDR + 0x0048, bytearray([0x8F, 0x1E, 0xA0, 0x7F]))    #                         sta !goal_item_count
    rom.write_bytes(INIT_RAM_ADDR + 0x004C, bytearray([0xA9, 0xFF]))                #                         lda #$FF
    rom.write_bytes(INIT_RAM_ADDR + 0x004E, bytearray([0x8D, 0x3C, 0x0F]))          #                         sta !thwimp_index
    rom.write_bytes(INIT_RAM_ADDR + 0x0051, bytearray([0xE2, 0x10]))                #                         sep #$10
    rom.write_bytes(INIT_RAM_ADDR + 0x0053, bytearray([0x22, 0x20, 0xF1, 0x0F]))    #                         jsl clear_tilemap
    rom.write_bytes(INIT_RAM_ADDR + 0x0057, bytearray([0x5C, 0xC0, 0x93, 0x00]))    #                         jml $0093C0

def handle_map_indicators(rom):
    rom.write_bytes(0x265EE, bytearray([0x4C, 0x00, 0xA3]))       # org $04E5EE : jmp check_events

    GET_MAP_LEVEL_NUM_ADDR = 0x22340
    rom.write_bytes(GET_MAP_LEVEL_NUM_ADDR + 0x0000, bytearray([0xC2, 0x30]))                 # get_translevel_num:         rep #$30
    rom.write_bytes(GET_MAP_LEVEL_NUM_ADDR + 0x0002, bytearray([0xAE, 0xD6, 0x0D]))           #                             ldx $0DD6
    rom.write_bytes(GET_MAP_LEVEL_NUM_ADDR + 0x0005, bytearray([0xBD, 0x1F, 0x1F]))           #                             lda $1F1F,x
    rom.write_bytes(GET_MAP_LEVEL_NUM_ADDR + 0x0008, bytearray([0x85, 0x00]))                 #                             sta $00
    rom.write_bytes(GET_MAP_LEVEL_NUM_ADDR + 0x000A, bytearray([0xBD, 0x21, 0x1F]))           #                             lda $1F21,x
    rom.write_bytes(GET_MAP_LEVEL_NUM_ADDR + 0x000D, bytearray([0x85, 0x02]))                 #                             sta $02
    rom.write_bytes(GET_MAP_LEVEL_NUM_ADDR + 0x000F, bytearray([0x8A]))                       #                             txa 
    rom.write_bytes(GET_MAP_LEVEL_NUM_ADDR + 0x0010, bytearray([0x4A]))                       #                             lsr 
    rom.write_bytes(GET_MAP_LEVEL_NUM_ADDR + 0x0011, bytearray([0x4A]))                       #                             lsr
    rom.write_bytes(GET_MAP_LEVEL_NUM_ADDR + 0x0012, bytearray([0xAA]))                       #                             tax 
    rom.write_bytes(GET_MAP_LEVEL_NUM_ADDR + 0x0013, bytearray([0x20, 0x85, 0x98]))           #                             jsr $9885
    rom.write_bytes(GET_MAP_LEVEL_NUM_ADDR + 0x0016, bytearray([0xA6, 0x04]))                 #                             ldx $04
    rom.write_bytes(GET_MAP_LEVEL_NUM_ADDR + 0x0018, bytearray([0xBF, 0x00, 0xD0, 0x7E]))     #                             lda $7ED000,x
    rom.write_bytes(GET_MAP_LEVEL_NUM_ADDR + 0x001C, bytearray([0xE2, 0x30]))                 #                             sep #$30
    rom.write_bytes(GET_MAP_LEVEL_NUM_ADDR + 0x001E, bytearray([0x85, 0x60]))                 #                             sta $60
    rom.write_bytes(GET_MAP_LEVEL_NUM_ADDR + 0x0020, bytearray([0xAA]))                       #                             tax 
    rom.write_bytes(GET_MAP_LEVEL_NUM_ADDR + 0x0021, bytearray([0xBF, 0x00, 0xFF, 0x06]))     #                             lda $06FF00,x
    rom.write_bytes(GET_MAP_LEVEL_NUM_ADDR + 0x0025, bytearray([0xC9, 0xFF]))                 #                             cmp #$FF
    rom.write_bytes(GET_MAP_LEVEL_NUM_ADDR + 0x0027, bytearray([0xF0, 0x02]))                 #                             beq +
    rom.write_bytes(GET_MAP_LEVEL_NUM_ADDR + 0x0029, bytearray([0x85, 0x60]))                 #                             sta $60
    rom.write_bytes(GET_MAP_LEVEL_NUM_ADDR + 0x002B, bytearray([0x60]))                       # +                           rts 

    GET_MAP_LEVEL_BIT_ADDR = 0x22380
    rom.write_bytes(GET_MAP_LEVEL_BIT_ADDR + 0x0000, bytearray([0xA5, 0x60]))                 # get_translevel_bit:         lda $60
    rom.write_bytes(GET_MAP_LEVEL_BIT_ADDR + 0x0002, bytearray([0x4A]))                       #                             lsr 
    rom.write_bytes(GET_MAP_LEVEL_BIT_ADDR + 0x0003, bytearray([0x4A]))                       #                             lsr 
    rom.write_bytes(GET_MAP_LEVEL_BIT_ADDR + 0x0004, bytearray([0x4A]))                       #                             lsr 
    rom.write_bytes(GET_MAP_LEVEL_BIT_ADDR + 0x0005, bytearray([0xA8]))                       #                             tay 
    rom.write_bytes(GET_MAP_LEVEL_BIT_ADDR + 0x0006, bytearray([0xA5, 0x60]))                 #                             lda $60
    rom.write_bytes(GET_MAP_LEVEL_BIT_ADDR + 0x0008, bytearray([0x29, 0x07]))                 #                             and #$07
    rom.write_bytes(GET_MAP_LEVEL_BIT_ADDR + 0x000A, bytearray([0xAA]))                       #                             tax 
    rom.write_bytes(GET_MAP_LEVEL_BIT_ADDR + 0x000B, bytearray([0x60]))                       #                             rts 

    UPDATE_MAP_PTRS_ADDR = 0x223C0
    rom.write_bytes(UPDATE_MAP_PTRS_ADDR + 0x0000, bytearray([0xE6, 0x00]))                   # update_flag_pointers:       inc $00
    rom.write_bytes(UPDATE_MAP_PTRS_ADDR + 0x0002, bytearray([0xE6, 0x00]))                   #                             inc $00
    rom.write_bytes(UPDATE_MAP_PTRS_ADDR + 0x0004, bytearray([0xE6, 0x03]))                   #                             inc $03
    rom.write_bytes(UPDATE_MAP_PTRS_ADDR + 0x0006, bytearray([0xE6, 0x03]))                   #                             inc $03
    rom.write_bytes(UPDATE_MAP_PTRS_ADDR + 0x0008, bytearray([0xE6, 0x06]))                   #                             inc $06
    rom.write_bytes(UPDATE_MAP_PTRS_ADDR + 0x000A, bytearray([0xE6, 0x06]))                   #                             inc $06
    rom.write_bytes(UPDATE_MAP_PTRS_ADDR + 0x000C, bytearray([0xE6, 0x62]))                   #                             inc $62
    rom.write_bytes(UPDATE_MAP_PTRS_ADDR + 0x000E, bytearray([0xE6, 0x62]))                   #                             inc $62
    rom.write_bytes(UPDATE_MAP_PTRS_ADDR + 0x0010, bytearray([0xE6, 0x63]))                   #                             inc $63
    rom.write_bytes(UPDATE_MAP_PTRS_ADDR + 0x0012, bytearray([0x60]))                         #                             rts 

    CLEAR_TILEMAP_ADDR = 0x7F120
    rom.write_bytes(CLEAR_TILEMAP_ADDR + 0x0000, bytearray([0xC2, 0x20]))                     # clear_tilemap:              rep #$20
    rom.write_bytes(CLEAR_TILEMAP_ADDR + 0x0002, bytearray([0xA9, 0x1F, 0x39]))               #                             lda.w #$3900+!icon_disabled
    rom.write_bytes(CLEAR_TILEMAP_ADDR + 0x0005, bytearray([0xA2, 0x1E]))                     #                             ldx #$1E
    rom.write_bytes(CLEAR_TILEMAP_ADDR + 0x0007, bytearray([0x9F, 0x20, 0xA1, 0x7F]))         # .loop                       sta !ow_tilemap_switches,x
    rom.write_bytes(CLEAR_TILEMAP_ADDR + 0x000B, bytearray([0x9F, 0x00, 0xA1, 0x7F]))         #                             sta !ow_tilemap_abilities,x
    rom.write_bytes(CLEAR_TILEMAP_ADDR + 0x000F, bytearray([0x9F, 0x40, 0xA1, 0x7F]))         #                             sta !ow_tilemap_flags_top,x
    rom.write_bytes(CLEAR_TILEMAP_ADDR + 0x0013, bytearray([0x9F, 0x60, 0xA1, 0x7F]))         #                             sta !ow_tilemap_flags_mid,x
    rom.write_bytes(CLEAR_TILEMAP_ADDR + 0x0017, bytearray([0x9F, 0x80, 0xA1, 0x7F]))         #                             sta !ow_tilemap_flags_bot,x
    rom.write_bytes(CLEAR_TILEMAP_ADDR + 0x001B, bytearray([0xCA]))                           #                             dex 
    rom.write_bytes(CLEAR_TILEMAP_ADDR + 0x001C, bytearray([0xCA]))                           #                             dex
    rom.write_bytes(CLEAR_TILEMAP_ADDR + 0x001D, bytearray([0x10, 0xE8]))                     #                             bpl .loop 
    rom.write_bytes(CLEAR_TILEMAP_ADDR + 0x001F, bytearray([0xE2, 0x20]))                     #                             sep #$20
    rom.write_bytes(CLEAR_TILEMAP_ADDR + 0x0021, bytearray([0xA9, 0x07]))                     #                             lda #$07
    rom.write_bytes(CLEAR_TILEMAP_ADDR + 0x0023, bytearray([0x85, 0x63]))                     #                             sta $63
    rom.write_bytes(CLEAR_TILEMAP_ADDR + 0x0025, bytearray([0x0A]))                           #                             asl 
    rom.write_bytes(CLEAR_TILEMAP_ADDR + 0x0026, bytearray([0x85, 0x62]))                     #                             sta $62
    rom.write_bytes(CLEAR_TILEMAP_ADDR + 0x0028, bytearray([0x6B]))                           #                             rtl 

    CLEAR_TILEMAP_FLAGS_ADDR = 0x7F180
    rom.write_bytes(CLEAR_TILEMAP_FLAGS_ADDR + 0x0000, bytearray([0xC2, 0x20]))               # clear_tilemap_flags:        rep #$20
    rom.write_bytes(CLEAR_TILEMAP_FLAGS_ADDR + 0x0002, bytearray([0xA9, 0x1F, 0x39]))         #                             lda.w #$3900+!icon_disabled
    rom.write_bytes(CLEAR_TILEMAP_FLAGS_ADDR + 0x0005, bytearray([0xA2, 0x0C]))               #                             ldx.b #($07*2)-2
    rom.write_bytes(CLEAR_TILEMAP_FLAGS_ADDR + 0x0007, bytearray([0x9F, 0x40, 0xA1, 0x7F]))   # .loop                       sta !ow_tilemap_flags_top,x
    rom.write_bytes(CLEAR_TILEMAP_FLAGS_ADDR + 0x000B, bytearray([0x9F, 0x60, 0xA1, 0x7F]))   #                             sta !ow_tilemap_flags_mid,x
    rom.write_bytes(CLEAR_TILEMAP_FLAGS_ADDR + 0x000F, bytearray([0x9F, 0x80, 0xA1, 0x7F]))   #                             sta !ow_tilemap_flags_bot,x
    rom.write_bytes(CLEAR_TILEMAP_FLAGS_ADDR + 0x0013, bytearray([0xCA]))                     #                             dex 
    rom.write_bytes(CLEAR_TILEMAP_FLAGS_ADDR + 0x0014, bytearray([0xCA]))                     #                             dex 
    rom.write_bytes(CLEAR_TILEMAP_FLAGS_ADDR + 0x0015, bytearray([0x10, 0xF0]))               #                             bpl .loop 
    rom.write_bytes(CLEAR_TILEMAP_FLAGS_ADDR + 0x0017, bytearray([0xE2, 0x20]))               #                             sep #$20
    rom.write_bytes(CLEAR_TILEMAP_FLAGS_ADDR + 0x0019, bytearray([0xA9, 0x06]))               #                             lda #$06
    rom.write_bytes(CLEAR_TILEMAP_FLAGS_ADDR + 0x001B, bytearray([0x85, 0x63]))               #                             sta $63
    rom.write_bytes(CLEAR_TILEMAP_FLAGS_ADDR + 0x001D, bytearray([0x0A]))                     #                             asl 
    rom.write_bytes(CLEAR_TILEMAP_FLAGS_ADDR + 0x001E, bytearray([0x85, 0x62]))               #                             sta $62
    rom.write_bytes(CLEAR_TILEMAP_FLAGS_ADDR + 0x0020, bytearray([0xA9, 0xFF]))               #                             lda #$FF
    rom.write_bytes(CLEAR_TILEMAP_FLAGS_ADDR + 0x0022, bytearray([0x8D, 0x3C, 0x0F]))         #                             sta !thwimp_index
    rom.write_bytes(CLEAR_TILEMAP_FLAGS_ADDR + 0x0025, bytearray([0x6B]))                     #                             rtl 

    CHECK_EVENTS_ADDR = 0x22300
    rom.write_bytes(CHECK_EVENTS_ADDR + 0x0000, bytearray([0xDA]))                            # check_events:               phx 
    rom.write_bytes(CHECK_EVENTS_ADDR + 0x0001, bytearray([0x20, 0x40, 0xA3]))                #                             jsr get_translevel_num
    rom.write_bytes(CHECK_EVENTS_ADDR + 0x0004, bytearray([0xAD, 0xD5, 0x0D]))                #                             lda $0DD5
    rom.write_bytes(CHECK_EVENTS_ADDR + 0x0007, bytearray([0xF0, 0x17]))                      #                             beq .dont_sync
    rom.write_bytes(CHECK_EVENTS_ADDR + 0x0009, bytearray([0x30, 0x15]))                      #                             bmi .dont_sync
    rom.write_bytes(CHECK_EVENTS_ADDR + 0x000B, bytearray([0xC9, 0x05]))                      #                             cmp #$05
    rom.write_bytes(CHECK_EVENTS_ADDR + 0x000D, bytearray([0xB0, 0x11]))                      #                             bcs .dont_sync
    rom.write_bytes(CHECK_EVENTS_ADDR + 0x000F, bytearray([0x29, 0x07]))                      #                             and #$07
    rom.write_bytes(CHECK_EVENTS_ADDR + 0x0011, bytearray([0xAA]))                            #                             tax 
    rom.write_bytes(CHECK_EVENTS_ADDR + 0x0012, bytearray([0xBF, 0x7D, 0x9E, 0x00]))          #                             lda.l $009E7D,x
    rom.write_bytes(CHECK_EVENTS_ADDR + 0x0016, bytearray([0xA6, 0x60]))                      #                             ldx $60
    rom.write_bytes(CHECK_EVENTS_ADDR + 0x0018, bytearray([0x1F, 0x00, 0xA2, 0x7F]))          #                             ora !level_clears,x
    rom.write_bytes(CHECK_EVENTS_ADDR + 0x001C, bytearray([0x9F, 0x00, 0xA2, 0x7F]))          #                             sta !level_clears,x
    rom.write_bytes(CHECK_EVENTS_ADDR + 0x0020, bytearray([0xFA]))                            # .dont_sync                  plx 
    rom.write_bytes(CHECK_EVENTS_ADDR + 0x0021, bytearray([0xAD, 0xD5, 0x0D]))                #                             lda $0DD5
    rom.write_bytes(CHECK_EVENTS_ADDR + 0x0024, bytearray([0xC9, 0x02]))                      #                             cmp #$02
    rom.write_bytes(CHECK_EVENTS_ADDR + 0x0026, bytearray([0xD0, 0x03]))                      #                             bne .no_secret
    rom.write_bytes(CHECK_EVENTS_ADDR + 0x0028, bytearray([0xEE, 0xEA, 0x1D]))                #                             inc $1DEA
    rom.write_bytes(CHECK_EVENTS_ADDR + 0x002B, bytearray([0x4C, 0xF8, 0xE5]))                # .no_secret                  jmp $E5F8

    DRAW_MAP_TILEMAP_ADDR = 0x221B6
    rom.write_bytes(0x00222, bytearray([0x5C, 0xB6, 0xA1, 0x04])) # org $008222 : jml draw_ow_tilemap
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0000, bytearray([0xAD, 0xD9, 0x13]))            # draw_ow_tilemap:            lda $13D9
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0003, bytearray([0xC9, 0x0A]))                  #                             cmp #$0A
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0005, bytearray([0xD0, 0x04]))                  #                             bne write_tilemap
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0007, bytearray([0x5C, 0x29, 0x82, 0x00]))      #                             jml $008229
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x000B, bytearray([0xC2, 0x20]))                  # write_tilemap:              rep #$20
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x000D, bytearray([0xA0, 0x80]))                  #                             ldy #$80
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x000F, bytearray([0x8C, 0x15, 0x21]))            #                             sty $2115
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0012, bytearray([0xA9, 0x27, 0x50]))            # write_abilities:            lda #!vram_abilities_top
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0015, bytearray([0x8D, 0x16, 0x21]))            #                             sta $2116
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0018, bytearray([0xA2, 0x00]))                  #                             ldx.b #$00
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x001A, bytearray([0xBF, 0xA2, 0xA2, 0x04]))      # ..loop                      lda.l abilities_top,x 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x001E, bytearray([0x8D, 0x18, 0x21]))            #                             sta $2118
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0021, bytearray([0xE8]))                        #                             inx 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0022, bytearray([0xE8]))                        #                             inx 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0023, bytearray([0xE0, 0x14]))                  #                             cpx.b #$0A*2
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0025, bytearray([0x90, 0xF3]))                  #                             bcc ..loop
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0027, bytearray([0xA9, 0x47, 0x50]))            # .mid                        lda #!vram_abilities_mid
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x002A, bytearray([0x8D, 0x16, 0x21]))            #                             sta $2116
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x002D, bytearray([0xA2, 0x00]))                  #                             ldx.b #$00
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x002F, bytearray([0xBF, 0xB6, 0xA2, 0x04]))      # ..loop                      lda.l abilities_bottom,x 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0033, bytearray([0x8D, 0x18, 0x21]))            #                             sta $2118
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0036, bytearray([0xE8]))                        #                             inx 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0037, bytearray([0xE8]))                        #                             inx 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0038, bytearray([0xE0, 0x14]))                  #                             cpx.b #$0A*2
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x003A, bytearray([0x90, 0xF3]))                  #                             bcc ..loop
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x003C, bytearray([0xA9, 0x67, 0x50]))            # .bot                        lda #!vram_abilities_bot
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x003F, bytearray([0x8D, 0x16, 0x21]))            #                             sta $2116
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0042, bytearray([0xA2, 0x00]))                  #                             ldx.b #$00
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0044, bytearray([0xBF, 0x00, 0xA1, 0x7F]))      # ..loop                      lda !ow_tilemap_abilities,x 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0048, bytearray([0x8D, 0x18, 0x21]))            #                             sta $2118
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x004B, bytearray([0xE8]))                        #                             inx 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x004C, bytearray([0xE8]))                        #                             inx 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x004D, bytearray([0xE0, 0x14]))                  #                             cpx.b #$0A*2
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x004F, bytearray([0x90, 0xF3]))                  #                             bcc ..loop
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0051, bytearray([0xA9, 0x32, 0x50]))            # write_switches:             lda #!vram_switches_top
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0054, bytearray([0x8D, 0x16, 0x21]))            #                             sta $2116
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0057, bytearray([0xA2, 0x00]))                  #                             ldx.b #$00
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0059, bytearray([0xBF, 0xCA, 0xA2, 0x04]))      # ..loop                      lda.l switches_top,x 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x005D, bytearray([0x8D, 0x18, 0x21]))            #                             sta $2118
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0060, bytearray([0xE8]))                        #                             inx 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0061, bytearray([0xE8]))                        #                             inx 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0062, bytearray([0xE0, 0x0A]))                  #                             cpx.b #$05*2
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0064, bytearray([0x90, 0xF3]))                  #                             bcc ..loop
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0066, bytearray([0xA9, 0x52, 0x50]))            # .mid                        lda #!vram_switches_mid
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0069, bytearray([0x8D, 0x16, 0x21]))            #                             sta $2116
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x006C, bytearray([0xA2, 0x00]))                  #                             ldx.b #$00
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x006E, bytearray([0xBF, 0xD4, 0xA2, 0x04]))      # ..loop                      lda.l switches_bottom,x 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0072, bytearray([0x8D, 0x18, 0x21]))            #                             sta $2118
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0075, bytearray([0xE8]))                        #                             inx 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0076, bytearray([0xE8]))                        #                             inx 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0077, bytearray([0xE0, 0x0A]))                  #                             cpx.b #$05*2
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0079, bytearray([0x90, 0xF3]))                  #                             bcc ..loop
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x007B, bytearray([0xA9, 0x72, 0x50]))            # .bot                        lda #!vram_switches_bot
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x007E, bytearray([0x8D, 0x16, 0x21]))            #                             sta $2116
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0081, bytearray([0xA2, 0x00]))                  #                             ldx.b #$00
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0083, bytearray([0xBF, 0x20, 0xA1, 0x7F]))      # ..loop                      lda !ow_tilemap_switches,x 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0087, bytearray([0x8D, 0x18, 0x21]))            #                             sta $2118
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x008A, bytearray([0xE8]))                        #                             inx 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x008B, bytearray([0xE8]))                        #                             inx 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x008C, bytearray([0xE0, 0x0A]))                  #                             cpx.b #$05*2
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x008E, bytearray([0x90, 0xF3]))                  #                             bcc ..loop
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0090, bytearray([0xD4, 0x00]))                  # write_level_data:           pei ($00)
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0092, bytearray([0xA5, 0x63]))                  #                             lda $63
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0094, bytearray([0x29, 0xFF, 0x00]))            #                             and #$00FF
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0097, bytearray([0x85, 0x00]))                  #                             sta $00
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0099, bytearray([0xF0, 0x48]))                  #                             beq .skip_flags
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x009B, bytearray([0xA9, 0x3E, 0x50]))            # .top                        lda.w #!vram_level_data_top+$01
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x009E, bytearray([0x38]))                        #                             sec 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x009F, bytearray([0xE5, 0x00]))                  #                             sbc $00
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00A1, bytearray([0x8D, 0x16, 0x21]))            #                             sta $2116
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00A4, bytearray([0xA6, 0x62]))                  #                             ldx.b $62
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00A6, bytearray([0xCA]))                        #                             dex 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00A7, bytearray([0xCA]))                        #                             dex 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00A8, bytearray([0xBF, 0x40, 0xA1, 0x7F]))      # ..loop                      lda.l !ow_tilemap_flags_top,x
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00AC, bytearray([0x8D, 0x18, 0x21]))            #                             sta $2118
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00AF, bytearray([0xCA]))                        #                             dex 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00B0, bytearray([0xCA]))                        #                             dex 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00B1, bytearray([0x10, 0xF5]))                  #                             bpl ..loop
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00B3, bytearray([0xA9, 0x5E, 0x50]))            # .mid                        lda.w #!vram_level_data_mid+$01
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00B6, bytearray([0x38]))                        #                             sec 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00B7, bytearray([0xE5, 0x00]))                  #                             sbc $00
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00B9, bytearray([0x8D, 0x16, 0x21]))            #                             sta $2116
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00BC, bytearray([0xA6, 0x62]))                  #                             ldx.b $62
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00BE, bytearray([0xCA]))                        #                             dex 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00BF, bytearray([0xCA]))                        #                             dex 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00C0, bytearray([0xBF, 0x60, 0xA1, 0x7F]))      # ..loop                      lda.l !ow_tilemap_flags_mid,x
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00C4, bytearray([0x8D, 0x18, 0x21]))            #                             sta $2118
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00C7, bytearray([0xCA]))                        #                             dex 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00C8, bytearray([0xCA]))                        #                             dex 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00C9, bytearray([0x10, 0xF5]))                  #                             bpl ..loop
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00CB, bytearray([0xA9, 0x7E, 0x50]))            # .bot                        lda.w #!vram_level_data_bot+$01
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00CE, bytearray([0x38]))                        #                             sec 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00CF, bytearray([0xE5, 0x00]))                  #                             sbc $00
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00D1, bytearray([0x8D, 0x16, 0x21]))            #                             sta $2116
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00D4, bytearray([0xA6, 0x62]))                  #                             ldx.b $62
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00D6, bytearray([0xCA]))                        #                             dex 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00D7, bytearray([0xCA]))                        #                             dex 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00D8, bytearray([0xBF, 0x80, 0xA1, 0x7F]))      # ..loop                      lda.l !ow_tilemap_flags_bot,x
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00DC, bytearray([0x8D, 0x18, 0x21]))            #                             sta $2118
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00DF, bytearray([0xCA]))                        #                             dex 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00E0, bytearray([0xCA]))                        #                             dex 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00E1, bytearray([0x10, 0xF5]))                  #                             bpl ..loop
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00E3, bytearray([0x68]))                        # .skip_flags                 pla 
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00E4, bytearray([0x85, 0x00]))                  #                             sta $00
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00E6, bytearray([0xE2, 0x20]))                  #                             sep #$20
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00E8, bytearray([0x5C, 0x37, 0x82, 0x00]))      #                             jml $008237
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00EC, bytearray([0x0F, 0x39, 0x12, 0x39]))      # abilities_top:              dw $390F,$3912
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00F0, bytearray([0x11, 0x39, 0x02, 0x39]))      #                             dw $3911,$3902
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00F4, bytearray([0x12, 0x39, 0x02, 0x39]))      #                             dw $3912,$3902
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00F8, bytearray([0x18, 0x39, 0x0F, 0x39]))      #                             dw $3918,$390F
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x00FC, bytearray([0x0F, 0x39, 0x12, 0x39]))      #                             dw $390F,$3912
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0100, bytearray([0x4E, 0x39, 0x4F, 0x39]))      # abilities_bottom:           dw $394E,$394F
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0104, bytearray([0x54, 0x39, 0x40, 0x39]))      #                             dw $3954,$3940
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0108, bytearray([0x56, 0x39, 0x4B, 0x39]))      #                             dw $3956,$394B
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x010C, bytearray([0x4E, 0x39, 0x52, 0x39]))      #                             dw $394E,$3952
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0110, bytearray([0x41, 0x39, 0x53, 0x39]))      #                             dw $3941,$3953
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0114, bytearray([0x18, 0x39, 0x06, 0x39]))      # switches_top:               dw $3918,$3906
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0118, bytearray([0x11, 0x39, 0x01, 0x39]))      #                             dw $3911,$3901
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x011C, bytearray([0x12, 0x39]))                  #                             dw $3912
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x011E, bytearray([0x12, 0x39, 0x12, 0x39]))      # switches_bottom:            dw $3912,$3912
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0122, bytearray([0x12, 0x39, 0x12, 0x39]))      #                             dw $3912,$3912
    rom.write_bytes(DRAW_MAP_TILEMAP_ADDR + 0x0126, bytearray([0x4F, 0x39]))                  #                             dw $394F

    BUILD_TILEMAP_ADDR = 0x26F3E
    rom.write_bytes(0x021C7, bytearray([0x22, 0x3E, 0xEF, 0x04])) # org $00A1C7 : jsl prepare_dynamic_tilemap
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0000, bytearray([0x22, 0x41, 0x82, 0x04]))         # prepare_dynamic_tilemap:    jsl $048241
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0004, bytearray([0xA0, 0x22]))                     # .handle_powerup:            ldy #$22
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0006, bytearray([0xAD, 0x2D, 0x1F]))               #                             lda $1F2D
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0009, bytearray([0x4A]))                           #                             lsr 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x000A, bytearray([0x90, 0x01]))                     #                             bcc $01
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x000C, bytearray([0xC8]))                           #                             iny 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x000D, bytearray([0x4A]))                           #                             lsr 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x000E, bytearray([0x90, 0x01]))                     #                             bcc $01
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0010, bytearray([0xC8]))                           #                             iny 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0011, bytearray([0x4A]))                           #                             lsr 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0012, bytearray([0x90, 0x01]))                     #                             bcc $01
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0014, bytearray([0xC8]))                           #                             iny 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0015, bytearray([0x98]))                           #                             tya 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0016, bytearray([0x8F, 0x00, 0xA1, 0x7F]))         #                             sta !ow_tilemap_abilities         ; Progressive powerup
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x001A, bytearray([0xA0, 0x5E]))                     # .handle_spinjump:           ldy #!icon_not_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x001C, bytearray([0xAD, 0x1C, 0x1F]))               #                             lda $1F1C
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x001F, bytearray([0x29, 0x08]))                     #                             and #$08
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0021, bytearray([0xF0, 0x02]))                     #                             beq $02
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0023, bytearray([0xA0, 0x3F]))                     #                             ldy #!icon_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0025, bytearray([0x98]))                           #                             tya 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0026, bytearray([0x8F, 0x02, 0xA1, 0x7F]))         #                             sta !ow_tilemap_abilities+$02         ; Spin jump
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x002A, bytearray([0xA0, 0x5E]))                     # .handle_run:                ldy.b #!icon_not_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x002C, bytearray([0xAD, 0x1C, 0x1F]))               #                             lda $1F1C
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x002F, bytearray([0x29, 0x80]))                     #                             and #$80
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0031, bytearray([0xF0, 0x02]))                     #                             beq $02
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0033, bytearray([0xA0, 0x3F]))                     #                             ldy.b #!icon_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0035, bytearray([0x98]))                           #                             tya 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0036, bytearray([0x8F, 0x04, 0xA1, 0x7F]))         #                             sta !ow_tilemap_abilities+$04         ; Run
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x003A, bytearray([0xA0, 0x5E]))                     # .handle_carry:              ldy.b #!icon_not_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x003C, bytearray([0xAD, 0x1C, 0x1F]))               #                             lda $1F1C
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x003F, bytearray([0x29, 0x40]))                     #                             and #$40
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0041, bytearray([0xF0, 0x02]))                     #                             beq $02
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0043, bytearray([0xA0, 0x3F]))                     #                             ldy.b #!icon_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0045, bytearray([0x98]))                           #                             tya 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0046, bytearray([0x8F, 0x06, 0xA1, 0x7F]))         #                             sta !ow_tilemap_abilities+$06         ; Carry
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x004A, bytearray([0xA0, 0x5E]))                     # .handle_swim:               ldy.b #!icon_not_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x004C, bytearray([0xAD, 0x1C, 0x1F]))               #                             lda $1F1C
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x004F, bytearray([0x29, 0x04]))                     #                             and #$04
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0051, bytearray([0xF0, 0x02]))                     #                             beq $02
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0053, bytearray([0xA0, 0x3F]))                     #                             ldy.b #!icon_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0055, bytearray([0x98]))                           #                             tya 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0056, bytearray([0x8F, 0x08, 0xA1, 0x7F]))         #                             sta !ow_tilemap_abilities+$08         ; Swim
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x005A, bytearray([0xA0, 0x5E]))                     # .handle_climb:              ldy.b #!icon_not_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x005C, bytearray([0xAD, 0x1C, 0x1F]))               #                             lda $1F1C
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x005F, bytearray([0x29, 0x20]))                     #                             and #$20
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0061, bytearray([0xF0, 0x02]))                     #                             beq $02
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0063, bytearray([0xA0, 0x3F]))                     #                             ldy.b #!icon_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0065, bytearray([0x98]))                           #                             tya 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0066, bytearray([0x8F, 0x0A, 0xA1, 0x7F]))         #                             sta !ow_tilemap_abilities+$0A         ; Climb
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x006A, bytearray([0xA0, 0x5E]))                     # .handle_yoshi:              ldy.b #!icon_not_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x006C, bytearray([0xAD, 0x1C, 0x1F]))               #                             lda $1F1C
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x006F, bytearray([0x29, 0x02]))                     #                             and #$02
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0071, bytearray([0xF0, 0x02]))                     #                             beq $02
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0073, bytearray([0xA0, 0x3F]))                     #                             ldy.b #!icon_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0075, bytearray([0x98]))                           #                             tya 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0076, bytearray([0x8F, 0x0C, 0xA1, 0x7F]))         #                             sta !ow_tilemap_abilities+$0C         ; Yoshi
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x007A, bytearray([0xA0, 0x5E]))                     # .handle_pswitch:            ldy.b #!icon_not_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x007C, bytearray([0xAD, 0x1C, 0x1F]))               #                             lda $1F1C
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x007F, bytearray([0x29, 0x10]))                     #                             and #$10
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0081, bytearray([0xF0, 0x02]))                     #                             beq $02
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0083, bytearray([0xA0, 0x3F]))                     #                             ldy.b #!icon_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0085, bytearray([0x98]))                           #                             tya 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0086, bytearray([0x8F, 0x0E, 0xA1, 0x7F]))         #                             sta !ow_tilemap_abilities+$0E         ; P-Switch
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x008A, bytearray([0xA0, 0x5E]))                     # .handle_pballoon:           ldy.b #!icon_not_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x008C, bytearray([0xAD, 0x2D, 0x1F]))               #                             lda $1F2D
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x008F, bytearray([0x29, 0x08]))                     #                             and #$08
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0091, bytearray([0xF0, 0x02]))                     #                             beq $02
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0093, bytearray([0xA0, 0x3F]))                     #                             ldy.b #!icon_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0095, bytearray([0x98]))                           #                             tya 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0096, bytearray([0x8F, 0x10, 0xA1, 0x7F]))         #                             sta !ow_tilemap_abilities+$10         ; P-Balloon
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x009A, bytearray([0xA0, 0x5E]))                     # .handle_star:               ldy.b #!icon_not_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x009C, bytearray([0xAD, 0x2D, 0x1F]))               #                             lda $1F2D
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x009F, bytearray([0x29, 0x10]))                     #                             and #$10
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00A1, bytearray([0xF0, 0x02]))                     #                             beq $02
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00A3, bytearray([0xA0, 0x3F]))                     #                             ldy.b #!icon_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00A5, bytearray([0x98]))                           #                             tya 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00A6, bytearray([0x8F, 0x12, 0xA1, 0x7F]))         #                             sta !ow_tilemap_abilities+$12         ; Star
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00AA, bytearray([0xA0, 0x5E]))                     # .handle_yellow_switch:      ldy.b #!icon_not_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00AC, bytearray([0xAD, 0x28, 0x1F]))               #                             lda $1F28
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00AF, bytearray([0xF0, 0x02]))                     #                             beq $02
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00B1, bytearray([0xA0, 0x3F]))                     #                             ldy.b #!icon_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00B3, bytearray([0x98]))                           #                             tya 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00B4, bytearray([0x8F, 0x20, 0xA1, 0x7F]))         #                             sta !ow_tilemap_switches+$00
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00B8, bytearray([0xA0, 0x5E]))                     # .handle_green_switch:       ldy.b #!icon_not_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00BA, bytearray([0xAD, 0x27, 0x1F]))               #                             lda $1F27
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00BD, bytearray([0xF0, 0x02]))                     #                             beq $02
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00BF, bytearray([0xA0, 0x3F]))                     #                             ldy.b #!icon_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00C1, bytearray([0x98]))                           #                             tya 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00C2, bytearray([0x8F, 0x22, 0xA1, 0x7F]))         #                             sta !ow_tilemap_switches+$02
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00C6, bytearray([0xA0, 0x5E]))                     # .handle_red_switch:         ldy.b #!icon_not_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00C8, bytearray([0xAD, 0x2A, 0x1F]))               #                             lda $1F2A
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00CB, bytearray([0xF0, 0x02]))                     #                             beq $02
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00CD, bytearray([0xA0, 0x3F]))                     #                             ldy.b #!icon_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00CF, bytearray([0x98]))                           #                             tya 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00D0, bytearray([0x8F, 0x24, 0xA1, 0x7F]))         #                             sta !ow_tilemap_switches+$04
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00D4, bytearray([0xA0, 0x5E]))                     # .handle_blue_switch:        ldy.b #!icon_not_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00D6, bytearray([0xAD, 0x29, 0x1F]))               #                             lda $1F29
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00D9, bytearray([0xF0, 0x02]))                     #                             beq $02
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00DB, bytearray([0xA0, 0x3F]))                     #                             ldy.b #!icon_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00DD, bytearray([0x98]))                           #                             tya 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00DE, bytearray([0x8F, 0x26, 0xA1, 0x7F]))         #                             sta !ow_tilemap_switches+$06
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00E2, bytearray([0xA0, 0x5E]))                     # .handle_special_world_clear:    ldy.b #!icon_not_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00E4, bytearray([0xAD, 0x1E, 0x1F]))               #                             lda !special_world_clear_flag
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00E7, bytearray([0xF0, 0x02]))                     #                             beq $02
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00E9, bytearray([0xA0, 0x3F]))                     #                             ldy.b #!icon_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00EB, bytearray([0x98]))                           #                             tya 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00EC, bytearray([0x8F, 0x28, 0xA1, 0x7F]))         #                             sta !ow_tilemap_switches+$08
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00F0, bytearray([0x22, 0x80, 0xF1, 0x0F]))         #                             jsl clear_tilemap_flags
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00F4, bytearray([0xAD, 0xD9, 0x13]))               #                             lda $13D9
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00F7, bytearray([0xC9, 0x01]))                     #                             cmp #$01
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00F9, bytearray([0xF0, 0x05]))                     #                             beq process_level
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00FB, bytearray([0xC9, 0x03]))                     #                             cmp #$03
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00FD, bytearray([0xF0, 0x01]))                     #                             beq process_level
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x00FF, bytearray([0x6B]))                           #                             rtl
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0100, bytearray([0x20, 0x40, 0xA3]))               # process_level:              jsr get_translevel_num
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0103, bytearray([0xA6, 0x60]))                     #                             ldx $60
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0105, bytearray([0xBF, 0x00, 0xF4, 0x0F]))         #                             lda.l level_data,x
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0109, bytearray([0x10, 0x01]))                     #                             bpl .handle_data
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x010B, bytearray([0x6B]))                           #                             rtl 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x010C, bytearray([0x64, 0x62]))                     # .handle_data                stz $62
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x010E, bytearray([0x64, 0x63]))                     #                             stz $63
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0110, bytearray([0xC2, 0x20]))                     #                             rep #$20
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0112, bytearray([0xA9, 0x40, 0xA1]))               #                             lda.w #!ow_tilemap_flags_top
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0115, bytearray([0x85, 0x00]))                     #                             sta $00
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0117, bytearray([0xA9, 0x60, 0xA1]))               #                             lda.w #!ow_tilemap_flags_mid
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x011A, bytearray([0x85, 0x03]))                     #                             sta $03
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x011C, bytearray([0xA9, 0x80, 0xA1]))               #                             lda.w #!ow_tilemap_flags_bot
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x011F, bytearray([0x85, 0x06]))                     #                             sta $06
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0121, bytearray([0xE2, 0x20]))                     #                             sep #$20
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0123, bytearray([0xA9, 0x7F]))                     #                             lda.b #!ow_tilemap_flags_top>>16
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0125, bytearray([0x85, 0x02]))                     #                             sta $02
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0127, bytearray([0x85, 0x05]))                     #                             sta $05
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0129, bytearray([0x85, 0x08]))                     #                             sta $08
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x012B, bytearray([0xAF, 0xAB, 0xBF, 0x03]))         # handle_blocksanity:         lda.l blocksanity_enabled_flag
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x012F, bytearray([0xF0, 0x30]))                     #                             beq handle_bonus_blocks
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0131, bytearray([0xA6, 0x60]))                     #                             ldx $60
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0133, bytearray([0xA0, 0x1F]))                     #                             ldy.b #!icon_disabled
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0135, bytearray([0xBF, 0x00, 0xF4, 0x0F]))         #                             lda.l level_data,x
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0139, bytearray([0x29, 0x40]))                     #                             and #$40
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x013B, bytearray([0xF0, 0x24]))                     #                             beq handle_bonus_blocks
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x013D, bytearray([0xA0, 0x5E]))                     #                             ldy.b #!icon_not_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x013F, bytearray([0x5A]))                           #                             phy 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0140, bytearray([0x20, 0x80, 0xA3]))               #                             jsr get_translevel_bit
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0143, bytearray([0xDA]))                           #                             phx 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0144, bytearray([0xBB]))                           #                             tyx 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0145, bytearray([0xBF, 0x10, 0xA0, 0x7F]))         #                             lda.l !blocksanity_flags,x
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0149, bytearray([0xFA]))                           #                             plx 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x014A, bytearray([0x7A]))                           #                             ply 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x014B, bytearray([0x3F, 0xA6, 0xA8, 0x0D]))         #                             and.l $0DA8A6,x
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x014F, bytearray([0xF0, 0x02]))                     #                             beq .write
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0151, bytearray([0xA0, 0x3F]))                     #                             ldy.b #!icon_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0153, bytearray([0x98]))                           # .write                      tya 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0154, bytearray([0x87, 0x06]))                     #                             sta [$06]
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0156, bytearray([0xA9, 0x01]))                     #                             lda #$01
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0158, bytearray([0x87, 0x00]))                     #                             sta [$00]
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x015A, bytearray([0xA9, 0x12]))                     #                             lda #$12
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x015C, bytearray([0x87, 0x03]))                     #                             sta [$03]
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x015E, bytearray([0x20, 0xC0, 0xA3]))               #                             jsr update_flag_pointers
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0161, bytearray([0xAF, 0xAA, 0xBF, 0x03]))         # handle_bonus_blocks:        lda.l bonus_block_enabled_flag
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0165, bytearray([0xF0, 0x30]))                     #                             beq handle_checkpoints
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0167, bytearray([0xA6, 0x60]))                     #                             ldx $60
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0169, bytearray([0xA0, 0x1F]))                     #                             ldy.b #!icon_disabled
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x016B, bytearray([0xBF, 0x00, 0xF4, 0x0F]))         #                             lda.l level_data,x
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x016F, bytearray([0x29, 0x20]))                     #                             and #$20
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0171, bytearray([0xF0, 0x24]))                     #                             beq handle_checkpoints
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0173, bytearray([0xA0, 0x5E]))                     #                             ldy.b #!icon_not_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0175, bytearray([0x5A]))                           #                             phy 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0176, bytearray([0x20, 0x80, 0xA3]))               #                             jsr get_translevel_bit
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0179, bytearray([0xDA]))                           #                             phx 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x017A, bytearray([0xBB]))                           #                             tyx 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x017B, bytearray([0xBF, 0x00, 0xA0, 0x7F]))         #                             lda !bonus_block_flags,x
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x017F, bytearray([0xFA]))                           #                             plx 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0180, bytearray([0x7A]))                           #                             ply 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0181, bytearray([0x3F, 0xA6, 0xA8, 0x0D]))         #                             and.l $0DA8A6,x
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0185, bytearray([0xF0, 0x02]))                     #                             beq .write
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0187, bytearray([0xA0, 0x3F]))                     #                             ldy.b #!icon_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0189, bytearray([0x98]))                           # .write                      tya 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x018A, bytearray([0x87, 0x06]))                     #                             sta [$06]
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x018C, bytearray([0xA9, 0x01]))                     #                             lda #$01
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x018E, bytearray([0x87, 0x00]))                     #                             sta [$00]
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0190, bytearray([0xA9, 0x4E]))                     #                             lda #$4E
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0192, bytearray([0x87, 0x03]))                     #                             sta [$03]
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0194, bytearray([0x20, 0xC0, 0xA3]))               #                             jsr update_flag_pointers
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0197, bytearray([0xAF, 0xA9, 0xBF, 0x03]))         # handle_checkpoints:         lda.l checkpoints_enabled_flag
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x019B, bytearray([0xF0, 0x2A]))                     #                             beq handle_moons
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x019D, bytearray([0xA6, 0x60]))                     #                             ldx $60
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x019F, bytearray([0xBF, 0x00, 0xF4, 0x0F]))         #                             lda.l level_data,x
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01A3, bytearray([0x29, 0x10]))                     #                             and #$10
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01A5, bytearray([0xF0, 0x20]))                     #                             beq handle_moons
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01A7, bytearray([0xA0, 0x5E]))                     #                             ldy.b #!icon_not_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01A9, bytearray([0x5A]))                           #                             phy 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01AA, bytearray([0x20, 0x80, 0xA3]))               #                             jsr get_translevel_bit
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01AD, bytearray([0xB9, 0x3C, 0x1F]))               #                             lda !checkpoints_flags,y
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01B0, bytearray([0x7A]))                           #                             ply 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01B1, bytearray([0x3F, 0xA6, 0xA8, 0x0D]))         #                             and.l $0DA8A6,x
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01B5, bytearray([0xF0, 0x02]))                     #                             beq .write
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01B7, bytearray([0xA0, 0x3F]))                     #                             ldy.b #!icon_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01B9, bytearray([0x98]))                           # .write                      tya 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01BA, bytearray([0x87, 0x06]))                     #                             sta [$06]
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01BC, bytearray([0xA9, 0x07]))                     #                             lda #$07
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01BE, bytearray([0x87, 0x00]))                     #                             sta [$00]
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01C0, bytearray([0xA9, 0x48]))                     #                             lda #$48
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01C2, bytearray([0x87, 0x03]))                     #                             sta [$03]
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01C4, bytearray([0x20, 0xC0, 0xA3]))               #                             jsr update_flag_pointers
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01C7, bytearray([0xAF, 0xA8, 0xBF, 0x03]))         # handle_moons:               lda.l moon_enabled_flag
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01CB, bytearray([0xF0, 0x2A]))                     #                             beq handle_dragon_coins
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01CD, bytearray([0xA6, 0x60]))                     #                             ldx $60
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01CF, bytearray([0xBF, 0x00, 0xF4, 0x0F]))         #                             lda.l level_data,x
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01D3, bytearray([0x29, 0x08]))                     #                             and #$08
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01D5, bytearray([0xF0, 0x20]))                     #                             beq handle_dragon_coins
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01D7, bytearray([0xA0, 0x5E]))                     #                             ldy.b #!icon_not_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01D9, bytearray([0x5A]))                           #                             phy 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01DA, bytearray([0x20, 0x80, 0xA3]))               #                             jsr get_translevel_bit
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01DD, bytearray([0xB9, 0xEE, 0x1F]))               #                             lda !moons_flags,y
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01E0, bytearray([0x7A]))                           #                             ply 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01E1, bytearray([0x3F, 0xA6, 0xA8, 0x0D]))         #                             and.l $0DA8A6,x
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01E5, bytearray([0xF0, 0x02]))                     #                             beq .write
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01E7, bytearray([0xA0, 0x3F]))                     #                             ldy.b #!icon_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01E9, bytearray([0x98]))                           # .write                      tya 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01EA, bytearray([0x87, 0x06]))                     #                             sta [$06]
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01EC, bytearray([0xA9, 0x0C]))                     #                             lda #$0C
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01EE, bytearray([0x87, 0x00]))                     #                             sta [$00]
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01F0, bytearray([0xA9, 0x4E]))                     #                             lda #$4E
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01F2, bytearray([0x87, 0x03]))                     #                             sta [$03]
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01F4, bytearray([0x20, 0xC0, 0xA3]))               #                             jsr update_flag_pointers
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01F7, bytearray([0xAF, 0xA6, 0xBF, 0x03]))         # handle_dragon_coins:        lda.l dragon_coin_enabled_flag
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01FB, bytearray([0xF0, 0x2A]))                     #                             beq handle_exit_2
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01FD, bytearray([0xA6, 0x60]))                     #                             ldx $60
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x01FF, bytearray([0xBF, 0x00, 0xF4, 0x0F]))         #                             lda.l level_data,x
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0203, bytearray([0x29, 0x04]))                     #                             and #$04
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0205, bytearray([0xF0, 0x20]))                     #                             beq handle_exit_2
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0207, bytearray([0xA0, 0x5E]))                     #                             ldy.b #!icon_not_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0209, bytearray([0x5A]))                           #                             phy 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x020A, bytearray([0x20, 0x80, 0xA3]))               #                             jsr get_translevel_bit
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x020D, bytearray([0xB9, 0x2F, 0x1F]))               #                             lda !yoshi_coins_flags,y
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0210, bytearray([0x7A]))                           #                             ply 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0211, bytearray([0x3F, 0xA6, 0xA8, 0x0D]))         #                             and.l $0DA8A6,x
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0215, bytearray([0xF0, 0x02]))                     #                             beq .write
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0217, bytearray([0xA0, 0x3F]))                     #                             ldy.b #!icon_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0219, bytearray([0x98]))                           # .write                      tya 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x021A, bytearray([0x87, 0x06]))                     #                             sta [$06]
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x021C, bytearray([0xA9, 0x03]))                     #                             lda #$03
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x021E, bytearray([0x87, 0x00]))                     #                             sta [$00]
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0220, bytearray([0xA9, 0x02]))                     #                             lda #$02
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0222, bytearray([0x87, 0x03]))                     #                             sta [$03]
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0224, bytearray([0x20, 0xC0, 0xA3]))               #                             jsr update_flag_pointers
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0227, bytearray([0xA6, 0x60]))                     # handle_exit_2:              ldx $60
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0229, bytearray([0xBF, 0x00, 0xF4, 0x0F]))         #                             lda.l level_data,x
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x022D, bytearray([0x29, 0x02]))                     #                             and #$02
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x022F, bytearray([0xF0, 0x1A]))                     #                             beq handle_exit_1
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0231, bytearray([0xA0, 0x5E]))                     #                             ldy.b #!icon_not_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0233, bytearray([0xBF, 0x00, 0xA2, 0x7F]))         #                             lda !level_clears,x
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0237, bytearray([0x29, 0x02]))                     #                             and #$02
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0239, bytearray([0xF0, 0x02]))                     #                             beq .write
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x023B, bytearray([0xA0, 0x3F]))                     #                             ldy.b #!icon_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x023D, bytearray([0x98]))                           # .write                      tya 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x023E, bytearray([0x87, 0x06]))                     #                             sta [$06]
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0240, bytearray([0xA9, 0x04]))                     #                             lda #$04
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0242, bytearray([0x87, 0x00]))                     #                             sta [$00]
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0244, bytearray([0xA9, 0x24]))                     #                             lda #$24
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0246, bytearray([0x87, 0x03]))                     #                             sta [$03]
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0248, bytearray([0x20, 0xC0, 0xA3]))               #                             jsr update_flag_pointers
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x024B, bytearray([0xA6, 0x60]))                     # handle_exit_1:              ldx $60
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x024D, bytearray([0xBF, 0x00, 0xF4, 0x0F]))         #                             lda.l level_data,x
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0251, bytearray([0x29, 0x01]))                     #                             and #$01
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0253, bytearray([0xF0, 0x1A]))                     #                             beq .dont_draw
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0255, bytearray([0xA0, 0x5E]))                     #                             ldy.b #!icon_not_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0257, bytearray([0xBF, 0x00, 0xA2, 0x7F]))         #                             lda !level_clears,x
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x025B, bytearray([0x29, 0x01]))                     #                             and #$01
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x025D, bytearray([0xF0, 0x02]))                     #                             beq .write
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x025F, bytearray([0xA0, 0x3F]))                     #                             ldy.b #!icon_obtained
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0261, bytearray([0x98]))                           # .write                      tya 
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0262, bytearray([0x87, 0x06]))                     #                             sta [$06]
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0264, bytearray([0xA9, 0x04]))                     #                             lda #$04
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0266, bytearray([0x87, 0x00]))                     #                             sta [$00]
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x0268, bytearray([0xA9, 0x23]))                     #                             lda #$23
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x026A, bytearray([0x87, 0x03]))                     #                             sta [$03]
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x026C, bytearray([0x20, 0xC0, 0xA3]))               #                             jsr update_flag_pointers
    rom.write_bytes(BUILD_TILEMAP_ADDR + 0x026F, bytearray([0x6B]))                           # .dont_draw                  rtl 

    LEVEL_INDICATOR_DATA_ADDR = 0x7F400
    rom.write_bytes(LEVEL_INDICATOR_DATA_ADDR + 0x0000, bytearray([0x80,0x45,0x45,0x80,0x43,0x65,0x5D,0x51]))
    rom.write_bytes(LEVEL_INDICATOR_DATA_ADDR + 0x0008, bytearray([0x01,0x47,0x47,0x51,0x65,0x45,0x41,0x4F]))
    rom.write_bytes(LEVEL_INDICATOR_DATA_ADDR + 0x0010, bytearray([0x55,0x45,0x80,0x43,0x01,0x57,0x80,0x80]))
    rom.write_bytes(LEVEL_INDICATOR_DATA_ADDR + 0x0018, bytearray([0x45,0x80,0x51,0x41,0x45,0x45,0x80,0x41]))
    rom.write_bytes(LEVEL_INDICATOR_DATA_ADDR + 0x0020, bytearray([0x45,0x41,0x4D,0x67,0x57,0x41,0x55,0x65]))
    rom.write_bytes(LEVEL_INDICATOR_DATA_ADDR + 0x0028, bytearray([0x80,0x4D,0x45,0x55,0x80,0x47,0x4D,0x45]))
    rom.write_bytes(LEVEL_INDICATOR_DATA_ADDR + 0x0030, bytearray([0x80,0x80,0x80,0x43,0x55,0x41,0x80,0x45]))
    rom.write_bytes(LEVEL_INDICATOR_DATA_ADDR + 0x0038, bytearray([0x47,0x57,0x4D,0x41,0x47,0x55,0x47,0x01]))
    rom.write_bytes(LEVEL_INDICATOR_DATA_ADDR + 0x0040, bytearray([0x41,0x4F,0x43,0x47,0x47,0x01,0x45,0x57]))
    rom.write_bytes(LEVEL_INDICATOR_DATA_ADDR + 0x0048, bytearray([0x80,0x45,0x45,0x45,0x45,0x80,0x55,0x45]))
    rom.write_bytes(LEVEL_INDICATOR_DATA_ADDR + 0x0050, bytearray([0x45,0x45,0x80,0x80,0x43,0x80,0x43,0x80]))
    rom.write_bytes(LEVEL_INDICATOR_DATA_ADDR + 0x0058, bytearray([0x07,0x43,0x43,0x80,0x80,0x80,0x80,0x80]))


def handle_indicators(rom):
    INDICATOR_QUEUE_CODE = 0x86000
    rom.write_bytes(0x022E6, bytearray([0x22, 0x00, 0xE0, 0x10])) # org $00A2E6 : jsl gm14_hijack
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0000, bytearray([0xAD, 0x00, 0x01]))       # gm14_hijack:            lda $0100
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0003, bytearray([0xC9, 0x14]))             #                         cmp #$14
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0005, bytearray([0xD0, 0x04]))             #                         bne .invalid
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0007, bytearray([0xA5, 0x71]))             #                         lda $71
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0009, bytearray([0xF0, 0x04]))             #                         beq .valid
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x000B, bytearray([0x5C, 0xB1, 0x8A, 0x02])) # .invalid                jml $028AB1
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x000F, bytearray([0xC2, 0x30]))             # .valid                  rep #$30
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0011, bytearray([0xAF, 0x04, 0xB0, 0x7F])) #                         lda !score_sprite_add_1_coin
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0015, bytearray([0xF0, 0x03]))             #                         beq .no_1_coin
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0017, bytearray([0x20, 0xC1, 0xE0]))       #                         jsr add_1_coin
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x001A, bytearray([0xAF, 0x06, 0xB0, 0x7F])) # .no_1_coin              lda !score_sprite_add_5_coins
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x001E, bytearray([0xF0, 0x03]))             #                         beq .no_5_coins
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0020, bytearray([0x20, 0xDF, 0xE0]))       #                         jsr add_5_coins
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0023, bytearray([0xAF, 0x08, 0xB0, 0x7F])) # .no_5_coins             lda !score_sprite_add_10_coins
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0027, bytearray([0xF0, 0x03]))             #                         beq .no_10_coins
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0029, bytearray([0x20, 0xFD, 0xE0]))       #                         jsr add_10_coins
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x002C, bytearray([0xAF, 0x0A, 0xB0, 0x7F])) # .no_10_coins            lda !score_sprite_add_15_coins
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0030, bytearray([0xF0, 0x03]))             #                         beq .no_15_coins
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0032, bytearray([0x20, 0x1B, 0xE1]))       #                         jsr add_15_coins
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0035, bytearray([0xAF, 0x10, 0xB0, 0x7F])) # .no_15_coins            lda !score_sprite_add_1up
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0039, bytearray([0xF0, 0x03]))             #                         beq .no_1up
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x003B, bytearray([0x20, 0x39, 0xE1]))       #                         jsr add_1up
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x003E, bytearray([0xAF, 0x0C, 0xB0, 0x7F])) # .no_1up                 lda !score_sprite_add_yoshi_egg
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0042, bytearray([0xF0, 0x03]))             #                         beq .no_yoshi_egg
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0044, bytearray([0x20, 0x57, 0xE1]))       #                         jsr add_yoshi_egg
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0047, bytearray([0xAF, 0x0E, 0xB0, 0x7F])) # .no_yoshi_egg           lda !score_sprite_add_boss_token
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x004B, bytearray([0xF0, 0x03]))             #                         beq .no_boss_token
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x004D, bytearray([0x20, 0xCF, 0xE1]))       #                         jsr add_boss_token
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0050, bytearray([0xE2, 0x30]))             # .no_boss_token          sep #$30
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0052, bytearray([0x20, 0xED, 0xE1]))       #                         jsr goal_sanity_check
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0055, bytearray([0x20, 0x5C, 0xE0]))       #                         jsr score_sprite_queue
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0058, bytearray([0x5C, 0xB1, 0x8A, 0x02])) #                         jml $028AB1
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x005C, bytearray([0xAF, 0x20, 0xB0, 0x7F])) # score_sprite_queue:     lda !score_sprite_queue_delay
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0060, bytearray([0xF0, 0x06]))             #                         beq .spawn
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0062, bytearray([0x3A]))                   #                         dec 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0063, bytearray([0x8F, 0x20, 0xB0, 0x7F])) #                         sta !score_sprite_queue_delay
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0067, bytearray([0x60]))                   #                         rts 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0068, bytearray([0xA9, 0x08]))             # .spawn                  lda #$08
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x006A, bytearray([0x8F, 0x20, 0xB0, 0x7F])) #                         sta !score_sprite_queue_delay
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x006E, bytearray([0xC2, 0x30]))             #                         rep #$30
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0070, bytearray([0xAF, 0x02, 0xB0, 0x7F])) #                         lda !score_sprite_index
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0074, bytearray([0xCF, 0x00, 0xB0, 0x7F])) #                         cmp !score_sprite_count
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0078, bytearray([0xD0, 0x03]))             #                         bne .check_slots
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x007A, bytearray([0xE2, 0x30]))             #                         sep #$30
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x007C, bytearray([0x60]))                   #                         rts 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x007D, bytearray([0xA0, 0x05, 0x00]))       # .check_slots            ldy #$0005
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0080, bytearray([0xB9, 0xE1, 0x16]))       # ..loop                  lda !score_sprite_num,y
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0083, bytearray([0x29, 0xFF, 0x00]))       #                         and #$00FF
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0086, bytearray([0xF0, 0x06]))             #                         beq .found_free
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0088, bytearray([0x88]))                   #                         dey 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0089, bytearray([0x10, 0xF5]))             #                         bpl ..loop
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x008B, bytearray([0xE2, 0x30]))             #                         sep #$30
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x008D, bytearray([0x60]))                   #                         rts 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x008E, bytearray([0xAF, 0x02, 0xB0, 0x7F])) # .found_free             lda !score_sprite_index
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0092, bytearray([0x1A]))                   #                         inc 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0093, bytearray([0xAA]))                   #                         tax 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0094, bytearray([0x8F, 0x02, 0xB0, 0x7F])) #                         sta !score_sprite_index
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0098, bytearray([0xBF, 0x22, 0xB0, 0x7F])) #                         lda !score_sprite_queue,x
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x009C, bytearray([0xE2, 0x30]))             #                         sep #$30
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x009E, bytearray([0x99, 0xE1, 0x16]))       #                         sta !score_sprite_num,y
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00A1, bytearray([0xA5, 0x94]))             #                         lda $94
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00A3, bytearray([0x99, 0xED, 0x16]))       #                         sta !score_sprite_x_lo,y
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00A6, bytearray([0xA5, 0x95]))             #                         lda $95
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00A8, bytearray([0x99, 0xF3, 0x16]))       #                         sta !score_sprite_x_hi,y
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00AB, bytearray([0xA5, 0x96]))             #                         lda $96
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00AD, bytearray([0x99, 0xE7, 0x16]))       #                         sta !score_sprite_y_lo,y
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00B0, bytearray([0xA5, 0x97]))             #                         lda $97
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00B2, bytearray([0x99, 0xF9, 0x16]))       #                         sta !score_sprite_y_hi,y
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00B5, bytearray([0xA9, 0x30]))             #                         lda #$30
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00B7, bytearray([0x99, 0xFF, 0x16]))       #                         sta !score_sprite_timer,y
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00BA, bytearray([0xAD, 0xF9, 0x13]))       #                         lda $13F9
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00BD, bytearray([0x99, 0x05, 0x17]))       #                         sta !score_sprite_layer,y
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00C0, bytearray([0x60]))                   #                         rts 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00C1, bytearray([0xAF, 0x04, 0xB0, 0x7F])) # add_1_coin:             lda !score_sprite_add_1_coin
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00C5, bytearray([0x3A]))                   #                         dec 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00C6, bytearray([0x8F, 0x04, 0xB0, 0x7F])) #                         sta !score_sprite_add_1_coin
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00CA, bytearray([0xAF, 0x00, 0xB0, 0x7F])) #                         lda !score_sprite_count
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00CE, bytearray([0x1A]))                   #                         inc 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00CF, bytearray([0x8F, 0x00, 0xB0, 0x7F])) #                         sta !score_sprite_count
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00D3, bytearray([0xAA]))                   #                         tax 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00D4, bytearray([0xE2, 0x20]))             #                         sep #$20
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00D6, bytearray([0xA9, 0x11]))             #                         lda #$11
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00D8, bytearray([0x9F, 0x22, 0xB0, 0x7F])) #                         sta !score_sprite_queue,x
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00DC, bytearray([0xC2, 0x20]))             #                         rep #$20
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00DE, bytearray([0x60]))                   #                         rts
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00DF, bytearray([0xAF, 0x06, 0xB0, 0x7F])) # add_5_coins:            lda !score_sprite_add_5_coins
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00E3, bytearray([0x3A]))                   #                         dec 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00E4, bytearray([0x8F, 0x06, 0xB0, 0x7F])) #                         sta !score_sprite_add_5_coins
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00E8, bytearray([0xAF, 0x00, 0xB0, 0x7F])) #                         lda !score_sprite_count
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00EC, bytearray([0x1A]))                   #                         inc 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00ED, bytearray([0x8F, 0x00, 0xB0, 0x7F])) #                         sta !score_sprite_count
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00F1, bytearray([0xAA]))                   #                         tax 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00F2, bytearray([0xE2, 0x20]))             #                         sep #$20
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00F4, bytearray([0xA9, 0x12]))             #                         lda #$12
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00F6, bytearray([0x9F, 0x22, 0xB0, 0x7F])) #                         sta !score_sprite_queue,x
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00FA, bytearray([0xC2, 0x20]))             #                         rep #$20
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00FC, bytearray([0x60]))                   #                         rts
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x00FD, bytearray([0xAF, 0x08, 0xB0, 0x7F])) # add_10_coins:           lda !score_sprite_add_10_coins
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0101, bytearray([0x3A]))                   #                         dec 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0102, bytearray([0x8F, 0x08, 0xB0, 0x7F])) #                         sta !score_sprite_add_10_coins
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0106, bytearray([0xAF, 0x00, 0xB0, 0x7F])) #                         lda !score_sprite_count
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x010A, bytearray([0x1A]))                   #                         inc 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x010B, bytearray([0x8F, 0x00, 0xB0, 0x7F])) #                         sta !score_sprite_count
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x010F, bytearray([0xAA]))                   #                         tax 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0110, bytearray([0xE2, 0x20]))             #                         sep #$20
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0112, bytearray([0xA9, 0x13]))             #                         lda #$13
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0114, bytearray([0x9F, 0x22, 0xB0, 0x7F])) #                         sta !score_sprite_queue,x
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0118, bytearray([0xC2, 0x20]))             #                         rep #$20
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x011A, bytearray([0x60]))                   #                         rts
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x011B, bytearray([0xAF, 0x0A, 0xB0, 0x7F])) # add_15_coins:           lda !score_sprite_add_15_coins
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x011F, bytearray([0x3A]))                   #                         dec 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0120, bytearray([0x8F, 0x0A, 0xB0, 0x7F])) #                         sta !score_sprite_add_15_coins
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0124, bytearray([0xAF, 0x00, 0xB0, 0x7F])) #                         lda !score_sprite_count
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0128, bytearray([0x1A]))                   #                         inc 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0129, bytearray([0x8F, 0x00, 0xB0, 0x7F])) #                         sta !score_sprite_count
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x012D, bytearray([0xAA]))                   #                         tax 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x012E, bytearray([0xE2, 0x20]))             #                         sep #$20
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0130, bytearray([0xA9, 0x14]))             #                         lda #$14
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0132, bytearray([0x9F, 0x22, 0xB0, 0x7F])) #                         sta !score_sprite_queue,x
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0136, bytearray([0xC2, 0x20]))             #                         rep #$20
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0138, bytearray([0x60]))                   #                         rts
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0139, bytearray([0xAF, 0x10, 0xB0, 0x7F])) # add_1up:                lda !score_sprite_add_1up
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x013D, bytearray([0x3A]))                   #                         dec 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x013E, bytearray([0x8F, 0x10, 0xB0, 0x7F])) #                         sta !score_sprite_add_1up
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0142, bytearray([0xAF, 0x00, 0xB0, 0x7F])) #                         lda !score_sprite_count
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0146, bytearray([0x1A]))                   #                         inc 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0147, bytearray([0x8F, 0x00, 0xB0, 0x7F])) #                         sta !score_sprite_count
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x014B, bytearray([0xAA]))                   #                         tax 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x014C, bytearray([0xE2, 0x20]))             #                         sep #$20
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x014E, bytearray([0xA9, 0x16]))             #                         lda #$16
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0150, bytearray([0x9F, 0x22, 0xB0, 0x7F])) #                         sta !score_sprite_queue,x
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0154, bytearray([0xC2, 0x20]))             #                         rep #$20
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0156, bytearray([0x60]))                   #                         rts
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0157, bytearray([0xAF, 0x0C, 0xB0, 0x7F])) # add_yoshi_egg:          lda !score_sprite_add_yoshi_egg
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x015B, bytearray([0x3A]))                   #                         dec 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x015C, bytearray([0x8F, 0x0C, 0xB0, 0x7F])) #                         sta !score_sprite_add_yoshi_egg
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0160, bytearray([0xAF, 0x00, 0xB0, 0x7F])) #                         lda !score_sprite_count
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0164, bytearray([0x1A]))                   #                         inc 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0165, bytearray([0x8F, 0x00, 0xB0, 0x7F])) #                         sta !score_sprite_count
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0169, bytearray([0xAA]))                   #                         tax 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x016A, bytearray([0xE2, 0x20]))             #                         sep #$20
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x016C, bytearray([0xA9, 0x15]))             #                         lda #$15
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x016E, bytearray([0x9F, 0x22, 0xB0, 0x7F])) #                         sta !score_sprite_queue,x
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0172, bytearray([0xC2, 0x20]))             #                         rep #$20
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0174, bytearray([0x60]))                   #                         rts
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0175, bytearray([0xAF, 0x12, 0xB0, 0x7F])) # add_mushroom:           lda !score_sprite_add_mushroom
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0179, bytearray([0x3A]))                   #                         dec 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x017A, bytearray([0x8F, 0x12, 0xB0, 0x7F])) #                         sta !score_sprite_add_mushroom
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x017E, bytearray([0xAF, 0x00, 0xB0, 0x7F])) #                         lda !score_sprite_count
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0182, bytearray([0x1A]))                   #                         inc 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0183, bytearray([0x8F, 0x00, 0xB0, 0x7F])) #                         sta !score_sprite_count
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0187, bytearray([0xAA]))                   #                         tax 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0188, bytearray([0xE2, 0x20]))             #                         sep #$20
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x018A, bytearray([0xA9, 0x17]))             #                         lda #$17
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x018C, bytearray([0x9F, 0x22, 0xB0, 0x7F])) #                         sta !score_sprite_queue,x
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0190, bytearray([0xC2, 0x20]))             #                         rep #$20
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0192, bytearray([0x60]))                   #                         rts
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0193, bytearray([0xAF, 0x14, 0xB0, 0x7F])) # add_flower:             lda !score_sprite_add_flower
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0197, bytearray([0x3A]))                   #                         dec 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0198, bytearray([0x8F, 0x14, 0xB0, 0x7F])) #                         sta !score_sprite_add_flower
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x019C, bytearray([0xAF, 0x00, 0xB0, 0x7F])) #                         lda !score_sprite_count
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01A0, bytearray([0x1A]))                   #                         inc 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01A1, bytearray([0x8F, 0x00, 0xB0, 0x7F])) #                         sta !score_sprite_count
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01A5, bytearray([0xAA]))                   #                         tax 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01A6, bytearray([0xE2, 0x20]))             #                         sep #$20
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01A8, bytearray([0xA9, 0x18]))             #                         lda #$18
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01AA, bytearray([0x9F, 0x22, 0xB0, 0x7F])) #                         sta !score_sprite_queue,x
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01AE, bytearray([0xC2, 0x20]))             #                         rep #$20
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01B0, bytearray([0x60]))                   #                         rts
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01B1, bytearray([0xAF, 0x16, 0xB0, 0x7F])) # add_feather:            lda !score_sprite_add_feather
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01B5, bytearray([0x3A]))                   #                         dec 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01B6, bytearray([0x8F, 0x16, 0xB0, 0x7F])) #                         sta !score_sprite_add_feather
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01BA, bytearray([0xAF, 0x00, 0xB0, 0x7F])) #                         lda !score_sprite_count
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01BE, bytearray([0x1A]))                   #                         inc 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01BF, bytearray([0x8F, 0x00, 0xB0, 0x7F])) #                         sta !score_sprite_count
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01C3, bytearray([0xAA]))                   #                         tax 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01C4, bytearray([0xE2, 0x20]))             #                         sep #$20
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01C6, bytearray([0xA9, 0x19]))             #                         lda #$19
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01C8, bytearray([0x9F, 0x22, 0xB0, 0x7F])) #                         sta !score_sprite_queue,x
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01CC, bytearray([0xC2, 0x20]))             #                         rep #$20
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01CE, bytearray([0x60]))                   #                         rts
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01CF, bytearray([0xAF, 0x0E, 0xB0, 0x7F])) # add_boss_token:         lda !score_sprite_add_boss_token
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01D3, bytearray([0x3A]))                   #                         dec 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01D4, bytearray([0x8F, 0x0E, 0xB0, 0x7F])) #                         sta !score_sprite_add_boss_token
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01D8, bytearray([0xAF, 0x00, 0xB0, 0x7F])) #                         lda !score_sprite_count
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01DC, bytearray([0x1A]))                   #                         inc 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01DD, bytearray([0x8F, 0x00, 0xB0, 0x7F])) #                         sta !score_sprite_count
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01E1, bytearray([0xAA]))                   #                         tax 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01E2, bytearray([0xE2, 0x20]))             #                         sep #$20
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01E4, bytearray([0xA9, 0x1A]))             #                         lda #$1A
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01E6, bytearray([0x9F, 0x22, 0xB0, 0x7F])) #                         sta !score_sprite_queue,x
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01EA, bytearray([0xC2, 0x20]))             #                         rep #$20
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01EC, bytearray([0x60]))                   #                         rts
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01ED, bytearray([0xAF, 0xA0, 0xBF, 0x03])) # goal_sanity_check:      lda $03BFA0
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01F1, bytearray([0x29, 0x01]))             #                         and #$01
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01F3, bytearray([0x49, 0x01]))             #                         eor #$01
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01F5, bytearray([0x0A]))                   #                         asl 
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01F6, bytearray([0xC2, 0x20]))             #                         rep #$20
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01F8, bytearray([0xBF, 0x0C, 0xB0, 0x7F])) #                         lda !score_sprite_add_yoshi_egg,x
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01FC, bytearray([0xD0, 0x18]))             #                         bne .return
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x01FE, bytearray([0xAF, 0x02, 0xB0, 0x7F])) # .check_queue            lda !score_sprite_index
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0202, bytearray([0xCF, 0x00, 0xB0, 0x7F])) #                         cmp !score_sprite_count
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0206, bytearray([0xD0, 0x0E]))             #                         bne .return
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0208, bytearray([0xE2, 0x20]))             # .check_count            sep #$20
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x020A, bytearray([0xAF, 0x1E, 0xA0, 0x7F])) #                         lda !goal_item_count
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x020E, bytearray([0xDD, 0x24, 0x1F]))       #                         cmp $1F24,x
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0211, bytearray([0xF0, 0x03]))             #                         beq .return
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0213, bytearray([0x9D, 0x24, 0x1F]))       #                         sta $1F24,x
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0216, bytearray([0xE2, 0x20]))             # .return                 sep #$20
    rom.write_bytes(INDICATOR_QUEUE_CODE + 0x0218, bytearray([0x60]))                   #                         rts 

    # Add code for indicators when receiving items during levels
    INDICATOR_CODE = 0x84000
    rom.write_bytes(0x12DBA, bytearray([0x5C, 0x00, 0xC0, 0x10])) # org $02ADBA : jsl score_sprites
    rom.write_bytes(INDICATOR_CODE + 0x0000, bytearray([0xBD, 0xE1, 0x16]))                 # score_sprites:          lda !score_sprite_num,x
    rom.write_bytes(INDICATOR_CODE + 0x0003, bytearray([0xF0, 0x2D]))                       #                         beq .return
    rom.write_bytes(INDICATOR_CODE + 0x0005, bytearray([0x8E, 0xE9, 0x15]))                 #                         stx $15E9
    rom.write_bytes(INDICATOR_CODE + 0x0008, bytearray([0xC2, 0x30]))                       #                         rep #$30
    rom.write_bytes(INDICATOR_CODE + 0x000A, bytearray([0x29, 0x1F, 0x00]))                 #                         and #$001F
    rom.write_bytes(INDICATOR_CODE + 0x000D, bytearray([0x85, 0x00]))                       #                         sta $00
    rom.write_bytes(INDICATOR_CODE + 0x000F, bytearray([0x0A]))                             #                         asl 
    rom.write_bytes(INDICATOR_CODE + 0x0010, bytearray([0x18]))                             #                         clc 
    rom.write_bytes(INDICATOR_CODE + 0x0011, bytearray([0x65, 0x00]))                       #                         adc $00
    rom.write_bytes(INDICATOR_CODE + 0x0013, bytearray([0xAA]))                             #                         tax 
    rom.write_bytes(INDICATOR_CODE + 0x0014, bytearray([0xBF, 0x37, 0xC0, 0x10]))           #                         lda.l .pointers-3,x
    rom.write_bytes(INDICATOR_CODE + 0x0018, bytearray([0x85, 0x00]))                       #                         sta $00
    rom.write_bytes(INDICATOR_CODE + 0x001A, bytearray([0xE2, 0x30]))                       #                         sep #$30
    rom.write_bytes(INDICATOR_CODE + 0x001C, bytearray([0xBF, 0x39, 0xC0, 0x10]))           #                         lda.l .pointers-3+2,x
    rom.write_bytes(INDICATOR_CODE + 0x0020, bytearray([0x85, 0x02]))                       #                         sta $02
    rom.write_bytes(INDICATOR_CODE + 0x0022, bytearray([0xE2, 0x10]))                       #                         sep #$10
    rom.write_bytes(INDICATOR_CODE + 0x0024, bytearray([0xAE, 0xE9, 0x15]))                 #                         ldx $15E9
    rom.write_bytes(INDICATOR_CODE + 0x0027, bytearray([0x8B]))                             #                         phb 
    rom.write_bytes(INDICATOR_CODE + 0x0028, bytearray([0x48]))                             #                         pha 
    rom.write_bytes(INDICATOR_CODE + 0x0029, bytearray([0xAB]))                             #                         plb 
    rom.write_bytes(INDICATOR_CODE + 0x002A, bytearray([0x4B]))                             #                         phk 
    rom.write_bytes(INDICATOR_CODE + 0x002B, bytearray([0xF4, 0x30, 0xC0]))                 #                         pea.w .return_code-1
    rom.write_bytes(INDICATOR_CODE + 0x002E, bytearray([0xDC, 0x00, 0x00]))                 #                         jml [$0000]
    rom.write_bytes(INDICATOR_CODE + 0x0031, bytearray([0xAB]))                             # .return_code            plb
    rom.write_bytes(INDICATOR_CODE + 0x0032, bytearray([0x5C, 0xC5, 0xAD, 0x02]))           # .return                 jml $02ADC5
    rom.write_bytes(INDICATOR_CODE + 0x0036, bytearray([0x9E, 0xE1, 0x16]))                 # .kill                   stz !score_sprite_num,x
    rom.write_bytes(INDICATOR_CODE + 0x0039, bytearray([0x6B]))                             #                         rtl 
    rom.write_bytes(INDICATOR_CODE + 0x003A, bytearray([0x97, 0xC0, 0x10]))                 # .pointers               dl original_score_sprites       ; 01 - 10 points
    rom.write_bytes(INDICATOR_CODE + 0x003D, bytearray([0x97, 0xC0, 0x10]))                 #                         dl original_score_sprites       ; 02 - 20 points
    rom.write_bytes(INDICATOR_CODE + 0x0040, bytearray([0x97, 0xC0, 0x10]))                 #                         dl original_score_sprites       ; 03 - 40 points
    rom.write_bytes(INDICATOR_CODE + 0x0043, bytearray([0x97, 0xC0, 0x10]))                 #                         dl original_score_sprites       ; 04 - 80 points
    rom.write_bytes(INDICATOR_CODE + 0x0046, bytearray([0x97, 0xC0, 0x10]))                 #                         dl original_score_sprites       ; 05 - 100 points
    rom.write_bytes(INDICATOR_CODE + 0x0049, bytearray([0x97, 0xC0, 0x10]))                 #                         dl original_score_sprites       ; 06 - 200 points
    rom.write_bytes(INDICATOR_CODE + 0x004C, bytearray([0x97, 0xC0, 0x10]))                 #                         dl original_score_sprites       ; 07 - 400 points
    rom.write_bytes(INDICATOR_CODE + 0x004F, bytearray([0x97, 0xC0, 0x10]))                 #                         dl original_score_sprites       ; 08 - 800 points
    rom.write_bytes(INDICATOR_CODE + 0x0052, bytearray([0x97, 0xC0, 0x10]))                 #                         dl original_score_sprites       ; 09 - 1000 points
    rom.write_bytes(INDICATOR_CODE + 0x0055, bytearray([0x97, 0xC0, 0x10]))                 #                         dl original_score_sprites       ; 0A - 2000 points
    rom.write_bytes(INDICATOR_CODE + 0x0058, bytearray([0x97, 0xC0, 0x10]))                 #                         dl original_score_sprites       ; 0B - 4000 points
    rom.write_bytes(INDICATOR_CODE + 0x005B, bytearray([0x97, 0xC0, 0x10]))                 #                         dl original_score_sprites       ; 0C - 8000 points
    rom.write_bytes(INDICATOR_CODE + 0x005E, bytearray([0x97, 0xC0, 0x10]))                 #                         dl original_score_sprites       ; 0D - 1-up
    rom.write_bytes(INDICATOR_CODE + 0x0061, bytearray([0x97, 0xC0, 0x10]))                 #                         dl original_score_sprites       ; 0E - 2-up
    rom.write_bytes(INDICATOR_CODE + 0x0064, bytearray([0x97, 0xC0, 0x10]))                 #                         dl original_score_sprites       ; 0F - 3-up
    rom.write_bytes(INDICATOR_CODE + 0x0067, bytearray([0x97, 0xC0, 0x10]))                 #                         dl original_score_sprites       ; 10 - 5-up
    rom.write_bytes(INDICATOR_CODE + 0x006A, bytearray([0xA7, 0xC0, 0x10]))                 #                         dl icon_score                   ; 11 - 1 coin
    rom.write_bytes(INDICATOR_CODE + 0x006D, bytearray([0xA7, 0xC0, 0x10]))                 #                         dl icon_score                   ; 12 - 5 coins
    rom.write_bytes(INDICATOR_CODE + 0x0070, bytearray([0xA7, 0xC0, 0x10]))                 #                         dl icon_score                   ; 13 - 10 coins
    rom.write_bytes(INDICATOR_CODE + 0x0073, bytearray([0xA7, 0xC0, 0x10]))                 #                         dl icon_score                   ; 14 - 15 coins
    rom.write_bytes(INDICATOR_CODE + 0x0076, bytearray([0xA7, 0xC0, 0x10]))                 #                         dl icon_score                   ; 15 - Yoshi Egg
    rom.write_bytes(INDICATOR_CODE + 0x0079, bytearray([0xA7, 0xC0, 0x10]))                 #                         dl icon_score                   ; 16 - 1up Mushroom
    rom.write_bytes(INDICATOR_CODE + 0x007C, bytearray([0xA7, 0xC0, 0x10]))                 #                         dl icon_score                   ; 17 - Mushroom
    rom.write_bytes(INDICATOR_CODE + 0x007F, bytearray([0xA7, 0xC0, 0x10]))                 #                         dl icon_score                   ; 18 - Flower
    rom.write_bytes(INDICATOR_CODE + 0x0082, bytearray([0xA7, 0xC0, 0x10]))                 #                         dl icon_score                   ; 19 - Feather
    rom.write_bytes(INDICATOR_CODE + 0x0085, bytearray([0xA7, 0xC0, 0x10]))                 #                         dl icon_score                   ; 1A - Boss token
    rom.write_bytes(INDICATOR_CODE + 0x0088, bytearray([0xA7, 0xC0, 0x10]))                 #                         dl icon_score                   ; 1B - 
    rom.write_bytes(INDICATOR_CODE + 0x008B, bytearray([0xA7, 0xC0, 0x10]))                 #                         dl icon_score                   ; 1C - 
    rom.write_bytes(INDICATOR_CODE + 0x008E, bytearray([0xA7, 0xC0, 0x10]))                 #                         dl icon_score                   ; 1D - 
    rom.write_bytes(INDICATOR_CODE + 0x0091, bytearray([0xA7, 0xC0, 0x10]))                 #                         dl icon_score                   ; 1E - 
    rom.write_bytes(INDICATOR_CODE + 0x0094, bytearray([0xA7, 0xC0, 0x10]))                 #                         dl icon_score                   ; 1F - 
    rom.write_bytes(INDICATOR_CODE + 0x0097, bytearray([0xA9, 0x02]))                       # original_score_sprites: lda #$02
    rom.write_bytes(INDICATOR_CODE + 0x0099, bytearray([0x48]))                             #                         pha 
    rom.write_bytes(INDICATOR_CODE + 0x009A, bytearray([0xAB]))                             #                         plb
    rom.write_bytes(INDICATOR_CODE + 0x009B, bytearray([0x4B]))                             #                         phk
    rom.write_bytes(INDICATOR_CODE + 0x009C, bytearray([0xF4, 0xA5, 0xC0]))                 #                         pea.w .jslrtsreturn-1
    rom.write_bytes(INDICATOR_CODE + 0x009F, bytearray([0xF4, 0x88, 0xB8]))                 #                         pea.w $B889-1
    rom.write_bytes(INDICATOR_CODE + 0x00A2, bytearray([0x5C, 0xC9, 0xAD, 0x02]))           #                         jml $02ADC9
    rom.write_bytes(INDICATOR_CODE + 0x00A6, bytearray([0x6B]))                             # .jslrtsreturn           rtl 
    rom.write_bytes(INDICATOR_CODE + 0x00A7, bytearray([0xBD, 0xFF, 0x16]))                 # icon_score:             lda !score_sprite_timer,x
    rom.write_bytes(INDICATOR_CODE + 0x00AA, bytearray([0xD0, 0x04]))                       #                         bne .active
    rom.write_bytes(INDICATOR_CODE + 0x00AC, bytearray([0x9E, 0xE1, 0x16]))                 #                         stz !score_sprite_num,x
    rom.write_bytes(INDICATOR_CODE + 0x00AF, bytearray([0x6B]))                             #                         rtl 
    rom.write_bytes(INDICATOR_CODE + 0x00B0, bytearray([0xDE, 0xFF, 0x16]))                 # .active                 dec !score_sprite_timer,x
    rom.write_bytes(INDICATOR_CODE + 0x00B3, bytearray([0xC9, 0x30]))                       #                         cmp #$30
    rom.write_bytes(INDICATOR_CODE + 0x00B5, bytearray([0xD0, 0x14]))                       #                         bne .handle_movement
    rom.write_bytes(INDICATOR_CODE + 0x00B7, bytearray([0xBD, 0xE1, 0x16]))                 #                         lda !score_sprite_num,x
    rom.write_bytes(INDICATOR_CODE + 0x00BA, bytearray([0x38]))                             #                         sec 
    rom.write_bytes(INDICATOR_CODE + 0x00BB, bytearray([0xE9, 0x11]))                       #                         sbc #$11
    rom.write_bytes(INDICATOR_CODE + 0x00BD, bytearray([0x0A]))                             #                         asl 
    rom.write_bytes(INDICATOR_CODE + 0x00BE, bytearray([0xA8]))                             #                         tay 
    rom.write_bytes(INDICATOR_CODE + 0x00BF, bytearray([0xC2, 0x20]))                       #                         rep #$20
    rom.write_bytes(INDICATOR_CODE + 0x00C1, bytearray([0xB9, 0x4B, 0xC2]))                 #                         lda .reward_ptrs,y 
    rom.write_bytes(INDICATOR_CODE + 0x00C4, bytearray([0x85, 0x00]))                       #                         sta $00
    rom.write_bytes(INDICATOR_CODE + 0x00C6, bytearray([0xE2, 0x20]))                       #                         sep #$20
    rom.write_bytes(INDICATOR_CODE + 0x00C8, bytearray([0x6C, 0x00, 0x00]))                 #                         jmp ($0000)
    rom.write_bytes(INDICATOR_CODE + 0x00CB, bytearray([0xBD, 0xFF, 0x16]))                 # .handle_movement        lda !score_sprite_timer,x
    rom.write_bytes(INDICATOR_CODE + 0x00CE, bytearray([0x4A]))                             #                         lsr 
    rom.write_bytes(INDICATOR_CODE + 0x00CF, bytearray([0x4A]))                             #                         lsr 
    rom.write_bytes(INDICATOR_CODE + 0x00D0, bytearray([0x4A]))                             #                         lsr  
    rom.write_bytes(INDICATOR_CODE + 0x00D1, bytearray([0x4A]))                             #                         lsr 
    rom.write_bytes(INDICATOR_CODE + 0x00D2, bytearray([0xA8]))                             #                         tay 
    rom.write_bytes(INDICATOR_CODE + 0x00D3, bytearray([0xA5, 0x13]))                       #                         lda $13
    rom.write_bytes(INDICATOR_CODE + 0x00D5, bytearray([0x39, 0xF0, 0xC0]))                 #                         and .speed,y
    rom.write_bytes(INDICATOR_CODE + 0x00D8, bytearray([0xD0, 0x14]))                       #                         bne ..skip_update
    rom.write_bytes(INDICATOR_CODE + 0x00DA, bytearray([0xBD, 0xE7, 0x16]))                 #                         lda !score_sprite_y_lo,x
    rom.write_bytes(INDICATOR_CODE + 0x00DD, bytearray([0xA8]))                             #                         tay 
    rom.write_bytes(INDICATOR_CODE + 0x00DE, bytearray([0x38]))                             #                         sec 
    rom.write_bytes(INDICATOR_CODE + 0x00DF, bytearray([0xE5, 0x1C]))                       #                         sbc $1C
    rom.write_bytes(INDICATOR_CODE + 0x00E1, bytearray([0xC9, 0x04]))                       #                         cmp #$04
    rom.write_bytes(INDICATOR_CODE + 0x00E3, bytearray([0x90, 0x09]))                       #                         bcc ..skip_update
    rom.write_bytes(INDICATOR_CODE + 0x00E5, bytearray([0xDE, 0xE7, 0x16]))                 #                         dec !score_sprite_y_lo,x
    rom.write_bytes(INDICATOR_CODE + 0x00E8, bytearray([0x98]))                             #                         tya 
    rom.write_bytes(INDICATOR_CODE + 0x00E9, bytearray([0xD0, 0x03]))                       #                         bne ..skip_update
    rom.write_bytes(INDICATOR_CODE + 0x00EB, bytearray([0xDE, 0xF9, 0x16]))                 #                         dec !score_sprite_y_hi,x
    rom.write_bytes(INDICATOR_CODE + 0x00EE, bytearray([0x80, 0x05]))                       # ..skip_update           bra .gfx 
    rom.write_bytes(INDICATOR_CODE + 0x00F0, bytearray([0x03, 0x01, 0x00, 0x00]))           # .speed                  db $03,$01,$00,$00
    rom.write_bytes(INDICATOR_CODE + 0x00F4, bytearray([0x6B]))                             # .return                 rtl
    rom.write_bytes(INDICATOR_CODE + 0x00F5, bytearray([0xBD, 0x05, 0x17]))                 # .gfx                    lda !score_sprite_layer,x
    rom.write_bytes(INDICATOR_CODE + 0x00F8, bytearray([0x0A]))                             #                         asl
    rom.write_bytes(INDICATOR_CODE + 0x00F9, bytearray([0x0A]))                             #                         asl 
    rom.write_bytes(INDICATOR_CODE + 0x00FA, bytearray([0xA8]))                             #                         tay 
    rom.write_bytes(INDICATOR_CODE + 0x00FB, bytearray([0xC2, 0x20]))                       #                         rep #$20
    rom.write_bytes(INDICATOR_CODE + 0x00FD, bytearray([0xB9, 0x1C, 0x00]))                 #                         lda $001C,y
    rom.write_bytes(INDICATOR_CODE + 0x0100, bytearray([0x85, 0x02]))                       #                         sta $02
    rom.write_bytes(INDICATOR_CODE + 0x0102, bytearray([0xB9, 0x1A, 0x00]))                 #                         lda $001A,y
    rom.write_bytes(INDICATOR_CODE + 0x0105, bytearray([0x85, 0x04]))                       #                         sta $04
    rom.write_bytes(INDICATOR_CODE + 0x0107, bytearray([0xE2, 0x20]))                       #                         sep #$20
    rom.write_bytes(INDICATOR_CODE + 0x0109, bytearray([0xBD, 0xF3, 0x16]))                 #                         lda !score_sprite_x_hi,x
    rom.write_bytes(INDICATOR_CODE + 0x010C, bytearray([0xEB]))                             #                         xba 
    rom.write_bytes(INDICATOR_CODE + 0x010D, bytearray([0xBD, 0xED, 0x16]))                 #                         lda !score_sprite_x_lo,x
    rom.write_bytes(INDICATOR_CODE + 0x0110, bytearray([0xC2, 0x20]))                       #                         rep #$20
    rom.write_bytes(INDICATOR_CODE + 0x0112, bytearray([0x38]))                             #                         sec 
    rom.write_bytes(INDICATOR_CODE + 0x0113, bytearray([0xE5, 0x04]))                       #                         sbc $04
    rom.write_bytes(INDICATOR_CODE + 0x0115, bytearray([0x38]))                             #                         sec 
    rom.write_bytes(INDICATOR_CODE + 0x0116, bytearray([0xE9, 0x06, 0x00]))                 #                         sbc #$0006
    rom.write_bytes(INDICATOR_CODE + 0x0119, bytearray([0xC9, 0xEA, 0x00]))                 #                         cmp #$00EA
    rom.write_bytes(INDICATOR_CODE + 0x011C, bytearray([0xE2, 0x20]))                       #                         sep #$20
    rom.write_bytes(INDICATOR_CODE + 0x011E, bytearray([0xB0, 0xD4]))                       #                         bcs .return
    rom.write_bytes(INDICATOR_CODE + 0x0120, bytearray([0xBD, 0xE7, 0x16]))                 #                         lda !score_sprite_y_lo,x
    rom.write_bytes(INDICATOR_CODE + 0x0123, bytearray([0xC5, 0x02]))                       #                         cmp $02
    rom.write_bytes(INDICATOR_CODE + 0x0125, bytearray([0xBD, 0xF9, 0x16]))                 #                         lda !score_sprite_y_hi,x
    rom.write_bytes(INDICATOR_CODE + 0x0128, bytearray([0xE5, 0x03]))                       #                         sbc $03
    rom.write_bytes(INDICATOR_CODE + 0x012A, bytearray([0xD0, 0xC8]))                       #                         bne .return 
    rom.write_bytes(INDICATOR_CODE + 0x012C, bytearray([0xBF, 0x9E, 0xAD, 0x02]))           #                         lda $02AD9E,x
    rom.write_bytes(INDICATOR_CODE + 0x0130, bytearray([0xA8]))                             #                         tay 
    rom.write_bytes(INDICATOR_CODE + 0x0131, bytearray([0xBD, 0xE7, 0x16]))                 #                         lda !score_sprite_y_lo,x
    rom.write_bytes(INDICATOR_CODE + 0x0134, bytearray([0x38]))                             #                         sec 
    rom.write_bytes(INDICATOR_CODE + 0x0135, bytearray([0xE5, 0x02]))                       #                         sbc $02
    rom.write_bytes(INDICATOR_CODE + 0x0137, bytearray([0x99, 0x01, 0x02]))                 #                         sta $0201,y
    rom.write_bytes(INDICATOR_CODE + 0x013A, bytearray([0x99, 0x05, 0x02]))                 #                         sta $0205,y
    rom.write_bytes(INDICATOR_CODE + 0x013D, bytearray([0xBD, 0xED, 0x16]))                 #                         lda !score_sprite_x_lo,x
    rom.write_bytes(INDICATOR_CODE + 0x0140, bytearray([0x38]))                             #                         sec 
    rom.write_bytes(INDICATOR_CODE + 0x0141, bytearray([0xE5, 0x04]))                       #                         sbc $04
    rom.write_bytes(INDICATOR_CODE + 0x0143, bytearray([0x18]))                             #                         clc 
    rom.write_bytes(INDICATOR_CODE + 0x0144, bytearray([0x69, 0x09]))                       #                         adc #$09
    rom.write_bytes(INDICATOR_CODE + 0x0146, bytearray([0x99, 0x00, 0x02]))                 #                         sta $0200,y
    rom.write_bytes(INDICATOR_CODE + 0x0149, bytearray([0x18]))                             #                         clc 
    rom.write_bytes(INDICATOR_CODE + 0x014A, bytearray([0x69, 0x05]))                       #                         adc #$05
    rom.write_bytes(INDICATOR_CODE + 0x014C, bytearray([0x99, 0x04, 0x02]))                 #                         sta $0204,y
    rom.write_bytes(INDICATOR_CODE + 0x014F, bytearray([0xDA]))                             #                         phx 
    rom.write_bytes(INDICATOR_CODE + 0x0150, bytearray([0xBD, 0xE1, 0x16]))                 #                         lda !score_sprite_num,x
    rom.write_bytes(INDICATOR_CODE + 0x0153, bytearray([0x38]))                             #                         sec 
    rom.write_bytes(INDICATOR_CODE + 0x0154, bytearray([0xE9, 0x11]))                       #                         sbc #$11
    rom.write_bytes(INDICATOR_CODE + 0x0156, bytearray([0x0A]))                             #                         asl 
    rom.write_bytes(INDICATOR_CODE + 0x0157, bytearray([0xAA]))                             #                         tax 
    rom.write_bytes(INDICATOR_CODE + 0x0158, bytearray([0xBD, 0x09, 0xC2]))                 #                         lda ..num_tile+$00,x 
    rom.write_bytes(INDICATOR_CODE + 0x015B, bytearray([0x99, 0x02, 0x02]))                 #                         sta $0202,y
    rom.write_bytes(INDICATOR_CODE + 0x015E, bytearray([0xBD, 0x0A, 0xC2]))                 #                         lda ..num_tile+$01,x
    rom.write_bytes(INDICATOR_CODE + 0x0161, bytearray([0x99, 0x06, 0x02]))                 #                         sta $0206,y
    rom.write_bytes(INDICATOR_CODE + 0x0164, bytearray([0xBD, 0x27, 0xC2]))                 #                         lda ..num_props+$00,x
    rom.write_bytes(INDICATOR_CODE + 0x0167, bytearray([0x99, 0x03, 0x02]))                 #                         sta $0203,y
    rom.write_bytes(INDICATOR_CODE + 0x016A, bytearray([0xBD, 0x28, 0xC2]))                 #                         lda ..num_props+$01,x
    rom.write_bytes(INDICATOR_CODE + 0x016D, bytearray([0x99, 0x07, 0x02]))                 #                         sta $0207,y
    rom.write_bytes(INDICATOR_CODE + 0x0170, bytearray([0xFA]))                             #                         plx 
    rom.write_bytes(INDICATOR_CODE + 0x0171, bytearray([0x98]))                             #                         tya 
    rom.write_bytes(INDICATOR_CODE + 0x0172, bytearray([0x4A]))                             #                         lsr 
    rom.write_bytes(INDICATOR_CODE + 0x0173, bytearray([0x4A]))                             #                         lsr 
    rom.write_bytes(INDICATOR_CODE + 0x0174, bytearray([0xA8]))                             #                         tay 
    rom.write_bytes(INDICATOR_CODE + 0x0175, bytearray([0xA9, 0x00]))                       #                         lda #$00
    rom.write_bytes(INDICATOR_CODE + 0x0177, bytearray([0x99, 0x20, 0x04]))                 #                         sta $0420,y
    rom.write_bytes(INDICATOR_CODE + 0x017A, bytearray([0x99, 0x21, 0x04]))                 #                         sta $0421,y
    rom.write_bytes(INDICATOR_CODE + 0x017D, bytearray([0xBF, 0x45, 0xC2, 0x10]))           #                         lda.l ..oam_2,x
    rom.write_bytes(INDICATOR_CODE + 0x0181, bytearray([0xA8]))                             #                         tay 
    rom.write_bytes(INDICATOR_CODE + 0x0182, bytearray([0xBD, 0xE7, 0x16]))                 #                         lda !score_sprite_y_lo,x
    rom.write_bytes(INDICATOR_CODE + 0x0185, bytearray([0x38]))                             #                         sec 
    rom.write_bytes(INDICATOR_CODE + 0x0186, bytearray([0xE5, 0x02]))                       #                         sbc $02
    rom.write_bytes(INDICATOR_CODE + 0x0188, bytearray([0x99, 0x01, 0x02]))                 #                         sta $0201,y
    rom.write_bytes(INDICATOR_CODE + 0x018B, bytearray([0x99, 0x05, 0x02]))                 #                         sta $0205,y
    rom.write_bytes(INDICATOR_CODE + 0x018E, bytearray([0xBD, 0xED, 0x16]))                 #                         lda !score_sprite_x_lo,x
    rom.write_bytes(INDICATOR_CODE + 0x0191, bytearray([0x38]))                             #                         sec 
    rom.write_bytes(INDICATOR_CODE + 0x0192, bytearray([0xE5, 0x04]))                       #                         sbc $04
    rom.write_bytes(INDICATOR_CODE + 0x0194, bytearray([0xE9, 0x07]))                       #                         sbc #$07
    rom.write_bytes(INDICATOR_CODE + 0x0196, bytearray([0x99, 0x00, 0x02]))                 #                         sta $0200,y
    rom.write_bytes(INDICATOR_CODE + 0x0199, bytearray([0x18]))                             #                         clc 
    rom.write_bytes(INDICATOR_CODE + 0x019A, bytearray([0x69, 0x08]))                       #                         adc #$08
    rom.write_bytes(INDICATOR_CODE + 0x019C, bytearray([0x99, 0x04, 0x02]))                 #                         sta $0204,y
    rom.write_bytes(INDICATOR_CODE + 0x019F, bytearray([0xDA]))                             #                         phx 
    rom.write_bytes(INDICATOR_CODE + 0x01A0, bytearray([0xBD, 0xE1, 0x16]))                 #                         lda !score_sprite_num,x
    rom.write_bytes(INDICATOR_CODE + 0x01A3, bytearray([0x38]))                             #                         sec 
    rom.write_bytes(INDICATOR_CODE + 0x01A4, bytearray([0xE9, 0x11]))                       #                         sbc #$11
    rom.write_bytes(INDICATOR_CODE + 0x01A6, bytearray([0xAA]))                             #                         tax 
    rom.write_bytes(INDICATOR_CODE + 0x01A7, bytearray([0xBD, 0xCD, 0xC1]))                 #                         lda ..icon_tile,x
    rom.write_bytes(INDICATOR_CODE + 0x01AA, bytearray([0x99, 0x02, 0x02]))                 #                         sta $0202,y
    rom.write_bytes(INDICATOR_CODE + 0x01AD, bytearray([0xBD, 0xDC, 0xC1]))                 #                         lda ..icon_props,x
    rom.write_bytes(INDICATOR_CODE + 0x01B0, bytearray([0x99, 0x03, 0x02]))                 #                         sta $0203,y
    rom.write_bytes(INDICATOR_CODE + 0x01B3, bytearray([0xBD, 0xFA, 0xC1]))                 #                         lda ..plus_props,x
    rom.write_bytes(INDICATOR_CODE + 0x01B6, bytearray([0x99, 0x07, 0x02]))                 #                         sta $0207,y
    rom.write_bytes(INDICATOR_CODE + 0x01B9, bytearray([0xBD, 0xEB, 0xC1]))                 #                         lda ..plus_tile,x
    rom.write_bytes(INDICATOR_CODE + 0x01BC, bytearray([0x99, 0x06, 0x02]))                 #                         sta $0206,y
    rom.write_bytes(INDICATOR_CODE + 0x01BF, bytearray([0xFA]))                             #                         plx 
    rom.write_bytes(INDICATOR_CODE + 0x01C0, bytearray([0x98]))                             #                         tya 
    rom.write_bytes(INDICATOR_CODE + 0x01C1, bytearray([0x4A]))                             #                         lsr
    rom.write_bytes(INDICATOR_CODE + 0x01C2, bytearray([0x4A]))                             #                         lsr 
    rom.write_bytes(INDICATOR_CODE + 0x01C3, bytearray([0xA8]))                             #                         tay 
    rom.write_bytes(INDICATOR_CODE + 0x01C4, bytearray([0xA9, 0x00]))                       #                         lda #$00
    rom.write_bytes(INDICATOR_CODE + 0x01C6, bytearray([0x99, 0x20, 0x04]))                 #                         sta $0420,y
    rom.write_bytes(INDICATOR_CODE + 0x01C9, bytearray([0x99, 0x21, 0x04]))                 #                         sta $0421,y
    rom.write_bytes(INDICATOR_CODE + 0x01CC, bytearray([0x6B]))                             #                         rtl 
    rom.write_bytes(INDICATOR_CODE + 0x01CD, bytearray([0x1B]))                             # ..icon_tile             db $1B      ; 1 coin
    rom.write_bytes(INDICATOR_CODE + 0x01CE, bytearray([0x1B]))                             #                         db $1B      ; 5 coins
    rom.write_bytes(INDICATOR_CODE + 0x01CF, bytearray([0x1B]))                             #                         db $1B      ; 10 coins
    rom.write_bytes(INDICATOR_CODE + 0x01D0, bytearray([0x1B]))                             #                         db $1B      ; 15 coins
    rom.write_bytes(INDICATOR_CODE + 0x01D1, bytearray([0x0A]))                             #                         db $0A      ; yoshi egg
    rom.write_bytes(INDICATOR_CODE + 0x01D2, bytearray([0x0B]))                             #                         db $0B      ; 1up mushroom
    rom.write_bytes(INDICATOR_CODE + 0x01D3, bytearray([0x0B]))                             #                         db $0B      ; mushroom
    rom.write_bytes(INDICATOR_CODE + 0x01D4, bytearray([0x7E]))                             #                         db $7E      ; flower
    rom.write_bytes(INDICATOR_CODE + 0x01D5, bytearray([0x7F]))                             #                         db $7F      ; feather
    rom.write_bytes(INDICATOR_CODE + 0x01D6, bytearray([0x38]))                             #                         db $38      ; boss token
    rom.write_bytes(INDICATOR_CODE + 0x01D7, bytearray([0x5A]))                             #                         db $5A      ;  
    rom.write_bytes(INDICATOR_CODE + 0x01D8, bytearray([0x5A]))                             #                         db $5A      ;  
    rom.write_bytes(INDICATOR_CODE + 0x01D9, bytearray([0x5A]))                             #                         db $5A      ;  
    rom.write_bytes(INDICATOR_CODE + 0x01DA, bytearray([0x5A]))                             #                         db $5A      ;  
    rom.write_bytes(INDICATOR_CODE + 0x01DB, bytearray([0x0B]))                             #                         db $0B      ;  
    rom.write_bytes(INDICATOR_CODE + 0x01DC, bytearray([0x34]))                             # ..icon_props            db $34      ; coin
    rom.write_bytes(INDICATOR_CODE + 0x01DD, bytearray([0x34]))                             #                         db $34      ; coin
    rom.write_bytes(INDICATOR_CODE + 0x01DE, bytearray([0x34]))                             #                         db $34      ; coin
    rom.write_bytes(INDICATOR_CODE + 0x01DF, bytearray([0x34]))                             #                         db $34      ; coin
    rom.write_bytes(INDICATOR_CODE + 0x01E0, bytearray([0x3A]))                             #                         db $3A      ; yoshi egg
    rom.write_bytes(INDICATOR_CODE + 0x01E1, bytearray([0x3A]))                             #                         db $3A      ; 1up mushroom
    rom.write_bytes(INDICATOR_CODE + 0x01E2, bytearray([0x38]))                             #                         db $38      ; mushroom
    rom.write_bytes(INDICATOR_CODE + 0x01E3, bytearray([0x3A]))                             #                         db $3A      ; flower
    rom.write_bytes(INDICATOR_CODE + 0x01E4, bytearray([0x34]))                             #                         db $34      ; feather
    rom.write_bytes(INDICATOR_CODE + 0x01E5, bytearray([0x34]))                             #                         db $34      ; boss token
    rom.write_bytes(INDICATOR_CODE + 0x01E6, bytearray([0x34]))                             #                         db $34      ;  
    rom.write_bytes(INDICATOR_CODE + 0x01E7, bytearray([0x3A]))                             #                         db $3A      ;  
    rom.write_bytes(INDICATOR_CODE + 0x01E8, bytearray([0x38]))                             #                         db $38      ;  
    rom.write_bytes(INDICATOR_CODE + 0x01E9, bytearray([0x36]))                             #                         db $36      ;  
    rom.write_bytes(INDICATOR_CODE + 0x01EA, bytearray([0x36]))                             #                         db $36      ;  
    rom.write_bytes(INDICATOR_CODE + 0x01EB, bytearray([0x1A]))                             # ..plus_tile             db $1A      ; 1 coin
    rom.write_bytes(INDICATOR_CODE + 0x01EC, bytearray([0x1A]))                             #                         db $1A      ; 3 coins
    rom.write_bytes(INDICATOR_CODE + 0x01ED, bytearray([0x1A]))                             #                         db $1A      ; 5 coins
    rom.write_bytes(INDICATOR_CODE + 0x01EE, bytearray([0x1A]))                             #                         db $1A      ; 10 coins
    rom.write_bytes(INDICATOR_CODE + 0x01EF, bytearray([0x1A]))                             #                         db $1A      ; yoshi egg
    rom.write_bytes(INDICATOR_CODE + 0x01F0, bytearray([0x1A]))                             #                         db $1A      ; 1up mushroom
    rom.write_bytes(INDICATOR_CODE + 0x01F1, bytearray([0x1A]))                             #                         db $1A      ; mushroom
    rom.write_bytes(INDICATOR_CODE + 0x01F2, bytearray([0x1A]))                             #                         db $1A      ; flower
    rom.write_bytes(INDICATOR_CODE + 0x01F3, bytearray([0x1A]))                             #                         db $1A      ; feather
    rom.write_bytes(INDICATOR_CODE + 0x01F4, bytearray([0x1A]))                             #                         db $1A      ; boss token
    rom.write_bytes(INDICATOR_CODE + 0x01F5, bytearray([0x1A]))                             #                         db $1A      ; 
    rom.write_bytes(INDICATOR_CODE + 0x01F6, bytearray([0x1A]))                             #                         db $1A      ; 
    rom.write_bytes(INDICATOR_CODE + 0x01F7, bytearray([0x1A]))                             #                         db $1A      ; 
    rom.write_bytes(INDICATOR_CODE + 0x01F8, bytearray([0x1A]))                             #                         db $1A      ; 
    rom.write_bytes(INDICATOR_CODE + 0x01F9, bytearray([0x1A]))                             #                         db $1A      ; 
    rom.write_bytes(INDICATOR_CODE + 0x01FA, bytearray([0x32]))                             # ..plus_props            db $32      ; 1 coin
    rom.write_bytes(INDICATOR_CODE + 0x01FB, bytearray([0x32]))                             #                         db $32      ; 5 coins
    rom.write_bytes(INDICATOR_CODE + 0x01FC, bytearray([0x32]))                             #                         db $32      ; 10 coins
    rom.write_bytes(INDICATOR_CODE + 0x01FD, bytearray([0x32]))                             #                         db $32      ; 50 coins
    rom.write_bytes(INDICATOR_CODE + 0x01FE, bytearray([0x32]))                             #                         db $32      ; yoshi egg
    rom.write_bytes(INDICATOR_CODE + 0x01FF, bytearray([0x32]))                             #                         db $32      ; 1up mushroom
    rom.write_bytes(INDICATOR_CODE + 0x0200, bytearray([0x32]))                             #                         db $32      ; mushroom
    rom.write_bytes(INDICATOR_CODE + 0x0201, bytearray([0x32]))                             #                         db $32      ; flower
    rom.write_bytes(INDICATOR_CODE + 0x0202, bytearray([0x32]))                             #                         db $32      ; feather
    rom.write_bytes(INDICATOR_CODE + 0x0203, bytearray([0x32]))                             #                         db $32      ; boss token
    rom.write_bytes(INDICATOR_CODE + 0x0204, bytearray([0x32]))                             #                         db $32      ; 
    rom.write_bytes(INDICATOR_CODE + 0x0205, bytearray([0x32]))                             #                         db $32      ;  
    rom.write_bytes(INDICATOR_CODE + 0x0206, bytearray([0x32]))                             #                         db $32      ;  
    rom.write_bytes(INDICATOR_CODE + 0x0207, bytearray([0x32]))                             #                         db $32      ;  
    rom.write_bytes(INDICATOR_CODE + 0x0208, bytearray([0x32]))                             #                         db $32      ;  
    rom.write_bytes(INDICATOR_CODE + 0x0209, bytearray([0x4B, 0x69]))                       # ..num_tile              db $4B,$69  ; 1 coin
    rom.write_bytes(INDICATOR_CODE + 0x020B, bytearray([0x5B, 0x69]))                       #                         db $5B,$69  ; 5 coins
    rom.write_bytes(INDICATOR_CODE + 0x020D, bytearray([0x4B, 0x4A]))                       #                         db $4B,$4A  ; 10 coins
    rom.write_bytes(INDICATOR_CODE + 0x020F, bytearray([0x5B, 0x4A]))                       #                         db $4B,$5B  ; 50 coins
    rom.write_bytes(INDICATOR_CODE + 0x0211, bytearray([0x4B, 0x69]))                       #                         db $4B,$69  ; yoshi egg
    rom.write_bytes(INDICATOR_CODE + 0x0213, bytearray([0x4B, 0x69]))                       #                         db $4B,$69  ; 1up mushroom
    rom.write_bytes(INDICATOR_CODE + 0x0215, bytearray([0x4B, 0x69]))                       #                         db $4B,$69  ; mushroom
    rom.write_bytes(INDICATOR_CODE + 0x0217, bytearray([0x4B, 0x69]))                       #                         db $4B,$69  ; flower
    rom.write_bytes(INDICATOR_CODE + 0x0219, bytearray([0x4B, 0x69]))                       #                         db $4B,$69  ; feather
    rom.write_bytes(INDICATOR_CODE + 0x021B, bytearray([0x4B, 0x69]))                       #                         db $4B,$69  ; boss token
    rom.write_bytes(INDICATOR_CODE + 0x021D, bytearray([0x69, 0x69]))                       #                         db $69,$69  ;  
    rom.write_bytes(INDICATOR_CODE + 0x021F, bytearray([0x69, 0x69]))                       #                         db $69,$69  ;  
    rom.write_bytes(INDICATOR_CODE + 0x0221, bytearray([0x69, 0x69]))                       #                         db $69,$69  ;  
    rom.write_bytes(INDICATOR_CODE + 0x0223, bytearray([0x69, 0x69]))                       #                         db $69,$69  ;  
    rom.write_bytes(INDICATOR_CODE + 0x0225, bytearray([0x69, 0x69]))                       #                         db $69,$69  ; 
    rom.write_bytes(INDICATOR_CODE + 0x0227, bytearray([0x34, 0x34]))                       # ..num_props             db $34,$34  ; 1 coin
    rom.write_bytes(INDICATOR_CODE + 0x0229, bytearray([0x34, 0x34]))                       #                         db $34,$34  ; 5 coins
    rom.write_bytes(INDICATOR_CODE + 0x022B, bytearray([0x34, 0x34]))                       #                         db $34,$34  ; 10 coins
    rom.write_bytes(INDICATOR_CODE + 0x022D, bytearray([0x34, 0x34]))                       #                         db $34,$34  ; 50 coins
    rom.write_bytes(INDICATOR_CODE + 0x022F, bytearray([0x34, 0x34]))                       #                         db $34,$34  ; yoshi egg
    rom.write_bytes(INDICATOR_CODE + 0x0231, bytearray([0x34, 0x34]))                       #                         db $34,$34  ; 1up mushroom
    rom.write_bytes(INDICATOR_CODE + 0x0233, bytearray([0x34, 0x34]))                       #                         db $34,$34  ; mushroom
    rom.write_bytes(INDICATOR_CODE + 0x0235, bytearray([0x34, 0x34]))                       #                         db $34,$34  ; flower
    rom.write_bytes(INDICATOR_CODE + 0x0237, bytearray([0x34, 0x34]))                       #                         db $34,$34  ; feather
    rom.write_bytes(INDICATOR_CODE + 0x0239, bytearray([0x34, 0x34]))                       #                         db $34,$34  ; boss token
    rom.write_bytes(INDICATOR_CODE + 0x023B, bytearray([0x34, 0x34]))                       #                         db $34,$34  ;  
    rom.write_bytes(INDICATOR_CODE + 0x023D, bytearray([0x34, 0x34]))                       #                         db $34,$34  ;  
    rom.write_bytes(INDICATOR_CODE + 0x023F, bytearray([0x34, 0x34]))                       #                         db $34,$34  ; 
    rom.write_bytes(INDICATOR_CODE + 0x0241, bytearray([0x34, 0x34]))                       #                         db $34,$34  ;  
    rom.write_bytes(INDICATOR_CODE + 0x0243, bytearray([0x34, 0x34]))                       #                         db $34,$34  ;  
    rom.write_bytes(INDICATOR_CODE + 0x0245, bytearray([0x50, 0x58, 0x60, 0x68, 0x70, 0x78]))# ..oam_2                 db $50,$58,$60,$68,$70,$78
    rom.write_bytes(INDICATOR_CODE + 0x024B, bytearray([0x69, 0xC2]))                       # .reward_ptrs            dw .one_coin
    rom.write_bytes(INDICATOR_CODE + 0x024D, bytearray([0x6D, 0xC2]))                       #                         dw .five_coins
    rom.write_bytes(INDICATOR_CODE + 0x024F, bytearray([0x71, 0xC2]))                       #                         dw .ten_coins
    rom.write_bytes(INDICATOR_CODE + 0x0251, bytearray([0x75, 0xC2]))                       #                         dw .fifty_coins
    rom.write_bytes(INDICATOR_CODE + 0x0253, bytearray([0x8A, 0xC2]))                       #                         dw .yoshi_egg
    rom.write_bytes(INDICATOR_CODE + 0x0255, bytearray([0xA7, 0xC2]))                       #                         dw .green_mushroom
    rom.write_bytes(INDICATOR_CODE + 0x0257, bytearray([0xAD, 0xC2]))                       #                         dw .mushroom
    rom.write_bytes(INDICATOR_CODE + 0x0259, bytearray([0xAF, 0xC2]))                       #                         dw .flower
    rom.write_bytes(INDICATOR_CODE + 0x025B, bytearray([0xB1, 0xC2]))                       #                         dw .shared_item
    rom.write_bytes(INDICATOR_CODE + 0x025D, bytearray([0x9C, 0xC2]))                       #                         dw .boss_token
    rom.write_bytes(INDICATOR_CODE + 0x025F, bytearray([0xCB, 0xC0]))                       #                         dw .handle_movement
    rom.write_bytes(INDICATOR_CODE + 0x0261, bytearray([0xCB, 0xC0]))                       #                         dw .handle_movement
    rom.write_bytes(INDICATOR_CODE + 0x0263, bytearray([0xCB, 0xC0]))                       #                         dw .handle_movement
    rom.write_bytes(INDICATOR_CODE + 0x0265, bytearray([0xCB, 0xC0]))                       #                         dw .handle_movement
    rom.write_bytes(INDICATOR_CODE + 0x0267, bytearray([0xCB, 0xC0]))                       #                         dw .handle_movement
    rom.write_bytes(INDICATOR_CODE + 0x0269, bytearray([0xA9, 0x01]))                       # .one_coin               lda #$01
    rom.write_bytes(INDICATOR_CODE + 0x026B, bytearray([0x80, 0x0A]))                       #                         bra .shared_coins
    rom.write_bytes(INDICATOR_CODE + 0x026D, bytearray([0xA9, 0x05]))                       # .five_coins             lda #$05
    rom.write_bytes(INDICATOR_CODE + 0x026F, bytearray([0x80, 0x06]))                       #                         bra .shared_coins
    rom.write_bytes(INDICATOR_CODE + 0x0271, bytearray([0xA9, 0x0A]))                       # .ten_coins              lda #$0A
    rom.write_bytes(INDICATOR_CODE + 0x0273, bytearray([0x80, 0x02]))                       #                         bra .shared_coins
    rom.write_bytes(INDICATOR_CODE + 0x0275, bytearray([0xA9, 0x32]))                       # .fifty_coins            lda #$32
    rom.write_bytes(INDICATOR_CODE + 0x0277, bytearray([0x18]))                             # .shared_coins           clc 
    rom.write_bytes(INDICATOR_CODE + 0x0278, bytearray([0x6D, 0xCC, 0x13]))                 #                         adc $13CC
    rom.write_bytes(INDICATOR_CODE + 0x027B, bytearray([0x90, 0x02]))                       #                         bcc +
    rom.write_bytes(INDICATOR_CODE + 0x027D, bytearray([0xA9, 0xFF]))                       #                         lda #$FF
    rom.write_bytes(INDICATOR_CODE + 0x027F, bytearray([0x8D, 0xCC, 0x13]))                 # +                       sta $13CC
    rom.write_bytes(INDICATOR_CODE + 0x0282, bytearray([0xA9, 0x01]))                       #                         lda #$01
    rom.write_bytes(INDICATOR_CODE + 0x0284, bytearray([0x8D, 0xFC, 0x1D]))                 #                         sta $1DFC
    rom.write_bytes(INDICATOR_CODE + 0x0287, bytearray([0x4C, 0xCB, 0xC0]))                 #                         jmp .handle_movement
    rom.write_bytes(INDICATOR_CODE + 0x028A, bytearray([0xAD, 0x24, 0x1F]))                 # .yoshi_egg              lda $1F24
    rom.write_bytes(INDICATOR_CODE + 0x028D, bytearray([0xC9, 0xFF]))                       #                         cmp #$FF
    rom.write_bytes(INDICATOR_CODE + 0x028F, bytearray([0xF0, 0x03]))                       #                         beq ..nope
    rom.write_bytes(INDICATOR_CODE + 0x0291, bytearray([0xEE, 0x24, 0x1F]))                 #                         inc $1F24
    rom.write_bytes(INDICATOR_CODE + 0x0294, bytearray([0xA9, 0x1F]))                       # ..nope                  lda #$1F
    rom.write_bytes(INDICATOR_CODE + 0x0296, bytearray([0x8D, 0xFC, 0x1D]))                 #                         sta $1DFC
    rom.write_bytes(INDICATOR_CODE + 0x0299, bytearray([0x4C, 0xCB, 0xC0]))                 #                         jmp .handle_movement
    rom.write_bytes(INDICATOR_CODE + 0x029C, bytearray([0xEE, 0x26, 0x1F]))                 # .boss_token             inc $1F26
    rom.write_bytes(INDICATOR_CODE + 0x029F, bytearray([0xA9, 0x09]))                       #                         lda #$09
    rom.write_bytes(INDICATOR_CODE + 0x02A1, bytearray([0x8D, 0xFC, 0x1D]))                 #                         sta $1DFC
    rom.write_bytes(INDICATOR_CODE + 0x02A4, bytearray([0x4C, 0xCB, 0xC0]))                 #                         jmp .handle_movement
    rom.write_bytes(INDICATOR_CODE + 0x02A7, bytearray([0xEE, 0xE4, 0x18]))                 # .green_mushroom         inc $18E4
    rom.write_bytes(INDICATOR_CODE + 0x02AA, bytearray([0x4C, 0xCB, 0xC0]))                 #                         jmp .handle_movement
    rom.write_bytes(INDICATOR_CODE + 0x02AD, bytearray([0x80, 0x02]))                       # .mushroom               bra .shared_item
    rom.write_bytes(INDICATOR_CODE + 0x02AF, bytearray([0x80, 0x00]))                       # .flower                 bra .shared_item
    rom.write_bytes(INDICATOR_CODE + 0x02B1, bytearray([0xA9, 0x0B]))                       # .shared_item            lda #$0B
    rom.write_bytes(INDICATOR_CODE + 0x02B3, bytearray([0x8D, 0xFC, 0x1D]))                 #                         sta $1DFC
    rom.write_bytes(INDICATOR_CODE + 0x02B6, bytearray([0x4C, 0xCB, 0xC0]))                 #                         jmp .handle_movement

def handle_traps(rom):
    TRAPS_CODE = 0x86C00
    rom.write_bytes(0x022D8, bytearray([0x22, 0x00, 0xEC, 0x10])) # org $00A2D8 : jsl score_sprites
    rom.write_bytes(TRAPS_CODE + 0x0000, bytearray([0xAD, 0x00, 0x01]))         # handle_traps:           lda $0100
    rom.write_bytes(TRAPS_CODE + 0x0003, bytearray([0xC9, 0x14]))               #                         cmp #$14
    rom.write_bytes(TRAPS_CODE + 0x0005, bytearray([0xD0, 0x04]))               #                         bne .invalid
    rom.write_bytes(TRAPS_CODE + 0x0007, bytearray([0xA5, 0x71]))               #                         lda $71
    rom.write_bytes(TRAPS_CODE + 0x0009, bytearray([0xF0, 0x09]))               #                         beq .valid
    rom.write_bytes(TRAPS_CODE + 0x000B, bytearray([0xA9, 0xFF]))               # .invalid                lda #$FF
    rom.write_bytes(TRAPS_CODE + 0x000D, bytearray([0x8D, 0x3C, 0x0F]))         #                         sta !thwimp_index
    rom.write_bytes(TRAPS_CODE + 0x0010, bytearray([0x5C, 0xBD, 0xE2, 0x00]))   #                         jml $00E2BD
    rom.write_bytes(TRAPS_CODE + 0x0014, bytearray([0xAD, 0xB4, 0x18]))         # .valid                  lda !reverse_controls_trap
    rom.write_bytes(TRAPS_CODE + 0x0017, bytearray([0xF0, 0x03]))               #                         beq .no_reverse_controls
    rom.write_bytes(TRAPS_CODE + 0x0019, bytearray([0x20, 0x2B, 0xEC]))         #                         jsr reverse_controls_trap
    rom.write_bytes(TRAPS_CODE + 0x001C, bytearray([0xAD, 0xB7, 0x18]))         # .no_reverse_controls    lda !thwimp_trap
    rom.write_bytes(TRAPS_CODE + 0x001F, bytearray([0xF0, 0x03]))               #                         beq .no_thwimp
    rom.write_bytes(TRAPS_CODE + 0x0021, bytearray([0x20, 0x86, 0xEC]))         #                         jsr spawn_thwimp
    rom.write_bytes(TRAPS_CODE + 0x0024, bytearray([0x20, 0xCB, 0xEC]))         # .no_thwimp              jsr handle_thwimp
    rom.write_bytes(TRAPS_CODE + 0x0027, bytearray([0x5C, 0xBD, 0xE2, 0x00]))   #                         jml $00E2BD
    rom.write_bytes(TRAPS_CODE + 0x002B, bytearray([0xA5, 0x15]))               # reverse_controls_trap:  lda $15
    rom.write_bytes(TRAPS_CODE + 0x002D, bytearray([0x89, 0x03]))               #                         bit #$03
    rom.write_bytes(TRAPS_CODE + 0x002F, bytearray([0xF0, 0x04]))               #                         beq ..no_swap_hold
    rom.write_bytes(TRAPS_CODE + 0x0031, bytearray([0x49, 0x03]))               #                         eor #$03
    rom.write_bytes(TRAPS_CODE + 0x0033, bytearray([0x85, 0x15]))               #                         sta $15
    rom.write_bytes(TRAPS_CODE + 0x0035, bytearray([0xA5, 0x16]))               # ..no_swap_hold          lda $16
    rom.write_bytes(TRAPS_CODE + 0x0037, bytearray([0x89, 0x03]))               #                         bit #$03
    rom.write_bytes(TRAPS_CODE + 0x0039, bytearray([0xF0, 0x04]))               #                         beq ..no_swap_press
    rom.write_bytes(TRAPS_CODE + 0x003B, bytearray([0x49, 0x03]))               #                         eor #$03
    rom.write_bytes(TRAPS_CODE + 0x003D, bytearray([0x85, 0x16]))               #                         sta $16
    rom.write_bytes(TRAPS_CODE + 0x003F, bytearray([0xA5, 0x15]))               # .swap_up_and_down       lda $15
    rom.write_bytes(TRAPS_CODE + 0x0041, bytearray([0x89, 0x0C]))               #                         bit #$0C
    rom.write_bytes(TRAPS_CODE + 0x0043, bytearray([0xF0, 0x04]))               #                         beq .no_swap_hold
    rom.write_bytes(TRAPS_CODE + 0x0045, bytearray([0x49, 0x0C]))               #                         eor #$0C
    rom.write_bytes(TRAPS_CODE + 0x0047, bytearray([0x85, 0x15]))               #                         sta $15
    rom.write_bytes(TRAPS_CODE + 0x0049, bytearray([0xA5, 0x16]))               # .no_swap_hold           lda $16
    rom.write_bytes(TRAPS_CODE + 0x004B, bytearray([0x89, 0x0C]))               #                         bit #$0C
    rom.write_bytes(TRAPS_CODE + 0x004D, bytearray([0xF0, 0x04]))               #                         beq ..no_swap_press
    rom.write_bytes(TRAPS_CODE + 0x004F, bytearray([0x49, 0x0C]))               #                         eor #$0C
    rom.write_bytes(TRAPS_CODE + 0x0051, bytearray([0x85, 0x16]))               #                         sta $16
    rom.write_bytes(TRAPS_CODE + 0x0053, bytearray([0xA5, 0x16]))               # .swap_a_and_b           lda $16
    rom.write_bytes(TRAPS_CODE + 0x0055, bytearray([0x10, 0x0C]))               #                         bpl ..no_swap_b
    rom.write_bytes(TRAPS_CODE + 0x0057, bytearray([0x49, 0x80]))               #                         eor #$80
    rom.write_bytes(TRAPS_CODE + 0x0059, bytearray([0x85, 0x16]))               #                         sta $16
    rom.write_bytes(TRAPS_CODE + 0x005B, bytearray([0xA5, 0x18]))               #                         lda $18
    rom.write_bytes(TRAPS_CODE + 0x005D, bytearray([0x49, 0x80]))               #                         eor #$80
    rom.write_bytes(TRAPS_CODE + 0x005F, bytearray([0x85, 0x18]))               #                         sta $18
    rom.write_bytes(TRAPS_CODE + 0x0061, bytearray([0x80, 0x0E]))               #                         bra .swap_l_and_r
    rom.write_bytes(TRAPS_CODE + 0x0063, bytearray([0xA5, 0x18]))               # ..no_swap_b             lda $18
    rom.write_bytes(TRAPS_CODE + 0x0065, bytearray([0x10, 0x0A]))               #                         bpl .swap_l_and_r
    rom.write_bytes(TRAPS_CODE + 0x0067, bytearray([0x49, 0x80]))               #                         eor #$80
    rom.write_bytes(TRAPS_CODE + 0x0069, bytearray([0x85, 0x18]))               #                         sta $18
    rom.write_bytes(TRAPS_CODE + 0x006B, bytearray([0xA5, 0x16]))               #                         lda $16
    rom.write_bytes(TRAPS_CODE + 0x006D, bytearray([0x49, 0x80]))               #                         eor #$80
    rom.write_bytes(TRAPS_CODE + 0x006F, bytearray([0x85, 0x16]))               #                         sta $16
    rom.write_bytes(TRAPS_CODE + 0x0071, bytearray([0xA5, 0x17]))               # .swap_l_and_r           lda $17
    rom.write_bytes(TRAPS_CODE + 0x0073, bytearray([0x89, 0x30]))               #                         bit #$30
    rom.write_bytes(TRAPS_CODE + 0x0075, bytearray([0xF0, 0x04]))               #                         beq ..no_swap_hold
    rom.write_bytes(TRAPS_CODE + 0x0077, bytearray([0x49, 0x30]))               #                         eor #$30
    rom.write_bytes(TRAPS_CODE + 0x0079, bytearray([0x85, 0x17]))               #                         sta $17
    rom.write_bytes(TRAPS_CODE + 0x007B, bytearray([0xA5, 0x18]))               # ..no_swap_hold          lda $18
    rom.write_bytes(TRAPS_CODE + 0x007D, bytearray([0x89, 0x30]))               #                         bit #$30
    rom.write_bytes(TRAPS_CODE + 0x007F, bytearray([0xF0, 0x04]))               #                         beq ..no_swap_press
    rom.write_bytes(TRAPS_CODE + 0x0081, bytearray([0x49, 0x30]))               #                         eor #$30
    rom.write_bytes(TRAPS_CODE + 0x0083, bytearray([0x85, 0x18]))               #                         sta $18
    rom.write_bytes(TRAPS_CODE + 0x0085, bytearray([0x60]))                     # ..no_swap_press         rts
    rom.write_bytes(TRAPS_CODE + 0x0086, bytearray([0xAE, 0x3C, 0x0F]))         # spawn_thwimp:           ldx !thwimp_index
    rom.write_bytes(TRAPS_CODE + 0x0089, bytearray([0x10, 0x06]))               #                         bpl .return
    rom.write_bytes(TRAPS_CODE + 0x008B, bytearray([0x22, 0xE4, 0xA9, 0x02]))   #                         jsl $02A9E4
    rom.write_bytes(TRAPS_CODE + 0x008F, bytearray([0x10, 0x01]))               #                         bpl .found
    rom.write_bytes(TRAPS_CODE + 0x0091, bytearray([0x60]))                     # .return                 rts 
    rom.write_bytes(TRAPS_CODE + 0x0092, bytearray([0xBB]))                     # .found                  tyx 
    rom.write_bytes(TRAPS_CODE + 0x0093, bytearray([0x9C, 0xB7, 0x18]))         #                         stz !thwimp_trap
    rom.write_bytes(TRAPS_CODE + 0x0096, bytearray([0xA9, 0x10]))               #                         lda #$10
    rom.write_bytes(TRAPS_CODE + 0x0098, bytearray([0x8D, 0xF9, 0x1D]))         #                         sta $1DF9
    rom.write_bytes(TRAPS_CODE + 0x009B, bytearray([0xA9, 0x27]))               #                         lda #$27
    rom.write_bytes(TRAPS_CODE + 0x009D, bytearray([0x95, 0x9E]))               #                         sta $9E,x
    rom.write_bytes(TRAPS_CODE + 0x009F, bytearray([0xA9, 0x08]))               #                         lda #$08
    rom.write_bytes(TRAPS_CODE + 0x00A1, bytearray([0x9D, 0xC8, 0x14]))         #                         sta $14C8,x
    rom.write_bytes(TRAPS_CODE + 0x00A4, bytearray([0x22, 0xD2, 0xF7, 0x07]))   #                         jsl $07F7D2
    rom.write_bytes(TRAPS_CODE + 0x00A8, bytearray([0xA5, 0x94]))               #                         lda $94
    rom.write_bytes(TRAPS_CODE + 0x00AA, bytearray([0x95, 0xE4]))               #                         sta $E4,x
    rom.write_bytes(TRAPS_CODE + 0x00AC, bytearray([0xA5, 0x95]))               #                         lda $95
    rom.write_bytes(TRAPS_CODE + 0x00AE, bytearray([0x9D, 0xE0, 0x14]))         #                         sta $14E0,x
    rom.write_bytes(TRAPS_CODE + 0x00B1, bytearray([0xA5, 0x1C]))               #                         lda $1C
    rom.write_bytes(TRAPS_CODE + 0x00B3, bytearray([0x38]))                     #                         sec 
    rom.write_bytes(TRAPS_CODE + 0x00B4, bytearray([0xE9, 0x0F]))               #                         sbc #$0F
    rom.write_bytes(TRAPS_CODE + 0x00B6, bytearray([0x95, 0xD8]))               #                         sta $D8,x
    rom.write_bytes(TRAPS_CODE + 0x00B8, bytearray([0xA5, 0x1D]))               #                         lda $1D
    rom.write_bytes(TRAPS_CODE + 0x00BA, bytearray([0xE9, 0x00]))               #                         sbc #$00
    rom.write_bytes(TRAPS_CODE + 0x00BC, bytearray([0x9D, 0xD4, 0x14]))         #                         sta $14D4,x
    rom.write_bytes(TRAPS_CODE + 0x00BF, bytearray([0xBD, 0x86, 0x16]))         #                         lda $1686,x
    rom.write_bytes(TRAPS_CODE + 0x00C2, bytearray([0x09, 0x80]))               #                         ora #$80
    rom.write_bytes(TRAPS_CODE + 0x00C4, bytearray([0x9D, 0x86, 0x16]))         #                         sta $1686,x
    rom.write_bytes(TRAPS_CODE + 0x00C7, bytearray([0x8E, 0x3C, 0x0F]))         #                         stx !thwimp_index
    rom.write_bytes(TRAPS_CODE + 0x00CA, bytearray([0x60]))                     #                         rts 
    rom.write_bytes(TRAPS_CODE + 0x00CB, bytearray([0xAE, 0x3C, 0x0F]))         # handle_thwimp:          ldx !thwimp_index
    rom.write_bytes(TRAPS_CODE + 0x00CE, bytearray([0x30, 0x1C]))               #                         bmi .return
    rom.write_bytes(TRAPS_CODE + 0x00D0, bytearray([0xBD, 0xD4, 0x14]))         #                         lda $14D4,x
    rom.write_bytes(TRAPS_CODE + 0x00D3, bytearray([0xEB]))                     #                         xba 
    rom.write_bytes(TRAPS_CODE + 0x00D4, bytearray([0xB5, 0xD8]))               #                         lda $D8,x
    rom.write_bytes(TRAPS_CODE + 0x00D6, bytearray([0xC2, 0x20]))               #                         rep #$20
    rom.write_bytes(TRAPS_CODE + 0x00D8, bytearray([0x38]))                     #                         sec 
    rom.write_bytes(TRAPS_CODE + 0x00D9, bytearray([0xE5, 0x96]))               #                         sbc $96
    rom.write_bytes(TRAPS_CODE + 0x00DB, bytearray([0xE2, 0x20]))               #                         sep #$20
    rom.write_bytes(TRAPS_CODE + 0x00DD, bytearray([0x30, 0x0D]))               #                         bmi .return
    rom.write_bytes(TRAPS_CODE + 0x00DF, bytearray([0xA9, 0xFF]))               #                         lda #$FF
    rom.write_bytes(TRAPS_CODE + 0x00E1, bytearray([0x8D, 0x3C, 0x0F]))         #                         sta !thwimp_index
    rom.write_bytes(TRAPS_CODE + 0x00E4, bytearray([0xBD, 0x86, 0x16]))         #                         lda $1686,x
    rom.write_bytes(TRAPS_CODE + 0x00E7, bytearray([0x29, 0x7F]))               #                         and #$7F
    rom.write_bytes(TRAPS_CODE + 0x00E9, bytearray([0x9D, 0x86, 0x16]))         #                         sta $1686,x
    rom.write_bytes(TRAPS_CODE + 0x00EC, bytearray([0x60]))                     # .return                 rts 



def read_graphics_file(filename):
    return pkgutil.get_data(__name__, f"data/graphics/{filename}")

def handle_uncompressed_player_gfx(rom):
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
    SMW_COMPRESSED_PLAYER_GFX = 0x40000
    SMW_COMPRESSED_ANIMATED_GFX = 0x43FC0
    SMW_COMPRESSED_GFX_00 = 0x459F9
    SMW_COMPRESSED_GFX_10 = 0x4EF1E
    SMW_COMPRESSED_GFX_28 = 0x5C06C
    compressed_player_gfx = rom.read_bytes(SMW_COMPRESSED_PLAYER_GFX, 0x3FC0)
    compressed_animated_gfx = rom.read_bytes(SMW_COMPRESSED_ANIMATED_GFX, 0x1A39)
    compressed_gfx_00 = rom.read_bytes(SMW_COMPRESSED_GFX_00, 0x0838)
    compressed_gfx_10 = rom.read_bytes(SMW_COMPRESSED_GFX_10, 0x0891)
    compressed_gfx_28 = rom.read_bytes(SMW_COMPRESSED_GFX_28, 0x0637)
    decompressed_player_gfx = decompress_gfx(compressed_player_gfx)
    decompressed_animated_gfx = convert_3bpp(decompress_gfx(compressed_animated_gfx))
    decompressed_gfx_00 = convert_3bpp(decompress_gfx(compressed_gfx_00))
    decompressed_gfx_10 = convert_3bpp(decompress_gfx(compressed_gfx_10))
    decompressed_gfx_28 = decompress_gfx(compressed_gfx_28)

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

    rom.write_bytes(0xE0000, decompressed_player_gfx)
    rom.write_bytes(0xE8000, decompressed_animated_gfx)
    rom.write_bytes(0xE6000, player_small_tiles)
    rom.write_bytes(0xE6400, player_map_tiles)
    rom.write_bytes(0xE6C00, player_name_tiles)

    # Skip Player & Animated tile decompression
    rom.write_bytes(0x03888, bytearray([0x60])) # RTS

    # Edit Mario DMA routine
    MARIO_GFX_DMA_ADDR = 0x02300
    rom.write_bytes(MARIO_GFX_DMA_ADDR + 0x0000, bytearray([0xA2, 0x04]))             # LDX #$04
    rom.write_bytes(MARIO_GFX_DMA_ADDR + 0x0002, bytearray([0x22, 0x00, 0xF0, 0x10])) # JSL $10F000 ; upload_score_sprite_gfx
    rom.write_bytes(MARIO_GFX_DMA_ADDR + 0x0006, bytearray([0x22, 0x00, 0xF8, 0x0F])) # JSL $0FF800 ; player_code
    rom.write_bytes(MARIO_GFX_DMA_ADDR + 0x000A, bytearray([0x60]))                   # RTS

    PLAYER_UPLOAD_ADDR = 0x7F800
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0000, bytearray([0xC2, 0x20]))                     # player_code:                rep #$20
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0002, bytearray([0xAC, 0x84, 0x0D]))               #                             ldy $0D84
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0005, bytearray([0xD0, 0x03]))                     #                             bne .upload_player_palette
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0007, bytearray([0x4C, 0xD2, 0xF8]))               #                             jmp .skip_everything
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x000A, bytearray([0xA0, 0x86]))                     # .upload_player_palette      ldy #$86
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x000C, bytearray([0x8C, 0x21, 0x21]))               #                             sty $2121
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x000F, bytearray([0xA9, 0x00, 0x22]))               #                             lda #$2200
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0012, bytearray([0x8D, 0x20, 0x43]))               #                             sta $4320
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0015, bytearray([0xA8]))                           #                             tay 
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0016, bytearray([0xAD, 0x82, 0x0D]))               #                             lda $0D82
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0019, bytearray([0x8D, 0x22, 0x43]))               #                             sta $4322
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x001C, bytearray([0x8C, 0x24, 0x43]))               #                             sty $4324
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x001F, bytearray([0xA9, 0x14, 0x00]))               #                             lda #$0014
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0022, bytearray([0x8D, 0x25, 0x43]))               #                             sta $4325
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0025, bytearray([0x8E, 0x0B, 0x42]))               #                             stx $420B
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0028, bytearray([0xA0, 0x80]))                     #                             ldy #$80
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x002A, bytearray([0x8C, 0x15, 0x21]))               #                             sty $2115
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x002D, bytearray([0xA9, 0x01, 0x18]))               #                             lda #$1801
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0030, bytearray([0x8D, 0x20, 0x43]))               #                             sta $4320
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0033, bytearray([0xA0, 0x1C]))                     #                             ldy.b #player_gfx>>16
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0035, bytearray([0x8C, 0x24, 0x43]))               #                             sty $4324
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0038, bytearray([0xA9, 0x00, 0x60]))               # .upload_player_top          lda #$6000
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x003B, bytearray([0x8D, 0x16, 0x21]))               #                             sta $2116
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x003E, bytearray([0xA8]))                           #                             tay  
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x003F, bytearray([0xB9, 0x85, 0x0D]))               # -                           lda $0D85,y
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0042, bytearray([0x8D, 0x22, 0x43]))               #                             sta $4322
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0045, bytearray([0xA9, 0x40, 0x00]))               #                             lda #$0040
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0048, bytearray([0x8D, 0x25, 0x43]))               #                             sta $4325
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x004B, bytearray([0x8E, 0x0B, 0x42]))               #                             stx $420B
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x004E, bytearray([0xC8]))                           #                             iny 
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x004F, bytearray([0xC8]))                           #                             iny 
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0050, bytearray([0xC0, 0x06]))                     #                             cpy #$06
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0052, bytearray([0xD0, 0xEB]))                     #                             bne -
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0054, bytearray([0xA9, 0x00, 0x61]))               # .upload_player_bottom       lda #$6100
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0057, bytearray([0x8D, 0x16, 0x21]))               #                             sta $2116
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x005A, bytearray([0xA8]))                           #                             tay  
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x005B, bytearray([0xB9, 0x8F, 0x0D]))               # -                           lda $0D8F,y
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x005E, bytearray([0x8D, 0x22, 0x43]))               #                             sta $4322
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0061, bytearray([0xA9, 0x40, 0x00]))               #                             lda #$0040
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0064, bytearray([0x8D, 0x25, 0x43]))               #                             sta $4325
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0067, bytearray([0x8E, 0x0B, 0x42]))               #                             stx $420B
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x006A, bytearray([0xC8]))                           #                             iny 
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x006B, bytearray([0xC8]))                           #                             iny 
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x006C, bytearray([0xC0, 0x06]))                     #                             cpy #$06
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x006E, bytearray([0xD0, 0xEB]))                     #                             bne -
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0070, bytearray([0xAC, 0x9B, 0x0D]))               # .upload_player_extended     ldy $0D9B
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0073, bytearray([0xC0, 0x02]))                     #                             cpy #$02
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0075, bytearray([0xF0, 0x5B]))                     #                             beq .skip_everything
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0077, bytearray([0xA9, 0xC0, 0x60]))               #                             lda #$60C0
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x007A, bytearray([0x8D, 0x16, 0x21]))               #                             sta $2116
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x007D, bytearray([0xAD, 0x99, 0x0D]))               #                             lda $0D99
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0080, bytearray([0x8D, 0x22, 0x43]))               #                             sta $4322
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0083, bytearray([0xA9, 0x40, 0x00]))               #                             lda #$0040
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0086, bytearray([0x8D, 0x25, 0x43]))               #                             sta $4325
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0089, bytearray([0x8E, 0x0B, 0x42]))               #                             stx $420B
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x008C, bytearray([0xA0, 0x1D]))                     # .upload_misc_tiles          ldy.b #animated_tiles>>16
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x008E, bytearray([0x8C, 0x24, 0x43]))               #                             sty $4324
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0091, bytearray([0xA9, 0x60, 0x60]))               #                             lda #$6060
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0094, bytearray([0x8D, 0x16, 0x21]))               #                             sta $2116
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0097, bytearray([0xA0, 0x06]))                     #                             ldy #$06
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x0099, bytearray([0xCC, 0x84, 0x0D]))               #                             cpy $0D84
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x009C, bytearray([0xB0, 0x34]))                     #                             bcs .skip_everything
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x009E, bytearray([0xB9, 0x85, 0x0D]))               # -                           lda $0D85,y
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x00A1, bytearray([0x8D, 0x22, 0x43]))               #                             sta $4322
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x00A4, bytearray([0xA9, 0x40, 0x00]))               #                             lda #$0040
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x00A7, bytearray([0x8D, 0x25, 0x43]))               #                             sta $4325
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x00AA, bytearray([0x8E, 0x0B, 0x42]))               #                             stx $420B
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x00AD, bytearray([0xC8]))                           #                             iny 
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x00AE, bytearray([0xC8]))                           #                             iny 
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x00AF, bytearray([0xCC, 0x84, 0x0D]))               #                             cpy $0D84
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x00B2, bytearray([0x90, 0xEA]))                     #                             bcc -
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x00B4, bytearray([0xA9, 0x60, 0x61]))               #                             lda #$6160
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x00B7, bytearray([0x8D, 0x16, 0x21]))               #                             sta $2116
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x00BA, bytearray([0xA0, 0x06]))                     #                             ldy #$06
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x00BC, bytearray([0xB9, 0x8F, 0x0D]))               # -                           lda $0D8F,y
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x00BF, bytearray([0x8D, 0x22, 0x43]))               #                             sta $4322
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x00C2, bytearray([0xA9, 0x40, 0x00]))               #                             lda #$0040
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x00C5, bytearray([0x8D, 0x25, 0x43]))               #                             sta $4325
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x00C8, bytearray([0x8E, 0x0B, 0x42]))               #                             stx $420B
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x00CB, bytearray([0xC8]))                           #                             iny 
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x00CC, bytearray([0xC8]))                           #                             iny 
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x00CD, bytearray([0xCC, 0x84, 0x0D]))               #                             cpy $0D84
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x00D0, bytearray([0x90, 0xEA]))                     #                             bcc -
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x00D2, bytearray([0xE2, 0x20]))                     # .skip_everything            sep #$20
    rom.write_bytes(PLAYER_UPLOAD_ADDR + 0x00D4, bytearray([0x6B]))                           #                             rtl 

    # Obtain data for new 8x8 tile
    CHAR_TILE_CODE_ADDR = 0x05FE2
    rom.write_bytes(0x063B1, bytearray([0x20, 0xE2, 0xDF])) # jsr $DFE2
    rom.write_bytes(CHAR_TILE_CODE_ADDR + 0x0000, bytearray([0xB9, 0x1A, 0xDF])) # lda $DF1A,y
    rom.write_bytes(CHAR_TILE_CODE_ADDR + 0x0003, bytearray([0x10, 0x06]))       # bpl $06
    rom.write_bytes(CHAR_TILE_CODE_ADDR + 0x0005, bytearray([0x29, 0x7F]))       # and #$7F
    rom.write_bytes(CHAR_TILE_CODE_ADDR + 0x0007, bytearray([0x85, 0x0D]))       # sta $0D
    rom.write_bytes(CHAR_TILE_CODE_ADDR + 0x0009, bytearray([0xA9, 0x04]))       # lda #$04
    rom.write_bytes(CHAR_TILE_CODE_ADDR + 0x000B, bytearray([0x60]))             # rts

    rom.write_bytes(0x0640D, bytearray([0x20, 0xEE, 0xDF])) # jsr $DFEE
    CAPE_TILE_CODE_ADDR = 0x05FEE
    rom.write_bytes(CAPE_TILE_CODE_ADDR + 0x0000, bytearray([0xA5, 0x0D]))       # lda $0D
    rom.write_bytes(CAPE_TILE_CODE_ADDR + 0x0002, bytearray([0xE0, 0x2B]))       # cpx #$2B
    rom.write_bytes(CAPE_TILE_CODE_ADDR + 0x0004, bytearray([0x90, 0x07]))       # bcc $07
    rom.write_bytes(CAPE_TILE_CODE_ADDR + 0x0006, bytearray([0xE0, 0x40]))       # cpx #$40
    rom.write_bytes(CAPE_TILE_CODE_ADDR + 0x0008, bytearray([0xB0, 0x03]))       # bcs $03
    rom.write_bytes(CAPE_TILE_CODE_ADDR + 0x000A, bytearray([0xBD, 0xD7, 0xE1])) # lda $E1D7,x
    rom.write_bytes(CAPE_TILE_CODE_ADDR + 0x000D, bytearray([0x60]))             # rts

    # Edit Mario's 8x8 tile data
    MARIO_AUX_TILE_DATA_ADDR = 0x05F1A
    rom.write_bytes(MARIO_AUX_TILE_DATA_ADDR + 0x0000, bytearray([0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
    rom.write_bytes(MARIO_AUX_TILE_DATA_ADDR + 0x0008, bytearray([0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
    rom.write_bytes(MARIO_AUX_TILE_DATA_ADDR + 0x0010, bytearray([0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
    rom.write_bytes(MARIO_AUX_TILE_DATA_ADDR + 0x0018, bytearray([0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
    rom.write_bytes(MARIO_AUX_TILE_DATA_ADDR + 0x0020, bytearray([0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
    rom.write_bytes(MARIO_AUX_TILE_DATA_ADDR + 0x0028, bytearray([0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
    rom.write_bytes(MARIO_AUX_TILE_DATA_ADDR + 0x0030, bytearray([0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
    rom.write_bytes(MARIO_AUX_TILE_DATA_ADDR + 0x0038, bytearray([0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
    rom.write_bytes(MARIO_AUX_TILE_DATA_ADDR + 0x0040, bytearray([0x00,0x00,0x00,0x28,0x00,0x00,0x00,0x00]))
    rom.write_bytes(MARIO_AUX_TILE_DATA_ADDR + 0x0048, bytearray([0x00,0x00,0x82,0x82,0x82,0x00,0x00,0x00]))
    rom.write_bytes(MARIO_AUX_TILE_DATA_ADDR + 0x0050, bytearray([0x00,0x00,0x84,0x00,0x00,0x00,0x00,0x86]))
    rom.write_bytes(MARIO_AUX_TILE_DATA_ADDR + 0x0058, bytearray([0x86,0x86,0x00,0x00,0x88,0x88,0x8A,0x8A]))
    rom.write_bytes(MARIO_AUX_TILE_DATA_ADDR + 0x0060, bytearray([0x8C,0x8C,0x00,0x00,0x90,0x00,0x00,0x00]))
    rom.write_bytes(MARIO_AUX_TILE_DATA_ADDR + 0x0068, bytearray([0x00,0x8E,0x00,0x00,0x00,0x00,0x92,0x00]))
    rom.write_bytes(MARIO_AUX_TILE_DATA_ADDR + 0x0070, bytearray([0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
    rom.write_bytes(MARIO_AUX_TILE_DATA_ADDR + 0x0078, bytearray([0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
    rom.write_bytes(MARIO_AUX_TILE_DATA_ADDR + 0x0080, bytearray([0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x82]))
    rom.write_bytes(MARIO_AUX_TILE_DATA_ADDR + 0x0088, bytearray([0x82,0x82,0x00,0x00,0x00,0x00,0x00,0x84]))
    rom.write_bytes(MARIO_AUX_TILE_DATA_ADDR + 0x0090, bytearray([0x00,0x00,0x00,0x00,0x86,0x86,0x86,0x00]))
    rom.write_bytes(MARIO_AUX_TILE_DATA_ADDR + 0x0098, bytearray([0x00,0x88,0x88,0x8A,0x8A,0x8C,0x8C,0x00]))
    rom.write_bytes(MARIO_AUX_TILE_DATA_ADDR + 0x00A0, bytearray([0x00,0x90,0x00,0x00,0x00,0x00,0x8E,0x00]))
    rom.write_bytes(MARIO_AUX_TILE_DATA_ADDR + 0x00A8, bytearray([0x00,0x00,0x00,0x92,0x00,0x00,0x00,0x00]))
    rom.write_bytes(MARIO_AUX_TILE_DATA_ADDR + 0x00B0, bytearray([0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
    rom.write_bytes(MARIO_AUX_TILE_DATA_ADDR + 0x00B8, bytearray([0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
    
    MARIO_AUX_TILE_OFFSETS_ADDR = 0x05FDA # ends at $00E00C
    rom.write_bytes(MARIO_AUX_TILE_OFFSETS_ADDR + 0x0000, bytearray([0x00,0x02,0x80,0x80,0x00,0x02,0x0C,0x0D]))
    rom.write_bytes(MARIO_AUX_TILE_OFFSETS_ADDR + 0x0022, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x00,0x02]))
    rom.write_bytes(MARIO_AUX_TILE_OFFSETS_ADDR + 0x002A, bytearray([0x02,0x80,0x04,0x0C,0x0D,0xFF,0xFF,0xFF]))

    MARIO_AUX_CAPE_TILE_DATA_ADDR = 0x061FF
    rom.write_bytes(MARIO_AUX_CAPE_TILE_DATA_ADDR + 0x0000, bytearray([0x00,0x8C,0x14,0x14,0x2E]))
    rom.write_bytes(MARIO_AUX_CAPE_TILE_DATA_ADDR + 0x0005, bytearray([0x00,0xCA,0x16,0x16,0x2E]))
    rom.write_bytes(MARIO_AUX_CAPE_TILE_DATA_ADDR + 0x000A, bytearray([0x00,0x8E,0x18,0x18,0x2E]))
    rom.write_bytes(MARIO_AUX_CAPE_TILE_DATA_ADDR + 0x000F, bytearray([0x00,0xEB,0x1A,0x1A,0x2E]))
    rom.write_bytes(MARIO_AUX_CAPE_TILE_DATA_ADDR + 0x0014, bytearray([0x04,0xED,0x1C,0x1C]))

    # Edit player data offsets
    rom.write_bytes(0x07649, bytearray([0x69, 0x00, 0x80])) # adc #$8000
    rom.write_bytes(0x07667, bytearray([0x69, 0x00, 0x80])) # adc #$8000
    rom.write_bytes(0x0767C, bytearray([0x69, 0x00, 0x80])) # adc #$8000
    rom.write_bytes(0x07691, bytearray([0x69, 0x00, 0xE0])) # adc #$E000

    # Fix berries
    FIX_BERRIES_ADDR = 0x7FFE0
    rom.write_bytes(FIX_BERRIES_ADDR + 0x0000, bytearray([0xA0, 0x1D]))                       # fix_berries:            ldy.b #animated_tiles>>16
    rom.write_bytes(FIX_BERRIES_ADDR + 0x0002, bytearray([0x8C, 0x24, 0x43]))                 #                             sty $4324
    rom.write_bytes(FIX_BERRIES_ADDR + 0x0005, bytearray([0xAD, 0x76, 0x0D]))                 #                             lda $0D76
    rom.write_bytes(FIX_BERRIES_ADDR + 0x0008, bytearray([0x8D, 0x22, 0x43]))                 #                             sta $4322
    rom.write_bytes(FIX_BERRIES_ADDR + 0x000B, bytearray([0x6B]))                             #                             rtl 

    # Fix animated graphics
    rom.write_bytes(0x018D1, bytearray([0x1D])) # db $1D
    rom.write_bytes(0x0239E, bytearray([0x1D])) # db $1D

    rom.write_bytes(0x023F0, bytearray([0x22, 0xE0, 0xFF, 0x0F])) # jsl $0FFFE0
    rom.write_bytes(0x023F4, bytearray([0xEA]))                   # nop
    rom.write_bytes(0x023F5, bytearray([0xEA]))                   # nop
    
    rom.write_bytes(0x0E1A8, bytearray([0x69, 0x00, 0x88])) # adc #$8800
    rom.write_bytes(0x0EEB4, bytearray([0x69, 0x00, 0x88])) # adc #$8800
    rom.write_bytes(0x0EEC9, bytearray([0x69, 0x00, 0x88])) # adc #$8800
    rom.write_bytes(0x16A3E, bytearray([0x69, 0x00, 0x88])) # adc #$8800

    ANIMATED_TILE_DATA_ADDR = 0x2B999
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0000, bytearray([0x00,0x98,0x00,0x9A,0x00,0x9C,0x00,0x9E]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0008, bytearray([0x80,0x98,0x80,0x9A,0x80,0x9C,0x80,0x9E]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0010, bytearray([0x00,0x99,0x00,0x99,0x00,0x99,0x00,0x99]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0018, bytearray([0x80,0xA0,0x80,0xA2,0x80,0xA4,0x80,0xA6]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0020, bytearray([0x00,0x99,0x00,0x9B,0x00,0x9D,0x00,0x9F]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0028, bytearray([0x00,0xB0,0x80,0xB0,0x00,0xB1,0x80,0xB1]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0030, bytearray([0x20,0xAF,0x20,0xAF,0x20,0xAF,0x20,0xAF]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0038, bytearray([0x20,0xAF,0x20,0xAF,0x20,0xAF,0x20,0xAF]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0040, bytearray([0x80,0x96,0x80,0x96,0x80,0x96,0x80,0x96]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0048, bytearray([0x00,0xA7,0x80,0xA7,0x00,0xA7,0x80,0xA7]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0050, bytearray([0x20,0xAF,0x20,0xAF,0x20,0xAF,0x20,0xAF]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0058, bytearray([0x00,0xAF,0x00,0xAF,0x00,0xAF,0x00,0xAF]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0060, bytearray([0x00,0x94,0x00,0x94,0x00,0x94,0x00,0x94]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0068, bytearray([0x80,0x99,0x80,0x9B,0x80,0x9D,0x80,0x9F]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0070, bytearray([0x00,0xA0,0x00,0xA2,0x00,0xA4,0x00,0xA6]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0078, bytearray([0x80,0x91,0x80,0x93,0x80,0x95,0x80,0x97]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0080, bytearray([0x00,0x98,0x00,0x98,0x00,0x98,0x00,0x98]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0088, bytearray([0x00,0x98,0x00,0x98,0x00,0x98,0x00,0x98]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0090, bytearray([0x00,0x98,0x00,0x98,0x00,0x98,0x00,0x98]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0098, bytearray([0x00,0xA0,0x00,0xA2,0x00,0xA4,0x00,0xA6]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x00A0, bytearray([0x80,0x91,0x80,0x93,0x80,0x95,0x80,0x97]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x00A8, bytearray([0x00,0x80,0x00,0x82,0x00,0x84,0x00,0x86]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x00B0, bytearray([0x00,0x86,0x00,0x84,0x00,0x82,0x00,0x80]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x00B8, bytearray([0x00,0xA1,0x00,0xA3,0x00,0xA5,0x00,0xA3]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x00C0, bytearray([0x00,0xA0,0x00,0xA2,0x00,0xA4,0x00,0xA6]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x00C8, bytearray([0x00,0xA8,0x00,0xAA,0x00,0xAC,0x00,0xAE]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x00D0, bytearray([0x80,0xA8,0x80,0xAA,0x80,0xAC,0x80,0xAE]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x00D8, bytearray([0x80,0xAE,0x80,0xAC,0x80,0xAA,0x80,0xA8]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x00E0, bytearray([0x00,0x98,0x00,0x98,0x00,0x98,0x00,0x98]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x00E8, bytearray([0x80,0xA1,0x80,0xA3,0x80,0xA5,0x80,0xA3]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x00F0, bytearray([0x80,0x80,0x80,0x82,0x80,0x84,0x80,0x86]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x00F8, bytearray([0x00,0x81,0x00,0x83,0x00,0x85,0x00,0x87]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0100, bytearray([0x80,0x81,0x80,0x83,0x80,0x85,0x80,0x87]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0108, bytearray([0x80,0x86,0x80,0x84,0x80,0x82,0x80,0x80]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0110, bytearray([0x00,0x98,0x00,0x98,0x00,0x98,0x00,0x98]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0118, bytearray([0x80,0xA9,0x80,0xAB,0x80,0xAD,0x80,0xAB]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0120, bytearray([0x00,0x91,0x00,0x93,0x00,0x95,0x00,0x97]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0128, bytearray([0x00,0x98,0x00,0x98,0x00,0x98,0x00,0x98]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0130, bytearray([0x00,0x98,0x00,0x98,0x00,0x98,0x00,0x98]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0138, bytearray([0x80,0xA1,0x80,0xA3,0x80,0xA5,0x80,0xA3]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0140, bytearray([0x00,0xA9,0x00,0xAB,0x00,0xAD,0x00,0xAB]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0148, bytearray([0x00,0x98,0x00,0x98,0x00,0x98,0x00,0x98]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0150, bytearray([0x00,0x98,0x00,0x98,0x00,0x98,0x00,0x98]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0158, bytearray([0x00,0x98,0x00,0x98,0x00,0x98,0x00,0x98]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0160, bytearray([0x80,0x94,0x80,0x94,0x80,0x94,0x80,0x94]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0168, bytearray([0x80,0x99,0x80,0x9B,0x80,0x9D,0x80,0x9F]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0170, bytearray([0x80,0x99,0x80,0x9B,0x80,0x9D,0x80,0x9F]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0178, bytearray([0x80,0x99,0x80,0x9B,0x80,0x9D,0x80,0x9F]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0180, bytearray([0x00,0x98,0x00,0x9A,0x00,0x9C,0x00,0x9E]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0188, bytearray([0x80,0xAF,0x80,0xAF,0x80,0xAF,0x80,0xAF]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0190, bytearray([0x00,0x96,0x00,0x96,0x00,0x96,0x00,0x96]))
    rom.write_bytes(ANIMATED_TILE_DATA_ADDR + 0x0198, bytearray([0x80,0x96,0x80,0x96,0x80,0x96,0x80,0x96]))

    # Insert hand drawn graphics for in level indicators
    rom.write_bytes(0xE7000, read_graphics_file("indicators.bin"))
    # Upload indicator GFX
    UPLOAD_INDICATOR_GFX = 0x87000
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0000, bytearray([0xAD, 0x00, 0x01]))       # upload_score_sprite_gfx:    lda $0100
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0003, bytearray([0xC9, 0x13]))             #                             cmp #$13
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0005, bytearray([0xF0, 0x03]))             #                             beq .check_level
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0007, bytearray([0x4C, 0x9D, 0xF0]))       #                             jmp .check_map
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x000A, bytearray([0xA5, 0x7C]))             # .check_level                lda $7C
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x000C, bytearray([0xF0, 0x03]))             #                             beq ..perform 
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x000E, bytearray([0x4C, 0x9C, 0xF0]))       #                             jmp .skip
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0011, bytearray([0xE6, 0x7C]))             # ..perform                   inc $7C
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0013, bytearray([0xC2, 0x20]))             #                             rep #$20
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0015, bytearray([0xA0, 0x80]))             #                             ldy #$80
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0017, bytearray([0x8C, 0x15, 0x21]))       #                             sty $2115
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x001A, bytearray([0xA9, 0x01, 0x18]))       #                             lda #$1801
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x001D, bytearray([0x8D, 0x20, 0x43]))       #                             sta $4320
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0020, bytearray([0xA0, 0x1C]))             #                             ldy.b #$1C
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0022, bytearray([0x8C, 0x24, 0x43]))       #                             sty $4324
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0025, bytearray([0xA9, 0x00, 0xF0]))       #                             lda.w #$F000
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0028, bytearray([0x8D, 0x22, 0x43]))       #                             sta $4322
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x002B, bytearray([0xA9, 0xA0, 0x64]))       # .nums_01                    lda #$64A0
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x002E, bytearray([0x8D, 0x16, 0x21]))       #                             sta $2116
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0031, bytearray([0xA9, 0x40, 0x00]))       #                             lda #$0040
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0034, bytearray([0x8D, 0x25, 0x43]))       #                             sta $4325
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0037, bytearray([0x8E, 0x0B, 0x42]))       #                             stx $420B
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x003A, bytearray([0xA9, 0xA0, 0x65]))       # .nums_35                    lda #$65A0
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x003D, bytearray([0x8D, 0x16, 0x21]))       #                             sta $2116
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0040, bytearray([0xA9, 0x40, 0x00]))       #                             lda #$0040
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0043, bytearray([0x8D, 0x25, 0x43]))       #                             sta $4325
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0046, bytearray([0x8E, 0x0B, 0x42]))       #                             stx $420B
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0049, bytearray([0xA9, 0xA0, 0x61]))       # .plus_coin                  lda #$61A0
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x004C, bytearray([0x8D, 0x16, 0x21]))       #                             sta $2116
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x004F, bytearray([0xA9, 0x40, 0x00]))       #                             lda #$0040
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0052, bytearray([0x8D, 0x25, 0x43]))       #                             sta $4325
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0055, bytearray([0x8E, 0x0B, 0x42]))       #                             stx $420B
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0058, bytearray([0xA9, 0xA0, 0x60]))       # .egg_mushroom               lda #$60A0
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x005B, bytearray([0x8D, 0x16, 0x21]))       #                             sta $2116
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x005E, bytearray([0xA9, 0x40, 0x00]))       #                             lda #$0040
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0061, bytearray([0x8D, 0x25, 0x43]))       #                             sta $4325
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0064, bytearray([0x8E, 0x0B, 0x42]))       #                             stx $420B
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0067, bytearray([0xA9, 0xE0, 0x67]))       # .thwimp                     lda #$67E0
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x006A, bytearray([0x8D, 0x16, 0x21]))       #                             sta $2116
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x006D, bytearray([0xA9, 0x40, 0x00]))       #                             lda #$0040
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0070, bytearray([0x8D, 0x25, 0x43]))       #                             sta $4325
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0073, bytearray([0x8E, 0x0B, 0x42]))       #                             stx $420B
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0076, bytearray([0xA9, 0x80, 0x63]))       # .token                      lda #$6380
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0079, bytearray([0x8D, 0x16, 0x21]))       #                             sta $2116
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x007C, bytearray([0xA9, 0x20, 0x00]))       #                             lda #$0020
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x007F, bytearray([0x8D, 0x25, 0x43]))       #                             sta $4325
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0082, bytearray([0x8E, 0x0B, 0x42]))       #                             stx $420B
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0085, bytearray([0xA9, 0x00, 0xEC]))       # .layer_3                    lda #$EC00
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0088, bytearray([0x8D, 0x22, 0x43]))       #                             sta $4322
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x008B, bytearray([0xA9, 0x80, 0x41]))       #                             lda #$4180
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x008E, bytearray([0x8D, 0x16, 0x21]))       #                             sta $2116
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0091, bytearray([0xA9, 0x50, 0x00]))       #                             lda #$0050
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0094, bytearray([0x8D, 0x25, 0x43]))       #                             sta $4325
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0097, bytearray([0x8E, 0x0B, 0x42]))       #                             stx $420B
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x009A, bytearray([0xE2, 0x20]))             #                             sep #$20
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x009C, bytearray([0x6B]))                   # .skip                       rtl 
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x009D, bytearray([0xC9, 0x0E]))             # .check_map                  cmp #$0E
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x009F, bytearray([0xF0, 0x51]))             #                             beq .map_pal
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00A1, bytearray([0xC9, 0x0D]))             #                             cmp #$0D
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00A3, bytearray([0xD0, 0xF7]))             #                             bne .skip
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00A5, bytearray([0xA5, 0x7C]))             #                             lda $7C
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00A7, bytearray([0xD0, 0xF3]))             #                             bne .skip
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00A9, bytearray([0xE6, 0x7C]))             #                             inc $7C
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00AB, bytearray([0xC2, 0x20]))             #                             rep #$20
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00AD, bytearray([0xA0, 0x80]))             #                             ldy #$80
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00AF, bytearray([0x8C, 0x15, 0x21]))       #                             sty $2115
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00B2, bytearray([0xA9, 0x01, 0x18]))       #                             lda #$1801
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00B5, bytearray([0x8D, 0x20, 0x43]))       #                             sta $4320
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00B8, bytearray([0xA0, 0x1C]))             #                             ldy.b #$1C
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00BA, bytearray([0x8C, 0x24, 0x43]))       #                             sty $4324
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00BD, bytearray([0xA9, 0x00, 0xE4]))       #                             lda.w #$E400
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00C0, bytearray([0x8D, 0x22, 0x43]))       #                             sta $4322
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00C3, bytearray([0xDA]))                   #                             phx 
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00C4, bytearray([0x9B]))                   #                             txy 
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00C5, bytearray([0xA2, 0x18]))             #                             ldx.b #(.map_targets_end-.map_targets-1)*2
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00C7, bytearray([0xA9, 0x40, 0x00]))       # ..loop                      lda #$0040
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00CA, bytearray([0x8D, 0x25, 0x43]))       #                             sta $4325
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00CD, bytearray([0xBF, 0x80, 0xFF, 0x10])) #                             lda.l .map_targets,x
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00D1, bytearray([0x8D, 0x16, 0x21]))       #                             sta $2116
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00D4, bytearray([0x8C, 0x0B, 0x42]))       #                             sty $420B
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00D7, bytearray([0xBF, 0x80, 0xFF, 0x10])) #                             lda.l .map_targets,x
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00DB, bytearray([0x18]))                   #                             clc 
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00DC, bytearray([0x69, 0x00, 0x01]))       #                             adc #$0100
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00DF, bytearray([0x8D, 0x16, 0x21]))       #                             sta $2116
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00E2, bytearray([0xA9, 0x40, 0x00]))       #                             lda #$0040
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00E5, bytearray([0x8D, 0x25, 0x43]))       #                             sta $4325
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00E8, bytearray([0x8C, 0x0B, 0x42]))       #                             sty $420B
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00EB, bytearray([0xCA]))                   #                             dex 
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00EC, bytearray([0xCA]))                   #                             dex 
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00ED, bytearray([0x10, 0xD8]))             #                             bpl .loop
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00EF, bytearray([0xFA]))                   #                             plx 
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00F0, bytearray([0xE2, 0x20]))             #                             sep #$20
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00F2, bytearray([0xA9, 0xA3]))             # .map_pal                    lda #$A3
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00F4, bytearray([0x8D, 0x21, 0x21]))       #                             sta $2121
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00F7, bytearray([0xAF, 0x9C, 0xB5, 0x00])) #                             lda $00B59C
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00FB, bytearray([0x8D, 0x22, 0x21]))       #                             sta $2122
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x00FE, bytearray([0xAF, 0x9D, 0xB5, 0x00])) #                             lda $00B59D
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0102, bytearray([0x8D, 0x22, 0x21]))       #                             sta $2122
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0105, bytearray([0xAF, 0x9E, 0xB5, 0x00])) #                             lda $00B59E
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0109, bytearray([0x8D, 0x22, 0x21]))       #                             sta $2122
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x010C, bytearray([0xAF, 0x9F, 0xB5, 0x00])) #                             lda $00B59F
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0110, bytearray([0x8D, 0x22, 0x21]))       #                             sta $2122
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0113, bytearray([0xAF, 0xA0, 0xB5, 0x00])) #                             lda $00B5A0
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0117, bytearray([0x8D, 0x22, 0x21]))       #                             sta $2122
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x011A, bytearray([0xAF, 0xA1, 0xB5, 0x00])) #                             lda $00B5A1
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x011E, bytearray([0x8D, 0x22, 0x21]))       #                             sta $2122
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0121, bytearray([0xAF, 0xA2, 0xB5, 0x00])) #                             lda $00B5A2
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0125, bytearray([0x8D, 0x22, 0x21]))       #                             sta $2122
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0128, bytearray([0xAF, 0xA3, 0xB5, 0x00])) #                             lda $00B5A3
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x012C, bytearray([0x8D, 0x22, 0x21]))       #                             sta $2122
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x012F, bytearray([0xAF, 0xA4, 0xB5, 0x00])) #                             lda $00B5A4
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0133, bytearray([0x8D, 0x22, 0x21]))       #                             sta $2122
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x0136, bytearray([0xAF, 0xA5, 0xB5, 0x00])) #                             lda $00B5A5
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x013A, bytearray([0x8D, 0x22, 0x21]))       #                             sta $2122
    rom.write_bytes(UPLOAD_INDICATOR_GFX + 0x013D, bytearray([0x6B]))                   #                             rtl 

    vram_targets = bytearray([
        0x20,0x64, 0x00,0x64, 0xE0,0x62,
        0x60,0x66, 0x40,0x66,
        0x60,0x64,
        0x40,0x62, 0x00,0x62,
        0xE0,0x60, 0xC0,0x60, 0xA0,0x60, 0x80,0x60, 0x60,0x60
    ])
    rom.write_bytes(0x87F80, vram_targets)


def handle_chocolate_island_2(rom):
    FIX_CHOCOISLAND2_ADDR = 0x87200
    rom.write_bytes(0x2DB3E, bytearray([0x5C, 0x00, 0xF2, 0x10])) # jml fix_choco_island_2
    rom.write_bytes(FIX_CHOCOISLAND2_ADDR + 0x0000, bytearray([0xAD, 0x33, 0x1F]))        # fix_choco_island_2  lda $1F2F+$04
    rom.write_bytes(FIX_CHOCOISLAND2_ADDR + 0x0003, bytearray([0x29, 0x08]))              #                     and #$08
    rom.write_bytes(FIX_CHOCOISLAND2_ADDR + 0x0005, bytearray([0xD0, 0x0D]))              #                     bne .dc_room
    rom.write_bytes(FIX_CHOCOISLAND2_ADDR + 0x0007, bytearray([0xAD, 0x22, 0x14]))        #                     lda $1422
    rom.write_bytes(FIX_CHOCOISLAND2_ADDR + 0x000A, bytearray([0xC9, 0x04]))              #                     cmp #$04
    rom.write_bytes(FIX_CHOCOISLAND2_ADDR + 0x000C, bytearray([0xF0, 0x06]))              #                     beq .dc_room
    rom.write_bytes(FIX_CHOCOISLAND2_ADDR + 0x000E, bytearray([0xA2, 0x02]))              # .rex_room           ldx #$02
    rom.write_bytes(FIX_CHOCOISLAND2_ADDR + 0x0010, bytearray([0x5C, 0x49, 0xDB, 0x05]))  #                     jml $05DB49
    rom.write_bytes(FIX_CHOCOISLAND2_ADDR + 0x0014, bytearray([0xA2, 0x00]))              # .dc_room            ldx #$00
    rom.write_bytes(FIX_CHOCOISLAND2_ADDR + 0x0016, bytearray([0x5C, 0x49, 0xDB, 0x05]))  #                     jml $05DB49


def decompress_gfx(compressed_graphics):
    # This code decompresses graphics in LC_LZ2 format in order to be able to swap player and yoshi's graphics with ease.
    decompressed_gfx = bytearray([])
    i = 0
    while True:
        cmd = compressed_graphics[i]
        i += 1
        if cmd == 0xFF:
            break
        else:
            if (cmd >> 5) == 0x07:
                size = ((cmd & 0x03) << 8) + compressed_graphics[i] + 1
                cmd = (cmd & 0x1C) >> 2
                i += 1
            else:
                size = (cmd & 0x1F) + 1
                cmd = cmd >> 5
            if cmd == 0x00:
                decompressed_gfx += bytearray([compressed_graphics[i+j] for j in range(size)])
                i += size
            elif cmd == 0x01:
                byte_fill = compressed_graphics[i]
                i += 1
                decompressed_gfx += bytearray([byte_fill for j in range(size)])
            elif cmd == 0x02:
                byte_fill_1 = compressed_graphics[i]
                i += 1
                byte_fill_2 = compressed_graphics[i]
                i += 1
                for j in range(size):
                    if (j & 0x1) == 0x00:
                        decompressed_gfx += bytearray([byte_fill_1])
                    else:
                        decompressed_gfx += bytearray([byte_fill_2])
            elif cmd == 0x03:
                byte_read = compressed_graphics[i]
                i += 1
                decompressed_gfx += bytearray([(byte_read + j) for j in range(size)])
            elif cmd == 0x04:
                position = (compressed_graphics[i] << 8) + compressed_graphics[i+1]
                i += 2
                for j in range(size):
                    copy_byte = decompressed_gfx[position+j]
                    decompressed_gfx += bytearray([copy_byte])
    return decompressed_gfx


def convert_3bpp(decompressed_gfx):
    i = 0
    converted_gfx = bytearray([])
    while i < len(decompressed_gfx):
        converted_gfx += bytearray([decompressed_gfx[i+j] for j in range(16)])
        i += 16
        for j in range(8):
            converted_gfx += bytearray([decompressed_gfx[i]])
            converted_gfx += bytearray([0x00])
            i += 1
    return converted_gfx


def copy_gfx_tiles(original, order, size):
    result = bytearray([])
    for x in range(len(order)):
        z = order[x] << size[0]
        result += bytearray([original[z+y] for y in range(size[1])])
    return result


def file_to_bytes(filename):  
    return open(os.path.dirname(__file__)+filename, "rb").read()
   

def handle_music_shuffle(rom, world: World):
    from .Aesthetics import generate_shuffled_level_music, generate_shuffled_ow_music, level_music_address_data, ow_music_address_data

    shuffled_level_music = generate_shuffled_level_music(world)
    for i in range(len(shuffled_level_music)):
        rom.write_byte(level_music_address_data[i], shuffled_level_music[i])

    shuffled_ow_music = generate_shuffled_ow_music(world)
    for i in range(len(shuffled_ow_music)):
        for addr in ow_music_address_data[i]:
            rom.write_byte(addr, shuffled_ow_music[i])


def handle_mario_palette(rom, world: World):
    from .Aesthetics import mario_palettes, fire_mario_palettes, ow_mario_palettes

    chosen_palette = world.options.mario_palette.value

    rom.write_bytes(0x32C8, bytes(mario_palettes[chosen_palette]))
    rom.write_bytes(0x32F0, bytes(fire_mario_palettes[chosen_palette]))
    rom.write_bytes(0x359C, bytes(ow_mario_palettes[chosen_palette]))


def handle_swap_donut_gh_exits(rom):
    rom.write_bytes(0x2567C, bytes([0xC0]))
    rom.write_bytes(0x25873, bytes([0xA9]))
    rom.write_bytes(0x25875, bytes([0x85]))
    rom.write_bytes(0x25954, bytes([0x92]))
    rom.write_bytes(0x25956, bytes([0x0A]))
    rom.write_bytes(0x25E31, bytes([0x00, 0x00, 0xD8, 0x04, 0x24, 0x00, 0x98, 0x04, 0x48, 0x00, 0xD8, 0x03, 0x6C, 0x00, 0x56, 0x03,
                                    0x90, 0x00, 0x56, 0x03, 0xB4, 0x00, 0x56, 0x03, 0x10, 0x05, 0x18, 0x05, 0x28, 0x09, 0x24, 0x05,
                                    0x38, 0x0B, 0x14, 0x07, 0xEC, 0x09, 0x12, 0x05, 0xF0, 0x09, 0xD2, 0x04, 0xF4, 0x09, 0x92, 0x04]))
    rom.write_bytes(0x26371, bytes([0x32]))


def handle_bowser_rooms(rom, world: World):
    if world.options.bowser_castle_rooms == "random_two_room":
        chosen_rooms = world.random.sample(standard_bowser_rooms, 2)

        rom.write_byte(0x3A680, chosen_rooms[0].roomID)
        rom.write_byte(0x3A684, chosen_rooms[0].roomID)
        rom.write_byte(0x3A688, chosen_rooms[0].roomID)
        rom.write_byte(0x3A68C, chosen_rooms[0].roomID)

        for i in range(1, len(chosen_rooms)):
            rom.write_byte(chosen_rooms[i-1].exitAddress, chosen_rooms[i].roomID)

        rom.write_byte(chosen_rooms[len(chosen_rooms)-1].exitAddress, 0xBD)

    elif world.options.bowser_castle_rooms == "random_five_room":
        chosen_rooms = world.random.sample(standard_bowser_rooms, 5)

        rom.write_byte(0x3A680, chosen_rooms[0].roomID)
        rom.write_byte(0x3A684, chosen_rooms[0].roomID)
        rom.write_byte(0x3A688, chosen_rooms[0].roomID)
        rom.write_byte(0x3A68C, chosen_rooms[0].roomID)

        for i in range(1, len(chosen_rooms)):
            rom.write_byte(chosen_rooms[i-1].exitAddress, chosen_rooms[i].roomID)

        rom.write_byte(chosen_rooms[len(chosen_rooms)-1].exitAddress, 0xBD)

    elif world.options.bowser_castle_rooms == "gauntlet":
        chosen_rooms = standard_bowser_rooms.copy()
        world.random.shuffle(chosen_rooms)

        rom.write_byte(0x3A680, chosen_rooms[0].roomID)
        rom.write_byte(0x3A684, chosen_rooms[0].roomID)
        rom.write_byte(0x3A688, chosen_rooms[0].roomID)
        rom.write_byte(0x3A68C, chosen_rooms[0].roomID)

        for i in range(1, len(chosen_rooms)):
            rom.write_byte(chosen_rooms[i-1].exitAddress, chosen_rooms[i].roomID)

        rom.write_byte(chosen_rooms[len(chosen_rooms)-1].exitAddress, 0xBD)
    elif world.options.bowser_castle_rooms == "labyrinth":
        bowser_rooms_copy = full_bowser_rooms.copy()

        entrance_point = bowser_rooms_copy.pop(0)

        world.random.shuffle(bowser_rooms_copy)

        rom.write_byte(entrance_point.exitAddress, bowser_rooms_copy[0].roomID)
        for i in range(0, len(bowser_rooms_copy) - 1):
            rom.write_byte(bowser_rooms_copy[i].exitAddress, bowser_rooms_copy[i+1].roomID)

        rom.write_byte(bowser_rooms_copy[len(bowser_rooms_copy)-1].exitAddress, 0xBD)


def handle_boss_shuffle(rom, world: World):
    if world.options.boss_shuffle == "simple":
        submap_boss_rooms_copy = submap_boss_rooms.copy()
        ow_boss_rooms_copy = ow_boss_rooms.copy()

        world.random.shuffle(submap_boss_rooms_copy)
        world.random.shuffle(ow_boss_rooms_copy)

        for i in range(len(submap_boss_rooms_copy)):
            rom.write_byte(submap_boss_rooms[i].exitAddress, submap_boss_rooms_copy[i].roomID)

        for i in range(len(ow_boss_rooms_copy)):
            rom.write_byte(ow_boss_rooms[i].exitAddress, ow_boss_rooms_copy[i].roomID)

            if ow_boss_rooms[i].exitAddressAlt is not None:
                rom.write_byte(ow_boss_rooms[i].exitAddressAlt, ow_boss_rooms_copy[i].roomID)

    elif world.options.boss_shuffle == "full":
        for i in range(len(submap_boss_rooms)):
            chosen_boss = world.random.choice(submap_boss_rooms)
            rom.write_byte(submap_boss_rooms[i].exitAddress, chosen_boss.roomID)

        for i in range(len(ow_boss_rooms)):
            chosen_boss = world.random.choice(ow_boss_rooms)
            rom.write_byte(ow_boss_rooms[i].exitAddress, chosen_boss.roomID)

            if ow_boss_rooms[i].exitAddressAlt is not None:
                rom.write_byte(ow_boss_rooms[i].exitAddressAlt, chosen_boss.roomID)

    elif world.options.boss_shuffle == "singularity":
        chosen_submap_boss = world.random.choice(submap_boss_rooms)
        chosen_ow_boss = world.random.choice(ow_boss_rooms)

        for i in range(len(submap_boss_rooms)):
            rom.write_byte(submap_boss_rooms[i].exitAddress, chosen_submap_boss.roomID)

        for i in range(len(ow_boss_rooms)):
            rom.write_byte(ow_boss_rooms[i].exitAddress, chosen_ow_boss.roomID)

            if ow_boss_rooms[i].exitAddressAlt is not None:
                rom.write_byte(ow_boss_rooms[i].exitAddressAlt, chosen_ow_boss.roomID)


def patch_rom(world: World, rom, player, active_level_dict):
    goal_text = generate_goal_text(world)

    rom.write_bytes(0x2A6E2, goal_text)
    rom.write_byte(0x2B1D8, 0x80)

    intro_text = generate_text_box("Bowser has stolen all of Mario's abilities. Can you help Mario travel across Dinosaur land to get them back and save the Princess from him?")
    rom.write_bytes(0x2A5D9, intro_text)

    handle_bowser_rooms(rom, world)
    handle_boss_shuffle(rom, world)

    # Handle ROM expansion
    rom.write_bytes(0x07FD7, bytearray([0x0A]))
    rom.write_bytes(0x80000, bytearray([0x00 for _ in range(0x80000)]))

    # Prevent Title Screen Deaths
    rom.write_byte(0x1C6A, 0x80)

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

    rom.write_bytes(0x2B7F1, player_name_bytes) # MARIO A
    rom.write_bytes(0x2B726, player_name_bytes) # MARIO A

    rom.write_bytes(0x2B815, bytearray([0xFC, 0x38] * 0x10)) # MARIO B
    rom.write_bytes(0x2B74A, bytearray([0xFC, 0x38] * 0x10)) # MARIO B
    rom.write_bytes(0x2B839, bytearray([0x71, 0x31, 0x74, 0x31, 0x2D, 0x31, 0x84, 0x30,
                                        0x82, 0x30, 0x6F, 0x31, 0x73, 0x31, 0x70, 0x31,
                                        0x71, 0x31, 0x75, 0x31, 0x83, 0x30, 0xFC, 0x38,
                                        0xFC, 0x38, 0xFC, 0x38, 0xFC, 0x38, 0xFC, 0x38])) # MARIO C
    rom.write_bytes(0x2B76E, bytearray([0xFC, 0x38] * 0x10)) # MARIO C
    rom.write_bytes(0x2B79E, bytearray([0xFC, 0x38] * 0x05)) # EMPTY
    rom.write_bytes(0x2B7AE, bytearray([0xFC, 0x38] * 0x05)) # EMPTY
    rom.write_bytes(0x2B8A8, bytearray([0xFC, 0x38] * 0x0D)) # 2 PLAYER GAME

    rom.write_bytes(0x2B85D, bytearray([0xFC, 0x38] * 0x0A)) # ERASE

    rom.write_bytes(0x2B88E, bytearray([0x2C, 0x31, 0x73, 0x31, 0x75, 0x31, 0x82, 0x30, 0x30, 0x31, 0xFC, 0x38, 0x31, 0x31, 0x73, 0x31,
                                        0x73, 0x31, 0x7C, 0x30, 0xFC, 0x38, 0xFC, 0x38, 0xFC, 0x38])) # 1 Player Game

    rom.write_bytes(0x2B6D7, bytearray([0x16, 0x38, 0x18, 0x38, 0x0D, 0x38, 0xFC, 0x38, 0x0B, 0x38, 0x22, 0x38,
                                        0xFC, 0x38, 0x19, 0x38, 0x18, 0x38, 0x1B, 0x38, 0x22, 0x38, 0x10, 0x38, 0x18, 0x38, 0x17, 0x38,
                                        0x0E, 0x38, 0xFC, 0x38, 0x15, 0x38, 0x21, 0x38, 0x05, 0x38])) # Mod by PoryGone + lx5

    # Title Options
    rom.write_bytes(0x1E6A, bytearray([0x01]))
    rom.write_bytes(0x1E6C, bytearray([0x01]))
    rom.write_bytes(0x1E6E, bytearray([0x01]))

    # Save current level number to RAM (not translevel)
    rom.write_bytes(0x2D8B9, bytearray([0x20, 0x46, 0xDC]))             # org $05D8B9 : jsr level_num
    rom.write_bytes(0x2DC46 + 0x0000, bytearray([0xA5, 0x0E]))          # level_num:    lda $0E
    rom.write_bytes(0x2DC46 + 0x0002, bytearray([0x8D, 0x0B, 0x01]))    #               sta $010B
    rom.write_bytes(0x2DC46 + 0x0005, bytearray([0x0A]))                #               asl 
    rom.write_bytes(0x2DC46 + 0x0006, bytearray([0x60]))                #               rts 

    # Always allow Start+Select
    rom.write_bytes(0x2267, bytearray([0xEA, 0xEA]))

    # Always bring up save prompt on beating a level
    if world.options.autosave:
        rom.write_bytes(0x20F93, bytearray([0x00]))

    if world.options.overworld_speed == "fast":
        rom.write_bytes(0x21414, bytearray([0x20, 0x10]))
    elif world.options.overworld_speed == "slow":
        rom.write_bytes(0x21414, bytearray([0x05, 0x05]))

    # Starting Life Count
    rom.write_bytes(0x1E25, bytearray([world.options.starting_life_count.value - 1]))

    # Repurpose Bonus Stars counter for Boss Token or Yoshi Eggs
    rom.write_bytes(0x3F1AA, bytearray([0x00] * 0x20))

    # Make bonus star counter go up to 255 (999 in theory, but can't load a 16-bit addr there)
    rom.write_bytes(0x00F5B, bytearray([0x4C, 0x73, 0x8F]))
    rom.write_byte(0x00F95, 0x08)
    rom.write_byte(0x00F97, 0x0C)
    rom.write_byte(0x00FAC, 0x02)
    rom.write_byte(0x00F9E, 0x1D)
    rom.write_byte(0x00FA5, 0x1D)
    rom.write_byte(0x00FA8, 0x02)
    rom.write_byte(0x00FB0, 0x1D)
    rom.write_byte(0x00FB8, 0x02)
    rom.write_byte(0x00FBE, 0x1D)
    rom.write_byte(0x00FC2, 0x03)

    # Move Dragon coins one spot to the left & fix tilemap
    rom.write_byte(0x00FF0, 0xFE)
    rom.write_byte(0x00C94, 0x3C)
    rom.write_byte(0x00C9C, 0x38)

     # Delete Routine that would copy Mario position data over repurposed Luigi save data
    rom.write_bytes(0x20F9F, bytearray([0xEA] * 0x3D))

    # Prevent Switch Palaces setting the Switch Palace flags
    rom.write_bytes(0x6EC9A, bytearray([0xEA, 0xEA]))
    rom.write_bytes(0x6EB1, bytearray([0xEA, 0xEA]))
    rom.write_bytes(0x6EB4, bytearray([0xEA, 0xEA, 0xEA]))

    # Move Thwimps tilemap to another spot in VRAM in order to make them global
    rom.write_bytes(0x09C13, bytearray([0x7E, 0x7E, 0x7F, 0x7F]))
    rom.write_byte(0x3F425, 0x32)

    handle_chocolate_island_2(rom)

    handle_ability_code(rom)

    handle_yoshi_box(rom)
    handle_bowser_damage(rom)

    handle_collected_paths(rom)

    handle_vertical_scroll(rom)

    handle_ram(rom)
    handle_bonus_block(rom)
    handle_blocksanity(rom)

    handle_uncompressed_player_gfx(rom)
    
    # Handle Special Zone Clear flag
    rom.write_bytes(0x02A74, bytearray([0x1E, 0x1F]))
    rom.write_bytes(0x09826, bytearray([0x1E, 0x1F]))
    rom.write_bytes(0x0B9CD, bytearray([0x1E, 0x1F]))
    rom.write_bytes(0x12986, bytearray([0x1E, 0x1F]))
    rom.write_bytes(0x62E0F, bytearray([0x1E, 0x1F]))

    handle_indicators(rom)
    handle_map_indicators(rom)

    # Handle extra traps
    handle_traps(rom)

    # Mario Start! -> Player Start!
    text_data_top_tiles = bytearray([
        0x00,0xFF,0x4D,0x4C,0x03,0x4D,0x5D,0xFF,0x4C,0x4B,
        0x4A,0x03,0x4E,0x01,0x00,0x02,0x00,0x4a,0x4E,0xFF
    ])
    text_data_top_props = bytearray([
        0x34,0x30,0x34,0x34,0x34,0x34,0x34,0x30,0x34,0x34,
        0x34,0x34,0x34,0x34,0x34,0x34,0x34,0x34,0x34,0x30
    ])
    text_data_bottom_tiles = bytearray([
        0x10,0xFF,0x00,0x5C,0x13,0x00,0x5D,0xFF,0x5C,0x5B,
        0x00,0x13,0x5E,0x11,0x00,0x12,0x00,0x03,0x5E,0xFF
    ])
    text_data_bottom_props = bytearray([
        0x34,0x30,0xb4,0x34,0x34,0xb4,0xf4,0x30,0x34,0x34,
        0xB4,0x34,0x34,0x34,0xb4,0x34,0xb4,0xb4,0x34,0x30
    ])

    rom.write_bytes(0x010D1, text_data_top_tiles)
    rom.write_bytes(0x01139, text_data_top_props)
    rom.write_bytes(0x01105, text_data_bottom_tiles)
    rom.write_bytes(0x0116A, text_data_bottom_props)

    # Handle Level Shuffle
    handle_level_shuffle(rom, active_level_dict)

    # Handle Music Shuffle
    if world.options.music_shuffle != "none":
        handle_music_shuffle(rom, world)

    generate_shuffled_ow_palettes(rom, world)

    generate_shuffled_header_data(rom, world)

    if world.options.level_palette_shuffle == "on_curated":
        generate_curated_level_palette_data(rom, world)

    if world.options.overworld_palette_shuffle == "on_curated":
        generate_curated_map_palette_data(rom, world)
    
    if world.options.sfx_shuffle != "none":
        generate_shuffled_sfx(rom, world)
    
    if world.options.swap_donut_gh_exits:
        handle_swap_donut_gh_exits(rom)

    handle_mario_palette(rom, world)

    # Store all relevant option results in ROM
    rom.write_byte(0x01BFA0, world.options.goal.value)
    if world.options.goal.value == 0:
        rom.write_byte(0x01BFA1, world.options.bosses_required.value)
    else:
        rom.write_byte(0x01BFA1, 0x7F)
    required_yoshi_eggs = world.required_egg_count
    rom.write_byte(0x01BFA2, required_yoshi_eggs)
    #rom.write_byte(0x01BFA3, world.options.display_sent_item_popups.value)
    rom.write_byte(0x01BFA4, world.options.display_received_item_popups.value)
    rom.write_byte(0x01BFA5, world.options.death_link.value)
    rom.write_byte(0x01BFA6, world.options.dragon_coin_checks.value)
    rom.write_byte(0x01BFA7, world.options.swap_donut_gh_exits.value)
    rom.write_byte(0x01BFA8, world.options.moon_checks.value)
    rom.write_byte(0x01BFA9, world.options.hidden_1up_checks.value)
    rom.write_byte(0x01BFAA, world.options.bonus_block_checks.value)
    rom.write_byte(0x01BFAB, world.options.blocksanity.value)
    rom.write_byte(0x01BFB7, world.options.trap_link.value)
    rom.write_byte(0x01BFB8, world.options.ring_link.value)


    from Utils import __version__
    rom.name = bytearray(f'SMW{__version__.replace(".", "")[0:3]}_{player}_{world.multiworld.seed:11}\0', 'utf8')[:21]
    rom.name.extend([0] * (21 - len(rom.name)))
    rom.write_bytes(0x7FC0, rom.name)

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
    options = Utils.get_options()
    if not file_name:
        file_name = options["smw_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
