import itertools
import re
import ndspy.lz10
import json
import itertools

from .TextArchiveAddresses import ArchiveToReferences, ArchiveToSizeComp, ArchiveToSizeUncomp, CompressedArchives, UncompressedArchives, Commands

charDict = {
    ' ':0x00,'0':0x01,'1':0x02,'2':0x03,'3':0x04,'4':0x05,'5':0x06,'6':0x07,'7':0x08,'8':0x09,'9':0x0A,
    'A':0x0B,'B':0x0C,'C':0x0D,'D':0x0E,'E':0x0F,'F':0x10,'G':0x11,'H':0x12,'I':0x13,'J':0x14,'K':0x15,
    'L':0x16,'M':0x17,'N':0x18,'O':0x19,'P':0x1A,'Q':0x1B,'R':0x1C,'S':0x1D,'T':0x1E,'U':0x1F,'V':0x20,
    'W':0x21,'X':0x22,'Y':0x23,'Z':0x24,'a':0x25,'b':0x26,'c':0x27,'d':0x28,'e':0x29,'f':0x2A,'g':0x2B,
    'h':0x2C,'i':0x2D,'j':0x2E,'k':0x2F,'l':0x30,'m':0x31,'n':0x32,'o':0x33,'p':0x34,'q':0x35,'r':0x36,
    's':0x37,'t':0x38,'u':0x39,'v':0x3A,'w':0x3B,'x':0x3C,'y':0x3D,'z':0x3E,'-':0x3F,'×':0x40,'=':0x41,
    ':':0x42,'+':0x43,'÷':0x44,'※':0x45,'*':0x46,'!':0x47,'?':0x48,'%':0x49,'&':0x4A,',':0x4B,'⋯':0x4C,
    '.':0x4D,'・':0x4E,';':0x4F,'\'':0x50,'\"':0x51,'\~':0x52,'/':0x53,'(':0x54,')':0x55,'「':0x56,'」':0x57,
    "V2":0x58,"V3":0x59,"V4":0x5A,"V5":0x5B,'@':0x5C,'♥':0x5D,'♪':0x5E,"MB":0x5F,'■':0x60,'_':0x61,
    "circle1":0x62,"circle2":0x63,"cross1":0x64,"cross2":0x65,"bracket1":0x66,"bracket2":0x67,"ModTools1":0x68,
    "ModTools2":0x69,"ModTools3":0x6A,'Σ':0x6B,'Ω':0x6C,'α':0x6D,'β':0x6E,'#':0x6F,'…':0x70,'>':0x71,
    '<':0x72,'エ':0x73,"BowneGlobal1":0x74,"BowneGlobal2":0x75,"BowneGlobal3":0x76,"BowneGlobal4":0x77,
    "BowneGlobal5":0x78,"BowneGlobal6":0x79,"BowneGlobal7":0x7A,"BowneGlobal8":0x7B,"BowneGlobal9":0x7C,
    "BowneGlobal10":0x7D,"BowneGlobal11":0x7E,'\n':0xE8
}

rom_data: bytearray
modified_rom_data: bytearray

giveChipBytes = [0xF6, 0x10]
giveItemBytes = [0xF6, 0x20]
giveZennyBytes = [0xF6, 0x30]
giveProgramBytes = [0xF6, 0x40]
giveBugFragBytes = [0xF6, 0x50]


def read_u16_le(data, offset) -> int:
    low_byte = data[offset]
    high_byte = data[offset+1]
    return (high_byte << 8) + low_byte


def int32ToByteList_le(x) -> bytearray:
    byte32_string = "{:08x}".format(x)
    data = bytearray.fromhex(byte32_string)
    data.reverse()
    return data


def int16ToByteList_le(x) -> bytearray:
    byte32_string = "{:04x}".format(x)
    data = bytearray.fromhex(byte32_string)
    data.reverse()
    return data


def GenerateTextBytes(message) -> bytearray:
    byteList = []
    for c in message:
        byteList.append(charDict[c])
    return bytearray(byteList)

