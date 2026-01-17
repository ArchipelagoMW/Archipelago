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
Support for LZ10 compression.
"""

from __future__ import annotations

import argparse
import os
import pathlib
import struct
from typing import Sequence

from . import _lzCommon


def decompress(data: bytes) -> bytes:
    """
    Decompress LZ10-compressed data.
    """

    # NOTE:
    # This code is ported from NSMBe, which was converted from Elitemap.

    if data[0] != 0x10:
        raise TypeError("This isn't a LZ10-compressed file.")

    dataLen = struct.unpack_from('<I', data)[0] >> 8

    out = bytearray(dataLen)
    inPos, outPos = 4, 0

    while dataLen > 0:
        d = data[inPos]; inPos += 1

        if d:
            for i in range(8):
                if d & 0x80:
                    thing, = struct.unpack_from('>H', data, inPos); inPos += 2

                    length = (thing >> 12) + 3
                    offset = thing & 0xFFF
                    windowOffset = outPos - offset - 1

                    for j in range(length):
                        out[outPos] = out[windowOffset]
                        outPos += 1; windowOffset += 1; dataLen -= 1

                        if dataLen == 0:
                            return bytes(out)

                else:
                    out[outPos] = data[inPos]
                    outPos += 1; inPos += 1; dataLen -= 1

                    if dataLen == 0:
                        return bytes(out)

                d <<= 1
        else:
            for i in range(8):
                out[outPos] = data[inPos]
                outPos += 1; inPos += 1; dataLen -= 1

                if dataLen == 0:
                    return bytes(out)

    return bytes(out)


def decompressFromFile(filePath: str | os.PathLike) -> bytes:
    """
    Load a LZ10-compressed filesystem file, and decompress it.
    """
    with open(filePath, 'rb') as f:
        return decompress(f.read())


def decompressToFile(data: bytes, filePath: str | os.PathLike) -> None:
    """
    Decompress LZ10-compressed data, and save it to a filesystem file.
    """
    d = decompress(data)
    with open(filePath, 'wb') as f:
        f.write(d)


def compress(data: bytes) -> bytes:
    """
    Compress data in LZ10 format.
    """

    # NOTE:
    # This code is ported from NSMBe.

    compressed, _, _ = _lzCommon.compress(data, 1, 0x1000, 18, True, False)
    compressed = bytearray(compressed)
    compressed[:0] = struct.pack('<I', (len(data) << 8) | 0x10)
    return bytes(compressed)


def compressFromFile(filePath: str | os.PathLike) -> bytes:
    """
    Load a filesystem file, and compress its data in LZ10 format.
    """
    with open(filePath, 'rb') as f:
        return compress(f.read())


def compressToFile(data: bytes, filePath: str | os.PathLike) -> None:
    """
    Compress data in LZ10 format, and save it to a filesystem file.
    """
    d = compress(data)
    with open(filePath, 'wb') as f:
        f.write(d)


def main(args: Sequence[str] | None = None) -> None:
    """
    Main function for the CLI
    """
    parser = argparse.ArgumentParser(
        description='ndspy.lz10 CLI: Compress or decompress files using LZ10.')
    subparsers = parser.add_subparsers(title='commands',
        description='(run a command with -h for additional help)')

    def handleCompress(pArgs):
        """
        Handle the "compress" command.
        """
        with open(str(pArgs.input_file), 'rb') as f:
            data = f.read()

        outfp = pArgs.output_file
        if outfp is None: outfp = pArgs.input_file.with_suffix('.cmp')

        compressToFile(data, outfp)

    parser_compress = subparsers.add_parser('compress', aliases=['c'],
                                            help='compress a file')
    parser_compress.add_argument('input_file', type=pathlib.Path,
        help='input file to compress')
    parser_compress.add_argument('output_file', nargs='?', type=pathlib.Path,
        help='what to save the compressed file as')
    parser_compress.set_defaults(func=handleCompress)

    def handleDecompress(pArgs):
        """
        Handle the "decompress" command.
        """
        data = decompressFromFile(pArgs.input_file)

        outfp = pArgs.output_file
        if outfp is None: outfp = pArgs.input_file.with_suffix('.dec')

        with open(str(outfp), 'wb') as f:
            f.write(data)

    parser_decompress = subparsers.add_parser('decompress', aliases=['d'],
                                              help='decompress a file')
    parser_decompress.add_argument('input_file', type=pathlib.Path,
        help='input file to decompress')
    parser_decompress.add_argument('output_file', nargs='?', type=pathlib.Path,
        help='what to save the decompressed file as')
    parser_decompress.set_defaults(func=handleDecompress)

    # Parse args and run appropriate function
    pArgs = parser.parse_args(args)
    if hasattr(pArgs, 'func'):
        pArgs.func(pArgs)
    else:  # this happens if no arguments were specified at all
        parser.print_usage()


if __name__ == '__main__':
    main()
