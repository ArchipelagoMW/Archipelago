# Copyright 2019 RoadrunnerWMC
#
# This file is part of ndspy.
#
# ndspy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ndspy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ndspy.  If not, see <https://www.gnu.org/licenses/>.
"""
Support for executable code files.
"""

from __future__ import annotations

import os
import struct
from typing import Callable, Container

from . import _common
from . import codeCompression


# Code settings full struct (from nds-bootstrap):
# typedef struct {
#     u32 auto_load_list_offset;
#     u32 auto_load_list_end;
#     u32 auto_load_start;
#     u32 static_bss_start;
#     u32 static_bss_end;
#     u32 compressed_static_end;
#     u32 sdk_version;
#     u32 nitro_code_be;
#     u32 nitro_code_le;
# } module_params_t;


class MainCodeFile:
    """
    Either the main ARM7 code file or the main ARM9 code file.
    """

    class Section:
        """
        A single section within an ARM7 or ARM9 code file. Code not
        technically contained within a section defined in the sections
        table in the code settings block is represented as an "implicit"
        section.
        """

        data: bytes
        ramAddress: int
        bssSize: int
        # There's an implicit first section in the file, which is not
        # defined in the sections table with the others. This attribute
        # will be True if this is that section.
        implicit: bool


        def __init__(
            self,
            data: bytes,
            ramAddress: int,
            bssSize: int,
            *,
            implicit: bool = False,
        ):
            self.data = bytearray(data)
            self.ramAddress = ramAddress
            self.bssSize = bssSize
            self.implicit = implicit


        def __str__(self) -> str:
            data = _common.shortBytesRepr(self.data)
            imp = ' implicit' if self.implicit else ''
            return f'<code-section at 0x{self.ramAddress:08X}: {data}{imp}>'


        def __repr__(self) -> str:
            data = _common.shortBytesRepr(self.data)

            return (f'{type(self).__name__}({data}'
                    f', 0x{self.ramAddress:08X}'
                    f', 0x{self.bssSize:X}'
                    f'{", implicit=True" if self.implicit else ""})')


    sections: list[Section]
    ramAddress: int
    codeSettingsOffs: int | None


    def __init__(self, data: bytes, ramAddress: int, codeSettingsPointerAddress: int | None = None):
        self.sections = []
        self.ramAddress = ramAddress

        data = codeCompression.decompress(data)

        self.codeSettingsOffs = None
        if codeSettingsPointerAddress:
            # (codeSettingsPointerAddress might be None if it's not
            # available, or 0 if the ROM has it set to 0)
            try:
                codeSettingsAddr, = struct.unpack_from(
                    '<I', data, codeSettingsPointerAddress - ramAddress - 4)
                self.codeSettingsOffs = codeSettingsAddr - ramAddress
                assert 0 <= self.codeSettingsOffs < len(data) - 4

            except Exception:
                # Something was probably out of range. Fall back to the
                # manual search
                self.codeSettingsOffs = None

        if self.codeSettingsOffs is None:
            # Manual search algorithm used as a fallback
            self.codeSettingsOffs = self._searchForCodeSettingsOffs(data)

        if self.codeSettingsOffs is not None:
            copyTableBegin, copyTableEnd, dataBegin = \
                struct.unpack_from('<3I', data, self.codeSettingsOffs)
            copyTableBegin -= ramAddress
            copyTableEnd -= ramAddress
            dataBegin -= ramAddress
        else:
            # No code settings, so the entire file is one implied section
            copyTableBegin = copyTableEnd = 0
            dataBegin = len(data)

        def makeSection(
            ramAddr: int,
            ramLen: int,
            fileOffs: int,
            bssSize: int,
            implicit: bool = False,
        ) -> None:
            sdata = data[fileOffs : fileOffs + ramLen]
            self.sections.append(self.Section(sdata,
                                              ramAddr,
                                              bssSize,
                                              implicit=implicit))

        # Implicit first section
        makeSection(ramAddress, dataBegin, 0, 0, implicit=True)

        copyTablePos  = copyTableBegin
        while copyTablePos < copyTableEnd:
            secRamAddr, secSize, bssSize = \
                struct.unpack_from('<3I', data, copyTablePos)
            copyTablePos += 12

            makeSection(secRamAddr, secSize, dataBegin, bssSize)

            dataBegin += secSize


    @classmethod
    def fromCompressed(cls, data: bytes, *args) -> MainCodeFile:
        """
        Create a main code file from compressed code data.

        This function is a bit outdated, since the default constructor
        can now detect code compression. There is no real reason to use
        this function anymore, and it may be removed at some point.

        Parameters are the same as those of the default constructor.
        """
        data = codeCompression.decompress(data)
        return cls(data, *args)


    @classmethod
    def fromSections(cls, sections: list[Section], ramAddress: int) -> MainCodeFile:
        """
        Create a main code file from a list of sections.
        """
        self = cls(b'', ramAddress)
        self.sections = sections
        return self


    @classmethod
    def fromFile(cls, filePath: str | os.PathLike, ramAddress: int) -> MainCodeFile:
        """
        Load a main code file from a filesystem file.
        """
        with open(filePath, 'rb') as f:
            return cls(f.read(), ramAddress)


    def save(self, *, compress: bool = False) -> bytes:
        """
        Generate a bytes object representing this code file.
        """
        data = bytearray()

        for s in self.sections:
            data.extend(s.data)

            # Align to 0x04
            while len(data) % 4:
                data.append(0)

        # These loops are NOT identical!
        # The first one only operates on sections with length != 0,
        # and the second operates on sections with length == 0!

        sectionTable = bytearray()

        for s in self.sections:
            if s.implicit: continue
            if len(s.data) == 0: continue
            sectionTable.extend(
                struct.pack('<3I', s.ramAddress, len(s.data), s.bssSize))

        for s in self.sections:
            if s.implicit: continue
            if len(s.data) != 0: continue
            sectionTable.extend(
                struct.pack('<3I', s.ramAddress, len(s.data), s.bssSize))

        sectionTableOffset = len(data)
        data.extend(sectionTable)

        def setInt(addr: int, val: int) -> None:
            struct.pack_into('<I', data, addr, val)

        sectionTableAddr = self.ramAddress + sectionTableOffset
        sectionTableEnd = sectionTableAddr + len(sectionTable)

        cso = self.codeSettingsOffs
        if cso is not None:
            setInt(cso + 0x00, sectionTableAddr)
            setInt(cso + 0x04, sectionTableEnd)
            setInt(cso + 0x08, self.ramAddress + len(self.sections[0].data))
        else:
            # Welp, hopefully we only have one section :P
            pass

        if compress:
            data = bytearray(codeCompression.compress(data, True))
            setInt(cso + 0x14, self.ramAddress + len(data))
        else:
            setInt(cso + 0x14, 0)

        return data


    def saveToFile(self, filePath: str | os.PathLike, *, compress: bool = False) -> None:
        """
        Generate file data representing this main code file, and save it
        to a filesystem file.
        """
        d = self.save(compress=compress)
        with open(filePath, 'wb') as f:
            f.write(d)


    def _searchForCodeSettingsOffs(self, data: bytes) -> int | None:
        """
        Find the offset of the code settings area in the data given.
        Return None if it can't be found.
        """

        # Simple heuristic that works in most arm9.bin's:
        for i in range(0, 0x8000, 4):
            if data[i:i+8] == b'\x21\x06\xC0\xDE\xDE\xC0\x06\x21':
                return i - 0x1C

        # But to support arm7, which lacks that magic, we can fall back
        # to a different heuristic based on the assumption that the code
        # section table will be the very last thing in the code file.
        # Which... isn't a great assumption, but it's the best I've got
        # right now.
        expectedTableEnd = self.ramAddress + len(data)
        expectedTableEndBytes = struct.pack('<I', expectedTableEnd)
        if expectedTableEndBytes in data:
            try:
                match = data.index(expectedTableEndBytes, 0)
            except ValueError:
                match = None
            while match is not None:
                possibleTableStart, = struct.unpack_from('<I', data, match - 4)
                if (possibleTableStart % 4 == 0
                        and (expectedTableEnd - possibleTableStart) % 12 == 0
                        and expectedTableEnd - possibleTableStart < 0x100):
                    # Probably a match
                    return match - 4
                try:
                    match = data.index(expectedTableEndBytes, match + 1)
                except ValueError:
                    match = None


    def __str__(self) -> str:
        linesList = [f'<main-code at 0x{self.ramAddress:08X}']

        for s in self.sections:
            linesList.append(f'    {s}')

        linesList.append('>')

        return '\n'.join(linesList)


    def __repr__(self) -> str:
        return (f'{type(self).__name__}.fromSections({self.sections!r}'
                f', 0x{self.ramAddress:08X})')


