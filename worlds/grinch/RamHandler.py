from typing import NamedTuple


class GrinchRamData(NamedTuple):
    ram_address: int
    value: int = None
    binary_bit_position: int = None
    bit_size: int = 1
