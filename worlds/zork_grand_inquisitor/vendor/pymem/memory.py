import ctypes
import struct

import pymem.exception
import pymem.ressources.kernel32
import pymem.ressources.structure


def allocate_memory(handle, size, allocation_type=None, protection_type=None):
    """Reserves or commits a region of memory within the virtual address space of a specified process.
    The function initializes the memory it allocates to zero, unless MEM_RESET is used.

    https://msdn.microsoft.com/en-us/library/windows/desktop/aa366890%28v=vs.85%29.aspx

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    size: int
        The size of the region of memory to allocate, in bytes.
    allocation_type: MEMORY_STATE
        The type of memory allocation.
    protection_type: MEMORY_PROTECTION
        The memory protection for the region of pages to be allocated.

    Returns
    -------
    int
        The address of the allocated region of pages.
    """
    if not allocation_type:
        allocation_type = pymem.ressources.structure.MEMORY_STATE.MEM_COMMIT.value
    if not protection_type:
        protection_type = pymem.ressources.structure.MEMORY_PROTECTION.PAGE_EXECUTE_READWRITE.value
    pymem.ressources.kernel32.SetLastError(0)
    address = pymem.ressources.kernel32.VirtualAllocEx(handle, None, size, allocation_type, protection_type)
    return address


def free_memory(handle, address, free_type=None):
    """Releases, decommits, or releases and decommits a region of memory within the virtual address space of a specified
    process.

    https://msdn.microsoft.com/en-us/library/windows/desktop/aa366894%28v=vs.85%29.aspx

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of memory to be freed.
    free_type: MEMORY_PROTECTION
        The type of free operation.

    Returns
    -------
    int
        A boolean indicating if the call was a success.
    """
    if not free_type:
        free_type = pymem.ressources.structure.MEMORY_STATE.MEM_RELEASE
    pymem.ressources.kernel32.SetLastError(0)
    ret = pymem.ressources.kernel32.VirtualFreeEx(handle, address, 0, free_type)
    return ret


def read_bytes(handle, address, byte):
    """Reads data from an area of memory in a specified process.
    The entire area to be read must be accessible or the operation fails.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms680553%28v=vs.85%29.aspx

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of memory to be read.
    byte: int
        Number of bytes to be read

    Raises
    ------
    TypeError
        If address is not a valid integer
    WinAPIError
        If ReadProcessMemory failed

    Returns
    -------
    bytes
        The raw value read as bytes
    """
    return read_ctype(handle, address, (byte * ctypes.c_char)(), get_py_value=False).raw


def read_ctype(handle, address, ctype, *, get_py_value=True, raw_bytes=False):
    """
    Read a ctype basic type or structure from <address>

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of memory to be read.
    ctype:
        A simple ctypes type or structure
    get_py_value: bool
        If the corrosponding python type should be used instead of returning the ctype
        This is automatically set to False for ctypes.Structure or ctypes.Array instances
    raw_bytes: bool
        If we should return the raw ctype bytes

    Raises
    ------
    WinAPIError
        If ReadProcessMemory failed

    Returns
    -------
    Any
        Return will be either the ctype with the read value if get_py_value is false or
        the corropsonding python type
    """
    if raw_bytes:
        return read_bytes(handle, address, ctypes.sizeof(ctype))

    if isinstance(ctype, (ctypes.Structure, ctypes.Array)):
        get_py_value = False

    pymem.ressources.kernel32.SetLastError(0)

    result = pymem.ressources.kernel32.ReadProcessMemory(
        handle,
        ctypes.c_void_p(address),
        ctypes.byref(ctype),
        ctypes.sizeof(ctype),
        None,
    )

    if result == 0:
        error_code = ctypes.windll.kernel32.GetLastError()
        raise pymem.exception.WinAPIError(error_code)

    if get_py_value:
        return ctype.value

    return ctype


def read_bool(handle, address):
    """Reads 1 byte from an area of memory in a specified process.
    The entire area to be read must be accessible or the operation fails.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms680553%28v=vs.85%29.aspx

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of memory to be read.

    Raises
    ------
    TypeError
        If address is not a valid integer
    WinAPIError
        If ReadProcessMemory failed

    Returns
    -------
    bool
        The raw value read as a bool
    """
    return read_ctype(handle, address, ctypes.c_bool())


