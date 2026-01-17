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

# Support for DS color values.

# On the NDS, colors are stored as 16-bit values, with 5 bits for each of
# R, G and B, and 1 bit for A. In some specific contexts, an additional
# 4 bits of alpha channel are available from somewhere else.

# ndspy's default/canonical format is officially an int in range 0000-FFFF.
# The primary advantage of this format is that it makes it possible to
# quickly convert colors to other formats using lookup table lists.

# ndspy also uses several other color formats in various places, as
# appropriate. You can convert colors between formats using the
# convert() function.

# If you want to decode a large number of colors (such as a palette or
# a direct-color image), and performance is a concern, you can use the
# provided LUT_*** constants after calling prepareLUTs() to initialize
# them. There are no LUTs provided for *en*coding because they would
# take up several GB of your RAM.

########
# Further API improvement ideas:
# - Add separate classes (namedtuples? dataclasses that support [0-3] indexing?)
#   for the different tuples, allowing convert() to autodetect the input format.
#   Make a convert(x, to_) overload style that requires that x be an autodetectable type.
# - Change the enum members from auto()s to strings, and allow strings to be
#   used in their place (like with PIL image formats)
# - Add a generic exception handler to convert() that does post-mortem
#   input verification, so that error messages will be less cryptic. Make
#   it clear in the documentation that this feature is only to aid in
#   debugging, and is not to be relied upon in general (since it will,
#   by design, not capture every invalid input)
########


import collections
import enum
import struct

from . import _common


class ColorFormat(enum.Enum):
    """
    Represents a possible format a color might be in. These are not all
    equivalent to each other!
    """
    INT_16 = enum.auto()
    BYTES_2 = enum.auto()
    TUPLE_RGB5A1 = enum.auto()
    TUPLE_RGB5A5 = enum.auto()
    TUPLE_RGBA255 = enum.auto()


ColorTuple = collections.namedtuple('ColorTuple', 'r g b a')


_lutsPrepared = False
def prepareLUTs():
    """
    Create and populate the lookup tables, if this hasn't been done yet.
    Calling this function multiple times is safe and has no real
    performance impact.
    """
    global _lutsPrepared
    global LUT_UNPACKED, LUT_UNPACKED_255
    global LUT_RGBA_255, LUT_ARGB_255, LUT_BGRA_255, LUT_ABGR_255

    if _lutsPrepared: return
    _lutsPrepared = True

    # Avoiding using the already-defined functions here because doing so
    # provides a significant speedup, and this code always runs upon startup
    # for any program that uses this module (directly or otherwise)
    LUT_UNPACKED = [None] * 0x10000
    LUT_UNPACKED_255 = [None] * 0x10000
    LUT_RGBA_255 = [None] * 0x10000
    LUT_ARGB_255 = [None] * 0x10000
    LUT_BGRA_255 = [None] * 0x10000
    LUT_ABGR_255 = [None] * 0x10000

    for i in range(0x10000):
        r = i & 0x1F
        g = (i >> 5) & 0x1F
        b = (i >> 10) & 0x1F
        a = (i >> 15) & 1
        LUT_UNPACKED[i] = ColorTuple(r, g, b, a)

        r255 = r << 3 | r >> 2
        g255 = g << 3 | g >> 2
        b255 = b << 3 | b >> 2
        a255 = 255 if a else 0
        LUT_UNPACKED_255[i] = ColorTuple(r255, g255, b255, a255)

        LUT_RGBA_255[i] = (r255 << 24) | (g255 << 16) | (b255 << 8) | a255
        LUT_ARGB_255[i] = (a255 << 24) | (r255 << 16) | (g255 << 8) | b255
        LUT_BGRA_255[i] = (b255 << 24) | (g255 << 16) | (r255 << 8) | a255
        LUT_ABGR_255[i] = (a255 << 24) | (b255 << 16) | (g255 << 8) | r255

        # Here's a clever (at least, in my opinion) trick that improves
        # memory usage by about 19%. The trade-off is that it also makes
        # this function about 54% slower, which is why it's not used by
        # default. It replaces the four "LUT_****_255[i] =" lines above.
        #
        # It works by having Python reuse int instances instead of
        # creating duplicate ones for the four different LUTs.
        #
        # (To use this, also put "INT_CACHE = {}" just before the loop
        # this comment is in.)

        # v = (r255 << 24) | (g255 << 16) | (b255 << 8) | a255
        # LUT_RGBA_255[i] = INT_CACHE.setdefault(v, v)
        # v = (a255 << 24) | (r255 << 16) | (g255 << 8) | b255
        # LUT_ARGB_255[i] = INT_CACHE.setdefault(v, v)
        # v = (b255 << 24) | (g255 << 16) | (r255 << 8) | a255
        # LUT_BGRA_255[i] = INT_CACHE.setdefault(v, v)
        # v = (a255 << 24) | (b255 << 16) | (g255 << 8) | r255
        # LUT_ABGR_255[i] = INT_CACHE.setdefault(v, v)


