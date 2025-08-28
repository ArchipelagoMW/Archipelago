# -*- coding: utf-8 -*-

# Read more about process_vm_(read/write)v here:
# https://man7.org/linux/man-pages/man2/process_vm_readv.2.html

# Read more about proc and memory mapping here:
# https://man7.org/linux/man-pages/man5/proc.5.html

from ctypes import addressof, sizeof
from typing import Dict, Generator, Optional, Sequence, Tuple, Type, TypeVar, Union

from ..enums import ScanTypesEnum
from ..util import convert_from_byte_array, get_c_type_of, scan_memory, scan_memory_for_exact_value
from .ptrace import libc
from .types import MEMORY_BASIC_INFORMATION, iovec

import ctypes


T = TypeVar("T")


def get_memory_regions(pid: int) -> Generator[dict, None, None]:
    """
    Generates dictionaries with the address and size of a region used by the process.
    """
    mapping_filename = "/proc/{}/maps".format(pid)

    with open(mapping_filename, "r") as mapping_file:
        for line in mapping_file:

            # Each line keeps information about a memory region of the process.
            region_information = line.split()

            addressing_range, privileges, offset, device, inode = region_information[0: 5]
            path = region_information[5] if len(region_information) >= 6 else str()

            # Convert hexadecimal values to decimal.
            start_address, end_address = [int(addr, 16) for addr in addressing_range.split("-")]
            major_id, minor_id = [int(_id, 16) for _id in device.split(":")]

            offset = int(offset, 16)
            inode = int(inode, 16)

            # Calculate the region size.
            size = end_address - start_address

            region = MEMORY_BASIC_INFORMATION(start_address, size, privileges.encode(), offset, major_id, minor_id, inode, path.encode())
            yield {"address": start_address, "size": region.RegionSize, "struct": region}


def read_process_memory(
    pid: int,
    address: int,
    pytype: Type[T],
    bufflength: int
) -> T:
    """
    Return a value from a memory address.
    """
    if pytype not in [bool, int, float, str, bytes]:
        raise ValueError("The type must be bool, int, float, str or bytes.")

    data = get_c_type_of(pytype, bufflength)

    libc.process_vm_readv(
        pid, (iovec * 1)(iovec(addressof(data), sizeof(data))),
        1, (iovec * 1)(iovec(address, sizeof(data))), 1, 0
    )

    if pytype is str:
        return bytes(data).decode()
    elif pytype is bytes:
        return bytes(data)
    else:
        return data.value


def search_addresses_by_value(
    pid: int,
    pytype: Type[T],
    bufflength: int,
    value: Union[bool, int, float, str, bytes, tuple],
    scan_type: ScanTypesEnum = ScanTypesEnum.EXACT_VALUE,
    progress_information: bool = False,
    writeable_only: bool = False,
) -> Generator[Union[int, Tuple[int, dict]], None, None]:
    """
    Search the whole memory space, accessible to the process,
    for the provided value, returning the found addresses.
    """
    if pytype not in [bool, int, float, str, bytes]:
        raise ValueError("The type must be bool, int, float, str or bytes.")

    # Convert the target value, or all values of a tuple, as bytes.
    target_values = value if isinstance(value, tuple) else (value,)

    conversion_buffer = list()

    for v in target_values:
        target_value = get_c_type_of(pytype, bufflength)
        target_value.value = v.encode() if isinstance(v, str) else v

        target_value_bytes = ctypes.cast(ctypes.byref(target_value), ctypes.POINTER(ctypes.c_byte * bufflength))
        conversion_buffer.append(bytes(target_value_bytes.contents))

    target_value_bytes = tuple(conversion_buffer) if isinstance(value, tuple) else conversion_buffer[0]

    checked_memory_size = 0
    memory_total = 0
    memory_regions = list()

    # Get the memory regions, computing the total amount of memory to be scanned.
    for region in get_memory_regions(pid):

        # Only readable memory pages.
        if b"r" not in region["struct"].Privileges: continue

        # If writeable_only is True, checks if the memory page is writeable.
        if writeable_only and b"w" not in region["struct"].Privileges: continue

        memory_total += region["size"]
        memory_regions.append(region)

    # Sort the list to return ordered addresses.
    memory_regions.sort(key=lambda region: region["address"])

    # Check each memory region used by the process.
    for region in memory_regions:
        address, size = region["address"], region["size"]
        region_data = (ctypes.c_byte * size)()

        # Get data from the region.
        libc.process_vm_readv(
            pid, (iovec * 1)(iovec(addressof(region_data), sizeof(region_data))),
            1, (iovec * 1)(iovec(address, sizeof(region_data))), 1, 0
        )

        # Choose the searching method.
        searching_method = scan_memory

        if scan_type in [ScanTypesEnum.EXACT_VALUE, ScanTypesEnum.NOT_EXACT_VALUE]:
            searching_method = scan_memory_for_exact_value

        # Search the value and return the found addresses.
        for offset in searching_method(region_data, size, target_value_bytes, bufflength, scan_type, pytype is str):
            found_address = address + offset

            extra_information = {
                "memory_total": memory_total,
                "progress": (checked_memory_size + offset) / memory_total,
            }
            yield (found_address, extra_information) if progress_information else found_address

        # Compute the region size to the checked memory size.
        checked_memory_size += size


