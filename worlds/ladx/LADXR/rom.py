import bsdiff4
import binascii
import Utils

b2h = binascii.hexlify
h2b = binascii.unhexlify


class ROM:
    def __init__(self, data, patches=None):
        if patches:
            for patch in patches:
                data = bsdiff4.patch(data, patch)

        self.banks = []
        for n in range(0x40):
            self.banks.append(bytearray(data[n*0x4000:(n+1)*0x4000]))

    def patch(self, bank_nr, addr, old, new, *, fill_nop=False):
        new = h2b(new)
        bank = self.banks[bank_nr]
        if old is not None:
            if isinstance(old, int):
                old = bank[addr:old]
            else:
                old = h2b(old)
            if fill_nop:
                assert len(old) >= len(new), "Length mismatch: %d != %d (%s != %s)" % (len(old), len(new), b2h(old), b2h(new))
                new += b'\x00' * (len(old) - len(new))
            else:
                assert len(old) == len(new), "Length mismatch: %d != %d (%s != %s)" % (len(old), len(new), b2h(old), b2h(new))
            assert addr >= 0 and addr + len(old) <= 16*1024
            if bank[addr:addr+len(old)] != old:
                if bank[addr:addr + len(old)] == new:
                    # Patch is already applied.
                    return
                loc = bank.find(old)
                while loc > -1:
                    print("Possible at:", hex(loc))
                    loc = bank.find(old, loc+1)
                assert False, "Patch mismatch:\n%s !=\n%s at 0x%04x" % (b2h(bank[addr:addr+len(old)]), b2h(old), addr)
        bank[addr:addr+len(new)] = new
        assert len(bank) == 0x4000

    def fixHeader(self, *, name=None):
        if name is not None:
            name = name.encode("utf-8")
            name = (name + (b"\x00" * 15))[:15]
            self.banks[0][0x134:0x143] = name

        checksum = 0
        for c in self.banks[0][0x134:0x14D]:
            checksum -= c + 1
        self.banks[0][0x14D] = checksum & 0xFF

        # zero out the checksum before calculating it.
        self.banks[0][0x14E] = 0
        self.banks[0][0x14F] = 0
        checksum = 0
        for bank in self.banks:
            checksum = (checksum + sum(bank)) & 0xFFFF
        self.banks[0][0x14E] = checksum >> 8
        self.banks[0][0x14F] = checksum & 0xFF

    def save(self):
        # don't pass the name to fixHeader
        self.fixHeader()
        return b"".join(self.banks)

    def readHexSeed(self):
        return self.banks[0x3E][0x2F00:0x2F10].hex().upper()
