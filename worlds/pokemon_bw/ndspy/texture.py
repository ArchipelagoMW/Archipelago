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

import enum
import struct

from . import _common
from . import color as ndspyColor


class TextureFormat(enum.IntEnum):
    """
    An enum describing the various texture formats (for 3D models) the
    Nintendo DS supports.
    """
    UNKNOWN_0 = 0
    A3I5 = 1
    I2 = 2
    I4 = 3
    I8 = 4
    TEXELED = 5
    A5I3 = 6
    A1BGR5 = 7


    def bitsPerPixel1(self):
        """
        Return the number of bits per pixel that this format requires in
        a texture's first data region.
        This is useful for calculating the expected amount of data some
        texture will have, given its width, height and format.
        """
        return {
            type(self).UNKNOWN_0: 0,
            type(self).A3I5: 8,
            type(self).I2: 2,
            type(self).I4: 4,
            type(self).I8: 8,
            type(self).TEXELED: 2,
            type(self).A5I3: 8,
            type(self).A1BGR5: 16,
            }[self]


    def bitsPerPixel2(self):
        """
        Return the number of bits per pixel that this format requires in
        a texture's second data region.
        This is useful for calculating the expected amount of data some
        texture will have, given its width, height and format.
        """
        # Only TEXELED uses the second data region, and it's 1bpp
        # there. 
        if self == type(self).TEXELED:
            return 1
        else:
            return 0


class TextureCoordinatesTransformationMode(enum.IntEnum):
    """
    An enum describing the four ways texture coordinates can be
    transformed.
    See https://problemkaputt.de/gbatek.htm#ds3dtexturecoordinates
    for more.
    """
    NONE = 0
    TEX_COORD = 1
    NORMAL = 2
    VERTEX = 3


class Texture:
    """
    A texture for a 3D model. May depend on a palette.
    """
    def __init__(self, unk00, unk02, params, unk04, data1, data2):
        self.unk00 = unk00
        self.unk02 = unk02

        self.repeatS = bool(params & 1)                 # TODO: figure out what this means
        self.repeatT = bool(params & 2)                 # TODO: figure out what this means
        self.mirrorS = bool(params & 4)                 # TODO: figure out what this means
        self.mirrorT = bool(params & 8)                 # TODO: figure out what this means
        self.width = 8 << ((params >> 4) & 7)
        self.height = 8 << ((params >> 7) & 7)
        self.format = TextureFormat((params >> 10) & 7)
        self.isColor0Transparent = bool(params & 0x2000)
        self.coordsTransformationMode = TextureCoordinatesTransformationMode(
            (params >> 14) & 3)

        self.unk04 = unk04
        self.data1 = data1
        self.data2 = data2


    @classmethod
    def fromFlags(cls, unk00, unk02, repeatS, repeatT, mirrorS, mirrorT,
            width, height, format, isColor0Transparent,
            coordsTransformationMode, unk04, data1, data2):
        self = cls(unk00, unk02, 0, unk04, data1, data2)
        self.repeatS = repeatS
        self.repeatT = repeatT
        self.mirrorS = mirrorS
        self.mirrorT = mirrorT
        self.width = width
        self.height = height
        self.format = format
        self.isColor0Transparent = isColor0Transparent
        self.coordsTransformationMode = coordsTransformationMode
        return self


    @property
    def size(self):
        return self.width, self.height
    @size.setter
    def size(self, value):
        self.width, self.height = value


    def save(self):
        params = 0

        if self.repeatS: params |= 1
        if self.repeatT: params |= 2
        if self.mirrorS: params |= 4
        if self.mirrorT: params |= 8

        SIZES_ENCODED = {
            8:    0,
            16:   1,
            32:   2,
            64:   3,
            128:  4,
            256:  5,
            512:  6,
            1024: 7,
        }

        if self.width not in SIZES_ENCODED:
            raise ValueError(f'Texture width (currently {self.width})'
                ' must be a power of 2 between 8 and 1024 inclusive!')
        if self.height not in SIZES_ENCODED:
            raise ValueError(f'Texture height (currently {self.height})'
                ' must be a power of 2 between 8 and 1024 inclusive!')

        params |= SIZES_ENCODED[self.width] << 4
        params |= SIZES_ENCODED[self.height] << 7

        params |= (self.format & 7) << 10
        if self.isColor0Transparent: params |= 0x2000
        params |= (self.coordsTransformationMode & 3) << 14

        return self.unk00, self.unk02, params, self.unk04, self.data1, self.data2


    def render(self, palette=None):
        """
        Given a palette, render this texture as a list of (r5, g5, b5, a5) quadruples.
        (Yes, a is 5 bits long.)
        palette should be a Palette.
        palette can be None if the texture is in a format that doesn't
        need a palette (A1BGR5).
        """
        colors = palette.colors if palette is not None else None
        return renderTextureData(self.data1,
                                 self.data2,
                                 self.format,
                                 self.width,
                                 self.height,
                                 colors,
                                 self.isColor0Transparent)


    def renderAsImage(self, palette=None):
        """
        Given a palette, render this texture as a PIL Image.
        palette should be a Palette.
        palette can be None if the texture is in a format that doesn't
        need a palette (A1BGR5).
        """
        colors = palette.colors if palette is not None else None
        return renderTextureDataAsImage(self.data1,
                                        self.data2,
                                        self.format,
                                        self.width,
                                        self.height,
                                        colors,
                                        self.isColor0Transparent)


    def __str__(self):
        format = {
            int(TextureFormat.UNKNOWN_0): 'unknown-0',
            int(TextureFormat.A3I5): 'a3i5',
            int(TextureFormat.I2): 'i2',
            int(TextureFormat.I4): 'i4',
            int(TextureFormat.I8): 'i8',
            int(TextureFormat.TEXELED): 'texeled',
            int(TextureFormat.A5I3): 'a5i3',
            int(TextureFormat.A1BGR5): 'a1bgr5',
            }.get(self.format, 'invalid')
        return f'<texture {format} {self.width}x{self.height}>'


    def __repr__(self):
        try:
            argsList = list(self.save())

            # Params
            argsList[2] = hex(argsList[2])

            # Datas 1 & 2
            argsList[4] = _common.shortBytesRepr(argsList[4])
            argsList[5] = _common.shortBytesRepr(argsList[5])

            args = ', '.join(str(x) for x in argsList)

        except Exception:
            args = '...'

        return f'{type(self).__name__}({args})'


