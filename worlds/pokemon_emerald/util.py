import math
from typing import Tuple

from .data import data


def location_name_to_label(name: str) -> str:
    return data.locations[name].label


def int_to_bool_array(num):
    binary_string = format(num, '064b')
    bool_array = [bit == '1' for bit in reversed(binary_string)]
    return bool_array


def bool_array_to_int(bool_array):
    binary_string = ''.join(['1' if bit else '0' for bit in reversed(bool_array)])
    num = int(binary_string, 2)
    return num


def get_easter_egg(easter_egg: str) -> Tuple[int, int]:
    result1 = 0
    result2 = 0
    for c in easter_egg:
        result1 = ((result1 << 5) - result1 + ord(c)) & 0xFFFFFFFF
        result2 = ((result2 << 4) - result2 + ord(c)) & 0xFF

    if result1 == 0x2FFF9742:
        if result2 < 252:
            return (1, result2)
    elif result1 == 0x911BAF95:
        return (2, (result1 & result2) - 31)
    elif result1 == 0x91AD33AD:
        return (3, (result2 - 212) & 0xFF)
    return (0, 0)
