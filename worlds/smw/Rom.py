import Utils
from worlds.Files import APDeltaPatch
from .Aesthetics import generate_shuffled_header_data, generate_shuffled_ow_palettes
from .Levels import level_info_dict, full_bowser_rooms, standard_bowser_rooms, submap_boss_rooms, ow_boss_rooms
from .Names.TextBox import generate_goal_text, title_text_mapping, generate_text_box

USHASH = 'cdd3c8c37322978ca8669b34bc89c804'
ROM_PLAYER_LIMIT = 65535

import hashlib
import os
import math


ability_rom_data = {
    0xBC0003: [[0x1F2C, 0x7]], # Run         0x80
    0xBC0004: [[0x1F2C, 0x6]], # Carry       0x40
    0xBC0005: [[0x1F2C, 0x2]], # Swim        0x04
    0xBC0006: [[0x1F2C, 0x3]], # Spin Jump   0x08
    0xBC0007: [[0x1F2C, 0x5]], # Climb       0x20
    0xBC0008: [[0x1F2C, 0x1]], # Yoshi       0x02
    0xBC0009: [[0x1F2C, 0x4]], # P-Switch    0x10
    #0xBC000A: [[]]
    0xBC000B: [[0x1F2D, 0x3]], # P-Balloon   0x08
    0xBC000D: [[0x1F2D, 0x4]], # Super Star  0x10
}


item_rom_data = {
    0xBC0001: [0x18E4, 0x1], # 1-Up Mushroom

    0xBC0002: [0x1F24, 0x1, 0x1F], # Yoshi Egg
    0xBC0012: [0x1F26, 0x1, 0x09], # Boss Token

    0xBC000E: [0x1F28, 0x1, 0x1C], # Yellow Switch Palace
    0xBC000F: [0x1F27, 0x1, 0x1C], # Green Switch Palace
    0xBC0010: [0x1F2A, 0x1, 0x1C], # Red Switch Palace
    0xBC0011: [0x1F29, 0x1, 0x1C], # Blue Switch Palace
}