def search_values_by_addresses(
    pid: int,
    pytype: Type[T],
    bufflength: int,
    addresses: Sequence[int],
    *,
    memory_regions: Optional[Sequence[Dict]] = None,
    raise_error: bool = False,
) -> Generator[Tuple[int, Optional[T]], None, None]:
    """
    Search the whole memory space, accessible to the process,
    for the provided list of addresses, returning their values.
    """
    if pytype not in [bool, int, float, str, bytes]:
        raise ValueError("The type must be bool, int, float, str or bytes.")

    memory_regions = list(memory_regions) if memory_regions else list()
    addresses = sorted(addresses)

    # If no memory page has been given, get all readable memory pages.
    if not memory_regions:
        for region in get_memory_regions(pid):
            if b"r" not in region["struct"].Privileges: continue
            memory_regions.append(region)

    memory_regions.sort(key=lambda region: region["address"])
    address_index = 0

    # Walk by each memory region.
    for region in memory_regions:
        if address_index >= len(addresses): break

        target_address = addresses[address_index]

        # Check if the memory region contains the target address.
        base_address, size = region["address"], region["size"]
        if not (base_address <= target_address < base_address + size): continue

        region_data = (ctypes.c_byte * size)()

        # Get data from the region.
        libc.process_vm_readv(
            pid, (iovec * 1)(iovec(addressof(region_data), sizeof(region_data))),
            1, (iovec * 1)(iovec(base_address, sizeof(region_data))), 1, 0
        )

        # Get the value of each address.
        while base_address <= target_address < base_address + size:
            offset = target_address - base_address
            address_index += 1

            try:
                data = region_data[offset: offset + bufflength]
                data = (ctypes.c_byte * bufflength)(*data)
                yield target_address, convert_from_byte_array(data, pytype, bufflength)

            except Exception as error:
                if raise_error: raise error
                yield target_address, None

            if address_index >= len(addresses): break
            target_address = addresses[address_index]


def write_process_memory(
    pid: int,
    address: int,
    pytype: Type[T],
    bufflength: int,
    value: Union[bool, int, float, str, bytes]
) -> T:
    """
    Write a value to a memory address.
    """
    if pytype not in [bool, int, float, str, bytes]:
        raise ValueError("The type must be bool, int, float, str or bytes.")

    data = get_c_type_of(pytype, bufflength)
    data.value = value.encode() if isinstance(value, str) else value

    libc.process_vm_writev(
        pid, (iovec * 1)(iovec(addressof(data), sizeof(data))),
        1, (iovec * 1)(iovec(address, sizeof(data))), 1, 0
    )
    return value
