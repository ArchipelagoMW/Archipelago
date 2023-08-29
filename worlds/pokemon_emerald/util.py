from typing import List

from .data import data


def location_name_to_label(name: str) -> str:
    return data.locations[name].label


def int_to_bool_array(num: int) -> List[bool]:
    binary_string = format(num, '064b')
    bool_array = [bit == '1' for bit in reversed(binary_string)]
    return bool_array


def bool_array_to_int(bool_array: List[bool]) -> int:
    binary_string = ''.join(['1' if bit else '0' for bit in reversed(bool_array)])
    num = int(binary_string, 2)
    return num
