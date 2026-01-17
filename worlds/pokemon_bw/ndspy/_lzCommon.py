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


def compress(data, posSubtract, maxMatchDiff, maxMatchLen, zerosAtEnd,
        searchReverse):
    """
    A configurable function suitable for all LZ-like algorithms.
    Returns the compressed data, the amount of data at the end that
    can be left uncompressed (if the format supports that, such as code
    compression), and the amount of compressed data that that data
    comprises.

    This code is primarily ported from NSMBe.
    """

    def compressionSearch(pos):
        """
        Find the longest match in `data` (nonlocal) at or after `pos`.
        This function has been rewritten in place of NSMBe's,
        to optimize its performance in Python.
        (A straight port of NSMBe's algorithm caused some files to take
        over 40 seconds to compress. With this version, all files I've
        tested take less than one second, and the compressed files
        match the old algorithm's output byte for byte.)
        """

        start = max(0, pos - maxMatchDiff)

        # Strategy: do a binary search of potential match sizes, to
        # find the longest match that exists in the data.

        lower = 0
        upper = min(maxMatchLen, len(data) - pos)

        recordMatchPos = recordMatchLen = 0
        while lower <= upper:
            # Attempt to find a match at the middle length
            matchLen = (lower + upper) // 2
            match = data[pos : pos + matchLen]
            if searchReverse:
                matchPos = data.rfind(match, start, pos)
            else:
                matchPos = data.find(match, start, pos)

            if matchPos == -1:
                # No such match -- any matches will be smaller than this
                upper = matchLen - 1
            else:
                # Match found!
                if matchLen > recordMatchLen:
                    recordMatchPos, recordMatchLen = matchPos, matchLen
                lower = matchLen + 1

        return recordMatchPos, recordMatchLen

    result = bytearray()

    current = 0 # Index of current byte to compress

    ignorableDataAmount = 0
    ignorableCompressedAmount = 0

    bestSavingsSoFar = 0

    while current < len(data):
        blockFlags = 0

        # We'll go back and fill in blockFlags at the end of the loop.
        blockFlagsOffset = len(result)
        result.append(0)
        ignorableCompressedAmount += 1

        for i in range(8):

            # Not sure if this is needed. The DS probably ignores this data.
            if current >= len(data):
                if zerosAtEnd:
                    result.append(0)
                continue

            searchPos, searchLen = compressionSearch(current)
            searchDisp = current - searchPos - posSubtract

            if searchLen > 2:
                # We found a big match; let's write a compressed block
                blockFlags |= 1 << (7 - i)

                result.append((((searchLen - 3) & 0xF) << 4) | ((searchDisp >> 8) & 0xF))
                result.append(searchDisp & 0xFF)
                current += searchLen

                ignorableDataAmount += searchLen
                ignorableCompressedAmount += 2

            else:
                result.append(data[current])
                current += 1
                ignorableDataAmount += 1
                ignorableCompressedAmount += 1

            savingsNow = current - len(result)
            if savingsNow > bestSavingsSoFar:
                ignorableDataAmount = 0
                ignorableCompressedAmount = 0
                bestSavingsSoFar = savingsNow

        result[blockFlagsOffset] = blockFlags

    return bytes(result), ignorableDataAmount, ignorableCompressedAmount