def convert(x, from_, to_):
    """
    Convert color x from format "from_" to format "to_"
    (both ColorFormat enum members), as accurately as possible.
    (In particular, if a conversion can be performed losslessly, it will be.)
    For speed, this function does NOT check for values out of bounds.
    Output in such cases is undefined.
    """
    CF = ColorFormat
    CF_INT_16 = CF.INT_16
    CF_BYTES_2 = CF.BYTES_2
    CF_TUPLE_RGB5A1 = CF.TUPLE_RGB5A1
    CF_TUPLE_RGB5A5 = CF.TUPLE_RGB5A5
    CF_TUPLE_RGBA255 = CF.TUPLE_RGBA255

    # If input is bytes, convert to int and proceed as if it was an int
    # input
    if from_ is CF_BYTES_2:
        x = x[1] << 8 | x[0]
        from_ = CF_INT_16

    if from_ is CF_INT_16:

        if to_ is CF_INT_16:
            return x

        elif to_ is CF_BYTES_2:
            return bytes([x & 0xFF, x >> 8])

        else:  # one of the tuple formats
            r =  x        & 0x1F
            g = (x >>  5) & 0x1F
            b = (x >> 10) & 0x1F
            a =  x >> 15

            if to_ is CF_TUPLE_RGB5A1:
                return ColorTuple(r, g, b, a)

            elif to_ is CF_TUPLE_RGB5A5:
                return ColorTuple(r, g, b, 0x1F if a else 0)

            else:  # CF_TUPLE_RGBA255
                r = r << 3 | r >> 2
                g = g << 3 | g >> 2
                b = b << 3 | b >> 2
                return ColorTuple(r, g, b, 255 if a else 0)

    elif from_ is CF_TUPLE_RGB5A1:

        if to_ is CF_TUPLE_RGB5A1:
            return ColorTuple(*x)

        elif to_ is CF_TUPLE_RGB5A5:
            return ColorTuple(x[0], x[1], x[2], 0x1F if x[3] else 0)

        elif to_ is CF_TUPLE_RGBA255:
            return ColorTuple(x[0] << 3 | x[0] >> 2,
                              x[1] << 3 | x[1] >> 2,
                              x[2] << 3 | x[2] >> 2,
                              255 if x[3] else 0)

        else:  # CF_INT_16 or CF_BYTES_2
            v = (   (x[0] & 0x1F)
                 | ((x[1] & 0x1F) << 5)
                 | ((x[2] & 0x1F) << 10)
                 | ( x[3]         << 15))

            # (v will be returned as int or bytes from after this giant
            # if statement)

    elif from_ is CF_TUPLE_RGB5A5:

        if to_ is CF_TUPLE_RGB5A5:
            return ColorTuple(*x)

        elif to_ is CF_TUPLE_RGB5A1:
            return ColorTuple(x[0], x[1], x[2], 1 if x[3] >= 0x10 else 0)

        elif to_ is CF_TUPLE_RGBA255:
            return ColorTuple(x[0] << 3 | x[0] >> 2,
                              x[1] << 3 | x[1] >> 2,
                              x[2] << 3 | x[2] >> 2,
                              x[3] << 3 | x[3] >> 2)

        else:  # CF_INT_16 or CF_BYTES_2
            v = (   (x[0] & 0x1F)
                 | ((x[1] & 0x1F) << 5)
                 | ((x[2] & 0x1F) << 10)
                 | ((1 if x[3] >= 0x10 else 0) << 15))

            # (v will be returned as int or bytes from after this giant
            # if statement)

    else:  # CF_TUPLE_RGBA255

        if to_ is CF_TUPLE_RGBA255:
            return ColorTuple(*x)

        elif to_ is CF_TUPLE_RGB5A1:
            return ColorTuple(((x[0] + 4) << 2) // 33,
                              ((x[1] + 4) << 2) // 33,
                              ((x[2] + 4) << 2) // 33,
                              1 if x[3] >= 0x80 else 0)

        elif to_ is CF_TUPLE_RGB5A5:
            return ColorTuple(((x[0] + 4) << 2) // 33,
                              ((x[1] + 4) << 2) // 33,
                              ((x[2] + 4) << 2) // 33,
                              ((x[3] + 4) << 2) // 33)

        else:  # CF_INT_16 or CF_BYTES_2
            v = (   ((((x[0] + 4) << 2) // 33) & 0x1F)
                 | (((((x[1] + 4) << 2) // 33) & 0x1F) << 5)
                 | (((((x[2] + 4) << 2) // 33) & 0x1F) << 10)
                 | ((1 if x[3] >= 0x80 else 0) << 15))

            # (v will be returned as int or bytes from after this giant
            # if statement)

    # If execution made it this far, we're converting something to an
    # int or bytes, and the "v" variable is available with the int value
    if to_ is CF_INT_16:
        return v
    else:  # CF_BYTES_2
        return bytes([v & 0xFF, v >> 8])


# MOST OF THE FUNCTIONS FOLLOWING THIS LINE ARE MORE-OR-LESS DEPRECATED
# unless I change my mind about this API change -----------------------


def unpack(v):
    """
    Unpack the color value as a quadruple (r5, g5, b5, a1).
    """
    return ColorTuple( v        & 0x1F,
                      (v >>  5) & 0x1F,
                      (v >> 10) & 0x1F,
                      (v >> 15) &    1)


def pack(r, g, b, a=1):
    """
    Pack the (r5, g5, b5, a1) values into a color value.
    """
    return (   (r & 0x1F)
            | ((g & 0x1F) << 5)
            | ((b & 0x1F) << 10)
            | ((a & 1) << 15))


def unpack255(v):
    """
    Unpack the color as an approximate quadruple (r8, g8, b8, a8).
    Equivalent to expand(unpack(color)).
    """
    r, g, b, a = unpack(v)
    r = r << 3 | r >> 2
    g = g << 3 | g >> 2
    b = b << 3 | b >> 2
    return ColorTuple(r, g, b, 255 if a else 0)


def pack255(r, g, b, a=255):
    """
    Pack the (r8, g8, b8, a8) values into an approximate color value.
    Equivalent to pack(contract(r, g, b[, a])).
    """
    return pack(((r + 4) << 2) // 33,
                ((g + 4) << 2) // 33,
                ((b + 4) << 2) // 33,
                0 if a < 128 else 1)


def expand(r, g, b, a=1):
    """
    Convert the given (r5, g5, b5, a1) values to an approximate (r8, g8, b8, a8) quadruple.
    """
    r = r << 3 | r >> 2
    g = g << 3 | g >> 2
    b = b << 3 | b >> 2
    return ColorTuple(r, g, b, 255 if a else 0)


def contract(r, g, b, a=255):
    """
    Convert the given (r8, g8, b8, a8) values to an approximate (r5, g5, b5, a1) quadruple.
    """
    return ColorTuple(((r + 4) << 2) // 33,
                      ((g + 4) << 2) // 33,
                      ((b + 4) << 2) // 33,
                      0 if a < 128 else 1)


def load(data):
    """
    Convert two bytes of data representing a color value to a (r5, g5, b5, a1) quadruple.
    """
    return unpack(data[1] << 8 | data[0])


def save(r, g, b, a=1):
    """
    Convert the given (r5, g5, b5, a1) values to two bytes of data representing a color value.
    """
    v = pack(r, g, b, a)
    return bytes([v & 0xFF, v >> 8])


def loadPalette(data):
    """
    Convert binary data to a list of (r5, g5, b5, a1) quadruples.
    This is the inverse of savePalette().
    """
    return [unpack(c) for c in struct.unpack_from(f'<{len(data) // 2}H', data)]


def loadPaletteFromFile(filePath):
    """
    Load a palette from a filesystem file.
    This is the inverse of savePaletteToFile().
    """
    with open(filePath, 'rb') as f:
        return loadPalette(f.read())


def savePalette(colors):
    """
    Convert a list of (r5, g5, b5, a1) quadruples to binary data.
    This is the inverse of loadPalette().
    """
    return struct.pack(f'<{len(colors)}H', *(pack(*c) for c in colors))


def savePaletteToFile(colors, filePath):
    """
    Convert a list of (r5, g5, b5, a1) quadruples to binary data, and save
    it to a filesystem file.
    This is the inverse of loadPaletteFromFile().
    """
    d = savePalette(colors)
    with open(filePath, 'wb') as f:
        f.write(d)