def read_char(handle, address):
    """Reads 1 byte from an area of memory in a specified process.
    The entire area to be read must be accessible or the operation fails.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms680553%28v=vs.85%29.aspx

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of memory to be read.

    Raises
    ------
    TypeError
        If address is not a valid integer
    WinAPIError
        If ReadProcessMemory failed

    Returns
    -------
    str
        The raw value read as a string
    """
    return read_ctype(handle, address, ctypes.c_char()).decode()


def read_uchar(handle, address):
    """Reads 1 byte from an area of memory in a specified process.
    The entire area to be read must be accessible or the operation fails.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms680553%28v=vs.85%29.aspx

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of memory to be read.

    Raises
    ------
    TypeError
        If address is not a valid integer
    WinAPIError
        If ReadProcessMemory failed

    Returns
    -------
    int
        The raw value read as an int
    """
    return read_ctype(handle, address, ctypes.c_ubyte())


def read_short(handle, address):
    """Reads 2 byte from an area of memory in a specified process.
    The entire area to be read must be accessible or the operation fails.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms680553%28v=vs.85%29.aspx

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of memory to be read.

    Raises
    ------
    TypeError
        If address is not a valid integer
    WinAPIError
        If ReadProcessMemory failed

    Returns
    -------
    int
        The raw value read as an int
    """
    return read_ctype(handle, address, ctypes.c_short())


def read_ushort(handle, address):
    """Reads 2 byte from an area of memory in a specified process.
    The entire area to be read must be accessible or the operation fails.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms680553%28v=vs.85%29.aspx

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of memory to be read.

    Raises
    ------
    TypeError
        If address is not a valid integer
    WinAPIError
        If ReadProcessMemory failed

    Returns
    -------
    int
        The raw value read as an int
    """
    return read_ctype(handle, address, ctypes.c_ushort())


def read_int(handle, address):
    """Reads 4 byte from an area of memory in a specified process.
    The entire area to be read must be accessible or the operation fails.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms680553%28v=vs.85%29.aspx

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of memory to be read.

    Raises
    ------
    TypeError
        If address is not a valid integer
    WinAPIError
        If ReadProcessMemory failed

    Returns
    -------
    int
        The raw value read as an int
    """
    return read_ctype(handle, address, ctypes.c_int())


def read_uint(handle, address, is_64=False):
    """Reads 4 byte from an area of memory in a specified process.
    The entire area to be read must be accessible or the operation fails.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms680553%28v=vs.85%29.aspx

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of memory to be read.
    is_64: bool
        Should we unpack as big-endian

    Raises
    ------
    TypeError
        If address is not a valid integer
    WinAPIError
        If ReadProcessMemory failed

    Returns
    -------
    int
        The raw value read as an int
    """
    if not is_64:
        return read_ctype(handle, address, ctypes.c_uint())

    # should this just be c_uint64? the doc string says to read as big-endian
    raw = read_bytes(handle, address, struct.calcsize('I'))
    return struct.unpack('>I', raw)[0]


def read_float(handle, address):
    """Reads 4 byte from an area of memory in a specified process.
    The entire area to be read must be accessible or the operation fails.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms680553%28v=vs.85%29.aspx

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of memory to be read.

    Raises
    ------
    TypeError
        If address is not a valid integer
    WinAPIError
        If ReadProcessMemory failed

    Returns
    -------
    float
        The raw value read as a float
    """
    return read_ctype(handle, address, ctypes.c_float())


def read_long(handle, address):
    """Reads 4 byte from an area of memory in a specified process.
    The entire area to be read must be accessible or the operation fails.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms680553%28v=vs.85%29.aspx

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of memory to be read.

    Raises
    ------
    TypeError
        If address is not a valid integer
    WinAPIError
        If ReadProcessMemory failed

    Returns
    -------
    int
        The raw value read as an int
    """
    return read_ctype(handle, address, ctypes.c_long())