class Overlay:
    """
    An ARM7 or ARM9 code overlay.
    """

    data: bytes
    ramAddress: int
    ramSize: int
    bssSize: int
    staticInitStart: int
    staticInitEnd: int
    fileID: int
    compressedSize: int
    flags: int


    def __init__(
        self,
        data: bytes,
        ramAddress: int,
        ramSize: int,
        bssSize: int,
        staticInitStart: int,
        staticInitEnd: int,
        fileID: int,
        compressedSize: int,
        flags: int,
    ):
        self.ramAddress = ramAddress
        self.ramSize = ramSize
        self.bssSize = bssSize
        self.staticInitStart = staticInitStart
        self.staticInitEnd = staticInitEnd
        self.fileID = fileID
        self.compressedSize = compressedSize
        self.flags = flags

        if self.compressed:
            self.data = bytearray(codeCompression.decompress(data))
        else:
            self.data = bytearray(data)


    @property
    def compressed(self) -> bool:
        return bool(self.flags & 1)
    @compressed.setter
    def compressed(self, value: bool) -> None:
        if value:
            self.flags |= 1
        else:
            self.flags &= ~1


    @property
    def verifyHash(self) -> bool:
        return bool(self.flags & 2)
    @verifyHash.setter
    def verifyHash(self, value: bool) -> None:
        if value:
            self.flags |= 2
        else:
            self.flags &= ~2


    def save(self, *, compress: bool = False) -> bytes:
        """
        Generate a bytes object representing this overlay.
        """
        self.ramSize = len(self.data)
        if compress:
            data = codeCompression.compress(self.data, False)
        else:
            data = self.data
        self.compressedSize = len(data)
        self.compressed = compress
        return data


    def __str__(self) -> str:
        fields = []
        fields.append('at 0x%08X' % self.ramAddress)
        fields.append(f'file={self.fileID}')
        if self.compressed:
            fields.append('compressed')
        if self.verifyHash:
            fields.append('verify-hash')

        return f'<overlay {" ".join(fields)}>'

    def __repr__(self) -> str:
        fields = []
        fields.append(_common.shortBytesRepr(self.data))
        fields.append('0x%08X' % self.ramAddress)
        fields.append('0x%X' % self.ramSize)
        fields.append('0x%X' % self.bssSize)
        fields.append('0x%08X' % self.staticInitStart)
        fields.append('0x%08X' % self.staticInitEnd)
        fields.append(repr(self.fileID))
        fields.append('0x%X' % self.compressedSize)
        fields.append('0x%X' % self.flags)
        return f'{type(self).__name__}({", ".join(fields)})'


