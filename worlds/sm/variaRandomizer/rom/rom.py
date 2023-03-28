import base64

from worlds.sm.variaRandomizer.rom.ips import IPS_Patch

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

class ROM(object):
    def readWord(self, address=None):
        return self.readBytes(2, address)

    def readByte(self, address=None):
        return self.readBytes(1, address)

    def readBytes(self, size, address=None):
        if address != None:
            self.seek(address)
        return int.from_bytes(self.read(size), byteorder='little')

    def writeWord(self, word, address=None):
        self.writeBytes(word, 2, address)

    def writeByte(self, byte, address=None):
        self.writeBytes(byte, 1, address)

    def writeBytes(self, value, size, address=None):
        if address != None:
            self.seek(address)
        self.write(value.to_bytes(size, byteorder='little'))
        
class RealROM(ROM):
    def __init__(self, name):
        self.romFile = open(name, "rb+")
        self.address = 0

    def seek(self, address):
        self.address = address
        self.romFile.seek(address)

    def write(self, bytes):
        self.romFile.write(bytes)

    def read(self, byteCount):
        return self.romFile.read(byteCount)

    def close(self):
        self.romFile.close()

    def ipsPatch(self, ipsPatches):
        for ips in ipsPatches:
            ips.applyFile(self)
