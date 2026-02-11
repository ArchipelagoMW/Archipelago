import hashlib
import math
import os
import struct
import random

from settings import get_settings
import Utils
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes

from worlds.AutoWorld import World

NOP = bytes([0x00,0x00,0x00,0x00])
MD5Hash = "093058ece14c8cc1a887b2087eb5cfe9"

DEATHLINK_ROUTINE = [   
    0x8C,0x42,0xEE,0x34, # LW	V0, 0xEE34 (V0)
    0x3C,0x1C,0x80,0x09, # LUI	GP, 0x8009
    0x27,0x9C,0xED,0x00, # ADDIU	GP, GP, 0xE5E0
    0x8F,0x8B,0x00,0x50, # LW	T3, 0x0050 (GP)

    0x00,0x00,0x00,0x00, # NOP
    0x11,0x60,0x00,0x0E, # BEQZ	T3, 0x80277B48
    0x00,0x00,0x00,0x00, # NOP
    0x24,0x05,0x00,0x01, # ADDIU	A1, R0, 0x0001

    0xAF,0x80,0x00,0x50, # SW	R0, 0x0050 (GP)
    0x08,0x09,0x20,0x52, # J	0x80248148 [Damage Routine]
    0x00,0x1C,0xE0,0x24, # AND	GP, R0, GP
    0x00,0x00,0x00,0x00, # NOP

    0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00, 
    0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,

    0x00,0x1C,0xE0,0x24, # AND	GP, R0, GP
    0x03,0xE0,0x00,0x08, # JR
    # Jump long used to preserve the stack
              ]

REMOTE_POWER_CHECK = [

    0x00,0x0A,0x50,0xC0, # SLL	T2, T2, 3 ; From Original code
    0x01,0x4B,0x18,0x21, # ADDU	V1, T2, T3 ; From Original code
    0x3C,0x1C,0x80,0x2B, # LUI	GP, 0x802B
    0x27,0x9C,0xC5,0xD0, # ADDIU	GP, GP, 0xC5D0

    0x83,0x8E,0x00,0x07, # LB	T6, 0x0007 (GP) ; T6 = Stage ID
    #0x83,0x8F,0x00,0x0B, # LB	T7, 0x000B (GP)
    0x21,0xCE,0xFF,0xD8, # ADDI	T6, T6, 0xFFD8
    #0x00,0x0E,0x71,0x00, # SLL	T6, T6, 4
    0x00,0x6E,0x18,0x21, # ADDU	V1, V1, T6
    0x00,0x00,0x00,0x00, # NOP

    #0x00,0x0F,0x78,0x80, # SLL	T7, T7, 2
    #0x00,0x6F,0x18,0x21, # ADDU	V1, V1, T7
    0x00,0x00,0x00,0x00, # NOP
    0x00,0x00,0x00,0x00, # NOP
    0x08,0x09,0xE6,0x6D, # J 0x802799B4
    0x03,0x80,0xE0,0x24, # AND	GP, GP, R0

    0x00,0x0C,0x60,0xC0, # SLL	T4, T4, 3
    0x01,0x8D,0x18,0x21, # ADDU	V1, T4, T5
    0x3C,0x1C,0x80,0x2B, # LUI	GP, 0x802B
    0x27,0x9C,0xC5,0xD0, # ADDIU	GP, GP, 0xC5D0

    0x83,0x98,0x00,0x07, # LB	T8, 0x0007 (GP)
    0x23,0x18,0xFF,0xD8, # ADDI	T8, T8, 0xFFD8
    #0x83,0x99,0x00,0x0B, # LB	T9, 0x000B (GP)
    #0x00,0x18,0xC1,0x00, # SLL	T8, T8, 4
    0x00,0x78,0x18,0x21, # ADDU	V1, V1, T8
    0x00,0x00,0x00,0x00, # NOP

    0x00,0x00,0x00,0x00, # NOP
    0x00,0x00,0x00,0x00, # NOP
    #0x00,0x19,0xC8,0x80, # SLL	T9, T9, 2
    #0x00,0x79,0x18,0x21, # ADDU	V1, V1, T9
    0x08,0x09,0xE6,0x57, # J	0x8027995C
    0x03,0x80,0xE0,0x24, # AND	GP, GP, R0
]

