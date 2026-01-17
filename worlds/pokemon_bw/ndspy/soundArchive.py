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
Support for SDAT sound archives.
"""


import itertools
import struct

from . import _common
from . import soundBank
from . import soundGroup
from . import soundSequence
from . import soundSequenceArchive
from . import soundSequencePlayer
from . import soundStream
from . import soundStreamPlayer
from . import soundWaveArchive


class SDAT:
    """
    A sound data archive file (SDAT).
    """
    def __init__(self, data=None):
        self.sequences = []
        self.sequenceArchives = []
        self.banks = []
        self.waveArchives = []
        self.sequencePlayers = []
        self.groups = []
        self.streamPlayers = []
        self.streams = []

        self.fatLengthsIncludePadding = False
        self.firstFileAlignment = None
        self.fileAlignment = 0x20
        self.padAtEnd = True # only inaccurate 3rd party tools change
                             # this from the default, but we support it
                             # anyway
        self.padSymbSizeTo4InSDATHeader = False # same as above

        if data is not None:
            self._initFromData(data)


    def _initFromData(self, data):
        """
        Initialize the SDAT using the raw file data given.
        """
        # Read the standard header
        magic, bom, version, filesize, headersize, numblocks = \
            _common.NDS_STD_FILE_HEADER.unpack_from(data, 0)
        if version != 0x100:
            raise ValueError(f'Unsupported SDAT version: {version}')

        if magic != b'SDAT':
            raise ValueError("Wrong magic (should be b'SDAT', instead found "
                             f'{magic})')

        # Read the block offsets and sizes
        (symbolsBlockOffset, symbolsBlockSize,
            infoBlockOffset, infoBlockSize,
            fatBlockOffset, fatBlockSize,
            fileBlockOffset, fileBlockSize,
            ) = struct.unpack_from('<8I', data, 0x10)

        # Read the symbols block
        (symbolsMagic, symbolsSize) = \
            struct.unpack_from('<4sI', data, symbolsBlockOffset)

        if symbolsBlockOffset != 0:
            symbolsOffsets = struct.unpack_from('<8I', data,
                                                symbolsBlockOffset + 8)
            assert symbolsMagic == b'SYMB', f'Incorrect SDAT SYMB magic ({symbolsMagic})'
        else:
            symbolsOffsets = [None] * 8


        lastEndOfString = 0 # relative to SYMB block
        def readSymbolsList(offset, hasSubgroups):
            """
            Read a list of symbols at offset offset. If hasSubgroups,
            it'll be parsed assuming that the symbol table has entries
            for sub-symbol-lists as well. (In practice, this only occurs
            for SSARs.)
            If there are no symbols, return an empty list.
            """
            nonlocal lastEndOfString

            if offset is None: return []

            off = symbolsBlockOffset + offset
            count, = struct.unpack_from('<I', data, off); off += 4

            symbols = []
            for i in range(count):
                symbolOff, = struct.unpack_from('<I', data, off)
                off += 4

                if symbolOff == 0:
                    thisSymbol = None
                else:
                    thisSymbol = _common.loadNullTerminatedStringFrom(data,
                        symbolsBlockOffset + symbolOff)
                    lastEndOfString = symbolOff + len(thisSymbol) + 1

                if not hasSubgroups:
                    symbols.append(thisSymbol)
                else:
                    subSymbolsOff, = struct.unpack_from('<I', data, off)
                    off += 4

                    if subSymbolsOff == 0:
                        subSymbols = []
                    else:
                        subSymbols = readSymbolsList(subSymbolsOff, False)

                    symbols.append((thisSymbol, subSymbols))
            
            return symbols


        # Read the FAT block
        (fatMagic, fatSize, fatCount) = \
            struct.unpack_from('<4sII', data, fatBlockOffset)
        assert fatMagic == b'FAT ', f'Incorrect SDAT "FAT " magic ({fatMagic})' # note trailing space

        # Read the files from the FILES block
        files = []
        fatArrayPos = fatBlockOffset + 0x0C
        self.fileAlignment = 0x200
        self.fatLengthsIncludePadding = True
        finalFileEnd = fileBlockOffset + 8
        for i in range(fatCount):
            (fileOffset, fileSize) = \
                struct.unpack_from('<II', data, fatArrayPos)
            fatArrayPos += 0x10 # There's 8 pad bytes.

            # We'll need this later
            finalFileEnd = fileOffset + fileSize

            if i != fatCount - 1:
                nextOffset, = struct.unpack_from('<I', data, fatArrayPos)
                paddedSize = nextOffset - fileOffset
                if paddedSize != fileSize:
                    self.fatLengthsIncludePadding = False

            # Most SDATs require files to be padded to 0x20, but some
            # use other amounts. We check for that here, so that we can
            # rebuild it correctly later.
            if fileOffset % 0x200 == 0x100:
                self.fileAlignment = min(self.fileAlignment, 0x100)
            if fileOffset % 0x100 == 0x80:
                self.fileAlignment = min(self.fileAlignment, 0x80)
            if fileOffset % 0x80 == 0x40:
                self.fileAlignment = min(self.fileAlignment, 0x40)
            if fileOffset % 0x40 == 0x20:
                self.fileAlignment = min(self.fileAlignment, 0x20)
            if fileOffset % 0x20 == 0x10:
                self.fileAlignment = min(self.fileAlignment, 0x10)
            if fileOffset % 0x10 == 8:
                self.fileAlignment = min(self.fileAlignment, 8)
            if fileOffset % 8 == 4:
                self.fileAlignment = min(self.fileAlignment, 4)
            if fileOffset % 4 == 2:
                self.fileAlignment = min(self.fileAlignment, 2)
            if fileOffset % 2 == 1: # yes, this happens sometimes
                self.fileAlignment = min(self.fileAlignment, 1)

            if i == 0:
                self.firstFileAlignment = self.fileAlignment

            file = data[fileOffset : fileOffset + fileSize]
            files.append(file)

        if self.firstFileAlignment == self.fileAlignment:
            self.firstFileAlignment = None

        # Check if the end is definitely unpadded (that is, if there
        # should be padding and it's not present)
        if finalFileEnd == len(data) and finalFileEnd % self.fileAlignment != 0:
            self.padAtEnd = False

        # Do another quick pass to find if the FAT file lengths include
        # padding

        # Read the info block
        (infoMagic, infoSize) = \
            struct.unpack_from('<4sI', data, infoBlockOffset)
        infoOffsets = struct.unpack_from('<8I', data,
                                         infoBlockOffset + 8)
        assert infoMagic == b'INFO', f'Incorrect SDAT INFO magic ({infoMagic})'

        def getInfoEntryOffsets(partNum):
            off = infoOffsets[partNum]
            count, = struct.unpack_from('<I', data, infoBlockOffset + off)
            entryOffsets = struct.unpack_from(f'<{count}I', data,
                                              infoBlockOffset + off + 4)
            for entryOff in entryOffsets:
                if entryOff == 0:
                    yield None
                else:
                    yield infoBlockOffset + entryOff


        # Info part 0: SSEQ (references SBNK)
        for entryOff, symb in itertools.zip_longest(getInfoEntryOffsets(0),
                                  readSymbolsList(symbolsOffsets[0], False)):
            if entryOff is None:
                sseq = None
            else:
                (fileID, unk02, bankID, volume, channelPressure,
                    polyphonicPressure, playerID) = \
                    struct.unpack_from('<3H4B', data, entryOff)
                sseq = soundSequence.SSEQ(files[fileID], unk02, bankID,
                            volume, channelPressure, polyphonicPressure, playerID)
                sseq.dataMergeOptimizationID = fileID

            self.sequences.append((symb, sseq))

        # Info part 1: SSAR
        for entryOff, symb in itertools.zip_longest(getInfoEntryOffsets(1),
                                  readSymbolsList(symbolsOffsets[1], True)):
            if entryOff is None:
                ssar = None
            else:
                fileID, unk02 = struct.unpack_from('<HH', data, entryOff)
                subSymb = symb[1] if symb is not None else None
                ssar = soundSequenceArchive.SSAR(files[fileID], unk02, subSymb)
                ssar.dataMergeOptimizationID = fileID

            name = symb[0] if symb is not None else None
            self.sequenceArchives.append((name, ssar))

        # Info part 2: SBNK
        for entryOff, symb in itertools.zip_longest(getInfoEntryOffsets(2),
                                  readSymbolsList(symbolsOffsets[2], False)):
            if entryOff is None:
                sbnk = None
            else:
                fileID, unk02 = struct.unpack_from('<HH', data, entryOff)
                swarIDs = struct.unpack_from('<4h', data, entryOff + 4)
                swarIDs2 = []
                for x in swarIDs:
                    if x == -1:
                        swarIDs2.append(None)
                    else:
                        swarIDs2.append(x)

                sbnk = soundBank.SBNK(files[fileID], unk02, swarIDs2)
                sbnk.dataMergeOptimizationID = fileID

            self.banks.append((symb, sbnk))

        # Info part 3: SWAR
        for entryOff, symb in itertools.zip_longest(getInfoEntryOffsets(3),
                                  readSymbolsList(symbolsOffsets[3], False)):
            if entryOff is None:
                swar = None
            else:
                fileID, unk02 = struct.unpack_from('<HH', data, entryOff)
                swar = soundWaveArchive.SWAR(files[fileID], unk02)
                swar.dataMergeOptimizationID = fileID

            self.waveArchives.append((symb, swar))

        # Info part 4: Sequence players
        for entryOff, symb in itertools.zip_longest(getInfoEntryOffsets(4),
                                  readSymbolsList(symbolsOffsets[4], False)):
            if entryOff is None:
                sp = None
            else:
                maxSequences, channelMask, heapSize = \
                    struct.unpack_from('<HHI', data, entryOff)

                channels = set()
                for i in range(16):
                    if (channelMask >> i) & 1:
                        channels.add(i)

                sp = soundSequencePlayer.SequencePlayer(maxSequences,
                                                   channels,
                                                   heapSize)

            self.sequencePlayers.append((symb, sp))

        # Info part 5: Groups
        for groupOff, symb in itertools.zip_longest(getInfoEntryOffsets(5),
                                  readSymbolsList(symbolsOffsets[5], False)):
            if groupOff is None:
                entries = None
            else:
                entriesCount, = struct.unpack_from('<I', data, groupOff)

                entries = []
                arrayOff = groupOff + 4
                for i in range(entriesCount):
                    type, options, id = struct.unpack_from('<BHxI', data, arrayOff)
                    arrayOff += 8

                    entries.append(soundGroup.GroupEntry(type, options, id))

            self.groups.append((symb, entries))

        # Info part 6: Stream players
        for entryOff, symb in itertools.zip_longest(getInfoEntryOffsets(6),
                                  readSymbolsList(symbolsOffsets[6], False)):
            if entryOff is None:
                sp = None
            else:
                count, = struct.unpack_from('<B', data, entryOff)
                channels = list(
                    struct.unpack_from(f'<{count}B', data, entryOff + 1))
                sp = soundStreamPlayer.StreamPlayer(channels)

            self.streamPlayers.append((symb, sp))

        # Info part 7: Streams
        for entryOff, symb in itertools.zip_longest(getInfoEntryOffsets(7),
                                  readSymbolsList(symbolsOffsets[7], False)):
            if entryOff is None:
                strm = None
            else:
                fileID, unk02, volume, priority, playerID, unk07 = \
                    struct.unpack_from('<HH4B', data, entryOff)
                strm = soundStream.STRM(files[fileID], unk02, volume, priority, playerID, unk07)
                strm.dataMergeOptimizationID = fileID

            self.streams.append((symb, strm))


        # If the symbols block size is definitely padded, record that
        if symbolsBlockSize % 4 == 0 and lastEndOfString % 4 != 0:
            self.padSymbSizeTo4InSDATHeader = True


    @classmethod
    def fromFile(cls, filePath):
        """
        Load an SDAT from a filesystem file.
        """
        with open(filePath, 'rb') as f:
            return cls(f.read())


    def save(self):
        """
        Generate file data representing this SDAT.
        """
        # First, just allocate enough memory for the SDAT header.
        data = bytearray(0x40)

        # -------------------
        # Make the SYMB block

        symbolsStringTable = bytearray()
        def addSymbolAndGetOffset(symbol):
            if symbol is None:
                return -1
            offset = len(symbolsStringTable)
            symbolsStringTable.extend(symbol.encode('latin-1') + b'\0')
            return offset

        symbolsHeaderOffsets = []

        # Parallel arrays, here.
        symbolsTableValues = []
        shouldIncrementByTableLen = []

        anySymbolsInWholeFile = False

        def addSymbolsFrom(namedList, nested=False):

            # First, figure out if any actual symbols exist
            anyActualSymbols = False
            anyActualSubsymbols = False
            if not nested:
                for symbol, _ in namedList:
                    if symbol is not None:
                        anyActualSymbols = True
                        break
            else:
                for symbol, entry in namedList:
                    if symbol is not None:
                        anyActualSymbols = True
                        break
                    for subSymbol, subEntry in entry.sequences:
                        if subSymbol is not None:
                            anyActualSubsymbols = True
                            break


            nonlocal anySymbolsInWholeFile
            anySymbolsInWholeFile |= anyActualSymbols
            anySymbolsInWholeFile |= anyActualSubsymbols

            # If there *are* any symbols, keep going
            symbolsHeaderOffsets.append(len(symbolsTableValues) * 4)

            if not nested:
                symbolsTableValues.append(len(namedList))
                shouldIncrementByTableLen.append(False)

                for symbol, _ in namedList:
                    symbolsTableValues.append(addSymbolAndGetOffset(symbol))
                    shouldIncrementByTableLen.append(True)

            else:
                mainList, subListsArea = [], []
                mainListSIBTL, subListsAreaSIBTL = [], []

                mainList.append(len(namedList))
                mainListSIBTL.append(False)

                mainListFullLength = (1 + 2 * len(namedList)) * 4
                subListsAreaOffset = (0x40
                                      + len(symbolsTableValues) * 4
                                      + mainListFullLength)

                for symbol, entry in namedList:

                    mainList.append(addSymbolAndGetOffset(symbol))
                    mainListSIBTL.append(True)

                    subListOffset = subListsAreaOffset + len(subListsArea) * 4

                    if entry is None:
                        subNames = []
                    else:
                        subNames = [n for (n, s) in entry.sequences]

                    if entry or subNames:
                        subListsArea.append(len(subNames))
                        subListsAreaSIBTL.append(False)

                        for subSymbol in subNames:
                            subListsArea.append(addSymbolAndGetOffset(subSymbol))
                            subListsAreaSIBTL.append(True)

                        mainList.append(subListOffset)
                        mainListSIBTL.append(False)

                    else:
                        mainList.append(0)
                        mainListSIBTL.append(False)

                symbolsTableValues.extend(mainList)
                symbolsTableValues.extend(subListsArea)
                shouldIncrementByTableLen.extend(mainListSIBTL)
                shouldIncrementByTableLen.extend(subListsAreaSIBTL)

        addSymbolsFrom(self.sequences)
        addSymbolsFrom(self.sequenceArchives, True)
        addSymbolsFrom(self.banks)
        addSymbolsFrom(self.waveArchives)
        addSymbolsFrom(self.sequencePlayers)
        addSymbolsFrom(self.groups)
        addSymbolsFrom(self.streamPlayers)
        addSymbolsFrom(self.streams)

        # Only add the SYMB block if there are any symbols
        if anySymbolsInWholeFile:
            symbolsBlockOffset = len(data)

            symbolsTableLen = len(symbolsTableValues) * 4
            symbolsTable = bytearray()
            for value, shouldIncrement in itertools.zip_longest(symbolsTableValues,
                                              shouldIncrementByTableLen):
                if value == -1:
                    symbolsTable.extend(b'\0\0\0\0')
                else:
                    if shouldIncrement:
                        value += symbolsTableLen + 0x40
                    symbolsTable.extend(struct.pack('<I', value))

            symbolsBlockSize = 0x40 + len(symbolsTable) + len(symbolsStringTable)
            paddedSymbSize = symbolsBlockSize
            while paddedSymbSize % 4:
                paddedSymbSize += 1
            if self.padSymbSizeTo4InSDATHeader:
                symbolsBlockSize = paddedSymbSize

            symbolsHeaderOffsetsTable = bytearray()
            for value in symbolsHeaderOffsets:
                if value is None:
                    symbolsHeaderOffsetsTable.extend(b'\0\0\0\0')
                else:
                    symbolsHeaderOffsetsTable.extend(struct.pack('<I', value + 0x40))

            symbolsHeader = struct.pack('<4sI',
                b'SYMB', paddedSymbSize)

            data.extend(symbolsHeader)
            data.extend(symbolsHeaderOffsetsTable)
            data.extend(b'\0' * 0x18)
            data.extend(symbolsTable)
            data.extend(symbolsStringTable)

        else:
            symbolsBlockOffset = None
            symbolsBlockSize = None


        # -------------------
        # Make the INFO block
        while len(data) % 4: data.append(0)
        infoBlockOffset = len(data)

        # Add room to add the header later
        data.extend(b'\0' * (8 + 8 * 4))

        # Pad to 0x20 relative to the INFO block, for some reason
        while (len(data) - infoBlockOffset) % 0x20: data.append(0)

        # Helper functions
        def info_declarePart(partNumber):
            struct.pack_into('<I', data, infoBlockOffset + 8 + 4 * partNumber,
                len(data) - infoBlockOffset)
        def addFileAndGetID(file, dataMergeOptimizationID):
            idx = _common.listFind(files, file)

            while idx != -1:
                if dataMergeOptimizationID == fileMergeIDs[idx]:
                    return idx
                idx = _common.listFind(files, file, idx + 1)

            files.append(file)
            fileMergeIDs.append(dataMergeOptimizationID)
            return len(files) - 1

        # We encode sections out of order, so that the files will be in
        # the same order as in retail SDATs.
        fileMergeIDs = []
        files = []

        # Info part 0: SSEQ
        info_declarePart(0)

        data.extend(struct.pack('<I', len(self.sequences)))
        sseqOffsetsTableOffset = len(data)
        data.extend(b'\0' * (4 * len(self.sequences)))

        for i, (_, sseq) in enumerate(self.sequences):
            if sseq is None:
                entryOff = 0
            else:
                entryOff = len(data) - infoBlockOffset

                (file, unk02, bankID, volume, channelPressure,
                    polyphonicPressure, playerID) = sseq.save()
                fileID = addFileAndGetID(file, sseq.dataMergeOptimizationID)

                data.extend(struct.pack('<3H4Bxx',
                    fileID, unk02, bankID, volume, channelPressure,
                    polyphonicPressure, playerID))

            struct.pack_into('<I', data, sseqOffsetsTableOffset + 4 * i, entryOff)

        # Info part 1: SSAR
        info_declarePart(1)

        data.extend(struct.pack('<I', len(self.sequenceArchives)))
        ssarOffsetsTableOffset = len(data)
        data.extend(b'\0' * (4 * len(self.sequenceArchives)))

        for i, (_, ssar) in enumerate(self.sequenceArchives):
            if ssar is None:
                entryOff = 0
            else:
                entryOff = len(data) - infoBlockOffset

                file, unk02, _ = ssar.save()
                fileID = addFileAndGetID(file, ssar.dataMergeOptimizationID)

                data.extend(struct.pack('<HH',
                    fileID, unk02))

            struct.pack_into('<I', data, ssarOffsetsTableOffset + 4 * i, entryOff)

        # Info part 2: SBNK
        info_declarePart(2)

        data.extend(struct.pack('<I', len(self.banks)))
        sbnkOffsetsTableOffset = len(data)
        data.extend(b'\0' * (4 * len(self.banks)))

        for i, (sbnkName, sbnk) in enumerate(self.banks):
            if sbnk is None:
                entryOff = 0
            else:
                entryOff = len(data) - infoBlockOffset

                file, unk02, waveArchives = sbnk.save()
                fileID = addFileAndGetID(file, sbnk.dataMergeOptimizationID)

                swarIDs = []
                for s in waveArchives:
                    swarIDs.append(-1 if s is None else s)
                while len(swarIDs) < 4:
                    swarIDs.append(-1)

                if len(swarIDs) > 4:
                    raise ValueError(f'SBNK {i} ("{sbnkName}") uses '
                        f'{len(swarIDs)} SWARs. The maximum is 4.')

                data.extend(struct.pack('<HH4h',
                    fileID, unk02, *swarIDs))

            struct.pack_into('<I', data, sbnkOffsetsTableOffset + 4 * i, entryOff)


        # Info part 3: SWAR
        info_declarePart(3)

        data.extend(struct.pack('<I', len(self.waveArchives)))
        swarOffsetsTableOffset = len(data)
        data.extend(b'\0' * (4 * len(self.waveArchives)))

        for i, (_, swar) in enumerate(self.waveArchives):
            if swar is None:
                entryOff = 0
            else:
                entryOff = len(data) - infoBlockOffset

                file, unk02 = swar.save()
                fileID = addFileAndGetID(file, swar.dataMergeOptimizationID)

                data.extend(struct.pack('<HH',
                    fileID, unk02))

            struct.pack_into('<I', data, swarOffsetsTableOffset + 4 * i, entryOff)


        # Info part 4: Sequence players
        info_declarePart(4)

        data.extend(struct.pack('<I', len(self.sequencePlayers)))
        spOffsetsTableOffset = len(data)
        data.extend(b'\0' * (4 * len(self.sequencePlayers)))

        for i, (_, sp) in enumerate(self.sequencePlayers):
            if sp is None:
                entryOff = 0
            else:
                entryOff = len(data) - infoBlockOffset

                maxSequences, channels, heapSize = sp.save()

                channelMask = 0
                for j in range(16):
                    if j in channels:
                        channelMask |= 1 << j

                data.extend(struct.pack('<HHI',
                    maxSequences, channelMask, heapSize))

            struct.pack_into('<I', data, spOffsetsTableOffset + 4 * i, entryOff)


        # Info part 5: Groups
        info_declarePart(5)

        data.extend(struct.pack('<I', len(self.groups)))
        groupOffsetsTableOffset = len(data)
        data.extend(b'\0' * (4 * len(self.groups)))

        for i, (_, group) in enumerate(self.groups):
            if group is None:
                entryOff = 0
            else:
                entryOff = len(data) - infoBlockOffset

                data.extend(struct.pack('<I', len(group)))

                for gEntry in group:
                    data.extend(struct.pack('<BHxI', *gEntry.save()))

            struct.pack_into('<I', data, groupOffsetsTableOffset + 4 * i, entryOff)


        # Info part 6: Stream players
        info_declarePart(6)

        data.extend(struct.pack('<I', len(self.streamPlayers)))
        spOffsetsTableOffset = len(data)
        data.extend(b'\0' * (4 * len(self.streamPlayers)))

        for i, (_, sp) in enumerate(self.streamPlayers):
            if sp is None:
                entryOff = 0
            else:
                entryOff = len(data) - infoBlockOffset

                channels = sp.save()
                chanCount = len(channels)
                while len(channels) < 16:
                    channels.append(0xFF)

                data.append(chanCount)
                data.extend(channels)

                # This has to occur in order for the padding to work out
                # correctly. Weird, but, what can you do. Might even be
                # an unknown value.
                data.extend(b'\0\0\0\0')

            struct.pack_into('<I', data, spOffsetsTableOffset + 4 * i, entryOff)

            while len(data) % 4: data.append(0)


        # Info part 7: Streams
        info_declarePart(7)

        data.extend(struct.pack('<I', len(self.streams)))
        strmOffsetsTableOffset = len(data)
        data.extend(b'\0' * (4 * len(self.streams)))

        for i, (_, strm) in enumerate(self.streams):
            if strm is None:
                entryOff = 0
            else:
                entryOff = len(data) - infoBlockOffset

                file, unk02, volume, priority, playerID, unk07 = strm.save()
                fileID = addFileAndGetID(file, strm.dataMergeOptimizationID)

                data.extend(struct.pack('<HH4B4x',
                    fileID, unk02, volume, priority, playerID, unk07))

            struct.pack_into('<I', data, strmOffsetsTableOffset + 4 * i, entryOff)

        # Now we can finally fill the header in.
        struct.pack_into('<4sI', data, infoBlockOffset,
            b'INFO', len(data) - infoBlockOffset)

        infoBlockSize = len(data) - infoBlockOffset


        # ----------------------
        # Make a dummy FAT block, to be filled in when adding to the
        # FILE block

        while len(data) % 4: data.append(0)
        fatBlockOffset = len(data)
        fatBlockSize = 0xC + 0x10 * len(files)
        fatTableOffset = fatBlockOffset + 0xC

        fatHeader = struct.pack('<4sII',
            b'FAT ', 0xC + 0x10 * len(files), len(files))

        data.extend(fatHeader)
        data.extend(b'\0' * (0x10 * len(files)))


        # -------------------
        # Make the FILE block and fill in the FAT block
        while len(data) % 4: data.append(0)
        fileBlockOffset = len(data)

        # Dummy header (to be filled in after we know the total size)
        data.extend(b'\0' * 0xC)

        # Some games align the first file differently
        if self.firstFileAlignment is not None:
            while len(data) % self.firstFileAlignment:
                data.append(0)

        # Add each file
        for i, file in enumerate(files):

            # Files must be aligned to 0x20 relative to the SDAT
            # itself... usually. Some games align to other amounts.
            while len(data) % self.fileAlignment:
                data.append(0)

            # Actually add the file
            fileOffset = len(data)
            data.extend(file)
            
            # Add the appropriate FAT entry
            fLen = len(file)
            if self.fatLengthsIncludePadding:
                while fLen % self.fileAlignment: fLen += 1

            struct.pack_into('<II', data, fatTableOffset + 0x10 * i,
                fileOffset, fLen)

        # And one last pad for good measure. (And because retail files
        # do so.)
        if self.padAtEnd:
            while len(data) % self.fileAlignment:
                data.append(0)

        # Add the header
        struct.pack_into('<4sII', data, fileBlockOffset,
            b'FILE', len(data) - fileBlockOffset, len(files))

        fileBlockSize = len(data) - fileBlockOffset


        # -----------------------
        # Put the blocks together

        # Write the SDAT header
        struct.pack_into('<8I', data, 0x10,
            0 if symbolsBlockOffset is None else symbolsBlockOffset,
            0 if symbolsBlockSize is None else symbolsBlockSize,
            0 if infoBlockOffset is None else infoBlockOffset,
            0 if infoBlockSize is None else infoBlockSize,
            0 if fatBlockOffset is None else fatBlockOffset,
            0 if fatBlockSize is None else fatBlockSize,
            0 if fileBlockOffset is None else fileBlockOffset,
            0 if fileBlockSize is None else fileBlockSize)

        # Write the standard header to the beginning
        _common.NDS_STD_FILE_HEADER.pack_into(data, 0,
            b'SDAT', 0xFEFF, 0x100, len(data), 0x40,
            3 if symbolsBlockOffset is None else 4)

        return data


    def saveToFile(self, filePath):
        """
        Generate file data representing this SDAT, and save it to a
        filesystem file.
        """
        d = self.save()
        with open(filePath, 'wb') as f:
            f.write(d)


    def __str__(self):
        return (f'<sdat'
                f' {len(self.sequences)} sequences'
                f' {len(self.sequenceArchives)} sequence archives'
                f' {len(self.banks)} banks'
                f' {len(self.waveArchives)} wave archives'
                f' {len(self.sequencePlayers)} sequence players'
                f' {len(self.groups)} groups'
                f' {len(self.streamPlayers)} stream players'
                f' {len(self.streams)} streams>')


    def __repr__(self):
        try:
            data = _common.shortBytesRepr(self.save())
        except Exception:
            data = '...'
        return f'{type(self).__name__}({data})'
