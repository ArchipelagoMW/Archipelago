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
Support for ROMs.
"""

from __future__ import annotations

import math
import os
import struct
from typing import Container

from . import _common
from . import code
from . import fnt as fntLib


_ICON_BANNER_LENGTHS = {
    # version: length,
    0x0001: 0x840,
    0x0002: 0x940,
    0x0003: 0x1240,
    0x0103: 0x23C0,
}


class NintendoDSRom:
    """
    A Nintendo DS ROM file (.nds).
    """
    name: bytes
    idCode: bytes
    developerCode: bytes
    unitCode: int
    encryptionSeedSelect: int
    deviceCapacity: int
    pad015: int
    pad016: int
    pad017: int
    pad108: int
    pad019: int
    pad01A: int
    pad01B: int
    pad01C: int
    region: int
    version: int
    autostart: int
    arm9EntryAddress: int
    arm9RamAddress: int
    arm7EntryAddress: int
    arm7RamAddress: int
    normalCardControlRegisterSettings: int
    secureAreaChecksum: int
    secureTransferDelay: int
    arm9CodeSettingsPointerAddress: int
    arm7CodeSettingsPointerAddress: int
    secureAreaDisable: bytes
    pad088: bytes
    nintendoLogo: bytes
    debugRomAddress: int
    pad16C: bytes
    pad200: bytes
    rsaSignature: bytes
    arm9: bytes
    arm9PostData: bytes
    arm7: bytes
    arm9OverlayTable: bytes
    arm7OverlayTable: bytes
    iconBanner: bytes
    debugRom: bytes
    filenames: fntLib.Folder
    files: list[bytes]
    sortedFileIds: list[int]


    def __init__(self, data: bytes | None = None):
        super().__init__()

        if data is None:
            self._initAsNew()
        else:
            self._initFromData(data)


    def _initAsNew(self) -> None:
        """
        Initialize this ROM with default values.
        """

        self.name = b''
        self.idCode = b'####'
        self.developerCode = b'\0\0'
        self.unitCode = 0
        self.encryptionSeedSelect = 0
        self.deviceCapacity = 9
        self.pad015 = 0
        self.pad016 = 0
        self.pad017 = 0
        self.pad018 = 0
        self.pad019 = 0
        self.pad01A = 0
        self.pad01B = 0
        self.pad01C = 0
        self.region = 0
        self.version = 0
        self.autostart = 0
        self.arm9EntryAddress = 0x2000800
        self.arm9RamAddress = 0x2000000
        self.arm7EntryAddress = 0x2380000
        self.arm7RamAddress = 0x2380000
        self.normalCardControlRegisterSettings = 0x0416657
        self.secureCardControlRegisterSettings = 0x81808f8
        self.secureAreaChecksum = 0x0000
        self.secureTransferDelay = 0x0D7E
        self.arm9CodeSettingsPointerAddress = 0
        self.arm7CodeSettingsPointerAddress = 0
        self.secureAreaDisable = b'\0' * 8
        self.pad088 = b'\0' * 0x38
        self.nintendoLogo = (b'$\xff\xaeQi\x9a\xa2!=\x84\x82\n\x84\xe4\t\xad'
            b"\x11$\x8b\x98\xc0\x81\x7f!\xa3R\xbe\x19\x93\t\xce \x10FJJ\xf8'1"
            b'\xecX\xc7\xe83\x82\xe3\xce\xbf\x85\xf4\xdf\x94\xceK\t\xc1\x94V'
            b"\x8a\xc0\x13r\xa7\xfc\x9f\x84Ms\xa3\xca\x9aaX\x97\xa3'\xfc\3\x98"
            b'v#\x1d\xc7a\3\4\xaeV\xbf8\x84\0@\xa7\x0e\xfd\xffR\xfe\3o\x950'
            b'\xf1\x97\xfb\xc0\x85`\xd6\x80%\xa9c\xbe\3\1N8\xe2\xf9\xa24\xff'
            b'\xbb>\3Dx\0\x90\xcb\x88\x11:\x94e\xc0|c\x87\xf0<\xaf\xd6%\xe4'
            b'\x8b8\n\xacr!\xd4\xf8\7')
        self.debugRomAddress = 0
        self.pad16C = b'\0' * 0x94
        self.pad200 = b'\0' * 0x3E00

        self.rsaSignature = b''

        self.arm9 = b''
        self.arm9PostData = b''
        self.arm7 = b''
        self.arm9OverlayTable = b''
        self.arm7OverlayTable = b''
        self.iconBanner = b''
        self.debugRom = b''

        self.filenames = fntLib.Folder()
        self.files = []
        self.sortedFileIds = []


    def _initFromData(self, data: bytes) -> None:
        """
        Initialize this ROM from existing data.
        """
        # I could read the header as one huge struct,
        # but... no.

        data = bytearray(data)
        if len(data) < 0x200:
            data.extend(b'\0' * (0x200 - len(data)))
            assert len(data) == 0x200, f'ROM data extension to length 0x200 failed (actual new length {hex(len(data))})'

        headerOffset = 0
        def readRaw(length: int) -> bytearray:
            nonlocal headerOffset
            retVal = data[headerOffset : headerOffset+length]
            headerOffset += length
            return retVal
        def read8() -> int:
            nonlocal headerOffset
            retVal = data[headerOffset]
            headerOffset += 1
            return retVal
        def read16() -> int:
            nonlocal headerOffset
            retVal, = struct.unpack_from('<H', data, headerOffset)
            headerOffset += 2
            return retVal
        def read32() -> int:
            nonlocal headerOffset
            retVal, = struct.unpack_from('<I', data, headerOffset)
            headerOffset += 4
            return retVal

        assert headerOffset == 0, f'(Load) Header offset check at 0x00: {hex(headerOffset)}'
        self.name = readRaw(12).rstrip(b'\0')
        self.idCode = readRaw(4)
        self.developerCode = readRaw(2)
        self.unitCode = read8()
        self.encryptionSeedSelect = read8()
        self.deviceCapacity = read8()
        assert headerOffset == 0x15, f'(Load) Header offset check at 0x15: {hex(headerOffset)}'
        self.pad015 = read8()
        self.pad016 = read8()
        self.pad017 = read8()
        self.pad018 = read8()
        self.pad019 = read8()
        self.pad01A = read8()
        self.pad01B = read8()
        self.pad01C = read8()
        self.region = read8()
        self.version = read8()
        self.autostart = read8()
        assert headerOffset == 0x20, f'(Load) Header offset check at 0x20: {hex(headerOffset)}'
        arm9Offset = read32()
        self.arm9EntryAddress = read32()
        self.arm9RamAddress = read32()
        arm9Len = read32()
        arm7Offset = read32()
        self.arm7EntryAddress = read32()
        self.arm7RamAddress = read32()
        arm7Len = read32()
        assert headerOffset == 0x40, f'(Load) Header offset check at 0x40: {hex(headerOffset)}'
        fntOffset = read32()
        fntLen = read32()
        fatOffset = read32()
        fatLen = read32()
        arm9OvTOffset = read32()
        arm9OvTLen = read32()
        arm7OvTOffset = read32()
        arm7OvTLen = read32()
        assert headerOffset == 0x60, f'(Load) Header offset check at 0x60: {hex(headerOffset)}'
        self.normalCardControlRegisterSettings = read32()
        self.secureCardControlRegisterSettings = read32()
        iconBannerOffset = read32()
        self.secureAreaChecksum = read16() # TODO: Actually recalculate
                                           # this upon saving.
        self.secureTransferDelay = read16()
        assert headerOffset == 0x70, f'(Load) Header offset check at 0x70: {hex(headerOffset)}'
        self.arm9CodeSettingsPointerAddress = read32()
        self.arm7CodeSettingsPointerAddress = read32()
        self.secureAreaDisable = readRaw(8)
        assert headerOffset == 0x80, f'(Load) Header offset check at 0x80: {hex(headerOffset)}'
        romSizeOrRsaSigOffset = read32()
        headerSize = read32()
        self.pad088 = readRaw(0x38)
        self.nintendoLogo = readRaw(0x9C)
        nintendoLogoChecksum = read16()
        headerChecksum = read16()
        assert headerOffset == 0x160, f'(Load) Header offset check at 0x160: {hex(headerOffset)}'
        debugRomOffset = read32()
        debugRomSize = read32()
        self.debugRomAddress = read32()
        self.pad16C = readRaw(0x94)
        assert headerOffset == 0x200, f'(Load) Header offset check at 0x200: {hex(headerOffset)}'
        self.pad200 = data[0x200 : min(arm9Offset, len(data))]

        # Read the RSA signature file
        realSigOffset = 0
        if len(data) >= 0x1004:
            realSigOffset, = struct.unpack_from('<I', data, 0x1000)
        if not realSigOffset and len(data) > romSizeOrRsaSigOffset:
            realSigOffset = romSizeOrRsaSigOffset
        self.rsaSignature = b''
        if realSigOffset:
            self.rsaSignature = data[realSigOffset : min(len(data), realSigOffset + 0x88)]

        # Read arm9, arm7, FNT, FAT, overlay tables, icon banner
        self.arm9 = data[arm9Offset : arm9Offset+arm9Len]
        self.arm7 = data[arm7Offset : arm7Offset+arm7Len]
        fnt = data[fntOffset : fntOffset+fntLen]
        fat = data[fatOffset : fatOffset+fatLen]
        self.arm9OverlayTable = data[
            arm9OvTOffset : arm9OvTOffset + arm9OvTLen]
        self.arm7OverlayTable = data[
            arm7OvTOffset : arm7OvTOffset + arm7OvTLen]
        if iconBannerOffset:
            version, = struct.unpack_from('<H', data, iconBannerOffset)
            iconBannerLen = _ICON_BANNER_LENGTHS.get(version, _ICON_BANNER_LENGTHS[1])
            self.iconBanner = \
                data[iconBannerOffset : iconBannerOffset + iconBannerLen]
        else:
            self.iconBanner = b''
        if debugRomOffset:
            self.debugRom = \
                data[debugRomOffset : debugRomOffset + debugRomSize]
        else:
            self.debugRom = b''

        # Read the small amount of data immediately following arm9
        # No idea what this is, though...
        # Probably related to the "code settings" stuff in code.py.
        arm9PostData = bytearray()
        arm9PostDataOffset = arm9Offset+arm9Len
        while (data[arm9PostDataOffset:arm9PostDataOffset+4]
                == b'\x21\x06\xC0\xDE'):
            arm9PostData.extend(data[arm9PostDataOffset:arm9PostDataOffset+12])
            arm9PostDataOffset += 12
        self.arm9PostData = arm9PostData

        # Read the filename table
        if fnt:
            self.filenames = fntLib.load(fnt)
        else:
            self.filenames = fntLib.Folder()

        # Read files
        self.files = []
        self.sortedFileIds = []
        if fat:
            offset2Id = {}
            for i in range(len(fat) // 8):
                startOffset, endOffset = struct.unpack_from('<II', fat, 8 * i)
                self.files.append(data[startOffset:endOffset])
                offset2Id[startOffset] = i
            for off in sorted(offset2Id):
                self.sortedFileIds.append(offset2Id[off])


    @classmethod
    def fromFile(cls, filePath: str | os.PathLike) -> NintendoDSRom:
        """
        Load a ROM from a filesystem file.
        """
        with open(filePath, 'rb') as f:
            return cls(f.read())


    def save(self, *, updateDeviceCapacity: bool = False) -> bytes:
        """
        Generate file data representing this ROM.
        """

        fileOffsets = {}

        # The header will be filled in at the end.
        data = bytearray(0x200)

        def align(alignment: int, fill: bytes = b'\0') -> None:
            if len(data) % alignment:
                extra = len(data) % alignment
                needed = alignment - extra
                data.extend(fill * needed)

        # Add post-header padding
        data.extend(self.pad200)
        align(0x4000)

        # Pack arm9
        arm9Offset = len(data)
        data.extend(self.arm9)
        data.extend(self.arm9PostData)
        align(0x200, b'\xFF')

        # Pack arm9 overlay table
        if self.arm9OverlayTable:
            arm9OvTOffset = len(data)
            data.extend(self.arm9OverlayTable)
            align(0x200, b'\xFF')
        else:
            arm9OvTOffset = 0

        # Pack arm9 overlays
        for i in range(0, len(self.arm9OverlayTable), 32):
            fileId, = struct.unpack_from('<I', self.arm9OverlayTable, i + 0x18)
            fileOffsets[fileId] = len(data)
            data.extend(self.files[fileId])
            align(0x200, b'\xFF')

        # Pack arm7
        arm7Offset = len(data)
        data.extend(self.arm7)
        align(0x200, b'\xFF')

        # Pack arm7 overlay table
        if self.arm7OverlayTable:
            arm7OvTOffset = len(data)
            data.extend(self.arm7OverlayTable)
            align(0x200, b'\xFF')
        else:
            arm7OvTOffset = 0

        # Pack arm7 overlays
        for i in range(0, len(self.arm7OverlayTable), 32):
            fileId, = struct.unpack_from('<I', self.arm7OverlayTable, i + 0x18)
            fileOffsets[fileId] = len(data)
            data.extend(self.files[fileId])
            align(0x200, b'\xFF')

        # Pack the filename table
        fntOffset = len(data)
        fnt = fntLib.save(self.filenames)
        data.extend(fnt)
        align(0x200, b'\xFF')

        # Leave some empty space for the file allocation table -- we'll
        # fill in the real values later
        fatOffset = len(data)
        data.extend(b'\0' * 8 * len(self.files))
        align(0x200, b'\xFF')

        # Pack the icon/banner
        if self.iconBanner:
            version, = struct.unpack_from('<H', self.iconBanner, 0)
            iconBannerLen = _ICON_BANNER_LENGTHS.get(version, _ICON_BANNER_LENGTHS[1])
            assert len(self.iconBanner) == iconBannerLen, f'(Save) Icon banner length is wrong (version {hex(version)}, length {hex(len(self.iconBanner))})'
            iconBannerOffset = len(data)
            data.extend(self.iconBanner)
            align(0x200, b'\xFF')
        else:
            iconBannerOffset = 0

        # Pack the debug rom
        # I don't know if this is really where it would go, but it seems
        # to be the logical place to put it...
        if self.debugRom:
            debugRomOffset = len(data)
            data.extend(self.debugRom)
            align(0x200, b'\xFF')
        else:
            debugRomOffset = 0

        # Pack the rest of the files
        def iterFilenums():
            for fileNum in self.sortedFileIds:
                if fileNum not in fileOffsets and fileNum < len(self.files):
                    yield fileNum
            for fileNum in range(len(self.files)):
                if fileNum not in fileOffsets:
                    yield fileNum

        for fileNum in iterFilenums():
            # Align before instead of after, so that there's no extra
            # padding after the last file
            align(0x200, b'\xFF')
            fileOffsets[fileNum] = len(data)
            data.extend(self.files[fileNum])

        # Pack the FAT
        for i, file in enumerate(self.files):
            assert i in fileOffsets, f'(Save) File {i} has no offset'
            startOffset = fileOffsets[i]
            endOffset = startOffset + len(file)
            struct.pack_into('<II', data, fatOffset + 8 * i, startOffset, endOffset)

        # Pack the RSA signature
        align(0x20)
        rsaSignatureOffset = len(data)
        data.extend(self.rsaSignature)

        # We need to do this for compatibility with NSMBe
        struct.pack_into('<I', data, 0x1000, rsaSignatureOffset)

        # Now that we know how large the ROM data is, we can update the
        # device capacity value
        if updateDeviceCapacity:
            self.deviceCapacity = math.ceil(math.log2(len(data))) - 17

        # Now that all the offsets and stuff are determined, write the
        # header data
        headerOffset = 0
        def writeRaw(value: bytes) -> None:
            nonlocal headerOffset
            data[headerOffset : headerOffset+len(value)] = value
            headerOffset += len(value)
        def write8(value: int) -> None:
            nonlocal headerOffset
            data[headerOffset] = value
            headerOffset += 1
        def write16(value: int) -> None:
            nonlocal headerOffset
            struct.pack_into('<H', data, headerOffset, value)
            headerOffset += 2
        def write32(value: int) -> None:
            nonlocal headerOffset
            struct.pack_into('<I', data, headerOffset, value)
            headerOffset += 4

        assert headerOffset == 0, f'(Save) Header offset check at 0x00: {hex(headerOffset)}'
        writeRaw(self.name.ljust(12, b'\0')[:12])
        assert len(self.idCode) == 4, f'(Save) Wrong ID code length: {len(self.idCode)}'
        writeRaw(self.idCode)
        assert len(self.developerCode) == 2, f'(Save) Wrong developer code length: {len(self.developerCode)}'
        writeRaw(self.developerCode)
        write8(self.unitCode)
        write8(self.encryptionSeedSelect)
        write8(self.deviceCapacity)
        assert headerOffset == 0x15, f'(Save) Header offset check at 0x15: {hex(headerOffset)}'
        write8(self.pad015)
        write8(self.pad016)
        write8(self.pad017)
        write8(self.pad018)
        write8(self.pad019)
        write8(self.pad01A)
        write8(self.pad01B)
        write8(self.pad01C)
        write8(self.region)
        write8(self.version)
        write8(self.autostart)
        assert headerOffset == 0x20, f'(Save) Header offset check at 0x20: {hex(headerOffset)}'
        write32(arm9Offset)
        write32(self.arm9EntryAddress)
        write32(self.arm9RamAddress)
        write32(len(self.arm9))
        write32(arm7Offset)
        write32(self.arm7EntryAddress)
        write32(self.arm7RamAddress)
        write32(len(self.arm7))
        assert headerOffset == 0x40, f'(Save) Header offset check at 0x40: {hex(headerOffset)}'
        write32(fntOffset)
        write32(len(fnt))
        write32(fatOffset)
        write32(len(self.files) * 8)
        write32(arm9OvTOffset)
        write32(len(self.arm9OverlayTable))
        write32(arm7OvTOffset)
        write32(len(self.arm7OverlayTable))
        assert headerOffset == 0x60, f'(Save) Header offset check at 0x60: {hex(headerOffset)}'
        write32(self.normalCardControlRegisterSettings)
        write32(self.secureCardControlRegisterSettings)
        write32(iconBannerOffset)
        write16(self.secureAreaChecksum)
        write16(self.secureTransferDelay)
        assert headerOffset == 0x70, f'(Save) Header offset check at 0x70: {hex(headerOffset)}'
        write32(self.arm9CodeSettingsPointerAddress)
        write32(self.arm7CodeSettingsPointerAddress)
        writeRaw(self.secureAreaDisable.ljust(8, b'\0')[:8])
        assert headerOffset == 0x80, f'(Save) Header offset check at 0x80: {hex(headerOffset)}'
        write32(rsaSignatureOffset)
        write32(0x4000)
        assert len(self.pad088) == 0x38, f'(Save) Wrong pad088 length: {hex(len(self.pad088))}'
        writeRaw(self.pad088)
        assert len(self.nintendoLogo) == 0x9C, f'(Save) Wrong Nintendo logo length: {hex(len(self.nintendoLogo))}'
        writeRaw(self.nintendoLogo)
        write16(_common.crc16(self.nintendoLogo))
        write16(_common.crc16(data[0:0x15e]))
        assert headerOffset == 0x160, f'(Save) Header offset check at 0x160: {hex(headerOffset)}'
        write32(debugRomOffset)
        write32(len(self.debugRom))
        write32(self.debugRomAddress)
        assert len(self.pad16C) == 0x94, f'(Save) Wrong pad16C length: {hex(len(self.pad16C))}'
        writeRaw(self.pad16C)
        assert headerOffset == 0x200, f'(Save) Header offset check at 0x200: {hex(headerOffset)}'

        return bytes(data)


    def saveToFile(
        self,
        filePath: str | os.PathLike,
        *,
        updateDeviceCapacity: bool = False,
    ) -> None:
        """
        Generate file data representing this ROM, and save it to a
        filesystem file.
        """
        d = self.save(updateDeviceCapacity=updateDeviceCapacity)
        with open(filePath, 'wb') as f:
            f.write(d)


    def loadArm9(self) -> code.MainCodeFile:
        """
        Create a MainCodeFile object representing the main ARM9 code
        file in this ROM.
        """
        return code.MainCodeFile(self.arm9,
                                 self.arm9RamAddress,
                                 self.arm9CodeSettingsPointerAddress)


    def loadArm7(self) -> code.MainCodeFile:
        """
        Create a MainCodeFile object representing the main ARM7 code
        file in this ROM.
        """
        return code.MainCodeFile(self.arm7,
                                 self.arm7RamAddress,
                                 self.arm7CodeSettingsPointerAddress)


    def loadArm9Overlays(self, idsToLoad: Container[int] | None = None) -> dict[int, code.Overlay]:
        """
        Create a dictionary of this ROM's ARM9 overlays.
        """
        def callback(ovID: int, fileID: int) -> bytes:
            return self.files[fileID]
        return code.loadOverlayTable(self.arm9OverlayTable, callback, idsToLoad)


    def loadArm7Overlays(self, idsToLoad: Container[int] | None = None) -> dict[int, code.Overlay]:
        """
        Create a dictionary of this ROM's ARM7 overlays.
        """
        def callback(ovID: int, fileID: int) -> bytes:
            return self.files[fileID]
        return code.loadOverlayTable(self.arm7OverlayTable, callback, idsToLoad)


    def getFileByName(self, filename: str) -> bytes:
        """
        Return the data for the file with the given filename (path).
        This is a convenience function.
        """
        fid = self.filenames.idOf(filename)
        if fid is None:
            raise ValueError(f'Cannot find file ID of "{filename}"')
        return self.files[fid]


    def setFileByName(self, filename: str, data: bytes) -> None:
        """
        Replace the data for the file with the given filename (path)
        with the given data. This is a convenience function.
        """
        fid = self.filenames.idOf(filename)
        if fid is None:
            raise ValueError(f'Cannot find file ID of "{filename}"')
        self.files[fid] = data


    def __str__(self) -> str:
        title = repr(bytes(self.name))[2:-1].rstrip(' ')
        code = repr(bytes(self.idCode))[2:-1]
        return f'<rom "{title}" ({code})>'


    def __repr__(self) -> str:
        try:
            data = _common.shortBytesRepr(self.save())
        except Exception:
            data = '...'
        return f'{type(self).__name__}({data})'