def GenerateChipGet(chip, code, amt) -> bytearray:
    chipBytes = int16ToByteList_le(chip)
    byteList = [
        0xF6, 0x10, chipBytes[0], chipBytes[1], code, amt,
        charDict['G'], charDict['o'], charDict['t'], charDict[' '], charDict['a'], charDict[' '], charDict['c'], charDict['h'], charDict['i'], charDict['p'], charDict[' '], charDict['f'], charDict['o'], charDict['r'], charDict['\n'],
    ]
    byteList.extend([
        charDict['\"'], 0xF9, 0x00, chipBytes[0], 0x01 if chip < 256 else 0x02, 0x00, 0xF9, 0x00, code, 0x03, charDict['\"'], charDict['!'], charDict['!']
    ])
    return bytearray(byteList)

def GenerateKeyItemGet(item, amt) -> bytearray:
    byteList = [
        0xF6, 0x00, item, amt,
        charDict['G'], charDict['o'], charDict['t'], charDict[' '], charDict['a'], charDict['\n'],
        charDict['\"'], 0xF9, 0x00, item, 0x00, charDict['\"'],charDict['!'],charDict['!']
    ]
    return bytearray(byteList)

def GenerateSubChipGet(subchip, amt) -> bytearray:
    #SubChips have an extra bit of trouble. If you have too many, they're supposed to skip to another text bank that doesn't give you the item
    #Instead, I'm going to just let it get eaten
    byteList = [
        0xF6, 0x20, subchip, amt, 0xFF, 0xFF, 0xFF,
        charDict['G'], charDict['o'], charDict['t'], charDict[' '], charDict['a'], charDict['\n'],
        charDict['S'], charDict['u'], charDict['b'], charDict['C'], charDict['h'], charDict['i'], charDict['p'], charDict[' '], charDict['f'], charDict['o'], charDict['r'], charDict['\n'],
        charDict['\"'], 0xF9, 0x00, subchip, 0x00, charDict['\"'],charDict['!'],charDict['!']
    ]
    return bytearray(byteList)

def GenerateZennyGet(amt) -> bytearray:
    zennyBytes = int32ToByteList_le(amt)
    byteList = [
        0xF6, 0x30, zennyBytes[1], zennyBytes[2], zennyBytes[3], zennyBytes[4], 0xFF, 0xFF, 0xFF,
        charDict['G'], charDict['o'], charDict['t'], charDict[' '], charDict['a'], charDict['\n'], charDict['\"']
    ]
    #The text needs to be added one char at a time, so we need to convert the number to a string then iterate through it
    zennyStr = str(amt)
    for c in zennyStr:
        byteList.append(charDict[c])
    byteList.extend([
        charDict[' '], charDict['Z'], charDict['e'], charDict['n'], charDict['n'], charDict['y'], charDict['s'], charDict['\"'],charDict['!'],charDict['!']
    ])
    return bytearray(byteList)

def GenerateProgramGet(program, color, amt) -> bytearray:
    byteList = [
        0xF6, 0x40, program, color, amt,
        charDict['G'], charDict['o'], charDict['t'], charDict[' '], charDict['a'], charDict[' '], charDict['N'], charDict['a'], charDict['v'], charDict['i'], charDict['\n'],
        charDict['C'], charDict['u'], charDict['s'], charDict['t'], charDict['o'], charDict['m'], charDict['i'], charDict['z'], charDict['e'], charDict['r'], charDict[' '], charDict['P'], charDict['r'], charDict['o'], charDict['g'], charDict['r'], charDict['a'], charDict['m'], charDict[':'], charDict['\n'],
        charDict['\"'], 0xF9, 0x00, program, 0x05, charDict['\"'],charDict['!'],charDict['!']
    ]
    return bytearray(byteList)

