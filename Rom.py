import hashlib
from pathlib import Path
from BaseClasses import MultiWorld

import Utils
from Patch import APDeltaPatch


MD5_US_EU = "5fe47355a33e3fabec2a1607af88a404"


class WL4DeltaPatch(APDeltaPatch):
    hash = MD5_US_EU
    game = "Wario Land 4"
    patch_file_ending = ".apwl4"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


class LocalRom():
    def __init__(self, file: Path, name=None, hash=None):
        self.name = name
        self.hash = hash


        with open(file, "rb") as stream:
            self.buffer = bytearray(stream.read())

    def read_bit(self, address: int, bit_number: int) -> bool:
        bitflag = (1 << bit_number)
        return ((self.buffer[address] & bitflag) != 0)

    def read_byte(self, address: int) -> int:
        return self.buffer[address]

    def read_bytes(self, startaddress: int, length: int) -> bytes:
        return self.buffer[startaddress:startaddress + length]
    
    def read_halfword(self, address: int) -> int:
        assert address % 2 == 0, "Misaligned halfword address"
        halfword = self.read_bytes(address, 2)
        return int.from_bytes(halfword, "little")
    
    def read_word(self, address: int) -> int:
        assert address % 4 == 0, "Misaligned word address"
        word = self.read_bytes(address, 4)
        return int.from_bytes(word, "little")

    def write_byte(self, address: int, value: int):
        self.buffer[address] = value

    def write_bytes(self, startaddress: int, values):
        self.buffer[startaddress:startaddress + len(values)] = values
    
    def write_halfword(self, address: int, value: int):
        assert address % 2 == 0, "Misaligned halfword address"
        halfword = value.to_bytes(2, "little")
        self.write_bytes(address, halfword)
    
    def write_word(self, address: int, value: int):
        assert address % 4 == 0, "Misaligned word address"
        word = value.to_bytes(4, "little")
        self.write_bytes(address, word)

    def write_to_file(self, file: Path):
        with open(file, 'wb') as stream:
            stream.write(self.buffer)


def patch_rom(world: MultiWorld, rom: LocalRom, player: int):
    class Halfword(int):
        pass
    class Word(int):
        pass

    add_location_save_data = {
        # Level states are in save data as 32-bit numbers, but only the lower 6 bits
        # are used in vanilla, so we can use the second byte to store check data.

        # Load checked location data from bits 13:8 in ItemGetFlgSet_LoadSavestateInfo2RAM()
        0x75E4E: Halfword(0x7849),  # ldrb r1, [r1, #1]  ; Jewel piece 1
        0x75E78: Halfword(0x7849),  # ldrb r1, [r1, #1]  ; Jewel piece 2
        0x75EA0: Halfword(0x7849),  # ldrb r1, [r1, #1]  ; Jewel piece 3
        0x75EC8: Halfword(0x7849),  # ldrb r1, [r1, #1]  ; Jewel piece 4
        0x75EF0: Halfword(0x7849),  # ldrb r1, [r1, #1]  ; CD

        # Save checked location data to bits 13:8 in SeisanSave()
        0x811D0: Halfword(0x7848),  # ldrb r0, [r1, #1]  ; Jewel piece 1
        0x811D6: Halfword(0x7048),  # strb r0, [r1, #1]  ; Jewel piece 1
        0x811F4: Halfword(0x7848),  # ldrb r0, [r1, #1]  ; Jewel piece 2
        0x811FA: Halfword(0x7048),  # strb r0, [r1, #1]  ; Jewel piece 2
        0x81216: Halfword(0x7848),  # ldrb r0, [r1, #1]  ; Jewel piece 3
        0x8121C: Halfword(0x7048),  # strb r0, [r1, #1]  ; Jewel piece 3
        0x81238: Halfword(0x7848),  # ldrb r0, [r1, #1]  ; Jewel piece 4
        0x8123E: Halfword(0x7048),  # strb r0, [r1, #1]  ; Jewel piece 4
        0x8125A: Halfword(0x7848),  # ldrb r0, [r1, #1]  ; CD
        0x81260: Halfword(0x7048),  # strb r0, [r1, #1]  ; CD
    }

    skip_cutscenes = {
        # Intro cutscene
        # This does three things:
        #  1: Prevent the cutscene from starting
        #  2: Stop the title music playing
        #  3: Don't play the car engine sound
        # Each of these is a separate event due to the way the cutscene is timed
        0x00312: Halfword(0x2001),  # movs r0, #1  ; 1: Assume data exists in MainGameLoop()
        0x91944: Halfword(0x0000),  # movs r0, r0  ; 2: Never branch in GameReady()
        0x91DA8: Word(0x8091DD8),   # 3: Modify jump table in ReadySet_SelectKey()

        # TODO Autosave tutorial
        # TODO Jewel cutscene
    }

    # TODO more rando check logic

    # Currently unused but what's written here was convenient enough to handle now
    keysanity = {
        # Check data
        0x75F18: Halfword(0x7849),  # ldrb r1, [r1, #1]  ; ItemGetFlgSet_LoadSavestateInfo2RAM()
        0x8127C: Halfword(0x7848),  # ldrb r0, [r1, #1]  ; SeisanSave()
        0x81282: Halfword(0x7048),  # strb r0, [r1, #1]  ; SeisanSave()

        # TODO skip cutscene
    }

    patches = {
        **add_location_save_data,
        **skip_cutscenes
    }
    
    for address, value in patches.items():
        if type(value) == Halfword:
            rom.write_halfword(address, value)
        if type(value) == Word:
            rom.write_word(address, value)

def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_path = get_base_rom_path(file_name)
        base_rom_bytes = bytes(open(file_path, "rb").read())

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if MD5_US_EU != basemd5.hexdigest():
            raise Exception("Supplied base ROM does not match US/EU version."
                            "Please provide the correct ROM version")
        
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> Path:
    options = Utils.get_options()
    if not file_name:
        file_name = options["wl4_options"]["rom_file"]

    file_path = Path(file_name)
    if file_path.exists():
        return file_path
    else:
        return Path(Utils.local_path(file_name))
