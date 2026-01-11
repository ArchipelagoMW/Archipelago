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
MD5Hash = "aec1fdb0f1caad86c9f457989a4ce482"

OPTIONS_BASE = 0x99FD0

class BombTSAProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Bomberman The Second Attack"
    hash = MD5Hash
    patch_file_ending = ".apbombtsa"
    result_file_ending = ".z64"
    #name: str = ""

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()
    
def write_tokens(world:World, patch:BombTSAProcedurePatch, startbomb):
    # Write Rom name
    for j, b in enumerate(world.romName):
        patch.write_token(APTokenTypes.WRITE, 0x99FE0 + j, struct.pack("<B", b))
    for j, b in enumerate(world.playerName):
        patch.write_token(APTokenTypes.WRITE, 0x9A000 + j, struct.pack("<B", b))

    # write game options
    patch.write_token(APTokenTypes.WRITE,OPTIONS_BASE,bytes([world.options.noah_boss.value]))
    patch.write_token(APTokenTypes.WRITE,OPTIONS_BASE+1,bytes([world.options.game_goal.value]))
    if world.options.death_link:
        patch.write_token(APTokenTypes.WRITE,OPTIONS_BASE+2,bytes([0x01]))
    patch.write_token(APTokenTypes.WRITE,OPTIONS_BASE+4,bytes([world.options.noah_open.value]))
    patch.write_token(APTokenTypes.WRITE,OPTIONS_BASE+5,bytes([world.options.planet_required.value]))
    #patch.write_token(APTokenTypes.WRITE,OPTIONS_BASE+6,bytes([world.options.random_music]))
    # Random Starting Bomb
    patch.write_token(APTokenTypes.WRITE,OPTIONS_BASE+7,bytes([startbomb]))
    patch.write_token(APTokenTypes.WRITE,OPTIONS_BASE+8,bytes([world.options.pommyshop]))
    toggle_options = 0
    if world.options.random_efx:
        toggle_options += 1
    if world.options.random_sound:
        toggle_options += 2
    if world.options.random_music:
        toggle_options += 4
    patch.write_token(APTokenTypes.WRITE,OPTIONS_BASE+9,bytes([toggle_options]))
    # Change ROM name to 'BOMBERMANTSAU' to keep Bizhawk handler from thinking it's Bomberman 64
    patch.write_token(APTokenTypes.WRITE, 0x29, bytes([0x54,0x53,0x41,0x55]))
    # Bypass CIC
    patch.write_token(APTokenTypes.WRITE, 0x66C, NOP)
    patch.write_token(APTokenTypes.WRITE, 0x678, NOP)

    # Setup GP
    patch.write_token(APTokenTypes.WRITE, 0x38314, bytes([0x3C,0x1C,0x80,0x41])) # LUI	GP, 0x8041
    
    # Stage Select
    #patch.write_token(APTokenTypes.WRITE, 0x237B5C, bytes([0x14])) # Changes Base pointer
    #patch.write_token(APTokenTypes.WRITE, 0x237B72, bytes([0x80])) # Changes Base pointer

    # Bomb elemet Patch
    patch.write_token(APTokenTypes.WRITE, 0x32528, bytes([0x26,0x84,0x01,0xC0])) # ADDIU	A0, S4, 0x01C0
    patch.write_token(APTokenTypes.WRITE, 0x32534, bytes([0x10,0x40,0x00,0x0A])) # BEQZ	V0, 0x80031960
    #patch.write_token(APTokenTypes.WRITE, 0x32570, bytes([0x2A,0x61,0x00,0x00])) # SLTI	AT, S3, 0x0000

    # Move Pommy's Transformation
    patch.write_token(APTokenTypes.WRITE, 0x2B950, bytes([0xA0,0xEE,0x00,0x24])) # SB	T6, 0x0024 (A3)
    
    # Don't lose boss clears
    patch.write_token(APTokenTypes.WRITE, 0x3FB54, NOP)
    patch.write_token(APTokenTypes.WRITE, 0x3FC24, NOP)

    # Allow Cutscene Skip
    patch.write_token(APTokenTypes.WRITE, 0x53BB0, bytes([0x24,0x0E,0x00,0x01])) # ADDIU	T6, R0, 0x0001

    # Set Starting Bomb Type
    patch.write_token(APTokenTypes.WRITE, 0x5D010, bytes([0x34,0x05,0x00,startbomb])) # ORI	A1, R0, 0x000X
    # Guardian Armor Checks
    # Boots
    patch.write_token(APTokenTypes.WRITE, 0x31654, bytes([0x24,0x84,0x01,0x64]))
    
    # Powerup Checks; SW	T7, 0x0010 (V1)
    patch.write_token(APTokenTypes.WRITE, 0x5CBF8, bytes([0x80])) # Kick Load
    patch.write_token(APTokenTypes.WRITE, 0x5CC08, bytes([0xA0])) # Kick Write
    patch.write_token(APTokenTypes.WRITE, 0x5CC58, bytes([0x80])) # Glove Read
    patch.write_token(APTokenTypes.WRITE, 0x5CC68, bytes([0xA0])) # Glove Write
    patch.write_token(APTokenTypes.WRITE, 0x5CCB8, bytes([0x80])) # Remote Bomb Read
    patch.write_token(APTokenTypes.WRITE, 0x5CCC8, bytes([0xA0])) # Remote Bomb Write
    #patch.write_token(APTokenTypes.WRITE, 0x5CC08, NOP)
    #patch.write_token(APTokenTypes.WRITE, 0x5CC63, bytes([0x00]))
    
    # Keep Money Upon Level Exit
    patch.write_token(APTokenTypes.WRITE, 0x3FD50, NOP)

    # Keep Food on Death
    patch.write_token(APTokenTypes.WRITE, 0x31CA0, NOP)

    # Keep Progress flags on level reset
    #patch.write_token(APTokenTypes.WRITE, 0x3FD24, NOP)

    # Keep Max HP
    #patch.write_token(APTokenTypes.WRITE, 0x5D128, bytes([0x8C,0x6D,0x00,0x30])) # LW	T5, 0x0030 (V1)
    #patch.write_token(APTokenTypes.WRITE, 0x5D16C, bytes([0x8C,0x64,0xFF,0xF4])) # LW	A0, 0xFFF4 (V1)
    #patch.write_token(APTokenTypes.WRITE, 0x5CF40, NOP)


    # Keep Pommy Status Upon Level Exit
    pommy_status = bytes([0x90,0x59,0x00,0x20, 0x90,0x4E,0x00,0x21, 0x90,0x4F,0x00,0x22, 0x90,0x58,0x00,0x23])
    patch.write_token(APTokenTypes.WRITE, 0x3FD54, pommy_status)
    
    # Do not Gain Items
     # Max Health
    #patch.write_token(APTokenTypes.WRITE, 0x5CF40, NOP)
     # Max Health on Level 
    #patch.write_token(APTokenTypes.WRITE, 0x5D130, NOP)
     # Firepower 
    #patch.write_token(APTokenTypes.WRITE, 0x5CAA8, NOP)
     # Firepower
    #patch.write_token(APTokenTypes.WRITE, 0x5D004, NOP)
     # Speed
    #patch.write_token(APTokenTypes.WRITE, 0x5CBA8, NOP)
     # Bomb Kick
    

    # Reduce Pommy's food requirements to 10/20/30
    if world.options.reduce_food:
        patch.write_token(APTokenTypes.WRITE, 0x902A0, bytes([
            0x00,0x00,0x00,0x0A, 0x00,0x00,0x00,0x0A, 0x00,0x00,0x00,0x0A, 
            0x00,0x00,0x00,0x0A, 0x00,0x00,0x00,0x0A, 0x00,0x00,0x00,0x0A, 
        ]))
    
    # Fix Analog Stick Issue
    patch.write_token(APTokenTypes.WRITE, 0x43D4, bytes([0x24,0x10,0x00,0x00])) # ADDIU	S0, R0, 0x0000
    
    # Smooth Joystick Rotation
    patch.write_token(APTokenTypes.WRITE, 0x490C, bytes([0x24,0x02,0x00,0x7F])) # LUI	AT, 0x3F80
    patch.write_token(APTokenTypes.WRITE, 0x57D58, bytes([0x3C,0x01,0x3F,0x80])) # ADDIU	V0, R0, 0x007F

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
            raise Exception("Supplied Rom does not match known MD5 for Bobmerman The Second Attack")
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes

def get_base_rom_path(file_name: str="")-> str:
    if not file_name:
        file_name = get_settings().bombermantsa_settings.rom_file
    if not os.path.exists(file_name):
        file_name= Utils.user_path(file_name)
    return file_name