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


import struct

HavePIL = True
try:
    import PIL.Image
except ImportError:
    HavePIL = False

from . import Alignment


# Nintendo DS standard file header:
NDS_STD_FILE_HEADER = struct.Struct('<4sHHIHH')
# - Magic
# - BOM
# - Version (generally 1)
# - File size (including this header)
# - Size of this header (16)
# - Number of blocks


def crc16(data):
    crc = 0xFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            carry = crc & 1
            crc >>= 1
            if carry:
                crc ^= 0xA001
    return crc & 0xFFFF


def loadNullTerminatedStringFrom(
        data, offset, charWidth=1, encoding='latin-1'):
    """
    Load a null-terminated string from data at offset, with the options
    given
    """
    end = data.find(b'\0' * charWidth, offset)
    return data[offset:end].decode(encoding)


def listFind(L, *args):
    try:
        return L.index(*args)
    except ValueError:
        return -1


def noteName(value):
    note = value - 60
    letter = 'ccddeffggaab'[note % 12]
    sharp  = ' ♯ ♯  ♯ ♯ ♯ '[note % 12].strip()
    if note < -12:
        letter = letter.upper()
    accents = ''
    while note >= 0:
        accents += "'"
        note -= 12
    while note < -24:
        accents += '͵'
        note += 12
    return letter + sharp + accents


def isIterable(object):
    """
    Check whether an object is iterable or not.
    """
    # https://stackoverflow.com/a/1952481
    try:
        iter(object)
        return True
    except TypeError:
        return False


def shortBytesRepr(data, maxLen=None):
    """
    Like bytes.__repr__(), but will truncate large amounts of data.
    Will also take advantage of octal encoding to make the output more
    compact.
    """
    if maxLen is None:
        maxLen = 0x20

    dataTrunc = data[:maxLen]
    r = ["b'"]
    for i, b in enumerate(data):
        # We have to be careful to avoid shortening e.g. b'\x01\x31' into b'\11',
        # so we don't shorten if the following byte is an ASCII digit
        if b < 8 and (i == len(data) - 1 or data[i + 1] not in range(0x30, 0x3A)):
            r.append(f'\\{b}')
        else:
            r.append(repr(b.to_bytes(1, 'big'))[2:-1])
    r.append("'")

    final = ''.join(r)

    if len(data) > maxLen:
        return final + '...'
    else:
        return final


def shortColorsListRepr(colors):
    """
    Like shortBytesRepr(), but for lists of colors.
    """
    MAX_COLORS = 20
    colorsTrunc = colors[:MAX_COLORS]
    strColors = (f'({r},{g},{b},{a})' for r, g, b, a in colorsTrunc)
    ellipsis = ', ...' if len(colors) > MAX_COLORS else ''
    return f'[{", ".join(strColors)}{ellipsis}]'


def loadInfoBlock(data, off, expectedEntryLengths=None):
    """
    Read an info block.
    These are used extensively in NSBMD and NSBTX files.
    """

    # Read overall header
    count, infoBlockSize = struct.unpack_from('<xBH', data, off)
    off += 4

    # Read unk block header and get array pointer
    unkHeaderLen, unkLen, unkUnk04 = \
        struct.unpack_from('<HHI', data, off)
    off += 8
    assert unkHeaderLen == 8, f'(Info block load) Wrong unknown block header length ({unkHeaderLen})'
    assert unkLen == 12 + 4 * count, f'(Info block load) Wrong unknown block length ({unkLen}; count is {count})'
    assert unkUnk04 == 0x17F, f'(Info block load) Wrong unknown block unknown value 04 ({unkUnk04})'
    unkBlockOff = off
    off += 4 * count

    # Read entries block header and get array pointer
    eachEntryLen, entriesLen = \
        struct.unpack_from('<HH', data, off)
    if expectedEntryLengths is not None:
        assert eachEntryLen == expectedEntryLengths, \
            (f'(Info block load) Expected entry length ({expectedEntryLengths})'
             f' does not match actual entry length ({eachEntryLen})')
    assert entriesLen == 4 + count * eachEntryLen, \
        (f'(Info block load) Discrepancy between total entries length ({entriesLen}),'
         f' count ({count}), and entry length ({eachEntryLen})')
    off += 4
    entryOff = off
    off += eachEntryLen * count

    # Get names array pointer
    nameOff = off

    # Gather entries into a list
    entries = []
    for i in range(count):
        unk00, unk02 = struct.unpack_from('<HH', data, unkBlockOff)
        entry = data[entryOff : entryOff+eachEntryLen]
        name = data[nameOff : nameOff+16].rstrip(b'\0').decode('latin-1')

        entries.append((name, unk00, unk02, entry))

        unkBlockOff += 4
        entryOff += eachEntryLen
        nameOff += 16

    return entries