class Palette:
    """
    A palette as used in 3D model textures.
    Contains a colors list as well as some other metadata.
    """
    def __init__(self, unk00, unk02, unkHeader02, data):
        self.unk00 = unk00
        self.unk02 = unk02
        self.unkHeader02 = unkHeader02
        self.colors = ndspyColor.loadPalette(data)


    def save(self):
        return self.unk00, self.unk02, self.unkHeader02, ndspyColor.savePalette(self.colors)


    @classmethod
    def fromColors(cls, unk00, unk02, unkHeader02, colors):
        self = cls(unk00, unk02, unkHeader02, b'')
        self.colors = colors
        return self


    def __str__(self):
        return f'<palette ({len(self.colors)} colors) {_common.shortColorsListRepr(self.colors)}>'


    def __repr__(self):
        return (f'{type(self).__name__}.fromColors('
            f'{self.unk00},'
            f' {self.unk02},'
            f' {self.unkHeader02},'
            f' {_common.shortColorsListRepr(self.colors)})')


class NSBTX:
    """
    Similar to NSBMD, but only contains textures and palettes (no 3D
    data).
    """
    def __init__(self, data=None):
        # TODO: find reasonable default values for these
        self.unk08 = 0
        self.unk10 = 0
        self.unk18 = 0
        self.unk20 = 0
        self.unk2C = 0
        self.unk32 = 0
        self.textures = []
        self.palettes = []

        if data is not None:
            self._initFromData(data)


    def _initFromData(self, data):
        """
        Load the NSBTX from file data.
        """
        if not data.startswith(b'BTX0'):
            raise ValueError('Invalid NSBTX: incorrect magic')

        magic, bom, version, filesize, headersize, numblocks = \
            _common.NDS_STD_FILE_HEADER.unpack_from(data, 0)
        if version != 1:
            raise ValueError(f'Unsupported NSBTX version: {version}')
        
        assert numblocks == 1, f'NSBTX has {numblocks} blocks'

        TEX0 = data[0x14:]
        assert TEX0.startswith(b'TEX0'), f'Incorrect NSBTX TEX0 magic ({TEX0[:4]})'

        parsed = _readTEX0(TEX0)
        self.unk08 = parsed['unk08']
        self.unk10 = parsed['unk10']
        self.unk18 = parsed['unk18']
        self.unk20 = parsed['unk20']
        self.unk2C = parsed['unk2C']
        self.unk32 = parsed['unk32']
        self.textures = parsed['textures']
        self.palettes = parsed['palettes']


    @classmethod
    def fromTexturesAndPalettes(cls, unk08, unk10, unk18, unk20, unk2C, unk32, textures, palettes):
        self = cls()
        self.unk08 = unk08
        self.unk10 = unk10
        self.unk18 = unk18
        self.unk20 = unk20
        self.unk2C = unk2C
        self.unk32 = unk32
        self.textures = textures
        self.palettes = palettes
        return self


    def save(self):
        """
        Save the NSBTX back to a file.
        """
        texInfo = {}
        texInfo['unk08'] = self.unk08
        texInfo['unk10'] = self.unk10
        texInfo['unk18'] = self.unk18
        texInfo['unk20'] = self.unk20
        texInfo['unk2C'] = self.unk2C
        texInfo['unk32'] = self.unk32
        texInfo['textures'] = self.textures
        texInfo['palettes'] = self.palettes
        TEX0 = _saveTEX0(texInfo)

        data = bytearray(0x14)
        data.extend(TEX0)

        # Add the NDS standard file header
        _common.NDS_STD_FILE_HEADER.pack_into(data, 0,
            b'BTX0', 0xFEFF, 1, len(data), 0x10, 1)

        # Insert the offset to the TEX0 block
        data[0x10] = 0x14

        # And return.
        return bytes(data)


