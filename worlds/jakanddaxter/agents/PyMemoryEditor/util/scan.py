# -*- coding: utf-8 -*-

from ..enums import ScanTypesEnum
from .search.kmp import KMPSearch

from typing import Generator, Sequence, Tuple, Union
import ctypes
import sys


def scan_memory_for_exact_value(
    memory_region_data: Sequence,
    memory_region_data_size: int,
    target_value: bytes,
    target_value_size: int,
    comparison: ScanTypesEnum = ScanTypesEnum.EXACT_VALUE,
    *args, **kwargs
) -> Generator[int, None, None]:
    """
    Search for an exact value at the memory region.

    This method uses an efficient searching algorithm.
    """
    searcher = KMPSearch(target_value, target_value_size)
    last_index = 0

    for found_index in searcher.search(memory_region_data, memory_region_data_size):

        # Return the found index if user is searching for an exact value.
        if comparison is ScanTypesEnum.EXACT_VALUE:
            yield found_index
            continue

        # Return the interval between last_index and found_address, if user is searching for a different value.
        for different_index in range(last_index, found_index):
            yield different_index
        last_index = found_index + 1

    # If user is searching for a different value, return the rest of the addresses that were not found.
    if comparison is ScanTypesEnum.NOT_EXACT_VALUE:
        for different_index in range(last_index, memory_region_data_size):
            yield different_index


def scan_memory(
    memory_region_data: Sequence,
    memory_region_data_size: int,
    target_value: Union[bytes, Tuple[bytes]],
    target_value_size: int,
    scan_type: ScanTypesEnum,
    is_string: bool,
) -> Generator[int, None, None]:
    """
    Search for a value at the memory region.
    """
    byte_order = sys.byteorder if not is_string else "big"

    # If target_value is a tuple, it means the user wants to compare to more than one value.
    if isinstance(target_value, tuple):
        start_target_value_int = int.from_bytes(target_value[0], byte_order)
        end_target_value_int = int.from_bytes(target_value[1], byte_order)
    else: target_value_int = int.from_bytes(target_value, byte_order)

    for found_index in range(memory_region_data_size - target_value_size):

        # Convert data to an integer.
        data = memory_region_data[found_index: found_index + target_value_size]
        data = bytes((ctypes.c_byte * target_value_size)(*data))
        data = int.from_bytes(data, byte_order)

        # Compare value between.
        if scan_type is ScanTypesEnum.VALUE_BETWEEN and (start_target_value_int > data or data > end_target_value_int): continue
        elif scan_type is ScanTypesEnum.NOT_VALUE_BETWEEN and (start_target_value_int < data < end_target_value_int): continue

        # Compare the value.
        elif scan_type is ScanTypesEnum.EXACT_VALUE and data != target_value_int: continue
        elif scan_type is ScanTypesEnum.NOT_EXACT_VALUE and data == target_value_int: continue
        elif scan_type is ScanTypesEnum.BIGGER_THAN and data <= target_value_int: continue
        elif scan_type is ScanTypesEnum.SMALLER_THAN and data >= target_value_int: continue
        elif scan_type is ScanTypesEnum.BIGGER_THAN_OR_EXACT_VALUE and data < target_value_int: continue
        elif scan_type is ScanTypesEnum.SMALLER_THAN_OR_EXACT_VALUE and data > target_value_int: continue

        yield found_index
