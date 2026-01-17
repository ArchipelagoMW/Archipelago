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


class ImageFormat(enum.Enum):
    """
    Image formats
    """
    I8 = 0
    I4 = 1
    # A1BGR5 also exists, but probably not for tiles... need to look into that
    # further and decide how to support non-tiled graphics layers in general
    # (like ENPG)


class TilemapFormat(enum.Enum):
    """
    Tilemap formats
    """
    I10H1V1P4 = 0 # 10-bit index, 1 h-flip, 1 v-flip, 4 palette ID
    I8 = 1        # 8-bit index


def _checkImageFormat(value):
    """
    Raise a ValueError if the image format is invalid
    """
    if not isinstance(value, ImageFormat):
        raise ValueError(f'Image format should be an ImageFormat,'
                         f' not {value}!')


def _checkTilemapFormat(value):
    """
    Raise a ValueError if the tilemap format is invalid
    """
    if not isinstance(value, TilemapFormat):
        raise ValueError(f'Tilemap format should be a TilemapFormat,'
                         f' not {value}!')


class ImageTile:
    """
    A class that represents a single image tile.
    """
    pixels = None
    format = ImageFormat.I8

    def __init__(self, data=None, format=ImageFormat.I8):
        """
        data should be bytes or bytearray
        """
        _checkImageFormat(format)

        if data is None:
            self.pixels = [0] * 64

        else:
            if format == ImageFormat.I4:
                if len(data) != 32:
                    raise ValueError(f'I4 ImageTile data should be 32'
                                     f' bytes long, but is actually'
                                     f' {len(data)} bytes long')

                self.pixels = []
                for byte in data:
                    self.pixels.append(byte & 0xF)
                    self.pixels.append(byte >> 4)

            else:
                if len(data) != 64:
                    raise ValueError(f'I8 ImageTile data should be 64'
                                     f' bytes long, but is actually'
                                     f' {len(data)} bytes long')

                self.pixels = list(data)

        self.format = format


    @classmethod
    def fromPixels(cls, pixels, format=ImageFormat.I8):
        self = cls(None, format)
        self.pixels = pixels
        return self


    def render(self, colors, paletteNum=0):
        """
        Given a list of colors and the desired palette number to use, 
        render this ImageTile as a list of (r5, g5, b5, a1) quadruples.
        colors should be a list of (r5, g5, b5, a1) quadruples.
        """
        _checkImageFormat(self.format)

        # Force alpha on, because the hardware ignores the alpha channel in this instance
        # and considers all colors as opaque other than color 0 (which is considered
        # transparent no matter what)
        colors2 = [(r, g, b, 1) for (r, g, b, a) in colors]

        out = []

        paletteSize = 16 if (self.format == ImageFormat.I4) else 256
        cs = paletteNum * paletteSize
        for y in range(8):
            for x in range(8):
                px = self.pixels[y * 8 + x]
                # "0" is always transparent
                if px:
                    out.append(colors2[cs + px])
                else:
                    out.append((0, 0, 0, 0))

        return out


    def renderAsImage(self, colors, paletteNum=0):
        """
        Given a list of colors and the desired palette number to use, 
        render this ImageTile as a PIL Image.
        colors should be a list of (r5, g5, b5, a1) quadruples.
        """
        return _common.colorsToImage(self.render(colors, paletteNum), 8, 8, aBits=1)


    def save(self):
        _checkImageFormat(self.format)

        if self.format == ImageFormat.I4:
            data = bytearray()

            left = None
            for px in self.pixels:
                if left is None:
                    left = px & 0xF
                    continue

                value = left | ((px << 4) & 0xF0)
                left = None
                data.append(value)

            return bytes(data)

        else:
            return bytes(self.pixels)


def loadImageTiles(data, format=ImageFormat.I8):
    """
    Convert binary data to a list of ImageTiles.
    This is the inverse of saveImageTiles().
    """
    _checkImageFormat(format)

    bytesPerTile = 32 if (format == ImageFormat.I4) else 64
    tileCount = len(data) // bytesPerTile

    tiles = []
    for i in range(tileCount):
        start = i * bytesPerTile
        tiles.append(ImageTile(data[start : start+bytesPerTile], format))

    return tiles


def loadImageTilesFromFile(filePath, format=ImageFormat.I8):
    """
    Load a list of ImageTiles from a filesystem file.
    This is the inverse of saveImageTilesToFile().
    """
    with open(filePath, 'rb') as f:
        return loadImageTiles(f.read(), format)


def saveImageTiles(tiles):
    """
    Convert a list of ImageTiles to binary data.
    This is the inverse of loadImageTiles().
    """
    if tiles:
        # Quick sanity check
        format = tiles[0].format
        if not all(t.format == format for t in tiles):
            raise ValueError('saveImageTiles(): Inconsistent image formats')

        return b''.join(t.save() for t in tiles)

    else:
        return b''