def GenerateBugfragGet(amt) -> bytearray:
    fragBytes = int32ToByteList_le(amt)
    byteList = [
        0xF6, 0x50, fragBytes[1], fragBytes[2], fragBytes[3], fragBytes[4], 0xFF, 0xFF, 0xFF,
        charDict['G'], charDict['o'], charDict['t'], charDict[':'], charDict['\n'], charDict['\"']
    ]
    #The text needs to be added one char at a time, so we need to convert the number to a string then iterate through it
    bugFragStr = str(amt)
    for c in bugFragStr:
        byteList.append(charDict[c])
    byteList.extend([
        charDict[' '], charDict['B'], charDict['u'], charDict['g'], charDict['F'], charDict['r'], charDict['a'], charDict['g'], charDict['s'],charDict['\"'],charDict['!'],charDict['!']
    ])
    return bytearray(byteList)

def GenerateGetMessageFromItem(item) -> bytearray:
    #Special case for progressive undernet
    #if item["type"] == "progressive-undernet":
        #return GenerateKeyItemGet(Next_Progressive_Undernet_ID(),1)
    if item.type == "chip":
        return GenerateChipGet(item.itemID, item.subItemID, item.count)
    elif item.type == "key":
        return GenerateKeyItemGet(item.itemID, item.count)
    elif item.type == "subchip":
        return GenerateSubChipGet(item.itemID, item.count)
    elif item.type == "zenny":
        return GenerateZennyGet(item.count)
    elif item.type == "program":
        return GenerateProgramGet(item.itemID, item.subItemID, item.count)
    elif item.type == "bugfrag":
        return GenerateBugfragGet(item.count)

    return GenerateTextBytes("Empty Message")

def GenerateItemMessage(itemData) -> bytearray:
    byteList = [0xF8, 0x04, 0x18]
    byteList.extend(GenerateGetMessageFromItem(itemData))
    byteList.extend([0xF8, 0x0C])
    byteList.extend([0xEB, 0xF8, 0x08])
    byteList.extend([0xF8, 0x10])
    return bytearray(byteList)

def list_contains_subsequence(list, sublist) -> bool:
    subIndex = 0
    for index, item in enumerate(list):
        if item == sublist[subIndex]:
            subIndex += 1
            if subIndex >= len(sublist):
                return True
        else:
            subIndex = 0
    return False


class ArchiveScript:
    def __init__(self, index, messageBytes):
        self.index = index
        self.messageBoxes = []

        messageBox = []

        commandIndex = 0
        for byte in messageBytes:
            if commandIndex <= 0 and (byte == 0xE9 or byte == 0xE7):
                if byte == 0xE9: # More textboxes to come, don't end it yet
                    messageBox.append(byte)
                    self.messageBoxes.append(messageBox)
                else: # It's the end of the script, add another message to end it after this one
                    self.messageBoxes.append(messageBox)
                    self.messageBoxes.append([0xE7])
                messageBox = []

            else:
                # We can hit a command that might contain an E9 or an E7. If we do, skip checking the next 6 bytes
                if byte == 0xF6:
                    commandIndex = 7
                commandIndex -= 1
                messageBox.append(byte)
        # If there's still bytes left over, add them even if we didn't hit an end
        if (len(messageBox) > 0):
            self.messageBoxes.append(messageBox)
            messageBox = []

    def GetBytes(self):
        data = []
        for message in self.messageBoxes:
            data.extend(message)
        return data

    def __str__(self):
        s = str(self.index)+' - \n'
        for messageBox in self.messageBoxes:
            s += '  '+str(["{:02x}".format(x) for x in messageBox])+'\n'


