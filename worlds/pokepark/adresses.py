from dataclasses import dataclass
from enum import Enum


class MemoryRange(Enum):
    BYTE = 1  # 1 Byte
    HALFWORD = 2  # 2 Bytes
    WORD = 4  # 4 Bytes

    @property
    def mask(self):
        if self == MemoryRange.WORD:
            return 0xFFFFFFFF
        elif self == MemoryRange.HALFWORD:
            return 0xFFFF
        else:  # BYTE
            return 0xFF

@dataclass
class MemoryAddress:
    base_address: int
    offset: int = 0
    memory_range: MemoryRange = MemoryRange.WORD
    value: int = 0

    @property
    def final_address(self):
        return self.base_address + self.offset


POWER_MAP = {
    "Progressive Dash": [0x01, 0x04, 0x08, 0x4000],
    "Progressive Thunderbolt": [0x10, 0x20, 0x40, 0x80],
    "Progressive Health": [0x100, 0x200, 0x400],
    "Progressive Iron Tail": [0x800, 0x1000, 0x2000],
    "Double Dash": [0x02]
}
