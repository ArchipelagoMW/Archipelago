# Copyright 2020 RoadrunnerWMC
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
Support for loading WBMGT text files as patches for ndspy.bmg.BMG
objects
"""

import string

from ... import bmg

from . import _common


def patch(bmg, data, **kwargs):
    """
    Load WBMGT text data, and apply it as a patch to a BMG object
    """
    WBMGTPatcher(bmg, data, **kwargs).patch()


class WBMGTPatcher:
    """
    Because the patch() function was getting uncomfortably long.
    """
    def __init__(self, bmg, data, *,
            messageIDParseFunction=None, uEscapeFunction=None,
            colorParseFunction=None, colorEscapeFunction=None,
            macros=None):
        self.bmg = bmg
        self.data = data

        self.messageIDParseFunction = messageIDParseFunction
        self.uEscapeFunction = uEscapeFunction
        self.colorParseFunction = colorParseFunction
        self.colorEscapeFunction = colorEscapeFunction
        self.macros = {} if macros is None else macros

        self.infSize = None
        self.defaultAttribs = None


    def iterInterestingLines(self):
        """
        Iterate over non-empty and non-comment WBMGT lines, and lstrip
        each one
        """
        for line in self.data.splitlines():
            line = line.lstrip()
            if line.startswith('#') or not line: continue
            yield line


    def getMessageForID(self, id):
        """
        Retrieve the Message object for the given message ID, creating
        it if it doesn't already exist.

        self.defaultAttribs must have already been initialized before
        calling this function.
        """
        if id > 99999:
            # Raise an exception instead of consuming all of the
            # computer's RAM
            raise RuntimeError(f'Message ID {id} is too high; resulting BMG file would be huge!')

        # Fill in null messages as needed
        while id >= len(self.bmg.messages):
            self.bmg.messages.append(bmg.Message(self.defaultAttribs, [], True))

        return self.bmg.messages[id]


    def handleGlobalParameters(self):
        """
        Handle all @PARAMETER lines.

        Note that "#" comments are allowed in these, and so need to be
        removed when parsing.
        """

        # Locate @INF-SIZE first, since that's required to properly
        # parse the @DEFAULT-ATTRIBS one

        self.infSize = None
        for line in self.iterInterestingLines():
            line = line.split('#')[0]

            if line.startswith('@INF-SIZE'):
                self.infSize = int(line.split('=')[-1].strip(), 0)

        if self.infSize is None or self.infSize < 4 or self.infSize > 1000:
            self.infSize = 8 # Default value used by wbmgt in these cases

        # Now handle all the other @PARAMETER lines

        for line in self.iterInterestingLines():
            line = line.split('#')[0]

            if line.startswith('@DEFAULT-ATTRIBS'):
                self.defaultAttribs = self.parseAttributesString(
                    line.split('=')[-1].strip(),
                    self.infSize - 4)

            elif line.startswith('@BMG-MID'):
                if line.split('=')[-1].strip() != '0':
                    raise ValueError('ndspy does not support MID1 sections')

        if self.defaultAttribs is None:
            self.defaultAttribs = b'\0' * (self.infSize - 4)


    def patch(self):
        """
        Parse the WBMGT and apply it as a patch over the BMG object
        """
        if not self.data.startswith('#BMG'):
            raise ValueError('Incorrect WBMGT file magic')

        # Parse all @PARAMETER lines first
        self.handleGlobalParameters()

        # And now parse all message lines

        messageAssignments = []
        previousMessageID = None  # used for "+" line continuations

        for line in self.iterInterestingLines():

            # Ignore @PARAMETER lines
            if line.startswith('@'): continue

            i = 0  # Index of the current character in the line
            attrib = None  # Attribute value explicitly specified in the
                           # line (or None)
            canBeContinued = False # Whether the next line is allowed to
                                   # be a continuation line

            if line[i] == '+':
                # This is a continuation line.

                if previousMessageID is None:
                    raise ValueError('Trying to "+"-continue a line that can\'t be continued')

                # Spec says to skip 0 or 1 spaces or tabs
                if i + 1 < len(line) and line[i] in ' \t':
                    i += 1

                # We can access the message directly instead of through
                # self.getMessageForID(), since the message is
                # guaranteed to already exist
                message = self.bmg.messages[previousMessageID]
                sp = self.parseStringParts(line, i + 1)

                # If the message currently ends with a str-type part,
                # and the new string parts begin with a str-type part,
                # combine them when putting the lists together
                if message.stringParts and isinstance(message.stringParts[-1], str) and sp and isinstance(sp[0], str):
                    sp[0] = message.stringParts[-1] + sp[0]
                    message.stringParts.pop()

                # Combine lists
                message.stringParts += sp

            else:
                # Start of a new message line.

                # Read the message ID
                while line[i] in (string.ascii_letters + string.digits): i += 1
                messageID = self.parseMessageID(line[:i])

                # Read whitespace
                while line[i] in ' \t': i += 1

                # Read the optional attrib value
                if line[i] == '[':
                    endBracketIdx = line.find(']')
                    if endBracketIdx == -1:
                        raise ValueError('Unclosed attributes "[" bracket')
                    attrib = self.parseAttributesString(line[i : endBracketIdx+1], self.infSize - 4)
                    i = endBracketIdx + 1

                    # Read whitespace
                    while line[i] in ' \t': i += 1

                if line[i] == '~':  # MID ~ ATTRIB32
                    if attrib is not None:
                        raise ValueError("\"MID '[' ATTRIB ']' ~\" is not valid syntax")

                    i += 1 # skip '~'

                    # Read whitespace
                    while line[i] in ' \t': i += 1

                    # Read ATTRIB32
                    attribVal = int(line[i:], 16)
                    attrib = attribVal.to_bytes(self.infSize - 4, 'big')

                    # Apply the attribute to message
                    self.getMessageForID(messageID).info = attrib

                elif line[i] == '/':  # MID / or MID '[' ATTRIB ']' /

                    message = self.getMessageForID(messageID)

                    if attrib is not None:
                        # Apply the attribute to the message
                        message.info = attrib

                    # Set the message to null
                    message.isNull = True
                    message.stringParts.clear()

                elif line[i] == '=':  # MID = or MID '[' ATTRIB ']' =

                    message = self.getMessageForID(messageID)

                    if attrib is not None:
                        # "MID '[' ATTRIB ']' = string" line
                        # Apply the attribute to the message
                        message.info = attrib

                    message.stringParts = self.parseStringParts(line, i + 1)
                    message.isNull = False

                    canBeContinued = True  # "+" lines following this one are allowed

                elif line[i] == ':':  # MID1 : MID2
                    if attrib is not None:
                        raise ValueError("\"MID '[' ATTRIB ']' :\" is not valid syntax")

                    i += 1 # skip ':'

                    # Read whitespace
                    while line[i] in ' \t': i += 1

                    # Read the second message ID
                    mid2Start = i
                    while i < len(line) and line[i] in (string.ascii_letters + string.digits): i += 1
                    messageID2 = self.parseMessageID(line[mid2Start:i])

                    messageAssignments.append((messageID, messageID2))

                else:
                    raise ValueError('Unknown WBMGT line syntax: ' + line)

                # Keep track of the current message ID iff the line is
                # allowed to be followed with more "+" lines
                if canBeContinued:
                    previousMessageID = messageID
                else:
                    previousMessageID = None

        # Now handle all of the message assignments, in order
        for mid1, mid2 in messageAssignments:
            cloneMessageInto(self.getMessageForID(mid2),
                              self.getMessageForID(mid1))


    def parseStringParts(self, line, startAt):
        """
        Return a stringParts list representing the provided line,
        starting at index startAt (which should point to the character
        directly after the "=" or "+")
        """

        # We're going to iterate over the raw string parts in this line,
        # and remove empty ones and combine strings where possible.
        stringParts = []
        for item in self.iterRawStringPartsFromLine(line, startAt):

            # If the item's empty, ignore
            if isinstance(item, str) and not item:
                continue

            # If this item and the last item currently in the list are
            # both strings, append it to that string.
            if stringParts and isinstance(item, str) and isinstance(stringParts[-1], str):
                stringParts[-1] += item
            else:
                stringParts.append(item)

        return stringParts


    def iterRawStringPartsFromLine(self, line, startAt):
        """
        Iterator used by parseStringParts(), which yields items suitable
        for inclusion in a stringParts list, in order.
        The sequence of items yielded by this function may not be in
        minimal form -- that is, it may yield string-typed values
        multiple times in a row. (parseStringParts() takes care of
        combining them.)
        """
        i = startAt

        # Spec says to skip 0 or 1 spaces or tabs
        if i + 1 < len(line) and line[i] in ' \t':
            i += 1

        while i < len(line):
            nextBackslash = line.find('\\', i)

            if nextBackslash == -1:
                # No more backslashes!
                yield line[i:]
                return

            else:
                # Read string up until that backslash
                yield line[i:nextBackslash]
                i = nextBackslash

                # Skip past the backslash
                i += 1
                assert i < len(line), 'backslash followed by newline is illegal'

                # Now actually handle the escape.

                # First, check if it's one of the standard C-langauge escapes
                equivControl = _common.CONTROL_ESCAPES_INV.get('\\' + line[i])
                if equivControl is not None:
                    # Yay
                    yield equivControl
                    i += 1

                else:
                    # One of the WBMGT-specific escape types, then...
                    if line[i] in string.octdigits:  # Octal escape
                        if i + 2 < len(line) and line[i + 1] in string.octdigits and line[i + 2] in string.octdigits:
                            # \nnn
                            yield chr(int(line[i:i+3], 8))
                            i += 3
                        elif i + 1 < len(line) and line[i + 1] in string.octdigits:
                            # \nn
                            yield chr(int(line[i:i+2], 8))
                            i += 2
                        else:
                            # \n
                            yield chr(int(line[i], 8))
                            i += 1

                    elif line[i] in _common.BRACKETED_ESCAPES:
                        escapeType = line[i]

                        i += 1  # skip "{"
                        assert line[i] == '{', f'invalid \\{escapeType} escape'
                        extraInfoStart = i + 1
                        while line[i] != '}': i += 1
                        extraInfo = line[extraInfoStart : i]
                        i += 1  # skip "}"

                        # There's a lot of code for these, so it's split
                        # into its own function.
                        yield from self.iterRawStringPartsFromBracketedEscape(escapeType, extraInfo)

                    else:
                        raise ValueError('Unknown escape sequence in line: ' + line)


    def iterRawStringPartsFromBracketedEscape(self, escapeType, extraInfo):
        """
        Read one of the escape types that include {} braces, and yield
        stringParts items from it.
        - escapeType: the escape type (1-char string)
          Must be one of the characters in _common.BRACKETED_ESCAPES.
        - extraInfo: string containing whatever was in the braces
        """
        if escapeType in 'mM':  # \m{} or \M{} message/macro insertion

            # There can be multiple comma-separated values
            for numStr in extraInfo.split(','):
                v = int(numStr, 16)

                if escapeType == 'm' and v < len(self.bmg.messages):
                    # Insert string parts from that message
                    # (\m{}-escapes only, not \M{}-escapes)
                    for thing in self.bmg.messages[v].stringParts:
                        yield thing

                elif v in self.macros:
                    # Insert macro text
                    macro = self.macros[v]

                    # Macro can be a str, Message.Escape, or
                    # a list of those
                    if isinstance(macro, list) or isinstance(macro, tuple):
                        for thing in macro:
                            yield thing
                    else:
                        yield macro

                else:
                    # Spec says to do this :P
                    yield '\\' + escapeType + '{' + hex(v)[2:] + '}'

        elif escapeType in 'xu':  # \x{} hex escape
                                  # or \u{} Nintendo 32-bit char escape

            # There can be multiple comma-separated values
            for numStr in extraInfo.split(','):
                v = int(numStr, 16)

                if escapeType == 'x':
                    # 16-bit codepoint
                    yield chr(v & 0xFFFF)
                else:
                    # 32-bit codepoint, inserted using
                    # self.uEscapeFunction().
                    v &= 0xFFFFFFFF
                    yield self.escapeUValue(v)

        elif escapeType == 'z':  # \z{} Nintendo escape
            yield self.parseNintendoEscapeBody(extraInfo)

        elif escapeType == 'c':  # \c{} color escape
            yield self.escapeColorValue(self.parseColorValue(extraInfo.strip()))


    def parseMessageID(self, s):
        """
        Parse the given message ID string, as hex if possible, or else
        with self.messageIDParseFunction (if not None)
        """
        if s[0] in string.hexdigits:
            # Standard hex message ID
            return int(s, 16)

        # If we reached here, it's a custom message ID format.

        # (Exception to raise if the message ID string turns out to be
        # invalid)
        exc = ValueError('Invalid message ID: ' + s)

        # Use the custom parser function if available
        messageID = None
        if self.messageIDParseFunction is not None:
            try:
                messageID = self.messageIDParseFunction(s)
            except Exception:
                # Be sure to raise exc in this
                # "except" block, so that the original exception
                # will be displayed along with the new one
                raise exc

        if messageID is None:
            # We could reach here if there was no messageIDParseFunction
            # provided, or if it returned None.
            # Regardless of which reason, we raise an exception here.
            raise exc

        else:
            return messageID


    def parseColorValue(self, s):
        """
        Parse the given color value string, as hex if possible, or else
        with self.colorParseFunction (if not None)
        """
        if all(c in string.hexdigits for c in s):
            # Standard hex color ID
            return int(s, 16)

        # If we reached here, it's a custom color value format.

        # (Exception to raise if the color value string turns out to be
        # invalid)
        exc = ValueError('Invalid color value: ' + s)

        # Use the custom parser function if available
        color = None
        if self.colorParseFunction is not None:
            try:
                color = self.colorParseFunction(s)
            except Exception:
                # Be sure to raise exc in this
                # "except" block, so that the original exception
                # will be displayed along with the new one
                raise exc

        if color is None:
            # We could reach here if there was no colorParseFunction
            # provided, or if it returned None.
            # Regardless of which reason, we raise an exception here.
            raise exc

        else:
            return color


    def escapeUValue(self, v):
        """
        U-Escape the given 32-bit value with self.uEscapeFunction (if
        not None)
        """

        # (Exception to raise if the value cannot be escaped)
        exc = ValueError(f'Unable to escape value: 0x{v:x}')

        # Use the custom escaper function if available
        escape = None
        if self.uEscapeFunction is not None:
            try:
                escape = self.uEscapeFunction(v)
            except Exception:
                # Be sure to raise exc in this
                # "except" block, so that the original exception
                # will be displayed along with the new one
                raise exc

        if escape is None:
            # We could reach here if there was no uEscapeFunction
            # provided, or if it returned None.
            # Regardless of which reason, we raise an exception here.
            raise exc

        else:
            return escape


    def escapeColorValue(self, v):
        """
        Color-escape the given color value with self.colorEscapeFunction
        (if not None)
        """

        # (Exception to raise if the color cannot be escaped)
        exc = ValueError(f'Unable to escape color: 0x{v:x}')

        # Use the custom escaper function if available
        escape = None
        if self.colorEscapeFunction is not None:
            try:
                escape = self.colorEscapeFunction(v)
            except Exception:
                # Be sure to raise exc in this
                # "except" block, so that the original exception
                # will be displayed along with the new one
                raise exc

        if escape is None:
            # We could reach here if there was no colorEscapeFunction
            # provided, or if it returned None.
            # Regardless of which reason, we raise an exception here.
            raise exc

        else:
            return escape


    @staticmethod
    def parseAttributesString(s, totalLength):
        """
        Convert the provided attributes string to a bytes object of length
        totalLength.
        The data will be truncated if longer than totalLength.
        """
        assert s.startswith('[') and s.endswith(']')

        values = []

        v = None
        for i in range(1, len(s) - 1):  # ignore "[" and "]"
            c = s[i]

            if c in string.hexdigits:
                if v is None: v = 0
                v = ((v << 4) | int(c, 16)) & 0xFF

            elif c == ',':
                values.append(0 if v is None else v)
                v = None

            elif c == '/':
                # While the spec doesn't really clarify if e.g. "[/5]"
                # means "[5]" or "[0,0,0,0,5]", the reference
                # implementation interprets it as the latter. So we
                # append one zero before aligning, to accomplish that.
                values.append(0 if v is None else v)  # see above
                while len(values) % 4:
                    values.append(0)
                v = None

        if v is not None:
            values.append(v)

        # Pad or truncate to proper length
        while len(values) < totalLength:
            values.append(0)
        if len(values) > totalLength:
            values = values[:totalLength]

        # Return bytes
        return bytes(values)


    @staticmethod
    def parseNintendoEscapeBody(body):
        r"""
        Parse the body (the part within the braces) of a Nintendo escape
        (\z{}).
        Return a bmg.Message.Escape.
        """

        # This is a really stupid algorithm, but we do it this way to
        # match wbmgt's (stupid) behavior exactly.

        # The part of the spec that tries to explain these escapes is
        # largely unclear ("5 or more characters of each 16-bit"?) or
        # flat-out wrong ("In this case, a padding 0 is appended on
        # UTF-16 encodings"), so this implementation is instead based on
        # the reference implementation (v2.13a)'s behavior. (Note:
        # certain older versions (probably < 2.08a) handled these
        # escapes quite differently.)

        # Terminology: "chunk" = one comma-separated hex value from the
        # escape body.

        # Get the control values at the beginning
        controlValue = int(body.split(',')[0], 16)
        rawLength = controlValue >> 8
        rawType = controlValue & 0xFF

        # Calculate the target length of the bytes data, as well as a
        # copy of that value that's aligned to 2.
        # "- 4" accounts for the "\x00\x1A" escape character, and the
        # 2 control bytes that follow ("xyy" in the wbmgt spec).
        # The escape character can be 1 or 2 bytes long depending on the
        # encoding, but in the wbmgt text format, the length must always
        # be interpreted as if the output file were UTF-16. (That's what
        # the reference implementation does, at least.)
        # Using the reference implementation to encode "\z{600,1}" in
        # CP-1252, for example, yields 1A 05 00 00 01. (Notice how the
        # 6 is replaced with a 05 in the output.)
        targetLength = rawLength - 4
        targetLengthAligned = targetLength
        if targetLengthAligned % 2: targetLengthAligned += 1

        # Handle "zero-length" edge case
        if targetLength <= 0:
            return bmg.Message.Escape(rawType, b'')

        # Convert all of the chunks (other than the first one, with the
        # control values) to bytes objects, each one padded or truncated
        # to be exactly 8 bytes long
        inputChunks = []
        for chunk in body.split(',')[1:]:
            chunk = chunk.strip().zfill(16)
            if len(chunk) > 16: chunk = chunk[-16:]
            inputChunks.append(bytes.fromhex(chunk))

        # Make a list for us to add output data chunks to.
        # This will be similar to the previous list, except that the
        # first chunk will be trimmed if necessary, and the list may be
        # truncated overall.
        outputChunks = []

        # Trim the first chunk if needed, and add it to the output
        # chunks list
        if targetLengthAligned % 8 == 0:
            outputChunks.append(inputChunks.pop(0))
        else:
            outputChunks.append(inputChunks.pop(0)[-(targetLengthAligned % 8):])

        # Add more chunks until we reach targetLengthAligned
        currentLength = len(outputChunks[0])
        while currentLength < targetLengthAligned:
            if inputChunks:
                outputChunks.append(inputChunks.pop(0))
            else:
                outputChunks.append(b'\0' * 8)

            currentLength += 8

        # Join it all up
        outputData = b''.join(outputChunks)

        # If our target data length is odd, chop off the last byte
        # indiscriminately. (This is dumb -- what the heck, wbmgt??)
        if targetLength % 2:
            outputData = outputData[:-1]

        # Assert that we hit the target length, and return
        assert len(outputData) == targetLength, 'Nintendo escape data length did not match expected length; this indicates a bug in ndspy itself'
        return bmg.Message.Escape(rawType, outputData)


def cloneMessageInto(messageFrom, messageTo):
    """
    Helper function to clone all of the properties of messageFrom into
    messageTo. messageTo will thus become an exact copy of messageFrom.
    (This is used to implement the "MID1 : MID2" syntax.)
    """
    # Easy stuff first
    messageTo.info = messageFrom.info
    messageTo.isNull = messageFrom.isNull

    # And now stringParts
    messageTo.stringParts = []
    for part in messageFrom.stringParts:
        if isinstance(part, str):
            # Easy
            messageTo.stringParts.append(part)

        elif isinstance(part, bmg.Message.Escape):
            # Meh
            messageTo.stringParts.append(
                bmg.Message.Escape(part.type, bytes(part.data)))

        else:
            raise ValueError(f'Unknown item in Message.stringParts: {part}')
