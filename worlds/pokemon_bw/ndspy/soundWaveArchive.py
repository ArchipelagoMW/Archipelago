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
Support for SWAR sound wave archives.
"""

import struct

from . import WaveType
from . import _common
from . import soundWave


class SWAR:
    """
    A SWAR sound wave archive.
    """
    # When saving SDAT, two otherwise identical SWARs will share data
    # only if their dataMergeOptimizationIDs are the same.
    # You can pretty safely ignore this.
    dataMergeOptimizationID = 0

    def __init__(self, file=None, unk02=0):
        self.unk02 = unk02
        self.waves = []

        if file is not None:
            if not file.startswith(b'SWAR'):
                raise ValueError("Wrong magic (should be b'SWAR', instead "
                                 f'found {file[:4]})')

            self._initFromData(file)


    def _initFromData(self, data):
        """
        Initialize the SWAR from file data.
        """
        magic, bom, version, filesize, headersize, numblocks = \
            _common.NDS_STD_FILE_HEADER.unpack_from(data, 0)
        if version != 0x100:
            raise ValueError(f'Unsupported SWAR version: {version}')
        assert magic == b'SWAR', f'Incorrect SWAR magic ({magic})'

        dataMagic, dataSize, swavCount = \
            struct.unpack_from('<4sI32xI', data, 0x10)
        assert dataMagic == b'DATA', f'Incorrect SWAR DATA magic ({dataMagic})'

        dataArrayPos = 0x3C
        for i in range(swavCount):
            swavOffset, nextOffset = \
                struct.unpack_from('<II', data, dataArrayPos)
            dataArrayPos += 4
            if i == swavCount - 1:
                # DON'T use len(data) here -- there can sometimes be
                # extra pad at the end, which will mess this up!
                nextOffset = filesize

            swavData = data[swavOffset:nextOffset]

            waveType, loopFlag, sampleRate, time, loopOffset, totalLength = \
                struct.unpack_from('<B?3HI', swavData)

            swav = soundWave.SWAV.fromData(swavData[0xC:],
                                           waveType=WaveType(waveType),
                                           isLooped=loopFlag,
                                           sampleRate=sampleRate,
                                           time=time,
                                           loopOffset=loopOffset,
                                           totalLength=loopOffset + totalLength)
            self.waves.append(swav)


    @classmethod
    def fromWaves(cls, waves, unk02=0):
        """
        Create a SWAR from a list of SWAVs.
        """
        obj = cls(unk02=unk02)
        obj.waves = waves
        return obj


    @classmethod
    def fromFile(cls, filePath, unk02=0):
        """
        Load a SWAR from a filesystem file.
        """
        with open(filePath, 'rb') as f:
            return cls(f.read(), unk02=0)


    def save(self):
        """
        Generate file data representing this SWAR, and then return that
        data and .unk02 as a pair (2-tuple). This matches the parameters
        of the default class constructor.
        """
        fileLen = 0x3C + sum(4 + 0xC + len(s.data) for s in self.waves)

        data = bytearray()
        data.extend(_common.NDS_STD_FILE_HEADER.pack(
            b'SWAR', 0xFEFF, 0x100, fileLen, 0x10, 1))
        data.extend(struct.pack(
            '<4sI32xI', b'DATA', fileLen - 0x10, len(self.waves)))

        lenOffsetsTable = 4 * len(self.waves)
        offsets = []
        swavsTable = bytearray()

        for swav in self.waves:
            offsets.append(0x3C + lenOffsetsTable + len(swavsTable))
            swavData = swav.save()[0x18:] # Chop off the file header
                                          # but not the SWAVInfo struct
            swavsTable.extend(swavData)

        offsetsTable = struct.pack(f'<{len(offsets)}I', *offsets)
        data.extend(offsetsTable)
        data.extend(swavsTable)

        return (data, self.unk02)


    def saveToFile(self, filePath):
        """
        Generate file data representing this SWAR, and save it to a
        filesystem file.
        """
        d = self.save()[0]
        with open(filePath, 'wb') as f:
            f.write(d)


    def __str__(self):
        linesList = [f'<swar']
        linesList.extend(_common.enumeratedListOfStrs(self.waves))
        linesList.append('>')
        return '\n'.join(linesList)


    def __repr__(self):
        return f'{type(self).__name__}.fromWaves({self.waves!r})'