trap_rom_data = {
    0xBC0013: [0x0086, 0x1, 0x0E], # Ice Trap
    0xBC0014: [0x18BD, 0x7F, 0x18], # Stun Trap
    0xBC0016: [0x0F31, 0x1], # Timer Trap
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

    def read_bytes(self, startaddress: int, length: int) -> bytes:
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
    rom.write_bytes(RUN_SUB_ADDR + 0x08, bytearray([0xAD, 0x2C, 0x1F])) # LDA $1F2C
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
    rom.write_bytes(PURPLE_BLOCK_CARRY_SUB_ADDR + 0x01, bytearray([0xAD, 0x2C, 0x1F])) # LDA $1F2C
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
    rom.write_bytes(SPRINGBOARD_CARRY_SUB_ADDR + 0x02, bytearray([0xAD, 0x2C, 0x1F])) # LDA $1F2C
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
    rom.write_bytes(0xAA66, bytearray([0xAD, 0x2C, 0x1F]))       # LDA $1F2C
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
    rom.write_bytes(YOSHI_CARRY_SUB_ADDR + 0x01, bytearray([0xAD, 0x2C, 0x1F])) # LDA $1F2C
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
    rom.write_bytes(CLIMB_SUB_ADDR + 0x01, bytearray([0xAD, 0x2C, 0x1F]))       # LDA $1F2C
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
    rom.write_bytes(CLIMB_ROPE_SUB_ADDR + 0x01, bytearray([0xAD, 0x2C, 0x1F])) # LDA $1F2C
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
    rom.write_bytes(P_SWITCH_SUB_ADDR + 0x01, bytearray([0xAD, 0x2C, 0x1F])) # LDA $1F2C
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
    rom.write_bytes(0x5645, bytearray([0xAD, 0x2C, 0x1F]))       # LDA $1F2C
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
    rom.write_bytes(SPIN_JUMP_WATER_SUB_ADDR + 0x01, bytearray([0xAD, 0x2C, 0x1F])) # LDA $1F2C
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
    rom.write_bytes(SPIN_JUMP_SPRING_SUB_ADDR + 0x01, bytearray([0xAD, 0x2C, 0x1F])) # LDA $1F2C
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
    rom.write_bytes(SWIM_SUB_ADDR + 0x02, bytearray([0xAD, 0x2C, 0x1F])) # LDA $1F2C
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
    rom.write_bytes(SWIM_SUB_ADDR + 0x02, bytearray([0xAD, 0x2C, 0x1F])) # LDA $1F2C
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
    rom.write_bytes(YOSHI_SUB_ADDR + 0x01, bytearray([0xAD, 0x2C, 0x1F])) # LDA $1F2C
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
    rom.write_bytes(YOSHI_SUB_ADDR + 0x04, bytearray([0xAD, 0x2C, 0x1F])) # LDA $1F2C
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

    rom.write_bytes(0x1A509, bytearray([0x20, 0x50, 0xBC])) # JSR $03BC50

    BOWSER_BALLS_SUB_ADDR = 0x01BC50
    rom.write_bytes(BOWSER_BALLS_SUB_ADDR + 0x00, bytearray([0x08]))                   # PHP
    rom.write_bytes(BOWSER_BALLS_SUB_ADDR + 0x01, bytearray([0xAD, 0x48, 0x0F]))       # LDA $F48
    rom.write_bytes(BOWSER_BALLS_SUB_ADDR + 0x04, bytearray([0xCF, 0xA1, 0xBF, 0x03])) # CMP $03BFA1
    rom.write_bytes(BOWSER_BALLS_SUB_ADDR + 0x08, bytearray([0x90, 0x06]))             # BCC +0x06
    rom.write_bytes(BOWSER_BALLS_SUB_ADDR + 0x0A, bytearray([0x28]))                   # PLP
    rom.write_bytes(BOWSER_BALLS_SUB_ADDR + 0x0B, bytearray([0xEE, 0xB8, 0x14]))       # INC $14B8
    rom.write_bytes(BOWSER_BALLS_SUB_ADDR + 0x0E, bytearray([0x80, 0x01]))             # BRA +0x01
    rom.write_bytes(BOWSER_BALLS_SUB_ADDR + 0x10, bytearray([0x28]))                   # PLP
    rom.write_bytes(BOWSER_BALLS_SUB_ADDR + 0x11, bytearray([0x60]))                   # RTS

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
    rom.write_bytes(0x285BA, bytearray([0x22, 0x90, 0xBC, 0x03])) # JSL $03BC90

    VERTICAL_SCROLL_SUB_ADDR = 0x01BC90
    rom.write_bytes(VERTICAL_SCROLL_SUB_ADDR + 0x00, bytearray([0x4A]))       # LSR
    rom.write_bytes(VERTICAL_SCROLL_SUB_ADDR + 0x01, bytearray([0x4A]))       # LSR
    rom.write_bytes(VERTICAL_SCROLL_SUB_ADDR + 0x02, bytearray([0x4A]))       # LSR
    rom.write_bytes(VERTICAL_SCROLL_SUB_ADDR + 0x03, bytearray([0x4A]))       # LSR
    rom.write_bytes(VERTICAL_SCROLL_SUB_ADDR + 0x04, bytearray([0x08]))       # PHP
    rom.write_bytes(VERTICAL_SCROLL_SUB_ADDR + 0x05, bytearray([0xC9, 0x02])) # CMP #02
    rom.write_bytes(VERTICAL_SCROLL_SUB_ADDR + 0x07, bytearray([0xD0, 0x02])) # BNE +0x02
    rom.write_bytes(VERTICAL_SCROLL_SUB_ADDR + 0x09, bytearray([0xA9, 0x01])) # LDA #01
    rom.write_bytes(VERTICAL_SCROLL_SUB_ADDR + 0x0B, bytearray([0x28]))       # PLP
    rom.write_bytes(VERTICAL_SCROLL_SUB_ADDR + 0x0C, bytearray([0x6B]))       # RTL


def handle_music_shuffle(rom, world, player):
    from .Aesthetics import generate_shuffled_level_music, generate_shuffled_ow_music, level_music_address_data, ow_music_address_data

    shuffled_level_music = generate_shuffled_level_music(world, player)
    for i in range(len(shuffled_level_music)):
        rom.write_byte(level_music_address_data[i], shuffled_level_music[i])

    shuffled_ow_music = generate_shuffled_ow_music(world, player)
    for i in range(len(shuffled_ow_music)):
        for addr in ow_music_address_data[i]:
            rom.write_byte(addr, shuffled_ow_music[i])


def handle_mario_palette(rom, world, player):
    from .Aesthetics import mario_palettes, fire_mario_palettes, ow_mario_palettes

    chosen_palette = world.mario_palette[player].value

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


def handle_bowser_rooms(rom, world, player: int):
    if world.bowser_castle_rooms[player] == "random_two_room":
        chosen_rooms = world.per_slot_randoms[player].sample(standard_bowser_rooms, 2)

        rom.write_byte(0x3A680, chosen_rooms[0].roomID)
        rom.write_byte(0x3A684, chosen_rooms[0].roomID)
        rom.write_byte(0x3A688, chosen_rooms[0].roomID)
        rom.write_byte(0x3A68C, chosen_rooms[0].roomID)

        for i in range(1, len(chosen_rooms)):
            rom.write_byte(chosen_rooms[i-1].exitAddress, chosen_rooms[i].roomID)

        rom.write_byte(chosen_rooms[len(chosen_rooms)-1].exitAddress, 0xBD)

    elif world.bowser_castle_rooms[player] == "random_five_room":
        chosen_rooms = world.per_slot_randoms[player].sample(standard_bowser_rooms, 5)

        rom.write_byte(0x3A680, chosen_rooms[0].roomID)
        rom.write_byte(0x3A684, chosen_rooms[0].roomID)
        rom.write_byte(0x3A688, chosen_rooms[0].roomID)
        rom.write_byte(0x3A68C, chosen_rooms[0].roomID)

        for i in range(1, len(chosen_rooms)):
            rom.write_byte(chosen_rooms[i-1].exitAddress, chosen_rooms[i].roomID)

        rom.write_byte(chosen_rooms[len(chosen_rooms)-1].exitAddress, 0xBD)

    elif world.bowser_castle_rooms[player] == "gauntlet":
        chosen_rooms = standard_bowser_rooms.copy()
        world.per_slot_randoms[player].shuffle(chosen_rooms)

        rom.write_byte(0x3A680, chosen_rooms[0].roomID)
        rom.write_byte(0x3A684, chosen_rooms[0].roomID)
        rom.write_byte(0x3A688, chosen_rooms[0].roomID)
        rom.write_byte(0x3A68C, chosen_rooms[0].roomID)

        for i in range(1, len(chosen_rooms)):
            rom.write_byte(chosen_rooms[i-1].exitAddress, chosen_rooms[i].roomID)

        rom.write_byte(chosen_rooms[len(chosen_rooms)-1].exitAddress, 0xBD)
    elif world.bowser_castle_rooms[player] == "labyrinth":
        bowser_rooms_copy = full_bowser_rooms.copy()

        entrance_point = bowser_rooms_copy.pop(0)

        world.per_slot_randoms[player].shuffle(bowser_rooms_copy)

        rom.write_byte(entrance_point.exitAddress, bowser_rooms_copy[0].roomID)
        for i in range(0, len(bowser_rooms_copy) - 1):
            rom.write_byte(bowser_rooms_copy[i].exitAddress, bowser_rooms_copy[i+1].roomID)

        rom.write_byte(bowser_rooms_copy[len(bowser_rooms_copy)-1].exitAddress, 0xBD)


def handle_boss_shuffle(rom, world, player):
    if world.boss_shuffle[player] == "simple":
        submap_boss_rooms_copy = submap_boss_rooms.copy()
        ow_boss_rooms_copy = ow_boss_rooms.copy()

        world.per_slot_randoms[player].shuffle(submap_boss_rooms_copy)
        world.per_slot_randoms[player].shuffle(ow_boss_rooms_copy)

        for i in range(len(submap_boss_rooms_copy)):
            rom.write_byte(submap_boss_rooms[i].exitAddress, submap_boss_rooms_copy[i].roomID)

        for i in range(len(ow_boss_rooms_copy)):
            rom.write_byte(ow_boss_rooms[i].exitAddress, ow_boss_rooms_copy[i].roomID)

            if ow_boss_rooms[i].exitAddressAlt is not None:
                rom.write_byte(ow_boss_rooms[i].exitAddressAlt, ow_boss_rooms_copy[i].roomID)

    elif world.boss_shuffle[player] == "full":
        for i in range(len(submap_boss_rooms)):
            chosen_boss = world.per_slot_randoms[player].choice(submap_boss_rooms)
            rom.write_byte(submap_boss_rooms[i].exitAddress, chosen_boss.roomID)

        for i in range(len(ow_boss_rooms)):
            chosen_boss = world.per_slot_randoms[player].choice(ow_boss_rooms)
            rom.write_byte(ow_boss_rooms[i].exitAddress, chosen_boss.roomID)

            if ow_boss_rooms[i].exitAddressAlt is not None:
                rom.write_byte(ow_boss_rooms[i].exitAddressAlt, chosen_boss.roomID)

    elif world.boss_shuffle[player] == "singularity":
        chosen_submap_boss = world.per_slot_randoms[player].choice(submap_boss_rooms)
        chosen_ow_boss = world.per_slot_randoms[player].choice(ow_boss_rooms)

        for i in range(len(submap_boss_rooms)):
            rom.write_byte(submap_boss_rooms[i].exitAddress, chosen_submap_boss.roomID)

        for i in range(len(ow_boss_rooms)):
            rom.write_byte(ow_boss_rooms[i].exitAddress, chosen_ow_boss.roomID)

            if ow_boss_rooms[i].exitAddressAlt is not None:
                rom.write_byte(ow_boss_rooms[i].exitAddressAlt, chosen_ow_boss.roomID)


def patch_rom(world, rom, player, active_level_dict):
    goal_text = generate_goal_text(world, player)

    rom.write_bytes(0x2A6E2, goal_text)
    rom.write_byte(0x2B1D8, 0x80)

    intro_text = generate_text_box("Bowser has stolen all of Mario's abilities. Can you help Mario travel across Dinosaur land to get them back and save the Princess from him?")
    rom.write_bytes(0x2A5D9, intro_text)

    handle_bowser_rooms(rom, world, player)
    handle_boss_shuffle(rom, world, player)

    # Prevent Title Screen Deaths
    rom.write_byte(0x1C6A, 0x80)

    # Title Screen Text
    player_name_bytes = bytearray()
    player_name = world.get_player_name(player)
    for i in range(16):
        char = " "
        if i < len(player_name):
            char = world.get_player_name(player)[i]
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

    rom.write_bytes(0x2B6D7, bytearray([0xFC, 0x38, 0xFC, 0x38, 0x16, 0x38, 0x18, 0x38, 0x0D, 0x38, 0xFC, 0x38, 0x0B, 0x38, 0x22, 0x38,
                                        0xFC, 0x38, 0x19, 0x38, 0x18, 0x38, 0x1B, 0x38, 0x22, 0x38, 0x10, 0x38, 0x18, 0x38, 0x17, 0x38,
                                        0x0E, 0x38, 0xFC, 0x38, 0xFC, 0x38])) # Mod by PoryGone

    # Title Options
    rom.write_bytes(0x1E6A, bytearray([0x01]))
    rom.write_bytes(0x1E6C, bytearray([0x01]))
    rom.write_bytes(0x1E6E, bytearray([0x01]))

    # Always allow Start+Select
    rom.write_bytes(0x2267, bytearray([0xEA, 0xEA]))

    # Always bring up save prompt on beating a level
    if world.autosave[player]:
        rom.write_bytes(0x20F93, bytearray([0x00]))

    if world.overworld_speed[player] == "fast":
        rom.write_bytes(0x21414, bytearray([0x20, 0x10]))
    elif world.overworld_speed[player] == "slow":
        rom.write_bytes(0x21414, bytearray([0x05, 0x05]))

    # Starting Life Count
    rom.write_bytes(0x1E25, bytearray([world.starting_life_count[player].value - 1]))

    # Repurpose Bonus Stars counter for Boss Token or Yoshi Eggs
    rom.write_bytes(0x3F1AA, bytearray([0x00] * 0x20))

     # Delete Routine that would copy Mario position data over repurposed Luigi save data
    rom.write_bytes(0x20F9F, bytearray([0xEA] * 0x3D))

    # Prevent Switch Palaces setting the Switch Palace flags
    rom.write_bytes(0x6EC9A, bytearray([0xEA, 0xEA]))
    rom.write_bytes(0x6EB1, bytearray([0xEA, 0xEA]))
    rom.write_bytes(0x6EB4, bytearray([0xEA, 0xEA, 0xEA]))

    handle_ability_code(rom)

    handle_yoshi_box(rom)
    handle_bowser_damage(rom)

    handle_collected_paths(rom)

    handle_vertical_scroll(rom)

    # Handle Level Shuffle
    handle_level_shuffle(rom, active_level_dict)

    # Handle Music Shuffle
    if world.music_shuffle[player] != "none":
        handle_music_shuffle(rom, world, player)

    generate_shuffled_ow_palettes(rom, world, player)

    generate_shuffled_header_data(rom, world, player)

    if world.swap_donut_gh_exits[player]:
        handle_swap_donut_gh_exits(rom)

    handle_mario_palette(rom, world, player)

    # Store all relevant option results in ROM
    rom.write_byte(0x01BFA0, world.goal[player].value)
    if world.goal[player].value == 0:
        rom.write_byte(0x01BFA1, world.bosses_required[player].value)
    else:
        rom.write_byte(0x01BFA1, 0x7F)
    required_yoshi_eggs = max(math.floor(
        world.number_of_yoshi_eggs[player].value * (world.percentage_of_yoshi_eggs[player].value / 100.0)), 1)
    rom.write_byte(0x01BFA2, required_yoshi_eggs)
    #rom.write_byte(0x01BFA3, world.display_sent_item_popups[player].value)
    rom.write_byte(0x01BFA4, world.display_received_item_popups[player].value)
    rom.write_byte(0x01BFA5, world.death_link[player].value)
    rom.write_byte(0x01BFA6, world.dragon_coin_checks[player].value)
    rom.write_byte(0x01BFA7, world.swap_donut_gh_exits[player].value)


    from Utils import __version__
    rom.name = bytearray(f'SMW{__version__.replace(".", "")[0:3]}_{player}_{world.seed:11}\0', 'utf8')[:21]
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