bomnberani_offsets = [
    0x69787, # 0x01 - Falling
    0x69814, # 0x02 - Walking
    0x6988F, # 0x03 - Run
    #0x6481B, # 0x04 - Hold
    0x6476F, # 0x06 - Throw
    0x64063, # 0x07 - Kick
    0x66BA3, # 0x08 - Stun
    0x62742, # 0x0B - Hit
    #0x6405F, # 0x10 - Kick Animation?
]

class Bomb64ProcedurePatch(APProcedurePatch, APTokenMixin):#
    game = "Bomberman 64"
    hash = MD5Hash
    patch_file_ending = ".apbomb64"
    result_file_ending = ".z64"
    #name: str = ""

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()
    
def write_tokens(world:World, patch:Bomb64ProcedurePatch):
    # Write Rom name
    for j, b in enumerate(world.romName):
        patch.write_token(APTokenTypes.WRITE, 0xDFFC0 + j, struct.pack("<B", b))
    for j, b in enumerate(world.playerName):
        patch.write_token(APTokenTypes.WRITE, 0xDFFE0 + j, struct.pack("<B", b))
    
    # Write game options
    patch.write_token(APTokenTypes.WRITE, 0xDFFB0, bytes([world.options.gold_cards.value]))
    patch.write_token(APTokenTypes.WRITE, 0xDFFB1, bytes([world.options.game_goal.value]))
    patch.write_token(APTokenTypes.WRITE, 0xDFFB2, bytes([world.options.death_link.value]))
    patch.write_token(APTokenTypes.WRITE, 0xDFFB3, bytes([world.options.difficulty.value]))
    patch.write_token(APTokenTypes.WRITE, 0xDFFB4, bytes([world.options.enemy_model.value]))
    patch.write_token(APTokenTypes.WRITE, 0xDFFB5, bytes([world.options.enemy_ai.value]))
    patch.write_token(APTokenTypes.WRITE, 0xDFFB6, bytes([world.options.random_music.value]))
    patch.write_token(APTokenTypes.WRITE, 0xDFFB7, bytes([world.options.random_sound.value]))
    #patch.write_token(APTokenTypes.WRITE, 0xDFFB8, bytearray([world.team]))

    # Bypass CIC
    patch.write_token(APTokenTypes.WRITE, 0x66C, NOP)
    patch.write_token(APTokenTypes.WRITE, 0x678, NOP)
    
    # Do Not Gain Bombs
    #patch.write_token(APTokenTypes.WRITE, 0x9232C, bytearray([0x01, 0x40, 0x58, 0x21]))
    patch.write_token(APTokenTypes.WRITE, 0x94108, NOP)
    # Do Not Gain Fireups
    #patch.write_token(APTokenTypes.WRITE, 0x936BC, bytearray([0x01, 0x40, 0x58, 0x21]))
    # This frees up some space
    patch.write_token(APTokenTypes.WRITE, 0x940C8, NOP)

    # Do Not Gain Remote Bomb
    # patch.write_token(APTokenTypes.WRITE, 0x941CF, bytearray([0x00]))
    # Do Not Gain Power Bombs
    # patch.write_token(APTokenTypes.WRITE, 0x94178, NOP)

    # Jump to AP routines
    patch.write_token(APTokenTypes.WRITE, 0x5EBE4, bytes([0x08,0x09,0xDE,0xBE, 0x00,0x4E,0x10,0x21])) # J 0x80277AF8
    
    # Custom AP routine
    #  Deathlink
    patch.write_token(APTokenTypes.WRITE, 0x922F8, bytes(DEATHLINK_ROUTINE))

    #  Remote/Power Checks

    #    Power Bomb Jump to routine
    patch.write_token(APTokenTypes.WRITE, 0x9414C, bytes([
        0x3C,0x0D,0x80,0x09, # LUI	T5, 0x8009
        0x25,0xAD,0xEF,0x60, # ADDIU T5, T5, 0xEF60
        0x08,0x09,0xE3,0xAD, # J	0x80278EB4
        0x00,0x00,0x00,0x00, # NOP
        0x80,0x6E,0x00,0x00, # LB	T6, 0x0000 (V1)

    ]))
    patch.write_token(APTokenTypes.WRITE, 0x94178, bytes([0xA0,0x6F,0x00,0x00])) # SB	T7, 0x0000 (V1)
    #    Remote Bomb Jump to routine
    patch.write_token(APTokenTypes.WRITE, 0x941A4, bytes([
        0x3C,0x0B,0x80,0x09, # LUI	T3, 0x8009
        0x25,0x6B,0xEF,0x60, # ADDIU T3, T3, 0xEF60
        0x08,0x09,0xE3,0xA1, # J	0x80278E84
        0x00,0x00,0x00,0x00, # NOP
        0x80,0x6C,0x00,0x00, # LB	T4, 0x0000 (V1)
    ]))
    patch.write_token(APTokenTypes.WRITE, 0x941D0, bytes([0xA0,0x6D,0x00,0x00])) # SB	T5, 0x0000 (V1)
    
    patch.write_token(APTokenTypes.WRITE, 0x93684, bytes(REMOTE_POWER_CHECK))
    #patch.write_token(APTokenTypes.WRITE, 0x922A0, bytearray([FREESPACE]))
    
    # Require Power Gloves to Pick up Items
    patch.write_token(APTokenTypes.WRITE, 0x64820, bytes([0x8E, 0xA5, 0x16, 0x08]))

    # Requrie Bomb Kick
    patch.write_token(APTokenTypes.WRITE, 0x64094, bytes([0x8E, 0xA5, 0x16, 0x0C]))

    # Enable stage exit
    patch.write_token(APTokenTypes.WRITE, 0x56318, NOP)
    patch.write_token(APTokenTypes.WRITE, 0x56600, NOP)
    patch.write_token(APTokenTypes.WRITE, 0x554D4, NOP)

    # Do not auto advance to next stage
    #patch.write_token(APTokenTypes.WRITE, 0x166A5F, bytearray([0x01]))

    # Open Black Fortress
    #patch.write_token(APTokenTypes.WRITE, 0x166A5F, bytearray([0x8C, 0x43, 0x01,0x64])),

    # Game Crashes without this
    patch.write_token(APTokenTypes.WRITE, 0x935E0, bytes([0x10,0x00,0x00,0x04])) # BEZ -> B 0x80278DF4

    # Retain Gold Cards On Level Exit
    patch.write_token(APTokenTypes.WRITE, 0xA4C80, NOP)

    # Check for kill requirement at 0xBD000
    patch.write_token(APTokenTypes.WRITE, 0x9D200, bytes([0x8C, 0x61, 0x0A, 0xE0])) # LW AT, 0x0AE0 (v1)
    patch.write_token(APTokenTypes.WRITE, 0x9D208, bytes([0x00, 0x01, 0x08, 0x40])) # SLL AT, AT, 1
    patch.write_token(APTokenTypes.WRITE, 0x9D210, bytes([0x00, 0x01, 0x08, 0x40])) # SLL AT, AT, 1
    patch.write_token(APTokenTypes.WRITE, 0x9D218, bytes([0x00, 0x01, 0x08, 0x40])) # SLL AT, AT, 1

    # Write patch file
    patch.write_file("token_data.bin", patch.get_token_binary())

def get_base_rom_bytes(file_name: str ="") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(Utils.read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        md5hash = basemd5.hexdigest()
        if MD5Hash !=md5hash:
            raise Exception("Supplied Rom does not match known MD5 for Bobmerman 64")
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes

def get_base_rom_path(file_name: str="")-> str:
    if not file_name:
        file_name = get_settings().bomberman64_settings.rom_file
    if not os.path.exists(file_name):
        file_name= Utils.user_path(file_name)
    return file_name
