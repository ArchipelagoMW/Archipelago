"""Library functions to convert data from one type to another."""

import struct
from typing import Union


def float_to_hex(f: Union[float, int]) -> str:
    """Convert float to hex."""
    if f == 0:
        return "0x00000000"
    return hex(struct.unpack("<I", struct.pack("<f", f))[0])


def short_to_ushort(short: int) -> int:
    """Convert short to unsigned short format."""
    if short < 0:
        return short + 65536
    return short


def intf_to_float(intf: int) -> float:
    """Convert float as int format to float."""
    if intf == 0:
        return 0
    else:
        return struct.unpack("!f", bytes.fromhex("{:08X}".format(intf)))[0]


def ushort_to_short(ushort):
    """Convert unsigned short to signed short."""
    if ushort > 32767:
        return ushort - 65536
    return ushort


def int_to_list(num: int, size: int):
    """Convert an integer to a list."""
    arr = [0] * size
    for a in range(size):
        slot = (size - 1) - a
        val = num % 256
        num = int((num - val) / 256)
        arr[slot] = val
    return arr


def arr_to_value(arr: bytearray, offset: int, size: int) -> int:
    """Read value from bytearray and convert it to a value."""
    value = 0
    for x in range(size):
        value <<= 8
        value += arr[offset + x]
    return value
