# -*- coding: utf-8 -*-

# Read more about operations with processes by ptrace system call here:
# https://man7.org/linux/man-pages/man2/ptrace.2.html
# https://refspecs.linuxbase.org/LSB_5.0.0/LSB-Core-generic/LSB-Core-generic/baselib-ptrace-1.html
# ...

from .enums import PtraceCommandsEnum

from ctypes.util import find_library
import ctypes

libc = ctypes.CDLL(find_library("c"), use_errno=True)
libc.ptrace.argtypes = (ctypes.c_ulong,) * 4
libc.ptrace.restype = ctypes.c_long


def ptrace(command: PtraceCommandsEnum, pid: int, *args: int) -> int:
    """
    Run ptrace() system call with the provided command, pid and arguments.
    """
    result = libc.ptrace(command.value, pid, *args)

    if result == -1:
        error_no = ctypes.get_errno()

        if error_no:
            error_msg = ctypes.string_at(libc.strerror(error_no))
            raise OSError(error_msg)

    return result