def saveImageTilesToFile(tiles, filePath):
    """
    Convert a list of ImageTiles to binary data, and save it to a
    filesystem file.
    This is the inverse of loadImageTilesFromFile().
    """
    d = saveImageTiles(tiles)
    with open(filePath, 'wb') as f:
        f.write(d)


class TilemapTile:
    """
    A class representing a single tilemap tile
    """
    format = TilemapFormat.I10H1V1P4
    tileNum = 0
    hFlip = False
    vFlip = False
    paletteNum = 0

    def __init__(self, value=0, format=TilemapFormat.I10H1V1P4):
        """
        Initialize the TilemapTile from a raw 16-bit data value.
        """
        _checkTilemapFormat(format)
        self.value = value
        self.format = format


    @classmethod
    def fromParameters(cls, tileNum, format=TilemapFormat.I10H1V1P4, hFlip=False, vFlip=False, paletteNum=0):
        """
        Create a new TilemapTile with the parameters given.
        """
        self = cls()
        self.tileNum = tileNum
        self.format = format
        self.hFlip = hFlip
        self.vFlip = vFlip
        self.paletteNum = paletteNum
        return self


    @property
    def value(self):
        """
        This tile's 8-bit or 16-bit data value.
        """
        if self.format == TilemapFormat.I8:
            return self.tileNum & 0xFF
        else:
            v = 0
            v |= self.tileNum & 0x3FF
            if self.hFlip: v |= 0x400
            if self.vFlip: v |= 0x800
            v |= (self.paletteNum & 0xF) << 12
            return v

    @value.setter
    def value(self, v):
        if self.format == TilemapFormat.I8:
            self.tileNum = v & 0xFF
        else:
            self.tileNum = v & 0x3FF
            self.hFlip = bool(v & 0x400)
            self.vFlip = bool(v & 0x800)
            self.paletteNum = (v >> 12) & 0xF


    def renderSingle(self, imageTile, colors):
        """
        Given an image tile and a list of colors, render this
        TilemapTile as a list of (r5, g5, b5, a1) quadruples.
        imageTile should be an ImageTile.
        colors should be a list of (r5, g5, b5, a1) quadruples.
        """
        pixels = imageTile.render(colors, 0 if self.format == TilemapFormat.I8 else self.paletteNum)

        if self.format == TilemapFormat.I10H1V1P4: # I8 doesn't support flipping
            if self.hFlip and self.vFlip:
                # Calculate row offset (inverted), add x offset (inverted)
                pixels = [pixels[(56 - (i - i % 8)) + (7 - (i % 8))] for i in range(64)]
            elif self.hFlip:
                # Calculate row offset, add x offset (inverted)
                pixels = [pixels[      (i - i % 8)  + (7 - (i % 8))] for i in range(64)]
            elif self.vFlip:
                # Calculate row offset (inverted), add x offset
                pixels = [pixels[(56 - (i - i % 8)) +      (i % 8) ] for i in range(64)]

        return pixels


    def renderSingleAsImage(self, imageTile, colors):
        """
        Given an image tile and a list of colors, render this
        TilemapTile as a PIL Image.
        imageTile should be an ImageTile.
        colors should be a list of (r5, g5, b5, a1) quadruples.
        """
        return _common.colorsToImage(self.renderSingle(imageTile, colors), 8, 8, aBits=1)


    def render(self, imageTiles, colors, tileNumOffset=0):
        """
        Given lists of image tiles and colors, render this TilemapTile
        as a list of (r5, g5, b5, a1) quadruples.
        imageTiles should be a list of, well, ImageTiles.
        colors should be a list of (r5, g5, b5, a1) quadruples.
        """
        if self.tileNum < tileNumOffset:
            raise ValueError(f'TilemapTile.tileNum < tileNumOffset ({self.tileNum} < {tileNumOffset})')
        return self.renderSingle(imageTiles[self.tileNum - tileNumOffset], colors)


    def renderAsImage(self, imageTiles, colors, tileNumOffset=0):
        """
        Given lists of image tiles and colors, render this TilemapTile
        as a PIL Image.
        imageTiles should be a list of, well, ImageTiles.
        colors should be a list of (r5, g5, b5, a1) quadruples.
        """
        if self.tileNum < tileNumOffset:
            raise ValueError(f'TilemapTile.tileNum < tileNumOffset ({self.tileNum} < {tileNumOffset})')
        return self.renderSingleAsImage(imageTiles[self.tileNum - tileNumOffset], colors)


def loadTilemapTiles(data, format=TilemapFormat.I10H1V1P4):
    """
    Convert binary data to a list of TilemapTiles.
    This is the inverse of saveTilemapTiles().
    """
    tiles = []

    if format == TilemapFormat.I10H1V1P4:
        for i in range(0, len(data), 2):
            t, = struct.unpack_from('<H', data, i)
            tiles.append(TilemapTile(t, format))
    else:
        for t in data:
            tiles.append(TilemapTile(t, format))

    return tiles


