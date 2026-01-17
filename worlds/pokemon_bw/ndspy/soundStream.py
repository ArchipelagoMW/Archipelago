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
Support for STRMs.
"""

import struct

from . import WaveType
from . import _common


class STRM:
    """
    A STRM streamed audio file. This is a piece of music, usually used
    for background music or jingles.
    """
    # When saving SDAT, two otherwise identical STRMs will share data
    # only if their dataMergeOptimizationIDs are the same.
    # You can pretty safely ignore this.
    dataMergeOptimizationID = 0

    def __init__(self, file=None, unk02=0, volume=127, priority=64, playerID=0, unk07=0):

        self.unk02 = unk02
        self.volume = volume
        self.priority = priority
        self.playerID = playerID
        self.unk07 = unk07

        if file is not None:
            if not file.startswith(b'STRM'):
                raise ValueError("Wrong magic (should be b'STRM', instead"
                                 f' found {file[:4]})')

            self._initFromData(file)

        else:
            self.waveType = WaveType.PCM8
            self.isLooped = False
            self.channels = []
            self.unk03 = 0
            self.sampleRate = 8000
            self.time = 0
            self.loopOffset = 0
            self.samplesPerBlock = 0
            self.samplesInLastBlock = 0
            self.unk28 = 0
            self.unk2C = 0
            self.unk30 = 0
            self.unk34 = 0
            self.unk38 = 0
            self.unk3C = 0
            self.unk40 = 0
            self.unk44 = 0


    @classmethod
    def fromChannels(cls, channels,
            unk02=0, volume=127, priority=64, playerID=0, unk07=0):
        """
        Create a STRM from a list of channels.
        """
        obj = cls(unk02=unk02, volume=volume, priority=priority,
                  playerID=playerID, unk07=unk07)
        obj.channels = channels
        return obj


    @classmethod
    def fromFile(cls, filePath, *args, **kwargs):
        """
        Load a STRM from a filesystem file.
        """
        with open(filePath, 'rb') as f:
            return cls(f.read(), *args, **kwargs)


    def _initFromData(self, file):
        """
        Initialize the STRM from file data.
        """

        magic, bom, version, filesize, headersize, numblocks = \
            _common.NDS_STD_FILE_HEADER.unpack_from(file, 0)
        if version != 0x100:
            raise ValueError(f'Unsupported STRM version: {version}')
        assert magic == b'STRM', f'Incorrect STRM magic ({magic})'

        headMagic, headSize = struct.unpack_from('<4sI', file, 0x10)
        assert headMagic == b'HEAD', f'Incorrect STRM HEAD magic ({headMagic})'

        (waveType, self.isLooped, numChannels, self.unk03,
            self.sampleRate, self.time,
            self.loopOffset,
            numSamples,
            dataOffset,
            numBlocks,
            bytesPerBlock, # per channel
            self.samplesPerBlock, # per channel
            bytesInLastBlock, # per channel
            self.samplesInLastBlock, # per channel
            self.unk28,
            self.unk2C,
            self.unk30,
            self.unk34,
            self.unk38,
            self.unk3C,
            self.unk40,
            self.unk44,
            ) = struct.unpack_from('<B?BB2H16I', file, 0x18)
        assert dataOffset == 0x68, f'Unexpected STRM data offset ({hex(dataOffset)})'
        self.waveType = WaveType(waveType)

        dataOffs = 0x10 + headSize
        dataMagic, dataSize = struct.unpack_from('<4sI', file, dataOffs)
        assert dataMagic == b'DATA', f'Incorrect STRM DATA magic ({dataMagic})'
        data = file[dataOffs + 8 : dataOffs + dataSize]

        isOneBigLongBlock = (numBlocks == 1 and waveType == WaveType.ADPCM)

        self.channels = []
        for _ in range(numChannels):
            self.channels.append([])

        offs = 0
        for bn in range(numBlocks):
            blockSize = bytesPerBlock
            if bn == numBlocks - 1:
                blockSize = bytesInLastBlock

            if isOneBigLongBlock:
                blockSize += 4

            for cn in range(numChannels):
                self.channels[cn].append(data[offs : offs + blockSize])
                offs += blockSize

            while offs % 4: offs += 1


    def save(self, *, updateTime=False):
        """
        Generate file data representing this STRM, and then return that
        data, .unk02, .volume, .priority, .playerID, and .unk07, as a
        6-tuple. This matches the parameters of the default class
        constructor.
        """

        # Figure out the number of blocks, bytes per block, and bytes in
        # the last block (while also checking that these are consistent
        # across channels as they should be)
        numBlocks = bytesPerBlock = bytesInLastBlock = 0

        if self.channels:
            numBlocks = len(self.channels[0])

            # All channels should have the same number of blocks
            for i, blocks in enumerate(self.channels):
                if len(blocks) != numBlocks:
                    raise ValueError(f'Channels 1 and {i + 1} have'
                        f' different numbers of blocks ({numBlocks} vs'
                        f' {len(blocks)})!')

            if numBlocks > 0:
                bytesPerBlock = len(self.channels[0][0])
                bytesInLastBlock = len(self.channels[0][-1])

                # All channels should have all but the final block be
                # bytesPerBlock bytes long, and the last one be
                # bytesInLastBlock long
                for i, blocks in enumerate(self.channels):
                    for j, b in enumerate(blocks[:-1]): # ignore last block
                        if len(b) != bytesPerBlock:
                            raise ValueError('Detected block size is'
                                f' {bytesPerBlock}, but block {j + 1} in'
                                f' channel {i + 1} is {len(b)} bytes'
                                ' long!')

                    b = blocks[-1]
                    if len(b) != bytesInLastBlock:
                        raise ValueError('Detected last block size is'
                            f' {bytesInLastBlock}, but the last block in'
                            f' channel {i + 1} is {len(b)} bytes'
                            ' long!')

        # Construct the wave data
        waveData = bytearray()
        for blocks in zip(*self.channels):
            for b in blocks:
                waveData.extend(b)
            while len(waveData) % 4: waveData.append(0)

        # Construct the file data
        data = bytearray()
        data.extend(_common.NDS_STD_FILE_HEADER.pack(
            b'STRM', 0xFEFF, 0x100, 0x68 + len(waveData), 0x10, 2))

        if updateTime:
            self.time = int(1.0 / self.sampleRate * 16756991 / 32)

        adpcmBlockSizeAdjust = 0
        if self.waveType == WaveType.ADPCM and numBlocks == 1:
            adpcmBlockSizeAdjust = 4

        data.extend(struct.pack(
            '<4sI', b'HEAD', 0x50))
        data.extend(struct.pack('<B?BB2H16I',
            self.waveType, self.isLooped, len(self.channels), self.unk03,
            self.sampleRate, self.time,
            self.loopOffset,
            (numBlocks - 1) * self.samplesPerBlock + self.samplesInLastBlock,
            0x68,
            numBlocks,
            bytesPerBlock - adpcmBlockSizeAdjust,
            self.samplesPerBlock,
            bytesInLastBlock - adpcmBlockSizeAdjust,
            self.samplesInLastBlock,
            self.unk28,
            self.unk2C,
            self.unk30,
            self.unk34,
            self.unk38,
            self.unk3C,
            self.unk40,
            self.unk44,
            ))

        data.extend(struct.pack(
            '<4sI', b'DATA', 8 + len(waveData)))
        data.extend(waveData)

        return (bytes(data),
                self.unk02,
                self.volume,
                self.priority,
                self.playerID,
                self.unk07)


    def saveToFile(self, filePath, *, updateTime=False):
        """
        Generate file data representing this STRM, and save it to a
        filesystem file.
        """
        d = self.save(updateTime=updateTime)[0]
        with open(filePath, 'wb') as f:
            f.write(d)


    def __str__(self):
        if self.channels:
            if all(len(c) == len(self.channels[0]) for c in self.channels):
                num = len(self.channels[0])
                word = 'block' if num == 1 else 'blocks'
                blockInfo = f'of {num} {word} each'
            else:
                blockInfo = 'of differing numbers of blocks each'

            num = len(self.channels)
            word = 'channel' if num == 1 else 'channels'
            channelsInfo = f'[{num} {word} {blockInfo}]'

        else:
            channelsInfo = '[0 channels]'

        try:
            waveType = WaveType(self.waveType).name
        except Exception:
            waveType = f'waveType={hex(self.waveType)}'

        looped = ' looped' if self.isLooped else ''

        return f'<strm {waveType} {self.sampleRate}Hz {channelsInfo} volume={self.volume}{looped}>'


    def __repr__(self):
        c = ['[']
        if self.channels:
            c.append('[')
            if self.channels[0]:
                c.append(_common.shortBytesRepr(self.channels[0][0]))
                if len(self.channels[0]) > 1:
                    c.append(', ...')
            c.append(']')
            if len(self.channels) > 1:
                c.append(', ...')
        c.append(']')
        c = ''.join(c)

        return (f'{type(self).__name__}.fromChannels({c}'
                f', {self.unk02!r}, {self.volume!r}, {self.priority!r}'
                f', {self.playerID!r}, {self.unk07!r})')
