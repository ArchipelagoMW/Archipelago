import sys

import pymem.memory
import pymem.ressources.kernel32
import pymem.ressources.structure

try:
    # faster than builtin re
    import regex as re
except ImportError:
    import re


# TODO: warn that pattern is a regex and may need to be escaped
# TODO: 2.0 rename to pattern_scan_page
def scan_pattern_page(handle, address, pattern, *, return_multiple=False):
    """Search a byte pattern given a memory location.
    Will query memory location information and search over until it reaches the
    length of the memory page. If nothing is found the function returns the
    next page location.

    Parameters
    ----------
    handle: int
        Handle to an open object
    address: int
        An address to search from
    pattern: bytes
        A regex byte pattern to search for
    return_multiple: bool
        If multiple results should be returned instead of stopping on the first

    Returns
    -------
    tuple
        next_region, found address

        found address may be None if one was not found, or we didn't have permission to scan
        the region

        if return_multiple is True found address will instead be a list of found addresses
        or an empty list if no results

    Examples
    --------
    >>> pm = pymem.Pymem("Notepad.exe")
    >>> address_reference = 0x7ABC00001
    # Here the "." means that the byte can be any byte; a "wildcard"
    # also note that this pattern may be outdated
    >>> bytes_pattern = b".\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00" \\
    ...                 b"\\x00\\x00\\x00\\x00\\x00\\x00..\\x00\\x00..\\x00\\x00\\x64\\x04"
    >>> character_count_address = pymem.pattern.scan_pattern_page(pm.process_handle, address_reference, bytes_pattern)
    """
    mbi = pymem.memory.virtual_query(handle, address)
    next_region = mbi.BaseAddress + mbi.RegionSize
    allowed_protections = [
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_EXECUTE,
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_EXECUTE_READ,
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_EXECUTE_READWRITE,
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_READWRITE,
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_READONLY,
    ]
    if mbi.state != pymem.ressources.structure.MEMORY_STATE.MEM_COMMIT or mbi.protect not in allowed_protections:
        return next_region, None

    page_bytes = pymem.memory.read_bytes(handle, address, mbi.RegionSize)

    if not return_multiple:
        found = None
        match = re.search(pattern, page_bytes, re.DOTALL)

        if match:
            found = address + match.span()[0]

    else:
        found = []

        for match in re.finditer(pattern, page_bytes, re.DOTALL):
            found_address = address + match.span()[0]
            found.append(found_address)

    return next_region, found


def pattern_scan_module(handle, module, pattern, *, return_multiple=False):
    """Given a handle over an opened process and a module will scan memory after
    a byte pattern and return its corresponding memory address.

    Parameters
    ----------
    handle: int
        Handle to an open object
    module: MODULEINFO
        An instance of a given module
    pattern: bytes
        A regex byte pattern to search for
    return_multiple: bool
        If multiple results should be returned instead of stopping on the first

    Returns
    -------
    int, list, optional
        Memory address of given pattern, or None if one was not found
        or a list of found addresses in return_multiple is True

    Examples
    --------
    >>> pm = pymem.Pymem("Notepad.exe")
    # Here the "." means that the byte can be any byte; a "wildcard"
    # also note that this pattern may be outdated
    >>> bytes_pattern = b".\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00" \\
    ...                 b"\\x00\\x00\\x00\\x00\\x00\\x00..\\x00\\x00..\\x00\\x00\\x64\\x04"
    >>> module_notepad = pymem.process.module_from_name(pm.process_handle, "Notepad.exe")
    >>> character_count_address = pymem.pattern.pattern_scan_module(pm.process_handle, module_notepad, bytes_pattern)
    """
    base_address = module.lpBaseOfDll
    max_address = module.lpBaseOfDll + module.SizeOfImage
    page_address = base_address

    if not return_multiple:
        found = None
        while page_address < max_address:
            page_address, found = scan_pattern_page(handle, page_address, pattern)

            if found:
                break

    else:
        found = []
        while page_address < max_address:
            page_address, new_found = scan_pattern_page(handle, page_address, pattern, return_multiple=True)

            if new_found:
                found += new_found

    return found


def pattern_scan_all(handle, pattern, *, return_multiple=False):
    """Scan the entire address space for a given regex pattern

    Parameters
    ----------
    handle: int
        Handle to an open process
    pattern: bytes
        A regex bytes pattern to search for
    return_multiple: bool
        If multiple results should be returned

    Returns
    -------
    int, list, optional
        Memory address of given pattern, or None if one was not found
        or a list of found addresses in return_multiple is True
    """
    next_region = 0

    found = []
    user_space_limit = 0x7FFFFFFF0000 if sys.maxsize > 2**32 else 0x7fff0000
    while next_region < user_space_limit:
        next_region, page_found = scan_pattern_page(
            handle,
            next_region,
            pattern,
            return_multiple=return_multiple
        )

        if not return_multiple and page_found:
            return page_found

        if page_found:
            found += page_found

    if not return_multiple:
        return None

    return found
