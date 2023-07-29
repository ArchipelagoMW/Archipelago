import os

import bsdiff4

from ..Rom import get_base_rom_bytes


def apply_basepatch(base_rom_bytes: bytes) -> bytes:
    with open(os.path.join(os.path.dirname(__file__), "basepatch.bsdiff4"), "rb") as basepatch:
        delta: bytes = basepatch.read()
    return bsdiff4.patch(base_rom_bytes, delta)


def create_basepatch() -> None:
    from .asar import close as asar_close, geterrors as asar_errors, getprints as asar_prints, \
        getwarnings as asar_warnings, init as asar_init, patch as asar_patch

    os.add_dll_directory(os.path.dirname(__file__))
    print("Initializing Asar library")
    asar_init()

    print("Opening base ROM")
    old_rom_data: bytes = get_base_rom_bytes()

    print("Patching base ROM")
    result, new_rom_data = asar_patch(os.path.join(os.path.dirname(__file__), "basepatch.asm"), old_rom_data)

    warnings = asar_warnings()
    print("\nWarnings: " + str(len(warnings)))
    for w in warnings:
        print(w)

    if result:
        print("Success")
        for p in asar_prints():
            print(p)
        asar_close()
        delta: bytes = bsdiff4.diff(old_rom_data, new_rom_data)
        with open(os.path.join(os.path.dirname(__file__), "basepatch.bsdiff4"), "wb") as f:
            f.write(delta)
    else:
        errors = asar_errors()
        print("\nErrors: " + str(len(errors)))
        for error in errors:
            print(error)
        asar_close()
        raise RuntimeError("Asar errors while trying to create basepatch for Lufia II Ancient Cave.")
