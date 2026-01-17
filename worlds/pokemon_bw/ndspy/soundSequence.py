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
Support for SSEQs and their sequence events.
"""

import enum
import struct

from . import _common


class SSEQ:
    """
    A SSEQ sound sequence file.
    """
    # When saving SDAT, two otherwise identical SSEQs will share data
    # only if their dataMergeOptimizationIDs are the same.
    # You can pretty safely ignore this.
    dataMergeOptimizationID = 0

    def __init__(self, file=None, unk02=0, bankID=0, volume=127,
                 channelPressure=64, polyphonicPressure=50, playerID=0):
        #        ^
        # Default values here are the most common ones in the NSMB SDAT.

        self.unk02 = unk02
        self.bankID = bankID
        self.volume = volume
        self.channelPressure = channelPressure
        self.polyphonicPressure = polyphonicPressure
        self.playerID = playerID

        if file is not None:
            if not file.startswith(b'SSEQ'):
                raise ValueError("Wrong magic (should be b'SSEQ', instead "
                                 f'found {file[:4]})')

            version, totalFileLen = struct.unpack_from('<HI', file, 6)
            if version != 0x100:
                raise ValueError(f'Unsupported SSEQ version: {version}')

            self._events = []
            dataOffs, = struct.unpack_from('<I', file, 0x18)
            self._eventsData = file[dataOffs:totalFileLen]
            self._parsed = False

        else:

            self._events = []
            self._parsed = True


    @classmethod
    def fromEvents(cls, events, unk02=0, bankID=0, volume=127,
                   channelPressure=64, polyphonicPressure=50, playerID=0):
        """
        Create a new SSEQ object from a list of sequence events.
        """
        obj = cls(None, unk02, bankID, volume, channelPressure,
            polyphonicPressure, playerID)
        obj.events = events
        return obj


    @classmethod
    def fromFile(cls, filePath, *args, **kwargs):
        """
        Load an SSEQ from a filesystem file.
        """
        with open(filePath, 'rb') as f:
            return cls(f.read(), *args, **kwargs)


    @property
    def events(self):
        if not self.parsed:
            raise ValueError('You must parse the SSEQ with .parse() before you'
                             ' can access .events!')
        return self._events
    @events.setter
    def events(self, value):
        self._events = value


    @property
    def eventsData(self):
        if self.parsed:
            raise ValueError('You cannot use .eventsData after you have parsed'
                             ' the SSEQ!')
        return self._eventsData
    @eventsData.setter
    def eventsData(self, value):
        self._eventsData = value


    @property
    def parsed(self):
        return self._parsed
    @parsed.setter
    def parsed(self, value):
        raise RuntimeError('SSEQ.parsed is read-only!')


    def parse(self):
        """
        Attempt to process .eventsData to create .events. If successful,
        this switches the SSEQ from the unparsed to the parsed state.
        """
        if self.parsed: return
        self._events, _ = readSequenceEvents(self._eventsData, [])
        self._parsed = True


    def save(self):
        """
        Generate file data representing this SSEQ, and then return
        that data, .unk02, .bankID, .volume, .channelPressure,
        .polyphonicPressure, and .playerID as a 7-tuple. This matches
        the parameters of the default class constructor.
        """
        if self.parsed:
            seqEv, _ = saveSequenceEvents(self.events, [])
        else:
            seqEv = self._eventsData

        file = bytearray(0x1C + len(seqEv))

        _common.NDS_STD_FILE_HEADER.pack_into(file, 0,
            b'SSEQ', 0xFEFF, 0x100, len(file), 0x10, 1)
        struct.pack_into('<4sII', file, 0x10,
            b'DATA', len(file) - 0x10, 0x1C)
        file[0x1C:] = seqEv

        return (file,
                self.unk02,
                self.bankID,
                self.volume,
                self.channelPressure,
                self.polyphonicPressure,
                self.playerID)


    def saveToFile(self, filePath):
        """
        Generate file data representing this SSEQ, and save it to a
        filesystem file.
        """
        d = self.save()[0]
        with open(filePath, 'wb') as f:
            f.write(d)


    def __str__(self):
        fields = (f'bankID={self.bankID} volume={self.volume}'
                  f' channelPressure={self.channelPressure}'
                  f' polyphonicPressure={self.polyphonicPressure}'
                  f' playerID={self.playerID}')
        if not self.parsed:
            return f'<sseq unparsed {fields}>'

        linesList = [f'<sseq {fields}']
        linesList.append(printSequenceEventList(self.events, {}, ' ' * 2))
        linesList.append('>')
        return '\n'.join(linesList)


    def __repr__(self):

        if self.parsed:
            if len(self.events) > 8:
                ev = repr(self.events[:8])[:-1] + ', ...]'
            else:
                ev = repr(self.events)

            return (f'{type(self).__name__}.fromEvents({ev}'
                    f', {self.unk02!r}, {self.bankID!r}'
                    f', {self.volume!r}, {self.channelPressure!r}'
                    f', {self.polyphonicPressure!r}'
                    f', {self.playerID!r})')

        else:
            data = _common.shortBytesRepr(self.eventsData)
            return f'{type(self).__name__}({data})'


class SequenceEvent:
    """
    An abstract base class representing any sequence event in a SSEQ or
    SSAR file.
    """
    dataLength = 1


    def __init__(self, type):
        self.type = type


    def save(self, eventsToOffsets=None):
        """
        Generate data representing this sequence event. This abstract
        base class implementation simply returns a single byte
        containing .type. Subclasses should reimplement this function to
        append their own data to this byte.
        """
        return self.type.to_bytes(1, 'little')


    @classmethod
    def fromData(cls, type, data, startOffset=0):
        """
        Create an instance of the SequenceEvent subclass this function
        is called on, using a particular type value and reading data
        beginning at some offset. This abstract base class
        implementation simply raises NotImplementedError.
        """
        raise NotImplementedError('SequenceEvent subclasses that can '
            'load themselves from data without context can implement this.')


    def __str__(self):
        return f'<sequence event {hex(self.type)}>'

    def __repr__(self):
        return f'{type(self).__name__}({hex(self.type)})'


def _readVariableLengthInt(data, startOffset, limit=4):
    """
    Read a variable-length integer (as SSEQ encodes them) from `data`
    beginning at `startOffset`, limiting the number of read bytes to
    `limit`.
    
    While the code below looks complicated, the method to read such an
    integer is simple:
    - Read a byte. AND it with 0x7F for the part relevant to the
      integer value.
    - If its MSB (that you just trimmed off) is set, left-shift the int
      value by 7, move on to the next byte and repeat.

    So you read 7 bits as a time for as long as the MSB continues to be
    set.
    """
    offset = startOffset
    value = data[offset] & 0x7F; offset += 1
    length = 0
    while data[offset - 1] & 0x80:
        value <<= 7
        value |= data[offset] & 0x7F; offset += 1; length += 1
        if length > limit:
            raise ValueError('Read variable-length int past its end')
    return value


def _lengthOfVariableLengthInt(x):
    """
    Returns the length of a variable-length integer `x`, as encoded in
    SSEQ. See _readVariableLengthInt() for a description of the format.
    This can be implemented more concisely, but I opted for readability.
    """
    if x < 0:
        raise ValueError(f'Cannot write a negative variable-length int: {x}')
    bits = x.bit_length()
    length = 0
    while bits > 0:
        length += 1
        bits -= 7
    return max(1, length)


def _writeVariableLengthInt(x):
    """
    Find the bytes representing the arbitrarily-large (positive) integer
    `x` in the format used by SSEQ variable-length integer fields.
    See _readVariableLengthInt() for a description of this format.
    """
    if x < 0:
        raise ValueError(f'Cannot write a negative variable-length int: {x}')

    ret = []

    while True:
        value, x = x & 0x7F, x >> 7
        ret.append(value)
        if x == 0:
            break

    ret.reverse()

    for i, v in enumerate(ret[:-1]):
        ret[i] = v | 0x80

    return bytes(ret)


class NoteSequenceEvent(SequenceEvent):
    """
    A sequence event that plays a note. This class represents sequence
    event types 0x00 through 0x7F; the type value actually determines
    the pitch.
    """

    def __init__(self, type, velocityAndFlag, duration):
        super().__init__(type)
        self.velocity = velocityAndFlag & 0x7F
        self.unknownFlag = bool(velocityAndFlag & 0x80)
        self.duration = duration

    @property
    def name(self):
        return _common.noteName(self.type)

    @property
    def dataLength(self):
        return 2 + _lengthOfVariableLengthInt(self.duration)

    @property
    def pitch(self):
        return self.type
    @pitch.setter
    def pitch(self, value):
        self.type = value

    def save(self, eventsToOffsets=None):
        if self.type < 0:
            raise ValueError(f'Note pitch must be >= 0 (found:'
                             f' {self.type})')
        if self.type > 127:
            raise ValueError(f'Note pitch must be < 128 (found:'
                             f' {self.type})')
        if self.velocity > 127:
            raise ValueError(f'Note velocity must be < 128 (found:'
                             f' {self.velocity})')
        velocityValue = self.velocity | (0x80 if self.unknownFlag else 0)
        return (super().save()
                + velocityValue.to_bytes(1, 'little')
                + _writeVariableLengthInt(self.duration))

    @classmethod
    def fromData(cls, type, data, startOffset=0):
        velocity = data[startOffset + 1]
        duration = _readVariableLengthInt(data, startOffset + 2)
        return cls(type, velocity, duration)

    def __str__(self):
        flag = ' unknown-flag' if self.unknownFlag else ''
        return f'<{self.name} velocity={self.velocity} duration={self.duration}{flag}>'

    def __repr__(self):
        velocityValue = self.velocity | (0x80 if self.unknownFlag else 0)
        return f'{type(self).__name__}({self.type}, {velocityValue!r}, {self.duration!r})'


class RestSequenceEvent(SequenceEvent):
    """
    A sequence event that causes SSEQ execution to pause for some amount
    of time before moving on. This is sequence event type 0x80.
    """

    def __init__(self, duration):
        super().__init__(0x80)
        self.duration = duration

    @property
    def dataLength(self):
        return 1 + _lengthOfVariableLengthInt(self.duration)

    def save(self, eventsToOffsets=None):
        return super().save() + _writeVariableLengthInt(self.duration)

    @classmethod
    def fromData(cls, type, data, startOffset=0):
        duration = _readVariableLengthInt(data, startOffset + 1)
        return cls(duration)

    def __str__(self):
        return f'<rest {self.duration}>'

    def __repr__(self):
        return f'{type(self).__name__}({self.duration!r})'


class InstrumentSwitchSequenceEvent(SequenceEvent):
    """
    A sequence event that causes the track it's placed in to switch to
    using a different instrument (possibly in a different SBNK). This is
    sequence event type 0x81.
    """

    def __init__(self, bankID, instrumentID):
        super().__init__(0x81)
        self.bankID = bankID
        self.instrumentID = instrumentID

    @property
    def dataLength(self):
        return 1 + _lengthOfVariableLengthInt(
            self.bankID << 7 | self.instrumentID)

    def save(self, eventsToOffsets=None):
        value = self.instrumentID & 0x7F | self.bankID << 7
        return super().save() + _writeVariableLengthInt(value)

    @classmethod
    def fromData(cls, type, data, startOffset=0):
        value = _readVariableLengthInt(data, startOffset + 1)
        instrumentID = value & 0x7F
        bankID = value >> 7
        return cls(bankID, instrumentID)

    def __str__(self):
        return f'<instrument {self.bankID}/{self.instrumentID}>'

    def __repr__(self):
        return f'{type(self).__name__}({self.bankID!r}, {self.instrumentID!r})'


class BeginTrackSequenceEvent(SequenceEvent):
    """
    A sequence event that declares the location in the sequence event
    data at which a particular track should begin executing. This is
    sequence event type 0x93.
    """
    dataLength = 5

    def __init__(self, trackNumber, firstEvent):
        super().__init__(0x93)
        self.trackNumber = trackNumber
        self.firstEvent = firstEvent

    def save(self, eventsToOffsets=None):
        return (super().save()
                + self.trackNumber.to_bytes(1, 'little')
                + eventsToOffsets[self.firstEvent].to_bytes(3, 'little'))

    def __str__(self):
        return f'<begin track {self.trackNumber} id={id(self.firstEvent)}>'

    def __repr__(self):
        return f'{type(self).__name__}({self.trackNumber!r}, {self.firstEvent!r} at {id(self.firstEvent)})'


class JumpSequenceEvent(SequenceEvent):
    """
    A sequence event that causes execution of the current track to jump
    to some other location. This is sequence event type 0x94.
    """
    dataLength = 4

    def __init__(self, destination):
        super().__init__(0x94)
        self.destination = destination

    def save(self, eventsToOffsets=None):
        return (super().save()
                + eventsToOffsets[self.destination].to_bytes(3, 'little'))

    def __str__(self):
        return f'<jump id={id(self.destination)}>'

    def __repr__(self):
        return f'{type(self).__name__}({self.destination!r} at {id(self.destination)})'


class CallSequenceEvent(SequenceEvent):
    """
    A sequence event that causes execution of the current track to jump
    to some other location, and pushes the current event's address to a
    return-address stack. This is sequence event type 0x95.
    """
    dataLength = 4

    def __init__(self, destination):
        super().__init__(0x95)
        self.destination = destination

    def save(self, eventsToOffsets=None):
        return (super().save()
                + eventsToOffsets[self.destination].to_bytes(3, 'little'))

    def __str__(self):
        return f'<call id={id(self.destination)}>'

    def __repr__(self):
        return f'{type(self).__name__}({self.destination!r} at {id(self.destination)})'


class RandomSequenceEvent(SequenceEvent):
    """
    A sequence event that causes some other event to execute with a
    randomized argument. This is sequence event type 0xA0.
    """

    def __init__(self, subType, args, randMin, randMax):
        super().__init__(0xA0)
        self.subType = subType
        self.args = args
        self.randMin = randMin
        self.randMax = randMax

    @property
    def dataLength(self):
        return self._dataLength_for_subtype(self.subType)

    @staticmethod
    def _dataLength_for_subtype(subType):
        if subType <= 0x7F:
            return 7

        # This is really really hacky, but... works
        for i in range(5):
            try:
                subEvent = _EVENT_TYPES[subType](0, *([0] * i))
                return 4 + subEvent.dataLength
            except TypeError as e:
                pass
        raise ValueError("Couldn't determine dataLength for"
            ' RandomSequenceEvent for some reason...?'
            f' subType={hex(subType)}')

    def save(self, eventsToOffsets=None):
        return (super().save()
                + bytes([self.subType, *self.args])
                + struct.pack('<hh', self.randMin, self.randMax))

    @classmethod
    def fromData(cls, type, data, startOffset=0):
        subType = data[startOffset + 1]
        length = cls._dataLength_for_subtype(subType)

        args = []
        offset = startOffset + 2
        for i in range(length - 6):
            args.append(data[offset])
            offset += 1

        randMin, randMax = struct.unpack_from('<hh', data, offset)

        return cls(subType, args, randMin, randMax)

    def __str__(self):
        return (f'<random {hex(self.subType)}'
                f' {" ".join([str(x) for x in self.args])}'
                f'{" " if self.args else ""}'
                f'{(self.randMin, self.randMax)}>')

    def __repr__(self):
        return f'{type(self).__name__}({hex(self.subType)}, {self.args!r}, {self.randMin!r}, {self.randMax!r})'


class FromVariableSequenceEvent(SequenceEvent):
    """
    A sequence event that executes some other event with its last
    argument taken from a variable. This is sequence event type 0xA1.
    """

    def __init__(self, subType, variableID, unknown=None):
        super().__init__(0xA1)
        self.subType = subType
        self.variableID = variableID
        self.unknown = unknown

    @property
    def dataLength(self):
        # Original comment on this logic from sseq2mid.c:
        # /* loveemu is a lazy person :P */

        # (loveemu is the author of sseq2mid.)
        # Interpret as you will.

        return 4 if (0xB0 <= self.subType <= 0xBD) else 3

    def save(self, eventsToOffsets=None):
        if self.dataLength == 3:
            return super().save() + struct.pack('<Bh',
                                                self.subType,
                                                self.variableID)
        else:
            if self.unknown is None:
                raise ValueError('FromVariableSequenceEvent: trying to'
                    ' save with unknown, but unknown is None!')
            return super().save() + struct.pack('<Bbbxx',
                                                self.subType,
                                                self.unknown,
                                                self.variableID)

    @classmethod
    def fromData(cls, type, data, startOffset=0):
        subType = data[startOffset + 1]
        if 0xB0 <= subType <= 0xBD:
            unknown, variableID = struct.unpack_from('<bb',
                                                     data,
                                                     startOffset + 2)
        else:
            unknown = None
            variableID, = struct.unpack_from('<h', data, startOffset + 2)
        return cls(subType, variableID, unknown)

    def __str__(self):
        unk = f' {self.unknown}' if self.unknown is not None else ''
        return f'<from variable {hex(self.subType)} {self.variableID}{unk}>'

    def __repr__(self):
        unk = f', {self.unknown}' if self.unknown is not None else ''
        return f'{type(self).__name__}({hex(self.subType)}, {self.variableID!r}{unk})'


class IfSequenceEvent(SequenceEvent):
    """
    A sequence event that causes the next event to be skipped if the
    conditional flag is currently false. This is sequence event type
    0xA2.
    """
    def __init__(self):
        super().__init__(0xA2)
    @classmethod
    def fromData(cls, type, data, startOffset=0):
        return cls()
    def __str__(self):
        return '<if>'
    def __repr__(self):
        return f'{type(self).__name__}()'


def _make_arithmetic_sequence_event_class(typeNum, symbol, name, description):
    """
    Helper function to make a SequenceEvent subclass for the arithmetic
    operations.
    """
    __doc__ = f'A sequence event that {description}. This is sequence event type 0x{typeNum:02X}.'

    def __init__(self, variableID, value):
        SequenceEvent.__init__(self, typeNum)
        self.variableID = variableID
        self.value = value

    def save(self, eventsToOffsets=None):
        return (SequenceEvent.save(self)
                + struct.pack('<Bh', self.variableID, self.value))

    @classmethod
    def fromData(cls, type, data, startOffset=0):
        variableID, value = struct.unpack_from('<Bh', data, startOffset + 1)
        return cls(variableID, value)

    def __str__(self):
        return f'<(var {self.variableID}) {symbol.lower()} {self.value}>'

    def __repr__(self):
        return f'{type(self).__name__}({self.variableID!r}, {self.value!r})'

    return type(name,
                (SequenceEvent,),
                {'__doc__': __doc__,
                 '__init__': __init__,
                 'save': save,
                 'fromData': fromData,
                 '__str__': __str__,
                 '__repr__': __repr__,
                 'dataLength': 4})


VariableAssignmentSequenceEvent = _make_arithmetic_sequence_event_class(0xB0,
    '=', 'VariableAssignmentSequenceEvent', 'sets a variable to a given value')

VariableAdditionSequenceEvent = _make_arithmetic_sequence_event_class(0xB1,
    '+=', 'VariableAdditionSequenceEvent', 'increments a variable by a given value')

VariableSubtractionSequenceEvent = _make_arithmetic_sequence_event_class(0xB2,
    '-=', 'VariableSubtractionSequenceEvent', 'decrements a variable by a given value')

VariableMultiplicationSequenceEvent = _make_arithmetic_sequence_event_class(0xB3,
    '*=', 'VariableMultiplicationSequenceEvent', 'multiplies a variable by a given value')

VariableDivisionSequenceEvent = _make_arithmetic_sequence_event_class(0xB4,
    '/=', 'VariableDivisionSequenceEvent', 'divides a variable by a given value')

VariableShiftSequenceEvent = _make_arithmetic_sequence_event_class(0xB5,
    '<<=', 'VariableShiftSequenceEvent',
    'left-shifts a variable by a given value')

VariableRandSequenceEvent = _make_arithmetic_sequence_event_class(0xB6,
    '[rand]', 'VariableRandSequenceEvent',
    'sets a variable to a random value')

# Deprecated
VariableUnknownB7SequenceEvent = _make_arithmetic_sequence_event_class(0xB7,
    '[nop]', 'VariableUnknownB7SequenceEvent', 'does nothing')

VariableEqualSequenceEvent = _make_arithmetic_sequence_event_class(0xB8,
    '==', 'VariableEqualSequenceEvent',
    'sets the conditional flag to true if the specified variable contains a given value,'
        ' or to false otherwise')

VariableGreaterThanOrEqualSequenceEvent = _make_arithmetic_sequence_event_class(0xB9,
    '>=', 'VariableGreaterThanOrEqualSequenceEvent',
    'sets the conditional flag to true if the specified variable contains a value greater'
        ' than or equal to a given value, or to false otherwise')

VariableGreaterThanSequenceEvent = _make_arithmetic_sequence_event_class(0xBA,
    '>', 'VariableGreaterThanSequenceEvent',
    'sets the conditional flag to true if the specified variable contains a value greater'
        ' than a given value, or to false otherwise')

VariableLessThanOrEqualSequenceEvent = _make_arithmetic_sequence_event_class(0xBB,
    '<=', 'VariableLessThanOrEqualSequenceEvent',
    'sets the conditional flag to true if the specified variable contains a value less'
        ' than or equal to a given value, or to false otherwise')

VariableLessThanSequenceEvent = _make_arithmetic_sequence_event_class(0xBC,
    '<', 'VariableLessThanSequenceEvent',
    'sets the conditional flag to true if the specified variable contains a value less'
        ' than a given value, or to false otherwise')

VariableNotEqualSequenceEvent = _make_arithmetic_sequence_event_class(0xBD,
    '!=', 'VariableNotEqualSequenceEvent',
    'sets the conditional flag to true if the specified variable does not contain'
        ' a given value, or to false otherwise')


def _make_simple_sequence_event_class(typeNum, shortName, name, description):
    """
    Helper function to make a simple SequenceEvent subclass with one
    parameter.
    """
    __doc__ = f'A sequence event {description}. This is sequence event type 0x{typeNum:02X}.'

    def __init__(self, value):
        SequenceEvent.__init__(self, typeNum)
        self.value = value

    def save(self, eventsToOffsets=None):
        return SequenceEvent.save(self) + self.value.to_bytes(1, 'little')

    @classmethod
    def fromData(cls, type, data, startOffset=0):
        return cls(data[startOffset + 1])

    def __str__(self):
        return f'<{shortName.lower()} {self.value}>'

    def __repr__(self):
        return f'{type(self).__name__}({self.value!r})'

    return type(name,
                (SequenceEvent,),
                {'__doc__': __doc__,
                 '__init__': __init__,
                 'save': save,
                 'fromData': fromData,
                 '__str__': __str__,
                 '__repr__': __repr__,
                 'dataLength': 2})


PanSequenceEvent = _make_simple_sequence_event_class(0xC0,
    'Pan', 'PanSequenceEvent',
    'that sets the stereo panning value for the current track')

TrackVolumeSequenceEvent = _make_simple_sequence_event_class(0xC1,
    'Track volume', 'TrackVolumeSequenceEvent',
    'that sets the volume of the current track')

GlobalVolumeSequenceEvent = _make_simple_sequence_event_class(0xC2,
    'Global volume', 'GlobalVolumeSequenceEvent',
    'that sets the global volume, for all tracks')

TransposeSequenceEvent = _make_simple_sequence_event_class(0xC3,
    'Transpose', 'TransposeSequenceEvent',
    'that causes NoteSequenceEvents following it in the current track to be transposed')

PortamentoSequenceEvent = _make_simple_sequence_event_class(0xC4,
    'Portamento', 'PortamentoSequenceEvent', 'related to portamentos')

PortamentoRangeSequenceEvent = _make_simple_sequence_event_class(0xC5,
    'Portamento range', 'PortamentoRangeSequenceEvent', 'related to portamentos')

TrackPrioritySequenceEvent = _make_simple_sequence_event_class(0xC6,
    'Track priority', 'TrackPrioritySequenceEvent',
    'that sets the priority of the current track')


class MonoPolySequenceEvent(SequenceEvent):
    """
    A sequence event that switches the current track to mono mode or
    poly mode. This is sequence event type 0xC7.
    """
    dataLength = 2

    class Value(enum.IntEnum):
        POLY = 0
        MONO = 1

    def __init__(self, value):
        super().__init__(0xC7)
        self.value = self.Value(value)

    def save(self, eventsToOffsets=None):
        return super().save() + self.value.to_bytes(1, 'little')

    @classmethod
    def fromData(cls, type, data, startOffset=0):
        return cls(data[startOffset + 1])

    def __str__(self):
        return '<mono>' if self.value else '<poly>'

    def __repr__(self):
        return f'{type(self).__name__}({self.value!r})'

# Change the internal name of the MonoPolySequenceEvent.Value enum to
# "MonoPolySequenceEvent.Value"
MonoPolySequenceEvent.Value.__name__ = \
    f'{MonoPolySequenceEvent.__name__}.{MonoPolySequenceEvent.Value.__name__}'


class TieSequenceEvent(SequenceEvent):
    """
    A sequence event that enables or disables "tie" mode on the current
    track. This is sequence event type 0xC8.
    """
    dataLength = 2

    def __init__(self, value):
        super().__init__(0xC8)
        if value in [0, 1]:
            value = bool(value)
        self.value = value

    def save(self, eventsToOffsets=None):
        return super().save() + self.value.to_bytes(1, 'little')

    @classmethod
    def fromData(cls, type, data, startOffset=0):
        return cls(data[startOffset + 1])

    def __str__(self):
        if self.value in [0, 1, False, True]:
            v = 'on' if self.value else 'off'
        else:
            v = self.value
        return f'<tie {v}>'

    def __repr__(self):
        return f'{type(self).__name__}({self.value!r})'


class PortamentoFromSequenceEvent(SequenceEvent):
    """
    A sequence event related to portamentos. This is sequence event type
    0xC9.
    """
    dataLength = 2

    def __init__(self, value):
        super().__init__(0xC9)
        self.value = value

    def save(self, eventsToOffsets=None):
        return super().save() + self.value.to_bytes(1, 'little')

    @classmethod
    def fromData(cls, type, data, startOffset=0):
        return cls(data[startOffset + 1])

    def __str__(self):
        return f'<portamento from {_common.noteName(self.value)}>'

    def __repr__(self):
        return f'{type(self).__name__}({self.value!r})'


VibratoDepthSequenceEvent = _make_simple_sequence_event_class(0xCA,
    'Vibrato depth', 'VibratoDepthSequenceEvent',
    'related to vibratos')

VibratoSpeedSequenceEvent = _make_simple_sequence_event_class(0xCB,
    'Vibrato speed', 'VibratoSpeedSequenceEvent',
    'related to vibratos')


class VibratoTypeSequenceEvent(SequenceEvent):
    """
    A sequence event that sets the current vibrato type. This is
    sequence event type 0xCC.
    """
    dataLength = 2

    class Value(enum.IntEnum):
        PITCH = 0
        VOLUME = 1
        PAN = 2

    def __init__(self, value):
        super().__init__(0xCC)
        self.value = self.Value(value)

    def save(self, eventsToOffsets=None):
        return super().save() + self.value.to_bytes(1, 'little')

    @classmethod
    def fromData(cls, type, data, startOffset=0):
        return cls(data[startOffset + 1])

    def _valueName(self):
        if self.value in [0, 1, 2]:
            return ['pitch', 'volume', 'pan'][self.value]
        else:
            return str(self.value)

    def __str__(self):
        return f'<vibrato type {self._valueName()}>'

    def __repr__(self):
        return f'{type(self).__name__}({self.value!r})'

# Change the internal name of the VibratoTypeSequenceEvent.Value enum to
# "VibratoTypeSequenceEvent.Value"
VibratoTypeSequenceEvent.Value.__name__ = \
    f'{VibratoTypeSequenceEvent.__name__}.{VibratoTypeSequenceEvent.Value.__name__}'


VibratoRangeSequenceEvent = _make_simple_sequence_event_class(0xCD,
    'Vibrato range', 'VibratoRangeSequenceEvent',
    'related to vibratos')


class PortamentoOnOffSequenceEvent(SequenceEvent):
    """
    A sequence event that enables or disables portamento mode. This is
    sequence event type 0xCE.
    """
    dataLength = 2

    def __init__(self, value):
        super().__init__(0xCE)
        if value in [0, 1]:
            value = bool(value)
        self.value = value

    def save(self, eventsToOffsets=None):
        return super().save() + self.value.to_bytes(1, 'little')

    @classmethod
    def fromData(cls, type, data, startOffset=0):
        return cls(data[startOffset + 1])

    def __str__(self):
        if self.value in [0, 1, False, True]:
            v = 'on' if self.value else 'off'
        else:
            v = self.value
        return f'<portamento {v}>'

    def __repr__(self):
        return f'{type(self).__name__}({self.value!r})'


PortamentoDurationSequenceEvent = _make_simple_sequence_event_class(0xCF,
    'Portamento duration', 'PortamentoDurationSequenceEvent',
    'related to portamentos')

AttackRateSequenceEvent = _make_simple_sequence_event_class(0xD0,
    'Attack rate', 'AttackRateSequenceEvent',
    'that sets the attack rate for notes in the current track')

DecayRateSequenceEvent = _make_simple_sequence_event_class(0xD1,
    'Decay rate', 'DecayRateSequenceEvent',
    'that sets the decay rate for notes in the current track')

SustainRateSequenceEvent = _make_simple_sequence_event_class(0xD2,
    'Sustain rate', 'SustainRateSequenceEvent',
    'that sets the sustain rate for notes in the current track')

ReleaseRateSequenceEvent = _make_simple_sequence_event_class(0xD3,
    'Release rate', 'ReleaseRateSequenceEvent',
    'that sets the release rate for notes in the current track')


class BeginLoopSequenceEvent(SequenceEvent):
    """
    A sequence event that begins a loop in the current track. This is
    sequence event type 0xD4.

    The end of the loop must be marked by an EndLoopSequenceEvent.
    """
    dataLength = 2

    def __init__(self, loopCount):
        super().__init__(0xD4)
        self.loopCount = loopCount

    def save(self, eventsToOffsets=None):
        return super().save() + self.loopCount.to_bytes(1, 'little')

    @classmethod
    def fromData(cls, type, data, startOffset=0):
        return cls(data[startOffset + 1])

    def __str__(self):
        return f'<begin loop {self.loopCount}>'

    def __repr__(self):
        return f'{type(self).__name__}({self.loopCount!r})'


ExpressionSequenceEvent = _make_simple_sequence_event_class(0xD5,
    'Expression', 'ExpressionSequenceEvent', 'that is unknown')

PrintVariableSequenceEvent = _make_simple_sequence_event_class(0xD6,
    'Print variable', 'PrintVariableSequenceEvent', 'that is unknown')

VibratoDelaySequenceEvent = _make_simple_sequence_event_class(0xE0,
    'Vibrato delay', 'VibratoDelaySequenceEvent',
    'related to vibratos')


class TempoSequenceEvent(SequenceEvent):
    """
    A sequence event that sets the tempo for all tracks in the sequence.
    This is sequence event type 0xE1.
    """
    dataLength = 3

    def __init__(self, value):
        super().__init__(0xE1)
        self.value = value

    def save(self, eventsToOffsets=None):
        return super().save() + struct.pack('<H', self.value)

    @classmethod
    def fromData(cls, type, data, startOffset=0):
        return cls(struct.unpack_from('<H', data, startOffset + 1)[0])

    def __str__(self):
        return f'<tempo {self.value}>'

    def __repr__(self):
        return f'{type(self).__name__}({self.value!r})'


class SweepPitchSequenceEvent(SequenceEvent):
    """
    An unknown sequence event type. This is sequence event type 0xE3.
    """
    dataLength = 3

    def __init__(self, value):
        super().__init__(0xE3)
        self.value = value

    def save(self, eventsToOffsets=None):
        return super().save() + struct.pack('<H', self.value)

    @classmethod
    def fromData(cls, type, data, startOffset=0):
        return cls(struct.unpack_from('<H', data, startOffset + 1)[0])

    def __str__(self):
        return f'<sweep pitch {self.value}>'

    def __repr__(self):
        return f'{type(self).__name__}({self.value!r})'


class EndLoopSequenceEvent(SequenceEvent):
    """
    A sequence event that ends a loop previously begun with a
    BeginLoopSequenceEvent. This is sequence event type 0xFC.
    """
    def __init__(self):
        super().__init__(0xFC)

    @classmethod
    def fromData(cls, type, data, startOffset=0):
        return cls()

    def __str__(self):
        return '<end loop>'

    def __repr__(self):
        return f'{type(self).__name__}()'


class ReturnSequenceEvent(SequenceEvent):
    """
    A sequence event that causes execution of the current track to jump
    back to the most recently encountered CallSequenceEvent. This is
    sequence event type 0xFD.
    """
    def __init__(self):
        super().__init__(0xFD)

    @classmethod
    def fromData(cls, type, data, startOffset=0):
        return cls()

    def __str__(self):
        return '<return>'

    def __repr__(self):
        return f'{type(self).__name__}()'


class DefineTracksSequenceEvent(SequenceEvent):
    """
    A sequence event that defines the tracks that will be used in the
    sequence. This is sequence event type 0xFE.
    """
    dataLength = 3

    def __init__(self, trackNumbers):
        super().__init__(0xFE)
        self.trackNumbers = trackNumbers

    def save(self, eventsToOffsets=None):
        tracksBitfield = 0
        for i in range(16):
            if i in self.trackNumbers:
                tracksBitfield |= 1 << i
        return super().save() + struct.pack('<H', tracksBitfield)

    @classmethod
    def fromData(cls, type, data, startOffset=0):
        tracksBitfield, = struct.unpack_from('<H', data, startOffset + 1)
        trackNumbers = set()
        for i in range(16):
            if tracksBitfield & (1 << i):
                trackNumbers.add(i)
        return cls(trackNumbers)

    def __str__(self):
        return f'<define tracks {" ".join(str(x) for x in sorted(self.trackNumbers))}>'

    def __repr__(self):
        return f'{type(self).__name__}({self.trackNumbers!r})'


class EndTrackSequenceEvent(SequenceEvent):
    """
    A sequence event that ends execution of the current track. This is
    sequence event type 0xFF.
    """
    def __init__(self):
        super().__init__(0xFF)

    @classmethod
    def fromData(cls, type, data, startOffset=0):
        return cls()

    def __str__(self):
        return '<end track>'

    def __repr__(self):
        return f'{type(self).__name__}()'


class RawDataSequenceEvent(SequenceEvent):
    """
    A dummy sequence event that represents raw binary data that seems to
    be unreachable as far as ndspy can tell.
    """
    @property
    def dataLength(self):
        return len(self.data)

    def __init__(self, data):
        super().__init__(None)
        self.data = data

    def save(self, eventsToOffsets=None):
        return self.data

    def __str__(self):
        return f'<raw data {bytes(self.data)}>'

    def __repr__(self):
        return f'{type(self).__name__}({self.data!r})'


_EVENT_TYPES = {
    0x80: RestSequenceEvent,
    0x81: InstrumentSwitchSequenceEvent,
    0x93: BeginTrackSequenceEvent,
    0x94: JumpSequenceEvent,
    0x95: CallSequenceEvent,
    0xA0: RandomSequenceEvent,
    0xA1: FromVariableSequenceEvent,
    0xA2: IfSequenceEvent,
    0xB0: VariableAssignmentSequenceEvent,
    0xB1: VariableAdditionSequenceEvent,
    0xB2: VariableSubtractionSequenceEvent,
    0xB3: VariableMultiplicationSequenceEvent,
    0xB4: VariableDivisionSequenceEvent,
    0xB5: VariableShiftSequenceEvent,
    0xB6: VariableRandSequenceEvent,
    0xB7: VariableUnknownB7SequenceEvent,
    0xB8: VariableEqualSequenceEvent,
    0xB9: VariableGreaterThanOrEqualSequenceEvent,
    0xBA: VariableGreaterThanSequenceEvent,
    0xBB: VariableLessThanOrEqualSequenceEvent,
    0xBC: VariableLessThanSequenceEvent,
    0xBD: VariableNotEqualSequenceEvent,
    0xC0: PanSequenceEvent,
    0xC1: TrackVolumeSequenceEvent,
    0xC2: GlobalVolumeSequenceEvent,
    0xC3: TransposeSequenceEvent,
    0xC4: PortamentoSequenceEvent,
    0xC5: PortamentoRangeSequenceEvent,
    0xC6: TrackPrioritySequenceEvent,
    0xC7: MonoPolySequenceEvent,
    0xC8: TieSequenceEvent,
    0xC9: PortamentoFromSequenceEvent,
    0xCA: VibratoDepthSequenceEvent,
    0xCB: VibratoSpeedSequenceEvent,
    0xCC: VibratoTypeSequenceEvent,
    0xCD: VibratoRangeSequenceEvent,
    0xCE: PortamentoOnOffSequenceEvent,
    0xCF: PortamentoDurationSequenceEvent,
    0xD0: AttackRateSequenceEvent,
    0xD1: DecayRateSequenceEvent,
    0xD2: SustainRateSequenceEvent,
    0xD3: ReleaseRateSequenceEvent,
    0xD4: BeginLoopSequenceEvent,
    0xD5: ExpressionSequenceEvent,
    0xD6: PrintVariableSequenceEvent,
    0xE0: VibratoDelaySequenceEvent,
    0xE1: TempoSequenceEvent,
    0xE3: SweepPitchSequenceEvent,
    0xFC: EndLoopSequenceEvent,
    0xFD: ReturnSequenceEvent,
    0xFE: DefineTracksSequenceEvent,
    0xFF: EndTrackSequenceEvent,
}


def readSequenceEvents(data, notableOffsets=None):
    """
    Convert raw sequence event data (as seen in SSEQ and SSAR files) to
    a list of SequenceEvent objects. This is the inverse of
    saveSequenceEvents().

    A second list will also be returned that contains the elements from
    the first list that appeared in the input data at the offsets given
    in notableOffsets.
    """
    if notableOffsets is None: notableOffsets = []

    events = {}

    FATE_INPROGRESS = 0
    FATE_RETURN = 1
    FATE_LOOP = 2
    FATE_EOT = 3
    fates = {}

    def parse_at(off):
        offsetsOfMySequentialEvents = []

        while off < len(data):
            if off in fates:
                fate = fates[off]
                if fate == FATE_INPROGRESS:
                    fate = FATE_LOOP
                for off_ in offsetsOfMySequentialEvents:
                    fates[off_] = fate
                return fate

            try:

                type = data[off]

                if type == 0x93: # BeginTrack
                    trackNumber = data[off + 1]
                    firstEventOff = int.from_bytes(data[off + 2 : off + 5], 'little') # 3-byte int

                    event = BeginTrackSequenceEvent(trackNumber, None)
                    events[off] = event
                    fates[off] = FATE_INPROGRESS
                    parse_at(firstEventOff)
                    event.firstEvent = events[firstEventOff]

                elif type == 0x94: # Jump
                    destination = int.from_bytes(data[off + 1 : off + 4], 'little') # 3-byte int

                    event = JumpSequenceEvent(None)
                    events[off] = event
                    fates[off] = FATE_INPROGRESS
                    fate = parse_at(destination)
                    event.destination = events[destination]

                    for off_ in offsetsOfMySequentialEvents:
                        fates[off_] = fate

                    # Should we keep parsing past here? Only if this
                    # is part of an if statement (and thus might be
                    # skipped).
                    x = off - 1
                    while x not in events and x >= 0:
                        x -= 1
                    if x == -1:
                        partOfIfStatement = False
                    else:
                        partOfIfStatement = (events[x].type == 0xA2)

                    if not partOfIfStatement:
                        return fate

                elif type == 0x95: # Call
                    destination = int.from_bytes(data[off + 1 : off + 4], 'little') # 3-byte int

                    event = CallSequenceEvent(None)
                    events[off] = event
                    fates[off] = FATE_INPROGRESS
                    fate = parse_at(destination)
                    event.destination = events[destination]

                    if fate == FATE_EOT:
                        fates[off] = fate
                        for off_ in offsetsOfMySequentialEvents:
                            fates[off_] = fate
                        return fate
                    elif fate == FATE_RETURN:
                        pass
                    elif fate == FATE_LOOP:
                        fates[off] = fate
                        for off_ in offsetsOfMySequentialEvents:
                            fates[off_] = fate
                        return fate

                elif type == 0xFD: # Return
                    events[off] = ReturnSequenceEvent()
                    fates[off] = FATE_RETURN
                    for off_ in offsetsOfMySequentialEvents:
                        fates[off_] = FATE_RETURN
                    return FATE_RETURN

                elif type == 0xFF: # EoT
                    events[off] = EndTrackSequenceEvent()
                    fates[off] = FATE_EOT
                    for off_ in offsetsOfMySequentialEvents:
                        fates[off_] = FATE_EOT
                    return FATE_EOT

                else:

                    if type <= 0x7F:
                        eventCls = NoteSequenceEvent
                    elif type not in _EVENT_TYPES:
                        raise ValueError(f'Event {hex(type)} unrecognized.')
                    else:
                        eventCls = _EVENT_TYPES[type]

                    event = eventCls.fromData(type, data, off)
                    events[off] = event
                    fates[off] = FATE_INPROGRESS

                offsetsOfMySequentialEvents.append(off)
                off += event.dataLength

            except (struct.error, IndexError):
                raise EOFError('Reached EoF of sequence.')
        raise EOFError('Reached EoF of sequence.')

    starts = notableOffsets
    if not starts: starts = [0]
    for start in starts:
        ultimateFate = parse_at(start)
        assert ultimateFate in (FATE_EOT, FATE_LOOP), f'Starting point {hex(start)} results in fate {ultimateFate}'

    eventsList = []
    i = 0
    while i < len(data):
        if i in events:
            eventsList.append(events[i])
            i += events[i].dataLength
        else:
            j = i
            while j not in events and j < len(data):
                j += 1
            eventsList.append(RawDataSequenceEvent(data[i:j]))
            i = j

    notableEvents = [events[off] for off in notableOffsets]

    return eventsList, notableEvents


def saveSequenceEvents(events, notableEvents=None):
    """
    Convert a list of SequenceEvent objects to raw sequence event data.
    This is the inverse of readSequenceEvents().

    A second list will also be returned that contains the offsets in the
    output data of the elements from notableEvents.
    """
    if notableEvents is None: notableEvents = []
    
    events2Offsets = {}

    off = 0
    for e in events:
        events2Offsets[e] = off
        off += e.dataLength
    data = bytearray(off)

    for event, offset in events2Offsets.items():
        eData = event.save(events2Offsets)
        data[offset : offset + len(eData)] = eData

    notableOffsets = [events2Offsets[e] for e in notableEvents]

    return data, notableOffsets


def printSequenceEventList(events, labels=None, linePrefix=''):
    """
    Produce a string representation of a list of sequence events. You
    can optionally provide a dictionary of labels to mark certain
    events, and a prefix string that will be prepended to every line.
    """
    if labels is None: labels = {}

    warningsList = []
    linesList = []

    maxNameLen = 0
    i2SfxName = {}
    for name, event in labels.items():
        if event in events:
            i = events.index(event)
        elif event is None:
            linesList.append(f'{linePrefix}{name}: (none)')
            continue
        else:
            warningsList.append(f'{linePrefix}(WARNING: {event!r} ({name}) not in events list!)')
            continue
        if name is None: name = str(i)
        if i not in i2SfxName:
            i2SfxName[i] = name
        else:
            i2SfxName[i] += ', ' + name
        maxNameLen = max(maxNameLen, len(i2SfxName[i]))
    maxNameLen = min(maxNameLen, 48)
    maxNumLen = len(str(len(events) - 1))

    maxNameLen += 1 # for the ":" at the end

    def getDestinationStr(primaryEvent, destination):
        if destination in events:
            return str(events.index(destination))
        else:
            warningsList.append(f'{linePrefix}(WARNING: {destination!r} (target of {primaryEvent!r}) not in events list!)')
            return 'NOWHERE'

    def printEvent(e):
        label = i2SfxName[i] + ':' if i in i2SfxName else ''
        labelLst = []
        while label:
            labelLst.append(label[:maxNameLen])
            label = label[maxNameLen:]
        if labelLst:
            labelLst[-1] = f'{labelLst[-1]:{maxNameLen}}'
        else:
            labelLst = [' ' * maxNameLen]
        label = f'\n{linePrefix}'.join(labelLst)

        if isinstance(e, JumpSequenceEvent):
            etext = f'<jump @{getDestinationStr(e, e.destination)}>'
        elif isinstance(e, CallSequenceEvent):
            etext = f'<call @{getDestinationStr(e, e.destination)}>'
        elif isinstance(e, BeginTrackSequenceEvent):
            etext = f'<begin track {e.trackNumber} @{getDestinationStr(e, e.firstEvent)}>'
        else:
            etext = str(e)

        return f'{linePrefix}{label}  [{i:{maxNumLen}}] {etext},'

    for i, e in enumerate(events):
        linesList.append(printEvent(e))

    # Remove last ","
    if events:
        linesList[-1] = linesList[-1][:-1]

    return '\n'.join(warningsList + linesList)
