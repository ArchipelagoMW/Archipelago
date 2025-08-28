# -*- coding: utf-8 -*-
from enum import Enum


class MemoryTypesEnum(Enum):
    """
    Enum with all types of a memory page.
    """
    # Indicates that the memory pages within the region are mapped into the view of an image section.
    MEM_IMAGE = 0x1000000

    # Indicates that the memory pages within the region are mapped into the view of a section.
    MEM_MAPPED = 0x40000

    # Indicates that the memory pages within the region are private (that is, not shared by other processes).
    MEM_PRIVATE = 0x20000
