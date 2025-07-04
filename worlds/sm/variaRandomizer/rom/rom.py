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

class FakeROM(ROM):
    # to have the same code for real ROM and the webservice
    def __init__(self, data=None):
        super(FakeROM, self).__init__()
        if data is None:
            self.data = {}
        else:
            self.data = data
        self.ipsPatches = []

    def write(self, bytes):
        for byte in bytes:
            self.data[self.address] = byte
            self.inc()

    def read(self, byteCount):
        bytes = []
        for i in range(byteCount):
            bytes.append(self.data[self.address])
            self.inc()

        return bytes

    def ipsPatch(self, ipsPatches):
        self.ipsPatches += ipsPatches

    # generate ips from self data
    def ips(self):
        groupedData = {}
        startAddress = -1
        prevAddress = -1
        curData = []
        for address in sorted(self.data):
            if address == prevAddress + 1:
                curData.append(self.data[address])
                prevAddress = address
            else:
                if len(curData) > 0:
                    groupedData[startAddress] = curData
                startAddress = address
                prevAddress = address
                curData = [self.data[startAddress]]
        if startAddress != -1:
            groupedData[startAddress] = curData

        return IPS_Patch(groupedData)

    # generate final IPS for web patching with first the IPS patches, then written data
    def close(self):
        self.mergedIPS = IPS_Patch()
        for ips in self.ipsPatches:
            self.mergedIPS.append(ips)
        self.mergedIPS.append(self.ips())
        #patchData = mergedIPS.encode()
        #self.data = {}
        #self.data["ips"] = base64.b64encode(patchData).decode()
        #if mergedIPS.truncate_length is not None:
        #    self.data["truncate_length"] = mergedIPS.truncate_length
        #self.data["max_size"] = mergedIPS.max_size

    def getPatchDict(self):
        return self.mergedIPS.toDict()
                
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
