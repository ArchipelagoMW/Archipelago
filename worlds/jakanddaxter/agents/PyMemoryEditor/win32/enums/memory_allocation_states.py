# -*- coding: utf-8 -*-
from enum import Enum


class MemoryAllocationStatesEnum(Enum):
    """
    Enum with all states of a memory page allocation.
    """
    # Indicates committed pages for which physical storage has been allocated,
    # either in memory or in the paging file on disk.
    MEM_COMMIT = 0x1000

    # Indicates free pages not accessible to the calling process and available
    # to be allocated. For free pages, the information in the AllocationBase,
    # AllocationProtect, Protect, and Type members is undefined.
    MEM_FREE = 0x10000

    # Allocates memory using large page support. The size and alignment must be a multiple
    # of the large-page minimum. To obtain this value, use the GetLargePageMinimum function.
    # If you specify this value, you must also specify MEM_RESERVE and MEM_COMMIT.
    MEM_LARGE_PAGES = 0x20000000

    # Reserves an address range that can be used to map Address Windowing Extensions (AWE) pages.
    # This value must be used with MEM_RESERVE and no other values.
    MEM_PHYSICAL = 0x00400000

    # Allocates memory at the highest possible address. This can be slower than regular
    # allocations, especially when there are many allocations.
    MEM_TOP_DOWN = 0x00100000

    # Indicates reserved pages where a range of the process's virtual address
    # space is reserved without any physical storage being allocated. For reserved
    # pages, the information in the Protect member is undefined.
    MEM_RESERVE = 0x2000

    # Indicates that data in the memory range is no longer of interest. The pages
    # should not be read from or written to the paging file. However, the memory
    # block will be used again later, so it should not be decommitted. This value
    # cannot be used with any other value.
    MEM_RESET = 0x00080000

    # MEM_RESET_UNDO should only be called on an address range to which MEM_RESET
    # was successfully applied earlier. It indicates that the data in the specified
    # memory range specified by lpAddress and dwSize is of interest to the caller
    # and attempts to reverse the effects of MEM_RESET. If the function succeeds,
    # that means all data in the specified address range is intact. If the function
    # fails, at least some of the data in the address range has been replaced with
    # zeroes. This value cannot be used with any other value.
    MEM_RESET_UNDO = 0x1000000