def loadTilemapTilesFromFile(filePath, format=TilemapFormat.I10H1V1P4):
    """
    Load a list of TilemapTiles from a filesystem file.
    This is the inverse of saveTilemapTilesToFile().
    """
    with open(filePath, 'rb') as f:
        return loadTilemapTiles(f.read(), format)


def saveTilemapTiles(tiles):
    """
    Convert a list of TilemapTiles to binary data.
    This is the inverse of loadTilemapTiles().
    """
    if tiles:
        # Quick sanity check
        format = tiles[0].format
        if not all(t.format == format for t in tiles):
            raise ValueError('saveTilemapTiles(): Inconsistent tilemap tile formats')
        
        if format == TilemapFormat.I10H1V1P4:
            return b''.join(struct.pack('<H', t.value) for t in tiles)
        else:
            return bytes(t.value for t in tiles)

    else:
        return b''


def saveTilemapTilesToFile(tiles, filePath):
    """
    Convert a list of TilemapTiles to binary data, and save it to a
    filesystem file.
    This is the inverse of loadTilemapTilesFromFile().
    """
    d = saveTilemapTiles(tiles)
    with open(filePath, 'wb') as f:
        f.write(d)


def renderImageTiles(tiles, colors, paletteNum=0, width=32):
    """
    Given a list of ImageTiles, a list of colors, and a desired palette
    ID to render with, render all the tiles as a list of (r5, g5, b5, a1)
    quadruples.
    The width of the image defaults to 32 tiles, but can be adjusted.
    """
    height, remainder = divmod(len(tiles), width)
    if remainder: height += 1

    img = [(0, 0, 0, 0)] * (width * height * 64)

    tileIter = iter(tiles)
    for y in range(height):
        for x in range(width):
            tilePixels = next(tileIter).render(colors, paletteNum)
            for y2 in range(8):
                base = ((y * 8 + y2) * width + x) * 8
                img[base : base + 8] = tilePixels[y2 * 8 : y2 * 8 + 8]

    return img


def renderImageTilesAsImage(tiles, colors, paletteNum=0, width=32):
    """
    Given a list of ImageTiles, a list of colors, and a desired palette
    ID to render with, render all the tiles as a single image.
    The width of the image defaults to 32 tiles, but can be adjusted.
    """
    height, remainder = divmod(len(tiles), width)
    if remainder: height += 1
    return _common.colorsToImage(
        renderImageTiles(tiles, colors, paletteNum, width),
        width * 8, height * 8, aBits=1)


def renderTilemapTiles(tilemapTiles, imageTiles, colors, width, tileNumOffset=0):
    """
    Given a list of TilemapTiles, a list of ImageTiles, and a list of
    colors, render the tilemap to a list of (r5, g5, b5, a1) quadruples.
    The tilemap's width must also be specified.
    """
    height, remainder = divmod(len(tilemapTiles), width)
    if remainder: height += 1

    img = [(0, 0, 0, 0)] * (width * height * 64)

    tilemapIter = iter(tilemapTiles)
    for y in range(height):
        for x in range(width):
            tilePixels = next(tilemapIter).render(imageTiles, colors, tileNumOffset)
            for y2 in range(8):
                base = ((y * 8 + y2) * width + x) * 8
                img[base : base + 8] = tilePixels[y2 * 8 : y2 * 8 + 8]

    return img


def renderTilemapTilesAsImage(tilemapTiles, imageTiles, colors, width, tileNumOffset=0):
    """
    Given a list of TilemapTiles, a list of ImageTiles, and a list of
    colors, render the tilemap to an image. The tilemap's width must
    also be specified.
    """
    height, remainder = divmod(len(tilemapTiles), width)
    if remainder: height += 1
    return _common.colorsToImage(
        renderTilemapTiles(tilemapTiles, imageTiles, colors, width, tileNumOffset),
        width * 8, height * 8, aBits=1)


def tileAt(tiles, x, y, *, width=32):
    """
    Convenience function: return the tile at (x, y) in the tile list
    given, assuming a row width of `w` (32 by default).
    This can be used with ImageTile.pixels as well (with width 8).
    TODO: maybe rename it somehow to indicate that? Maybe even move it
    into ndspy.__init__ (like the named-list things)?
    """
    if x >= width or y >= width: return None
    if x < 0 or y < 0: return None
    try:
        return tiles[y * width + x]
    except IndexError:
        return None


def putTile(tiles, x, y, t, *, width=32):
    """
    Convenience function: replace the tile at (x, y) in the tile list
    given with `t`, assuming a row width of `w` (32 by default).
    If (x, y) is not in the tile list, nothing happens.
    This can be used with ImageTile.pixels as well (with width 8).
    TODO: maybe rename it somehow to indicate that? Maybe even move it
    into ndspy.__init__ (like the named-list things)?
    Returns True if the tile was placed, False otherwise (i.e. OOB)
    """
    if x >= width or y >= width: return False
    if x < 0 or y < 0: return False
    try:
        tiles[y * width + x] = t
        return True
    except IndexError:
        return False