def saveInfoBlock(entries, entryLengths):
    """
    The inverse of loadInfoBlock().
    entryLengths is required, so the code can properly handle the case
    of a completely empty entries list.
    """
    data = bytearray()

    # Create the overall header
    # (overall size value will be inserted at the end)
    data.extend(struct.pack('<xBH', len(entries), 0))

    # Write the unk block
    data.extend(struct.pack('<HHI', 8, 12 + 4 * len(entries), 0x17F))
    for e in entries:
        data.extend(struct.pack('<HH', e[1], e[2]))

    # Write the entries block
    data.extend(struct.pack('<HH', entryLengths, 4 + len(entries) * entryLengths))
    for e in entries:
        if len(e[3]) != entryLengths:
            raise ValueError('One of the entries is not of length'
                f' {entryLengths} like it should be'
                f' (actual length is {len(e[3])})')
        data.extend(e[3])

    # Write the names block
    for e in entries:
        if e[0] is None:
            data.extend(b'\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0')
        else:
            data.extend(e[0].encode('latin-1').ljust(16, b'\0'))

    # Insert the overall size, now that we know what it is
    struct.pack_into('<H', data, 2, len(data))

    return bytes(data)


def unpackAlignmentFromPos(xPack, yPack):
    """
    Given x/y values with alignment information included, as in
    BNCL/BNCD/BNBL, return the actual x, y and alignment values.
    """
    align = 0

    x = xPack & 0xFFF
    align |= [
        Alignment.LEFT,
        Alignment.H_CENTER,
        Alignment.RIGHT,
        Alignment.LEFT, # 3 is treated the same as 0
    ][(xPack >> 12) & 3]

    y = yPack & 0xFFF
    align |= [
        Alignment.TOP,
        Alignment.V_CENTER,
        Alignment.BOTTOM,
        Alignment.TOP, # 3 is treated the same as 0
    ][(yPack >> 12) & 3]

    return x, y, align


def packAlignmentIntoPos(x, y, alignment):
    """
    Given x, y and alignment values, return packed x/y values with the
    alignment information embedded, as in BNCL/BNCD/BNBL.
    """
    xPack = x & 0xFFF
    yPack = y & 0xFFF

    if alignment & Alignment.H_CENTER:
        xPack |= 0x1000
    elif alignment & Alignment.RIGHT:
        xPack |= 0x2000

    if alignment & Alignment.V_CENTER:
        yPack |= 0x1000
    elif alignment & Alignment.BOTTOM:
        yPack |= 0x2000

    return xPack, yPack


def getTopLeftOfAlignedRect(x, y, width, height, alignment):
    """
    Given x/y/w/h and alignment for a rectangle, return the coordinate
    of its top-left corner as calculated for BNCL/BNCD/BNBL.
    """

    # These formulas are straight from NSMB, "+ 1"s and all

    if alignment & Alignment.H_CENTER:
        x -= (width + 1) // 2
    elif alignment & Alignment.RIGHT:
        x -= width

    if alignment & Alignment.V_CENTER:
        y -= (height + 1) // 2
    elif alignment & Alignment.BOTTOM:
        y -= height

    return x, y


def getAlignmentName(alignment):
    """
    Return a nice string name for the given alignment value.
    """

    xAlignStr = 'left'
    if alignment & Alignment.H_CENTER:
        xAlignStr = 'center'
    elif alignment & Alignment.RIGHT:
        xAlignStr = 'right'

    yAlignStr = 'top'
    if alignment & Alignment.V_CENTER:
        yAlignStr = 'center'
    elif alignment & Alignment.BOTTOM:
        yAlignStr = 'bottom'

    alignStr = f'{yAlignStr}-{xAlignStr}'

    # Special case: "center-center" -> "center"
    if alignStr == 'center-center':
        alignStr = 'center'

    return alignStr


def enumeratedListOfStrs(items, indent=4):
    """
    Return a list of strings, where each string is indented by the
    specified amount. Each string shows an item's index and its string
    representation (__str__).
    """
    lines = []
    indentStr = ' ' * indent
    maxNumLen = len(str(len(items) - 1))
    for i, item in enumerate(items):
        lines.append(indentStr + f'[{i:{maxNumLen}}] {item}')
    return lines


def ensurePIL():
    """
    Display a nice error if PIL (Pillow) is not installed
    """
    if not HavePIL:
        raise RuntimeError('PIL (Pillow) is not installed, so ndspy cannot render image data as PIL images. Run "pip install Pillow" to install it.')


def colorsToImage(colors, width, height, *, aBits=1):
    """
    Render the given list of color values as a PIL Image.
    colors should be a list of (r5, g5, b5, aN) quadruples, where
    aN is of length aBits (usually 1 or 5).
    """
    ensurePIL()

    if aBits not in [1, 5]:
        raise ValueError(f'colorsToImage(): Unsupported value for aBits ({aBits})')

    # Avoiding using color.expand() here because minimizing Python function calls in
    # image-rendering functions is a very good idea for performance

    pxiter = iter(colors)
    dest = [0] * (width * height)
    for y in range(height):
        for x in range(width):
            r31, g31, b31, a = next(pxiter)
            r255 = r31 << 3 | r31 >> 2
            g255 = g31 << 3 | g31 >> 2
            b255 = b31 << 3 | b31 >> 2
            if aBits == 1:
                a255 = 255 if a else 0
            elif aBits == 5:
                a255 = a << 3 | a >> 2
            rgba = (a255 << 24) | (b255 << 16) | (g255 << 8) | r255
            dest[y * width + x] = rgba

    img = PIL.Image.frombytes('RGBA', (width, height), struct.pack(f'<{width * height}I', *dest))

    return img
