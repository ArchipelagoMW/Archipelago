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
Support for SSARs.
"""

import struct

from . import _common
from . import soundSequence


class SSAR:
    """
    A SSAR*sequence archive file. This contains a blob of sequence
    events data, and a list of "sequences" that are essentially just
    pointers to starting locations in that data.
    """
    # When saving SDAT, two otherwise identical SSARs will share data
    # only if their dataMergeOptimizationIDs are the same.
    # You can pretty safely ignore this.
    dataMergeOptimizationID = 0

    _events = None
    sequences = None

    def __init__(self, file=None, unk02=0, names=None):
        self.unk02 = unk02

        self.sequences = []

        if file is not None:
            if not file.startswith(b'SSAR'):
                raise ValueError("Wrong magic (should be b'SSAR', instead"
                                 f' found {file[:4]})')

            # Read SSAR header
            magic, bom, version, filesize, headersize, numblocks = \
                _common.NDS_STD_FILE_HEADER.unpack_from(file, 0)
            if version != 0x100:
                raise ValueError(f'Unsupported SSAR version: {version}')
            assert magic == b'SSAR', f'Incorrect SSAR magic ({magic})'

            # Read DATA block header
            dataMagic, dataSize, dataOffset, dataCount = \
                struct.unpack_from('<4s3I', file, 0x10)
            assert dataMagic == b'DATA', f'Incorrect SSAR DATA magic ({dataMagic})'

            # Pad the length of the names list to the number of
            # sequences
            names = list(names) if names is not None else []
            while len(names) < dataCount:
                names.append(None)

            self.eventsData = file[dataOffset:filesize]

            dataArrayPos = 0x20
            for i in range(dataCount):
                (sequenceOffset, bankID, volume, channelPressure,
                        polyphonicPressure, playerID) = \
                    struct.unpack_from('<iH4B', file, dataArrayPos)
                dataArrayPos += 0xC

                seq = SSARSequence(sequenceOffset, bankID, volume,
                    channelPressure, polyphonicPressure, playerID,
                    parsed=False)

                self.sequences.append((names[i], seq))

            self.parsed = False
        else:
            self._events = []
            self.parsed = True


    @classmethod
    def fromEventsAndSequences(cls, events, sequences, unk02=0):
        """
        Create a new SSAR object from a list of sequence events and a
        list of sequences.
        """
        obj = cls(unk02=unk02)
        obj.events = events
        obj.sequences = sequences
        return obj


    @classmethod
    def fromFile(cls, filePath, *args, **kwargs):
        """
        Load an SSAR from a filesystem file.
        """
        with open(filePath, 'rb') as f:
            return cls(f.read(), *args, **kwargs)


    @property
    def events(self):
        if not self.parsed:
            raise ValueError('You must parse the SSAR with .parse()'
                             ' before you can access .events!')
        return self._events
    @events.setter
    def events(self, value):
        self._events = value


    @property
    def eventsData(self):
        if self.parsed:
            raise ValueError('You cannot use .eventsData after you have'
                             ' parsed the SSAR!')
        return self._eventsData
    @eventsData.setter
    def eventsData(self, value):
        self._eventsData = value


    def parse(self):
        """
        Attempt to process .eventsData to create .events. If successful,
        this switches the SSAR from the unparsed to the parsed state.
        """
        if self.parsed: return
        self._initFromData(self._eventsData)
        self.parsed = True
        del self._eventsData


    def _initFromData(self, eventsData):
        """
        Finish initializing the SSAR using events data.
        """

        startOffs = []
        startOffs2Seq = {}
        for i, (seqName, seq) in enumerate(self.sequences):
            if seq.firstEventOffset not in [-1, None]:
                startOffs.append(seq.firstEventOffset)

                # Put lists in the dictionary, because there can be
                # multiple sequences referencing the same offset
                if seq.firstEventOffset not in startOffs2Seq:
                    startOffs2Seq[seq.firstEventOffset] = []
                startOffs2Seq[seq.firstEventOffset].append(seq)

        self.events, startEvents = soundSequence.readSequenceEvents(
            eventsData, startOffs)

        for event, originalOff in zip(startEvents, startOffs):
            for seq in startOffs2Seq[originalOff]:
                # These have to happen in this order
                seq.parsed = True
                seq.firstEvent = event


    def save(self):
        """
        Generate file data representing this SSAR, and then return that
        data, .unk02, and a list of sequence names as a triple. This
        matches the parameters of the default class constructor.
        """

        tableData = bytearray()

        if self.parsed:
            startEvents = []
            seq2StartEvent = {}
            for seqName, seq in self.sequences:
                if not seq.parsed:
                    raise ValueError('Attempting to save a parsed SSAR, but'
                                     f' {seqName} is not parsed!')

                if seq.firstEvent is not None:
                    startEvents.append(seq.firstEvent)
                    seq2StartEvent[seq] = seq.firstEvent
            eventsData, startOffs = soundSequence.saveSequenceEvents(self.events,
                                                                   startEvents)

            for seqName, seq in self.sequences:
                if seq in seq2StartEvent:
                    off = startOffs[startEvents.index(seq2StartEvent[seq])]
                else:
                    off = -1
                s = struct.pack('<iH4B2x', off, *(seq.save()[1:]))
                tableData.extend(s)

        else:
            eventsData = self.eventsData
            for seqName, seq in self.sequences:
                if seq.parsed:
                    raise ValueError('Attempting to save an unparsed SSAR, but'
                                     f' {seqName} is parsed!')

                feo = seq.firstEventOffset
                if feo is None: feo = -1
                s = struct.pack('<iH4B2x', feo, *(seq.save()[1:]))
                tableData.extend(s)

        dataOffset = 0x20 + len(self.sequences) * 0xC
        fileLen = dataOffset + len(eventsData)

        data = bytearray()
        data.extend(_common.NDS_STD_FILE_HEADER.pack(b'SSAR', 0xFEFF, 0x100, fileLen, 16, 1))

        data.extend(struct.pack('<4s3I',
            b'DATA', fileLen - 0x10, dataOffset, len(self.sequences)))

        data.extend(tableData)
        data.extend(eventsData)

        return (data,
                self.unk02,
                [seqName for (seqName, seq) in self.sequences])


    def saveToFile(self, filePath):
        """
        Generate file data representing this SSAR, and save it to a
        filesystem file.
        """
        d = self.save()[0]
        with open(filePath, 'wb') as f:
            f.write(d)


    def __str__(self):
        if not self.parsed:
            names = [str(n) for (n, s) in self.sequences]
            return f'<ssar unparsed [{", ".join(names)}]>'

        linesList = ['<ssar']
        linesList.append(soundSequence.printSequenceEventList(
            self.events,
            {seqName: seq.firstEvent for (seqName, seq) in self.sequences},
            ' ' * 4))
        linesList.append('>')
        return '\n'.join(linesList)


    def __repr__(self):
        if self.parsed:
            return f'{type(self).__name__}.fromEventsAndSequences({self.events!r}, {self.sequences!r})'

        else:
            data = _common.shortBytesRepr(self.eventsData)
            names = [str(n) for (n, s) in self.sequences]
            return f'{type(self).__name__}({data}, names={names!r})'


class SSARSequence:
    """
    A sequence within a *SSAR* sequence archive file. These generally
    contain sound effects.
    """
    def __init__(self, firstEvent_firstEventOffset, bankID=0, volume=127,
                 channelPressure=64, polyphonicPressure=50, playerID=0,
                 *, parsed=True):

        if parsed:
            self._firstEvent = firstEvent_firstEventOffset
            self.firstEventOffset = 0
        else:
            self._firstEvent = None
            if firstEvent_firstEventOffset == -1:
                firstEvent_firstEventOffset = None
            self.firstEventOffset = firstEvent_firstEventOffset

        self.bankID = bankID
        self.volume = volume
        self.channelPressure = channelPressure
        self.polyphonicPressure = polyphonicPressure
        self.playerID = playerID
        self.parsed = parsed


    @property
    def firstEvent(self):
        if not self.parsed:
            raise ValueError('You must parse the SSAR with .parse() before you'
                             ' can access .firstEvent in sequences!')
        return self._firstEvent
    @firstEvent.setter
    def firstEvent(self, value):
        self._firstEvent = value


    @property
    def firstEventOffset(self):
        if self.parsed:
            raise ValueError('You cannot access .firstEventOffset after you'
                             ' have parsed the SSAR!')
        return self._firstEventOffset
    @firstEventOffset.setter
    def firstEventOffset(self, value):
        self._firstEventOffset = value


    def save(self):
        """
        Return this SSAR sequence's first event or first event offset,
        .bankID, .volume, .channelPressure, .polyphonicPressure, and
        .playerID as a 6-tuple. This matches the parameters of the
        default class constructor.
        """
        return (self.firstEvent if self.parsed else self.firstEventOffset,
                self.bankID,
                self.volume,
                self.channelPressure,
                self.polyphonicPressure,
                self.playerID)


    def __str__(self):
        up = ' unparsed' if not self.parsed else ''
        fields = []
        fields.append(f'bank={self.bankID}')
        fields.append(f'volume={self.volume}')
        fields.append(f'playerID={self.playerID}')
        return f'<ssar-sequence{up} {" ".join(fields)}>'


    def __repr__(self):
        fields = []
        fields.append(repr(self.firstEvent if self.parsed else self.firstEventOffset))
        fields.append(repr(self.bankID))
        fields.append(repr(self.volume))
        fields.append(repr(self.channelPressure))
        fields.append(repr(self.polyphonicPressure))
        fields.append(repr(self.playerID))
        if not self.parsed:
            fields.append('parsed=False')
        return f'{type(self).__name__}({", ".join(fields)})'
