from collections import defaultdict
from operator import itemgetter
import struct
from typing import Union

ByteString = Union[bytes, bytearray, memoryview]


"""
Taken from the Archipelago Metroid: Zero Mission implementation by Lil David at:
https://github.com/lilDavid/Archipelago-Metroid-Zero-Mission/blob/main/lz10.py

Tweaked version of nlzss modified to work with raw data and return bytes instead of operating on whole files.
LZ11 functionality has been removed since it is not necessary for Zero Mission nor Circle of the Moon.

https://github.com/magical/nlzss
"""


def decompress(data: ByteString):
    """Decompress LZSS-compressed bytes. Returns a bytearray containing the decompressed data."""
    header = data[:4]
    if header[0] == 0x10:
        decompress_raw = decompress_raw_lzss10
    else:
        raise DecompressionError("not as lzss-compressed file")

    decompressed_size = int.from_bytes(header[1:], "little")

    data = data[4:]
    return decompress_raw(data, decompressed_size)


def compress(data: bytearray):
    byteOut = bytearray()
    # header
    byteOut.extend(struct.pack("<L", (len(data) << 8) + 0x10))

    # body
    length = 0
    for tokens in chunkit(_compress(data), 8):
        flags = [type(t) is tuple for t in tokens]
        byteOut.extend(struct.pack(">B", packflags(flags)))

        for t in tokens:
            if type(t) is tuple:
                count, disp = t
                count -= 3
                disp = (-disp) - 1
                assert 0 <= disp < 4096
                sh = (count << 12) | disp
                byteOut.extend(struct.pack(">H", sh))
            else:
                byteOut.extend(struct.pack(">B", t))

        length += 1
        length += sum(2 if f else 1 for f in flags)

    # padding
    padding = 4 - (length % 4 or 4)
    if padding:
        byteOut.extend(b'\xff' * padding)
    return byteOut


class SlidingWindow:
    # The size of the sliding window
    size = 4096

    # The minimum displacement.
    disp_min = 2

    # The hard minimum — a disp less than this can't be represented in the
    # compressed stream.
    disp_start = 1

    # The minimum length for a successful match in the window
    match_min = 3

    # The maximum length of a successful match, inclusive.
    match_max = 3 + 0xf

    def __init__(self, buf):
        self.data = buf
        self.hash = defaultdict(list)
        self.full = False

        self.start = 0
        self.stop = 0
        # self.index = self.disp_min - 1
        self.index = 0

        assert self.match_max is not None

    def next(self):
        if self.index < self.disp_start - 1:
            self.index += 1
            return

        if self.full:
            olditem = self.data[self.start]
            assert self.hash[olditem][0] == self.start
            self.hash[olditem].pop(0)

        item = self.data[self.stop]
        self.hash[item].append(self.stop)
        self.stop += 1
        self.index += 1

        if self.full:
            self.start += 1
        else:
            if self.size <= self.stop:
                self.full = True

    def advance(self, n=1):
        """Advance the window by n bytes"""
        for _ in range(n):
            self.next()

    def search(self):
        match_max = self.match_max
        match_min = self.match_min

        counts = []
        indices = self.hash[self.data[self.index]]
        for i in indices:
            matchlen = self.match(i, self.index)
            if matchlen >= match_min:
                disp = self.index - i
                if self.disp_min <= disp:
                    counts.append((matchlen, -disp))
                    if matchlen >= match_max:
                        return counts[-1]

        if counts:
            match = max(counts, key=itemgetter(0))
            return match

        return None

    def match(self, start, bufstart):
        size = self.index - start

        if size == 0:
            return 0

        matchlen = 0
        it = range(min(len(self.data) - bufstart, self.match_max))
        for i in it:
            if self.data[start + (i % size)] == self.data[bufstart + i]:
                matchlen += 1
            else:
                break
        return matchlen


def _compress(input, windowclass=SlidingWindow):
    """Generates a stream of tokens. Either a byte (int) or a tuple of (count,
    displacement)."""

    window = windowclass(input)

    i = 0
    while True:
        if len(input) <= i:
            break
        match = window.search()
        if match:
            yield match
            window.advance(match[0])
            i += match[0]
        else:
            yield input[i]
            window.next()
            i += 1


def packflags(flags):
    n = 0
    for i in range(8):
        n <<= 1
        try:
            if flags[i]:
                n |= 1
        except IndexError:
            pass
    return n


def chunkit(it, n):
    buf = []
    for x in it:
        buf.append(x)
        if n <= len(buf):
            yield buf
            buf = []
    if buf:
        yield buf


def bits(byte):
    return ((byte >> 7) & 1,
            (byte >> 6) & 1,
            (byte >> 5) & 1,
            (byte >> 4) & 1,
            (byte >> 3) & 1,
            (byte >> 2) & 1,
            (byte >> 1) & 1,
            byte & 1)


def decompress_raw_lzss10(indata, decompressed_size, _overlay=False):
    """Decompress LZSS-compressed bytes. Returns a bytearray."""
    data = bytearray()

    it = iter(indata)

    if _overlay:
        disp_extra = 3
    else:
        disp_extra = 1

    def writebyte(b):
        data.append(b)

    def readbyte():
        return next(it)

    def readshort():
        # big-endian
        a = next(it)
        b = next(it)
        return (a << 8) | b

    def copybyte():
        data.append(next(it))

    while len(data) < decompressed_size:
        b = readbyte()
        flags = bits(b)
        for flag in flags:
            if flag == 0:
                copybyte()
            elif flag == 1:
                sh = readshort()
                count = (sh >> 0xc) + 3
                disp = (sh & 0xfff) + disp_extra

                for _ in range(count):
                    writebyte(data[-disp])
            else:
                raise ValueError(flag)

            if decompressed_size <= len(data):
                break

    if len(data) != decompressed_size:
        raise DecompressionError("decompressed size does not match the expected size")

    return data


class DecompressionError(ValueError):
    pass
