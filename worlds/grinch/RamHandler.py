from enum import STRICT, IntEnum
from typing import NamedTuple, Optional


class UpdateMethod(IntEnum, boundary=STRICT):
    SET = 1
    ADD = 2
    SUBTRACT = 3
    FREEZE = 4


class GrinchRamData(NamedTuple):
    """A Representation of an update to RAM data for The Grinch.

    ram_address (int): The RAM address that we are updating, usually passed in with hex, representation (0x11111111)
    value (int; Optional): The value we are using to set, add, or subtract from the RAM Address Value. Defaults to 1 if binary_bit_pos is passed in
    binary_bit_pos: (int; Optional): If passed in, we are looking for a specific bit within the byte of the ram_address. This is represented as a small-endian bit position, meaning the right-most bit is 0, and the left-most bit is 7
    byte_size: (int: Default: 1): The size of the RAM Address address we are looking for.
    update_method (UpdateMethod; Default: SET): Determines what we are doing to the RAM Address. We can either SET the address, simply assigning a value. We can ADD or SUBTRACT, modifying hte existing value by a set amount. And we can FREEZE the address, preventing it from updating in the future
    min_count: The minimum amount that a value can go down to using SUBTRACT
    max_count: The maximum amount that a value can go down to using ADD
    """

    ram_address: int
    value: Optional[int] = None  # none is empty/null
    # Either set or add either hex or unsigned values through Client.py
    # Hex uses 0x00, unsigned are base whole numbers
    binary_bit_pos: Optional[int] = None
    byte_size: int = 1
    update_method: UpdateMethod = UpdateMethod.SET
    min_count: int = 0
    max_count: int = 255

    def __init__(
        self,
        ram_address: int,
        value: Optional[int],
        byte_size: int,
        update_method: UpdateMethod,
        min_count: int,
        max_count: int,
    ):
        self.ram_address = ram_address

        if value:
            self.value = value
        else:
            self.value = 1

        if byte_size:
            self.byte_size = byte_size

        if update_method:
            self.update_method = update_method

        if min_count and min_count > -1:
            self.min_count = min_count

        if max_count and max_count > -1:
            self.max_count = max_count
        elif max_count and max_count > ((2 ** (self.byte_size * 8)) - 1):
            raise ValueError(
                "max_count cannot be larger than the RAM addresses max possible value"
            )
        else:
            self.max_count = (2 ** (self.byte_size * 8)) - 1
