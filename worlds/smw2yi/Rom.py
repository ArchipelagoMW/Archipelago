import Utils
import pdb
from Patch import read_rom, APDeltaPatch
USHASH = 'cb472164c5a71ccd3739963390ec6a50'
ROM_PLAYER_LIMIT = 65535

import hashlib
import os
import pdb
import math







rom_item_sprites = {
    16001: [[0x707E7F, 0x1]], # Spring Ball
    16002: [[0x707E8B, 0x1]], # Large Spring Ball
    16003: [[0x707E82, 0x1]], # ! Switch
    16004: [[0x707E84, 0x1]], # Dashed Platform
    16005: [[0x707E83, 0x1]], # Dashed Stairs
    16007: [[0x707E8A, 0x1]], # Beanstalk
    16008: [[0x707E85, 0x1]], # Helicopter
    16009: [[0x707E87, 0x1]], # Mole Tank
    16010: [[0x707E86, 0x1]], # Car
    16011: [[0x707E88, 0x1]], # Submarine
    16012: [[0x707E89, 0x1]], # Train
}



class LocalRom(object):

    def __init__(self, file, patch=True, vanillaRom=None, name=None, hash=None):
        self.name = name
        self.hash = hash
        self.orig_buffer = None

        with open(file, 'rb') as stream:
            self.buffer = read_rom(stream)
        
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




def handle_sprite_code(rom):

    #Spring Ball
    rom.write_bytes(0x0582F7, bytearray([0x5C, 0xB0, 0xF7, 0x00])) # JSL $03BB91
    
    rom.write_bytes(0xF7B0, bytearray([0xAF, 0x7F, 0x7E, 0x70]))  #LDA $707E7F
    rom.write_bytes(0xF7B4, bytearray([0xE2, 0x20])) #SEP #$20   
    rom.write_bytes(0xF7B6, bytearray([0xC9, 0x01])) #CMP #$01
    rom.write_bytes(0xF7B8, bytearray([0xC2, 0x20])) #REP #$20
    rom.write_bytes(0xF7BA, bytearray([0xF0, 0x04])) #BEQ
    rom.write_bytes(0xF7BC, bytearray([0x5C, 0x2E, 0xA3, 0x03])) #JML $03A32E
    rom.write_bytes(0xF7C0, bytearray([0x22, 0x07, 0xA0, 0x00])) #JSL $02A007
    rom.write_bytes(0xF7C4, bytearray([0x5C, 0xFB, 0x82, 0x05])) #JML $0582FB

    #End Spring Ball


    return




def patch_rom(world, rom, player):
    local_random = world.slot_seeds[player]

    
    rom.write_bytes(0x2267, bytearray([0xEA, 0xEA])) 
    rom.write_bytes(0x01C151, bytearray([0x5C, 0x53, 0xC1, 0x01]))

    rom.write_bytes(0x5142, bytearray([0x22, 0x65, 0xBB, 0x03])) # JSL $03BB65
    rom.write_bytes(0x5146, bytearray([0x60] * 0x01))            # RTS

    handle_sprite_code(rom)

    from Main import __version__
    rom.name = bytearray(f'YI{__version__.replace(".", "")[0:3]}_{player}_{world.seed:11}\0', 'utf8')[:21]
    rom.name.extend([0] * (21 - len(rom.name)))
    rom.write_bytes(0x7FC0, rom.name)



    

class YIDeltaPatch(APDeltaPatch):
    hash = USHASH
    game: str = "Yoshi's Island"
    patch_file_ending = ".apyi"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(read_rom(open(file_name, "rb")))

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
        file_name = options["yoshis_island_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.local_path(file_name)
    return file_name