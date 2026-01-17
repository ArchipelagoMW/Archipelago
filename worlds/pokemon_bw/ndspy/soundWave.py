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
Support for SWAV sound waves.
"""

import enum
import struct

from . import WaveType
from . import _common


class SWAV:
    """
    An SWAV streamed audio file.
    """

    def __init__(self, file=None):
        self.waveType = WaveType.PCM8
        self.isLooped = False
        self.sampleRate = 8000
        self.time = 0
        self.loopOffset = 0
        self.totalLength = 0
        self.data = b''

        if file is not None:
            if not file.startswith(b'SWAV'):
                raise ValueError("Wrong magic (should be b'SWAV', instead "
                                 f'found {file[:4]})')

            self._initFromData(file)


    def _initFromData(self, file):
        """
        Initialize the SWAV from file data.
        """

        magic, bom, version, filesize, headersize, numblocks = \
            _common.NDS_STD_FILE_HEADER.unpack_from(file, 0)
        if version != 0x100:
            raise ValueError(f'Unsupported SWAV version: {version}')
        assert magic == b'SWAV', f'Incorrect SWAV magic ({magic})'

        dataMagic, dataSize = struct.unpack_from('<4sI', file, 0x10)
        assert dataMagic == b'DATA', f'Incorrect SWAV DATA magic ({dataMagic})'

        (waveType, self.isLooped, self.sampleRate, self.time, self.loopOffset,
            loopLength) = struct.unpack_from('<B?3HI', file, 0x18)
        self.waveType = WaveType(waveType)
        self.totalLength = self.loopOffset + loopLength

        self.data = file[0x24:filesize]


    @classmethod
    def fromData(cls, data=b'', *, waveType=WaveType.PCM8, isLooped=False,
            sampleRate=8000, time=0, loopOffset=0, totalLength=0):
        """
        Create an SWAV from raw waveform data.
        """
        self = cls()
        self.waveType = waveType
        self.isLooped = isLooped
        self.sampleRate = sampleRate
        self.time = time
        self.loopOffset = loopOffset
        self.totalLength = totalLength
        self.data = data
        return self


    @classmethod
    def fromFile(cls, filePath):
        """
        Load an SWAV from a filesystem file.
        """
        with open(filePath, 'rb') as f:
            return cls(f.read())


    def save(self, *, updateTime=False, updateTotalLength=False):
        """
        Generate file data representing this SWAV.
        """

        if updateTime:
            self.time = int(16756991 / self.sampleRate)

        if updateTotalLength:
            self.totalLength = len(self.data) // 4

        if self.loopOffset > self.totalLength:
            raise ValueError(f'Loop offset ({self.loopOffset}) > total length ({self.totalLength})!')

        data = bytearray()
        data.extend(_common.NDS_STD_FILE_HEADER.pack(
            b'SWAV', 0xFEFF, 0x100, 0x24 + len(self.data), 0x10, 1))
        data.extend(struct.pack(
            '<4sI', b'DATA', 0x14 + len(self.data)))
        data.extend(struct.pack(
            '<B?3HI', self.waveType, self.isLooped, self.sampleRate, self.time,
            self.loopOffset, self.totalLength - self.loopOffset))
        data.extend(self.data)
        return bytes(data)


    def saveToFile(self, filePath, *, updateTime=False, updateTotalLength=False):
        """
        Generate file data representing this SWAV, and save it to a
        filesystem file.
        """
        d = self.save(updateTime=updateTime,
                      updateTotalLength=updateTotalLength)
        with open(filePath, 'wb') as f:
            f.write(d)


    def __str__(self):
        try:
            waveType = WaveType(self.waveType).name
        except Exception:
            waveType = f'waveType={hex(self.waveType)}'

        looped = ' looped' if self.isLooped else ''

        return f'<swav {waveType} {self.sampleRate}Hz{looped}>'


    def __repr__(self):
        args = []
        args.append(_common.shortBytesRepr(self.data))
        args.append(f'waveType={self.waveType!r}')
        args.append(f'isLooped={self.isLooped!r}')
        args.append(f'sampleRate={self.sampleRate!r}')
        args.append(f'time={self.time!r}')
        args.append(f'loopOffset={self.loopOffset!r}')
        args.append(f'totalLength={self.totalLength!r}')
        return f'{type(self).__name__}.fromData({", ".join(args)})'
