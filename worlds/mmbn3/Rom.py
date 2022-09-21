import re
import ndspy.lz10

mmchars = [" ", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "-", "[smallx]", "=", ":", "+", "[divide]", "[burst]", "*", "!", "?", "%", "&", ",", "[hollowbox]", ".", "[tinydot]", ";", "'", '"', "~", "/", "(", ")", "[leftJbracket]", "[rightJbracket]", "[V2]", "[V3]", "[V4]", "[V5]", "@", "[heart]", "[note]", "[MB]", "[box]", "_", "[circle1]", "[circle2]", "[cross1]", "[cross2]", "[bracket1]", "[bracket2]", "[ModTools1]", "[ModTools2]", "[ModTools3]", "[sigma]", "[omega]", "[alpha]", "[beta]", "#", "[ellipses]", ">", "<", "[weirdIthing]"]

def GetDataChunk(data, startOffset, size):
    return data[startOffset:startOffset+size]

def main():
    global rom_data
    rom_file = 'C:/Users/digiholic/Projects/BN3AP/armips/output.gba'
    with open(rom_file, "rb") as rom:
        rom_data = rom.read()
        data = GetDataChunk(rom_data, 0x759BF8, 0x4BC)
        decompData = ndspy.lz10.decompress(data)
        #data = ndspy.lz10.decompress(rom_data)
        out_file = 'C:/Users/digiholic/Projects/BN3AP/TextPet.v1.0-alpha3/ripped-decomp.bin'
        with open(out_file, "wb") as out:
            out.write(decompData)

        for byte in decompData:
            print(hex(byte))


if __name__ == "__main__": main()