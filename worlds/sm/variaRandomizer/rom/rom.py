import base64

from ..rom.ips import IPS_Patch

def pc_to_snes(pcaddress):
    snesaddress=(((pcaddress<<1)&0x7F0000)|(pcaddress&0x7FFF)|0x8000)|0x800000
    return snesaddress

def snes_to_pc(B):
    B_1 = B >> 16
    B_2 = B & 0xFFFF
    # return 0 if invalid LoROM address
    if B_1 < 0x80 or B_1 > 0xFFFFFF or B_2 < 0x8000:
        return 0
    A_1 = (B_1 - 0x80) >> 1
    # if B_1 is even, remove most significant bit
    A_2 = B_2 & 0x7FFF if (B_1 & 1) == 0 else B_2

    return (A_1 << 16) | A_2

VANILLA_ROM_SIZE = 3145728
BANK_SIZE = 0x8000

class ROM(object):
    def __init__(self, data={}):
        self.address = 0
        self.maxAddress = VANILLA_ROM_SIZE

    def close(self):
        pass

    def seek(self, address):
        if address > self.maxAddress:
            self.maxAddress = address
        self.address = address

    def tell(self):
        if self.address > self.maxAddress:
            self.maxAddress = self.address
        return self.address

    def inc(self, n=1):
        self.address += n
        self.tell()

    def read(self, byteCount):
        pass

    def readWord(self, address=None):
        return self.readBytes(2, address)

    def readByte(self, address=None):
        return self.readBytes(1, address)

    def readLong(self, address=None):
        return self.readBytes(3, address)

    def readBytes(self, size, address=None):
        if address != None:
            self.seek(address)
        return int.from_bytes(self.read(size), byteorder='little')
    
    def write(self, bytes):
        pass

    def writeWord(self, word, address=None):
        self.writeBytes(word, 2, address)

    def writeByte(self, byte, address=None):
        self.writeBytes(byte, 1, address)

    def writeLong(self, lng, address=None):
        self.writeBytes(lng, 3, address)

    def writeBytes(self, value, size, address=None):
        if address != None:
            self.seek(address)
        self.write(value.to_bytes(size, byteorder='little'))

    def ipsPatch(self, ipsPatches):
        pass

    def fillToNextBank(self):
        off = self.maxAddress % BANK_SIZE
        if off > 0:
            self.seek(self.maxAddress + BANK_SIZE - off - 1)
            self.writeByte(0xff)
        assert (self.maxAddress % BANK_SIZE) == 0
        
class RealROM(ROM):
    def __init__(self, name):
        super(RealROM, self).__init__()
        self.romFile = open(name, "rb+")

    def seek(self, address):
        super(RealROM, self).seek(address)
        self.romFile.seek(address)

    def tell(self):
        self.address = self.romFile.tell()
        return super(RealROM, self).tell()
    
    def write(self, bytes):
        self.romFile.write(bytes)
        self.tell()

    def read(self, byteCount):
        ret = self.romFile.read(byteCount)
        self.tell()
        return ret

    def close(self):
        self.romFile.close()

    def ipsPatch(self, ipsPatches):
        for ips in ipsPatches:
            ips.applyFile(self)
