# -*- coding: utf-8 -*-

# Read more about proc and memory mapping here:
# https://man7.org/linux/man-pages/man5/proc.5.html

# Read more about iovec here:
# https://man7.org/linux/man-pages/man3/iovec.3type.html

from ctypes import Structure, c_char_p, c_size_t, c_uint, c_void_p


class MEMORY_BASIC_INFORMATION(Structure):
    _fields_ = [
        ("BaseAddress", c_uint),
        ("RegionSize", c_uint),
        ("Privileges", c_char_p),
        ("Offset", c_uint),
        ("MajorID", c_uint),
        ("MinorID", c_uint),
        ("InodeID", c_uint),
        ("Path", c_char_p),
    ]


class iovec(Structure):
    """
    Describes a region of memory, beginning at iov_base address and
    with the size of iov_len bytes.  System calls use arrays of this
    structure, where each element of the array represents a memory
    region, and the whole array represents a vector of memory
    regions. The maximum number of iovec structures in that array is
    limited by IOV_MAX (defined in <limits.h>, or accessible via the
    call sysconf(_SC_IOV_MAX)).

    Reference: https://man7.org/linux/man-pages/man3/iovec.3type.html
    """
    _fields_ = [
        ("iov_base", c_void_p),
        ("iov_len", c_size_t)
    ]
