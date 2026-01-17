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
Support for executable code files compression.
"""

from __future__ import annotations

import argparse
import os
import pathlib
import struct
from typing import Sequence

from . import _lzCommon


def _detectAppendedData(data: bytes) -> int | None:
    """
    Attempt to check if there's any appended data at the end of the
    given data. Returns an integer representing the amount of such data
    if so, or None if the data doesn't seem to be compressed.
    """
    for possibleAmt in range(0, 0x20, 4):
        try:
            headerLen = data[-5 - possibleAmt]
        except IndexError:
            return None

        compLenHeaderLen, extraSize = struct.unpack_from('<II', data, len(data) - possibleAmt - 8)
        headerLen = compLenHeaderLen >> 24
        compressedLen = compLenHeaderLen & 0xFFFFFF

        if headerLen < 8: continue
        if compressedLen > len(data): continue
        for byte in data[-possibleAmt - headerLen  : -possibleAmt - 8]:
            if byte != 0xFF:
                continue

        return possibleAmt

    return None


def decompress(data: bytes) -> bytes:
    """
    Decompress data that was compressed using code compression. This is
    the inverse of compress().
    """

    # NOTE:
    # This code is ported from DSDecmp:
    # http://www.romhacking.net/utilities/789/
    # https://github.com/Barubary/dsdecmp

    appendedDataAmount = _detectAppendedData(data)

    if appendedDataAmount is None:
        # Probably not compressed.
        return data

    if appendedDataAmount == 0:
        appendedData = b''
    else:
        appendedData = data[-appendedDataAmount:]
        data = data[:-appendedDataAmount]

    # If extraSize (the last value in the header) is 0, the data is not
    # actually compressed
    if data[-4:] == b'\0\0\0\0':
        return data

    # Read the header
    compLenHeaderLen, extraSize = struct.unpack_from('<II', data, len(data) - 8)
    headerLen = compLenHeaderLen >> 24
    compressedLen = compLenHeaderLen & 0xFFFFFF

    if len(data) < headerLen:
        raise ValueError(f'File is too small for header ({len(data)} < {headerLen})')

    if compressedLen > len(data):
        raise ValueError("Compressed length doesn't fit in the input file")

    # The rest of the header should be all 0xFF's
    for byte in data[-headerLen:-8]:
        if byte != 0xFF:
            raise ValueError("Header padding isn't entirely 0xFF")


    # Format description:
    #
    # Code LZ compression is basically just LZ-0x10 compression.
    # However, the order of reading is reversed: the compression starts
    # at the end of the file. Assuming we start reading at the end
    # towards the beginning, the format is:
    #
    # u32 extraSize            | decompressed data size = file length
    #                          | (including header) + this value
    # u8 headerLen             |
    # u24 compressedLen        | Can be less than file size (without
    #                          | header): if so, the rest of the file is
    #                          | uncompressed. It may also be the file
    #                          | size.
    # u8[headerSize-8] padding | 0xFF's
    # 
    # 0x10-like-compressed data follows (without the usual 4-byte
    # header). The only difference is that 2 should be added to the DISP
    # value in compressed blocks to get the proper value. The u32 and
    # u24 are read most significant byte first. If extraSize is 0, there
    # is no headerSize, decompressedLength or padding: the data starts
    # immediately, and is uncompressed.
    # 
    # arm9.bin has 3 extra u32 values at the 'start' (ie: end of the
    # file), which may be ignored (and are ignored here). These 12 bytes
    # also should not be included in the computation of the output size.

    # The compressed size is sometimes the file size
    if compressedLen >= len(data):
        compressedLen = len(data)

    # The first part of the file, not included in compressedLen, is not
    # compressed, and should be ignored.
    passthroughLen = len(data) - compressedLen
    passthroughData = data[:passthroughLen]

    # Then there's the compressed data. Also make a bytearray where
    # we'll be putting the decompressed data.
    compData = data[passthroughLen : passthroughLen + compressedLen - headerLen]
    decompData = bytearray(len(data) + extraSize - passthroughLen)

    # Main decompression loop
    currentOutSize = 0
    decompLen = len(decompData)
    readBytes = 0
    flags = 0
    mask = 1
    while currentOutSize < decompLen:

        # Update the mask. If all flag bits have been read, get a new
        # set.
        if mask == 1:
            if readBytes >= compressedLen:
                raise RuntimeError('Not enough data to decompress')

            flags = compData[-1 - readBytes]
            readBytes += 1

            mask = 0x80
        else:
            mask >>= 1

        # Bit = 1 means it's compressed
        if flags & mask:
            # Get length and displacement ("disp") values from the next 2 bytes
            if readBytes + 1 >= len(data):
                raise RuntimeError('Not enough data to decompress')

            byte1 = compData[-1 - readBytes]; readBytes += 1
            byte2 = compData[-1 - readBytes]; readBytes += 1

            # The number of bytes to copy
            length = (byte1 >> 4) + 3

            # Where the bytes should be copied from (relatively)
            disp = (((byte1 & 0x0F) << 8) | byte2) + 3

            if disp > currentOutSize:
                if currentOutSize < 2:
                    raise RuntimeError(
                        'Cannot go back more than already written; '
                        f'attempted to go back {hex(disp)} bytes when only '
                        f'{hex(currentOutSize)} bytes have been written')

                # HACK. This seems to produce valid files, but isn't the
                # most elegant solution. Although this *could* be the
                # actual way to use a disp of 2 in this format, as,
                # otherwise, the minimum would be 3 (and 0 is undefined,
                # and 1 is less useful).
                disp = 2

            bufIdx = currentOutSize - disp
            for i in range(length):
                next = decompData[-1 - bufIdx]
                bufIdx += 1

                decompData[-1 - currentOutSize] = next
                currentOutSize += 1

        else:
            if readBytes > len(data):
                raise RuntimeError('Not enough data to decompress')

            next = compData[-1 - readBytes]
            readBytes += 1

            decompData[-1 - currentOutSize] = next
            currentOutSize += 1

    return passthroughData + decompData + appendedData


def decompressFromFile(filePath: str | os.PathLike) -> bytes:
    """
    Load a code-compressed filesystem file, and decompress it.
    """
    with open(filePath, 'rb') as f:
        return decompress(f.read())


def decompressToFile(data: bytes, filePath: str | os.PathLike) -> None:
    """
    Decompress code-compressed data, and save it to a filesystem file.
    """
    d = decompress(data)
    with open(filePath, 'wb') as f:
        f.write(d)


def compress(data: bytes, isArm9: bool = False) -> bytes:
    """
    Compress code data. This is the inverse of decompress().
    """

    # NOTE:
    # This code is ported (with substantial changes) from
    # Nintendo DS/GBA Compressors by CUE:
    # https://gbatemp.net/threads/nintendo-ds-gba-compressors.313278/
    # http://www.romhacking.net/utilities/826/

    if isArm9:
        prefix = data[:0x4000]
        data = data[0x4000:]
    else:
        prefix = b''

    return bytes(prefix + _compress(data))


def _compress(data: bytes) -> bytearray:

    compressed, ignorableD, ignorableC = \
        _lzCommon.compress(bytes(reversed(data)), 3, 0x1002, 18, False, True)
    compressed = bytearray(reversed(compressed))

    if not compressed or (len(data) + 4 < ((len(compressed) + 3) & ~4) + 8):
        # Compressed size too large -- copy the raw data over instead

        compressed = bytearray(data)

        while len(compressed) % 4:
            compressed.append(0)

        for i in range(4):
            compressed.append(0)

        return compressed

    else:
        # Remove ignorable data (i.e. data that can remain uncompressed
        # without making the overall output file size larger), and tack
        # on the header at the end

        actualCompLen = len(compressed) - ignorableC
        headerLen = 8
        compressed = bytearray(data[:ignorableD]) + compressed[ignorableC:]
        extraLen = len(data) - len(compressed)

        while len(compressed) % 4:
            compressed.append(0xFF)
            headerLen += 1

        ptr = len(compressed)

        compressed.extend(b'\0' * 8)
        struct.pack_into('<I', compressed, ptr, actualCompLen + headerLen)
        compressed[ptr + 3] = headerLen
        ptr += 4
        struct.pack_into('<I', compressed, ptr, extraLen - headerLen)

    return compressed


def compressFromFile(filePath: str | os.PathLike, isArm9: bool = False) -> bytes:
    """
    Load a filesystem file, and compress its data in LZ10 format.
    """
    with open(filePath, 'rb') as f:
        return compress(f.read(), isArm9=isArm9)


def compressToFile(data: bytes, filePath: str | os.PathLike, isArm9: bool = False) -> None:
    """
    Compress data in LZ10 format, and save it to a filesystem file.
    """
    d = compress(data, isArm9=isArm9)
    with open(filePath, 'wb') as f:
        f.write(d)


def main(args: Sequence[str] | None = None) -> None:
    """
    Main function for the CLI
    """
    parser = argparse.ArgumentParser(
        description='ndspy.codeCompression CLI: Compress or decompress files using the code compression format.')
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

        compressToFile(data, outfp, isArm9=pArgs.is_arm9)

    parser_compress = subparsers.add_parser('compress', aliases=['c'],
                                            help='compress a file')
    parser_compress.add_argument('input_file', type=pathlib.Path,
        help='input file to compress')
    parser_compress.add_argument('output_file', nargs='?', type=pathlib.Path,
        help='what to save the compressed file as')
    parser_compress.add_argument('--is_arm9', action='store_true',
        help='treat the data as a main ARM9 code file (do not use for overlays)')
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
