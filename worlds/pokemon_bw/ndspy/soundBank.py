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
Support for SBNK instrument banks.
"""


import enum
import struct

from . import _common


# Constants for various instrument types
NO_INSTRUMENT_TYPE = 0
SINGLE_NOTE_PCM_INSTRUMENT_TYPE = 1
SINGLE_NOTE_PSG_SQUARE_WAVE_INSTRUMENT_TYPE = 2
SINGLE_NOTE_PSG_WHITE_NOISE_INSTRUMENT_TYPE = 3
RANGE_INSTRUMENT_TYPE = 16
REGIONAL_INSTRUMENT_TYPE = 17


class NoteType(enum.IntEnum):
    """
    An enumeration that distinguishes between the three primary types of
    note definitions.
    """
    PCM = 1
    PSG_SQUARE_WAVE = 2
    PSG_WHITE_NOISE = 3


class NoteDefinition:
    """
    A note definition within a SBNK instrument.
    """
    def __init__(self, waveID_dutyCycle=0, waveArchiveIDID=0, pitch=60,
            attack=127, decay=127, sustain=127, release=127, pan=64,
            type=1):
        self.waveID = waveID_dutyCycle
        self.waveArchiveIDID = waveArchiveIDID
        self.pitch = pitch
        self.attack = attack
        self.decay = decay
        self.sustain = sustain
        self.release = release
        self.pan = pan
        if type in [1, 2, 3]: type = NoteType(type)
        self.type = type


    @property
    def dutyCycle(self):
        return self.waveID
    @dutyCycle.setter
    def dutyCycle(self, value):
        self.waveID = value
    

    @classmethod
    def fromData(cls, data, type=1):
        """
        Create a note definition from raw file data that does not
        include the type value at the beginning.
        """
        return cls(*struct.unpack_from('<HH6B', data), type)


    @classmethod
    def fromDataWithType(cls, data):
        """
        Create a note definition from raw file data that includes the
        type value at the beginning.
        """
        values = struct.unpack_from('<3H6B', data)
        return cls(*values[1:], values[0])


    def save(self):
        """
        Generate data representing this note definition, without
        including the type value.
        """
        return struct.pack('<HH6B', self.waveID, self.waveArchiveIDID,
            self.pitch, self.attack, self.decay, self.sustain,
            self.release, self.pan)


    def saveWithType(self):
        """
        Generate data representing this note definition, including the
        type value at the beginning.
        """
        return struct.pack('<H', self.type) + self.save()


    def __str__(self):
        name = _common.noteName(self.pitch)

        if self.type == NoteType.PSG_SQUARE_WAVE:
            pct = ['12.5%',
                   '25%',
                   '37.5%',
                   '50%',
                   '62.5%',
                   '75%',
                   '87.5%',
                   '0%'][self.dutyCycle & 7]
            extraInfo = f'PSG square wave: {pct} duty cycle'
        elif self.type == NoteType.PSG_WHITE_NOISE:
            extraInfo = 'PSG white noise'
        else:
            extraInfo = f'PCM: SWAR {self.waveArchiveIDID}, SWAV {self.waveID}'

        return f'<note def {name} ({extraInfo})>'


    def __repr__(self):
        params = ', '.join(repr(s) for s in
            [self.waveID, self.waveArchiveIDID, self.pitch, self.attack,
            self.decay, self.sustain, self.release, self.pan,
            self.type])
        return f'{type(self).__name__}({params})'
        


class Instrument:
    """
    An instrument within a SBNK file. This is an abstract base class,
    and should be subclassed in order to be used.
    """

    bankOrderKey = 0
    dataMergeOptimizationID = 0


    def __init__(self, type):
        """
        Initialize the instrument.
        """
        self.type = type


    @classmethod
    def fromData(cls, type, data, startOffset):
        """
        Create an instrument from raw file data.

        This method must be implemented in subclasses; this
        abstract-base-class implementation simply raises
        NotImplementedError.
        """
        raise NotImplementedError('Override fromData() in Instrument '
                                  'subclasses!')


    def save(self):
        """
        Return the instrument's type value as a 1-tuple. Subclasses may
        return longer tuples with more data; currently, all subclasses
        add a :py:class:`bytes` instance.
        """
        return (self.type,)


class SingleNoteInstrument(Instrument):
    """
    An instrument that contains one note definition and nothing else.
    This class encompasses instrument type values 1 through 15.
    """
    def __init__(self, noteDefinition):
        self.noteDefinition = noteDefinition
        super().__init__(int(noteDefinition.type))


    @property
    def type(self):
        return int(self.noteDefinition.type)
    @type.setter
    def type(self, value):
        if value in [1, 2, 3]: value = NoteType(value)
        self.noteDefinition.type = value


    @classmethod
    def fromData(cls, type, data, startOffset):
        """
        Create a single-note instrument from raw file data.
        """

        noteData = data[startOffset : startOffset + 10]
        noteDefinition = NoteDefinition.fromData(noteData, type)

        return cls(noteDefinition), 10


    def save(self):
        """
        Generate file data representing this instrument, and then return
        the instrument's type value and that data as a pair.
        """
        return super().save() + (self.noteDefinition.save(),)


    def __str__(self):
        return f'<single-note instrument {self.noteDefinition}>'


    def __repr__(self):
        return (f'{type(self).__name__}({self.noteDefinition!r})')


class RangeInstrument(Instrument):
    """
    An instrument that contains one note definition for each pitch in a
    given range.
    """
    def __init__(self, firstPitch, noteDefinitions):
        super().__init__(RANGE_INSTRUMENT_TYPE)
        self.firstPitch = firstPitch
        self.noteDefinitions = noteDefinitions


    @classmethod
    def fromData(cls, _, data, startOffset):
        """
        Create a range instrument from raw file data.
        """
        firstPitch, lastPitch = \
            struct.unpack_from('<BB', data, startOffset)

        noteDefinitions = []
        off = startOffset + 2
        for i in range(lastPitch - firstPitch + 1):
            noteData = data[off : off+0xC]
            noteDefinitions.append(
                NoteDefinition.fromDataWithType(noteData))
            off += 0xC

        return (cls(firstPitch, noteDefinitions),
                off - startOffset)


    def save(self):
        """
        Generate file data representing this instrument, and then return
        the instrument's type value and that data as a pair.
        """
        data = bytearray(2 + 0xC * len(self.noteDefinitions))
        struct.pack_into('<BB', data, 0,
            self.firstPitch, self.firstPitch + len(self.noteDefinitions) - 1)

        off = 2
        for n in self.noteDefinitions:
            data[off : off+0xC] = n.saveWithType()
            off += 0xC

        return super().save() + (data,)


    def __str__(self):
        joinList = []
        for i, d in enumerate(self.noteDefinitions):
            joinList.append(
                f'{_common.noteName(i + self.firstPitch)}: {d}')
        defs = ', '.join(joinList)
        firstNote = _common.noteName(self.firstPitch)
        return f'<range instrument starting at {firstNote} {{{defs}}}>'


    def __repr__(self):
        defs = ', '.join(repr(d) for d in self.noteDefinitions)
        return (f'{type(self).__name__}('
                f'{self.firstPitch!r}, '
                f'[{defs}])')


class RegionalInstrument(Instrument):
    """
    An instrument that partitions the range [0, 127] into sections, and
    contains one note definition for each.
    """

    class Region:
        """
        A region within a regional instrument.
        """
        def __init__(self, lastPitch, noteDefinition):
            self.lastPitch = lastPitch
            self.noteDefinition = noteDefinition


        def __str__(self):
            return (f'<region through {_common.noteName(self.lastPitch)} '
                    f'{self.noteDefinition}>')


        def __repr__(self):
            return (f'{type(self).__name__}('
                    f'{self.lastPitch!r}, '
                    f'{self.noteDefinition!r})')


    def __init__(self, regions):
        super().__init__(REGIONAL_INSTRUMENT_TYPE)
        self.regions = regions


    @classmethod
    def fromData(cls, _, data, startOffset):
        """
        Create a regional instrument from raw file data.
        """
        regionEnds = struct.unpack_from('8B', data, startOffset)

        regions = []
        off = startOffset + 8
        for e in regionEnds:
            if e == 0 and off != startOffset + 8: break

            noteData = data[off : off+0xC]
            note = NoteDefinition.fromDataWithType(noteData)
            off += 0xC

            regions.append(cls.Region(e, note))

        return cls(regions), off - startOffset


    def save(self):
        """
        Generate file data representing this instrument, and then return
        the instrument's type value and that data as a pair.
        """
        if len(self.regions) > 8:
            raise ValueError("Can't save RegionalInstrument -- too many "
                             f'regions ({len(self.regions)})!')

        data = bytearray(8 + 0xC * len(self.regions))
        for i, region in enumerate(self.regions):
            data[i] = region.lastPitch
            data[8 + 0xC * i : 0x14 + 0xC * i] = \
                region.noteDefinition.saveWithType()

        return super().save() + (data,)


    def __str__(self):
        fill = []
        last = 0
        for region in self.regions:
            def betterNoteName(num):
                if num == 0: return 'min'
                elif num == 127: return 'max'
                else: return _common.noteName(num)
            fill.append(f'{betterNoteName(last)}'
                        f'-{betterNoteName(region.lastPitch)}: '
                        f'{region.noteDefinition}')
            last = region.lastPitch + 1
        return f'<regional instrument {{{", ".join(fill)}}}>'


    def __repr__(self):
        return (f'{type(self).__name__}('
                f'[{", ".join(repr(r) for r in self.regions)}])')


def instrumentClass(type):
    """
    A convenience function that returns the Instrument subclass that
    should be used to load an instrument with the given type value.
    """
    if type == NO_INSTRUMENT_TYPE: # 0
        return None
    elif type < RANGE_INSTRUMENT_TYPE: # < 16
        return SingleNoteInstrument
    elif type == RANGE_INSTRUMENT_TYPE: # 16
        return RangeInstrument
    elif type == REGIONAL_INSTRUMENT_TYPE: # 17
        return RegionalInstrument
    else:
        raise ValueError(f'Instrument type {type} is invalid.')


def guessInstrumentType(data, startOffset, possibleTypes, bytesAvailable):
    """
    Try to guess the type of instrument stored in some binary data based
    on both the data and a set of possible types (ones that haven't been
    ruled out by the instrument's position in the surrounding data).
    This function is entirely based on heuristics, so it may return
    different answers for similar data, and it cannot always be
    accurate. Types 1, 2 and 3 are considered equivalent by this
    function, since they are very similar and all use the same Python
    class (SingleNoteInstrument). None will be returned if it's very
    unlikely that there is an instrument at that position.
    """
    possibleTypes = set(possibleTypes)

    # Types 2 and 3 (the PSG single-note instruments) should be
    # considered equivalent to type 1 (PCM single-note instrument)
    if SINGLE_NOTE_PSG_SQUARE_WAVE_INSTRUMENT_TYPE in possibleTypes:
        possibleTypes.remove(SINGLE_NOTE_PSG_SQUARE_WAVE_INSTRUMENT_TYPE)
        possibleTypes.add(SINGLE_NOTE_PCM_INSTRUMENT_TYPE)
    if SINGLE_NOTE_PSG_WHITE_NOISE_INSTRUMENT_TYPE in possibleTypes:
        possibleTypes.remove(SINGLE_NOTE_PSG_WHITE_NOISE_INSTRUMENT_TYPE)
        possibleTypes.add(SINGLE_NOTE_PCM_INSTRUMENT_TYPE)

    # By doing
    # if returnEarly(): return early()
    # you can quickly check if len(possibleTypes) < 2, and return the
    # appropriate type or None.
    def returnEarly():
        return len(possibleTypes) < 2
    def early():
        if possibleTypes:
            return list(possibleTypes)[0]
        else:
            return None


    # Return immediately if possible
    if returnEarly(): return early()


    # Start by ruling out the impossible...
    def ruleOut(type):
        if type in possibleTypes:
            possibleTypes.remove(type)
    if bytesAvailable < 10:
        ruleOut(NO_INSTRUMENT_TYPE)
    if bytesAvailable < 2 + 0xC:
        ruleOut(RANGE_INSTRUMENT_TYPE)
    if bytesAvailable < 8 + 0xC:
        ruleOut(REGIONAL_INSTRUMENT_TYPE)

    if returnEarly(): return early()


    # Then rule out the improbable...

    if SINGLE_NOTE_PCM_INSTRUMENT_TYPE in possibleTypes:
        # Among the games I've looked at, SWAV ID and SWAR ID are never
        # each more than 0xA00, so we can use that as a reasonable limit
        if data[startOffset + 1] >= 10: ruleOut(SINGLE_NOTE_PCM_INSTRUMENT_TYPE)
        if data[startOffset + 3] >= 10: ruleOut(SINGLE_NOTE_PCM_INSTRUMENT_TYPE)
        # And pitch will probably never be 0, right?
        if data[startOffset + 4] == 0: ruleOut(SINGLE_NOTE_PCM_INSTRUMENT_TYPE)
        # For that matter, if pitch is 0x3C (middle C), we can probably
        # just assume straight away that this is a single-note inst
        if data[startOffset + 4] == 0x3C:
            return SINGLE_NOTE_PCM_INSTRUMENT_TYPE
    if returnEarly(): return early()

    if RANGE_INSTRUMENT_TYPE in possibleTypes:
        firstPitch, lastPitch = data[startOffset : startOffset+2]
        if firstPitch > lastPitch:
            ruleOut(RANGE_INSTRUMENT_TYPE)
        else:
            expectedLen = 2 + 0xC * (lastPitch - firstPitch + 1)
            if expectedLen > bytesAvailable:
                ruleOut(RANGE_INSTRUMENT_TYPE)
    if returnEarly(): return early()

    if REGIONAL_INSTRUMENT_TYPE in possibleTypes:
        regionEnds = data[startOffset : startOffset+8]

        # Check that all ends are strictly increasing, followed by
        # all zeroes
        # (not every regional instrument ends with 7F, surprisingly)
        previous = -1
        for end in regionEnds:
            if previous != 0 and end == 0:
                # first zero byte
                previous = 0
            elif previous == 0 and end != 0:
                # nonzero byte after a zero byte? bad bad bad
                ruleOut(REGIONAL_INSTRUMENT_TYPE)
                break
            elif previous != 0:
                if end <= previous:
                    ruleOut(REGIONAL_INSTRUMENT_TYPE)
                    break
                previous = end
        else:
            # Finally, check that we have sufficient length
            regionCount = 0
            for e in regionEnds:
                if not e: break
                regionCount += 1
            expectedLen = 8 + 0xC * regionCount
            if expectedLen > bytesAvailable:
                ruleOut(REGIONAL_INSTRUMENT_TYPE)
    if returnEarly(): return early()


    # At this point, just pick one of the remaining options at random.
    return early()


class SBNK:
    """
    A SBNK instrument bank file. This defines a set of instruments
    that sequences and sequence archives can use.
    """
    # When saving SDAT, two otherwise identical SBNKs will share data
    # only if their dataMergeOptimizationIDs are the same.
    # You can pretty safely ignore this.
    dataMergeOptimizationID = 0

    def __init__(self, file=None, unk02=0, waveArchiveIDs=None):
        self.unk02 = unk02

        if waveArchiveIDs is None:
            self.waveArchiveIDs = []
        else:
            self.waveArchiveIDs = list(waveArchiveIDs)

            # Remove trailing `None`s if they exist
            while self.waveArchiveIDs and self.waveArchiveIDs[-1] is None:
                self.waveArchiveIDs = self.waveArchiveIDs[:-1]

        self.instruments = []
        self.inaccessibleInstruments = {}

        if file is not None:
            if not file.startswith(b'SBNK'):
                raise ValueError("Wrong magic (should be b'SBNK', instead "
                                 f'found {file[:4]})')

            self._initFromData(file)


    @classmethod
    def fromInstruments(cls, instruments, unk02=0, waveArchiveIDs=None):
        """
        Create a SBNK from a list of instruments.
        """
        obj = cls(unk02=unk02, waveArchiveIDs=waveArchiveIDs)
        obj.instruments = instruments
        return obj


    @classmethod
    def fromFile(cls, filePath, *args, **kwargs):
        """
        Load an SBNK from a filesystem file.
        """
        with open(filePath, 'rb') as f:
            return cls(f.read(), *args, **kwargs)
    

    def _initFromData(self, data):
        """
        Initialize the SBNK from file data.
        """

        magic, bom, version, filesize, headersize, numblocks = \
            _common.NDS_STD_FILE_HEADER.unpack_from(data, 0)
        assert magic == b'SBNK', f'Incorrect SBNK magic ({magic})'
        if version != 0x100:
            raise ValueError(f'Unsupported SBNK version: {version}')

        dataMagic, dataSize, instrumentCount = \
            struct.unpack_from('<4sI32xI', data, 0x10)
        assert dataMagic == b'DATA', f'Incorrect SBNK DATA magic ({dataMagic})'

        unconsumedBytes = set(range(0x3C + instrumentCount * 4, filesize))

        idsToOffsets = {}

        def makeInstrumentAt(type, offset):
            instrumentCls = instrumentClass(type)
            if instrumentCls is None:
                instrument = None
                consumedBytesHere = 0
            else:
                instrument, consumedBytesHere = instrumentCls.fromData(type,
                                                                       data,
                                                                       offset)
                instrument.bankOrderKey = offset
                instrument.dataMergeOptimizationID = offset

            for j in range(consumedBytesHere):
                if offset + j in unconsumedBytes:
                    unconsumedBytes.remove(offset + j)

            return instrument

        dataArrayPos = 0x3C
        for id in range(instrumentCount):
            (instrumentType, instrumentOffset) = \
                struct.unpack_from('<BHx', data, dataArrayPos)
            dataArrayPos += 4

            instrument = makeInstrumentAt(instrumentType, instrumentOffset)
            self.instruments.append(instrument)

            if instrument is not None:
                idsToOffsets[id] = instrumentOffset

        # Why do we have to do this D:
        while unconsumedBytes:

            # Account for possible 2 bytes of padding at the end
            if (filesize - 1 in unconsumedBytes
                and filesize - 2 in unconsumedBytes
                and filesize - 3 not in unconsumedBytes):
                unconsumedBytes.remove(filesize - 1)
                unconsumedBytes.remove(filesize - 2)
            if not unconsumedBytes: break

            thisOffset = min(unconsumedBytes)

            # Find the previous and following instrument IDs
            prevID = -1
            prevOffset = -1
            nextID = 9E9
            nextOffset = 9E9
            for id, offset in idsToOffsets.items():
                if offset < thisOffset and offset > prevOffset:
                    prevID = id
                    prevOffset = offset
                if offset > thisOffset and offset < nextOffset:
                    nextID = id
                    nextOffset = offset
            if prevID == -1: prevID = None
            if nextID == 9E9: nextID = None

            # Find possible types for this instrument based on that
            possibleTypes = {SINGLE_NOTE_PCM_INSTRUMENT_TYPE,
                             RANGE_INSTRUMENT_TYPE,
                             REGIONAL_INSTRUMENT_TYPE}
            prevInst = None if prevID is None else self.instruments[prevID]
            nextInst = None if nextID is None else self.instruments[nextID]
            if prevInst is not None:
                if prevInst.type >= RANGE_INSTRUMENT_TYPE:
                    possibleTypes.remove(1)
                if prevInst.type == REGIONAL_INSTRUMENT_TYPE:
                    possibleTypes.remove(RANGE_INSTRUMENT_TYPE)
            if nextInst is not None:
                if (nextInst.type <= RANGE_INSTRUMENT_TYPE
                        and REGIONAL_INSTRUMENT_TYPE in possibleTypes):
                    possibleTypes.remove(REGIONAL_INSTRUMENT_TYPE)
                if (nextInst.type < RANGE_INSTRUMENT_TYPE
                        and RANGE_INSTRUMENT_TYPE in possibleTypes):
                    possibleTypes.remove(RANGE_INSTRUMENT_TYPE)

            # Count the number of contiguous bytes we've got
            tempOffset = thisOffset + 1
            while tempOffset in unconsumedBytes:
                tempOffset += 1
            bytesAvailable = tempOffset - thisOffset

            # Use advanced heuristics™ to determine this instrument's
            # type
            instrumentType = guessInstrumentType(data,
                                                 thisOffset,
                                                 possibleTypes,
                                                 bytesAvailable)

            if instrumentType is None:
                instrument = None
            else:
                try:
                    instrument = makeInstrumentAt(instrumentType, thisOffset)
                except Exception:
                    instrument = None

            if instrument is None:
                # Couldn't make an instrument there, so, assume that
                # it's garbage data that we have to skip (to avoid an
                # infinite loop)
                unconsumedBytes.remove(thisOffset)
                if thisOffset + 1 in unconsumedBytes:
                    unconsumedBytes.remove(thisOffset + 1)

            else:
                if prevID not in self.inaccessibleInstruments:
                    self.inaccessibleInstruments[prevID] = []
                self.inaccessibleInstruments[prevID].append(instrument)


    def save(self):
        """
        Generate file data representing this SBNK, and then return that
        data, .unk02, and .waveArchiveIDs as a triple.
        """
        data = bytearray(0x3C + 4 * len(self.instruments))
        instrumentsData = bytearray()

        # Instrument data (that the offset points to) is stored in order of:
        # - Single-note instruments
        # - Range instruments
        # - Regional instruments
        # Yet the instruments offsets table is in the order that forms
        # the instruments IDs exposed to other files. So we save in two
        # steps.
        # Also, the order within each of those three categories can be
        # arbitrary. So instruments have a bankOrderKey that can be used
        # to sort within each category.

        # First, put together the instruments data itself
        indexToOffset = [None for _ in self.instruments]
        dataReuseCache = {}
        def addInstrument(instrument):
            instrumentType, instrumentData = instrument.save()
            instrumentData = bytes(instrumentData)
            mergeID = instrument.dataMergeOptimizationID

            if (instrumentData, mergeID) not in dataReuseCache:
                dataReuseCache[(instrumentData, mergeID)] = \
                    len(instrumentsData)
                instrumentsData.extend(instrumentData)

            return dataReuseCache[(instrumentData, mergeID)]

        test1 = lambda id: id < RANGE_INSTRUMENT_TYPE
        test2 = lambda id: id == RANGE_INSTRUMENT_TYPE
        test3 = lambda id: id == REGIONAL_INSTRUMENT_TYPE
        if None in self.inaccessibleInstruments:
            for inacc in self.inaccessibleInstruments[None]:
                addInstrument(inacc)
        for test in (test1, test2, test3):
            inThisGroup = []
            for i, instrument in enumerate(self.instruments):
                if instrument is None: continue
                if test(instrument.type):
                    inThisGroup.append((i, instrument))

            inThisGroup.sort(key=lambda elem: elem[1].bankOrderKey)

            for i, instrument in inThisGroup:
                indexToOffset[i] = addInstrument(instrument)

                if i in self.inaccessibleInstruments:
                    for inacc in self.inaccessibleInstruments[i]:
                        addInstrument(inacc)

        # Add any inaccessible instruments with IDs that are too high
        idSet = set(self.inaccessibleInstruments)
        if None in idSet: idSet.remove(None)
        for inaccID in sorted(idSet):
            if inaccID < len(self.instruments): continue
            for inacc in self.inaccessibleInstruments[inaccID]:
                addInstrument(inacc)

        # And now construct the table using that.
        for i, instrument in enumerate(self.instruments):
            instrumentType = instrument.type if instrument is not None else 0

            offs = indexToOffset[i]
            if offs is None: offs = 0
            else: offs += len(data)

            struct.pack_into('<BH', data, 0x3C + 4 * i,
                             instrumentType, offs)

        data.extend(instrumentsData)

        while len(data) % 4:
            data.append(0)

        _common.NDS_STD_FILE_HEADER.pack_into(data, 0,
            b'SBNK', 0xFEFF, 0x100, len(data), 0x10, 1)
        struct.pack_into('<4sI32xI', data, 0x10,
            b'DATA', len(data) - 0x10, len(self.instruments))

        return (data, self.unk02, self.waveArchiveIDs)


    def saveToFile(self, filePath):
        """
        Generate file data representing this SBNK, and save it to a
        filesystem file.
        """
        d = self.save()[0]
        with open(filePath, 'wb') as f:
            f.write(d)


    def __str__(self):
        linesList = [f'<sbnk waveArchiveIDs={self.waveArchiveIDs}']
        linesList.extend(_common.enumeratedListOfStrs(self.instruments))
        linesList.append('>')
        return '\n'.join(linesList)


    def __repr__(self):
        return (f'{type(self).__name__}.fromInstruments('
                f'{self.instruments!r}, '
                f'waveArchiveIDs={self.waveArchiveIDs!r})')
