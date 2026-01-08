import struct
from typing import Any, overload

from . import lz10
from .symbols import get_symbol


ROM_START = 0x8000000


def get_rom_address(ptr: str | int, offset=0):
    if isinstance(ptr, str):
        address = get_symbol(ptr, offset)
    else:
        address = ptr + offset
    if not address & ROM_START:
        raise ValueError(f"{ptr}+{offset} is not in ROM (address: {address:07x})")
    return address & ROM_START - 1


class LocalRom:
    data: bytearray
    extra_space_address: int

    def __init__(self, data: bytes):
        self.data = bytearray(data)
        self.extra_space_address = get_rom_address("sRandoExtraData")

    @overload
    def read(self, address: int, length: int) -> bytes:
        ...

    @overload
    def read(self, address: int, struct: str) -> tuple[Any, ...]:
        ...

    def read(self, address: int, length_or_struct: int | str):
        if type(length_or_struct) is int:
            length = length_or_struct
        else:
            length = struct.calcsize(length_or_struct)
        data = self.data[address:address + length]
        if type(length_or_struct) is int:
            return data
        else:
            return struct.unpack(length_or_struct, data)

    def view(self, start_address: int) -> memoryview:
        return memoryview(self.data)[start_address:]

    def decompress_lzss(self, address: int) -> bytes:
        return bytes(lz10.decompress(self.view(address)))

    def alloc(self, size: int) -> int:
        assert size >= 0
        # Word-align all allocations
        if self.extra_space_address % 4 != 0:
            self.extra_space_address += 4 - self.extra_space_address % 4
        address = self.extra_space_address
        self.extra_space_address += size
        return address

    def write(self, address: int, data: bytes):
        assert address <= len(self.data), f"Address 0x{address:07x} out of range for ROM length 0x{len(self.data):07x}"
        self.data[address:address + len(data)] = data

    def append(self, data: bytes):
        address = self.alloc(len(data))
        self.write(address, data)
        return address | ROM_START

    def to_bytes(self):
        return bytes(self.data)
