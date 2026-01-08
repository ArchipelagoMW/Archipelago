from collections.abc import Collection
from typing import Optional

from worlds.tloz_oos.patching.Util import hex_str


class RomData:
    buffer: bytearray

    def __init__(self, file: bytes, name: Optional[str] = None) -> None:
        self.file = bytearray(file)
        self.name = name

    def read_bit(self, address: int, bit_number: int) -> bool:
        bitflag = (1 << bit_number)
        return (self.buffer[address] & bitflag) != 0

    def read_byte(self, address: int) -> int:
        return self.file[address]

    def read_bytes(self, start_address: int, length: int) -> bytearray:
        return self.file[start_address:start_address + length]

    def read_word(self, address: int):
        word_bytes = self.read_bytes(address, 2)
        return (word_bytes[1] * 0x100) + word_bytes[0]

    def write_byte(self, address: int, value: int) -> None:
        self.file[address] = value

    def write_bytes(self, start_address: int, values: Collection[int]) -> None:
        self.file[start_address:start_address + len(values)] = values

    def write_word(self, address: int, value: int) -> None:
        value = value & 0xFFFF
        self.write_bytes(address, [value & 0xFF, (value >> 8) & 0xFF])

    def write_word_be(self, address: int, value: int) -> None:
        value = value & 0xFFFF
        self.write_bytes(address, [(value >> 8) & 0xFF, value & 0xFF])

    def add_bank(self, fill: int) -> None:
        self.file.extend([fill] * 0x4000)

    def update_header_checksum(self) -> None:
        """
        Updates the 8-bit checksum for ROM data located in the rom header.
        """
        result = -0x19
        for b in self.read_bytes(0x134, 0x19):
            result -= int(b)
        self.write_byte(0x14D, result & 0xFF)

    def update_checksum(self, address):
        """
        Updates the 16-bit checksum for ROM data located in the rom header.
        This is calculated by summing the non-global-checksum bytes in the rom.
        This must not be confused with the header checksum, which is the byte before.
        """
        result = 0
        for b in self.read_bytes(0x0, address):
            result += b
        for b in self.read_bytes(address + 2, 0xffffff):
            result += b
        result &= 0xffff
        self.write_word_be(address, result & 0xffff)

    def update_rom_size(self) -> None:
        """
         Updates the ROM size for ROM data located in the rom header.
        """
        if len(self.file) == 0x100000:
            self.write_byte(0x148, 0x05)
        elif len(self.file) == 0x200000:
            self.write_byte(0x148, 0x06)
        else:
            raise ValueError(f"Invalid ROM size: {hex(len(self.file))}")


    def get_chest_addr(self, group_and_room: int):
        """
        Return the address where to edit item ID and sub-ID to modify the contents
        of the chest contained in given room of given group
        """
        base_addr = 0x54f6c
        room = group_and_room & 0xFF
        group = group_and_room >> 8
        current_addr = 0x50000 + self.read_word(base_addr + (group * 2))
        while self.read_byte(current_addr) != 0xff:
            chest_room = self.read_byte(current_addr + 1)
            if chest_room == room:
                return current_addr + 2
            current_addr += 4
        raise Exception(f"Unknown chest in room {group}|{hex_str(room)}")

    def output(self) -> bytes:
        return bytes(self.file)