def read_ulong(handle, address):
    """Reads 4 byte from an area of memory in a specified process.
    The entire area to be read must be accessible or the operation fails.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms680553%28v=vs.85%29.aspx

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of memory to be read.

    Raises
    ------
    TypeError
        If address is not a valid integer
    WinAPIError
        If ReadProcessMemory failed

    Returns
    -------
    int
        The raw value read as an int
    """
    return read_ctype(handle, address, ctypes.c_ulong())


def read_longlong(handle, address):
    """Reads 8 byte from an area of memory in a specified process.
    The entire area to be read must be accessible or the operation fails.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms680553%28v=vs.85%29.aspx

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of memory to be read.

    Raises
    ------
    TypeError
        If address is not a valid integer
    WinAPIError
        If ReadProcessMemory failed

    Returns
    -------
    int
        The raw value read as an int
    """
    return read_ctype(handle, address, ctypes.c_longlong())


def read_ulonglong(handle, address):
    """Reads 8 byte from an area of memory in a specified process.
    The entire area to be read must be accessible or the operation fails.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms680553%28v=vs.85%29.aspx

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of memory to be read.

    Raises
    ------
    TypeError
        If address is not a valid integer
    WinAPIError
        If ReadProcessMemory failed

    Returns
    -------
    int
        The raw value read as an int
    """
    return read_ctype(handle, address, ctypes.c_ulonglong())


def read_double(handle, address):
    """Reads 8 byte from an area of memory in a specified process.
    The entire area to be read must be accessible or the operation fails.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms680553%28v=vs.85%29.aspx

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of memory to be read.

    Raises
    ------
    TypeError
        If address is not a valid integer
    WinAPIError
        If ReadProcessMemory failed

    Returns
    -------
    float
        The raw value read as a float
    """
    return read_ctype(handle, address, ctypes.c_double())


def read_string(handle, address, byte=50):
    """Reads n `byte` from an area of memory in a specified process.
    The entire area to be read must be accessible or the operation fails.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms680553%28v=vs.85%29.aspx

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of memory to be read.
    byte: int, default=50
        max number of bytes to check for null terminator, defaults to 50

    Raises
    ------
    TypeError
        If address is not a valid integer
    WinAPIError
        If ReadProcessMemory failed

    Returns
    -------
    str
        The raw value read as a string
    """
    buff = read_bytes(handle, address, byte)
    i = buff.find(b'\x00')
    if i != -1:
        buff = buff[:i]
    buff = buff.decode()
    return buff


def write_bytes(handle, address, data, length):
    """Writes data to an area of memory in a specified process.
    The entire area to be written to must be accessible or the operation fails.

    Casts address using ctypes.c_char_p.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms681674%28v=vs.85%29.aspx

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of memory to be written.
    data: void
        A buffer that contains data to be written
    length: int
        Number of bytes to be written.

    Raises
    ------
    TypeError
        If address is not a valid integer
    WinAPIError
        if WriteProcessMemory failed

    Returns
    -------
    bool
        A boolean indicating a successful write.
    """
    buffer = (length * ctypes.c_char)()
    buffer.value = data
    return write_ctype(handle, address, buffer)


def write_ctype(handle, address, ctype):
    """
    Write a ctype basic type or structure to <address>

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of memory to be written.
    ctype:
        A simple ctypes type or structure

    Raises
    ------
    WinAPIError
        If WriteProcessMemory failed

    Returns
    -------
    bool
        A boolean indicating a successful write.
    """
    pymem.ressources.kernel32.SetLastError(0)

    result = pymem.ressources.kernel32.WriteProcessMemory(
        handle,
        ctypes.cast(address, ctypes.c_void_p),
        ctypes.cast(ctypes.byref(ctype), ctypes.c_void_p),
        ctypes.sizeof(ctype),
        None
    )

    if result == 0:
        error_code = ctypes.windll.kernel32.GetLastError()
        raise pymem.exception.WinAPIError(error_code)

    # TODO: remove in next breaking change
    # there isn't much point in returning this as it will always be true/1 (error raised otherwise)
    return result


def write_bool(handle, address, value):
    """Writes 1 byte to an area of memory in a specified process.
    The entire area to be written to must be accessible or the operation fails.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms681674%28v=vs.85%29.aspx

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of memory to be written.
    value: bool
        A boolean representing the value to be written

    Raises
    ------
    TypeError
        If address is not a valid integer
    WinAPIError
        if WriteProcessMemory failed

    Returns
    -------
    bool
        A boolean indicating a successful write.
    """
    return write_ctype(handle, address, ctypes.c_bool(value))


