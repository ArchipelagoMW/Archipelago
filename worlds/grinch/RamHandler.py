from enum import STRICT, IntEnum
from typing import Optional


class UpdateMethod(IntEnum, boundary=STRICT):
    SET = 1
    ADD = 2
    SUBTRACT = 3
    FREEZE = 4  # Currently Non-functional


class GrinchRamData:
    """A Representation of an update to RAM data for The Grinch.

    ram_address (int): The RAM address that we are updating, usually passed in with hex, representation (0x11111111)
    value (int; Optional): The value we are using to set, add, or subtract from the RAM Address Value. Defaults to 1 if binary_bit_pos is passed in
    binary_bit_pos: (int; Optional): If passed in, we are looking for a specific bit within the byte of the ram_address. This is represented as a small-endian bit position, meaning the right-most bit is 0, and the left-most bit is 7
    byte_size: (int: Default: 1): The size of the RAM Address address we are looking for.
    update_method (UpdateMethod; Default: SET): Determines what we are doing to the RAM Address. We can either SET the address, simply assigning a value. We can ADD or SUBTRACT, modifying the existing value by a set amount. And we can FREEZE the address, preventing it from updating in the future
    min_count: The minimum amount that a value can go down to using SUBTRACT
    max_count: The maximum amount that a value can go down to using ADD
    """

    ram_address: int
    value: Optional[int] = None  # none is empty/null
    binary_bit_pos: Optional[int] = None
    byte_size: int = 1
    endian = "little"
    update_method: UpdateMethod = UpdateMethod.SET
    min_count: int = 0
    max_count: int = 255
    ram_area = "MainRAM"

    def __init__(
        self,
        ram_address: int,
        value: Optional[int] = None,
        binary_bit_pos: int = -1,
        byte_size: int = 1,
        update_method: UpdateMethod = UpdateMethod.SET,
        min_count: int = -1,
        max_count: int = -1,
        endian: str = "little",
        ram_area: str = "MainRAM",
    ):
        self.ram_address = ram_address

        if value:
            self.value = value
        else:
            self.value = 1

        if binary_bit_pos > -1:
            self.binary_bit_pos = binary_bit_pos

        if byte_size > 0:
            self.byte_size = byte_size

        if update_method:
            self.update_method = update_method

        if min_count and min_count > -1:
            self.min_count = min_count

        if max_count and max_count > -1:
            self.max_count = max_count
        elif max_count and max_count > ((2 ** (self.byte_size * 8)) - 1):
            raise ValueError("max_count cannot be larger than the RAM addresses max possible value")
        else:
            self.max_count = (2 ** (self.byte_size * 8)) - 1

        self.endian = endian
        self.ram_area = ram_area

        # Error Handling
        if self.value and self.value > self.max_count:
            raise ValueError(
                f"Value passed in is greater than max_count.\n\nRAM Address: {self.ram_address}\nValue: {self.value}\nMax Count: {self.max_count}"
            )

        if self.value and self.value < self.min_count:
            raise ValueError(
                f"Value passed in is lower than min_count.\n\nRAM Address: {self.ram_address}\nValue: {self.value}\nMin Count: {self.max_count}"
            )

        if self.binary_bit_pos and self.update_method not in [UpdateMethod.SET, UpdateMethod.FREEZE]:
            raise ValueError(f"binary_bit_position can only be passed in if update_method is SET or FREEZE")

        if self.binary_bit_pos and self.value not in [0, 1]:
            raise ValueError(f"value must be 0 or 1 if using binary_bit_position")