def _readTEX0(data):
    """
    Read a TEX0 block.
    Return a bunch of data as a dict.
    """
    assert data.startswith(b'TEX0'), f'Incorrect TEX0 magic ({data[:4]})'

    returnVal = {}

    # TEX0 header
    (unk08, texDataLen, texOff,
            unk10, texDataOff, unk18, compressedData1Len, compressedInfoOff,
            unk20, compressedData1Off, compressedData2Off, unk2C,
            palDataLen, unk32, palOff, palDataOff) = \
        struct.unpack_from('<IHH3IHH4IHH2I', data, 0x8)
    returnVal['unk08'] = unk08
    returnVal['unk10'] = unk10
    returnVal['unk18'] = unk18
    returnVal['unk20'] = unk20
    returnVal['unk2C'] = unk2C
    returnVal['unk32'] = unk32

    texDataLen <<= 3
    palDataLen <<= 3
    compressedData1Len <<= 3
    compressedData2Len = compressedData1Len // 2

    # Textures
    returnVal['textures'] = []
    for name, unk00, unk02, texHeader in _common.loadInfoBlock(data, texOff, 8):
        thisTexOff, params, unk04 = struct.unpack('<HHI', texHeader)
        thisTexOff <<= 3

        tex = Texture(unk00, unk02, params, unk04, b'', b'')

        if tex.format == TextureFormat.TEXELED:
            thisTexOff1 = compressedData1Off + thisTexOff
            thisTexOff2 = compressedData2Off + thisTexOff // 2
            thisTexDataLen1 = int(tex.width * tex.height * tex.format.bitsPerPixel1() / 8)
            thisTexDataLen2 = int(tex.width * tex.height * tex.format.bitsPerPixel2() / 8)
            thisTexData1 = data[thisTexOff1 : thisTexOff1 + thisTexDataLen1]
            thisTexData2 = data[thisTexOff2 : thisTexOff2 + thisTexDataLen2]
        else:
            thisTexOff += texDataOff
            thisTexDataLen = int(tex.width * tex.height * tex.format.bitsPerPixel1() / 8)
            thisTexData1 = data[thisTexOff : thisTexOff+thisTexDataLen]
            thisTexData2 = b''

        tex.data1 = thisTexData1
        tex.data2 = thisTexData2

        returnVal['textures'].append((name, tex))

    # Palettes
    # This needs to be done in 2 passes because palettes don't have a
    # "data length" value: first we collect all the palette data start
    # positions (and metadata), then we sort the data start positions,
    # and then we make the actual Palette objects with the palette data.
    paletteStartOffsets = []
    palette2StartOffset = {}

    paletteTuples = []
    returnVal['palettes'] = []

    for name, unk00, unk02, palHeader in _common.loadInfoBlock(data, palOff, 4):
        thisPalOff, unkHeader02 = struct.unpack('<HH', palHeader)
        thisPalOff <<= 3
        thisPalOff += palDataOff

        pt = (name, unk00, unk02, unkHeader02)

        paletteStartOffsets.append(thisPalOff)
        palette2StartOffset[pt] = thisPalOff
        paletteTuples.append(pt)

    paletteStartOffsets.append(palDataOff + palDataLen)
    paletteStartOffsets.sort()

    for pt in paletteTuples:
        startOff = palette2StartOffset[pt]
        endOff = paletteStartOffsets[paletteStartOffsets.index(startOff) + 1]
        palData = data[startOff : endOff]

        name, unk00, unk02, unkHeader02 = pt
        pal = Palette(unk00, unk02, unkHeader02, palData)
        returnVal['palettes'].append((name, pal))

    return returnVal