def write_char(handle, address, value):
    """Writes 1 byte to an area of memory in a specified process.
    The entire area to be written to must be accessible or the operation fails.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms681674%28v=vs.85%29.aspx

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of memory to be written.
    value: str
        A buffer that contains data to be written

    Raises
    ------
    TypeError
        If address is not a valid integer
    WinAPIError
        if WriteProcessMemory failed

    Returns
    -------
    bool
        A boolean indicating a successful write.
    """
    return write_ctype(handle, address, ctypes.c_char(value))


def write_uchar(handle, address, value):
    """Writes 1 byte to an area of memory in a specified process.
    The entire area to be written to must be accessible or the operation fails.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms681674%28v=vs.85%29.aspx

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of memory to be written.
    value: str
        A buffer that contains data to be written

    Raises
    ------
    TypeError
        If address is not a valid integer
    WinAPIError
        if WriteProcessMemory failed

    Returns
    -------
    bool
        A boolean indicating a successful write.
    """
    return write_ctype(handle, address, ctypes.c_ubyte(value))


def write_short(handle, address, value):
    """Writes 2 bytes to an area of memory in a specified process.
    The entire area to be written to must be accessible or the operation fails.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms681674%28v=vs.85%29.aspx

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of memory to be written.
    value: int
        A buffer that contains data to be written

    Raises
    ------
    TypeError
        If address is not a valid integer
    WinAPIError
        if WriteProcessMemory failed

    Returns
    -------
    bool
        A boolean indicating a successful write.
    """
    return write_ctype(handle, address, ctypes.c_short(value))


def write_ushort(handle, address, value):
    """Writes 2 bytes to an area of memory in a specified process.
    The entire area to be written to must be accessible or the operation fails.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms681674%28v=vs.85%29.aspx

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of memory to be written.
    value: int
        A buffer that contains data to be written

    Raises
    ------
    TypeError
        If address is not a valid integer
    WinAPIError
        if WriteProcessMemory failed

    Returns
    -------
    bool
        A boolean indicating a successful write.
    """
    return write_ctype(handle, address, ctypes.c_ushort(value))


def write_int(handle, address, value):
    """Writes 4 bytes to an area of memory in a specified process.
    The entire area to be written to must be accessible or the operation fails.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms681674%28v=vs.85%29.aspx

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of memory to be written.
    value: int
        A buffer that contains data to be written

    Raises
    ------
    TypeError
        If address is not a valid integer
    WinAPIError
        if WriteProcessMemory failed

    Returns
    -------
    bool
        A boolean indicating a successful write.
    """
    return write_ctype(handle, address, ctypes.c_int(value))


def write_uint(handle, address, value):
    """Writes 4 bytes to an area of memory in a specified process.
    The entire area to be written to must be accessible or the operation fails.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms681674%28v=vs.85%29.aspx

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of memory to be written.
    value: int
        A buffer that contains data to be written

    Raises
    ------
    TypeError
        If address is not a valid integer
    WinAPIError
        if WriteProcessMemory failed

    Returns
    -------
    bool
        A boolean indicating a successful write.
    """
    return write_ctype(handle, address, ctypes.c_uint(value))


def write_float(handle, address, value):
    """Writes 4 bytes to an area of memory in a specified process.
    The entire area to be written to must be accessible or the operation fails.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms681674%28v=vs.85%29.aspx

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of memory to be written.
    value: float
        A buffer that contains data to be written

    Raises
    ------
    TypeError
        If address is not a valid integer
    WinAPIError
        if WriteProcessMemory failed

    Returns
    -------
    bool
        A boolean indicating a successful write.
    """
    return write_ctype(handle, address, ctypes.c_float(value))


