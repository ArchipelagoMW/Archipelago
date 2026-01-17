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
Support for NARC archives.
"""

from __future__ import annotations

import os
import struct
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Literal

from . import _common
from . import fnt


class NARC:
    """
    A class representing a NARC archive file.
    """
    filenames: fnt.Folder
    files: list[bytes]
    endiannessOfBeginning: Literal['<', '>']

    def __init__(self, data: bytes | None = None):
        self.filenames = fnt.Folder()
        self.files = []
        self.endiannessOfBeginning = '<'
        if data is not None:
            self._initFromData(data)


    def _initFromData(self, data: bytes) -> None:
        """
        Read NARC data, and create a filename table and a list of files.
        """
        # Read the standard header
        magic, bom, version, filesize, headersize, numblocks = \
            _common.NDS_STD_FILE_HEADER.unpack_from(data, 0)

        # Little-endian beginnings are in e.g. Spirit Tracks
        # Big-endian beginnings are in e.g. NSMB
        if bom == 0xFFFE:
            self.endiannessOfBeginning = '>'
            version = (version & 0xFF) << 8 | version >> 8

        if version != 1:
            raise ValueError(f'Unsupported NARC version: {version}')

        if magic != b'NARC':
            raise ValueError("Wrong magic (should be b'NARC', instead found "
                             f'{magic})')

        # Read the file allocation block
        fatbMagic, fatbSize, fileCount = struct.unpack_from('<4sII', data, 0x10)
        assert fatbMagic == b'FATB'[::-1], f'Incorrect NARC FATB magic ({fatbMagic})'

        # Read the file name block
        fntbOffset = 0x10 + fatbSize
        fntbMagic, fntbSize = struct.unpack_from('<4sI', data, fntbOffset)
        assert fntbMagic == b'FNTB'[::-1], f'Incorrect NARC FNTB magic ({fntbMagic})'

        # Get the data from the file data block before continuing
        fimgOffset = fntbOffset + fntbSize
        fimgMagic, gmifSize = struct.unpack_from('<4sI', data, fimgOffset)
        assert fimgMagic == b'FIMG'[::-1], f'Incorrect NARC FIMG magic ({fimgMagic})'
        rawDataOffset = fimgOffset + 8

        # Read the file datas
        self.files = []
        for i in range(fileCount):
            startOffset, endOffset = struct.unpack_from('<II', data, 0x1C + 8 * i)
            self.files.append(data[rawDataOffset+startOffset : rawDataOffset+endOffset])

        # Parse the filenames
        self.filenames = fnt.load(data[fntbOffset + 8 : fntbOffset + fntbSize])


    @classmethod
    def fromFilesAndNames(cls, files: list[bytes], filenames: fnt.Folder | None = None) -> NARC:
        """
        Create a NARC archive from a list of files and (optionally) a
        filename table.
        """
        self = cls()
        self.files = files
        if filenames is not None:
            self.filenames = filenames
        return self


    @classmethod
    def fromFile(cls, filePath: str | os.PathLike, *args, **kwargs) -> NARC:
        """
        Load a NARC archive from a filesystem file.
        """
        with open(filePath, 'rb') as f:
            return cls(f.read(), *args, **kwargs)


    def save(self) -> bytes:
        """
        Generate file data representing this NARC.
        """

        # Prepare the filedata and file allocation table block
        fimgData = bytearray(8)

        fatbData = bytearray()
        fatbData.extend(struct.pack('<4sII',
            b'FATB'[::-1], 0x0C + 8 * len(self.files), len(self.files)))

        # Write data into the FIMG and FAT blocks
        for i, fd in enumerate(self.files):
            startOff = len(fimgData) - 8
            fimgData.extend(fd)
            endOff = startOff + len(fd)
            fatbData.extend(struct.pack('<II', startOff, endOff))
            while len(fimgData) % 4:
                fimgData.append(0)

        # Put the header on the FIMG block
        struct.pack_into('<4sI', fimgData, 0, b'FIMG'[::-1], len(fimgData))

        # Assemble the filename table block
        nameTable = bytearray(fnt.save(self.filenames))
        while len(nameTable) % 4:
            nameTable.append(0xFF)
        fntbData = struct.pack('<4sI', b'FNTB'[::-1], len(nameTable) + 8) + nameTable

        # Put everything together and return.
        data = bytearray(0x10)
        data.extend(fatbData)
        data.extend(fntbData)
        data.extend(fimgData)

        bom = 0xFEFF
        version = 1
        if self.endiannessOfBeginning == '>':
            bom = 0xFFFE
            version = 0x100

        _common.NDS_STD_FILE_HEADER.pack_into(
            data, 0, b'NARC', bom, version, len(data), 0x10, 3)
        return bytes(data)


    def saveToFile(self, filePath: str | os.PathLike) -> None:
        """
        Generate file data representing this NARC, and save it to a
        filesystem file.
        """
        d = self.save()
        with open(filePath, 'wb') as f:
            f.write(d)


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


    def __str__(self):
        notes = []

        if self.endiannessOfBeginning != '<':
            notes.append(f'endiannessOfBeginning={self.endiannessOfBeginning!r}')

        if notes: notes.insert(0, '') # so it'll begin with a space
        notes = ' '.join(notes)

        filenames = '\n    '.join(self.filenames._strList(0, self.files))

        return f'<narc{notes}\n    {filenames}\n>'


    def __repr__(self):

        if self.files:
            try:
                file0repr = _common.shortBytesRepr(self.files[0])
            except Exception:
                file0repr = "b'...'"

            more = ', ...' if len(self.files) > 1 else ''
            files = f'[{file0repr}{more}]'
        else:
            files = '[]'

        return f'{type(self).__name__}.fromFilesAndNames({files}, {self.filenames!r})'