def _saveTEX0(fields):
    """
    Given a dict containing TEX0 data (in the format returned by
    _loadTEX0), return a bytes object representing the TEX0 block.
    """

    data = bytearray(0x3C)
    texturesData = bytearray()
    compressedData1 = bytearray()
    compressedData2 = bytearray()
    palettesData = bytearray()

    # Textures header
    compressedInfoOff = len(data)
    texOff = len(data)
    
    entries = []
    for texName, tex in fields['textures']:
        unk00, unk02, params, unk04, data1, data2 = tex.save()

        if tex.format == TextureFormat.TEXELED:
            thisTexOff = len(compressedData1)
            if len(data1) != len(data2) * 2:
                raise ValueError(f'For texeled textures, data1 must'
                    ' be twice as long as data2!'
                    f' (Found lengths: {len(data1)}, {len(data2)})')
            compressedData1.extend(data1)
            compressedData2.extend(data2)
        else:
            thisTexOff = len(texturesData)
            texturesData.extend(data1)

        entryData = struct.pack('<HHI', thisTexOff >> 3, params, unk04)
        entries.append((texName, unk00, unk02, entryData))

    data.extend(_common.saveInfoBlock(entries, 8))

    # Palettes header
    palOff = len(data)
    
    entries = []
    for palName, pal in fields['palettes']:
        unk00, unk02, unkHeader02, thisPaletteData = pal.save()
        if len(thisPaletteData) % 8:
            # 4 colors = 8 bytes
            raise ValueError('Palette must be a multiple of 4 colors long')
        thisPalOff = len(palettesData)
        palettesData.extend(thisPaletteData)

        entryData = struct.pack('<HH', thisPalOff >> 3, unkHeader02)
        entries.append((palName, unk00, unk02, entryData))

    data.extend(_common.saveInfoBlock(entries, 4))

    # Data bytearrays
    texDataOff = len(data)
    data.extend(texturesData)
    compressedData1Off = len(data)
    data.extend(compressedData1)
    compressedData2Off = len(data)
    data.extend(compressedData2)
    palDataOff = len(data)
    data.extend(palettesData)

    # TEX0 header
    struct.pack_into('<4sIIHH3IHH4IHH2I', data, 0,
        b'TEX0', len(data), fields['unk08'], len(texturesData) >> 3, texOff,
        fields['unk10'], texDataOff, fields['unk18'], len(compressedData1) >> 3, compressedInfoOff,
        fields['unk20'], compressedData1Off, compressedData2Off, fields['unk2C'],
        len(palettesData) >> 3, fields['unk32'], palOff, palDataOff)

    return bytes(data)


def renderTextureDataAsImage(data1, data2, format, width, height, palette=None, isColor0Transparent=True):
    """
    Render the given texture data as a PIL Image.
    format should be a TextureFormat.
    palette should be a list of colors (or None, if the texture format
    doesn't require one).
    """
    return _common.colorsToImage(
        renderTextureData(data1, data2, format, width, height, palette, isColor0Transparent),
        width, height, aBits=5)


