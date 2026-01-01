import itertools
from .ntype import BigStream, uint32

def calculate_crc(self):

    t1 = t2 = t3 = t4 = t5 = t6 = 0xDF26F436
    u32 = 0xFFFFFFFF

    m1 = self.read_bytes(0x1000, 0x100000)
    words = map(uint32.value, zip(m1[0::4], m1[1::4], m1[2::4], m1[3::4]))

    m2 = self.read_bytes(0x750, 0x100)
    words2 = map(uint32.value, zip(m2[0::4], m2[1::4], m2[2::4], m2[3::4]))

    for d, d2 in zip(words, itertools.cycle(words2)):
        # keep t2 and t6 in u32 for comparisons; others can wait to be truncated
        if ((t6 + d) & u32) < t6:
            t4 += 1

        t6 = (t6+d) & u32
        t3 ^= d
        shift = d & 0x1F
        r = ((d << shift) | (d >> (32 - shift)))
        t5 += r

        if t2 > d:
            t2 ^= r & u32
        else:
            t2 ^= t6 ^ d

        t1 += d2 ^ d

    crc0 = (t6 ^ t4 ^ t3) & u32
    crc1 = (t5 ^ t2 ^ t1) & u32

    return uint32.bytes(crc0) + uint32.bytes(crc1)