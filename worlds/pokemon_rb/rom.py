from Patch import read_rom
import os
import hashlib
from Utils import local_path, user_path, int16_as_bytes, int32_as_bytes
import Patch

POKEROMHASH = {"Red": 0, "Blue": 0}
POKERANDOBASEROMHASH = {"Red": 0, "Blue": 0}


class LocalRom(object):

    def __init__(self, file, patch=True, vanillaRom=None, name=None, hash=None):
        self.name = name
        self.hash = hash
        self.orig_buffer = None

        with open(file, 'rb') as stream:
            self.buffer = read_rom(stream)
        if patch:
            self.patch_base_rom()
            self.orig_buffer = self.buffer.copy()
        if vanillaRom:
            with open(vanillaRom, 'rb') as vanillaStream:
                self.orig_buffer = read_rom(vanillaStream)

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

    @staticmethod
    def verify(buffer, expected: str) -> bool:
        buffermd5 = hashlib.md5()
        buffermd5.update(buffer)
        return expected == buffermd5.hexdigest()

    def patch_base_rom(self):
        if os.path.isfile(local_path('pokebasepatch.gb')):
            with open(local_path('pokebasepatch.gb'), 'rb') as stream:
                buffer = bytearray(stream.read())

            if self.verify(buffer):
                self.buffer = buffer
                if not os.path.exists(local_path('data', 'pokebasepatch.apbp')):
                    Patch.create_patch_file(local_path('pokebasepatch.gb'))
                return

            if not os.path.isfile(local_path('data', 'pokebasepatch.apbp')):
                raise RuntimeError('Base patch unverified.  Unable to continue.')

        if os.path.isfile(local_path('data', 'pokebasepatch.apbp')):
            _, target, buffer = Patch.create_rom_bytes(local_path('data', 'pokebasepatch.apbp'), ignore_version=True)
            if self.verify(buffer):
                self.buffer = bytearray(buffer)
                with open(user_path('pokebasepatch.gb'), 'wb') as stream:
                    stream.write(buffer)
                return
            raise RuntimeError('Base patch unverified.  Unable to continue.')

        raise RuntimeError('Could not find Base Patch. Unable to continue.')

    def write_crc(self):
        crc = (sum(self.buffer[:0x7FDC] + self.buffer[0x7FE0:]) + 0x01FE) & 0xFFFF
        inv = crc ^ 0xFFFF
        self.write_bytes(0x7FDC, [inv & 0xFF, (inv >> 8) & 0xFF, crc & 0xFF, (crc >> 8) & 0xFF])

    def get_hash(self) -> str:
        h = hashlib.md5()
        h.update(self.buffer)
        return h.hexdigest()

    def write_int16(self, address: int, value: int):
        self.write_bytes(address, int16_as_bytes(value))

    def write_int32(self, address: int, value: int):
        self.write_bytes(address, int32_as_bytes(value))

    def write_int16s(self, startaddress: int, values):
        for i, value in enumerate(values):
            self.write_int16(startaddress + (i * 2), value)

    def write_int32s(self, startaddress: int, values):
        for i, value in enumerate(values):
            self.write_int32(startaddress + (i * 4), value)