def renderTextureData(data1, data2, format, width, height, palette=None, isColor0Transparent=True):
    """
    Render the given texture data as a list of (r5, g5, b5, a5) quadruples.
    (Yes, a is 5 bits long.)
    format should be a TextureFormat.
    palette should be a list of colors (or None, if the texture format
    doesn't require one).
    """
    if format == TextureFormat.A3I5:
        return _renderA3I5(data1, width, height, palette)
    elif format == TextureFormat.I2:
        return _renderI2(data1, width, height, palette, isColor0Transparent)
    elif format == TextureFormat.I4:
        return _renderI4(data1, width, height, palette, isColor0Transparent)
    elif format == TextureFormat.I8:
        return _renderI8(data1, width, height, palette, isColor0Transparent)
    elif format == TextureFormat.TEXELED:
        return _renderTexeled(data1, data2, width, height, palette, isColor0Transparent)
    elif format == TextureFormat.A5I3:
        return _renderA5I3(data1, width, height, palette)
    elif format == TextureFormat.A1BGR5:
        return _renderA1BGR5(data1, width, height)
    else:
        raise ValueError(f'Cannot render texture format: {format}')


def _renderA3I5(data, w, h, colors):
    """
    Render this texture using the A3I5 format.
    """
    COLOR_LUT = ndspyColor.LUT_UNPACKED

    pxiter = iter(data)
    dest = [0] * (w * h)
    for y in range(h):
        for x in range(w):
            value = next(pxiter)
            color = colors[value & 0x1F]

            r, g, b, _ = COLOR_LUT[color]
            a = value >> 5
            a = (a << 2) | (a >> 1)

            dest[y * w + x] = (r, g, b, a)

    return dest


def _renderI2(data, w, h, colors, isColor0Transparent):
    """
    Render this texture using the I2 format.
    """
    COLOR_LUT = ndspyColor.LUT_UNPACKED
    alpha0 = 0 if isColor0Transparent else 31

    pxiter = iter(data)
    dest = [0] * (w * h)
    for y in range(h):
        for x in range(0, w, 4):
            value = next(pxiter)

            value1 = value & 3
            color = colors[value1]
            r, g, b, _ = COLOR_LUT[color]
            a = 31 if value1 != 0 else alpha0
            dest[y * w + x] = (r, g, b, a)

            value2 = (value >> 2) & 3
            color = colors[value2]
            r, g, b, _ = COLOR_LUT[color]
            a = 31 if value2 != 0 else alpha0
            dest[y * w + x + 1] = (r, g, b, a)

            value3 = (value >> 4) & 3
            color = colors[value3]
            r, g, b, _ = COLOR_LUT[color]
            a = 31 if value3 != 0 else alpha0
            dest[y * w + x + 2] = (r, g, b, a)

            value3 = value >> 6
            color = colors[value3]
            r, g, b, _ = COLOR_LUT[color]
            a = 31 if value3 != 0 else alpha0
            dest[y * w + x + 3] = (r, g, b, a)

    return dest


def _renderI4(data, w, h, colors, isColor0Transparent):
    """
    Render this texture using the I4 format.
    """
    COLOR_LUT = ndspyColor.LUT_UNPACKED
    alpha0 = 0 if isColor0Transparent else 31

    pxiter = iter(data)
    dest = [0] * (w * h)
    for y in range(h):
        for x in range(0, w, 2):
            value = next(pxiter)

            value1 = value & 0xF
            color = colors[value1]
            r, g, b, _ = COLOR_LUT[color]
            a = 31 if value1 != 0 else alpha0
            dest[y * w + x] = (r, g, b, a)

            value2 = value >> 4
            color = colors[value2]
            r, g, b, _ = COLOR_LUT[color]
            a = 31 if value2 != 0 else alpha0
            dest[y * w + x + 1] = (r, g, b, a)

    return dest


def _renderI8(data, w, h, colors, isColor0Transparent):
    """
    Render this texture using the I8 format.
    """
    COLOR_LUT = ndspyColor.LUT_UNPACKED
    alpha0 = 0 if isColor0Transparent else 31

    pxiter = iter(data)
    dest = [0] * (w * h)
    for y in range(h):
        for x in range(w):
            value = data[y * w + x]
            color = colors[value]
            r, g, b, _ = COLOR_LUT[color]
            a = 31 if value != 0 else alpha0
            dest[y * w + x] = (r, g, b, a)

    return dest