def write_long(handle, address, value):
    """Writes 4 bytes to an area of memory in a specified process.
    The entire area to be written to must be accessible or the operation fails.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms681674%28v=vs.85%29.aspx

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of memory to be written.
    value: int
        A buffer that contains data to be written

    Raises
    ------
    TypeError
        If address is not a valid integer
    WinAPIError
        if WriteProcessMemory failed

    Returns
    -------
    bool
        A boolean indicating a successful write.
    """
    return write_ctype(handle, address, ctypes.c_long(value))


def write_ulong(handle, address, value):
    """Writes 4 bytes to an area of memory in a specified process.
    The entire area to be written to must be accessible or the operation fails.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms681674%28v=vs.85%29.aspx

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of memory to be written.
    value: int
        A buffer that contains data to be written

    Raises
    ------
    TypeError
        If address is not a valid integer
    WinAPIError
        if WriteProcessMemory failed

    Returns
    -------
    bool
        A boolean indicating a successful write.
    """
    return write_ctype(handle, address, ctypes.c_ulong(value))


def write_longlong(handle, address, value):
    """Writes 8 bytes to an area of memory in a specified process.
    The entire area to be written to must be accessible or the operation fails.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms681674%28v=vs.85%29.aspx

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of memory to be written.
    value: int
        A buffer that contains data to be written

    Raises
    ------
    TypeError
        If address is not a valid integer
    WinAPIError
        if WriteProcessMemory failed

    Returns
    -------
    bool
        A boolean indicating a successful write.
    """
    return write_ctype(handle, address, ctypes.c_longlong(value))


def write_ulonglong(handle, address, value):
    """Writes 8 bytes to an area of memory in a specified process.
    The entire area to be written to must be accessible or the operation fails.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms681674%28v=vs.85%29.aspx

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of memory to be written.
    value: int
        A buffer that contains data to be written

    Raises
    ------
    TypeError
        If address is not a valid integer
    WinAPIError
        if WriteProcessMemory failed

    Returns
    -------
    bool
        A boolean indicating a successful write.
    """
    return write_ctype(handle, address, ctypes.c_ulonglong(value))


def write_double(handle, address, value):
    """Writes 8 bytes to an area of memory in a specified process.
    The entire area to be written to must be accessible or the operation fails.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms681674%28v=vs.85%29.aspx

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of memory to be written.
    value: float
        A buffer that contains data to be written

    Raises
    ------
    TypeError
        If address is not a valid integer
    WinAPIError
        if WriteProcessMemory failed

    Returns
    -------
    bool
        A boolean indicating a successful write.
    """
    return write_ctype(handle, address, ctypes.c_double(value))


def write_string(handle, address, bytecode):
    """Writes n `bytes` of len(`bytecode`) to an area of memory in a specified process.
    The entire area to be written to must be accessible or the operation fails.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms681674%28v=vs.85%29.aspx

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of memory to be written.
    bytecode: str, bytes
        A buffer that contains data to be written

    Raises
    ------
    TypeError
        If address is not a valid integer
    WinAPIError
        if WriteProcessMemory failed

    Returns
    -------
    bool
        A boolean indicating a successful write.
    """
    if isinstance(bytecode, str):
        bytecode = bytecode.encode()

    return write_bytes(handle, address, bytecode, len(bytecode))


def virtual_query(handle, address):
    """Retrieves information about a range of pages within the virtual address space
    of a specified process.

    https://msdn.microsoft.com/en-us/library/windows/desktop/aa366775(v=vs.85).aspx
    https://msdn.microsoft.com/en-us/library/windows/desktop/aa366907(v=vs.85).aspx

    Parameters
    ----------
    handle: int
        The handle to a process. The function allocates memory within the virtual address space of this process.
        The handle must have the PROCESS_VM_OPERATION access right.
    address: int
        An address of the region of to be read.

    Returns
    -------
    MEMORY_BASIC_INFORMATION
        A memory basic information object
    """
    mbi = pymem.ressources.structure.MEMORY_BASIC_INFORMATION()
    pymem.ressources.kernel32.SetLastError(0)
    pymem.ressources.kernel32.VirtualQueryEx(handle, address, ctypes.byref(mbi), ctypes.sizeof(mbi))
    error_code = ctypes.windll.kernel32.GetLastError()
    if error_code:
        pymem.ressources.kernel32.SetLastError(0)
        raise pymem.exception.WinAPIError(error_code)
    return mbi