def loadOverlayTable(
    tableData: bytes,
    fileCallback: Callable[[int, int], bytes],
    idsToLoad: Container[int] | None = None,
) -> dict[int, Overlay]:
    """
    Parse ARM7 or ARM9 overlay table data to create a dictionary of
    Overlays. This is the inverse of saveOverlayTable().
    """
    ovs: dict[int, Overlay] = {}
    for i in range(0, len(tableData), 32):
        (ovID, ramAddr, ramSize, bssSize, staticInitStart, staticInitEnd,
            fileID, compressedSize_Flags) = struct.unpack_from('<8I', tableData, i)

        if idsToLoad is not None and ovID not in idsToLoad:
            continue

        fileData = fileCallback(ovID, fileID)

        ovs[ovID] = Overlay(fileData, ramAddr, ramSize, bssSize,
            staticInitStart, staticInitEnd, fileID,
            compressedSize_Flags & 0xFFFFFF, compressedSize_Flags >> 24)

    return ovs


def saveOverlayTable(table: dict[int, Overlay]) -> bytes:
    """
    Generate a bytes object representing this dictionary of Overlays, in
    proper ARM7 or ARM9 overlay table format. This is the inverse of
    loadOverlayTable().
    """
    if not table: return b''

    ovt = bytearray()

    # Ensure that we loop over overlay IDs in order
    for ovId in sorted(table):
        ov = table[ovId]

        values = []
        values.append(ovId)                # 0x00
        values.append(ov.ramAddress)       # 0x04
        values.append(ov.ramSize)          # 0x08
        values.append(ov.bssSize)          # 0x0C
        values.append(ov.staticInitStart)  # 0x10
        values.append(ov.staticInitEnd)    # 0x14
        values.append(ov.fileID)           # 0x18
        values.append(ov.compressedSize | ov.flags << 24) # 0x1C

        ovt.extend(struct.pack('<8I', *values))

    return ovt