def _renderTexeled(data1, data2, w, h, colors, isColor0Transparent):
    """
    Render this texture using the Texeled format.
    """
    COLOR_LUT = ndspyColor.LUT_UNPACKED

    # This one sure is... fun :(

    pxiter1 = iter(data1)
    pxiter2 = iter(data2)
    dest = [0] * (w * h)
    for y in range(0, h, 4):
        for x in range(0, w, 4):
            value2 = next(pxiter2) | (next(pxiter2) << 8)
            paletteOffset = (value2 & 0x3FFF) * 2
            interpMode = value2 >> 14

            for suby in range(4):
                value1 = next(pxiter1)
                for subx in range(4):
                    subvalue = value1 & 3
                    value1 >>= 2

                    # The color-averaging code is based on code from
                    # melonDS, because I trust its accuracy in this area

                    alpha = 31

                    if subvalue < 2:
                        color = colors[paletteOffset + subvalue]

                    elif subvalue == 2:

                        if interpMode == 1:
                            # Texel value 2 interp mode 1:
                            # (color0 + color1) / 2

                            color0 = colors[paletteOffset]
                            color1 = colors[paletteOffset + 1]

                            r0 = color0 & 0x001F
                            g0 = color0 & 0x03E0
                            b0 = color0 & 0x7C00
                            r1 = color1 & 0x001F
                            g1 = color1 & 0x03E0
                            b1 = color1 & 0x7C00

                            r = (r0 + r1) >> 1
                            g = ((g0 + g1) >> 1) & 0x03E0
                            b = ((b0 + b1) >> 1) & 0x7C00

                            color = r | g | b

                        elif interpMode == 3:
                            # Texel value 2 interp mode 3:
                            # (color0 * 5 + color1 * 3) / 8

                            color0 = colors[paletteOffset]
                            color1 = colors[paletteOffset + 1]

                            r0 = color0 & 0x001F
                            g0 = color0 & 0x03E0
                            b0 = color0 & 0x7C00
                            r1 = color1 & 0x001F
                            g1 = color1 & 0x03E0
                            b1 = color1 & 0x7C00

                            r = (r0 * 5 + r1 * 3) >> 3
                            g = ((g0 * 5 + g1 * 3) >> 3) & 0x03E0
                            b = ((b0 * 5 + b1 * 3) >> 3) & 0x7C00

                            color = r | g | b

                        else:
                            color = colors[paletteOffset + 2]

                    elif subvalue == 3:

                        if interpMode < 2:
                            # (transparent)
                            color = alpha = 0

                        elif interpMode == 2:
                            color = colors[paletteOffset + 3]

                        else:
                            # Texel value 3 interp mode 3:
                            # (color0 * 3 + color1 * 5) / 8

                            color0 = colors[paletteOffset]
                            color1 = colors[paletteOffset + 1]

                            r0 = color0 & 0x001F
                            g0 = color0 & 0x03E0
                            b0 = color0 & 0x7C00
                            r1 = color1 & 0x001F
                            g1 = color1 & 0x03E0
                            b1 = color1 & 0x7C00

                            r = (r0 * 3 + r1 * 5) >> 3
                            g = ((g0 * 3 + g1 * 5) >> 3) & 0x03E0
                            b = ((b0 * 3 + b1 * 5) >> 3) & 0x7C00

                            color = r | g | b

                    if alpha == 31:
                        r, g, b, _ = COLOR_LUT[color]
                    else:
                        r = g = b = 0

                    dest[(y + suby) * w + x + subx] = (r, g, b, alpha)

    return dest


def _renderA5I3(data, w, h, colors):
    """
    Render this texture using the A5I3 format.
    """
    COLOR_LUT = ndspyColor.LUT_UNPACKED

    pxiter = iter(data)
    dest = [0] * (w * h)
    for y in range(h):
        for x in range(w):
            value = next(pxiter)
            color = colors[value & 0x7]
            r, g, b, _ = COLOR_LUT[color]
            a = value >> 3
            dest[y * w + x] = (r, g, b, a)

    return dest


def _renderA1BGR5(data, w, h):
    """
    Render this texture using the A1BGR5 format.
    """
    COLOR_LUT = ndspyColor.LUT_UNPACKED

    pxiter = iter(data)
    dest = [0] * (w * h)
    for y in range(h):
        for x in range(w):
            color = next(pxiter) | (next(pxiter) << 8)
            r, g, b, a1 = COLOR_LUT[color]
            a = 31 if a1 else 0
            dest[y * w + x] = (r, g, b, a)

    return dest