class TextArchive:
    def __init__(self, offset, size, compressed=True):
        self.startOffset = offset
        self.compressed = compressed
        self.scripts = {}
        self.scriptCount = 0xFF
        self.references = ArchiveToReferences[offset]

        if compressed:
            self.compressedSize = size
            self.compressedData = GetDataChunk(rom_data, offset, size)
            self.uncompressedData = ndspy.lz10.decompress(self.compressedData)
            self.uncompressedSize = len(self.uncompressedData)
        else:
            self.uncompressedSize = size
            self.uncompressedData = GetDataChunk(rom_data, offset, size)
            self.compressedData = ndspy.lz10.compress(self.uncompressedData)
            self.compressedSize = len(self.compressedData)
        self.scriptCount = (read_u16_le(self.uncompressedData, 0)) >> 1

        for i in range(0, self.scriptCount):
            start = read_u16_le(self.uncompressedData, i*2)
            next = read_u16_le(self.uncompressedData, (i+1)*2)
            if start != next:
                messageBytes = list(self.uncompressedData[start:next])
                #messageBytes = list(itertools.takewhile(lambda b: b != 0xE7, self.uncompressedData[start:]))
                #messageBytes.append(0xE7)
                message = ArchiveScript(i, messageBytes)
                self.scripts[i] = message

    def GenerateData(self, compressed=True):
        header = []
        scripts = []
        byteOffset = self.scriptCount * 2
        for i in range(0, self.scriptCount):
            header.extend(int16ToByteList_le(byteOffset))
            if i in self.scripts:
                script = self.scripts[i]
                scriptbytes = script.GetBytes()
                scripts.extend(scriptbytes)
                byteOffset += len(scriptbytes)

        data = []
        data.extend(header)
        data.extend(scripts)
        byteData = bytes(data)
        if compressed:
            byteData = ndspy.lz10.compress(byteData)

        return byteData

    def InjectItemMessage(self, scriptIndex, messageIndex, newBytes):
        # First step, if the old message had any flag sets, we need to keep them.
        # Mystery data has a flag set to actually remove the mystery data, and jobs often have a completion flag
        oldbytes = self.scripts[scriptIndex].messageBoxes[messageIndex]
        for i in range(len(oldbytes)-3):
            # F2 00 is the code for "flagSet", with the two bytes after it being the flag to set. Add those to the message box.
            if oldbytes[i] == 0xF2 and oldbytes[i+1] == 0x00:
                flag = oldbytes[i:i+4]
                newBytes.extend(flag)

        self.scripts[scriptIndex].messageBoxes[messageIndex] = newBytes

    def InjectIntoRom(self):
        global modified_rom_data

        originalSize = self.compressedSize if self.compressed else self.uncompressedSize
        # with open("C:/Users/digiholic/Projects/BN3AP/Patches/temp.bin","wb") as temp:
           # temp.write(self.GenerateData(False))

        workingData = self.GenerateData(self.compressed)

        if len(workingData) < originalSize:
            # If it's shorter than the original data, we can pad the difference with FF and directrly replace
            workingData.extend([0xFF] * (originalSize - len(workingData)))
            modified_rom_data[self.startOffset:self.startOffset+len(workingData)] = workingData
        else:
            # It needs to start on an even byte. If the rom data is odd, add an FF
            if (len(modified_rom_data) % 2 != 0):
                modified_rom_data.append(0xFF)
            newStartOffset = 0x08000000 + len(modified_rom_data)
            offsetByte = int32ToByteList_le(newStartOffset)
            modified_rom_data.extend(workingData)
            for offset in self.references:
                oldBytes = list(modified_rom_data[offset:offset+4])
                print(oldBytes)
                modified_rom_data[offset:offset+4] = offsetByte
                oldBytes = list(modified_rom_data[offset:offset + 4])
                print(oldBytes)




def GetDataChunk(data, startOffset, size):
    return data[startOffset:startOffset+size]


def ReplaceItem(location, item):
    offset = location.text_archive_address
    size = 0
    archive = None
    if (CompressedArchives.__contains__(offset)):
        size = ArchiveToSizeComp[offset]
        archive = TextArchive(offset, size, True)
    else:
        size = ArchiveToSizeUncomp[offset]
        archive = TextArchive(offset, size, False)
    archive.InjectItemMessage(location.text_script_index, location.text_box_index, GenerateItemMessage(item))
    archive.InjectIntoRom()

def read_rom(path):
    global rom_data
    global modified_rom_data
    with open(path, "rb") as rom:
        rom_data = bytearray(rom.read())
        modified_rom_data = bytearray(rom_data[:])

def write_rom(path):
    global modified_rom_data
    with open(path, "wb") as rom:
        rom.write(modified_rom_data)