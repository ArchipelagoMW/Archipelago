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
Support for BMG files.
"""

from __future__ import annotations

import os
import struct
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Literal

from . import _common


# (Please keep this in sync with the type annotation for the
# `BMG.encoding` attribute:)
_ENCODINGS = [None, 'cp1252', 'utf-16', 'shift-jis', 'utf-8']
# CP1252 is found in Animal Crossing Wild World and Super Princess Peach
# UTF-16 is found in the Zeldas and NSMB
# SJIS is found in Super Princess Peach
# UTF-8 is found in WarioWare DIY


class BMG:
    """
    A class representing a BMG file.
    """
    messages: list[Message]
    instructions: list[bytes]
    labels: list[tuple[int, int]]
    scripts: list[tuple[int, int]]

    id: int
    # (Please keep this in sync with the `_ENCODINGS` global:)
    encoding: Literal['cp1252', 'utf-16', 'shift-jis', 'utf-8']
    endianness: Literal['<', '>']
    unk14: int
    unk18: int
    unk1C: int

    def __init__(self, data: bytes | None = None, *, id: int = 0):

        self.messages = []
        self.instructions = []
        self.labels = []
        self.scripts = []

        self.id = id

        self.encoding = 'utf-16'
        self.endianness = '<'
        self.unk14 = 0
        self.unk18 = 0
        self.unk1C = 0

        if data is not None:
            self._initFromData(data)


    @property
    def fullEncoding(self) -> str:
        if self.encoding.lower() == 'utf-16':
            return 'utf-16' + ('le' if self.endianness == '<' else 'be')
        return self.encoding


    def _initFromData(self, data: bytes) -> None:
        if data[:8] != b'MESGbmg1':
            raise ValueError('Not a BMG file.')

        # Super Princess Peach uses *big-endian* BMGs. What even.

        # Well, OK, whatever. We can make an extremely accurate guess by
        # reading the file length value both ways and seeing which one
        # seems to make more sense:
        dataLenLE, = struct.unpack_from('<I', data, 8)
        dataLenBE, = struct.unpack_from('>I', data, 8)
        self.endianness = se = '<' if dataLenLE < dataLenBE else '>'
        # Still, though... ugh.

        magic, dataLen, sectionCount, enc, self.unk14, self.unk18, self.unk1C = \
            struct.unpack_from(se + '8sIIB3I', data, 0)
        if enc != 0 and enc < len(_ENCODINGS):
            self.encoding = _ENCODINGS[enc]
        else:
            raise ValueError(f'Unknown encoding value: {enc}')

        INF1 = []
        def parseINF1(offset: int, length: int) -> None:
            count, entryLength, self.id = struct.unpack_from(se + 'HHI', data, offset + 8)

            for i in range(count):
                thingOff = offset + 16 + i * entryLength
                entryOff, = struct.unpack_from(se + 'I', data, thingOff)
                entryAttribs = data[thingOff + 4 : thingOff + entryLength]
                INF1.append((entryOff, entryAttribs))

        DAT1 = b''
        def parseDAT1(offset: int, length: int) -> None:
            nonlocal DAT1
            DAT1 = data[offset + 8 : offset + length]

        self.instructions = []
        self.labels = []
        def parseFLW1(offset: int, length: int) -> None:
            instructionsCount, labelsCount, unk0C = \
                struct.unpack_from(se + 'HHI', data, offset + 8)
            # unk0C is always 0, as far as I can tell

            instructionsTableOffset = offset + 16
            for i in range(instructionsCount):
                instOff = instructionsTableOffset + i * 8
                cmd = data[instOff : instOff + 8]
                if cmd != b'\0\0\0\0\0\0\0\0':
                    self.instructions.append(cmd)

            indicesTableOffset = instructionsTableOffset + instructionsCount * 8
            bmgIDsTableOffset = indicesTableOffset + labelsCount * 2
            for i in range(labelsCount):
                index, = struct.unpack_from(se + 'h', data, indicesTableOffset + i * 2)
                bmgID, = struct.unpack_from(se + 'b', data, bmgIDsTableOffset + i)
                if bmgID != 0 or index != 0:
                    self.labels.append((bmgID, index))

        self.scripts = []
        def parseFLI1(offset: int, length: int) -> None:
            count, entryLength, unk0C = struct.unpack_from(se + 'HHI', data, offset + 8)
            assert entryLength == 8, f'Unexpected FLI1 entry length ({entryLength})'
            # unk0C is always 0, as far as I can tell

            for i in range(count):
                id, index = struct.unpack_from(se + 'IHxx', data, offset + 16 + i * 8)
                self.scripts.append((id, index))

        offset = 0x20
        for i in range(sectionCount):
            sectionMagic, sectionLen = struct.unpack_from(se + '4sI', data, offset)
            if sectionMagic == b'INF1':
                parseINF1(offset, sectionLen)
            elif sectionMagic == b'DAT1':
                parseDAT1(offset, sectionLen)
            elif sectionMagic == b'FLW1':
                parseFLW1(offset, sectionLen)
            elif sectionMagic == b'FLI1':
                parseFLI1(offset, sectionLen)
            else:
                raise ValueError('Unknown BMG section: ' + repr(sectionMagic))
            offset += sectionLen

        # Now we just need to read the messages.

        nullChar = '\0'.encode(self.fullEncoding)
        escapeSequenceStart = '\x1A'.encode(self.fullEncoding)

        self.messages = []
        for offset, attribs in INF1:

            # The "currentStringStart" setup may seem needlessly
            # confusing, but it's intended to keep the number of calls
            # to bytes.decode() to a minimum. Based on my testing, it
            # really does make the code run significantly faster.

            stringParts = []
            currentStringStart = offset

            nextBytes = DAT1[offset : offset + len(nullChar)]
            while nextBytes != nullChar:
                if nextBytes == escapeSequenceStart: # escape sequence
                    if currentStringStart and currentStringStart != offset:
                        stringParts.append(DAT1[currentStringStart:offset].decode(self.fullEncoding))
                    escapeLen, escapeType = DAT1[offset + len(escapeSequenceStart) : offset + len(escapeSequenceStart) + 2]
                    escapeData = DAT1[offset + len(escapeSequenceStart) + 2 : offset + escapeLen]
                    stringParts.append(Message.Escape(escapeType, escapeData))
                    offset += escapeLen
                    currentStringStart = offset
                else:
                    offset += len(nullChar)

                nextBytes = DAT1[offset : offset + len(nullChar)]

            if currentStringStart and currentStringStart != offset:
                stringParts.append(DAT1[currentStringStart:offset].decode(self.fullEncoding))

            self.messages.append(Message(attribs, stringParts, offset == 0))


    @classmethod
    def fromMessages(
        cls,
        messages: list[Message],
        instructions: list[bytes] | None = None,
        labels: list[tuple[int, int]] | None = None,
        scripts: list[tuple[int, int]] | None = None,
        *,
        id: int = 0,
    ) -> BMG:
        """
        Create a BMG from a list of messages.
        """
        self = cls(id=id)
        self.messages = messages

        if instructions is not None:
            self.instructions = instructions
        if labels is not None:
            self.labels = labels
        if scripts is not None:
            self.scripts = scripts

        return self


    @classmethod
    def fromFile(cls, filePath: str | os.PathLike, *args, **kwargs) -> BMG:
        """
        Load a BMG from a filesystem file.
        """
        with open(filePath, 'rb') as f:
            return cls(f.read(), *args, **kwargs)


    def save(self) -> bytes:
        """
        Generate file data representing this BMG.
        """
        se = self.endianness
        if se not in '<>':
            raise ValueError(f"BMG.endianness is '{se}', which is"
                             f" neither '<' nor '>'")
        if not isinstance(self.encoding, str) or \
                self.encoding.lower() not in _ENCODINGS:
            raise ValueError(f'Unknown BMG encoding: {self.encoding}')

        data = bytearray(0x20)

        instructionsCount = len(self.instructions)
        if instructionsCount % 2: instructionsCount += 1

        labelsCount = len(self.labels)
        while labelsCount % 8: labelsCount += 1

        INF1 = bytearray(16)
        DAT1 = bytearray(8)
        FLW1 = bytearray(16)
        FLI1 = bytearray(16)

        DAT1.extend('\0'.encode(self.fullEncoding))

        if self.messages:
            inf1EntryLen = 4 + len(self.messages[0].info)
        else:
            inf1EntryLen = 4

        for i, message in enumerate(self.messages):
            if len(message.info) != inf1EntryLen - 4:
                raise ValueError(f'Message info values are presumed to'
                                 f' be {inf1EntryLen - 4} bytes long,'
                                 f' but message {i} has a'
                                 f' {len(message.info)}-byte-long info'
                                 f' value!')

            offset = 0 if message.isNull else len(DAT1) - 8
            INF1.extend(struct.pack(se + 'I', offset))
            INF1.extend(message.info)
            if not message.isNull:
                DAT1.extend(message.save(self.fullEncoding))

        for inst in self.instructions:
            if hasattr(inst, 'save'):
                inst = inst.save()
            if len(inst) != 8:
                raise ValueError(f'Length of instruction {inst} is not 8 bytes!')
            FLW1.extend(inst)
        while len(FLW1) % 16: FLW1.extend(b'\0' * 8)

        for bmgID, instIndex in self.labels:
            FLW1.extend(struct.pack(se + 'h', instIndex))
        for _ in range(labelsCount - len(self.labels)):
            FLW1.extend(b'\0\0')
        for bmgID, instIndex in self.labels:
            FLW1.extend(struct.pack(se + 'b', bmgID))

        for id, startIndex in self.scripts:
            FLI1.extend(struct.pack(se + 'II', id, startIndex))

        # Sections' lengths must be 32-byte aligned
        while len(INF1) % 32: INF1.append(0)
        while len(DAT1) % 32: DAT1.append(0)
        while len(FLW1) % 32: FLW1.append(0)

        # FLI1's length isn't actually padded, but the length it claims
        # in its header is. (I know. It's confusing.)
        FLI1len = len(FLI1)
        while FLI1len % 32: FLI1len += 1

        # Pack section headers
        struct.pack_into(se + '4sIHHI', INF1, 0,
            b'INF1', len(INF1), len(self.messages), inf1EntryLen, self.id)
        struct.pack_into(se + '4sI', DAT1, 0, b'DAT1', len(DAT1))
        struct.pack_into(se + '4sIHH', FLW1, 0,
            b'FLW1', len(FLW1), instructionsCount, labelsCount)
        struct.pack_into(se + '4sIHH', FLI1, 0,
            b'FLI1', FLI1len, len(self.scripts), 8)

        # Insert the sections
        numSections = 2
        data.extend(INF1)
        data.extend(DAT1)
        if self.instructions or self.labels:
            numSections += 1
            data.extend(FLW1)
        if self.scripts:
            numSections += 1
            data.extend(FLI1)

        # Pack the BMG header
        totalLen = len(data)
        while totalLen % 32: totalLen += 1
        struct.pack_into(se + '8sIIB3I', data, 0,
            b'MESGbmg1', totalLen, numSections,
            _ENCODINGS.index(self.encoding.lower()), self.unk14, self.unk18, self.unk1C)

        return bytes(data)


    def saveToFile(self, filePath: str | os.PathLike) -> None:
        """
        Generate file data representing this BMG, and save it to a
        filesystem file.
        """
        d = self.save()
        with open(filePath, 'wb') as f:
            f.write(d)


    def __str__(self) -> str:
        return (f'<bmg id={self.id} '
                f'({len(self.messages)} messages, '
                f'{len(self.scripts)} scripts)>')


    def __repr__(self) -> str:
        args = [repr(self.messages)]

        if self.instructions:
            args.append(repr(self.instructions))

        if self.labels:
            p = ''
            if len(args) < 2:
                p = 'labels='
            args.append(p + repr(self.labels))

        if self.scripts:
            p = ''
            if len(args) < 3:
                p = 'scripts='
            args.append(p + repr(self.scripts))

        args.append(f'id={self.id:#x}')

        return (f'{type(self).__name__}.fromMessages('
                f'{", ".join(args)})')


class Message:
    """
    A single message in a BMG file.
    """

    class Escape:
        """
        An escape sequence within a BMG message. Escape sequences have a
        type and optional parameter data.
        """

        type: int
        data: bytes

        def __init__(self, type: int = 0, data: bytes = b''):
            self.type = type
            self.data = data

            # Type = 4 is used for pluralization in Spirit Tracks
            # (and there are a couple parameters -- need to look into
            # that)

        def save(self, encoding: str) -> bytes:
            """
            Generate binary data representing this escape sequence.
            """
            start = '\x1A'.encode(encoding)
            data = bytearray(start)
            data.append(len(self.data) + 2 + len(start))
            data.append(self.type)
            data.extend(self.data)
            return data

        def __repr__(self) -> str:
            return f'{type(self).__name__}({self.type!r}, {self.data!r})'

        def __str__(self) -> str:
            return f'[{self.type}:{self.data.hex()}]'

    info: bytes
    stringParts: list[str | Escape]
    isNull: bool

    def __init__(
        self,
        info: bytes = b'',
        stringParts: str | list[str] | None = None,
        isNull: bool = False,
    ):
        # If a single string is passed in, put it in a list for convenience
        if isinstance(stringParts, str):
            stringParts = [stringParts]

        self.info = info
        self.stringParts = [] if stringParts is None else stringParts
        self.isNull = isNull

    def save(self, encoding: str) -> bytes:
        """
        Generate binary data representing this message.
        """
        if self.isNull: return b''

        data = bytearray()
        for part in self.stringParts:
            if isinstance(part, str):
                if '\0' in part:
                    raise ValueError('Null character found in message during BMG saving')
                if '\x1A' in part:
                    raise ValueError('\\x1A character found in message during BMG saving')
                data.extend(part.encode(encoding))
            else:
                data.extend(part.save(encoding))
        data.extend('\0'.encode(encoding))
        return data

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self.info!r}, {self.stringParts!r})'

    def __str__(self) -> str:
        return ''.join(str(s) for s in self.stringParts)
