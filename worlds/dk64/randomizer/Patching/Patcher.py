"""Patcher class and Functions for modifying ROM files."""

from __future__ import annotations

import copy
import os
from io import BytesIO
import pkgutil
from typing import TYPE_CHECKING, Union
import struct

import js

if TYPE_CHECKING:
    from randomizer.Enums.Kongs import Kongs
    from randomizer.Lists.EnemyTypes import Enemies
    from randomizer.Lists.MapsAndExits import Maps
    from randomizer.Patching.ItemRando import CustomActors


def ftoi(f: float) -> str:
    """Convert float to int representation."""
    if f == 0:
        return 0
    return struct.unpack("<I", struct.pack("<f", f))[0]


class ROM:
    """Patcher for ROM files loaded via Rompatcherjs."""

    def __init__(self, file=None):
        """Patch functions for the ROM loaded within Rompatcherjs.

        This is mostly a hint file, you could directly call the javascript functions,
        but to keep this a bit more logical for team members we just import it and treat
        this like a bytesIO object.

        Args:
            file ([type], optional): [description]. Defaults to None.
        """
        if file is None:
            self.rom = js.patchedRom
        else:
            self.rom = file

    def write(self, val: int):
        """Write value to current position.

        Starts at 0x0 as the inital position without seeking.

        Args:
            val (int): Int value to write.
        """
        self.rom.writeU8(val)

    def writeBytes(self, byte_data: bytes):
        """Write an array a bytes to the current position.

        Starts at 0x0 as the inital position without seeking.

        Args:
            byte_data (bytes): Bytes object to write to current position.
        """
        self.rom.writeBytes(bytes(byte_data))

    def writeMultipleBytes(self, value: int, size: int):
        """Write multiple bytes of a size to the current position.

        Starts at 0x0 as the inital position without seeking.

        Args:
            value (int): Value to write.
            size (int): Size of the bytes to write.
        """
        arr = []
        temp = value
        for x in range(size):
            arr.append(0)
        will_pass = True
        idx = size - 1
        while will_pass:
            write = temp % 256
            arr[idx] = write
            temp = int((temp - write) / 256)
            if idx == 0 or temp == 0:
                will_pass = False
            idx -= 1
        for x in arr:
            self.write(x)

    def writeFloat(self, value: float):
        """Write 32-bit floating point value to the current position."""
        self.writeMultipleBytes(ftoi(value), 4)

    def save(self, file_name: str):
        """Save the patched file to a downloadable file.

        You need to pass the whole file and extension.
        eg save("dk64-randomizer-12345.z64")

        Args:
            file_id (str): Name of file to save as.
        """
        self.rom.fileName = file_name
        self.rom.save()

    def seek(self, val: int):
        """Seek to position in current file.

        Args:
            val (int): Position to seek to.
        """
        self.rom.seek(val)

    def readBytes(self, len: int):
        """Read bytes from current position.

        Starts at 0x0 as the inital position without seeking.

        Args:
            len (int): Length to read.

        Returns:
            bytes: List of bytes read from current position.
        """
        return bytes(self.rom.readBytes(len))

    def fixChecksum(self):
        """Fix the checksum of the current file."""
        js.fixChecksum(self.rom)

    def fixSecurityValue(self):
        """Set the security code and update the rom checksum."""
        self.seek(0x3154)
        self.write(0)
        self.fixChecksum()


# Try except for when the browser is trying to load this file
def load_base_rom() -> None:
    """Load the base ROM file for patching."""
    try:
        print("Loading base rom")
        from randomizer.Patching import BPS as bps

        try:
            patch = open("./static/patches/shrink-dk64.bps", "rb")
        except Exception:
            try:
                patch = BytesIO(js.getFile("static/patches/shrink-dk64.bps"))
            except Exception:
                patch = open("./worlds/dk64/static/patches/shrink-dk64.bps", "rb")

        original = open("dk64.z64", "rb")
        og_patched_rom = BytesIO(bps.patch(original, patch).read())
        return og_patched_rom
    except Exception as e:
        print(e)
        raise Exception("Unable to load BPS.") from e
        pass


class LocalROM:
    """Patcher for ROM files loaded via Rompatcherjs."""

    def __init__(self) -> None:
        """Patch functions for the ROM loaded within Rompatcherjs.

        This is mostly a hint file, you could directly call the javascript functions,
        but to keep this a bit more logical for team members we just import it and treat
        this like a bytesIO object.

        Args:
            file ([type], optional): [description]. Defaults to None.
        """
        patchedRom = None
        if "PYTEST_CURRENT_TEST" in os.environ:
            data_size = 32 * 1024  # 32KB = 32 * 1024 bytes
            data = bytes(range(256)) * (data_size // 256)  # Repeat values from 0 to 255 to fill 32KB
            # Create a BytesIO object
            patchedRom = BytesIO(data)
        else:
            if not os.path.exists("dk64.z64"):
                raise Exception("No ROM was loaded, please make sure you have dk64.z64 in the root directory of the project.")
            elif patchedRom is None:
                patchedRom = load_base_rom()

        self.rom = patchedRom

    def write(self, val: Union[Maps, int]) -> None:
        """Write value to current position.

        Starts at 0x0 as the inital position without seeking.

        Args:
            val (int): Int value to write.
        """
        self.rom.write((val).to_bytes(1, byteorder="big", signed=False))

    def writeBytes(self, byte_data: Union[bytearray, bytes]) -> None:
        """Write an array a bytes to the current position.

        Starts at 0x0 as the inital position without seeking.

        Args:
            byte_data (bytes): Bytes object to write to current position.
        """
        self.rom.write(bytes(byte_data))

    def writeMultipleBytes(self, value: Union[int, Enemies, Maps, Kongs, CustomActors], size: int) -> None:
        """Write multiple bytes of a size to the current position.

        Starts at 0x0 as the inital position without seeking.

        Args:
            value (int): Value to write.
            size (int): Size of the bytes to write.
        """
        arr = []
        temp = value
        for x in range(size):
            arr.append(0)
        will_pass = True
        idx = size - 1
        while will_pass:
            if temp is None:
                temp = 0
            write = temp % 256
            arr[idx] = write
            temp = int((temp - write) / 256)
            if idx == 0 or temp == 0:
                will_pass = False
            idx -= 1
        for x in arr:
            self.write(x)

    def writeFloat(self, value: float):
        """Write 32-bit floating point value to the current position."""
        self.writeMultipleBytes(ftoi(value), 4)

    def seek(self, val: int) -> None:
        """Seek to position in current file.

        Args:
            val (int): Position to seek to.
        """
        self.rom.seek(val)

    def readBytes(self, len: int) -> bytes:
        """Read bytes from current position.

        Starts at 0x0 as the inital position without seeking.

        Args:
            len (int): Length to read.

        Returns:
            bytes: List of bytes read from current position.
        """
        return bytes(self.rom.read(len))
